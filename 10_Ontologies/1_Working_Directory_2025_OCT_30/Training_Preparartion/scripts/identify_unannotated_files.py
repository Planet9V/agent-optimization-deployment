#!/usr/bin/env python3
"""
Phase 6 Unannotated File Identifier
Identifies all markdown files with zero entity annotations that should be removed
before NER v5 retraining to prevent wrong negative training.

Context:
- Phase 6 created 526 files
- v4 training showed 75% had 0 annotations
- These files teach model to NOT recognize entities (wrong negatives)
- Expected ~390 files to remove
- All 32 vendor files confirmed to have 0 annotations
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

class UnannotatedFileIdentifier:
    """Identifies files with zero entity annotations in training dataset"""

    def __init__(self, base_path: str):
        """Initialize with base path to Training_Preparation directory"""
        self.base_path = Path(base_path)

        # Entity types from NER pipeline (24 total)
        self.entity_types = [
            # Baseline types (7)
            'VENDOR', 'EQUIPMENT', 'PROTOCOL', 'OPERATION',
            'ARCHITECTURE', 'SECURITY', 'SUPPLIER',
            # Cybersecurity types (17)
            'THREAT_MODEL', 'TACTIC', 'TECHNIQUE', 'ATTACK_PATTERN',
            'VULNERABILITY', 'WEAKNESS', 'INDICATOR', 'THREAT_ACTOR',
            'CAMPAIGN', 'SOFTWARE_COMPONENT', 'HARDWARE_COMPONENT',
            'PERSONALITY_TRAIT', 'COGNITIVE_BIAS', 'INSIDER_INDICATOR',
            'SOCIAL_ENGINEERING', 'ATTACK_VECTOR', 'MITIGATION'
        ]

        # Results storage
        self.files_with_annotations = []
        self.files_without_annotations = []
        self.annotation_counts = defaultdict(int)
        self.sector_stats = defaultdict(lambda: {'total': 0, 'unannotated': 0, 'files': []})

        # Entity pattern regex
        # Pattern: vendor-name-here, VENDOR: "vendor name"
        self.entity_pattern = re.compile(
            r'\{(' + '|'.join(self.entity_types) + r'):\s*"[^"]+"\}'
        )

    def count_annotations(self, file_path: Path) -> int:
        """Count entity annotations in a markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = self.entity_pattern.findall(content)
                return len(matches)
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
            return 0

    def get_sector_name(self, file_path: Path) -> str:
        """Extract sector name from file path"""
        # Path structure: .../SectorName/subdirectory/file.md
        parts = file_path.parts
        base_index = parts.index('Training_Preparartion')
        if base_index + 1 < len(parts):
            return parts[base_index + 1]
        return 'Unknown'

    def is_metadata_file(self, file_path: Path) -> bool:
        """Check if file is metadata (should be skipped)"""
        metadata_names = [
            'COMPLETION_REPORT.md', 'VALIDATION_SUMMARY.md',
            'README.md', 'VALIDATION_REPORT.txt',
            'PHASE_6_COMPLETION_SUMMARY.md'
        ]
        return file_path.name in metadata_names

    def analyze_all_files(self) -> Dict:
        """Analyze all markdown files in training dataset"""
        print("🔍 Analyzing training dataset for unannotated files...")
        print(f"📁 Base path: {self.base_path}")
        print()

        # Find all markdown files
        all_md_files = list(self.base_path.rglob('*.md'))
        print(f"📊 Found {len(all_md_files)} total markdown files")

        # Filter out metadata and venv
        training_files = [
            f for f in all_md_files
            if not self.is_metadata_file(f)
            and 'venv' not in str(f)
            and '.git' not in str(f)
        ]

        print(f"📝 Training files to analyze: {len(training_files)}")
        print()

        # Analyze each file
        for idx, file_path in enumerate(training_files, 1):
            if idx % 50 == 0:
                print(f"   Progress: {idx}/{len(training_files)} files analyzed...")

            annotation_count = self.count_annotations(file_path)
            sector = self.get_sector_name(file_path)

            # Track by sector
            self.sector_stats[sector]['total'] += 1

            if annotation_count == 0:
                self.files_without_annotations.append(str(file_path))
                self.sector_stats[sector]['unannotated'] += 1
                self.sector_stats[sector]['files'].append(file_path.name)
            else:
                self.files_with_annotations.append(str(file_path))
                self.annotation_counts[str(file_path)] = annotation_count

        print(f"✅ Analysis complete!\n")

        return self.generate_report()

    def generate_report(self) -> Dict:
        """Generate comprehensive analysis report"""
        total_files = len(self.files_with_annotations) + len(self.files_without_annotations)
        unannotated_count = len(self.files_without_annotations)
        annotated_count = len(self.files_with_annotations)

        unannotated_percentage = (unannotated_count / total_files * 100) if total_files > 0 else 0

        report = {
            'summary': {
                'total_files_analyzed': total_files,
                'files_with_annotations': annotated_count,
                'files_without_annotations': unannotated_count,
                'unannotated_percentage': round(unannotated_percentage, 2)
            },
            'files_to_remove': self.files_without_annotations,
            'files_to_keep': self.files_with_annotations,
            'sector_breakdown': dict(self.sector_stats)
        }

        return report

    def print_report(self, report: Dict):
        """Print formatted report to console"""
        print("=" * 80)
        print("PHASE 6 UNANNOTATED FILE ANALYSIS REPORT")
        print("=" * 80)
        print()

        summary = report['summary']
        print("📊 SUMMARY")
        print(f"   Total files analyzed: {summary['total_files_analyzed']}")
        print(f"   Files WITH annotations (KEEP): {summary['files_with_annotations']}")
        print(f"   Files WITHOUT annotations (REMOVE): {summary['files_without_annotations']}")
        print(f"   Unannotated percentage: {summary['unannotated_percentage']}%")
        print()

        # Sector breakdown
        print("🏢 SECTOR BREAKDOWN")
        print(f"{'Sector':<30} {'Total':<8} {'Unannotated':<13} {'%':<6}")
        print("-" * 60)

        for sector, stats in sorted(report['sector_breakdown'].items()):
            if stats['total'] > 0:
                percentage = (stats['unannotated'] / stats['total'] * 100)
                print(f"{sector:<30} {stats['total']:<8} {stats['unannotated']:<13} {percentage:>5.1f}%")

        print()

        # Sample files to remove
        print("📝 SAMPLE FILES TO REMOVE (First 10)")
        for idx, file_path in enumerate(report['files_to_remove'][:10], 1):
            print(f"   {idx}. {Path(file_path).name}")
            print(f"      Path: {file_path}")

        if len(report['files_to_remove']) > 10:
            print(f"   ... and {len(report['files_to_remove']) - 10} more files")

        print()

        # Sample files to keep
        print("✅ SAMPLE FILES TO KEEP (First 10)")
        for idx, file_path in enumerate(report['files_to_keep'][:10], 1):
            print(f"   {idx}. {Path(file_path).name}")
            print(f"      Path: {file_path}")

        if len(report['files_to_keep']) > 10:
            print(f"   ... and {len(report['files_to_keep']) - 10} more files")

        print()

        # Validation against expectations
        print("🎯 VALIDATION AGAINST EXPECTATIONS")
        expected_remove = 390  # 75% of 526
        actual_remove = summary['files_without_annotations']
        variance = actual_remove - expected_remove

        print(f"   Expected files to remove: ~{expected_remove}")
        print(f"   Actual files to remove: {actual_remove}")
        print(f"   Variance: {variance:+d} files")

        if 350 <= actual_remove <= 450:
            print("   ✅ Within expected range (±60 files)")
        else:
            print("   ⚠️  Outside expected range - investigate")

        print()

        # Vendor file check
        vendor_files_unannotated = [
            f for f in report['files_to_remove']
            if 'vendor' in f.lower()
        ]
        print(f"🏭 VENDOR FILES WITHOUT ANNOTATIONS: {len(vendor_files_unannotated)}")
        print(f"   Expected: 32 vendor files with 0 annotations")

        if len(vendor_files_unannotated) >= 32:
            print("   ✅ Confirmed: All vendor files have 0 annotations")
        else:
            print("   ⚠️  Some vendor files may have annotations")

        print()
        print("=" * 80)

    def save_file_lists(self, output_dir: Path):
        """Save file lists to text files for manual review"""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Files to remove
        remove_file = output_dir / "V5_FILES_TO_REMOVE.txt"
        with open(remove_file, 'w') as f:
            f.write("# Phase 6 Files to Remove Before v5 Training\n")
            f.write("# These files have ZERO entity annotations\n")
            f.write(f"# Total: {len(self.files_without_annotations)} files\n")
            f.write("# Generated: Phase 2A Task 1 Analysis\n")
            f.write("#\n\n")

            for file_path in sorted(self.files_without_annotations):
                f.write(f"{file_path}\n")

        print(f"✅ Saved: {remove_file}")

        # Files to keep
        keep_file = output_dir / "V5_FILES_TO_KEEP.txt"
        with open(keep_file, 'w') as f:
            f.write("# Phase 6 Files to KEEP for v5 Training\n")
            f.write("# These files have entity annotations\n")
            f.write(f"# Total: {len(self.files_with_annotations)} files\n")
            f.write("# Generated: Phase 2A Task 1 Analysis\n")
            f.write("#\n\n")

            for file_path in sorted(self.files_with_annotations):
                annotations = self.annotation_counts.get(file_path, 0)
                f.write(f"{file_path}  # {annotations} annotations\n")

        print(f"✅ Saved: {keep_file}")

        # JSON report
        json_file = output_dir / "V5_UNANNOTATED_ANALYSIS.json"
        report_data = {
            'summary': {
                'total_files': len(self.files_with_annotations) + len(self.files_without_annotations),
                'files_to_remove': len(self.files_without_annotations),
                'files_to_keep': len(self.files_with_annotations),
                'analysis_date': '2025-11-06',
                'phase': 'Phase 2A Task 1'
            },
            'files_to_remove': self.files_without_annotations,
            'files_to_keep': [
                {'path': path, 'annotation_count': self.annotation_counts.get(path, 0)}
                for path in self.files_with_annotations
            ],
            'sector_stats': self.sector_stats
        }

        with open(json_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"✅ Saved: {json_file}")


def main():
    """Main execution function"""
    base_path = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion")

    # Initialize analyzer
    analyzer = UnannotatedFileIdentifier(str(base_path))

    # Run analysis
    report = analyzer.analyze_all_files()

    # Print report
    analyzer.print_report(report)

    # Save file lists
    output_dir = base_path / "Data Pipeline Builder"
    analyzer.save_file_lists(output_dir)

    print()
    print("🎯 NEXT STEPS:")
    print("   1. Review generated file lists")
    print("   2. Validate sample of files manually")
    print("   3. Proceed to Phase 2A Task 2 (backup and removal)")
    print()


if __name__ == "__main__":
    main()
