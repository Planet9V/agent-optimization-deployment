---
title: Core Tools Reference (Part 1 of 2)
category: 05_Tools_Reference
last_updated: 2025-10-25
line_count: 434
status: published
tags: [neocoder, mcp, documentation]
---


# Core Tools Reference

[← Back to Workflows](../04_Workflows/03_Advanced_Templates.md) | [Next: Knowledge Graph Tools →](02_Knowledge_Graph_Tools.md)

## Overview

Core tools are available across all incarnations and provide fundamental capabilities for project management, workflow execution, and system interaction.

## Project Management Tools

### create_project

Creates a new project in Neo4j graph.

**Signature**:
```python
async def create_project(
    name: str,
    root_path: str,
    description: str = "",
    metadata: dict | None = None,
    tags: list[str] | None = None
) -> dict
```

**Parameters**:
- `name` - Project name (unique identifier)
- `root_path` - Filesystem root path
- `description` - Project description (optional)
- `metadata` - Additional properties as key-value pairs (optional)
- `tags` - Categorization tags (optional)

**Returns**:
```json
{
  "success": true,
  "project_id": "uuid-string",
  "project": {...}
}
```

**Example**:
```python
project = await create_project(
    name="AuthService",
    root_path="/src/auth-service",
    description="User authentication microservice",
    metadata={"language": "Python", "framework": "FastAPI"},
    tags=["microservice", "authentication"]
)
```

---

### get_project_structure

Retrieves project structure from graph.

**Signature**:
```python
async def get_project_structure(
    project_id: str,
    include_files: bool = True,
    include_directories: bool = True
) -> dict
```

**Returns**: Project tree with files and directories

---

### update_project_metadata

Updates project properties.

**Signature**:
```python
async def update_project_metadata(
    project_id: str,
    metadata: dict | None = None,
    tags: list[str] | None = None,
    description: str | None = None
) -> dict
```

---

## File Management Tools

### add_file_to_project

Registers a file in project graph.

**Signature**:
```python
async def add_file_to_project(
    project_id: str,
    file_path: str,
    content_hash: str | None = None,
    language: str | None = None,
    store_content: bool = False
) -> dict
```

**Parameters**:
- `project_id` - Project UUID
- `file_path` - Relative file path
- `content_hash` - SHA-256 hash (optional, auto-calculated if not provided)
- `language` - Programming language (optional, auto-detected)
- `store_content` - Whether to store file content in graph (optional)

**Example**:
```python
file = await add_file_to_project(
    project_id="proj-123",
    file_path="src/auth/login.py",
    language="Python"
)
```

---

### add_directory_to_project

Registers directory structure in graph.

**Signature**:
```python
async def add_directory_to_project(
    project_id: str,
    directory_path: str,
    recursive: bool = True
) -> dict
```

**Parameters**:
- `project_id` - Project UUID
- `directory_path` - Directory path
- `recursive` - Include subdirectories and files

**Returns**: Count of directories and files added

---

## Workflow Tools

### create_action_template

Defines a reusable workflow template.

**Signature**:
```python
async def create_action_template(
    keyword: str,
    description: str,
    cypher_query: str,
    guidance: str,
    parameters: dict,
    version: str = "1.0.0"
) -> dict
```

**Parameters**:
- `keyword` - Unique template identifier (uppercase recommended)
- `description` - Template purpose
- `cypher_query` - Cypher queries for execution
- `guidance` - Usage instructions for AI assistants
- `parameters` - Parameter schema with types
- `version` - Template version (semantic versioning)

**Example**:
```python
template = await create_action_template(
    keyword="CODE_REVIEW",
    description="Review code for quality and security",
    cypher_query="""
        MATCH (f:File {path: $file_path})
        CREATE (exec:WorkflowExecution {
          id: randomUUID(),
          templateKeyword: 'CODE_REVIEW',
          status: 'pending',
          parameters: $params
        })-[:EXECUTED_ON]->(f)
        RETURN exec
    """,
    guidance="Use for systematic code review",
    parameters={
        "file_path": "string",
        "review_type": "string",
        "severity_threshold": "string"
    }
)
```

---

### execute_workflow

Executes an action template with parameters.

**Signature**:
```python
async def execute_workflow(
    template_keyword: str,
    parameters: dict
) -> dict
```

