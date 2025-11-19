---
title: API Reference (Part 1)
category: 08_Reference
last_updated: 2025-10-25
line_count: 482
status: published
tags: [neocoder, mcp, documentation]
---

# API Reference

[← Back to Cypher Patterns](01_Cypher_Patterns.md) | [Next: Troubleshooting →](03_Troubleshooting.md)

## Overview

Complete API reference for NeoCoder MCP server tools, organized by incarnation and functionality.

## Core System APIs

### Incarnation Management

#### `get_current_incarnation()`

Get active incarnation type.

**Returns**:
```python
{
    "success": bool,
    "incarnation": str,  # "knowledge_graph" | "coding" | "code_analysis" | etc.
    "description": str
}
```

#### `switch_incarnation(incarnation_type: str)`

Switch to a different incarnation.

**Parameters**:
- `incarnation_type` (str): Target incarnation name

**Returns**:
```python
{
    "success": bool,
    "previous_incarnation": str,
    "current_incarnation": str,
    "message": str
}
```

### Guidance Hub APIs

#### `get_guidance_hub(hub_name: str)`

Retrieve guidance hub content.

**Parameters**:
- `hub_name` (str): Hub name (e.g., "main_hub", "knowledge_graph_hub")

**Returns**:
```python
{
    "success": bool,
    "hub_name": str,
    "title": str,
    "content": str,  # Markdown content
    "version": str,
    "related_hubs": List[str]
}
```

## Project Management APIs

### Project Operations

#### `create_project(name: str, root_path: str, description: str = "", metadata: Optional[Dict] = None, tags: Optional[List[str]] = None)`

Create a new project.

**Parameters**:
- `name` (str): Project name
- `root_path` (str): Absolute path to project root
- `description` (str, optional): Project description
- `metadata` (Dict, optional): Additional metadata
- `tags` (List[str], optional): Classification tags

**Returns**:
```python
{
    "success": bool,
    "project_id": str,  # UUID
    "message": str
}
```

#### `get_project(project_id: str)`

Retrieve project details.

**Parameters**:
- `project_id` (str): Project UUID

**Returns**:
```python
{
    "success": bool,
    "project": {
        "id": str,
        "name": str,
        "description": str,
        "root_path": str,
        "metadata": Dict,
        "tags": List[str],
        "created": str,  # ISO 8601
        "updated": str   # ISO 8601
    },
    "file_count": int,
    "entity_count": int
}
```

### File Operations

#### `add_file_to_project(project_id: str, file_path: str, content: Optional[str] = None, metadata: Optional[Dict] = None)`

Add file to project.

**Parameters**:
- `project_id` (str): Project UUID
- `file_path` (str): Relative or absolute file path
- `content` (str, optional): File content
- `metadata` (Dict, optional): File metadata

**Returns**:
```python
{
    "success": bool,
    "file_id": str,
    "message": str
}
```

## Knowledge Graph APIs

### Entity Management

#### `create_knowledge_entity(name: str, entity_type: str, description: str = "", domain: Optional[str] = None, properties: Optional[Dict] = None, tags: Optional[List[str]] = None)`

Create knowledge entity.

**Parameters**:
- `name` (str): Entity name
- `entity_type` (str): Type: "concept", "technology", "person", "organization"
- `description` (str, optional): Detailed description
- `domain` (str, optional): Knowledge domain
- `properties` (Dict, optional): Custom properties
- `tags` (List[str], optional): Tags

**Returns**:
```python
{
    "success": bool,
    "entity_id": str,
    "message": str
}
```

#### `get_knowledge_entity(entity_id: str)`

Retrieve entity details.

**Parameters**:
- `entity_id` (str): Entity UUID

**Returns**:
```python
{
    "success": bool,
    "entity": {
        "id": str,
        "name": str,
        "type": str,
        "description": str,
        "domain": str,
        "properties": Dict,
        "tags": List[str],
        "created": str,
        "updated": str
    },
    "relationships": List[Dict],
    "citations": List[Dict]
}
```

#### `update_knowledge_entity(entity_id: str, updates: Dict)`

Update entity properties.

**Parameters**:
- `entity_id` (str): Entity UUID
- `updates` (Dict): Properties to update

**Returns**:
```python
{
    "success": bool,
    "entity_id": str,
    "updated_fields": List[str],
    "message": str
}
```

### Relationship Management

#### `create_relationship(source_id: str, target_id: str, relationship_type: str, description: str = "", properties: Optional[Dict] = None)`

Create relationship between entities.

**Parameters**:
- `source_id` (str): Source entity UUID
- `target_id` (str): Target entity UUID
- `relationship_type` (str): Relationship type
- `description` (str, optional): Relationship description
- `properties` (Dict, optional): Additional properties

**Returns**:
```python
{
    "success": bool,
    "relationship_id": str,
    "source_id": str,
    "target_id": str,
    "type": str,
    "message": str
}
```

### Knowledge Querying

#### `query_knowledge_graph(query: str, filters: Optional[Dict] = None, limit: int = 10)`

Query knowledge graph with natural language.

**Parameters**:
- `query` (str): Natural language query
- `filters` (Dict, optional): Filter criteria
  - `domain` (str): Filter by domain
  - `entity_type` (str): Filter by type
  - `tags` (List[str]): Filter by tags
