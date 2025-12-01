#!/usr/bin/env python3
"""
NVD CVE Importer - Complete implementation for importing CVE data from NVD API 2.0
Handles rate limiting, incremental updates, CPE/CWE linking, and error recovery.
"""

import os
import sys
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import requests
from neo4j import GraphDatabase, Driver
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nvd_importer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class ImportMetrics:
    """Track import statistics"""
    total_cves: int = 0
    new_cves: int = 0
    updated_cves: int = 0
    errors: int = 0
    start_time: float = 0
    end_time: float = 0

    def duration_seconds(self) -> float:
        return self.end_time - self.start_time if self.end_time else 0


class NVDImporter:
    """Import CVE data from NVD API 2.0 into Neo4j"""

    # NVD API 2.0 constants
    API_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    RATE_LIMIT_CALLS = 50
    RATE_LIMIT_PERIOD = 30  # seconds
    MAX_RESULTS_PER_PAGE = 2000

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str,
                 api_key: Optional[str] = None):
        """
        Initialize NVD importer

        Args:
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
            api_key: NVD API key (optional but recommended for higher rate limits)
        """
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.api_key = api_key
        self.metrics = ImportMetrics()
        self._verify_connection()
        self._create_indexes()

    def _verify_connection(self):
        """Verify Neo4j connection"""
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                result.single()
            logger.info("Neo4j connection verified")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    def _create_indexes(self):
        """Create necessary indexes and constraints"""
        indexes = [
            "CREATE CONSTRAINT cve_id IF NOT EXISTS FOR (c:CVE) REQUIRE c.id IS UNIQUE",
            "CREATE INDEX cve_published IF NOT EXISTS FOR (c:CVE) ON (c.published)",
            "CREATE INDEX cve_modified IF NOT EXISTS FOR (c:CVE) ON (c.lastModified)",
            "CREATE INDEX cve_severity IF NOT EXISTS FOR (c:CVE) ON (c.baseSeverity)",
            "CREATE CONSTRAINT cpe_uri IF NOT EXISTS FOR (c:CPE) REQUIRE c.uri IS UNIQUE",
            "CREATE CONSTRAINT cwe_id IF NOT EXISTS FOR (c:CWE) REQUIRE c.id IS UNIQUE",
        ]

        with self.driver.session() as session:
            for index_query in indexes:
                try:
                    session.run(index_query)
                    logger.info(f"Created index/constraint: {index_query[:50]}...")
                except Exception as e:
                    logger.warning(f"Index creation warning: {e}")

    @sleep_and_retry
    @limits(calls=RATE_LIMIT_CALLS, period=RATE_LIMIT_PERIOD)
    def _call_nvd_api(self, params: Dict[str, Any]) -> Dict:
        """
        Call NVD API with rate limiting

        Args:
            params: API query parameters

        Returns:
            JSON response data
        """
        headers = {}
        if self.api_key:
            headers['apiKey'] = self.api_key

        try:
            response = requests.get(
                self.API_BASE_URL,
                params=params,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise

    def fetch_cves(self, last_modified_start_date: Optional[str] = None,
                   last_modified_end_date: Optional[str] = None,
                   published_start_date: Optional[str] = None,
                   published_end_date: Optional[str] = None) -> List[Dict]:
        """
        Fetch CVEs from NVD API

        Args:
            last_modified_start_date: ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sss)
            last_modified_end_date: ISO 8601 format
            published_start_date: ISO 8601 format
            published_end_date: ISO 8601 format

        Returns:
            List of CVE dictionaries
        """
        all_cves = []
        start_index = 0

        params = {
            'resultsPerPage': self.MAX_RESULTS_PER_PAGE,
            'startIndex': start_index
        }

        if last_modified_start_date:
            params['lastModStartDate'] = last_modified_start_date
        if last_modified_end_date:
            params['lastModEndDate'] = last_modified_end_date
        if published_start_date:
            params['pubStartDate'] = published_start_date
        if published_end_date:
            params['pubEndDate'] = published_end_date

        logger.info(f"Fetching CVEs with params: {params}")

        # Get first page to determine total
        first_response = self._call_nvd_api(params)
        total_results = first_response.get('totalResults', 0)

        logger.info(f"Total CVEs to fetch: {total_results}")

        if total_results == 0:
            return []

        # Process first page
        all_cves.extend(first_response.get('vulnerabilities', []))

        # Fetch remaining pages
        with tqdm(total=total_results, desc="Fetching CVEs") as pbar:
            pbar.update(len(all_cves))

            while start_index + self.MAX_RESULTS_PER_PAGE < total_results:
                start_index += self.MAX_RESULTS_PER_PAGE
                params['startIndex'] = start_index

                response = self._call_nvd_api(params)
                cves = response.get('vulnerabilities', [])
                all_cves.extend(cves)
                pbar.update(len(cves))

        logger.info(f"Fetched {len(all_cves)} CVEs from NVD")
        return all_cves

    def _parse_cvss_metrics(self, cve_item: Dict) -> Dict:
        """Parse CVSS metrics from CVE item"""
        metrics = {}

        # Try CVSS v3.1 first, then v3.0, then v2.0
        for version in ['cvssMetricV31', 'cvssMetricV30', 'cvssMetricV2']:
            metric_list = cve_item.get('cve', {}).get('metrics', {}).get(version, [])
            if metric_list:
                cvss_data = metric_list[0].get('cvssData', {})
                metrics.update({
                    'cvssVersion': cvss_data.get('version'),
                    'baseScore': cvss_data.get('baseScore'),
                    'baseSeverity': cvss_data.get('baseSeverity'),
                    'vectorString': cvss_data.get('vectorString'),
                    'attackVector': cvss_data.get('attackVector'),
                    'attackComplexity': cvss_data.get('attackComplexity'),
                    'privilegesRequired': cvss_data.get('privilegesRequired'),
                    'userInteraction': cvss_data.get('userInteraction'),
                    'scope': cvss_data.get('scope'),
                    'confidentialityImpact': cvss_data.get('confidentialityImpact'),
                    'integrityImpact': cvss_data.get('integrityImpact'),
                    'availabilityImpact': cvss_data.get('availabilityImpact'),
                    'exploitabilityScore': metric_list[0].get('exploitabilityScore'),
                    'impactScore': metric_list[0].get('impactScore')
                })
                break

        return metrics

    def _extract_cpe_matches(self, cve_item: Dict) -> List[str]:
        """Extract CPE URIs from CVE configurations"""
        cpe_matches = []

        configurations = cve_item.get('cve', {}).get('configurations', [])
        for config in configurations:
            for node in config.get('nodes', []):
                for cpe_match in node.get('cpeMatch', []):
                    if cpe_match.get('vulnerable', True):
                        cpe_uri = cpe_match.get('criteria')
                        if cpe_uri:
                            cpe_matches.append(cpe_uri)

        return list(set(cpe_matches))

    def _extract_cwe_ids(self, cve_item: Dict) -> List[str]:
        """Extract CWE IDs from CVE weaknesses"""
        cwe_ids = []

        weaknesses = cve_item.get('cve', {}).get('weaknesses', [])
        for weakness in weaknesses:
            for desc in weakness.get('description', []):
                cwe_value = desc.get('value', '')
                if cwe_value.startswith('CWE-'):
                    cwe_ids.append(cwe_value)

        return list(set(cwe_ids))

    def _extract_references(self, cve_item: Dict) -> List[Dict[str, str]]:
        """Extract reference URLs and tags"""
        references = []

        refs = cve_item.get('cve', {}).get('references', [])
        for ref in refs:
            references.append({
                'url': ref.get('url', ''),
                'source': ref.get('source', ''),
                'tags': ','.join(ref.get('tags', []))
            })

        return references

    def batch_import(self, cves: List[Dict], batch_size: int = 1000):
        """
        Import CVEs in batches using UNWIND

        Args:
            cves: List of CVE dictionaries
            batch_size: Number of CVEs per batch
        """
        if not cves:
            logger.warning("No CVEs to import")
            return

        # Process CVE data
        processed_cves = []
        for cve_item in cves:
            try:
                cve = cve_item.get('cve', {})
                cve_id = cve.get('id')

                if not cve_id:
                    continue

                # Get description
                descriptions = cve.get('descriptions', [])
                description = next((d['value'] for d in descriptions if d.get('lang') == 'en'), '')

                # Parse metrics
                metrics = self._parse_cvss_metrics(cve_item)

                # Extract relationships
                cpe_matches = self._extract_cpe_matches(cve_item)
                cwe_ids = self._extract_cwe_ids(cve_item)
                references = self._extract_references(cve_item)

                processed_cves.append({
                    'id': cve_id,
                    'description': description,
                    'published': cve.get('published'),
                    'lastModified': cve.get('lastModified'),
                    'vulnStatus': cve.get('vulnStatus'),
                    'cpeMatches': cpe_matches,
                    'cweIds': cwe_ids,
                    'references': references,
                    **metrics
                })

            except Exception as e:
                logger.error(f"Error processing CVE: {e}")
                self.metrics.errors += 1

        # Import in batches
        cypher = """
        UNWIND $batch as cve
        MERGE (c:CVE {id: cve.id})
        SET c.description = cve.description,
            c.published = datetime(cve.published),
            c.lastModified = datetime(cve.lastModified),
            c.vulnStatus = cve.vulnStatus,
            c.cvssVersion = cve.cvssVersion,
            c.baseScore = cve.baseScore,
            c.baseSeverity = cve.baseSeverity,
            c.vectorString = cve.vectorString,
            c.attackVector = cve.attackVector,
            c.attackComplexity = cve.attackComplexity,
            c.privilegesRequired = cve.privilegesRequired,
            c.userInteraction = cve.userInteraction,
            c.scope = cve.scope,
            c.confidentialityImpact = cve.confidentialityImpact,
            c.integrityImpact = cve.integrityImpact,
            c.availabilityImpact = cve.availabilityImpact,
            c.exploitabilityScore = cve.exploitabilityScore,
            c.impactScore = cve.impactScore,
            c.lastImported = datetime()

        WITH c, cve
        UNWIND cve.cpeMatches as cpeUri
        MERGE (cpe:CPE {uri: cpeUri})
        MERGE (c)-[:AFFECTS]->(cpe)

        WITH c, cve
        UNWIND cve.cweIds as cweId
        MERGE (cwe:CWE {id: cweId})
        MERGE (c)-[:HAS_WEAKNESS]->(cwe)

        WITH c, cve
        UNWIND cve.references as ref
        MERGE (r:Reference {url: ref.url})
        SET r.source = ref.source,
            r.tags = ref.tags
        MERGE (c)-[:HAS_REFERENCE]->(r)

        RETURN count(c) as imported
        """

        with self.driver.session() as session:
            total_batches = (len(processed_cves) + batch_size - 1) // batch_size

            with tqdm(total=len(processed_cves), desc="Importing CVEs") as pbar:
                for i in range(0, len(processed_cves), batch_size):
                    batch = processed_cves[i:i + batch_size]

                    try:
                        result = session.run(cypher, batch=batch)
                        count = result.single()['imported']
                        self.metrics.new_cves += count
                        pbar.update(len(batch))
                    except Exception as e:
                        logger.error(f"Batch import failed: {e}")
                        self.metrics.errors += len(batch)

        logger.info(f"Import complete: {self.metrics.new_cves} CVEs processed")

    def incremental_update(self, days_back: int = 7):
        """
        Perform incremental update for CVEs modified in last N days

        Args:
            days_back: Number of days to look back
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days_back)

        start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S.000')
        end_str = end_date.strftime('%Y-%m-%dT%H:%M:%S.000')

        logger.info(f"Incremental update from {start_str} to {end_str}")

        cves = self.fetch_cves(
            last_modified_start_date=start_str,
            last_modified_end_date=end_str
        )

        self.batch_import(cves)

    def full_import(self, year: Optional[int] = None):
        """
        Perform full import of all CVEs or specific year

        Args:
            year: Specific year to import (None for all)
        """
        if year:
            start_date = f"{year}-01-01T00:00:00.000"
            end_date = f"{year}-12-31T23:59:59.999"
            logger.info(f"Full import for year {year}")

            cves = self.fetch_cves(
                published_start_date=start_date,
                published_end_date=end_date
            )
        else:
            logger.info("Full import of all CVEs")
            cves = self.fetch_cves()

        self.batch_import(cves)

    def get_metrics(self) -> ImportMetrics:
        """Return import metrics"""
        return self.metrics

    def close(self):
        """Close Neo4j driver"""
        self.driver.close()
        logger.info("NVD importer closed")


def main():
    """Main execution function"""
    # Configuration from environment or defaults
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')
    NVD_API_KEY = os.getenv('NVD_API_KEY')

    if not NVD_API_KEY:
        logger.warning("NVD_API_KEY not set - using lower rate limits")

    # Initialize importer
    importer = NVDImporter(
        neo4j_uri=NEO4J_URI,
        neo4j_user=NEO4J_USER,
        neo4j_password=NEO4J_PASSWORD,
        api_key=NVD_API_KEY
    )

    try:
        # Start metrics tracking
        importer.metrics.start_time = time.time()

        # Perform incremental update (last 7 days)
        logger.info("Starting incremental update...")
        importer.incremental_update(days_back=7)

        # End metrics tracking
        importer.metrics.end_time = time.time()

        # Print metrics
        metrics = importer.get_metrics()
        logger.info(f"""
        Import Metrics:
        - Duration: {metrics.duration_seconds():.2f} seconds
        - CVEs Processed: {metrics.new_cves}
        - Errors: {metrics.errors}
        """)

    except Exception as e:
        logger.error(f"Import failed: {e}")
        sys.exit(1)
    finally:
        importer.close()


if __name__ == "__main__":
    main()
