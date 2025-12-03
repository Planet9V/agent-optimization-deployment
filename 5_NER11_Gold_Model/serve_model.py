"""
NER11 Gold Standard API with Hybrid Search
==========================================

High-performance Named Entity Recognition API using the NER11 Gold Standard Model.
Features:
- Entity extraction (60 NER labels, 566 fine-grained types)
- Semantic search (Qdrant vector similarity)
- Hybrid search (Qdrant + Neo4j graph expansion)
- Hierarchical filtering (Tier 1, Tier 2, Tier 3)

Version: 3.0.0 (Phase 3: Hybrid Search)
"""

import spacy
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
import sys
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add utils directory to Python path for context augmentation imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

# Import context augmentation for improved short text NER
try:
    from context_augmentation import extract_pattern_entities, extract_with_augmentation
    CONTEXT_AUGMENTATION_AVAILABLE = True
    logger.info("✅ Context augmentation module loaded successfully")
except ImportError as e:
    CONTEXT_AUGMENTATION_AVAILABLE = False
    logger.warning(f"⚠️ Context augmentation not available: {e}")

# Import model validator for startup verification
try:
    from model_validator import (
        verify_model_checksums,
        health_check as validator_health_check,
        PRODUCTION_MODEL_ID,
        EXPECTED_CHECKSUMS,
        MODEL_BASE_PATH
    )
    MODEL_VALIDATOR_AVAILABLE = True
    logger.info("✅ Model validator module loaded successfully")
except ImportError as e:
    MODEL_VALIDATOR_AVAILABLE = False
    logger.warning(f"⚠️ Model validator not available: {e}")

# Add pipelines directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pipelines'))

# Import hierarchical embedding service
try:
    # Try direct import from pipelines directory
    from pipelines import entity_embedding_service_hierarchical as emb_module
    NER11HierarchicalEmbeddingService = emb_module.NER11HierarchicalEmbeddingService
    EMBEDDING_SERVICE_AVAILABLE = True
except ImportError:
    try:
        # Fallback: try with importlib using actual filename
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "entity_embedding_service_hierarchical",
            os.path.join(os.path.dirname(__file__), "pipelines", "entity_embedding_service_hierarchical.py")
        )
        emb_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(emb_module)
        NER11HierarchicalEmbeddingService = emb_module.NER11HierarchicalEmbeddingService
        EMBEDDING_SERVICE_AVAILABLE = True
    except Exception as import_error:
        EMBEDDING_SERVICE_AVAILABLE = False
        print(f"⚠️  Warning: Embedding service not available: {import_error}")
        print("   Semantic search endpoint will be disabled.")

# Initialize FastAPI app
app = FastAPI(
    title="NER11 Gold Standard API",
    description="High-performance Named Entity Recognition API with Hierarchical Semantic Search and Neo4j Graph Expansion.",
    version="3.3.0"
)

# Global model variables
nlp = None
nlp_fallback = None  # Fallback to en_core_web_trf for working NER
embedding_service = None
neo4j_driver = None
model_checksum_valid = False  # Track checksum validation status
MODEL_PATH = os.getenv("MODEL_PATH", "models/ner11_v3/model-best")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "en_core_web_trf")
USE_FALLBACK = os.getenv("USE_FALLBACK_NER", "true").lower() == "true"  # Enable fallback by default
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j@openspg")

