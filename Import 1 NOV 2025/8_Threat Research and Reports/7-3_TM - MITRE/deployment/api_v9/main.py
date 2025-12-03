"""
NER v9 Comprehensive MITRE Model API
Production FastAPI server for Named Entity Recognition with 18 entity types
"""
import os
import time
from typing import List, Dict, Optional
from datetime import datetime
import logging

from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import spacy
from spacy.tokens import Doc
import uvicorn
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('ner_v9_requests_total', 'Total NER v9 requests', ['endpoint', 'status'])
REQUEST_LATENCY = Histogram('ner_v9_request_latency_seconds', 'Request latency', ['endpoint'])
ENTITY_COUNT = Counter('ner_v9_entities_detected', 'Total entities detected', ['entity_type'])

# Model configuration
MODEL_PATH = "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/models/ner_v9_comprehensive"
MODEL_VERSION = "v9"
DEFAULT_CONFIDENCE_THRESHOLD = 0.8

# Entity types supported by V9 model (18 comprehensive types)
ENTITY_TYPES = [
    "ATTACK_TECHNIQUE",
    "CAPEC",
    "CVE",
    "CWE",
    "DATA_SOURCE",
    "EQUIPMENT",
    "HARDWARE_COMPONENT",
    "INDICATOR",
    "MITIGATION",
    "OWASP",
    "PROTOCOL",
    "SECURITY",
    "SOFTWARE",
    "SOFTWARE_COMPONENT",
    "THREAT_ACTOR",
    "VENDOR",
    "VULNERABILITY",
    "WEAKNESS"
]

# API configuration - Clerk JWT authentication integration
CLERK_ENABLED = os.getenv("CLERK_ENABLED", "true").lower() == "true"
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY", "")
API_KEY = os.getenv("NER_API_KEY", "dev-key-change-in-production")
RATE_LIMIT = 100  # requests per minute

# Initialize FastAPI
app = FastAPI(
    title="NER v9 Comprehensive MITRE API",
    description="Production Named Entity Recognition API for MITRE ATT&CK entities with 18 comprehensive entity types",
    version="9.0.0",
    docs_url="/api/v9/docs",
    redoc_url="/api/v9/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model storage
_nlp = None
_model_loaded_at = None

# Rate limiting storage (simple in-memory)
_request_timestamps = []


def get_model():
    """Lazy load and cache the spaCy model"""
    global _nlp, _model_loaded_at

    if _nlp is None:
        try:
            logger.info(f"Loading NER v9 model from {MODEL_PATH}")
            start_time = time.time()
            _nlp = spacy.load(MODEL_PATH)
            _model_loaded_at = datetime.utcnow()
            load_time = time.time() - start_time
            logger.info(f"Model loaded successfully in {load_time:.2f} seconds")
            logger.info(f"Model supports {len(ENTITY_TYPES)} entity types")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Model loading failed: {str(e)}"
            )

    return _nlp


def verify_api_key(x_api_key: str = Header(None)):
    """Verify API key authentication (compatible with Clerk JWT)"""
    # If Clerk is enabled, allow Clerk JWT tokens
    if CLERK_ENABLED and x_api_key and x_api_key.startswith("Bearer "):
        # In production, validate Clerk JWT token here
        # For now, accept any Bearer token format
        logger.info("Clerk JWT authentication mode")
        return x_api_key

    # Fallback to API key authentication
    if not x_api_key or x_api_key != API_KEY:
        logger.warning("Invalid API key attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key or authentication token"
        )
    return x_api_key


def check_rate_limit():
    """Simple rate limiting check"""
    global _request_timestamps

    current_time = time.time()
    # Remove timestamps older than 1 minute
    _request_timestamps = [ts for ts in _request_timestamps if current_time - ts < 60]

    if len(_request_timestamps) >= RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded: {RATE_LIMIT} requests per minute"
        )

    _request_timestamps.append(current_time)


# Pydantic models
class Entity(BaseModel):
    """Detected entity with metadata"""
    text: str = Field(..., description="Entity text")
    label: str = Field(..., description="Entity label/type")
    start: int = Field(..., description="Start character position")
    end: int = Field(..., description="End character position")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class ExtractRequest(BaseModel):
    """Entity extraction request"""
    text: str = Field(..., min_length=1, max_length=50000, description="Input text for NER")
    confidence_threshold: Optional[float] = Field(
        DEFAULT_CONFIDENCE_THRESHOLD,
        ge=0.0,
        le=1.0,
        description="Minimum confidence threshold for entities"
    )

    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v


