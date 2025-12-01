---
title: NeoCoder Architecture (Part 1)
category: 02_Core_Concepts
last_updated: 2025-10-25
line_count: 485
status: published
tags: [neocoder, mcp, documentation]
---

# NeoCoder Architecture

NeoCoder implements a revolutionary hybrid AI reasoning system that combines Neo4j knowledge graphs, Qdrant vector databases, and MCP orchestration to create a Context-Augmented Reasoning platform for knowledge management, research analysis, and standardized workflows.

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Desktop (AI)                      │
│                 Model Context Protocol (MCP)                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  NeoCoder MCP Server                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Incarnation Registry & Tool Manager          │   │
│  │  - Dynamic incarnation loading                       │   │
│  │  - Tool registration and routing                     │   │
│  │  - Schema initialization coordination                │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│     ┌───────────────────┼───────────────────┐                │
│     ▼                   ▼                   ▼                │
│  ┌──────┐          ┌──────┐           ┌──────────┐          │
│  │Base  │          │Code  │           │Knowledge │          │
│  │      │    ...   │Anal  │    ...    │Graph     │   ...    │
│  │Incar │          │Incar │           │Incar     │          │
│  └──────┘          └──────┘           └──────────┘          │
└────────┬────────────────────┬──────────────────────┬─────────┘
         │                    │                      │
         ▼                    ▼                      ▼
┌─────────────────┐  ┌────────────────┐  ┌──────────────────┐
│     Neo4j       │  │    Qdrant      │  │  External Tools  │
│ Graph Database  │  │Vector Database │  │  (AST, etc.)     │
│  - Structured   │  │  - Semantic    │  │  - Code parsing  │
│    facts        │  │    search      │  │  - Analysis      │
│  - Workflows    │  │  - Embeddings  │  │  - Processing    │
│  - Audit trail  │  │  - Context     │  │                  │
└─────────────────┘  └────────────────┘  └──────────────────┘
```

## Core Components

### 1. MCP Server Layer

**File**: `src/mcp_neocoder/server.py` (90,452 bytes - main server implementation)

The MCP server is the primary interface between Claude AI and the NeoCoder system:

**Key Responsibilities**:
- Handles MCP protocol communication with Claude Desktop
- Manages tool registration and routing
- Coordinates incarnation switching
- Maintains database connections (Neo4j and Qdrant)
- Implements process lifecycle management
- Handles signal processing (SIGTERM/SIGINT)
- Manages resource cleanup and garbage collection

**Process Management Features** (implemented in v1.0.0+):
- Proper signal handlers for graceful shutdown
- Resource tracking (processes, connections, background tasks)
- Zombie cleanup and orphaned instance detection
- Memory management and leak prevention
- Background task safety

**Tools Available**:
```python
# Core system tools
check_connection()
get_guidance_hub()
list_incarnations()
switch_incarnation()
get_current_incarnation()
suggest_tool()

# Workflow tools
get_action_template()
list_action_templates()
log_workflow_execution()
get_workflow_history()

# Cypher tools
run_custom_query()
write_neo4j_cypher()
list_cypher_snippets()
search_cypher_snippets()
```

### 2. Incarnation System

**File**: `src/mcp_neocoder/incarnation_registry.py` (18,780 bytes)

The incarnation system enables NeoCoder to adapt for different use cases while maintaining a common graph core.

**Architecture Principles**:
- **Graph-Native Stack**: Same Neo4j core, different manifestations
- **Orthogonal Tiers**: Facts, workflows, and execution engines are decoupled
- **Dynamic Loading**: Incarnations discovered automatically from `incarnations/` directory
- **Schema Independence**: Each incarnation can define its own Neo4j schema
- **Tool Isolation**: Tools automatically registered per incarnation

**Incarnation Types** (defined in `polymorphic_adapter.py`):
```python
class IncarnationType(str, Enum):
    CODING = "coding"                    # Base workflow management
    CODE_ANALYSIS = "code_analysis"      # AST/ASG code analysis
    KNOWLEDGE_GRAPH = "knowledge_graph"  # Hybrid reasoning system
    RESEARCH = "research_orchestration"  # Scientific research platform
    DECISION = "decision_support"        # Decision analysis
    DATA_ANALYSIS = "data_analysis"      # Data analytics
    LEARNING = "continuous_learning"     # Educational environment
    SIMULATION = "complex_system"        # System modeling
