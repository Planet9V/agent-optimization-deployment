#!/usr/bin/env python3
"""
CWE Overlap Diagnosis Script
Analyzes why there's zero overlap between CVE-connected CWEs and CAPEC-connected CWEs
"""

from neo4j import GraphDatabase
import json
from collections import defaultdict

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

def get_driver():
    """Create Neo4j driver"""
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_cve_connected_cwes(driver):
    """Get all CWE IDs that have CVE relationships"""
    query = """
    MATCH (cve:CVE)-[:HAS_CWE]->(cwe:CWE)
    RETURN DISTINCT cwe.id AS cwe_id
    ORDER BY cwe_id
    """

    with driver.session() as session:
        result = session.run(query)
        return [record["cwe_id"] for record in result]

def get_capec_connected_cwes(driver):
    """Get all CWE IDs that have CAPEC relationships"""
    query = """
    MATCH (cwe:CWE)-[:CAN_FOLLOW|CAN_PRECEDE]->(capec:CAPEC)
    RETURN DISTINCT cwe.id AS cwe_id
    ORDER BY cwe_id
    """

    with driver.session() as session:
        result = session.run(query)
        return [record["cwe_id"] for record in result]

def get_sample_cve_cwe_relationships(driver, limit=20):
    """Get sample CVE->CWE relationships"""
    query = """
    MATCH (cve:CVE)-[:HAS_CWE]->(cwe:CWE)
    RETURN cve.id AS cve_id, cwe.id AS cwe_id, cwe.name AS cwe_name
    LIMIT $limit
    """

    with driver.session() as session:
        result = session.run(query, limit=limit)
        return [dict(record) for record in result]

def get_sample_cwe_capec_relationships(driver, limit=20):
    """Get sample CWE->CAPEC relationships"""
    query = """
    MATCH (cwe:CWE)-[r:CAN_FOLLOW|CAN_PRECEDE]->(capec:CAPEC)
    RETURN cwe.id AS cwe_id, cwe.name AS cwe_name,
           type(r) AS relationship_type, capec.id AS capec_id
    LIMIT $limit
    """

    with driver.session() as session:
        result = session.run(query, limit=limit)
        return [dict(record) for record in result]

def analyze_id_formats(cwe_ids):
    """Analyze the format patterns of CWE IDs"""
    formats = defaultdict(list)

    for cwe_id in cwe_ids[:50]:  # Sample first 50
        if cwe_id is None:
            formats['null'].append(cwe_id)
        elif cwe_id.startswith('CWE-'):
            formats['CWE-###'].append(cwe_id)
        elif cwe_id.startswith('cwe-'):
            formats['cwe-###'].append(cwe_id)
        elif cwe_id.isdigit():
            formats['### (numeric)'].append(cwe_id)
        else:
            formats['other'].append(cwe_id)

    return formats

def check_case_insensitive_overlap(cve_cwes, capec_cwes):
    """Check if there's overlap when ignoring case"""
    cve_cwes_lower = {cwe.lower() if cwe else '' for cwe in cve_cwes}
    capec_cwes_lower = {cwe.lower() if cwe else '' for cwe in capec_cwes}

    overlap = cve_cwes_lower & capec_cwes_lower
    return overlap

