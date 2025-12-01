#!/usr/bin/env python3
"""
Retroactive Tagging for Wave 3: Energy Grid
Apply created_by tags to untagged Wave 3 nodes based on node type patterns
Target: 35,475 nodes
"""
import logging
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave3RetroactiveTagger:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def tag_wave_3_nodes(self):
        """Tag all Wave 3 energy grid nodes"""
        logging.info("=" * 80)
        logging.info("WAVE 3 RETROACTIVE TAGGING - ENERGY GRID")
        logging.info("=" * 80)
        logging.info("")

        with self.driver.session() as session:
            tagged_counts = {}

            # 1. Tag EnergyDevice nodes
            logging.info("Tagging EnergyDevice nodes...")
            result = session.run("""
                MATCH (n:EnergyDevice)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE3',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['EnergyDevice'] = count
            logging.info(f"  ✅ Tagged {count} EnergyDevice nodes")

            # 2. Tag EnergyProperty nodes
            logging.info("Tagging EnergyProperty nodes...")
            result = session.run("""
                MATCH (n:EnergyProperty)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE3',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['EnergyProperty'] = count
            logging.info(f"  ✅ Tagged {count} EnergyProperty nodes")

            # 3. Tag Substation nodes
            logging.info("Tagging Substation nodes...")
            result = session.run("""
                MATCH (n:Substation)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE3',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['Substation'] = count
            logging.info(f"  ✅ Tagged {count} Substation nodes")

            # 4. Tag TransmissionLine nodes
            logging.info("Tagging TransmissionLine nodes...")
            result = session.run("""
                MATCH (n:TransmissionLine)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE3',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['TransmissionLine'] = count
            logging.info(f"  ✅ Tagged {count} TransmissionLine nodes")

            # 5. Tag EnergyManagementSystem nodes
            logging.info("Tagging EnergyManagementSystem nodes...")
            result = session.run("""
                MATCH (n:EnergyManagementSystem)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE3',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['EnergyManagementSystem'] = count
            logging.info(f"  ✅ Tagged {count} EnergyManagementSystem nodes")

            # 6. Tag DistributedEnergyResource nodes
            logging.info("Tagging DistributedEnergyResource nodes...")
            result = session.run("""
                MATCH (n:DistributedEnergyResource)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE3',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['DistributedEnergyResource'] = count
            logging.info(f"  ✅ Tagged {count} DistributedEnergyResource nodes")

            # 7. Tag NERCCIPStandard nodes
            logging.info("Tagging NERCCIPStandard nodes...")
            result = session.run("""
                MATCH (n:NERCCIPStandard)
                WHERE n.created_by IS NULL
                SET n.created_by = 'AEON_INTEGRATION_WAVE3',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['NERCCIPStandard'] = count
            logging.info(f"  ✅ Tagged {count} NERCCIPStandard nodes")

            # 8. Tag energy-specific Measurement nodes
            logging.info("Tagging energy-specific Measurement nodes...")
            result = session.run("""
                MATCH (n:Measurement)
                WHERE n.created_by IS NULL
                  AND n.measurementId STARTS WITH 'energy:'
                SET n.created_by = 'AEON_INTEGRATION_WAVE3',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['Measurement'] = count
            logging.info(f"  ✅ Tagged {count} Measurement nodes")

            # 9. Tag energy-related Device nodes (extended from Wave 1)
            logging.info("Tagging energy-related Device nodes...")
            result = session.run("""
                MATCH (n:Device)
                WHERE n.created_by IS NULL
                  AND NOT n:WaterDevice
                  AND (n.deviceId STARTS WITH 'energy:'
                       OR n.deploymentLocation CONTAINS 'Substation'
                       OR n.deviceCategory IN ['Generator', 'Transformer', 'CircuitBreaker'])
                SET n.created_by = 'AEON_INTEGRATION_WAVE3',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['Device'] = count
            logging.info(f"  ✅ Tagged {count} Device nodes")

            # 10. Tag energy-related Property nodes (extended from Wave 1)
            logging.info("Tagging energy-related Property nodes...")
            result = session.run("""
                MATCH (n:Property)
                WHERE n.created_by IS NULL
                  AND NOT n:WaterProperty
                  AND (n.propertyId STARTS WITH 'energy:'
                       OR n.propertyType IN ['Voltage', 'Current', 'Power', 'Frequency'])
                SET n.created_by = 'AEON_INTEGRATION_WAVE3',
                    n.tagged_date = datetime(),
                    n.tagging_method = 'retroactive',
                    n.validation_status = 'VALIDATED'
                RETURN count(n) as count
            """)
            count = result.single()['count']
            tagged_counts['Property'] = count
            logging.info(f"  ✅ Tagged {count} Property nodes")

            # Calculate total
            total_tagged = sum(tagged_counts.values())

            logging.info("")
            logging.info("=" * 80)
            logging.info("WAVE 3 TAGGING SUMMARY")
            logging.info("=" * 80)
            for node_type, count in sorted(tagged_counts.items(), key=lambda x: x[1], reverse=True):
                logging.info(f"  {node_type:35s}: {count:>6,} nodes")
            logging.info(f"  {'TOTAL':35s}: {total_tagged:>6,} nodes")
            logging.info("")

            # Verify total Wave 3 nodes
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE3'
                RETURN count(n) as total
            """)
            verified_total = result.single()['total']

            logging.info(f"Verification: {verified_total:,} total nodes now have Wave 3 tags")

            if verified_total == total_tagged:
                logging.info("✅ VALIDATION PASSED: All tagged nodes verified")
            else:
                logging.warning(f"⚠️  Discrepancy: Tagged {total_tagged}, verified {verified_total}")

            logging.info("")
            logging.info("=" * 80)

            return tagged_counts

if __name__ == "__main__":
    tagger = Wave3RetroactiveTagger()
    tagger.tag_wave_3_nodes()
    tagger.driver.close()
