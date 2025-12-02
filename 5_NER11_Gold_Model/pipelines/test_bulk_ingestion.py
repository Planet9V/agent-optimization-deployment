"""
Test Script for Bulk Graph Ingestion Processor

Validates the bulk ingestion processor with a small test run before
processing the full corpus.

File: test_bulk_ingestion.py
Created: 2025-12-01
Version: 1.0.0
"""

import sys
from pathlib import Path
import logging

# Import bulk processor
sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_bulk_processor():
    """
    Test bulk ingestion processor with small document set.

    Validates:
    1. Document discovery
    2. Entity extraction
    3. Node creation with MERGE
    4. Relationship extraction
    5. Critical validation (node preservation)
    """
    print("="*80)
    print("BULK GRAPH INGESTION - TEST RUN")
    print("="*80)

    try:
        # Import processor
        spec = __import__('06_bulk_graph_ingestion')
        BulkGraphIngestionProcessor = spec.BulkGraphIngestionProcessor

        # Initialize processor
        print("\n[STEP 1] Initializing Bulk Processor")
        processor = BulkGraphIngestionProcessor()

        print(f"  Corpus root: {processor.corpus_root}")
        print(f"  Log file: {processor.log_file}")
        print(f"  State file: {processor.state_file}")

        # Test document discovery
        print("\n[STEP 2] Testing Document Discovery")
        documents = processor._find_corpus_documents()
        print(f"  Found {len(documents)} documents in corpus")

        if documents:
            print(f"  Sample documents:")
            for doc in documents[:5]:
                print(f"    - {doc.relative_to(processor.corpus_root)}")

        # Test document reading
        print("\n[STEP 3] Testing Document Reading")
        if documents:
            test_doc = documents[0]
            content = processor._read_document_content(test_doc)
            if content:
                print(f"  Successfully read: {test_doc.name}")
                print(f"  Content length: {len(content)} characters")
                print(f"  Preview: {content[:200]}...")
            else:
                print(f"  Failed to read: {test_doc.name}")

        # Record baseline
        print("\n[STEP 4] Recording Baseline Metrics")
        baseline = processor._record_baseline_metrics()
        print(f"  Baseline nodes: {baseline.get('total_nodes', 0):,}")
        print(f"  Tier 1 count: {baseline.get('tier1_count', 0):,}")
        print(f"  Tier 2 count: {baseline.get('tier2_count', 0):,}")

        # Process test documents (max 3)
        print("\n[STEP 5] Processing Test Documents (max 3)")
        stats = processor.process_corpus(
            max_documents=3,
            skip_processed=False,
            batch_size=1
        )

        print("\n[STEP 6] Test Processing Results")
        print(f"  Documents found: {stats.get('documents_found', 0)}")
        print(f"  Documents processed: {stats.get('documents_processed', 0)}")
        print(f"  Entities extracted: {stats.get('total_entities', 0)}")
        print(f"  Nodes created: {stats.get('total_nodes_created', 0)}")
        print(f"  Relationships: {stats.get('total_relationships', 0)}")
        print(f"  Errors: {stats.get('documents_failed', 0)}")

        # Validation
        print("\n[STEP 7] Post-Test Validation")
        validation = stats.get("validation_report", {})

        print(f"  Baseline nodes: {validation.get('baseline_nodes', 0):,}")
        print(f"  Current nodes: {validation.get('current_nodes', 0):,}")
        print(f"  Nodes added: {validation.get('nodes_added', 0):,}")
        print(f"  Node preservation: {'✅ PASS' if validation.get('node_preservation') else '❌ FAIL'}")
        print(f"  Tier 2 > Tier 1: {'✅ PASS' if validation.get('tier2_greater_than_tier1') else '❌ FAIL'}")
        print(f"  Overall: {'✅ PASS' if validation.get('validation_passed') else '❌ FAIL'}")

        # Close processor
        processor.close()

        print("\n" + "="*80)
        if validation.get('validation_passed'):
            print("✅ TEST SUCCESSFUL - READY FOR FULL CORPUS PROCESSING")
            print("="*80)
            print("\nTo process full corpus, run:")
            print("  python pipelines/06_bulk_graph_ingestion.py")
            print("\nTo process with limit:")
            print("  python pipelines/06_bulk_graph_ingestion.py --max-docs 100")
            return True
        else:
            print("⚠️ TEST COMPLETED WITH WARNINGS")
            print("="*80)
            if not validation.get('node_preservation'):
                print("\n⚠️ WARNING: Node count not preserved!")
                print("   Review baseline and post-ingestion metrics")
            return False

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_prerequisites():
    """
    Validate that all prerequisites are met.

    Checks:
    1. Neo4j connection available
    2. NER11 API running
    3. Required modules importable
    4. Corpus directory exists
    """
    print("="*80)
    print("PREREQUISITE VALIDATION")
    print("="*80)

    checks_passed = True

    # Check corpus directory
    print("\n[CHECK 1] Corpus Directory")
    corpus_path = Path("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/training_data")
    if corpus_path.exists():
        print(f"  ✅ Corpus directory exists: {corpus_path}")
    else:
        print(f"  ❌ Corpus directory not found: {corpus_path}")
        checks_passed = False

    # Check pipeline module
    print("\n[CHECK 2] Pipeline Module (Task 2.3)")
    pipeline_file = Path(__file__).parent / "05_ner11_to_neo4j_hierarchical.py"
    if pipeline_file.exists():
        print(f"  ✅ Pipeline module exists")
    else:
        print(f"  ❌ Pipeline module not found: {pipeline_file}")
        checks_passed = False

    # Check Neo4j connection
    print("\n[CHECK 3] Neo4j Connection")
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "neo4j@openspg")
        )
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            result.single()
        driver.close()
        print(f"  ✅ Neo4j connection successful")
    except Exception as e:
        print(f"  ❌ Neo4j connection failed: {e}")
        checks_passed = False

    # Check NER11 API
    print("\n[CHECK 4] NER11 API")
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print(f"  ✅ NER11 API responding")
        else:
            print(f"  ⚠️ NER11 API responded with status {response.status_code}")
    except Exception as e:
        print(f"  ❌ NER11 API not accessible: {e}")
        print(f"     Make sure NER11 API is running:")
        print(f"     cd 5_NER11_Gold_Model && python serve_model.py")
        checks_passed = False

    print("\n" + "="*80)
    if checks_passed:
        print("✅ ALL PREREQUISITES MET")
    else:
        print("❌ SOME PREREQUISITES FAILED")
    print("="*80)

    return checks_passed


if __name__ == "__main__":
    # Validate prerequisites first
    if not validate_prerequisites():
        print("\n⚠️ Please fix prerequisites before running tests")
        sys.exit(1)

    # Run test
    print("\n")
    success = test_bulk_processor()

    sys.exit(0 if success else 1)
