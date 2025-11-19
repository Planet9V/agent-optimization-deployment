"""
NER v8 MITRE Model API
Production FastAPI server for Named Entity Recognition
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
REQUEST_COUNT = Counter('ner_requests_total', 'Total NER requests', ['endpoint', 'status'])
REQUEST_LATENCY = Histogram('ner_request_latency_seconds', 'Request latency', ['endpoint'])
ENTITY_COUNT = Counter('ner_entities_detected', 'Total entities detected', ['entity_type'])

# Model configuration
MODEL_PATH = "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/models/ner_v8_mitre"
MODEL_VERSION = "v8"
MODEL_PERFORMANCE = {
    "f1_score": 97.01,
    "precision": 94.20,
    "recall": 100.00
}

# API configuration
API_KEY = os.getenv("NER_API_KEY", "dev-key-change-in-production")
RATE_LIMIT = 100  # requests per minute

# Initialize FastAPI
app = FastAPI(
    title="NER v8 MITRE API",
    description="Production Named Entity Recognition API for MITRE ATT&CK entities",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
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
            logger.info(f"Loading NER model from {MODEL_PATH}")
            start_time = time.time()
            _nlp = spacy.load(MODEL_PATH)
            _model_loaded_at = datetime.utcnow()
            load_time = time.time() - start_time
            logger.info(f"Model loaded successfully in {load_time:.2f} seconds")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Model loading failed: {str(e)}"
            )

    return _nlp


def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key authentication"""
    if x_api_key != API_KEY:
        logger.warning("Invalid API key attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
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


class NERRequest(BaseModel):
    """Single text NER request"""
    text: str = Field(..., min_length=1, max_length=50000, description="Input text for NER")

    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v


class NERResponse(BaseModel):
    """NER prediction response"""
    text: str
    entities: List[Entity]
    processing_time_ms: float
    model_version: str


class BatchNERRequest(BaseModel):
    """Batch NER request"""
    texts: List[str] = Field(..., min_items=1, max_items=100, description="List of texts")

    @validator('texts')
    def validate_texts(cls, v):
        if not all(text.strip() for text in v):
            raise ValueError('All texts must be non-empty')
        return v


class BatchNERResponse(BaseModel):
    """Batch NER response"""
    results: List[NERResponse]
    total_processing_time_ms: float
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
    performance_metrics: Dict[str, float]
    entity_labels: List[str]
    pipeline_components: List[str]
    loaded_at: Optional[str]


# API endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "NER v8 MITRE API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/v1/docs"
    }


@app.get("/api/v1/ner/v8/health", response_model=HealthResponse)
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


@app.get("/api/v1/ner/v8/info", response_model=InfoResponse)
async def model_info(api_key: str = Depends(verify_api_key)):
    """
    Get model information and metadata
    Requires API key authentication
    """
    nlp = get_model()

    return InfoResponse(
        model_version=MODEL_VERSION,
        model_path=MODEL_PATH,
        performance_metrics=MODEL_PERFORMANCE,
        entity_labels=nlp.get_pipe("ner").labels if nlp.has_pipe("ner") else [],
        pipeline_components=nlp.pipe_names,
        loaded_at=_model_loaded_at.isoformat() if _model_loaded_at else None
    )


@app.post("/api/v1/ner/v8/predict", response_model=NERResponse)
async def predict_entities(
    request: NERRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Predict named entities in text
    Requires API key authentication
    """
    check_rate_limit()

    start_time = time.time()

    try:
        nlp = get_model()

        # Process text
        with REQUEST_LATENCY.labels(endpoint="predict").time():
            doc = nlp(request.text)

        # Extract entities with confidence scores
        entities = []
        for ent in doc.ents:
            # Get confidence score (if available from model)
            # spaCy doesn't provide direct confidence, using 1.0 as default
            # In production, you may want to add custom scoring
            confidence = 1.0

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

        REQUEST_COUNT.labels(endpoint="predict", status="success").inc()

        logger.info(f"Processed text with {len(entities)} entities in {processing_time:.2f}ms")

        return NERResponse(
            text=request.text,
            entities=entities,
            processing_time_ms=processing_time,
            model_version=MODEL_VERSION
        )

    except Exception as e:
        REQUEST_COUNT.labels(endpoint="predict", status="error").inc()
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/api/v1/ner/v8/batch", response_model=BatchNERResponse)
async def batch_predict(
    request: BatchNERRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Batch process multiple texts
    Requires API key authentication
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
                entities.append(Entity(
                    text=ent.text,
                    label=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=1.0
                ))
                ENTITY_COUNT.labels(entity_type=ent.label_).inc()

            results.append(NERResponse(
                text=text,
                entities=entities,
                processing_time_ms=0,  # Individual time not tracked in batch
                model_version=MODEL_VERSION
            ))

        total_processing_time = (time.time() - start_time) * 1000

        REQUEST_COUNT.labels(endpoint="batch", status="success").inc()

        logger.info(f"Batch processed {len(request.texts)} texts in {total_processing_time:.2f}ms")

        return BatchNERResponse(
            results=results,
            total_processing_time_ms=total_processing_time,
            model_version=MODEL_VERSION
        )

    except Exception as e:
        REQUEST_COUNT.labels(endpoint="batch", status="error").inc()
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )


@app.get("/api/v1/ner/v8/metrics")
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
        port=8000,
        reload=True,
        log_level="info"
    )