```

**Common Schema Motifs** (shared across incarnations):

| Element | Purpose | Labels/Relationships |
|---------|---------|---------------------|
| **Actor** | Human/agent/tool identity | `(:Agent)-[:PLAYS_ROLE]->(:Role)` |
| **Intent** | Hypothesis, decision, scenario | `(:Intent {type})` |
| **Evidence** | Documentation, metrics, observations | `(:Evidence)-[:SUPPORTS]->(:Intent)` |
| **Outcome** | Results, states, payoffs | `(:Outcome)-[:RESULT_OF]->(:Intent)` |

### 3. Neo4j Graph Database

**Primary Data Store**: Structured facts, relationships, and workflows

**Core Node Types**:
```cypher
// System navigation and guidance
(:AiGuidanceHub {id, description, createdAt, lastUpdated})

// Workflow templates
(:ActionTemplate {
    keyword,      // e.g., "FIX", "REFACTOR"
    version,      // Template version
    isCurrent,    // Boolean flag
    description,
    steps,        // Multi-line workflow instructions
    complexity,   // "LOW", "MEDIUM", "HIGH"
    estimatedEffort  // Minutes
})

// Execution audit trail
(:WorkflowExecution {
    id,
    timestamp,
    keywordUsed,
    description,
    status,
    testResults,
    executionTime
})

// Project structure
(:Project {projectId, name, readmeContent})
(:File {path, project_id})
(:Directory {path, project_id})
```

**Key Relationships**:
```cypher
// Navigation
(:AiGuidanceHub)-[:LINKS_TO]->(:Guide)

// Workflows
(:WorkflowExecution)-[:USED_TEMPLATE]->(:ActionTemplate)
(:WorkflowExecution)-[:APPLIED_TO_PROJECT]->(:Project)
(:WorkflowExecution)-[:MODIFIED]->(:File)

// Structure
(:Project)-[:CONTAINS]->(:Directory)
(:Directory)-[:CONTAINS]->(:File|:Directory)
```

**Constraints and Indexes**:
```cypher
// Uniqueness constraints
CREATE CONSTRAINT unique_action_template_current IF NOT EXISTS
FOR (t:ActionTemplate)
REQUIRE (t.keyword, t.isCurrent) IS UNIQUE;

CREATE CONSTRAINT unique_project_id IF NOT EXISTS
FOR (p:Project)
REQUIRE p.projectId IS UNIQUE;

// Performance indexes
CREATE INDEX action_template_keyword IF NOT EXISTS
FOR (t:ActionTemplate) ON (t.keyword);

CREATE INDEX file_path IF NOT EXISTS
FOR (f:File) ON (f.path);
```

### 4. Qdrant Vector Database

**Purpose**: Semantic search and contextual understanding

**Integration Points**:
- **Document Chunking**: Text split for vector storage
- **Embedding Generation**: Semantic representations
- **Similarity Search**: Context retrieval
- **Cross-Reference**: Links to Neo4j graph entities

**Typical Use**:
```python
# Document ingestion (handled by NeoCoder)
# 1. Parse document
# 2. Generate embeddings
# 3. Store in Qdrant collection
# 4. Link to Neo4j entities via metadata

# Semantic search
qdrant_client.search(
    collection_name="documents",
    query_vector=embedding,
    limit=10
)
```

**Collections Structure**:
- Documents collection: `neocoder_documents`
- Research papers collection: `research_papers`
- Code snippets collection: `code_analysis`
- Custom collections per incarnation

### 5. Hybrid Reasoning Engine

**Revolutionary Feature**: Context-Augmented Reasoning beyond traditional RAG

**Three-Step Process**:

#### Step 1: Smart Query Router
```python
# AI analyzes query intent
query_type = classify_intent(user_query)
# Returns: "graph-centric", "vector-centric", or "hybrid"

# Examples:
# "Who works with whom?" → graph-centric
# "What are opinions on X?" → vector-centric
# "What did [person] say about [topic]?" → hybrid
```

#### Step 2: Parallel Data Retrieval
```python
# Graph query
neo4j_results = run_cypher_query(...)

# Vector search
qdrant_results = semantic_search(...)

# For hybrid: use graph results to refine vector search
```

#### Step 3: Cross-Database Synthesis
```python
# Intelligent synthesis
# - Neo4j facts as authoritative
# - Qdrant for nuance and opinion
# - Full citation tracking
# - Conflict detection

