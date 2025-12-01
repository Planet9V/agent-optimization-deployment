#!/usr/bin/env python3
"""
Wave 5: MITRE ATT&CK ICS Framework Integration
Complete integration of ICS tactics, techniques, assets, protocols, and critical infrastructure sectors
"""

import logging
import json
from datetime import datetime
from typing import Dict, List
from neo4j import GraphDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Wave5Executor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log_file = "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/logs/wave_5_execution.jsonl"

    def log_operation(self, operation: str, details: dict):
        """Log operation to JSON Lines file"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "details": details
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        logging.info(f"{operation}: {details}")

    def execute(self):
        """Execute Wave 5 implementation"""
        try:
            self.log_operation("wave_5_execution_started", {"timestamp": datetime.utcnow().isoformat()})

            # Phase 1: Create constraints and indexes
            self.log_operation("phase_started", {"phase": "constraints_and_indexes"})
            self.create_constraints_and_indexes()
            self.log_operation("phase_completed", {"phase": "constraints_and_indexes"})

            # Phase 2: Create core ICS nodes
            self.log_operation("phase_started", {"phase": "create_ics_nodes"})
            tactics = self.create_ics_tactics()
            techniques = self.create_ics_techniques()
            assets = self.create_ics_assets()
            protocols = self.create_ics_protocols()
            sectors = self.create_critical_infrastructure_sectors()

            total_nodes = tactics + techniques + assets + protocols + sectors
            self.log_operation("phase_completed", {"phase": "create_ics_nodes", "nodes_created": total_nodes})

            # Phase 3: Create relationships
            self.log_operation("phase_started", {"phase": "create_relationships"})
            relationship_counts = self.create_relationships()
            total_rels = sum(relationship_counts.values())
            self.log_operation("phase_completed", {"phase": "create_relationships", "total_relationships": total_rels})

            self.log_operation("wave_5_execution_completed", {
                "timestamp": datetime.utcnow().isoformat(),
                "nodes_created": total_nodes,
                "relationships_created": total_rels
            })

            logging.info(f"Wave 5 completed successfully: {total_nodes} nodes, {total_rels} relationships")

        except Exception as e:
            self.log_operation("wave_5_execution_error", {"error": str(e)})
            logging.error(f"Wave 5 execution failed: {e}")
            raise
        finally:
            self.driver.close()

    def create_constraints_and_indexes(self):
        """Create all constraints and indexes for Wave 5"""
        constraints_and_indexes = [
            # Constraints
            "CREATE CONSTRAINT ics_tactic_id_unique IF NOT EXISTS FOR (t:ICS_Tactic) REQUIRE t.tactic_id IS UNIQUE",
            "CREATE CONSTRAINT ics_technique_id_unique IF NOT EXISTS FOR (t:ICS_Technique) REQUIRE t.technique_id IS UNIQUE",
            "CREATE CONSTRAINT ics_asset_id_unique IF NOT EXISTS FOR (a:ICS_Asset) REQUIRE a.asset_id IS UNIQUE",
            "CREATE CONSTRAINT ics_protocol_id_unique IF NOT EXISTS FOR (p:ICS_Protocol) REQUIRE p.protocol_id IS UNIQUE",
            "CREATE CONSTRAINT sector_id_unique IF NOT EXISTS FOR (s:Critical_Infrastructure_Sector) REQUIRE s.sector_id IS UNIQUE",

            # Indexes
            "CREATE INDEX ics_tactic_name_idx IF NOT EXISTS FOR (t:ICS_Tactic) ON (t.name)",
            "CREATE INDEX ics_tactic_order_idx IF NOT EXISTS FOR (t:ICS_Tactic) ON (t.order_position)",
            "CREATE INDEX ics_technique_name_idx IF NOT EXISTS FOR (t:ICS_Technique) ON (t.name)",
            "CREATE INDEX ics_technique_severity_idx IF NOT EXISTS FOR (t:ICS_Technique) ON (t.severity_rating)",
            "CREATE INDEX ics_asset_type_idx IF NOT EXISTS FOR (a:ICS_Asset) ON (a.asset_type)",
            "CREATE INDEX ics_asset_criticality_idx IF NOT EXISTS FOR (a:ICS_Asset) ON (a.criticality)",
            "CREATE INDEX ics_asset_purdue_idx IF NOT EXISTS FOR (a:ICS_Asset) ON (a.purdue_level)",
            "CREATE INDEX ics_asset_zone_idx IF NOT EXISTS FOR (a:ICS_Asset) ON (a.network_zone)",
            "CREATE INDEX ics_protocol_name_idx IF NOT EXISTS FOR (p:ICS_Protocol) ON (p.protocol_name)",
            "CREATE INDEX sector_name_idx IF NOT EXISTS FOR (s:Critical_Infrastructure_Sector) ON (s.sector_name)"
        ]

        with self.driver.session() as session:
            for statement in constraints_and_indexes:
                session.run(statement)
                self.log_operation("constraint_or_index_created", {"statement": statement[:80] + "..."})

    def create_ics_tactics(self) -> int:
        """Create 12 ICS Tactics"""
        query = """
        UNWIND [
          {tactic_id: "TA0108", name: "Initial Access", order: 1, desc: "Gain initial foothold in ICS environment"},
          {tactic_id: "TA0109", name: "Execution", order: 2, desc: "Execute adversary-controlled code in ICS"},
          {tactic_id: "TA0110", name: "Persistence", order: 3, desc: "Maintain presence in ICS environment"},
          {tactic_id: "TA0111", name: "Privilege Escalation", order: 4, desc: "Gain higher-level permissions in ICS"},
          {tactic_id: "TA0112", name: "Evasion", order: 5, desc: "Avoid detection in ICS environment"},
          {tactic_id: "TA0100", name: "Impair Process Control", order: 6, desc: "Manipulate or disable industrial process control"},
          {tactic_id: "TA0101", name: "Inhibit Response Function", order: 7, desc: "Prevent safety systems and response"},
          {tactic_id: "TA0102", name: "Collection", order: 8, desc: "Gather ICS process data and intelligence"},
          {tactic_id: "TA0103", name: "Command and Control", order: 9, desc: "Communicate with compromised ICS systems"},
          {tactic_id: "TA0104", name: "Lateral Movement", order: 10, desc: "Move through ICS network zones"},
          {tactic_id: "TA0105", name: "Discovery", order: 11, desc: "Gain knowledge of ICS environment"},
          {tactic_id: "TA0106", name: "Impact", order: 12, desc: "Disrupt, manipulate, or destroy ICS processes"}
        ] AS tactic
        CREATE (t:ICS_Tactic {
          tactic_id: tactic.tactic_id,
          name: tactic.name,
          description: tactic.desc,
          order_position: tactic.order,
          attack_domain: "ics",
          version: "v13",
          mitre_url: "https://attack.mitre.org/tactics/" + tactic.tactic_id,
          created_date: datetime(),
          modified_date: datetime(),
          classification: "MITRE_ICS_TACTIC",
          confidence_score: 1.0,
          data_source: "MITRE ATT&CK ICS v13",
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE5",
          last_updated: datetime(),
          validation_status: "VALIDATED"
        })
        RETURN count(t) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("ics_tactics_created", {"count": count})
            return count

    def create_ics_techniques(self) -> int:
        """Create 78+ ICS Techniques"""
        query = """
        UNWIND [
          {id: "T0800", name: "Activate Firmware Update Mode", severity: "HIGH", tactics: ["TA0110"]},
          {id: "T0801", name: "Monitor Process State", severity: "MEDIUM", tactics: ["TA0102"]},
          {id: "T0802", name: "Automated Collection", severity: "MEDIUM", tactics: ["TA0102"]},
          {id: "T0803", name: "Block Command Message", severity: "HIGH", tactics: ["TA0101"]},
          {id: "T0804", name: "Block Reporting Message", severity: "HIGH", tactics: ["TA0101"]},
          {id: "T0805", name: "Block Serial COM", severity: "HIGH", tactics: ["TA0101"]},
          {id: "T0806", name: "Brute Force I/O", severity: "CRITICAL", tactics: ["TA0100"]},
          {id: "T0807", name: "Command-Line Interface", severity: "MEDIUM", tactics: ["TA0109"]},
          {id: "T0808", name: "Control Device Identification", severity: "MEDIUM", tactics: ["TA0105"]},
          {id: "T0809", name: "Data Destruction", severity: "CRITICAL", tactics: ["TA0106"]},
          {id: "T0810", name: "Data Historian Compromise", severity: "HIGH", tactics: ["TA0102"]},
          {id: "T0811", name: "Data from Information Repositories", severity: "MEDIUM", tactics: ["TA0102"]},
          {id: "T0812", name: "Default Credentials", severity: "HIGH", tactics: ["TA0108"]},
          {id: "T0813", name: "Denial of Control", severity: "CRITICAL", tactics: ["TA0106"]},
          {id: "T0814", name: "Denial of View", severity: "HIGH", tactics: ["TA0106"]},
          {id: "T0815", name: "Denial of Service", severity: "HIGH", tactics: ["TA0101", "TA0106"]},
          {id: "T0816", name: "Device Restart/Shutdown", severity: "HIGH", tactics: ["TA0101"]},
          {id: "T0817", name: "Drive-by Compromise", severity: "MEDIUM", tactics: ["TA0108"]},
          {id: "T0818", name: "Engineering Workstation Compromise", severity: "CRITICAL", tactics: ["TA0108"]},
          {id: "T0819", name: "Exploit Public-Facing Application", severity: "HIGH", tactics: ["TA0108"]},
          {id: "T0820", name: "Exploitation for Evasion", severity: "MEDIUM", tactics: ["TA0112"]},
          {id: "T0821", name: "Modify Controller Tasking", severity: "CRITICAL", tactics: ["TA0100", "TA0109", "TA0110"]},
          {id: "T0822", name: "External Remote Services", severity: "HIGH", tactics: ["TA0108", "TA0110"]},
          {id: "T0823", name: "Graphical User Interface", severity: "MEDIUM", tactics: ["TA0109"]},
          {id: "T0824", name: "I/O Module Discovery", severity: "MEDIUM", tactics: ["TA0105"]},
          {id: "T0825", name: "Location Identification", severity: "LOW", tactics: ["TA0105"]},
          {id: "T0826", name: "Loss of Availability", severity: "CRITICAL", tactics: ["TA0106"]},
          {id: "T0827", name: "Loss of Control", severity: "CRITICAL", tactics: ["TA0106"]},
          {id: "T0828", name: "Loss of Productivity and Revenue", severity: "HIGH", tactics: ["TA0106"]},
          {id: "T0829", name: "Loss of Protection", severity: "CRITICAL", tactics: ["TA0106"]},
          {id: "T0830", name: "Man in the Middle", severity: "HIGH", tactics: ["TA0102", "TA0103"]},
          {id: "T0831", name: "Manipulation of Control", severity: "CRITICAL", tactics: ["TA0100"]},
          {id: "T0832", name: "Manipulation of View", severity: "HIGH", tactics: ["TA0100"]},
          {id: "T0833", name: "Modify Alarm Settings", severity: "HIGH", tactics: ["TA0101"]},
          {id: "T0834", name: "Native API", severity: "MEDIUM", tactics: ["TA0109"]},
          {id: "T0835", name: "Network Connection Enumeration", severity: "LOW", tactics: ["TA0105"]},
          {id: "T0836", name: "Modify Parameter", severity: "CRITICAL", tactics: ["TA0100"]},
          {id: "T0837", name: "Loss of Protection", severity: "CRITICAL", tactics: ["TA0106"]},
          {id: "T0838", name: "Modify Program", severity: "CRITICAL", tactics: ["TA0100", "TA0110"]},
          {id: "T0839", name: "Module Firmware", severity: "HIGH", tactics: ["TA0110"]},
          {id: "T0840", name: "Network Connection Proxy", severity: "MEDIUM", tactics: ["TA0103", "TA0112"]},
          {id: "T0841", name: "Network Service Scanning", severity: "LOW", tactics: ["TA0105"]},
          {id: "T0842", name: "Network Sniffing", severity: "MEDIUM", tactics: ["TA0102", "TA0105"]},
          {id: "T0843", name: "Program Download", severity: "HIGH", tactics: ["TA0109", "TA0110"]},
          {id: "T0844", name: "Program Organization Units", severity: "MEDIUM", tactics: ["TA0105"]},
          {id: "T0845", name: "Program Upload", severity: "HIGH", tactics: ["TA0102"]},
          {id: "T0846", name: "Project File Infection", severity: "HIGH", tactics: ["TA0110"]},
          {id: "T0847", name: "Replication Through Removable Media", severity: "MEDIUM", tactics: ["TA0108", "TA0104"]},
          {id: "T0848", name: "Rogue Master", severity: "HIGH", tactics: ["TA0100"]},
          {id: "T0849", name: "Masquerading", severity: "MEDIUM", tactics: ["TA0112"]},
          {id: "T0850", name: "Role Identification", severity: "LOW", tactics: ["TA0105"]},
          {id: "T0851", name: "Rootkit", severity: "HIGH", tactics: ["TA0112"]},
          {id: "T0852", name: "Screen Capture", severity: "MEDIUM", tactics: ["TA0102"]},
          {id: "T0853", name: "Scripting", severity: "MEDIUM", tactics: ["TA0109"]},
          {id: "T0854", name: "Serial Connection Enumeration", severity: "LOW", tactics: ["TA0105"]},
          {id: "T0855", name: "Unauthorized Command Message", severity: "CRITICAL", tactics: ["TA0100"]},
          {id: "T0856", name: "Spoof Reporting Message", severity: "HIGH", tactics: ["TA0100"]},
          {id: "T0857", name: "System Firmware", severity: "HIGH", tactics: ["TA0110"]},
          {id: "T0858", name: "Change Operating Mode", severity: "HIGH", tactics: ["TA0100"]},
          {id: "T0859", name: "Valid Accounts", severity: "HIGH", tactics: ["TA0108", "TA0110"]},
          {id: "T0860", name: "Wireless Compromise", severity: "HIGH", tactics: ["TA0108"]},
          {id: "T0861", name: "Point & Tag Identification", severity: "MEDIUM", tactics: ["TA0102", "TA0105"]},
          {id: "T0862", name: "Supply Chain Compromise", severity: "HIGH", tactics: ["TA0108"]},
          {id: "T0863", name: "User Execution", severity: "MEDIUM", tactics: ["TA0109"]},
          {id: "T0864", name: "Transient Cyber Asset", severity: "MEDIUM", tactics: ["TA0108"]},
          {id: "T0865", name: "Spearphishing Attachment", severity: "HIGH", tactics: ["TA0108"]},
          {id: "T0866", name: "Exploitation of Remote Services", severity: "HIGH", tactics: ["TA0108", "TA0104"]},
          {id: "T0867", name: "Lateral Tool Transfer", severity: "MEDIUM", tactics: ["TA0104"]},
          {id: "T0868", name: "Detect Operating Mode", severity: "LOW", tactics: ["TA0105"]},
          {id: "T0869", name: "Standard Application Layer Protocol", severity: "MEDIUM", tactics: ["TA0103"]},
          {id: "T0870", name: "Detect Program State", severity: "LOW", tactics: ["TA0105"]},
          {id: "T0871", name: "Execution through API", severity: "MEDIUM", tactics: ["TA0109"]},
          {id: "T0872", name: "Indicator Removal on Host", severity: "MEDIUM", tactics: ["TA0112"]},
          {id: "T0873", name: "Project File Infection", severity: "HIGH", tactics: ["TA0108", "TA0110"]},
          {id: "T0874", name: "Hooking", severity: "MEDIUM", tactics: ["TA0110", "TA0112"]},
          {id: "T0875", name: "Change Program State", severity: "HIGH", tactics: ["TA0100"]},
          {id: "T0876", name: "Remote Services", severity: "HIGH", tactics: ["TA0104"]},
          {id: "T0877", name: "I/O Image", severity: "MEDIUM", tactics: ["TA0102"]},
          {id: "T0878", name: "Alarm Suppression", severity: "HIGH", tactics: ["TA0101"]},
          {id: "T0879", name: "Damage to Property", severity: "CRITICAL", tactics: ["TA0106"]},
          {id: "T0880", name: "Loss of Safety", severity: "CRITICAL", tactics: ["TA0106"]},
          {id: "T0881", name: "Service Stop", severity: "HIGH", tactics: ["TA0101"]},
          {id: "T0882", name: "Theft of Operational Information", severity: "HIGH", tactics: ["TA0102"]}
        ] AS tech
        CREATE (t:ICS_Technique {
          technique_id: tech.id,
          name: tech.name,
          severity_rating: tech.severity,
          tactics: tech.tactics,
          is_subtechnique: false,
          mitre_url: "https://attack.mitre.org/techniques/" + tech.id,
          version: "v13",
          attack_domain: "ics",
          classification: "MITRE_ICS_TECHNIQUE",
          confidence_score: 0.9,
          data_source: "MITRE ATT&CK ICS v13",
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE5",
          created_date: datetime(),
          last_updated: datetime(),
          validation_status: "VALIDATED"
        })
        RETURN count(t) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("ics_techniques_created", {"count": count})
            return count

    def create_ics_assets(self) -> int:
        """Create 16 ICS Asset types"""
        query = """
        UNWIND [
          {type: "Programmable Logic Controller (PLC)", level: 1, criticality: "CRITICAL", zone: "Control Network"},
          {type: "Remote Terminal Unit (RTU)", level: 1, criticality: "HIGH", zone: "Field Network"},
          {type: "Intelligent Electronic Device (IED)", level: 1, criticality: "HIGH", zone: "Field Network"},
          {type: "Variable Frequency Drive (VFD)", level: 0, criticality: "MEDIUM", zone: "Field Network"},
          {type: "Industrial Sensor", level: 0, criticality: "MEDIUM", zone: "Field Network"},
          {type: "Industrial Actuator", level: 0, criticality: "MEDIUM", zone: "Field Network"},
          {type: "SCADA Server", level: 2, criticality: "CRITICAL", zone: "Control Network"},
          {type: "Distributed Control System (DCS)", level: 2, criticality: "CRITICAL", zone: "Control Network"},
          {type: "Human-Machine Interface (HMI)", level: 2, criticality: "HIGH", zone: "Control Network"},
          {type: "Engineering Workstation", level: 2, criticality: "HIGH", zone: "Control Network"},
          {type: "Historian Server", level: 2, criticality: "HIGH", zone: "Control Network"},
          {type: "Safety Instrumented System (SIS)", level: 1, criticality: "CRITICAL", zone: "Safety Network"},
          {type: "Emergency Shutdown System (ESD)", level: 1, criticality: "CRITICAL", zone: "Safety Network"},
          {type: "Industrial Ethernet Switch", level: 2, criticality: "HIGH", zone: "Control Network"},
          {type: "Industrial Firewall", level: 3, criticality: "HIGH", zone: "DMZ"},
          {type: "Data Diode", level: 3, criticality: "MEDIUM", zone: "DMZ"}
        ] AS asset
        CREATE (a:ICS_Asset {
          asset_id: randomUUID(),
          asset_type: asset.type,
          purdue_level: asset.level,
          criticality: asset.criticality,
          network_zone: asset.zone,
          asset_category: CASE
            WHEN asset.level IN [0, 1] THEN "Field Device"
            WHEN asset.level = 2 THEN "Control System"
            ELSE "Network Device"
          END,
          authentication_enabled: asset.level >= 2,
          encryption_supported: asset.level >= 2,
          iec_62443_level: CASE
            WHEN asset.criticality = "CRITICAL" THEN "SL3"
            WHEN asset.criticality = "HIGH" THEN "SL2"
            ELSE "SL1"
          END,
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE5",
          created_date: datetime(),
          last_updated: datetime(),
          validation_status: "VALIDATED"
        })
        RETURN count(a) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("ics_assets_created", {"count": count})
            return count

    def create_ics_protocols(self) -> int:
        """Create 10 ICS Protocols"""
        query = """
        UNWIND [
          {id: "MODBUS-TCP", name: "Modbus TCP/IP", port: 502, auth: false, encrypt: false, level: "WIDESPREAD"},
          {id: "MODBUS-RTU", name: "Modbus RTU", port: null, auth: false, encrypt: false, level: "WIDESPREAD"},
          {id: "DNP3", name: "DNP3 (Distributed Network Protocol)", port: 20000, auth: true, encrypt: true, level: "COMMON"},
          {id: "OPC-UA", name: "OPC Unified Architecture", port: 4840, auth: true, encrypt: true, level: "WIDESPREAD"},
          {id: "PROFINET", name: "Profinet IO", port: 34962, auth: false, encrypt: false, level: "WIDESPREAD"},
          {id: "ETHERNETIP", name: "EtherNet/IP", port: 44818, auth: false, encrypt: false, level: "WIDESPREAD"},
          {id: "BACNET", name: "BACnet/IP", port: 47808, auth: false, encrypt: false, level: "COMMON"},
          {id: "IEC-61850", name: "IEC 61850 (Substation Automation)", port: 102, auth: false, encrypt: false, level: "COMMON"},
          {id: "IEC-60870-5-104", name: "IEC 60870-5-104", port: 2404, auth: false, encrypt: false, level: "COMMON"},
          {id: "S7COMM", name: "Siemens S7 Communication", port: 102, auth: false, encrypt: false, level: "COMMON"}
        ] AS proto
        CREATE (p:ICS_Protocol {
          protocol_id: proto.id,
          protocol_name: proto.name,
          port_numbers: CASE WHEN proto.port IS NOT NULL THEN [proto.port] ELSE [] END,
          authentication_support: proto.auth,
          encryption_support: proto.encrypt,
          adoption_level: proto.level,
          transport_protocol: "TCP",
          osi_layer: 7,
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE5",
          created_date: datetime(),
          last_updated: datetime(),
          validation_status: "VALIDATED"
        })
        RETURN count(p) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("ics_protocols_created", {"count": count})
            return count

    def create_critical_infrastructure_sectors(self) -> int:
        """Create 16 Critical Infrastructure Sectors"""
        query = """
        UNWIND [
          {id: "CISA-SECTOR-CHEMICAL", name: "Chemical Sector", abbr: "CHEMICAL"},
          {id: "CISA-SECTOR-COMMERCIAL", name: "Commercial Facilities Sector", abbr: "COMMERCIAL"},
          {id: "CISA-SECTOR-COMMUNICATIONS", name: "Communications Sector", abbr: "COMMUNICATIONS"},
          {id: "CISA-SECTOR-CRITICAL-MANUFACTURING", name: "Critical Manufacturing Sector", abbr: "MANUFACTURING"},
          {id: "CISA-SECTOR-DAMS", name: "Dams Sector", abbr: "DAMS"},
          {id: "CISA-SECTOR-DEFENSE", name: "Defense Industrial Base Sector", abbr: "DEFENSE"},
          {id: "CISA-SECTOR-EMERGENCY", name: "Emergency Services Sector", abbr: "EMERGENCY"},
          {id: "CISA-SECTOR-ENERGY", name: "Energy Sector", abbr: "ENERGY"},
          {id: "CISA-SECTOR-FINANCIAL", name: "Financial Services Sector", abbr: "FINANCIAL"},
          {id: "CISA-SECTOR-FOOD-AG", name: "Food and Agriculture Sector", abbr: "FOOD-AG"},
          {id: "CISA-SECTOR-GOV-FACILITIES", name: "Government Facilities Sector", abbr: "GOVERNMENT"},
          {id: "CISA-SECTOR-HEALTHCARE", name: "Healthcare and Public Health Sector", abbr: "HEALTHCARE"},
          {id: "CISA-SECTOR-IT", name: "Information Technology Sector", abbr: "IT"},
          {id: "CISA-SECTOR-NUCLEAR", name: "Nuclear Reactors, Materials, and Waste Sector", abbr: "NUCLEAR"},
          {id: "CISA-SECTOR-TRANSPORTATION", name: "Transportation Systems Sector", abbr: "TRANSPORTATION"},
          {id: "CISA-SECTOR-WATER", name: "Water and Wastewater Systems Sector", abbr: "WATER"}
        ] AS sector
        CREATE (s:Critical_Infrastructure_Sector {
          sector_id: sector.id,
          sector_name: sector.name,
          sector_abbreviation: sector.abbr,
          cisa_designation: "Critical Infrastructure Sector",
          security_frameworks: ["NIST CSF", "IEC 62443", "ISO 27001"],
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE5",
          created_date: datetime(),
          last_updated: datetime(),
          validation_status: "VALIDATED"
        })
        RETURN count(s) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("critical_infrastructure_sectors_created", {"count": count})
            return count

    def create_relationships(self) -> Dict[str, int]:
        """Create all relationships for Wave 5"""
        relationship_counts = {}

        with self.driver.session() as session:
            # 1. CONTAINS_ICS_TECHNIQUE (Tactic → Technique)
            query1 = """
            MATCH (tactic:ICS_Tactic), (technique:ICS_Technique)
            WHERE tactic.tactic_id IN technique.tactics
            CREATE (tactic)-[r:CONTAINS_ICS_TECHNIQUE {
              relationship_id: randomUUID(),
              technique_applicability: "PRIMARY",
              confidence_score: 1.0,
              mitre_validated: true,
              created_date: datetime(),
              last_updated: datetime()
            }]->(technique)
            RETURN count(r) as count
            """
            result = session.run(query1)
            relationship_counts["CONTAINS_ICS_TECHNIQUE"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "CONTAINS_ICS_TECHNIQUE", "count": relationship_counts["CONTAINS_ICS_TECHNIQUE"]})

            # 2. TARGETS_ICS_ASSET (Technique → Asset)
            query2 = """
            MATCH (technique:ICS_Technique), (asset:ICS_Asset)
            WHERE (asset.asset_type CONTAINS "PLC" AND technique.technique_id IN ["T0821", "T0836", "T0838", "T0803"]) OR
                  (asset.asset_type CONTAINS "SCADA" AND technique.technique_id IN ["T0810", "T0815", "T0813"]) OR
                  (asset.asset_type CONTAINS "HMI" AND technique.technique_id IN ["T0814", "T0815", "T0823"]) OR
                  (asset.asset_type CONTAINS "Engineering Workstation" AND technique.technique_id IN ["T0818", "T0843"]) OR
                  (asset.asset_type CONTAINS "RTU" AND technique.technique_id IN ["T0803", "T0855"]) OR
                  (asset.asset_type CONTAINS "Safety" AND technique.technique_id IN ["T0821", "T0829", "T0880"])
            CREATE (technique)-[r:TARGETS_ICS_ASSET {
              relationship_id: randomUUID(),
              impact_severity: asset.criticality,
              attack_vector: "Network",
              required_access_level: "ADMIN",
              confidence_score: 0.9,
              created_date: datetime(),
              last_updated: datetime()
            }]->(asset)
            RETURN count(r) as count
            """
            result = session.run(query2)
            relationship_counts["TARGETS_ICS_ASSET"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "TARGETS_ICS_ASSET", "count": relationship_counts["TARGETS_ICS_ASSET"]})

            # 3. USES_PROTOCOL (Asset → Protocol)
            query3 = """
            MATCH (asset:ICS_Asset), (protocol:ICS_Protocol)
            WHERE (asset.asset_type CONTAINS "PLC" AND protocol.protocol_id IN ["MODBUS-TCP", "PROFINET", "ETHERNETIP", "OPC-UA"]) OR
                  (asset.asset_type CONTAINS "SCADA" AND protocol.protocol_id IN ["DNP3", "MODBUS-TCP", "IEC-60870-5-104", "OPC-UA"]) OR
                  (asset.asset_type CONTAINS "RTU" AND protocol.protocol_id IN ["DNP3", "MODBUS-RTU", "IEC-60870-5-104"]) OR
                  (asset.asset_type CONTAINS "IED" AND protocol.protocol_id IN ["IEC-61850", "DNP3"]) OR
                  (asset.asset_type CONTAINS "HMI" AND protocol.protocol_id IN ["OPC-UA", "MODBUS-TCP"])
            CREATE (asset)-[r:USES_PROTOCOL {
              relationship_id: randomUUID(),
              usage_type: "PRIMARY",
              protocol_role: "SERVER",
              security_enabled: false,
              created_date: datetime(),
              last_updated: datetime()
            }]->(protocol)
            RETURN count(r) as count
            """
            result = session.run(query3)
            relationship_counts["USES_PROTOCOL"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "USES_PROTOCOL", "count": relationship_counts["USES_PROTOCOL"]})

            # 4. DEPLOYS_ASSET (Sector → Asset)
            query4 = """
            MATCH (sector:Critical_Infrastructure_Sector), (asset:ICS_Asset)
            WHERE (sector.sector_abbreviation IN ["ENERGY", "WATER", "MANUFACTURING", "CHEMICAL"] AND asset.criticality = "CRITICAL") OR
                  (sector.sector_abbreviation IN ["ENERGY"] AND asset.asset_type CONTAINS "SCADA") OR
                  (sector.sector_abbreviation IN ["WATER"] AND asset.asset_type IN ["SCADA Server", "PLC", "RTU"])
            CREATE (sector)-[r:DEPLOYS_ASSET {
              relationship_id: randomUUID(),
              deployment_prevalence: "UBIQUITOUS",
              criticality_in_sector: asset.criticality,
              regulatory_requirements: ["NERC CIP", "IEC 62443"],
              created_date: datetime(),
              last_updated: datetime()
            }]->(asset)
            RETURN count(r) as count
            """
            result = session.run(query4)
            relationship_counts["DEPLOYS_ASSET"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "DEPLOYS_ASSET", "count": relationship_counts["DEPLOYS_ASSET"]})

            # 5. EXPLOITS_PROTOCOL (Technique → Protocol)
            query5 = """
            MATCH (technique:ICS_Technique), (protocol:ICS_Protocol)
            WHERE (protocol.authentication_support = false AND technique.technique_id IN ["T0855", "T0848", "T0830", "T0856"]) OR
                  (technique.technique_id IN ["T0815", "T0813"] AND protocol.adoption_level = "WIDESPREAD")
            CREATE (technique)-[r:EXPLOITS_PROTOCOL {
              relationship_id: randomUUID(),
              exploitation_method: "Unauthenticated command injection",
              protocol_weakness_exploited: "No authentication mechanism",
              detection_difficulty: "MODERATE",
              created_date: datetime(),
              last_updated: datetime()
            }]->(protocol)
            RETURN count(r) as count
            """
            result = session.run(query5)
            relationship_counts["EXPLOITS_PROTOCOL"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "EXPLOITS_PROTOCOL", "count": relationship_counts["EXPLOITS_PROTOCOL"]})

        return relationship_counts

if __name__ == "__main__":
    executor = Wave5Executor()
    executor.execute()
