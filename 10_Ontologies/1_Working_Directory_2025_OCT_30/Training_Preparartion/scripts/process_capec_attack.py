#!/usr/bin/env python3
"""
Process Neo4j CAPEC→ATT&CK extraction into NER training format.
Reads raw Neo4j output and creates JSON training data.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set

def parse_neo4j_output(filepath: str) -> List[Dict]:
    """Parse Neo4j cypher-shell output into structured data."""
    records = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skip header line
    for line in lines[1:]:
        line = line.strip()
        if not line or line.startswith('(') or line.startswith('-'):
            continue

        # Parse CSV-like format with quoted fields
        parts = []
        current = []
        in_quotes = False

        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                parts.append(''.join(current).strip().strip('"'))
                current = []
            else:
                current.append(char)

        if current:
            parts.append(''.join(current).strip().strip('"'))

        if len(parts) >= 6:
            records.append({
                'capec_id': parts[0],
                'capec_name': parts[1],
                'capec_desc': parts[2],
                'attack_id': parts[3],
                'attack_name': parts[4],
                'attack_desc': parts[5] if len(parts) > 5 else ''
            })

    return records

def parse_owasp_output(filepath: str) -> Dict[str, str]:
    """Parse OWASP mappings into CAPEC→OWASP dict."""
    owasp_map = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines[1:]:
        line = line.strip()
        if not line or line.startswith('('):
            continue

        parts = [p.strip().strip('"') for p in line.split(',')]
        if len(parts) >= 3:
            capec_id = parts[0]
            owasp_cat = parts[2]
            owasp_map[capec_id] = owasp_cat

    return owasp_map

def create_ner_training_entry(record: Dict, owasp_map: Dict) -> Dict:
    """Create NER training entry from CAPEC-ATT&CK record."""
    capec_id = record['capec_id']
    capec_name = record['capec_name']
    capec_desc = record['capec_desc']
    attack_id = record['attack_id']
    attack_name = record['attack_name']
    attack_desc = record['attack_desc']

    # Build context text
    context_parts = [f"CAPEC-{capec_id}: {capec_name}"]

    if capec_desc:
        context_parts.append(capec_desc)

    if capec_id in owasp_map:
        context_parts.append(f"OWASP Category: {owasp_map[capec_id]}")

    context_parts.append(f"Implements ATT&CK Technique {attack_id}: {attack_name}")

    if attack_desc:
        context_parts.append(attack_desc)

    text = '. '.join(context_parts)

    # Create entity annotations
    entities = []

    # Find CAPEC pattern in text
    capec_match = re.search(rf'CAPEC-{re.escape(capec_id)}:\s*{re.escape(capec_name)}', text)
    if capec_match:
        entities.append({
            "start": capec_match.start(),
            "end": capec_match.end(),
            "label": "ATTACK_PATTERN",
            "text": capec_match.group()
        })

    # Find ATT&CK technique in text
    attack_match = re.search(rf'{re.escape(attack_id)}:\s*{re.escape(attack_name)}', text)
    if attack_match:
        entities.append({
            "start": attack_match.start(),
            "end": attack_match.end(),
            "label": "TECHNIQUE",
            "text": attack_match.group()
        })

    # Find OWASP category if present
    if capec_id in owasp_map:
        owasp_cat = owasp_map[capec_id]
        owasp_match = re.search(rf'OWASP Category:\s*{re.escape(owasp_cat)}', text)
        if owasp_match:
            entities.append({
                "start": owasp_match.start(),
                "end": owasp_match.end(),
                "label": "VULNERABILITY_CLASS",
                "text": owasp_match.group()
            })

    return {
        "text": text,
        "entities": entities,
        "metadata": {
            "source": "neo4j_capec_attack",
            "capec_id": capec_id,
            "attack_id": attack_id,
            "has_owasp": capec_id in owasp_map
        }
    }

def main():
    """Main processing function."""
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data" / "ner_training"

    # Read raw data
    print("Reading Neo4j extraction data...")
    capec_records = parse_neo4j_output(data_dir / "capec_attack_raw.txt")
    owasp_map = parse_owasp_output(data_dir / "capec_attack_owasp_raw.txt")

    print(f"Loaded {len(capec_records)} CAPEC-ATT&CK records")
    print(f"Loaded {len(owasp_map)} OWASP mappings")

    # Create training entries
    print("Creating NER training entries...")
    training_data = []
    seen_pairs: Set[tuple] = set()

    for record in capec_records:
        pair_key = (record['capec_id'], record['attack_id'])

        # Skip duplicates
        if pair_key in seen_pairs:
            continue

        seen_pairs.add(pair_key)
        entry = create_ner_training_entry(record, owasp_map)
        training_data.append(entry)

    print(f"Created {len(training_data)} unique training entries")

    # Save to JSON
    output_file = data_dir / "v7_capec_attack_owasp.json"
    print(f"Writing to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully created {output_file}")
    print(f"   Total entries: {len(training_data)}")
    print(f"   With OWASP context: {sum(1 for e in training_data if e['metadata']['has_owasp'])}")

    # Sample output
    print("\n📊 Sample entry:")
    if training_data:
        sample = training_data[0]
        print(f"Text: {sample['text'][:150]}...")
        print(f"Entities: {len(sample['entities'])}")
        for ent in sample['entities']:
            print(f"  - {ent['label']}: {ent['text']}")

if __name__ == "__main__":
    main()
