# Part 1 of 5: Retrieval & Indexing

**Series**: RAG Best Practices
**Navigation**: [📚 Series Overview](./00_Series_Overview.md) | [Part 2 →](./02_FAISS_Optimization.md)

---

# Hierarchical RAG Implementation Best Practices: A Comprehensive Guide

**Research Date:** October 16, 2025
**Focus Areas:** Two-round retrieval, hierarchical indexing, FAISS optimization, production scaling
**Confidence Level:** High (based on academic papers, production case studies, and official documentation)

---

## Executive Summary

This report synthesizes best practices for implementing hierarchical Retrieval-Augmented Generation (RAG) systems at production scale. Key findings include:

- **Two-round retrieval architectures** (like RAPTOR and HM-RAG) significantly improve performance on complex, multi-hop queries
- **FAISS optimization** through proper index selection and GPU acceleration can achieve 98%+ precision with minimal memory footprint
- **Chunk size optimization** (250-400 tokens with 15% overlap) balances context and precision
- **Scaling to 100K+ documents** requires distributed architecture, hybrid indexing, and careful resource management
- **Common failure modes** include poor chunking, embedding drift, and insufficient evaluation frameworks

---

## Table of Contents

1. [Two-Round Retrieval Architectures](#1-two-round-retrieval-architectures)
2. [Category-Based Indexing Strategies](#2-category-based-indexing-strategies)
3. [FAISS Optimization for Production](#3-faiss-optimization-for-production)
4. [Vector Embedding Strategies](#4-vector-embedding-strategies)
5. [Performance Benchmarks](#5-performance-benchmarks)
6. [Common Pitfalls and Failure Modes](#6-common-pitfalls-and-failure-modes)
7. [Scaling to 100K+ Documents](#7-scaling-to-100k-documents)
8. [LangChain-FAISS Integration Patterns](#8-langchain-faiss-integration-patterns)
9. [Production Deployment Checklist](#9-production-deployment-checklist)

---

## 1. Two-Round Retrieval Architectures

### Overview

Two-round (multi-stage) retrieval systems significantly outperform single-pass retrieval on complex queries requiring multi-hop reasoning. These architectures typically involve:

1. **First Stage:** Broad retrieval using fast approximate methods
2. **Second Stage:** Reranking and refinement using more sophisticated models

### RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval

**Architecture:**
- Recursively embeds, clusters, and summarizes text at multiple levels of abstraction
- Creates a hierarchical tree structure from documents
- Enables retrieval at different granularity levels

**Key Features:**
- **Tree Traversal:** Sequentially traverses layers to select relevant nodes
- **Collapsed Tree:** Searches across all layers simultaneously for optimal granularity

**Implementation Example:**

```python
# RAPTOR Implementation Pattern
from raptor import RetrievalAugmentation
from transformers import AutoTokenizer, AutoModel

# Initialize RAPTOR with custom models
raptor = RetrievalAugmentation(
    summarization_model="gpt-3.5-turbo",
    qa_model="gpt-4",
    embedding_model="text-embedding-3-large"
)

# Build hierarchical tree from documents
raptor.add_documents(
    documents=document_list,
    max_length=512,
    summarization_length=100
)

# Query with tree traversal
results = raptor.answer_question(
    question="What are the key factors?",
    retrieval_mode="tree_traversal",  # or "collapsed_tree"
    tree_depth=3
)
```

**Official Repository:** [github.com/parthsarthi03/raptor](https://github.com/parthsarthi03/raptor)

### HM-RAG: Hierarchical Multi-Agent Multimodal RAG

**Architecture:**
- Hierarchical multi-agent framework for dynamic query adaptation
- Supports multimodal retrieval (text, images, tables)
- Agent-based coordination for complex queries

**Use Cases:**
- Complex enterprise document collections
- Multimodal content retrieval
- Multi-step reasoning tasks

### LevelRAG: Multi-hop Logic Planning

**Architecture:**
- Two-level system: high-level and low-level searchers
- Query decomposition into atomic sub-queries
- Iterative refinement and aggregation

**Process:**
1. High-level searcher processes user query
2. Decomposes into atomic queries
3. Low-level searchers rewrite and refine each query
4. Aggregates results before generation

### HF-RAG: Hierarchical Fusion

**Two-Stage Process:**
1. **Intra-source fusion:** Reciprocal rank fusion within each IR system
2. **Inter-source fusion:** Z-score normalization across sources

**Benefits:**
- Combines multiple retrieval systems effectively
- Balances precision and recall
- Robust to individual ranker failures

---

## 2. Category-Based Indexing Strategies

### Hierarchical vs. Flat vs. Hybrid Indexing

#### Flat Indexing
**Characteristics:**
- Brute-force search through all vectors
- No modifications to input vectors
- Simple but slow at scale

**Use Cases:**
- Small datasets (<10K documents)
- Exact search requirements
- Prototyping and baseline comparisons

**Implementation:**
```python
import faiss
import numpy as np

# Create flat index (exact search)
dimension = 768  # embedding dimension
index = faiss.IndexFlatL2(dimension)

# Add vectors
vectors = np.random.random((10000, dimension)).astype('float32')
index.add(vectors)

# Search
query = np.random.random((1, dimension)).astype('float32')
distances, indices = index.search(query, k=10)
```

#### Cluster-Based Indexing (IVF)

**Characteristics:**
- Partitions dataset into clusters
- Searches only most relevant clusters
- Dramatically reduces distance computations

**Advantages:**
- 10-100x faster than flat indexing
- Tunable speed/accuracy tradeoff
- Suitable for 100K-10M documents

**Implementation:**
```python
# IVF index with PQ compression
nlist = 100  # number of clusters
m = 8        # number of subquantizers
nbits = 8    # bits per subquantizer

# Create quantizer for clustering
quantizer = faiss.IndexFlatL2(dimension)

# Create IVF index with PQ
index = faiss.IndexIVFPQ(quantizer, dimension, nlist, m, nbits)

# Train on representative sample
train_data = vectors[:50000]  # use subset for training
index.train(train_data)

# Add all vectors
index.add(vectors)

# Search parameters
index.nprobe = 10  # search 10 clusters (tune for speed/accuracy)
distances, indices = index.search(query, k=10)
```

#### Hierarchical Indexing

**Characteristics:**
- Multi-level tree structure
- Parent nodes contain summaries/abstracts
- Child nodes contain detailed content

**Benefits:**
- Efficient for multi-granularity retrieval
- Supports complex queries requiring context
- Natural fit for hierarchical documents

**Architecture Pattern:**
```python
# Hierarchical indexing pattern
class HierarchicalIndex:
    def __init__(self, levels=3):
        self.levels = levels
        self.indexes = []

        # Create index for each level
        for level in range(levels):
            index = faiss.IndexIVFPQ(
                faiss.IndexFlatL2(dimension),
                dimension,
                nlist=100 * (level + 1),  # more clusters at deeper levels
                m=8,
                nbits=8
            )
            self.indexes.append(index)

    def add_document(self, doc, summaries):
        """
        Add document at multiple granularity levels
        summaries: list of text at each level (abstract → section → paragraph)
        """
        for level, summary in enumerate(summaries):
            embedding = self.embed_text(summary)
            self.indexes[level].add(embedding)

    def search_hierarchical(self, query, start_level=0):
        """
        Start at coarse level, drill down to fine-grained
        """
        results = []
        current_query = query

        for level in range(start_level, self.levels):
            query_embedding = self.embed_text(current_query)
            distances, indices = self.indexes[level].search(query_embedding, k=10)
            results.append((level, distances, indices))

            # Refine query based on retrieved content (optional)
            if level < self.levels - 1:
                current_query = self.refine_query(current_query, results[-1])

        return results
```

### Locality Sensitive Hashing (LSH)

**Characteristics:**
- Hash similar vectors into same "buckets"
- Probabilistic approximate search
- Very fast for high-dimensional data

**Use Cases:**
- Ultra-low latency requirements
- Very large datasets (>10M documents)
- Acceptable false negative rate

**Implementation:**
```python
# LSH index in FAISS
nbits = 256  # hash size

index = faiss.IndexLSH(dimension, nbits)
index.add(vectors)

# Fast approximate search
distances, indices = index.search(query, k=10)
```

### Hybrid Indexing Strategy

**Recommended Production Pattern:**

```python
class HybridRAGIndex:
    """
    Combines dense vectors, sparse keywords, and metadata filtering
    """
    def __init__(self):
        # Dense vector index (semantic search)
        self.dense_index = self.create_ivf_index()

        # Sparse index (keyword search)
        self.sparse_index = self.create_bm25_index()

        # Metadata store (filtering)
        self.metadata_db = {}  # or use PostgreSQL, Elasticsearch

    def create_ivf_index(self):
        """Create optimized FAISS index"""
        quantizer = faiss.IndexFlatL2(768)
        index = faiss.IndexIVFPQ(quantizer, 768, 100, 8, 8)
        return index

    def create_bm25_index(self):
        """Create sparse keyword index"""
        from rank_bm25 import BM25Okapi
        return BM25Okapi

    def search_hybrid(self, query, filters=None, alpha=0.5):
        """
        Hybrid search combining dense and sparse retrieval
        alpha: weight for dense vs sparse (0=sparse only, 1=dense only)
        """
        # Dense retrieval
        dense_scores = self.dense_search(query)

        # Sparse retrieval
        sparse_scores = self.sparse_search(query)

        # Combine scores
        combined = alpha * dense_scores + (1 - alpha) * sparse_scores

        # Apply metadata filters
        if filters:
            combined = self.apply_filters(combined, filters)

        return self.get_top_k(combined, k=10)

    def apply_filters(self, results, filters):
        """
        Filter by metadata: date range, document type, category, etc.
        """
        filtered = []
        for doc_id, score in results:
            metadata = self.metadata_db.get(doc_id, {})
            if self.matches_filters(metadata, filters):
                filtered.append((doc_id, score))
        return filtered
```

---

## 3. FAISS Optimization for Production

### Index Selection Guide

| Index Type | Speed | Memory | Accuracy | Use Case |
|-----------|-------|--------|----------|----------|
| `IndexFlatL2` | Slow | High | 100% | <10K docs, baseline |
| `IndexIVFFlat` | Fast | High | 95-99% | 10K-100K docs |
| `IndexIVFPQ` | Very Fast | Low | 90-98% | 100K-10M docs |
| `IndexHNSW` | Fast | Medium | 95-99% | 100K-1M docs, low latency |
| `IndexLSH` | Very Fast | Low | 85-95% | >10M docs, approx OK |

### Production-Grade Configuration

```python
import faiss
import numpy as np

class ProductionFAISSIndex:
    """
    Production-optimized FAISS configuration
    """
    def __init__(self, dimension=768, data_size=1000000):
        self.dimension = dimension
        self.data_size = data_size
        self.index = self.create_optimized_index()

    def create_optimized_index(self):
        """
        Choose optimal index based on data size
        """
        if self.data_size < 10000:
            # Small dataset: use exact search
            return faiss.IndexFlatL2(self.dimension)

        elif self.data_size < 100000:
            # Medium dataset: IVF without compression
            nlist = 100
            quantizer = faiss.IndexFlatL2(self.dimension)
            index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist)
            return index

        elif self.data_size < 1000000:
            # Large dataset: IVF with PQ compression
            nlist = 4096
            m = 8  # number of subquantizers
            nbits = 8

            quantizer = faiss.IndexFlatL2(self.dimension)
            index = faiss.IndexIVFPQ(quantizer, self.dimension, nlist, m, nbits)
            return index

        else:
            # Very large dataset: HNSW for speed
            M = 32  # number of connections
            index = faiss.IndexHNSWFlat(self.dimension, M)
            index.hnsw.efConstruction = 80
            return index

    def train_and_add(self, vectors, batch_size=10000):
        """
        Efficient training and indexing with batching
        """
        # Train on representative sample (10% of data or max 1M)
        train_size = min(len(vectors) // 10, 1000000)
        train_data = vectors[:train_size]

        if hasattr(self.index, 'train'):
            print(f"Training index on {train_size} vectors...")
            self.index.train(train_data)

        # Add vectors in batches for memory efficiency
        print(f"Adding {len(vectors)} vectors in batches...")
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            self.index.add(batch)
            if (i // batch_size) % 10 == 0:
                print(f"  Added {i + len(batch)}/{len(vectors)} vectors")

    def optimize_search_params(self, query_vectors, ground_truth, k=10):
        """
        Auto-tune search parameters for optimal speed/accuracy
        """
        if isinstance(self.index, faiss.IndexIVF):
            best_nprobe = None
            best_recall = 0

            # Test different nprobe values
            for nprobe in [1, 5, 10, 20, 50, 100]:
                self.index.nprobe = nprobe
                recall = self.evaluate_recall(query_vectors, ground_truth, k)
                print(f"nprobe={nprobe}: recall={recall:.3f}")

                if recall > best_recall:
                    best_recall = recall
                    best_nprobe = nprobe

                # Stop if recall is good enough
                if recall > 0.95:
                    break

            self.index.nprobe = best_nprobe
            print(f"Optimal nprobe: {best_nprobe} (recall: {best_recall:.3f})")

        elif isinstance(self.index, faiss.IndexHNSW):
            # Tune efSearch for HNSW
            best_ef = None
            best_recall = 0

            for ef in [16, 32, 64, 128, 256]:


---

**Navigation**: [📚 Series Overview](./00_Series_Overview.md) | [Part 2 →](./02_FAISS_Optimization.md)
**Part 1 of 5** | Lines 1-450 of original document
