---
title: "Agent Zero - 02 MCP Integration"
category: "03_Agent_Zero_Core/01_Roadmap/02_Enhancement_Roadmap"
part: "2 of 4"
line_count: 362
last_updated: 2025-10-25
status: published
tags: ['agent-zero', 'roadmap', 'core']
related:
  - "01_Core_Enhancements.md"
  - "03_Security_Features.md"
---

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
        Hierarchical two-round search (8x better than flat search)

        Falls back to regular search if hierarchical RAG not enabled
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
            return await self.search_similarity_threshold(
                query,
                limit=top_k_categories * docs_per_category,
                threshold=threshold
            )
```

#### Agent Prompt Integration

**File:** `prompts/default/agent.system.md`

```markdown
# Memory System (Enhanced)

You have access to an enhanced memory system with hierarchical retrieval:

## Search Strategies

1. **Hierarchical Search** (Recommended for complex queries):
   - Searches across topic categories first
   - Then drills down into relevant categories
   - 8x better precision than flat search
   - Use when: Looking for specific information across broad knowledge base

2. **Flat Search** (Existing behavior):
   - Direct similarity search across all documents
   - Faster for simple queries
   - Use when: General information retrieval

## Memory Tool Usage

When using memory tools, consider query complexity:
- Complex/specific queries → Use hierarchical search
- Simple/broad queries → Use standard search
```

### Implementation Metrics

**Performance Targets:**
- 8x improvement in retrieval precision (PentestAgent benchmark)
- <100ms overhead for category search
- Backward compatible - existing workflows unchanged
- No new dependencies required

**Success Criteria:**
- Hierarchical search operational with existing FAISS
- Category auto-indexing for new documents
- Seamless fallback to flat search
- User-configurable via prompts

---

## Part 4: Priority 2 - OSINT Enhancement

### Current Capabilities

**File:** `python/tools/search_engine.py`
**Search Provider:** DuckDuckGo Search
**Browser:** browser-use integration

**Current Limitations:**
- Single search source (DuckDuckGo only)
- No multi-source aggregation
- No entity extraction
- No intelligence clustering
- Limited metadata extraction

### Enhancement Design: OSINT Collection Module

**Inspired by:** Taranis AI's multi-source collection + Story clustering

**Design Philosophy:**
- Build on existing search_engine.py and browser_agent.py
- Use existing browser-use for complex scraping
- Leverage existing sentence-transformers for entity extraction
- No heavy NLP dependencies (avoid XLM-RoBERTa)

#### Implementation Specification

**File Structure:**
```
python/tools/
├── search_engine.py (enhanced)
├── osint_collector.py (NEW)
└── osint_analyzer.py (NEW)

python/helpers/
└── entity_extractor.py (NEW - uses existing sentence-transformers)
```

**New Tool: `osint_collector.py`**

```python
# python/tools/osint_collector.py
"""
OSINT Collection Tool for Agent Zero

Multi-source intelligence gathering using existing Agent Zero infrastructure:
- DuckDuckGo search (existing)
- Browser agent for scraping (existing browser-use)
- RSS feed collection (new, minimal dependency)
- Entity extraction (existing sentence-transformers)

No heavy NLP models required.
"""

from python.helpers.tool import Tool, Response
from python.helpers import duckduckgo_search, browser
from agent import Agent
import json, re
from typing import List, Dict, Any
from datetime import datetime, timedelta

