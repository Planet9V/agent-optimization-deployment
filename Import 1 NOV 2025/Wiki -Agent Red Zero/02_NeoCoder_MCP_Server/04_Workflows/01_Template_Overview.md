---
title: Workflow Template Overview
category: 04_Workflows
last_updated: 2025-10-25
line_count: 453
status: published
tags: [neocoder, mcp, documentation]
---

# Workflow Template Overview

[← Back to Incarnations](../03_Incarnations/05_Other_Incarnations.md) | [Next: Core Templates →](02_Core_Templates.md)

## What Are Workflow Templates?

Workflow templates (ActionTemplates) are **reusable workflow patterns** stored in Neo4j that define standardized processes for common operations. They combine Cypher queries, parameter definitions, and execution guidance to create consistent, traceable workflows.

## Template Architecture

### Components

**ActionTemplate Node**:
```cypher
CREATE (template:ActionTemplate {
  keyword: 'CODE_ANALYZE',              // Unique identifier
  description: 'Analyze code structure',// Human-readable purpose
  isCurrent: true,                      // Active version flag
  version: '1.0.0',                     // Template version
  created: datetime(),                  // Creation timestamp
  cypher: $cypher_queries,              // Execution queries
  guidance: $usage_instructions,        // How to use template
  parameters: {                         // Parameter schema
    file_path: 'string',
    analysis_depth: 'integer'
  }
})
```

### Template Lifecycle

1. **Definition** - Create template with keyword, Cypher, parameters
2. **Registration** - Store in Neo4j with current version flag
3. **Discovery** - AI assistants find templates via guidance hubs
4. **Execution** - Run template with parameters
5. **Tracking** - Create WorkflowExecution audit node
6. **Versioning** - Update template, mark new version as current

## Template Categories

### Project Management Templates
- **CREATE_PROJECT** - Initialize new project
- **ADD_FILES** - Register files in project
- **UPDATE_METADATA** - Modify project properties

### Code Operations Templates
- **CODE_ANALYZE** - Analyze code structure
- **FIX** - Fix bugs or issues
- **REFACTOR** - Improve code structure
- **FEATURE** - Add new functionality

### Knowledge Management Templates
- **KNOWLEDGE_EXTRACT** - Extract semantic knowledge
- **KNOWLEDGE_QUERY** - Query knowledge graph
- **KNOWLEDGE_LINK** - Create entity relationships

### Development Workflow Templates
- **BUILD** - Build project
- **DEPLOY** - Deploy to environment
- **TEST** - Execute tests
- **TOOL_ADD** - Add new tool

## Standard Template Keywords

NeoCoder defines several standard action template keywords:

**Code Development**:
- `FIX` - Fix bug or resolve issue
- `REFACTOR` - Restructure code for improvement
- `FEATURE` - Add new feature or capability
- `CODE_ANALYZE` - Perform code structure analysis
- `OPTIMIZE` - Performance optimization

**Deployment & Operations**:
- `BUILD` - Build and compile project
- `DEPLOY` - Deploy to target environment
- `TOOL_ADD` - Add new tool or dependency
- `CONFIGURE` - Update configuration

**Knowledge Operations**:
- `KNOWLEDGE_QUERY` - Query knowledge base
- `KNOWLEDGE_EXTRACT` - Extract knowledge from source
- `KNOWLEDGE_LINK` - Create knowledge relationships

**Research Operations**:
- `RESEARCH_ANALYZE` - Analyze research papers
- `CITATION_MAP` - Map citation networks
- `SYNTHESIZE` - F-Contraction knowledge synthesis

## Template Structure

### Minimum Viable Template

```python
{
  "keyword": "EXAMPLE_TEMPLATE",
  "description": "Example workflow template",
  "isCurrent": true,
  "version": "1.0.0",
  "cypher": """
    MATCH (p:Project {id: $project_id})
    CREATE (exec:WorkflowExecution {
      id: randomUUID(),
      templateKeyword: 'EXAMPLE_TEMPLATE',
      status: 'pending',
      startTime: datetime(),
      parameters: $params
    })-[:EXECUTED_ON]->(p)
    RETURN exec
  """,
  "guidance": "Use this template for example workflows",
  "parameters": {
    "project_id": "string",
    "param1": "string"
  }
}
```

### Complete Template

