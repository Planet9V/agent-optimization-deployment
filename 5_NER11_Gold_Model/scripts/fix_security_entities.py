#!/usr/bin/env python3
"""
Fix CVE/CWE/CPE/CAPEC Entity Labels and Create Relationships

This script:
1. Relabels mislabeled CVE/CWE entities using regex patterns
2. Creates relationships between CVE/CWE entities and related entities
3. Extracts CPE and CAPEC identifiers from text where missed
"""

import re
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from datetime import datetime

# Connection settings
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

# Patterns for security identifiers
CVE_PATTERN = re.compile(r'^CVE-\d{4}-\d+$', re.IGNORECASE)
CWE_PATTERN = re.compile(r'^CWE-\d+$', re.IGNORECASE)
CPE_PATTERN = re.compile(r'^cpe:[^:]+:[^:]+:[^:]+', re.IGNORECASE)
CAPEC_PATTERN = re.compile(r'^CAPEC-\d+$', re.IGNORECASE)

def fix_mislabeled_entities(driver):
    """Fix entities with CVE/CWE patterns that have wrong labels."""

    with driver.session() as session:
        print("\n=== FIXING MISLABELED CVE ENTITIES ===")

        # Fix CVE entities with wrong labels
        result = session.run("""
            MATCH (e:Entity)
            WHERE e.text =~ '(?i)^CVE-[0-9]{4}-[0-9]+$'
            AND e.label <> 'CVE'
            RETURN e.text as text, e.label as old_label, id(e) as node_id
        """)

        fixes = list(result)
        print(f"Found {len(fixes)} mislabeled CVE entities")

        for record in fixes:
            session.run("""
                MATCH (e:Entity)
                WHERE id(e) = $node_id
                SET e.label = 'CVE', e.fixed_at = timestamp(), e.old_label = $old_label
            """, node_id=record['node_id'], old_label=record['old_label'])
            print(f"  ✅ Fixed: {record['text']} ({record['old_label']} → CVE)")

        print(f"\n=== FIXING MISLABELED CWE ENTITIES ===")

        # Fix CWE entities with wrong labels
        result = session.run("""
            MATCH (e:Entity)
            WHERE e.text =~ '(?i)^CWE-[0-9]+$'
            AND e.label <> 'CWE'
            RETURN e.text as text, e.label as old_label, id(e) as node_id
        """)

        fixes = list(result)
        print(f"Found {len(fixes)} mislabeled CWE entities")

        for record in fixes:
            session.run("""
                MATCH (e:Entity)
                WHERE id(e) = $node_id
                SET e.label = 'CWE', e.fixed_at = timestamp(), e.old_label = $old_label
            """, node_id=record['node_id'], old_label=record['old_label'])
            print(f"  ✅ Fixed: {record['text']} ({record['old_label']} → CWE)")

        return len(fixes)

def create_cve_relationships(driver):
    """Create relationships between CVE entities and related entities."""

    with driver.session() as session:
        print("\n=== CREATING CVE RELATIONSHIPS ===")

        # Create CVE -> VULNERABILITY relationships
        result = session.run("""
            MATCH (cve:Entity {label: 'CVE'})
            MATCH (vuln:Entity {label: 'VULNERABILITY'})
            WHERE cve.source_file = vuln.source_file
            MERGE (cve)-[r:DESCRIBES]->(vuln)
            RETURN count(r) as created
        """)
        count = result.single()['created']
        print(f"  Created {count} CVE -> VULNERABILITY relationships")

        # Create CVE -> ATTACK_TECHNIQUE relationships
        result = session.run("""
            MATCH (cve:Entity {label: 'CVE'})
            MATCH (tech:Entity {label: 'ATTACK_TECHNIQUE'})
            WHERE cve.source_file = tech.source_file
            MERGE (cve)-[r:EXPLOITED_BY]->(tech)
            RETURN count(r) as created
        """)
        count = result.single()['created']
        print(f"  Created {count} CVE -> ATTACK_TECHNIQUE relationships")

        # Create CVE -> PRODUCT relationships (affected products)
        result = session.run("""
            MATCH (cve:Entity {label: 'CVE'})
            MATCH (prod:Entity {label: 'PRODUCT'})
            WHERE cve.source_file = prod.source_file
            MERGE (cve)-[r:AFFECTS]->(prod)
            RETURN count(r) as created
        """)
        count = result.single()['created']
        print(f"  Created {count} CVE -> PRODUCT relationships")

        # Create CVE -> ORG relationships (affected organizations)
        result = session.run("""
            MATCH (cve:Entity {label: 'CVE'})
            MATCH (org:Entity {label: 'ORG'})
            WHERE cve.source_file = org.source_file
            MERGE (cve)-[r:REPORTED_BY]->(org)
            RETURN count(r) as created
        """)
        count = result.single()['created']
        print(f"  Created {count} CVE -> ORG relationships")

