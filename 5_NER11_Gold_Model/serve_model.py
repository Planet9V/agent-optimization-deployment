import spacy
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import sys

# Add pipelines directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pipelines'))

# Import hierarchical embedding service
try:
    # Try with numbered prefix first (actual file name)
    from pipelines import entity_embedding_service_hierarchical as emb_module
    NER11HierarchicalEmbeddingService = emb_module.NER11HierarchicalEmbeddingService
    EMBEDDING_SERVICE_AVAILABLE = True
except ImportError:
    try:
        # Fallback: try direct import
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "entity_embedding_service_hierarchical",
            os.path.join(os.path.dirname(__file__), "pipelines", "02_entity_embedding_service_hierarchical.py")
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
    description="High-performance Named Entity Recognition API using the NER11 Gold Standard Model with Hierarchical Semantic Search.",
    version="2.0.0"
)

# Global model variables
nlp = None
embedding_service = None
MODEL_PATH = os.getenv("MODEL_PATH", "models/ner11_v3/model-best")

@app.on_event("startup")
async def load_model():
    global nlp, embedding_service
    try:
        print(f"Loading NER11 Gold Standard model from {MODEL_PATH}...")
        nlp = spacy.load(MODEL_PATH)
        print("✅ NER model loaded successfully!")

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

    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise RuntimeError(f"Failed to load model: {e}")

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

@app.post("/ner", response_model=NerResponse)
async def extract_entities(request: TextRequest):
    """Extract named entities from text using NER11 Gold model."""
    if not nlp:
        raise HTTPException(status_code=503, detail="Model not loaded")

    doc = nlp(request.text)

    entities = []
    for ent in doc.ents:
        entities.append(Entity(
            text=ent.text,
            label=ent.label_,
            start=ent.start_char,
            end=ent.end_char
        ))

    return NerResponse(entities=entities, doc_length=len(doc))

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

@app.get("/health")
async def health_check():
    """Health check endpoint with service status."""
    ner_status = "loaded" if nlp else "not_loaded"
    embedding_status = "available" if embedding_service else "not_available"

    overall_status = "healthy" if nlp else "unhealthy"

    return {
        "status": overall_status,
        "ner_model": ner_status,
        "semantic_search": embedding_status,
        "version": "2.0.0"
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