@app.on_event("startup")
async def load_model():
    global nlp, nlp_fallback, embedding_service, neo4j_driver, model_checksum_valid
    try:
        print(f"Loading NER11 Gold Standard model from {MODEL_PATH}...")
        nlp = spacy.load(MODEL_PATH)
        print("✅ NER model loaded successfully!")

        # Verify model checksums at startup (using model_validator)
        if MODEL_VALIDATOR_AVAILABLE:
            try:
                from pathlib import Path
                model_path = Path(MODEL_PATH)
                checksum_valid, checksum_errors = verify_model_checksums(
                    PRODUCTION_MODEL_ID,
                    model_path
                )
                model_checksum_valid = checksum_valid
                if checksum_valid:
                    print(f"✅ Model checksum verification PASSED for {PRODUCTION_MODEL_ID}")
                else:
                    print(f"⚠️ Model checksum verification FAILED:")
                    for err in checksum_errors:
                        print(f"   - {err}")
            except Exception as checksum_error:
                print(f"⚠️ Could not verify checksums: {checksum_error}")
                model_checksum_valid = False
        else:
            print("⚠️ Model validator not available - skipping checksum verification")

        # Load fallback model for reliable NER extraction
        if USE_FALLBACK:
            try:
                print(f"Loading fallback model ({FALLBACK_MODEL})...")
                nlp_fallback = spacy.load(FALLBACK_MODEL)
                print(f"✅ Fallback model ({FALLBACK_MODEL}) loaded successfully!")
            except Exception as fallback_error:
                print(f"⚠️  Warning: Could not load fallback model: {fallback_error}")
                nlp_fallback = None

        # Initialize embedding service if available
        if EMBEDDING_SERVICE_AVAILABLE:
            try:
                print("Initializing hierarchical embedding service...")
                embedding_service = NER11HierarchicalEmbeddingService(
                    ner_api_url=os.getenv("NER_API_URL", "http://localhost:8000"),
                    qdrant_host=os.getenv("QDRANT_HOST", "localhost"),
                    qdrant_port=int(os.getenv("QDRANT_PORT", "6333")),
                    collection_name=os.getenv("QDRANT_COLLECTION", "ner11_entities_hierarchical")
                )
                print("✅ Embedding service initialized successfully!")
            except Exception as emb_error:
                print(f"⚠️  Warning: Could not initialize embedding service: {emb_error}")
                print("   Semantic search endpoint will be disabled.")

        # Initialize Neo4j connection for hybrid search
        try:
            print(f"Connecting to Neo4j at {NEO4J_URI}...")
            neo4j_driver = GraphDatabase.driver(
                NEO4J_URI,
                auth=(NEO4J_USER, NEO4J_PASSWORD)
            )
            # Verify connection
            with neo4j_driver.session() as session:
                session.run("RETURN 1")
            print("✅ Neo4j connection established successfully!")
        except Exception as neo4j_error:
            print(f"⚠️  Warning: Could not connect to Neo4j: {neo4j_error}")
            print("   Hybrid search graph expansion will be disabled.")
            neo4j_driver = None

    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise RuntimeError(f"Failed to load model: {e}")

@app.on_event("shutdown")
async def shutdown():
    global neo4j_driver
    if neo4j_driver:
        neo4j_driver.close()
        print("Neo4j connection closed.")

class TextRequest(BaseModel):
    text: str

class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int
    score: float = 1.0  # spaCy NER doesn't always give per-entity confidence, defaulting to 1.0

class NerResponse(BaseModel):
    entities: List[Entity]
    doc_length: int

class SemanticSearchRequest(BaseModel):
    """Request model for semantic search endpoint."""
    query: str
    limit: int = 10
    label_filter: Optional[str] = None  # Tier 1: 60 NER labels
    fine_grained_filter: Optional[str] = None  # Tier 2: 566 types - CRITICAL
    confidence_threshold: float = 0.0

class SemanticSearchResult(BaseModel):
    """Individual search result."""
    score: float
    entity: str
    ner_label: str
    fine_grained_type: str
    hierarchy_path: str
    confidence: float
    doc_id: str

class SemanticSearchResponse(BaseModel):
    """Response model for semantic search endpoint."""
    results: List[SemanticSearchResult]
    query: str
    filters_applied: Dict[str, Any]
    total_results: int


# ============================================================================
# HYBRID SEARCH MODELS (Task 3.1 - Phase 3)
# ============================================================================

class HybridSearchRequest(BaseModel):
    """Request model for hybrid search combining semantic + graph expansion."""
    query: str = Field(..., description="Search query text")
    limit: int = Field(default=10, ge=1, le=100, description="Max semantic results")
    expand_graph: bool = Field(default=True, description="Enable Neo4j graph expansion")
    hop_depth: int = Field(default=2, ge=1, le=3, description="Graph traversal depth (1-3 hops)")
    label_filter: Optional[str] = Field(default=None, description="Tier 1: NER label filter")
    fine_grained_filter: Optional[str] = Field(default=None, description="Tier 2: Fine-grained type filter")
    confidence_threshold: float = Field(default=0.0, ge=0.0, le=1.0, description="Min confidence")
    relationship_types: Optional[List[str]] = Field(
        default=None,
        description="Relationship types to follow (EXPLOITS, USES, TARGETS, AFFECTS, ATTRIBUTED_TO, MITIGATES, INDICATES)"
    )


