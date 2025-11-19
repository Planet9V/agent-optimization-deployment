# Claude Flow Swarm Initialization Architecture
**Version:** 2.0.0
**Date:** 2025-11-12
**Status:** APPROVED

## Executive Summary

This document defines the system architecture for Claude Flow swarm initialization, a high-performance distributed agent coordination system optimized for parallel execution and memory-based coordination. The architecture achieves 10-20x performance improvement through concurrent agent spawning and supports up to 54 specialized agent types across 4 topology patterns.

## System Overview

### Core Design Principles

1. **Parallel-First Execution**: Default to concurrent operations, sequential only when dependencies require
2. **Memory-Based Coordination**: Shared SQLite store for persistent state and cross-agent communication
3. **Event-Driven Automation**: Hook system for lifecycle management and automated optimizations
4. **Execution Over Frameworks**: Agents do actual work, not build tools to do work
5. **Clear Separation of Concerns**: MCP coordinates, Claude Code Task tool executes
6. **Auto-Optimization**: Intelligent defaults with manual override capability

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                   Coordination Layer                         │
│  (MCP Tools: swarm_init, agent_spawn, task_orchestrate)    │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                  Execution Layer                             │
│  (Claude Code Task Tool: Parallel Agent Spawning)          │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                 Agent Layer (54 Agent Types)                │
│  Core Dev | Swarm Coord | GitHub | SPARC | Specialized     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│              Infrastructure Layer                            │
│  Memory Store | Hooks System | Logging | Monitoring        │
└─────────────────────────────────────────────────────────────┘
```

## Topology Architecture

### 1. Mesh Topology
**Use Case:** High coordination requirements, parallel execution
**Max Agents:** 10
**Communication:** O(n²) overhead
**Fault Tolerance:** High (no single point of failure)

```
    Agent1 ←──→ Agent2
      ↕    ╲   ╱    ↕
      ↕     ╲╱     ↕
    Agent3 ←──→ Agent4
```

**Advantages:**
- Full connectivity between all agents
- No single point of failure
- Fast consensus and coordination
- Excellent for parallel algorithms

**Disadvantages:**
- High message overhead (scales O(n²))
- Practical limit ~10 agents
- Complex state management

### 2. Hierarchical Topology
**Use Case:** Task delegation, clear command structure
**Max Agents:** 50
**Communication:** O(log n) overhead
**Fault Tolerance:** Medium (coordinator dependency)

```
         Coordinator
        ╱     │     ╲
    Agent1  Agent2  Agent3
     ╱│╲    ╱│╲    ╱│╲
    W W W  W W W  W W W
```

**Advantages:**
- Scalable to 50+ agents
- Clear responsibility hierarchy
- Efficient message routing
- Natural task delegation pattern

**Disadvantages:**
- Coordinator can become bottleneck
- Single point of failure at coordinator level
- Requires careful load balancing

### 3. Ring Topology
**Use Case:** Sequential workflows, pipeline processing
**Max Agents:** 20
**Communication:** O(n) overhead
**Fault Tolerance:** Low (break in ring disrupts flow)

```
Agent1 → Agent2 → Agent3 → Agent4
  ↑                          │
  └──────────────────────────┘
```

**Advantages:**
- Simple coordination logic
- Ordered execution guaranteed
- Low implementation complexity
- Natural pipeline pattern

**Disadvantages:**
- Sequential bottleneck
- Poor fault tolerance
- Latency accumulation
- Single break disrupts entire ring

### 4. Star Topology
**Use Case:** Centralized coordination, monitoring
**Max Agents:** 30
**Communication:** O(1) overhead
**Fault Tolerance:** Low (hub dependency)

```
      Agent2
        │
Agent1─Hub─Agent3
        │
      Agent4
```

**Advantages:**
- Simple routing logic
- Easy centralized monitoring
- Fast broadcast to all agents
- Low complexity implementation

**Disadvantages:**
- Hub becomes bottleneck
- Single point of failure
- Limited scalability
- Hub resource constraints

## Auto-Topology Selection Algorithm

```javascript
function selectTopology(task) {
  const complexity = analyzeComplexity(task);

  if (task.isSequentialWorkflow) {
    return { topology: 'ring', maxAgents: 10 };
  }

  if (complexity < 0.3 || task.singleFile) {
    return { topology: 'star', maxAgents: 3 };
  }

  if (complexity >= 0.7 || task.crossProject) {
    return { topology: 'mesh', maxAgents: 15 };
  }

  // Default: moderate complexity
  return { topology: 'hierarchical', maxAgents: 8 };
}
```

## Communication Architecture

### Memory-Based Coordination

**Implementation:** SQLite-backed shared memory store
**Location:** `.swarm/memory.db`
**Persistence:** Cross-session with TTL support

**Namespace Structure:**
```
research/          → Research findings and requirements
architecture/      → Architectural decisions and designs
implementation/    → Code and implementation artifacts
swarm/            → Swarm state and agent coordination
  ├─ [agent-id]/state
  ├─ [agent-id]/[task-step]
  └─ dependencies/[task-id]
