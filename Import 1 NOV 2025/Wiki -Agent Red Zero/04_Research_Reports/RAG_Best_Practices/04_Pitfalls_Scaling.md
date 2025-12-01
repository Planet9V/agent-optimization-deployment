# Part 4 of 5: Pitfalls & Scaling

**Series**: RAG Best Practices
**Navigation**: [← Part 3](./03_Embedding_Performance.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 5 →](./05_Integration_Deployment.md)

---

        """
        Retrieve with metadata filtering and boosting

        filters: {"date_range": ["2024-01-01", "2024-12-31"], "category": "technical"}
        boost_metadata: {"recency": 0.2, "popularity": 0.1}
        """
        # Get initial candidates (retrieve more for filtering)
        candidates = self.vector_index.search(query, k=k*5)

        # Apply metadata filters
        if filters:
            candidates = self.apply_filters(candidates, filters)

        # Apply metadata boosting
        if boost_metadata:
            candidates = self.apply_boosts(candidates, boost_metadata)

        # Return top k after filtering and boosting
        return candidates[:k]

    def apply_filters(self, candidates, filters):
        """Hard filters: must match"""
        filtered = []
        for doc_id, score in candidates:
            metadata = self.metadata_db.get(doc_id)

            if self.matches_filters(metadata, filters):
                filtered.append((doc_id, score))

        return filtered

    def apply_boosts(self, candidates, boost_config):
        """Soft boosts: adjust scores"""
        boosted = []
        for doc_id, score in candidates:
            metadata = self.metadata_db.get(doc_id)

            # Calculate boost multiplier
            boost = 1.0

            # Recency boost
            if "recency" in boost_config:
                days_old = (time.time() - metadata['created_at']) / 86400
                recency_boost = 1.0 - (days_old / 365) * boost_config['recency']
                boost *= max(recency_boost, 0.5)

            # Popularity boost
            if "popularity" in boost_config:
                popularity_boost = 1.0 + (metadata['view_count'] / 1000) * boost_config['popularity']
                boost *= min(popularity_boost, 2.0)

            boosted_score = score * boost
            boosted.append((doc_id, boosted_score))

        # Re-sort by boosted scores
        boosted.sort(key=lambda x: x[1], reverse=True)
        return boosted
```

#### 7. No Monitoring or Evaluation

**Issue:** Silent failures go undetected in production.

**Solution: Continuous Monitoring**
```python
class RAGMonitor:
    """
    Production monitoring for RAG systems
    """
    def __init__(self):
        self.metrics_store = []
        self.alert_thresholds = {
            "latency_p95": 2000,  # ms
            "retrieval_quality": 0.7,  # minimum acceptable
            "generation_failure_rate": 0.05  # 5%
        }

    def log_query(self, query, results, latency, quality_score):
        """
        Log every query for analysis
        """
        metric = {
            "timestamp": time.time(),
            "query": query,
            "num_results": len(results),
            "latency": latency,
            "quality_score": quality_score,
            "success": quality_score > 0.7
        }

        self.metrics_store.append(metric)

        # Check for alerts
        self.check_alerts(metric)

    def check_alerts(self, metric):
        """
        Alert on anomalies
        """
        # Latency spike
        if metric['latency'] > self.alert_thresholds['latency_p95']:
            self.send_alert(f"High latency: {metric['latency']}ms")

        # Quality drop
        if metric['quality_score'] < self.alert_thresholds['retrieval_quality']:
            self.send_alert(f"Low quality: {metric['quality_score']}")

    def get_daily_metrics(self):
        """
        Calculate daily performance metrics
        """
        recent = [m for m in self.metrics_store if m['timestamp'] > time.time() - 86400]

        return {
            "total_queries": len(recent),
            "avg_latency": np.mean([m['latency'] for m in recent]),
            "p95_latency": np.percentile([m['latency'] for m in recent], 95),
            "success_rate": np.mean([m['success'] for m in recent]),
            "avg_quality": np.mean([m['quality_score'] for m in recent])
        }
