#!/usr/bin/env python3
"""
Phase 8: Device-CVE Matching - Create VULNERABLE_TO relationships
Matches Device firmware to CVE CPE data to regenerate relationships
"""

import sys
import os
import logging
from datetime import datetime
from neo4j import GraphDatabase
from pathlib import Path
import yaml

# Setup logging
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f'phase8_device_matching_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

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

def normalize_vendor_name(name):
    """Normalize vendor names for matching"""
    if not name:
        return ""

    # Common vendor name mappings
    mappings = {
        'siemens ag': 'siemens',
        'schneider electric': 'schneider_electric',
        'rockwell automation': 'rockwell',
        'abb': 'abb',
        'honeywell': 'honeywell'
    }

    normalized = name.lower().strip()
    return mappings.get(normalized, normalized.replace(' ', '_'))

def match_devices_to_cves(session):
    """
    Match Devices to CVEs based on manufacturer and product
    Creates VULNERABLE_TO relationships
    """

    # Get all devices
    device_query = """
    MATCH (d:Device)
    WHERE d.manufacturer IS NOT NULL AND d.model IS NOT NULL
    RETURN d.deviceId as device_id,
           d.manufacturer as manufacturer,
           d.model as model,
           d.firmwareVersion as firmware
    """

    devices = session.run(device_query).data()
    logger.info(f"Found {len(devices)} devices to process")

    total_relationships = 0
    devices_matched = 0

    for idx, device in enumerate(devices):
        device_id = device['device_id']
        manufacturer = normalize_vendor_name(device['manufacturer'])
        model = device['model']
        firmware = device['firmware']

        # Match CVEs with this manufacturer in CPE data
        match_query = """
        MATCH (d:Device {deviceId: $device_id})
        MATCH (cve:CVE)
        WHERE any(vendor IN cve.cpe_vendors WHERE toLower(vendor) CONTAINS $manufacturer)
           OR any(product IN cve.cpe_products WHERE toLower(product) CONTAINS toLower($model))
        WITH d, cve
        WHERE NOT EXISTS((d)-[:VULNERABLE_TO]->(cve))
        MERGE (d)-[r:VULNERABLE_TO]->(cve)
        SET r.matched_on = 'cpe_vendor_product',
            r.confidence = 'medium',
            r.discovered = datetime(),
            r.firmware_version = $firmware
        RETURN count(r) as relationships_created
        """

        result = session.run(match_query, {
            'device_id': device_id,
            'manufacturer': manufacturer,
            'model': model,
            'firmware': firmware
        })

        rels_created = result.single()['relationships_created']

        if rels_created > 0:
            total_relationships += rels_created
            devices_matched += 1
            logger.info(f"Device {device_id} ({manufacturer} {model}): {rels_created} CVE relationships created")

        # Progress update every 100 devices
        if (idx + 1) % 100 == 0:
            progress_pct = ((idx + 1) / len(devices)) * 100
            logger.info(f"Progress: {idx + 1}/{len(devices)} ({progress_pct:.1f}%) - Total relationships: {total_relationships:,}")

            # Checkpoint
            os.system(f'npx claude-flow@alpha hooks post-edit --file "phase8_device_matching.py" --memory-key "swarm/phase8/checkpoint_{idx+1}" --data \'{{"devices_processed": {idx+1}, "relationships": {total_relationships}}}\'')

    return total_relationships, devices_matched

def match_equipment_to_cves(session):
    """
    Match Equipment to CVEs based on vendor
    Creates VULNERABLE_TO relationships
    """

    equipment_query = """
    MATCH (e:Equipment)
    WHERE e.vendor IS NOT NULL
    RETURN id(e) as equipment_id, e.vendor as vendor, e.name as name
    """

    equipment = session.run(equipment_query).data()
    logger.info(f"Found {len(equipment)} equipment nodes to process")

    total_relationships = 0
    equipment_matched = 0

    for idx, equip in enumerate(equipment):
        equip_id = equip['equipment_id']
        vendor = normalize_vendor_name(equip['vendor'])
        name = equip['name']

        match_query = """
        MATCH (e:Equipment)
        WHERE id(e) = $equipment_id
        MATCH (cve:CVE)
        WHERE any(v IN cve.cpe_vendors WHERE toLower(v) CONTAINS $vendor)
        WITH e, cve
        WHERE NOT EXISTS((e)-[:VULNERABLE_TO]->(cve))
        MERGE (e)-[r:VULNERABLE_TO]->(cve)
        SET r.matched_on = 'cpe_vendor',
            r.confidence = 'low',
            r.discovered = datetime()
        RETURN count(r) as relationships_created
        """

        result = session.run(match_query, {
            'equipment_id': equip_id,
            'vendor': vendor
        })

        rels_created = result.single()['relationships_created']

        if rels_created > 0:
            total_relationships += rels_created
            equipment_matched += 1
            logger.info(f"Equipment {name} ({vendor}): {rels_created} CVE relationships created")

        if (idx + 1) % 10 == 0:
            progress_pct = ((idx + 1) / len(equipment)) * 100
            logger.info(f"Progress: {idx + 1}/{len(equipment)} ({progress_pct:.1f}%) - Total relationships: {total_relationships:,}")

    return total_relationships, equipment_matched

def main():
    """Main execution"""
    logger.info("="*80)
    logger.info("PHASE 8: DEVICE-CVE MATCHING & RELATIONSHIP CREATION")
    logger.info("="*80)

    with driver.session() as session:
        # Check if CVEs have CPE data
        result = session.run("""
            MATCH (cve:CVE)
            WHERE cve.cpe_uris IS NOT NULL
            RETURN count(cve) AS cves_with_cpe
        """)
        cves_with_cpe = result.single()['cves_with_cpe']
        logger.info(f"CVEs with CPE data: {cves_with_cpe:,}")

        if cves_with_cpe == 0:
            logger.error("No CVEs have CPE data! Run phase7_cpe_enrichment.py first")
            return

        # Match Devices to CVEs
        logger.info("\n" + "="*80)
        logger.info("MATCHING DEVICES TO CVEs")
        logger.info("="*80)
        device_rels, devices_matched = match_devices_to_cves(session)

        # Match Equipment to CVEs
        logger.info("\n" + "="*80)
        logger.info("MATCHING EQUIPMENT TO CVEs")
        logger.info("="*80)
        equipment_rels, equipment_matched = match_equipment_to_cves(session)

        # Final statistics
        logger.info("\n" + "="*80)
        logger.info("RELATIONSHIP CREATION COMPLETE")
        logger.info("="*80)
        logger.info(f"Devices matched: {devices_matched:,}")
        logger.info(f"Device→CVE relationships: {device_rels:,}")
        logger.info(f"Equipment matched: {equipment_matched:,}")
        logger.info(f"Equipment→CVE relationships: {equipment_rels:,}")
        logger.info(f"Total VULNERABLE_TO relationships: {device_rels + equipment_rels:,}")

        # Verify in database
        result = session.run("""
            MATCH ()-[r:VULNERABLE_TO]->()
            RETURN count(r) AS total
        """)
        total_in_db = result.single()['total']
        logger.info(f"Verified in database: {total_in_db:,} VULNERABLE_TO relationships")

    driver.close()

if __name__ == "__main__":
    main()
