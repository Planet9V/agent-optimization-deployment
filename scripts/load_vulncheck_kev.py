#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
VulnCheck KEV Data Loader
Created: 2025-11-28
Purpose: Load VulnCheck Known Exploited Vulnerabilities data into Neo4j
Data: 2981 CVEs with exploit intelligence
═══════════════════════════════════════════════════════════════
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List
from neo4j import GraphDatabase
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════

KEV_JSON_PATH = "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/NVS Full CVE CAPEC CWE EMBED/vulncheck-kev.json"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# ═══════════════════════════════════════════════════════════════
# Neo4j Loader
# ═══════════════════════════════════════════════════════════════

class VulnCheckKEVLoader:
    """Load VulnCheck KEV data into Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_kev_entry(self, entry: Dict) -> bool:
        """Load single KEV entry with CVE and exploitation data."""
        query = """
        // Get CVE IDs from entry
        UNWIND $cves AS cve_id

        // Create or update CVE node
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
            cve.customer_namespace = 'shared:vulncheck-kev'

        // Link to CWEs if present
        WITH cve
        UNWIND $cwes AS cwe_id
        MERGE (cwe:CWE {cweId: cwe_id})
        ON CREATE SET
          cwe.customer_namespace = 'shared:cwe',
          cwe.is_shared = true
        MERGE (cve)-[:IS_WEAKNESS_TYPE]->(cwe)

        // Create ExploitEvidence nodes
        WITH cve
        UNWIND $exploitEvidence AS evidence
        CREATE (exp:ExploitEvidence {
          url: evidence.url,
          dateAdded: date(substring(evidence.date_added, 0, 10)),
          source: 'VulnCheck'
        })
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

    def load_all(self, json_path: str):
        """Load all KEV entries from JSON file."""
        path = Path(json_path)
        if not path.exists():
            logger.error(f"KEV JSON file not found: {json_path}")
            return 0

        logger.info(f"Loading KEV data from: {json_path}")

        with open(path, 'r') as f:
            entries = json.load(f)

        logger.info(f"Found {len(entries)} KEV entries")

        successes = 0
        with tqdm(total=len(entries), desc="Loading KEV data") as pbar:
            for entry in entries:
                if self.load_kev_entry(entry):
                    successes += 1
                pbar.update(1)

        logger.info(f"Successfully loaded {successes}/{len(entries)} KEV entries")
        return successes

# ═══════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════

def main():
    """Main execution function."""
    loader = VulnCheckKEVLoader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        count = loader.load_all(KEV_JSON_PATH)

        # Verify counts
        with loader.driver.session() as session:
            result = session.run("""
                MATCH (cve:CVE {hasExploit: true})
                WHERE cve.customer_namespace = 'shared:vulncheck-kev'
                RETURN count(cve) AS count
            """)
            record = result.single()
            logger.info(f"Total KEV CVEs in database: {record['count']}")

            result = session.run("""
                MATCH (exp:ExploitEvidence)
                RETURN count(exp) AS count
            """)
            record = result.single()
            logger.info(f"Total exploit evidence records: {record['count']}")

    finally:
        loader.close()

if __name__ == "__main__":
    main()
