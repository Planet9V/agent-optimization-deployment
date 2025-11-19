---
title: 1. Create API version (Part 2 of 2)
category: 03_Incarnations
last_updated: 2025-10-25
line_count: 160
status: published
tags: [neocoder, mcp, documentation]
---

## Example Workflow

```python
# 1. Create API version
version = await create_api_version(
    version="v1",
    release_date="2024-01-15"
)

# 2. Create request schema
user_schema = await create_api_schema(
    name="User",
    type="object",
    schema_json={
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "email": {"type": "string", "format": "email"},
            "name": {"type": "string"}
        },
        "required": ["email", "name"]
    }
)

# 3. Create endpoint
endpoint = await create_api_endpoint(
    path="/api/v1/users",
    method="POST",
    description="Create new user",
    request_schema_id=user_schema["id"],
    response_schema_id=user_schema["id"],
    version="v1"
)

# 4. Generate OpenAPI spec
spec = await generate_openapi_spec(version="v1")
```
    """

    # Store in Neo4j
    query = """
    MERGE (hub:GuidanceHub {name: 'api_design_guide'})
    SET hub.content = $content,
        hub.updated = datetime()
    RETURN hub
    """

    async with self.driver.session() as session:
        await session.run(query, {"content": api_design_guide})
```

### Step 5: Implement Validation

```python
async def validate_state(self) -> bool:
    """Validate API Design incarnation state."""

    validation_checks = []

    # Check 1: No orphaned schemas
    query_orphan_schemas = """
    MATCH (schema:APISchema)
    WHERE NOT (schema)<-[:HAS_REQUEST_SCHEMA|HAS_RESPONSE_SCHEMA]-()
    RETURN count(schema) as orphan_count
    """

    async with self.driver.session() as session:
        result = await session.run(query_orphan_schemas)
        record = await result.single()
        orphan_count = record["orphan_count"]

        validation_checks.append({
            "name": "orphan_schemas",
            "passed": orphan_count == 0,
            "message": f"Found {orphan_count} orphaned schemas"
        })

    # Check 2: All endpoints have valid methods
    query_invalid_methods = """
    MATCH (endpoint:APIEndpoint)
    WHERE NOT endpoint.method IN ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
    RETURN count(endpoint) as invalid_count
    """

    async with self.driver.session() as session:
        result = await session.run(query_invalid_methods)
        record = await result.single()
        invalid_count = record["invalid_count"]

        validation_checks.append({
            "name": "valid_methods",
            "passed": invalid_count == 0,
            "message": f"Found {invalid_count} endpoints with invalid methods"
        })

    # Check 3: All endpoints belong to a version
    query_unversioned = """
    MATCH (endpoint:APIEndpoint)
    WHERE NOT (endpoint)-[:BELONGS_TO_VERSION]->()
    RETURN count(endpoint) as unversioned_count
    """

    async with self.driver.session() as session:
        result = await session.run(query_unversioned)
        record = await result.single()
        unversioned_count = record["unversioned_count"]

        validation_checks.append({
            "name": "versioned_endpoints",
            "passed": unversioned_count == 0,
            "message": f"Found {unversioned_count} unversioned endpoints"
        })

    # Return validation result
    all_passed = all(check["passed"] for check in validation_checks)

    if not all_passed:
        failed = [c for c in validation_checks if not c["passed"]]
        logger.warning(f"Validation failed: {failed}")

    return all_passed
```

### Step 6: Implement Cleanup

```python
async def cleanup(self):
    """Cleanup resources when switching incarnations."""

    # Save current state
    await self.save_incarnation_state()

    # Clear tool cache
    self.tools.clear()

    # Validate before exit
    if not await self.validate_state():
        logger.warning("Incarnation state validation failed on cleanup")

    # Optional: Archive old data
    await self.archive_old_entities(days=90)

async def save_incarnation_state(self):
    """Save current incarnation state."""
    query = """
    MERGE (state:IncarnationState {incarnation: 'api_design'})
    SET state.last_active = datetime(),
        state.endpoint_count = (
          MATCH (e:APIEndpoint) RETURN count(e)
        ),
        state.schema_count = (
          MATCH (s:APISchema) RETURN count(s)
        )
    RETURN state
    """

    async with self.driver.session() as session:
        await session.run(query)
```
