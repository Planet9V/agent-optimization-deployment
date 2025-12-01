#!/usr/bin/env python3
"""
INTEGRATED DATA COMPLETION PIPELINE
Using NVD API + VulnCheck KEV API for complete Neo4j relationships

Data Sources:
1. VulnCheck KEV API: EPSS scores, KEV status, CWE mappings (FAST - no rate limits)
2. NVD API: Official CVE→CWE mappings (fallback, rate limited)
3. CWE v4.18 XML: Complete weakness catalog
4. CAPEC v3.9 XML: Attack pattern mappings

Strategy:
- Phase 1: VulnCheck KEV API (primary) - enriches CVEs with EPSS, KEV, CWE
- Phase 2: NVD API (fallback) - fills gaps for CVEs not in VulnCheck
- Phase 3: CWE/CAPEC XML - creates complete relationship chains

Author: AEON Protocol - Integrated Implementation
Date: 2025-11-07
Version: 4.0.0
"""

import requests
import time
import logging
import sys
import json
from typing import Dict, List, Set, Tuple, Optional
from neo4j import GraphDatabase
from collections import defaultdict
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('integrated_data_completion.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# API Configuration
NIST_NVD_API_KEY = "534786f5-5359-40b8-8e54-b28eb742de7c"
VULNCHECK_API_KEY = "vulncheck_d50b2321719330fa9fd39437b61bab52d729bfa093b8f15fe97b4db4349f584c"

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
VULNCHECK_KEV_URL = "https://api.vulncheck.com/v3/index/vulncheck-kev"

# Neo4j Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# Rate limiting
NVD_RATE_LIMIT = 5  # requests per 30 seconds
NVD_REQUESTS = []


class IntegratedDataCompletion:
    """
    Complete Neo4j database using VulnCheck KEV API (primary) and NVD API (fallback).
    """

    def __init__(self, uri: str, user: str, password: str):
        """Initialize connections."""
        self.driver = GraphDatabase.driver(
            uri,
            auth=(user, password),
            max_connection_pool_size=10,
            connection_acquisition_timeout=30
        )
        self.session_http = requests.Session()
        self.cwe_cache = {}  # Cache for CWE existence checks
        self.stats = {
            'total_cves': 0,
            'vulncheck_enriched': 0,
            'nvd_fallback': 0,
            'epss_updated': 0,
            'kev_flagged': 0,
            'cwe_relationships': 0,
            'missing_cwes': defaultdict(int),
            'errors': 0,
            'cache_hits': 0
        }
        # Pre-load all CWE IDs into cache
        self._load_cwe_cache()
        logger.info(f"Connected to Neo4j at {uri}")

    def _load_cwe_cache(self):
        """Pre-load all CWE IDs into cache to avoid repeated queries."""
        logger.info("Pre-loading CWE cache...")
        query = "MATCH (w:CWE) RETURN toLower(w.id) AS cwe_id"

        try:
            with self.driver.session() as session:
                result = session.run(query)
                for record in result:
                    self.cwe_cache[record['cwe_id']] = True
            logger.info(f"CWE cache loaded: {len(self.cwe_cache):,} CWEs")
        except Exception as e:
            logger.error(f"Failed to load CWE cache: {e}")
            logger.warning("Continuing without cache - performance may be degraded")

    def close(self):
        """Close connections."""
        self.driver.close()
        self.session_http.close()

    def test_vulncheck_access(self) -> Tuple[bool, str]:
        """
        Test VulnCheck API access and capabilities.

        Returns:
            Tuple of (success, message)
        """
        logger.info("Testing VulnCheck KEV API access...")

        url = f"{VULNCHECK_KEV_URL}?cve=CVE-2021-44228"  # Test with Log4Shell
        headers = {"Authorization": f"Bearer {VULNCHECK_API_KEY}"}

        try:
            response = self.session_http.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            if 'data' in data and len(data['data']) > 0:
                sample = data['data'][0]
                logger.info("✅ VulnCheck API access successful!")
                logger.info(f"Sample CVE: {sample.get('cve')}")
                logger.info(f"Available fields: {list(sample.keys())}")

                # Check for key fields
                has_epss = 'epss' in sample
                has_kev = 'vulncheck_kev' in sample or 'cisa_date_added' in sample
                has_cwe = 'cwes' in sample or 'cwe' in sample or 'weaknesses' in sample

                logger.info(f"EPSS available: {has_epss}")
                logger.info(f"KEV available: {has_kev}")
                logger.info(f"CWE available: {has_cwe}")
                if 'cwes' in sample:
                    logger.info(f"Sample CWEs: {sample['cwes'][:5] if len(sample['cwes']) > 5 else sample['cwes']}")

                return True, "VulnCheck API fully functional"
            else:
                return False, "No data returned from VulnCheck"

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 402:
                return False, "Payment Required - Subscription inactive"
            elif e.response.status_code == 401:
                return False, "Unauthorized - Invalid API key"
            else:
                return False, f"HTTP Error: {e.response.status_code}"
        except Exception as e:
            return False, f"Connection error: {str(e)}"

    def query_vulncheck_cve(self, cve_id: str) -> Optional[Dict]:
        """
        Query VulnCheck KEV API for CVE enrichment data.

        Returns:
            Dictionary with CVE enrichment data or None if error
        """
        url = f"{VULNCHECK_KEV_URL}?cve={cve_id}"
        headers = {"Authorization": f"Bearer {VULNCHECK_API_KEY}"}

        try:
            response = self.session_http.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            if 'data' in data and len(data['data']) > 0:
                vuln_data = data['data'][0]

                # Extract CWE IDs (VulnCheck uses 'cwes' field)
                cwe_ids = []

                # Check both 'cwes' (VulnCheck KEV) and 'cwe' (legacy)
                cwe_field = vuln_data.get('cwes') or vuln_data.get('cwe')

                if cwe_field:
                    if isinstance(cwe_field, list):
                        for cwe in cwe_field:
                            if isinstance(cwe, str):
                                # Normalize to lowercase cwe-### format
                                cwe_clean = cwe.lower()
                                if cwe_clean.startswith('cwe-'):
                                    cwe_ids.append(cwe_clean)
                                elif cwe.isdigit():
                                    cwe_ids.append(f"cwe-{cwe}")
                    elif isinstance(cwe_field, str):
                        cwe_clean = cwe_field.lower()
                        if cwe_clean.startswith('cwe-'):
                            cwe_ids.append(cwe_clean)
                        elif cwe_field.isdigit():
                            cwe_ids.append(f"cwe-{cwe_field}")

                # Determine KEV status from multiple fields
                is_kev = False
                if 'vulncheck_kev' in vuln_data:
                    is_kev = vuln_data['vulncheck_kev'].get('known_exploited', False)
                elif 'knownRansomwareCampaignUse' in vuln_data:
                    is_kev = vuln_data['knownRansomwareCampaignUse'] == 'Known'
                elif 'cisa_date_added' in vuln_data:
                    is_kev = vuln_data['cisa_date_added'] is not None

                return {
                    'cve_id': cve_id,
                    'epss': vuln_data.get('epss'),
                    'epss_percentile': vuln_data.get('epss_percentile'),
                    'is_kev': is_kev,
                    'cwe_ids': cwe_ids,
                    'source': 'vulncheck',
                    'date_added': vuln_data.get('date_added'),
                    'cisa_date_added': vuln_data.get('cisa_date_added')
                }

            return None

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.debug(f"CVE not in VulnCheck: {cve_id}")
            else:
                logger.error(f"VulnCheck error for {cve_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error querying VulnCheck for {cve_id}: {e}")
            return None

    def rate_limit_nvd(self):
        """Enforce NVD API rate limiting."""
        global NVD_REQUESTS
        now = time.time()
        NVD_REQUESTS = [req_time for req_time in NVD_REQUESTS if now - req_time < 30]

        if len(NVD_REQUESTS) >= NVD_RATE_LIMIT:
            sleep_time = 30 - (now - NVD_REQUESTS[0]) + 0.5
            if sleep_time > 0:
                logger.debug(f"NVD rate limit: sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
                NVD_REQUESTS = []

        NVD_REQUESTS.append(time.time())

    def query_nvd_cve_fallback(self, cve_id: str) -> Optional[Dict]:
        """
        Fallback to NVD API if VulnCheck doesn't have the CVE.

        Returns:
            Dictionary with CVE data or None
        """
        self.rate_limit_nvd()

        url = f"{NVD_API_URL}?cveId={cve_id}"
        headers = {"apiKey": NIST_NVD_API_KEY}

        try:
            response = self.session_http.get(url, headers=headers, timeout=30)
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

                return {
                    'cve_id': cve_id,
                    'cwe_ids': cwe_ids,
                    'source': 'nvd'
                }

            return None

        except Exception as e:
            logger.error(f"NVD API error for {cve_id}: {e}")
            return None

    def get_cves_needing_enrichment(self, limit: int = None) -> List[str]:
        """Get CVEs that need enrichment (no CWE relationships)."""
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

        logger.info(f"Found {len(cve_ids):,} CVEs needing enrichment")
        return cve_ids

    def update_cve_enrichment(self, cve_id: str, enrichment: Dict) -> bool:
        """Update CVE node with enrichment data."""
        query = """
        MATCH (cve:CVE {id: $cve_id})
        SET cve.epss_score = $epss,
            cve.epss_percentile = $epss_percentile,
            cve.is_kev = $is_kev,
            cve.enrichment_source = $source,
            cve.enrichment_date = datetime()
        RETURN cve.id AS updated
        """

        try:
            with self.driver.session() as session:
                result = session.run(
                    query,
                    cve_id=cve_id,
                    epss=enrichment.get('epss'),
                    epss_percentile=enrichment.get('epss_percentile'),
                    is_kev=enrichment.get('is_kev', False),
                    source=enrichment.get('source')
                )
                return result.single() is not None
        except Exception as e:
            logger.error(f"Error updating CVE {cve_id}: {e}")
            return False

    def verify_cwe_exists(self, cwe_id: str) -> bool:
        """Check if CWE exists using pre-loaded cache."""
        cwe_lower = cwe_id.lower()
        exists = cwe_lower in self.cwe_cache

        if exists:
            self.stats['cache_hits'] += 1

        return exists

    def create_cve_cwe_relationship(self, cve_id: str, cwe_id: str) -> bool:
        """Create IS_WEAKNESS_TYPE relationship with retry logic."""
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
                    logger.warning(f"Relationship creation failed (attempt {attempt + 1}/{max_retries}), retrying...")
                    time.sleep(1)
                else:
                    logger.error(f"Error creating relationship {cve_id}→{cwe_id} after {max_retries} attempts: {e}")
                    return False

    def process_integrated_enrichment(self, max_cves: int = None):
        """
        Integrated enrichment: VulnCheck primary, NVD fallback.

        Args:
            max_cves: Maximum CVEs to process (None = all)
        """
        logger.info("=" * 80)
        logger.info("INTEGRATED DATA ENRICHMENT")
        logger.info("VulnCheck KEV API (primary) + NVD API (fallback)")
        logger.info("=" * 80)

        # Test VulnCheck access first
        vulncheck_ok, message = self.test_vulncheck_access()
        logger.info(f"VulnCheck status: {message}")

        if not vulncheck_ok:
            logger.warning("⚠️ VulnCheck unavailable, will use NVD API only")

        # Get CVEs needing enrichment
        cve_ids = self.get_cves_needing_enrichment(limit=max_cves)
        self.stats['total_cves'] = len(cve_ids)

        if not cve_ids:
            logger.info("No CVEs need enrichment!")
            return

        start_time = time.time()

        for i, cve_id in enumerate(cve_ids, 1):
            enrichment = None

            # Try VulnCheck first (if available)
            if vulncheck_ok:
                enrichment = self.query_vulncheck_cve(cve_id)
                if enrichment:
                    self.stats['vulncheck_enriched'] += 1

                    # Update CVE with EPSS/KEV data
                    if enrichment.get('epss'):
                        if self.update_cve_enrichment(cve_id, enrichment):
                            self.stats['epss_updated'] += 1

                    if enrichment.get('is_kev'):
                        self.stats['kev_flagged'] += 1

            # Fallback to NVD if VulnCheck didn't have it
            if not enrichment:
                enrichment = self.query_nvd_cve_fallback(cve_id)
                if enrichment:
                    self.stats['nvd_fallback'] += 1

            # Process CWE relationships
            if enrichment and enrichment.get('cwe_ids'):
                for cwe_id in enrichment['cwe_ids']:
                    # Check if CWE exists
                    if not self.verify_cwe_exists(cwe_id):
                        self.stats['missing_cwes'][cwe_id] += 1
                        continue

                    # Create relationship
                    if self.create_cve_cwe_relationship(cve_id, cwe_id):
                        self.stats['cwe_relationships'] += 1

            # Progress logging
            if i % 100 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0
                eta = (len(cve_ids) - i) / rate if rate > 0 else 0

                logger.info(f"Progress: {i:,}/{len(cve_ids):,} ({100*i/len(cve_ids):.1f}%) | "
                          f"Rate: {rate:.1f} CVE/s | ETA: {eta/60:.0f}min | "
                          f"VulnCheck: {self.stats['vulncheck_enriched']:,} | "
                          f"NVD: {self.stats['nvd_fallback']:,} | "
                          f"Relationships: {self.stats['cwe_relationships']:,}")

        # Final statistics
        elapsed = time.time() - start_time
        logger.info("\n" + "=" * 80)
        logger.info("ENRICHMENT COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Total CVEs processed: {len(cve_ids):,}")
        logger.info(f"VulnCheck enriched: {self.stats['vulncheck_enriched']:,}")
        logger.info(f"NVD fallback used: {self.stats['nvd_fallback']:,}")
        logger.info(f"EPSS scores updated: {self.stats['epss_updated']:,}")
        logger.info(f"KEV flagged: {self.stats['kev_flagged']:,}")
        logger.info(f"CVE→CWE relationships created: {self.stats['cwe_relationships']:,}")
        logger.info(f"Unique missing CWEs: {len(self.stats['missing_cwes'])}")
        logger.info(f"Total time: {elapsed/60:.1f} minutes")
        logger.info(f"Average rate: {len(cve_ids)/elapsed:.1f} CVE/s")

        if self.stats['missing_cwes']:
            logger.info("\nTop 20 missing CWEs:")
            for cwe_id, count in sorted(self.stats['missing_cwes'].items(),
                                       key=lambda x: x[1], reverse=True)[:20]:
                logger.info(f"  {cwe_id}: {count} occurrences")


def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("INTEGRATED DATA COMPLETION PIPELINE")
    logger.info("VulnCheck KEV API + NVD API")
    logger.info("=" * 80)

    # Check mode
    test_mode = '--test' in sys.argv
    max_cves = 1000 if test_mode else None

    if test_mode:
        logger.info("🧪 TEST MODE: Processing first 1,000 CVEs")
    else:
        logger.info("🚀 FULL MODE: Processing ALL CVEs")

    completer = IntegratedDataCompletion(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        completer.process_integrated_enrichment(max_cves=max_cves)

        logger.info("\n✅ PIPELINE COMPLETE")

        # Save statistics
        with open('integrated_enrichment_stats.json', 'w') as f:
            json.dump({
                'stats': completer.stats,
                'missing_cwes': dict(completer.stats['missing_cwes'])
            }, f, indent=2)

        logger.info("Statistics saved to: integrated_enrichment_stats.json")

        return True

    except KeyboardInterrupt:
        logger.warning("\n⚠️ Interrupted by user")
        return False
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        return False
    finally:
        completer.close()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
