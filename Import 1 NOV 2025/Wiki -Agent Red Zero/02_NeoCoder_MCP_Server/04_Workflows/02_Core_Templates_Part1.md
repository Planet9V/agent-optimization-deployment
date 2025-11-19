---
title: Core Workflow Templates (Part 1)
category: 04_Workflows
last_updated: 2025-10-25
line_count: 492
status: published
tags: [neocoder, mcp, documentation]
---

# Core Workflow Templates

[← Back to Overview](01_Template_Overview.md) | [Next: Advanced Templates →](03_Advanced_Templates.md)

## Overview

Core templates are the standard workflow patterns provided by NeoCoder for common development, knowledge management, and analysis operations.

## Development Templates

### FIX Template

**Purpose**: Fix bugs, resolve issues, or correct problems in code

**Keyword**: `FIX`

**Parameters**:
```json
{
  "file_path": "string (required)",
  "issue_description": "string (required)",
  "fix_type": "string (optional): bug|typo|logic|performance",
  "project_id": "string (optional)"
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="FIX",
    parameters={
        "file_path": "src/auth.py",
        "issue_description": "Authentication bypass vulnerability",
        "fix_type": "bug"
    }
)
```

**Workflow Steps**:
1. Create WorkflowExecution node with FIX keyword
2. Link to target file
3. Record issue description and fix type
4. Track execution status
5. Store fix results and verification

---

### REFACTOR Template

**Purpose**: Restructure code for improved maintainability, readability, or performance

**Keyword**: `REFACTOR`

**Parameters**:
```json
{
  "file_path": "string (required)",
  "refactor_goal": "string (required)",
  "scope": "string (optional): function|class|module",
  "preserve_behavior": "boolean (default: true)"
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="REFACTOR",
    parameters={
        "file_path": "src/data_processor.py",
        "refactor_goal": "Extract complex validation logic into separate functions",
        "scope": "module",
        "preserve_behavior": true
    }
)
```

**Workflow Steps**:
1. Analyze current code structure
2. Create refactoring plan
3. Execute refactoring transformations
4. Verify behavior preservation
5. Update code entities in graph

---

### FEATURE Template

**Purpose**: Add new feature or capability to codebase

**Keyword**: `FEATURE`

**Parameters**:
```json
{
  "feature_name": "string (required)",
  "description": "string (required)",
  "files_affected": "array[string] (optional)",
  "project_id": "string (optional)"
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="FEATURE",
    parameters={
        "feature_name": "Two-Factor Authentication",
        "description": "Add TOTP-based 2FA support",
        "files_affected": ["src/auth/totp.py", "src/auth/models.py"],
        "project_id": "proj-123"
    }
)
```

**Workflow Steps**:
1. Create feature tracking node
2. Link to affected files
3. Track implementation progress
4. Record feature completion
5. Update project metadata

---

### CODE_ANALYZE Template

**Purpose**: Perform code structure and dependency analysis

**Keyword**: `CODE_ANALYZE`

**Parameters**:
```json
{
  "file_path": "string (required)",
  "analysis_depth": "integer (1-5, default: 3)",
  "include_metrics": "boolean (default: true)",
  "include_dependencies": "boolean (default: true)"
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="CODE_ANALYZE",
    parameters={
        "file_path": "src/auth/service.py",
        "analysis_depth": 3,
        "include_metrics": true,
        "include_dependencies": true
    }
)
```

**Workflow Steps**:
1. Parse file into AST
2. Extract code entities (classes, functions)
3. Map dependencies and call graphs
4. Calculate complexity metrics
5. Store analysis results in graph

---

## Deployment Templates

### BUILD Template

**Purpose**: Build and compile project

**Keyword**: `BUILD`

**Parameters**:
```json
{
  "project_id": "string (required)",
  "build_type": "string (optional): dev|staging|production",
  "clean": "boolean (default: false)",
  "run_tests": "boolean (default: true)"
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="BUILD",
    parameters={
        "project_id": "proj-123",
        "build_type": "production",
        "clean": true,
        "run_tests": true
    }
)
```

**Workflow Steps**:
1. Clean build artifacts (if requested)
2. Compile source code
3. Run tests (if enabled)
4. Package build outputs
5. Store build metadata

---

### DEPLOY Template

**Purpose**: Deploy project to target environment

**Keyword**: `DEPLOY`

**Parameters**:
```json
{
  "project_id": "string (required)",
  "environment": "string (required): dev|staging|production",
  "version": "string (optional)",
  "rollback_enabled": "boolean (default: true)"
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="DEPLOY",
    parameters={
        "project_id": "proj-123",
        "environment": "staging",
        "version": "2.0.1",
        "rollback_enabled": true
    }
)
```

**Workflow Steps**:
1. Verify build completion
2. Prepare deployment package
3. Execute deployment to environment
4. Run health checks
5. Enable rollback if needed

---

### TOOL_ADD Template

**Purpose**: Add new tool or dependency to project

