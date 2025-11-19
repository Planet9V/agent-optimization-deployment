---
title: Good: Meaningful, contextual text (Part 2 of 2)
category: 06_Advanced_Topics
last_updated: 2025-10-25
line_count: 60
status: published
tags: [neocoder, mcp, documentation]
---

## Best Practices

### Embedding Quality

**Use appropriate text for embeddings**:
```python
# Good: Meaningful, contextual text
text = f"{entity['name']}: {entity['description']}"

# Avoid: Just IDs or short names
text = entity['id']  # Not semantic
```

**Include context**:
```python
# Good: Include domain context
text = f"[{domain}] {name}: {description}"

# Better: Include relationships
text = f"{name} in {domain}. {description}. Related to: {', '.join(related_entities)}"
```

### Collection Management

**Use separate collections for different entity types**:
```python
# Good: Type-specific collections
await add_to_vector_store(entity_id, text, collection="code")
await add_to_vector_store(entity_id, text, collection="knowledge")

# Avoid: Mixed collection
await add_to_vector_store(entity_id, text, collection="all")  # Hard to filter
```

### Query Optimization

**Filter before vector search**:
```python
# Good: Filter in Qdrant
results = qdrant.search(
    query_vector=vector,
    query_filter={"domain": "ai"},  # Filter in vector DB
    limit=10
)

# Avoid: Filter after retrieval
results = qdrant.search(query_vector=vector, limit=1000)
filtered = [r for r in results if r.payload.get("domain") == "ai"][:10]
```

## Related Documentation

- [Hybrid Reasoning](01_Hybrid_Reasoning.md) - Integration architecture
- [Multi-Database](04_Multi_Database.md) - Coordination patterns
- [Knowledge Graph Tools](../05_Tools_Reference/02_Knowledge_Graph_Tools.md) - Entity management
- [F-Contraction](02_F_Contraction.md) - Knowledge synthesis

---
*Last Updated: 2025-10-24 | [Report Issues](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues)*
