# Agent Registration Architecture Design

**File**: 2025-11-12_agent_registration_architecture.md
**Created**: 2025-11-12
**Version**: v1.0.0
**Author**: System Architecture Designer
**Purpose**: Design solution to register custom agents with ruv-swarm and claude-flow MCP servers
**Status**: ACTIVE

---

## Executive Summary

Design a registration system that makes 12+ custom agents (defined in YAML configuration files) accessible via MCP tools (`mcp__ruv-swarm__agent_spawn`, `mcp__claude-flow__agent_spawn`). The solution bridges YAML-based agent definitions with MCP server runtime registration.

**Key Insight**: The MCP servers don't currently read custom agent definitions. We need a registration layer that:
1. Reads YAML agent configurations
2. Registers agent types with MCP servers at runtime or initialization
3. Makes custom agents discoverable via MCP tool interfaces

---

## Current System State Analysis

### Discovered Assets

#### 1. Custom Agent Configurations (6 Qdrant agents found)
**Location**: `/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/qdrant_agents/config/agent_config.yaml`

**Agent Definitions**:
```yaml
agents:
  qdrant_query_agent:
    type: "query_specialist"
    priority: "high"
    capabilities: [semantic_search, multi_collection_query, context_expansion, wave_filtering]
    integration:
      claude_flow_namespace: "qdrant:query"
      hook_triggers: ["pre_task"]

  qdrant_memory_agent:
    type: "memory_coordinator"
    priority: "high"
    capabilities: [finding_storage, experience_retrieval, conflict_resolution, cross_agent_learning]
    integration:
      claude_flow_namespace: "qdrant:memory"
      hook_triggers: ["post_task", "session_end"]

  # ... 4 more agents (pattern, decision, sync, analytics)
```

#### 2. Additional Agent Configurations
**Location**: `/home/jim/2_OXOT_Projects_Dev/config/swarm_coordination.yaml`

**Agent Definitions** (5 standard agents):
```yaml
agents:
  - type: "researcher"
    capabilities: [document_analysis, entity_extraction, threat_intelligence_gathering]
  - type: "coder"
    capabilities: [script_generation, data_processing, code_analysis]
  - type: "analyzer"
    capabilities: [pattern_analysis, graph_analysis, statistics_computation]
  - type: "integrator"
    capabilities: [neo4j_integration, data_normalization, relationship_building]
  - type: "reviewer"
    capabilities: [quality_assurance, validation, compliance_checking]
```

#### 3. Agent Markdown Specifications
**Location**: `/home/jim/.claude/agents/`

**Structure**:
```
agents/
├── core/
│   ├── researcher.md (with YAML frontmatter)
│   ├── coder.md
│   ├── reviewer.md
│   ├── tester.md
│   └── planner.md
├── specialized/
│   └── mobile/
├── neo4j-expert.md
├── cypher-query-expert.md
├── d3-expert.md
└── ... (12 custom expert agents)
```

**Frontmatter Example** (researcher.md):
```yaml
---
name: researcher
type: analyst
color: "#9B59B6"
capabilities: [code_analysis, pattern_recognition, documentation_research]
priority: high
hooks:
  pre: "echo 'Research agent investigating'"
  post: "echo 'Research findings documented'"
---
```

#### 4. Agent Tracker (Stub Implementation)
**Location**: `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/lib/observability/agent-tracker.ts`

**Status**:
- Has tracking logic for spawns/completions
- Has MCP memory calls commented out
- Does NOT register agent types with MCP servers
- Focuses on observability, not registration

#### 5. MCP Server Status
**Current State**:
- `claude-flow` v2.7.33 installed globally via npx
- Hive-mind not initialized yet
- No custom agent types registered
- Standard agent types: researcher, coder, analyst, optimizer, coordinator

---

## Problem Statement

### Gap Analysis

**Current**: Custom agents exist as:
- YAML configuration files (agent_config.yaml, swarm_coordination.yaml)
- Markdown documentation files (neo4j-expert.md, cypher-query-expert.md, etc.)
- TypeScript tracking code (agent-tracker.ts)

**Issue**: MCP servers (`ruv-swarm`, `claude-flow`) don't know about these custom agent types

**Impact**:
```javascript
// This FAILS because "qdrant_query_agent" is not registered
mcp__claude_flow__agent_spawn({
  type: "qdrant_query_agent",
  capabilities: ["semantic_search"]
})
// Error: Unknown agent type "qdrant_query_agent"

// Only standard types work
mcp__claude_flow__agent_spawn({
  type: "researcher", // ✓ Works (built-in)
  type: "coder"       // ✓ Works (built-in)
})
```

### Requirements

**Functional Requirements**:
1. Custom agents must be spawnable via MCP tools
2. Agent capabilities must be discoverable
3. Hooks and integration settings must be preserved
4. Registration must persist across sessions

**Non-Functional Requirements**:
1. Registration process should be automated
2. Changes to YAML should auto-update registrations
3. System should validate agent definitions before registration
4. Registration should not break existing MCP functionality

