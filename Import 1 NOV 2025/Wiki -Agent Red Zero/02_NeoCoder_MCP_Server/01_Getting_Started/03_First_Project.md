---
title: Your First NeoCoder Project
category: 01_Getting_Started
last_updated: 2025-10-25
line_count: 444
status: published
tags: [neocoder, mcp, documentation]
---

# Your First NeoCoder Project

This guide walks you through setting up and using NeoCoder for the first time, demonstrating core capabilities and workflow patterns.

## Prerequisites

Before starting, ensure you have:
- ✅ NeoCoder installed (see [Installation Guide](01_Installation.md))
- ✅ Neo4j running and accessible at `bolt://localhost:7687`
- ✅ Qdrant running at `localhost:6333` (for hybrid reasoning features)
- ✅ Claude Desktop configured with the NeoCoder MCP server

## Verifying Your Installation

First, verify that NeoCoder can connect to Neo4j:

```python
# In Claude Desktop, use:
check_connection()
```

Expected response:
```
✅ Connected to Neo4j at bolt://localhost:7687
Database: neo4j
Neo4j version: 5.x.x
```

## Understanding the Guidance Hub

NeoCoder uses a **Guidance Hub** system to help you navigate its capabilities. Start by accessing the main hub:

```python
get_guidance_hub()
```

This returns comprehensive information about:
- Available incarnations and their purposes
- Core workflow templates
- Tool categories and capabilities
- Getting started recommendations

**TIP**: The guidance hub is your primary reference - consult it whenever you're unsure about next steps.

## Choosing Your First Incarnation

NeoCoder offers specialized "incarnations" for different use cases. For your first project, we recommend starting with one of these:

### Option 1: Knowledge Graph Incarnation (Recommended for Beginners)
**Purpose**: Build and explore knowledge networks

```python
switch_incarnation(incarnation_type="knowledge_graph")
get_guidance_hub()  # See knowledge graph specific guidance
```

### Option 2: Code Analysis Incarnation
**Purpose**: Analyze code structure using AST/ASG

```python
switch_incarnation(incarnation_type="code_analysis")
get_guidance_hub()  # See code analysis specific guidance
```

### Option 3: Base Coding Incarnation
**Purpose**: Standard software development workflows

```python
switch_incarnation(incarnation_type="coding")
get_guidance_hub()  # See coding workflow guidance
```

## Project 1: Building a Simple Knowledge Graph

Let's create a small knowledge graph to understand NeoCoder's core concepts.

### Step 1: Switch to Knowledge Graph Incarnation

```python
switch_incarnation(incarnation_type="knowledge_graph")
```

### Step 2: Create Your First Entities

```python
create_entities(entities=[
    {
        "name": "Python",
        "entityType": "ProgrammingLanguage",
        "observations": [
            "High-level, interpreted language",
            "Created by Guido van Rossum in 1991",
            "Emphasizes code readability"
        ]
    },
    {
        "name": "Neo4j",
        "entityType": "Database",
        "observations": [
            "Graph database management system",
            "Uses Cypher query language",
            "Optimized for connected data"
        ]
    },
    {
        "name": "NeoCoder",
        "entityType": "Framework",
        "observations": [
            "MCP server for AI-assisted development",
            "Integrates Neo4j with Claude AI",
            "Supports multiple specialized incarnations"
        ]
    }
])
```

Expected response confirms creation of all entities with timestamps.

### Step 3: Create Relationships Between Entities

```python
create_relations(relations=[
    {
        "from": "NeoCoder",
        "to": "Neo4j",
        "relationType": "USES"
    },
    {
        "from": "NeoCoder",
        "to": "Python",
        "relationType": "IMPLEMENTED_IN"
    }
])
```

### Step 4: View Your Knowledge Graph

```python
read_graph()
```

This displays the complete graph structure including:
- All entities and their observations
- All relationships between entities
- Timestamps for tracking

### Step 5: Search Your Knowledge Graph

```python
search_nodes(query="graph database")
```

This performs a full-text search across entity names, types, and observations.

### Step 6: Get Detailed Entity Information

```python
open_nodes(names=["Neo4j", "NeoCoder"])
```

This returns detailed information including:
- All observations for each entity
- Incoming relationships
- Outgoing relationships
- Related entities

## Project 2: Using a Workflow Template

NeoCoder provides pre-built workflow templates for common tasks. Let's use the FIX template to understand structured workflows.

### Step 1: List Available Templates

```python
list_action_templates()
```

You'll see templates including:
- `FIX` - Bug fixing workflow
- `REFACTOR` - Code improvement workflow
- `FEATURE` - New feature development
- `DEPLOY` - Deployment procedures
- `CODE_ANALYZE` - Code structure analysis
- `TOOL_ADD` - Adding new tools to NeoCoder

### Step 2: Get Template Details

```python
get_action_template(keyword="FIX")
```

This returns the complete step-by-step workflow for fixing bugs, including:
1. Context identification
2. Issue reproduction
3. Root cause analysis
4. Implementation
5. Testing requirements
6. Documentation updates

### Step 3: Follow the Template Steps

The template provides structured guidance. Key points:
- **ALL testing steps are mandatory** before logging completion
- Each step builds on previous steps
- Verification checkpoints ensure quality

### Step 4: Log Workflow Completion

After successfully completing a workflow (tests passed):

```python
log_workflow_execution(
    project_id="my-first-project",
    action_keyword="FIX",
    summary="Fixed connection timeout in database module",
    files_changed=["src/database.py", "tests/test_database.py"],
    notes="Increased timeout from 5s to 30s based on production metrics"
)
```

This creates an audit trail in Neo4j linking:
- The workflow template used
- Files modified
- Project affected
- Timestamp and details

## Project 3: Exploring Code Analysis

