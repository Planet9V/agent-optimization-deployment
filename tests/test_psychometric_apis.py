"""
Test suite for Psychometric APIs
Tests all 8 endpoints against actual Neo4j data
"""

import requests
import json
from typing import Dict, Any

# API Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v2/psychometrics"

def print_test_result(endpoint: str, status: int, data: Any, expected_status: int = 200):
    """Print formatted test results"""
    success = status == expected_status
    symbol = "✅" if success else "❌"
    print(f"\n{symbol} {endpoint}")
    print(f"   Status: {status} (expected {expected_status})")
    if isinstance(data, dict):
        print(f"   Keys: {list(data.keys())}")
    elif isinstance(data, list):
        print(f"   Count: {len(data)}")
        if data and len(data) > 0:
            print(f"   Sample: {data[0] if isinstance(data[0], str) else list(data[0].keys())}")
    return success

def test_1_list_traits():
    """Test GET /api/v2/psychometrics/traits"""
    url = f"{BASE_URL}{API_PREFIX}/traits"
    print(f"\n{'='*60}")
    print("TEST 1: List All Psychological Traits")
    print(f"{'='*60}")

    try:
        response = requests.get(url, params={"limit": 10})
        data = response.json()
        success = print_test_result("GET /traits", response.status_code, data)

        if success and isinstance(data, list):
            print(f"\n   Retrieved {len(data)} traits")
            if data:
                print(f"   First trait: {data[0]['name']}")

        return success
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_2_get_trait_details():
    """Test GET /api/v2/psychometrics/traits/{trait_id}"""
    url = f"{BASE_URL}{API_PREFIX}/traits"
    print(f"\n{'='*60}")
    print("TEST 2: Get Trait Details")
    print(f"{'='*60}")

    try:
        # First get a trait ID
        list_response = requests.get(url, params={"limit": 1})
        traits = list_response.json()

        if not traits:
            print("❌ No traits available for testing")
            return False

        trait_id = traits[0]['trait_id']
        print(f"   Testing with trait: {trait_id}")

        # Get trait details
        detail_url = f"{url}/{trait_id}"
        response = requests.get(detail_url)
        data = response.json()
        success = print_test_result(f"GET /traits/{trait_id}", response.status_code, data)

        if success:
            print(f"   Trait: {data.get('name')}")
            print(f"   Actors: {data.get('actor_count', 0)}")

        return success
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_3_get_actor_profile():
    """Test GET /api/v2/psychometrics/actors/{actor_id}/profile"""
    url = f"{BASE_URL}{API_PREFIX}/actors"
    print(f"\n{'='*60}")
    print("TEST 3: Get Actor Personality Profile")
    print(f"{'='*60}")

    try:
        # Use a known actor or get one from traits
        actor_id = "APT28"  # Common threat actor

        profile_url = f"{url}/{actor_id}/profile"
        response = requests.get(profile_url)
        data = response.json()
        success = print_test_result(f"GET /actors/{actor_id}/profile", response.status_code, data)

        if success:
            print(f"   Actor: {data.get('actor_name')}")
            print(f"   Traits: {len(data.get('traits', []))}")
            print(f"   Dominant: {data.get('dominant_traits', [])[:3]}")

        return success
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_4_get_actors_by_trait():
    """Test GET /api/v2/psychometrics/actors/by-trait/{trait_id}"""
    url = f"{BASE_URL}{API_PREFIX}/actors/by-trait"
    print(f"\n{'='*60}")
    print("TEST 4: Get Actors by Trait")
    print(f"{'='*60}")

    try:
        # Get a trait first
        traits_response = requests.get(f"{BASE_URL}{API_PREFIX}/traits", params={"limit": 1})
        traits = traits_response.json()

        if not traits:
            print("❌ No traits available")
            return False

        trait_id = traits[0]['trait_id']
        print(f"   Testing with trait: {trait_id}")

        actors_url = f"{url}/{trait_id}"
        response = requests.get(actors_url, params={"limit": 10})
        data = response.json()
        success = print_test_result(f"GET /actors/by-trait/{trait_id}", response.status_code, data)

        if success and isinstance(data, list):
            print(f"   Found {len(data)} actors with this trait")
            if data:
                print(f"   Sample actor: {data[0].get('actor_name')}")

        return success
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_5_list_biases():
    """Test GET /api/v2/psychometrics/biases"""
    url = f"{BASE_URL}{API_PREFIX}/biases"
    print(f"\n{'='*60}")
    print("TEST 5: List Cognitive Biases")
    print(f"{'='*60}")

    try:
        response = requests.get(url, params={"limit": 10})
        data = response.json()
        success = print_test_result("GET /biases", response.status_code, data)

        if success and isinstance(data, list):
            print(f"\n   Retrieved {len(data)} biases")
            if data:
                print(f"   First bias: {data[0]['name']}")

        return success
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_6_get_bias_details():
    """Test GET /api/v2/psychometrics/biases/{bias_id}"""
    url = f"{BASE_URL}{API_PREFIX}/biases"
    print(f"\n{'='*60}")
    print("TEST 6: Get Bias Details")
    print(f"{'='*60}")

    try:
        # Get a bias first
        list_response = requests.get(url, params={"limit": 1})
        biases = list_response.json()

        if not biases:
            print("❌ No biases available")
            return False

        bias_id = biases[0]['bias_id']
        print(f"   Testing with bias: {bias_id}")

        detail_url = f"{url}/{bias_id}"
        response = requests.get(detail_url)
        data = response.json()
        success = print_test_result(f"GET /biases/{bias_id}", response.status_code, data)

        if success:
            print(f"   Bias: {data.get('name')}")
            print(f"   Category: {data.get('category')}")

        return success
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_7_lacanian_registers():
    """Test GET /api/v2/psychometrics/lacanian/registers"""
    url = f"{BASE_URL}{API_PREFIX}/lacanian/registers"
    print(f"\n{'='*60}")
    print("TEST 7: Get Lacanian Registers")
    print(f"{'='*60}")

    try:
        response = requests.get(url)
        data = response.json()
        success = print_test_result("GET /lacanian/registers", response.status_code, data)

        if success and isinstance(data, list):
            print(f"\n   Retrieved {len(data)} registers")
            for register in data:
                print(f"   {register['register_type']}: {register['count']} traits")

        return success
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_8_dashboard():
    """Test GET /api/v2/psychometrics/dashboard"""
    url = f"{BASE_URL}{API_PREFIX}/dashboard"
    print(f"\n{'='*60}")
    print("TEST 8: Get Psychometric Dashboard")
    print(f"{'='*60}")

    try:
        response = requests.get(url)
        data = response.json()
        success = print_test_result("GET /dashboard", response.status_code, data)

        if success:
            print(f"\n   Dashboard Statistics:")
            print(f"   - Psych Traits: {data.get('total_psych_traits')}")
            print(f"   - Personality Traits: {data.get('total_personality_traits')}")
            print(f"   - Cognitive Biases: {data.get('total_cognitive_biases')}")
            print(f"   - Actor Profiles: {data.get('total_actor_profiles')}")
            print(f"   - Top Traits: {len(data.get('top_traits', []))}")

        return success
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """Run all psychometric API tests"""
    print("\n" + "="*60)
    print("PSYCHOMETRIC API TEST SUITE")
    print("Testing 8 APIs against Neo4j data")
    print("="*60)

    tests = [
        ("List Traits", test_1_list_traits),
        ("Trait Details", test_2_get_trait_details),
        ("Actor Profile", test_3_get_actor_profile),
        ("Actors by Trait", test_4_get_actors_by_trait),
        ("List Biases", test_5_list_biases),
        ("Bias Details", test_6_get_bias_details),
        ("Lacanian Registers", test_7_lacanian_registers),
        ("Dashboard", test_8_dashboard),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            results.append((name, False))

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        symbol = "✅" if result else "❌"
        print(f"{symbol} {name}")

    print(f"\nPassed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")

    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
