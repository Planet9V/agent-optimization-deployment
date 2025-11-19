---
title: "Agent Zero - 02 Advanced Development"
category: "03_Agent_Zero_Core/03_Implementation/01_Development_Reference"
part: "2 of 2"
line_count: 342
last_updated: 2025-10-25
status: published
tags: ['agent-zero', 'roadmap', 'core']
related:
  - "01_Core_Development.md"
---

            "type": task_type,
            "data": task_data,
            "context": await self._get_shared_context(),
            "agent_id": self.agent.agent_name
        }

        if not self.a2a_client:
            self.a2a_client = Fasta2aClient(endpoint)

        response = await self.a2a_client.send_message(
            message=json.dumps(request),
            await_response=True
        )

        return json.loads(response) if isinstance(response, str) else response

    async def _get_shared_context(self) -> Dict[str, Any]:
        """Get current agent context"""
        return {
            "agent_name": self.agent.agent_name,
            "current_task": self.agent.get_data("current_task", "")
        }

    # TODO: Implement receive_from_superclaude, task handlers, etc.
```

#### Step 2: Create Webhook API

```bash
touch python/api/superclaude_webhook.py
```

```python
# python/api/superclaude_webhook.py
from flask import request, jsonify
from python.helpers import api
from python.helpers.superclaude_bridge import SuperClaudeBridge

def setup_routes(app):
    @app.route('/api/superclaude/task', methods=['POST'])
    @api.require_auth
    async def superclaude_task():
        """Receive task from SuperClaude"""
        try:
            task_data = request.json

            from initialize import initialize_agent
            agent_config = initialize_agent()
            from agent import Agent
            agent = Agent(0, agent_config)

            bridge = SuperClaudeBridge(agent)
            result = await bridge.receive_from_superclaude(task_data)

            return jsonify({"success": True, "result": result})

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
```

#### Step 3: Register webhook in Flask app

```python
# In main Flask app initialization (app.py or similar)

from python.api import superclaude_webhook

# Register routes
superclaude_webhook.setup_routes(app)
```

### 3.2 Week 7-8: Tool Orchestration

#### Step 1: Create Tool Registry

```bash
touch python/helpers/tool_registry.json
```

```json
{
    "tools": {
        "osint_collector": {
            "capabilities": ["reconnaissance", "intelligence_gathering"],
            "success_rate": 0.95,
            "avg_execution_time": 4.5
        },
        "code_execution": {
            "capabilities": ["code_execution", "validation"],
            "success_rate": 0.98,
            "avg_execution_time": 2.1
        }
    }
}
```

#### Step 2: Create Orchestrator

```bash
touch python/helpers/tool_orchestrator.py
```

```python
# python/helpers/tool_orchestrator.py
"""
Intelligent Tool Orchestration for Agent Zero 2.0
"""

import json
from typing import List, Dict, Any
from python.helpers import files

class ToolOrchestrator:
    def __init__(self):
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        """Load tool registry"""
        registry_file = files.get_abs_path("python/helpers/tool_registry.json")
        if files.exists(registry_file):
            return json.loads(files.read_file(registry_file))
        return {"tools": {}}

    def select_tools(
        self,
        required_capabilities: List[str],
        max_tools: int = 3
    ) -> List[str]:
        """Select best tools for required capabilities"""

        scored_tools = []
        for tool_name, tool_meta in self.registry["tools"].items():
            score = self._score_tool(tool_meta, required_capabilities)
            scored_tools.append((tool_name, score))

        scored_tools.sort(key=lambda x: x[1], reverse=True)
        return [name for name, score in scored_tools[:max_tools]]

    def _score_tool(
        self,
        tool_meta: Dict[str, Any],
        required_capabilities: List[str]
    ) -> float:
        """Score tool for capabilities"""

        tool_caps = set(tool_meta["capabilities"])
        required_caps = set(required_capabilities)

        capability_match = len(tool_caps & required_caps) / len(required_caps)
        success_rate = tool_meta.get("success_rate", 0.5)

        return capability_match * 0.6 + success_rate * 0.4
