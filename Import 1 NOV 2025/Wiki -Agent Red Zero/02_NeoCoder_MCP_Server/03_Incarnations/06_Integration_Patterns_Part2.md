---
title: Batch all code analysis (Part 2 of 2)
category: 03_Incarnations
last_updated: 2025-10-25
line_count: 81
status: published
tags: [neocoder, mcp, documentation]
---

## Performance Considerations

### Minimize Incarnation Switching

**Inefficient**:
```python
for file in files:
    await switch_incarnation("code_analysis")
    await analyze_code_structure(file)
    await switch_incarnation("knowledge_graph")
    await create_knowledge_entity_from_analysis()
```

**Optimized**:
```python
# Batch all code analysis
await switch_incarnation("code_analysis")
analyses = [await analyze_code_structure(f) for f in files]

# Batch all knowledge graph operations
await switch_incarnation("knowledge_graph")
for analysis in analyses:
    await create_knowledge_entity_from_analysis(analysis)
```

### Cache Incarnation State

```python
class IncarnationCache:
    """Cache incarnation data to reduce switching overhead."""

    def __init__(self):
        self.current = None
        self.state_cache = {}

    async def switch_with_cache(self, incarnation: str):
        """Switch incarnation with state caching."""
        if self.current:
            # Save current state
            self.state_cache[self.current] = await get_current_state()

        # Switch incarnation
        await switch_incarnation(incarnation)
        self.current = incarnation

        # Restore cached state if available
        if incarnation in self.state_cache:
            await restore_state(self.state_cache[incarnation])
```

### Parallel Incarnation Execution

```python
import asyncio

async def parallel_incarnation_workflow():
    """Execute independent incarnation tasks in parallel."""

    # Define independent tasks
    async def code_task():
        await switch_incarnation("code_analysis")
        return await analyze_all_code()

    async def research_task():
        await switch_incarnation("research")
        return await process_new_papers()

    async def data_task():
        await switch_incarnation("data_analysis")
        return await analyze_data_pipeline()

    # Execute in parallel (requires separate Neo4j connections)
    results = await asyncio.gather(
        code_task(),
        research_task(),
        data_task()
    )

    return results
```
