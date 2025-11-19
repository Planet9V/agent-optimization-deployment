#!/usr/bin/env python3
"""
Demo script showing NLP pipeline capabilities without requiring Neo4j
"""

import spacy
from nlp_ingestion_pipeline import (
    DocumentLoader,
    TextPreprocessor,
    EntityExtractor,
    RelationshipExtractor,
    TableExtractor,
    MetadataTracker
)

# Sample document with cybersecurity content
SAMPLE_DOCUMENT = """
# Critical Vulnerability Alert: CVE-2024-5678

## Executive Summary

A critical remote code execution vulnerability (CVE-2024-5678) has been discovered
in Apache Log4j version 2.14.0 through 2.16.0. This vulnerability was reported by
Dr. Sarah Chen from Google Security Research Team in Mountain View, California.

## Technical Details

The vulnerability allows attackers to execute arbitrary code through JNDI lookup
substitution when message lookup substitution is enabled. This attack maps to
MITRE ATT&CK technique T1190 (Exploit Public-Facing Application) and is related
to CAPEC-248 (Command Injection).

Organizations using affected versions must upgrade immediately to version 2.17.0 or later.

## Affected Systems

| Software | Vulnerable Versions | Patched Version |
|----------|-------------------|-----------------|
| Apache Log4j | 2.14.0 - 2.16.0 | 2.17.0+ |
| Spring Boot | 2.5.x - 2.6.0 | 2.6.1+ |
| Elasticsearch | 7.0 - 7.16 | 7.16.3+ |

## Indicators of Compromise

The following IOCs have been observed:

- IP Address: 203.0.113.42
- Malicious Domain: evil-server.example.com
- URL: https://malicious-site.example/payload
- File Hash: 5d41402abc4b2a76b9719d911017c592ed3d5de3

## Mitigation Steps

Microsoft Azure and Amazon Web Services have released patches. Google Cloud Platform
deployed fixes automatically. Cisco Systems and IBM Security recommend immediate patching.

The vulnerability affects approximately 35% of global enterprise systems, making it one
of the most severe vulnerabilities since Heartbleed (CVE-2014-0160).

## References

- Common Weakness Enumeration: CWE-502 (Deserialization of Untrusted Data)
- NIST NVD Score: 10.0 (Critical)
- Related: CVE-2021-44228, CVE-2021-45046
"""


def demo_document_loading():
    """Demo document loading and preprocessing"""
    print("=" * 70)
    print("DEMO: Document Loading & Preprocessing")
    print("=" * 70)

    # Preprocess
    preprocessor = TextPreprocessor()
    clean_text = preprocessor.clean(SAMPLE_DOCUMENT)

    # Metadata
    metadata = MetadataTracker.create_metadata("demo_document.md", clean_text)

    print(f"\n📄 Document Metadata:")
    print(f"  - Characters: {metadata['char_count']:,}")
    print(f"  - Lines: {metadata['line_count']}")
    print(f"  - SHA256: {metadata['sha256'][:32]}...")
    print(f"  - Processed: {metadata['processed_at']}")


def demo_entity_extraction():
    """Demo entity extraction with spaCy"""
    print("\n" + "=" * 70)
    print("DEMO: Entity Extraction")
    print("=" * 70)

    # Load spaCy model
    nlp = spacy.load("en_core_web_lg")
    extractor = EntityExtractor(nlp)

    # Extract entities
    entities = extractor.extract(SAMPLE_DOCUMENT)

    # Group by type
    by_label = {}
    for entity in entities:
        label = entity['label']
        if label not in by_label:
            by_label[label] = []
        by_label[label].append(entity['text'])

    print(f"\n🔍 Extracted {len(entities)} entities:")
    print()

    # Show cybersecurity entities
    print("Cybersecurity Entities:")
    for label in ['CVE', 'CAPEC', 'CWE', 'TECHNIQUE', 'IP_ADDRESS', 'HASH', 'URL']:
        if label in by_label:
            print(f"  {label}:")
            unique_texts = list(set(by_label[label]))[:5]  # Convert to list first
            for text in unique_texts:
                print(f"    - {text}")

    print()
    print("Named Entities:")
    for label in ['PERSON', 'ORG', 'GPE', 'PRODUCT']:
        if label in by_label:
            print(f"  {label}:")
            unique_texts = list(set(by_label[label]))[:5]
            for text in unique_texts:
                print(f"    - {text}")

    return entities


