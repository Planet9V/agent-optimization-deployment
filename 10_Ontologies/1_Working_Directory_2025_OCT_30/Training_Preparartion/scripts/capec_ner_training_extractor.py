#!/usr/bin/env python3
"""
CAPEC v3.9 NER Training Data Extractor
Extracts entity-rich text from CAPEC attack patterns for NER model training
"""

import xml.etree.ElementTree as ET
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set
import re

# XML namespace
NS = {'capec': 'http://capec.mitre.org/capec-3'}

# CAPEC v3.9 XML file location
CAPEC_XML = "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/NVS Full CVE CAPEC CWE/capec_latest/capec_v3.9.xml"

class CAPECNERExtractor:
    """Extract NER training data from CAPEC v3.9 XML"""

    def __init__(self, xml_file: str):
        self.xml_file = xml_file
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        self.ner_training_data = []
        self.entity_statistics = {
            'capec_patterns': 0,
            'cwe_references': 0,
            'attack_techniques': 0,
            'text_blocks': 0,
            'total_entities': 0
        }

    def extract_text_with_entities(self, pattern: ET.Element) -> List[Dict]:
        """Extract text blocks with embedded entity references"""
        training_examples = []

        capec_id = pattern.get('ID')
        capec_name = pattern.get('Name')
        abstraction = pattern.get('Abstraction', 'Unknown')

        # Entity catalog for this pattern
        entities = {
            'CAPEC': [(capec_id, capec_name)],
            'CWE': [],
            'ATTACK_TECHNIQUE': [],
            'WASC': [],
            'OWASP': []
        }

        # Collect all entity references
        for weakness in pattern.findall('.//capec:Related_Weakness', NS):
            cwe_id = weakness.get('CWE_ID')
            if cwe_id:
                entities['CWE'].append(cwe_id)

        for taxonomy in pattern.findall('.//capec:Taxonomy_Mapping', NS):
            tax_name = taxonomy.get('Taxonomy_Name')
            entry_id_elem = taxonomy.find('capec:Entry_ID', NS)

            if tax_name == 'ATTACK' and entry_id_elem is not None:
                attack_id = entry_id_elem.text
                if attack_id:
                    entities['ATTACK_TECHNIQUE'].append(attack_id)
            elif tax_name == 'WASC' and entry_id_elem is not None:
                wasc_id = entry_id_elem.text
                if wasc_id:
                    entities['WASC'].append(wasc_id)
            elif tax_name == 'OWASP Attacks':
                # OWASP uses Entry_Name only, no Entry_ID
                entry_name_elem = taxonomy.find('capec:Entry_Name', NS)
                if entry_name_elem is not None:
                    owasp_name = entry_name_elem.text
                    if owasp_name:
                        entities['OWASP'].append(owasp_name)

        # Extract rich text descriptions
        description_elem = pattern.find('capec:Description', NS)
        if description_elem is not None and description_elem.text:
            training_examples.append({
                'text': description_elem.text.strip(),
                'context': 'description',
                'capec_id': capec_id,
                'capec_name': capec_name,
                'abstraction': abstraction,
                'entities': entities.copy(),
                'entity_count': sum(len(v) if isinstance(v, list) else 1 for v in entities.values())
            })

        # Extract extended description
        extended_desc = pattern.find('capec:Extended_Description', NS)
        if extended_desc is not None:
            for child in extended_desc:
                if child.text and len(child.text.strip()) > 50:
                    training_examples.append({
                        'text': child.text.strip(),
                        'context': 'extended_description',
                        'capec_id': capec_id,
                        'capec_name': capec_name,
                        'abstraction': abstraction,
                        'entities': entities.copy(),
                        'entity_count': sum(len(v) if isinstance(v, list) else 1 for v in entities.values())
                    })

        # Extract prerequisites
        prerequisites = pattern.find('capec:Prerequisites', NS)
        if prerequisites is not None:
            for prereq in prerequisites.findall('capec:Prerequisite', NS):
                if prereq.text and len(prereq.text.strip()) > 30:
                    training_examples.append({
                        'text': prereq.text.strip(),
                        'context': 'prerequisite',
                        'capec_id': capec_id,
                        'capec_name': capec_name,
                        'abstraction': abstraction,
                        'entities': entities.copy(),
                        'entity_count': sum(len(v) if isinstance(v, list) else 1 for v in entities.values())
                    })

        # Extract consequences
        consequences = pattern.find('capec:Consequences', NS)
        if consequences is not None:
            for consequence in consequences.findall('capec:Consequence', NS):
                for scope in consequence.findall('capec:Consequence_Scope', NS):
                    if scope.text:
                        # Find associated impact text
                        impact = consequence.find('capec:Consequence_Technical_Impact', NS)
                        if impact is not None and impact.text:
                            text = f"Scope: {scope.text.strip()}. Impact: {impact.text.strip()}"
                            training_examples.append({
                                'text': text,
                                'context': 'consequence',
                                'capec_id': capec_id,
                                'capec_name': capec_name,
                                'abstraction': abstraction,
                                'entities': entities.copy(),
                                'entity_count': sum(len(v) if isinstance(v, list) else 1 for v in entities.values())
                            })

        # Extract execution flow descriptions
        execution_flow = pattern.find('capec:Execution_Flow', NS)
        if execution_flow is not None:
            for attack_step in execution_flow.findall('.//capec:Attack_Step', NS):
                description = attack_step.find('capec:Step_Description', NS)
                if description is not None and description.text:
                    if len(description.text.strip()) > 30:
                        training_examples.append({
                            'text': description.text.strip(),
                            'context': 'execution_flow',
                            'capec_id': capec_id,
                            'capec_name': capec_name,
                            'abstraction': abstraction,
                            'entities': entities.copy(),
                            'entity_count': sum(len(v) if isinstance(v, list) else 1 for v in entities.values())
                        })

        # Extract example instances
        examples = pattern.find('capec:Example_Instances', NS)
        if examples is not None:
            for example in examples.findall('capec:Example', NS):
                if example.text and len(example.text.strip()) > 50:
                    training_examples.append({
                        'text': example.text.strip(),
                        'context': 'example_instance',
                        'capec_id': capec_id,
                        'capec_name': capec_name,
                        'abstraction': abstraction,
                        'entities': entities.copy(),
                        'entity_count': sum(len(v) if isinstance(v, list) else 1 for v in entities.values())
                    })

        # Update statistics
        self.entity_statistics['capec_patterns'] += 1
        self.entity_statistics['cwe_references'] += len(entities['CWE'])
        self.entity_statistics['attack_techniques'] += len(entities['ATTACK_TECHNIQUE'])
        self.entity_statistics['text_blocks'] += len(training_examples)
        self.entity_statistics['total_entities'] += sum(
            example['entity_count'] for example in training_examples
        )

        return training_examples

    def extract_all_patterns(self):
        """Extract NER training data from all attack patterns"""
        print("🔍 Extracting NER training data from CAPEC v3.9...")
        print(f"   Source: {self.xml_file}")

        patterns = self.root.findall('.//capec:Attack_Pattern', NS)
        print(f"   Found {len(patterns)} attack patterns\n")

        for idx, pattern in enumerate(patterns, 1):
            if idx % 100 == 0:
                print(f"   Progress: {idx}/{len(patterns)} patterns processed...")

            training_examples = self.extract_text_with_entities(pattern)
            self.ner_training_data.extend(training_examples)

        print(f"\n✅ Extraction complete!")

    def generate_statistics_report(self) -> Dict:
        """Generate comprehensive statistics report"""
        # Analyze entity distribution
        entity_type_distribution = {
            'with_cwe': 0,
            'with_attack': 0,
            'with_both': 0,
            'with_neither': 0
        }

        context_distribution = {}
        abstraction_distribution = {}

        for example in self.ner_training_data:
            has_cwe = len(example['entities']['CWE']) > 0
            has_attack = len(example['entities']['ATTACK_TECHNIQUE']) > 0

            if has_cwe and has_attack:
                entity_type_distribution['with_both'] += 1
            elif has_cwe:
                entity_type_distribution['with_cwe'] += 1
            elif has_attack:
                entity_type_distribution['with_attack'] += 1
            else:
                entity_type_distribution['with_neither'] += 1

            # Context distribution
            context = example['context']
            context_distribution[context] = context_distribution.get(context, 0) + 1

            # Abstraction level
            abstraction = example['abstraction']
            abstraction_distribution[abstraction] = abstraction_distribution.get(abstraction, 0) + 1

        return {
            'extraction_date': datetime.now().isoformat(),
            'source_file': self.xml_file,
            'total_training_examples': len(self.ner_training_data),
            'entity_statistics': self.entity_statistics,
            'entity_type_distribution': entity_type_distribution,
            'context_distribution': context_distribution,
            'abstraction_distribution': abstraction_distribution,
            'average_entities_per_example': (
                self.entity_statistics['total_entities'] / len(self.ner_training_data)
                if self.ner_training_data else 0
            )
        }

    def save_training_data(self):
        """Save NER training data to files"""
        output_dir = Path('data/ner_training')
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save full training data
        full_data_file = output_dir / 'CAPEC_NER_TRAINING_DATA.json'
        with open(full_data_file, 'w') as f:
            json.dump(self.ner_training_data, f, indent=2)

        print(f"💾 Training data saved: {full_data_file}")
        print(f"   Size: {full_data_file.stat().st_size / 1024:.1f} KB")
        print(f"   Examples: {len(self.ner_training_data)}")

        # Save statistics
        stats = self.generate_statistics_report()
        stats_file = output_dir / 'CAPEC_NER_STATISTICS.json'
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)

        print(f"📊 Statistics saved: {stats_file}")

        # Create entity-focused dataset (high entity count examples)
        high_entity_examples = [
            ex for ex in self.ner_training_data
            if ex['entity_count'] >= 2
        ]

        entity_rich_file = output_dir / 'CAPEC_NER_ENTITY_RICH.json'
        with open(entity_rich_file, 'w') as f:
            json.dump(high_entity_examples, f, indent=2)

        print(f"🎯 Entity-rich dataset: {entity_rich_file}")
        print(f"   Examples: {len(high_entity_examples)}")

        # Create abstraction-level specific datasets
        for abstraction in ['Meta', 'Standard', 'Detailed']:
            abstraction_examples = [
                ex for ex in self.ner_training_data
                if ex['abstraction'] == abstraction
            ]

            if abstraction_examples:
                abstraction_file = output_dir / f'CAPEC_NER_{abstraction.upper()}.json'
                with open(abstraction_file, 'w') as f:
                    json.dump(abstraction_examples, f, indent=2)

                print(f"📋 {abstraction} dataset: {abstraction_file}")
                print(f"   Examples: {len(abstraction_examples)}")

        # Create golden bridge dataset (patterns with both CWE and ATT&CK)
        golden_examples = [
            ex for ex in self.ner_training_data
            if len(ex['entities']['CWE']) > 0 and len(ex['entities']['ATTACK_TECHNIQUE']) > 0
        ]

        if golden_examples:
            golden_file = output_dir / 'CAPEC_NER_GOLDEN_BRIDGES.json'
            with open(golden_file, 'w') as f:
                json.dump(golden_examples, f, indent=2)

            print(f"🌟 Golden Bridge dataset: {golden_file}")
            print(f"   Examples: {len(golden_examples)}")

        return stats

    def generate_sample_annotations(self, num_samples: int = 10):
        """Generate sample annotated examples for manual review"""
        print(f"\n📝 Generating {num_samples} sample annotations...")

        output_dir = Path('data/ner_training')
        samples_file = output_dir / 'CAPEC_NER_SAMPLES.txt'

        with open(samples_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("CAPEC NER TRAINING DATA - SAMPLE ANNOTATIONS\n")
            f.write("=" * 80 + "\n\n")

            # Get diverse samples (different contexts and entity counts)
            samples = []

            # Get samples with different entity counts
            for entity_count in [0, 1, 2, 3, 5]:
                matching = [ex for ex in self.ner_training_data if ex['entity_count'] == entity_count]
                if matching:
                    samples.append(matching[0])

            # Fill remaining with random high-quality examples
            high_quality = [ex for ex in self.ner_training_data if ex['entity_count'] >= 2]
            samples.extend(high_quality[:num_samples - len(samples)])

            for idx, example in enumerate(samples[:num_samples], 1):
                f.write(f"SAMPLE {idx}\n")
                f.write("-" * 80 + "\n")
                f.write(f"CAPEC: {example['capec_id']} - {example['capec_name']}\n")
                f.write(f"Abstraction: {example['abstraction']}\n")
                f.write(f"Context: {example['context']}\n")
                f.write(f"Entity Count: {example['entity_count']}\n\n")

                f.write("TEXT:\n")
                f.write(example['text'][:500] + ("..." if len(example['text']) > 500 else "") + "\n\n")

                f.write("ENTITIES:\n")
                for entity_type, entity_list in example['entities'].items():
                    if entity_list:
                        if isinstance(entity_list, list):
                            if entity_type == 'CAPEC':
                                f.write(f"  {entity_type}: {entity_list[0][0]} ({entity_list[0][1]})\n")
                            else:
                                f.write(f"  {entity_type}: {', '.join(entity_list)}\n")

                f.write("\n" + "=" * 80 + "\n\n")

        print(f"✅ Sample annotations saved: {samples_file}")


def main():
    print("=" * 80)
    print("🚀 CAPEC V3.9 NER TRAINING DATA EXTRACTOR")
    print("=" * 80)
    print("Purpose: Extract entity-rich text for NER model training")
    print("Target: ~10,000-15,000 annotated training examples\n")

    # Initialize extractor
    extractor = CAPECNERExtractor(CAPEC_XML)

    # Extract training data
    extractor.extract_all_patterns()

    # Display statistics
    print("\n" + "=" * 80)
    print("📊 EXTRACTION STATISTICS")
    print("=" * 80)

    stats = extractor.generate_statistics_report()

    print(f"\nDataset Overview:")
    print(f"  • Total Training Examples: {stats['total_training_examples']:,}")
    print(f"  • CAPEC Patterns Processed: {stats['entity_statistics']['capec_patterns']}")
    print(f"  • CWE References: {stats['entity_statistics']['cwe_references']}")
    print(f"  • ATT&CK Techniques: {stats['entity_statistics']['attack_techniques']}")
    print(f"  • Text Blocks: {stats['entity_statistics']['text_blocks']}")
    print(f"  • Avg Entities/Example: {stats['average_entities_per_example']:.2f}")

    print(f"\nEntity Distribution:")
    print(f"  • With CWE only: {stats['entity_type_distribution']['with_cwe']}")
    print(f"  • With ATT&CK only: {stats['entity_type_distribution']['with_attack']}")
    print(f"  • With BOTH (Golden): {stats['entity_type_distribution']['with_both']}")
    print(f"  • With neither: {stats['entity_type_distribution']['with_neither']}")

    print(f"\nContext Distribution:")
    for context, count in sorted(stats['context_distribution'].items(), key=lambda x: x[1], reverse=True):
        print(f"  • {context}: {count}")

    print(f"\nAbstraction Levels:")
    for level, count in sorted(stats['abstraction_distribution'].items(), key=lambda x: x[1], reverse=True):
        print(f"  • {level}: {count}")

    # Save all data
    print("\n" + "=" * 80)
    print("💾 SAVING TRAINING DATASETS")
    print("=" * 80 + "\n")

    extractor.save_training_data()

    # Generate samples
    extractor.generate_sample_annotations(num_samples=20)

    print("\n" + "=" * 80)
    print("✅ NER TRAINING DATA EXTRACTION COMPLETE")
    print("=" * 80)
    print("\n💡 NEXT STEPS:")
    print("   1. Review sample annotations: data/ner_training/CAPEC_NER_SAMPLES.txt")
    print("   2. Train NER model with: data/ner_training/CAPEC_NER_TRAINING_DATA.json")
    print("   3. Use Golden Bridge dataset for high-quality training")
    print("   4. Validate model on entity-rich test set")

    print("\n📊 TRAINING DATA READY FOR:")
    print("   • SpaCy NER model training")
    print("   • Transformers (BERT, RoBERTa) fine-tuning")
    print("   • Conditional Random Fields (CRF) training")
    print("   • Custom entity recognition pipelines")


if __name__ == '__main__':
    main()
