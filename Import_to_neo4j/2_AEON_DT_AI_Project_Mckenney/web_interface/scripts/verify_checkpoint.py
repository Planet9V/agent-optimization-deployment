#!/usr/bin/env python3
"""Verify checkpoint storage in Qdrant."""

from qdrant_client import QdrantClient
import os
import json

def verify_checkpoint():
    """Verify the checkpoint was stored successfully."""

    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY", None)

    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    collection_name = "aeon_ui_checkpoints"

    try:
        # Get collection info
        collection_info = client.get_collection(collection_name)
        print(f"Collection: {collection_name}")
        print(f"Points count: {collection_info.points_count}")
        print(f"Vectors config: {collection_info.config.params.vectors}")
        print()

        # Scroll through points to find our checkpoint
        scroll_result = client.scroll(
            collection_name=collection_name,
            limit=10,
            with_payload=True,
            with_vectors=False
        )

        points, _ = scroll_result

        for point in points:
            payload = point.payload
            if payload.get('implementation_id') == 'aeon_ui_enhancement_2025-11-03':
                print("✅ CHECKPOINT FOUND")
                print(f"Point ID: {point.id}")
                print(f"Implementation ID: {payload['implementation_id']}")
                print(f"Status: {payload['status']}")
                print(f"Timestamp: {payload['timestamp']}")
                print(f"Features: {len(payload['features_implemented'])}")
                print(f"Files Created: {payload['files_created']['total']}")
                print(f"API Endpoints: {payload['api_endpoints']['total_endpoints']}")
                print()
                print("Features Implemented:")
                for feature in payload['features_implemented']:
                    print(f"  - {feature['name']}: {feature['description']}")
                return True

        print("❌ CHECKPOINT NOT FOUND")
        return False

    except Exception as e:
        print(f"Error verifying checkpoint: {e}")
        return False

if __name__ == "__main__":
    verify_checkpoint()
