---
title: AgentZero MCP Integration - Examples and Troubleshooting
category: 05_Integration_Guides/01_MCP/01_AgentZero_MCP_Integration
last_updated: 2025-10-25
line_count: 286
status: published
tags: [mcp, integration, python, troubleshooting, testing]
---

# AgentZero MCP Integration - Examples and Troubleshooting

## 🧪 Testing MCP Connection

### Test 1: Verify Host Access from Container

```bash
# From inside AgentZero container
docker exec agentzero ping -c 3 host.docker.internal

# Test HTTP connection to host
docker exec agentzero curl -v http://host.docker.internal:3000
```

### Test 2: Test MCP Server Availability

```bash
# Check if MCP server is running on host
curl http://localhost:3000/health

# From inside container
docker exec agentzero curl http://host.docker.internal:3000/health
```

### Test 3: Python MCP Client Test

```python
# Inside AgentZero container
# Create test script: /app/test_mcp.py

import requests
import json

def test_mcp_server(url):
    try:
        response = requests.post(
            url,
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 1
            },
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Test MCP Docker server
test_mcp_server("http://host.docker.internal:3000")
```

---

## 📝 Example: AgentZero MCP Integration

### Create MCP Integration Module

**File**: `/app/python/helpers/mcp_helper.py`

```python
import os
import requests
from typing import Dict, Any, Optional

class MCPHelper:
    """Helper class for MCP server integration"""

    def __init__(self):
        self.servers = {
            "docker": os.getenv("MCP_DOCKER_URL", "http://host.docker.internal:3000"),
            "sequential": os.getenv("MCP_SEQUENTIAL_URL", "http://host.docker.internal:3001"),
            "context7": os.getenv("MCP_CONTEXT7_URL", "http://host.docker.internal:3002"),
        }
        self.enabled = os.getenv("ENABLE_MCP", "false").lower() == "true"

    def call_tool(self, server: str, tool_name: str, arguments: Dict[str, Any]) -> Optional[Dict]:
        """Call MCP tool on specified server"""
        if not self.enabled:
            return None

        if server not in self.servers:
            raise ValueError(f"Unknown MCP server: {server}")

        url = self.servers[server]

        try:
            response = requests.post(
                url,
                json={
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments
                    },
                    "id": 1
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"MCP Error: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"MCP Connection Error: {e}")
            return None

    def list_tools(self, server: str) -> Optional[list]:
        """List available tools on MCP server"""
        if not self.enabled:
            return None

        if server not in self.servers:
            raise ValueError(f"Unknown MCP server: {server}")

        url = self.servers[server]

        try:
            response = requests.post(
                url,
                json={
                    "jsonrpc": "2.0",
                    "method": "tools/list",
                    "params": {},
                    "id": 1
                },
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("result", {}).get("tools", [])
            else:
                return None

        except requests.exceptions.RequestException as e:
            print(f"MCP Connection Error: {e}")
            return None

# Global instance
mcp = MCPHelper()
```

### Use MCP in AgentZero Instruments

**Example: Docker Container Management Tool**

```python
# In an AgentZero instrument
from python.helpers.mcp_helper import mcp

def docker_list_containers():
    """List Docker containers using MCP Docker server"""
    result = mcp.call_tool(
        server="docker",
        tool_name="list_containers",
        arguments={"all": True}
    )

    if result:
        return result.get("result", {})
    else:
        # Fallback to direct docker command
        import subprocess
        output = subprocess.check_output(["docker", "ps", "-a"])
        return output.decode()
```

---

## 🔍 Troubleshooting

### Issue 1: Cannot Connect to host.docker.internal

**Symptom**: `ping: host.docker.internal: Name or service not known`

**Solution**: Use the host's IP address instead:

```bash
# Find host IP from inside container
ip route | grep default | awk '{print $3}'

# Or use this in docker-compose.yml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

### Issue 2: MCP Server Not Responding

**Check MCP server is running on host**:
```bash
ps aux | grep mcp
lsof -i :3000  # Check port 3000
```

**Check firewall**:
```bash
# macOS: Allow connections to MCP ports
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /path/to/mcp-server
```

### Issue 3: Connection Refused

**Verify MCP server binds to 0.0.0.0, not 127.0.0.1**:
```bash
# Bad (only localhost)
node server.js --host 127.0.0.1 --port 3000

# Good (all interfaces)
node server.js --host 0.0.0.0 --port 3000
```

---

## 📋 Quick Start Checklist

```
Setup MCP Integration:
[ ] Identify which MCP servers you want to use
[ ] Choose integration method (host.docker.internal recommended)
[ ] Configure MCP servers to accept network connections
[ ] Add MCP environment variables to docker-compose.yml
[ ] Install MCP client in AgentZero container
[ ] Create MCP helper module
[ ] Test connection from container to host
[ ] Verify MCP tool calls work
[ ] Integrate MCP tools into AgentZero instruments
```

---

## 📚 Resources

**MCP Documentation**:
- Model Context Protocol: https://modelcontextprotocol.io
- MCP Servers: https://github.com/modelcontextprotocol/servers

**Docker Networking**:
- host.docker.internal: https://docs.docker.com/desktop/networking/#i-want-to-connect-from-a-container-to-a-service-on-the-host
- Docker Networks: https://docs.docker.com/network/

**AgentZero**:
- AgentZero GitHub: https://github.com/frdel/agent-zero
- AgentZero Docs: https://github.com/frdel/agent-zero/tree/main/docs

---

## 🎉 Next Steps

1. **Choose your integration method** (host.docker.internal recommended)
2. **Configure MCP servers** to accept network connections
3. **Update docker-compose.yml** with MCP environment variables
4. **Test connectivity** from AgentZero to MCP servers
5. **Create MCP helper module** for AgentZero integration
6. **Build instruments** that leverage MCP tools

---

## Related Topics

- [Overview and Configuration Methods](01_Overview_and_Methods.md)
- [Docker MCP Toolkit](../02_Docker_MCP_Toolkit.md)

---
**Last Updated:** 2025-10-25 | **Lines:** 286/400 | **Status:** published
**Complexity**: Intermediate
**Time Required**: 30-60 minutes
