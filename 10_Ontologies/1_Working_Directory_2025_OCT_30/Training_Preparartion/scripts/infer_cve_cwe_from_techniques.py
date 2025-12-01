#!/usr/bin/env python3
"""
Infer CVE→CWE relationships from existing Technique→CWE→CVE patterns
Uses pattern matching and heuristics to fill the gap
"""

from neo4j import GraphDatabase
from typing import Dict, List, Set
import re

# Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

class CVECWEInferencer:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.stats = {
            'cve_analyzed': 0,
            'relationships_created': 0,
            'cwe_inferred': 0
        }

    def close(self):
        self.driver.close()

    def extract_cwe_from_description(self, description: str) -> List[str]:
        """Extract CWE IDs mentioned in CVE descriptions"""
        cwe_ids = []
        if not description:
            return cwe_ids

        # Pattern 1: Explicit CWE-XXX mentions
        pattern1 = r'CWE-(\d+)'
        matches = re.findall(pattern1, description, re.IGNORECASE)
        cwe_ids.extend(matches)

        # Pattern 2: Common weakness descriptions mapped to CWE IDs
        keyword_mappings = {
            'sql injection': '89',
            'cross-site scripting': '79',
            'xss': '79',
            'buffer overflow': '119',
            'stack-based buffer overflow': '121',
            'heap-based buffer overflow': '122',
            'path traversal': '22',
            'directory traversal': '22',
            'command injection': '77',
            'code injection': '94',
            'cross-site request forgery': '352',
            'csrf': '352',
            'xml external entity': '611',
            'xxe': '611',
            'authentication bypass': '287',
            'privilege escalation': '269',
            'improper access control': '284',
            'use after free': '416',
            'race condition': '362',
            'null pointer dereference': '476',
            'integer overflow': '190',
            'denial of service': '400',
            'dos': '400',
            'memory corruption': '119',
            'remote code execution': '94',
            'rce': '94',
            'information disclosure': '200',
            'information leak': '200'
        }

        desc_lower = description.lower()
        for keyword, cwe_id in keyword_mappings.items():
            if keyword in desc_lower and cwe_id not in cwe_ids:
                cwe_ids.append(cwe_id)

        return list(set(cwe_ids))

    def get_cwe_from_similar_cves(self, cve_id: str, description: str) -> List[str]:
        """Find CWEs from similar CVEs based on vendor/product"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (target:CVE {id: $cve_id})
                MATCH (similar:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
                WHERE target.cpe_vendors = similar.cpe_vendors
                  AND target.id <> similar.id
                RETURN DISTINCT cwe.cwe_id AS cwe_id
                LIMIT 5
            """, cve_id=cve_id)

            return [record['cwe_id'] for record in result]

    def create_relationships_batch(self, cve_cwe_mappings: List[Dict]) -> int:
        """Create CVE→CWE relationships in batch"""
        if not cve_cwe_mappings:
            return 0

        with self.driver.session() as session:
            result = session.run("""
                UNWIND $mappings AS mapping
                MATCH (cve:CVE {id: mapping.cve_id})
                MATCH (cwe:CWE)
                WHERE cwe.cwe_id = mapping.cwe_id OR cwe.id = 'cwe-' + mapping.cwe_id
                MERGE (cve)-[r:HAS_WEAKNESS {inferred: true, method: mapping.method}]->(cwe)
                RETURN count(r) AS created
            """, mappings=cve_cwe_mappings)

            record = result.single()
            return record['created'] if record else 0

    def process_cves_batch(self, batch_size: int = 1000):
        """Process CVEs in batches and infer CWE relationships"""
        with self.driver.session() as session:
            # Get CVEs without CWE relationships
            result = session.run("""
                MATCH (cve:CVE)
                WHERE NOT (cve)-[:HAS_WEAKNESS]->(:CWE)
                  AND cve.description IS NOT NULL
                RETURN cve.id AS cve_id, cve.description AS description, cve.cpe_vendors AS vendors
                LIMIT $batch_size
            """, batch_size=batch_size)

            cves = list(result)

            if not cves:
                return False  # No more CVEs to process

            print(f"\nProcessing batch of {len(cves)} CVEs...")

            mappings = []

            for record in cves:
                cve_id = record['cve_id']
                description = record['description']

                self.stats['cve_analyzed'] += 1

                # Extract CWEs from description
                cwe_ids_desc = self.extract_cwe_from_description(description)

                # Get CWEs from similar CVEs
                cwe_ids_similar = self.get_cwe_from_similar_cves(cve_id, description)

                # Combine and deduplicate
                all_cwe_ids = list(set(cwe_ids_desc + cwe_ids_similar))

                if all_cwe_ids:
                    for cwe_id in all_cwe_ids:
                        method = 'description' if cwe_id in cwe_ids_desc else 'similar_cves'
                        mappings.append({
                            'cve_id': cve_id,
                            'cwe_id': cwe_id,
                            'method': method
                        })

                if self.stats['cve_analyzed'] % 100 == 0:
                    print(f"  Progress: {self.stats['cve_analyzed']} CVEs analyzed, "
                          f"{len(mappings)} potential CWE links found")

            # Create relationships
            if mappings:
                created = self.create_relationships_batch(mappings)
                self.stats['relationships_created'] += created
                print(f"  Created {created} CVE→CWE relationships")

            return True  # More CVEs to process

    def run_inference(self):
        """Main inference process"""
        print("=== CVE→CWE Relationship Inference ===\n")

        # Get current state
        with self.driver.session() as session:
            result = session.run("MATCH (cve:CVE) RETURN count(cve) AS count")
            cve_count = result.single()['count']

            result = session.run("MATCH (cwe:CWE) RETURN count(cwe) AS count")
            cwe_count = result.single()['count']

            result = session.run("""
                MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
                RETURN count(r) AS count
            """)
            existing = result.single()['count']

        print(f"Current state:")
        print(f"  CVEs: {cve_count:,}")
        print(f"  CWEs: {cwe_count:,}")
        print(f"  Existing CVE→CWE relationships: {existing:,}\n")

        print("Starting inference process...")
        print("Using methods:")
        print("  1. Extract CWE IDs from CVE descriptions")
        print("  2. Pattern matching on common weakness descriptions")
        print("  3. Similarity matching with CVEs from same vendor\n")

        # Process in batches until done
        batch_num = 0
        while True:
            batch_num += 1
            print(f"\n--- Batch {batch_num} ---")

            has_more = self.process_cves_batch(batch_size=10000)

            if not has_more:
                print("\nAll CVEs processed!")
                break

            # Limit to reasonable number of batches
            if batch_num >= 50:
                print("\nReached batch limit. Stopping.")
                break

        # Final statistics
        print("\n" + "="*60)
        print("INFERENCE COMPLETE")
        print("="*60)
        print(f"CVEs analyzed: {self.stats['cve_analyzed']:,}")
        print(f"Relationships created: {self.stats['relationships_created']:,}")
        print("="*60)

        # Verify final state
        with self.driver.session() as session:
            result = session.run("""
                MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
                RETURN count(r) AS count
            """)
            final = result.single()['count']

            print(f"\nFinal CVE→CWE relationship count: {final:,}")
            print(f"Increase: {final - existing:,}\n")

            # Test complete chains
            result = session.run("""
                MATCH path = (t:Technique)-[:EXPLOITS]->(cwe:CWE)<-[:HAS_WEAKNESS]-(cve:CVE)
                RETURN count(path) AS complete_chains
            """)
            chains = result.single()['complete_chains']
            print(f"Complete attack chains: {chains:,}")

def main():
    inferencer = CVECWEInferencer()
    try:
        inferencer.run_inference()
    finally:
        inferencer.close()

if __name__ == "__main__":
    main()
