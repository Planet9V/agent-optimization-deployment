#!/usr/bin/env python3
"""
EPSS Enrichment Script
Enriches CVE nodes with EPSS scores from FIRST.org API
Batch processing for 316,552 CVEs with progress tracking
"""

import requests
import time
from typing import List, Dict, Tuple
from neo4j import GraphDatabase
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/scripts/epss_enrichment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# FIRST.org EPSS API
EPSS_API_URL = "https://api.first.org/data/v1/epss"
BATCH_SIZE = 1000  # FIRST.org supports up to 1000 CVEs per request
REQUEST_DELAY = 0.5  # Delay between requests (seconds)


class EPSSEnrichment:
    """EPSS enrichment handler for CVE nodes"""

    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.stats = {
            'total_cves': 0,
            'already_enriched': 0,
            'newly_enriched': 0,
            'failed': 0,
            'no_epss_data': 0,
            'priority_now': 0,
            'priority_next': 0,
            'priority_never': 0
        }

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()

    def get_all_cve_ids(self) -> List[str]:
        """Get all CVE IDs from Neo4j"""
        query = """
        MATCH (c:CVE)
        RETURN c.cve_id AS cve_id
        ORDER BY c.cve_id
        """
        with self.driver.session() as session:
            result = session.run(query)
            cve_ids = [record['cve_id'] for record in result]
            logger.info(f"Retrieved {len(cve_ids)} CVE IDs from database")
            return cve_ids

    def get_unenriched_cve_ids(self) -> List[str]:
        """Get CVE IDs without EPSS scores"""
        query = """
        MATCH (c:CVE)
        WHERE c.epss_score IS NULL AND c.cve_id IS NOT NULL
        RETURN c.cve_id AS cve_id
        ORDER BY c.cve_id
        """
        with self.driver.session() as session:
            result = session.run(query)
            cve_ids = [record['cve_id'] for record in result if record['cve_id']]
            logger.info(f"Found {len(cve_ids)} CVEs without EPSS scores")
            return cve_ids

    def check_existing_epss_coverage(self) -> Dict[str, int]:
        """Check current EPSS coverage statistics"""
        query = """
        MATCH (c:CVE)
        RETURN
            count(c) AS total_cves,
            count(c.epss_score) AS with_epss,
            count(CASE WHEN c.epss_score IS NULL THEN 1 END) AS without_epss,
            count(CASE WHEN c.epss_score >= 0.7 THEN 1 END) AS priority_now,
            count(CASE WHEN c.epss_score >= 0.3 AND c.epss_score < 0.7 THEN 1 END) AS priority_next,
            count(CASE WHEN c.epss_score < 0.3 THEN 1 END) AS priority_never
        """
        with self.driver.session() as session:
            result = session.run(query)
            stats = result.single()
            coverage = {
                'total_cves': stats['total_cves'],
                'with_epss': stats['with_epss'],
                'without_epss': stats['without_epss'],
                'priority_now': stats['priority_now'],
                'priority_next': stats['priority_next'],
                'priority_never': stats['priority_never']
            }
            logger.info(f"Current EPSS coverage: {coverage['with_epss']}/{coverage['total_cves']} "
                       f"({coverage['with_epss']/coverage['total_cves']*100:.2f}%)")
            return coverage

    def fetch_epss_scores(self, cve_ids: List[str]) -> Dict[str, Dict]:
        """
        Fetch EPSS scores from FIRST.org API for a batch of CVEs

        Args:
            cve_ids: List of CVE IDs (max 1000)

        Returns:
            Dictionary mapping CVE ID to EPSS data
        """
        if len(cve_ids) > BATCH_SIZE:
            logger.warning(f"Batch size {len(cve_ids)} exceeds maximum {BATCH_SIZE}, truncating")
            cve_ids = cve_ids[:BATCH_SIZE]

        # Build comma-separated CVE list
        cve_param = ','.join(cve_ids)

        try:
            # Make API request
            response = requests.get(
                EPSS_API_URL,
                params={'cve': cve_param},
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            # Parse response
            epss_data = {}
            if 'data' in data:
                for item in data['data']:
                    cve_id = item.get('cve')
                    epss_score = float(item.get('epss', 0))
                    percentile = float(item.get('percentile', 0))

                    epss_data[cve_id] = {
                        'epss_score': epss_score,
                        'epss_percentile': percentile,
                        'priority_tier': self._calculate_priority_tier(epss_score)
                    }

            logger.info(f"Fetched EPSS data for {len(epss_data)}/{len(cve_ids)} CVEs")
            return epss_data

        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return {}

    def _calculate_priority_tier(self, epss_score: float) -> str:
        """Calculate priority tier based on EPSS score"""
        if epss_score >= 0.7:
            return "NOW"
        elif epss_score >= 0.3:
            return "NEXT"
        else:
            return "NEVER"

    def update_cve_epss(self, cve_id: str, epss_data: Dict):
        """Update CVE node with EPSS data"""
        query = """
        MATCH (c:CVE {cve_id: $cve_id})
        SET
            c.epss_score = $epss_score,
            c.epss_percentile = $epss_percentile,
            c.priority_tier = $priority_tier,
            c.epss_updated = datetime()
        """
        with self.driver.session() as session:
            session.run(
                query,
                cve_id=cve_id,
                epss_score=epss_data['epss_score'],
                epss_percentile=epss_data['epss_percentile'],
                priority_tier=epss_data['priority_tier']
            )

    def batch_update_cves(self, epss_data: Dict[str, Dict]):
        """Batch update CVE nodes with EPSS data"""
        query = """
        UNWIND $batch AS item
        MATCH (c:CVE {cve_id: item.cve_id})
        SET
            c.epss_score = item.epss_score,
            c.epss_percentile = item.epss_percentile,
            c.priority_tier = item.priority_tier,
            c.epss_updated = datetime()
        """

        batch = [
            {
                'cve_id': cve_id,
                'epss_score': data['epss_score'],
                'epss_percentile': data['epss_percentile'],
                'priority_tier': data['priority_tier']
            }
            for cve_id, data in epss_data.items()
        ]

        with self.driver.session() as session:
            session.run(query, batch=batch)
            logger.info(f"Updated {len(batch)} CVEs with EPSS data")

    def process_all_cves(self, force_refresh: bool = False):
        """
        Process all CVEs and enrich with EPSS scores

        Args:
            force_refresh: If True, refresh all CVEs. If False, only process unenriched CVEs
        """
        logger.info("Starting EPSS enrichment process")
        logger.info(f"Force refresh: {force_refresh}")

        # Check current coverage
        coverage = self.check_existing_epss_coverage()
        self.stats['total_cves'] = coverage['total_cves']
        self.stats['already_enriched'] = coverage['with_epss']

        # Get CVE IDs to process
        if force_refresh:
            cve_ids = self.get_all_cve_ids()
        else:
            cve_ids = self.get_unenriched_cve_ids()

        if not cve_ids:
            logger.info("No CVEs to process")
            return

        # Process in batches
        total_batches = (len(cve_ids) + BATCH_SIZE - 1) // BATCH_SIZE
        logger.info(f"Processing {len(cve_ids)} CVEs in {total_batches} batches")

        for i in range(0, len(cve_ids), BATCH_SIZE):
            batch_num = i // BATCH_SIZE + 1
            batch = cve_ids[i:i + BATCH_SIZE]

            logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} CVEs)")

            # Fetch EPSS scores
            epss_data = self.fetch_epss_scores(batch)

            if epss_data:
                # Update CVEs
                self.batch_update_cves(epss_data)
                self.stats['newly_enriched'] += len(epss_data)

                # Track priority distribution
                for data in epss_data.values():
                    if data['priority_tier'] == 'NOW':
                        self.stats['priority_now'] += 1
                    elif data['priority_tier'] == 'NEXT':
                        self.stats['priority_next'] += 1
                    else:
                        self.stats['priority_never'] += 1

                # Track missing data
                missing = len(batch) - len(epss_data)
                if missing > 0:
                    self.stats['no_epss_data'] += missing
                    logger.warning(f"{missing} CVEs in batch had no EPSS data")
            else:
                self.stats['failed'] += len(batch)
                logger.error(f"Batch {batch_num} failed completely")

            # Rate limiting
            if batch_num < total_batches:
                time.sleep(REQUEST_DELAY)

        logger.info("EPSS enrichment complete")
        self._print_final_stats()

    def _print_final_stats(self):
        """Print final statistics"""
        logger.info("=" * 60)
        logger.info("EPSS ENRICHMENT FINAL STATISTICS")
        logger.info("=" * 60)
        logger.info(f"Total CVEs in database: {self.stats['total_cves']:,}")
        logger.info(f"Already enriched: {self.stats['already_enriched']:,}")
        logger.info(f"Newly enriched: {self.stats['newly_enriched']:,}")
        logger.info(f"No EPSS data available: {self.stats['no_epss_data']:,}")
        logger.info(f"Failed updates: {self.stats['failed']:,}")
        logger.info("")
        logger.info("PRIORITY DISTRIBUTION:")
        logger.info(f"  NOW (EPSS ≥ 0.7):   {self.stats['priority_now']:,}")
        logger.info(f"  NEXT (0.3-0.7):     {self.stats['priority_next']:,}")
        logger.info(f"  NEVER (< 0.3):      {self.stats['priority_never']:,}")
        logger.info("")

        total_enriched = self.stats['already_enriched'] + self.stats['newly_enriched']
        coverage_pct = (total_enriched / self.stats['total_cves'] * 100) if self.stats['total_cves'] > 0 else 0
        logger.info(f"FINAL COVERAGE: {total_enriched:,}/{self.stats['total_cves']:,} ({coverage_pct:.2f}%)")
        logger.info("=" * 60)


def main():
    """Main execution"""
    enrichment = EPSSEnrichment()

    try:
        # Check arguments for force refresh
        import sys
        force_refresh = '--force' in sys.argv or '--refresh' in sys.argv

        # Process all CVEs
        enrichment.process_all_cves(force_refresh=force_refresh)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        enrichment.close()


if __name__ == "__main__":
    main()
