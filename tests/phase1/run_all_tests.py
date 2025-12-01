"""
Phase 1 Test Runner and Results Matrix Generator
Executes all Phase 1 tests and generates comprehensive results
"""

import pytest
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import subprocess

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class Phase1TestRunner:
    """Orchestrates Phase 1 test execution and reporting"""

    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "phase": "Phase 1 - McKenney-Lacan Gap Closure",
            "gaps": {
                "ML-004": {"name": "Temporal Versioning", "tests": []},
                "ML-005": {"name": "WebSocket EWS", "tests": []},
                "ML-010": {"name": "Cascade Tracking", "tests": []},
                "ML-011": {"name": "Batch Prediction", "tests": []},
                "Integration": {"name": "Phase 1 Integration", "tests": []}
            },
            "summary": {},
            "overall_status": "PENDING"
        }

    def run_test_file(self, test_file: Path, gap_id: str) -> Dict[str, Any]:
        """Run a single test file and capture results"""
        print(f"\n{'='*80}")
        print(f"Running {test_file.name}...")
        print(f"{'='*80}\n")

        # Run pytest with JSON report
        cmd = [
            "pytest",
            str(test_file),
            "-v",
            "--tb=short",
            "--json-report",
            f"--json-report-file={test_file.stem}_report.json"
        ]

        result = subprocess.run(
            cmd,
            cwd=self.test_dir,
            capture_output=True,
            text=True
        )

        # Parse JSON report
        report_file = self.test_dir / f"{test_file.stem}_report.json"
        if report_file.exists():
            with open(report_file) as f:
                report = json.load(f)

            # Extract test results
            for test in report.get("tests", []):
                test_result = {
                    "name": test["nodeid"].split("::")[-1],
                    "status": test["outcome"],
                    "duration": test.get("duration", 0),
                    "error": test.get("call", {}).get("longrepr") if test["outcome"] == "failed" else None
                }
                self.results["gaps"][gap_id]["tests"].append(test_result)

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def run_all_tests(self):
        """Execute all Phase 1 tests"""
        test_files = [
            ("test_ml004_temporal_versioning.py", "ML-004"),
            ("test_ml005_websocket_ews.py", "ML-005"),
            ("test_ml010_cascade_tracking.py", "ML-010"),
            ("test_ml011_batch_prediction.py", "ML-011"),
            ("test_phase1_integration.py", "Integration")
        ]

        for test_file, gap_id in test_files:
            file_path = self.test_dir / test_file
            if file_path.exists():
                self.run_test_file(file_path, gap_id)
            else:
                print(f"Warning: {test_file} not found")

        self._calculate_summary()

    def _calculate_summary(self):
        """Calculate test summary statistics"""
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        total_duration = 0

        for gap_id, gap_data in self.results["gaps"].items():
            gap_total = len(gap_data["tests"])
            gap_passed = sum(1 for t in gap_data["tests"] if t["status"] == "passed")
            gap_failed = sum(1 for t in gap_data["tests"] if t["status"] == "failed")
            gap_duration = sum(t["duration"] for t in gap_data["tests"])

            total_tests += gap_total
            passed_tests += gap_passed
            failed_tests += gap_failed
            total_duration += gap_duration

            self.results["gaps"][gap_id]["summary"] = {
                "total": gap_total,
                "passed": gap_passed,
                "failed": gap_failed,
                "pass_rate": (gap_passed / gap_total * 100) if gap_total > 0 else 0,
                "duration": gap_duration
            }

        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_duration": total_duration
        }

        self.results["overall_status"] = "PASS" if failed_tests == 0 else "FAIL"

    def generate_results_matrix(self) -> str:
        """Generate comprehensive results matrix"""
        matrix = []
        matrix.append("\n" + "="*100)
        matrix.append("PHASE 1 TEST RESULTS MATRIX")
        matrix.append("="*100 + "\n")

        # Overall summary
        matrix.append(f"Overall Status: {self.results['overall_status']}")
        matrix.append(f"Total Tests: {self.results['summary']['total_tests']}")
        matrix.append(f"Passed: {self.results['summary']['passed']}")
        matrix.append(f"Failed: {self.results['summary']['failed']}")
        matrix.append(f"Pass Rate: {self.results['summary']['pass_rate']:.1f}%")
        matrix.append(f"Total Duration: {self.results['summary']['total_duration']:.2f}s\n")

        # Gap-by-gap breakdown
        for gap_id, gap_data in self.results["gaps"].items():
            matrix.append(f"\n{'-'*100}")
            matrix.append(f"{gap_id}: {gap_data['name']}")
            matrix.append(f"{'-'*100}")

            summary = gap_data.get("summary", {})
            matrix.append(f"Tests: {summary.get('total', 0)} | " +
                         f"Passed: {summary.get('passed', 0)} | " +
                         f"Failed: {summary.get('failed', 0)} | " +
                         f"Pass Rate: {summary.get('pass_rate', 0):.1f}%\n")

            # Individual test results
            for test in gap_data["tests"]:
                status_symbol = "✓" if test["status"] == "passed" else "✗"
                matrix.append(f"  {status_symbol} {test['name']} ({test['duration']:.3f}s)")
                if test["error"]:
                    matrix.append(f"    Error: {test['error'][:200]}...")

        matrix.append("\n" + "="*100 + "\n")

        return "\n".join(matrix)

    def save_results(self):
        """Save results to JSON and text files"""
        # JSON results
        json_file = self.test_dir / "phase1_test_results.json"
        with open(json_file, "w") as f:
            json.dump(self.results, f, indent=2)

        # Text matrix
        matrix = self.generate_results_matrix()
        text_file = self.test_dir / "phase1_test_results.txt"
        with open(text_file, "w") as f:
            f.write(matrix)

        print(matrix)
        print(f"\nResults saved to:")
        print(f"  - {json_file}")
        print(f"  - {text_file}")

    def prepare_qdrant_document(self) -> Dict[str, Any]:
        """Prepare results for Qdrant storage"""
        return {
            "document_type": "test_results",
            "phase": "phase1",
            "timestamp": self.results["timestamp"],
            "overall_status": self.results["overall_status"],
            "summary": self.results["summary"],
            "gap_summaries": {
                gap_id: {
                    "name": gap_data["name"],
                    "summary": gap_data.get("summary", {}),
                    "test_count": len(gap_data["tests"])
                }
                for gap_id, gap_data in self.results["gaps"].items()
            },
            "detailed_results": self.results["gaps"],
            "metadata": {
                "generated_by": "Phase1TestRunner",
                "test_framework": "pytest",
                "phase_description": "McKenney-Lacan Gap Closure - ML-004, ML-005, ML-010, ML-011"
            }
        }


def main():
    """Main execution function"""
    runner = Phase1TestRunner()

    print("\n" + "="*100)
    print("PHASE 1 TEST SUITE - MCKENNEY-LACAN GAP CLOSURE")
    print("="*100 + "\n")
    print("Testing Gaps:")
    print("  - ML-004: Temporal Versioning")
    print("  - ML-005: WebSocket Early Warning System")
    print("  - ML-010: Cascade Tracking")
    print("  - ML-011: Batch Prediction")
    print("  - Integration: Complete workflow\n")

    runner.run_all_tests()
    runner.save_results()

    # Prepare Qdrant document
    qdrant_doc = runner.prepare_qdrant_document()
    qdrant_file = runner.test_dir / "phase1_qdrant_document.json"
    with open(qdrant_file, "w") as f:
        json.dump(qdrant_doc, f, indent=2)

    print(f"\nQdrant document prepared: {qdrant_file}")
    print("\nTo store in Qdrant, run:")
    print(f"  python scripts/store_to_qdrant.py {qdrant_file} phase1-test-results")

    # Exit with appropriate code
    sys.exit(0 if runner.results["overall_status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
