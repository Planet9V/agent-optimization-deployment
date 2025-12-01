#!/usr/bin/env python3
"""
Check all waves (1-12) in the database
Identify which waves account for the 252,032 enhancement nodes
"""
import logging
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AllWavesChecker:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def check_all_waves(self):
        """Check nodes for all waves 1-12"""
        logging.info("=" * 80)
        logging.info("COMPREHENSIVE WAVE STATUS - ALL WAVES 1-12")
        logging.info("=" * 80)
        logging.info("")

        wave_data = {}
        total_enhancement_nodes = 0

        with self.driver.session() as session:
            for wave_num in range(1, 13):
                result = session.run(f"""
                    MATCH (n)
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE{wave_num}'
                    RETURN count(n) as total
                """)
                count = result.single()['total']
                wave_data[wave_num] = count
                total_enhancement_nodes += count

                if count > 0:
                    # Get top node types
                    result = session.run(f"""
                        MATCH (n)
                        WHERE n.created_by = 'AEON_INTEGRATION_WAVE{wave_num}'
                        WITH labels(n)[0] as label, count(*) as count
                        RETURN label, count
                        ORDER BY count DESC
                        LIMIT 5
                    """)

                    node_types = [(record['label'], record['count']) for record in result]
                    logging.info(f"✅ Wave {wave_num:2d}: {count:>7,} nodes")
                    for label, type_count in node_types:
                        logging.info(f"            - {label}: {type_count:,}")
                else:
                    logging.info(f"❌ Wave {wave_num:2d}: {count:>7,} nodes (NOT EXECUTED)")

                logging.info("")

            # Summary
            logging.info("=" * 80)
            logging.info("SUMMARY")
            logging.info("=" * 80)

            executed_waves = [w for w in range(1, 13) if wave_data[w] > 0]
            missing_waves = [w for w in range(1, 13) if wave_data[w] == 0]

            logging.info(f"Executed Waves: {executed_waves}")
            logging.info(f"Missing Waves: {missing_waves}")
            logging.info(f"")
            logging.info(f"Total Enhancement Nodes (tagged): {total_enhancement_nodes:,}")

            # Get actual total
            result = session.run("MATCH (n) RETURN count(n) as total")
            db_total = result.single()['total']

            result = session.run("MATCH (n:CVE) RETURN count(n) as total")
            cve_total = result.single()['total']

            actual_enhancement = db_total - cve_total

            logging.info(f"Database Total Nodes: {db_total:,}")
            logging.info(f"CVE Baseline: {cve_total:,}")
            logging.info(f"Actual Enhancement Nodes: {actual_enhancement:,}")
            logging.info(f"")

            if actual_enhancement > total_enhancement_nodes:
                diff = actual_enhancement - total_enhancement_nodes
                logging.info(f"⚠️  UNTAGGED NODES: {diff:,} nodes lack wave tags!")
                logging.info(f"   This suggests nodes were created without proper wave tags")
            elif actual_enhancement == total_enhancement_nodes:
                logging.info(f"✅ All enhancement nodes are properly tagged")

            logging.info("")
            logging.info("=" * 80)

if __name__ == "__main__":
    checker = AllWavesChecker()
    checker.check_all_waves()
    checker.driver.close()
