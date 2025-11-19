---
title: Creating Custom Tools (Part 1 of 2)
category: 07_Development
last_updated: 2025-10-25
line_count: 420
status: published
tags: [neocoder, mcp, documentation]
---


# Creating Custom Tools

[← Back to Creating Incarnations](../03_Incarnations/07_Creating_Incarnations.md) | [Next: Creating Templates →](02_Creating_Templates.md)

## Overview

NeoCoder's tool system allows you to extend incarnation capabilities with custom tools. This guide covers tool development, registration, and best practices for creating production-ready tools.

## Tool Architecture

### Base Tool Structure

```python
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from abc import ABC, abstractmethod

class ToolParameter(BaseModel):
    """Parameter definition for tool."""
    name: str
    type: str  # 'string', 'integer', 'boolean', 'object', 'array'
    description: str
    required: bool = True
    default: Optional[Any] = None
    enum: Optional[List[str]] = None

class ToolDefinition(BaseModel):
    """Tool definition for MCP."""
    name: str
    description: str
    inputSchema: Dict[str, Any]
```

### Tool Implementation

```python
async def create_knowledge_entity(
    name: str,
    entity_type: str,
    description: str = "",
    domain: Optional[str] = None,
    properties: Optional[Dict] = None,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create a new knowledge entity in Neo4j.

    Args:
        name: Entity name
        entity_type: Type (concept, technology, person, organization)
        description: Detailed description
        domain: Knowledge domain
        properties: Additional properties
        tags: Classification tags

    Returns:
        Dict with entity_id and success status

    Raises:
        ValueError: Invalid parameters
        Neo4jError: Database operation failed
    """
    # Validation
    if not name or not name.strip():
        raise ValueError("Entity name cannot be empty")

    if entity_type not in ['concept', 'technology', 'person', 'organization']:
        raise ValueError(f"Invalid entity_type: {entity_type}")

    try:
        async with get_neo4j_session() as session:
            result = await session.run("""
                CREATE (e:KnowledgeEntity {
                  id: randomUUID(),
                  name: $name,
                  type: $entity_type,
                  description: $description,
                  domain: $domain,
                  properties: $properties,
                  tags: $tags,
                  created: datetime(),
                  updated: datetime()
                })
                RETURN e.id as entity_id
            """, {
                "name": name.strip(),
                "entity_type": entity_type,
                "description": description,
                "domain": domain,
                "properties": properties or {},
                "tags": tags or []
            })

            record = await result.single()
            entity_id = record["entity_id"]

            return {
                "success": True,
                "entity_id": entity_id,
                "message": f"Created entity '{name}'"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to create entity: {e}"
        }
```

## Tool Registration

### Incarnation Tool Registry

```python
class KnowledgeGraphIncarnation(BaseIncarnation):
    """Knowledge graph management incarnation."""

    def __init__(self):
        super().__init__(
            incarnation_type=IncarnationType.KNOWLEDGE_GRAPH,
            description="Knowledge entity and relationship management"
        )

    def get_tools(self) -> List[ToolDefinition]:
        """Return available tools for this incarnation."""
        return [
            ToolDefinition(
                name="create_knowledge_entity",
                description="Create a new knowledge entity",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Entity name"
                        },
                        "entity_type": {
                            "type": "string",
                            "enum": ["concept", "technology", "person", "organization"],
                            "description": "Entity type"
                        },
                        "description": {
                            "type": "string",
                            "description": "Entity description"
                        },
                        "domain": {
                            "type": "string",
                            "description": "Knowledge domain (optional)"
                        }
                    },
                    "required": ["name", "entity_type"]
                }
            ),
            # Additional tools...
        ]
```

### MCP Server Registration

```python
from mcp.server import Server
from mcp.types import Tool

class NeoCoderMCPServer:
    """MCP server for NeoCoder."""

    def __init__(self):
        self.server = Server("neocoder")
        self.incarnations = {}
        self.current_incarnation = None

    async def initialize(self):
        """Initialize server and incarnations."""
        # Load incarnations
        self.incarnations = {
            IncarnationType.KNOWLEDGE_GRAPH: KnowledgeGraphIncarnation(),
            IncarnationType.CODING: CodingIncarnation(),
            # etc.
        }

        # Register tools from all incarnations
        for incarnation in self.incarnations.values():
            for tool_def in incarnation.get_tools():
                @self.server.tool(tool_def.name)
                async def tool_handler(**kwargs):
                    return await self._handle_tool_call(
                        tool_def.name,
                        kwargs
                    )

    async def _handle_tool_call(
        self,
        tool_name: str,
        params: Dict
    ) -> Any:
        """Route tool calls to appropriate incarnation."""
        # Find incarnation with this tool
        for incarnation in self.incarnations.values():
            if tool_name in [t.name for t in incarnation.get_tools()]:
                return await incarnation.execute_tool(tool_name, params)

        raise ValueError(f"Unknown tool: {tool_name}")
```

## Parameter Validation

### Input Validation

