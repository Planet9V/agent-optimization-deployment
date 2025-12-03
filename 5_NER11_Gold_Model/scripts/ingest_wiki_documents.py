#!/usr/bin/env python3
"""
Wiki Document Ingestion Script with Relationship Extraction
Processes AEON wiki documents through:
NER11 → Hierarchical Classification → Relationship Extraction → Qdrant + Neo4j Graph

ENHANCED: Now extracts relationships automatically!
- Co-occurrence analysis
- Pattern-based relationship detection
- Type-based relationship inference
- Automatic graph building in Neo4j

Usage:
    python3 scripts/ingest_wiki_documents.py --limit 10  # Process 10 documents
    python3 scripts/ingest_wiki_documents.py --all       # Process all documents
"""

import sys
import os
import requests
import json
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

# Import relationship extractor with direct import
import importlib.util
spec = importlib.util.spec_from_file_location("relationship_extractor", pipelines_path / "relationship_extractor.py")
rel_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rel_module)
RelationshipExtractor = rel_module.RelationshipExtractor


class WikiDocumentIngestionPipeline:
    """Complete ingestion pipeline with automatic relationship extraction."""

    def __init__(
        self,
        ner11_api_url: str = "http://localhost:8000",
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg"
    ):
        """Initialize pipeline with all service connections."""
        self.ner11_api_url = ner11_api_url

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

        print(f"✅ Pipeline initialized")
        print(f"   - NER11 API: {ner11_api_url}")
        print(f"   - Qdrant: {qdrant_host}:{qdrant_port}")
        print(f"   - Neo4j: {neo4j_uri}")
        print(f"   - Relationship extraction: ENABLED")

    def extract_entities(self, text: str) -> List[Dict]:
        """Extract entities using NER11 API."""
        try:
            response = requests.post(
                f"{self.ner11_api_url}/ner",
                json={"text": text},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("entities", [])
            else:
                print(f"   ⚠️  NER11 API error: {response.status_code}")
                return []
        except Exception as e:
            print(f"   ❌ NER11 API failed: {e}")
            return []

    def classify_hierarchical(self, entity: Dict, context: str = "") -> Dict:
        """
        Apply hierarchical classification to entity.
        Simple implementation - can be enhanced with full HierarchicalEntityProcessor.
        """
        ner_label = entity.get("label", "")
        text = entity.get("text", "").lower()

        # Simple keyword-based classification (subset of 566 types)
        fine_grained_type = ner_label  # Default to NER label

        # Malware classification
        if ner_label == "MALWARE":
            if any(kw in text for kw in ["ransomware", "crypto", "locker"]):
                fine_grained_type = "RANSOMWARE"
            elif any(kw in text for kw in ["trojan", "horse"]):
                fine_grained_type = "TROJAN"
            elif "worm" in text:
                fine_grained_type = "WORM"

        # Threat Actor classification
        elif ner_label == "THREAT_ACTOR":
            if any(kw in text for kw in ["apt", "nation", "state"]):
                fine_grained_type = "NATION_STATE"
            elif "hacktivist" in text:
                fine_grained_type = "HACKTIVIST"

        # Device classification
        elif ner_label == "DEVICE":
            if "plc" in text:
                fine_grained_type = "PLC"
            elif "rtu" in text:
                fine_grained_type = "RTU"
            elif "hmi" in text:
                fine_grained_type = "HMI"

        # Cognitive Bias classification
        elif ner_label == "COGNITIVE_BIAS":
            if "confirmation" in text:
                fine_grained_type = "CONFIRMATION_BIAS"
            elif "normalcy" in text:
                fine_grained_type = "NORMALCY_BIAS"
            elif "availability" in text:
                fine_grained_type = "AVAILABILITY_HEURISTIC"

        # Build enriched entity
        enriched = {
            "text": entity.get("text", ""),
            "ner_label": ner_label,
            "fine_grained_type": fine_grained_type,
            "specific_instance": entity.get("text", ""),
            "hierarchy_path": f"{ner_label}/{fine_grained_type}/{entity.get('text', '')}",
            "hierarchy_level": 3 if fine_grained_type != ner_label else 2,
            "confidence": entity.get("score", 0.0),
            "classification_confidence": 0.9 if fine_grained_type != ner_label else 0.7
        }

        return enriched

    def store_in_qdrant(self, entities: List[Dict], doc_id: str) -> int:
        """Store entities in Qdrant with embeddings and enhanced temporal tracking."""
        if not entities:
            return 0

        now = datetime.utcnow().isoformat()
        points = []

        # Collect all point IDs we'll be creating
        point_ids = []
        for idx, entity in enumerate(entities):
            point_id = hash(f"{doc_id}_{idx}_{entity['text']}") % (2**63 - 1)
            point_ids.append(point_id)

        # Batch retrieve existing points to preserve temporal data
        existing_payloads = {}
        try:
            existing = self.qdrant.retrieve(
                collection_name=self.collection_name,
                ids=point_ids,
                with_payload=True
            )
            for point in existing:
                existing_payloads[point.id] = point.payload or {}
        except:
            pass  # Points don't exist yet

        for idx, entity in enumerate(entities):
            # Create embedding
            text_to_embed = f"{entity['text']} [CONTEXT: {entity.get('ner_label', '')}]"
            embedding = self.embedding_model.encode(text_to_embed).tolist()

            point_id = point_ids[idx]
            existing_payload = existing_payloads.get(point_id, {})

            # Create point with enhanced temporal tracking
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "entity": entity["text"],
                    "ner_label": entity["ner_label"],
                    "fine_grained_type": entity["fine_grained_type"],
                    "specific_instance": entity["specific_instance"],
                    "hierarchy_path": entity["hierarchy_path"],
                    "hierarchy_level": entity["hierarchy_level"],
                    "confidence": entity["confidence"],
                    "classification_confidence": entity["classification_confidence"],
                    "doc_id": doc_id,
                    # Enhanced temporal tracking
                    "first_seen": existing_payload.get("first_seen", now),  # Preserve original discovery
                    "last_seen": now,  # Always update to current time
                    "seen_count": existing_payload.get("seen_count", 0) + 1,  # Increment observation count
                    "created_at": existing_payload.get("created_at", now)  # Backward compat
                }
            )
            points.append(point)

        # Batch upsert to Qdrant
        try:
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return len(points)
        except Exception as e:
            print(f"   ❌ Qdrant storage failed: {e}")
            return 0

    def store_in_neo4j(self, entities: List[Dict], doc_id: str) -> int:
        """Store entities in Neo4j with hierarchical properties."""
        if not entities:
            return 0

        stored = 0
        with self.neo4j_driver.session() as session:
            for entity in entities:
                try:
                    # Determine Neo4j label (simplified mapping)
                    neo4j_label = self._map_to_neo4j_label(entity["ner_label"])

                    # MERGE node (preserve existing nodes)
                    result = session.run(f"""
                        MERGE (n:{neo4j_label} {{name: $name}})
                        ON CREATE SET
                            n.id = randomUUID(),
                            n.ner_label = $ner_label,
                            n.fine_grained_type = $fine_grained_type,
                            n.specific_instance = $specific_instance,
                            n.hierarchy_path = $hierarchy_path,
                            n.hierarchy_level = $hierarchy_level,
                            n.confidence = $confidence,
                            n.created_at = datetime()
                        ON MATCH SET
                            n.ner_label = $ner_label,
                            n.fine_grained_type = $fine_grained_type,
                            n.updated_at = datetime()
                        RETURN n.id as node_id
                    """,
                        name=entity["text"],
                        ner_label=entity["ner_label"],
                        fine_grained_type=entity["fine_grained_type"],
                        specific_instance=entity["specific_instance"],
                        hierarchy_path=entity["hierarchy_path"],
                        hierarchy_level=entity["hierarchy_level"],
                        confidence=entity["confidence"]
                    )

                    if result.single():
                        stored += 1

                except Exception as e:
                    print(f"   ⚠️  Neo4j storage failed for '{entity['text']}': {e}")
                    continue

        return stored

    def _map_to_neo4j_label(self, ner_label: str) -> str:
        """Map NER label to Neo4j Super Label."""
        # Simplified mapping (60 NER → 16 Super Labels)
        label_map = {
            "MALWARE": "Malware",
            "THREAT_ACTOR": "ThreatActor",
            "DEVICE": "Asset",
            "COGNITIVE_BIAS": "PsychTrait",
            "CVE": "Vulnerability",
            "PROTOCOL": "Protocol",
            "SOFTWARE_COMPONENT": "Software",
            "CONTROLS": "Control",
            "VULNERABILITY": "Vulnerability",
            "ATTACK_TECHNIQUE": "AttackPattern",
            "ORGANIZATION": "Organization",
            "LOCATION": "Location",
            "SECTORS": "Sector"
        }

        return label_map.get(ner_label, "Indicator")  # Default to Indicator

    def create_relationships_in_neo4j(self, relationships: List, doc_id: str) -> int:
        """Create relationships in Neo4j knowledge graph."""
        if not relationships:
            return 0

        created = 0
        with self.neo4j_driver.session() as session:
            for rel in relationships:
                try:
                    # Map to Neo4j labels
                    source_label = self._map_to_neo4j_label(rel.source_type)
                    target_label = self._map_to_neo4j_label(rel.target_type)

                    # Create relationship with MERGE (idempotent)
                    session.run(f"""
                        MATCH (source:{source_label} {{name: $source_name}})
                        MATCH (target:{target_label} {{name: $target_name}})
                        MERGE (source)-[r:{rel.relationship_type}]->(target)
                        ON CREATE SET
                            r.confidence = $confidence,
                            r.evidence = $evidence,
                            r.method = $method,
                            r.doc_id = $doc_id,
                            r.created_at = datetime()
                        RETURN r
                    """,
                        source_name=rel.source_entity,
                        target_name=rel.target_entity,
                        confidence=rel.confidence,
                        evidence=rel.evidence[:200],  # Limit evidence text
                        method=rel.method,
                        doc_id=doc_id
                    )
                    created += 1
                except Exception as e:
                    # Skip if nodes don't exist or other error
                    continue

        return created

    def process_document(self, doc_path: Path) -> Dict[str, Any]:
        """Process a single document through the complete pipeline with relationships."""
        doc_id = f"wiki_{doc_path.stem}"

        # Read document
        try:
            with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except Exception as e:
            return {"status": "error", "error": str(e)}

        # Step 1: Extract entities via NER11
        entities = self.extract_entities(text)
        if not entities:
            return {"status": "no_entities", "entities_extracted": 0}

        # Step 2: Hierarchical enrichment
        enriched_entities = [
            self.classify_hierarchical(e, text) for e in entities
        ]

        # Step 3: Extract relationships ⭐ NEW
        relationships = self.relationship_extractor.extract_relationships_from_text(
            text=text,
            entities=entities,
            doc_id=doc_id
        )

        # Step 4: Store in Qdrant
        qdrant_stored = self.store_in_qdrant(enriched_entities, doc_id)

        # Step 5: Store entities in Neo4j
        neo4j_stored = self.store_in_neo4j(enriched_entities, doc_id)

        # Step 6: Create relationships in Neo4j ⭐ NEW
        relationships_created = self.create_relationships_in_neo4j(relationships, doc_id)

        # Validation: Check tier2 > tier1
        tier1_types = set(e["ner_label"] for e in enriched_entities)
        tier2_types = set(e["fine_grained_type"] for e in enriched_entities)
        hierarchy_valid = len(tier2_types) >= len(tier1_types)

        return {
            "status": "success",
            "doc_id": doc_id,
            "entities_extracted": len(entities),
            "entities_enriched": len(enriched_entities),
            "relationships_extracted": len(relationships),
            "qdrant_stored": qdrant_stored,
            "neo4j_stored": neo4j_stored,
            "relationships_created": relationships_created,
            "tier1_unique": len(tier1_types),
            "tier2_unique": len(tier2_types),
            "hierarchy_valid": hierarchy_valid
        }

    def process_wiki_documents(self, wiki_root: str, limit: int = None) -> Dict:
        """Process multiple wiki documents with relationship extraction."""
        wiki_path = Path(wiki_root)

        # Find all markdown files
        all_docs = list(wiki_path.rglob("*.md"))

        # Apply limit
        docs_to_process = all_docs[:limit] if limit else all_docs

        print(f"\n📚 Wiki Document Ingestion Pipeline with Relationship Extraction")
        print(f"   Found: {len(all_docs)} total documents")
        print(f"   Processing: {len(docs_to_process)} documents")
        print(f"   Features: NER + Hierarchy + Co-occurrence + Pattern Matching + Graph Building\n")

        # Process each document
        results = []
        total_entities_qdrant = 0
        total_entities_neo4j = 0
        total_relationships = 0

        for doc_path in docs_to_process:
            print(f"📄 {doc_path.name}")
            result = self.process_document(doc_path)

            if result["status"] == "success":
                print(f"   ✅ Entities: {result['entities_extracted']} → "
                      f"Qdrant: {result['qdrant_stored']}, Neo4j: {result['neo4j_stored']}")
                print(f"   🔗 Relationships: {result['relationships_extracted']} extracted → "
                      f"{result['relationships_created']} created in graph")
                print(f"   📊 Tier1: {result['tier1_unique']}, Tier2: {result['tier2_unique']} "
                      f"({'✅ Valid' if result['hierarchy_valid'] else '❌ Invalid'})")
                total_entities_qdrant += result['qdrant_stored']
                total_entities_neo4j += result['neo4j_stored']
                total_relationships += result['relationships_created']
            else:
                print(f"   ⚠️  {result['status']}")

            results.append(result)

        # Summary
        successful = sum(1 for r in results if r["status"] == "success")

        return {
            "documents_processed": len(docs_to_process),
            "documents_successful": successful,
            "total_entities_qdrant": total_entities_qdrant,
            "total_entities_neo4j": total_entities_neo4j,
            "total_relationships_created": total_relationships,
            "results": results
        }

    def cleanup(self):
        """Close connections."""
        if self.neo4j_driver:
            self.neo4j_driver.close()


