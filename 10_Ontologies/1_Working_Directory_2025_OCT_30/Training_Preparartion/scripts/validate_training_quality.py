#!/usr/bin/env python3
"""
Validate NER v7 training data quality and ensure no degradation from baseline.

DELIVERABLE: Quality validation of spaCy v3 training data with detailed metrics.
"""

import sys
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple
import json

import spacy
from spacy.tokens import DocBin


class TrainingDataValidator:
    """Validates spaCy training data format and quality."""

    EXPECTED_LABELS = {'CVE', 'CWE', 'CAPEC', 'ATTACK'}
    TARGET_DIVERSITY = {
        'CVE': 0.25,    # CVE/CWE dataset target
        'CWE': 0.25,
        'ATTACK': 0.90,  # Attack chain dataset target
        'CAPEC': 0.90
    }

    def __init__(self, training_data_dir: Path):
        self.data_dir = training_data_dir
        self.nlp = spacy.blank("en")

    def load_spacy_data(self, filename: str) -> List[spacy.tokens.Doc]:
        """Load .spacy binary file."""
        filepath = self.data_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Training file not found: {filepath}")

        doc_bin = DocBin().from_disk(filepath)
        return list(doc_bin.get_docs(self.nlp.vocab))

    def validate_format(self, docs: List[spacy.tokens.Doc]) -> Dict[str, any]:
        """Validate spaCy v3 format correctness."""
        issues = []

        for idx, doc in enumerate(docs):
            # Check text exists
            if not doc.text or len(doc.text.strip()) == 0:
                issues.append(f"Doc {idx}: Empty text")

            # Check entities
            for ent_idx, ent in enumerate(doc.ents):
                # Validate span boundaries
                if ent.start >= ent.end:
                    issues.append(f"Doc {idx}, Entity {ent_idx}: Invalid span (start >= end)")

                # Validate text bounds
                if ent.start_char < 0 or ent.end_char > len(doc.text):
                    issues.append(f"Doc {idx}, Entity {ent_idx}: Span outside text bounds")

                # Validate label types
                if ent.label_ not in self.EXPECTED_LABELS:
                    issues.append(f"Doc {idx}, Entity {ent_idx}: Unexpected label '{ent.label_}'")

        return {
            'valid': len(issues) == 0,
            'total_docs': len(docs),
            'issues': issues,
            'issue_count': len(issues)
        }

    def calculate_metrics(self, docs: List[spacy.tokens.Doc], dataset_name: str) -> Dict[str, any]:
        """Calculate quality metrics."""
        total_examples = len(docs)
        entity_counts = Counter()
        unique_entities = defaultdict(set)
        text_lengths = []
        entities_per_doc = []

        for doc in docs:
            text_lengths.append(len(doc.text))
            entities_per_doc.append(len(doc.ents))

            for ent in doc.ents:
                entity_counts[ent.label_] += 1
                unique_entities[ent.label_].add(ent.text)

        # Calculate diversity scores
        diversity_scores = {}
        for label in self.EXPECTED_LABELS:
            count = entity_counts.get(label, 0)
            unique_count = len(unique_entities.get(label, set()))
            diversity_scores[label] = unique_count / count if count > 0 else 0.0

        return {
            'dataset': dataset_name,
            'total_examples': total_examples,
            'total_entities': sum(entity_counts.values()),
            'entity_counts': dict(entity_counts),
            'unique_entity_counts': {k: len(v) for k, v in unique_entities.items()},
            'diversity_scores': diversity_scores,
            'avg_entities_per_doc': sum(entities_per_doc) / len(entities_per_doc) if entities_per_doc else 0,
            'text_length_stats': {
                'min': min(text_lengths) if text_lengths else 0,
                'max': max(text_lengths) if text_lengths else 0,
                'avg': sum(text_lengths) / len(text_lengths) if text_lengths else 0
            },
            'label_balance': {
                label: count / sum(entity_counts.values()) if sum(entity_counts.values()) > 0 else 0
                for label, count in entity_counts.items()
            }
        }

    def check_quality_degradation(self, metrics: Dict[str, any]) -> Tuple[bool, List[str]]:
        """Check for quality degradation indicators."""
        warnings = []
        passed = True

        dataset = metrics['dataset']

        # Check diversity scores against targets
        for label, score in metrics['diversity_scores'].items():
            target = self.TARGET_DIVERSITY.get(label, 0.5)

            if score < target * 0.8:  # Allow 20% below target
                warnings.append(
                    f"{dataset}: {label} diversity {score:.3f} below target {target:.3f}"
                )
                passed = False

        # Check for reasonable entity counts
        if metrics['total_entities'] < 100:
            warnings.append(f"{dataset}: Very low entity count ({metrics['total_entities']})")
            passed = False

        # Check for reasonable example count
        if metrics['total_examples'] < 50:
            warnings.append(f"{dataset}: Very low example count ({metrics['total_examples']})")
            passed = False

        # Check for label imbalance
        for label, balance in metrics['label_balance'].items():
            if balance < 0.05:  # Less than 5% of total
                warnings.append(f"{dataset}: {label} severely underrepresented ({balance:.1%})")

        return passed, warnings

    def validate_all(self) -> Dict[str, any]:
        """Execute complete validation workflow."""
        results = {
            'validation_date': '2025-11-08',
            'datasets': {},
            'overall_status': 'PASS',
            'warnings': [],
            'recommendations': []
        }

        # Define datasets to validate
        datasets = {
            'train': 'train.spacy',
            'dev': 'dev.spacy',
            'test': 'test.spacy'
        }

        all_passed = True

        for dataset_name, filename in datasets.items():
            try:
                # Load data
                docs = self.load_spacy_data(filename)

                # Validate format
                format_validation = self.validate_format(docs)

                # Calculate metrics
                metrics = self.calculate_metrics(docs, dataset_name)

                # Check quality
                quality_passed, warnings = self.check_quality_degradation(metrics)

                results['datasets'][dataset_name] = {
                    'file': filename,
                    'format_validation': format_validation,
                    'metrics': metrics,
                    'quality_passed': quality_passed,
                    'warnings': warnings
                }

                if not format_validation['valid']:
                    all_passed = False
                    results['warnings'].extend([
                        f"{dataset_name}: Format validation failed",
                        *format_validation['issues'][:5]  # Show first 5 issues
                    ])

                if not quality_passed:
                    all_passed = False
                    results['warnings'].extend(warnings)

            except Exception as e:
                all_passed = False
                results['datasets'][dataset_name] = {
                    'file': filename,
                    'error': str(e)
                }
                results['warnings'].append(f"{dataset_name}: Failed to load - {e}")

        results['overall_status'] = 'PASS' if all_passed else 'FAIL'

        # Generate recommendations
        if not all_passed:
            results['recommendations'].extend([
                "Review format validation errors and fix entity spans",
                "Increase diversity by adding more unique examples",
                "Balance label distribution across entity types",
                "Ensure minimum thresholds met for production readiness"
            ])

        return results