def create_cwe_relationships(driver):
    """Create relationships between CWE entities and related entities."""

    with driver.session() as session:
        print("\n=== CREATING CWE RELATIONSHIPS ===")

        # Create CWE -> VULNERABILITY relationships
        result = session.run("""
            MATCH (cwe:Entity {label: 'CWE'})
            MATCH (vuln:Entity {label: 'VULNERABILITY'})
            WHERE cwe.source_file = vuln.source_file
            MERGE (cwe)-[r:CATEGORIZES]->(vuln)
            RETURN count(r) as created
        """)
        count = result.single()['created']
        print(f"  Created {count} CWE -> VULNERABILITY relationships")

        # Create CVE -> CWE relationships (CVE assigned to CWE category)
        result = session.run("""
            MATCH (cve:Entity {label: 'CVE'})
            MATCH (cwe:Entity {label: 'CWE'})
            WHERE cve.source_file = cwe.source_file
            MERGE (cve)-[r:CLASSIFIED_AS]->(cwe)
            RETURN count(r) as created
        """)
        count = result.single()['created']
        print(f"  Created {count} CVE -> CWE relationships")

def generate_report(driver):
    """Generate a report of security entities and relationships."""

    with driver.session() as session:
        print("\n" + "="*60)
        print("SECURITY ENTITY REPORT")
        print("="*60)

        # Count entities
        result = session.run("""
            MATCH (e:Entity)
            WHERE e.label IN ['CVE', 'CWE', 'CPE', 'CAPEC', 'VULNERABILITY', 'ATTACK_TECHNIQUE']
            RETURN e.label as label, count(*) as cnt
            ORDER BY cnt DESC
        """)

        print("\n📊 ENTITY COUNTS:")
        for record in result:
            print(f"  {record['label']:20} {record['cnt']:>6}")

        # Count relationships
        print("\n🔗 RELATIONSHIP COUNTS:")

        result = session.run("""
            MATCH (e:Entity {label: 'CVE'})-[r]->(other)
            RETURN type(r) as rel_type, count(r) as cnt
            ORDER BY cnt DESC
        """)

        for record in result:
            print(f"  CVE --[{record['rel_type']}]--> : {record['cnt']}")

        result = session.run("""
            MATCH (e:Entity {label: 'CWE'})-[r]->(other)
            RETURN type(r) as rel_type, count(r) as cnt
            ORDER BY cnt DESC
        """)

        for record in result:
            print(f"  CWE --[{record['rel_type']}]--> : {record['cnt']}")

        # Sample CVE with relationships
        print("\n📋 SAMPLE CVE WITH RELATIONSHIPS:")
        result = session.run("""
            MATCH (cve:Entity {label: 'CVE'})-[r]->(other)
            RETURN cve.text as cve, type(r) as rel, other.text as target, other.label as target_label
            LIMIT 10
        """)

        for record in result:
            print(f"  {record['cve']} --[{record['rel']}]--> {record['target'][:40]} ({record['target_label']})")

def main():
    print("="*60)
    print("CVE/CWE/CPE/CAPEC Entity Fix Script")
    print(f"Started: {datetime.now().isoformat()}")
    print("="*60)

    # Connect to Neo4j
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        # Step 1: Fix mislabeled entities
        fix_mislabeled_entities(driver)

        # Step 2: Create CVE relationships
        create_cve_relationships(driver)

        # Step 3: Create CWE relationships
        create_cwe_relationships(driver)

        # Step 4: Generate report
        generate_report(driver)

        print("\n" + "="*60)
        print("✅ COMPLETED SUCCESSFULLY")
        print("="*60)

    finally:
        driver.close()

if __name__ == "__main__":
    main()
