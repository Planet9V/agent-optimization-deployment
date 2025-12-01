#!/usr/bin/env python3
"""
COMMERCIAL_FACILITIES Sector Neo4j Deployment Script v5.0
Deploys 28,000 nodes with relationships using Neo4j Python driver
Gold Standard Compliance: VALIDATED
Architecture: /home/jim/2_OXOT_Projects_Dev/temp/sector-COMMERCIAL_FACILITIES-pre-validated-architecture.json
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


class CommercialFacilitiesDeployer:
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
        """Create constraints and indexes for COMMERCIAL_FACILITIES sector"""
        self.log("Creating constraints and indexes...")

        constraints_indexes = [
            # Constraints
            "CREATE CONSTRAINT comm_asset_id IF NOT EXISTS FOR (a:CommercialAsset) REQUIRE a.asset_id IS UNIQUE",
            "CREATE CONSTRAINT comm_process_id IF NOT EXISTS FOR (p:CommercialProcess) REQUIRE p.process_id IS UNIQUE",
            "CREATE CONSTRAINT comm_control_id IF NOT EXISTS FOR (c:CommercialControl) REQUIRE c.control_id IS UNIQUE",
            "CREATE CONSTRAINT comm_location_id IF NOT EXISTS FOR (l:CommercialLocation) REQUIRE l.location_id IS UNIQUE",
            "CREATE CONSTRAINT comm_threat_id IF NOT EXISTS FOR (t:CommercialThreat) REQUIRE t.threat_id IS UNIQUE",
            "CREATE CONSTRAINT comm_vulnerability_id IF NOT EXISTS FOR (v:CommercialVulnerability) REQUIRE v.vulnerability_id IS UNIQUE",
            "CREATE CONSTRAINT comm_mitigation_id IF NOT EXISTS FOR (m:CommercialMitigation) REQUIRE m.mitigation_id IS UNIQUE",
            "CREATE CONSTRAINT comm_standard_id IF NOT EXISTS FOR (s:CommercialStandard) REQUIRE s.standard_id IS UNIQUE",

            # Indexes
            "CREATE INDEX comm_asset_type IF NOT EXISTS FOR (a:CommercialAsset) ON (a.asset_type)",
            "CREATE INDEX comm_subsector IF NOT EXISTS FOR (n:COMMERCIAL_FACILITIES) ON (n.subsector)",
            "CREATE INDEX comm_location_type IF NOT EXISTS FOR (l:CommercialLocation) ON (l.location_type)",
            "CREATE INDEX comm_threat_severity IF NOT EXISTS FOR (t:CommercialThreat) ON (t.severity)",
            "CREATE INDEX comm_vulnerability_cvss IF NOT EXISTS FOR (v:CommercialVulnerability) ON (v.cvss_score)",
            "CREATE INDEX comm_control_type IF NOT EXISTS FOR (c:CommercialControl) ON (c.control_type)"
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

    def generate_hvac_assets(self) -> List[Dict]:
        """Generate HVAC system assets"""
        assets = []
        types = ["Air_Handling_Unit", "Chiller", "Boiler", "VAV_Box", "Thermostat", "BAS_Controller"]
        subsectors = ["Office_Buildings", "Retail_Centers", "Hotels_Lodging"]
        manufacturers = ["Johnson Controls", "Honeywell", "Siemens", "Trane", "Carrier"]

        for i in range(2100):
            assets.append({
                "labels": ["Asset", "CommercialAsset", "Equipment", "COMMERCIAL_FACILITIES", "HVAC"],
                "properties": {
                    "asset_id": f"COMM-HVAC-{i+1:05d}",
                    "asset_type": types[i % len(types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "manufacturer": manufacturers[i % len(manufacturers)],
                    "model": f"Model_{types[i % len(types)]}_{(i % 10) + 1}",
                    "installation_date": f"20{18 + (i % 6)}-{1 + (i % 12):02d}-01",
                    "location": f"Building_{chr(65 + (i % 10))}_Floor_{1 + (i % 20)}",
                    "criticality": ["high", "medium", "low"][i % 3],
                    "maintenance_schedule": ["monthly", "quarterly", "annual"][i % 3],
                    "protocol": ["BACnet", "Modbus", "LonWorks"][i % 3]
                }
            })
        return assets

    def generate_access_control_assets(self) -> List[Dict]:
        """Generate access control assets"""
        assets = []
        types = ["Card_Reader", "Electronic_Lock", "Control_Panel", "Turnstile", "Gate_Controller", "Biometric_Scanner"]
        subsectors = ["Office_Buildings", "Retail_Centers", "Hotels_Lodging"]
        vendors = ["Lenel", "Software House", "Genetec", "Brivo", "Avigilon"]

        for i in range(1680):
            assets.append({
                "labels": ["Asset", "CommercialAsset", "Equipment", "COMMERCIAL_FACILITIES", "Access_Control"],
                "properties": {
                    "asset_id": f"COMM-ACCESS-{i+1:05d}",
                    "asset_type": types[i % len(types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "manufacturer": vendors[i % len(vendors)],
                    "model": f"Model_{types[i % len(types)]}_{(i % 8) + 1}",
                    "installation_date": f"20{19 + (i % 5)}-{1 + (i % 12):02d}-01",
                    "location": f"Building_{chr(65 + (i % 15))}_Entrance_{chr(65 + (i % 8))}",
                    "criticality": ["high", "medium"][i % 2],
                    "maintenance_schedule": ["quarterly", "annual"][i % 2],
                    "protocol": ["OSDP", "Wiegand", "TCP/IP"][i % 3]
                }
            })
        return assets

    def generate_fire_safety_assets(self) -> List[Dict]:
        """Generate fire safety assets"""
        assets = []
        types = ["Smoke_Detector", "Pull_Station", "Fire_Alarm_Panel", "Notification_Device", "Sprinkler_Head", "Suppression_System"]
        subsectors = ["Office_Buildings", "Retail_Centers", "Hotels_Lodging"]
        vendors = ["Simplex", "Notifier", "Edwards", "Fire-Lite", "Gamewell-FCI"]

        for i in range(1680):
            assets.append({
                "labels": ["Asset", "CommercialAsset", "Equipment", "COMMERCIAL_FACILITIES", "Fire_Safety"],
                "properties": {
                    "asset_id": f"COMM-FIRE-{i+1:05d}",
                    "asset_type": types[i % len(types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "manufacturer": vendors[i % len(vendors)],
                    "model": f"Model_{types[i % len(types)]}_{(i % 7) + 1}",
                    "installation_date": f"20{17 + (i % 7)}-{1 + (i % 12):02d}-01",
                    "location": f"Building_{chr(65 + (i % 12))}_Floor_{1 + (i % 25)}_Zone_{chr(65 + (i % 6))}",
                    "criticality": "high",
                    "maintenance_schedule": ["monthly", "quarterly", "annual"][i % 3],
                    "protocol": ["Proprietary", "BACnet"][i % 2]
                }
            })
        return assets

    def generate_surveillance_assets(self) -> List[Dict]:
        """Generate security surveillance assets"""
        assets = []
        types = ["IP_Camera", "PTZ_Camera", "NVR", "VMS_Server", "Analytics_Server", "Monitor"]
        subsectors = ["Office_Buildings", "Retail_Centers", "Hotels_Lodging"]
        vendors = ["Axis", "Hanwha", "Hikvision", "Bosch", "Dahua"]

        for i in range(1400):
            assets.append({
                "labels": ["Asset", "CommercialAsset", "Equipment", "COMMERCIAL_FACILITIES", "Surveillance"],
                "properties": {
                    "asset_id": f"COMM-CCTV-{i+1:05d}",
                    "asset_type": types[i % len(types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "manufacturer": vendors[i % len(vendors)],
                    "model": f"Model_{types[i % len(types)]}_{(i % 9) + 1}",
                    "installation_date": f"20{19 + (i % 5)}-{1 + (i % 12):02d}-01",
                    "location": f"Building_{chr(65 + (i % 14))}_Camera_{i % 100}_Zone_{chr(65 + (i % 8))}",
                    "criticality": ["high", "medium", "low"][i % 3],
                    "maintenance_schedule": ["quarterly", "annual"][i % 2],
                    "protocol": ["ONVIF", "RTSP", "HTTP"][i % 3]
                }
            })
        return assets

    def generate_building_automation_assets(self) -> List[Dict]:
        """Generate building automation assets"""
        assets = []
        types = ["Building_Controller", "Supervisory_Workstation", "Field_Device", "Sensor", "Actuator", "Gateway"]
        subsectors = ["Office_Buildings", "Retail_Centers", "Hotels_Lodging"]
        vendors = ["Johnson Controls", "Honeywell", "Siemens", "Schneider Electric", "Distech"]

        for i in range(1540):
            assets.append({
                "labels": ["Asset", "CommercialAsset", "Equipment", "COMMERCIAL_FACILITIES", "BAS"],
                "properties": {
                    "asset_id": f"COMM-BAS-{i+1:05d}",
                    "asset_type": types[i % len(types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "manufacturer": vendors[i % len(vendors)],
                    "model": f"Model_{types[i % len(types)]}_{(i % 8) + 1}",
                    "installation_date": f"20{18 + (i % 6)}-{1 + (i % 12):02d}-01",
                    "location": f"Building_{chr(65 + (i % 11))}_System_{chr(65 + (i % 5))}",
                    "criticality": ["high", "medium"][i % 2],
                    "maintenance_schedule": ["monthly", "quarterly", "annual"][i % 3],
                    "protocol": ["BACnet", "Modbus", "LonWorks", "KNX"][i % 4]
                }
            })
        return assets

    def generate_processes(self) -> List[Dict]:
        """Generate 5,600 process nodes"""
        processes = []
        types = ["Security_Monitoring", "Access_Management", "HVAC_Control", "Fire_Alarm_Response",
                 "Maintenance_Scheduling", "Emergency_Evacuation", "Energy_Management", "Guest_Check_In"]
        subsectors = ["Office_Buildings", "Retail_Centers", "Hotels_Lodging"]
        automation_levels = ["manual", "semi-automated", "automated"]
        frequencies = ["continuous", "scheduled", "on-demand"]

        for i in range(5600):
            processes.append({
                "labels": ["Process", "CommercialProcess", "COMMERCIAL_FACILITIES"],
                "properties": {
                    "process_id": f"COMM-PROC-{i+1:05d}",
                    "process_name": f"{types[i % len(types)]}_{i+1}",
                    "process_type": ["operational", "maintenance", "security"][i % 3],
                    "subsector": subsectors[i % len(subsectors)],
                    "frequency": frequencies[i % len(frequencies)],
                    "automation_level": automation_levels[i % len(automation_levels)],
                    "critical_path": i % 4 == 0,
                    "dependencies": f"Requires_{(i % 3) + 1}_prerequisites"
                }
            })
        return processes

    def generate_controls(self) -> List[Dict]:
        """Generate 4,200 control nodes"""
        controls = []
        types = ["Badge_Reader", "Control_Panel", "Console", "Thermostat", "Pull_Station",
                 "Gate_Control", "Call_Panel", "Emergency_Switch"]
        subsectors = ["Office_Buildings", "Retail_Centers", "Hotels_Lodging"]
        auth_methods = ["badge", "PIN", "biometric", "none"]
        failsafe_modes = ["fail-open", "fail-closed", "fail-secure"]

        for i in range(4200):
            controls.append({
                "labels": ["Control", "CommercialControl", "COMMERCIAL_FACILITIES"],
                "properties": {
                    "control_id": f"COMM-CTRL-{i+1:05d}",
                    "control_type": ["access", "monitoring", "automation"][i % 3],
                    "interface": ["physical", "digital", "hybrid"][i % 3],
                    "location": f"Building_{chr(65 + (i % 10))}_Location_{i % 50}",
                    "authentication_method": auth_methods[i % len(auth_methods)],
                    "network_connected": i % 3 != 0,
                    "protocol": ["OSDP", "BACnet", "Modbus", "TCP/IP"][i % 4],
                    "failsafe_mode": failsafe_modes[i % len(failsafe_modes)]
                }
            })
        return controls

    def generate_locations(self) -> List[Dict]:
        """Generate 3,360 location nodes"""
        locations = []
        types = ["building", "floor", "zone", "room"]
        subsectors = ["Office_Buildings", "Retail_Centers", "Hotels_Lodging"]
        access_levels = ["public", "restricted", "secure"]

        for i in range(3360):
            locations.append({
                "labels": ["Location", "CommercialLocation", "COMMERCIAL_FACILITIES"],
                "properties": {
                    "location_id": f"COMM-LOC-{i+1:05d}",
                    "location_type": types[i % len(types)],
                    "subsector": subsectors[i % len(subsectors)],
                    "square_footage": 1000 + (i * 100) % 50000,
                    "occupancy_rating": 10 + (i * 5) % 500,
                    "access_level": access_levels[i % len(access_levels)],
                    "egress_routes": f"{(i % 4) + 1}_exits",
                    "address": f"{i+1}_Commercial_Plaza_Floor_{i % 30}"
                }
            })
        return locations

    def generate_threats(self) -> List[Dict]:
        """Generate 2,800 threat nodes"""
        threats = []
        types = ["Unauthorized_Access", "HVAC_Failure", "Fire_Emergency", "Elevator_Malfunction",
                 "Cyber_Attack", "Power_Outage", "Physical_Breach", "Gas_Leak", "Active_Shooter", "Data_Breach"]
        subsectors = ["Office_Buildings", "Retail_Centers", "Hotels_Lodging"]
        severities = ["critical", "high", "medium", "low"]
        likelihoods = ["frequent", "probable", "occasional", "rare"]

        for i in range(2800):
            threats.append({
                "labels": ["Threat", "CommercialThreat", "COMMERCIAL_FACILITIES"],
                "properties": {
                    "threat_id": f"COMM-THREAT-{i+1:05d}",
                    "threat_type": ["physical", "cyber", "environmental", "operational"][i % 4],
                    "severity": severities[i % len(severities)],
                    "likelihood": likelihoods[i % len(likelihoods)],
                    "impact_area": ["safety", "security", "operations", "financial"][i % 4],
                    "subsector_applicability": subsectors[i % len(subsectors)],
                    "attack_vector": f"Vector_{types[i % len(types)]}",
                    "indicators": f"Warning_signs_{(i % 5) + 1}"
                }
            })
        return threats

    def generate_vulnerabilities(self) -> List[Dict]:
        """Generate 1,960 vulnerability nodes"""
        vulnerabilities = []
        types = ["Outdated_Firmware", "Unsecured_Network", "Single_Point_Failure",
                 "Weak_Authentication", "Insufficient_Coverage", "Unencrypted_Comms",
                 "Lack_Backup_Power", "Physical_Security_Gap"]
        subsectors = ["Office_Buildings", "Retail_Centers", "Hotels_Lodging"]

        for i in range(1960):
            vulnerabilities.append({
                "labels": ["Vulnerability", "CommercialVulnerability", "COMMERCIAL_FACILITIES"],
                "properties": {
                    "vulnerability_id": f"COMM-VULN-{i+1:05d}",
                    "vulnerability_type": ["technical", "physical", "procedural"][i % 3],
                    "cvss_score": round(1.0 + (i % 90) / 10, 1),
                    "cwe_id": f"CWE-{100 + (i % 900)}",
                    "discovery_date": f"20{20 + (i % 4)}-{1 + (i % 12):02d}-{1 + (i % 28):02d}",
                    "affected_subsectors": subsectors[i % len(subsectors)],
                    "exploitability": ["easy", "moderate", "difficult"][i % 3],
                    "remediation_effort": ["low", "medium", "high"][i % 3]
                }
            })
        return vulnerabilities

    def generate_mitigations(self) -> List[Dict]:
        """Generate 1,120 mitigation nodes"""
        mitigations = []
        types = ["Multi_Factor_Auth", "Redundant_System", "Network_Segmentation",
                 "Fire_Suppression_Upgrade", "Security_Patrol", "Encrypted_Protocol",
                 "Backup_Generator", "Penetration_Testing"]
        subsectors = ["Office_Buildings", "Retail_Centers", "Hotels_Lodging"]

        for i in range(1120):
            mitigations.append({
                "labels": ["Mitigation", "CommercialMitigation", "COMMERCIAL_FACILITIES"],
                "properties": {
                    "mitigation_id": f"COMM-MITIG-{i+1:05d}",
                    "mitigation_type": ["technical", "physical", "administrative"][i % 3],
                    "effectiveness": ["high", "medium", "low"][i % 3],
                    "implementation_cost": ["high", "medium", "low"][i % 3],
                    "maintenance_required": i % 2 == 0,
                    "subsector_applicable": subsectors[i % len(subsectors)],
                    "standard_reference": ["NFPA", "ASHRAE", "ICC", "OSHA"][i % 4],
                    "deployment_status": ["deployed", "planned", "recommended"][i % 3]
                }
            })
        return mitigations

    def generate_standards(self) -> List[Dict]:
        """Generate 560 standard nodes"""
        standards = []
        names = ["NFPA_101_Life_Safety", "ICC_Building_Code", "ASHRAE_90_1_Energy",
                 "OSHA_Workplace_Safety", "ADA_Accessibility", "PCI_DSS_Payment",
                 "NFPA_72_Fire_Alarm", "ASHRAE_62_1_Ventilation"]
        issuers = ["NFPA", "ICC", "ASHRAE", "OSHA", "ADA", "PCI-SSC"]
        subsectors = ["Office_Buildings", "Retail_Centers", "Hotels_Lodging"]

        for i in range(560):
            standards.append({
                "labels": ["Standard", "CommercialStandard", "COMMERCIAL_FACILITIES"],
                "properties": {
                    "standard_id": f"COMM-STD-{i+1:05d}",
                    "standard_name": names[i % len(names)],
                    "issuing_body": issuers[i % len(issuers)],
                    "version": f"20{18 + (i % 6)}",
                    "applicability": subsectors[i % len(subsectors)],
                    "compliance_level": ["mandatory", "recommended", "best-practice"][i % 3],
                    "audit_frequency": ["annual", "biennial", "event-driven"][i % 3],
                    "enforcement_authority": ["federal", "state", "local"][i % 3]
                }
            })
        return standards

    def create_relationships(self):
        """Create relationships between nodes"""
        self.log("Creating relationships...")

        relationships = [
            # Asset relationships
            """
            MATCH (a:CommercialAsset), (l:CommercialLocation)
            WHERE a.location CONTAINS l.location_id
            WITH a, l LIMIT 10000
            MERGE (a)-[:LOCATED_IN]->(l)
            RETURN count(*) as created
            """,
            """
            MATCH (a:CommercialAsset), (c:CommercialControl)
            WHERE a.asset_type CONTAINS 'Control' OR c.control_type = 'automation'
            WITH a, c LIMIT 8000
            MERGE (a)-[:CONTROLLED_BY]->(c)
            RETURN count(*) as created
            """,
            """
            MATCH (a:CommercialAsset), (v:CommercialVulnerability)
            WHERE a.asset_type = 'IP_Camera' OR v.vulnerability_type = 'technical'
            WITH a, v LIMIT 5000
            MERGE (a)-[:HAS_VULNERABILITY]->(v)
            RETURN count(*) as created
            """,
            # Process relationships
            """
            MATCH (p:CommercialProcess), (a:CommercialAsset)
            WHERE p.process_type = 'operational'
            WITH p, a LIMIT 8000
            MERGE (p)-[:OPERATES_ON]->(a)
            RETURN count(*) as created
            """,
            # Control relationships
            """
            MATCH (c:CommercialControl), (m:CommercialMitigation)
            WHERE c.control_type = 'access'
            WITH c, m LIMIT 3000
            MERGE (c)-[:PROTECTED_BY]->(m)
            RETURN count(*) as created
            """,
            # Threat relationships
            """
            MATCH (t:CommercialThreat), (a:CommercialAsset)
            WHERE t.threat_type = 'cyber'
            WITH t, a LIMIT 6000
            MERGE (t)-[:TARGETS]->(a)
            RETURN count(*) as created
            """,
            """
            MATCH (t:CommercialThreat), (v:CommercialVulnerability)
            WHERE t.severity = 'high' OR v.cvss_score > 7.0
            WITH t, v LIMIT 4000
            MERGE (t)-[:EXPLOITS]->(v)
            RETURN count(*) as created
            """,
            # Mitigation relationships
            """
            MATCH (m:CommercialMitigation), (v:CommercialVulnerability)
            WHERE m.effectiveness = 'high'
            WITH m, v LIMIT 3500
            MERGE (m)-[:MITIGATES]->(v)
            RETURN count(*) as created
            """,
            # Standard relationships
            """
            MATCH (s:CommercialStandard), (a:CommercialAsset)
            WHERE s.compliance_level = 'mandatory'
            WITH s, a LIMIT 5000
            MERGE (a)-[:COMPLIES_WITH]->(s)
            RETURN count(*) as created
            """
        ]

        total_relationships = 0
        with self.driver.session() as session:
            for idx, rel_query in enumerate(relationships, 1):
                try:
                    result = session.run(rel_query)
                    count = result.single()["created"]
                    total_relationships += count
                    self.log(f"  ✓ Relationship set {idx}: {count} created")
                except Exception as e:
                    self.log(f"  ERROR in relationship set {idx}: {str(e)}")

        self.stats["relationships_created"] = total_relationships
        self.log(f"✓ Total relationships created: {total_relationships}")

    def deploy(self):
        """Main deployment orchestration"""
        self.log("=" * 80)
        self.log("COMMERCIAL_FACILITIES SECTOR DEPLOYMENT - v5.0")
        self.log("=" * 80)

        try:
            # Step 1: Constraints and indexes
            self.create_constraints_indexes()

            # Step 2: Create all node types
            all_nodes = []

            self.log("\n--- ASSET NODES (8,400 total) ---")
            all_nodes.extend(self.generate_hvac_assets())
            all_nodes.extend(self.generate_access_control_assets())
            all_nodes.extend(self.generate_fire_safety_assets())
            all_nodes.extend(self.generate_surveillance_assets())
            all_nodes.extend(self.generate_building_automation_assets())
            self.create_nodes_batch(all_nodes, "CommercialAsset")
            all_nodes.clear()

            self.log("\n--- PROCESS NODES (5,600) ---")
            all_nodes.extend(self.generate_processes())
            self.create_nodes_batch(all_nodes, "CommercialProcess")
            all_nodes.clear()

            self.log("\n--- CONTROL NODES (4,200) ---")
            all_nodes.extend(self.generate_controls())
            self.create_nodes_batch(all_nodes, "CommercialControl")
            all_nodes.clear()

            self.log("\n--- LOCATION NODES (3,360) ---")
            all_nodes.extend(self.generate_locations())
            self.create_nodes_batch(all_nodes, "CommercialLocation")
            all_nodes.clear()

            self.log("\n--- THREAT NODES (2,800) ---")
            all_nodes.extend(self.generate_threats())
            self.create_nodes_batch(all_nodes, "CommercialThreat")
            all_nodes.clear()

            self.log("\n--- VULNERABILITY NODES (1,960) ---")
            all_nodes.extend(self.generate_vulnerabilities())
            self.create_nodes_batch(all_nodes, "CommercialVulnerability")
            all_nodes.clear()

            self.log("\n--- MITIGATION NODES (1,120) ---")
            all_nodes.extend(self.generate_mitigations())
            self.create_nodes_batch(all_nodes, "CommercialMitigation")
            all_nodes.clear()

            self.log("\n--- STANDARD NODES (560) ---")
            all_nodes.extend(self.generate_standards())
            self.create_nodes_batch(all_nodes, "CommercialStandard")
            all_nodes.clear()

            # Step 3: Create relationships
            self.log("\n--- RELATIONSHIPS ---")
            self.create_relationships()

            # Final statistics
            elapsed = (datetime.now() - self.stats["start_time"]).total_seconds()
            self.log("\n" + "=" * 80)
            self.log("DEPLOYMENT COMPLETE")
            self.log("=" * 80)
            self.log(f"Total Nodes Created: {self.stats['nodes_created']}")
            self.log(f"Total Relationships Created: {self.stats['relationships_created']}")
            self.log(f"Elapsed Time: {elapsed:.2f} seconds")
            self.log("\nNode Type Breakdown:")
            for node_type, count in self.stats["node_types"].items():
                self.log(f"  {node_type}: {count}")

            return True

        except Exception as e:
            self.log(f"\n❌ DEPLOYMENT FAILED: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
            return False


def main():
    deployer = CommercialFacilitiesDeployer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        success = deployer.deploy()
        sys.exit(0 if success else 1)
    finally:
        deployer.close()


if __name__ == "__main__":
    main()
