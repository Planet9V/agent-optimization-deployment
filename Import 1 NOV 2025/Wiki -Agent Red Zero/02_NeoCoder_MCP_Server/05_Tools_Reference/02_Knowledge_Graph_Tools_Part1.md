---
title: Knowledge Graph Tools Reference (Part 1)
category: 05_Tools_Reference
last_updated: 2025-10-25
line_count: 481
status: published
tags: [neocoder, mcp, documentation]
---

# Knowledge Graph Tools Reference

[← Back to Core Tools](01_Core_Tools.md) | [Next: Code Analysis Tools →](03_Code_Analysis_Tools.md)

## Overview

Knowledge Graph tools enable semantic entity management, relationship creation, and knowledge querying in Neo4j. Available in the `knowledge_graph` incarnation.

## Entity Management

### create_knowledge_entity

Creates a semantic knowledge entity.

**Signature**:
```python
async def create_knowledge_entity(
    name: str,
    entity_type: str,
    description: str = "",
    domain: str | None = None,
    properties: dict | None = None,
    tags: list[str] | None = None
) -> dict
```

**Parameters**:
- `name` - Entity name (unique within domain)
- `entity_type` - Type: concept, fact, process, method, principle, etc.
- `description` - Entity description
- `domain` - Knowledge domain (e.g., "artificial_intelligence", "biology")
- `properties` - Additional attributes
- `tags` - Categorization tags

**Returns**:
```json
{
  "success": true,
  "entity_id": "uuid",
  "entity": {
    "id": "uuid",
    "name": "Deep Learning",
    "type": "concept",
    "domain": "artificial_intelligence"
  }
}
```

**Example**:
```python
entity = await create_knowledge_entity(
    name="Transformer Architecture",
    entity_type="concept",
    description="Attention-based neural network architecture",
    domain="artificial_intelligence",
    properties={
        "introduced": "2017",
        "key_innovation": "self-attention mechanism"
    },
    tags=["neural-networks", "nlp", "deep-learning"]
)
```

---

### get_entity_by_id

Retrieves entity by UUID.

**Signature**:
```python
async def get_entity_by_id(
    entity_id: str,
    include_relationships: bool = False
) -> dict
```

---

### get_entity_by_name

Retrieves entity by name.

**Signature**:
```python
async def get_entity_by_name(
    name: str,
    domain: str | None = None
) -> dict
```

---

### update_entity

Updates entity properties.

**Signature**:
```python
async def update_entity(
    entity_id: str,
    properties: dict | None = None,
    tags: list[str] | None = None,
    description: str | None = None
) -> dict
```

---

### delete_entity

Deletes an entity and its relationships.

**Signature**:
```python
async def delete_entity(
    entity_id: str,
    cascade: bool = False
) -> dict
```

**Parameters**:
- `entity_id` - Entity to delete
- `cascade` - Delete related entities if orphaned

---

## Relationship Management

### create_relationship

Creates typed relationship between entities.

**Signature**:
```python
async def create_relationship(
    source_id: str,
    target_id: str,
    relationship_type: str,
    properties: dict | None = None
) -> dict
```

**Parameters**:
- `source_id` - Source entity UUID
- `target_id` - Target entity UUID
- `relationship_type` - Type: RELATES_TO, IS_A, PART_OF, DEPENDS_ON, SUPPORTS, CONTRADICTS
- `properties` - Relationship metadata (strength, confidence, etc.)

**Relationship Types**:
- `RELATES_TO` - General association
- `IS_A` - Type hierarchy (inheritance)
- `PART_OF` - Composition
- `DEPENDS_ON` - Dependency
- `SUPPORTS` - Evidence/support
- `CONTRADICTS` - Conflict
- `ENABLES` - Causation
- `PREVENTS` - Negation

**Example**:
```python
# Create hierarchical relationship
rel = await create_relationship(
    source_id="deep-learning-uuid",
    target_id="machine-learning-uuid",
    relationship_type="IS_A",
    properties={
        "strength": 1.0,
        "confidence": 0.95,
        "since": "2006"
    }
)

# Create support relationship
support = await create_relationship(
    source_id="research-paper-uuid",
    target_id="hypothesis-uuid",
    relationship_type="SUPPORTS",
    properties={
        "evidence_strength": "strong",
        "confidence": 0.85
    }
)
```

---

### get_entity_relationships

Retrieves relationships for an entity.

**Signature**:
```python
async def get_entity_relationships(
    entity_id: str,
    direction: str = "both",
    relationship_types: list[str] | None = None
) -> dict
```

**Parameters**:
- `entity_id` - Entity UUID
- `direction` - "outgoing", "incoming", or "both"
- `relationship_types` - Filter by specific types

---

### update_relationship

Updates relationship properties.

**Signature**:
```python
async def update_relationship(
    relationship_id: str,
    properties: dict
) -> dict
```

