---
title: Creating Custom Incarnations (Part 1 of 2)
category: 03_Incarnations
last_updated: 2025-10-25
line_count: 345
status: published
tags: [neocoder, mcp, documentation]
---


# Creating Custom Incarnations

[← Back to Integration Patterns](06_Integration_Patterns.md)

## Overview

This guide walks through creating custom incarnations for domain-specific workflows. Learn how to extend NeoCoder with specialized tools, schemas, and patterns tailored to your specific use cases.

## Prerequisites

- Python 3.10+ installed
- NeoCoder development environment setup
- Neo4j database access
- Basic understanding of MCP protocol
- Familiarity with Cypher query language

## Incarnation Architecture

### BaseIncarnation Class

All incarnations extend `BaseIncarnation`:

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Any

class IncarnationType(Enum):
    """Enumeration of incarnation types."""
    CODING = "coding"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    CODE_ANALYSIS = "code_analysis"
    RESEARCH = "research"
    DECISION_SUPPORT = "decision_support"
    DATA_ANALYSIS = "data_analysis"
    COMPLEX_SYSTEM = "complex_system"
    # Add custom types here

class BaseIncarnation(ABC):
    """Base class for all incarnations."""

    incarnation_type: IncarnationType
    description: str
    version: str

    def __init__(self, driver, config: Dict[str, Any]):
        """Initialize incarnation with Neo4j driver and configuration."""
        self.driver = driver
        self.config = config
        self.tools = []
        self.guidance_hubs = []

    @abstractmethod
    async def initialize_schema(self):
        """Initialize Neo4j schema (constraints, indexes)."""
        pass

    @abstractmethod
    async def initialize_tools(self):
        """Register incarnation-specific tools."""
        pass

    @abstractmethod
    async def get_guidance_hubs(self) -> List[str]:
        """Return list of guidance hub names."""
        pass

    async def cleanup(self):
        """Cleanup resources when switching incarnations."""
        # Override if custom cleanup needed
        pass

    async def validate_state(self) -> bool:
        """Validate incarnation state is consistent."""
        # Override for custom validation
        return True
```

## Step-by-Step Development

### Step 1: Define Incarnation Purpose

**Example**: Create incarnation for API design and documentation

```python
# incarnations/api_design.py

from neocoder_mcp.incarnations.base import BaseIncarnation, IncarnationType
from enum import Enum

class APIDesignIncarnation(BaseIncarnation):
    """
    API Design Incarnation

    Purpose: Design, document, and version RESTful APIs

    Use Cases:
    - API endpoint design and specification
    - OpenAPI/Swagger documentation
    - API versioning and changelog
    - Request/response schema management
    - API testing and validation
    """

    incarnation_type = IncarnationType.API_DESIGN  # Add to enum
    description = "RESTful API design and documentation"
    version = "1.0.0"
```

### Step 2: Design Neo4j Schema

**Node Types**:
```python
async def initialize_schema(self):
    """Initialize API Design schema."""

    schema_queries = [
        # Constraints
        """
        CREATE CONSTRAINT unique_api_endpoint IF NOT EXISTS
        FOR (e:APIEndpoint)
        REQUIRE e.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT unique_api_schema IF NOT EXISTS
        FOR (s:APISchema)
        REQUIRE s.id IS UNIQUE
        """,

        # Indexes
        """
        CREATE INDEX api_endpoint_path IF NOT EXISTS
        FOR (e:APIEndpoint)
        ON (e.path)
        """,
        """
        CREATE INDEX api_endpoint_method IF NOT EXISTS
        FOR (e:APIEndpoint)
        ON (e.method)
        """,
        """
        CREATE INDEX api_version IF NOT EXISTS
        FOR (v:APIVersion)
        ON (v.version)
        """
    ]

    async with self.driver.session() as session:
        for query in schema_queries:
            await session.run(query)
```

**Schema Design**:
```cypher
-- APIEndpoint node
CREATE (endpoint:APIEndpoint {
  id: randomUUID(),
  path: '/api/v1/users/{id}',
  method: 'GET',
  description: 'Retrieve user by ID',
  deprecated: false,
  created: datetime(),
  updated: datetime()
})

-- APISchema node
CREATE (schema:APISchema {
  id: randomUUID(),
  name: 'User',
  type: 'object',
  schema_json: {...},  // JSON Schema definition
  created: datetime()
})

-- APIVersion node
CREATE (version:APIVersion {
  id: randomUUID(),
  version: 'v1',
  release_date: date('2024-01-15'),
  deprecated: false,
  changelog: 'Initial release'
})