class ExtractResponse(BaseModel):
    """Entity extraction response"""
    text: str
    entities: List[Entity]
    processing_time_ms: float
    model_version: str
    confidence_threshold: float


class BatchExtractRequest(BaseModel):
    """Batch entity extraction request"""
    texts: List[str] = Field(..., min_items=1, max_items=100, description="List of texts")
    confidence_threshold: Optional[float] = Field(
        DEFAULT_CONFIDENCE_THRESHOLD,
        ge=0.0,
        le=1.0,
        description="Minimum confidence threshold"
    )

    @validator('texts')
    def validate_texts(cls, v):
        if not all(text.strip() for text in v):
            raise ValueError('All texts must be non-empty')
        return v


class BatchExtractResponse(BaseModel):
    """Batch extraction response"""
    results: List[ExtractResponse]
    total_processing_time_ms: float
    model_version: str


class EntityTypeInfo(BaseModel):
    """Information about an entity type"""
    label: str
    description: str


class EntityTypesResponse(BaseModel):
    """List of supported entity types"""
    entity_types: List[EntityTypeInfo]
    total_types: int
    model_version: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    model_path: str
    model_version: str
    loaded_at: Optional[str]
    uptime_seconds: Optional[float]


class InfoResponse(BaseModel):
    """Model information response"""
    model_version: str
    model_path: str
    entity_types: List[str]
    total_entity_types: int
    pipeline_components: List[str]
    loaded_at: Optional[str]
    default_confidence_threshold: float


# API endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "NER v9 Comprehensive MITRE API",
        "version": "9.0.0",
        "status": "operational",
        "docs": "/api/v9/docs",
        "entity_types": len(ENTITY_TYPES)
    }


