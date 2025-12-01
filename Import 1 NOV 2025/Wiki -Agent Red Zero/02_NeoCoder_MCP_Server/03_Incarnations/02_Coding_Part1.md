---
title: Coding Incarnation (Part 1 of 2)
category: 03_Incarnations
last_updated: 2025-10-25
line_count: 454
status: published
tags: [neocoder, mcp, documentation]
---


# Coding Incarnation

[← Back to Overview](01_Overview.md) | [Next: Knowledge Graph →](03_Knowledge_Graph.md)

## Overview

The **Coding Incarnation** is designed for software development workflows, providing tools and schema for managing software projects, tracking file structures, executing development workflows, and maintaining project metadata in Neo4j.

**Incarnation Type**: `coding`
**Version**: 1.0.0
**Primary Use Cases**: Project management, file tracking, development workflows

## Core Capabilities

### Project Management
- Create and configure software projects
- Track project metadata and properties
- Query project structure and composition
- Manage project lifecycle

### File System Integration
- Register files and directories in graph
- Track file modifications and versions
- Map directory hierarchies
- Store file metadata and content hashes

### Workflow Execution
- Execute action templates for common tasks
- Track workflow execution history
- Maintain audit trails
- Coordinate multi-step operations

### Development Operations
- Build and deployment tracking
- Code modification workflows
- Test execution management
- CI/CD integration points

## Schema

### Node Types

**Project**:
```cypher
CREATE (p:Project {
  id: randomUUID(),
  name: 'MyProject',
  description: 'Project description',
  rootPath: '/path/to/project',
  created: datetime(),
  updated: datetime(),
  metadata: {
    language: 'Python',
    framework: 'FastAPI',
    version: '1.0.0'
  },
  tags: ['api', 'microservice']
})
```

**File**:
```cypher
CREATE (f:File {
  id: randomUUID(),
  path: 'src/main.py',
  absolutePath: '/project/src/main.py',
  name: 'main.py',
  extension: 'py',
  size: 4096,
  hash: 'sha256:abc123...',
  created: datetime(),
  updated: datetime(),
  language: 'Python'
})
```

**Directory**:
```cypher
CREATE (d:Directory {
  id: randomUUID(),
  path: 'src',
  absolutePath: '/project/src',
  name: 'src',
  created: datetime(),
  updated: datetime()
})
```

**ActionTemplate**:
```cypher
CREATE (t:ActionTemplate {
  keyword: 'BUILD_PROJECT',
  description: 'Build and compile project',
  isCurrent: true,
  version: '1.0.0',
  created: datetime(),
  cypher: '...',
  guidance: 'Run build workflow',
  parameters: {
    build_type: 'string',
    clean: 'boolean'
  }
})
```

**WorkflowExecution**:
```cypher
CREATE (e:WorkflowExecution {
  id: randomUUID(),
  templateKeyword: 'BUILD_PROJECT',
  status: 'completed',
  startTime: datetime(),
  endTime: datetime(),
  parameters: {build_type: 'release'},
  results: {success: true},
  executedBy: 'claude'
})
```

### Relationships

**Project → File/Directory**:
```cypher
(p:Project)-[:HAS_FILE]->(f:File)
(p:Project)-[:HAS_DIRECTORY]->(d:Directory)
```

**Directory Hierarchy**:
```cypher
(parent:Directory)-[:CONTAINS]->(child:Directory)
(dir:Directory)-[:CONTAINS]->(file:File)
(file:File)-[:PARENT_DIR]->(dir:Directory)
```

**Workflow Tracking**:
```cypher
(exec:WorkflowExecution)-[:USED_TEMPLATE]->(template:ActionTemplate)
(exec:WorkflowExecution)-[:EXECUTED_ON]->(target)
(exec:WorkflowExecution)-[:CREATED]->(entity)
(exec:WorkflowExecution)-[:MODIFIED]->(entity)
```

## Available Tools

### create_project

Creates a new software project in Neo4j.

**Signature**:
```python
async def create_project(
    name: str,
    root_path: str,
    description: str = "",
    metadata: dict = None,
    tags: list[str] = None
) -> dict
```

**Parameters**:
- `name` (string, required) - Project name
- `root_path` (string, required) - Filesystem root path
- `description` (string, optional) - Project description
- `metadata` (dict, optional) - Additional properties
- `tags` (list[string], optional) - Categorization tags

**Returns**:
```json
{
  "success": true,
  "project_id": "uuid-string",
  "project": {
    "id": "uuid-string",
    "name": "MyProject",
    "rootPath": "/path/to/project"
  }
}
```

**Example**:
```python
result = await create_project(
    name="AuthService",
    root_path="/src/auth-service",
    description="User authentication microservice",
    metadata={
        "language": "Python",
        "framework": "FastAPI"
    },
    tags=["microservice", "authentication"]
)
```

