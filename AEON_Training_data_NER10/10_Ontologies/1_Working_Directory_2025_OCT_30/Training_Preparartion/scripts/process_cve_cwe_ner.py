#!/usr/bin/env python3
"""
Process CVE-CWE data into NER training format
Extracts entities: VULNERABILITY (CVE), WEAKNESS (CWE), SOFTWARE, PROTOCOL, VERSION
"""

import csv
import json
import re
from typing import List, Dict, Tuple
from pathlib import Path

def extract_entities_from_text(text: str, cve_id: str, cwe_id: str) -> List[Dict]:
    """Extract all entities from CVE description text"""
    entities = []

    # 1. CVE IDs (both primary and referenced)
    cve_pattern = r'CVE-\d{4}-\d{4,7}'
    for match in re.finditer(cve_pattern, text):
        entities.append({
            "start": match.start(),
            "end": match.end(),
            "label": "VULNERABILITY",
            "text": match.group()
        })

    # 2. CWE IDs (from text and parameter)
    cwe_pattern = r'CWE-\d+'
    for match in re.finditer(cwe_pattern, text):
        entities.append({
            "start": match.start(),
            "end": match.end(),
            "label": "WEAKNESS",
            "text": match.group()
        })

    # 3. Software/Products (common patterns)
    software_patterns = [
        r'Microsoft Windows [A-Z][A-Za-z0-9\s]+',
        r'Windows (XP|Vista|7|8|10|11|Server \d{4})',
        r'Linux [A-Za-z0-9\s]+',
        r'Apache [A-Za-z0-9\s]+',
        r'Oracle [A-Za-z0-9\s]+',
        r'Cisco [A-Za-z0-9\s]+',
        r'OpenSSL',
        r'VLC Media Player',
        r'Zope',
        r'Plone',
        r'VideoLAN',
        r'Micro Focus [A-Za-z\s]+',
        r'win32k\.sys',
        r'kernel-mode drivers'
    ]

    for pattern in software_patterns:
        for match in re.finditer(pattern, text):
            entities.append({
                "start": match.start(),
                "end": match.end(),
                "label": "SOFTWARE",
                "text": match.group()
            })

    # 4. Protocols
    protocol_patterns = [
        r'\b(HTTP|HTTPS|FTP|SSH|SSL|TLS|TCP|UDP|IP)\b',
        r'Ethernet/IP'
    ]

    for pattern in protocol_patterns:
        for match in re.finditer(pattern, text):
            entities.append({
                "start": match.start(),
                "end": match.end(),
                "label": "PROTOCOL",
                "text": match.group()
            })

    # 5. Version numbers
    version_patterns = [
        r'SP\d+',
        r'v?\d+\.\d+(?:\.\d+)?(?:\.\d+)?',
        r'R\d+',
        r'before version \d+\.\d+(?:\.\d+)?'
    ]

    for pattern in version_patterns:
        for match in re.finditer(pattern, text):
            # Avoid overlapping with already matched entities
            if not any(e['start'] <= match.start() < e['end'] for e in entities):
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": "VERSION",
                    "text": match.group()
                })

    # Sort by start position
    entities.sort(key=lambda x: x['start'])

    return entities

def create_ner_example(cve_id: str, cve_desc: str, cwe_id: str, cwe_name: str, cwe_desc: str) -> Dict:
    """Create a single NER training example"""

    # Combine CVE description with CWE context for richer training data
    full_text = f"{cve_desc} This vulnerability is classified as {cwe_id} ({cwe_name})."

    # Extract entities
    entities = extract_entities_from_text(cve_desc, cve_id, cwe_id)

    # Add CWE reference at end
    cwe_start = len(cve_desc) + len(" This vulnerability is classified as ")
    entities.append({
        "start": cwe_start,
        "end": cwe_start + len(cwe_id),
        "label": "WEAKNESS",
        "text": cwe_id
    })

    return {
        "text": full_text,
        "entities": entities,
        "metadata": {
            "cve_id": cve_id,
            "cwe_id": cwe_id,
            "cwe_name": cwe_name,
            "entity_count": len(entities),
            "entity_types": list(set(e['label'] for e in entities))
        }
    }

def process_csv_to_ner(input_file: Path, output_file: Path, max_examples: int = 2000):
    """Process raw CSV data into NER training format"""

    examples = []
    skipped = 0

    print(f"Processing {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        # Skip header
        next(reader)

        for row in reader:
            if len(row) < 5:
                skipped += 1
                continue

            cve_id = row[0].strip(' "')
            cve_desc = row[1].strip(' "')
            cwe_id = row[2].strip(' "')
            cwe_name = row[3].strip(' "')
            cwe_desc = row[4].strip(' "')

            # Skip deprecated or empty entries
            if 'DEPRECATED' in cwe_name or len(cve_desc) < 50:
                skipped += 1
                continue

            # Format CWE ID properly
            if not cwe_id.startswith('CWE-'):
                cwe_id = f'CWE-{cwe_id}'

            # Create NER example
            example = create_ner_example(cve_id, cve_desc, cwe_id, cwe_name, cwe_desc)

            # Only include examples with meaningful entities
            if len(example['entities']) >= 3:
                examples.append(example)
            else:
                skipped += 1

            if len(examples) >= max_examples:
                break

    # Save to JSON
    output_data = {
        "dataset_info": {
            "name": "CVE-CWE NER Training Dataset",
            "version": "7.0",
            "description": "Named Entity Recognition training data extracted from CVE-CWE mappings",
            "total_examples": len(examples),
            "entity_types": ["VULNERABILITY", "WEAKNESS", "SOFTWARE", "PROTOCOL", "VERSION"],
            "source": "Neo4j OpenSPG CVE-CWE relationships"
        },
        "examples": examples
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    # Statistics
    entity_type_counts = {}
    for example in examples:
        for entity in example['entities']:
            label = entity['label']
            entity_type_counts[label] = entity_type_counts.get(label, 0) + 1

    print(f"\n✅ Processing complete!")
    print(f"Total examples: {len(examples)}")
    print(f"Skipped: {skipped}")
    print(f"\nEntity type distribution:")
    for entity_type, count in sorted(entity_type_counts.items()):
        print(f"  {entity_type}: {count}")
    print(f"\nOutput: {output_file}")

if __name__ == "__main__":
    input_file = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/ner_training/raw_cve_cwe_data.txt")
    output_file = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/ner_training/v7_cve_cwe_mappings.json")

    process_csv_to_ner(input_file, output_file, max_examples=2000)
