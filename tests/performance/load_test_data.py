#!/usr/bin/env python3
"""
Load test data for cache performance benchmarks
Creates sample Assets and CriticalInfrastructure nodes with relationships
"""

from neo4j import GraphDatabase
import os

def load_test_data(uri: str, user: str, password: str):
    driver = GraphDatabase.driver(uri, auth=(user, password))

    with driver.session() as session:
        print("🔧 Loading test data for benchmarks...")

        # Create constraints and indexes
        print("  📊 Creating indexes...")
        session.run("""
        CREATE CONSTRAINT asset_id IF NOT EXISTS
        FOR (a:Asset) REQUIRE a.assetId IS UNIQUE
        """)

        session.run("""
        CREATE CONSTRAINT ci_asset_id IF NOT EXISTS
        FOR (c:CriticalInfrastructure) REQUIRE c.assetId IS UNIQUE
        """)

        session.run("""
        CREATE INDEX asset_sector IF NOT EXISTS
        FOR (c:CriticalInfrastructure) ON (c.sector)
        """)

        # Create sample data
        print("  🏗️ Creating Assets...")
        session.run("""
        UNWIND range(1, 100) AS i
        CREATE (:Asset {
            assetId: 'ASSET-' + toString(i),
            name: 'Asset ' + toString(i),
            type: CASE i % 3
                WHEN 0 THEN 'Server'
                WHEN 1 THEN 'Network Device'
                ELSE 'Storage'
            END,
            status: CASE i % 2 WHEN 0 THEN 'Active' ELSE 'Standby' END,
            created: datetime()
        })
        """)

        print("  🏭 Creating CriticalInfrastructure nodes...")
        session.run("""
        UNWIND ['Energy', 'Water', 'Transportation', 'Healthcare', 'Financial'] AS sector
        UNWIND range(1, 20) AS i
        CREATE (:CriticalInfrastructure {
            assetId: sector + '-ASSET-' + toString(i),
            name: sector + ' Asset ' + toString(i),
            sector: sector,
            criticality: CASE i % 3
                WHEN 0 THEN 'HIGH'
                WHEN 1 THEN 'MEDIUM'
                ELSE 'LOW'
            END,
            location: 'Location-' + toString(i),
            status: 'Operational',
            created: datetime()
        })
        """)

        print("  🔗 Creating relationships...")
        session.run("""
        MATCH (a:Asset), (b:Asset)
        WHERE id(a) < id(b) AND rand() < 0.1
        CREATE (a)-[:CONNECTS_TO {
            bandwidth: toString(toInteger(rand() * 1000)) + 'Mbps',
            latency: toString(toInteger(rand() * 100)) + 'ms',
            protocol: CASE toInteger(rand() * 3)
                WHEN 0 THEN 'TCP'
                WHEN 1 THEN 'UDP'
                ELSE 'HTTP'
            END
        }]->(b)
        """)

        session.run("""
        MATCH (c:CriticalInfrastructure), (a:Asset)
        WHERE rand() < 0.05
        CREATE (c)-[:DEPENDS_ON {
            dependency_type: CASE toInteger(rand() * 3)
                WHEN 0 THEN 'Power'
                WHEN 1 THEN 'Network'
                ELSE 'Data'
            END,
            criticality: 'HIGH'
        }]->(a)
        """)

        # Verify data
        result = session.run("""
        MATCH (n)
        RETURN labels(n)[0] AS type, count(n) AS count
        ORDER BY type
        """)

        print("\n  ✅ Test data loaded:")
        for record in result:
            print(f"    - {record['type']}: {record['count']} nodes")

        result = session.run("""
        MATCH ()-[r]->()
        RETURN type(r) AS type, count(r) AS count
        ORDER BY type
        """)

        print("\n  🔗 Relationships created:")
        for record in result:
            print(f"    - {record['type']}: {record['count']} relationships")

    driver.close()
    print("\n✅ Test data loading complete!")

def main():
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "your_password")

    load_test_data(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

if __name__ == "__main__":
    main()
