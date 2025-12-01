---
title: Incarnations Overview
category: 03_Incarnations
last_updated: 2025-10-25
line_count: 483
status: published
tags: [neocoder, mcp, documentation]
---

# Incarnations Overview

[← Back to Guidance Hub](../02_Core_Concepts/04_Guidance_Hub.md) | [Next: Coding Incarnation →](02_Coding.md)

## What Are Incarnations?

Incarnations are **specialized operational modes** that configure NeoCoder for specific task domains. Each incarnation provides:

- **Domain-Specific Tools** - Curated toolset for particular workflows
- **Custom Schema** - Neo4j graph structure for domain data
- **Guidance Hubs** - Contextual documentation and best practices
- **Action Templates** - Reusable workflow patterns
- **Tool Integration** - Coordinated tool usage patterns

Think of incarnations as **expert personalities** - each one knows how to handle its domain effectively, with the right tools, knowledge structures, and workflows.

## Available Incarnations

### 1. Coding Incarnation
**Purpose**: Software development and codebase management

**Use Cases**:
- Project structure management
- File and directory tracking
- Development workflow execution
- Build and deployment processes
- Code modification tracking

**Key Tools**:
- `create_project` - Initialize software projects
- `add_file_to_project` - Register source files
- `execute_workflow` - Run development workflows
- `get_project_structure` - Query project tree

**Schema**:
- Project, File, Directory nodes
- HAS_FILE, CONTAINS relationships
- WorkflowExecution tracking

[Learn More →](02_Coding.md)

### 2. Knowledge Graph Incarnation
**Purpose**: Knowledge base construction and semantic querying

**Use Cases**:
- Building knowledge repositories
- Entity and relationship mapping
- Semantic knowledge queries
- Knowledge graph visualization
- Domain modeling

**Key Tools**:
- `create_knowledge_entity` - Add semantic entities
- `create_relationship` - Connect entities
- `query_knowledge_graph` - Execute Cypher queries
- `get_entity_neighbors` - Explore relationships

**Schema**:
- KnowledgeEntity, Concept nodes
- RELATES_TO, IS_A, PART_OF relationships
- Domain-specific entity types

[Learn More →](03_Knowledge_Graph.md)

### 3. Code Analysis Incarnation
**Purpose**: AST/ASG-based code structure analysis

**Use Cases**:
- Abstract Syntax Tree analysis
- Abstract Semantic Graph construction
- Dependency analysis
- Code complexity metrics
- Refactoring pattern detection

**Key Tools**:
- `analyze_code_structure` - Parse and analyze code
- `create_code_entity` - Store code constructs
- `find_dependencies` - Map code dependencies
- `calculate_complexity` - Compute metrics

**Schema**:
- CodeEntity, FunctionNode, ClassNode
- DEFINES, CALLS, INHERITS relationships
- AST/ASG structure representation

[Learn More →](04_Code_Analysis.md)

### 4. Research Incarnation
**Purpose**: Research synthesis and citation tracking

**Use Cases**:
- Literature review management
- Citation network analysis
- Research synthesis workflows
- Source attribution
- Knowledge synthesis with F-Contraction

**Key Tools**:
- `add_research_paper` - Register academic papers
- `create_citation` - Track sources
- `synthesize_knowledge` - F-Contraction synthesis
- `find_related_research` - Citation network queries

**Schema**:
- ResearchPaper, Citation, Author nodes
- CITED_BY, AUTHORED_BY relationships
- Citation network structure

[Learn More →](05_Research.md)

### 5. Decision Support Incarnation
**Purpose**: Multi-criteria decision analysis and tracking

**Use Cases**:
- Decision modeling
- Alternative evaluation
- Criteria weighting
- Decision history tracking
- Impact analysis

**Key Tools**:
- `create_decision` - Model decisions
- `add_alternative` - Define options
- `evaluate_criteria` - Score alternatives
- `track_decision_outcome` - Record results

**Schema**:
- Decision, Alternative, Criterion nodes
- HAS_ALTERNATIVE, EVALUATED_BY relationships
- Decision tree structures

[Learn More →](06_Decision_Support.md)

### 6. Data Analysis Incarnation
**Purpose**: Data pipeline and analysis workflow management

**Use Cases**:
- Data pipeline tracking
- Analysis workflow execution
- Dataset versioning
- Transformation tracking
- Quality monitoring

**Key Tools**:
- `register_dataset` - Track data sources
- `create_transformation` - Define data operations
- `execute_analysis` - Run analysis workflows
- `track_data_lineage` - Query data provenance

