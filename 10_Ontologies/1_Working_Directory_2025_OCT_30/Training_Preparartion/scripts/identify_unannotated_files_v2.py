#!/usr/bin/env python3
"""
Phase 6 Unannotated File Identifier v2
Simulates EntityRuler pattern matching to identify files that would generate
ZERO annotations during training.

Context:
- Annotations are NOT embedded in files
- EntityRuler applies patterns DURING training
- Need to simulate pattern matching to find files with 0 matches
- Expected ~390 files (75% of 526) to have 0 annotations
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict

class UnannotatedFileIdentifierV2:
    """Identifies files that generate zero annotations when patterns are applied"""

    def __init__(self, base_path: str):
        """Initialize with base path to Training_Preparation directory"""
        self.base_path = Path(base_path)

        # Load actual patterns from NER training pipeline
        self.patterns = self.load_entity_patterns()

        # Results storage
        self.files_with_annotations = []
        self.files_without_annotations = []
        self.file_annotation_counts = {}
        self.sector_stats = defaultdict(lambda: {'total': 0, 'unannotated': 0, 'files': [], 'annotated_files': []})

    def load_entity_patterns(self) -> Dict[str, List[str]]:
        """Load entity patterns from NER training pipeline"""
        patterns = {
            'VENDOR': [
                "Siemens Energy Automation", "Siemens AG", "Siemens Power Automation", "Siemens",
                "ABB Power Grids", "ABB Automation", "ABB",
                "Schneider Electric", "Schneider",
                "Honeywell Process Solutions", "Honeywell",
                "Rockwell Automation", "Rockwell", "Allen-Bradley",
                "GE Grid Solutions", "GE Digital Energy", "GE",
                "Emerson Process Management", "Emerson",
                "Yokogawa",
                "SEL Schweitzer Engineering", "Schweitzer Engineering Laboratories", "SEL",
                "Mitsubishi Electric", "Mitsubishi",
                "Omron",
                "Cisco Industrial", "Cisco",
                "Palo Alto Networks",
                "Fortinet",
                "Thales",
                "Alstom",
                "Motorola Solutions", "Motorola",
                "Harris Corporation", "Harris",
                "Ericsson",
                "Nokia"
            ],
            'PROTOCOL': [
                "DNP3", "DNP3 Secure Authentication",
                "IEC 61850", "IEC 62443", "IEC 60870",
                "Modbus TCP", "Modbus RTU", "Modbus Plus", "Modbus",
                "NERC CIP",
                "IEEE 1815", "IEEE 1474",
                "NIST SP 800-82",
                "OPC UA", "OPC DA", "OPC",
                "PROFINET IO", "PROFINET RT", "PROFINET",
                "EtherNet/IP",
                "GOOSE", "MMS",
                "ETCS", "CBTC", "PTC",
                "AES-256", "AES-128", "AES",
                "SSL", "TLS", "HTTPS"
            ],
            'SECURITY': [
                "NGFW", "Firewall", "IDS", "IPS",
                "Intrusion Detection", "Intrusion Prevention",
                "Deep Packet Inspection", "DMZ",
                "Electronic Security Perimeter",
                "Access Control",
                "Network Segmentation",
                "Encryption", "Authentication", "Authorization",
                "SIEM", "Zero Trust",
                "Vulnerability Assessment", "Penetration Testing",
                "Security Audit",
                "Cybersecurity", "Cyber Security"
            ],
            'ARCHITECTURE': [
                "Network Architecture", "System Architecture", "Security Architecture",
                "Purdue Model", "DMZ", "VLAN", "VPN", "ESP",
                "Hierarchical Architecture", "Redundant Architecture",
                "Distributed Architecture",
                "Ring Topology", "Star Topology", "Mesh Network",
                "N+1 Redundancy", "Hot Standby", "Cold Standby"
            ],
            'EQUIPMENT': [
                "PLC", "RTU", "HMI", "SCADA",
                "DCS", "SIS", "IED",
                "Programmable Logic Controller",
                "Remote Terminal Unit",
                "Human Machine Interface",
                "Distributed Control System",
                "Safety Instrumented System",
                "Intelligent Electronic Device"
            ],
            'OPERATION': [
                "control", "monitoring", "automation",
                "shutdown", "startup", "emergency",
                "override", "manual", "automatic",
                "setpoint", "alarm", "trip"
            ],
            'THREAT_ACTOR': [
                "APT28", "APT29", "APT33", "APT41",
                "Sandworm", "Volt Typhoon",
                "Lazarus Group", "FIN7",
                "nation-state"
            ],
            'TECHNIQUE': [
                "phishing", "ransomware", "malware",
                "SQL injection", "buffer overflow",
                "man-in-the-middle", "denial of service",
                "privilege escalation", "lateral movement"
            ]
        }
        return patterns

    def count_pattern_matches(self, file_path: Path) -> int:
        """Count how many entity patterns would match in this file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            total_matches = 0
            entity_breakdown = {}

            # Check each entity type's patterns
            for entity_type, pattern_list in self.patterns.items():
                matches_for_type = 0
                for pattern in pattern_list:
                    # Case-insensitive pattern matching
                    matches = len(re.findall(re.escape(pattern), content, re.IGNORECASE))
                    matches_for_type += matches

                if matches_for_type > 0:
                    entity_breakdown[entity_type] = matches_for_type
                total_matches += matches_for_type

            return total_matches

        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
            return 0

    def get_sector_name(self, file_path: Path) -> str:
        """Extract sector name from file path"""
        parts = file_path.parts
        try:
            base_index = parts.index('Training_Preparartion')
            if base_index + 1 < len(parts):
                return parts[base_index + 1]
        except ValueError:
            pass
        return 'Unknown'

    def is_metadata_file(self, file_path: Path) -> bool:
        """Check if file is metadata (should be skipped)"""
        metadata_names = [
            'COMPLETION_REPORT.md', 'VALIDATION_SUMMARY.md',
            'README.md', 'VALIDATION_REPORT.txt',
            'PHASE_6_COMPLETION_SUMMARY.md',
            'PHASE_4_VALIDATION_AND_RETRAINING_REPORT.md',
            'PHASE_5_VALIDATION_SUMMARY.md'
        ]
        return file_path.name in metadata_names

    def analyze_all_files(self) -> Dict:
        """Analyze all markdown files by simulating pattern matching"""
        print("🔍 Analyzing training dataset with pattern matching simulation...")
        print(f"📁 Base path: {self.base_path}")
        print(f"🎯 Loaded {sum(len(p) for p in self.patterns.values())} total patterns")
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

            match_count = self.count_pattern_matches(file_path)
            sector = self.get_sector_name(file_path)

            # Track by sector
            self.sector_stats[sector]['total'] += 1

            if match_count == 0:
                self.files_without_annotations.append(str(file_path))
                self.sector_stats[sector]['unannotated'] += 1
                self.sector_stats[sector]['files'].append(file_path.name)
            else:
                self.files_with_annotations.append(str(file_path))
                self.file_annotation_counts[str(file_path)] = match_count
                self.sector_stats[sector]['annotated_files'].append(file_path.name)

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
            'sector_breakdown': dict(self.sector_stats),
            'annotation_counts': self.file_annotation_counts
        }

        return report

    def print_report(self, report: Dict):
        """Print formatted report to console"""
        print("=" * 80)
        print("PHASE 6 UNANNOTATED FILE ANALYSIS REPORT v2")
        print("(Using Pattern Matching Simulation)")
        print("=" * 80)
        print()

        summary = report['summary']
        print("📊 SUMMARY")
        print(f"   Total files analyzed: {summary['total_files_analyzed']}")
        print(f"   Files WITH pattern matches (KEEP): {summary['files_with_annotations']}")
        print(f"   Files WITHOUT pattern matches (REMOVE): {summary['files_without_annotations']}")
        print(f"   Unannotated percentage: {summary['unannotated_percentage']}%")
        print()

        # Sector breakdown
        print("🏢 SECTOR BREAKDOWN")
        print(f"{'Sector':<35} {'Total':<8} {'Unannotated':<13} {'%':<6}")
        print("-" * 70)

        for sector, stats in sorted(report['sector_breakdown'].items()):
            if stats['total'] > 0:
                percentage = (stats['unannotated'] / stats['total'] * 100)
                print(f"{sector:<35} {stats['total']:<8} {stats['unannotated']:<13} {percentage:>5.1f}%")

        print()

        # Sample files to remove
        print("📝 SAMPLE FILES TO REMOVE (First 10)")
        for idx, file_path in enumerate(report['files_to_remove'][:10], 1):
            print(f"   {idx}. {Path(file_path).name}")

        if len(report['files_to_remove']) > 10:
            print(f"   ... and {len(report['files_to_remove']) - 10} more files")

        print()

        # Sample files to keep with annotation counts
        print("✅ SAMPLE FILES TO KEEP (First 10 with annotation counts)")
        for idx, file_path in enumerate(report['files_to_keep'][:10], 1):
            count = report['annotation_counts'].get(file_path, 0)
            print(f"   {idx}. {Path(file_path).name} ({count} pattern matches)")

        if len(report['files_to_keep']) > 10:
            print(f"   ... and {len(report['files_to_keep']) - 10} more files")

        print()

        # Validation against expectations
        print("🎯 VALIDATION AGAINST EXPECTATIONS")
        expected_remove = 390  # 75% of 526
        actual_remove = summary['files_without_annotations']
        variance = actual_remove - expected_remove

        print(f"   Expected files to remove: ~{expected_remove} (75% of 526)")
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
            if 'vendor' in Path(f).name.lower() or 'vendor' in str(f).lower()
        ]
        print(f"🏭 VENDOR FILES WITHOUT PATTERN MATCHES: {len(vendor_files_unannotated)}")
        print(f"   Expected: ~32 vendor files with 0 annotations")

        if len(vendor_files_unannotated) >= 30:
            print("   ✅ Confirmed: Most vendor files have 0 pattern matches")
        else:
            print("   ℹ️  Vendor files may have some pattern matches")

        # Show sample vendor files
        if vendor_files_unannotated:
            print(f"\n   Sample vendor files to remove:")
            for vf in vendor_files_unannotated[:5]:
                print(f"      - {Path(vf).name}")

        print()
        print("=" * 80)

    def save_file_lists(self, output_dir: Path):
        """Save file lists to text files for manual review"""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Files to remove
        remove_file = output_dir / "V5_FILES_TO_REMOVE.txt"
        with open(remove_file, 'w') as f:
            f.write("# Phase 6 Files to Remove Before v5 Training\n")
            f.write("# These files have ZERO pattern matches (would generate 0 annotations)\n")
            f.write(f"# Total: {len(self.files_without_annotations)} files\n")
            f.write("# Analysis Method: Pattern Matching Simulation\n")
            f.write("# Generated: Phase 2A Task 1 Analysis v2\n")
            f.write("#\n\n")

            for file_path in sorted(self.files_without_annotations):
                f.write(f"{file_path}\n")

        print(f"✅ Saved: {remove_file}")

        # Files to keep
        keep_file = output_dir / "V5_FILES_TO_KEEP.txt"
        with open(keep_file, 'w') as f:
            f.write("# Phase 6 Files to KEEP for v5 Training\n")
            f.write("# These files have pattern matches (would generate annotations)\n")
            f.write(f"# Total: {len(self.files_with_annotations)} files\n")
            f.write("# Analysis Method: Pattern Matching Simulation\n")
            f.write("# Generated: Phase 2A Task 1 Analysis v2\n")
            f.write("#\n\n")

            for file_path in sorted(self.files_with_annotations):
                match_count = self.file_annotation_counts.get(file_path, 0)
                f.write(f"{file_path}  # {match_count} pattern matches\n")

        print(f"✅ Saved: {keep_file}")

        # JSON report
        json_file = output_dir / "V5_UNANNOTATED_ANALYSIS.json"
        report_data = {
            'summary': {
                'total_files': len(self.files_with_annotations) + len(self.files_without_annotations),
                'files_to_remove': len(self.files_without_annotations),
                'files_to_keep': len(self.files_with_annotations),
                'analysis_method': 'pattern_matching_simulation',
                'analysis_date': '2025-11-06',
                'phase': 'Phase 2A Task 1 v2'
            },
            'files_to_remove': self.files_without_annotations,
            'files_to_keep': [
                {'path': path, 'pattern_matches': self.file_annotation_counts.get(path, 0)}
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
    analyzer = UnannotatedFileIdentifierV2(str(base_path))

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
    print("   2. Validate sample files manually")
    print("   3. Verify vendor files have 0 matches")
    print("   4. Proceed to Phase 2A Task 2 (backup and removal)")
    print()


if __name__ == "__main__":
    main()
