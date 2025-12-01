---
title: Troubleshooting Guide (Part 1 of 2)
category: 08_Reference
last_updated: 2025-10-25
line_count: 469
status: published
tags: [neocoder, mcp, documentation]
---


# Troubleshooting Guide

[← Back to API Reference](02_API_Reference.md) | [Next: Changelog →](04_Changelog.md)

## Overview

Common issues, error messages, and solutions for NeoCoder deployment and operation.

## Installation Issues

### Neo4j Connection Failed

**Symptom**:
```
Error: Failed to connect to Neo4j at bolt://localhost:7687
ServiceUnavailable: Unable to retrieve routing information
```

**Solutions**:

1. **Verify Neo4j is running**:
```bash
docker ps | grep neo4j
# Should show running container

# If not running, start Neo4j
docker start neocoder-neo4j
```

2. **Check connection parameters**:
```bash
# Verify .env file
cat .env | grep NEO4J

# Should show:
# NEO4J_URI=bolt://localhost:7687
# NEO4J_USER=neo4j
# NEO4J_PASSWORD=your-password
```

3. **Test connection manually**:
```bash
# Using cypher-shell
cypher-shell -a bolt://localhost:7687 -u neo4j -p your-password

# Or using Python
python -c "from neo4j import GraphDatabase; driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'your-password')); driver.verify_connectivity()"
```

4. **Check firewall and ports**:
```bash
# Verify port 7687 is accessible
nc -zv localhost 7687

# Check Neo4j logs
docker logs neocoder-neo4j
```

### Qdrant Connection Timeout

**Symptom**:
```
TimeoutError: Qdrant connection timed out at http://localhost:6333
```

**Solutions**:

1. **Verify Qdrant is running**:
```bash
docker ps | grep qdrant

# Start if needed
docker start neocoder-qdrant
```

2. **Check Qdrant health**:
```bash
curl http://localhost:6333/health
# Should return: {"title":"qdrant - vector search engine","version":"..."}
```

3. **Verify configuration**:
```python
# Test Qdrant connection
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
print(client.get_collections())
```

### MCP Server Not Recognized

**Symptom**:
```
MCP server "neocoder" not found in Claude Desktop
Tools not appearing in Claude Code
```

**Solutions**:

1. **Verify MCP configuration**:
```bash
# Check Claude Desktop config
# macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
# Windows: %APPDATA%/Claude/claude_desktop_config.json

cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. **Correct configuration format**:
```json
{
  "mcpServers": {
    "neocoder": {
      "command": "python",
      "args": ["-m", "neocoder_mcp"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "your-password",
        "QDRANT_URL": "http://localhost:6333",
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

3. **Restart Claude Desktop** after configuration changes

4. **Check Python environment**:
```bash
# Verify neocoder_mcp module
python -m neocoder_mcp --version

# If not found, reinstall
pip install -e .
```

## Runtime Errors

### Workflow Execution Failed

**Symptom**:
```
{
  "success": false,
  "error_code": "database_error",
  "message": "Workflow execution failed"
}
```

**Diagnostic Steps**:

1. **Check workflow parameters**:
```python
# Verify required parameters provided
result = await execute_workflow(
    keyword="FEATURE",
    parameters={
        "feature_name": "test",  # Required
        "feature_type": "module",  # Required
        # Missing parameters?
    }
)
```

2. **View workflow history**:
```cypher
MATCH (exec:WorkflowExecution)
WHERE exec.status = 'failed'
RETURN exec
ORDER BY exec.started DESC
LIMIT 10
```

3. **Check execution logs**:
```bash
# View NeoCoder logs
tail -f neocoder.log

# Filter for errors
grep ERROR neocoder.log
```

4. **Verify template exists**:
```cypher
MATCH (t:ActionTemplate {keyword: 'FEATURE'})
WHERE t.isCurrent = true
RETURN t
```

### Entity Creation Validation Error

**Symptom**:
```
{
  "success": false,
  "error_code": "validation_error",
  "details": [
    {"field": "entity_type", "message": "Invalid entity type"}
  ]
}
```

**Solutions**:

1. **Use valid entity types**:
```python
# Valid types
entity_types = ["concept", "technology", "person", "organization"]

# Correct usage
result = await create_knowledge_entity(
    name="Machine Learning",
    entity_type="concept",  # Must be from valid types
    description="..."
)
```

2. **Check parameter constraints**:
```python
# Name: 1-200 characters
# Domain: optional string
# Tags: max 20 tags
# Properties: valid JSON dict
```

### Memory/Performance Issues

**Symptom**:
```
System running slowly
High memory usage
Query timeouts
```

**Solutions**:

1. **Check Neo4j memory settings**:
```bash
# View Neo4j configuration
docker exec neocoder-neo4j cat /var/lib/neo4j/conf/neo4j.conf | grep memory

# Increase if needed (in docker-compose.yml)
environment:
  - NEO4J_server_memory_heap_initial__size=512m
  - NEO4J_server_memory_heap_max__size=2G
  - NEO4J_server_memory_pagecache_size=1G
```

2. **Optimize queries**:
```cypher
// Add LIMIT to prevent unbounded queries
MATCH (e:KnowledgeEntity)
RETURN e
LIMIT 100  // Always include limit

// Use indexes
CREATE INDEX IF NOT EXISTS FOR (e:KnowledgeEntity) ON (e.id)
```

3. **Clear query cache**:
```cypher
CALL db.clearQueryCaches()
```

4. **Monitor active queries**:
```cypher
CALL dbms.listQueries()
YIELD query, elapsedTimeMillis
WHERE elapsedTimeMillis > 1000
RETURN query, elapsedTimeMillis
ORDER BY elapsedTimeMillis DESC
```

## Data Issues

### Duplicate Entities

**Symptom**:
```
Multiple entities with same name created
Relationship errors due to duplicates
```

**Solutions**:

1. **Find duplicates**:
```cypher
MATCH (e:KnowledgeEntity)
WITH e.name as name, collect(e) as entities
WHERE size(entities) > 1
RETURN name, entities
```

2. **Merge duplicates**:
```cypher
// For each duplicate set, keep first and merge relationships
MATCH (e:KnowledgeEntity)
WITH e.name as name, collect(e) as entities
WHERE size(entities) > 1

WITH name, entities[0] as keep, entities[1..] as duplicates
UNWIND duplicates as dup

// Transfer relationships
MATCH (dup)-[r]-(other)
MERGE (keep)-[new:RELATES_TO {type: r.type}]-(other)

// Delete duplicate
DETACH DELETE dup
```

3. **Prevent duplicates going forward**:
```cypher
// Use MERGE instead of CREATE
MERGE (e:KnowledgeEntity {name: $name})
ON CREATE SET e.id = randomUUID(),
              e.created = datetime()
ON MATCH SET e.updated = datetime()
```

### Orphaned Nodes

**Symptom**:
```
Entities with no relationships
Unused project files
```

**Solutions**:

1. **Find orphaned entities**:
```cypher
MATCH (e:KnowledgeEntity)
WHERE NOT (e)-[]-()
RETURN e
```

2. **Clean up orphans**:
```cypher
// Review first, then delete
MATCH (e:KnowledgeEntity)
WHERE NOT (e)-[]-()
  AND e.created < datetime() - duration('P30D')  // Older than 30 days
DELETE e
```

3. **Find orphaned files**:
```cypher
MATCH (f:File)
WHERE NOT (f)<-[:HAS_FILE]-()
RETURN f
```

### Broken Relationships

**Symptom**:
```
Relationships pointing to non-existent entities
Circular dependencies
```

**Solutions**:

1. **Find broken relationships**:
```cypher
MATCH (e)-[r]-(target)
WHERE target.id IS NULL OR e.id IS NULL
RETURN e, r, target
```

2. **Fix or remove broken relationships**:
```cypher
MATCH ()-[r]-()
WHERE startNode(r).id IS NULL OR endNode(r).id IS NULL
DELETE r
```

3. **Detect circular dependencies**:
```cypher
MATCH path = (e:KnowledgeEntity)-[:RELATES_TO*]->(e)
RETURN path
LIMIT 10
```

## Vector Store Issues

### Embedding Generation Failed

**Symptom**:
```
Error: OpenAI API key invalid or quota exceeded
Failed to generate embedding for text
```

**Solutions**:

1. **Verify API key**:
```bash
# Check environment variable
echo $OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

2. **Check quota and billing**:
- Visit https://platform.openai.com/usage
- Verify billing information
- Check rate limits

3. **Use fallback embeddings**:
```python
# Option 1: Local embeddings (sentence-transformers)
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode(text)

# Option 2: Cached embeddings
# Implement caching layer to reduce API calls
```

### Vector Search Returns No Results

**Symptom**:
```
Semantic search returns empty results
Low relevance scores
```

**Solutions**:

1. **Verify collection exists**:
```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
collections = client.get_collections()
print([c.name for c in collections.collections])
```

2. **Check collection has vectors**:
```python
collection_info = client.get_collection("knowledge")
print(f"Vectors count: {collection_info.vectors_count}")
```

3. **Lower similarity threshold**:
```python
# Default threshold might be too high
results = await semantic_search(
    query_text="...",
    threshold=0.5  # Try lower threshold
)
```

4. **Verify embedding dimensions match**:
```python
# Check collection config
collection = client.get_collection("knowledge")
print(f"Vector size: {collection.config.params.vectors.size}")
# Should be 1536 for OpenAI ada-002
```
