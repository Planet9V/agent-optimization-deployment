# n8n MCP Server Comprehensive Installation Guide

**Date**: 2025-10-18
**Status**: ✅ Successfully Installed
**Systems Installed**: 2 Different n8n MCP Servers

---

## Overview

This document provides a comprehensive guide for installing and configuring TWO different n8n MCP servers for Claude Code CLI. Both servers are now installed and working:

1. **mcp-n8n-builder** - Workflow builder and manager (10 tools)
2. **n8n-mcp** - Node documentation and advanced n8n integration (39+ tools)

---

## System Architecture

### Current Configuration

```
Claude Code CLI (Host)
├── MCP_DOCKER (Gateway) ✓ Connected
├── n8n-workflow-builder (mcp-n8n-builder) ✓ Connected
└── n8n-mcp (czlonkowski/n8n-mcp) ✓ Connected

n8n Docker Container
└── http://localhost:5678 (Container: n8n)
    └── Docker Network: http://n8n:5678
```

---

## Installation 1: mcp-n8n-builder

### Purpose
Basic workflow creation, management, and execution tools

### Features
- 10 MCP Tools for workflow management
- Workflow CRUD operations
- Node listing
- Execution management
- Token-optimized with OUTPUT_VERBOSITY=concise

### Installation Command
```bash
claude mcp add n8n-workflow-builder \
  --env N8N_HOST=http://n8n:5678/api/v1 \
  --env N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZTA5YWMyYS05NTE5LTRhMWYtODE1ZS1kYzE5MGUxY2Y1YjciLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYwNzY1MTEwfQ.r8y-3bLzp9WlVh6uwCUbSd19ORqu0zIMrHBH5oJ3H6A \
  --env OUTPUT_VERBOSITY=concise \
  -- npx -y mcp-n8n-builder
```

### Configuration Location
**File**: `~/.claude.json` (Global)

**JSON Block**:
```json
{
  "mcpServers": {
    "n8n-workflow-builder": {
      "command": "npx",
      "args": ["-y", "mcp-n8n-builder"],
      "env": {
        "N8N_HOST": "http://n8n:5678/api/v1",
        "N8N_API_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZTA5YWMyYS05NTE5LTRhMWYtODE1ZS1kYzE5MGUxY2Y1YjciLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYwNzY1MTEwfQ.r8y-3bLzp9WlVh6uwCUbSd19ORqu0zIMrHBH5oJ3H6A",
        "OUTPUT_VERBOSITY": "concise"
      }
    }
  }
}
```

### Available Tools (10)

#### Workflow Management (7 tools)
1. `list_workflows` - List all workflows
2. `create_workflow` - Create new workflow
3. `get_workflow` - Get workflow by ID
4. `update_workflow` - Update workflow
5. `delete_workflow` - Delete workflow
6. `activate_workflow` - Enable workflow
7. `deactivate_workflow` - Disable workflow

#### Node Management (1 tool)
8. `list_available_nodes` - List all n8n nodes

#### Execution Management (2 tools)
9. `list_executions` - List execution history
10. `get_execution` - Get execution details

### Usage Examples
```
You: "List all my n8n workflows"
You: "Create a workflow with HTTP trigger and Slack notification"
You: "Activate workflow ID 5"
```

---

## Installation 2: n8n-mcp (czlonkowski)

### Purpose
Advanced n8n node documentation, validation, templates, and comprehensive workflow management

### Features
- 39+ MCP Tools
- 536 n8n nodes documented
- 2,500+ workflow templates
- AI-powered validation
- Node property documentation
- Template discovery
- Comprehensive n8n management (when API configured)

### Installation Command
```bash
claude mcp add n8n-mcp \
  --env MCP_MODE=stdio \
  --env LOG_LEVEL=error \
  --env DISABLE_CONSOLE_OUTPUT=true \
  --env N8N_API_URL=http://n8n:5678 \
  --env N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZTA5YWMyYS05NTE5LTRhMWYtODE1ZS1kYzE5MGUxY2Y1YjciLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYwNzY1MTEwfQ.r8y-3bLzp9WlVh6uwCUbSd19ORqu0zIMrHBH5oJ3H6A \
  --env WEBHOOK_SECURITY_MODE=moderate \
  -- npx n8n-mcp
```

### Configuration Location
**File**: `~/.claude.json` → `/Users/jim` project

**JSON Block**:
```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "http://n8n:5678",
        "N8N_API_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZTA5YWMyYS05NTE5LTRhMWYtODE1ZS1kYzE5MGUxY2Y1YjciLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYwNzY1MTEwfQ.r8y-3bLzp9WlVh6uwCUbSd19ORqu0zIMrHBH5oJ3H6A",
        "WEBHOOK_SECURITY_MODE": "moderate"
      }
    }
  }
}
```

### Available Tools (39+)