**Schema**:
- Dataset, Transformation, Analysis nodes
- DERIVES_FROM, PRODUCES relationships
- Data lineage graphs

[Learn More →](07_Data_Analysis.md)

### 7. Complex System Incarnation
**Purpose**: System modeling and simulation

**Use Cases**:
- System dynamics modeling
- Component interaction tracking
- Simulation workflow management
- Emergent behavior analysis
- System optimization

**Key Tools**:
- `create_system_component` - Model system parts
- `define_interaction` - Connect components
- `run_simulation` - Execute system models
- `analyze_behavior` - Study patterns

**Schema**:
- Component, Interaction, State nodes
- INTERACTS_WITH, AFFECTS relationships
- System topology graphs

## Incarnation System Architecture

### Base Incarnation Class

All incarnations extend the `BaseIncarnation` class:

```python
from enum import Enum
from abc import ABC, abstractmethod

class IncarnationType(Enum):
    CODING = "coding"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    CODE_ANALYSIS = "code_analysis"
    RESEARCH = "research"
    DECISION_SUPPORT = "decision_support"
    DATA_ANALYSIS = "data_analysis"
    COMPLEX_SYSTEM = "complex_system"

class BaseIncarnation(ABC):
    """Base class for all incarnations."""

    incarnation_type: IncarnationType
    description: str
    version: str

    @abstractmethod
    async def initialize_schema(self):
        """Initialize Neo4j schema for this incarnation."""
        pass

    @abstractmethod
    async def initialize_tools(self):
        """Register incarnation-specific tools."""
        pass

    @abstractmethod
    async def get_guidance_hubs(self) -> list[str]:
        """Return list of guidance hub names."""
        pass

    async def cleanup(self):
        """Cleanup resources when switching incarnations."""
        pass
```

### Incarnation Lifecycle

**Initialization**:
1. Load incarnation configuration
2. Initialize Neo4j schema (constraints, indexes)
3. Register tools with MCP server
4. Create/update guidance hubs
5. Mark incarnation as active

**Runtime**:
1. Route tool requests to incarnation handlers
2. Execute domain-specific logic
3. Track operations in WorkflowExecution nodes
4. Maintain schema integrity

**Cleanup**:
1. Unregister tools from MCP
2. Save state if needed
3. Release resources
4. Prepare for incarnation switch

### Switching Incarnations

**Via MCP Tool**:
```python
# Use switch_incarnation tool
await switch_incarnation(incarnation_type="code_analysis")
```

**Via Environment Variable**:
```bash
export NEOCODER_INCARNATION=research
python -m neocoder_mcp
```

**Via Configuration**:
```json
{
  "default_incarnation": "coding",
  "auto_switch": true,
  "context_detection": true
}
```

## Multi-Incarnation Workflows

### Sequential Incarnation Usage

```python
# 1. Start with coding incarnation
await switch_incarnation("coding")
await create_project(name="AuthService", root_path="/src/auth")
await add_file_to_project(project_id, "auth/login.py")

# 2. Switch to code_analysis for structure analysis
await switch_incarnation("code_analysis")
await analyze_code_structure(file_path="auth/login.py")

# 3. Switch to knowledge_graph for documentation
await switch_incarnation("knowledge_graph")
await create_knowledge_entity(
    name="Authentication Flow",
    type="process",
    description="JWT-based authentication workflow"
)
```

### Cross-Incarnation Queries

```cypher
-- Query across incarnation schemas
MATCH (project:Project {name: 'AuthService'})
MATCH (project)-[:HAS_FILE]->(file:File)
MATCH (file)-[:DEFINES]->(entity:CodeEntity)
MATCH (concept:KnowledgeEntity {name: 'Authentication'})
MATCH path = (entity)-[*1..3]-(concept)
RETURN project, file, entity, concept, path
```

## Creating Custom Incarnations

### Incarnation Template