synthesized_answer = merge_sources(
    neo4j_results,
    qdrant_results,
    prioritize="structured"  # or "semantic"
)
```

### 6. Action Template System

**File**: `src/mcp_neocoder/action_templates.py` (30,789 bytes)

Workflow templates stored in Neo4j provide standardized procedures:

**Available Templates**:
- `FIX`: Bug fixing with mandatory testing
- `REFACTOR`: Code improvement while maintaining functionality
- `DEPLOY`: Production deployment with safety checks
- `FEATURE`: New feature development
- `TOOL_ADD`: Adding new tools to NeoCoder
- `CODE_ANALYZE`: Structured code analysis with AST/ASG
- `KNOWLEDGE_QUERY`: Hybrid knowledge query workflow
- `KNOWLEDGE_EXTRACT`: Document extraction with F-Contraction

**Template Structure**:
```python
{
    "keyword": "FIX",
    "version": "1.2",
    "isCurrent": True,
    "description": "Fix reported bugs with verification",
    "steps": """
1. **Identify Context:**
   - Issue description
   - Expected vs actual behavior

2. **Reproduce Issue:**
   - Create test case
   - Verify reproduction

3. **Root Cause Analysis:**
   - Analyze code
   - Identify underlying cause

4. **Implement Fix:**
   - Minimal change principle
   - Maintain compatibility

5. **Testing (MANDATORY):**
   - All tests must pass
   - Add new test for this issue

6. **Documentation:**
   - Update comments
   - Update README if needed
""",
    "complexity": "MEDIUM",
    "estimatedEffort": 60  # minutes
}
```

### 7. Lotka-Volterra Ecosystem Integration

**Experimental Feature**: Ecological framework for knowledge graph dynamics

**Files**:
- `lv_ecosystem.py` (27,755 bytes)
- `lv_integration.py` (28,596 bytes)
- `lv_neo4j_storage.py` (24,982 bytes)
- `lv_templates.py` (44,143 bytes)

**Purpose**: Model knowledge entity interactions using ecological equations

**Key Concepts**:
- **Species**: Knowledge entity types
- **Population**: Entity counts
- **Interactions**: Prey/predator relationships between entity types
- **Dynamics**: How knowledge populations evolve

**Integration with WolframAlpha**:
- Mathematical modeling
- Differential equation solving
- Visualization generation
- Parameter optimization

## Data Flow Patterns

### Pattern 1: Standard Workflow Execution

```
User Request
    ↓
Claude AI
    ↓
MCP Protocol
    ↓
NeoCoder Server
    ↓
Get Template from Neo4j
    ↓
Execute Steps
    ↓
Verify/Test
    ↓
Log Execution to Neo4j
    ↓
Return Results via MCP
    ↓
Claude AI Response
```

### Pattern 2: Hybrid Knowledge Query

```
User Query
    ↓
Smart Query Router (AI classifies intent)
    ↓
    ├─→ Neo4j Cypher Query (structured facts)
    └─→ Qdrant Vector Search (semantic context)
    ↓
Cross-Database Synthesizer
    ├─ Priority: Neo4j facts
    ├─ Enhancement: Qdrant context
    ├─ Citation tracking
    └─ Conflict detection
    ↓
Synthesized Answer with Sources
```

### Pattern 3: Knowledge Extraction (F-Contraction)

```
Document Input
    ↓
Parse & Chunk
    ↓
    ├─→ Neo4j: Extract entities, relationships
    └─→ Qdrant: Store semantic chunks
    ↓
F-Contraction Merging
    ├─ Detect similar entities (LLM-powered)
    ├─ Merge duplicates
    └─ Preserve source attribution
    ↓
Cross-Reference Mapping
    ├─ Link Neo4j entities to Qdrant chunks
    └─ Bidirectional navigation
```

## Security and Resource Management

### Connection Management

**Neo4j Driver** (`process_manager.py`):
```python
# Connection pooling
driver = AsyncGraphDatabase.driver(
    uri,
    auth=(username, password),
    max_connection_lifetime=3600,
    max_connection_pool_size=50,
    connection_acquisition_timeout=60
)

# Automatic cleanup
async def cleanup():
    await driver.close()
```

### Process Management

**Signal Handlers**:
```python
def setup_signal_handlers():
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

async def handle_shutdown(signum, frame):
    # Clean up resources
    # Close database connections
    # Cancel background tasks
    # Exit gracefully
```

**Resource Tracking**:
- Active processes monitored
- Connection pools managed
- Background tasks tracked
- Zombie process cleanup

### Environment Variables

```bash
# Required
NEO4J_URL="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="your_password"
NEO4J_DATABASE="neo4j"

# Optional
QDRANT_URL="http://localhost:6333"
DEFAULT_INCARNATION="coding"
LOG_LEVEL="INFO"
```

## Performance Optimizations

### Caching Strategies

1. **Template Caching**: Action templates cached after first retrieval
2. **Schema Caching**: Neo4j schema information cached
3. **Tool Registry**: Tool definitions cached per incarnation
4. **Connection Pooling**: Reuse database connections

### Query Optimization

1. **Parameterized Queries**: Prevent query recompilation
2. **Index Usage**: Leverage Neo4j indexes
3. **Batch Operations**: Group operations when possible
4. **Async Execution**: Non-blocking operations
