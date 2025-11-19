---
title: Hybrid Reasoning Architecture
category: 06_Advanced_Topics
last_updated: 2025-10-25
line_count: 428
status: published
tags: [neocoder, mcp, documentation]
---

# Hybrid Reasoning Architecture

[← Back to Tools Reference](../05_Tools_Reference/04_Specialized_Tools.md) | [Next: F-Contraction Synthesis →](02_F_Contraction.md)

## Overview

Hybrid Reasoning is NeoCoder's core architectural pattern that combines **Neo4j graph databases** for structured knowledge with **Qdrant vector databases** for semantic search, enabling context-augmented reasoning beyond traditional RAG (Retrieval-Augmented Generation).

## Why Hybrid Reasoning?

### Limitations of Single-Database Approaches

**Graph Databases Alone**:
- ✅ Excellent for structured relationships
- ✅ Fast traversal queries
- ❌ Limited semantic similarity search
- ❌ Requires exact matches or traversal patterns

**Vector Databases Alone**:
- ✅ Excellent semantic similarity
- ✅ Natural language queries
- ❌ No structured relationships
- ❌ Limited reasoning capabilities

**Hybrid Approach**:
- ✅ Structured facts AND semantic search
- ✅ Relationship traversal AND similarity matching
- ✅ Explicit knowledge AND contextual understanding
- ✅ Provenance tracking across both systems

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────┐
│                  AI Assistant                        │
│               (Claude, GPT, etc.)                    │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              NeoCoder MCP Server                     │
│  ┌──────────────────┬──────────────────────────┐   │
│  │  Neo4j Driver    │    Qdrant Client         │   │
│  └────────┬─────────┴────────────┬─────────────┘   │
└───────────┼──────────────────────┼─────────────────┘
            │                       │
            ▼                       ▼
┌───────────────────────┐  ┌───────────────────────┐
│      Neo4j Graph      │  │  Qdrant Vector Store  │
│                       │  │                       │
│  • Projects           │  │  • Embeddings         │
│  • Files              │  │  • Semantic Search    │
│  • Code Entities      │  │  • Similarity         │
│  • Knowledge Entities │  │  • Contextual Data    │
│  • Relationships      │  │                       │
└───────────────────────┘  └───────────────────────┘
```

### Data Flow

**Write Path**:
1. Create entity in Neo4j with structured data
2. Generate embedding for entity content
3. Store embedding in Qdrant with Neo4j ID reference
4. Maintain bidirectional linking

**Read Path (Hybrid Query)**:
1. Perform semantic search in Qdrant
2. Get Neo4j IDs from Qdrant results
3. Retrieve full entities from Neo4j
4. Traverse related entities via graph
5. Enrich results with relationship context

## Implementation Patterns

### Dual-Database Entity Creation

```python
async def create_hybrid_entity(
    entity_data: dict,
    embedding_text: str
) -> dict:
    """Create entity in both Neo4j and Qdrant."""

    # 1. Create graph entity
    async with neo4j_session() as session:
        result = await session.run("""
            CREATE (e:KnowledgeEntity {
              id: randomUUID(),
              name: $name,
              description: $description,
              domain: $domain,
              created: datetime()
            })
            RETURN e.id as entity_id
        """, entity_data)

        entity_id = result.single()["entity_id"]

    # 2. Generate embedding
    embedding = await generate_embedding(embedding_text)

    # 3. Store in vector database
    await qdrant_client.upsert(
        collection_name="knowledge",
        points=[{
            "id": entity_id,  # Same ID as Neo4j
            "vector": embedding,
            "payload": {
                "name": entity_data["name"],
                "description": entity_data["description"],
                "domain": entity_data["domain"],
                "neo4j_id": entity_id  # Explicit reference
            }
        }]
    )

    return {"success": True, "entity_id": entity_id}
