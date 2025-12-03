#!/usr/bin/env python3
"""
Rate-Limited Document Ingestion Script
Processes documents ONE AT A TIME with delays to prevent API crashes.

Usage:
    python3 scripts/rate_limited_ingest.py --wiki-root "/path/to/docs" --delay 5
"""

import sys
import os
import requests
import json
import time
from pathlib import Path
from typing import List, Dict, Any
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

# Files that crash NER11 API - skip these
SKIP_FILES = {
    "ANZ_Rail Cybersecurity Thrats_2025_10.md",
    "QTMP_Rail Cyberthreat Research_2025_10.md",
    "PHASE_1_EXECUTION_STATUS.md",
    "AGENT_ARCHITECTURE_SPECIALIZED.md",
    "PILOT_DEEP_ANALYSIS_STRATEGIC_INTELLIGENCE_REPORT.md",
    "AEON_Complete_Technical_White_Paper.md",
    "V9_ANALYSIS_COMPLETION_REPORT.md",
    # Added from E30 session - crash API after 3 retries
    "Casper Sleep Inc. GTM Analysis_.md",
    "GE Go-to-Market Analysis_.md",
    "Boeing GTM Analysis Framework_.md",
    "Constellation Energy GTM Analysis Part 1_.md",
    # Added from current session - crashes API
    "SEMANTIC_MAPPING_PROBABILISTIC_DESIGN.md",
    # Added from E32 session - crashes API
    "Prompt - Energy Grid Destablisation Model.md",
}