```

---

## 4. Testing Guide

### 4.1 Unit Testing

**Framework:** pytest

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_hierarchical_rag.py -v

# Run with coverage
pytest tests/ --cov=python --cov-report=html
```

### 4.2 Integration Testing

```python
# tests/integration/test_phase1_integration.py
import pytest
from python.helpers.memory import Memory
from python.tools.osint_collector import OSINTCollector

@pytest.mark.asyncio
async def test_osint_to_rag_integration():
    """Test OSINT collection stores in hierarchical RAG"""

    # Collect OSINT
    tool = OSINTCollector(agent, "osint_collector", {}, None)
    result = await tool.execute(query="CVE-2024-1234", sources=["web"])

    # Check memory storage
    memory = await Memory.get_by_subdir("default")
    rag = memory.enable_hierarchical_rag()

    # Search stored intelligence
    results = await memory.search_hierarchical(
        query="CVE-2024-1234",
        top_k_categories=2
    )

    assert len(results) > 0
    assert any("CVE-2024-1234" in r[0].page_content for r in results)
```

### 4.3 Performance Testing

```python
# tests/performance/test_rag_performance.py
import pytest, time
from python.helpers.memory import Memory

@pytest.mark.asyncio
async def test_hierarchical_search_performance():
    """Benchmark hierarchical search"""

    memory = await Memory.get_by_subdir("default")
    rag = memory.enable_hierarchical_rag()

    queries = generate_test_queries(n=100)
    times = []

    for query in queries:
        start = time.time()
        results = await memory.search_hierarchical(query)
        elapsed = time.time() - start
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    assert avg_time < 0.150  # <150ms target

    print(f"Average search time: {avg_time*1000:.2f}ms")
```

---

## 5. Troubleshooting

### 5.1 Common Issues

#### Issue: Import errors for new modules

**Error:**
```
ModuleNotFoundError: No module named 'python.helpers.memory_rag'
```

**Solution:**
```bash
# Ensure file exists
ls python/helpers/memory_rag.py

# Check __init__.py exists
ls python/helpers/__init__.py

# Restart Agent Zero
docker-compose restart
```

#### Issue: FAISS category filtering not working

**Error:**
```
ValueError: Invalid filter expression: category == "security"
```

**Solution:**
```python
# Ensure metadata has 'category' field
doc.metadata["category"] = "security_vulnerabilities"

# Use correct filter syntax (simpleeval)
filter='category == "security_vulnerabilities"'
```

#### Issue: OSINT tool not found

**Error:**
```
Unknown tool: osint_collector
```

**Solution:**
```bash
# Ensure tool specification exists
ls python/tools/osint_collector.json

# Restart to reload tools
docker-compose restart

# Check tool is registered
curl http://localhost:50001/api/tools
```

### 5.2 Debugging Tips

#### Enable verbose logging

```python
# Add to python/helpers/log.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Test individual components

```python
# Test RAG in isolation
python -c "
from python.helpers.memory import Memory
import asyncio

async def test():
    memory = await Memory.get_by_subdir('default')
    rag = memory.enable_hierarchical_rag()
    results = await rag.hierarchical_search('test query')
    print(f'Found {len(results)} results')

asyncio.run(test())
"
```

#### Check memory contents

```bash
# Inspect FAISS index
python -c "
from python.helpers.memory import Memory
import asyncio

async def inspect():
    memory = await Memory.get_by_subdir('default')
    docs = memory.db.get_all_docs()
    print(f'Total documents: {len(docs)}')
    for doc_id, doc in list(docs.items())[:5]:
        print(f'{doc_id}: {doc.page_content[:100]}...')

