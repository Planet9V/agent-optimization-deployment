---
title: Knowledge Graph Incarnation (Part 1 of 2)
category: 03_Incarnations
last_updated: 2025-10-25
line_count: 450
status: published
tags: [neocoder, mcp, documentation]
---


# Knowledge Graph Incarnation

[← Back to Coding](02_Coding.md) | [Next: Code Analysis →](04_Code_Analysis.md)

## Overview

The **Knowledge Graph Incarnation** is designed for building and querying semantic knowledge bases. It provides tools for creating entities, relationships, and domain models stored in Neo4j's graph structure.

**Incarnation Type**: `knowledge_graph`
**Version**: 1.0.0
**Primary Use Cases**: Knowledge base construction, semantic modeling, relationship mapping

## Core Capabilities

### Entity Management
- Create and configure knowledge entities
- Define entity types and properties
- Track entity metadata and provenance
- Query entities by type and attributes

### Relationship Modeling
- Create typed relationships between entities
- Define relationship properties
- Query relationship patterns
- Map domain semantics

### Knowledge Querying
- Execute semantic queries
- Traverse knowledge graphs
- Discover related concepts
- Analyze knowledge structure

### Domain Modeling
- Build domain-specific taxonomies
- Create hierarchical knowledge structures
- Model complex relationships
- Support multiple knowledge domains

## Schema

### Node Types

**KnowledgeEntity**:
```cypher
CREATE (entity:KnowledgeEntity {
  id: randomUUID(),
  type: 'concept',
  name: 'Machine Learning',
  description: 'Field of AI focused on learning from data',
  domain: 'artificial_intelligence',
  created: datetime(),
  updated: datetime(),
  properties: {
    definition: 'Statistical learning algorithms',
    scope: 'supervised and unsupervised learning'
  },
  tags: ['ai', 'data-science']
})
```

**Concept**:
```cypher
CREATE (concept:Concept {
  id: randomUUID(),
  name: 'Neural Network',
  description: 'Computing system inspired by biological neural networks',
  category: 'algorithm',
  abstraction_level: 'high',
  created: datetime()
})
```

**Citation**:
```cypher
CREATE (citation:Citation {
  id: randomUUID(),
  source: 'Wikipedia',
  title: 'Machine Learning Overview',
  url: 'https://en.wikipedia.org/wiki/Machine_learning',
  retrieved: datetime(),
  credibility: 'high'
})
```

### Relationships

**Semantic Relationships**:
```cypher
// Entity associations
(entity1:KnowledgeEntity)-[:RELATES_TO {strength: 0.8}]->(entity2:KnowledgeEntity)

// Hierarchical relationships
(child:KnowledgeEntity)-[:IS_A]->(parent:KnowledgeEntity)
(part:KnowledgeEntity)-[:PART_OF]->(whole:KnowledgeEntity)

// Dependency relationships
(dependent:KnowledgeEntity)-[:DEPENDS_ON]->(dependency:KnowledgeEntity)

// Attribution relationships
(entity:KnowledgeEntity)-[:CITED_BY]->(citation:Citation)
(entity:KnowledgeEntity)-[:SUPPORTS]->(claim:KnowledgeEntity)
(entity1:KnowledgeEntity)-[:CONTRADICTS]->(entity2:KnowledgeEntity)
```

## Available Tools

### create_knowledge_entity

Creates a new knowledge entity in the graph.

**Signature**:
```python
async def create_knowledge_entity(
    name: str,
    entity_type: str,
    description: str = "",
    domain: str = None,
    properties: dict = None,
    tags: list[str] = None
) -> dict
```

**Parameters**:
- `name` (string, required) - Entity name
- `entity_type` (string, required) - Entity type (concept, fact, process, etc.)
- `description` (string, optional) - Entity description
- `domain` (string, optional) - Knowledge domain
- `properties` (dict, optional) - Additional properties
- `tags` (list[string], optional) - Categorization tags

**Example**:
```python
entity = await create_knowledge_entity(
    name="Deep Learning",
    entity_type="concept",
    description="Neural networks with multiple layers",
    domain="artificial_intelligence",
    properties={
        "definition": "ML using multi-layer neural networks",
        "applications": ["computer vision", "NLP"]
    },
    tags=["ai", "neural-networks"]
)
```

### create_relationship

Creates a typed relationship between entities.

**Signature**:
```python
async def create_relationship(
    source_id: str,
    target_id: str,
    relationship_type: str,
    properties: dict = None
) -> dict
```

**Parameters**:
- `source_id` (string, required) - Source entity UUID
- `target_id` (string, required) - Target entity UUID
- `relationship_type` (string, required) - Relationship type
- `properties` (dict, optional) - Relationship properties

**Relationship Types**:
- `RELATES_TO` - General association
- `IS_A` - Type hierarchy
- `PART_OF` - Composition
- `DEPENDS_ON` - Dependency
- `CONTRADICTS` - Conflict
- `SUPPORTS` - Evidence

**Example**:
```python
rel = await create_relationship(
    source_id="deep-learning-uuid",
    target_id="machine-learning-uuid",
    relationship_type="IS_A",
    properties={
        "strength": 1.0,
        "since": "2006"
    }
)
```

### query_knowledge_graph

Executes Cypher queries against the knowledge graph.

**Signature**:
```python
async def query_knowledge_graph(
    cypher_query: str,
    parameters: dict = None
) -> dict
```

**Parameters**:
- `cypher_query` (string, required) - Cypher query
- `parameters` (dict, optional) - Query parameters

**Returns**:
```json
{
  "success": true,
  "results": [
    {"entity": {...}, "relationships": [...]}
  ],
  "result_count": 15
}
```

