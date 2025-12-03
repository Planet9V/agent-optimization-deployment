#!/usr/bin/env python3
"""
Link NER11 Entity Nodes to Structured Security Taxonomy

This script creates bridge relationships between:
- Entity nodes (from NER11 extraction) → CVE nodes (structured taxonomy)
- Entity nodes → CWE nodes (weakness taxonomy)
- Entity nodes → CAPEC nodes (attack pattern taxonomy)
- Entity nodes → AttackPattern nodes (ICS threat intel)

Relationship types:
- REFERENCES: Entity mentions a CVE/CWE/CAPEC in document context
- INSTANCE_OF: Entity is an instance of the structured taxonomy node
"""

import re
from neo4j import GraphDatabase
from datetime import datetime

# Connection settings
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# Patterns for security identifiers
CVE_PATTERN = re.compile(r'^CVE-\d{4}-\d+$', re.IGNORECASE)
CWE_PATTERN = re.compile(r'^CWE-\d+$', re.IGNORECASE)
CAPEC_PATTERN = re.compile(r'^CAPEC-\d+$', re.IGNORECASE)


def link_entity_cves_to_taxonomy(driver):
    """Link Entity nodes with CVE text to structured CVE nodes."""

    with driver.session() as session:
        print("\n=== LINKING ENTITY CVEs TO TAXONOMY ===")

        # Find Entity nodes with CVE pattern and link to CVE taxonomy
        result = session.run("""
            MATCH (e:Entity)
            WHERE e.text =~ '(?i)^CVE-[0-9]{4}-[0-9]+$'
            WITH e, toUpper(e.text) as cve_id
            MATCH (cve:CVE {id: cve_id})
            MERGE (e)-[r:REFERENCES]->(cve)
            ON CREATE SET r.created_at = timestamp(), r.link_type = 'entity_to_taxonomy'
            RETURN count(r) as links_created
        """)

        created = result.single()['links_created']
        print(f"  ✅ Created {created} Entity → CVE REFERENCES relationships")

        # Also create INSTANCE_OF for exact matches
        result = session.run("""
            MATCH (e:Entity)
            WHERE e.text =~ '(?i)^CVE-[0-9]{4}-[0-9]+$'
            WITH e, toUpper(e.text) as cve_id
            MATCH (cve:CVE {id: cve_id})
            MERGE (e)-[r:INSTANCE_OF]->(cve)
            ON CREATE SET r.created_at = timestamp()
            RETURN count(r) as links_created
        """)

        created = result.single()['links_created']
        print(f"  ✅ Created {created} Entity → CVE INSTANCE_OF relationships")

        return created


def link_entity_cwes_to_taxonomy(driver):
    """Link Entity nodes with CWE text to structured CWE nodes."""

    with driver.session() as session:
        print("\n=== LINKING ENTITY CWEs TO TAXONOMY ===")

        # CWE IDs are stored as lowercase in taxonomy (cwe-79)
        result = session.run("""
            MATCH (e:Entity)
            WHERE e.text =~ '(?i)^CWE-[0-9]+$'
            WITH e, toLower(e.text) as cwe_id
            MATCH (cwe:CWE)
            WHERE cwe.id = cwe_id OR toLower(cwe.id) = cwe_id
            MERGE (e)-[r:REFERENCES]->(cwe)
            ON CREATE SET r.created_at = timestamp(), r.link_type = 'entity_to_taxonomy'
            RETURN count(r) as links_created
        """)

        created = result.single()['links_created']
        print(f"  ✅ Created {created} Entity → CWE REFERENCES relationships")

        result = session.run("""
            MATCH (e:Entity)
            WHERE e.text =~ '(?i)^CWE-[0-9]+$'
            WITH e, toLower(e.text) as cwe_id
            MATCH (cwe:CWE)
            WHERE cwe.id = cwe_id OR toLower(cwe.id) = cwe_id
            MERGE (e)-[r:INSTANCE_OF]->(cwe)
            ON CREATE SET r.created_at = timestamp()
            RETURN count(r) as links_created
        """)

        created = result.single()['links_created']
        print(f"  ✅ Created {created} Entity → CWE INSTANCE_OF relationships")

        return created


def link_entity_capecs_to_taxonomy(driver):
    """Link Entity nodes with CAPEC text to structured CAPEC nodes."""

    with driver.session() as session:
        print("\n=== LINKING ENTITY CAPECs TO TAXONOMY ===")

        result = session.run("""
            MATCH (e:Entity)
            WHERE e.text =~ '(?i)^CAPEC-[0-9]+$'
            WITH e, toUpper(e.text) as capec_id
            MATCH (capec:CAPEC)
            WHERE capec.id = capec_id OR toUpper(capec.id) = capec_id
            MERGE (e)-[r:REFERENCES]->(capec)
            ON CREATE SET r.created_at = timestamp(), r.link_type = 'entity_to_taxonomy'
            RETURN count(r) as links_created
        """)

        created = result.single()['links_created']
        print(f"  ✅ Created {created} Entity → CAPEC REFERENCES relationships")

        return created


def link_entity_attack_techniques(driver):
    """Link Entity attack technique mentions to AttackPattern nodes."""

    with driver.session() as session:
        print("\n=== LINKING ATTACK TECHNIQUES ===")

        # Link by MITRE ATT&CK ID pattern (T1234, T1234.001)
        result = session.run("""
            MATCH (e:Entity)
            WHERE e.label IN ['ATTACK_TECHNIQUE', 'TTP', 'ATT_CK_Technique']
            AND e.text =~ '(?i)^T[0-9]{4}(\\.[0-9]+)?$'
            WITH e, e.text as technique_id
            MATCH (ap:AttackPattern)
            WHERE ap.id = technique_id OR ap.technique_id = technique_id
            MERGE (e)-[r:REFERENCES]->(ap)
            ON CREATE SET r.created_at = timestamp()
            RETURN count(r) as links_created
        """)

        created = result.single()['links_created']
        print(f"  ✅ Created {created} Entity → AttackPattern REFERENCES relationships")

        return created