session/          → Session state and checkpoints
```

**Operations:**
- `store(key, value, namespace, ttl)` - Store data with optional TTL
- `retrieve(key, namespace)` - Retrieve stored data
- `list(namespace)` - List all keys in namespace
- `delete(key, namespace)` - Delete specific key
- `search(pattern, namespace)` - Search for matching keys

### Hook-Based Event System

**Lifecycle Hooks:**

1. **pre-task** - Execute before agent starts work
   ```bash
   npx claude-flow@alpha hooks pre-task --description "task description"
   ```
   Actions: Resource preparation, context loading, validation

2. **post-edit** - Execute after file modifications
   ```bash
   npx claude-flow@alpha hooks post-edit --file "filepath" --memory-key "key"
   ```
   Actions: Auto-format, pattern training, memory update

3. **post-task** - Execute after agent completes
   ```bash
   npx claude-flow@alpha hooks post-task --task-id "task-id"
   ```
   Actions: Result storage, metrics collection, cleanup

4. **session-restore** - Execute at session start
   ```bash
   npx claude-flow@alpha hooks session-restore --session-id "session-id"
   ```
   Actions: Context restoration, state recovery

5. **session-end** - Execute at session completion
   ```bash
   npx claude-flow@alpha hooks session-end --export-metrics true
   ```
   Actions: State persistence, metrics export

6. **notify** - Broadcast message to other agents
   ```bash
   npx claude-flow@alpha hooks notify --message "notification message"
   ```
   Actions: Inter-agent communication, status updates

## Task Orchestration Workflow

### Phase 1: Swarm Initialization (5-10s)

```
┌──────────────────────────────────────────────────┐
│ 1. Analyze task complexity and requirements     │
│    → Output: complexity_score, task_breakdown    │
├──────────────────────────────────────────────────┤
│ 2. Select optimal topology                      │
│    → Input: complexity_score                     │
│    → Logic: auto_topology_selection rules        │
│    → Output: topology_type, max_agents          │
├──────────────────────────────────────────────────┤
│ 3. Initialize swarm coordination                │
│    → MCP: swarm_init(topology, maxAgents)       │
│    → Output: swarm_id                           │
├──────────────────────────────────────────────────┤
│ 4. Define agent types for coordination          │
│    → MCP: agent_spawn(type) for each agent      │
│    → Output: agent_type_definitions             │
└──────────────────────────────────────────────────┘
```

### Phase 2: Parallel Agent Deployment (Instant)

```
┌──────────────────────────────────────────────────┐
│ CRITICAL: ALL AGENTS IN SINGLE MESSAGE          │
├──────────────────────────────────────────────────┤
│ 1. Spawn all agents via Claude Code Task tool   │
│    Task("Agent 1", "instructions", "type")      │
│    Task("Agent 2", "instructions", "type")      │
│    Task("Agent 3", "instructions", "type")      │
│    ... (all agents in parallel)                 │
├──────────────────────────────────────────────────┤
│ 2. Each agent: pre-task hook (parallel)         │
├──────────────────────────────────────────────────┤
│ 3. Each agent: session-restore (parallel)       │
├──────────────────────────────────────────────────┤
│ 4. Batch ALL TodoWrite in single call           │
│    TodoWrite({ todos: [5-10+ todos] })          │
└──────────────────────────────────────────────────┘
```

### Phase 3: Coordinated Execution (Variable)

```
┌──────────────────────────────────────────────────┐
│ Agents execute actual work concurrently:        │
│                                                  │
│ Agent 1: Execute task                           │
│   ├─ Check dependencies via memory              │
│   ├─ Do ACTUAL work (not build frameworks)      │
│   ├─ File ops trigger post-edit hooks           │
│   └─ Store results in memory                    │
│                                                  │
│ Agent 2: Execute task (parallel)                │
│   ├─ Check dependencies via memory              │
│   ├─ Do ACTUAL work                             │
│   ├─ File ops trigger post-edit hooks           │
│   └─ Store results in memory                    │
│                                                  │
│ Coordinator: Monitor via memory                 │
│   ├─ Track completion status                    │
│   ├─ Detect failures                            │
│   └─ Broadcast notifications                    │
└──────────────────────────────────────────────────┘
```

### Phase 4: Completion and Cleanup (5-10s)

```
┌──────────────────────────────────────────────────┐
│ 1. Each agent: post-task hook (parallel)        │
│    → Collect metrics                            │
├──────────────────────────────────────────────────┤
│ 2. Store final results in memory                │
│    → Keys: swarm/final-results, session/summary │
├──────────────────────────────────────────────────┤
│ 3. Session-end hook for persistence             │
│    → Export metrics, state, workflow data       │
├──────────────────────────────────────────────────┤
│ 4. Swarm status report                          │
│    → MCP: swarm_status()                        │
│    → Output: health report, metrics             │
└──────────────────────────────────────────────────┘
```

## Monitoring and Health System

### Health Check Mechanisms

**Agent Health:**
- Method: post-task hook completion tracking
- Indicators: Hook success, memory writes, task status, error count
- Thresholds:
  - Healthy: hooks successful && errors == 0
  - Degraded: hooks successful && errors < 3
  - Unhealthy: hooks failed || errors >= 3

**Swarm Health:**
- Method: `mcp__claude-flow__swarm_status`
- Metrics: Active agents, topology integrity, memory accessibility, completion rate
- Thresholds:
  - Healthy: active_agents > 0 && topology_valid
  - Degraded: active_agents > 0 && topology_degraded
  - Failed: active_agents == 0 || topology_invalid

**Memory Health:**
- Method: memory_usage tool checks
- Checks: Database accessibility, write/read success, storage capacity
- Recovery: Automatic retry with exponential backoff

### Performance Metrics

**Agent Metrics** (via `agent_metrics`):
- Task completion time
- File operations count
- Memory operations count
- Hook execution time
- Error count

**Swarm Metrics** (via `session-end --export-metrics`):
- Total execution time
- Parallel efficiency ratio
- Agent utilization rate
- Memory usage
- Token consumption

**Task Metrics** (via `task_status` and `task_results`):
- Task queue depth
- Task completion rate
- Dependency resolution time
- Average task duration

### Self-Healing Mechanisms

**Agent Restart:**
```
Trigger: agent_failure detected
Action:
  1. Retrieve last checkpoint from memory
  2. Respawn agent with Task() tool
  3. Restore context via session-restore hook
  4. Resume from last successful state
