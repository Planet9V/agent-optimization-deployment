---
title: Claude Code → Docker MCP Toolkit Integration
category: 05_Integration_Guides/01_MCP
last_updated: 2025-10-25
line_count: 367
status: published
tags: [mcp, docker, claude-code, toolkit, gateway]
---

# Claude Code → Docker MCP Toolkit Integration

**Status**: ✅ SUCCESSFULLY CONFIGURED
**Date**: 2025-10-18
**Location**: `/Users/jim/.docker/mcp/`

## Integration Summary

Claude Code is now connected to Docker MCP Toolkit as a centralized gateway for accessing MCP servers. This configuration enables:

- **Universal Access**: All 227+ MCP servers available through single gateway
- **Centralized Management**: Docker MCP Toolkit manages server lifecycle
- **Easy Expansion**: Enable new servers with single command
- **Cross-Client Consistency**: Same servers available to gordon, lmstudio, and claude-code

## Current Configuration

### Connected Clients (Global)
```
✅ claude-code: connected via Docker MCP gateway (stdio)
✅ gordon: connected via Docker MCP gateway (stdio)
✅ lmstudio: connected via Docker MCP gateway (stdio)
❌ claude-desktop: disconnected
❌ zed: disconnected
```

### Currently Enabled MCP Servers (6)

| Server | Purpose | Tools Available |
|--------|---------|-----------------|
| **context7** | Up-to-date code documentation for libraries/frameworks | `get-library-docs`, `resolve-library-id` |
| **deepwiki** | Fetch and ask questions about GitHub repositories | Repository analysis tools |
| **fetch** | Extract web content as markdown | URL fetching and markdown conversion |
| **perplexity-ask** | Real-time web research via Perplexity API | Web search and research |
| **sequentialthinking** | Dynamic problem-solving through thought sequences | Sequential reasoning tools |
| **vuln-nist-mcp-server** | Query NVD/CVE vulnerability database | Security vulnerability lookups |

## Complete MCP Server Catalog (227 Servers)

### Development & Code Tools
- **context7**: Library/framework documentation
- **github**: GitHub API interaction
- **github-official**: Official GitHub MCP server
- **gitlab**: GitLab API operations
- **git**: Git repository operations
- **gitmcp**: Git automation tools
- **ast-grep**: Code structural search and lint
- **javadocs**: Java/Kotlin/Scala documentation
- **npm-sentinel**: NPM package monitoring
- **maven-tools-mcp**: Maven build tools

### Documentation & Research
- **deepwiki**: GitHub repository analysis
- **fetch**: Web content extraction
- **perplexity-ask**: Real-time research
- **atlas-docs**: Library documentation hosting
- **astro-docs**: Astro framework docs
- **cloudflare-docs**: Cloudflare products docs
- **aws-documentation**: AWS docs access
- **wikipedia-mcp**: Wikipedia information retrieval

### AI & Problem Solving
- **sequentialthinking**: Dynamic reasoning
- **e2b**: Code execution environment
- **mcp-code-interpreter**: Code interpretation
- **mcp-python-refactoring**: Python refactoring tools

### Cloud & Infrastructure
- **aws-core-mcp-server**: AWS services
- **aws-cdk-mcp-server**: AWS CDK patterns
- **aws-terraform**: Terraform on AWS
- **aws-diagram**: AWS architecture diagrams
- **azure**: Azure services
- **aks**: Azure Kubernetes Service
- **cloud-run-mcp**: Google Cloud Run
- **heroku**: Heroku platform
- **docker**: Docker CLI
- **dockerhub**: Docker Hub operations
- **kubernetes**: K8s management
- **kubectl-mcp-server**: kubectl operations

### Databases
- **database-server**: PostgreSQL, MySQL, SQLite with natural language
- **postgres**: PostgreSQL operations
- **mongodb**: MongoDB operations
- **neo4j-cypher**: Neo4j graph database
- **neo4j-cloud-aura-api**: Neo4j Aura management
- **redis**: Redis operations
- **redis-cloud**: Redis Cloud management
- **clickhouse**: ClickHouse database
- **cockroachdb**: CockroachDB operations
- **couchbase**: Couchbase operations
- **elasticsearch**: Elasticsearch queries
- **astra-db**: Astra DB workloads
- **chroma**: Chroma vector database
- **pinecone**: Pinecone vector DB
- **singlestore**: SingleStore operations

### Web Search & Data
- **brave**: Brave Search API
- **tavily**: Web search and research
- **exa**: Web search and crawling
- **kagisearch**: Kagi search engine
- **duckduckgo**: DuckDuckGo search
- **wolfram-alpha**: Computational intelligence

### Web Scraping & Automation
- **apify**: Web scraping marketplace
- **browserbase**: AI-powered browser automation
- **playwright**: Browser automation
- **puppeteer**: Headless browser control
- **firecrawl**: Web scraping and search
- **scrapegraph**: Graph-based scraping
- **scrapezy**: Web scraping tools
- **oxylabs**: Enterprise web scraping

### Communication & Collaboration
- **slack**: Slack workspace interaction
- **gmail-mcp**: Gmail operations (IMAP/SMTP)
- **discord**: Discord MCP server
- **atlassian**: Confluence and Jira tools
- **notion**: Notion workspace
- **obsidian**: Obsidian vault access

### Project Management
- **buildkite**: CI/CD build management
- **circleci**: CircleCI workflows
- **github**: Issue/PR management
- **gitlab**: GitLab project management
- **jetbrains**: JetBrains IDE integration
- **teamwork**: Teamwork project management

### Security & Compliance
- **vuln-nist-mcp-server**: NVD/CVE vulnerability data
- **beagle-security**: Security testing and vulnerabilities
- **semgrep**: Code security scanning
- **sentry**: Error monitoring
- **stackhawk**: Application security testing
- **sonarqube**: Code quality and security

