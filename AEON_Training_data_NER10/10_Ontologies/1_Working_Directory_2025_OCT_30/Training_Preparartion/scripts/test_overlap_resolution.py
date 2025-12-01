#!/usr/bin/env python3
"""
Test script for entity overlap resolution
Tests the _resolve_overlapping_entities method with 5 test cases
"""
import sys
sys.path.insert(0, '/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/scripts')
from ner_training_pipeline import NERTrainingPipeline

# Test cases
test_cases = [
    # Test 1: Substring - longer wins
    {
        'entities': [(0, 7, 'PROTOCOL'), (0, 11, 'EQUIPMENT')],  # AES-128 vs AES-128-GCM
        'expected': [(0, 11, 'EQUIPMENT')],
        'name': 'Substring - EQUIPMENT beats PROTOCOL (longer)'
    },
    # Test 2: Duplicate - priority wins
    {
        'entities': [(0, 18, 'SECURITY'), (0, 18, 'MITIGATION')],  # Penetration testing
        'expected': [(0, 18, 'SECURITY')],
        'name': 'Duplicate - SECURITY beats MITIGATION (higher priority)'
    },
    # Test 3: Multiple overlaps
    {
        'entities': [(0, 7, 'VENDOR'), (0, 11, 'EQUIPMENT'), (0, 15, 'EQUIPMENT')],
        'expected': [(0, 15, 'EQUIPMENT')],
        'name': 'Multiple overlaps - longest wins'
    },
    # Test 4: No overlaps
    {
        'entities': [(0, 5, 'VENDOR'), (10, 15, 'EQUIPMENT')],
        'expected': [(0, 5, 'VENDOR'), (10, 15, 'EQUIPMENT')],
        'name': 'No overlaps - keep both'
    },
    # Test 5: Adjacent entities
    {
        'entities': [(0, 7, 'VENDOR'), (7, 15, 'EQUIPMENT')],
        'expected': [(0, 7, 'VENDOR'), (7, 15, 'EQUIPMENT')],
        'name': 'Adjacent - keep both'
    }
]

pipeline = NERTrainingPipeline('/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/Data Pipeline Builder/PATTERN_EXTRACTION_VALIDATION_RESULTS.json')

print("Testing Overlap Resolution\n" + "="*60)
passed = 0
failed = 0

for test in test_cases:
    result = pipeline._resolve_overlapping_entities(test['entities'])
    success = result == test['expected']

    if success:
        passed += 1
        print(f"✅ {test['name']}")
    else:
        failed += 1
        print(f"❌ {test['name']}")
        print(f"   Input: {test['entities']}")
        print(f"   Expected: {test['expected']}")
        print(f"   Got: {result}")

print(f"\n{'='*60}")
print(f"Results: {passed}/{len(test_cases)} passed, {failed} failed")

if failed == 0:
    print("✅ ALL TESTS PASSED - Resolver working correctly")
else:
    print("❌ SOME TESTS FAILED - Review implementation")
