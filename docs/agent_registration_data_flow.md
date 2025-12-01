# Agent Registration Data Flow & Integration

**File**: 2025-11-12_agent_registration_data_flow.md
**Created**: 2025-11-12
**Version**: v1.0.0
**Purpose**: Visual data flow and integration architecture

---

## System Overview Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AGENT DEFINITION SOURCES                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
│  │  YAML Configs    │  │  Markdown Files  │  │  JSON Configs    │      │
│  │                  │  │                  │  │  (Future)        │      │
│  │ • agent_config   │  │ • neo4j-expert   │  │                  │      │
│  │ • swarm_coord    │  │ • researcher     │  │ • API responses  │      │
│  │                  │  │ • cypher-query   │  │ • Remote sources │      │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘      │
│           │                     │                      │                │
└───────────┼─────────────────────┼──────────────────────┼────────────────┘
            │                     │                      │
            └──────────┬──────────┴──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           AGENT PARSER LAYER                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  AgentParser                                                     │    │
│  │  • parseYamlConfig()      → Parse YAML to AgentDefinition[]     │    │
│  │  • parseMarkdownAgent()   → Parse MD frontmatter                │    │
│  │  • normalizeAgentDef()    → Unified schema transformation       │    │
│  │  • discoverAllAgents()    → Scan all sources                    │    │
│  └──────────────────────────┬──────────────────────────────────────┘    │
│                             │                                            │
│                             ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Unified AgentDefinition Schema                                 │    │
│  │  {                                                               │    │
│  │    name: "qdrant_query_agent",                                  │    │
│  │    type: "query_specialist",                                    │    │
│  │    priority: "high",                                            │    │
│  │    capabilities: ["semantic_search", "multi_collection_query"], │    │
│  │    hooks: {...},                                                │    │
│  │    integration: {...}                                           │    │
│  │  }                                                               │    │
│  └──────────────────────────┬──────────────────────────────────────┘    │
│                             │                                            │
└─────────────────────────────┼────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        VALIDATION & ENRICHMENT                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  RegistrationEngine.validateAgent()                             │    │
│  │                                                                  │    │
│  │  ✓ Required Fields:                                             │    │
│  │    • name (unique)                                              │    │
│  │    • type                                                       │    │
│  │    • capabilities (non-empty)                                   │    │
│  │                                                                  │    │
│  │  ✓ Security Checks:                                             │    │
│  │    • Hook script safety                                         │    │
│  │    • Capability whitelist                                       │    │
│  │    • Resource limits                                            │    │
│  │                                                                  │    │
│  │  ✓ Conflict Detection:                                          │    │
│  │    • Duplicate names                                            │    │
│  │    • Type conflicts                                             │    │
│  │                                                                  │    │
│  └──────────────────────────┬──────────────────────────────────────┘    │
│                             │                                            │
│                             ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Enrichment & Transformation                                    │    │
│  │  • Map priority → cognitive pattern                             │    │
│  │  • Generate registration metadata                               │    │
│  │  • Prepare MCP-specific payloads                                │    │
│  └──────────────────────────┬──────────────────────────────────────┘    │
│                             │                                            │
└─────────────────────────────┼────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         REGISTRATION LAYER                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  RegistrationEngine.registerAgent()                             │    │
│  │                                                                  │    │
│  │  Process:                                                       │    │
│  │  1. Validate agent definition                                   │    │
│  │  2. Transform for target MCP servers                            │    │
│  │  3. Register with claude-flow                                   │    │
│  │  4. Register with ruv-swarm                                     │    │
│  │  5. Persist registration state                                  │    │
│  │  6. Update registration cache                                   │    │
│  │  7. Log registration event                                      │    │
│  └──────────────────────────┬──────────────────────────────────────┘    │
│                             │                                            │
│             ┌───────────────┴───────────────┐                            │
│             │                               │                            │
│             ▼                               ▼                            │
│  ┌──────────────────────┐       ┌──────────────────────┐               │
│  │  Claude-Flow         │       │  Ruv-Swarm           │               │
│  │  Registration        │       │  Registration        │               │
│  │                      │       │                      │               │
│  │  • Memory namespace: │       │  • DAA agent create  │               │
│  │    claude-flow-agents│       │  • Memory namespace: │               │
│  │  • Store metadata    │       │    ruv-swarm-agents  │               │
│  │  • Set TTL: 7 days   │       │  • Cognitive pattern │               │
│  └──────────┬───────────┘       └──────────┬───────────┘               │
│             │                               │                            │
└─────────────┼───────────────────────────────┼────────────────────────────┘
              │                               │
              ▼                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         PERSISTENCE LAYER                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  MCP Memory Namespaces                                          │    │