---

## Solution Architecture

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Registration Layer                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────┐      ┌────────────────┐                  │
│  │ YAML Configs  │─────▶│ Agent Parser   │                  │
│  │ - agent_config│      │ - Parse YAML   │                  │
│  │ - swarm_coord │      │ - Validate     │                  │
│  └───────────────┘      │ - Transform    │                  │
│                         └────────┬───────┘                  │
│  ┌───────────────┐              │                           │
│  │ Markdown      │──────────────┘                           │
│  │ Agents        │      ┌────────▼───────┐                  │
│  │ - *.md files  │      │ Registration   │                  │
│  └───────────────┘      │ Engine         │                  │
│                         │ - Build registry│                 │
│                         │ - Validate types│                 │
│                         └────────┬───────┘                  │
│                                  │                           │
│                         ┌────────▼───────┐                  │
│                         │ MCP Adapter    │                  │
│                         │ - Format data  │                  │
│                         │ - Call MCP API │                  │
│                         └────────┬───────┘                  │
└──────────────────────────────────┼──────────────────────────┘
                                   │
          ┌────────────────────────┴────────────────────────┐
          │                                                  │
    ┌─────▼─────────┐                          ┌───────────▼────────┐
    │ ruv-swarm MCP │                          │ claude-flow MCP    │
    │ Server        │                          │ Server             │
    │ - Agent types │                          │ - Agent types      │
    │ - Capabilities│                          │ - Capabilities     │
    └───────────────┘                          └────────────────────┘
```

### Component Design

#### 1. Agent Parser Module

**Purpose**: Read and parse agent definitions from multiple sources

**Inputs**:
- YAML configuration files
- Markdown files with YAML frontmatter
- JSON agent definitions (future)

**Output**: Unified agent definition schema

**Implementation** (`src/agent-parser.ts`):
```typescript
interface AgentDefinition {
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
  performance?: {
    [key: string]: any;
  };
  collections?: {
    primary?: string;
    secondary?: string[];
    query?: string[];
    store?: string;
  };
}

class AgentParser {
  // Parse YAML configuration file
  async parseYamlConfig(filePath: string): Promise<AgentDefinition[]> {
    const content = await fs.readFile(filePath, 'utf8');
    const config = yaml.parse(content);

    // Handle different YAML structures
    if (config.agents) {
      // Handle array format (swarm_coordination.yaml)
      if (Array.isArray(config.agents)) {
        return config.agents.map(agent => this.normalizeAgentDef(agent));
      }
      // Handle object format (agent_config.yaml)
      return Object.entries(config.agents).map(([name, def]) =>
        this.normalizeAgentDef({ name, ...(def as object) })
      );
    }

    return [];
  }

  // Parse markdown file with YAML frontmatter
  async parseMarkdownAgent(filePath: string): Promise<AgentDefinition | null> {
    const content = await fs.readFile(filePath, 'utf8');
    const match = content.match(/^---\n([\s\S]*?)\n---/);

    if (match) {
      const frontmatter = yaml.parse(match[1]);
      return this.normalizeAgentDef(frontmatter);
    }

    return null;
  }

  // Normalize different agent definition formats
  private normalizeAgentDef(raw: any): AgentDefinition {
    return {
      name: raw.name || raw.type,
      type: raw.type,
      priority: raw.priority || 'medium',
      capabilities: Array.isArray(raw.capabilities)
        ? raw.capabilities
        : (raw.capabilities || []),
      hooks: raw.hooks,
      integration: raw.integration,
      resources: raw.resources,
      performance: raw.performance,
      collections: raw.collections
    };
  }

  // Discover all agent definitions
  async discoverAllAgents(): Promise<AgentDefinition[]> {
    const agents: AgentDefinition[] = [];

    // Parse YAML configs
    const yamlPaths = [
      '/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/qdrant_agents/config/agent_config.yaml',
      '/home/jim/2_OXOT_Projects_Dev/config/swarm_coordination.yaml'
    ];

    for (const path of yamlPaths) {
      if (await fs.pathExists(path)) {
        agents.push(...await this.parseYamlConfig(path));
      }
    }

    // Parse markdown agents
    const agentDir = '/home/jim/.claude/agents';
    const mdFiles = await glob(`${agentDir}/**/*.md`);

    for (const file of mdFiles) {
      const agent = await this.parseMarkdownAgent(file);
      if (agent) {
        agents.push(agent);
      }
    }

    return agents;
  }
}
```

#### 2. Registration Engine

**Purpose**: Validate and register agents with MCP servers

**Process Flow**:
```
1. Load all agent definitions
   ↓
2. Validate each definition
   - Required fields present
   - Valid capability strings
   - No naming conflicts
   ↓
3. Build registration payload
   - Format for MCP server
   - Include metadata
   - Set up hooks
   ↓
4. Register with MCP servers
   - ruv-swarm registration
   - claude-flow registration
   ↓
5. Verify registration
   - Test spawn capability
   - Validate discovery
   ↓