class OSINTCollector(Tool):

    async def execute(
        self,
        query: str,
        sources: List[str] = ["web", "news"],
        timeframe: str = "7d",
        max_results: int = 20,
        extract_entities: bool = True,
        **kwargs
    ):
        """
        Collect OSINT from multiple sources

        Args:
            query: Search query or topic
            sources: ["web", "news", "social"] - collection sources
            timeframe: "1d", "7d", "30d" - time window
            max_results: Maximum results per source
            extract_entities: Extract CVEs, IPs, domains, etc.

        Returns:
            Collected intelligence with metadata
        """

        self.agent.set_data("osint_query", query)

        results = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "sources": {},
            "entities": {},
            "summary": ""
        }

        # Collect from each source
        if "web" in sources:
            results["sources"]["web"] = await self._collect_web(
                query, max_results
            )

        if "news" in sources:
            results["sources"]["news"] = await self._collect_news(
                query, timeframe, max_results
            )

        # Entity extraction
        if extract_entities:
            all_content = self._aggregate_content(results["sources"])
            results["entities"] = await self._extract_entities(all_content)

        # Store in memory for future reference
        await self._store_intelligence(results)

        # Format response
        formatted = self._format_results(results)

        return Response(
            message=formatted,
            break_loop=False
        )

    async def _collect_web(
        self,
        query: str,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Collect web search results using existing DuckDuckGo"""
        # Use existing Agent Zero search
        search_results = await duckduckgo_search.search(
            query,
            max_results=max_results,
            region="wt-wt"  # worldwide
        )

        enriched_results = []
        for result in search_results:
            enriched_results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("body", ""),
                "source": "web",
                "timestamp": datetime.now().isoformat()
            })

        return enriched_results

    async def _collect_news(
        self,
        query: str,
        timeframe: str,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Collect news using DuckDuckGo news search"""
        # Use existing DuckDuckGo but with news focus
        search_results = await duckduckgo_search.search(
            query,
            max_results=max_results,
            region="wt-wt",
            safesearch="off",
            timelimit=self._timeframe_to_ddg(timeframe)
        )

        news_results = []
        for result in search_results:
            news_results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("body", ""),
                "source": "news",
                "timestamp": datetime.now().isoformat()
            })

        return news_results

    def _timeframe_to_ddg(self, timeframe: str) -> str:
        """Convert timeframe to DuckDuckGo timelimit"""
        mapping = {
            "1d": "d",
            "7d": "w",
            "30d": "m"
        }
        return mapping.get(timeframe, "w")

    async def _extract_entities(
        self,
        content: str
    ) -> Dict[str, List[str]]:
        """
        Extract entities using regex patterns (lightweight)

        Uses regex for:
        - CVEs
        - IP addresses
        - Domains
        - Email addresses
        - URLs

        No heavy NLP required.
        """
        entities = {
            "cves": [],
            "ip_addresses": [],
            "domains": [],
            "emails": [],
            "urls": []
        }

        # CVE pattern: CVE-YYYY-NNNNN
        cves = re.findall(r'CVE-\d{4}-\d{4,7}', content, re.IGNORECASE)
        entities["cves"] = list(set(cves))

        # IP addresses (v4)
        ips = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', content)
        # Filter valid IPs
        entities["ip_addresses"] = [
            ip for ip in set(ips)
            if all(0 <= int(octet) <= 255 for octet in ip.split('.'))
        ]

        # Domains
        domains = re.findall(
            r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b',
            content,
            re.IGNORECASE
        )
        entities["domains"] = list(set(domains))[:50]  # Limit to 50

        # Emails
        emails = re.findall(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            content
        )
        entities["emails"] = list(set(emails))

        # URLs
        urls = re.findall(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            content
        )
        entities["urls"] = list(set(urls))[:50]

        return entities

    def _aggregate_content(self, sources: Dict[str, List[Dict]]) -> str:
        """Aggregate all content for entity extraction"""
        content = ""
        for source_name, results in sources.items():
            for result in results:
                content += f"{result.get('title', '')} {result.get('snippet', '')} "
        return content

    async def _store_intelligence(self, results: Dict[str, Any]):
        """Store intelligence in Agent Zero memory"""
        from python.helpers.memory import Memory
        from langchain_core.documents import Document

        # Get memory instance
        memory = await Memory.get(self.agent)

        # Create document for storage
        doc_content = f"""OSINT Collection Results
Query: {results['query']}
Timestamp: {results['timestamp']}

Sources Collected: {', '.join(results['sources'].keys())}
Total Results: {sum(len(v) for v in results['sources'].values())}

Entities Extracted:
- CVEs: {len(results['entities'].get('cves', []))}
- IP Addresses: {len(results['entities'].get('ip_addresses', []))}
- Domains: {len(results['entities'].get('domains', []))}

Key Findings:
{json.dumps(results['entities'], indent=2)}
"""

        doc = Document(
            page_content=doc_content,
            metadata={
                "type": "osint",
                "query": results["query"],
                "timestamp": results["timestamp"],
                "area": "main"
            }
        )

        await memory.insert_documents([doc])

    def _format_results(self, results: Dict[str, Any]) -> str:
        """Format results for display"""
        output = f"# OSINT Collection Results\n\n"
        output += f"**Query:** {results['query']}\n"
        output += f"**Timestamp:** {results['timestamp']}\n\n"

        # Sources summary
        output += "## Sources Collected\n\n"
        for source_name, source_results in results['sources'].items():
            output += f"### {source_name.title()} ({len(source_results)} results)\n\n"
            for i, result in enumerate(source_results[:5], 1):  # Show top 5
                output += f"{i}. **{result['title']}**\n"
                output += f"   - {result['snippet'][:150]}...\n"
                output += f"   - URL: {result['url']}\n\n"

        # Entities
        output += "## Entities Extracted\n\n"
        entities = results['entities']

        if entities.get('cves'):
            output += f"**CVEs Found:** {', '.join(entities['cves'][:10])}\n\n"

        if entities.get('ip_addresses'):
            output += f"**IP Addresses:** {', '.join(entities['ip_addresses'][:10])}\n\n"

        if entities.get('domains'):
            output += f"**Domains:** {', '.join(entities['domains'][:15])}\n\n"

        output += "\n*Intelligence stored in memory for future reference.*\n"

        return output
```

**Tool Specification File:**

```python
# python/tools/osint_collector.json
{
    "name": "osint_collector",
    "title": "OSINT Intelligence Collector",
    "description": "Collect open-source intelligence from multiple sources (web, news). Extracts entities like CVEs, IP addresses, domains. Stores findings in memory.",
    "version": "2.0",
    "enabled": true,
    "schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query or intelligence topic (e.g., 'CVE-2024-1234', 'ransomware attacks 2024')"
            },
            "sources": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": ["web", "news"]
                },
                "description": "Intelligence sources to collect from",
                "default": ["web", "news"]
            },
            "timeframe": {
                "type": "string",
                "enum": ["1d", "7d", "30d"],
                "description": "Time window for collection",
                "default": "7d"
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum results per source",
                "default": 20,
                "minimum": 1,
                "maximum": 100
            },


---

**Part 2 of 4** | Next: [03_Security_Features.md](03_Security_Features.md) | Previous: [01_Core_Enhancements.md](01_Core_Enhancements.md)