│  │                                                                  │    │
│  │  • claude-flow-agents/                                          │    │
│  │    ├── agent-qdrant_query_agent                                 │    │
│  │    ├── agent-qdrant_memory_agent                                │    │
│  │    ├── agent-neo4j-expert                                       │    │
│  │    └── ...                                                      │    │
│  │                                                                  │    │
│  │  • ruv-swarm-agents/                                            │    │
│  │    ├── agent-qdrant_query_agent                                 │    │
│  │    ├── agent-qdrant_memory_agent                                │    │
│  │    └── ...                                                      │    │
│  │                                                                  │    │
│  │  • agent-registry/ (master registry)                            │    │
│  │    ├── qdrant_query_agent                                       │    │
│  │    ├── qdrant_memory_agent                                      │    │
│  │    └── ...                                                      │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         DISCOVERY & USAGE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Agent Discovery                                                │    │
│  │                                                                  │    │
│  │  mcp__claude_flow__agent_list()                                 │    │
│  │    └─▶ Query claude-flow-agents namespace                       │    │
│  │    └─▶ Return: ["qdrant_query_agent", "neo4j-expert", ...]     │    │
│  │                                                                  │    │
│  │  mcp__ruv_swarm__agent_list()                                   │    │
│  │    └─▶ Query ruv-swarm-agents namespace                         │    │
│  │    └─▶ Return: ["qdrant_memory_agent", "cypher-query-expert"]  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Agent Spawning                                                 │    │
│  │                                                                  │    │
│  │  Via Claude Code Task Tool:                                     │    │
│  │    Task("Agent Name", "Task desc", "qdrant_query_agent")        │    │
│  │      └─▶ Lookup agent definition from registry                  │    │
│  │      └─▶ Spawn with registered capabilities                     │    │
│  │      └─▶ Apply hooks and integration settings                   │    │
│  │                                                                  │    │
│  │  Via MCP Tools:                                                 │    │
│  │    mcp__claude_flow__agent_spawn({                              │    │
│  │      type: "qdrant_query_agent",                                │    │
│  │      capabilities: [...],                                       │    │
│  │      name: "Query-Agent-001"                                    │    │
│  │    })                                                            │    │
│  │      └─▶ Lookup registration from memory                        │    │
│  │      └─▶ Create agent instance                                  │    │
│  │      └─▶ Return agent ID and status                             │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Data Transformation Flow

### YAML → AgentDefinition → MCP Registration

```
┌─────────────────────────────────────────────┐
│  YAML Configuration                         │
├─────────────────────────────────────────────┤
│  agents:                                    │
│    qdrant_query_agent:                      │
│      type: "query_specialist"               │
│      priority: "high"                       │
│      capabilities:                          │
│        - semantic_search                    │
│        - multi_collection_query             │
│      integration:                           │
│        claude_flow_namespace: "qdrant:query"│
│        hook_triggers: ["pre_task"]          │
└──────────────┬──────────────────────────────┘
               │
               │ Parser.parseYamlConfig()
               ▼
┌─────────────────────────────────────────────┐
│  AgentDefinition (Unified Schema)           │
├─────────────────────────────────────────────┤
│  {                                          │
│    name: "qdrant_query_agent",              │
│    type: "query_specialist",                │
│    priority: "high",                        │
│    capabilities: [                          │
│      "semantic_search",                     │
│      "multi_collection_query"               │
│    ],                                       │
│    integration: {                           │
│      claude_flow_namespace: "qdrant:query", │
│      hook_triggers: ["pre_task"]            │
│    }                                        │
│  }                                          │
└──────────────┬──────────────────────────────┘
               │
               │ Engine.registerAgent()
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌─────────────┐  ┌─────────────────┐
│ Claude-Flow │  │  Ruv-Swarm      │
│ Payload     │  │  Payload        │
├─────────────┤  ├─────────────────┤
│ {           │  │ {               │
│   agentType:│  │   id: "qdrant..." │
│   name:     │  │   type: "query_..." │
│   capabili..│  │   cognitivePattern: │
│   priority: │  │     "adaptive"  │
│   hooks:    │  │   capabilities: │
│   integra.. │  │   enableMemory: │
│   register..│  │     true        │
│ }           │  │ }               │
└──────┬──────┘  └────────┬────────┘
       │                  │
       │ MCP Memory Store │
       ▼                  ▼
┌──────────────────────────────────┐
│  Persistent Memory Namespaces    │
├──────────────────────────────────┤
│  claude-flow-agents/             │
│    agent-qdrant_query_agent      │
│                                  │
│  ruv-swarm-agents/               │
│    agent-qdrant_query_agent      │
│                                  │
│  agent-registry/                 │
│    qdrant_query_agent            │
└──────────────────────────────────┘
```

