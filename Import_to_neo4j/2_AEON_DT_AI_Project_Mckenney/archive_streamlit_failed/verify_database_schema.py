#!/usr/bin/env python3
"""
Database Schema Verification and Index Creation
Analyzes Neo4j database and creates optimization indexes for entity resolution
"""

from neo4j import GraphDatabase
import sys
from datetime import datetime

# Database connection parameters
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

class DatabaseAnalyzer:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def verify_connection(self):
        """Verify database connection"""
        print("=" * 80)
        print("DATABASE CONNECTION VERIFICATION")
        print("=" * 80)
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                record = result.single()
                if record and record["test"] == 1:
                    print("✅ Successfully connected to Neo4j")
                    return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
        return False

    def count_cves_by_year(self):
        """Count CVEs by year from 2000-2025"""
        print("\n" + "=" * 80)
        print("CVE DATASET ANALYSIS BY YEAR (2000-2025)")
        print("=" * 80)

        query = """
        MATCH (c:CVE)
        WHERE c.year >= 2000 AND c.year <= 2025
        RETURN c.year as year, count(c) as count
        ORDER BY c.year
        """

        try:
            with self.driver.session() as session:
                results = session.run(query)
                records = list(results)

                if not records:
                    print("⚠️  No CVE data found in the database")
                    return

                total = 0
                year_counts = {}

                print("\nYear | CVE Count")
                print("-" * 30)
                for record in records:
                    year = record["year"]
                    count = record["count"]
                    year_counts[year] = count
                    total += count
                    print(f"{year} | {count:,}")

                # Check for 2018-2019 gap
                print("\n" + "-" * 80)
                print("2018-2019 GAP ANALYSIS")
                print("-" * 80)
                if 2018 not in year_counts and 2019 not in year_counts:
                    print("⚠️  CONFIRMED: No CVEs found for 2018 or 2019")
                elif 2018 not in year_counts:
                    print("⚠️  CONFIRMED: No CVEs found for 2018")
                elif 2019 not in year_counts:
                    print("⚠️  CONFIRMED: No CVEs found for 2019")
                else:
                    print(f"✅ CVEs found for 2018: {year_counts[2018]:,}")
                    print(f"✅ CVEs found for 2019: {year_counts[2019]:,}")

                print(f"\nTotal CVEs (2000-2025): {total:,}")

        except Exception as e:
            print(f"❌ Error counting CVEs: {e}")

    def verify_relationships(self):
        """Verify CVE→CWE and CVE→CAPEC relationships"""
        print("\n" + "=" * 80)
        print("RELATIONSHIP VERIFICATION")
        print("=" * 80)

        queries = {
            "CVE→CWE": """
                MATCH (c:CVE)-[r]->(w:CWE)
                RETURN type(r) as rel_type, count(r) as count
            """,
            "CVE→CAPEC": """
                MATCH (c:CVE)-[r]->(a:CAPEC)
                RETURN type(r) as rel_type, count(r) as count
            """
        }

        try:
            with self.driver.session() as session:
                for name, query in queries.items():
                    print(f"\n{name} relationships:")
                    results = session.run(query)
                    records = list(results)

                    if not records or all(r["count"] == 0 for r in records):
                        print(f"  ⚠️  No {name} relationships found")
                    else:
                        for record in records:
                            rel_type = record["rel_type"]
                            count = record["count"]
                            print(f"  ✅ {rel_type}: {count:,} relationships")

        except Exception as e:
            print(f"❌ Error verifying relationships: {e}")

    def check_existing_indexes(self):
        """Check existing indexes in database"""
        print("\n" + "=" * 80)
        print("EXISTING INDEXES")
        print("=" * 80)

        query = """
        SHOW INDEXES
        YIELD name, labelsOrTypes, properties, type
        RETURN name, labelsOrTypes, properties, type
        """

        try:
            with self.driver.session() as session:
                results = session.run(query)
                records = list(results)

                if not records:
                    print("⚠️  No indexes found in database")
                    return

                print("\nCurrent Indexes:")
                print("-" * 80)
                for record in records:
                    name = record["name"]
                    labels = record["labelsOrTypes"]
                    properties = record["properties"]
                    idx_type = record["type"]
                    print(f"Name: {name}")
                    print(f"  Labels: {labels}")
                    print(f"  Properties: {properties}")
                    print(f"  Type: {idx_type}")
                    print()

        except Exception as e:
            print(f"❌ Error checking indexes: {e}")

    def create_entity_resolution_indexes(self):
        """Create indexes for entity resolution optimization"""
        print("\n" + "=" * 80)
        print("CREATING ENTITY RESOLUTION INDEXES")
        print("=" * 80)

        indexes = [
            {
                "name": "entity_resolution_status",
                "query": "CREATE INDEX entity_resolution_status IF NOT EXISTS FOR (e:Entity) ON (e.resolution_status)"
            },
            {
                "name": "entity_attempted_resolution",
                "query": "CREATE INDEX entity_attempted_resolution IF NOT EXISTS FOR (e:Entity) ON (e.attempted_resolution_date)"
            }
        ]

        try:
            with self.driver.session() as session:
                for index in indexes:
                    print(f"\nCreating index: {index['name']}")
                    try:
                        session.run(index["query"])
                        print(f"  ✅ Index '{index['name']}' created successfully")
                    except Exception as e:
                        if "already exists" in str(e).lower() or "equivalent" in str(e).lower():
                            print(f"  ℹ️  Index '{index['name']}' already exists")
                        else:
                            print(f"  ⚠️  Error creating index: {e}")

        except Exception as e:
            print(f"❌ Error in index creation process: {e}")

    def verify_entity_indexes(self):
        """Verify Entity.text, Entity.label, RELATIONSHIP.doc_id indexes"""
        print("\n" + "=" * 80)
        print("VERIFYING ENTITY-SPECIFIC INDEXES")
        print("=" * 80)

        expected_indexes = [
            ("Entity", "text"),
            ("Entity", "label"),
            ("RELATIONSHIP", "doc_id")
        ]

        query = """
        SHOW INDEXES
        YIELD name, labelsOrTypes, properties
        RETURN name, labelsOrTypes, properties
        """

        try:
            with self.driver.session() as session:
                results = session.run(query)
                records = list(results)

                existing = set()
                for record in records:
                    labels = record["labelsOrTypes"]
                    properties = record["properties"]
                    for label in labels:
                        for prop in properties:
                            existing.add((label, prop))

                print("\nExpected Index Verification:")
                print("-" * 80)
                for label, prop in expected_indexes:
                    if (label, prop) in existing:
                        print(f"✅ Index exists: {label}.{prop}")
                    else:
                        print(f"⚠️  Index missing: {label}.{prop}")

        except Exception as e:
            print(f"❌ Error verifying entity indexes: {e}")

    def get_database_statistics(self):
        """Get overall database statistics"""
        print("\n" + "=" * 80)
        print("DATABASE STATISTICS")
        print("=" * 80)

        queries = {
            "Total Nodes": "MATCH (n) RETURN count(n) as count",
            "Total Relationships": "MATCH ()-[r]->() RETURN count(r) as count",
            "Node Labels": "CALL db.labels() YIELD label RETURN collect(label) as labels",
            "Relationship Types": "CALL db.relationshipTypes() YIELD relationshipType RETURN collect(relationshipType) as types"
        }

        try:
            with self.driver.session() as session:
                for name, query in queries.items():
                    result = session.run(query)
                    record = result.single()

                    if name in ["Node Labels", "Relationship Types"]:
                        items = record[list(record.keys())[0]]
                        print(f"\n{name}:")
                        for item in items:
                            print(f"  - {item}")
                    else:
                        count = record["count"]
                        print(f"\n{name}: {count:,}")

        except Exception as e:
            print(f"❌ Error getting database statistics: {e}")

    def run_full_analysis(self):
        """Run complete database analysis"""
        print("\n")
        print("█" * 80)
        print("█" + " " * 78 + "█")
        print("█" + " " * 20 + "NEO4J DATABASE ANALYSIS REPORT" + " " * 28 + "█")
        print("█" + " " * 78 + "█")
        print("█" * 80)
        print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Database: {NEO4J_URI}")

        # Run all verification steps
        if not self.verify_connection():
            print("\n❌ Cannot proceed without database connection")
            return False

        self.get_database_statistics()
        self.count_cves_by_year()
        self.verify_relationships()
        self.check_existing_indexes()
        self.verify_entity_indexes()
        self.create_entity_resolution_indexes()

        # Final verification of new indexes
        print("\n" + "=" * 80)
        print("FINAL INDEX VERIFICATION")
        print("=" * 80)
        self.check_existing_indexes()

        print("\n" + "█" * 80)
        print("█" + " " * 25 + "ANALYSIS COMPLETE" + " " * 37 + "█")
        print("█" * 80)
        print("\n")

        return True


def main():
    """Main execution function"""
    analyzer = DatabaseAnalyzer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        success = analyzer.run_full_analysis()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Fatal error during analysis: {e}")
        sys.exit(1)
    finally:
        analyzer.close()


if __name__ == "__main__":
    main()