Switch to the code analysis incarnation to analyze code structure.

### Step 1: Switch Incarnation

```python
switch_incarnation(incarnation_type="code_analysis")
```

### Step 2: Analyze a Python File

```python
analyze_file(
    file_path="/path/to/your/file.py",
    analysis_type="both",  # Both AST and ASG analysis
    include_metrics=True
)
```

This parses the file and stores:
- Abstract Syntax Tree (AST) structure
- Abstract Semantic Graph (ASG) relationships
- Complexity metrics
- Code structure hierarchy

### Step 3: Explore Code Structure

```python
explore_code_structure(
    target="/path/to/your/file.py",
    view_type="hierarchy",
    include_metrics=True
)
```

### Step 4: Find Code Quality Issues

```python
find_code_smells(
    target="/path/to/your/file.py",
    threshold="medium"
)
```

This identifies potential issues like:
- High complexity functions
- Duplicated code patterns
- Unused variables
- Long parameter lists

## Understanding NeoCoder Concepts

### Incarnations
**Incarnations** are specialized modes that adapt NeoCoder for specific use cases:
- Same Neo4j core, different tools and workflows
- Easy switching between incarnations
- Each has specialized Neo4j schema
- Tools automatically registered when switching

### Workflow Templates
**Templates** are standardized procedures stored in Neo4j:
- Step-by-step instructions
- Mandatory verification checkpoints
- Automatic tracking and audit trails
- Version controlled and updatable

### The Graph Structure
NeoCoder stores everything in Neo4j:
- `:AiGuidanceHub` - Navigation hubs for different areas
- `:ActionTemplate` - Workflow templates
- `:WorkflowExecution` - Completed work audit trail
- Incarnation-specific nodes (`:Entity`, `:CodeFile`, etc.)

### Tools and MCP Integration
NeoCoder is an MCP (Model Context Protocol) server:
- All functionality exposed as tools to Claude
- Tools automatically registered based on active incarnation
- Direct Neo4j access through Cypher queries
- Qdrant integration for semantic search

## Common Patterns

### Pattern 1: Consult Hub → Use Template → Log Execution

```python
# 1. Get guidance
get_guidance_hub()

# 2. Get template
get_action_template(keyword="FEATURE")

# 3. Follow template steps...
# ... implementation work ...

# 4. Log completion
log_workflow_execution(...)
```

### Pattern 2: Switch Incarnation → Explore Tools → Execute

```python
# 1. Switch context
switch_incarnation(incarnation_type="research")

# 2. See what's available
get_guidance_hub()

# 3. Use specialized tools
register_hypothesis(...)
create_experiment(...)
```

### Pattern 3: Build Knowledge → Query → Refine

```python
# 1. Add information
create_entities(...)
create_relations(...)

# 2. Query and explore
search_nodes(query="...")
read_graph()

# 3. Add observations
add_observations(...)
```

## Querying Neo4j Directly

For advanced users, you can run custom Cypher queries:

```python
# Read-only query
run_custom_query(cypher="""
    MATCH (e:Entity)-[r]->(related:Entity)
    WHERE e.entityType = 'Framework'
    RETURN e.name, type(r), related.name
    LIMIT 10
""")

# Write query (use with caution)
write_neo4j_cypher(cypher="""
    MATCH (e:Entity {name: 'NeoCoder'})
    SET e.lastUpdated = datetime()
    RETURN e
""")
```

## Next Steps

Now that you understand the basics:

1. **Explore More Incarnations**: Try research, decision, or data_analysis incarnations
2. **Build Complex Knowledge Graphs**: Create multi-entity networks with rich relationships
3. **Customize Templates**: Modify workflow templates for your team's needs
4. **Integrate with Qdrant**: Use hybrid reasoning capabilities for semantic search
5. **Create Custom Tools**: Extend NeoCoder with your own specialized tools

## Common Issues and Solutions

### Issue: "Can't connect to Neo4j"
**Solution**: Verify Neo4j is running and credentials are correct in your environment variables.

```bash
# Check Neo4j status
neo4j status

# Verify connection details
echo $NEO4J_URL
echo $NEO4J_USERNAME
```

### Issue: "Incarnation tools not available"
**Solution**: Ensure you've switched to the incarnation first:

```python
switch_incarnation(incarnation_type="knowledge_graph")
# Now knowledge graph tools are available
```

### Issue: "Template not found"
**Solution**: Verify the template keyword is correct and current:

```python
list_action_templates()  # See all available templates
```

### Issue: "Transaction out of scope errors"
**Solution**: These are typically handled internally. If operations complete successfully, you can ignore these messages.

## Resources

- [Core Concepts](../02_Core_Concepts/01_Architecture.md) - Understand NeoCoder's architecture
- [Incarnations Overview](../03_Incarnations/01_Overview.md) - Deep dive into incarnation system
- [Workflow Templates](../04_Workflows/01_Template_Overview.md) - Complete template documentation
- [Tools Reference](../05_Tools_Reference/01_Core_Tools.md) - Comprehensive tool documentation

## Summary

You've learned how to:
- ✅ Verify NeoCoder installation
- ✅ Access the guidance hub system
- ✅ Switch between incarnations
- ✅ Create and query knowledge graphs
- ✅ Use workflow templates
- ✅ Analyze code with AST/ASG tools
- ✅ Query Neo4j directly
- ✅ Troubleshoot common issues

**Next recommended reading**: [Architecture Overview](../02_Core_Concepts/01_Architecture.md) to understand how NeoCoder's components work together.

---

*See Also*:
- Repository: [NeoCoder GitHub](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow)
- Documentation: [docs/README.md](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/tree/main/docs)
- System Directory: [docs/system_directory.md](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/blob/main/docs/system_directory.md)
