---
title: Advanced Workflow Templates (Part 1 of 2)
category: 04_Workflows
last_updated: 2025-10-25
line_count: 428
status: published
tags: [neocoder, mcp, documentation]
---


# Advanced Workflow Templates

[← Back to Core Templates](02_Core_Templates.md) | [Next: Tools Reference →](../05_Tools_Reference/01_Core_Tools.md)

## Overview

Advanced templates demonstrate complex workflow patterns including composition, conditional execution, parallel processing, and cross-incarnation coordination.

## Composite Templates

### Multi-Step Deployment

**Pattern**: Chain multiple templates for complex workflows

```python
{
  "keyword": "FULL_DEPLOYMENT",
  "description": "Complete build, test, and deployment workflow",
  "cypher": """
    // Step 1: Build project
    CREATE (build:WorkflowExecution {
      id: randomUUID(),
      templateKeyword: 'BUILD',
      status: 'pending',
      parameters: $build_params
    })

    // Step 2: Run tests (depends on build)
    CREATE (test:WorkflowExecution {
      id: randomUUID(),
      templateKeyword: 'RUN_TESTS',
      status: 'pending',
      parameters: $test_params
    })
    CREATE (test)-[:DEPENDS_ON]->(build)

    // Step 3: Deploy (depends on tests)
    CREATE (deploy:WorkflowExecution {
      id: randomUUID(),
      templateKeyword: 'DEPLOY',
      status: 'pending',
      parameters: $deploy_params
    })
    CREATE (deploy)-[:DEPENDS_ON]->(test)

    RETURN build, test, deploy
  """,
  "parameters": {
    "build_params": "object",
    "test_params": "object",
    "deploy_params": "object"
  }
}
```

**Usage**:
```python
result = await execute_workflow(
    template_keyword="FULL_DEPLOYMENT",
    parameters={
        "build_params": {"project_id": "proj-123", "build_type": "production"},
        "test_params": {"suite": "integration"},
        "deploy_params": {"environment": "production"}
    }
)
```

---

## Conditional Templates

### Smart Refactoring

**Pattern**: Execute different logic based on conditions

```python
{
  "keyword": "SMART_REFACTOR",
  "description": "Refactor only if complexity exceeds threshold",
  "cypher": """
    // Analyze code complexity
    MATCH (f:File {path: $file_path})
    OPTIONAL MATCH (f)-[:DEFINES]->(entity:CodeEntity)

    // Calculate average complexity
    WITH f, avg(entity.complexity) as avg_complexity

    // Only refactor if complexity is high
    FOREACH (ignoreMe IN CASE WHEN avg_complexity > $threshold THEN [1] ELSE [] END |
      CREATE (refactor:WorkflowExecution {
        id: randomUUID(),
        templateKeyword: 'REFACTOR',
        status: 'pending',
        startTime: datetime(),
        parameters: {
          file_path: $file_path,
          refactor_goal: 'Reduce complexity from ' + toString(avg_complexity)
        }
      })
      CREATE (refactor)-[:EXECUTED_ON]->(f)
    )

    RETURN avg_complexity, avg_complexity > $threshold as should_refactor
  """,
  "parameters": {
    "file_path": "string",
    "threshold": "number"
  }
}
```

---

## Batch Processing Templates

### Multi-File Analysis

**Pattern**: Process multiple entities in parallel

```python
{
  "keyword": "BATCH_ANALYZE",
  "description": "Analyze multiple files in batch",
  "cypher": """
    // Get all files matching pattern
    MATCH (p:Project {id: $project_id})-[:HAS_FILE]->(f:File)
    WHERE f.extension = $file_extension

    // Create analysis execution for each file
    WITH collect(f) as files
    UNWIND files as file
    CREATE (exec:WorkflowExecution {
      id: randomUUID(),
      templateKeyword: 'CODE_ANALYZE',
      status: 'pending',
      startTime: datetime(),
      parameters: {
        file_path: file.path,
        analysis_depth: $analysis_depth
      }
    })
    CREATE (exec)-[:EXECUTED_ON]->(file)

    RETURN count(exec) as executions_created
  """,
  "parameters": {
    "project_id": "string",
    "file_extension": "string",
    "analysis_depth": "integer"
  }
}
```

**Usage**:
```python
# Analyze all Python files in project
result = await execute_workflow(
    template_keyword="BATCH_ANALYZE",
    parameters={
        "project_id": "proj-123",
        "file_extension": "py",
        "analysis_depth": 3
    }
)
```

---

## Cross-Incarnation Templates

### Code to Knowledge

**Pattern**: Coordinate multiple incarnations for complex tasks

```python
{
  "keyword": "CODE_TO_KNOWLEDGE",
  "description": "Extract knowledge from code and build knowledge graph",
  "workflow": """
    1. Switch to code_analysis incarnation
    2. Analyze code structure
    3. Switch to knowledge_graph incarnation
    4. Extract design patterns
    5. Create knowledge entities
    6. Link to code entities
  """,
  "cypher": """
    // Step 1: Analyze code (code_analysis incarnation)
    MATCH (f:File {path: $file_path})
    OPTIONAL MATCH (f)-[:DEFINES]->(entity:CodeEntity)

    // Step 2: Extract patterns from code
    WITH f, collect(entity) as code_entities
    UNWIND code_entities as ce
    WHERE ce.type = 'class'

    // Step 3: Create knowledge entities (knowledge_graph incarnation)
    CREATE (knowledge:KnowledgeEntity {
      id: randomUUID(),
      type: 'design_pattern',
      name: 'Pattern from ' + ce.name,
      description: 'Extracted from code analysis',
      domain: 'software_engineering',
      properties: {
        source_file: f.path,
        source_entity: ce.name,
        complexity: ce.complexity
      }
    })

    // Step 4: Link knowledge to code
    CREATE (knowledge)-[:EXTRACTED_FROM]->(ce)
    CREATE (knowledge)-[:SOURCED_FROM]->(f)

    RETURN count(knowledge) as patterns_extracted
  """,
  "parameters": {
    "file_path": "string"
  }
}
```

