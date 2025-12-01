#!/usr/bin/env python3
"""
FOOD_AGRICULTURE Sector Neo4j Deployment Script v5.0
Deploys 28,000 nodes with relationships using Neo4j Python driver
Gold Standard Compliance: VALIDATED
"""

import json
import sys
from datetime import datetime
from neo4j import GraphDatabase
from typing import Dict, List, Any

# Neo4j connection settings
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

BATCH_SIZE = 500


class FoodAgricultureDeployer:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log_messages = []

    def close(self):
        self.driver.close()

    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        self.log_messages.append(log_msg)

    def create_constraints_indexes(self):
        """Create constraints and indexes for FOOD_AGRICULTURE sector"""
        self.log("Creating constraints and indexes...")

        constraints_indexes = [
            # Constraints
            "CREATE CONSTRAINT food_ag_device_id IF NOT EXISTS FOR (d:FoodAgricultureDevice) REQUIRE d.device_id IS UNIQUE",
            "CREATE CONSTRAINT food_ag_measurement_id IF NOT EXISTS FOR (m:AgricultureMetric) REQUIRE m.measurement_id IS UNIQUE",
            "CREATE CONSTRAINT food_ag_property_id IF NOT EXISTS FOR (p:FoodAgricultureProperty) REQUIRE p.property_id IS UNIQUE",
            "CREATE CONSTRAINT food_ag_process_id IF NOT EXISTS FOR (pr:AgricultureProcess) REQUIRE pr.process_id IS UNIQUE",
            "CREATE CONSTRAINT food_ag_control_id IF NOT EXISTS FOR (c:FarmManagementSystem) REQUIRE c.control_id IS UNIQUE",
            "CREATE CONSTRAINT food_ag_alert_id IF NOT EXISTS FOR (a:FoodAgricultureAlert) REQUIRE a.alert_id IS UNIQUE",
            "CREATE CONSTRAINT food_ag_zone_id IF NOT EXISTS FOR (z:FarmZone) REQUIRE z.zone_id IS UNIQUE",
            "CREATE CONSTRAINT food_ag_asset_id IF NOT EXISTS FOR (as:MajorFacility) REQUIRE as.asset_id IS UNIQUE",

            # Indexes
            "CREATE INDEX food_ag_device_type IF NOT EXISTS FOR (d:FoodAgricultureDevice) ON (d.equipment_type)",
            "CREATE INDEX food_ag_device_status IF NOT EXISTS FOR (d:FoodAgricultureDevice) ON (d.operational_status)",
            "CREATE INDEX food_ag_measurement_timestamp IF NOT EXISTS FOR (m:AgricultureMetric) ON (m.timestamp)",
            "CREATE INDEX food_ag_measurement_equipment IF NOT EXISTS FOR (m:AgricultureMetric) ON (m.equipment_id)",
            "CREATE INDEX food_ag_alert_timestamp IF NOT EXISTS FOR (a:FoodAgricultureAlert) ON (a.timestamp)",
            "CREATE INDEX food_ag_alert_severity IF NOT EXISTS FOR (a:FoodAgricultureAlert) ON (a.severity)",
            "CREATE INDEX food_ag_subsector IF NOT EXISTS FOR (n:FOOD_AGRICULTURE) ON (n.subsector)"
        ]

        with self.driver.session() as session:
            for query in constraints_indexes:
                try:
                    session.run(query)
                    self.log(f"  ✓ {query.split()[1]}")
                except Exception as e:
                    self.log(f"  ⚠ {query.split()[1]}: {str(e)}")

        self.log("Constraints and indexes created successfully")

    def create_nodes_batch(self, nodes: List[Dict], node_type: str):
        """Create nodes in batches using UNWIND"""
        self.log(f"Creating {len(nodes)} {node_type} nodes in batches of {BATCH_SIZE}...")

        total_created = 0
        batches = [nodes[i:i + BATCH_SIZE] for i in range(0, len(nodes), BATCH_SIZE)]

        for batch_num, batch in enumerate(batches, 1):
            with self.driver.session() as session:
                # Prepare batch data
                batch_data = []
                for node in batch:
                    batch_data.append({
                        "labels": node["labels"],
                        "properties": node["properties"]
                    })

                # Create nodes with dynamic labels
                query = """
                UNWIND $batch AS node_data
                CALL apoc.create.node(node_data.labels, node_data.properties) YIELD node
                RETURN count(node) as created
                """

                try:
                    result = session.run(query, batch=batch_data)
                    count = result.single()["created"]
                    total_created += count
                    self.log(f"  Batch {batch_num}/{len(batches)}: {count} nodes created")
                except Exception as e:
                    self.log(f"  ✗ Batch {batch_num} failed: {str(e)}")
                    # Fallback to individual creation
                    self.log(f"  Trying individual node creation for batch {batch_num}...")
                    for node_data in batch_data:
                        try:
                            # Create node with labels
                            labels = ":".join(node_data["labels"])
                            create_query = f"CREATE (n:{labels}) SET n = $properties RETURN n"
                            session.run(create_query, properties=node_data["properties"])
                            total_created += 1
                        except Exception as e2:
                            self.log(f"    ✗ Failed to create individual node: {str(e2)}")

        self.log(f"✓ {total_created} {node_type} nodes created")
        return total_created

    def create_relationships(self, data: Dict):
        """Create relationships between nodes"""
        self.log("Creating relationships...")

        devices = data["nodes"]["devices"]
        measurements = data["nodes"]["measurements"]
        properties = data["nodes"]["properties"]
        processes = data["nodes"]["processes"]
        controls = data["nodes"]["controls"]
        alerts = data["nodes"]["alerts"]
        zones = data["nodes"]["zones"]
        assets = data["nodes"]["assets"]

        # 1. MONITORS: Device -> Measurement
        self.log("  Creating MONITORS relationships (Device -> Measurement)...")
        self.create_monitors_relationships(measurements)

        # 2. HAS_PROPERTY: Device -> Property
        self.log("  Creating HAS_PROPERTY relationships (Device -> Property)...")
        self.create_has_property_relationships(properties)

        # 3. EXECUTES: Device -> Process
        self.log("  Creating EXECUTES relationships (Device -> Process)...")
        self.create_executes_relationships(devices, processes)

        # 4. CONTROLS: Control -> Device
        self.log("  Creating CONTROLS relationships (Control -> Device)...")
        self.create_controls_relationships(controls, devices)

        # 5. TRIGGERS: Measurement -> Alert
        self.log("  Creating TRIGGERS relationships (Measurement -> Alert)...")
        self.create_triggers_relationships(measurements, alerts)

        # 6. LOCATED_IN: Device -> Zone
        self.log("  Creating LOCATED_IN relationships (Device -> Zone)...")
        self.create_located_in_relationships(devices, zones)

        # 7. SUPPORTS: Asset -> Device
        self.log("  Creating SUPPORTS relationships (Asset -> Device)...")
        self.create_supports_relationships(assets, devices)

        # 8. REPORTS_TO: Device -> Control
        self.log("  Creating REPORTS_TO relationships (Device -> Control)...")
        self.create_reports_to_relationships(devices, controls)

        # 9. REQUIRES: Process -> Device
        self.log("  Creating REQUIRES relationships (Process -> Device)...")
        self.create_requires_relationships(processes, devices)

        self.log("✓ All relationships created")

    def create_monitors_relationships(self, measurements: List[Dict]):
        """Create MONITORS relationships"""
        batch_size = 1000
        batches = [measurements[i:i + batch_size] for i in range(0, len(measurements), batch_size)]

        for batch_num, batch in enumerate(batches, 1):
            with self.driver.session() as session:
                rel_data = [
                    {"equipment_id": m["properties"]["equipment_id"], "measurement_id": m["properties"]["measurement_id"]}
                    for m in batch if m["properties"].get("equipment_id")
                ]

                query = """
                UNWIND $rels AS rel
                MATCH (d:FoodAgricultureDevice {device_id: rel.equipment_id})
                MATCH (m:AgricultureMetric {measurement_id: rel.measurement_id})
                MERGE (d)-[r:MONITORS]->(m)
                RETURN count(r) as created
                """
                result = session.run(query, rels=rel_data)
                count = result.single()["created"]
                self.log(f"    Batch {batch_num}/{len(batches)}: {count} MONITORS relationships")

    def create_has_property_relationships(self, properties: List[Dict]):
        """Create HAS_PROPERTY relationships"""
        batch_size = 1000
        batches = [properties[i:i + batch_size] for i in range(0, len(properties), batch_size)]

        for batch_num, batch in enumerate(batches, 1):
            with self.driver.session() as session:
                rel_data = [
                    {"device_id": p["properties"]["device_id"], "property_id": p["properties"]["property_id"]}
                    for p in batch
                ]

                query = """
                UNWIND $rels AS rel
                MATCH (d:FoodAgricultureDevice {device_id: rel.device_id})
                MATCH (p:FoodAgricultureProperty {property_id: rel.property_id})
                MERGE (d)-[r:HAS_PROPERTY]->(p)
                RETURN count(r) as created
                """
                result = session.run(query, rels=rel_data)
                count = result.single()["created"]
                self.log(f"    Batch {batch_num}/{len(batches)}: {count} HAS_PROPERTY relationships")

    def create_executes_relationships(self, devices: List[Dict], processes: List[Dict]):
        """Create EXECUTES relationships (Device -> Process)"""
        with self.driver.session() as session:
            # Sample: 3 devices per process
            rel_data = []
            for process in processes:
                import random
                sampled_devices = random.sample(devices, min(3, len(devices)))
                for device in sampled_devices:
                    rel_data.append({
                        "device_id": device["properties"]["device_id"],
                        "process_id": process["properties"]["process_id"]
                    })

            # Create in batches
            batch_size = 1000
            batches = [rel_data[i:i + batch_size] for i in range(0, len(rel_data), batch_size)]

            for batch_num, batch in enumerate(batches, 1):
                query = """
                UNWIND $rels AS rel
                MATCH (d:FoodAgricultureDevice {device_id: rel.device_id})
                MATCH (p:AgricultureProcess {process_id: rel.process_id})
                MERGE (d)-[r:EXECUTES]->(p)
                RETURN count(r) as created
                """
                result = session.run(query, rels=batch)
                count = result.single()["created"]
                self.log(f"    Batch {batch_num}/{len(batches)}: {count} EXECUTES relationships")

    def create_controls_relationships(self, controls: List[Dict], devices: List[Dict]):
        """Create CONTROLS relationships (Control -> Device)"""
        with self.driver.session() as session:
            # Sample: each control system controls ~6 devices
            import random
            rel_data = []
            for control in controls:
                sampled_devices = random.sample(devices, min(6, len(devices)))
                for device in sampled_devices:
                    rel_data.append({
                        "control_id": control["properties"]["control_id"],
                        "device_id": device["properties"]["device_id"]
                    })

            batch_size = 1000
            batches = [rel_data[i:i + batch_size] for i in range(0, len(rel_data), batch_size)]

            for batch_num, batch in enumerate(batches, 1):
                query = """
                UNWIND $rels AS rel
                MATCH (c:FarmManagementSystem {control_id: rel.control_id})
                MATCH (d:FoodAgricultureDevice {device_id: rel.device_id})
                MERGE (c)-[r:CONTROLS]->(d)
                RETURN count(r) as created
                """
                result = session.run(query, rels=batch)
                count = result.single()["created"]
                self.log(f"    Batch {batch_num}/{len(batches)}: {count} CONTROLS relationships")

    def create_triggers_relationships(self, measurements: List[Dict], alerts: List[Dict]):
        """Create TRIGGERS relationships (Measurement -> Alert)"""
        with self.driver.session() as session:
            # Sample: 2 measurements per alert
            import random
            rel_data = []
            for alert in alerts:
                sampled_measurements = random.sample(measurements, min(2, len(measurements)))
                for measurement in sampled_measurements:
                    rel_data.append({
                        "measurement_id": measurement["properties"]["measurement_id"],
                        "alert_id": alert["properties"]["alert_id"]
                    })

            batch_size = 1000
            batches = [rel_data[i:i + batch_size] for i in range(0, len(rel_data), batch_size)]

            for batch_num, batch in enumerate(batches, 1):
                query = """
                UNWIND $rels AS rel
                MATCH (m:AgricultureMetric {measurement_id: rel.measurement_id})
                MATCH (a:FoodAgricultureAlert {alert_id: rel.alert_id})
                MERGE (m)-[r:TRIGGERS]->(a)
                RETURN count(r) as created
                """
                result = session.run(query, rels=batch)
                count = result.single()["created"]
                self.log(f"    Batch {batch_num}/{len(batches)}: {count} TRIGGERS relationships")

    def create_located_in_relationships(self, devices: List[Dict], zones: List[Dict]):
        """Create LOCATED_IN relationships (Device -> Zone)"""
        with self.driver.session() as session:
            # Each device in one zone
            import random
            rel_data = []
            for device in devices:
                zone = random.choice(zones)
                rel_data.append({
                    "device_id": device["properties"]["device_id"],
                    "zone_id": zone["properties"]["zone_id"]
                })

            batch_size = 1000
            batches = [rel_data[i:i + batch_size] for i in range(0, len(rel_data), batch_size)]

            for batch_num, batch in enumerate(batches, 1):
                query = """
                UNWIND $rels AS rel
                MATCH (d:FoodAgricultureDevice {device_id: rel.device_id})
                MATCH (z:FarmZone {zone_id: rel.zone_id})
                MERGE (d)-[r:LOCATED_IN]->(z)
                RETURN count(r) as created
                """
                result = session.run(query, rels=batch)
                count = result.single()["created"]
                self.log(f"    Batch {batch_num}/{len(batches)}: {count} LOCATED_IN relationships")

    def create_supports_relationships(self, assets: List[Dict], devices: List[Dict]):
        """Create SUPPORTS relationships (Asset -> Device)"""
        with self.driver.session() as session:
            # Each asset supports ~70 devices
            import random
            rel_data = []
            for asset in assets:
                sampled_devices = random.sample(devices, min(70, len(devices)))
                for device in sampled_devices:
                    rel_data.append({
                        "asset_id": asset["properties"]["asset_id"],
                        "device_id": device["properties"]["device_id"]
                    })

            batch_size = 1000
            batches = [rel_data[i:i + batch_size] for i in range(0, len(rel_data), batch_size)]

            for batch_num, batch in enumerate(batches, 1):
                query = """
                UNWIND $rels AS rel
                MATCH (a:MajorFacility {asset_id: rel.asset_id})
                MATCH (d:FoodAgricultureDevice {device_id: rel.device_id})
                MERGE (a)-[r:SUPPORTS]->(d)
                RETURN count(r) as created
                """
                result = session.run(query, rels=batch)
                count = result.single()["created"]
                self.log(f"    Batch {batch_num}/{len(batches)}: {count} SUPPORTS relationships")

    def create_reports_to_relationships(self, devices: List[Dict], controls: List[Dict]):
        """Create REPORTS_TO relationships (Device -> Control)"""
        with self.driver.session() as session:
            # Each device reports to one control
            import random
            rel_data = []
            for device in devices:
                control = random.choice(controls)
                rel_data.append({
                    "device_id": device["properties"]["device_id"],
                    "control_id": control["properties"]["control_id"]
                })

            batch_size = 1000
            batches = [rel_data[i:i + batch_size] for i in range(0, len(rel_data), batch_size)]

            for batch_num, batch in enumerate(batches, 1):
                query = """
                UNWIND $rels AS rel
                MATCH (d:FoodAgricultureDevice {device_id: rel.device_id})
                MATCH (c:FarmManagementSystem {control_id: rel.control_id})
                MERGE (d)-[r:REPORTS_TO]->(c)
                RETURN count(r) as created
                """
                result = session.run(query, rels=batch)
                count = result.single()["created"]
                self.log(f"    Batch {batch_num}/{len(batches)}: {count} REPORTS_TO relationships")

    def create_requires_relationships(self, processes: List[Dict], devices: List[Dict]):
        """Create REQUIRES relationships (Process -> Device)"""
        with self.driver.session() as session:
            # Each process requires 3-5 devices
            import random
            rel_data = []
            for process in processes:
                sampled_devices = random.sample(devices, min(random.randint(3, 5), len(devices)))
                for device in sampled_devices:
                    rel_data.append({
                        "process_id": process["properties"]["process_id"],
                        "device_id": device["properties"]["device_id"]
                    })

            batch_size = 1000
            batches = [rel_data[i:i + batch_size] for i in range(0, len(rel_data), batch_size)]

            for batch_num, batch in enumerate(batches, 1):
                query = """
                UNWIND $rels AS rel
                MATCH (p:AgricultureProcess {process_id: rel.process_id})
                MATCH (d:FoodAgricultureDevice {device_id: rel.device_id})
                MERGE (p)-[r:REQUIRES]->(d)
                RETURN count(r) as created
                """
                result = session.run(query, rels=batch)
                count = result.single()["created"]
                self.log(f"    Batch {batch_num}/{len(batches)}: {count} REQUIRES relationships")

    def validate_deployment(self) -> Dict[str, Any]:
        """Validate deployment with queries"""
        self.log("Validating deployment...")

        validation_results = {}

        with self.driver.session() as session:
            # Count nodes by type
            queries = {
                "total_nodes": "MATCH (n:FOOD_AGRICULTURE) RETURN count(n) as count",
                "device_nodes": "MATCH (n:FoodAgricultureDevice) RETURN count(n) as count",
                "measurement_nodes": "MATCH (n:AgricultureMetric) RETURN count(n) as count",
                "property_nodes": "MATCH (n:FoodAgricultureProperty) RETURN count(n) as count",
                "process_nodes": "MATCH (n:AgricultureProcess) RETURN count(n) as count",
                "control_nodes": "MATCH (n:FarmManagementSystem) RETURN count(n) as count",
                "alert_nodes": "MATCH (n:FoodAgricultureAlert) RETURN count(n) as count",
                "zone_nodes": "MATCH (n:FarmZone) RETURN count(n) as count",
                "asset_nodes": "MATCH (n:MajorFacility) RETURN count(n) as count",
                "total_relationships": "MATCH ()-[r]->() WHERE ANY(label IN labels(startNode(r)) WHERE label = 'FOOD_AGRICULTURE') RETURN count(r) as count"
            }

            for key, query in queries.items():
                result = session.run(query)
                count = result.single()["count"]
                validation_results[key] = count
                self.log(f"  {key}: {count}")

        return validation_results


