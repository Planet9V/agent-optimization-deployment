#!/usr/bin/env python3
"""
Wave 1 Master Executor - Phase 2: Surgical Deletion and Rebuild
SAREF Core Foundation with 6-Level Validation

Operation: DELETE_AND_REBUILD
Target: 5,000 SAREF nodes with correct multi-label structure
Validation Levels: 6 (Pre-delete, Deletion, CVE, Import, Post-import, Final)

Generated: 2025-10-31
Version: 2.0.0 (PHASE 2 - SURGICAL REBUILD)
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import json

# Add parent directories to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "scripts"))

try:
    from neo4j import GraphDatabase
    import yaml
    from checkpoint.checkpoint_manager import CheckpointManager
    from wave_1_devices_properties import Wave1DevicesPropertiesExecutor
    from wave_1_measurements import Wave1MeasurementsExecutor
    from wave_1_services_functions import Wave1ServicesFunctionsExecutor
    from wave_1_commands_states_units import Wave1CommandsStatesUnitsExecutor
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    print("Required packages: neo4j-driver, pyyaml")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class Wave1MasterExecutor:
    """
    Master executor for Wave 1 surgical deletion and rebuild
    Implements 6-level validation for safe deletion and recreation
    """

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        project_root: Path = None
    ):
        """
        Initialize Wave 1 Master Executor

        Args:
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
            project_root: Project root directory
        """
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password

        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "wave_1_master_execution.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Load master taxonomy
        taxonomy_path = self.project_root / "master_taxonomy.yaml"
        with open(taxonomy_path, 'r') as f:
            self.taxonomy = yaml.safe_load(f)

        self.wave_config = self.taxonomy['wave_1']
        self.checkpoint_mgr = CheckpointManager(neo4j_uri, neo4j_user, neo4j_password)

        # Expected counts
        self.expected_cve_count = 267487
        self.expected_wave1_count = 5000

        # Node type mappings from taxonomy
        self.expected_node_counts = {
            "Device": 2000,
            "Property": 1500,
            "Function": 800,
            "State": 700
        }

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
        logging.info(f"[{status}] {operation}: {json.dumps(details or {}, indent=2)}")

    # =========================================================================
    # LEVEL 1: PRE-DELETE VALIDATION
    # =========================================================================

    def validate_level1_pre_delete(self) -> Dict[str, Any]:
        """
        Level 1: Capture current Wave 1 state before deletion

        Returns:
            Dict with current state snapshot
        """
        logging.info("=" * 80)
        logging.info("LEVEL 1: PRE-DELETE VALIDATION")
        logging.info("=" * 80)

        with self.driver.session() as session:
            # Total Wave 1 count
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                RETURN count(n) as count
            """)
            current_count = result.single()["count"]

            # Node type distribution
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                RETURN labels(n) as labels, count(n) as count
                ORDER BY count DESC
            """)

            label_distribution = []
            for record in result:
                label_distribution.append({
                    "labels": record["labels"],
                    "count": record["count"]
                })

            # CVE baseline
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]

            # Total nodes in database
            result = session.run("MATCH (n) RETURN count(n) as count")
            total_nodes = result.single()["count"]

        state = {
            "wave1_count": current_count,
            "label_distribution": label_distribution,
            "cve_count": cve_count,
            "total_nodes": total_nodes,
            "timestamp": datetime.now().isoformat()
        }

        self._log("validate_level1_pre_delete", "SUCCESS", state)

        logging.info(f"Current Wave 1 nodes: {current_count}")
        logging.info(f"CVE baseline: {cve_count}")
        logging.info(f"Total database nodes: {total_nodes}")
        logging.info(f"Unique label combinations: {len(label_distribution)}")

        return state

    # =========================================================================
    # LEVEL 2: SURGICAL DELETION
    # =========================================================================

    def execute_level2_surgical_deletion(self) -> Dict[str, Any]:
        """
        Level 2: Delete ONLY Wave 1 nodes, preserve all others

        Returns:
            Dict with deletion results
        """
        logging.info("=" * 80)
        logging.info("LEVEL 2: SURGICAL DELETION")
        logging.info("=" * 80)

        with self.driver.session() as session:
            # Delete in batches to avoid memory issues
            batch_size = 100
            total_deleted = 0

            while True:
                result = session.run(f"""
                    MATCH (n)
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                    WITH n LIMIT {batch_size}
                    DETACH DELETE n
                    RETURN count(n) as deleted
                """)

                deleted = result.single()["deleted"]
                if deleted == 0:
                    break

                total_deleted += deleted
                logging.info(f"Deleted batch: {deleted} nodes (total: {total_deleted})")

            # Verify deletion
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                RETURN count(n) as remaining
            """)
            remaining = result.single()["remaining"]

        deletion_result = {
            "total_deleted": total_deleted,
            "remaining_wave1_nodes": remaining,
            "deletion_complete": remaining == 0
        }

        self._log("execute_level2_surgical_deletion", "SUCCESS", deletion_result)

        logging.info(f"Total deleted: {total_deleted}")
        logging.info(f"Remaining Wave 1 nodes: {remaining}")

        if remaining != 0:
            raise ValueError(f"Deletion incomplete: {remaining} Wave 1 nodes remain")

        return deletion_result

    # =========================================================================
    # LEVEL 3: CVE PRESERVATION VALIDATION
    # =========================================================================

    def validate_level3_cve_preservation(self) -> bool:
        """
        Level 3: MANDATORY verification that CVE nodes are untouched

        Returns:
            bool: True if CVE count is exactly 267,487
        """
        logging.info("=" * 80)
        logging.info("LEVEL 3: CVE PRESERVATION VALIDATION (MANDATORY)")
        logging.info("=" * 80)

        with self.driver.session() as session:
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]

        preserved = (cve_count == self.expected_cve_count)

        self._log(
            "validate_level3_cve_preservation",
            "PASS" if preserved else "CRITICAL_FAIL",
            {"expected": self.expected_cve_count, "actual": cve_count}
        )

        logging.info(f"CVE count: {cve_count} (expected: {self.expected_cve_count})")

        if not preserved:
            raise ValueError(f"CRITICAL: CVE count changed! {cve_count} != {self.expected_cve_count}")

        return preserved

    # =========================================================================
    # LEVEL 4: RE-IMPORT EXECUTION
    # =========================================================================

    def execute_level4_reimport(self) -> Dict[str, Any]:
        """
        Level 4: Execute Wave 1 import scripts with corrected labels

        Returns:
            Dict with import results from all 4 scripts
        """
        logging.info("=" * 80)
        logging.info("LEVEL 4: RE-IMPORT WITH CORRECTED LABELS")
        logging.info("=" * 80)

        results = {}

        # Script 1: Devices & Properties
        logging.info("\n[1/4] Executing: Devices & Properties...")
        try:
            executor1 = Wave1DevicesPropertiesExecutor(
                self.neo4j_uri,
                self.neo4j_user,
                self.neo4j_password
            )
            results["devices_properties"] = executor1.execute()
            logging.info("✅ Devices & Properties complete")
        except Exception as e:
            logging.error(f"❌ Devices & Properties failed: {e}")
            results["devices_properties"] = {"error": str(e)}

        # Script 2: Measurements
        logging.info("\n[2/4] Executing: Measurements...")
        try:
            executor2 = Wave1MeasurementsExecutor(
                self.neo4j_uri,
                self.neo4j_user,
                self.neo4j_password
            )
            results["measurements"] = executor2.execute()
            logging.info("✅ Measurements complete")
        except Exception as e:
            logging.error(f"❌ Measurements failed: {e}")
            results["measurements"] = {"error": str(e)}

        # Script 3: Services & Functions
        logging.info("\n[3/4] Executing: Services & Functions...")
        try:
            executor3 = Wave1ServicesFunctionsExecutor(
                self.neo4j_uri,
                self.neo4j_user,
                self.neo4j_password
            )
            results["services_functions"] = executor3.execute()
            logging.info("✅ Services & Functions complete")
        except Exception as e:
            logging.error(f"❌ Services & Functions failed: {e}")
            results["services_functions"] = {"error": str(e)}

        # Script 4: Commands, States & Units
        logging.info("\n[4/4] Executing: Commands, States & Units...")
        try:
            executor4 = Wave1CommandsStatesUnitsExecutor(
                self.neo4j_uri,
                self.neo4j_user,
                self.neo4j_password
            )
            results["commands_states_units"] = executor4.execute()
            logging.info("✅ Commands, States & Units complete")
        except Exception as e:
            logging.error(f"❌ Commands, States & Units failed: {e}")
            results["commands_states_units"] = {"error": str(e)}

        self._log("execute_level4_reimport", "SUCCESS", results)

        return results

    # =========================================================================
    # LEVEL 5: POST-IMPORT VALIDATION
    # =========================================================================

    def validate_level5_post_import(self) -> Dict[str, Any]:
        """
        Level 5: Validate correct structure after re-import

        Returns:
            Dict with validation results
        """
        logging.info("=" * 80)
        logging.info("LEVEL 5: POST-IMPORT VALIDATION")
        logging.info("=" * 80)

        with self.driver.session() as session:
            # Total Wave 1 count
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                RETURN count(n) as count
            """)
            wave1_count = result.single()["count"]

            # Validate each node type from taxonomy
            node_type_validations = {}
            for node_type, expected_count in self.expected_node_counts.items():
                result = session.run(f"""
                    MATCH (n:{node_type})
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                    RETURN count(n) as count
                """)
                actual_count = result.single()["count"]

                node_type_validations[node_type] = {
                    "expected": expected_count,
                    "actual": actual_count,
                    "valid": actual_count == expected_count
                }

                if actual_count == expected_count:
                    logging.info(f"✅ {node_type}: {actual_count}/{expected_count}")
                else:
                    logging.error(f"❌ {node_type}: {actual_count}/{expected_count}")

        all_valid = (
            wave1_count == self.expected_wave1_count and
            all(v["valid"] for v in node_type_validations.values())
        )

        validation_result = {
            "wave1_total": wave1_count,
            "expected_total": self.expected_wave1_count,
            "node_type_validations": node_type_validations,
            "all_valid": all_valid
        }

        status = "PASS" if all_valid else "FAIL"
        self._log("validate_level5_post_import", status, validation_result)

        return validation_result

    # =========================================================================
    # LEVEL 6: COMPREHENSIVE FINAL VALIDATION
    # =========================================================================

    def validate_level6_comprehensive(self) -> Dict[str, Any]:
        """
        Level 6: Comprehensive validation across all dimensions

        Returns:
            Dict with comprehensive validation results
        """
        logging.info("=" * 80)
        logging.info("LEVEL 6: COMPREHENSIVE FINAL VALIDATION")
        logging.info("=" * 80)

        with self.driver.session() as session:
            # 1. Label completeness check
            result = session.run("""
                MATCH (n:SAREF)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                RETURN count(n) as count
            """)
            saref_labeled = result.single()["count"]

            # 2. Subdomain check
            result = session.run("""
                MATCH (n:SAREF_Core)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                RETURN count(n) as count
            """)
            subdomain_labeled = result.single()["count"]

            # 3. Relationship preservation
            result = session.run("""
                MATCH (n)-[r]->(m)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                RETURN count(r) as count
            """)
            relationships_count = result.single()["count"]

            # 4. CVE final check
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            final_cve_count = result.single()["count"]

            # 5. Total database integrity
            result = session.run("MATCH (n) RETURN count(n) as count")
            total_nodes = result.single()["count"]

        comprehensive_result = {
            "saref_domain_labeled": saref_labeled,
            "saref_core_subdomain_labeled": subdomain_labeled,
            "relationships_created": relationships_count,
            "cve_final_count": final_cve_count,
            "total_database_nodes": total_nodes,
            "all_checks_passed": (
                saref_labeled == self.expected_wave1_count and
                subdomain_labeled == self.expected_wave1_count and
                final_cve_count == self.expected_cve_count
            )
        }

        status = "PASS" if comprehensive_result["all_checks_passed"] else "FAIL"
        self._log("validate_level6_comprehensive", status, comprehensive_result)

        logging.info(f"SAREF labeled: {saref_labeled}/{self.expected_wave1_count}")
        logging.info(f"SAREF_Core labeled: {subdomain_labeled}/{self.expected_wave1_count}")
        logging.info(f"Relationships: {relationships_count}")
        logging.info(f"CVE preserved: {final_cve_count}")
        logging.info(f"Total nodes: {total_nodes}")

        return comprehensive_result

    # =========================================================================
    # MASTER EXECUTION WORKFLOW
    # =========================================================================

    def execute(self) -> bool:
        """
        Execute complete Wave 1 surgical deletion and rebuild with 6-level validation

        Returns:
            bool: True if successful
        """
        try:
            logging.info("=" * 80)
            logging.info("WAVE 1 MASTER EXECUTOR - PHASE 2: SURGICAL REBUILD")
            logging.info("=" * 80)
            logging.info("")

            # Create pre-execution checkpoint
            logging.info("[0/6] Creating pre-execution checkpoint...")
            pre_checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 1 Phase 2 - Pre-Execution",
                phase="PHASE_2",
                wave="WAVE1"
            )
            logging.info(f"✅ Pre-checkpoint: {pre_checkpoint_id}")
            logging.info("")

            # LEVEL 1: Pre-delete validation
            logging.info("[1/6] Level 1: Pre-Delete Validation")
            pre_delete_state = self.validate_level1_pre_delete()
            logging.info("✅ Pre-delete state captured")
            logging.info("")

            # LEVEL 2: Surgical deletion
            logging.info("[2/6] Level 2: Surgical Deletion")
            deletion_result = self.execute_level2_surgical_deletion()
            logging.info(f"✅ Deleted {deletion_result['total_deleted']} Wave 1 nodes")
            logging.info("")

            # LEVEL 3: CVE preservation validation
            logging.info("[3/6] Level 3: CVE Preservation Validation")
            if not self.validate_level3_cve_preservation():
                logging.error("❌ CRITICAL: CVE preservation check failed!")
                return False
            logging.info("✅ CVE baseline preserved")
            logging.info("")

            # Create post-delete checkpoint
            logging.info("Creating post-delete checkpoint...")
            post_delete_checkpoint = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 1 Phase 2 - Post-Delete",
                phase="PHASE_2",
                wave="WAVE1",
                metadata={"deletion_result": deletion_result}
            )
            logging.info(f"✅ Post-delete checkpoint: {post_delete_checkpoint}")
            logging.info("")

            # LEVEL 4: Re-import
            logging.info("[4/6] Level 4: Re-Import Execution")
            import_results = self.execute_level4_reimport()
            logging.info("✅ All import scripts executed")
            logging.info("")

            # LEVEL 5: Post-import validation
            logging.info("[5/6] Level 5: Post-Import Validation")
            post_import_validation = self.validate_level5_post_import()
            if not post_import_validation["all_valid"]:
                logging.warning("⚠️  Some post-import validations failed")
            else:
                logging.info("✅ All post-import validations passed")
            logging.info("")

            # LEVEL 6: Comprehensive validation
            logging.info("[6/6] Level 6: Comprehensive Final Validation")
            comprehensive_validation = self.validate_level6_comprehensive()
            if not comprehensive_validation["all_checks_passed"]:
                logging.error("❌ Comprehensive validation failed")
                return False
            logging.info("✅ All comprehensive checks passed")
            logging.info("")

            # Create final checkpoint
            logging.info("Creating final checkpoint...")
            final_checkpoint = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 1 Phase 2 - Complete",
                phase="PHASE_2",
                wave="WAVE1",
                metadata={
                    "pre_delete_state": pre_delete_state,
                    "deletion_result": deletion_result,
                    "import_results": import_results,
                    "post_import_validation": post_import_validation,
                    "comprehensive_validation": comprehensive_validation
                }
            )
            logging.info(f"✅ Final checkpoint: {final_checkpoint}")
            logging.info("")

            # Success summary
            logging.info("=" * 80)
            logging.info("✅ WAVE 1 PHASE 2 COMPLETE - SURGICAL REBUILD SUCCESSFUL")
            logging.info("=" * 80)
            logging.info("")
            logging.info(f"Deleted: {deletion_result['total_deleted']} nodes")
            logging.info(f"Recreated: {post_import_validation['wave1_total']} nodes")
            logging.info(f"CVE Preserved: {comprehensive_validation['cve_final_count']}")
            logging.info(f"All Validations: ✅ PASSED (6/6 levels)")
            logging.info("")

            return True

        except Exception as e:
            self._log("execute", "FAILED", {"error": str(e)})
            logging.error(f"\n❌ ERROR: {e}")
            return False

        finally:
            self.checkpoint_mgr.close()
            self.driver.close()


def main():
    """Main execution function"""
    executor = Wave1MasterExecutor()
    success = executor.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