**Example**:
```python
results = await query_knowledge_graph(
    cypher_query="""
        MATCH (concept:KnowledgeEntity {type: 'concept'})
        WHERE concept.domain = $domain
        RETURN concept.name as name, concept.description as desc
    """,
    parameters={"domain": "artificial_intelligence"}
)
```

### get_entity_neighbors

Finds entities related to a given entity.

**Signature**:
```python
async def get_entity_neighbors(
    entity_id: str,
    relationship_types: list[str] = None,
    max_depth: int = 1,
    limit: int = 50
) -> dict
```

**Parameters**:
- `entity_id` (string, required) - Entity UUID
- `relationship_types` (list[string], optional) - Filter by relationship types
- `max_depth` (int, optional) - Traversal depth (1-3)
- `limit` (int, optional) - Max results

**Returns**:
```json
{
  "success": true,
  "entity": {...},
  "neighbors": [
    {
      "entity": {...},
      "relationship": "IS_A",
      "distance": 1
    }
  ]
}
```

### find_path_between_entities

Finds relationship paths between two entities.

**Signature**:
```python
async def find_path_between_entities(
    source_id: str,
    target_id: str,
    max_length: int = 5
) -> dict
```

**Returns**:
```json
{
  "success": true,
  "paths": [
    {
      "length": 2,
      "entities": ["Entity A", "Entity B", "Entity C"],
      "relationships": ["IS_A", "RELATES_TO"]
    }
  ]
}
```

## Common Workflows

### Building a Domain Knowledge Base

```python
# 1. Create top-level domain entity
domain_entity = await create_knowledge_entity(
    name="Artificial Intelligence",
    entity_type="domain",
    description="Field of computer science creating intelligent agents"
)

# 2. Create sub-domain entities
ml_entity = await create_knowledge_entity(
    name="Machine Learning",
    entity_type="concept",
    description="AI systems that learn from data",
    domain="artificial_intelligence"
)

dl_entity = await create_knowledge_entity(
    name="Deep Learning",
    entity_type="concept",
    description="ML using neural networks",
    domain="artificial_intelligence"
)

# 3. Create hierarchical relationships
await create_relationship(
    source_id=ml_entity["entity_id"],
    target_id=domain_entity["entity_id"],
    relationship_type="PART_OF"
)

await create_relationship(
    source_id=dl_entity["entity_id"],
    target_id=ml_entity["entity_id"],
    relationship_type="IS_A"
)

# 4. Add citations
citation = await create_citation(
    source="Deep Learning Book",
    title="Deep Learning by Goodfellow et al.",
    url="https://www.deeplearningbook.org"
)

await create_relationship(
    source_id=dl_entity["entity_id"],
    target_id=citation["citation_id"],
    relationship_type="CITED_BY"
)
```

### Semantic Query Workflow

```python
# 1. Find concepts in a domain
concepts = await query_knowledge_graph(
    cypher_query="""
        MATCH (concept:KnowledgeEntity {type: 'concept'})
        WHERE concept.domain = $domain
        RETURN concept
        ORDER BY concept.name
    """,
    parameters={"domain": "artificial_intelligence"}
)

# 2. Explore relationships from a concept
neighbors = await get_entity_neighbors(
    entity_id="deep-learning-uuid",
    relationship_types=["IS_A", "RELATES_TO"],
    max_depth=2
)

# 3. Find paths between concepts
path = await find_path_between_entities(
    source_id="neural-network-uuid",
    target_id="backpropagation-uuid",
    max_length=3
)

# 4. Analyze knowledge structure
analysis = await query_knowledge_graph(
    cypher_query="""
        MATCH (e:KnowledgeEntity)
        RETURN e.domain as domain,
               count(e) as entity_count,
               collect(DISTINCT e.type) as types
        ORDER BY entity_count DESC
    """
)
```

## Cypher Query Patterns

### Entity Queries

**Find Entities by Type and Domain**:
```cypher
MATCH (e:KnowledgeEntity)
WHERE e.type = $entity_type
  AND e.domain = $domain
RETURN e.name as name,
       e.description as description,
       e.tags as tags
ORDER BY e.name
```

**Get Entity with Citations**:
```cypher
MATCH (entity:KnowledgeEntity {id: $entity_id})
OPTIONAL MATCH (entity)-[:CITED_BY]->(citation:Citation)
RETURN entity,
       collect(citation) as citations
```

### Relationship Queries

**Find Related Concepts**:
```cypher
MATCH (concept:KnowledgeEntity {id: $concept_id})
MATCH path = (concept)-[:RELATES_TO*1..2]-(related:KnowledgeEntity)
RETURN DISTINCT related.name as related_concept,
       length(path) as distance,
       [rel IN relationships(path) | type(rel)] as relationship_types
ORDER BY distance, related_concept
```

**Explore Hierarchies**:
```cypher
MATCH path = (child:KnowledgeEntity)-[:IS_A*1..5]->(parent:KnowledgeEntity)
WHERE child.id = $entity_id
RETURN [node IN nodes(path) | node.name] as hierarchy,
       length(path) as depth
ORDER BY depth DESC
LIMIT 1
```

### Knowledge Analysis

**Domain Statistics**:
```cypher
MATCH (e:KnowledgeEntity)
WHERE e.domain IS NOT NULL
RETURN e.domain as domain,
       count(e) as entity_count,
       collect(DISTINCT e.type) as entity_types,
       count(DISTINCT e.type) as type_diversity
ORDER BY entity_count DESC
```

**Find Knowledge Gaps**:
```cypher
// Entities without citations
MATCH (e:KnowledgeEntity)
WHERE NOT (e)-[:CITED_BY]->(:Citation)
  AND e.type = 'concept'
RETURN e.name as uncited_concept,
       e.domain as domain
```
