#!/usr/bin/env python3
"""
Extract CWE→CAPEC→ATT&CK training examples from Neo4j database.

File: scripts/extract_attack_chain_training.py
Created: 2025-11-08
Purpose: Extract attack chain data for spaCy NER training
Status: ACTIVE
"""

import json
import os
from neo4j import GraphDatabase
from typing import List, Dict, Any
from collections import Counter


class AttackChainExtractor:
    """Extract attack chain training data from Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        """Initialize Neo4j connection."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Close Neo4j connection."""
        self.driver.close()

    def extract_chains(self) -> List[Dict[str, Any]]:
        """
        Extract CWE→CAPEC→ATT&CK chains from Neo4j.

        Returns:
            List of chain dictionaries with CWE, CAPEC, and ATT&CK data
        """
        query = """
        MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
              -[:USES_TECHNIQUE]->(attack:AttackTechnique)
        WHERE cwe.id IS NOT NULL
          AND capec.capecId IS NOT NULL
          AND capec.name IS NOT NULL
          AND attack.techniqueId IS NOT NULL
        RETURN
          cwe.id as cwe_id,
          cwe.name as cwe_name,
          cwe.description as cwe_description,
          capec.capecId as capec_id,
          capec.name as capec_name,
          capec.description as capec_description,
          attack.techniqueId as attack_id,
          attack.name as attack_name,
          attack.description as attack_description
        """

        with self.driver.session() as session:
            result = session.run(query)
            chains = []
            for record in result:
                chains.append({
                    'cwe_id': record['cwe_id'],
                    'cwe_name': record['cwe_name'] or '',
                    'cwe_description': record['cwe_description'] or '',
                    'capec_id': record['capec_id'],
                    'capec_name': record['capec_name'] or '',
                    'capec_description': record['capec_description'] or '',
                    'attack_id': record['attack_id'],
                    'attack_name': record['attack_name'] or '',
                    'attack_description': record['attack_description'] or ''
                })
            return chains

    def convert_to_spacy_format(self, chains: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Convert attack chains to spaCy v3 training format.

        Args:
            chains: List of attack chain dictionaries

        Returns:
            List of spaCy training examples with text and entities
        """
        training_data = []

        for chain in chains:
            # Create descriptive text from chain
            text = (
                f"{chain['cwe_id']} {chain['cwe_name']} enables "
                f"{chain['capec_id']} {chain['capec_name']} using "
                f"{chain['attack_id']} {chain['attack_name']}. "
            )

            # Add descriptions if available
            if chain['cwe_description']:
                text += f"Weakness: {chain['cwe_description'][:200]}... "
            if chain['capec_description']:
                text += f"Attack Pattern: {chain['capec_description'][:200]}... "
            if chain['attack_description']:
                text += f"Technique: {chain['attack_description'][:200]}..."

            # Find entity positions
            entities = []

            # CWE entity
            cwe_start = text.find(chain['cwe_id'])
            if cwe_start != -1:
                cwe_end = cwe_start + len(chain['cwe_id'])
                entities.append({
                    "start": cwe_start,
                    "end": cwe_end,
                    "label": "CWE"
                })

            # CAPEC entity
            capec_start = text.find(chain['capec_id'])
            if capec_start != -1:
                capec_end = capec_start + len(chain['capec_id'])
                entities.append({
                    "start": capec_start,
                    "end": capec_end,
                    "label": "CAPEC"
                })

            # ATT&CK entity
            attack_start = text.find(chain['attack_id'])
            if attack_start != -1:
                attack_end = attack_start + len(chain['attack_id'])
                entities.append({
                    "start": attack_start,
                    "end": attack_end,
                    "label": "ATTACK"
                })

            training_data.append({
                "text": text,
                "entities": entities
            })

        return training_data

    def calculate_stats(self, chains: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistics about extracted chains.

        Args:
            chains: List of attack chain dictionaries

        Returns:
            Dictionary with statistics
        """
        unique_cwes = set(c['cwe_id'] for c in chains)
        unique_capecs = set(c['capec_id'] for c in chains)
        unique_attacks = set(c['attack_id'] for c in chains)

        # Calculate diversity score (average unique entities per chain)
        total_entities = len(unique_cwes) + len(unique_capecs) + len(unique_attacks)
        diversity_score = total_entities / (3 * len(chains)) if chains else 0

        return {
            'total_chains': len(chains),
            'unique_cwes': len(unique_cwes),
            'unique_capecs': len(unique_capecs),
            'unique_attacks': len(unique_attacks),
            'diversity_score': round(diversity_score, 3)
        }


def main():
    """Main execution function."""
    # Neo4j connection details
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "neo4j@openspg"

    # Output file
    output_dir = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/training_data"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "ner_v7_attack_chain_partial.json")

    print("=" * 80)
    print("ATTACK CHAIN TRAINING DATA EXTRACTION")
    print("=" * 80)
    print(f"\nConnecting to Neo4j at {NEO4J_URI}...")

    # Extract data
    extractor = AttackChainExtractor(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        print("\nExecuting Cypher query to extract attack chains...")
        chains = extractor.extract_chains()
        print(f"✅ Extracted {len(chains)} attack chain segments")

        if not chains:
            print("❌ No attack chains found in database!")
            return

        print("\nConverting to spaCy v3 training format...")
        training_data = extractor.convert_to_spacy_format(chains)
        print(f"✅ Converted {len(training_data)} training examples")

        print(f"\nSaving to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved training data")

        print("\nCalculating statistics...")
        stats = extractor.calculate_stats(chains)

        print("\n" + "=" * 80)
        print("EXTRACTION RESULTS")
        print("=" * 80)
        print(f"Total chain segments: {stats['total_chains']}")
        print(f"Unique CWEs: {stats['unique_cwes']}")
        print(f"Unique CAPECs: {stats['unique_capecs']}")
        print(f"Unique ATT&CK techniques: {stats['unique_attacks']}")
        print(f"Diversity score: {stats['diversity_score']}")
        print(f"\nOutput file: {output_file}")
        print(f"File size: {os.path.getsize(output_file):,} bytes")

        # Show sample
        print("\n" + "=" * 80)
        print("SAMPLE TRAINING EXAMPLE")
        print("=" * 80)
        sample = training_data[0]
        print(f"Text: {sample['text'][:200]}...")
        print(f"\nEntities: {sample['entities']}")

        print("\n✅ EXTRACTION COMPLETE")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        extractor.close()
        print("\nNeo4j connection closed.")


if __name__ == "__main__":
    main()
