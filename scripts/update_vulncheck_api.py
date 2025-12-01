#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
VulnCheck API Update Script
Created: 2025-11-28
Purpose: Fetch latest KEV updates from VulnCheck API
Uses: Configured VulnCheck API key from environment
═══════════════════════════════════════════════════════════════
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Optional
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

VULNCHECK_API_BASE_URL = "https://api.vulncheck.com/v3"
VULNCHECK_API_KEY = os.getenv("VULNCHECK_API_KEY")

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# ═══════════════════════════════════════════════════════════════
# VulnCheck API Client
# ═══════════════════════════════════════════════════════════════

class VulnCheckAPIClient:
    """Client for VulnCheck API."""

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("VULNCHECK_API_KEY is required")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        })

    def fetch_kev_updates(self) -> List[Dict]:
        """
        Fetch latest KEV updates from VulnCheck.

        Returns:
            List of KEV entries
        """
        endpoint = f"{VULNCHECK_API_BASE_URL}/kev"

        logger.info("Fetching latest KEV data from VulnCheck...")

        try:
            response = self.session.get(endpoint, timeout=30)
            response.raise_for_status()
            data = response.json()

            # VulnCheck API returns data in 'data' field
            entries = data.get("data", [])
            logger.info(f"Fetched {len(entries)} KEV entries")

            return entries

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return []

# ═══════════════════════════════════════════════════════════════
# Neo4j Loader
# ═══════════════════════════════════════════════════════════════

class KEVLoader:
    """Load KEV data into Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_kev_entry(self, entry: Dict) -> bool:
        """Load or update single KEV entry."""
        query = """
        UNWIND $cves AS cve_id

        MERGE (cve:CVE {cveId: cve_id})
        SET cve.hasExploit = true,
            cve.exploitMaturity = 'ACTIVE',
            cve.vulnerabilityName = $vulnerabilityName,
            cve.shortDescription = $shortDescription,
            cve.vendorProject = $vendorProject,
            cve.product = $product,
            cve.requiredAction = $requiredAction,
            cve.knownRansomware = $knownRansomware,
            cve.is_shared = true,
            cve.customer_namespace = 'shared:vulncheck-kev',
            cve.lastUpdated = datetime()

        WITH cve
        UNWIND $cwes AS cwe_id
        MERGE (cwe:CWE {cweId: cwe_id})
        ON CREATE SET
          cwe.customer_namespace = 'shared:cwe',
          cwe.is_shared = true
        MERGE (cve)-[:IS_WEAKNESS_TYPE]->(cwe)

        WITH cve
        UNWIND $exploitEvidence AS evidence
        MERGE (exp:ExploitEvidence {
          url: evidence.url,
          dateAdded: date(substring(evidence.date_added, 0, 10))
        })
        ON CREATE SET
          exp.source = 'VulnCheck'
        MERGE (cve)-[:HAS_EXPLOIT_EVIDENCE]->(exp)

        RETURN cve.cveId AS cveId
        """

        try:
            with self.driver.session() as session:
                result = session.run(query,
                    cves=entry.get('cve', []),
                    vulnerabilityName=entry.get('vulnerabilityName', ''),
                    shortDescription=entry.get('shortDescription', ''),
                    vendorProject=entry.get('vendorProject', ''),
                    product=entry.get('product', ''),
                    requiredAction=entry.get('required_action', ''),
                    knownRansomware=entry.get('knownRansomwareCampaignUse', 'Unknown'),
                    cwes=entry.get('cwes', []) if entry.get('cwes') else [],
                    exploitEvidence=entry.get('vulncheck_reported_exploitation', [])
                )
                return True

        except Exception as e:
            logger.error(f"Failed to load KEV entry: {e}")
            return False

    def load_all(self, entries: List[Dict]):
        """Load all KEV entries."""
        successes = 0

        with tqdm(total=len(entries), desc="Updating KEV data") as pbar:
            for entry in entries:
                if self.load_kev_entry(entry):
                    successes += 1
                pbar.update(1)

        logger.info(f"Successfully updated {successes}/{len(entries)} KEV entries")
        return successes

# ═══════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════

def main():
    """Main execution function."""
    if not VULNCHECK_API_KEY:
        logger.error("VULNCHECK_API_KEY not set in environment")
        logger.info("Please set VULNCHECK_API_KEY in .env file")
        sys.exit(1)

    client = VulnCheckAPIClient(api_key=VULNCHECK_API_KEY)
    loader = KEVLoader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        entries = client.fetch_kev_updates()

        if entries:
            loader.load_all(entries)

            # Verify counts
            with loader.driver.session() as session:
                result = session.run("""
                    MATCH (cve:CVE {hasExploit: true})
                    WHERE cve.customer_namespace = 'shared:vulncheck-kev'
                    RETURN count(cve) AS count
                """)
                count = result.single()['count']
                logger.info(f"Total KEV CVEs in database: {count}")

        else:
            logger.warning("No KEV entries fetched from API")

    finally:
        loader.close()

if __name__ == "__main__":
    main()
