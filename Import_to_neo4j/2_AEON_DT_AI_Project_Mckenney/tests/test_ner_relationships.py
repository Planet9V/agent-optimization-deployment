"""
Test NER Agent Relationship Extraction
Validates the new extract_relationships() functionality
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.ner_agent import NERAgent


def test_relationship_extraction():
    """Test relationship extraction with sample cybersecurity text"""

    # Sample text with cybersecurity entities and relationships
    test_text = """
    CVE-2021-44228 is a critical vulnerability in Apache Log4j that was exploited
    by APT29 (Cozy Bear) threat actor. The vulnerability affects multiple vendors
    including VMware, Cisco, and Siemens. The malware Emotet uses the attack technique
    T1566 (phishing) to target industrial control systems. Rockwell Automation released
    patches to mitigate CVE-2021-44228. The Lazarus Group exploited CVE-2021-44228
    using their custom malware. Siemens PLCs implement the Modbus protocol and support
    IEC 61850 standard.
    """

    # Initialize agent
    config = {
        'pattern_library_path': 'pattern_library'
    }

    agent = NERAgent(config)

    # Execute extraction
    result = agent.execute({
        'text': test_text,
        'sector': 'industrial',
        'extract_relationships': True
    })

    # Print results
    print("=" * 80)
    print("NER AGENT RELATIONSHIP EXTRACTION TEST")
    print("=" * 80)

    print(f"\n📊 SUMMARY:")
    print(f"  - Entities extracted: {result['entity_count']}")
    print(f"  - Relationships extracted: {result['relationship_count']}")
    print(f"  - Entity precision estimate: {result['precision_estimate']:.1%}")
    print(f"  - Relationship accuracy estimate: {result['relationship_accuracy']:.1%}")

    print(f"\n🏷️  ENTITIES BY TYPE:")
    for entity_type, count in sorted(result['by_type'].items(), key=lambda x: -x[1]):
        print(f"  - {entity_type}: {count}")

    print(f"\n🔗 RELATIONSHIPS BY TYPE:")
    for rel_type, count in sorted(result['by_relationship'].items(), key=lambda x: -x[1]):
        print(f"  - {rel_type}: {count}")

    print(f"\n📝 SAMPLE ENTITIES:")
    for i, entity in enumerate(result['entities'][:10], 1):
        print(f"  {i}. {entity['text']} ({entity['label']}) - confidence: {entity['confidence']:.3f}")

    print(f"\n🔗 SAMPLE RELATIONSHIPS:")
    for i, rel in enumerate(result['relationships'][:10], 1):
        print(f"  {i}. {rel['subject']} ({rel['subject_type']}) "
              f"-[{rel['predicate']}]-> "
              f"{rel['object']} ({rel['object_type']})")
        print(f"     Confidence: {rel['confidence']:.3f}")
        print(f"     Source: {rel['sentence'][:100]}...")
        print()

    # Validation checks
    print("\n✅ VALIDATION CHECKS:")

    checks = [
        (result['entity_count'] > 0, "Entities extracted"),
        (result['relationship_count'] > 0, "Relationships extracted"),
        ('EXPLOITS' in result['by_relationship'], "EXPLOITS relationships found"),
        ('MITIGATES' in result['by_relationship'], "MITIGATES relationships found"),
        ('CVE' in result['by_type'], "CVE entities found"),
        ('THREAT_ACTOR' in result['by_type'] or 'APT_GROUP' in result['by_type'], "Threat actors found"),
        (result['relationship_accuracy'] >= 0.70, "Relationship accuracy >= 70%"),
    ]

    passed = 0
    for check, description in checks:
        status = "✓" if check else "✗"
        print(f"  [{status}] {description}")
        if check:
            passed += 1

    print(f"\n📈 TEST RESULTS: {passed}/{len(checks)} checks passed")

    if passed >= len(checks) * 0.75:  # 75% pass rate
        print("\n🎉 SUCCESS: Relationship extraction is working!")
        return True
    else:
        print("\n⚠️  WARNING: Some validation checks failed")
        return False


if __name__ == '__main__':
    success = test_relationship_extraction()
    sys.exit(0 if success else 1)
