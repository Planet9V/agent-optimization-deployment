---
title: NeoCoder Architecture (Part 2)
category: 02_Core_Concepts
last_updated: 2025-10-25
line_count: 52
status: published
tags: [neocoder, mcp, documentation]
---

## Extension Points

### Adding New Incarnations

1. Create file in `src/mcp_neocoder/incarnations/`
2. Inherit from `BaseIncarnation`
3. Implement `initialize_schema()`
4. Define tool methods
5. Auto-discovered on startup

### Adding New Templates

```python
# Add via Cypher
write_neo4j_cypher(cypher="""
    CREATE (t:ActionTemplate {
        keyword: 'CUSTOM',
        version: '1.0',
        isCurrent: true,
        description: '...',
        steps: '...'
    })
""")
```

### Custom Tools

Implement in incarnation class:
```python
async def my_custom_tool(
    self,
    param1: str = Field(..., description="...")
) -> List[types.TextContent]:
    """Tool description."""
    # Implementation
    return [types.TextContent(type="text", text=result)]
```

## Related Documentation

- [MCP Integration](02_MCP_Integration.md) - Deep dive into MCP protocol usage
- [Graph Structure](03_Graph_Structure.md) - Neo4j schema details
- [Guidance Hub System](04_Guidance_Hub.md) - Navigation architecture
- [Incarnations Overview](../03_Incarnations/01_Overview.md) - Incarnation system details

---

*See Also*:
- Repository: [server.py](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/blob/main/src/mcp_neocoder/server.py)
- Process Management: [process_manager.py](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/blob/main/src/mcp_neocoder/process_manager.py)
- Incarnation Registry: [incarnation_registry.py](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/blob/main/src/mcp_neocoder/incarnation_registry.py)