```

### Failure Mode Summary Table

| Failure Mode | Impact | Detection | Solution |
|-------------|--------|-----------|----------|
| Poor chunking | Low recall | Manual review | Semantic splitting, 15% overlap |
| Embedding drift | Declining accuracy | A/B testing | Version tracking, migrations |
| Insufficient context | Hallucinations | User feedback | Context window expansion |
| Poor ranking | Low precision | Relevance metrics | Two-stage reranking |
| Single LLM dependency | Downtime | Health checks | Multi-provider fallback |
| Ignored metadata | Irrelevant results | User feedback | Metadata filters and boosts |
| No monitoring | Silent failures | Too late | Continuous logging and alerts |

---

## 7. Scaling to 100K+ Documents

### Architectural Patterns

#### Distributed Architecture

```python
import ray
from typing import List

@ray.remote
class DistributedVectorStore:
    """
    Sharded vector store across multiple nodes
    """
    def __init__(self, shard_id, dimension, shard_size):
        self.shard_id = shard_id
        self.index = faiss.IndexIVFPQ(
            faiss.IndexFlatL2(dimension),
            dimension,
            nlist=100,
            m=8,
            nbits=8
        )
        self.doc_ids = []

    def add_vectors(self, vectors, doc_ids):
        """Add vectors to this shard"""
        if not self.index.is_trained:
            self.index.train(vectors)
        self.index.add(vectors)
        self.doc_ids.extend(doc_ids)

    def search(self, query, k):
        """Search within this shard"""
        distances, indices = self.index.search(query, k)
        return distances, [self.doc_ids[i] for i in indices[0]]

class DistributedRAG:
    """
    Distributed RAG system for 100K+ documents
    """
    def __init__(self, num_shards=4, dimension=768):
        # Initialize Ray
        ray.init(ignore_reinit_error=True)

        # Create sharded vector stores
        self.shards = [
            DistributedVectorStore.remote(i, dimension, shard_size=None)
            for i in range(num_shards)
        ]
        self.num_shards = num_shards

    def add_documents(self, documents, embeddings):
        """
        Distribute documents across shards
        """
        shard_size = len(documents) // self.num_shards

        # Distribute to shards in parallel
        futures = []
        for i, shard in enumerate(self.shards):
            start = i * shard_size
            end = start + shard_size if i < self.num_shards - 1 else len(documents)

            shard_docs = documents[start:end]
            shard_embeddings = embeddings[start:end]
            shard_doc_ids = [doc['id'] for doc in shard_docs]

            future = shard.add_vectors.remote(
                np.array(shard_embeddings),
                shard_doc_ids
            )
            futures.append(future)

        # Wait for all shards to finish
        ray.get(futures)

    def search(self, query_embedding, k=10):
        """
        Search across all shards in parallel
        """
        # Query all shards in parallel
        futures = [
            shard.search.remote(np.array([query_embedding]), k)
            for shard in self.shards
        ]

        # Collect results
        results = ray.get(futures)

        # Merge and re-rank
        all_distances = []
        all_doc_ids = []

        for distances, doc_ids in results:
            all_distances.extend(distances[0])
            all_doc_ids.extend(doc_ids)

        # Sort by distance
        sorted_pairs = sorted(zip(all_distances, all_doc_ids))

        # Return top k
        return sorted_pairs[:k]
