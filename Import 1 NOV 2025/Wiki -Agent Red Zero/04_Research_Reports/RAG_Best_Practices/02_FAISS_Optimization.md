# Part 2 of 5: FAISS Optimization

**Series**: RAG Best Practices
**Navigation**: [← Part 1](./01_Retrieval_Indexing.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 3 →](./03_Embedding_Performance.md)

---

                self.index.hnsw.efSearch = ef
                recall = self.evaluate_recall(query_vectors, ground_truth, k)
                print(f"efSearch={ef}: recall={recall:.3f}")

                if recall > best_recall:
                    best_recall = recall
                    best_ef = ef

                if recall > 0.95:
                    break

            self.index.hnsw.efSearch = best_ef
            print(f"Optimal efSearch: {best_ef} (recall: {best_recall:.3f})")

    def evaluate_recall(self, queries, ground_truth, k):
        """
        Calculate recall@k for evaluation
        """
        _, predictions = self.index.search(queries, k)

        recalls = []
        for pred, gt in zip(predictions, ground_truth):
            recall = len(set(pred) & set(gt)) / len(gt)
            recalls.append(recall)

        return np.mean(recalls)
```

### GPU Acceleration

```python
import faiss

def create_gpu_index(cpu_index, gpu_id=0):
    """
    Transfer index to GPU for faster search
    """
    res = faiss.StandardGpuResources()

    # Configure GPU options
    gpu_options = faiss.GpuClonerOptions()
    gpu_options.useFloat16 = True  # Use half precision for memory

    # Clone to GPU
    gpu_index = faiss.index_cpu_to_gpu(res, gpu_id, cpu_index, gpu_options)

    return gpu_index

# Multi-GPU support
def create_multi_gpu_index(cpu_index, gpu_ids=[0, 1, 2, 3]):
    """
    Distribute index across multiple GPUs
    """
    resources = [faiss.StandardGpuResources() for _ in gpu_ids]

    # Shard index across GPUs
    gpu_index = faiss.index_cpu_to_all_gpus(cpu_index, co=None, gpus=gpu_ids)

    return gpu_index
```

### Batch Processing Optimization

```python
def batch_search_optimized(index, queries, k=10, batch_size=1000):
    """
    Optimized batch search for high throughput
    """
    all_distances = []
    all_indices = []

    # FAISS is optimized for batch processing
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i+batch_size]
        distances, indices = index.search(batch, k)
        all_distances.append(distances)
        all_indices.append(indices)

    return np.vstack(all_distances), np.vstack(all_indices)
```

### Persistence and Serialization

```python
def save_index(index, filepath):
    """
    Save index to disk for persistence
    """
    faiss.write_index(index, filepath)

def load_index(filepath):
    """
    Load index from disk
    """
    return faiss.read_index(filepath)

# Memory-mapped index for very large datasets
def create_memory_mapped_index(filepath, dimension):
    """
    Create index that stays on disk (useful for >100GB indexes)
    """
    index = faiss.IndexFlatL2(dimension)

    # Convert to memory-mapped version
    index = faiss.index_factory(dimension, "Flat")

    # Write to disk
    faiss.write_index(index, filepath)

    # Load as memory-mapped
    index = faiss.read_index(filepath, faiss.IO_FLAG_MMAP)

    return index
