# Cypher Query API Documentation

**File:** Cypher-Query-API.md
**Created:** 2025-11-03 17:21:26 CST
**Modified:** 2025-11-08 14:30:00 CST
**Version:** v2.0.0
**Author:** OpenAPI Documentation Specialist
**Purpose:** Comprehensive Cypher query language reference for AEON knowledge graph operations including MITRE ATT&CK
**Status:** ACTIVE

Tags: #cypher #neo4j #query-language #graph #api #knowledge-graph
Backlinks: [[Neo4j-Database]] [[AEON-UI-Application]]

---

## Executive Summary

Complete reference for Neo4j Cypher query language covering pattern matching, CRUD operations, aggregations, graph algorithms, MITRE ATT&CK integration, and performance optimization for the AEON Digital Twin Cybersecurity knowledge graph (115 documents, 12,256 entities, 14,645 relationships, 2,051 MITRE entities, 40,886 MITRE relationships).

---

## Current System State

**Database Status** (2025-11-03 17:21:26 CST):
- Neo4j Version: 5.26.0 Community Edition
- Protocol: Bolt + HTTP Transactional API
- Database: neo4j (default)
- Entities: 12,256 nodes
- Relationships: 14,645 edges
- Documents: 115

**Connection Details**:
- Bolt: `bolt://localhost:7687`
- HTTP API: `http://localhost:7474`
- Auth: neo4j / neo4j@openspg

---

## Cypher Language Fundamentals

### Query Structure

```cypher
// Basic Pattern: Match nodes and relationships
MATCH (variable:Label {property: value})
WHERE condition
RETURN variable
ORDER BY variable.property
LIMIT count
```

### Pattern Syntax

| Pattern | Meaning | Example |
|---------|---------|---------|
| `()` | Anonymous node | `MATCH (n)` |
| `(n)` | Named node variable | `MATCH (n:Entity)` |
| `(n:Label)` | Node with label | `MATCH (n:Document)` |
| `{prop: val}` | Property match | `MATCH (n {id: "123"})` |
| `-[]->` | Directed relationship | `(a)-[r:RELATES]->(b)` |
| `-[]-` | Undirected relationship | `(a)-[r]-(b)` |
| `-[*]->` | Variable length path | `(a)-[*1..3]->(b)` |

### Data Types

```cypher
// Scalar Types
String:    "text"
Integer:   42
Float:     3.14
Boolean:   true, false
Null:      null

// Temporal Types
Date:      date("2025-11-03")
DateTime:  datetime("2025-11-03T17:21:26Z")
Duration:  duration("P1Y2M3D")

// Spatial Types
Point:     point({latitude: 40.7128, longitude: -74.0060})

// Collection Types
List:      [1, 2, 3]
Map:       {key: "value", num: 42}
```

---

## Pattern Matching

### Basic Node Matching

```cypher
// Match all nodes
MATCH (n) RETURN n LIMIT 100

// Match nodes by label
MATCH (d:Document) RETURN d

// Match nodes by property
MATCH (e:Entity {type: "vulnerability"}) RETURN e

// Match nodes with multiple labels
MATCH (n:Entity:Threat) RETURN n

// Match with WHERE clause
MATCH (e:Entity)
WHERE e.confidence > 0.8 AND e.type = "malware"
RETURN e.name, e.confidence
```

### Relationship Matching

```cypher
// Match any relationship
MATCH (a)-[r]->(b) RETURN a, r, b LIMIT 50

// Match specific relationship type
MATCH (d:Document)-[r:CONTAINS]->(e:Entity)
RETURN d.title, e.name

// Match multiple relationship types
MATCH (e:Entity)-[r:RELATES_TO|DEPENDS_ON]->(related)
RETURN e, type(r), related

// Match relationship with properties
MATCH (e1:Entity)-[r:SIMILAR_TO {score: > 0.9}]->(e2:Entity)
RETURN e1.name, r.score, e2.name

// Bidirectional matching
MATCH (a:Entity)-[r]-(b:Entity)
WHERE a.id = "entity_123"
RETURN DISTINCT b
```

### Path Patterns

```cypher
// Variable length paths (1 to 3 hops)
MATCH path = (start:Entity)-[*1..3]->(end:Entity)
WHERE start.id = "entity_001"
RETURN path

// Shortest path
MATCH (start:Entity {id: "entity_001"}),
      (end:Entity {id: "entity_999"}),
      path = shortestPath((start)-[*..10]-(end))
RETURN path

// All paths between nodes
MATCH path = (start:Entity {id: "entity_001"})
            -[*..5]-
            (end:Entity {id: "entity_999"})
RETURN path

// Path with relationship type constraints
MATCH path = (doc:Document)-[:CONTAINS*1..2]->(entity:Entity)
WHERE doc.title CONTAINS "security"
RETURN path LIMIT 10
```

### Complex Patterns

```cypher
// Multiple pattern matching
MATCH (d:Document)-[:CONTAINS]->(e:Entity),
      (e)-[:RELATES_TO]->(related:Entity)
WHERE d.source = "NIST"
RETURN d.title, collect(DISTINCT e.name) AS entities,
       collect(DISTINCT related.name) AS related_entities

// Pattern with optional match
MATCH (e:Entity)
OPTIONAL MATCH (e)-[r:HAS_ATTRIBUTE]->(attr:Attribute)
RETURN e.name, collect(attr.value) AS attributes

// Negation (nodes without relationships)
MATCH (e:Entity)
WHERE NOT (e)-[:RELATES_TO]->()
RETURN e.name AS isolated_entities

// Pattern with multiple conditions
MATCH (source:Entity)-[r:RELATES_TO]->(target:Entity)
WHERE source.type = "threat"
  AND target.type = "vulnerability"
  AND r.confidence > 0.7
RETURN source.name, r.relationship_type, target.name
ORDER BY r.confidence DESC
```

---

## CRUD Operations

### CREATE - Add Data

#### Create Nodes

```cypher
// Create single node
CREATE (e:Entity {
  id: "entity_" + randomUUID(),
  name: "SQL Injection",
  type: "vulnerability",
  severity: "high",
  cwe_id: "CWE-89",
  created: datetime(),
  updated: datetime()
})
RETURN e

// Create multiple nodes
CREATE
  (e1:Entity {id: "e001", name: "XSS", type: "vulnerability"}),
  (e2:Entity {id: "e002", name: "CSRF", type: "vulnerability"}),
  (e3:Entity {id: "e003", name: "RCE", type: "vulnerability"})
RETURN e1, e2, e3

// Create with parameters
CREATE (e:Entity $props)
RETURN e
// Parameters: {props: {id: "e123", name: "Buffer Overflow", type: "vulnerability"}}
```

#### Create Relationships

```cypher
// Create relationship between existing nodes
MATCH (source:Entity {id: "entity_001"}),
      (target:Entity {id: "entity_002"})
CREATE (source)-[r:RELATES_TO {
  type: "exploits",
  confidence: 0.95,
  created: datetime()
}]->(target)
RETURN r

// Create nodes and relationships together
CREATE (d:Document {id: "doc_123", title: "Security Report"}),
       (e1:Entity {id: "e_456", name: "Malware"}),
       (e2:Entity {id: "e_789", name: "Trojan"}),
       (d)-[:CONTAINS]->(e1),
       (d)-[:CONTAINS]->(e2),
       (e1)-[:IS_TYPE_OF]->(e2)
RETURN d, e1, e2
```

### READ - Query Data

```cypher
// Simple read
MATCH (e:Entity)
RETURN e.name, e.type, e.severity
LIMIT 100

// Read with filtering
MATCH (e:Entity)
WHERE e.type = "vulnerability" AND e.severity IN ["high", "critical"]
RETURN e.name, e.cwe_id, e.severity
ORDER BY e.severity DESC, e.name ASC

// Read with aggregation
MATCH (d:Document)-[:CONTAINS]->(e:Entity)
RETURN d.title, count(e) AS entity_count
ORDER BY entity_count DESC
LIMIT 10

// Read with complex filtering
MATCH (e:Entity)
WHERE e.name =~ "(?i).*injection.*"  // Case-insensitive regex
  AND e.created > datetime() - duration("P30D")  // Last 30 days
RETURN e.name, e.type, e.created
```

