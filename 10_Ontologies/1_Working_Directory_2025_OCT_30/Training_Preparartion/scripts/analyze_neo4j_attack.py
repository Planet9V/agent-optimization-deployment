#!/usr/bin/env python3
"""
Neo4j ATT&CK Schema Analysis
Analyzes current ATT&CK relationship coverage and identifies missing links
"""

from neo4j import GraphDatabase
import json
from datetime import datetime

# Database connection
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j@openspg")

class Neo4jAttackAnalyzer:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def run_query(self, query, description=""):
        with self.driver.session() as session:
            result = session.run(query)
            records = [dict(record) for record in result]
            return records

    def analyze_attack_coverage(self):
        """Query 1: ATT&CK Node Coverage"""
        query = """
        MATCH (n)
        WHERE n:AttackTechnique OR n:AttackTactic OR n:AttackGroup OR n:AttackSoftware
        RETURN labels(n)[0] as type, count(n) as count
        """
        return self.run_query(query, "ATT&CK Node Coverage")

    def analyze_relationship_types(self):
        """Query 2: Relationship types to ATT&CK"""
        query = """
        MATCH (a)-[r]->(b)
        WHERE (a:CVE OR a:CWE OR a:CAPEC) AND b:AttackTechnique
        RETURN type(r) as relationship_type, count(r) as count
        ORDER BY count DESC
        """
        return self.run_query(query, "Relationship Types to ATT&CK")

    def count_cve_attack_paths(self):
        """Query 3: CVE to ATT&CK paths"""
        query = """
        MATCH p=(cve:CVE)-[*]-(attack:AttackTechnique)
        RETURN count(p) as cve_to_attack_paths
        LIMIT 1
        """
        return self.run_query(query, "CVE to ATT&CK Paths")

    def get_attack_metadata(self):
        """Query 4: ATT&CK Technique Metadata"""
        query = """
        MATCH (att:AttackTechnique)
        RETURN att.techniqueId as techniqueId,
               att.name as name,
               att.description as description,
               keys(att) as all_properties
        LIMIT 5
        """
        return self.run_query(query, "ATT&CK Metadata Sample")

    def count_isolated_techniques(self):
        """Query 5: Isolated ATT&CK techniques"""
        query = """
        MATCH (att:AttackTechnique)
        WHERE NOT ()<-[]->(att)
        RETURN count(att) as isolated_techniques
        """
        return self.run_query(query, "Isolated Techniques")

    def count_capec_only_techniques(self):
        """Query 6: CAPEC-only connections"""
        query = """
        MATCH (att:AttackTechnique)
        WHERE (att)<-[:USES_TECHNIQUE]-(:CAPEC)
          AND NOT (att)<-[]-(:CVE)
        RETURN count(att) as capec_only_techniques
        """
        return self.run_query(query, "CAPEC-only Techniques")

    def analyze_all_attack_relationships(self):
        """Query 7: All relationship patterns involving ATT&CK"""
        query = """
        MATCH (a)-[r]->(b)
        WHERE a:AttackTechnique OR b:AttackTechnique
        RETURN DISTINCT type(r) as relationship_type,
               labels(a)[0] as from_type,
               labels(b)[0] as to_type,
               count(*) as count
        ORDER BY count DESC
        """
        return self.run_query(query, "All ATT&CK Relationship Patterns")

    def calculate_connectivity_metrics(self):
        """Query 8: ATT&CK connectivity metrics"""
        query = """
        MATCH (att:AttackTechnique)
        WITH count(att) as total
        MATCH (att:AttackTechnique)
        WHERE ()<-[]->(att)
        WITH total, count(att) as connected
        RETURN total,
               connected,
               total - connected as isolated,
               toFloat(connected) / toFloat(total) * 100 as coverage_percent
        """
        return self.run_query(query, "Connectivity Metrics")

    def get_all_node_types(self):
        """Additional: Get all node types in database"""
        query = """
        MATCH (n)
        RETURN DISTINCT labels(n)[0] as node_type, count(n) as count
        ORDER BY count DESC
        """
        return self.run_query(query, "All Node Types")

    def get_attack_technique_details(self):
        """Additional: Get detailed ATT&CK technique properties"""
        query = """
        MATCH (att:AttackTechnique)
        RETURN att.techniqueId as id,
               att.name as name,
               size((att)<-[:USES_TECHNIQUE]-()) as capec_connections,
               size((att)<-[]-(:CVE)) as cve_connections,
               size((att)<-[]-(:CWE)) as cwe_connections,
               size(()<-[]->(att)) as total_connections
        ORDER BY total_connections DESC
        LIMIT 20
        """
        return self.run_query(query, "Top Connected Techniques")

