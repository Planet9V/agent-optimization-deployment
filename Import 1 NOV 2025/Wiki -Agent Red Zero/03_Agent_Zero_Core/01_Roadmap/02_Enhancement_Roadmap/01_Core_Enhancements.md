---
title: "Agent Zero - 01 Core Enhancements"
category: "03_Agent_Zero_Core/01_Roadmap/02_Enhancement_Roadmap"
part: "1 of 4"
line_count: 353
last_updated: 2025-10-25
status: published
tags: ['agent-zero', 'roadmap', 'core']
related:
  - "02_MCP_Integration.md"
---

# Agent Zero 2.0 Enhancement Roadmap
## Native Architecture-Focused Enhancements

**Document Version:** 2.0
**Created:** 2025-10-16
**Status:** Design Phase
**Target Release:** Q2 2025

---

## Executive Summary

This roadmap defines Agent Zero's evolution from v0.9.6 to v2.0, incorporating best practices from 6 leading security and OSINT frameworks while preserving Agent Zero's core philosophy of simplicity, transparency, and customizability.

**Strategic Focus:**
1. **Vector Storage Enhancement (RAG)** - Priority 1
2. **OSINT Capabilities** - Priority 2
3. **SuperClaude Deep Integration** - Priority 3

**Key Principle:** Leverage existing Agent Zero libraries and architecture patterns. Avoid introducing new dependencies unless absolutely necessary.

---

## Part 1: Framework Comparison Analysis

### Comparative Strengths and Weaknesses Matrix

| Framework | Key Strengths | Key Weaknesses | Adoption Priority |
|-----------|---------------|----------------|-------------------|
| **PentAGI** | • 3-tier memory architecture<br>• Enterprise observability stack<br>• 4-agent microservices design<br>• PostgreSQL + pgvector persistence | • Resource intensive (16GB RAM)<br>• Complex deployment<br>• Heavy external dependencies<br>• Over-engineered for general use | **LOW** - Too complex |
| **PentestAgent** | • Hierarchical RAG implementation<br>• 8x better reconnaissance<br>• MCP-native architecture<br>• Two-round retrieval system | • Academic implementation<br>• Limited production use<br>• Narrow security focus<br>• Requires significant adaptation | **HIGH** - RAG patterns |
| **MAPTA** | • 76.9% task success rate<br>• Mandatory PoC validation<br>• Single container strategy<br>• Low cost ($0.073/task) | • Limited tool ecosystem<br>• Narrow pentesting focus<br>• No OSINT capabilities<br>• Academic prototype status | **MEDIUM** - Validation patterns |
| **HexStrike AI** | • 150+ tool orchestration<br>• Sub-second response times<br>• FastMCP architecture<br>• Multi-LLM support | • Weaponization concerns<br>• Security implications<br>• Black-box orchestration<br>• Limited documentation | **MEDIUM** - Tool patterns only |
| **Kali GPT** | • 600+ Kali tool integration<br>• 70% time reduction<br>• Native Linux integration<br>• CVE-to-exploit mapping | • Requires Kali Linux<br>• Security/ethical concerns<br>• Limited generalization<br>• GPT-4 dependency | **LOW** - Too specialized |
| **Taranis AI** | • Multi-source OSINT collection<br>• 100-language NLP support<br>• Story clustering algorithm<br>• EU defense backing | • Resource intensive<br>• Complex microservices<br>• Heavy NLP dependencies<br>• Limited security tools | **HIGH** - OSINT patterns |

### Technology Rationalization Analysis

#### Agent Zero Current Stack (KEEP)
```python
# Core Libraries - Already in Agent Zero
✅ faiss-cpu==1.11.0              # Vector storage - USE THIS
✅ sentence-transformers==3.0.1   # Embeddings - USE THIS
✅ langchain-core==0.3.49         # LLM framework - USE THIS
✅ langchain-community==0.3.19    # Vector stores - USE THIS
✅ duckduckgo-search==6.1.12      # Search - ENHANCE THIS
✅ browser-use==0.5.11            # Web automation - USE THIS
✅ fastmcp==2.3.4                 # MCP protocol - USE THIS
✅ litellm==1.75.0                # LLM routing - USE THIS
✅ flask==3.0.3                   # Web framework - USE THIS
✅ docker==7.1.0                  # Containerization - USE THIS
```