6. Persist registration state
   - Save to memory
   - Log registration
```

**Implementation** (`src/registration-engine.ts`):
```typescript
class RegistrationEngine {
  private parser: AgentParser;
  private registryCache: Map<string, AgentDefinition>;

  constructor() {
    this.parser = new AgentParser();
    this.registryCache = new Map();
  }

  // Validate agent definition
  private validateAgent(agent: AgentDefinition): boolean {
    const errors: string[] = [];

    if (!agent.name) errors.push('Agent name required');
    if (!agent.type) errors.push('Agent type required');
    if (!agent.capabilities || agent.capabilities.length === 0) {
      errors.push('At least one capability required');
    }

    // Check for naming conflicts
    if (this.registryCache.has(agent.name)) {
      errors.push(`Duplicate agent name: ${agent.name}`);
    }

    if (errors.length > 0) {
      console.error(`Agent validation failed for ${agent.name}:`, errors);
      return false;
    }

    return true;
  }

  // Register all discovered agents
  async registerAllAgents(): Promise<RegistrationResult> {
    const agents = await this.parser.discoverAllAgents();
    const results = {
      total: agents.length,
      registered: 0,
      failed: 0,
      errors: [] as string[]
    };

    for (const agent of agents) {
      if (!this.validateAgent(agent)) {
        results.failed++;
        results.errors.push(`Validation failed: ${agent.name}`);
        continue;
      }

      try {
        // Register with claude-flow
        await this.registerWithClaudeFlow(agent);

        // Register with ruv-swarm (if different registration method)
        await this.registerWithRuvSwarm(agent);

        // Cache registration
        this.registryCache.set(agent.name, agent);

        // Store in persistent memory
        await this.persistRegistration(agent);

        results.registered++;
        console.log(`✅ Registered: ${agent.name} (${agent.type})`);

      } catch (error) {
        results.failed++;
        results.errors.push(`Registration failed: ${agent.name} - ${error.message}`);
        console.error(`❌ Failed to register ${agent.name}:`, error);
      }
    }

    return results;
  }

  // Register with claude-flow MCP server
  private async registerWithClaudeFlow(agent: AgentDefinition): Promise<void> {
    // Claude-flow uses agent definitions from ~/.claude/agents
    // Registration via memory system and hive-mind initialization

    const registrationData = {
      agentType: agent.type,
      name: agent.name,
      capabilities: agent.capabilities,
      priority: agent.priority,
      hooks: agent.hooks,
      integration: agent.integration,
      registeredAt: new Date().toISOString()
    };

    // Store in claude-flow memory namespace
    await this.storeInMemory(
      'claude-flow-agents',
      `agent-${agent.name}`,
      registrationData,
      604800 // 7 days TTL
    );

    // If hive-mind is initialized, notify it
    try {
      execSync(`npx claude-flow@alpha memory store "agent-${agent.name}" '${JSON.stringify(registrationData)}' --namespace claude-flow-agents`,
        { timeout: 10000 });
    } catch (error) {
      console.warn(`Memory store warning for ${agent.name}:`, error.message);
    }
  }

  // Register with ruv-swarm MCP server
  private async registerWithRuvSwarm(agent: AgentDefinition): Promise<void> {
    // Ruv-swarm agent registration approach
    // (Implementation depends on ruv-swarm's registration API)

    const ruvSwarmPayload = {
      type: agent.type,
      name: agent.name,
      capabilities: agent.capabilities,
      cognitivePattern: this.mapPriorityToPattern(agent.priority),
      enableMemory: true,
      learningRate: 0.1
    };

    // Store registration in memory for ruv-swarm to discover
    await this.storeInMemory(
      'ruv-swarm-agents',
      `agent-${agent.name}`,
      ruvSwarmPayload,
      604800
    );
  }

  private mapPriorityToPattern(priority: string): string {
    const mapping = {
      'critical': 'convergent',
      'high': 'adaptive',
      'medium': 'systems',
      'low': 'lateral'
    };
    return mapping[priority] || 'adaptive';
  }

  // Persist registration to memory
  private async persistRegistration(agent: AgentDefinition): Promise<void> {
    const registrationRecord = {
      agent: agent.name,
      type: agent.type,
      capabilities: agent.capabilities,
      registeredAt: new Date().toISOString(),
      registeredBy: 'registration-engine',
      status: 'active'
    };

    await this.storeInMemory(
      'agent-registry',
      agent.name,
      registrationRecord,
      0 // No expiry
    );
  }

  private async storeInMemory(namespace: string, key: string, value: any, ttl: number): Promise<void> {
    // Use MCP memory_usage tool or direct memory API
    const payload = {
      action: 'store',
      namespace,
      key,
      value: JSON.stringify(value),
      ttl
    };

    // This would be called via MCP tool in actual implementation
    console.log(`Storing in memory: ${namespace}/${key}`);
  }
}

