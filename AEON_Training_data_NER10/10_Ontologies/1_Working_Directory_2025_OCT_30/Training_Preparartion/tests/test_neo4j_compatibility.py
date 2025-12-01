#!/usr/bin/env python3
"""
Test Neo4j 5.26 Compatibility for CWE Import Scripts
Validates that elementId() function works correctly with first 10 CWE entries
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from neo4j import GraphDatabase
import sys

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"
XML_PATH = Path(__file__).parent.parent / "cwec_v4.18.xml"
MAX_TEST_ENTRIES = 10

class Neo4jCompatibilityTester:
    """Test Neo4j 5.26 compatibility fixes"""

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.test_results = {
            'elementId_function': False,
            'sample_import': False,
            'hierarchy_import': False,
            'total_tests': 3,
            'passed_tests': 0
        }

    def close(self):
        self.driver.close()

    def test_elementId_function(self):
        """Test that elementId() function works in Neo4j 5.26"""
        print("\n[TEST 1] Testing elementId() function...")

        with self.driver.session() as session:
            try:
                # Create a test node
                session.run("""
                    CREATE (test:TEST_NODE {name: 'neo4j_compatibility_test'})
                """)

                # Try to query using elementId()
                result = session.run("""
                    MATCH (n:TEST_NODE {name: 'neo4j_compatibility_test'})
                    RETURN elementId(n) as element_id, n.name as name
                """)

                record = result.single()
                if record and record['element_id']:
                    print(f"✅ PASS: elementId() returned: {record['element_id']}")
                    self.test_results['elementId_function'] = True
                    self.test_results['passed_tests'] += 1
                else:
                    print("❌ FAIL: elementId() did not return a value")

                # Cleanup
                session.run("MATCH (n:TEST_NODE) DELETE n")

            except Exception as e:
                print(f"❌ FAIL: elementId() function error: {e}")

    def test_sample_cwe_import(self):
        """Test importing first 10 CWE entries with new syntax"""
        print(f"\n[TEST 2] Testing sample CWE import (first {MAX_TEST_ENTRIES} entries)...")

        # Parse first 10 CWEs from XML
        tree = ET.parse(XML_PATH)
        root = tree.getroot()
        ns = {'cwe': 'http://cwe.mitre.org/cwe-7'}

        cwes = []
        for weakness in root.findall('.//cwe:Weakness', ns)[:MAX_TEST_ENTRIES]:
            cwe_id = weakness.get('ID')
            name = weakness.get('Name')
            desc_elem = weakness.find('.//cwe:Description', ns)
            description = desc_elem.text if desc_elem is not None else ""

            cwes.append({
                'cwe_id': cwe_id,
                'name': name,
                'description': description[:200] if description else ""
            })

        print(f"  Parsed {len(cwes)} CWE entries from XML")

        with self.driver.session() as session:
            try:
                imported = 0
                for cwe in cwes:
                    # Use same import logic as main script
                    session.run("""
                        MERGE (c:CWE_TEST {cwe_id: $cwe_id})
                        SET c.name = $name,
                            c.description = $description,
                            c.test_import = true
                    """,
                    cwe_id=cwe['cwe_id'],
                    name=cwe['name'],
                    description=cwe['description'])
                    imported += 1

                # Verify using elementId()
                result = session.run("""
                    MATCH (c:CWE_TEST)
                    RETURN elementId(c) as element_id, c.cwe_id as cwe_id, c.name as name
                    LIMIT 5
                """)

                verified = list(result)
                if len(verified) > 0:
                    print(f"✅ PASS: Imported {imported} CWEs successfully")
                    print(f"  Sample verification:")
                    for record in verified[:3]:
                        print(f"    - CWE-{record['cwe_id']}: {record['name'][:50]}...")

                    self.test_results['sample_import'] = True
                    self.test_results['passed_tests'] += 1
                else:
                    print("❌ FAIL: No CWEs found after import")

                # Cleanup
                session.run("MATCH (n:CWE_TEST) DELETE n")

            except Exception as e:
                print(f"❌ FAIL: Sample import error: {e}")
                import traceback
                traceback.print_exc()

    def test_hierarchy_import(self):
        """Test hierarchy import with integer CWE IDs"""
        print("\n[TEST 3] Testing hierarchy import with integer IDs...")

        with self.driver.session() as session:
            try:
                # Create test CWE nodes with string IDs (as stored in DB)
                session.run("""
                    CREATE (child:CWE_TEST {cwe_id: '79', name: 'XSS'})
                    CREATE (parent:CWE_TEST {cwe_id: '20', name: 'Input Validation'})
                """)

                # Test relationship creation using integer→string conversion
                test_relationships = [(79, 20)]  # Integer IDs as parsed from XML

                session.run("""
                    UNWIND $relationships as rel
                    MATCH (child:CWE_TEST {cwe_id: toString(rel[0])})
                    MATCH (parent:CWE_TEST {cwe_id: toString(rel[1])})
                    MERGE (child)-[:CHILDOF_TEST]->(parent)
                """, relationships=test_relationships)

                # Verify relationship using elementId() in result display
                result = session.run("""
                    MATCH (child:CWE_TEST)-[r:CHILDOF_TEST]->(parent:CWE_TEST)
                    RETURN child.cwe_id as child_id, parent.cwe_id as parent_id, count(r) as rels
                """)

                record = result.single()
                if record and record['rels'] > 0:
                    print(f"✅ PASS: Hierarchy relationship created")
                    print(f"  CWE-{record['child_id']} → CWE-{record['parent_id']}")
                    self.test_results['hierarchy_import'] = True
                    self.test_results['passed_tests'] += 1
                else:
                    print("❌ FAIL: Hierarchy relationship not created")

                # Cleanup
                session.run("MATCH (n:CWE_TEST) DETACH DELETE n")

            except Exception as e:
                print(f"❌ FAIL: Hierarchy import error: {e}")
                import traceback
                traceback.print_exc()

    def run_all_tests(self):
        """Run all compatibility tests"""
        print("="*80)
        print("  NEO4J 5.26 COMPATIBILITY TESTS")
        print("="*80)

        self.test_elementId_function()
        self.test_sample_cwe_import()
        self.test_hierarchy_import()

        # Summary
        print("\n" + "="*80)
        print("  TEST SUMMARY")
        print("="*80)
        print(f"Tests Passed: {self.test_results['passed_tests']}/{self.test_results['total_tests']}")
        print()

        if self.test_results['passed_tests'] == self.test_results['total_tests']:
            print("✅ ALL TESTS PASSED - Scripts are Neo4j 5.26 compatible")
            print()
            print("Ready for production import:")
            print("  1. Run: python scripts/import_complete_cwe_catalog_neo4j.py")
            print("  2. Run: python scripts/import_cwe_hierarchy.py")
            return 0
        else:
            print("❌ SOME TESTS FAILED - Review errors above")
            return 1

def main():
    if not XML_PATH.exists():
        print(f"ERROR: CWE XML file not found: {XML_PATH}")
        return 1

    tester = None
    try:
        tester = Neo4jCompatibilityTester(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
        return tester.run_all_tests()
    except Exception as e:
        print(f"ERROR: Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if tester:
            tester.close()

if __name__ == "__main__":
    sys.exit(main())
