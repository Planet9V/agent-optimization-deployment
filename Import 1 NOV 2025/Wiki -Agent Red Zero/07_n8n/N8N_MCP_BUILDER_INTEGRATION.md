# n8n MCP Builder Integration Guide

**Status**: ✅ CONFIGURED
**Date**: 2025-10-18
**MCP Server**: mcp-n8n-builder v0.0.4

## Overview

The **n8n MCP Builder** is a Model Context Protocol server that enables AI assistants (like Claude Code) to programmatically create, manage, and automate n8n workflows without manual intervention.

## Configuration Complete

### Claude Code Integration

**File**: `/Users/jim/.claude/plugins/config.json`

```json
{
  "repositories": {
    "n8n-builder": {
      "command": "npx",
      "args": ["-y", "mcp-n8n-builder"],
      "env": {
        "N8N_HOST": "http://localhost:5678/api/v1",
        "N8N_API_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZTA5YWMyYS05NTE5LTRhMWYtODE1ZS1kYzE5MGUxY2Y1YjciLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYwNzY1MTEwfQ.r8y-3bLzp9WlVh6uwCUbSd19ORqu0zIMrHBH5oJ3H6A",
        "OUTPUT_VERBOSITY": "concise"
      }
    }
  }
}
```

### Connection Details

- **n8n URL**: http://localhost:5678
- **API Endpoint**: http://localhost:5678/api/v1
- **API Key**: Configured ✅
- **Verbosity**: `concise` (reduces token usage)

## Available MCP Tools (10 Tools)

### 1. Workflow Management (7 tools)

| Tool | Purpose | Usage |
|------|---------|-------|
| **list_workflows** | List all workflows | Filter by name, tags, active status |
| **create_workflow** | Create new workflow | Validates nodes before creation |
| **get_workflow** | Get workflow details | Retrieve complete workflow JSON |
| **update_workflow** | Update existing workflow | Full workflow structure required |
| **delete_workflow** | Delete workflow | Permanent deletion |
| **activate_workflow** | Enable workflow | Start automatic execution |
| **deactivate_workflow** | Disable workflow | Stop automatic execution |

### 2. Node Management (1 tool)

| Tool | Purpose | Usage |
|------|---------|-------|
| **list_available_nodes** | List all available n8n nodes | **MUST USE BEFORE** creating workflows |

### 3. Execution Management (2 tools)

| Tool | Purpose | Usage |
|------|---------|-------|
| **list_executions** | List execution history | Filter by workflow, status, limit |
| **get_execution** | Get execution details | Full execution data and logs |

## MCP Resources (3 Resources)

1. **n8n://workflows** - List of all workflows
2. **n8n://workflows/{id}** - Specific workflow details
3. **n8n://executions/{id}** - Specific execution details

## Usage Examples

### Example 1: List All Workflows

```
User: List all my n8n workflows
Claude: [Uses list_workflows tool]
```

**Expected Output**:
```json
{
  "data": [],
  "nextCursor": null
}
```
*(Currently no workflows exist)*

### Example 2: Create a Simple Workflow

```
User: Create a workflow that triggers every hour and sends a webhook
Claude: [Uses list_available_nodes first, then create_workflow]
```

**Workflow Structure**:
```json
{
  "name": "Hourly Webhook Trigger",
  "nodes": [
    {
      "id": "trigger",
      "type": "n8n-nodes-base.schedule",
      "name": "Schedule Trigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "hours", "value": 1}]
        }
      },
      "position": [250, 300]
    },
    {
      "id": "webhook",
      "type": "n8n-nodes-base.httpRequest",
      "name": "Send Webhook",
      "parameters": {
        "url": "https://example.com/webhook",
        "method": "POST"
      },
      "position": [450, 300]
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [[{"node": "Send Webhook", "type": "main", "index": 0}]]
    }
  }
}
```

### Example 3: List Available Nodes

```
User: What nodes are available in n8n?
Claude: [Uses list_available_nodes]
```

This returns all installed n8n nodes (HTTP Request, Slack, Gmail, etc.)

### Example 4: Monitor Workflow Executions

```
User: Show me the execution history for workflow ID 1
Claude: [Uses list_executions with workflowId filter]
```

### Example 5: Activate a Workflow

```
User: Activate the workflow named "Daily Report"
Claude: [Uses list_workflows to find ID, then activate_workflow]
```

## Token Usage Warning

⚠️ **This tool is a "token monster"** due to n8n workflow complexity:

- **Complex JSON structures**: Workflows can have nested nodes, connections, parameters
- **High token consumption**: A single workflow can use thousands of tokens
- **Cannot be reduced**: JSON structure is essential and cannot be simplified

### Mitigation Strategies

1. **Use `concise` verbosity** (already configured) - Shows summaries instead of full JSON
2. **List workflows first** - Low token cost to identify what you need
3. **Work with simple workflows** - Complex workflows may exceed context limits
4. **Break into smaller pieces** - Manage workflows in parts
5. **Selective retrieval** - Only get workflows you need

