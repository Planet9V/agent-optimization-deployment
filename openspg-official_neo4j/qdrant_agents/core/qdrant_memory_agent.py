#!/usr/bin/env python3
"""
Qdrant Memory Agent - Shared Memory Coordinator
Enables cross-agent learning and finding storage
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
import uuid
import json
import structlog

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.embedding_generator import EmbeddingGenerator
from utils.collection_manager import CollectionManager

logger = structlog.get_logger()

class QdrantMemoryAgent:
    """
    Specialized agent for cross-agent memory coordination

    Capabilities:
    - Store agent findings for cross-agent learning
    - Retrieve relevant past experiences
    - Resolve conflicts in agent memories
    - Track agent collaboration patterns
    - Maintain dual memory (Qdrant + local backup)
    """

    def __init__(
        self,
        url: str = "http://localhost:6333",
        api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        local_backup_path: Optional[Path] = None
    ):
        """Initialize memory agent"""
        self.url = url
        self.api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

        self.local_backup_path = local_backup_path or Path(
            "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/qdrant_backup/agent_memories"
        )
        self.local_backup_path.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.qdrant = QdrantClient(url=self.url, api_key=self.api_key)
        self.embedder = EmbeddingGenerator(
            api_key=self.openai_api_key,
            model="text-embedding-3-large",
            dimensions=3072
        )
        self.collection_mgr = CollectionManager(url=self.url, api_key=self.api_key)

        logger.info("qdrant_memory_agent_initialized")

    def store_finding(
        self,
        finding: str,
        agent_name: str,
        context: Dict[str, Any],
        tags: Optional[List[str]] = None,
        wave: Optional[int] = None
    ) -> str:
        """
        Store agent finding in shared memory

        Args:
            finding: The discovery or lesson learned
            agent_name: Name of agent storing the finding
            context: Additional context (file, task, etc.)
            tags: Optional categorization tags
            wave: Optional wave number for phased implementation

        Returns:
            Finding ID
        """
        try:
            # Generate unique ID
            finding_id = str(uuid.uuid4())

            # Generate embedding
            embedding = self.embedder.create(finding)

            # Prepare payload
            payload = {
                "finding": finding,
                "agent_name": agent_name,
                "context": context,
                "tags": tags or [],
                "wave": wave,
                "timestamp": datetime.now().isoformat(),
                "finding_id": finding_id
            }

            # Store in Qdrant
            point = PointStruct(
                id=finding_id,
                vector=embedding,
                payload=payload
            )

            self.qdrant.upsert(
                collection_name="agent_shared_memory",
                points=[point],
                wait=True
            )

            # Backup locally
            self._backup_locally(finding_id, payload, embedding)

            logger.info(
                "finding_stored",
                finding_id=finding_id,
                agent=agent_name,
                wave=wave
            )

            return finding_id

        except Exception as e:
            logger.error("finding_storage_failed", agent=agent_name, error=str(e))
            raise

    def _backup_locally(
        self,
        finding_id: str,
        payload: Dict[str, Any],
        embedding: List[float]
    ):
        """Backup finding to local filesystem"""
        try:
            backup_file = self.local_backup_path / f"{finding_id}.json"

            backup_data = {
                "payload": payload,
                "embedding": embedding,
                "backup_timestamp": datetime.now().isoformat()
            }

            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)

        except Exception as e:
            logger.warning("local_backup_failed", finding_id=finding_id, error=str(e))

    def retrieve_experiences(
        self,
        query: str,
        agent_filter: Optional[str] = None,
        wave_filter: Optional[int] = None,
        tag_filter: Optional[List[str]] = None,
        top_k: int = 5,
        score_threshold: float = 0.55
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant past experiences

        Args:
            query: What you're looking for
            agent_filter: Filter by specific agent
            wave_filter: Filter by wave number
            tag_filter: Filter by tags
            top_k: Number of experiences
            score_threshold: Minimum relevance

        Returns:
            Relevant past experiences
        """
        try:
            # Generate query embedding
            query_vector = self.embedder.create(query)

            # Build filter
            filter_conditions = []
            if agent_filter:
                filter_conditions.append(
                    FieldCondition(
                        key="agent_name",
                        match=MatchValue(value=agent_filter)
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

            # Search
            results = self.qdrant.search(
                collection_name="agent_shared_memory",
                query_vector=query_vector,
                query_filter=query_filter,
                limit=top_k,
                score_threshold=score_threshold,
                with_payload=True
            )

            # Format results
            experiences = []
            for result in results:
                experience = {
                    "score": result.score,
                    "finding": result.payload.get("finding", ""),
                    "agent_name": result.payload.get("agent_name", ""),
                    "context": result.payload.get("context", {}),
                    "tags": result.payload.get("tags", []),
                    "wave": result.payload.get("wave"),
                    "timestamp": result.payload.get("timestamp", ""),
                    "finding_id": result.payload.get("finding_id", "")
                }

                # Tag filtering (Qdrant doesn't support list matching natively)
                if tag_filter:
                    experience_tags = set(experience["tags"])
                    if not any(tag in experience_tags for tag in tag_filter):
                        continue

                experiences.append(experience)

            logger.info(
                "experiences_retrieved",
                query=query[:50],
                results=len(experiences)
            )

            return experiences

        except Exception as e:
            logger.error("experience_retrieval_failed", error=str(e))
            return []

    def get_agent_contributions(
        self,
        agent_name: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get all contributions from a specific agent

        Args:
            agent_name: Agent to query
            limit: Maximum contributions

        Returns:
            Agent's contributions
        """
        try:
            results = self.collection_mgr.get_points_by_filter(
                collection_name="agent_shared_memory",
                filter_dict={"agent_name": agent_name},
                limit=limit
            )

            contributions = []
            for point in results:
                contributions.append({
                    "finding": point.payload.get("finding", ""),
                    "context": point.payload.get("context", {}),
                    "tags": point.payload.get("tags", []),
                    "wave": point.payload.get("wave"),
                    "timestamp": point.payload.get("timestamp", ""),
                    "finding_id": point.id
                })

            logger.info(
                "agent_contributions_retrieved",
                agent=agent_name,
                count=len(contributions)
            )

            return contributions

        except Exception as e:
            logger.error("agent_contributions_failed", agent=agent_name, error=str(e))
            return []

    def detect_conflicts(
        self,
        recent_hours: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Detect conflicting findings from different agents

        Args:
            recent_hours: How far back to check

        Returns:
            Potential conflicts
        """
        try:
            # Get recent findings
            cutoff_time = datetime.now().timestamp() - (recent_hours * 3600)

            # Scroll through recent memories
            all_points, _ = self.qdrant.scroll(
                collection_name="agent_shared_memory",
                limit=1000,
                with_payload=True,
                with_vectors=True
            )

            # Filter by time
            recent_points = []
            for point in all_points:
                timestamp_str = point.payload.get("timestamp", "")
                if timestamp_str:
                    try:
                        point_time = datetime.fromisoformat(timestamp_str).timestamp()
                        if point_time >= cutoff_time:
                            recent_points.append(point)
                    except Exception:
                        pass

            # Detect conflicts by finding highly similar findings from different agents
            conflicts = []
            for i, point1 in enumerate(recent_points):
                for point2 in recent_points[i+1:]:
                    # Skip if same agent
                    if point1.payload.get("agent_name") == point2.payload.get("agent_name"):
                        continue

                    # Calculate similarity (simple dot product)
                    similarity = sum(a * b for a, b in zip(point1.vector, point2.vector))

                    # High similarity from different agents = potential conflict
                    if similarity > 0.9:
                        conflicts.append({
                            "similarity": similarity,
                            "finding_1": {
                                "agent": point1.payload.get("agent_name"),
                                "finding": point1.payload.get("finding", "")[:200],
                                "timestamp": point1.payload.get("timestamp", "")
                            },
                            "finding_2": {
                                "agent": point2.payload.get("agent_name"),
                                "finding": point2.payload.get("finding", "")[:200],
                                "timestamp": point2.payload.get("timestamp", "")
                            }
                        })

            logger.info(
                "conflict_detection_completed",
                recent_hours=recent_hours,
                conflicts_found=len(conflicts)
            )

            return conflicts

        except Exception as e:
            logger.error("conflict_detection_failed", error=str(e))
            return []

    def get_collaboration_patterns(self) -> Dict[str, Any]:
        """
        Analyze cross-agent collaboration patterns

        Returns:
            Collaboration statistics and patterns
        """
        try:
            # Get all agent memories
            all_points, _ = self.qdrant.scroll(
                collection_name="agent_shared_memory",
                limit=10000,
                with_payload=True
            )

            # Analyze patterns
            agent_activity = {}
            wave_activity = {}
            tag_frequency = {}

            for point in all_points:
                agent = point.payload.get("agent_name", "unknown")
                wave = point.payload.get("wave")
                tags = point.payload.get("tags", [])

                # Agent activity
                agent_activity[agent] = agent_activity.get(agent, 0) + 1

                # Wave activity
                if wave is not None:
                    wave_activity[wave] = wave_activity.get(wave, 0) + 1

                # Tag frequency
                for tag in tags:
                    tag_frequency[tag] = tag_frequency.get(tag, 0) + 1

            patterns = {
                "total_findings": len(all_points),
                "agent_activity": dict(sorted(
                    agent_activity.items(),
                    key=lambda x: x[1],
                    reverse=True
                )),
                "wave_activity": dict(sorted(wave_activity.items())),
                "tag_frequency": dict(sorted(
                    tag_frequency.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:20]),  # Top 20 tags
                "most_active_agent": max(agent_activity.items(), key=lambda x: x[1])[0] if agent_activity else None,
                "most_active_wave": max(wave_activity.items(), key=lambda x: x[1])[0] if wave_activity else None
            }

            logger.info(
                "collaboration_patterns_analyzed",
                total_findings=patterns["total_findings"],
                agents=len(agent_activity),
                waves=len(wave_activity)
            )

            return patterns

        except Exception as e:
            logger.error("collaboration_analysis_failed", error=str(e))
            return {}

    def sync_from_local_backup(self) -> int:
        """
        Sync findings from local backup to Qdrant (disaster recovery)

        Returns:
            Number of findings restored
        """
        try:
            restored = 0
            backup_files = list(self.local_backup_path.glob("*.json"))

            for backup_file in backup_files:
                try:
                    with open(backup_file, 'r') as f:
                        backup_data = json.load(f)

                    finding_id = backup_data["payload"]["finding_id"]

                    # Check if already in Qdrant
                    try:
                        self.qdrant.retrieve(
                            collection_name="agent_shared_memory",
                            ids=[finding_id]
                        )
                        continue  # Already exists
                    except Exception:
                        pass  # Doesn't exist, restore it

                    # Restore to Qdrant
                    point = PointStruct(
                        id=finding_id,
                        vector=backup_data["embedding"],
                        payload=backup_data["payload"]
                    )

                    self.qdrant.upsert(
                        collection_name="agent_shared_memory",
                        points=[point],
                        wait=True
                    )

                    restored += 1

                except Exception as e:
                    logger.warning(
                        "backup_restore_failed",
                        file=backup_file.name,
                        error=str(e)
                    )

            logger.info(
                "local_backup_sync_completed",
                restored=restored,
                total_backups=len(backup_files)
            )

            return restored

        except Exception as e:
            logger.error("backup_sync_failed", error=str(e))
            return 0

    def export_memories(
        self,
        output_path: Optional[Path] = None
    ) -> str:
        """
        Export all memories to JSON file

        Args:
            output_path: Where to save export

        Returns:
            Export file path
        """
        try:
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = self.local_backup_path / f"memory_export_{timestamp}.json"

            # Get all memories
            all_points, _ = self.qdrant.scroll(
                collection_name="agent_shared_memory",
                limit=100000,
                with_payload=True
            )

            # Format for export
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "total_memories": len(all_points),
                "memories": [
                    {
                        "finding_id": point.id,
                        **point.payload
                    }
                    for point in all_points
                ]
            }

            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)

            logger.info(
                "memories_exported",
                path=str(output_path),
                count=len(all_points)
            )

            return str(output_path)

        except Exception as e:
            logger.error("memory_export_failed", error=str(e))
            raise


# CLI Interface for Testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Qdrant Memory Agent")
    subparsers = parser.add_subparsers(dest="command")

    # Store command
    store_parser = subparsers.add_parser("store", help="Store a finding")
    store_parser.add_argument("finding", help="Finding to store")
    store_parser.add_argument("--agent", required=True, help="Agent name")
    store_parser.add_argument("--wave", type=int, help="Wave number")
    store_parser.add_argument("--tags", nargs="+", help="Tags")

    # Retrieve command
    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve experiences")
    retrieve_parser.add_argument("query", help="Search query")
    retrieve_parser.add_argument("--agent", help="Filter by agent")
    retrieve_parser.add_argument("--wave", type=int, help="Filter by wave")
    retrieve_parser.add_argument("--top-k", type=int, default=5, help="Number of results")

    # Patterns command
    subparsers.add_parser("patterns", help="Show collaboration patterns")

    # Sync command
    subparsers.add_parser("sync", help="Sync from local backup")

    args = parser.parse_args()

    agent = QdrantMemoryAgent()

    if args.command == "store":
        finding_id = agent.store_finding(
            finding=args.finding,
            agent_name=args.agent,
            context={"cli": True},
            tags=args.tags,
            wave=args.wave
        )
        print(f"✓ Finding stored: {finding_id}")

    elif args.command == "retrieve":
        results = agent.retrieve_experiences(
            query=args.query,
            agent_filter=args.agent,
            wave_filter=args.wave,
            top_k=args.top_k
        )
        print(f"\n🔍 Query: {args.query}")
        print(f"📊 Results: {len(results)}\n")
        for i, exp in enumerate(results, 1):
            print(f"{i}. Score: {exp['score']:.3f} | Agent: {exp['agent_name']}")
            print(f"   Finding: {exp['finding'][:200]}...")
            print(f"   Wave: {exp.get('wave', 'N/A')} | Tags: {exp['tags']}\n")

    elif args.command == "patterns":
        patterns = agent.get_collaboration_patterns()
        print("\n📊 Collaboration Patterns\n")
        print(f"Total Findings: {patterns['total_findings']}")
        print(f"\nAgent Activity:")
        for agent, count in list(patterns['agent_activity'].items())[:10]:
            print(f"  {agent}: {count} findings")
        print(f"\nWave Activity:")
        for wave, count in patterns['wave_activity'].items():
            print(f"  Wave {wave}: {count} findings")

    elif args.command == "sync":
        restored = agent.sync_from_local_backup()
        print(f"✓ Restored {restored} findings from local backup")
