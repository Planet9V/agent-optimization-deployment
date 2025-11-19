---
title: Code Analysis Incarnation (Part 1 of 2)
category: 03_Incarnations
last_updated: 2025-10-25
line_count: 444
status: published
tags: [neocoder, mcp, documentation]
---


# Code Analysis Incarnation

[← Back to Knowledge Graph](03_Knowledge_Graph.md) | [Next: Other Incarnations →](05_Other_Incarnations.md)

## Overview

The **Code Analysis Incarnation** provides AST (Abstract Syntax Tree) and ASG (Abstract Semantic Graph) analysis capabilities for understanding code structure, dependencies, and complexity metrics.

**Incarnation Type**: `code_analysis`
**Version**: 1.0.0
**Primary Use Cases**: Code structure analysis, dependency mapping, complexity metrics, refactoring support

## Core Capabilities

### AST/ASG Analysis
- Parse code into Abstract Syntax Trees
- Build Abstract Semantic Graphs
- Analyze code structure and patterns
- Extract code entities and relationships

### Dependency Analysis
- Map function call graphs
- Track import dependencies
- Identify circular dependencies
- Analyze coupling and cohesion

### Complexity Metrics
- Calculate cyclomatic complexity
- Measure cognitive complexity
- Identify code hotspots
- Track complexity trends

### Code Entity Extraction
- Identify classes, functions, methods
- Extract code documentation
- Map inheritance hierarchies
- Track code modifications

## Schema

### Node Types

**CodeEntity**:
```cypher
CREATE (entity:CodeEntity {
  id: randomUUID(),
  type: 'class',
  name: 'AuthService',
  filePath: 'src/auth/service.py',
  startLine: 10,
  endLine: 150,
  complexity: 8,
  docstring: 'Authentication service class',
  signature: 'class AuthService(BaseService)',
  created: datetime()
})
```

**FunctionNode**:
```cypher
CREATE (func:FunctionNode {
  id: randomUUID(),
  name: 'login',
  signature: 'def login(username: str, password: str) -> Token',
  returnType: 'Token',
  parameters: ['username', 'password'],
  parameterTypes: ['str', 'str'],
  complexity: 5,
  lineCount: 25,
  docstring: 'Authenticate user and return token'
})
```

**ClassNode**:
```cypher
CREATE (class:ClassNode {
  id: randomUUID(),
  name: 'UserManager',
  baseClasses: ['BaseManager'],
  methods: ['create_user', 'delete_user', 'update_user'],
  attributes: ['db', 'cache'],
  isAbstract: false
})
```

### Relationships

**Code Structure**:
```cypher
// File defines code entity
(file:File)-[:DEFINES]->(entity:CodeEntity)

// Class inheritance
(child:ClassNode)-[:INHERITS]->(parent:ClassNode)

// Function calls
(caller:FunctionNode)-[:CALLS]->(callee:FunctionNode)

// Module imports
(file:File)-[:IMPORTS]->(module:File)

// Method ownership
(class:ClassNode)-[:HAS_METHOD]->(method:FunctionNode)
```

## Available Tools

### analyze_code_structure

Parses code and creates AST/ASG representation in Neo4j.

**Signature**:
```python
async def analyze_code_structure(
    file_path: str,
    analysis_depth: int = 3,
    include_ast: bool = True,
    include_metrics: bool = True
) -> dict
```

**Parameters**:
- `file_path` (string, required) - File to analyze
- `analysis_depth` (int, optional) - AST traversal depth (1-5)
- `include_ast` (bool, optional) - Include full AST
- `include_metrics` (bool, optional) - Calculate complexity metrics

**Returns**:
```json
{
  "success": true,
  "file_path": "src/auth.py",
  "entities": [
    {
      "type": "class",
      "name": "AuthService",
      "complexity": 8,
      "methods": 5
    }
  ],
  "metrics": {
    "total_lines": 150,
    "code_lines": 120,
    "comment_lines": 20,
    "complexity": 15
  }
}
```

**Example**:
```python
result = await analyze_code_structure(
    file_path="src/auth/service.py",
    analysis_depth=3,
    include_metrics=True
)
```

### create_code_entity

Creates a code entity node from analysis results.

**Signature**:
```python
async def create_code_entity(
    entity_type: str,
    name: str,
    file_path: str,
    start_line: int,
    end_line: int,
    complexity: int = None,
    signature: str = None
) -> dict
```

### find_dependencies

Maps code dependencies and function call graphs.

**Signature**:
```python
async def find_dependencies(
    file_path: str = None,
    entity_name: str = None,
    dependency_type: str = None,
    max_depth: int = 3
) -> dict
```

**Parameters**:
- `file_path` (string, optional) - Scope to file
- `entity_name` (string, optional) - Specific entity
- `dependency_type` (string, optional) - IMPORTS, CALLS, INHERITS
- `max_depth` (int, optional) - Traversal depth

**Returns**:
```json
{
  "success": true,
  "dependencies": [
    {
      "source": "login_function",
      "target": "validate_credentials",
      "type": "CALLS",
      "file": "src/auth.py"
    }
  ],
  "dependency_graph": {...}
}
```

### calculate_complexity

Computes code complexity metrics.

**Signature**:
```python
async def calculate_complexity(
    file_path: str = None,
    entity_id: str = None,
    metric_types: list[str] = None
) -> dict
```

**Metric Types**:
- `cyclomatic` - Cyclomatic complexity
- `cognitive` - Cognitive complexity
- `maintainability` - Maintainability index
- `halstead` - Halstead metrics

