#!/usr/bin/env python3
"""
Comprehensive CVE Statistics Report
Analyzes all CVE data in the Neo4j graph database
"""

from neo4j import GraphDatabase
import sys
from datetime import datetime

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

class CVEStatistics:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_header(self, title):
        print("\n" + "="*80)
        print(title.center(80))
        print("="*80)

    def total_cve_count(self):
        """Count total CVEs in database"""
        self.print_header("TOTAL CVE COUNT")

        with self.driver.session() as session:
            result = session.run("MATCH (c:CVE) RETURN count(c) as total")
            record = result.single()
            total = record["total"]
            print(f"\n✅ Total CVEs in Database: {total:,}")
            return total

    def cves_by_year(self):
        """Count CVEs by publication year"""
        self.print_header("CVE COUNT BY YEAR (Published Date)")

        query = """
        MATCH (c:CVE)
        WHERE c.published_date IS NOT NULL
        WITH substring(toString(c.published_date), 0, 4) as year, count(c) as count
        RETURN year, count
        ORDER BY year
        """

        with self.driver.session() as session:
            results = session.run(query)
            records = list(results)

            print("\nYear | CVE Count")
            print("-" * 40)

            total = 0
            year_data = {}
            for record in records:
                year = record["year"]
                count = record["count"]
                year_data[year] = count
                total += count
                print(f"{year} | {count:,}")

            print("-" * 40)
            print(f"Total | {total:,}")

            # Highlight key ranges
            print("\n" + "-" * 40)
            print("KEY DATE RANGES")
            print("-" * 40)

            range_2012_2017 = sum(year_data.get(str(y), 0) for y in range(2012, 2018))
            range_2018_2019 = sum(year_data.get(str(y), 0) for y in range(2018, 2020))
            range_2020_2025 = sum(year_data.get(str(y), 0) for y in range(2020, 2026))

            print(f"2012-2017 (NVD Import): {range_2012_2017:,}")
            print(f"2018-2019 (NVD Import): {range_2018_2019:,}")
            print(f"2020-2025 (Mixed Sources): {range_2020_2025:,}")

    def cves_by_severity(self):
        """Count CVEs by severity level"""
        self.print_header("CVE COUNT BY SEVERITY")

        query = """
        MATCH (c:CVE)
        WHERE c.severity IS NOT NULL
        RETURN c.severity as severity, count(c) as count
        ORDER BY
            CASE c.severity
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
                ELSE 5
            END
        """

        with self.driver.session() as session:
            results = session.run(query)
            records = list(results)

            print("\nSeverity | CVE Count | Percentage")
            print("-" * 50)

            total = sum(record["count"] for record in records)
            for record in records:
                severity = record["severity"]
                count = record["count"]
                pct = (count / total * 100) if total > 0 else 0
                print(f"{severity:10} | {count:8,} | {pct:5.1f}%")

            print("-" * 50)
            print(f"{'TOTAL':10} | {total:8,} | 100.0%")

    def cvss_score_distribution(self):
        """Analyze CVSS score distribution"""
        self.print_header("CVSS SCORE DISTRIBUTION")

        query = """
        MATCH (c:CVE)
        WHERE c.cvss_score IS NOT NULL AND c.cvss_score > 0
        RETURN
            min(c.cvss_score) as min_score,
            max(c.cvss_score) as max_score,
            avg(c.cvss_score) as avg_score,
            count(c) as total_with_scores
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()

            if record:
                print(f"\nMinimum CVSS Score: {record['min_score']:.1f}")
                print(f"Maximum CVSS Score: {record['max_score']:.1f}")
                print(f"Average CVSS Score: {record['avg_score']:.2f}")
                print(f"CVEs with Scores: {record['total_with_scores']:,}")

        # Score ranges
        query_ranges = """
        MATCH (c:CVE)
        WHERE c.cvss_score IS NOT NULL AND c.cvss_score > 0
        WITH
            CASE
                WHEN c.cvss_score >= 9.0 THEN 'CRITICAL (9.0-10.0)'
                WHEN c.cvss_score >= 7.0 THEN 'HIGH (7.0-8.9)'
                WHEN c.cvss_score >= 4.0 THEN 'MEDIUM (4.0-6.9)'
                ELSE 'LOW (0.1-3.9)'
            END as score_range,
            count(c) as count
        RETURN score_range, count
        ORDER BY
            CASE score_range
                WHEN 'CRITICAL (9.0-10.0)' THEN 1
                WHEN 'HIGH (7.0-8.9)' THEN 2
                WHEN 'MEDIUM (4.0-6.9)' THEN 3
                ELSE 4
            END
        """

        with self.driver.session() as session:
            results = session.run(query_ranges)
            records = list(results)

            print("\nScore Range | CVE Count | Percentage")
            print("-" * 50)

            total = sum(record["count"] for record in records)
            for record in records:
                range_label = record["score_range"]
                count = record["count"]
                pct = (count / total * 100) if total > 0 else 0
                print(f"{range_label:20} | {count:8,} | {pct:5.1f}%")

    def cve_cwe_relationships(self):
        """Analyze CVE→CWE relationships"""
        self.print_header("CVE → CWE RELATIONSHIPS")

        query = """
        MATCH (c:CVE)-[r:EXPLOITS_WEAKNESS]->(w:CWE)
        RETURN
            count(DISTINCT c) as cves_with_cwe,
            count(DISTINCT w) as unique_cwes,
            count(r) as total_relationships
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()

            if record:
                print(f"\nCVEs linked to CWEs: {record['cves_with_cwe']:,}")
                print(f"Unique CWEs referenced: {record['unique_cwes']:,}")
                print(f"Total CVE→CWE relationships: {record['total_relationships']:,}")

                # Calculate coverage
                total_query = "MATCH (c:CVE) RETURN count(c) as total"
                total_result = session.run(total_query)
                total_record = total_result.single()
                total_cves = total_record["total"]

                coverage = (record['cves_with_cwe'] / total_cves * 100) if total_cves > 0 else 0
                print(f"\nCWE Coverage: {coverage:.1f}% of all CVEs")

        # Top 10 most exploited CWEs
        query_top_cwes = """
        MATCH (c:CVE)-[r:EXPLOITS_WEAKNESS]->(w:CWE)
        WITH w, count(DISTINCT c) as cve_count
        ORDER BY cve_count DESC
        LIMIT 10
        RETURN w.cwe_id as cwe_id, w.name as cwe_name, cve_count
        """

        with self.driver.session() as session:
            results = session.run(query_top_cwes)
            records = list(results)

            if records:
                print("\n" + "-" * 80)
                print("TOP 10 MOST EXPLOITED CWEs")
                print("-" * 80)
                print(f"{'CWE ID':15} | {'CVE Count':12} | {'CWE Name'}")
                print("-" * 80)

                for record in records:
                    cwe_id = record["cwe_id"] or "N/A"
                    cve_count = record["cve_count"]
                    cwe_name = (record["cwe_name"] or "N/A")[:45]
                    print(f"{cwe_id:15} | {cve_count:12,} | {cwe_name}")

    def cve_capec_relationships(self):
        """Analyze CVE→CAPEC relationships"""
        self.print_header("CVE → CAPEC RELATIONSHIPS")

        query = """
        MATCH (c:CVE)-[r:ENABLES_ATTACK_PATTERN]->(a:CAPEC)
        RETURN
            count(DISTINCT c) as cves_with_capec,
            count(DISTINCT a) as unique_capecs,
            count(r) as total_relationships
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()

            if record and record['total_relationships'] > 0:
                print(f"\nCVEs linked to CAPECs: {record['cves_with_capec']:,}")
                print(f"Unique CAPECs referenced: {record['unique_capecs']:,}")
                print(f"Total CVE→CAPEC relationships: {record['total_relationships']:,}")

                # Calculate coverage
                total_query = "MATCH (c:CVE) RETURN count(c) as total"
                total_result = session.run(total_query)
                total_record = total_result.single()
                total_cves = total_record["total"]

                coverage = (record['cves_with_capec'] / total_cves * 100) if total_cves > 0 else 0
                print(f"\nCAPEC Coverage: {coverage:.1f}% of all CVEs")
            else:
                print("\n⚠️  No CVE→CAPEC relationships found")
                print("   This is expected if CAPEC linking hasn't been implemented yet")

    def document_mentions(self):
        """Analyze CVE mentions in documents"""
        self.print_header("CVE MENTIONS IN DOCUMENTS")

        # Check for direct Document→CVE relationships
        query = """
        MATCH (d:Document)-[r:MENTIONS_CVE]->(c:CVE)
        RETURN
            count(DISTINCT d) as docs_mentioning_cves,
            count(DISTINCT c) as unique_cves_mentioned,
            count(r) as total_mentions
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()

            if record and record['total_mentions'] > 0:
                print(f"\nDocuments mentioning CVEs: {record['docs_mentioning_cves']:,}")
                print(f"Unique CVEs mentioned: {record['unique_cves_mentioned']:,}")
                print(f"Total CVE mentions: {record['total_mentions']:,}")
            else:
                print("\n⚠️  No direct Document→CVE relationships found")
                print("   CVE mentions may be tracked through Entity nodes")

        # Check for Entity→CVE resolutions
        query_entities = """
        MATCH (e:Entity {label: 'CVE'})-[r:RESOLVES_TO]->(c:CVE)
        RETURN
            count(DISTINCT e) as resolved_entities,
            count(DISTINCT c) as unique_cves_resolved,
            count(r) as total_resolutions
        """

        with self.driver.session() as session:
            result = session.run(query_entities)
            record = result.single()

            if record and record['total_resolutions'] > 0:
                print("\n" + "-" * 40)
                print("ENTITY RESOLUTION (Entity→CVE)")
                print("-" * 40)
                print(f"Resolved CVE entities: {record['resolved_entities']:,}")
                print(f"Unique CVEs resolved to: {record['unique_cves_resolved']:,}")
                print(f"Total resolutions: {record['total_resolutions']:,}")

    def data_sources(self):
        """Analyze CVE data sources"""
        self.print_header("CVE DATA SOURCES")

        # Check for namespace property (indicates data source)
        query = """
        MATCH (c:CVE)
        WHERE c.namespace IS NOT NULL
        RETURN c.namespace as source, count(c) as count
        ORDER BY count DESC
        """

        with self.driver.session() as session:
            results = session.run(query)
            records = list(results)

            if records:
                print("\nData Source | CVE Count")
                print("-" * 40)
                for record in records:
                    source = record["source"]
                    count = record["count"]
                    print(f"{source:20} | {count:,}")
            else:
                print("\n⚠️  No namespace data found")
                print("   CVEs likely imported from NVD API without namespace tagging")

        # Check for CVEs with vs without published_date
        query_dates = """
        MATCH (c:CVE)
        RETURN
            count(CASE WHEN c.published_date IS NOT NULL THEN 1 END) as with_date,
            count(CASE WHEN c.published_date IS NULL THEN 1 END) as without_date,
            count(c) as total
        """

        with self.driver.session() as session:
            result = session.run(query_dates)
            record = result.single()

            if record:
                print("\n" + "-" * 40)
                print("DATA COMPLETENESS")
                print("-" * 40)
                print(f"CVEs with published_date: {record['with_date']:,}")
                print(f"CVEs without published_date: {record['without_date']:,}")

                completeness = (record['with_date'] / record['total'] * 100) if record['total'] > 0 else 0
                print(f"Date Completeness: {completeness:.1f}%")

    def generate_report(self):
        """Generate complete CVE statistics report"""
        print("\n")
        print("█" * 80)
        print("█" + " " * 78 + "█")
        print("█" + "CVE STATISTICS REPORT".center(78) + "█")
        print("█" + " " * 78 + "█")
        print("█" * 80)
        print(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Database: {NEO4J_URI}")

        # Run all statistics
        self.total_cve_count()
        self.cves_by_year()
        self.cves_by_severity()
        self.cvss_score_distribution()
        self.cve_cwe_relationships()
        self.cve_capec_relationships()
        self.document_mentions()
        self.data_sources()

        # Final summary
        self.print_header("REPORT COMPLETE")
        print("\n✅ CVE statistics report generated successfully")
        print("\n" + "█" * 80)
        print("\n")

def main():
    stats = CVEStatistics(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        stats.generate_report()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error generating statistics: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        stats.close()

if __name__ == "__main__":
    main()
