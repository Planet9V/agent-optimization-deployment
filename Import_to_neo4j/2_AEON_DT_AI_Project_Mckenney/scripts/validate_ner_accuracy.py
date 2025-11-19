#!/usr/bin/env python3
"""
NER Validation Test - Gate 2: Entity Ruler Bug Fix Validation
Tests accuracy improvement from 29% to 92%+ after EntityRuler pattern priority fix

This is a standalone script that directly imports NER agent without going through __init__.py
"""

import sys
import json
from pathlib import Path
from collections import defaultdict
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Direct import to avoid __init__.py dependencies
sys.path.insert(0, str(project_root / "agents"))
from base_agent import BaseAgent
from ner_agent import NERAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Test document paths
TEST_DOCUMENTS = [
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Dams/standards/standard-fema-20250102-05.md",
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Dams/standards/standard-icold-20250102-05.md",
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Dams/vendors/vendor-andritz-20250102-05.md",
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Dams/vendors/vendor-abb-20250102-05.md",
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Dams/equipment/device-generator-hydroelectric-20250102-05.md",
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Dams/equipment/device-turbine-francis-20250102-05.md",
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Dams/protocols/protocol-modbus-20250102-05.md",
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Dams/architectures/dam-control-system-20250102-05.md",
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Dams/security/dam-vulnerabilities-20250102-05.md",
]

# Expected entities per document (manually verified - conservative estimates)
EXPECTED_ENTITIES = {
    "standard-fema-20250102-05.md": {
        "ORGANIZATION": 3,
        "VENDOR": 5,
        "COMPONENT": 5,
        "STANDARD": 2,
    },
    "standard-icold-20250102-05.md": {
        "ORGANIZATION": 3,
        "COMPONENT": 8,
        "STANDARD": 8,
        "MEASUREMENT": 10,
    },
    "vendor-andritz-20250102-05.md": {
        "ORGANIZATION": 1,
        "VENDOR": 1,
        "COMPONENT": 10,
        "STANDARD": 2,
        "PROTOCOL": 5,
        "MEASUREMENT": 15,
    },
    "vendor-abb-20250102-05.md": {
        "ORGANIZATION": 1,
        "VENDOR": 1,
        "COMPONENT": 12,
        "STANDARD": 4,
        "PROTOCOL": 4,
        "MEASUREMENT": 12,
    },
    "device-generator-hydroelectric-20250102-05.md": {
        "ORGANIZATION": 3,
        "VENDOR": 3,
        "COMPONENT": 10,
        "STANDARD": 3,
        "MEASUREMENT": 15,
    },
    "device-turbine-francis-20250102-05.md": {
        "ORGANIZATION": 5,
        "VENDOR": 5,
        "COMPONENT": 12,
        "STANDARD": 1,
        "MEASUREMENT": 20,
    },
    "protocol-modbus-20250102-05.md": {
        "ORGANIZATION": 2,
        "VENDOR": 4,
        "COMPONENT": 4,
        "STANDARD": 3,
        "PROTOCOL": 3,
    },
    "dam-control-system-20250102-05.md": {
        "ORGANIZATION": 6,
        "VENDOR": 8,
        "COMPONENT": 10,
        "STANDARD": 5,
        "PROTOCOL": 7,
        "SYSTEM_LAYER": 5,
    },
    "dam-vulnerabilities-20250102-05.md": {
        "ORGANIZATION": 4,
        "VENDOR": 6,
        "COMPONENT": 4,
        "STANDARD": 4,
        "PROTOCOL": 3,
        "CVE": 3,
    },
}