def generate_report(results: Dict[str, any], output_path: Path):
    """Generate markdown validation report."""
    report = []
    report.append("# NER v7 Training Data Validation Report\n")
    report.append(f"**Validation Date**: {results['validation_date']}\n")
    report.append(f"**Overall Status**: {results['overall_status']}\n\n")

    # Summary
    report.append("## Executive Summary\n")
    if results['overall_status'] == 'PASS':
        report.append("✅ All training datasets meet quality standards.\n\n")
    else:
        report.append("❌ Quality issues detected requiring attention.\n\n")
        report.append("### Critical Warnings\n")
        for warning in results['warnings']:
            report.append(f"- {warning}\n")
        report.append("\n")

    # Dataset Details
    report.append("## Dataset Metrics\n\n")
    for dataset_name, data in results['datasets'].items():
        report.append(f"### {dataset_name.upper()}\n")

        if 'error' in data:
            report.append(f"❌ **Error**: {data['error']}\n\n")
            continue

        metrics = data.get('metrics', {})
        format_val = data.get('format_validation', {})

        report.append(f"**File**: `{data['file']}`\n")
        report.append(f"**Format Valid**: {'✅ Yes' if format_val.get('valid') else '❌ No'}\n")
        report.append(f"**Quality Status**: {'✅ PASS' if data.get('quality_passed') else '⚠️ NEEDS REVIEW'}\n\n")

        # Metrics table
        report.append("| Metric | Value |\n")
        report.append("|--------|-------|\n")
        report.append(f"| Total Examples | {metrics.get('total_examples', 0)} |\n")
        report.append(f"| Total Entities | {metrics.get('total_entities', 0)} |\n")
        report.append(f"| Avg Entities/Doc | {metrics.get('avg_entities_per_doc', 0):.2f} |\n")
        report.append(f"| Avg Text Length | {metrics.get('text_length_stats', {}).get('avg', 0):.0f} chars |\n\n")

        # Entity breakdown
        report.append("**Entity Distribution**:\n")
        entity_counts = metrics.get('entity_counts', {})
        for label in sorted(entity_counts.keys()):
            count = entity_counts[label]
            unique = metrics.get('unique_entity_counts', {}).get(label, 0)
            diversity = metrics.get('diversity_scores', {}).get(label, 0)
            balance = metrics.get('label_balance', {}).get(label, 0)
            report.append(f"- **{label}**: {count} total, {unique} unique (diversity: {diversity:.3f}, {balance:.1%} of dataset)\n")

        report.append("\n")

        # Format issues
        if format_val.get('issues'):
            report.append(f"**Format Issues** ({format_val['issue_count']} total):\n")
            for issue in format_val['issues'][:10]:  # Show first 10
                report.append(f"- {issue}\n")
            if format_val['issue_count'] > 10:
                report.append(f"- ... and {format_val['issue_count'] - 10} more\n")
            report.append("\n")

    # Recommendations
    if results.get('recommendations'):
        report.append("## Recommendations\n\n")
        for rec in results['recommendations']:
            report.append(f"- {rec}\n")
        report.append("\n")

    # Conclusion
    report.append("## Conclusion\n\n")
    if results['overall_status'] == 'PASS':
        report.append("Training data validation **PASSED**. All datasets meet quality standards for NER model training.\n")
    else:
        report.append("Training data validation **FAILED**. Address warnings and recommendations before proceeding with model training.\n")

    # Write report
    output_path.write_text(''.join(report))
    print(f"Validation report written to: {output_path}")


