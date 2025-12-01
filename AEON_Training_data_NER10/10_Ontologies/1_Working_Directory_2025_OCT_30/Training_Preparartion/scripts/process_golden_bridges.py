#!/usr/bin/env python3
"""
Process Neo4j golden bridge query results into NER training format.
Extracts CAPEC-CWE-ATT&CK triples and creates spaCy training examples.
"""

import json
import re
from typing import List, Dict, Any

def parse_cypher_output(file_path: str) -> List[Dict[str, str]]:
    """Parse Neo4j cypher-shell output into structured records."""
    records = []

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skip header line
    for line in lines[1:]:
        if not line.strip():
            continue

        # Parse the comma-separated CSV-like values with quoted strings
        # Format: "CAPEC-1", "Name", "Desc", "123", "CWE Name", "T1234", "ATT&CK Name"
        parts = []
        current = ""
        in_quotes = False

        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                parts.append(current.strip().strip('"'))
                current = ""
                continue
            else:
                current += char

        # Add last part
        if current:
            parts.append(current.strip().strip('"'))

        if len(parts) >= 7:
            record = {
                'capec_id': parts[0],
                'capec_name': parts[1],
                'capec_desc': parts[2][:500] if len(parts[2]) > 500 else parts[2],  # Truncate long descriptions
                'cwe_id': parts[3],
                'cwe_name': parts[4],
                'attack_id': parts[5],
                'attack_name': parts[6]
            }
            records.append(record)

    return records

def create_ner_example(capec_id: str, capec_name: str, cwe_id: str, cwe_name: str,
                       attack_id: str, attack_name: str) -> Dict[str, Any]:
    """Create a single NER training example from golden bridge data."""

    # Template 1: Full context sentence
    text = f"{capec_id} {capec_name} exploits {cwe_id} {cwe_name} leading to {attack_id} {attack_name}"

    entities = []
    pos = 0

    # Find CAPEC pattern
    capec_match = text.find(capec_id)
    if capec_match != -1:
        capec_end = text.find(' exploits', capec_match)
        entities.append({
            "start": capec_match,
            "end": capec_end,
            "label": "ATTACK_PATTERN"
        })
        pos = capec_end

    # Find CWE pattern
    cwe_match = text.find(cwe_id, pos)
    if cwe_match != -1:
        cwe_end = text.find(' leading to', cwe_match)
        entities.append({
            "start": cwe_match,
            "end": cwe_end,
            "label": "WEAKNESS"
        })
        pos = cwe_end

    # Find ATT&CK pattern
    attack_match = text.find(attack_id, pos)
    if attack_match != -1:
        entities.append({
            "start": attack_match,
            "end": len(text),
            "label": "TECHNIQUE"
        })

    return {
        "text": text,
        "entities": entities
    }

def create_ner_variations(record: Dict[str, str]) -> List[Dict[str, Any]]:
    """Create multiple NER training variations from a single golden bridge record."""
    examples = []

    # Variation 1: Full context
    ex1 = create_ner_example(
        record['capec_id'], record['capec_name'],
        record['cwe_id'], record['cwe_name'],
        record['attack_id'], record['attack_name']
    )
    examples.append(ex1)

    # Variation 2: ID-only format
    text2 = f"{record['capec_id']} exploits {record['cwe_id']} enabling {record['attack_id']}"
    entities2 = [
        {"start": 0, "end": len(record['capec_id']), "label": "ATTACK_PATTERN"},
        {"start": text2.find(record['cwe_id']), "end": text2.find(record['cwe_id']) + len(record['cwe_id']), "label": "WEAKNESS"},
        {"start": text2.find(record['attack_id']), "end": len(text2), "label": "TECHNIQUE"}
    ]
    examples.append({"text": text2, "entities": entities2})

    # Variation 3: Name-only format
    text3 = f"The attack pattern {record['capec_name']} leverages weakness {record['cwe_name']} to perform {record['attack_name']}"
    entities3 = []

    start = text3.find(record['capec_name'])
    entities3.append({"start": start, "end": start + len(record['capec_name']), "label": "ATTACK_PATTERN"})

    start = text3.find(record['cwe_name'])
    entities3.append({"start": start, "end": start + len(record['cwe_name']), "label": "WEAKNESS"})

    start = text3.find(record['attack_name'])
    entities3.append({"start": start, "end": start + len(record['attack_name']), "label": "TECHNIQUE"})

    examples.append({"text": text3, "entities": entities3})

    return examples

def main():
    """Main processing function."""
    input_file = "/tmp/golden_bridges_raw.txt"
    output_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/ner_training/v7_golden_bridges.json"

    print("Parsing Neo4j output...")
    records = parse_cypher_output(input_file)
    print(f"Found {len(records)} golden bridge records")

    print("Creating NER training examples...")
    all_examples = []

    # Track unique combinations to avoid duplicates
    seen = set()

    for record in records:
        # Create unique key for deduplication
        key = f"{record['capec_id']}|{record['cwe_id']}|{record['attack_id']}"

        if key not in seen:
            seen.add(key)
            variations = create_ner_variations(record)
            all_examples.extend(variations)

    print(f"Created {len(all_examples)} NER training examples")

    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_examples, f, indent=2, ensure_ascii=False)

    print(f"Saved training data to {output_file}")

    # Print sample
    print("\nSample examples:")
    for i, ex in enumerate(all_examples[:3]):
        print(f"\nExample {i+1}:")
        print(f"Text: {ex['text']}")
        print(f"Entities: {ex['entities']}")

if __name__ == "__main__":
    main()
