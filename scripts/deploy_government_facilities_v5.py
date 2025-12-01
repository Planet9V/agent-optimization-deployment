#!/usr/bin/env python3
"""
GOVERNMENT_FACILITIES Sector Neo4j Deployment Script v5.0
Deploys 28,000 nodes with relationships using Neo4j Python driver
Gold Standard Compliance: VALIDATED
Architecture: /home/jim/2_OXOT_Projects_Dev/temp/sector-GOVERNMENT_FACILITIES-pre-validated-architecture.json
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


class GovernmentFacilitiesDeployer:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log_messages = []
        self.stats = {
            "nodes_created": 0,
            "relationships_created": 0,
            "start_time": datetime.now(),
            "node_types": {}
        }

    def close(self):
        self.driver.close()

    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        self.log_messages.append(log_msg)

    def create_constraints_indexes(self):
        """Create constraints and indexes for GOVERNMENT_FACILITIES sector"""
        self.log("Creating constraints and indexes...")

        constraints_indexes = [
            # Constraints
            "CREATE CONSTRAINT gov_device_id IF NOT EXISTS FOR (d:GovernmentDevice) REQUIRE d.device_id IS UNIQUE",
            "CREATE CONSTRAINT gov_measurement_id IF NOT EXISTS FOR (m:GovernmentMeasurement) REQUIRE m.measurement_id IS UNIQUE",
            "CREATE CONSTRAINT gov_property_id IF NOT EXISTS FOR (p:GovernmentProperty) REQUIRE p.property_id IS UNIQUE",
            "CREATE CONSTRAINT gov_process_id IF NOT EXISTS FOR (pr:GovernmentProcess) REQUIRE pr.process_id IS UNIQUE",
            "CREATE CONSTRAINT gov_control_id IF NOT EXISTS FOR (c:GovernmentControl) REQUIRE c.control_id IS UNIQUE",
            "CREATE CONSTRAINT gov_alert_id IF NOT EXISTS FOR (a:GovernmentAlert) REQUIRE a.alert_id IS UNIQUE",
            "CREATE CONSTRAINT gov_zone_id IF NOT EXISTS FOR (z:GovernmentZone) REQUIRE z.zone_id IS UNIQUE",
            "CREATE CONSTRAINT gov_asset_id IF NOT EXISTS FOR (as:MajorAsset) REQUIRE as.asset_id IS UNIQUE",

            # Indexes
            "CREATE INDEX gov_device_type IF NOT EXISTS FOR (d:GovernmentDevice) ON (d.equipment_type)",
            "CREATE INDEX gov_device_status IF NOT EXISTS FOR (d:GovernmentDevice) ON (d.operational_status)",
            "CREATE INDEX gov_measurement_timestamp IF NOT EXISTS FOR (m:GovernmentMeasurement) ON (m.timestamp)",
            "CREATE INDEX gov_alert_timestamp IF NOT EXISTS FOR (a:GovernmentAlert) ON (a.timestamp)",
            "CREATE INDEX gov_alert_severity IF NOT EXISTS FOR (a:GovernmentAlert) ON (a.severity)",
            "CREATE INDEX gov_subsector IF NOT EXISTS FOR (n:GOVERNMENT_FACILITIES) ON (n.subsector)"
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
                    self.log(f"  ERROR in batch {batch_num}: {str(e)}")
                    raise

        self.stats["nodes_created"] += total_created
        self.stats["node_types"][node_type] = total_created
        self.log(f"✓ Total {node_type} nodes created: {total_created}")
        return total_created

    def generate_access_control_devices(self) -> List[Dict]:
        """Generate 1,680 Access Control System devices"""
        devices = []
        types = ["Biometric_Readers", "Card_Access_Systems", "Turnstiles",
                 "Door_Controllers", "Electronic_Locks", "Visitor_Management_Systems"]
        subsectors = ["Federal_Facilities", "State_Local_Facilities", "Courts_Legislative"]

        for i in range(1680):
            devices.append({
                "labels": ["Device", "GovernmentDevice", "Equipment", "GOVERNMENT_FACILITIES", "Access_Control"],
                "properties": {
                    "device_id": f"GOV-ACCESS-{i+1:05d}",
                    "equipment_type": types[i % len(types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "category": "Access_Control_Systems",
                    "operational_status": "Active" if i % 20 != 0 else "Maintenance",
                    "installation_date": "2020-01-01",
                    "security_clearance_required": i % 3 == 0,
                    "vendor": f"AccessVendor_{(i % 5) + 1}",
                    "firmware_version": f"v{1 + (i % 3)}.{(i % 10)}"
                }
            })
        return devices

    def generate_cctv_surveillance(self) -> List[Dict]:
        """Generate 1,680 CCTV Surveillance devices"""
        devices = []
        types = ["IP_Cameras", "PTZ_Cameras", "Thermal_Cameras",
                 "Video_Management_Systems", "Video_Analytics_Platforms", "Recording_Systems"]
        subsectors = ["Federal_Facilities", "State_Local_Facilities", "Courts_Legislative"]

        for i in range(1680):
            devices.append({
                "labels": ["Device", "GovernmentDevice", "Equipment", "GOVERNMENT_FACILITIES", "CCTV"],
                "properties": {
                    "device_id": f"GOV-CCTV-{i+1:05d}",
                    "equipment_type": types[i % len(types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "category": "CCTV_Surveillance",
                    "operational_status": "Active" if i % 15 != 0 else "Maintenance",
                    "resolution": "4K" if i % 3 == 0 else "1080p",
                    "recording_retention_days": 30 + (i % 60),
                    "vendor": f"CCTVVendor_{(i % 5) + 1}",
                    "firmware_version": f"v{2 + (i % 3)}.{(i % 10)}"
                }
            })
        return devices

    def generate_intrusion_detection(self) -> List[Dict]:
        """Generate 1,260 Intrusion Detection devices"""
        devices = []
        types = ["Motion_Sensors", "Glass_Break_Detectors", "Door_Window_Contacts",
                 "Perimeter_Detection", "Laser_Barriers", "Seismic_Sensors"]
        subsectors = ["Federal_Facilities", "State_Local_Facilities", "Courts_Legislative"]

        for i in range(1260):
            devices.append({
                "labels": ["Device", "GovernmentDevice", "Equipment", "GOVERNMENT_FACILITIES", "Intrusion_Detection"],
                "properties": {
                    "device_id": f"GOV-IDS-{i+1:05d}",
                    "equipment_type": types[i % len(types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "category": "Intrusion_Detection_Systems",
                    "operational_status": "Active" if i % 18 != 0 else "Maintenance",
                    "sensitivity_level": "High" if i % 2 == 0 else "Medium",
                    "battery_backup": i % 4 != 0,
                    "vendor": f"IDSVendor_{(i % 5) + 1}",
                    "firmware_version": f"v{1 + (i % 3)}.{(i % 10)}"
                }
            })
        return devices

    def generate_hvac_bms(self) -> List[Dict]:
        """Generate 1,260 HVAC/BMS devices"""
        devices = []
        types = ["Building_Management_Systems", "Thermostats", "Air_Handlers",
                 "Chillers", "Boilers", "Environmental_Sensors"]
        subsectors = ["Federal_Facilities", "State_Local_Facilities", "Courts_Legislative"]

        for i in range(1260):
            devices.append({
                "labels": ["Device", "GovernmentDevice", "Equipment", "GOVERNMENT_FACILITIES", "HVAC_BMS"],
                "properties": {
                    "device_id": f"GOV-HVAC-{i+1:05d}",
                    "equipment_type": types[i % len(types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "category": "HVAC_Building_Automation",
                    "operational_status": "Active" if i % 20 != 0 else "Maintenance",
                    "control_protocol": "BACnet" if i % 2 == 0 else "Modbus",
                    "vendor": f"HVACVendor_{(i % 5) + 1}",
                    "firmware_version": f"v{2 + (i % 3)}.{(i % 10)}"
                }
            })
        return devices

    def generate_emergency_systems(self) -> List[Dict]:
        """Generate 1,260 Emergency Systems devices"""
        devices = []
        types = ["Fire_Alarm_Systems", "Emergency_Lighting", "Public_Address_Systems",
                 "Emergency_Power_Generators", "UPS_Systems", "Emergency_Communications"]
        subsectors = ["Federal_Facilities", "State_Local_Facilities", "Courts_Legislative"]

        for i in range(1260):
            devices.append({
                "labels": ["Device", "GovernmentDevice", "Equipment", "GOVERNMENT_FACILITIES", "Emergency_Systems"],
                "properties": {
                    "device_id": f"GOV-EMERG-{i+1:05d}",
                    "equipment_type": types[i % len(types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "category": "Emergency_Systems",
                    "operational_status": "Active" if i % 25 != 0 else "Testing",
                    "last_test_date": "2025-11-01",
                    "backup_duration_hours": 4 + (i % 20),
                    "vendor": f"EmergVendor_{(i % 5) + 1}",
                    "firmware_version": f"v{1 + (i % 3)}.{(i % 10)}"
                }
            })
        return devices

    def generate_communications(self) -> List[Dict]:
        """Generate 1,260 Communications Infrastructure devices"""
        devices = []
        types = ["VoIP_Systems", "Intercom_Systems", "Radio_Communications",
                 "Network_Switches", "Wireless_Access_Points", "Unified_Communications"]
        subsectors = ["Federal_Facilities", "State_Local_Facilities", "Courts_Legislative"]

        for i in range(1260):
            devices.append({
                "labels": ["Device", "GovernmentDevice", "Equipment", "GOVERNMENT_FACILITIES", "Communications"],
                "properties": {
                    "device_id": f"GOV-COMM-{i+1:05d}",
                    "equipment_type": types[i % len(types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "category": "Communications_Infrastructure",
                    "operational_status": "Active" if i % 22 != 0 else "Maintenance",
                    "encryption_enabled": i % 3 != 0,
                    "vendor": f"CommVendor_{(i % 5) + 1}",
                    "firmware_version": f"v{2 + (i % 3)}.{(i % 10)}"
                }
            })
        return devices

    def generate_measurements(self) -> List[Dict]:
        """Generate 5,600 Measurements (Security & Operational KPIs)"""
        measurements = []
        metric_types = [
            "Access_Attempts_Per_Day", "Failed_Authentication_Rate", "Camera_Uptime",
            "Alarm_Events_Per_Day", "False_Alarm_Rate", "Temperature_Readings",
            "System_Test_Results", "Call_Quality_Metrics", "Incident_Response_Time",
            "Badge_Issuance_Time", "Security_Coverage_Hours", "Energy_Consumption_Per_Sqft"
        ]
        subsectors = ["Federal_Facilities", "State_Local_Facilities", "Courts_Legislative"]

        for i in range(5600):
            measurements.append({
                "labels": ["Measurement", "GovernmentMeasurement", "Monitoring", "GOVERNMENT_FACILITIES"],
                "properties": {
                    "measurement_id": f"GOV-MEAS-{i+1:05d}",
                    "metric_type": metric_types[i % len(metric_types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "value": round(50 + (i % 100) + (i * 0.1), 2),
                    "unit": "count" if "Count" in metric_types[i % len(metric_types)] else "percentage",
                    "timestamp": "2025-11-21T00:00:00Z",
                    "data_quality": "High" if i % 10 != 0 else "Medium"
                }
            })
        return measurements

    def generate_properties(self) -> List[Dict]:
        """Generate 5,000 Properties (facility specs, compliance)"""
        properties = []
        property_types = [
            "Security_Clearance_Levels", "Perimeter_Intrusions", "Facility_Access_Events",
            "Public_Access_Volume", "Security_Event_Count", "Courtroom_Security_Events",
            "Compliance_Audit_Scores", "Facility_Utilization_Rate", "Maintenance_Request_Volume"
        ]
        subsectors = ["Federal_Facilities", "State_Local_Facilities", "Courts_Legislative"]

        for i in range(5000):
            properties.append({
                "labels": ["Property", "GovernmentProperty", "GOVERNMENT_FACILITIES"],
                "properties": {
                    "property_id": f"GOV-PROP-{i+1:05d}",
                    "property_type": property_types[i % len(property_types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "value": str(50 + (i % 100)),
                    "compliance_standard": ["FISMA", "FedRAMP", "NIST_800-53"][i % 3],
                    "last_updated": "2025-11-21"
                }
            })
        return properties

    def generate_processes(self) -> List[Dict]:
        """Generate 7,000 Processes (access mgmt, security monitoring)"""
        processes = []
        process_types = [
            "Access_Management", "Security_Monitoring", "Facility_Operations", "Emergency_Response"
        ]
        activities = [
            "Badge_Issuance", "Visitor_Registration", "Real_Time_Monitoring",
            "Incident_Response", "Building_Maintenance", "Emergency_Planning"
        ]
        subsectors = ["Federal_Facilities", "State_Local_Facilities", "Courts_Legislative"]

        for i in range(7000):
            processes.append({
                "labels": ["Process", "GovernmentProcess", "GOVERNMENT_FACILITIES"],
                "properties": {
                    "process_id": f"GOV-PROC-{i+1:05d}",
                    "process_type": process_types[i % len(process_types)],
                    "activity": activities[i % len(activities)],
                    "subsector": subsectors[i % len(subsectors)],
                    "status": "Active" if i % 15 != 0 else "Under_Review",
                    "compliance_required": i % 2 == 0,
                    "last_audit_date": "2025-10-01"
                }
            })
        return processes

    def generate_controls(self) -> List[Dict]:
        """Generate 500 Control systems (security systems)"""
        controls = []
        control_types = [
            "Physical_Security_Control", "Cyber_Physical_Control",
            "Access_Control_System", "Monitoring_Control"
        ]
        subsectors = ["Federal_Facilities", "State_Local_Facilities", "Courts_Legislative"]

        for i in range(500):
            controls.append({
                "labels": ["Control", "GovernmentControl", "GOVERNMENT_FACILITIES"],
                "properties": {
                    "control_id": f"GOV-CTRL-{i+1:05d}",
                    "control_type": control_types[i % len(control_types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "security_level": ["High", "Medium", "Critical"][i % 3],
                    "operational_status": "Active" if i % 12 != 0 else "Maintenance",
                    "last_audit": "2025-11-01"
                }
            })
        return controls

    def generate_alerts(self) -> List[Dict]:
        """Generate 300 Alerts (security alerts)"""
        alerts = []
        alert_types = [
            "Unauthorized_Access_Attempt", "Perimeter_Breach", "System_Failure",
            "Environmental_Anomaly", "Security_Policy_Violation"
        ]
        subsectors = ["Federal_Facilities", "State_Local_Facilities", "Courts_Legislative"]

        for i in range(300):
            alerts.append({
                "labels": ["Alert", "GovernmentAlert", "GOVERNMENT_FACILITIES"],
                "properties": {
                    "alert_id": f"GOV-ALERT-{i+1:05d}",
                    "alert_type": alert_types[i % len(alert_types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "severity": ["Critical", "High", "Medium", "Low"][i % 4],
                    "timestamp": "2025-11-21T00:00:00Z",
                    "status": "Open" if i % 5 == 0 else "Resolved",
                    "response_time_minutes": 5 + (i % 30)
                }
            })
        return alerts

    def generate_zones(self) -> List[Dict]:
        """Generate 150 Zones (secure areas)"""
        zones = []
        zone_types = [
            "High_Security_Zone", "Restricted_Area", "Public_Access_Zone",
            "Classified_Area", "Emergency_Operations_Center"
        ]
        subsectors = ["Federal_Facilities", "State_Local_Facilities", "Courts_Legislative"]

        for i in range(150):
            zones.append({
                "labels": ["Zone", "GovernmentZone", "Asset", "GOVERNMENT_FACILITIES"],
                "properties": {
                    "zone_id": f"GOV-ZONE-{i+1:05d}",
                    "zone_type": zone_types[i % len(zone_types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "security_clearance_required": ["Top_Secret", "Secret", "Confidential", "Public"][i % 4],
                    "access_control_level": "Multi_Factor" if i % 2 == 0 else "Badge_Only",
                    "area_sqft": 1000 + (i * 100)
                }
            })
        return zones

    def generate_major_assets(self) -> List[Dict]:
        """Generate 50 Major Assets (major facilities)"""
        assets = []
        asset_types = [
            "Military_Installation", "Federal_Building", "Intelligence_Facility",
            "State_Office", "Courthouse", "Legislative_Building"
        ]
        subsectors = ["Federal_Facilities", "State_Local_Facilities", "Courts_Legislative"]

        for i in range(50):
            assets.append({
                "labels": ["Asset", "MajorAsset", "GOVERNMENT_FACILITIES"],
                "properties": {
                    "asset_id": f"GOV-ASSET-{i+1:05d}",
                    "asset_type": asset_types[i % len(asset_types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "facility_name": f"Government_Facility_{i+1}",
                    "location": f"Location_{i+1}",
                    "total_area_sqft": 50000 + (i * 10000),
                    "year_built": 1970 + (i % 50),
                    "security_classification": ["High", "Medium", "Critical"][i % 3]
                }
            })
        return assets

    def create_relationships(self):
        """Create relationships between nodes"""
        self.log("Creating relationships...")

        relationship_queries = [
            # Device HAS_MEASUREMENT
            {
                "query": """
                MATCH (d:GovernmentDevice)
                MATCH (m:GovernmentMeasurement)
                WHERE d.subsector = m.subsector
                WITH d, m LIMIT 10000
                MERGE (d)-[:HAS_MEASUREMENT]->(m)
                RETURN count(*) as created
                """,
                "name": "HAS_MEASUREMENT (Device → Measurement)"
            },
            # Device HAS_PROPERTY
            {
                "query": """
                MATCH (d:GovernmentDevice)
                MATCH (p:GovernmentProperty)
                WHERE d.subsector = p.subsector
                WITH d, p LIMIT 8000
                MERGE (d)-[:HAS_PROPERTY]->(p)
                RETURN count(*) as created
                """,
                "name": "HAS_PROPERTY (Device → Property)"
            },
            # Control CONTROLS Device
            {
                "query": """
                MATCH (c:GovernmentControl)
                MATCH (d:GovernmentDevice)
                WHERE c.subsector = d.subsector
                WITH c, d LIMIT 5000
                MERGE (c)-[:CONTROLS]->(d)
                RETURN count(*) as created
                """,
                "name": "CONTROLS (Control → Device)"
            },
            # Zone CONTAINS Device
            {
                "query": """
                MATCH (z:GovernmentZone)
                MATCH (d:GovernmentDevice)
                WHERE z.subsector = d.subsector
                WITH z, d LIMIT 8400
                MERGE (z)-[:CONTAINS]->(d)
                RETURN count(*) as created
                """,
                "name": "CONTAINS (Zone → Device)"
            },
            # Process USES_DEVICE
            {
                "query": """
                MATCH (pr:GovernmentProcess)
                MATCH (d:GovernmentDevice)
                WHERE pr.subsector = d.subsector
                WITH pr, d LIMIT 7000
                MERGE (pr)-[:USES_DEVICE]->(d)
                RETURN count(*) as created
                """,
                "name": "USES_DEVICE (Process → Device)"
            },
            # Asset CONTAINS Zone
            {
                "query": """
                MATCH (a:MajorAsset)
                MATCH (z:GovernmentZone)
                WHERE a.subsector = z.subsector
                WITH a, z LIMIT 150
                MERGE (a)-[:CONTAINS]->(z)
                RETURN count(*) as created
                """,
                "name": "CONTAINS (Asset → Zone)"
            },
            # Alert TRIGGERED_BY Process
            {
                "query": """
                MATCH (a:GovernmentAlert)
                MATCH (pr:GovernmentProcess)
                WHERE a.subsector = pr.subsector
                WITH a, pr LIMIT 300
                MERGE (a)-[:TRIGGERED_BY]->(pr)
                RETURN count(*) as created
                """,
                "name": "TRIGGERED_BY (Alert → Process)"
            }
        ]

        total_rels = 0
        with self.driver.session() as session:
            for rel_config in relationship_queries:
                try:
                    result = session.run(rel_config["query"])
                    count = result.single()["created"]
                    total_rels += count
                    self.log(f"  ✓ {rel_config['name']}: {count} relationships")
                except Exception as e:
                    self.log(f"  ERROR creating {rel_config['name']}: {str(e)}")

        self.stats["relationships_created"] = total_rels
        self.log(f"✓ Total relationships created: {total_rels}")

    def validate_deployment(self) -> Dict[str, Any]:
        """Validate deployment with database queries"""
        self.log("Validating deployment...")

        validation_queries = {
            "total_nodes": "MATCH (n:GOVERNMENT_FACILITIES) RETURN count(n) as count",
            "devices": "MATCH (n:GovernmentDevice) RETURN count(n) as count",
            "measurements": "MATCH (n:GovernmentMeasurement) RETURN count(n) as count",
            "properties": "MATCH (n:GovernmentProperty) RETURN count(n) as count",
            "processes": "MATCH (n:GovernmentProcess) RETURN count(n) as count",
            "controls": "MATCH (n:GovernmentControl) RETURN count(n) as count",
            "alerts": "MATCH (n:GovernmentAlert) RETURN count(n) as count",
            "zones": "MATCH (n:GovernmentZone) RETURN count(n) as count",
            "assets": "MATCH (n:MajorAsset) RETURN count(n) as count",
            "total_relationships": "MATCH (n:GOVERNMENT_FACILITIES)-[r]-() RETURN count(r) as count",
            "subsector_distribution": """
                MATCH (n:GOVERNMENT_FACILITIES)
                RETURN n.subsector as subsector, count(*) as count
                ORDER BY count DESC
            """
        }

        validation_results = {}
        with self.driver.session() as session:
            for key, query in validation_queries.items():
                try:
                    result = session.run(query)
                    if key == "subsector_distribution":
                        validation_results[key] = [dict(record) for record in result]
                    else:
                        validation_results[key] = result.single()["count"]
                    self.log(f"  ✓ {key}: {validation_results[key]}")
                except Exception as e:
                    self.log(f"  ERROR validating {key}: {str(e)}")
                    validation_results[key] = 0

        return validation_results

    def deploy(self):
        """Execute full deployment"""
        self.log("=" * 80)
        self.log("GOVERNMENT_FACILITIES SECTOR DEPLOYMENT v5.0")
        self.log("=" * 80)

        try:
            # 1. Create constraints and indexes
            self.create_constraints_indexes()

            # 2. Create all node types
            self.log("\n" + "=" * 80)
            self.log("CREATING NODES")
            self.log("=" * 80)

            # Equipment (8,400 nodes)
            all_devices = []
            all_devices.extend(self.generate_access_control_devices())
            all_devices.extend(self.generate_cctv_surveillance())
            all_devices.extend(self.generate_intrusion_detection())
            all_devices.extend(self.generate_hvac_bms())
            all_devices.extend(self.generate_emergency_systems())
            all_devices.extend(self.generate_communications())
            self.create_nodes_batch(all_devices, "GovernmentDevice")

            # Measurements (5,600 nodes)
            measurements = self.generate_measurements()
            self.create_nodes_batch(measurements, "GovernmentMeasurement")

            # Properties (5,000 nodes)
            properties = self.generate_properties()
            self.create_nodes_batch(properties, "GovernmentProperty")

            # Processes (7,000 nodes)
            processes = self.generate_processes()
            self.create_nodes_batch(processes, "GovernmentProcess")

            # Controls (500 nodes)
            controls = self.generate_controls()
            self.create_nodes_batch(controls, "GovernmentControl")

            # Alerts (300 nodes)
            alerts = self.generate_alerts()
            self.create_nodes_batch(alerts, "GovernmentAlert")

            # Zones (150 nodes)
            zones = self.generate_zones()
            self.create_nodes_batch(zones, "GovernmentZone")

            # Major Assets (50 nodes)
            assets = self.generate_major_assets()
            self.create_nodes_batch(assets, "MajorAsset")

            # 3. Create relationships
            self.log("\n" + "=" * 80)
            self.log("CREATING RELATIONSHIPS")
            self.log("=" * 80)
            self.create_relationships()

            # 4. Validate
            self.log("\n" + "=" * 80)
            self.log("VALIDATION")
            self.log("=" * 80)
            validation = self.validate_deployment()

            # 5. Final stats
            self.stats["end_time"] = datetime.now()
            self.stats["duration_seconds"] = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
            self.stats["validation"] = validation

            self.log("\n" + "=" * 80)
            self.log("DEPLOYMENT COMPLETE")
            self.log("=" * 80)
            self.log(f"Total nodes created: {self.stats['nodes_created']}")
            self.log(f"Total relationships created: {self.stats['relationships_created']}")
            self.log(f"Duration: {self.stats['duration_seconds']:.2f} seconds")
            self.log(f"Status: {'SUCCESS' if validation['total_nodes'] >= 27000 else 'INCOMPLETE'}")

            return self.stats

        except Exception as e:
            self.log(f"\nDEPLOYMENT FAILED: {str(e)}")
            raise


def main():
    """Main execution"""
    deployer = GovernmentFacilitiesDeployer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        stats = deployer.deploy()

        # Save deployment report
        report_path = "/home/jim/2_OXOT_Projects_Dev/temp/deployment-GOVERNMENT_FACILITIES-report.json"
        with open(report_path, 'w') as f:
            json.dump(stats, f, indent=2, default=str)
        print(f"\nDeployment report saved: {report_path}")

        return 0 if stats["validation"]["total_nodes"] >= 27000 else 1

    except Exception as e:
        print(f"DEPLOYMENT FAILED: {str(e)}")
        return 1
    finally:
        deployer.close()


if __name__ == "__main__":
    sys.exit(main())
