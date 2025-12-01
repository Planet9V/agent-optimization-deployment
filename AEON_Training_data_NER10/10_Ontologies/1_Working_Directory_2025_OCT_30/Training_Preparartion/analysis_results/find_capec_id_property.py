#!/usr/bin/env python3
"""
Find the actual property name used for CAPEC IDs
"""

from neo4j import GraphDatabase
import json

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_capec_node_properties(driver):
    """Get all properties from a CAPEC node"""
    query = """
    MATCH (capec:CAPEC)
    RETURN capec
    LIMIT 5
    """

    with driver.session() as session:
        result = session.run(query)
        nodes = []
        for record in result:
            node_props = dict(record["capec"])
            nodes.append(node_props)
        return nodes

def search_for_id_properties(driver):
    """Search for properties containing 'id' or 'ID'"""
    query = """
    MATCH (capec:CAPEC)
    WHERE capec.capec_id IS NOT NULL
       OR capec.ID IS NOT NULL
       OR capec.attack_id IS NOT NULL
       OR capec.identifier IS NOT NULL
    RETURN capec.capec_id AS capec_id,
           capec.ID AS ID,
           capec.attack_id AS attack_id,
           capec.identifier AS identifier,
           capec.name AS name
    LIMIT 10
    """

    with driver.session() as session:
        result = session.run(query)
        return [dict(record) for record in result]

def count_capec_with_various_ids(driver):
    """Count CAPECs with different ID properties"""
    queries = {
        "total_capec": "MATCH (c:CAPEC) RETURN count(*) AS count",
        "has_id": "MATCH (c:CAPEC) WHERE c.id IS NOT NULL RETURN count(*) AS count",
        "has_capec_id": "MATCH (c:CAPEC) WHERE c.capec_id IS NOT NULL RETURN count(*) AS count",
        "has_ID": "MATCH (c:CAPEC) WHERE c.ID IS NOT NULL RETURN count(*) AS count",
        "has_attack_id": "MATCH (c:CAPEC) WHERE c.attack_id IS NOT NULL RETURN count(*) AS count",
        "has_name": "MATCH (c:CAPEC) WHERE c.name IS NOT NULL RETURN count(*) AS count"
    }

    counts = {}
    with driver.session() as session:
        for key, query in queries.items():
            result = session.run(query)
            counts[key] = result.single()["count"]

    return counts

def get_cwe_capec_with_all_properties(driver):
    """Get CWE→CAPEC relationships showing all possible ID properties"""
    query = """
    MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
    RETURN cwe.id AS cwe_id,
           cwe.cwe_id AS cwe_cwe_id,
           cwe.name AS cwe_name,
           capec.id AS capec_id,
           capec.capec_id AS capec_capec_id,
           capec.ID AS capec_ID,
           capec.attack_id AS capec_attack_id,
           capec.name AS capec_name
    LIMIT 20
    """

    with driver.session() as session:
        result = session.run(query)
        return [dict(record) for record in result]

def main():
    print("=" * 80)
    print("FINDING ACTUAL CAPEC ID PROPERTY NAME")
    print("=" * 80)

    driver = get_driver()

    try:
        # Get full CAPEC node properties
        print("\n[1] Sample CAPEC node properties...")
        capec_nodes = get_capec_node_properties(driver)
        for i, node in enumerate(capec_nodes, 1):
            print(f"\nCAPEC Node {i} properties:")
            for key, value in node.items():
                # Only show first 100 chars of long values
                value_str = str(value)[:100] if len(str(value)) > 100 else str(value)
                print(f"  - {key}: {value_str}")

        # Count CAPECs with various ID properties
        print("\n[2] Counting CAPECs with different ID properties...")
        counts = count_capec_with_various_ids(driver)
        print("CAPEC node counts:")
        for key, count in counts.items():
            print(f"  - {key}: {count}")

        # Search for ID properties
        print("\n[3] Searching for nodes with specific ID properties...")
        id_results = search_for_id_properties(driver)
        if id_results:
            print(f"Found {len(id_results)} CAPECs with ID properties:")
            for result in id_results[:5]:
                print(f"  - {result}")
        else:
            print("  No CAPECs found with standard ID properties")

        # Get CWE→CAPEC relationships with all properties
        print("\n[4] CWE→CAPEC relationships showing all ID properties...")
        relationships = get_cwe_capec_with_all_properties(driver)
        print(f"Sample of {len(relationships)} relationships:")
        for i, rel in enumerate(relationships[:10], 1):
            print(f"\n  Relationship {i}:")
            for key, value in rel.items():
                print(f"    {key}: {value}")

        # Save report
        report = {
            "sample_capec_nodes": capec_nodes,
            "id_property_counts": counts,
            "sample_with_id_properties": id_results,
            "cwe_capec_relationships": relationships
        }

        output_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/analysis_results/capec_id_property_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"\n✓ Report saved to: {output_file}")

        # Conclusion
        print("\n" + "=" * 80)
        print("DIAGNOSIS")
        print("=" * 80)

        if counts['has_capec_id'] > 0:
            print(f"\n✓ CAPEC nodes use 'capec_id' property ({counts['has_capec_id']} nodes)")
        elif counts['has_ID'] > 0:
            print(f"\n✓ CAPEC nodes use 'ID' property ({counts['has_ID']} nodes)")
        elif counts['has_attack_id'] > 0:
            print(f"\n✓ CAPEC nodes use 'attack_id' property ({counts['has_attack_id']} nodes)")
        else:
            print("\n⚠️  CAPEC nodes don't have standard ID property!")
            print("   - Checking node properties for alternative identifiers...")

        print("\n" + "=" * 80)

    finally:
        driver.close()

if __name__ == "__main__":
    main()