```

### Hybrid Search Query

```python
async def hybrid_search(
    query_text: str,
    limit: int = 10,
    graph_filter: dict | None = None
) -> dict:
    """Combine vector search with graph traversal."""

    # 1. Generate query embedding
    query_embedding = await generate_embedding(query_text)

    # 2. Semantic search in Qdrant
    vector_results = await qdrant_client.search(
        collection_name="knowledge",
        query_vector=query_embedding,
        limit=limit * 2,  # Get extra for filtering
        score_threshold=0.7
    )

    # 3. Extract Neo4j IDs
    entity_ids = [result.id for result in vector_results]

    # 4. Retrieve from Neo4j with relationships
    async with neo4j_session() as session:
        result = await session.run("""
            MATCH (e:KnowledgeEntity)
            WHERE e.id IN $entity_ids
            OPTIONAL MATCH (e)-[r]-(related:KnowledgeEntity)
            RETURN e,
                   collect(DISTINCT related) as neighbors,
                   collect(DISTINCT type(r)) as relationship_types
            LIMIT $limit
        """, {
            "entity_ids": entity_ids,
            "limit": limit
        })

        graph_results = [record async for record in result]

    # 5. Merge vector scores with graph data
    hybrid_results = []
    for graph_result in graph_results:
        entity = graph_result["e"]
        # Find matching vector result for score
        vector_match = next(
            (v for v in vector_results if v.id == entity["id"]),
            None
        )

        hybrid_results.append({
            "entity": entity,
            "similarity_score": vector_match.score if vector_match else 0.0,
            "neighbors": graph_result["neighbors"],
            "relationship_types": graph_result["relationship_types"]
        })

    return {
        "success": True,
        "results": hybrid_results,
        "result_count": len(hybrid_results)
    }
```

### Context-Augmented Reasoning

```python
async def augmented_reasoning(
    user_query: str,
    context_depth: int = 2
) -> dict:
    """Retrieve context using hybrid approach."""

    # 1. Semantic search for relevant entities
    semantic_results = await hybrid_search(user_query, limit=5)

    # 2. Expand context via graph traversal
    entity_ids = [r["entity"]["id"] for r in semantic_results["results"]]

    async with neo4j_session() as session:
        result = await session.run("""
            MATCH (start:KnowledgeEntity)
            WHERE start.id IN $entity_ids
            MATCH path = (start)-[*1..$depth]-(related:KnowledgeEntity)
            RETURN DISTINCT related,
                   min(length(path)) as distance
            ORDER BY distance, related.name
        """, {
            "entity_ids": entity_ids,
            "depth": context_depth
        })

        context_entities = [record async for record in result]

    # 3. Build comprehensive context
    context = {
        "primary_results": semantic_results["results"],
        "related_context": context_entities,
        "total_context_size": len(semantic_results["results"]) + len(context_entities)
    }

    return context
```

## Use Cases

### 1. Semantic Code Search with Structure

**Scenario**: Find authentication-related code with dependencies

```python
# Semantic search in Qdrant
vector_results = await qdrant_client.search(
    collection_name="code",
    query_vector=embed("authentication and password validation"),
    limit=10
)

# Graph traversal in Neo4j
file_ids = [r.id for r in vector_results]
dependencies = await neo4j_session.run("""
    MATCH (f:File)-[:IMPORTS]->(dep:File)
    WHERE f.id IN $file_ids
    RETURN f.path, collect(dep.path) as dependencies
""", {"file_ids": file_ids})

# Result: Semantically relevant files + their import dependencies
```

### 2. Knowledge Discovery with Provenance

**Scenario**: Research synthesis with citation tracking

```python
# Find similar research
papers = await hybrid_search(
    "transformer architecture innovations",
    limit=5
)

# Get citation network from graph
for paper in papers["results"]:
    citations = await neo4j_session.run("""
        MATCH (p:ResearchPaper {id: $id})
        MATCH (p)-[:CITES]->(cited:ResearchPaper)
        RETURN cited
    """, {"id": paper["entity"]["id"]})

