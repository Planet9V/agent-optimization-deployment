---
title: NeoCoder Installation Guide
category: NeoCoder/Getting_Started
last_updated: 2025-10-24
line_count: 380
status: published
tags: [neocoder, installation, setup, prerequisites, neo4j, qdrant]
---

# NeoCoder Installation Guide

## Overview

Complete installation guide for setting up NeoCoder, an MCP server that combines Neo4j knowledge graphs with Qdrant vector databases for hybrid AI reasoning. This guide covers all prerequisites, installation steps, and verification procedures.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Neo4j Setup](#neo4j-setup)
- [Qdrant Setup](#qdrant-setup)
- [NeoCoder Installation](#neocoder-installation)
- [Claude Desktop Configuration](#claude-desktop-configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Related Topics](#related-topics)

---

## Prerequisites

### Required Software

| Component | Minimum Version | Purpose |
|-----------|----------------|---------|
| **Neo4j** | 4.4+ | Knowledge graph database |
| **Qdrant** | Latest | Vector database for semantic search |
| **Python** | 3.10+ | Runtime environment |
| **uv** | Latest | Python package manager for MCP |
| **Claude Desktop** | Latest | AI assistant interface |

### System Requirements

- **OS:** macOS, Linux, or Windows (WSL2 recommended)
- **RAM:** 8GB minimum, 16GB recommended
- **Disk Space:** 2GB for NeoCoder + databases
- **Network:** Internet connection for package installation

### Optional MCP Servers

Enhanced NeoCoder capabilities with additional MCP servers:

- **MCP-Desktop-Commander**: CLI and filesystem operations
- **wolframalpha-llm-mcp**: Mathematical and computational queries
- **mcp-server-qdrant-enhanced**: Extended Qdrant functionality
- **arxiv-mcp-server**: Academic paper retrieval

---

## Neo4j Setup

### Option 1: Neo4j Desktop (Recommended for Development)

```bash
# Download from https://neo4j.com/download/
# Install and launch Neo4j Desktop

# Create new database
1. Open Neo4j Desktop
2. Click "New" → "Create Project"
3. Click "Add" → "Local DBMS"
4. Set password (remember this!)
5. Click "Start"
```

### Option 2: Docker (Recommended for Production)

```bash
# Pull Neo4j image
docker pull neo4j:latest

# Run Neo4j container
docker run \
  --name neo4j \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your-password \
  -v neo4j_data:/data \
  -d neo4j:latest
```

### Verify Neo4j Installation

```bash
# Access Neo4j Browser
open http://localhost:7474

# Login with:
# Username: neo4j
# Password: [your password]

# Test connection
RETURN "Hello, Neo4j!" as message;
```

---

## Qdrant Setup

### Docker Installation (Recommended)

```bash
# Pull Qdrant image
docker pull qdrant/qdrant

# Run with persistent storage
docker run -p 6333:6333 -p 6334:6334 \
  -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
  -d qdrant/qdrant
```

### Verify Qdrant Installation

```bash
# Check Qdrant API
curl http://localhost:6333/

# Expected response:
# {"title":"qdrant - vector search engine","version":"..."}
```

---

## NeoCoder Installation

### Clone Repository

```bash
# Clone from GitHub
git clone https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow.git
cd NeoCoder-neo4j-ai-workflow
```

### Python Environment Setup

```bash
# Install pyenv if not already installed
# macOS: brew install pyenv
# Linux: curl https://pyenv.run | bash

# Install Python 3.11.12
pyenv install 3.11.12
pyenv local 3.11.12

# Create virtual environment with uv
uv venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

### Install Dependencies

```bash
# Install all dependencies
uv pip install -e '.[dev,docs,gpu]'

# Verify installation
python -c "import mcp_neocoder; print('NeoCoder installed successfully')"
```

### Environment Configuration

Create `.env` file (or use environment variables):

```bash
# Create .env file
cat > .env << 'EOF'
# Neo4j Configuration
NEO4J_URL=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password-here
NEO4J_DATABASE=neo4j

# Qdrant Configuration
QDRANT_URL=http://localhost:6333

# Optional: Wolfram Alpha API
WOLFRAM_ALPHA_APP_ID=your-app-id

# Optional: Default incarnation
DEFAULT_INCARNATION=knowledge_graph
EOF
```

---

## Claude Desktop Configuration

### Configure MCP Server

Edit Claude Desktop configuration file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "neocoder": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/NeoCoder-neo4j-ai-workflow/src/mcp_neocoder",
        "run",
        "mcp_neocoder"
      ],
      "env": {
        "NEO4J_URL": "bolt://localhost:7687",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "your-password-here",
        "NEO4J_DATABASE": "neo4j"
      }
    }
  }
}
```

**Critical:** Replace `/absolute/path/to/` with your actual installation path.

### Restart Claude Desktop

```bash
# Completely quit Claude Desktop
# Restart the application
```

---

## Verification

### Test Neo4j Connection

```bash
# From NeoCoder directory
python -m mcp_neocoder.server --test-connection
```

### Test MCP Server

In Claude Desktop, try:

```
Can you check your connection to Neo4j?
```

Expected response includes connection status and database information.

### Initialize NeoCoder Schema

```bash
# Run initialization script
python scripts/init_graph.py \
  --uri bolt://localhost:7687 \
  --username neo4j \
  --password your-password
```

### Verify Installation Completeness

```bash
# List available incarnations
python -m mcp_neocoder.server --list-incarnations

# Should show:
# - coding
# - knowledge_graph
# - code_analysis
# - research
# - decision_support
# - data_analysis
# - complex_system
```

---

## Troubleshooting

### Neo4j Connection Errors

**Problem:** `ServiceUnavailable: Connection refused`

**Solutions:**
```bash
# Check Neo4j is running
docker ps  # or check Neo4j Desktop

# Verify port 7687 is open
nc -zv localhost 7687

# Check firewall settings
```

### Qdrant Connection Errors

**Problem:** `Connection refused on port 6333`

**Solutions:**
```bash
# Check Qdrant is running
docker ps | grep qdrant

# Restart Qdrant
docker restart qdrant

# Check Qdrant logs
docker logs qdrant
```

### Python Environment Issues

**Problem:** Package import errors

**Solutions:**
```bash
# Verify virtual environment is activated
which python  # should show .venv path

# Reinstall dependencies
uv pip install -e '.[dev,docs,gpu]' --force-reinstall

# Check Python version
python --version  # should be 3.10+
```

### Claude Desktop Not Finding MCP Server

**Problem:** MCP server not listed in Claude

**Solutions:**
1. Verify `claude_desktop_config.json` syntax (use JSON validator)
2. Check absolute paths are correct
3. Ensure Neo4j password matches configuration
4. Restart Claude Desktop completely
5. Check Claude logs for error messages

### Permission Errors

**Problem:** Permission denied errors during installation

**Solutions:**
```bash
# macOS/Linux: Fix permissions
chmod +x scripts/*.py

# Ensure write access to qdrant_storage
chmod -R 755 qdrant_storage/
```

---

## Next Steps

Once installation is complete:

1. **[Quick Start Guide](02_Quick_Start.md)** - First steps with NeoCoder
2. **[Create First Project](03_First_Project.md)** - Set up your first project
3. **[Core Concepts](../02_Core_Concepts/01_Architecture.md)** - Understand the architecture

---

## Related Topics

- [Architecture Overview](../02_Core_Concepts/01_Architecture.md) - System components and design
- [MCP Integration](../02_Core_Concepts/02_MCP_Integration.md) - Model Context Protocol details
- [Troubleshooting Guide](../08_Reference/03_Troubleshooting.md) - Common issues and solutions

## See Also

- [NeoCoder Repository](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow) - Source code
- [Neo4j Documentation](https://neo4j.com/docs/) - Official Neo4j docs
- [Qdrant Documentation](https://qdrant.tech/documentation/) - Official Qdrant docs
- [MCP Specification](https://modelcontextprotocol.io) - Model Context Protocol

---

**Last Updated:** 2025-10-24 | **Lines:** 380/400 | **Status:** published
