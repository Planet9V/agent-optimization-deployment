#!/usr/bin/env python3
"""
Import CWE→CAPEC relationship mappings from CAPEC v3.9 catalog
Creates ENABLES_ATTACK_PATTERN relationships between CWE and CAPEC nodes
"""

import xml.etree.ElementTree as ET
from neo4j import GraphDatabase
import sys

# Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

class CAPECCWEImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            'relationships_created': 0,
            'cwe_not_found': set(),
            'capec_not_found': set(),
            'total_mappings': 0
        }

    def close(self):
        self.driver.close()

    def parse_capec_xml(self, xml_file):
        """Parse CAPEC XML and extract CWE relationships"""
        print(f"Parsing {xml_file}...")
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Define namespace
        ns = {'capec': 'http://capec.mitre.org/capec-3'}

        cwe_relationships = []

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
                            'cwe_id': cwe_id,  # Keep as string for matching
                            'capec_id': f"CAPEC-{capec_id}"
                        })

        print(f"Found {len(cwe_relationships)} CWE→CAPEC relationship mappings")
        return cwe_relationships

    def create_relationships(self, relationships):
        """Create CWE→CAPEC ENABLES_ATTACK_PATTERN relationships in Neo4j"""
        print("\nCreating CWE→CAPEC relationships...")
        self.stats['total_mappings'] = len(relationships)

        # Use UNWIND for efficient batch processing
        query = """
        UNWIND $rels AS rel
        MATCH (cwe:CWE {cwe_id: rel.cwe_id})
        MATCH (capec:CAPEC {capecId: rel.capec_id})
        MERGE (cwe)-[r:ENABLES_ATTACK_PATTERN]->(capec)
        RETURN count(r) as created
        """

        with self.driver.session() as session:
            result = session.run(query, rels=relationships)
            record = result.single()
            created = record['created'] if record else 0
            self.stats['relationships_created'] = created
            print(f"✅ Created {created} CWE→CAPEC relationships")

            # Check for missing CWEs
            missing_cwe_query = """
            UNWIND $rels AS rel
            OPTIONAL MATCH (cwe:CWE {cwe_id: rel.cwe_id})
            WITH rel, cwe
            WHERE cwe IS NULL
            RETURN DISTINCT rel.cwe_id as missing_cwe
            """
            result = session.run(missing_cwe_query, rels=relationships)
            missing_cwes = [r['missing_cwe'] for r in result]
            self.stats['cwe_not_found'].update(missing_cwes)

            # Check for missing CAPECs
            missing_capec_query = """
            UNWIND $rels AS rel
            OPTIONAL MATCH (capec:CAPEC {capecId: rel.capec_id})
            WITH rel, capec
            WHERE capec IS NULL
            RETURN DISTINCT rel.capec_id as missing_capec
            """
            result = session.run(missing_capec_query, rels=relationships)
            missing_capecs = [r['missing_capec'] for r in result]
            self.stats['capec_not_found'].update(missing_capecs)

    def verify_relationships(self):
        """Verify the created relationships"""
        print("\nVerifying relationships...")

        with self.driver.session() as session:
            # Count total relationships
            result = session.run("""
                MATCH (cwe:CWE)-[r:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                RETURN count(r) as total
            """)
            total = result.single()['total']
            print(f"Total ENABLES_ATTACK_PATTERN relationships: {total}")

            # Sample relationships
            result = session.run("""
                MATCH (cwe:CWE)-[r:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                RETURN cwe.cwe_id as cwe_id, capec.capecId as capec_id
                LIMIT 5
            """)
            print("\nSample relationships:")
            for record in result:
                print(f"  CWE-{record['cwe_id']} → {record['capec_id']}")

    def print_summary(self):
        """Print execution summary"""
        print("\n" + "="*80)
        print("IMPORT SUMMARY")
        print("="*80)
        print(f"Total mappings found in CAPEC catalog: {self.stats['total_mappings']}")
        print(f"Relationships created in Neo4j: {self.stats['relationships_created']}")

        success_rate = (self.stats['relationships_created'] / self.stats['total_mappings'] * 100) if self.stats['total_mappings'] > 0 else 0
        print(f"Success rate: {success_rate:.1f}%")

        if self.stats['cwe_not_found']:
            print(f"\nMissing CWE nodes: {len(self.stats['cwe_not_found'])}")
            print(f"  Examples: {list(self.stats['cwe_not_found'])[:10]}")

        if self.stats['capec_not_found']:
            print(f"\nMissing CAPEC nodes: {len(self.stats['capec_not_found'])}")
            print(f"  Examples: {list(self.stats['capec_not_found'])[:10]}")

        print("="*80)

def main():
    xml_file = '/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/capec_v3.9.xml'

    importer = CAPECCWEImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Parse CAPEC XML
        relationships = importer.parse_capec_xml(xml_file)

        # Create relationships
        importer.create_relationships(relationships)

        # Verify results
        importer.verify_relationships()

        # Print summary
        importer.print_summary()

    finally:
        importer.close()

    print("\n✅ CWE→CAPEC relationship import complete!")

if __name__ == "__main__":
    main()