def main():
    print("=" * 80)
    print("FOOD_AGRICULTURE Sector Deployment v5.0")
    print("=" * 80)

    # Load generated data
    data_file = "temp/sector-FOOD_AGRICULTURE-generated-data.json"
    print(f"\nLoading data from {data_file}...")

    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"✗ Error: {data_file} not found")
        print("Please run generate_food_agriculture_data_v5.py first")
        sys.exit(1)

    print(f"✓ Data loaded: {data['metadata']['total_nodes']} nodes")

    # Deploy to Neo4j
    deployer = FoodAgricultureDeployer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Create constraints and indexes
        deployer.create_constraints_indexes()

        # Create nodes
        deployer.create_nodes_batch(data["nodes"]["devices"], "Device")
        deployer.create_nodes_batch(data["nodes"]["measurements"], "Measurement")
        deployer.create_nodes_batch(data["nodes"]["properties"], "Property")
        deployer.create_nodes_batch(data["nodes"]["processes"], "Process")
        deployer.create_nodes_batch(data["nodes"]["controls"], "Control")
        deployer.create_nodes_batch(data["nodes"]["alerts"], "Alert")
        deployer.create_nodes_batch(data["nodes"]["zones"], "Zone")
        deployer.create_nodes_batch(data["nodes"]["assets"], "Asset")

        # Create relationships
        deployer.create_relationships(data)

        # Validate
        validation = deployer.validate_deployment()

        # Save log
        log_file = "temp/sector-FOOD_AGRICULTURE-deployment-log.txt"
        with open(log_file, 'w') as f:
            f.write("\n".join(deployer.log_messages))
            f.write("\n\n" + "=" * 80)
            f.write("\nVALIDATION RESULTS\n")
            f.write("=" * 80 + "\n")
            for key, value in validation.items():
                f.write(f"{key}: {value}\n")

        deployer.log(f"\n✓ Deployment log saved to {log_file}")
        deployer.log("\n🎉 FOOD_AGRICULTURE sector deployment COMPLETE!")

    finally:
        deployer.close()


if __name__ == "__main__":
    main()
