#!/usr/bin/env python3
"""
TEST SCRIPT: Process exactly 5 documents to verify fixes
Tests spaCy loading and single-worker processing
"""
import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# Add NLP pipeline to path
sys.path.insert(0, '/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney')

try:
    from nlp_ingestion_pipeline import NLPIngestionPipeline
except ImportError as e:
    print(f"ERROR: Failed to import NLP pipeline: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_5_documents():
    """Test processing on exactly 5 documents"""
    import hashlib

    print("=" * 80)
    print("TEST: Processing 5 Documents")
    print("=" * 80)

    # Initialize processor first to query already-processed documents
    print("\n🔧 Initializing NLP pipeline (single worker, error handling enabled)...")

    try:
        processor = NLPIngestionPipeline(
            neo4j_uri="bolt://localhost:7687",
            neo4j_user="neo4j",
            neo4j_password="neo4j@openspg"
        )
        print("✓ Pipeline initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize pipeline: {e}")
        return False

    # Get SHA256 hashes of already-processed documents
    print("\n📊 Querying already-processed documents...")
    processed_hashes = set()
    try:
        with processor.neo4j_inserter.driver.session() as session:
            result = session.run("MATCH (m:Metadata) RETURN m.sha256 as hash")
            processed_hashes = {record['hash'] for record in result}
        print(f"✓ Found {len(processed_hashes)} already-processed documents")
    except Exception as e:
        print(f"⚠️  Could not query processed documents: {e}")

    # Find 5 unprocessed documents
    root_dir = Path('/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j')
    supported_extensions = {'.md', '.txt'}

    print("\n📂 Finding 5 unprocessed test documents...")
    test_files = []
    checked_count = 0

    for file_path in root_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            checked_count += 1

            # Calculate SHA256 to check if already processed
            try:
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()

                if file_hash not in processed_hashes:
                    test_files.append(file_path)
                    if len(test_files) >= 5:
                        break
            except Exception as e:
                print(f"⚠️  Could not read {file_path.name}: {e}")

    print(f"✓ Checked {checked_count} files, found {len(test_files)} unprocessed documents:")
    for i, f in enumerate(test_files, 1):
        print(f"  {i}. {f.name}")

    if len(test_files) < 5:
        print(f"⚠️  Only found {len(test_files)} unprocessed files")

    # Process each document
    print(f"\n📝 Processing {len(test_files)} documents...")
    print("-" * 80)

    results = {
        'successful': 0,
        'duplicates': 0,
        'failed': 0,
        'errors': []
    }

    start_time = datetime.now()

    for i, file_path in enumerate(test_files, 1):
        print(f"\n[{i}/{len(test_files)}] Processing: {file_path.name}")

        try:
            result = processor.process_document(str(file_path))

            if result.get('status') == 'success':
                results['successful'] += 1
                entities = result.get('entities', 0)
                relationships = result.get('relationships', 0)
                print(f"  ✅ SUCCESS - Entities: {entities}, Relationships: {relationships}")

            elif result.get('status') == 'duplicate':
                results['duplicates'] += 1
                print(f"  ⊗ DUPLICATE - Already processed")

            else:
                results['failed'] += 1
                error_msg = result.get('error', 'Unknown error')
                results['errors'].append(f"{file_path.name}: {error_msg}")
                print(f"  ❌ FAILED - {error_msg}")

        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f"{file_path.name}: {str(e)}")
            print(f"  ❌ EXCEPTION - {e}")

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Cleanup
    processor.close()

    # Print results
    print("\n" + "=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    print(f"Total Processed: {len(test_files)}")
    print(f"✅ Successful: {results['successful']}")
    print(f"⊗  Duplicates: {results['duplicates']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"⏱️  Duration: {duration:.1f} seconds")
    print(f"📊 Rate: {len(test_files)/duration:.2f} docs/second")

    if results['errors']:
        print(f"\n❌ Errors ({len(results['errors'])}):")
        for error in results['errors'][:5]:
            print(f"  - {error}")

    # Success criteria
    success_rate = results['successful'] / len(test_files)

    print("\n" + "=" * 80)
    if success_rate >= 0.8:
        print("✅ TEST PASSED - Ready for full processing")
        print(f"   Success rate: {success_rate*100:.1f}%")
        return True
    else:
        print("⚠️  TEST NEEDS REVIEW")
        print(f"   Success rate: {success_rate*100:.1f}% (target: 80%+)")
        return False


if __name__ == '__main__':
    success = test_5_documents()
    sys.exit(0 if success else 1)
