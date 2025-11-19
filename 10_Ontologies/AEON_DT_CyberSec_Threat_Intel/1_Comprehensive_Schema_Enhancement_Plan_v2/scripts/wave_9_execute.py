#!/usr/bin/env python3
"""
Wave 9 Master Executor: Coordinates all Wave 9 scripts and validates 5,000 nodes
"""

import logging
import subprocess
import sys
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave9MasterExecutor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def run_script(self, script_name: str) -> bool:
        """Execute a Wave 9 sub-script and return success status"""
        logging.info(f"🚀 Starting {script_name}...")
        try:
            result = subprocess.run(
                [sys.executable, f"/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/1_Comprehensive_Schema_Enhancement_Plan_v2/scripts/{script_name}"],
                check=True,
                capture_output=True,
                text=True
            )
            logging.info(f"✅ {script_name} completed successfully")
            logging.info(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ {script_name} failed: {e}")
            logging.error(e.stderr)
            return False

    def validate_total_nodes(self) -> dict:
        """Validate that exactly 5,000 Wave 9 nodes were created"""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (n) WHERE n.created_by = 'AEON_INTEGRATION_WAVE9'
            RETURN labels(n)[0] as nodeType, count(*) as count
            ORDER BY nodeType
            """)

            node_counts = {}
            total = 0
            for record in result:
                node_type = record['nodeType']
                count = record['count']
                node_counts[node_type] = count
                total += count
                logging.info(f"  {node_type}: {count} nodes")

            logging.info(f"📊 Total Wave 9 nodes: {total}")
            assert total == 5000, f"Expected 5000 nodes, got {total}"

            return {"total": total, "breakdown": node_counts}

    def validate_cve_preservation(self) -> int:
        """Validate that all 267,487 CVE nodes are intact"""
        with self.driver.session() as session:
            result = session.run("MATCH (c:CVE) RETURN count(c) as cve_count")
            cve_count = result.single()['cve_count']
            logging.info(f"🛡️  CVE nodes: {cve_count}")
            assert cve_count == 267487, f"CVE preservation FAILED! Expected 267487, got {cve_count}"
            logging.info("✅ CVE preservation verified: 267,487 nodes intact")
            return cve_count

    def validate_uniqueness(self):
        """Validate that all Wave 9 nodes have unique node_id values"""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (n) WHERE n.created_by = 'AEON_INTEGRATION_WAVE9'
            WITH n.node_id as id, count(*) as occurrences
            WHERE occurrences > 1
            RETURN id, occurrences
            """)

            duplicates = list(result)
            if duplicates:
                logging.error(f"❌ Duplicate node_id values found: {duplicates}")
                raise AssertionError("Uniqueness validation failed")

            logging.info("✅ All node_id values are unique")

    def execute(self):
        try:
            start_time = datetime.utcnow()
            logging.info(f"🎯 Wave 9 Master Execution Started: {start_time.isoformat()}")

            # Phase 1: Hardware Assets (1,500 nodes)
            if not self.run_script("wave_9_hardware.py"):
                raise Exception("Hardware script failed")

            # Phase 2: Software Assets (1,500 nodes)
            if not self.run_script("wave_9_software.py"):
                raise Exception("Software script failed")

            # Phase 3: Cloud Infrastructure (1,000 nodes)
            if not self.run_script("wave_9_cloud.py"):
                raise Exception("Cloud script failed")

            # Phase 4: Virtualization (1,000 nodes)
            if not self.run_script("wave_9_virtualization.py"):
                raise Exception("Virtualization script failed")

            # Validation Phase
            logging.info("=" * 80)
            logging.info("🔍 COMPREHENSIVE VALIDATION PHASE")
            logging.info("=" * 80)

            node_stats = self.validate_total_nodes()
            cve_count = self.validate_cve_preservation()
            self.validate_uniqueness()

            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()

            logging.info("=" * 80)
            logging.info("🎉 WAVE 9 EXECUTION COMPLETE")
            logging.info("=" * 80)
            logging.info(f"Total Nodes Created: {node_stats['total']}")
            logging.info(f"CVE Nodes Preserved: {cve_count}")
            logging.info(f"Execution Time: {duration:.2f} seconds")
            logging.info(f"Node Creation Rate: {node_stats['total'] / duration:.2f} nodes/second")
            logging.info("✅ All validations passed")
            logging.info("=" * 80)

        except Exception as e:
            logging.error(f"💥 Wave 9 execution failed: {e}")
            raise
        finally:
            self.driver.close()

if __name__ == "__main__":
    executor = Wave9MasterExecutor()
    executor.execute()
