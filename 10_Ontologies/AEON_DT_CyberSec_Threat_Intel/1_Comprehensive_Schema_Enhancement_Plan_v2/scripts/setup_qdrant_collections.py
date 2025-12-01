#!/usr/bin/env python3
"""
Qdrant Collections Setup for Neo4j Ontology Checkpoint Management
Creates collections for crash-resistant state persistence

Generated: 2025-10-31
Version: 1.0.0
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import json

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
except ImportError:
    print("ERROR: qdrant-client not installed")
    print("Run: pip install qdrant-client")
    sys.exit(1)


class QdrantSetup:
    """Initialize Qdrant collections for ontology checkpoint management"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        api_key: str = None,
        log_file: Path = None
    ):
        """
        Initialize Qdrant setup manager

        Args:
            host: Qdrant server host
            port: Qdrant server port
            api_key: Qdrant API key for authentication
            log_file: Path to log file for operation tracking
        """
        self.client = QdrantClient(
            host=host,
            port=port,
            api_key=api_key,
            https=False,  # Use HTTP instead of HTTPS
            prefer_grpc=False  # Use REST API instead of gRPC
        )
        self.log_file = log_file or Path(__file__).parent.parent / "logs" / "qdrant_setup.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def _log(self, operation: str, status: str, details: Dict[str, Any] = None):
        """Log operation to JSONL file"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "status": status,
            "details": details or {}
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        print(f"[{status}] {operation}: {json.dumps(details or {}, indent=2)}")

    def create_checkpoint_collection(self) -> bool:
        """
        Create ontology_checkpoints collection for Neo4j state snapshots

        Returns:
            bool: True if created successfully
        """
        collection_name = "ontology_checkpoints"

        try:
            # Check if collection already exists
            collections = self.client.get_collections().collections
            if any(c.name == collection_name for c in collections):
                self._log(
                    "create_checkpoint_collection",
                    "EXISTS",
                    {"collection": collection_name, "action": "skipped"}
                )
                return True

            # Create collection with 384-dimensional vectors (typical embedding size)
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=384,  # Dimension for semantic search of checkpoint metadata
                    distance=Distance.COSINE
                )
            )

            self._log(
                "create_checkpoint_collection",
                "SUCCESS",
                {
                    "collection": collection_name,
                    "vector_size": 384,
                    "distance_metric": "COSINE"
                }
            )

            # Create initial test checkpoint
            test_point = PointStruct(
                id=1,
                vector=[0.0] * 384,
                payload={
                    "checkpoint_id": "INITIAL_SETUP",
                    "operation": "qdrant_initialization",
                    "timestamp": datetime.utcnow().isoformat(),
                    "cve_count": 267487,
                    "total_nodes": 489179,
                    "metadata": {
                        "purpose": "Test checkpoint to verify collection setup",
                        "status": "initialized"
                    }
                }
            )

            self.client.upsert(
                collection_name=collection_name,
                points=[test_point]
            )

            self._log(
                "create_test_checkpoint",
                "SUCCESS",
                {"checkpoint_id": "INITIAL_SETUP"}
            )

            return True

        except Exception as e:
            self._log(
                "create_checkpoint_collection",
                "FAILED",
                {"error": str(e)}
            )
            raise

    def create_operation_log_collection(self) -> bool:
        """
        Create operation_logs collection for operation history tracking

        Returns:
            bool: True if created successfully
        """
        collection_name = "operation_logs"

        try:
            # Check if collection already exists
            collections = self.client.get_collections().collections
            if any(c.name == collection_name for c in collections):
                self._log(
                    "create_operation_log_collection",
                    "EXISTS",
                    {"collection": collection_name, "action": "skipped"}
                )
                return True

            # Create collection with 384-dimensional vectors for semantic log search
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

            self._log(
                "create_operation_log_collection",
                "SUCCESS",
                {
                    "collection": collection_name,
                    "vector_size": 384,
                    "distance_metric": "COSINE"
                }
            )

            # Create initial test log entry
            test_log = PointStruct(
                id=1,
                vector=[0.0] * 384,
                payload={
                    "operation_id": "SETUP_LOG_001",
                    "operation_type": "qdrant_initialization",
                    "phase": "SETUP",
                    "wave": "SYSTEM",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "SUCCESS",
                    "details": {
                        "message": "Operation log collection initialized",
                        "collections_created": ["ontology_checkpoints", "operation_logs"]
                    }
                }
            )

            self.client.upsert(
                collection_name=collection_name,
                points=[test_log]
            )

            self._log(
                "create_test_operation_log",
                "SUCCESS",
                {"operation_id": "SETUP_LOG_001"}
            )

            return True

        except Exception as e:
            self._log(
                "create_operation_log_collection",
                "FAILED",
                {"error": str(e)}
            )
            raise

    def verify_collections(self) -> Dict[str, bool]:
        """
        Verify both collections exist and are accessible

        Returns:
            Dict mapping collection names to existence status
        """
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            checkpoints_exist = "ontology_checkpoints" in collection_names
            logs_exist = "operation_logs" in collection_names

            verification_result = {
                "ontology_checkpoints": checkpoints_exist,
                "operation_logs": logs_exist
            }

            self._log(
                "verify_collections",
                "SUCCESS" if all(verification_result.values()) else "PARTIAL",
                verification_result
            )

            return verification_result

        except Exception as e:
            self._log(
                "verify_collections",
                "FAILED",
                {"error": str(e)}
            )
            raise

    def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a collection

        Args:
            collection_name: Name of collection to inspect

        Returns:
            Dict with collection information
        """
        try:
            info = self.client.get_collection(collection_name=collection_name)

            collection_info = {
                "name": collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status,
                "config": {
                    "vector_size": info.config.params.vectors.size,
                    "distance": info.config.params.vectors.distance.value
                }
            }

            self._log(
                "get_collection_info",
                "SUCCESS",
                collection_info
            )

            return collection_info

        except Exception as e:
            self._log(
                "get_collection_info",
                "FAILED",
                {"collection": collection_name, "error": str(e)}
            )
            raise

    def setup_all(self) -> bool:
        """
        Execute complete Qdrant setup

        Returns:
            bool: True if all collections created successfully
        """
        print("=" * 80)
        print("QDRANT COLLECTIONS SETUP")
        print("=" * 80)
        print()

        try:
            # Create checkpoint collection
            print("Creating ontology_checkpoints collection...")
            self.create_checkpoint_collection()
            print("✅ ontology_checkpoints collection ready")
            print()

            # Create operation log collection
            print("Creating operation_logs collection...")
            self.create_operation_log_collection()
            print("✅ operation_logs collection ready")
            print()

            # Verify collections
            print("Verifying collections...")
            verification = self.verify_collections()

            if all(verification.values()):
                print("✅ All collections verified successfully")
                print()

                # Show collection info
                print("Collection Information:")
                print("-" * 80)
                for collection_name in ["ontology_checkpoints", "operation_logs"]:
                    info = self.get_collection_info(collection_name)
                    print(f"\n{collection_name}:")
                    print(f"  Points: {info['points_count']}")
                    print(f"  Vectors: {info['vectors_count']}")
                    print(f"  Status: {info['status']}")
                    print(f"  Vector Size: {info['config']['vector_size']}")
                    print(f"  Distance: {info['config']['distance']}")

                print()
                print("=" * 80)
                print("SETUP COMPLETE")
                print("=" * 80)
                print()
                print(f"Log file: {self.log_file}")

                return True
            else:
                print("⚠️  Some collections could not be verified:")
                for name, exists in verification.items():
                    status = "✅" if exists else "❌"
                    print(f"  {status} {name}")
                return False

        except Exception as e:
            print(f"\n❌ SETUP FAILED: {e}")
            return False


def main():
    """Main execution function"""

    # Parse command line arguments for custom host/port
    import argparse
    parser = argparse.ArgumentParser(
        description="Set up Qdrant collections for Neo4j ontology checkpoint management"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Qdrant server host (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=6333,
        help="Qdrant server port (default: 6333)"
    )
    parser.add_argument(
        "--api-key",
        default="deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=",
        help="Qdrant API key for authentication"
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Custom log file path (default: ../logs/qdrant_setup.jsonl)"
    )

    args = parser.parse_args()

    # Initialize setup manager
    setup = QdrantSetup(
        host=args.host,
        port=args.port,
        api_key=args.api_key,
        log_file=args.log_file
    )

    # Execute setup
    success = setup.setup_all()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
