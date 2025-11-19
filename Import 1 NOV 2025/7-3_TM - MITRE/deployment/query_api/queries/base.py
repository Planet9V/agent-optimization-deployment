"""
Base Query Executor
File: queries/base.py
Created: 2025-11-08
Purpose: Base class for all query executors with caching and error handling
"""

from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from config.database import Neo4jConnection
from config.cache import CacheManager
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class QueryExecutor(ABC):
    """Base class for query executors with common functionality"""

    def __init__(self, db: Neo4jConnection, cache: CacheManager):
        self.db = db
        self.cache = cache

    @abstractmethod
    def get_query_simple(self) -> str:
        """Return simple query pattern"""
        pass

    @abstractmethod
    def get_query_intermediate(self) -> str:
        """Return intermediate query pattern"""
        pass

    @abstractmethod
    def get_query_advanced(self) -> str:
        """Return advanced query pattern"""
        pass

    async def execute(
        self,
        complexity: str = "simple",
        parameters: Dict[str, Any] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Execute query with specified complexity level

        Args:
            complexity: Query complexity (simple, intermediate, advanced)
            parameters: Query parameters
            use_cache: Whether to use caching

        Returns:
            Query results with metadata
        """
        # Validate complexity
        if complexity not in ["simple", "intermediate", "advanced"]:
            raise ValueError(f"Invalid complexity: {complexity}. Must be simple, intermediate, or advanced")

        # Get appropriate query
        query_method = getattr(self, f"get_query_{complexity}")
        query = query_method()

        # Prepare parameters with defaults
        params = self._prepare_parameters(parameters or {})

        # Try cache first
        if use_cache:
            cached_result = await self.cache.get(query, params)
            if cached_result:
                return {
                    "cached": True,
                    "complexity": complexity,
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": cached_result
                }

        # Execute query
        start_time = datetime.utcnow()

        try:
            results = await self.db.execute_read(query, params)

            execution_time = (datetime.utcnow() - start_time).total_seconds()

            response = {
                "cached": False,
                "complexity": complexity,
                "timestamp": datetime.utcnow().isoformat(),
                "execution_time_seconds": execution_time,
                "record_count": len(results),
                "data": results
            }

            # Cache results
            if use_cache and results:
                await self.cache.set(query, params, results)

            logger.info(
                f"Query executed: {self.__class__.__name__}, "
                f"complexity={complexity}, "
                f"records={len(results)}, "
                f"time={execution_time:.3f}s"
            )

            return response

        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise

    def _prepare_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare and validate query parameters"""
        # Override in subclasses for parameter validation
        return params

    def _paginate_results(
        self,
        results: List[Any],
        page: int = 1,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """Paginate query results"""
        total = len(results)
        start = (page - 1) * page_size
        end = start + page_size

        return {
            "data": results[start:end],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_records": total,
                "total_pages": (total + page_size - 1) // page_size
            }
        }


class QueryParameter:
    """Query parameter definition with validation"""

    def __init__(
        self,
        name: str,
        param_type: type,
        required: bool = False,
        default: Any = None,
        description: str = ""
    ):
        self.name = name
        self.param_type = param_type
        self.required = required
        self.default = default
        self.description = description

    def validate(self, value: Any) -> Any:
        """Validate and convert parameter value"""
        if value is None:
            if self.required:
                raise ValueError(f"Required parameter missing: {self.name}")
            return self.default

        # Type conversion
        try:
            if self.param_type == bool and isinstance(value, str):
                return value.lower() in ('true', '1', 'yes')
            return self.param_type(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid type for {self.name}: expected {self.param_type.__name__}, got {type(value).__name__}")
