"""
NER30 Semantic Search API Router with Customer Isolation
========================================================

FastAPI router for customer-isolated semantic search endpoints.
Integrates with CUSTOMER_LABELS Phase B1 for multi-tenant isolation.

Version: 1.0.0
Created: 2025-12-04
"""

from fastapi import APIRouter, HTTPException, Header, Depends, Query
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

from .customer_context import (
    CustomerContext,
    CustomerContextManager,
    CustomerAccessLevel,
)
from .isolated_semantic_service import (
    CustomerIsolatedSemanticService,
    CustomerSemanticSearchRequest,
    CustomerSemanticSearchResponse,
    create_isolated_semantic_service,
)

logger = logging.getLogger(__name__)

# Create router with prefix
router = APIRouter(
    prefix="/api/v2/search",
    tags=["semantic-search", "customer-isolation"],
)

# Global service instance (initialize on startup)
_semantic_service: Optional[CustomerIsolatedSemanticService] = None


def get_semantic_service() -> CustomerIsolatedSemanticService:
    """Dependency to get semantic service instance."""
    global _semantic_service
    if _semantic_service is None:
        _semantic_service = create_isolated_semantic_service()
    return _semantic_service


def get_customer_context(
    x_customer_id: str = Header(..., description="Customer ID for isolation"),
    x_namespace: Optional[str] = Header(None, description="Optional namespace"),
    x_user_id: Optional[str] = Header(None, description="User ID for audit"),
    include_system: bool = Query(True, description="Include SYSTEM entities"),
) -> CustomerContext:
    """
    Dependency to extract and validate customer context from request headers.

    Required Headers:
        X-Customer-ID: Customer identifier for isolation

    Optional Headers:
        X-Namespace: Customer namespace (defaults to customer_id)
        X-User-ID: User identifier for audit trail
    """
    if not x_customer_id:
        raise HTTPException(
            status_code=400,
            detail="X-Customer-ID header is required"
        )

    return CustomerContext(
        customer_id=x_customer_id,
        namespace=x_namespace or x_customer_id.lower().replace("-", "_"),
        access_level=CustomerAccessLevel.READ,
        user_id=x_user_id,
        include_system=include_system,
    )


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post(
    "/semantic",
    response_model=CustomerSemanticSearchResponse,
    summary="Customer-Isolated Semantic Search",
    description="""
    Semantic search with automatic customer isolation.

    All results are filtered by customer_id to ensure multi-tenant data isolation.
    Optionally includes SYSTEM entities (shared CVEs, CWEs, CAPECs).

    **Hierarchical Filtering:**
    - Tier 1: label_filter (60 NER labels)
    - Tier 2: fine_grained_filter (566 fine-grained types)

    **Required Headers:**
    - X-Customer-ID: Customer identifier

    **Optional Headers:**
    - X-Namespace: Customer namespace
    - X-User-ID: User identifier for audit
    """
)
async def semantic_search(
    query: str = Query(..., description="Search query text"),
    limit: int = Query(10, ge=1, le=100, description="Max results"),
    label_filter: Optional[str] = Query(None, description="Tier 1 NER label filter"),
    fine_grained_filter: Optional[str] = Query(None, description="Tier 2 fine-grained type"),
    confidence_threshold: float = Query(0.0, ge=0.0, le=1.0),
    context: CustomerContext = Depends(get_customer_context),
    service: CustomerIsolatedSemanticService = Depends(get_semantic_service),
):
    """
    Execute customer-isolated semantic search.

    Returns semantically similar entities filtered by customer_id.
    """
    try:
        # Create request
        request = CustomerSemanticSearchRequest(
            query=query,
            limit=limit,
            customer_id=context.customer_id,
            label_filter=label_filter,
            fine_grained_filter=fine_grained_filter,
            confidence_threshold=confidence_threshold,
            include_system=context.include_system,
            namespace=context.namespace,
        )

        # Execute search
        response = service.search(request)

        return response

    except Exception as e:
        logger.error(f"Semantic search error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


@router.post(
    "/semantic/body",
    response_model=CustomerSemanticSearchResponse,
    summary="Semantic Search with JSON Body",
    description="Alternative endpoint accepting full request body."
)
async def semantic_search_body(
    request: CustomerSemanticSearchRequest,
    service: CustomerIsolatedSemanticService = Depends(get_semantic_service),
):
    """
    Execute customer-isolated semantic search with JSON body.

    Use this endpoint when you need to pass all parameters in request body.
    """
    try:
        response = service.search(request)
        return response
    except Exception as e:
        logger.error(f"Semantic search error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


@router.get(
    "/health",
    summary="Service Health Check",
    response_model=Dict[str, Any],
)
async def health_check(
    service: CustomerIsolatedSemanticService = Depends(get_semantic_service),
):
    """Check semantic search service health."""
    try:
        # Check Qdrant connection
        collections = service.client.get_collections()
        collection_exists = any(
            c.name == service.collection_name
            for c in collections.collections
        )

        return {
            "status": "healthy",
            "service": "customer-isolated-semantic-search",
            "version": "1.0.0",
            "qdrant_connected": True,
            "collection_exists": collection_exists,
            "collection_name": service.collection_name,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }


@router.get(
    "/customers/{customer_id}/stats",
    summary="Customer Search Statistics",
    response_model=Dict[str, Any],
)
async def customer_stats(
    customer_id: str,
    context: CustomerContext = Depends(get_customer_context),
    service: CustomerIsolatedSemanticService = Depends(get_semantic_service),
):
    """
    Get search statistics for a specific customer.

    Returns entity counts and metadata for the customer's isolated data.
    """
    # Verify customer_id matches context (security check)
    if customer_id != context.customer_id:
        raise HTTPException(
            status_code=403,
            detail="Cannot access statistics for other customers"
        )

    try:
        # Count entities for customer
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        count = service.client.count(
            collection_name=service.collection_name,
            count_filter=Filter(
                must=[
                    FieldCondition(
                        key="customer_id",
                        match=MatchValue(value=customer_id)
                    )
                ]
            ),
        )

        return {
            "customer_id": customer_id,
            "namespace": context.namespace,
            "entity_count": count.count,
            "include_system_access": context.include_system,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Stats error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve stats: {str(e)}"
        )


# ============================================================================
# INITIALIZATION
# ============================================================================

def init_semantic_router(
    qdrant_url: str = "http://openspg-qdrant:6333",
    collection_name: str = "ner11_gold_entities",
    api_key: Optional[str] = None,
) -> APIRouter:
    """
    Initialize router with custom configuration.

    Args:
        qdrant_url: Qdrant server URL
        collection_name: Collection name
        api_key: Optional API key

    Returns:
        Configured APIRouter
    """
    global _semantic_service
    _semantic_service = create_isolated_semantic_service(
        qdrant_url=qdrant_url,
        collection_name=collection_name,
        api_key=api_key,
    )
    return router
