#!/usr/bin/env python3
"""
Import CAPEC to ATT&CK Technique Relationships
Maps CAPEC attack patterns to MITRE ATT&CK techniques using CAPEC catalog metadata.
"""

import xml.etree.ElementTree as ET
from neo4j import GraphDatabase
import sys
from collections import defaultdict
from datetime import datetime

# Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

class CAPECAttackMapper:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            'capec_attack_created': 0,
            'capec_patterns_with_attack': 0,
            'attack_techniques_linked': 0,
            'capec_not_found': set(),
            'attack_not_found': set(),
            'total_mappings_in_xml': 0
        }

    def close(self):
        self.driver.close()

    def parse_capec_attack_mappings(self, xml_file):
        """Parse CAPEC XML and extract ATT&CK technique mappings"""
        print(f"Parsing {xml_file}...")
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Define namespace
        ns = {'capec': 'http://capec.mitre.org/capec-3'}

        attack_relationships = []

        # Find all Attack_Pattern elements
        for pattern in root.findall('.//capec:Attack_Pattern', ns):
            capec_id = pattern.get('ID')
            if not capec_id:
                continue

            # Extract ATT&CK relationships from taxonomy mappings
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

                                # Get technique name if available
                                technique_name = None
                                for entry_name in mapping.findall('.//capec:Entry_Name', ns):
                                    technique_name = entry_name.text
                                    break

                                attack_relationships.append({
                                    'capec_id': f"CAPEC-{capec_id}",
                                    'technique_id': technique_id,
                                    'technique_name': technique_name
                                })

        self.stats['total_mappings_in_xml'] = len(attack_relationships)
        print(f"Found {len(attack_relationships)} CAPEC→ATT&CK mappings in XML")

        # Show sample mappings
        if attack_relationships:
            print("\nSample mappings:")
            for rel in attack_relationships[:5]:
                print(f"  {rel['capec_id']} → {rel['technique_id']} ({rel['technique_name']})")

        return attack_relationships

    def create_capec_attack_relationships(self, relationships):
        """Create CAPEC→ATT&CK IMPLEMENTS relationships in Neo4j"""
        print("\n" + "="*80)
        print("Creating CAPEC→ATT&CK relationships...")
        print("="*80)

        query = """
        UNWIND $rels AS rel
        MATCH (capec:CAPEC {capecId: rel.capec_id})
        MATCH (tech:AttackTechnique {techniqueId: rel.technique_id})
        MERGE (capec)-[r:IMPLEMENTS]->(tech)
        ON CREATE SET r.created = datetime(),
                      r.source = 'CAPEC v3.9 Taxonomy Mapping'
        RETURN count(*) as created
        """

        with self.driver.session() as session:
            result = session.run(query, rels=relationships)
            record = result.single()
            created = record['created'] if record else 0
            self.stats['capec_attack_created'] = created
            print(f"✅ Created {created} CAPEC→ATT&CK IMPLEMENTS relationships")

            # Count unique CAPEC patterns with ATT&CK mappings
            count_query = """
            MATCH (capec:CAPEC)-[:IMPLEMENTS]->(tech:AttackTechnique)
            RETURN count(DISTINCT capec) as capec_count,
                   count(DISTINCT tech) as tech_count
            """
            result = session.run(count_query)
            record = result.single()
            if record:
                self.stats['capec_patterns_with_attack'] = record['capec_count']
                self.stats['attack_techniques_linked'] = record['tech_count']
                print(f"   {record['capec_count']} unique CAPEC patterns mapped to ATT&CK")
                print(f"   {record['tech_count']} unique ATT&CK techniques linked")

            # Check for missing CAPECs
            missing_capec_query = """
            UNWIND $rels AS rel
            OPTIONAL MATCH (capec:CAPEC {capecId: rel.capec_id})
            WITH rel, capec
            WHERE capec IS NULL
            RETURN DISTINCT rel.capec_id as missing_capec
            """
            result = session.run(missing_capec_query, rels=relationships)
            missing_capec = [r['missing_capec'] for r in result]
            self.stats['capec_not_found'].update(missing_capec)
            if missing_capec:
                print(f"\n⚠️  {len(missing_capec)} CAPEC IDs not found in database")
                print(f"   First 5: {missing_capec[:5]}")

            # Check for missing ATT&CK techniques
            missing_attack_query = """
            UNWIND $rels AS rel
            OPTIONAL MATCH (tech:AttackTechnique {techniqueId: rel.technique_id})
            WITH rel, tech
            WHERE tech IS NULL
            RETURN DISTINCT rel.technique_id as missing_tech
            """
            result = session.run(missing_attack_query, rels=relationships)
            missing_attack = [r['missing_tech'] for r in result]
            self.stats['attack_not_found'].update(missing_attack)
            if missing_attack:
                print(f"\n⚠️  {len(missing_attack)} ATT&CK technique IDs not found in database")
                print(f"   First 5: {missing_attack[:5]}")

    def verify_relationships(self):
        """Verify created relationships with sample queries"""
        print("\n" + "="*80)
        print("Verifying relationships...")
        print("="*80)

        with self.driver.session() as session:
            # Sample CAPEC→ATT&CK relationships
            sample_query = """
            MATCH (capec:CAPEC)-[r:IMPLEMENTS]->(tech:AttackTechnique)
            RETURN capec.capecId, capec.name, tech.techniqueId, tech.name
            LIMIT 5
            """
            result = session.run(sample_query)
            print("\nSample CAPEC→ATT&CK relationships:")
            for r in result:
                print(f"  {r[0]} ({r[1][:50]}...)")
                print(f"    → {r[2]} ({r[3][:50]}...)")

            # Check for complete CWE→CAPEC→ATT&CK chains
            chain_query = """
            MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)-[:IMPLEMENTS]->(tech:AttackTechnique)
            RETURN count(DISTINCT cwe) as cwe_count,
                   count(DISTINCT capec) as capec_count,
                   count(DISTINCT tech) as tech_count,
                   count(*) as total_chains
            """
            result = session.run(chain_query)
            record = result.single()
            if record:
                print(f"\nComplete CWE→CAPEC→ATT&CK chains:")
                print(f"  CWEs in chains: {record['cwe_count']}")
                print(f"  CAPECs in chains: {record['capec_count']}")
                print(f"  ATT&CK techniques in chains: {record['tech_count']}")
                print(f"  Total chain paths: {record['total_chains']}")

    def print_summary(self):
        """Print execution summary"""
        print("\n" + "="*80)
        print("EXECUTION SUMMARY")
        print("="*80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nInput:")
        print(f"  Total CAPEC→ATT&CK mappings in XML: {self.stats['total_mappings_in_xml']}")

        print(f"\nOutput:")
        print(f"  IMPLEMENTS relationships created: {self.stats['capec_attack_created']}")
        print(f"  Unique CAPEC patterns mapped: {self.stats['capec_patterns_with_attack']}")
        print(f"  Unique ATT&CK techniques linked: {self.stats['attack_techniques_linked']}")

        if self.stats['capec_not_found']:
            print(f"\n⚠️  Issues:")
            print(f"  Missing CAPEC IDs: {len(self.stats['capec_not_found'])}")

        if self.stats['attack_not_found']:
            print(f"  Missing ATT&CK IDs: {len(self.stats['attack_not_found'])}")

        # Calculate success rate
        success_rate = (self.stats['capec_attack_created'] / self.stats['total_mappings_in_xml'] * 100) if self.stats['total_mappings_in_xml'] > 0 else 0
        print(f"\n✅ Success Rate: {success_rate:.1f}%")
        print("="*80)

def main():
    xml_file = '/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/capec_v3.9.xml'

    print("="*80)
    print("CAPEC→ATT&CK Relationship Import")
    print("="*80)
    print(f"Source: CAPEC v3.9 XML Catalog")
    print(f"Target: Neo4j Knowledge Graph")
    print(f"Relationship: CAPEC-[:IMPLEMENTS]->AttackTechnique")
    print("="*80)

    mapper = CAPECAttackMapper(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Parse CAPEC XML for ATT&CK mappings
        attack_rels = mapper.parse_capec_attack_mappings(xml_file)

        if not attack_rels:
            print("\n❌ No CAPEC→ATT&CK mappings found in XML")
            return 1

        # Create relationships in Neo4j
        mapper.create_capec_attack_relationships(attack_rels)

        # Verify results
        mapper.verify_relationships()

        # Print summary
        mapper.print_summary()

        print("\n✅ CAPEC→ATT&CK relationship import COMPLETE!")
        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        mapper.close()

if __name__ == "__main__":
    sys.exit(main())
