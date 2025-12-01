# Architectural Decision Records (ADRs)
**System:** Claude Flow Swarm Initialization
**Version:** 2.0.0
**Date:** 2025-11-12

## ADR-001: Memory-Based Coordination Over Message Passing

**Status:** ACCEPTED
**Date:** 2025-11-12
**Decision Makers:** System Architect

### Context
Agents need to coordinate across asynchronous execution without direct communication channels. Traditional message-passing systems require complex infrastructure and state management.

### Decision
Use SQLite-backed shared memory store as the primary coordination mechanism for all inter-agent communication and state management.

### Rationale

**Advantages:**
1. **Persistence:** Survives across sessions for long-running tasks
2. **Simplicity:** Key-value API accessible to all agents without complex protocols
3. **Namespacing:** Logical separation of concerns without interference
4. **Eventual Consistency:** Sufficient for agent coordination use cases
5. **TTL Support:** Automatic cleanup prevents unbounded growth
6. **No Network Overhead:** Local SQLite database eliminates latency
7. **Transaction Support:** ACID guarantees for critical operations

**Technical Implementation:**
- Storage: `.swarm/memory.db` (SQLite)
- API: `store()`, `retrieve()`, `list()`, `delete()`, `search()`
- Namespaces: `research/`, `architecture/`, `implementation/`, `swarm/`, `session/`
- Consistency: Eventual (last-write-wins)

### Consequences

**Positive:**
- Simple API reduces cognitive overhead
- Cross-session persistence enables long-running workflows
- No external dependencies required
- Easy debugging via SQL queries

**Negative:**
- Eventual consistency only (no strong guarantees)
- Potential race conditions on concurrent writes
- Storage growth requires management

**Risks:**
- **Race Conditions:** Mitigated by using atomic operations and last-write-wins
- **Storage Growth:** Mitigated by TTL support and periodic cleanup
- **Corruption:** Mitigated by WAL mode and regular backups

### Alternatives Considered

**Redis Pub/Sub:**
- Rejected: External dependency, unnecessary complexity for local coordination
- Would require Redis installation and management
- Network overhead even for local communication

**File-Based Coordination:**
- Rejected: Race conditions, no transaction support
- Lock file complexity
- Poor performance for frequent updates

**Direct Agent Messaging:**
- Rejected: Complex routing, state management overhead
- Requires message queue infrastructure
- Difficult to debug and monitor

---

## ADR-002: Hook-Based Event System for Agent Lifecycle

**Status:** ACCEPTED
**Date:** 2025-11-12
**Decision Makers:** System Architect

### Context
Need standardized agent lifecycle management and automation triggers without coupling agents to infrastructure code.

### Decision
Implement a hook system with six lifecycle hooks: pre-task, post-edit, post-task, session-restore, session-end, notify.

### Rationale

**Lifecycle Coverage:**
1. **pre-task:** Resource preparation before agent starts
2. **post-edit:** Automated actions after file modifications
3. **post-task:** Cleanup and metrics after agent completes
4. **session-restore:** Context restoration at session start
5. **session-end:** State persistence at session completion
6. **notify:** Inter-agent communication and broadcasting

**Automation Opportunities:**
- Auto-format code after edits
- Train neural patterns from successful operations
- Collect performance metrics automatically
- Persist session state without manual intervention

### Consequences

**Positive:**
- Consistent agent behavior across all types
- Clear lifecycle boundaries for debugging
- Extensible for future automation needs
- Decouples infrastructure from agent logic

**Negative:**
- Hook execution overhead (typically 50-200ms)
- Potential hook failures require error handling
- Complexity in hook ordering and dependencies

**Risks:**
- **Hook Execution Delays:** Mitigated by async execution where possible
- **Error Propagation:** Mitigated by fail-safe defaults and logging
- **Hook Dependencies:** Mitigated by clear documentation

### Implementation Details

**CLI Interface:**
```bash
npx claude-flow@alpha hooks <hook-name> --<params>
```

