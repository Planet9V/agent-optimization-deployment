"""
FastAPI routes for SBOM APIs
Implements 4 core SBOM endpoints with multi-tenant isolation
"""

from fastapi import APIRouter, Header, HTTPException, status
from typing import Optional
from datetime import datetime
from uuid import uuid4

from .models import (
    SBOMAnalyzeRequest,
    SBOMAnalyzeResponse,
    SBOMDetailResponse,
    SBOMSummaryResponse,
    ComponentSearchRequest,
    ComponentSearchResponse,
    ComponentSearchResult,
    Component,
    ErrorResponse
)
from .database import SBOMDatabase

router = APIRouter(prefix="/api/v2/sbom", tags=["SBOM"])

# Initialize database (in production, use dependency injection)
db = SBOMDatabase()


def validate_customer_id(customer_id: Optional[str]) -> str:
    """Validate and return customer ID from headers"""
    if not customer_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-Customer-ID header is required"
        )
    return customer_id


@router.post(
    "/analyze",
    response_model=SBOMAnalyzeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Analyze and store SBOM",
    description="""
    Parse SBOM file (CycloneDX or SPDX format), extract components and dependencies,
    store in Neo4j graph database, and create Qdrant embeddings for semantic search.

    **ICE Score: 8.1**
    - Impact: 9 (Critical for vulnerability tracking)
    - Confidence: 9 (Well-defined SBOM standards)
    - Ease: 7 (Complex parsing and storage)
    """
)
async def analyze_sbom(
    request: SBOMAnalyzeRequest,
    x_customer_id: Optional[str] = Header(None, alias="X-Customer-ID")
) -> SBOMAnalyzeResponse:
    """
    Analyze SBOM file and store components in graph database

    Multi-tenant isolation: Uses X-Customer-ID header to isolate data
    """
    customer_id = validate_customer_id(x_customer_id)

    try:
        # Generate unique SBOM ID
        sbom_id = str(uuid4())

        # Parse components from SBOM content
        components = []

        if request.format == "cyclonedx":
            # Parse CycloneDX format
            cyclonedx_components = request.content.get("components", [])
            for comp in cyclonedx_components:
                component = Component(
                    name=comp.get("name", "unknown"),
                    version=comp.get("version", "0.0.0"),
                    purl=comp.get("purl"),
                    cpe=comp.get("cpe"),
                    license=comp.get("licenses", [{}])[0].get("license", {}).get("id") if comp.get("licenses") else None,
                    supplier=comp.get("supplier", {}).get("name")
                )
                components.append(component.model_dump())

        elif request.format == "spdx":
            # Parse SPDX format
            spdx_packages = request.content.get("packages", [])
            for pkg in spdx_packages:
                component = Component(
                    name=pkg.get("name", "unknown"),
                    version=pkg.get("versionInfo", "0.0.0"),
                    license=pkg.get("licenseConcluded"),
                    supplier=pkg.get("supplier")
                )
                components.append(component.model_dump())

        # Store in Neo4j
        result = db.create_sbom(
            sbom_id=sbom_id,
            project_name=request.project_name,
            project_version=request.project_version or "1.0.0",
            format=request.format,
            customer_id=customer_id,
            components=components
        )

        # Store component embeddings in Qdrant for semantic search
        for comp in components:
            db.store_component_embedding(
                component_id=comp['component_id'],
                name=comp['name'],
                version=comp['version'],
                sbom_id=sbom_id,
                project_name=request.project_name,
                customer_id=customer_id
            )

        return SBOMAnalyzeResponse(
            sbom_id=sbom_id,
            project_name=request.project_name,
            components_count=result["components_created"],
            vulnerabilities_count=0,  # Will be populated by vulnerability correlation
            created_at=datetime.utcnow(),
            customer_id=customer_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze SBOM: {str(e)}"
        )