### UPDATE - Modify Data

```cypher
// Update single property
MATCH (e:Entity {id: "entity_123"})
SET e.severity = "critical",
    e.updated = datetime()
RETURN e

// Update multiple properties
MATCH (e:Entity)
WHERE e.type = "vulnerability" AND e.cvss_score > 9.0
SET e.severity = "critical",
    e.priority = "immediate",
    e.reviewed = true,
    e.updated = datetime()
RETURN count(e) AS updated_count

// Add label
MATCH (e:Entity {type: "malware"})
SET e:Threat
RETURN e

// Remove property
MATCH (e:Entity {id: "entity_123"})
REMOVE e.deprecated_field
RETURN e

// Update with parameters
MATCH (e:Entity {id: $id})
SET e += $updates  // Merge properties
RETURN e
// Parameters: {id: "e123", updates: {severity: "high", reviewed: true}}
```

### MERGE - Create or Update

```cypher
// Merge node (create if not exists, update if exists)
MERGE (e:Entity {id: "entity_123"})
ON CREATE SET e.name = "New Entity",
              e.created = datetime(),
              e.type = "vulnerability"
ON MATCH SET e.updated = datetime(),
             e.access_count = coalesce(e.access_count, 0) + 1
RETURN e

// Merge relationship
MATCH (source:Entity {id: "e001"}),
      (target:Entity {id: "e002"})
MERGE (source)-[r:RELATES_TO]->(target)
ON CREATE SET r.created = datetime(),
              r.confidence = 0.8
ON MATCH SET r.updated = datetime(),
             r.count = coalesce(r.count, 0) + 1
RETURN r

// Complex merge with multiple patterns
MERGE (d:Document {id: $doc_id})
ON CREATE SET d.title = $title, d.created = datetime()
WITH d
MERGE (e:Entity {id: $entity_id})
ON CREATE SET e.name = $entity_name, e.created = datetime()
WITH d, e
MERGE (d)-[r:CONTAINS]->(e)
ON CREATE SET r.created = datetime()
RETURN d, e, r
```

### DELETE - Remove Data

```cypher
// Delete node (requires no relationships)
MATCH (e:Entity {id: "entity_123"})
DELETE e

// Delete node and all relationships
MATCH (e:Entity {id: "entity_123"})
DETACH DELETE e

// Delete relationships only
MATCH (e1:Entity)-[r:RELATES_TO]->(e2:Entity)
WHERE r.confidence < 0.5
DELETE r

// Conditional delete with count
MATCH (e:Entity)
WHERE e.deprecated = true AND e.created < datetime() - duration("P365D")
WITH e
DETACH DELETE e
RETURN count(e) AS deleted_count

// Delete all data (DANGEROUS - use with caution)
MATCH (n)
DETACH DELETE n
```

---

## Aggregation & Analytics

### Basic Aggregations

```cypher
// Count nodes
MATCH (e:Entity)
RETURN count(e) AS total_entities

// Count by type
MATCH (e:Entity)
RETURN e.type, count(*) AS count
ORDER BY count DESC

// Sum, average, min, max
MATCH (e:Entity)
WHERE e.cvss_score IS NOT NULL
RETURN
  count(e) AS total,
  avg(e.cvss_score) AS avg_score,
  min(e.cvss_score) AS min_score,
  max(e.cvss_score) AS max_score,
  stDev(e.cvss_score) AS std_dev

// Percentiles
MATCH (e:Entity)
WHERE e.cvss_score IS NOT NULL
RETURN
  percentileCont(e.cvss_score, 0.25) AS q1,
  percentileCont(e.cvss_score, 0.50) AS median,
  percentileCont(e.cvss_score, 0.75) AS q3,
  percentileCont(e.cvss_score, 0.95) AS p95
```

### Collection Functions

```cypher
// Collect values into list
MATCH (d:Document)-[:CONTAINS]->(e:Entity)
RETURN d.title, collect(e.name) AS entities
ORDER BY size(collect(e.name)) DESC
LIMIT 10

// Collect distinct values
MATCH (e:Entity)-[:HAS_TAG]->(t:Tag)
RETURN e.name, collect(DISTINCT t.value) AS tags

// List comprehension
MATCH (d:Document)
RETURN d.title,
       [e IN d.entities | e.name] AS entity_names,
       [e IN d.entities WHERE e.type = "threat" | e.name] AS threats
```

### Grouping & Aggregation

```cypher
// Group by with multiple aggregations
MATCH (d:Document)-[:CONTAINS]->(e:Entity)
RETURN
  d.source,
  count(DISTINCT d) AS document_count,
  count(e) AS total_entities,
  count(DISTINCT e.type) AS entity_types,
  avg(size((d)-[:CONTAINS]->())) AS avg_entities_per_doc
ORDER BY total_entities DESC

// Window-like aggregation with WITH
MATCH (e:Entity)
WITH e.type AS entity_type, collect(e) AS entities
RETURN
  entity_type,
  size(entities) AS count,
  [e IN entities | e.name][..5] AS sample_names
ORDER BY count DESC
```

### Statistical Analysis

```cypher
// Distribution analysis
MATCH (e:Entity)
WHERE e.type = "vulnerability"
WITH e.severity AS severity, count(*) AS count
RETURN severity, count,
       100.0 * count / sum(count) AS percentage
ORDER BY count DESC

// Time series aggregation
MATCH (e:Entity)
WHERE e.created IS NOT NULL
WITH date(e.created) AS creation_date
RETURN
  creation_date.year AS year,
  creation_date.month AS month,
  count(*) AS entities_created
ORDER BY year, month

// Relationship density
MATCH (e:Entity)
WITH count(e) AS total_nodes
MATCH ()-[r]->()
WITH total_nodes, count(r) AS total_rels
RETURN
  total_nodes,
  total_rels,
  2.0 * total_rels / (total_nodes * (total_nodes - 1)) AS density
```

---

## Graph Algorithms

### Centrality Measures

```cypher
// Degree centrality (connection count)
MATCH (e:Entity)
RETURN e.name,
       size((e)-->()) AS out_degree,
       size((e)<--()) AS in_degree,
       size((e)--()) AS total_degree
ORDER BY total_degree DESC
LIMIT 10

// Betweenness centrality (simplified)
MATCH (n:Entity)
WITH n, size((n)--()) AS degree
ORDER BY degree DESC
LIMIT 10
RETURN n.name, degree

// PageRank-like calculation
MATCH (e:Entity)<-[r]-(source)
WITH e, count(r) AS incoming, collect(source) AS sources
RETURN e.name, incoming,
       reduce(score = 0.0, s IN sources |
         score + 1.0 / size((s)--())
       ) AS pagerank_score
ORDER BY pagerank_score DESC
LIMIT 10
```

### Path Finding

```cypher
// Shortest path
MATCH (start:Entity {id: "entity_001"}),
      (end:Entity {id: "entity_999"})
MATCH path = shortestPath((start)-[*..10]-(end))
RETURN path, length(path) AS path_length

// All shortest paths
MATCH (start:Entity {name: "SQL Injection"}),
      (end:Entity {name: "Database Breach"})
MATCH paths = allShortestPaths((start)-[*..10]-(end))
RETURN paths, length(paths) AS path_length

// Dijkstra-style weighted path
MATCH (start:Entity {id: "entity_001"}),
      (end:Entity {id: "entity_999"})
CALL apoc.algo.dijkstra(start, end, 'RELATES_TO', 'weight')
YIELD path, weight
RETURN path, weight
```

### Community Detection

