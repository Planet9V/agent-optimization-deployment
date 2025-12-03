#!/usr/bin/env python3
"""
Create v9 Comprehensive Training Dataset
Merges infrastructure (v5/v6) + cybersecurity (v7) + MITRE data
"""

import json
import re
from pathlib import Path
from collections import defaultdict
import hashlib

# Source paths
SECTOR_BASE = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion")
V7_CYBER_PATH = SECTOR_BASE / "data/ner_training/V7_NER_TRAINING_DATA_SPACY.json"
MITRE_PATH = Path("/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/data/ner_training/stratified_v7_mitre_training_data.json")
OUTPUT_PATH = Path("/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/data/ner_training/v9_comprehensive_training_data.json")

# All 16 infrastructure sectors
SECTORS = [
    "Chemical_Sector",
    "Commercial_Facilities_Sector",
    "Communications_Sector",
    "Critical_Manufacturing_Sector",
    "Dams_Sector",
    "Defense_Sector",
    "Emergency_Services_Sector",
    "Energy_Sector",
    "Financial_Sector",
    "Food_Agriculture_Sector",
    "Government_Sector",
    "Healthcare_Sector",
    "IT_Telecom_Sector",
    "Manufacturing_Sector",
    "Transportation_Sector",
    "Water_Sector"
]

# Entity types for infrastructure
INFRASTRUCTURE_ENTITIES = [
    "VENDOR", "EQUIPMENT", "PROTOCOL", "SECURITY",
    "HARDWARE_COMPONENT", "SOFTWARE_COMPONENT",
    "INDICATOR", "MITIGATION"
]


def hash_example(text):
    """Create hash to detect duplicates"""
    return hashlib.md5(text.lower().encode()).hexdigest()


def extract_entities_from_markdown(md_file):
    """Extract training examples from markdown files"""
    examples = []

    if not md_file.exists():
        return examples

    content = md_file.read_text(encoding='utf-8', errors='ignore')

    # Extract entity patterns from markdown
    # Look for bold text as potential entities
    bold_pattern = r'\*\*([^*]+)\*\*'

    # Split into sentences
    sentences = re.split(r'[.!?]\s+', content)

    for sentence in sentences:
        if len(sentence.strip()) < 20 or len(sentence) > 500:
            continue

        # Find all bold terms in this sentence
        entities = []
        for match in re.finditer(bold_pattern, sentence):
            entity_text = match.group(1).strip()
            if len(entity_text) < 3 or len(entity_text) > 100:
                continue

            # Determine entity type based on keywords
            entity_type = classify_entity_type(entity_text, sentence)
            if entity_type:
                start = match.start(1)
                end = match.end(1)
                entities.append((start, end, entity_type))

        if entities:
            # Clean sentence text
            clean_text = re.sub(r'\*\*', '', sentence).strip()
            # Adjust entity positions after removing markdown
            adjusted_entities = adjust_entity_positions(clean_text, entities, sentence)

            if adjusted_entities:
                examples.append((clean_text, {"entities": adjusted_entities}))

    return examples


def classify_entity_type(text, context):
    """Classify entity type based on text and context"""
    text_lower = text.lower()
    context_lower = context.lower()

    # Vendor patterns
    if any(vendor in text_lower for vendor in ['siemens', 'abb', 'schneider', 'honeywell', 'ge', 'cisco', 'rockwell', 'emerson', 'yokogawa']):
        return "VENDOR"

    # Protocol patterns
    if any(proto in text_lower for proto in ['modbus', 'dnp3', 'profinet', 'ethernet/ip', 'bacnet', 'mqtt', 'opc', 'iec', 'tcp/ip']):
        return "PROTOCOL"

    # Equipment patterns
    if any(equip in text_lower for equip in ['plc', 'rtu', 'hmi', 'scada', 'controller', 'sensor', 'actuator', 'valve', 'pump', 'turbine']):
        return "EQUIPMENT"

    # Security patterns
    if any(sec in text_lower for sec in ['firewall', 'encryption', 'authentication', 'authorization', 'vpn', 'ids', 'ips', 'security']):
        return "SECURITY"

    # Hardware component patterns
    if any(hw in text_lower for hw in ['cpu', 'memory', 'processor', 'module', 'card', 'interface', 'port']):
        return "HARDWARE_COMPONENT"

    # Software component patterns
    if any(sw in text_lower for sw in ['firmware', 'software', 'application', 'program', 'driver', 'operating system']):
        return "SOFTWARE_COMPONENT"

    # Mitigation patterns
    if any(mit in context_lower for mit in ['mitigation', 'remediation', 'patch', 'update', 'fix']):
        if any(action in text_lower for action in ['patch', 'update', 'configure', 'implement', 'disable', 'enable']):
            return "MITIGATION"

    return None


def adjust_entity_positions(clean_text, entities, original_text):
    """Adjust entity positions after markdown removal"""
    adjusted = []

    for start, end, entity_type in entities:
        # Extract entity text from original
        entity_text = original_text[start:end]
        # Find in clean text
        clean_start = clean_text.find(entity_text)
        if clean_start != -1:
            clean_end = clean_start + len(entity_text)
            adjusted.append((clean_start, clean_end, entity_type))

    return adjusted


