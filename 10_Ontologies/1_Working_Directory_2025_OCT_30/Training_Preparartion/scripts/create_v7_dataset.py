#!/usr/bin/env python3
"""
V7 NER Training Dataset Creation
Merges all CAPEC, CVE-CWE, and ATTACK data into enhanced training dataset
"""

import json
import csv
import re
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Set, Tuple

class V7DatasetCreator:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.examples = []
        self.seen_texts = set()
        self.entity_stats = defaultdict(int)

        # Entity types to track
        self.entity_types = {
            'VULNERABILITY', 'WEAKNESS', 'ATTACK_PATTERN',
            'TECHNIQUE', 'CAPEC', 'CWE', 'CVE', 'ATTACK'
        }

    def load_existing_capec_data(self):
        """Load all existing CAPEC NER training files"""
        files = [
            'CAPEC_NER_TRAINING_DATA.json',
            'CAPEC_NER_ENTITY_RICH.json',
            'CAPEC_NER_DETAILED.json',
            'CAPEC_NER_GOLDEN_BRIDGES.json',
            'CAPEC_NER_META.json'
        ]

        print("Loading existing CAPEC data...")
        for filename in files:
            filepath = self.base_path / filename
            if filepath.exists():
                with open(filepath) as f:
                    data = json.load(f)
                    count = len(data)
                    print(f"  {filename}: {count} examples")

                    # Add examples with deduplication
                    for example in data:
                        text_key = example.get('text', '')[:100]
                        if text_key not in self.seen_texts:
                            self.seen_texts.add(text_key)
                            self.examples.append(example)

                            # Count entities
                            if 'entities' in example:
                                for entity_type, entities in example['entities'].items():
                                    if isinstance(entities, list):
                                        self.entity_stats[entity_type] += len(entities)

    def extract_cve_cwe_examples(self):
        """Extract NER training examples from CVE-CWE JSON data"""
        filepath = self.base_path / 'cve_cwe_data.json'
        if not filepath.exists():
            print("CVE-CWE data not found, skipping...")
            return

        print("\nExtracting CVE-CWE examples...")
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        count = 0
        for record in data:
            cve_id = record.get('cve_id', '').strip()
            cve_desc = record.get('cve_description', '').strip()
            cwe_id = record.get('cwe_id', '').strip()
            cwe_name = record.get('cwe_name', '').strip()
            cwe_desc = record.get('cwe_description', '').strip()

            # Skip invalid entries
            if not cve_desc or not cwe_desc:
                continue

            # Create example from CVE description with entity annotations
            if len(cve_desc) > 50:
                example = self._create_example(
                    text=cve_desc,
                    context='cve_description',
                    source_id=cve_id,
                    source_type='CVE',
                    entities={
                        'CVE': [[cve_id, cve_id]] if cve_id else [],
                        'CWE': [[cwe_id, cwe_name]] if cwe_id and cwe_name else [],
                        'VULNERABILITY': [[cve_id, 'vulnerability']]
                    }
                )

                if self._add_example(example):
                    count += 1

            # Create example from CWE description
            if len(cwe_desc) > 50:
                example = self._create_example(
                    text=cwe_desc,
                    context='cwe_description',
                    source_id=cwe_id,
                    source_type='CWE',
                    entities={
                        'CWE': [[cwe_id, cwe_name]] if cwe_id and cwe_name else [],
                        'WEAKNESS': [[cwe_id, 'weakness']]
                    }
                )

                if self._add_example(example):
                    count += 1

        print(f"  Added {count} CVE-CWE examples")

    def extract_capec_attack_examples(self):
        """Extract NER training examples from CAPEC-ATTACK JSON data"""
        filepath = self.base_path / 'capec_attack_data.json'
        if not filepath.exists():
            print("CAPEC-ATTACK data not found, skipping...")
            return

        print("\nExtracting CAPEC-ATTACK examples...")
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        count = 0
        for record in data:
            capec_id = record.get('capec_id', '').strip()
            capec_name = record.get('capec_name', '').strip()
            capec_desc = record.get('capec_description', '').strip()
            attack_id = record.get('attack_id', '').strip()
            attack_name = record.get('attack_name', '').strip()

            # Create example from CAPEC description with ATTACK mapping
            if capec_desc and len(capec_desc) > 50:
                entities = {
                    'CAPEC': [[capec_id, capec_name]] if capec_id and capec_name else [],
                    'ATTACK_PATTERN': [[capec_id, 'attack_pattern']]
                }

                # Add ATTACK technique if available
                if attack_id and attack_name:
                    entities['ATTACK'] = [[attack_id, attack_name]]
                    entities['TECHNIQUE'] = [[attack_id, attack_name]]

                example = self._create_example(
                    text=capec_desc,
                    context='capec_attack_mapping',
                    source_id=capec_id,
                    source_type='CAPEC',
                    entities=entities
                )

                if self._add_example(example):
                    count += 1

        print(f"  Added {count} CAPEC-ATTACK examples")

    def _create_example(self, text: str, context: str, source_id: str,
                       source_type: str, entities: Dict) -> Dict:
        """Create a standardized NER training example"""
        return {
            'text': text,
            'context': context,
            f'{source_type.lower()}_id': source_id,
            'entities': {k: v for k, v in entities.items() if v}
        }

    def _add_example(self, example: Dict) -> bool:
        """Add example if not duplicate"""
        text_key = example['text'][:100]
        if text_key not in self.seen_texts:
            self.seen_texts.add(text_key)
            self.examples.append(example)

            # Update stats
            for entity_type, entities in example.get('entities', {}).items():
                self.entity_stats[entity_type] += len(entities)

            return True
        return False

    def balance_entity_types(self):
        """Ensure good coverage of each entity type"""
        print("\nBalancing entity types...")
        print("Current distribution:")
        for entity_type in sorted(self.entity_stats.keys()):
            count = self.entity_stats[entity_type]
            print(f"  {entity_type}: {count}")

        # Check for underrepresented types
        min_count = 200
        underrepresented = {
            k: v for k, v in self.entity_stats.items()
            if v < min_count
        }

        if underrepresented:
            print(f"\nUnderrepresented types (< {min_count}):")
            for entity_type, count in underrepresented.items():
                print(f"  {entity_type}: {count} (need {min_count - count} more)")

    def validate_dataset(self) -> bool:
        """Validate JSON structure and entity spans"""
        print("\nValidating dataset...")
        errors = []

        for i, example in enumerate(self.examples):
            # Check required fields
            if 'text' not in example:
                errors.append(f"Example {i}: missing 'text' field")
                continue

            # Check entities structure
            if 'entities' in example:
                entities = example['entities']
                if not isinstance(entities, dict):
                    errors.append(f"Example {i}: entities must be dict")
                    continue

                # Check for overlapping entities
                all_spans = []
                for entity_type, entity_list in entities.items():
                    if not isinstance(entity_list, list):
                        errors.append(f"Example {i}: {entity_type} must be list")
                        continue

        if errors:
            print(f"Found {len(errors)} validation errors:")
            for error in errors[:10]:
                print(f"  {error}")
            return False

        print("  ✓ All examples valid")
        return True

    def generate_statistics(self) -> Dict:
        """Generate comprehensive statistics"""
        stats = {
            'total_examples': len(self.examples),
            'by_entity_type': dict(self.entity_stats),
            'by_context': defaultdict(int),
            'entity_coverage': {},
            'dataset_quality': {}
        }

        # Context distribution
        for example in self.examples:
            context = example.get('context', 'unknown')
            stats['by_context'][context] += 1

        # Entity coverage
        examples_with_entities = sum(
            1 for ex in self.examples
            if ex.get('entities') and any(ex['entities'].values())
        )
        stats['entity_coverage']['examples_with_entities'] = examples_with_entities
        stats['entity_coverage']['coverage_percentage'] = (
            examples_with_entities / len(self.examples) * 100
            if self.examples else 0
        )

        # Quality metrics
        avg_text_length = sum(len(ex['text']) for ex in self.examples) / len(self.examples)
        stats['dataset_quality']['avg_text_length'] = avg_text_length
        stats['dataset_quality']['min_entity_type_count'] = (
            min(self.entity_stats.values()) if self.entity_stats else 0
        )
        stats['dataset_quality']['max_entity_type_count'] = (
            max(self.entity_stats.values()) if self.entity_stats else 0
        )

        return stats

    def save_dataset(self, output_path: Path):
        """Save final V7 dataset"""
        print(f"\nSaving V7 dataset to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.examples, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Saved {len(self.examples)} examples")

    def save_statistics(self, output_path: Path):
        """Save statistics report"""
        stats = self.generate_statistics()

        print(f"\nSaving statistics to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        print("\n" + "="*60)
        print("V7 DATASET STATISTICS")
        print("="*60)
        print(f"Total examples: {stats['total_examples']}")
        print(f"\nBy Entity Type:")
        for entity_type in sorted(stats['by_entity_type'].keys()):
            count = stats['by_entity_type'][entity_type]
            print(f"  {entity_type}: {count}")

        print(f"\nEntity Coverage:")
        print(f"  Examples with entities: {stats['entity_coverage']['examples_with_entities']}")
        print(f"  Coverage: {stats['entity_coverage']['coverage_percentage']:.1f}%")

        print(f"\nDataset Quality:")
        print(f"  Avg text length: {stats['dataset_quality']['avg_text_length']:.0f} chars")
        print(f"  Min entity count: {stats['dataset_quality']['min_entity_type_count']}")
        print(f"  Max entity count: {stats['dataset_quality']['max_entity_type_count']}")
        print("="*60)

        return stats

def main():
    base_path = '/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/ner_training'

    creator = V7DatasetCreator(base_path)

    # Load all data sources
    creator.load_existing_capec_data()
    creator.extract_cve_cwe_examples()
    creator.extract_capec_attack_examples()

    # Balance and validate
    creator.balance_entity_types()
    if not creator.validate_dataset():
        print("Dataset validation failed!")
        return 1

    # Save final dataset
    output_path = Path(base_path) / 'V7_NER_TRAINING_DATA.json'
    stats_path = Path(base_path) / 'V7_STATISTICS.json'

    creator.save_dataset(output_path)
    stats = creator.save_statistics(stats_path)

    # Calculate improvement
    original_count = 1741
    improvement = stats['total_examples'] - original_count
    improvement_pct = (improvement / original_count) * 100

    print(f"\nImprovement over V6:")
    print(f"  +{improvement} examples (+{improvement_pct:.1f}%)")

    return 0

if __name__ == '__main__':
    exit(main())