```cypher
// Simple clustering by common neighbors
MATCH (e1:Entity)-[:RELATES_TO]->(common)<-[:RELATES_TO]-(e2:Entity)
WHERE id(e1) < id(e2)
WITH e1, e2, count(common) AS common_neighbors
WHERE common_neighbors > 3
RETURN e1.name, e2.name, common_neighbors
ORDER BY common_neighbors DESC

// Triangle detection (triangular relationships)
MATCH (a:Entity)-[:RELATES_TO]->(b:Entity)-[:RELATES_TO]->(c:Entity)
WHERE (a)-[:RELATES_TO]->(c) AND id(a) < id(b) AND id(b) < id(c)
RETURN a.name, b.name, c.name
LIMIT 50
```

### Graph Metrics

```cypher
// Network diameter (longest shortest path)
MATCH (n:Entity), (m:Entity)
WHERE id(n) < id(m)
MATCH path = shortestPath((n)-[*..20]-(m))
RETURN max(length(path)) AS diameter

// Average path length
MATCH (n:Entity), (m:Entity)
WHERE id(n) < id(m)
MATCH path = shortestPath((n)-[*..20]-(m))
RETURN avg(length(path)) AS avg_path_length

// Clustering coefficient
MATCH (n:Entity)
OPTIONAL MATCH (n)-[:RELATES_TO]-(neighbor)
WITH n, collect(DISTINCT neighbor) AS neighbors,
     count(DISTINCT neighbor) AS degree
WHERE degree > 1
UNWIND neighbors AS n1
UNWIND neighbors AS n2
WITH n, n1, n2, degree
WHERE id(n1) < id(n2) AND (n1)-[:RELATES_TO]-(n2)
RETURN n.name,
       count(*) * 2.0 / (degree * (degree - 1)) AS clustering_coef
ORDER BY clustering_coef DESC
LIMIT 10
```

---

## Performance Optimization

### Index Usage

```cypher
// Create indexes for common queries
CREATE INDEX entity_id_idx FOR (n:Entity) ON (n.id);
CREATE INDEX entity_type_idx FOR (n:Entity) ON (n.type);
CREATE INDEX document_title_idx FOR (n:Document) ON (n.title);
CREATE INDEX entity_name_idx FOR (n:Entity) ON (n.name);

// Composite index for multi-property queries
CREATE INDEX entity_type_severity_idx
FOR (n:Entity) ON (n.type, n.severity);

// Full-text search index
CREATE FULLTEXT INDEX entity_fulltext
FOR (n:Entity) ON EACH [n.name, n.description];

// Show all indexes
SHOW INDEXES;

// Use full-text search
CALL db.index.fulltext.queryNodes(
  "entity_fulltext",
  "sql injection OR xss"
) YIELD node, score
RETURN node.name, score
ORDER BY score DESC;
```

### Query Optimization

```cypher
// Use PROFILE to analyze query execution
PROFILE
MATCH (d:Document)-[:CONTAINS]->(e:Entity)
WHERE e.type = "vulnerability"
RETURN d.title, count(e) AS vuln_count
ORDER BY vuln_count DESC;

// Use EXPLAIN for query plan without execution
EXPLAIN
MATCH (e:Entity)
WHERE e.name STARTS WITH "SQL"
RETURN e;

// Optimize with early filtering
// BAD: Filter after pattern match
MATCH (d:Document)-[:CONTAINS]->(e:Entity)
WHERE d.source = "NIST" AND e.type = "threat"
RETURN d, e;

// GOOD: Filter early in pattern
MATCH (d:Document {source: "NIST"})-[:CONTAINS]->(e:Entity {type: "threat"})
RETURN d, e;

// Use LIMIT for large result sets
MATCH (e:Entity)
WHERE e.type = "vulnerability"
RETURN e
LIMIT 100;

// Use parameters for repeated queries (enables query caching)
MATCH (e:Entity {type: $entity_type})
WHERE e.severity = $severity
RETURN e;
```

### Batch Operations

```cypher
// Process in batches using UNWIND
UNWIND $batch AS item
MERGE (e:Entity {id: item.id})
SET e += item.properties;

// Batch create with parameters
UNWIND $entities AS entity_data
CREATE (e:Entity)
SET e = entity_data;

// Periodic commit for large imports (deprecated in Neo4j 5+)
// Use CALL { ... } IN TRANSACTIONS instead
LOAD CSV WITH HEADERS FROM "file:///entities.csv" AS row
CALL {
  WITH row
  CREATE (e:Entity {
    id: row.id,
    name: row.name,
    type: row.type
  })
} IN TRANSACTIONS OF 1000 ROWS;
```

### Memory Management

```cypher
// Use WITH to free memory during query
MATCH (d:Document)
WITH d.id AS doc_id, d.title AS title
MATCH (d:Document {id: doc_id})-[:CONTAINS]->(e:Entity)
RETURN title, collect(e.name) AS entities;

// Limit intermediate results
MATCH (e:Entity)
WHERE e.type = "vulnerability"
WITH e LIMIT 1000
MATCH (e)-[:RELATES_TO]->(related)
RETURN e.name, collect(related.name) AS related_entities;

// Use count(*) instead of count(variable) when possible
MATCH (e:Entity)
RETURN count(*) AS total;  // More efficient
```

---

## Integration with AEON UI

### Common UI Query Patterns

#### Dashboard Statistics

```cypher
// Entity type distribution for pie chart
MATCH (e:Entity)
RETURN e.type AS entity_type, count(*) AS count
ORDER BY count DESC;

// Relationship type distribution
MATCH ()-[r]->()
RETURN type(r) AS relationship_type, count(*) AS count
ORDER BY count DESC
LIMIT 10;

// Time series of entity creation
MATCH (e:Entity)
WHERE e.created IS NOT NULL
WITH date(e.created) AS creation_date
WITH creation_date.year AS year,
     creation_date.month AS month,
     count(*) AS count
RETURN year, month, count
ORDER BY year, month;

// Top documents by entity count
MATCH (d:Document)-[:CONTAINS]->(e:Entity)
RETURN d.id, d.title, count(e) AS entity_count
ORDER BY entity_count DESC
LIMIT 10;
```

#### Search & Filter Queries

```cypher
// Full-text entity search
CALL db.index.fulltext.queryNodes(
  "entity_fulltext",
  $searchQuery
) YIELD node, score
RETURN node.id, node.name, node.type, score
ORDER BY score DESC
LIMIT 20;

// Filtered entity list with pagination
MATCH (e:Entity)
WHERE ($type IS NULL OR e.type = $type)
  AND ($severity IS NULL OR e.severity = $severity)
  AND ($searchTerm IS NULL OR e.name CONTAINS $searchTerm)
RETURN e.id, e.name, e.type, e.severity, e.created
ORDER BY e.created DESC
SKIP $skip
LIMIT $limit;

// Autocomplete suggestions
MATCH (e:Entity)
WHERE e.name STARTS WITH $prefix
RETURN DISTINCT e.name
ORDER BY e.name
LIMIT 10;
```

#### Graph Visualization Queries

```cypher
// Get node and its immediate neighborhood
MATCH (center:Entity {id: $nodeId})
OPTIONAL MATCH (center)-[r]-(connected:Entity)
RETURN center, collect(DISTINCT r) AS relationships,
       collect(DISTINCT connected) AS connected_nodes;

// Get subgraph within N hops
MATCH path = (center:Entity {id: $nodeId})-[*1..$maxHops]-(connected)
WITH nodes(path) AS pathNodes, relationships(path) AS pathRels
RETURN collect(DISTINCT pathNodes) AS nodes,
       collect(DISTINCT pathRels) AS relationships;

// Get strongly connected component
MATCH (start:Entity {id: $nodeId})
CALL apoc.path.subgraphAll(start, {
  relationshipFilter: "RELATES_TO",
  maxLevel: 3
}) YIELD nodes, relationships
RETURN nodes, relationships;
```

### Python Driver Integration