```

**Coordination Recovery:**
```
Trigger: topology_degraded || coordination_timeout
Action:
  1. Rebuild coordination state from memory
  2. Re-establish agent connections
  3. Validate topology integrity
  4. Resume with recovered state
```

**Memory Recovery:**
```
Trigger: memory_operation_failure
Action:
  1. Retry with exponential backoff
  2. Check database integrity
  3. Rebuild from session backup if needed
  4. Alert if corruption detected
```

## Architectural Decision Records

See [ADR Document](./architectural-decisions.md) for complete records:

- ADR-001: Memory-Based Coordination Over Message Passing
- ADR-002: Hook-Based Event System for Agent Lifecycle
- ADR-003: Single-Message Parallel Agent Spawning
- ADR-004: MCP for Coordination, Claude Code Task for Execution
- ADR-005: Auto-Topology Selection Based on Complexity
- ADR-006: Iron Law: Do Actual Work, Not Framework Building
- ADR-007: File Organization: No Root Folder Saves
- ADR-008: Tool Usage Rules: Read() for Files Only

## Performance Characteristics

**Parallel Execution Benefits:**
- 10-20x faster than sequential agent spawning
- 2.8-4.4x overall speed improvement
- 32.3% token reduction through efficiency
- 84.8% SWE-Bench solve rate

**Scalability Limits:**
- Mesh: 10 agents (O(n²) communication)
- Hierarchical: 50 agents (O(log n) communication)
- Ring: 20 agents (O(n) sequential)
- Star: 30 agents (hub capacity limited)

**Resource Usage:**
- Memory: ~100MB per session
- Storage: SQLite database grows with memory operations
- Token consumption: Optimized through batching and hooks

## Integration Patterns

### MCP + Claude Code Pattern

```javascript
// Step 1: MCP Coordination Setup (optional for complex tasks)
[Single Message]:
  mcp__claude-flow__swarm_init({ topology: "mesh", maxAgents: 6 })
  mcp__claude-flow__agent_spawn({ type: "researcher" })
  mcp__claude-flow__agent_spawn({ type: "coder" })

// Step 2: Claude Code Parallel Execution (REQUIRED)
[Single Message]:
  Task("Researcher", "DO ACTUAL RESEARCH - analyze files, not build frameworks", "researcher")
  Task("Coder", "WRITE ACTUAL CODE - implement features, not build tools", "coder")
  Task("Tester", "CREATE ACTUAL TESTS - write and run tests, not build frameworks", "tester")

  TodoWrite({ todos: [...8-10 todos...] })

  Write("src/feature.js")
  Write("tests/feature.test.js")
```

### Dependency Management Pattern

```javascript
// Agent A stores result
memory.store("swarm/agent-a/output", result);

// Agent B waits for dependency
const dependency = memory.retrieve("swarm/agent-a/output");
if (!dependency) {
  // Wait or request via hooks
  hooks.notify("Waiting for agent-a output");
}

// Coordinator monitors
const status = memory.list("swarm/*/output");
```

## Security Considerations

1. **Memory Isolation**: Namespaces prevent cross-contamination
2. **Hook Validation**: Validate hook execution permissions
3. **Agent Authentication**: Verify agent identity in coordination
4. **Data Encryption**: Consider encryption for sensitive memory data
5. **Access Control**: Implement role-based access for memory operations

## Future Enhancements

1. **Neural Network Integration**: ML-based topology optimization
2. **Advanced Consensus**: Implement Raft or Byzantine fault tolerance
3. **Distributed Memory**: Multi-node memory synchronization
4. **Real-time Monitoring**: Live dashboard for swarm health
5. **Cost Optimization**: Token usage prediction and optimization

---

**Document Version:** 2.0.0
**Last Updated:** 2025-11-12
**Status:** APPROVED FOR IMPLEMENTATION
