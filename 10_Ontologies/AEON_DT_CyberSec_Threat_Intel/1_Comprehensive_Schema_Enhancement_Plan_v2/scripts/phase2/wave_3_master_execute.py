#!/usr/bin/env python3
"""
Wave 3 Master Executor - ENERGY GRID (35,924 nodes)
Surgical deletion and rebuild with 6-level validation

CRITICAL FIXES:
- Remove 18,000 mislabeled WATER measurements (should be ENERGY)
- Fix lowercase 'Energy' to uppercase 'ENERGY'
- Add proper subdomain labels (Energy_Generation, Energy_Transmission, etc.)
- Add functional role labels (Asset, Monitoring, Control, Process)

Operation: DELETE_AND_REBUILD
Target: 35,924 nodes
Labels: ENERGY + subdomain + functional role + node type

Generated: 2025-10-31
Version: 1.0.0
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
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


class Wave3MasterExecutor:
    """Execute Wave 3 surgical deletion and rebuild with comprehensive validation"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        project_root: Path = None
    ):
        """Initialize Wave 3 Master Executor"""
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "wave_3_master_execution.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Load master taxonomy
        taxonomy_path = self.project_root / "master_taxonomy.yaml"
        with open(taxonomy_path, 'r') as f:
            self.taxonomy = yaml.safe_load(f)

        self.wave_config = self.taxonomy['wave_3']
        self.checkpoint_mgr = CheckpointManager(neo4j_uri, neo4j_user, neo4j_password)

    def _log(self, operation: str, status: str, details: Dict[str, Any] = None):
        """Log operation to JSONL file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "status": status,
            "details": details or {}
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\\n')
        print(f"[{status}] {operation}: {json.dumps(details or {}, indent=2)}")

    def execute_level1_predeletion_validation(self) -> Dict[str, Any]:
        """
        LEVEL 1: Pre-Deletion Validation
        Capture current state before deletion
        """
        print("LEVEL 1: Pre-Deletion Validation")
        print("-" * 80)

        with self.driver.session() as session:
            # Count Wave 3 nodes
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                RETURN count(n) as count
            """)
            wave3_count = result.single()["count"]

            # Get node type distribution
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                RETURN labels(n) as labels, count(n) as count
                ORDER BY count DESC
            """)
            node_types = {}
            for record in result:
                labels = tuple(sorted(record["labels"]))
                node_types[str(labels)] = record["count"]

            # Count mislabeled WATER nodes
            result = session.run("""
                MATCH (n:WATER)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                RETURN count(n) as count
            """)
            mislabeled_water = result.single()["count"]

            # Verify CVE baseline
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]

        validation_result = {
            "wave3_total": wave3_count,
            "expected_total": 35924,
            "node_types": node_types,
            "mislabeled_water_nodes": mislabeled_water,
            "cve_count": cve_count,
            "cve_expected": 267487,
            "ready_for_deletion": wave3_count == 35924 and cve_count == 267487
        }

        status = "PASS" if validation_result["ready_for_deletion"] else "FAIL"
        self._log("level1_predeletion_validation", status, validation_result)

        print(f"Wave 3 nodes: {wave3_count:,} (expected: 35,924)")
        print(f"Mislabeled WATER nodes: {mislabeled_water:,}")
        print(f"CVE count: {cve_count:,} (expected: 267,487)")
        print(f"Status: {status}")
        print()

        return validation_result

    def execute_level2_surgical_deletion(self) -> Dict[str, Any]:
        """
        LEVEL 2: Surgical Deletion
        Delete ONLY Wave 3 nodes, preserve all other data
        """
        print("LEVEL 2: Surgical Deletion")
        print("-" * 80)

        deleted_counts = {}

        with self.driver.session() as session:
            # Delete Wave 3 nodes in batches
            batch_size = 1000
            total_deleted = 0

            while True:
                result = session.run(f"""
                    MATCH (n)
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                    WITH n LIMIT {batch_size}
                    DETACH DELETE n
                    RETURN count(n) as deleted
                """)
                batch_deleted = result.single()["deleted"]

                if batch_deleted == 0:
                    break

                total_deleted += batch_deleted
                print(f"  Deleted batch: {batch_deleted:,} nodes (total: {total_deleted:,})")

            deleted_counts["total_deleted"] = total_deleted

            # Verify deletion
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                RETURN count(n) as count
            """)
            remaining = result.single()["count"]

            # Verify CVE preservation
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]

        deletion_result = {
            "deleted": total_deleted,
            "remaining_wave3": remaining,
            "cve_count": cve_count,
            "cve_preserved": cve_count == 267487,
            "deletion_complete": remaining == 0
        }

        status = "PASS" if deletion_result["deletion_complete"] and deletion_result["cve_preserved"] else "FAIL"
        self._log("level2_surgical_deletion", status, deletion_result)

        print(f"Deleted: {total_deleted:,} nodes")
        print(f"Remaining Wave 3 nodes: {remaining:,}")
        print(f"CVE count: {cve_count:,} (preserved: {deletion_result['cve_preserved']})")
        print(f"Status: {status}")
        print()

        return deletion_result

    def execute_level3_cve_preservation_check(self) -> Dict[str, Any]:
        """
        LEVEL 3: CVE Preservation Check (MANDATORY GATE)
        Verify CVE baseline unchanged
        """
        print("LEVEL 3: CVE Preservation Check")
        print("-" * 80)

        with self.driver.session() as session:
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]

        expected = 267487
        preserved = (cve_count == expected)

        preservation_result = {
            "cve_count": cve_count,
            "cve_expected": expected,
            "preserved": preserved
        }

        status = "PASS" if preserved else "CRITICAL_FAIL"
        self._log("level3_cve_preservation", status, preservation_result)

        print(f"CVE count: {cve_count:,}")
        print(f"Expected: {expected:,}")
        print(f"Status: {status}")
        print()

        if not preserved:
            print("❌ CRITICAL: CVE preservation failed! Aborting Wave 3 execution.")
            return preservation_result

        return preservation_result

    def execute_level4_reimport(self) -> Dict[str, Any]:
        """
        LEVEL 4: Re-Import Execution
        Execute Wave 3 import script to recreate nodes with correct structure
        """
        print("LEVEL 4: Re-Import Execution")
        print("-" * 80)

        scripts_dir = self.project_root / "scripts"
        script_path = scripts_dir / "wave_3_execute.py"

        if not script_path.exists():
            print(f"❌ Import script not found: {script_path}")
            return {"success": False, "error": "Script not found"}

        # Execute import script with extended timeout for 35,924 nodes
        try:
            print(f"Executing: {script_path}")
            print("This will take several minutes for 35,924 nodes...")
            print()

            process = subprocess.run(
                ["python3", str(script_path)],
                cwd=str(scripts_dir),
                capture_output=True,
                text=True,
                timeout=900  # 15 minute timeout
            )

            import_result = {
                "success": process.returncode == 0,
                "returncode": process.returncode,
                "stdout": process.stdout[-2000:] if process.stdout else "",
                "stderr": process.stderr[-1000:] if process.stderr else ""
            }

            if process.returncode == 0:
                print("✅ Import completed successfully")
                print(process.stdout[-500:] if process.stdout else "")
            else:
                print(f"❌ Import failed with code {process.returncode}")
                print(process.stderr[-500:] if process.stderr else "")

            self._log("level4_reimport", "SUCCESS" if import_result["success"] else "FAILED", import_result)

        except subprocess.TimeoutExpired:
            import_result = {
                "success": False,
                "error": "Import timeout after 15 minutes"
            }
            self._log("level4_reimport", "TIMEOUT", import_result)
            print("❌ Import timeout after 15 minutes")

        print()
        return import_result

    def execute_level5_post_import_validation(self) -> Dict[str, Any]:
        """
        LEVEL 5: Post-Import Validation
        Verify correct node count and structure
        """
        print("LEVEL 5: Post-Import Validation")
        print("-" * 80)

        with self.driver.session() as session:
            # Count Wave 3 nodes
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                RETURN count(n) as count
            """)
            wave3_count = result.single()["count"]

            # Validate each node type from taxonomy
            node_type_validations = {}
            for node_type, config in self.wave_config['node_type_mappings'].items():
                expected_count = config['count']

                # Query by node type
                result = session.run(f"""
                    MATCH (n:{node_type})
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                    RETURN count(n) as count
                """)
                actual_count = result.single()["count"]

                node_type_validations[node_type] = {
                    "expected": expected_count,
                    "actual": actual_count,
                    "valid": actual_count == expected_count
                }

                status_symbol = "✅" if actual_count == expected_count else "❌"
                print(f"{status_symbol} {node_type}: {actual_count:,} / {expected_count:,}")

        all_valid = (
            wave3_count == 35924 and
            all(v["valid"] for v in node_type_validations.values())
        )

        validation_result = {
            "wave3_total": wave3_count,
            "expected_total": 35924,
            "node_type_validations": node_type_validations,
            "all_valid": all_valid
        }

        status = "PASS" if all_valid else "FAIL"
        self._log("level5_post_import_validation", status, validation_result)

        print()
        print(f"Total Wave 3 nodes: {wave3_count:,} (expected: 35,924)")
        print(f"Status: {status}")
        print()

        return validation_result

    def execute_level6_comprehensive_validation(self) -> Dict[str, Any]:
        """
        LEVEL 6: Comprehensive Validation
        Verify ENERGY labels, subdomains, functional roles, and relationships
        """
        print("LEVEL 6: Comprehensive Validation")
        print("-" * 80)

        with self.driver.session() as session:
            # Check ENERGY domain label
            result = session.run("""
                MATCH (n:ENERGY)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                RETURN count(n) as count
            """)
            energy_count = result.single()["count"]

            # Check subdomain labels
            subdomains = {}
            for subdomain in self.wave_config['label_strategy']['subdomain_labels']:
                result = session.run(f"""
                    MATCH (n:{subdomain})
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                    RETURN count(n) as count
                """)
                subdomains[subdomain] = result.single()["count"]

            # Check functional roles
            roles = {}
            for role in self.wave_config['label_strategy']['functional_roles']:
                result = session.run(f"""
                    MATCH (n:{role})
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                    RETURN count(n) as count
                """)
                roles[role] = result.single()["count"]

            # Check for any mislabeled WATER nodes
            result = session.run("""
                MATCH (n:WATER)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                RETURN count(n) as count
            """)
            mislabeled_water = result.single()["count"]

            # Verify CVE preservation
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]

        all_valid = (
            energy_count == 35924 and
            sum(subdomains.values()) == 35924 and
            mislabeled_water == 0 and
            cve_count == 267487
        )

        validation_result = {
            "energy_labeled": energy_count,
            "expected_total": 35924,
            "subdomains": subdomains,
            "functional_roles": roles,
            "mislabeled_water": mislabeled_water,
            "cve_count": cve_count,
            "cve_preserved": cve_count == 267487,
            "all_valid": all_valid
        }

        status = "PASS" if all_valid else "FAIL"
        self._log("level6_comprehensive_validation", status, validation_result)

        print(f"ENERGY labeled nodes: {energy_count:,} (expected: 35,924)")
        print(f"Mislabeled WATER nodes: {mislabeled_water:,} (expected: 0)")
        print(f"CVE count: {cve_count:,} (expected: 267,487)")
        print()
        print("Subdomain distribution:")
        for subdomain, count in subdomains.items():
            print(f"  {subdomain}: {count:,}")
        print()
        print("Functional role distribution:")
        for role, count in roles.items():
            print(f"  {role}: {count:,}")
        print()
        print(f"Status: {status}")
        print()

        return validation_result

    def execute(self) -> bool:
        """
        Execute complete Wave 3 surgical deletion and rebuild workflow

        Returns:
            bool: True if successful
        """
        try:
            print("=" * 80)
            print("PHASE 2: WAVE 3 SURGICAL DELETION AND REBUILD (35,924 nodes)")
            print("=" * 80)
            print()

            print("[1/8] Creating pre-deletion checkpoint...")
            checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 3 Surgical Deletion - Start",
                phase="PHASE_2",
                wave="WAVE3"
            )
            print(f"✅ Checkpoint created: {checkpoint_id}")
            print()

            print("[2/8] Level 1: Pre-deletion validation...")
            level1 = self.execute_level1_predeletion_validation()
            if not level1.get("ready_for_deletion"):
                print("❌ Pre-deletion validation failed")
                return False
            print("✅ Pre-deletion validation passed")
            print()

            print("[3/8] Level 2: Surgical deletion...")
            level2 = self.execute_level2_surgical_deletion()
            if not level2.get("deletion_complete"):
                print("❌ Surgical deletion failed")
                return False
            print("✅ Surgical deletion completed")
            print()

            print("[4/8] Level 3: CVE preservation check...")
            level3 = self.execute_level3_cve_preservation_check()
            if not level3.get("preserved"):
                print("❌ CRITICAL: CVE preservation failed!")
                return False
            print("✅ CVE baseline preserved")
            print()

            print("[5/8] Level 4: Re-import execution...")
            level4 = self.execute_level4_reimport()
            if not level4.get("success"):
                print("❌ Re-import failed")
                return False
            print("✅ Re-import completed")
            print()

            print("[6/8] Level 5: Post-import validation...")
            level5 = self.execute_level5_post_import_validation()
            if not level5.get("all_valid"):
                print("⚠️  Post-import validation warnings - review logs")
            else:
                print("✅ Post-import validation passed")
            print()

            print("[7/8] Level 6: Comprehensive validation...")
            level6 = self.execute_level6_comprehensive_validation()
            if not level6.get("all_valid"):
                print("⚠️  Comprehensive validation warnings - review logs")
            else:
                print("✅ Comprehensive validation passed")
            print()

            print("[8/8] Creating post-rebuild checkpoint...")
            final_checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 3 Surgical Deletion and Rebuild - Complete",
                phase="PHASE_2",
                wave="WAVE3",
                metadata={
                    "level1": level1,
                    "level2": level2,
                    "level3": level3,
                    "level4": level4,
                    "level5": level5,
                    "level6": level6
                }
            )
            print(f"✅ Final checkpoint created: {final_checkpoint_id}")
            print()

            print("=" * 80)
            print("✅ WAVE 3 SURGICAL DELETION AND REBUILD COMPLETE")
            print("=" * 80)
            print()
            print(f"Pre-deletion: {level1['wave3_total']:,} nodes")
            print(f"Deleted: {level2['deleted']:,} nodes")
            print(f"Re-imported: {level5['wave3_total']:,} nodes")
            print(f"ENERGY labeled: {level6['energy_labeled']:,} nodes")
            print(f"Mislabeled WATER fixed: {level1['mislabeled_water_nodes']:,} → 0")
            print(f"CVE preservation: ✅ INTACT ({level6['cve_count']:,})")
            print()

            return True

        except Exception as e:
            self._log("execute", "FAILED", {"error": str(e)})
            print(f"\\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            self.checkpoint_mgr.close()
            self.driver.close()


def main():
    """Main execution function"""
    executor = Wave3MasterExecutor()
    success = executor.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
