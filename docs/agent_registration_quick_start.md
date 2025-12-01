# Agent Registration Quick Start Guide

**File**: 2025-11-12_agent_registration_quick_start.md
**Created**: 2025-11-12
**Version**: v1.0.0
**Purpose**: Quick implementation guide for agent registration system

---

## TL;DR - Execute This to Register Agents

```bash
# 1. Initialize hive-mind
npx claude-flow@alpha hive-mind init

# 2. Run registration script (after implementation)
bash scripts/register-agents.sh

# 3. Verify registrations
bash scripts/verify-agents.sh

# 4. Use custom agents
# Via Claude Code Task tool:
Task("Query Agent", "Search threats", "qdrant_query_agent")
```

---

## Implementation Checklist

### Phase 1: Setup (30 minutes)

- [ ] Create project structure
  ```bash
  mkdir -p agent-registration/{src,scripts,tests,config,docs}
  cd agent-registration
  npm init -y
  npm install yaml glob fs-extra
  npm install -D typescript ts-node @types/node
  ```

- [ ] Create tsconfig.json
  ```json
  {
    "compilerOptions": {
      "target": "ES2020",
      "module": "commonjs",
      "outDir": "./dist",
      "rootDir": "./src",
      "strict": true,
      "esModuleInterop": true
    }
  }
  ```

- [ ] Initialize hive-mind
  ```bash
  npx claude-flow@alpha hive-mind init
  npx claude-flow@alpha hive-mind status
  ```

### Phase 2: Core Implementation (2-3 hours)

- [ ] Implement `src/types.ts` (interface definitions)
- [ ] Implement `src/agent-parser.ts` (YAML/MD parsing)
- [ ] Implement `src/registration-engine.ts` (registration logic)
- [ ] Implement `src/mcp-adapter.ts` (MCP interface)
- [ ] Implement `src/index.ts` (main entry point)

### Phase 3: Scripts (1 hour)

- [ ] Create `scripts/register-agents.sh` (automated registration)
- [ ] Create `scripts/verify-agents.sh` (verification)
- [ ] Create `scripts/agent-status.sh` (dashboard)
- [ ] Make scripts executable
  ```bash
  chmod +x scripts/*.sh
  ```

### Phase 4: Testing (1 hour)

- [ ] Test agent discovery
  ```bash
  npx ts-node -e "
  const { AgentParser } = require('./src/agent-parser');
  const parser = new AgentParser();
  parser.discoverAllAgents().then(agents => {
    console.log('Found agents:', agents.length);
    agents.forEach(a => console.log('  -', a.name));
  });
  "
  ```

- [ ] Test registration
  ```bash
  npm run register
  ```

- [ ] Verify agents in memory
  ```bash
  npx claude-flow@alpha memory list --namespace claude-flow-agents
  npx claude-flow@alpha memory list --namespace ruv-swarm-agents
  ```

- [ ] Test agent spawn
  ```typescript
  // Via Claude Code Task tool
  Task("Test Agent", "Test task", "qdrant_query_agent")
  ```

---

## Critical Files to Create

### 1. `src/types.ts`

```typescript
export interface AgentDefinition {
  name: string;
  type: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  capabilities: string[];
  hooks?: {
    pre?: string | string[];
    post?: string | string[];
    triggers?: string[];
  };
  integration?: {
    namespace?: string;
    claude_flow_namespace?: string;
    hook_triggers?: string[];
  };
  resources?: {
    memory_mb?: number;
    timeout_seconds?: number;
  };
  performance?: Record<string, any>;
  collections?: {
    primary?: string;
    secondary?: string[];
    query?: string[];
    store?: string;
  };
}

export interface RegistrationResult {
  total: number;
  registered: number;
  failed: number;
  errors: string[];
}
```

### 2. `scripts/register-agents.sh`

```bash
#!/bin/bash
set -e

echo "🚀 Registering Custom Agents with MCP Servers"
echo "=============================================="

# Initialize if needed
if ! npx claude-flow@alpha hive-mind status &>/dev/null; then
  echo "Initializing hive-mind..."
  npx claude-flow@alpha hive-mind init
fi

# Run registration
echo "Running registration engine..."
npx ts-node src/index.ts

# Verify
echo ""
echo "Verification:"
npx claude-flow@alpha memory list --namespace claude-flow-agents | grep "agent-" || echo "No agents registered"

echo ""
echo "✅ Registration Complete!"
```

### 3. `scripts/verify-agents.sh`

