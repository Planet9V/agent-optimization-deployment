#!/usr/bin/env python3
"""
Batch inference test for v6 NER model
Tests on 20 real cybersecurity annual reports
"""
import spacy
from pathlib import Path
from collections import defaultdict, Counter
import json
from datetime import datetime
import time

def process_document(nlp, doc_path: Path):
    """Process a single document and extract entities"""
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Process with NER model
        doc = nlp(text)

        # Collect entities
        entities_by_type = defaultdict(list)
        for ent in doc.ents:
            entities_by_type[ent.label_].append(ent.text)

        return {
            'success': True,
            'file': doc_path.name,
            'char_count': len(text),
            'word_count': len(text.split()),
            'total_entities': len(doc.ents),
            'unique_types': len(entities_by_type),
            'entities_by_type': {k: len(v) for k, v in entities_by_type.items()},
            'unique_entities': {k: len(set(v)) for k, v in entities_by_type.items()},
            'sample_entities': {k: list(dict.fromkeys(v))[:3] for k, v in entities_by_type.items()}
        }
    except Exception as e:
        return {
            'success': False,
            'file': doc_path.name,
            'error': str(e)
        }

def generate_summary(results):
    """Generate summary statistics across all documents"""

    # Overall stats
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    # Entity type distribution
    entity_type_counts = Counter()
    entity_type_unique = Counter()
    for result in successful:
        for entity_type, count in result['entities_by_type'].items():
            entity_type_counts[entity_type] += count
        for entity_type, count in result['unique_entities'].items():
            entity_type_unique[entity_type] += count

    # Document stats
    total_chars = sum(r['char_count'] for r in successful)
    total_words = sum(r['word_count'] for r in successful)
    total_entities = sum(r['total_entities'] for r in successful)

    # Top entity types
    top_types = entity_type_counts.most_common(10)

    return {
        'summary': {
            'total_documents': len(results),
            'successful': len(successful),
            'failed': len(failed),
            'total_characters': total_chars,
            'total_words': total_words,
            'total_entities_extracted': total_entities,
            'avg_entities_per_doc': total_entities / len(successful) if successful else 0,
            'unique_entity_types': len(entity_type_counts)
        },
        'entity_distribution': {
            'total_by_type': dict(entity_type_counts),
            'unique_by_type': dict(entity_type_unique),
            'top_10_types': top_types
        },
        'failed_documents': [r['file'] for r in failed] if failed else []
    }