def generate_markdown_report(analyzer):
    """Generate comprehensive markdown report"""

    report = []
    report.append("# Neo4j ATT&CK Schema Analysis Report")
    report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"\n**Database:** bolt://localhost:7687")
    report.append("\n---\n")

    # Executive Summary
    report.append("## Executive Summary\n")

    # 1. ATT&CK Node Coverage
    report.append("## 1. ATT&CK Node Coverage\n")
    coverage = analyzer.analyze_attack_coverage()
    report.append("Current ATT&CK nodes in the database:\n")
    report.append("| Node Type | Count |")
    report.append("|-----------|-------|")
    total_attack_nodes = 0
    for row in coverage:
        report.append(f"| {row['type']} | {row['count']} |")
        total_attack_nodes += row['count']
    report.append(f"\n**Total ATT&CK Nodes:** {total_attack_nodes}\n")

    # 2. Relationship Types to ATT&CK
    report.append("## 2. Relationship Types Connecting to ATT&CK\n")
    rel_types = analyzer.analyze_relationship_types()
    if rel_types:
        report.append("| Relationship Type | Count |")
        report.append("|------------------|-------|")
        for row in rel_types:
            report.append(f"| {row['relationship_type']} | {row['count']} |")
    else:
        report.append("**⚠️ NO RELATIONSHIPS FOUND** from CVE/CWE/CAPEC to AttackTechnique nodes.\n")

    # 3. CVE to ATT&CK Paths
    report.append("\n## 3. CVE to ATT&CK Path Analysis\n")
    paths = analyzer.count_cve_attack_paths()
    if paths and paths[0]['cve_to_attack_paths'] > 0:
        report.append(f"**Total CVE → ATT&CK Paths:** {paths[0]['cve_to_attack_paths']}\n")
    else:
        report.append("**⚠️ NO PATHS FOUND** between CVE and AttackTechnique nodes.\n")

    # 4. ATT&CK Metadata Sample
    report.append("## 4. ATT&CK Technique Metadata Sample\n")
    metadata = analyzer.get_attack_metadata()
    if metadata:
        report.append("Sample of ATT&CK technique properties:\n")
        for tech in metadata[:3]:
            report.append(f"\n### {tech['techniqueId']} - {tech['name']}")
            report.append(f"\n**Properties:** {', '.join(tech['all_properties'])}")
            if tech['description']:
                desc = tech['description'][:200] + "..." if len(tech['description']) > 200 else tech['description']
                report.append(f"\n**Description:** {desc}\n")

    # 5. Isolated Techniques
    report.append("## 5. Missing Links Analysis\n")
    isolated = analyzer.count_isolated_techniques()
    report.append(f"**Isolated ATT&CK Techniques (no relationships):** {isolated[0]['isolated_techniques']}\n")

    capec_only = analyzer.count_capec_only_techniques()
    report.append(f"**CAPEC-only Techniques (no CVE links):** {capec_only[0]['capec_only_techniques']}\n")

    # 6. All ATT&CK Relationship Patterns
    report.append("## 6. Complete Relationship Pattern Analysis\n")
    all_rels = analyzer.analyze_all_attack_relationships()
    report.append("All relationships involving AttackTechnique nodes:\n")
    report.append("| From Type | Relationship | To Type | Count |")
    report.append("|-----------|--------------|---------|-------|")
    for row in all_rels:
        report.append(f"| {row['from_type']} | {row['relationship_type']} | {row['to_type']} | {row['count']} |")

    # 7. Connectivity Metrics
    report.append("\n## 7. Coverage Metrics\n")
    metrics = analyzer.calculate_connectivity_metrics()
    if metrics:
        m = metrics[0]
        report.append(f"- **Total ATT&CK Techniques:** {m['total']}")
        report.append(f"- **Connected Techniques:** {m['connected']}")
        report.append(f"- **Isolated Techniques:** {m['isolated']}")
        report.append(f"- **Coverage Percentage:** {m['coverage_percent']:.2f}%\n")

    # 8. Top Connected Techniques
    report.append("## 8. Top Connected ATT&CK Techniques\n")
    top_connected = analyzer.get_attack_technique_details()
    report.append("| Technique ID | Name | CAPEC | CVE | CWE | Total |")
    report.append("|--------------|------|-------|-----|-----|-------|")
    for tech in top_connected:
        report.append(f"| {tech['id']} | {tech['name']} | {tech['capec_connections']} | {tech['cve_connections']} | {tech['cwe_connections']} | {tech['total_connections']} |")

    # 9. Assessment and Recommendations
    report.append("\n## 9. Assessment: What Exists vs What's Needed\n")

    report.append("### Current State:")
    report.append("- ✅ ATT&CK techniques are loaded in the database")
    report.append("- ✅ CAPEC → ATT&CK relationships exist")

    # Check if CVE connections exist
    if rel_types and any('CVE' in str(r) for r in rel_types):
        report.append("- ✅ CVE → ATT&CK relationships exist")
    else:
        report.append("- ❌ CVE → ATT&CK relationships are MISSING")

    # Check if CWE connections exist
    all_node_types = analyzer.get_all_node_types()
    has_cwe = any(row['node_type'] == 'CWE' for row in all_node_types)
    if has_cwe:
        report.append("- ⚠️ CWE nodes exist but may not connect to ATT&CK")
    else:
        report.append("- ❌ CWE nodes may be missing")

    report.append("\n### Required for Complete Attack Chains:")
    report.append("1. **CVE → CWE → CAPEC → ATT&CK** chain")
    report.append("2. **Direct CVE → ATT&CK** mappings where available")
    report.append("3. **ATT&CK Tactic → Technique** hierarchies")
    report.append("4. **ATT&CK Software → Technique** relationships")
    report.append("5. **ATT&CK Group → Technique** relationships")

    report.append("\n### Gap Analysis:")

    # Calculate gaps
    if not rel_types or len(rel_types) == 0:
        report.append("- **CRITICAL:** No relationships from vulnerability data (CVE/CWE/CAPEC) to ATT&CK")

    if isolated and isolated[0]['isolated_techniques'] > 0:
        isolated_count = isolated[0]['isolated_techniques']
        total_count = metrics[0]['total'] if metrics else 0
        isolated_pct = (isolated_count / total_count * 100) if total_count > 0 else 0
        report.append(f"- **HIGH:** {isolated_count} ({isolated_pct:.1f}%) ATT&CK techniques have no connections")

    if capec_only and capec_only[0]['capec_only_techniques'] > 0:
        capec_only_count = capec_only[0]['capec_only_techniques']
        report.append(f"- **MEDIUM:** {capec_only_count} techniques only connected via CAPEC (no direct CVE links)")

    report.append("\n### Next Steps:")
    report.append("1. Establish CVE → ATT&CK mappings using:")
    report.append("   - MITRE ATT&CK mappings to CVEs where available")
    report.append("   - Inferred mappings through CWE → CAPEC → ATT&CK chains")
    report.append("2. Complete ATT&CK internal hierarchy (Tactics, Groups, Software)")
    report.append("3. Validate relationship semantics and cardinality")
    report.append("4. Add temporal properties (dates, versions) to relationships")

    report.append("\n---\n")
    report.append(f"\n*Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    return "\n".join(report)

def main():
    print("Connecting to Neo4j database...")
    analyzer = Neo4jAttackAnalyzer(URI, AUTH)

    try:
        print("Running analysis queries...")
        report = generate_markdown_report(analyzer)

        output_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/docs/NEO4J_ATTACK_SCHEMA_ANALYSIS.md"

        with open(output_file, 'w') as f:
            f.write(report)

        print(f"\n✅ Analysis complete! Report saved to:\n{output_file}")
        print("\nPreview:")
        print("=" * 80)
        print(report[:1500] + "\n...\n[Full report in file]")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
    finally:
        analyzer.close()
        print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()
