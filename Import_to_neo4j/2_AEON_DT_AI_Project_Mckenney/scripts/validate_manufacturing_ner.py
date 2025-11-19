#!/usr/bin/env python3
"""
Manufacturing NER Validation Script
Validates extracted Manufacturing patterns by running NER on 9 diverse test documents
"""

import sys
import os
import json
import yaml
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Add agents directory to path
sys.path.insert(0, '/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/agents')

from ner_agent import NERAgent

# Test document selection (9 diverse documents)
TEST_DOCUMENTS = [
    # 2 vendor files (different vendors from pattern extraction)
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Manufacturing/vendors/vendor-omron-20250102-06.md",
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Manufacturing/vendors/vendor-mitsubishi-20250102-06.md",
    # 2 equipment files
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Manufacturing/equipment/device-cnc-machine-20250102-06.md",
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Manufacturing/equipment/device-plc-20250102-06.md",
    # 2 operations files
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Manufacturing/operations/procedure-equipment-maintenance-20250102-06.md",
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Manufacturing/operations/procedure-plc-maintenance-20250102-06.md",
    # 1 protocol file
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Manufacturing/protocols/protocol-modbus-20250102-06.md",
    # 1 architecture file
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Manufacturing/architectures/network-pattern-industrial-iot-20250102-06.md",
    # 1 supplier file
    "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Manufacturing/suppliers/supplier-distributor-industrial-20250102-06.md",
]

# Pattern files directory
PATTERNS_DIR = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Critical_Infrastructure_Sectors_Patterns/manufacturing/patterns"

# Output directory
OUTPUT_DIR = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Critical_Infrastructure_Sectors_Patterns/manufacturing/validation"


