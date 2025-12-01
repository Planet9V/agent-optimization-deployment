---
title: Guidance Hub System (Part 1)
category: 02_Core_Concepts
last_updated: 2025-10-25
line_count: 486
status: published
tags: [neocoder, mcp, documentation]
---

# Guidance Hub System

[← Back to Graph Structure](03_Graph_Structure.md) | [Next: Incarnations Overview →](../03_Incarnations/01_Overview.md)

## Overview

The Guidance Hub System is NeoCoder's intelligent navigation framework that helps AI assistants discover capabilities, understand context, and make effective use of available tools. Hubs are stored as graph nodes in Neo4j and exposed as MCP resources, creating a self-documenting system that guides AI decision-making.

## What Are Guidance Hubs?

Guidance hubs are **contextualized documentation nodes** that:
- **Orient AI Assistants** - Provide situational awareness of capabilities
- **Suggest Workflows** - Recommend appropriate templates for tasks
- **Link Related Concepts** - Create navigation paths through knowledge
- **Document Best Practices** - Encode expert knowledge in graph structure
- **Enable Discovery** - Allow AI to explore capabilities organically

Unlike static documentation, hubs are:
- **Dynamic** - Generated from current graph state
- **Interconnected** - Form a navigation graph
- **Context-Aware** - Adapt to current incarnation and project
- **Machine-Readable** - Structured for AI consumption
- **Human-Readable** - Formatted as markdown for humans

## Hub Types

### Main Hub

**Purpose**: Root navigation entry point for all AI assistants

**Hub Name**: `main_hub`

**Contents**:
- Overview of NeoCoder capabilities
- Links to incarnation-specific hubs
- Common workflow templates
- Getting started guidance
- Resource discovery instructions

**Access**:
```python
# MCP resource access
hub_content = await read_resource("guidance://main_hub")
```

**Example Structure**:
```markdown
# NeoCoder Main Navigation Hub

## Available Incarnations
- **coding** - Software development and codebase management
- **knowledge_graph** - Knowledge base construction
- **code_analysis** - Code structure analysis
- **research** - Research synthesis

## Common Templates
- CODE_ANALYZE - Analyze code structure
- KNOWLEDGE_EXTRACT - Extract semantic knowledge
- FIX - Fix bugs or issues

## Getting Started
1. Select appropriate incarnation
2. Create or select project
3. Choose workflow template
```

### Incarnation Hub

**Purpose**: Incarnation-specific capabilities and tools

**Hub Names**:
- `coding_guide`
- `knowledge_graph_guide`
- `code_analysis_guide`
- `research_guide`
- `decision_support_guide`
- `data_analysis_guide`
- `complex_system_guide`

**Contents**:
- Available tools for incarnation
- Typical workflows
- Data model overview
- Best practices
- Example queries

**Example** (coding_guide):
```markdown
# Coding Incarnation Guide

## Tools Available
- create_project - Initialize software project
- add_file_to_project - Register source files
- execute_workflow - Run workflow templates
- get_project_structure - Query project tree

## Common Workflows
- **New Project Setup** - Create project → Add files → Initialize structure
- **Code Analysis** - Select project → Execute CODE_ANALYZE template
- **Dependency Tracking** - Import analysis → Relationship mapping

## Best Practices
- Always create project before adding files
- Use templates for consistent workflows
- Track modifications in WorkflowExecution nodes
```

### Cypher Guide Hub

**Purpose**: Cypher query pattern library for each incarnation

**Hub Names**:
- `coding_cypher_guide`
- `knowledge_graph_cypher_guide`
- `code_analysis_cypher_guide`
- `research_cypher_guide`

**Contents**:
- Verified query patterns
- Performance-optimized queries
- Common operations
- Anti-patterns to avoid
- Schema-specific queries

**Example** (coding_cypher_guide):
```markdown
# Coding Incarnation Cypher Patterns

## Project Queries

### Get Project with Files
\`\`\`cypher
MATCH (p:Project {id: $project_id})
OPTIONAL MATCH (p)-[:HAS_FILE]->(f:File)
RETURN p, collect(f) as files
\`\`\`

### Find Files by Extension
\`\`\`cypher
MATCH (p:Project)-[:HAS_FILE]->(f:File)
WHERE f.extension = $extension
RETURN f.path as file_path, f.size as size
ORDER BY f.path
\`\`\`

## Anti-Patterns

❌ **Avoid**: Scanning all files without project context
\`\`\`cypher
MATCH (f:File) RETURN f  // Too broad, poor performance
\`\`\`

✅ **Prefer**: Project-scoped queries
\`\`\`cypher
MATCH (p:Project {id: $id})-[:HAS_FILE]->(f:File)
RETURN f
\`\`\`
```

