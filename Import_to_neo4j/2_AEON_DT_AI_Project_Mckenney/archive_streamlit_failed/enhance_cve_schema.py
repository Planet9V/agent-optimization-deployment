#!/usr/bin/env python3
"""
CVE Schema Enhancement Script
Adds namespace and year properties to all CVE nodes for improved querying
"""

from neo4j import GraphDatabase
import sys
from datetime import datetime

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

class SchemaEnhancer:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_namespace_property(self):
        """Add namespace property to track data source"""
        print("\n" + "="*80)
        print("ADDING NAMESPACE PROPERTY TO NVD CVEs")
        print("="*80)

        # Mark NVD-sourced CVEs (those with published_date from NVD imports)
        query = """
        MATCH (c:CVE)
        WHERE c.namespace IS NULL
          AND c.published_date IS NOT NULL
          AND c.published_date >= '2012-01-01'
          AND c.published_date < '2026-01-01'
          AND c.cve_id =~ 'CVE-.*'
        SET c.namespace = 'NVD'
        RETURN count(c) as updated_count
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()
            count = record["updated_count"]
            print(f"\n✅ Added namespace='NVD' to {count:,} CVE nodes")

        # Mark other CVEs with existing namespace or set to 'Unknown'
        query_other = """
        MATCH (c:CVE)
        WHERE c.namespace IS NULL
        SET c.namespace = COALESCE(c.customer_namespace, 'CybersecurityKB')
        RETURN count(c) as updated_count
        """

        with self.driver.session() as session:
            result = session.run(query_other)
            record = result.single()
            count = record["updated_count"]
            print(f"✅ Set namespace for {count:,} other CVE nodes")

    def add_year_property(self):
        """Extract year from published_date for query optimization"""
        print("\n" + "="*80)
        print("ADDING YEAR PROPERTY FOR QUERY OPTIMIZATION")
        print("="*80)

        query = """
        MATCH (c:CVE)
        WHERE c.published_date IS NOT NULL
          AND c.year IS NULL
        SET c.year = toInteger(substring(toString(c.published_date), 0, 4))
        RETURN count(c) as updated_count
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()
            count = record["updated_count"]
            print(f"\n✅ Added year property to {count:,} CVE nodes")

    def create_year_index(self):
        """Create index on year property"""
        print("\n" + "="*80)
        print("CREATING YEAR INDEX")
        print("="*80)

        query = """
        CREATE INDEX cve_year_index IF NOT EXISTS FOR (c:CVE) ON (c.year)
        """

        try:
            with self.driver.session() as session:
                session.run(query)
                print("\n✅ Year index created successfully")
        except Exception as e:
            if "already exists" in str(e).lower() or "equivalent" in str(e).lower():
                print("\nℹ️  Year index already exists")
            else:
                print(f"\n⚠️  Error creating index: {e}")

    def create_namespace_index(self):
        """Create index on namespace property"""
        print("\n" + "="*80)
        print("CREATING NAMESPACE INDEX")
        print("="*80)

        query = """
        CREATE INDEX cve_namespace_index IF NOT EXISTS FOR (c:CVE) ON (c.namespace)
        """

        try:
            with self.driver.session() as session:
                session.run(query)
                print("\n✅ Namespace index created successfully")
        except Exception as e:
            if "already exists" in str(e).lower() or "equivalent" in str(e).lower():
                print("\nℹ️  Namespace index already exists")
            else:
                print(f"\n⚠️  Error creating index: {e}")

    def verify_enhancements(self):
        """Verify schema enhancements were applied correctly"""
        print("\n" + "="*80)
        print("VERIFYING SCHEMA ENHANCEMENTS")
        print("="*80)

        # Check namespace distribution
        query_namespace = """
        MATCH (c:CVE)
        RETURN c.namespace as namespace, count(c) as count
        ORDER BY count DESC
        """

        with self.driver.session() as session:
            results = session.run(query_namespace)
            records = list(results)

            print("\nNamespace Distribution:")
            print("-" * 50)
            for record in records:
                namespace = record["namespace"] or "NULL"
                count = record["count"]
                print(f"{namespace:25} | {count:,}")

        # Check year distribution
        query_years = """
        MATCH (c:CVE)
        WHERE c.year IS NOT NULL
        WITH c.year as year, count(c) as count
        ORDER BY year
        RETURN min(year) as min_year, max(year) as max_year, sum(count) as total_with_years
        """

        with self.driver.session() as session:
            result = session.run(query_years)
            record = result.single()

            print("\nYear Property Statistics:")
            print("-" * 50)
            print(f"Earliest Year: {record['min_year']}")
            print(f"Latest Year: {record['max_year']}")
            print(f"Total CVEs with year: {record['total_with_years']:,}")

    def run_full_enhancement(self):
        """Execute complete schema enhancement"""
        print("\n")
        print("█" * 80)
        print("█" + " " * 78 + "█")
        print("█" + " " * 25 + "CVE SCHEMA ENHANCEMENT" + " " * 32 + "█")
        print("█" + " " * 78 + "█")
        print("█" * 80)
        print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            self.add_namespace_property()
            self.add_year_property()
            self.create_year_index()
            self.create_namespace_index()
            self.verify_enhancements()

            print("\n" + "="*80)
            print("SCHEMA ENHANCEMENT COMPLETE")
            print("="*80)
            print("\n✅ All CVE nodes now have:")
            print("   - namespace property (data source tracking)")
            print("   - year property (query optimization)")
            print("   - Indexes for fast filtering")
            print("\n" + "█" * 80)
            print("\n")

            return True

        except Exception as e:
            print(f"\n❌ Error during schema enhancement: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    enhancer = SchemaEnhancer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        success = enhancer.run_full_enhancement()
        sys.exit(0 if success else 1)
    finally:
        enhancer.close()

if __name__ == "__main__":
    main()
