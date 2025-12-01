#!/usr/bin/env python3
"""
List actual CWE IDs in database
"""

from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

with driver.session() as session:
    # Get all CWE IDs
    result = session.run("MATCH (c:CWE) WHERE c.id IS NOT NULL RETURN c.id AS id ORDER BY c.id LIMIT 50")
    cwes = [record['id'] for record in result]

    print(f"First 50 CWEs in database:")
    print("=" * 60)
    for cwe in cwes:
        print(f"  {cwe}")

    # Get total count
    result = session.run("MATCH (c:CWE) WHERE c.id IS NOT NULL RETURN count(c) AS total")
    total = result.single()['total']
    print(f"\nTotal CWEs with ID: {total:,}")

    # Check for NULL IDs
    result = session.run("MATCH (c:CWE) WHERE c.id IS NULL RETURN count(c) AS null_count")
    null_count = result.single()['null_count']
    print(f"CWEs with NULL ID: {null_count:,}")

driver.close()
