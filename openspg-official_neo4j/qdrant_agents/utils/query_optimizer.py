#!/usr/bin/env python3
"""
Query Optimizer - Performance optimization for Qdrant queries
Implements caching, query rewriting, and performance profiling
"""

import time
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
from datetime import datetime, timedelta
import structlog

logger = structlog.get_logger()

class QueryOptimizer:
    """
    Optimizes Qdrant queries through caching and query analysis
    """

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        cache_ttl: int = 3600,
        enable_profiling: bool = True
    ):
        """
        Initialize query optimizer

        Args:
            cache_dir: Directory for query cache
            cache_ttl: Cache time-to-live in seconds (default 1 hour)
            enable_profiling: Enable performance profiling
        """
        self.cache_dir = cache_dir or Path("/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/qdrant_backup/query_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_ttl = cache_ttl
        self.enable_profiling = enable_profiling

        # Performance tracking
        self.query_stats = defaultdict(list)
        self.cache_hits = 0
        self.cache_misses = 0

        logger.info(
            "query_optimizer_initialized",
            cache_dir=str(self.cache_dir),
            cache_ttl=self.cache_ttl
        )

    def _cache_key(self, query_params: Dict[str, Any]) -> str:
        """Generate cache key from query parameters"""
        # Create deterministic hash from query params
        query_json = json.dumps(query_params, sort_keys=True)
        return hashlib.sha256(query_json.encode()).hexdigest()

    def _get_cached_results(
        self,
        query_params: Dict[str, Any]
    ) -> Optional[List[Dict[str, Any]]]:
        """Retrieve cached query results if valid"""
        cache_key = self._cache_key(query_params)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if not cache_file.exists():
            self.cache_misses += 1
            return None

        try:
            with open(cache_file, 'r') as f:
                cached = json.load(f)

            # Check TTL
            cached_time = datetime.fromisoformat(cached["timestamp"])
            age = (datetime.now() - cached_time).total_seconds()

            if age > self.cache_ttl:
                # Expired - delete and return None
                cache_file.unlink()
                self.cache_misses += 1
                return None

            self.cache_hits += 1
            logger.debug(
                "query_cache_hit",
                age_seconds=age,
                results_count=len(cached["results"])
            )
            return cached["results"]

        except Exception as e:
            logger.warning("query_cache_read_failed", error=str(e))
            self.cache_misses += 1
            return None

    def _set_cached_results(
        self,
        query_params: Dict[str, Any],
        results: List[Dict[str, Any]]
    ):
        """Store query results in cache"""
        cache_key = self._cache_key(query_params)
        cache_file = self.cache_dir / f"{cache_key}.json"

        try:
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "query_params": query_params,
                "results": results
            }

            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)

            logger.debug("query_cached", results_count=len(results))

        except Exception as e:
            logger.warning("query_cache_write_failed", error=str(e))

    def optimize_query(
        self,
        query: str,
        collection: str,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Optimize query parameters for best performance

        Args:
            query: Search query text
            collection: Target collection
            top_k: Number of results

        Returns:
            Optimized query parameters
        """
        optimized = {
            "query": query,
            "collection": collection,
            "top_k": top_k,
            "score_threshold": self._suggest_threshold(collection),
            "search_params": self._suggest_search_params(top_k)
        }

        logger.debug("query_optimized", params=optimized)
        return optimized

    def _suggest_threshold(self, collection: str) -> float:
        """
        Suggest optimal score threshold based on collection

        Different collections may need different thresholds
        based on their vector distributions
        """
        # Collection-specific thresholds learned from usage
        thresholds = {
            "schema_knowledge": 0.5,  # Broad semantic search
            "query_patterns": 0.6,    # More specific patterns
            "agent_shared_memory": 0.55,  # Agent experiences
            "implementation_decisions": 0.65  # Precise decisions
        }

        return thresholds.get(collection, 0.5)

    def _suggest_search_params(self, top_k: int) -> Dict[str, int]:
        """
        Suggest HNSW search parameters based on top_k

        Balances speed vs accuracy
        """
        # ef (exploration factor) should be >= top_k
        # Higher ef = better accuracy but slower
        if top_k <= 5:
            ef = 32  # Fast for small top_k
        elif top_k <= 20:
            ef = 64  # Balanced
        else:
            ef = 128  # Accuracy priority for large top_k

        return {
            "hnsw_ef": ef,
            "exact": False  # Use approximate search
        }

    def profile_query(
        self,
        query_func,
        query_params: Dict[str, Any],
        use_cache: bool = True
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Execute query with profiling

        Args:
            query_func: Function to execute query
            query_params: Query parameters
            use_cache: Whether to use cache

        Returns:
            (results, profiling_stats)
        """
        # Check cache first
        if use_cache:
            cached = self._get_cached_results(query_params)
            if cached is not None:
                return cached, {
                    "cached": True,
                    "duration_ms": 0,
                    "cache_hit_rate": self.get_cache_hit_rate()
                }

        # Execute with timing
        start_time = time.time()
        results = query_func(**query_params)
        duration = (time.time() - start_time) * 1000  # Convert to ms

        # Cache results
        if use_cache:
            self._set_cached_results(query_params, results)

        # Record stats
        if self.enable_profiling:
            self.query_stats[query_params["collection"]].append({
                "duration_ms": duration,
                "results_count": len(results),
                "timestamp": datetime.now().isoformat()
            })

        profiling_stats = {
            "cached": False,
            "duration_ms": duration,
            "results_count": len(results),
            "cache_hit_rate": self.get_cache_hit_rate()
        }

        logger.info(
            "query_profiled",
            collection=query_params.get("collection"),
            duration_ms=round(duration, 2),
            results=len(results)
        )

        return results, profiling_stats

    def get_cache_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total

    def get_performance_stats(
        self,
        collection: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get performance statistics

        Args:
            collection: Optional collection filter

        Returns:
            Performance metrics
        """
        if collection and collection in self.query_stats:
            stats = self.query_stats[collection]
        else:
            # Aggregate all collections
            stats = []
            for coll_stats in self.query_stats.values():
                stats.extend(coll_stats)

        if not stats:
            return {
                "total_queries": 0,
                "avg_duration_ms": 0,
                "cache_hit_rate": self.get_cache_hit_rate()
            }

        durations = [s["duration_ms"] for s in stats]
        result_counts = [s["results_count"] for s in stats]

        return {
            "total_queries": len(stats),
            "avg_duration_ms": sum(durations) / len(durations),
            "min_duration_ms": min(durations),
            "max_duration_ms": max(durations),
            "avg_results": sum(result_counts) / len(result_counts),
            "cache_hit_rate": self.get_cache_hit_rate(),
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses
        }

    def clear_cache(self, older_than_hours: Optional[int] = None):
        """
        Clear query cache

        Args:
            older_than_hours: Only clear entries older than X hours
        """
        try:
            if older_than_hours is None:
                # Clear all
                for cache_file in self.cache_dir.glob("*.json"):
                    cache_file.unlink()
                logger.info("query_cache_cleared", type="all")
            else:
                # Clear old entries
                cutoff = datetime.now() - timedelta(hours=older_than_hours)
                cleared = 0

                for cache_file in self.cache_dir.glob("*.json"):
                    try:
                        with open(cache_file, 'r') as f:
                            cached = json.load(f)
                        cached_time = datetime.fromisoformat(cached["timestamp"])

                        if cached_time < cutoff:
                            cache_file.unlink()
                            cleared += 1

                    except Exception as e:
                        logger.warning("cache_file_check_failed", file=str(cache_file), error=str(e))

                logger.info(
                    "query_cache_cleared",
                    type="selective",
                    older_than_hours=older_than_hours,
                    cleared=cleared
                )

        except Exception as e:
            logger.error("cache_clear_failed", error=str(e))

    def analyze_query_patterns(self) -> Dict[str, Any]:
        """
        Analyze query patterns across all collections

        Returns:
            Pattern analysis with recommendations
        """
        analysis = {
            "collections": {},
            "overall": self.get_performance_stats(),
            "recommendations": []
        }

        # Per-collection analysis
        for collection, stats in self.query_stats.items():
            coll_analysis = self.get_performance_stats(collection)
            analysis["collections"][collection] = coll_analysis

            # Generate recommendations
            if coll_analysis["avg_duration_ms"] > 1000:
                analysis["recommendations"].append({
                    "collection": collection,
                    "issue": "Slow queries",
                    "suggestion": "Consider reducing top_k or increasing score_threshold"
                })

        # Cache recommendations
        hit_rate = self.get_cache_hit_rate()
        if hit_rate < 0.3:
            analysis["recommendations"].append({
                "issue": "Low cache hit rate",
                "current_rate": hit_rate,
                "suggestion": "Increase cache TTL or review query patterns for more reuse"
            })

        return analysis