```bash
#!/bin/bash

echo "🔍 Agent Registration Status"
echo "============================"
echo ""

# Count registered agents
cf_count=$(npx claude-flow@alpha memory list --namespace claude-flow-agents 2>/dev/null | grep -c "agent-" || echo "0")
ruv_count=$(npx claude-flow@alpha memory list --namespace ruv-swarm-agents 2>/dev/null | grep -c "agent-" || echo "0")

echo "Claude-Flow: $cf_count agents"
echo "Ruv-Swarm:   $ruv_count agents"
echo ""

# List agents
echo "Registered Agents:"
npx claude-flow@alpha memory list --namespace claude-flow-agents 2>/dev/null | \
  grep -oP 'agent-\K[^"]+' | \
  sed 's/^/  ✓ /'

echo ""
echo "✅ Verification Complete"
```

---

## Usage After Registration

### Spawn Custom Agents via Task Tool

```typescript
// Qdrant query agent
Task(
  "Qdrant Query Agent",
  "Execute semantic search for threat patterns",
  "qdrant_query_agent"
);

// Neo4j expert agent
Task(
  "Neo4j Expert",
  "Optimize graph queries for performance",
  "neo4j-expert"
);

// Multiple custom agents in parallel
Task("Memory Agent", "Store findings", "qdrant_memory_agent");
Task("Pattern Agent", "Analyze patterns", "qdrant_pattern_agent");
Task("Decision Agent", "Track decisions", "qdrant_decision_agent");
```

### Spawn via MCP Tools

```typescript
// Claude-flow
const agent = await mcp__claude_flow__agent_spawn({
  type: "qdrant_query_agent",
  name: "Query-Agent-001",
  capabilities: ["semantic_search", "multi_collection_query"]
});

// Ruv-swarm
const agent2 = await mcp__ruv_swarm__agent_spawn({
  type: "qdrant_memory_agent",
  capabilities: ["finding_storage", "experience_retrieval"]
});
```

### List Registered Agents

```bash
# All agents
npx claude-flow@alpha memory list --namespace claude-flow-agents

# Specific agent details
npx claude-flow@alpha memory query "agent-qdrant_query_agent" --namespace claude-flow-agents

# Agent status dashboard
bash scripts/agent-status.sh
```

---

## Troubleshooting Quick Fixes

### Hive-mind not initialized
```bash
npx claude-flow@alpha hive-mind init
```

### Agent not found after registration
```bash
# Re-register
bash scripts/register-agents.sh

# Check memory
npx claude-flow@alpha memory list --namespace claude-flow-agents
```

### Memory namespace not found
```bash
# Initialize namespace
npx claude-flow@alpha memory store "init" '{"initialized":true}' --namespace claude-flow-agents
```

### Duplicate agent name
```yaml
# Rename in YAML config
agents:
  custom_researcher:  # Add prefix
    type: "custom_analyst"
```

---

## Directory Structure After Setup

```
agent-registration/
├── package.json
├── tsconfig.json
├── src/
│   ├── types.ts
│   ├── agent-parser.ts
│   ├── registration-engine.ts
│   ├── mcp-adapter.ts
│   └── index.ts
├── scripts/
│   ├── register-agents.sh
│   ├── verify-agents.sh
│   └── agent-status.sh
├── tests/
│   └── agent-registration.test.ts
└── logs/
    └── agent-registration.log
```

---

## Success Criteria

✅ **Registration Complete When**:
- [ ] Hive-mind initialized
- [ ] All custom agents discovered (12+)
- [ ] All agents registered in claude-flow memory
- [ ] All agents registered in ruv-swarm memory
- [ ] Custom agents appear in agent list
- [ ] Custom agents are spawnable via Task tool
- [ ] Custom agents are spawnable via MCP tools
- [ ] Registration persists after system restart

---

## Next Steps After Registration

1. **Test Agent Execution**
   - Spawn each custom agent
   - Verify task execution
   - Check agent coordination

2. **Monitor Agent Activity**
   - Check agent metrics
   - Review execution logs
   - Track performance

3. **Optimize Agent Configuration**
   - Adjust resource limits
   - Tune capabilities
   - Update hooks

4. **Automate Registration**
   - Set up file watchers
   - Create git hooks
   - Add to CI/CD

---

**Quick Start Status**: ✅ READY FOR IMPLEMENTATION
**Estimated Setup Time**: 3-4 hours
**Prerequisites**: Node.js, npm, npx, claude-flow@alpha