## Workflow Composition Best Practices

### 1. Always List Available Nodes First

```
IMPORTANT: Before creating or updating workflows:
1. Use list_available_nodes to see what's available
2. Verify node types exist in your n8n instance
3. Prevents errors from using non-existent nodes
```

### 2. Node Validation

The MCP server automatically:
- ✅ Validates node types against available nodes
- ✅ Suggests similar nodes if invalid type detected
- ✅ Provides detailed error messages

### 3. Workflow Structure

Every workflow needs:
- **Unique ID** for each node
- **Node type** (from available nodes)
- **Node name** (descriptive)
- **Parameters** (node-specific configuration)
- **Position** `[x, y]` for visual layout
- **Connections** defining data flow

### 4. Connection Format

```json
{
  "connections": {
    "Node Name 1": {
      "main": [[{"node": "Node Name 2", "type": "main", "index": 0}]]
    }
  }
}
```

## Integration with AgentZero

### Option 1: Direct API Calls

AgentZero can use the n8n API directly:

```python
import requests

headers = {
    "X-N8N-API-KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

# List workflows
response = requests.get(
    "http://localhost:5678/api/v1/workflows",
    headers=headers
)
workflows = response.json()
```

### Option 2: MCP Client Integration

Add MCP client to AgentZero following `AGENTZERO_MCP_INTEGRATION_GUIDE.md`

## Common Workflows to Build

### 1. Data Collection Workflow
- **Trigger**: Schedule (hourly/daily)
- **Action**: HTTP Request to API
- **Storage**: Save to database/spreadsheet

### 2. Notification Workflow
- **Trigger**: Webhook
- **Condition**: Check data criteria
- **Action**: Send Slack/Email notification

### 3. Data Processing Pipeline
- **Trigger**: Manual/Schedule
- **Process**: Transform data (Code node)
- **Output**: Multiple destinations

### 4. Integration Workflow
- **Trigger**: Service A event
- **Transform**: Data mapping
- **Action**: Update Service B

## Troubleshooting

### Issue: "API Key Required"
**Solution**: Verify n8n API key is configured in Claude Code config

### Issue: "Node type not found"
**Solution**: Run `list_available_nodes` to see available types

### Issue: "Workflow creation failed"
**Solution**: Check workflow JSON structure and node connections

### Issue: "High token usage"
**Solution**: Use `OUTPUT_VERBOSITY=concise` and work with simpler workflows

## Next Steps

### To Use in Current Session:

**You need to restart Claude Code** for the MCP server configuration to take effect.

After restart:
1. Ask Claude: "List my n8n workflows"
2. Ask Claude: "What n8n nodes are available?"
3. Ask Claude: "Create a simple test workflow"

### Testing Checklist:

- [ ] Restart Claude Code
- [ ] Test `list_workflows` tool
- [ ] Test `list_available_nodes` tool
- [ ] Create a simple test workflow
- [ ] Activate the workflow
- [ ] Check execution history
- [ ] Modify the workflow
- [ ] Deactivate the workflow

## Security Notes

### API Key Protection

⚠️ **API Key is stored in Claude Code config** at:
`/Users/jim/.claude/plugins/config.json`

**Security Considerations**:
- File contains sensitive credentials
- Keep file permissions restricted
- Do not commit to version control
- Rotate API keys periodically

### n8n Security

- API key provides full workflow access
- Can create, modify, delete workflows
- Can execute workflows
- Can access execution data

**Recommended Actions**:
1. Use separate API keys for different purposes
2. Monitor n8n audit logs
3. Implement workflow approval process for production
4. Regular security reviews

## Resources

- **MCP Server Repo**: https://github.com/spences10/mcp-n8n-builder
- **n8n Documentation**: https://docs.n8n.io/
- **n8n API Docs**: https://docs.n8n.io/api/
- **Local n8n**: http://localhost:5678
- **n8n Dashboard**: http://localhost:5678/workflow

## Advanced Usage

### Custom Node Development

If you need custom nodes:
1. Develop n8n community node
2. Install in n8n instance
3. Use `list_available_nodes` to verify
4. Use in workflows via MCP server

### Workflow Templates

Create reusable workflow templates:
1. Build workflow once
2. Export via `get_workflow`
3. Modify parameters as needed
4. Import via `create_workflow`

### Batch Operations

Process multiple workflows:
1. List all workflows
2. Filter by criteria
3. Bulk activate/deactivate
4. Batch updates

## Support

For issues or questions:
- n8n Community: https://community.n8n.io/
- MCP Server Issues: https://github.com/spences10/mcp-n8n-builder/issues
- This integration: Check AgentZero documentation

---

**Last Updated**: 2025-10-18
**Configuration Version**: v1.0
**MCP Server Version**: 0.0.4