#### Core Documentation Tools
- `tools_documentation` - Get MCP tool documentation (START HERE!)
- `list_nodes` - List all n8n nodes with filtering
- `get_node_info` - Comprehensive node information
- `get_node_essentials` - Essential properties only (10-20 vs 200+)
- `search_nodes` - Full-text search across nodes
- `search_node_properties` - Find specific properties
- `list_ai_tools` - List AI-capable nodes
- `get_node_as_tool_info` - Use any node as AI tool

#### Template Tools
- `list_templates` - Browse 2,500+ templates
- `search_templates` - Text search templates
- `search_templates_by_metadata` - Filter by complexity/audience
- `list_node_templates` - Templates using specific nodes
- `get_template` - Get complete workflow JSON
- `get_templates_for_task` - Curated templates for tasks

#### Validation Tools
- `validate_workflow` - Complete workflow validation + AI Agent validation
- `validate_workflow_connections` - Structure and AI tool validation
- `validate_workflow_expressions` - n8n expression validation
- `validate_node_operation` - Validate node configurations
- `validate_node_minimal` - Quick required fields check

#### Advanced Tools
- `get_property_dependencies` - Property visibility conditions
- `get_node_documentation` - Parsed n8n-docs documentation
- `get_database_statistics` - Database metrics

#### n8n Management Tools (with API configured)

**Workflow Management:**
- `n8n_create_workflow` - Create workflows
- `n8n_get_workflow` - Get complete workflow
- `n8n_get_workflow_details` - Workflow with execution stats
- `n8n_get_workflow_structure` - Simplified structure
- `n8n_get_workflow_minimal` - Minimal info
- `n8n_update_full_workflow` - Complete replacement
- `n8n_update_partial_workflow` - Diff operations
- `n8n_delete_workflow` - Delete workflows
- `n8n_list_workflows` - List with filtering
- `n8n_validate_workflow` - Validate by ID
- `n8n_autofix_workflow` - Auto-fix common errors

**Execution Management:**
- `n8n_trigger_webhook_workflow` - Trigger via webhook
- `n8n_get_execution` - Execution details
- `n8n_list_executions` - List executions
- `n8n_delete_execution` - Delete execution records

**System Tools:**
- `n8n_health_check` - Check API connectivity
- `n8n_diagnostic` - Troubleshoot issues
- `n8n_list_available_tools` - List all tools

### Usage Examples
```
You: "Show me documentation for Slack nodes"
You: "Get essential properties for HTTP Request node with examples"
You: "Search templates for 'webhook to slack'"
You: "Validate this workflow configuration"
You: "List all AI-capable nodes"
You: "Find templates for beginners using OpenAI"
```

---

## Key Differences: mcp-n8n-builder vs n8n-mcp

| Feature | mcp-n8n-builder | n8n-mcp |
|---------|-----------------|---------|
| **Purpose** | Workflow management | Node documentation + management |
| **Tools** | 10 | 39+ |
| **Node Docs** | No | ✅ 536 nodes |
| **Templates** | No | ✅ 2,500+ |
| **Validation** | Basic | ✅ Advanced + AI |
| **Token Optimization** | ✅ Concise mode | ✅ Essential properties |
| **API Required** | Yes (all tools) | No (docs work without API) |
| **Best For** | Quick workflow CRUD | Learning, validation, templates |

---

## Environment Configuration

### Docker Networking

**Why `http://n8n:5678` instead of `http://localhost:5678`?**

When MCP servers run on the host machine but n8n runs in Docker:
- `localhost:5678` works from host
- `n8n:5678` resolves via Docker networking
- Both access the same n8n instance
- MCP servers use host context, so both work

### n8n API Configuration

**API Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZTA5YWMyYS05NTE5LTRhMWYtODE1ZS1kYzE5MGUxY2Y1YjciLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYwNzY1MTEwfQ.r8y-3bLzp9WlVh6uwCUbSd19ORqu0zIMrHBH5oJ3H6A`

**n8n Dashboard**: http://localhost:5678
**n8n API**: http://localhost:5678/api/v1
**Docker Network**: http://n8n:5678

### Webhook Security

**WEBHOOK_SECURITY_MODE=moderate** - Allows local webhooks while blocking:
- Private networks
- Cloud metadata endpoints
- Unsafe localhost patterns

---

## Verification Commands

### Check All MCP Servers
```bash
claude mcp list
```

**Expected Output:**
```
MCP_DOCKER: docker mcp gateway run - ✓ Connected
n8n-workflow-builder: npx -y mcp-n8n-builder - ✓ Connected
n8n-mcp: npx n8n-mcp - ✓ Connected
```

### Get Server Details
```bash
claude mcp get n8n-workflow-builder
claude mcp get n8n-mcp
```

### Test n8n API Connection
```bash
curl -H "X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZTA5YWMyYS05NTE5LTRhMWYtODE1ZS1kYzE5MGUxY2Y1YjciLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYwNzY1MTEwfQ.r8y-3bLzp9WlVh6uwCUbSd19ORqu0zIMrHBH5oJ3H6A" \
  http://localhost:5678/api/v1/workflows
