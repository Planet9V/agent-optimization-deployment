#!/usr/bin/env python3
"""
Create Transitive CWE→CAPEC Relationships via Hierarchy
Bridges CVE-CWEs to CAPEC-CWEs using parent-child relationships
"""

from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"


class TransitiveRelationshipCreator:
    """Create transitive CAPEC relationships through CWE hierarchy"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            'relationships_created': 0,
            'cves_bridged': 0
        }

    def close(self):
        """Close database connection"""
        self.driver.close()

    def create_transitive_relationships(self, max_hops: int = 5):
        """
        Create transitive ENABLES_ATTACK_PATTERN relationships

        If CWE-A has CVEs and CWE-A is ChildOf CWE-B (up to max_hops),
        and CWE-B has CAPEC, then create CWE-A → CAPEC relationship
        """
        print(f"Creating transitive relationships (max {max_hops} hops)...")

        with self.driver.session() as session:
            # Create transitive relationships through hierarchy
            result = session.run(f"""
                MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe_child:CWE)
                MATCH (cwe_child)-[:CHILDOF*1..{max_hops}]->(cwe_parent:CWE)
                MATCH (cwe_parent)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)

                // Only create if relationship doesn't already exist
                WHERE NOT (cwe_child)-[:ENABLES_ATTACK_PATTERN]->(capec)

                // Create the transitive relationship
                MERGE (cwe_child)-[r:ENABLES_ATTACK_PATTERN]->(capec)
                SET r.transitive = true,
                    r.created_via = 'hierarchy_bridge'

                RETURN count(DISTINCT r) as relationships_created,
                       count(DISTINCT cve) as cves_bridged
            """)

            record = result.single()
            self.stats['relationships_created'] = record['relationships_created']
            self.stats['cves_bridged'] = record['cves_bridged']

            print(f"  Created {self.stats['relationships_created']} transitive relationships")
            print(f"  Bridged {self.stats['cves_bridged']} CVEs to CAPEC")

    def verify_chains(self):
        """Verify complete attack chains now exist"""
        print()
        print("Verifying complete attack chains...")

        with self.driver.session() as session:
            # Count complete chains
            result = session.run("""
                MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
                      -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                      -[:USES_TECHNIQUE]->(attack:AttackTechnique)
                RETURN count(DISTINCT cve) as complete_chains
            """)
            complete_chains = result.single()['complete_chains']

            # Get sample chains
            result = session.run("""
                MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
                      -[r_capec:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                      -[:USES_TECHNIQUE]->(attack:AttackTechnique)
                RETURN cve.id as cve_id,
                       cwe.id as cwe_id,
                       capec.id as capec_id,
                       attack.id as attack_id,
                       r_capec.transitive as is_transitive
                LIMIT 10
            """)
            samples = list(result)

            print()
            print("="*80)
            print("  CHAIN VERIFICATION")
            print("="*80)
            print(f"Complete CVE→CWE→CAPEC→ATT&CK chains: {complete_chains}")
            print()

            if samples:
                print("Sample chains:")
                print("CVE ID         CWE ID      CAPEC ID    ATT&CK ID     Transitive")
                print("-"*80)
                for record in samples:
                    transitive = "✓" if record['is_transitive'] else " "
                    print(f"{record['cve_id']:<14} {record['cwe_id']:<11} "
                          f"{record['capec_id']:<11} {record['attack_id']:<13} {transitive}")
                print()

            if complete_chains >= 124:
                print("🎉 SUCCESS! Minimum threshold of 124 chains achieved!")
            else:
                shortfall = 124 - complete_chains
                print(f"⚠ Need {shortfall} more chains to reach 124 threshold")

            return complete_chains

    def analyze_coverage(self):
        """Analyze CWE coverage improvements"""
        print()
        print("Analyzing coverage improvements...")

        with self.driver.session() as session:
            # CWEs with CAPEC relationships before/after
            result = session.run("""
                MATCH (cwe:CWE)-[r:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                RETURN
                    count(DISTINCT cwe) as total_cwes_with_capec,
                    sum(CASE WHEN r.transitive = true THEN 1 ELSE 0 END) as transitive_links,
                    sum(CASE WHEN r.transitive IS NULL OR r.transitive = false THEN 1 ELSE 0 END) as direct_links
            """)
            record = result.single()

            print()
            print("CWE→CAPEC Coverage:")
            print(f"  Total CWEs with CAPEC links: {record['total_cwes_with_capec']}")
            print(f"  Direct links:                {record['direct_links']}")
            print(f"  Transitive links (new):      {record['transitive_links']}")


def main():
    """Main execution"""
    print("="*80)
    print("  CREATE TRANSITIVE CWE→CAPEC RELATIONSHIPS")
    print("="*80)
    print()

    creator = None
    try:
        creator = TransitiveRelationshipCreator(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

        # Create transitive relationships
        creator.create_transitive_relationships(max_hops=5)

        # Analyze coverage
        creator.analyze_coverage()

        # Verify complete chains
        complete_chains = creator.verify_chains()

        # Summary
        print()
        print("="*80)
        print("  SUMMARY")
        print("="*80)
        print(f"Transitive relationships created: {creator.stats['relationships_created']}")
        print(f"CVEs bridged to CAPEC:            {creator.stats['cves_bridged']}")
        print(f"Complete attack chains:           {complete_chains}")
        print()

        if complete_chains >= 124:
            print("✅ VALIDATION SUCCESS: Minimum threshold achieved!")
            return 0
        else:
            print("⚠ VALIDATION PENDING: Below minimum threshold")
            return 1

    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        if creator:
            creator.close()


if __name__ == "__main__":
    exit(main())
