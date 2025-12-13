#!/usr/bin/env python3
"""
Create Neo4j Schema - Constraints and Indexes
Execute ACTUAL schema creation in the real AEON Digital Twin database
"""

import os
import sys
from pathlib import Path
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Neo4j connection details
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD]):
    print("ERROR: Missing Neo4j credentials in .env file")
    sys.exit(1)

# Schema creation queries
CONSTRAINTS = [
    "CREATE CONSTRAINT threat_actor_name IF NOT EXISTS FOR (ta:ThreatActor) REQUIRE ta.name IS UNIQUE",
    "CREATE CONSTRAINT campaign_name IF NOT EXISTS FOR (c:Campaign) REQUIRE c.name IS UNIQUE",
    "CREATE CONSTRAINT ioc_value_type IF NOT EXISTS FOR (ioc:IoC) REQUIRE (ioc.value, ioc.type) IS UNIQUE",
    "CREATE CONSTRAINT malware_name IF NOT EXISTS FOR (m:Malware) REQUIRE m.name IS UNIQUE",
    "CREATE CONSTRAINT vulnerability_id IF NOT EXISTS FOR (v:Vulnerability) REQUIRE v.cve_id IS UNIQUE"
]

INDEXES = [
    "CREATE INDEX ioc_type IF NOT EXISTS FOR (ioc:IoC) ON (ioc.type)",
    "CREATE INDEX ioc_confidence IF NOT EXISTS FOR (ioc:IoC) ON (ioc.confidence)",
    "CREATE INDEX threat_actor_confidence IF NOT EXISTS FOR (ta:ThreatActor) ON (ta.confidence)",
    "CREATE INDEX campaign_timeframe IF NOT EXISTS FOR (c:Campaign) ON (c.timeframe)"
]

VERIFICATION_QUERIES = [
    ("Sectors", "MATCH (s:Sector) RETURN COUNT(s) AS count"),
    ("CVEs", "MATCH (cve:CVE) RETURN COUNT(cve) AS count"),
    ("MITRE Techniques", "MATCH (mt:MITRETechnique) RETURN COUNT(mt) AS count"),
    ("Threat Actors", "MATCH (ta:ThreatActor) RETURN COUNT(ta) AS count"),
    ("Campaigns", "MATCH (c:Campaign) RETURN COUNT(c) AS count"),
    ("IoCs", "MATCH (ioc:IoC) RETURN COUNT(ioc) AS count"),
    ("Malware", "MATCH (m:Malware) RETURN COUNT(m) AS count"),
    ("Vulnerabilities", "MATCH (v:Vulnerability) RETURN COUNT(v) AS count")
]

def create_schema():
    """Create constraints and indexes in Neo4j database"""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    results = {
        'constraints_created': [],
        'constraints_failed': [],
        'indexes_created': [],
        'indexes_failed': [],
        'verification': {}
    }

    try:
        with driver.session() as session:
            # Create constraints
            print("\n=== Creating Constraints ===")
            for constraint in CONSTRAINTS:
                try:
                    session.run(constraint)
                    constraint_name = constraint.split()[2]  # Extract constraint name
                    results['constraints_created'].append(constraint_name)
                    print(f"✅ Created constraint: {constraint_name}")
                except Exception as e:
                    results['constraints_failed'].append((constraint, str(e)))
                    print(f"❌ Failed constraint: {str(e)}")

            # Create indexes
            print("\n=== Creating Indexes ===")
            for index in INDEXES:
                try:
                    session.run(index)
                    index_name = index.split()[2]  # Extract index name
                    results['indexes_created'].append(index_name)
                    print(f"✅ Created index: {index_name}")
                except Exception as e:
                    results['indexes_failed'].append((index, str(e)))
                    print(f"❌ Failed index: {str(e)}")

            # Verify existing nodes
            print("\n=== Verifying Existing Nodes ===")
            for label, query in VERIFICATION_QUERIES:
                try:
                    result = session.run(query)
                    count = result.single()['count']
                    results['verification'][label] = count
                    print(f"📊 {label}: {count:,} nodes")
                except Exception as e:
                    results['verification'][label] = f"ERROR: {str(e)}"
                    print(f"❌ Failed to verify {label}: {str(e)}")

            # Show all constraints
            print("\n=== All Constraints in Database ===")
            constraint_result = session.run("SHOW CONSTRAINTS")
            for record in constraint_result:
                print(f"  - {record['name']}: {record['type']} on {record['labelsOrTypes']}")

            # Show all indexes
            print("\n=== All Indexes in Database ===")
            index_result = session.run("SHOW INDEXES")
            for record in index_result:
                print(f"  - {record['name']}: {record['type']} on {record['labelsOrTypes']}")

    finally:
        driver.close()

    return results

def generate_report(results):
    """Generate validation report"""
    report_lines = [
        "# Neo4j Schema Validation Report",
        f"Database: {NEO4J_URI}",
        "",
        "## Constraints Created",
        ""
    ]

    if results['constraints_created']:
        for constraint in results['constraints_created']:
            report_lines.append(f"✅ {constraint}")
    else:
        report_lines.append("(none)")

    if results['constraints_failed']:
        report_lines.append("\n## Constraints Failed\n")
        for constraint, error in results['constraints_failed']:
            report_lines.append(f"❌ {constraint}")
            report_lines.append(f"   Error: {error}")

    report_lines.extend([
        "",
        "## Indexes Created",
        ""
    ])

    if results['indexes_created']:
        for index in results['indexes_created']:
            report_lines.append(f"✅ {index}")
    else:
        report_lines.append("(none)")

    if results['indexes_failed']:
        report_lines.append("\n## Indexes Failed\n")
        for index, error in results['indexes_failed']:
            report_lines.append(f"❌ {index}")
            report_lines.append(f"   Error: {error}")

    report_lines.extend([
        "",
        "## Node Verification",
        ""
    ])

    for label, count in results['verification'].items():
        if isinstance(count, int):
            report_lines.append(f"📊 {label}: {count:,} nodes")
        else:
            report_lines.append(f"❌ {label}: {count}")

    report_lines.extend([
        "",
        "## Summary",
        f"- Constraints created: {len(results['constraints_created'])}/{len(CONSTRAINTS)}",
        f"- Indexes created: {len(results['indexes_created'])}/{len(INDEXES)}",
        f"- Database ready for APT data ingestion: {'✅ YES' if not results['constraints_failed'] and not results['indexes_failed'] else '⚠️  WITH WARNINGS'}"
    ])

    return "\n".join(report_lines)

if __name__ == "__main__":
    print("=" * 60)
    print("Neo4j Schema Creation - AEON Digital Twin")
    print("=" * 60)

    # Create schema
    results = create_schema()

    # Generate report
    report = generate_report(results)

    # Save report
    output_dir = Path(__file__).parent.parent / 'docs' / 'e01_apt_ingestion'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'schema_validation_report.txt'

    with open(output_file, 'w') as f:
        f.write(report)

    print(f"\n📄 Report saved to: {output_file}")
    print("\n" + "=" * 60)
    print("Schema creation COMPLETE")
    print("=" * 60)