```python
from neocoder_mcp.incarnations.base import BaseIncarnation, IncarnationType

class CustomIncarnation(BaseIncarnation):
    """Custom domain incarnation."""

    incarnation_type = IncarnationType.CUSTOM
    description = "Custom domain-specific functionality"
    version = "1.0.0"

    async def initialize_schema(self):
        """Set up Neo4j schema."""
        schema_queries = [
            # Constraints
            """
            CREATE CONSTRAINT unique_custom_entity IF NOT EXISTS
            FOR (e:CustomEntity)
            REQUIRE e.id IS UNIQUE
            """,
            # Indexes
            """
            CREATE INDEX custom_entity_name IF NOT EXISTS
            FOR (e:CustomEntity)
            ON (e.name)
            """
        ]

        async with self.driver.session() as session:
            for query in schema_queries:
                await session.run(query)

    async def initialize_tools(self):
        """Register custom tools."""
        self.tools = [
            self.create_custom_entity_tool,
            self.query_custom_data_tool,
            # ... more tools
        ]

    async def get_guidance_hubs(self) -> list[str]:
        """Return guidance hub names."""
        return [
            'custom_guide',
            'custom_cypher_guide'
        ]

    @tool_decorator(
        name="create_custom_entity",
        description="Create custom domain entity"
    )
    async def create_custom_entity_tool(
        self,
        name: str,
        properties: dict
    ) -> dict:
        """Tool implementation."""
        async with self.driver.session() as session:
            result = await session.run("""
                CREATE (e:CustomEntity {
                  id: randomUUID(),
                  name: $name,
                  created: datetime()
                })
                SET e += $properties
                RETURN e
            """, {'name': name, 'properties': properties})

            return {"success": True, "entity": result.single()['e']}
```

### Registering Custom Incarnations

```python
from neocoder_mcp import register_incarnation

# Register custom incarnation
register_incarnation(CustomIncarnation)

# Start server with custom incarnation
export NEOCODER_INCARNATION=custom
python -m neocoder_mcp
```

## Incarnation Selection Guide

### Task-Based Selection

| Task | Recommended Incarnation | Reason |
|------|------------------------|---------|
| Build software project | coding | Project structure tracking |
| Analyze code dependencies | code_analysis | AST/ASG analysis tools |
| Create knowledge base | knowledge_graph | Entity relationship modeling |
| Literature review | research | Citation tracking |
| Evaluate options | decision_support | Multi-criteria analysis |
| Track data pipeline | data_analysis | Data lineage tracking |
| Model system | complex_system | System dynamics tools |

### Context-Based Auto-Selection

NeoCoder can automatically suggest incarnations based on context:

```python
async def suggest_incarnation(task_description: str) -> str:
    """Suggest appropriate incarnation for task."""
    keywords = {
        'coding': ['project', 'file', 'code', 'build', 'deploy'],
        'code_analysis': ['analyze', 'dependency', 'structure', 'ast'],
        'knowledge_graph': ['knowledge', 'entity', 'relationship', 'domain'],
        'research': ['paper', 'citation', 'research', 'synthesis'],
        'decision_support': ['decision', 'alternative', 'criteria', 'evaluate'],
        'data_analysis': ['data', 'pipeline', 'analysis', 'dataset'],
        'complex_system': ['system', 'simulation', 'component', 'interaction']
    }

    # Score each incarnation
    scores = {}
    for inc, keys in keywords.items():
        score = sum(1 for key in keys if key in task_description.lower())
        scores[inc] = score

    # Return highest scoring incarnation
    return max(scores, key=scores.get)
```

## Best Practices

### Incarnation Usage

**Match Tools to Task**:
- Use the incarnation whose tools best match your workflow
- Don't force tools from wrong incarnation
- Switch incarnations as task phases change

**Leverage Guidance Hubs**:
```python
# Check incarnation guide before starting
guide = await read_resource("guidance://coding_guide")
# Follow suggested workflows from hub
```

**Maintain Schema Consistency**:
- Let incarnation manage its schema
- Don't manually modify incarnation-specific nodes
- Use incarnation tools for data operations

### Performance Optimization

**Minimize Incarnation Switching**:
```python
# Good: Batch operations in one incarnation
await switch_incarnation("coding")
await create_project(...)
await add_files_batch([...])  # Multiple files at once

# Avoid: Excessive switching
await switch_incarnation("coding")
await create_project(...)
await switch_incarnation("code_analysis")  # Unnecessary switch
await switch_incarnation("coding")  # Back and forth
```

**Cache Incarnation State**:
- Current incarnation tools are cached in MCP server
- Guidance hubs are cached after first access
- Schema is initialized once per session

## Related Documentation

- [Architecture Overview](../02_Core_Concepts/01_Architecture.md) - System design
- [MCP Integration](../02_Core_Concepts/02_MCP_Integration.md) - Tool registration
- [Guidance Hub System](../02_Core_Concepts/04_Guidance_Hub.md) - Hub navigation
- [Individual Incarnations](02_Coding.md) - Detailed incarnation guides
- [Creating Tools](../07_Development/01_Creating_Tools.md) - Tool development guide

---
*Last Updated: 2025-10-24 | [Report Issues](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues)*