```

---

## Usage Recommendations

### When to Use mcp-n8n-builder

✅ **Use for:**
- Quick workflow creation
- Basic CRUD operations
- Listing workflows
- Managing executions
- Simple workflow activation/deactivation

❌ **Not ideal for:**
- Learning n8n nodes
- Finding templates
- Validating complex workflows
- Understanding node properties

### When to Use n8n-mcp

✅ **Use for:**
- Learning about n8n nodes
- Finding workflow templates
- Validating workflow configurations
- Understanding node properties
- AI-powered workflow development
- Complex workflow validation
- Template-based workflow creation

❌ **Not ideal for:**
- When you just need basic CRUD (use mcp-n8n-builder)

### Combined Workflow

**Best Practice**: Use both together!

1. **Discovery Phase** (n8n-mcp):
   - Search for templates
   - Get node documentation
   - Understand properties
   - Validate configurations

2. **Creation Phase** (mcp-n8n-builder):
   - Create workflows
   - Update workflows
   - Manage executions

3. **Validation Phase** (n8n-mcp):
   - Validate workflow
   - Check AI agent configurations
   - Verify expressions

---

## Troubleshooting

### Connection Issues

**Problem**: MCP server shows "disconnected"

**Solutions:**
1. Check n8n container: `docker ps | grep n8n`
2. Verify API: `curl http://localhost:5678/api/v1`
3. Restart MCP: `claude mcp remove <server>` then re-add
4. Check Docker network: `docker network inspect agentzero-network`

### Node Type Errors

**Problem**: "Node type not found" when creating workflows

**Solution**: Use `list_available_nodes` (mcp-n8n-builder) or `list_nodes` (n8n-mcp)

### Authentication Errors

**Problem**: "API key required" or "unauthorized"

**Solutions:**
1. Verify API key is correct
2. Check n8n container is running
3. Test API key with curl

---

## Security Considerations

### API Key Storage
- Stored in `~/.claude.json` (local config)
- Keep this file secure
- Never commit to version control
- Rotate keys periodically

### Webhook Security
- `WEBHOOK_SECURITY_MODE=moderate` is safe for local development
- Blocks private networks and cloud metadata
- Allows localhost webhooks for testing

---

## Resources

### Official Documentation
- **mcp-n8n-builder**: https://github.com/spences10/mcp-n8n-builder
- **n8n-mcp**: https://github.com/czlonkowski/n8n-mcp
- **n8n Documentation**: https://docs.n8n.io/
- **n8n API Reference**: https://docs.n8n.io/api/

### Local Resources
- **n8n Dashboard**: http://localhost:5678
- **n8n API**: http://localhost:5678/api/v1
- **Docker Compose**: `/Users/jim/Documents/5_AgentZero/container_agentzero/docker-compose.yml`

---

## Installation Summary

**Date Completed**: 2025-10-18

### Installed Systems ✅
1. **mcp-n8n-builder** v0.0.4
   - Location: Global (`~/.claude.json`)
   - Status: ✓ Connected
   - Tools: 10

2. **n8n-mcp** Latest
   - Location: Project (`~/.claude.json` → `/Users/jim`)
   - Status: ✓ Connected
   - Tools: 39+

### Configuration Files
- **Claude Code Config**: `~/.claude.json`
- **n8n Docker Compose**: `docker-compose.yml`
- **n8n MCP Config (Container)**: `/root/.config/mcp/config.json` (inside agentzero container)

### Credentials
- **n8n Username**: jims67mustang
- **n8n Password**: Jimmy123$
- **n8n API Key**: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZTA5YWMyYS05NTE5LTRhMWYtODE1ZS1kYzE5MGUxY2Y1YjciLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYwNzY1MTEwfQ.r8y-3bLzp9WlVh6uwCUbSd19ORqu0zIMrHBH5oJ3H6A

---

## Next Steps

1. **Start Using MCP Tools**:
   ```
   You: "List all n8n workflows"
   You: "Show me Slack node documentation"
   You: "Find templates for webhook automation"
   ```

2. **Create Your First Workflow**:
   ```
   You: "Search templates for 'webhook to slack'"
   You: "Create a workflow using that template"
   You: "Activate the workflow"
   ```

3. **Explore Advanced Features**:
   ```
   You: "List all AI-capable nodes"
   You: "Get essential properties for OpenAI chat node"
   You: "Validate my workflow configuration"
   ```

---

**Status**: ✅ All Systems Operational
**Ready to Use**: Yes - both MCP servers available!
**Documentation Location**: `/Users/jim/Documents/5_AgentZero/container_agentzero/claudedocs/`
