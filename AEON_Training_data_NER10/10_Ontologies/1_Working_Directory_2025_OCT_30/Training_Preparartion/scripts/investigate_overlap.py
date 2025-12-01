#!/usr/bin/env python3
"""
Investigation: CWE Overlap Analysis
Determines why CVE-CWEs don't connect to CAPEC-CWEs
"""

from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def investigate_overlap():
    """Check actual CWE IDs to find overlap"""

    with driver.session() as session:
        # Get CVE-connected CWEs
        result = session.run("""
            MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
            RETURN DISTINCT cwe.id as cwe_id
            ORDER BY cwe_id
            LIMIT 50
        """)
        cve_cwes = set(record['cwe_id'] for record in result)

        # Get CAPEC-connected CWEs
        result = session.run("""
            MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
            WHERE cwe.id IS NOT NULL
            RETURN DISTINCT cwe.id as cwe_id
            ORDER BY cwe_id
            LIMIT 50
        """)
        capec_cwes = set(record['cwe_id'] for record in result if record['cwe_id'] is not None)

        # Check overlap
        overlap = cve_cwes.intersection(capec_cwes)

        print("="*80)
        print("  CWE OVERLAP INVESTIGATION")
        print("="*80)
        print()
        print(f"CVE-connected CWEs (sample): {len(cve_cwes)}")
        print(f"First 10: {sorted(list(cve_cwes))[:10]}")
        print()
        print(f"CAPEC-connected CWEs (sample): {len(capec_cwes)}")
        print(f"First 10: {sorted(list(capec_cwes))[:10]}")
        print()
        print(f"Overlap: {len(overlap)}")
        if overlap:
            print(f"Overlapping CWEs: {sorted(list(overlap))[:20]}")

            # If overlap exists, check why chains still don't exist
            print()
            print("Checking chain completeness for overlapping CWEs...")
            for cwe_id in sorted(list(overlap))[:5]:
                result = session.run("""
                    MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE {id: $cwe_id})
                          -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                          -[:USES_TECHNIQUE]->(attack:AttackTechnique)
                    RETURN count(*) as chain_count
                """, cwe_id=cwe_id)
                record = result.single()
                print(f"  {cwe_id}: {record['chain_count']} complete chains")
        else:
            print("NO OVERLAP FOUND!")
            print()
            print("Root Cause: CVE-CWEs and CAPEC-CWEs are completely disjoint sets")

        print()
        print("="*80)

        # Check total counts
        result = session.run("MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE) RETURN count(DISTINCT cwe) as count")
        total_cve_cwes = result.single()['count']

        result = session.run("MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC) RETURN count(DISTINCT cwe) as count")
        total_capec_cwes = result.single()['count']

        print(f"Total CVE-connected CWEs: {total_cve_cwes}")
        print(f"Total CAPEC-connected CWEs: {total_capec_cwes}")

        # Get full overlap count
        result = session.run("""
            MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe1:CWE)
            MATCH (cwe2:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
            WHERE cwe1.id = cwe2.id
            RETURN count(DISTINCT cwe1) as overlap_count
        """)
        total_overlap = result.single()['overlap_count']

        print(f"Total overlapping CWEs: {total_overlap}")
        print(f"Overlap percentage: {(total_overlap / total_cve_cwes * 100):.1f}%")

if __name__ == "__main__":
    try:
        investigate_overlap()
    finally:
        driver.close()
