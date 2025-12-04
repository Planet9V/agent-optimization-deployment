#!/usr/bin/env python3
"""
E30 Safe Ingestion Script - Defensive Rate-Limited Processing
Designed to NEVER crash the NER11 API by skipping problematic documents immediately.

Key Features:
- 8-second delay between documents (conservative)
- 30-second timeout (fail fast on problematic docs)
- IMMEDIATE skip on any error (no retries that could crash API)
- Tracks skipped files for later review
- Verifies NER11 v3 model is loaded before starting

Usage:
    python3 scripts/safe_ingest_e30.py --wiki-root "/path/to/docs" --delay 8
"""

import sys
import os
import requests
import json
import time
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

# Files known to crash NER11 API - NEVER process these
SKIP_FILES = {
    # Original API crashers
    "ANZ_Rail Cybersecurity Thrats_2025_10.md",
    "QTMP_Rail Cyberthreat Research_2025_10.md",
    "PHASE_1_EXECUTION_STATUS.md",
    "AGENT_ARCHITECTURE_SPECIALIZED.md",
    "PILOT_DEEP_ANALYSIS_STRATEGIC_INTELLIGENCE_REPORT.md",
    "AEON_Complete_Technical_White_Paper.md",
    "V9_ANALYSIS_COMPLETION_REPORT.md",
    # E30 session crashers
    "Casper Sleep Inc. GTM Analysis_.md",
    "GE Go-to-Market Analysis_.md",
    "Boeing GTM Analysis Framework_.md",
    "Constellation Energy GTM Analysis Part 1_.md",
    "SEMANTIC_MAPPING_PROBABILISTIC_DESIGN.md",
    "Prompt - Energy Grid Destablisation Model.md",
}


