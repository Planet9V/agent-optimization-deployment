#!/usr/bin/env python3
"""
TEST SCRIPT: Process 5 NEW non-cybersecurity documents
Tests spaCy loading and entity extraction on fresh documents
"""
import sys
import logging
from datetime import datetime
from pathlib import Path

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

def test_new_documents():
    """Test processing on 5 specific NEW documents"""

    print("=" * 80)
    print("TEST: Processing 5 NEW Documents (Non-Cybersecurity)")
    print("=" * 80)

    # Specific test files (non-CVE/CWE/CAPEC/MITRE)
    test_files = [
        "/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/Sector - Hydrogen/Sector Hydrogen Fueling Stations 6c7a67db78e9445eb5bee45e29b6b8f0.md",
        "/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/Sector - Hydrogen/Sector Hydrogen Ent Arch Proposla b0e084a14426440892d572e85a068da0.md",
        "/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/Sector - Hydrogen/Sector Hydrogen Architecture ad5010a2d4be4a799a3ecbfe95eb817f.md",
        "/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/3_Dev_Apps_PRDs/AEON Agent Red/KB 15 - Optimizing Multi-Repository Security Assessment Pipelines.md",
        "/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/3_Dev_Apps_PRDs/AEON Agent Red/KB 2 - Security Finding Normalization Framework.md",
    ]

    print(f"\n📂 Test documents:")
    for i, f in enumerate(test_files, 1):
        fname = Path(f).name
        print(f"  {i}. {fname}")

    # Initialize processor
    print("\n🔧 Initializing NLP pipeline (single worker, error handling enabled)...")

    try:
        processor = NLPIngestionPipeline(
            neo4j_uri="bolt://localhost:7687",
            neo4j_user="neo4j",
            neo4j_password="neo4j@openspg"
        )
        print("✓ Pipeline initialized successfully")
        print("✓ spaCy model loaded without errors")
    except Exception as e:
        print(f"❌ Failed to initialize pipeline: {e}")
        return False

    # Process each document
    print(f"\n📝 Processing {len(test_files)} documents...")
    print("-" * 80)

    results = {
        'successful': 0,
        'duplicates': 0,
        'failed': 0,
        'errors': [],
        'entity_counts': [],
        'relationship_counts': []
    }

    start_time = datetime.now()

    for i, file_path in enumerate(test_files, 1):
        fname = Path(file_path).name
        print(f"\n[{i}/{len(test_files)}] Processing: {fname}")

        try:
            result = processor.process_document(file_path)

            if result.get('status') == 'success':
                results['successful'] += 1
                entities = result.get('entities', 0)
                relationships = result.get('relationships', 0)
                results['entity_counts'].append(entities)
                results['relationship_counts'].append(relationships)
                print(f"  ✅ SUCCESS - Entities: {entities}, Relationships: {relationships}")

            elif result.get('status') == 'duplicate':
                results['duplicates'] += 1
                print(f"  ⊗ DUPLICATE - Already processed")

            else:
                results['failed'] += 1
                error_msg = result.get('error', 'Unknown error')
                results['errors'].append(f"{fname}: {error_msg}")
                print(f"  ❌ FAILED - {error_msg}")

        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f"{fname}: {str(e)}")
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

    if results['successful'] > 0:
        print(f"\n📈 Entity Extraction:")
        print(f"   Total entities extracted: {sum(results['entity_counts'])}")
        print(f"   Avg entities per doc: {sum(results['entity_counts'])/results['successful']:.1f}")
        print(f"   Total relationships: {sum(results['relationship_counts'])}")
        print(f"   Avg relationships per doc: {sum(results['relationship_counts'])/results['successful']:.1f}")

    if results['errors']:
        print(f"\n❌ Errors ({len(results['errors'])}):")
        for error in results['errors'][:5]:
            print(f"  - {error}")

    # Success criteria
    success_rate = results['successful'] / len(test_files)
    has_entities = sum(results['entity_counts']) > 0 if results['successful'] > 0 else False

    print("\n" + "=" * 80)
    if success_rate >= 0.8 and has_entities:
        print("✅ TEST PASSED - spaCy loading works, entities extracted")
        print(f"   Success rate: {success_rate*100:.1f}%")
        print(f"   Total entities extracted: {sum(results['entity_counts'])}")
        print("\n🚀 READY TO PROCESS ALL 1,289 DOCUMENTS")
        return True
    elif success_rate >= 0.8:
        print("⚠️  TEST NEEDS REVIEW - Documents processed but no entities")
        print(f"   Success rate: {success_rate*100:.1f}%")
        return False
    else:
        print("❌ TEST FAILED")
        print(f"   Success rate: {success_rate*100:.1f}% (target: 80%+)")
        return False


if __name__ == '__main__':
    success = test_new_documents()
    sys.exit(0 if success else 1)