#### Frameworks' Libraries (AVOID/ADAPT)
```python
# PentAGI - AVOID (Too Heavy)
❌ PostgreSQL + pgvector          # Agent Zero uses FAISS
❌ Grafana + Prometheus           # Too heavy, create lightweight alternative
❌ Jaeger + Loki                  # Not needed for Agent Zero scale

# PentestAgent - ADAPT (RAG Patterns Only)
✅ Hierarchical retrieval logic   # Implement on existing FAISS
❌ Custom RAG database            # Use Agent Zero's existing memory.py
✅ Two-round search algorithm     # Implement as enhancement

# MAPTA - ADAPT (Validation Only)
✅ PoC validation patterns        # Use Agent Zero's existing code execution
❌ Custom container isolation     # Agent Zero already has Docker

# HexStrike AI - ADAPT (Orchestration Only)
✅ Tool selection algorithms      # Implement as enhancement
❌ FastMCP custom implementation  # Agent Zero already has fastmcp==2.3.4

# Kali GPT - AVOID (Too Specialized)
❌ Kali Linux dependency          # Not portable
❌ 600+ security tools            # Too heavy, select subset

# Taranis AI - ADAPT (OSINT Patterns Only)
✅ Multi-source collection logic  # Implement with existing tools
❌ XLM-RoBERTa NLP model          # Too heavy, use lighter alternatives
❌ Microservices architecture     # Agent Zero is monolithic
```

### Rationalized Technology Choices

| Need | Agent Zero Native | Alternative Considered | Decision |
|------|-------------------|----------------------|----------|
| **Vector Storage** | FAISS (already in use) | pgvector, Chroma | ✅ **FAISS** - Keep existing |
| **Embeddings** | sentence-transformers | OpenAI embeddings | ✅ **sentence-transformers** - Keep existing |
| **Web Search** | DuckDuckGo | SearXNG, Tavily | ✅ **Enhance DuckDuckGo**, add optional Tavily |
| **Web Scraping** | browser-use | Playwright, Selenium | ✅ **browser-use** - Keep existing |
| **MCP Protocol** | fastmcp==2.3.4 | Custom implementation | ✅ **fastmcp** - Keep existing |
| **LLM Routing** | litellm | Direct API calls | ✅ **litellm** - Keep existing |
| **NLP** | sentence-transformers | spaCy, XLM-RoBERTa | ✅ **sentence-transformers** - Keep existing |
| **Observability** | None | Grafana/Prometheus | ✅ **Build lightweight** with Flask |
| **Database** | FAISS + JSON files | PostgreSQL | ✅ **FAISS + JSON** - Keep existing |

---

## Part 2: Agent Zero 2.0 Architecture

### Core Principles

1. **Native First:** Build on existing Agent Zero architecture
2. **No Breaking Changes:** Backward compatible with v0.9.6
3. **Optional Modules:** All enhancements can be disabled
4. **Minimal Dependencies:** Avoid adding new libraries unless critical
5. **Prompt-Driven:** Configurable through prompts/, not hardcoded

### Architecture Enhancements Overview

```
Agent Zero v0.9.6                    Agent Zero v2.0
┌─────────────────────┐              ┌─────────────────────────────┐
│ Agent Core          │              │ Agent Core (unchanged)      │
│ ├─ LLM Calls        │              │ ├─ LLM Calls                │
│ ├─ Tool Execution   │              │ ├─ Tool Execution           │
│ └─ Memory (FAISS)   │──────────┐   │ └─ Memory (Enhanced FAISS)  │
└─────────────────────┘          │   │     ├─ Hierarchical RAG     │
                                 │   │     ├─ Two-round retrieval  │
┌─────────────────────┐          │   │     └─ Category indexing    │
│ Tools               │          │   ├─────────────────────────────┤
│ ├─ code_execution   │          │   │ Enhanced Tools              │
│ ├─ search_engine    │          │   │ ├─ code_execution (same)    │
│ ├─ browser_agent    │          │   │ ├─ search_engine (enhanced) │
│ └─ memory_*         │          │   │ ├─ browser_agent (same)     │
└─────────────────────┘          │   │ ├─ osint_collector (NEW)    │
                                 │   │ ├─ tool_orchestrator (NEW)  │
┌─────────────────────┐          │   │ └─ memory_* (enhanced)      │
│ MCP Servers         │          │   ├─────────────────────────────┤
│ └─ External tools   │          │   │ MCP Servers (Enhanced)      │
└─────────────────────┘          │   │ ├─ External tools (same)    │
                                 │   │ ├─ SuperClaude Bridge (NEW) │
                                 │   │ └─ OSINT MCP Server (NEW)   │
                                 │   ├─────────────────────────────┤
                                 └───│ Observability (NEW)         │
                                     │ ├─ Metrics collector         │
                                     │ └─ Performance dashboard     │
                                     └─────────────────────────────┘
```

