#!/usr/bin/env python3
"""
Wave 8 Relationships Fix: Create missing relationships only
"""

import logging
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave8RelationshipsFix:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def execute(self):
        try:
            with self.driver.session() as session:
                # 5. HOSTS: Physical Server → Virtual Server (fixed - no Map property)
                logging.info("Creating HOSTS relationships...")
                query5 = """
                MATCH (physical:Server) WHERE physical.created_by = 'AEON_INTEGRATION_WAVE8'
                  AND physical.server_type = "PHYSICAL" AND physical.server_role = "Hypervisor Host"
                MATCH (virtual:Server) WHERE virtual.created_by = 'AEON_INTEGRATION_WAVE8'
                  AND virtual.server_type = "VIRTUAL" AND virtual.hypervisor IS NOT NULL
                WITH physical, virtual LIMIT 100
                CREATE (physical)-[r:HOSTS {
                  relationship_id: randomUUID(),
                  hypervisor_type: virtual.hypervisor,
                  allocated_vcpu: virtual.cpu_cores,
                  allocated_ram_gb: virtual.ram_gb,
                  allocated_storage_gb: virtual.storage_capacity_gb,
                  created_by: "AEON_INTEGRATION_WAVE8",
                  created_date: datetime()
                }]->(virtual)
                """
                result = session.run(query5)
                hosts_count = result.consume().counters.relationships_created
                logging.info(f"HOSTS relationships created: {hosts_count}")

                # 6. PHYSICALLY_LOCATED_IN: Server → DataCenterFacility
                logging.info("Creating PHYSICALLY_LOCATED_IN relationships...")
                query6 = """
                MATCH (s:Server) WHERE s.created_by = 'AEON_INTEGRATION_WAVE8' AND s.data_center IS NOT NULL
                MATCH (dcf:DataCenterFacility {facility_id: s.data_center})
                CREATE (s)-[r:PHYSICALLY_LOCATED_IN {
                  relationship_id: randomUUID(),
                  rack_id: s.rack_id,
                  rack_unit: s.rack_unit_position,
                  power_circuit: "PDU-A-CIRCUIT-" + toString(toInteger(rand() * 20) + 1),
                  created_by: "AEON_INTEGRATION_WAVE8",
                  created_date: datetime()
                }]->(dcf)
                """
                result = session.run(query6)
                located_count = result.consume().counters.relationships_created
                logging.info(f"PHYSICALLY_LOCATED_IN relationships created: {located_count}")

                # 7. HAS_VULNERABILITY: Server → CVE (sample mappings)
                logging.info("Creating HAS_VULNERABILITY relationships...")
                query7 = """
                MATCH (s:Server) WHERE s.created_by = 'AEON_INTEGRATION_WAVE8'
                MATCH (cve:CVE) WHERE cve.cvss_base_score >= 7.0
                WITH s, cve WHERE rand() < 0.05
                LIMIT 50
                CREATE (s)-[r:HAS_VULNERABILITY {
                  relationship_id: randomUUID(),
                  affected_component: "Sample Component",
                  exploitability: CASE WHEN cve.cvss_base_score >= 9.0 THEN "EASY" ELSE "MODERATE" END,
                  patch_available: true,
                  patch_status: "PENDING",
                  created_by: "AEON_INTEGRATION_WAVE8",
                  created_date: datetime()
                }]->(cve)
                """
                result = session.run(query7)
                vuln_count = result.consume().counters.relationships_created
                logging.info(f"HAS_VULNERABILITY relationships created: {vuln_count}")

                # 8. ENABLES_LATERAL_MOVEMENT: NetworkSegment → ICS_Technique
                logging.info("Creating ENABLES_LATERAL_MOVEMENT relationships...")
                query8 = """
                MATCH (ns_source:NetworkSegment) WHERE ns_source.created_by = 'AEON_INTEGRATION_WAVE8'
                  AND ns_source.trust_level = "SEMI_TRUSTED"
                MATCH (tech:ICS_Technique) WHERE tech.technique_id IN ["T0867", "T0886", "T0822"]
                WITH ns_source, tech LIMIT 30
                CREATE (ns_source)-[r:ENABLES_LATERAL_MOVEMENT {
                  relationship_id: randomUUID(),
                  technique_applicability: "APPLICABLE",
                  attack_complexity: "LOW",
                  detection_difficulty: "MODERATE",
                  created_by: "AEON_INTEGRATION_WAVE8",
                  created_date: datetime()
                }]->(tech)
                """
                result = session.run(query8)
                lateral_count = result.consume().counters.relationships_created
                logging.info(f"ENABLES_LATERAL_MOVEMENT relationships created: {lateral_count}")

                total_new = hosts_count + located_count + vuln_count + lateral_count
                logging.info(f"Wave 8 relationships fix completed: {total_new} new relationships created")

        except Exception as e:
            logging.error(f"Error creating relationships: {e}")
            raise
        finally:
            self.driver.close()

if __name__ == "__main__":
    fix = Wave8RelationshipsFix()
    fix.execute()
