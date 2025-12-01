---
title: 04_Specialized_Tools_Part1 (Part 2 of 2)
category: 05_Tools_Reference
last_updated: 2025-10-25
line_count: 98
status: published
tags: [neocoder, mcp, documentation]
---

## Advanced Cypher Tools

### execute_parameterized_query

Executes Cypher with parameter validation.

**Signature**:
```python
async def execute_parameterized_query(
    query: str,
    parameters: dict,
    validate: bool = True
) -> dict
```

**Example**:
```python
result = await execute_parameterized_query("""
    MATCH (p:Project)-[:HAS_FILE]->(f:File)
    WHERE p.id = $project_id
      AND f.extension IN $extensions
    RETURN f.path as file, f.size as size
    ORDER BY f.size DESC
    LIMIT $limit
""", {
    "project_id": "proj-123",
    "extensions": ["py", "js", "ts"],
    "limit": 10
})
```

---

### batch_cypher_execution

Executes multiple Cypher queries in transaction.

**Signature**:
```python
async def batch_cypher_execution(
    queries: list[dict]
) -> dict
```

**Query Format**:
```json
{
  "queries": [
    {"query": "CREATE (n:Node {id: $id})", "parameters": {"id": 1}},
    {"query": "CREATE (n:Node {id: $id})", "parameters": {"id": 2}}
  ]
}
```

---

### optimize_query

Analyzes and optimizes Cypher query.

**Signature**:
```python
async def optimize_query(
    query: str
) -> dict
```

**Returns**:
```json
{
  "original_query": "...",
  "optimized_query": "...",
  "improvements": [
    "Added index hint",
    "Reordered MATCH clauses",
    "Removed redundant OPTIONAL MATCH"
  ],
  "estimated_speedup": "3x"
}
```

---

### explain_query

Explains query execution plan.

**Signature**:
```python
async def explain_query(
    query: str
) -> dict
```

**Returns**: Query execution plan with estimated rows and operations

---
