#!/usr/bin/env python3
"""
Entity Boundary Validator for NER Training Data

Analyzes entity annotations in markdown files to identify boundary issues,
quality problems, and consistency concerns.

Usage:
    python entity_boundary_validator.py <file_or_directory> [--sample-size N]
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class BoundaryIssue:
    """Represents a single boundary validation issue"""
    line_number: int
    entity_text: str
    entity_type: str
    issue_type: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    description: str
    context: str


@dataclass
class FileQualityScore:
    """Quality metrics for a single file"""
    file_path: str
    total_entities: int
    total_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    quality_score: float  # 0-100
    issues_by_type: Dict[str, int]
    vendor_quality_score: float  # 0-100 for VENDOR entities
    equipment_quality_score: float  # 0-100 for EQUIPMENT entities


class EntityBoundaryValidator:
    """Validates entity boundaries and annotation quality"""

    # Markdown syntax patterns that should not be part of entities
    # Note: Parentheses are allowed in entity names (e.g., "TMR (Triple Modular Redundant)")
    MARKDOWN_SYNTAX = [
        r'^#+\s',  # Headers
        r'\*\*',   # Bold
        r'__',     # Bold alternative
        r'(?<!\w)\*(?!\w)',     # Italic (not part of word)
        r'(?<!\w)_(?!\w)',      # Italic alternative (not part of word)
        r'^\d+\.',  # Ordered list
        r'^-\s',   # Unordered list
        r'^>\s',   # Blockquote
        r'`',      # Code
        r'\[',     # Link start
        r'\]',     # Link end
    ]

    # Common vendor/product naming patterns
    VENDOR_PATTERNS = {
        'company_suffixes': ['Inc', 'Inc.', 'Ltd', 'Ltd.', 'Corp', 'Corp.',
                            'LLC', 'AG', 'GmbH', 'Limited', 'Group', 'Company'],
        'product_indicators': ['System', 'Platform', 'Controller', 'Series',
                              'Model', 'Version', 'Edition'],
    }

    def __init__(self):
        self.issues: List[BoundaryIssue] = []
        self.entity_stats = defaultdict(lambda: {'count': 0, 'unique': set()})

    def validate_entity_boundaries(self, file_path: Path) -> FileQualityScore:
        """
        Validate all entity annotations in a file

        Args:
            file_path: Path to markdown file with entity annotations

        Returns:
            FileQualityScore object with metrics and issues
        """
        self.issues = []
        self.entity_stats = defaultdict(lambda: {'count': 0, 'unique': set()})

        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return self._create_error_score(str(file_path))

        lines = content.split('\n')

        # Extract entities from markdown (format: [[ENTITY_TYPE: text]])
        entity_pattern = r'\[\[([A-Z_]+):\s*([^\]]+?)\]\]'

        for line_num, line in enumerate(lines, 1):
            matches = re.finditer(entity_pattern, line)

            for match in matches:
                entity_type = match.group(1)
                entity_text = match.group(2)

                # Track statistics
                self.entity_stats[entity_type]['count'] += 1
                self.entity_stats[entity_type]['unique'].add(entity_text)

                # Validate this entity
                self._validate_single_entity(
                    entity_text, entity_type, line_num, line, match.span()
                )

        return self._calculate_quality_score(str(file_path))

    def _validate_single_entity(self, entity_text: str, entity_type: str,
                                line_num: int, line: str, span: Tuple[int, int]):
        """Validate a single entity annotation"""

        # Check 1: Leading/trailing whitespace
        if entity_text != entity_text.strip():
            self.issues.append(BoundaryIssue(
                line_number=line_num,
                entity_text=entity_text,
                entity_type=entity_type,
                issue_type='whitespace',
                severity='high',
                description='Entity has leading or trailing whitespace',
                context=line.strip()
            ))

        # Check 2: Markdown syntax within entity
        for syntax_pattern in self.MARKDOWN_SYNTAX:
            if re.search(syntax_pattern, entity_text):
                self.issues.append(BoundaryIssue(
                    line_number=line_num,
                    entity_text=entity_text,
                    entity_type=entity_type,
                    issue_type='markdown_syntax',
                    severity='critical',
                    description=f'Entity contains markdown syntax: {syntax_pattern}',
                    context=line.strip()
                ))

        # Check 3: Word boundary issues
        if not self._check_word_boundaries(entity_text, line, span):
            self.issues.append(BoundaryIssue(
                line_number=line_num,
                entity_text=entity_text,
                entity_type=entity_type,
                issue_type='word_boundary',
                severity='medium',
                description='Entity not on word boundaries',
                context=line.strip()
            ))

        # Check 4: Multi-line entities (should not happen in this format)
        if '\n' in entity_text:
            self.issues.append(BoundaryIssue(
                line_number=line_num,
                entity_text=entity_text,
                entity_type=entity_type,
                issue_type='multiline',
                severity='critical',
                description='Entity spans multiple lines',
                context=line.strip()
            ))

        # Check 5: Empty or very short entities
        if len(entity_text.strip()) < 2:
            self.issues.append(BoundaryIssue(
                line_number=line_num,
                entity_text=entity_text,
                entity_type=entity_type,
                issue_type='too_short',
                severity='high',
                description='Entity is too short (< 2 characters)',
                context=line.strip()
            ))

        # Check 6: Vendor-specific validation
        if entity_type == 'VENDOR':
            self._validate_vendor_entity(entity_text, entity_type, line_num, line)

        # Check 7: Equipment-specific validation
        if entity_type == 'EQUIPMENT':
            self._validate_equipment_entity(entity_text, entity_type, line_num, line)

    def _check_word_boundaries(self, entity_text: str, line: str,
                               span: Tuple[int, int]) -> bool:
        """Check if entity is on word boundaries"""
        # Get the actual text position in the line (accounting for markdown)
        start_pos = span[0]
        end_pos = span[1]

        # Check character before entity
        if start_pos > 0:
            char_before = line[start_pos - 1]
            if char_before.isalnum():
                return False

        # Check character after entity
        if end_pos < len(line):
            char_after = line[end_pos]
            if char_after.isalnum():
                return False

        return True

    def _validate_vendor_entity(self, entity_text: str, entity_type: str,
                                line_num: int, line: str):
        """Vendor-specific validation"""

        # Check if it's a product name masquerading as vendor
        product_indicators = ['System', 'Platform', 'Controller', 'Interface',
                             'Server', 'Gateway', 'Module', 'Device']

        if any(indicator in entity_text for indicator in product_indicators):
            self.issues.append(BoundaryIssue(
                line_number=line_num,
                entity_text=entity_text,
                entity_type=entity_type,
                issue_type='vendor_product_confusion',
                severity='medium',
                description='VENDOR entity may be a product name',
                context=line.strip()
            ))

        # Check for inconsistent naming (e.g., "Siemens" vs "Siemens AG")
        base_name = entity_text.split()[0] if entity_text else ""
        if base_name and len(entity_text.split()) > 2:
            self.issues.append(BoundaryIssue(
                line_number=line_num,
                entity_text=entity_text,
                entity_type=entity_type,
                issue_type='vendor_naming_consistency',
                severity='low',
                description='Complex vendor name may need normalization',
                context=line.strip()
            ))

    def _validate_equipment_entity(self, entity_text: str, entity_type: str,
                                   line_num: int, line: str):
        """Equipment-specific validation"""

        # Check if it contains vendor name (should be separate entities)
        known_vendors = ['Siemens', 'ABB', 'GE', 'Schneider', 'Rockwell']

        for vendor in known_vendors:
            if vendor in entity_text:
                self.issues.append(BoundaryIssue(
                    line_number=line_num,
                    entity_text=entity_text,
                    entity_type=entity_type,
                    issue_type='equipment_vendor_overlap',
                    severity='high',
                    description=f'EQUIPMENT contains vendor name: {vendor}',
                    context=line.strip()
                ))

    def _calculate_quality_score(self, file_path: str) -> FileQualityScore:
        """Calculate overall quality score for file"""

        total_entities = sum(stats['count'] for stats in self.entity_stats.values())

        if total_entities == 0:
            return self._create_error_score(file_path)

        # Count issues by severity
        critical = sum(1 for i in self.issues if i.severity == 'critical')
        high = sum(1 for i in self.issues if i.severity == 'high')
        medium = sum(1 for i in self.issues if i.severity == 'medium')
        low = sum(1 for i in self.issues if i.severity == 'low')

        # Calculate weighted quality score
        # Critical: -10, High: -5, Medium: -2, Low: -1
        penalty = (critical * 10) + (high * 5) + (medium * 2) + (low * 1)
        max_score = total_entities * 10  # Perfect score baseline

        quality_score = max(0, 100 * (1 - penalty / max_score))

        # Calculate entity-type specific scores
        vendor_score = self._calculate_entity_type_score('VENDOR')
        equipment_score = self._calculate_entity_type_score('EQUIPMENT')

        # Count issues by type
        issues_by_type = defaultdict(int)
        for issue in self.issues:
            issues_by_type[issue.issue_type] += 1

        return FileQualityScore(
            file_path=file_path,
            total_entities=total_entities,
            total_issues=len(self.issues),
            critical_issues=critical,
            high_issues=high,
            medium_issues=medium,
            low_issues=low,
            quality_score=quality_score,
            issues_by_type=dict(issues_by_type),
            vendor_quality_score=vendor_score,
            equipment_quality_score=equipment_score
        )

    def _calculate_entity_type_score(self, entity_type: str) -> float:
        """Calculate quality score for specific entity type"""

        entity_issues = [i for i in self.issues if i.entity_type == entity_type]
        entity_count = self.entity_stats[entity_type]['count']

        if entity_count == 0:
            return 0.0

        # Weighted penalty
        penalty = sum(
            10 if i.severity == 'critical' else
            5 if i.severity == 'high' else
            2 if i.severity == 'medium' else 1
            for i in entity_issues
        )

        max_score = entity_count * 10
        return max(0, 100 * (1 - penalty / max_score))

    def _create_error_score(self, file_path: str) -> FileQualityScore:
        """Create a score object for files with errors"""
        return FileQualityScore(
            file_path=file_path,
            total_entities=0,
            total_issues=0,
            critical_issues=0,
            high_issues=0,
            medium_issues=0,
            low_issues=0,
            quality_score=0.0,
            issues_by_type={},
            vendor_quality_score=0.0,
            equipment_quality_score=0.0
        )

    def analyze_vendor_annotations(self, file_path: Path) -> Dict[str, Any]:
        """
        Detailed analysis of VENDOR entity annotations

        Returns:
            Dictionary with vendor-specific metrics
        """
        score = self.validate_entity_boundaries(file_path)

        vendor_issues = [i for i in self.issues if i.entity_type == 'VENDOR']
        vendor_entities = self.entity_stats['VENDOR']['unique']

        # Analyze naming patterns
        naming_patterns = {
            'base_names': set(),
            'with_suffix': [],
            'product_like': [],
        }

        for vendor in vendor_entities:
            base = vendor.split()[0] if vendor else ""
            naming_patterns['base_names'].add(base)

            # Check for company suffixes
            if any(suffix in vendor for suffix in self.VENDOR_PATTERNS['company_suffixes']):
                naming_patterns['with_suffix'].append(vendor)

            # Check for product-like names
            if any(ind in vendor for ind in self.VENDOR_PATTERNS['product_indicators']):
                naming_patterns['product_like'].append(vendor)

        return {
            'file_path': str(file_path),
            'total_vendor_annotations': self.entity_stats['VENDOR']['count'],
            'unique_vendors': len(vendor_entities),
            'vendor_issues': len(vendor_issues),
            'vendor_quality_score': score.vendor_quality_score,
            'naming_patterns': {
                'unique_base_names': len(naming_patterns['base_names']),
                'vendors_with_suffix': len(naming_patterns['with_suffix']),
                'product_like_names': len(naming_patterns['product_like']),
            },
            'issues_by_type': defaultdict(int, {
                i.issue_type: sum(1 for x in vendor_issues if x.issue_type == i.issue_type)
                for i in vendor_issues
            }),
            'sample_issues': [
                {
                    'line': i.line_number,
                    'text': i.entity_text,
                    'type': i.issue_type,
                    'severity': i.severity
                }
                for i in vendor_issues[:10]  # Sample of first 10 issues
            ]
        }


def batch_analyze_directory(directory: Path, sample_size: int = 50) -> Dict[str, Any]:
    """
    Analyze a sample of files from a directory

    Args:
        directory: Path to directory containing markdown files
        sample_size: Number of files to analyze (default 50)

    Returns:
        Summary statistics and quality scores
    """
    validator = EntityBoundaryValidator()

    # Find all markdown files
    md_files = list(directory.rglob('*.md'))

    # Filter out README files
    md_files = [f for f in md_files if 'README' not in f.name.upper()]

    print(f"Found {len(md_files)} markdown files in {directory}")

    # Sample files if needed
    if len(md_files) > sample_size:
        import random
        md_files = random.sample(md_files, sample_size)
        print(f"Analyzing sample of {sample_size} files")

    results = {
        'summary': {
            'total_files_analyzed': 0,
            'total_entities': 0,
            'total_issues': 0,
            'average_quality_score': 0.0,
            'files_by_quality': {
                'excellent': 0,  # 90-100
                'good': 0,       # 75-89
                'fair': 0,       # 60-74
                'poor': 0,       # <60
            },
        },
        'file_scores': [],
        'worst_files': [],
        'issue_distribution': defaultdict(int),
    }

    quality_scores = []

    for md_file in md_files:
        print(f"Analyzing: {md_file.name}")

        score = validator.validate_entity_boundaries(md_file)
        quality_scores.append(score.quality_score)

        results['summary']['total_entities'] += score.total_entities
        results['summary']['total_issues'] += score.total_issues

        # Categorize by quality
        if score.quality_score >= 90:
            results['summary']['files_by_quality']['excellent'] += 1
        elif score.quality_score >= 75:
            results['summary']['files_by_quality']['good'] += 1
        elif score.quality_score >= 60:
            results['summary']['files_by_quality']['fair'] += 1
        else:
            results['summary']['files_by_quality']['poor'] += 1

        # Track issue types
        for issue_type, count in score.issues_by_type.items():
            results['issue_distribution'][issue_type] += count

        results['file_scores'].append(asdict(score))

    results['summary']['total_files_analyzed'] = len(md_files)
    results['summary']['average_quality_score'] = (
        sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
    )

    # Find worst performing files
    sorted_scores = sorted(results['file_scores'],
                          key=lambda x: x['quality_score'])
    results['worst_files'] = sorted_scores[:10]

    return results


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python entity_boundary_validator.py <file_or_directory> [--sample-size N]")
        sys.exit(1)

    target = Path(sys.argv[1])
    sample_size = 50

    # Parse sample size if provided
    if '--sample-size' in sys.argv:
        idx = sys.argv.index('--sample-size')
        if idx + 1 < len(sys.argv):
            sample_size = int(sys.argv[idx + 1])

    if target.is_file():
        # Analyze single file
        validator = EntityBoundaryValidator()
        score = validator.validate_entity_boundaries(target)

        print(json.dumps(asdict(score), indent=2))

        # Print detailed issues
        if validator.issues:
            print("\n=== Issues Found ===")
            for issue in validator.issues:
                print(f"\nLine {issue.line_number} [{issue.severity.upper()}]:")
                print(f"  Entity: [{issue.entity_type}:{issue.entity_text}]")
                print(f"  Issue: {issue.issue_type}")
                print(f"  Description: {issue.description}")
                print(f"  Context: {issue.context}")

    elif target.is_dir():
        # Batch analyze directory
        results = batch_analyze_directory(target, sample_size)

        # Write results to JSON
        output_file = target / 'entity_validation_results.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\n=== Batch Analysis Results ===")
        print(f"Results written to: {output_file}")
        print(f"\nSummary:")
        print(f"  Files Analyzed: {results['summary']['total_files_analyzed']}")
        print(f"  Total Entities: {results['summary']['total_entities']}")
        print(f"  Total Issues: {results['summary']['total_issues']}")
        print(f"  Average Quality Score: {results['summary']['average_quality_score']:.2f}")
        print(f"\nQuality Distribution:")
        for quality, count in results['summary']['files_by_quality'].items():
            print(f"  {quality.capitalize()}: {count} files")

        print(f"\nTop Issue Types:")
        sorted_issues = sorted(results['issue_distribution'].items(),
                              key=lambda x: x[1], reverse=True)
        for issue_type, count in sorted_issues[:5]:
            print(f"  {issue_type}: {count}")

        print(f"\nWorst Performing Files:")
        for file_score in results['worst_files'][:5]:
            print(f"  {Path(file_score['file_path']).name}: {file_score['quality_score']:.2f}")

    else:
        print(f"Error: {target} is neither a file nor directory")
        sys.exit(1)


if __name__ == '__main__':
    main()
