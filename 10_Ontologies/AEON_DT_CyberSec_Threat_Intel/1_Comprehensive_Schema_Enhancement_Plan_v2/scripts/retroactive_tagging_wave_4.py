#!/usr/bin/env python3
"""
Retroactive Tagging for Wave 4: ICS Security & Threat Intelligence
Apply created_by tags to untagged Wave 4 nodes based on node type patterns
Target: ~11,000 nodes
"""
import logging
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave4RetroactiveTagger:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def tag_wave_4_nodes(self):
        """Tag all Wave 4 ICS security and threat intelligence nodes"""
        logging.info("=" * 80)
        logging.info("WAVE 4 RETROACTIVE TAGGING - ICS SECURITY & THREAT INTELLIGENCE")
        logging.info("=" * 80)
        logging.info("")

        with self.driver.session() as session:
            tagged_counts = {}

            # 1. Tag ThreatActor nodes
            logging.info("Tagging ThreatActor nodes...")
            result = session.run("""
                MATCH (n:ThreatActor)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE4',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['ThreatActor'] = count
            logging.info(f"  ✅ Tagged {count} ThreatActor nodes")

            # 2. Tag AttackPattern nodes
            logging.info("Tagging AttackPattern nodes...")
            result = session.run("""
                MATCH (n:AttackPattern)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE4',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['AttackPattern'] = count
            logging.info(f"  ✅ Tagged {count} AttackPattern nodes")

            # 3. Tag Malware nodes
            logging.info("Tagging Malware nodes...")
            result = session.run("""
                MATCH (n:Malware)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE4',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['Malware'] = count
            logging.info(f"  ✅ Tagged {count} Malware nodes")

            # 4. Tag Campaign nodes
            logging.info("Tagging Campaign nodes...")
            result = session.run("""
                MATCH (n:Campaign)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE4',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['Campaign'] = count
            logging.info(f"  ✅ Tagged {count} Campaign nodes")

            # 5. Tag TTP nodes
            logging.info("Tagging TTP nodes...")
            result = session.run("""
                MATCH (n:TTP)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE4',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['TTP'] = count
            logging.info(f"  ✅ Tagged {count} TTP nodes")

            # 6. Tag CAPEC nodes
            logging.info("Tagging CAPEC nodes...")
            result = session.run("""
                MATCH (n:CAPEC)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE4',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['CAPEC'] = count
            logging.info(f"  ✅ Tagged {count} CAPEC nodes")

            # 7. Tag CWE nodes
            logging.info("Tagging CWE nodes...")
            result = session.run("""
                MATCH (n:CWE)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE4',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['CWE'] = count
            logging.info(f"  ✅ Tagged {count} CWE nodes")

            # 8. Tag DetectionSignature nodes
            logging.info("Tagging DetectionSignature nodes...")
            result = session.run("""
                MATCH (n:DetectionSignature)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE4',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['DetectionSignature'] = count
            logging.info(f"  ✅ Tagged {count} DetectionSignature nodes")

            # 9. Tag Indicator nodes
            logging.info("Tagging Indicator nodes...")
            result = session.run("""
                MATCH (n:Indicator)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE4',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['Indicator'] = count
            logging.info(f"  ✅ Tagged {count} Indicator nodes")

            # 10. Tag AttackTechnique nodes
            logging.info("Tagging AttackTechnique nodes...")
            result = session.run("""
                MATCH (n:AttackTechnique)
                WHERE n.created_by IS NULL
                  AND NOT n:ICS_Technique
                SET n.created_by = 'AEON_INTEGRATION_WAVE4',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['AttackTechnique'] = count
            logging.info(f"  ✅ Tagged {count} AttackTechnique nodes")

            # Calculate total
            total_tagged = sum(tagged_counts.values())

            logging.info("")
            logging.info("=" * 80)
            logging.info("WAVE 4 TAGGING SUMMARY")
            logging.info("=" * 80)
            for node_type, count in sorted(tagged_counts.items(), key=lambda x: x[1], reverse=True):
                logging.info(f"  {node_type:35s}: {count:>6,} nodes")
            logging.info(f"  {'TOTAL':35s}: {total_tagged:>6,} nodes")
            logging.info("")

            # Verify total Wave 4 nodes
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE4'
                RETURN count(n) as total
            """)
            verified_total = result.single()['total']

            logging.info(f"Verification: {verified_total:,} total nodes now have Wave 4 tags")

            if verified_total == total_tagged:
                logging.info("✅ VALIDATION PASSED: All tagged nodes verified")
            else:
                logging.warning(f"⚠️  Discrepancy: Tagged {total_tagged}, verified {verified_total}")

            logging.info("")
            logging.info("=" * 80)

            return tagged_counts

if __name__ == "__main__":
    tagger = Wave4RetroactiveTagger()
    tagger.tag_wave_4_nodes()
    tagger.driver.close()
