"""
Test script for NER v8 API
Run this after starting the API to verify functionality
"""
import requests
import json
import time

# Configuration
API_URL = "http://localhost:8000"
API_KEY = "dev-key-change-in-production"  # Change to your API key

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def test_health_check():
    """Test health endpoint (no auth required)"""
    print("\n1. Testing health check endpoint...")
    response = requests.get(f"{API_URL}/api/v1/ner/v8/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check passed")

def test_model_info():
    """Test model info endpoint"""
    print("\n2. Testing model info endpoint...")
    response = requests.get(f"{API_URL}/api/v1/ner/v8/info", headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Model Version: {result['model_version']}")
    print(f"Performance: {result['performance_metrics']}")
    print(f"Entity Labels: {result['entity_labels']}")
    assert response.status_code == 200
    print("✅ Model info passed")

def test_single_prediction():
    """Test single text prediction"""
    print("\n3. Testing single prediction endpoint...")

    test_text = "APT28 used credential dumping techniques to access the domain controller."

    response = requests.post(
        f"{API_URL}/api/v1/ner/v8/predict",
        headers=headers,
        json={"text": test_text}
    )

    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Text: {result['text']}")
    print(f"Processing Time: {result['processing_time_ms']:.2f}ms")
    print(f"Entities Found: {len(result['entities'])}")

    for entity in result['entities']:
        print(f"  - {entity['text']} ({entity['label']}) "
              f"[{entity['start']}:{entity['end']}] "
              f"confidence: {entity['confidence']}")

    assert response.status_code == 200
    assert len(result['entities']) > 0
    print("✅ Single prediction passed")

def test_batch_prediction():
    """Test batch prediction"""
    print("\n4. Testing batch prediction endpoint...")

    test_texts = [
        "APT28 used credential dumping techniques.",
        "The ransomware encrypted files on the network.",
        "Lateral movement was detected across multiple systems."
    ]

    response = requests.post(
        f"{API_URL}/api/v1/ner/v8/batch",
        headers=headers,
        json={"texts": test_texts}
    )

    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Texts Processed: {len(result['results'])}")
    print(f"Total Processing Time: {result['total_processing_time_ms']:.2f}ms")

    for i, text_result in enumerate(result['results']):
        print(f"\n  Text {i+1}: {text_result['text'][:50]}...")
        print(f"  Entities: {len(text_result['entities'])}")
        for entity in text_result['entities']:
            print(f"    - {entity['text']} ({entity['label']})")

    assert response.status_code == 200
    assert len(result['results']) == len(test_texts)
    print("✅ Batch prediction passed")

def test_invalid_api_key():
    """Test authentication failure"""
    print("\n5. Testing invalid API key...")

    invalid_headers = {
        "X-API-Key": "invalid-key",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{API_URL}/api/v1/ner/v8/predict",
        headers=invalid_headers,
        json={"text": "Test text"}
    )

    print(f"Status: {response.status_code}")
    assert response.status_code == 401
    print("✅ Authentication validation passed")

def test_rate_limiting():
    """Test rate limiting (optional - may take time)"""
    print("\n6. Testing rate limiting...")
    print("(Sending 10 requests quickly)")

    success_count = 0
    rate_limited_count = 0

    for i in range(10):
        response = requests.post(
            f"{API_URL}/api/v1/ner/v8/predict",
            headers=headers,
            json={"text": f"Test text {i}"}
        )
        if response.status_code == 200:
            success_count += 1
        elif response.status_code == 429:
            rate_limited_count += 1

    print(f"Successful: {success_count}, Rate Limited: {rate_limited_count}")
    print("✅ Rate limiting test completed")

def test_metrics_endpoint():
    """Test Prometheus metrics endpoint"""
    print("\n7. Testing metrics endpoint...")
    response = requests.get(f"{API_URL}/api/v1/ner/v8/metrics")
    print(f"Status: {response.status_code}")
    print(f"Content Type: {response.headers.get('content-type')}")
    assert response.status_code == 200
    assert 'text/plain' in response.headers.get('content-type', '')
    print("✅ Metrics endpoint passed")

def run_all_tests():
    """Run all test cases"""
    print("="*60)
    print("NER v8 API Test Suite")
    print("="*60)

    try:
        test_health_check()
        test_model_info()
        test_single_prediction()
        test_batch_prediction()
        test_invalid_api_key()
        test_metrics_endpoint()
        # test_rate_limiting()  # Uncomment to test rate limiting

        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("Make sure the API is running at", API_URL)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    run_all_tests()