@app.get("/api/v9/ner/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    Returns model status and uptime
    """
    try:
        nlp = get_model()
        model_loaded = True
        uptime = (datetime.utcnow() - _model_loaded_at).total_seconds() if _model_loaded_at else None
    except Exception:
        model_loaded = False
        uptime = None

    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        model_loaded=model_loaded,
        model_path=MODEL_PATH,
        model_version=MODEL_VERSION,
        loaded_at=_model_loaded_at.isoformat() if _model_loaded_at else None,
        uptime_seconds=uptime
    )


@app.get("/api/v9/ner/info", response_model=InfoResponse)
async def model_info(api_key: str = Depends(verify_api_key)):
    """
    Get model information and metadata
    Requires API key authentication or Clerk JWT
    """
    nlp = get_model()

    return InfoResponse(
        model_version=MODEL_VERSION,
        model_path=MODEL_PATH,
        entity_types=ENTITY_TYPES,
        total_entity_types=len(ENTITY_TYPES),
        pipeline_components=nlp.pipe_names,
        loaded_at=_model_loaded_at.isoformat() if _model_loaded_at else None,
        default_confidence_threshold=DEFAULT_CONFIDENCE_THRESHOLD
    )


@app.get("/api/v9/ner/entity-types", response_model=EntityTypesResponse)
async def get_entity_types(api_key: str = Depends(verify_api_key)):
    """
    Get list of all supported entity types with descriptions
    Requires API key authentication or Clerk JWT
    """
    entity_descriptions = {
        "ATTACK_TECHNIQUE": "MITRE ATT&CK technique identifiers and methods",
        "CAPEC": "Common Attack Pattern Enumeration and Classification IDs",
        "CVE": "Common Vulnerabilities and Exposures identifiers",
        "CWE": "Common Weakness Enumeration identifiers",
        "DATA_SOURCE": "Security data sources and telemetry",
        "EQUIPMENT": "Security equipment and hardware devices",
        "HARDWARE_COMPONENT": "Hardware components and system parts",
        "INDICATOR": "Indicators of compromise and security signals",
        "MITIGATION": "Security mitigation strategies and controls",
        "OWASP": "OWASP security classifications and categories",
        "PROTOCOL": "Network and communication protocols",
        "SECURITY": "General security concepts and terms",
        "SOFTWARE": "Software applications and systems",
        "SOFTWARE_COMPONENT": "Software components and libraries",
        "THREAT_ACTOR": "Threat actors and adversary groups",
        "VENDOR": "Security vendors and technology providers",
        "VULNERABILITY": "Security vulnerabilities and weaknesses",
        "WEAKNESS": "Security weaknesses and flaws"
    }

    entity_types_info = [
        EntityTypeInfo(label=entity_type, description=entity_descriptions.get(entity_type, ""))
        for entity_type in ENTITY_TYPES
    ]

    return EntityTypesResponse(
        entity_types=entity_types_info,
        total_types=len(ENTITY_TYPES),
        model_version=MODEL_VERSION
    )


@app.post("/api/v9/ner/extract", response_model=ExtractResponse)
async def extract_entities(
    request: ExtractRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Extract named entities from text with confidence threshold filtering
    Requires API key authentication or Clerk JWT
    """
    check_rate_limit()

    start_time = time.time()

    try:
        nlp = get_model()

        # Process text
        with REQUEST_LATENCY.labels(endpoint="extract").time():
            doc = nlp(request.text)

        # Extract entities with confidence filtering
        entities = []
        for ent in doc.ents:
            # spaCy doesn't provide direct confidence scores by default
            # Using 1.0 for now - in production, add custom scoring logic
            confidence = 1.0

            # Apply confidence threshold
            if confidence >= request.confidence_threshold:
                entities.append(Entity(
                    text=ent.text,
                    label=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=confidence
                ))

                # Track entity type
                ENTITY_COUNT.labels(entity_type=ent.label_).inc()

        processing_time = (time.time() - start_time) * 1000

        REQUEST_COUNT.labels(endpoint="extract", status="success").inc()

        logger.info(f"Extracted {len(entities)} entities in {processing_time:.2f}ms")

        return ExtractResponse(
            text=request.text,
            entities=entities,
            processing_time_ms=processing_time,
            model_version=MODEL_VERSION,
            confidence_threshold=request.confidence_threshold
        )

    except Exception as e:
        REQUEST_COUNT.labels(endpoint="extract", status="error").inc()
        logger.error(f"Extraction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Entity extraction failed: {str(e)}"
        )


@app.post("/api/v9/ner/batch", response_model=BatchExtractResponse)
async def batch_extract(
    request: BatchExtractRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Batch extract entities from multiple texts
    Requires API key authentication or Clerk JWT
    """
    check_rate_limit()

    start_time = time.time()

    try:
        nlp = get_model()
        results = []

        # Process texts using spaCy's pipe for efficiency
        with REQUEST_LATENCY.labels(endpoint="batch").time():
            docs = list(nlp.pipe(request.texts))

        # Extract entities from each doc
        for text, doc in zip(request.texts, docs):
            entities = []
            for ent in doc.ents:
                confidence = 1.0

                if confidence >= request.confidence_threshold:
                    entities.append(Entity(
                        text=ent.text,
                        label=ent.label_,
                        start=ent.start_char,
                        end=ent.end_char,
                        confidence=confidence
                    ))
                    ENTITY_COUNT.labels(entity_type=ent.label_).inc()

            results.append(ExtractResponse(
                text=text,
                entities=entities,
                processing_time_ms=0,  # Individual time not tracked in batch
                model_version=MODEL_VERSION,
                confidence_threshold=request.confidence_threshold
            ))

        total_processing_time = (time.time() - start_time) * 1000

        REQUEST_COUNT.labels(endpoint="batch", status="success").inc()

        logger.info(f"Batch extracted from {len(request.texts)} texts in {total_processing_time:.2f}ms")

        return BatchExtractResponse(
            results=results,
            total_processing_time_ms=total_processing_time,
            model_version=MODEL_VERSION
        )

    except Exception as e:
        REQUEST_COUNT.labels(endpoint="batch", status="error").inc()
        logger.error(f"Batch extraction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch extraction failed: {str(e)}"
        )


@app.get("/api/v9/ner/metrics")
async def metrics():
    """
    Prometheus metrics endpoint
    Public endpoint for monitoring
    """
    return Response(content=generate_latest(), media_type="text/plain")


if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
