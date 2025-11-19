#!/usr/bin/env python3
"""
Wave 2 Label Enhancement - Add Subdomain and Functional Role Labels
Non-destructive label addition to 15,000 Wave 2 nodes after re-import

Operation: ADD_LABELS (preserves all existing data)
Target: 15,000 Wave 2 nodes
Domain: WATER
Labels Added: Subdomain (Water_Treatment/Water_Distribution/Water_Collection) + Functional Role (Asset/Monitoring/Control/Process)
Pagination: SKIP 0 pattern (prevents offset drift)

Generated: 2025-10-31
Version: 1.0.0
Pattern: Proven from Wave 1
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


class Wave2LabelEnhancer:
    """Enhance Wave 2 nodes with subdomain and functional role labels"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        project_root: Path = None
    ):
        """Initialize Wave 2 Label Enhancer"""
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "wave_2_label_enhancement.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Load master taxonomy
        taxonomy_path = self.project_root / "master_taxonomy.yaml"
        with open(taxonomy_path, 'r') as f:
            self.taxonomy = yaml.safe_load(f)

        self.wave_config = self.taxonomy['wave_2']
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

    def add_labels_by_property_filter(
        self,
        base_label: str,
        property_filter: Dict[str, Any],
        labels_to_add: list,
        batch_size: int = 50,
        description: str = ""
    ) -> int:
        """
        Add labels to nodes matching a property filter

        Args:
            base_label: Base node label to match (WaterDevice, WaterProperty, etc.)
            property_filter: Dictionary of property filters
            labels_to_add: Labels to add (e.g., [WATER, Water_Treatment, Asset])
            batch_size: Number of nodes to process per batch
            description: Human-readable description for logging

        Returns:
            int: Number of nodes enhanced
        """
        total_enhanced = 0
        batch_num = 0

        # Build WHERE clause from property filter
        where_conditions = []
        for key, value in property_filter.items():
            if isinstance(value, list):
                # Handle IN clause for lists
                values_str = ", ".join([f"'{v}'" for v in value])
                where_conditions.append(f"n.{key} IN [{values_str}]")
            else:
                where_conditions.append(f"n.{key} = '{value}'")

        where_clause = " AND ".join(where_conditions) if where_conditions else "true"

        # Determine check label (WATER domain label)
        check_label = "WATER"

        with self.driver.session() as session:
            # Process until no nodes remain
            while True:
                # Always SKIP 0 - take first N unlabeled nodes
                enhance_query = f"""
                    MATCH (n:{base_label})
                    WHERE {where_clause}
                    AND NOT n:{check_label}
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
                        "base_label": base_label,
                        "description": description,
                        "batch_number": batch_num,
                        "batch_size": batch_enhanced,
                        "labels_added": labels_to_add,
                        "cumulative_total": total_enhanced
                    }
                )

                # Progress indicator every 500 nodes
                if total_enhanced % 500 == 0:
                    print(f"  Progress: {total_enhanced:,} nodes enhanced...")

        return total_enhanced

    def add_tracking_property(
        self,
        base_label: str,
        batch_size: int = 100
    ) -> int:
        """
        Add created_by tracking property to existing Wave 2 nodes

        Args:
            base_label: Base node label to match
            batch_size: Number of nodes to process per batch

        Returns:
            int: Number of nodes updated
        """
        total_updated = 0

        with self.driver.session() as session:
            while True:
                update_query = f"""
                    MATCH (n:{base_label})
                    WHERE n.created_by IS NULL
                    AND (n.deviceId STARTS WITH 'water:' OR
                         n.propertyId STARTS WITH 'water:' OR
                         n.measurementId STARTS WITH 'water:' OR
                         n.processId STARTS WITH 'water:' OR
                         n.scadaId STARTS WITH 'water:' OR
                         n.zoneId STARTS WITH 'water:' OR
                         n.alertId STARTS WITH 'water:')
                    WITH n LIMIT {batch_size}
                    SET n.created_by = 'AEON_INTEGRATION_WAVE2'
                    RETURN count(n) as updated
                """

                result = session.run(update_query)
                batch_updated = result.single()["updated"]

                if batch_updated == 0:
                    break

                total_updated += batch_updated

                if total_updated % 1000 == 0:
                    print(f"  Progress: {total_updated:,} nodes updated...")

        return total_updated

    def enhance_all_wave2_nodes(self) -> Dict[str, int]:
        """
        Enhance all Wave 2 nodes with WATER domain + subdomain + functional role labels

        Maps existing rich water infrastructure nodes to taxonomy structure

        Returns:
            Dict with enhancement statistics per category
        """
        print("=" * 80)
        print("WAVE 2 LABEL ENHANCEMENT - HYBRID APPROACH")
        print("=" * 80)
        print()

        enhancement_stats = {}

        # Step 1: Add tracking property to all Wave 2 nodes
        print("Step 1: Adding tracking property to existing nodes...")
        node_types = ["WaterDevice", "WaterProperty", "Measurement", "TreatmentProcess",
                     "SCADASystem", "WaterZone", "WaterAlert"]

        for node_type in node_types:
            updated = self.add_tracking_property(node_type)
            print(f"  ✅ Added tracking to {updated:,} {node_type} nodes")
        print()

        # Step 2: Map existing nodes to taxonomy structure
        # Strategy: Add WATER domain + appropriate subdomain + functional role based on properties

        print("Step 2: Adding taxonomy labels to existing nodes...")
        print()

        # WaterDevice nodes -> Map by waterDeviceType property
        print("Processing WaterDevice nodes (1,500)...")

        # Pumps -> Water_Distribution + Asset
        pumps = self.add_labels_by_property_filter(
            "WaterDevice",
            {"waterDeviceType": "Pump"},
            ["WATER", "Water_Distribution", "Asset"],
            description="Pumps"
        )
        enhancement_stats["WaterDevice_Pump"] = {"enhanced": pumps, "labels": ["WATER", "Water_Distribution", "Asset"]}
        print(f"  ✅ Pumps: {pumps:,}")

        # Valves -> Water_Distribution + Control
        valves = self.add_labels_by_property_filter(
            "WaterDevice",
            {"waterDeviceType": "Valve"},
            ["WATER", "Water_Distribution", "Control"],
            description="Valves"
        )
        enhancement_stats["WaterDevice_Valve"] = {"enhanced": valves, "labels": ["WATER", "Water_Distribution", "Control"]}
        print(f"  ✅ Valves: {valves:,}")

        # Sensors -> Water_Treatment + Monitoring
        sensors = self.add_labels_by_property_filter(
            "WaterDevice",
            {"waterDeviceType": "Sensor"},
            ["WATER", "Water_Treatment", "Monitoring"],
            description="Sensors"
        )
        enhancement_stats["WaterDevice_Sensor"] = {"enhanced": sensors, "labels": ["WATER", "Water_Treatment", "Monitoring"]}
        print(f"  ✅ Sensors: {sensors:,}")

        # Chlorinators, Filters -> Water_Treatment + Process
        treatment = self.add_labels_by_property_filter(
            "WaterDevice",
            {"waterDeviceType": ["Chlorinator", "Filter"]},
            ["WATER", "Water_Treatment", "Process"],
            description="Treatment Equipment"
        )
        enhancement_stats["WaterDevice_Treatment"] = {"enhanced": treatment, "labels": ["WATER", "Water_Treatment", "Process"]}
        print(f"  ✅ Treatment Equipment: {treatment:,}")

        # RTUs -> Water_Distribution + Control
        rtus = self.add_labels_by_property_filter(
            "WaterDevice",
            {"waterDeviceType": "RTU"},
            ["WATER", "Water_Distribution", "Control"],
            description="RTUs"
        )
        enhancement_stats["WaterDevice_RTU"] = {"enhanced": rtus, "labels": ["WATER", "Water_Distribution", "Control"]}
        print(f"  ✅ RTUs: {rtus:,}")

        # Flowmeters -> Water_Distribution + Monitoring
        flowmeters = self.add_labels_by_property_filter(
            "WaterDevice",
            {"waterDeviceType": "Flowmeter"},
            ["WATER", "Water_Distribution", "Monitoring"],
            description="Flowmeters"
        )
        enhancement_stats["WaterDevice_Flowmeter"] = {"enhanced": flowmeters, "labels": ["WATER", "Water_Distribution", "Monitoring"]}
        print(f"  ✅ Flowmeters: {flowmeters:,}")

        # Turbidity Sensors -> Water_Treatment + Monitoring
        turbidity_sensors = self.add_labels_by_property_filter(
            "WaterDevice",
            {"waterDeviceType": "Turbidity Sensor"},
            ["WATER", "Water_Treatment", "Monitoring"],
            description="Turbidity Sensors"
        )
        enhancement_stats["WaterDevice_TurbiditySensor"] = {"enhanced": turbidity_sensors, "labels": ["WATER", "Water_Treatment", "Monitoring"]}
        print(f"  ✅ Turbidity Sensors: {turbidity_sensors:,}")
        print()

        # WaterProperty nodes -> Map by waterPropertyCategory
        print("Processing WaterProperty nodes (3,000)...")

        # Chemical properties -> Water_Treatment + Monitoring
        chemical = self.add_labels_by_property_filter(
            "WaterProperty",
            {"waterPropertyCategory": "Chemical"},
            ["WATER", "Water_Treatment", "Monitoring"],
            description="Chemical Properties"
        )
        enhancement_stats["WaterProperty_Chemical"] = {"enhanced": chemical, "labels": ["WATER", "Water_Treatment", "Monitoring"]}
        print(f"  ✅ Chemical Properties: {chemical:,}")

        # Physical properties -> Water_Treatment + Monitoring
        physical = self.add_labels_by_property_filter(
            "WaterProperty",
            {"waterPropertyCategory": "Physical"},
            ["WATER", "Water_Treatment", "Monitoring"],
            description="Physical Properties"
        )
        enhancement_stats["WaterProperty_Physical"] = {"enhanced": physical, "labels": ["WATER", "Water_Treatment", "Monitoring"]}
        print(f"  ✅ Physical Properties: {physical:,}")

        # Biological properties -> Water_Treatment + Monitoring
        biological = self.add_labels_by_property_filter(
            "WaterProperty",
            {"waterPropertyCategory": "Biological"},
            ["WATER", "Water_Treatment", "Monitoring"],
            description="Biological Properties"
        )
        enhancement_stats["WaterProperty_Biological"] = {"enhanced": biological, "labels": ["WATER", "Water_Treatment", "Monitoring"]}
        print(f"  ✅ Biological Properties: {biological:,}")

        # Hydraulic properties -> Water_Distribution + Monitoring
        hydraulic = self.add_labels_by_property_filter(
            "WaterProperty",
            {"waterPropertyCategory": "Hydraulic"},
            ["WATER", "Water_Distribution", "Monitoring"],
            description="Hydraulic Properties"
        )
        enhancement_stats["WaterProperty_Hydraulic"] = {"enhanced": hydraulic, "labels": ["WATER", "Water_Distribution", "Monitoring"]}
        print(f"  ✅ Hydraulic Properties: {hydraulic:,}")
        print()

        # Measurement nodes -> Water_Treatment + Monitoring
        print("Processing Measurement nodes (9,000)...")
        measurements = self.add_labels_by_property_filter(
            "Measurement",
            {},  # No filter - all measurements
            ["WATER", "Water_Treatment", "Monitoring"],
            description="Measurements"
        )
        enhancement_stats["Measurement"] = {"enhanced": measurements, "labels": ["WATER", "Water_Treatment", "Monitoring"]}
        print(f"  ✅ Measurements: {measurements:,}")
        print()

        # TreatmentProcess nodes -> Water_Treatment + Process
        print("Processing TreatmentProcess nodes (500)...")
        processes = self.add_labels_by_property_filter(
            "TreatmentProcess",
            {},
            ["WATER", "Water_Treatment", "Process"],
            description="Treatment Processes"
        )
        enhancement_stats["TreatmentProcess"] = {"enhanced": processes, "labels": ["WATER", "Water_Treatment", "Process"]}
        print(f"  ✅ Treatment Processes: {processes:,}")
        print()

        # SCADASystem nodes -> Water_Distribution + Control
        print("Processing SCADASystem nodes (300)...")
        scada = self.add_labels_by_property_filter(
            "SCADASystem",
            {},
            ["WATER", "Water_Distribution", "Control"],
            description="SCADA Systems"
        )
        enhancement_stats["SCADASystem"] = {"enhanced": scada, "labels": ["WATER", "Water_Distribution", "Control"]}
        print(f"  ✅ SCADA Systems: {scada:,}")
        print()

        # WaterZone nodes -> Water_Distribution + Asset
        print("Processing WaterZone nodes (200)...")
        zones = self.add_labels_by_property_filter(
            "WaterZone",
            {},
            ["WATER", "Water_Distribution", "Asset"],
            description="Water Zones"
        )
        enhancement_stats["WaterZone"] = {"enhanced": zones, "labels": ["WATER", "Water_Distribution", "Asset"]}
        print(f"  ✅ Water Zones: {zones:,}")
        print()

        # WaterAlert nodes -> Water_Treatment + Monitoring
        print("Processing WaterAlert nodes (500)...")
        alerts = self.add_labels_by_property_filter(
            "WaterAlert",
            {},
            ["WATER", "Water_Treatment", "Monitoring"],
            description="Water Alerts"
        )
        enhancement_stats["WaterAlert"] = {"enhanced": alerts, "labels": ["WATER", "Water_Treatment", "Monitoring"]}
        print(f"  ✅ Water Alerts: {alerts:,}")
        print()

        return enhancement_stats

    def validate_label_additions(self) -> Dict[str, Any]:
        """
        Validate that all Wave 2 nodes have correct labels

        Returns:
            Dict with validation results
        """
        print("Validating label additions...")

        with self.driver.session() as session:
            # Check tracking property
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE2'
                RETURN count(n) as count
            """)
            tracking_count = result.single()["count"]

            # Check that all Wave 2 nodes have WATER domain label
            result = session.run("""
                MATCH (n:WATER)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE2'
                RETURN count(n) as count
            """)
            water_count = result.single()["count"]

            # Check subdomain labels
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE2'
                AND (n:Water_Treatment OR n:Water_Distribution OR n:Water_Collection)
                RETURN count(n) as count
            """)
            subdomain_count = result.single()["count"]

            # Check functional role labels
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE2'
                AND (n:Asset OR n:Monitoring OR n:Control OR n:Process)
                RETURN count(n) as count
            """)
            functional_role_count = result.single()["count"]

            # Get label distribution
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE2'
                RETURN labels(n) as labels, count(n) as count
                ORDER BY count DESC
                LIMIT 10
            """)
            label_distribution = [
                {"labels": record["labels"], "count": record["count"]}
                for record in result
            ]

        all_valid = (
            tracking_count == 15000 and
            water_count == 15000 and
            subdomain_count == 15000 and
            functional_role_count == 15000
        )

        validation_result = {
            "tracking_property": tracking_count,
            "water_labeled": water_count,
            "subdomain_labeled": subdomain_count,
            "functional_role_labeled": functional_role_count,
            "expected_total": 15000,
            "label_distribution": label_distribution,
            "all_valid": all_valid
        }

        status = "PASS" if all_valid else "PARTIAL"
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
        Execute complete Wave 2 label enhancement workflow

        Returns:
            bool: True if successful
        """
        try:
            print("=" * 80)
            print("PHASE 2: WAVE 2 LABEL ENHANCEMENT (15,000 nodes)")
            print("=" * 80)
            print()

            print("[1/5] Creating pre-enhancement checkpoint...")
            checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 2 Label Enhancement - Start",
                phase="PHASE_2",
                wave="WAVE2"
            )
            print(f"✅ Checkpoint created: {checkpoint_id}")
            print()

            print("[2/5] Enhancing all Wave 2 nodes...")
            enhancement_stats = self.enhance_all_wave2_nodes()
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
                operation_name="Wave 2 Label Enhancement - Complete",
                phase="PHASE_2",
                wave="WAVE2",
                metadata={
                    "enhancement_stats": enhancement_stats,
                    "validation": validation
                }
            )
            print(f"✅ Final checkpoint created: {final_checkpoint_id}")
            print()

            print("=" * 80)
            print("✅ WAVE 2 LABEL ENHANCEMENT COMPLETE")
            print("=" * 80)
            print()
            print(f"Enhanced: {total_enhanced:,} nodes")
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
    enhancer = Wave2LabelEnhancer()
    success = enhancer.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
