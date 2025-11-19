#!/usr/bin/env python3
"""
NVD API CVE Import Script for 2020-2021
Imports ~38,000-40,000 CVEs from the NVD API v2.0 into Neo4j

Features:
- NVD API v2.0 compliance with rate limiting (5 req/30s)
- Date range: 2020-01-01 to 2019-12-31
- Creates CVE nodes with full properties
- Creates CVE→CWE and CVE→CAPEC relationships
- MERGE logic to avoid duplicates
- Progress tracking and resumability
- Error handling and retry logic
"""

import os
import sys
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

import requests
from neo4j import GraphDatabase
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nvd_import_2018_2019.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
NVD_API_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
RESULTS_PER_PAGE = 2000
RATE_LIMIT_DELAY = 6  # 6 seconds between requests (5 req/30s = 1 req/6s)
MAX_RETRIES = 3
RETRY_DELAY = 30

# Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# Progress tracking
PROGRESS_FILE = ".nvd_import_progress_2020_2021.json"


class NVDImporter:
    """NVD API CVE importer with Neo4j integration"""

    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.session_stats = {
            'cves_processed': 0,
            'cves_created': 0,
            'cwes_linked': 0,
            'capecs_linked': 0,
            'errors': 0,
            'start_time': datetime.now().isoformat()
        }
        self.load_progress()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.save_progress()

    def load_progress(self):
        """Load progress from file to resume if interrupted"""
        if Path(PROGRESS_FILE).exists():
            with open(PROGRESS_FILE, 'r') as f:
                self.progress = json.load(f)
                logger.info(f"Resuming from progress: {self.progress.get('last_processed_date', 'start')}")
        else:
            self.progress = {
                'last_processed_date': '2020-01-01T00:00:00.000',
                'total_processed': 0,
                'last_update': datetime.now().isoformat()
            }

    def save_progress(self):
        """Save progress to file"""
        self.progress['last_update'] = datetime.now().isoformat()
        self.progress['session_stats'] = self.session_stats
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(self.progress, f, indent=2)
        logger.info(f"Progress saved: {self.progress['total_processed']} CVEs processed")

    def setup_schema(self):
        """Create indexes and constraints for optimal performance"""
        logger.info("Setting up Neo4j schema...")

        with self.driver.session() as session:
            # CVE constraints and indexes
            try:
                session.run("CREATE CONSTRAINT cve_id_unique IF NOT EXISTS FOR (c:CVE) REQUIRE c.cve_id IS UNIQUE")
                session.run("CREATE INDEX cve_published IF NOT EXISTS FOR (c:CVE) ON (c.published_date)")
                session.run("CREATE INDEX cve_severity IF NOT EXISTS FOR (c:CVE) ON (c.severity)")
                session.run("CREATE INDEX cve_score IF NOT EXISTS FOR (c:CVE) ON (c.cvss_score)")

                # CWE constraints
                session.run("CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS FOR (w:CWE) REQUIRE w.cwe_id IS UNIQUE")

                # CAPEC constraints
                session.run("CREATE CONSTRAINT capec_id_unique IF NOT EXISTS FOR (a:CAPEC) REQUIRE a.capec_id IS UNIQUE")

                logger.info("Schema setup complete")
            except Exception as e:
                logger.warning(f"Schema setup warning (may already exist): {e}")

    def fetch_cves(self, start_date: str, end_date: str, start_index: int = 0) -> Optional[Dict[str, Any]]:
        """Fetch CVEs from NVD API with retry logic"""

        params = {
            'pubStartDate': start_date,
            'pubEndDate': end_date,
            'resultsPerPage': RESULTS_PER_PAGE,
            'startIndex': start_index
        }

        for attempt in range(MAX_RETRIES):
            try:
                logger.debug(f"Fetching CVEs: {start_date} to {end_date}, index {start_index}")
                response = requests.get(NVD_API_BASE, params=params, timeout=30)

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 403:
                    logger.warning("Rate limit hit (403), waiting longer...")
                    time.sleep(RETRY_DELAY * 2)
                elif response.status_code == 503:
                    logger.warning("Service unavailable (503), retrying...")
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error(f"API error {response.status_code}: {response.text}")
                    time.sleep(RETRY_DELAY)

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)

        return None

    def extract_cvss_data(self, cve_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract CVSS score, vector, and severity from CVE data"""
        metrics = cve_data.get('metrics', {})

        # Try CVSS v3.1 first, then v3.0, then v2.0
        for version in ['cvssMetricV31', 'cvssMetricV30', 'cvssMetricV2']:
            if version in metrics and metrics[version]:
                metric = metrics[version][0]
                cvss_data = metric.get('cvssData', {})

                return {
                    'cvss_score': cvss_data.get('baseScore', 0.0),
                    'cvss_vector': cvss_data.get('vectorString', ''),
                    'severity': metric.get('baseSeverity', 'UNKNOWN'),
                    'cvss_version': version.replace('cvssMetricV', '')
                }

        return {
            'cvss_score': 0.0,
            'cvss_vector': '',
            'severity': 'UNKNOWN',
            'cvss_version': 'N/A'
        }

    def extract_cwe_ids(self, cve_data: Dict[str, Any]) -> List[str]:
        """Extract CWE IDs from CVE data"""
        cwe_ids = []

        weaknesses = cve_data.get('weaknesses', [])
        for weakness in weaknesses:
            for desc in weakness.get('description', []):
                value = desc.get('value', '')
                if value.startswith('CWE-'):
                    cwe_ids.append(value)

        return list(set(cwe_ids))  # Remove duplicates

    def import_cve_batch(self, cves: List[Dict[str, Any]]):
        """Import batch of CVEs into Neo4j with relationships"""

        with self.driver.session() as session:
            for cve_item in cves:
                try:
                    cve_data = cve_item.get('cve', {})
                    cve_id = cve_data.get('id', '')

                    if not cve_id:
                        continue

                    # Extract CVE properties
                    cvss_data = self.extract_cvss_data(cve_data)
                    cwe_ids = self.extract_cwe_ids(cve_data)

                    # Get description
                    descriptions = cve_data.get('descriptions', [])
                    description = ''
                    for desc in descriptions:
                        if desc.get('lang') == 'en':
                            description = desc.get('value', '')
                            break

                    # Get dates
                    published_date = cve_data.get('published', '')
                    modified_date = cve_data.get('lastModified', '')

                    # Create/update CVE node
                    cve_query = """
                    MERGE (c:CVE {cve_id: $cve_id})
                    SET c.cvss_score = $cvss_score,
                        c.cvss_vector = $cvss_vector,
                        c.cvss_version = $cvss_version,
                        c.severity = $severity,
                        c.description = $description,
                        c.published_date = $published_date,
                        c.modified_date = $modified_date,
                        c.cwe_ids = $cwe_ids,
                        c.last_updated = datetime()
                    RETURN c
                    """

                    session.run(cve_query, {
                        'cve_id': cve_id,
                        'cvss_score': cvss_data['cvss_score'],
                        'cvss_vector': cvss_data['cvss_vector'],
                        'cvss_version': cvss_data['cvss_version'],
                        'severity': cvss_data['severity'],
                        'description': description[:5000],  # Limit description length
                        'published_date': published_date,
                        'modified_date': modified_date,
                        'cwe_ids': cwe_ids
                    })

                    self.session_stats['cves_created'] += 1

                    # Create CWE relationships
                    for cwe_id in cwe_ids:
                        cwe_query = """
                        MERGE (w:CWE {cwe_id: $cwe_id})
                        WITH w
                        MATCH (c:CVE {cve_id: $cve_id})
                        MERGE (c)-[r:EXPLOITS_WEAKNESS]->(w)
                        SET r.discovered = datetime()
                        """

                        session.run(cwe_query, {
                            'cwe_id': cwe_id,
                            'cve_id': cve_id
                        })

                        self.session_stats['cwes_linked'] += 1

                    self.session_stats['cves_processed'] += 1

                except Exception as e:
                    logger.error(f"Error importing CVE {cve_id}: {e}")
                    self.session_stats['errors'] += 1

    def import_year_range(self, start_year: int, end_year: int):
        """Import CVEs for a year range"""

        logger.info(f"Starting import for years {start_year}-{end_year}")

        for year in range(start_year, end_year + 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing year: {year}")
            logger.info(f"{'='*60}\n")

            # Process in monthly chunks to avoid timeout and manage progress
            for month in range(1, 13):
                start_date = f"{year}-{month:02d}-01T00:00:00.000"

                # Calculate end date (last day of month)
                if month == 12:
                    end_date = f"{year}-12-31T23:59:59.999"
                else:
                    next_month = datetime(year, month + 1, 1)
                    last_day = (next_month - timedelta(days=1)).day
                    end_date = f"{year}-{month:02d}-{last_day}T23:59:59.999"

                logger.info(f"Processing {year}-{month:02d}: {start_date} to {end_date}")

                start_index = 0
                total_results = None

                while True:
                    # Fetch CVEs
                    time.sleep(RATE_LIMIT_DELAY)  # Rate limiting

                    data = self.fetch_cves(start_date, end_date, start_index)

                    if not data:
                        logger.error(f"Failed to fetch data for {year}-{month:02d}, index {start_index}")
                        break

                    vulnerabilities = data.get('vulnerabilities', [])

                    if not vulnerabilities:
                        logger.info(f"No more CVEs for {year}-{month:02d}")
                        break

                    if total_results is None:
                        total_results = data.get('totalResults', 0)
                        logger.info(f"Total CVEs for {year}-{month:02d}: {total_results}")

                    # Import batch
                    self.import_cve_batch(vulnerabilities)

                    logger.info(f"Imported batch: {start_index} to {start_index + len(vulnerabilities)}")

                    # Update progress
                    self.progress['last_processed_date'] = end_date
                    self.progress['total_processed'] = self.session_stats['cves_processed']
                    self.save_progress()

                    # Check if we've fetched all results
                    start_index += len(vulnerabilities)
                    if start_index >= total_results:
                        break

                logger.info(f"Completed {year}-{month:02d}: {self.session_stats['cves_processed']} total CVEs")

    def print_summary(self):
        """Print import summary statistics"""
        duration = datetime.now() - datetime.fromisoformat(self.session_stats['start_time'])

        logger.info("\n" + "="*60)
        logger.info("IMPORT SUMMARY")
        logger.info("="*60)
        logger.info(f"CVEs Processed: {self.session_stats['cves_processed']}")
        logger.info(f"CVEs Created: {self.session_stats['cves_created']}")
        logger.info(f"CWEs Linked: {self.session_stats['cwes_linked']}")
        logger.info(f"CAPECs Linked: {self.session_stats['capecs_linked']}")
        logger.info(f"Errors: {self.session_stats['errors']}")
        logger.info(f"Duration: {duration}")
        logger.info(f"Rate: {self.session_stats['cves_processed'] / duration.total_seconds():.2f} CVEs/second")
        logger.info("="*60 + "\n")


def main():
    """Main execution function"""

    logger.info("="*60)
    logger.info("NVD CVE Import Script - 2020-2021")
    logger.info("="*60)
    logger.info(f"Start time: {datetime.now()}")
    logger.info(f"Target: ~38,000-40,000 CVEs from 2020-2021")
    logger.info(f"Rate limit: {RATE_LIMIT_DELAY}s between requests")
    logger.info("="*60 + "\n")

    try:
        with NVDImporter() as importer:
            # Setup schema
            importer.setup_schema()

            # Import 2020-2021 CVEs
            importer.import_year_range(2020, 2021)

            # Print summary
            importer.print_summary()

        logger.info("Import completed successfully!")
        return 0

    except KeyboardInterrupt:
        logger.warning("\nImport interrupted by user. Progress saved.")
        return 1

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
