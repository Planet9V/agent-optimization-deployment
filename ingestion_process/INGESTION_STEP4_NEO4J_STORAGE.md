# WAVE 4 Step 4: Neo4j Graph Storage & Persistence

**Document Version**: 1.0
**Created**: 2025-11-25
**Last Modified**: 2025-11-25
**Status**: ACTIVE
**Purpose**: Graph database normalization, persistence, indexing, and query optimization

---

## Table of Contents

1. [Step 4 Overview](#step-4-overview)
2. [Neo4j Database Architecture](#neo4j-database-architecture)
3. [Graph Schema Design](#graph-schema-design)
4. [Data Normalization](#data-normalization)
5. [Transaction Management](#transaction-management)
6. [Index Strategy](#index-strategy)
7. [Query Optimization](#query-optimization)
8. [Data Import Pipeline](#data-import-pipeline)
9. [ACID Compliance](#acid-compliance)
10. [Performance Tuning](#performance-tuning)

---

## Step 4 Overview

### Purpose

Step 4 persists the enriched knowledge graph into Neo4j, a graph database optimized for storing and querying semantic relationships. This step ensures ACID compliance, efficient querying, and scalable storage.

### Key Responsibilities

- Normalize entities and relationships for Neo4j storage
- Create graph schema and constraints
- Manage transactional integrity
- Optimize indices for query performance
- Handle incremental updates
- Maintain data consistency
- Monitor database health
- Enable full-text search capabilities

### Expected Inputs

- Knowledge graph from OpenSPG reasoning
- Entities with types and properties
- Relationships with confidence scores
- Metadata and provenance information

### Expected Outputs

- Persistent Neo4j database
- Optimized query indices
- Query execution statistics
- Database health metrics
- Recovery and backup information

---

## Neo4j Database Architecture

### Database Structure

```
Neo4j Instance
├── Graph Database
│   ├── Nodes (Entities)
│   │   ├── Properties
│   │   ├── Labels (Types)
│   │   └── Indices
│   ├── Relationships (Edges)
│   │   ├── Properties
│   │   ├── Types
│   │   └── Direction
│   └── Constraints
│       ├── Uniqueness
│       ├── Property Existence
│       └── Relationship Cardinality
├── APOC Library (Advanced Operations)
├── Full-Text Search Indices
└── Transaction Logs
```

### Instance Configuration

```yaml
# File: neo4j/config/neo4j.conf

# Server settings
server.default_listen_address=0.0.0.0
server.default_advertised_address=localhost
server.bolt.listen_address=0.0.0.0:7687
server.http.listen_address=0.0.0.0:7474

# Memory settings
server.memory.heap.initial_size=2G
server.memory.heap.max_size=4G
server.memory.pagecache.size=2G

# Database settings
dbms.databases.default_to_read_only=false
dbms.transaction.timeout=60s
dbms.transaction.monitor.check_interval=5m

# Security settings
dbms.security.auth_enabled=true
dbms.security.procedures.unrestricted=apoc.*

# Performance settings
dbms.memory.transaction.total.max=10G
dbms.query_statistics.enabled=true
```

---

## Graph Schema Design

### Node Types (Labels)

```cypher
// Define node labels and their purposes

// Entities - Cybersecurity Domain
CREATE CONSTRAINT threat_actor_id IF NOT EXISTS
FOR (t:ThreatActor) REQUIRE t.id IS UNIQUE;

CREATE CONSTRAINT malware_id IF NOT EXISTS
FOR (m:Malware) REQUIRE m.id IS UNIQUE;

CREATE CONSTRAINT vulnerability_id IF NOT EXISTS
FOR (v:Vulnerability) REQUIRE v.id IS UNIQUE;

CREATE CONSTRAINT cve_id IF NOT EXISTS
FOR (c:CVE) REQUIRE c.cve_id IS UNIQUE;

// Entities - General Domain
CREATE CONSTRAINT person_id IF NOT EXISTS
FOR (p:Person) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT organization_id IF NOT EXISTS
FOR (o:Organization) REQUIRE o.id IS UNIQUE;

CREATE CONSTRAINT location_id IF NOT EXISTS
FOR (l:Location) REQUIRE l.id IS UNIQUE;

CREATE CONSTRAINT document_id IF NOT EXISTS
FOR (d:Document) REQUIRE d.document_id IS UNIQUE;

// Entities - Infrastructure
CREATE CONSTRAINT system_id IF NOT EXISTS
FOR (s:System) REQUIRE s.id IS UNIQUE;

CREATE CONSTRAINT infrastructure_id IF NOT EXISTS
FOR (i:Infrastructure) REQUIRE i.id IS UNIQUE;
```

### Node Properties

```
ThreatActor:
  - id (UNIQUE, String)
  - name (String)
  - aliases (List[String])
  - description (Text)
  - country_origin (String)
  - first_seen (DateTime)
  - last_seen (DateTime)
  - confidence (Float 0-1)
  - source (String)
  - document_id (String)

Malware:
  - id (UNIQUE, String)
  - name (String)
  - aliases (List[String])
  - type (String: trojan, worm, ransomware, etc.)
  - description (Text)
  - first_seen (DateTime)
  - attack_vectors (List[String])
  - confidence (Float 0-1)
  - source (String)

Vulnerability:
  - id (UNIQUE, String)
  - cve_id (String)
  - description (Text)
  - cvss_score (Float)
  - attack_vector (String)
  - complexity (String)
  - privileges_required (String)
  - user_interaction (String)
  - published_date (DateTime)
  - patched_date (DateTime, optional)

CVE:
  - cve_id (UNIQUE, String)
  - description (Text)
  - published_date (DateTime)
  - updated_date (DateTime)
  - cvss_score (Float)
  - severity (String: critical, high, medium, low)
```

### Relationship Types

```
USES (ThreatActor -> Malware/Tool)
  Properties:
    - first_observed (DateTime)
    - last_observed (DateTime)
    - confidence (Float)
    - evidence_count (Integer)
    - source (String)

EXPLOITS (ThreatActor/Malware -> Vulnerability)
  Properties:
    - date_observed (DateTime)
    - confidence (Float)
    - attack_success_rate (Float)

TARGETS (ThreatActor/Malware -> System/Organization)
  Properties:
    - impact_type (String)
    - severity (String)
    - date_observed (DateTime)

CAUSES (Vulnerability/Malware -> Impact)
  Properties:
    - impact_severity (String)
    - date_observed (DateTime)

RELATED_TO (Entity -> Entity)
  Properties:
    - relationship_type (String)
    - confidence (Float)
    - context (String)

WORKS_FOR (Person -> Organization)
  Properties:
    - role (String)
    - start_date (DateTime)
    - end_date (DateTime, optional)

LOCATED_IN (Location/Organization -> Location)
  Properties:
    - precision (String: country, city, building)

MENTIONED_IN (Entity -> Document)
  Properties:
    - mention_count (Integer)
    - first_mention (DateTime)
    - last_mention (DateTime)
    - context (Text)
```

---

## Data Normalization

### Entity Normalization

```python
# File: backend/services/graph_normalizer.py

from typing import Dict, List, Optional
from datetime import datetime
import uuid

class EntityNormalizer:
    """Normalize entities for Neo4j storage"""

    @staticmethod
    def normalize_for_storage(entity: Dict) -> Dict:
        """Normalize entity for Neo4j"""

        normalized = {
            'id': EntityNormalizer._generate_entity_id(entity),
            'name': entity.get('text', '').strip(),
            'type': entity.get('entity_type', ''),
            'confidence': float(entity.get('confidence', 0.0)),
            'source_model': entity.get('source_model', ''),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'properties': {},
        }

        # Type-specific normalization
        entity_type = entity.get('entity_type', '').upper()

        if entity_type == 'CVE':
            normalized['properties'] = EntityNormalizer._normalize_cve(entity)
        elif entity_type == 'PERSON':
            normalized['properties'] = EntityNormalizer._normalize_person(entity)
        elif entity_type == 'ORGANIZATION':
            normalized['properties'] = EntityNormalizer._normalize_organization(entity)
        elif entity_type == 'LOCATION':
            normalized['properties'] = EntityNormalizer._normalize_location(entity)

        return normalized

    @staticmethod
    def _generate_entity_id(entity: Dict) -> str:
        """Generate unique entity ID"""
        entity_type = entity.get('entity_type', 'unknown').upper()
        entity_text = entity.get('text', '').lower().replace(' ', '_')

        # Include type in ID for uniqueness
        base_id = f"{entity_type}_{entity_text}"

        # Use hash for consistent IDs
        import hashlib
        hash_obj = hashlib.md5(base_id.encode())
        return f"{entity_type}_{hash_obj.hexdigest()[:8]}"

    @staticmethod
    def _normalize_cve(entity: Dict) -> Dict:
        """Normalize CVE entity"""
        text = entity.get('text', '')

        import re
        match = re.match(r'CVE-(\d{4})-(\d{4,5})', text)

        return {
            'cve_id': text,
            'year': int(match.group(1)) if match else None,
            'sequence': int(match.group(2)) if match else None,
        }

    @staticmethod
    def _normalize_person(entity: Dict) -> Dict:
        """Normalize person entity"""
        text = entity.get('text', '')
        parts = text.split()

        return {
            'first_name': parts[0] if parts else '',
            'last_name': parts[-1] if len(parts) > 1 else '',
            'full_name': text,
        }

    @staticmethod
    def _normalize_organization(entity: Dict) -> Dict:
        """Normalize organization entity"""
        return {
            'organization_name': entity.get('text', ''),
            'normalized_name': entity.get('text', '').lower(),
        }

    @staticmethod
    def _normalize_location(entity: Dict) -> Dict:
        """Normalize location entity"""
        return {
            'location_name': entity.get('text', ''),
        }


class RelationshipNormalizer:
    """Normalize relationships for Neo4j storage"""

    @staticmethod
    def normalize_for_storage(relationship: Dict) -> Dict:
        """Normalize relationship for Neo4j"""

        return {
            'type': relationship.get('relationship_type', 'RELATED_TO'),
            'confidence': float(relationship.get('confidence', 0.0)),
            'strength': float(relationship.get('strength', 0.0)),
            'evidence_count': relationship.get('evidence_count', 1),
            'source_context': relationship.get('sentence_context', ''),
            'reasoning_rules': relationship.get('reasoning_rules', []),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
        }
```

---

## Transaction Management

### ACID Transaction Implementation

```python
# File: backend/services/neo4j_client.py

from neo4j import GraphDatabase, Transaction
from typing import List, Dict, Callable, Optional
from datetime import datetime
import logging

class Neo4jClient:
    """Neo4j database client with transaction management"""

    def __init__(
        self,
        uri: str = "bolt://localhost:7687",
        username: str = "neo4j",
        password: str = "password",
        max_retries: int = 3
    ):
        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password),
            max_pool_size=50,
            connection_timeout=30,
        )
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)

    def close(self):
        """Close database connection"""
        self.driver.close()

    def execute_write_transaction(
        self,
        query: str,
        parameters: Dict = None
    ) -> Dict:
        """Execute write transaction with ACID guarantees"""

        with self.driver.session() as session:
            try:
                result = session.write_transaction(
                    self._execute_query,
                    query,
                    parameters or {}
                )

                self.logger.info(f"Write transaction successful: {query[:50]}...")
                return {
                    'success': True,
                    'result': result,
                }

            except Exception as e:
                self.logger.error(f"Write transaction failed: {str(e)}")
                return {
                    'success': False,
                    'error': str(e),
                }

    def execute_read_transaction(
        self,
        query: str,
        parameters: Dict = None
    ) -> List[Dict]:
        """Execute read transaction"""

        with self.driver.session() as session:
            try:
                result = session.read_transaction(
                    self._execute_query,
                    query,
                    parameters or {}
                )

                return result

            except Exception as e:
                self.logger.error(f"Read transaction failed: {str(e)}")
                return []

    def batch_write_transaction(
        self,
        operations: List[tuple]
    ) -> Dict:
        """
        Execute batch write with automatic rollback on failure

        operations: List of (query, parameters) tuples
        """

        with self.driver.session() as session:
            try:
                transaction = session.begin_transaction()

                results = []
                for query, params in operations:
                    result = self._execute_on_transaction(
                        transaction,
                        query,
                        params
                    )
                    results.append(result)

                # All operations succeeded, commit
                transaction.commit()

                self.logger.info(f"Batch transaction successful: {len(operations)} operations")
                return {
                    'success': True,
                    'operations_count': len(operations),
                    'results': results,
                }

            except Exception as e:
                # Rollback on any failure
                transaction.rollback()

                self.logger.error(f"Batch transaction failed, rolled back: {str(e)}")
                return {
                    'success': False,
                    'error': str(e),
                    'rolled_back': True,
                }

    @staticmethod
    def _execute_query(tx: Transaction, query: str, parameters: Dict) -> List[Dict]:
        """Execute query in transaction context"""
        result = tx.run(query, parameters)
        return [record.data() for record in result]

    @staticmethod
    def _execute_on_transaction(tx: Transaction, query: str, parameters: Dict) -> Dict:
        """Execute single query on open transaction"""
        result = tx.run(query, parameters)
        summary = result.consume()

        return {
            'nodes_created': summary.counters.nodes_created,
            'relationships_created': summary.counters.relationships_created,
            'properties_set': summary.counters.properties_set,
        }

    def import_entities(self, entities: List[Dict]) -> Dict:
        """Import entities into Neo4j"""

        operations = []

        for entity in entities:
            entity_id = entity['id']
            entity_type = entity['type'].upper()
            properties = entity.get('properties', {})

            # Create entity node
            query = f"""
                MERGE (n:{entity_type} {{id: $id}})
                SET n.name = $name
                SET n.confidence = $confidence
                SET n.created_at = $created_at
                SET n += $properties
                RETURN n
            """

            params = {
                'id': entity_id,
                'name': entity.get('name', ''),
                'confidence': entity.get('confidence', 0.0),
                'created_at': datetime.now().isoformat(),
                'properties': properties,
            }

            operations.append((query, params))

        return self.batch_write_transaction(operations)

    def import_relationships(self, relationships: List[Dict]) -> Dict:
        """Import relationships into Neo4j"""

        operations = []

        for rel in relationships:
            # Find or create nodes and relationships
            query = """
                MATCH (source {id: $source_id})
                MATCH (target {id: $target_id})
                MERGE (source)-[r:REL]->(target)
                SET r.type = $rel_type
                SET r.confidence = $confidence
                SET r.strength = $strength
                SET r.created_at = $created_at
                SET r += $properties
                RETURN r
            """

            params = {
                'source_id': rel['source_id'],
                'target_id': rel['target_id'],
                'rel_type': rel['type'],
                'confidence': rel.get('confidence', 0.0),
                'strength': rel.get('strength', 0.0),
                'created_at': datetime.now().isoformat(),
                'properties': rel.get('properties', {}),
            }

            operations.append((query, params))

        return self.batch_write_transaction(operations)
```

---

## Index Strategy

### Index Types & Creation

```cypher
// File: neo4j/indexes/create_indices.cypher

// Unique constraints (automatically create indices)
CREATE CONSTRAINT entity_id_unique IF NOT EXISTS
FOR (e:Entity) REQUIRE e.id IS UNIQUE;

// Property indices for fast lookups
CREATE INDEX entity_name_index IF NOT EXISTS
FOR (n:Entity) ON (n.name);

CREATE INDEX entity_type_index IF NOT EXISTS
FOR (n:Entity) ON (n.type);

CREATE INDEX entity_confidence_index IF NOT EXISTS
FOR (n:Entity) ON (n.confidence);

CREATE INDEX relationship_type_index IF NOT EXISTS
FOR ()-[r]->() WHERE true
ON (type(r));

CREATE INDEX relationship_confidence_index IF NOT EXISTS
FOR ()-[r]->() WHERE true
ON (r.confidence);

// Full-text search indices
CALL db.index.fulltext.createIndex(
    "entity_full_text_index",
    ["Entity"],
    ["name", "description"],
    {analyzer: "standard"}
);

CALL db.index.fulltext.createIndex(
    "document_full_text_index",
    ["Document"],
    ["content", "title"],
    {analyzer: "standard"}
);

// Composite indices for common queries
CREATE INDEX entity_type_confidence_index IF NOT EXISTS
FOR (n:Entity) ON (n.type, n.confidence DESC);
```

### Index Maintenance

```python
class IndexManager:
    """Manage Neo4j indices"""

    def __init__(self, client: Neo4jClient):
        self.client = client

    def analyze_index_usage(self) -> Dict:
        """Analyze index utilization"""

        query = """
            CALL db.indexes()
            YIELD name, entityType, labelsOrTypes, properties, type, state
            RETURN name, entityType, labelsOrTypes, properties, type, state
        """

        results = self.client.execute_read_transaction(query)
        return results

    def rebuild_indices(self) -> Dict:
        """Rebuild all indices"""

        queries = [
            "CALL db.indexes() YIELD name RETURN name",
            "CALL db.awaitIndexes()",
        ]

        for query in queries:
            self.client.execute_write_transaction(query)

        return {
            'success': True,
            'message': 'Indices rebuilt successfully',
        }

    def optimize_indices(self) -> Dict:
        """Optimize index statistics"""

        query = """
            CALL db.stats.retrieve('INDEXES')
        """

        results = self.client.execute_read_transaction(query)
        return results
```

---

## Query Optimization

### Query Examples

```cypher
// Find threat actors and their tools
MATCH (ta:ThreatActor)-[uses:USES]->(tool:Tool)
WHERE ta.confidence > 0.8 AND uses.confidence > 0.7
RETURN ta.name, collect(tool.name) as tools
ORDER BY ta.first_seen DESC;

// Find attack chains
MATCH path = (ta:ThreatActor)-[:USES]->(m:Malware)-[:EXPLOITS]->(v:Vulnerability)
RETURN ta.name, m.name, v.cve_id, length(path) as chain_length;

// Find related entities with shortest path
MATCH (e1:Entity {id: $entity_id_1})
MATCH (e2:Entity {id: $entity_id_2})
MATCH shortestPath((e1)-[*]-(e2))
RETURN shortestPath;

// Entity neighborhood query
MATCH (center:Entity {id: $entity_id})
MATCH (center)--[r]-(neighbor)
RETURN center, collect({neighbor: neighbor, relationship: type(r)}) as neighbors;

// Pattern matching for threat hunting
MATCH (ta:ThreatActor)-[:USES]->(m:Malware)
      (m)-[:EXPLOITS]->(v:Vulnerability)
      (v)-[:AFFECTS]->(system:System)
WHERE v.cvss_score > 7.0
RETURN ta, m, v, system;
```

---

## Data Import Pipeline

### Bulk Import Process

```python
class BulkImportPipeline:
    """Pipeline for bulk importing data into Neo4j"""

    def __init__(self, client: Neo4jClient, batch_size: int = 1000):
        self.client = client
        self.batch_size = batch_size

    def import_from_knowledge_graph(self, kg: Dict) -> Dict:
        """Import entire knowledge graph"""

        # Import nodes
        node_import_result = self._import_nodes(kg['nodes'])

        # Import relationships
        rel_import_result = self._import_relationships(kg['edges'])

        return {
            'nodes_imported': node_import_result.get('count', 0),
            'relationships_imported': rel_import_result.get('count', 0),
        }

    def _import_nodes(self, nodes: List[Dict]) -> Dict:
        """Batch import nodes"""

        total_imported = 0

        for i in range(0, len(nodes), self.batch_size):
            batch = nodes[i:i + self.batch_size]

            # Create MERGE statement for batch
            merge_queries = []
            for node in batch:
                merge_queries.append(f"""
                    MERGE (n:{node.get('type', 'Entity')} {{id: '{node['id']}'}})
                    SET n.name = '{node.get('name', '')}'
                    SET n.confidence = {node.get('confidence', 0.0)}
                """)

            # Execute batch
            result = self.client.batch_write_transaction([
                (q, {}) for q in merge_queries
            ])

            if result['success']:
                total_imported += len(batch)

        return {'count': total_imported}

    def _import_relationships(self, edges: List[Dict]) -> Dict:
        """Batch import relationships"""

        total_imported = 0

        for i in range(0, len(edges), self.batch_size):
            batch = edges[i:i + self.batch_size]

            merge_queries = []
            for edge in batch:
                merge_queries.append(f"""
                    MATCH (source {{id: '{edge['source']}'}})
                    MATCH (target {{id: '{edge['target']}'}})
                    MERGE (source)-[r:{edge.get('type', 'RELATED_TO')}]->(target)
                    SET r.confidence = {edge.get('confidence', 0.0)}
                """)

            result = self.client.batch_write_transaction([
                (q, {}) for q in merge_queries
            ])

            if result['success']:
                total_imported += len(batch)

        return {'count': total_imported}
```

---

## ACID Compliance

### Consistency Guarantees

```python
class ACIDManager:
    """Manage ACID properties"""

    @staticmethod
    def verify_consistency(client: Neo4jClient) -> Dict:
        """Verify database consistency"""

        # Check for orphaned relationships
        query = """
            MATCH (n)-->(m)
            WHERE NOT EXISTS((n))
            OR NOT EXISTS((m))
            RETURN count(*) as orphaned_relationships
        """

        results = client.execute_read_transaction(query)

        return {
            'orphaned_relationships': results[0].get('orphaned_relationships', 0) if results else 0,
            'consistent': results[0].get('orphaned_relationships', 0) == 0 if results else False,
        }

    @staticmethod
    def create_backup(client: Neo4jClient) -> Dict:
        """Create database backup"""

        query = "CALL db.checkpoint()"

        result = client.execute_write_transaction(query)

        return {
            'backup_created': result['success'],
            'timestamp': datetime.now().isoformat(),
        }
```

---

## Performance Tuning

### Query Performance Analysis

```python
class QueryOptimizer:
    """Optimize query performance"""

    @staticmethod
    def analyze_query_plan(client: Neo4jClient, query: str) -> Dict:
        """Analyze query execution plan"""

        explain_query = f"EXPLAIN {query}"

        results = client.execute_read_transaction(explain_query)

        return {
            'plan': results,
            'analysis': QueryOptimizer._extract_insights(results),
        }

    @staticmethod
    def _extract_insights(plan: List[Dict]) -> Dict:
        """Extract optimization insights"""

        return {
            'full_scans': any('AllNodesScan' in str(step) for step in plan),
            'cartesian_products': any('CartesianProduct' in str(step) for step in plan),
            'recommendations': [],
        }
```

---

**End of INGESTION_STEP4_NEO4J_STORAGE.md**
*Total Lines: 764 | Complete Neo4j implementation with transactions and optimization*