```python
from neo4j import GraphDatabase

class AEONGraphDB:
    def __init__(self, uri="bolt://localhost:7687",
                 user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_entity_by_id(self, entity_id):
        """Get single entity by ID"""
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (e:Entity {id: $id}) RETURN e",
                id=entity_id
            )
            record = result.single()
            return dict(record["e"]) if record else None

    def search_entities(self, search_term, entity_type=None, limit=20):
        """Full-text search with optional type filter"""
        query = """
        CALL db.index.fulltext.queryNodes('entity_fulltext', $search)
        YIELD node, score
        WHERE $type IS NULL OR node.type = $type
        RETURN node, score
        ORDER BY score DESC
        LIMIT $limit
        """
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                query,
                search=search_term,
                type=entity_type,
                limit=limit
            )
            return [
                {**dict(record["node"]), "score": record["score"]}
                for record in result
            ]

    def get_entity_neighborhood(self, entity_id, max_hops=2):
        """Get entity with connected nodes and relationships"""
        query = """
        MATCH (center:Entity {id: $id})
        OPTIONAL MATCH path = (center)-[*1..$maxHops]-(connected)
        WITH center, collect(DISTINCT nodes(path)) AS pathNodes,
             collect(DISTINCT relationships(path)) AS pathRels
        RETURN center,
               [n IN pathNodes | {
                 id: n.id,
                 name: n.name,
                 type: n.type
               }] AS nodes,
               [r IN pathRels | {
                 type: type(r),
                 source: startNode(r).id,
                 target: endNode(r).id
               }] AS relationships
        """
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                query,
                id=entity_id,
                maxHops=max_hops
            )
            record = result.single()
            if not record:
                return None

            return {
                "center": dict(record["center"]),
                "nodes": record["nodes"],
                "relationships": record["relationships"]
            }

    def get_dashboard_stats(self):
        """Get statistics for dashboard"""
        query = """
        MATCH (d:Document)
        WITH count(d) AS doc_count
        MATCH (e:Entity)
        WITH doc_count, count(e) AS entity_count, collect(e.type) AS types
        MATCH ()-[r]->()
        RETURN doc_count, entity_count, count(r) AS rel_count,
               apoc.coll.frequencies(types) AS type_distribution
        """
        with self.driver.session(database="neo4j") as session:
            result = session.run(query)
            return result.single().data()

# Usage example
db = AEONGraphDB()
try:
    stats = db.get_dashboard_stats()
    print(f"Documents: {stats['doc_count']}")
    print(f"Entities: {stats['entity_count']}")
    print(f"Relationships: {stats['rel_count']}")

    results = db.search_entities("sql injection", entity_type="vulnerability")
    for entity in results:
        print(f"{entity['name']}: {entity['score']}")
finally:
    db.close()
```

---

## HTTP Transactional API

### Execute Cypher via REST

```http
POST /db/neo4j/tx/commit
Host: localhost:7474
Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==
Content-Type: application/json

{
  "statements": [
    {
      "statement": "MATCH (e:Entity {type: $type}) RETURN e.name, e.severity LIMIT $limit",
      "parameters": {
        "type": "vulnerability",
        "limit": 10
      },
      "resultDataContents": ["row", "graph"]
    }
  ]
}
```

**Response**:
```json
{
  "results": [
    {
      "columns": ["e.name", "e.severity"],
      "data": [
        {
          "row": ["SQL Injection", "high"],
          "graph": {
            "nodes": [{
              "id": "123",
              "labels": ["Entity"],
              "properties": {
                "name": "SQL Injection",
                "type": "vulnerability",
                "severity": "high"
              }
            }],
            "relationships": []
          }
        }
      ]
    }
  ],
  "errors": []
}
```

### Transaction Management

```http
# Begin transaction
POST /db/neo4j/tx
Content-Type: application/json
Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==

{
  "statements": [{
    "statement": "CREATE (e:Entity {id: $id, name: $name}) RETURN e",
    "parameters": {"id": "e123", "name": "Test Entity"}
  }]
}

# Continue transaction (use transaction_id from response)
POST /db/neo4j/tx/{transaction_id}
Content-Type: application/json
Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==

{
  "statements": [{
    "statement": "MATCH (e:Entity {id: $id}) SET e.verified = true RETURN e",
    "parameters": {"id": "e123"}
  }]
}

# Commit transaction
POST /db/neo4j/tx/{transaction_id}/commit
Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==

# Rollback transaction
DELETE /db/neo4j/tx/{transaction_id}
Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==
```

---

## Advanced Cypher Features

### Subqueries

```cypher
// Subquery with CALL
MATCH (d:Document)
CALL {
  WITH d
  MATCH (d)-[:CONTAINS]->(e:Entity)
  RETURN count(e) AS entity_count
}
RETURN d.title, entity_count
ORDER BY entity_count DESC
LIMIT 10;

// Post-union processing
CALL {
  MATCH (e:Entity {type: "threat"})
  RETURN e.name AS name, "threat" AS category
  UNION
  MATCH (e:Entity {type: "vulnerability"})
  RETURN e.name AS name, "vulnerability" AS category
}
RETURN category, count(*) AS count;
```

### Conditional Logic

```cypher
// CASE expressions
MATCH (e:Entity)
RETURN e.name,
       CASE e.severity
         WHEN "critical" THEN 4
         WHEN "high" THEN 3
         WHEN "medium" THEN 2
         WHEN "low" THEN 1
         ELSE 0
       END AS severity_level
ORDER BY severity_level DESC;

// CASE with conditions
MATCH (e:Entity)
RETURN e.name,
       CASE
         WHEN e.cvss_score >= 9.0 THEN "critical"
         WHEN e.cvss_score >= 7.0 THEN "high"
         WHEN e.cvss_score >= 4.0 THEN "medium"
         ELSE "low"
       END AS calculated_severity;
```

### List Operations

```cypher
// List comprehension
MATCH (d:Document)-[:CONTAINS]->(e:Entity)
RETURN d.title,
       [x IN collect(e.name) WHERE x STARTS WITH "SQL" | x] AS sql_entities;

// List predicates
MATCH (e:Entity)
WHERE ALL(tag IN e.tags WHERE tag IN ["security", "vulnerability"])
RETURN e.name;

MATCH (e:Entity)
WHERE ANY(tag IN e.tags WHERE tag = "critical")
RETURN e.name;

// List reduction
MATCH (d:Document)-[:CONTAINS]->(e:Entity)
RETURN d.title,
       reduce(score = 0, e IN collect(e) |
         score + coalesce(e.confidence, 0.5)
       ) AS total_confidence;
```

---

## MITRE ATT&CK Query Patterns

### Capability 1: Attack Path Discovery

```cypher
// Find attack paths from threat actor to critical CVEs
MATCH path = (actor:MitreActor {name: $actorName})
             -[:USES_TECHNIQUE|LEVERAGES_SOFTWARE*1..4]->
             (tech:MitreTechnique)
             -[:EXPLOITS_CVE]->(cve:CVE)
WHERE cve.cvss_score >= 9.0
RETURN path, length(path) AS hops, cve.cvss_score
ORDER BY cve.cvss_score DESC, hops
LIMIT 10
```

**Parameters**: `{actorName: "APT28"}`
**Use Case**: Threat hunting, risk assessment, attack surface analysis

---

### Capability 2: Defensive Gap Analysis

```cypher
// Find critical techniques with insufficient mitigations
MATCH (tech:MitreTechnique)
WHERE "Initial Access" IN tech.tactic OR "Execution" IN tech.tactic
OPTIONAL MATCH (tech)<-[r:MITIGATES]-(mit:MitreMitigation)
WHERE r.effectiveness IN ["significant", "complete"]
WITH tech, count(mit) AS mitigation_count
WHERE mitigation_count < 2
RETURN tech.id, tech.name, tech.tactic, mitigation_count
ORDER BY mitigation_count, tech.id
```

**Use Case**: Security posture improvement, defensive planning

---

### Capability 3: Threat Actor Profiling

```cypher
// Complete profile of threat actor TTPs and toolset
MATCH (actor:MitreActor {name: $actorName})
OPTIONAL MATCH (actor)-[:USES_TECHNIQUE]->(tech:MitreTechnique)
OPTIONAL MATCH (actor)-[:LEVERAGES_SOFTWARE]->(soft:MitreSoftware)
RETURN actor {
  .*,
  techniques: collect(DISTINCT tech {.id, .name, .tactic}),
  software: collect(DISTINCT soft {.id, .name, .type}),
  technique_count: count(DISTINCT tech),
  software_count: count(DISTINCT soft)
} AS profile
```

