#!/usr/bin/env python3
"""
Analyze which CWEs exist in database vs which are needed
"""

from neo4j import GraphDatabase
from collections import Counter

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

with driver.session() as session:
    # Get all CWE IDs from database
    result = session.run("MATCH (c:CWE) RETURN c.id AS id")
    existing_cwes = set(record['id'] for record in result)
    print(f"CWEs in database: {len(existing_cwes):,}")

    # Check if common weaknesses exist
    missing_common = []
    for cwe in ['cwe-79', 'cwe-78', 'cwe-200', 'cwe-22', 'cwe-20', 'cwe-89', 'cwe-119', 'cwe-120']:
        if cwe not in existing_cwes:
            missing_common.append(cwe)

    if missing_common:
        print(f"\n❌ Missing {len(missing_common)} of 8 most common CWEs:")
        for cwe in missing_common:
            print(f"   {cwe}")
    else:
        print("\n✅ All common CWEs exist in database")

    # Sample what DOES exist
    print("\nSample of CWEs that exist:")
    sample_cwes = sorted(list(existing_cwes))[:30]
    for cwe in sample_cwes:
        print(f"  {cwe}")

driver.close()