def read_document(file_path: str) -> str:
    """Read markdown document"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def count_entities_by_type(entities: list) -> dict:
    """Count entities by type"""
    counts = defaultdict(int)
    for entity in entities:
        counts[entity['label']] += 1
    return dict(counts)


def calculate_accuracy_metrics(extracted: dict, expected: dict) -> dict:
    """
    Calculate precision, recall, F1 score

    Precision = TP / (TP + FP) = correctly extracted / total extracted
    Recall = TP / (TP + FN) = correctly extracted / total expected
    F1 = 2 * (Precision * Recall) / (Precision + Recall)
    """
    all_types = set(list(extracted.keys()) + list(expected.keys()))

    metrics = {}
    total_tp = 0
    total_extracted = 0
    total_expected = 0

    for entity_type in all_types:
        extracted_count = extracted.get(entity_type, 0)
        expected_count = expected.get(entity_type, 0)

        # True Positives: minimum of extracted and expected
        tp = min(extracted_count, expected_count)

        # False Positives: extracted more than expected
        fp = max(0, extracted_count - expected_count)

        # False Negatives: expected more than extracted
        fn = max(0, expected_count - extracted_count)

        # Calculate metrics
        precision = tp / extracted_count if extracted_count > 0 else 0
        recall = tp / expected_count if expected_count > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        metrics[entity_type] = {
            'tp': tp,
            'fp': fp,
            'fn': fn,
            'extracted': extracted_count,
            'expected': expected_count,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }

        total_tp += tp
        total_extracted += extracted_count
        total_expected += expected_count

    # Overall metrics
    overall_precision = total_tp / total_extracted if total_extracted > 0 else 0
    overall_recall = total_tp / total_expected if total_expected > 0 else 0
    overall_f1 = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0

    metrics['OVERALL'] = {
        'tp': total_tp,
        'extracted': total_extracted,
        'expected': total_expected,
        'precision': overall_precision,
        'recall': overall_recall,
        'f1': overall_f1
    }

    return metrics


def run_validation():
    """Run validation testing on all documents"""
    logger.info("=" * 80)
    logger.info("NER VALIDATION TEST - GATE 2: EntityRuler Bug Fix")
    logger.info("=" * 80)
    logger.info("")

    # Initialize NER agent
    config = {
        'pattern_library_path': '/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Critical_Infrastructure_Sectors_Patterns/dams/patterns'
    }

    logger.info("Initializing NER Agent...")
    try:
        ner_agent = NERAgent(config)
        logger.info(f"NER Agent initialized. spaCy available: {ner_agent.nlp is not None}")
    except Exception as e:
        logger.error(f"Failed to initialize NER Agent: {e}")
        return None
    logger.info("")

    # Process each document
    results = []
    all_metrics = []

    for doc_path in TEST_DOCUMENTS:
        doc_name = Path(doc_path).name
        logger.info(f"\n{'='*80}")
        logger.info(f"Processing: {doc_name}")
        logger.info(f"{'='*80}")

        # Read document
        try:
            text = read_document(doc_path)
            logger.info(f"Document length: {len(text)} chars")
        except Exception as e:
            logger.error(f"Failed to read document: {e}")
            continue

        # Extract entities
        try:
            extraction_result = ner_agent.execute({
                'text': text,
                'sector': 'dams',
                'extract_relationships': False
            })

            entities = extraction_result['entities']
            entity_counts = count_entities_by_type(entities)

            logger.info(f"Extracted {len(entities)} entities")
            logger.info(f"Entity counts by type: {entity_counts}")
        except Exception as e:
            logger.error(f"Failed to extract entities: {e}")
            continue

        # Get expected entities
        expected = EXPECTED_ENTITIES.get(doc_name, {})
        logger.info(f"Expected entities: {expected}")

        # Calculate metrics
        metrics = calculate_accuracy_metrics(entity_counts, expected)

        # Log metrics
        logger.info(f"\nAccuracy Metrics:")
        logger.info(f"  Precision: {metrics['OVERALL']['precision']:.2%}")
        logger.info(f"  Recall:    {metrics['OVERALL']['recall']:.2%}")
        logger.info(f"  F1 Score:  {metrics['OVERALL']['f1']:.2%}")

        # Store results
        results.append({
            'document': doc_name,
            'extracted_count': len(entities),
            'expected_count': sum(expected.values()),
            'entity_counts': entity_counts,
            'expected_entities': expected,
            'metrics': metrics
        })

        all_metrics.append(metrics['OVERALL'])

    if not all_metrics:
        logger.error("No results collected!")
        return None

    # Calculate overall average metrics
    avg_precision = sum(m['precision'] for m in all_metrics) / len(all_metrics)
    avg_recall = sum(m['recall'] for m in all_metrics) / len(all_metrics)
    avg_f1 = sum(m['f1'] for m in all_metrics) / len(all_metrics)

    logger.info(f"\n{'='*80}")
    logger.info("OVERALL RESULTS")
    logger.info(f"{'='*80}")
    logger.info(f"Documents tested: {len(TEST_DOCUMENTS)}")
    logger.info(f"Average Precision: {avg_precision:.2%}")
    logger.info(f"Average Recall:    {avg_recall:.2%}")
    logger.info(f"Average F1 Score:  {avg_f1:.2%}")
    logger.info("")

    # Determine pass/fail (target: ≥85% F1)
    target_f1 = 0.85
    passed = avg_f1 >= target_f1

    logger.info(f"Target F1 Score: {target_f1:.2%}")
    logger.info(f"Result: {'✓ PASS' if passed else '✗ FAIL'}")
    logger.info("")

    # Compare to expected 29% before fix
    improvement = avg_f1 - 0.29
    logger.info(f"Improvement from 29% (before fix): +{improvement:.2%}")
    logger.info(f"Expected target (92%+): {'✓ ACHIEVED' if avg_f1 >= 0.92 else '- Not quite there yet'}")
    logger.info("")

    return {
        'results': results,
        'avg_precision': avg_precision,
        'avg_recall': avg_recall,
        'avg_f1': avg_f1,
        'passed': passed,
        'target': target_f1
    }


if __name__ == "__main__":
    validation_results = run_validation()

    if validation_results is None:
        logger.error("Validation failed!")
        sys.exit(1)

    # Save results to JSON
    output_file = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Critical_Infrastructure_Sectors_Patterns/dams/validation/ner_validation_results.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        # Convert to JSON-serializable format
        serializable_results = {
            'avg_precision': validation_results['avg_precision'],
            'avg_recall': validation_results['avg_recall'],
            'avg_f1': validation_results['avg_f1'],
            'passed': validation_results['passed'],
            'target': validation_results['target'],
            'results': []
        }

        for result in validation_results['results']:
            serializable_results['results'].append({
                'document': result['document'],
                'extracted_count': result['extracted_count'],
                'expected_count': result['expected_count'],
                'entity_counts': result['entity_counts'],
                'expected_entities': result['expected_entities'],
                'precision': result['metrics']['OVERALL']['precision'],
                'recall': result['metrics']['OVERALL']['recall'],
                'f1': result['metrics']['OVERALL']['f1']
            })

        json.dump(serializable_results, f, indent=2)

    logger.info(f"Results saved to: {output_file}")
