#!/usr/bin/env python3
"""
Chunked Document Ingestion Script

Processes large documents by splitting them into smaller chunks to prevent
NER11 API memory exhaustion. This fixes the crash issue for documents >70KB.

Usage:
    python3 scripts/chunked_ingest.py --wiki-root "/path/to/docs" --delay 3
    python3 scripts/chunked_ingest.py --file "/path/to/large_doc.md"
"""

import sys
import os
import requests
import json
import time
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import argparse

# Add pipelines to path
pipelines_path = Path(__file__).parent.parent / "pipelines"
sys.path.insert(0, str(pipelines_path))

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

# Import relationship extractor
import importlib.util
spec = importlib.util.spec_from_file_location("relationship_extractor", pipelines_path / "relationship_extractor.py")
rel_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rel_module)
RelationshipExtractor = rel_module.RelationshipExtractor

# Configuration
MAX_CHUNK_SIZE = 50000  # 50KB per chunk - safe threshold
MIN_CHUNK_SIZE = 5000   # Don't create tiny chunks
OVERLAP_SIZE = 500      # Overlap between chunks to preserve context


def chunk_document(content: str, max_size: int = MAX_CHUNK_SIZE) -> List[str]:
    """
    Split large documents into processable chunks.

    Strategy:
    1. Try to split on paragraph boundaries
    2. Fall back to sentence boundaries
    3. Last resort: character boundaries with overlap
    """
    if len(content) <= max_size:
        return [content]

    chunks = []

    # Try paragraph-based splitting first
    paragraphs = content.split('\n\n')
    current_chunk = ""

    for para in paragraphs:
        # If adding this paragraph keeps us under limit, add it
        if len(current_chunk) + len(para) + 2 < max_size:
            current_chunk += para + "\n\n"
        else:
            # Save current chunk if it has content
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            # If paragraph itself is too large, split it further
            if len(para) > max_size:
                # Split on sentences
                sentences = re.split(r'(?<=[.!?])\s+', para)
                current_chunk = ""
                for sent in sentences:
                    if len(current_chunk) + len(sent) + 1 < max_size:
                        current_chunk += sent + " "
                    else:
                        if current_chunk.strip():
                            chunks.append(current_chunk.strip())
                        # If sentence is still too long, hard split
                        if len(sent) > max_size:
                            for i in range(0, len(sent), max_size - OVERLAP_SIZE):
                                chunk_text = sent[i:i + max_size]
                                if chunk_text.strip():
                                    chunks.append(chunk_text.strip())
                            current_chunk = ""
                        else:
                            current_chunk = sent + " "
            else:
                current_chunk = para + "\n\n"

    # Don't forget the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Filter out tiny chunks and merge them
    final_chunks = []
    merge_buffer = ""

    for chunk in chunks:
        if len(chunk) < MIN_CHUNK_SIZE:
            merge_buffer += " " + chunk
        else:
            if merge_buffer:
                final_chunks.append(merge_buffer.strip())
                merge_buffer = ""
            final_chunks.append(chunk)

    if merge_buffer.strip():
        if final_chunks:
            # Append to last chunk if possible
            if len(final_chunks[-1]) + len(merge_buffer) < max_size:
                final_chunks[-1] += " " + merge_buffer.strip()
            else:
                final_chunks.append(merge_buffer.strip())
        else:
            final_chunks.append(merge_buffer.strip())

    return final_chunks if final_chunks else [content[:max_size]]


