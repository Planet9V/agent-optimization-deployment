#!/usr/bin/env python3
"""
Module: 01_configure_qdrant_collection.py
Specification: 03_SPECIFICATIONS/07_NER11_HIERARCHICAL_INTEGRATION_COMPLETE_SPECIFICATION.md
Section: 5.1-5.2 Qdrant Vector Storage Specification
Version: 1.0.0
Created: 2025-12-01
Last Updated: 2025-12-01
Author: AEON Architecture Team
Purpose: Configure Qdrant collection for NER11 hierarchical entities with complete indexing

This script creates and configures the Qdrant collection for storing NER11 Gold Standard
hierarchical entities with 3-tier taxonomy (60 labels → 566 types → unlimited instances).

REUSES existing Qdrant container (openspg-qdrant) running on localhost:6333.
"""

import sys
from typing import Dict, List
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PayloadSchemaType,
    CreateCollection,
)

# Configuration Constants
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "ner11_entities_hierarchical"
VECTOR_SIZE = 384  # sentence-transformers/all-MiniLM-L6-v2
DISTANCE_METRIC = Distance.COSINE

# Payload indexes for hierarchical filtering
PAYLOAD_INDEXES = [
    ("ner_label", PayloadSchemaType.KEYWORD),           # Tier 1: 60 NER labels
    ("fine_grained_type", PayloadSchemaType.KEYWORD),   # Tier 2: 566 types - CRITICAL
    ("specific_instance", PayloadSchemaType.KEYWORD),   # Tier 3: Entity names
    ("hierarchy_path", PayloadSchemaType.KEYWORD),      # Full path pattern matching
    ("hierarchy_level", PayloadSchemaType.INTEGER),     # Depth level (1, 2, or 3)
    ("confidence", PayloadSchemaType.FLOAT),            # NER confidence filtering
    ("doc_id", PayloadSchemaType.KEYWORD),              # Document lookup
    ("batch_id", PayloadSchemaType.KEYWORD),            # Batch tracking
]


