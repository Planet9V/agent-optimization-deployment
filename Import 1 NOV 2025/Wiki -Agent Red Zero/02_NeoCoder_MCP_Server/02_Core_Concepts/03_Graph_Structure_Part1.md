---
title: Graph Structure in NeoCoder (Part 1 of 2)
category: 02_Core_Concepts
last_updated: 2025-10-25
line_count: 447
status: published
tags: [neocoder, mcp, documentation]
---


# Graph Structure in NeoCoder

[← Back to MCP Integration](02_MCP_Integration.md) | [Next: Guidance Hub System →](04_Guidance_Hub.md)

## Overview

NeoCoder uses Neo4j as its primary knowledge graph database to store structured information about projects, workflows, code structures, and AI guidance. The graph schema is designed to support hybrid reasoning, workflow tracking, and contextual AI assistance.

## Core Node Types

### AiGuidanceHub

Central navigation nodes for AI assistants to discover capabilities and best practices.

**Properties**:
- `name` (string, unique) - Hub identifier
- `title` (string) - Human-readable name
- `description` (string) - Hub purpose and scope
- `content` (text) - Markdown-formatted guidance
- `version` (string) - Hub version
- `created` (datetime) - Creation timestamp
- `updated` (datetime) - Last modification

**Example**:
```cypher
CREATE (hub:AiGuidanceHub {
  name: 'main_hub',
  title: 'NeoCoder Main Navigation Hub',
  description: 'Root hub for AI assistant guidance',
  content: '# Welcome to NeoCoder...',
  version: '1.0.0',
  created: datetime(),
  updated: datetime()
})
```

### ActionTemplate

Reusable workflow templates that define standardized processes.

**Properties**:
- `keyword` (string) - Template identifier (e.g., 'CODE_ANALYZE')
- `description` (string) - Template purpose
- `isCurrent` (boolean) - Active version flag
- `version` (string) - Template version
- `created` (datetime) - Creation timestamp
- `cypher` (text) - Cypher queries for execution
- `guidance` (text) - Usage instructions
- `parameters` (map) - Parameter definitions

**Constraints**:
```cypher
CREATE CONSTRAINT unique_action_template_current IF NOT EXISTS
FOR (t:ActionTemplate)
REQUIRE (t.keyword, t.isCurrent) IS UNIQUE
```

**Example**:
```cypher
CREATE (template:ActionTemplate {
  keyword: 'CODE_ANALYZE',
  description: 'Analyze code structure and dependencies',
  isCurrent: true,
  version: '1.0.0',
  created: datetime(),
  cypher: 'MATCH (f:File)...',
  guidance: 'Use for AST/ASG analysis',
  parameters: {
    file_path: 'string',
    analysis_depth: 'integer'
  }
})
```

### Project

Represents a software project or knowledge domain.

**Properties**:
- `id` (string, unique) - Project UUID
- `name` (string) - Project name
- `description` (string) - Project purpose
- `rootPath` (string) - Filesystem root path
- `created` (datetime) - Creation timestamp
- `updated` (datetime) - Last modification
- `metadata` (map) - Additional properties
- `tags` (list[string]) - Project categorization

**Constraints**:
```cypher
CREATE CONSTRAINT unique_project_id IF NOT EXISTS
FOR (p:Project)
REQUIRE p.id IS UNIQUE
```

**Example**:
```cypher
CREATE (proj:Project {
  id: randomUUID(),
  name: 'Authentication Service',
  description: 'User authentication microservice',
  rootPath: '/src/auth-service',
  created: datetime(),
  updated: datetime(),
  metadata: {
    language: 'Python',
    framework: 'FastAPI'
  },
  tags: ['microservice', 'authentication']
})
```

### File

Represents individual files within projects.

**Properties**:
- `id` (string, unique) - File UUID
- `path` (string) - Relative file path
- `absolutePath` (string) - Full filesystem path
- `name` (string) - Filename with extension
- `extension` (string) - File extension
- `size` (integer) - File size in bytes
- `hash` (string) - Content hash (SHA-256)
- `created` (datetime) - Creation timestamp
- `updated` (datetime) - Last modification
- `content` (text, optional) - File content
- `language` (string) - Programming language

**Constraints**:
```cypher
CREATE CONSTRAINT unique_file_id IF NOT EXISTS
FOR (f:File)
REQUIRE f.id IS UNIQUE
```

