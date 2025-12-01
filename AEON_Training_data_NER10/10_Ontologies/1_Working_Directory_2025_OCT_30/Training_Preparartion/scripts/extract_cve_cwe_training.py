#!/usr/bin/env python3
"""
Extract CVE→CWE training examples from Neo4j database.
Converts to spaCy v3 training format for NER.
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Any
from neo4j import GraphDatabase

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# Output file
OUTPUT_FILE = "training_data/ner_v7_cve_cwe_partial.json"

# Cypher query to extract CVE→CWE relationships
CYPHER_QUERY = """
MATCH (cve:CVE)-[r:IS_WEAKNESS_TYPE]->(cwe:CWE)
WHERE cve.description IS NOT NULL AND cwe.id IS NOT NULL
RETURN
  cve.id as cve_id,
  cve.description as cve_description,
  cve.publishedDate as published_date,
  cwe.id as cwe_id,
  cwe.name as cwe_name,
  cwe.description as cwe_description
LIMIT 430
"""


def connect_neo4j():
    """Connect to Neo4j database."""
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        # Test connection
        with driver.session() as session:
            session.run("RETURN 1")
        print(f"✅ Connected to Neo4j at {NEO4J_URI}")
        return driver
    except Exception as e:
        print(f"❌ Failed to connect to Neo4j: {e}")
        raise


def extract_data(driver) -> List[Dict[str, Any]]:
    """Extract CVE→CWE data from Neo4j."""
    print(f"\n🔍 Executing Cypher query...")

    with driver.session() as session:
        result = session.run(CYPHER_QUERY)
        records = [record.data() for record in result]

    print(f"✅ Extracted {len(records)} CVE→CWE relationships")
    return records


def find_entity_positions(text: str, entity: str) -> List[tuple]:
    """Find all positions of an entity in text (case-insensitive)."""
    positions = []
    pattern = re.compile(re.escape(entity), re.IGNORECASE)

    for match in pattern.finditer(text):
        positions.append((match.start(), match.end()))

    return positions


def create_spacy_example(record: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a Neo4j record to spaCy v3 training format."""
    cve_id = record['cve_id']
    cve_desc = record['cve_description']
    cwe_id = record['cwe_id']
    cwe_name = record['cwe_name'] or ""

    # Create training text: "CVE-ID: description"
    text = f"{cve_id}: {cve_desc}"

    entities = []

    # Find CVE ID position
    cve_positions = find_entity_positions(text, cve_id)
    for start, end in cve_positions:
        entities.append({
            "start": start,
            "end": end,
            "label": "CVE"
        })

    # Find CWE ID positions in description
    cwe_positions = find_entity_positions(text, cwe_id)
    for start, end in cwe_positions:
        entities.append({
            "start": start,
            "end": end,
            "label": "CWE"
        })

    # Find CWE name positions if it appears in description
    if cwe_name:
        cwe_name_positions = find_entity_positions(text, cwe_name)
        for start, end in cwe_name_positions:
            # Only add if not overlapping with CWE ID
            if not any(e['start'] <= start < e['end'] or e['start'] < end <= e['end']
                      for e in entities):
                entities.append({
                    "start": start,
                    "end": end,
                    "label": "CWE"
                })

    # Sort entities by start position
    entities.sort(key=lambda e: e['start'])

    return {
        "text": text,
        "entities": entities,
        "meta": {
            "cve_id": cve_id,
            "cwe_id": cwe_id,
            "cwe_name": cwe_name,
            "published_date": record['published_date']
        }
    }


def calculate_statistics(examples: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate statistics about the training data."""
    unique_cves = set()
    unique_cwes = set()
    total_entities = 0
    entity_counts = {"CVE": 0, "CWE": 0}

    for example in examples:
        meta = example.get('meta', {})
        if meta.get('cve_id'):
            unique_cves.add(meta['cve_id'])
        if meta.get('cwe_id'):
            unique_cwes.add(meta['cwe_id'])

        for entity in example.get('entities', []):
            total_entities += 1
            label = entity.get('label')
            if label in entity_counts:
                entity_counts[label] += 1

    # Calculate diversity score (ratio of unique CWEs to total examples)
    diversity_score = len(unique_cwes) / len(examples) if examples else 0

    return {
        "total_examples": len(examples),
        "unique_cves": len(unique_cves),
        "unique_cwes": len(unique_cwes),
        "total_entities": total_entities,
        "entity_counts": entity_counts,
        "diversity_score": round(diversity_score, 3),
        "avg_entities_per_example": round(total_entities / len(examples), 2) if examples else 0
    }


def save_training_data(examples: List[Dict[str, Any]], output_file: str):
    """Save training data to JSON file."""
    print(f"\n💾 Saving training data to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(examples)} examples to {output_file}")


def main():
    """Main execution function."""
    print("=" * 70)
    print("CVE→CWE Training Data Extraction")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Connect to Neo4j
    driver = connect_neo4j()

    try:
        # Extract data
        records = extract_data(driver)

        if not records:
            print("⚠️  No records found!")
            return

        # Convert to spaCy format
        print(f"\n🔄 Converting to spaCy v3 format...")
        examples = [create_spacy_example(record) for record in records]

        # Calculate statistics
        stats = calculate_statistics(examples)

        # Save training data
        save_training_data(examples, OUTPUT_FILE)

        # Print statistics
        print("\n" + "=" * 70)
        print("STATISTICS")
        print("=" * 70)
        print(f"Total Examples: {stats['total_examples']}")
        print(f"Unique CVEs: {stats['unique_cves']}")
        print(f"Unique CWEs: {stats['unique_cwes']}")
        print(f"Total Entities: {stats['total_entities']}")
        print(f"  - CVE entities: {stats['entity_counts']['CVE']}")
        print(f"  - CWE entities: {stats['entity_counts']['CWE']}")
        print(f"Diversity Score: {stats['diversity_score']}")
        print(f"Avg Entities/Example: {stats['avg_entities_per_example']}")
        print("=" * 70)

        # Show sample examples
        print("\n📝 SAMPLE EXAMPLES (first 3):")
        print("=" * 70)
        for i, example in enumerate(examples[:3], 1):
            print(f"\nExample {i}:")
            print(f"Text: {example['text'][:100]}...")
            print(f"Entities: {len(example['entities'])} entities")
            for entity in example['entities']:
                text_span = example['text'][entity['start']:entity['end']]
                print(f"  - {entity['label']}: '{text_span}' ({entity['start']}-{entity['end']})")
        print("=" * 70)

        print(f"\n✅ COMPLETE - Data extraction finished successfully")
        print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    finally:
        driver.close()
        print(f"\n🔌 Disconnected from Neo4j")


if __name__ == "__main__":
    main()
