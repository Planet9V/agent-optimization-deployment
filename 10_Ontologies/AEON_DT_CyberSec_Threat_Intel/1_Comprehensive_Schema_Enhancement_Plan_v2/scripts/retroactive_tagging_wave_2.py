#!/usr/bin/env python3
"""
Retroactive Tagging for Wave 2: Water Infrastructure
Apply created_by tags to untagged Wave 2 nodes based on node type patterns
Target: 15,000 nodes
"""
import logging
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave2RetroactiveTagger:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def tag_wave_2_nodes(self):
        """Tag all Wave 2 water infrastructure nodes"""
        logging.info("=" * 80)
        logging.info("WAVE 2 RETROACTIVE TAGGING - WATER INFRASTRUCTURE")
        logging.info("=" * 80)
        logging.info("")

        with self.driver.session() as session:
            tagged_counts = {}

            # 1. Tag WaterDevice nodes
            logging.info("Tagging WaterDevice nodes...")
            result = session.run("""
                MATCH (n:WaterDevice)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE2',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['WaterDevice'] = count
            logging.info(f"  ✅ Tagged {count} WaterDevice nodes")

            # 2. Tag WaterProperty nodes
            logging.info("Tagging WaterProperty nodes...")
            result = session.run("""
                MATCH (n:WaterProperty)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE2',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['WaterProperty'] = count
            logging.info(f"  ✅ Tagged {count} WaterProperty nodes")

            # 3. Tag TreatmentProcess nodes
            logging.info("Tagging TreatmentProcess nodes...")
            result = session.run("""
                MATCH (n:TreatmentProcess)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE2',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['TreatmentProcess'] = count
            logging.info(f"  ✅ Tagged {count} TreatmentProcess nodes")

            # 4. Tag SCADASystem nodes (water-specific)
            logging.info("Tagging SCADASystem nodes (water-specific)...")
            result = session.run("""
                MATCH (n:SCADASystem)
                WHERE n.created_by IS NULL
                  AND (n.scadaId STARTS WITH 'water:' OR n.systemName CONTAINS 'Water')
                SET n.created_by = 'AEON_INTEGRATION_WAVE2',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['SCADASystem'] = count
            logging.info(f"  ✅ Tagged {count} SCADASystem nodes")

            # 5. Tag WaterZone nodes
            logging.info("Tagging WaterZone nodes...")
            result = session.run("""
                MATCH (n:WaterZone)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE2',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['WaterZone'] = count
            logging.info(f"  ✅ Tagged {count} WaterZone nodes")

            # 6. Tag WaterAlert nodes
            logging.info("Tagging WaterAlert nodes...")
            result = session.run("""
                MATCH (n:WaterAlert)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE2',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['WaterAlert'] = count
            logging.info(f"  ✅ Tagged {count} WaterAlert nodes")

            # 7. Tag water-specific Measurement nodes
            logging.info("Tagging water-specific Measurement nodes...")
            result = session.run("""
                MATCH (n:Measurement)
                WHERE n.created_by IS NULL
                  AND n.measurementId STARTS WITH 'water:'
                SET n.created_by = 'AEON_INTEGRATION_WAVE2',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['Measurement'] = count
            logging.info(f"  ✅ Tagged {count} Measurement nodes")

            # Calculate total
            total_tagged = sum(tagged_counts.values())

            logging.info("")
            logging.info("=" * 80)
            logging.info("WAVE 2 TAGGING SUMMARY")
            logging.info("=" * 80)
            for node_type, count in tagged_counts.items():
                logging.info(f"  {node_type:30s}: {count:>6,} nodes")
            logging.info(f"  {'TOTAL':30s}: {total_tagged:>6,} nodes")
            logging.info("")

            # Verify total Wave 2 nodes
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE2'
                RETURN count(n) as total
            """)
            verified_total = result.single()['total']

            logging.info(f"Verification: {verified_total:,} total nodes now have Wave 2 tags")

            if verified_total == total_tagged:
                logging.info("✅ VALIDATION PASSED: All tagged nodes verified")
            else:
                logging.warning(f"⚠️  Discrepancy: Tagged {total_tagged}, verified {verified_total}")

            logging.info("")
            logging.info("=" * 80)

            return tagged_counts

if __name__ == "__main__":
    tagger = Wave2RetroactiveTagger()
    tagger.tag_wave_2_nodes()
    tagger.driver.close()
