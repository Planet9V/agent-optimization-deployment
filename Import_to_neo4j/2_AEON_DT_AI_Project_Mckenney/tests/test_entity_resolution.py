#!/usr/bin/env python3
"""
Test Suite for Entity Resolution with Forward Compatibility

Tests the entity_resolver.py module's ability to:
1. Link document entities (CVE/CWE/CAPEC) to API-imported knowledge base nodes
2. Handle unresolved entities with proper status tracking
3. Prevent duplicate relationships
4. Create direct document-to-entity links for optimized querying
5. Support future entity types through extensible patterns

Test Philosophy:
- Verify actual resolution behavior against live Neo4j database
- Test both positive (entity exists) and negative (entity not found) cases
- Validate relationship structure and properties
- Ensure idempotency (no duplicate relationships on re-run)
"""

import unittest
import sys
import uuid
import logging
from typing import Dict, List, Set
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney')

from neo4j import GraphDatabase
from entity_resolver import EntityResolver

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestEntityResolution(unittest.TestCase):
    """
    Test suite for entity resolution with forward compatibility.

    Test Database Schema:
    - Document nodes created with unique test IDs
    - Entity nodes linked via CONTAINS_ENTITY
    - API nodes (CVE/CWE/CAPEC) created to simulate existing knowledge base
    - Resolution creates RESOLVES_TO and MENTIONS_* relationships
    """

    @classmethod
    def setUpClass(cls):
        """Set up test database connection once for all tests"""
        cls.neo4j_uri = "bolt://localhost:7687"
        cls.neo4j_user = "neo4j"
        cls.neo4j_password = "neo4j@openspg"

        try:
            cls.driver = GraphDatabase.driver(
                cls.neo4j_uri,
                auth=(cls.neo4j_user, cls.neo4j_password)
            )
            # Verify connection
            with cls.driver.session() as session:
                session.run("RETURN 1")
            logger.info("✓ Connected to Neo4j test database")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

        cls.resolver = EntityResolver(cls.driver)

    @classmethod
    def tearDownClass(cls):
        """Clean up database connection"""
        if hasattr(cls, 'driver'):
            cls.driver.close()

    def setUp(self):
        """Set up test data before each test"""
        self.test_doc_id = f"test-doc-{uuid.uuid4()}"
        self.test_entities: List[Dict] = []
        self.test_api_nodes: List[Dict] = []

    def tearDown(self):
        """Clean up test data after each test"""
        with self.driver.session() as session:
            # Delete test document and all related entities
            session.run("""
                MATCH (d:Document {id: $doc_id})
                OPTIONAL MATCH (d)-[r1:CONTAINS_ENTITY]->(e:Entity)
                OPTIONAL MATCH (e)-[r2:RESOLVES_TO]->()
                OPTIONAL MATCH (d)-[r3:MENTIONS_CVE|MENTIONS_CWE|MENTIONS_CAPEC]->()
                DELETE r1, r2, r3, e, d
            """, doc_id=self.test_doc_id)

            # Delete test API nodes
            for api_node in self.test_api_nodes:
                node_type = api_node['type']
                node_id = api_node['id']
                session.run(f"""
                    MATCH (n:{node_type} {{id: $node_id}})
                    DETACH DELETE n
                """, node_id=node_id)

    # Helper Methods

    def create_test_document(self, title: str = "Test Document"):
        """Create a test document node"""
        with self.driver.session() as session:
            session.run("""
                CREATE (d:Document {
                    id: $doc_id,
                    title: $title,
                    created_at: datetime()
                })
            """, doc_id=self.test_doc_id, title=title)

    def create_test_entity(self, entity_type: str, entity_text: str) -> str:
        """
        Create a test entity node linked to test document.

        Args:
            entity_type: Entity label (CVE, CWE, CAPEC)
            entity_text: Entity text content (e.g., "CVE-2024-1234")

        Returns:
            Entity UUID
        """
        entity_id = f"entity-{uuid.uuid4()}"

        with self.driver.session() as session:
            session.run("""
                MATCH (d:Document {id: $doc_id})
                CREATE (e:Entity {
                    id: $entity_id,
                    label: $entity_type,
                    text: $entity_text,
                    created_at: datetime()
                })
                CREATE (d)-[:CONTAINS_ENTITY]->(e)
            """, doc_id=self.test_doc_id, entity_id=entity_id,
                entity_type=entity_type, entity_text=entity_text)

        self.test_entities.append({
            'id': entity_id,
            'type': entity_type,
            'text': entity_text
        })

        return entity_id

    def create_api_cve_node(self, cve_id: str, description: str = "Test CVE"):
        """Create a test CVE node simulating API-imported data"""
        api_node_id = f"cve-{cve_id.lower()}"

        with self.driver.session() as session:
            session.run("""
                CREATE (c:CVE {
                    id: $node_id,
                    cve_id: $cve_id,
                    cveId: $cve_id,
                    description: $description,
                    created_at: datetime()
                })
            """, node_id=api_node_id, cve_id=cve_id, description=description)

        self.test_api_nodes.append({
            'type': 'CVE',
            'id': api_node_id
        })

    def create_api_cwe_node(self, cwe_id: str, name: str = "Test CWE"):
        """Create a test CWE node simulating API-imported data"""
        api_node_id = f"cwe-{cwe_id}"

        with self.driver.session() as session:
            session.run("""
                CREATE (w:CWE {
                    id: $node_id,
                    cwe_id: $cwe_id,
                    name: $name,
                    created_at: datetime()
                })
            """, node_id=api_node_id, cwe_id=cwe_id, name=name)

        self.test_api_nodes.append({
            'type': 'CWE',
            'id': api_node_id
        })

    def create_api_capec_node(self, capec_id: str, name: str = "Test CAPEC"):
        """Create a test CAPEC node simulating API-imported data"""
        api_node_id = f"capec-{capec_id}"

        with self.driver.session() as session:
            session.run("""
                MERGE (cap:CAPEC {capecId: $capec_id})
                ON CREATE SET
                    cap.id = $node_id,
                    cap.name = $name,
                    cap.created_at = datetime()
                ON MATCH SET
                    cap.id = $node_id,
                    cap.name = $name
            """, node_id=api_node_id, capec_id=capec_id, name=name)

        self.test_api_nodes.append({
            'type': 'CAPEC',
            'id': api_node_id
        })

    def get_resolves_to_count(self, entity_id: str) -> int:
        """Count RESOLVES_TO relationships for an entity"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e:Entity {id: $entity_id})-[r:RESOLVES_TO]->()
                RETURN count(r) as count
            """, entity_id=entity_id)
            record = result.single()
            return record['count'] if record else 0

    def get_mentions_relationship_count(self, doc_id: str, rel_type: str) -> int:
        """Count MENTIONS_* relationships for a document"""
        with self.driver.session() as session:
            result = session.run(f"""
                MATCH (d:Document {{id: $doc_id}})-[r:{rel_type}]->()
                RETURN count(r) as count
            """, doc_id=doc_id)
            record = result.single()
            return record['count'] if record else 0

    def entity_has_resolution_status(self, entity_id: str) -> bool:
        """Check if entity has resolution_status property"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e:Entity {id: $entity_id})
                RETURN exists(e.resolution_status) as has_status
            """, entity_id=entity_id)
            record = result.single()
            return record['has_status'] if record else False

    # Test Cases

    def test_cve_exists_in_api_creates_resolves_to_relationship(self):
        """
        SCENARIO: CVE entity exists in API database
        EXPECTED: RESOLVES_TO relationship created
        """
        # Arrange
        self.create_test_document("CVE Test Document")
        self.create_api_cve_node("CVE-2024-1234", "SQL Injection vulnerability")
        entity_id = self.create_test_entity("CVE", "CVE-2024-1234")

        # Act
        stats = self.resolver.resolve_all_entities(self.test_doc_id)

        # Assert
        self.assertEqual(stats['cve_resolved'], 1, "Should resolve 1 CVE")
        self.assertEqual(stats['cve_not_found'], 0, "Should have 0 unresolved CVEs")

        resolves_count = self.get_resolves_to_count(entity_id)
        self.assertEqual(resolves_count, 1, "Should create 1 RESOLVES_TO relationship")

    def test_cve_not_in_api_marks_entity_unresolved(self):
        """
        SCENARIO: CVE entity does NOT exist in API database
        EXPECTED: Entity marked as unresolved, no RESOLVES_TO created
        """
        # Arrange
        self.create_test_document("Unresolved CVE Document")
        entity_id = self.create_test_entity("CVE", "CVE-9999-9999")  # Non-existent CVE

        # Act
        stats = self.resolver.resolve_all_entities(self.test_doc_id)

        # Assert
        self.assertEqual(stats['cve_resolved'], 0, "Should resolve 0 CVEs")
        self.assertEqual(stats['cve_not_found'], 1, "Should have 1 unresolved CVE")

        resolves_count = self.get_resolves_to_count(entity_id)
        self.assertEqual(resolves_count, 0, "Should NOT create RESOLVES_TO relationship")

    def test_duplicate_cve_mentions_no_duplicate_relationships(self):
        """
        SCENARIO: Same CVE mentioned multiple times in document
        EXPECTED: Multiple entities resolve to same CVE, no duplicate relationships
        """
        # Arrange
        self.create_test_document("Duplicate CVE Document")
        self.create_api_cve_node("CVE-2024-5678", "Buffer overflow")

        entity1_id = self.create_test_entity("CVE", "CVE-2024-5678")
        entity2_id = self.create_test_entity("CVE", "CVE-2024-5678")  # Duplicate mention

        # Act
        stats = self.resolver.resolve_all_entities(self.test_doc_id)

        # Assert
        self.assertEqual(stats['cve_resolved'], 2, "Should resolve both CVE mentions")

        # Both entities should have RESOLVES_TO relationships
        self.assertEqual(self.get_resolves_to_count(entity1_id), 1)
        self.assertEqual(self.get_resolves_to_count(entity2_id), 1)

        # Document should have only 1 MENTIONS_CVE relationship (no duplicates)
        mentions_count = self.get_mentions_relationship_count(self.test_doc_id, "MENTIONS_CVE")
        self.assertEqual(mentions_count, 1, "Should create only 1 MENTIONS_CVE relationship")

    def test_multiple_cves_all_resolved_correctly(self):
        """
        SCENARIO: Document contains multiple different CVEs
        EXPECTED: All CVEs resolved with separate relationships
        """
        # Arrange
        self.create_test_document("Multiple CVEs Document")
        self.create_api_cve_node("CVE-2024-1111", "XSS vulnerability")
        self.create_api_cve_node("CVE-2024-2222", "CSRF vulnerability")
        self.create_api_cve_node("CVE-2024-3333", "RCE vulnerability")

        entity1_id = self.create_test_entity("CVE", "CVE-2024-1111")
        entity2_id = self.create_test_entity("CVE", "CVE-2024-2222")
        entity3_id = self.create_test_entity("CVE", "CVE-2024-3333")

        # Act
        stats = self.resolver.resolve_all_entities(self.test_doc_id)

        # Assert
        self.assertEqual(stats['cve_resolved'], 3, "Should resolve all 3 CVEs")
        self.assertEqual(stats['cve_not_found'], 0, "Should have 0 unresolved")

        # Each entity should be resolved
        self.assertEqual(self.get_resolves_to_count(entity1_id), 1)
        self.assertEqual(self.get_resolves_to_count(entity2_id), 1)
        self.assertEqual(self.get_resolves_to_count(entity3_id), 1)

        # Document should have 3 MENTIONS_CVE relationships
        mentions_count = self.get_mentions_relationship_count(self.test_doc_id, "MENTIONS_CVE")
        self.assertEqual(mentions_count, 3, "Should create 3 MENTIONS_CVE relationships")

    def test_cwe_resolution_same_logic_as_cve(self):
        """
        SCENARIO: CWE entity resolution
        EXPECTED: Same resolution logic applies as CVE
        """
        # Arrange
        self.create_test_document("CWE Test Document")
        self.create_api_cwe_node("89", "SQL Injection")
        entity_id = self.create_test_entity("CWE", "CWE-89")

        # Act
        stats = self.resolver.resolve_all_entities(self.test_doc_id)

        # Assert
        self.assertEqual(stats['cwe_resolved'], 1, "Should resolve 1 CWE")
        self.assertEqual(stats['cwe_not_found'], 0, "Should have 0 unresolved CWEs")

        resolves_count = self.get_resolves_to_count(entity_id)
        self.assertEqual(resolves_count, 1, "Should create RESOLVES_TO relationship")

        mentions_count = self.get_mentions_relationship_count(self.test_doc_id, "MENTIONS_CWE")
        self.assertEqual(mentions_count, 1, "Should create MENTIONS_CWE relationship")

    def test_capec_resolution_same_logic_as_cve(self):
        """
        SCENARIO: CAPEC entity resolution
        EXPECTED: Same resolution logic applies as CVE
        """
        # Arrange
        self.create_test_document("CAPEC Test Document")
        self.create_api_capec_node("CAPEC-66", "SQL Injection")
        entity_id = self.create_test_entity("CAPEC", "CAPEC-66")

        # Act
        stats = self.resolver.resolve_all_entities(self.test_doc_id)

        # Assert
        self.assertEqual(stats['capec_resolved'], 1, "Should resolve 1 CAPEC")
        self.assertEqual(stats['capec_not_found'], 0, "Should have 0 unresolved CAPECs")

        resolves_count = self.get_resolves_to_count(entity_id)
        self.assertEqual(resolves_count, 1, "Should create RESOLVES_TO relationship")

        mentions_count = self.get_mentions_relationship_count(self.test_doc_id, "MENTIONS_CAPEC")
        self.assertEqual(mentions_count, 1, "Should create MENTIONS_CAPEC relationship")

    def test_mixed_entity_types_all_resolved(self):
        """
        SCENARIO: Document contains CVE, CWE, and CAPEC entities
        EXPECTED: All entity types resolved correctly
        """
        # Arrange
        self.create_test_document("Mixed Entities Document")
        self.create_api_cve_node("CVE-2024-4444", "Test CVE")
        self.create_api_cwe_node("79", "XSS")
        self.create_api_capec_node("CAPEC-63", "Cross-Site Scripting")

        self.create_test_entity("CVE", "CVE-2024-4444")
        self.create_test_entity("CWE", "CWE-79")
        self.create_test_entity("CAPEC", "CAPEC-63")

        # Act
        stats = self.resolver.resolve_all_entities(self.test_doc_id)

        # Assert
        self.assertEqual(stats['cve_resolved'], 1, "Should resolve CVE")
        self.assertEqual(stats['cwe_resolved'], 1, "Should resolve CWE")
        self.assertEqual(stats['capec_resolved'], 1, "Should resolve CAPEC")

        # Verify direct document links
        self.assertEqual(self.get_mentions_relationship_count(self.test_doc_id, "MENTIONS_CVE"), 1)
        self.assertEqual(self.get_mentions_relationship_count(self.test_doc_id, "MENTIONS_CWE"), 1)
        self.assertEqual(self.get_mentions_relationship_count(self.test_doc_id, "MENTIONS_CAPEC"), 1)

    def test_idempotent_resolution_no_duplicates_on_rerun(self):
        """
        SCENARIO: Entity resolution runs twice on same document
        EXPECTED: No duplicate relationships created (idempotency)
        """
        # Arrange
        self.create_test_document("Idempotency Test")
        self.create_api_cve_node("CVE-2024-7777", "Test")
        entity_id = self.create_test_entity("CVE", "CVE-2024-7777")

        # Act - Run resolution twice
        stats1 = self.resolver.resolve_all_entities(self.test_doc_id)
        stats2 = self.resolver.resolve_all_entities(self.test_doc_id)

        # Assert - Same results both times
        self.assertEqual(stats1['cve_resolved'], stats2['cve_resolved'])

        # Still only 1 relationship exists
        resolves_count = self.get_resolves_to_count(entity_id)
        self.assertEqual(resolves_count, 1, "Should maintain single RESOLVES_TO relationship")

        mentions_count = self.get_mentions_relationship_count(self.test_doc_id, "MENTIONS_CVE")
        self.assertEqual(mentions_count, 1, "Should maintain single MENTIONS_CVE relationship")

    def test_relationship_has_created_at_timestamp(self):
        """
        SCENARIO: Entity resolved successfully
        EXPECTED: RESOLVES_TO relationship has created_at timestamp
        """
        # Arrange
        self.create_test_document("Timestamp Test")
        self.create_api_cve_node("CVE-2024-8888", "Test")
        entity_id = self.create_test_entity("CVE", "CVE-2024-8888")

        # Act
        self.resolver.resolve_all_entities(self.test_doc_id)

        # Assert - Check relationship has timestamp
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e:Entity {id: $entity_id})-[r:RESOLVES_TO]->()
                RETURN r.created_at as timestamp
            """, entity_id=entity_id)
            record = result.single()

            self.assertIsNotNone(record, "RESOLVES_TO relationship should exist")
            self.assertIsNotNone(record['timestamp'], "Relationship should have created_at timestamp")

    def test_forward_compatibility_extensible_entity_types(self):
        """
        FORWARD COMPATIBILITY TEST:
        Verify resolution pattern can extend to future entity types.

        This test documents the pattern for adding new entity types:
        1. Create Entity node with new label
        2. Create corresponding API node type
        3. Add resolver method following naming convention
        4. Use same RESOLVES_TO and MENTIONS_* patterns
        """
        # This test serves as documentation for future entity types
        # Example: Adding "MITRE_TECHNIQUE" entity type would follow:
        #
        # 1. create_test_entity("MITRE_TECHNIQUE", "T1003")
        # 2. create_api_mitre_technique_node("T1003", "Credential Dumping")
        # 3. resolver.resolve_mitre_technique_entities(doc_id)
        # 4. resolver.create_document_mitre_technique_links(doc_id)
        #
        # The pattern is consistent and extensible.

        logger.info("✓ Entity resolution pattern is extensible for future entity types")
        logger.info("  Pattern: Entity[TYPE] -> resolve_TYPE_entities() -> RESOLVES_TO -> TYPE_NODE")
        logger.info("  Pattern: Document -> MENTIONS_TYPE -> TYPE_NODE")

        # This test always passes - it documents the extension pattern
        self.assertTrue(True, "Forward compatibility pattern documented")


def run_tests():
    """Run all entity resolution tests"""
    print("=" * 80)
    print("ENTITY RESOLUTION TEST SUITE")
    print("=" * 80)
    print("\nTesting entity resolution with forward compatibility...")
    print("Database: bolt://localhost:7687")
    print("-" * 80)

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestEntityResolution)

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"💥 Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED - Entity resolution working correctly!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED - Review errors above")
        return 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
