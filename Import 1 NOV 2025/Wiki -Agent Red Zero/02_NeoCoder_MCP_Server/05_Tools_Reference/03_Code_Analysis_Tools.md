---
title: Code Analysis Tools Reference
category: 05_Tools_Reference
last_updated: 2025-10-25
line_count: 485
status: published
tags: [neocoder, mcp, documentation]
---

# Code Analysis Tools Reference

[← Back to Knowledge Graph Tools](02_Knowledge_Graph_Tools.md) | [Next: Specialized Tools →](04_Specialized_Tools.md)

## Overview

Code Analysis tools provide AST (Abstract Syntax Tree) and ASG (Abstract Semantic Graph) analysis capabilities. Available in the `code_analysis` incarnation.

## Code Structure Analysis

### analyze_code_structure

Parses code and creates AST/ASG representation.

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
- `file_path` - File to analyze
- `analysis_depth` - AST traversal depth (1-5)
- `include_ast` - Include full AST structure
- `include_metrics` - Calculate complexity metrics

**Returns**:
```json
{
  "success": true,
  "file_path": "src/auth.py",
  "entities": [
    {
      "type": "class",
      "name": "AuthService",
      "start_line": 10,
      "end_line": 150,
      "complexity": 8,
      "methods": ["login", "logout", "verify_token"]
    }
  ],
  "metrics": {
    "total_lines": 150,
    "code_lines": 120,
    "comment_lines": 20,
    "blank_lines": 10,
    "cyclomatic_complexity": 15,
    "cognitive_complexity": 22
  }
}
```

**Example**:
```python
analysis = await analyze_code_structure(
    file_path="src/auth/service.py",
    analysis_depth=3,
    include_metrics=True
)

# Access results
for entity in analysis["entities"]:
    print(f"{entity['type']}: {entity['name']} (complexity: {entity['complexity']})")
```

---

### create_code_entity

Creates code entity node from analysis results.

**Signature**:
```python
async def create_code_entity(
    entity_type: str,
    name: str,
    file_path: str,
    start_line: int,
    end_line: int,
    complexity: int | None = None,
    signature: str | None = None,
    docstring: str | None = None
) -> dict
```

**Entity Types**:
- `class` - Class definition
- `function` - Function or method
- `module` - Python module
- `interface` - Interface definition
- `enum` - Enumeration

**Example**:
```python
entity = await create_code_entity(
    entity_type="class",
    name="AuthService",
    file_path="src/auth/service.py",
    start_line=10,
    end_line=150,
    complexity=8,
    signature="class AuthService(BaseService)",
    docstring="Authentication service for user management"
)
```

---

## Dependency Analysis

### find_dependencies

Maps code dependencies and call graphs.

**Signature**:
```python
async def find_dependencies(
    file_path: str | None = None,
    entity_name: str | None = None,
    dependency_type: str | None = None,
    max_depth: int = 3
) -> dict
```

**Parameters**:
- `file_path` - Scope to specific file
- `entity_name` - Specific entity to analyze
- `dependency_type` - IMPORTS, CALLS, INHERITS, or None (all)
- `max_depth` - Traversal depth

**Returns**:
```json
{
  "success": true,
  "dependencies": [
    {
      "source": "AuthService.login",
      "target": "TokenService.create_token",
      "type": "CALLS",
      "file": "src/auth/service.py",
      "line": 45
    }
  ],
  "dependency_graph": {
    "nodes": [...],
    "edges": [...]
  }
}
```

**Example**:
```python
# Find all dependencies for a file
deps = await find_dependencies(
    file_path="src/auth/service.py",
    max_depth=2
)

# Find function calls
calls = await find_dependencies(
    entity_name="login",
    dependency_type="CALLS",
    max_depth=3
)

# Find imports
imports = await find_dependencies(
    file_path="src/auth/service.py",
    dependency_type="IMPORTS"
)
```

---

### analyze_imports

Analyzes module import structure.

**Signature**:
```python
async def analyze_imports(
    file_path: str
) -> dict
```

**Returns**: List of imported modules with metadata

---

### find_call_graph

Builds function call graph.

**Signature**:
```python
async def find_call_graph(
    start_function: str,
    max_depth: int = 3
) -> dict
```

**Returns**: Call graph starting from specified function

---

## Complexity Metrics

### calculate_complexity

Computes code complexity metrics.

**Signature**:
```python
async def calculate_complexity(
    file_path: str | None = None,
    entity_id: str | None = None,
    metric_types: list[str] | None = None
) -> dict
```

**Metric Types**:
- `cyclomatic` - Cyclomatic complexity (control flow)
- `cognitive` - Cognitive complexity (readability)
- `maintainability` - Maintainability index
- `halstead` - Halstead complexity measures

**Returns**:
```json
{
  "success": true,
  "file_path": "src/auth.py",
  "metrics": {
    "cyclomatic": 15,
    "cognitive": 22,
    "maintainability": 65,
    "halstead": {
      "volume": 450.5,
      "difficulty": 12.3,
      "effort": 5541.15
    },
    "lines_of_code": 150
  },
  "hotspots": [
    {
      "entity": "login",
      "complexity": 12,
      "recommendation": "Consider refactoring - high complexity"
    }
  ]
}
```

