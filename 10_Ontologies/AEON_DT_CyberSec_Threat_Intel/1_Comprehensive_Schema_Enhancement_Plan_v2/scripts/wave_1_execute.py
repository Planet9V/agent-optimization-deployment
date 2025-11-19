#!/usr/bin/env python3
"""
Wave 1 Master Coordinator: SAREF Core Foundation
Executes all Wave 1 scripts with comprehensive validation

Wave 1 Target: 5,000 SAREF nodes
- Devices & Properties: 2,000 (800 Device + 1,200 Property)
- Measurements: 1,500
- Services & Functions: 900 (600 Service + 300 Function)
- Commands, States & Units: 600 (400 Command + 100 State + 100 UnitOfMeasure)
"""
import logging
import sys
from datetime import datetime
from pathlib import Path
from neo4j import GraphDatabase

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent))

from wave_1_devices_properties import Wave1DevicesPropertiesExecutor
from wave_1_measurements import Wave1MeasurementsExecutor
from wave_1_services_functions import Wave1ServicesFunctionsExecutor
from wave_1_commands_states_units import Wave1CommandsStatesUnitsExecutor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Wave1MasterCoordinator:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.expected_cve_count = 267487
        self.target_wave1_nodes = 5000

    def validate_categories(self):
        """Validate node counts by category"""
        logging.info("🔍 Validating Wave 1 categories...")

        categories = {
            "Devices & Properties": ["Device", "Property"],
            "Measurements": ["Measurement"],
            "Services & Functions": ["Service", "Function"],
            "Commands, States & Units": ["Command", "State", "UnitOfMeasure"]
        }

        expected_totals = {
            "Devices & Properties": 2000,
            "Measurements": 1500,
            "Services & Functions": 900,
            "Commands, States & Units": 600
        }

        expected_by_type = {
            "Device": 800,
            "Property": 1200,
            "Measurement": 1500,
            "Service": 600,
            "Function": 300,
            "Command": 400,
            "State": 100,
            "UnitOfMeasure": 100
        }

        results = {}
        with self.driver.session() as session:
            for category, types in categories.items():
                total = 0
                for node_type in types:
                    result = session.run(
                        f"MATCH (n:{node_type}) WHERE n.created_by = 'AEON_INTEGRATION_WAVE1' RETURN count(n) as count"
                    )
                    count = result.single()['count']

                    # Validate individual type count
                    expected = expected_by_type[node_type]
                    if count != expected:
                        logging.error(f"❌ {node_type}: {count} (expected {expected})")
                        raise ValueError(f"{node_type} count mismatch: {count} != {expected}")

                    logging.info(f"✅ {node_type}: {count}")
                    total += count

                results[category] = total
                expected = expected_totals[category]

                if total == expected:
                    logging.info(f"✅ {category}: {total} (expected {expected})")
                else:
                    logging.error(f"❌ {category}: {total} (expected {expected})")
                    raise ValueError(f"{category} count mismatch")

        return results

    def validate_wave1_total(self):
        """Validate total Wave 1 node count"""
        logging.info("🔍 Validating total Wave 1 nodes...")

        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                RETURN count(n) as total
            """)
            total = result.single()['total']

            if total == self.target_wave1_nodes:
                logging.info(f"✅ Total Wave 1 nodes: {total} (target {self.target_wave1_nodes})")
                return total
            else:
                logging.error(f"❌ Total Wave 1 nodes: {total} (target {self.target_wave1_nodes})")
                raise ValueError(f"Wave 1 node count mismatch: {total} != {self.target_wave1_nodes}")

    def validate_cve_preservation(self):
        """Verify CVE nodes are intact"""
        logging.info("🔍 Validating CVE preservation...")

        with self.driver.session() as session:
            result = session.run("""
                MATCH (n:CVE)
                RETURN count(n) as total
            """)
            total = result.single()['total']

            if total == self.expected_cve_count:
                logging.info(f"✅ CVE nodes preserved: {total}")
                return total
            else:
                logging.error(f"❌ CVE nodes: {total} (expected {self.expected_cve_count})")
                raise ValueError(f"CVE preservation failed: {total} != {self.expected_cve_count}")

    def validate_uniqueness(self):
        """Validate all node_id values are unique"""
        logging.info("🔍 Validating node_id uniqueness...")

        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE1'
                WITH n.node_id as node_id, count(*) as cnt
                WHERE cnt > 1
                RETURN count(*) as duplicates
            """)
            duplicates = result.single()['duplicates']

            if duplicates == 0:
                logging.info(f"✅ All {self.target_wave1_nodes} node_id values are unique")
                return True
            else:
                logging.error(f"❌ Found {duplicates} duplicate node_id values")
                raise ValueError(f"Duplicate node_id values detected: {duplicates}")

    def execute(self):
        """Execute all Wave 1 scripts with validation"""
        overall_start = datetime.utcnow()

        try:
            logging.info("=" * 80)
            logging.info("🚀 WAVE 1: SAREF CORE FOUNDATION - MASTER COORDINATOR")
            logging.info("=" * 80)
            logging.info(f"Target: {self.target_wave1_nodes} nodes")
            logging.info(f"Started: {overall_start.isoformat()}")
            logging.info("")

            # Track individual script performance
            script_metrics = []

            # Execute Script 1: Devices & Properties
            logging.info("📦 Executing Script 1: Devices & Properties (2,000 nodes)")
            script_start = datetime.utcnow()
            executor1 = Wave1DevicesPropertiesExecutor()
            executor1.execute()
            script_duration = (datetime.utcnow() - script_start).total_seconds()
            script_metrics.append({
                "script": "wave_1_devices_properties.py",
                "nodes": 2000,
                "duration": script_duration,
                "rate": 2000 / script_duration
            })
            logging.info("")

            # Execute Script 2: Measurements
            logging.info("📦 Executing Script 2: Measurements (1,500 nodes)")
            script_start = datetime.utcnow()
            executor2 = Wave1MeasurementsExecutor()
            executor2.execute()
            script_duration = (datetime.utcnow() - script_start).total_seconds()
            script_metrics.append({
                "script": "wave_1_measurements.py",
                "nodes": 1500,
                "duration": script_duration,
                "rate": 1500 / script_duration
            })
            logging.info("")

            # Execute Script 3: Services & Functions
            logging.info("📦 Executing Script 3: Services & Functions (900 nodes)")
            script_start = datetime.utcnow()
            executor3 = Wave1ServicesFunctionsExecutor()
            executor3.execute()
            script_duration = (datetime.utcnow() - script_start).total_seconds()
            script_metrics.append({
                "script": "wave_1_services_functions.py",
                "nodes": 900,
                "duration": script_duration,
                "rate": 900 / script_duration
            })
            logging.info("")

            # Execute Script 4: Commands, States & Units
            logging.info("📦 Executing Script 4: Commands, States & Units (600 nodes)")
            script_start = datetime.utcnow()
            executor4 = Wave1CommandsStatesUnitsExecutor()
            executor4.execute()
            script_duration = (datetime.utcnow() - script_start).total_seconds()
            script_metrics.append({
                "script": "wave_1_commands_states_units.py",
                "nodes": 600,
                "duration": script_duration,
                "rate": 600 / script_duration
            })
            logging.info("")

            # Comprehensive Validation
            logging.info("=" * 80)
            logging.info("🔍 COMPREHENSIVE VALIDATION")
            logging.info("=" * 80)

            # Validate categories
            category_results = self.validate_categories()
            logging.info("")

            # Validate total Wave 1 nodes
            wave1_total = self.validate_wave1_total()
            logging.info("")

            # Validate CVE preservation
            cve_count = self.validate_cve_preservation()
            logging.info("")

            # Validate uniqueness
            self.validate_uniqueness()
            logging.info("")

            # Calculate overall metrics
            overall_duration = (datetime.utcnow() - overall_start).total_seconds()
            overall_rate = self.target_wave1_nodes / overall_duration

            # Final Report
            logging.info("=" * 80)
            logging.info("✅ WAVE 1 COMPLETION REPORT")
            logging.info("=" * 80)
            logging.info(f"Total Nodes Created: {wave1_total}")
            logging.info(f"Total Duration: {overall_duration:.2f} seconds")
            logging.info(f"Overall Rate: {overall_rate:.2f} nodes/second")
            logging.info("")

            logging.info("📊 Per-Script Performance:")
            for metrics in script_metrics:
                logging.info(f"  {metrics['script']}")
                logging.info(f"    Nodes: {metrics['nodes']}")
                logging.info(f"    Time: {metrics['duration']:.2f}s")
                logging.info(f"    Rate: {metrics['rate']:.2f} nodes/s")
            logging.info("")

            logging.info("📋 Category Breakdown:")
            for category, count in category_results.items():
                logging.info(f"  {category}: {count}")
            logging.info("")

            logging.info("🎯 Validation Results:")
            logging.info(f"  ✅ Total Wave 1 Nodes: {wave1_total} (target {self.target_wave1_nodes})")
            logging.info(f"  ✅ CVE Preservation: {cve_count} nodes intact")
            logging.info(f"  ✅ Uniqueness: All {wave1_total} node_id values unique")
            logging.info("")

            logging.info("🏆 Knowledge Graph Statistics:")
            total_nodes = cve_count + wave1_total
            logging.info(f"  Total Nodes: {total_nodes:,}")
            logging.info(f"    CVE Baseline: {cve_count:,}")
            logging.info(f"    Wave 1 (SAREF Core): {wave1_total:,}")
            logging.info("")

            logging.info("=" * 80)
            logging.info("✅ WAVE 1: SAREF CORE FOUNDATION - COMPLETE")
            logging.info("=" * 80)

        except Exception as e:
            logging.error(f"❌ Wave 1 execution failed: {e}")
            raise
        finally:
            self.driver.close()

if __name__ == "__main__":
    Wave1MasterCoordinator().execute()
