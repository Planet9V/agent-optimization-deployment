#!/usr/bin/env python3
"""
Qdrant Sync Agent - Dual Memory Synchronization
Manages bidirectional sync between Qdrant and local backup with conflict resolution
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import structlog

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.collection_manager import CollectionManager

logger = structlog.get_logger()

class QdrantSyncAgent:
    """
    Specialized agent for Qdrant-local synchronization

    Capabilities:
    - Bidirectional sync between Qdrant and local storage
    - Conflict resolution strategies
    - Git integration for version control
    - Disaster recovery
    - Incremental sync optimization
    """

    def __init__(
        self,
        url: str = "http://localhost:6333",
        api_key: Optional[str] = None,
        local_backup_path: Optional[Path] = None,
        git_auto_commit: bool = True,
        conflict_strategy: str = "qdrant_wins"
    ):
        """
        Initialize sync agent

        Args:
            url: Qdrant URL
            api_key: Qdrant API key
            local_backup_path: Local backup directory
            git_auto_commit: Auto-commit changes to git
            conflict_strategy: "qdrant_wins", "local_wins", or "merge"
        """
        self.url = url
        self.api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.local_backup_path = local_backup_path or Path(
            "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/qdrant_backup"
        )
        self.git_auto_commit = git_auto_commit
        self.conflict_strategy = conflict_strategy

        # Initialize components
        self.qdrant = QdrantClient(url=self.url, api_key=self.api_key)
        self.collection_mgr = CollectionManager(url=self.url, api_key=self.api_key)

        # Ensure backup directory exists
        self.local_backup_path.mkdir(parents=True, exist_ok=True)

        logger.info(
            "qdrant_sync_agent_initialized",
            backup_path=str(self.local_backup_path),
            conflict_strategy=self.conflict_strategy
        )

    def sync_collection(
        self,
        collection_name: str,
        direction: str = "bidirectional"
    ) -> Dict[str, Any]:
        """
        Synchronize a collection

        Args:
            collection_name: Collection to sync
            direction: "qdrant_to_local", "local_to_qdrant", or "bidirectional"

        Returns:
            Sync statistics
        """
        try:
            stats = {
                "collection": collection_name,
                "direction": direction,
                "timestamp": datetime.now().isoformat(),
                "qdrant_to_local": 0,
                "local_to_qdrant": 0,
                "conflicts_resolved": 0,
                "errors": 0
            }

            if direction in ["bidirectional", "qdrant_to_local"]:
                # Sync from Qdrant to local
                qdrant_stats = self._sync_qdrant_to_local(collection_name)
                stats["qdrant_to_local"] = qdrant_stats["synced"]
                stats["conflicts_resolved"] += qdrant_stats["conflicts"]

            if direction in ["bidirectional", "local_to_qdrant"]:
                # Sync from local to Qdrant
                local_stats = self._sync_local_to_qdrant(collection_name)
                stats["local_to_qdrant"] = local_stats["synced"]
                stats["conflicts_resolved"] += local_stats["conflicts"]

            # Git commit if enabled
            if self.git_auto_commit and direction in ["bidirectional", "qdrant_to_local"]:
                self._git_commit(collection_name, stats)

            logger.info(
                "collection_sync_completed",
                collection=collection_name,
                **stats
            )

            return stats

        except Exception as e:
            logger.error("collection_sync_failed", collection=collection_name, error=str(e))
            return {"error": str(e)}

    def _sync_qdrant_to_local(self, collection_name: str) -> Dict[str, int]:
        """Sync from Qdrant to local filesystem"""
        try:
            # Get all points from Qdrant
            points, _ = self.qdrant.scroll(
                collection_name=collection_name,
                limit=100000,
                with_payload=True,
                with_vectors=True
            )

            collection_dir = self.local_backup_path / collection_name
            collection_dir.mkdir(parents=True, exist_ok=True)

            synced = 0
            conflicts = 0

            for point in points:
                point_id = str(point.id)
                local_file = collection_dir / f"{point_id}.json"

                # Check for conflicts
                if local_file.exists():
                    conflict_result = self._resolve_conflict(
                        point,
                        local_file,
                        "qdrant_source"
                    )
                    if conflict_result["conflict"]:
                        conflicts += 1

                # Write to local
                data = {
                    "id": point_id,
                    "vector": point.vector,
                    "payload": point.payload,
                    "synced_at": datetime.now().isoformat()
                }

                with open(local_file, 'w') as f:
                    json.dump(data, f, indent=2)

                synced += 1

            return {"synced": synced, "conflicts": conflicts}

        except Exception as e:
            logger.error("qdrant_to_local_sync_failed", error=str(e))
            return {"synced": 0, "conflicts": 0}

    def _sync_local_to_qdrant(self, collection_name: str) -> Dict[str, int]:
        """Sync from local filesystem to Qdrant"""
        try:
            collection_dir = self.local_backup_path / collection_name

            if not collection_dir.exists():
                logger.warning("no_local_backup", collection=collection_name)
                return {"synced": 0, "conflicts": 0}

            local_files = list(collection_dir.glob("*.json"))
            synced = 0
            conflicts = 0

            for local_file in local_files:
                try:
                    with open(local_file, 'r') as f:
                        data = json.load(f)

                    point_id = data["id"]

                    # Check if exists in Qdrant
                    try:
                        existing = self.qdrant.retrieve(
                            collection_name=collection_name,
                            ids=[point_id]
                        )

                        # Conflict: exists in both
                        if existing:
                            conflict_result = self._resolve_conflict(
                                data,
                                local_file,
                                "local_source"
                            )
                            if conflict_result["conflict"]:
                                conflicts += 1

                            if not conflict_result["use_local"]:
                                continue  # Skip this point

                    except Exception:
                        pass  # Doesn't exist in Qdrant, proceed with insert

                    # Upsert to Qdrant
                    point = PointStruct(
                        id=point_id,
                        vector=data["vector"],
                        payload=data["payload"]
                    )

                    self.qdrant.upsert(
                        collection_name=collection_name,
                        points=[point],
                        wait=True
                    )

                    synced += 1

                except Exception as e:
                    logger.warning(
                        "point_sync_failed",
                        file=local_file.name,
                        error=str(e)
                    )

            return {"synced": synced, "conflicts": conflicts}

        except Exception as e:
            logger.error("local_to_qdrant_sync_failed", error=str(e))
            return {"synced": 0, "conflicts": 0}

    def _resolve_conflict(
        self,
        point_data: Any,
        local_file: Path,
        source: str
    ) -> Dict[str, Any]:
        """
        Resolve sync conflicts

        Args:
            point_data: Data from Qdrant or dict from local
            local_file: Local file path
            source: "qdrant_source" or "local_source"

        Returns:
            Resolution result
        """
        try:
            # Load local data
            with open(local_file, 'r') as f:
                local_data = json.load(f)

            # Extract timestamps
            if source == "qdrant_source":
                qdrant_payload = point_data.payload
                qdrant_timestamp = qdrant_payload.get("timestamp", "")
                local_timestamp = local_data.get("synced_at", "")
            else:
                qdrant_timestamp = ""
                local_timestamp = local_data.get("synced_at", "")

            # Compute hashes to detect changes
            if source == "qdrant_source":
                qdrant_hash = self._compute_hash(point_data.payload)
            else:
                qdrant_hash = self._compute_hash(point_data.get("payload", {}))

            local_hash = self._compute_hash(local_data.get("payload", {}))

            # No conflict if data is identical
            if qdrant_hash == local_hash:
                return {"conflict": False, "use_local": False}

            # Conflict detected - apply strategy
            if self.conflict_strategy == "qdrant_wins":
                use_local = False
            elif self.conflict_strategy == "local_wins":
                use_local = True
            else:  # merge strategy
                # Use newer timestamp
                try:
                    qdrant_time = datetime.fromisoformat(qdrant_timestamp) if qdrant_timestamp else datetime.min
                    local_time = datetime.fromisoformat(local_timestamp) if local_timestamp else datetime.min
                    use_local = local_time > qdrant_time
                except Exception:
                    use_local = False  # Default to Qdrant on parse error

            logger.warning(
                "conflict_detected",
                file=local_file.name,
                strategy=self.conflict_strategy,
                resolution="local" if use_local else "qdrant"
            )

            return {
                "conflict": True,
                "use_local": use_local,
                "qdrant_hash": qdrant_hash,
                "local_hash": local_hash
            }

        except Exception as e:
            logger.error("conflict_resolution_failed", error=str(e))
            return {"conflict": True, "use_local": False}

    def _compute_hash(self, data: Dict[str, Any]) -> str:
        """Compute hash of data for conflict detection"""
        # Create deterministic JSON string
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()

    def _git_commit(self, collection_name: str, stats: Dict[str, Any]):
        """Commit changes to git"""
        try:
            import subprocess

            os.chdir(str(self.local_backup_path))

            # Add all changes
            subprocess.run(["git", "add", collection_name], check=True)

            # Commit with stats
            commit_message = f"""Sync {collection_name} - {datetime.now().isoformat()}