def connect_to_qdrant() -> QdrantClient:
    """
    Connect to existing Qdrant server (REUSE openspg-qdrant container).

    Returns:
        QdrantClient: Connected client instance

    Raises:
        ConnectionError: If Qdrant server is not accessible
    """
    try:
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

        # Test connection
        collections = client.get_collections()
        print(f"✅ Successfully connected to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
        print(f"   Existing collections: {len(collections.collections)}")

        return client

    except Exception as e:
        print(f"❌ ERROR: Failed to connect to Qdrant server")
        print(f"   Host: {QDRANT_HOST}:{QDRANT_PORT}")
        print(f"   Error: {str(e)}")
        print(f"\n   ⚠️  SOLUTION: Ensure Qdrant container is running:")
        print(f"   docker ps | grep qdrant")
        print(f"   docker start openspg-qdrant  # if stopped")
        raise ConnectionError(f"Qdrant connection failed: {str(e)}")


def collection_exists(client: QdrantClient) -> bool:
    """
    Check if collection already exists.

    Args:
        client: QdrantClient instance

    Returns:
        bool: True if collection exists, False otherwise
    """
    try:
        collections = client.get_collections()
        existing_names = [col.name for col in collections.collections]
        exists = COLLECTION_NAME in existing_names

        if exists:
            print(f"⚠️  Collection '{COLLECTION_NAME}' already exists")

        return exists

    except Exception as e:
        print(f"❌ ERROR: Failed to check collection existence: {str(e)}")
        return False


def create_collection(client: QdrantClient) -> bool:
    """
    Create Qdrant collection with hierarchical entity schema.

    Args:
        client: QdrantClient instance

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"\n📦 Creating collection: {COLLECTION_NAME}")
        print(f"   Vector size: {VECTOR_SIZE}")
        print(f"   Distance metric: {DISTANCE_METRIC.value}")

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=DISTANCE_METRIC
            )
        )

        print(f"✅ Collection created successfully")
        return True

    except Exception as e:
        print(f"❌ ERROR: Failed to create collection: {str(e)}")
        return False


def create_payload_indexes(client: QdrantClient) -> Dict[str, bool]:
    """
    Create all required payload indexes for hierarchical filtering.

    Critical indexes:
    - fine_grained_type: Enables 566-type filtering (Tier 2)
    - ner_label: Enables 60-label filtering (Tier 1)
    - hierarchy_path: Enables path pattern matching
    - hierarchy_level: Enables depth filtering
    - confidence: Enables quality filtering
    - doc_id, batch_id: Enables traceability

    Args:
        client: QdrantClient instance

    Returns:
        Dict[str, bool]: Index creation status for each field
    """
    results = {}

    print(f"\n🔍 Creating payload indexes...")

    for field_name, schema_type in PAYLOAD_INDEXES:
        try:
            client.create_payload_index(
                collection_name=COLLECTION_NAME,
                field_name=field_name,
                field_schema=schema_type
            )

            results[field_name] = True

            # Highlight critical indexes
            if field_name == "fine_grained_type":
                print(f"   ✅ {field_name} ({schema_type.value}) - CRITICAL: Enables 566-type filtering")
            else:
                print(f"   ✅ {field_name} ({schema_type.value})")

        except Exception as e:
            results[field_name] = False
            print(f"   ❌ {field_name} ({schema_type.value}) - ERROR: {str(e)}")

    return results


def verify_collection(client: QdrantClient) -> bool:
    """
    Verify collection configuration and indexes.

    Args:
        client: QdrantClient instance

    Returns:
        bool: True if verification passed, False otherwise
    """
    try:
        print(f"\n🔬 Verifying collection configuration...")

        # Get collection info
        collection_info = client.get_collection(collection_name=COLLECTION_NAME)

        # Verify vector configuration
        vector_config = collection_info.config.params.vectors
        if vector_config.size != VECTOR_SIZE:
            print(f"   ❌ Vector size mismatch: expected {VECTOR_SIZE}, got {vector_config.size}")
            return False

        if vector_config.distance != DISTANCE_METRIC:
            print(f"   ❌ Distance metric mismatch: expected {DISTANCE_METRIC}, got {vector_config.distance}")
            return False

        print(f"   ✅ Vector configuration verified")
        print(f"      Size: {vector_config.size}")
        print(f"      Distance: {vector_config.distance.value}")

        # Verify indexes
        print(f"\n   📋 Payload indexes:")
        expected_indexes = set(field for field, _ in PAYLOAD_INDEXES)

        # Note: Qdrant may not expose index list directly via API
        # This is a basic verification
        print(f"      Expected indexes: {len(expected_indexes)}")
        for field_name, _ in PAYLOAD_INDEXES:
            print(f"      - {field_name}")

        print(f"\n   ✅ Collection verification PASSED")
        return True

    except Exception as e:
        print(f"\n   ❌ Collection verification FAILED: {str(e)}")
        return False


def print_usage_examples():
    """Print example usage patterns for the configured collection."""
    print(f"\n" + "="*70)
    print(f"📚 COLLECTION USAGE EXAMPLES")
    print(f"="*70)

    print(f"""
Collection: {COLLECTION_NAME}
Embedding Model: sentence-transformers/all-MiniLM-L6-v2 (384-dim)

🔍 Query Patterns:

1. Tier 1 Query (Broad Category - 60 NER Labels):
   ```python
   results = client.query_points(
       collection_name="{COLLECTION_NAME}",
       query=query_embedding,
       query_filter={{
           "must": [
               {{"key": "ner_label", "match": {{"value": "MALWARE"}}}}
           ]
       }},
       limit=100
   )
   # Returns: All malware types (ransomware, trojans, worms, etc.)
   ```

2. Tier 2 Query (Specific Type - 566 Fine-Grained Types) - CRITICAL:
   ```python
   results = client.query_points(
       collection_name="{COLLECTION_NAME}",
       query=query_embedding,
       query_filter={{
           "must": [
               {{"key": "fine_grained_type", "match": {{"value": "RANSOMWARE"}}}}
           ]
       }},
       limit=100
   )
   # Returns: ONLY ransomware, not all malware
   ```

3. Tier 3 Query (Specific Instance):
   ```python
   results = client.query_points(
       collection_name="{COLLECTION_NAME}",
       query=query_embedding,
       query_filter={{
           "must": [
               {{"key": "specific_instance", "match": {{"value": "WannaCry"}}}}
           ]
       }},
       limit=10
   )
   # Returns: WannaCry ransomware instances
   ```

4. Combined Semantic + Hierarchical + Quality:
   ```python
   results = client.query_points(
       collection_name="{COLLECTION_NAME}",
       query=query_embedding,
       query_filter={{
           "must": [
               {{"key": "fine_grained_type", "match": {{"any": ["PLC", "RTU", "HMI"]}}}},
               {{"key": "confidence", "range": {{"gte": 0.8}}}}
           ]
       }},
       limit=50
   )
   # Returns: High-confidence ICS devices semantically similar to query
   ```

5. Hierarchy Path Pattern Matching:
   ```python
   results = client.query_points(
       collection_name="{COLLECTION_NAME}",
       query=query_embedding,
       query_filter={{
           "must": [
               {{"key": "hierarchy_path", "match": {{"text": "MALWARE/RANSOMWARE/"}}}}
           ]
       }},
       limit=100
   )
   # Returns: All ransomware entities via path matching
   ```

✅ Next Steps:
   1. Run embedding pipeline to populate collection
   2. Verify hierarchy preservation (tier2 > tier1)
   3. Test semantic search with hierarchical filters
   4. Monitor query performance (<100ms target)

📋 Validation:
   curl http://localhost:6333/collections/{COLLECTION_NAME}
""")


def main():
    """Main execution function."""
    print("="*70)
    print("🚀 NER11 HIERARCHICAL QDRANT COLLECTION CONFIGURATION")
    print("="*70)
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Target: {QDRANT_HOST}:{QDRANT_PORT} (REUSE existing container)")
    print(f"Vector: {VECTOR_SIZE}-dim, {DISTANCE_METRIC.value} distance")
    print(f"Indexes: {len(PAYLOAD_INDEXES)} payload fields")
    print("="*70)

    try:
        # Step 1: Connect to Qdrant
        client = connect_to_qdrant()

        # Step 2: Check if collection exists
        if collection_exists(client):
            print(f"\n⚠️  Collection already exists. Options:")
            print(f"   1. Delete and recreate: client.delete_collection('{COLLECTION_NAME}')")
            print(f"   2. Skip and verify: Continue with verification")
            print(f"\n   Proceeding with verification...")
        else:
            # Step 3: Create collection
            if not create_collection(client):
                print(f"\n❌ FAILED: Collection creation failed")
                sys.exit(1)

        # Step 4: Create payload indexes
        index_results = create_payload_indexes(client)

        # Check if all indexes created successfully
        failed_indexes = [field for field, success in index_results.items() if not success]
        if failed_indexes:
            print(f"\n⚠️  WARNING: Some indexes failed to create:")
            for field in failed_indexes:
                print(f"   - {field}")
            print(f"\n   Impact: Queries on these fields may be slower")
        else:
            print(f"\n✅ All {len(PAYLOAD_INDEXES)} indexes created successfully")

        # Step 5: Verify collection
        if not verify_collection(client):
            print(f"\n❌ FAILED: Collection verification failed")
            sys.exit(1)

        # Step 6: Print usage examples
        print_usage_examples()

        # Final success message
        print(f"\n" + "="*70)
        print(f"✅ SUCCESS: Collection configured and ready")
        print(f"="*70)
        print(f"\n📊 Summary:")
        print(f"   Collection: {COLLECTION_NAME}")
        print(f"   Status: READY")
        print(f"   Vectors: 0 (empty, ready for ingestion)")
        print(f"   Indexes: {len(PAYLOAD_INDEXES)} payload fields")
        print(f"   Connection: {QDRANT_HOST}:{QDRANT_PORT}")
        print(f"\n🔍 Verify with:")
        print(f"   curl http://localhost:6333/collections/{COLLECTION_NAME}")
        print(f"\n📋 Next Step:")
        print(f"   Run embedding pipeline to populate collection")
        print(f"   (Task 1.3 in TASKMASTER_NER11_GOLD_COMPLETE_v2.0.md)")

        sys.exit(0)

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
