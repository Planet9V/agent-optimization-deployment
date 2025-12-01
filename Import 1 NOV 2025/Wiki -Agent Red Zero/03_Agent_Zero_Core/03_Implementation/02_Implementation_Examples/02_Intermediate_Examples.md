---
title: "Agent Zero - 02 Intermediate Examples"
category: "03_Agent_Zero_Core/03_Implementation/02_Implementation_Examples"
part: "2 of 3"
line_count: 283
last_updated: 2025-10-25
status: published
tags: ['agent-zero', 'roadmap', 'core']
related:
  - "01_Basic_Examples.md"
  - "03_Advanced_Examples.md"
---

                response += chunk

            category = response.strip().lower()
            # Clean category name
            category = ''.join(c if c.isalnum() or c in [' ', '_'] else '' for c in category)
            category = category.replace(' ', '_')

            return category if category else "general"

        except Exception as e:
            print(f"LLM categorization failed: {e}")
            return self._extract_topic(doc)

    def _extract_topic(self, doc: Document, max_words: int = 3) -> str:
        """Extract topic from document using simple heuristics"""
        import re

        # Get area if available
        if "area" in doc.metadata:
            return doc.metadata["area"]

        # Extract significant words
        words = re.findall(r'\b\w+\b', doc.page_content.lower())

        # Filter stopwords
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did'}
        significant = [w for w in words if w not in stopwords and len(w) > 3]

        if significant:
            topic = '_'.join(significant[:max_words])
            return topic if len(topic) < 50 else topic[:50]

        return "general"

    async def add_document_with_category(
        self,
        doc: Document,
        category: Optional[str] = None,
        llm_model = None
    ) -> str:
        """
        Add document with automatic categorization

        Args:
            doc: Document to add
            category: Explicit category (optional)
            llm_model: LLM for auto-categorization (optional)

        Returns:
            Document ID
        """
        # Auto-categorize if not provided
        if not category:
            category = await self.auto_categorize_document(doc, llm_model)

        # Add category to metadata
        doc.metadata["category"] = category
        doc.metadata["auto_categorized"] = (category is None)

        # Insert document using existing memory system
        doc_ids = await self.memory.insert_documents([doc])
        doc_id = doc_ids[0]

        # Update category index
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(doc_id)

        # Save categories
        self._save_categories()

        self._stats["documents_added"] += 1

        return doc_id

    def get_stats(self) -> Dict[str, any]:
        """Get RAG statistics"""
        return dict(self._stats)

    def clear_cache(self):
        """Clear category embedding cache"""
        self._category_embeddings_cache.clear()
        self._cache_timestamps.clear()
        self._stats["cache_cleared"] += 1
```

### 1.2 Integration with Memory

```python
# Add to python/helpers/memory.py

class Memory:
    # ... existing code ...

    def enable_hierarchical_rag(self):
        """Enable hierarchical RAG enhancement"""
        from python.helpers.memory_rag import HierarchicalRAG
        if not hasattr(self, '_rag'):
            self._rag = HierarchicalRAG(self)
        return self._rag

    async def search_hierarchical(
        self,
        query: str,
        top_k_categories: int = 3,
        docs_per_category: int = 5,
        threshold: float = 0.6
    ):
        """
        Hierarchical two-round search

        Falls back to regular search if RAG not enabled
        """
        if hasattr(self, '_rag'):
            return await self._rag.hierarchical_search(
                query,
                top_k_categories,
                docs_per_category,
                threshold
            )
        else:
            # Fallback to regular search
            docs = await self.search_similarity_threshold(
                query,
                limit=top_k_categories * docs_per_category,
                threshold=threshold
            )
            return [(doc, getattr(doc, 'score', 0.5)) for doc in docs]

    def get_rag_stats(self) -> Dict[str, any]:
        """Get RAG statistics if enabled"""
        if hasattr(self, '_rag'):
            return self._rag.get_stats()
        return {}
```

### 1.3 Usage Examples

```python
# Example 1: Basic hierarchical search
from python.helpers.memory import Memory

async def example_hierarchical_search():
    # Get memory instance
    memory = await Memory.get_by_subdir("default")

    # Enable hierarchical RAG
    rag = memory.enable_hierarchical_rag()

    # Search with hierarchical retrieval
    results = await memory.search_hierarchical(
        query="CVE vulnerability analysis methodologies",
        top_k_categories=3,
        docs_per_category=5,
        threshold=0.6
    )

    # Process results
    for doc, score in results:
        print(f"Score: {score:.3f}")
        print(f"Category: {doc.metadata.get('category', 'unknown')}")
        print(f"Content: {doc.page_content[:200]}...\n")

    # Get statistics
    stats = memory.get_rag_stats()
    print(f"RAG Stats: {stats}")