class GraphEntity(BaseModel):
    """Entity from Neo4j graph expansion."""
    name: str
    label: str
    ner_label: Optional[str] = None
    fine_grained_type: Optional[str] = None
    hierarchy_path: Optional[str] = None
    hop_distance: int
    relationship: str
    relationship_direction: str  # "outgoing" or "incoming"


class HybridSearchResult(BaseModel):
    """Individual hybrid search result with graph context."""
    # Semantic match
    score: float
    entity: str
    ner_label: str
    fine_grained_type: str
    hierarchy_path: str
    confidence: float
    doc_id: str
    # Graph expansion
    related_entities: List[GraphEntity] = []
    graph_context: Dict[str, Any] = {}


class HybridSearchResponse(BaseModel):
    """Response model for hybrid search."""
    results: List[HybridSearchResult]
    query: str
    filters_applied: Dict[str, Any]
    total_semantic_results: int
    total_graph_entities: int
    graph_expansion_enabled: bool
    hop_depth: int
    performance_ms: float

@app.post("/ner", response_model=NerResponse)
async def extract_entities(request: TextRequest):
    """
    Extract named entities from text using enhanced multi-layer NER approach.

    Strategy (in priority order):
    1. Pattern-based extraction (HIGH confidence for CVE, APT, MITRE patterns)
    2. Fallback model (en_core_web_trf) for general NER
    3. Custom NER11 model for cybersecurity-specific entities

    The pattern-based extraction addresses the context-dependency issue where
    transformer models require longer context to identify short entities like
    "APT29", "CVE-2024-12345", or "T1566".
    """
    if not nlp and not nlp_fallback and not CONTEXT_AUGMENTATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="No NER model available")

    entities = []
    seen_spans = set()  # Track unique entity spans to avoid duplicates
    doc_length = len(request.text.split())  # Token count approximation

    # STEP 1: Pattern-based extraction (HIGH PRIORITY for cybersecurity entities)
    # This addresses context-dependency issue with short text inputs
    if CONTEXT_AUGMENTATION_AVAILABLE:
        pattern_entities = extract_pattern_entities(request.text)
        pattern_count = 0
        for ent in pattern_entities:
            span_key = (ent.start, ent.end)
            if span_key not in seen_spans:
                seen_spans.add(span_key)
                entities.append(Entity(
                    text=ent.text,
                    label=ent.label,
                    start=ent.start,
                    end=ent.end,
                    score=ent.confidence
                ))
                pattern_count += 1
        if pattern_count > 0:
            logger.info(f"Pattern extraction found {pattern_count} cybersecurity entities")

    # STEP 2: Fallback model (en_core_web_trf) for general NER coverage
    if nlp_fallback:
        doc = nlp_fallback(request.text)
        doc_length = len(doc)
        general_count = 0
        for ent in doc.ents:
            span_key = (ent.start_char, ent.end_char)
            if span_key not in seen_spans:
                seen_spans.add(span_key)
                entities.append(Entity(
                    text=ent.text,
                    label=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char
                ))
                general_count += 1
        if general_count > 0:
            logger.info(f"Fallback model (en_core_web_trf) added {general_count} entities")

    # STEP 3: Custom NER11 model for additional cybersecurity-specific entities
    if nlp:
        doc = nlp(request.text)
        if doc_length == 0:
            doc_length = len(doc)
        custom_count = 0
        for ent in doc.ents:
            span_key = (ent.start_char, ent.end_char)
            if span_key not in seen_spans:
                seen_spans.add(span_key)
                entities.append(Entity(
                    text=ent.text,
                    label=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char
                ))
                custom_count += 1
        if custom_count > 0:
            logger.info(f"Custom NER11 model added {custom_count} additional entities")

    # Sort entities by position for consistent output
    entities.sort(key=lambda x: x.start)

    logger.info(f"Total entities extracted: {len(entities)}")
    return NerResponse(entities=entities, doc_length=doc_length)