class SafeIngestionPipeline:
    """Defensive ingestion pipeline - skips immediately on any issue."""

    def __init__(
        self,
        ner11_api_url: str = "http://localhost:8000",
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        delay_between_docs: float = 8.0,  # SLOWER - 8 seconds
        timeout: int = 30  # SHORTER - fail fast
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

        print(f"\n{'='*60}")
        print(f"🛡️  E30 SAFE INGESTION PIPELINE")
        print(f"{'='*60}")
        print(f"   NER11 API: {ner11_api_url}")
        print(f"   Delay: {delay_between_docs}s (conservative)")
        print(f"   Timeout: {timeout}s (fail fast)")
        print(f"   Strategy: SKIP immediately on any error")
        print(f"{'='*60}")

    def verify_ner11_v3(self) -> bool:
        """Verify NER11 v3 Gold Model is loaded."""
        try:
            response = requests.get(f"{self.ner11_api_url}/info", timeout=10)
            if response.status_code == 200:
                info = response.json()
                version = info.get("version", "unknown")
                labels = info.get("labels", [])
                print(f"\n✅ NER11 Model Verified:")
                print(f"   Version: {version}")
                print(f"   Labels: {len(labels)} (including ner11_v3 labels)")
                return "3" in str(version) and len(labels) >= 50
            return False
        except Exception as e:
            print(f"❌ Failed to verify NER11: {e}")
            return False

    def check_api_health(self) -> bool:
        """Quick API health check."""
        try:
            response = requests.get(f"{self.ner11_api_url}/health", timeout=5)
            return response.status_code == 200 and response.json().get("status") == "healthy"
        except:
            return False

    def wait_for_api(self, max_wait: int = 120) -> bool:
        """Wait for API to recover after potential issue."""
        print("   ⏳ Waiting for API recovery...", end="", flush=True)
        for i in range(max_wait):
            if self.check_api_health():
                print(f" OK after {i}s")
                return True
            time.sleep(1)
            if i % 15 == 14:
                print(".", end="", flush=True)
        print(" TIMEOUT!")
        return False

    def extract_entities_safe(self, text: str) -> Optional[List[Dict]]:
        """Extract entities - return None on ANY error (no retries)."""
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
                return None  # Skip on non-200
        except requests.exceptions.Timeout:
            return None  # Skip on timeout
        except Exception:
            return None  # Skip on any error

    def process_single_document(self, filepath: Path, doc_num: int, total: int) -> Dict:
        """Process single document - SKIP immediately on any issue."""
        filename = filepath.name
        relative_path = str(filepath).split("Import 1 NOV 2025/")[-1] if "Import 1 NOV 2025" in str(filepath) else filename
        print(f"\n📄 [{doc_num}/{total}] {relative_path[:60]}...")

        # Read document
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"   ⏭️  SKIP: Read error")
            return {"status": "skip_read_error", "entities": 0}

        # Limit document size to prevent API overload
        doc_size = len(content)
        if doc_size > 80000:  # 80KB limit (stricter)
            print(f"   ⏭️  SKIP: Too large ({doc_size:,} bytes)")
            return {"status": "skip_too_large", "entities": 0, "size": doc_size}

        # Skip nearly empty documents
        if doc_size < 100:
            print(f"   ⏭️  SKIP: Too small ({doc_size} bytes)")
            return {"status": "skip_too_small", "entities": 0}

        # Extract entities - NO RETRY
        entities = self.extract_entities_safe(content)

        if entities is None:
            print(f"   ⏭️  SKIP: API error/timeout")
            return {"status": "skip_api_error", "entities": 0}

        if len(entities) == 0:
            print(f"   ℹ️  No entities found")
            return {"status": "no_entities", "entities": 0}

        # Process entities
        entity_count = len(entities)
        qdrant_count = 0
        neo4j_count = 0

        # Store in Qdrant with temporal tracking
        for ent in entities:
            try:
                text = ent.get("text", "")
                label = ent.get("label", "UNKNOWN")

                if not text or len(text) < 2:
                    continue

                embedding = self.embedding_model.encode(text).tolist()
                point_id = hash(f"{text}_{label}_{filepath.stem}") % (2**63)
                now = datetime.utcnow().isoformat()

                # Check existing for temporal tracking
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
                    pass

                payload = {
                    "text": text,
                    "label": label,
                    "source_file": filepath.name,
                    "source_dir": str(filepath.parent.name),
                    "first_seen": existing_payload.get("first_seen", now),
                    "last_seen": now,
                    "seen_count": existing_payload.get("seen_count", 0) + 1,
                }

                self.qdrant.upsert(
                    collection_name=self.collection_name,
                    points=[PointStruct(id=point_id, vector=embedding, payload=payload)]
                )
                qdrant_count += 1
            except:
                pass

        # Store in Neo4j
        try:
            with self.neo4j_driver.session() as session:
                for ent in entities[:500]:  # Limit to prevent overload
                    text = ent.get("text", "")
                    label = ent.get("label", "UNKNOWN")
                    if text and len(text) >= 2:
                        session.run("""
                            MERGE (e:Entity {text: $text, label: $label})
                            ON CREATE SET e.source_file = $source, e.created_at = timestamp()
                            ON MATCH SET e.last_seen = timestamp()
                        """, text=text, label=label, source=filepath.name)
                        neo4j_count += 1
        except:
            pass

        print(f"   ✅ {entity_count} entities → Qdrant: {qdrant_count}")
        return {"status": "success", "entities": entity_count, "qdrant": qdrant_count, "neo4j": neo4j_count}

    def process_directory(self, wiki_root: str, already_processed: set = None) -> Dict:
        """Process all documents with safe rate limiting."""
        wiki_path = Path(wiki_root)
        already_processed = already_processed or set()

        # Find all markdown and text files
        all_files = list(wiki_path.rglob("*.md")) + list(wiki_path.rglob("*.txt"))

        # Filter out already processed and skip files
        files_to_process = []
        for f in all_files:
            if f.name in SKIP_FILES:
                continue
            if f.name in already_processed:
                continue
            files_to_process.append(f)

        total = len(files_to_process)

        print(f"\n📚 E30 SAFE INGESTION - REMAINING FILES")
        print(f"   Total found: {len(all_files)}")
        print(f"   Known crashers: {len(SKIP_FILES)} (will skip)")
        print(f"   Already processed: {len(already_processed)}")
        print(f"   To process: {total}")
        print(f"   Delay: {self.delay}s | Timeout: {self.timeout}s")
        print(f"   Estimated time: ~{(total * self.delay) / 60:.1f} minutes")

        results = {
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "no_entities": 0,
            "total_entities": 0,
            "skipped_files": [],
            "failed_files": [],
            "processed_files": []
        }

        start_time = time.time()

        for i, filepath in enumerate(files_to_process, 1):
            # Check API health every 10 documents
            if i % 10 == 1:
                if not self.check_api_health():
                    print(f"\n⚠️  API unhealthy at doc {i}, waiting...")
                    if not self.wait_for_api(120):
                        print(f"❌ API down, stopping")
                        break
                    time.sleep(self.delay * 2)  # Extra delay after recovery

            result = self.process_single_document(filepath, i, total)

            if result["status"] == "success":
                results["success"] += 1
                results["total_entities"] += result["entities"]
                results["processed_files"].append(filepath.name)
            elif result["status"] == "no_entities":
                results["no_entities"] += 1
                results["processed_files"].append(filepath.name)
            elif result["status"].startswith("skip"):
                results["skipped"] += 1
                results["skipped_files"].append({"file": filepath.name, "reason": result["status"]})
            else:
                results["failed"] += 1
                results["failed_files"].append(filepath.name)

            # Rate limit
            if i < total:
                time.sleep(self.delay)

            # Progress update every 50 docs
            if i % 50 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed * 60
                remaining = (total - i) / rate if rate > 0 else 0
                print(f"\n   📊 Progress: {i}/{total} ({i*100/total:.1f}%) | {rate:.1f} docs/min | ~{remaining:.0f}min left")

        elapsed = time.time() - start_time

        print(f"\n{'='*60}")
        print(f"📊 E30 SAFE INGESTION COMPLETE")
        print(f"{'='*60}")
        print(f"   Duration: {elapsed/60:.1f} minutes")
        print(f"   Processed: {results['success'] + results['no_entities']}/{total}")
        print(f"   Successful: {results['success']}")
        print(f"   No Entities: {results['no_entities']}")
        print(f"   Skipped: {results['skipped']}")
        print(f"   Failed: {results['failed']}")
        print(f"   Total Entities: {results['total_entities']:,}")
        print(f"{'='*60}")

        return results


