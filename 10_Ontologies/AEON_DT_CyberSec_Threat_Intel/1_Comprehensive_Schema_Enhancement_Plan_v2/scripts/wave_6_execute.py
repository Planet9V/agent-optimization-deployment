#!/usr/bin/env python3
"""
Wave 6: UCO (Unified Cyber Ontology) and STIX 2.1 Integration
Core implementation of UCO observables and STIX 2.1 objects for threat intelligence sharing
"""

import logging
import json
from datetime import datetime
from typing import Dict
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave6Executor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log_file = "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/logs/wave_6_execution.jsonl"

    def log_operation(self, operation: str, details: dict):
        log_entry = {"timestamp": datetime.utcnow().isoformat(), "operation": operation, "details": details}
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        logging.info(f"{operation}: {details}")

    def execute(self):
        try:
            self.log_operation("wave_6_execution_started", {"timestamp": datetime.utcnow().isoformat()})

            self.log_operation("phase_started", {"phase": "constraints_and_indexes"})
            self.create_constraints_and_indexes()
            self.log_operation("phase_completed", {"phase": "constraints_and_indexes"})

            self.log_operation("phase_started", {"phase": "create_uco_stix_nodes"})
            uco_obs = self.create_uco_observables()
            stix_sdo = self.create_stix_domain_objects()
            stix_sco = self.create_stix_cyber_observables()
            investigation = self.create_investigation_cases()
            total_nodes = uco_obs + stix_sdo + stix_sco + investigation
            self.log_operation("phase_completed", {"phase": "create_uco_stix_nodes", "nodes_created": total_nodes})

            self.log_operation("phase_started", {"phase": "create_relationships"})
            relationship_counts = self.create_relationships()
            total_rels = sum(relationship_counts.values())
            self.log_operation("phase_completed", {"phase": "create_relationships", "total_relationships": total_rels})

            self.log_operation("wave_6_execution_completed", {
                "timestamp": datetime.utcnow().isoformat(),
                "nodes_created": total_nodes,
                "relationships_created": total_rels
            })

            logging.info(f"Wave 6 completed successfully: {total_nodes} nodes, {total_rels} relationships")

        except Exception as e:
            self.log_operation("wave_6_execution_error", {"error": str(e)})
            logging.error(f"Wave 6 execution failed: {e}")
            raise
        finally:
            self.driver.close()

    def create_constraints_and_indexes(self):
        constraints_and_indexes = [
            "CREATE CONSTRAINT uco_observable_id_unique IF NOT EXISTS FOR (o:UCO_Observable) REQUIRE o.observable_id IS UNIQUE",
            "CREATE CONSTRAINT stix_object_id_unique IF NOT EXISTS FOR (s:STIX_Object) REQUIRE s.stix_id IS UNIQUE",
            "CREATE CONSTRAINT investigation_case_id_unique IF NOT EXISTS FOR (c:Investigation_Case) REQUIRE c.case_id IS UNIQUE",
            "CREATE INDEX uco_observable_type_idx IF NOT EXISTS FOR (o:UCO_Observable) ON (o.observable_type)",
            "CREATE INDEX stix_object_type_idx IF NOT EXISTS FOR (s:STIX_Object) ON (s.stix_type)",
            "CREATE INDEX stix_object_created_idx IF NOT EXISTS FOR (s:STIX_Object) ON (s.created)",
            "CREATE INDEX investigation_case_status_idx IF NOT EXISTS FOR (c:Investigation_Case) ON (c.case_status)"
        ]

        with self.driver.session() as session:
            for statement in constraints_and_indexes:
                session.run(statement)
                self.log_operation("constraint_or_index_created", {"statement": statement[:80] + "..."})

    def create_uco_observables(self) -> int:
        """Create 15 UCO Observable types"""
        query = """
        UNWIND [
          {type: "File", desc: "File system object with hash, size, path"},
          {type: "NetworkConnection", desc: "Network connection with source/dest IP, ports, protocol"},
          {type: "Process", desc: "Running process with PID, command line, parent process"},
          {type: "UserAccount", desc: "User account with username, privileges, creation date"},
          {type: "EmailMessage", desc: "Email message with sender, recipients, subject, body"},
          {type: "IPv4Address", desc: "IPv4 network address"},
          {type: "IPv6Address", desc: "IPv6 network address"},
          {type: "DomainName", desc: "DNS domain name"},
          {type: "URL", desc: "Uniform Resource Locator"},
          {type: "MACAddress", desc: "Media Access Control address"},
          {type: "WindowsRegistryKey", desc: "Windows registry key and values"},
          {type: "Directory", desc: "File system directory"},
          {type: "AutonomousSystem", desc: "BGP autonomous system"},
          {type: "X509Certificate", desc: "X.509 digital certificate"},
          {type: "Software", desc: "Software product with name, version, vendor"}
        ] AS obs
        CREATE (o:UCO_Observable {
          observable_id: randomUUID(),
          observable_type: obs.type,
          description: obs.desc,
          uco_version: "1.2.0",
          created_date: datetime(),
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE6",
          last_updated: datetime(),
          validation_status: "VALIDATED"
        })
        RETURN count(o) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("uco_observables_created", {"count": count})
            return count

    def create_stix_domain_objects(self) -> int:
        """Create 12 STIX Domain Object types"""
        query = """
        UNWIND [
          {type: "attack-pattern", name: "STIX Attack Pattern", desc: "TTP from MITRE ATT&CK"},
          {type: "campaign", name: "STIX Campaign", desc: "Coordinated threat activity"},
          {type: "course-of-action", name: "STIX Course of Action", desc: "Response/mitigation action"},
          {type: "identity", name: "STIX Identity", desc: "Individual, organization, group"},
          {type: "indicator", name: "STIX Indicator", desc: "Pattern for detecting malicious activity"},
          {type: "infrastructure", name: "STIX Infrastructure", desc: "Systems, software, services used by adversary"},
          {type: "intrusion-set", name: "STIX Intrusion Set", desc: "Grouped threat actor activity"},
          {type: "malware", name: "STIX Malware", desc: "Malicious software instance"},
          {type: "threat-actor", name: "STIX Threat Actor", desc: "Individual or group with malicious intent"},
          {type: "tool", name: "STIX Tool", desc: "Legitimate software used for attack"},
          {type: "vulnerability", name: "STIX Vulnerability", desc: "Weakness in system (CVE mapping)"},
          {type: "report", name: "STIX Report", desc: "Collections of threat intelligence"}
        ] AS sdo
        CREATE (s:STIX_Object:STIX_Domain_Object {
          stix_id: "STIX-SDO-" + randomUUID(),
          stix_type: sdo.type,
          name: sdo.name,
          description: sdo.desc,
          spec_version: "2.1",
          created: datetime(),
          modified: datetime(),
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE6",
          last_updated: datetime(),
          validation_status: "VALIDATED"
        })
        RETURN count(s) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("stix_domain_objects_created", {"count": count})
            return count

    def create_stix_cyber_observables(self) -> int:
        """Create 18 STIX Cyber-observable Object types"""
        query = """
        UNWIND [
          {type: "artifact", name: "Artifact", desc: "Raw binary or text data"},
          {type: "autonomous-system", name: "Autonomous System", desc: "BGP AS number"},
          {type: "directory", name: "Directory", desc: "File system directory"},
          {type: "domain-name", name: "Domain Name", desc: "DNS domain"},
          {type: "email-addr", name: "Email Address", desc: "Email address"},
          {type: "email-message", name: "Email Message", desc: "Email instance"},
          {type: "file", name: "File", desc: "File object with hashes"},
          {type: "ipv4-addr", name: "IPv4 Address", desc: "IPv4 address"},
          {type: "ipv6-addr", name: "IPv6 Address", desc: "IPv6 address"},
          {type: "mac-addr", name: "MAC Address", desc: "MAC address"},
          {type: "mutex", name: "Mutex", desc: "Named mutex"},
          {type: "network-traffic", name: "Network Traffic", desc: "Network connection"},
          {type: "process", name: "Process", desc: "Running process"},
          {type: "software", name: "Software", desc: "Software product"},
          {type: "url", name: "URL", desc: "Uniform Resource Locator"},
          {type: "user-account", name: "User Account", desc: "User account"},
          {type: "windows-registry-key", name: "Windows Registry Key", desc: "Registry key"},
          {type: "x509-certificate", name: "X.509 Certificate", desc: "Digital certificate"}
        ] AS sco
        CREATE (s:STIX_Object:STIX_Cyber_Observable {
          stix_id: "STIX-SCO-" + randomUUID(),
          stix_type: sco.type,
          name: sco.name,
          description: sco.desc,
          spec_version: "2.1",
          created: datetime(),
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE6",
          last_updated: datetime(),
          validation_status: "VALIDATED"
        })
        RETURN count(s) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("stix_cyber_observables_created", {"count": count})
            return count

    def create_investigation_cases(self) -> int:
        """Create 10 sample investigation cases"""
        query = """
        UNWIND range(1, 10) AS case_num
        CREATE (c:Investigation_Case {
          case_id: "CASE-" + toString(case_num),
          case_name: "Investigation Case " + toString(case_num),
          case_status: CASE
            WHEN case_num <= 3 THEN "OPEN"
            WHEN case_num <= 7 THEN "IN_PROGRESS"
            ELSE "CLOSED"
          END,
          case_priority: CASE
            WHEN case_num % 3 = 0 THEN "HIGH"
            WHEN case_num % 3 = 1 THEN "MEDIUM"
            ELSE "LOW"
          END,
          case_type: "Cyber Investigation",
          created_date: datetime(),
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE6",
          last_updated: datetime()
        })
        RETURN count(c) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("investigation_cases_created", {"count": count})
            return count

    def create_relationships(self) -> Dict[str, int]:
        """Create relationships for Wave 6"""
        relationship_counts = {}

        with self.driver.session() as session:
            # 1. Map ATT&CK techniques to STIX Attack Patterns
            query1 = """
            MATCH (tech:ICS_Technique)
            MATCH (stix:STIX_Domain_Object {stix_type: "attack-pattern"})
            WITH tech, stix
            LIMIT 50
            CREATE (tech)-[r:MAPS_TO_STIX {
              relationship_id: randomUUID(),
              mapping_type: "attack_pattern",
              confidence_score: 0.95,
              created_date: datetime()
            }]->(stix)
            RETURN count(r) as count
            """
            result = session.run(query1)
            relationship_counts["MAPS_TO_STIX_ATTACK_PATTERN"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "MAPS_TO_STIX_ATTACK_PATTERN", "count": relationship_counts["MAPS_TO_STIX_ATTACK_PATTERN"]})

            # 2. Map CVEs to STIX Vulnerabilities
            query2 = """
            MATCH (cve:CVE)
            MATCH (stix:STIX_Domain_Object {stix_type: "vulnerability"})
            WITH cve, stix
            LIMIT 100
            CREATE (cve)-[r:MAPS_TO_STIX {
              relationship_id: randomUUID(),
              mapping_type: "vulnerability",
              confidence_score: 1.0,
              created_date: datetime()
            }]->(stix)
            RETURN count(r) as count
            """
            result = session.run(query2)
            relationship_counts["MAPS_TO_STIX_VULNERABILITY"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "MAPS_TO_STIX_VULNERABILITY", "count": relationship_counts["MAPS_TO_STIX_VULNERABILITY"]})

            # 3. Link UCO observables to STIX cyber-observables
            query3 = """
            MATCH (uco:UCO_Observable), (stix:STIX_Cyber_Observable)
            WHERE uco.observable_type = "File" AND stix.stix_type = "file"
               OR uco.observable_type = "IPv4Address" AND stix.stix_type = "ipv4-addr"
               OR uco.observable_type = "DomainName" AND stix.stix_type = "domain-name"
               OR uco.observable_type = "URL" AND stix.stix_type = "url"
            CREATE (uco)-[r:EQUIVALENT_TO_STIX {
              relationship_id: randomUUID(),
              equivalence_type: "type_mapping",
              created_date: datetime()
            }]->(stix)
            RETURN count(r) as count
            """
            result = session.run(query3)
            relationship_counts["EQUIVALENT_TO_STIX"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "EQUIVALENT_TO_STIX", "count": relationship_counts["EQUIVALENT_TO_STIX"]})

            # 4. Link investigation cases to UCO observables
            query4 = """
            MATCH (case:Investigation_Case), (obs:UCO_Observable)
            WITH case, obs
            WHERE toInteger(split(case.case_id, "-")[1]) <= 5 AND obs.observable_type IN ["File", "NetworkConnection", "Process"]
            CREATE (case)-[r:CONTAINS_EVIDENCE {
              relationship_id: randomUUID(),
              evidence_type: obs.observable_type,
              chain_of_custody: true,
              created_date: datetime()
            }]->(obs)
            RETURN count(r) as count
            """
            result = session.run(query4)
            relationship_counts["CONTAINS_EVIDENCE"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "CONTAINS_EVIDENCE", "count": relationship_counts["CONTAINS_EVIDENCE"]})

        return relationship_counts

if __name__ == "__main__":
    executor = Wave6Executor()
    executor.execute()
