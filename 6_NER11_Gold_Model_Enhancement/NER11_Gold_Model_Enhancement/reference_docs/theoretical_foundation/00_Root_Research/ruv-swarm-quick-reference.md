# RUV-Swarm Quick Reference Guide

## Fast Setup (< 2 Minutes)

### Installation
```bash
# NPX (recommended)
npx ruv-swarm mcp start --protocol=stdio

# Configure Claude Code
# Add to .claude/mcp.json:
{
  "servers": {
    "ruv-swarm": {
      "command": "npx",
      "args": ["ruv-swarm", "mcp", "start"]
    }
  }
}
```

## Common Usage Patterns

### 1. Quick Research Task
```typescript
// Initialize + spawn + orchestrate in one flow
await mcp__ruv_swarm__swarm_init({
    topology: "mesh",
    maxAgents: 5
});

await mcp__ruv_swarm__agent_spawn({
    type: "researcher",
    capabilities: ["academic_search", "analysis"]
});

await mcp__ruv_swarm__task_orchestrate({
    task: "Research renewable energy trends 2025",
    strategy: "parallel"
});
```

### 2. Development Team
```typescript
// Backend + Frontend + Tester
await mcp__ruv_swarm__swarm_init({
    topology: "hierarchical",
    maxAgents: 10
});

const agents = await Promise.all([
    mcp__ruv_swarm__agent_spawn({ type: "coder", name: "Backend" }),
    mcp__ruv_swarm__agent_spawn({ type: "coder", name: "Frontend" }),
    mcp__ruv_swarm__agent_spawn({ type: "tester", name: "QA" })
]);

await mcp__ruv_swarm__task_orchestrate({
    task: "Build REST API with tests",
    priority: "high",
    maxAgents: 3
});
```

### 3. ML Pipeline
```typescript
// Data analysis + model training + optimization
await mcp__ruv_swarm__swarm_init({
    topology: "star",
    maxAgents: 8
});

await mcp__ruv_swarm__agent_spawn({
    type: "analyst",
    capabilities: ["feature_engineering", "eda"]
});

await mcp__ruv_swarm__neural_train({
    iterations: 50
});

await mcp__ruv_swarm__task_orchestrate({
    task: "Build time-series forecasting model",
    strategy: "adaptive"
});
```

## Quick Decision Matrix

### When to Use Each Topology

| Agents | Topology | Use Case |
|--------|----------|----------|
| 1-8 | Mesh | Small teams, high coordination |
| 8-20 | Star | Medium teams, scalability |
| 20-100+ | Hierarchical | Large distributed systems |

### When to Use Each Agent Type

| Task | Primary Agent | Secondary Agent |
|------|---------------|-----------------|
| Research | Researcher | Analyst |
| Coding | Coder | Reviewer |
| Analysis | Analyst | Researcher |
| Optimization | Optimizer | Coder |
| Management | Coordinator | All types |

### Cognitive Pattern Selection

| Task Type | Pattern Mix |
|-----------|-------------|
| Creative (design, brainstorming) | 40% divergent, 30% convergent, 30% lateral |
| Analytical (data, research) | 40% convergent, 35% divergent, 25% lateral |
| Strategic (planning, architecture) | 33% convergent, 33% divergent, 34% systems |

## Performance Tuning Checklist

### ✅ Before Production

- [ ] Switch from mesh to star/hierarchical (if > 8 agents)
- [ ] Enable SIMD acceleration
- [ ] Configure SQLite/PostgreSQL persistence
- [ ] Set memory limits per agent (256MB recommended)
- [ ] Enable health checks (30s interval)
- [ ] Implement agent pooling for repetitive tasks
- [ ] Use shared memory for local communication
- [ ] Configure WebSocket compression for distributed
- [ ] Set timeouts (30s recommended)
- [ ] Enable monitoring and metrics

### ❌ Common Mistakes to Avoid

- Don't use mesh topology for > 8 agents
- Don't spawn agents without capabilities
- Don't use homogeneous cognitive patterns
- Don't disable SIMD in production
- Don't accumulate unbounded results
- Don't skip timeout configuration
- Don't use in-memory persistence in production
- Don't ignore error logs

## Troubleshooting

### High Memory Usage
```typescript
// Set per-agent limits
await mcp__ruv_swarm__agent_spawn({
    type: "coder",
    memory_limit: "256MB",
    evict_on_limit: true
});

// Check current usage
await mcp__ruv_swarm__memory_usage({
    detail: "by-agent"
});
```

### Slow Task Execution
```typescript
// Check bottlenecks
await mcp__ruv_swarm__benchmark_run({
    type: "swarm",
    iterations: 10
});

// Verify SIMD support
await mcp__ruv_swarm__features_detect({
    category: "simd"
});
```

### Agent Unresponsiveness
```typescript
// Add timeout and retry
await mcp__ruv_swarm__task_orchestrate({
    task: "...",
    timeout: 30_000,
    retry_on_timeout: true,
    max_retries: 3
});
```

## Key Metrics

### Performance Targets
- Agent spawn: < 50ms (20ms optimized)
- Task orchestration: < 200ms
- Memory per agent: < 256MB
- Throughput: 50+ tasks/sec

### Quality Targets
- SWE-Bench solve rate: > 80%
- Task completion rate: > 95%
- Agent uptime: > 99%

## Full Documentation
Comprehensive research: `/home/jim/2_OXOT_Projects_Dev/docs/research/ruv-swarm-capabilities-nov-2025.md`

## Resources
- GitHub: https://github.com/ruvnet/ruv-FANN
- MCP Usage: https://github.com/ruvnet/ruv-FANN/blob/main/ruv-swarm/docs/MCP_USAGE.md
- Crates: https://lib.rs/crates/ruv-swarm-mcp