def extract_from_sector(sector_name):
    """Extract training examples from a sector directory"""
    sector_path = SECTOR_BASE / sector_name
    examples = []

    if not sector_path.exists():
        print(f"Warning: Sector directory not found: {sector_path}")
        return examples

    # Find all markdown files
    md_files = list(sector_path.rglob("*.md"))
    print(f"Processing {len(md_files)} files from {sector_name}...")

    for md_file in md_files:
        file_examples = extract_entities_from_markdown(md_file)
        examples.extend(file_examples)

    print(f"  Extracted {len(examples)} examples from {sector_name}")
    return examples


def load_json_data(file_path):
    """Load training data from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle different JSON formats
        if isinstance(data, dict):
            # MITRE format with wrapper
            if "annotations" in data:
                examples = []
                for item in data["annotations"]:
                    text = item["text"]
                    entities = [(start, end, label) for start, end, label in item["entities"]]
                    examples.append((text, {"entities": entities}))
                print(f"Loaded {len(examples)} examples from {file_path.name} (MITRE format)")
                return examples
        elif isinstance(data, list):
            # v7 format - direct list
            examples = []
            for item in data:
                if isinstance(item, dict):
                    text = item.get("text", "")
                    entity_list = item.get("entities", [])
                    # Convert to tuple format
                    if entity_list and isinstance(entity_list[0], dict):
                        # Format: [{"start": 0, "end": 10, "label": "X"}]
                        entities = [(e["start"], e["end"], e["label"]) for e in entity_list]
                    else:
                        # Already in tuple format or empty
                        entities = entity_list
                    examples.append((text, {"entities": entities}))
                elif isinstance(item, (list, tuple)) and len(item) == 2:
                    # Already in (text, annotations) format
                    examples.append(item)
            print(f"Loaded {len(examples)} examples from {file_path.name}")
            return examples

        print(f"Loaded {len(data)} examples from {file_path.name}")
        return data
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []


def deduplicate_examples(examples):
    """Remove duplicate examples"""
    seen = set()
    unique = []

    for text, annotations in examples:
        text_hash = hash_example(text)
        if text_hash not in seen:
            seen.add(text_hash)
            unique.append((text, annotations))

    return unique


def main():
    print("=" * 80)
    print("CREATING v9 COMPREHENSIVE TRAINING DATASET")
    print("=" * 80)

    all_examples = []
    stats = defaultdict(int)

    # 1. Extract infrastructure data from all 16 sectors
    print("\n1. EXTRACTING INFRASTRUCTURE DATA (v5/v6)")
    print("-" * 80)
    for sector in SECTORS:
        sector_examples = extract_from_sector(sector)
        all_examples.extend(sector_examples)
        stats[f"infrastructure_{sector}"] = len(sector_examples)

    infrastructure_count = len(all_examples)
    print(f"\nTotal infrastructure examples: {infrastructure_count}")

    # 2. Load v7 cybersecurity data
    print("\n2. LOADING V7 CYBERSECURITY DATA")
    print("-" * 80)
    v7_cyber = load_json_data(V7_CYBER_PATH)
    all_examples.extend(v7_cyber)
    stats["v7_cybersecurity"] = len(v7_cyber)

    # 3. Load MITRE data
    print("\n3. LOADING MITRE DATA")
    print("-" * 80)
    mitre_data = load_json_data(MITRE_PATH)
    all_examples.extend(mitre_data)
    stats["mitre"] = len(mitre_data)

    # 4. Deduplicate
    print("\n4. DEDUPLICATING EXAMPLES")
    print("-" * 80)
    before_dedup = len(all_examples)
    all_examples = deduplicate_examples(all_examples)
    after_dedup = len(all_examples)
    duplicates_removed = before_dedup - after_dedup
    print(f"Before: {before_dedup} examples")
    print(f"After: {after_dedup} examples")
    print(f"Duplicates removed: {duplicates_removed}")

    # 5. Analyze entity types
    print("\n5. ENTITY TYPE ANALYSIS")
    print("-" * 80)
    entity_counts = defaultdict(int)
    for text, annotations in all_examples:
        for start, end, label in annotations.get("entities", []):
            entity_counts[label] += 1

    for entity_type in sorted(entity_counts.keys()):
        print(f"  {entity_type}: {entity_counts[entity_type]}")

    # 6. Save v9 dataset
    print("\n6. SAVING V9 COMPREHENSIVE DATASET")
    print("-" * 80)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_examples, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved {len(all_examples)} examples to:")
    print(f"  {OUTPUT_PATH}")

    # 7. Generate statistics report
    print("\n7. DATASET COMPOSITION")
    print("-" * 80)
    print(f"Infrastructure examples: {infrastructure_count}")
    print(f"Cybersecurity examples (v7): {stats['v7_cybersecurity']}")
    print(f"MITRE examples: {stats['mitre']}")
    print(f"Total (before dedup): {before_dedup}")
    print(f"Total (after dedup): {after_dedup}")
    print(f"Entity types: {len(entity_counts)}")

    # Save detailed stats
    stats_data = {
        "total_examples": after_dedup,
        "infrastructure_examples": infrastructure_count,
        "cybersecurity_examples": stats["v7_cybersecurity"],
        "mitre_examples": stats["mitre"],
        "duplicates_removed": duplicates_removed,
        "entity_types": dict(entity_counts),
        "sectors_processed": SECTORS
    }

    stats_path = OUTPUT_PATH.parent / "v9_dataset_stats.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats_data, f, indent=2)

    print(f"\n✓ Statistics saved to: {stats_path}")
    print("\n" + "=" * 80)
    print("V9 DATASET CREATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
