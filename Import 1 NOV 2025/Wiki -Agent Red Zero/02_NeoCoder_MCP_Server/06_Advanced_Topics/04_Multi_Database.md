---
title: Multi-Database Coordination
category: 06_Advanced_Topics
last_updated: 2025-10-25
line_count: 487
status: published
tags: [neocoder, mcp, documentation]
---

# Multi-Database Coordination

[← Back to Vector Integration](03_Vector_Integration.md) | [Next: Development Guide →](../07_Development/01_Creating_Tools.md)

## Overview

NeoCoder coordinates multiple databases (Neo4j graph + Qdrant vector) to provide comprehensive knowledge management. This page covers coordination patterns, consistency strategies, and transaction management across databases.

## Database Roles

### Neo4j - Graph Database
**Responsibilities**:
- Structured facts and relationships
- Workflow execution tracking
- Project and file organization
- Citation networks
- Code structure (AST/ASG)
- Query patterns and traversal

**Strengths**:
- Complex relationship queries
- Graph traversal
- ACID transactions
- Schema constraints
- Audit trails

### Qdrant - Vector Database
**Responsibilities**:
- Semantic embeddings
- Similarity search
- Natural language queries
- Contextual matching
- Recommendation systems

**Strengths**:
- Fast similarity search
- High-dimensional vectors
- Filtering capabilities
- Scalable indexing
- Approximate nearest neighbor (ANN)

## Coordination Patterns

### Pattern 1: ID Synchronization

**Principle**: Use same UUID across both databases

```python
async def create_synchronized_entity(
    entity_data: dict,
    embedding_text: str
) -> dict:
    """Create entity in both databases with synchronized ID."""

    # Generate single UUID
    entity_id = str(uuid.uuid4())

    try:
        # 1. Create in Neo4j with ID
        async with neo4j_session() as session:
            await session.run("""
                CREATE (e:KnowledgeEntity {
                  id: $id,
                  name: $name,
                  description: $description,
                  created: datetime()
                })
            """, {
                "id": entity_id,
                "name": entity_data["name"],
                "description": entity_data["description"]
            })

        # 2. Create in Qdrant with same ID
        vector = await generate_embedding(embedding_text)
        qdrant.upsert(
            collection_name="knowledge",
            points=[{
                "id": entity_id,  # Same ID
                "vector": vector,
                "payload": {
                    "neo4j_id": entity_id,  # Explicit reference
                    "name": entity_data["name"]
                }
            }]
        )

        return {"success": True, "entity_id": entity_id}

    except Exception as e:
        # Rollback Neo4j if Qdrant fails
        await rollback_neo4j(entity_id)
        raise
```

### Pattern 2: Reference Storage

**Store database references in payload**:

```python
# Neo4j stores Qdrant status
await neo4j_session.run("""
    MATCH (e:KnowledgeEntity {id: $id})
    SET e.qdrant_indexed = true,
        e.qdrant_collection = $collection,
        e.embedding_model = $model
""", {
    "id": entity_id,
    "collection": "knowledge",
    "model": "text-embedding-ada-002"
})

# Qdrant stores Neo4j reference
qdrant.set_payload(
    collection_name="knowledge",
    payload={
        "neo4j_id": entity_id,
        "neo4j_labels": ["KnowledgeEntity"],
        "neo4j_synced": True
    },
    points=[entity_id]
)
```

### Pattern 3: Hybrid Query

**Combine vector search with graph enrichment**:

