# Part 1 of 3: Framework & Architecture

**Series**: PentAGI
**Navigation**: [📚 Series Overview](./00_Series_Overview.md) | [Part 2 →](./02_Autonomous_Capabilities.md)

---

# PentAGI Autonomous Pentesting Framework - Comprehensive Technical Analysis

**Research Date**: 2025-10-16
**Framework**: PentAGI by VXControl
**Repository**: https://github.com/vxcontrol/pentagi
**Website**: https://pentagi.com/
**License**: MIT Open Source

---

## Executive Summary

PentAGI is a fully autonomous AI-powered penetration testing framework that leverages multi-agent orchestration, professional security tools, and isolated Docker execution environments. Developed by VXControl, it represents a significant advancement in autonomous security testing by combining LLM-based decision-making with 20+ integrated professional security tools in a microservices architecture.

**Key Differentiators**:
- Fully autonomous multi-agent system with specialized roles (Orchestrator, Researcher, Developer, Executor)
- Complete Docker sandbox isolation for zero-risk testing
- Persistent memory system using PostgreSQL with pgvector for knowledge retention
- Comprehensive observability stack (Grafana, Prometheus, Jaeger, Loki)
- REST and GraphQL APIs for CI/CD integration
- Support for multiple LLM providers (OpenAI, Anthropic, Gemini, AWS Bedrock, Ollama)

**Confidence Level**: High (85%) - Based on official documentation, GitHub repository analysis, and community resources.

---

## 1. Architecture and Design Patterns

### 1.1 System Architecture Overview

PentAGI employs a **microservices-based design** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
│                 React + TypeScript Web UI                   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway Layer                       │
│              Go Backend (REST + GraphQL APIs)               │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  Multi-Agent Orchestration                  │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│   │ Orchestrator │  │  Researcher  │  │  Developer   │    │
│   └──────────────┘  └──────────────┘  └──────────────┘    │
│                     ┌──────────────┐                        │
│                     │   Executor   │                        │
│                     └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Data & Memory Layer                      │
│  ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  PostgreSQL +   │  │  Redis Cache │  │ MinIO S3     │  │
│  │    pgvector     │  │ Rate Limiter │  │ Storage      │  │
│  └─────────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│              Monitoring & Observability Stack               │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────────┐    │
│  │   Grafana    │  │   Jaeger    │  │      Loki      │    │
│  │  Dashboards  │  │   Tracing   │  │ Log Aggregation│    │
│  └──────────────┘  └─────────────┘  └────────────────┘    │
│  ┌──────────────┐  ┌─────────────┐                         │
│  │VictoriaMetrics│ │  Langfuse   │                         │
│  │ Time-Series  │  │ LLM Monitor │                         │
│  └──────────────┘  └─────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│              Tool Execution & Isolation Layer               │
│         Docker Sandbox with 20+ Security Tools              │
│  (nmap, metasploit, sqlmap, nikto, burp, hydra, etc.)      │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Core Design Patterns

**1. Multi-Agent Delegation Pattern**
- Specialized agents for different phases of penetration testing
- Clear separation of concerns: research, planning, execution, orchestration
- Shared memory system enables agent coordination and knowledge sharing

**2. Microservices Architecture**
- Independent services communicating via REST/GraphQL
- Horizontal scalability for each component
- Separate networks for core services, monitoring, and analytics

**3. Sandbox Isolation Pattern**
- All tool execution happens in isolated Docker containers
- Zero-risk testing through complete environmental separation
- Dynamic Docker image selection based on task requirements

**4. Event-Driven Processing**
- Asynchronous task queue for handling long-running operations
- OpenTelemetry integration for distributed tracing
- Real-time event streaming for monitoring and observability

**5. Memory-Augmented Generation (MAG)**
- Vector embeddings for semantic search (PostgreSQL + pgvector)
- Three-tier memory system: long-term, working, episodic
- Knowledge base for storing successful attack patterns and methodologies

### 1.3 Context Management: Chain Summarization

PentAGI implements intelligent conversation summarization to prevent token limit exhaustion:

- **Preservation Window**: Recent messages kept in original form
- **Section-Based Summarization**: Older content selectively condensed
- **QA Pair Extraction**: Critical information retained through question-answer pairs
- **Per-Agent Tuning**: Configurable preservation thresholds for each agent type

This approach maintains conversation coherence while reducing token consumption by approximately 40-60%.

---

## 2. Multi-Agent System Architecture

### 2.1 Agent Types and Responsibilities

**Orchestrator Agent**
- **Role**: Workflow coordination and context management
- **Capabilities**:
  - Delegates tasks to specialized agents
  - Maintains overall testing strategy and objectives
  - Manages agent communication and handoffs
  - Queries similar tasks from knowledge base
  - Loads relevant context for each phase
- **Memory Access**: Long-term strategy patterns, historical workflow successes