def link_vulnerability_entities_to_cves(driver):
    """Link VULNERABILITY Entity nodes to CVE nodes mentioned in same document."""

    with driver.session() as session:
        print("\n=== LINKING VULNERABILITIES TO CVEs ===")

        # Link vulnerabilities to CVEs from same source document
        result = session.run("""
            MATCH (vuln:Entity {label: 'VULNERABILITY'})
            MATCH (cve_entity:Entity)
            WHERE cve_entity.text =~ '(?i)^CVE-[0-9]{4}-[0-9]+$'
            AND cve_entity.source_file = vuln.source_file
            WITH vuln, cve_entity, toUpper(cve_entity.text) as cve_id
            MATCH (cve:CVE {id: cve_id})
            MERGE (vuln)-[r:DESCRIBED_BY]->(cve)
            ON CREATE SET r.created_at = timestamp()
            RETURN count(r) as links_created
        """)

        created = result.single()['links_created']
        print(f"  ✅ Created {created} Vulnerability → CVE DESCRIBED_BY relationships")

        return created


def link_threat_actors_to_cves(driver):
    """Link THREAT_ACTOR entities to CVEs they exploit (same document context)."""

    with driver.session() as session:
        print("\n=== LINKING THREAT ACTORS TO CVEs ===")

        result = session.run("""
            MATCH (actor:Entity {label: 'THREAT_ACTOR'})
            MATCH (cve_entity:Entity)
            WHERE cve_entity.text =~ '(?i)^CVE-[0-9]{4}-[0-9]+$'
            AND cve_entity.source_file = actor.source_file
            WITH actor, cve_entity, toUpper(cve_entity.text) as cve_id
            MATCH (cve:CVE {id: cve_id})
            MERGE (actor)-[r:EXPLOITS_CVE]->(cve)
            ON CREATE SET r.created_at = timestamp(), r.context = 'document_co_occurrence'
            RETURN count(r) as links_created
        """)

        created = result.single()['links_created']
        print(f"  ✅ Created {created} ThreatActor → CVE EXPLOITS_CVE relationships")

        return created


def link_malware_to_cves(driver):
    """Link MALWARE entities to CVEs they exploit (same document context)."""

    with driver.session() as session:
        print("\n=== LINKING MALWARE TO CVEs ===")

        result = session.run("""
            MATCH (malware:Entity {label: 'MALWARE'})
            MATCH (cve_entity:Entity)
            WHERE cve_entity.text =~ '(?i)^CVE-[0-9]{4}-[0-9]+$'
            AND cve_entity.source_file = malware.source_file
            WITH malware, cve_entity, toUpper(cve_entity.text) as cve_id
            MATCH (cve:CVE {id: cve_id})
            MERGE (malware)-[r:EXPLOITS_CVE]->(cve)
            ON CREATE SET r.created_at = timestamp(), r.context = 'document_co_occurrence'
            RETURN count(r) as links_created
        """)

        created = result.single()['links_created']
        print(f"  ✅ Created {created} Malware → CVE EXPLOITS_CVE relationships")

        return created


def generate_link_report(driver):
    """Generate report of Entity → Taxonomy links."""

    with driver.session() as session:
        print("\n" + "="*60)
        print("ENTITY → TAXONOMY LINK REPORT")
        print("="*60)

        # Count links by type
        result = session.run("""
            MATCH (e:Entity)-[r]->(target)
            WHERE target:CVE OR target:CWE OR target:CAPEC OR target:AttackPattern
            RETURN type(r) as rel_type, labels(target)[0] as target_type, count(r) as count
            ORDER BY count DESC
        """)

        print("\n📊 ENTITY → TAXONOMY RELATIONSHIPS:")
        total = 0
        for record in result:
            print(f"  Entity --[{record['rel_type']}]--> {record['target_type']}: {record['count']}")
            total += record['count']

        print(f"\n  TOTAL: {total} cross-domain links")

        # Sample linked entities
        print("\n📋 SAMPLE LINKED ENTITIES:")
        result = session.run("""
            MATCH (e:Entity)-[r:REFERENCES]->(cve:CVE)
            RETURN e.text as entity, e.source_file as source, cve.id as cve_id,
                   cve.epss_score as epss, cve.priority_tier as tier
            LIMIT 5
        """)

        for record in result:
            print(f"  {record['entity']} → {record['cve_id']} (EPSS: {record['epss']}, Tier: {record['tier']})")


def main():
    print("="*60)
    print("Entity → Taxonomy Link Script")
    print(f"Started: {datetime.now().isoformat()}")
    print("="*60)

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        # Link Entity CVEs to CVE taxonomy
        link_entity_cves_to_taxonomy(driver)

        # Link Entity CWEs to CWE taxonomy
        link_entity_cwes_to_taxonomy(driver)

        # Link Entity CAPECs to CAPEC taxonomy
        link_entity_capecs_to_taxonomy(driver)

        # Link attack techniques
        link_entity_attack_techniques(driver)

        # Link vulnerabilities to CVEs
        link_vulnerability_entities_to_cves(driver)

        # Link threat actors to CVEs
        link_threat_actors_to_cves(driver)

        # Link malware to CVEs
        link_malware_to_cves(driver)

        # Generate report
        generate_link_report(driver)

        print("\n" + "="*60)
        print("✅ ENTITY → TAXONOMY LINKING COMPLETE")
        print("="*60)

    finally:
        driver.close()


if __name__ == "__main__":
    main()
