#!/usr/bin/env python3
"""
Store comprehensive API test results in Qdrant
Namespace: api-fixes/test-script
Usage: python3 store_test_results_qdrant.py --results-file <file> --json-file <file> --collection <name>
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

# Initialize Qdrant client
client = QdrantClient(url="http://localhost:6333")

def generate_embedding(text):
    """Generate simple embedding from text"""
    import hashlib
    hash_bytes = hashlib.sha384(text.encode()).digest()
    # Convert to 384-dim vector (normalized)
    vector = [float((b - 128) / 128.0) for b in hash_bytes[:384]]
    return vector

def ensure_collection(collection_name):
    """Ensure collection exists"""
    try:
        client.get_collection(collection_name)
        print(f"✅ Collection '{collection_name}' exists")
    except:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"✅ Collection '{collection_name}' created")

def parse_results_markdown(results_file):
    """Parse markdown results file to extract test data"""
    with open(results_file, 'r') as f:
        content = f.read()

    # Extract summary statistics
    summary = {}
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '**Total Tests**:' in line:
            summary['total'] = int(line.split(':')[1].strip())
        elif '**Passed**:' in line:
            parts = line.split(':')[1].strip().split()
            summary['passed'] = int(parts[0])
        elif '**Client Errors**:' in line:
            summary['client_errors'] = int(line.split(':')[1].strip())
        elif '**Server Errors**:' in line:
            summary['server_errors'] = int(line.split(':')[1].strip())

    return summary

def store_results(results_file, json_file, collection_name):
    """Store comprehensive test results in Qdrant"""

    # Ensure collection exists
    ensure_collection(collection_name)

    # Load JSON test data
    with open(json_file, 'r') as f:
        test_data = json.load(f)

    # Parse markdown summary
    summary = parse_results_markdown(results_file)

    print(f"\n📊 Processing {len(test_data)} test results...")

    points = []

    # Store overall summary
    timestamp = datetime.now().isoformat()
    summary_text = f"API Testing Run {timestamp}: {summary.get('total', 0)} APIs tested, {summary.get('passed', 0)} passed"

    points.append(PointStruct(
        id=hash(f"summary-{timestamp}") % (2**31),
        vector=generate_embedding(summary_text),
        payload={
            "type": "test_summary",
            "namespace": "api-fixes/test-script",
            "timestamp": timestamp,
            "total_tests": summary.get('total', 0),
            "passed": summary.get('passed', 0),
            "client_errors": summary.get('client_errors', 0),
            "server_errors": summary.get('server_errors', 0),
            "pass_rate": round(summary.get('passed', 0) * 100 / summary.get('total', 1), 2),
            "results_file": str(results_file),
            "json_file": str(json_file)
        }
    ))

    # Store each test result
    for idx, test in enumerate(test_data):
        test_text = f"{test.get('description', 'Unknown')} - {test.get('method', 'GET')} {test.get('endpoint', '')} - Status: {test.get('status', 'UNKNOWN')}"

        point_id = hash(f"{test.get('service', 'unknown')}-{test.get('endpoint', '')}-{idx}") % (2**31)

        points.append(PointStruct(
            id=point_id,
            vector=generate_embedding(test_text),
            payload={
                "type": "test_result",
                "namespace": "api-fixes/test-script",
                "test_number": test.get('test_number', idx + 1),
                "description": test.get('description', ''),
                "category": test.get('category', ''),
                "service": test.get('service', ''),
                "method": test.get('method', ''),
                "endpoint": test.get('endpoint', ''),
                "status": test.get('status', ''),
                "http_code": test.get('http_code', ''),
                "response_time": test.get('response_time', ''),
                "timestamp": test.get('timestamp', timestamp)
            }
        ))

    # Group by status
    status_groups = {}
    for test in test_data:
        status = test.get('status', 'UNKNOWN')
        if status not in status_groups:
            status_groups[status] = []
        status_groups[status].append(test)

    # Store status summaries
    for status, tests in status_groups.items():
        status_text = f"{status} APIs: {len(tests)} endpoints with status {status}"

        points.append(PointStruct(
            id=hash(f"status-{status}-{timestamp}") % (2**31),
            vector=generate_embedding(status_text),
            payload={
                "type": "status_summary",
                "namespace": "api-fixes/test-script",
                "status": status,
                "count": len(tests),
                "timestamp": timestamp,
                "endpoints": [f"{t.get('method', '')} {t.get('endpoint', '')}" for t in tests[:10]]  # First 10
            }
        ))

    # Group by service
    service_groups = {}
    for test in test_data:
        service = test.get('service', 'unknown')
        if service not in service_groups:
            service_groups[service] = {'total': 0, 'passed': 0, 'failed': 0, 'errors': 0}

        service_groups[service]['total'] += 1
        status = test.get('status', '')
        if status == 'PASS':
            service_groups[service]['passed'] += 1
        elif 'ERROR' in status:
            service_groups[service]['errors'] += 1
        else:
            service_groups[service]['failed'] += 1

    # Store service summaries
    for service, stats in service_groups.items():
        service_text = f"{service} service: {stats['total']} APIs tested, {stats['passed']} passed, {stats['failed']} failed, {stats['errors']} errors"

        points.append(PointStruct(
            id=hash(f"service-{service}-{timestamp}") % (2**31),
            vector=generate_embedding(service_text),
            payload={
                "type": "service_summary",
                "namespace": "api-fixes/test-script",
                "service": service,
                "timestamp": timestamp,
                **stats,
                "pass_rate": round(stats['passed'] * 100 / stats['total'], 2) if stats['total'] > 0 else 0
            }
        ))

    # Group by category
    category_groups = {}
    for test in test_data:
        category = test.get('category', 'unknown')
        if category not in category_groups:
            category_groups[category] = {'total': 0, 'passed': 0}

        category_groups[category]['total'] += 1
        if test.get('status') == 'PASS':
            category_groups[category]['passed'] += 1

    # Store category summaries
    for category, stats in category_groups.items():
        category_text = f"{category} APIs: {stats['total']} tested, {stats['passed']} passed"

        points.append(PointStruct(
            id=hash(f"category-{category}-{timestamp}") % (2**31),
            vector=generate_embedding(category_text),
            payload={
                "type": "category_summary",
                "namespace": "api-fixes/test-script",
                "category": category,
                "timestamp": timestamp,
                **stats,
                "pass_rate": round(stats['passed'] * 100 / stats['total'], 2) if stats['total'] > 0 else 0
            }
        ))

    # Upload to Qdrant in batches
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i+batch_size]
        client.upsert(
            collection_name=collection_name,
            points=batch
        )
        print(f"  Uploaded batch {i//batch_size + 1}/{(len(points) + batch_size - 1)//batch_size}")

    print(f"\n✅ Stored {len(points)} points in Qdrant")
    print(f"📊 Summary Statistics:")
    print(f"   Total Tests: {summary.get('total', 0)}")
    print(f"   Passed: {summary.get('passed', 0)} ({round(summary.get('passed', 0) * 100 / summary.get('total', 1), 1)}%)")
    print(f"   Client Errors: {summary.get('client_errors', 0)}")
    print(f"   Server Errors: {summary.get('server_errors', 0)}")
    print(f"\n🏷️ Services Tested:")
    for service, stats in service_groups.items():
        print(f"   {service}: {stats['passed']}/{stats['total']} passed ({stats['pass_rate']:.1f}%)")
    print(f"\n📁 Categories Tested:")
    for category, stats in category_groups.items():
        print(f"   {category}: {stats['passed']}/{stats['total']} passed ({stats['pass_rate']:.1f}%)")

def query_test_results(collection_name):
    """Query and display test results"""
    print(f"\n🔍 Querying test results from '{collection_name}'...")

    # Search for failed tests
    search_text = "failed error server"
    results = client.search(
        collection_name=collection_name,
        query_vector=generate_embedding(search_text),
        limit=5,
        query_filter={
            "must": [
                {"key": "namespace", "match": {"value": "api-fixes/test-script"}}
            ]
        }
    )

    print(f"\nTop results for '{search_text}':")
    for hit in results:
        print(f"  - Score: {hit.score:.3f}")
        print(f"    Type: {hit.payload.get('type', 'unknown')}")
        if hit.payload.get('type') == 'test_result':
            print(f"    Test: {hit.payload.get('description', 'N/A')}")
            print(f"    Endpoint: {hit.payload.get('method', '')} {hit.payload.get('endpoint', '')}")
            print(f"    Status: {hit.payload.get('status', 'UNKNOWN')}")
        elif hit.payload.get('type') == 'status_summary':
            print(f"    Status: {hit.payload.get('status', '')} ({hit.payload.get('count', 0)} tests)")
        print()

def main():
    parser = argparse.ArgumentParser(description='Store API test results in Qdrant')
    parser.add_argument('--results-file', required=True, help='Path to markdown results file')
    parser.add_argument('--json-file', required=True, help='Path to JSON test data file')
    parser.add_argument('--collection', default='api-fixes', help='Qdrant collection name')
    parser.add_argument('--query', action='store_true', help='Query results after storing')

    args = parser.parse_args()

    # Validate files exist
    if not Path(args.results_file).exists():
        print(f"❌ Results file not found: {args.results_file}")
        sys.exit(1)

    if not Path(args.json_file).exists():
        print(f"❌ JSON file not found: {args.json_file}")
        sys.exit(1)

    print("=" * 70)
    print("API TEST RESULTS - QDRANT STORAGE")
    print("=" * 70)
    print(f"Results File: {args.results_file}")
    print(f"JSON File: {args.json_file}")
    print(f"Collection: {args.collection}")
    print("=" * 70)

    try:
        store_results(args.results_file, args.json_file, args.collection)

        if args.query:
            query_test_results(args.collection)

        print("\n✅ Storage complete!")
        print(f"📍 Collection: {args.collection}")
        print(f"🏷️ Namespace: api-fixes/test-script")
        print(f"🕐 Timestamp: {datetime.now().isoformat()}")

    except Exception as e:
        print(f"\n❌ Error storing results: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
