#!/usr/bin/env python3
"""
Extract CVE-CWE mappings directly to NER training format
Handles CSV format correctly with proper quoting
"""

import json
import re
from typing import List, Dict
from pathlib import Path

def extract_entities(text: str) -> List[Dict]:
    """Extract entities from text"""
    entities = []

    # CVE IDs
    for match in re.finditer(r'CVE-\d{4}-\d{4,7}', text):
        entities.append({
            "start": match.start(),
            "end": match.end(),
            "label": "VULNERABILITY",
            "text": match.group()
        })

    # CWE IDs
    for match in re.finditer(r'CWE-\d+', text):
        entities.append({
            "start": match.start(),
            "end": match.end(),
            "label": "WEAKNESS",
            "text": match.group()
        })

    # Software products
    software_patterns = [
        r'Microsoft Windows [A-Za-z0-9\s]+?(?=,|\.|$)',
        r'Windows (?:XP|Vista|7|8|10|11|Server)',
        r'(?:Apache|Oracle|Cisco|Linux|OpenSSL|VLC|Zope|Plone|VideoLAN|Micro Focus) [A-Za-z0-9\s]+?(?=,|\.|$)',
        r'win32k\.sys',
        r'SoMachine Basic',
        r'Modicon M\d+',
        r'Enterprise (?:Server|Developer)',
        r'kernel-mode drivers'
    ]

    for pattern in software_patterns:
        for match in re.finditer(pattern, text):
            # Avoid nested captures
            if not any(e['start'] <= match.start() < e['end'] for e in entities):
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": "SOFTWARE",
                    "text": match.group().strip()
                })

    # Protocols
    for match in re.finditer(r'\b(HTTP|HTTPS|FTP|SSH|SSL|TLS|TCP|UDP|IP|Ethernet)\b', text):
        if not any(e['start'] <= match.start() < e['end'] for e in entities):
            entities.append({
                "start": match.start(),
                "end": match.end(),
                "label": "PROTOCOL",
                "text": match.group()
            })

    # Version numbers
    for match in re.finditer(r'(?:v?|\bversion\s+)\d+\.\d+(?:\.\d+)?(?:\.\d+)?|SP\d+|R\d+(?:\s+SP\d+)?', text, re.IGNORECASE):
        if not any(e['start'] <= match.start() < e['end'] for e in entities):
            entities.append({
                "start": match.start(),
                "end": match.end(),
                "label": "VERSION",
                "text": match.group().strip()
            })

    entities.sort(key=lambda x: x['start'])
    return entities

def parse_csv_line(line: str) -> Dict:
    """Parse a single CSV line handling quoted fields with commas"""
    import csv
    import io

    reader = csv.reader(io.StringIO(line))
    row = next(reader, [])

    if len(row) >= 5:
        return {
            'cve_id': row[0].strip(),
            'cve_desc': row[1].strip(),
            'cwe_id': row[2].strip(),
            'cwe_name': row[3].strip(),
            'cwe_desc': row[4].strip() if len(row) > 4 else ''
        }
    return None

def main():
    input_file = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/ner_training/raw_cve_cwe_plain.txt")
    output_file = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/ner_training/v7_cve_cwe_mappings.json")

    examples = []
    skipped = 0

    print(f"Processing {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        # Skip header
        next(f)

        for line_num, line in enumerate(f, 2):
            data = parse_csv_line(line)

            if not data or len(data['cve_desc']) < 50:
                skipped += 1
                continue

            # Format CWE ID
            cwe_id = data['cwe_id']
            if not cwe_id.startswith('CWE-'):
                cwe_id = f'CWE-{cwe_id}'

            # Create full text with CWE classification
            full_text = f"{data['cve_desc']} This vulnerability is classified as {cwe_id} ({data['cwe_name']})."

            # Extract entities
            entities = extract_entities(data['cve_desc'])

            # Add CWE reference
            cwe_start = len(data['cve_desc']) + len(" This vulnerability is classified as ")
            entities.append({
                "start": cwe_start,
                "end": cwe_start + len(cwe_id),
                "label": "WEAKNESS",
                "text": cwe_id
            })

            if len(entities) >= 3:
                examples.append({
                    "text": full_text,
                    "entities": entities,
                    "metadata": {
                        "cve_id": data['cve_id'],
                        "cwe_id": cwe_id,
                        "cwe_name": data['cwe_name'],
                        "entity_count": len(entities),
                        "entity_types": sorted(list(set(e['label'] for e in entities)))
                    }
                })
            else:
                skipped += 1

            if len(examples) >= 1000:
                break

    # Entity statistics
    entity_counts = {}
    for ex in examples:
        for ent in ex['entities']:
            label = ent['label']
            entity_counts[label] = entity_counts.get(label, 0) + 1

    # Save output
    output_data = {
        "dataset_info": {
            "name": "CVE-CWE NER Training Dataset",
            "version": "7.0",
            "description": "Named Entity Recognition training data from CVE-CWE relationship mappings",
            "total_examples": len(examples),
            "entity_types": ["VULNERABILITY", "WEAKNESS", "SOFTWARE", "PROTOCOL", "VERSION"],
            "source": "Neo4j OpenSPG Database - CVE-CWE Relationships (64,224 total mappings)",
            "extraction_date": "2025-11-08"
        },
        "examples": examples
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ COMPLETE!")
    print(f"Total examples: {len(examples)}")
    print(f"Skipped: {skipped}")
    print(f"\n📊 Entity Distribution:")
    for label in sorted(entity_counts.keys()):
        print(f"  {label}: {entity_counts[label]}")
    print(f"\n💾 Output: {output_file}")
    print(f"📏 File size: {output_file.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