**Parameters**: `{actorName: "APT28"}`
**Use Case**: Threat intelligence, incident response, attribution

---

### Capability 4: Mitigation Prioritization

```cypher
// Find mitigations with broadest coverage against active threats
MATCH (actor:MitreActor {active: true})-[:USES_TECHNIQUE]->(tech:MitreTechnique)
MATCH (tech)<-[:MITIGATES]-(mit:MitreMitigation)
WITH mit,
     count(DISTINCT actor) AS actors_covered,
     count(DISTINCT tech) AS techniques_covered,
     collect(DISTINCT tech.name)[..5] AS sample_techniques
RETURN mit.id, mit.name, mit.description,
       actors_covered,
       techniques_covered,
       sample_techniques
ORDER BY actors_covered DESC, techniques_covered DESC
LIMIT 20
```

**Use Case**: Budget allocation, security roadmap planning

---

### Capability 5: Software Capability Analysis

```cypher
// Analyze malware capabilities and available mitigations
MATCH (soft:MitreSoftware {name: $softwareName})
      -[:IMPLEMENTS_TECHNIQUE]->(tech:MitreTechnique)
OPTIONAL MATCH (tech)<-[:MITIGATES]-(mit:MitreMitigation)
RETURN tech.id, tech.name, tech.tactic,
       collect(DISTINCT mit.name) AS available_mitigations,
       size(collect(DISTINCT mit)) AS mitigation_count
ORDER BY mitigation_count, tech.id
```

**Parameters**: `{softwareName: "Mimikatz"}`
**Use Case**: Malware analysis, detection engineering

---

### Capability 6: CVE Exploitation Chains

```cypher
// Find CVEs exploited by multiple APT groups
MATCH (actor:MitreActor {sophistication: "advanced"})
      -[:USES_TECHNIQUE]->(tech:MitreTechnique)
      -[:EXPLOITS_CVE]->(cve:CVE)
WITH cve,
     collect(DISTINCT actor.name) AS exploiting_actors,
     collect(DISTINCT tech.name) AS techniques_used,
     max(cve.cvss_score) AS max_cvss
RETURN cve.id, max_cvss,
       size(exploiting_actors) AS apt_count,
       exploiting_actors[..5] AS top_actors,
       techniques_used[..3] AS common_techniques
ORDER BY apt_count DESC, max_cvss DESC
LIMIT 20
```

**Use Case**: Vulnerability prioritization, patch management

---

### Capability 7: Platform-Specific Threats

```cypher
// Analyze threats targeting specific platform
MATCH (tech:MitreTechnique)
WHERE $platform IN tech.platform
MATCH (actor:MitreActor {active: true})-[:USES_TECHNIQUE]->(tech)
WITH tech,
     count(DISTINCT actor) AS actor_count,
     collect(DISTINCT actor.name)[..5] AS top_actors
ORDER BY actor_count DESC
RETURN tech.id, tech.name, tech.tactic,
       actor_count,
       top_actors
LIMIT 25
```

**Parameters**: `{platform: "Windows"}`
**Use Case**: Platform-specific security hardening

---

### Capability 8: Probabilistic Threat Inference

```cypher
// Predict likely next techniques based on observed technique
MATCH (observed:MitreTechnique {id: $observedTechniqueId})
MATCH (actor:MitreActor)-[:USES_TECHNIQUE]->(observed)
MATCH (actor)-[:USES_TECHNIQUE]->(likely_next:MitreTechnique)
WHERE likely_next.id <> observed.id
WITH likely_next,
     count(DISTINCT actor) AS actor_count,
     587 AS total_actors  // Total MITRE actors
ORDER BY actor_count DESC
RETURN likely_next.id, likely_next.name, likely_next.tactic,
       actor_count AS likelihood_score,
       round(100.0 * actor_count / total_actors, 2) AS probability_percentage
LIMIT 15
```

**Parameters**: `{observedTechniqueId: "T1566"}` (Phishing)
**Use Case**: Predictive threat hunting, SIEM correlation rules

---

### MITRE Entity Statistics

```cypher
// Get comprehensive MITRE statistics
MATCH (tech:MitreTechnique)
WITH count(tech) AS techniques
MATCH (mit:MitreMitigation)
WITH techniques, count(mit) AS mitigations
MATCH (actor:MitreActor)
WITH techniques, mitigations, count(actor) AS actors, count(CASE WHEN actor.active THEN 1 END) AS active_actors
MATCH (soft:MitreSoftware)
WITH techniques, mitigations, actors, active_actors, count(soft) AS software
MATCH ()-[r:USES_TECHNIQUE]->()
WITH techniques, mitigations, actors, active_actors, software, count(r) AS uses_technique_rels
MATCH ()-[r:MITIGATES]->()
WITH techniques, mitigations, actors, active_actors, software, uses_technique_rels, count(r) AS mitigates_rels
RETURN {
  entities: {
    techniques: techniques,
    mitigations: mitigations,
    actors: actors,
    active_actors: active_actors,
    software: software,
    total: techniques + mitigations + actors + software
  },
  relationships: {
    uses_technique: uses_technique_rels,
    mitigates: mitigates_rels
  }
} AS mitre_statistics
```

---

### Actor Arsenal Comparison

```cypher
// Compare toolsets and techniques of multiple actors
MATCH (actor:MitreActor)
WHERE actor.name IN $actorNames
OPTIONAL MATCH (actor)-[:USES_TECHNIQUE]->(tech:MitreTechnique)
OPTIONAL MATCH (actor)-[:LEVERAGES_SOFTWARE]->(soft:MitreSoftware)
RETURN actor.name,
       actor.country,
       actor.sophistication,
       collect(DISTINCT tech.tactic) AS tactics,
       count(DISTINCT tech) AS technique_count,
       count(DISTINCT soft) AS software_count,
       collect(DISTINCT soft.name)[..5] AS sample_software
ORDER BY technique_count DESC
```

**Parameters**: `{actorNames: ["APT28", "APT29", "APT32"]}`
**Use Case**: Comparative threat analysis, attribution

---

### Technique Coverage Matrix

```cypher
// Generate technique coverage by tactic
MATCH (tech:MitreTechnique)
UNWIND tech.tactic AS tactic
WITH tactic, collect(tech) AS techniques
OPTIONAL MATCH (t)<-[:MITIGATES]-(mit:MitreMitigation)
WHERE t IN techniques
WITH tactic,
     size(techniques) AS total_techniques,
     count(DISTINCT mit) AS total_mitigations,
     size([t IN techniques WHERE size((t)<-[:MITIGATES]-()) > 0]) AS mitigated_count
RETURN tactic,
       total_techniques,
       mitigated_count,
       total_techniques - mitigated_count AS unmitigated_count,
       round(100.0 * mitigated_count / total_techniques, 2) AS coverage_percentage
ORDER BY coverage_percentage
```

**Use Case**: Security coverage assessment, gap analysis

---

## Backend MITRE Query API

### API Overview

The AEON backend provides specialized REST API endpoints for MITRE ATT&CK query capabilities with support for simple, intermediate, and advanced complexity levels.

**Base URL**: `http://localhost:8000/api/v1/mitre`

**Authentication**: Bearer token required for all endpoints

**Rate Limiting**: 100 requests/minute per API key

### Query Complexity Levels

| Complexity | Hops | Response Time | Use Case |
|------------|------|---------------|----------|
| **Simple** | 1-2 | < 100ms | Single-entity lookups, basic relationships |
| **Intermediate** | 3-4 | < 500ms | Multi-hop analysis, technique coverage |
| **Advanced** | 5+ | < 2s | Attack path discovery, probabilistic inference |

---

### Capability 1: Attack Path Discovery

**Endpoint**: `POST /api/v1/mitre/attack-paths`

**Description**: Discover attack paths from threat actor to critical CVEs

**Complexity**: Advanced (3-4 hops)

