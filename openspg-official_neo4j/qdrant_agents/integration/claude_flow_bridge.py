#!/usr/bin/env python3
"""
Claude-Flow Bridge - Integration Layer for Qdrant Agents
Enables seamless calling of Qdrant agents from Claude-Flow ecosystem
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import structlog

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from core.qdrant_query_agent import QdrantQueryAgent
from core.qdrant_memory_agent import QdrantMemoryAgent
from core.qdrant_pattern_agent import QdrantPatternAgent
from core.qdrant_decision_agent import QdrantDecisionAgent
from core.qdrant_sync_agent import QdrantSyncAgent
from core.qdrant_analytics_agent import QdrantAnalyticsAgent

logger = structlog.get_logger()

class ClaudeFlowBridge:
    """
    Integration bridge between Qdrant agents and Claude-Flow

    Provides unified interface for Claude-Flow to call Qdrant agents
    """

    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        qdrant_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None
    ):
        """Initialize bridge with all Qdrant agents"""
        self.qdrant_url = qdrant_url
        self.qdrant_api_key = qdrant_api_key or os.getenv("QDRANT_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

        # Initialize all agents
        self.query_agent = QdrantQueryAgent(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            openai_api_key=self.openai_api_key
        )

        self.memory_agent = QdrantMemoryAgent(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            openai_api_key=self.openai_api_key
        )

        self.pattern_agent = QdrantPatternAgent(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            openai_api_key=self.openai_api_key
        )

        self.decision_agent = QdrantDecisionAgent(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            openai_api_key=self.openai_api_key
        )

        self.sync_agent = QdrantSyncAgent(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key
        )

        self.analytics_agent = QdrantAnalyticsAgent(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            openai_api_key=self.openai_api_key
        )

        logger.info("claude_flow_bridge_initialized")

    # ========== Query Agent Methods ==========

    def search_knowledge(
        self,
        query: str,
        collection: str = "schema_knowledge",
        top_k: int = 5,
        wave: Optional[int] = None,
        file_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search knowledge base (exposed to Claude-Flow)

        Args:
            query: Search query
            collection: Collection to search
            top_k: Number of results
            wave: Optional wave filter
            file_filter: Optional file filter

        Returns:
            Search results with metadata
        """
        try:
            results = self.query_agent.search_schema_knowledge(
                query=query,
                top_k=top_k,
                wave_filter=wave,
                file_filter=file_filter
            )

            return {
                "success": True,
                "query": query,
                "collection": collection,
                "results": results,
                "count": len(results)
            }

        except Exception as e:
            logger.error("knowledge_search_failed", error=str(e))
            return {"success": False, "error": str(e)}

    def find_similar_implementations(
        self,
        description: str,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Find similar past implementations (exposed to Claude-Flow)

        Args:
            description: What you're trying to implement
            top_k: Number of similar implementations

        Returns:
            Similar implementations with decisions
        """
        try:
            results = self.query_agent.find_similar_implementations(
                description=description,
                top_k=top_k
            )

            return {
                "success": True,
                "description": description,
                "similar_implementations": results,
                "count": len(results)
            }

        except Exception as e:
            logger.error("similar_implementations_search_failed", error=str(e))
            return {"success": False, "error": str(e)}

    def get_wave_context(
        self,
        wave_number: int
    ) -> Dict[str, Any]:
        """
        Get all context for a wave (exposed to Claude-Flow)

        Args:
            wave_number: Wave number (1-12)

        Returns:
            Wave-specific knowledge, decisions, and patterns
        """
        try:
            context = self.query_agent.get_wave_context(wave_number=wave_number)

            return {
                "success": True,
                "wave": wave_number,
                "context": context
            }

        except Exception as e:
            logger.error("wave_context_failed", error=str(e))
            return {"success": False, "error": str(e)}

    # ========== Memory Agent Methods ==========

    def store_finding(
        self,
        finding: str,
        agent_name: str,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        wave: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Store agent finding (exposed to Claude-Flow)

        Args:
            finding: Discovery or lesson learned
            agent_name: Name of agent
            context: Additional context
            tags: Categorization tags
            wave: Wave number

        Returns:
            Finding ID and status
        """
        try:
            finding_id = self.memory_agent.store_finding(
                finding=finding,
                agent_name=agent_name,
                context=context or {},
                tags=tags,
                wave=wave
            )

            return {
                "success": True,
                "finding_id": finding_id,
                "agent": agent_name,
                "wave": wave
            }

        except Exception as e:
            logger.error("finding_storage_failed", error=str(e))
            return {"success": False, "error": str(e)}

    def retrieve_experiences(
        self,
        query: str,
        agent_filter: Optional[str] = None,
        wave_filter: Optional[int] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Retrieve relevant past experiences (exposed to Claude-Flow)

        Args:
            query: What to search for
            agent_filter: Filter by agent
            wave_filter: Filter by wave
            top_k: Number of experiences

        Returns:
            Relevant experiences
        """
        try:
            experiences = self.memory_agent.retrieve_experiences(
                query=query,
                agent_filter=agent_filter,
                wave_filter=wave_filter,
                top_k=top_k
            )

            return {
                "success": True,
                "query": query,
                "experiences": experiences,
                "count": len(experiences)
            }

        except Exception as e:
            logger.error("experience_retrieval_failed", error=str(e))
            return {"success": False, "error": str(e)}

    # ========== Pattern Agent Methods ==========

    def discover_patterns(
        self,
        algorithm: str = "kmeans",
        n_clusters: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Discover implementation patterns (exposed to Claude-Flow)

        Args:
            algorithm: "kmeans" or "dbscan"
            n_clusters: Number of clusters (auto if None)

        Returns:
            Discovered patterns
        """
        try:
            patterns = self.pattern_agent.extract_patterns(
                source_collection="agent_shared_memory",
                clustering_algorithm=algorithm,
                n_clusters=n_clusters
            )

            # Store patterns
            for pattern in patterns:
                self.pattern_agent.store_pattern(pattern)

            return {
                "success": True,
                "algorithm": algorithm,
                "patterns": patterns,
                "count": len(patterns)
            }

        except Exception as e:
            logger.error("pattern_discovery_failed", error=str(e))
            return {"success": False, "error": str(e)}

    def find_patterns(
        self,
        query: str,
        top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Find similar patterns (exposed to Claude-Flow)

        Args:
            query: Pattern description
            top_k: Number of patterns

        Returns:
            Matching patterns
        """
        try:
            patterns = self.pattern_agent.find_similar_patterns(
                query=query,
                top_k=top_k
            )

            return {
                "success": True,
                "query": query,
                "patterns": patterns,
                "count": len(patterns)
            }

        except Exception as e:
            logger.error("pattern_search_failed", error=str(e))
            return {"success": False, "error": str(e)}

    # ========== Decision Agent Methods ==========

    def record_decision(
        self,
        decision: str,
        rationale: str,
        alternatives: Optional[List[str]] = None,
        decision_type: str = "implementation",
        wave: Optional[int] = None,
        made_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Record implementation decision (exposed to Claude-Flow)

        Args:
            decision: Decision made
            rationale: Why this decision
            alternatives: Alternatives considered
            decision_type: Type of decision
            wave: Wave number
            made_by: Agent or person

        Returns:
            Decision ID and status
        """
        try:
            decision_id = self.decision_agent.record_decision(
                decision=decision,
                rationale=rationale,
                alternatives=alternatives,
                decision_type=decision_type,
                wave=wave,
                made_by=made_by
            )

            return {
                "success": True,
                "decision_id": decision_id,
                "decision_type": decision_type,
                "wave": wave
            }

        except Exception as e:
            logger.error("decision_recording_failed", error=str(e))
            return {"success": False, "error": str(e)}

    def find_related_decisions(
        self,
        query: str,
        decision_type: Optional[str] = None,
        wave: Optional[int] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Find related decisions (exposed to Claude-Flow)

        Args:
            query: Search query
            decision_type: Filter by type
            wave: Filter by wave
            top_k: Number of decisions

        Returns:
            Related decisions
        """
        try:
            decisions = self.decision_agent.find_related_decisions(
                query=query,
                decision_type=decision_type,
                wave_filter=wave,
                top_k=top_k
            )

            return {
                "success": True,
                "query": query,
                "decisions": decisions,
                "count": len(decisions)
            }

        except Exception as e:
            logger.error("decision_search_failed", error=str(e))
            return {"success": False, "error": str(e)}

    # ========== Sync Agent Methods ==========

    def sync_memories(
        self,
        direction: str = "bidirectional"
    ) -> Dict[str, Any]:
        """
        Sync memories between Qdrant and local (exposed to Claude-Flow)

        Args:
            direction: "bidirectional", "qdrant_to_local", or "local_to_qdrant"

        Returns:
            Sync statistics
        """
        try:
            results = self.sync_agent.sync_all_collections(direction=direction)

            total_synced = sum(
                r.get("qdrant_to_local", 0) + r.get("local_to_qdrant", 0)
                for r in results
            )

            return {
                "success": True,
                "direction": direction,
                "total_synced": total_synced,
                "collections": results
            }

        except Exception as e:
            logger.error("memory_sync_failed", error=str(e))
            return {"success": False, "error": str(e)}

    # ========== Analytics Agent Methods ==========

    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Get current system metrics (exposed to Claude-Flow)

        Returns:
            Comprehensive metrics
        """
        try:
            metrics = self.analytics_agent.collect_system_metrics()

            return {
                "success": True,
                "metrics": metrics
            }

        except Exception as e:
            logger.error("metrics_collection_failed", error=str(e))
            return {"success": False, "error": str(e)}

    def get_recommendations(self) -> Dict[str, Any]:
        """
        Get optimization recommendations (exposed to Claude-Flow)

        Returns:
            Prioritized recommendations
        """
        try:
            recommendations = self.analytics_agent.generate_optimization_recommendations()

            return {
                "success": True,
                "recommendations": recommendations,
                "count": len(recommendations)
            }

        except Exception as e:
            logger.error("recommendation_generation_failed", error=str(e))
            return {"success": False, "error": str(e)}

    # ========== Unified Query Interface ==========

    def query(
        self,
        operation: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Unified query interface for Claude-Flow

        Args:
            operation: Operation name
            **kwargs: Operation parameters

        Returns:
            Operation result

        Supported Operations:
            - search_knowledge
            - find_implementations
            - get_wave_context
            - store_finding
            - retrieve_experiences
            - discover_patterns
            - find_patterns
            - record_decision
            - find_decisions
            - sync_memories
            - get_metrics
            - get_recommendations
        """
        operations = {
            "search_knowledge": self.search_knowledge,
            "find_implementations": self.find_similar_implementations,
            "get_wave_context": self.get_wave_context,
            "store_finding": self.store_finding,
            "retrieve_experiences": self.retrieve_experiences,
            "discover_patterns": self.discover_patterns,
            "find_patterns": self.find_patterns,
            "record_decision": self.record_decision,
            "find_decisions": self.find_related_decisions,
            "sync_memories": self.sync_memories,
            "get_metrics": self.get_system_metrics,
            "get_recommendations": self.get_recommendations
        }

        if operation not in operations:
            return {
                "success": False,
                "error": f"Unknown operation: {operation}",
                "available_operations": list(operations.keys())
            }

        try:
            return operations[operation](**kwargs)

        except Exception as e:
            logger.error("unified_query_failed", operation=operation, error=str(e))
            return {"success": False, "error": str(e)}


# Singleton instance for easy import
_bridge_instance = None

def get_bridge() -> ClaudeFlowBridge:
    """Get singleton bridge instance"""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = ClaudeFlowBridge()
    return _bridge_instance


# CLI Interface
if __name__ == "__main__":
    import argparse
    import json as jsonlib

    parser = argparse.ArgumentParser(description="Claude-Flow Bridge")
    parser.add_argument("operation", help="Operation to perform")
    parser.add_argument("--params", help="JSON parameters")

    args = parser.parse_args()

    bridge = get_bridge()

    # Parse parameters
    params = jsonlib.loads(args.params) if args.params else {}

    # Execute operation
    result = bridge.query(args.operation, **params)

    # Print result
    print(jsonlib.dumps(result, indent=2))
