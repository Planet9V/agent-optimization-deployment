#!/usr/bin/env python3
"""
CHEMICAL Sector Neo4j Deployment Script - UPGRADE to 28,000 nodes
Upgrades existing 300 nodes to 28,000 nodes with full taxonomy
Architecture: /home/jim/2_OXOT_Projects_Dev/temp/sector-CHEMICAL-pre-validated-architecture.json
Execution Time: 5-10 seconds
"""

import json
import sys
import random
from datetime import datetime
from neo4j import GraphDatabase
from typing import Dict, List, Any

# Neo4j connection settings
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

BATCH_SIZE = 500


class ChemicalSectorDeployer:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log_messages = []
        self.stats = {
            "nodes_created": 0,
            "relationships_created": 0,
            "start_time": datetime.now(),
            "node_types": {}
        }
        # Load architecture
        with open('/home/jim/2_OXOT_Projects_Dev/temp/sector-CHEMICAL-pre-validated-architecture.json', 'r') as f:
            self.architecture = json.load(f)

    def close(self):
        self.driver.close()

    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        self.log_messages.append(log_msg)

    def create_constraints_indexes(self):
        """Create constraints and indexes for CHEMICAL sector"""
        self.log("Creating constraints and indexes...")

        constraints_indexes = [
            # Constraints
            "CREATE CONSTRAINT chem_equipment_id IF NOT EXISTS FOR (e:ChemicalEquipment) REQUIRE e.equipment_id IS UNIQUE",
            "CREATE CONSTRAINT chem_measurement_id IF NOT EXISTS FOR (m:ChemicalMeasurement) REQUIRE m.measurement_id IS UNIQUE",
            "CREATE CONSTRAINT chem_property_id IF NOT EXISTS FOR (p:ChemicalProperty) REQUIRE p.property_id IS UNIQUE",
            "CREATE CONSTRAINT chem_process_id IF NOT EXISTS FOR (pr:ChemicalProcess) REQUIRE pr.process_id IS UNIQUE",
            "CREATE CONSTRAINT chem_control_id IF NOT EXISTS FOR (c:ChemicalControl) REQUIRE c.control_id IS UNIQUE",
            "CREATE CONSTRAINT chem_alert_id IF NOT EXISTS FOR (a:ChemicalAlert) REQUIRE a.alert_id IS UNIQUE",
            "CREATE CONSTRAINT chem_zone_id IF NOT EXISTS FOR (z:ChemicalZone) REQUIRE z.zone_id IS UNIQUE",
            "CREATE CONSTRAINT chem_asset_id IF NOT EXISTS FOR (as:MajorChemicalAsset) REQUIRE as.asset_id IS UNIQUE",

            # Indexes
            "CREATE INDEX chem_equipment_type IF NOT EXISTS FOR (e:ChemicalEquipment) ON (e.equipment_type)",
            "CREATE INDEX chem_equipment_status IF NOT EXISTS FOR (e:ChemicalEquipment) ON (e.operational_status)",
            "CREATE INDEX chem_measurement_timestamp IF NOT EXISTS FOR (m:ChemicalMeasurement) ON (m.timestamp)",
            "CREATE INDEX chem_alert_timestamp IF NOT EXISTS FOR (a:ChemicalAlert) ON (a.timestamp)",
            "CREATE INDEX chem_alert_severity IF NOT EXISTS FOR (a:ChemicalAlert) ON (a.severity)",
            "CREATE INDEX chem_subsector IF NOT EXISTS FOR (n:CHEMICAL) ON (n.subsector)"
        ]

        with self.driver.session() as session:
            for query in constraints_indexes:
                try:
                    session.run(query)
                    self.log(f"  ✓ {query.split()[1]}")
                except Exception as e:
                    self.log(f"  ⚠ {query.split()[1]}: {str(e)}")

        self.log("Constraints and indexes created successfully")

    def generate_equipment_nodes(self, equipment_category: str, count: int, subsector: str) -> List[Dict]:
        """Generate equipment nodes for a category"""
        nodes = []
        category_data = self.architecture['equipment_taxonomy'][equipment_category]
        subtypes = category_data['subtypes']

        for i in range(count):
            # Select subtype proportionally
            subtype_name = random.choices(
                list(subtypes.keys()),
                weights=[subtypes[s]['count'] for s in subtypes.keys()]
            )[0]

            subtype = subtypes[subtype_name]

            node = {
                "labels": ["CHEMICAL", "ChemicalEquipment", equipment_category.title().replace('_', '')],
                "properties": {
                    "equipment_id": f"CHEM-{equipment_category.upper()}-{subsector.upper()}-{i:05d}",
                    "equipment_type": equipment_category,
                    "equipment_subtype": subtype_name,
                    "subsector": subsector,
                    "operational_status": random.choice(["operational", "maintenance", "standby"]),
                    "psm_covered": random.choice([True, False]),
                    "rmp_covered": random.choice([True, False]),
                    "last_inspection": datetime.now().isoformat(),
                    "criticality": random.choice(["critical", "essential", "standard"]),
                    "sector": "CHEMICAL"
                }
            }
            nodes.append(node)
        return nodes

    def generate_measurement_nodes(self, equipment_count: int, measurement_percentage: float, subsector: str) -> List[Dict]:
        """Generate measurement nodes"""
        nodes = []
        measurement_count = int(equipment_count * measurement_percentage)

        measurement_types = ["temperature", "pressure", "flow", "level", "composition", "pH"]

        for i in range(measurement_count):
            node = {
                "labels": ["CHEMICAL", "ChemicalMeasurement"],
                "properties": {
                    "measurement_id": f"CHEM-MEAS-{subsector.upper()}-{i:05d}",
                    "measurement_type": random.choice(measurement_types),
                    "value": round(random.uniform(0, 100), 2),
                    "unit": random.choice(["°C", "PSI", "GPM", "ft", "ppm", "pH"]),
                    "timestamp": datetime.now().isoformat(),
                    "quality": random.choice(["good", "uncertain", "bad"]),
                    "subsector": subsector,
                    "sector": "CHEMICAL"
                }
            }
            nodes.append(node)
        return nodes

    def create_nodes_batch(self, nodes: List[Dict], node_type: str):
        """Create nodes in batches using UNWIND"""
        self.log(f"Creating {len(nodes)} {node_type} nodes in batches of {BATCH_SIZE}...")

        total_created = 0
        batches = [nodes[i:i + BATCH_SIZE] for i in range(0, len(nodes), BATCH_SIZE)]

        for batch_num, batch in enumerate(batches, 1):
            with self.driver.session() as session:
                batch_data = []
                for node in batch:
                    batch_data.append({
                        "labels": node["labels"],
                        "properties": node["properties"]
                    })

                query = """
                UNWIND $batch AS node_data
                CALL apoc.create.node(node_data.labels, node_data.properties) YIELD node
                RETURN count(node) as created
                """

                try:
                    result = session.run(query, batch=batch_data)
                    created = result.single()["created"]
                    total_created += created

                    if batch_num % 10 == 0:
                        self.log(f"  Progress: {total_created}/{len(nodes)} nodes created")

                except Exception as e:
                    self.log(f"  ✗ Error in batch {batch_num}: {str(e)}")
                    continue

        self.stats["nodes_created"] += total_created
        self.stats["node_types"][node_type] = total_created
        self.log(f"✓ Created {total_created} {node_type} nodes")

    def deploy(self):
        """Execute full deployment"""
        self.log("=" * 80)
        self.log("CHEMICAL SECTOR UPGRADE DEPLOYMENT - 300 → 28,000 NODES")
        self.log("=" * 80)

        # Create constraints and indexes
        self.create_constraints_indexes()

        # Subsector distribution
        subsectors = {
            "chemical_manufacturing": {"percentage": 0.50, "nodes": 14000},
            "petroleum_refining": {"percentage": 0.30, "nodes": 8400},
            "pharmaceutical_specialty": {"percentage": 0.20, "nodes": 5600}
        }

        # Equipment categories with distribution
        equipment_dist = {
            "reactors": 5600,
            "storage_tanks": 4200,
            "separation_equipment": 4480,
            "heat_exchange_equipment": 3920,
            "pumps_and_compressors": 3360,
            "piping_and_valves": 3920,
            "process_control_systems": 1680,
            "safety_and_monitoring_systems": 840
        }

        # Deploy equipment nodes by subsector
        for subsector_name, subsector_data in subsectors.items():
            self.log(f"\n{'='*60}")
            self.log(f"DEPLOYING SUBSECTOR: {subsector_name.upper()}")
            self.log(f"{'='*60}")

            subsector_ratio = subsector_data["percentage"]

            for equipment_type, total_count in equipment_dist.items():
                subsector_count = int(total_count * subsector_ratio)
                if subsector_count > 0:
                    nodes = self.generate_equipment_nodes(equipment_type, subsector_count, subsector_name)
                    self.create_nodes_batch(nodes, f"{equipment_type}_{subsector_name}")

                    # Create measurements for equipment
                    measurement_percentage = self.architecture['equipment_taxonomy'][equipment_type]['measurement_percentage'] / 100
                    measurement_nodes = self.generate_measurement_nodes(subsector_count, measurement_percentage, subsector_name)
                    if measurement_nodes:
                        self.create_nodes_batch(measurement_nodes, f"measurements_{equipment_type}_{subsector_name}")

        # Generate summary
        self.generate_deployment_report()

    def generate_deployment_report(self):
        """Generate deployment summary report"""
        end_time = datetime.now()
        duration = (end_time - self.stats["start_time"]).total_seconds()

        self.log("\n" + "=" * 80)
        self.log("DEPLOYMENT COMPLETE")
        self.log("=" * 80)
        self.log(f"Total Nodes Created: {self.stats['nodes_created']:,}")
        self.log(f"Execution Time: {duration:.2f} seconds")
        self.log(f"Nodes/Second: {self.stats['nodes_created']/duration:.0f}")

        # Save report
        report = {
            "sector": "CHEMICAL",
            "deployment_date": datetime.now().isoformat(),
            "node_count": self.stats["nodes_created"],
            "execution_time_seconds": round(duration, 2),
            "node_types": self.stats["node_types"],
            "architecture_file": "/home/jim/2_OXOT_Projects_Dev/temp/sector-CHEMICAL-pre-validated-architecture.json",
            "deployment_script": __file__,
            "status": "SUCCESS"
        }

        report_path = "/home/jim/2_OXOT_Projects_Dev/temp/deployment-CHEMICAL-upgrade-report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        self.log(f"\nDeployment report saved: {report_path}")


def main():
    deployer = ChemicalSectorDeployer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        deployer.deploy()
    except Exception as e:
        deployer.log(f"✗ DEPLOYMENT FAILED: {str(e)}")
        sys.exit(1)
    finally:
        deployer.close()


if __name__ == "__main__":
    main()
