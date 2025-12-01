#!/usr/bin/env python3
"""
CWE Hierarchy Import Script
Imports parent-child (ChildOf) relationships from CWE XML catalog
This is CRITICAL for bridging CVE-CWEs to CAPEC-CWEs via hierarchy
"""

import xml.etree.ElementTree as ET
from neo4j import GraphDatabase
from pathlib import Path

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"
XML_PATH = Path(__file__).parent.parent / "cwec_v4.18.xml"

class CWEHierarchyImporter:
    """Import CWE parent-child relationships"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            'childof_created': 0,
            'weaknesses_processed': 0,
            'relationships_found': 0,
            'errors': 0
        }

    def close(self):
        """Close database connection"""
        self.driver.close()

    def parse_xml_hierarchy(self, xml_path: Path):
        """Parse CWE XML for parent-child relationships"""
        print(f"Parsing {xml_path}...")

        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Find namespace
        namespace = {'': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}
        ns_prefix = '' if not namespace else '{' + list(namespace.values())[0] + '}'

        relationships = []

        # Parse Weaknesses
        for weakness in root.findall(f'.//{ns_prefix}Weakness'):
            self.stats['weaknesses_processed'] += 1
            cwe_id_attr = weakness.get('ID')
            if not cwe_id_attr:
                continue

            child_id = int(cwe_id_attr)

            # Find Related_Weaknesses
            related = weakness.find(f'{ns_prefix}Related_Weaknesses')
            if related is not None:
                for related_weakness in related.findall(f'{ns_prefix}Related_Weakness'):
                    nature = related_weakness.get('Nature', '')
                    if nature == 'ChildOf':
                        parent_cwe_id = related_weakness.get('CWE_ID')
                        if parent_cwe_id:
                            parent_id = int(parent_cwe_id)
                            relationships.append((child_id, parent_id))
                            self.stats['relationships_found'] += 1

        print(f"Found {self.stats['relationships_found']} ChildOf relationships")
        return relationships

    def import_hierarchy(self, relationships):
        """Import relationships into Neo4j"""
        print(f"Importing {len(relationships)} relationships...")

        with self.driver.session() as session:
            # Create relationships in batches
            batch_size = 1000
            for i in range(0, len(relationships), batch_size):
                batch = relationships[i:i+batch_size]

                result = session.run("""
                    UNWIND $relationships as rel
                    MATCH (child:CWE {cwe_id: toString(rel[0])})
                    MATCH (parent:CWE {cwe_id: toString(rel[1])})
                    MERGE (child)-[:CHILDOF]->(parent)
                    RETURN count(*) as created
                """, relationships=batch)

                created = result.single()['created']
                self.stats['childof_created'] += created

                print(f"  Batch {i//batch_size + 1}: {created} relationships created")

    def verify_import(self):
        """Verify hierarchy was imported successfully"""
        with self.driver.session() as session:
            # Count total CHILDOF relationships
            result = session.run("""
                MATCH (cwe1:CWE)-[r:CHILDOF]->(cwe2:CWE)
                RETURN count(r) as total
            """)
            total_childof = result.single()['total']

            # Sample some relationships
            result = session.run("""
                MATCH (child:CWE)-[:CHILDOF]->(parent:CWE)
                RETURN child.cwe_id as child_id, parent.cwe_id as parent_id
                LIMIT 10
            """)
            samples = list(result)

            print()
            print("="*80)
            print("  VERIFICATION")
            print("="*80)
            print(f"Total CHILDOF relationships: {total_childof}")
            print()
            print("Sample relationships:")
            for record in samples:
                print(f"  {record['child_id']} → {record['parent_id']}")
            print()

            # Check if this could bridge CVE-CWEs to CAPEC-CWEs
            result = session.run("""
                MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe1:CWE)
                MATCH (cwe1)-[:CHILDOF*1..5]->(cwe2:CWE)
                MATCH (cwe2)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                RETURN count(DISTINCT cve) as bridgeable_cves
            """)
            bridgeable = result.single()['bridgeable_cves']

            print(f"✓ CVEs bridgeable via hierarchy: {bridgeable}")

            if bridgeable > 0:
                print()
                print("🎉 SUCCESS! CWE hierarchy can bridge CVE-CWEs to CAPEC-CWEs")
                print()
                print("Next step: Create transitive ENABLES_ATTACK_PATTERN relationships")
            else:
                print()
                print("⚠ WARNING: Hierarchy exists but doesn't bridge the gap")
                print("   May need deeper hierarchy traversal (>5 hops)")


def main():
    """Main execution"""
    print("="*80)
    print("  CWE HIERARCHY IMPORT")
    print("="*80)
    print()

    if not XML_PATH.exists():
        print(f"ERROR: XML file not found: {XML_PATH}")
        return 1

    importer = None
    try:
        importer = CWEHierarchyImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

        # Parse XML
        relationships = importer.parse_xml_hierarchy(XML_PATH)

        if not relationships:
            print("ERROR: No relationships found in XML")
            return 1

        # Import to Neo4j
        importer.import_hierarchy(relationships)

        # Verify
        importer.verify_import()

        # Summary
        print("="*80)
        print("  IMPORT SUMMARY")
        print("="*80)
        print(f"Weaknesses processed:      {importer.stats['weaknesses_processed']}")
        print(f"Relationships found:       {importer.stats['relationships_found']}")
        print(f"CHILDOF relationships:     {importer.stats['childof_created']}")
        print()

    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        if importer:
            importer.close()

    return 0


if __name__ == "__main__":
    exit(main())
