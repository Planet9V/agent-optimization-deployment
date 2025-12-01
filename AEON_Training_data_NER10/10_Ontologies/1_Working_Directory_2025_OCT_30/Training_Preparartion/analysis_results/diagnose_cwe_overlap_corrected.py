#!/usr/bin/env python3
"""
CWE Overlap Diagnosis Script - CORRECTED VERSION
Uses actual relationship types: IS_WEAKNESS_TYPE and ENABLES_ATTACK_PATTERN
"""

from neo4j import GraphDatabase
import json
from collections import defaultdict

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

def get_driver():
    """Create Neo4j driver"""
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_cve_connected_cwes(driver):
    """Get all CWE IDs that have CVE relationships (via IS_WEAKNESS_TYPE)"""
    query = """
    MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
    RETURN DISTINCT cwe.id AS cwe_id
    ORDER BY cwe_id
    """

    with driver.session() as session:
        result = session.run(query)
        return [record["cwe_id"] for record in result if record["cwe_id"] is not None]

def get_capec_connected_cwes(driver):
    """Get all CWE IDs that have CAPEC relationships (via ENABLES_ATTACK_PATTERN)"""
    query = """
    MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
    RETURN DISTINCT cwe.id AS cwe_id
    ORDER BY cwe_id
    """

    with driver.session() as session:
        result = session.run(query)
        return [record["cwe_id"] for record in result if record["cwe_id"] is not None]

def get_sample_cve_cwe_relationships(driver, limit=20):
    """Get sample CVE->CWE relationships"""
    query = """
    MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
    WHERE cwe.id IS NOT NULL
    RETURN cve.id AS cve_id, cwe.id AS cwe_id, cwe.name AS cwe_name
    LIMIT $limit
    """

    with driver.session() as session:
        result = session.run(query, limit=limit)
        return [dict(record) for record in result]

def get_sample_cwe_capec_relationships(driver, limit=20):
    """Get sample CWE->CAPEC relationships"""
    query = """
    MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
    WHERE cwe.id IS NOT NULL AND capec.id IS NOT NULL
    RETURN cwe.id AS cwe_id, cwe.name AS cwe_name, capec.id AS capec_id
    LIMIT $limit
    """

    with driver.session() as session:
        result = session.run(query, limit=limit)
        return [dict(record) for record in result]

def get_null_id_counts(driver):
    """Count nodes with NULL IDs"""
    queries = {
        "cve_null_ids": "MATCH (cve:CVE) WHERE cve.id IS NULL RETURN count(*) AS count",
        "cwe_null_ids": "MATCH (cwe:CWE) WHERE cwe.id IS NULL RETURN count(*) AS count",
        "capec_null_ids": "MATCH (capec:CAPEC) WHERE capec.id IS NULL RETURN count(*) AS count"
    }

    counts = {}
    with driver.session() as session:
        for key, query in queries.items():
            result = session.run(query)
            counts[key] = result.single()["count"]

    return counts

def analyze_id_formats(cwe_ids):
    """Analyze the format patterns of CWE IDs"""
    formats = defaultdict(list)

    for cwe_id in cwe_ids[:100]:  # Sample first 100
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
    # Remove empty string if present
    overlap.discard('')
    return overlap

def check_numeric_overlap(cve_cwes, capec_cwes):
    """Extract numeric IDs and check overlap"""
    def extract_number(cwe_id):
        if cwe_id is None:
            return None
        # Extract numbers from formats like 'CWE-123', 'cwe-123', '123'
        import re
        match = re.search(r'\d+', str(cwe_id))
        return match.group() if match else None

    cve_numbers = {extract_number(cwe) for cwe in cve_cwes if extract_number(cwe)}
    capec_numbers = {extract_number(cwe) for cwe in capec_cwes if extract_number(cwe)}

    overlap = cve_numbers & capec_numbers
    return overlap

