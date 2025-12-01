#!/usr/bin/env python3
"""
NVD API TEST IMPORT - Quick Validation
Test CVE→CWE relationship creation with fixed CWE data

Tests with 100 CVEs to validate emergency fix success
Expected: 30-50 relationships created (vs previous 0)
"""

import requests
import time
import logging
import sys
from typing import Dict, List
from neo4j import GraphDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nvd_test_import_quick.log'),
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

# Rate limiting
NVD_RATE_LIMIT = 5
NVD_REQUESTS = []


class NVDTestImporter:
    """Quick NVD API test importer."""

    def __init__(self, uri: str, user: str, password: str):
        """Initialize connections."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            'processed': 0,
            'relationships_created': 0,
            'cves_with_cwe': 0,
            'cwes_missing': set(),
            'errors': 0
        }
        logger.info(f"Connected to Neo4j at {uri}")

    def close(self):
        """Close connections."""
        self.driver.close()

    def rate_limit_nvd(self):
        """Enforce NVD API rate limiting."""
        global NVD_REQUESTS
        now = time.time()
        NVD_REQUESTS = [req_time for req_time in NVD_REQUESTS if now - req_time < 30]

        if len(NVD_REQUESTS) >= NVD_RATE_LIMIT:
            sleep_time = 30 - (now - NVD_REQUESTS[0]) + 0.5
            if sleep_time > 0:
                time.sleep(sleep_time)
                NVD_REQUESTS = []

        NVD_REQUESTS.append(time.time())

    def get_test_cves(self, limit: int = 100) -> List[str]:
        """Get test CVEs without CWE relationships."""
        query = """
        MATCH (c:CVE)
        WHERE NOT (c)-[:IS_WEAKNESS_TYPE]->(:CWE)
        RETURN c.id AS cve_id
        ORDER BY c.id
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            cve_ids = [record['cve_id'] for record in result]

        logger.info(f"Retrieved {len(cve_ids):,} test CVEs")
        return cve_ids

    def query_nvd_cve(self, cve_id: str) -> Dict:
        """Query NVD API for CVE data."""
        self.rate_limit_nvd()

        url = f"{NVD_API_URL}?cveId={cve_id}"
        headers = {"apiKey": NVD_API_KEY}

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get('vulnerabilities'):
                vuln = data['vulnerabilities'][0]['cve']

                # Extract CWE IDs
                cwe_ids = []
                if 'weaknesses' in vuln:
                    for weakness in vuln['weaknesses']:
                        for desc in weakness.get('description', []):
                            value = desc.get('value', '')
                            if value.startswith('CWE-') or value.startswith('cwe-'):
                                cwe_ids.append(value.lower())

                return {'cve_id': cve_id, 'cwe_ids': cwe_ids, 'success': True}

            return {'cve_id': cve_id, 'cwe_ids': [], 'success': True}

        except Exception as e:
            logger.error(f"Error querying {cve_id}: {e}")
            return {'cve_id': cve_id, 'cwe_ids': [], 'success': False}

    def verify_cwe_exists(self, cwe_id: str) -> bool:
        """Check if CWE exists (case-insensitive)."""
        query = """
        MATCH (w:CWE)
        WHERE toLower(w.id) = toLower($cwe_id)
        RETURN count(w) > 0 AS exists
        """

        with self.driver.session() as session:
            result = session.run(query, cwe_id=cwe_id)
            return result.single()['exists']

    def create_cve_cwe_relationship(self, cve_id: str, cwe_id: str) -> bool:
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
            logger.error(f"Error creating relationship {cve_id}→{cwe_id}: {e}")
            return False

    def test_import(self, limit: int = 100):
        """Run test import."""
        logger.info("=" * 80)
        logger.info(f"NVD API TEST IMPORT - {limit} CVEs")
        logger.info("=" * 80)

        # Get test CVEs
        cve_ids = self.get_test_cves(limit=limit)

        if not cve_ids:
            logger.info("No CVEs without CWE relationships found!")
            return

        start_time = time.time()

        for i, cve_id in enumerate(cve_ids, 1):
            # Query NVD
            nvd_data = self.query_nvd_cve(cve_id)

            if not nvd_data['success']:
                self.stats['errors'] += 1
                self.stats['processed'] += 1
                continue

            # Process CWE mappings
            if nvd_data['cwe_ids']:
                self.stats['cves_with_cwe'] += 1

                for cwe_id in nvd_data['cwe_ids']:
                    # Check if CWE exists
                    if not self.verify_cwe_exists(cwe_id):
                        self.stats['cwes_missing'].add(cwe_id)
                        continue

                    # Create relationship
                    if self.create_cve_cwe_relationship(cve_id, cwe_id):
                        self.stats['relationships_created'] += 1

            self.stats['processed'] += 1

            # Progress
            if i % 20 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0

                logger.info(f"Progress: {i}/{len(cve_ids)} ({100*i/len(cve_ids):.1f}%) | "
                          f"Rate: {rate:.1f} CVE/s | "
                          f"Relationships: {self.stats['relationships_created']:,}")

        # Final statistics
        elapsed = time.time() - start_time
        logger.info("\n" + "=" * 80)
        logger.info("TEST IMPORT COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Total CVEs processed: {self.stats['processed']:,}")
        logger.info(f"CVEs with CWE mappings: {self.stats['cves_with_cwe']:,}")
        logger.info(f"Relationships created: {self.stats['relationships_created']:,}")
        logger.info(f"Success rate: {100*self.stats['relationships_created']/self.stats['processed']:.1f}%")
        logger.info(f"Missing CWEs: {len(self.stats['cwes_missing'])}")
        logger.info(f"Total time: {elapsed:.1f} seconds")
        logger.info(f"Average rate: {self.stats['processed']/elapsed:.1f} CVE/s")

        if self.stats['cwes_missing']:
            logger.info(f"\nMissing CWEs encountered:")
            for cwe_id in sorted(self.stats['cwes_missing']):
                logger.info(f"  {cwe_id}")

        # Assessment
        logger.info("\n" + "=" * 80)
        logger.info("ASSESSMENT")
        logger.info("=" * 80)

        if self.stats['relationships_created'] > 30:
            logger.info("✅ SUCCESS: Emergency fix effective!")
            logger.info(f"   Relationship creation working ({self.stats['relationships_created']} created)")
        elif self.stats['relationships_created'] > 10:
            logger.info("⚠️ PARTIAL SUCCESS: Some relationships created")
            logger.info(f"   Review missing CWEs: {len(self.stats['cwes_missing'])}")
        else:
            logger.info("❌ FAILED: Relationship creation still blocked")
            logger.info(f"   Only {self.stats['relationships_created']} relationships created")


def main():
    """Main execution function."""
    importer = NVDTestImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        importer.test_import(limit=100)
        return 0

    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        return 1

    finally:
        importer.close()


if __name__ == "__main__":
    sys.exit(main())