```python
{
  "keyword": "CODE_ANALYZE",
  "description": "Analyze code structure and dependencies",
  "isCurrent": true,
  "version": "1.2.0",
  "created": "2024-01-15T10:00:00Z",
  "cypher": """
    // Step 1: Create execution record
    CREATE (exec:WorkflowExecution {
      id: randomUUID(),
      templateKeyword: 'CODE_ANALYZE',
      status: 'running',
      startTime: datetime(),
      parameters: $params,
      executedBy: $user_id
    })

    // Step 2: Find file to analyze
    WITH exec
    MATCH (f:File {path: $file_path})

    // Step 3: Link execution to file
    CREATE (exec)-[:EXECUTED_ON]->(f)

    // Step 4: Return execution for tracking
    RETURN exec.id as execution_id, f.path as file_path
  """,
  "guidance": """
    Use this template to analyze code structure.

    Required parameters:
    - file_path: Path to file for analysis
    - analysis_depth: Depth of AST traversal (1-5)

    Optional parameters:
    - include_metrics: Calculate complexity metrics
    - include_dependencies: Map function calls

    Best practices:
    - Use depth 3 for balanced analysis
    - Enable metrics for code quality review
    - Review execution results for issues
  """,
  "parameters": {
    "file_path": "string",
    "analysis_depth": "integer",
    "include_metrics": "boolean",
    "include_dependencies": "boolean",
    "user_id": "string"
  },
  "constraints": {
    "analysis_depth": {"min": 1, "max": 5},
    "file_path": {"required": true}
  },
  "tags": ["code-analysis", "ast", "metrics"],
  "incarnation": "code_analysis"
}
```

## Template Execution

### Basic Execution

```python
# Using execute_workflow tool
result = await execute_workflow(
    template_keyword="CODE_ANALYZE",
    parameters={
        "file_path": "src/auth.py",
        "analysis_depth": 3,
        "include_metrics": true,
        "user_id": "claude-assistant"
    }
)
```

### Execution Flow

1. **Validation** - Check template exists and is current
2. **Parameter Validation** - Verify required parameters provided
3. **Cypher Execution** - Run template's Cypher query
4. **Audit Trail** - Create WorkflowExecution node
5. **Result Capture** - Store execution results
6. **Status Update** - Mark execution as completed/failed
7. **Return Results** - Provide execution summary

### Execution Tracking

```cypher
// Create execution record
CREATE (exec:WorkflowExecution {
  id: randomUUID(),
  templateKeyword: $keyword,
  status: 'running',
  startTime: datetime(),
  parameters: $params,
  executedBy: $user_id
})

// Link to template
MATCH (template:ActionTemplate {keyword: $keyword, isCurrent: true})
CREATE (exec)-[:USED_TEMPLATE]->(template)

// Link to target entity
MATCH (target) WHERE target.id = $target_id
CREATE (exec)-[:EXECUTED_ON]->(target)

// After completion, update status
MATCH (exec:WorkflowExecution {id: $exec_id})
SET exec.status = 'completed',
    exec.endTime = datetime(),
    exec.results = $results
RETURN exec
```

## Template Discovery

### Via Guidance Hubs

Templates are suggested by guidance hubs based on context:

```markdown
# Coding Incarnation Guide

## Suggested Templates
- **CODE_ANALYZE** - Analyze code structure and dependencies
- **FIX** - Fix bugs or issues in code
- **REFACTOR** - Improve code organization
```

### Via Query

```cypher
// Find templates by keyword
MATCH (template:ActionTemplate)
WHERE template.keyword CONTAINS $search_term
  AND template.isCurrent = true
RETURN template

// Find templates by incarnation
MATCH (template:ActionTemplate)
WHERE template.incarnation = $incarnation
  AND template.isCurrent = true
RETURN template.keyword, template.description
ORDER BY template.keyword

// Find recently used templates
MATCH (exec:WorkflowExecution)-[:USED_TEMPLATE]->(template:ActionTemplate)
WHERE exec.startTime > datetime() - duration('P7D')
RETURN template.keyword,
       count(exec) as execution_count
ORDER BY execution_count DESC
```

## Template Versioning

### Creating New Version

