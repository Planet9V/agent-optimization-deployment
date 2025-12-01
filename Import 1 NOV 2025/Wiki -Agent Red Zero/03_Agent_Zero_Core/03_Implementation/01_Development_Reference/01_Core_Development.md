---
title: "Agent Zero - 01 Core Development"
category: "03_Agent_Zero_Core/03_Implementation/01_Development_Reference"
part: "1 of 2"
line_count: 367
last_updated: 2025-10-25
status: published
tags: ['agent-zero', 'roadmap', 'core']
related:
  - "02_Advanced_Development.md"
---

# Agent Zero 2.0 Development Reference Guide
## Quick Start Guide for Implementation Team

**Document Version:** 1.0
**Created:** 2025-10-16
**Purpose:** Fast reference for developers implementing Agent Zero 2.0

---

## Quick Navigation

| Section | Purpose | Time to Read |
|---------|---------|--------------|
| [Setup](#1-development-setup) | Environment setup | 5 min |
| [Phase 1](#2-phase-1-implementation) | RAG + OSINT | 15 min |
| [Phase 2](#3-phase-2-implementation) | SuperClaude + Orchestration | 15 min |
| [Testing](#4-testing-guide) | How to test | 10 min |
| [Troubleshooting](#5-troubleshooting) | Common issues | 5 min |

---

## 1. Development Setup

### 1.1 Prerequisites

```bash
# System Requirements
- Python 3.11+
- Docker Desktop (running)
- 8GB+ RAM
- 10GB disk space

# Agent Zero v0.9.6 installed
cd /path/to/agent-zero
git status  # Should show clean working directory
```

### 1.2 Environment Setup

```bash
# 1. Create development branch
git checkout -b feature/agentzero-2.0

# 2. Install dependencies (should already be installed)
pip install -r requirements.txt

# 3. Verify existing libraries
python -c "import faiss; import sentence_transformers; print('OK')"

# 4. Run existing Agent Zero
./run.sh  # or docker-compose up

# 5. Verify http://localhost:50001 is accessible
```

### 1.3 Project Structure

```
agent-zero/
├── python/
│   ├── helpers/
│   │   ├── memory.py          (ENHANCE - add RAG)
│   │   ├── memory_rag.py      (NEW - hierarchical RAG)
│   │   └── superclaude_bridge.py  (NEW - integration)
│   ├── tools/
│   │   ├── osint_collector.py (NEW - OSINT tool)
│   │   └── tool_orchestrator.py  (NEW - orchestration)
│   └── api/
│       └── superclaude_webhook.py  (NEW - API endpoint)
├── prompts/
│   └── default/
│       ├── agent.system.md    (ENHANCE - add RAG guidance)
│       └── superclaude_integration.md  (NEW - integration docs)
└── memory/
    └── default/
        ├── index.faiss        (EXISTING)
        ├── categories.json    (NEW - category index)
        └── metadata_index.json  (NEW - fast lookups)
```

---

## 2. Phase 1 Implementation (Weeks 1-4)

### 2.1 Week 1-2: Hierarchical RAG

#### Step 1: Create `memory_rag.py`

```bash
# Create new file
touch python/helpers/memory_rag.py
```

**Copy this template:**

```python
# python/helpers/memory_rag.py
"""
Hierarchical RAG for Agent Zero 2.0

Build on existing FAISS memory system
No new dependencies required
"""

from typing import List, Dict, Tuple
from langchain_core.documents import Document
from python.helpers.memory import Memory
import json, os, time
from python.helpers import files
import numpy as np

class HierarchicalRAG:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.categories = self._load_categories()
        self._category_embeddings_cache = {}
        self._cache_ttl = 3600

    def _load_categories(self) -> Dict[str, List[str]]:
        """Load category index from disk"""
        category_file = files.get_abs_path(
            Memory._abs_db_dir(self.memory.memory_subdir),
            "categories.json"
        )
        if files.exists(category_file):
            return json.loads(files.read_file(category_file))
        return {}

    async def hierarchical_search(
        self,
        query: str,
        top_k_categories: int = 3,
        docs_per_category: int = 5,
        threshold: float = 0.6
    ) -> List[Tuple[Document, float]]:
        """Two-round hierarchical search"""

        # ROUND 1: Category search
        relevant_categories = await self._search_categories(query, top_k_categories)

        if not relevant_categories:
            # Fallback to flat search
            return await self.memory.search_similarity_threshold(
                query,
                limit=top_k_categories * docs_per_category,
                threshold=threshold
            )

        # ROUND 2: Document search within categories
        all_results = []
        for category, category_score in relevant_categories:
            docs = await self.memory.search_similarity_threshold(
                query,
                limit=docs_per_category,
                threshold=threshold,
                filter=f'category == "{category}"'
            )

            for doc in docs:
                boosted_score = doc.metadata.get('score', 0.5) * category_score
                all_results.append((doc, boosted_score))

        all_results.sort(key=lambda x: x[1], reverse=True)
        return all_results[:top_k_categories * docs_per_category]

    # TODO: Implement _search_categories, _compute_category_embedding, etc.
```

#### Step 2: Enhance `memory.py`

```python
# Add to python/helpers/memory.py at end of Memory class

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
        """Hierarchical two-round search"""
        if hasattr(self, '_rag'):
            return await self._rag.hierarchical_search(
                query, top_k_categories, docs_per_category, threshold
            )
        else:
            # Fallback
            return await self.search_similarity_threshold(
                query,
                limit=top_k_categories * docs_per_category,
                threshold=threshold
            )
```

#### Step 3: Test Hierarchical RAG

```python
# tests/test_hierarchical_rag.py
import pytest
from python.helpers.memory import Memory
from python.helpers.memory_rag import HierarchicalRAG

@pytest.mark.asyncio
async def test_hierarchical_search():
    """Test hierarchical RAG vs flat search"""

    # Get memory instance
    memory = await Memory.get_by_subdir("test")

    # Enable RAG
    rag = memory.enable_hierarchical_rag()

    # Test query
    results = await memory.search_hierarchical(
        query="CVE vulnerability analysis",
        top_k_categories=3,
        docs_per_category=5
    )

    assert len(results) <= 15
    assert all(isinstance(r[0], Document) for r in results)
    print(f"Found {len(results)} results")
```

**Run test:**

```bash
pytest tests/test_hierarchical_rag.py -v
```

### 2.2 Week 3-4: OSINT Collector

#### Step 1: Create `osint_collector.py`

```bash
# Create new tool file
touch python/tools/osint_collector.py
```

**Copy this template:**

```python
# python/tools/osint_collector.py
"""
OSINT Collection Tool for Agent Zero 2.0

Uses existing DuckDuckGo search and browser-use
No new heavy dependencies
"""

from python.helpers.tool import Tool, Response
from python.helpers import duckduckgo_search
from agent import Agent
import json, re
from typing import List, Dict, Any
from datetime import datetime

class OSINTCollector(Tool):
    async def execute(
        self,
        query: str,
        sources: List[str] = ["web", "news"],
        timeframe: str = "7d",
        max_results: int = 20,
        extract_entities: bool = True,
        **kwargs
    ) -> Response:
        """Collect OSINT from multiple sources"""

        results = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "sources": {},
            "entities": {}
        }

        # Collect from sources
        if "web" in sources:
            results["sources"]["web"] = await self._collect_web(query, max_results)

        if "news" in sources:
            results["sources"]["news"] = await self._collect_news(
                query, timeframe, max_results
            )

        # Extract entities
        if extract_entities:
            all_content = self._aggregate_content(results["sources"])
            results["entities"] = await self._extract_entities(all_content)

        # Store in memory
        await self._store_intelligence(results)

        # Format response
        formatted = self._format_results(results)

        return Response(message=formatted, break_loop=False)

    async def _collect_web(self, query: str, max_results: int) -> List[Dict]:
        """Use existing DuckDuckGo"""
        search_results = await duckduckgo_search.search(
            query, max_results=max_results, region="wt-wt"
        )

        return [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("body", ""),
                "source": "web",
                "timestamp": datetime.now().isoformat()
            }
            for r in search_results
        ]

    async def _extract_entities(self, content: str) -> Dict[str, List[str]]:
        """Extract entities using regex"""
        entities = {
            "cves": list(set(re.findall(r'CVE-\d{4}-\d{4,7}', content, re.I))),
            "ip_addresses": [
                ip for ip in set(re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', content))
                if self._validate_ip(ip)
            ],
            "domains": list(set(re.findall(
                r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b',
                content, re.I
            )))[:50]
        }
        return entities

    # TODO: Implement _collect_news, _store_intelligence, _format_results, etc.
```

#### Step 2: Register OSINT Tool

```bash
# Create tool specification
touch python/tools/osint_collector.json
```

```json
{
    "name": "osint_collector",
    "title": "OSINT Intelligence Collector",
    "description": "Collect open-source intelligence from web and news sources. Extracts CVEs, IPs, domains.",
    "version": "2.0",
    "enabled": true,
    "schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query (e.g., 'CVE-2024-1234')"
            },
            "sources": {
                "type": "array",
                "items": {"type": "string", "enum": ["web", "news"]},
                "default": ["web", "news"]
            },
            "max_results": {
                "type": "integer",
                "default": 20,
                "minimum": 1,
                "maximum": 100
            }
        },
        "required": ["query"]
    }
}
```

#### Step 3: Test OSINT Collector

```python
# tests/test_osint_collector.py
import pytest
from python.tools.osint_collector import OSINTCollector

@pytest.mark.asyncio
async def test_osint_collection():
    """Test OSINT collection"""

    # Mock agent
    from agent import Agent
    import initialize
    agent_config = initialize.initialize_agent()
    agent = Agent(0, agent_config)

    # Create tool
    tool = OSINTCollector(agent, "osint_collector", {}, None)

    # Execute
    result = await tool.execute(
        query="CVE-2024-1234",
        sources=["web"],
        max_results=5
    )

    assert "CVE-2024-1234" in result.message
    assert "web" in result.message
    print(result.message)
```

**Run test:**

```bash
pytest tests/test_osint_collector.py -v
```

---

## 3. Phase 2 Implementation (Weeks 5-8)

### 3.1 Week 5-6: SuperClaude Bridge

#### Step 1: Create `superclaude_bridge.py`

```bash
touch python/helpers/superclaude_bridge.py
```

**Template:**

```python
# python/helpers/superclaude_bridge.py
"""
SuperClaude <-> Agent Zero Integration Bridge

Uses existing A2A protocol (fasta2a)
"""

from typing import Dict, Any
import json
from python.helpers.fasta2a_client import Fasta2aClient
from python.helpers import files
from agent import Agent

class SuperClaudeBridge:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.a2a_client = None

    async def send_to_superclaude(
        self,
        task_type: str,
        task_data: Dict[str, Any],
        endpoint: str = "http://localhost:3000"
    ) -> Dict[str, Any]:
        """Send task to SuperClaude via A2A"""

        request = {


---

**Part 1 of 2** | Next: [02_Advanced_Development.md](02_Advanced_Development.md)