**Keyword**: `TOOL_ADD`

**Parameters**:
```json
{
  "project_id": "string (required)",
  "tool_name": "string (required)",
  "tool_type": "string (required): library|package|service",
  "version": "string (optional)",
  "configuration": "object (optional)"
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="TOOL_ADD",
    parameters={
        "project_id": "proj-123",
        "tool_name": "redis",
        "tool_type": "service",
        "version": "7.0",
        "configuration": {"port": 6379}
    }
)
```

---

## Knowledge Management Templates

### KNOWLEDGE_QUERY Template

**Purpose**: Query knowledge graph with structured queries

**Keyword**: `KNOWLEDGE_QUERY`

**Parameters**:
```json
{
  "query_type": "string (required): cypher|semantic|hybrid",
  "query": "string (required)",
  "parameters": "object (optional)",
  "limit": "integer (default: 50)"
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="KNOWLEDGE_QUERY",
    parameters={
        "query_type": "cypher",
        "query": "MATCH (e:KnowledgeEntity {domain: $domain}) RETURN e",
        "parameters": {"domain": "artificial_intelligence"},
        "limit": 20
    }
)
```

**Workflow Steps**:
1. Validate query syntax
2. Execute query against Neo4j
3. Format results
4. Track query execution
5. Return results with metadata

---

### KNOWLEDGE_EXTRACT Template

**Purpose**: Extract semantic knowledge from text or documents

**Keyword**: `KNOWLEDGE_EXTRACT`

**Parameters**:
```json
{
  "source_text": "string (required)",
  "domain": "string (optional)",
  "entity_types": "array[string] (optional)",
  "extraction_method": "string (default: nlp)"
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="KNOWLEDGE_EXTRACT",
    parameters={
        "source_text": "Machine learning is a subset of AI...",
        "domain": "artificial_intelligence",
        "entity_types": ["concept", "process", "method"]
    }
)
```

**Workflow Steps**:
1. Parse source text
2. Extract entities and relationships
3. Create KnowledgeEntity nodes
4. Link entities with relationships
5. Add citations if source provided

---

### KNOWLEDGE_LINK Template

**Purpose**: Create relationships between knowledge entities

**Keyword**: `KNOWLEDGE_LINK`

**Parameters**:
```json
{
  "source_entity_id": "string (required)",
  "target_entity_id": "string (required)",
  "relationship_type": "string (required): RELATES_TO|IS_A|PART_OF|DEPENDS_ON",
  "properties": "object (optional)"
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="KNOWLEDGE_LINK",
    parameters={
        "source_entity_id": "deep-learning-uuid",
        "target_entity_id": "machine-learning-uuid",
        "relationship_type": "IS_A",
        "properties": {"confidence": 1.0}
    }
)
```

---

## Research Templates

### RESEARCH_ANALYZE Template

**Purpose**: Analyze research papers and extract key information

**Keyword**: `RESEARCH_ANALYZE`

**Parameters**:
```json
{
  "paper_id": "string (required)",
  "analysis_type": "string (optional): summary|citation_network|methodology",
  "extract_entities": "boolean (default: true)"
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="RESEARCH_ANALYZE",
    parameters={
        "paper_id": "paper-123",
        "analysis_type": "citation_network",
        "extract_entities": true
    }
)
```

**Workflow Steps**:
1. Retrieve paper metadata
2. Analyze paper content
3. Extract key entities and concepts
4. Map citation relationships
5. Store analysis results

---

### CITATION_MAP Template

**Purpose**: Map citation networks between research papers

**Keyword**: `CITATION_MAP`

**Parameters**:
```json
{
  "paper_id": "string (required)",
  "direction": "string (optional): cited_by|references|both",
  "max_depth": "integer (default: 2)"
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="CITATION_MAP",
    parameters={
        "paper_id": "paper-123",
        "direction": "both",
        "max_depth": 3
    }
)
```

**Workflow Steps**:
1. Find paper node in graph
2. Traverse citation relationships
3. Map citation network structure
4. Calculate citation metrics
5. Visualize citation graph

---

### SYNTHESIZE Template

**Purpose**: F-Contraction knowledge synthesis from multiple sources

**Keyword**: `SYNTHESIZE`

**Parameters**:
```json
{
  "source_ids": "array[string] (required)",
  "synthesis_method": "string (default: f_contraction)",
  "preserve_attribution": "boolean (default: true)",
  "output_format": "string (optional): knowledge_graph|document"
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="SYNTHESIZE",
    parameters={
        "source_ids": ["paper-1", "paper-2", "paper-3"],
        "synthesis_method": "f_contraction",
        "preserve_attribution": true,
        "output_format": "knowledge_graph"
    }
)
```

**Workflow Steps**:
1. Retrieve source entities
2. Apply F-Contraction synthesis
3. Create synthesized knowledge entity
4. Link to source entities with DERIVED_FROM
5. Maintain citation attribution

---
