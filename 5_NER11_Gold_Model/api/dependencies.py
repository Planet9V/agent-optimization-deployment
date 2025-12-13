"""
API Dependencies Module
========================

Shared dependencies for FastAPI routers including Qdrant client
and customer access verification.

Version: 1.0.0
Created: 2025-12-04
"""

import os
from typing import Optional
from functools import lru_cache

from fastapi import Header, HTTPException, Depends
from qdrant_client import QdrantClient

from .customer_isolation import (
    CustomerContext,
    CustomerContextManager,
    CustomerAccessLevel,
)


# ============================================================================
# Qdrant Client Dependency
# ============================================================================

@lru_cache()
def get_qdrant_client() -> QdrantClient:
    """
    Get cached Qdrant client instance.

    Uses QDRANT_URL environment variable or defaults to localhost.

    Returns:
        QdrantClient: Configured Qdrant client instance
    """
    qdrant_url = os.getenv("QDRANT_URL", "http://openspg-qdrant:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if qdrant_api_key:
        return QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    return QdrantClient(url=qdrant_url)


# ============================================================================
# Customer Access Verification
# ============================================================================

async def verify_customer_access(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
    x_namespace: Optional[str] = Header(None, alias="X-Namespace"),
    x_access_level: Optional[str] = Header("read", alias="X-Access-Level"),
) -> CustomerContext:
    """
    Verify customer access and create context.

    Args:
        x_customer_id: Required customer identifier from header
        x_namespace: Optional namespace for multi-tenant isolation
        x_access_level: Access level (read, write, admin)

    Returns:
        CustomerContext: Validated customer context

    Raises:
        HTTPException: If customer ID is invalid or access denied
    """
    if not x_customer_id or len(x_customer_id.strip()) == 0:
        raise HTTPException(
            status_code=422,
            detail="X-Customer-ID header is required and cannot be empty"
        )

    # Normalize customer ID
    customer_id = x_customer_id.strip().lower()

    # Validate no injection attempts
    if any(c in customer_id for c in [';', '--', "'", '"', '\\', '\n', '\r']):
        raise HTTPException(
            status_code=422,
            detail="Invalid characters in customer ID"
        )

    # Parse access level
    try:
        access_level = CustomerAccessLevel(x_access_level.lower())
    except ValueError:
        access_level = CustomerAccessLevel.READ

    # Create customer context
    context = CustomerContextManager.create_context(
        customer_id=customer_id,
        namespace=x_namespace,
        access_level=access_level,
    )

    return context


# ============================================================================
# Optional Dependencies
# ============================================================================

async def get_optional_customer_context(
    x_customer_id: Optional[str] = Header(None, alias="X-Customer-ID"),
) -> Optional[CustomerContext]:
    """
    Get optional customer context (for endpoints that support public access).

    Returns:
        Optional[CustomerContext]: Customer context if provided, None otherwise
    """
    if not x_customer_id:
        return None

    return await verify_customer_access(x_customer_id=x_customer_id)


# ============================================================================
# Admin Dependencies
# ============================================================================

async def verify_admin_access(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
    x_admin_token: str = Header(..., alias="X-Admin-Token"),
) -> CustomerContext:
    """
    Verify admin-level access.

    Args:
        x_customer_id: Customer identifier
        x_admin_token: Admin authentication token

    Returns:
        CustomerContext: Admin-level customer context

    Raises:
        HTTPException: If admin access denied
    """
    expected_token = os.getenv("ADMIN_TOKEN", "")

    if not expected_token or x_admin_token != expected_token:
        raise HTTPException(
            status_code=403,
            detail="Admin access denied"
        )

    context = await verify_customer_access(
        x_customer_id=x_customer_id,
        x_access_level="admin"
    )

    return context


# ============================================================================
# SYSTEM Customer Access (for cross-tenant operations)
# ============================================================================

async def get_system_context() -> CustomerContext:
    """
    Get SYSTEM customer context for cross-tenant operations.

    Returns:
        CustomerContext: SYSTEM-level context
    """
    return CustomerContextManager.create_context(
        customer_id="SYSTEM",
        access_level=CustomerAccessLevel.ADMIN,
    )