**Request Body**:
```json
{
  "actor_name": "APT28",
  "min_cvss_score": 9.0,
  "max_hops": 4,
  "limit": 10
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/v1/mitre/attack-paths \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "actor_name": "APT28",
    "min_cvss_score": 9.0,
    "max_hops": 4,
    "limit": 10
  }'
```

**Python Example**:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/mitre/attack-paths",
    headers={
        "Authorization": "Bearer YOUR_API_TOKEN",
        "Content-Type": "application/json"
    },
    json={
        "actor_name": "APT28",
        "min_cvss_score": 9.0,
        "max_hops": 4,
        "limit": 10
    }
)

paths = response.json()
for path in paths["data"]:
    print(f"Path length: {path['hops']}, CVE: {path['cve_id']}, CVSS: {path['cvss_score']}")
```

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "path_id": "path_001",
      "actor": "APT28",
      "path_length": 3,
      "hops": 3,
      "nodes": [
        {"type": "MitreActor", "id": "G0016", "name": "APT28"},
        {"type": "MitreTechnique", "id": "T1566", "name": "Phishing"},
        {"type": "CVE", "id": "CVE-2021-34527", "cvss_score": 9.8}
      ],
      "relationships": [
        {"type": "USES_TECHNIQUE", "confidence": 0.95},
        {"type": "EXPLOITS_CVE", "exploit_available": true}
      ],
      "cve_id": "CVE-2021-34527",
      "cvss_score": 9.8
    }
  ],
  "metadata": {
    "query_time_ms": 245,
    "total_paths": 7,
    "complexity": "advanced"
  }
}
```

---

### Capability 2: Defensive Gap Analysis

**Endpoint**: `GET /api/v1/mitre/defensive-gaps`

**Description**: Find critical techniques with insufficient mitigations

**Complexity**: Intermediate (2-3 hops)

**Query Parameters**:
- `tactics`: Comma-separated list (e.g., "Initial Access,Execution")
- `max_mitigations`: Maximum mitigation count threshold (default: 2)
- `limit`: Results limit (default: 20)

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/v1/mitre/defensive-gaps?tactics=Initial%20Access,Execution&max_mitigations=2&limit=20" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Python Example**:
```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/mitre/defensive-gaps",
    headers={"Authorization": "Bearer YOUR_API_TOKEN"},
    params={
        "tactics": "Initial Access,Execution",
        "max_mitigations": 2,
        "limit": 20
    }
)

gaps = response.json()
for technique in gaps["data"]:
    print(f"{technique['id']}: {technique['name']} - {technique['mitigation_count']} mitigations")
```

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "technique_id": "T1566",
      "name": "Phishing",
      "tactic": ["Initial Access"],
      "mitigation_count": 1,
      "available_mitigations": [
        {"id": "M1047", "name": "Audit", "effectiveness": "partial"}
      ],
      "gap_severity": "high",
      "recommended_actions": [
        "Implement email filtering",
        "User security awareness training"
      ]
    }
  ],
  "metadata": {
    "query_time_ms": 123,
    "total_gaps": 15,
    "complexity": "intermediate"
  }
}
```

---

### Capability 3: Threat Actor Profiling

**Endpoint**: `GET /api/v1/mitre/actor-profile/{actor_name}`

**Description**: Complete TTPs and toolset profile for threat actor

**Complexity**: Intermediate (2-3 hops)

**Path Parameters**:
- `actor_name`: Threat actor name (e.g., "APT28")

**cURL Example**:
```bash
curl -X GET http://localhost:8000/api/v1/mitre/actor-profile/APT28 \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Python Example**:
```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/mitre/actor-profile/APT28",
    headers={"Authorization": "Bearer YOUR_API_TOKEN"}
)

profile = response.json()["data"]
print(f"Actor: {profile['name']}")
print(f"Techniques: {profile['technique_count']}")
print(f"Software: {profile['software_count']}")
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "id": "G0016",
    "name": "APT28",
    "aliases": ["Fancy Bear", "Sofacy", "Sednit"],
    "country": "Russia",
    "sophistication": "advanced",
    "active": true,
    "technique_count": 142,
    "software_count": 18,
    "techniques": [
      {"id": "T1566", "name": "Phishing", "tactic": ["Initial Access"]},
      {"id": "T1003", "name": "Credential Dumping", "tactic": ["Credential Access"]}
    ],
    "software": [
      {"id": "S0002", "name": "Mimikatz", "type": "tool"},
      {"id": "S0363", "name": "Empire", "type": "tool"}
    ],
    "tactics_used": ["Initial Access", "Execution", "Persistence", "Credential Access"],
    "targets": ["Government", "Military", "Defense", "Media"]
  },
  "metadata": {
    "query_time_ms": 89,
    "complexity": "intermediate"
  }
}
```

---

### Capability 4: Mitigation Prioritization

**Endpoint**: `GET /api/v1/mitre/mitigation-priority`

**Description**: Find mitigations with broadest coverage against active threats

**Complexity**: Intermediate (3 hops)

**Query Parameters**:
- `active_only`: Filter for active actors only (default: true)
- `min_actor_coverage`: Minimum number of actors covered (default: 5)
- `limit`: Results limit (default: 20)

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/v1/mitre/mitigation-priority?active_only=true&min_actor_coverage=5&limit=20" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "mitigation_id": "M1047",
      "name": "Audit",
      "description": "Perform audits or scans of systems...",
      "actors_covered": 234,
      "techniques_covered": 87,
      "implementation_cost": "medium",
      "effectiveness": "significant",
      "roi_score": 9.2,
      "sample_techniques": [
        "T1003: Credential Dumping",
        "T1078: Valid Accounts",
        "T1098: Account Manipulation"
      ]
    }
  ],
  "metadata": {
    "query_time_ms": 156,
    "total_mitigations": 412,
    "complexity": "intermediate"
  }
}
```

---

### Capability 5: Software Capability Analysis

**Endpoint**: `GET /api/v1/mitre/software-capabilities/{software_name}`

**Description**: Analyze malware capabilities and available mitigations

**Complexity**: Simple (2 hops)

**cURL Example**:
```bash
curl -X GET http://localhost:8000/api/v1/mitre/software-capabilities/Mimikatz \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "software_id": "S0002",
    "name": "Mimikatz",
    "type": "tool",
    "platforms": ["Windows"],
    "technique_count": 12,
    "techniques": [
      {
        "id": "T1003",
        "name": "OS Credential Dumping",
        "tactic": ["Credential Access"],
        "mitigation_count": 3,
        "available_mitigations": [
          {"id": "M1027", "name": "Password Policies"},
          {"id": "M1043", "name": "Credential Access Protection"},
          {"id": "M1047", "name": "Audit"}
        ]
      }
    ],
    "detection_methods": ["Process Monitoring", "API Monitoring", "File Monitoring"]
  },
  "metadata": {
    "query_time_ms": 45,
    "complexity": "simple"
  }
}
```

---

### Capability 6: CVE Exploitation Chains

**Endpoint**: `GET /api/v1/mitre/cve-exploitation`

**Description**: Find CVEs exploited by multiple APT groups

**Complexity**: Advanced (4 hops)

**Query Parameters**:
- `min_cvss_score`: Minimum CVSS score (default: 7.0)
- `min_apt_count`: Minimum APT groups exploiting (default: 2)
- `sophistication`: Actor sophistication level (default: "advanced")
- `limit`: Results limit (default: 20)

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/v1/mitre/cve-exploitation?min_cvss_score=9.0&min_apt_count=2&limit=20" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "cve_id": "CVE-2021-44228",
      "cvss_score": 10.0,
      "apt_count": 15,
      "exploiting_actors": ["APT28", "APT29", "APT32", "Lazarus Group", "OilRig"],
      "techniques_used": ["T1190: Exploit Public-Facing Application", "T1210: Exploitation of Remote Services"],
      "exploit_available": true,
      "exploited_in_wild": true,
      "first_exploited": "2021-12-09",
      "threat_level": "critical"
    }
  ],
  "metadata": {
    "query_time_ms": 567,
    "total_cves": 234,
    "complexity": "advanced"
  }
}
```

