#!/usr/bin/env python3
"""
V7 NER Training Pipeline - Enhanced with Complete Attack Chain Data
Uses comprehensive dataset with golden bridges, complete chains, and multi-hop paths.

Dataset: V7_NER_TRAINING_DATA.json (2,731 examples)
Improvement over v6: +990 examples (+56.9%)
"""

import spacy
from spacy.tokens import DocBin
from spacy.training import Example
import json
import random
from pathlib import Path
from typing import List, Dict
import sys

class V7NERTrainer:
    """Enhanced NER trainer using v7 comprehensive dataset"""

    def __init__(self, dataset_path: str = "data/ner_training/V7_NER_TRAINING_DATA_SPACY.json"):
        self.dataset_path = Path(dataset_path)

        # Enhanced entity types covering all cybersecurity domains
        self.entity_types = [
            # Core security entities
            'CVE', 'CWE', 'CAPEC', 'ATTACK_TECHNIQUE', 'OWASP', 'WASC',
            # Descriptive variants
            'VULNERABILITY', 'WEAKNESS', 'ATTACK_PATTERN', 'TECHNIQUE',
            # Infrastructure entities
            'SOFTWARE', 'HARDWARE', 'PROTOCOL', 'VERSION',
            # Threat entities
            'THREAT_ACTOR', 'CAMPAIGN', 'INDICATOR',
            # Extended types
            'VENDOR', 'EQUIPMENT', 'OPERATION', 'ARCHITECTURE',
            'SECURITY', 'SUPPLIER', 'THREAT_MODEL', 'TACTIC',
            'SOFTWARE_COMPONENT', 'HARDWARE_COMPONENT',
            'PERSONALITY_TRAIT', 'COGNITIVE_BIAS', 'INSIDER_INDICATOR',
            'SOCIAL_ENGINEERING', 'ATTACK_VECTOR', 'MITIGATION',
            'VULNERABILITY_CLASS', 'ATTACK'
        ]

        self.nlp = spacy.blank("en")
        self.training_data = []

    def load_v7_dataset(self) -> List[Dict]:
        """Load v7 enhanced dataset"""
        print(f"\n📂 Loading V7 dataset from: {self.dataset_path}")

        if not self.dataset_path.exists():
            raise FileNotFoundError(f"V7 dataset not found: {self.dataset_path}")

        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"✅ Loaded {len(data)} training examples")

        # Statistics - handle grouped entity format
        entity_counts = {}
        for example in data:
            entities = example.get('entities', {})
            if isinstance(entities, dict):
                # Grouped format: {label: [values]}
                for label, values in entities.items():
                    if values and len(values) > 0:
                        entity_counts[label] = entity_counts.get(label, 0) + len(values)
            elif isinstance(entities, list):
                # spaCy format: [{start, end, label}]
                for entity in entities:
                    label = entity.get('label', 'UNKNOWN')
                    entity_counts[label] = entity_counts.get(label, 0) + 1

        print(f"\n📊 Entity Distribution:")
        for label, count in sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
            print(f"  {label}: {count}")

        return data

    def create_training_examples(self, data: List[Dict]) -> List[Example]:
        """Convert v7 data to spaCy training examples"""
        examples = []

        print(f"\n🔄 Converting {len(data)} examples to spaCy format...")

        for i, item in enumerate(data):
            if i % 500 == 0:
                print(f"  Processing: {i}/{len(data)}")

            text = item['text']
            entities = item.get('entities', [])

            # Create spaCy doc
            doc = self.nlp.make_doc(text)

            # Create entity spans
            ents = []
            for ent in entities:
                start = ent['start']
                end = ent['end']
                label = ent['label']

                # Validate entity bounds
                if start >= 0 and end <= len(text) and start < end:
                    span = doc.char_span(start, end, label=label, alignment_mode="contract")
                    if span is not None:
                        ents.append(span)

            # Set entities on doc
            try:
                doc.ents = ents
                example = Example.from_dict(doc, {"entities": [(e.start_char, e.end_char, e.label_) for e in ents]})
                examples.append(example)
            except Exception as e:
                print(f"⚠️  Skipping example {i}: {str(e)[:100]}")
                continue

        print(f"✅ Created {len(examples)} valid training examples")
        return examples

    def train_model(self, examples: List[Example], iterations: int = 50):
        """Train enhanced NER model"""
        print(f"\n🎯 Training V7 NER model with {iterations} iterations...")

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

        # Split train/dev (80/20)
        random.shuffle(examples)
        split = int(len(examples) * 0.8)
        train_examples = examples[:split]
        dev_examples = examples[split:]

        print(f"📚 Training set: {len(train_examples)} examples")
        print(f"📊 Dev set: {len(dev_examples)} examples")

        # Training loop
        for iteration in range(iterations):
            random.shuffle(train_examples)
            losses = {}

            # Mini-batch training
            batch_size = 8
            for i in range(0, len(train_examples), batch_size):
                batch = train_examples[i:i+batch_size]
                self.nlp.update(batch, drop=0.3, losses=losses, sgd=optimizer)

            # Periodic evaluation
            if (iteration + 1) % 5 == 0:
                scores = self.evaluate(dev_examples)
                print(f"  Iteration {iteration + 1}/{iterations} - Loss: {losses.get('ner', 0):.4f} - F1: {scores['ents_f']:.2%}")

        print(f"\n✅ Training complete!")
        return self.nlp

    def evaluate(self, examples: List[Example]) -> Dict:
        """Evaluate model on dev set"""
        scores = self.nlp.evaluate(examples)
        return scores

    def save_model(self, output_dir: str = "models/v7_ner_model"):
        """Save trained model"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        self.nlp.to_disk(output_path)
        print(f"\n💾 Model saved to: {output_path}")

    def final_evaluation(self, test_examples: List[Example]):
        """Comprehensive final evaluation"""
        print(f"\n🧪 Final Evaluation on {len(test_examples)} examples...")

        scores = self.evaluate(test_examples)

        print(f"\n📊 V7 NER Model Performance:")
        print(f"  Precision: {scores.get('ents_p', 0):.2%}")
        print(f"  Recall: {scores.get('ents_r', 0):.2%}")
        print(f"  F1-Score: {scores.get('ents_f', 0):.2%}")

        # Per-entity evaluation
        print(f"\n📋 Per-Entity Performance:")
        per_type = scores.get('ents_per_type', {})
        for entity_type, metrics in sorted(per_type.items(), key=lambda x: x[1].get('f', 0), reverse=True)[:20]:
            p = metrics.get('p', 0)
            r = metrics.get('r', 0)
            f = metrics.get('f', 0)
            print(f"  {entity_type:20s} - P: {p:.2%}, R: {r:.2%}, F1: {f:.2%}")

        return scores

def main():
    """Execute V7 NER training pipeline"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     V7 NER TRAINING PIPELINE                                 ║