def main():
    """Execute the diagnosis"""
    print("=" * 80)
    print("CWE OVERLAP DIAGNOSIS - EXECUTING ACTUAL DATABASE QUERIES")
    print("=" * 80)

    driver = get_driver()

    try:
        # 1. Get CVE-connected CWEs
        print("\n[STEP 1] Querying CVE-connected CWEs...")
        cve_cwes = get_cve_connected_cwes(driver)
        print(f"✓ Found {len(cve_cwes)} unique CWEs connected to CVEs")

        # 2. Get CAPEC-connected CWEs
        print("\n[STEP 2] Querying CAPEC-connected CWEs...")
        capec_cwes = get_capec_connected_cwes(driver)
        print(f"✓ Found {len(capec_cwes)} unique CWEs connected to CAPECs")

        # 3. Check exact overlap
        print("\n[STEP 3] Checking exact ID overlap...")
        exact_overlap = set(cve_cwes) & set(capec_cwes)
        print(f"✗ Exact overlap: {len(exact_overlap)} CWEs")

        # 4. Analyze ID formats for CVE-connected CWEs
        print("\n[STEP 4] Analyzing CVE-connected CWE ID formats...")
        cve_formats = analyze_id_formats(cve_cwes)
        print("CVE-connected CWE ID formats:")
        for format_type, examples in cve_formats.items():
            print(f"  - {format_type}: {len(examples)} examples")
            print(f"    Examples: {examples[:5]}")

        # 5. Analyze ID formats for CAPEC-connected CWEs
        print("\n[STEP 5] Analyzing CAPEC-connected CWE ID formats...")
        capec_formats = analyze_id_formats(capec_cwes)
        print("CAPEC-connected CWE ID formats:")
        for format_type, examples in capec_formats.items():
            print(f"  - {format_type}: {len(examples)} examples")
            print(f"    Examples: {examples[:5]}")

        # 6. Check case-insensitive overlap
        print("\n[STEP 6] Checking case-insensitive overlap...")
        case_insensitive_overlap = check_case_insensitive_overlap(cve_cwes, capec_cwes)
        print(f"Case-insensitive overlap: {len(case_insensitive_overlap)} CWEs")
        if case_insensitive_overlap:
            print(f"Examples: {list(case_insensitive_overlap)[:10]}")

        # 7. Get sample relationships
        print("\n[STEP 7] Examining sample CVE→CWE relationships...")
        cve_samples = get_sample_cve_cwe_relationships(driver, 20)
        print("Sample CVE→CWE relationships:")
        for i, sample in enumerate(cve_samples[:5], 1):
            print(f"  {i}. {sample['cve_id']} → {sample['cwe_id']} ({sample['cwe_name']})")

        print("\n[STEP 8] Examining sample CWE→CAPEC relationships...")
        capec_samples = get_sample_cwe_capec_relationships(driver, 20)
        print("Sample CWE→CAPEC relationships:")
        for i, sample in enumerate(capec_samples[:5], 1):
            print(f"  {i}. {sample['cwe_id']} -{sample['relationship_type']}→ {sample['capec_id']}")

        # 8. Detailed comparison
        print("\n[STEP 9] Detailed ID comparison...")
        print("\nFirst 20 CVE-connected CWE IDs:")
        for i, cwe_id in enumerate(cve_cwes[:20], 1):
            print(f"  {i}. {repr(cwe_id)}")

        print("\nFirst 20 CAPEC-connected CWE IDs:")
        for i, cwe_id in enumerate(capec_cwes[:20], 1):
            print(f"  {i}. {repr(cwe_id)}")

        # 9. Generate diagnostic report
        print("\n[STEP 10] Generating diagnostic report...")

        report = {
            "summary": {
                "cve_connected_cwes": len(cve_cwes),
                "capec_connected_cwes": len(capec_cwes),
                "exact_overlap": len(exact_overlap),
                "case_insensitive_overlap": len(case_insensitive_overlap)
            },
            "cve_cwe_format_analysis": {
                format_type: {
                    "count": len(examples),
                    "examples": examples[:10]
                }
                for format_type, examples in cve_formats.items()
            },
            "capec_cwe_format_analysis": {
                format_type: {
                    "count": len(examples),
                    "examples": examples[:10]
                }
                for format_type, examples in capec_formats.items()
            },
            "sample_cve_cwe_relationships": cve_samples,
            "sample_cwe_capec_relationships": capec_samples,
            "cve_connected_cwe_ids_sample": cve_cwes[:50],
            "capec_connected_cwe_ids_sample": capec_cwes[:50]
        }

        # Save report
        output_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/analysis_results/cwe_overlap_diagnosis.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"✓ Diagnostic report saved to: {output_file}")

        # 10. Diagnosis conclusion
        print("\n" + "=" * 80)
        print("DIAGNOSIS CONCLUSION")
        print("=" * 80)

        if len(exact_overlap) == 0 and len(case_insensitive_overlap) > 0:
            print("\n⚠️  DIAGNOSIS: Case sensitivity mismatch detected!")
            print(f"   - {len(case_insensitive_overlap)} CWEs would overlap if case-insensitive")
            print("   - Recommendation: Normalize CWE IDs to uppercase 'CWE-###' format")
        elif len(exact_overlap) == 0 and len(case_insensitive_overlap) == 0:
            print("\n⚠️  DIAGNOSIS: Complete data separation detected!")
            print("   - CVE and CAPEC datasets reference entirely different CWE populations")
            print("   - Possible causes:")
            print("     1. Different CWE data sources used for CVE vs CAPEC")
            print("     2. ID transformation during import")
            print("     3. Different CWE versions (e.g., CWE 4.x vs CWE 3.x)")
        else:
            print("\n✓ Some overlap found - investigating specific mismatches...")

        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)

    finally:
        driver.close()

if __name__ == "__main__":
    main()
