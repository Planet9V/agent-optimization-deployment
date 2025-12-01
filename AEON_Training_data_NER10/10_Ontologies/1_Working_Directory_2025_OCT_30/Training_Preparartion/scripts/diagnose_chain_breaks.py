#!/usr/bin/env python3
"""
Diagnose where attack chains are breaking
"""

from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def diagnose_breaks():
    """Check each link in the chain"""

    with driver.session() as session:
        print("="*80)
        print("  ATTACK CHAIN BREAK DIAGNOSIS")
        print("="*80)
        print()

        # 1. CVE → CWE
        result = session.run("""
            MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
            RETURN count(DISTINCT cve) as cve_count,
                   count(DISTINCT cwe) as cwe_count
        """)
        record = result.single()
        print(f"1. CVE → CWE:")
        print(f"   CVEs with CWE links:  {record['cve_count']}")
        print(f"   Unique CWEs linked:   {record['cwe_count']}")
        print()

        # 2. CWE → CAPEC
        result = session.run("""
            MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
            RETURN count(DISTINCT cwe) as cwe_count,
                   count(DISTINCT capec) as capec_count
        """)
        record = result.single()
        print(f"2. CWE → CAPEC:")
        print(f"   CWEs with CAPEC links: {record['cwe_count']}")
        print(f"   Unique CAPECs linked:  {record['capec_count']}")
        print()

        # 3. CAPEC → ATT&CK
        result = session.run("""
            MATCH (capec:CAPEC)-[:USES_TECHNIQUE]->(attack:AttackTechnique)
            RETURN count(DISTINCT capec) as capec_count,
                   count(DISTINCT attack) as attack_count
        """)
        record = result.single()
        print(f"3. CAPEC → ATT&CK:")
        print(f"   CAPECs with ATT&CK links: {record['capec_count']}")
        print(f"   Unique ATT&CK techniques: {record['attack_count']}")
        print()

        # 4. Check CVE → CWE → CAPEC (partial chain)
        result = session.run("""
            MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
                  -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
            RETURN count(DISTINCT cve) as cve_count,
                   count(DISTINCT capec) as capec_count
        """)
        record = result.single()
        print(f"4. CVE → CWE → CAPEC (partial chain):")
        print(f"   CVEs reaching CAPEC:  {record['cve_count']}")
        print(f"   CAPECs reached:       {record['capec_count']}")
        print()

        # 5. Check CWE → CAPEC → ATT&CK (partial chain)
        result = session.run("""
            MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                  -[:USES_TECHNIQUE]->(attack:AttackTechnique)
            RETURN count(DISTINCT cwe) as cwe_count,
                   count(DISTINCT capec) as capec_count,
                   count(DISTINCT attack) as attack_count
        """)
        record = result.single()
        print(f"5. CWE → CAPEC → ATT&CK (partial chain):")
        print(f"   CWEs reaching ATT&CK: {record['cwe_count']}")
        print(f"   CAPECs with ATT&CK:   {record['capec_count']}")
        print(f"   ATT&CK techniques:    {record['attack_count']}")
        print()

        # 6. Check complete chain
        result = session.run("""
            MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
                  -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                  -[:USES_TECHNIQUE]->(attack:AttackTechnique)
            RETURN count(DISTINCT cve) as complete_chains
        """)
        record = result.single()
        print(f"6. Complete CVE → CWE → CAPEC → ATT&CK:")
        print(f"   Complete chains: {record['complete_chains']}")
        print()

        # 7. Find where chains break
        print("="*80)
        print("  BOTTLENECK ANALYSIS")
        print("="*80)
        print()

        # Check CVE-CWEs that reach CAPEC but no ATT&CK
        result = session.run("""
            MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
                  -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
            WHERE NOT (capec)-[:USES_TECHNIQUE]->(:AttackTechnique)
            RETURN count(DISTINCT cve) as broken_cves,
                   count(DISTINCT capec) as capecs_without_attack,
                   collect(DISTINCT capec.id)[0..10] as sample_capecs
        """)
        record = result.single()

        if record['broken_cves'] > 0:
            print(f"❌ BOTTLENECK: CAPEC → ATT&CK")
            print(f"   {record['broken_cves']} CVEs reach CAPEC but can't reach ATT&CK")
            print(f"   {record['capecs_without_attack']} CAPECs lack ATT&CK links")
            print(f"   Sample CAPECs without ATT&CK: {record['sample_capecs']}")
            print()
            print("   SOLUTION: Import CAPEC→ATT&CK relationships")
        else:
            print("✓ All CAPECs have ATT&CK links")

        print()

        # Check CVE-CWEs that don't reach CAPEC
        result = session.run("""
            MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
            WHERE NOT (cwe)-[:ENABLES_ATTACK_PATTERN]->(:CAPEC)
            RETURN count(DISTINCT cve) as broken_cves,
                   count(DISTINCT cwe) as cwes_without_capec,
                   collect(DISTINCT cwe.id)[0..10] as sample_cwes
        """)
        record = result.single()

        if record['broken_cves'] > 0:
            print(f"❌ BOTTLENECK: CWE → CAPEC")
            print(f"   {record['broken_cves']} CVEs can't reach CAPEC")
            print(f"   {record['cwes_without_capec']} CWEs lack CAPEC links")
            print(f"   Sample CWEs without CAPEC: {record['sample_cwes']}")
            print()
            print("   SOLUTION: Expand CWE hierarchy traversal or import more CWE→CAPEC links")
        else:
            print("✓ All CVE-CWEs can reach CAPEC")


if __name__ == "__main__":
    try:
        diagnose_breaks()
    finally:
        driver.close()
