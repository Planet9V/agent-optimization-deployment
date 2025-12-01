---
title: NeoCoder Quick Start Guide
category: NeoCoder/Getting_Started
last_updated: 2025-10-24
line_count: 295
status: published
tags: [neocoder, quickstart, tutorial, first-steps, workflows]
---

# NeoCoder Quick Start Guide

## Overview

Get started with NeoCoder in 15 minutes. This guide walks you through your first interaction with the NeoCoder system, from connection verification to executing your first workflow template.

## Prerequisites

- ✅ NeoCoder installed ([Installation Guide](01_Installation.md))
- ✅ Neo4j running and accessible
- ✅ Claude Desktop configured with MCP server
- ✅ Qdrant running (for hybrid reasoning features)

---

## Table of Contents

- [First Connection](#first-connection)
- [Understanding Incarnations](#understanding-incarnations)
- [Using Action Templates](#using-action-templates)
- [Your First Workflow](#your-first-workflow)
- [Exploring Tools](#exploring-tools)
- [Next Steps](#next-steps)

---

## First Connection

### Verify NeoCoder is Working

In Claude Desktop, ask:

```
Can you check your connection to Neo4j using NeoCoder?
```

**Expected Response:**
```
✅ Connected to Neo4j at bolt://localhost:7687
Database: neo4j
Neo4j Version: 5.x.x
Available Incarnations: 7
Current Incarnation: knowledge_graph
```

### Get the Guidance Hub

```
Show me the NeoCoder guidance hub
```

**What You'll See:**
- Welcome message
- System capabilities overview
- Available incarnations list
- Quick start instructions
- Links to key resources

---

## Understanding Incarnations

NeoCoder operates in specialized modes called "incarnations." Each incarnation provides different tools and workflows optimized for specific tasks.

### Available Incarnations

| Incarnation | Purpose | Common Use Cases |
|-------------|---------|------------------|
| **knowledge_graph** | Knowledge management | Document processing, entity tracking, research |
| **code_analysis** | Code structure analysis | AST parsing, code smell detection, documentation |
| **research** | Scientific research | Hypothesis tracking, experiments, publications |
| **decision_support** | Decision analysis | Alternative evaluation, evidence tracking |
| **data_analysis** | Data and system modeling | Complex systems, simulations |
| **coding** | Standard workflows | Default mode for basic development |

### Switch Incarnation

```
Switch to the knowledge_graph incarnation
```

**Result:**
- Incarnation changed
- New tools registered
- Schema initialized
- Guidance hub updated

---

## Using Action Templates

Action templates provide standardized workflows for common tasks. Each template enforces best practices, mandatory testing, and proper documentation.

### List Available Templates

```
List all available action templates
```

**Common Templates:**
- **FIX**: Bug fixing workflow with testing requirements
- **REFACTOR**: Code improvement with safety checks
- **FEATURE**: New feature implementation with documentation
- **DEPLOY**: Production deployment with validation
- **CODE_ANALYZE**: Code structure analysis
- **KNOWLEDGE_QUERY**: Hybrid reasoning queries
- **KNOWLEDGE_EXTRACT**: Document knowledge extraction

### Get Template Details

```
Get the FIX action template
```

**Template Structure:**
1. **Identify Context** - Understand the issue
2. **Reproduce Problem** - Verify the bug
3. **Implement Fix** - Make changes
4. **Execute Tests** - **MANDATORY** - All tests must pass
5. **Log Completion** - Record workflow execution

---

## Your First Workflow

Let's walk through a simple knowledge management workflow using the knowledge_graph incarnation.

### Step 1: Switch Incarnation

```
Switch to knowledge_graph incarnation
```

### Step 2: Create Your First Entity

```
Create a new entity named "NeoCoder System" of type "Software"
with observations:
- "MCP server implementation for Neo4j integration"
- "Supports 7 different operational incarnations"
- "Hybrid reasoning with Neo4j + Qdrant"
```

**What Happens:**
- Entity created in Neo4j
- Observations linked with timestamps
- Proper labeling applied
- Result returned with entity ID

### Step 3: Create Related Entity

```
Create an entity named "Neo4j Database" of type "Technology"
with observations:
- "Graph database for knowledge representation"
- "Stores entities, relationships, and workflows"
```

### Step 4: Link Entities

```
Create a relationship from "NeoCoder System" to "Neo4j Database"
with type "USES" and properties:
- "purpose": "Primary data store"
- "connection": "bolt://localhost:7687"
```

### Step 5: Query Your Knowledge

```
Search for nodes containing "Neo4j"
```

**Result:** Both entities returned with their observations and relationships.

### Step 6: View Graph Structure

```
Read the entire knowledge graph
```

**Result:** Complete graph visualization showing entities, observations, and relationships.

---

## Exploring Tools

### Core System Tools

```bash
# Check connection status
check_connection()

# Get current incarnation info
get_current_incarnation()

# List all incarnations
list_incarnations()

# Get guidance for current mode
get_guidance_hub()
```

### Knowledge Graph Tools

```bash
# Entity Management
create_entities(entities=[...])
delete_entities(entityNames=[...])
open_nodes(names=[...])

# Relationship Management
create_relations(relations=[...])
delete_relations(relations=[...])

# Search and Query
search_nodes(query="...")
read_graph()
```

### Workflow Tools

```bash
# Templates
list_action_templates()
get_action_template(keyword="FIX")
get_best_practices()

# Execution Tracking
log_workflow_execution(...)
get_workflow_history(project_id="...")
```

---

## Common Patterns

### Pattern 1: Knowledge Extraction from Text

```
Use KNOWLEDGE_EXTRACT template to process this document:
[paste document content]

Extract entities, relationships, and store in both Neo4j and Qdrant
```

### Pattern 2: Hybrid Reasoning Query

```
Use KNOWLEDGE_QUERY template to answer:
"What is the relationship between NeoCoder and Neo4j,
and what do documents say about their integration?"

Query both graph and vector databases
```

### Pattern 3: Code Analysis

```
Switch to code_analysis incarnation

Analyze this Python file:
/path/to/file.py

Generate AST, identify patterns, find code smells
```

---

## Quick Reference Commands

### Getting Help

```bash
# Show guidance hub
"Show me the NeoCoder guidance hub"

# List tools for current incarnation
"What tools are available in [incarnation_name] incarnation?"

# Get template help
"Explain the [TEMPLATE_NAME] workflow template"
```

### Common Workflows

```bash
# Create knowledge from document
"Extract knowledge from this PDF and store in Neo4j"

# Analyze code structure
"Analyze the structure of this codebase: /path/to/project"

# Execute standard workflow
"Use the FIX template to fix this bug in auth.py"
```

### Troubleshooting

```bash
# Connection issues
"Check the connection to Neo4j"
"Verify Qdrant is accessible"

# Template issues
"Show me the steps for the REFACTOR template"

# Tool issues
"List all tools available in the current incarnation"
```

---

## Next Steps

### Essential Reading

1. **[First Project](03_First_Project.md)** - Create a complete project
2. **[Architecture](../02_Core_Concepts/01_Architecture.md)** - Understand system design
3. **[Incarnations Overview](../03_Incarnations/01_Overview.md)** - Deep dive into modes

### Explore Features

1. **Try Different Incarnations** - Switch between modes and explore capabilities
2. **Run Workflow Templates** - Practice with FIX, REFACTOR, FEATURE templates
3. **Build Knowledge Graph** - Create entities, relationships, observations
4. **Hybrid Reasoning** - Use KNOWLEDGE_QUERY for multi-source analysis

### Advanced Topics

1. **[Hybrid Reasoning](../06_Advanced_Topics/01_Hybrid_Reasoning.md)** - Context-Augmented Reasoning
2. **[F-Contraction](../06_Advanced_Topics/02_F_Contraction.md)** - Dynamic knowledge merging
3. **[Creating Tools](../07_Development/01_Creating_Tools.md)** - Extend NeoCoder

---

## Related Topics

- [Installation Guide](01_Installation.md) - Setup and configuration
- [First Project Guide](03_First_Project.md) - Complete project setup
- [Knowledge Graph Tools](../05_Tools_Reference/02_Knowledge_Graph_Tools.md) - Tool reference
- [Workflow Templates](../04_Workflows/01_Template_Overview.md) - Template documentation

## See Also

- [NeoCoder Repository](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow) - Source code and examples
- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/) - Query language reference
- [MCP Documentation](https://modelcontextprotocol.io) - Protocol specification

---

**Last Updated:** 2025-10-24 | **Lines:** 295/400 | **Status:** published
