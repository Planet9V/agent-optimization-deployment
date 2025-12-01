#!/usr/bin/env python3
"""
Create CWE→CAPEC→ATT&CK relationships from CAPEC v3.9 XML catalog
"""

import xml.etree.ElementTree as ET
from neo4j import GraphDatabase
import sys
from collections import defaultdict

# Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

class CAPECRelationshipCreator:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            'cwe_capec_created': 0,
            'capec_attack_created': 0,
            'cwe_not_found': set(),
            'attack_not_found': set(),
            'complete_chains': 0
        }

    def close(self):
        self.driver.close()

    def parse_capec_xml(self, xml_file):
        """Parse CAPEC XML and extract relationships"""
        print(f"Parsing {xml_file}...")
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Define namespace
        ns = {'capec': 'http://capec.mitre.org/capec-3'}

        cwe_relationships = []
        attack_relationships = []

        # Find all Attack_Pattern elements
        for pattern in root.findall('.//capec:Attack_Pattern', ns):
            capec_id = pattern.get('ID')
            if not capec_id:
                continue

            # Extract CWE relationships
            related_weaknesses = pattern.find('.//capec:Related_Weaknesses', ns)
            if related_weaknesses is not None:
                for weakness in related_weaknesses.findall('.//capec:Related_Weakness', ns):
                    cwe_id = weakness.get('CWE_ID')
                    if cwe_id:
                        cwe_relationships.append({
                            'cwe_id': cwe_id,  # Store as number without "CWE-" prefix
                            'capec_id': f"CAPEC-{capec_id}"
                        })

            # Extract ATT&CK relationships
            taxonomy_mappings = pattern.find('.//capec:Taxonomy_Mappings', ns)
            if taxonomy_mappings is not None:
                for mapping in taxonomy_mappings.findall('.//capec:Taxonomy_Mapping', ns):
                    taxonomy_name = mapping.get('Taxonomy_Name')
                    if taxonomy_name == 'ATTACK':
                        # Find Entry_ID which contains the technique ID
                        for entry in mapping.findall('.//capec:Entry_ID', ns):
                            technique_id = entry.text
                            if technique_id:
                                # Add "T" prefix if not present
                                if not technique_id.startswith('T'):
                                    technique_id = f"T{technique_id}"
                                attack_relationships.append({
                                    'capec_id': f"CAPEC-{capec_id}",
                                    'technique_id': technique_id
                                })

        print(f"Found {len(cwe_relationships)} CWE→CAPEC relationships")
        print(f"Found {len(attack_relationships)} CAPEC→ATT&CK relationships")

        return cwe_relationships, attack_relationships

    def create_cwe_capec_relationships(self, relationships):
        """Create CWE→CAPEC relationships in Neo4j"""
        print("\nCreating CWE→CAPEC relationships...")

        # Convert relationships to use number property
        number_rels = []
        for rel in relationships:
            number_rels.append({
                'number': int(rel['cwe_id']),  # Convert to integer
                'capec_id': rel['capec_id']
            })

        query = """
        UNWIND $rels AS rel
        MATCH (cwe:CWE {number: rel.number})
        MATCH (capec:CAPEC {capecId: rel.capec_id})
        MERGE (cwe)-[:ENABLES_ATTACK_PATTERN]->(capec)
        RETURN count(*) as created
        """

        with self.driver.session() as session:
            result = session.run(query, rels=number_rels)
            record = result.single()
            created = record['created'] if record else 0
            self.stats['cwe_capec_created'] = created
            print(f"Created {created} CWE→CAPEC relationships")

            # Check for missing CWEs
            missing_query = """
            UNWIND $rels AS rel
            OPTIONAL MATCH (cwe:CWE {number: rel.number})
            WITH rel, cwe
            WHERE cwe IS NULL
            RETURN DISTINCT rel.number as missing_cwe
            """
            result = session.run(missing_query, rels=number_rels)
            missing = [r['missing_cwe'] for r in result]
            self.stats['cwe_not_found'].update([str(x) for x in missing])
            if missing:
                print(f"Warning: {len(missing)} CWE IDs not found in database")

    def create_capec_attack_relationships(self, relationships):
        """Create CAPEC→ATT&CK relationships in Neo4j"""
        print("\nCreating CAPEC→ATT&CK relationships...")

        query = """
        UNWIND $rels AS rel
        MATCH (capec:CAPEC {capecId: rel.capec_id})
        MATCH (tech:AttackTechnique {techniqueId: rel.technique_id})
        MERGE (capec)-[:USES_TECHNIQUE]->(tech)
        RETURN count(*) as created
        """

        with self.driver.session() as session:
            result = session.run(query, rels=relationships)
            record = result.single()
            created = record['created'] if record else 0
            self.stats['capec_attack_created'] = created
            print(f"Created {created} CAPEC→ATT&CK relationships")

            # Check for missing techniques
            missing_query = """
            UNWIND $rels AS rel
            OPTIONAL MATCH (tech:AttackTechnique {techniqueId: rel.technique_id})
            WITH rel, tech
            WHERE tech IS NULL
            RETURN DISTINCT rel.technique_id as missing_tech
            """
            result = session.run(missing_query, rels=relationships)
            missing = [r['missing_tech'] for r in result]
            self.stats['attack_not_found'].update(missing)
            if missing:
                print(f"Warning: {len(missing)} ATT&CK technique IDs not found in database")

    def analyze_complete_chains(self):
        """Count complete CVE→CWE→CAPEC→ATT&CK chains"""
        print("\nAnalyzing complete attack chains...")

        query = """
        MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)-[:USES_TECHNIQUE]->(tech:AttackTechnique)
        RETURN count(DISTINCT cve) as complete_chains,
               count(DISTINCT cwe) as cwes_in_chains,
               count(DISTINCT capec) as capecs_in_chains,
               count(DISTINCT tech) as techniques_in_chains
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()
            if record:
                self.stats['complete_chains'] = record['complete_chains']
                print(f"Complete CVE→CWE→CAPEC→ATT&CK chains: {record['complete_chains']}")
                print(f"CWEs participating in chains: {record['cwes_in_chains']}")
                print(f"CAPECs participating in chains: {record['capecs_in_chains']}")
                print(f"Techniques participating in chains: {record['techniques_in_chains']}")

    def get_coverage_metrics(self):
        """Calculate coverage metrics"""
        print("\nCalculating coverage metrics...")

        query = """
        MATCH (cwe:CWE)
        OPTIONAL MATCH (cwe)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
        WITH count(DISTINCT cwe) as total_cwes,
             count(DISTINCT capec) as cwes_with_capec
        MATCH (capec:CAPEC)
        OPTIONAL MATCH (capec)-[:USES_TECHNIQUE]->(tech:AttackTechnique)
        WITH total_cwes, cwes_with_capec,
             count(DISTINCT capec) as total_capecs,
             count(DISTINCT tech) as capecs_with_tech
        RETURN total_cwes, cwes_with_capec,
               total_capecs, capecs_with_tech,
               round(100.0 * cwes_with_capec / total_cwes, 2) as cwe_coverage,
               round(100.0 * capecs_with_tech / total_capecs, 2) as capec_coverage
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()
            if record:
                print(f"CWE coverage: {record['cwes_with_capec']}/{record['total_cwes']} ({record['cwe_coverage']}%)")
                print(f"CAPEC coverage: {record['capecs_with_tech']}/{record['total_capecs']} ({record['capec_coverage']}%)")

    def print_summary(self):
        """Print execution summary"""
        print("\n" + "="*80)
        print("EXECUTION SUMMARY")
        print("="*80)
        print(f"CWE→CAPEC relationships created: {self.stats['cwe_capec_created']}")
        print(f"CAPEC→ATT&CK relationships created: {self.stats['capec_attack_created']}")
        print(f"Complete CVE→CWE→CAPEC→ATT&CK chains: {self.stats['complete_chains']}")

        if self.stats['cwe_not_found']:
            print(f"\nMissing CWE IDs: {len(self.stats['cwe_not_found'])} (first 10: {list(self.stats['cwe_not_found'])[:10]})")

        if self.stats['attack_not_found']:
            print(f"Missing ATT&CK IDs: {len(self.stats['attack_not_found'])} (first 10: {list(self.stats['attack_not_found'])[:10]})")

        print("="*80)

def main():
    xml_file = '/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/capec_v3.9.xml'

    creator = CAPECRelationshipCreator(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Parse CAPEC XML
        cwe_rels, attack_rels = creator.parse_capec_xml(xml_file)

        # Create relationships
        creator.create_cwe_capec_relationships(cwe_rels)
        creator.create_capec_attack_relationships(attack_rels)

        # Analyze results
        creator.analyze_complete_chains()
        creator.get_coverage_metrics()

        # Print summary
        creator.print_summary()

    finally:
        creator.close()

    print("\n✅ Attack chain creation complete!")

if __name__ == "__main__":
    main()