**Hook Guarantees:**
- Best-effort execution (failures logged but don't block agents)
- Idempotent operations (safe to retry)
- Timeout protection (max 30s per hook)

---

## ADR-003: Single-Message Parallel Agent Spawning

**Status:** ACCEPTED (CRITICAL)
**Date:** 2025-11-12
**Decision Makers:** System Architect

### Context
Sequential agent spawning creates 10-20x performance bottlenecks. Users were spawning agents one-at-a-time in separate messages, causing massive delays.

### Decision
MANDATORY: All agents MUST be spawned in a single message using Claude Code's Task tool with parallel execution.

### Rationale

**Performance Impact:**
- Sequential spawning: ~5-10s per agent × 6 agents = 30-60s
- Parallel spawning: ~5-10s total for all agents = **10-20x improvement**
- Reduced coordination overhead
- Better resource utilization

**Implementation Pattern:**
```javascript
[Single Message - All Agents]:
  Task("Agent 1", "instructions", "type")
  Task("Agent 2", "instructions", "type")
  Task("Agent 3", "instructions", "type")
  // ... all agents in parallel

  TodoWrite({ todos: [...all todos...] })
```

### Consequences

**Positive:**
- Massive 10-20x speed improvement
- Simpler coordination (all agents start together)
- Better resource utilization
- Natural dependency management

**Negative:**
- All agents must be planned upfront
- Harder to add agents dynamically mid-execution
- Requires careful resource planning

**Risks:**
- **Resource Contention:** Mitigated by max agent limits per topology
- **Planning Overhead:** Mitigated by auto-topology selection
- **Mid-Execution Changes:** Mitigated by coordination layer hooks

### Enforcement

**Critical Rule in CLAUDE.md:**
```markdown
MANDATORY PATTERNS:
- TodoWrite: ALWAYS batch ALL todos in ONE call
- Task tool: ALWAYS spawn ALL agents in ONE message
- File operations: ALWAYS batch ALL reads/writes in ONE message
```

**Validation:** Code reviews check for sequential spawning anti-pattern

---

## ADR-004: MCP for Coordination, Claude Code Task for Execution

**Status:** ACCEPTED
**Date:** 2025-11-12
**Decision Makers:** System Architect

### Context
Clear separation needed between orchestration (what to do) and execution (doing it).

### Decision
MCP tools handle topology and coordination setup; Claude Code Task tool handles actual agent execution and work.

### Rationale

**Tool Strengths:**
- **MCP Tools:** Designed for high-level orchestration, topology management
- **Claude Code Task:** Optimized for parallel execution, actual work

**Responsibility Separation:**
```
MCP Layer (Coordination):
  - swarm_init: Initialize topology
  - agent_spawn: Define agent types
  - task_orchestrate: High-level planning
  - swarm_status: Health monitoring

Claude Code Task Layer (Execution):
  - Task(): Spawn agents with full instructions
  - Parallel execution of actual work
  - File operations (Read, Write, Edit)
  - Code generation and implementation
```

### Consequences

**Positive:**
- Clear separation of concerns
- Optimal tool usage for each purpose
- Better performance through specialization
- Easier to understand and debug

**Negative:**
- Two systems to understand and coordinate
- Potential confusion about which tool to use
- Documentation overhead

**Risks:**
- **Tool Misuse:** Mitigated by clear documentation and examples
- **Coordination Gaps:** Mitigated by memory-based state sharing

### Pattern

```javascript
// Step 1: MCP Coordination (optional for complex tasks)
mcp__claude-flow__swarm_init({ topology: "mesh" })
mcp__claude-flow__agent_spawn({ type: "researcher" })

// Step 2: Claude Code Execution (REQUIRED)
Task("Researcher", "DO ACTUAL RESEARCH", "researcher")
Task("Coder", "WRITE ACTUAL CODE", "coder")
```

---

## ADR-005: Auto-Topology Selection Based on Complexity

**Status:** ACCEPTED
**Date:** 2025-11-12
**Decision Makers:** System Architect

### Context
Manual topology selection creates cognitive overhead and risk of mismatch between task needs and topology capabilities.

### Decision
Implement automatic topology selection based on task complexity scoring with manual override capability.

### Rationale

**Complexity-Topology Mapping:**
```javascript
complexity < 0.3 → star (simple, 3 agents)
0.3 ≤ complexity < 0.7 → hierarchical (moderate, 8 agents)
complexity ≥ 0.7 → mesh (complex, 15 agents)
sequential_workflow → ring (pipeline, 10 agents)
```

**Complexity Factors:**
- File count (single vs multi vs cross-project)
- Dependency depth
- Agent type diversity
- Estimated execution time

### Consequences

**Positive:**
- Better defaults reduce errors
- Faster initialization (no manual decision)
- Codifies best practices
- Allows overrides when needed

**Negative:**
- May not match user intent in edge cases
- Complexity scoring logic needs tuning
- Can surprise users with unexpected topology

**Risks:**
- **Incorrect Assessment:** Mitigated by allowing manual overrides
- **Suboptimal Topology:** Mitigated by monitoring and learning from metrics

### Algorithm

```python
def select_topology(task):
    score = 0

    # File-based factors
    if task.files == 1: score += 0.1
    elif task.files <= 5: score += 0.4
    else: score += 0.8

    # Dependency factors
    score += task.dependency_depth * 0.2

    # Agent diversity
    score += len(task.agent_types) * 0.1

    # Special cases
    if task.is_sequential: return 'ring'
    if score < 0.3: return 'star'
    if score >= 0.7: return 'mesh'
    return 'hierarchical'
```

---

## ADR-006: Iron Law - Do Actual Work, Not Framework Building

**Status:** ACCEPTED (CRITICAL)
**Date:** 2025-11-12
**Decision Makers:** System Architect

### Context
Recurring anti-pattern: agents building tools/frameworks instead of executing actual requested tasks (development theater).

### Decision
MANDATORY instruction in every agent spawn: "DO THE ACTUAL WORK - do not build frameworks, pipelines, or tools to do the work."

### Rationale

**Problem Examples:**
- Asked to "process 39 documents" → builds document processing framework
- Asked to "import data" → creates data import pipeline
- Asked to "analyze files" → builds analysis tooling

**Correct Behavior:**
- Asked to "process 39 documents" → PROCESSES THE 39 DOCUMENTS
- Asked to "import data" → IMPORTS THE ACTUAL DATA
- Asked to "analyze files" → ANALYZES THE ACTUAL FILES

### Consequences

**Positive:**
- Real deliverables produced
- No wasted effort on unnecessary tooling
- Clear expectations for agents
- Faster task completion

**Negative:**
- May discourage legitimate tooling in rare cases
- Requires careful instruction wording
- Enforcement through code review

**Risks:**
- **Overly Restrictive:** Mitigated by allowing exceptions when explicitly needed
- **Ambiguous Cases:** Mitigated by clear examples and guidelines

### Enforcement

**Required in EVERY Task() spawn:**
```javascript
Task(
  "Agent Name",
  "EXECUTE the actual task requested. DO NOT build frameworks or tools. DO THE ACTUAL WORK. Report COMPLETE only when real deliverable exists.",
  "agent-type"
)
```

**Validation:** Before marking COMPLETE, verify actual deliverables exist (not just tools/frameworks)

---

## ADR-007: File Organization - No Root Folder Saves

**Status:** ACCEPTED
**Date:** 2025-11-12
**Decision Makers:** System Architect

### Context
Root folder clutter from unorganized file creation degrades project professionalism and navigation.

### Decision
NEVER save working files to project root; use structured directories: `/src`, `/tests`, `/docs`, `/config`, `/scripts`, `/examples`.

### Rationale

**Professional Structure:**
```
project/
├── src/          # Source code
├── tests/        # Test files
├── docs/         # Documentation
├── config/       # Configuration
├── scripts/      # Utility scripts
└── examples/     # Example code
```

**Benefits:**
- Clean, navigable structure
- Follows industry standards
- Easier onboarding
- Better IDE support

### Consequences

**Positive:**
- Professional project appearance
- Easy navigation and file discovery
- Clear file purpose by location
- Improved maintainability

**Negative:**
- Requires directory planning
- Potential confusion about placement
- Need for directory creation

**Risks:**
- **Inconsistent Usage:** Mitigated by automated checks and templates
- **Wrong Directory Choice:** Mitigated by clear guidelines

### Guidelines

**File Type → Directory Mapping:**
- `*.js`, `*.ts`, `*.py` (source) → `/src`
- `*.test.js`, `*.spec.ts` (tests) → `/tests`
- `*.md`, `*.pdf` (docs) → `/docs`
- `*.json`, `*.yaml`, `*.toml` (config) → `/config`
- `*.sh`, utility scripts → `/scripts`
- Example/demo code → `/examples`

---

## ADR-008: Tool Usage Rules - Read() for Files Only

**Status:** ACCEPTED
**Date:** 2025-11-12
**Decision Makers:** System Architect

### Context
EISDIR errors from using Read() on directories cause agent failures and confusion.

### Decision
Use Read() ONLY for specific files; use Bash()/Glob() for directory exploration and file discovery.

### Rationale

**Tool Responsibilities:**
- **Read():** Read content of specific file paths
- **Bash():** Execute shell commands including `ls`, `find`
- **Glob():** Pattern-based file discovery

**Error Prevention:**
```javascript
// ❌ WRONG: Causes EISDIR error
Read("/path/to/directory/")

// ✅ CORRECT: Discover files, then read
Glob("**/*.js")  // Find files
Read("/path/to/specific.js")  // Read specific file
```

### Consequences

**Positive:**
- No EISDIR errors
- Correct tool usage
- Better performance (Glob optimized for discovery)
- Clearer intent in code

**Negative:**
- Requires two-step process (discover then read)
- Potential for confusion initially
- More tool selection decisions

**Risks:**
- **Developers Forgetting Rule:** Mitigated by error messages and documentation
- **Discovery Overhead:** Mitigated by efficient Glob implementation

### Enforcement

**Agent Instructions Must Include:**
```
TOOL USAGE RULES:
- Use Read() ONLY for specific files, NEVER for directories
- Use Bash() or Glob() to explore directories and find files
- NEVER use Read(/path/to/directory/) - this causes EISDIR errors
```

**Error Handling:** Detect EISDIR errors and suggest correct tool usage

---

## Summary of Architectural Principles

1. **Parallel-First:** Default to concurrent execution
2. **Memory-Based Coordination:** Shared state over messaging
3. **Event-Driven Automation:** Hooks for lifecycle management
4. **Execution Over Frameworks:** Do actual work, not build tools
5. **Clear Separation:** MCP coordinates, Claude Code executes
6. **Auto-Optimization:** Intelligent defaults with override capability
7. **File Organization:** Structured directories, no root clutter
8. **Tool Responsibility:** Right tool for each operation type

---

**Document Version:** 2.0.0
**Last Updated:** 2025-11-12
**Status:** APPROVED FOR IMPLEMENTATION
