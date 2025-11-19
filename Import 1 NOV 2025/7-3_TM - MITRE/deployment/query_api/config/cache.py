"""
Redis Cache Management
File: config/cache.py
Created: 2025-11-08
Purpose: Query result caching with Redis
"""

from typing import Optional, Any
import json
import hashlib
import redis.asyncio as redis
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """Redis cache manager for query results"""

    def __init__(self):
        self._redis: Optional[redis.Redis] = None
        self._enabled = True

    async def initialize(self):
        """Initialize Redis connection"""
        try:
            self._redis = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password,
                decode_responses=True,
                socket_timeout=5.0,
                socket_connect_timeout=5.0
            )

            # Test connection
            await self._redis.ping()
            logger.info(f"Redis cache initialized: {settings.redis_host}:{settings.redis_port}")

        except Exception as e:
            logger.warning(f"Redis cache unavailable, caching disabled: {e}")
            self._enabled = False

    async def close(self):
        """Close Redis connection"""
        if self._redis:
            await self._redis.close()
            logger.info("Redis cache closed")

    def _generate_cache_key(self, query: str, parameters: dict) -> str:
        """Generate cache key from query and parameters"""
        # Create deterministic hash of query and parameters
        data = json.dumps({"query": query, "params": parameters}, sort_keys=True)
        return f"aeon:query:{hashlib.sha256(data.encode()).hexdigest()}"

    async def get(self, query: str, parameters: dict) -> Optional[Any]:
        """Get cached query result"""
        if not self._enabled or not self._redis:
            return None

        try:
            cache_key = self._generate_cache_key(query, parameters)
            cached_data = await self._redis.get(cache_key)

            if cached_data:
                logger.debug(f"Cache hit: {cache_key}")
                return json.loads(cached_data)

            logger.debug(f"Cache miss: {cache_key}")
            return None

        except Exception as e:
            logger.warning(f"Cache get error: {e}")
            return None

    async def set(self, query: str, parameters: dict, data: Any, ttl: Optional[int] = None):
        """Cache query result"""
        if not self._enabled or not self._redis:
            return

        try:
            cache_key = self._generate_cache_key(query, parameters)
            cache_ttl = ttl or settings.cache_ttl

            await self._redis.setex(
                cache_key,
                cache_ttl,
                json.dumps(data, default=str)
            )

            logger.debug(f"Cached: {cache_key} (TTL: {cache_ttl}s)")

        except Exception as e:
            logger.warning(f"Cache set error: {e}")

    async def invalidate_pattern(self, pattern: str):
        """Invalidate cache entries matching pattern"""
        if not self._enabled or not self._redis:
            return

        try:
            keys = []
            async for key in self._redis.scan_iter(match=f"aeon:query:{pattern}*"):
                keys.append(key)

            if keys:
                await self._redis.delete(*keys)
                logger.info(f"Invalidated {len(keys)} cache entries matching: {pattern}")

        except Exception as e:
            logger.warning(f"Cache invalidation error: {e}")


# Global cache instance
cache_manager = CacheManager()


async def get_cache() -> CacheManager:
    """Dependency injection for cache manager"""
    return cache_manager
