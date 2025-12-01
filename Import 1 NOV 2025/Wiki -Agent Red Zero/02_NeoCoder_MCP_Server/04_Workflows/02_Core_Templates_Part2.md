---
title: Core Workflow Templates (Part 2)
category: 04_Workflows
last_updated: 2025-10-25
line_count: 145
status: published
tags: [neocoder, mcp, documentation]
---

## Template Usage Patterns

### Sequential Workflow

```python
# 1. Analyze code
analysis = await execute_workflow(
    template_keyword="CODE_ANALYZE",
    parameters={"file_path": "src/auth.py"}
)

# 2. Fix identified issues
if analysis["results"]["issues"]:
    fix = await execute_workflow(
        template_keyword="FIX",
        parameters={
            "file_path": "src/auth.py",
            "issue_description": analysis["results"]["issues"][0]
        }
    )

# 3. Refactor improved code
refactor = await execute_workflow(
    template_keyword="REFACTOR",
    parameters={
        "file_path": "src/auth.py",
        "refactor_goal": "Simplify authentication logic"
    }
)

# 4. Build and test
build = await execute_workflow(
    template_keyword="BUILD",
    parameters={
        "project_id": "proj-123",
        "run_tests": true
    }
)
```

### Parallel Workflow

```python
import asyncio

# Execute multiple analyses in parallel
results = await asyncio.gather(
    execute_workflow("CODE_ANALYZE", {"file_path": "file1.py"}),
    execute_workflow("CODE_ANALYZE", {"file_path": "file2.py"}),
    execute_workflow("CODE_ANALYZE", {"file_path": "file3.py"})
)
```

### Conditional Workflow

```cypher
// Execute deployment only if build succeeds
MATCH (build:WorkflowExecution {templateKeyword: 'BUILD'})
WHERE build.status = 'completed'
  AND build.results.all_tests_passed = true

WITH build
CREATE (deploy:WorkflowExecution {
  id: randomUUID(),
  templateKeyword: 'DEPLOY',
  status: 'pending',
  startTime: datetime()
})
CREATE (deploy)-[:DEPENDS_ON]->(build)
RETURN deploy
```

## Best Practices

### Parameter Validation

Always validate parameters before execution:

```python
def validate_fix_parameters(params):
    required = ["file_path", "issue_description"]
    for req in required:
        if req not in params:
            raise ValueError(f"Missing required parameter: {req}")

    if params.get("fix_type") not in ["bug", "typo", "logic", "performance", None]:
        raise ValueError("Invalid fix_type")

    return True
```

### Result Handling

Store comprehensive execution results:

```cypher
SET exec.status = 'completed',
    exec.endTime = datetime(),
    exec.results = {
      success: true,
      entities_modified: 3,
      files_changed: ['src/auth.py'],
      metrics: {
        lines_changed: 45,
        complexity_before: 15,
        complexity_after: 8
      },
      verification: {
        tests_passed: true,
        lint_passed: true
      }
    }
```

### Error Recovery

Implement error handling in templates:

```cypher
// Attempt operation
OPTIONAL MATCH (target:File {path: $file_path})
WITH target
FOREACH (ignoreMe IN CASE WHEN target IS NULL THEN [1] ELSE [] END |
  CREATE (exec:WorkflowExecution {
    status: 'failed',
    error: 'File not found: ' + $file_path
  })
)

// Proceed only if target exists
WITH target
WHERE target IS NOT NULL
// ... continue workflow
```

## Related Documentation

- [Template Overview](01_Template_Overview.md) - Template architecture
- [Advanced Templates](03_Advanced_Templates.md) - Complex patterns
- [Tools Reference](../05_Tools_Reference/01_Core_Tools.md) - Tool documentation
- [Creating Templates](../07_Development/02_Creating_Templates.md) - Template development

---
*Last Updated: 2025-10-24 | [Report Issues](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues)*
