"""
Test NER Agent - Pattern-Neural Hybrid NER
Demonstrates actual working entity extraction
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.ner_agent import NERAgent


def test_pattern_ner():
    """Test pattern-based NER extraction"""
    print("\n" + "="*80)
    print("TEST 1: Pattern-Based NER (High Precision)")
    print("="*80)

    config = {
        'pattern_library_path': 'pattern_library'
    }

    agent = NERAgent(config)

    test_text = """
    The Siemens S7-1500 PLC communicates with the Rockwell Automation HMI via Modbus TCP.
    The system operates at 150 PSI and 2500 GPM, meeting IEC 61508 SIL 2 requirements.
    Foundation Fieldbus connects to Yokogawa transmitters at the field level (L0).
    """

    result = agent.run({
        'text': test_text,
        'sector': 'industrial'
    })

    print(f"\nExtracted {result['entity_count']} entities:")
    for ent in result['entities']:
        print(f"  - {ent['text']:30s} [{ent['label']:15s}] confidence={ent['confidence']:.2f} source={ent['source']}")

    print(f"\nBy Type:")
    for ent_type, count in result['by_type'].items():
        print(f"  {ent_type}: {count}")

    print(f"\nPrecision Estimate: {result['precision_estimate']:.1%}")


def test_multiple_sectors():
    """Test entity extraction across multiple sectors"""
    print("\n" + "="*80)
    print("TEST 2: Multi-Sector Extraction")
    print("="*80)

    config = {}
    agent = NERAgent(config)

    test_cases = [
        ("industrial", "ABB drives controlled by Schneider Electric PLC using Profinet protocol."),
        ("industrial", "Safety system meets IEC 61511 SIL 3 with redundant controllers at L1."),
        ("industrial", "OPC UA server bridges Honeywell DCS with enterprise MES system at L4."),
    ]

    for sector, text in test_cases:
        result = agent.run({'text': text, 'sector': sector})
        print(f"\n[{sector}] Extracted {result['entity_count']} entities from: {text[:60]}...")
        for ent in result['entities']:
            print(f"  - {ent['text']:25s} [{ent['label']:12s}]")


def test_measurement_extraction():
    """Test measurement and unit extraction"""
    print("\n" + "="*80)
    print("TEST 3: Measurement and Unit Extraction")
    print("="*80)

    config = {}
    agent = NERAgent(config)

    test_text = """
    Operating conditions: 85.5 PSI, 1200 GPM, 72°F ambient temperature.
    Motor rating: 250 HP, 480V, 60Hz.
    Pump delivers 850 GPM at 125 PSI with 85 kW power consumption.
    """

    result = agent.run({
        'text': test_text,
        'sector': 'industrial'
    })

    print(f"\nExtracted {result['entity_count']} entities:")
    measurements = [e for e in result['entities'] if e['label'] == 'MEASUREMENT']
    print(f"\nMeasurements found: {len(measurements)}")
    for ent in measurements:
        print(f"  - {ent['text']}")


def test_protocol_and_standards():
    """Test protocol and standard extraction"""
    print("\n" + "="*80)
    print("TEST 4: Protocol and Standards Extraction")
    print("="*80)

    config = {}
    agent = NERAgent(config)

    test_text = """
    Network architecture:
    - Level 0-1: Foundation Fieldbus and HART devices
    - Level 2: Modbus TCP/IP and EtherCAT for motion control
    - Level 3: OPC UA and BACnet for building automation
    - Standards compliance: IEC 62443, IEEE 802.11, ISO 27001
    """

    result = agent.run({
        'text': test_text,
        'sector': 'industrial'
    })

    print(f"\nExtracted {result['entity_count']} entities:")

    protocols = [e for e in result['entities'] if e['label'] == 'PROTOCOL']
    standards = [e for e in result['entities'] if e['label'] == 'STANDARD']

    print(f"\nProtocols found: {len(protocols)}")
    for ent in protocols:
        print(f"  - {ent['text']}")

    print(f"\nStandards found: {len(standards)}")
    for ent in standards:
        print(f"  - {ent['text']}")


def test_statistics():
    """Test statistics tracking"""
    print("\n" + "="*80)
    print("TEST 5: Statistics and Performance")
    print("="*80)

    config = {}
    agent = NERAgent(config)

    # Run multiple extractions
    test_texts = [
        "Siemens PLC with Modbus protocol at 100 PSI",
        "Rockwell HMI meets IEC 61508 SIL 2",
        "ABB VFD controlled via Profinet at L1",
        "Honeywell transmitter using HART protocol",
        "Yokogawa DCS with Foundation Fieldbus"
    ]

    for text in test_texts:
        agent.run({'text': text, 'sector': 'industrial'})

    stats = agent.get_stats()

    print(f"\nStatistics after {len(test_texts)} extractions:")
    print(f"  Total extractions: {stats['total_extractions']}")
    print(f"  Pattern entities: {stats['total_pattern_entities']}")
    print(f"  Neural entities: {stats['total_neural_entities']}")
    print(f"  Merged entities: {stats['total_merged_entities']}")
    print(f"  Average precision: {stats['average_precision']:.1%}")
    print(f"  spaCy available: {stats['spacy_available']}")
    print(f"  Model loaded: {stats['model_loaded']}")

    print(f"\nEntities by type:")
    for ent_type, count in sorted(stats['entities_by_type'].items(), key=lambda x: -x[1]):
        print(f"  {ent_type:15s}: {count}")


def test_real_document():
    """Test with realistic technical document text"""
    print("\n" + "="*80)
    print("TEST 6: Real Document Extraction")
    print("="*80)

    config = {}
    agent = NERAgent(config)

    document_text = """
    ## Process Control System Architecture

    ### Level 0-1: Field Devices
    The field instrumentation consists of Emerson pressure transmitters (0-300 PSI)
    and Yokogawa temperature sensors (32-212°F) connected via Foundation Fieldbus.
    Flow meters measure 0-5000 GPM with ±0.5% accuracy.

    ### Level 2: Control Layer
    Redundant Siemens S7-1500 PLCs provide SIL 2 control functionality per IEC 61508.
    Communication uses Profinet IRT with 1ms cycle time. ABB drives control pumps
    rated at 500 HP each, operating at 480V 60Hz.

    ### Level 3: Supervisory Control
    Rockwell Automation FactoryTalk SE SCADA system monitors 2500+ I/O points.
    OPC UA server bridges to Honeywell Experion DCS for coordinated control.
    Historian stores data with 1-second resolution meeting FDA 21 CFR Part 11.

    ### Network Security
    Defense-in-depth architecture complies with IEC 62443 and NIST SP 800-82.
    Firewall rules enforce Purdue Model segmentation between L1-L4.
    """

    result = agent.run({
        'text': document_text,
        'sector': 'industrial'
    })

    print(f"\nDocument Analysis:")
    print(f"  Total entities extracted: {result['entity_count']}")
    print(f"  Precision estimate: {result['precision_estimate']:.1%}")

    print(f"\nEntity Distribution:")
    for ent_type, count in sorted(result['by_type'].items(), key=lambda x: -x[1]):
        print(f"  {ent_type:15s}: {count:3d}")

    print(f"\nSample Entities:")
    by_label = {}
    for ent in result['entities']:
        label = ent['label']
        if label not in by_label:
            by_label[label] = []
        by_label[label].append(ent['text'])

    for label in ['VENDOR', 'PROTOCOL', 'STANDARD', 'COMPONENT', 'MEASUREMENT']:
        if label in by_label:
            print(f"\n  {label}:")
            for text in by_label[label][:5]:  # Show first 5
                print(f"    - {text}")


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("NER AGENT - PATTERN-NEURAL HYBRID TESTING")
    print("Target: 92-96% Combined Precision")
    print("="*80)

    test_pattern_ner()
    test_multiple_sectors()
    test_measurement_extraction()
    test_protocol_and_standards()
    test_statistics()
    test_real_document()

    print("\n" + "="*80)
    print("ALL TESTS COMPLETED")
    print("="*80)


if __name__ == "__main__":
    main()
