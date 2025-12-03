#!/usr/bin/env python3
"""
MITRE ATT&CK NER Training Data Generator - Phase 2: Incremental Expansion
Scales from 50 to 600+ techniques with comprehensive entity coverage.

Entity Mapping (Phase 2):
- attack-pattern -> ATTACK_TECHNIQUE
- course-of-action -> MITIGATION
- intrusion-set -> THREAT_ACTOR
- malware/tool -> SOFTWARE
- x-mitre-data-source -> DATA_SOURCE (NEW)
- x-mitre-data-component -> DATA_SOURCE (NEW)

Strategy:
- Generate 600+ training examples from all Enterprise ATT&CK techniques
- Stratified sampling: 30% V7 baseline + 70% MITRE for balanced training
- Diverse sentence templates for better generalization
- Target F1 score improvement: >95.5% (from 95.05%)
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Set
from collections import defaultdict
import random

class MitrePhase2NerDataGenerator:
    """Enhanced NER training data generator for Phase 2 expansion"""

    def __init__(self, stix_file: str):
        self.stix_file = Path(stix_file)
        self.data = self._load_stix_data()
        self.entity_counts = defaultdict(int)
        self.technique_ids_used = set()

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
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\[\[.*?\]\]', '', text)  # Remove citation markers
        text = re.sub(r'\(Citation:.*?\)', '', text)  # Remove citations
        return text.strip()

    def _get_technique_id(self, technique: dict) -> str:
        """Extract MITRE ATT&CK ID (e.g., T1003)"""
        for ref in technique.get('external_references', []):
            if ref.get('source_name') == 'mitre-attack':
                return ref.get('external_id', '')
        return ''

    def _get_tactic_names(self, technique: dict) -> List[str]:
        """Extract tactic names from kill chain phases"""
        tactics = []
        for phase in technique.get('kill_chain_phases', []):
            tactic = phase.get('phase_name', '').replace('-', ' ').title()
            if tactic:
                tactics.append(tactic)
        return tactics

    def _create_diverse_sentence(self, technique: dict,
                                  mitigations: List[dict],
                                  actors: List[dict],
                                  software: List[dict],
                                  data_sources: List[dict]) -> Tuple[str, List[Tuple]]:
        """Generate diverse contextual sentences with multiple entities"""

        name = technique.get('name', '')
        tech_id = self._get_technique_id(technique)
        description = technique.get('description', '')
        tactics = self._get_tactic_names(technique)

        # Truncate description intelligently
        sentences = [s.strip() for s in description.split('. ') if s.strip()]
        short_desc = sentences[0] if sentences else description[:150]

        # Track technique ID usage
        self.technique_ids_used.add(tech_id)

        # Template selection with weighting for diversity
        templates = []

        # Template 1: Technique description with ID (20%)
        if tech_id:
            sentence = f"The attack technique {name} ({tech_id}) involves {short_desc}."
            entities = [
                (sentence.find(name), sentence.find(name) + len(name), 'ATTACK_TECHNIQUE'),
                (sentence.find(tech_id), sentence.find(tech_id) + len(tech_id), 'ATTACK_TECHNIQUE')
            ]
            templates.append((sentence, entities, 20))

        # Template 2: Threat actor using technique (25%)
        if actors:
            actor = random.choice(actors)
            actor_name = actor.get('name', '')
            if tactics:
                tactic = random.choice(tactics)
                sentence = f"Threat actor {actor_name} has been observed using {name} ({tech_id}) during the {tactic} phase of attacks."
            else:
                sentence = f"Security researchers identified {actor_name} leveraging {name} to compromise target systems."

            entities = [
                (sentence.find(actor_name), sentence.find(actor_name) + len(actor_name), 'THREAT_ACTOR'),
                (sentence.find(name), sentence.find(name) + len(name), 'ATTACK_TECHNIQUE')
            ]
            if tech_id and tech_id in sentence:
                entities.append((sentence.find(tech_id), sentence.find(tech_id) + len(tech_id), 'ATTACK_TECHNIQUE'))
            templates.append((sentence, entities, 25))

        # Template 3: Mitigation strategy (20%)
        if mitigations:
            mit = random.choice(mitigations)
            mit_name = mit.get('name', '')
            sentence = f"Organizations can defend against {name} by implementing {mit_name} security controls."
            entities = [
                (sentence.find(name), sentence.find(name) + len(name), 'ATTACK_TECHNIQUE'),
                (sentence.find(mit_name), sentence.find(mit_name) + len(mit_name), 'MITIGATION')
            ]
            templates.append((sentence, entities, 20))

        # Template 4: Software implementation (15%)
        if software:
            sw = random.choice(software)
            sw_name = sw.get('name', '')
            sentence = f"The malware family {sw_name} employs {name} ({tech_id}) to evade detection and maintain persistence."
            entities = [
                (sentence.find(sw_name), sentence.find(sw_name) + len(sw_name), 'SOFTWARE'),
                (sentence.find(name), sentence.find(name) + len(name), 'ATTACK_TECHNIQUE'),
                (sentence.find(tech_id), sentence.find(tech_id) + len(tech_id), 'ATTACK_TECHNIQUE')
            ]
            templates.append((sentence, entities, 15))

        # Template 5: Data source detection (NEW for Phase 2) (10%)
        if data_sources:
            ds = random.choice(data_sources)
            ds_name = ds.get('name', '')
            if ds_name:
                sentence = f"Security teams can detect {name} ({tech_id}) by monitoring {ds_name} for suspicious activity."
                entities = [
                    (sentence.find(name), sentence.find(name) + len(name), 'ATTACK_TECHNIQUE'),
                    (sentence.find(tech_id), sentence.find(tech_id) + len(tech_id), 'ATTACK_TECHNIQUE'),
                    (sentence.find(ds_name), sentence.find(ds_name) + len(ds_name), 'DATA_SOURCE')
                ]
                templates.append((sentence, entities, 10))

        # Template 6: Multi-entity complex scenario (10%)
        if actors and mitigations and software:
            actor = random.choice(actors)
            mit = random.choice(mitigations)
            sw = random.choice(software)
            actor_name = actor.get('name', '')
            mit_name = mit.get('name', '')
            sw_name = sw.get('name', '')

            sentence = f"After {actor_name} was discovered using {sw_name} to execute {name}, security teams deployed {mit_name} as countermeasure."
            entities = [
                (sentence.find(actor_name), sentence.find(actor_name) + len(actor_name), 'THREAT_ACTOR'),
                (sentence.find(sw_name), sentence.find(sw_name) + len(sw_name), 'SOFTWARE'),
                (sentence.find(name), sentence.find(name) + len(name), 'ATTACK_TECHNIQUE'),
                (sentence.find(mit_name), sentence.find(mit_name) + len(mit_name), 'MITIGATION')
            ]
            templates.append((sentence, entities, 10))

        # Weighted random selection
        if templates:
            total_weight = sum(w for _, _, w in templates)
            r = random.uniform(0, total_weight)
            cumulative = 0
            for sentence, entities, weight in templates:
                cumulative += weight
                if r <= cumulative:
                    selected_sentence, selected_entities = sentence, entities
                    break
            else:
                selected_sentence, selected_entities = templates[0][:2]
        else:
            # Fallback
            selected_sentence = f"{name} ({tech_id}) is an attack technique in the MITRE ATT&CK framework."
            selected_entities = [
                (selected_sentence.find(name), selected_sentence.find(name) + len(name), 'ATTACK_TECHNIQUE'),
                (selected_sentence.find(tech_id), selected_sentence.find(tech_id) + len(tech_id), 'ATTACK_TECHNIQUE')
            ]

        # Validate and filter entities
        valid_entities = []
        for start, end, label in selected_entities:
            if start >= 0 and end <= len(selected_sentence) and start < end:
                valid_entities.append((start, end, label))
                self.entity_counts[label] += 1

        return self._clean_text(selected_sentence), valid_entities

    def extract_all_techniques(self) -> List[dict]:
        """Extract ALL attack techniques from MITRE ATT&CK (600+ for Phase 2)"""
        techniques = self._extract_objects_by_type('attack-pattern')

        # Filter to valid techniques only
        valid_techniques = [
            t for t in techniques
            if t.get('name') and
               t.get('description') and
               not t.get('x_mitre_deprecated', False) and
               not t.get('revoked', False) and
               any(ref.get('source_name') == 'mitre-attack'
                   for ref in t.get('external_references', []))
        ]

        # Sort by ID for consistent ordering
        valid_techniques.sort(key=lambda x: self._get_technique_id(x))

        return valid_techniques

    def extract_data_sources(self) -> List[dict]:
        """Extract data sources for detection (NEW for Phase 2)"""
        data_sources = []

        # x-mitre-data-source objects
        ds_objects = self._extract_objects_by_type('x-mitre-data-source')
        data_sources.extend(ds_objects)

        # x-mitre-data-component objects
        dc_objects = self._extract_objects_by_type('x-mitre-data-component')
        data_sources.extend(dc_objects)

        return data_sources

    def generate_comprehensive_training_data(self) -> List[dict]:
        """Generate comprehensive Phase 2 training data (600+ examples)"""

        print("=" * 80)
        print("Phase 2: Extracting ALL MITRE ATT&CK techniques...")
        print("=" * 80)

        techniques = self.extract_all_techniques()
        mitigations = self._extract_objects_by_type('course-of-action')
        actors = self._extract_objects_by_type('intrusion-set')
        malware = self._extract_objects_by_type('malware')
        tools = self._extract_objects_by_type('tool')
        data_sources = self.extract_data_sources()

        software = malware + tools

        print(f"\nFound MITRE ATT&CK objects:")
        print(f"  Techniques: {len(techniques)}")
        print(f"  Mitigations: {len(mitigations)}")
        print(f"  Threat Actors: {len(actors)}")
        print(f"  Software (Malware + Tools): {len(software)}")
        print(f"  Data Sources: {len(data_sources)}")
        print(f"\nTarget: Generate 600+ training examples\n")

        training_data = []

        # Generate 1 example per technique minimum
        for idx, technique in enumerate(techniques, 1):
            if idx % 100 == 0:
                print(f"Processing technique {idx}/{len(techniques)}...")

            # Generate 1-2 examples per technique for diversity
            num_variants = random.randint(1, 2) if idx % 3 == 0 else 1

            for _ in range(num_variants):
                sentence, entities = self._create_diverse_sentence(
                    technique, mitigations, actors, software, data_sources
                )

                if entities:
                    training_example = {
                        "text": sentence,
                        "entities": entities
                    }
                    training_data.append(training_example)

        print(f"\n" + "=" * 80)
        print(f"Phase 2 Generation Complete")
        print("=" * 80)
        print(f"\nGenerated {len(training_data)} training examples")
        print(f"Unique technique IDs: {len(self.technique_ids_used)}")
        print(f"\nEntity distribution:")
        total_entities = sum(self.entity_counts.values())
        for entity_type, count in sorted(self.entity_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_entities) * 100
            print(f"  {entity_type}: {count} ({percentage:.1f}%)")

        return training_data

    def save_training_data(self, training_data: List[dict], output_file: str):
        """Save training data in spaCy v3 format"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        spacy_format = {
            "version": "2.0",
            "source": "MITRE ATT&CK Phase 2 - Incremental Expansion",
            "annotations": training_data,
            "metadata": {
                "entity_distribution": dict(self.entity_counts),
                "total_examples": len(training_data),
                "unique_techniques": len(self.technique_ids_used),
                "mitre_version": "17.0",
                "phase": "2",
                "stratified_sampling": "30% V7 baseline + 70% MITRE"
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(spacy_format, f, indent=2, ensure_ascii=False)

        print(f"\nTraining data saved to: {output_path}")
        print(f"File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")


def main():
    """Main execution function"""

    # Paths
    stix_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/MITRE-ATT-CK-STIX/enterprise-attack/enterprise-attack-17.0.json"
    output_file = "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/data/ner_training/mitre_phase2_training_data.json"

    print("=" * 80)
    print("MITRE ATT&CK NER Training Data Generator - Phase 2")
    print("Incremental Expansion: 50 → 600+ Techniques")
    print("=" * 80)
    print(f"\nSource: {stix_file}")
    print(f"Target: {output_file}")
    print(f"Goal: Generate 600+ comprehensive NER training examples")
    print(f"Strategy: Stratified sampling (30% V7 + 70% MITRE)")
    print(f"New entities: DATA_SOURCE added for detection coverage")
    print(f"Target F1: >95.5% (from 95.05% baseline)\n")

    # Generate comprehensive Phase 2 training data
    generator = MitrePhase2NerDataGenerator(stix_file)
    training_data = generator.generate_comprehensive_training_data()

    # Save to file
    generator.save_training_data(training_data, output_file)

    print("\n" + "=" * 80)
    print("Next Steps:")
    print("=" * 80)
    print("1. Validate training data: python scripts/validate_mitre_phase2_training.py")
    print("2. Merge with V7 baseline using stratified sampling (30% V7, 70% MITRE)")
    print("3. Retrain NER model with combined dataset")
    print("4. Evaluate F1 score improvement (target: >95.5%)")
    print("5. Proceed to Phase 3 if targets met")
    print("\n")


if __name__ == "__main__":
    main()
