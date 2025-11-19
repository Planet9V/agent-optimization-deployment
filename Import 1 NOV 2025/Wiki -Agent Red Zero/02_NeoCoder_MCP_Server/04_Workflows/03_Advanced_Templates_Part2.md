---
title: 03_Advanced_Templates_Part1 (Part 2 of 2)
category: 04_Workflows
last_updated: 2025-10-25
line_count: 88
status: published
tags: [neocoder, mcp, documentation]
---

## Performance Optimization Patterns

### Batch with Limits

**Pattern**: Process large datasets in manageable chunks

```cypher
// Process files in batches of 10
MATCH (p:Project {id: $project_id})-[:HAS_FILE]->(f:File)
WHERE NOT EXISTS((f)<-[:EXECUTED_ON]-(:WorkflowExecution {templateKeyword: 'ANALYZE'}))
WITH f
LIMIT 10

CREATE (exec:WorkflowExecution {
  id: randomUUID(),
  templateKeyword: 'ANALYZE',
  status: 'pending',
  batch_number: $batch_number
})
CREATE (exec)-[:EXECUTED_ON]->(f)

RETURN count(exec) as files_in_batch
```

### Parallel Execution

**Pattern**: Execute independent workflows concurrently

```python
import asyncio

async def parallel_workflow_execution(workflows):
    """Execute multiple workflows in parallel."""
    tasks = [
        execute_workflow(wf["keyword"], wf["parameters"])
        for wf in workflows
    ]
    results = await asyncio.gather(*tasks)
    return results

# Usage
workflows = [
    {"keyword": "CODE_ANALYZE", "parameters": {"file_path": "file1.py"}},
    {"keyword": "CODE_ANALYZE", "parameters": {"file_path": "file2.py"}},
    {"keyword": "CODE_ANALYZE", "parameters": {"file_path": "file3.py"}}
]

results = await parallel_workflow_execution(workflows)
```

---

## Best Practices

### Template Composition

**Do**: Break complex workflows into reusable templates
```python
# Good: Modular templates
BUILD → TEST → DEPLOY

# Avoid: Monolithic template
BUILD_TEST_DEPLOY_ALL_IN_ONE
```

### Error Handling

**Do**: Implement graceful degradation
```cypher
// Attempt operation with fallback
OPTIONAL MATCH (target) WHERE target.id = $id
FOREACH (x IN CASE WHEN target IS NULL THEN [1] ELSE [] END |
  CREATE (fallback:Entity {id: $id, created_by: 'fallback'})
)
```

### State Management

**Do**: Track workflow state explicitly
```cypher
CREATE (workflow:WorkflowExecution {
  state: 'pending',
  substates: ['initialized', 'validated', 'executing', 'finalizing'],
  current_substate: 'initialized',
  progress: 0.0
})
```
