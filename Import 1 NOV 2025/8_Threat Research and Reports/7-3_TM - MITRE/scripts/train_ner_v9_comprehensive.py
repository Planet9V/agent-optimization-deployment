#!/usr/bin/env python3
"""
V9 NER Training Pipeline - Comprehensive Infrastructure + Cybersecurity + MITRE Dataset
Merges infrastructure (v5/v6) + cybersecurity (v7) + MITRE data

Dataset: v9_comprehensive_training_data.json
Target: F1 score >96.0%
Entity types: 16 comprehensive categories
"""

import spacy
from spacy.tokens import DocBin
from spacy.training import Example
import json
import random
from pathlib import Path
from typing import List, Dict, Tuple
import sys
from collections import Counter
import numpy as np

class V9ComprehensiveNERTrainer:
    """V9 NER trainer using comprehensive infrastructure + cybersecurity + MITRE dataset"""

    def __init__(self, dataset_path: str = "data/ner_training/v9_comprehensive_training_data.json"):
        self.dataset_path = Path(dataset_path)

        # 16 comprehensive entity types
        self.entity_types = [
            # Infrastructure entities
            'VENDOR', 'EQUIPMENT', 'PROTOCOL', 'SECURITY',
            'HARDWARE_COMPONENT', 'SOFTWARE_COMPONENT', 'INDICATOR', 'MITIGATION',
            # Cybersecurity entities
            'CVE', 'CWE', 'CAPEC', 'VULNERABILITY',
            'ATTACK_TECHNIQUE', 'WEAKNESS', 'THREAT_ACTOR',
            # Software/Data entities
            'SOFTWARE', 'DATA_SOURCE'
        ]

        self.nlp = spacy.blank("en")
        self.training_data = []

    def load_comprehensive_dataset(self) -> List[Tuple]:
        """Load v9 comprehensive dataset"""
        print(f"\n📂 Loading V9 Comprehensive dataset from: {self.dataset_path}")

        if not self.dataset_path.exists():
            raise FileNotFoundError(f"V9 dataset not found: {self.dataset_path}")

        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"✅ Loaded {len(data)} training examples")

        # Statistics
        entity_counts = Counter()
        source_counts = Counter()

        for example in data:
            text, annotations = example
            entities = annotations.get('entities', [])
            for start, end, label in entities:
                entity_counts[label] += 1

        print(f"\n📊 Entity Distribution:")
        total_entities = sum(entity_counts.values())
        for label, count in entity_counts.most_common():
            percentage = (count / total_entities) * 100
            print(f"  {label:25s}: {count:5d} ({percentage:5.2f}%)")

        return data

    def create_training_examples(self, data: List[Tuple]) -> List[Example]:
        """Convert v9 data to spaCy training examples"""
        examples = []
        skipped = 0

        print(f"\n🔄 Converting {len(data)} examples to spaCy format...")

        for i, (text, annotations) in enumerate(data):
            if i % 300 == 0:
                print(f"  Processing: {i}/{len(data)}")

            entities = annotations.get('entities', [])

            # Create spaCy doc
            doc = self.nlp.make_doc(text)

            # Create entity spans
            ents = []
            for start, end, label in entities:
                # Validate entity bounds
                if start >= 0 and end <= len(text) and start < end:
                    span = doc.char_span(start, end, label=label, alignment_mode="contract")
                    if span is not None:
                        ents.append(span)
                    else:
                        skipped += 1

            # Set entities on doc
            try:
                doc.ents = ents
                example = Example.from_dict(doc, {"entities": [(e.start_char, e.end_char, e.label_) for e in ents]})
                examples.append(example)
            except Exception as e:
                skipped += 1
                continue

        print(f"✅ Created {len(examples)} valid training examples")
        print(f"⚠️  Skipped {skipped} entity annotations due to alignment issues")
        return examples

    def stratified_split(self, examples: List[Example],
                        train_ratio: float = 0.70,
                        dev_ratio: float = 0.15,
                        test_ratio: float = 0.15) -> Tuple[List[Example], List[Example], List[Example]]:
        """Stratified train/dev/test split maintaining entity distribution"""

        assert abs(train_ratio + dev_ratio + test_ratio - 1.0) < 0.01, "Ratios must sum to 1.0"

        # Group examples by their entity types
        entity_groups = {etype: [] for etype in self.entity_types}
        unclassified = []

        for example in examples:
            doc = example.reference
            if doc.ents:
                # Assign to first entity type found
                primary_label = doc.ents[0].label_
                if primary_label in entity_groups:
                    entity_groups[primary_label].append(example)
                else:
                    unclassified.append(example)
            else:
                unclassified.append(example)

        # Split each group proportionally
        train_examples = []
        dev_examples = []
        test_examples = []

        for entity_type, group in entity_groups.items():
            if not group:
                continue

            random.shuffle(group)
            n = len(group)

            train_end = int(n * train_ratio)
            dev_end = train_end + int(n * dev_ratio)

            train_examples.extend(group[:train_end])
            dev_examples.extend(group[train_end:dev_end])
            test_examples.extend(group[dev_end:])

        # Add unclassified to training
        if unclassified:
            random.shuffle(unclassified)
            train_examples.extend(unclassified)

        # Shuffle final sets
        random.shuffle(train_examples)
        random.shuffle(dev_examples)
        random.shuffle(test_examples)

        print(f"\n📚 Stratified Split:")
        print(f"  Training:   {len(train_examples)} examples ({len(train_examples)/len(examples)*100:.1f}%)")
        print(f"  Dev:        {len(dev_examples)} examples ({len(dev_examples)/len(examples)*100:.1f}%)")
        print(f"  Test:       {len(test_examples)} examples ({len(test_examples)/len(examples)*100:.1f}%)")

        return train_examples, dev_examples, test_examples

    def train_model(self, train_examples: List[Example],
                   dev_examples: List[Example],
                   iterations: int = 120,
                   patience: int = 12):
        """Train NER model with early stopping"""
        print(f"\n🎯 Training V9 NER model with {iterations} max iterations...")

        # Add NER pipeline
        if "ner" not in self.nlp.pipe_names:
            ner = self.nlp.add_pipe("ner")
        else:
            ner = self.nlp.get_pipe("ner")

        # Add all entity labels
        for entity_type in self.entity_types:
            ner.add_label(entity_type)

        # Initialize training
        optimizer = self.nlp.initialize()

        print(f"📚 Training set: {len(train_examples)} examples")
        print(f"📊 Dev set: {len(dev_examples)} examples")

        # Early stopping tracking
        best_f1 = 0.0
        patience_counter = 0
        best_model = None

        # Training loop
        for iteration in range(iterations):
            random.shuffle(train_examples)
            losses = {}

            # Mini-batch training
            batch_size = 8
            for i in range(0, len(train_examples), batch_size):
                batch = train_examples[i:i+batch_size]
                self.nlp.update(batch, drop=0.35, losses=losses, sgd=optimizer)

            # Periodic evaluation
            if (iteration + 1) % 5 == 0:
                scores = self.evaluate(dev_examples)
                current_f1 = scores['ents_f']

                print(f"  Iteration {iteration + 1:3d}/{iterations} - Loss: {losses.get('ner', 0):7.4f} - F1: {current_f1:.2%} - P: {scores['ents_p']:.2%} - R: {scores['ents_r']:.2%}")

                # Early stopping check
                if current_f1 > best_f1:
                    best_f1 = current_f1
                    patience_counter = 0
                    best_model = self.nlp.to_bytes()
                    print(f"    ✨ New best F1: {best_f1:.2%}")
                else:
                    patience_counter += 1

                if patience_counter >= patience:
                    print(f"\n⏸️  Early stopping triggered at iteration {iteration + 1}")
                    print(f"    Best F1: {best_f1:.2%} (patience: {patience})")
                    break

        # Restore best model
        if best_model is not None:
            self.nlp.from_bytes(best_model)
            print(f"\n✅ Restored best model (F1: {best_f1:.2%})")

        print(f"\n✅ Training complete!")
        return self.nlp

    def evaluate(self, examples: List[Example]) -> Dict:
        """Evaluate model on examples"""
        scores = self.nlp.evaluate(examples)
        return scores

    def save_model(self, output_dir: str = "models/ner_v9_comprehensive"):
        """Save trained model"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        self.nlp.to_disk(output_path)
        print(f"\n💾 Model saved to: {output_path}")

    def comprehensive_evaluation(self, test_examples: List[Example]) -> Dict:
        """Comprehensive final evaluation with per-entity metrics"""
        print(f"\n🧪 Final Evaluation on {len(test_examples)} test examples...")

        scores = self.evaluate(test_examples)

        print(f"\n📊 V9 NER Model Performance:")
        print(f"  Precision:  {scores.get('ents_p', 0):.4f} ({scores.get('ents_p', 0)*100:.2f}%)")
        print(f"  Recall:     {scores.get('ents_r', 0):.4f} ({scores.get('ents_r', 0)*100:.2f}%)")
        print(f"  F1-Score:   {scores.get('ents_f', 0):.4f} ({scores.get('ents_f', 0)*100:.2f}%)")

        # Per-entity evaluation
        print(f"\n📋 Per-Entity Type Performance:")
        print(f"  {'Entity Type':25s} {'Precision':>10s} {'Recall':>10s} {'F1':>10s} {'Count':>8s}")
        print(f"  {'-'*25} {'-'*10} {'-'*10} {'-'*10} {'-'*8}")

        per_type = scores.get('ents_per_type', {})
        for entity_type in sorted(self.entity_types):
            if entity_type in per_type:
                metrics = per_type[entity_type]
                p = metrics.get('p', 0)
                r = metrics.get('r', 0)
                f = metrics.get('f', 0)
                count = metrics.get('tp', 0) + metrics.get('fp', 0)
                print(f"  {entity_type:25s} {p:10.4f} {r:10.4f} {f:10.4f} {count:8d}")
            else:
                print(f"  {entity_type:25s} {'N/A':>10s} {'N/A':>10s} {'N/A':>10s} {'0':>8s}")

        # Validation against target
        target_f1 = 0.960
        achieved_f1 = scores.get('ents_f', 0)

        print(f"\n🎯 Target Validation:")
        print(f"  Target F1:   {target_f1:.4f} ({target_f1*100:.2f}%)")
        print(f"  Achieved F1: {achieved_f1:.4f} ({achieved_f1*100:.2f}%)")

        if achieved_f1 >= target_f1:
            print(f"  ✅ TARGET MET! (+{(achieved_f1-target_f1)*100:.2f}% above target)")
        else:
            print(f"  ❌ TARGET MISSED (-{(target_f1-achieved_f1)*100:.2f}% below target)")

        return scores

def main():
    """Execute V9 NER training pipeline"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     V9 NER TRAINING PIPELINE                                 ║
