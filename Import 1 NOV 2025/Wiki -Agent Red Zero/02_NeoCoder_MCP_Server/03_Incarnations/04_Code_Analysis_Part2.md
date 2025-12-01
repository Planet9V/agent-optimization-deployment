---
title: 1. Coding incarnation: Create project and add files (Part 2 of 2)
category: 03_Incarnations
last_updated: 2025-10-25
line_count: 52
status: published
tags: [neocoder, mcp, documentation]
---

## Integration with Other Incarnations

### Coding + Code Analysis

```python
# 1. Coding incarnation: Create project and add files
await switch_incarnation("coding")
project = await create_project(name="MyProject", root_path="/src")
await add_file_to_project(project_id, "src/auth.py")

# 2. Code Analysis incarnation: Analyze structure
await switch_incarnation("code_analysis")
analysis = await analyze_code_structure("src/auth.py")

# 3. Query combined data
result = await query_cypher("""
    MATCH (p:Project)-[:HAS_FILE]->(f:File)
    MATCH (f)-[:DEFINES]->(entity:CodeEntity)
    WHERE p.id = $project_id
    RETURN f.path, entity.name, entity.complexity
""")
```

### Code Analysis + Knowledge Graph

```python
# 1. Analyze code to extract patterns
analysis = await analyze_code_structure("src/patterns.py")

# 2. Switch to knowledge graph to document patterns
await switch_incarnation("knowledge_graph")
await create_knowledge_entity(
    name="Repository Pattern",
    entity_type="design_pattern",
    description="Data access abstraction pattern",
    properties={
        "implementation": "src/patterns.py:RepositoryBase",
        "complexity": analysis["entities"][0]["complexity"]
    }
)
```

## Related Documentation

- [Overview](01_Overview.md) - Incarnation system
- [Coding](02_Coding.md) - Project management
- [Graph Structure](../02_Core_Concepts/03_Graph_Structure.md) - Schema details
- [Tools Reference](../05_Tools_Reference/03_Code_Analysis_Tools.md) - Complete tools

---
*Last Updated: 2025-10-24 | [Report Issues](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues)*
