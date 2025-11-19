---
title: Common Cypher Patterns (Part 1 of 2)
category: 08_Reference
last_updated: 2025-10-25
line_count: 430
status: published
tags: [neocoder, mcp, documentation]
---


# Common Cypher Patterns

[← Back to Contributing](../07_Development/03_Contributing.md) | [Next: API Reference →](02_API_Reference.md)

## Overview

This reference provides commonly-used Cypher query patterns for NeoCoder operations. All patterns are tested and optimized for performance.

## Entity Operations

### Create Entity

```cypher
// Create knowledge entity with full metadata
CREATE (e:KnowledgeEntity {
  id: randomUUID(),
  name: $name,
  type: $entity_type,
  description: $description,
  domain: $domain,
  properties: $properties,
  tags: $tags,
  created: datetime(),
  updated: datetime()
})
RETURN e.id as entity_id, e.name as name
```

### Find Entity by ID

```cypher
MATCH (e:KnowledgeEntity {id: $entity_id})
RETURN e
```

### Find Entity by Name

```cypher
MATCH (e:KnowledgeEntity)
WHERE e.name = $name
RETURN e
LIMIT 1
```

### Update Entity

```cypher
MATCH (e:KnowledgeEntity {id: $entity_id})
SET e.description = $description,
    e.properties = $properties,
    e.updated = datetime()
RETURN e
```

### Delete Entity

```cypher
MATCH (e:KnowledgeEntity {id: $entity_id})
DETACH DELETE e
```

## Relationship Operations

### Create Relationship

```cypher
MATCH (source:KnowledgeEntity {id: $source_id})
MATCH (target:KnowledgeEntity {id: $target_id})
CREATE (source)-[r:RELATES_TO {
  type: $relationship_type,
  description: $description,
  strength: $strength,
  created: datetime()
}]->(target)
RETURN r
```

### Find Relationships

```cypher
// All relationships for an entity
MATCH (e:KnowledgeEntity {id: $entity_id})-[r]-(related)
RETURN e, r, related

// Specific relationship type
MATCH (e:KnowledgeEntity {id: $entity_id})-[r:RELATES_TO]-(related)
WHERE r.type = $relationship_type
RETURN related

// Outgoing relationships only
MATCH (e:KnowledgeEntity {id: $entity_id})-[r:RELATES_TO]->(related)
RETURN related

// Incoming relationships only
MATCH (e:KnowledgeEntity {id: $entity_id})<-[r:RELATES_TO]-(related)
RETURN related
```

### Update Relationship

```cypher
MATCH (source)-[r:RELATES_TO {type: $relationship_type}]->(target)
WHERE source.id = $source_id AND target.id = $target_id
SET r.strength = $strength,
    r.description = $description,
    r.updated = datetime()
RETURN r
```

### Delete Relationship

```cypher
MATCH (source)-[r:RELATES_TO]->(target)
WHERE source.id = $source_id AND target.id = $target_id AND r.type = $relationship_type
DELETE r
```

## Graph Traversal

### Find Neighbors

```cypher
// Direct neighbors (1 hop)
MATCH (start:KnowledgeEntity {id: $entity_id})-[r]-(neighbor:KnowledgeEntity)
RETURN DISTINCT neighbor, type(r) as relationship_type

// Two hops away
MATCH (start:KnowledgeEntity {id: $entity_id})-[*1..2]-(related:KnowledgeEntity)
RETURN DISTINCT related

// Variable depth (up to N hops)
MATCH path = (start:KnowledgeEntity {id: $entity_id})-[*1..$max_depth]-(related:KnowledgeEntity)
RETURN related, length(path) as distance
ORDER BY distance
LIMIT $limit
```

### Shortest Path

```cypher
MATCH (start:KnowledgeEntity {id: $start_id})
MATCH (end:KnowledgeEntity {id: $end_id})
MATCH path = shortestPath((start)-[*]-(end))
RETURN path, length(path) as path_length
```

### All Paths Between Entities

```cypher
MATCH (start:KnowledgeEntity {id: $start_id})
MATCH (end:KnowledgeEntity {id: $end_id})
MATCH path = (start)-[*1..$max_depth]-(end)
RETURN path, length(path) as path_length
ORDER BY path_length
LIMIT $limit
```

### Find Connected Component

```cypher
// All entities connected to starting entity
MATCH (start:KnowledgeEntity {id: $entity_id})
MATCH path = (start)-[*]-(connected:KnowledgeEntity)
RETURN DISTINCT connected
```

## Project Operations

### Create Project

```cypher
CREATE (p:Project {
  id: randomUUID(),
  name: $name,
  description: $description,
  root_path: $root_path,
  metadata: $metadata,
  tags: $tags,
  created: datetime(),
  updated: datetime()
})
RETURN p.id as project_id
```

### Add File to Project

```cypher
MATCH (p:Project {id: $project_id})
MERGE (f:File {path: $file_path})
ON CREATE SET f.id = randomUUID(),
              f.created = datetime()
ON MATCH SET f.updated = datetime()
MERGE (p)-[r:HAS_FILE]->(f)
RETURN f.id as file_id
```

### Get Project Files

```cypher
MATCH (p:Project {id: $project_id})-[:HAS_FILE]->(f:File)
RETURN f
ORDER BY f.path
```

