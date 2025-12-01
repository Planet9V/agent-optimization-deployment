#!/usr/bin/env python3
"""Check CVE node properties"""

from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def check_properties():
    query = """
    MATCH (c:CVE)
    RETURN c
    LIMIT 5
    """
    
    with driver.session() as session:
        result = session.run(query)
        print("Sample CVE nodes and their properties:")
        print("=" * 80)
        for i, record in enumerate(result, 1):
            cve = dict(record['c'])
            print(f"\nCVE #{i}:")
            for key, value in sorted(cve.items()):
                if isinstance(value, str) and len(str(value)) > 100:
                    print(f"  {key}: {str(value)[:100]}...")
                else:
                    print(f"  {key}: {value}")
        print("=" * 80)

if __name__ == "__main__":
    check_properties()
    driver.close()
