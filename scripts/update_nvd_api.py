#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
NVD API Incremental Update Script
Created: 2025-11-28
Purpose: Fetch and load recent CVE updates from NVD API
Uses: Configured NVD API key from environment
═══════════════════════════════════════════════════════════════
"""

import os
import sys
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Generator
import requests
from neo4j import GraphDatabase
from dotenv import load_dotenv
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════

load_dotenv()

NVD_API_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_API_KEY = os.getenv("NVD_API_KEY")
RATE_LIMIT_DELAY = 0.6 if NVD_API_KEY else 6.0

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# ═══════════════════════════════════════════════════════════════
# NVD API Client
# ═══════════════════════════════════════════════════════════════

class NVDAPIClient:
    """Client for NVD API v2.0."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"apiKey": api_key})
        self.last_request_time = 0

    def _rate_limit(self):
        """Enforce rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - elapsed)
        self.last_request_time = time.time()

    def fetch_recent_cves(
        self,
        days_back: int = 7,
        results_per_page: int = 2000
    ) -> Generator[Dict, None, None]:
        """
        Fetch CVEs modified in the last N days.

        Args:
            days_back: Number of days to look back
            results_per_page: Results per API call (max 2000)

        Yields:
            CVE data from NVD API
        """
        start_date = datetime.now() - timedelta(days=days_back)

        params = {
            "resultsPerPage": min(results_per_page, 2000),
            "startIndex": 0,
            "lastModStartDate": start_date.strftime("%Y-%m-%dT%H:%M:%S.000")
        }

        total_results = None

        with tqdm(desc="Fetching recent CVEs", unit=" CVEs") as pbar:
            while True:
                self._rate_limit()

                try:
                    response = self.session.get(NVD_API_BASE_URL, params=params, timeout=30)
                    response.raise_for_status()
                    data = response.json()

                    if total_results is None:
                        total_results = data.get("totalResults", 0)
                        pbar.total = total_results
                        logger.info(f"Found {total_results} CVEs modified in last {days_back} days")

                    vulnerabilities = data.get("vulnerabilities", [])
                    if not vulnerabilities:
                        break

                    for vuln in vulnerabilities:
                        yield vuln
                        pbar.update(1)

                    params["startIndex"] += len(vulnerabilities)
                    if params["startIndex"] >= total_results:
                        break

                except requests.exceptions.RequestException as e:
                    logger.error(f"API request failed: {e}")
                    break

    def parse_cve(self, vuln_data: Dict) -> Optional[Dict]:
        """Parse CVE data from NVD API response."""
        try:
            cve = vuln_data.get("cve", {})
            cve_id = cve.get("id")

            descriptions = cve.get("descriptions", [])
            description = next(
                (d["value"] for d in descriptions if d.get("lang") == "en"),
                descriptions[0]["value"] if descriptions else "No description"
            )

            metrics = cve.get("metrics", {})
            cvss_v31 = metrics.get("cvssMetricV31", [{}])[0].get("cvssData", {})
            cvss_v30 = metrics.get("cvssMetricV30", [{}])[0].get("cvssData", {})
            cvss = cvss_v31 if cvss_v31 else cvss_v30

            weaknesses = cve.get("weaknesses", [])
            cwe_ids = []
            for weakness in weaknesses:
                for desc in weakness.get("description", []):
                    if desc.get("lang") == "en":
                        cwe_ids.append(desc.get("value"))

            return {
                'cveId': cve_id,
                'description': description,
                'publishedDate': cve.get("published", "")[:10],
                'lastModifiedDate': cve.get("lastModified", "")[:10],
                'cvssV3Vector': cvss.get("vectorString"),
                'cvssV3BaseScore': cvss.get("baseScore"),
                'cvssV3Severity': cvss.get("baseSeverity"),
                'exploitabilityScore': metrics.get("cvssMetricV31", [{}])[0].get("exploitabilityScore"),
                'impactScore': metrics.get("cvssMetricV31", [{}])[0].get("impactScore"),
                'cwe_ids': cwe_ids
            }

        except Exception as e:
            logger.error(f"Failed to parse CVE: {e}")
            return None

# ═══════════════════════════════════════════════════════════════
# Neo4j Loader
# ═══════════════════════════════════════════════════════════════

class CVELoader:
    """Load CVE data into Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_cve(self, cve_data: Dict) -> bool:
        """Load or update single CVE."""
        query = """
        MERGE (cve:CVE {cveId: $cveId})
        SET cve.description = $description,
            cve.publishedDate = date($publishedDate),
            cve.lastModifiedDate = date($lastModifiedDate),
            cve.cvssV3Vector = $cvssV3Vector,
            cve.cvssV3BaseScore = $cvssV3BaseScore,
            cve.cvssV3Severity = $cvssV3Severity,
            cve.exploitabilityScore = $exploitabilityScore,
            cve.impactScore = $impactScore,
            cve.is_shared = true,
            cve.customer_namespace = 'shared:nvd',
            cve.lastUpdated = datetime()

        WITH cve
        UNWIND $cwe_ids AS cwe_id
        MERGE (cwe:CWE {cweId: cwe_id})
        ON CREATE SET
          cwe.customer_namespace = 'shared:cwe',
          cwe.is_shared = true
        MERGE (cve)-[:IS_WEAKNESS_TYPE]->(cwe)

        RETURN cve.cveId AS cveId
        """

        try:
            with self.driver.session() as session:
                result = session.run(query, **cve_data)
                return True

        except Exception as e:
            logger.error(f"Failed to load {cve_data['cveId']}: {e}")
            return False

# ═══════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════

def main():
    """Main execution function."""
    if not NVD_API_KEY:
        logger.warning("NVD_API_KEY not set - using slow rate limit (6 seconds per request)")
    else:
        logger.info("Using NVD_API_KEY - fast rate limit (0.6 seconds per request)")

    days_back = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    logger.info(f"Fetching CVEs modified in last {days_back} days")

    client = NVDAPIClient(api_key=NVD_API_KEY)
    loader = CVELoader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        successes = 0
        total = 0

        for vuln_data in client.fetch_recent_cves(days_back=days_back):
            cve_data = client.parse_cve(vuln_data)
            if cve_data:
                total += 1
                if loader.load_cve(cve_data):
                    successes += 1

        logger.info(f"Updated {successes}/{total} CVEs successfully")

        # Verify count
        with loader.driver.session() as session:
            result = session.run("MATCH (c:CVE) RETURN count(c) AS count")
            count = result.single()['count']
            logger.info(f"Total CVEs in database: {count}")

    finally:
        loader.close()

if __name__ == "__main__":
    main()
