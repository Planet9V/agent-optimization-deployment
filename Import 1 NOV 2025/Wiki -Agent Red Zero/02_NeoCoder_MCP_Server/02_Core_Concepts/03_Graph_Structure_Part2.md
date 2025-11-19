---
title: 03_Graph_Structure_Part1 (Part 2 of 2)
category: 02_Core_Concepts
last_updated: 2025-10-25
line_count: 95
status: published
tags: [neocoder, mcp, documentation]
---

## Common Query Patterns

### Project Structure Queries

**Get Complete Project Structure**:
```cypher
MATCH (p:Project {id: $project_id})
OPTIONAL MATCH (p)-[:HAS_DIRECTORY]->(dir:Directory)
OPTIONAL MATCH (dir)-[:CONTAINS*0..]->(subdir:Directory)
OPTIONAL MATCH (d:Directory)-[:CONTAINS]->(f:File)
WHERE d.id = dir.id OR d.id IN [sd IN collect(subdir) | sd.id]
RETURN p,
       collect(DISTINCT dir) as directories,
       collect(DISTINCT f) as files
```

**Get File with Context**:
```cypher
MATCH (f:File {id: $file_id})
OPTIONAL MATCH (f)-[:PARENT_DIR]->(dir:Directory)
OPTIONAL MATCH (f)<-[:HAS_FILE]-(proj:Project)
OPTIONAL MATCH (f)-[:DEFINES]->(entity:CodeEntity)
RETURN f, dir, proj, collect(entity) as entities
```

### Workflow History Queries

**Get Recent Workflow Executions**:
```cypher
MATCH (exec:WorkflowExecution)
WHERE exec.startTime > datetime() - duration('P7D')
OPTIONAL MATCH (exec)-[:USED_TEMPLATE]->(template:ActionTemplate)
OPTIONAL MATCH (exec)-[:EXECUTED_ON]->(target)
RETURN exec, template, target
ORDER BY exec.startTime DESC
LIMIT 50
```

**Get Template Usage Statistics**:
```cypher
MATCH (template:ActionTemplate {isCurrent: true})
OPTIONAL MATCH (exec:WorkflowExecution)-[:USED_TEMPLATE]->(template)
RETURN template.keyword as template,
       count(exec) as execution_count,
       count(CASE WHEN exec.status = 'completed' THEN 1 END) as successful,
       count(CASE WHEN exec.status = 'failed' THEN 1 END) as failed
ORDER BY execution_count DESC
```

### Code Analysis Queries

**Find Function Dependencies**:
```cypher
MATCH (func:FunctionNode {name: $function_name})
MATCH path = (func)-[:CALLS*1..3]->(dependency:FunctionNode)
RETURN path,
       [node IN nodes(path) | node.name] as call_chain
```

**Get Code Complexity Hotspots**:
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

### Knowledge Graph Queries

**Find Related Concepts**:
```cypher
MATCH (concept:KnowledgeEntity {name: $concept_name})
MATCH path = (concept)-[:RELATES_TO*1..2]-(related:KnowledgeEntity)
RETURN DISTINCT related.name as related_concept,
       length(path) as distance,
       [rel IN relationships(path) | type(rel)] as relationship_types
ORDER BY distance
```

**Get Citations for Entity**:
```cypher
MATCH (entity:KnowledgeEntity {id: $entity_id})
MATCH (entity)-[:CITED_BY]->(citation:Citation)
RETURN entity.name as entity,
       collect({
         source: citation.source,
         title: citation.title,
         url: citation.url
       }) as citations
```
