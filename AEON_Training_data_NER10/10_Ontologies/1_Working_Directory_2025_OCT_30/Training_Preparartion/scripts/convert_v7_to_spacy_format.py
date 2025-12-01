#!/usr/bin/env python3
"""
Convert V7 NER dataset to spaCy format with character-level annotations.

The V7 dataset has entities grouped by type without character positions.
This script finds each entity in the text and adds start/end positions.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple

def find_entity_positions(text: str, entity_value: str, label: str) -> List[Tuple[int, int, str]]:
    """Find all occurrences of entity in text and return (start, end, label) tuples"""
    positions = []

    # Handle different entity formats
    if isinstance(entity_value, list):
        # CAPEC format: [id, name]
        search_terms = [entity_value[0], entity_value[1]] if len(entity_value) > 1 else [entity_value[0]]
    else:
        search_terms = [str(entity_value)]

    for term in search_terms:
        if not term:
            continue

        # Try exact match first
        pattern = re.escape(term)
        for match in re.finditer(pattern, text, re.IGNORECASE):
            positions.append((match.start(), match.end(), label))

        # For CWE, also try "CWE-XXX" format
        if label in ['CWE', 'WEAKNESS']:
            cwe_pattern = f"CWE-{term}"
            for match in re.finditer(re.escape(cwe_pattern), text, re.IGNORECASE):
                positions.append((match.start(), match.end(), label))

    return positions

def convert_example(example: Dict) -> Dict:
    """Convert a single example from V7 format to spaCy format"""
    text = example['text']
    entities_dict = example.get('entities', {})

    # Collect all entity positions
    all_entities = []

    for label, values in entities_dict.items():
        if not values:
            continue

        # Handle different value formats
        if isinstance(values, list):
            for value in values:
                positions = find_entity_positions(text, value, label)
                all_entities.extend(positions)

    # Remove duplicates and overlapping spans
    unique_entities = []
    seen_positions = set()

    for start, end, label in sorted(all_entities, key=lambda x: (x[0], -x[1])):
        # Check if this position overlaps with any existing entity
        overlaps = False
        for seen_start, seen_end in seen_positions:
            if (start < seen_end and end > seen_start):
                overlaps = True
                break

        if not overlaps:
            unique_entities.append({"start": start, "end": end, "label": label})
            seen_positions.add((start, end))

    return {
        "text": text,
        "entities": unique_entities
    }

def convert_dataset(input_path: str, output_path: str):
    """Convert entire V7 dataset to spaCy format"""
    print(f"\n📂 Loading V7 dataset from: {input_path}")

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✅ Loaded {len(data)} examples")
    print(f"\n🔄 Converting to spaCy format with character-level annotations...")

    converted_data = []
    skipped = 0

    for i, example in enumerate(data):
        if i % 500 == 0:
            print(f"  Processing: {i}/{len(data)}")

        try:
            converted = convert_example(example)
            if converted['entities']:  # Only include if we found entities
                converted_data.append(converted)
            else:
                skipped += 1
        except Exception as e:
            print(f"⚠️  Skipping example {i}: {str(e)[:100]}")
            skipped += 1

    print(f"\n✅ Converted {len(converted_data)} examples")
    print(f"⚠️  Skipped {skipped} examples (no entities found)")

    # Save converted data
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Saved spaCy-format dataset to: {output_path}")

    # Show statistics
    entity_counts = {}
    for example in converted_data:
        for entity in example['entities']:
            label = entity['label']
            entity_counts[label] = entity_counts.get(label, 0) + 1

    print(f"\n📊 Entity Distribution:")
    for label, count in sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"  {label}: {count}")

    # Show sample
    print(f"\n📋 Sample Converted Example:")
    if converted_data:
        sample = converted_data[0]
        print(f"Text: {sample['text'][:200]}...")
        print(f"Entities: {len(sample['entities'])}")
        for ent in sample['entities'][:5]:
            print(f"  {ent['label']}: '{sample['text'][ent['start']:ent['end']]}'")

if __name__ == "__main__":
    convert_dataset(
        input_path="data/ner_training/V7_NER_TRAINING_DATA.json",
        output_path="data/ner_training/V7_NER_TRAINING_DATA_SPACY.json"
    )

    print(f"\n✅ CONVERSION COMPLETE")
