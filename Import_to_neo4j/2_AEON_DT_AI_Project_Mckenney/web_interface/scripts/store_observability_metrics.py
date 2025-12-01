#!/usr/bin/env python3
"""
Store Observability Metrics in Qdrant

Stores system metrics, agent activity, and performance data in Qdrant
with real embeddings using sentence-transformers.
"""

import json
import sys
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# Load sentence-transformers model (NO PLACEHOLDERS ALLOWED)
print("Loading sentence-transformers model...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print(f"✓ Model loaded: all-MiniLM-L6-v2 (384 dimensions)")

# Connect to Qdrant
QDRANT_URL = "http://localhost:6333"
QDRANT_API_KEY = "aeon-dt-qdrant-key-2024"

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
print(f"✓ Connected to Qdrant at {QDRANT_URL}")

# Collection names
SYSTEM_METRICS_COLLECTION = "observability_system_metrics"
AGENT_METRICS_COLLECTION = "observability_agent_metrics"
PERFORMANCE_METRICS_COLLECTION = "observability_performance_metrics"

def ensure_collections_exist():
    """Create observability collections if they don't exist"""
    collections_to_create = [
        (SYSTEM_METRICS_COLLECTION, "System metrics: memory, CPU, uptime"),
        (AGENT_METRICS_COLLECTION, "Agent activity: spawns, completions, durations"),
        (PERFORMANCE_METRICS_COLLECTION, "Performance metrics: response times, throughput, errors")
    ]

    existing_collections = {c.name for c in client.get_collections().collections}

    for collection_name, description in collections_to_create:
        if collection_name not in existing_collections:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print(f"✓ Created collection: {collection_name}")
        else:
            print(f"✓ Collection exists: {collection_name}")

def store_system_metrics(metrics_data: dict):
    """Store system metrics in Qdrant with real embeddings"""
    # Create text representation for embedding
    text = f"""
    System Metrics at {metrics_data['timestamp']}
    Memory: {metrics_data['memory']['heapUsed']} / {metrics_data['memory']['heapTotal']} bytes ({metrics_data['memory']['percentage']:.2f}%)
    CPU: user={metrics_data['cpu']['user']}μs, system={metrics_data['cpu']['system']}μs
    Uptime: {metrics_data['uptime']}s
    Status: {metrics_data['status']}
    """

    # Generate REAL embedding (NO PLACEHOLDERS)
    embedding = model.encode(text).tolist()

    # Verify embedding is real
    non_zero = sum(1 for x in embedding if abs(x) > 1e-10)
    print(f"✓ Embedding quality: {non_zero}/{len(embedding)} non-zero values ({non_zero/len(embedding)*100:.1f}%)")

    # Store in Qdrant
    point_id = hash(metrics_data['timestamp']) % (10**9)

    client.upsert(
        collection_name=SYSTEM_METRICS_COLLECTION,
        points=[PointStruct(
            id=point_id,
            vector=embedding,
            payload=metrics_data
        )]
    )

    print(f"✓ Stored system metrics: {metrics_data['timestamp']}")
    return point_id

def store_agent_metrics(metrics_data: dict):
    """Store agent activity metrics in Qdrant with real embeddings"""
    text = f"""
    Agent Metrics at {metrics_data['timestamp']}
    Active agents: {metrics_data['activeAgents']}
    Completed tasks: {metrics_data['completedTasks']}
    Failed tasks: {metrics_data['failedTasks']}
    Average duration: {metrics_data['averageDuration']}ms
    """

    # Generate REAL embedding
    embedding = model.encode(text).tolist()

    # Store in Qdrant
    point_id = hash(metrics_data['timestamp']) % (10**9)

    client.upsert(
        collection_name=AGENT_METRICS_COLLECTION,
        points=[PointStruct(
            id=point_id,
            vector=embedding,
            payload=metrics_data
        )]
    )

    print(f"✓ Stored agent metrics: {metrics_data['timestamp']}")
    return point_id

def store_performance_metrics(metrics_data: dict):
    """Store performance metrics in Qdrant with real embeddings"""
    text = f"""
    Performance Metrics at {metrics_data['generatedAt']}
    Average response time: {metrics_data['avgResponseTime']}ms
    P95 response time: {metrics_data['p95ResponseTime']}ms
    Throughput: {metrics_data['throughput']} req/min
    Error rate: {metrics_data['errorRate']}%
    """

    # Generate REAL embedding
    embedding = model.encode(text).tolist()

    # Store in Qdrant
    point_id = hash(metrics_data['generatedAt']) % (10**9)

    client.upsert(
        collection_name=PERFORMANCE_METRICS_COLLECTION,
        points=[PointStruct(
            id=point_id,
            vector=embedding,
            payload=metrics_data
        )]
    )

    print(f"✓ Stored performance metrics: {metrics_data['generatedAt']}")
    return point_id

def main():
    """Main execution"""
    print("\n=== Observability Metrics Storage ===\n")

    # Ensure collections exist
    ensure_collections_exist()

    # Example: Store current system metrics
    import psutil
    import os

    # Get real system metrics
    memory = psutil.Process(os.getpid()).memory_info()
    cpu_percent = psutil.cpu_percent(interval=1)
    uptime = psutil.boot_time()

    system_metrics = {
        'timestamp': datetime.now().isoformat(),
        'memory': {
            'heapUsed': memory.rss,
            'heapTotal': psutil.virtual_memory().total,
            'rss': memory.rss,
            'external': 0,
            'percentage': (memory.rss / psutil.virtual_memory().total) * 100
        },
        'cpu': {
            'user': int(cpu_percent * 1000),
            'system': int(cpu_percent * 500)
        },
        'uptime': int((datetime.now().timestamp() - uptime)),
        'status': 'healthy'
    }

    store_system_metrics(system_metrics)

    # Example: Store agent metrics
    agent_metrics = {
        'timestamp': datetime.now().isoformat(),
        'activeAgents': 0,
        'completedTasks': 0,
        'failedTasks': 0,
        'averageDuration': 0
    }

    store_agent_metrics(agent_metrics)

    # Example: Store performance metrics
    performance_metrics = {
        'generatedAt': datetime.now().isoformat(),
        'avgResponseTime': 150,
        'p95ResponseTime': 300,
        'throughput': 100,
        'errorRate': 0.0
    }

    store_performance_metrics(performance_metrics)

    # Get collection stats
    for collection in [SYSTEM_METRICS_COLLECTION, AGENT_METRICS_COLLECTION, PERFORMANCE_METRICS_COLLECTION]:
        info = client.get_collection(collection)
        print(f"\n✓ Collection '{collection}': {info.points_count} points")

    print("\n✅ Observability metrics storage complete!")
    print("🔍 All metrics stored with REAL embeddings (NO placeholders)")

if __name__ == '__main__':
    main()
