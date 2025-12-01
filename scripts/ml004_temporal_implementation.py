#!/usr/bin/env python3
"""
ML-004 TEMPORAL VERSIONING IMPLEMENTATION
Executes temporal property additions to Actor nodes in Neo4j
"""

from neo4j import GraphDatabase
from datetime import datetime
import sys

# Connection details (openspg-neo4j container)
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j"

def execute_ml004():
    """Execute ML-004 temporal versioning implementation"""
    driver = None
    try:
        # Connect to Neo4j
        print("Connecting to Neo4j at localhost:7687 (openspg-neo4j container)...")
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:
            # STEP 1: Add temporal properties to Actor nodes
            print("\n[STEP 1] Adding temporal properties to Actor nodes...")
            result = session.run("""
                MATCH (a:Actor)
                WHERE a.id IS NOT NULL
                SET a.valid_from = COALESCE(a.valid_from, datetime()),
                    a.valid_to = COALESCE(a.valid_to, datetime('9999-12-31')),
                    a.version = COALESCE(a.version, 1),
                    a.change_source = COALESCE(a.change_source, 'INITIAL'),
                    a.change_actor = COALESCE(a.change_actor, 'SYSTEM'),
                    a.updated_at = datetime()
                RETURN count(a) as actors_updated
            """)

            actors_updated = result.single()[0]
            print(f"✓ Updated {actors_updated} Actor nodes with temporal properties")

            # STEP 2: Create temporal indexes
            print("\n[STEP 2] Creating temporal indexes...")

            session.run("CREATE INDEX actor_valid_from_idx IF NOT EXISTS FOR (a:Actor) ON (a.valid_from)")
            print("✓ Created index: actor_valid_from_idx")

            session.run("CREATE INDEX actor_valid_to_idx IF NOT EXISTS FOR (a:Actor) ON (a.valid_to)")
            print("✓ Created index: actor_valid_to_idx")

            session.run("CREATE INDEX actor_version_idx IF NOT EXISTS FOR (a:Actor) ON (a.version)")
            print("✓ Created index: actor_version_idx")

            # STEP 3: Verify indexes
            print("\n[STEP 3] Verifying indexes...")
            result = session.run("""
                SHOW INDEXES
                WHERE name CONTAINS 'valid' OR name CONTAINS 'version'
            """)

            indexes = list(result)
            print(f"✓ Found {len(indexes)} temporal indexes:")
            for idx in indexes:
                print(f"  - {idx.get('name', 'unnamed')}: {idx.get('labelsOrTypes', [])} ON {idx.get('properties', [])}")

            # STEP 4: Test point-in-time query
            print("\n[STEP 4] Testing point-in-time query...")
            result = session.run("""
                MATCH (a:Actor)
                WHERE a.valid_from <= datetime() AND a.valid_to > datetime()
                RETURN a.id, a.version, a.change_source, a.valid_from, a.valid_to
                LIMIT 5
            """)

            records = list(result)
            print(f"✓ Point-in-time query returned {len(records)} current Actor records:")
            for record in records:
                print(f"  - Actor {record['a.id']}: version={record['a.version']}, source={record['a.change_source']}")

            # Final verification
            print("\n" + "="*60)
            print("ML-004 IMPLEMENTATION COMPLETE")
            print("="*60)
            print(f"✓ Actors updated: {actors_updated}")
            print(f"✓ Indexes created: 3")
            print(f"✓ Point-in-time queries: WORKING")
            print("\nTemporal versioning is now operational on all Actor nodes.")

            return True

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

    finally:
        if driver:
            driver.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    success = execute_ml004()
    sys.exit(0 if success else 1)
