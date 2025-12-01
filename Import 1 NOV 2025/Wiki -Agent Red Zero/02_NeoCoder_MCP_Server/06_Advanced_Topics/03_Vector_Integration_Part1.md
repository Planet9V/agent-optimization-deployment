---
title: Qdrant Vector Integration (Part 1 of 2)
category: 06_Advanced_Topics
last_updated: 2025-10-25
line_count: 437
status: published
tags: [neocoder, mcp, documentation]
---


# Qdrant Vector Integration

[← Back to F-Contraction](02_F_Contraction.md) | [Next: Multi-Database Coordination →](04_Multi_Database.md)

## Overview

NeoCoder integrates Qdrant vector database for semantic search capabilities, enabling natural language queries and similarity matching alongside Neo4j's graph structure.

## Qdrant Setup

### Configuration

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Initialize client
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Create collection
qdrant.create_collection(
    collection_name="knowledge",
    vectors_config=VectorParams(
        size=1536,  # OpenAI ada-002 dimension
        distance=Distance.COSINE
    )
)
```

### Collection Structure

**knowledge** - Knowledge entities
```json
{
  "id": "neo4j-entity-uuid",
  "vector": [0.1, 0.2, ...],  // 1536 dimensions
  "payload": {
    "name": "Entity name",
    "description": "Entity description",
    "domain": "artificial_intelligence",
    "neo4j_id": "uuid",
    "entity_type": "concept"
  }
}
```

**code** - Code entities
```json
{
  "id": "code-entity-uuid",
  "vector": [...],
  "payload": {
    "name": "Function name",
    "file_path": "src/auth.py",
    "entity_type": "function",
    "language": "Python",
    "neo4j_id": "uuid"
  }
}
```

**documents** - Document embeddings
```json
{
  "id": "document-uuid",
  "vector": [...],
  "payload": {
    "title": "Document title",
    "content": "Full text...",
    "source": "file/url",
    "neo4j_id": "uuid"
  }
}
```

## Embedding Generation

### Text Embeddings

```python
import openai

async def generate_embedding(text: str) -> list[float]:
    """Generate embedding using OpenAI."""
    response = await openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response['data'][0]['embedding']
```

### Code Embeddings

```python
async def generate_code_embedding(
    code: str,
    language: str
) -> list[float]:
    """Generate embedding for code with context."""
    # Combine code with language context
    text = f"[{language}]\n{code}"
    return await generate_embedding(text)
```

## Vector Operations

### Inserting Vectors

```python
async def add_to_vector_store(
    entity_id: str,
    embedding_text: str,
    collection: str = "knowledge",
    metadata: dict | None = None
) -> dict:
    """Add entity embedding to Qdrant."""

    # Generate embedding
    vector = await generate_embedding(embedding_text)

    # Prepare payload
    payload = metadata or {}
    payload["neo4j_id"] = entity_id

    # Insert
    qdrant.upsert(
        collection_name=collection,
        points=[{
            "id": entity_id,
            "vector": vector,
            "payload": payload
        }]
    )

    return {"success": True, "entity_id": entity_id}
```

### Batch Insertion

```python
async def batch_vector_insert(
    entities: list[dict],
    collection: str = "knowledge"
):
    """Insert multiple vectors efficiently."""

    points = []
    for entity in entities:
        vector = await generate_embedding(entity["text"])
        points.append({
            "id": entity["id"],
            "vector": vector,
            "payload": entity.get("metadata", {})
        })

    # Insert in batch
    qdrant.upsert(
        collection_name=collection,
        points=points,
        batch_size=100
    )
```

## Semantic Search

### Basic Search

```python
async def semantic_search(
    query_text: str,
    collection: str = "knowledge",
    limit: int = 10,
    threshold: float = 0.7
) -> dict:
    """Perform semantic search."""

    # Generate query embedding
    query_vector = await generate_embedding(query_text)

    # Search
    results = qdrant.search(
        collection_name=collection,
        query_vector=query_vector,
        limit=limit,
        score_threshold=threshold
    )

    return {
        "success": True,
        "results": [
            {
                "id": r.id,
                "score": r.score,
                "payload": r.payload
            }
            for r in results
        ]
    }
