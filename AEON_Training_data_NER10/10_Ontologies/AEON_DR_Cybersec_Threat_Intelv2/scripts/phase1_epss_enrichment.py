#!/usr/bin/env python3
"""
Phase 1 Day 1: EPSS Score Enrichment
Enrich all 267,487 CVE nodes with EPSS scores from FIRST.org API

EXECUTION: DO THE ACTUAL WORK - enrich all CVEs with EPSS scores
"""

import time
import json
import logging
import requests
from datetime import datetime
from neo4j import GraphDatabase
from typing import Dict, List, Tuple
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/epss_enrichment_errors.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"
EPSS_API_BASE = "https://api.first.org/data/v1/epss"
API_BATCH_SIZE = 100  # Reduced to avoid URI Too Long errors
NEO4J_BATCH_SIZE = 5000  # Neo4j transaction batch size
CHECKPOINT_INTERVAL = 25000  # Checkpoint every 25K CVEs
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

class EPSSEnrichment:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.stats = {
            'total_cves': 0,
            'enriched_cves': 0,
            'failed_cves': 0,
            'api_calls': 0,
            'api_errors': 0,
            'start_time': datetime.now(),
            'checkpoints': []
        }

    def close(self):
        self.driver.close()

    def get_all_cve_ids(self) -> List[str]:
        """Fetch all CVE IDs from Neo4j"""
        logger.info("Fetching all CVE IDs from Neo4j...")
        with self.driver.session() as session:
            result = session.run("""
                MATCH (cve:CVE)
                WHERE cve.id IS NOT NULL
                RETURN cve.id AS cve_id
                ORDER BY cve.id
            """)
            cve_ids = [record['cve_id'] for record in result if record['cve_id'] is not None]
            self.stats['total_cves'] = len(cve_ids)
            logger.info(f"Found {len(cve_ids)} CVEs to enrich (filtered NULL IDs)")
            return cve_ids

    def fetch_epss_scores(self, cve_ids: List[str]) -> Dict[str, Tuple[float, float]]:
        """Fetch EPSS scores from FIRST.org API with retry logic"""
        epss_data = {}

        for attempt in range(MAX_RETRIES):
            try:
                self.stats['api_calls'] += 1

                # Build query parameters
                params = {'cve': ','.join(cve_ids)}

                logger.info(f"API call {self.stats['api_calls']}: Fetching EPSS for {len(cve_ids)} CVEs (attempt {attempt + 1}/{MAX_RETRIES})")

                response = requests.get(EPSS_API_BASE, params=params, timeout=30)
                response.raise_for_status()

                data = response.json()

                if data.get('status') == 'OK' and 'data' in data:
                    for entry in data['data']:
                        cve_id = entry.get('cve')
                        epss_score = float(entry.get('epss', 0.0))
                        epss_percentile = float(entry.get('percentile', 0.0))
                        epss_data[cve_id] = (epss_score, epss_percentile)

                    logger.info(f"Successfully fetched EPSS data for {len(epss_data)} CVEs")
                    return epss_data
                else:
                    logger.warning(f"Unexpected API response: {data.get('status')}")

            except requests.exceptions.RequestException as e:
                self.stats['api_errors'] += 1
                logger.error(f"API request failed (attempt {attempt + 1}/{MAX_RETRIES}): {str(e)}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    logger.error(f"Failed to fetch EPSS data after {MAX_RETRIES} attempts")

        return epss_data

    def update_neo4j_batch(self, epss_batch: Dict[str, Tuple[float, float]]) -> int:
        """Update Neo4j with EPSS scores in batch"""
        if not epss_batch:
            return 0

        # Prepare data for UNWIND
        batch_data = [
            {
                'cve_id': cve_id,
                'epss_score': score,
                'epss_percentile': percentile
            }
            for cve_id, (score, percentile) in epss_batch.items()
        ]

        with self.driver.session() as session:
            result = session.run("""
                UNWIND $batch AS item
                MATCH (cve:CVE {id: item.cve_id})
                SET cve.epss_score = item.epss_score,
                    cve.epss_percentile = item.epss_percentile,
                    cve.epss_updated = datetime()
                RETURN count(cve) AS updated_count
            """, batch=batch_data)

            updated_count = result.single()['updated_count']
            return updated_count

    def save_checkpoint(self, processed_count: int):
        """Save checkpoint to enable recovery"""
        checkpoint = {
            'processed_count': processed_count,
            'enriched_count': self.stats['enriched_cves'],
            'timestamp': datetime.now().isoformat(),
            'api_calls': self.stats['api_calls']
        }
        self.stats['checkpoints'].append(checkpoint)

        checkpoint_file = f'/tmp/epss_checkpoint_{processed_count}.json'
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)

        logger.info(f"Checkpoint saved: {processed_count} CVEs processed")

    def run_enrichment(self):
        """Main enrichment execution"""
        logger.info("=" * 80)
        logger.info("PHASE 1 DAY 1: EPSS ENRICHMENT - STARTING")
        logger.info("=" * 80)

        # Get all CVE IDs
        all_cve_ids = self.get_all_cve_ids()

        if not all_cve_ids:
            logger.error("No CVEs found in database!")
            return

        total_cves = len(all_cve_ids)
        processed_count = 0
        neo4j_batch = {}

        # Process in API batches of 1000
        for i in range(0, total_cves, API_BATCH_SIZE):
            batch_cve_ids = all_cve_ids[i:i + API_BATCH_SIZE]
            batch_num = (i // API_BATCH_SIZE) + 1
            total_batches = (total_cves + API_BATCH_SIZE - 1) // API_BATCH_SIZE

            logger.info(f"\n--- Processing API Batch {batch_num}/{total_batches} ({len(batch_cve_ids)} CVEs) ---")

            # Fetch EPSS scores
            epss_data = self.fetch_epss_scores(batch_cve_ids)

            # Add to Neo4j batch
            neo4j_batch.update(epss_data)
            processed_count += len(batch_cve_ids)

            # Update Neo4j when we reach NEO4J_BATCH_SIZE or end of data
            if len(neo4j_batch) >= NEO4J_BATCH_SIZE or i + API_BATCH_SIZE >= total_cves:
                logger.info(f"Updating Neo4j with {len(neo4j_batch)} CVEs...")
                updated_count = self.update_neo4j_batch(neo4j_batch)
                self.stats['enriched_cves'] += updated_count
                self.stats['failed_cves'] += len(neo4j_batch) - updated_count

                logger.info(f"Neo4j update complete: {updated_count} CVEs enriched")
                neo4j_batch = {}

            # Checkpoint every CHECKPOINT_INTERVAL CVEs
            if processed_count % CHECKPOINT_INTERVAL == 0:
                self.save_checkpoint(processed_count)

            # Progress report
            progress_pct = (processed_count / total_cves) * 100
            logger.info(f"Progress: {processed_count}/{total_cves} CVEs ({progress_pct:.1f}%)")

            # Rate limiting (1 second between API calls)
            time.sleep(1)

        # Final checkpoint
        self.save_checkpoint(processed_count)

        # Calculate final statistics
        self.stats['end_time'] = datetime.now()
        self.stats['duration'] = (self.stats['end_time'] - self.stats['start_time']).total_seconds()

        self.generate_report()

    def generate_report(self):
        """Generate final enrichment report"""
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 1 DAY 1: EPSS ENRICHMENT - COMPLETE")
        logger.info("=" * 80)

        # Get enrichment statistics
        with self.driver.session() as session:
            result = session.run("""
                MATCH (cve:CVE)
                WHERE cve.epss_score IS NOT NULL
                RETURN
                    count(cve) AS enriched_count,
                    avg(cve.epss_score) AS avg_epss,
                    min(cve.epss_score) AS min_epss,
                    max(cve.epss_score) AS max_epss,
                    avg(cve.epss_percentile) AS avg_percentile
            """)
            db_stats = result.single()

        coverage_pct = (db_stats['enriched_count'] / self.stats['total_cves']) * 100

        report = f"""
EPSS ENRICHMENT REPORT
=====================

Execution Summary:
- Total CVEs in Database: {self.stats['total_cves']:,}
- CVEs Enriched: {db_stats['enriched_count']:,}
- Coverage: {coverage_pct:.2f}%
- Failed CVEs: {self.stats['failed_cves']:,}

EPSS Statistics:
- Average EPSS Score: {db_stats['avg_epss']:.6f}
- Min EPSS Score: {db_stats['min_epss']:.6f}
- Max EPSS Score: {db_stats['max_epss']:.6f}
- Average Percentile: {db_stats['avg_percentile']:.2f}

Performance:
- Total API Calls: {self.stats['api_calls']:,}
- API Errors: {self.stats['api_errors']:,}
- Execution Time: {self.stats['duration']:.2f} seconds ({self.stats['duration']/60:.2f} minutes)
- CVEs per Second: {self.stats['total_cves']/self.stats['duration']:.2f}
- Checkpoints Created: {len(self.stats['checkpoints'])}

Status: {'SUCCESS' if coverage_pct > 99 else 'PARTIAL SUCCESS'}
"""

        logger.info(report)

        # Save report to file
        report_file = '/tmp/epss_enrichment_report.txt'
        with open(report_file, 'w') as f:
            f.write(report)

        logger.info(f"\nReport saved to: {report_file}")
        logger.info(f"Error log: /tmp/epss_enrichment_errors.log")

        return report

def main():
    """Main execution function"""
    enrichment = EPSSEnrichment()
    try:
        enrichment.run_enrichment()
    except Exception as e:
        logger.error(f"Fatal error during enrichment: {str(e)}", exc_info=True)
        raise
    finally:
        enrichment.close()

if __name__ == "__main__":
    main()
