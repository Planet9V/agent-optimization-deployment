#!/usr/bin/env python3
"""
NER Training Pipeline
Trains spaCy NER model on critical infrastructure sector documentation.
Uses EntityRuler for pattern-based entity extraction with 7 entity types.
"""

import spacy
from spacy.tokens import DocBin, Doc
from spacy.training import Example
import json
import random
from pathlib import Path
from typing import List, Dict, Tuple
import re

class NERTrainingPipeline:
    """Pipeline for training spaCy NER model on ICS/OT entities"""

    def __init__(self, validation_results_path: str):
        """Initialize with validation results JSON"""
        self.validation_results_path = Path(validation_results_path)
        self.base_path = self.validation_results_path.parent.parent  # Already at Training_Preparartion level

        # Load validation results
        with open(self.validation_results_path, 'r') as f:
            self.validation_data = json.load(f)

        # Entity types - 24 total (7 baseline + 17 cybersecurity)
        self.entity_types = [
            # Baseline types (7)
            'VENDOR', 'EQUIPMENT', 'PROTOCOL', 'OPERATION',
            'ARCHITECTURE', 'SECURITY', 'SUPPLIER',
            # Cybersecurity types (17)
            'THREAT_MODEL', 'TACTIC', 'TECHNIQUE', 'ATTACK_PATTERN',
            'VULNERABILITY', 'WEAKNESS', 'INDICATOR', 'THREAT_ACTOR',
            'CAMPAIGN', 'SOFTWARE_COMPONENT', 'HARDWARE_COMPONENT',
            'PERSONALITY_TRAIT', 'COGNITIVE_BIAS', 'INSIDER_INDICATOR',
            'SOCIAL_ENGINEERING', 'ATTACK_VECTOR', 'MITIGATION'
        ]

        # Initialize spaCy
        self.nlp = spacy.blank("en")

        # Training data storage
        self.training_examples = []
        self.annotation_stats = {entity_type: 0 for entity_type in self.entity_types}

    def load_sector_files(self, sector_name: str) -> List[Tuple[str, str]]:
        """Load all markdown files from a sector directory"""
        sector_path = self.base_path / sector_name
        files_content = []

        if not sector_path.exists():
            print(f"⚠️  Sector path not found: {sector_path}")
            return files_content

        for md_file in sector_path.rglob('*.md'):
            # Skip metadata files
            if md_file.name in ['COMPLETION_REPORT.md', 'VALIDATION_SUMMARY.md', 'README.md']:
                continue

            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    files_content.append((md_file.name, content))
            except Exception as e:
                print(f"⚠️  Error reading {md_file}: {e}")

        return files_content

    def create_entity_patterns(self) -> List[Dict]:
        """Create pattern-based entity extraction rules for EntityRuler"""
        patterns = []

        # VENDOR patterns
        vendor_patterns = [
            "Siemens Energy Automation", "Siemens AG", "Siemens Power Automation",
            "ABB Power Grids", "ABB Automation", "Schneider Electric",
            "Honeywell Process Solutions", "Honeywell", "Rockwell Automation",
            "Allen-Bradley", "GE Grid Solutions", "GE Digital Energy",
            "Emerson Process Management", "Emerson", "Yokogawa",
            "SEL Schweitzer Engineering", "Schweitzer Engineering Laboratories",
            "Mitsubishi Electric", "Omron", "Cisco Industrial", "Cisco",
            "Palo Alto Networks", "Fortinet", "Thales", "Alstom",
            "Motorola Solutions", "Harris Corporation", "Ericsson", "Nokia"
        ]
        patterns.extend([{"label": "VENDOR", "pattern": v} for v in vendor_patterns])

        # PROTOCOL patterns
        protocol_patterns = [
            "DNP3", "DNP3 Secure Authentication", "IEC 61850", "IEC 62443",
            "Modbus TCP", "Modbus RTU", "Modbus Plus", "NERC CIP",
            "IEEE 1815", "IEEE 1474", "NIST SP 800-82", "OPC UA", "OPC DA",
            "PROFINET IO", "PROFINET RT", "EtherNet/IP", "GOOSE", "MMS",
            "ETCS", "CBTC", "PTC", "AES-256", "AES-128"
        ]
        patterns.extend([{"label": "PROTOCOL", "pattern": p} for p in protocol_patterns])

        # SECURITY patterns
        security_keywords = [
            "NGFW", "Firewall", "IDS", "IPS", "Intrusion Detection",
            "Intrusion Prevention", "Deep Packet Inspection", "DMZ",
            "Electronic Security Perimeter", "Access Control",
            "Network Segmentation", "Encryption", "Authentication",
            "Authorization", "SIEM", "Zero Trust", "Vulnerability Assessment",
            "Penetration Testing", "Security Audit"
        ]
        patterns.extend([{"label": "SECURITY", "pattern": s} for s in security_keywords])

        # ARCHITECTURE patterns
        architecture_keywords = [
            "Network Architecture", "System Architecture", "Security Architecture",
            "Purdue Model", "DMZ", "VLAN", "VPN", "ESP",
            "Hierarchical Architecture", "Redundant Architecture",
            "Distributed Architecture", "Ring Topology", "Star Topology",
            "Mesh Network", "N+1 Redundancy", "Hot Standby", "Cold Standby"
        ]
        patterns.extend([{"label": "ARCHITECTURE", "pattern": a} for a in architecture_keywords])

        return patterns

    def convert_to_spacy_format(self, text: str, entities_dict: Dict[str, List[str]]) -> Tuple[str, Dict]:
        """Convert extracted entities to spaCy annotation format with intelligent deduplication"""
        entities = []

        for entity_type, entity_list in entities_dict.items():
            for entity_text in entity_list:
                # Find all occurrences of this entity in the text
                # Use word boundaries to prevent substring matches (e.g., "ge " matching in "manage")
                pattern = r'\b' + re.escape(entity_text) + r'\b'
                for match in re.finditer(pattern, text):
                    start, end = match.span()
                    entities.append((start, end, entity_type))

        # Resolve overlaps using priority hierarchy (includes deduplication)
        resolved = self._resolve_overlapping_entities(entities)

        # Update statistics
        for start, end, label in resolved:
            self.annotation_stats[label] += 1

        return (text, {"entities": resolved})

    def _resolve_overlapping_entities(self, entities):
        """
        Resolve overlapping entities using priority hierarchy and length rules.

        Rules:
        1. Longer span wins (more specific)
        2. Higher priority type wins if same length
        3. Keep non-overlapping entities
        """
        if not entities:
            return []

        # Remove exact duplicates first (CRITICAL: prevents E103 errors)
        # Use ordered deduplication to preserve original order
        seen = set()
        unique_entities = []
        for entity in entities:
            if entity not in seen:
                seen.add(entity)
                unique_entities.append(entity)
        entities = unique_entities

        # Entity priority hierarchy (lower number = higher priority)
        PRIORITY = {
            'EQUIPMENT': 1, 'HARDWARE_COMPONENT': 2, 'SOFTWARE_COMPONENT': 3,
            'PROTOCOL': 4, 'VULNERABILITY': 5, 'WEAKNESS': 6,
            'VENDOR': 7, 'SUPPLIER': 8, 'THREAT_ACTOR': 9, 'CAMPAIGN': 10,
            'TECHNIQUE': 11, 'TACTIC': 12,
            'ARCHITECTURE': 13, 'OPERATION': 14, 'ATTACK_PATTERN': 15,
            'ATTACK_VECTOR': 16, 'THREAT_MODEL': 17,
            'INDICATOR': 18, 'PERSONALITY_TRAIT': 19, 'COGNITIVE_BIAS': 20,
            'INSIDER_INDICATOR': 21, 'SOCIAL_ENGINEERING': 22,
            'SECURITY': 23, 'MITIGATION': 24
        }

        # Sort by start position
        sorted_entities = sorted(entities, key=lambda x: (x[0], -(x[1] - x[0])))

        resolved = []
        skip_indices = set()

        for i, (start1, end1, label1) in enumerate(sorted_entities):
            if i in skip_indices:
                continue

            # Find overlapping entities
            conflicts = []
            for j in range(i + 1, len(sorted_entities)):
                if j in skip_indices:
                    continue

                start2, end2, label2 = sorted_entities[j]

                # Check for overlap
                if start2 < end1:
                    conflicts.append((j, start2, end2, label2))
                else:
                    break

            if not conflicts:
                resolved.append((start1, end1, label1))
                continue

            # Resolve conflicts
            current_winner = (i, start1, end1, label1)

            for j, start2, end2, label2 in conflicts:
                len1 = current_winner[2] - current_winner[1]
                len2 = end2 - start2

                # Rule 1: Longer span wins
                if len2 > len1:
                    skip_indices.add(current_winner[0])
                    current_winner = (j, start2, end2, label2)
                elif len2 == len1:
                    # Rule 2: Higher priority wins
                    priority1 = PRIORITY.get(current_winner[3], 999)
                    priority2 = PRIORITY.get(label2, 999)

                    if priority2 < priority1:
                        skip_indices.add(current_winner[0])
                        current_winner = (j, start2, end2, label2)
                    else:
                        skip_indices.add(j)
                else:
                    skip_indices.add(j)

            resolved.append((current_winner[1], current_winner[2], current_winner[3]))

        return resolved

    def process_sector_for_training(self, sector_name: str) -> int:
        """Process a sector and create training examples"""
        print(f"\n📁 Processing {sector_name}...")

        # Get sector data from validation results
        sector_data = self.validation_data['sectors'].get(sector_name)
        if not sector_data:
            print(f"⚠️  No validation data for {sector_name}")
            return 0

        # Load sector files
        files = self.load_sector_files(sector_name)
        if not files:
            print(f"⚠️  No files found for {sector_name}")
            return 0

        examples_created = 0

        # Process each file
        for file_name, content in files:
            # Find matching file in validation results
            file_data = next((f for f in sector_data['files'] if f['file'] == file_name), None)

            if not file_data or 'patterns' not in file_data:
                continue

            # Convert to spaCy format
            spacy_annotation = self.convert_to_spacy_format(content, file_data['patterns'])

            if spacy_annotation[1]['entities']:
                self.training_examples.append(spacy_annotation)
                examples_created += 1

        print(f"  ✅ Created {examples_created} training examples")
        return examples_created

    def create_dataset_splits(self) -> Tuple[List, List, List]:
        """Split training data into train/validation/test sets (70/15/15)"""
        # Shuffle examples
        random.shuffle(self.training_examples)

        total = len(self.training_examples)
        train_size = int(total * 0.70)
        val_size = int(total * 0.15)

        train_data = self.training_examples[:train_size]
        val_data = self.training_examples[train_size:train_size + val_size]
        test_data = self.training_examples[train_size + val_size:]

        print(f"\n📊 Dataset Split:")
        print(f"  Train: {len(train_data)} examples (70%)")
        print(f"  Validation: {len(val_data)} examples (15%)")
        print(f"  Test: {len(test_data)} examples (15%)")

        return train_data, val_data, test_data

    def save_spacy_docbin(self, examples: List[Tuple], output_path: Path):
        """Save training examples to spaCy DocBin format"""
        db = DocBin()

        for text, annotations in examples:
            doc = self.nlp.make_doc(text)
            ents = []

            for start, end, label in annotations['entities']:
                span = doc.char_span(start, end, label=label, alignment_mode="expand")
                if span:
                    ents.append(span)

            # Filter out overlapping spans - keep only non-overlapping entities
            filtered_ents = self._filter_overlaps(ents)
            try:
                doc.ents = filtered_ents
                db.add(doc)
            except ValueError as e:
                # Skip documents with unresolvable entity conflicts
                print(f"  ⚠️  Skipping document due to entity overlap: {e}")
                continue

        db.to_disk(output_path)
        print(f"  💾 Saved to {output_path}")

    def _filter_overlaps(self, spans):
        """
        Filter overlapping spans using same resolution logic as _resolve_overlapping_entities.

        Uses priority hierarchy and length rules to resolve conflicts.
        """
        if not spans:
            return []

        # Convert spans to tuples for resolution
        span_tuples = [(s.start_char, s.end_char, s.label_) for s in spans]

        # Use same resolution logic as convert_to_spacy_format
        resolved_tuples = self._resolve_overlapping_entities(span_tuples)

        # Create a mapping from tuple back to original span
        span_map = {(s.start_char, s.end_char, s.label_): s for s in spans}

        # Return spans in order, using original span objects where possible
        result = []
        for start, end, label in resolved_tuples:
            if (start, end, label) in span_map:
                result.append(span_map[(start, end, label)])
            else:
                # Find first matching span
                matching = [s for s in spans if s.start_char == start and s.end_char == end and s.label_ == label]
                if matching:
                    result.append(matching[0])

        return result

    def train_ner_model(self, train_data: List, val_data: List, n_iter: int = 50):
        """Train spaCy NER model"""
        print(f"\n🚀 Training NER Model ({n_iter} iterations)...")

        # Add NER component if not present
        if "ner" not in self.nlp.pipe_names:
            ner = self.nlp.add_pipe("ner", last=True)
        else:
            ner = self.nlp.get_pipe("ner")

        # Add entity labels
        for entity_type in self.entity_types:
            ner.add_label(entity_type)

        # Disable other pipeline components during training
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != "ner"]

        # Training loop
        with self.nlp.disable_pipes(*other_pipes):
            optimizer = self.nlp.begin_training()

            for iteration in range(n_iter):
                random.shuffle(train_data)
                losses = {}

                # Batch training examples
                for text, annotations in train_data:
                    doc = self.nlp.make_doc(text)

                    # CRITICAL: Deduplicate entities to prevent E103 errors
                    # Remove exact duplicates (same position, same type)
                    entities = annotations.get('entities', [])
                    unique_entities = list(set(entities))
                    annotations['entities'] = unique_entities

                    example = Example.from_dict(doc, annotations)
                    self.nlp.update([example], drop=0.5, losses=losses, sgd=optimizer)

                if (iteration + 1) % 5 == 0:
                    print(f"  Iteration {iteration + 1}/{n_iter} - Loss: {losses.get('ner', 0):.4f}")

        print("  ✅ Training complete")

    def evaluate_model(self, test_data: List) -> Dict[str, float]:
        """Evaluate trained NER model on test set"""
        print("\n📊 Evaluating Model...")

        tp = {entity: 0 for entity in self.entity_types}
        fp = {entity: 0 for entity in self.entity_types}
        fn = {entity: 0 for entity in self.entity_types}

        for text, annotations in test_data:
            doc = self.nlp(text)

            # Predicted entities
            pred_entities = set((ent.start_char, ent.end_char, ent.label_) for ent in doc.ents)

            # True entities
            true_entities = set()
            for start, end, label in annotations['entities']:
                true_entities.add((start, end, label))

            # Calculate metrics
            for entity in pred_entities:
                if entity in true_entities:
                    tp[entity[2]] += 1
                else:
                    fp[entity[2]] += 1

            for entity in true_entities:
                if entity not in pred_entities:
                    fn[entity[2]] += 1

        # Calculate precision, recall, F1
        results = {}

        for entity in self.entity_types:
            precision = tp[entity] / (tp[entity] + fp[entity]) if (tp[entity] + fp[entity]) > 0 else 0
            recall = tp[entity] / (tp[entity] + fn[entity]) if (tp[entity] + fn[entity]) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            results[entity] = {
                'precision': round(precision, 4),
                'recall': round(recall, 4),
                'f1': round(f1, 4),
                'support': tp[entity] + fn[entity]
            }

        # Overall metrics
        overall_tp = sum(tp.values())
        overall_fp = sum(fp.values())
        overall_fn = sum(fn.values())

        overall_precision = overall_tp / (overall_tp + overall_fp) if (overall_tp + overall_fp) > 0 else 0
        overall_recall = overall_tp / (overall_tp + overall_fn) if (overall_tp + overall_fn) > 0 else 0
        overall_f1 = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0

        results['OVERALL'] = {
            'precision': round(overall_precision, 4),
            'recall': round(overall_recall, 4),
            'f1': round(overall_f1, 4),
            'support': overall_tp + overall_fn
        }

        return results

    def run_full_pipeline(self):
        """Execute complete NER training pipeline"""
        print("=" * 80)
        print("NER TRAINING PIPELINE")
        print("=" * 80)

        # Process all sectors from validation results
        total_examples = 0
        for sector_name in self.validation_data['sectors'].keys():
            total_examples += self.process_sector_for_training(sector_name)

        print(f"\n✅ Total training examples created: {total_examples}")

        # Print annotation statistics
        print("\n📊 Annotation Statistics:")
        for entity_type, count in self.annotation_stats.items():
            percentage = (count / sum(self.annotation_stats.values()) * 100) if sum(self.annotation_stats.values()) > 0 else 0
            print(f"  {entity_type}: {count:,} ({percentage:.1f}%)")

        # Create dataset splits
        train_data, val_data, test_data = self.create_dataset_splits()

        # Save datasets
        output_dir = self.base_path / "ner_training_data"
        output_dir.mkdir(parents=True, exist_ok=True)

        print("\n💾 Saving Dataset Splits...")
        self.save_spacy_docbin(train_data, output_dir / "train.spacy")
        self.save_spacy_docbin(val_data, output_dir / "dev.spacy")
        self.save_spacy_docbin(test_data, output_dir / "test.spacy")

        # Train model with 50 iterations for expanded dataset
        self.train_ner_model(train_data, val_data, n_iter=50)

        # Evaluate model
        evaluation_results = self.evaluate_model(test_data)

        # Print evaluation results
        print("\n" + "=" * 80)
        print("EVALUATION RESULTS")
        print("=" * 80)

        for entity_type, metrics in evaluation_results.items():
            print(f"\n{entity_type}:")
            print(f"  Precision: {metrics['precision']:.2%}")
            print(f"  Recall: {metrics['recall']:.2%}")
            print(f"  F1-Score: {metrics['f1']:.2%}")
            print(f"  Support: {metrics['support']}")

        # Save trained model
        model_dir = self.base_path / "ner_model"
        self.nlp.to_disk(model_dir)
        print(f"\n💾 Model saved to {model_dir}")

        # Save evaluation results
        eval_file = self.base_path / "Data Pipeline Builder" / "NER_EVALUATION_RESULTS.json"
        with open(eval_file, 'w') as f:
            json.dump({
                'evaluation_metrics': evaluation_results,
                'annotation_stats': self.annotation_stats,
                'dataset_splits': {
                    'train': len(train_data),
                    'validation': len(val_data),
                    'test': len(test_data)
                }
            }, f, indent=2)

        print(f"📄 Evaluation results saved to {eval_file}")

        return evaluation_results


if __name__ == "__main__":
    validation_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/Data Pipeline Builder/PATTERN_EXTRACTION_VALIDATION_RESULTS.json"

    pipeline = NERTrainingPipeline(validation_file)
    results = pipeline.run_full_pipeline()

    print("\n" + "=" * 80)
    print("🎉 NER TRAINING PIPELINE COMPLETE")
    print("=" * 80)
    print(f"\n📊 Overall F1 Score: {results['OVERALL']['f1']:.2%}")
    print(f"✅ Model ready for deployment")
