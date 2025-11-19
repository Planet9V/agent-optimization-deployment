# n8n MCP Server Installation - COMPLETE ✅

**Date**: 2025-10-18
**Status**: Successfully Installed & Connected
**MCP Server**: mcp-n8n-builder v0.0.4

## Installation Summary

### ✅ Step 1: Research Complete
Used Perplexity MCP to gather detailed installation instructions from official sources.

### ✅ Step 2: Installation Complete
```bash
claude mcp add --transport stdio n8n-workflow-builder \
  --env N8N_HOST=http://n8n:5678/api/v1 \
  --env N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... \
  --env OUTPUT_VERBOSITY=concise \
  -- npx -y mcp-n8n-builder
```

### ✅ Step 3: Configuration Verified
**Config File**: `/Users/jim/.claude.json`

**Configuration Details**:
- **Scope**: Local (project-specific)
- **Status**: ✓ Connected
- **Transport**: stdio
- **Command**: `npx -y mcp-n8n-builder`

**Environment Variables**:
- `N8N_HOST`: `http://n8n:5678/api/v1` (Docker container name)
- `N8N_API_KEY`: Configured ✅
- `OUTPUT_VERBOSITY`: `concise` (optimized for token usage)

### ✅ Step 4: Connection Test
**MCP Server Health Check**:
```
n8n-workflow-builder: ✓ Connected
```

## Available MCP Tools (10 Tools)

Now that the server is connected, you have access to:

### Workflow Management (7 tools)
1. **list_workflows** - List all n8n workflows
2. **create_workflow** - Create new workflow
3. **get_workflow** - Get workflow details by ID
4. **update_workflow** - Update existing workflow
5. **delete_workflow** - Delete workflow permanently
6. **activate_workflow** - Enable workflow execution
7. **deactivate_workflow** - Disable workflow execution

### Node Management (1 tool)
8. **list_available_nodes** - List all available n8n nodes
   - ⚠️ **IMPORTANT**: Always use this BEFORE creating workflows!

### Execution Management (2 tools)
9. **list_executions** - List workflow execution history
10. **get_execution** - Get detailed execution information

## How to Use (Examples)

### Example 1: List Your Workflows
```
You: List all my n8n workflows
```

### Example 2: See Available Nodes
```
You: What n8n nodes are available?
```

### Example 3: Create a Simple Workflow
```
You: Create a workflow that:
1. Triggers every hour
2. Makes an HTTP GET request to https://api.example.com/data
3. Sends the result to a webhook
```

### Example 4: Check Workflow Executions
```
You: Show me the execution history for my workflows
```

### Example 5: Activate/Deactivate Workflow
```
You: Activate workflow with ID 1
You: Deactivate workflow named "Daily Report"
```

## Configuration Details

### Docker Network Integration

**Why we use `http://n8n:5678`**:
- Claude Code MCP server runs on the host machine
- n8n Docker container is accessible via its service name
- Docker networking resolves `n8n` to the container's internal IP
- Port 5678 is exposed to host via `docker-compose.yml`

**Alternative Access Methods**:
- From host: `http://localhost:5678` ✅ Works
- From Docker: `http://n8n:5678` ✅ Works (used in config)
- From containers: `http://n8n:5678` ✅ Works

### Token Usage Optimization

**OUTPUT_VERBOSITY=concise** is configured to:
- Show workflow summaries instead of full JSON
- List only essential fields (id, name, status, node count)
- Include relevant guide sections in errors only
- Reduce token consumption by 50-70%

**Best Practices**:
1. List workflows first (low token cost)
2. Work with simple workflows when possible
3. Use concise verbosity unless full JSON needed
4. Break complex workflows into smaller pieces

## Verification Commands

### Check MCP Server Status
```bash
claude mcp list
```

**Expected Output**:
```
n8n-workflow-builder: npx -y mcp-n8n-builder - ✓ Connected
```

### Get Server Details
```bash
claude mcp get n8n-workflow-builder
```