**Researcher Agent**
- **Role**: Target analysis and intelligence gathering
- **Capabilities**:
  - Analyzes target systems and infrastructure
  - Searches for similar penetration testing cases
  - Queries vulnerability databases
  - Gathers OSINT (Open Source Intelligence)
  - Stores findings in vector database
- **Memory Access**: Vulnerability knowledge base, similar case histories
- **Tools**: Built-in web scraper, search API integration (Tavily, DuckDuckGo, Google Custom Search, Perplexity, Searxng, Traversaal)

**Developer Agent**
- **Role**: Attack strategy planning and exploit development
- **Capabilities**:
  - Plans multi-step attack chains
  - Queries exploit databases and techniques
  - Loads tool-specific information and usage patterns
  - Develops custom exploits when needed
  - Designs comprehensive testing strategies
- **Memory Access**: Exploit patterns, tool documentation, technique libraries
- **Decision-Making**: Selects appropriate tools and methods based on target characteristics

**Executor Agent**
- **Role**: Command execution and result validation
- **Capabilities**:
  - Executes planned attack steps in Docker sandbox
  - Loads tool-specific usage guides
  - Interprets command outputs
  - Validates exploitation success
  - Stores execution results and outcomes
- **Memory Access**: Tool usage patterns, command history, result templates
- **Safety**: All execution happens in isolated containers

### 2.2 Agent Communication Flow

```
┌─────────────┐
│     User    │
│   Request   │
└──────┬──────┘
       │
       v
┌─────────────────────────────────────┐
│         Orchestrator                │
│  - Parse objective                  │
│  - Query similar tasks              │
│  - Plan overall approach            │
└──────┬──────────────────────────────┘
       │
       ├──────────────────────┐
       │                      │
       v                      v
┌─────────────┐      ┌───────────────┐
│  Researcher │      │   Developer   │
│  - Analyze  │──────>│  - Plan       │
│  - Gather   │      │  - Query      │
│    intel    │      │    exploits   │
└─────────────┘      └───────┬───────┘
                             │
                             v
                     ┌───────────────┐
                     │   Executor    │
                     │  - Execute    │
                     │  - Validate   │
                     │  - Store      │
                     └───────┬───────┘
                             │
                             v
                     ┌───────────────┐
                     │  Vector Store │
                     │  - Results    │
                     │  - Patterns   │
                     │  - Knowledge  │
                     └───────────────┘
```

### 2.3 Autonomous Decision-Making Approach

**LLM-Based Planning**
- Each agent uses LLM inference for decision-making
- Supports multiple providers: OpenAI (GPT-4/4o), Anthropic (Claude 3.5/4), Google Gemini, AWS Bedrock, Ollama (local)
- Agent-specific model selection based on task complexity and requirements

**Reasoning Strategies**
- **Claude 3.7**: Step-by-step thinking for security research
- **Claude 4 Series**: Sophisticated reasoning for complex attack planning
- **Claude 3.5 Haiku**: Fast vulnerability scanning and initial reconnaissance

**Memory-Augmented Decision Making**
1. Agent receives task from Orchestrator
2. Queries vector database for similar past cases
3. Retrieves relevant knowledge and successful patterns
4. LLM generates action plan based on context + memory
5. Executes actions with validation at each step
6. Stores successful approaches for future reuse

**Feedback Loops**
- Executor results feed back to Developer for strategy adjustment
- Researcher findings inform Developer's exploit selection
- Orchestrator monitors overall progress and can trigger replanning
- All outcomes stored in episodic memory for learning

### 2.4 Agent Configuration

Configurable via environment variables:
- `ASSISTANT_USE_AGENTS`: Enable/disable agent delegation by default
- Agent-specific LLM provider and model selection
- Memory retention policies per agent type
- Summarization thresholds for context management

---

## 3. Tool Integration Methodology (20+ Tools)

### 3.1 Integrated Security Tools

PentAGI includes 20+ professional security tools accessible to agents:

**Network Reconnaissance**
- **nmap**: Network scanning and service enumeration
- **masscan**: High-speed port scanner

**Vulnerability Assessment**
- **nikto**: Web server vulnerability scanner
- **sqlmap**: Automated SQL injection detection and exploitation
- **wpscan**: WordPress vulnerability scanner
- **nuclei**: Template-based vulnerability scanner

**Exploitation Frameworks**
- **metasploit**: Comprehensive exploitation framework
- **exploit-db**: Exploit database integration

**Web Application Testing**
- **burp suite**: Web application security testing
- **gobuster**: Directory/file brute-forcing
- **ffuf**: Fast web fuzzer

**Password Cracking**
- **hydra**: Network login cracker
- **john the ripper**: Password hash cracking
- **hashcat**: Advanced password recovery

**Network Analysis**
- **wireshark**: Network protocol analyzer
- **tcpdump**: Packet analyzer

