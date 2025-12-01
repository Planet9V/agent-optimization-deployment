#!/usr/bin/env python3
"""
Extract CVE→CWE mappings directly from NVD Data Feeds
Downloads and processes NVD JSON files to create relationships
"""

import requests
import json
import gzip
from neo4j import GraphDatabase
from pathlib import Path
import time
from typing import Dict, List, Set

# Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# NVD Data Feed URLs (JSON 1.1 format - still active)
NVD_FEED_BASE = "https://nvd.nist.gov/feeds/json/cve/1.1"
YEARS = list(range(2020, 2026))  # 2020-2025

# Download directory
DOWNLOAD_DIR = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/nvd_feeds")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

class NVDCWEExtractor:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.stats = {
            'files_processed': 0,
            'cves_with_cwe': 0,
            'relationships_created': 0,
            'cve_not_found': 0,
            'cwe_not_found': 0
        }

    def close(self):
        self.driver.close()

    def download_nvd_feed(self, year: int) -> Path:
        """Download NVD JSON feed for specific year"""
        filename = f"nvdcve-1.1-{year}.json.gz"
        url = f"{NVD_FEED_BASE}/{filename}"
        local_path = DOWNLOAD_DIR / filename
        json_path = DOWNLOAD_DIR / f"nvdcve-1.1-{year}.json"

        # Skip if already downloaded and extracted
        if json_path.exists():
            print(f"  {year}: Already downloaded")
            return json_path

        try:
            print(f"  {year}: Downloading from {url}...")
            response = requests.get(url, stream=True, timeout=120)
            response.raise_for_status()

            # Save gzipped file
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Extract gzip
            print(f"  {year}: Extracting...")
            with gzip.open(local_path, 'rb') as f_in:
                with open(json_path, 'wb') as f_out:
                    f_out.write(f_in.read())

            # Remove gzip file to save space
            local_path.unlink()

            print(f"  {year}: Downloaded and extracted to {json_path}")
            return json_path

        except Exception as e:
            print(f"  {year}: Error downloading - {e}")
            return None

    def extract_cwe_ids(self, cve_item: Dict) -> List[str]:
        """Extract CWE IDs from CVE JSON (NVD 1.1 format)"""
        cwe_ids = []

        try:
            problemtype = cve_item.get('cve', {}).get('problemtype', {})
            for problemtype_data in problemtype.get('problemtype_data', []):
                for description in problemtype_data.get('description', []):
                    value = description.get('value', '')
                    if value.startswith('CWE-'):
                        cwe_ids.append(value)
        except Exception as e:
            pass

        return list(set(cwe_ids))  # Remove duplicates

    def create_relationships_batch(self, cve_cwe_mappings: List[tuple]) -> int:
        """Create CVE→CWE relationships in batch"""
        if not cve_cwe_mappings:
            return 0

        with self.driver.session() as session:
            result = session.run("""
                UNWIND $mappings AS mapping
                MATCH (cve:CVE)
                WHERE cve.id = mapping.cve_id
                WITH cve, mapping
                MATCH (cwe:CWE)
                WHERE cwe.cwe_id = mapping.cwe_number OR cwe.id = mapping.cwe_id_full
                MERGE (cve)-[r:HAS_WEAKNESS]->(cwe)
                RETURN count(r) AS created
            """, mappings=cve_cwe_mappings)

            record = result.single()
            return record['created'] if record else 0

    def process_nvd_file(self, json_path: Path):
        """Process NVD JSON file and create relationships"""
        if not json_path or not json_path.exists():
            return

        print(f"\nProcessing: {json_path.name}")

        try:
            with open(json_path, 'r') as f:
                data = json.load(f)

            cve_items = data.get('CVE_Items', [])
            print(f"  Total CVEs in file: {len(cve_items):,}")

            # Collect all CVE→CWE mappings
            mappings = []

            for item in cve_items:
                cve_id = item.get('cve', {}).get('CVE_data_meta', {}).get('ID', '')
                if not cve_id:
                    continue

                cwe_ids = self.extract_cwe_ids(item)

                if cwe_ids:
                    self.stats['cves_with_cwe'] += 1

                    for cwe_id in cwe_ids:
                        cwe_number = cwe_id.replace('CWE-', '')
                        mappings.append({
                            'cve_id': cve_id,
                            'cwe_id_full': cwe_id.lower(),  # e.g., "cwe-79"
                            'cwe_number': cwe_number         # e.g., "79"
                        })

            # Create relationships in batches of 1000
            batch_size = 1000
            total_created = 0

            for i in range(0, len(mappings), batch_size):
                batch = mappings[i:i + batch_size]
                created = self.create_relationships_batch(batch)
                total_created += created

                if (i // batch_size + 1) % 10 == 0:
                    print(f"  Progress: {i + len(batch):,}/{len(mappings):,} processed, "
                          f"{total_created:,} relationships created")

            self.stats['relationships_created'] += total_created
            self.stats['files_processed'] += 1

            print(f"  CVEs with CWE data: {len(set(m['cve_id'] for m in mappings)):,}")
            print(f"  Relationships created: {total_created:,}")

        except Exception as e:
            print(f"  Error processing file: {e}")

    def run_extraction(self):
        """Main extraction process"""
        print("=== CVE→CWE Mapping Extraction from NVD ===\n")

        # Get existing counts
        with self.driver.session() as session:
            result = session.run("MATCH (cve:CVE) RETURN count(cve) AS count")
            cve_count = result.single()['count']

            result = session.run("MATCH (cwe:CWE) RETURN count(cwe) AS count")
            cwe_count = result.single()['count']

            result = session.run("""
                MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
                RETURN count(r) AS count
            """)
            existing_relationships = result.single()['count']

        print(f"Current state:")
        print(f"  CVEs in database: {cve_count:,}")
        print(f"  CWEs in database: {cwe_count:,}")
        print(f"  Existing CVE→CWE relationships: {existing_relationships:,}\n")

        # Download and process feeds
        print("Downloading NVD data feeds...\n")

        for year in YEARS:
            json_path = self.download_nvd_feed(year)
            if json_path:
                self.process_nvd_file(json_path)
                time.sleep(1)  # Be nice to NVD servers

        # Final statistics
        print("\n" + "="*60)
        print("EXTRACTION COMPLETE")
        print("="*60)
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"CVEs with CWE data: {self.stats['cves_with_cwe']:,}")
        print(f"Relationships created: {self.stats['relationships_created']:,}")
        print("="*60)

        # Verify final state
        with self.driver.session() as session:
            result = session.run("""
                MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
                RETURN count(r) AS count
            """)
            final_count = result.single()['count']

            print(f"\nFinal CVE→CWE relationship count: {final_count:,}")

            # Test complete chains
            result = session.run("""
                MATCH path = (t:Technique)-[:EXPLOITS]->(cwe:CWE)<-[:HAS_WEAKNESS]-(cve:CVE)
                RETURN count(path) AS complete_chains
            """)
            chains = result.single()['complete_chains']
            print(f"Complete attack chains (Technique→CWE→CVE): {chains:,}")

def main():
    extractor = NVDCWEExtractor()
    try:
        extractor.run_extraction()
    finally:
        extractor.close()

if __name__ == "__main__":
    main()
