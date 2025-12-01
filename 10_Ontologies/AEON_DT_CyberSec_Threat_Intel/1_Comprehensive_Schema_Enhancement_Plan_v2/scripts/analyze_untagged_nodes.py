#!/usr/bin/env python3
"""
Analyze the 93,497 untagged enhancement nodes
Identify their types and potential wave associations
"""
import logging
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UntaggedAnalyzer:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def analyze_untagged(self):
        """Find and analyze nodes without wave tags"""
        logging.info("=" * 80)
        logging.info("UNTAGGED NODE ANALYSIS")
        logging.info("=" * 80)
        logging.info("")

        with self.driver.session() as session:
            # Find nodes without created_by property (excluding CVE)
            result = session.run("""
                MATCH (n)
                WHERE NOT n:CVE
                  AND n.created_by IS NULL
                WITH labels(n)[0] as label, count(*) as count
                RETURN label, count
                ORDER BY count DESC
                LIMIT 20
            """)

            logging.info("Top 20 Node Types WITHOUT wave tags:")
            logging.info("")

            total_untagged = 0
            node_types = []

            for record in result:
                label = record['label']
                count = record['count']
                total_untagged += count
                node_types.append((label, count))
                logging.info(f"  {label:40s}: {count:>8,}")

            logging.info("")
            logging.info(f"Total Untagged Nodes (top 20 types): {total_untagged:,}")
            logging.info("")

            # Check for nodes with other created_by tags
            result = session.run("""
                MATCH (n)
                WHERE n.created_by IS NOT NULL
                  AND NOT n.created_by STARTS WITH 'AEON_INTEGRATION_WAVE'
                WITH n.created_by as tag, count(*) as count
                RETURN tag, count
                ORDER BY count DESC
            """)

            other_tags = list(result)
            if other_tags:
                logging.info("Nodes with non-wave created_by tags:")
                logging.info("")
                for record in other_tags:
                    logging.info(f"  {record['tag']:40s}: {record['count']:>8,}")
                logging.info("")

            # Analyze potential Wave 2/3/4 nodes by type patterns
            logging.info("=" * 80)
            logging.info("POTENTIAL WAVE 2/3/4 NODE IDENTIFICATION")
            logging.info("=" * 80)
            logging.info("")

            # Wave 2 patterns: Threat Intelligence (ATT&CK, threat actors, malware)
            wave2_patterns = [
                'ThreatActor', 'MalwareFamily', 'Campaign', 'IntrusionSet',
                'AttackPattern', 'Technique', 'Tactic', 'Procedure'
            ]

            # Wave 3 patterns: IT Infrastructure (networks, servers, OS, protocols)
            wave3_patterns = [
                'Network', 'Router', 'Switch', 'Firewall', 'LoadBalancer',
                'OperatingSystem', 'Protocol', 'Port', 'IPAddress'
            ]

            # Wave 4 patterns: Critical Infrastructure Sectors 1-4
            wave4_patterns = [
                'PowerGrid', 'EnergyFacility', 'WaterTreatment', 'Hospital',
                'HealthcareFacility', 'Bank', 'FinancialInstitution'
            ]

            for wave_num, patterns in [(2, wave2_patterns), (3, wave3_patterns), (4, wave4_patterns)]:
                logging.info(f"Wave {wave_num} Pattern Analysis:")
                found = False
                for pattern in patterns:
                    result = session.run(f"""
                        MATCH (n)
                        WHERE labels(n)[0] = '{pattern}'
                          AND n.created_by IS NULL
                        RETURN count(n) as count
                    """)
                    count = result.single()['count']
                    if count > 0:
                        logging.info(f"  Found {pattern}: {count:,} nodes")
                        found = True

                if not found:
                    logging.info(f"  No matching patterns found")
                logging.info("")

            logging.info("=" * 80)

if __name__ == "__main__":
    analyzer = UntaggedAnalyzer()
    analyzer.analyze_untagged()
    analyzer.driver.close()
