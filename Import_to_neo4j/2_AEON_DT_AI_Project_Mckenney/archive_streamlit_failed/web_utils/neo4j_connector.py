"""
Neo4j Database Connector for AEON Web Interface
Provides connection pooling and query utilities
"""

import os
from typing import Dict, List, Any, Optional
from neo4j import GraphDatabase, Driver
import logging

logger = logging.getLogger(__name__)


class Neo4jConnector:
    """Neo4j database connection manager"""

    def __init__(
        self,
        uri: str = "bolt://localhost:7687",
        user: str = "neo4j",
        password: Optional[str] = None
    ):
        """
        Initialize Neo4j connector

        Args:
            uri: Neo4j connection URI
            user: Neo4j username
            password: Neo4j password (reads from NEO4J_PASSWORD env var if None)
        """
        self.uri = uri
        self.user = user
        self.password = password or os.getenv("NEO4J_PASSWORD", "neo4j@openspg")
        self._driver: Optional[Driver] = None

    @property
    def driver(self) -> Driver:
        """Get or create Neo4j driver"""
        if self._driver is None:
            try:
                self._driver = GraphDatabase.driver(
                    self.uri,
                    auth=(self.user, self.password)
                )
                logger.info(f"Connected to Neo4j at {self.uri}")
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {e}")
                raise
        return self._driver

    def close(self):
        """Close Neo4j connection"""
        if self._driver:
            self._driver.close()
            self._driver = None
            logger.info("Neo4j connection closed")

    def test_connection(self) -> bool:
        """Test if Neo4j connection is working"""
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 AS test")
                return result.single()["test"] == 1
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

    # ========== Document Queries ==========

    def get_documents(
        self,
        search: str = "",
        sector: Optional[str] = None,
        subsector: Optional[str] = None,
        doc_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get documents with optional filtering

        Args:
            search: Search term for title/content
            sector: Filter by sector
            subsector: Filter by subsector
            doc_type: Filter by document type
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return

        Returns:
            List of document dictionaries
        """
        with self.driver.session() as session:
            query = """
            MATCH (d:Document)
            WHERE ($search = '' OR d.title CONTAINS $search OR d.content CONTAINS $search)
              AND ($sector IS NULL OR d.sector = $sector)
              AND ($subsector IS NULL OR d.subsector = $subsector)
              AND ($doc_type IS NULL OR d.document_type = $doc_type)
            RETURN d
            ORDER BY d.processed_date DESC
            SKIP $skip LIMIT $limit
            """
            result = session.run(
                query,
                search=search,
                sector=sector,
                subsector=subsector,
                doc_type=doc_type,
                skip=skip,
                limit=limit
            )
            return [dict(record["d"]) for record in result]

    def get_document_count(
        self,
        search: str = "",
        sector: Optional[str] = None,
        subsector: Optional[str] = None,
        doc_type: Optional[str] = None
    ) -> int:
        """Get total count of documents matching filters"""
        with self.driver.session() as session:
            query = """
            MATCH (d:Document)
            WHERE ($search = '' OR d.title CONTAINS $search OR d.content CONTAINS $search)
              AND ($sector IS NULL OR d.sector = $sector)
              AND ($subsector IS NULL OR d.subsector = $subsector)
              AND ($doc_type IS NULL OR d.document_type = $doc_type)
            RETURN count(d) AS total
            """
            result = session.run(
                query,
                search=search,
                sector=sector,
                subsector=subsector,
                doc_type=doc_type
            )
            return result.single()["total"]

    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get single document by ID"""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (d:Document {id: $id}) RETURN d",
                id=doc_id
            )
            record = result.single()
            return dict(record["d"]) if record else None

    def get_document_entities(self, doc_id: str) -> List[Dict[str, Any]]:
        """Get all entities for a document"""
        with self.driver.session() as session:
            query = """
            MATCH (d:Document {id: $id})-[r:CONTAINS_ENTITY]->(e:Entity)
            RETURN e.text AS text,
                   e.label AS label,
                   e.confidence AS confidence,
                   r.count AS mention_count,
                   r.prominence AS prominence
            ORDER BY r.prominence DESC
            """
            result = session.run(query, id=doc_id)
            return [dict(record) for record in result]

    # ========== Entity Queries ==========

    def get_entities(
        self,
        search: str = "",
        label: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get entities with optional filtering"""
        with self.driver.session() as session:
            query = """
            MATCH (e:Entity)
            WHERE ($search = '' OR e.text CONTAINS $search)
              AND ($label IS NULL OR e.label = $label)
            RETURN e.text AS text,
                   e.label AS label,
                   e.confidence AS confidence,
                   count{(e)<-[:CONTAINS_ENTITY]-()} AS document_count
            ORDER BY document_count DESC
            SKIP $skip LIMIT $limit
            """
            result = session.run(
                query,
                search=search,
                label=label,
                skip=skip,
                limit=limit
            )
            return [dict(record) for record in result]

    def get_entity_types(self) -> List[Dict[str, Any]]:
        """Get all entity types with counts"""
        with self.driver.session() as session:
            query = """
            MATCH (e:Entity)
            RETURN e.label AS label, count(*) AS count
            ORDER BY count DESC
            """
            result = session.run(query)
            return [dict(record) for record in result]

    def get_entity_documents(
        self,
        entity_text: str,
        entity_label: str
    ) -> List[Dict[str, Any]]:
        """Get all documents containing a specific entity"""
        with self.driver.session() as session:
            query = """
            MATCH (e:Entity {text: $text, label: $label})<-[:CONTAINS_ENTITY]-(d:Document)
            RETURN d.id AS id,
                   d.title AS title,
                   d.sector AS sector,
                   d.processed_date AS processed_date
            ORDER BY d.processed_date DESC
            """
            result = session.run(query, text=entity_text, label=entity_label)
            return [dict(record) for record in result]

    # ========== Statistics Queries ==========

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        with self.driver.session() as session:
            # Document count
            doc_count = session.run("MATCH (d:Document) RETURN count(d) AS count")
            total_docs = doc_count.single()["count"]

            # Entity count
            entity_count = session.run("MATCH (e:Entity) RETURN count(e) AS count")
            total_entities = entity_count.single()["count"]

            # Relationship count
            rel_count = session.run("MATCH ()-[r:CONTAINS_ENTITY]->() RETURN count(r) AS count")
            total_relationships = rel_count.single()["count"]

            # Sector distribution
            sector_dist = session.run("""
                MATCH (d:Document)
                RETURN d.sector AS sector, count(*) AS count
                ORDER BY count DESC
            """)
            sectors = [dict(record) for record in sector_dist]

            # Entity type distribution
            entity_types = session.run("""
                MATCH (e:Entity)
                RETURN e.label AS type, count(*) AS count
                ORDER BY count DESC
            """)
            entity_type_dist = [dict(record) for record in entity_types]

            return {
                "total_documents": total_docs,
                "total_entities": total_entities,
                "total_relationships": total_relationships,
                "sector_distribution": sectors,
                "entity_type_distribution": entity_type_dist
            }

    def get_recent_documents(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recently processed documents"""
        with self.driver.session() as session:
            query = """
            MATCH (d:Document)
            RETURN d.id AS id,
                   d.title AS title,
                   d.sector AS sector,
                   d.document_type AS doc_type,
                   d.processed_date AS processed_date,
                   d.entity_count AS entity_count
            ORDER BY d.processed_date DESC
            LIMIT $limit
            """
            result = session.run(query, limit=limit)
            return [dict(record) for record in result]

    # ========== Search Queries ==========

    def search_all(self, query: str, limit: int = 20) -> Dict[str, List]:
        """Search across documents and entities"""
        with self.driver.session() as session:
            # Search documents
            doc_results = session.run("""
                MATCH (d:Document)
                WHERE d.title CONTAINS $query OR d.content CONTAINS $query
                RETURN d.id AS id, d.title AS title, d.sector AS sector
                LIMIT $limit
            """, query=query, limit=limit)
            documents = [dict(r) for r in doc_results]

            # Search entities
            entity_results = session.run("""
                MATCH (e:Entity)
                WHERE e.text CONTAINS $query
                RETURN e.text AS text, e.label AS label,
                       count{(e)<-[:CONTAINS_ENTITY]-()} AS doc_count
                ORDER BY doc_count DESC
                LIMIT $limit
            """, query=query, limit=limit)
            entities = [dict(r) for r in entity_results]

            return {
                "documents": documents,
                "entities": entities
            }


# Global connector instance
_connector: Optional[Neo4jConnector] = None


def get_connector() -> Neo4jConnector:
    """Get global Neo4j connector instance"""
    global _connector
    if _connector is None:
        _connector = Neo4jConnector()
    return _connector


def close_connector():
    """Close global connector"""
    global _connector
    if _connector:
        _connector.close()
        _connector = None
