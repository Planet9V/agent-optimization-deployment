#!/usr/bin/env python3
"""
FINAL CWE Overlap Diagnosis - Using Correct Property Names
CWE uses: .id (lowercase) = 'cwe-123'
CWE also has: .cwe_id (numeric) = 123
CAPEC uses: .capecId (camelCase) = 'CAPEC-123'
"""

from neo4j import GraphDatabase
import json

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_cve_connected_cwes(driver):
    """Get CWE IDs from CVE relationships"""
    query = """
    MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
    WHERE cwe.id IS NOT NULL
    RETURN DISTINCT cwe.id AS cwe_string_id,
           cwe.cwe_id AS cwe_numeric_id
    ORDER BY cwe_string_id
    """
    with driver.session() as session:
        result = session.run(query)
        return [(r["cwe_string_id"], r["cwe_numeric_id"]) for r in result]

def get_capec_connected_cwes(driver):
    """Get CWE IDs from CAPEC relationships"""
    query = """
    MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
    WHERE cwe.id IS NOT NULL OR cwe.cwe_id IS NOT NULL
    RETURN DISTINCT cwe.id AS cwe_string_id,
           cwe.cwe_id AS cwe_numeric_id
    ORDER BY cwe_string_id
    """
    with driver.session() as session:
        result = session.run(query)
        return [(r["cwe_string_id"], r["cwe_numeric_id"]) for r in result]

def get_cve_cwe_capec_chains(driver):
    """Get complete CVE→CWE→CAPEC chains"""
    query = """
    MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
    WHERE cwe.id IS NOT NULL AND capec.capecId IS NOT NULL
    RETURN cve.id AS cve_id,
           cwe.id AS cwe_id,
           cwe.cwe_id AS cwe_numeric,
           cwe.name AS cwe_name,
           capec.capecId AS capec_id,
           capec.name AS capec_name
    LIMIT 100
    """
    with driver.session() as session:
        result = session.run(query)
        return [dict(r) for r in result]

def get_cwe_capec_samples(driver):
    """Get CWE→CAPEC relationships with correct property names"""
    query = """
    MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
    WHERE capec.capecId IS NOT NULL
    RETURN cwe.id AS cwe_string_id,
           cwe.cwe_id AS cwe_numeric_id,
           cwe.name AS cwe_name,
           capec.capecId AS capec_id,
           capec.name AS capec_name
    LIMIT 50
    """
    with driver.session() as session:
        result = session.run(query)
        return [dict(r) for r in result]

