"""
Test Suite for NER11 to Neo4j Hierarchical Pipeline

Tests:
1. Pipeline initialization
2. Entity extraction (mocked NER11 API)
3. Hierarchical enrichment
4. Node creation with MERGE
5. Relationship extraction
6. Validation (node count + tier distribution)

File: test_05_neo4j_hierarchical_pipeline.py
Created: 2025-12-01
Version: 1.0.0
Status: PRODUCTION-READY
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add parent directory to path
pipeline_dir = Path(__file__).parent
sys.path.insert(0, str(pipeline_dir))

# Import pipeline
import importlib.util
spec = importlib.util.spec_from_file_location(
    "neo4j_pipeline",
    pipeline_dir / "05_ner11_to_neo4j_hierarchical.py"
)
pipeline_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_module)
NER11ToNeo4jPipeline = pipeline_module.NER11ToNeo4jPipeline


class TestNER11ToNeo4jPipeline(unittest.TestCase):
    """Test suite for Neo4j hierarchical pipeline"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock NER11 API responses
        self.mock_entities = [
            {"text": "APT29", "label": "APT_GROUP", "start": 0, "end": 5},
            {"text": "CVE-2020-0688", "label": "CVE", "start": 100, "end": 113},
            {"text": "WellMess", "label": "MALWARE", "start": 200, "end": 208},
            {"text": "Microsoft Exchange Server", "label": "SOFTWARE_COMPONENT", "start": 150, "end": 175},
            {"text": "United States", "label": "LOCATION", "start": 300, "end": 313}
        ]

    @patch('neo4j.GraphDatabase.driver')
    @patch('requests.post')
    def test_pipeline_initialization(self, mock_post, mock_driver):
        """Test 1: Pipeline initializes correctly"""
        print("\n[TEST 1] Pipeline Initialization")

        # Mock Neo4j driver
        mock_driver.return_value = MagicMock()

        # Initialize pipeline
        pipeline = NER11ToNeo4jPipeline(
            neo4j_uri="bolt://localhost:7687",
            neo4j_user="neo4j",
            neo4j_password="neo4j@openspg"
        )

        # Assertions
        self.assertIsNotNone(pipeline.hierarchical_processor)
        self.assertIsNotNone(pipeline.mapper)
        self.assertEqual(pipeline.stats["documents_processed"], 0)

        print("✅ Pipeline initialized successfully")
        print(f"   Taxonomy size: {len(pipeline.hierarchical_processor.taxonomy)}")
        print(f"   Mapper labels: {len(pipeline.mapper.mapping_table)}")

    @patch('neo4j.GraphDatabase.driver')
    @patch('requests.post')
    def test_entity_extraction(self, mock_post, mock_driver):
        """Test 2: Entity extraction from NER11 API"""
        print("\n[TEST 2] Entity Extraction")

        # Mock responses
        mock_driver.return_value = MagicMock()
        mock_post.return_value.json.return_value = {
            "entities": self.mock_entities
        }
        mock_post.return_value.raise_for_status = MagicMock()

        # Initialize and extract
        pipeline = NER11ToNeo4jPipeline()
        entities = pipeline.extract_entities_from_text("Sample text")

        # Assertions
        self.assertEqual(len(entities), 5)
        self.assertEqual(entities[0]["text"], "APT29")
        self.assertEqual(entities[1]["label"], "CVE")

        print(f"✅ Extracted {len(entities)} entities")
        for entity in entities:
            print(f"   - {entity['text']} ({entity['label']})")

    @patch('neo4j.GraphDatabase.driver')
    def test_entity_enrichment(self, mock_driver):
        """Test 3: Hierarchical entity enrichment"""
        print("\n[TEST 3] Entity Enrichment")

        mock_driver.return_value = MagicMock()

        pipeline = NER11ToNeo4jPipeline()

        # Test enrichment for different entity types
        test_cases = [
            {
                "input": {"text": "APT29", "label": "APT_GROUP", "start": 0, "end": 5},
                "expected_super_label": "ThreatActor",
                "expected_tier": 1
            },
            {
                "input": {"text": "CVE-2020-0688", "label": "CVE", "start": 0, "end": 13},
                "expected_super_label": "Vulnerability",
                "expected_tier": 1
            },
            {
                "input": {"text": "WellMess", "label": "MALWARE", "start": 0, "end": 8},
                "expected_super_label": "Malware",
                "expected_tier": 1
            }
        ]

        for i, test in enumerate(test_cases, 1):
            enriched = pipeline.enrich_entity(test["input"])

            self.assertEqual(enriched["super_label"], test["expected_super_label"])
            self.assertEqual(enriched["tier"], test["expected_tier"])
            self.assertIn("hierarchy_path", enriched)
            self.assertIn("fine_grained_type", enriched)

            print(f"✅ Test case {i}: {enriched['specific_instance']}")
            print(f"   Super Label: {enriched['super_label']}")
            print(f"   Tier: {enriched['tier']}")
            print(f"   Hierarchy: {enriched['hierarchy_path']}")

    @patch('neo4j.GraphDatabase.driver')
    def test_node_creation(self, mock_driver):
        """Test 4: Node creation with MERGE"""
        print("\n[TEST 4] Node Creation")

        # Mock Neo4j session
        mock_session = MagicMock()
        mock_session.run.return_value.single.return_value = {"n": {"name": "APT29"}}
        mock_driver.return_value.session.return_value.__enter__.return_value = mock_session

        pipeline = NER11ToNeo4jPipeline()

        # Enrich and create node
        entity = {"text": "APT29", "label": "APT_GROUP", "start": 0, "end": 5}
        enriched = pipeline.enrich_entity(entity)
        result = pipeline.create_node_in_neo4j(enriched)

        # Assertions
        self.assertTrue(result)
        self.assertGreater(pipeline.stats["nodes_merged"], 0)

        # Verify MERGE was used (check query)
        call_args = mock_session.run.call_args
        query = call_args[0][0]
        self.assertIn("MERGE", query)
        self.assertNotIn("CREATE (n:", query.split("MERGE")[0])  # No CREATE before MERGE

        print("✅ Node created with MERGE")
        print(f"   Nodes merged: {pipeline.stats['nodes_merged']}")
        print("   Query contains MERGE: ✓")

    @patch('neo4j.GraphDatabase.driver')
    def test_relationship_extraction(self, mock_driver):
        """Test 5: Relationship extraction"""
        print("\n[TEST 5] Relationship Extraction")

        mock_driver.return_value = MagicMock()

        pipeline = NER11ToNeo4jPipeline()

        # Create enriched entities
        entities = [
            pipeline.enrich_entity({"text": "APT29", "label": "APT_GROUP", "start": 0, "end": 5}),
            pipeline.enrich_entity({"text": "CVE-2020-0688", "label": "CVE", "start": 100, "end": 113}),
            pipeline.enrich_entity({"text": "WellMess", "label": "MALWARE", "start": 200, "end": 208})
        ]

        # Extract relationships
        relationships = pipeline.extract_relationships(entities, "Sample text")

        # Should find relationships like:
        # - ThreatActor EXPLOITS Vulnerability
        # - ThreatActor USES Malware
        self.assertGreater(len(relationships), 0)

        print(f"✅ Extracted {len(relationships)} relationships")
        for source, rel_type, target in relationships:
            print(f"   - {source['specific_instance']} -{rel_type}-> {target['specific_instance']}")

    @patch('neo4j.GraphDatabase.driver')
    def test_validation(self, mock_driver):
        """Test 6: Validation (node count + tier distribution)"""
        print("\n[TEST 6] Validation")

        # Mock validation queries
        mock_session = MagicMock()

        # Mock total node count query
        mock_session.run.return_value.single.return_value = {"total": 1104500}

        # Mock tier distribution query
        tier_results = [
            {"tier": 1, "count": 500},
            {"tier": 2, "count": 1000}
        ]
        mock_session.run.return_value.__iter__ = lambda self: iter(tier_results)

        mock_driver.return_value.session.return_value.__enter__.return_value = mock_session

        pipeline = NER11ToNeo4jPipeline()

        # Run validation
        validation = pipeline.validate_ingestion()

        # Assertions
        self.assertGreater(validation["total_nodes"], 1104066)
        self.assertTrue(validation["node_count_preserved"])
        self.assertTrue(validation["tier2_greater_than_tier1"])

        print("✅ Validation checks")
        print(f"   Total nodes: {validation['total_nodes']:,}")
        print(f"   Node count preserved: {validation['node_count_preserved']}")
        print(f"   Tier 2 > Tier 1: {validation['tier2_greater_than_tier1']}")
        print(f"   Overall passed: {validation['validation_passed']}")

    @patch('neo4j.GraphDatabase.driver')
    @patch('requests.post')
    def test_full_document_processing(self, mock_post, mock_driver):
        """Test 7: Full document processing pipeline"""
        print("\n[TEST 7] Full Document Processing")

        # Mock NER11 API
        mock_post.return_value.json.return_value = {
            "entities": self.mock_entities
        }
        mock_post.return_value.raise_for_status = MagicMock()

        # Mock Neo4j
        mock_session = MagicMock()
        mock_session.run.return_value.single.return_value = {"n": {"name": "test"}}
        mock_driver.return_value.session.return_value.__enter__.return_value = mock_session

        pipeline = NER11ToNeo4jPipeline()

        # Process sample document
        sample_text = """
        APT29 exploited CVE-2020-0688 in Microsoft Exchange Server
        using WellMess malware to target organizations in the United States.
        """

        doc_stats = pipeline.process_document(sample_text, "test_doc")

        # Assertions
        self.assertEqual(doc_stats["entities_extracted"], 5)
        self.assertGreater(doc_stats["nodes_created"], 0)

        print("✅ Document processed successfully")
        print(f"   Entities: {doc_stats['entities_extracted']}")
        print(f"   Nodes: {doc_stats['nodes_created']}")
        print(f"   Relationships: {doc_stats['relationships_created']}")


def run_tests():
    """Run all tests with detailed output"""
    print("="*80)
    print("NER11 TO NEO4J HIERARCHICAL PIPELINE - TEST SUITE")
    print("="*80)

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestNER11ToNeo4jPipeline)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED")
    else:
        print("\n❌ SOME TESTS FAILED")

    print("="*80)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
