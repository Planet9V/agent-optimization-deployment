#!/usr/bin/env python3
"""
Validate Waves 2-8 Database Status
Check if nodes were actually created for each wave
"""
import logging
from neo4j import GraphDatabase
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WaveValidator:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.expected_cve_count = 267487

    def check_wave_nodes(self, wave_num):
        """Check if nodes exist for a specific wave"""
        with self.driver.session() as session:
            # Get total count
            result = session.run(f"""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE{wave_num}'
                RETURN count(n) as total
            """)
            total = result.single()['total']

            if total == 0:
                return {
                    'wave': wave_num,
                    'status': 'NOT_EXECUTED',
                    'total_nodes': 0,
                    'node_types': []
                }

            # Get node type breakdown
            result = session.run(f"""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE{wave_num}'
                WITH labels(n)[0] as label, count(*) as count
                RETURN label, count
                ORDER BY count DESC
            """)

            node_types = []
            for record in result:
                node_types.append({
                    'type': record['label'],
                    'count': record['count']
                })

            return {
                'wave': wave_num,
                'status': 'EXECUTED',
                'total_nodes': total,
                'node_types': node_types
            }

    def check_total_nodes(self):
        """Get total node count in database"""
        with self.driver.session() as session:
            result = session.run("MATCH (n) RETURN count(n) as total")
            return result.single()['total']

    def check_cve_preservation(self):
        """Verify CVE baseline is intact"""
        with self.driver.session() as session:
            result = session.run("MATCH (n:CVE) RETURN count(n) as total")
            return result.single()['total']

    def validate_all_waves(self):
        """Comprehensive validation of Waves 2-8"""
        logging.info("=" * 80)
        logging.info("WAVE 2-8 DATABASE VALIDATION")
        logging.info("=" * 80)
        logging.info(f"Started: {datetime.utcnow().isoformat()}")
        logging.info("")

        # Check CVE preservation
        cve_count = self.check_cve_preservation()
        logging.info(f"CVE Baseline: {cve_count:,} nodes (expected {self.expected_cve_count:,})")
        if cve_count != self.expected_cve_count:
            logging.warning(f"⚠️  CVE count mismatch!")
        else:
            logging.info("✅ CVE baseline preserved")
        logging.info("")

        # Check total nodes
        total_nodes = self.check_total_nodes()
        logging.info(f"Total Graph Nodes: {total_nodes:,}")
        logging.info("")

        # Validate each wave
        wave_results = {}
        total_wave_nodes = 0

        for wave_num in range(2, 9):
            logging.info(f"Checking Wave {wave_num}...")
            result = self.check_wave_nodes(wave_num)
            wave_results[wave_num] = result

            if result['status'] == 'EXECUTED':
                logging.info(f"  ✅ Wave {wave_num}: {result['total_nodes']:,} nodes created")
                total_wave_nodes += result['total_nodes']

                # Show top node types
                for node_type in result['node_types'][:5]:
                    logging.info(f"     - {node_type['type']}: {node_type['count']:,}")
                if len(result['node_types']) > 5:
                    logging.info(f"     ... and {len(result['node_types']) - 5} more types")
            else:
                logging.info(f"  ❌ Wave {wave_num}: NO NODES FOUND - Not executed or failed")
            logging.info("")

        # Summary
        logging.info("=" * 80)
        logging.info("VALIDATION SUMMARY")
        logging.info("=" * 80)

        executed_waves = [w for w in range(2, 9) if wave_results[w]['status'] == 'EXECUTED']
        missing_waves = [w for w in range(2, 9) if wave_results[w]['status'] == 'NOT_EXECUTED']

        logging.info(f"Waves 2-8 Status:")
        logging.info(f"  ✅ Executed: {len(executed_waves)} waves - {executed_waves}")
        logging.info(f"  ❌ Missing: {len(missing_waves)} waves - {missing_waves}")
        logging.info(f"  📊 Total Nodes from Waves 2-8: {total_wave_nodes:,}")
        logging.info("")

        # Expected vs Actual
        expected_from_waves_2_8 = total_nodes - cve_count
        logging.info(f"Database Analysis:")
        logging.info(f"  Total Nodes: {total_nodes:,}")
        logging.info(f"  CVE Baseline: {cve_count:,}")
        logging.info(f"  Enhancement Nodes: {expected_from_waves_2_8:,}")
        logging.info(f"  Waves 2-8 Tagged Nodes: {total_wave_nodes:,}")

        if total_wave_nodes > 0:
            logging.info("")
            logging.info(f"⚠️  Note: If Waves 2-8 tagged nodes < Enhancement nodes,")
            logging.info(f"    other waves (1, 9-12) account for the difference")

        logging.info("")
        logging.info("=" * 80)

        return wave_results

if __name__ == "__main__":
    validator = WaveValidator()
    validator.validate_all_waves()
    validator.driver.close()
