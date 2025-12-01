#!/usr/bin/env python3
"""Verify NUCLEAR sector deployment"""
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j@openspg")

driver = GraphDatabase.driver(URI, auth=AUTH)

with driver.session() as session:
    # Count by node type
    result = session.run("""
    MATCH (n)
    WHERE n.sector = 'NUCLEAR'
    RETURN labels(n) as labels, count(*) as count
    ORDER BY count DESC
    """)

    print("NUCLEAR Sector Deployment Verification")
    print("=" * 60)
    print(f"{'Node Type':<40} {'Count':>10}")
    print("-" * 60)

    total = 0
    for record in result:
        labels_str = ':'.join(sorted(record['labels']))
        count = record['count']
        total += count
        print(f"{labels_str:<40} {count:>10,}")

    print("-" * 60)
    print(f"{'TOTAL':<40} {total:>10,}")

    # Verify registry
    result = session.run("""
    MATCH (r:DeploymentRegistry {id: 'SECTOR_REGISTRY'})
    RETURN r.NUCLEAR as deployed_time, r.NUCLEAR_status as status
    """)

    record = result.single()
    if record:
        print("\nRegistry Status:")
        print(f"  Status: {record['status']}")
        print(f"  Deployed: {record['deployed_time']}")

driver.close()