```

#### Tiered Storage Strategy

```python
class TieredStorageRAG:
    """
    Hot/Warm/Cold storage tiers for cost optimization
    """
    def __init__(self):
        # Hot tier: Recent/frequently accessed (in-memory)
        self.hot_index = faiss.IndexIVFPQ(
            faiss.IndexFlatL2(768), 768, 100, 8, 8
        )

        # Warm tier: Less frequent (SSD)
        self.warm_index_path = "/ssd/warm_index.faiss"

        # Cold tier: Archival (S3/object storage)
        self.cold_index_path = "s3://bucket/cold_index.faiss"

        # Access frequency tracking
        self.access_counts = {}
        self.last_access = {}

    def search(self, query, k=10):
        """
        Search with automatic tier promotion
        """
        # Try hot tier first
        results = self.search_hot(query, k)

        if len(results) < k:
            # Fallback to warm tier
            warm_results = self.search_warm(query, k - len(results))
            results.extend(warm_results)

        if len(results) < k:
            # Fallback to cold tier
            cold_results = self.search_cold(query, k - len(results))
            results.extend(cold_results)

        # Update access patterns
        for doc_id in [r['id'] for r in results]:
            self.update_access(doc_id)

        # Promote frequently accessed documents
        self.rebalance_tiers()

        return results

    def rebalance_tiers(self):
        """
        Move frequently accessed docs to hot tier
        Move cold docs to warm/cold tiers
        """
        # Promote: warm -> hot
        hot_candidates = sorted(
            self.access_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:1000]  # Top 1000 documents

        # Demote: hot -> warm
        cold_candidates = [
            doc_id for doc_id, last_access in self.last_access.items()
            if time.time() - last_access > 7 * 86400  # 7 days
        ]

        # Perform migrations
        self.migrate_to_hot(hot_candidates)
        self.migrate_to_warm(cold_candidates)
```

### Performance Optimization Strategies

#### Async Processing Pipeline

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncRAGPipeline:
    """
    Asynchronous RAG pipeline for high throughput
    """
    def __init__(self, max_workers=10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def process_query(self, query):
        """
        Async end-to-end RAG pipeline
        """
        # Parallel execution of independent steps
        embedding_task = self.get_embedding_async(query)

        # Wait for embedding
        query_embedding = await embedding_task

        # Parallel retrieval from multiple sources
        retrieval_tasks = [
            self.retrieve_from_index_async(query_embedding, index)
            for index in self.indexes
        ]

        # Wait for all retrievals
        retrieval_results = await asyncio.gather(*retrieval_tasks)

        # Merge and rerank
        merged = self.merge_results(retrieval_results)
        reranked = await self.rerank_async(query, merged)

        # Generate response
        response = await self.generate_async(query, reranked)

        return response

    async def get_embedding_async(self, text):
        """Async embedding"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self.embedder.embed,
            text
        )

    async def retrieve_from_index_async(self, query_embedding, index):
        """Async index search"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            index.search,
            query_embedding,
            10
        )

    async def batch_process(self, queries):
        """
        Process multiple queries concurrently
        """
        tasks = [self.process_query(q) for q in queries]
        return await asyncio.gather(*tasks)
```

#### Caching Strategy

```python
from functools import lru_cache
import hashlib
import redis

class RAGCache:
    """
    Multi-level caching for RAG systems
    """
    def __init__(self):
        # L1: In-memory LRU cache
        self.memory_cache = {}

        # L2: Redis for distributed caching
        self.redis_client = redis.Redis(host='localhost', port=6379)

        # Cache TTLs
        self.embedding_ttl = 3600  # 1 hour
        self.retrieval_ttl = 1800  # 30 minutes
        self.generation_ttl = 600   # 10 minutes

    def cache_key(self, prefix, content):
        """Generate cache key"""
        hash_obj = hashlib.sha256(content.encode())
        return f"{prefix}:{hash_obj.hexdigest()}"

    def get_embedding_cached(self, text):
        """
        Get embedding with caching
        """
        key = self.cache_key("emb", text)

        # Try L1 cache
        if key in self.memory_cache:
            return self.memory_cache[key]

        # Try L2 cache (Redis)
        cached = self.redis_client.get(key)
        if cached:
            embedding = np.frombuffer(cached, dtype=np.float32)
            self.memory_cache[key] = embedding  # Promote to L1
            return embedding

        # Cache miss: compute embedding
        embedding = self.embedder.embed(text)

        # Store in both caches
        self.memory_cache[key] = embedding
        self.redis_client.setex(
            key,
            self.embedding_ttl,
            embedding.tobytes()
        )

        return embedding

    def get_retrieval_cached(self, query):
        """
        Cache retrieval results
        """
        key = self.cache_key("retr", query)

        cached = self.redis_client.get(key)
        if cached:


---

**Navigation**: [← Part 3](./03_Embedding_Performance.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 5 →](./05_Integration_Deployment.md)
**Part 4 of 5** | Lines 1351-1800 of original document
