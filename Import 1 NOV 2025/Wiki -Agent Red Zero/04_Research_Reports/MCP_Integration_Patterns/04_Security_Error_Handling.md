# Part 4 of 6: Security & Error Handling

**Series**: MCP Integration Patterns
**Navigation**: [← Part 3](./03_Communication_Tools.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 5 →](./05_Performance_FastMCP.md)

---

```python
@mcp.resource("data://user-profile/{user_id}")
async def get_user_profile(user_id: str):
    """Dynamic resource with URI template

    Accessible as: data://user-profile/123
    """
    user = await db.get_user(user_id)
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "joined": user.created_at.isoformat()
    }

@mcp.resource("data://recent-orders/{user_id}")
async def get_recent_orders(user_id: str, limit: int = 10):
    """Resource with optional parameters"""
    orders = await db.query(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        user_id, limit
    )
    return orders
```

**Use Cases**:
- User profiles: `data://user/{id}`
- File access: `file://documents/{path}`
- Database records: `db://table/{id}`
- API endpoints: `api://resource/{id}`

### Context Access Pattern

```python
from fastmcp import Context

@mcp.tool
async def log_activity(message: str, ctx: Context):
    """Access MCP session context"""

    # Send log message to client
    await ctx.log(f"Activity: {message}")

    # Access session metadata
    session_id = ctx.session.id

    # Call other resources from within tool
    user_data = await ctx.read_resource("data://user/123")

    return {"logged": True, "session": session_id}
```

**Context Capabilities**:
- Logging to client
- Reading resources
- Session management
- Request metadata access

### Streaming Results Pattern

```python
@mcp.tool
async def generate_report(data_source: str):
    """Stream results as they're generated"""

    async for chunk in process_large_dataset(data_source):
        # Yield partial results
        yield {
            "type": "progress",
            "data": chunk,
            "timestamp": time.time()
        }

    yield {"type": "complete", "status": "success"}
```

**Benefits**:
- Responsive UIs during long operations
- Real-time feedback
- Reduced memory footprint
- Early error detection

### Client Testing Pattern

```python
import pytest
from fastmcp import FastMCP
from fastmcp.client import Client

@pytest.mark.asyncio
async def test_mcp_server():
    """Test MCP server with in-memory transport"""

    # Create server
    mcp = FastMCP("test-server")

    @mcp.tool
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    # Test with client
    async with Client(mcp) as client:
        # List available tools
        tools = await client.list_tools()
        assert len(tools) == 1
        assert tools[0].name == "greet"

        # Call tool
        result = await client.call_tool("greet", {"name": "World"})
        assert result == "Hello, World!"
```

### Server Composition Pattern

```python
from fastmcp import FastMCP, compose_servers

# Create specialized servers
auth_server = FastMCP("auth")
data_server = FastMCP("data")

@auth_server.tool
async def authenticate(token: str):
    return {"valid": validate_token(token)}

@data_server.tool
async def query_data(sql: str):
    return await db.execute(sql)

# Compose into single server
app = compose_servers(auth_server, data_server)

# Now exposes both auth and data tools
```

**Use Cases**:
- Modular server design
- Service composition
- Team collaboration (different teams own different servers)
- Incremental development

### Proxy Pattern

```python
from fastmcp import FastMCP, proxy_to

# Proxy to existing MCP server
remote_server = FastMCP("proxy")

# Forward all calls to remote server
remote_server.proxy_to("https://api.example.com/mcp")

# Can also transform requests/responses
@remote_server.middleware
async def transform_request(request):
    # Add authentication
    request.headers["Authorization"] = f"Bearer {get_token()}"
    return request
```

### OpenAPI Generation Pattern

```python
from fastmcp import FastMCP

mcp = FastMCP("api-server")

# Define MCP tools
@mcp.tool
async def create_user(name: str, email: str) -> dict:
    """Create a new user"""
    user = await db.create_user(name, email)
    return {"id": user.id, "name": user.name}

# Generate OpenAPI spec
openapi_spec = mcp.to_openapi()

# Generate FastAPI routes
fastapi_app = mcp.to_fastapi()

# Now callable as REST API
# POST /tools/create_user
# {"name": "John", "email": "john@example.com"}
```

**Benefits**:
- Dual interface: MCP + REST API
- Automatic OpenAPI documentation
- Easy integration with existing systems
- Standard HTTP clients can consume

### Authentication Integration

```python
from fastmcp import FastMCP
from fastmcp.auth import GoogleAuth, GitHubAuth, WorkOSAuth

mcp = FastMCP("secure-app")

# Multiple auth providers
mcp.add_auth(GoogleAuth(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
))

mcp.add_auth(GitHubAuth(
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET")
))

@mcp.tool(requires_auth=True)
async def protected_action(data: str, ctx: Context):
    """Only accessible with valid authentication"""
    user = ctx.user  # Authenticated user info
    return f"Processing for {user.email}: {data}"
```

**Supported Providers**:
- Google OAuth
- GitHub OAuth
- WorkOS (enterprise SSO)
- Azure AD
- Auth0
- Custom OAuth 2.0 providers

### Error Handling Pattern

```python
from fastmcp import FastMCP, MCPError

mcp = FastMCP("robust-server")

@mcp.tool
async def risky_operation(data: str):
    """Operation with proper error handling"""
    try:
        result = await process(data)
        return result

    except ValidationError as e:
        # Client error - don't retry
        raise MCPError(
            code=-32602,
            message="Invalid parameters",
            data={"details": str(e)},
            retryable=False
        )

    except DatabaseError as e:
        # Server error - retryable
        raise MCPError(
            code=-32603,
            message="Database error",
            data={"details": "Temporary issue"},
            retryable=True
        )

# FastMCP automatically structures error responses
```