```

### Performance Benchmarks

Based on production systems and research:

| Configuration | Dataset Size | Query Time | Recall@10 | Memory |
|--------------|--------------|------------|-----------|---------|
| IndexFlatL2 | 100K | 200ms | 100% | 300MB |
| IndexIVFFlat (nprobe=10) | 100K | 15ms | 98% | 300MB |
| IndexIVFPQ (m=8, nprobe=10) | 100K | 8ms | 95% | 24MB |
| IndexIVFPQ (m=8, nprobe=10) | 1M | 25ms | 95% | 240MB |
| IndexHNSW (M=32, ef=64) | 1M | 12ms | 97% | 800MB |
| IndexIVFPQ + GPU | 10M | 35ms | 95% | 2.4GB |

---

## 4. Vector Embedding Strategies

### Embedding Model Selection

#### Comparison: OpenAI vs. Open-Source

| Model | Dimension | MTEB Score | Latency | Cost | Use Case |
|-------|-----------|------------|---------|------|----------|
| text-embedding-3-large | 3072 | 64.6 | Medium | $0.13/1M | High accuracy, proprietary OK |
| text-embedding-3-small | 1536 | 62.3 | Fast | $0.02/1M | Cost-sensitive, good accuracy |
| sentence-transformers/all-MiniLM-L6-v2 | 384 | 58.8 | Very Fast | Free | Fast inference, memory-efficient |
| BAAI/bge-large-en-v1.5 | 1024 | 64.0 | Medium | Free | Open-source, high accuracy |
| intfloat/e5-large-v2 | 1024 | 62.3 | Medium | Free | Open-source, balanced |

#### Recommendation Decision Tree

```python
def select_embedding_model(
    budget_monthly: float,
    latency_requirement: str,  # "low", "medium", "high"
    accuracy_requirement: str,  # "baseline", "good", "best"
    data_privacy: bool  # True if data must stay on-premise
):
    """
    Decision tree for embedding model selection
    """
    if data_privacy:
        # Must use open-source
        if accuracy_requirement == "best":
            return "BAAI/bge-large-en-v1.5"
        elif latency_requirement == "low":
            return "sentence-transformers/all-MiniLM-L6-v2"
        else:
            return "intfloat/e5-large-v2"

    # Can use proprietary models
    if budget_monthly > 500:  # High budget
        if accuracy_requirement == "best":
            return "text-embedding-3-large"
        else:
            return "text-embedding-3-small"
    else:  # Cost-sensitive
        if accuracy_requirement == "best":
            return "BAAI/bge-large-en-v1.5"  # Open-source best
        else:
            return "sentence-transformers/all-MiniLM-L6-v2"  # Fast & free
```

### Implementation Patterns

#### OpenAI Embeddings

```python
from openai import OpenAI

client = OpenAI()

def get_openai_embedding(text, model="text-embedding-3-large"):
    """
    Get embedding from OpenAI API
    """
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

# Batch processing for efficiency
def get_openai_embeddings_batch(texts, model="text-embedding-3-large", batch_size=100):
    """
    Process embeddings in batches to minimize API calls
    """
    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        response = client.embeddings.create(
            input=batch,
            model=model
        )
        batch_embeddings = [item.embedding for item in response.data]
        embeddings.extend(batch_embeddings)

    return embeddings
```

#### Sentence Transformers (Open-Source)

```python
from sentence_transformers import SentenceTransformer
import torch

class EmbeddingService:
    """
    Production-grade embedding service with caching and batching
    """
    def __init__(self, model_name="BAAI/bge-large-en-v1.5", device=None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = SentenceTransformer(model_name, device=device)
        self.cache = {}  # Simple cache (use Redis in production)

    def embed(self, text):
        """
        Single text embedding with caching
        """
        if text in self.cache:
            return self.cache[text]

        embedding = self.model.encode(text, convert_to_numpy=True)
        self.cache[text] = embedding
        return embedding

    def embed_batch(self, texts, batch_size=32, show_progress=False):
        """
        Efficient batch embedding
        """
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
            normalize_embeddings=True  # L2 normalization
        )
        return embeddings

    def embed_with_pooling(self, text, pooling="mean"):
        """
        Custom pooling strategies
        """
        # Get token embeddings
        token_embeddings = self.model.encode(
            text,
            output_value="token_embeddings"
        )

        if pooling == "mean":
            return token_embeddings.mean(axis=0)
        elif pooling == "max":
            return token_embeddings.max(axis=0)
        elif pooling == "cls":
            return token_embeddings[0]  # CLS token
        else:
            raise ValueError(f"Unknown pooling: {pooling}")
