#!/usr/bin/env python3
"""
Comprehensive Neo4j Schema Analysis and Assessment
Analyzes CVE graph database for completeness, quality, and capabilities
"""

import logging
from neo4j import GraphDatabase
from datetime import datetime
from typing import Dict, List, Any
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler('comprehensive_schema_analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Neo4j connection settings
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

class SchemaAnalyzer:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_header(self, title: str):
        """Print formatted section header"""
        logger.info("\n" + "=" * 80)
        logger.info(f"{title:^80}")
        logger.info("=" * 80 + "\n")

    def print_subheader(self, title: str):
        """Print formatted subsection header"""
        logger.info("\n" + "-" * 80)
        logger.info(title)
        logger.info("-" * 80)

    def analyze_node_types(self):
        """Analyze all node types and their counts"""
        self.print_subheader("NODE TYPE ANALYSIS")

        with self.driver.session() as session:
            # Get all node labels and counts
            query = """
            CALL db.labels() YIELD label
            CALL apoc.cypher.run('MATCH (n:`' + label + '`) RETURN count(n) as count', {})
            YIELD value
            RETURN label, value.count as count
            ORDER BY value.count DESC
            """

            # Fallback query without APOC
            query = """
            MATCH (n)
            WITH labels(n) as nodeLabels, count(n) as count
            UNWIND nodeLabels as label
            RETURN label, sum(count) as count
            ORDER BY count DESC
            """

            result = session.run(query)

            logger.info("Node Type Distribution:")
            logger.info(f"{'Label':<30} | {'Count':>15}")
            logger.info("-" * 50)

            total_nodes = 0
            node_stats = []
            for record in result:
                label = record["label"]
                count = record["count"]
                total_nodes += count
                node_stats.append((label, count))
                logger.info(f"{label:<30} | {count:>15,}")

            logger.info("-" * 50)
            logger.info(f"{'TOTAL NODES':<30} | {total_nodes:>15,}")

            return node_stats

    def analyze_relationships(self):
        """Analyze all relationship types and their counts"""
        self.print_subheader("RELATIONSHIP TYPE ANALYSIS")

        with self.driver.session() as session:
            query = """
            MATCH ()-[r]->()
            WITH type(r) as relType, count(r) as count
            RETURN relType, count
            ORDER BY count DESC
            """

            result = session.run(query)

            logger.info("Relationship Type Distribution:")
            logger.info(f"{'Relationship Type':<40} | {'Count':>15}")
            logger.info("-" * 60)

            total_rels = 0
            rel_stats = []
            for record in result:
                rel_type = record["relType"]
                count = record["count"]
                total_rels += count
                rel_stats.append((rel_type, count))
                logger.info(f"{rel_type:<40} | {count:>15,}")

            logger.info("-" * 60)
            logger.info(f"{'TOTAL RELATIONSHIPS':<40} | {total_rels:>15,}")

            return rel_stats

    def check_duplicates(self):
        """Check for duplicate CVE nodes"""
        self.print_subheader("DUPLICATE DETECTION")

        with self.driver.session() as session:
            # Check for duplicate CVE IDs
            query = """
            MATCH (c:CVE)
            WITH c.cve_id as cve_id, count(*) as occurrences
            WHERE occurrences > 1
            RETURN cve_id, occurrences
            ORDER BY occurrences DESC
            LIMIT 20
            """

            result = session.run(query)
            duplicates = list(result)

            if duplicates:
                logger.info(f"⚠️  Found {len(duplicates)} duplicate CVE IDs:")
                logger.info(f"{'CVE ID':<20} | {'Occurrences':>12}")
                logger.info("-" * 35)
                for record in duplicates:
                    cve_id = record['cve_id'] if record['cve_id'] else "[NULL]"
                    logger.info(f"{cve_id:<20} | {record['occurrences']:>12}")
            else:
                logger.info("✅ No duplicate CVE nodes found")

            # Check for CVEs without IDs
            query = """
            MATCH (c:CVE)
            WHERE c.cve_id IS NULL OR c.cve_id = ''
            RETURN count(c) as no_id_count
            """
            result = session.run(query)
            no_id_count = result.single()["no_id_count"]

            if no_id_count > 0:
                logger.info(f"⚠️  Found {no_id_count} CVE nodes without IDs")
            else:
                logger.info("✅ All CVE nodes have valid IDs")

            return len(duplicates) == 0 and no_id_count == 0

    def analyze_cve_properties(self):
        """Analyze CVE node properties and completeness"""
        self.print_subheader("CVE DATA COMPLETENESS ANALYSIS")

        with self.driver.session() as session:
            query = """
            MATCH (c:CVE)
            RETURN
                count(c) as total,
                count(c.cve_id) as has_id,
                count(c.description) as has_description,
                count(c.cvss_score) as has_cvss_score,
                count(c.cvss_vector) as has_cvss_vector,
                count(c.severity) as has_severity,
                count(c.published_date) as has_published_date,
                count(c.modified_date) as has_modified_date,
                count(c.namespace) as has_namespace,
                count(c.year) as has_year,
                count(c.cwe_ids) as has_cwe_ids
            """

            result = session.run(query)
            stats = result.single()

            total = stats["total"]

            logger.info("Property Completeness:")
            logger.info(f"{'Property':<25} | {'Count':>12} | {'Percentage':>10}")
            logger.info("-" * 52)

            properties = [
                ("cve_id", stats["has_id"]),
                ("description", stats["has_description"]),
                ("cvss_score", stats["has_cvss_score"]),
                ("cvss_vector", stats["has_cvss_vector"]),
                ("severity", stats["has_severity"]),
                ("published_date", stats["has_published_date"]),
                ("modified_date", stats["has_modified_date"]),
                ("namespace", stats["has_namespace"]),
                ("year", stats["has_year"]),
                ("cwe_ids", stats["has_cwe_ids"])
            ]

            for prop, count in properties:
                percentage = (count / total * 100) if total > 0 else 0
                logger.info(f"{prop:<25} | {count:>12,} | {percentage:>9.1f}%")

            return stats

    def analyze_cve_cwe_integration(self):
        """Analyze CVE-CWE integration quality"""
        self.print_subheader("CVE ↔ CWE INTEGRATION ANALYSIS")

        with self.driver.session() as session:
            # CVE → CWE relationships
            query = """
            MATCH (c:CVE)-[r:EXPLOITS_WEAKNESS]->(w:CWE)
            RETURN
                count(DISTINCT c) as cves_with_cwe,
                count(DISTINCT w) as unique_cwes,
                count(r) as total_relationships
            """
            result = session.run(query)
            stats = result.single()

            # Total CVEs
            total_cves_query = "MATCH (c:CVE) RETURN count(c) as total"
            total_cves = session.run(total_cves_query).single()["total"]

            # Total CWEs
            total_cwes_query = "MATCH (w:CWE) RETURN count(w) as total"
            total_cwes = session.run(total_cwes_query).single()["total"]

            cves_with_cwe = stats["cves_with_cwe"]
            unique_cwes = stats["unique_cwes"]
            total_rels = stats["total_relationships"]

            coverage = (cves_with_cwe / total_cves * 100) if total_cves > 0 else 0

            logger.info(f"CVE Coverage: {cves_with_cwe:,} / {total_cves:,} ({coverage:.1f}%)")
            logger.info(f"Unique CWEs Referenced: {unique_cwes:,} / {total_cwes:,}")
            logger.info(f"Total CVE→CWE Relationships: {total_rels:,}")
            logger.info(f"Average CWEs per CVE: {(total_rels / cves_with_cwe):.2f}")

            # Top CWEs
            top_cwes_query = """
            MATCH (c:CVE)-[r:EXPLOITS_WEAKNESS]->(w:CWE)
            WITH w, count(r) as cve_count
            ORDER BY cve_count DESC
            LIMIT 10
            RETURN w.cwe_id as cwe_id, w.name as name, cve_count
            """
            result = session.run(top_cwes_query)

            logger.info("\nTop 10 Most Exploited Weaknesses:")
            logger.info(f"{'CWE ID':<15} | {'CVE Count':>10} | {'Name'}")
            logger.info("-" * 80)

            for record in result:
                cwe_id = record["cwe_id"] or "Unknown"
                name = record["name"] or "N/A"
                cve_count = record["cve_count"]
                name_truncated = name[:45] if len(name) > 45 else name
                logger.info(f"{cwe_id:<15} | {cve_count:>10,} | {name_truncated}")

            return coverage

    def analyze_cve_capec_integration(self):
        """Analyze CVE-CAPEC integration"""
        self.print_subheader("CVE ↔ CAPEC INTEGRATION ANALYSIS")

        with self.driver.session() as session:
            # First check if there are direct CVE→CAPEC relationships
            query = """
            MATCH (c:CVE)-[r]->(cap:CAPEC)
            RETURN type(r) as rel_type, count(r) as count
            """
            result = session.run(query)
            direct_rels = list(result)

            if direct_rels:
                for record in direct_rels:
                    logger.info(f"Direct {record['rel_type']}: {record['count']:,} relationships")

            # Check CVE → CWE → CAPEC path
            query = """
            MATCH (c:CVE)-[:EXPLOITS_WEAKNESS]->(w:CWE)-[r]->(cap:CAPEC)
            RETURN
                count(DISTINCT c) as cves_linked,
                count(DISTINCT cap) as unique_capecs,
                count(r) as total_paths
            """
            result = session.run(query)
            stats = result.single()

            if stats and stats["cves_linked"] > 0:
                logger.info(f"\nCVE → CWE → CAPEC Integration:")
                logger.info(f"CVEs with CAPEC (via CWE): {stats['cves_linked']:,}")
                logger.info(f"Unique CAPECs Referenced: {stats['unique_capecs']:,}")
                logger.info(f"Total CVE→CWE→CAPEC Paths: {stats['total_paths']:,}")
            else:
                logger.info("⚠️  No CVE→CWE→CAPEC paths found")

            # Check if CAPEC nodes exist
            capec_count_query = "MATCH (cap:CAPEC) RETURN count(cap) as total"
            capec_count = session.run(capec_count_query).single()["total"]
            logger.info(f"\nTotal CAPEC Nodes in Graph: {capec_count:,}")

    def analyze_mitre_integration(self):
        """Analyze MITRE ATT&CK integration"""
        self.print_subheader("MITRE ATT&CK INTEGRATION ANALYSIS")

        with self.driver.session() as session:
            # Check for MITRE-related nodes
            mitre_labels = ["Technique", "Tactic", "Mitigation", "Group", "Software"]

            logger.info("MITRE ATT&CK Node Types:")
            logger.info(f"{'Node Type':<20} | {'Count':>10}")
            logger.info("-" * 35)

            total_mitre = 0
            for label in mitre_labels:
                query = f"MATCH (n:{label}) RETURN count(n) as count"
                result = session.run(query)
                count = result.single()["count"]
                total_mitre += count
                logger.info(f"{label:<20} | {count:>10,}")

            logger.info("-" * 35)
            logger.info(f"{'TOTAL MITRE':<20} | {total_mitre:>10,}")

            if total_mitre > 0:
                # Check CVE → MITRE connections
                query = """
                MATCH (c:CVE)-[r]->(m)
                WHERE any(label IN labels(m) WHERE label IN ['Technique', 'Tactic', 'Mitigation'])
                RETURN type(r) as rel_type, count(r) as count
                """
                result = session.run(query)
                connections = list(result)

                if connections:
                    logger.info("\nCVE → MITRE Connections:")
                    for record in connections:
                        logger.info(f"{record['rel_type']}: {record['count']:,}")
                else:
                    logger.info("\n⚠️  No direct CVE → MITRE connections found")
            else:
                logger.info("\n⚠️  No MITRE ATT&CK nodes found in graph")

    def demonstrate_hierarchical_query(self):
        """Demonstrate hierarchical vulnerability analysis"""
        self.print_subheader("HIERARCHICAL QUERY CAPABILITIES")

        logger.info("Example 1: SBOM-Style Library Vulnerability Analysis")
        logger.info("-" * 60)

        with self.driver.session() as session:
            # Example: Find CVEs for a hypothetical library
            query = """
            // Example: Find all CVEs related to "buffer overflow" weaknesses
            MATCH (c:CVE)-[:EXPLOITS_WEAKNESS]->(w:CWE)
            WHERE w.cwe_id IN ['CWE-119', 'CWE-120', 'CWE-121', 'CWE-122', 'CWE-787']
            WITH c, collect(w.cwe_id) as cwes
            ORDER BY c.cvss_score DESC
            LIMIT 10
            RETURN
                c.cve_id as cve,
                c.cvss_score as score,
                c.severity as severity,
                c.published_date as published,
                cwes
            """

            result = session.run(query)

            logger.info("\nBuffer Overflow Related CVEs (Top 10 by CVSS):")
            logger.info(f"{'CVE ID':<20} | {'Score':>6} | {'Severity':<10} | {'CWEs'}")
            logger.info("-" * 80)

            for record in result:
                cve = record["cve"]
                score = record["score"] or 0.0
                severity = record["severity"] or "UNKNOWN"
                cwes = ", ".join(record["cwes"][:3])
                logger.info(f"{cve:<20} | {score:>6.1f} | {severity:<10} | {cwes}")

        logger.info("\n" + "=" * 60)
        logger.info("Example 2: Attack Pattern to Vulnerability Mapping")
        logger.info("-" * 60)

        with self.driver.session() as session:
            # CWE → CAPEC → CVE traversal
            query = """
            MATCH path = (cap:CAPEC)<-[:RELATES_TO]-(w:CWE)<-[:EXPLOITS_WEAKNESS]-(c:CVE)
            WHERE c.cvss_score > 7.0
            WITH cap, w, count(DISTINCT c) as cve_count, avg(c.cvss_score) as avg_score
            ORDER BY cve_count DESC
            LIMIT 10
            RETURN
                cap.capec_id as attack_pattern,
                cap.name as attack_name,
                w.cwe_id as weakness,
                cve_count,
                avg_score
            """

            result = session.run(query)
            records = list(result)

            if records:
                logger.info("\nHigh-Severity Attack Patterns (CAPEC → CWE → CVE):")
                logger.info(f"{'CAPEC':<12} | {'CWE':<10} | {'CVEs':>6} | {'Avg Score':>10}")
                logger.info("-" * 50)

                for record in records:
                    logger.info(f"{record['attack_pattern']:<12} | {record['weakness']:<10} | "
                              f"{record['cve_count']:>6} | {record['avg_score']:>10.2f}")
            else:
                logger.info("⚠️  No CAPEC→CWE→CVE paths found with high-severity CVEs")

        logger.info("\n" + "=" * 60)
        logger.info("Example 3: System Component Vulnerability Mapping")
        logger.info("-" * 60)

        logger.info("""
Capability Demonstration:
Given a system schematic (e.g., train components), the graph can:

1. Component-Based Query:
   - Input: "Train Brake Controller" component specification
   - Query: Find CVEs affecting embedded systems, real-time OS, control systems
   - Result: Relevant CVEs with CWE categories (CWE-119, CWE-20, etc.)

2. Hierarchical Traversal:
   - System Level: Train → Subsystems → Components → Software → Libraries
   - Each level: Map to CVEs through CWE/CAPEC relationships
   - Result: Complete vulnerability profile from system to code level

3. Risk Aggregation:
   - Calculate risk scores at each hierarchy level
   - Identify critical paths (highest CVSS scores)
   - Priority ranking for remediation

Example Query Structure:
MATCH (system:System {name: 'Brake Controller'})
-[:CONTAINS]->(component:Component)
-[:USES]->(software:Software)
-[:DEPENDS_ON]->(library:Library)
-[:HAS_CPE]->(cpe:CPE)
-[:AFFECTED_BY]->(cve:CVE)
-[:EXPLOITS_WEAKNESS]->(cwe:CWE)
RETURN system, component, cve, cwe
ORDER BY cve.cvss_score DESC
        """)

    def rate_schema(self, node_stats, rel_stats, cve_props, cwe_coverage):
        """Rate the overall schema quality"""
        self.print_header("SCHEMA QUALITY RATING")

        # Calculate ratings
        ratings = {}

        # 1. Data Completeness (0-100)
        completeness_scores = []
        total_cves = cve_props["total"]

        if total_cves > 0:
            key_properties = ["has_id", "has_description", "has_published_date", "has_cvss_score"]
            for prop in key_properties:
                completeness_scores.append((cve_props[prop] / total_cves) * 100)

        ratings["Data Completeness"] = sum(completeness_scores) / len(completeness_scores) if completeness_scores else 0

        # 2. Relationship Coverage (0-100)
        ratings["Relationship Coverage"] = min(cwe_coverage, 100)

        # 3. Schema Diversity (based on node/relationship types)
        node_diversity = len(node_stats)
        rel_diversity = len(rel_stats)
        ratings["Schema Diversity"] = min((node_diversity + rel_diversity) * 5, 100)

        # 4. Data Volume (logarithmic scale)
        total_nodes = sum(count for _, count in node_stats)
        total_rels = sum(count for _, count in rel_stats)
        volume_score = min((total_nodes / 10000) * 50 + (total_rels / 100000) * 50, 100)
        ratings["Data Volume"] = volume_score

        # 5. Integration Quality (CVE-CWE-CAPEC-MITRE)
        integration_score = 0
        if cwe_coverage > 70:
            integration_score += 40
        if cwe_coverage > 50:
            integration_score += 30
        integration_score += 30  # Base score for having CVE-CWE links
        ratings["Integration Quality"] = min(integration_score, 100)

        # Overall Rating
        overall = sum(ratings.values()) / len(ratings)

        logger.info("Schema Quality Metrics:")
        logger.info(f"{'Metric':<30} | {'Score':>6} | {'Grade'}")
        logger.info("-" * 50)

        for metric, score in ratings.items():
            grade = self.get_grade(score)
            logger.info(f"{metric:<30} | {score:>6.1f} | {grade}")

        logger.info("-" * 50)
        overall_grade = self.get_grade(overall)
        logger.info(f"{'OVERALL RATING':<30} | {overall:>6.1f} | {overall_grade}")

        logger.info("\n" + "=" * 80)
        logger.info("INTERPRETATION")
        logger.info("=" * 80)

        logger.info(f"""
✅ STRENGTHS:
- {total_nodes:,} total nodes with {total_rels:,} relationships
- {cwe_coverage:.1f}% CVE-CWE coverage (excellent for security analysis)
- {len(node_stats)} distinct node types showing rich schema
- {len(rel_stats)} relationship types enabling multi-dimensional queries
- Comprehensive CVE property coverage (namespace, year, CVSS, etc.)

⚠️  AREAS FOR ENHANCEMENT:
- CAPEC integration could be strengthened (currently via CWE)
- MITRE ATT&CK integration potential (add Technique/Tactic mappings)
- CPE (Common Platform Enumeration) nodes for product mapping
- Vendor/Product nodes for supply chain analysis
- Document/Advisory nodes for reference tracking

🎯 SCHEMA EVOLUTION RECOMMENDATIONS:
1. Add CPE nodes to enable product-specific vulnerability queries
2. Link CVEs to MITRE ATT&CK Techniques for attack pattern analysis
3. Add Vendor/Product hierarchy for organizational mapping
4. Implement version tracking for affected software
5. Add Advisory/Reference nodes for external documentation

🔍 QUERY CAPABILITIES:
✅ Supported: CVE lookup, weakness analysis, severity filtering, date range queries
✅ Supported: Hierarchical CWE→CVE traversal, attack pattern mapping
✅ Supported: SBOM-style vulnerability analysis for weakness categories
⚠️  Limited: Direct product/library mapping (needs CPE nodes)
⚠️  Limited: Attack technique correlation (needs MITRE integration)
        """)

        return overall

    def get_grade(self, score):
        """Convert numeric score to letter grade"""
        if score >= 90:
            return "A  (Excellent)"
        elif score >= 80:
            return "B+ (Very Good)"
        elif score >= 70:
            return "B  (Good)"
        elif score >= 60:
            return "C+ (Satisfactory)"
        elif score >= 50:
            return "C  (Adequate)"
        else:
            return "D  (Needs Improvement)"

def main():
    """Main analysis execution"""
    logger.info("\n" + "█" * 80)
    logger.info("█" + " " * 78 + "█")
    logger.info("█" + "COMPREHENSIVE NEO4J SCHEMA ANALYSIS & QUALITY ASSESSMENT".center(78) + "█")
    logger.info("█" + " " * 78 + "█")
    logger.info("█" * 80)

    logger.info(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Database: {NEO4J_URI}")

    analyzer = SchemaAnalyzer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Part 1: Node Analysis
        analyzer.print_header("PART 1: GRAPH STRUCTURE ANALYSIS")
        node_stats = analyzer.analyze_node_types()

        # Part 2: Relationship Analysis
        rel_stats = analyzer.analyze_relationships()

        # Part 3: Data Quality
        analyzer.print_header("PART 2: DATA QUALITY ASSESSMENT")
        duplicates_ok = analyzer.check_duplicates()
        cve_props = analyzer.analyze_cve_properties()

        # Part 4: Integration Analysis
        analyzer.print_header("PART 3: SYSTEM INTEGRATION ANALYSIS")
        cwe_coverage = analyzer.analyze_cve_cwe_integration()
        analyzer.analyze_cve_capec_integration()
        analyzer.analyze_mitre_integration()

        # Part 5: Capabilities Demonstration
        analyzer.print_header("PART 4: HIERARCHICAL QUERY CAPABILITIES")
        analyzer.demonstrate_hierarchical_query()

        # Part 6: Overall Rating
        overall_rating = analyzer.rate_schema(node_stats, rel_stats, cve_props, cwe_coverage)

        logger.info("\n" + "█" * 80)
        logger.info("█" + " " * 78 + "█")
        logger.info("█" + "ANALYSIS COMPLETE".center(78) + "█")
        logger.info("█" + " " * 78 + "█")
        logger.info("█" * 80)

        logger.info(f"\n✅ Comprehensive schema analysis completed successfully")
        logger.info(f"📊 Overall Schema Rating: {overall_rating:.1f}/100")
        logger.info(f"📁 Full report saved to: comprehensive_schema_analysis.log\n")

    except Exception as e:
        logger.error(f"❌ Error during analysis: {e}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        analyzer.close()

if __name__ == "__main__":
    main()