def main():
    parser = argparse.ArgumentParser(description="E30 Safe Ingestion")
    parser.add_argument("--wiki-root", required=True, help="Directory containing documents")
    parser.add_argument("--delay", type=float, default=8.0, help="Delay between documents (default: 8s)")
    parser.add_argument("--timeout", type=int, default=30, help="API timeout (default: 30s)")
    parser.add_argument("--skip-already", type=str, default="", help="File with already processed filenames")

    args = parser.parse_args()

    # Load already processed files if provided
    already_processed = set()
    if args.skip_already and os.path.exists(args.skip_already):
        with open(args.skip_already, 'r') as f:
            already_processed = set(line.strip() for line in f)
        print(f"Loaded {len(already_processed)} already-processed files")

    pipeline = SafeIngestionPipeline(
        delay_between_docs=args.delay,
        timeout=args.timeout
    )

    # Verify NER11 v3 is loaded
    if not pipeline.verify_ner11_v3():
        print("❌ NER11 v3 not verified - please check the API")
        sys.exit(1)

    results = pipeline.process_directory(args.wiki_root, already_processed)

    # Save results
    results_file = Path(__file__).parent.parent / "logs" / "e30_safe_ingest_results.json"
    results_file.parent.mkdir(exist_ok=True)
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📝 Results saved to: {results_file}")

    # Save processed files list for future runs
    processed_file = Path(__file__).parent.parent / "logs" / "e30_processed_files.txt"
    with open(processed_file, 'w') as f:
        for name in results["processed_files"]:
            f.write(f"{name}\n")
    print(f"📝 Processed files list: {processed_file}")


if __name__ == "__main__":
    main()
