#!/usr/bin/env python3
"""
NVD Daily CVE Sync Script

Fetches CVEs modified in the last 24 hours from NVD API v2.0 and updates Neo4j database.
Implements incremental sync strategy with rate limiting and error handling.

File: nvd_daily_sync.py
Created: 2025-11-01
Version: 1.0.0
Author: Automation Agent
Purpose: Daily incremental CVE sync from NVD API
Status: ACTIVE
"""

import os
import sys
import time
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from neo4j import GraphDatabase
import yaml


class NVDDailySync:
    """NVD API v2.0 daily synchronization client with rate limiting."""

    NVD_API_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    # Rate limits (requests per 30 seconds)
    RATE_LIMIT_WITH_KEY = 50
    RATE_LIMIT_NO_KEY = 5

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize NVD sync client with configuration."""
        self.config = self._load_config(config_path)

        # NVD API configuration
        self.api_key = os.getenv("NVD_API_KEY", self.config.get("nvd_api_key"))
        self.rate_limit = (self.RATE_LIMIT_WITH_KEY if self.api_key
                          else self.RATE_LIMIT_NO_KEY)

        # Neo4j connection
        self.neo4j_driver = GraphDatabase.driver(
            self.config["neo4j"]["uri"],
            auth=(self.config["neo4j"]["user"],
                  self.config["neo4j"]["password"])
        )

        # Rate limiting state
        self.request_count = 0
        self.window_start = time.time()

        # Metrics
        self.metrics = {
            "cves_fetched": 0,
            "cves_created": 0,
            "cves_updated": 0,
            "api_calls": 0,
            "errors": 0,
            "start_time": datetime.now()
        }

        # Setup logging
        self._setup_logging()

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        if not os.path.exists(config_path):
            logging.error(f"Configuration file not found: {config_path}")
            sys.exit(1)

        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _setup_logging(self):
        """Configure logging to file and console."""
        log_level = getattr(logging, self.config.get("log_level", "INFO"))
        log_file = self.config.get("log_file", "nvd_sync.log")

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _rate_limit(self):
        """Enforce NVD API rate limits (requests per 30 seconds)."""
        current_time = time.time()
        elapsed = current_time - self.window_start

        # Reset window if 30 seconds have passed
        if elapsed >= 30:
            self.request_count = 0
            self.window_start = current_time
            return

        # Check if limit reached
        if self.request_count >= self.rate_limit:
            sleep_time = 30 - elapsed
            self.logger.info(f"Rate limit reached. Sleeping {sleep_time:.1f}s...")
            time.sleep(sleep_time)
            self.request_count = 0
            self.window_start = time.time()

    def fetch_modified_cves(self,
                           hours_back: int = 24,
                           batch_size: int = 2000) -> List[Dict]:
        """
        Fetch CVEs modified within the last N hours from NVD API.

        Args:
            hours_back: Number of hours to look back (default: 24)
            batch_size: Results per page (max: 2000)

        Returns:
            List of CVE dictionaries from NVD API
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=hours_back)

        # Format dates for NVD API (ISO 8601)
        start_str = start_date.strftime("%Y-%m-%dT%H:%M:%S.000")
        end_str = end_date.strftime("%Y-%m-%dT%H:%M:%S.000")

        self.logger.info(f"Fetching CVEs modified between {start_str} and {end_str}")

        all_cves = []
        start_index = 0

        while True:
            self._rate_limit()

            # Build request parameters
            params = {
                "lastModStartDate": start_str,
                "lastModEndDate": end_str,
                "resultsPerPage": batch_size,
                "startIndex": start_index
            }

            # Add API key if available
            headers = {}
            if self.api_key:
                headers["apiKey"] = self.api_key

            try:
                response = requests.get(
                    self.NVD_API_BASE,
                    params=params,
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()

                self.request_count += 1
                self.metrics["api_calls"] += 1

                data = response.json()
                vulnerabilities = data.get("vulnerabilities", [])

                if not vulnerabilities:
                    break

                all_cves.extend(vulnerabilities)
                self.metrics["cves_fetched"] += len(vulnerabilities)

                self.logger.info(f"Fetched {len(vulnerabilities)} CVEs "
                               f"(total: {len(all_cves)})")

                # Check if more pages available
                total_results = data.get("totalResults", 0)
                if start_index + batch_size >= total_results:
                    break

                start_index += batch_size

            except requests.exceptions.RequestException as e:
                self.logger.error(f"NVD API request failed: {e}")
                self.metrics["errors"] += 1
                raise

        self.logger.info(f"Total CVEs fetched from NVD: {len(all_cves)}")
        return all_cves

    def _parse_cve_data(self, cve_item: Dict) -> Dict:
        """
        Extract and normalize CVE data from NVD API response.

        Args:
            cve_item: CVE item from NVD API vulnerabilities array

        Returns:
            Normalized CVE dictionary for Neo4j
        """
        cve = cve_item.get("cve", {})
        cve_id = cve.get("id")

        # Extract metrics (CVSS scores)
        metrics = cve.get("metrics", {})
        cvss_v3 = metrics.get("cvssMetricV31", [{}])[0] if metrics.get("cvssMetricV31") else {}
        cvss_v2 = metrics.get("cvssMetricV2", [{}])[0] if metrics.get("cvssMetricV2") else {}

        cvss_data = cvss_v3.get("cvssData", {}) if cvss_v3 else cvss_v2.get("cvssData", {})

        # Extract descriptions
        descriptions = cve.get("descriptions", [])
        description = next(
            (d["value"] for d in descriptions if d.get("lang") == "en"),
            descriptions[0]["value"] if descriptions else ""
        )

        # Extract references
        references = [ref.get("url") for ref in cve.get("references", [])]

        # Extract CPE configurations
        configurations = cve.get("configurations", [])
        cpe_list = []
        for config in configurations:
            for node in config.get("nodes", []):
                cpe_list.extend([
                    cpe_match.get("criteria")
                    for cpe_match in node.get("cpeMatch", [])
                    if cpe_match.get("criteria")
                ])

        return {
            "id": cve_id,
            "description": description,
            "cvss_score": cvss_data.get("baseScore"),
            "cvss_version": cvss_data.get("version"),
            "cvss_vector": cvss_data.get("vectorString"),
            "severity": cvss_v3.get("baseSeverity") or cvss_v2.get("baseSeverity"),
            "published": cve.get("published"),
            "last_modified": cve.get("lastModified"),
            "references": references,
            "cpe_list": cpe_list,
            "source": "nvd",
            "updated_at": datetime.utcnow().isoformat()
        }

    def upsert_cve_to_neo4j(self, cve_data: Dict) -> Tuple[str, bool]:
        """
        Insert or update CVE in Neo4j database.

        Args:
            cve_data: Normalized CVE dictionary

        Returns:
            Tuple of (cve_id, was_created)
        """
        query = """
        MERGE (cve:CVE {id: $id})
        ON CREATE SET
            cve.description = $description,
            cve.cvssScore = $cvss_score,
            cve.cvssVersion = $cvss_version,
            cve.cvssVector = $cvss_vector,
            cve.severity = $severity,
            cve.published = datetime($published),
            cve.lastModified = datetime($last_modified),
            cve.source = $source,
            cve.created_at = datetime(),
            cve.updated_at = datetime()
        ON MATCH SET
            cve.description = $description,
            cve.cvssScore = $cvss_score,
            cve.cvssVersion = $cvss_version,
            cve.cvssVector = $cvss_vector,
            cve.severity = $severity,
            cve.lastModified = datetime($last_modified),
            cve.updated_at = datetime()
        RETURN cve.id AS cve_id,
               CASE WHEN cve.created_at = cve.updated_at THEN true ELSE false END AS was_created
        """

        with self.neo4j_driver.session() as session:
            result = session.run(query, **cve_data)
            record = result.single()
            return record["cve_id"], record["was_created"]

    def fetch_all_cves_bulk(self, start_year: int = 2002, end_year: int = 2025) -> List[Dict]:
        """
        Fetch ALL CVEs from NVD API using year-based date ranges.
        SINGLE WORKER mode to comply with NVD rate limits.

        Args:
            start_year: First year to fetch (default: 2002)
            end_year: Last year to fetch (default: 2025)

        Returns:
            List of all CVE dictionaries from NVD API
        """
        all_cves = []

        for year in range(start_year, end_year + 1):
            # Build date range for full year
            start_date = f"{year}-01-01T00:00:00.000"
            end_date = f"{year}-12-31T23:59:59.999"

            self.logger.info(f"Fetching CVEs for year {year}...")

            start_index = 0
            year_cves = []

            while True:
                self._rate_limit()

                params = {
                    "pubStartDate": start_date,
                    "pubEndDate": end_date,
                    "resultsPerPage": 2000,  # NVD maximum
                    "startIndex": start_index
                }

                headers = {}
                if self.api_key:
                    headers["apiKey"] = self.api_key

                try:
                    response = requests.get(
                        self.NVD_API_BASE,
                        params=params,
                        headers=headers,
                        timeout=30
                    )
                    response.raise_for_status()

                    self.request_count += 1
                    self.metrics["api_calls"] += 1

                    data = response.json()
                    vulnerabilities = data.get("vulnerabilities", [])

                    if not vulnerabilities:
                        break

                    year_cves.extend(vulnerabilities)
                    self.metrics["cves_fetched"] += len(vulnerabilities)

                    self.logger.info(f"  Year {year}: Fetched {len(year_cves)} CVEs so far")

                    # Check pagination
                    total_results = data.get("totalResults", 0)
                    if start_index + 2000 >= total_results:
                        break

                    start_index += 2000

                except requests.exceptions.RequestException as e:
                    self.logger.error(f"API request failed for year {year}: {e}")
                    self.metrics["errors"] += 1
                    # Continue with next year instead of failing completely
                    break

            all_cves.extend(year_cves)
            self.logger.info(f"Year {year} complete: {len(year_cves)} CVEs")

        self.logger.info(f"Bulk fetch complete: {len(all_cves)} total CVEs")
        return all_cves

    def bulk_import_all_cves(self, start_year: int = 2002, end_year: int = 2025) -> Dict:
        """
        Bulk import all CVEs from NVD API (SINGLE WORKER).
        Designed to replace/clean existing CVE data.

        Args:
            start_year: First year to import
            end_year: Last year to import

        Returns:
            Metrics dictionary with import results
        """
        self.logger.info("=" * 60)
        self.logger.info("NVD BULK IMPORT - Starting (SINGLE WORKER)")
        self.logger.info(f"Date Range: {start_year}-{end_year}")
        self.logger.info("=" * 60)

        try:
            # Fetch all CVEs
            cve_items = self.fetch_all_cves_bulk(start_year, end_year)

            if not cve_items:
                self.logger.error("No CVEs fetched from NVD!")
                return self.metrics

            # Process in batches for better performance (SINGLE WORKER)
            batch_size = 1000
            for i in range(0, len(cve_items), batch_size):
                batch = cve_items[i:i + batch_size]

                for idx, cve_item in enumerate(batch, 1):
                    try:
                        cve_data = self._parse_cve_data(cve_item)
                        cve_id, was_created = self.upsert_cve_to_neo4j(cve_data)

                        if was_created:
                            self.metrics["cves_created"] += 1
                        else:
                            self.metrics["cves_updated"] += 1

                        # Progress logging every 1000 CVEs
                        total_processed = i + idx
                        if total_processed % 1000 == 0:
                            self.logger.info(f"Progress: {total_processed}/{len(cve_items)} CVEs processed ({(total_processed/len(cve_items)*100):.1f}%)")

                    except Exception as e:
                        self.logger.error(f"Failed to process CVE: {e}")
                        self.metrics["errors"] += 1
                        continue

            # Calculate duration
            self.metrics["duration"] = (datetime.now() - self.metrics["start_time"]).total_seconds()

            # Log final metrics
            self.logger.info("=" * 60)
            self.logger.info("NVD BULK IMPORT - Completed")
            self.logger.info("=" * 60)
            self.logger.info(f"CVEs fetched: {self.metrics['cves_fetched']}")
            self.logger.info(f"CVEs created: {self.metrics['cves_created']}")
            self.logger.info(f"CVEs updated: {self.metrics['cves_updated']}")
            self.logger.info(f"API calls: {self.metrics['api_calls']}")
            self.logger.info(f"Errors: {self.metrics['errors']}")
            self.logger.info(f"Duration: {self.metrics['duration']:.1f}s ({self.metrics['duration']/60:.1f} minutes)")

            return self.metrics

        except Exception as e:
            self.logger.error(f"Bulk import failed: {e}", exc_info=True)
            raise
        finally:
            self.neo4j_driver.close()

    def sync_daily_updates(self, hours_back: int = 24) -> Dict:
        """
        Main synchronization workflow.

        Args:
            hours_back: Number of hours to look back for modifications

        Returns:
            Metrics dictionary with sync results
        """
        self.logger.info("=" * 60)
        self.logger.info("NVD Daily CVE Sync - Starting")
        self.logger.info("=" * 60)

        try:
            # Fetch modified CVEs from NVD
            cve_items = self.fetch_modified_cves(hours_back=hours_back)

            if not cve_items:
                self.logger.info("No CVEs modified in the specified period.")
                return self.metrics

            # Process each CVE
            for idx, cve_item in enumerate(cve_items, 1):
                try:
                    cve_data = self._parse_cve_data(cve_item)
                    cve_id, was_created = self.upsert_cve_to_neo4j(cve_data)

                    if was_created:
                        self.metrics["cves_created"] += 1
                        self.logger.debug(f"Created new CVE: {cve_id}")
                    else:
                        self.metrics["cves_updated"] += 1
                        self.logger.debug(f"Updated existing CVE: {cve_id}")

                    if idx % 100 == 0:
                        self.logger.info(f"Processed {idx}/{len(cve_items)} CVEs...")

                except Exception as e:
                    self.logger.error(f"Failed to process CVE: {e}")
                    self.metrics["errors"] += 1
                    continue

            # Calculate duration
            self.metrics["duration"] = (datetime.now() -
                                       self.metrics["start_time"]).total_seconds()

            # Log final metrics
            self.logger.info("=" * 60)
            self.logger.info("NVD Daily Sync - Completed")
            self.logger.info("=" * 60)
            self.logger.info(f"CVEs fetched: {self.metrics['cves_fetched']}")
            self.logger.info(f"CVEs created: {self.metrics['cves_created']}")
            self.logger.info(f"CVEs updated: {self.metrics['cves_updated']}")
            self.logger.info(f"API calls: {self.metrics['api_calls']}")
            self.logger.info(f"Errors: {self.metrics['errors']}")
            self.logger.info(f"Duration: {self.metrics['duration']:.1f}s")

            return self.metrics

        except Exception as e:
            self.logger.error(f"Sync failed with error: {e}", exc_info=True)
            raise

        finally:
            self.neo4j_driver.close()


def main():
    """Main entry point for daily sync and bulk import."""
    import argparse

    parser = argparse.ArgumentParser(
        description="NVD CVE Synchronization Script (Daily & Bulk Modes)"
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)"
    )

    # MODE SELECTION (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--daily",
        action="store_true",
        help="Daily incremental sync mode (modified CVEs in last N hours)"
    )
    mode_group.add_argument(
        "--bulk",
        action="store_true",
        help="Bulk import mode (all CVEs from start_year to end_year)"
    )

    # DAILY MODE OPTIONS
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="Hours to look back for daily sync (default: 24)"
    )

    # BULK MODE OPTIONS
    parser.add_argument(
        "--start-year",
        type=int,
        default=2002,
        help="Start year for bulk import (default: 2002)"
    )
    parser.add_argument(
        "--end-year",
        type=int,
        default=2025,
        help="End year for bulk import (default: 2025)"
    )

    args = parser.parse_args()

    try:
        syncer = NVDDailySync(config_path=args.config)

        if args.daily:
            # DAILY INCREMENTAL SYNC
            metrics = syncer.sync_daily_updates(hours_back=args.hours)
        elif args.bulk:
            # BULK IMPORT
            metrics = syncer.bulk_import_all_cves(
                start_year=args.start_year,
                end_year=args.end_year
            )

        # Exit with error code if errors occurred
        sys.exit(1 if metrics["errors"] > 0 else 0)

    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
