#!/usr/bin/env python3
"""
Neo4j ATT&CK Schema Analysis - Robust Version with Retries
"""

from neo4j import GraphDatabase
import time
from datetime import datetime

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j@openspg")

class Neo4jAttackAnalyzer:
    def __init__(self, uri, auth, max_retries=5):
        self.uri = uri
        self.auth = auth
        self.max_retries = max_retries
        self.driver = None
        self._connect()

    def _connect(self):
        """Connect with retries"""
        for attempt in range(self.max_retries):
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=self.auth)
                # Test connection
                with self.driver.session() as session:
                    session.run("RETURN 1")
                print(f"✅ Connected to Neo4j")
                return
            except Exception as e:
                print(f"Connection attempt {attempt + 1}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(5)
                else:
                    raise

    def close(self):
        if self.driver:
            self.driver.close()

    def run_query(self, query, description="", handle_empty=True):
        """Run query with better error handling"""
        try:
            with self.driver.session() as session:
                result = session.run(query)
                records = [dict(record) for record in result]
                return records if records else [] if handle_empty else None
        except Exception as e:
            print(f"⚠️ Query failed ({description}): {e}")
            return [] if handle_empty else None

    def discover_schema(self):
        """Discover what's actually in the database"""
        print("\n🔍 Discovering database schema...")

        # Get all labels
        labels_query = "CALL db.labels()"
        labels = self.run_query(labels_query, "Get labels")
        available_labels = [r['label'] for r in labels] if labels else []

        print(f"   Found {len(available_labels)} labels")

        # Count nodes for each label
        schema = {}
        for label in available_labels:
            count_query = f"MATCH (n:{label}) RETURN count(n) as count"
            result = self.run_query(count_query, f"Count {label}")
            if result:
                schema[label] = result[0]['count']

        return schema, available_labels

    def analyze_attack_nodes(self, labels):
        """Query 1: ATT&CK Node Coverage"""
        print("📊 Analyzing ATT&CK node coverage...")

        attack_labels = [l for l in labels if 'Attack' in l or 'attack' in l.lower()]
        results = []

        for label in attack_labels:
            query = f"MATCH (n:{label}) RETURN '{label}' as type, count(n) as count"
            result = self.run_query(query, f"Count {label}")
            if result:
                results.extend(result)

        return results

    def analyze_relationships(self):
        """Query 2: All relationship patterns"""
        print("🔗 Analyzing relationship patterns...")

        query = """
        MATCH (a)-[r]->(b)
        RETURN DISTINCT labels(a)[0] as from_label,
               type(r) as relationship_type,
               labels(b)[0] as to_label,
               count(*) as count
        ORDER BY count DESC
        LIMIT 100
        """
        return self.run_query(query, "All relationships")

    def analyze_attack_relationships(self):
        """Query 3: Relationships involving ATT&CK nodes"""
        print("⚔️ Analyzing ATT&CK relationships...")

        query = """
        MATCH (a)-[r]->(b)
        WHERE any(label IN labels(a) WHERE label CONTAINS 'Attack')
           OR any(label IN labels(b) WHERE label CONTAINS 'Attack')
        RETURN DISTINCT labels(a)[0] as from_label,
               type(r) as relationship_type,
               labels(b)[0] as to_label,
               count(*) as count
        ORDER BY count DESC
        """
        return self.run_query(query, "ATT&CK relationships")

    def analyze_vulnerability_to_attack_paths(self):
        """Query 4: CVE/CWE/CAPEC to ATT&CK paths"""
        print("🛤️ Analyzing vulnerability → ATT&CK paths...")

        results = {}

        # CVE → ATT&CK
        query_cve = """
        MATCH p=(cve:CVE)-[*1..3]-(att)
        WHERE any(label IN labels(att) WHERE label CONTAINS 'Attack')
        RETURN count(DISTINCT p) as paths,
               count(DISTINCT cve) as cve_count,
               count(DISTINCT att) as attack_count
        """
        results['cve_to_attack'] = self.run_query(query_cve, "CVE to ATT&CK")

        # CWE → ATT&CK
        query_cwe = """
        MATCH p=(cwe:CWE)-[*1..3]-(att)
        WHERE any(label IN labels(att) WHERE label CONTAINS 'Attack')
        RETURN count(DISTINCT p) as paths,
               count(DISTINCT cwe) as cwe_count,
               count(DISTINCT att) as attack_count
        """
        results['cwe_to_attack'] = self.run_query(query_cwe, "CWE to ATT&CK")

        # CAPEC → ATT&CK
        query_capec = """
        MATCH p=(capec:CAPEC)-[*1..2]-(att)
        WHERE any(label IN labels(att) WHERE label CONTAINS 'Attack')
        RETURN count(DISTINCT p) as paths,
               count(DISTINCT capec) as capec_count,
               count(DISTINCT att) as attack_count
        """
        results['capec_to_attack'] = self.run_query(query_capec, "CAPEC to ATT&CK")

        return results

    def analyze_connected_techniques(self):
        """Query 5: ATT&CK technique connectivity"""
        print("📈 Analyzing ATT&CK technique connectivity...")

        query = """
        MATCH (att)
        WHERE any(label IN labels(att) WHERE label CONTAINS 'Attack' AND label CONTAINS 'Technique')
        WITH att, size((att)-[]-()) as connections
        RETURN count(att) as total_techniques,
               sum(CASE WHEN connections = 0 THEN 1 ELSE 0 END) as isolated,
               sum(CASE WHEN connections > 0 THEN 1 ELSE 0 END) as connected,
               avg(toFloat(connections)) as avg_connections,
               max(connections) as max_connections
        """
        return self.run_query(query, "Technique connectivity")

    def get_top_connected_techniques(self):
        """Query 6: Most connected ATT&CK techniques"""
        print("🏆 Finding top connected techniques...")

        query = """
        MATCH (att)
        WHERE any(label IN labels(att) WHERE label CONTAINS 'Attack' AND label CONTAINS 'Technique')
        WITH att, size((att)-[]-()) as connections
        WHERE connections > 0
        RETURN coalesce(att.techniqueId, att.id, att.name, id(att)) as identifier,
               att.name as name,
               connections
        ORDER BY connections DESC
        LIMIT 20
        """
        return self.run_query(query, "Top connected techniques")

    def get_sample_attack_properties(self):
        """Query 7: Sample ATT&CK technique properties"""
        print("🔬 Sampling ATT&CK technique properties...")

        query = """
        MATCH (att)
        WHERE any(label IN labels(att) WHERE label CONTAINS 'Attack' AND label CONTAINS 'Technique')
        RETURN coalesce(att.techniqueId, att.id, att.name) as identifier,
               att.name as name,
               keys(att) as properties
        LIMIT 5
        """
        return self.run_query(query, "Sample properties")

def generate_report(analyzer):
    """Generate comprehensive report"""

    report = []
    report.append("# Neo4j ATT&CK Schema Analysis Report")
    report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"\n**Database:** bolt://localhost:7687")
    report.append("\n---\n")

    # Discover schema
    schema, labels = analyzer.discover_schema()

    report.append("## 1. Database Schema Overview\n")
    report.append(f"**Total Label Types:** {len(labels)}\n")
    report.append("| Label | Count |")
    report.append("|-------|-------|")
    for label in sorted(schema.keys(), key=lambda x: schema[x], reverse=True):
        report.append(f"| {label} | {schema[label]:,} |")

    # ATT&CK nodes
    report.append("\n## 2. ATT&CK Node Coverage\n")
    attack_nodes = analyzer.analyze_attack_nodes(labels)
    if attack_nodes:
        report.append("| Node Type | Count |")
        report.append("|-----------|-------|")
        total_attack = 0
        for node in attack_nodes:
            report.append(f"| {node['type']} | {node['count']:,} |")
            total_attack += node['count']
        report.append(f"\n**Total ATT&CK Nodes:** {total_attack:,}\n")
    else:
        report.append("⚠️ No ATT&CK nodes found in database.\n")

    # All relationships
    report.append("## 3. Database Relationship Patterns\n")
    all_rels = analyzer.analyze_relationships()
    if all_rels:
        report.append("Top relationship patterns in database:\n")
        report.append("| From | Relationship | To | Count |")
        report.append("|------|--------------|-----|-------|")
        for rel in all_rels[:30]:
            report.append(f"| {rel['from_label']} | {rel['relationship_type']} | {rel['to_label']} | {rel['count']:,} |")

    # ATT&CK relationships
    report.append("\n## 4. ATT&CK Relationship Analysis\n")
    attack_rels = analyzer.analyze_attack_relationships()
    if attack_rels:
        report.append("Relationships involving ATT&CK nodes:\n")
        report.append("| From | Relationship | To | Count |")
        report.append("|------|--------------|-----|-------|")
        for rel in attack_rels:
            report.append(f"| {rel['from_label']} | {rel['relationship_type']} | {rel['to_label']} | {rel['count']:,} |")
    else:
        report.append("⚠️ No relationships found involving ATT&CK nodes.\n")

    # Vulnerability → ATT&CK paths
    report.append("\n## 5. Vulnerability → ATT&CK Chain Analysis\n")
    paths = analyzer.analyze_vulnerability_to_attack_paths()

    for path_type, results in paths.items():
        if results and results[0].get('paths', 0) > 0:
            r = results[0]
            report.append(f"### {path_type.upper().replace('_', ' ')}")
            report.append(f"- **Paths:** {r['paths']:,}")
            report.append(f"- **Source Nodes:** {r.get(path_type.split('_')[0] + '_count', 0):,}")
            report.append(f"- **ATT&CK Nodes Reached:** {r.get('attack_count', 0):,}\n")
        else:
            report.append(f"### {path_type.upper().replace('_', ' ')}")
            report.append("- ❌ No paths found\n")

    # Connectivity metrics
    report.append("## 6. ATT&CK Technique Connectivity Metrics\n")
    connectivity = analyzer.analyze_connected_techniques()
    if connectivity:
        c = connectivity[0]
        total = c.get('total_techniques', 0)
        isolated = c.get('isolated', 0)
        connected = c.get('connected', 0)

        report.append(f"- **Total ATT&CK Techniques:** {total:,}")
        report.append(f"- **Connected Techniques:** {connected:,}")
        report.append(f"- **Isolated Techniques:** {isolated:,}")
        if total > 0:
            coverage = (connected / total * 100)
            report.append(f"- **Coverage:** {coverage:.1f}%")
        report.append(f"- **Average Connections:** {c.get('avg_connections', 0):.1f}")
        report.append(f"- **Max Connections:** {c.get('max_connections', 0)}\n")

    # Top connected
    report.append("## 7. Top Connected ATT&CK Techniques\n")
    top_connected = analyzer.get_top_connected_techniques()
    if top_connected:
        report.append("| Identifier | Name | Connections |")
        report.append("|------------|------|-------------|")
        for tech in top_connected:
            name = tech.get('name', 'N/A')
            report.append(f"| {tech['identifier']} | {name} | {tech['connections']} |")

    # Sample properties
    report.append("\n## 8. ATT&CK Technique Property Sample\n")
    samples = analyzer.get_sample_attack_properties()
    if samples:
        for sample in samples:
            report.append(f"### {sample.get('identifier', 'N/A')}")
            report.append(f"**Name:** {sample.get('name', 'N/A')}")
            report.append(f"**Properties:** {', '.join(sample.get('properties', []))}\n")

    # Assessment
    report.append("## 9. Gap Analysis & Recommendations\n")

    report.append("### Current State:\n")
    has_attack = len([l for l in labels if 'Attack' in l]) > 0
    has_cve = 'CVE' in labels
    has_cwe = 'CWE' in labels
    has_capec = 'CAPEC' in labels

    report.append(f"- {'✅' if has_attack else '❌'} ATT&CK nodes present")
    report.append(f"- {'✅' if has_cve else '❌'} CVE nodes present")
    report.append(f"- {'✅' if has_cwe else '❌'} CWE nodes present")
    report.append(f"- {'✅' if has_capec else '❌'} CAPEC nodes present")

    # Check connectivity
    if attack_rels and len(attack_rels) > 0:
        report.append("- ✅ ATT&CK nodes have relationships")
    else:
        report.append("- ❌ ATT&CK nodes are isolated")

    if paths and any(p and p[0].get('paths', 0) > 0 for p in paths.values()):
        report.append("- ✅ Vulnerability → ATT&CK paths exist")
    else:
        report.append("- ❌ No vulnerability → ATT&CK paths found")

    report.append("\n### Required for Complete Attack Chains:\n")
    report.append("1. **CVE → CWE → CAPEC → ATT&CK** chain")
    report.append("2. **ATT&CK internal hierarchy:** Tactics → Techniques → Sub-techniques")
    report.append("3. **ATT&CK entity relationships:** Groups ← use → Techniques, Software ← use → Techniques")
    report.append("4. **Temporal properties:** Dates, versions, threat intel timestamps")
    report.append("5. **Bidirectional navigation:** All paths should be queryable in both directions")

    report.append("\n### Recommended Next Steps:\n")
    if not paths or not any(p and p[0].get('paths', 0) > 0 for p in paths.values() if p):
        report.append("1. **CRITICAL:** Establish CVE/CWE/CAPEC → ATT&CK relationships")
    if connectivity and connectivity[0].get('isolated', 0) > 0:
        report.append("2. **HIGH:** Connect isolated ATT&CK techniques to relevant entities")
    report.append("3. Validate relationship semantics and cardinality constraints")
    report.append("4. Add metadata: confidence scores, data sources, timestamps")
    report.append("5. Implement graph algorithms: shortest paths, PageRank, community detection")

    report.append("\n---")
    report.append(f"\n*Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    return "\n".join(report)

def main():
    print("=" * 80)
    print("Neo4j ATT&CK Schema Analysis")
    print("=" * 80)

    analyzer = None
    try:
        analyzer = Neo4jAttackAnalyzer(URI, AUTH)

        report = generate_report(analyzer)

        output_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/docs/NEO4J_ATTACK_SCHEMA_ANALYSIS.md"

        with open(output_file, 'w') as f:
            f.write(report)

        print("\n" + "=" * 80)
        print(f"✅ Analysis complete! Report saved to:")
        print(f"   {output_file}")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if analyzer:
            analyzer.close()

if __name__ == "__main__":
    main()