Qdrant → Local: {stats['qdrant_to_local']}
Local → Qdrant: {stats['local_to_qdrant']}
Conflicts: {stats['conflicts_resolved']}
"""
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                check=False  # Don't fail if nothing to commit
            )

            logger.info("git_commit_completed", collection=collection_name)

        except Exception as e:
            logger.warning("git_commit_failed", error=str(e))

    def sync_all_collections(
        self,
        direction: str = "bidirectional"
    ) -> List[Dict[str, Any]]:
        """
        Sync all collections

        Args:
            direction: Sync direction

        Returns:
            Stats for all collections
        """
        try:
            collections = self.collection_mgr.list_collections()

            results = []
            for collection in collections:
                stats = self.sync_collection(
                    collection_name=collection["name"],
                    direction=direction
                )
                results.append(stats)

            logger.info(
                "all_collections_synced",
                collections=len(results),
                direction=direction
            )

            return results

        except Exception as e:
            logger.error("all_collections_sync_failed", error=str(e))
            return []

    def scheduled_sync(
        self,
        interval_hours: int = 4,
        direction: str = "bidirectional"
    ):
        """
        Run scheduled sync (daemon mode)

        Args:
            interval_hours: Sync interval
            direction: Sync direction
        """
        import time

        logger.info(
            "scheduled_sync_started",
            interval_hours=interval_hours,
            direction=direction
        )

        while True:
            try:
                results = self.sync_all_collections(direction=direction)

                total_synced = sum(
                    r.get("qdrant_to_local", 0) + r.get("local_to_qdrant", 0)
                    for r in results
                )

                logger.info(
                    "scheduled_sync_completed",
                    total_synced=total_synced
                )

            except Exception as e:
                logger.error("scheduled_sync_error", error=str(e))

            # Sleep until next sync
            time.sleep(interval_hours * 3600)

    def disaster_recovery(
        self,
        collection_name: str
    ) -> Dict[str, Any]:
        """
        Recover collection from local backup

        Args:
            collection_name: Collection to recover

        Returns:
            Recovery statistics
        """
        try:
            logger.warning(
                "disaster_recovery_initiated",
                collection=collection_name
            )

            # Delete existing collection
            self.collection_mgr.delete_collection(collection_name, force=True)

            # Recreate collection (assuming 3072-dimensional vectors)
            self.collection_mgr.create_collection(
                name=collection_name,
                vector_size=3072
            )

            # Restore from local
            stats = self._sync_local_to_qdrant(collection_name)

            logger.warning(
                "disaster_recovery_completed",
                collection=collection_name,
                recovered_points=stats["synced"]
            )

            return {
                "collection": collection_name,
                "recovered_points": stats["synced"],
                "status": "success"
            }

        except Exception as e:
            logger.error("disaster_recovery_failed", error=str(e))
            return {"error": str(e)}


# CLI Interface for Testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Qdrant Sync Agent")
    subparsers = parser.add_subparsers(dest="command")

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Sync a collection")
    sync_parser.add_argument("collection", help="Collection name")
    sync_parser.add_argument("--direction", choices=["bidirectional", "qdrant_to_local", "local_to_qdrant"],
                            default="bidirectional", help="Sync direction")

    # Sync all command
    sync_all_parser = subparsers.add_parser("sync-all", help="Sync all collections")
    sync_all_parser.add_argument("--direction", choices=["bidirectional", "qdrant_to_local", "local_to_qdrant"],
                                default="bidirectional", help="Sync direction")

    # Disaster recovery command
    recover_parser = subparsers.add_parser("recover", help="Disaster recovery")
    recover_parser.add_argument("collection", help="Collection to recover")

    # Scheduled sync command
    scheduled_parser = subparsers.add_parser("scheduled", help="Run scheduled sync daemon")
    scheduled_parser.add_argument("--interval", type=int, default=4, help="Sync interval (hours)")
    scheduled_parser.add_argument("--direction", choices=["bidirectional", "qdrant_to_local", "local_to_qdrant"],
                                 default="bidirectional", help="Sync direction")

    args = parser.parse_args()

    agent = QdrantSyncAgent()

    if args.command == "sync":
        stats = agent.sync_collection(
            collection_name=args.collection,
            direction=args.direction
        )
        print(f"\n✓ Sync Completed: {args.collection}")
        print(f"Qdrant → Local: {stats.get('qdrant_to_local', 0)}")
        print(f"Local → Qdrant: {stats.get('local_to_qdrant', 0)}")
        print(f"Conflicts: {stats.get('conflicts_resolved', 0)}")

    elif args.command == "sync-all":
        results = agent.sync_all_collections(direction=args.direction)
        print(f"\n✓ All Collections Synced: {len(results)}\n")
        for result in results:
            print(f"{result['collection']}:")
            print(f"  Qdrant → Local: {result.get('qdrant_to_local', 0)}")
            print(f"  Local → Qdrant: {result.get('local_to_qdrant', 0)}")
            print(f"  Conflicts: {result.get('conflicts_resolved', 0)}\n")

    elif args.command == "recover":
        result = agent.disaster_recovery(args.collection)
        print(f"\n⚠️  Disaster Recovery: {args.collection}")
        print(f"Recovered Points: {result.get('recovered_points', 0)}")
        print(f"Status: {result.get('status', 'failed')}")

    elif args.command == "scheduled":
        print(f"\n🔄 Starting scheduled sync daemon (interval: {args.interval}h)")
        agent.scheduled_sync(interval_hours=args.interval, direction=args.direction)