---

## Registration State Machine

```
┌──────────────┐
│ Unregistered │
│  (Initial)   │
└──────┬───────┘
       │
       │ discoverAgent()
       ▼
┌──────────────┐
│  Discovered  │──────┐
│              │      │ validateAgent() FAIL
└──────┬───────┘      │
       │              │
       │ validate()   │
       │ SUCCESS      │
       ▼              │
┌──────────────┐      │
│  Validated   │      │
│              │      │
└──────┬───────┘      │
       │              │
       │ register()   │
       ▼              │
┌──────────────┐      │
│ Registering  │──────┤
│              │      │ register() FAIL
└──────┬───────┘      │
       │              │
       │ SUCCESS      │
       ▼              │
┌──────────────┐      │
│  Registered  │      │
│  (Active)    │      │
└──────┬───────┘      │
       │              │
       │              │
       │ spawn()      │
       ▼              ▼
┌──────────────┐  ┌─────────┐
│   Spawned    │  │ Failed  │
│  (Running)   │  │         │
└──────────────┘  └─────────┘
```

---

## Memory Namespace Architecture

```
MCP Memory System
├── claude-flow-agents/          # Claude-Flow agent registry
│   ├── agent-qdrant_query_agent
│   │   └── { agentType, capabilities, priority, hooks, integration }
│   ├── agent-qdrant_memory_agent
│   │   └── { ... }
│   └── agent-neo4j-expert
│       └── { ... }
│
├── ruv-swarm-agents/            # Ruv-Swarm agent registry
│   ├── agent-qdrant_query_agent
│   │   └── { id, type, cognitivePattern, capabilities }
│   ├── agent-qdrant_memory_agent
│   │   └── { ... }
│   └── agent-cypher-query-expert
│       └── { ... }
│
├── agent-registry/              # Master registry (all agents)
│   ├── qdrant_query_agent
│   │   └── { name, type, status, registeredAt, servers: [...] }
│   ├── qdrant_memory_agent
│   │   └── { ... }
│   └── neo4j-expert
│       └── { ... }
│
├── agent-activities/            # Runtime activity tracking
│   ├── agent-{id}-spawn
│   ├── agent-{id}-complete
│   └── agent-{id}-metrics
│
└── wiki-notifications/          # Wiki agent notifications
    └── wiki-event-{timestamp}
```

---

## Hook Execution Flow

```
┌────────────────────────────────────────────────┐
│         Agent Spawn Request                    │
│  Task("Agent", "Task", "qdrant_query_agent")   │
└──────────────────┬─────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────┐
│  1. Lookup Agent in Registry                   │
│     • Query agent-registry namespace           │
│     • Retrieve agent definition                │
│     • Load hooks and integration settings      │
└──────────────────┬─────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────┐
│  2. Pre-Spawn Hook Execution                   │
│     • Execute hook.pre script                  │
│     • Store context in memory                  │
│     • Notify hive-mind                         │
└──────────────────┬─────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────┐
│  3. Agent Instance Creation                    │
│     • Spawn agent with MCP tool                │
│     • Apply capabilities                       │
│     • Set resource limits                      │
└──────────────────┬─────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────┐
│  4. Task Execution                             │
│     • Agent performs task                      │
│     • Periodic status updates                  │
│     • Memory operations                        │
└──────────────────┬─────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────┐
│  5. Post-Task Hook Execution                   │
│     • Execute hook.post script                 │
│     • Store results in memory                  │
│     • Update agent metrics                     │
│     • Notify Wiki Agent                        │
└──────────────────┬─────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────┐
│  6. Cleanup & Logging                          │
│     • Log execution time                       │
│     • Update agent statistics                  │
│     • Persist state for future runs            │
└────────────────────────────────────────────────┘
```

