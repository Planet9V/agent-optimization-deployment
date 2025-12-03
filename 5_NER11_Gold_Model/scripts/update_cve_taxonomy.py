#!/usr/bin/env python3
"""
CVE Taxonomy Incremental Update Script

Updates CVE taxonomy with new vulnerabilities from NVD and EPSS scores.
Designed to be run weekly as a cron job.

Usage:
    python3 scripts/update_cve_taxonomy.py --days 7
    python3 scripts/update_cve_taxonomy.py --cve CVE-2024-12345

Cron setup (weekly):
    0 0 * * 0 cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model && python3 scripts/update_cve_taxonomy.py --days 7 >> logs/cve_update.log 2>&1
"""

import sys
import argparse
import requests
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from neo4j import GraphDatabase

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"
EPSS_API = "https://api.first.org/data/v1/epss"

# Rate limiting for NVD API (free tier: 5 requests per 30 seconds)
NVD_RATE_LIMIT = 6  # seconds between requests


class CVETaxonomyUpdater:
    """Updates CVE taxonomy from NVD and EPSS APIs."""

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )
        print(f"✅ Connected to Neo4j at {neo4j_uri}")

    def close(self):
        """Close Neo4j connection."""
        self.driver.close()

    def get_nvd_cves(self, days_back: int = 7, specific_cve: str = None) -> List[Dict]:
        """
        Fetch CVEs from NVD API.

        Args:
            days_back: Number of days to look back for new CVEs
            specific_cve: Specific CVE ID to fetch

        Returns:
            List of CVE dictionaries from NVD
        """
        if specific_cve:
            print(f"📥 Fetching specific CVE: {specific_cve}")
            params = {"cveId": specific_cve}
        else:
            start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%dT00:00:00.000")
            end_date = datetime.now().strftime("%Y-%m-%dT23:59:59.999")
            print(f"📥 Fetching CVEs from {start_date[:10]} to {end_date[:10]}")
            params = {
                "pubStartDate": start_date,
                "pubEndDate": end_date
            }

        all_cves = []
        start_index = 0
        results_per_page = 2000

        while True:
            params["startIndex"] = start_index
            params["resultsPerPage"] = results_per_page

            try:
                response = requests.get(NVD_API, params=params, timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    vulnerabilities = data.get("vulnerabilities", [])
                    total_results = data.get("totalResults", 0)

                    all_cves.extend(vulnerabilities)
                    print(f"   Fetched {len(vulnerabilities)} CVEs (total: {len(all_cves)}/{total_results})")

                    if len(all_cves) >= total_results:
                        break

                    start_index += results_per_page
                    time.sleep(NVD_RATE_LIMIT)  # Rate limiting
                else:
                    print(f"   ⚠️ NVD API error: {response.status_code}")
                    break

            except Exception as e:
                print(f"   ❌ NVD API failed: {e}")
                break

        return all_cves

    def get_epss_scores(self, cve_ids: List[str]) -> Dict[str, Dict]:
        """
        Fetch EPSS scores for list of CVEs.

        Args:
            cve_ids: List of CVE IDs

        Returns:
            Dictionary mapping CVE ID to EPSS data
        """
        if not cve_ids:
            return {}

        print(f"📊 Fetching EPSS scores for {len(cve_ids)} CVEs")
        scores = {}
        chunk_size = 100  # EPSS API accepts up to 100 CVEs per request

        for i in range(0, len(cve_ids), chunk_size):
            chunk = cve_ids[i:i + chunk_size]
            cve_param = ",".join(chunk)

            try:
                response = requests.get(
                    f"{EPSS_API}?cve={cve_param}",
                    timeout=30
                )
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get("data", []):
                        cve_id = item.get("cve")
                        if cve_id:
                            scores[cve_id] = {
                                "epss": float(item.get("epss", 0)),
                                "percentile": float(item.get("percentile", 0))
                            }
                    print(f"   Got EPSS for {len(data.get('data', []))} CVEs")
                else:
                    print(f"   ⚠️ EPSS API error: {response.status_code}")

            except Exception as e:
                print(f"   ⚠️ EPSS API failed: {e}")

            time.sleep(1)  # Brief pause between requests

        return scores

    def calculate_priority_tier(self, epss_score: float, cvss_score: float = 0) -> str:
        """
        Calculate priority tier based on EPSS and CVSS.

        Tiers:
        - Tier1 (Critical): EPSS > 0.5 or CVSS >= 9.0
        - Tier2 (High): EPSS > 0.1 or CVSS >= 7.0
        - Tier3 (Medium): EPSS > 0.01 or CVSS >= 4.0
        - Tier4 (Low): Everything else
        """
        if epss_score > 0.5 or cvss_score >= 9.0:
            return "Tier1"
        elif epss_score > 0.1 or cvss_score >= 7.0:
            return "Tier2"
        elif epss_score > 0.01 or cvss_score >= 4.0:
            return "Tier3"
        else:
            return "Tier4"

    def update_neo4j(self, cves: List[Dict], epss_scores: Dict[str, Dict]) -> Dict:
        """
        Insert/update CVEs in Neo4j.

        Args:
            cves: List of CVE dictionaries from NVD
            epss_scores: Dictionary of EPSS scores

        Returns:
            Statistics dictionary
        """
        stats = {
            "created": 0,
            "updated": 0,
            "cwe_links": 0,
            "errors": 0
        }

        with self.driver.session() as session:
            for vuln in cves:
                try:
                    cve = vuln.get("cve", {})
                    cve_id = cve.get("id")

                    if not cve_id:
                        continue

                    # Get EPSS score
                    epss = epss_scores.get(cve_id, {})
                    epss_score = epss.get("epss", 0.0)
                    epss_percentile = epss.get("percentile", 0.0)

                    # Get CVSS score (prefer v3.1, fallback to v3.0, then v2.0)
                    metrics = cve.get("metrics", {})
                    cvss_score = 0.0
                    cvss_vector = ""

                    if "cvssMetricV31" in metrics:
                        cvss_data = metrics["cvssMetricV31"][0].get("cvssData", {})
                        cvss_score = float(cvss_data.get("baseScore", 0))
                        cvss_vector = cvss_data.get("vectorString", "")
                    elif "cvssMetricV30" in metrics:
                        cvss_data = metrics["cvssMetricV30"][0].get("cvssData", {})
                        cvss_score = float(cvss_data.get("baseScore", 0))
                        cvss_vector = cvss_data.get("vectorString", "")
                    elif "cvssMetricV2" in metrics:
                        cvss_data = metrics["cvssMetricV2"][0].get("cvssData", {})
                        cvss_score = float(cvss_data.get("baseScore", 0))
                        cvss_vector = cvss_data.get("vectorString", "")

                    # Calculate priority tier
                    priority_tier = self.calculate_priority_tier(epss_score, cvss_score)

                    # Get description
                    descriptions = cve.get("descriptions", [])
                    description = ""
                    for desc in descriptions:
                        if desc.get("lang") == "en":
                            description = desc.get("value", "")
                            break

                    # MERGE into Neo4j
                    result = session.run("""
                        MERGE (c:CVE {id: $cve_id})
                        ON CREATE SET
                            c.description = $description,
                            c.published = $published,
                            c.last_modified = $modified,
                            c.epss_score = $epss,
                            c.epss_percentile = $percentile,
                            c.cvss_score = $cvss,
                            c.cvss_vector = $vector,
                            c.priority_tier = $tier,
                            c.created_at = timestamp()
                        ON MATCH SET
                            c.description = $description,
                            c.last_modified = $modified,
                            c.epss_score = $epss,
                            c.epss_percentile = $percentile,
                            c.cvss_score = $cvss,
                            c.cvss_vector = $vector,
                            c.priority_tier = $tier,
                            c.updated_at = timestamp()
                        RETURN c.created_at IS NOT NULL AND c.updated_at IS NULL AS is_new
                    """,
                        cve_id=cve_id,
                        description=description[:2000],  # Truncate long descriptions
                        published=cve.get("published"),
                        modified=cve.get("lastModified"),
                        epss=epss_score,
                        percentile=epss_percentile,
                        cvss=cvss_score,
                        vector=cvss_vector,
                        tier=priority_tier
                    )

                    record = result.single()
                    if record and record["is_new"]:
                        stats["created"] += 1
                    else:
                        stats["updated"] += 1

                    # Link to CWEs
                    for weakness in cve.get("weaknesses", []):
                        for desc in weakness.get("description", []):
                            cwe_value = desc.get("value", "")
                            if cwe_value.startswith("CWE-"):
                                cwe_id = cwe_value.lower()  # Our CWE IDs are lowercase
                                try:
                                    session.run("""
                                        MATCH (c:CVE {id: $cve_id})
                                        MATCH (w:CWE)
                                        WHERE w.id = $cwe_id OR toLower(w.id) = $cwe_id
                                        MERGE (c)-[r:HAS_WEAKNESS]->(w)
                                        ON CREATE SET r.created_at = timestamp()
                                    """, cve_id=cve_id, cwe_id=cwe_id)
                                    stats["cwe_links"] += 1
                                except:
                                    pass  # CWE might not exist

                except Exception as e:
                    stats["errors"] += 1
                    print(f"   ⚠️ Error processing {cve_id}: {e}")

        return stats

    def generate_report(self) -> Dict:
        """Generate update statistics report."""
        with self.driver.session() as session:
            # Get CVE counts by tier
            result = session.run("""
                MATCH (c:CVE)
                RETURN c.priority_tier as tier, count(*) as count
                ORDER BY tier
            """)

            tier_counts = {record["tier"]: record["count"] for record in result}

            # Get EPSS coverage
            result = session.run("""
                MATCH (c:CVE)
                WITH count(*) as total
                MATCH (c:CVE) WHERE c.epss_score > 0
                WITH total, count(*) as with_epss
                RETURN total, with_epss,
                       round(100.0 * with_epss / total, 1) as epss_pct
            """)

            coverage = result.single()

            # Get CVSS coverage
            result = session.run("""
                MATCH (c:CVE)
                WITH count(*) as total
                MATCH (c:CVE) WHERE c.cvss_score > 0
                WITH total, count(*) as with_cvss
                RETURN total, with_cvss,
                       round(100.0 * with_cvss / total, 1) as cvss_pct
            """)

            cvss_coverage = result.single()

            return {
                "total_cves": coverage["total"],
                "epss_coverage": coverage["epss_pct"],
                "cvss_coverage": cvss_coverage["cvss_pct"],
                "tier_counts": tier_counts
            }


def main():
    parser = argparse.ArgumentParser(description="CVE Taxonomy Update")
    parser.add_argument("--days", type=int, default=7, help="Days to look back for new CVEs")
    parser.add_argument("--cve", type=str, help="Specific CVE ID to fetch")
    parser.add_argument("--epss-only", action="store_true", help="Only refresh EPSS scores")
    parser.add_argument("--report-only", action="store_true", help="Only generate report")

    args = parser.parse_args()

    print("="*60)
    print("CVE Taxonomy Update")
    print(f"Started: {datetime.now().isoformat()}")
    print("="*60)

    updater = CVETaxonomyUpdater(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        if args.report_only:
            # Just generate report
            report = updater.generate_report()
            print(f"\n📊 CVE TAXONOMY REPORT")
            print(f"   Total CVEs: {report['total_cves']:,}")
            print(f"   EPSS Coverage: {report['epss_coverage']}%")
            print(f"   CVSS Coverage: {report['cvss_coverage']}%")
            print(f"   Tier Distribution:")
            for tier, count in sorted(report['tier_counts'].items()):
                print(f"     {tier}: {count:,}")
        else:
            # Fetch and update
            cves = updater.get_nvd_cves(
                days_back=args.days,
                specific_cve=args.cve
            )

            if not cves:
                print("No new CVEs to process")
                return

            # Get EPSS scores
            cve_ids = [v["cve"]["id"] for v in cves]
            epss_scores = updater.get_epss_scores(cve_ids)

            # Update Neo4j
            print("\n📝 Updating Neo4j...")
            stats = updater.update_neo4j(cves, epss_scores)

            print(f"\n✅ UPDATE COMPLETE")
            print(f"   Created: {stats['created']}")
            print(f"   Updated: {stats['updated']}")
            print(f"   CWE Links: {stats['cwe_links']}")
            print(f"   Errors: {stats['errors']}")

            # Generate final report
            report = updater.generate_report()
            print(f"\n📊 CURRENT STATE")
            print(f"   Total CVEs: {report['total_cves']:,}")
            print(f"   EPSS Coverage: {report['epss_coverage']}%")
            print(f"   CVSS Coverage: {report['cvss_coverage']}%")

    finally:
        updater.close()

    print(f"\n{'='*60}")
    print(f"Finished: {datetime.now().isoformat()}")
    print("="*60)


if __name__ == "__main__":
    main()