---

### Capability 7: Platform-Specific Threats

**Endpoint**: `GET /api/v1/mitre/platform-threats/{platform}`

**Description**: Analyze threats targeting specific platform

**Complexity**: Intermediate (3 hops)

**Path Parameters**:
- `platform`: Target platform (e.g., "Windows", "Linux", "macOS")

**Query Parameters**:
- `active_only`: Filter for active actors (default: true)
- `limit`: Results limit (default: 25)

**cURL Example**:
```bash
curl -X GET http://localhost:8000/api/v1/mitre/platform-threats/Windows?active_only=true&limit=25 \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "technique_id": "T1003",
      "name": "OS Credential Dumping",
      "tactic": ["Credential Access"],
      "actor_count": 89,
      "top_actors": ["APT28", "APT29", "Lazarus Group", "OilRig", "FIN7"],
      "platform_specific_details": {
        "common_tools": ["Mimikatz", "ProcDump", "gsecdump"],
        "detection_signatures": ["LSASS memory access", "SAM registry access"]
      }
    }
  ],
  "metadata": {
    "query_time_ms": 198,
    "platform": "Windows",
    "total_techniques": 412,
    "complexity": "intermediate"
  }
}
```

---

### Capability 8: Probabilistic Threat Inference

**Endpoint**: `POST /api/v1/mitre/threat-inference`

**Description**: Predict likely next techniques based on observed TTPs

**Complexity**: Advanced (4-5 hops)

**Request Body**:
```json
{
  "observed_technique_id": "T1566",
  "top_n": 15
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/v1/mitre/threat-inference \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "observed_technique_id": "T1566",
    "top_n": 15
  }'
```

**Python Example**:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/mitre/threat-inference",
    headers={
        "Authorization": "Bearer YOUR_API_TOKEN",
        "Content-Type": "application/json"
    },
    json={
        "observed_technique_id": "T1566",
        "top_n": 15
    }
)

predictions = response.json()
for pred in predictions["data"]:
    print(f"{pred['technique_id']}: {pred['name']} - {pred['probability_percentage']}% likely")
```

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "technique_id": "T1059",
      "name": "Command and Scripting Interpreter",
      "tactic": ["Execution"],
      "likelihood_score": 234,
      "probability_percentage": 39.86,
      "confidence": "high",
      "reasoning": "234 out of 587 actors using T1566 also use T1059",
      "recommended_detections": [
        "PowerShell logging",
        "Command line monitoring",
        "Script execution analysis"
      ]
    },
    {
      "technique_id": "T1204",
      "name": "User Execution",
      "tactic": ["Execution"],
      "likelihood_score": 198,
      "probability_percentage": 33.73,
      "confidence": "high"
    }
  ],
  "metadata": {
    "observed_technique": "T1566: Phishing",
    "total_actors_using": 587,
    "query_time_ms": 423,
    "complexity": "advanced"
  }
}
```

---

### Authentication Setup

**Bearer Token Authentication**:

```bash
# Obtain API token (one-time setup)
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'

# Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}

# Use token in subsequent requests
curl -X GET http://localhost:8000/api/v1/mitre/actor-profile/APT28 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Python Token Management**:
```python
import requests
from datetime import datetime, timedelta

class MitreAPIClient:
    def __init__(self, base_url="http://localhost:8000", username=None, password=None):
        self.base_url = base_url
        self.token = None
        self.token_expiry = None
        if username and password:
            self.authenticate(username, password)

    def authenticate(self, username, password):
        """Obtain API token"""
        response = requests.post(
            f"{self.base_url}/api/v1/auth/token",
            json={"username": username, "password": password}
        )
        data = response.json()
        self.token = data["access_token"]
        self.token_expiry = datetime.now() + timedelta(seconds=data["expires_in"])

    def _get_headers(self):
        """Get headers with valid token"""
        if not self.token or datetime.now() >= self.token_expiry:
            raise Exception("Token expired or not set. Please authenticate.")
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_actor_profile(self, actor_name):
        """Get threat actor profile"""
        response = requests.get(
            f"{self.base_url}/api/v1/mitre/actor-profile/{actor_name}",
            headers=self._get_headers()
        )
        return response.json()

# Usage
client = MitreAPIClient(username="user", password="pass")
profile = client.get_actor_profile("APT28")
```

---

### Rate Limiting and Quotas

**Rate Limits**:
- **Free Tier**: 100 requests/minute, 10,000 requests/day
- **Standard Tier**: 500 requests/minute, 100,000 requests/day
- **Enterprise Tier**: 2,000 requests/minute, unlimited daily requests

**Rate Limit Headers**:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1699459200
```

**Rate Limit Exceeded Response**:
```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API rate limit exceeded. Retry after 2025-11-08T21:00:00Z",
    "retry_after": 45
  }
}
```

**Python Rate Limit Handling**:
```python
import time
import requests

def make_request_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()

        elif response.status_code == 429:  # Rate limit exceeded
            retry_after = int(response.headers.get("X-RateLimit-Reset", 60))
            print(f"Rate limit exceeded. Waiting {retry_after} seconds...")
            time.sleep(retry_after)

        else:
            response.raise_for_status()

    raise Exception("Max retries exceeded")
```

---

### Error Codes and Handling

**Standard Error Response Format**:
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional context"
    }
  }
}
```

**Common Error Codes**:

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| `INVALID_TOKEN` | 401 | Invalid or expired token | Re-authenticate |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests | Wait and retry |
| `RESOURCE_NOT_FOUND` | 404 | Actor/technique not found | Check entity ID |
| `INVALID_PARAMETER` | 400 | Invalid query parameter | Review API docs |
| `DATABASE_ERROR` | 500 | Neo4j connection failure | Contact support |
| `TIMEOUT` | 504 | Query timeout exceeded | Reduce complexity |

**Error Handling Examples**:

```python
import requests

def handle_api_errors(response):
    """Handle common API errors"""
    if response.status_code == 200:
        return response.json()

    error_data = response.json()
    error_code = error_data.get("error", {}).get("code")

    if error_code == "INVALID_TOKEN":
        print("Authentication failed. Please check your credentials.")
        # Re-authenticate

    elif error_code == "RATE_LIMIT_EXCEEDED":
        retry_after = error_data["error"].get("retry_after", 60)
        print(f"Rate limit exceeded. Retry after {retry_after} seconds.")
        # Implement backoff

    elif error_code == "RESOURCE_NOT_FOUND":
        print("Entity not found. Please check the ID or name.")
        return None

    else:
        print(f"API error: {error_data['error']['message']}")
        response.raise_for_status()

# Usage
response = requests.get(
    "http://localhost:8000/api/v1/mitre/actor-profile/INVALID",
    headers={"Authorization": "Bearer TOKEN"}
)
result = handle_api_errors(response)
```

---

### Performance and SLA

**Service Level Agreement**:
- **Availability**: 99.9% uptime
- **Response Time**:
  - Simple queries: < 100ms (P95)
  - Intermediate queries: < 500ms (P95)
  - Advanced queries: < 2s (P95)
- **Data Freshness**: Updated daily from MITRE ATT&CK v14.1

**Performance Optimization Tips**:
1. **Use caching**: Cache frequently accessed data client-side
2. **Limit results**: Use `limit` parameter to reduce response size
3. **Filter early**: Apply filters to reduce query complexity
4. **Batch requests**: Combine multiple queries when possible
5. **Use webhooks**: Subscribe to data updates instead of polling

---

### Troubleshooting Guide

#### Connection Issues

**Problem**: Cannot connect to API endpoint

**Solution**:
```bash
# 1. Verify service is running
docker ps | grep aeon-backend

# 2. Test connectivity
curl -v http://localhost:8000/health

# 3. Check firewall rules
sudo iptables -L | grep 8000

# 4. Verify network configuration
docker network inspect openspg-network
```

#### Authentication Failures

**Problem**: 401 Unauthorized errors

**Solution**:
```python
# 1. Verify token is valid and not expired
import jwt
token = "YOUR_TOKEN"
decoded = jwt.decode(token, options={"verify_signature": False})
print(f"Expires: {decoded['exp']}")

