"""
API Integration Test Suite for NER v9
Tests all endpoints and functionality
"""
import requests
import json
import time

BASE_URL = "http://localhost:8001"
API_KEY = "dev-key-change-in-production"

def print_test(name, passed, details=""):
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"\n{status}: {name}")
    if details:
        print(f"  {details}")

def test_root():
    """Test root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        passed = response.status_code == 200 and "NER v9" in response.json().get("service", "")
        print_test("Root endpoint", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Root endpoint", False, f"Error: {str(e)}")
        return False

def test_health():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v9/ner/health")
        data = response.json()
        passed = response.status_code == 200 and data.get("model_loaded") == True
        print_test("Health check", passed, f"Model loaded: {data.get('model_loaded')}, Status: {data.get('status')}")
        return passed
    except Exception as e:
        print_test("Health check", False, f"Error: {str(e)}")
        return False

def test_info():
    """Test model info endpoint"""
    try:
        headers = {"x-api-key": API_KEY}
        response = requests.get(f"{BASE_URL}/api/v9/ner/info", headers=headers)
        data = response.json()
        passed = (response.status_code == 200 and
                 data.get("model_version") == "v9" and
                 data.get("total_entity_types") == 18)
        print_test("Model info", passed, f"Version: {data.get('model_version')}, Entity types: {data.get('total_entity_types')}")
        return passed
    except Exception as e:
        print_test("Model info", False, f"Error: {str(e)}")
        return False

def test_entity_types():
    """Test entity types endpoint"""
    try:
        headers = {"x-api-key": API_KEY}
        response = requests.get(f"{BASE_URL}/api/v9/ner/entity-types", headers=headers)
        data = response.json()
        passed = (response.status_code == 200 and
                 data.get("total_types") == 18 and
                 len(data.get("entity_types", [])) == 18)
        print_test("Entity types list", passed, f"Types: {data.get('total_types')}")
        return passed
    except Exception as e:
        print_test("Entity types list", False, f"Error: {str(e)}")
        return False

def test_extract():
    """Test entity extraction endpoint"""
    try:
        headers = {"x-api-key": API_KEY}
        payload = {
            "text": "The APT29 threat actor exploited CVE-2021-44228 vulnerability in Apache Log4j software using T1566 phishing technique.",
            "confidence_threshold": 0.8
        }
        response = requests.post(f"{BASE_URL}/api/v9/ner/extract", headers=headers, json=payload)
        data = response.json()
        passed = (response.status_code == 200 and
                 "entities" in data and
                 data.get("model_version") == "v9")
        entity_count = len(data.get("entities", []))
        print_test("Entity extraction", passed, f"Entities: {entity_count}, Time: {data.get('processing_time_ms', 0):.2f}ms")

        if entity_count > 0:
            print("  Extracted entities:")
            for ent in data["entities"][:5]:  # Show first 5
                print(f"    - {ent['label']:20s} | {ent['text']}")

        return passed
    except Exception as e:
        print_test("Entity extraction", False, f"Error: {str(e)}")
        return False

def test_batch():
    """Test batch extraction endpoint"""
    try:
        headers = {"x-api-key": API_KEY}
        payload = {
            "texts": [
                "APT29 used CVE-2021-44228 exploit",
                "The firewall equipment blocked malicious traffic",
                "SQL injection vulnerability in web application"
            ],
            "confidence_threshold": 0.7
        }
        response = requests.post(f"{BASE_URL}/api/v9/ner/batch", headers=headers, json=payload)
        data = response.json()
        passed = (response.status_code == 200 and
                 len(data.get("results", [])) == 3 and
                 data.get("model_version") == "v9")
        total_entities = sum(len(r["entities"]) for r in data.get("results", []))
        print_test("Batch extraction", passed,
                  f"Texts: 3, Total entities: {total_entities}, Time: {data.get('total_processing_time_ms', 0):.2f}ms")
        return passed
    except Exception as e:
        print_test("Batch extraction", False, f"Error: {str(e)}")
        return False

def test_authentication():
    """Test API authentication"""
    try:
        # Test without API key
        response = requests.post(f"{BASE_URL}/api/v9/ner/extract", json={"text": "test"})
        passed = response.status_code == 401
        print_test("Authentication (no key)", passed, f"Status: {response.status_code}")

        # Test with invalid API key
        headers = {"x-api-key": "invalid-key"}
        response = requests.post(f"{BASE_URL}/api/v9/ner/extract", headers=headers, json={"text": "test"})
        passed = passed and response.status_code == 401
        print_test("Authentication (invalid key)", passed, f"Status: {response.status_code}")

        return passed
    except Exception as e:
        print_test("Authentication", False, f"Error: {str(e)}")
        return False

def test_metrics():
    """Test Prometheus metrics endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v9/ner/metrics")
        passed = (response.status_code == 200 and
                 "ner_v9_requests_total" in response.text)
        print_test("Prometheus metrics", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Prometheus metrics", False, f"Error: {str(e)}")
        return False

def test_performance():
    """Test API performance"""
    try:
        headers = {"x-api-key": API_KEY}
        payload = {
            "text": "APT29 exploited CVE-2021-44228 in Apache Log4j software using phishing attacks on corporate networks.",
            "confidence_threshold": 0.8
        }

        times = []
        iterations = 10

        for _ in range(iterations):
            start = time.time()
            response = requests.post(f"{BASE_URL}/api/v9/ner/extract", headers=headers, json=payload)
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)

        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        passed = avg_time < 100  # Should be under 100ms
        print_test("Performance benchmark", passed,
                  f"Avg: {avg_time:.2f}ms, Min: {min_time:.2f}ms, Max: {max_time:.2f}ms")
        return passed
    except Exception as e:
        print_test("Performance benchmark", False, f"Error: {str(e)}")
        return False

def main():
    print("=" * 80)
    print("NER v9 API Integration Test Suite")
    print("=" * 80)
    print(f"\nBase URL: {BASE_URL}")
    print(f"Starting tests at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    tests = [
        ("Root Endpoint", test_root),
        ("Health Check", test_health),
        ("Model Info", test_info),
        ("Entity Types", test_entity_types),
        ("Entity Extraction", test_extract),
        ("Batch Extraction", test_batch),
        ("Authentication", test_authentication),
        ("Prometheus Metrics", test_metrics),
        ("Performance", test_performance),
    ]

    results = []
    for name, test_func in tests:
        print(f"\n--- {name} ---")
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"❌ FAILED: {name} - {str(e)}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"{status} {name}")

    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    print(f"Success rate: {(passed_count/total_count)*100:.1f}%")
    print("=" * 80)

    return passed_count == total_count

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