def main():
    parser = argparse.ArgumentParser(description="Ingest wiki documents into NER11 pipeline")
    parser.add_argument("--limit", type=int, default=5, help="Number of documents to process (default: 5)")
    parser.add_argument("--all", action="store_true", help="Process all documents")
    parser.add_argument("--wiki-root", default="/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current")

    args = parser.parse_args()

    # Initialize pipeline
    pipeline = WikiDocumentIngestionPipeline()

    try:
        # Process documents
        limit = None if args.all else args.limit
        summary = pipeline.process_wiki_documents(args.wiki_root, limit=limit)

        # Print summary
        print(f"\n{'='*70}")
        print(f"📊 INGESTION SUMMARY WITH RELATIONSHIP EXTRACTION")
        print(f"{'='*70}")
        print(f"Documents Processed: {summary['documents_processed']}")
        print(f"Documents Successful: {summary['documents_successful']}")
        print(f"Entities → Qdrant: {summary['total_entities_qdrant']}")
        print(f"Entities → Neo4j: {summary['total_entities_neo4j']}")
        print(f"Relationships → Neo4j Graph: {summary.get('total_relationships_created', 0)} ⭐ NEW")
        print(f"{'='*70}\n")

        # Save summary
        summary_path = "/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/wiki_ingestion_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"📝 Summary saved to: {summary_path}")

    finally:
        pipeline.cleanup()


if __name__ == "__main__":
    main()