```python
from pydantic import BaseModel, validator, Field

class CreateEntityParams(BaseModel):
    """Parameters for create_knowledge_entity."""
    name: str = Field(..., min_length=1, max_length=200)
    entity_type: str
    description: str = ""
    domain: Optional[str] = None
    properties: Optional[Dict] = Field(default_factory=dict)
    tags: Optional[List[str]] = Field(default_factory=list)

    @validator('name')
    def validate_name(cls, v):
        """Validate entity name."""
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @validator('entity_type')
    def validate_type(cls, v):
        """Validate entity type."""
        valid_types = ['concept', 'technology', 'person', 'organization']
        if v not in valid_types:
            raise ValueError(f"Type must be one of: {', '.join(valid_types)}")
        return v

    @validator('tags')
    def validate_tags(cls, v):
        """Validate tags list."""
        if v and len(v) > 20:
            raise ValueError("Maximum 20 tags allowed")
        return v

async def create_knowledge_entity(**kwargs) -> Dict:
    """Create knowledge entity with validation."""
    try:
        # Validate parameters
        params = CreateEntityParams(**kwargs)

        # Execute with validated params
        return await _create_entity_impl(params)

    except ValidationError as e:
        return {
            "success": False,
            "error": "validation_error",
            "details": e.errors()
        }
```

### Schema Validation

```python
def validate_tool_schema(tool_def: ToolDefinition) -> bool:
    """Validate tool definition schema."""
    required_fields = ['type', 'properties', 'required']

    schema = tool_def.inputSchema
    if not all(field in schema for field in required_fields):
        raise ValueError(f"Schema missing required fields: {required_fields}")

    # Validate property types
    valid_types = ['string', 'integer', 'number', 'boolean', 'object', 'array']
    for prop_name, prop_def in schema['properties'].items():
        if prop_def.get('type') not in valid_types:
            raise ValueError(f"Invalid type for {prop_name}")

    return True
```

## Error Handling

### Robust Error Handling

```python
from enum import Enum

class ErrorCode(Enum):
    """Standard error codes."""
    VALIDATION_ERROR = "validation_error"
    DATABASE_ERROR = "database_error"
    NOT_FOUND = "not_found"
    PERMISSION_DENIED = "permission_denied"
    INTERNAL_ERROR = "internal_error"

class ToolError(Exception):
    """Base exception for tool errors."""
    def __init__(self, code: ErrorCode, message: str, details: Optional[Dict] = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)

async def safe_tool_execution(tool_func, **kwargs) -> Dict:
    """Execute tool with comprehensive error handling."""
    try:
        result = await tool_func(**kwargs)
        return result

    except ValidationError as e:
        return {
            "success": False,
            "error_code": ErrorCode.VALIDATION_ERROR.value,
            "message": "Invalid parameters",
            "details": e.errors()
        }

    except Neo4jError as e:
        return {
            "success": False,
            "error_code": ErrorCode.DATABASE_ERROR.value,
            "message": "Database operation failed",
            "details": {"neo4j_error": str(e)}
        }

    except ToolError as e:
        return {
            "success": False,
            "error_code": e.code.value,
            "message": e.message,
            "details": e.details
        }

    except Exception as e:
        # Log unexpected errors
        logger.exception(f"Unexpected error in tool execution: {e}")
        return {
            "success": False,
            "error_code": ErrorCode.INTERNAL_ERROR.value,
            "message": "Internal error occurred",
            "details": {"error": str(e)}
        }
```

## Testing Tools

### Unit Tests

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_create_knowledge_entity_success():
    """Test successful entity creation."""
    # Mock Neo4j session
    mock_session = AsyncMock()
    mock_result = AsyncMock()
    mock_result.single.return_value = {"entity_id": "test-uuid"}
    mock_session.run.return_value = mock_result

    with patch('neocoder.db.get_neo4j_session', return_value=mock_session):
        result = await create_knowledge_entity(
            name="Test Entity",
            entity_type="concept",
            description="Test description"
        )

    assert result["success"] is True
    assert "entity_id" in result
    assert result["entity_id"] == "test-uuid"

@pytest.mark.asyncio
async def test_create_knowledge_entity_validation_error():
    """Test validation error handling."""
    result = await create_knowledge_entity(
        name="",  # Invalid: empty name
        entity_type="concept"
    )

    assert result["success"] is False
    assert result["error_code"] == "validation_error"
```

### Integration Tests

```python
@pytest.mark.asyncio
@pytest.mark.integration
async def test_entity_creation_integration():
    """Test entity creation with real Neo4j."""
    # Requires test Neo4j instance
    async with get_neo4j_session() as session:
        # Create entity
        result = await create_knowledge_entity(
            name="Integration Test Entity",
            entity_type="concept",
            description="Test entity for integration testing"
        )

        assert result["success"] is True
        entity_id = result["entity_id"]

        # Verify in database
        verify_result = await session.run("""
            MATCH (e:KnowledgeEntity {id: $id})
            RETURN e.name as name
        """, {"id": entity_id})

        record = await verify_result.single()
        assert record["name"] == "Integration Test Entity"

        # Cleanup
        await session.run("""
            MATCH (e:KnowledgeEntity {id: $id})
            DELETE e
        """, {"id": entity_id})
```
