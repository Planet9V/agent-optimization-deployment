#!/usr/bin/env python3
"""
Import CVE→CWE mappings from NVD API
Rapidly creates relationships between existing CVE and CWE nodes
"""

import requests
import time
from neo4j import GraphDatabase
from datetime import datetime, timedelta
import json
from typing import Set, Dict, List
import sys

# Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# NVD API configuration
NVD_API_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
RATE_LIMIT_DELAY = 6  # 10 requests per minute = 6 seconds between requests

class CVECWEImporter:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.stats = {
            'cves_processed': 0,
            'cwe_relationships_created': 0,
            'cves_with_no_cwe': 0,
            'errors': 0
        }

    def close(self):
        self.driver.close()

    def get_existing_cve_ids(self, limit: int = None) -> Set[str]:
        """Get CVE IDs already in Neo4j"""
        with self.driver.session() as session:
            query = "MATCH (cve:CVE) RETURN cve.id AS id"
            if limit:
                query += f" LIMIT {limit}"
            result = session.run(query)
            return {record['id'] for record in result}

    def get_existing_cwe_ids(self) -> Set[str]:
        """Get CWE IDs already in Neo4j"""
        with self.driver.session() as session:
            result = session.run("MATCH (cwe:Weakness) RETURN cwe.cwe_id AS id")
            return {record['id'] for record in result}

    def create_cve_cwe_relationship(self, cve_id: str, cwe_ids: List[str]) -> int:
        """Create HAS_WEAKNESS relationships between CVE and CWE nodes"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (cve:CVE {id: $cve_id})
                WITH cve, $cwe_ids AS cwe_list
                UNWIND cwe_list AS cwe_id
                MATCH (cwe:Weakness)
                WHERE cwe.cwe_id = cwe_id OR cwe.id = cwe_id
                MERGE (cve)-[r:HAS_WEAKNESS]->(cwe)
                RETURN count(r) AS created
            """, cve_id=cve_id, cwe_ids=cwe_ids)
            record = result.single()
            return record['created'] if record else 0

    def extract_cwe_ids_from_nvd(self, cve_data: Dict) -> List[str]:
        """Extract CWE IDs from NVD CVE data"""
        cwe_ids = []

        try:
            if 'weaknesses' in cve_data.get('cve', {}):
                for weakness in cve_data['cve']['weaknesses']:
                    for desc in weakness.get('description', []):
                        cwe_value = desc.get('value', '')
                        if cwe_value.startswith('CWE-'):
                            cwe_ids.append(cwe_value)
        except Exception as e:
            print(f"Error extracting CWE IDs: {e}")

        return list(set(cwe_ids))  # Remove duplicates

    def query_nvd_api(self, start_date: str, end_date: str) -> List[Dict]:
        """Query NVD API for CVEs in date range"""
        params = {
            'pubStartDate': start_date,
            'pubEndDate': end_date,
            'resultsPerPage': 2000
        }

        try:
            print(f"Querying NVD API: {start_date} to {end_date}")
            response = requests.get(NVD_API_BASE, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            vulnerabilities = data.get('vulnerabilities', [])
            total_results = data.get('totalResults', 0)

            print(f"  Found {total_results} CVEs, retrieved {len(vulnerabilities)}")

            time.sleep(RATE_LIMIT_DELAY)  # Rate limiting
            return vulnerabilities

        except Exception as e:
            print(f"Error querying NVD API: {e}")
            self.stats['errors'] += 1
            return []

    def process_year_range(self, start_year: int, end_year: int):
        """Process CVEs for a year range"""
        for year in range(start_year, end_year + 1):
            start_date = f"{year}-01-01T00:00:00.000"
            end_date = f"{year}-12-31T23:59:59.999"

            vulnerabilities = self.query_nvd_api(start_date, end_date)

            for vuln in vulnerabilities:
                cve_data = vuln.get('cve', {})
                cve_id = cve_data.get('id', '')

                if not cve_id:
                    continue

                # Extract CWE IDs
                cwe_ids = self.extract_cwe_ids_from_nvd(cve_data)

                self.stats['cves_processed'] += 1

                if cwe_ids:
                    # Create relationships
                    created = self.create_cve_cwe_relationship(cve_id, cwe_ids)
                    self.stats['cwe_relationships_created'] += created

                    if created > 0:
                        print(f"  {cve_id}: Linked to {len(cwe_ids)} CWEs ({created} relationships created)")
                else:
                    self.stats['cves_with_no_cwe'] += 1

                # Progress update
                if self.stats['cves_processed'] % 100 == 0:
                    print(f"\nProgress: {self.stats['cves_processed']} CVEs processed, "
                          f"{self.stats['cwe_relationships_created']} relationships created")

    def quick_import_recent_years(self):
        """Quick import focusing on recent years with highest CWE coverage"""
        print("\n=== Starting CVE→CWE Mapping Import ===\n")

        # Get existing CVE and CWE counts
        with self.driver.session() as session:
            result = session.run("MATCH (cve:CVE) RETURN count(cve) AS count")
            cve_count = result.single()['count']

            result = session.run("MATCH (cwe:Weakness) RETURN count(cwe) AS count")
            cwe_count = result.single()['count']

            result = session.run("MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:Weakness) RETURN count(r) AS count")
            existing_relationships = result.single()['count']

        print(f"Existing data:")
        print(f"  CVEs: {cve_count:,}")
        print(f"  CWEs: {cwe_count:,}")
        print(f"  CVE→CWE relationships: {existing_relationships:,}\n")

        # Process years 2020-2025 (highest CWE coverage period)
        self.process_year_range(2020, 2025)

        # If we need more, process 2015-2019
        if self.stats['cwe_relationships_created'] < 50000:
            print("\nProcessing additional years to reach 50K target...")
            self.process_year_range(2015, 2019)

        # Final stats
        print("\n=== Import Complete ===")
        print(f"CVEs processed: {self.stats['cves_processed']:,}")
        print(f"CVE→CWE relationships created: {self.stats['cwe_relationships_created']:,}")
        print(f"CVEs with no CWE data: {self.stats['cves_with_no_cwe']:,}")
        print(f"Errors: {self.stats['errors']}")

        # Verify final state
        with self.driver.session() as session:
            result = session.run("MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:Weakness) RETURN count(r) AS count")
            final_relationships = result.single()['count']

            print(f"\nFinal CVE→CWE relationship count: {final_relationships:,}")

            # Test complete chain query
            result = session.run("""
                MATCH path = (t:Technique)-[:EXPLOITS]->(cwe:Weakness)<-[:HAS_WEAKNESS]-(cve:CVE)
                RETURN count(path) AS complete_chains
                LIMIT 1
            """)
            complete_chains = result.single()['complete_chains']
            print(f"Complete attack chains (Technique→CWE→CVE): {complete_chains:,}")

def main():
    importer = CVECWEImporter()
    try:
        importer.quick_import_recent_years()
    finally:
        importer.close()

if __name__ == "__main__":
    main()
