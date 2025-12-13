"""
Customer-Isolated Semantic Search Service
==========================================

NER30 Semantic Search with automatic multi-tenant customer isolation.
Extends the NER11 hierarchical embedding service with customer filtering.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import logging
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchAny

from .customer_context import (
    CustomerContext,
    CustomerContextManager,
    CustomerAccessLevel,
    require_customer_context,
)

logger = logging.getLogger(__name__)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class CustomerSemanticSearchRequest(BaseModel):
    """
    Request model for customer-isolated semantic search.

    Extends standard SemanticSearchRequest with customer isolation parameters.
    """
    query: str = Field(..., description="Search query text")
    limit: int = Field(default=10, ge=1, le=100, description="Max results")
    customer_id: str = Field(..., description="Customer identifier for isolation")

    # Hierarchical filters (NER11 taxonomy)
    label_filter: Optional[str] = Field(default=None, description="Tier 1: 60 NER labels")
    fine_grained_filter: Optional[str] = Field(default=None, description="Tier 2: 566 types")
    confidence_threshold: float = Field(default=0.0, ge=0.0, le=1.0)

    # Customer isolation options
    include_system: bool = Field(default=True, description="Include SYSTEM entities (CVEs, CWEs)")
    namespace: Optional[str] = Field(default=None, description="Customer namespace override")


class CustomerSemanticSearchResult(BaseModel):
    """Individual search result with customer context."""
    score: float
    entity: str
    ner_label: str
    fine_grained_type: str
    hierarchy_path: str
    confidence: float
    doc_id: str
    customer_id: str  # Added: Owner customer
    is_system: bool = False  # Added: True if from SYSTEM tenant


class CustomerSemanticSearchResponse(BaseModel):
    """Response model for customer-isolated semantic search."""
    results: List[CustomerSemanticSearchResult]
    query: str
    customer_id: str
    filters_applied: Dict[str, Any]
    total_results: int
    isolation_metadata: Dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# ISOLATED SEMANTIC SERVICE
# ============================================================================

class CustomerIsolatedSemanticService:
    """
    Semantic search service with automatic customer isolation.

    All searches are automatically filtered by customer_id, ensuring
    multi-tenant data isolation. SYSTEM entities (shared CVEs, CWEs, CAPECs)
    are optionally included based on configuration.

    Features:
    - Automatic customer_id filtering on all searches
    - Optional SYSTEM entity inclusion
    - Hierarchical NER11 taxonomy filtering
    - Audit logging for compliance
    - Performance optimization with filter caching
    """

    def __init__(
        self,
        qdrant_url: str = "http://openspg-qdrant:6333",
        collection_name: str = "ner11_gold_entities",
        embedding_model: Optional[Any] = None,
        api_key: Optional[str] = None,
    ):
        """
        Initialize customer-isolated semantic service.

        Args:
            qdrant_url: Qdrant server URL
            collection_name: Qdrant collection name
            embedding_model: Sentence transformer model for embeddings
            api_key: Optional Qdrant API key
        """
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self.api_key = api_key

        # Initialize Qdrant client
        self.client = QdrantClient(url=qdrant_url, api_key=api_key)

        # Initialize embedding model (lazy load if not provided)
        self._embedding_model = embedding_model

        logger.info(
            f"CustomerIsolatedSemanticService initialized: "
            f"url={qdrant_url}, collection={collection_name}"
        )

    @property
    def embedding_model(self):
        """Lazy load embedding model."""
        if self._embedding_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
                logger.info("Loaded default embedding model: all-MiniLM-L6-v2")
            except ImportError:
                raise RuntimeError(
                    "sentence-transformers not installed. "
                    "Install with: pip install sentence-transformers"
                )
        return self._embedding_model

    def _build_customer_filter(
        self,
        context: CustomerContext,
        additional_filters: Optional[List[FieldCondition]] = None
    ) -> Filter:
        """
        Build Qdrant filter with customer isolation.

        Args:
            context: Customer context for isolation
            additional_filters: Optional additional filter conditions

        Returns:
            Qdrant Filter object with customer isolation
        """
        customer_ids = context.get_customer_ids()

        must_conditions = [
            FieldCondition(
                key="customer_id",
                match=MatchAny(any=customer_ids)
            )
        ]

        if additional_filters:
            must_conditions.extend(additional_filters)

        return Filter(must=must_conditions)

    def _build_hierarchy_filters(
        self,
        ner_label: Optional[str] = None,
        fine_grained_type: Optional[str] = None,
        min_confidence: float = 0.0
    ) -> List[FieldCondition]:
        """
        Build hierarchical taxonomy filter conditions.

        Args:
            ner_label: Tier 1 NER label filter
            fine_grained_type: Tier 2 fine-grained type filter
            min_confidence: Minimum confidence threshold

        Returns:
            List of FieldCondition objects for hierarchy filtering
        """
        filters = []

        if ner_label:
            filters.append(
                FieldCondition(
                    key="ner_label",
                    match=MatchValue(value=ner_label)
                )
            )

        if fine_grained_type:
            filters.append(
                FieldCondition(
                    key="fine_grained_type",
                    match=MatchValue(value=fine_grained_type)
                )
            )

        if min_confidence > 0:
            filters.append(
                FieldCondition(
                    key="confidence",
                    range={"gte": min_confidence}
                )
            )

        return filters

    def search(
        self,
        request: CustomerSemanticSearchRequest,
    ) -> CustomerSemanticSearchResponse:
        """
        Execute customer-isolated semantic search.

        Args:
            request: Search request with customer context

        Returns:
            CustomerSemanticSearchResponse with isolated results
        """
        # Create customer context from request
        context = CustomerContext(
            customer_id=request.customer_id,
            namespace=request.namespace or request.customer_id.lower(),
            access_level=CustomerAccessLevel.READ,
            include_system=request.include_system,
        )

        # Set context for request lifecycle
        CustomerContextManager.set_context(context)

        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([request.query])[0].tolist()

            # Build hierarchy filters
            hierarchy_filters = self._build_hierarchy_filters(
                ner_label=request.label_filter,
                fine_grained_type=request.fine_grained_filter,
                min_confidence=request.confidence_threshold,
            )

            # Build complete filter with customer isolation
            query_filter = self._build_customer_filter(
                context=context,
                additional_filters=hierarchy_filters,
            )

            # Execute search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=query_filter,
                limit=request.limit,
            )

            # Format results with customer context
            formatted_results = []
            for point in results:
                payload = point.payload or {}
                result_customer_id = payload.get("customer_id", "UNKNOWN")

                formatted_results.append(
                    CustomerSemanticSearchResult(
                        score=point.score,
                        entity=payload.get("specific_instance", payload.get("entity", "")),
                        ner_label=payload.get("ner_label", ""),
                        fine_grained_type=payload.get("fine_grained_type", ""),
                        hierarchy_path=payload.get("hierarchy_path", ""),
                        confidence=payload.get("confidence", 0.0),
                        doc_id=payload.get("doc_id", ""),
                        customer_id=result_customer_id,
                        is_system=(result_customer_id == "SYSTEM"),
                    )
                )

            # Build response
            filters_applied = {
                "customer_ids": context.get_customer_ids(),
                "label_filter": request.label_filter,
                "fine_grained_filter": request.fine_grained_filter,
                "confidence_threshold": request.confidence_threshold,
            }

            response = CustomerSemanticSearchResponse(
                results=formatted_results,
                query=request.query,
                customer_id=request.customer_id,
                filters_applied=filters_applied,
                total_results=len(formatted_results),
                isolation_metadata={
                    "include_system": request.include_system,
                    "namespace": context.namespace,
                    "search_timestamp": datetime.utcnow().isoformat(),
                },
            )

            # Audit log
            logger.info(
                f"Customer semantic search: customer={request.customer_id}, "
                f"query='{request.query[:50]}...', results={len(formatted_results)}"
            )

            return response

        finally:
            CustomerContextManager.clear_context()

    def upsert_entity(
        self,
        entity_id: str,
        entity_text: str,
        embedding: List[float],
        payload: Dict[str, Any],
        context: CustomerContext,
    ) -> bool:
        """
        Upsert entity with automatic customer_id assignment.

        Args:
            entity_id: Unique entity identifier
            entity_text: Entity text for reference
            embedding: Entity embedding vector
            payload: Entity metadata
            context: Customer context for ownership

        Returns:
            True if upsert successful

        Raises:
            PermissionError: If context doesn't allow writes
        """
        if not context.can_write():
            raise PermissionError(
                f"Customer {context.customer_id} does not have write access"
            )

        # Add customer_id to payload
        payload["customer_id"] = context.customer_id
        payload["namespace"] = context.namespace
        payload["created_at"] = datetime.utcnow().isoformat()
        payload["created_by"] = context.user_id or "system"

        from qdrant_client.models import PointStruct

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=entity_id,
                    vector=embedding,
                    payload=payload,
                )
            ],
        )

        logger.info(
            f"Entity upserted: id={entity_id}, customer={context.customer_id}"
        )

        return True


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_isolated_semantic_service(
    qdrant_url: str = "http://openspg-qdrant:6333",
    collection_name: str = "ner11_gold_entities",
    api_key: Optional[str] = None,
) -> CustomerIsolatedSemanticService:
    """
    Factory function to create customer-isolated semantic service.

    Args:
        qdrant_url: Qdrant server URL
        collection_name: Collection name
        api_key: Optional API key

    Returns:
        Configured CustomerIsolatedSemanticService
    """
    return CustomerIsolatedSemanticService(
        qdrant_url=qdrant_url,
        collection_name=collection_name,
        api_key=api_key,
    )