║                                                                              ║
║  Dataset: V7_NER_TRAINING_DATA_SPACY.json (spaCy format)                    ║
║  Source: Golden bridges + Complete chains + CVE-CWE + CAPEC-ATT&CK          ║
║  Format: Character-level annotations with start/end positions               ║
║  Target: F1 > 85% (v6 baseline: 84.16%)                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    # Initialize trainer
    trainer = V7NERTrainer()

    # Load v7 dataset
    data = trainer.load_v7_dataset()

    # Create training examples
    examples = trainer.create_training_examples(data)

    if len(examples) < 100:
        print(f"\n❌ ERROR: Insufficient training examples ({len(examples)})")
        sys.exit(1)

    # Train model
    trainer.train_model(examples, iterations=50)

    # Final evaluation (use last 20% as test set)
    split = int(len(examples) * 0.8)
    test_examples = examples[split:]
    scores = trainer.final_evaluation(test_examples)

    # Save model
    trainer.save_model("models/v7_ner_model")

    # Save results
    results = {
        "version": "v7",
        "dataset_size": len(data),
        "training_examples": len(examples),
        "improvement_over_v6": "+990 examples (+56.9%)",
        "f1_score": scores.get('ents_f', 0),
        "precision": scores.get('ents_p', 0),
        "recall": scores.get('ents_r', 0),
        "v6_baseline_f1": 0.8416
    }

    with open('data/ner_training/V7_TRAINING_RESULTS.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n🎉 V7 NER TRAINING COMPLETE")
    print(f"📊 Overall F1 Score: {scores.get('ents_f', 0):.2%}")
    print(f"📈 Improvement vs v6: {scores.get('ents_f', 0) - 0.8416:+.2%}")

if __name__ == "__main__":
    main()