---

### delete_relationship

Deletes a relationship.

**Signature**:
```python
async def delete_relationship(
    relationship_id: str
) -> dict
```

---

## Knowledge Querying

### query_knowledge_graph

Executes Cypher query against knowledge graph.

**Signature**:
```python
async def query_knowledge_graph(
    cypher_query: str,
    parameters: dict | None = None
) -> dict
```

**Example**:
```python
# Find all concepts in a domain
result = await query_knowledge_graph("""
    MATCH (e:KnowledgeEntity {type: 'concept'})
    WHERE e.domain = $domain
    RETURN e.name as concept, e.description as description
    ORDER BY e.name
""", {"domain": "artificial_intelligence"})

# Find related entities
related = await query_knowledge_graph("""
    MATCH (start:KnowledgeEntity {name: $name})
    MATCH path = (start)-[:RELATES_TO*1..2]-(related:KnowledgeEntity)
    RETURN DISTINCT related.name as entity,
           length(path) as distance
    ORDER BY distance, entity
""", {"name": "Deep Learning"})
```

---

### get_entity_neighbors

Finds entities connected to a given entity.

**Signature**:
```python
async def get_entity_neighbors(
    entity_id: str,
    relationship_types: list[str] | None = None,
    max_depth: int = 1,
    limit: int = 50
) -> dict
```

**Parameters**:
- `entity_id` - Source entity
- `relationship_types` - Filter by types
- `max_depth` - Traversal depth (1-3 recommended)
- `limit` - Maximum results

**Returns**:
```json
{
  "success": true,
  "entity": {...},
  "neighbors": [
    {
      "entity": {...},
      "relationship": "IS_A",
      "distance": 1,
      "path": [...]
    }
  ]
}
```

---

### find_path_between_entities

Finds paths between two entities.

**Signature**:
```python
async def find_path_between_entities(
    source_id: str,
    target_id: str,
    max_length: int = 5,
    relationship_types: list[str] | None = None
) -> dict
```

**Returns**: List of paths with entities and relationships

---

## Citation Management

### create_citation

Creates a citation/source reference.

**Signature**:
```python
async def create_citation(
    source: str,
    title: str,
    url: str | None = None,
    retrieved: str | None = None,
    credibility: str = "medium"
) -> dict
```

**Parameters**:
- `source` - Source name (e.g., "Wikipedia", "Nature Journal")
- `title` - Source title
- `url` - Source URL
- `retrieved` - Retrieval date (ISO 8601)
- `credibility` - "low", "medium", "high"

**Example**:
```python
citation = await create_citation(
    source="Wikipedia",
    title="Transformer (machine learning model)",
    url="https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)",
    retrieved="2024-01-15",
    credibility="medium"
)

# Link entity to citation
await create_relationship(
    source_id=entity_id,
    target_id=citation["citation_id"],
    relationship_type="CITED_BY"
)
```

---

### link_entity_to_citation

Links knowledge entity to citation.

**Signature**:
```python
async def link_entity_to_citation(
    entity_id: str,
    citation_id: str
) -> dict
```

---

## Domain Management

### create_domain

Creates a knowledge domain.

**Signature**:
```python
async def create_domain(
    name: str,
    description: str,
    parent_domain: str | None = None
) -> dict
```

**Example**:
```python
# Create top-level domain
ai_domain = await create_domain(
    name="artificial_intelligence",
    description="Field of computer science creating intelligent agents"
)

# Create sub-domain
ml_domain = await create_domain(
    name="machine_learning",
    description="AI systems that learn from data",
    parent_domain="artificial_intelligence"
)
```

---

### get_domain_entities

Retrieves all entities in a domain.

**Signature**:
```python
async def get_domain_entities(
    domain: str,
    entity_type: str | None = None,
    limit: int = 100
) -> dict
```

---

## Knowledge Analysis

### analyze_knowledge_structure

Analyzes knowledge graph structure and statistics.

**Signature**:
```python
async def analyze_knowledge_structure(
    domain: str | None = None
) -> dict
```

**Returns**:
```json
{
  "success": true,
  "statistics": {
    "total_entities": 150,
    "total_relationships": 300,
    "entity_types": ["concept", "fact", "process"],
    "relationship_types": ["IS_A", "RELATES_TO", "PART_OF"],
    "domains": ["ai", "biology", "chemistry"],
    "avg_relationships_per_entity": 2.0,
    "max_depth": 5,
    "connected_components": 1
  }
}
```

---

### find_knowledge_gaps

Identifies entities without sufficient relationships or citations.

**Signature**:
```python
async def find_knowledge_gaps(
    domain: str | None = None,
    min_relationships: int = 1,
    require_citations: bool = True
) -> dict
```

**Returns**: List of entities missing relationships or citations

---