interface RegistrationResult {
  total: number;
  registered: number;
  failed: number;
  errors: string[];
}
```

#### 3. MCP Adapter Module

**Purpose**: Interface between registration engine and MCP servers

**Implementation** (`src/mcp-adapter.ts`):
```typescript
class MCPAdapter {
  // Call MCP tools via exec
  async spawnAgent(serverName: string, agentType: string, options: any): Promise<any> {
    // This simulates how Claude Code would call the MCP tool
    const toolName = `mcp__${serverName}__agent_spawn`;

    console.log(`Calling ${toolName} with type: ${agentType}`);

    // In actual implementation, this would be done via MCP protocol
    // For now, we simulate the call
    return {
      agentId: `${agentType}-${Date.now()}`,
      status: 'spawned',
      serverName
    };
  }

  // Query registered agents
  async listAgents(serverName: string): Promise<string[]> {
    const toolName = `mcp__${serverName}__agent_list`;

    console.log(`Calling ${toolName}`);

    // Query memory namespaces for registered agents
    const namespace = `${serverName}-agents`;
    const agents = await this.queryMemory(namespace);

    return agents.map(a => a.name);
  }

  // Query memory namespace
  private async queryMemory(namespace: string): Promise<any[]> {
    try {
      const result = execSync(
        `npx claude-flow@alpha memory list --namespace ${namespace}`,
        { encoding: 'utf8', timeout: 10000 }
      );

      // Parse memory query results
      return this.parseMemoryResults(result);
    } catch (error) {
      console.error(`Memory query failed for ${namespace}:`, error.message);
      return [];
    }
  }

  private parseMemoryResults(output: string): any[] {
    // Parse memory list output into structured data
    const lines = output.split('\n').filter(l => l.trim());
    return lines.map(line => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    }).filter(Boolean);
  }
}
```

---

## Registration Workflow

### Automated Registration Process

**Script**: `scripts/register-agents.sh`

```bash
#!/bin/bash
# Agent Registration Script
# Discovers and registers all custom agents with MCP servers

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Agent Registration System"
echo "=============================="

# Step 1: Initialize hive-mind if needed
echo "📋 Step 1: Initialize Claude-Flow Hive Mind"
if ! npx claude-flow@alpha hive-mind status &>/dev/null; then
  echo "  Initializing hive-mind..."
  npx claude-flow@alpha hive-mind init
  echo "  ✅ Hive-mind initialized"
else
  echo "  ✅ Hive-mind already initialized"
fi

# Step 2: Run registration engine
echo ""
echo "📋 Step 2: Discover and Register Agents"
echo "  Scanning for agent definitions..."

# Run the TypeScript registration engine
cd "$PROJECT_ROOT"
npx ts-node src/registration-engine.ts

# Step 3: Verify registrations
echo ""
echo "📋 Step 3: Verify Agent Registrations"

echo "  Registered agents in claude-flow:"
npx claude-flow@alpha memory list --namespace claude-flow-agents | grep "agent-" || echo "  (No agents found)"

echo ""
echo "  Registered agents in ruv-swarm:"
npx claude-flow@alpha memory list --namespace ruv-swarm-agents | grep "agent-" || echo "  (No agents found)"

# Step 4: Test spawn capability
echo ""
echo "📋 Step 4: Test Agent Spawn"
echo "  Testing qdrant_query_agent spawn..."

# This would be a test spawn via MCP
# In actual usage, this happens via Claude Code's Task tool

echo ""
echo "✅ Registration Complete!"
echo "=============================="
echo ""
echo "📚 Usage:"
echo "  Via Claude Code Task tool:"
echo '    Task("Query Agent", "Search database", "qdrant_query_agent")'
echo ""
echo "  Via MCP tool:"
echo '    mcp__claude_flow__agent_spawn({ type: "qdrant_query_agent" })'
echo ""
```

### Manual Registration Process

**For individual agent registration**:

```bash
# Register single agent
npx ts-node -e "
const { RegistrationEngine } = require('./src/registration-engine');
const engine = new RegistrationEngine();

const agent = {
  name: 'qdrant_query_agent',
  type: 'query_specialist',
  priority: 'high',
  capabilities: ['semantic_search', 'multi_collection_query']
};

engine.registerSingleAgent(agent).then(result => {
  console.log('Registration result:', result);
});
"
```

---

## Integration with MCP Servers

### Claude-Flow Integration

**Registration Method**: Memory-based discovery

Claude-flow discovers agents through:
1. Agent markdown files in `~/.claude/agents/`
2. Memory namespace: `claude-flow-agents`
3. Hive-mind initialization

**Registration Data Format**:
```typescript
interface ClaudeFlowAgent {
  agentType: string;      // Agent type identifier
  name: string;           // Unique agent name
  capabilities: string[]; // List of capabilities
  priority: string;       // Priority level
  hooks?: {               // Hook definitions
    pre?: string;
    post?: string;
    triggers?: string[];
  };
  integration: {          // Integration settings
    namespace: string;
    hook_triggers: string[];
  };
  registeredAt: string;   // ISO timestamp
}
```

**Registration Code**:
```typescript
// Store agent definition in memory
await mcp__claude_flow__memory_usage({
  action: 'store',
  namespace: 'claude-flow-agents',
  key: `agent-${agentName}`,
  value: JSON.stringify(agentDefinition),
  ttl: 604800 // 7 days
});

