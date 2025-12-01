#!/usr/bin/env python3
"""
Investigate why CWE→CAPEC relationships show NULL IDs
"""

from neo4j import GraphDatabase
import json

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def investigate_cwe_capec_nulls(driver):
    """Check CWE→CAPEC relationships with NULL filtering"""
    queries = {
        "total_relationships": """
            MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
            RETURN count(*) AS count
        """,
        "null_cwe_ids": """
            MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
            WHERE cwe.id IS NULL
            RETURN count(*) AS count
        """,
        "null_capec_ids": """
            MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
            WHERE capec.id IS NULL
            RETURN count(*) AS count
        """,
        "both_null": """
            MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
            WHERE cwe.id IS NULL AND capec.id IS NULL
            RETURN count(*) AS count
        """,
        "both_not_null": """
            MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
            WHERE cwe.id IS NOT NULL AND capec.id IS NOT NULL
            RETURN count(*) AS count
        """
    }

    results = {}
    with driver.session() as session:
        for key, query in queries.items():
            result = session.run(query)
            results[key] = result.single()["count"]

    return results

def get_sample_with_nulls(driver, limit=20):
    """Get samples showing all fields regardless of NULL"""
    query = """
    MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
    RETURN cwe.id AS cwe_id, cwe.name AS cwe_name,
           capec.id AS capec_id, capec.name AS capec_name,
           id(cwe) AS cwe_internal_id, id(capec) AS capec_internal_id
    LIMIT $limit
    """

    with driver.session() as session:
        result = session.run(query, limit=limit)
        return [dict(record) for record in result]

def get_cwe_properties(driver):
    """Get a sample CWE node to see what properties it has"""
    query = """
    MATCH (cwe:CWE)
    WHERE cwe.id IS NOT NULL
    RETURN cwe
    LIMIT 1
    """

    with driver.session() as session:
        result = session.run(query)
        record = result.single()
        if record:
            return dict(record["cwe"])
        return None

def get_capec_properties(driver):
    """Get a sample CAPEC node to see what properties it has"""
    query = """
    MATCH (capec:CAPEC)
    WHERE capec.id IS NOT NULL
    RETURN capec
    LIMIT 1
    """

    with driver.session() as session:
        result = session.run(query)
        record = result.single()
        if record:
            return dict(record["capec"])
        return None

def main():
    print("=" * 80)
    print("INVESTIGATING NULL IDs IN CWE→CAPEC RELATIONSHIPS")
    print("=" * 80)

    driver = get_driver()

    try:
        # Check NULL distribution
        print("\n[1] Analyzing NULL ID distribution...")
        null_stats = investigate_cwe_capec_nulls(driver)
        print("Relationship statistics:")
        for key, count in null_stats.items():
            print(f"  - {key}: {count}")

        # Get sample with all fields
        print("\n[2] Sample relationships (showing all fields)...")
        samples = get_sample_with_nulls(driver, 20)
        print(f"Retrieved {len(samples)} samples:")
        for i, sample in enumerate(samples[:10], 1):
            print(f"\n  Sample {i}:")
            print(f"    CWE ID: {sample['cwe_id']}")
            print(f"    CWE Name: {sample['cwe_name']}")
            print(f"    CWE Internal ID: {sample['cwe_internal_id']}")
            print(f"    CAPEC ID: {sample['capec_id']}")
            print(f"    CAPEC Name: {sample['capec_name']}")
            print(f"    CAPEC Internal ID: {sample['capec_internal_id']}")

        # Check node properties
        print("\n[3] Sample CWE node properties...")
        cwe_props = get_cwe_properties(driver)
        if cwe_props:
            print("CWE node properties:")
            for key, value in list(cwe_props.items())[:10]:
                print(f"  - {key}: {value}")
        else:
            print("  No CWE nodes with id found!")

        print("\n[4] Sample CAPEC node properties...")
        capec_props = get_capec_properties(driver)
        if capec_props:
            print("CAPEC node properties:")
            for key, value in list(capec_props.items())[:10]:
                print(f"  - {key}: {value}")
        else:
            print("  No CAPEC nodes with id found!")

        # Save report
        report = {
            "null_statistics": null_stats,
            "sample_relationships": samples,
            "sample_cwe_properties": cwe_props,
            "sample_capec_properties": capec_props
        }

        output_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/analysis_results/null_id_investigation.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"\n✓ Report saved to: {output_file}")

        # Conclusion
        print("\n" + "=" * 80)
        print("KEY FINDINGS")
        print("=" * 80)

        if null_stats['both_null'] == null_stats['total_relationships']:
            print("\n⚠️  ALL CWE→CAPEC relationships have NULL IDs!")
            print("   - This explains why we got 0 samples in the previous query")
            print("   - CWE nodes in these relationships don't have 'id' property set")
            print("   - CAPEC nodes in these relationships don't have 'id' property set")
        elif null_stats['both_not_null'] > 0:
            print(f"\n✓ Found {null_stats['both_not_null']} relationships with valid IDs")
            print("   - These can be used for attack chain analysis")

        print("\n" + "=" * 80)

    finally:
        driver.close()

if __name__ == "__main__":
    main()