**Additional Tools**
- **searchsploit**: Exploit-DB command-line search
- **smbclient**: SMB/CIFS network protocol client
- **enum4linux**: Linux enumeration tool for Windows/Samba
- **dirb**: Web content scanner
- **wfuzz**: Web application fuzzer

### 3.2 Tool Integration Architecture

**Dynamic Tool Selection**
- Agents query tool information from knowledge base
- Developer Agent selects appropriate tools based on target characteristics
- Automatic tool chaining for multi-step attacks

**Docker Image Management**
- Configurable Docker image selection per task type
- System automatically chooses most appropriate image
- Support for custom/corporate images
- Pre-built toolsets for performance optimization

**Tool Execution Flow**
```
Developer Agent           Executor Agent           Docker Container
      │                         │                         │
      │──Plan: Use nmap────────>│                         │
      │                         │──Spin up container─────>│
      │                         │                         │
      │                         │──Execute: nmap -sV──────>│
      │                         │                  [scan] │
      │                         │<─────Results────────────│
      │<───Parsed output────────│                         │
      │                         │──Cleanup container─────>│
```

**Result Interpretation**
- Executor Agent parses tool outputs
- LLM interprets results and extracts key findings
- Structured data stored in PostgreSQL
- Vector embeddings created for semantic search

### 3.3 Tool Knowledge Base

Each tool has associated metadata:
- Usage patterns and best practices
- Common flags and options
- Output format and parsing strategies
- Success/failure indicators
- Integration with other tools

Stored in vector database for semantic retrieval:
- "How to perform subdomain enumeration?" → nmap, gobuster, sublist3r
- "Detect SQL injection?" → sqlmap, burp, manual testing techniques

### 3.4 Safety and Rate Limiting

- All tool execution isolated in Docker containers
- Redis-based rate limiting to prevent resource exhaustion
- Configurable execution timeouts
- Audit logging of all commands via PostgreSQL

---

## 4. Docker Sandbox Implementation

### 4.1 Containerization Strategy

**Core Principle**: Complete isolation for zero-risk testing

**Architecture Components**:
1. **PentAGI Service Container**
   - Runs as root user (requires docker.sock access for container management)
   - Alternative: Use default `pentagi` user with TCP/IP Docker connection
   - Handles orchestration and agent coordination

2. **Tool Execution Containers**
   - Ephemeral containers spun up per tool execution
   - Pre-configured with specific security tools
   - Destroyed immediately after task completion

3. **Network Isolation**
   - Separate Docker networks for services, monitoring, and analytics
   - Network segmentation ensures security boundaries
   - Configurable network policies

### 4.2 Docker Compose Deployment

**Deployment Model**: One-click deployment via docker-compose.yml

**Service Structure**:
```yaml
services:
  pentagi:
    # Main application service
    # Requires: docker.sock or Docker TCP connection
    # Environment: LLM credentials, config paths

  postgres:
    # PostgreSQL + pgvector extension
    # Persistent storage for commands, outputs, embeddings

  redis:
    # Caching and rate limiting

  minio:
    # S3-compatible object storage for artifacts

  grafana:
    # Monitoring dashboards

  victoriametrics:
    # Time-series metrics storage

  jaeger:
    # Distributed tracing

  loki:
    # Log aggregation

  clickhouse:
    # Analytics data warehouse

  langfuse:
    # Optional: LLM performance tracking
```

### 4.3 Security Considerations

**Isolation Benefits**:
- Malicious exploits contained within ephemeral containers
- No risk to host system or other services
- Clean slate for each tool execution
- Network activity isolated and monitored

**Configuration Options**:
- **Verified Images Only**: Restrict to trusted container images
- **Corporate Images**: Use organization-specific base images
- **Resource Limits**: CPU, memory, and network constraints per container
- **Execution Timeouts**: Automatic termination of long-running tasks

**Root Access Trade-off**:
- Root required for docker.sock management
- Alternative: TCP/IP connection with non-root user
- Security vs. convenience balance configurable

### 4.4 System Requirements

**Minimum**:
- 4GB RAM
- 10GB disk space
- Docker and Docker Compose installed
- LLM provider credentials (OpenAI, Anthropic, etc.)

**Recommended for Production**:
- 16GB+ RAM for concurrent testing
- 50GB+ disk space for logs and results
- SSD storage for database performance
- Load balancer for horizontal scaling

### 4.5 Scalability Architecture

**Horizontal Scaling**:
- Each service can scale independently
- Multiple Executor containers for parallel tool execution
- Load balancing across agent instances

**High Availability**:
- PostgreSQL replication for data persistence
- Redis clustering for distributed caching
- MinIO distributed mode for storage redundancy



---

**Navigation**: [📚 Series Overview](./00_Series_Overview.md) | [Part 2 →](./02_Autonomous_Capabilities.md)
**Part 1 of 3** | Lines 1-450 of original document
