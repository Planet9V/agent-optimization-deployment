#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
NVD API Connector - CVE/CPE/CVSS Data Ingestion
Phase 1: Core Schema Foundation
Created: 2025-10-29
═══════════════════════════════════════════════════════════════

Purpose:
  - Fetch CVE data from NIST National Vulnerability Database (NVD) API 2.0
  - Transform JSON to Neo4j Cypher statements
  - Handle rate limiting (50 requests per 30 seconds with API key)
  - Support incremental updates (last modified date filtering)

API Documentation:
  https://nvd.nist.gov/developers/vulnerabilities

Dependencies:
  pip install requests neo4j python-dotenv tqdm

Environment Variables:
  NVD_API_KEY: NIST NVD API key (optional, increases rate limit)
  NEO4J_URI: Neo4j connection URI (default: bolt://localhost:7687)
  NEO4J_USER: Neo4j username (default: neo4j)
  NEO4J_PASSWORD: Neo4j password
"""

import os
import sys
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Generator
from dataclasses import dataclass, asdict

import requests
from neo4j import GraphDatabase
from dotenv import load_dotenv
from tqdm import tqdm

# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# NVD API Configuration
NVD_API_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_API_KEY = os.getenv("NVD_API_KEY")
RATE_LIMIT_DELAY = 0.6 if NVD_API_KEY else 6.0  # seconds between requests

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# ═══════════════════════════════════════════════════════════════
# Data Models
# ═══════════════════════════════════════════════════════════════

@dataclass
class CVEMetadata:
    """CVE metadata matching Neo4j schema."""
    cveId: str
    description: str
    publishedDate: str
    lastModifiedDate: str
    cvssV3Vector: Optional[str]
    cvssV3BaseScore: Optional[float]
    cvssV3Severity: Optional[str]
    exploitabilityScore: Optional[float]
    impactScore: Optional[float]
    hasExploit: bool = False
    exploitMaturity: str = "NOT_DEFINED"
    is_shared: bool = True
    customer_namespace: str = "shared:nvd"

    # Additional metadata for correlation
    affected_cpes: List[str] = None
    cwe_ids: List[str] = None
    references: List[str] = None

    def __post_init__(self):
        if self.affected_cpes is None:
            self.affected_cpes = []
        if self.cwe_ids is None:
            self.cwe_ids = []
        if self.references is None:
            self.references = []

# ═══════════════════════════════════════════════════════════════
# NVD API Client
# ═══════════════════════════════════════════════════════════════

class NVDAPIClient:
    """Client for NIST NVD API 2.0."""

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

    def fetch_cves(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        results_per_page: int = 2000,
        cvss_v3_severity: Optional[str] = None
    ) -> Generator[Dict, None, None]:
        """
        Fetch CVEs from NVD API with pagination.

        Args:
            start_date: Filter by last modified date (start)
            end_date: Filter by last modified date (end)
            results_per_page: Number of results per API call (max 2000)
            cvss_v3_severity: Filter by CVSS v3 severity (LOW, MEDIUM, HIGH, CRITICAL)

        Yields:
            Dict: CVE data from NVD API
        """
        params = {
            "resultsPerPage": min(results_per_page, 2000),
            "startIndex": 0
        }

        if start_date:
            params["lastModStartDate"] = start_date.strftime("%Y-%m-%dT%H:%M:%S.000")
        if end_date:
            params["lastModEndDate"] = end_date.strftime("%Y-%m-%dT%H:%M:%S.000")
        if cvss_v3_severity:
            params["cvssV3Severity"] = cvss_v3_severity

        total_results = None

        with tqdm(desc="Fetching CVEs", unit=" CVEs") as pbar:
            while True:
                self._rate_limit()

                try:
                    response = self.session.get(NVD_API_BASE_URL, params=params, timeout=30)
                    response.raise_for_status()
                    data = response.json()

                    if total_results is None:
                        total_results = data.get("totalResults", 0)
                        pbar.total = total_results
                        logger.info(f"Total CVEs to fetch: {total_results}")

                    vulnerabilities = data.get("vulnerabilities", [])
                    if not vulnerabilities:
                        break

                    for vuln in vulnerabilities:
                        yield vuln
                        pbar.update(1)

                    # Check if more results available
                    params["startIndex"] += len(vulnerabilities)
                    if params["startIndex"] >= total_results:
                        break

                except requests.exceptions.RequestException as e:
                    logger.error(f"API request failed: {e}")
                    break

    def parse_cve(self, vuln_data: Dict) -> Optional[CVEMetadata]:
        """
        Parse NVD API CVE data into CVEMetadata object.

        Args:
            vuln_data: Raw vulnerability data from NVD API

        Returns:
            CVEMetadata object or None if parsing fails
        """
        try:
            cve = vuln_data.get("cve", {})
            cve_id = cve.get("id")

            # Extract description (prefer English)
            descriptions = cve.get("descriptions", [])
            description = next(
                (d["value"] for d in descriptions if d.get("lang") == "en"),
                descriptions[0]["value"] if descriptions else "No description available"
            )

            # Extract CVSS v3 metrics (prefer v3.1, fallback to v3.0)
            metrics = cve.get("metrics", {})
            cvss_v31 = metrics.get("cvssMetricV31", [{}])[0].get("cvssData", {})
            cvss_v30 = metrics.get("cvssMetricV30", [{}])[0].get("cvssData", {})
            cvss = cvss_v31 if cvss_v31 else cvss_v30

            cvss_vector = cvss.get("vectorString")
            cvss_base_score = cvss.get("baseScore")
            cvss_severity = cvss.get("baseSeverity")

            # Extract exploitability and impact scores
            exploitability = metrics.get("cvssMetricV31", [{}])[0].get("exploitabilityScore")
            impact = metrics.get("cvssMetricV31", [{}])[0].get("impactScore")

            # Extract CWE IDs
            weaknesses = cve.get("weaknesses", [])
            cwe_ids = []
            for weakness in weaknesses:
                for desc in weakness.get("description", []):
                    if desc.get("lang") == "en":
                        cwe_ids.append(desc.get("value"))

            # Extract CPE configurations (affected products)
            configurations = cve.get("configurations", [])
            affected_cpes = []
            for config in configurations:
                for node in config.get("nodes", []):
                    for cpe_match in node.get("cpeMatch", []):
                        if cpe_match.get("vulnerable"):
                            affected_cpes.append(cpe_match.get("criteria"))

            # Extract references
            references = [ref.get("url") for ref in cve.get("references", [])]

            return CVEMetadata(
                cveId=cve_id,
                description=description,
                publishedDate=cve.get("published", ""),
                lastModifiedDate=cve.get("lastModified", ""),
                cvssV3Vector=cvss_vector,
                cvssV3BaseScore=cvss_base_score,
                cvssV3Severity=cvss_severity,
                exploitabilityScore=exploitability,
                impactScore=impact,
                affected_cpes=affected_cpes,
                cwe_ids=cwe_ids,
                references=references
            )

        except Exception as e:
            logger.error(f"Failed to parse CVE: {e}")
            return None

# ═══════════════════════════════════════════════════════════════
# Neo4j Ingestion
# ═══════════════════════════════════════════════════════════════

class Neo4jCVEIngester:
    """Ingest CVE data into Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def ingest_cve(self, cve: CVEMetadata) -> bool:
        """
        Ingest single CVE into Neo4j.

        Returns:
            bool: True if successful, False otherwise
        """
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
            cve.hasExploit = $hasExploit,
            cve.exploitMaturity = $exploitMaturity,
            cve.is_shared = $is_shared,
            cve.customer_namespace = $customer_namespace

        // Create CWE relationships
        WITH cve
        UNWIND $cwe_ids AS cwe_id
        MERGE (cwe:CWE {cweId: cwe_id})
        MERGE (cve)-[:IS_WEAKNESS_TYPE]->(cwe)

        RETURN cve.cveId AS cveId
        """

        try:
            with self.driver.session() as session:
                # Convert dates to ISO format strings
                params = asdict(cve)
                params['publishedDate'] = cve.publishedDate[:10] if cve.publishedDate else None
                params['lastModifiedDate'] = cve.lastModifiedDate[:10] if cve.lastModifiedDate else None

                result = session.run(query, **params)
                record = result.single()
                return record is not None

        except Exception as e:
            logger.error(f"Failed to ingest CVE {cve.cveId}: {e}")
            return False

    def ingest_batch(self, cves: List[CVEMetadata], batch_size: int = 100):
        """Ingest CVEs in batches for better performance."""
        total = len(cves)
        successes = 0

        with tqdm(total=total, desc="Ingesting CVEs", unit=" CVEs") as pbar:
            for i in range(0, total, batch_size):
                batch = cves[i:i + batch_size]
                for cve in batch:
                    if self.ingest_cve(cve):
                        successes += 1
                    pbar.update(1)

        logger.info(f"Ingested {successes}/{total} CVEs successfully")
        return successes

# ═══════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════

def main():
    """Main execution function."""

    # Validate Neo4j credentials
    if not NEO4J_PASSWORD:
        logger.error("NEO4J_PASSWORD environment variable not set")
        sys.exit(1)

    # Initialize clients
    nvd_client = NVDAPIClient(api_key=NVD_API_KEY)
    neo4j_ingester = Neo4jCVEIngester(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Fetch CVEs from last 30 days (incremental update)
        start_date = datetime.now() - timedelta(days=30)

        logger.info(f"Fetching CVEs modified since {start_date.strftime('%Y-%m-%d')}")

        cves = []
        for vuln_data in nvd_client.fetch_cves(start_date=start_date):
            cve = nvd_client.parse_cve(vuln_data)
            if cve:
                cves.append(cve)

        logger.info(f"Parsed {len(cves)} CVEs")

        # Ingest into Neo4j
        if cves:
            neo4j_ingester.ingest_batch(cves)
        else:
            logger.warning("No CVEs to ingest")

    finally:
        neo4j_ingester.close()

if __name__ == "__main__":
    main()
