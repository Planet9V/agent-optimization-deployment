"""
Customer Context for NER30 Semantic Search API
==============================================

Provides customer isolation context management for multi-tenant semantic search.
Compatible with CUSTOMER_LABELS Phase B1 implementation.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any, Callable
from functools import wraps
from contextvars import ContextVar
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class CustomerAccessLevel(Enum):
    """Customer access levels for semantic search operations."""
    READ = "read"           # Search only
    WRITE = "write"         # Search + upsert entities
    ADMIN = "admin"         # Full access including delete


@dataclass
class CustomerContext:
    """
    Customer context for request-level isolation in semantic search.

    Attributes:
        customer_id: Unique customer identifier (e.g., "CUST-001")
        namespace: Customer namespace for isolation (e.g., "acme-corp")
        access_level: Access level for operations
        user_id: Optional user identifier for audit
        session_id: Optional session identifier
        include_system: Include SYSTEM entities (shared CVEs, CWEs, CAPECs)
        metadata: Additional context metadata
    """
    customer_id: str
    namespace: str
    access_level: CustomerAccessLevel = CustomerAccessLevel.READ
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    include_system: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate customer context on creation."""
        if not self.customer_id:
            raise ValueError("customer_id is required")
        if not self.namespace:
            raise ValueError("namespace is required")

    def get_customer_ids(self) -> List[str]:
        """
        Get list of customer IDs to include in search.

        Returns:
            List containing customer_id and optionally 'SYSTEM' for shared data.
        """
        if self.include_system:
            return [self.customer_id, "SYSTEM"]
        return [self.customer_id]

    def can_write(self) -> bool:
        """Check if context allows write operations."""
        return self.access_level in (CustomerAccessLevel.WRITE, CustomerAccessLevel.ADMIN)

    def can_admin(self) -> bool:
        """Check if context allows admin operations."""
        return self.access_level == CustomerAccessLevel.ADMIN

    def to_audit_dict(self) -> Dict[str, Any]:
        """Convert context to audit-friendly dictionary."""
        return {
            "customer_id": self.customer_id,
            "namespace": self.namespace,
            "access_level": self.access_level.value,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "include_system": self.include_system,
            "timestamp": datetime.utcnow().isoformat(),
        }


# Context variable for request-scoped customer context
_customer_context: ContextVar[Optional[CustomerContext]] = ContextVar(
    "customer_context", default=None
)


class CustomerContextManager:
    """
    Manager for customer context lifecycle.

    Provides context creation, storage, and retrieval for semantic search operations.
    Thread-safe using contextvars for request-scoped isolation.
    """

    @staticmethod
    def set_context(context: CustomerContext) -> None:
        """Set customer context for current request."""
        _customer_context.set(context)
        logger.debug(f"Customer context set: {context.customer_id}")

    @staticmethod
    def get_context() -> Optional[CustomerContext]:
        """Get customer context for current request."""
        return _customer_context.get()

    @staticmethod
    def clear_context() -> None:
        """Clear customer context after request completion."""
        _customer_context.set(None)
        logger.debug("Customer context cleared")

    @staticmethod
    def require_context() -> CustomerContext:
        """
        Get customer context or raise error if not set.

        Returns:
            CustomerContext for current request.

        Raises:
            ValueError: If no customer context is set.
        """
        context = _customer_context.get()
        if context is None:
            raise ValueError(
                "Customer context required but not set. "
                "Ensure request includes customer_id header or parameter."
            )
        return context

    @staticmethod
    def create_context(
        customer_id: str,
        namespace: Optional[str] = None,
        access_level: CustomerAccessLevel = CustomerAccessLevel.READ,
        user_id: Optional[str] = None,
        include_system: bool = True,
    ) -> CustomerContext:
        """
        Create and set a new customer context.

        Args:
            customer_id: Customer identifier
            namespace: Optional namespace (defaults to customer_id-based)
            access_level: Access level for operations
            user_id: Optional user identifier
            include_system: Include SYSTEM entities in searches

        Returns:
            Created CustomerContext
        """
        if namespace is None:
            namespace = customer_id.lower().replace("-", "_")

        context = CustomerContext(
            customer_id=customer_id,
            namespace=namespace,
            access_level=access_level,
            user_id=user_id,
            include_system=include_system,
        )

        CustomerContextManager.set_context(context)
        return context


def get_customer_context() -> Optional[CustomerContext]:
    """Convenience function to get current customer context."""
    return CustomerContextManager.get_context()


def require_customer_context(func: Callable) -> Callable:
    """
    Decorator to require customer context for a function.

    Usage:
        @require_customer_context
        def my_search_function(...):
            context = get_customer_context()
            # context is guaranteed to be set
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        context = CustomerContextManager.require_context()
        return func(*args, **kwargs)
    return wrapper


class CustomerContextMiddleware:
    """
    FastAPI middleware for automatic customer context extraction.

    Extracts customer_id from request headers or query parameters
    and sets up CustomerContext for the request lifecycle.
    """

    def __init__(self, app, header_name: str = "X-Customer-ID"):
        self.app = app
        self.header_name = header_name

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Extract customer_id from headers
            headers = dict(scope.get("headers", []))
            customer_id = headers.get(
                self.header_name.lower().encode(),
                b""
            ).decode()

            if customer_id:
                CustomerContextManager.create_context(
                    customer_id=customer_id,
                    access_level=CustomerAccessLevel.READ,
                )

            try:
                await self.app(scope, receive, send)
            finally:
                CustomerContextManager.clear_context()
        else:
            await self.app(scope, receive, send)
