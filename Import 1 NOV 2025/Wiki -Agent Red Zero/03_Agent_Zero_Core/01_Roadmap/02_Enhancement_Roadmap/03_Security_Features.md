---
title: "Agent Zero - 03 Security Features"
category: "03_Agent_Zero_Core/01_Roadmap/02_Enhancement_Roadmap"
part: "3 of 4"
line_count: 348
last_updated: 2025-10-25
status: published
tags: ['agent-zero', 'roadmap', 'core']
related:
  - "02_MCP_Integration.md"
  - "04_Advanced_Capabilities.md"
---

            "extract_entities": {
                "type": "boolean",
                "description": "Extract CVEs, IPs, domains from results",
                "default": true
            }
        },
        "required": ["query"]
    }
}
```

#### Integration with Existing Architecture

**Modifications:**

1. **Enhanced `search_engine.py`:**
```python
# Add OSINT mode to existing search_engine.py
# No breaking changes, just additions

async def execute(self, query, mode="standard", **kwargs):
    if mode == "osint":
        # Delegate to OSINT collector
        from python.tools.osint_collector import OSINTCollector
        osint = OSINTCollector(self.agent, self.name, self.args, self.message)
        return await osint.execute(query, **kwargs)
    else:
        # Existing search behavior
        return await self._standard_search(query)
```

2. **Prompt Integration:**

```markdown
# prompts/default/tools/osint_collector.md

# OSINT Collection Tool

Collect open-source intelligence from multiple sources.

## When to Use
- Threat intelligence gathering
- Vulnerability research (CVE analysis)
- Domain/IP reconnaissance
- Security news monitoring
- Incident investigation

## Usage Examples

1. **CVE Intelligence:**
   ```
   Use osint_collector to research CVE-2024-1234
   ```

2. **Threat Actor Research:**
   ```
   Collect intelligence on "APT29 recent activity"
   ```

3. **Domain Investigation:**
   ```
   Investigate "suspicious-domain.com" using OSINT sources
   ```

## Outputs
- Multi-source results (web + news)
- Extracted entities (CVEs, IPs, domains)
- Stored in memory for future reference
- Formatted intelligence report
```

### Implementation Metrics

**Performance Targets:**
- Multi-source collection: <5 seconds
- Entity extraction: <1 second
- Memory storage: <500ms
- Zero new heavy dependencies

**Success Criteria:**
- OSINT collection operational with existing tools
- Entity extraction using regex (no heavy NLP)
- Seamless integration with search_engine.py
- Intelligence stored in memory system

---

## Part 5: Priority 3 - SuperClaude Deep Integration

### Current State

**SuperClaude Capabilities:**
- Deep research mode (/sc:research)
- Multi-agent orchestration
- MCP server integration (Tavily, Sequential, Context7, etc.)
- Task breakdown and delegation
- Session persistence with Serena MCP

**Agent Zero Capabilities:**
- MCP server mode (can act as MCP server)
- MCP client (can use external MCP servers)
- A2A protocol (Agent-to-Agent communication)

**Current Gap:**
- No direct SuperClaude → Agent Zero workflow
- No shared memory/context
- Manual handoff required

### Enhancement Design: SuperClaude Bridge

**Design Philosophy:**
- Leverage existing MCP and A2A infrastructure
- Create bidirectional communication channel
- Share memory and context seamlessly
- Enable workflow orchestration

#### Implementation Specification

**File Structure:**
```
python/helpers/
└── superclaude_bridge.py (NEW)

python/api/
└── superclaude_webhook.py (NEW - API endpoint)

prompts/default/
└── superclaude_integration.md (NEW - guidance)
```

**New Module: `superclaude_bridge.py`**

```python
# python/helpers/superclaude_bridge.py
"""
SuperClaude <-> Agent Zero Integration Bridge

Enables bidirectional communication using existing protocols:
- A2A (Agent-to-Agent) for task delegation
- MCP for tool sharing
- Shared memory via file system
"""

from typing import Dict, Any, Optional
import json, asyncio
from python.helpers.fasta2a_client import Fasta2aClient
from python.helpers import files
from agent import Agent