@router.get(
    "/{sbom_id}",
    response_model=SBOMDetailResponse,
    summary="Get SBOM details",
    description="""
    Retrieve detailed SBOM information including components, vulnerabilities, and metadata.

    **ICE Score: 9.0**
    - Impact: 9 (Essential for SBOM inspection)
    - Confidence: 10 (Straightforward graph query)
    - Ease: 9 (Simple Neo4j query)
    """
)
async def get_sbom(
    sbom_id: str,
    x_customer_id: Optional[str] = Header(None, alias="X-Customer-ID")
) -> SBOMDetailResponse:
    """
    Retrieve SBOM details by ID

    Multi-tenant isolation: Queries filtered by customer_id
    """
    customer_id = validate_customer_id(x_customer_id)

    try:
        result = db.get_sbom(sbom_id, customer_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"SBOM {sbom_id} not found for customer {customer_id}"
            )

        # Convert components to Pydantic models
        components = [
            Component(**comp) for comp in result.get("components", [])
            if comp.get('name')  # Filter out null components
        ]

        return SBOMDetailResponse(
            sbom_id=result["sbom_id"],
            project_name=result["project_name"],
            project_version=result["project_version"],
            format=result["format"],
            components_count=result["components_count"],
            vulnerabilities_count=result["vulnerabilities_count"],
            high_severity_count=0,  # TODO: Calculate from CVE relationships
            critical_severity_count=0,
            created_at=result["created_at"],
            customer_id=result["customer_id"],
            components=components
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve SBOM: {str(e)}"
        )


@router.get(
    "/summary",
    response_model=SBOMSummaryResponse,
    summary="Get SBOM summary statistics",
    description="""
    Aggregate SBOM statistics including total counts and vulnerability risk levels.

    **ICE Score: 8.0**
    - Impact: 8 (Important for dashboards)
    - Confidence: 10 (Simple aggregation)
    - Ease: 8 (Straightforward query)
    """
)
async def get_sbom_summary(
    x_customer_id: Optional[str] = Header(None, alias="X-Customer-ID")
) -> SBOMSummaryResponse:
    """
    Get aggregate SBOM statistics for a customer

    Multi-tenant isolation: Aggregates filtered by customer_id
    """
    customer_id = validate_customer_id(x_customer_id)

    try:
        result = db.get_sbom_summary(customer_id)

        return SBOMSummaryResponse(
            total_sboms=result.get("total_sboms", 0),
            total_components=result.get("total_components", 0),
            total_vulnerabilities=result.get("total_vulnerabilities", 0),
            critical_vulnerabilities=result.get("critical_count", 0),
            high_vulnerabilities=result.get("high_count", 0),
            medium_vulnerabilities=result.get("medium_count", 0),
            low_vulnerabilities=result.get("low_count", 0),
            customer_id=customer_id,
            last_updated=datetime.utcnow()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve SBOM summary: {str(e)}"
        )


@router.post(
    "/components/search",
    response_model=ComponentSearchResponse,
    summary="Semantic search for SBOM components",
    description="""
    Semantic search across SBOM components using Qdrant vector similarity.
    Enables natural language queries like "find all Apache components with vulnerabilities".

    **ICE Score: 7.29**
    - Impact: 8 (Useful for discovery)
    - Confidence: 9 (Proven vector search)
    - Ease: 8 (Qdrant integration)
    """
)
async def search_components(
    request: ComponentSearchRequest,
    x_customer_id: Optional[str] = Header(None, alias="X-Customer-ID")
) -> ComponentSearchResponse:
    """
    Semantic search for components using vector similarity

    Multi-tenant isolation: Search filtered by customer_id
    """
    customer_id = validate_customer_id(x_customer_id)

    try:
        results = db.search_components(
            query=request.query,
            customer_id=customer_id,
            limit=request.limit,
            similarity_threshold=request.similarity_threshold
        )

        # Convert to response models
        search_results = [
            ComponentSearchResult(
                component_id=r["component_id"],
                name=r["name"],
                version=r["version"],
                sbom_id=r["sbom_id"],
                project_name=r["project_name"],
                similarity_score=r["similarity_score"],
                vulnerabilities_count=r.get("vulnerabilities_count", 0)
            )
            for r in results
        ]

        return ComponentSearchResponse(
            results=search_results,
            total_results=len(search_results),
            query=request.query,
            customer_id=customer_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Component search failed: {str(e)}"
        )


@router.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown"""
    db.close()