# Example 2: Adding documents with auto-categorization
async def example_add_with_category():
    memory = await Memory.get_by_subdir("default")
    rag = memory.enable_hierarchical_rag()

    # Create document
    from langchain_core.documents import Document
    doc = Document(
        page_content="Analysis of CVE-2024-1234 remote code execution vulnerability...",
        metadata={"source": "security_report", "timestamp": "2025-10-16"}
    )

    # Add with auto-categorization
    doc_id = await rag.add_document_with_category(
        doc,
        category=None,  # Auto-categorize
        llm_model=agent.config.chat_model  # Use agent's LLM
    )

    print(f"Document added with ID: {doc_id}")
    print(f"Category: {doc.metadata['category']}")

# Example 3: Comparing flat vs hierarchical search
async def example_comparison():
    memory = await Memory.get_by_subdir("default")
    rag = memory.enable_hierarchical_rag()

    query = "authentication security best practices"

    # Flat search
    import time
    start = time.time()
    flat_results = await memory.search_similarity_threshold(
        query, limit=15, threshold=0.6
    )
    flat_time = time.time() - start

    # Hierarchical search
    start = time.time()
    hier_results = await memory.search_hierarchical(
        query, top_k_categories=3, docs_per_category=5
    )
    hier_time = time.time() - start

    print(f"Flat search: {len(flat_results)} results in {flat_time*1000:.1f}ms")
    print(f"Hierarchical search: {len(hier_results)} results in {hier_time*1000:.1f}ms")
    print(f"\nFlat top result score: {getattr(flat_results[0], 'score', 0):.3f}")
    print(f"Hierarchical top result score: {hier_results[0][1]:.3f}")
```

---

## 2. OSINT Collector

### 2.1 Complete OSINTCollector Implementation

```python
# python/tools/osint_collector.py
"""
Complete OSINT Collection Tool for Agent Zero 2.0
Production-ready with error handling, rate limiting, and ethics
"""

from python.helpers.tool import Tool, Response
from python.helpers import duckduckgo_search
from agent import Agent
import json, re, asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import time

class OSINTCollector(Tool):
    """
    Open-Source Intelligence Collection Tool

    Capabilities:
    - Multi-source collection (web, news)
    - Entity extraction (CVEs, IPs, domains, emails, hashes)
    - Rate limiting and ethical collection
    - Memory storage with categorization
    - Formatted intelligence reporting
    """

    # Entity extraction patterns
    PATTERNS = {
        "cve": re.compile(r'CVE-\d{4}-\d{4,7}', re.IGNORECASE),
        "ip_v4": re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'),
        "domain": re.compile(
            r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b',
            re.IGNORECASE
        ),
        "email": re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        ),
        "url": re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        ),
        "hash_md5": re.compile(r'\b[a-fA-F0-9]{32}\b'),
        "hash_sha1": re.compile(r'\b[a-fA-F0-9]{40}\b'),
        "hash_sha256": re.compile(r'\b[a-fA-F0-9]{64}\b'),
    }

    # Rate limiting config
    RATE_LIMIT = {
        "requests_per_second": 2,
        "burst_size": 5
    }

    def __init__(self, agent: Agent, name: str, args: dict, message: Any):
        super().__init__(agent, name, args, message)
        self._request_times = []
        self._stats = defaultdict(int)

    async def execute(
        self,
        query: str,
        sources: List[str] = ["web", "news"],
        timeframe: str = "7d",
        max_results: int = 20,
        extract_entities: bool = True,
        store_in_memory: bool = True,
        **kwargs
    ) -> Response:
        """
        Collect OSINT from multiple sources

        Args:
            query: Search query or topic
            sources: Collection sources ["web", "news"]
            timeframe: Time window "1d", "7d", "30d"
            max_results: Maximum results per source
            extract_entities: Extract CVEs, IPs, domains, etc.
            store_in_memory: Store intelligence in agent memory

        Returns:
            Response with formatted intelligence report
        """
        self.agent.set_data("osint_query", query)
        start_time = time.time()

        results = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "sources": {},
            "entities": {},
            "summary": "",
            "stats": {}
        }

        try:
            # Collect from each source with rate limiting
            if "web" in sources:
                await self._rate_limit()
                results["sources"]["web"] = await self._collect_web(query, max_results)
                self._stats["web_requests"] += 1

            if "news" in sources:
                await self._rate_limit()
                results["sources"]["news"] = await self._collect_news(
                    query, timeframe, max_results
                )
                self._stats["news_requests"] += 1

            # Entity extraction
            if extract_entities:
                all_content = self._aggregate_content(results["sources"])
                results["entities"] = self._extract_entities(all_content)
                self._stats["entities_extracted"] += sum(
                    len(v) for v in results["entities"].values()
                )

            # Store in memory
            if store_in_memory:
                await self._store_intelligence(results)
                self._stats["stored_in_memory"] += 1

            # Add stats


---

**Part 2 of 3** | Next: [03_Advanced_Examples.md](03_Advanced_Examples.md) | Previous: [01_Basic_Examples.md](01_Basic_Examples.md)