**Returns**:
```json
{
  "success": true,
  "file_path": "src/auth.py",
  "metrics": {
    "cyclomatic": 15,
    "cognitive": 22,
    "maintainability": 65,
    "lines_of_code": 150
  },
  "hotspots": [
    {
      "entity": "login",
      "complexity": 12,
      "recommendation": "Consider refactoring"
    }
  ]
}
```

## Common Workflows

### Code Structure Analysis Workflow

```python
# 1. Analyze code structure
analysis = await analyze_code_structure(
    file_path="src/auth/service.py",
    analysis_depth=3,
    include_metrics=True
)

# 2. Create entities in graph
for entity in analysis["entities"]:
    await create_code_entity(
        entity_type=entity["type"],
        name=entity["name"],
        file_path="src/auth/service.py",
        start_line=entity["start_line"],
        end_line=entity["end_line"],
        complexity=entity["complexity"],
        signature=entity["signature"]
    )

# 3. Map dependencies
dependencies = await find_dependencies(
    file_path="src/auth/service.py",
    dependency_type="CALLS",
    max_depth=2
)

# 4. Calculate complexity metrics
metrics = await calculate_complexity(
    file_path="src/auth/service.py",
    metric_types=["cyclomatic", "cognitive", "maintainability"]
)

# 5. Identify refactoring candidates
if metrics["metrics"]["cyclomatic"] > 10:
    print("High complexity - consider refactoring")
    for hotspot in metrics["hotspots"]:
        print(f"  - {hotspot['entity']}: complexity {hotspot['complexity']}")
```

### Dependency Analysis Workflow

```python
# 1. Find all function calls from a specific function
calls = await find_dependencies(
    entity_name="login",
    dependency_type="CALLS",
    max_depth=3
)

# 2. Find all imports in a file
imports = await find_dependencies(
    file_path="src/auth/service.py",
    dependency_type="IMPORTS"
)

# 3. Identify circular dependencies
circular = await query_cypher("""
    MATCH path = (a:FunctionNode)-[:CALLS*2..5]->(a)
    RETURN [node IN nodes(path) | node.name] as cycle
""")

# 4. Analyze coupling
coupling = await query_cypher("""
    MATCH (f:File)-[r:IMPORTS]->(m:File)
    RETURN f.path as file,
           count(r) as import_count,
           collect(m.path) as imported_modules
    ORDER BY import_count DESC
""")
```

## Cypher Query Patterns

### Code Entity Queries

**Find Complex Functions**:
```cypher
MATCH (f:File)-[:DEFINES]->(entity:CodeEntity)
WHERE entity.complexity > $threshold
RETURN f.path as file,
       entity.name as name,
       entity.type as type,
       entity.complexity as complexity
ORDER BY entity.complexity DESC
LIMIT 20
```

**Get Class Hierarchy**:
```cypher
MATCH path = (child:ClassNode)-[:INHERITS*1..5]->(parent:ClassNode)
WHERE child.name = $class_name
RETURN [node IN nodes(path) | node.name] as inheritance_chain,
       length(path) as depth
```

### Dependency Queries

**Function Call Graph**:
```cypher
MATCH (func:FunctionNode {name: $function_name})
MATCH path = (func)-[:CALLS*1..3]->(dependency:FunctionNode)
RETURN path,
       [node IN nodes(path) | node.name] as call_chain,
       length(path) as depth
ORDER BY depth
```

**Import Dependencies**:
```cypher
MATCH (f:File {path: $file_path})
MATCH (f)-[:IMPORTS]->(imported:File)
RETURN imported.path as module,
       count(*) as import_count
ORDER BY import_count DESC
```

### Complexity Analysis

**Complexity Hotspots**:
```cypher
MATCH (entity:CodeEntity)
WHERE entity.complexity IS NOT NULL
RETURN entity.type as type,
       avg(entity.complexity) as avg_complexity,
       max(entity.complexity) as max_complexity,
       count(entity) as count
ORDER BY avg_complexity DESC
```

**File-Level Metrics**:
```cypher
MATCH (f:File)-[:DEFINES]->(entity:CodeEntity)
RETURN f.path as file,
       count(entity) as entity_count,
       sum(entity.complexity) as total_complexity,
       avg(entity.complexity) as avg_complexity
ORDER BY total_complexity DESC
```

## Best Practices

### Analysis Configuration

**Depth Selection**:
- Depth 1-2: Quick structure overview
- Depth 3: Balanced analysis (recommended)
- Depth 4-5: Deep analysis (performance impact)

**Metric Selection**:
- Use cyclomatic for control flow complexity
- Use cognitive for readability assessment
- Use maintainability for overall code health
- Combine metrics for comprehensive view

### Performance Optimization

**Batch Analysis**:
```python
# Good: Analyze multiple files in batch
files = ["file1.py", "file2.py", "file3.py"]
await analyze_files_batch(files)

# Avoid: Sequential single-file analysis
for file in files:
    await analyze_code_structure(file)
```

**Incremental Updates**:
```python
# Only re-analyze modified files
modified_files = get_modified_files()
for file in modified_files:
    await analyze_code_structure(file)
```

### Code Quality

**Complexity Thresholds**:
- Cyclomatic < 10: Good
- Cyclomatic 10-20: Moderate
- Cyclomatic > 20: High (refactor recommended)

**Maintainability Targets**:
- MI > 85: High maintainability
- MI 65-85: Moderate
- MI < 65: Low (improvement needed)
