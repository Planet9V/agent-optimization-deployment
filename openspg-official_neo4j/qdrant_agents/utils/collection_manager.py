#!/usr/bin/env python3
"""
Collection Manager - CRUD operations for Qdrant collections
Provides centralized collection management with health monitoring
"""

import os
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue,
    CollectionInfo, CollectionStatus
)
import structlog

logger = structlog.get_logger()

class CollectionManager:
    """
    Manages Qdrant collection lifecycle and health monitoring
    """

    def __init__(
        self,
        url: str = "http://localhost:6333",
        api_key: Optional[str] = None
    ):
        """Initialize collection manager"""
        self.url = url
        self.api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.client = QdrantClient(url=self.url, api_key=self.api_key)

        logger.info("collection_manager_initialized", url=self.url)

    def create_collection(
        self,
        name: str,
        vector_size: int = 3072,
        distance: Distance = Distance.COSINE,
        **kwargs
    ) -> bool:
        """
        Create a new collection with optimized configuration

        Args:
            name: Collection name
            vector_size: Dimension of vectors
            distance: Distance metric (COSINE, EUCLIDEAN, DOT)
            **kwargs: Additional collection parameters

        Returns:
            Success status
        """
        try:
            # Check if exists
            if self.collection_exists(name):
                logger.warning("collection_already_exists", name=name)
                return False

            # Create with optimized params
            self.client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=distance
                ),
                **kwargs
            )

            logger.info("collection_created", name=name, vector_size=vector_size)
            return True

        except Exception as e:
            logger.error("collection_creation_failed", name=name, error=str(e))
            raise

    def delete_collection(self, name: str, force: bool = False) -> bool:
        """
        Delete a collection

        Args:
            name: Collection name
            force: Skip safety checks

        Returns:
            Success status
        """
        try:
            if not force:
                # Safety check - verify collection exists
                if not self.collection_exists(name):
                    logger.warning("collection_not_found", name=name)
                    return False

            self.client.delete_collection(collection_name=name)
            logger.info("collection_deleted", name=name)
            return True

        except Exception as e:
            logger.error("collection_deletion_failed", name=name, error=str(e))
            raise

    def collection_exists(self, name: str) -> bool:
        """Check if collection exists"""
        try:
            collections = self.client.get_collections().collections
            return any(c.name == name for c in collections)
        except Exception as e:
            logger.error("collection_check_failed", name=name, error=str(e))
            return False

    def get_collection_info(self, name: str) -> Optional[CollectionInfo]:
        """Get detailed collection information"""
        try:
            return self.client.get_collection(collection_name=name)
        except Exception as e:
            logger.error("collection_info_failed", name=name, error=str(e))
            return None

    def get_collection_stats(self, name: str) -> Dict[str, Any]:
        """
        Get collection statistics

        Returns:
            Dict with vectors_count, points_count, segments, status
        """
        try:
            info = self.get_collection_info(name)
            if not info:
                return {}

            return {
                "name": name,
                "vectors_count": info.vectors_count or 0,
                "points_count": info.points_count,
                "segments_count": info.segments_count,
                "status": info.status,
                "config": {
                    "vector_size": info.config.params.vectors.size,
                    "distance": info.config.params.vectors.distance
                }
            }

        except Exception as e:
            logger.error("collection_stats_failed", name=name, error=str(e))
            return {}

    def list_collections(self) -> List[Dict[str, Any]]:
        """List all collections with stats"""
        try:
            collections = self.client.get_collections().collections
            return [
                {
                    "name": c.name,
                    "vectors_count": self.get_collection_stats(c.name).get("vectors_count", 0)
                }
                for c in collections
            ]

        except Exception as e:
            logger.error("list_collections_failed", error=str(e))
            return []

    def health_check(self, name: str) -> Dict[str, Any]:
        """
        Comprehensive health check for collection

        Returns:
            Health status with recommendations
        """
        try:
            stats = self.get_collection_stats(name)
            if not stats:
                return {"healthy": False, "error": "Collection not found"}

            # Health indicators
            healthy = True
            warnings = []
            recommendations = []

            # Check status
            if stats["status"] != CollectionStatus.GREEN:
                healthy = False
                warnings.append(f"Collection status: {stats['status']}")

            # Check vector count
            if stats["vectors_count"] == 0:
                warnings.append("No vectors in collection")
                recommendations.append("Index documentation to populate collection")

            # Check segment count
            if stats["segments_count"] > 10:
                warnings.append(f"High segment count: {stats['segments_count']}")
                recommendations.append("Consider optimizing collection")

            return {
                "healthy": healthy,
                "stats": stats,
                "warnings": warnings,
                "recommendations": recommendations
            }

        except Exception as e:
            logger.error("health_check_failed", name=name, error=str(e))
            return {"healthy": False, "error": str(e)}

    def optimize_collection(self, name: str) -> bool:
        """
        Optimize collection by triggering compaction

        Returns:
            Success status
        """
        try:
            # Trigger optimization
            self.client.update_collection(
                collection_name=name,
                optimizer_config={
                    "indexing_threshold": 20000
                }
            )

            logger.info("collection_optimized", name=name)
            return True

        except Exception as e:
            logger.error("collection_optimization_failed", name=name, error=str(e))
            return False

    def backup_collection(
        self,
        name: str,
        backup_path: str = "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/qdrant_backup"
    ) -> bool:
        """
        Backup collection to snapshot

        Args:
            name: Collection name
            backup_path: Backup directory path

        Returns:
            Success status
        """
        try:
            # Create snapshot
            snapshot = self.client.create_snapshot(collection_name=name)

            logger.info(
                "collection_backed_up",
                name=name,
                snapshot=snapshot.name,
                path=backup_path
            )
            return True

        except Exception as e:
            logger.error("collection_backup_failed", name=name, error=str(e))
            return False

    def get_vector_count(self, name: str) -> int:
        """Get total vector count in collection"""
        stats = self.get_collection_stats(name)
        return stats.get("vectors_count", 0)

    def get_points_by_filter(
        self,
        collection_name: str,
        filter_dict: Dict[str, Any],
        limit: int = 100
    ) -> List[PointStruct]:
        """
        Retrieve points by metadata filter

        Args:
            collection_name: Collection to query
            filter_dict: Filter conditions {"field": "value"}
            limit: Maximum points to return

        Returns:
            List of matching points
        """
        try:
            # Build filter
            conditions = [
                FieldCondition(
                    key=key,
                    match=MatchValue(value=value)
                )
                for key, value in filter_dict.items()
            ]

            filter_obj = Filter(must=conditions) if conditions else None

            # Scroll through results
            results, _ = self.client.scroll(
                collection_name=collection_name,
                scroll_filter=filter_obj,
                limit=limit,
                with_payload=True,
                with_vectors=True
            )

            logger.debug(
                "points_retrieved",
                collection=collection_name,
                count=len(results),
                filter=filter_dict
            )

            return results

        except Exception as e:
            logger.error(
                "points_retrieval_failed",
                collection=collection_name,
                error=str(e)
            )
            return []
