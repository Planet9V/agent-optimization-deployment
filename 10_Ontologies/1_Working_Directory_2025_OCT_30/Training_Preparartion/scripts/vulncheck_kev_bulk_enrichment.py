#!/usr/bin/env python3
"""
VULNCHECK KEV BULK ENRICHMENT
Fetch ALL KEV data from VulnCheck API and enrich Neo4j CVEs

Strategy:
1. Fetch ALL 4,321 KEV CVEs from VulnCheck API (bulk paginated)
2. Extract CWE mappings from each KEV CVE
3. Match against Neo4j CVEs and create relationships
4. Flag CVEs as Known Exploited (is_kev=True)

Author: AEON Protocol
Date: 2025-11-07
Version: 1.0.0
"""

import requests
import time
import logging
import sys
import json
from typing import Dict, List, Set
from neo4j import GraphDatabase
from collections import defaultdict
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vulncheck_kev_bulk.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# API Configuration
VULNCHECK_API_KEY = "vulncheck_d50b2321719330fa9fd39437b61bab52d729bfa093b8f15fe97b4db4349f584c"
VULNCHECK_KEV_URL = "https://api.vulncheck.com/v3/index/vulncheck-kev"

# Neo4j Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"


class VulnCheckKEVBulkEnrichment:
    """Bulk fetch VulnCheck KEV data and enrich Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        """Initialize connections."""
        self.driver = GraphDatabase.driver(
            uri,
            auth=(user, password),
            max_connection_pool_size=10
        )
        self.session_http = requests.Session()
        self.kev_data = {}  # CVE ID -> KEV enrichment data
        self.cwe_cache = {}  # CWE existence cache
        self.stats = {
            'total_kev_cves': 0,
            'matched_in_db': 0,
            'kev_flagged': 0,
            'cwe_relationships': 0,
            'missing_cwes': defaultdict(int),
            'cache_hits': 0
        }
        logger.info(f"Connected to Neo4j at {uri}")

    def close(self):
        """Close connections."""
        self.driver.close()
        self.session_http.close()

    def load_cwe_cache(self):
        """Pre-load all CWE IDs into cache."""
        logger.info("Loading CWE cache...")
        query = "MATCH (w:CWE) RETURN toLower(w.id) AS cwe_id"

        try:
            with self.driver.session() as session:
                result = session.run(query)
                for record in result:
                    self.cwe_cache[record['cwe_id']] = True
            logger.info(f"✅ CWE cache loaded: {len(self.cwe_cache):,} CWEs")
        except Exception as e:
            logger.error(f"Failed to load CWE cache: {e}")

    def fetch_all_kev_data(self):
        """Fetch ALL KEV CVEs from VulnCheck API using pagination."""
        logger.info("Fetching ALL KEV data from VulnCheck API...")

        url = VULNCHECK_KEV_URL
        headers = {"Authorization": f"Bearer {VULNCHECK_API_KEY}"}

        page = 1
        total_fetched = 0

        while True:
            try:
                logger.info(f"Fetching page {page}...")
                response = self.session_http.get(
                    url,
                    headers=headers,
                    params={'page': page, 'size': 1000},
                    timeout=60
                )
                response.raise_for_status()
                data = response.json()

                if 'data' not in data or len(data['data']) == 0:
                    logger.info("No more data, pagination complete")
                    break

                # Process each KEV CVE
                for vuln in data['data']:
                    cve_list = vuln.get('cve', [])
                    if not isinstance(cve_list, list):
                        cve_list = [cve_list]

                    for cve_id in cve_list:
                        if not cve_id:
                            continue

                        # Extract CWE IDs
                        cwe_ids = []
                        cwes_field = vuln.get('cwes', [])
                        if isinstance(cwes_field, list):
                            for cwe in cwes_field:
                                if isinstance(cwe, str):
                                    cwe_clean = cwe.lower()
                                    if cwe_clean.startswith('cwe-'):
                                        cwe_ids.append(cwe_clean)
                                    elif cwe.isdigit():
                                        cwe_ids.append(f"cwe-{cwe}")

                        # Determine KEV status
                        is_kev = True  # All entries in this index are KEV
                        cisa_date = vuln.get('cisa_date_added') or vuln.get('date_added')

                        self.kev_data[cve_id] = {
                            'cve_id': cve_id,
                            'cwe_ids': cwe_ids,
                            'is_kev': is_kev,
                            'cisa_date_added': cisa_date,
                            'ransomware_use': vuln.get('knownRansomwareCampaignUse'),
                            'vulnerability_name': vuln.get('vulnerabilityName'),
                            'description': vuln.get('shortDescription'),
                            'vendor_project': vuln.get('vendorProject'),
                            'product': vuln.get('product')
                        }
                        total_fetched += 1

                # Check if there are more pages
                meta = data.get('_meta', {})
                max_pages = meta.get('max_pages', page)

                logger.info(f"Page {page} complete: {len(data['data'])} CVEs | Total: {total_fetched:,}")

                if page >= max_pages:
                    logger.info(f"Reached last page ({max_pages})")
                    break

                page += 1
                time.sleep(0.1)  # Rate limiting courtesy

            except Exception as e:
                logger.error(f"Error fetching page {page}: {e}")
                break

        self.stats['total_kev_cves'] = total_fetched
        logger.info(f"✅ Fetched {total_fetched:,} KEV CVEs from VulnCheck")

    def enrich_neo4j_cves(self):
        """Enrich Neo4j CVEs with KEV data and CWE relationships."""
        logger.info("Enriching Neo4j CVEs with KEV data...")

        processed = 0
        for cve_id, kev_info in self.kev_data.items():
            try:
                # Update CVE with KEV flag
                if kev_info['is_kev']:
                    self._flag_cve_as_kev(cve_id, kev_info)
                    self.stats['kev_flagged'] += 1

                # Create CWE relationships
                for cwe_id in kev_info['cwe_ids']:
                    # Check if CWE exists
                    if cwe_id.lower() not in self.cwe_cache:
                        self.stats['missing_cwes'][cwe_id] += 1
                        continue

                    # Create relationship
                    if self._create_cve_cwe_relationship(cve_id, cwe_id):
                        self.stats['cwe_relationships'] += 1

                processed += 1

                if processed % 100 == 0:
                    logger.info(f"Progress: {processed:,}/{len(self.kev_data):,} | "
                              f"KEV flagged: {self.stats['kev_flagged']:,} | "
                              f"Relationships: {self.stats['cwe_relationships']:,}")

            except Exception as e:
                logger.error(f"Error processing {cve_id}: {e}")

        logger.info(f"✅ Processed {processed:,} KEV CVEs")

    def _flag_cve_as_kev(self, cve_id: str, kev_info: Dict) -> bool:
        """Flag CVE as Known Exploited in Neo4j."""
        query = """
        MATCH (cve:CVE {id: $cve_id})
        SET cve.is_kev = true,
            cve.kev_date_added = $date_added,
            cve.kev_enrichment_date = datetime(),
            cve.ransomware_use = $ransomware_use
        RETURN cve.id AS updated
        """

        try:
            with self.driver.session() as session:
                result = session.run(
                    query,
                    cve_id=cve_id,
                    date_added=kev_info.get('cisa_date_added'),
                    ransomware_use=kev_info.get('ransomware_use')
                )
                return result.single() is not None
        except Exception as e:
            logger.debug(f"CVE not in database: {cve_id}")
            return False

    def _create_cve_cwe_relationship(self, cve_id: str, cwe_id: str) -> bool:
        """Create CVE→CWE relationship."""
        query = """
        MATCH (cve:CVE {id: $cve_id})
        MATCH (cwe:CWE)
        WHERE toLower(cwe.id) = toLower($cwe_id)
        MERGE (cve)-[r:IS_WEAKNESS_TYPE]->(cwe)
        RETURN count(r) > 0 AS created
        """

        try:
            with self.driver.session() as session:
                result = session.run(query, cve_id=cve_id, cwe_id=cwe_id)
                return result.single()['created']
        except Exception as e:
            logger.debug(f"Relationship creation failed for {cve_id}→{cwe_id}: {e}")
            return False

    def run(self):
        """Execute full KEV enrichment pipeline."""
        logger.info("=" * 80)
        logger.info("VULNCHECK KEV BULK ENRICHMENT")
        logger.info("=" * 80)

        start_time = time.time()

        # Step 1: Load CWE cache
        self.load_cwe_cache()

        # Step 2: Fetch ALL KEV data
        self.fetch_all_kev_data()

        # Step 3: Enrich Neo4j CVEs
        self.enrich_neo4j_cves()

        # Final statistics
        elapsed = time.time() - start_time
        logger.info("\n" + "=" * 80)
        logger.info("ENRICHMENT COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Total KEV CVEs fetched: {self.stats['total_kev_cves']:,}")
        logger.info(f"CVEs flagged as KEV: {self.stats['kev_flagged']:,}")
        logger.info(f"CVE→CWE relationships created: {self.stats['cwe_relationships']:,}")
        logger.info(f"Missing CWEs: {len(self.stats['missing_cwes'])}")
        logger.info(f"Total time: {elapsed/60:.1f} minutes")

        if self.stats['missing_cwes']:
            logger.info("\nTop 20 missing CWEs:")
            for cwe_id, count in sorted(self.stats['missing_cwes'].items(),
                                       key=lambda x: x[1], reverse=True)[:20]:
                logger.info(f"  {cwe_id}: {count} occurrences")

        # Save statistics
        with open('vulncheck_kev_stats.json', 'w') as f:
            json.dump({
                'stats': self.stats,
                'missing_cwes': dict(self.stats['missing_cwes'])
            }, f, indent=2)

        logger.info("\n✅ Statistics saved to: vulncheck_kev_stats.json")


def main():
    """Main execution function."""
    enricher = VulnCheckKEVBulkEnrichment(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        enricher.run()
        return True
    except KeyboardInterrupt:
        logger.warning("\n⚠️ Interrupted by user")
        return False
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        return False
    finally:
        enricher.close()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
