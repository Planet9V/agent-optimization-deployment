---
title: Good: One clear purpose (Part 2 of 2)
category: 07_Development
last_updated: 2025-10-25
line_count: 99
status: published
tags: [neocoder, mcp, documentation]
---

## Best Practices

### Design Principles

**Single Responsibility**:
```python
# Good: One clear purpose
async def create_entity(...) -> Dict:
    """Create entity only."""
    pass

async def link_entities(...) -> Dict:
    """Link entities only."""
    pass

# Avoid: Multiple responsibilities
async def create_and_link_entity(...) -> Dict:
    """Does too many things."""
    pass
```

**Consistent Return Format**:
```python
# Standard success response
{
    "success": True,
    "entity_id": "uuid",
    "message": "Entity created"
}

# Standard error response
{
    "success": False,
    "error_code": "validation_error",
    "message": "Invalid parameters",
    "details": {...}
}
```

**Idempotency**:
```python
async def create_or_update_entity(name: str, **kwargs) -> Dict:
    """Idempotent entity creation."""
    # Check if exists
    existing = await find_entity_by_name(name)

    if existing:
        # Update existing
        return await update_entity(existing["id"], **kwargs)
    else:
        # Create new
        return await create_entity(name, **kwargs)
```

### Documentation Standards

```python
async def advanced_query(
    query_text: str,
    filters: Optional[Dict] = None,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Execute advanced knowledge graph query.

    This tool performs hybrid search combining vector similarity
    and graph traversal for comprehensive results.

    Args:
        query_text: Natural language query
        filters: Optional filters
            - domain: Filter by knowledge domain
            - entity_type: Filter by entity type
            - min_confidence: Minimum confidence score (0.0-1.0)
        limit: Maximum results to return (default: 10)

    Returns:
        Dict containing:
            - success (bool): Operation status
            - results (List[Dict]): Query results
            - count (int): Number of results
            - query_time (float): Execution time in seconds

    Raises:
        ValueError: Invalid query or filters
        DatabaseError: Query execution failed

    Example:
        >>> result = await advanced_query(
        ...     query_text="neural network architectures",
        ...     filters={"domain": "artificial_intelligence"},
        ...     limit=5
        ... )
        >>> print(result["count"])
        5
    """
    pass
```
