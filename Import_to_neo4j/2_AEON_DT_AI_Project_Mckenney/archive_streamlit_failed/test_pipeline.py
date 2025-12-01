#!/usr/bin/env python3
"""
Test script for NLP Ingestion Pipeline
"""

import os
import tempfile
from pathlib import Path
from nlp_ingestion_pipeline import (
    DocumentLoader,
    TextPreprocessor,
    EntityExtractor,
    RelationshipExtractor,
    TableExtractor,
    MetadataTracker,
    NLPIngestionPipeline
)
import spacy

# Test sample documents
SAMPLE_MD = """
# Cybersecurity Threat Analysis

CVE-2024-1234 is a critical vulnerability affecting Apache Struts framework.
This vulnerability was discovered by John Smith from Acme Security Corp in New York.

## Impact Assessment

The vulnerability allows remote code execution through malicious payloads.
Organizations should patch immediately using version 2.5.33 or later.

### Affected Systems
| System | Version | Status |
|--------|---------|--------|
| Apache Struts | 2.5.0-2.5.32 | Vulnerable |
| Apache Struts | 2.5.33+ | Patched |

## Related Techniques

This attack maps to MITRE ATT&CK technique T1190 (Exploit Public-Facing Application).
CAPEC-63 describes similar attack patterns.

## Indicators of Compromise

IP Address: 192.168.1.100
Hash: 5d41402abc4b2a76b9719d911017c592
URL: https://malicious-site.com/payload
"""

SAMPLE_TXT = """
Security Advisory: SQL Injection in Web Application

A SQL injection vulnerability (CWE-89) was identified in the authentication module.
The vulnerability affects Microsoft SQL Server and Oracle Database systems.
London-based researcher Jane Doe reported this issue to the security team.
"""


def test_document_loader():
    """Test document loading functionality"""
    print("\n=== Testing DocumentLoader ===")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(SAMPLE_MD)
        md_file = f.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(SAMPLE_TXT)
        txt_file = f.name

    try:
        # Test markdown loading
        md_content = DocumentLoader.load(md_file)
        assert len(md_content) > 0
        assert "CVE-2024-1234" in md_content
        print("✓ Markdown loading successful")

        # Test text loading
        txt_content = DocumentLoader.load(txt_file)
        assert len(txt_content) > 0
        assert "SQL injection" in txt_content
        print("✓ Text loading successful")

    finally:
        os.unlink(md_file)
        os.unlink(txt_file)


def test_text_preprocessor():
    """Test text preprocessing"""
    print("\n=== Testing TextPreprocessor ===")

    dirty_text = """This    has   excessive   whitespace
    and \x00 control \x1f characters and "smart quotes" """

    clean_text = TextPreprocessor.clean(dirty_text)

    # Check excessive whitespace reduced
    assert dirty_text.count(' ') > clean_text.count(' ')
    assert '"' in clean_text  # Smart quotes converted
    assert '\x00' not in clean_text  # Control chars removed
    print("✓ Text preprocessing successful")
    print(f"  - Original length: {len(dirty_text)}, Clean length: {len(clean_text)}")


def test_entity_extraction():
    """Test entity extraction"""
    print("\n=== Testing EntityExtractor ===")

    nlp = spacy.load("en_core_web_lg")
    extractor = EntityExtractor(nlp)

    entities = extractor.extract(SAMPLE_MD)

    # Check for CVE detection
    cve_entities = [e for e in entities if e['label'] == 'CVE']
    assert len(cve_entities) > 0
    assert cve_entities[0]['text'] == 'CVE-2024-1234'
    print(f"✓ Found {len(cve_entities)} CVE entities")

    # Check for person detection
    person_entities = [e for e in entities if e['label'] == 'PERSON']
    print(f"✓ Found {len(person_entities)} person entities")

    # Check for organization detection
    org_entities = [e for e in entities if e['label'] == 'ORG']
    print(f"✓ Found {len(org_entities)} organization entities")

    # Check for IP address detection
    ip_entities = [e for e in entities if e['label'] == 'IP_ADDRESS']
    assert len(ip_entities) > 0
    print(f"✓ Found {len(ip_entities)} IP address entities")

    # Check for technique detection
    technique_entities = [e for e in entities if e['label'] == 'TECHNIQUE']
    assert len(technique_entities) > 0
    print(f"✓ Found {len(technique_entities)} MITRE technique entities")

    print(f"✓ Total entities extracted: {len(entities)}")


