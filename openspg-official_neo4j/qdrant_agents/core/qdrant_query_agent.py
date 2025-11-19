#!/usr/bin/env python3
"""
Qdrant Query Agent - Semantic Search Specialist
Optimized for fast, relevant documentation and knowledge retrieval
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import structlog

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.embedding_generator import EmbeddingGenerator
from utils.query_optimizer import QueryOptimizer
from utils.collection_manager import CollectionManager

logger = structlog.get_logger()

class QdrantQueryAgent:
    """
    Specialized agent for semantic search and knowledge retrieval

    Capabilities:
    - Semantic search across documentation
    - Multi-collection queries
    - Context expansion
    - Wave-specific filtering
    - Query pattern learning
    """

    def __init__(
        self,
        url: str = "http://localhost:6333",
        api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None
    ):
        """Initialize query agent"""
        self.url = url
        self.api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

        # Initialize components
        self.qdrant = QdrantClient(url=self.url, api_key=self.api_key)
        self.embedder = EmbeddingGenerator(
            api_key=self.openai_api_key,
            model="text-embedding-3-large",
            dimensions=3072
        )
        self.optimizer = QueryOptimizer(
            cache_ttl=3600,  # 1 hour cache
            enable_profiling=True
        )
        self.collection_mgr = CollectionManager(url=self.url, api_key=self.api_key)

        logger.info("qdrant_query_agent_initialized")

    def search_schema_knowledge(
        self,
        query: str,
        top_k: int = 5,
        file_filter: Optional[str] = None,
        wave_filter: Optional[int] = None,
        score_threshold: float = 0.5,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search schema knowledge collection

        Args:
            query: Natural language search query
            top_k: Number of results to return
            file_filter: Filter by source file (e.g., "SAREF")
            wave_filter: Filter by wave number for phased implementation
            score_threshold: Minimum similarity score
            use_cache: Use query cache for performance

        Returns:
            List of search results with metadata and scores
        """
        try:
            # Generate query embedding
            query_vector = self.embedder.create(query, use_cache=use_cache)

            # Build metadata filter
            filter_conditions = []
            if file_filter:
                filter_conditions.append(
                    FieldCondition(
                        key="source_file",
                        match=MatchValue(value=file_filter)
                    )
                )
            if wave_filter is not None:
                filter_conditions.append(
                    FieldCondition(
                        key="wave",
                        match=MatchValue(value=wave_filter)
                    )
                )

            query_filter = Filter(must=filter_conditions) if filter_conditions else None

            # Execute search with optimization
            query_params = {
                "collection_name": "schema_knowledge",
                "query_vector": query_vector,
                "query_filter": query_filter,
                "limit": top_k,
                "score_threshold": score_threshold,
                "with_payload": True
            }

            def execute_query(**params):
                return self.qdrant.search(**params)

            results, profiling = self.optimizer.profile_query(
                execute_query,
                query_params,
                use_cache=use_cache
            )

            # Format results
            formatted = []
            for result in results:
                formatted.append({
                    "score": result.score,
                    "content": result.payload.get("content", ""),
                    "source_file": result.payload.get("source_file", ""),
                    "chunk_id": result.payload.get("chunk_id", ""),
                    "metadata": result.payload.get("metadata", {})
                })

            logger.info(
                "schema_search_completed",
                query=query[:50],
                results=len(formatted),
                duration_ms=profiling.get("duration_ms", 0),
                cached=profiling.get("cached", False)
            )

            return formatted

        except Exception as e:
            logger.error("schema_search_failed", query=query, error=str(e))
            raise

    def search_query_patterns(
        self,
        query: str,
        top_k: int = 3,
        score_threshold: float = 0.6
    ) -> List[Dict[str, Any]]:
        """
        Search for similar query patterns (learn from past queries)

        Args:
            query: Current query
            top_k: Number of pattern matches
            score_threshold: Minimum similarity

        Returns:
            Similar past queries with their successful results
        """
        try:
            query_vector = self.embedder.create(query)

            results = self.qdrant.search(
                collection_name="query_patterns",
                query_vector=query_vector,
                limit=top_k,
                score_threshold=score_threshold,
                with_payload=True
            )

            patterns = []
            for result in results:
                patterns.append({
                    "score": result.score,
                    "original_query": result.payload.get("query", ""),
                    "successful_results": result.payload.get("result_count", 0),
                    "optimal_threshold": result.payload.get("optimal_threshold", 0.5),
                    "collections_used": result.payload.get("collections", []),
                    "timestamp": result.payload.get("timestamp", "")
                })

            logger.debug("query_patterns_found", patterns=len(patterns))
            return patterns

        except Exception as e:
            logger.error("query_pattern_search_failed", error=str(e))
            return []

    def multi_collection_search(
        self,
        query: str,
        collections: List[str],
        top_k_per_collection: int = 3,
        score_threshold: float = 0.5
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search across multiple collections simultaneously

        Args:
            query: Search query
            collections: List of collection names
            top_k_per_collection: Results per collection
            score_threshold: Minimum score

        Returns:
            Dict mapping collection names to their results
        """
        try:
            query_vector = self.embedder.create(query)

            results_by_collection = {}

            for collection in collections:
                try:
                    results = self.qdrant.search(
                        collection_name=collection,
                        query_vector=query_vector,
                        limit=top_k_per_collection,
                        score_threshold=score_threshold,
                        with_payload=True
                    )

                    formatted = []
                    for result in results:
                        formatted.append({
                            "score": result.score,
                            "content": result.payload.get("content", ""),
                            "metadata": result.payload
                        })

                    results_by_collection[collection] = formatted

                except Exception as e:
                    logger.warning(
                        "collection_search_failed",
                        collection=collection,
                        error=str(e)
                    )
                    results_by_collection[collection] = []

            logger.info(
                "multi_collection_search_completed",
                collections=len(collections),
                total_results=sum(len(r) for r in results_by_collection.values())
            )

            return results_by_collection

        except Exception as e:
            logger.error("multi_collection_search_failed", error=str(e))
            raise

    def expand_context(
        self,
        initial_query: str,
        expansion_depth: int = 2,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Expand search context by following related content

        Args:
            initial_query: Starting query
            expansion_depth: How many levels to expand
            top_k: Results per level

        Returns:
            Expanded result set with provenance
        """
        try:
            all_results = []
            seen_chunks = set()
            current_queries = [initial_query]

            for depth in range(expansion_depth):
                next_queries = []

                for query in current_queries:
                    results = self.search_schema_knowledge(
                        query=query,
                        top_k=top_k,
                        score_threshold=0.5
                    )

                    for result in results:
                        chunk_id = result.get("chunk_id", "")
                        if chunk_id not in seen_chunks:
                            seen_chunks.add(chunk_id)
                            result["expansion_depth"] = depth
                            result["expansion_query"] = query
                            all_results.append(result)

                            # Use content as next query for expansion
                            content = result.get("content", "")
                            if content and len(content) > 100:
                                # Use first sentence as expansion query
                                next_query = content[:200]
                                next_queries.append(next_query)

                current_queries = next_queries[:top_k]  # Limit expansion

                if not current_queries:
                    break

            logger.info(
                "context_expansion_completed",
                depth=depth + 1,
                total_results=len(all_results)
            )

            return all_results

        except Exception as e:
            logger.error("context_expansion_failed", error=str(e))
            return []

    def get_wave_context(
        self,
        wave_number: int,
        context_type: str = "all"
    ) -> Dict[str, Any]:
        """
        Get all context for a specific wave

        Args:
            wave_number: Wave number (1-12)
            context_type: "schema", "decisions", "patterns", or "all"

        Returns:
            Wave-specific context aggregated from relevant collections
        """
        try:
            context = {
                "wave": wave_number,
                "schema_knowledge": [],
                "decisions": [],
                "patterns": []
            }

            # Get schema knowledge for wave
            if context_type in ["schema", "all"]:
                context["schema_knowledge"] = self.collection_mgr.get_points_by_filter(
                    collection_name="schema_knowledge",
                    filter_dict={"wave": wave_number},
                    limit=100
                )

            # Get implementation decisions for wave
            if context_type in ["decisions", "all"]:
                context["decisions"] = self.collection_mgr.get_points_by_filter(
                    collection_name="implementation_decisions",
                    filter_dict={"wave": wave_number},
                    limit=50
                )

            # Get relevant patterns
            if context_type in ["patterns", "all"]:
                # Patterns don't have wave numbers, so search semantically
                wave_query = f"Implementation patterns for wave {wave_number}"
                pattern_results = self.qdrant.search(
                    collection_name="query_patterns",
                    query_vector=self.embedder.create(wave_query),
                    limit=10,
                    score_threshold=0.5,
                    with_payload=True
                )
                context["patterns"] = [r.payload for r in pattern_results]

            logger.info(
                "wave_context_retrieved",
                wave=wave_number,
                schema_items=len(context["schema_knowledge"]),
                decisions=len(context["decisions"]),
                patterns=len(context["patterns"])
            )

            return context

        except Exception as e:
            logger.error("wave_context_failed", wave=wave_number, error=str(e))
            return {"wave": wave_number, "error": str(e)}

    def find_similar_implementations(
        self,
        description: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find similar past implementations

        Args:
            description: Description of what you want to implement
            top_k: Number of similar implementations

        Returns:
            Similar implementations with their decisions
        """
        try:
            results = self.multi_collection_search(
                query=description,
                collections=["implementation_decisions", "agent_shared_memory"],
                top_k_per_collection=top_k,
                score_threshold=0.55
            )

            # Combine and sort by score
            combined = []
            for collection, items in results.items():
                for item in items:
                    item["source_collection"] = collection
                    combined.append(item)

            combined.sort(key=lambda x: x["score"], reverse=True)

            logger.info(
                "similar_implementations_found",
                description=description[:50],
                results=len(combined)
            )

            return combined[:top_k]

        except Exception as e:
            logger.error("similar_implementations_failed", error=str(e))
            return []

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get query performance statistics"""
        return self.optimizer.get_performance_stats()

    def clear_query_cache(self, older_than_hours: Optional[int] = None):
        """Clear query cache"""
        self.optimizer.clear_cache(older_than_hours=older_than_hours)
        logger.info("query_cache_cleared")


# CLI Interface for Testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Qdrant Query Agent")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--collection", default="schema_knowledge",
                       help="Collection to search")
    parser.add_argument("--top-k", type=int, default=5,
                       help="Number of results")
    parser.add_argument("--file-filter", help="Filter by source file")
    parser.add_argument("--wave", type=int, help="Filter by wave number")

    args = parser.parse_args()

    agent = QdrantQueryAgent()

    if args.collection == "schema_knowledge":
        results = agent.search_schema_knowledge(
            query=args.query,
            top_k=args.top_k,
            file_filter=args.file_filter,
            wave_filter=args.wave
        )
    else:
        query_vector = agent.embedder.create(args.query)
        results = agent.qdrant.search(
            collection_name=args.collection,
            query_vector=query_vector,
            limit=args.top_k,
            with_payload=True
        )

    print(f"\n🔍 Query: {args.query}")
    print(f"📚 Collection: {args.collection}")
    print(f"📊 Results: {len(results)}\n")

    for i, result in enumerate(results, 1):
        if isinstance(result, dict):
            print(f"{i}. Score: {result['score']:.3f}")
            print(f"   Content: {result['content'][:200]}...")
            print(f"   Source: {result.get('source_file', 'Unknown')}\n")
        else:
            print(f"{i}. Score: {result.score:.3f}")
            print(f"   Content: {result.payload.get('content', '')[:200]}...")
            print(f"   Source: {result.payload.get('source_file', 'Unknown')}\n")
