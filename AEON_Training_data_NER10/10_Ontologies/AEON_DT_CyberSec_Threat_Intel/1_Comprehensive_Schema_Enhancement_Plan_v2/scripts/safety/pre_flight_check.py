#!/usr/bin/env python3
"""
Pre-Flight Safety Check for Neo4j Ontology Operations
Validates system state before any task execution

Generated: 2025-10-31
Version: 1.0.0
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Tuple
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from neo4j import GraphDatabase
    from qdrant_client import QdrantClient
    import yaml
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    print("Required packages: neo4j-driver, qdrant-client, pyyaml")
    sys.exit(1)


class PreFlightCheck:
    """Pre-flight safety validation before task execution"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        qdrant_api_key: str = "deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=",
        project_root: Path = None
    ):
        """
        Initialize pre-flight check manager

        Args:
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
            qdrant_host: Qdrant server host
            qdrant_port: Qdrant server port
            qdrant_api_key: Qdrant API key
            project_root: Project root directory path
        """
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.qdrant_host = qdrant_host
        self.qdrant_port = qdrant_port
        self.qdrant_api_key = qdrant_api_key

        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "pre_flight_checks.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Initialize clients (will be set during connectivity checks)
        self.neo4j_driver = None
        self.qdrant_client = None

    def _log(self, check_name: str, status: str, details: Dict[str, Any] = None):
        """Log check result to JSONL file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "check": check_name,
            "status": status,
            "details": details or {}
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def check_neo4j_connectivity(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Check Neo4j database connectivity

        Returns:
            Tuple of (success: bool, details: dict)
        """
        try:
            self.neo4j_driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password)
            )

            # Test connection with simple query
            with self.neo4j_driver.session() as session:
                result = session.run("RETURN 1 as test")
                test_value = result.single()["test"]

                if test_value != 1:
                    raise Exception("Test query returned unexpected value")

            details = {
                "uri": self.neo4j_uri,
                "connected": True
            }
            self._log("neo4j_connectivity", "PASS", details)
            return True, details

        except Exception as e:
            details = {
                "uri": self.neo4j_uri,
                "connected": False,
                "error": str(e)
            }
            self._log("neo4j_connectivity", "FAIL", details)
            return False, details

    def check_cve_baseline(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Verify CVE baseline integrity (MANDATORY: 267,487 nodes)

        Returns:
            Tuple of (success: bool, details: dict)
        """
        try:
            if not self.neo4j_driver:
                raise Exception("Neo4j connection not established")

            with self.neo4j_driver.session() as session:
                result = session.run("""
                    MATCH (n:CVE)
                    RETURN count(n) as cve_count
                """)
                cve_count = result.single()["cve_count"]

            expected_count = 267487
            status = "PASS" if cve_count == expected_count else "FAIL"

            details = {
                "expected": expected_count,
                "actual": cve_count,
                "variance": cve_count - expected_count,
                "integrity": "INTACT" if cve_count == expected_count else "COMPROMISED"
            }

            self._log("cve_baseline_integrity", status, details)
            return (cve_count == expected_count), details

        except Exception as e:
            details = {
                "expected": 267487,
                "actual": None,
                "error": str(e)
            }
            self._log("cve_baseline_integrity", "FAIL", details)
            return False, details

    def check_qdrant_connectivity(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Check Qdrant vector database connectivity

        Returns:
            Tuple of (success: bool, details: dict)
        """
        try:
            self.qdrant_client = QdrantClient(
                host=self.qdrant_host,
                port=self.qdrant_port,
                api_key=self.qdrant_api_key,
                https=False,
                prefer_grpc=False
            )

            # Test connection by listing collections
            collections = self.qdrant_client.get_collections().collections
            collection_names = [c.name for c in collections]

            required_collections = ["ontology_checkpoints", "operation_logs"]
            missing_collections = [
                c for c in required_collections if c not in collection_names
            ]

            success = len(missing_collections) == 0

            details = {
                "host": self.qdrant_host,
                "port": self.qdrant_port,
                "connected": True,
                "collections_found": collection_names,
                "required_collections": required_collections,
                "missing_collections": missing_collections
            }

            status = "PASS" if success else "FAIL"
            self._log("qdrant_connectivity", status, details)
            return success, details

        except Exception as e:
            details = {
                "host": self.qdrant_host,
                "port": self.qdrant_port,
                "connected": False,
                "error": str(e)
            }
            self._log("qdrant_connectivity", "FAIL", details)
            return False, details

    def check_master_taxonomy(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Verify master taxonomy file exists and is valid

        Returns:
            Tuple of (success: bool, details: dict)
        """
        try:
            taxonomy_path = self.project_root / "master_taxonomy.yaml"

            if not taxonomy_path.exists():
                raise FileNotFoundError(f"Master taxonomy not found at {taxonomy_path}")

            # Load and validate structure
            with open(taxonomy_path, 'r') as f:
                taxonomy = yaml.safe_load(f)

            # Check for required top-level keys
            required_keys = [
                "strategy",
                "cve_enhancement",
                "wave_1", "wave_2", "wave_3", "wave_4",
                "wave_5", "wave_6", "wave_7", "wave_8",
                "wave_9", "wave_10", "wave_11", "wave_12",
                "index_strategy",
                "consistency_rules",
                "validation_framework"
            ]

            missing_keys = [k for k in required_keys if k not in taxonomy]

            success = len(missing_keys) == 0

            details = {
                "file_path": str(taxonomy_path),
                "file_exists": True,
                "required_keys": required_keys,
                "missing_keys": missing_keys,
                "valid": success
            }

            status = "PASS" if success else "FAIL"
            self._log("master_taxonomy_check", status, details)
            return success, details

        except Exception as e:
            details = {
                "file_path": str(self.project_root / "master_taxonomy.yaml"),
                "file_exists": False,
                "error": str(e)
            }
            self._log("master_taxonomy_check", "FAIL", details)
            return False, details

    def check_wave_integrity(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Check Wave 9-12 integrity (must be intact for Phase 1)

        Returns:
            Tuple of (success: bool, details: dict)
        """
        try:
            if not self.neo4j_driver:
                raise Exception("Neo4j connection not established")

            with self.neo4j_driver.session() as session:
                result = session.run("""
                    MATCH (n)
                    WHERE n.created_by IN [
                        'AEON_INTEGRATION_WAVE9',
                        'AEON_INTEGRATION_WAVE10',
                        'AEON_INTEGRATION_WAVE11',
                        'AEON_INTEGRATION_WAVE12'
                    ]
                    RETURN n.created_by as wave, count(n) as count
                    ORDER BY wave
                """)

                wave_counts = {record["wave"]: record["count"] for record in result}

            expected_counts = {
                "AEON_INTEGRATION_WAVE9": 5000,
                "AEON_INTEGRATION_WAVE10": 140000,
                "AEON_INTEGRATION_WAVE11": 4000,
                "AEON_INTEGRATION_WAVE12": 4000
            }

            all_correct = all(
                wave_counts.get(wave, 0) == expected
                for wave, expected in expected_counts.items()
            )

            details = {
                "expected": expected_counts,
                "actual": wave_counts,
                "total_expected": sum(expected_counts.values()),
                "total_actual": sum(wave_counts.values()),
                "integrity": "INTACT" if all_correct else "COMPROMISED"
            }

            status = "PASS" if all_correct else "FAIL"
            self._log("wave_9_12_integrity", status, details)
            return all_correct, details

        except Exception as e:
            details = {"error": str(e)}
            self._log("wave_9_12_integrity", "FAIL", details)
            return False, details

    def run_all_checks(self) -> Dict[str, Any]:
        """
        Execute all pre-flight checks

        Returns:
            Dict with overall status and individual check results
        """
        print("=" * 80)
        print("PRE-FLIGHT SAFETY CHECK")
        print("=" * 80)
        print()

        checks = []

        # Check 1: Neo4j Connectivity
        print("[1/5] Checking Neo4j connectivity...")
        neo4j_ok, neo4j_details = self.check_neo4j_connectivity()
        checks.append(("Neo4j Connectivity", neo4j_ok, neo4j_details, True))
        print(f"  {'✅ PASS' if neo4j_ok else '❌ FAIL'}: {neo4j_details}")
        print()

        # Check 2: CVE Baseline (CRITICAL)
        print("[2/5] Verifying CVE baseline integrity...")
        cve_ok, cve_details = self.check_cve_baseline()
        checks.append(("CVE Baseline", cve_ok, cve_details, True))
        print(f"  {'✅ PASS' if cve_ok else '❌ CRITICAL FAIL'}: {cve_details}")
        print()

        # Check 3: Qdrant Connectivity
        print("[3/5] Checking Qdrant connectivity...")
        qdrant_ok, qdrant_details = self.check_qdrant_connectivity()
        checks.append(("Qdrant Connectivity", qdrant_ok, qdrant_details, True))
        print(f"  {'✅ PASS' if qdrant_ok else '❌ FAIL'}: {qdrant_details}")
        print()

        # Check 4: Master Taxonomy
        print("[4/5] Validating master taxonomy...")
        taxonomy_ok, taxonomy_details = self.check_master_taxonomy()
        checks.append(("Master Taxonomy", taxonomy_ok, taxonomy_details, True))
        print(f"  {'✅ PASS' if taxonomy_ok else '❌ FAIL'}: {taxonomy_details}")
        print()

        # Check 5: Wave 9-12 Integrity
        print("[5/5] Checking Wave 9-12 integrity...")
        wave_ok, wave_details = self.check_wave_integrity()
        checks.append(("Wave 9-12 Integrity", wave_ok, wave_details, False))
        print(f"  {'✅ PASS' if wave_ok else '⚠️  WARNING'}: {wave_details}")
        print()

        # Summary
        critical_checks = [(name, passed) for name, passed, _, critical in checks if critical]
        all_critical_passed = all(passed for _, passed in critical_checks)
        all_checks_passed = all(passed for _, passed, _, _ in checks)

        print("=" * 80)
        if all_critical_passed:
            print("✅ PRE-FLIGHT CHECK: PASSED (all critical checks)")
        else:
            print("❌ PRE-FLIGHT CHECK: FAILED (critical check failed)")
        print("=" * 80)
        print()

        summary = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "PASS" if all_critical_passed else "FAIL",
            "all_checks_passed": all_checks_passed,
            "critical_checks_passed": all_critical_passed,
            "checks": [
                {
                    "name": name,
                    "passed": passed,
                    "critical": critical,
                    "details": details
                }
                for name, passed, details, critical in checks
            ],
            "log_file": str(self.log_file)
        }

        # Close connections
        if self.neo4j_driver:
            self.neo4j_driver.close()

        return summary


def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run pre-flight safety checks before Neo4j operations"
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    # Run checks
    checker = PreFlightCheck()
    summary = checker.run_all_checks()

    if args.json_output:
        print(json.dumps(summary, indent=2))

    # Exit with appropriate code
    sys.exit(0 if summary["critical_checks_passed"] else 1)


if __name__ == "__main__":
    main()