**Example**:
```python
# Calculate all metrics for file
metrics = await calculate_complexity(
    file_path="src/auth.py",
    metric_types=["cyclomatic", "cognitive", "maintainability"]
)

# Check if refactoring needed
if metrics["metrics"]["cyclomatic"] > 10:
    print("High complexity - refactoring recommended")
    for hotspot in metrics["hotspots"]:
        print(f"  - {hotspot['entity']}: {hotspot['complexity']}")
```

---

### identify_hotspots

Identifies code areas with high complexity.

**Signature**:
```python
async def identify_hotspots(
    project_id: str,
    threshold: int = 10,
    metric: str = "cyclomatic"
) -> dict
```

**Returns**: List of high-complexity code entities

---

## Code Pattern Detection

### detect_patterns

Identifies common code patterns and anti-patterns.

**Signature**:
```python
async def detect_patterns(
    file_path: str,
    pattern_types: list[str] | None = None
) -> dict
```

**Pattern Types**:
- `design_patterns` - Design patterns (Singleton, Factory, etc.)
- `anti_patterns` - Code smells and anti-patterns
- `security_patterns` - Security vulnerabilities
- `performance_patterns` - Performance issues

**Returns**:
```json
{
  "success": true,
  "patterns": [
    {
      "type": "singleton",
      "location": "src/auth.py:45",
      "confidence": 0.85
    }
  ],
  "anti_patterns": [
    {
      "type": "god_class",
      "entity": "AuthService",
      "severity": "medium",
      "recommendation": "Split into smaller classes"
    }
  ]
}
```

---

## Refactoring Support

### suggest_refactorings

Suggests refactoring opportunities.

**Signature**:
```python
async def suggest_refactorings(
    file_path: str | None = None,
    entity_id: str | None = None
) -> dict
```

**Returns**:
```json
{
  "success": true,
  "suggestions": [
    {
      "type": "extract_method",
      "target": "AuthService.login",
      "rationale": "Long method with multiple responsibilities",
      "impact": "medium",
      "complexity_reduction": 5
    }
  ]
}
```

---

### extract_method_candidates

Identifies code blocks suitable for extraction.

**Signature**:
```python
async def extract_method_candidates(
    function_id: str,
    min_lines: int = 5
) -> dict
```

---

## Integration Tools

### link_code_to_knowledge

Links code entities to knowledge graph concepts.

**Signature**:
```python
async def link_code_to_knowledge(
    code_entity_id: str,
    knowledge_entity_id: str,
    relationship_type: str = "IMPLEMENTS"
) -> dict
```

**Example**:
```python
# Link code implementation to design pattern
await link_code_to_knowledge(
    code_entity_id="auth-service-class-uuid",
    knowledge_entity_id="singleton-pattern-uuid",
    relationship_type="IMPLEMENTS"
)
```

---

## Best Practices

### Analysis Configuration

**Choose appropriate depth**:
```python
# Quick overview - depth 1
await analyze_code_structure(file_path, analysis_depth=1)

# Balanced analysis - depth 3 (recommended)
await analyze_code_structure(file_path, analysis_depth=3)

# Deep analysis - depth 5 (expensive)
await analyze_code_structure(file_path, analysis_depth=5)
```

**Select relevant metrics**:
```python
# For code review
await calculate_complexity(file_path, metric_types=["cyclomatic", "cognitive"])

# For maintainability assessment
await calculate_complexity(file_path, metric_types=["maintainability"])

# Comprehensive analysis
await calculate_complexity(file_path, metric_types=["cyclomatic", "cognitive", "maintainability", "halstead"])
```

### Performance Optimization

**Batch analysis**:
```python
# Good: Analyze multiple files in batch
files = ["file1.py", "file2.py", "file3.py"]
results = await asyncio.gather(*[
    analyze_code_structure(f) for f in files
])

# Avoid: Sequential analysis
for file in files:
    await analyze_code_structure(file)
```

**Incremental updates**:
```python
# Only re-analyze modified files
modified = get_modified_files()
for file in modified:
    await analyze_code_structure(file)
```

### Quality Thresholds

**Cyclomatic Complexity**:
- < 10: Good
- 10-20: Moderate (review recommended)
- > 20: High (refactoring recommended)

**Maintainability Index**:
- > 85: High maintainability
- 65-85: Moderate maintainability
- < 65: Low maintainability (improvement needed)

**Cognitive Complexity**:
- < 15: Easy to understand
- 15-30: Moderate complexity
- > 30: Difficult to understand

## Related Documentation

- [Core Tools](01_Core_Tools.md) - Foundation tools
- [Code Analysis Incarnation](../03_Incarnations/04_Code_Analysis.md) - Detailed guide
- [Graph Structure](../02_Core_Concepts/03_Graph_Structure.md) - Schema for code entities
- [Workflows](../04_Workflows/02_Core_Templates.md) - CODE_ANALYZE template

---
*Last Updated: 2025-10-24 | [Report Issues](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues)*
