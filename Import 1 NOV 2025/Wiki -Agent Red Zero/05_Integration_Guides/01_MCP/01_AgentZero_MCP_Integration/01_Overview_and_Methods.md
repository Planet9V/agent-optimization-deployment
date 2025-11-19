---
title: AgentZero MCP Integration - Overview and Methods
category: 05_Integration_Guides/01_MCP/01_AgentZero_MCP_Integration
last_updated: 2025-10-25
line_count: 250
status: published
tags: [mcp, integration, docker, networking, configuration]
---

# AgentZero MCP Integration - Overview and Methods

**Purpose**: Connect AgentZero Docker container to MCP (Model Context Protocol) servers running on your host machine
**Date**: 2025-10-17
**Status**: Configuration Guide

---

## 🎯 Overview

To use MCP servers (like Claude Desktop's Docker MCP Toolkit) from within the AgentZero Docker container, you need to:

1. **Network Configuration**: Allow container to access host services
2. **MCP Server Setup**: Ensure MCP servers are accessible
3. **AgentZero Configuration**: Configure AgentZero to use MCP endpoints

---

## 🔌 Architecture

```
┌─────────────────────────────────────────┐
│         Host Machine (Mac)              │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   MCP Server (Claude Desktop)    │  │
│  │   - Docker MCP Toolkit           │  │
│  │   - Sequential Thinking          │  │
│  │   - Context7                     │  │
│  │   - Other MCP Servers            │  │
│  │   Port: Various (stdio/socket)   │  │
│  └──────────────────────────────────┘  │
│                   ↕                     │
│           host.docker.internal          │
│                   ↕                     │
│  ┌──────────────────────────────────┐  │
│  │   AgentZero Container            │  │
│  │   - Python Application           │  │
│  │   - MCP Client                   │  │
│  │   - Connects to host MCP servers │  │
│  └──────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🛠️ Method 1: Using host.docker.internal (Recommended)

Docker Desktop for Mac provides a special DNS name `host.docker.internal` that resolves to the host machine's IP address.

### Step 1: Configure MCP Servers to Accept Network Connections

MCP servers typically use stdio (standard input/output) by default. To make them accessible from Docker, you need to expose them via network sockets.

**Option A: Use MCP Server with TCP Sockets**

If your MCP server supports TCP, configure it to listen on a network port:

```json
// Example MCP server configuration
{
  "mcpServers": {
    "docker": {
      "command": "docker-mcp-server",
      "args": ["--host", "0.0.0.0", "--port", "3000"],
      "env": {}
    }
  }
}
```

**Option B: Use npx with MCP over HTTP**

Some MCP servers can be run via npx with HTTP transport:

```json
{
  "mcpServers": {
    "sequential": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking",
        "--transport", "http",
        "--port", "3001"
      ]
    }
  }
}
```

### Step 2: Update AgentZero to Use Host MCP Servers

**Add environment variables to docker-compose.yml**:

```yaml
agentzero:
  image: agent0ai/agent-zero:latest
  container_name: agentzero

  environment:
    # Existing environment variables...

    # MCP Server Endpoints (on host)
    - MCP_DOCKER_URL=http://host.docker.internal:3000
    - MCP_SEQUENTIAL_URL=http://host.docker.internal:3001
    - MCP_CONTEXT7_URL=http://host.docker.internal:3002
    - MCP_MAGIC_URL=http://host.docker.internal:3003

    # Enable MCP in AgentZero
    - ENABLE_MCP=true
```

### Step 3: Install MCP Client in AgentZero

**Add to AgentZero's requirements or install manually**:

```bash
# Inside AgentZero container
docker exec -it agentzero pip install mcp anthropic-mcp-client
```

### Step 4: Configure AgentZero to Use MCP

Create a configuration file in AgentZero:

```python
# /app/conf/mcp_config.py
import os

MCP_SERVERS = {
    "docker": {
        "url": os.getenv("MCP_DOCKER_URL", "http://host.docker.internal:3000"),
        "enabled": os.getenv("ENABLE_MCP", "false").lower() == "true"
    },
    "sequential": {
        "url": os.getenv("MCP_SEQUENTIAL_URL", "http://host.docker.internal:3001"),
        "enabled": os.getenv("ENABLE_MCP", "false").lower() == "true"
    },
    "context7": {
        "url": os.getenv("MCP_CONTEXT7_URL", "http://host.docker.internal:3002"),
        "enabled": os.getenv("ENABLE_MCP", "false").lower() == "true"
    }
}

def get_mcp_client(server_name):
    """Get MCP client for specified server"""
    if server_name not in MCP_SERVERS:
        raise ValueError(f"Unknown MCP server: {server_name}")

    config = MCP_SERVERS[server_name]
    if not config["enabled"]:
        return None

    from anthropic_mcp_client import MCPClient
    return MCPClient(config["url"])
```

---

## 🛠️ Method 2: Using Docker Network Mode (Alternative)

Run AgentZero with `--network="host"` to share the host's network namespace.

**Warning**: This removes network isolation and may cause port conflicts.

**Update docker-compose.yml**:

```yaml
agentzero:
  image: agent0ai/agent-zero:latest
  container_name: agentzero
  network_mode: "host"  # Use host network

  # Remove ports section (not needed with host network)
  # ports:
  #   - "50001:80"
```

**Then access MCP servers via localhost**:

```python
MCP_DOCKER_URL = "http://localhost:3000"
MCP_SEQUENTIAL_URL = "http://localhost:3001"
```

---

## 🛠️ Method 3: Running MCP Servers Inside Docker (Best Integration)

Instead of accessing host MCP servers, run MCP servers as Docker containers in the same network.

### Step 1: Add MCP Server Containers

**Update docker-compose.yml**:

```yaml
services:
  # Existing services...

  mcp-docker:
    image: node:20-alpine
    container_name: mcp-docker
    working_dir: /app
    command: npx -y @modelcontextprotocol/server-docker
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - agentzero-network
    restart: unless-stopped

  mcp-sequential:
    image: node:20-alpine
    container_name: mcp-sequential
    working_dir: /app
    command: npx -y @modelcontextprotocol/server-sequential-thinking
    networks:
      - agentzero-network
    restart: unless-stopped

  mcp-context7:
    image: node:20-alpine
    container_name: mcp-context7
    working_dir: /app
    command: npx -y @modelcontextprotocol/server-context7
    networks:
      - agentzero-network
    restart: unless-stopped
```

### Step 2: Update AgentZero Environment

```yaml
agentzero:
  environment:
    # MCP servers accessible by container name
    - MCP_DOCKER_URL=http://mcp-docker:3000
    - MCP_SEQUENTIAL_URL=http://mcp-sequential:3001
    - MCP_CONTEXT7_URL=http://mcp-context7:3002
    - ENABLE_MCP=true
```

### Step 3: Restart Stack

```bash
docker-compose down
docker-compose up -d
```

---

## 🎯 Recommended Setup

**For Development** (Easiest):
1. Use Method 1 (host.docker.internal)
2. Run MCP servers on host via Claude Desktop
3. Configure AgentZero to connect via host.docker.internal

**For Production** (Most Reliable):
1. Use Method 3 (MCP servers in Docker)
2. All services in same Docker network
3. No dependency on host services

---

## Related Topics

- [Integration Examples and Troubleshooting](02_Integration_Examples.md)
- [Docker MCP Toolkit](../02_Docker_MCP_Toolkit.md)

## See Also

- MCP Documentation: https://modelcontextprotocol.io
- Docker Networking: https://docs.docker.com/desktop/networking/

---
**Last Updated:** 2025-10-25 | **Lines:** 250/400 | **Status:** published
