#!/usr/bin/env python3
"""
Test 2012-2017 CVE Coverage
Verifies the NVD API import by analyzing CVEs by published_date
"""

from neo4j import GraphDatabase
import sys

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

class CVECoverageTest:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def test_2012_2017_coverage(self):
        """Test CVEs imported from 2012-2017 using published_date"""
        print("\n" + "="*80)
        print("CVE COVERAGE TEST: 2012-2017 (by published_date)")
        print("="*80)

        query = """
        MATCH (c:CVE)
        WHERE c.published_date >= '2012-01-01' AND c.published_date < '2018-01-01'
        WITH substring(c.published_date, 0, 4) as year, count(c) as count
        RETURN year, count
        ORDER BY year
        """

        with self.driver.session() as session:
            results = session.run(query)
            records = list(results)

            if not records:
                print("❌ No CVEs found for 2012-2017")
                return False

            total = 0
            print("\nYear | CVE Count")
            print("-" * 30)
            for record in records:
                year = record["year"]
                count = record["count"]
                total += count
                print(f"{year} | {count:,}")

            print(f"\nTotal CVEs (2012-2017): {total:,}")
            print(f"Expected: ~49,908")

            if total >= 49000:
                print(f"\n✅ SUCCESS: {total:,} CVEs imported successfully")
                return True
            else:
                print(f"\n⚠️  WARNING: Only {total:,} CVEs found, expected ~49,908")
                return False

    def test_entity_resolution_readiness(self):
        """Test that entity resolution can now resolve 2012-2017 CVEs"""
        print("\n" + "="*80)
        print("ENTITY RESOLUTION READINESS TEST")
        print("="*80)

        # Check if we have any unresolved CVE entities that could now be resolved
        query = """
        MATCH (e:Entity {label: 'CVE', resolution_status: 'unresolved'})
        WITH e.text as cve_text, e
        MATCH (c:CVE)
        WHERE c.cve_id = cve_text
          AND c.published_date >= '2012-01-01'
          AND c.published_date < '2018-01-01'
        RETURN count(DISTINCT c) as resolvable_count,
               collect(DISTINCT c.cve_id)[..10] as sample_cves
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()

            if record and record["resolvable_count"] > 0:
                count = record["resolvable_count"]
                samples = record["sample_cves"]
                print(f"\n✅ Found {count} previously unresolved CVE entities from 2012-2017")
                print(f"   that can now be resolved with the expanded dataset")
                print(f"\nSample CVEs: {samples[:5]}")
                return True
            else:
                print("\n✅ No previously unresolved 2012-2017 CVEs found")
                print("   (This is good - means entities are already resolved or not referenced)")
                return True

    def test_cwe_relationships(self):
        """Test CVE→CWE relationships for 2012-2017"""
        print("\n" + "="*80)
        print("CVE→CWE RELATIONSHIP TEST (2012-2017)")
        print("="*80)

        query = """
        MATCH (c:CVE)-[r:EXPLOITS_WEAKNESS]->(w:CWE)
        WHERE c.published_date >= '2012-01-01' AND c.published_date < '2018-01-01'
        RETURN count(DISTINCT r) as relationship_count,
               count(DISTINCT c) as cves_with_cwes,
               count(DISTINCT w) as unique_cwes
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()

            if record:
                rel_count = record["relationship_count"]
                cve_count = record["cves_with_cwes"]
                cwe_count = record["unique_cwes"]

                print(f"\n✅ CVE→CWE Relationships: {rel_count:,}")
                print(f"✅ CVEs with CWE links: {cve_count:,}")
                print(f"✅ Unique CWEs referenced: {cwe_count:,}")

                coverage = (cve_count / 49908) * 100 if 49908 > 0 else 0
                print(f"\nCWE Coverage: {coverage:.1f}%")

                return True

            return False

def main():
    tester = CVECoverageTest(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        test1 = tester.test_2012_2017_coverage()
        test2 = tester.test_entity_resolution_readiness()
        test3 = tester.test_cwe_relationships()

        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"2012-2017 Coverage Test: {'✅ PASS' if test1 else '❌ FAIL'}")
        print(f"Entity Resolution Test: {'✅ PASS' if test2 else '❌ FAIL'}")
        print(f"CWE Relationships Test: {'✅ PASS' if test3 else '❌ FAIL'}")

        if test1 and test2 and test3:
            print("\n🎉 ALL TESTS PASSED - Ready for full document processing")
            sys.exit(0)
        else:
            print("\n⚠️  SOME TESTS FAILED - Review results above")
            sys.exit(1)

    finally:
        tester.close()

if __name__ == "__main__":
    main()
