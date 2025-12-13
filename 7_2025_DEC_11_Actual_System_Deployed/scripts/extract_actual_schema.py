#!/usr/bin/env python3
"""
Extract ACTUAL Neo4j Schema - Query real database for implemented schema
This queries the LIVE database to document what's actually deployed.
"""

import json
from neo4j import GraphDatabase
from collections import defaultdict
from datetime import datetime

# Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

def extract_schema():
    """Extract complete schema from live Neo4j database"""

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    schema = {
        "extraction_date": datetime.now().isoformat(),
        "database_uri": NEO4J_URI,
        "total_nodes": 0,
        "total_relationships": 0,
        "labels": {},
        "relationship_types": {},
        "property_keys": set(),
        "super_labels": {},
        "hierarchical_mappings": {},
        "sample_nodes": {}
    }

    with driver.session() as session:
        # Get total counts
        result = session.run("MATCH (n) RETURN COUNT(n) as total")
        schema["total_nodes"] = result.single()["total"]

        result = session.run("MATCH ()-[r]->() RETURN COUNT(r) as total")
        schema["total_relationships"] = result.single()["total"]

        print(f"Total nodes: {schema['total_nodes']:,}")
        print(f"Total relationships: {schema['total_relationships']:,}")

        # Get all labels with counts
        print("\nExtracting labels...")
        result = session.run("""
            CALL db.labels() YIELD label
            CALL apoc.cypher.run(
                'MATCH (n:`' + label + '`) RETURN count(n) as count',
                {}
            ) YIELD value
            RETURN label, value.count as count
            ORDER BY count DESC
        """)

        for record in result:
            label = record["label"]
            count = record["count"]
            schema["labels"][label] = count
            print(f"  {label}: {count:,}")

        # Get all relationship types with counts
        print("\nExtracting relationship types...")
        result = session.run("""
            CALL db.relationshipTypes() YIELD relationshipType
            CALL apoc.cypher.run(
                'MATCH ()-[r:`' + relationshipType + '`]->() RETURN count(r) as count',
                {}
            ) YIELD value
            RETURN relationshipType, value.count as count
            ORDER BY count DESC
        """)

        for record in result:
            rel_type = record["relationshipType"]
            count = record["count"]
            schema["relationship_types"][rel_type] = count
            print(f"  {rel_type}: {count:,}")

        # Get all property keys
        print("\nExtracting property keys...")
        result = session.run("CALL db.propertyKeys() YIELD propertyKey RETURN propertyKey")
        schema["property_keys"] = [record["propertyKey"] for record in result]
        print(f"  Total property keys: {len(schema['property_keys'])}")

        # Check for super_label property
        print("\nChecking for super_label property...")
        result = session.run("""
            MATCH (n)
            WHERE n.super_label IS NOT NULL
            RETURN DISTINCT n.super_label as super_label, count(n) as count
            ORDER BY count DESC
        """)

        super_label_counts = {}
        for record in result:
            super_label = record["super_label"]
            count = record["count"]
            super_label_counts[super_label] = count
            print(f"  {super_label}: {count:,}")

        schema["super_labels"] = super_label_counts

        # Check for hierarchical properties
        print("\nChecking hierarchical properties...")
        result = session.run("""
            MATCH (n)
            WHERE n.ner_label IS NOT NULL OR n.fine_grained_type IS NOT NULL
            RETURN
                n.super_label as super_label,
                n.ner_label as ner_label,
                n.fine_grained_type as fine_grained_type,
                count(n) as count
            ORDER BY count DESC
            LIMIT 50
        """)

        hierarchical_mappings = []
        for record in result:
            hierarchical_mappings.append({
                "super_label": record["super_label"],
                "ner_label": record["ner_label"],
                "fine_grained_type": record["fine_grained_type"],
                "count": record["count"]
            })

        schema["hierarchical_mappings"] = hierarchical_mappings
        print(f"  Found {len(hierarchical_mappings)} hierarchical mappings")

        # Get sample nodes for top 20 labels
        print("\nGetting sample nodes...")
        for label in list(schema["labels"].keys())[:20]:
            try:
                result = session.run(f"""
                    MATCH (n:`{label}`)
                    RETURN n LIMIT 3
                """)

                samples = []
                for record in result:
                    node = record["n"]
                    # Convert node to dict and handle non-serializable types
                    node_dict = {}
                    for key, value in dict(node).items():
                        if hasattr(value, 'isoformat'):
                            node_dict[key] = value.isoformat()
                        elif hasattr(value, '__str__'):
                            node_dict[key] = str(value)
                        else:
                            node_dict[key] = value
                    samples.append(node_dict)

                schema["sample_nodes"][label] = samples
            except Exception as e:
                print(f"  Error getting samples for {label}: {e}")

    driver.close()

    # Convert set to list for JSON serialization
    schema["property_keys"] = list(schema["property_keys"])

    return schema

if __name__ == "__main__":
    print("="*80)
    print("EXTRACTING ACTUAL NEO4J SCHEMA FROM LIVE DATABASE")
    print("="*80)

    schema = extract_schema()

    # Save to JSON
    output_file = "/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/temp_notes/actual_neo4j_schema.json"
    with open(output_file, 'w') as f:
        json.dump(schema, f, indent=2)

    print(f"\n✅ Schema extracted and saved to: {output_file}")
    print(f"\nSummary:")
    print(f"  Total nodes: {schema['total_nodes']:,}")
    print(f"  Total relationships: {schema['total_relationships']:,}")
    print(f"  Unique labels: {len(schema['labels'])}")
    print(f"  Unique relationship types: {len(schema['relationship_types'])}")
    print(f"  Property keys: {len(schema['property_keys'])}")
    print(f"  Super labels: {len(schema['super_labels'])}")