### TypeScript Implementation

```typescript
import { FastMCP } from "fastmcp";
import { z } from "zod";

const server = new FastMCP({
  name: "TypeScript Server",
  version: "1.0.0",
});

// Add tool with Zod validation
server.addTool({
  name: "calculate",
  description: "Perform calculation",
  parameters: z.object({
    operation: z.enum(["add", "subtract", "multiply", "divide"]),
    a: z.number(),
    b: z.number(),
  }),
  execute: async (args) => {
    switch (args.operation) {
      case "add":
        return String(args.a + args.b);
      case "subtract":
        return String(args.a - args.b);
      case "multiply":
        return String(args.a * args.b);
      case "divide":
        if (args.b === 0) throw new Error("Division by zero");
        return String(args.a / args.b);
    }
  },
});

// Start server
await server.start({ transport: "stdio" });
```

### FastMCP vs Raw SDK Comparison

| Feature | FastMCP | Raw SDK |
|---------|---------|---------|
| Development Speed | 5x faster | Baseline |
| Boilerplate | Minimal | Significant |
| Schema Generation | Automatic | Manual |
| Validation | Built-in | Manual |
| Testing | Integrated | Manual setup |
| Auth Providers | 6+ built-in | Manual implementation |
| Server Composition | Native support | Manual |
| OpenAPI Generation | One-line | Not available |
| Learning Curve | Gentle | Steep |
| Production Ready | Yes | Requires hardening |

---

## Agent Zero Integration

Agent Zero is a dynamic, self-learning agent framework with comprehensive MCP support.

### Architecture Overview

Agent Zero is designed to be:
- **Dynamic**: Organically growing and learning as you use it
- **Transparent**: Fully readable and comprehensible
- **Customizable**: Easy to modify and extend
- **Interactive**: Direct interaction with agent processes

### MCP Integration Architecture

```
┌─────────────────────────────────────┐
│         Agent Zero Core             │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │
│  │   MCP Client System         │   │
│  │  - Server Management        │   │
│  │  - Tool Discovery           │   │
│  │  - Lifecycle Handling       │   │
│  └─────────────────────────────┘   │
│           ↓           ↓             │
│   ┌──────────┐   ┌──────────┐     │
│   │  Local   │   │  Remote  │     │
│   │  Servers │   │  Servers │     │
│   └──────────┘   └──────────┘     │
└─────────────────────────────────────┘
```

### Server Types

#### MCPServerLocal (stdio transport)

```python
from agent_zero.mcp import MCPServerLocal

# Configure local MCP server
local_server = MCPServerLocal(
    name="sqlite",
    command="uvx",
    args=["mcp-server-sqlite", "--db-path", "./data.db"],
    env={"LOG_LEVEL": "info"}
)

# Agent Zero manages subprocess lifecycle
await local_server.start()

# Tools automatically available to agent
# Called as: sqlite.query, sqlite.execute, etc.
```

**Features**:
- Automatic subprocess management
- stdio transport handling
- Error recovery and restart
- Output logging

#### MCPServerRemote (HTTP/SSE transport)

```python
from agent_zero.mcp import MCPServerRemote

# Configure remote MCP server
remote_server = MCPServerRemote(
    name="github",
    url="https://api.github.com/mcp",
    auth_token=os.getenv("GITHUB_TOKEN"),
    transport="sse"  # or "streamable-http"
)

await remote_server.connect()

# Tools available as: github.create_issue, github.search_code, etc.
```

**Features**:
- HTTP/SSE connection management
- Authentication handling
- Automatic reconnection
- Network error recovery

### Tool Namespacing

```python
# Agent Zero namespaces tools to avoid conflicts
# Format: {server_name}.{tool_name}

# SQLite server tools
await agent.call_tool("sqlite.query", {"sql": "SELECT * FROM users"})
await agent.call_tool("sqlite.execute", {"sql": "INSERT INTO..."})

# GitHub server tools
await agent.call_tool("github.create_issue", {
    "repo": "user/repo",
    "title": "Bug report",
    "body": "Description..."
})

# No naming conflicts even if tools have same base name
```

### Configuration Pattern

```yaml
# agent_config.yaml
mcp_servers:
  # Local servers
  sqlite:
    type: local
    command: uvx
    args:
      - mcp-server-sqlite
      - --db-path
      - ./database.db

  filesystem:
    type: local
    command: python
    args:
      - -m
      - mcp_server_filesystem
      - --root
      - /workspace

  # Remote servers
  github:
    type: remote
    url: https://api.github.com/mcp
    transport: sse
    auth:
      type: bearer
      token_env: GITHUB_TOKEN

  custom_api:
    type: remote
    url: https://mcp.example.com
    transport: streamable-http
    auth:
      type: oauth2
      client_id_env: API_CLIENT_ID
      client_secret_env: API_CLIENT_SECRET
```

### Automatic Tool Discovery

```python
# Agent Zero automatically discovers tools on server connection
class AgentZero:
    async def connect_mcp_servers(self):
        """Connect to all configured MCP servers"""
        for server_name, config in self.mcp_config.items():
            server = self._create_server(server_name, config)
            await server.connect()

            # Discover available tools
            tools = await server.list_tools()

            # Register with agent
            for tool in tools:
                namespaced_name = f"{server_name}.{tool.name}"
                self.register_tool(namespaced_name, tool)


---

**Navigation**: [← Part 3](./03_Communication_Tools.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 5 →](./05_Performance_FastMCP.md)
**Part 4 of 6** | Lines 1441-1920 of original document
