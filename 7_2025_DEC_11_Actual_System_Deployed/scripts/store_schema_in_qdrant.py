#!/usr/bin/env python3
"""
Store Neo4j Schema Analysis in Qdrant
Namespace: aeon-actual-system
"""

import json
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# Configuration
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "aeon-actual-system"
MODEL_NAME = "all-MiniLM-L6-v2"

def init_qdrant_collection(client):
    """Initialize Qdrant collection if it doesn't exist"""
    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]

    if COLLECTION_NAME not in collection_names:
        print(f"Creating collection: {COLLECTION_NAME}")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
    else:
        print(f"Collection already exists: {COLLECTION_NAME}")

def chunk_document(doc_path, chunk_size=1000, overlap=200):
    """Chunk large documents into smaller pieces with overlap"""
    with open(doc_path, 'r') as f:
        content = f.read()

    chunks = []
    lines = content.split('\n')
    current_chunk = []
    current_size = 0

    for line in lines:
        line_size = len(line)
        if current_size + line_size > chunk_size and current_chunk:
            # Save chunk
            chunks.append('\n'.join(current_chunk))
            # Keep overlap
            overlap_lines = current_chunk[-5:] if len(current_chunk) > 5 else current_chunk
            current_chunk = overlap_lines + [line]
            current_size = sum(len(l) for l in current_chunk)
        else:
            current_chunk.append(line)
            current_size += line_size

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks

def store_document(client, model, doc_path, doc_type, metadata=None):
    """Store document chunks in Qdrant with embeddings"""
    chunks = chunk_document(doc_path)
    print(f"\n📄 Processing {doc_path.name}: {len(chunks)} chunks")

    points = []
    for i, chunk in enumerate(chunks):
        # Generate embedding
        embedding = model.encode(chunk).tolist()

        # Create metadata
        chunk_metadata = {
            "doc_type": doc_type,
            "doc_name": doc_path.name,
            "chunk_index": i,
            "total_chunks": len(chunks),
            "content": chunk,
            "namespace": "aeon-actual-system"
        }
        if metadata:
            chunk_metadata.update(metadata)

        # Create point
        point = PointStruct(
            id=hash(f"{doc_path.name}_{i}") % (2**63),  # Unique ID
            vector=embedding,
            payload=chunk_metadata
        )
        points.append(point)

    # Upsert to Qdrant
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    print(f"✅ Stored {len(points)} chunks from {doc_path.name}")

def main():
    # Initialize clients
    print("Initializing Qdrant client...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    # Initialize collection
    init_qdrant_collection(client)

    # Document paths
    base_path = Path("/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed")
    docs_path = base_path / "docs"
    queries_path = base_path / "queries"

    # Store main schema documentation
    schema_doc = docs_path / "ACTUAL_SCHEMA_IMPLEMENTED.md"
    if schema_doc.exists():
        store_document(
            client, model, schema_doc,
            doc_type="schema_documentation",
            metadata={
                "category": "neo4j_schema",
                "extraction_date": "2025-12-12",
                "database": "openspg-neo4j",
                "version": "v1.0.0"
            }
        )

    # Store summary
    summary_doc = docs_path / "SCHEMA_ANALYSIS_SUMMARY.md"
    if summary_doc.exists():
        store_document(
            client, model, summary_doc,
            doc_type="schema_summary",
            metadata={
                "category": "neo4j_schema",
                "extraction_date": "2025-12-12",
                "database": "openspg-neo4j"
            }
        )

    # Store query results
    query_files = [
        "all_labels.txt",
        "all_relationship_types.txt",
        "multi_label_combinations.txt",
        "label_distribution.txt",
        "relationship_patterns.txt"
    ]

    for query_file in query_files:
        query_path = queries_path / query_file
        if query_path.exists():
            store_document(
                client, model, query_path,
                doc_type="query_result",
                metadata={
                    "category": "neo4j_schema_query",
                    "query_type": query_file.replace('.txt', ''),
                    "extraction_date": "2025-12-12"
                }
            )

    # Get collection info
    collection_info = client.get_collection(COLLECTION_NAME)
    print(f"\n📊 Collection Stats:")
    print(f"   Name: {collection_info.name}")
    print(f"   Points: {collection_info.points_count}")
    print(f"   Vectors: {collection_info.vectors_count}")

    print("\n✅ All documents stored in Qdrant namespace: aeon-actual-system")

if __name__ == "__main__":
    main()
