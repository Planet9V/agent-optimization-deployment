#!/usr/bin/env python3
"""
End-to-End Pipeline Validation Test
Tests classifier_agent.py and ner_agent.py with real document
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.classifier_agent import ClassifierAgent
from agents.ner_agent import NERAgent
import json
from datetime import datetime

def main():
    print("\n" + "="*80)
    print("E2E PIPELINE VALIDATION TEST")
    print("Testing: Classifier Agent → NER Agent")
    print("="*80)

    # Test Document
    test_doc = """
    The Siemens S7-1500 PLC system controls ABB variable frequency drives
    through Profinet protocol. The system operates at 150 PSI and 2500 GPM,
    meeting IEC 61508 SIL 2 safety requirements. Foundation Fieldbus connects
    to Yokogawa EJA transmitters at field level (Purdue L0).

    The Schneider Electric Unity Pro software configures the PLC ladder logic,
    while the Honeywell DCS provides supervisory control at L3. OPC UA server
    enables communication between the DCS and enterprise MES system at L4.

    Operating parameters: 480V 60Hz motor, 250 HP rating, 85 kW power consumption.
    Ambient conditions: 72°F, 45% RH. Maximum operating pressure: 175 PSI.
    """

    # Step 1: Classifier Agent
    print("\n[STEP 1] Running Classifier Agent...")
    classifier = ClassifierAgent(
        name='e2e_classifier',
        config={'classification': {'model_paths': {}}}
    )

    try:
        class_result = classifier.run({
            'text': test_doc,
            'metadata': {'source': 'e2e_test'}
        })

        print(f"✅ Classification completed")
        print(f"   Sector: {class_result.get('sector', 'N/A')}")
        print(f"   Subsector: {class_result.get('subsector', 'N/A')}")
        print(f"   Confidence: {class_result.get('confidence', 0):.2f}")

    except Exception as e:
        print(f"❌ Classifier failed: {e}")
        return False

    # Step 2: NER Agent
    print("\n[STEP 2] Running NER Agent...")
    ner = NERAgent(config={'pattern_library_path': 'pattern_library'})

    try:
        ner_result = ner.run({
            'text': test_doc,
            'sector': class_result.get('sector', 'industrial')
        })

        print(f"✅ NER extraction completed")
        print(f"   Total entities: {ner_result['entity_count']}")
        print(f"   Precision estimate: {ner_result['precision_estimate']:.1%}")

        # Show entity breakdown
        print(f"\n   Entities by type:")
        for ent_type, count in ner_result['by_type'].items():
            print(f"     • {ent_type}: {count}")

        # Show sample entities
        print(f"\n   Sample entities:")
        for ent in ner_result['entities'][:10]:
            print(f"     • {ent['text']:30s} [{ent['label']:15s}] ({ent['source']})")

    except Exception as e:
        print(f"❌ NER failed: {e}")
        return False

    # Step 3: Output Results
    results = {
        'timestamp': datetime.now().isoformat(),
        'test_status': 'SUCCESS',
        'classifier_output': {
            'sector': class_result.get('sector'),
            'subsector': class_result.get('subsector'),
            'confidence': class_result.get('confidence')
        },
        'ner_output': {
            'entity_count': ner_result['entity_count'],
            'precision_estimate': ner_result['precision_estimate'],
            'by_type': ner_result['by_type'],
            'sample_entities': [
                {
                    'text': e['text'],
                    'label': e['label'],
                    'confidence': e['confidence']
                } for e in ner_result['entities'][:20]
            ]
        }
    }

    output_file = '/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/claudedocs/e2e_test_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Results saved to: {output_file}")
    print("\n" + "="*80)
    print("E2E PIPELINE TEST COMPLETED SUCCESSFULLY")
    print("="*80)

    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