---

## Iterative Templates

### Progressive Refactoring

**Pattern**: Iterative improvements until goal achieved

```python
{
  "keyword": "PROGRESSIVE_REFACTOR",
  "description": "Iteratively refactor until complexity target met",
  "cypher": """
    // Initial complexity check
    MATCH (f:File {path: $file_path})
    MATCH (f)-[:DEFINES]->(entity:CodeEntity)
    WITH f, max(entity.complexity) as current_complexity

    // Create iteration tracking
    CREATE (iteration:RefactorIteration {
      id: randomUUID(),
      file_path: $file_path,
      target_complexity: $target_complexity,
      current_complexity: current_complexity,
      iteration: 1,
      status: CASE WHEN current_complexity <= $target_complexity
                   THEN 'complete'
                   ELSE 'pending'
              END
    })

    // Schedule refactoring if needed
    WITH iteration
    WHERE iteration.status = 'pending'
    CREATE (refactor:WorkflowExecution {
      id: randomUUID(),
      templateKeyword: 'REFACTOR',
      status: 'pending',
      parameters: {
        file_path: $file_path,
        refactor_goal: 'Reduce complexity iteration 1'
      }
    })
    CREATE (refactor)-[:PART_OF]->(iteration)

    RETURN iteration
  """,
  "parameters": {
    "file_path": "string",
    "target_complexity": "number"
  }
}
```

---

## State Machine Templates

### Deployment Pipeline

**Pattern**: State-based workflow progression

```cypher
// Define states and transitions
CREATE (pipeline:DeploymentPipeline {
  id: randomUUID(),
  project_id: $project_id,
  current_state: 'pending',
  states: ['pending', 'building', 'testing', 'staging', 'production', 'rollback'],
  transitions: {
    pending: ['building'],
    building: ['testing', 'rollback'],
    testing: ['staging', 'rollback'],
    staging: ['production', 'rollback'],
    production: ['rollback'],
    rollback: ['pending']
  }
})

// Execute state transitions
MATCH (pipeline:DeploymentPipeline {id: $pipeline_id})
WHERE $next_state IN pipeline.transitions[pipeline.current_state]
SET pipeline.current_state = $next_state,
    pipeline.updated = datetime()

// Create execution for new state
CREATE (exec:WorkflowExecution {
  id: randomUUID(),
  templateKeyword: 'PIPELINE_STEP',
  status: 'running',
  state: $next_state,
  pipeline_id: $pipeline_id
})

RETURN pipeline, exec
```

---

## Event-Driven Templates

### Automated Response

**Pattern**: Trigger workflows based on events

```python
{
  "keyword": "AUTO_FIX_ON_FAILURE",
  "description": "Automatically attempt fix when tests fail",
  "cypher": """
    // Detect test failure
    MATCH (test:WorkflowExecution {templateKeyword: 'RUN_TESTS'})
    WHERE test.status = 'failed'
      AND test.endTime > datetime() - duration('PT5M')
      AND NOT EXISTS((test)<-[:TRIGGERED_BY]-(:WorkflowExecution))

    // Extract failed test information
    WITH test, test.results.failed_tests as failed_tests
    UNWIND failed_tests as failed_test

    // Create auto-fix execution
    CREATE (fix:WorkflowExecution {
      id: randomUUID(),
      templateKeyword: 'AUTO_FIX',
      status: 'pending',
      startTime: datetime(),
      parameters: {
        test_name: failed_test.name,
        error_message: failed_test.error,
        file_path: failed_test.file
      }
    })
    CREATE (fix)-[:TRIGGERED_BY]->(test)

    RETURN count(fix) as auto_fixes_created
  """,
  "parameters": {}
}
```

---

## Data Pipeline Templates

### ETL Workflow

**Pattern**: Extract, Transform, Load data pipeline

```python
{
  "keyword": "ETL_PIPELINE",
  "description": "Complete data pipeline from source to analysis",
  "cypher": """
    // Step 1: Extract - Register source dataset
    CREATE (source:Dataset {
      id: randomUUID(),
      name: $source_name,
      type: 'source',
      status: 'extracting'
    })

    // Step 2: Transform - Create transformation node
    CREATE (transform:Transformation {
      id: randomUUID(),
      name: $transform_name,
      type: $transform_type,
      logic: $transform_logic
    })
    CREATE (transform)-[:PROCESSES]->(source)

    // Step 3: Load - Create target dataset
    CREATE (target:Dataset {
      id: randomUUID(),
      name: $target_name,
      type: 'processed',
      status: 'loading'
    })
    CREATE (target)-[:DERIVED_FROM]->(transform)
    CREATE (target)-[:TRACES_TO]->(source)

    // Step 4: Create pipeline execution
    CREATE (pipeline:WorkflowExecution {
      id: randomUUID(),
      templateKeyword: 'ETL_PIPELINE',
      status: 'running',
      startTime: datetime()
    })
    CREATE (pipeline)-[:EXTRACTS]->(source)
    CREATE (pipeline)-[:TRANSFORMS]->(transform)
    CREATE (pipeline)-[:LOADS]->(target)

    RETURN pipeline, source, transform, target
  """,
  "parameters": {
    "source_name": "string",
    "transform_name": "string",
    "transform_type": "string",
    "transform_logic": "string",
    "target_name": "string"
  }
}
```

---