def main():
    print("=" * 100)
    print("BATCH NER INFERENCE TEST - 20 CYBERSECURITY ANNUAL REPORTS")
    print("=" * 100)

    # Configuration
    model_path = Path("ner_model")
    reports_dir = Path("/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/12_Reports - Annual Cyber Security/2025")

    # Load model
    print(f"\n📦 Loading NER model...")
    start_time = time.time()
    nlp = spacy.load(str(model_path))
    load_time = time.time() - start_time
    print(f"✅ Model loaded in {load_time:.2f}s")

    # Get first 20 markdown files
    report_files = sorted(reports_dir.glob("*.md"))[:20]
    print(f"\n📄 Found {len(report_files)} documents to process")

    if not report_files:
        print("❌ No documents found!")
        return

    # Process documents
    print(f"\n🔍 Processing documents...")
    results = []

    for i, doc_path in enumerate(report_files, 1):
        print(f"\n[{i:2d}/20] Processing: {doc_path.name}")
        start = time.time()
        result = process_document(nlp, doc_path)
        elapsed = time.time() - start

        if result['success']:
            print(f"  ✅ Extracted {result['total_entities']} entities ({result['unique_types']} types) in {elapsed:.2f}s")
            print(f"     Document: {result['word_count']:,} words, {result['char_count']:,} chars")
            # Show top 3 entity types for this document
            if result['entities_by_type']:
                top_3 = sorted(result['entities_by_type'].items(), key=lambda x: -x[1])[:3]
                print(f"     Top types: {', '.join(f'{k}({v})' for k, v in top_3)}")
        else:
            print(f"  ❌ Failed: {result['error']}")

        results.append(result)

    # Generate summary
    print("\n" + "=" * 100)
    print("📊 COMPREHENSIVE RESULTS")
    print("=" * 100)

    summary = generate_summary(results)

    # Overall statistics
    print(f"\n📈 OVERALL STATISTICS")
    print("-" * 100)
    print(f"  Documents processed:    {summary['summary']['successful']}/{summary['summary']['total_documents']}")
    print(f"  Total characters:       {summary['summary']['total_characters']:,}")
    print(f"  Total words:            {summary['summary']['total_words']:,}")
    print(f"  Total entities:         {summary['summary']['total_entities_extracted']:,}")
    print(f"  Avg entities/doc:       {summary['summary']['avg_entities_per_doc']:.1f}")
    print(f"  Unique entity types:    {summary['summary']['unique_entity_types']}")

    # Entity type distribution
    print(f"\n🏷️  TOP 10 ENTITY TYPES EXTRACTED")
    print("-" * 100)
    for entity_type, count in summary['entity_distribution']['top_10_types']:
        unique_count = summary['entity_distribution']['unique_by_type'].get(entity_type, 0)
        print(f"  {entity_type:25s} {count:5,} total ({unique_count:4,} unique)")

    # Category breakdown
    categories = {
        "Critical Infrastructure": ["VENDOR", "EQUIPMENT", "PROTOCOL", "OPERATION", "ARCHITECTURE", "SUPPLIER"],
        "Cybersecurity": ["SECURITY", "VULNERABILITY", "WEAKNESS", "MITIGATION"],
        "Threat Intelligence": ["THREAT_MODEL", "TACTIC", "TECHNIQUE", "ATTACK_PATTERN", "INDICATOR"],
        "Attribution": ["THREAT_ACTOR", "CAMPAIGN"],
        "Technical Components": ["SOFTWARE_COMPONENT", "HARDWARE_COMPONENT"],
        "Human Factors": ["PERSONALITY_TRAIT", "COGNITIVE_BIAS", "INSIDER_INDICATOR", "SOCIAL_ENGINEERING", "ATTACK_VECTOR"]
    }

    print(f"\n📂 EXTRACTION BY CATEGORY")
    print("-" * 100)

    for category, entity_types in categories.items():
        category_total = sum(summary['entity_distribution']['total_by_type'].get(et, 0) for et in entity_types)
        if category_total > 0:
            print(f"\n  {category.upper()}:")
            for entity_type in entity_types:
                count = summary['entity_distribution']['total_by_type'].get(entity_type, 0)
                unique = summary['entity_distribution']['unique_by_type'].get(entity_type, 0)
                if count > 0:
                    print(f"    {entity_type:25s} {count:5,} total ({unique:4,} unique)")

    # Sample extractions from first document
    print(f"\n📝 SAMPLE EXTRACTIONS (From: {results[0]['file']})")
    print("-" * 100)

    if results[0]['success'] and results[0]['sample_entities']:
        # Show top 5 entity types
        top_types = sorted(results[0]['entities_by_type'].items(), key=lambda x: -x[1])[:5]
        for entity_type, count in top_types:
            samples = results[0]['sample_entities'].get(entity_type, [])
            if samples:
                print(f"\n  {entity_type} ({count} found):")
                for sample in samples[:3]:
                    print(f"    • {sample}")

    # Performance summary
    print(f"\n⚡ MODEL PERFORMANCE EXPECTATIONS")
    print("-" * 100)
    print(f"  Expected Performance Levels:")
    print(f"    • Excellent (F1 ≥ 90%):  19 entity types - Full automation ready")
    print(f"    • Good (F1 80-89%):       1 entity type  - Use with spot-checking")
    print(f"    • Caution (F1 < 50%):     3 entity types - Manual verification required")
    print(f"                              (VENDOR, VULNERABILITY, INDICATOR)")

    # Save results
    output = {
        'test_metadata': {
            'test_date': datetime.now().isoformat(),
            'model_path': str(model_path),
            'documents_tested': len(report_files),
            'model_load_time': load_time
        },
        'summary': summary['summary'],
        'entity_distribution': summary['entity_distribution'],
        'detailed_results': results
    }

    output_file = Path("batch_inference_results.json")
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n💾 Detailed results saved to: {output_file}")

    print("\n" + "=" * 100)
    print("✅ BATCH INFERENCE TEST COMPLETE")
    print("=" * 100)

if __name__ == "__main__":
    main()
