---
title: 02_Creating_Templates_Part1 (Part 2 of 2)
category: 07_Development
last_updated: 2025-10-25
line_count: 47
status: published
tags: [neocoder, mcp, documentation]
---

## Best Practices

### Design Principles

**Atomic Operations**:
```cypher
// Good: Single clear purpose
MATCH (p:Project {id: $project_id})
CREATE (f:File {path: $file_path})
CREATE (p)-[:HAS_FILE]->(f)

// Avoid: Multiple unrelated operations
MATCH (p:Project {id: $project_id})
CREATE (f:File {path: $file_path})
CREATE (k:KnowledgeEntity {name: $entity_name})  // Unrelated
```

**Idempotency**:
```cypher
// Idempotent: MERGE instead of CREATE
MERGE (p:Project {id: $project_id})
ON CREATE SET p.created = datetime()
ON MATCH SET p.updated = datetime()

// Not idempotent: Multiple executions create duplicates
CREATE (p:Project {id: $project_id})
```

**Error Recovery**:
```cypher
// Include rollback in template
MATCH (exec:WorkflowExecution {id: $exec_id})
WHERE exec.status = 'failed'

// Cleanup partial execution
MATCH (exec)-[:CREATED]->(node)
DETACH DELETE node

SET exec.status = 'rolled_back',
    exec.rolled_back_at = datetime()
```

### Documentation Standards

```markdown
# Template Documentation Format