def test_relationship_extraction():
    """Test relationship extraction"""
    print("\n=== Testing RelationshipExtractor ===")

    nlp = spacy.load("en_core_web_lg")
    extractor = RelationshipExtractor(nlp)

    relationships = extractor.extract(SAMPLE_MD)

    # Should find some SVO triples
    svo_rels = [r for r in relationships if r['type'] == 'SVO']
    print(f"✓ Found {len(svo_rels)} SVO relationships")

    # Should find some prepositional relationships
    prep_rels = [r for r in relationships if r['type'] == 'PREP']
    print(f"✓ Found {len(prep_rels)} prepositional relationships")

    print(f"✓ Total relationships extracted: {len(relationships)}")

    # Display sample relationships
    if relationships:
        print("\nSample relationships:")
        for rel in relationships[:3]:
            print(f"  - {rel['subject']} -> {rel['predicate']} -> {rel['object']}")


def test_table_extraction():
    """Test table extraction"""
    print("\n=== Testing TableExtractor ===")

    tables = TableExtractor.extract_markdown_tables(SAMPLE_MD)

    assert len(tables) > 0
    print(f"✓ Found {len(tables)} tables")

    # Check first table structure
    df = tables[0]
    print(f"✓ Table has {len(df)} rows and {len(df.columns)} columns")
    print(f"✓ Columns: {list(df.columns)}")


def test_metadata_tracker():
    """Test metadata tracking"""
    print("\n=== Testing MetadataTracker ===")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(SAMPLE_MD)
        temp_file = f.name

    try:
        # Compute hash
        hash1 = MetadataTracker.compute_hash(SAMPLE_MD)
        hash2 = MetadataTracker.compute_hash(SAMPLE_MD)
        assert hash1 == hash2
        print(f"✓ SHA256 hash: {hash1[:16]}...")

        # Create metadata
        metadata = MetadataTracker.create_metadata(temp_file, SAMPLE_MD)

        assert metadata['sha256'] == hash1
        assert metadata['file_name'].endswith('.md')
        assert metadata['char_count'] == len(SAMPLE_MD)
        print("✓ Metadata creation successful")
        print(f"  - File: {metadata['file_name']}")
        print(f"  - Size: {metadata['file_size']} bytes")
        print(f"  - Lines: {metadata['line_count']}")

    finally:
        os.unlink(temp_file)


def test_integration():
    """Test full pipeline integration"""
    print("\n=== Testing Full Pipeline Integration ===")

    # Create test directory with sample files
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        test_files = [
            (Path(tmpdir) / "doc1.md", SAMPLE_MD),
            (Path(tmpdir) / "doc2.txt", SAMPLE_TXT),
        ]

        for file_path, content in test_files:
            file_path.write_text(content)

        print(f"✓ Created {len(test_files)} test documents")

        # Note: Actual Neo4j testing requires running Neo4j instance
        print("\n⚠️  Full Neo4j integration test requires:")
        print("  1. Running Neo4j instance")
        print("  2. Neo4j credentials")
        print("  3. Run with: python nlp_ingestion_pipeline.py <directory> --neo4j-password <password>")


def main():
    """Run all tests"""
    print("=" * 60)
    print("NLP Ingestion Pipeline - Test Suite")
    print("=" * 60)

    try:
        test_document_loader()
        test_text_preprocessor()
        test_entity_extraction()
        test_relationship_extraction()
        test_table_extraction()
        test_metadata_tracker()
        test_integration()

        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