---

## Multi-Agent Coordination Flow

```
┌─────────────────────────────────────────────────────────┐
│  User Request: "Process cybersecurity threat data"      │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Orchestration Layer (Claude Code)                      │
│  • Analyze request complexity                           │
│  • Identify required agent types                        │
│  • Plan parallel execution                              │
└──────────────────────┬──────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
┌──────────────────┐        ┌──────────────────┐
│  Spawn Researcher│        │  Spawn Analyzer  │
│  (qdrant_query)  │        │  (pattern_agent) │
└────────┬─────────┘        └────────┬─────────┘
         │                           │
         │ Hook: pre_task            │ Hook: pre_task
         ▼                           ▼
┌──────────────────┐        ┌──────────────────┐
│  Execute Research│        │  Execute Analysis│
│  • Search Qdrant │        │  • Identify      │
│  • Extract threats│       │    patterns      │
│  • Store findings│        │  • Cluster data  │
└────────┬─────────┘        └────────┬─────────┘
         │                           │
         │ Store in memory           │ Store in memory
         │ namespace: findings       │ namespace: patterns
         │                           │
         └─────────────┬─────────────┘
                       │
                       ▼
         ┌─────────────────────────────┐
         │  Memory Coordination        │
         │  • findings/research-001    │
         │  • patterns/analysis-001    │
         └─────────────┬───────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Spawn Integrator Agent                                 │
│  • Read from memory namespaces                          │
│  • Combine findings + patterns                          │
│  • Store integrated results                             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Final Results                                          │
│  • Comprehensive threat analysis                        │
│  • Pattern-based insights                               │
│  • Actionable recommendations                           │
└─────────────────────────────────────────────────────────┘
```

---

## Error Handling & Recovery Flow

```
┌─────────────────────┐
│  Registration Start │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │  Parse Agent │──────▶ Parse Error ──────┐
    └──────┬───────┘                          │
           │                                  │
           ▼                                  │
    ┌──────────────┐                         │
    │  Validate    │──────▶ Validation Error─┤
    └──────┬───────┘                          │
           │                                  │
           ▼                                  │
    ┌──────────────┐                         │
    │  Register    │──────▶ Registration     │
    │  with MCP    │        Error            │
    └──────┬───────┘                          │
           │                                  │
           │ Success                          │
           ▼                                  │
    ┌──────────────┐                         │
    │  Verify      │──────▶ Verification     │
    │  Registration│        Failed           │
    └──────┬───────┘                          │
           │                                  │
           │ Success                          │
           ▼                                  │
    ┌──────────────┐                         │
    │  Persist     │──────▶ Persistence      │
    │  State       │        Failed           │
    └──────┬───────┘                          │
           │                                  │
           │ Success                          │
           ▼                                  │
    ┌──────────────┐                         │
    │  Complete    │                         │
    └──────────────┘                         │
                                             │
           ┌─────────────────────────────────┘
           │
           ▼
    ┌──────────────┐
    │  Error       │
    │  Handler     │
    └──────┬───────┘
           │
           ├─▶ Log error
           ├─▶ Retry with backoff
           ├─▶ Skip and continue
           └─▶ Rollback changes
```

---

## Integration Points Summary

### Claude Code Task Tool Integration
```
Task("Agent Name", "Task Description", "agent_type")
          │                    │              │
          │                    │              └─▶ Lookup in agent-registry
          │                    │
          │                    └─▶ Pass to agent instance
          │
          └─▶ Display name for user tracking
```

### MCP Tool Integration
```
mcp__claude_flow__agent_spawn({ type: "agent_type", ... })
          │
          └─▶ Query claude-flow-agents namespace
          └─▶ Load agent definition
          └─▶ Spawn with registered capabilities
```

### Memory System Integration
```
Registration ──▶ Memory Store ──▶ Namespaces ──▶ Discovery ──▶ Spawn
```

### Hook System Integration
```
Pre-Task Hook ──▶ Agent Execution ──▶ Post-Task Hook ──▶ Wiki Notification
```

---

**Status**: ✅ ARCHITECTURE COMPLETE
**Ready for**: Implementation Phase