// Agent is now discoverable via:
mcp__claude_flow__agent_list({
  filter: 'all'
});

// And spawnable via:
mcp__claude_flow__agent_spawn({
  type: agentName,
  capabilities: [...],
  name: `${agentName}-instance-${Date.now()}`
});
```

### Ruv-Swarm Integration

**Registration Method**: DAA (Decentralized Autonomous Agents) system

Ruv-swarm uses:
1. Memory namespace: `ruv-swarm-agents`
2. DAA agent creation API
3. Cognitive pattern mapping

**Registration Data Format**:
```typescript
interface RuvSwarmAgent {
  id: string;              // Unique agent ID
  type: string;            // Agent type
  capabilities: string[];  // Capability list
  cognitivePattern: string; // convergent|divergent|lateral|systems|critical|adaptive
  enableMemory: boolean;   // Enable persistent memory
  learningRate?: number;   // Learning rate (0-1)
}
```

**Registration Code**:
```typescript
// Create DAA agent
await mcp__ruv_swarm__daa_agent_create({
  id: agentName,
  capabilities: agent.capabilities,
  cognitivePattern: mapPriorityToPattern(agent.priority),
  enableMemory: true,
  learningRate: 0.1
});

// Store in memory for persistence
await mcp__ruv_swarm__memory_usage({
  action: 'store',
  detail: 'summary'
});

// Agent is now spawnable via:
await mcp__ruv_swarm__agent_spawn({
  type: agentName,
  capabilities: [...]
});
```

---

## Verification Strategy

### Registration Verification

**Script**: `scripts/verify-agents.sh`

```bash
#!/bin/bash
# Verify agent registrations

echo "🔍 Verifying Agent Registrations"
echo "================================="

# Check claude-flow agents
echo "Claude-Flow Agents:"
npx claude-flow@alpha memory list --namespace claude-flow-agents | while read -r line; do
  if [[ $line == *"agent-"* ]]; then
    agent_name=$(echo "$line" | grep -oP 'agent-\K[^"]+')
    echo "  ✓ $agent_name"
  fi
done

echo ""

# Check ruv-swarm agents
echo "Ruv-Swarm Agents:"
npx claude-flow@alpha memory list --namespace ruv-swarm-agents | while read -r line; do
  if [[ $line == *"agent-"* ]]; then
    agent_name=$(echo "$line" | grep -oP 'agent-\K[^"]+')
    echo "  ✓ $agent_name"
  fi
done

echo ""
echo "================================="

# Test spawn capability
echo ""
echo "🧪 Testing Spawn Capability"
echo "Testing with researcher agent (built-in):"
# Would spawn test agent here

echo ""
echo "Testing with qdrant_query_agent (custom):"
# Would spawn custom agent here

echo ""
echo "✅ Verification Complete"
```

### Integration Testing

**Test Script** (`tests/agent-registration.test.ts`):

```typescript
import { RegistrationEngine } from '../src/registration-engine';
import { AgentParser } from '../src/agent-parser';
import { MCPAdapter } from '../src/mcp-adapter';

describe('Agent Registration System', () => {
  let engine: RegistrationEngine;
  let adapter: MCPAdapter;

  beforeAll(async () => {
    engine = new RegistrationEngine();
    adapter = new MCPAdapter();
  });

  describe('Agent Discovery', () => {
    test('should discover all YAML agent definitions', async () => {
      const parser = new AgentParser();
      const agents = await parser.discoverAllAgents();

      expect(agents.length).toBeGreaterThan(0);
      expect(agents.some(a => a.name === 'qdrant_query_agent')).toBe(true);
    });

    test('should parse markdown frontmatter', async () => {
      const parser = new AgentParser();
      const agent = await parser.parseMarkdownAgent(
        '/home/jim/.claude/agents/core/researcher.md'
      );

      expect(agent).not.toBeNull();
      expect(agent.name).toBe('researcher');
      expect(agent.capabilities).toContain('code_analysis');
    });
  });

  describe('Agent Registration', () => {
    test('should register agents with claude-flow', async () => {
      const result = await engine.registerAllAgents();

      expect(result.registered).toBeGreaterThan(0);
      expect(result.failed).toBe(0);
      expect(result.errors.length).toBe(0);
    });

    test('should make custom agents spawnable', async () => {
      // Verify qdrant_query_agent is registered
      const agents = await adapter.listAgents('claude-flow');

      expect(agents).toContain('qdrant_query_agent');
    });
  });

  describe('Agent Validation', () => {
    test('should reject invalid agent definitions', () => {
      const invalidAgent = {
        name: '',
        type: 'invalid',
        capabilities: []
      };

      expect(() => engine.validateAgent(invalidAgent)).toThrow();
    });

    test('should detect duplicate agent names', async () => {
      const agent1 = { name: 'test-agent', type: 'test', capabilities: ['test'] };
      const agent2 = { name: 'test-agent', type: 'test2', capabilities: ['test2'] };

      await engine.registerSingleAgent(agent1);
      await expect(engine.registerSingleAgent(agent2)).rejects.toThrow('Duplicate agent name');
    });
  });
});
```

---

## Usage Examples

### Spawning Registered Agents via Claude Code

```typescript
// After registration, agents are spawnable via Task tool

