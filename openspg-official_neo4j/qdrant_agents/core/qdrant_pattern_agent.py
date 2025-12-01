#!/usr/bin/env python3
"""
Qdrant Pattern Agent - Pattern Discovery and Template Generation
Uses ML clustering to identify reusable implementation patterns
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
import json
import structlog

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.embedding_generator import EmbeddingGenerator
from utils.collection_manager import CollectionManager

logger = structlog.get_logger()

class QdrantPatternAgent:
    """
    Specialized agent for pattern discovery and template generation

    Capabilities:
    - Extract implementation patterns from agent memories
    - Cluster similar approaches using ML
    - Generate reusable templates
    - Detect anti-patterns
    - Track pattern effectiveness
    """

    def __init__(
        self,
        url: str = "http://localhost:6333",
        api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        min_pattern_frequency: int = 3,
        similarity_threshold: float = 0.7
    ):
        """Initialize pattern agent"""
        self.url = url
        self.api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.min_pattern_frequency = min_pattern_frequency
        self.similarity_threshold = similarity_threshold

        # Initialize components
        self.qdrant = QdrantClient(url=self.url, api_key=self.api_key)
        self.embedder = EmbeddingGenerator(
            api_key=self.openai_api_key,
            model="text-embedding-3-large",
            dimensions=3072
        )
        self.collection_mgr = CollectionManager(url=self.url, api_key=self.api_key)

        logger.info(
            "qdrant_pattern_agent_initialized",
            min_frequency=self.min_pattern_frequency,
            similarity_threshold=self.similarity_threshold
        )

    def extract_patterns(
        self,
        source_collection: str = "agent_shared_memory",
        clustering_algorithm: str = "kmeans",
        n_clusters: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract patterns from agent memories using ML clustering

        Args:
            source_collection: Collection to analyze
            clustering_algorithm: "kmeans" or "dbscan"
            n_clusters: Number of clusters (auto-detect if None)

        Returns:
            Discovered patterns with examples
        """
        try:
            # Get all memories with vectors
            memories, _ = self.qdrant.scroll(
                collection_name=source_collection,
                limit=10000,
                with_payload=True,
                with_vectors=True
            )

            if len(memories) < self.min_pattern_frequency:
                logger.warning(
                    "insufficient_data_for_patterns",
                    memories=len(memories),
                    min_required=self.min_pattern_frequency
                )
                return []

            # Extract vectors and metadata
            vectors = np.array([point.vector for point in memories])
            payloads = [point.payload for point in memories]

            # Perform clustering
            if clustering_algorithm == "kmeans":
                labels, n_clusters_actual = self._kmeans_clustering(vectors, n_clusters)
            elif clustering_algorithm == "dbscan":
                labels, n_clusters_actual = self._dbscan_clustering(vectors)
            else:
                raise ValueError(f"Unknown algorithm: {clustering_algorithm}")

            # Extract patterns from clusters
            patterns = self._extract_cluster_patterns(
                labels,
                vectors,
                payloads,
                n_clusters_actual
            )

            logger.info(
                "patterns_extracted",
                algorithm=clustering_algorithm,
                clusters=n_clusters_actual,
                patterns_found=len(patterns)
            )

            return patterns

        except Exception as e:
            logger.error("pattern_extraction_failed", error=str(e))
            return []

    def _kmeans_clustering(
        self,
        vectors: np.ndarray,
        n_clusters: Optional[int]
    ) -> Tuple[np.ndarray, int]:
        """Perform K-means clustering with optimal cluster selection"""
        if n_clusters is None:
            # Auto-detect optimal number of clusters
            n_clusters = self._find_optimal_clusters(vectors)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(vectors)

        return labels, n_clusters

    def _dbscan_clustering(
        self,
        vectors: np.ndarray
    ) -> Tuple[np.ndarray, int]:
        """Perform DBSCAN clustering (density-based)"""
        # DBSCAN doesn't require n_clusters
        # eps and min_samples are critical parameters
        dbscan = DBSCAN(eps=0.3, min_samples=self.min_pattern_frequency, metric='cosine')
        labels = dbscan.fit_predict(vectors)

        # Count actual clusters (excluding noise labeled as -1)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        return labels, n_clusters

    def _find_optimal_clusters(
        self,
        vectors: np.ndarray,
        max_clusters: int = 10
    ) -> int:
        """Find optimal number of clusters using silhouette score"""
        n_samples = len(vectors)
        max_clusters = min(max_clusters, n_samples // 2)

        if max_clusters < 2:
            return 2

        silhouette_scores = []

        for k in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(vectors)
            score = silhouette_score(vectors, labels)
            silhouette_scores.append((k, score))

        # Choose k with highest silhouette score
        optimal_k = max(silhouette_scores, key=lambda x: x[1])[0]

        logger.debug(
            "optimal_clusters_found",
            optimal_k=optimal_k,
            scores=silhouette_scores
        )

        return optimal_k

    def _extract_cluster_patterns(
        self,
        labels: np.ndarray,
        vectors: np.ndarray,
        payloads: List[Dict[str, Any]],
        n_clusters: int
    ) -> List[Dict[str, Any]]:
        """Extract patterns from clusters"""
        patterns = []

        for cluster_id in range(n_clusters):
            # Get points in this cluster
            cluster_mask = labels == cluster_id
            cluster_indices = np.where(cluster_mask)[0]

            if len(cluster_indices) < self.min_pattern_frequency:
                continue

            # Get cluster metadata
            cluster_payloads = [payloads[i] for i in cluster_indices]
            cluster_vectors = vectors[cluster_mask]

            # Calculate cluster centroid
            centroid = np.mean(cluster_vectors, axis=0)

            # Extract pattern characteristics
            pattern = self._analyze_cluster(
                cluster_id,
                cluster_payloads,
                centroid,
                cluster_vectors
            )

            patterns.append(pattern)

        return patterns

    def _analyze_cluster(
        self,
        cluster_id: int,
        payloads: List[Dict[str, Any]],
        centroid: np.ndarray,
        vectors: np.ndarray
    ) -> Dict[str, Any]:
        """Analyze a cluster to extract pattern characteristics"""
        # Aggregate metadata
        agents = defaultdict(int)
        waves = defaultdict(int)
        tags = defaultdict(int)
        contexts = []

        for payload in payloads:
            agents[payload.get("agent_name", "unknown")] += 1

            wave = payload.get("wave")
            if wave is not None:
                waves[wave] += 1

            for tag in payload.get("tags", []):
                tags[tag] += 1

            contexts.append(payload.get("context", {}))

        # Generate pattern description
        pattern_examples = [p.get("finding", "")[:200] for p in payloads[:5]]

        # Calculate cohesion (how similar are vectors in cluster)
        cohesion = self._calculate_cohesion(vectors, centroid)

        pattern = {
            "pattern_id": f"pattern_{cluster_id}",
            "frequency": len(payloads),
            "cohesion_score": float(cohesion),
            "primary_agents": dict(sorted(agents.items(), key=lambda x: x[1], reverse=True)[:3]),
            "wave_distribution": dict(sorted(waves.items())),
            "common_tags": dict(sorted(tags.items(), key=lambda x: x[1], reverse=True)[:5]),
            "examples": pattern_examples,
            "centroid": centroid.tolist(),
            "identified_at": datetime.now().isoformat()
        }

        return pattern

    def _calculate_cohesion(
        self,
        vectors: np.ndarray,
        centroid: np.ndarray
    ) -> float:
        """Calculate cluster cohesion (lower is better)"""
        distances = np.linalg.norm(vectors - centroid, axis=1)
        return float(np.mean(distances))

    def store_pattern(
        self,
        pattern: Dict[str, Any],
        description: Optional[str] = None
    ) -> str:
        """
        Store discovered pattern in query_patterns collection

        Args:
            pattern: Pattern to store
            description: Optional human-readable description

        Returns:
            Pattern ID
        """
        try:
            pattern_id = pattern.get("pattern_id", str(uuid.uuid4()))

            # Generate embedding from examples
            examples_text = " ".join(pattern["examples"])
            embedding = self.embedder.create(examples_text)

            # Prepare payload
            payload = {
                **pattern,
                "description": description or f"Pattern with {pattern['frequency']} instances",
                "stored_at": datetime.now().isoformat()
            }

            # Store in Qdrant
            point = PointStruct(
                id=pattern_id,
                vector=embedding,
                payload=payload
            )

            self.qdrant.upsert(
                collection_name="query_patterns",
                points=[point],
                wait=True
            )

            logger.info(
                "pattern_stored",
                pattern_id=pattern_id,
                frequency=pattern["frequency"]
            )

            return pattern_id

        except Exception as e:
            logger.error("pattern_storage_failed", error=str(e))
            raise

    def find_similar_patterns(
        self,
        query: str,
        top_k: int = 3,
        score_threshold: float = 0.6
    ) -> List[Dict[str, Any]]:
        """
        Find patterns similar to a query

        Args:
            query: Description of what you're implementing
            top_k: Number of patterns to return
            score_threshold: Minimum similarity

        Returns:
            Matching patterns
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
                    "pattern_id": result.payload.get("pattern_id", ""),
                    "frequency": result.payload.get("frequency", 0),
                    "cohesion_score": result.payload.get("cohesion_score", 0),
                    "primary_agents": result.payload.get("primary_agents", {}),
                    "examples": result.payload.get("examples", []),
                    "description": result.payload.get("description", "")
                })

            logger.info(
                "similar_patterns_found",
                query=query[:50],
                patterns=len(patterns)
            )

            return patterns

        except Exception as e:
            logger.error("pattern_search_failed", error=str(e))
            return []

    def detect_anti_patterns(
        self,
        error_threshold: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Detect anti-patterns (patterns with low success rates)

        Args:
            error_threshold: Minimum error rate to flag as anti-pattern

        Returns:
            Detected anti-patterns
        """
        try:
            # Get all patterns
            patterns, _ = self.qdrant.scroll(
                collection_name="query_patterns",
                limit=1000,
                with_payload=True
            )

            anti_patterns = []

            for pattern_point in patterns:
                payload = pattern_point.payload

                # Check for error indicators in tags or context
                error_tags = sum(
                    1 for tag in payload.get("common_tags", {}).keys()
                    if any(err in tag.lower() for err in ["error", "fail", "bug", "issue"])
                )

                total_tags = len(payload.get("common_tags", {}))

                if total_tags > 0:
                    error_rate = error_tags / total_tags

                    if error_rate >= error_threshold:
                        anti_patterns.append({
                            "pattern_id": payload.get("pattern_id", ""),
                            "error_rate": error_rate,
                            "frequency": payload.get("frequency", 0),
                            "examples": payload.get("examples", []),
                            "warning": "High error rate detected"
                        })

            logger.info("anti_patterns_detected", count=len(anti_patterns))

            return anti_patterns

        except Exception as e:
            logger.error("anti_pattern_detection_failed", error=str(e))
            return []

    def generate_template(
        self,
        pattern_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Generate reusable template from pattern

        Args:
            pattern_id: Pattern to convert to template

        Returns:
            Template specification
        """
        try:
            # Retrieve pattern
            results = self.qdrant.retrieve(
                collection_name="query_patterns",
                ids=[pattern_id]
            )

            if not results:
                logger.warning("pattern_not_found", pattern_id=pattern_id)
                return None

            pattern = results[0].payload

            # Generate template
            template = {
                "template_id": f"template_{pattern_id}",
                "based_on_pattern": pattern_id,
                "frequency": pattern.get("frequency", 0),
                "recommended_for": {
                    "waves": list(pattern.get("wave_distribution", {}).keys()),
                    "scenarios": list(pattern.get("common_tags", {}).keys())
                },
                "example_usage": pattern.get("examples", [])[0] if pattern.get("examples") else "",
                "best_practices": self._extract_best_practices(pattern),
                "generated_at": datetime.now().isoformat()
            }

            logger.info("template_generated", template_id=template["template_id"])

            return template

        except Exception as e:
            logger.error("template_generation_failed", pattern_id=pattern_id, error=str(e))
            return None

    def _extract_best_practices(
        self,
        pattern: Dict[str, Any]
    ) -> List[str]:
        """Extract best practices from pattern analysis"""
        practices = []

        # High frequency = proven approach
        if pattern.get("frequency", 0) >= 10:
            practices.append("Well-tested approach used multiple times successfully")

        # Low cohesion might indicate flexibility
        if pattern.get("cohesion_score", 1.0) < 0.3:
            practices.append("Highly adaptable pattern with diverse implementations")

        # Multiple agents = collaborative pattern
        primary_agents = pattern.get("primary_agents", {})
        if len(primary_agents) >= 3:
            practices.append("Cross-agent collaboration pattern")

        # Wave distribution insights
        waves = pattern.get("wave_distribution", {})
        if len(waves) > 1:
            practices.append(f"Applicable across waves {sorted(waves.keys())}")

        return practices

    def export_patterns(
        self,
        output_path: Optional[Path] = None
    ) -> str:
        """
        Export all patterns to JSON

        Args:
            output_path: Where to save export

        Returns:
            Export file path
        """
        try:
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = Path(f"/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/qdrant_backup/patterns_export_{timestamp}.json")

            # Get all patterns
            patterns, _ = self.qdrant.scroll(
                collection_name="query_patterns",
                limit=10000,
                with_payload=True
            )

            # Format for export
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "total_patterns": len(patterns),
                "patterns": [point.payload for point in patterns]
            }

            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)

            logger.info(
                "patterns_exported",
                path=str(output_path),
                count=len(patterns)
            )

            return str(output_path)

        except Exception as e:
            logger.error("pattern_export_failed", error=str(e))
            raise


# CLI Interface for Testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Qdrant Pattern Agent")
    subparsers = parser.add_subparsers(dest="command")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract patterns")
    extract_parser.add_argument("--algorithm", choices=["kmeans", "dbscan"],
                               default="kmeans", help="Clustering algorithm")
    extract_parser.add_argument("--clusters", type=int, help="Number of clusters")

    # Find command
    find_parser = subparsers.add_parser("find", help="Find similar patterns")
    find_parser.add_argument("query", help="Search query")
    find_parser.add_argument("--top-k", type=int, default=3, help="Number of results")

    # Anti-patterns command
    subparsers.add_parser("anti-patterns", help="Detect anti-patterns")

    # Export command
    subparsers.add_parser("export", help="Export all patterns")

    args = parser.parse_args()

    agent = QdrantPatternAgent()

    if args.command == "extract":
        patterns = agent.extract_patterns(
            clustering_algorithm=args.algorithm,
            n_clusters=args.clusters
        )
        print(f"\n📊 Patterns Extracted: {len(patterns)}\n")
        for i, pattern in enumerate(patterns, 1):
            print(f"{i}. Pattern ID: {pattern['pattern_id']}")
            print(f"   Frequency: {pattern['frequency']}")
            print(f"   Cohesion: {pattern['cohesion_score']:.3f}")
            print(f"   Agents: {pattern['primary_agents']}")
            print(f"   Example: {pattern['examples'][0][:100]}...\n")

            # Store pattern
            agent.store_pattern(pattern)

    elif args.command == "find":
        patterns = agent.find_similar_patterns(
            query=args.query,
            top_k=args.top_k
        )
        print(f"\n🔍 Query: {args.query}")
        print(f"📊 Patterns Found: {len(patterns)}\n")
        for i, pattern in enumerate(patterns, 1):
            print(f"{i}. Score: {pattern['score']:.3f} | Frequency: {pattern['frequency']}")
            print(f"   {pattern['description']}")
            print(f"   Examples: {pattern['examples'][0][:150]}...\n")

    elif args.command == "anti-patterns":
        anti_patterns = agent.detect_anti_patterns()
        print(f"\n⚠️  Anti-Patterns Detected: {len(anti_patterns)}\n")
        for i, ap in enumerate(anti_patterns, 1):
            print(f"{i}. Pattern ID: {ap['pattern_id']}")
            print(f"   Error Rate: {ap['error_rate']:.1%}")
            print(f"   Frequency: {ap['frequency']}")
            print(f"   Warning: {ap['warning']}\n")

    elif args.command == "export":
        path = agent.export_patterns()
        print(f"✓ Patterns exported to: {path}")
