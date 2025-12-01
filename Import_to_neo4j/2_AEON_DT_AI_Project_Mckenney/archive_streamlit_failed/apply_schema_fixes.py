#!/usr/bin/env python3
"""Apply schema fixes to Neo4j database"""
from neo4j import GraphDatabase
import sys

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))

print("Applying schema fixes to Neo4j database...")
print("=" * 80)

with driver.session() as session:
    # NOTE: Neo4j Community Edition limitations:
    # - NODE KEY constraints require Enterprise Edition
    # - Composite unique constraints not supported in Community Edition
    # - Solution: Use Entity MERGE with (text, label) and add composite index

    fixes = [
        ("RELATIONSHIP.doc_id Index",
         "CREATE INDEX relationship_doc_id IF NOT EXISTS FOR ()-[r:RELATIONSHIP]-() ON (r.doc_id)"),

        ("Entity Composite Index",
         "CREATE INDEX entity_composite IF NOT EXISTS FOR (e:Entity) ON (e.text, e.label)"),
    ]

    for name, query in fixes:
        try:
            print(f"\n✓ Applying: {name}")
            session.run(query)
            print(f"  SUCCESS: {name} created")
        except Exception as e:
            if "already exists" in str(e).lower() or "equivalent" in str(e).lower():
                print(f"  SKIPPED: {name} already exists")
            else:
                print(f"  ERROR: {name} failed - {e}")
                sys.exit(1)

print("\n" + "=" * 80)
print("Schema fixes applied successfully!")
print("\nVerifying constraints and indexes...")

# Verify constraints
result = session.run("SHOW CONSTRAINTS")
print("\n📋 CONSTRAINTS:")
for record in result:
    print(f"  - {record.get('name', 'unnamed')}: {record.get('labelsOrTypes', [])} on {record.get('properties', [])}")

# Verify indexes
result = session.run("SHOW INDEXES")
print("\n📊 INDEXES:")
for record in result:
    idx_type = record.get('type', 'unknown')
    idx_name = record.get('name', 'unnamed')
    properties = record.get('properties', [])
    print(f"  - {idx_name} ({idx_type}): {properties}")

driver.close()
print("\n✅ Schema verification complete!")