```cypher
// Mark old version as archived
MATCH (old:ActionTemplate {keyword: $keyword, isCurrent: true})
SET old.isCurrent = false,
    old:ArchivedTemplate
REMOVE old:ActionTemplate

// Create new version
CREATE (new:ActionTemplate {
  keyword: $keyword,
  description: $new_description,
  isCurrent: true,
  version: $new_version,
  created: datetime(),
  cypher: $new_cypher,
  guidance: $new_guidance,
  parameters: $new_parameters,
  previousVersion: $old_version
})

// Preserve execution history link
MATCH (old:ArchivedTemplate {keyword: $keyword})
WHERE old.version = $old_version
CREATE (new)-[:SUPERSEDES]->(old)
```

### Version Querying

```cypher
// Get version history
MATCH path = (current:ActionTemplate {keyword: $keyword, isCurrent: true})
             -[:SUPERSEDES*0..]->(previous:ArchivedTemplate)
RETURN [node IN nodes(path) | {
  version: node.version,
  created: node.created,
  description: node.description
}] as version_history
```

## Template Composition

### Nested Templates

Templates can reference other templates:

```cypher
// Parent template
CREATE (parent:ActionTemplate {
  keyword: 'FULL_DEPLOYMENT',
  cypher: """
    // Execute BUILD template
    CALL apoc.cypher.run(
      'MATCH (t:ActionTemplate {keyword: "BUILD", isCurrent: true})
       WITH t.cypher as build_query
       CALL apoc.cypher.run(build_query, $params) YIELD value
       RETURN value',
      {params: $build_params}
    ) YIELD value as build_result

    // Execute DEPLOY template
    CALL apoc.cypher.run(
      'MATCH (t:ActionTemplate {keyword: "DEPLOY", isCurrent: true})
       WITH t.cypher as deploy_query
       CALL apoc.cypher.run(deploy_query, $params) YIELD value
       RETURN value',
      {params: $deploy_params}
    ) YIELD value as deploy_result

    RETURN build_result, deploy_result
  """
})
```

### Conditional Workflows

```cypher
CREATE (template:ActionTemplate {
  keyword: 'CONDITIONAL_BUILD',
  cypher: """
    // Check if tests pass
    MATCH (test_exec:WorkflowExecution {status: 'completed'})
    WHERE test_exec.templateKeyword = 'RUN_TESTS'
      AND test_exec.results.all_passed = true

    // If tests pass, proceed with build
    WITH test_exec
    WHERE test_exec IS NOT NULL
    CREATE (build_exec:WorkflowExecution {
      id: randomUUID(),
      templateKeyword: 'BUILD',
      status: 'running',
      startTime: datetime()
    })
    CREATE (build_exec)-[:DEPENDS_ON]->(test_exec)
    RETURN build_exec
  """
})
```

## Best Practices

### Template Design

**Single Responsibility**:
- Each template should do ONE thing well
- Avoid monolithic multi-purpose templates
- Compose complex workflows from simpler templates

**Parameter Clarity**:
- Use descriptive parameter names
- Document required vs optional parameters
- Provide parameter validation in guidance
- Use type annotations

**Error Handling**:
```cypher
// Good: Handle edge cases
OPTIONAL MATCH (target) WHERE target.id = $target_id
WITH target
WHERE target IS NOT NULL
// ... proceed with workflow

// Or provide clear error
WITH target
WHERE target IS NULL
RETURN {success: false, error: 'Target not found'}
```

### Execution Patterns

**Always Create Audit Trail**:
```python
# Every execution should create WorkflowExecution node
exec_node = {
  "id": uuid(),
  "templateKeyword": template_keyword,
  "status": "running",
  "startTime": datetime.now(),
  "parameters": parameters
}
```

**Link to Entities**:
```cypher
// Link execution to relevant entities
CREATE (exec)-[:EXECUTED_ON]->(target)
CREATE (exec)-[:USED_TEMPLATE]->(template)
CREATE (exec)-[:CREATED]->(new_entity)
CREATE (exec)-[:MODIFIED]->(updated_entity)
```

**Capture Results**:
```cypher
// Update execution with results
SET exec.status = 'completed',
    exec.endTime = datetime(),
    exec.results = {
      success: true,
      entities_created: 5,
      modifications: 3,
      metrics: {...}
    }
```

## Related Documentation

- [Core Templates](02_Core_Templates.md) - Standard template catalog
- [Advanced Templates](03_Advanced_Templates.md) - Complex workflow patterns
- [Graph Structure](../02_Core_Concepts/03_Graph_Structure.md) - WorkflowExecution schema
- [Creating Templates](../07_Development/02_Creating_Templates.md) - Template development guide

---
*Last Updated: 2025-10-24 | [Report Issues](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues)*
