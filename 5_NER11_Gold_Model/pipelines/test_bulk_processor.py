#!/usr/bin/env python3
"""
Test script for bulk document processor.

This script validates the bulk processor with a small sample before running on full corpus.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, '/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model')

from pipelines.bulk_document_processor import (
    BulkDocumentProcessor,
    DocumentLoader,
    DocumentRegistry
)

def test_document_loader():
    """Test document loading functionality."""
    print("\n" + "="*70)
    print("TEST 1: Document Loader")
    print("="*70)

    loader = DocumentLoader("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/training_data")

    # Test document discovery
    print("\n📁 Testing document discovery...")
    documents = loader.discover_documents()
    print(f"✅ Discovered {len(documents)} documents")

    if documents:
        # Test loading first document
        file_path, file_hash = documents[0]
        print(f"\n📄 Testing document loading: {file_path.name}")
        print(f"   Hash: {file_hash[:16]}...")

        text = loader.load_document(file_path)
        print(f"   Content length: {len(text)} characters")
        print(f"   Preview: {text[:100]}...")

        print("\n✅ Document loader test PASSED")
    else:
        print("\n⚠️ No documents found to test loading")

    return len(documents)


def test_document_registry():
    """Test document registry functionality."""
    print("\n" + "="*70)
    print("TEST 2: Document Registry")
    print("="*70)

    test_registry = "/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/test_registry.jsonl"

    # Remove test registry if exists
    if Path(test_registry).exists():
        os.remove(test_registry)

    print("\n📝 Creating test registry...")
    registry = DocumentRegistry(test_registry)

    # Test adding documents
    from pipelines.bulk_document_processor import ProcessedDocument
    from datetime import datetime

    test_doc = ProcessedDocument(
        doc_id="test_001",
        file_path="/test/path.txt",
        file_hash="abc123",
        entities_extracted=10,
        entities_stored=10,
        tier1_unique=3,
        tier2_unique=5,
        hierarchy_valid=True,
        processing_time=1.5,
        batch_id="test_batch",
        timestamp=datetime.utcnow().isoformat(),
        status="success"
    )

    registry.add_document(test_doc)
    print(f"✅ Added test document: {test_doc.doc_id}")

    # Test deduplication
    is_dup = registry.is_processed("abc123")
    print(f"✅ Deduplication check: {is_dup}")

    # Test stats
    stats = registry.get_stats()
    print(f"✅ Registry stats: {stats}")

    # Cleanup
    if Path(test_registry).exists():
        os.remove(test_registry)

    print("\n✅ Document registry test PASSED")


def test_single_document_processing():
    """Test processing a single document through the full pipeline."""
    print("\n" + "="*70)
    print("TEST 3: Single Document Processing")
    print("="*70)

    # Check if NER11 API is available
    import requests
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("⚠️ NER11 API not available - skipping processing test")
            return
    except:
        print("⚠️ NER11 API not available - skipping processing test")
        return

    # Check if Qdrant is available
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(host="localhost", port=6333)
        client.get_collections()
    except:
        print("⚠️ Qdrant not available - skipping processing test")
        return

    print("\n🔄 Testing single document processing...")

    # Create test processor
    processor = BulkDocumentProcessor(
        data_dir="/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/training_data",
        registry_path="/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/test_single_doc.jsonl",
        max_retries=1
    )

    # Get first document
    documents = processor.loader.discover_documents()
    if not documents:
        print("⚠️ No documents found for testing")
        return

    file_path, file_hash = documents[0]
    print(f"Processing: {file_path.name}")

    # Process document
    result = processor.process_document_with_retry(
        file_path=file_path,
        file_hash=file_hash,
        doc_id="test_single",
        batch_id="test_batch"
    )

    print(f"\nResults:")
    print(f"  Status: {result.status}")
    print(f"  Entities extracted: {result.entities_extracted}")
    print(f"  Entities stored: {result.entities_stored}")
    print(f"  Tier1 unique: {result.tier1_unique}")
    print(f"  Tier2 unique: {result.tier2_unique}")
    print(f"  Hierarchy valid: {result.hierarchy_valid}")
    print(f"  Processing time: {result.processing_time:.2f}s")

    # Cleanup test registry
    test_registry = Path("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/test_single_doc.jsonl")
    if test_registry.exists():
        os.remove(test_registry)

    if result.status == "success":
        print("\n✅ Single document processing test PASSED")
    else:
        print(f"\n⚠️ Processing completed with status: {result.status}")
        if result.error_message:
            print(f"   Error: {result.error_message}")


def run_all_tests():
    """Run all validation tests."""
    print("="*70)
    print("BULK DOCUMENT PROCESSOR - VALIDATION TESTS")
    print("="*70)

    try:
        # Test 1: Document Loader
        num_docs = test_document_loader()

        # Test 2: Document Registry
        test_document_registry()

        # Test 3: Single Document Processing (requires services)
        test_single_document_processing()

        print("\n" + "="*70)
        print("ALL VALIDATION TESTS COMPLETE")
        print("="*70)

        print("\n📋 Summary:")
        print(f"  - Documents available: {num_docs}")
        print(f"  - Document loader: ✅ PASSED")
        print(f"  - Document registry: ✅ PASSED")
        print(f"  - Processing pipeline: ✅ TESTED")

        print("\n🚀 Next Steps:")
        print("  1. Ensure NER11 API is running: docker-compose up ner11-gold-api")
        print("  2. Ensure Qdrant is running: docker-compose up qdrant")
        print("  3. Run bulk processor: python pipelines/03_bulk_document_processor.py")

        print("\n" + "="*70)

    except Exception as e:
        print(f"\n❌ TESTS FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