### Workflow Guide Hub

**Purpose**: Template usage instructions and workflow composition

**Hub Name**: `workflow_guide_hub`

**Contents**:
- Action template catalog
- Template parameters
- Workflow composition patterns
- Execution monitoring
- Error handling guidance

**Example**:
```markdown
# Workflow Template Guide

## Available Templates

### CODE_ANALYZE
**Purpose**: Analyze code structure and dependencies
**Parameters**:
- `file_path` (string) - File to analyze
- `analysis_depth` (int) - AST traversal depth

**Usage**:
\`\`\`cypher
MATCH (template:ActionTemplate {keyword: 'CODE_ANALYZE'})
CREATE (exec:WorkflowExecution {
  id: randomUUID(),
  templateKeyword: 'CODE_ANALYZE',
  parameters: {file_path: 'src/main.py', analysis_depth: 3},
  status: 'pending'
})-[:USED_TEMPLATE]->(template)
\`\`\`

### KNOWLEDGE_EXTRACT
**Purpose**: Extract semantic knowledge from text
**Parameters**:
- `text` (string) - Content to analyze
- `domain` (string) - Knowledge domain

**Best Practices**:
- Chunk large texts into manageable pieces
- Specify domain for better extraction
- Link extracted entities to source citations
```

## Hub Structure in Neo4j

### Hub Node Schema

```cypher
CREATE (hub:AiGuidanceHub {
  name: 'main_hub',                    // Unique identifier
  title: 'NeoCoder Main Hub',          // Display title
  description: 'Root navigation hub',  // Purpose description
  content: '# Main Hub...',            // Markdown content
  version: '1.0.0',                    // Hub version
  incarnation: null,                   // Null for global hubs
  created: datetime(),
  updated: datetime()
})
```

### Hub Relationships

**Navigation Links**:
```cypher
(main:AiGuidanceHub {name: 'main_hub'})
  -[:LINKS_TO]->
(coding:AiGuidanceHub {name: 'coding_guide'})
```

**Template Suggestions**:
```cypher
(hub:AiGuidanceHub {name: 'coding_guide'})
  -[:SUGGESTS_TEMPLATE]->
(template:ActionTemplate {keyword: 'CODE_ANALYZE'})
```

**Concept Guidance**:
```cypher
(hub:AiGuidanceHub {name: 'workflow_guide_hub'})
  -[:PROVIDES_GUIDANCE_ON]->
(concept:Concept {name: 'workflow_composition'})
```

**Tool Recommendations**:
```cypher
(hub:AiGuidanceHub {name: 'coding_guide'})
  -[:RECOMMENDS_TOOL]->
(tool:ToolDefinition {name: 'create_project'})
```

## Creating Guidance Hubs

### Manual Hub Creation

```cypher
-- Create incarnation hub
CREATE (hub:AiGuidanceHub {
  name: 'coding_guide',
  title: 'Coding Incarnation Guide',
  description: 'Tools and workflows for software development',
  content: $markdown_content,
  version: '1.0.0',
  incarnation: 'coding',
  created: datetime(),
  updated: datetime()
})

-- Link to main hub
MATCH (main:AiGuidanceHub {name: 'main_hub'})
MATCH (coding:AiGuidanceHub {name: 'coding_guide'})
MERGE (main)-[:LINKS_TO]->(coding)

-- Link to templates
MATCH (hub:AiGuidanceHub {name: 'coding_guide'})
MATCH (template:ActionTemplate {keyword: 'CODE_ANALYZE'})
MERGE (hub)-[:SUGGESTS_TEMPLATE]->(template)
```

### Programmatic Hub Generation

```python
async def create_guidance_hub(
    name: str,
    title: str,
    description: str,
    content: str,
    incarnation: str | None = None,
    parent_hub: str | None = "main_hub"
):
    """Create a new guidance hub with relationships."""
    async with driver.session() as session:
        # Create hub node
        result = await session.run("""
            CREATE (hub:AiGuidanceHub {
              name: $name,
              title: $title,
              description: $description,
              content: $content,
              version: '1.0.0',
              incarnation: $incarnation,
              created: datetime(),
              updated: datetime()
            })
            RETURN hub
        """, {
            'name': name,
            'title': title,
            'description': description,
            'content': content,
            'incarnation': incarnation
        })

        # Link to parent
        if parent_hub:
            await session.run("""
                MATCH (parent:AiGuidanceHub {name: $parent})
                MATCH (child:AiGuidanceHub {name: $child})
                MERGE (parent)-[:LINKS_TO]->(child)
            """, {'parent': parent_hub, 'child': name})
```

## Accessing Guidance Hubs

### Through MCP Resources