asyncio.run(inspect())
"
```

---

## 6. Quick Reference

### 6.1 File Checklist

**Phase 1:**
- [ ] `python/helpers/memory_rag.py` (NEW)
- [ ] `python/helpers/memory.py` (ENHANCED)
- [ ] `python/tools/osint_collector.py` (NEW)
- [ ] `python/tools/osint_collector.json` (NEW)
- [ ] `tests/test_hierarchical_rag.py` (NEW)
- [ ] `tests/test_osint_collector.py` (NEW)

**Phase 2:**
- [ ] `python/helpers/superclaude_bridge.py` (NEW)
- [ ] `python/api/superclaude_webhook.py` (NEW)
- [ ] `python/helpers/tool_orchestrator.py` (NEW)
- [ ] `python/helpers/tool_registry.json` (NEW)

### 6.2 Command Reference

```bash
# Development
git checkout -b feature/agentzero-2.0
git add .
git commit -m "feat: implement hierarchical RAG"
git push origin feature/agentzero-2.0

# Testing
pytest tests/ -v
pytest tests/test_hierarchical_rag.py -k "test_search"
pytest tests/ --cov=python --cov-report=term

# Running
docker-compose up
docker-compose restart
docker-compose logs -f

# Debugging
docker exec -it agentzero python -c "import python.helpers.memory_rag"
docker logs agentzero --tail 100

# Performance
pytest tests/performance/ --benchmark-only
```

### 6.3 Key Functions

```python
# Hierarchical RAG
from python.helpers.memory import Memory
memory = await Memory.get_by_subdir("default")
rag = memory.enable_hierarchical_rag()
results = await memory.search_hierarchical("query", top_k_categories=3)

# OSINT Collection
from python.tools.osint_collector import OSINTCollector
tool = OSINTCollector(agent, "osint_collector", {}, None)
result = await tool.execute(query="CVE-2024-1234", sources=["web", "news"])

# SuperClaude Bridge
from python.helpers.superclaude_bridge import SuperClaudeBridge
bridge = SuperClaudeBridge(agent)
result = await bridge.send_to_superclaude("research", {"query": "test"})

# Tool Orchestration
from python.helpers.tool_orchestrator import ToolOrchestrator
orchestrator = ToolOrchestrator()
tools = orchestrator.select_tools(["reconnaissance", "scanning"])
```

---

## 7. Resources

### 7.1 Documentation Links

**Agent Zero 2.0 Roadmap:**
- `/home/jim/5_AgentZero/claudedocs/Agent0Roadmap2.0.md`

**Technical Specifications:**
- `/home/jim/5_AgentZero/claudedocs/Agent0_Technical_Specifications.md`

**Research Reports:**
- `/home/jim/5_AgentZero/claudedocs/agentzero_improvement_recommendations_20251016.md`
- `/home/jim/5_AgentZero/claudedocs/research_pentestagent_20251016.md` (RAG patterns)
- `/home/jim/5_AgentZero/claudedocs/research_taranis_ai_20251016.md` (OSINT patterns)

### 7.2 External Resources

**Agent Zero Official:**
- GitHub: https://github.com/agent0ai/agent-zero
- Discord: https://discord.gg/B8KZKNsPpj
- Docs: https://github.com/agent0ai/agent-zero/tree/main/docs

**Technologies:**
- FAISS: https://github.com/facebookresearch/faiss
- sentence-transformers: https://www.sbert.net/
- LangChain: https://python.langchain.com/

### 7.3 Team Contacts

**Development Team:**
- Project Lead: [TBD]
- RAG Implementation: [TBD]
- OSINT Implementation: [TBD]
- SuperClaude Integration: [TBD]
- QA & Testing: [TBD]

---

**Document Status:** Development Reference Complete
**Last Updated:** 2025-10-16
**Next Review:** Start of Phase 1 implementation

**Quick Start:** Begin with Section 2 (Phase 1 Implementation) after completing Section 1 (Setup).



---

**Part 2 of 2** | Previous: [01_Core_Development.md](01_Core_Development.md)