**Example**:
```cypher
CREATE (file:File {
  id: randomUUID(),
  path: 'src/auth/login.py',
  absolutePath: '/project/src/auth/login.py',
  name: 'login.py',
  extension: 'py',
  size: 4096,
  hash: 'abc123...',
  created: datetime(),
  updated: datetime(),
  language: 'Python'
})
```

### Directory

Represents directory structures within projects.

**Properties**:
- `id` (string, unique) - Directory UUID
- `path` (string) - Relative directory path
- `absolutePath` (string) - Full filesystem path
- `name` (string) - Directory name
- `created` (datetime) - Creation timestamp
- `updated` (datetime) - Last modification

**Constraints**:
```cypher
CREATE CONSTRAINT unique_directory_id IF NOT EXISTS
FOR (d:Directory)
REQUIRE d.id IS UNIQUE
```

### WorkflowExecution

Records of workflow executions for audit trails and learning.

**Properties**:
- `id` (string, unique) - Execution UUID
- `templateKeyword` (string) - Template used
- `status` (string) - 'pending', 'running', 'completed', 'failed'
- `startTime` (datetime) - Execution start
- `endTime` (datetime, optional) - Execution completion
- `parameters` (map) - Input parameters
- `results` (map) - Execution results
- `error` (string, optional) - Error message if failed
- `executedBy` (string) - AI assistant or user identifier

**Constraints**:
```cypher
CREATE CONSTRAINT unique_workflow_execution_id IF NOT EXISTS
FOR (e:WorkflowExecution)
REQUIRE e.id IS UNIQUE
```

**Example**:
```cypher
CREATE (exec:WorkflowExecution {
  id: randomUUID(),
  templateKeyword: 'CODE_ANALYZE',
  status: 'completed',
  startTime: datetime('2024-01-15T10:30:00Z'),
  endTime: datetime('2024-01-15T10:32:15Z'),
  parameters: {
    file_path: 'src/auth/login.py',
    analysis_depth: 3
  },
  results: {
    complexity: 15,
    dependencies: ['bcrypt', 'jwt']
  },
  executedBy: 'claude-assistant'
})
```

## Incarnation-Specific Nodes

### Code Analysis Incarnation

**CodeEntity** - Represents code constructs:
```cypher
CREATE (entity:CodeEntity {
  id: randomUUID(),
  type: 'class',
  name: 'AuthService',
  filePath: 'src/auth/service.py',
  startLine: 10,
  endLine: 150,
  complexity: 8,
  docstring: 'Authentication service class'
})
```

**FunctionNode** - Represents functions/methods:
```cypher
CREATE (func:FunctionNode {
  id: randomUUID(),
  name: 'login',
  signature: 'def login(username: str, password: str) -> Token',
  returnType: 'Token',
  parameters: ['username', 'password'],
  complexity: 5
})
```

### Knowledge Graph Incarnation

**KnowledgeEntity** - Semantic entities:
```cypher
CREATE (entity:KnowledgeEntity {
  id: randomUUID(),
  type: 'concept',
  name: 'JWT Authentication',
  description: 'JSON Web Token based authentication',
  domain: 'security',
  created: datetime()
})
```

**Citation** - Source attribution:
```cypher
CREATE (citation:Citation {
  id: randomUUID(),
  source: 'RFC 7519',
  title: 'JSON Web Token (JWT)',
  url: 'https://tools.ietf.org/html/rfc7519',
  retrieved: datetime()
})
```

### Research Incarnation

**ResearchPaper** - Academic papers:
```cypher
CREATE (paper:ResearchPaper {
  id: randomUUID(),
  title: 'Attention Is All You Need',
  authors: ['Vaswani', 'Shazeer', 'Parmar'],
  year: 2017,
  doi: '10.48550/arXiv.1706.03762',
  citations: 50000
})
```

## Core Relationships

### Navigation Relationships

**:LINKS_TO** - Hub navigation:
```cypher
(hub:AiGuidanceHub)-[:LINKS_TO]->(child:AiGuidanceHub)
```

**:PROVIDES_GUIDANCE_ON** - Hub-to-concept:
```cypher
(hub:AiGuidanceHub)-[:PROVIDES_GUIDANCE_ON]->(concept:Concept)
```

