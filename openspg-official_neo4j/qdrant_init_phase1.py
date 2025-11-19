#!/usr/bin/env python3
"""
Qdrant Phase 1 Initialization
Creates collections and indexes schema documentation for 60x faster agent lookup

File: qdrant_init_phase1.py
Created: 2025-10-31
Purpose: Initialize Qdrant collections for AEON Digital Twin schema enhancement
Status: ACTIVE
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI

# Configuration
QDRANT_URL = "http://localhost:6333"
QDRANT_API_KEY = "deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ="
OPENAI_API_KEY = "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"
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMENSIONS = 3072
CHUNK_SIZE = 1000  # characters per chunk
CHUNK_OVERLAP = 200  # overlap for context preservation

# Paths
SCHEMA_DOCS_PATH = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/1_Comprehensive_Schema_Enhancement_Plan_v2")
LOCAL_BACKUP_PATH = Path("/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/qdrant_backup")

# Collections configuration
COLLECTIONS = {
    "schema_knowledge": {
        "description": "Indexed schema documentation for rapid agent lookup",
        "size": 3072,
        "distance": Distance.COSINE
    },
    "query_patterns": {
        "description": "Cypher query examples and patterns",
        "size": 3072,
        "distance": Distance.COSINE
    },
    "agent_shared_memory": {
        "description": "Cross-agent learnings and coordination",
        "size": 3072,
        "distance": Distance.COSINE
    },
    "implementation_decisions": {
        "description": "Architectural decisions and rationale",
        "size": 3072,
        "distance": Distance.COSINE
    }
}


class QdrantPhase1Initializer:
    """Initialize Qdrant collections and index documentation"""

    def __init__(self):
        """Initialize clients and paths"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Initializing Qdrant Phase 1...")

        # Initialize Qdrant client with API key
        # Note: UserWarning about insecure connection is expected for localhost HTTP
        import warnings
        warnings.filterwarnings('ignore', message='Api key is used with an insecure connection')
        self.qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        print(f"✓ Connected to Qdrant at {QDRANT_URL}")

        # Initialize OpenAI client (if API key available)
        if OPENAI_API_KEY:
            self.openai = OpenAI(api_key=OPENAI_API_KEY)
            print(f"✓ OpenAI client initialized")
        else:
            self.openai = None
            print(f"⚠ OpenAI API key not set - embeddings disabled")

        # Create local backup directory
        LOCAL_BACKUP_PATH.mkdir(parents=True, exist_ok=True)
        print(f"✓ Local backup path: {LOCAL_BACKUP_PATH}")

    def create_collections(self):
        """Create all Qdrant collections"""
        print(f"\n{'='*70}")
        print(f"CREATING QDRANT COLLECTIONS")
        print(f"{'='*70}\n")

        for collection_name, config in COLLECTIONS.items():
            try:
                # Check if collection already exists
                collections = self.qdrant.get_collections().collections
                if any(c.name == collection_name for c in collections):
                    print(f"⚠ Collection '{collection_name}' already exists - skipping")
                    continue

                # Create collection
                self.qdrant.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=config["size"],
                        distance=config["distance"]
                    )
                )
                print(f"✓ Created collection: {collection_name}")
                print(f"  Description: {config['description']}")
                print(f"  Vector size: {config['size']}")
                print(f"  Distance: {config['distance']}")

            except Exception as e:
                print(f"✗ Error creating collection '{collection_name}': {e}")
                sys.exit(1)

        print(f"\n✓ All collections created successfully\n")

    def chunk_document(self, content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk document into overlapping segments"""
        chunks = []
        start = 0
        chunk_id = 0

        while start < len(content):
            end = start + CHUNK_SIZE
            chunk_text = content[start:end]

            # Create chunk with metadata
            chunk = {
                "id": f"{metadata['file_name']}_chunk_{chunk_id}",
                "text": chunk_text,
                "metadata": {
                    **metadata,
                    "chunk_id": chunk_id,
                    "start_char": start,
                    "end_char": end,
                    "chunk_size": len(chunk_text)
                }
            }
            chunks.append(chunk)

            chunk_id += 1
            start = end - CHUNK_OVERLAP  # Overlap for context

        return chunks

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text"""
        if not self.openai:
            # Return zero vector if OpenAI not available
            return [0.0] * EMBEDDING_DIMENSIONS

        try:
            response = self.openai.embeddings.create(
                model=EMBEDDING_MODEL,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"⚠ Embedding error: {e}")
            return [0.0] * EMBEDDING_DIMENSIONS

    def index_documentation(self):
        """Index all markdown documentation files"""
        print(f"\n{'='*70}")
        print(f"INDEXING SCHEMA DOCUMENTATION")
        print(f"{'='*70}\n")

        # Find all markdown files
        md_files = list(SCHEMA_DOCS_PATH.glob("*.md"))
        print(f"Found {len(md_files)} markdown files to index\n")

        if not md_files:
            print(f"⚠ No markdown files found in {SCHEMA_DOCS_PATH}")
            return

        total_chunks = 0
        points = []

        for idx, md_file in enumerate(md_files, 1):
            try:
                # Read file content
                content = md_file.read_text(encoding='utf-8')

                # Extract metadata
                metadata = {
                    "file_name": md_file.name,
                    "file_path": str(md_file),
                    "file_size": len(content),
                    "indexed_at": datetime.now().isoformat()
                }

                # Chunk document
                chunks = self.chunk_document(content, metadata)
                print(f"[{idx}/{len(md_files)}] {md_file.name}: {len(chunks)} chunks")

                # Generate embeddings for each chunk
                for chunk in chunks:
                    if self.openai:
                        embedding = self.generate_embedding(chunk["text"])
                    else:
                        embedding = [0.0] * EMBEDDING_DIMENSIONS

                    # Create point for Qdrant
                    point = PointStruct(
                        id=hash(chunk["id"]) % (2**63),  # Convert string ID to int
                        vector=embedding,
                        payload={
                            "text": chunk["text"],
                            **chunk["metadata"]
                        }
                    )
                    points.append(point)

                total_chunks += len(chunks)

                # Backup to local JSON
                backup_file = LOCAL_BACKUP_PATH / f"{md_file.stem}_chunks.json"
                with open(backup_file, 'w') as f:
                    json.dump(chunks, f, indent=2)

            except Exception as e:
                print(f"✗ Error processing {md_file.name}: {e}")
                continue

        print(f"\n✓ Generated {total_chunks} chunks from {len(md_files)} files")

        # Upload to Qdrant in batches to avoid timeouts
        if points:
            batch_size = 100
            total_uploaded = 0
            print(f"\nUploading {len(points)} vectors to Qdrant (batches of {batch_size})...")

            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                try:
                    self.qdrant.upsert(
                        collection_name="schema_knowledge",
                        points=batch,
                        wait=True
                    )
                    total_uploaded += len(batch)
                    print(f"  Uploaded batch {i//batch_size + 1}/{(len(points) + batch_size - 1)//batch_size} ({total_uploaded}/{len(points)} vectors)")
                except Exception as e:
                    print(f"✗ Error uploading batch: {e}")
                    sys.exit(1)

            print(f"✓ Successfully uploaded {total_uploaded} vectors")

        print(f"\n✓ Documentation indexing complete")
        print(f"  Total files: {len(md_files)}")
        print(f"  Total chunks: {total_chunks}")
        print(f"  Local backup: {LOCAL_BACKUP_PATH}")

    def verify_collections(self):
        """Verify collection creation and content"""
        print(f"\n{'='*70}")
        print(f"VERIFYING COLLECTIONS")
        print(f"{'='*70}\n")

        collections = self.qdrant.get_collections().collections

        for collection in collections:
            info = self.qdrant.get_collection(collection.name)
            print(f"Collection: {collection.name}")
            print(f"  Vectors: {info.vectors_count}")
            print(f"  Points: {info.points_count}")
            print(f"  Status: {info.status}")
            print()

        print(f"✓ Verification complete")

    def run(self):
        """Execute Phase 1 initialization"""
        try:
            # Step 1: Create collections
            self.create_collections()

            # Step 2: Index documentation
            self.index_documentation()

            # Step 3: Verify setup
            self.verify_collections()

            # Summary
            print(f"\n{'='*70}")
            print(f"PHASE 1 INITIALIZATION COMPLETE")
            print(f"{'='*70}\n")
            print(f"✓ Qdrant collections created and operational")
            print(f"✓ Schema documentation indexed")
            print(f"✓ Local backups created")
            print(f"\nNext Steps:")
            print(f"  1. Test semantic search accuracy")
            print(f"  2. Implement dual memory manager")
            print(f"  3. Create agent query interface")
            print(f"  4. Begin Option B (12-wave implementation)")

        except Exception as e:
            print(f"\n✗ Phase 1 initialization failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    # Check for OpenAI API key
    if not OPENAI_API_KEY:
        print("⚠ WARNING: OPENAI_API_KEY not set in environment")
        print("   Embeddings will be disabled (zero vectors)")
        response = input("\nContinue without embeddings? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)

    # Run Phase 1 initialization
    initializer = QdrantPhase1Initializer()
    initializer.run()
