#!/usr/bin/env python3
"""
Fix CAPEC→CWE relationships for complete attack chain validation
Creates bidirectional relationships and ensures AttackPattern→Weakness links exist
"""

from neo4j import GraphDatabase
import sys

# Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

def create_reverse_relationships(driver):
    """Create CAPEC→CWE (EXPLOITS_WEAKNESS) from existing CWE→CAPEC (ENABLES_ATTACK_PATTERN)"""

    with driver.session() as session:
        print("Creating CAPEC→CWE (EXPLOITS_WEAKNESS) relationships...")

        # Create reverse relationships from existing CWE→CAPEC
        result = session.run("""
            MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
            MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
            RETURN count(r) as created
        """)
        created = result.single()['created']
        print(f"✅ Created {created} CAPEC→CWE (EXPLOITS_WEAKNESS) relationships")

        return created

def link_attackpattern_to_weakness(driver):
    """Link AttackPattern nodes to Weakness nodes where CAPEC/CWE connections exist"""

    with driver.session() as session:
        print("\nLinking AttackPattern→Weakness via CAPEC/CWE mappings...")

        # Link AttackPattern to Weakness where AttackPattern has MAPS_TO_ATTACK to CAPEC
        # and CAPEC has EXPLOITS_WEAKNESS to CWE (which has MAPS_TO CWE:Weakness)
        result = session.run("""
            MATCH (ap:AttackPattern)-[:MAPS_TO_ATTACK]->(capec:CAPEC)
            MATCH (capec)-[:EXPLOITS_WEAKNESS]->(cwe:CWE)
            MATCH (cwe)-[:MAPS_TO]->(weakness:Weakness)
            MERGE (ap)-[r:EXPLOITS_WEAKNESS]->(weakness)
            RETURN count(r) as created
        """)
        created = result.single()['created']
        print(f"✅ Created {created} AttackPattern→Weakness relationships")

        return created

def verify_complete_chains(driver):
    """Verify complete attack chains exist"""

    with driver.session() as session:
        print("\n" + "="*80)
        print("VERIFICATION")
        print("="*80)

        # Count CAPEC→CWE relationships
        result = session.run("""
            MATCH (capec:CAPEC)-[r:EXPLOITS_WEAKNESS]->(cwe:CWE)
            RETURN count(r) as total
        """)
        capec_cwe = result.single()['total']
        print(f"CAPEC→CWE (EXPLOITS_WEAKNESS): {capec_cwe}")

        # Count AttackPattern→Weakness relationships
        result = session.run("""
            MATCH (ap:AttackPattern)-[r:EXPLOITS_WEAKNESS]->(w:Weakness)
            RETURN count(r) as total
        """)
        ap_weakness = result.single()['total']
        print(f"AttackPattern→Weakness (EXPLOITS_WEAKNESS): {ap_weakness}")

        # Count complete attack chains: Technique→AttackPattern→Weakness→Vulnerability
        result = session.run("""
            MATCH path = (t:Technique)-[:IMPLEMENTS_ATTACK]->
                         (ap:AttackPattern)-[:EXPLOITS_WEAKNESS]->
                         (w:Weakness)-[:CAN_LEAD_TO]->
                         (vuln:Vulnerability)
            RETURN count(DISTINCT path) as chains
        """)
        chains = result.single()['chains']
        print(f"Complete attack chains (Technique→AttackPattern→Weakness→Vulnerability): {chains}")

        # Sample chains
        if chains > 0:
            result = session.run("""
                MATCH path = (t:Technique)-[:IMPLEMENTS_ATTACK]->
                             (ap:AttackPattern)-[:EXPLOITS_WEAKNESS]->
                             (w:Weakness)-[:CAN_LEAD_TO]->
                             (vuln:Vulnerability)
                RETURN
                    t.technique_id as technique,
                    ap.name as attack_pattern,
                    w.name as weakness,
                    vuln.cveId as vulnerability
                LIMIT 5
            """)
            print("\nSample complete attack chains:")
            for record in result:
                print(f"  {record['technique']} → {record['attack_pattern']} → {record['weakness']} → {record['vulnerability']}")

        print("="*80)

        return {
            'capec_cwe': capec_cwe,
            'attackpattern_weakness': ap_weakness,
            'complete_chains': chains
        }

def main():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        # Create reverse CAPEC→CWE relationships
        capec_cwe_created = create_reverse_relationships(driver)

        # Link AttackPattern to Weakness
        ap_weakness_created = link_attackpattern_to_weakness(driver)

        # Verify complete chains
        stats = verify_complete_chains(driver)

        print("\n" + "="*80)
        print("FIX SUMMARY")
        print("="*80)
        print(f"CAPEC→CWE relationships created: {capec_cwe_created}")
        print(f"AttackPattern→Weakness relationships created: {ap_weakness_created}")
        print(f"Complete attack chains found: {stats['complete_chains']}")
        print("="*80)

        if stats['complete_chains'] > 0:
            print("\n✅ CAPEC→CWE relationship fix COMPLETE!")
            print("✅ Complete attack chains are now available!")
            return 0
        else:
            print("\n⚠️ Relationships created but no complete chains found")
            print("Additional investigation needed for Technique→AttackPattern or Weakness→Vulnerability links")
            return 1

    finally:
        driver.close()

if __name__ == "__main__":
    sys.exit(main())