### Get Project with Files and Entities

```cypher
MATCH (p:Project {id: $project_id})
OPTIONAL MATCH (p)-[:HAS_FILE]->(f:File)
OPTIONAL MATCH (f)-[:DEFINES]->(e:CodeEntity)
RETURN p,
       collect(DISTINCT f) as files,
       collect(DISTINCT e) as entities
```

## Workflow Operations

### Create Workflow Execution

```cypher
MATCH (p:Project {id: $project_id})
CREATE (exec:WorkflowExecution {
  id: randomUUID(),
  workflow_keyword: $keyword,
  project_id: $project_id,
  status: 'in_progress',
  parameters: $parameters,
  started: datetime()
})
CREATE (p)-[:HAS_EXECUTION]->(exec)
RETURN exec.id as execution_id
```

### Update Workflow Status

```cypher
MATCH (exec:WorkflowExecution {id: $execution_id})
SET exec.status = $status,
    exec.completed = datetime(),
    exec.result = $result
RETURN exec
```

### Get Workflow History

```cypher
MATCH (p:Project {id: $project_id})-[:HAS_EXECUTION]->(exec:WorkflowExecution)
RETURN exec
ORDER BY exec.started DESC
LIMIT $limit
```

## Search and Filter

### Filter by Domain

```cypher
MATCH (e:KnowledgeEntity)
WHERE e.domain = $domain
RETURN e
ORDER BY e.created DESC
LIMIT $limit
```

### Filter by Type

```cypher
MATCH (e:KnowledgeEntity)
WHERE e.type = $entity_type
RETURN e
LIMIT $limit
```

### Filter by Tags

```cypher
MATCH (e:KnowledgeEntity)
WHERE $tag IN e.tags
RETURN e
LIMIT $limit
```

### Full-text Search (requires index)

```cypher
CALL db.index.fulltext.queryNodes('entity_search', $search_text)
YIELD node, score
RETURN node, score
ORDER BY score DESC
LIMIT $limit
```

### Complex Filter

```cypher
MATCH (e:KnowledgeEntity)
WHERE e.domain = $domain
  AND e.type IN $types
  AND ANY(tag IN e.tags WHERE tag IN $required_tags)
  AND e.created >= datetime($start_date)
RETURN e
ORDER BY e.updated DESC
LIMIT $limit
```

## Aggregation Patterns

### Count Entities by Type

```cypher
MATCH (e:KnowledgeEntity)
RETURN e.type as type, count(e) as count
ORDER BY count DESC
```

### Count Entities by Domain

```cypher
MATCH (e:KnowledgeEntity)
RETURN e.domain as domain, count(e) as count
ORDER BY count DESC
```

### Relationship Statistics

```cypher
MATCH (e:KnowledgeEntity)-[r:RELATES_TO]-()
RETURN e.name as entity,
       count(r) as relationship_count
ORDER BY relationship_count DESC
LIMIT $limit
```

### Average Relationship Strength

```cypher
MATCH ()-[r:RELATES_TO]->()
RETURN avg(r.strength) as average_strength,
       min(r.strength) as min_strength,
       max(r.strength) as max_strength
```

## Advanced Patterns

### Find Entities with No Relationships

```cypher
MATCH (e:KnowledgeEntity)
WHERE NOT (e)-[]-()
RETURN e
```

### Find Most Connected Entities

```cypher
MATCH (e:KnowledgeEntity)-[r]-()
RETURN e, count(r) as connection_count
ORDER BY connection_count DESC
LIMIT $limit
```

### Find Similar Entities by Shared Connections

```cypher
MATCH (e1:KnowledgeEntity {id: $entity_id})-[]-(shared)-[]-(e2:KnowledgeEntity)
WHERE e1 <> e2
RETURN e2, count(shared) as shared_connections
ORDER BY shared_connections DESC
LIMIT $limit
```

### Detect Circular Dependencies

```cypher
MATCH path = (e:KnowledgeEntity)-[:RELATES_TO*]->(e)
RETURN path
LIMIT $limit
```

### Find Bridge Entities

```cypher
// Entities that connect different clusters
MATCH (e:KnowledgeEntity)
MATCH (e)-[]-(n1:KnowledgeEntity)
MATCH (e)-[]-(n2:KnowledgeEntity)
WHERE n1.domain <> n2.domain
  AND NOT (n1)-[]-(n2)
RETURN e, count(DISTINCT n1.domain) as domains_connected
ORDER BY domains_connected DESC
LIMIT $limit
```

## Citation Network

### Create Citation

```cypher
MATCH (entity:KnowledgeEntity {id: $entity_id})
CREATE (citation:Citation {
  id: randomUUID(),
  title: $title,
  authors: $authors,
  year: $year,
  doi: $doi,
  url: $url,
  created: datetime()
})
CREATE (entity)-[:CITED_BY]->(citation)
RETURN citation
```

### Find All Citations

```cypher
MATCH (e:KnowledgeEntity {id: $entity_id})-[:CITED_BY]->(c:Citation)
RETURN c
ORDER BY c.year DESC
```

### Citation Chain

```cypher
// Follow citation chain
MATCH (start:KnowledgeEntity {id: $entity_id})
MATCH path = (start)-[:CITED_BY|:DERIVED_FROM*1..$depth]->(related)
RETURN path
```