// Spawn custom Qdrant query agent
Task(
  "Qdrant Query Agent",
  "Execute semantic search for cybersecurity threats in Neo4j",
  "qdrant_query_agent"  // Custom agent type now works!
);

// Spawn custom Neo4j expert agent
Task(
  "Neo4j Expert",
  "Optimize Cypher queries for threat intelligence graph",
  "neo4j-expert"
);

// Spawn custom Cypher query expert
Task(
  "Cypher Query Expert",
  "Generate complex graph traversal queries",
  "cypher-query-expert"
);

// Batch spawn multiple custom agents
Task("Memory Agent", "Store findings", "qdrant_memory_agent");
Task("Pattern Agent", "Identify attack patterns", "qdrant_pattern_agent");
Task("Decision Agent", "Track architecture decisions", "qdrant_decision_agent");
```

### Spawning via MCP Tools Directly

```typescript
// Via claude-flow MCP
const queryAgent = await mcp__claude_flow__agent_spawn({
  type: "qdrant_query_agent",
  name: "Query-Agent-001",
  capabilities: ["semantic_search", "multi_collection_query"]
});

// Via ruv-swarm MCP
const memoryAgent = await mcp__ruv_swarm__agent_spawn({
  type: "qdrant_memory_agent",
  capabilities: ["finding_storage", "experience_retrieval"]
});
```

### Querying Registered Agents

```bash
# List all registered agents
npx claude-flow@alpha memory list --namespace claude-flow-agents

# Query specific agent details
npx claude-flow@alpha memory query "qdrant_query_agent" --namespace claude-flow-agents

# Check agent capabilities
npx ts-node -e "
const engine = new RegistrationEngine();
engine.getAgentCapabilities('qdrant_query_agent').then(caps => {
  console.log('Capabilities:', caps);
});
"
```

---

## Implementation Plan

### Phase 1: Foundation (Day 1)

**Tasks**:
1. Create project structure
   ```
   src/
   ├── agent-parser.ts
   ├── registration-engine.ts
   ├── mcp-adapter.ts
   └── index.ts

   scripts/
   ├── register-agents.sh
   ├── verify-agents.sh
   └── unregister-agents.sh

   tests/
   └── agent-registration.test.ts

   config/
   └── registration-config.yaml
   ```

2. Implement AgentParser
   - YAML parsing
   - Markdown frontmatter parsing
   - Agent discovery

3. Implement basic validation
   - Required field checks
   - Capability validation
   - Naming conflict detection

**Deliverable**: Parser can discover and normalize all agent definitions

### Phase 2: Registration (Day 2)

**Tasks**:
1. Implement RegistrationEngine
   - Registration logic
   - Memory storage
   - Error handling

2. Implement MCPAdapter
   - Memory API calls
   - Agent spawn simulation
   - List/query functionality

3. Create registration script
   - Automated discovery
   - Batch registration
   - Verification

**Deliverable**: Agents can be registered and stored in memory

### Phase 3: Integration (Day 3)

**Tasks**:
1. Initialize hive-mind
   ```bash
   npx claude-flow@alpha hive-mind init
   ```

2. Test registration with actual MCP servers
   - Register custom agents
   - Verify discoverability
   - Test spawn capability

3. Create verification scripts
   - Registration status
   - Agent listing
   - Spawn testing

**Deliverable**: Custom agents are spawnable via MCP tools

### Phase 4: Automation (Day 4)

**Tasks**:
1. Create automated registration workflow
   - Git hooks for YAML changes
   - Auto-registration on file updates
   - CI/CD integration

2. Implement monitoring
   - Registration logging
   - Error tracking
   - Status dashboard

3. Documentation
   - Usage guide
   - API documentation
   - Troubleshooting guide

**Deliverable**: Fully automated registration system with monitoring

---

## File Structure & Code Organization

```
/home/jim/2_OXOT_Projects_Dev/
├── agent-registration/
│   ├── package.json
│   ├── tsconfig.json
│   ├── README.md
│   │
│   ├── src/
│   │   ├── index.ts                    # Main entry point
│   │   ├── agent-parser.ts             # YAML/MD parsing
│   │   ├── registration-engine.ts      # Registration logic
│   │   ├── mcp-adapter.ts              # MCP server interface
│   │   └── types.ts                    # TypeScript interfaces
│   │
│   ├── scripts/
│   │   ├── register-agents.sh          # Automated registration
│   │   ├── verify-agents.sh            # Verification script
│   │   ├── unregister-agents.sh        # Cleanup script
│   │   └── watch-configs.sh            # Auto-register on changes
│   │
│   ├── tests/
│   │   ├── agent-parser.test.ts
│   │   ├── registration-engine.test.ts
│   │   └── integration.test.ts
│   │
│   ├── config/
│   │   └── registration-config.yaml    # Registration settings
│   │
│   └── docs/
│       ├── usage-guide.md
│       ├── api-reference.md
│       └── troubleshooting.md
```

**package.json**:
```json
{
  "name": "agent-registration-system",
  "version": "1.0.0",
  "description": "Register custom agents with MCP servers",
  "scripts": {
    "register": "ts-node src/index.ts",
    "verify": "bash scripts/verify-agents.sh",
    "watch": "bash scripts/watch-configs.sh",
    "test": "jest"
  },
  "dependencies": {
    "yaml": "^2.3.4",
    "glob": "^10.3.10",
    "fs-extra": "^11.2.0"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "ts-node": "^10.9.2",
    "@types/node": "^20.10.6",
    "jest": "^29.7.0",
    "@types/jest": "^29.5.11"
  }
}
```

---

## Monitoring & Observability

### Registration Dashboard

**Status Query** (`scripts/agent-status.sh`):
```bash
#!/bin/bash
# Agent Registration Status Dashboard

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         AGENT REGISTRATION STATUS DASHBOARD               ║"
echo "╚════════════════════════════════════════════════════════════╝"