class ChunkedIngestionPipeline:
    """Ingestion pipeline with document chunking for large files."""

    def __init__(
        self,
        ner11_api_url: str = "http://localhost:8000",
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        delay_between_docs: float = 3.0,
        timeout: int = 90,
        chunk_size: int = MAX_CHUNK_SIZE
    ):
        self.ner11_api_url = ner11_api_url
        self.delay = delay_between_docs
        self.timeout = timeout
        self.chunk_size = chunk_size

        # Initialize Qdrant client
        self.qdrant = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.collection_name = "ner11_entities_hierarchical"

        # Initialize Neo4j driver
        self.neo4j_driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

        # Initialize embedding model
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        # Initialize relationship extractor
        print("Initializing relationship extractor...")
        self.relationship_extractor = RelationshipExtractor()

        print(f"✅ Chunked Ingestion Pipeline initialized")
        print(f"   - NER11 API: {ner11_api_url}")
        print(f"   - Max chunk size: {chunk_size:,} chars")
        print(f"   - Delay between docs: {delay_between_docs}s")
        print(f"   - Timeout: {timeout}s")

    def check_api_health(self) -> bool:
        """Check if API is healthy."""
        try:
            response = requests.get(f"{self.ner11_api_url}/health", timeout=10)
            return response.status_code == 200
        except:
            return False

    def wait_for_api(self, max_wait: int = 120) -> bool:
        """Wait for API to become available."""
        print("   ⏳ Waiting for API to recover...", end="", flush=True)
        for i in range(max_wait):
            if self.check_api_health():
                print(f" Ready after {i}s")
                return True
            time.sleep(1)
            if i % 10 == 9:
                print(".", end="", flush=True)
        print(" Timeout!")
        return False

    def extract_entities(self, text: str) -> Optional[List[Dict]]:
        """Extract entities using NER11 API."""
        try:
            response = requests.post(
                f"{self.ner11_api_url}/ner",
                json={"text": text},
                timeout=self.timeout
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("entities", [])
            else:
                print(f"   ⚠️  NER11 API error: {response.status_code}")
                return None
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout after {self.timeout}s")
            return None
        except Exception as e:
            print(f"   ❌ NER11 API failed: {e}")
            return None

    def store_entities(self, entities: List[Dict], source_file: Path) -> Dict:
        """Store entities in Qdrant and Neo4j."""
        if not entities:
            return {"status": "no_entities", "entities": 0}

        qdrant_count = 0
        neo4j_count = 0
        rel_count = 0

        # Deduplicate entities by (text, label) tuple
        seen = set()
        unique_entities = []
        for ent in entities:
            key = (ent.get("text", ""), ent.get("label", ""))
            if key not in seen:
                seen.add(key)
                unique_entities.append(ent)

        # Store in Qdrant
        for ent in unique_entities:
            try:
                text = ent.get("text", "")
                label = ent.get("label", "UNKNOWN")
                embedding = self.embedding_model.encode(text).tolist()

                point_id = hash(f"{text}_{label}_{source_file.stem}") % (2**63)

                self.qdrant.upsert(
                    collection_name=self.collection_name,
                    points=[PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload={
                            "text": text,
                            "label": label,
                            "source_file": source_file.name,
                            "created_at": datetime.utcnow().isoformat()
                        }
                    )]
                )
                qdrant_count += 1
            except Exception as e:
                pass

        # Store in Neo4j with MERGE for deduplication
        try:
            with self.neo4j_driver.session() as session:
                for ent in unique_entities:
                    text = ent.get("text", "")
                    label = ent.get("label", "UNKNOWN")
                    session.run("""
                        MERGE (e:Entity {text: $text, label: $label})
                        ON CREATE SET e.source_file = $source, e.created_at = timestamp()
                        ON MATCH SET e.last_seen = timestamp()
                    """, text=text, label=label, source=source_file.name)
                    neo4j_count += 1
        except Exception as e:
            print(f"   ⚠️  Neo4j error: {e}")

        return {
            "status": "success",
            "entities": len(unique_entities),
            "qdrant": qdrant_count,
            "neo4j": neo4j_count
        }

    def process_single_document(self, filepath: Path, doc_num: int = 1, total: int = 1) -> Dict:
        """Process a single document with chunking for large files."""
        filename = filepath.name
        print(f"\n📄 [{doc_num}/{total}] {filename}")

        # Read document
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"   ❌ Read error: {e}")
            return {"status": "read_error", "entities": 0}

        doc_size = len(content)
        print(f"   📏 Size: {doc_size:,} bytes")

        # Check if chunking is needed
        if doc_size > self.chunk_size:
            chunks = chunk_document(content, self.chunk_size)
            print(f"   🔪 Split into {len(chunks)} chunks")

            all_entities = []
            for i, chunk in enumerate(chunks, 1):
                print(f"   📦 Processing chunk {i}/{len(chunks)} ({len(chunk):,} chars)...", end=" ")

                # Wait for API to be ready
                if not self.check_api_health():
                    print("⚠️ API not ready")
                    if not self.wait_for_api():
                        print(f"   ❌ API down, skipping remaining chunks")
                        break

                entities = self.extract_entities(chunk)
                if entities is None:
                    print("⚠️ Failed")
                    # Try to recover
                    if not self.wait_for_api(60):
                        break
                    continue

                print(f"✅ {len(entities)} entities")
                all_entities.extend(entities)

                # Brief pause between chunks
                time.sleep(1)

            if not all_entities:
                return {"status": "no_entities", "entities": 0}

            result = self.store_entities(all_entities, filepath)
            print(f"   ✅ Total: {result['entities']} entities from {len(chunks)} chunks")
            return result
        else:
            # Small document - process directly
            entities = self.extract_entities(content)

            if entities is None:
                # Retry once after API recovery
                if not self.wait_for_api():
                    return {"status": "api_down", "entities": 0}
                entities = self.extract_entities(content)

            if not entities:
                print(f"   ⚠️  No entities found")
                return {"status": "no_entities", "entities": 0}

            result = self.store_entities(entities, filepath)
            print(f"   ✅ Entities: {result['entities']} → Qdrant: {result['qdrant']}, Neo4j: {result['neo4j']}")
            return result

    def process_directory(self, wiki_root: str) -> Dict:
        """Process all documents in directory with chunking."""
        wiki_path = Path(wiki_root)

        # Find all markdown files
        md_files = list(wiki_path.rglob("*.md"))
        total = len(md_files)

        print(f"\n📚 Chunked Ingestion Pipeline")
        print(f"   Found: {total} documents")
        print(f"   Max chunk: {self.chunk_size:,} chars")
        print(f"   Delay: {self.delay}s between documents")

        # Track results
        results = {
            "success": 0,
            "failed": 0,
            "no_entities": 0,
            "total_entities": 0,
            "chunked_docs": 0,
            "failed_files": []
        }

        for i, filepath in enumerate(md_files, 1):
            # Check API health before each document
            if not self.check_api_health():
                print(f"\n   ⚠️  API not healthy, waiting...")
                if not self.wait_for_api(120):
                    print(f"   ❌ API down, stopping at doc {i}")
                    break

            result = self.process_single_document(filepath, i, total)

            if result["status"] == "success":
                results["success"] += 1
                results["total_entities"] += result["entities"]
                # Track if document was chunked
                with open(filepath, 'r', errors='ignore') as f:
                    if len(f.read()) > self.chunk_size:
                        results["chunked_docs"] += 1
            elif result["status"] == "no_entities":
                results["no_entities"] += 1
            else:
                results["failed"] += 1
                results["failed_files"].append(str(filepath))

            # Rate limit - wait between documents
            if i < total:
                time.sleep(self.delay)

        # Summary
        print(f"\n{'='*60}")
        print(f"📊 CHUNKED INGESTION SUMMARY")
        print(f"{'='*60}")
        print(f"Documents Processed: {results['success'] + results['failed'] + results['no_entities']}/{total}")
        print(f"Successful: {results['success']}")
        print(f"Chunked Documents: {results['chunked_docs']}")
        print(f"No Entities: {results['no_entities']}")
        print(f"Failed: {results['failed']}")
        print(f"Total Entities Added: {results['total_entities']}")
        print(f"{'='*60}")

        return results


def main():
    parser = argparse.ArgumentParser(description="Chunked Document Ingestion")
    parser.add_argument("--wiki-root", help="Directory containing documents")
    parser.add_argument("--file", help="Single file to process")
    parser.add_argument("--delay", type=float, default=3.0, help="Delay between documents (seconds)")
    parser.add_argument("--timeout", type=int, default=90, help="API timeout per request (seconds)")
    parser.add_argument("--chunk-size", type=int, default=50000, help="Maximum chunk size in characters")

    args = parser.parse_args()

    if not args.wiki_root and not args.file:
        parser.error("Either --wiki-root or --file is required")

    pipeline = ChunkedIngestionPipeline(
        delay_between_docs=args.delay,
        timeout=args.timeout,
        chunk_size=args.chunk_size
    )

    if args.file:
        # Process single file
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        result = pipeline.process_single_document(filepath)
        print(f"\n✅ Result: {result}")
    else:
        # Process directory
        results = pipeline.process_directory(args.wiki_root)

        # Save results
        results_file = Path(__file__).parent.parent / "logs" / "chunked_ingest_results.json"
        results_file.parent.mkdir(exist_ok=True)
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📝 Results saved to: {results_file}")


if __name__ == "__main__":
    main()