║          Comprehensive Infrastructure + Cybersecurity + MITRE                ║
║                                                                              ║
║  Dataset: v9_comprehensive_training_data.json                                ║
║  Sources: Infrastructure (v5/v6) + Cybersecurity (v7) + MITRE               ║
║  Entity Types: 16 comprehensive categories                                  ║
║  Target: F1 > 96.0%                                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    # Initialize trainer
    trainer = V9ComprehensiveNERTrainer()

    # Load comprehensive dataset
    data = trainer.load_comprehensive_dataset()

    # Create training examples
    examples = trainer.create_training_examples(data)

    if len(examples) < 100:
        print(f"\n❌ ERROR: Insufficient training examples ({len(examples)})")
        sys.exit(1)

    # Stratified split: 70% train, 15% dev, 15% test
    train_examples, dev_examples, test_examples = trainer.stratified_split(
        examples,
        train_ratio=0.70,
        dev_ratio=0.15,
        test_ratio=0.15
    )

    # Train model with early stopping
    trainer.train_model(
        train_examples,
        dev_examples,
        iterations=120,
        patience=12
    )

    # Final evaluation on held-out test set
    scores = trainer.comprehensive_evaluation(test_examples)

    # Save model
    output_dir = "models/ner_v9_comprehensive"
    trainer.save_model(output_dir)

    # Save metrics report
    results = {
        "version": "v9",
        "dataset": "v9_comprehensive",
        "dataset_size": len(data),
        "training_examples": len(examples),
        "train_size": len(train_examples),
        "dev_size": len(dev_examples),
        "test_size": len(test_examples),
        "entity_types": trainer.entity_types,
        "target_f1": 0.960,
        "achieved_f1": scores.get('ents_f', 0),
        "precision": scores.get('ents_p', 0),
        "recall": scores.get('ents_r', 0),
        "baseline_f1": 0.9505,
        "improvement_vs_baseline": scores.get('ents_f', 0) - 0.9505,
        "target_met": scores.get('ents_f', 0) >= 0.960,
        "per_entity_scores": scores.get('ents_per_type', {})
    }

    metrics_path = Path("data/ner_training/v9_training_metrics.json")
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    with open(metrics_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📊 Metrics saved to: {metrics_path}")

    # Final summary
    print(f"\n{'='*80}")
    print(f"🎉 V9 NER TRAINING COMPLETE")
    print(f"{'='*80}")
    print(f"📦 Model: {output_dir}")
    print(f"📊 Overall F1 Score: {scores.get('ents_f', 0):.4f} ({scores.get('ents_f', 0)*100:.2f}%)")
    print(f"📈 Improvement vs baseline: {scores.get('ents_f', 0) - 0.9505:+.4f} ({(scores.get('ents_f', 0) - 0.9505)*100:+.2f}%)")
    print(f"🎯 Target (96.0%): {'✅ MET' if scores.get('ents_f', 0) >= 0.960 else '❌ MISSED'}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