### add_file_to_project

Registers a file in the project graph.

**Signature**:
```python
async def add_file_to_project(
    project_id: str,
    file_path: str,
    content_hash: str = None,
    language: str = None,
    store_content: bool = False
) -> dict
```

**Parameters**:
- `project_id` (string, required) - Project UUID
- `file_path` (string, required) - Relative file path
- `content_hash` (string, optional) - File content SHA-256 hash
- `language` (string, optional) - Programming language
- `store_content` (boolean, optional) - Whether to store file content in graph

**Returns**:
```json
{
  "success": true,
  "file_id": "uuid-string",
  "file": {
    "id": "uuid-string",
    "path": "src/main.py",
    "language": "Python"
  }
}
```

**Example**:
```python
result = await add_file_to_project(
    project_id="proj-123",
    file_path="src/auth/login.py",
    language="Python",
    content_hash="sha256:abc123..."
)
```

### add_directory_to_project

Registers a directory structure in the project graph.

**Signature**:
```python
async def add_directory_to_project(
    project_id: str,
    directory_path: str,
    recursive: bool = True
) -> dict
```

**Parameters**:
- `project_id` (string, required) - Project UUID
- `directory_path` (string, required) - Directory path
- `recursive` (boolean, optional) - Include subdirectories

**Returns**:
```json
{
  "success": true,
  "directory_id": "uuid-string",
  "files_added": 15,
  "directories_added": 3
}
```

### get_project_structure

Retrieves project structure from Neo4j.

**Signature**:
```python
async def get_project_structure(
    project_id: str,
    include_files: bool = True,
    include_directories: bool = True
) -> dict
```

**Parameters**:
- `project_id` (string, required) - Project UUID
- `include_files` (boolean, optional) - Include file nodes
- `include_directories` (boolean, optional) - Include directory nodes

**Returns**:
```json
{
  "success": true,
  "project": {
    "id": "uuid",
    "name": "MyProject",
    "rootPath": "/path"
  },
  "directories": [
    {"id": "dir-1", "path": "src", "name": "src"}
  ],
  "files": [
    {"id": "file-1", "path": "src/main.py", "language": "Python"}
  ]
}
```

### update_project_metadata

Modifies project properties.

**Signature**:
```python
async def update_project_metadata(
    project_id: str,
    metadata: dict = None,
    tags: list[str] = None,
    description: str = None
) -> dict
```

**Parameters**:
- `project_id` (string, required) - Project UUID
- `metadata` (dict, optional) - Properties to update
- `tags` (list[string], optional) - New tags
- `description` (string, optional) - New description

**Example**:
```python
await update_project_metadata(
    project_id="proj-123",
    metadata={"version": "2.0.0"},
    tags=["production", "stable"]
)
```

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
- `keyword` (string, required) - Template identifier
- `description` (string, required) - Template purpose
- `cypher_query` (string, required) - Cypher for execution
- `guidance` (string, required) - Usage instructions
- `parameters` (dict, required) - Parameter definitions
- `version` (string, optional) - Template version

**Example**:
```python
await create_action_template(
    keyword="BUILD_PROJECT",
    description="Build and compile project",
    cypher_query="""
        MATCH (p:Project {id: $project_id})
        CREATE (e:WorkflowExecution {
          id: randomUUID(),
          templateKeyword: 'BUILD_PROJECT',
          status: 'pending',
          startTime: datetime()
        })-[:EXECUTED_ON]->(p)
        RETURN e
    """,
    guidance="Use for building projects",
    parameters={
        "project_id": "string",
        "build_type": "string",
        "clean": "boolean"
    }
)
```

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
- `template_keyword` (string, required) - Template to execute
- `parameters` (dict, required) - Execution parameters

**Returns**:
```json
{
  "success": true,
  "execution_id": "uuid-string",
  "status": "completed",
  "results": {}
}
```

**Example**:
```python
result = await execute_workflow(
    template_keyword="BUILD_PROJECT",
    parameters={
        "project_id": "proj-123",
        "build_type": "release",
        "clean": true
    }
)
```

### get_workflow_history

Queries workflow execution audit trail.

**Signature**:
```python
async def get_workflow_history(
    project_id: str = None,
    template_keyword: str = None,
    status: str = None,
    limit: int = 50
) -> dict
```

**Parameters**:
- `project_id` (string, optional) - Filter by project
- `template_keyword` (string, optional) - Filter by template
- `status` (string, optional) - Filter by status
- `limit` (int, optional) - Max results

**Returns**:
```json
{
  "success": true,
  "executions": [
    {
      "id": "exec-1",
      "templateKeyword": "BUILD_PROJECT",
      "status": "completed",
      "startTime": "2024-01-15T10:00:00Z",
      "endTime": "2024-01-15T10:05:00Z"
    }
  ]
}
```
