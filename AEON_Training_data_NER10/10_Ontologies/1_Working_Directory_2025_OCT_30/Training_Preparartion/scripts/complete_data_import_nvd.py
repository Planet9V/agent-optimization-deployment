#!/usr/bin/env python3
"""
COMPLETE DATA IMPORT FROM NVD API
Comprehensive import of ALL CVE→CWE relationships using official NVD mappings

Based on validation findings:
- 316,552 CVEs in database
- Only 886 CVE→CWE relationships exist (0.28%)
- Need to create 100K+ relationships from NVD official data

This script will:
1. Query ALL CVEs from Neo4j
2. Fetch official CWE mappings from NVD API
3. Create complete CVE→CWE relationships
4. Validate coverage and completeness

Author: AEON Protocol - Complete Implementation
Date: 2025-11-07
Version: 3.0.0
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
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('complete_data_import_nvd.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# API Configuration
NVD_API_KEY = "534786f5-5359-40b8-8e54-b28eb742de7c"
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Neo4j Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# Rate limiting tracking
NVD_RATE_LIMIT = 5  # requests per 30 seconds
NVD_REQUESTS = []

# Progress tracking
CHECKPOINT_INTERVAL = 1000  # Save progress every N CVEs


class CompleteNVDImporter:
    """
    Complete importer for CVE→CWE relationships using NVD API.
    """

    def __init__(self, uri: str, user: str, password: str):
        """Initialize connections."""
        # Configure Neo4j driver with better connection handling
        self.driver = GraphDatabase.driver(
            uri,
            auth=(user, password),
            max_connection_lifetime=3600,  # 1 hour
            max_connection_pool_size=50,
            connection_timeout=30,
            keep_alive=True
        )
        self.session_http = requests.Session()
        self.stats = {
            'total_cves': 0,
            'processed': 0,
            'cves_with_cwe': 0,
            'relationships_created': 0,
            'cwes_missing': defaultdict(int),
            'errors': 0,
            'skipped': 0
        }
        logger.info(f"Connected to Neo4j at {uri}")

    def close(self):
        """Close connections."""
        self.driver.close()
        self.session_http.close()

    def rate_limit_nvd(self):
        """Enforce NVD API rate limiting (5 requests per 30 seconds)."""
        global NVD_REQUESTS
        now = time.time()

        # Remove requests older than 30 seconds
        NVD_REQUESTS = [req_time for req_time in NVD_REQUESTS if now - req_time < 30]

        # Wait if at rate limit
        if len(NVD_REQUESTS) >= NVD_RATE_LIMIT:
            sleep_time = 30 - (now - NVD_REQUESTS[0]) + 0.5  # Add buffer
            if sleep_time > 0:
                logger.debug(f"Rate limit: sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
                NVD_REQUESTS = []

        NVD_REQUESTS.append(time.time())

    def get_all_cves_from_neo4j(self) -> List[str]:
        """Get ALL CVE IDs from Neo4j."""
        query = """
        MATCH (c:CVE)
        RETURN c.id AS cve_id
        ORDER BY c.id
        """

        with self.driver.session() as session:
            result = session.run(query)
            cve_ids = [record['cve_id'] for record in result]

        logger.info(f"Retrieved {len(cve_ids):,} CVE IDs from Neo4j")
        self.stats['total_cves'] = len(cve_ids)
        return cve_ids

    def get_cves_without_cwe(self, limit: int = None) -> List[str]:
        """Get CVEs that don't have CWE relationships yet."""
        query = """
        MATCH (c:CVE)
        WHERE NOT (c)-[:IS_WEAKNESS_TYPE]->(:CWE)
        RETURN c.id AS cve_id
        ORDER BY c.id
        """
        if limit:
            query += f" LIMIT {limit}"

        with self.driver.session() as session:
            result = session.run(query)
            cve_ids = [record['cve_id'] for record in result]

        logger.info(f"Found {len(cve_ids):,} CVEs without CWE relationships")
        return cve_ids

    def query_nvd_cve(self, cve_id: str) -> Dict:
        """Query NVD API for CVE data including CWE mappings."""
        self.rate_limit_nvd()

        url = f"{NVD_API_URL}?cveId={cve_id}"
        headers = {"apiKey": self.nvd_api_key}

        try:
            response = self.session_http.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get('vulnerabilities'):
                vuln = data['vulnerabilities'][0]['cve']

                # Extract CWE IDs from weaknesses
                cwe_ids = []
                if 'weaknesses' in vuln:
                    for weakness in vuln['weaknesses']:
                        for desc in weakness.get('description', []):
                            value = desc.get('value', '')
                            if value.startswith('CWE-') or value.startswith('cwe-'):
                                # Normalize to lowercase
                                cwe_ids.append(value.lower())

                return {
                    'cve_id': cve_id,
                    'cwe_ids': cwe_ids,
                    'success': True
                }

            return {'cve_id': cve_id, 'cwe_ids': [], 'success': True}

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.debug(f"CVE not found in NVD: {cve_id}")
                return {'cve_id': cve_id, 'cwe_ids': [], 'success': True, 'not_found': True}
            logger.error(f"HTTP error for {cve_id}: {e}")
            return {'cve_id': cve_id, 'cwe_ids': [], 'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"Error querying {cve_id}: {e}")
            return {'cve_id': cve_id, 'cwe_ids': [], 'success': False, 'error': str(e)}

    def verify_cwe_exists(self, cwe_id: str) -> bool:
        """Check if CWE node exists in Neo4j."""
        query = """
        MATCH (w:CWE)
        WHERE toLower(w.id) = toLower($cwe_id)
        RETURN count(w) > 0 AS exists
        """

        max_retries = 3
        for attempt in range(max_retries):
            try:
                with self.driver.session() as session:
                    result = session.run(query, cwe_id=cwe_id)
                    return result.single()['exists']
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Retry {attempt+1}/{max_retries} for CWE verification: {cwe_id}")
                    time.sleep(1)
                    # Reconnect driver
                    self.driver.close()
                    self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
                else:
                    logger.error(f"Failed to verify CWE after {max_retries} attempts: {cwe_id}")
                    raise

    def create_cve_cwe_relationship(self, cve_id: str, cwe_id: str) -> bool:
        """Create IS_WEAKNESS_TYPE relationship between CVE and CWE."""
        query = """
        MATCH (cve:CVE {id: $cve_id})
        MATCH (cwe:CWE)
        WHERE toLower(cwe.id) = toLower($cwe_id)
        MERGE (cve)-[r:IS_WEAKNESS_TYPE]->(cwe)
        RETURN count(r) > 0 AS created
        """

        max_retries = 3
        for attempt in range(max_retries):
            try:
                with self.driver.session() as session:
                    result = session.run(query, cve_id=cve_id, cwe_id=cwe_id)
                    return result.single()['created']
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Retry {attempt+1}/{max_retries} for relationship creation: {cve_id}→{cwe_id}")
                    time.sleep(1)
                    # Reconnect driver
                    self.driver.close()
                    self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
                else:
                    logger.error(f"Error creating relationship {cve_id}→{cwe_id}: {e}")
                    return False

    def save_checkpoint(self):
        """Save progress checkpoint."""
        checkpoint_data = {
            'timestamp': datetime.now().isoformat(),
            'stats': dict(self.stats),
            'cwes_missing': dict(self.stats['cwes_missing'])
        }

        with open('import_checkpoint.json', 'w') as f:
            json.dump(checkpoint_data, f, indent=2)

        logger.info(f"Checkpoint saved: {self.stats['processed']:,} CVEs processed")

    def process_all_cves(self, batch_size: int = 1000, max_cves: int = None):
        """
        Process ALL CVEs to create complete CVE→CWE relationships.

        Args:
            batch_size: Number of CVEs to process before checkpoint
            max_cves: Maximum CVEs to process (None = all)
        """
        # Get CVEs that need CWE relationships
        cve_ids = self.get_cves_without_cwe(limit=max_cves)

        if not cve_ids:
            logger.info("No CVEs without CWE relationships found!")
            return

        logger.info("=" * 80)
        logger.info(f"PROCESSING {len(cve_ids):,} CVEs")
        logger.info("=" * 80)

        start_time = time.time()

        for i, cve_id in enumerate(cve_ids, 1):
            # Query NVD
            nvd_data = self.query_nvd_cve(cve_id)

            if not nvd_data['success']:
                self.stats['errors'] += 1
                self.stats['processed'] += 1
                continue

            if nvd_data.get('not_found'):
                self.stats['skipped'] += 1
                self.stats['processed'] += 1
                continue

            # Process CWE mappings
            if nvd_data['cwe_ids']:
                self.stats['cves_with_cwe'] += 1

                for cwe_id in nvd_data['cwe_ids']:
                    # Check if CWE exists
                    if not self.verify_cwe_exists(cwe_id):
                        self.stats['cwes_missing'][cwe_id] += 1
                        logger.warning(f"CWE not in database: {cwe_id} (from {cve_id})")
                        continue

                    # Create relationship
                    if self.create_cve_cwe_relationship(cve_id, cwe_id):
                        self.stats['relationships_created'] += 1

            self.stats['processed'] += 1

            # Progress logging
            if i % 100 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0
                eta = (len(cve_ids) - i) / rate if rate > 0 else 0

                logger.info(f"Progress: {i:,}/{len(cve_ids):,} ({100*i/len(cve_ids):.1f}%) | "
                          f"Rate: {rate:.1f} CVE/s | ETA: {eta/60:.0f}min | "
                          f"Relationships: {self.stats['relationships_created']:,}")

            # Checkpoint
            if i % CHECKPOINT_INTERVAL == 0:
                self.save_checkpoint()

        # Final save
        self.save_checkpoint()

        # Final statistics
        elapsed = time.time() - start_time
        logger.info("\n" + "=" * 80)
        logger.info("IMPORT COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Total CVEs processed: {self.stats['processed']:,}")
        logger.info(f"CVEs with CWE mappings: {self.stats['cves_with_cwe']:,}")
        logger.info(f"Relationships created: {self.stats['relationships_created']:,}")
        logger.info(f"Errors: {self.stats['errors']:,}")
        logger.info(f"Skipped (not found): {self.stats['skipped']:,}")
        logger.info(f"Unique missing CWEs: {len(self.stats['cwes_missing'])}")
        logger.info(f"Total time: {elapsed/60:.1f} minutes")
        logger.info(f"Average rate: {self.stats['processed']/elapsed:.1f} CVE/s")

        if self.stats['cwes_missing']:
            logger.info("\nTop 20 missing CWEs:")
            for cwe_id, count in sorted(self.stats['cwes_missing'].items(),
                                       key=lambda x: x[1], reverse=True)[:20]:
                logger.info(f"  {cwe_id}: {count} occurrences")

    @property
    def nvd_api_key(self):
        """Get NVD API key."""
        return NVD_API_KEY


def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("COMPLETE CVE→CWE IMPORT FROM NVD API")
    logger.info("=" * 80)

    # Check if this is a test run or full import
    import sys
    test_mode = '--test' in sys.argv
    max_cves = 1000 if test_mode else None

    if test_mode:
        logger.info("🧪 TEST MODE: Processing first 1,000 CVEs only")
    else:
        logger.info("🚀 FULL IMPORT: Processing ALL CVEs without CWE relationships")

    importer = CompleteNVDImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        importer.process_all_cves(batch_size=1000, max_cves=max_cves)

        logger.info("\n" + "=" * 80)
        logger.info("✅ IMPORT SUCCESSFUL")
        logger.info("=" * 80)

        # Generate summary report
        with open('nvd_import_summary.txt', 'w') as f:
            f.write("NVD IMPORT SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Processed: {importer.stats['processed']:,} CVEs\n")
            f.write(f"Relationships Created: {importer.stats['relationships_created']:,}\n")
            f.write(f"CVEs with CWE: {importer.stats['cves_with_cwe']:,}\n")
            f.write(f"Errors: {importer.stats['errors']:,}\n")
            f.write(f"Missing CWEs: {len(importer.stats['cwes_missing'])}\n")

        logger.info("Summary written to: nvd_import_summary.txt")

        return True

    except KeyboardInterrupt:
        logger.warning("\n⚠️ Import interrupted by user")
        importer.save_checkpoint()
        logger.info("Progress saved to checkpoint file")
        return False
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        importer.save_checkpoint()
        return False
    finally:
        importer.close()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