### Data & Analytics
- **grafana**: Metrics and dashboards
- **prometheus**: Monitoring and alerting
- **dynatrace-mcp-server**: Observability platform
- **metabase**: Business intelligence
- **databutton**: Data application platform

### Payment & E-commerce
- **stripe**: Payment processing
- **razorpay**: Payment gateway
- **mercado-pago**: Mercado Pago payments
- **mercado-libre**: Mercado Libre marketplace
- **bitrefill**: Cryptocurrency purchases

### AI & ML Platforms
- **hugging-face**: Models, datasets, papers
- **elevenlabs**: Text-to-speech
- **novita**: AI services
- **glif**: AI workflow execution

### File & Storage
- **filesystem**: Local filesystem access
- **box**: Box API interaction
- **onlyoffice-docspace**: OnlyOffice document collaboration

### Specialized Tools
- **inspektor-gadget**: Kubernetes/container troubleshooting
- **terraform**: Infrastructure as code
- **ffmpeg**: Video processing
- **handwriting-ocr**: Handwriting recognition
- **minecraft-wiki**: Minecraft information
- **youtube_transcript**: YouTube video transcripts

## How to Use MCP Servers in Claude Code

### Listing Available Servers
```bash
# List currently enabled servers
docker mcp server ls

# Show all servers in catalog (227 total)
docker mcp catalog show docker-mcp

# Get details about specific server
docker mcp server inspect context7
```

### Enabling Additional Servers
```bash
# Enable a server
docker mcp server enable playwright

# Enable multiple servers
docker mcp server enable github gitlab terraform

# Verify enabled
docker mcp server ls
```

### Disabling Servers
```bash
# Disable specific server
docker mcp server disable perplexity-ask

# Disable all servers
docker mcp server reset
```

### Reconnecting After Changes
When you enable/disable servers, Claude Code picks up changes automatically through the gateway connection.

## Integration with AgentZero

To enable AgentZero Docker container to use the same MCP servers, add to `docker-compose.yml`:

```yaml
services:
  agentzero:
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      - ENABLE_MCP=true
      - MCP_GATEWAY_URL=http://host.docker.internal:3000
```

Then use the MCP helper module documented in `AGENTZERO_MCP_INTEGRATION_GUIDE.md`.

## Technical Details

### Gateway Configuration
- **Type**: stdio (standard input/output)
- **Location**: `/Users/jim/.docker/mcp/`
- **Catalog Source**: `https://desktop.docker.com/mcp/catalog/v2/catalog.yaml`
- **Last Updated**: 2025-10-17

### Server Registry
File: `/Users/jim/.docker/mcp/registry.yaml`

Currently enabled servers tracked in registry:
```yaml
registry:
  context7:
    ref: ""
  deepwiki:
    ref: ""
  fetch:
    ref: ""
  perplexity-ask:
    ref: ""
  sequentialthinking:
    ref: ""
  vuln-nist-mcp-server:
    ref: ""
```

### Global Client Configuration
Stored at system level (managed by Docker MCP Toolkit):
```bash
docker mcp client ls --global
```

## Common Operations

### Search for Specific Server Type
```bash
# Search for database-related servers
docker mcp catalog show docker-mcp | grep -i database

# Search for cloud providers
docker mcp catalog show docker-mcp | grep -i "aws\|azure\|gcp"

# Search for security tools
docker mcp catalog show docker-mcp | grep -i "security\|vuln"
```

### Enable Recommended Development Stack
```bash
# Core development tools
docker mcp server enable \
  github \
  git \
  filesystem \
  context7 \
  playwright

# Verify
docker mcp server ls
```

### Enable Data Science Stack
```bash
# Data and ML tools
docker mcp server enable \
  postgres \
  database-server \
  hugging-face \
  jupyter

# Verify
docker mcp server ls
```

## Troubleshooting

### Claude Code Not Seeing New Servers
1. Verify server is enabled: `docker mcp server ls`
2. Check client connection: `docker mcp client ls --global`
3. Restart Claude Code if needed

### Gateway Connection Issues
```bash
# Check gateway status
docker mcp client ls --global

# Reconnect if needed
docker mcp client connect --global claude-code
```

### Server Not Working
```bash
# Inspect server details
docker mcp server inspect <server-name>

# Check if server needs configuration
docker mcp server inspect <server-name> | grep -i "config\|env"
```

## Next Steps

### Recommended Servers to Enable

**For Web Development**:
- `github` - GitHub integration
- `playwright` - Browser testing
- `filesystem` - Local file access
- `npm-sentinel` - Package monitoring

**For Cloud/DevOps**:
- `docker` - Docker CLI
- `kubernetes` - K8s management
- `terraform` - Infrastructure as code
- `aws-core-mcp-server` - AWS services

**For Data Work**:
- `database-server` - Multi-database support with natural language
- `postgres` - PostgreSQL operations
- `grafana` - Metrics and dashboards
- `elasticsearch` - Search and analytics

**For Security**:
- `semgrep` - Code security scanning
- `sentry` - Error monitoring
- `stackhawk` - Security testing

## Related Topics

- [AgentZero MCP Integration Guide](01_AgentZero_MCP_Integration/01_Overview_and_Methods.md)

## Resources

- **Docker MCP Toolkit Docs**: https://docs.docker.com/mcp/
- **MCP Protocol Spec**: https://modelcontextprotocol.io/
- **Server Catalog**: https://desktop.docker.com/mcp/catalog/v2/catalog.yaml
- **Local Config**: `/Users/jim/.docker/mcp/`

---
**Last Updated:** 2025-10-25 | **Lines:** 367/400 | **Status:** published