- `limit` (int): Maximum results

**Returns**:
```python
{
    "success": bool,
    "results": List[{
        "entity": Dict,
        "relevance_score": float,
        "matched_fields": List[str]
    }],
    "query_time": float
}
```

## Code Analysis APIs

### Structure Analysis

#### `analyze_code_structure(file_path: str, analysis_depth: int = 3, include_ast: bool = True, include_metrics: bool = True)`

Analyze code structure and generate AST.

**Parameters**:
- `file_path` (str): Path to code file
- `analysis_depth` (int): Analysis depth level (1-5)
- `include_ast` (bool): Include AST in response
- `include_metrics` (bool): Include complexity metrics

**Returns**:
```python
{
    "success": bool,
    "file_path": str,
    "language": str,
    "ast": Dict,  # Abstract Syntax Tree
    "entities": List[{
        "name": str,
        "type": str,  # "class", "function", "variable"
        "line_number": int,
        "complexity": int
    }],
    "metrics": {
        "total_lines": int,
        "code_lines": int,
        "comment_lines": int,
        "complexity": int,
        "maintainability_index": float
    }
}
```

#### `find_dependencies(file_path: str, include_external: bool = True)`

Find code dependencies.

**Parameters**:
- `file_path` (str): Path to code file
- `include_external` (bool): Include external library dependencies

**Returns**:
```python
{
    "success": bool,
    "file_path": str,
    "imports": List[str],
    "internal_dependencies": List[str],
    "external_dependencies": List[str],
    "dependency_graph": Dict
}
```

## Workflow APIs

### Template Execution

#### `execute_workflow(keyword: str, parameters: Dict, project_id: Optional[str] = None)`

Execute workflow template.

**Parameters**:
- `keyword` (str): Template keyword (e.g., "FIX", "FEATURE")
- `parameters` (Dict): Template-specific parameters
- `project_id` (str, optional): Associated project ID

**Returns**:
```python
{
    "success": bool,
    "execution_id": str,
    "keyword": str,
    "status": str,  # "completed" | "failed" | "in_progress"
    "result": Dict,
    "duration": float
}
```

#### `get_workflow_history(project_id: str, limit: int = 20)`

Get workflow execution history.

**Parameters**:
- `project_id` (str): Project UUID
- `limit` (int): Maximum executions to return

**Returns**:
```python
{
    "success": bool,
    "executions": List[{
        "execution_id": str,
        "keyword": str,
        "status": str,
        "started": str,
        "completed": str,
        "duration": float,
        "result": Dict
    }],
    "total_count": int
}
```

## Research APIs

### Citation Management

#### `add_research_citation(entity_id: str, title: str, authors: List[str], year: int, doi: Optional[str] = None, url: Optional[str] = None)`

Add research paper citation.

**Parameters**:
- `entity_id` (str): Related entity UUID
- `title` (str): Paper title
- `authors` (List[str]): Author names
- `year` (int): Publication year
- `doi` (str, optional): DOI identifier
- `url` (str, optional): Paper URL

**Returns**:
```python
{
    "success": bool,
    "citation_id": str,
    "message": str
}
```

### F-Contraction Synthesis

#### `f_contraction_synthesis(source_ids: List[str], preserve_attribution: bool = True)`

Synthesize knowledge using F-Contraction.

**Parameters**:
- `source_ids` (List[str]): Source entity UUIDs
- `preserve_attribution` (bool): Maintain citation chain

**Returns**:
```python
{
    "success": bool,
    "synthesized_id": str,
    "source_count": int,
    "citations_preserved": int,
    "conflicts": List[Dict],
    "message": str
}
```

## Hybrid Reasoning APIs

### Vector Search

#### `semantic_search(query_text: str, collection: str = "knowledge", limit: int = 10, threshold: float = 0.7)`

Semantic search using vector similarity.

**Parameters**:
- `query_text` (str): Natural language query
- `collection` (str): Qdrant collection name
- `limit` (int): Maximum results
- `threshold` (float): Minimum similarity score (0.0-1.0)

**Returns**:
```python
{
    "success": bool,
    "results": List[{
        "id": str,
        "score": float,
        "payload": Dict
    }],
    "query_time": float
}
```

#### `hybrid_search(query_text: str, graph_filter: Optional[Dict] = None, limit: int = 10)`

Combined vector + graph search.

**Parameters**:
- `query_text` (str): Search query
- `graph_filter` (Dict, optional): Neo4j filter criteria
- `limit` (int): Maximum results

**Returns**:
```python
{
    "success": bool,
    "results": List[{
        "entity": Dict,
        "similarity_score": float,
        "neighbors": List[Dict],
        "relationship_types": List[str]
    }],
    "result_count": int
}
```

### Embedding Operations

#### `add_to_vector_store(entity_id: str, embedding_text: str, collection: str = "knowledge", metadata: Optional[Dict] = None)`

Add entity embedding to Qdrant.

**Parameters**:
- `entity_id` (str): Entity UUID
- `embedding_text` (str): Text to embed
- `collection` (str): Collection name
- `metadata` (Dict, optional): Additional metadata

**Returns**:
```python
{
    "success": bool,
    "entity_id": str,
    "collection": str,
    "message": str
}
```