def main():
    print("=" * 80)
    print("FINAL CWE OVERLAP DIAGNOSIS - USING CORRECT PROPERTY NAMES")
    print("=" * 80)
    print("\nProperty name mappings:")
    print("  CVE:   .id (standard)")
    print("  CWE:   .id (string 'cwe-123') AND .cwe_id (numeric 123)")
    print("  CAPEC: .capecId (string 'CAPEC-123')")
    print("=" * 80)

    driver = get_driver()

    try:
        # Get CVE-connected CWEs
        print("\n[1] CVE-connected CWEs (via IS_WEAKNESS_TYPE)...")
        cve_cwes = get_cve_connected_cwes(driver)
        cve_string_ids = {cwe[0] for cwe in cve_cwes if cwe[0]}
        cve_numeric_ids = {cwe[1] for cwe in cve_cwes if cwe[1]}
        print(f"  ✓ {len(cve_cwes)} unique CWEs")
        print(f"  ✓ {len(cve_string_ids)} with string IDs (e.g., 'cwe-123')")
        print(f"  ✓ {len(cve_numeric_ids)} with numeric IDs (e.g., 123)")
        print(f"  Examples: {list(cve_string_ids)[:5]}")

        # Get CAPEC-connected CWEs
        print("\n[2] CAPEC-connected CWEs (via ENABLES_ATTACK_PATTERN)...")
        capec_cwes = get_capec_connected_cwes(driver)
        capec_string_ids = {cwe[0] for cwe in capec_cwes if cwe[0]}
        capec_numeric_ids = {cwe[1] for cwe in capec_cwes if cwe[1]}
        print(f"  ✓ {len(capec_cwes)} unique CWEs")
        print(f"  ✓ {len(capec_string_ids)} with string IDs")
        print(f"  ✓ {len(capec_numeric_ids)} with numeric IDs")
        print(f"  Examples: {list(capec_string_ids)[:5]}")

        # Check overlaps
        print("\n[3] Overlap Analysis...")
        string_overlap = cve_string_ids & capec_string_ids
        numeric_overlap = cve_numeric_ids & capec_numeric_ids

        print(f"  String ID overlap: {len(string_overlap)} CWEs")
        if string_overlap:
            print(f"  Examples: {list(string_overlap)[:10]}")

        print(f"  Numeric ID overlap: {len(numeric_overlap)} CWE numbers")
        if numeric_overlap:
            print(f"  Examples: {list(numeric_overlap)[:10]}")

        # Get complete chains
        print("\n[4] Complete CVE→CWE→CAPEC Attack Chains...")
        chains = get_cve_cwe_capec_chains(driver)
        print(f"  ✓ Found {len(chains)} complete attack chains!")

        if chains:
            print("\n  Sample chains:")
            for i, chain in enumerate(chains[:10], 1):
                print(f"    {i}. {chain['cve_id']} → {chain['cwe_id']} → {chain['capec_id']}")
                print(f"       CWE: {chain['cwe_name']}")
                print(f"       CAPEC: {chain['capec_name']}")

        # Get CWE→CAPEC samples
        print("\n[5] CWE→CAPEC Relationship Samples...")
        cwe_capec_samples = get_cwe_capec_samples(driver)
        print(f"  Retrieved {len(cwe_capec_samples)} samples:")
        for i, sample in enumerate(cwe_capec_samples[:10], 1):
            print(f"    {i}. {sample['cwe_string_id']} ({sample['cwe_numeric_id']}) → {sample['capec_id']}")

        # Create comprehensive report
        report = {
            "executive_summary": {
                "cve_connected_cwes": len(cve_cwes),
                "capec_connected_cwes": len(capec_cwes),
                "string_id_overlap": len(string_overlap),
                "numeric_id_overlap": len(numeric_overlap),
                "complete_attack_chains": len(chains)
            },
            "property_mapping": {
                "cve": ".id",
                "cwe": {
                    "string_id": ".id (e.g., 'cwe-123')",
                    "numeric_id": ".cwe_id (e.g., 123)"
                },
                "capec": ".capecId (e.g., 'CAPEC-123')"
            },
            "overlap_details": {
                "string_ids": {
                    "overlap_count": len(string_overlap),
                    "examples": list(string_overlap)[:50]
                },
                "numeric_ids": {
                    "overlap_count": len(numeric_overlap),
                    "examples": list(numeric_overlap)[:50]
                }
            },
            "cve_connected_cwe_samples": [
                {"string_id": cwe[0], "numeric_id": cwe[1]}
                for cwe in cve_cwes[:50]
            ],
            "capec_connected_cwe_samples": [
                {"string_id": cwe[0], "numeric_id": cwe[1]}
                for cwe in capec_cwes[:50]
            ],
            "attack_chains": chains,
            "cwe_capec_samples": cwe_capec_samples
        }

        output_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/analysis_results/FINAL_CWE_OVERLAP_DIAGNOSIS.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✓ Complete report saved to: {output_file}")

        # Final diagnosis
        print("\n" + "=" * 80)
        print("ROOT CAUSE DIAGNOSIS")
        print("=" * 80)

        if len(chains) > 0:
            print(f"\n✅ SUCCESS: Found {len(chains)} complete CVE→CWE→CAPEC chains!")
            print("\nPrevious validation showed 0 chains because:")
            print("  1. CAPEC property is 'capecId' (camelCase), not '.id'")
            print("  2. Query was looking for .id which is NULL for all CAPECs")
            print("\nCorrection needed in validator:")
            print("  - Change: WHERE capec.id IS NOT NULL")
            print("  - To: WHERE capec.capecId IS NOT NULL")
        else:
            print("\n⚠️  Still no complete chains found")
            print(f"  - CVE→CWE: {len(cve_cwes)} connections exist")
            print(f"  - CWE→CAPEC: {len(capec_cwes)} connections exist")
            print(f"  - String overlap: {len(string_overlap)}")
            print(f"  - Numeric overlap: {len(numeric_overlap)}")

        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE - REAL DATABASE DATA")
        print("=" * 80)

    finally:
        driver.close()

if __name__ == "__main__":
    main()
