"""
FastAPI Application Entry Point
SBOM Analysis APIs with Multi-Tenant Isolation
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

from api.v2.sbom import router as sbom_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="AEON Digital Twin - SBOM API",
    description="""
    Software Bill of Materials (SBOM) Analysis APIs for cybersecurity knowledge graph.

    ## Features
    - SBOM ingestion (CycloneDX, SPDX formats)
    - Component vulnerability correlation
    - Semantic search using vector embeddings
    - Multi-tenant data isolation
    - Neo4j graph storage
    - Qdrant vector search

    ## Authentication
    All endpoints require `X-Customer-ID` header for multi-tenant isolation.

    ## ICE Scores
    - POST /sbom/analyze: ICE 8.1 (High Impact, High Confidence)
    - GET /sbom/{id}: ICE 9.0 (Essential, Straightforward)
    - GET /sbom/summary: ICE 8.0 (Important, Simple)
    - POST /sbom/components/search: ICE 7.29 (Useful, Proven)
    """,
    version="1.0.0",
    contact={
        "name": "AEON Development Team",
        "url": "https://github.com/aeon-dt/sbom-api"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sbom_router)


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API information"""
    return {
        "service": "AEON SBOM API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "sbom_analyze": "/api/v2/sbom/analyze",
            "sbom_get": "/api/v2/sbom/{sbom_id}",
            "sbom_summary": "/api/v2/sbom/summary",
            "component_search": "/api/v2/sbom/components/search"
        },
        "documentation": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "operational",
            "neo4j": "operational",  # TODO: Add actual health checks
            "qdrant": "operational"
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
