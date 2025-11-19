"""
ClassifierAgent Demo
Demonstrates ML-based document classification with Qdrant memory integration
"""

import sys
import yaml
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.classifier_agent import ClassifierAgent


def load_config():
    """Load configuration"""
    config_path = project_root / 'config' / 'main_config.yaml'
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    config['config_dir'] = str(project_root / 'config')
    return config


def demo_training():
    """Demo: Train classification models"""
    print("=" * 60)
    print("DEMO: Training Classification Models")
    print("=" * 60)

    config = load_config()
    agent = ClassifierAgent('demo_classifier', config)

    # Create comprehensive training data
    training_data = {
        'sector': [
            # Energy sector samples
            {'text': 'nuclear reactor safety system emergency shutdown scram control rods', 'label': 'energy'},
            {'text': 'electric power grid substation transformer voltage regulation distribution', 'label': 'energy'},
            {'text': 'solar panel photovoltaic inverter renewable energy generation', 'label': 'energy'},
            {'text': 'wind turbine generator blade pitch control power output', 'label': 'energy'},
            {'text': 'hydroelectric dam turbine water flow power generation', 'label': 'energy'},

            # Water sector samples
            {'text': 'water treatment plant chlorine disinfection filtration process', 'label': 'water'},
            {'text': 'wastewater treatment biological digester aeration tank', 'label': 'water'},
            {'text': 'drinking water distribution pumping station pressure control', 'label': 'water'},
            {'text': 'sewage treatment primary secondary clarifier sludge', 'label': 'water'},
            {'text': 'water quality monitoring ph turbidity chlorine residual', 'label': 'water'},

            # Manufacturing sector samples
            {'text': 'manufacturing assembly line robotic automation plc control', 'label': 'manufacturing'},
            {'text': 'industrial production process quality control scada monitoring', 'label': 'manufacturing'},
            {'text': 'automotive assembly paint booth conveyor robotic welding', 'label': 'manufacturing'},
            {'text': 'pharmaceutical production clean room hvac sterile environment', 'label': 'manufacturing'},
            {'text': 'food processing packaging line temperature control safety', 'label': 'manufacturing'},
        ],
        'subsector': [
            # Energy subsectors
            {'text': 'nuclear power generation reactor control rod position monitoring', 'label': 'nuclear_power'},
            {'text': 'solar photovoltaic installation inverter panel mounting', 'label': 'renewable_energy'},
            {'text': 'electric grid transmission high voltage substation protection', 'label': 'electric_grid'},
            {'text': 'wind farm turbine array control power distribution', 'label': 'renewable_energy'},

            # Water subsectors
            {'text': 'water distribution network pumping station pipeline pressure', 'label': 'water_distribution'},
            {'text': 'wastewater treatment biological process aeration clarification', 'label': 'wastewater_treatment'},
            {'text': 'drinking water purification filtration disinfection storage', 'label': 'water_treatment'},

            # Manufacturing subsectors
            {'text': 'automotive manufacturing paint booth ventilation curing', 'label': 'automotive'},
            {'text': 'pharmaceutical production sterile processing clean room', 'label': 'pharmaceutical'},
            {'text': 'food processing pasteurization packaging quality control', 'label': 'food_processing'},
        ],
        'doctype': [
            # Document types
            {'text': 'technical specification document revision requirements detailed design parameters', 'label': 'technical_spec'},
            {'text': 'user manual operating procedures step by step instructions safety warnings', 'label': 'user_manual'},
            {'text': 'security advisory vulnerability CVE patch update mitigation', 'label': 'security_advisory'},
            {'text': 'maintenance procedure checklist inspection preventive repair schedule', 'label': 'maintenance_guide'},
            {'text': 'installation guide setup configuration commissioning steps', 'label': 'installation_guide'},
            {'text': 'compliance report regulatory audit findings certification requirements', 'label': 'compliance_report'},
            {'text': 'system architecture overview component diagram integration design', 'label': 'architecture_doc'},
            {'text': 'troubleshooting guide diagnostic procedures error codes solutions', 'label': 'troubleshooting_guide'},
            {'text': 'training materials course curriculum exercises certification', 'label': 'training_material'},
            {'text': 'release notes version changelog new features bug fixes', 'label': 'release_notes'},
        ]
    }

    print(f"\nTraining data summary:")
    print(f"  Sectors: {len(training_data['sector'])} samples")
    print(f"  Subsectors: {len(training_data['subsector'])} samples")
    print(f"  Document types: {len(training_data['doctype'])} samples")

    print("\nTraining models (this may take a moment)...")
    saved_paths = agent.train_models(training_data)

    print("\n✓ Models trained and saved:")
    for model_type, path in saved_paths.items():
        print(f"  {model_type}: {path}")

    return agent


