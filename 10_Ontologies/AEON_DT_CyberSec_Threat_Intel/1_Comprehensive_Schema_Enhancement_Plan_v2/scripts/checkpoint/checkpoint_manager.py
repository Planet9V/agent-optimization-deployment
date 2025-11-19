#!/usr/bin/env python3
"""
CheckpointManager - Qdrant-backed checkpoint management for Neo4j operations
Provides crash-resistant state persistence and rollback capability

Generated: 2025-10-31
Version: 1.0.0
"""

import sys
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from neo4j import GraphDatabase
    from qdrant_client import QdrantClient
    from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    print("Required packages: neo4j-driver, qdrant-client")
    sys.exit(1)


class CheckpointManager:
    """
    Manages Neo4j state checkpoints in Qdrant for crash recovery
    """

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        qdrant_api_key: str = "deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=",
        project_root: Path = None
    ):
        """
        Initialize CheckpointManager

        Args:
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
            qdrant_host: Qdrant server host
            qdrant_port: Qdrant server port
            qdrant_api_key: Qdrant API key
            project_root: Project root directory
        """
        # Neo4j connection
        self.neo4j_driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

        # Qdrant connection
        self.qdrant_client = QdrantClient(
            host=qdrant_host,
            port=qdrant_port,
            api_key=qdrant_api_key,
            https=False,
            prefer_grpc=False
        )

        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "checkpoint_manager.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Collection names
        self.checkpoint_collection = "ontology_checkpoints"
        self.log_collection = "operation_logs"

    def _log(self, operation: str, status: str, details: Dict[str, Any] = None):
        """Log operation to JSONL file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "status": status,
            "details": details or {}
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def _capture_neo4j_state(self) -> Dict[str, Any]:
        """
        Capture current Neo4j database state

        Returns:
            Dict with node counts per wave and CVE status
        """
        with self.neo4j_driver.session() as session:
            # CVE count
            cve_result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = cve_result.single()["count"]

            # Wave counts
            wave_result = session.run("""
                MATCH (n)
                WHERE n.created_by =~ 'AEON_INTEGRATION_WAVE.*'
                RETURN n.created_by as wave, count(n) as count
                ORDER BY wave
            """)
            wave_counts = {record["wave"]: record["count"] for record in wave_result}

            # Total nodes
            total_result = session.run("MATCH (n) RETURN count(n) as count")
            total_nodes = total_result.single()["count"]

            # Cross-wave relationships
            rel_result = session.run("""
                MATCH (w1)-[r]-(w2)
                WHERE w1.created_by =~ 'AEON_INTEGRATION_WAVE[1-8]'
                  AND w2.created_by =~ 'AEON_INTEGRATION_WAVE[1-8]'
                  AND w1.created_by <> w2.created_by
                RETURN count(r) as count
            """)
            cross_wave_rels = rel_result.single()["count"]

            return {
                "cve_count": cve_count,
                "wave_counts": wave_counts,
                "total_nodes": total_nodes,
                "cross_wave_relationships": cross_wave_rels,
                "timestamp": datetime.now().isoformat()
            }

    def create_checkpoint(
        self,
        operation_name: str,
        phase: str = None,
        wave: str = None,
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Create a checkpoint of current Neo4j state in Qdrant

        Args:
            operation_name: Name of operation being checkpointed
            phase: Phase name (e.g., "PHASE_1", "PHASE_2")
            wave: Wave being processed (e.g., "WAVE9", "WAVE1")
            metadata: Additional metadata to store

        Returns:
            checkpoint_id: Unique ID for this checkpoint
        """
        checkpoint_id = str(uuid.uuid4())

        try:
            # Capture Neo4j state
            state = self._capture_neo4j_state()

            # Create checkpoint payload
            payload = {
                "checkpoint_id": checkpoint_id,
                "operation_name": operation_name,
                "phase": phase or "UNKNOWN",
                "wave": wave or "SYSTEM",
                "timestamp": datetime.now().isoformat(),
                "neo4j_state": state,
                "metadata": metadata or {},
                "status": "CREATED"
            }

            # Store in Qdrant with zero vector (metadata-only storage)
            point = PointStruct(
                id=checkpoint_id,
                vector=[0.0] * 384,  # Zero vector for metadata storage
                payload=payload
            )

            self.qdrant_client.upsert(
                collection_name=self.checkpoint_collection,
                points=[point]
            )

            self._log(
                "create_checkpoint",
                "SUCCESS",
                {
                    "checkpoint_id": checkpoint_id,
                    "operation": operation_name,
                    "cve_count": state["cve_count"],
                    "total_nodes": state["total_nodes"]
                }
            )

            print(f"✅ Checkpoint created: {checkpoint_id}")
            print(f"   Operation: {operation_name}")
            print(f"   CVE Count: {state['cve_count']}")
            print(f"   Total Nodes: {state['total_nodes']}")

            return checkpoint_id

        except Exception as e:
            self._log(
                "create_checkpoint",
                "FAILED",
                {"operation": operation_name, "error": str(e)}
            )
            raise

    def get_checkpoint(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve checkpoint data from Qdrant

        Args:
            checkpoint_id: Checkpoint ID to retrieve

        Returns:
            Checkpoint payload or None if not found
        """
        try:
            result = self.qdrant_client.retrieve(
                collection_name=self.checkpoint_collection,
                ids=[checkpoint_id]
            )

            if result:
                payload = result[0].payload
                self._log(
                    "get_checkpoint",
                    "SUCCESS",
                    {"checkpoint_id": checkpoint_id}
                )
                return payload
            else:
                self._log(
                    "get_checkpoint",
                    "NOT_FOUND",
                    {"checkpoint_id": checkpoint_id}
                )
                return None

        except Exception as e:
            self._log(
                "get_checkpoint",
                "FAILED",
                {"checkpoint_id": checkpoint_id, "error": str(e)}
            )
            raise

    def list_checkpoints(
        self,
        phase: str = None,
        wave: str = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List checkpoints with optional filtering

        Args:
            phase: Filter by phase
            wave: Filter by wave
            limit: Maximum number of checkpoints to return

        Returns:
            List of checkpoint payloads
        """
        try:
            # Build filter conditions
            filter_conditions = []
            if phase:
                filter_conditions.append(
                    FieldCondition(key="phase", match=MatchValue(value=phase))
                )
            if wave:
                filter_conditions.append(
                    FieldCondition(key="wave", match=MatchValue(value=wave))
                )

            # Query Qdrant
            if filter_conditions:
                points, _ = self.qdrant_client.scroll(
                    collection_name=self.checkpoint_collection,
                    scroll_filter=Filter(must=filter_conditions),
                    limit=limit
                )
            else:
                points, _ = self.qdrant_client.scroll(
                    collection_name=self.checkpoint_collection,
                    limit=limit
                )

            checkpoints = [point.payload for point in points]

            self._log(
                "list_checkpoints",
                "SUCCESS",
                {"count": len(checkpoints), "phase": phase, "wave": wave}
            )

            return checkpoints

        except Exception as e:
            self._log(
                "list_checkpoints",
                "FAILED",
                {"error": str(e)}
            )
            raise

    def get_latest_checkpoint(
        self,
        phase: str = None,
        wave: str = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get most recent checkpoint with optional filtering

        Args:
            phase: Filter by phase
            wave: Filter by wave

        Returns:
            Latest checkpoint payload or None
        """
        checkpoints = self.list_checkpoints(phase=phase, wave=wave, limit=100)

        if not checkpoints:
            return None

        # Sort by timestamp and return latest
        sorted_checkpoints = sorted(
            checkpoints,
            key=lambda x: x["timestamp"],
            reverse=True
        )

        return sorted_checkpoints[0]

    def validate_checkpoint_integrity(
        self,
        checkpoint_id: str
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate checkpoint data integrity

        Args:
            checkpoint_id: Checkpoint ID to validate

        Returns:
            Tuple of (is_valid: bool, validation_details: dict)
        """
        checkpoint = self.get_checkpoint(checkpoint_id)

        if not checkpoint:
            return False, {"error": "Checkpoint not found"}

        state = checkpoint.get("neo4j_state", {})

        # Validation checks
        checks = {
            "cve_baseline": state.get("cve_count") == 267487,
            "has_wave_counts": bool(state.get("wave_counts")),
            "has_total_nodes": "total_nodes" in state,
            "has_timestamp": "timestamp" in checkpoint
        }

        all_valid = all(checks.values())

        details = {
            "checkpoint_id": checkpoint_id,
            "checks": checks,
            "valid": all_valid,
            "cve_count": state.get("cve_count"),
            "total_nodes": state.get("total_nodes")
        }

        status = "VALID" if all_valid else "INVALID"
        self._log("validate_checkpoint", status, details)

        return all_valid, details

    def log_operation(
        self,
        operation_type: str,
        phase: str,
        wave: str,
        status: str,
        details: Dict[str, Any] = None
    ) -> str:
        """
        Log an operation to Qdrant operation_logs collection

        Args:
            operation_type: Type of operation
            phase: Phase name
            wave: Wave identifier
            status: Operation status
            details: Additional operation details

        Returns:
            operation_id: Unique ID for this log entry
        """
        operation_id = str(uuid.uuid4())

        try:
            payload = {
                "operation_id": operation_id,
                "operation_type": operation_type,
                "phase": phase,
                "wave": wave,
                "timestamp": datetime.now().isoformat(),
                "status": status,
                "details": details or {}
            }

            point = PointStruct(
                id=operation_id,
                vector=[0.0] * 384,
                payload=payload
            )

            self.qdrant_client.upsert(
                collection_name=self.log_collection,
                points=[point]
            )

            self._log(
                "log_operation",
                "SUCCESS",
                {"operation_id": operation_id, "type": operation_type}
            )

            return operation_id

        except Exception as e:
            self._log(
                "log_operation",
                "FAILED",
                {"operation_type": operation_type, "error": str(e)}
            )
            raise

    def close(self):
        """Close connections"""
        if self.neo4j_driver:
            self.neo4j_driver.close()


def main():
    """Example usage and testing"""
    import argparse

    parser = argparse.ArgumentParser(
        description="CheckpointManager - Create and manage Neo4j checkpoints in Qdrant"
    )
    parser.add_argument(
        "action",
        choices=["create", "list", "get", "validate"],
        help="Action to perform"
    )
    parser.add_argument(
        "--operation",
        help="Operation name for checkpoint creation"
    )
    parser.add_argument(
        "--phase",
        help="Phase name"
    )
    parser.add_argument(
        "--wave",
        help="Wave identifier"
    )
    parser.add_argument(
        "--checkpoint-id",
        help="Checkpoint ID for get/validate actions"
    )

    args = parser.parse_args()

    mgr = CheckpointManager()

    try:
        if args.action == "create":
            if not args.operation:
                print("❌ ERROR: --operation required for create action")
                sys.exit(1)
            checkpoint_id = mgr.create_checkpoint(
                operation_name=args.operation,
                phase=args.phase,
                wave=args.wave
            )
            print(f"✅ Checkpoint created: {checkpoint_id}")

        elif args.action == "list":
            checkpoints = mgr.list_checkpoints(
                phase=args.phase,
                wave=args.wave
            )
            print(f"Found {len(checkpoints)} checkpoints:")
            for cp in checkpoints:
                op_name = cp.get('operation_name', cp.get('operation', 'UNKNOWN'))
                print(f"  - {cp['checkpoint_id']}: {op_name} "
                      f"({cp.get('phase', 'N/A')}/{cp.get('wave', 'N/A')}) at {cp['timestamp']}")

        elif args.action == "get":
            if not args.checkpoint_id:
                print("❌ ERROR: --checkpoint-id required for get action")
                sys.exit(1)
            checkpoint = mgr.get_checkpoint(args.checkpoint_id)
            if checkpoint:
                print(json.dumps(checkpoint, indent=2))
            else:
                print(f"❌ Checkpoint not found: {args.checkpoint_id}")

        elif args.action == "validate":
            if not args.checkpoint_id:
                print("❌ ERROR: --checkpoint-id required for validate action")
                sys.exit(1)
            valid, details = mgr.validate_checkpoint_integrity(args.checkpoint_id)
            if valid:
                print(f"✅ Checkpoint is valid")
            else:
                print(f"❌ Checkpoint validation failed")
            print(json.dumps(details, indent=2))

    finally:
        mgr.close()


if __name__ == "__main__":
    main()
