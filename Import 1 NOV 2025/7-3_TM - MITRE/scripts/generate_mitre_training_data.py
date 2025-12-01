#!/usr/bin/env python3
"""
MITRE ATT&CK NER Training Data Generator
Extracts top 50 MITRE ATT&CK techniques and generates spaCy-format training data
to improve NER F1 score by balancing entity distribution.

Entity Mapping:
- attack-pattern -> ATTACK_TECHNIQUE
- course-of-action -> MITIGATION
- intrusion-set -> THREAT_ACTOR
- malware/tool -> SOFTWARE

Target: Fix V7 entity imbalance (VULNERABILITY 42%, CAPEC 36%, CWE 21%)
by adding more diverse entity types from MITRE ATT&CK.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict
import random

class MitreNerDataGenerator:
    """Generate NER training data from MITRE ATT&CK STIX data"""

    def __init__(self, stix_file: str):
        self.stix_file = Path(stix_file)
        self.data = self._load_stix_data()
        self.entity_counts = defaultdict(int)

    def _load_stix_data(self) -> dict:
        """Load MITRE ATT&CK STIX JSON data"""
        with open(self.stix_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _extract_objects_by_type(self, obj_type: str) -> List[dict]:
        """Extract STIX objects by type"""
        return [obj for obj in self.data.get('objects', [])
                if obj.get('type') == obj_type]

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for NER training"""
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might interfere with NER
        text = text.strip()
        return text

    def _create_entity_annotation(self, text: str, entity_text: str,
                                   entity_type: str, start_pos: int = None) -> Tuple[int, int, str]:
        """Create entity annotation tuple (start, end, label)"""
        if start_pos is None:
            start_pos = text.find(entity_text)

        if start_pos == -1:
            return None

        end_pos = start_pos + len(entity_text)
        return (start_pos, end_pos, entity_type)

    def _generate_contextual_sentence(self, technique: dict,
                                       mitigations: List[dict],
                                       actors: List[dict],
                                       software: List[dict]) -> Tuple[str, List[Tuple]]:
        """Generate contextual sentence with multiple entities"""

        name = technique.get('name', '')
        tech_id = technique.get('external_references', [{}])[0].get('external_id', '')
        description = technique.get('description', '')

        # Truncate description to manageable length
        desc_sentences = description.split('. ')
        short_desc = desc_sentences[0] if desc_sentences else description[:200]

        entities = []

        # Strategy: Create natural sentences with entities
        templates = []

        # Template 1: Technique with mitigation
        if mitigations:
            mit = random.choice(mitigations)
            mit_name = mit.get('name', '')
            sentence = f"{name} ({tech_id}) is a technique where {short_desc}. This can be mitigated using {mit_name}."
            entities = [
                (sentence.find(name), sentence.find(name) + len(name), 'ATTACK_TECHNIQUE'),
                (sentence.find(tech_id), sentence.find(tech_id) + len(tech_id), 'ATTACK_TECHNIQUE'),
                (sentence.find(mit_name), sentence.find(mit_name) + len(mit_name), 'MITIGATION')
            ]
            templates.append((sentence, entities))

        # Template 2: Technique with threat actor
        if actors:
            actor = random.choice(actors)
            actor_name = actor.get('name', '')
            sentence = f"Threat group {actor_name} has been observed using {name} to compromise systems."
            entities = [
                (sentence.find(actor_name), sentence.find(actor_name) + len(actor_name), 'THREAT_ACTOR'),
                (sentence.find(name), sentence.find(name) + len(name), 'ATTACK_TECHNIQUE')
            ]
            templates.append((sentence, entities))

        # Template 3: Technique with software
        if software:
            sw = random.choice(software)
            sw_name = sw.get('name', '')
            sentence = f"The malware {sw_name} implements {name} ({tech_id}) to evade detection."
            entities = [
                (sentence.find(sw_name), sentence.find(sw_name) + len(sw_name), 'SOFTWARE'),
                (sentence.find(name), sentence.find(name) + len(name), 'ATTACK_TECHNIQUE'),
                (sentence.find(tech_id), sentence.find(tech_id) + len(tech_id), 'ATTACK_TECHNIQUE')
            ]
            templates.append((sentence, entities))

        # Template 4: Multiple entities
        if mitigations and actors:
            mit = random.choice(mitigations)
            actor = random.choice(actors)
            mit_name = mit.get('name', '')
            actor_name = actor.get('name', '')
            sentence = f"Security teams detected {actor_name} using {name} and applied {mit_name} as countermeasure."
            entities = [
                (sentence.find(actor_name), sentence.find(actor_name) + len(actor_name), 'THREAT_ACTOR'),
                (sentence.find(name), sentence.find(name) + len(name), 'ATTACK_TECHNIQUE'),
                (sentence.find(mit_name), sentence.find(mit_name) + len(mit_name), 'MITIGATION')
            ]
            templates.append((sentence, entities))

        # Select random template
        if templates:
            sentence, entities = random.choice(templates)
        else:
            # Fallback: simple technique mention
            sentence = f"{name} ({tech_id}) is an attack technique used in cyber operations."
            entities = [
                (sentence.find(name), sentence.find(name) + len(name), 'ATTACK_TECHNIQUE'),
                (sentence.find(tech_id), sentence.find(tech_id) + len(tech_id), 'ATTACK_TECHNIQUE')
            ]

        # Filter out None entities and ensure valid positions
        valid_entities = [e for e in entities if e and e[0] >= 0 and e[1] <= len(sentence)]

        # Track entity counts
        for _, _, label in valid_entities:
            self.entity_counts[label] += 1

        return self._clean_text(sentence), valid_entities

    def extract_top_techniques(self, limit: int = 50) -> List[dict]:
        """Extract top N attack techniques"""
        techniques = self._extract_objects_by_type('attack-pattern')

        # Filter to only include techniques with proper metadata
        valid_techniques = [
            t for t in techniques
            if t.get('name') and
               t.get('description') and
               any(ref.get('source_name') == 'mitre-attack'
                   for ref in t.get('external_references', []))
        ]

        # Sort by modified date (most recent first)
        valid_techniques.sort(
            key=lambda x: x.get('modified', ''),
            reverse=True
        )

        return valid_techniques[:limit]

    def generate_training_data(self, num_examples: int = 50) -> List[dict]:
        """Generate spaCy-format training data"""

        print(f"Extracting MITRE ATT&CK data...")
        techniques = self.extract_top_techniques(num_examples)
        mitigations = self._extract_objects_by_type('course-of-action')[:30]
        actors = self._extract_objects_by_type('intrusion-set')[:25]

        # Get software (both malware and tools)
        malware = self._extract_objects_by_type('malware')[:20]
        tools = self._extract_objects_by_type('tool')[:20]
        software = malware + tools

        print(f"Found: {len(techniques)} techniques, {len(mitigations)} mitigations, "
              f"{len(actors)} actors, {len(software)} software")

        training_data = []

        for technique in techniques:
            # Generate 1-2 training examples per technique for variety
            num_variants = random.randint(1, 2)

            for _ in range(num_variants):
                sentence, entities = self._generate_contextual_sentence(
                    technique, mitigations, actors, software
                )

                if entities:  # Only add if we have valid entities
                    training_example = {
                        "text": sentence,
                        "entities": entities
                    }
                    training_data.append(training_example)

        print(f"\nGenerated {len(training_data)} training examples")
        print(f"Entity distribution:")
        for entity_type, count in sorted(self.entity_counts.items()):
            percentage = (count / sum(self.entity_counts.values())) * 100
            print(f"  {entity_type}: {count} ({percentage:.1f}%)")

        return training_data

    def save_training_data(self, training_data: List[dict], output_file: str):
        """Save training data to JSON file in spaCy format"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Format for spaCy v3
        spacy_format = {
            "version": "1.0",
            "source": "MITRE ATT&CK Phase 1",
            "annotations": training_data,
            "metadata": {
                "entity_distribution": dict(self.entity_counts),
                "total_examples": len(training_data),
                "mitre_version": "17.0"
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(spacy_format, f, indent=2, ensure_ascii=False)

        print(f"\nTraining data saved to: {output_path}")
        print(f"Total examples: {len(training_data)}")


def main():
    """Main execution function"""

    # Paths
    stix_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/MITRE-ATT-CK-STIX/enterprise-attack/enterprise-attack-17.0.json"
    output_file = "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/data/ner_training/mitre_phase1_training_data.json"

    print("=" * 70)
    print("MITRE ATT&CK NER Training Data Generator - Phase 1")
    print("=" * 70)
    print(f"\nSource: {stix_file}")
    print(f"Target: {output_file}")
    print(f"Goal: Generate 50 high-quality NER training examples")
    print(f"Strategy: Balance entity distribution to improve F1 score\n")

    # Generate training data
    generator = MitreNerDataGenerator(stix_file)
    training_data = generator.generate_training_data(num_examples=50)

    # Save to file
    generator.save_training_data(training_data, output_file)

    print("\n" + "=" * 70)
    print("Phase 1 Complete")
    print("=" * 70)
    print("\nNext Steps:")
    print("1. Run validation: python scripts/validate_mitre_training_impact.py")
    print("2. Review training data quality")
    print("3. Proceed to Phase 2 if F1 improvement confirmed")


if __name__ == "__main__":
    main()
