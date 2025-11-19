# Custom Agent Accessibility Investigation Report
**Date:** 2025-11-12
**Investigator:** Research Agent
**Status:** COMPLETE

---

## Executive Summary

**ROOT CAUSE IDENTIFIED:** Custom Qdrant agents are **Python classes**, NOT MCP-registered agent types. They exist as **utility libraries** that can be called FROM agents, but are not themselves agents that can be spawned via MCP tools.

**Key Finding:** The user created 6 specialized **agent classes** (Python) but expected them to be **agent types** (MCP spawnable entities). These are fundamentally different concepts in the Claude-Flow architecture.

---

## Investigation Findings

### 1. Where Are The 12 Custom Agents Defined?

**Located:** `/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/qdrant_agents/`

**Breakdown:**
1. **6 Qdrant Agent Classes** (in `core/`):
   - `QdrantQueryAgent` - Semantic search specialist
   - `QdrantMemoryAgent` - Cross-agent memory coordinator
   - `QdrantPatternAgent` - Pattern discovery with ML clustering
   - `QdrantDecisionAgent` - Architecture decision tracker
   - `QdrantSyncAgent` - Bidirectional sync between Qdrant and local
   - `QdrantAnalyticsAgent` - Performance monitoring and optimization

2. **Agent Tracker TypeScript Class** (in web_interface):
   - `AgentActivityTracker` - Tracks spawns, executions, completions
   - **NOT an agent type** - monitoring/logging utility

**Total:** 6 actual agent classes + 1 tracker utility = 7 (not 12)

**Configuration File:** `qdrant_agents/config/agent_config.yaml` defines agent behavior, capabilities, and hook triggers.

---

### 2. Why Aren't They Accessible Via MCP Tools?

**CRITICAL DISTINCTION:**

| Concept | What It Is | How It's Used | Example |
|---------|-----------|---------------|---------|
| **MCP Agent Type** | Spawnable entity via MCP tools | `mcp__claude-flow__agent_spawn { type: "researcher" }` | `researcher`, `coder`, `analyst` |
| **Python Agent Class** | Utility library with specialized functions | Import and call methods directly | `QdrantQueryAgent.search_knowledge()` |

**The Problem:**
- User created **Python agent classes** (libraries with methods)
- Expected them to be **MCP agent types** (spawnable via `agent_spawn`)
- MCP tools only recognize hardcoded agent types: `researcher`, `coder`, `analyst`, `optimizer`, `coordinator`

**Evidence from MCP Tool Calls:**
```bash
# This works (generic MCP agent type):
mcp__claude-flow__agent_spawn { type: "researcher", name: "Bot1" }

# This FAILS (custom Python class):
mcp__claude-flow__agent_spawn { type: "qdrant_query_agent", name: "QueryBot" }
# Error: Unknown agent type
```

**Evidence from claude-flow CLI:**
```bash
$ npx claude-flow@alpha agent list
📋 No agents currently active

To create agents:
  claude-flow agent spawn researcher --name "ResearchBot"  ✅ Generic types only
  claude-flow agent spawn coder --name "CodeBot"
  claude-flow agent spawn analyst --name "DataBot"
```

---

### 3. What's The Missing Registration/Initialization Step?

**FUNDAMENTAL ARCHITECTURE MISMATCH:**

There is NO registration step because these aren't designed to be MCP agent types. They're designed as **callable libraries**.

**How They SHOULD Be Used (Current Architecture):**

```python
# Option 1: Call from within an agent's task
from qdrant_agents.core import QdrantQueryAgent

agent = QdrantQueryAgent(url="http://localhost:6333")
results = agent.search_schema_knowledge(query="SAREF sensors", top_k=5)
```

```python
# Option 2: Use the bridge interface
from qdrant_agents.integration import get_bridge

bridge = get_bridge()
results = bridge.search_knowledge(query="SAREF sensors", wave=3)
```

**How They CANNOT Be Used:**
```javascript
// ❌ This will NEVER work (no such registration system exists):
Task("Qdrant Query Agent", "Search for SAREF sensors", "qdrant_query_agent")
```

---

### 4. How Should Custom Agents Be Properly Registered?

**Answer:** They shouldn't be "registered" - they should be **integrated** as tools/utilities that generic agents call.

**Three Integration Approaches:**

#### Approach A: Generic Agent + Python Library (Current/Correct)
```javascript
// Spawn a generic researcher agent
Task("Researcher", `
  Execute Python script:

  from qdrant_agents.core import QdrantQueryAgent
  agent = QdrantQueryAgent(url="http://localhost:6333")
  results = agent.search_schema_knowledge(query="SAREF sensors", top_k=5)

  Analyze and report findings.
`, "researcher")
```

#### Approach B: Create MCP Wrapper (New Development Required)
To make these TRUE MCP agent types, you'd need to:

1. **Create MCP Server Plugin** (Node.js/TypeScript):
```typescript
// qdrant-agents-mcp/src/index.ts
import { McpServer } from '@modelcontextprotocol/sdk';

const server = new McpServer({
  name: 'qdrant-agents',
  version: '1.0.0',
  tools: {
    'qdrant-search': {
      description: 'Search Qdrant knowledge base',
      parameters: { /* ... */ },
      handler: async (params) => {
        // Call Python bridge
        const result = await execAsync(
          `python3 -m qdrant_agents.integration.claude_flow_bridge search_knowledge --params '${JSON.stringify(params)}'`
        );
        return JSON.parse(result);
      }
    }
  }
});

server.start();
```

2. **Register in ~/.claude/settings.json:**
```json
{
  "mcpServers": {
    "qdrant-agents": {
      "command": "npx",
      "args": ["qdrant-agents-mcp"]
    }
  }
}
```

3. **Use as MCP Tool (not agent type):**
```javascript
// Still not spawnable as agent, but callable as tool:
const results = await mcp__qdrant_agents__search({
  query: "SAREF sensors",
  collection: "schema_knowledge"
});
```

#### Approach C: Agent Wrapper Scripts (Simplest Fix)
Create wrapper agents that delegate to Python classes:

```bash
# /home/jim/2_OXOT_Projects_Dev/scripts/qdrant_query_agent_wrapper.sh
#!/bin/bash
TASK="$1"
python3 -m qdrant_agents.integration.claude_flow_bridge search_knowledge \
  --params "{\"query\": \"$TASK\", \"top_k\": 5}"
```

Then spawn generic agents with specific instructions:
```javascript
Task("Qdrant Query Specialist", `
  Execute: /home/jim/2_OXOT_Projects_Dev/scripts/qdrant_query_agent_wrapper.sh "SAREF sensors"
  Parse results and provide analysis.
`, "researcher")
```

---

## Architectural Analysis

### Current System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Agent System                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Generic Agent Types (Spawnable via MCP):                  │
│  ├─ researcher                                             │
│  ├─ coder                                                  │
│  ├─ analyst                                                │
│  ├─ optimizer                                              │
│  └─ coordinator                                            │
│                                                             │
│  These agents can:                                         │
│  - Call Python scripts                                     │
│  - Import libraries                                        │
│  - Use MCP tools                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                           ↓ calls
┌─────────────────────────────────────────────────────────────┐
│              Qdrant Agents (Python Library)                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Python Classes (NOT spawnable):                           │
│  ├─ QdrantQueryAgent      (search operations)              │
│  ├─ QdrantMemoryAgent     (memory operations)              │
│  ├─ QdrantPatternAgent    (ML clustering)                  │
│  ├─ QdrantDecisionAgent   (ADR tracking)                   │
│  ├─ QdrantSyncAgent       (sync operations)                │
│  └─ QdrantAnalyticsAgent  (monitoring)                     │
│                                                             │
│  Integration Bridge:                                        │
│  └─ ClaudeFlowBridge (unified interface)                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Why The Confusion Occurred

1. **Naming Convention:** Files named `*_agent.py` implied they were MCP agent types
2. **Configuration File:** `agent_config.yaml` with "agents:" section suggested MCP registration
3. **Hook Integration:** Hooks in `agent_config.yaml` implied MCP-level integration
4. **Documentation:** README.md described them as "6 specialized agents" without clarifying they're libraries

---

## Correct Usage Patterns

### Pattern 1: Direct Python Import (Within Agent Task)
```javascript
Task("Research Agent", `
  from qdrant_agents.integration import get_bridge

  bridge = get_bridge()

  # Search knowledge
  results = bridge.search_knowledge(
    query="How to implement SAREF energy sensors?",
    wave=3,
    top_k=5
  )

  # Analyze results
  for result in results['results']:
    print(f"- {result['payload']['section_title']}")
    print(f"  Score: {result['score']}")
    print(f"  Source: {result['payload']['file_source']}")
`, "researcher")
```

### Pattern 2: Bridge CLI Interface
```bash
# Call via command line (from any agent)
python3 -m qdrant_agents.integration.claude_flow_bridge \
  search_knowledge \
  --params '{"query": "SAREF sensors", "wave": 3, "top_k": 5}'
```

### Pattern 3: Pre/Post-Task Hooks (Automated)
```yaml
# In agent_config.yaml
hooks:
  pre_task:
    enabled: true
    agents: ["qdrant_query_agent", "qdrant_memory_agent"]
    # These trigger automatically before tasks
```

The hooks call the Python classes automatically, not via MCP spawning.

---

## MCP Tool Analysis Results

### ruv-swarm MCP Tools:
- **Agent Registration:** 0 custom agents
- **Agent Types:** Only generic types (researcher, coder, analyst, optimizer, coordinator)
- **Custom Agent Support:** None (hardcoded types only)

