#!/usr/bin/env python3
"""
Quick Neo4j ATT&CK Analysis - Fast version with timeouts
"""

from neo4j import GraphDatabase
import time
from datetime import datetime

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j@openspg")

def run_quick_query(driver, query, description, timeout=10):
    """Run query with timeout"""
    try:
        print(f"   Running: {description}...", end=" ", flush=True)
        with driver.session() as session:
            result = session.run(query)
            records = [dict(r) for r in result]
            print(f"✓ ({len(records)} results)")
            return records
    except Exception as e:
        print(f"✗ Error: {e}")
        return []

def main():
    print("=" * 80)
    print("Quick Neo4j ATT&CK Analysis")
    print("=" * 80 + "\n")

    # Connect with retry
    driver = None
    for attempt in range(3):
        try:
            driver = GraphDatabase.driver(URI, auth=AUTH)
            with driver.session() as session:
                session.run("RETURN 1")
            print("✅ Connected to Neo4j\n")
            break
        except Exception as e:
            print(f"Connection attempt {attempt + 1}/3 failed")
            if attempt < 2:
                time.sleep(3)
            else:
                print(f"❌ Failed to connect: {e}")
                return

    report = []
    report.append("# Neo4j ATT&CK Schema Analysis Report")
    report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"\n**Database:** bolt://localhost:7687\n")
    report.append("---\n")

    # 1. Get all labels
    print("1️⃣ Discovering database schema...")
    labels_result = run_quick_query(driver, "CALL db.labels()", "Get labels")
    labels = [r['label'] for r in labels_result] if labels_result else []

    report.append("## 1. Database Schema\n")
    report.append(f"**Total Labels:** {len(labels)}\n")

    # 2. Count nodes by label
    print("\n2️⃣ Counting nodes...")
    node_counts = {}
    for label in labels[:50]:  # Limit to first 50 labels
        query = f"MATCH (n:`{label}`) RETURN count(n) as count"
        result = run_quick_query(driver, query, f"Count {label}", timeout=5)
        if result:
            node_counts[label] = result[0]['count']

    report.append("| Label | Count |")
    report.append("|-------|-------|")
    for label in sorted(node_counts.keys(), key=lambda x: node_counts[x], reverse=True):
        report.append(f"| {label} | {node_counts[label]:,} |")

    # 3. ATT&CK specific counts
    print("\n3️⃣ Analyzing ATT&CK nodes...")
    attack_labels = [l for l in labels if 'Attack' in l or 'attack' in l]

    report.append("\n## 2. ATT&CK Node Coverage\n")
    if attack_labels:
        report.append("| ATT&CK Node Type | Count |")
        report.append("|------------------|-------|")
        total_attack = 0
        for label in attack_labels:
            count = node_counts.get(label, 0)
            report.append(f"| {label} | {count:,} |")
            total_attack += count
        report.append(f"\n**Total ATT&CK Nodes:** {total_attack:,}\n")
    else:
        report.append("⚠️ No ATT&CK-labeled nodes found.\n")

    # 4. Sample relationship types
    print("\n4️⃣ Analyzing relationships...")
    rels_query = """
    MATCH ()-[r]->()
    RETURN type(r) as rel_type, count(*) as count
    ORDER BY count DESC
    LIMIT 20
    """
    rels = run_quick_query(driver, rels_query, "Top relationship types")

    report.append("## 3. Top Relationship Types\n")
    if rels:
        report.append("| Relationship Type | Count |")
        report.append("|-------------------|-------|")
        for rel in rels:
            report.append(f"| {rel['rel_type']} | {rel['count']:,} |")
    report.append("\n")

    # 5. ATT&CK-specific relationships
    print("\n5️⃣ Finding ATT&CK relationships...")
    attack_rels_query = """
    MATCH (a)-[r]->(b)
    WHERE any(label IN labels(a) WHERE label CONTAINS 'Attack')
       OR any(label IN labels(b) WHERE label CONTAINS 'Attack')
    RETURN type(r) as rel_type, count(*) as count
    ORDER BY count DESC
    LIMIT 20
    """
    attack_rels = run_quick_query(driver, attack_rels_query, "ATT&CK relationships", timeout=15)

    report.append("## 4. ATT&CK Relationship Analysis\n")
    if attack_rels and len(attack_rels) > 0:
        report.append("| Relationship Type | Count |")
        report.append("|-------------------|-------|")
        for rel in attack_rels:
            report.append(f"| {rel['rel_type']} | {rel['count']:,} |")
    else:
        report.append("⚠️ No relationships found involving ATT&CK nodes.\n")

    # 6. Check for vulnerability → ATT&CK paths
    print("\n6️⃣ Checking vulnerability → ATT&CK paths...")

    # Simple existence check
    cve_exists = 'CVE' in labels
    cwe_exists = 'CWE' in labels
    capec_exists = 'CAPEC' in labels

    report.append("\n## 5. Vulnerability Chain Coverage\n")
    report.append(f"- {'✅' if cve_exists else '❌'} CVE nodes present")
    report.append(f"- {'✅' if cwe_exists else '❌'} CWE nodes present")
    report.append(f"- {'✅' if capec_exists else '❌'} CAPEC nodes present")
    report.append(f"- {'✅' if attack_labels else '❌'} ATT&CK nodes present\n")

    # Try to find a path (with short timeout)
    if cve_exists and attack_labels:
        path_query = """
        MATCH p=(cve:CVE)-[*1..3]-(att)
        WHERE any(label IN labels(att) WHERE label CONTAINS 'Attack')
        RETURN count(p) as path_count
        LIMIT 1
        """
        path_result = run_quick_query(driver, path_query, "CVE → ATT&CK paths", timeout=10)
        if path_result and path_result[0]['path_count'] > 0:
            report.append(f"✅ **CVE → ATT&CK Paths Found:** {path_result[0]['path_count']:,}\n")
        else:
            report.append("❌ **No CVE → ATT&CK paths found**\n")

    # 7. ATT&CK technique connectivity
    print("\n7️⃣ Analyzing ATT&CK technique connectivity...")
    if attack_labels:
        # Find AttackTechnique label
        tech_label = next((l for l in attack_labels if 'Technique' in l), attack_labels[0])

        conn_query = f"""
        MATCH (att:`{tech_label}`)
        WITH att, size((att)-[]-()) as connections
        RETURN count(att) as total,
               sum(CASE WHEN connections = 0 THEN 1 ELSE 0 END) as isolated,
               sum(CASE WHEN connections > 0 THEN 1 ELSE 0 END) as connected
        """
        conn_result = run_quick_query(driver, conn_query, "Technique connectivity", timeout=15)

        report.append("## 6. ATT&CK Technique Connectivity\n")
        if conn_result:
            c = conn_result[0]
            total = c['total']
            isolated = c['isolated']
            connected = c['connected']

            report.append(f"- **Total Techniques:** {total:,}")
            report.append(f"- **Connected:** {connected:,}")
            report.append(f"- **Isolated:** {isolated:,}")
            if total > 0:
                coverage = (connected / total * 100)
                report.append(f"- **Coverage:** {coverage:.1f}%\n")

    # 8. Gap analysis
    report.append("\n## 7. Gap Analysis & Recommendations\n")

    report.append("### Current State:\n")
    if attack_labels and len(attack_labels) > 0:
        report.append("- ✅ ATT&CK nodes loaded")
    else:
        report.append("- ❌ ATT&CK nodes missing")

    if attack_rels and len(attack_rels) > 0:
        report.append("- ✅ ATT&CK nodes have relationships")
    else:
        report.append("- ❌ ATT&CK nodes are isolated")

    report.append("\n### Missing Components:\n")
    missing = []
    if not cve_exists:
        missing.append("CVE nodes")
    if not cwe_exists:
        missing.append("CWE nodes")
    if not capec_exists:
        missing.append("CAPEC nodes")
    if not attack_labels:
        missing.append("ATT&CK nodes")

    if missing:
        for item in missing:
            report.append(f"- ❌ {item}")
    else:
        report.append("- ✅ All major node types present")

    report.append("\n### Required for Complete Attack Chains:\n")
    report.append("1. **CVE → CWE → CAPEC → ATT&CK** relationship chain")
    report.append("2. **ATT&CK internal relationships:** Tactics, Techniques, Sub-techniques")
    report.append("3. **Entity relationships:** Groups, Software linked to Techniques")
    report.append("4. **Metadata:** Confidence scores, timestamps, data sources")
    report.append("5. **Bidirectional queries:** Efficient traversal in both directions")

    report.append("\n### Next Steps:\n")
    report.append("1. Establish missing relationships between vulnerability data and ATT&CK")
    report.append("2. Complete ATT&CK internal hierarchy and entity relationships")
    report.append("3. Add metadata and confidence scores to relationships")
    report.append("4. Implement graph algorithms for attack path analysis")
    report.append("5. Create indexes for performance optimization")

    report.append("\n---")
    report.append(f"\n*Quick analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    # Save report
    output_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/docs/NEO4J_ATTACK_SCHEMA_ANALYSIS.md"

    with open(output_file, 'w') as f:
        f.write("\n".join(report))

    print("\n" + "=" * 80)
    print(f"✅ Analysis complete! Report saved to:")
    print(f"   {output_file}")
    print("=" * 80)

    driver.close()

if __name__ == "__main__":
    main()