def main():
    """Execute the diagnosis"""
    print("=" * 80)
    print("CWE OVERLAP DIAGNOSIS - CORRECTED VERSION")
    print("Using actual relationship types: IS_WEAKNESS_TYPE & ENABLES_ATTACK_PATTERN")
    print("=" * 80)

    driver = get_driver()

    try:
        # Check for NULL IDs
        print("\n[STEP 0] Checking for NULL IDs in database...")
        null_counts = get_null_id_counts(driver)
        print(f"NULL ID counts:")
        for node_type, count in null_counts.items():
            print(f"  - {node_type}: {count}")

        # 1. Get CVE-connected CWEs
        print("\n[STEP 1] Querying CVE-connected CWEs (via IS_WEAKNESS_TYPE)...")
        cve_cwes = get_cve_connected_cwes(driver)
        print(f"✓ Found {len(cve_cwes)} unique CWEs connected to CVEs")

        # 2. Get CAPEC-connected CWEs
        print("\n[STEP 2] Querying CAPEC-connected CWEs (via ENABLES_ATTACK_PATTERN)...")
        capec_cwes = get_capec_connected_cwes(driver)
        print(f"✓ Found {len(capec_cwes)} unique CWEs connected to CAPECs")

        # 3. Check exact overlap
        print("\n[STEP 3] Checking exact ID overlap...")
        exact_overlap = set(cve_cwes) & set(capec_cwes)
        print(f"Exact overlap: {len(exact_overlap)} CWEs")
        if exact_overlap:
            print(f"Examples: {list(exact_overlap)[:10]}")

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

        # 7. Check numeric overlap
        print("\n[STEP 7] Checking numeric ID overlap (ignoring prefix)...")
        numeric_overlap = check_numeric_overlap(cve_cwes, capec_cwes)
        print(f"Numeric overlap: {len(numeric_overlap)} CWE numbers")
        if numeric_overlap:
            print(f"Examples: {list(numeric_overlap)[:10]}")

        # 8. Get sample relationships
        print("\n[STEP 8] Examining sample CVE→CWE relationships...")
        cve_samples = get_sample_cve_cwe_relationships(driver, 20)
        print("Sample CVE→CWE relationships:")
        for i, sample in enumerate(cve_samples[:10], 1):
            print(f"  {i}. {sample['cve_id']} → {sample['cwe_id']} ({sample.get('cwe_name', 'N/A')})")

        print("\n[STEP 9] Examining sample CWE→CAPEC relationships...")
        capec_samples = get_sample_cwe_capec_relationships(driver, 20)
        print("Sample CWE→CAPEC relationships:")
        for i, sample in enumerate(capec_samples[:10], 1):
            print(f"  {i}. {sample['cwe_id']} ({sample.get('cwe_name', 'N/A')}) → {sample['capec_id']}")

        # 9. Detailed comparison
        print("\n[STEP 10] Detailed ID comparison...")
        print("\nFirst 30 CVE-connected CWE IDs:")
        for i, cwe_id in enumerate(cve_cwes[:30], 1):
            print(f"  {i}. {repr(cwe_id)}")

        print("\nFirst 30 CAPEC-connected CWE IDs:")
        for i, cwe_id in enumerate(capec_cwes[:30], 1):
            print(f"  {i}. {repr(cwe_id)}")

        # 10. Generate diagnostic report
        print("\n[STEP 11] Generating diagnostic report...")

        report = {
            "summary": {
                "cve_connected_cwes": len(cve_cwes),
                "capec_connected_cwes": len(capec_cwes),
                "exact_overlap": len(exact_overlap),
                "case_insensitive_overlap": len(case_insensitive_overlap),
                "numeric_overlap": len(numeric_overlap)
            },
            "null_id_counts": null_counts,
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
            "overlap_details": {
                "exact_match": list(exact_overlap)[:50],
                "case_insensitive_match": list(case_insensitive_overlap)[:50],
                "numeric_match": list(numeric_overlap)[:50]
            },
            "sample_cve_cwe_relationships": cve_samples,
            "sample_cwe_capec_relationships": capec_samples,
            "cve_connected_cwe_ids_sample": cve_cwes[:100],
            "capec_connected_cwe_ids_sample": capec_cwes[:100]
        }

        # Save report
        output_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/analysis_results/cwe_overlap_diagnosis_corrected.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"✓ Diagnostic report saved to: {output_file}")

        # 11. Diagnosis conclusion
        print("\n" + "=" * 80)
        print("DIAGNOSIS CONCLUSION")
        print("=" * 80)

        if len(exact_overlap) > 0:
            print(f"\n✓ Found {len(exact_overlap)} CWEs with exact ID match!")
            print("  - Attack chains are possible through these CWEs")
        elif len(case_insensitive_overlap) > 0:
            print(f"\n⚠️  DIAGNOSIS: Case sensitivity mismatch detected!")
            print(f"   - {len(case_insensitive_overlap)} CWEs would overlap if case-insensitive")
            print("   - Recommendation: Normalize CWE IDs to uppercase 'CWE-###' format")
        elif len(numeric_overlap) > 0:
            print(f"\n⚠️  DIAGNOSIS: ID format mismatch detected!")
            print(f"   - {len(numeric_overlap)} CWEs share the same numeric ID")
            print("   - Different prefixes used: CVE data vs CAPEC data")
            print("   - Recommendation: Normalize to consistent format")
        else:
            print("\n⚠️  DIAGNOSIS: Complete data separation detected!")
            print("   - CVE and CAPEC datasets reference entirely different CWE populations")
            print("   - Possible causes:")
            print("     1. Different CWE data sources used for CVE vs CAPEC")
            print("     2. ID transformation during import")
            print("     3. Different CWE versions (e.g., CWE 4.x vs CWE 3.x)")

        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE - REAL DATA RETRIEVED")
        print("=" * 80)

    finally:
        driver.close()

if __name__ == "__main__":
    main()