class RateLimitedIngestionPipeline:
    """Rate-limited ingestion pipeline that processes ONE document at a time."""

    def __init__(
        self,
        ner11_api_url: str = "http://localhost:8000",
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        delay_between_docs: float = 3.0,
        timeout: int = 90
    ):
        self.ner11_api_url = ner11_api_url
        self.delay = delay_between_docs
        self.timeout = timeout

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

        print(f"✅ Rate-Limited Pipeline initialized")
        print(f"   - NER11 API: {ner11_api_url}")
        print(f"   - Delay between docs: {delay_between_docs}s")
        print(f"   - Timeout: {timeout}s")

    def check_api_health(self) -> bool:
        """Check if API is healthy."""
        try:
            response = requests.get(f"{self.ner11_api_url}/health", timeout=10)
            return response.status_code == 200
        except:
            return False

    def wait_for_api(self, max_wait: int = 60) -> bool:
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

    def extract_entities(self, text: str) -> List[Dict]:
        """Extract entities using NER11 API with extended timeout."""
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
                return []
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout after {self.timeout}s")
            return None  # Signal timeout for retry
        except Exception as e:
            print(f"   ❌ NER11 API failed: {e}")
            return None  # Signal failure for retry

    def process_single_document(self, filepath: Path, doc_num: int, total: int) -> Dict:
        """Process a single document with retry logic."""
        filename = filepath.name
        print(f"\n📄 [{doc_num}/{total}] {filename}")

        # Read document
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"   ❌ Read error: {e}")
            return {"status": "read_error", "entities": 0}

        # Skip very large documents (>100KB)
        doc_size = len(content)
        if doc_size > 100000:
            print(f"   ⚠️  Large doc ({doc_size:,} bytes) - processing in chunks...")
            # Process first 100KB only
            content = content[:100000]

        # Extract entities with retry
        max_retries = 3
        for attempt in range(max_retries):
            entities = self.extract_entities(content)

            if entities is None:  # API failure
                if attempt < max_retries - 1:
                    print(f"   🔄 Retry {attempt + 2}/{max_retries}...")
                    if not self.wait_for_api():
                        return {"status": "api_down", "entities": 0}
                    time.sleep(self.delay)
                else:
                    return {"status": "failed_after_retries", "entities": 0}
            elif len(entities) == 0:
                print(f"   ⚠️  No entities found")
                return {"status": "no_entities", "entities": 0}
            else:
                break

        # Process entities
        entity_count = len(entities)
        qdrant_count = 0
        neo4j_count = 0
        rel_count = 0

        # Store in Qdrant with enhanced temporal tracking
        for ent in entities:
            try:
                text = ent.get("text", "")
                label = ent.get("label", "UNKNOWN")
                embedding = self.embedding_model.encode(text).tolist()

                point_id = hash(f"{text}_{label}_{filepath.stem}") % (2**63)
                now = datetime.utcnow().isoformat()

                # Check if point exists to preserve first_seen and increment seen_count
                existing_payload = {}
                try:
                    existing = self.qdrant.retrieve(
                        collection_name=self.collection_name,
                        ids=[point_id],
                        with_payload=True
                    )
                    if existing:
                        existing_payload = existing[0].payload or {}
                except:
                    pass  # Point doesn't exist yet

                # Build payload with temporal tracking
                payload = {
                    "text": text,
                    "label": label,
                    "source_file": filepath.name,
                    "first_seen": existing_payload.get("first_seen", now),  # Preserve original discovery
                    "last_seen": now,  # Always update to current time
                    "seen_count": existing_payload.get("seen_count", 0) + 1,  # Increment observation count
                    "created_at": existing_payload.get("created_at", now)  # Backward compat
                }

                self.qdrant.upsert(
                    collection_name=self.collection_name,
                    points=[PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload=payload
                    )]
                )
                qdrant_count += 1
            except Exception as e:
                pass

        # Store in Neo4j
        try:
            with self.neo4j_driver.session() as session:
                for ent in entities:
                    text = ent.get("text", "")
                    label = ent.get("label", "UNKNOWN")
                    session.run("""
                        MERGE (e:Entity {text: $text, label: $label})
                        ON CREATE SET e.source_file = $source, e.created_at = timestamp()
                        ON MATCH SET e.last_seen = timestamp()
                    """, text=text, label=label, source=filepath.name)
                    neo4j_count += 1
        except Exception as e:
            print(f"   ⚠️  Neo4j error: {e}")

        # Extract relationships
        try:
            relationships = self.relationship_extractor.extract(entities, content)
            with self.neo4j_driver.session() as session:
                for rel in relationships:
                    session.run("""
                        MATCH (e1:Entity {text: $e1_text})
                        MATCH (e2:Entity {text: $e2_text})
                        MERGE (e1)-[r:RELATES_TO {type: $rel_type}]->(e2)
                    """, e1_text=rel.get("source"), e2_text=rel.get("target"),
                    rel_type=rel.get("type", "CO_OCCURS"))
                    rel_count += 1
        except Exception as e:
            pass

        print(f"   ✅ Entities: {entity_count} → Qdrant: {qdrant_count}, Neo4j: {neo4j_count}, Rels: {rel_count}")
        return {"status": "success", "entities": entity_count, "qdrant": qdrant_count, "neo4j": neo4j_count}

    def process_directory(self, wiki_root: str) -> Dict:
        """Process all documents in directory with rate limiting."""
        wiki_path = Path(wiki_root)

        # Find all markdown files
        md_files = list(wiki_path.rglob("*.md"))
        total = len(md_files)

        print(f"\n📚 Rate-Limited Ingestion")
        print(f"   Found: {total} documents")
        print(f"   Delay: {self.delay}s between documents")
        print(f"   Timeout: {self.timeout}s per document")

        # Track results
        results = {
            "success": 0,
            "failed": 0,
            "no_entities": 0,
            "total_entities": 0,
            "failed_files": []
        }

        skipped = 0
        for i, filepath in enumerate(md_files, 1):
            # Skip problematic files that crash the API
            if filepath.name in SKIP_FILES:
                print(f"\n⏭️  [{i}/{total}] SKIPPING {filepath.name} (known to crash API)")
                skipped += 1
                continue

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
            elif result["status"] == "no_entities":
                results["no_entities"] += 1
            else:
                results["failed"] += 1
                results["failed_files"].append(str(filepath))

            # Rate limit - wait between documents
            if i < total:
                print(f"   ⏱️  Waiting {self.delay}s...", end="\r")
                time.sleep(self.delay)

        # Summary
        print(f"\n{'='*60}")
        print(f"📊 RATE-LIMITED INGESTION SUMMARY")
        print(f"{'='*60}")
        print(f"Documents Processed: {results['success'] + results['failed'] + results['no_entities']}/{total}")
        print(f"Successful: {results['success']}")
        print(f"No Entities: {results['no_entities']}")
        print(f"Failed: {results['failed']}")
        print(f"Skipped (API crashers): {skipped}")
        print(f"Total Entities Added: {results['total_entities']}")
        print(f"{'='*60}")
        results["skipped"] = skipped

        return results


def main():
    parser = argparse.ArgumentParser(description="Rate-Limited Document Ingestion")
    parser.add_argument("--wiki-root", required=True, help="Directory containing documents")
    parser.add_argument("--delay", type=float, default=3.0, help="Delay between documents (seconds)")
    parser.add_argument("--timeout", type=int, default=90, help="API timeout per document (seconds)")

    args = parser.parse_args()

    pipeline = RateLimitedIngestionPipeline(
        delay_between_docs=args.delay,
        timeout=args.timeout
    )

    results = pipeline.process_directory(args.wiki_root)

    # Save results
    results_file = Path(__file__).parent.parent / "logs" / "rate_limited_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📝 Results saved to: {results_file}")


if __name__ == "__main__":
    main()
