#!/usr/bin/env python3
"""
Verify CWE database contents and check for missing common CWEs
"""

from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Common CWEs that should exist
COMMON_CWES = [
    "CWE-79",   # XSS
    "CWE-89",   # SQL Injection
    "CWE-20",   # Improper Input Validation
    "CWE-200",  # Information Exposure
    "CWE-119",  # Buffer Overflow
    "CWE-120",  # Buffer Copy without Checking Size
    "CWE-125",  # Out-of-bounds Read
    "CWE-787",  # Out-of-bounds Write
    "CWE-416",  # Use After Free
    "CWE-476",  # NULL Pointer Dereference
]

with driver.session() as session:
    # Check total CWEs
    result = session.run("MATCH (c:CWE) RETURN count(c) AS total")
    total = result.single()['total']
    print(f"Total CWE nodes: {total:,}")
    print()

    # Check common CWEs
    print("Checking common CWEs:")
    print("=" * 60)
    for cwe_id in COMMON_CWES:
        result = session.run("MATCH (c:CWE {id: $cwe_id}) RETURN c.id AS id", cwe_id=cwe_id)
        record = result.single()
        status = "✅ EXISTS" if record else "❌ MISSING"
        print(f"{cwe_id:12} {status}")

    print()
    # Sample existing CWEs
    print("Sample of CWEs that DO exist:")
    print("=" * 60)
    result = session.run("MATCH (c:CWE) RETURN c.id AS id LIMIT 20")
    for record in result:
        print(f"  {record['id']}")

driver.close()