---

## Part 3: Priority 1 - Enhanced Vector Storage (RAG)

### Current Implementation Analysis

**File:** `python/helpers/memory.py`
**Vector Store:** FAISS (langchain_community.vectorstores.FAISS)
**Embeddings:** CacheBackedEmbeddings with sentence-transformers
**Storage:** Local file system (`memory/{subdir}/index.faiss`)

**Current Capabilities:**
- ✅ Similarity search with cosine distance
- ✅ Document storage with metadata
- ✅ Memory areas (MAIN, FRAGMENTS, SOLUTIONS, INSTRUMENTS)
- ✅ Knowledge preloading from directories
- ✅ Embedding caching

**Current Limitations:**
- ❌ Flat search - no hierarchical retrieval
- ❌ No category organization
- ❌ No two-round search for precision
- ❌ Limited metadata filtering
- ❌ No relevance scoring beyond similarity

### Enhancement Design: Hierarchical RAG System

**Inspired by:** PentestAgent's hierarchical two-round search (8x better performance)

**Design Philosophy:**
- Build on existing `memory.py`
- Use existing FAISS infrastructure
- No new dependencies required
- Backward compatible

#### Implementation Specification

**File Structure:**
```
python/helpers/
├── memory.py (enhanced)
└── memory_rag.py (new)

memory/{subdir}/
├── index.faiss (existing)
├── index.pkl (existing)
├── embedding.json (existing)
├── knowledge_import.json (existing)
├── categories.json (NEW - category index)
└── metadata_index.json (NEW - fast metadata lookup)
```

**New Class: `HierarchicalRAG`**

