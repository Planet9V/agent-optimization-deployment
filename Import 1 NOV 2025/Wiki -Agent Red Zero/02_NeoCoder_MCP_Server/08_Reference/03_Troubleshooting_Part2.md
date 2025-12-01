---
title: 03_Troubleshooting_Part1 (Part 2 of 2)
category: 08_Reference
last_updated: 2025-10-25
line_count: 59
status: published
tags: [neocoder, mcp, documentation]
---

## Hybrid Reasoning Issues

### ID Mismatch Between Databases

**Symptom**:
```
Entity exists in Neo4j but not in Qdrant
Vector search returns IDs not found in graph
```

**Solutions**:

1. **Audit sync status**:
```cypher
// Find entities not in Qdrant
MATCH (e:KnowledgeEntity)
WHERE e.qdrant_indexed IS NULL OR e.qdrant_indexed = false
RETURN count(e) as unindexed_count
```

2. **Re-sync entities**:
```python
async def resync_entity(entity_id: str):
    # Get from Neo4j
    entity = await get_knowledge_entity(entity_id)

    # Generate embedding
    text = f"{entity['name']}: {entity['description']}"
    embedding = await generate_embedding(text)

    # Update in Qdrant
    await qdrant_client.upsert(
        collection_name="knowledge",
        points=[{
            "id": entity_id,
            "vector": embedding,
            "payload": entity
        }]
    )

    # Mark as synced in Neo4j
    await mark_entity_synced(entity_id)
```

3. **Find orphaned vectors**:
```python
# Get all Qdrant IDs
qdrant_ids = set(qdrant_client.scroll(collection_name="knowledge")[0])

# Get all Neo4j IDs
async with neo4j_session() as session:
    result = await session.run("MATCH (e:KnowledgeEntity) RETURN e.id")
    neo4j_ids = set([r["e.id"] async for r in result])

# Find orphans
orphaned = qdrant_ids - neo4j_ids
print(f"Orphaned vectors: {len(orphaned)}")
```