```python
async def hybrid_query(
    query_text: str,
    enrich_with_graph: bool = True
) -> dict:
    """Query both databases in coordinated fashion."""

    # 1. Vector search in Qdrant
    query_vector = await generate_embedding(query_text)
    vector_results = qdrant.search(
        collection_name="knowledge",
        query_vector=query_vector,
        limit=20
    )

    # 2. Extract Neo4j IDs
    neo4j_ids = [r.id for r in vector_results]

    # 3. Enrich with Neo4j data
    if enrich_with_graph:
        async with neo4j_session() as session:
            result = await session.run("""
                MATCH (e:KnowledgeEntity)
                WHERE e.id IN $ids
                OPTIONAL MATCH (e)-[r]-(related:KnowledgeEntity)
                RETURN e,
                       collect(DISTINCT related) as neighbors,
                       collect(DISTINCT type(r)) as rel_types
            """, {"ids": neo4j_ids})

            graph_data = {
                r["e"]["id"]: {
                    "entity": r["e"],
                    "neighbors": r["neighbors"],
                    "relationship_types": r["rel_types"]
                }
                async for r in result
            }

    # 4. Combine results
    enriched_results = []
    for vr in vector_results:
        enriched_results.append({
            "id": vr.id,
            "similarity_score": vr.score,
            "vector_payload": vr.payload,
            "graph_data": graph_data.get(vr.id, {}),
            "neighbors_count": len(graph_data.get(vr.id, {}).get("neighbors", []))
        })

    return {"results": enriched_results}
```

## Consistency Management

### Eventual Consistency

```python
class SyncManager:
    """Manage eventual consistency between databases."""

    def __init__(self):
        self.sync_queue = []
        self.failed_syncs = []

    async def queue_sync(self, operation: dict):
        """Queue synchronization operation."""
        self.sync_queue.append(operation)

    async def process_sync_queue(self):
        """Process pending synchronizations."""
        while self.sync_queue:
            op = self.sync_queue.pop(0)

            try:
                if op["type"] == "create":
                    await self._sync_create(op)
                elif op["type"] == "update":
                    await self._sync_update(op)
                elif op["type"] == "delete":
                    await self._sync_delete(op)

            except Exception as e:
                # Move to failed queue
                op["error"] = str(e)
                op["attempts"] = op.get("attempts", 0) + 1
                self.failed_syncs.append(op)

    async def retry_failed_syncs(self):
        """Retry failed synchronizations."""
        for op in self.failed_syncs[:]:
            if op["attempts"] < 3:
                try:
                    await self.process_sync_queue()
                    self.failed_syncs.remove(op)
                except:
                    pass
```

### Strong Consistency

```python
async def atomic_multi_db_operation(
    entity_data: dict,
    embedding_text: str
) -> dict:
    """Perform atomic operation across databases."""

    # Use distributed transaction pattern
    transaction_id = str(uuid.uuid4())

    try:
        # Phase 1: Prepare (both databases)
        neo4j_prepared = await prepare_neo4j_write(transaction_id, entity_data)
        qdrant_prepared = await prepare_qdrant_write(transaction_id, embedding_text)

        if not (neo4j_prepared and qdrant_prepared):
            raise Exception("Preparation failed")

        # Phase 2: Commit (both databases)
        await commit_neo4j(transaction_id)
        await commit_qdrant(transaction_id)

        return {"success": True}

    except Exception as e:
        # Phase 3: Rollback (both databases)
        await rollback_neo4j(transaction_id)
        await rollback_qdrant(transaction_id)
        raise
```

## Update Strategies

### Synchronous Updates

```python
async def sync_update(
    entity_id: str,
    updates: dict
) -> dict:
    """Update both databases synchronously."""

    try:
        # Update Neo4j
        async with neo4j_session() as session:
            await session.run("""
                MATCH (e:KnowledgeEntity {id: $id})
                SET e += $updates,
                    e.updated = datetime()
            """, {"id": entity_id, "updates": updates})

        # Update Qdrant if description changed
        if "description" in updates:
            new_vector = await generate_embedding(updates["description"])
            qdrant.upsert(
                collection_name="knowledge",
                points=[{
                    "id": entity_id,
                    "vector": new_vector,
                    "payload": updates
                }]
            )

        return {"success": True}

    except Exception as e:
        # Rollback needed
        return {"success": False, "error": str(e)}
```

### Asynchronous Updates

```python
from asyncio import Queue

class AsyncUpdateManager:
    """Manage asynchronous database updates."""

    def __init__(self):
        self.update_queue = Queue()

    async def queue_update(self, entity_id: str, updates: dict):
        """Queue update for async processing."""
        await self.update_queue.put({
            "entity_id": entity_id,
            "updates": updates,
            "timestamp": datetime.now()
        })

    async def process_updates(self):
        """Process queued updates."""
        while True:
            update = await self.update_queue.get()

            try:
                # Update Neo4j immediately
                await update_neo4j(update["entity_id"], update["updates"])

                # Update Qdrant asynchronously
                if "description" in update["updates"]:
                    await update_qdrant_async(update["entity_id"], update["updates"])

            except Exception as e:
                # Log error, don't block queue
                logger.error(f"Update failed: {e}")

            self.update_queue.task_done()
```

