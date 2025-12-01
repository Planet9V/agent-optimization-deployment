#!/usr/bin/env python3
"""
Process pipe-delimited CVE-CWE data into NER training format
Clean extraction with proper entity annotation
"""

import json
import re
from typing import List, Dict
from pathlib import Path

def extract_entities(text: str) -> List[Dict]:
    """Extract cybersecurity entities from text"""
    entities = []

    # 1. CVE IDs (VULNERABILITY)
    for match in re.finditer(r'CVE-\d{4}-\d{4,7}', text):
        entities.append({
            "start": match.start(),
            "end": match.end(),
            "label": "VULNERABILITY",
            "text": match.group()
        })

    # 2. CWE IDs (WEAKNESS)
    for match in re.finditer(r'CWE-\d+', text):
        entities.append({
            "start": match.start(),
            "end": match.end(),
            "label": "WEAKNESS",
            "text": match.group()
        })

    # 3. Software/Products (SOFTWARE)
    software_patterns = [
        (r'Microsoft Windows [A-Za-z0-9\s]+?(?:SP\d+)?(?=,|\sand\s|\.|$)', 'Microsoft Windows'),
        (r'Windows (?:XP|Vista|7|8|10|11|Server\s+\d{4})\s*(?:SP\d+|R\d+)?', 'Windows Version'),
        (r'(?:Apache|Oracle|Cisco|Linux|OpenSSL|nginx|Docker) [A-Za-z0-9\s\.]+?(?=,|\.|$|version)', 'Server Software'),
        (r'VLC Media Player', 'VLC'),
        (r'VideoLAN', 'VideoLAN'),
        (r'Zope', 'Zope'),
        (r'Plone', 'Plone'),
        (r'SoMachine Basic', 'SoMachine'),
        (r'Modicon M\d+', 'Modicon PLC'),
        (r'Micro Focus [A-Za-z\s]+?(?=,|\.|$|version|and)', 'Micro Focus'),
        (r'Enterprise (?:Server|Developer)', 'Enterprise Software'),
        (r'win32k\.sys', 'win32k.sys'),
        (r'kernel-mode drivers?', 'kernel driver')
    ]

    for pattern, label in software_patterns:
        for match in re.finditer(pattern, text):
            # Avoid overlapping matches
            if not any(e['start'] <= match.start() < e['end'] for e in entities):
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": "SOFTWARE",
                    "text": match.group().strip()
                })

    # 4. Protocols (PROTOCOL)
    protocols = ['HTTP', 'HTTPS', 'FTP', 'FTPS', 'SSH', 'SSL', 'TLS', 'TCP', 'UDP', 'IP', 'ICMP', 'DNS', 'SMTP', 'POP3', 'IMAP', 'Ethernet']
    for proto in protocols:
        for match in re.finditer(rf'\b{proto}\b', text):
            if not any(e['start'] <= match.start() < e['end'] for e in entities):
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": "PROTOCOL",
                    "text": match.group()
                })

    # 5. Versions (VERSION)
    version_patterns = [
        r'\bv?\d+\.\d+(?:\.\d+)?(?:\.\d+)?\b',
        r'\bSP\d+\b',
        r'\bR\d+\b',
        r'\bversion\s+\d+(?:\.\d+)*',
        r'\bfirmware\s+V\d+(?:\.\d+)*'
    ]

    for pattern in version_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            if not any(e['start'] <= match.start() < e['end'] for e in entities):
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": "VERSION",
                    "text": match.group().strip()
                })

    # Sort by position
    entities.sort(key=lambda x: x['start'])
    return entities

def main():
    input_file = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/ner_training/raw_cve_cwe_pipe.txt")
    output_file = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/ner_training/v7_cve_cwe_mappings.json")

    examples = []
    skipped = 0
    processed = 0

    print(f"Processing {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip().strip('"')

            # Split by delimiter
            parts = line.split('|||||')

            if len(parts) < 5:
                skipped += 1
                continue

            cve_id = parts[0].strip()
            cve_desc = parts[1].strip()
            cwe_id = parts[2].strip()
            cwe_name = parts[3].strip()
            cwe_desc = parts[4].strip() if len(parts) > 4 else ''

            # Skip if description too short
            if len(cve_desc) < 50:
                skipped += 1
                continue

            # Format CWE ID
            if not cwe_id.startswith('CWE-'):
                cwe_id = f'CWE-{cwe_id}'

            # Create full annotated text
            full_text = f"{cve_desc} This vulnerability is classified as {cwe_id} ({cwe_name})."

            # Extract entities from CVE description
            entities = extract_entities(cve_desc)

            # Add CWE reference entity
            cwe_pos = len(cve_desc) + len(" This vulnerability is classified as ")
            entities.append({
                "start": cwe_pos,
                "end": cwe_pos + len(cwe_id),
                "label": "WEAKNESS",
                "text": cwe_id
            })

            # Only include if we have meaningful entities
            if len(entities) >= 2:
                examples.append({
                    "text": full_text,
                    "entities": entities,
                    "metadata": {
                        "cve_id": cve_id,
                        "cwe_id": cwe_id,
                        "cwe_name": cwe_name,
                        "entity_count": len(entities),
                        "entity_types": sorted(list(set(e['label'] for e in entities)))
                    }
                })
                processed += 1
            else:
                skipped += 1

            if processed >= 1000:
                break

    # Calculate entity statistics
    entity_stats = {}
    for ex in examples:
        for ent in ex['entities']:
            label = ent['label']
            entity_stats[label] = entity_stats.get(label, 0) + 1

    # Count unique CWEs
    unique_cwes = len(set(ex['metadata']['cwe_id'] for ex in examples))

    # Save to JSON
    output_data = {
        "dataset_info": {
            "name": "CVE-CWE NER Training Dataset",
            "version": "7.0",
            "description": "Named Entity Recognition training data extracted from CVE-CWE relationship mappings in OpenSPG knowledge graph",
            "total_examples": len(examples),
            "unique_cwe_types": unique_cwes,
            "entity_types": ["VULNERABILITY", "WEAKNESS", "SOFTWARE", "PROTOCOL", "VERSION"],
            "source": "Neo4j OpenSPG Database - CVE-CWE Relationships (64,224 total mappings sampled)",
            "extraction_date": "2025-11-08",
            "use_case": "Training spaCy NER models for cybersecurity entity recognition"
        },
        "examples": examples
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\n{'='*60}")
    print("✅ EXTRACTION COMPLETE!")
    print(f"{'='*60}")
    print(f"📊 Total examples: {len(examples)}")
    print(f"🗑️  Skipped: {skipped}")
    print(f"🎯 Unique CWE types: {unique_cwes}")
    print(f"\n📈 Entity Distribution:")
    for label in sorted(entity_stats.keys()):
        print(f"   {label:13} : {entity_stats[label]:5} entities")
    print(f"\n💾 Output file: {output_file}")
    print(f"📏 File size: {output_file.stat().st_size / 1024:.1f} KB")
    print(f"{'='*60}")

    # Show sample
    print(f"\n📝 SAMPLE EXAMPLE:")
    if examples:
        sample = examples[min(15, len(examples)-1)]  # Get a middle example for variety
        print(f"CVE: {sample['metadata']['cve_id']}")
        print(f"CWE: {sample['metadata']['cwe_id']} - {sample['metadata']['cwe_name']}")
        print(f"Text: {sample['text'][:150]}...")
        print(f"\nEntities ({len(sample['entities'])}):")
        for ent in sample['entities'][:8]:
            print(f"  [{ent['label']:13}] \"{ent['text']}\"")

if __name__ == "__main__":
    main()
