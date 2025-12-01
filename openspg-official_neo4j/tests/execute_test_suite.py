#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
COMPREHENSIVE NEO4J TEST SUITE EXECUTOR
═══════════════════════════════════════════════════════════════════════
File: execute_test_suite.py
Created: 2025-11-28 15:50:00 UTC
Version: v1.0.0
Purpose: Execute comprehensive test suite and generate detailed report
Target: 95%+ pass rate
═══════════════════════════════════════════════════════════════════════
"""

import subprocess
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple

class Neo4jTestExecutor:
    def __init__(self):
        self.container = "openspg-neo4j"
        self.user = "neo4j"
        self.password = "neo4j@openspg"
        self.results = []

    def execute_cypher(self, query: str) -> str:
        """Execute a Cypher query and return results"""
        cmd = [
            "docker", "exec", self.container,
            "cypher-shell", "-u", self.user, "-p", self.password,
            "--format", "plain", query
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout
        except Exception as e:
            return f"ERROR: {str(e)}"

    def parse_test_result(self, output: str) -> Dict:
        """Parse test output into structured result"""
        lines = output.strip().split('\n')
        if len(lines) < 2:
            return {"status": "ERROR", "error": "Invalid output"}

        # Parse header and data
        headers = [h.strip('"') for h in lines[0].split(',')]
        values = [v.strip('"') for v in lines[1].split(',')]

        result = dict(zip(headers, values))
        return result

    def run_test(self, test_id: int, test_query: str) -> Dict:
        """Run a single test and return structured result"""
        print(f"  Executing Test {test_id:03d}...", end=' ')

        output = self.execute_cypher(test_query)
        result = self.parse_test_result(output)

        if result.get('status') == 'PASS':
            print("✓ PASS")
        elif result.get('status') == 'FAIL':
            print("✗ FAIL")
        else:
            print("⚠ ERROR")

        return {
            "test_id": f"TEST_{test_id:03d}",
            "test_name": result.get('test_name', 'Unknown'),
            "test_description": result.get('test_description', ''),
            "expected": result.get('expected_greater_than') or result.get('expected_count') or result.get('expected_result', 'N/A'),
            "actual": result.get('actual_count') or result.get('actual_result', 'N/A'),
            "status": result.get('status', 'ERROR'),
            "query": test_query.strip()[:200] + "..." if len(test_query) > 200 else test_query.strip()
        }

    def load_tests(self, test_file: str) -> List[Tuple[int, str]]:
        """Load test queries from Cypher file"""
        with open(test_file, 'r') as f:
            content = f.read()

        # Split by test comments
        tests = []
        test_pattern = re.compile(r'// TEST (\d+):.*?\n(MATCH.*?;)', re.DOTALL)
        matches = test_pattern.findall(content)

        for test_num, query in matches:
            tests.append((int(test_num), query.strip()))

        return tests

    def generate_report(self, output_file: str):
        """Generate comprehensive test report"""
        # Calculate statistics
        total_tests = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        errors = sum(1 for r in self.results if r['status'] == 'ERROR')
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0

        report = {
            "test_suite": "Neo4j Comprehensive Validation",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "summary": {
                "total_tests": total_tests,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "pass_rate": f"{pass_rate:.2f}%",
                "target_pass_rate": "95%",
                "target_met": pass_rate >= 95.0
            },
            "tests": self.results
        }

        # Save JSON report
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        # Generate markdown report
        md_file = output_file.replace('.json', '.md')
        self.generate_markdown_report(report, md_file)

        return report

    def generate_markdown_report(self, report: Dict, output_file: str):
        """Generate markdown formatted report"""
        md = []
        md.append("# NEO4J COMPREHENSIVE TEST SUITE RESULTS")
        md.append("")
        md.append(f"**Test Suite**: {report['test_suite']}")
        md.append(f"**Timestamp**: {report['timestamp']}")
        md.append("")

        # Summary
        summary = report['summary']
        md.append("## Executive Summary")
        md.append("")
        md.append(f"- **Total Tests**: {summary['total_tests']}")
        md.append(f"- **Passed**: {summary['passed']} ✓")
        md.append(f"- **Failed**: {summary['failed']} ✗")
        md.append(f"- **Errors**: {summary['errors']} ⚠")
        md.append(f"- **Pass Rate**: {summary['pass_rate']}")
        md.append(f"- **Target Pass Rate**: {summary['target_pass_rate']}")
        md.append(f"- **Target Met**: {'YES ✓' if summary['target_met'] else 'NO ✗'}")
        md.append("")

        # Test Details
        md.append("## Test Results")
        md.append("")
        md.append("| Test ID | Test Name | Description | Expected | Actual | Status |")
        md.append("|---------|-----------|-------------|----------|--------|--------|")

        for test in report['tests']:
            status_icon = "✓" if test['status'] == 'PASS' else ("✗" if test['status'] == 'FAIL' else "⚠")
            md.append(f"| {test['test_id']} | {test['test_name']} | {test['test_description']} | {test['expected']} | {test['actual']} | {status_icon} {test['status']} |")

        md.append("")

        # Failed Tests Details
        failed_tests = [t for t in report['tests'] if t['status'] in ['FAIL', 'ERROR']]
        if failed_tests:
            md.append("## Failed/Error Tests Details")
            md.append("")
            for test in failed_tests:
                md.append(f"### {test['test_id']}: {test['test_name']}")
                md.append(f"- **Description**: {test['test_description']}")
                md.append(f"- **Expected**: {test['expected']}")
                md.append(f"- **Actual**: {test['actual']}")
                md.append(f"- **Status**: {test['status']}")
                md.append("")

        # Write markdown file
        with open(output_file, 'w') as f:
            f.write('\n'.join(md))

def main():
    print("═══════════════════════════════════════════════════════════════════════")
    print("NEO4J COMPREHENSIVE TEST SUITE EXECUTOR")
    print("═══════════════════════════════════════════════════════════════════════")
    print()

    executor = Neo4jTestExecutor()

    # Load tests
    test_file = "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/tests/actual_comprehensive_test_suite.cypher"
    print(f"Loading tests from: {test_file}")
    tests = executor.load_tests(test_file)
    print(f"Loaded {len(tests)} tests")
    print()

    # Execute tests
    print("Executing tests:")
    for test_id, query in tests:
        result = executor.run_test(test_id, query)
        executor.results.append(result)

    print()

    # Generate report
    output_file = f"/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/tests/test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    print(f"Generating report: {output_file}")
    report = executor.generate_report(output_file)

    # Print summary
    print()
    print("═══════════════════════════════════════════════════════════════════════")
    print("TEST EXECUTION SUMMARY")
    print("═══════════════════════════════════════════════════════════════════════")
    print(f"Total Tests:     {report['summary']['total_tests']}")
    print(f"Passed:          {report['summary']['passed']} ✓")
    print(f"Failed:          {report['summary']['failed']} ✗")
    print(f"Errors:          {report['summary']['errors']} ⚠")
    print(f"Pass Rate:       {report['summary']['pass_rate']}")
    print(f"Target Met:      {'YES ✓' if report['summary']['target_met'] else 'NO ✗'}")
    print("═══════════════════════════════════════════════════════════════════════")
    print()
    print(f"Detailed reports saved:")
    print(f"  - JSON: {output_file}")
    print(f"  - Markdown: {output_file.replace('.json', '.md')}")
    print()

if __name__ == "__main__":
    main()
