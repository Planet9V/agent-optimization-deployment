---
title: Guidance Hub System (Part 2)
category: 02_Core_Concepts
last_updated: 2025-10-25
line_count: 88
status: published
tags: [neocoder, mcp, documentation]
---

## Hub Maintenance

### Updating Hub Content

```cypher
-- Update hub content and version
MATCH (hub:AiGuidanceHub {name: 'coding_guide'})
SET hub.content = $new_content,
    hub.version = $new_version,
    hub.updated = datetime()
RETURN hub
```

### Adding Hub Relationships

```cypher
-- Link hub to new template
MATCH (hub:AiGuidanceHub {name: 'coding_guide'})
MATCH (template:ActionTemplate {keyword: 'NEW_TEMPLATE'})
MERGE (hub)-[:SUGGESTS_TEMPLATE]->(template)
```

### Versioning Hubs

```cypher
-- Create new version of hub
MATCH (old:AiGuidanceHub {name: 'coding_guide'})
CREATE (new:AiGuidanceHub)
SET new = old,
    new.version = $new_version,
    new.created = datetime(),
    new.updated = datetime()
WITH old, new
SET old:ArchivedHub
REMOVE old:AiGuidanceHub
```

## Best Practices

### Hub Design

**Keep Content Focused**:
- Each hub should cover one topic or incarnation
- Link to related hubs rather than duplicating content
- Use clear, actionable language

**Maintain Currency**:
- Update hubs when tools or templates change
- Version hubs for tracking changes
- Archive outdated content rather than deleting

**Enable Discovery**:
- Create rich relationship graphs
- Link hubs bidirectionally where appropriate
- Suggest relevant templates and tools

### AI Assistant Usage

**Start with Main Hub**:
```python
# Begin exploration from root
main_content = await read_resource("guidance://main_hub")
```

**Navigate Contextually**:
```python
# Switch to incarnation-specific hub
coding_content = await read_resource("guidance://coding_guide")
```

**Follow Suggestions**:
```python
# Use suggested templates from hub
template_keyword = extract_suggested_template(hub_content)
await execute_workflow(template_keyword, parameters)
```

## Related Documentation

- [MCP Integration](02_MCP_Integration.md) - Resource access patterns
- [Graph Structure](03_Graph_Structure.md) - Hub node schema
- [Incarnations Overview](../03_Incarnations/01_Overview.md) - Incarnation-specific hubs
- [Workflows](../04_Workflows/01_Template_Overview.md) - Template suggestions
- [Tools Reference](../05_Tools_Reference/01_Core_Tools.md) - Tool recommendations

---
*Last Updated: 2025-10-24 | [Report Issues](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues)*