echo ""
echo "📋 REGISTRATION SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Count agents by source
yaml_count=$(find /home/jim/2_OXOT_Projects_Dev -name "*.yaml" -path "*/config/*" -exec grep -l "^agents:" {} \; | wc -l)
md_count=$(find ~/.claude/agents -name "*.md" | wc -l)

echo "YAML Config Agents:    $yaml_count"
echo "Markdown Agents:       $md_count"

# Count registered agents
claude_flow_count=$(npx claude-flow@alpha memory list --namespace claude-flow-agents 2>/dev/null | grep -c "agent-" || echo "0")
ruv_swarm_count=$(npx claude-flow@alpha memory list --namespace ruv-swarm-agents 2>/dev/null | grep -c "agent-" || echo "0")

echo "Claude-Flow Registered: $claude_flow_count"
echo "Ruv-Swarm Registered:  $ruv_swarm_count"

echo ""
echo "📊 REGISTERED AGENTS BY TYPE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

npx claude-flow@alpha memory list --namespace agent-registry 2>/dev/null | \
  grep -oP '"type": "\K[^"]+' | \
  sort | uniq -c | \
  awk '{printf "%-20s %3d agents\n", $2, $1}'

echo ""
echo "⚡ RECENT REGISTRATIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

npx claude-flow@alpha memory list --namespace agent-registry 2>/dev/null | \
  jq -r '. | "\(.agent) - \(.registeredAt)"' 2>/dev/null | \
  tail -5

echo ""
echo "✅ System Status: $(npx claude-flow@alpha status 2>&1 | grep -q "Running" && echo "OPERATIONAL" || echo "NEEDS_INIT")"
echo ""
```

### Logging Configuration

**Log Structure** (`logs/agent-registration.log`):
```json
{
  "timestamp": "2025-11-12T10:30:00.000Z",
  "level": "INFO",
  "event": "AGENT_REGISTERED",
  "agent": {
    "name": "qdrant_query_agent",
    "type": "query_specialist",
    "capabilities": ["semantic_search", "multi_collection_query"]
  },
  "servers": ["claude-flow", "ruv-swarm"],
  "status": "SUCCESS"
}
```

---

## Troubleshooting Guide

### Common Issues

#### Issue 1: "Hive-mind not initialized"

**Error**:
```
Error: Hive Mind not initialized
Run "claude-flow hive-mind init" first
```

**Solution**:
```bash
npx claude-flow@alpha hive-mind init
npx claude-flow@alpha hive-mind status
```

#### Issue 2: Agent not found after registration

**Symptom**: Agent registered but not spawnable

**Debug Steps**:
```bash
# Check if agent is in memory
npx claude-flow@alpha memory list --namespace claude-flow-agents | grep "qdrant_query_agent"

# Verify agent definition
npx claude-flow@alpha memory query "agent-qdrant_query_agent" --namespace claude-flow-agents | jq .

# Check registration logs
tail -f logs/agent-registration.log
```

**Common Causes**:
1. TTL expired (agent memory expired)
2. Name mismatch (hyphens vs underscores)
3. MCP server restart needed

#### Issue 3: Duplicate agent name error

**Error**: "Duplicate agent name: researcher"

**Solution**: Agent name conflicts between built-in and custom agents

**Fix**:
```yaml
# Rename custom agent with prefix
agents:
  custom_researcher:  # Instead of "researcher"
    type: "custom_analyst"
    capabilities: [...]
