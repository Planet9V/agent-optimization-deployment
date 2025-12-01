#!/usr/bin/env python3
"""
CVE Enrichment Pipeline

Automatically enriches CVEs with EPSS scores, KEV flags, XDB exploit codes,
and calculates priority framework classifications.

File: enrichment_pipeline.py
Created: 2025-11-01
Version: 1.0.0
Author: Automation Agent
Purpose: Automated CVE enrichment orchestrator
Status: ACTIVE
"""

import os
import sys
import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional, Set
from neo4j import GraphDatabase
import yaml


class CVEEnrichmentPipeline:
    """Orchestrates automated CVE enrichment from multiple threat intelligence sources."""

    # API endpoints
    EPSS_API = "https://api.first.org/data/v1/epss"
    CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize enrichment pipeline."""
        self.config = self._load_config(config_path)

        # Neo4j connection
        self.neo4j_driver = GraphDatabase.driver(
            self.config["neo4j"]["uri"],
            auth=(self.config["neo4j"]["user"],
                  self.config["neo4j"]["password"])
        )

        # VulnCheck API (optional)
        self.vulncheck_token = os.getenv("VULNCHECK_API_TOKEN",
                                        self.config.get("vulncheck_api_token"))

        # Metrics
        self.metrics = {
            "epss_enriched": 0,
            "kev_flagged": 0,
            "exploits_linked": 0,
            "priority_calculated": 0,
            "errors": 0,
            "start_time": datetime.now()
        }

        # Setup logging
        self._setup_logging()

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _setup_logging(self):
        """Configure logging."""
        log_level = getattr(logging, self.config.get("log_level", "INFO"))
        log_file = self.config.get("enrichment_log_file", "enrichment.log")

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_cves_for_enrichment(self, limit: Optional[int] = None) -> List[str]:
        """
        Get list of CVE IDs that need enrichment.

        Args:
            limit: Maximum number of CVEs to enrich (None = all)

        Returns:
            List of CVE IDs requiring enrichment
        """
        query = """
        MATCH (cve:CVE)
        WHERE cve.epss_score IS NULL
           OR cve.epss_last_updated IS NULL
           OR duration.between(cve.epss_last_updated, datetime()).days > 7
        RETURN cve.id AS cve_id
        ORDER BY cve.published DESC
        """

        if limit:
            query += f" LIMIT {limit}"

        with self.neo4j_driver.session() as session:
            result = session.run(query)
            return [record["cve_id"] for record in result]

    def fetch_epss_scores(self, cve_ids: List[str]) -> Dict[str, Dict]:
        """
        Fetch EPSS scores from FIRST.org API.

        Args:
            cve_ids: List of CVE IDs to fetch scores for

        Returns:
            Dictionary mapping CVE ID to EPSS data
        """
        self.logger.info(f"Fetching EPSS scores for {len(cve_ids)} CVEs...")

        # FIRST API supports batch queries with comma-separated CVE IDs
        # Split into batches of 100 to avoid URL length limits
        batch_size = 100
        all_epss_data = {}

        for i in range(0, len(cve_ids), batch_size):
            batch = cve_ids[i:i + batch_size]
            cve_param = ",".join(batch)

            try:
                response = requests.get(
                    self.EPSS_API,
                    params={"cve": cve_param},
                    timeout=30
                )
                response.raise_for_status()

                data = response.json()

                for entry in data.get("data", []):
                    cve_id = entry.get("cve")
                    all_epss_data[cve_id] = {
                        "epss_score": float(entry.get("epss", 0)),
                        "epss_percentile": float(entry.get("percentile", 0)),
                        "epss_date": entry.get("date"),
                        "epss_last_updated": datetime.utcnow().isoformat()
                    }

                self.logger.info(f"Fetched EPSS for batch {i//batch_size + 1}")

            except requests.exceptions.RequestException as e:
                self.logger.error(f"EPSS API request failed: {e}")
                self.metrics["errors"] += 1
                continue

        self.logger.info(f"Retrieved EPSS scores for {len(all_epss_data)} CVEs")
        return all_epss_data

    def update_epss_in_neo4j(self, epss_data: Dict[str, Dict]):
        """
        Update CVE nodes with EPSS scores in Neo4j.

        Args:
            epss_data: Dictionary of CVE ID to EPSS data
        """
        query = """
        UNWIND $batch AS item
        MATCH (cve:CVE {id: item.cve_id})
        SET cve.epss_score = item.epss_score,
            cve.epss_percentile = item.epss_percentile,
            cve.epss_date = date(item.epss_date),
            cve.epss_last_updated = datetime(item.epss_last_updated)
        RETURN count(cve) AS updated_count
        """

        # Prepare batch data
        batch = [
            {"cve_id": cve_id, **data}
            for cve_id, data in epss_data.items()
        ]

        with self.neo4j_driver.session() as session:
            result = session.run(query, batch=batch)
            record = result.single()
            updated = record["updated_count"]

            self.metrics["epss_enriched"] += updated
            self.logger.info(f"Updated {updated} CVEs with EPSS scores")

    def fetch_cisa_kev(self) -> Set[str]:
        """
        Fetch CISA Known Exploited Vulnerabilities catalog.

        Returns:
            Set of CVE IDs in CISA KEV
        """
        self.logger.info("Fetching CISA KEV catalog...")

        try:
            response = requests.get(self.CISA_KEV_URL, timeout=30)
            response.raise_for_status()

            data = response.json()
            vulnerabilities = data.get("vulnerabilities", [])

            kev_cves = {vuln["cveID"] for vuln in vulnerabilities}

            self.logger.info(f"Retrieved {len(kev_cves)} CVEs from CISA KEV")
            return kev_cves

        except requests.exceptions.RequestException as e:
            self.logger.error(f"CISA KEV fetch failed: {e}")
            self.metrics["errors"] += 1
            return set()

    def update_kev_flags_in_neo4j(self, kev_cves: Set[str]):
        """
        Update CVE nodes with KEV flags.

        Args:
            kev_cves: Set of CVE IDs in CISA KEV
        """
        query = """
        UNWIND $cve_ids AS cve_id
        MATCH (cve:CVE {id: cve_id})
        SET cve.in_cisa_kev = true,
            cve.exploited_in_wild = true,
            cve.kev_last_updated = datetime()
        RETURN count(cve) AS updated_count
        """

        with self.neo4j_driver.session() as session:
            result = session.run(query, cve_ids=list(kev_cves))
            record = result.single()
            updated = record["updated_count"]

            self.metrics["kev_flagged"] += updated
            self.logger.info(f"Updated {updated} CVEs with KEV flags")

    def fetch_vulncheck_xdb(self, cve_ids: List[str]) -> Dict[str, List[Dict]]:
        """
        Fetch exploit code data from VulnCheck XDB.

        Args:
            cve_ids: List of CVE IDs to check for exploits

        Returns:
            Dictionary mapping CVE ID to list of exploit data
        """
        if not self.vulncheck_token:
            self.logger.warning("VulnCheck API token not configured. Skipping XDB enrichment.")
            return {}

        self.logger.info(f"Fetching XDB exploit data for {len(cve_ids)} CVEs...")

        # VulnCheck XDB API endpoint
        xdb_api = "https://api.vulncheck.com/v3/index/vulncheck-xdb"
        headers = {
            "Authorization": f"Bearer {self.vulncheck_token}",
            "Accept": "application/json"
        }

        exploit_data = {}

        for cve_id in cve_ids:
            try:
                params = {"cve": cve_id}
                response = requests.get(xdb_api, headers=headers, params=params, timeout=30)
                response.raise_for_status()

                data = response.json()
                exploits = data.get("data", [])

                if exploits:
                    exploit_data[cve_id] = exploits

            except requests.exceptions.RequestException as e:
                self.logger.error(f"XDB API request failed for {cve_id}: {e}")
                self.metrics["errors"] += 1
                continue

        self.logger.info(f"Found exploits for {len(exploit_data)} CVEs")
        return exploit_data

    def calculate_priority_tier(self, cve_id: str) -> str:
        """
        Calculate NOW/NEXT/NEVER priority tier for a CVE.

        Priority Logic:
        - NOW: in_cisa_kev OR (epss_score > 0.7 AND cvssScore >= 7.0)
        - NEXT: epss_score > 0.2 OR cvssScore >= 7.0
        - NEVER: everything else

        Args:
            cve_id: CVE ID to calculate priority for

        Returns:
            Priority tier string ("NOW", "NEXT", or "NEVER")
        """
        query = """
        MATCH (cve:CVE {id: $cve_id})
        RETURN cve.in_cisa_kev AS in_kev,
               cve.epss_score AS epss,
               cve.cvssScore AS cvss
        """

        with self.neo4j_driver.session() as session:
            result = session.run(query, cve_id=cve_id)
            record = result.single()

            if not record:
                return "NEVER"

            in_kev = record["in_kev"] or False
            epss = record["epss"] or 0.0
            cvss = record["cvss"] or 0.0

            # Priority logic
            if in_kev or (epss > 0.7 and cvss >= 7.0):
                return "NOW"
            elif epss > 0.2 or cvss >= 7.0:
                return "NEXT"
            else:
                return "NEVER"

    def update_priority_framework(self, cve_ids: List[str]):
        """
        Calculate and update priority framework for CVEs.

        Args:
            cve_ids: List of CVE IDs to update priorities for
        """
        self.logger.info(f"Calculating priority tiers for {len(cve_ids)} CVEs...")

        for cve_id in cve_ids:
            try:
                priority_tier = self.calculate_priority_tier(cve_id)

                # Update CVE with priority tier
                query = """
                MATCH (cve:CVE {id: $cve_id})
                SET cve.priority_tier = $priority_tier,
                    cve.priority_calculated_at = datetime()
                """

                with self.neo4j_driver.session() as session:
                    session.run(query, cve_id=cve_id, priority_tier=priority_tier)

                self.metrics["priority_calculated"] += 1

            except Exception as e:
                self.logger.error(f"Priority calculation failed for {cve_id}: {e}")
                self.metrics["errors"] += 1
                continue

        self.logger.info(f"Updated {self.metrics['priority_calculated']} CVEs with priority tiers")

    def run_enrichment(self, cve_ids: Optional[List[str]] = None, limit: Optional[int] = None):
        """
        Run complete enrichment pipeline.

        Args:
            cve_ids: Specific CVE IDs to enrich (None = auto-detect)
            limit: Maximum number of CVEs to process
        """
        self.logger.info("=" * 60)
        self.logger.info("CVE Enrichment Pipeline - Starting")
        self.logger.info("=" * 60)

        try:
            # Get CVEs to enrich
            if not cve_ids:
                cve_ids = self.get_cves_for_enrichment(limit=limit)

            if not cve_ids:
                self.logger.info("No CVEs require enrichment.")
                return

            self.logger.info(f"Enriching {len(cve_ids)} CVEs...")

            # Step 1: EPSS enrichment
            epss_data = self.fetch_epss_scores(cve_ids)
            if epss_data:
                self.update_epss_in_neo4j(epss_data)

            # Step 2: KEV enrichment
            kev_cves = self.fetch_cisa_kev()
            if kev_cves:
                # Only update CVEs in our enrichment list that are also in KEV
                kev_to_update = set(cve_ids) & kev_cves
                if kev_to_update:
                    self.update_kev_flags_in_neo4j(kev_to_update)

            # Step 3: XDB exploit enrichment (optional, requires API key)
            if self.vulncheck_token:
                exploit_data = self.fetch_vulncheck_xdb(cve_ids)
                # TODO: Create ExploitCode nodes and HAS_EXPLOIT_CODE relationships
                # This requires Recommendation 2 schema to be deployed

            # Step 4: Priority framework calculation
            self.update_priority_framework(cve_ids)

            # Calculate duration
            duration = (datetime.now() - self.metrics["start_time"]).total_seconds()

            # Log final metrics
            self.logger.info("=" * 60)
            self.logger.info("CVE Enrichment Pipeline - Completed")
            self.logger.info("=" * 60)
            self.logger.info(f"EPSS enriched: {self.metrics['epss_enriched']}")
            self.logger.info(f"KEV flagged: {self.metrics['kev_flagged']}")
            self.logger.info(f"Priority calculated: {self.metrics['priority_calculated']}")
            self.logger.info(f"Errors: {self.metrics['errors']}")
            self.logger.info(f"Duration: {duration:.1f}s")

        except Exception as e:
            self.logger.error(f"Enrichment pipeline failed: {e}", exc_info=True)
            raise

        finally:
            self.neo4j_driver.close()


def main():
    """Main entry point for enrichment pipeline."""
    import argparse

    parser = argparse.ArgumentParser(
        description="CVE Enrichment Pipeline"
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Maximum number of CVEs to enrich"
    )
    parser.add_argument(
        "--cve-ids",
        nargs="+",
        help="Specific CVE IDs to enrich"
    )

    args = parser.parse_args()

    try:
        pipeline = CVEEnrichmentPipeline(config_path=args.config)
        pipeline.run_enrichment(cve_ids=args.cve_ids, limit=args.limit)

        sys.exit(1 if pipeline.metrics["errors"] > 0 else 0)

    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