def demo_relationship_extraction():
    """Demo relationship extraction"""
    print("\n" + "=" * 70)
    print("DEMO: Relationship Extraction")
    print("=" * 70)

    nlp = spacy.load("en_core_web_lg")
    extractor = RelationshipExtractor(nlp)

    relationships = extractor.extract(SAMPLE_DOCUMENT)

    print(f"\n🔗 Extracted {len(relationships)} relationships:")
    print()

    # Show SVO relationships
    svo = [r for r in relationships if r['type'] == 'SVO']
    print(f"Subject-Verb-Object Relationships ({len(svo)}):")
    for rel in svo[:10]:  # Show first 10
        print(f"  {rel['subject']} → {rel['predicate']} → {rel['object']}")

    # Show prepositional relationships
    prep = [r for r in relationships if r['type'] == 'PREP']
    print(f"\nPrepositional Relationships ({len(prep)}):")
    for rel in prep[:10]:
        print(f"  {rel['subject']} → {rel['predicate']} → {rel['object']}")

    return relationships


def demo_table_extraction():
    """Demo table extraction"""
    print("\n" + "=" * 70)
    print("DEMO: Table Extraction")
    print("=" * 70)

    tables = TableExtractor.extract_markdown_tables(SAMPLE_DOCUMENT)

    print(f"\n📊 Extracted {len(tables)} tables:")
    print()

    for i, df in enumerate(tables, 1):
        print(f"Table {i}: {len(df)} rows × {len(df.columns)} columns")
        print(f"Columns: {list(df.columns)}")
        print()
        print(df.to_string(index=False))
        print()


def demo_full_analysis():
    """Demo complete analysis pipeline"""
    print("\n" + "=" * 70)
    print("DEMO: Full Document Analysis")
    print("=" * 70)

    nlp = spacy.load("en_core_web_lg")

    # Extract everything
    entity_extractor = EntityExtractor(nlp)
    rel_extractor = RelationshipExtractor(nlp)

    entities = entity_extractor.extract(SAMPLE_DOCUMENT)
    relationships = rel_extractor.extract(SAMPLE_DOCUMENT)
    tables = TableExtractor.extract_markdown_tables(SAMPLE_DOCUMENT)

    print(f"\n📈 Analysis Summary:")
    print(f"  - Entities: {len(entities)}")
    print(f"  - Relationships: {len(relationships)}")
    print(f"  - Tables: {len(tables)}")

    # Show entity type distribution
    entity_types = {}
    for e in entities:
        label = e['label']
        entity_types[label] = entity_types.get(label, 0) + 1

    print(f"\n📊 Entity Distribution:")
    for label, count in sorted(entity_types.items(), key=lambda x: -x[1])[:10]:
        print(f"  {label}: {count}")

    # Show key entities
    print(f"\n🔑 Key Cybersecurity Identifiers:")
    for e in entities:
        if e['label'] in ['CVE', 'CAPEC', 'CWE', 'TECHNIQUE']:
            print(f"  {e['label']}: {e['text']}")


def main():
    """Run all demos"""
    print("\n" + "🚀" * 35)
    print("NLP INGESTION PIPELINE - DEMONSTRATION")
    print("🚀" * 35)

    try:
        demo_document_loading()
        entities = demo_entity_extraction()
        relationships = demo_relationship_extraction()
        demo_table_extraction()
        demo_full_analysis()

        print("\n" + "=" * 70)
        print("✅ DEMO COMPLETE")
        print("=" * 70)
        print("\nTo process actual documents into Neo4j:")
        print("  python nlp_ingestion_pipeline.py <directory> --neo4j-password <pwd>")
        print()

    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