# 2. Check token format
# Token must start with "Bearer " in Authorization header
headers = {"Authorization": f"Bearer {token}"}

# 3. Re-authenticate if expired
response = requests.post(
    "http://localhost:8000/api/v1/auth/token",
    json={"username": "user", "password": "pass"}
)
new_token = response.json()["access_token"]
```

#### Query Timeout Errors

**Problem**: 504 Gateway Timeout on complex queries

**Solution**:
1. **Reduce `max_hops`**: Lower hop count for path queries
2. **Add `limit`**: Restrict result set size
3. **Use filters**: Apply filters to reduce search space
4. **Cache results**: Cache expensive query results

```python
# Instead of:
response = requests.post(
    "http://localhost:8000/api/v1/mitre/attack-paths",
    json={"actor_name": "APT28", "max_hops": 10}  # Too complex
)

# Use:
response = requests.post(
    "http://localhost:8000/api/v1/mitre/attack-paths",
    json={
        "actor_name": "APT28",
        "max_hops": 4,  # Reduced
        "limit": 10,    # Limited results
        "min_cvss_score": 7.0  # Filtered
    }
)
```

#### Data Inconsistency

**Problem**: Query returns unexpected or missing data

**Solution**:
```bash
# 1. Verify MITRE data is loaded
curl http://localhost:8000/api/v1/mitre/stats

# Expected response:
{
  "techniques": 832,
  "mitigations": 412,
  "actors": 587,
  "software": 220,
  "relationships": 40886
}

# 2. Check database indexes
docker exec openspg-neo4j cypher-shell -u neo4j -p neo4j@openspg \
  "SHOW INDEXES"

# 3. Verify entity exists
curl http://localhost:8000/api/v1/mitre/actor-profile/APT28
```

---

## Security Best Practices

### Parameter Usage

```cypher
// ALWAYS use parameters for user input (prevents injection)
// BAD - vulnerable to injection
MATCH (e:Entity)
WHERE e.name = '" + userInput + "'
RETURN e

// GOOD - safe with parameters
MATCH (e:Entity)
WHERE e.name = $name
RETURN e
// Parameters: {name: userInput}
```

### Access Control

```cypher
// Create read-only user (requires Enterprise Edition)
CREATE USER analyst SET PASSWORD 'secure_password';
GRANT TRAVERSE ON GRAPH neo4j NODES * TO analyst;
GRANT READ {*} ON GRAPH neo4j NODES * TO analyst;
GRANT TRAVERSE ON GRAPH neo4j RELATIONSHIPS * TO analyst;
GRANT READ {*} ON GRAPH neo4j RELATIONSHIPS * TO analyst;

// Revoke write permissions
DENY WRITE ON GRAPH neo4j TO analyst;
```

### Query Resource Limits

```cypher
// Set transaction timeout (in Neo4j config)
// dbms.transaction.timeout=30s

// Add query timeout in application
// Python example:
# session.run(query, parameters, timeout=30)

// Limit query complexity
// dbms.query.max_memory=4GB
```

---

## Error Handling

### Common Error Patterns

```cypher
// Handle missing data with OPTIONAL MATCH
MATCH (e:Entity {id: $id})
OPTIONAL MATCH (e)-[r]->(related)
RETURN e, collect(related) AS related_entities;

// Use coalesce for default values
MATCH (e:Entity)
RETURN e.name, coalesce(e.confidence, 0.5) AS confidence;

// Check existence before operations
MATCH (e:Entity {id: $id})
WITH count(e) AS exists
WHERE exists > 0
MATCH (e:Entity {id: $id})
SET e.updated = datetime()
RETURN e;
```

### Transaction Error Handling (Python)

```python
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, TransientError

def safe_query(driver, query, parameters=None, max_retries=3):
    """Execute query with retry logic"""
    for attempt in range(max_retries):
        try:
            with driver.session(database="neo4j") as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except TransientError as e:
            if attempt == max_retries - 1:
                raise
            print(f"Transient error, retrying... ({e})")
            time.sleep(2 ** attempt)  # Exponential backoff
        except ServiceUnavailable as e:
            print(f"Database unavailable: {e}")
            raise
        except Exception as e:
            print(f"Query failed: {e}")
            raise
    return []
```

---

## Performance Benchmarks

### Query Performance Guidelines

| Query Type | Expected Time | Optimization |
|------------|---------------|--------------|
| Simple node lookup (indexed) | < 10ms | Use indexes on lookup properties |
| Pattern match (2-3 hops) | < 100ms | Limit result set, use indexes |
| Full graph scan | 1-10s | Avoid if possible, use LIMIT |
| Aggregation (1M nodes) | 100-500ms | Use indexes, filter early |
| Shortest path (< 10 hops) | 50-200ms | Limit max depth |
| Graph algorithm | 1-60s | Consider APOC procedures |

### Monitoring Queries

```cypher
// Current running queries
CALL dbms.listQueries()
YIELD queryId, query, elapsedTimeMillis, status
WHERE elapsedTimeMillis > 1000
RETURN queryId, query, elapsedTimeMillis, status
ORDER BY elapsedTimeMillis DESC;

// Kill slow query
CALL dbms.killQuery($queryId);

// Database statistics
CALL apoc.meta.stats()
YIELD nodeCount, relCount, labelCount, relTypeCount
RETURN nodeCount, relCount, labelCount, relTypeCount;

// Memory usage
CALL dbms.listPools()
YIELD pool, used, total
RETURN pool, used, total;
```

---

## Troubleshooting

### Common Issues

#### Query Too Slow
```cypher
// Check query plan
PROFILE MATCH (e:Entity)-[r]->(related)
WHERE e.type = "vulnerability"
RETURN e, r, related;

// Add missing index
CREATE INDEX entity_type_idx FOR (n:Entity) ON (n.type);

// Reduce result set
MATCH (e:Entity {type: "vulnerability"})-[r]->(related)
RETURN e, r, related
LIMIT 100;
```

#### Out of Memory
```cypher
// Free memory with WITH
MATCH (d:Document)
WITH d.id AS doc_id
MATCH (d:Document {id: doc_id})-[:CONTAINS]->(e:Entity)
RETURN doc_id, collect(e.name) AS entities;

// Process in batches
MATCH (e:Entity)
WHERE e.type = "vulnerability"
WITH collect(e) AS entities
UNWIND entities[0..1000] AS entity
RETURN entity;
```

#### Connection Issues
```bash
# Test Bolt connection
docker exec -it openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg"

# Check Neo4j status
docker exec openspg-neo4j neo4j status

# Review logs
docker logs openspg-neo4j --tail 100
```

---

## Version History

- v2.0.0 (2025-11-08): Added MITRE ATT&CK query patterns
  - 8 key capability query examples
  - MITRE entity statistics queries
  - Actor arsenal comparison
  - Technique coverage matrix
  - Attack path discovery patterns
  - Probabilistic threat inference
- v1.0.0 (2025-11-03): Initial comprehensive Cypher API documentation
  - Complete query syntax reference
  - CRUD operations with examples
  - Aggregation and analytics patterns
  - Graph algorithms
  - Performance optimization
  - AEON UI integration patterns
  - Python driver examples

---

## References & Sources

- Neo4j Cypher Manual: https://neo4j.com/docs/cypher-manual/current/ (Accessed: 2025-11-03)
- Neo4j Python Driver: https://neo4j.com/docs/python-manual/current/ (Accessed: 2025-11-03)
- Neo4j HTTP API: https://neo4j.com/docs/http-api/current/ (Accessed: 2025-11-03)
- Graph Data Science Library: https://neo4j.com/docs/graph-data-science/ (Accessed: 2025-11-03)
- AEON knowledge graph statistics (2025-11-03 17:21:26 CST)

---

*Cypher Query API Documentation v1.0.0 | Comprehensive Reference | Production Ready*
*Updated: 2025-11-03 17:21:26 CST | Status: ACTIVE*
