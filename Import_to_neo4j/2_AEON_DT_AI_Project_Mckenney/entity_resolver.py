#!/usr/bin/env python3
"""
Entity Resolver - Link document entities to knowledge base nodes

Resolves extracted entities (CVE, CWE, CAPEC, etc.) to their corresponding
knowledge base nodes in Neo4j, creating RESOLVES_TO relationships and
direct document-to-entity MENTIONS_* relationships for optimized querying.

Features:
- Links Entity nodes to API-imported knowledge base (CVE/CWE/CAPEC)
- Creates RESOLVES_TO relationships for entity resolution
- Creates direct MENTIONS_* relationships from Document to knowledge base
- Tracks resolution status (resolved/unresolved)
- Prevents duplicate relationships (idempotent)
- Extensible pattern for future entity types
"""

import logging
import re
from typing import Dict, List, Optional, Any, Set
from collections import defaultdict

from neo4j import Driver, Session

logger = logging.getLogger(__name__)


class EntityResolver:
    """
    Resolve document entities to knowledge base nodes

    Resolution Process:
    1. Find Entity nodes linked to document via CONTAINS_ENTITY
    2. Match entities to knowledge base nodes (CVE, CWE, CAPEC)
    3. Create RESOLVES_TO relationship: Entity -> KnowledgeBaseNode
    4. Create MENTIONS_* relationship: Document -> KnowledgeBaseNode
    5. Mark unresolved entities with resolution_status property

    Benefits:
    - Direct document-to-entity queries without traversing CONTAINS_ENTITY
    - Track which entities are resolved vs. unresolved
    - Support for future entity types via extensible pattern
    """

    def __init__(self, driver: Driver):
        """
        Initialize entity resolver

        Args:
            driver: Neo4j driver instance
        """
        self.driver = driver

    def resolve_all_entities(self, doc_id: str) -> Dict[str, int]:
        """
        Resolve all entities for a document

        Args:
            doc_id: Document ID

        Returns:
            Statistics dictionary with resolution counts
        """
        stats = defaultdict(int)

        # Resolve CVE entities
        cve_stats = self._resolve_cve_entities(doc_id)
        stats.update(cve_stats)

        # Resolve CWE entities
        cwe_stats = self._resolve_cwe_entities(doc_id)
        stats.update(cwe_stats)

        # Resolve CAPEC entities
        capec_stats = self._resolve_capec_entities(doc_id)
        stats.update(capec_stats)

        # Create direct document-to-entity links
        self._create_document_links(doc_id)

        return dict(stats)

    def _resolve_cve_entities(self, doc_id: str) -> Dict[str, int]:
        """
        Resolve CVE entities to CVE knowledge base nodes

        Args:
            doc_id: Document ID

        Returns:
            Resolution statistics
        """
        stats = {'cve_resolved': 0, 'cve_not_found': 0}

        with self.driver.session() as session:
            # Find all CVE entities in document
            result = session.run("""
                MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity)
                WHERE e.label = 'CVE'
                RETURN e.id as entity_id, e.text as entity_text
            """, doc_id=doc_id)

            cve_entities = [dict(record) for record in result]

            for entity in cve_entities:
                entity_id = entity['entity_id']
                entity_text = entity['entity_text']

                # Extract CVE ID (e.g., "CVE-2024-1234" -> "CVE-2024-1234")
                cve_id = entity_text.strip()

                # Try to find matching CVE node in knowledge base
                match_result = session.run("""
                    MATCH (cve:CVE)
                    WHERE cve.cve_id = $cve_id OR cve.cveId = $cve_id
                    RETURN cve.id as cve_node_id
                    LIMIT 1
                """, cve_id=cve_id)

                cve_record = match_result.single()

                if cve_record:
                    # CVE found - create RESOLVES_TO relationship
                    cve_node_id = cve_record['cve_node_id']

                    session.run("""
                        MATCH (e:Entity {id: $entity_id})
                        MATCH (cve:CVE {id: $cve_node_id})
                        MERGE (e)-[r:RESOLVES_TO]->(cve)
                        ON CREATE SET r.created_at = datetime()
                        SET e.resolution_status = 'resolved'
                    """, entity_id=entity_id, cve_node_id=cve_node_id)

                    stats['cve_resolved'] += 1
                    logger.debug(f"Resolved CVE entity {entity_text} to knowledge base")
                else:
                    # CVE not found - mark as unresolved
                    session.run("""
                        MATCH (e:Entity {id: $entity_id})
                        SET e.resolution_status = 'unresolved'
                    """, entity_id=entity_id)

                    stats['cve_not_found'] += 1
                    logger.debug(f"CVE entity {entity_text} not found in knowledge base")

        return stats

    def _resolve_cwe_entities(self, doc_id: str) -> Dict[str, int]:
        """
        Resolve CWE entities to CWE knowledge base nodes

        Args:
            doc_id: Document ID

        Returns:
            Resolution statistics
        """
        stats = {'cwe_resolved': 0, 'cwe_not_found': 0}

        with self.driver.session() as session:
            # Find all CWE entities in document
            result = session.run("""
                MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity)
                WHERE e.label = 'CWE'
                RETURN e.id as entity_id, e.text as entity_text
            """, doc_id=doc_id)

            cwe_entities = [dict(record) for record in result]

            for entity in cwe_entities:
                entity_id = entity['entity_id']
                entity_text = entity['entity_text']

                # Extract CWE ID (e.g., "CWE-89" -> "89")
                cwe_match = re.search(r'CWE-(\d+)', entity_text)
                if not cwe_match:
                    stats['cwe_not_found'] += 1
                    continue

                cwe_id = cwe_match.group(1)

                # Try to find matching CWE node in knowledge base
                match_result = session.run("""
                    MATCH (cwe:CWE)
                    WHERE cwe.cwe_id = $cwe_id
                    RETURN cwe.id as cwe_node_id
                    LIMIT 1
                """, cwe_id=cwe_id)

                cwe_record = match_result.single()

                if cwe_record:
                    # CWE found - create RESOLVES_TO relationship
                    cwe_node_id = cwe_record['cwe_node_id']

                    session.run("""
                        MATCH (e:Entity {id: $entity_id})
                        MATCH (cwe:CWE {id: $cwe_node_id})
                        MERGE (e)-[r:RESOLVES_TO]->(cwe)
                        ON CREATE SET r.created_at = datetime()
                        SET e.resolution_status = 'resolved'
                    """, entity_id=entity_id, cwe_node_id=cwe_node_id)

                    stats['cwe_resolved'] += 1
                    logger.debug(f"Resolved CWE entity {entity_text} to knowledge base")
                else:
                    # CWE not found - mark as unresolved
                    session.run("""
                        MATCH (e:Entity {id: $entity_id})
                        SET e.resolution_status = 'unresolved'
                    """, entity_id=entity_id)

                    stats['cwe_not_found'] += 1
                    logger.debug(f"CWE entity {entity_text} not found in knowledge base")

        return stats

    def _resolve_capec_entities(self, doc_id: str) -> Dict[str, int]:
        """
        Resolve CAPEC entities to CAPEC knowledge base nodes

        Args:
            doc_id: Document ID

        Returns:
            Resolution statistics
        """
        stats = {'capec_resolved': 0, 'capec_not_found': 0}

        with self.driver.session() as session:
            # Find all CAPEC entities in document
            result = session.run("""
                MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity)
                WHERE e.label = 'CAPEC'
                RETURN e.id as entity_id, e.text as entity_text
            """, doc_id=doc_id)

            capec_entities = [dict(record) for record in result]

            for entity in capec_entities:
                entity_id = entity['entity_id']
                entity_text = entity['entity_text']

                # Extract CAPEC ID (e.g., "CAPEC-66" -> "CAPEC-66")
                capec_id = entity_text.strip()

                # Try to find matching CAPEC node in knowledge base
                match_result = session.run("""
                    MATCH (capec:CAPEC)
                    WHERE capec.capecId = $capec_id
                    RETURN capec.id as capec_node_id
                    LIMIT 1
                """, capec_id=capec_id)

                capec_record = match_result.single()

                if capec_record:
                    # CAPEC found - create RESOLVES_TO relationship
                    capec_node_id = capec_record['capec_node_id']

                    session.run("""
                        MATCH (e:Entity {id: $entity_id})
                        MATCH (capec:CAPEC {id: $capec_node_id})
                        MERGE (e)-[r:RESOLVES_TO]->(capec)
                        ON CREATE SET r.created_at = datetime()
                        SET e.resolution_status = 'resolved'
                    """, entity_id=entity_id, capec_node_id=capec_node_id)

                    stats['capec_resolved'] += 1
                    logger.debug(f"Resolved CAPEC entity {entity_text} to knowledge base")
                else:
                    # CAPEC not found - mark as unresolved
                    session.run("""
                        MATCH (e:Entity {id: $entity_id})
                        SET e.resolution_status = 'unresolved'
                    """, entity_id=entity_id)

                    stats['capec_not_found'] += 1
                    logger.debug(f"CAPEC entity {entity_text} not found in knowledge base")

        return stats

    def _create_document_links(self, doc_id: str):
        """
        Create direct MENTIONS_* relationships from document to knowledge base nodes

        This optimizes queries by allowing direct Document -> CVE/CWE/CAPEC traversal
        without needing to go through CONTAINS_ENTITY -> RESOLVES_TO

        Args:
            doc_id: Document ID
        """
        with self.driver.session() as session:
            # Create MENTIONS_CVE relationships
            session.run("""
                MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity)-[:RESOLVES_TO]->(cve:CVE)
                WITH d, cve, collect(DISTINCT e) as entities
                MERGE (d)-[r:MENTIONS_CVE]->(cve)
                ON CREATE SET r.created_at = datetime()
                SET r.mention_count = size(entities)
            """, doc_id=doc_id)

            # Create MENTIONS_CWE relationships
            session.run("""
                MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity)-[:RESOLVES_TO]->(cwe:CWE)
                WITH d, cwe, collect(DISTINCT e) as entities
                MERGE (d)-[r:MENTIONS_CWE]->(cwe)
                ON CREATE SET r.created_at = datetime()
                SET r.mention_count = size(entities)
            """, doc_id=doc_id)

            # Create MENTIONS_CAPEC relationships
            session.run("""
                MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity)-[:RESOLVES_TO]->(capec:CAPEC)
                WITH d, capec, collect(DISTINCT e) as entities
                MERGE (d)-[r:MENTIONS_CAPEC]->(capec)
                ON CREATE SET r.created_at = datetime()
                SET r.mention_count = size(entities)
            """, doc_id=doc_id)

    def get_unresolved_entities(self, doc_id: str) -> List[Dict[str, str]]:
        """
        Get list of unresolved entities for a document

        Args:
            doc_id: Document ID

        Returns:
            List of unresolved entities with text and label
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity)
                WHERE e.resolution_status = 'unresolved'
                RETURN e.text as text, e.label as label
                ORDER BY e.label, e.text
            """, doc_id=doc_id)

            return [dict(record) for record in result]

    def get_resolution_stats(self, doc_id: str) -> Dict[str, Any]:
        """
        Get resolution statistics for a document

        Args:
            doc_id: Document ID

        Returns:
            Statistics dictionary with counts by entity type and resolution status
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity)
                WITH e.label as entity_type,
                     e.resolution_status as status,
                     count(e) as count
                RETURN entity_type, status, count
                ORDER BY entity_type, status
            """, doc_id=doc_id)

            stats = defaultdict(lambda: defaultdict(int))
            for record in result:
                entity_type = record['entity_type']
                status = record['status'] or 'unprocessed'
                count = record['count']
                stats[entity_type][status] = count

            return dict(stats)


def resolve_document_entities(driver: Driver, doc_id: str) -> Dict[str, int]:
    """
    Convenience function to resolve all entities for a document

    Args:
        driver: Neo4j driver instance
        doc_id: Document ID

    Returns:
        Resolution statistics
    """
    resolver = EntityResolver(driver)
    return resolver.resolve_all_entities(doc_id)