@app.post("/search/semantic", response_model=SemanticSearchResponse)
async def semantic_search(request: SemanticSearchRequest):
    """
    Semantic search with hierarchical filtering (Task 1.5).

    Search entities using semantic similarity with hierarchical taxonomy filtering:
    - Tier 1 filtering: label_filter (60 NER labels)
    - Tier 2 filtering: fine_grained_filter (566 fine-grained types) - KEY FEATURE
    - Confidence filtering: confidence_threshold

    Example queries:
    - "ransomware attack" → Find semantically similar malware entities
    - "SCADA systems" with fine_grained_filter="SCADA_SERVER" → Precise infrastructure search
    - "threat actors" with label_filter="THREAT_ACTOR" → Category-filtered search

    Returns results with complete hierarchy_path for each entity.
    """
    if not embedding_service:
        raise HTTPException(
            status_code=503,
            detail="Semantic search service not available. Ensure Qdrant is running and embedding service is initialized."
        )

    try:
        # Execute semantic search with hierarchical filters
        results = embedding_service.semantic_search(
            query=request.query,
            limit=request.limit,
            ner_label=request.label_filter,  # Tier 1 filter
            fine_grained_type=request.fine_grained_filter,  # Tier 2 filter - CRITICAL
            min_confidence=request.confidence_threshold
        )

        # Convert to response model
        search_results = [
            SemanticSearchResult(
                score=r["score"],
                entity=r["entity"],
                ner_label=r["ner_label"],
                fine_grained_type=r["fine_grained_type"],
                hierarchy_path=r["hierarchy_path"],
                confidence=r["confidence"],
                doc_id=r["doc_id"]
            )
            for r in results
        ]

        # Track applied filters
        filters_applied = {
            "label_filter": request.label_filter,
            "fine_grained_filter": request.fine_grained_filter,
            "confidence_threshold": request.confidence_threshold
        }

        return SemanticSearchResponse(
            results=search_results,
            query=request.query,
            filters_applied=filters_applied,
            total_results=len(search_results)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Semantic search failed: {str(e)}"
        )


# ============================================================================
# HYBRID SEARCH ENDPOINT (Task 3.1 - Phase 3)
# ============================================================================

def expand_graph_for_entity(entity_name: str, hop_depth: int = 2, relationship_types: Optional[List[str]] = None) -> List[GraphEntity]:
    """
    Expand Neo4j graph around an entity to find related entities.

    Args:
        entity_name: Name of the seed entity
        hop_depth: How many hops to traverse (1-3)
        relationship_types: Specific relationships to follow (None = all)

    Returns:
        List of related entities with relationship info
    """
    if not neo4j_driver:
        return []

    related = []

    try:
        with neo4j_driver.session() as session:
            # Build relationship pattern
            if relationship_types:
                rel_pattern = "|".join(relationship_types)
                rel_clause = f"[r:{rel_pattern}*1..{hop_depth}]"
            else:
                rel_clause = f"[r*1..{hop_depth}]"

            # Query for outgoing relationships (FIXED - proper handling of variable-length paths)
            outgoing_query = f"""
            MATCH (source {{name: $name}})
            CALL {{
                WITH source
                MATCH path = (source)-{rel_clause}->(target)
                WHERE source <> target
                RETURN target, path
                LIMIT 20
            }}
            WITH DISTINCT target, path
            RETURN target.name AS name,
                   labels(target)[0] AS label,
                   target.ner_label AS ner_label,
                   target.fine_grained_type AS fine_grained_type,
                   target.hierarchy_path AS hierarchy_path,
                   length(path) AS distance,
                   [rel IN relationships(path) | type(rel)][0] AS relationship
            """

            result = session.run(outgoing_query, name=entity_name)
            for record in result:
                if record["name"]:
                    related.append(GraphEntity(
                        name=record["name"],
                        label=record["label"] or "Unknown",
                        ner_label=record["ner_label"],
                        fine_grained_type=record["fine_grained_type"],
                        hierarchy_path=record["hierarchy_path"],
                        hop_distance=record["distance"] or 1,
                        relationship=record["relationship"] or "RELATED_TO",
                        relationship_direction="outgoing"
                    ))

            # Query for incoming relationships (FIXED - proper handling of variable-length paths)
            incoming_query = f"""
            MATCH (target {{name: $name}})
            CALL {{
                WITH target
                MATCH path = (source)-{rel_clause}->(target)
                WHERE source <> target
                RETURN source, path
                LIMIT 20
            }}
            WITH DISTINCT source, path
            RETURN source.name AS name,
                   labels(source)[0] AS label,
                   source.ner_label AS ner_label,
                   source.fine_grained_type AS fine_grained_type,
                   source.hierarchy_path AS hierarchy_path,
                   length(path) AS distance,
                   [rel IN relationships(path) | type(rel)][0] AS relationship
            """

            result = session.run(incoming_query, name=entity_name)
            for record in result:
                if record["name"]:
                    related.append(GraphEntity(
                        name=record["name"],
                        label=record["label"] or "Unknown",
                        ner_label=record["ner_label"],
                        fine_grained_type=record["fine_grained_type"],
                        hierarchy_path=record["hierarchy_path"],
                        hop_distance=record["distance"] or 1,
                        relationship=record["relationship"] or "RELATED_TO",
                        relationship_direction="incoming"
                    ))

    except Neo4jError as e:
        logger.warning(f"Neo4j graph expansion error: {e}")
    except Exception as e:
        logger.warning(f"Graph expansion error: {e}")

    return related


