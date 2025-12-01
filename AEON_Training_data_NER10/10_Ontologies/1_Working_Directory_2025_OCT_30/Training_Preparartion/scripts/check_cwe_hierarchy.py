#!/usr/bin/env python3
"""
Check if CWE hierarchy relationships exist in database
"""

from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def check_hierarchy():
    """Check for CWE parent-child relationships"""

    with driver.session() as session:
        # Check for CHILDOF relationships
        result = session.run("""
            MATCH (cwe1:CWE)-[r:CHILDOF]->(cwe2:CWE)
            RETURN count(r) as childof_count
        """)
        childof_count = result.single()['childof_count']

        # Check for PARENT relationships
        result = session.run("""
            MATCH (cwe1:CWE)-[r:PARENT]->(cwe2:CWE)
            RETURN count(r) as parent_count
        """)
        parent_count = result.single()['parent_count']

        # Get sample hierarchy
        result = session.run("""
            MATCH (cwe1:CWE)-[r:CHILDOF]->(cwe2:CWE)
            RETURN cwe1.id as child, cwe2.id as parent
            LIMIT 10
        """)
        samples = list(result)

        print("="*80)
        print("  CWE HIERARCHY CHECK")
        print("="*80)
        print()
        print(f"CHILDOF relationships: {childof_count}")
        print(f"PARENT relationships:  {parent_count}")
        print()

        if childof_count > 0:
            print("✓ CWE hierarchy exists!")
            print()
            print("Sample relationships:")
            for record in samples:
                print(f"  {record['child']} → {record['parent']}")
            print()
            print("SOLUTION: Use hierarchy to bridge CVE-CWEs to CAPEC-CWEs")
        else:
            print("✗ NO CWE hierarchy found in database")
            print()
            print("SOLUTION: Import CWE hierarchy from cwec_v4.18.xml")

        # Check if hierarchy could bridge the gap
        if childof_count > 0:
            result = session.run("""
                MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe1:CWE)
                MATCH (cwe1)-[:CHILDOF*1..5]->(cwe2:CWE)
                MATCH (cwe2)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                RETURN count(DISTINCT cve) as bridgeable_cves
            """)
            bridgeable = result.single()['bridgeable_cves']

            print()
            print(f"CVEs that could be bridged via hierarchy: {bridgeable}")

if __name__ == "__main__":
    try:
        check_hierarchy()
    finally:
        driver.close()