```python
# python/helpers/memory_rag.py
from typing import List, Dict, Tuple
from langchain_core.documents import Document
from python.helpers.memory import Memory
import json, os
from python.helpers import files

class HierarchicalRAG:
    """
    Hierarchical Retrieval-Augmented Generation for Agent Zero

    Implements two-round search:
    1. Category-level search (broad)
    2. Document-level search within categories (narrow)

    Compatible with existing FAISS memory system.
    """

    def __init__(self, memory: Memory):
        self.memory = memory
        self.categories = self._load_categories()

    def _load_categories(self) -> Dict[str, List[str]]:
        """Load category index from disk"""
        category_file = files.get_abs_path(
            Memory._abs_db_dir(self.memory.memory_subdir),
            "categories.json"
        )
        if files.exists(category_file):
            return json.loads(files.read_file(category_file))
        return {}

    def _save_categories(self):
        """Persist category index"""
        category_file = files.get_abs_path(
            Memory._abs_db_dir(self.memory.memory_subdir),
            "categories.json"
        )
        files.write_file(category_file, json.dumps(self.categories))

    async def hierarchical_search(
        self,
        query: str,
        top_k_categories: int = 3,
        docs_per_category: int = 5,
        threshold: float = 0.6
    ) -> List[Tuple[Document, float]]:
        """
        Two-round hierarchical search

        Args:
            query: Search query
            top_k_categories: Number of relevant categories to search
            docs_per_category: Documents to retrieve per category
            threshold: Minimum similarity threshold

        Returns:
            List of (Document, score) tuples ranked by relevance
        """

        # ROUND 1: Category-level search
        relevant_categories = await self._search_categories(
            query,
            top_k_categories
        )

        # ROUND 2: Document-level search within categories
        all_results = []
        for category, category_score in relevant_categories:
            # Search within specific category
            category_docs = await self.memory.search_similarity_threshold(
                query,
                limit=docs_per_category,
                threshold=threshold,
                filter=f'category == "{category}"'
            )

            # Boost scores by category relevance
            for doc in category_docs:
                boosted_score = doc.metadata.get('score', 0.5) * category_score
                all_results.append((doc, boosted_score))

        # Sort by boosted scores
        all_results.sort(key=lambda x: x[1], reverse=True)

        return all_results[:top_k_categories * docs_per_category]

    async def _search_categories(
        self,
        query: str,
        top_k: int
    ) -> List[Tuple[str, float]]:
        """
        Search for relevant categories using category embeddings

        Returns:
            List of (category_name, relevance_score) tuples
        """
        if not self.categories:
            return [("default", 1.0)]

        # Create category embeddings from representative documents
        category_scores = {}
        for category, doc_ids in self.categories.items():
            # Sample representative documents from category
            sample_docs = await self.memory.db.aget_by_ids(doc_ids[:5])
            if sample_docs:
                # Average similarity to category samples
                scores = []
                for doc in sample_docs:
                    results = await self.memory.search_similarity_threshold(
                        query,
                        limit=1,
                        threshold=0.0
                    )
                    if results:
                        scores.append(results[0].metadata.get('score', 0.5))

                category_scores[category] = sum(scores) / len(scores) if scores else 0.0

        # Rank categories
        ranked = sorted(
            category_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]

    async def auto_categorize_document(
        self,
        doc: Document,
        llm_model
    ) -> str:
        """
        Automatically assign category to document using LLM

        Uses existing Agent Zero LLM infrastructure
        """
        # Extract key terms from document
        content_preview = doc.page_content[:500]
        existing_categories = list(self.categories.keys())

        # Prompt for categorization
        if existing_categories:
            category_list = ", ".join(existing_categories)
            prompt = f"""Categorize this document into one of these existing categories: {category_list}

Document preview:
{content_preview}

Choose the most relevant category or suggest "new_category" if none fit well.
Category:"""
        else:
            prompt = f"""Suggest a short category name (2-3 words) for this document:

{content_preview}

Category:"""

        # Call LLM (using existing Agent Zero pattern)
        from python.helpers.call_llm import call_llm_streaming

        response = ""
        async for chunk in call_llm_streaming(llm_model, [{"role": "user", "content": prompt}]):
            response += chunk

        category = response.strip().lower()

        # Add to new category or map to existing
        if category not in self.categories:
            if existing_categories and category == "new_category":
                # Extract topic from document
                category = self._extract_topic(doc)

        return category

    def _extract_topic(self, doc: Document, max_words: int = 3) -> str:
        """Extract topic from document content using simple heuristics"""
        # Get area if available
        if "area" in doc.metadata:
            return doc.metadata["area"]

        # Extract first significant words
        import re
        words = re.findall(r'\b\w+\b', doc.page_content.lower())
        # Filter common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        significant = [w for w in words if w not in stopwords and len(w) > 3]

        return "_".join(significant[:max_words]) if significant else "general"

    async def add_document_with_category(
        self,
        doc: Document,
        category: str = None,
        llm_model = None
    ) -> str:
        """
        Add document to memory with automatic categorization

        Args:
            doc: Document to add
            category: Explicit category (optional)
            llm_model: LLM for auto-categorization (optional)

        Returns:
            Document ID
        """
        # Auto-categorize if not provided
        if not category and llm_model:
            category = await self.auto_categorize_document(doc, llm_model)
        elif not category:
            category = self._extract_topic(doc)

        # Add category to document metadata
        doc.metadata["category"] = category

        # Insert document using existing memory system
        doc_ids = await self.memory.insert_documents([doc])
        doc_id = doc_ids[0]

        # Update category index
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(doc_id)
        self._save_categories()

        return doc_id
```

#### Integration with Existing Memory

**Enhanced `memory.py` additions:**

```python
# Add to python/helpers/memory.py

class Memory:
    # ... existing code ...

    def enable_hierarchical_rag(self):
        """Enable hierarchical RAG enhancement"""
        from python.helpers.memory_rag import HierarchicalRAG


---

**Part 1 of 4** | Next: [02_MCP_Integration.md](02_MCP_Integration.md)
