#!/usr/bin/env python3
"""
Wave 9 Label Enhancement - Add Multi-Label Strategy to IT Infrastructure Software
Non-destructive label addition to 5,000 existing nodes

Operation: ADD_LABELS (preserves all existing data)
Target: 5,000 Wave 9 nodes
Labels Added: IT_INFRASTRUCTURE + subdomain + functional role

Generated: 2025-10-31
Version: 1.0.0
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


class Wave9LabelEnhancer:
    """Enhance Wave 9 nodes with multi-label strategy"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        project_root: Path = None
    ):
        """
        Initialize Wave 9 Label Enhancer

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
        self.log_file = self.project_root / "logs" / "wave_9_label_enhancement.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Load master taxonomy
        taxonomy_path = self.project_root / "master_taxonomy.yaml"
        with open(taxonomy_path, 'r') as f:
            self.taxonomy = yaml.safe_load(f)

        self.wave_config = self.taxonomy['wave_9']
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

    def validate_wave_9_exists(self) -> bool:
        """
        Verify Wave 9 nodes exist and count is correct

        Returns:
            bool: True if exactly 5,000 Wave 9 nodes exist
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE9'
                RETURN count(n) as count
            """)
            count = result.single()["count"]

            expected = 5000
            if count != expected:
                self._log(
                    "validate_wave_9_exists",
                    "FAILED",
                    {"expected": expected, "actual": count}
                )
                return False

            self._log(
                "validate_wave_9_exists",
                "PASS",
                {"count": count}
            )
            return True

    def get_wave_9_node_types(self) -> Dict[str, int]:
        """
        Get current Wave 9 node type distribution

        Returns:
            Dict mapping node types to counts
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE9'
                RETURN labels(n) as labels, count(n) as count
                ORDER BY count DESC
            """)

            node_types = {}
            for record in result:
                # Extract primary type label (not created_by or domain labels)
                labels = record["labels"]
                type_label = [
                    l for l in labels
                    if l not in ["IT_INFRASTRUCTURE", "IT_Software", "Cloud_Infrastructure",
                                  "Virtualization", "Container_Technology", "Asset",
                                  "Control", "Compliance"]
                ]
                if type_label:
                    node_types[type_label[0]] = record["count"]

            self._log(
                "get_wave_9_node_types",
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
        Add labels to all nodes of a specific type

        Args:
            node_type_key: Key from taxonomy (e.g., "Application", "ApplicationMiddleware")
            config: Configuration dict from taxonomy
            batch_size: Number of nodes to process per batch

        Returns:
            int: Number of nodes enhanced
        """
        labels_to_add = config['add_labels']

        # Skip if no labels to add (already enhanced)
        if not labels_to_add:
            self._log(
                "skip_already_enhanced",
                "INFO",
                {"node_type": node_type_key, "count": config['count']}
            )
            return config['count']  # Return expected count

        # Build match pattern based on query_filter or simple type
        if 'query_filter' in config:
            # Special case: multi-label nodes (e.g., "Application AND Middleware")
            filter_parts = config['query_filter'].split(' AND ')
            match_labels = ':'.join(filter_parts)
            match_pattern = f"MATCH (n:{match_labels})"
        else:
            # Simple case: single label type
            # Extract primary type label from final_labels
            final_labels = config['final_labels']
            # Primary type is usually the last label (not domain/subdomain/role)
            primary_type = [l for l in final_labels
                          if l not in ['IT_INFRASTRUCTURE', 'IT_Software', 'IT_Hardware',
                                      'Virtualization', 'Cloud_Infrastructure',
                                      'Asset', 'Control', 'Compliance']][-1]
            match_pattern = f"MATCH (n:{primary_type})"

        total_enhanced = 0

        with self.driver.session() as session:
            # Get total count
            count_query = f"""
                {match_pattern}
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE9'
                AND NOT n:IT_INFRASTRUCTURE
                RETURN count(n) as count
            """
            count_result = session.run(count_query)
            total_nodes = count_result.single()["count"]

            if total_nodes == 0:
                self._log(
                    "no_nodes_to_enhance",
                    "INFO",
                    {"node_type": node_type_key}
                )
                return 0

            # Process in batches
            for offset in range(0, total_nodes, batch_size):
                enhance_query = f"""
                    {match_pattern}
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE9'
                    AND NOT n:IT_INFRASTRUCTURE
                    WITH n
                    SKIP {offset}
                    LIMIT {batch_size}
                    SET n:{':'.join(labels_to_add)}
                    RETURN count(n) as enhanced
                """

                result = session.run(enhance_query)
                batch_enhanced = result.single()["enhanced"]
                total_enhanced += batch_enhanced

                self._log(
                    "add_labels_batch",
                    "SUCCESS",
                    {
                        "node_type": node_type_key,
                        "batch_offset": offset,
                        "batch_size": batch_enhanced,
                        "labels_added": labels_to_add,
                        "progress": f"{total_enhanced}/{total_nodes}"
                    }
                )

        return total_enhanced

    def enhance_all_wave_9_nodes(self) -> Dict[str, int]:
        """
        Enhance all Wave 9 nodes with multi-label strategy

        Returns:
            Dict with enhancement statistics per node type
        """
        print("=" * 80)
        print("WAVE 9 LABEL ENHANCEMENT")
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
                print(f"  Expected nodes: {expected_count}")
                enhancement_stats[node_type_key] = {
                    "expected": expected_count,
                    "enhanced": expected_count,
                    "labels_added": [],
                    "status": "SKIPPED"
                }
                print()
                continue

            print(f"  Adding labels: {', '.join(labels_to_add)}")
            print(f"  Expected nodes: {expected_count}")

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
                print(f"  ✅ Enhanced {enhanced_count} nodes")
            elif enhanced_count == 0 and expected_count > 0:
                print(f"  ⚠️  No nodes found to enhance (may already be labeled)")
            else:
                print(f"  ⚠️  Warning: Expected {expected_count}, enhanced {enhanced_count}")

            print()

        return enhancement_stats

    def validate_label_additions(self) -> Dict[str, Any]:
        """
        Validate that all Wave 9 nodes have correct labels

        Returns:
            Dict with validation results
        """
        print("Validating label additions...")

        with self.driver.session() as session:
            # Check that all Wave 9 nodes have IT_INFRASTRUCTURE label
            result = session.run("""
                MATCH (n:IT_INFRASTRUCTURE)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE9'
                RETURN count(n) as count
            """)
            it_infra_count = result.single()["count"]

            # Check node type specific labels
            node_type_validations = {}
            for node_type, config in self.wave_config['node_type_mappings'].items():
                expected_labels = set(config['final_labels'])
                expected_count = config['count']

                # Build label filter query
                label_filter = ':'.join(expected_labels)
                result = session.run(f"""
                    MATCH (n:{label_filter})
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE9'
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
            it_infra_count == 5000 and
            all(v["valid"] for v in node_type_validations.values())
        )

        validation_result = {
            "it_infrastructure_labeled": it_infra_count,
            "expected_total": 5000,
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
        Execute complete Wave 9 label enhancement workflow

        Returns:
            bool: True if successful
        """
        try:
            # Pre-flight validation
            print("=" * 80)
            print("PHASE 1: WAVE 9 LABEL ENHANCEMENT")
            print("=" * 80)
            print()

            print("[1/7] Validating Wave 9 exists...")
            if not self.validate_wave_9_exists():
                print("❌ Wave 9 validation failed")
                return False
            print("✅ Wave 9 exists (5,000 nodes)")
            print()

            print("[2/7] Getting current node types...")
            node_types = self.get_wave_9_node_types()
            print(f"✅ Found {len(node_types)} node types")
            print()

            print("[3/7] Creating pre-enhancement checkpoint...")
            checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 9 Label Enhancement - Start",
                phase="PHASE_1",
                wave="WAVE9"
            )
            print(f"✅ Checkpoint created: {checkpoint_id}")
            print()

            print("[4/7] Enhancing all Wave 9 nodes...")
            enhancement_stats = self.enhance_all_wave_9_nodes()
            total_enhanced = sum(s["enhanced"] for s in enhancement_stats.values())
            print(f"✅ Enhanced {total_enhanced} nodes across {len(enhancement_stats)} types")
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
                operation_name="Wave 9 Label Enhancement - Complete",
                phase="PHASE_1",
                wave="WAVE9",
                metadata={
                    "enhancement_stats": enhancement_stats,
                    "validation": validation
                }
            )
            print(f"✅ Final checkpoint created: {final_checkpoint_id}")
            print()

            print("=" * 80)
            print("✅ WAVE 9 LABEL ENHANCEMENT COMPLETE")
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
    enhancer = Wave9LabelEnhancer()
    success = enhancer.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