```python
# AI assistant code
hub_content = await read_resource("guidance://main_hub")
print(hub_content)  # Markdown formatted guidance
```

### Direct Cypher Queries

```cypher
-- Get hub with navigation links
MATCH (hub:AiGuidanceHub {name: 'main_hub'})
OPTIONAL MATCH (hub)-[:LINKS_TO]->(child:AiGuidanceHub)
RETURN hub, collect(child) as linked_hubs

-- Get hub with template suggestions
MATCH (hub:AiGuidanceHub {name: 'coding_guide'})
OPTIONAL MATCH (hub)-[:SUGGESTS_TEMPLATE]->(template:ActionTemplate)
WHERE template.isCurrent = true
RETURN hub, collect(template) as suggested_templates
```

### Through Tools

```python
# Use list_guidance_hubs tool
hubs = await list_guidance_hubs(incarnation="coding")

# Use get_guidance_hub_content tool
content = await get_guidance_hub_content(hub_name="coding_guide")
```

## Hub Navigation Patterns

### Hierarchical Navigation

```
main_hub
├── coding_guide
│   ├── coding_cypher_guide
│   └── project_management_guide
├── knowledge_graph_guide
│   ├── knowledge_graph_cypher_guide
│   └── entity_modeling_guide
└── code_analysis_guide
    ├── code_analysis_cypher_guide
    └── ast_patterns_guide
```

**Query Navigation Path**:
```cypher
MATCH path = (root:AiGuidanceHub {name: 'main_hub'})
             -[:LINKS_TO*1..3]->
             (hub:AiGuidanceHub)
RETURN [node IN nodes(path) | node.name] as navigation_path,
       hub.title as destination
```

### Context-Based Navigation

```cypher
-- Find hubs relevant to current task
MATCH (hub:AiGuidanceHub)
WHERE hub.incarnation = $current_incarnation
  OR hub.incarnation IS NULL
OPTIONAL MATCH (hub)-[:SUGGESTS_TEMPLATE]->(template:ActionTemplate)
WHERE template.keyword = $task_keyword
RETURN hub, collect(template) as relevant_templates
ORDER BY count(template) DESC
```

### Discovery Navigation

```cypher
-- Explore from current hub
MATCH (current:AiGuidanceHub {name: $current_hub})
MATCH (current)-[:LINKS_TO]->(neighbor:AiGuidanceHub)
OPTIONAL MATCH (neighbor)-[:SUGGESTS_TEMPLATE]->(template:ActionTemplate)
OPTIONAL MATCH (neighbor)-[:PROVIDES_GUIDANCE_ON]->(concept)
RETURN neighbor.name as hub_name,
       neighbor.description as description,
       collect(DISTINCT template.keyword) as templates,
       collect(DISTINCT concept.name) as concepts
```

## Hub Content Generation

### Dynamic Content Assembly

```python
async def generate_hub_content(hub_name: str) -> str:
    """Generate hub content dynamically from graph state."""
    query = """
    MATCH (hub:AiGuidanceHub {name: $hub_name})
    OPTIONAL MATCH (hub)-[:LINKS_TO]->(child:AiGuidanceHub)
    OPTIONAL MATCH (hub)-[:SUGGESTS_TEMPLATE]->(template:ActionTemplate)
    WHERE template.isCurrent = true
    OPTIONAL MATCH (hub)-[:RECOMMENDS_TOOL]->(tool:ToolDefinition)
    RETURN hub,
           collect(DISTINCT child) as children,
           collect(DISTINCT template) as templates,
           collect(DISTINCT tool) as tools
    """

    result = await session.run(query, {'hub_name': hub_name})
    record = result.single()

    # Format as markdown
    content = f"# {record['hub'].get('title')}\n\n"
    content += f"{record['hub'].get('description')}\n\n"

    if record['children']:
        content += "## Related Hubs\n"
        for child in record['children']:
            content += f"- [{child['title']}](guidance://{child['name']})\n"

    if record['templates']:
        content += "\n## Suggested Templates\n"
        for template in record['templates']:
            content += f"- **{template['keyword']}** - {template['description']}\n"

    if record['tools']:
        content += "\n## Recommended Tools\n"
        for tool in record['tools']:
            content += f"- `{tool['name']}` - {tool['description']}\n"

    return content
```

### Template-Based Content

```python
HUB_TEMPLATE = """
# {title}

{description}

## Overview
{overview}

## Key Capabilities
{capabilities}

## Common Workflows
{workflows}

## Related Resources
{resources}

## Best Practices
{best_practices}
"""

def create_hub_from_template(data: dict) -> str:
    """Generate hub content from template."""
    return HUB_TEMPLATE.format(**data)
```