def get_graph_context(entity_name: str) -> Dict[str, Any]:
    """
    Get additional graph context for an entity.

    Args:
        entity_name: Name of the entity

    Returns:
        Dictionary with graph statistics and metadata
    """
    if not neo4j_driver:
        return {}

    context = {
        "node_exists": False,
        "outgoing_relationships": 0,
        "incoming_relationships": 0,
        "labels": [],
        "properties": {}
    }

    try:
        with neo4j_driver.session() as session:
            # Check node existence and get properties
            result = session.run("""
                MATCH (n {name: $name})
                RETURN labels(n) AS labels,
                       n.ner_label AS ner_label,
                       n.fine_grained_type AS fine_grained_type,
                       n.tier AS tier,
                       size([(n)-[]->() | 1]) AS outgoing,
                       size([(n)<-[]-() | 1]) AS incoming
            """, name=entity_name)

            record = result.single()
            if record:
                context["node_exists"] = True
                context["labels"] = record["labels"] or []
                context["outgoing_relationships"] = record["outgoing"] or 0
                context["incoming_relationships"] = record["incoming"] or 0
                context["properties"] = {
                    "ner_label": record["ner_label"],
                    "fine_grained_type": record["fine_grained_type"],
                    "tier": record["tier"]
                }

    except Exception as e:
        logger.warning(f"Graph context error: {e}")

    return context


