"""
Neo4j Database Connection Management
File: config/database.py
Created: 2025-11-08
Purpose: Neo4j connection pooling and session management
"""

from typing import Optional
from contextlib import asynccontextmanager
from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncSession
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class Neo4jConnection:
    """Neo4j database connection manager with connection pooling"""

    def __init__(self):
        self._driver: Optional[AsyncDriver] = None
        self._initialized = False

    async def initialize(self):
        """Initialize Neo4j driver with connection pool"""
        if self._initialized:
            return

        try:
            self._driver = AsyncGraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password),
                max_connection_pool_size=settings.neo4j_max_connection_pool_size,
                connection_acquisition_timeout=settings.neo4j_connection_acquisition_timeout
            )

            # Verify connectivity
            await self._driver.verify_connectivity()
            self._initialized = True
            logger.info(f"Neo4j connection initialized: {settings.neo4j_uri}")

        except Exception as e:
            logger.error(f"Failed to initialize Neo4j connection: {e}")
            raise

    async def close(self):
        """Close Neo4j driver and connection pool"""
        if self._driver:
            await self._driver.close()
            self._initialized = False
            logger.info("Neo4j connection closed")

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        """Get Neo4j session from connection pool"""
        if not self._initialized:
            await self.initialize()

        async with self._driver.session(database=settings.neo4j_database) as session:
            try:
                yield session
            except Exception as e:
                logger.error(f"Session error: {e}")
                raise

    async def execute_read(self, query: str, parameters: dict = None):
        """Execute read query"""
        async with self.get_session() as session:
            result = await session.run(query, parameters or {})
            records = await result.data()
            return records

    async def execute_write(self, query: str, parameters: dict = None):
        """Execute write query"""
        async with self.get_session() as session:
            result = await session.run(query, parameters or {})
            records = await result.data()
            return records


# Global Neo4j connection instance
neo4j_connection = Neo4jConnection()


async def get_neo4j() -> Neo4jConnection:
    """Dependency injection for Neo4j connection"""
    if not neo4j_connection._initialized:
        await neo4j_connection.initialize()
    return neo4j_connection