### claude-flow MCP Tools:
- **Agent Registration:** 3 generic agents available
- **Agent Types:** researcher, coder, analyst (expandable but requires MCP server development)
- **Custom Agent Support:** Via MCP server plugins (not currently implemented for Qdrant agents)

---

## Recommended Solutions

### Immediate Solution (No Code Changes)

**Use generic agents that call Qdrant library:**

```javascript
// Correct pattern used during upload pipeline implementation:
Task("Upload Researcher", `
  Research optimal upload strategies using Qdrant knowledge base:

  from qdrant_agents.integration import get_bridge
  bridge = get_bridge()

  # Search for similar implementations
  results = bridge.find_similar_implementations(
    description="bulk upload CSV to Neo4j",
    top_k=5
  )

  # Retrieve past experiences
  experiences = bridge.retrieve_experiences(
    query="upload optimization",
    top_k=3
  )

  Synthesize findings into recommendations.
`, "researcher")
```

### Long-Term Solution (Requires Development)

**Option 1: Create MCP Server for Qdrant Agents**
- Package as Node.js MCP server
- Expose Qdrant agent functions as MCP tools
- Register in ~/.claude/settings.json
- Still not spawnable agents, but callable as tools

**Option 2: Rename to Clarify Purpose**
- Rename `*_agent.py` → `*_service.py` or `*_tool.py`
- Update documentation to call them "Qdrant Services" not "Agents"
- Emphasize library/utility nature

**Option 3: Agent Wrapper Layer**
- Create shell script wrappers for each Qdrant agent class
- Generic agents can execute these scripts
- Simpler than full MCP server development

---

## Gap Analysis

| Expected | Actual | Gap |
|----------|--------|-----|
| 12 spawnable agent types | 6 Python library classes + 1 tracker | Architecture mismatch |
| MCP agent registration | Import-based library usage | No registration system |
| Direct agent spawning | Call via generic agents | Indirect access only |
| MCP tool integration | Python CLI bridge | No MCP server |

---

## Conclusion

**The 12 custom agents are NOT MISSING - they're MISCLASSIFIED.**

They exist as fully functional Python libraries but were never meant to be spawned as MCP agent types. The confusion arose from:

1. Naming convention (`*_agent.py`)
2. Configuration structure (`agent_config.yaml`)
3. Documentation describing them as "agents"

**Current State:**
- ✅ 6 Qdrant agent classes fully implemented and functional
- ✅ Bridge interface for easy calling
- ✅ Hook system for automated integration
- ❌ NOT spawnable via MCP agent_spawn tools
- ❌ NOT registered as MCP agent types

**Correct Usage:**
- Spawn generic MCP agents (researcher, coder, etc.)
- Have those agents call Qdrant library functions
- Use bridge interface or direct imports

**To Make Them Spawnable (Future Work):**
- Develop MCP server wrapper (Node.js/TypeScript)
- Register in Claude settings
- Expose as MCP tools (not agent types)

---

## Action Items

1. ✅ **Document correct usage patterns** (this report)
2. ⚠️ **Update agent naming** (`*_service.py` or add clear docstrings)
3. ⚠️ **Create usage examples** showing generic agent + Qdrant library pattern
4. 🔮 **Future:** Consider MCP server wrapper if direct tool calling is needed

---

## Example: How Upload Pipeline Should Have Been Implemented

```javascript
// CORRECT: Generic agents calling Qdrant libraries
[Single Message - All Agents Spawned]:

  // Research Agent (uses Qdrant Query Agent internally)
  Task("Upload Research Agent", `
    from qdrant_agents.integration import get_bridge
    bridge = get_bridge()

    # Find similar upload implementations
    similar = bridge.find_similar_implementations(
      description="CSV bulk upload to Neo4j graph database",
      top_k=5
    )

    # Search for optimization patterns
    patterns = bridge.find_patterns(
      query="upload optimization batch processing",
      top_k=3
    )

    Report findings: optimal batch size, error handling, performance tips
  `, "researcher"),

  // Implementation Agent (records decisions in Qdrant)
  Task("Upload Coder Agent", `
    Implement upload pipeline based on research findings.

    After implementation, record decision:

    from qdrant_agents.integration import get_bridge
    bridge = get_bridge()

    bridge.record_decision(
      decision="Batch size of 1000 rows with parallel processing",
      rationale="Balances memory usage and throughput based on research",
      alternatives=["Single threaded", "Larger batches"],
      wave=None,
      made_by="Upload Coder Agent"
    )
  `, "coder"),

  // All other agents follow same pattern...
```

---

**Report Status:** COMPLETE
**Deliverable:** Detailed analysis answering all investigation questions
**Next Steps:** Review recommendations and decide on long-term integration strategy