@app.post("/search/hybrid", response_model=HybridSearchResponse)
async def hybrid_search(request: HybridSearchRequest):
    """
    Hybrid search combining semantic similarity (Qdrant) with graph expansion (Neo4j).

    This is the core Phase 3 feature that provides:
    1. Semantic search via Qdrant vector similarity
    2. Graph expansion via Neo4j relationship traversal
    3. Re-ranking based on combined scores
    4. Hierarchical filtering (Tier 1 + Tier 2)

    Example usage:
    ```
    POST /search/hybrid
    {
        "query": "APT29 ransomware attack",
        "expand_graph": true,
        "hop_depth": 2,
        "relationship_types": ["USES", "TARGETS", "ATTRIBUTED_TO"]
    }
    ```

    Returns entities with their graph context and related entities.
    Performance target: <500ms.
    """
    import time
    start_time = time.time()

    if not embedding_service:
        raise HTTPException(
            status_code=503,
            detail="Semantic search service not available. Ensure Qdrant is running."
        )

    try:
        # Step 1: Execute semantic search via Qdrant
        semantic_results = embedding_service.semantic_search(
            query=request.query,
            limit=request.limit,
            ner_label=request.label_filter,
            fine_grained_type=request.fine_grained_filter,
            min_confidence=request.confidence_threshold
        )

        # Step 2: Enrich with graph expansion if enabled
        hybrid_results = []
        total_graph_entities = 0

        for sr in semantic_results:
            entity_name = sr.get("entity", "")

            # Get related entities from Neo4j graph
            related_entities = []
            graph_context = {}

            if request.expand_graph and neo4j_driver:
                related_entities = expand_graph_for_entity(
                    entity_name=entity_name,
                    hop_depth=request.hop_depth,
                    relationship_types=request.relationship_types
                )
                graph_context = get_graph_context(entity_name)
                total_graph_entities += len(related_entities)

            # Build hybrid result
            hybrid_result = HybridSearchResult(
                score=sr.get("score", 0.0),
                entity=entity_name,
                ner_label=sr.get("ner_label", ""),
                fine_grained_type=sr.get("fine_grained_type", ""),
                hierarchy_path=sr.get("hierarchy_path", ""),
                confidence=sr.get("confidence", 0.0),
                doc_id=sr.get("doc_id", ""),
                related_entities=related_entities,
                graph_context=graph_context
            )
            hybrid_results.append(hybrid_result)

        # Step 3: Re-rank results (semantic score + graph connectivity boost)
        for result in hybrid_results:
            graph_boost = min(0.1 * len(result.related_entities), 0.3)  # Max 30% boost
            result.score = min(1.0, result.score + graph_boost)

        # Sort by adjusted score
        hybrid_results.sort(key=lambda x: x.score, reverse=True)

        # Calculate performance
        elapsed_ms = (time.time() - start_time) * 1000

        # Build response
        filters_applied = {
            "label_filter": request.label_filter,
            "fine_grained_filter": request.fine_grained_filter,
            "confidence_threshold": request.confidence_threshold,
            "relationship_types": request.relationship_types
        }

        return HybridSearchResponse(
            results=hybrid_results,
            query=request.query,
            filters_applied=filters_applied,
            total_semantic_results=len(semantic_results),
            total_graph_entities=total_graph_entities,
            graph_expansion_enabled=request.expand_graph and neo4j_driver is not None,
            hop_depth=request.hop_depth,
            performance_ms=round(elapsed_ms, 2)
        )

    except Exception as e:
        logger.error(f"Hybrid search failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Hybrid search failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint with service status and model validation."""
    ner_custom_status = "loaded" if nlp else "not_loaded"
    ner_fallback_status = "loaded" if nlp_fallback else "not_loaded"
    embedding_status = "available" if embedding_service else "not_available"
    neo4j_status = "connected" if neo4j_driver else "not_connected"
    pattern_extraction_status = "enabled" if CONTEXT_AUGMENTATION_AVAILABLE else "disabled"
    checksum_status = "verified" if model_checksum_valid else "not_verified"

    # Healthy if any NER capability is available (pattern, custom, or fallback)
    overall_status = "healthy" if (nlp or nlp_fallback or CONTEXT_AUGMENTATION_AVAILABLE) else "unhealthy"

    return {
        "status": overall_status,
        "ner_model_custom": ner_custom_status,
        "ner_model_fallback": ner_fallback_status,
        "model_checksum": checksum_status,  # NEW: checksum verification status
        "model_validator": "available" if MODEL_VALIDATOR_AVAILABLE else "not_available",
        "pattern_extraction": pattern_extraction_status,
        "ner_extraction": "enabled" if (nlp or nlp_fallback or CONTEXT_AUGMENTATION_AVAILABLE) else "disabled",
        "semantic_search": embedding_status,
        "neo4j_graph": neo4j_status,
        "version": "3.3.0"  # Updated for model validation support
    }

@app.get("/info")
async def model_info():
    """Model information and capabilities."""
    if not nlp:
        return {"status": "model_not_loaded"}

    info = {
        "model_name": "NER11 Gold Standard",
        "version": "3.0",
        "api_version": "2.0.0",
        "pipeline": nlp.pipe_names,
        "labels": nlp.get_pipe("ner").labels,
        "capabilities": {
            "named_entity_recognition": True,
            "semantic_search": embedding_service is not None,
            "hierarchical_filtering": embedding_service is not None
        }
    }

    if embedding_service:
        info["hierarchy_info"] = {
            "tier1_labels": 60,
            "tier2_types": 566,
            "collection": os.getenv("QDRANT_COLLECTION", "ner11_entities_hierarchical"),
            "filtering": {
                "label_filter": "Tier 1 NER label filtering",
                "fine_grained_filter": "Tier 2 fine-grained type filtering (566 types)",
                "confidence_threshold": "Minimum confidence filtering"
            }
        }

    return info

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
