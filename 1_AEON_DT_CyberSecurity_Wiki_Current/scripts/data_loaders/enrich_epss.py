#!/usr/bin/env python3
"""
AEON Cyber Digital Twin - EPSS Enrichment
==========================================
Enriches CVE nodes with EPSS (Exploit Prediction Scoring System) scores
from FIRST.org API.

Usage:
    NEO4J_PASSWORD="neo4j@openspg" python3 enrich_epss.py

API Key: 534786f5-5359-40b8-8e54-b28eb742de7c

Sources:
    - https://api.first.org/data/v1/epss

Created: 2025-11-29
Version: 1.0.0
"""

import os
import sys
import logging
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional
from neo4j import GraphDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FIRST.org EPSS API
EPSS_API_BASE = "https://api.first.org/data/v1/epss"
EPSS_API_KEY = os.environ.get('EPSS_API_KEY', '534786f5-5359-40b8-8e54-b28eb742de7c')


class EPSSEnricher:
    """Enriches CVE nodes with EPSS scores."""

    def __init__(self, uri: str, user: str, password: str):
        """Initialize with Neo4j connection."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            'cves_queried': 0,
            'cves_enriched': 0,
            'api_calls': 0,
            'errors': []
        }

    def close(self):
        """Close the Neo4j connection."""
        self.driver.close()

    def get_cve_ids_needing_epss(self, limit: int = 1000) -> List[str]:
        """Get CVE IDs that need EPSS scores."""
        query = """
        MATCH (cve:CVE)
        WHERE cve.epssScore IS NULL OR cve.epssLastUpdated < datetime() - duration('P7D')
        RETURN cve.cveId AS cveId
        ORDER BY cve.publishedDate DESC
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, {'limit': limit})
            return [record['cveId'] for record in result]

    def fetch_epss_batch(self, cve_ids: List[str]) -> Dict[str, Dict]:
        """Fetch EPSS scores for a batch of CVEs."""
        if not cve_ids:
            return {}

        # EPSS API accepts comma-separated CVE IDs
        params = {
            'cve': ','.join(cve_ids)
        }

        headers = {
            'Accept': 'application/json'
        }

        if EPSS_API_KEY:
            headers['Authorization'] = f'Bearer {EPSS_API_KEY}'

        try:
            response = requests.get(
                EPSS_API_BASE,
                params=params,
                headers=headers,
                timeout=30
            )
            self.stats['api_calls'] += 1

            if response.status_code == 200:
                data = response.json()
                result = {}
                for item in data.get('data', []):
                    cve_id = item.get('cve')
                    if cve_id:
                        result[cve_id] = {
                            'epssScore': float(item.get('epss', 0)),
                            'epssPercentile': float(item.get('percentile', 0)),
                            'modelVersion': data.get('model_version'),
                            'scoreDate': data.get('score_date')
                        }
                return result
            elif response.status_code == 429:
                # Rate limited - wait and retry
                logger.warning("Rate limited, waiting 60 seconds...")
                time.sleep(60)
                return self.fetch_epss_batch(cve_ids)
            else:
                logger.warning(f"EPSS API returned {response.status_code}")
                return {}

        except Exception as e:
            logger.error(f"EPSS API error: {e}")
            self.stats['errors'].append(str(e))
            return {}

    def update_cve_epss(self, cve_id: str, epss_data: Dict):
        """Update a CVE node with EPSS data."""
        query = """
        MATCH (cve:CVE {cveId: $cveId})
        SET cve.epssScore = $epssScore,
            cve.epssPercentile = $epssPercentile,
            cve.epssModelVersion = $modelVersion,
            cve.epssScoreDate = $scoreDate,
            cve.epssLastUpdated = datetime()
        RETURN cve.cveId AS cveId
        """

        with self.driver.session() as session:
            result = session.run(query, {
                'cveId': cve_id,
                'epssScore': epss_data.get('epssScore', 0),
                'epssPercentile': epss_data.get('epssPercentile', 0),
                'modelVersion': epss_data.get('modelVersion'),
                'scoreDate': epss_data.get('scoreDate')
            })
            if result.single():
                self.stats['cves_enriched'] += 1

    def enrich_all(self, batch_size: int = 100, max_cves: int = 10000):
        """Enrich all CVEs needing EPSS scores."""
        logger.info(f"Starting EPSS enrichment (max: {max_cves} CVEs)")

        # Get CVEs needing enrichment
        cve_ids = self.get_cve_ids_needing_epss(limit=max_cves)
        total = len(cve_ids)
        logger.info(f"Found {total} CVEs needing EPSS scores")

        if not cve_ids:
            logger.info("No CVEs need EPSS enrichment")
            return

        # Process in batches
        for i in range(0, total, batch_size):
            batch = cve_ids[i:i + batch_size]
            self.stats['cves_queried'] += len(batch)

            logger.info(f"Processing batch {i//batch_size + 1} ({i+1}-{min(i+batch_size, total)} of {total})")

            # Fetch EPSS scores
            epss_data = self.fetch_epss_batch(batch)

            # Update CVEs
            for cve_id, data in epss_data.items():
                self.update_cve_epss(cve_id, data)

            # Rate limit protection
            if i + batch_size < total:
                time.sleep(1)  # 1 second between batches

        logger.info("EPSS enrichment completed")

    def get_high_risk_cves(self, epss_threshold: float = 0.1, limit: int = 100) -> List[Dict]:
        """Get CVEs with high EPSS scores."""
        query = """
        MATCH (cve:CVE)
        WHERE cve.epssScore >= $threshold
        RETURN cve.cveId AS cveId,
               cve.epssScore AS epssScore,
               cve.epssPercentile AS percentile,
               cve.cvssBase AS cvssBase,
               cve.severity AS severity,
               cve.descriptionEN AS description
        ORDER BY cve.epssScore DESC
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, {
                'threshold': epss_threshold,
                'limit': limit
            })
            return [dict(record) for record in result]

    def create_indexes(self):
        """Create indexes for EPSS-related queries."""
        queries = [
            "CREATE INDEX cve_epss IF NOT EXISTS FOR (c:CVE) ON (c.epssScore)",
            "CREATE INDEX cve_epss_percentile IF NOT EXISTS FOR (c:CVE) ON (c.epssPercentile)"
        ]

        with self.driver.session() as session:
            for query in queries:
                try:
                    session.run(query)
                    logger.info(f"Executed: {query}")
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        logger.warning(f"Index creation warning: {e}")

    def print_stats(self):
        """Print enrichment statistics."""
        print("\n" + "="*50)
        print("EPSS Enrichment Statistics")
        print("="*50)
        print(f"CVEs queried:    {self.stats['cves_queried']}")
        print(f"CVEs enriched:   {self.stats['cves_enriched']}")
        print(f"API calls:       {self.stats['api_calls']}")
        if self.stats['errors']:
            print(f"Errors:          {len(self.stats['errors'])}")
        print("="*50)


def main():
    """Main entry point."""
    # Get Neo4j connection settings
    uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
    user = os.environ.get('NEO4J_USER', 'neo4j')
    password = os.environ.get('NEO4J_PASSWORD', 'neo4j@openspg')

    logger.info(f"Connecting to Neo4j at {uri}")

    try:
        enricher = EPSSEnricher(uri, user, password)

        # Create indexes
        enricher.create_indexes()

        # Determine mode from command line
        if len(sys.argv) > 1:
            if sys.argv[1] == '--high-risk':
                # Show high-risk CVEs
                threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
                high_risk = enricher.get_high_risk_cves(epss_threshold=threshold)
                print(f"\nHigh-risk CVEs (EPSS >= {threshold}):")
                print("-" * 80)
                for cve in high_risk[:20]:
                    print(f"{cve['cveId']}: EPSS={cve['epssScore']:.4f}, "
                          f"Percentile={cve['percentile']:.2f}%, "
                          f"CVSS={cve['cvssBase']}")
                return

            elif sys.argv[1] == '--batch':
                # Process specific batch size
                batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 100
                max_cves = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
                enricher.enrich_all(batch_size=batch_size, max_cves=max_cves)
        else:
            # Default: enrich all
            enricher.enrich_all()

        # Print statistics
        enricher.print_stats()

    except Exception as e:
        logger.error(f"Error: {e}")
        raise
    finally:
        enricher.close()


if __name__ == '__main__':
    main()
