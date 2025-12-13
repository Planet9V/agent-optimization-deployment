#!/usr/bin/env python3
"""
Store Complete Schema Reference in Qdrant for Frontend Package

This script stores the COMPLETE_SCHEMA_REFERENCE_ENHANCED.md in Qdrant
under the 'frontend-package' namespace for easy retrieval by UI developers.
"""

import os
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import hashlib
import uuid

def load_schema_document():
    """Load the enhanced schema reference document."""
    doc_path = "/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/COMPLETE_SCHEMA_REFERENCE_ENHANCED.md"

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content

def generate_doc_id(content):
    """Generate stable UUID from content hash."""
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    # Use first 32 chars of hash to create UUID
    return str(uuid.UUID(content_hash[:32]))

def create_dummy_vector(dim=384):
    """Create a dummy vector for storage (actual embedding can be added later)."""
    import random
    return [random.random() for _ in range(dim)]

def main():
    # Connect to Qdrant
    client = QdrantClient(host="localhost", port=6333)

    # Load document
    content = load_schema_document()
    doc_id = generate_doc_id(content)

    print(f"📄 Loaded schema document ({len(content)} bytes)")
    print(f"🔑 Document ID: {doc_id}")

    # Create collection if it doesn't exist
    collection_name = "frontend-package"

    try:
        client.get_collection(collection_name)
        print(f"✅ Collection '{collection_name}' exists")
    except:
        print(f"📦 Creating collection '{collection_name}'...")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

    # Prepare point with rich metadata
    point = PointStruct(
        id=doc_id,
        vector=create_dummy_vector(384),
        payload={
            "document_type": "schema_reference",
            "title": "Complete Neo4j Schema Reference - ENHANCED",
            "version": "1.0.0",
            "generated": "2025-12-12",
            "verification_status": "COMPLETE",
            "database": "openspg-neo4j",
            "bolt_uri": "bolt://localhost:7687",

            # Schema statistics
            "total_labels": 631,
            "total_relationships": 183,
            "total_nodes": 1207069,
            "total_edges": 12344852,
            "super_label_coverage": 0.81,
            "super_labels_count": 17,

            # Completeness flags
            "labels_documented": True,
            "relationships_documented": True,
            "property_schemas_documented": True,
            "query_examples_provided": True,
            "api_integration_guide": True,
            "performance_optimization_guide": True,

            # Content sections
            "sections": [
                "hierarchical_structure",
                "super_labels",
                "complete_labels_631",
                "complete_relationships_183",
                "property_schemas",
                "advanced_query_examples",
                "api_integration_guide",
                "performance_optimization",
                "schema_quality_report"
            ],

            # Target audience
            "target_audience": [
                "frontend_developers",
                "api_developers",
                "data_scientists",
                "security_analysts",
                "infrastructure_engineers"
            ],

            # Content metadata
            "content_length": len(content),
            "format": "markdown",
            "language": "en",

            # Searchable tags
            "tags": [
                "schema",
                "neo4j",
                "documentation",
                "complete",
                "verified",
                "production",
                "frontend-ready",
                "no-truncation"
            ],

            # Full document content
            "content": content,

            # Document location
            "file_path": "/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/COMPLETE_SCHEMA_REFERENCE_ENHANCED.md",

            # Quality indicators
            "truncated": False,
            "complete": True,
            "verified_against_db": True,
            "verification_date": "2025-12-12",

            # Schema issues identified
            "known_issues": [
                "19% of nodes lack super_label property (229,920 nodes)",
                "Some Technique nodes misclassified with tier2='ThreatActor'",
                "Property schemas documented for 17 super labels only"
            ],

            # Quick stats for search
            "key_metrics": {
                "vulnerability_nodes": 314538,
                "measurement_nodes": 297158,
                "asset_nodes": 200275,
                "sbom_nodes": 140000,
                "impacts_relationships": 4780563,
                "vulnerable_to_relationships": 3117735
            }
        }
    )

    # Upsert the point
    print(f"💾 Storing in Qdrant collection '{collection_name}'...")
    client.upsert(
        collection_name=collection_name,
        points=[point]
    )

    print(f"\n✅ COMPLETE Schema Reference stored successfully!")
    print(f"📍 Point ID: {doc_id}")
    print(f"📦 Collection: {collection_name}")
    print(f"📄 Document size: {len(content):,} bytes")
    print(f"\n🔍 Retrieve with:")
    print(f"   client.retrieve(collection_name='{collection_name}', ids=['{doc_id}'])")
    print(f"\n💡 Search tags: schema, neo4j, complete, verified, frontend-ready")

    # Verify storage
    print(f"\n🔬 Verifying storage...")
    result = client.retrieve(
        collection_name=collection_name,
        ids=[doc_id]
    )

    if result:
        stored_content = result[0].payload.get('content', '')
        if len(stored_content) == len(content):
            print(f"✅ Verification PASSED - Content intact ({len(stored_content):,} bytes)")
        else:
            print(f"⚠️  Verification WARNING - Size mismatch: {len(stored_content):,} vs {len(content):,}")
    else:
        print(f"❌ Verification FAILED - Could not retrieve document")

    print(f"\n🎯 Document ready for frontend developers!")

if __name__ == "__main__":
    main()
