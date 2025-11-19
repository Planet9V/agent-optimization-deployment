"""
Test ClassifierAgent Implementation
Verifies ML-based document classification functionality
"""

import unittest
import os
import sys
import yaml
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.classifier_agent import ClassifierAgent


class TestClassifierAgent(unittest.TestCase):
    """Test cases for ClassifierAgent"""

    @classmethod
    def setUpClass(cls):
        """Set up test configuration"""
        # Load actual config
        config_path = project_root / 'config' / 'main_config.yaml'
        with open(config_path, 'r') as f:
            cls.config = yaml.safe_load(f)

        # Add config directory path
        cls.config['config_dir'] = str(project_root / 'config')

        # Create test agent
        cls.agent = ClassifierAgent('test_classifier', cls.config)

    def test_01_initialization(self):
        """Test agent initialization"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.name, 'test_classifier')
        self.assertEqual(self.agent.confidence_threshold, 0.75)
        self.assertTrue(self.agent.interactive_mode)

    def test_02_config_loading(self):
        """Test configuration loading"""
        self.assertIsNotNone(self.agent.sectors_config)
        self.assertIn('sectors', self.agent.sectors_config)

        # Check sectors loaded
        sectors = self.agent.sectors_config['sectors']
        self.assertGreater(len(sectors), 0)
        self.assertIn('energy', sectors)
        self.assertIn('water', sectors)

    def test_03_memory_manager_init(self):
        """Test memory manager initialization"""
        self.assertIsNotNone(self.agent.memory_manager)

        # Check memory stats
        stats = self.agent.memory_manager.get_stats()
        self.assertIn('enabled', stats)

    def test_04_model_paths(self):
        """Test model path configuration"""
        self.assertTrue(self.agent.sector_model_path.endswith('.pkl'))
        self.assertTrue(self.agent.subsector_model_path.endswith('.pkl'))
        self.assertTrue(self.agent.doctype_model_path.endswith('.pkl'))

    def test_05_train_models_with_sample_data(self):
        """Test model training with sample data"""
        # Create sample training data
        training_data = {
            'sector': [
                {'text': 'nuclear reactor safety system scram emergency shutdown', 'label': 'energy'},
                {'text': 'water treatment plant chlorine disinfection process', 'label': 'water'},
                {'text': 'manufacturing assembly line robotic automation plc', 'label': 'manufacturing'},
                {'text': 'electric power grid substation transformer voltage', 'label': 'energy'},
                {'text': 'wastewater treatment filtration biological process', 'label': 'water'},
                {'text': 'industrial production process quality control scada', 'label': 'manufacturing'},
            ],
            'subsector': [
                {'text': 'nuclear power generation reactor control', 'label': 'nuclear_power'},
                {'text': 'water distribution network pumping station', 'label': 'water_distribution'},
                {'text': 'automotive manufacturing paint booth ventilation', 'label': 'automotive'},
                {'text': 'solar panel installation photovoltaic inverter', 'label': 'renewable_energy'},
                {'text': 'sewage treatment biological digester', 'label': 'wastewater'},
                {'text': 'pharmaceutical production clean room hvac', 'label': 'pharmaceutical'},
            ],
            'doctype': [
                {'text': 'technical specification document revision 3.2 requirements', 'label': 'technical_spec'},
                {'text': 'user manual operating procedures safety instructions', 'label': 'user_manual'},
                {'text': 'security advisory vulnerability CVE patch update', 'label': 'security_advisory'},
                {'text': 'maintenance procedure checklist inspection steps', 'label': 'maintenance_guide'},
                {'text': 'installation guide setup configuration steps', 'label': 'installation_guide'},
                {'text': 'compliance report regulatory audit findings', 'label': 'compliance_report'},
            ]
        }

        # Train models
        saved_paths = self.agent.train_models(training_data)

        # Verify models were saved
        self.assertIn('sector', saved_paths)
        self.assertIn('subsector', saved_paths)
        self.assertIn('doctype', saved_paths)

        # Check files exist
        self.assertTrue(os.path.exists(saved_paths['sector']))
        self.assertTrue(os.path.exists(saved_paths['subsector']))
        self.assertTrue(os.path.exists(saved_paths['doctype']))

    def test_06_load_models(self):
        """Test loading trained models"""
        model_paths = {
            'sector': self.agent.sector_model_path,
            'subsector': self.agent.subsector_model_path,
            'doctype': self.agent.doctype_model_path
        }

        success = self.agent.load_models(model_paths)

        # If models were trained in previous test
        if os.path.exists(self.agent.sector_model_path):
            self.assertTrue(success)
            self.assertIsNotNone(self.agent.sector_classifier)
            self.assertIsNotNone(self.agent.sector_vectorizer)
            self.assertIsNotNone(self.agent.sector_encoder)

    def test_07_classify_document(self):
        """Test document classification"""
        # Skip if models not trained
        if not self.agent.sector_classifier:
            self.skipTest("Models not trained yet")

        # Test document
        test_doc = """
        Nuclear Reactor Safety System

        This document describes the emergency shutdown system (SCRAM) for a pressurized
        water reactor. The system monitors critical parameters including reactor pressure,
        temperature, and neutron flux. In case of unsafe conditions, control rods are
        automatically inserted to halt the nuclear reaction.

        The safety system integrates with redundant sensors and uses a 2-out-of-3 voting
        logic to prevent spurious trips while ensuring rapid response to genuine emergencies.
        """

        metadata = {'filename': 'test_reactor_doc.md', 'source': 'test'}

        # Classify
        result = self.agent.classify_document(test_doc, metadata)

        # Verify result structure
        self.assertIn('sector', result)
        self.assertIn('sector_confidence', result)
        self.assertIn('subsector', result)
        self.assertIn('subsector_confidence', result)
        self.assertIn('document_type', result)
        self.assertIn('doctype_confidence', result)
        self.assertIn('overall_confidence', result)
        self.assertIn('auto_classified', result)

        # Check confidence values are in valid range
        self.assertGreaterEqual(result['sector_confidence'], 0.0)
        self.assertLessEqual(result['sector_confidence'], 1.0)
        self.assertGreaterEqual(result['overall_confidence'], 0.0)
        self.assertLessEqual(result['overall_confidence'], 1.0)

        print(f"\nClassification Result:")
        print(f"  Sector: {result['sector']} (confidence: {result['sector_confidence']:.3f})")
        print(f"  Subsector: {result['subsector']} (confidence: {result['subsector_confidence']:.3f})")
        print(f"  Doc Type: {result['document_type']} (confidence: {result['doctype_confidence']:.3f})")
        print(f"  Overall: {result['overall_confidence']:.3f}")
        print(f"  Auto-classified: {result['auto_classified']}")

    def test_08_confidence_scoring(self):
        """Test confidence score retrieval"""
        if not self.agent.sector_classifier:
            self.skipTest("Models not trained yet")

        test_text = "nuclear reactor safety system emergency shutdown"

        confidence = self.agent.get_confidence_score(
            test_text,
            'energy',
            'sector'
        )

        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)

    def test_09_learn_from_correction(self):
        """Test learning from user corrections"""
        test_doc = "Sample document about water treatment"

        corrected_classification = {
            'sector': 'water',
            'subsector': 'water_treatment',
            'document_type': 'technical_spec'
        }

        # This will work even if Qdrant is not enabled (returns False gracefully)
        result = self.agent.learn_from_correction(test_doc, corrected_classification)

        # Just verify it doesn't crash
        self.assertIsInstance(result, bool)

    def test_10_execute_method(self):
        """Test BaseAgent execute method"""
        if not self.agent.sector_classifier:
            self.skipTest("Models not trained yet")

        input_data = {
            'text': 'water treatment chlorine disinfection process',
            'metadata': {'test': True}
        }

        result = self.agent.run(input_data)

        # Verify result structure
        self.assertIsNotNone(result)
        if result:  # If classification succeeded
            self.assertIn('sector', result)
            self.assertIn('overall_confidence', result)

    def test_11_get_stats(self):
        """Test statistics retrieval"""
        stats = self.agent.get_stats()

        self.assertIn('name', stats)
        self.assertIn('total_classified', stats)
        self.assertIn('auto_classified', stats)
        self.assertIn('interactive_classified', stats)
        self.assertIn('memory_stats', stats)

        print(f"\nAgent Statistics:")
        print(f"  Total classified: {stats['total_classified']}")
        print(f"  Auto-classified: {stats['auto_classified']}")
        print(f"  Interactive: {stats['interactive_classified']}")
        print(f"  Corrections learned: {stats['corrections_learned']}")

    def test_12_memory_search(self):
        """Test memory search for similar documents"""
        # This tests the integration even if Qdrant is not enabled
        test_text = "nuclear power plant reactor control system"

        similar = self.agent.memory_manager.search_similar(test_text, limit=3)

        # Should return empty list if memory not enabled, or list of results
        self.assertIsInstance(similar, list)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
