#!/usr/bin/env python3
"""
AEON Path Verification Script

File: verify_paths.py
Created: 2025-11-12 06:50:00 UTC
Modified: 2025-11-12 06:50:00 UTC
Version: 1.0.0
Author: AEON Development Team
Purpose: Verify all file paths, imports, and references before moving/archiving files
Status: ACTIVE
Constitutional Reference: Article II, Section 2.8 (Path Integrity)

USAGE:
    python verify_paths.py [options]

OPTIONS:
    --check-all          Check all paths in entire project
    --check-file FILE    Check specific file for broken references
    --check-dir DIR      Check all files in directory
    --report             Generate detailed report
    --fix                Attempt to fix broken paths (requires confirmation)
    --verbose            Verbose output

EXAMPLES:
    # Check all paths
    python verify_paths.py --check-all

    # Check specific file
    python verify_paths.py --check-file /path/to/file.py

    # Generate report
    python verify_paths.py --check-all --report

    # Fix broken paths
    python verify_paths.py --check-all --fix
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import subprocess

# Project root
PROJECT_ROOT = Path("/home/jim/2_OXOT_Projects_Dev")
WIKI_ROOT = PROJECT_ROOT / "1_AEON_DT_CyberSecurity_Wiki_Current"


@dataclass
class PathIssue:
    """Data class for path issues"""
    file_path: str
    line_number: int
    issue_type: str  # 'broken_import', 'missing_file', 'broken_reference', 'invalid_endpoint'
    severity: str  # 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
    current_path: str
    suggested_fix: str = ""
    context: str = ""


class PathVerifier:
    """Verify all file paths, imports, and references"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.issues: List[PathIssue] = []
        self.checked_files = 0
        self.total_lines = 0

        # Patterns to match
        self.import_patterns = [
            r'from\s+([\w.]+)\s+import',  # Python imports
            r'import\s+([\w.]+)',  # Python imports
            r'require\s*\(\s*["\']([^"\']+)["\']\s*\)',  # Node.js require
            r'from\s+["\']([^"\']+)["\']',  # ES6 imports
        ]

        self.file_ref_patterns = [
            r'["\']([^"\']+\.(py|js|ts|tsx|jsx|json|yaml|yml|md|sql))["\']',  # File references
            r'path\s*=\s*["\']([^"\']+)["\']',  # Path assignments
            r'file\s*=\s*["\']([^"\']+)["\']',  # File assignments
            r'@include\s+([^\s]+)',  # Include directives
        ]

        self.endpoint_patterns = [
            r'["\']/(api/[^"\']+)["\']',  # API endpoints
            r'router\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',  # Express routes
            r'@app\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',  # FastAPI routes
        ]

    def log(self, message: str, level: str = "INFO"):
        """Log message if verbose"""
        if self.verbose or level in ["ERROR", "WARNING"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}")

    def check_file_exists(self, file_path: str, base_dir: str = None) -> bool:
        """Check if file exists"""
        if base_dir:
            full_path = Path(base_dir) / file_path
        else:
            full_path = Path(file_path)

        if full_path.is_absolute():
            return full_path.exists()
        else:
            # Try relative to project root
            return (PROJECT_ROOT / full_path).exists()

    def check_python_imports(self, file_path: Path, content: str) -> List[PathIssue]:
        """Check Python imports"""
        issues = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            for pattern in self.import_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    # Convert module path to file path
                    module_parts = match.split('.')
                    possible_paths = [
                        PROJECT_ROOT / "src" / f"{'/'.join(module_parts)}.py",
                        PROJECT_ROOT / f"{'/'.join(module_parts)}.py",
                        file_path.parent / f"{'/'.join(module_parts)}.py",
                    ]

                    # Check if any possible path exists
                    found = False
                    for possible_path in possible_paths:
                        if possible_path.exists() or (possible_path.parent / "__init__.py").exists():
                            found = True
                            break

                    # Skip built-in and third-party modules
                    if not found and not self._is_builtin_or_third_party(match):
                        issues.append(PathIssue(
                            file_path=str(file_path),
                            line_number=line_num,
                            issue_type="broken_import",
                            severity="HIGH",
                            current_path=match,
                            context=line.strip(),
                            suggested_fix=f"Check if module '{match}' exists or is installed"
                        ))

        return issues

    def _is_builtin_or_third_party(self, module_name: str) -> bool:
        """Check if module is built-in or third-party"""
        builtin_modules = {
            'os', 'sys', 'json', 're', 'datetime', 'pathlib', 'typing', 'dataclasses',
            'subprocess', 'argparse', 'logging', 'time', 'asyncio', 'collections',
            # Add common third-party
            'requests', 'numpy', 'pandas', 'fastapi', 'express', 'react', 'next',
            'spacy', 'torch', 'neo4j', 'psycopg2', 'pymysql', 'qdrant_client'
        }
        return module_name.split('.')[0] in builtin_modules

    def check_file_references(self, file_path: Path, content: str) -> List[PathIssue]:
        """Check file path references"""
        issues = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            for pattern in self.file_ref_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    # match could be tuple (path, extension) or just path
                    ref_path = match[0] if isinstance(match, tuple) else match

                    # Skip URLs and environment variables
                    if ref_path.startswith(('http://', 'https://', '$', '@')):
                        continue

                    # Check if file exists
                    if not self.check_file_exists(ref_path, file_path.parent):
                        issues.append(PathIssue(
                            file_path=str(file_path),
                            line_number=line_num,
                            issue_type="missing_file",
                            severity="HIGH",
                            current_path=ref_path,
                            context=line.strip(),
                            suggested_fix=f"Create file or update path: {ref_path}"
                        ))

        return issues

    def check_api_endpoints(self, file_path: Path, content: str) -> List[PathIssue]:
        """Check API endpoint consistency"""
        issues = []
        lines = content.split('\n')
        declared_endpoints = set()

        # First pass: collect all declared endpoints
        for line_num, line in enumerate(lines, 1):
            for pattern in self.endpoint_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    endpoint = match[1] if isinstance(match, tuple) else match
                    declared_endpoints.add(endpoint)

        # Second pass: check if referenced endpoints exist
        endpoint_refs = re.findall(r'["\']/(api/[^"\']+)["\']', content)
        for ref in endpoint_refs:
            if ref not in declared_endpoints:
                # This might be a reference to an endpoint in another file
                # Flag as low severity for manual review
                issues.append(PathIssue(
                    file_path=str(file_path),
                    line_number=0,  # Can't determine line easily in second pass
                    issue_type="invalid_endpoint",
                    severity="LOW",
                    current_path=ref,
                    context="Endpoint referenced but not found in file",
                    suggested_fix=f"Verify endpoint '{ref}' exists in backend"
                ))

        return issues

    def check_docker_references(self, file_path: Path, content: str) -> List[PathIssue]:
        """Check Docker configuration references"""
        issues = []

        # Check docker-compose.yml references
        if file_path.name in ['docker-compose.yml', 'docker-compose.yaml']:
            # Check volume mounts
            volume_pattern = r'\s*-\s*([^:]+):([^:]+)'
            matches = re.findall(volume_pattern, content)

            for host_path, container_path in matches:
                host_path = host_path.strip()
                if host_path.startswith('./') or host_path.startswith('/'):
                    full_path = Path(host_path) if host_path.startswith('/') else file_path.parent / host_path
                    if not full_path.exists():
                        issues.append(PathIssue(
                            file_path=str(file_path),
                            line_number=0,
                            issue_type="missing_file",
                            severity="MEDIUM",
                            current_path=host_path,
                            context=f"Docker volume mount: {host_path}:{container_path}",
                            suggested_fix=f"Create directory or update volume mount: {host_path}"
                        ))

        return issues

    def check_file(self, file_path: Path) -> List[PathIssue]:
        """Check a single file for path issues"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            self.checked_files += 1
            self.total_lines += len(content.split('\n'))

            issues = []

            # Python files
            if file_path.suffix == '.py':
                issues.extend(self.check_python_imports(file_path, content))
                issues.extend(self.check_file_references(file_path, content))
                issues.extend(self.check_api_endpoints(file_path, content))

            # JavaScript/TypeScript files
            elif file_path.suffix in ['.js', '.ts', '.tsx', '.jsx']:
                issues.extend(self.check_file_references(file_path, content))
                issues.extend(self.check_api_endpoints(file_path, content))

            # Docker files
            elif file_path.name in ['docker-compose.yml', 'docker-compose.yaml', 'Dockerfile']:
                issues.extend(self.check_docker_references(file_path, content))

            # Markdown files
            elif file_path.suffix == '.md':
                issues.extend(self.check_file_references(file_path, content))

            self.log(f"Checked {file_path}: {len(issues)} issues found", "DEBUG")
            return issues

        except Exception as e:
            self.log(f"Error checking {file_path}: {e}", "ERROR")
            return []

    def check_directory(self, directory: Path, recursive: bool = True) -> List[PathIssue]:
        """Check all files in directory"""
        all_issues = []

        if not directory.exists():
            self.log(f"Directory does not exist: {directory}", "ERROR")
            return all_issues

        # File extensions to check
        extensions = {'.py', '.js', '.ts', '.tsx', '.jsx', '.md', '.yml', '.yaml', '.json'}

        pattern = "**/*" if recursive else "*"
        for file_path in directory.glob(pattern):
            if file_path.is_file() and file_path.suffix in extensions:
                # Skip node_modules, venv, .git
                if any(part in file_path.parts for part in ['node_modules', 'venv', '.git', '__pycache__']):
                    continue

                issues = self.check_file(file_path)
                all_issues.extend(issues)
                self.issues.extend(issues)

        return all_issues

    def generate_report(self, output_file: str = None) -> str:
        """Generate detailed report"""
        report_lines = [
            "=" * 80,
            "AEON PATH VERIFICATION REPORT",
            "=" * 80,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"Files Checked: {self.checked_files}",
            f"Total Lines: {self.total_lines:,}",
            f"Issues Found: {len(self.issues)}",
            "",
            "SUMMARY BY SEVERITY:",
            "-" * 80,
        ]

        # Count by severity
        severity_counts = {}
        for issue in self.issues:
            severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1

        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            count = severity_counts.get(severity, 0)
            report_lines.append(f"{severity:10s}: {count:5d}")

        report_lines.extend([
            "",
            "SUMMARY BY ISSUE TYPE:",
            "-" * 80,
        ])

        # Count by issue type
        type_counts = {}
        for issue in self.issues:
            type_counts[issue.issue_type] = type_counts.get(issue.issue_type, 0) + 1

        for issue_type, count in sorted(type_counts.items()):
            report_lines.append(f"{issue_type:20s}: {count:5d}")

        report_lines.extend([
            "",
            "DETAILED ISSUES:",
            "=" * 80,
        ])

        # Group by file
        issues_by_file = {}
        for issue in self.issues:
            if issue.file_path not in issues_by_file:
                issues_by_file[issue.file_path] = []
            issues_by_file[issue.file_path].append(issue)

        for file_path, file_issues in sorted(issues_by_file.items()):
            report_lines.extend([
                "",
                f"FILE: {file_path}",
                "-" * 80,
            ])

            for issue in sorted(file_issues, key=lambda x: x.line_number):
                report_lines.extend([
                    f"  Line {issue.line_number}: [{issue.severity}] {issue.issue_type}",
                    f"    Current: {issue.current_path}",
                    f"    Context: {issue.context}",
                    f"    Fix: {issue.suggested_fix}",
                    ""
                ])

        report_lines.extend([
            "=" * 80,
            "END OF REPORT",
            "=" * 80,
        ])

        report_text = "\n".join(report_lines)

        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            self.log(f"Report written to: {output_file}", "INFO")

        return report_text

    def export_json(self, output_file: str):
        """Export issues as JSON"""
        data = {
            "generated": datetime.now().isoformat(),
            "files_checked": self.checked_files,
            "total_lines": self.total_lines,
            "issues_count": len(self.issues),
            "issues": [asdict(issue) for issue in self.issues]
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        self.log(f"JSON export written to: {output_file}", "INFO")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AEON Path Verification Script - Verify all file paths and references",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --check-all
  %(prog)s --check-file /path/to/file.py
  %(prog)s --check-dir /path/to/directory
  %(prog)s --check-all --report
  %(prog)s --check-all --report --output report.txt
        """
    )

    parser.add_argument('--check-all', action='store_true',
                        help='Check all paths in entire project')
    parser.add_argument('--check-file', type=str,
                        help='Check specific file for broken references')
    parser.add_argument('--check-dir', type=str,
                        help='Check all files in directory')
    parser.add_argument('--report', action='store_true',
                        help='Generate detailed report')
    parser.add_argument('--output', type=str,
                        help='Output file for report (default: stdout)')
    parser.add_argument('--json', type=str,
                        help='Export issues as JSON to specified file')
    parser.add_argument('--verbose', action='store_true',
                        help='Verbose output')
    parser.add_argument('--recursive', action='store_true', default=True,
                        help='Recursive directory checking (default: True)')

    args = parser.parse_args()

    # Create verifier
    verifier = PathVerifier(verbose=args.verbose)

    # Determine what to check
    if args.check_all:
        print("Checking entire project...")
        verifier.check_directory(PROJECT_ROOT, recursive=True)
    elif args.check_file:
        file_path = Path(args.check_file)
        if file_path.exists():
            print(f"Checking file: {file_path}")
            verifier.check_file(file_path)
        else:
            print(f"ERROR: File does not exist: {file_path}")
            sys.exit(1)
    elif args.check_dir:
        dir_path = Path(args.check_dir)
        if dir_path.exists() and dir_path.is_dir():
            print(f"Checking directory: {dir_path}")
            verifier.check_directory(dir_path, recursive=args.recursive)
        else:
            print(f"ERROR: Directory does not exist: {dir_path}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(0)

    # Generate report
    if args.report:
        report = verifier.generate_report(output_file=args.output)
        if not args.output:
            print(report)

    # Export JSON
    if args.json:
        verifier.export_json(args.json)

    # Print summary
    print(f"\n{'=' * 80}")
    print(f"VERIFICATION COMPLETE")
    print(f"{'=' * 80}")
    print(f"Files Checked: {verifier.checked_files}")
    print(f"Total Lines: {verifier.total_lines:,}")
    print(f"Issues Found: {len(verifier.issues)}")

    # Count by severity
    severity_counts = {}
    for issue in verifier.issues:
        severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1

    print(f"\nBy Severity:")
    for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        count = severity_counts.get(severity, 0)
        print(f"  {severity:10s}: {count:5d}")

    # Exit code
    if len(verifier.issues) > 0:
        print(f"\n⚠️  {len(verifier.issues)} path issues found!")
        sys.exit(1)
    else:
        print("\n✅ No path issues found!")
        sys.exit(0)


if __name__ == "__main__":
    main()