def load_patterns():
    """Load all Manufacturing pattern files"""
    patterns = {}
    pattern_files = [
        'vendors.yaml',
        'equipment.yaml',
        'protocols.yaml',
        'operations.yaml',
        'architectures.yaml',
        'suppliers.yaml',
        'standards.yaml',
        'security.yaml'
    ]

    for filename in pattern_files:
        filepath = os.path.join(PATTERNS_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
                if data:
                    patterns[filename] = data

    return patterns


def extract_ground_truth(text, patterns):
    """
    Extract ground truth entities from text using pattern matching
    Returns dict of entity_type -> set of matched entities
    """
    ground_truth = defaultdict(set)

    # Extract vendors
    if 'vendors.yaml' in patterns:
        vendor_data = patterns['vendors.yaml']
        if 'patterns' in vendor_data:
            for pattern in vendor_data['patterns']:
                if 'pattern' in pattern:
                    matches = re.finditer(pattern['pattern'], text, re.IGNORECASE)
                    for match in matches:
                        ground_truth['VENDOR'].add(match.group(0))

    # Extract equipment
    if 'equipment.yaml' in patterns:
        equipment_data = patterns['equipment.yaml']
        if 'patterns' in equipment_data:
            for pattern in equipment_data['patterns']:
                if 'pattern' in pattern:
                    matches = re.finditer(pattern['pattern'], text, re.IGNORECASE)
                    for match in matches:
                        ground_truth['EQUIPMENT'].add(match.group(0))

    # Extract protocols
    if 'protocols.yaml' in patterns:
        protocol_data = patterns['protocols.yaml']
        if 'patterns' in protocol_data:
            for pattern in protocol_data['patterns']:
                if 'pattern' in pattern:
                    matches = re.finditer(pattern['pattern'], text, re.IGNORECASE)
                    for match in matches:
                        ground_truth['PROTOCOL'].add(match.group(0))

    # Extract operations
    if 'operations.yaml' in patterns:
        operations_data = patterns['operations.yaml']
        if 'patterns' in operations_data:
            for pattern in operations_data['patterns']:
                if 'pattern' in pattern:
                    matches = re.finditer(pattern['pattern'], text, re.IGNORECASE)
                    for match in matches:
                        ground_truth['OPERATION'].add(match.group(0))

    # Extract architectures
    if 'architectures.yaml' in patterns:
        arch_data = patterns['architectures.yaml']
        if 'patterns' in arch_data:
            for pattern in arch_data['patterns']:
                if 'pattern' in pattern:
                    matches = re.finditer(pattern['pattern'], text, re.IGNORECASE)
                    for match in matches:
                        ground_truth['ARCHITECTURE'].add(match.group(0))

    # Extract suppliers
    if 'suppliers.yaml' in patterns:
        supplier_data = patterns['suppliers.yaml']
        if 'patterns' in supplier_data:
            for pattern in supplier_data['patterns']:
                if 'pattern' in pattern:
                    matches = re.finditer(pattern['pattern'], text, re.IGNORECASE)
                    for match in matches:
                        ground_truth['SUPPLIER'].add(match.group(0))

    return ground_truth


def calculate_f1_score(predicted, ground_truth):
    """
    Calculate precision, recall, and F1 score
    """
    if not predicted and not ground_truth:
        return 1.0, 1.0, 1.0

    if not predicted:
        return 0.0, 0.0, 0.0

    if not ground_truth:
        return 0.0, 0.0, 0.0

    # Convert to sets for comparison
    pred_set = set(predicted)
    gt_set = set(ground_truth)

    # Calculate metrics
    true_positives = len(pred_set & gt_set)
    false_positives = len(pred_set - gt_set)
    false_negatives = len(gt_set - pred_set)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return precision, recall, f1


def validate_document(doc_path, ner_agent, patterns):
    """
    Validate NER extraction on a single document
    Returns validation results
    """
    # Read document
    with open(doc_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Extract entities using NER agent
    extracted_entities = ner_agent.extract_entities(text, 'manufacturing')

    # Extract ground truth using patterns
    ground_truth = extract_ground_truth(text, patterns)

    # Calculate scores per entity type
    entity_scores = {}
    all_predicted = []
    all_ground_truth = []

    for entity_type in set(list(extracted_entities.keys()) + list(ground_truth.keys())):
        predicted = [e['text'] for e in extracted_entities.get(entity_type, [])]
        gt = list(ground_truth.get(entity_type, set()))

        precision, recall, f1 = calculate_f1_score(predicted, gt)

        entity_scores[entity_type] = {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'predicted_count': len(predicted),
            'ground_truth_count': len(gt)
        }

        all_predicted.extend(predicted)
        all_ground_truth.extend(gt)

    # Calculate overall scores
    overall_precision, overall_recall, overall_f1 = calculate_f1_score(all_predicted, all_ground_truth)

    return {
        'document': os.path.basename(doc_path),
        'path': doc_path,
        'entity_scores': entity_scores,
        'overall': {
            'precision': overall_precision,
            'recall': overall_recall,
            'f1': overall_f1
        },
        'total_predicted': len(all_predicted),
        'total_ground_truth': len(all_ground_truth)
    }


def main():
    """Run validation on all test documents"""
    print("=" * 80)
    print("MANUFACTURING NER VALIDATION")
    print("=" * 80)
    print()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load patterns
    print("Loading patterns...")
    patterns = load_patterns()
    print(f"Loaded {len(patterns)} pattern files")
    print()

    # Initialize NER agent
    print("Initializing NER agent...")
    ner_agent = NERAgent()
    print()

    # Validate each document
    results = []
    total_f1 = 0.0

    print("Validating documents...")
    print("-" * 80)

    for i, doc_path in enumerate(TEST_DOCUMENTS, 1):
        if not os.path.exists(doc_path):
            print(f"⚠️  Document not found: {doc_path}")
            continue

        print(f"\n[{i}/9] {os.path.basename(doc_path)}")

        result = validate_document(doc_path, ner_agent, patterns)
        results.append(result)

        print(f"  F1 Score: {result['overall']['f1']:.3f}")
        print(f"  Precision: {result['overall']['precision']:.3f}")
        print(f"  Recall: {result['overall']['recall']:.3f}")
        print(f"  Entities: {result['total_predicted']} predicted, {result['total_ground_truth']} ground truth")

        total_f1 += result['overall']['f1']

    # Calculate average F1
    avg_f1 = total_f1 / len(results) if results else 0.0

    print()
    print("=" * 80)
    print(f"AVERAGE F1 SCORE: {avg_f1:.3f}")
    print("=" * 80)

    # Determine pass/fail
    threshold = 0.85
    verdict = "PASS" if avg_f1 >= threshold else "FAIL"
    print(f"Verdict: {verdict} (threshold: {threshold:.2f})")
    print()

    # Save JSON results
    json_output = {
        'sector': 'manufacturing',
        'test_date': datetime.now().strftime('%Y-%m-%d'),
        'total_documents': len(results),
        'average_f1_score': avg_f1,
        'threshold': threshold,
        'verdict': verdict,
        'documents': results
    }

    json_path = os.path.join(OUTPUT_DIR, 'ner_validation_results.json')
    with open(json_path, 'w') as f:
        json.dump(json_output, f, indent=2)

    print(f"JSON results saved to: {json_path}")

    # Generate markdown report
    report_path = os.path.join(OUTPUT_DIR, 'accuracy_validation_report.md')
    generate_report(results, avg_f1, verdict, threshold, report_path)

    print(f"Validation report saved to: {report_path}")
    print()

    return avg_f1


def generate_report(results, avg_f1, verdict, threshold, output_path):
    """Generate markdown validation report"""

    report = f"""# Manufacturing NER Accuracy Validation Report

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Sector**: Manufacturing
**Total Documents**: {len(results)}
**Average F1 Score**: {avg_f1:.3f}
**Threshold**: {threshold:.2f}
**Verdict**: **{verdict}**

## Executive Summary

This report validates the Named Entity Recognition (NER) patterns for the Manufacturing sector by testing extraction accuracy across 9 diverse documents representing different content types (vendors, equipment, operations, protocols, architectures, and suppliers).

## Test Document Selection

Following the Dams validation methodology, we selected 9 diverse documents:

| # | Document | Type |
|---|----------|------|
"""

    for i, result in enumerate(results, 1):
        doc_type = result['document'].split('-')[0]
        report += f"| {i} | {result['document']} | {doc_type} |\n"

    report += f"""
## Per-Document Results

"""

    for i, result in enumerate(results, 1):
        report += f"""### Document {i}: {result['document']}

- **Overall F1 Score**: {result['overall']['f1']:.3f}
- **Precision**: {result['overall']['precision']:.3f}
- **Recall**: {result['overall']['recall']:.3f}
- **Total Predicted**: {result['total_predicted']}
- **Total Ground Truth**: {result['total_ground_truth']}

#### Entity Type Breakdown

"""

        if result['entity_scores']:
            report += "| Entity Type | Precision | Recall | F1 Score | Predicted | Ground Truth |\n"
            report += "|-------------|-----------|--------|----------|-----------|---------------|\n"

            for entity_type, scores in sorted(result['entity_scores'].items()):
                report += f"| {entity_type} | {scores['precision']:.3f} | {scores['recall']:.3f} | {scores['f1']:.3f} | {scores['predicted_count']} | {scores['ground_truth_count']} |\n"
        else:
            report += "*No entities extracted*\n"

        report += "\n"

    report += f"""## Overall Performance

### Average Metrics

- **Average F1 Score**: {avg_f1:.3f}
- **Expected Range**: 0.89 - 0.91 (based on quality assessment)
- **Actual Performance**: {"Within expected range" if 0.89 <= avg_f1 <= 0.91 else "Outside expected range"}

### Entity Type Performance

"""

    # Calculate average scores per entity type
    entity_type_scores = defaultdict(lambda: {'precision': [], 'recall': [], 'f1': []})

    for result in results:
        for entity_type, scores in result['entity_scores'].items():
            entity_type_scores[entity_type]['precision'].append(scores['precision'])
            entity_type_scores[entity_type]['recall'].append(scores['recall'])
            entity_type_scores[entity_type]['f1'].append(scores['f1'])

    if entity_type_scores:
        report += "| Entity Type | Avg Precision | Avg Recall | Avg F1 Score |\n"
        report += "|-------------|---------------|------------|---------------|\n"

        for entity_type in sorted(entity_type_scores.keys()):
            avg_precision = sum(entity_type_scores[entity_type]['precision']) / len(entity_type_scores[entity_type]['precision'])
            avg_recall = sum(entity_type_scores[entity_type]['recall']) / len(entity_type_scores[entity_type]['recall'])
            avg_f1_type = sum(entity_type_scores[entity_type]['f1']) / len(entity_type_scores[entity_type]['f1'])

            report += f"| {entity_type} | {avg_precision:.3f} | {avg_recall:.3f} | {avg_f1_type:.3f} |\n"

    report += f"""
## Validation Verdict

**{verdict}** - Average F1 score of {avg_f1:.3f} {"meets" if avg_f1 >= threshold else "does not meet"} the threshold of {threshold:.2f}

### Comparison to Quality Assessment

The quality assessment predicted an F1 score range of 89-91% based on:
- High-quality pattern extraction
- Comprehensive entity coverage
- Well-structured YAML patterns
- Good regex pattern quality

**Actual Result**: {avg_f1*100:.1f}%
**Assessment Accuracy**: {"Accurate prediction" if 0.89 <= avg_f1 <= 0.91 else "Outside predicted range"}

## Recommendations

"""

    if avg_f1 >= 0.90:
        report += """- ✅ Patterns are performing excellently
- ✅ Ready for production use
- Consider expanding test coverage for edge cases
"""
    elif avg_f1 >= threshold:
        report += """- ✅ Patterns meet minimum requirements
- Consider refinement for improved accuracy
- Focus on entity types with lower F1 scores
"""
    else:
        report += """- ⚠️ Patterns need improvement
- Review low-performing entity types
- Add more pattern variations
- Consider manual review of extraction errors
"""

    report += f"""
## Methodology

### Pattern Loading
- Loaded 8 pattern files from Manufacturing patterns directory
- Pattern types: vendors, equipment, protocols, operations, architectures, suppliers, standards, security

### Ground Truth Extraction
- Applied regex patterns from YAML files to extract expected entities
- Matched extracted entities against NER agent predictions

### F1 Score Calculation
- **Precision**: True Positives / (True Positives + False Positives)
- **Recall**: True Positives / (True Positives + False Negatives)
- **F1 Score**: 2 × (Precision × Recall) / (Precision + Recall)

### Test Document Selection
- 9 diverse documents selected to represent sector breadth
- Balanced across content types (vendors, equipment, operations, etc.)
- Different vendors/equipment from pattern extraction sources

---

*Report generated by Manufacturing NER Validation Script*
*Validation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    with open(output_path, 'w') as f:
        f.write(report)


if __name__ == '__main__':
    avg_f1 = main()
    sys.exit(0 if avg_f1 >= 0.85 else 1)
