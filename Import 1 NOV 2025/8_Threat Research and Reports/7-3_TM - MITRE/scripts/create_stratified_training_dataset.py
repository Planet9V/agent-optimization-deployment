#!/usr/bin/env python3
"""
Stratified Training Dataset Creator
Merges V7 baseline training data with MITRE Phase 2 data using 30%/70% stratified sampling.

Strategy:
- 30% from V7 baseline (maintain existing model performance)
- 70% from MITRE Phase 2 (expand coverage and improve F1)
- Ensures entity distribution balance across both sources
- Prevents catastrophic forgetting of V7 capabilities
"""

import json
import random
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

class StratifiedDatasetCreator:
    """Create stratified training dataset from multiple sources"""

    def __init__(self):
        self.entity_counts = defaultdict(int)
        self.source_counts = defaultdict(int)

    def load_training_data(self, file_path: str) -> List[dict]:
        """Load training data from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle both formats: with/without annotations wrapper
        if 'annotations' in data:
            return data['annotations']
        elif isinstance(data, list):
            return data
        else:
            raise ValueError(f"Unexpected data format in {file_path}")

    def analyze_entity_distribution(self, dataset: List[dict], label: str):
        """Analyze and print entity distribution"""
        entity_dist = defaultdict(int)
        total_entities = 0

        for example in dataset:
            for entity in example.get('entities', []):
                # Handle both tuple and list formats
                if isinstance(entity, (list, tuple)) and len(entity) >= 3:
                    entity_label = entity[2]
                    entity_dist[entity_label] += 1
                    total_entities += 1

        print(f"\n{label} Dataset:")
        print(f"  Examples: {len(dataset)}")
        print(f"  Total entities: {total_entities}")
        print(f"  Entity distribution:")
        for entity_type, count in sorted(entity_dist.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_entities * 100) if total_entities > 0 else 0
            print(f"    {entity_type}: {count} ({percentage:.1f}%)")

    def create_stratified_sample(self, v7_data: List[dict],
                                  mitre_data: List[dict],
                                  v7_ratio: float = 0.30) -> List[dict]:
        """Create stratified sample with specified ratio"""

        v7_sample_size = int(len(mitre_data) * v7_ratio / (1 - v7_ratio))

        print(f"\nStratified Sampling Strategy:")
        print(f"  V7 baseline: {v7_ratio * 100:.0f}% = {v7_sample_size} examples")
        print(f"  MITRE Phase 2: {(1 - v7_ratio) * 100:.0f}% = {len(mitre_data)} examples")
        print(f"  Total combined: {v7_sample_size + len(mitre_data)} examples")

        # Sample V7 data (with replacement if necessary)
        if len(v7_data) >= v7_sample_size:
            v7_sample = random.sample(v7_data, v7_sample_size)
        else:
            # Not enough V7 data, use all and oversample
            print(f"  Warning: V7 dataset ({len(v7_data)}) smaller than target ({v7_sample_size})")
            print(f"  Using all V7 data and oversampling...")
            v7_sample = v7_data.copy()
            while len(v7_sample) < v7_sample_size:
                v7_sample.extend(random.sample(v7_data, min(len(v7_data), v7_sample_size - len(v7_sample))))

        # Use all MITRE data
        combined = v7_sample + mitre_data

        # Shuffle for training
        random.shuffle(combined)

        return combined

    def normalize_entity_format(self, examples: List[dict]) -> List[dict]:
        """Normalize entity format to (start, end, label) tuples"""
        normalized = []

        for example in examples:
            normalized_example = {
                "text": example["text"],
                "entities": []
            }

            for entity in example.get("entities", []):
                if isinstance(entity, dict):
                    # Dict format: {"start": X, "end": Y, "label": Z}
                    normalized_example["entities"].append((
                        entity["start"],
                        entity["end"],
                        entity["label"]
                    ))
                elif isinstance(entity, (list, tuple)) and len(entity) >= 3:
                    # Already in tuple/list format
                    normalized_example["entities"].append((
                        entity[0],
                        entity[1],
                        entity[2]
                    ))

            normalized.append(normalized_example)

        return normalized

    def save_combined_dataset(self, dataset: List[dict], output_file: str,
                               v7_count: int, mitre_count: int):
        """Save combined dataset with metadata"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Calculate entity distribution
        entity_dist = defaultdict(int)
        for example in dataset:
            for entity in example.get('entities', []):
                if isinstance(entity, (list, tuple)) and len(entity) >= 3:
                    entity_dist[entity[2]] += 1

        spacy_format = {
            "version": "2.0",
            "source": "Stratified V7 + MITRE Phase 2",
            "annotations": dataset,
            "metadata": {
                "total_examples": len(dataset),
                "v7_examples": v7_count,
                "mitre_examples": mitre_count,
                "v7_ratio": f"{(v7_count / len(dataset) * 100):.1f}%",
                "mitre_ratio": f"{(mitre_count / len(dataset) * 100):.1f}%",
                "entity_distribution": dict(entity_dist),
                "stratified_sampling": "30% V7 + 70% MITRE",
                "purpose": "Balanced training to maintain V7 performance while adding MITRE coverage"
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(spacy_format, f, indent=2, ensure_ascii=False)

        print(f"\nCombined dataset saved to: {output_path}")
        print(f"File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")


def main():
    """Main execution"""

    # Paths
    v7_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/ner_training/V7_NER_TRAINING_DATA_SPACY.json"
    mitre_phase2_file = "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/data/ner_training/mitre_phase2_training_data.json"
    output_file = "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/data/ner_training/stratified_v7_mitre_training_data.json"

    print("=" * 80)
    print("Stratified Training Dataset Creator")
    print("=" * 80)
    print(f"\nV7 Baseline: {v7_file}")
    print(f"MITRE Phase 2: {mitre_phase2_file}")
    print(f"Output: {output_file}")
    print(f"\nStrategy: 30% V7 + 70% MITRE for balanced training")

    # Initialize creator
    creator = StratifiedDatasetCreator()

    # Load datasets
    print("\n" + "=" * 80)
    print("Loading datasets...")
    print("=" * 80)

    v7_data = creator.load_training_data(v7_file)
    mitre_data = creator.load_training_data(mitre_phase2_file)

    print(f"\nLoaded:")
    print(f"  V7 baseline: {len(v7_data)} examples")
    print(f"  MITRE Phase 2: {len(mitre_data)} examples")

    # Analyze distributions
    print("\n" + "=" * 80)
    print("Analyzing entity distributions...")
    print("=" * 80)

    creator.analyze_entity_distribution(v7_data, "V7 Baseline")
    creator.analyze_entity_distribution(mitre_data, "MITRE Phase 2")

    # Normalize formats
    print("\n" + "=" * 80)
    print("Normalizing entity formats...")
    print("=" * 80)

    v7_normalized = creator.normalize_entity_format(v7_data)
    mitre_normalized = creator.normalize_entity_format(mitre_data)

    print(f"  V7 normalized: {len(v7_normalized)} examples")
    print(f"  MITRE normalized: {len(mitre_normalized)} examples")

    # Create stratified sample
    print("\n" + "=" * 80)
    print("Creating stratified sample...")
    print("=" * 80)

    combined_dataset = creator.create_stratified_sample(
        v7_normalized,
        mitre_normalized,
        v7_ratio=0.30
    )

    v7_count = int(len(combined_dataset) * 0.30)
    mitre_count = len(combined_dataset) - v7_count

    # Analyze combined distribution
    print("\n" + "=" * 80)
    print("Combined Dataset Analysis")
    print("=" * 80)

    creator.analyze_entity_distribution(combined_dataset, "Combined Stratified")

    # Save combined dataset
    print("\n" + "=" * 80)
    print("Saving combined dataset...")
    print("=" * 80)

    creator.save_combined_dataset(
        combined_dataset,
        output_file,
        v7_count,
        mitre_count
    )

    print("\n" + "=" * 80)
    print("Stratified Dataset Creation Complete")
    print("=" * 80)
    print("\nNext Steps:")
    print("1. Validate combined dataset format")
    print("2. Retrain NER model with stratified dataset")
    print("3. Evaluate F1 score improvement (target: >95.5%)")
    print("4. Compare with V7 baseline (95.05%)")
    print("\n")


if __name__ == "__main__":
    main()
