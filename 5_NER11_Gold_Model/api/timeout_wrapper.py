"""
Timeout Wrapper Utility
=======================

Provides timeout protection for database queries and async operations.

Version: 1.0.0
"""

import asyncio
from functools import wraps
from typing import TypeVar, Callable, Any
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class TimeoutError(Exception):
    """Raised when an operation times out"""
    pass


def with_timeout(timeout_seconds: float = 30.0):
    """
    Decorator to add timeout protection to async functions

    Usage:
        @with_timeout(timeout_seconds=10.0)
        async def my_async_function():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=timeout_seconds
                )
            except asyncio.TimeoutError:
                logger.error(f"⏱️ Timeout after {timeout_seconds}s in {func.__name__}")
                raise TimeoutError(f"{func.__name__} timed out after {timeout_seconds}s")
        return wrapper
    return decorator


async def run_with_timeout(coro, timeout_seconds: float = 30.0):
    """
    Run a coroutine with timeout protection

    Usage:
        result = await run_with_timeout(my_coroutine(), timeout_seconds=10.0)
    """
    try:
        return await asyncio.wait_for(coro, timeout=timeout_seconds)
    except asyncio.TimeoutError:
        logger.error(f"⏱️ Timeout after {timeout_seconds}s")
        raise TimeoutError(f"Operation timed out after {timeout_seconds}s")