```

### Document Categorization Strategies

#### Category-Aware Embedding

```python
class CategoryAwareRAG:
    """
    RAG system with category-based routing
    """
    def __init__(self, categories):
        self.categories = categories  # e.g., ["technical", "business", "legal"]
        self.category_embeddings = self.build_category_embeddings()
        self.indexes = {cat: self.create_index() for cat in categories}
        self.embedder = EmbeddingService()

    def build_category_embeddings(self):
        """
        Create representative embeddings for each category
        """
        category_descriptions = {
            "technical": "software engineering, architecture, code, API documentation",
            "business": "strategy, market analysis, financial reports, business plans",
            "legal": "contracts, compliance, regulations, legal documents"
        }

        embeddings = {}
        for cat, desc in category_descriptions.items():
            embeddings[cat] = self.embedder.embed(desc)

        return embeddings

    def categorize_document(self, text):
        """
        Assign document to most relevant category
        """
        doc_embedding = self.embedder.embed(text)

        # Calculate similarity to each category
        similarities = {}
        for cat, cat_embedding in self.category_embeddings.items():
            similarity = np.dot(doc_embedding, cat_embedding)
            similarities[cat] = similarity

        # Return most similar category
        return max(similarities, key=similarities.get)

    def add_document(self, doc_id, text):
        """
        Add document to appropriate category index
        """
        category = self.categorize_document(text)
        embedding = self.embedder.embed(text)

        self.indexes[category].add(embedding)

        return category

    def search(self, query, categories=None, k=10):
        """
        Search in specific categories or all categories
        """
        if categories is None:
            # Determine most relevant categories for query
            query_cat = self.categorize_document(query)
            categories = [query_cat]

        query_embedding = self.embedder.embed(query)

        all_results = []
        for cat in categories:
            distances, indices = self.indexes[cat].search(query_embedding, k)
            all_results.extend([(cat, idx, dist) for idx, dist in zip(indices[0], distances[0])])

        # Sort by distance and return top k
        all_results.sort(key=lambda x: x[2])
        return all_results[:k]
```

#### Multi-Vector Embeddings

```python
class MultiVectorRAG:
    """
    Store multiple embeddings per document for different aspects
    """
    def __init__(self):
        self.embedder = EmbeddingService()

        # Different indexes for different document aspects
        self.title_index = faiss.IndexFlatL2(1024)
        self.content_index = faiss.IndexFlatL2(1024)
        self.summary_index = faiss.IndexFlatL2(1024)

        self.doc_store = {}

    def add_document(self, doc_id, title, content, summary):
        """
        Create and store multiple embeddings per document
        """
        title_emb = self.embedder.embed(title)
        content_emb = self.embedder.embed(content)
        summary_emb = self.embedder.embed(summary)

        # Add to respective indexes
        self.title_index.add(np.array([title_emb]))
        self.content_index.add(np.array([content_emb]))
        self.summary_index.add(np.array([summary_emb]))

        # Store document
        self.doc_store[doc_id] = {
            "title": title,
            "content": content,
            "summary": summary
        }

    def search_adaptive(self, query, query_type="auto", k=10):
        """
        Adaptively search based on query type
        """
        query_emb = self.embedder.embed(query)

        if query_type == "auto":
            # Determine query type from characteristics
            if len(query.split()) <= 5:
                query_type = "title"  # Short queries search titles
            elif "summarize" in query.lower() or "overview" in query.lower():
                query_type = "summary"
            else:
                query_type = "content"

        # Search appropriate index
        if query_type == "title":
            distances, indices = self.title_index.search(np.array([query_emb]), k)
        elif query_type == "summary":
            distances, indices = self.summary_index.search(np.array([query_emb]), k)
        else:
            distances, indices = self.content_index.search(np.array([query_emb]), k)

        return indices[0], distances[0]
```

---

## 5. Performance Benchmarks

### Evaluation Framework

```python
import time
from typing import List, Tuple

class RAGBenchmark:
    """
    Comprehensive RAG system benchmarking
    """
    def __init__(self, rag_system, test_queries, ground_truth):
        self.rag_system = rag_system
        self.test_queries = test_queries
        self.ground_truth = ground_truth

    def benchmark_retrieval(self, k=10):
        """
        Measure retrieval metrics
        """
        metrics = {
            "precision": [],
            "recall": [],
            "f1": [],
            "ndcg": [],
            "mrr": [],
            "latency": []
        }



---

**Navigation**: [← Part 1](./01_Retrieval_Indexing.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 3 →](./03_Embedding_Performance.md)
**Part 2 of 5** | Lines 451-900 of original document
