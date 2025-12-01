#!/usr/bin/env python3
"""
FIX NUCLEAR SECTOR DUPLICATES
Removes duplicate nodes while preserving one copy of each unique ID
"""

from neo4j import GraphDatabase
import time

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j@openspg")

def remove_duplicates(driver):
    """Remove duplicate NUCLEAR nodes, keeping one of each unique ID"""

    print("=" * 70)
    print("NUCLEAR SECTOR DUPLICATE REMOVAL")
    print("=" * 70)

    start_time = time.time()

    with driver.session() as session:
        # Find and count duplicates
        result = session.run("""
        MATCH (n)
        WHERE n.sector = 'NUCLEAR'
        WITH n.id as id, collect(n) as nodes
        WHERE size(nodes) > 1
        RETURN count(*) as duplicate_groups, sum(size(nodes) - 1) as nodes_to_delete
        """)

        record = result.single()
        dup_groups = record['duplicate_groups']
        nodes_to_delete = record['nodes_to_delete']

        print(f"\nFound:")
        print(f"  Duplicate ID groups: {dup_groups:,}")
        print(f"  Nodes to delete: {nodes_to_delete:,}")

        if nodes_to_delete == 0:
            print("\n✓ No duplicates found!")
            return

        # Remove duplicates (keep first node of each ID)
        print(f"\nRemoving duplicates...")
        result = session.run("""
        MATCH (n)
        WHERE n.sector = 'NUCLEAR'
        WITH n.id as id, collect(n) as nodes
        WHERE size(nodes) > 1
        WITH nodes[1..] as duplicates
        UNWIND duplicates as dup
        DETACH DELETE dup
        RETURN count(*) as deleted
        """)

        deleted = result.single()['deleted']
        print(f"  ✓ Deleted {deleted:,} duplicate nodes")

        # Verify final count
        result = session.run("""
        MATCH (n)
        WHERE n.sector = 'NUCLEAR'
        RETURN count(*) as total
        """)

        final_count = result.single()['total']

        # Get breakdown
        result = session.run("""
        MATCH (n)
        WHERE n.sector = 'NUCLEAR'
        WITH labels(n) as lbls, count(*) as cnt
        RETURN lbls, cnt
        ORDER BY cnt DESC
        """)

        print(f"\nFinal NUCLEAR sector state:")
        print("=" * 70)
        for record in result:
            labels = [l for l in record['lbls'] if l not in ['Nuclear', 'Monitoring', 'Asset']]
            count = record['cnt']
            print(f"  {', '.join(labels):40s}: {count:,}")

        print("=" * 70)
        print(f"Total NUCLEAR nodes: {final_count:,}")

        # Verify no duplicates remain
        result = session.run("""
        MATCH (n)
        WHERE n.sector = 'NUCLEAR'
        WITH n.id as id, count(*) as cnt
        WHERE cnt > 1
        RETURN count(*) as remaining_duplicates
        """)

        remaining = result.single()['remaining_duplicates']
        print(f"\nRemaining duplicates: {remaining}")

    end_time = time.time()
    execution_time = round(end_time - start_time, 2)

    print(f"\nExecution time: {execution_time} seconds")
    print("=" * 70)

def main():
    driver = GraphDatabase.driver(URI, auth=AUTH)

    try:
        remove_duplicates(driver)
    finally:
        driver.close()

if __name__ == "__main__":
    main()
