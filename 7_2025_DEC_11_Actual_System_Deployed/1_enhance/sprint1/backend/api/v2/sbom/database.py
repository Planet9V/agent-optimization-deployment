"""
Database operations for SBOM APIs
Handles Neo4j graph operations and Qdrant vector storage
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import hashlib
import json


class SBOMDatabase:
    """Database operations for SBOM management"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333
    ):
        self.neo4j_driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self._ensure_collections()

    def _ensure_collections(self):
        """Ensure Qdrant collections exist"""
        collections = self.qdrant_client.get_collections().collections
        collection_names = [c.name for c in collections]

        if "sbom_components" not in collection_names:
            self.qdrant_client.create_collection(
                collection_name="sbom_components",
                vectors_config=VectorParams(size=768, distance=Distance.COSINE)
            )

    def create_sbom(
        self,
        sbom_id: str,
        project_name: str,
        project_version: str,
        format: str,
        customer_id: str,
        components: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create SBOM in Neo4j graph

        Args:
            sbom_id: Unique SBOM identifier
            project_name: Project name
            project_version: Project version
            format: SBOM format (cyclonedx, spdx)
            customer_id: Customer identifier for multi-tenancy
            components: List of component dictionaries

        Returns:
            Dict with creation results including counts
        """
        with self.neo4j_driver.session() as session:
            result = session.execute_write(
                self._create_sbom_tx,
                sbom_id,
                project_name,
                project_version,
                format,
                customer_id,
                components
            )
            return result

    @staticmethod
    def _create_sbom_tx(tx, sbom_id, project_name, project_version, format, customer_id, components):
        """Transaction for creating SBOM and components"""

        # Create SBOM node
        query_sbom = """
        CREATE (s:SBOM {
            sbom_id: $sbom_id,
            project_name: $project_name,
            version: $project_version,
            format: $format,
            customer_id: $customer_id,
            created_at: datetime(),
            super_label: 'Asset',
            tier: 'TIER2'
        })
        RETURN s.sbom_id as sbom_id
        """

        tx.run(
            query_sbom,
            sbom_id=sbom_id,
            project_name=project_name,
            project_version=project_version,
            format=format,
            customer_id=customer_id
        )

        # Create components and relationships
        components_created = 0
        dependencies_created = 0

        for comp in components:
            query_component = """
            MATCH (s:SBOM {sbom_id: $sbom_id, customer_id: $customer_id})
            CREATE (c:Component {
                component_id: $component_id,
                name: $name,
                version: $version,
                purl: $purl,
                cpe: $cpe,
                license: $license,
                supplier: $supplier,
                customer_id: $customer_id,
                super_label: 'Asset',
                tier: 'TIER3'
            })
            CREATE (s)-[:CONTAINS]->(c)
            RETURN c.component_id as component_id
            """

            tx.run(
                query_component,
                sbom_id=sbom_id,
                customer_id=customer_id,
                component_id=comp.get('component_id'),
                name=comp.get('name'),
                version=comp.get('version'),
                purl=comp.get('purl'),
                cpe=comp.get('cpe'),
                license=comp.get('license'),
                supplier=comp.get('supplier')
            )
            components_created += 1

            # Create dependencies
            for dep_id in comp.get('dependencies', []):
                query_dep = """
                MATCH (c1:Component {component_id: $component_id, customer_id: $customer_id})
                MATCH (c2:Component {component_id: $dep_id, customer_id: $customer_id})
                CREATE (c1)-[:DEPENDS_ON]->(c2)
                """
                tx.run(
                    query_dep,
                    component_id=comp.get('component_id'),
                    dep_id=dep_id,
                    customer_id=customer_id
                )
                dependencies_created += 1

        return {
            "sbom_id": sbom_id,
            "components_created": components_created,
            "dependencies_created": dependencies_created
        }

    def get_sbom(self, sbom_id: str, customer_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve SBOM details from Neo4j

        Args:
            sbom_id: SBOM identifier
            customer_id: Customer identifier for multi-tenancy

        Returns:
            Dict with SBOM details or None if not found
        """
        with self.neo4j_driver.session() as session:
            result = session.execute_read(self._get_sbom_tx, sbom_id, customer_id)
            return result

    @staticmethod
    def _get_sbom_tx(tx, sbom_id, customer_id):
        """Transaction for retrieving SBOM"""

        query = """
        MATCH (s:SBOM {sbom_id: $sbom_id, customer_id: $customer_id})
        OPTIONAL MATCH (s)-[:CONTAINS]->(c:Component)
        OPTIONAL MATCH (c)-[:HAS_VULNERABILITY]->(v:CVE)
        WITH s,
             count(DISTINCT c) as components_count,
             count(DISTINCT v) as vulnerabilities_count,
             collect(DISTINCT {
                 component_id: c.component_id,
                 name: c.name,
                 version: c.version,
                 purl: c.purl,
                 cpe: c.cpe,
                 license: c.license,
                 supplier: c.supplier
             }) as components
        RETURN s.sbom_id as sbom_id,
               s.project_name as project_name,
               s.version as project_version,
               s.format as format,
               s.created_at as created_at,
               s.customer_id as customer_id,
               components_count,
               vulnerabilities_count,
               components
        """

        result = tx.run(query, sbom_id=sbom_id, customer_id=customer_id)
        record = result.single()

        if record:
            return dict(record)
        return None

    def get_sbom_summary(self, customer_id: str) -> Dict[str, Any]:
        """
        Get aggregate SBOM statistics

        Args:
            customer_id: Customer identifier for multi-tenancy

        Returns:
            Dict with aggregate statistics
        """
        with self.neo4j_driver.session() as session:
            result = session.execute_read(self._get_summary_tx, customer_id)
            return result

    @staticmethod
    def _get_summary_tx(tx, customer_id):
        """Transaction for aggregate statistics"""

        query = """
        MATCH (s:SBOM {customer_id: $customer_id})
        OPTIONAL MATCH (s)-[:CONTAINS]->(c:Component)
        OPTIONAL MATCH (c)-[:HAS_VULNERABILITY]->(v:CVE)
        WITH count(DISTINCT s) as total_sboms,
             count(DISTINCT c) as total_components,
             count(DISTINCT v) as total_vulnerabilities,
             collect(DISTINCT v.cvss_base_score) as cvss_scores
        RETURN total_sboms,
               total_components,
               total_vulnerabilities,
               size([score IN cvss_scores WHERE score >= 9.0]) as critical_count,
               size([score IN cvss_scores WHERE score >= 7.0 AND score < 9.0]) as high_count,
               size([score IN cvss_scores WHERE score >= 4.0 AND score < 7.0]) as medium_count,
               size([score IN cvss_scores WHERE score < 4.0]) as low_count
        """

        result = tx.run(query, customer_id=customer_id)
        record = result.single()

        if record:
            return dict(record)
        return {
            "total_sboms": 0,
            "total_components": 0,
            "total_vulnerabilities": 0,
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0
        }

    def search_components(
        self,
        query: str,
        customer_id: str,
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Semantic search for components using Qdrant

        Args:
            query: Search query text
            customer_id: Customer identifier for multi-tenancy
            limit: Maximum results to return
            similarity_threshold: Minimum similarity score

        Returns:
            List of matching components with similarity scores
        """
        # Generate query embedding (simplified - in production use actual embedding model)
        query_vector = self._generate_embedding(query)

        # Search in Qdrant
        search_results = self.qdrant_client.search(
            collection_name="sbom_components",
            query_vector=query_vector,
            limit=limit,
            score_threshold=similarity_threshold,
            query_filter={
                "must": [
                    {"key": "customer_id", "match": {"value": customer_id}}
                ]
            }
        )

        # Enrich with Neo4j data
        results = []
        for hit in search_results:
            component_data = hit.payload
            component_data['similarity_score'] = hit.score
            results.append(component_data)

        return results

    def store_component_embedding(
        self,
        component_id: str,
        name: str,
        version: str,
        sbom_id: str,
        project_name: str,
        customer_id: str
    ):
        """Store component embedding in Qdrant for semantic search"""

        # Generate embedding from component metadata
        text = f"{name} {version} {project_name}"
        embedding = self._generate_embedding(text)

        # Store in Qdrant
        point = PointStruct(
            id=hashlib.md5(component_id.encode()).hexdigest()[:16],
            vector=embedding,
            payload={
                "component_id": component_id,
                "name": name,
                "version": version,
                "sbom_id": sbom_id,
                "project_name": project_name,
                "customer_id": customer_id,
                "vulnerabilities_count": 0
            }
        )

        self.qdrant_client.upsert(
            collection_name="sbom_components",
            points=[point]
        )

    @staticmethod
    def _generate_embedding(text: str) -> List[float]:
        """
        Generate embedding vector from text
        In production, use actual embedding model (e.g., sentence-transformers)
        This is a simplified placeholder using hash-based pseudo-embedding
        """
        # Simplified embedding - replace with actual model in production
        import hashlib
        hash_obj = hashlib.sha512(text.encode())
        hash_bytes = hash_obj.digest()

        # Convert to 768-dimensional vector (matching typical BERT dimensions)
        embedding = []
        for i in range(768):
            byte_val = hash_bytes[i % len(hash_bytes)]
            normalized_val = (byte_val / 255.0) * 2 - 1  # Normalize to [-1, 1]
            embedding.append(normalized_val)

        return embedding

    def close(self):
        """Close database connections"""
        self.neo4j_driver.close()
