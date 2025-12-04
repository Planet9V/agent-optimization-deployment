"""
NER30 Semantic Search API - Customer Isolation Module
=====================================================

Multi-tenant customer isolation for NER30 Semantic Search API.
Integrates with CUSTOMER_LABELS enhancement from Phase B1.

Version: 1.0.0
Created: 2025-12-04
"""

from .customer_context import (
    CustomerContext,
    CustomerAccessLevel,
    CustomerContextManager,
    get_customer_context,
    require_customer_context,
)

from .isolated_semantic_service import (
    CustomerIsolatedSemanticService,
    CustomerSemanticSearchRequest,
    CustomerSemanticSearchResponse,
)

__all__ = [
    # Context management
    "CustomerContext",
    "CustomerAccessLevel",
    "CustomerContextManager",
    "get_customer_context",
    "require_customer_context",
    # Isolated services
    "CustomerIsolatedSemanticService",
    "CustomerSemanticSearchRequest",
    "CustomerSemanticSearchResponse",
]