```

### Filtered Search

```python
async def filtered_semantic_search(
    query_text: str,
    filters: dict,
    limit: int = 10
) -> dict:
    """Search with metadata filters."""

    from qdrant_client.models import Filter, FieldCondition, MatchValue

    query_vector = await generate_embedding(query_text)

    # Build filter
    filter_conditions = []
    for key, value in filters.items():
        filter_conditions.append(
            FieldCondition(key=key, match=MatchValue(value=value))
        )

    # Search with filter
    results = qdrant.search(
        collection_name="knowledge",
        query_vector=query_vector,
        query_filter=Filter(must=filter_conditions),
        limit=limit
    )

    return {"results": results}
```

**Example**:
```python
# Search only AI domain entities
results = await filtered_semantic_search(
    query_text="neural network architectures",
    filters={"domain": "artificial_intelligence"}
)
```

### Multi-Vector Search

```python
async def multi_vector_search(
    query_texts: list[str],
    weights: list[float] | None = None
) -> dict:
    """Search with multiple query vectors."""

    # Generate embeddings
    vectors = [await generate_embedding(q) for q in query_texts]

    # Weight vectors
    if weights:
        weighted_vector = [
            sum(v[i] * w for v, w in zip(vectors, weights))
            for i in range(len(vectors[0]))
        ]
    else:
        # Average
        weighted_vector = [
            sum(v[i] for v in vectors) / len(vectors)
            for i in range(len(vectors[0]))
        ]

    # Search
    results = qdrant.search(
        collection_name="knowledge",
        query_vector=weighted_vector,
        limit=10
    )

    return {"results": results}
```

## Advanced Patterns

### Recommendation System

```python
async def recommend_similar(
    entity_id: str,
    limit: int = 5
) -> dict:
    """Find similar entities."""

    # Get entity vector
    entity = qdrant.retrieve(
        collection_name="knowledge",
        ids=[entity_id]
    )[0]

    # Search using entity vector
    results = qdrant.search(
        collection_name="knowledge",
        query_vector=entity.vector,
        limit=limit + 1  # +1 to exclude self
    )

    # Filter out the entity itself
    similar = [r for r in results if r.id != entity_id][:limit]

    return {"similar_entities": similar}
```

### Clustering

```python
from sklearn.cluster import KMeans

async def cluster_entities(
    entity_ids: list[str],
    n_clusters: int = 5
) -> dict:
    """Cluster entities by vector similarity."""

    # Retrieve vectors
    entities = qdrant.retrieve(
        collection_name="knowledge",
        ids=entity_ids
    )

    vectors = [e.vector for e in entities]

    # Cluster
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(vectors)

    # Group by cluster
    clusters = {}
    for entity, label in zip(entities, labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(entity.id)

    return {"clusters": clusters}
```

### Contextual Re-ranking

```python
async def rerank_results(
    results: list[dict],
    context: str
) -> list[dict]:
    """Re-rank results based on context."""

    # Generate context embedding
    context_vector = await generate_embedding(context)

    # Calculate relevance to context
    from scipy.spatial.distance import cosine

    for result in results:
        result_vector = result["vector"]
        context_score = 1 - cosine(context_vector, result_vector)
        result["context_relevance"] = context_score

        # Combine with original score
        result["final_score"] = (
            result["score"] * 0.7 +
            context_score * 0.3
        )

    # Sort by final score
    return sorted(results, key=lambda r: r["final_score"], reverse=True)
```

## Performance Optimization

### Index Configuration

```python
# Optimize for query performance
qdrant.update_collection(
    collection_name="knowledge",
    hnsw_config={
        "m": 16,  # Number of bi-directional links
        "ef_construct": 100,  # Size of dynamic candidate list
        "full_scan_threshold": 10000
    }
)

# Optimize for memory
qdrant.update_collection(
    collection_name="knowledge",
    optimizer_config={
        "indexing_threshold": 20000,
        "memmap_threshold": 50000
    }
)
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_embedding(text: str) -> tuple:
    """Cache embeddings for repeated queries."""
    embedding = generate_embedding(text)
    return tuple(embedding)  # tuple is hashable
```

### Batch Queries

```python
async def batch_search(
    queries: list[str],
    limit: int = 5
) -> list[dict]:
    """Execute multiple searches efficiently."""

    # Generate all embeddings
    vectors = await asyncio.gather(*[
        generate_embedding(q) for q in queries
    ])

    # Execute searches
    results = []
    for vector in vectors:
        result = qdrant.search(
            collection_name="knowledge",
            query_vector=vector,
            limit=limit
        )
        results.append(result)

    return results
```
