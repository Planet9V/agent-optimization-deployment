---
title: Knowledge Graph Tools Reference (Part 2)
category: 05_Tools_Reference
last_updated: 2025-10-25
line_count: 136
status: published
tags: [neocoder, mcp, documentation]
---

## Hybrid Reasoning

### semantic_search

Searches knowledge graph using vector similarity.

**Signature**:
```python
async def semantic_search(
    query_text: str,
    domain: str | None = None,
    limit: int = 10,
    threshold: float = 0.7
) -> dict
```

**Parameters**:
- `query_text` - Natural language query
- `domain` - Filter by domain
- `limit` - Maximum results
- `threshold` - Minimum similarity score (0-1)

**Example**:
```python
results = await semantic_search(
    query_text="how do neural networks learn",
    domain="artificial_intelligence",
    limit=5,
    threshold=0.75
)
```

---

### hybrid_search

Combines vector search with graph traversal.

**Signature**:
```python
async def hybrid_search(
    query_text: str,
    graph_filters: dict | None = None,
    limit: int = 10
) -> dict
```

**Parameters**:
- `query_text` - Semantic query
- `graph_filters` - Additional Cypher filters
- `limit` - Results limit

**Returns**: Combined results from Qdrant vector search and Neo4j graph traversal

---

## Best Practices

### Entity Design

**Use consistent naming**:
```python
# Good: Clear, consistent names
await create_knowledge_entity(name="Machine Learning", entity_type="concept")
await create_knowledge_entity(name="Deep Learning", entity_type="concept")

# Avoid: Inconsistent naming
await create_knowledge_entity(name="ML", entity_type="concept")
await create_knowledge_entity(name="deep_learning_concept", entity_type="concept")
```

**Specify domains**:
```python
# Good: Domain specified
await create_knowledge_entity(
    name="Gradient Descent",
    domain="artificial_intelligence"
)

# Avoid: No domain
await create_knowledge_entity(name="Gradient Descent")
```

### Relationship Modeling

**Use appropriate relationship types**:
```python
# Good: Specific relationships
await create_relationship(source_id, target_id, "IS_A")  # Hierarchy
await create_relationship(source_id, target_id, "PART_OF")  # Composition
await create_relationship(source_id, target_id, "DEPENDS_ON")  # Dependency

# Avoid: Generic relationships only
await create_relationship(source_id, target_id, "RELATES_TO")  # Too vague
```

**Add relationship metadata**:
```python
# Good: Metadata provides context
await create_relationship(
    source_id, target_id, "SUPPORTS",
    properties={
        "confidence": 0.85,
        "evidence": "experimental",
        "source": "research-paper-123"
    }
)
```

### Citation Tracking

**Always cite knowledge sources**:
```python
# Create entity
entity = await create_knowledge_entity(name="Transformer", ...)

# Create citation
citation = await create_citation(
    source="Attention Is All You Need",
    title="Vaswani et al., 2017"
)

# Link them
await create_relationship(entity["entity_id"], citation["citation_id"], "CITED_BY")
```

## Related Documentation

- [Core Tools](01_Core_Tools.md) - Foundation tools
- [Knowledge Graph Incarnation](../03_Incarnations/03_Knowledge_Graph.md) - Detailed guide
- [Hybrid Reasoning](../06_Advanced_Topics/01_Hybrid_Reasoning.md) - Vector integration
- [Graph Structure](../02_Core_Concepts/03_Graph_Structure.md) - Schema details

---
*Last Updated: 2025-10-24 | [Report Issues](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues)*
