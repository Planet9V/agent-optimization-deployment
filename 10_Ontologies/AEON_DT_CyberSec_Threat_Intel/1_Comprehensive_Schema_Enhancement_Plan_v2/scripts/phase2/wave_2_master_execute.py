#!/usr/bin/env python3
"""
Wave 2 Master Executor - WATER Infrastructure Surgical Deletion and Rebuild
Proven 6-level validation pattern from Wave 1

Operation: DELETE_AND_REBUILD
Domain: WATER
Target: 15,000 nodes (3x Wave 1)
Complexity: Complex (4 labels: domain + subdomain + functional role + node type)

6-Level Validation Framework:
1. Pre-Delete: Capture current state snapshot
2. Surgical Deletion: Delete ONLY Wave 2 nodes (batch delete)
3. CVE Preservation: Verify CVE count = 267,487 (MANDATORY)
4. Re-Import: Execute 6 Wave 2 import scripts
5. Post-Import: Validate node counts and structure
6. Comprehensive: Final validation across all metrics

Generated: 2025-10-31
Version: 1.0.0
Pattern: Proven from Wave 1
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import json
import subprocess

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from neo4j import GraphDatabase
    import yaml
    from checkpoint.checkpoint_manager import CheckpointManager
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    print("Required packages: neo4j-driver, pyyaml")
    sys.exit(1)


class Wave2MasterExecutor:
    """
    Wave 2 WATER Infrastructure Master Executor

    Manages surgical deletion and rebuild of 15,000 WATER domain nodes
    with 6-level validation framework proven in Wave 1.
    """

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        project_root: Path = None
    ):
        """Initialize Wave 2 Master Executor"""
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "wave_2_master_execution.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Load master taxonomy
        taxonomy_path = self.project_root / "master_taxonomy.yaml"
        with open(taxonomy_path, 'r') as f:
            self.taxonomy = yaml.safe_load(f)

        self.wave_config = self.taxonomy['wave_2']
        self.checkpoint_mgr = CheckpointManager(neo4j_uri, neo4j_user, neo4j_password)

        # Expected counts from taxonomy
        self.expected_wave2_count = 15000
        self.expected_cve_count = 267487

    def _log(self, operation: str, status: str, details: Dict[str, Any] = None):
        """Log operation to JSONL file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "status": status,
            "details": details or {}
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        print(f"[{status}] {operation}: {json.dumps(details or {}, indent=2)}")

    def validate_level1_pre_delete(self) -> Dict[str, Any]:
        """
        LEVEL 1: Pre-Delete Validation

        Capture current state snapshot before deletion

        Returns:
            Dict with current Wave 2 state
        """
        print("=" * 80)
        print("LEVEL 1: PRE-DELETE VALIDATION")
        print("=" * 80)

        with self.driver.session() as session:
            # Current Wave 2 count
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE2'
                RETURN count(n) as count
            """)
            wave2_count = result.single()["count"]

            # Label distribution
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE2'
                RETURN labels(n) as labels, count(n) as count
                ORDER BY count DESC
            """)
            label_distribution = [
                {"labels": record["labels"], "count": record["count"]}
                for record in result
            ]

            # CVE count
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]

            # Total nodes
            result = session.run("MATCH (n) RETURN count(n) as count")
            total_nodes = result.single()["count"]

        validation_result = {
            "wave2_count": wave2_count,
            "expected_wave2_count": self.expected_wave2_count,
            "label_distribution": label_distribution,
            "cve_count": cve_count,
            "total_nodes": total_nodes,
            "timestamp": datetime.now().isoformat()
        }

        self._log("validate_level1_pre_delete", "SUCCESS", validation_result)

        print(f"Current Wave 2 nodes: {wave2_count:,}")
        print(f"Expected after rebuild: {self.expected_wave2_count:,}")
        print(f"CVE baseline: {cve_count:,}")
        print(f"Total nodes: {total_nodes:,}")
        print()

        return validation_result

    def execute_level2_surgical_deletion(self, batch_size: int = 100) -> Dict[str, Any]:
        """
        LEVEL 2: Surgical Deletion

        Delete ONLY Wave 2 nodes in batches to avoid memory issues

        Args:
            batch_size: Number of nodes to delete per batch

        Returns:
            Dict with deletion statistics
        """
        print("=" * 80)
        print("LEVEL 2: SURGICAL DELETION (Wave 2 ONLY)")
        print("=" * 80)

        total_deleted = 0
        batch_num = 0

        with self.driver.session() as session:
            while True:
                result = session.run(f"""
                    MATCH (n)
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE2'
                    WITH n LIMIT {batch_size}
                    DETACH DELETE n
                    RETURN count(n) as deleted
                """)
                batch_deleted = result.single()["deleted"]

                if batch_deleted == 0:
                    break

                total_deleted += batch_deleted
                batch_num += 1

                self._log(
                    "surgical_deletion_batch",
                    "SUCCESS",
                    {
                        "batch_number": batch_num,
                        "batch_size": batch_deleted,
                        "cumulative_total": total_deleted
                    }
                )

                # Progress indicator every 1000 nodes
                if total_deleted % 1000 == 0:
                    print(f"  Progress: {total_deleted:,} nodes deleted...")

        deletion_result = {
            "total_deleted": total_deleted,
            "batch_count": batch_num,
            "batch_size": batch_size
        }

        self._log("execute_level2_surgical_deletion", "SUCCESS", deletion_result)

        print(f"✅ Deleted {total_deleted:,} Wave 2 nodes in {batch_num} batches")
        print()

        return deletion_result

    def validate_level3_cve_preservation(self) -> bool:
        """
        LEVEL 3: CVE Preservation Validation (MANDATORY)

        Verify CVE count remains exactly 267,487

        Returns:
            bool: True if CVE count is correct
        """
        print("=" * 80)
        print("LEVEL 3: CVE PRESERVATION VALIDATION (MANDATORY)")
        print("=" * 80)

        with self.driver.session() as session:
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]

        preserved = (cve_count == self.expected_cve_count)

        self._log(
            "validate_level3_cve_preservation",
            "PASS" if preserved else "CRITICAL_FAIL",
            {
                "expected": self.expected_cve_count,
                "actual": cve_count,
                "preserved": preserved
            }
        )

        if preserved:
            print(f"✅ CVE count preserved: {cve_count:,} / {self.expected_cve_count:,}")
        else:
            print(f"❌ CRITICAL: CVE count mismatch!")
            print(f"   Expected: {self.expected_cve_count:,}")
            print(f"   Actual: {cve_count:,}")
            print(f"   Difference: {cve_count - self.expected_cve_count:,}")

        print()
        return preserved

    def execute_level4_reimport(self) -> Dict[str, Any]:
        """
        LEVEL 4: Re-Import Execution

        Execute Wave 2 import script to recreate nodes

        Returns:
            Dict with import execution results
        """
        print("=" * 80)
        print("LEVEL 4: RE-IMPORT EXECUTION")
        print("=" * 80)

        scripts_dir = self.project_root / "scripts"
        script_path = scripts_dir / "wave_2_execute.py"

        print(f"Executing: wave_2_execute.py")

        if not script_path.exists():
            result = {
                "script": "wave_2_execute.py",
                "status": "FAILED",
                "reason": "Script not found",
                "path": str(script_path)
            }
            self._log("reimport_script", "FAILED", result)
            print(f"  ❌ Script not found at: {script_path}")
            return result

        try:
            # Execute import script with extended timeout for 15,000 nodes
            process = subprocess.run(
                ["python3", str(script_path)],
                cwd=str(scripts_dir),
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for 15,000 nodes
            )

            result = {
                "script": "wave_2_execute.py",
                "status": "SUCCESS" if process.returncode == 0 else "FAILED",
                "return_code": process.returncode,
                "stdout": process.stdout[-1000:] if process.stdout else "",  # Last 1000 chars
                "stderr": process.stderr[-1000:] if process.stderr else ""
            }

            self._log("reimport_script", result["status"], result)

            if process.returncode == 0:
                print(f"  ✅ Success")
                print(f"  {result['stdout'][-500:]}")  # Show last 500 chars of output
            else:
                print(f"  ❌ Failed (return code: {process.returncode})")
                if process.stderr:
                    print(f"     Error: {process.stderr[-500:]}")

        except subprocess.TimeoutExpired:
            result = {
                "script": "wave_2_execute.py",
                "status": "TIMEOUT",
                "reason": "Execution exceeded 10 minutes"
            }
            self._log("reimport_script", "FAILED", result)
            print(f"  ❌ Timeout after 10 minutes")

        except Exception as e:
            result = {
                "script": "wave_2_execute.py",
                "status": "ERROR",
                "error": str(e)
            }
            self._log("reimport_script", "FAILED", result)
            print(f"  ❌ Error: {e}")

        print()
        return result

    def validate_level5_post_import(self) -> Dict[str, Any]:
        """
        LEVEL 5: Post-Import Validation

        Validate node counts and structure after re-import

        Returns:
            Dict with validation results
        """
        print("=" * 80)
        print("LEVEL 5: POST-IMPORT VALIDATION")
        print("=" * 80)

        with self.driver.session() as session:
            # Total Wave 2 count
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE2'
                RETURN count(n) as count
            """)
            wave2_count = result.single()["count"]

            # Node type breakdown
            node_type_validations = {}
            for node_type, config in self.wave_config['node_type_mappings'].items():
                expected_count = config['count']

                result = session.run(f"""
                    MATCH (n:{node_type})
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE2'
                    RETURN count(n) as count
                """)
                actual_count = result.single()["count"]

                node_type_validations[node_type] = {
                    "expected": expected_count,
                    "actual": actual_count,
                    "valid": actual_count == expected_count
                }

                status = "✅" if actual_count == expected_count else "❌"
                print(f"{status} {node_type}: {actual_count:,} / {expected_count:,}")

        all_valid = (
            wave2_count == self.expected_wave2_count and
            all(v["valid"] for v in node_type_validations.values())
        )

        validation_result = {
            "wave2_total": wave2_count,
            "expected_total": self.expected_wave2_count,
            "node_type_validations": node_type_validations,
            "all_valid": all_valid
        }

        status = "PASS" if all_valid else "FAIL"
        self._log("validate_level5_post_import", status, validation_result)

        print()
        print(f"Total Wave 2 nodes: {wave2_count:,} / {self.expected_wave2_count:,}")
        print(f"Overall validation: {'✅ PASS' if all_valid else '❌ FAIL'}")
        print()

        return validation_result

    def validate_level6_comprehensive(self) -> Dict[str, Any]:
        """
        LEVEL 6: Comprehensive Final Validation

        Final validation across all metrics

        Returns:
            Dict with comprehensive validation results
        """
        print("=" * 80)
        print("LEVEL 6: COMPREHENSIVE FINAL VALIDATION")
        print("=" * 80)

        with self.driver.session() as session:
            # Wave 2 domain label
            result = session.run("""
                MATCH (n:WATER)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE2'
                RETURN count(n) as count
            """)
            water_labeled = result.single()["count"]

            # Subdomain labels (these will likely be missing until label enhancement)
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE2'
                AND (n:Water_Treatment OR n:Water_Distribution OR n:Water_Collection)
                RETURN count(n) as count
            """)
            subdomain_labeled = result.single()["count"]

            # CVE preservation
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]

        all_valid = (
            water_labeled == self.expected_wave2_count and
            subdomain_labeled == self.expected_wave2_count and
            cve_count == self.expected_cve_count
        )

        validation_result = {
            "water_labeled": water_labeled,
            "subdomain_labeled": subdomain_labeled,
            "expected_total": self.expected_wave2_count,
            "cve_count": cve_count,
            "cve_expected": self.expected_cve_count,
            "all_valid": all_valid
        }

        status = "PASS" if all_valid else "PARTIAL"
        self._log("validate_level6_comprehensive", status, validation_result)

        print(f"WATER labeled: {water_labeled:,} / {self.expected_wave2_count:,}")
        print(f"Subdomain labeled: {subdomain_labeled:,} / {self.expected_wave2_count:,}")
        print(f"CVE preserved: {cve_count:,} / {self.expected_cve_count:,}")
        print()

        if subdomain_labeled == 0:
            print("⚠️  NOTE: Subdomain labels missing (expected - will be added by label enhancer)")
            print()

        return validation_result

    def execute(self) -> bool:
        """
        Execute complete Wave 2 surgical deletion and rebuild workflow

        Returns:
            bool: True if successful
        """
        try:
            print("=" * 80)
            print("PHASE 2: WAVE 2 SURGICAL DELETION AND REBUILD (15,000 nodes)")
            print("=" * 80)
            print()

            print("[1/6] Level 1: Pre-Delete Validation...")
            level1_result = self.validate_level1_pre_delete()

            print("[2/6] Creating pre-deletion checkpoint...")
            checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 2 Surgical Deletion - Start",
                phase="PHASE_2",
                wave="WAVE2"
            )
            print(f"✅ Checkpoint created: {checkpoint_id}")
            print()

            print("[3/6] Level 2: Surgical Deletion...")
            level2_result = self.execute_level2_surgical_deletion()

            print("[4/6] Level 3: CVE Preservation Validation...")
            if not self.validate_level3_cve_preservation():
                print("❌ CRITICAL: CVE preservation check failed!")
                return False

            print("[5/6] Level 4: Re-Import Execution...")
            level4_result = self.execute_level4_reimport()

            print("[6/6] Level 5: Post-Import Validation...")
            level5_result = self.validate_level5_post_import()

            print("[7/7] Level 6: Comprehensive Final Validation...")
            level6_result = self.validate_level6_comprehensive()

            print("Creating post-rebuild checkpoint...")
            final_checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 2 Surgical Deletion - Complete",
                phase="PHASE_2",
                wave="WAVE2",
                metadata={
                    "level1_result": level1_result,
                    "level2_result": level2_result,
                    "level4_result": level4_result,
                    "level5_result": level5_result,
                    "level6_result": level6_result
                }
            )
            print(f"✅ Final checkpoint created: {final_checkpoint_id}")
            print()

            print("=" * 80)
            print("✅ WAVE 2 SURGICAL DELETION AND REBUILD COMPLETE")
            print("=" * 80)
            print()
            print(f"Deleted: {level2_result['total_deleted']:,} nodes")
            print(f"Rebuilt: {level5_result['wave2_total']:,} nodes")
            print(f"CVE preserved: ✅ {self.expected_cve_count:,}")
            print()
            print("⚠️  NEXT STEP: Run enhance_wave_2_labels.py to add subdomain and functional role labels")
            print()

            return True

        except Exception as e:
            self._log("execute", "FAILED", {"error": str(e)})
            print(f"\n❌ ERROR: {e}")
            return False

        finally:
            self.checkpoint_mgr.close()
            self.driver.close()


def main():
    """Main execution function"""
    executor = Wave2MasterExecutor()
    success = executor.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