# Result: Semantically similar papers + explicit citation relationships
```

### 3. Project Context Building

**Scenario**: Understand project architecture with semantic queries

```python
# Semantic: "How is authentication implemented?"
relevant_files = await qdrant_client.search(
    query_vector=embed("authentication implementation"),
    limit=5
)

# Graph: Get project structure
structure = await neo4j_session.run("""
    MATCH (p:Project)-[:HAS_FILE]->(f:File)
    WHERE f.id IN $file_ids
    MATCH (f)-[:DEFINES]->(entity:CodeEntity)
    RETURN p, f, collect(entity) as entities
""", {"file_ids": [r.id for r in relevant_files]})

# Result: Relevant files + complete project context + code entities
```

## Performance Optimization

### Caching Strategy

```python
# Cache frequently accessed embeddings
embedding_cache = {}

async def get_cached_embedding(text: str) -> list[float]:
    cache_key = hash(text)
    if cache_key in embedding_cache:
        return embedding_cache[cache_key]

    embedding = await generate_embedding(text)
    embedding_cache[cache_key] = embedding
    return embedding
```

### Batch Operations

```python
# Batch vector insertions
async def batch_vector_insert(entities: list[dict]):
    points = []
    for entity in entities:
        embedding = await generate_embedding(entity["description"])
        points.append({
            "id": entity["id"],
            "vector": embedding,
            "payload": entity
        })

    await qdrant_client.upsert(
        collection_name="knowledge",
        points=points
    )
```

### Index Optimization

```cypher
-- Neo4j indexes for hybrid queries
CREATE INDEX entity_id_index IF NOT EXISTS
FOR (e:KnowledgeEntity)
ON (e.id);

CREATE INDEX entity_domain_index IF NOT EXISTS
FOR (e:KnowledgeEntity)
ON (e.domain);
```

```python
# Qdrant index optimization
await qdrant_client.create_collection(
    collection_name="knowledge",
    vectors_config={
        "size": 1536,  # OpenAI embedding dimension
        "distance": "Cosine"
    },
    hnsw_config={
        "m": 16,  # Number of connections
        "ef_construct": 100  # Construction time parameter
    }
)
```

## Best Practices

### Data Consistency

**Maintain ID Alignment**:
```python
# Always use same ID in both databases
entity_id = str(uuid.uuid4())

# Neo4j
CREATE (e:Entity {id: $entity_id, ...})

# Qdrant
points = [{"id": entity_id, "vector": ..., "payload": {...}}]
```

**Atomic Operations**:
```python
try:
    # Create in Neo4j
    neo4j_id = await create_in_neo4j(entity_data)

    # Create in Qdrant
    await create_in_qdrant(neo4j_id, embedding, payload)

except Exception as e:
    # Rollback Neo4j if Qdrant fails
    await delete_from_neo4j(neo4j_id)
    raise
```

### Query Optimization

**Filter Early in Qdrant**:
```python
# Good: Filter in vector search
results = await qdrant_client.search(
    query_vector=embedding,
    query_filter={
        "must": [
            {"key": "domain", "match": {"value": "ai"}}
        ]
    }
)

# Then refine in Neo4j
```

**Use Graph for Relationships**:
```python
# Good: Leverage graph for traversal
MATCH (start)-[:RELATES_TO*1..3]-(related)

# Avoid: Manual relationship following in vectors
```

## Related Documentation

- [F-Contraction](02_F_Contraction.md) - Knowledge synthesis methodology
- [Vector Integration](03_Vector_Integration.md) - Qdrant details
- [Multi-Database](04_Multi_Database.md) - Coordination patterns
- [Knowledge Graph Tools](../05_Tools_Reference/02_Knowledge_Graph_Tools.md) - Implementation tools

---
*Last Updated: 2025-10-24 | [Report Issues](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues)*
