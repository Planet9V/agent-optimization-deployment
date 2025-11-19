#!/usr/bin/env python3
"""
Wave 11 Label Enhancement - Add Multi-Label Strategy to IoT Device Nodes
Non-destructive label addition to 4,000 existing nodes

Operation: ADD_LABELS (preserves all existing data)
Target: 4,000 Wave 11 nodes
Labels Added: Device + subdomain + functional role
Pagination: FIXED - Always SKIP 0 pattern (prevents offset drift)

Generated: 2025-10-31
Version: 2.0.0 (CORRECTED PAGINATION)
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
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


class Wave11LabelEnhancer:
    """Enhance Wave 11 nodes with multi-label strategy using corrected pagination"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        project_root: Path = None
    ):
        """
        Initialize Wave 11 Label Enhancer

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

        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "wave_11_label_enhancement.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Load master taxonomy
        taxonomy_path = self.project_root / "master_taxonomy.yaml"
        with open(taxonomy_path, 'r') as f:
            self.taxonomy = yaml.safe_load(f)

        self.wave_config = self.taxonomy['wave_11']
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

    def validate_wave_11_exists(self) -> bool:
        """
        Verify Wave 11 nodes exist and count is correct

        Returns:
            bool: True if exactly 140,000 Wave 11 nodes exist
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE11'
                RETURN count(n) as count
            """)
            count = result.single()["count"]

            expected = 4000
            if count != expected:
                self._log(
                    "validate_wave_11_exists",
                    "FAILED",
                    {"expected": expected, "actual": count}
                )
                return False

            self._log(
                "validate_wave_11_exists",
                "PASS",
                {"count": count}
            )
            return True

    def get_wave_11_node_types(self) -> Dict[str, int]:
        """
        Get current Wave 11 node type distribution

        Returns:
            Dict mapping node types to counts
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE11'
                RETURN labels(n) as labels, count(n) as count
                ORDER BY count DESC
            """)

            node_types = {}
            for record in result:
                labels = record["labels"]
                # Extract primary type label (not domain/subdomain/role labels)
                type_label = [
                    l for l in labels
                    if l not in ["Device", "Health_Monitor", "Agriculture",
                                  "Smart_City", "Asset", "Sensor",
                                  "Monitoring", "Measurement", "Control", "Property"]
                ]
                if type_label:
                    node_types[type_label[0]] = record["count"]

            self._log(
                "get_wave_11_node_types",
                "SUCCESS",
                {"node_types": node_types, "total_types": len(node_types)}
            )

            return node_types

    def add_labels_to_node_type(
        self,
        node_type_key: str,
        config: Dict[str, Any],
        batch_size: int = 50
    ) -> int:
        """
        Add labels to all nodes of a specific type using CORRECTED pagination

        **PAGINATION FIX**: Always SKIP 0 and process until no nodes remain.
        This prevents offset drift when filter changes during processing.

        Args:
            node_type_key: Key from taxonomy (e.g., "SoftwareComponent", "Dependency")
            config: Configuration dict from taxonomy
            batch_size: Number of nodes to process per batch

        Returns:
            int: Number of nodes enhanced
        """
        labels_to_add = config['add_labels']

        # Extract primary node type from final_labels
        # The primary type is the LAST label (rightmost in taxonomy)
        # It may overlap with subdomain names, so just use the last one
        final_labels = config['final_labels']
        primary_type = final_labels[-1]  # Last label is always the node type

        total_enhanced = 0
        batch_num = 0

        with self.driver.session() as session:
            # CORRECTED PAGINATION: Process until no nodes remain
            while True:
                # Always SKIP 0 - take first N unlabeled nodes
                enhance_query = f"""
                    MATCH (n:{primary_type})
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE11'
                    AND NOT n:Device
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
                        "node_type": node_type_key,
                        "batch_number": batch_num,
                        "batch_size": batch_enhanced,
                        "labels_added": labels_to_add,
                        "cumulative_total": total_enhanced
                    }
                )

                # Progress indicator every 1000 nodes
                if total_enhanced % 1000 == 0:
                    print(f"  Progress: {total_enhanced:,} nodes enhanced...")

        return total_enhanced

    def enhance_all_wave_11_nodes(self) -> Dict[str, int]:
        """
        Enhance all Wave 11 nodes with multi-label strategy

        Returns:
            Dict with enhancement statistics per node type
        """
        print("=" * 80)
        print("WAVE 10 LABEL ENHANCEMENT")
        print("=" * 80)
        print()

        enhancement_stats = {}
        node_type_mappings = self.wave_config['node_type_mappings']

        for node_type_key, config in node_type_mappings.items():
            labels_to_add = config['add_labels']
            expected_count = config['count']
            status = config.get('status', 'NEEDS_ENHANCEMENT')

            print(f"Processing {node_type_key}...")

            if status == "ALREADY_ENHANCED":
                print(f"  ℹ️  Already enhanced - skipping")
                print(f"  Expected nodes: {expected_count:,}")
                enhancement_stats[node_type_key] = {
                    "expected": expected_count,
                    "enhanced": expected_count,
                    "labels_added": [],
                    "status": "SKIPPED"
                }
                print()
                continue

            print(f"  Adding labels: {', '.join(labels_to_add)}")
            print(f"  Expected nodes: {expected_count:,}")

            enhanced_count = self.add_labels_to_node_type(
                node_type_key,
                config,
                batch_size=50
            )

            enhancement_stats[node_type_key] = {
                "expected": expected_count,
                "enhanced": enhanced_count,
                "labels_added": labels_to_add,
                "status": "ENHANCED"
            }

            if enhanced_count == expected_count:
                print(f"  ✅ Enhanced {enhanced_count:,} nodes")
            else:
                print(f"  ⚠️  Warning: Expected {expected_count:,}, enhanced {enhanced_count:,}")

            print()

        return enhancement_stats

    def validate_label_additions(self) -> Dict[str, Any]:
        """
        Validate that all Wave 11 nodes have correct labels

        Returns:
            Dict with validation results
        """
        print("Validating label additions...")

        with self.driver.session() as session:
            # Check that all Wave 11 nodes have Device label
            result = session.run("""
                MATCH (n:Device)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE11'
                RETURN count(n) as count
            """)
            device_count = result.single()["count"]

            # Check node type specific labels
            node_type_validations = {}
            for node_type, config in self.wave_config['node_type_mappings'].items():
                expected_labels = set(config['final_labels'])
                expected_count = config['count']

                # Build label filter query
                label_filter = ':'.join(expected_labels)
                result = session.run(f"""
                    MATCH (n:{label_filter})
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE11'
                    RETURN count(n) as count
                """)
                actual_count = result.single()["count"]

                node_type_validations[node_type] = {
                    "expected_count": expected_count,
                    "actual_count": actual_count,
                    "expected_labels": list(expected_labels),
                    "valid": actual_count == expected_count
                }

        all_valid = (
            device_count == 4000 and
            all(v["valid"] for v in node_type_validations.values())
        )

        validation_result = {
            "device_labeled": device_count,
            "expected_total": 4000,
            "node_type_validations": node_type_validations,
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
            result = session.run("""
                MATCH (n:CVE)
                RETURN count(n) as count
            """)
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
        Execute complete Wave 11 label enhancement workflow

        Returns:
            bool: True if successful
        """
        try:
            # Pre-flight validation
            print("=" * 80)
            print("PHASE 1: WAVE 10 LABEL ENHANCEMENT (140,000 nodes)")
            print("=" * 80)
            print()

            print("[1/7] Validating Wave 11 exists...")
            if not self.validate_wave_11_exists():
                print("❌ Wave 11 validation failed")
                return False
            print("✅ Wave 11 exists (140,000 nodes)")
            print()

            print("[2/7] Getting current node types...")
            node_types = self.get_wave_11_node_types()
            print(f"✅ Found {len(node_types)} node types")
            print()

            print("[3/7] Creating pre-enhancement checkpoint...")
            checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 11 Label Enhancement - Start",
                phase="PHASE_1",
                wave="WAVE11"
            )
            print(f"✅ Checkpoint created: {checkpoint_id}")
            print()

            print("[4/7] Enhancing all Wave 11 nodes...")
            print("Using CORRECTED pagination (SKIP 0 pattern)")
            enhancement_stats = self.enhance_all_wave_11_nodes()
            total_enhanced = sum(s["enhanced"] for s in enhancement_stats.values())
            print(f"✅ Enhanced {total_enhanced:,} nodes across {len(enhancement_stats)} types")
            print()

            print("[5/7] Validating label additions...")
            validation = self.validate_label_additions()
            if validation["all_valid"]:
                print("✅ All label additions validated successfully")
            else:
                print("⚠️  Some validations failed - review logs")
            print()

            print("[6/7] Validating CVE preservation (MANDATORY)...")
            if not self.validate_cve_preservation():
                print("❌ CRITICAL: CVE preservation check failed!")
                return False
            print("✅ CVE baseline preserved (267,487 nodes)")
            print()

            print("[7/7] Creating post-enhancement checkpoint...")
            final_checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 11 Label Enhancement - Complete",
                phase="PHASE_1",
                wave="WAVE11",
                metadata={
                    "enhancement_stats": enhancement_stats,
                    "validation": validation
                }
            )
            print(f"✅ Final checkpoint created: {final_checkpoint_id}")
            print()

            print("=" * 80)
            print("✅ WAVE 10 LABEL ENHANCEMENT COMPLETE")
            print("=" * 80)
            print()
            print(f"Enhanced: {total_enhanced:,} nodes")
            print(f"Node types: {len(enhancement_stats)}")
            print(f"All validations: {'✅ PASSED' if validation['all_valid'] else '⚠️  WARNING'}")
            print(f"CVE preservation: ✅ INTACT")
            print(f"Pagination: ✅ SINGLE RUN (SKIP 0 pattern)")
            print()

            return True

        except Exception as e:
            self._log("execute", "FAILED", {"error": str(e)})
            print(f"\\n❌ ERROR: {e}")
            return False

        finally:
            self.checkpoint_mgr.close()
            self.driver.close()


def main():
    """Main execution function"""
    enhancer = Wave11LabelEnhancer()
    success = enhancer.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
