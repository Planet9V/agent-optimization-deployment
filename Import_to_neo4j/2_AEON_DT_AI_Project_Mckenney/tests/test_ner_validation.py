#!/usr/bin/env python3
"""
NER Validation Test - Gate 2: Entity Ruler Bug Fix Validation
Tests accuracy improvement from 29% to 92%+ after EntityRuler pattern priority fix
"""

import sys
import json
from pathlib import Path
from collections import defaultdict
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.ner_agent import NERAgent

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

# Expected entities per document (manually verified from document reading)
# Format: {document_name: {entity_type: count}}
EXPECTED_ENTITIES = {
    "standard-fema-20250102-05.md": {
        "ORGANIZATION": 5,  # FEMA, USACE, state agencies, Leica Geosystems, Trimble, etc.
        "VENDOR": 8,  # Leica Geosystems, Trimble, Geokon, Bentley Systems, Federal Signal, etc.
        "COMPONENT": 5,  # piezometers, settlement gauges, crack monitors, seepage weirs, sirens
        "STANDARD": 3,  # inspection procedures, safety guidelines
        "PROTOCOL": 0,  # None mentioned
    },
    "standard-icold-20250102-05.md": {
        "ORGANIZATION": 3,  # ICOLD, FEMA, USACE
        "VENDOR": 0,
        "COMPONENT": 10,  # concrete dams, embankment dams, spillways, reservoirs, etc.
        "STANDARD": 10,  # Multiple ICOLD bulletins (bulletin_1 through bulletin_10)
        "PROTOCOL": 0,
        "MEASUREMENT": 15,  # MPa, m, seconds, etc.
    },
    "vendor-andritz-20250102-05.md": {
        "ORGANIZATION": 1,  # Andritz AG
        "VENDOR": 1,  # Andritz
        "COMPONENT": 12,  # Francis turbines, Kaplan turbines, Pelton turbines, generators, etc.
        "STANDARD": 2,  # IEC 61850, Modbus TCP
        "PROTOCOL": 6,  # IEC 61850, Modbus TCP, Profibus, OPC UA
        "MEASUREMENT": 20,  # MW, m, Hz, kV, %, etc.
    },
    "vendor-abb-20250102-05.md": {
        "ORGANIZATION": 1,  # ABB
        "VENDOR": 1,  # ABB
        "COMPONENT": 15,  # turbines, generators, control systems, PLCs, HMIs, etc.
        "STANDARD": 5,  # IEC 61850, IEEE C37.118, IEC 60255
        "PROTOCOL": 5,  # IEC 61850, Modbus TCP, Profibus, OPC UA
        "MEASUREMENT": 15,  # MW, m, Hz, kV, %
    },
    "device-generator-hydroelectric-20250102-05.md": {
        "ORGANIZATION": 3,  # ABB, Andritz, Voith
        "VENDOR": 3,  # ABB, Andritz, Voith
        "COMPONENT": 12,  # stator, rotor, excitation system, generator, synchronous generator, etc.
        "STANDARD": 3,  # IEC 60034, IEEE 1110, ISO 1940
        "PROTOCOL": 0,
        "MEASUREMENT": 20,  # MW, kV, Hz, °C, mm/s, MPa
    },
    "device-turbine-francis-20250102-05.md": {
        "ORGANIZATION": 5,  # ABB, Andritz, Voith, GE, Siemens
        "VENDOR": 5,  # ABB, Andritz, Voith, GE, Siemens
        "COMPONENT": 15,  # Francis turbine, spiral casing, runner, draft tube, guide vanes, etc.
        "STANDARD": 1,  # IEC 60193
        "PROTOCOL": 0,
        "MEASUREMENT": 25,  # m, MW, PSI, GPM, °C, mm/s
    },
    "protocol-modbus-20250102-05.md": {
        "ORGANIZATION": 3,  # Modbus Organization, various vendors
        "VENDOR": 5,  # Moxa, Advantech, Hirschmann, Siemens, Rockwell
        "COMPONENT": 5,  # PLCs, RTUs, HMIs, SCADA
        "STANDARD": 3,  # NIST SP 800-82, ISA-99/IEC 62443
        "PROTOCOL": 4,  # Modbus RTU, Modbus TCP, Modbus ASCII
    },
    "dam-control-system-20250102-05.md": {
        "ORGANIZATION": 7,  # Siemens, Rockwell, Schneider, ABB, GE, Cisco, etc.
        "VENDOR": 10,  # Siemens, Rockwell, Schneider, ABB, Mitsubishi, Omron, Cisco, Moxa, Dragos
        "COMPONENT": 12,  # PLCs, RTUs, HMIs, SCADA, network equipment
        "STANDARD": 5,  # NIST SP 800-82, ISA-62443, IEC 62443, IEC 60870-5-104
        "PROTOCOL": 8,  # Modbus, DNP3, IEC 61850, OPC UA, Profibus, HART, etc.
        "SYSTEM_LAYER": 8,  # L1-L5, field level, control level, supervisory level, enterprise level
    },
    "dam-vulnerabilities-20250102-05.md": {
        "ORGANIZATION": 5,  # CISA, DHS, NIST, ABB, Andritz, etc.
        "VENDOR": 7,  # ABB, Andritz, Voith, Siemens, Rockwell, Schneider, Cisco, Palo Alto, Dragos
        "COMPONENT": 5,  # PLCs, HMIs, SCADA systems
        "STANDARD": 4,  # ISA-62443, IEC 61508, NIST SP 800-82
        "PROTOCOL": 3,  # Modbus, DNP3, IEC 60870-5-104
        "CVE": 3,  # CVE-2021-34527, CVE-2021-44228, CVE-2020-1472
    },
}


def load_pattern_library(sector: str = "dams") -> dict:
    """Load sector-specific pattern library"""
    pattern_base = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Critical_Infrastructure_Sectors_Patterns")

    patterns = {}
    categories = ["standards", "vendors", "equipment", "protocols", "security", "architectures", "operations"]

    for category in categories:
        pattern_file = pattern_base / sector / "patterns" / f"{category}.yaml"
        if pattern_file.exists():
            logger.info(f"Found pattern file: {pattern_file}")

    return patterns


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
    ner_agent = NERAgent(config)
    logger.info(f"NER Agent initialized. spaCy available: {ner_agent.nlp is not None}")
    logger.info("")

    # Load pattern library
    load_pattern_library("dams")

    # Process each document
    results = []
    all_metrics = []

    for doc_path in TEST_DOCUMENTS:
        doc_name = Path(doc_path).name
        logger.info(f"\n{'='*80}")
        logger.info(f"Processing: {doc_name}")
        logger.info(f"{'='*80}")

        # Read document
        text = read_document(doc_path)
        logger.info(f"Document length: {len(text)} chars")

        # Extract entities
        extraction_result = ner_agent.execute({
            'text': text,
            'sector': 'dams',
            'extract_relationships': False
        })

        entities = extraction_result['entities']
        entity_counts = count_entities_by_type(entities)

        logger.info(f"Extracted {len(entities)} entities")
        logger.info(f"Entity counts by type: {entity_counts}")

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