## Deletion Strategies

### Soft Delete

```python
async def soft_delete(entity_id: str) -> dict:
    """Mark entity as deleted in both databases."""

    # Neo4j: Add deleted flag
    await neo4j_session.run("""
        MATCH (e:KnowledgeEntity {id: $id})
        SET e.deleted = true,
            e.deleted_at = datetime()
    """, {"id": entity_id})

    # Qdrant: Update payload
    qdrant.set_payload(
        collection_name="knowledge",
        payload={"deleted": True, "deleted_at": datetime.now().isoformat()},
        points=[entity_id]
    )

    return {"success": True}
```

### Hard Delete

```python
async def hard_delete(entity_id: str) -> dict:
    """Remove entity from both databases."""

    try:
        # Delete from Neo4j
        await neo4j_session.run("""
            MATCH (e:KnowledgeEntity {id: $id})
            DETACH DELETE e
        """, {"id": entity_id})

        # Delete from Qdrant
        qdrant.delete(
            collection_name="knowledge",
            points_selector=[entity_id]
        )

        return {"success": True}

    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Monitoring and Validation

### Sync Validation

```cypher
// Find entities in Neo4j but not in Qdrant
MATCH (e:KnowledgeEntity)
WHERE e.qdrant_indexed IS NULL OR e.qdrant_indexed = false
RETURN count(e) as unindexed_count
```

```python
# Find entities in Qdrant but not in Neo4j
qdrant_ids = set(qdrant.scroll(collection_name="knowledge")[0])

async with neo4j_session() as session:
    result = await session.run("MATCH (e:KnowledgeEntity) RETURN e.id")
    neo4j_ids = set([r["e.id"] async for r in result])

orphaned_in_qdrant = qdrant_ids - neo4j_ids
```

### Health Check

```python
async def multi_db_health_check() -> dict:
    """Check health of both databases."""

    # Neo4j health
    neo4j_healthy = await check_neo4j_health()

    # Qdrant health
    qdrant_healthy = qdrant.get_collections() is not None

    # Sync status
    sync_lag = await calculate_sync_lag()

    return {
        "neo4j_healthy": neo4j_healthy,
        "qdrant_healthy": qdrant_healthy,
        "sync_lag_seconds": sync_lag,
        "overall_healthy": neo4j_healthy and qdrant_healthy and sync_lag < 60
    }
```

## Best Practices

### ID Management

**Always use consistent IDs**:
```python
# Good: Single source of truth
entity_id = str(uuid.uuid4())
await create_in_neo4j(entity_id, data)
await create_in_qdrant(entity_id, vector, data)

# Avoid: Different IDs
neo4j_id = create_in_neo4j(data)
qdrant_id = create_in_qdrant(vector, data)  # Inconsistent
```

### Error Handling

**Implement rollback logic**:
```python
try:
    await neo4j_operation()
    await qdrant_operation()
except Exception:
    await rollback_neo4j()
    await rollback_qdrant()
    raise
```

### Performance

**Batch operations when possible**:
```python
# Good: Batch inserts
entities = [...]
await batch_neo4j_insert(entities)
await batch_qdrant_insert(entities)

# Avoid: Individual inserts in loop
for entity in entities:
    await create_in_neo4j(entity)
    await create_in_qdrant(entity)
```

## Related Documentation

- [Hybrid Reasoning](01_Hybrid_Reasoning.md) - Architecture overview
- [Vector Integration](03_Vector_Integration.md) - Qdrant details
- [Graph Structure](../02_Core_Concepts/03_Graph_Structure.md) - Neo4j schema
- [Core Tools](../05_Tools_Reference/01_Core_Tools.md) - Implementation tools

---
*Last Updated: 2025-10-24 | [Report Issues](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues)*
