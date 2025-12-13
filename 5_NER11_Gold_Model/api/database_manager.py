"""
Centralized Database Connection Manager
========================================

Singleton pattern for Neo4j and Qdrant connections to prevent connection sprawl.
Provides connection pooling and timeout protection.

Version: 1.0.0
"""

import os
from typing import Optional
from neo4j import GraphDatabase, Driver
from qdrant_client import QdrantClient
import logging

logger = logging.getLogger(__name__)


class DatabaseConnectionManager:
    """Singleton manager for database connections"""

    _instance: Optional['DatabaseConnectionManager'] = None
    _neo4j_driver: Optional[Driver] = None
    _qdrant_client: Optional[QdrantClient] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_neo4j_driver(self) -> Driver:
        """Get or create Neo4j driver singleton"""
        if self._neo4j_driver is None:
            neo4j_uri = os.getenv("NEO4J_URI", "bolt://openspg-neo4j:7687")
            neo4j_user = os.getenv("NEO4J_USER", "neo4j")
            neo4j_password = os.getenv("NEO4J_PASSWORD", "neo4j@openspg")

            logger.info(f"Creating Neo4j driver with connection pooling...")
            self._neo4j_driver = GraphDatabase.driver(
                neo4j_uri,
                auth=(neo4j_user, neo4j_password),
                max_connection_pool_size=50,  # Increased from default 100
                connection_timeout=10.0,  # 10 second connection timeout
                max_transaction_retry_time=10.0,  # Retry transactions for 10s
                connection_acquisition_timeout=10.0,  # Wait max 10s for connection
                keep_alive=True
            )

            # Verify connection
            try:
                with self._neo4j_driver.session() as session:
                    session.run("RETURN 1")
                logger.info("✅ Neo4j driver initialized with connection pooling")
            except Exception as e:
                logger.error(f"❌ Failed to verify Neo4j connection: {e}")
                raise

        return self._neo4j_driver

    def get_qdrant_client(self) -> QdrantClient:
        """Get or create Qdrant client singleton"""
        if self._qdrant_client is None:
            qdrant_host = os.getenv("QDRANT_HOST", "openspg-qdrant")
            qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
            qdrant_url = f"http://{qdrant_host}:{qdrant_port}"

            logger.info(f"Creating Qdrant client connection to {qdrant_url}...")
            self._qdrant_client = QdrantClient(
                url=qdrant_url,
                timeout=10.0  # 10 second timeout
            )

            # Verify connection
            try:
                collections = self._qdrant_client.get_collections()
                logger.info(f"✅ Qdrant client initialized ({len(collections.collections)} collections)")
            except Exception as e:
                logger.error(f"❌ Failed to verify Qdrant connection: {e}")
                raise

        return self._qdrant_client

    def close_all(self):
        """Close all database connections"""
        if self._neo4j_driver:
            logger.info("Closing Neo4j driver...")
            self._neo4j_driver.close()
            self._neo4j_driver = None

        if self._qdrant_client:
            logger.info("Closing Qdrant client...")
            # Qdrant client doesn't have explicit close method
            self._qdrant_client = None

        logger.info("✅ All database connections closed")


# Global singleton instance
db_manager = DatabaseConnectionManager()


# Convenience functions for importing in API modules
def get_neo4j_driver() -> Driver:
    """Get shared Neo4j driver with connection pooling"""
    return db_manager.get_neo4j_driver()


def get_qdrant_client() -> QdrantClient:
    """Get shared Qdrant client"""
    return db_manager.get_qdrant_client()


def close_database_connections():
    """Close all database connections"""
    db_manager.close_all()
