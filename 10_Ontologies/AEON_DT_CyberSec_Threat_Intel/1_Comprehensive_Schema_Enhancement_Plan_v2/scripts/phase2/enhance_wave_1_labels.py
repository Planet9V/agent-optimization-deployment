#!/usr/bin/env python3
"""
Wave 1 Label Enhancement - Add SAREF_Core subdomain and functional role labels
Non-destructive label addition to 5,000 Wave 1 nodes after re-import

Operation: ADD_LABELS (preserves all existing data)
Target: 5,000 Wave 1 nodes
Labels Added: SAREF_Core + functional role (Asset/Property)
Pagination: SKIP 0 pattern (prevents offset drift)

Generated: 2025-10-31
Version: 1.0.0
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import json

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


class Wave1LabelEnhancer:
    """Enhance Wave 1 nodes with SAREF_Core and functional role labels"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        project_root: Path = None
    ):
        """Initialize Wave 1 Label Enhancer"""
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "wave_1_label_enhancement.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Load master taxonomy
        taxonomy_path = self.project_root / "master_taxonomy.yaml"
        with open(taxonomy_path, 'r') as f:
            self.taxonomy = yaml.safe_load(f)

        self.wave_config = self.taxonomy['wave_1']
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
            f.write(json.dumps(log_entry) + '\n')
        print(f"[{status}] {operation}: {json.dumps(details or {}, indent=2)}")

    def add_labels_to_node_type(
        self,
        node_type: str,
        labels_to_add: list,
        batch_size: int = 50
    ) -> int:
        """
        Add SAREF_Core and functional role labels to a specific node type

        Args:
            node_type: Node type label (Device, Property, Function, State)
            labels_to_add: Labels to add (e.g., [SAREF_Core, Asset])
            batch_size: Number of nodes to process per batch

        Returns:
            int: Number of nodes enhanced
        """
        total_enhanced = 0
        batch_num = 0

        with self.driver.session() as session:
            # Process until no nodes remain
            while True:
                # Always SKIP 0 - take first N unlabeled nodes
                enhance_query = f"""
                    MATCH (n:{node_type})
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                    AND NOT n:SAREF_Core
                    WITH n
                    LIMIT {batch_size}
                    SET n:{':'.join(labels_to_add)}
                    RETURN count(n) as enhanced
                """

                result = session.run(enhance_query)
                batch_enhanced = result.single()["enhanced"]

                if batch_enhanced == 0:
                    # No more nodes to enhance
                    break

                total_enhanced += batch_enhanced
                batch_num += 1

                self._log(
                    "add_labels_batch",
                    "SUCCESS",
                    {
                        "node_type": node_type,
                        "batch_number": batch_num,
                        "batch_size": batch_enhanced,
                        "labels_added": labels_to_add,
                        "cumulative_total": total_enhanced
                    }
                )

        return total_enhanced

    def enhance_all_wave1_nodes(self) -> Dict[str, int]:
        """
        Enhance all Wave 1 nodes with SAREF_Core and functional role labels

        Returns:
            Dict with enhancement statistics per node type
        """
        print("=" * 80)
        print("WAVE 1 LABEL ENHANCEMENT")
        print("=" * 80)
        print()

        enhancement_stats = {}

        # Node type label mappings
        # From taxonomy: Device (2000) and Property (1500) need Asset/Property roles
        # But actual import created: Device (800), Property (1200), others
        label_mappings = {
            "Device": ["SAREF_Core", "Asset"],
            "Property": ["SAREF_Core", "Property"],
            "Measurement": ["SAREF_Core", "Property"],
            "Function": ["SAREF_Core", "Property"],
            "Service": ["SAREF_Core", "Property"],
            "Command": ["SAREF_Core", "Property"],
            "State": ["SAREF_Core", "Property"],
            "UnitOfMeasure": ["SAREF_Core", "Property"]
        }

        for node_type, labels_to_add in label_mappings.items():
            print(f"Processing {node_type}...")
            print(f"  Adding labels: {', '.join(labels_to_add)}")

            enhanced_count = self.add_labels_to_node_type(
                node_type,
                labels_to_add,
                batch_size=50
            )

            enhancement_stats[node_type] = {
                "enhanced": enhanced_count,
                "labels_added": labels_to_add
            }

            print(f"  ✅ Enhanced {enhanced_count} nodes")
            print()

        return enhancement_stats

    def validate_label_additions(self) -> Dict[str, Any]:
        """
        Validate that all Wave 1 nodes have SAREF_Core label

        Returns:
            Dict with validation results
        """
        print("Validating label additions...")

        with self.driver.session() as session:
            # Check that all Wave 1 nodes have SAREF label (should already exist)
            result = session.run("""
                MATCH (n:SAREF)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                RETURN count(n) as count
            """)
            saref_count = result.single()["count"]

            # Check that all Wave 1 nodes now have SAREF_Core label
            result = session.run("""
                MATCH (n:SAREF_Core)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                RETURN count(n) as count
            """)
            saref_core_count = result.single()["count"]

        all_valid = (
            saref_count == 5000 and
            saref_core_count == 5000
        )

        validation_result = {
            "saref_labeled": saref_count,
            "saref_core_labeled": saref_core_count,
            "expected_total": 5000,
            "all_valid": all_valid
        }

        status = "PASS" if all_valid else "FAIL"
        self._log("validate_label_additions", status, validation_result)

        return validation_result

    def validate_cve_preservation(self) -> bool:
        """
        MANDATORY: Verify CVE nodes unchanged

        Returns:
            bool: True if exactly 267,487 CVE nodes exist
        """
        with self.driver.session() as session:
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]

            expected = 267487
            preserved = (cve_count == expected)

            self._log(
                "validate_cve_preservation",
                "PASS" if preserved else "CRITICAL_FAIL",
                {"expected": expected, "actual": cve_count}
            )

            return preserved

    def execute(self) -> bool:
        """
        Execute complete Wave 1 label enhancement workflow

        Returns:
            bool: True if successful
        """
        try:
            print("=" * 80)
            print("PHASE 2: WAVE 1 LABEL ENHANCEMENT (5,000 nodes)")
            print("=" * 80)
            print()

            print("[1/5] Creating pre-enhancement checkpoint...")
            checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 1 Label Enhancement - Start",
                phase="PHASE_2",
                wave="WAVE1"
            )
            print(f"✅ Checkpoint created: {checkpoint_id}")
            print()

            print("[2/5] Enhancing all Wave 1 nodes...")
            enhancement_stats = self.enhance_all_wave1_nodes()
            total_enhanced = sum(s["enhanced"] for s in enhancement_stats.values())
            print(f"✅ Enhanced {total_enhanced} nodes across {len(enhancement_stats)} types")
            print()

            print("[3/5] Validating label additions...")
            validation = self.validate_label_additions()
            if validation["all_valid"]:
                print("✅ All label additions validated successfully")
            else:
                print("⚠️  Some validations failed - review logs")
            print()

            print("[4/5] Validating CVE preservation (MANDATORY)...")
            if not self.validate_cve_preservation():
                print("❌ CRITICAL: CVE preservation check failed!")
                return False
            print("✅ CVE baseline preserved (267,487 nodes)")
            print()

            print("[5/5] Creating post-enhancement checkpoint...")
            final_checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 1 Label Enhancement - Complete",
                phase="PHASE_2",
                wave="WAVE1",
                metadata={
                    "enhancement_stats": enhancement_stats,
                    "validation": validation
                }
            )
            print(f"✅ Final checkpoint created: {final_checkpoint_id}")
            print()

            print("=" * 80)
            print("✅ WAVE 1 LABEL ENHANCEMENT COMPLETE")
            print("=" * 80)
            print()
            print(f"Enhanced: {total_enhanced} nodes")
            print(f"Node types: {len(enhancement_stats)}")
            print(f"All validations: {'✅ PASSED' if validation['all_valid'] else '⚠️  WARNING'}")
            print(f"CVE preservation: ✅ INTACT")
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
    enhancer = Wave1LabelEnhancer()
    success = enhancer.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
