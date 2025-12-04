"""
CUSTOMER_LABELS: Multi-Tenant Isolation Middleware
Phase B1 - MVP Enhancement 1 of 6

This module provides customer isolation for the NER11 Gold Model.
"""

from .customer_context import (
    CustomerContext,
    CustomerAccessLevel,
    CustomerContextManager,
    CustomerIsolatedSession,
    CustomerIsolationError,
    require_customer_context,
    CUSTOMER_QUERY_PATTERNS
)

__all__ = [
    'CustomerContext',
    'CustomerAccessLevel',
    'CustomerContextManager',
    'CustomerIsolatedSession',
    'CustomerIsolationError',
    'require_customer_context',
    'CUSTOMER_QUERY_PATTERNS'
]