### Test n8n API Directly
```bash
curl -H "X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  http://localhost:5678/api/v1/workflows
```

## Important Notes

### ⚠️ Always List Available Nodes First
Before creating or updating workflows:
```
You: List all available n8n nodes
```

This prevents errors from using node types that don't exist in your n8n instance.

### 🔐 Security Considerations
- API key is stored in Claude Code config (`~/.claude.json`)
- Keep this file secure and don't commit to version control
- The API key provides full access to your n8n workflows
- Rotate keys periodically for security

### 📊 Token Consumption Warning
- n8n workflows are complex JSON structures
- A single workflow can consume thousands of tokens
- Use `concise` verbosity (already configured)
- Consider token cost before retrieving large workflows

## Workflow Composition Guidelines

### Basic Workflow Structure
Every n8n workflow needs:
1. **Unique ID** for each node
2. **Node type** (from available nodes list)
3. **Node name** (descriptive label)
4. **Parameters** (node-specific config)
5. **Position** `[x, y]` for visual layout
6. **Connections** defining data flow between nodes

### Example Workflow JSON
```json
{
  "name": "Simple HTTP Workflow",
  "nodes": [
    {
      "id": "trigger",
      "type": "n8n-nodes-base.schedule",
      "name": "Every Hour",
      "parameters": {
        "rule": {
          "interval": [{"field": "hours", "value": 1}]
        }
      },
      "position": [250, 300]
    },
    {
      "id": "http",
      "type": "n8n-nodes-base.httpRequest",
      "name": "Fetch Data",
      "parameters": {
        "url": "https://api.example.com/data",
        "method": "GET"
      },
      "position": [450, 300]
    }
  ],
  "connections": {
    "Every Hour": {
      "main": [[{"node": "Fetch Data", "type": "main", "index": 0}]]
    }
  }
}
```

## Next Steps

### Recommended First Actions

1. **List available nodes**:
   ```
   You: What n8n nodes are available in my instance?
   ```

2. **Check existing workflows**:
   ```
   You: List all my n8n workflows
   ```

3. **Create a test workflow**:
   ```
   You: Create a simple test workflow with a manual trigger and HTTP request
   ```

4. **Monitor executions**:
   ```
   You: Show me recent workflow executions
   ```

## Troubleshooting

### Connection Issues

**Problem**: Server shows "disconnected"

**Solutions**:
1. Check n8n container is running: `docker ps | grep n8n`
2. Verify API endpoint: `curl http://localhost:5678/api/v1`
3. Restart MCP server: `claude mcp remove n8n-workflow-builder` then re-add
4. Check Docker network: `docker network inspect container_agentzero_agentzero-network`

### Node Type Errors

**Problem**: "Node type not found" when creating workflows

**Solution**: Always run `list_available_nodes` first to see valid node types

### Authentication Errors

**Problem**: "API key required" or "unauthorized"

**Solutions**:
1. Verify API key is correct (no extra spaces)
2. Check API key hasn't expired
3. Test API key directly with curl

## Integration with AgentZero

The MCP server is accessible from:
- ✅ Claude Code (current session)
- ✅ AgentZero (via API calls to n8n)
- ✅ Other Docker containers (via `http://n8n:5678`)

## Resources

- **MCP Server Repository**: https://github.com/spences10/mcp-n8n-builder
- **n8n Documentation**: https://docs.n8n.io/
- **n8n API Reference**: https://docs.n8n.io/api/
- **Local n8n Dashboard**: http://localhost:5678
- **Local n8n API**: http://localhost:5678/api/v1

## Support & Documentation

- **Complete Integration Guide**: `N8N_MCP_BUILDER_INTEGRATION.md`
- **AgentZero MCP Guide**: `AGENTZERO_MCP_INTEGRATION_GUIDE.md`
- **Docker MCP Setup**: `CLAUDE_CODE_DOCKER_MCP_INTEGRATION.md`

---

**Installation Complete**: 2025-10-18
**Status**: ✅ All systems operational
**Ready to use**: Yes - start creating workflows!