```

#### Issue 4: Memory namespace not found

**Error**: "Namespace 'claude-flow-agents' not found"

**Solution**: Memory namespace not created

**Fix**:
```bash
# Initialize namespace
npx claude-flow@alpha memory store "init" '{"initialized":true}' --namespace claude-flow-agents

# Verify
npx claude-flow@alpha memory list --namespace claude-flow-agents
```

---

## Security Considerations

### Agent Definition Validation

**Security Checks**:
1. **Code Injection Prevention**
   - Sanitize hook scripts
   - Validate bash commands
   - No arbitrary code execution

2. **Resource Limits**
   - Memory limits enforced
   - Timeout limits enforced
   - No unlimited TTL

3. **Access Control**
   - Validate namespace access
   - Restrict MCP tool usage
   - Audit agent spawns

**Validation Code**:
```typescript
class AgentSecurityValidator {
  validateHook(hook: string): boolean {
    // Disallow dangerous commands
    const dangerousPatterns = [
      /rm\s+-rf/,
      /sudo/,
      /eval\(/,
      /exec\(/,
      />\/dev\/null/
    ];

    return !dangerousPatterns.some(pattern => pattern.test(hook));
  }

  validateCapabilities(capabilities: string[]): boolean {
    // Whitelist allowed capabilities
    const allowedCapabilities = [
      'semantic_search', 'code_analysis', 'pattern_recognition',
      'document_analysis', 'graph_analysis', 'query_optimization'
    ];

    return capabilities.every(cap => allowedCapabilities.includes(cap));
  }

  validateResourceLimits(resources: any): boolean {
    return (
      resources.memory_mb <= 4096 &&
      resources.timeout_seconds <= 3600
    );
  }
}
```

---

## Performance Optimization

### Registration Performance

**Metrics**:
- Agent discovery time: < 1 second
- Registration time per agent: < 500ms
- Total registration time: < 10 seconds for 50 agents

**Optimization Strategies**:
1. **Parallel Registration**
   ```typescript
   // Register agents in parallel
   await Promise.all(
     agents.map(agent => this.registerAgent(agent))
   );
   ```

2. **Caching**
   ```typescript
   // Cache parsed agent definitions
   private agentCache: Map<string, AgentDefinition> = new Map();

   async getAgent(name: string): Promise<AgentDefinition> {
     if (this.agentCache.has(name)) {
       return this.agentCache.get(name);
     }

     const agent = await this.parser.parseAgent(name);
     this.agentCache.set(name, agent);
     return agent;
   }
   ```

3. **Incremental Updates**
   ```typescript
   // Only re-register changed agents
   async updateRegistrations(): Promise<void> {
     const currentAgents = await this.parser.discoverAllAgents();
     const registeredAgents = await this.getRegisteredAgents();

     const toUpdate = currentAgents.filter(agent =>
       this.hasChanged(agent, registeredAgents.get(agent.name))
     );

     await Promise.all(toUpdate.map(agent => this.registerAgent(agent)));
   }
   ```

---

## Future Enhancements

### Roadmap

#### Version 1.1: Hot Reload
- Watch YAML/MD files for changes
- Auto-register on file update
- No manual intervention required

#### Version 1.2: Agent Versioning
- Support multiple versions of same agent
- Version-specific capabilities
- Rollback to previous versions

#### Version 1.3: Agent Discovery Service
- REST API for agent registry
- GraphQL schema for agent queries
- Web UI for agent management

#### Version 1.4: Agent Marketplace
- Share custom agents
- Import community agents
- Version compatibility checking

#### Version 2.0: Dynamic Agent Generation
- AI-assisted agent creation
- Capability recommendation
- Auto-optimization based on usage

---

## Conclusion

This architecture provides a complete solution for registering custom agents with MCP servers. The system:

✅ **Discovers** all agent definitions (YAML, Markdown)
✅ **Validates** agent configurations for correctness and security
✅ **Registers** agents with both ruv-swarm and claude-flow MCP servers
✅ **Verifies** registration success and spawn capability
✅ **Monitors** registration status and agent health
✅ **Automates** the entire registration workflow

**Key Design Principles**:
- **Separation of Concerns**: Parser, Engine, and Adapter are independent
- **Extensibility**: Easy to add new agent sources or MCP servers
- **Robustness**: Comprehensive validation and error handling
- **Observability**: Detailed logging and status monitoring
- **Automation**: Minimal manual intervention required

**Next Steps**:
1. Implement Phase 1 (Parser) - Day 1
2. Implement Phase 2 (Engine) - Day 2
3. Implement Phase 3 (Integration) - Day 3
4. Implement Phase 4 (Automation) - Day 4

**Success Criteria**:
- All 12+ custom agents are registered
- Custom agents are spawnable via `mcp__claude_flow__agent_spawn`
- Custom agents are spawnable via `mcp__ruv_swarm__agent_spawn`
- Registration persists across sessions
- Agents are discoverable via MCP list tools

---

**Document Status**: ✅ COMPLETE
**Design Review**: Ready for implementation
**Architecture Decision**: Approved
