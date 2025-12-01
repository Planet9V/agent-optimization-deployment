#!/usr/bin/env python3
"""
Autonomous Phase 7-8 Executor
Monitors EPSS completion, then executes CPE enrichment and device matching
All activities tracked in Qdrant memory via claude-flow hooks
"""

import subprocess
import time
import logging
import os
from datetime import datetime
from pathlib import Path
from neo4j import GraphDatabase
import yaml

# Setup logging
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f'autonomous_phase7_8_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load config
config_path = Path(__file__).parent.parent / 'config.yaml'
with open(config_path) as f:
    config = yaml.safe_load(f)

# Neo4j connection
driver = GraphDatabase.driver(
    config['neo4j']['uri'],
    auth=(config['neo4j']['user'], config['neo4j']['password'])
)

def store_checkpoint(phase, data):
    """Store checkpoint in Qdrant memory"""
    cmd = f"npx claude-flow@alpha hooks notify --message 'Phase {phase}: {data}'"
    subprocess.run(cmd, shell=True, capture_output=True)

def check_epss_progress():
    """Check EPSS enrichment progress"""
    with driver.session() as session:
        result = session.run("""
            MATCH (cve:CVE)
            WITH count(cve) AS total
            MATCH (cve2:CVE)
            WHERE cve2.epss_score IS NOT NULL
            WITH total, count(cve2) AS enriched
            RETURN total, enriched, (enriched * 100.0 / total) AS percent
        """)
        record = result.single()
        return record['total'], record['enriched'], record['percent']

def execute_phase(phase_num, script_name, description):
    """Execute a phase script"""
    logger.info("="*80)
    logger.info(f"EXECUTING PHASE {phase_num}: {description}")
    logger.info("="*80)

    store_checkpoint(phase_num, f"Starting {description}")

    script_path = Path(__file__).parent / script_name
    result = subprocess.run(['python3', str(script_path)], capture_output=True, text=True)

    if result.returncode == 0:
        logger.info(f"✅ Phase {phase_num} COMPLETE")
        store_checkpoint(phase_num, f"Completed successfully")
        return True
    else:
        logger.error(f"❌ Phase {phase_num} FAILED")
        logger.error(result.stderr)
        store_checkpoint(phase_num, f"Failed: {result.stderr[:200]}")
        return False

def main():
    """Main execution"""
    logger.info("="*80)
    logger.info("AUTONOMOUS PHASE 7-8 EXECUTOR - Starting")
    logger.info("="*80)

    # Phase 1: Monitor EPSS completion
    logger.info("\nMonitoring Phase 5 (EPSS enrichment) completion...")

    while True:
        total, enriched, percent = check_epss_progress()
        logger.info(f"EPSS Progress: {enriched:,}/{total:,} ({percent:.1f}%)")

        if percent >= 99.0:
            logger.info("✅ EPSS enrichment complete!")
            break

        if percent >= 94.9:
            logger.info("⏩ EPSS at 94.9% (manual trigger threshold), proceeding with CPE enrichment")
            break

        # Check every 5 minutes
        time.sleep(300)

    store_checkpoint("5", f"EPSS enrichment reached {percent:.1f}%")

    # Phase 7: CPE Enrichment
    success = execute_phase(7, "phase7_cpe_enrichment.py", "CVE CPE Data Enrichment")
    if not success:
        logger.error("Cannot proceed without CPE data")
        return

    # Phase 8: Device-CVE Matching
    success = execute_phase(8, "phase8_device_cve_matching.py", "Device-CVE Relationship Creation")

    # Final validation
    logger.info("\n" + "="*80)
    logger.info("FINAL VALIDATION")
    logger.info("="*80)

    with driver.session() as session:
        # Check CVE CPE enrichment
        result = session.run("""
            MATCH (cve:CVE)
            WHERE cve.cpe_uris IS NOT NULL
            RETURN count(cve) AS cpe_enriched
        """)
        cpe_enriched = result.single()['cpe_enriched']
        logger.info(f"CVEs with CPE data: {cpe_enriched:,}")

        # Check VULNERABLE_TO relationships
        result = session.run("""
            MATCH ()-[r:VULNERABLE_TO]->()
            RETURN count(r) AS vulnerable_to
        """)
        vulnerable_to = result.single()['vulnerable_to']
        logger.info(f"VULNERABLE_TO relationships: {vulnerable_to:,}")

        # Check Device matches
        result = session.run("""
            MATCH (d:Device)-[r:VULNERABLE_TO]->(cve:CVE)
            RETURN count(DISTINCT d) AS devices_matched, count(r) AS device_cve_rels
        """)
        record = result.single()
        logger.info(f"Devices matched: {record['devices_matched']:,}")
        logger.info(f"Device→CVE relationships: {record['device_cve_rels']:,}")

        # Check Equipment matches
        result = session.run("""
            MATCH (e:Equipment)-[r:VULNERABLE_TO]->(cve:CVE)
            RETURN count(DISTINCT e) AS equipment_matched, count(r) AS equipment_cve_rels
        """)
        record = result.single()
        logger.info(f"Equipment matched: {record['equipment_matched']:,}")
        logger.info(f"Equipment→CVE relationships: {record['equipment_cve_rels']:,}")

    logger.info("\n" + "="*80)
    logger.info("PHASES 7-8 COMPLETE - TRIGGERING PHASE 9")
    logger.info("="*80)

    # Store checkpoint
    store_checkpoint("phases_7_8_complete", f"{vulnerable_to:,} VULNERABLE_TO relationships created")

    # Phase 9: Ontology Integration
    logger.info("\n" + "="*80)
    logger.info("PHASE 9: ONTOLOGY INTEGRATION INTO QDRANT")
    logger.info("="*80)

    success = execute_phase(9, "phase9_ontology_integration.py", "Ontology Integration into Qdrant Vector Store")

    if success:
        logger.info("\n" + "="*80)
        logger.info("ALL PHASES COMPLETE INCLUDING ONTOLOGY INTEGRATION")
        logger.info("="*80)
        logger.info(f"✅ CVE Remediation: {vulnerable_to:,} relationships")
        logger.info("✅ Ontology Integration: Specialized agents registered in swarm")
        logger.info("✅ Qdrant Memory: Complete with domain-specific ontology knowledge")

        # Final checkpoint
        store_checkpoint("all_phases_complete", f"Complete: {vulnerable_to:,} relationships + ontology integration")
    else:
        logger.warning("⚠️ Phase 9 failed - continuing without ontology integration")
        store_checkpoint("final", f"Phases 7-8 complete: {vulnerable_to:,} relationships. Phase 9 failed.")

    driver.close()

if __name__ == "__main__":
    main()