**Parameters**:
- `template_keyword` - Template to execute (must exist with `isCurrent=true`)
- `parameters` - Execution parameters matching template schema

**Returns**:
```json
{
  "success": true,
  "execution_id": "uuid",
  "status": "completed",
  "results": {...}
}
```

**Example**:
```python
result = await execute_workflow(
    template_keyword="CODE_REVIEW",
    parameters={
        "file_path": "src/auth.py",
        "review_type": "security",
        "severity_threshold": "medium"
    }
)
```

---

### get_workflow_history

Queries workflow execution audit trail.

**Signature**:
```python
async def get_workflow_history(
    project_id: str | None = None,
    template_keyword: str | None = None,
    status: str | None = None,
    limit: int = 50
) -> dict
```

**Parameters**:
- `project_id` - Filter by project (optional)
- `template_keyword` - Filter by template (optional)
- `status` - Filter by status: pending, running, completed, failed (optional)
- `limit` - Maximum results (default: 50, max: 1000)

**Returns**: List of WorkflowExecution nodes with metadata

---

## Incarnation Management Tools

### switch_incarnation

Switches the active incarnation.

**Signature**:
```python
async def switch_incarnation(
    incarnation_type: str
) -> dict
```

**Parameters**:
- `incarnation_type` - Target incarnation: coding, knowledge_graph, code_analysis, research, decision_support, data_analysis, complex_system

**Returns**:
```json
{
  "success": true,
  "previous_incarnation": "coding",
  "current_incarnation": "code_analysis",
  "available_tools": [...]
}
```

**Example**:
```python
# Switch from coding to code analysis
result = await switch_incarnation("code_analysis")

# Verify switch
assert result["current_incarnation"] == "code_analysis"
```

---

### list_available_tools

Lists tools available in current incarnation.

**Signature**:
```python
async def list_available_tools(
    incarnation: str | None = None
) -> dict
```

**Parameters**:
- `incarnation` - Specific incarnation (optional, defaults to current)

**Returns**: List of tool names, descriptions, and signatures

---

## Guidance Hub Tools

### list_guidance_hubs

Lists available guidance hubs.

**Signature**:
```python
async def list_guidance_hubs(
    incarnation: str | None = None
) -> dict
```

**Returns**: List of hub names and descriptions

---

### get_guidance_hub_content

Retrieves guidance hub content.

**Signature**:
```python
async def get_guidance_hub_content(
    hub_name: str
) -> str
```

**Parameters**:
- `hub_name` - Hub identifier (e.g., 'main_hub', 'coding_guide', 'coding_cypher_guide')

**Returns**: Markdown-formatted guidance content

**Example**:
```python
# Get main navigation hub
content = await get_guidance_hub_content("main_hub")

# Get incarnation-specific guide
coding_guide = await get_guidance_hub_content("coding_guide")

# Get Cypher pattern library
cypher_patterns = await get_guidance_hub_content("coding_cypher_guide")
```

---

## Query Tools

### execute_cypher_query

Executes a Cypher query against Neo4j.

**Signature**:
```python
async def execute_cypher_query(
    query: str,
    parameters: dict | None = None
) -> dict
```

**Parameters**:
- `query` - Cypher query string
- `parameters` - Query parameters (optional)

**Returns**:
```json
{
  "success": true,
  "results": [...],
  "result_count": 10
}
```

**Example**:
```python
# Query projects
result = await execute_cypher_query("""
    MATCH (p:Project)
    WHERE p.tags CONTAINS $tag
    RETURN p.name as name, p.description as description
""", {"tag": "microservice"})

# Query with aggregation
stats = await execute_cypher_query("""
    MATCH (p:Project)-[:HAS_FILE]->(f:File)
    RETURN p.name as project,
           count(f) as file_count,
           collect(DISTINCT f.language) as languages
""")
```

---

### query_with_vector_search

Executes hybrid query combining Neo4j and Qdrant.

**Signature**:
```python
async def query_with_vector_search(
    query_text: str,
    collection_name: str = "knowledge",
    limit: int = 10,
    cypher_filter: str | None = None
) -> dict
```

**Parameters**:
- `query_text` - Semantic search query
- `collection_name` - Qdrant collection
- `limit` - Maximum results
- `cypher_filter` - Additional Neo4j filter (optional)

**Returns**: Combined results from vector and graph databases

---
