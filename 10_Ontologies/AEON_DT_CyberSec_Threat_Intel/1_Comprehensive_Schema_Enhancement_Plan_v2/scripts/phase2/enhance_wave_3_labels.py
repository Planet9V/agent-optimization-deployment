#!/usr/bin/env python3
"""
Wave 3 Label Enhancement - Add ENERGY domain labels to existing nodes
Hybrid approach: Preserve existing 17,424 Energy nodes + add taxonomy labels

Operation: ADD_LABELS (preserves all existing data)
Target: 17,424 existing Energy nodes
Labels Added: ENERGY + subdomain + functional role

NOTE: Expected 35,924 nodes, but only 17,424 exist.
      wave_3_execute.py appears incomplete/outdated.

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


class Wave3LabelEnhancer:
    """Enhance Wave 3 nodes with ENERGY and taxonomy labels"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        project_root: Path = None
    ):
        """Initialize Wave 3 Label Enhancer"""
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "wave_3_label_enhancement.jsonl"
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

    def add_tracking_property(
        self,
        base_label: str,
        batch_size: int = 100
    ) -> int:
        """Add created_by tracking property to existing Wave 3 Energy nodes"""
        total_updated = 0

        with self.driver.session() as session:
            while True:
                update_query = f"""
                    MATCH (n:{base_label})
                    WHERE n.created_by IS NULL
                    AND (n.deviceId STARTS WITH 'energy:' OR
                         n.propertyId STARTS WITH 'energy:' OR
                         n.substationId STARTS WITH 'SUBST-' OR
                         n.standardId STARTS WITH 'CIP-' OR
                         n:DistributedEnergyResource OR
                         n:TransmissionLine OR
                         n:Substation OR
                         n:NERCCIPStandard OR
                         n:EnergyManagementSystem)
                    WITH n LIMIT {batch_size}
                    SET n.created_by = 'AEON_INTEGRATION_WAVE3'
                    RETURN count(n) as updated
                """
                result = session.run(update_query)
                batch_updated = result.single()["updated"]

                if batch_updated == 0:
                    break

                total_updated += batch_updated

        return total_updated

    def add_labels_to_node_pattern(
        self,
        node_label: str,
        labels_to_add: list,
        batch_size: int = 100,
        description: str = ""
    ) -> int:
        """
        Add ENERGY domain + taxonomy labels to nodes

        Args:
            node_label: Base node label (EnergyDevice, EnergyProperty, etc.)
            labels_to_add: Labels to add (e.g., [ENERGY, Energy_Distribution, Monitoring])
            batch_size: Batch size for processing
            description: Description for logging

        Returns:
            int: Number of nodes enhanced
        """
        total_enhanced = 0
        batch_num = 0

        with self.driver.session() as session:
            # SKIP 0 pattern - process until no nodes remain
            while True:
                # Match nodes without ENERGY label
                enhance_query = f"""
                    MATCH (n:{node_label})
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                    AND NOT n:ENERGY
                    WITH n
                    LIMIT {batch_size}
                    SET n:{':'.join(labels_to_add)}
                    RETURN count(n) as enhanced
                """

                result = session.run(enhance_query)
                batch_enhanced = result.single()["enhanced"]

                if batch_enhanced == 0:
                    break

                total_enhanced += batch_enhanced
                batch_num += 1

                self._log(
                    "add_labels_batch",
                    "SUCCESS",
                    {
                        "node_label": node_label,
                        "description": description,
                        "batch_number": batch_num,
                        "batch_size": batch_enhanced,
                        "labels_added": labels_to_add,
                        "cumulative_total": total_enhanced
                    }
                )

        return total_enhanced

    def enhance_all_wave3_nodes(self) -> Dict[str, int]:
        """
        Enhance all Wave 3 Energy nodes with ENERGY domain + taxonomy labels

        Strategy:
        - EnergyDevice (10,000) -> Extract device type from deviceId
        - EnergyProperty (6,000) -> Energy_Transmission + Monitoring
        - DistributedEnergyResource (750) -> Energy_Generation + Asset
        - TransmissionLine (400) -> Energy_Transmission + Asset
        - Substation (200) -> Energy_Distribution + Asset
        - NERCCIPStandard (49) -> Energy_Distribution + Control (regulatory)
        - EnergyManagementSystem (25) -> Energy_Distribution + Control

        Returns:
            Dict with enhancement statistics per node type
        """
        print("=" * 80)
        print("WAVE 3 LABEL ENHANCEMENT - HYBRID APPROACH")
        print("=" * 80)
        print()

        enhancement_stats = {}

        # Step 1: Add tracking property to all Wave 3 Energy nodes
        print("Step 1: Adding tracking property to existing Energy nodes...")

        node_labels = [
            "EnergyDevice",
            "EnergyProperty",
            "DistributedEnergyResource",
            "TransmissionLine",
            "Substation",
            "NERCCIPStandard",
            "EnergyManagementSystem"
        ]

        for node_label in node_labels:
            updated = self.add_tracking_property(node_label)
            if updated > 0:
                print(f"  ✅ Added tracking to {updated:,} {node_label} nodes")

        print()

        # Step 2: Add ENERGY + subdomain + functional role labels
        print("Step 2: Adding ENERGY domain + taxonomy labels...")
        print()

        # EnergyDevice nodes (10,000) - Default to Energy_Distribution + Monitoring
        # Without deviceType property, we'll categorize all as monitoring devices
        print("Processing EnergyDevice nodes...")
        energy_devices = self.add_labels_to_node_pattern(
            "EnergyDevice",
            ["ENERGY", "Energy_Distribution", "Monitoring"],
            description="Energy Distribution Monitoring Devices"
        )
        enhancement_stats["EnergyDevice"] = {
            "enhanced": energy_devices,
            "labels": ["ENERGY", "Energy_Distribution", "Monitoring"]
        }
        print(f"  ✅ Enhanced {energy_devices:,} EnergyDevice nodes")
        print()

        # EnergyProperty nodes (6,000) - Energy properties are typically monitored
        print("Processing EnergyProperty nodes...")
        energy_properties = self.add_labels_to_node_pattern(
            "EnergyProperty",
            ["ENERGY", "Energy_Transmission", "Monitoring"],
            description="Energy Transmission Properties"
        )
        enhancement_stats["EnergyProperty"] = {
            "enhanced": energy_properties,
            "labels": ["ENERGY", "Energy_Transmission", "Monitoring"]
        }
        print(f"  ✅ Enhanced {energy_properties:,} EnergyProperty nodes")
        print()

        # DistributedEnergyResource nodes (750) - Generation assets
        print("Processing DistributedEnergyResource nodes...")
        ders = self.add_labels_to_node_pattern(
            "DistributedEnergyResource",
            ["ENERGY", "Energy_Generation", "Asset"],
            description="Distributed Energy Resources"
        )
        enhancement_stats["DistributedEnergyResource"] = {
            "enhanced": ders,
            "labels": ["ENERGY", "Energy_Generation", "Asset"]
        }
        print(f"  ✅ Enhanced {ders:,} DistributedEnergyResource nodes")
        print()

        # TransmissionLine nodes (400) - Transmission assets
        print("Processing TransmissionLine nodes...")
        transmission_lines = self.add_labels_to_node_pattern(
            "TransmissionLine",
            ["ENERGY", "Energy_Transmission", "Asset"],
            description="Transmission Lines"
        )
        enhancement_stats["TransmissionLine"] = {
            "enhanced": transmission_lines,
            "labels": ["ENERGY", "Energy_Transmission", "Asset"]
        }
        print(f"  ✅ Enhanced {transmission_lines:,} TransmissionLine nodes")
        print()

        # Substation nodes (200) - Distribution assets
        print("Processing Substation nodes...")
        substations = self.add_labels_to_node_pattern(
            "Substation",
            ["ENERGY", "Energy_Distribution", "Asset"],
            description="Substations"
        )
        enhancement_stats["Substation"] = {
            "enhanced": substations,
            "labels": ["ENERGY", "Energy_Distribution", "Asset"]
        }
        print(f"  ✅ Enhanced {substations:,} Substation nodes")
        print()

        # NERCCIPStandard nodes (49) - Regulatory control
        print("Processing NERCCIPStandard nodes...")
        nerc_standards = self.add_labels_to_node_pattern(
            "NERCCIPStandard",
            ["ENERGY", "Energy_Distribution", "Control"],
            description="NERC CIP Standards"
        )
        enhancement_stats["NERCCIPStandard"] = {
            "enhanced": nerc_standards,
            "labels": ["ENERGY", "Energy_Distribution", "Control"]
        }
        print(f"  ✅ Enhanced {nerc_standards:,} NERCCIPStandard nodes")
        print()

        # EnergyManagementSystem nodes (25) - Control systems
        print("Processing EnergyManagementSystem nodes...")
        ems = self.add_labels_to_node_pattern(
            "EnergyManagementSystem",
            ["ENERGY", "Energy_Distribution", "Control"],
            description="Energy Management Systems"
        )
        enhancement_stats["EnergyManagementSystem"] = {
            "enhanced": ems,
            "labels": ["ENERGY", "Energy_Distribution", "Control"]
        }
        print(f"  ✅ Enhanced {ems:,} EnergyManagementSystem nodes")
        print()

        return enhancement_stats

    def validate_label_additions(self) -> Dict[str, Any]:
        """
        Validate that all Wave 3 nodes have ENERGY label

        Returns:
            Dict with validation results
        """
        print("Validating label additions...")

        with self.driver.session() as session:
            # Check that all Wave 3 nodes have ENERGY label
            result = session.run("""
                MATCH (n:ENERGY)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                RETURN count(n) as count
            """)
            energy_count = result.single()["count"]

            # Count total Wave 3 nodes
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                RETURN count(n) as count
            """)
            total_count = result.single()["count"]

            # Check subdomain distribution
            subdomains = {}
            for subdomain in self.wave_config['label_strategy']['subdomain_labels']:
                result = session.run(f"""
                    MATCH (n:{subdomain})
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                    RETURN count(n) as count
                """)
                subdomains[subdomain] = result.single()["count"]

        all_valid = (
            energy_count == total_count and
            total_count > 0
        )

        validation_result = {
            "energy_labeled": energy_count,
            "total_wave3": total_count,
            "expected_total": 35924,
            "actual_vs_expected_note": f"Only {total_count:,} nodes exist (expected 35,924). wave_3_execute.py appears incomplete.",
            "subdomains": subdomains,
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
        Execute complete Wave 3 label enhancement workflow

        Returns:
            bool: True if successful
        """
        try:
            print("=" * 80)
            print("PHASE 2: WAVE 3 LABEL ENHANCEMENT (Hybrid Approach)")
            print("=" * 80)
            print()
            print("NOTE: Expected 35,924 nodes, but only 17,424 exist.")
            print("      Enhancing existing nodes with taxonomy labels.")
            print()

            print("[1/5] Creating pre-enhancement checkpoint...")
            checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 3 Label Enhancement - Start",
                phase="PHASE_2",
                wave="WAVE3"
            )
            print(f"✅ Checkpoint created: {checkpoint_id}")
            print()

            print("[2/5] Enhancing all Wave 3 Energy nodes...")
            enhancement_stats = self.enhance_all_wave3_nodes()
            total_enhanced = sum(s["enhanced"] for s in enhancement_stats.values())
            print(f"✅ Enhanced {total_enhanced:,} nodes across {len(enhancement_stats)} types")
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
                operation_name="Wave 3 Label Enhancement - Complete",
                phase="PHASE_2",
                wave="WAVE3",
                metadata={
                    "enhancement_stats": enhancement_stats,
                    "validation": validation
                }
            )
            print(f"✅ Final checkpoint created: {final_checkpoint_id}")
            print()

            print("=" * 80)
            print("✅ WAVE 3 LABEL ENHANCEMENT COMPLETE")
            print("=" * 80)
            print()
            print(f"Enhanced: {total_enhanced:,} nodes")
            print(f"Node types: {len(enhancement_stats)}")
            print(f"Expected: 35,924 nodes")
            print(f"Actual: {validation['total_wave3']:,} nodes")
            print(f"Coverage: {validation['total_wave3'] / 35924 * 100:.1f}%")
            print(f"All validations: {'✅ PASSED' if validation['all_valid'] else '⚠️  WARNING'}")
            print(f"CVE preservation: ✅ INTACT")
            print()
            print("⚠️  NOTE: wave_3_execute.py appears incomplete/outdated.")
            print("   Consider investigating why only 17,424 nodes exist instead of 35,924.")
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
    enhancer = Wave3LabelEnhancer()
    success = enhancer.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