**:SUGGESTS_TEMPLATE** - Hub-to-template:
```cypher
(hub:AiGuidanceHub)-[:SUGGESTS_TEMPLATE]->(template:ActionTemplate)
```

### Project Structure Relationships

**:HAS_FILE** - Project contains file:
```cypher
(project:Project)-[:HAS_FILE]->(file:File)
```

**:HAS_DIRECTORY** - Project contains directory:
```cypher
(project:Project)-[:HAS_DIRECTORY]->(dir:Directory)
```

**:CONTAINS** - Directory hierarchy:
```cypher
(parent:Directory)-[:CONTAINS]->(child:Directory)
(directory:Directory)-[:CONTAINS]->(file:File)
```

**:PARENT_DIR** - File to directory:
```cypher
(file:File)-[:PARENT_DIR]->(dir:Directory)
```

### Workflow Relationships

**:USED_TEMPLATE** - Execution to template:
```cypher
(exec:WorkflowExecution)-[:USED_TEMPLATE]->(template:ActionTemplate)
```

**:EXECUTED_ON** - Execution to target:
```cypher
(exec:WorkflowExecution)-[:EXECUTED_ON]->(file:File)
(exec:WorkflowExecution)-[:EXECUTED_ON]->(project:Project)
```

**:CREATED** - Workflow created entity:
```cypher
(exec:WorkflowExecution)-[:CREATED]->(entity)
```

**:MODIFIED** - Workflow modified entity:
```cypher
(exec:WorkflowExecution)-[:MODIFIED]->(entity)
```

### Code Structure Relationships

**:DEFINES** - File defines code entity:
```cypher
(file:File)-[:DEFINES]->(entity:CodeEntity)
```

**:CALLS** - Function calls:
```cypher
(caller:FunctionNode)-[:CALLS]->(callee:FunctionNode)
```

**:IMPORTS** - Module dependencies:
```cypher
(file:File)-[:IMPORTS]->(module:File)
```

**:INHERITS** - Class inheritance:
```cypher
(child:CodeEntity)-[:INHERITS]->(parent:CodeEntity)
```

### Knowledge Relationships

**:RELATES_TO** - Entity associations:
```cypher
(entity1:KnowledgeEntity)-[:RELATES_TO]->(entity2:KnowledgeEntity)
```

**:CITED_BY** - Citation tracking:
```cypher
(entity:KnowledgeEntity)-[:CITED_BY]->(citation:Citation)
```

**:SUPPORTS** - Evidence relationships:
```cypher
(evidence:KnowledgeEntity)-[:SUPPORTS]->(claim:KnowledgeEntity)
```

**:CONTRADICTS** - Conflicting information:
```cypher
(entity1:KnowledgeEntity)-[:CONTRADICTS]->(entity2:KnowledgeEntity)
```

## Schema Initialization

### Basic Schema Setup

```cypher
-- Create constraints for uniqueness
CREATE CONSTRAINT unique_project_id IF NOT EXISTS
FOR (p:Project)
REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT unique_file_id IF NOT EXISTS
FOR (f:File)
REQUIRE f.id IS UNIQUE;

CREATE CONSTRAINT unique_directory_id IF NOT EXISTS
FOR (d:Directory)
REQUIRE d.id IS UNIQUE;

CREATE CONSTRAINT unique_guidance_hub_name IF NOT EXISTS
FOR (h:AiGuidanceHub)
REQUIRE h.name IS UNIQUE;

CREATE CONSTRAINT unique_action_template_current IF NOT EXISTS
FOR (t:ActionTemplate)
REQUIRE (t.keyword, t.isCurrent) IS UNIQUE;

CREATE CONSTRAINT unique_workflow_execution_id IF NOT EXISTS
FOR (e:WorkflowExecution)
REQUIRE e.id IS UNIQUE;
```

### Performance Indexes

```cypher
-- Index for file path lookups
CREATE INDEX file_path_index IF NOT EXISTS
FOR (f:File)
ON (f.path);

-- Index for project name searches
CREATE INDEX project_name_index IF NOT EXISTS
FOR (p:Project)
ON (p.name);

-- Index for workflow status queries
CREATE INDEX workflow_status_index IF NOT EXISTS
FOR (e:WorkflowExecution)
ON (e.status);

-- Index for timestamp-based queries
CREATE INDEX workflow_start_time_index IF NOT EXISTS
FOR (e:WorkflowExecution)
ON (e.startTime);
```
