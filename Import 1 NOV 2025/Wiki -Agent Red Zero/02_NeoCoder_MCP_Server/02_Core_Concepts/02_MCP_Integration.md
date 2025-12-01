---
title: MCP Integration in NeoCoder
category: 02_Core_Concepts
last_updated: 2025-10-25
line_count: 413
status: published
tags: [neocoder, mcp, documentation]
---

# MCP Integration in NeoCoder

[← Back to Core Concepts](../INDEX.md#core-concepts) | [Next: Graph Structure →](03_Graph_Structure.md)

## Overview

NeoCoder implements the Model Context Protocol (MCP) as an official MCP server, enabling AI assistants to interact with Neo4j knowledge graphs and Qdrant vector databases through a standardized interface. This integration provides both graph-based structured reasoning and vector-based semantic search capabilities.

## MCP Server Architecture

### Server Implementation

NeoCoder runs as an MCP server that:
- **Exposes Tools**: Provides 100+ specialized tools across 7 incarnations
- **Manages State**: Maintains Neo4j and Qdrant connections
- **Handles Routing**: Routes requests to appropriate incarnation handlers
- **Provides Resources**: Offers guidance hubs and documentation access
- **Tracks Context**: Maintains workflow execution history

### Connection Configuration

**Standard MCP Configuration** (in Claude Desktop):
```json
{
  "mcpServers": {
    "neocoder": {
      "command": "python",
      "args": ["-m", "neocoder_mcp"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "your-password",
        "QDRANT_URL": "http://localhost:6333",
        "QDRANT_API_KEY": "optional-api-key"
      }
    }
  }
}
```

**Environment Variables**:
- `NEO4J_URI`: Neo4j database connection string
- `NEO4J_USER`: Database username
- `NEO4J_PASSWORD`: Database password
- `QDRANT_URL`: Qdrant vector database URL
- `QDRANT_API_KEY`: Optional Qdrant API key
- `NEOCODER_INCARNATION`: Default incarnation to load (optional)

## Incarnation System

### What Are Incarnations?

Incarnations are specialized operational modes that configure NeoCoder for specific task types. Each incarnation:
- **Registers specific tools** relevant to its purpose
- **Defines Neo4j schema** for its data types
- **Provides guidance hubs** for AI navigation
- **Offers templates** for common workflows

### Available Incarnations

1. **coding** - Software development and codebase management
2. **knowledge_graph** - Knowledge base construction and querying
3. **code_analysis** - AST/ASG-based code structure analysis
4. **research** - Research synthesis and citation tracking
5. **decision_support** - Multi-criteria decision analysis
6. **data_analysis** - Data pipeline and analysis workflows
7. **complex_system** - System modeling and simulation

See [Incarnations Overview](../03_Incarnations/01_Overview.md) for detailed information.

### Selecting an Incarnation

**At Server Start**:
```bash
export NEOCODER_INCARNATION=coding
python -m neocoder_mcp
```

**Through MCP Tool**:
```python
# Use the switch_incarnation tool
await switch_incarnation(incarnation_type="code_analysis")
```

**In AI Assistant**:
```
Please switch to the research incarnation for citation tracking
```

## Tool Registration System

### How Tools Are Registered

Each incarnation registers its tools during initialization:

```python
class CodingIncarnation(BaseIncarnation):
    incarnation_type = IncarnationType.CODING
    description = "Software development and codebase management"
    version = "1.0.0"

    async def initialize_tools(self):
        """Register coding-specific tools."""
        self.tools = [
            create_project_tool,
            add_file_to_project_tool,
            create_action_template_tool,
            execute_workflow_tool,
            # ... more tools
        ]
```

### Tool Discovery

AI assistants can discover available tools through:

1. **MCP Protocol** - Tools automatically appear in AI assistant's tool list
2. **list_available_tools** - Query currently registered tools
3. **Guidance Hubs** - Navigate tool documentation in Neo4j

### Tool Categories

**Project Management Tools**:
- `create_project` - Initialize new project in Neo4j
- `get_project_structure` - Retrieve project file tree
- `update_project_metadata` - Modify project properties

**File Operations Tools**:
- `add_file_to_project` - Register files in graph
- `add_directory_to_project` - Register directory structures
- `get_file_content` - Retrieve file content with metadata

**Workflow Tools**:
- `create_action_template` - Define reusable workflows
- `execute_workflow` - Run template-based workflows
- `get_workflow_history` - Query execution audit trail

**Knowledge Graph Tools**:
- `create_knowledge_entity` - Add semantic entities
- `create_relationship` - Connect entities
- `query_knowledge_graph` - Execute Cypher queries

**Vector Search Tools**:
- `add_to_vector_store` - Index embeddings in Qdrant
- `semantic_search` - Find similar content
- `hybrid_search` - Combine graph and vector search

See [Tools Reference](../05_Tools_Reference/01_Core_Tools.md) for complete tool documentation.

## Resource System

### Guidance Hubs

NeoCoder provides **guidance hubs** as MCP resources that AI assistants can access for contextual help:

```python
# Access guidance hub resource
hub_content = await read_resource("guidance://main_hub")
```

**Hub Types**:
- `main_hub` - Root navigation hub
- `incarnation_guide` - Incarnation-specific guidance
- `incarnation_cypher_guide` - Cypher pattern library
- `workflow_guide` - Template usage instructions

**Hub Structure**:
```
AiGuidanceHub
├── :LINKS_TO → ChildHub
├── :PROVIDES_GUIDANCE_ON → Concept
├── :SUGGESTS_TEMPLATE → ActionTemplate
└── :RECOMMENDS_TOOL → Tool
```

### Dynamic Resource Generation

Resources are generated dynamically from Neo4j:

```python
async def get_guidance_hub_content(hub_name: str) -> str:
    """Generate guidance hub content from graph."""
    query = """
    MATCH (hub:AiGuidanceHub {name: $hub_name})
    OPTIONAL MATCH (hub)-[:LINKS_TO]->(child:AiGuidanceHub)
    OPTIONAL MATCH (hub)-[:SUGGESTS_TEMPLATE]->(template:ActionTemplate)
    RETURN hub, collect(DISTINCT child) as children,
           collect(DISTINCT template) as templates
    """
    # ... format results as markdown
```

## Request Flow

### Tool Execution Flow

1. **AI Assistant** sends MCP tool request
2. **MCP Server** validates request and routes to incarnation
3. **Incarnation Handler** executes business logic
4. **Neo4j/Qdrant** data operations performed
5. **Response** formatted and returned to assistant
6. **Audit Trail** recorded in WorkflowExecution node

```
┌─────────────┐
│ AI Assistant│
└──────┬──────┘
       │ MCP Tool Request
       ▼
┌─────────────────┐
│  NeoCoder MCP   │
│     Server      │
└──────┬──────────┘
       │ Route to Incarnation
       ▼
┌─────────────────┐
│   Incarnation   │
│    Handler      │
└──────┬──────────┘
       │
       ├─────────► Neo4j (Graph Operations)
       │
       └─────────► Qdrant (Vector Operations)
```

### Workflow Execution Tracking

All workflow executions are tracked in Neo4j:

```cypher
CREATE (exec:WorkflowExecution {
  id: randomUUID(),
  templateKeyword: 'CODE_ANALYZE',
  status: 'completed',
  startTime: datetime(),
  endTime: datetime(),
  parameters: $params,
  results: $results
})

MATCH (template:ActionTemplate {keyword: 'CODE_ANALYZE'})
MERGE (exec)-[:USED_TEMPLATE]->(template)
```

This creates an audit trail of all AI assistant actions.

## Hybrid Reasoning Integration

### Graph + Vector Coordination

NeoCoder's MCP integration enables **hybrid reasoning**:

**Graph Database (Neo4j)**:
- Structured facts and relationships
- Workflow templates and execution history
- Project structure and metadata
- Citations and provenance

**Vector Database (Qdrant)**:
- Semantic search across documents
- Content similarity matching
- Contextual embeddings
- Cross-reference discovery

### Context-Augmented Reasoning

The hybrid approach enables **context-augmented reasoning** that goes beyond traditional RAG:

1. **Vector Search** finds semantically similar content
2. **Graph Traversal** discovers structured relationships
3. **F-Contraction** synthesizes knowledge from both sources
4. **Citation Tracking** maintains provenance through graph
5. **Workflow History** provides execution context

Example flow:
```
User Query: "How does authentication work in this system?"

1. Qdrant Search → Find similar authentication-related content
2. Neo4j Query → Get structured auth flow from graph
3. Graph Traversal → Find related security policies
4. Synthesis → Combine vector + graph results
5. Response → Answer with citations from both sources
```

## Advanced Integration Patterns

### Multi-Database Transactions

```python
async def hybrid_knowledge_update(
    entity_data: dict,
    embedding: list[float]
):
    """Update both Neo4j and Qdrant atomically."""
    async with neo4j_session() as session:
        # Create graph entity
        result = await session.run("""
            CREATE (e:KnowledgeEntity $props)
            RETURN e.id as entity_id
        """, props=entity_data)
        entity_id = result.single()["entity_id"]

    # Index in Qdrant with graph ID
    await qdrant_client.upsert(
        collection_name="knowledge",
        points=[{
            "id": entity_id,
            "vector": embedding,
            "payload": entity_data
        }]
    )
```

### Incarnation Switching

```python
async def switch_incarnation(incarnation_type: str):
    """Dynamically switch operational mode."""
    # Unregister current tools
    await current_incarnation.cleanup()

    # Load new incarnation
    new_incarnation = get_incarnation(incarnation_type)
    await new_incarnation.initialize_schema()
    await new_incarnation.initialize_tools()

    # Update MCP server state
    mcp_server.incarnation = new_incarnation
    mcp_server.refresh_tools()
```

### Custom Tool Registration

```python
from neocoder_mcp import register_custom_tool

@register_custom_tool(
    name="analyze_security",
    description="Perform security analysis on code",
    incarnation="coding"
)
async def analyze_security_tool(
    file_path: str,
    severity_threshold: str = "medium"
) -> dict:
    """Custom security analysis tool."""
    # Tool implementation
    return analysis_results
```

## Best Practices

### Tool Selection

**Use the Right Incarnation**:
- Code development → `coding` incarnation
- Research synthesis → `research` incarnation
- Code structure analysis → `code_analysis` incarnation
- Knowledge base building → `knowledge_graph` incarnation

**Leverage Guidance Hubs**:
```
"Please check the incarnation_cypher_guide for query patterns"
"What does the main_hub suggest for this task?"
```

### Error Handling

**MCP Tool Errors**:
- Tools return structured error responses
- Check `success` field in results
- Use `error` field for debugging
- Review WorkflowExecution nodes for audit trail

**Connection Issues**:
- Verify Neo4j/Qdrant are running
- Check environment variables
- Review MCP server logs
- Test database connections directly

### Performance Optimization

**Batch Operations**:
```python
# Good: Batch file additions
await add_files_batch(
    project_id="proj-123",
    file_paths=["src/file1.py", "src/file2.py", "src/file3.py"]
)

# Avoid: Sequential single additions
for file_path in file_paths:
    await add_file_to_project(project_id, file_path)
```

**Query Optimization**:
- Use guidance hub Cypher patterns
- Leverage indexes and constraints
- Limit result set sizes
- Use parameters in queries

## Related Documentation

- [Architecture Overview](01_Architecture.md) - System design and components
- [Graph Structure](03_Graph_Structure.md) - Neo4j schema details
- [Guidance Hub System](04_Guidance_Hub.md) - AI navigation system
- [Incarnations](../03_Incarnations/01_Overview.md) - Detailed incarnation guide
- [Tools Reference](../05_Tools_Reference/01_Core_Tools.md) - Complete tool documentation

---
*Last Updated: 2025-10-24 | [Report Issues](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues)*
