---
title: "Agent Zero - 01 Architecture Specs"
category: "03_Agent_Zero_Core/02_Technical_Specs/01_Specifications"
part: "1 of 3"
line_count: 304
last_updated: 2025-10-25
status: published
tags: ['agent-zero', 'roadmap', 'core']
related:
  - "02_Component_Specs.md"
---

# Agent Zero 2.0 Technical Specifications
## Implementation Reference for Development Team

**Document Version:** 1.0
**Created:** 2025-10-16
**Purpose:** Detailed technical specifications for implementing Agent Zero 2.0 enhancements

---

## Table of Contents

1. [Hierarchical RAG System](#1-hierarchical-rag-system)
2. [OSINT Collection Module](#2-osint-collection-module)
3. [SuperClaude Integration Bridge](#3-superclaude-integration-bridge)
4. [Tool Orchestration System](#4-tool-orchestration-system)
5. [API Specifications](#5-api-specifications)
6. [Data Schemas](#6-data-schemas)
7. [Performance Benchmarks](#7-performance-benchmarks)

---

## 1. Hierarchical RAG System

### 1.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│ Agent Query: "Find information about CVE-2024-1234"    │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ HierarchicalRAG.hierarchical_search()                   │
│                                                           │
│ ROUND 1: Category-Level Search                          │
│ ├─ Embed query with sentence-transformers              │
│ ├─ Search category embeddings                           │
│ ├─ Rank categories by relevance                         │
│ └─ Select top 3 categories                              │
│                                                           │
│ ROUND 2: Document-Level Search                          │
│ ├─ For each selected category:                          │
│ │   ├─ Search documents within category                 │
│ │   ├─ Apply similarity threshold (0.6)                 │
│ │   └─ Retrieve top 5 documents                         │
│ ├─ Boost scores by category relevance                   │
│ ├─ Merge and deduplicate results                        │
│ └─ Return top 15 documents                              │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ Returns: List[(Document, boosted_score)]                │
│ - Precision: 8x better than flat search                 │
│ - Latency: <100ms category overhead                     │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Class Specifications

#### HierarchicalRAG Class

**File:** `python/helpers/memory_rag.py`

```python
class HierarchicalRAG:
    """
    Hierarchical Retrieval-Augmented Generation

    Attributes:
        memory (Memory): Base memory instance with FAISS
        categories (Dict[str, List[str]]): Category -> Doc IDs mapping
        _category_embeddings (Dict[str, np.ndarray]): Cached category embeddings

    Methods:
        hierarchical_search() -> List[Tuple[Document, float]]
        auto_categorize_document() -> str
        add_document_with_category() -> str
        rebuild_category_index() -> None
    """

    def __init__(self, memory: Memory):
        """Initialize with existing Memory instance"""
        pass

    async def hierarchical_search(
        self,
        query: str,
        top_k_categories: int = 3,
        docs_per_category: int = 5,
        threshold: float = 0.6
    ) -> List[Tuple[Document, float]]:
        """
        Two-round hierarchical search

        Time Complexity: O(log N) for category search + O(K) for document search
        Space Complexity: O(C * E) where C=categories, E=embedding_dim

        Returns: Ranked documents with boosted relevance scores
        """
        pass

    async def _search_categories(
        self,
        query: str,
        top_k: int
    ) -> List[Tuple[str, float]]:
        """
        Round 1: Category-level search

        Algorithm:
        1. Load category embeddings (cached)
        2. Embed query using sentence-transformers
        3. Compute cosine similarity to each category
        4. Return top K categories

        Performance: O(C * E) where C=categories, E=embedding_dim
        """
        pass

    async def _search_within_category(
        self,
        category: str,
        query: str,
        limit: int,
        threshold: float
    ) -> List[Document]:
        """
        Round 2: Document search within category

        Uses existing FAISS search with metadata filter:
        filter=f'metadata["category"] == "{category}"'

        Performance: O(log D) where D=docs in category (FAISS)
        """
        pass

    def _compute_category_embedding(
        self,
        category: str
    ) -> np.ndarray:
        """
        Compute category embedding from representative documents

        Strategy:
        1. Sample up to 10 representative documents
        2. Average their embeddings
        3. Normalize result
        4. Cache for future use

        Performance: O(S * E) where S=sample_size, E=embedding_dim
        """
        pass
```

### 1.3 Data Structures

#### Category Index Schema

**File:** `memory/{subdir}/categories.json`

```json
{
    "security_vulnerabilities": [
        "doc_id_abc123",
        "doc_id_def456",
        "doc_id_ghi789"
    ],
    "code_solutions": [
        "doc_id_jkl012",
        "doc_id_mno345"
    ],
    "system_administration": [
        "doc_id_pqr678"
    ]
}
```

#### Enhanced Document Metadata

```python
{
    "id": "doc_abc123",
    "timestamp": "2025-10-16 10:30:00",
    "area": "main",  # Existing: MAIN, FRAGMENTS, SOLUTIONS, INSTRUMENTS
    "category": "security_vulnerabilities",  # NEW
    "auto_categorized": true,  # NEW: Was this auto-categorized?
    "category_confidence": 0.85,  # NEW: LLM confidence in category
    "keywords": ["cve", "vulnerability", "exploit"],  # NEW: Extracted keywords
    "source": "user_input",  # NEW: user_input, knowledge_import, etc.
}
```

### 1.4 Algorithm Pseudocode

#### Two-Round Retrieval

```
FUNCTION hierarchical_search(query, top_k_categories=3, docs_per_category=5):
    # Round 1: Category Search
    query_embedding = embed(query)
    category_scores = []

    FOR EACH category IN categories:
        category_embedding = get_category_embedding(category)
        similarity = cosine_similarity(query_embedding, category_embedding)
        category_scores.append((category, similarity))

    relevant_categories = top_k(category_scores, k=top_k_categories)

    # Round 2: Document Search
    all_documents = []

    FOR EACH (category, category_score) IN relevant_categories:
        # FAISS search within category
        docs = faiss_search(
            query=query,
            filter=f'category == "{category}"',
            limit=docs_per_category
        )

        # Boost document scores by category relevance
        FOR EACH doc IN docs:
            boosted_score = doc.score * category_score
            all_documents.append((doc, boosted_score))

    # Merge and rank
    all_documents = sort_by_score(all_documents, reverse=True)
    all_documents = deduplicate(all_documents)

    RETURN all_documents[:top_k_categories * docs_per_category]
```

### 1.5 Performance Optimization

#### Caching Strategy

```python
class HierarchicalRAG:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.categories = self._load_categories()

        # Caches
        self._category_embeddings_cache = {}  # category -> embedding
        self._cache_ttl = 3600  # 1 hour
        self._cache_timestamps = {}  # category -> timestamp
```

#### Lazy Loading

```python
async def _get_category_embedding(self, category: str) -> np.ndarray:
    """Get category embedding with lazy loading and caching"""

    # Check cache
    if category in self._category_embeddings_cache:
        if time.time() - self._cache_timestamps[category] < self._cache_ttl:
            return self._category_embeddings_cache[category]

    # Compute and cache
    embedding = await self._compute_category_embedding(category)
    self._category_embeddings_cache[category] = embedding
    self._cache_timestamps[category] = time.time()

    return embedding
```

### 1.6 Testing Requirements

#### Unit Tests

```python
# tests/test_hierarchical_rag.py

async def test_category_search():
    """Test category-level search accuracy"""
    rag = HierarchicalRAG(memory)

    categories = await rag._search_categories(
        query="CVE vulnerability analysis",
        top_k=3
    )

    assert len(categories) == 3
    assert categories[0][0] == "security_vulnerabilities"
    assert categories[0][1] > 0.7  # High confidence

async def test_hierarchical_vs_flat_search():
    """Benchmark hierarchical vs flat search precision"""
    queries = load_test_queries()  # 100 test queries
    relevant_docs = load_ground_truth()  # Known relevant documents

    # Flat search
    flat_precision = evaluate_precision(memory.search, queries, relevant_docs)

    # Hierarchical search
    hier_precision = evaluate_precision(rag.hierarchical_search, queries, relevant_docs)

    assert hier_precision / flat_precision >= 8.0  # 8x improvement target
```

#### Performance Benchmarks

```python
async def benchmark_hierarchical_search():
    """Measure search performance"""
    import time

    queries = generate_test_queries(n=1000)
    times = []

    for query in queries:
        start = time.time()
        results = await rag.hierarchical_search(query)
        elapsed = time.time() - start
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    p95_time = np.percentile(times, 95)

    assert avg_time < 0.150  # <150ms average
    assert p95_time < 0.300  # <300ms p95
```

---

## 2. OSINT Collection Module

### 2.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│ User Query: "Collect OSINT on CVE-2024-1234"           │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ OSINTCollector.execute()                                 │
│                                                           │
│ Step 1: Multi-Source Collection                         │
│ ├─ Web Search (DuckDuckGo) - 20 results                │
│ ├─ News Search (DuckDuckGo) - 20 results               │
│ └─ [Future] Social Media, RSS feeds                    │
│                                                           │
│ Step 2: Entity Extraction                               │
│ ├─ CVE patterns: CVE-\d{4}-\d{4,7}                    │
│ ├─ IP addresses: \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}  │
│ ├─ Domains: [a-z0-9-]+\.[a-z]{2,}                     │
│ ├─ Emails: [a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}     │
│ └─ URLs: http[s]?://...                                │
│                                                           │
│ Step 3: Intelligence Storage                            │
│ ├─ Create Document with metadata                        │
│ ├─ Store in FAISS memory                                │
│ └─ Category: "osint"                                    │
│                                                           │
│ Step 4: Response Formatting                             │
│ └─ Generate markdown report                             │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ Returns: Formatted intelligence report                   │
│ - Multi-source results                                   │
│ - Extracted entities                                     │
│ - Stored in memory                                       │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Tool Specification

#### OSINTCollector Class

**File:** `python/tools/osint_collector.py`

```python
class OSINTCollector(Tool):
    """
    Open-Source Intelligence Collection Tool



---

**Part 1 of 3** | Next: [02_Component_Specs.md](02_Component_Specs.md)
