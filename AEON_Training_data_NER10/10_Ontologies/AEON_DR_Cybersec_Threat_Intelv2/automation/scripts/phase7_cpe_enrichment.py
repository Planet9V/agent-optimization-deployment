#!/usr/bin/env python3
"""
Phase 7: CPE Enrichment - Add CPE data to CVE nodes for Device-CVE matching
Fetches CPE configurations from NVD API and stores in Neo4j
"""

import sys
import os
import requests
import time
import yaml
import json
import logging
from datetime import datetime
from neo4j import GraphDatabase
from pathlib import Path

# Setup logging
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f'phase7_cpe_enrichment_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

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

API_KEY = config['nvd_api_key']
NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Neo4j connection
driver = GraphDatabase.driver(
    config['neo4j']['uri'],
    auth=(config['neo4j']['user'], config['neo4j']['password'])
)

def rate_limit(request_count, window_start):
    """Enforce 50 req/30s rate limit"""
    if request_count >= 50:
        elapsed = time.time() - window_start
        if elapsed < 30:
            time.sleep(30 - elapsed)
        return 0, time.time()
    return request_count, window_start

def extract_cpe_data(cve_data):
    """Extract CPE configurations from CVE JSON"""
    cpe_list = []

    configurations = cve_data.get('configurations', [])
    for config in configurations:
        for node in config.get('nodes', []):
            for cpe_match in node.get('cpeMatch', []):
                if cpe_match.get('vulnerable', True):
                    cpe_uri = cpe_match.get('criteria', '')
                    if cpe_uri:
                        cpe_list.append(cpe_uri)

    return cpe_list

def parse_cpe_uri(cpe_uri):
    """
    Parse CPE URI to extract vendor, product, version
    CPE format: cpe:2.3:a:vendor:product:version:*:*:*:*:*:*:*
    """
    try:
        parts = cpe_uri.split(':')
        if len(parts) >= 6:
            return {
                'vendor': parts[3].replace('_', ' ').title(),
                'product': parts[4].replace('_', ' ').title(),
                'version': parts[5] if parts[5] != '*' else None,
                'full_cpe': cpe_uri
            }
    except:
        pass
    return None

def update_cve_with_cpe(session, cve_id, cpe_list):
    """Update CVE node with CPE data"""
    if not cpe_list:
        return

    # Parse CPE data
    parsed_cpes = [parse_cpe_uri(cpe) for cpe in cpe_list]
    parsed_cpes = [c for c in parsed_cpes if c is not None]

    if not parsed_cpes:
        return

    # Extract unique vendors and products
    vendors = list(set(c['vendor'] for c in parsed_cpes))
    products = list(set(c['product'] for c in parsed_cpes))

    query = """
    MATCH (cve:CVE {id: $cve_id})
    SET cve.cpe_uris = $cpe_uris,
        cve.cpe_vendors = $vendors,
        cve.cpe_products = $products,
        cve.cpe_enriched = datetime()
    """

    session.run(query, {
        'cve_id': cve_id,
        'cpe_uris': cpe_list,
        'vendors': vendors,
        'products': products
    })

def main():
    """Main execution"""
    logger.info("="*80)
    logger.info("PHASE 7: CVE CPE ENRICHMENT")
    logger.info("="*80)

    # Get total CVE count
    with driver.session() as session:
        result = session.run("MATCH (cve:CVE) RETURN count(cve) AS total")
        total_cves = result.single()['total']
        logger.info(f"Total CVEs to enrich: {total_cves:,}")

        # Check how many already enriched
        result = session.run("MATCH (cve:CVE) WHERE cve.cpe_uris IS NOT NULL RETURN count(cve) AS enriched")
        already_enriched = result.single()['enriched']
        logger.info(f"Already enriched: {already_enriched:,}")

        if already_enriched == total_cves:
            logger.info("All CVEs already have CPE data!")
            return

    # Fetch CVEs in batches and enrich
    batch_size = 2000
    start_index = 0
    request_count = 0
    window_start = time.time()
    total_enriched = already_enriched

    logger.info(f"Starting CPE enrichment (batch size: {batch_size})...")

    while start_index < total_cves:
        # Rate limiting
        request_count, window_start = rate_limit(request_count, window_start)

        # Fetch batch from NVD API
        try:
            response = requests.get(
                NVD_API,
                params={'resultsPerPage': batch_size, 'startIndex': start_index},
                headers={'apiKey': API_KEY},
                timeout=30
            )

            if response.status_code != 200:
                logger.error(f"API error {response.status_code}: {response.text[:200]}")
                time.sleep(5)
                continue

            data = response.json()
            vulnerabilities = data.get('vulnerabilities', [])

            if not vulnerabilities:
                break

            # Process each CVE in batch
            with driver.session() as session:
                for vuln in vulnerabilities:
                    cve_data = vuln['cve']
                    cve_id = cve_data['id']

                    # Extract CPE data
                    cpe_list = extract_cpe_data(cve_data)

                    # Update Neo4j
                    if cpe_list:
                        update_cve_with_cpe(session, cve_id, cpe_list)
                        total_enriched += 1

            request_count += 1
            start_index += batch_size

            # Progress logging
            progress_pct = (start_index / total_cves) * 100
            logger.info(f"Progress: {start_index:,}/{total_cves:,} ({progress_pct:.1f}%) - Enriched: {total_enriched:,}")

            # Checkpoint every 10K CVEs
            if start_index % 10000 == 0:
                os.system(f'npx claude-flow@alpha hooks post-edit --file "phase7_cpe_enrichment.py" --memory-key "swarm/phase7/checkpoint_{start_index}" --data \'{{"progress": {start_index}, "enriched": {total_enriched}}}\'')

        except Exception as e:
            logger.error(f"Error processing batch at {start_index}: {e}")
            time.sleep(5)
            continue

    logger.info("="*80)
    logger.info("CPE ENRICHMENT COMPLETE")
    logger.info(f"Total CVEs enriched with CPE data: {total_enriched:,}")
    logger.info("="*80)

    driver.close()

if __name__ == "__main__":
    main()
