#!/usr/bin/env python3
"""
Find actual relationship types in the Neo4j database
"""

from neo4j import GraphDatabase
import json

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_all_relationship_types(driver):
    """Get all relationship types in the database"""
    query = "CALL db.relationshipTypes()"

    with driver.session() as session:
        result = session.run(query)
        return [record["relationshipType"] for record in result]

def get_cve_cwe_relationships(driver):
    """Find actual CVE-CWE relationship patterns"""
    query = """
    MATCH (cve:CVE)-[r]->(cwe:CWE)
    RETURN DISTINCT type(r) AS rel_type, count(*) AS count
    ORDER BY count DESC
    """

    with driver.session() as session:
        result = session.run(query)
        return [dict(record) for record in result]

def get_cwe_capec_relationships(driver):
    """Find actual CWE-CAPEC relationship patterns"""
    query = """
    MATCH (cwe:CWE)-[r]->(capec:CAPEC)
    RETURN DISTINCT type(r) AS rel_type, count(*) AS count
    ORDER BY count DESC
    """

    with driver.session() as session:
        result = session.run(query)
        return [dict(record) for record in result]

def get_all_cve_relationships(driver):
    """Get all relationship types involving CVE nodes"""
    query = """
    MATCH (cve:CVE)-[r]-()
    RETURN DISTINCT type(r) AS rel_type, count(*) AS count
    ORDER BY count DESC
    """

    with driver.session() as session:
        result = session.run(query)
        return [dict(record) for record in result]

def get_all_capec_relationships(driver):
    """Get all relationship types involving CAPEC nodes"""
    query = """
    MATCH (capec:CAPEC)-[r]-()
    RETURN DISTINCT type(r) AS rel_type, count(*) AS count
    ORDER BY count DESC
    """

    with driver.session() as session:
        result = session.run(query)
        return [dict(record) for record in result]

def get_all_cwe_relationships(driver):
    """Get all relationship types involving CWE nodes"""
    query = """
    MATCH (cwe:CWE)-[r]-()
    RETURN DISTINCT type(r) AS rel_type, count(*) AS count
    ORDER BY count DESC
    """

    with driver.session() as session:
        result = session.run(query)
        return [dict(record) for record in result]

def get_sample_relationships(driver, rel_type, limit=5):
    """Get sample relationships of a specific type"""
    query = f"""
    MATCH (a)-[r:{rel_type}]->(b)
    RETURN labels(a)[0] AS source_label, a.id AS source_id,
           type(r) AS rel_type,
           labels(b)[0] AS target_label, b.id AS target_id
    LIMIT {limit}
    """

    with driver.session() as session:
        result = session.run(query)
        return [dict(record) for record in result]

def main():
    print("=" * 80)
    print("FINDING ACTUAL RELATIONSHIPS IN NEO4J DATABASE")
    print("=" * 80)

    driver = get_driver()

    try:
        # Get all relationship types
        print("\n[1] All relationship types in database:")
        all_rels = get_all_relationship_types(driver)
        for rel in all_rels:
            print(f"  - {rel}")

        # Get CVE-related relationships
        print("\n[2] Relationships involving CVE nodes:")
        cve_rels = get_all_cve_relationships(driver)
        for rel in cve_rels:
            print(f"  - {rel['rel_type']}: {rel['count']} relationships")

        # Get CWE-related relationships
        print("\n[3] Relationships involving CWE nodes:")
        cwe_rels = get_all_cwe_relationships(driver)
        for rel in cwe_rels:
            print(f"  - {rel['rel_type']}: {rel['count']} relationships")

        # Get CAPEC-related relationships
        print("\n[4] Relationships involving CAPEC nodes:")
        capec_rels = get_all_capec_relationships(driver)
        for rel in capec_rels:
            print(f"  - {rel['rel_type']}: {rel['count']} relationships")

        # Get CVE->CWE relationships
        print("\n[5] Direct CVE->CWE relationships:")
        cve_cwe = get_cve_cwe_relationships(driver)
        if cve_cwe:
            for rel in cve_cwe:
                print(f"  - {rel['rel_type']}: {rel['count']} relationships")
                # Get samples
                samples = get_sample_relationships(driver, rel['rel_type'], 3)
                for sample in samples:
                    print(f"    Example: ({sample['source_label']} {sample['source_id']})-[{sample['rel_type']}]->({sample['target_label']} {sample['target_id']})")
        else:
            print("  No direct CVE->CWE relationships found")

        # Get CWE->CAPEC relationships
        print("\n[6] Direct CWE->CAPEC relationships:")
        cwe_capec = get_cwe_capec_relationships(driver)
        if cwe_capec:
            for rel in cwe_capec:
                print(f"  - {rel['rel_type']}: {rel['count']} relationships")
                # Get samples
                samples = get_sample_relationships(driver, rel['rel_type'], 3)
                for sample in samples:
                    print(f"    Example: ({sample['source_label']} {sample['source_id']})-[{sample['rel_type']}]->({sample['target_label']} {sample['target_id']})")
        else:
            print("  No direct CWE->CAPEC relationships found")

        # Save report
        report = {
            "all_relationship_types": all_rels,
            "cve_relationships": cve_rels,
            "cwe_relationships": cwe_rels,
            "capec_relationships": capec_rels,
            "cve_to_cwe": cve_cwe,
            "cwe_to_capec": cwe_capec
        }

        output_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/analysis_results/actual_relationships.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✓ Report saved to: {output_file}")

        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)

    finally:
        driver.close()

if __name__ == "__main__":
    main()
