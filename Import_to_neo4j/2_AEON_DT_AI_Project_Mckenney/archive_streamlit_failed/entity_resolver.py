#!/usr/bin/env python3
"""
Entity Resolution Module
Links document-extracted entities to existing knowledge graph nodes (CVE/CWE/CAPEC)
"""
import logging
from typing import Dict, List, Optional, Tuple
from neo4j import GraphDatabase, Session

logger = logging.getLogger(__name__)


class EntityResolver:
    """
    Resolves extracted entities to existing knowledge graph nodes.
    Creates RESOLVES_TO relationships between Entity nodes and API-imported nodes.
    """

    def __init__(self, driver):
        """
        Initialize the entity resolver.

        Args:
            driver: Neo4j driver instance
        """
        self.driver = driver

    def resolve_all_entities(self, doc_id: str) -> Dict[str, int]:
        """
        Resolve all entity types for a given document.
        Marks unresolved entities for forward compatibility.

        Args:
            doc_id: Document UUID

        Returns:
            Dict with counts of resolved entities by type
        """
        stats = {
            'cve_resolved': 0,
            'cwe_resolved': 0,
            'capec_resolved': 0,
            'cve_not_found': 0,
            'cwe_not_found': 0,
            'capec_not_found': 0
        }

        # Resolve each entity type (document links created automatically)
        cve_resolved, cve_not_found = self.resolve_cve_entities(doc_id)
        stats['cve_resolved'] = cve_resolved
        stats['cve_not_found'] = cve_not_found

        cwe_resolved, cwe_not_found = self.resolve_cwe_entities(doc_id)
        stats['cwe_resolved'] = cwe_resolved
        stats['cwe_not_found'] = cwe_not_found

        capec_resolved, capec_not_found = self.resolve_capec_entities(doc_id)
        stats['capec_resolved'] = capec_resolved
        stats['capec_not_found'] = capec_not_found

        # Log summary statistics
        total_resolved = cve_resolved + cwe_resolved + capec_resolved
        total_unresolved = cve_not_found + cwe_not_found + capec_not_found
        total_entities = total_resolved + total_unresolved

        logger.info(
            f"Entity resolution for doc {doc_id}: "
            f"{total_resolved}/{total_entities} resolved ({total_resolved/total_entities*100:.1f}%), "
            f"{total_unresolved} marked as unresolved"
        )

        return stats

    def resolve_cve_entities(self, doc_id: str) -> Tuple[int, int]:
        """
        Link Entity[CVE] nodes to API CVE nodes.
        Marks unresolved entities with resolution_status for forward compatibility.

        Args:
            doc_id: Document UUID

        Returns:
            Tuple of (resolved_count, not_found_count)
        """
        with self.driver.session() as session:
            result = session.run("""
                // Find all CVE entities in document
                MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity {label: 'CVE'})

                // Try to match with API CVE node
                OPTIONAL MATCH (c:CVE)
                WHERE c.cve_id = e.text
                   OR c.cveId = e.text
                   OR c.id = 'cve-' + e.text

                // Create RESOLVES_TO relationship and mark as resolved if CVE found
                FOREACH (ignored IN CASE WHEN c IS NOT NULL THEN [1] ELSE [] END |
                    MERGE (e)-[r:RESOLVES_TO]->(c)
                    ON CREATE SET r.created_at = datetime()
                    SET e.resolution_status = 'resolved',
                        e.resolved_at = datetime()
                )

                // Mark as unresolved if CVE not found (forward compatibility)
                FOREACH (ignored IN CASE WHEN c IS NULL THEN [1] ELSE [] END |
                    SET e.resolution_status = 'unresolved',
                        e.attempted_resolution_date = datetime()
                )

                // Create direct document link if CVE found
                WITH d, e, c
                WHERE c IS NOT NULL
                MERGE (d)-[m:MENTIONS_CVE]->(c)
                ON CREATE SET m.created_at = datetime()

                // Return statistics
                RETURN
                    count(DISTINCT e) as total_entities,
                    count(DISTINCT c) as resolved_count,
                    collect(CASE WHEN c IS NULL THEN e.text ELSE NULL END) as not_found
            """, doc_id=doc_id)

            record = result.single()
            if record:
                resolved = record['resolved_count']
                not_found_list = [x for x in record['not_found'] if x is not None]
                not_found = len(not_found_list)

                # Enhanced logging with resolution statistics
                total = record['total_entities']
                logger.info(
                    f"CVE resolution for doc {doc_id}: "
                    f"{resolved}/{total} resolved ({resolved/total*100:.1f}%), "
                    f"{not_found} unresolved and marked for future resolution"
                )

                if not_found > 0:
                    logger.warning(f"CVEs not found in API database: {not_found_list[:5]}")

                return resolved, not_found

            return 0, 0

    def resolve_cwe_entities(self, doc_id: str) -> Tuple[int, int]:
        """
        Link Entity[CWE] nodes to API CWE nodes.
        Marks unresolved entities with resolution_status for forward compatibility.

        Args:
            doc_id: Document UUID

        Returns:
            Tuple of (resolved_count, not_found_count)
        """
        with self.driver.session() as session:
            result = session.run("""
                // Find all CWE entities in document
                MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity {label: 'CWE'})

                // Extract numeric ID from text (e.g., "CWE-89" -> "89")
                WITH d, e,
                     CASE
                         WHEN e.text =~ 'CWE-.*' THEN substring(e.text, 4)
                         ELSE e.text
                     END as numeric_id

                // Try to match with API CWE node
                OPTIONAL MATCH (w:CWE)
                WHERE w.cwe_id = numeric_id
                   OR w.id = 'cwe-' + numeric_id
                   OR w.id = e.text

                // Create RESOLVES_TO relationship and mark as resolved if CWE found
                FOREACH (ignored IN CASE WHEN w IS NOT NULL THEN [1] ELSE [] END |
                    MERGE (e)-[r:RESOLVES_TO]->(w)
                    ON CREATE SET r.created_at = datetime()
                    SET e.resolution_status = 'resolved',
                        e.resolved_at = datetime()
                )

                // Mark as unresolved if CWE not found (forward compatibility)
                FOREACH (ignored IN CASE WHEN w IS NULL THEN [1] ELSE [] END |
                    SET e.resolution_status = 'unresolved',
                        e.attempted_resolution_date = datetime()
                )

                // Create direct document link if CWE found
                WITH d, e, w
                WHERE w IS NOT NULL
                MERGE (d)-[m:MENTIONS_CWE]->(w)
                ON CREATE SET m.created_at = datetime()

                // Return statistics
                RETURN
                    count(DISTINCT e) as total_entities,
                    count(DISTINCT w) as resolved_count,
                    collect(CASE WHEN w IS NULL THEN e.text ELSE NULL END) as not_found
            """, doc_id=doc_id)

            record = result.single()
            if record:
                resolved = record['resolved_count']
                not_found_list = [x for x in record['not_found'] if x is not None]
                not_found = len(not_found_list)

                # Enhanced logging with resolution statistics
                total = record['total_entities']
                if total > 0:
                    logger.info(
                        f"CWE resolution for doc {doc_id}: "
                        f"{resolved}/{total} resolved ({resolved/total*100:.1f}%), "
                        f"{not_found} unresolved and marked for future resolution"
                    )

                if not_found > 0:
                    logger.warning(f"CWEs not found in API database: {not_found_list[:5]}")

                return resolved, not_found

            return 0, 0

    def resolve_capec_entities(self, doc_id: str) -> Tuple[int, int]:
        """
        Link Entity[CAPEC] nodes to API CAPEC nodes.
        Marks unresolved entities with resolution_status for forward compatibility.

        Args:
            doc_id: Document UUID

        Returns:
            Tuple of (resolved_count, not_found_count)
        """
        with self.driver.session() as session:
            result = session.run("""
                // Find all CAPEC entities in document
                MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity {label: 'CAPEC'})

                // Extract numeric ID from text (e.g., "CAPEC-66" -> "66")
                WITH d, e,
                     CASE
                         WHEN e.text =~ 'CAPEC-.*' THEN substring(e.text, 6)
                         ELSE e.text
                     END as numeric_id

                // Try to match with API CAPEC node
                OPTIONAL MATCH (cap:CAPEC)
                WHERE cap.capecId = 'CAPEC-' + numeric_id
                   OR cap.id = e.text
                   OR cap.id = 'capec-' + numeric_id

                // Create RESOLVES_TO relationship and mark as resolved if CAPEC found
                FOREACH (ignored IN CASE WHEN cap IS NOT NULL THEN [1] ELSE [] END |
                    MERGE (e)-[r:RESOLVES_TO]->(cap)
                    ON CREATE SET r.created_at = datetime()
                    SET e.resolution_status = 'resolved',
                        e.resolved_at = datetime()
                )

                // Mark as unresolved if CAPEC not found (forward compatibility)
                FOREACH (ignored IN CASE WHEN cap IS NULL THEN [1] ELSE [] END |
                    SET e.resolution_status = 'unresolved',
                        e.attempted_resolution_date = datetime()
                )

                // Create direct document link if CAPEC found
                WITH d, e, cap
                WHERE cap IS NOT NULL
                MERGE (d)-[m:MENTIONS_CAPEC]->(cap)
                ON CREATE SET m.created_at = datetime()

                // Return statistics
                RETURN
                    count(DISTINCT e) as total_entities,
                    count(DISTINCT cap) as resolved_count,
                    collect(CASE WHEN cap IS NULL THEN e.text ELSE NULL END) as not_found
            """, doc_id=doc_id)

            record = result.single()
            if record:
                resolved = record['resolved_count']
                not_found_list = [x for x in record['not_found'] if x is not None]
                not_found = len(not_found_list)

                # Enhanced logging with resolution statistics
                total = record['total_entities']
                if total > 0:
                    logger.info(
                        f"CAPEC resolution for doc {doc_id}: "
                        f"{resolved}/{total} resolved ({resolved/total*100:.1f}%), "
                        f"{not_found} unresolved and marked for future resolution"
                    )

                if not_found > 0:
                    logger.warning(f"CAPECs not found in API database: {not_found_list[:5]}")

                return resolved, not_found

            return 0, 0

    def get_unresolved_entities(
        self,
        entity_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, any]]:
        """
        Query entities that could not be resolved to API nodes.
        Useful for identifying CVEs/CWEs/CAPECs that need to be added to the API database.

        Args:
            entity_type: Filter by entity type ('CVE', 'CWE', 'CAPEC'), or None for all
            limit: Maximum number of results to return

        Returns:
            List of unresolved entities with their details
        """
        with self.driver.session() as session:
            query = """
                MATCH (d:Document)-[:CONTAINS_ENTITY]->(e:Entity)
                WHERE e.resolution_status = 'unresolved'
            """

            if entity_type:
                query += " AND e.label = $entity_type"

            query += """
                RETURN
                    e.text as entity_text,
                    e.label as entity_type,
                    e.attempted_resolution_date as attempted_date,
                    count(DISTINCT d) as document_count,
                    collect(DISTINCT d.id)[..5] as sample_documents
                ORDER BY document_count DESC
                LIMIT $limit
            """

            result = session.run(query, entity_type=entity_type, limit=limit)

            unresolved = []
            for record in result:
                unresolved.append({
                    'entity_text': record['entity_text'],
                    'entity_type': record['entity_type'],
                    'attempted_date': record['attempted_date'],
                    'document_count': record['document_count'],
                    'sample_documents': record['sample_documents']
                })

            if unresolved:
                logger.info(
                    f"Found {len(unresolved)} unresolved entities" +
                    (f" of type {entity_type}" if entity_type else "")
                )

            return unresolved

    def get_resolution_statistics(self) -> Dict[str, any]:
        """
        Get overall resolution statistics across all entities.

        Returns:
            Dict with resolution statistics by entity type
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e:Entity)
                WHERE e.label IN ['CVE', 'CWE', 'CAPEC']
                RETURN
                    e.label as entity_type,
                    count(CASE WHEN e.resolution_status = 'resolved' THEN 1 END) as resolved,
                    count(CASE WHEN e.resolution_status = 'unresolved' THEN 1 END) as unresolved,
                    count(CASE WHEN e.resolution_status IS NULL THEN 1 END) as not_attempted,
                    count(e) as total
                ORDER BY entity_type
            """)

            stats = {}
            for record in result:
                entity_type = record['entity_type']
                total = record['total']
                resolved = record['resolved']
                unresolved = record['unresolved']
                not_attempted = record['not_attempted']

                stats[entity_type] = {
                    'total': total,
                    'resolved': resolved,
                    'unresolved': unresolved,
                    'not_attempted': not_attempted,
                    'resolution_rate': (resolved / total * 100) if total > 0 else 0
                }

            logger.info(f"Overall resolution statistics: {stats}")
            return stats

    def enrich_existing_documents(self, batch_size: int = 50) -> Dict[str, int]:
        """
        Batch enrich all existing documents that don't have entity resolution.

        Args:
            batch_size: Number of documents to process per batch

        Returns:
            Dict with statistics
        """
        logger.info("Starting batch entity resolution for existing documents...")

        stats = {
            'documents_processed': 0,
            'cve_resolved': 0,
            'cwe_resolved': 0,
            'capec_resolved': 0
        }

        with self.driver.session() as session:
            # Get all documents that have entities but no RESOLVES_TO relationships
            result = session.run("""
                MATCH (d:Document)-[:CONTAINS_ENTITY]->(e:Entity)
                WHERE e.label IN ['CVE', 'CWE', 'CAPEC']
                  AND NOT (e)-[:RESOLVES_TO]->()
                RETURN DISTINCT d.id as doc_id
                LIMIT $batch_size
            """, batch_size=batch_size)

            doc_ids = [record['doc_id'] for record in result]

        if not doc_ids:
            logger.info("No documents need entity resolution")
            return stats

        logger.info(f"Found {len(doc_ids)} documents needing entity resolution")

        for doc_id in doc_ids:
            try:
                doc_stats = self.resolve_all_entities(doc_id)
                stats['documents_processed'] += 1
                stats['cve_resolved'] += doc_stats['cve_resolved']
                stats['cwe_resolved'] += doc_stats['cwe_resolved']
                stats['capec_resolved'] += doc_stats['capec_resolved']

                if stats['documents_processed'] % 10 == 0:
                    logger.info(f"Processed {stats['documents_processed']}/{len(doc_ids)} documents")

            except Exception as e:
                logger.error(f"Error resolving entities for document {doc_id}: {e}")
                continue

        logger.info(
            f"Batch enrichment complete: {stats['documents_processed']} documents, "
            f"{stats['cve_resolved']} CVEs, {stats['cwe_resolved']} CWEs, "
            f"{stats['capec_resolved']} CAPECs resolved"
        )

        return stats