-- Relationships
(endpoint)-[:HAS_REQUEST_SCHEMA]->(request_schema:APISchema)
(endpoint)-[:HAS_RESPONSE_SCHEMA]->(response_schema:APISchema)
(endpoint)-[:BELONGS_TO_VERSION]->(version:APIVersion)
(endpoint)-[:DEPRECATED_BY]->(new_endpoint:APIEndpoint)
```

### Step 3: Implement Tools

**Tool Definition Pattern**:
```python
from neocoder_mcp.tools import tool_decorator
from pydantic import BaseModel, Field

class CreateEndpointInput(BaseModel):
    """Input schema for create_endpoint tool."""
    path: str = Field(..., description="API endpoint path")
    method: str = Field(..., description="HTTP method (GET, POST, etc.)")
    description: str = Field(..., description="Endpoint description")
    request_schema_id: str = Field(None, description="Request schema ID")
    response_schema_id: str = Field(None, description="Response schema ID")
    version: str = Field("v1", description="API version")

@tool_decorator(
    name="create_api_endpoint",
    description="Create new API endpoint specification",
    input_schema=CreateEndpointInput
)
async def create_endpoint_tool(
    self,
    path: str,
    method: str,
    description: str,
    request_schema_id: str = None,
    response_schema_id: str = None,
    version: str = "v1"
) -> Dict[str, Any]:
    """Create API endpoint in Neo4j."""

    # Validation
    valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    if method.upper() not in valid_methods:
        return {
            "success": False,
            "error": f"Invalid method. Must be one of: {valid_methods}"
        }

    # Execute creation
    query = """
    CREATE (endpoint:APIEndpoint {
      id: randomUUID(),
      path: $path,
      method: $method,
      description: $description,
      deprecated: false,
      created: datetime(),
      updated: datetime()
    })

    WITH endpoint
    OPTIONAL MATCH (req_schema:APISchema {id: $request_schema_id})
    OPTIONAL MATCH (res_schema:APISchema {id: $response_schema_id})
    OPTIONAL MATCH (version:APIVersion {version: $version})

    FOREACH (ignoreMe IN CASE WHEN req_schema IS NOT NULL THEN [1] ELSE [] END |
      CREATE (endpoint)-[:HAS_REQUEST_SCHEMA]->(req_schema)
    )
    FOREACH (ignoreMe IN CASE WHEN res_schema IS NOT NULL THEN [1] ELSE [] END |
      CREATE (endpoint)-[:HAS_RESPONSE_SCHEMA]->(res_schema)
    )
    FOREACH (ignoreMe IN CASE WHEN version IS NOT NULL THEN [1] ELSE [] END |
      CREATE (endpoint)-[:BELONGS_TO_VERSION]->(version)
    )

    RETURN endpoint
    """

    async with self.driver.session() as session:
        result = await session.run(query, {
            "path": path,
            "method": method.upper(),
            "description": description,
            "request_schema_id": request_schema_id,
            "response_schema_id": response_schema_id,
            "version": version
        })

        record = await result.single()
        if not record:
            return {"success": False, "error": "Failed to create endpoint"}

        endpoint = dict(record["endpoint"])

        return {
            "success": True,
            "endpoint_id": endpoint["id"],
            "endpoint": endpoint,
            "message": f"Created {method} {path} endpoint"
        }
```

**Complete Tool Set**:
```python
async def initialize_tools(self):
    """Register all API Design tools."""

    self.tools = [
        self.create_endpoint_tool,
        self.create_schema_tool,
        self.create_version_tool,
        self.get_endpoint_tool,
        self.update_endpoint_tool,
        self.deprecate_endpoint_tool,
        self.generate_openapi_spec_tool,
        self.validate_api_consistency_tool
    ]

    # Register tools with MCP server
    for tool in self.tools:
        await self.register_tool(tool)
```

### Step 4: Create Guidance Hubs

**Guidance Hub Content**:
```python
async def get_guidance_hubs(self) -> List[str]:
    """Return guidance hub names for API Design."""
    return [
        'api_design_guide',
        'api_versioning_guide',
        'api_testing_guide'
    ]

async def create_guidance_hubs(self):
    """Create guidance hub content in Neo4j."""

    api_design_guide = """
# API Design Guide

## Best Practices

### RESTful Principles
- Use nouns for resources (/users, not /getUsers)
- HTTP methods for actions (GET, POST, PUT, DELETE)
- Consistent naming conventions
- Proper status codes

### Endpoint Design
1. Create version first: `create_api_version`
2. Define schemas: `create_api_schema`
3. Create endpoints: `create_api_endpoint`
4. Link schemas to endpoints
5. Generate OpenAPI spec: `generate_openapi_spec`

### Schema Management
- Use JSON Schema for request/response
- Version schemas alongside endpoints
- Reuse common schemas
- Document all fields