def demo_classification(agent):
    """Demo: Classify documents"""
    print("\n" + "=" * 60)
    print("DEMO: Document Classification")
    print("=" * 60)

    test_documents = [
        {
            'name': 'Nuclear Safety System',
            'content': """
            Nuclear Reactor Emergency Shutdown System (SCRAM)

            This technical specification describes the automatic reactor protection system
            for pressurized water reactors. The system continuously monitors critical
            parameters including reactor pressure, coolant temperature, and neutron flux
            levels. Upon detection of unsafe conditions, control rods are rapidly inserted
            into the reactor core to halt the nuclear chain reaction.

            The safety system employs redundant sensors with 2-out-of-3 voting logic to
            prevent spurious trips while ensuring reliable emergency shutdown capability.
            Response time from trip initiation to full control rod insertion is less than
            2 seconds.
            """
        },
        {
            'name': 'Water Treatment Manual',
            'content': """
            Municipal Water Treatment Plant Operating Manual

            This user manual provides comprehensive operating procedures for the
            chlorination and filtration systems. Operators must monitor water quality
            parameters including pH, turbidity, and chlorine residual levels throughout
            the treatment process.

            Daily startup procedures:
            1. Check all pump operation and pressure readings
            2. Verify chlorine feed rate and residual levels
            3. Inspect filter backwash cycle timing
            4. Record all parameters in the operations log

            Emergency shutdown procedures are detailed in Section 7.
            """
        },
        {
            'name': 'SCADA Vulnerability Advisory',
            'content': """
            Security Advisory: SCADA System Vulnerability CVE-2024-12345

            A critical vulnerability has been identified in industrial control system
            SCADA software affecting manufacturing facilities. The vulnerability allows
            unauthorized remote access to process control systems.

            Affected Systems:
            - Manufacturing automation controllers
            - Process monitoring systems
            - Industrial network devices

            Recommended Mitigation:
            - Apply security patch version 3.2.1 immediately
            - Implement network segmentation
            - Enable authentication logging
            - Review access control policies
            """
        }
    ]

    for doc in test_documents:
        print(f"\n{'─' * 60}")
        print(f"Document: {doc['name']}")
        print(f"{'─' * 60}")

        result = agent.classify_document(
            markdown_content=doc['content'],
            metadata={'name': doc['name']}
        )

        print(f"\nClassification Result:")
        print(f"  Sector: {result['sector']}")
        print(f"    Confidence: {result['sector_confidence']:.3f}")

        print(f"\n  Subsector: {result['subsector']}")
        print(f"    Confidence: {result['subsector_confidence']:.3f}")

        print(f"\n  Document Type: {result['document_type']}")
        print(f"    Confidence: {result['doctype_confidence']:.3f}")

        print(f"\n  Overall Confidence: {result['overall_confidence']:.3f}")

        if result['auto_classified']:
            print(f"  Status: ✓ Auto-classified (high confidence)")
        else:
            print(f"  Status: ⚠ Requires interactive review (low confidence)")

        # Show alternative predictions
        print(f"\n  Alternative Predictions:")
        if 'sector_confidence' in result:
            print(f"    (Top sector alternatives would be shown in production)")


def demo_learning(agent):
    """Demo: Learning from corrections"""
    print("\n" + "=" * 60)
    print("DEMO: Learning from User Corrections")
    print("=" * 60)

    # Simulate a document that was classified incorrectly
    doc_text = """
    Hydroelectric Dam Control System

    This document describes the automated control system for water flow
    management at hydroelectric generation facilities. The system monitors
    reservoir levels, turbine operation, and power generation output.
    """

    print("\nOriginal classification...")
    result = agent.classify_document(doc_text, metadata={'demo': True})

    print(f"  Predicted Sector: {result['sector']}")
    print(f"  Predicted Subsector: {result['subsector']}")

    # User provides correction
    corrected = {
        'sector': 'energy',  # Was perhaps classified as 'water'
        'subsector': 'hydroelectric',
        'document_type': 'technical_spec'
    }

    print(f"\nUser correction:")
    print(f"  Correct Sector: {corrected['sector']}")
    print(f"  Correct Subsector: {corrected['subsector']}")

    # Learn from correction
    success = agent.learn_from_correction(doc_text, corrected)

    if success:
        print(f"\n✓ Correction stored in memory for future reference")
    else:
        print(f"\n⚠ Memory storage not available (Qdrant disabled)")

    print(f"\nAgent will now use this correction to improve future classifications")


def demo_statistics(agent):
    """Demo: View agent statistics"""
    print("\n" + "=" * 60)
    print("DEMO: Agent Statistics")
    print("=" * 60)

    stats = agent.get_stats()

    print(f"\nClassification Statistics:")
    print(f"  Total Documents Classified: {stats['total_classified']}")
    print(f"  Auto-Classified (high confidence): {stats['auto_classified']}")
    print(f"  Interactive Classifications: {stats['interactive_classified']}")
    print(f"  User Corrections Learned: {stats['corrections_learned']}")

    print(f"\nMemory System:")
    mem_stats = stats['memory_stats']
    if mem_stats.get('enabled'):
        print(f"  Status: ✓ Enabled")
        print(f"  Stored Classifications: {mem_stats.get('total_classifications', 0)}")
    else:
        print(f"  Status: ⚠ Disabled (enable in config for learning features)")


def main():
    """Run all demos"""
    print("\n" + "=" * 60)
    print("ClassifierAgent Demo")
    print("ML-based Document Classification with Memory")
    print("=" * 60)

    # Train models
    agent = demo_training()

    # Classify documents
    demo_classification(agent)

    # Learn from corrections
    demo_learning(agent)

    # Show statistics
    demo_statistics(agent)

    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print("\nNext Steps:")
    print("  1. Train models with real document corpus")
    print("  2. Enable Qdrant for memory/learning features")
    print("  3. Integrate with document processing pipeline")
    print("  4. Tune confidence thresholds for your use case")


if __name__ == '__main__':
    main()