class SuperClaudeBridge:
    """
    Bridge for SuperClaude integration

    Workflows:
    1. SuperClaude → Agent Zero: Research → Execution
    2. Agent Zero → SuperClaude: Task → Deep Analysis
    3. Shared Memory: Bidirectional context sharing
    """

    def __init__(self, agent: Agent):
        self.agent = agent
        self.a2a_client = None

    async def send_to_superclaude(
        self,
        task_type: str,
        task_data: Dict[str, Any],
        endpoint: str = "http://localhost:3000"  # SuperClaude API
    ) -> Dict[str, Any]:
        """
        Send task to SuperClaude for deep research/analysis

        Args:
            task_type: "research", "analysis", "design", etc.
            task_data: Task parameters
            endpoint: SuperClaude API endpoint

        Returns:
            SuperClaude response
        """

        # Prepare request
        request = {
            "type": task_type,
            "data": task_data,
            "context": await self._get_shared_context(),
            "agent_id": self.agent.agent_name
        }

        # Send via A2A protocol (existing Agent Zero capability)
        if not self.a2a_client:
            self.a2a_client = Fasta2aClient(endpoint)

        response = await self.a2a_client.send_message(
            message=json.dumps(request),
            await_response=True
        )

        # Store SuperClaude response in memory
        await self._store_superclaude_response(response)

        return json.loads(response) if isinstance(response, str) else response

    async def _get_shared_context(self) -> Dict[str, Any]:
        """
        Get current agent context for SuperClaude

        Includes:
        - Recent conversation history
        - Current task state
        - Relevant memories
        """
        context = {
            "agent_name": self.agent.agent_name,
            "current_task": self.agent.get_data("current_task", ""),
            "recent_history": self._get_recent_history(last_n=5)
        }

        return context

    def _get_recent_history(self, last_n: int = 5) -> list:
        """Extract recent conversation history"""
        if hasattr(self.agent, 'history'):
            history = self.agent.history[-last_n:]
            return [
                {"role": msg.role, "content": msg.content}
                for msg in history
            ]
        return []

    async def _store_superclaude_response(self, response: Any):
        """Store SuperClaude response in Agent Zero memory"""
        from python.helpers.memory import Memory
        from langchain_core.documents import Document

        memory = await Memory.get(self.agent)

        doc = Document(
            page_content=json.dumps(response, indent=2),
            metadata={
                "type": "superclaude_response",
                "timestamp": Memory.get_timestamp(),
                "area": "main"
            }
        )

        await memory.insert_documents([doc])

    async def receive_from_superclaude(
        self,
        task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Receive and execute task from SuperClaude

        Args:
            task_data: Task from SuperClaude (via A2A or webhook)

        Returns:
            Execution result
        """

        task_type = task_data.get("type")

        if task_type == "execute_code":
            return await self._execute_code_task(task_data)

        elif task_type == "osint_collection":
            return await self._osint_task(task_data)

        elif task_type == "browser_automation":
            return await self._browser_task(task_data)

        else:
            return {"error": f"Unknown task type: {task_type}"}

    async def _execute_code_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code using Agent Zero's code execution tool"""
        from python.tools.code_execution_tool import CodeExecution

        code_tool = CodeExecution(
            agent=self.agent,
            name="code_execution",
            args={},
            message=None
        )

        result = await code_tool.execute(
            runtime=task_data.get("runtime", "python"),
            code=task_data.get("code", "")
        )

        return {
            "success": True,
            "output": result.message
        }

    async def _osint_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute OSINT collection"""
        from python.tools.osint_collector import OSINTCollector

        osint_tool = OSINTCollector(
            agent=self.agent,
            name="osint_collector",
            args={},
            message=None
        )

        result = await osint_tool.execute(**task_data.get("params", {}))

        return {
            "success": True,
            "results": result.message
        }

    async def _browser_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute browser automation"""
        from python.tools.browser_agent import BrowserAgent

        browser_tool = BrowserAgent(
            agent=self.agent,
            name="browser_agent",
            args={},
            message=None
        )

        result = await browser_tool.execute(
            prompt=task_data.get("prompt", ""),
            **task_data.get("params", {})
        )

        return {
            "success": True,
            "output": result.message
        }

    @staticmethod
    async def create_shared_workspace(
        workspace_name: str = "superclaude_agentzero"
    ) -> str:
        """
        Create shared workspace directory for file-based collaboration

        Returns:
            Workspace path
        """
        workspace_path = files.get_abs_path("work_dir", workspace_name)
        import os
        os.makedirs(workspace_path, exist_ok=True)

        # Create README
        readme = f"""# SuperClaude <-> Agent Zero Shared Workspace

Created: {Memory.get_timestamp()}

## Purpose
This workspace is for bidirectional file sharing between SuperClaude and Agent Zero.

## Usage
- SuperClaude places research results here
- Agent Zero places execution results here
- Both can read/write files for collaboration

## Structure
- /research/ - SuperClaude research outputs
- /execution/ - Agent Zero execution results
- /shared/ - Bidirectional collaboration files
"""

        files.write_file(
            files.get_abs_path(workspace_path, "README.md"),
            readme
        )

        return workspace_path
```

**API Endpoint for SuperClaude Webhooks:**

```python
# python/api/superclaude_webhook.py
"""
API endpoint for SuperClaude to send tasks to Agent Zero
"""

from flask import request, jsonify
from python.helpers import api
from python.helpers.superclaude_bridge import SuperClaudeBridge
import asyncio

def setup_routes(app):
    @app.route('/api/superclaude/task', methods=['POST'])
    @api.require_auth
    async def superclaude_task():
        """
        Receive task from SuperClaude

        POST /api/superclaude/task
        {
            "type": "execute_code" | "osint_collection" | "browser_automation",
            "data": { ... },
            "context": { ... }
        }
        """
        try:
            task_data = request.json

            # Get agent instance (use Agent 0)
            from initialize import initialize_agent
            agent_config = initialize_agent()
            from agent import Agent
            agent = Agent(0, agent_config)

            # Create bridge
            bridge = SuperClaudeBridge(agent)

            # Execute task
            result = await bridge.receive_from_superclaude(task_data)

            return jsonify({
                "success": True,
                "result": result
            })

        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

    @app.route('/api/superclaude/status', methods=['GET'])
    @api.require_auth
    def superclaude_status():
        """Check SuperClaude integration status"""
        return jsonify({
            "integration": "active",
            "endpoints": [
                "/api/superclaude/task",
                "/api/superclaude/status"
            ],


---

**Part 3 of 4** | Next: [04_Advanced_Capabilities.md](04_Advanced_Capabilities.md) | Previous: [02_MCP_Integration.md](02_MCP_Integration.md)
