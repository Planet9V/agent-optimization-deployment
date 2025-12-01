---
title: 01_Cypher_Patterns_Part1 (Part 2 of 2)
category: 08_Reference
last_updated: 2025-10-25
line_count: 105
status: published
tags: [neocoder, mcp, documentation]
---

## F-Contraction Patterns

### Create Synthesis

```cypher
// Create synthesized entity
CREATE (synth:KnowledgeEntity {
  id: randomUUID(),
  name: $name,
  type: 'synthesized',
  description: $description,
  synthesis_method: 'f_contraction',
  source_count: $source_count,
  created: datetime()
})
RETURN synth.id as synthesis_id
```

### Link to Sources

```cypher
MATCH (synth:KnowledgeEntity {id: $synthesis_id})
MATCH (source:KnowledgeEntity)
WHERE source.id IN $source_ids
CREATE (synth)-[:DERIVED_FROM {
  method: 'f_contraction',
  timestamp: datetime()
}]->(source)
```

### Find Synthesis Sources

```cypher
MATCH (synth:KnowledgeEntity {id: $synthesis_id})-[:DERIVED_FROM]->(source)
RETURN source
ORDER BY source.created
```

### Find Syntheses Using Source

```cypher
MATCH (source:KnowledgeEntity {id: $source_id})<-[:DERIVED_FROM]-(synth)
WHERE synth.type = 'synthesized'
RETURN synth
```

## Performance Optimization

### Use Indexes

```cypher
// Create indexes for common queries
CREATE INDEX entity_id_index IF NOT EXISTS
FOR (e:KnowledgeEntity) ON (e.id);

CREATE INDEX entity_name_index IF NOT EXISTS
FOR (e:KnowledgeEntity) ON (e.name);

CREATE INDEX entity_domain_index IF NOT EXISTS
FOR (e:KnowledgeEntity) ON (e.domain);

CREATE INDEX project_id_index IF NOT EXISTS
FOR (p:Project) ON (p.id);

CREATE INDEX file_path_index IF NOT EXISTS
FOR (f:File) ON (f.path);
```

### Use LIMIT

```cypher
// Always limit results for large datasets
MATCH (e:KnowledgeEntity)
RETURN e
LIMIT 100  // Prevents unbounded queries
```

### Use Parameters

```cypher
// Good: Parameterized query (can be cached)
MATCH (e:KnowledgeEntity {id: $entity_id})
RETURN e

// Avoid: Literal values (each query is unique)
MATCH (e:KnowledgeEntity {id: 'uuid-here'})
RETURN e
```

### EXPLAIN and PROFILE

```cypher
// Analyze query plan
EXPLAIN
MATCH (e:KnowledgeEntity)-[r]->(related)
WHERE e.domain = $domain
RETURN e, related

// Analyze actual execution
PROFILE
MATCH (e:KnowledgeEntity)-[r]->(related)
WHERE e.domain = $domain
RETURN e, related
```