def main():
    """Main validation execution."""
    base_dir = Path(__file__).parent.parent
    training_data_dir = base_dir / "ner_training_data"

    print("="*60)
    print("NER v7 Training Data Quality Validation")
    print("="*60)
    print(f"Training data directory: {training_data_dir}")
    print()

    # Execute validation
    validator = TrainingDataValidator(training_data_dir)
    results = validator.validate_all()

    # Save results
    results_file = base_dir / "docs" / "validation_results.json"
    results_file.parent.mkdir(exist_ok=True)
    results_file.write_text(json.dumps(results, indent=2))
    print(f"Validation results: {results_file}")

    # Generate report
    report_file = base_dir / "docs" / "VALIDATION_REPORT.md"
    generate_report(results, report_file)

    # Print summary
    print()
    print("="*60)
    print(f"VALIDATION STATUS: {results['overall_status']}")
    print("="*60)

    if results['overall_status'] == 'FAIL':
        print("\nCritical Warnings:")
        for warning in results['warnings'][:10]:
            print(f"  ⚠️  {warning}")
        if len(results['warnings']) > 10:
            print(f"  ... and {len(results['warnings']) - 10} more warnings")
        sys.exit(1)
    else:
        print("\n✅ All quality checks passed. Training data ready for model training.")
        sys.exit(0)


if __name__ == "__main__":
    main()
