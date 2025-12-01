# OpenSPG Server

**File:** OpenSPG-Server.md
**Created:** 2025-11-03 17:12:04 CST
**Version:** v1.0.0
**Status:** ACTIVE
**Tags:** #openspg #knowledge-graph #server #api #backend

---

## Executive Summary

OpenSPG Server is the core backend service for the OpenSPG (Open Semantic-enhanced Programmable Graph) knowledge graph platform. It provides RESTful API endpoints for schema management, knowledge graph operations, data processing pipelines, and integration with multiple storage backends including MySQL, Neo4j, MinIO, and Qdrant vector database.

**Current Status:**
- **Container Status:** Running
- **Health Status:** ⚠️ Unhealthy (service operational but health check failing)
- **Port:** 8887
- **IP Address:** 172.18.0.4
- **Network:** openspg-network
- **Image:** spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-server:latest

---

## System Architecture

### Container Configuration

```yaml
Container Details:
  Name: openspg-server
  Image: spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-server:latest
  Port Mapping: 0.0.0.0:8887 → 8887/tcp
  Network: openspg-network (172.18.0.4/16)
  Timezone: Asia/Shanghai

Runtime Configuration:
  Java Options: -Xms2048m -Xmx8192m -Dfile.encoding=UTF-8
  Memory Allocation:
    - Minimum Heap: 2048 MB
    - Maximum Heap: 8192 MB
  Encoding: UTF-8
  Locale: C.UTF-8

Volume Mounts:
  - openspg-server-logs → /app/logs (RW)
  - openspg-shared-data → /shared (RW)
  - /etc/localtime → /etc/localtime (RO)
```

### Network Topology

```
OpenSPG Ecosystem Network (172.18.0.0/16):
┌─────────────────────────────────────────────────────────┐
│                    openspg-network                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐         ┌──────────────┐             │
│  │  AEON-UI     │────────▶│ OpenSPG      │             │
│  │  172.18.0.8  │         │ Server       │             │
│  │  Port: 3000  │         │ 172.18.0.4   │             │
│  └──────────────┘         │ Port: 8887   │             │
│                           └──────┬───────┘             │
│                                  │                      │
│         ┌────────────────────────┼──────────┐          │
│         ▼                        ▼          ▼          │
│  ┌────────────┐        ┌──────────────┐ ┌─────────┐   │
│  │ MySQL      │        │ Neo4j Graph  │ │ MinIO   │   │
│  │ 172.18.0.5 │        │ 172.18.0.3   │ │Storage  │   │
│  │ Port: 3306 │        │ Port: 7687   │ │172.18.0.2│  │
│  └────────────┘        └──────────────┘ └─────────┘   │
│         │                                      │        │
│         └──────────────────┬──────────────────┘        │
│                            ▼                            │
│                   ┌──────────────┐                      │
│                   │ Qdrant       │                      │
│                   │ Vector DB    │                      │
│                   │ 172.18.0.6   │                      │
│                   │ Port: 6333   │                      │
│                   └──────────────┘                      │
└─────────────────────────────────────────────────────────┘
```

### Component Connections

**Database Integrations:**
- **MySQL (172.18.0.5:3306)** - Primary relational data storage
  - Schema metadata
  - Project configurations
  - Job scheduling data
  - User authentication

- **Neo4j (172.18.0.3:7687)** - Graph database backend
  - Knowledge graph storage
  - Ontology relationships
  - Entity connections
  - Property graphs

- **MinIO (172.18.0.2:9000)** - Object storage
  - File uploads
  - Data imports/exports
  - Large binary objects
  - Model artifacts

- **Qdrant (172.18.0.6:6333)** - Vector database
  - Semantic embeddings
  - Vector similarity search
  - AI/ML model outputs

**UI Integration:**
- **AEON-UI (172.18.0.8:3000)** - Web interface frontend
  - User management
  - Schema design interface
  - Knowledge graph visualization
  - Data import/export tools

---

## Core Capabilities

### 1. Schema Management

OpenSPG Server provides comprehensive schema definition and management:

- **Project Management:** Create and manage knowledge graph projects
- **Ontology Design:** Define entity types, properties, and relationships
- **Schema Versioning:** Track schema evolution and migrations
- **Type System:** Strong typing for entities and properties
- **Validation Rules:** Schema-level data validation

### 2. Knowledge Graph Operations

- **Entity CRUD:** Create, read, update, delete entities
- **Relationship Management:** Define and manage graph connections
- **Query Processing:** Graph traversal and pattern matching
- **Batch Operations:** Bulk entity and relationship operations
- **Import/Export:** Data migration and backup capabilities

### 3. Data Processing Pipeline

**Scheduler System:**
```
Components:
  - GenerateInstanceScheduleHandler: Create job instances from periodic jobs
  - ExecuteInstanceScheduleHandler: Execute scheduled job instances
  - Distributed Lock: Coordinator-based locking (172.18.0.4)

Capabilities:
  - Periodic job execution
  - Instance tracking
  - Distributed coordination
  - Automatic retry logic
```

### 4. RESTful API

**Base Endpoint:** `http://172.18.0.4:8887`

**API Structure:**
```
/api/
├── /health              - Health check endpoint
├── /schema/             - Schema management
│   ├── /project/list    - List all projects
│   └── /project/*       - Project operations
├── /graph/              - Graph operations
├── /data/               - Data import/export
└── /job/                - Job scheduling
```

**Authentication:**
- ACL-based access control
- Filter-based authorization
- Session management
- Public health endpoints

---

## Service Operations

### Health Monitoring

**Current Health Status:**
- ✅ **Application:** Running normally
- ⚠️ **Health Check:** Failing (investigating)
- ✅ **Scheduler:** Active and functioning
- ✅ **Database Connections:** Operational

**Health Endpoint Behavior:**
```
GET /health
Response: 200 OK (endpoint accessible)
Logging: Request tracked with correlation ID
Processing: 2-3ms average response time
```

**Investigation Notes:**
The container health check is marked as "unhealthy" despite the service functioning normally. This appears to be a Docker health check configuration issue rather than actual service failure:
- Health endpoint responds successfully
- Logs show normal operations
- Scheduler tasks executing properly
- No error patterns detected

### Logging System

**Log Configuration:**
```
Location: /app/logs/ (mounted from openspg-server-logs volume)
Format: Timestamp [CorrelationID] [Context] [Thread] LEVEL Class - Message
Timezone: Asia/Shanghai
```

**Log Patterns:**
```java
Example Entry:
2025-11-04 07:08:46,350 [ac120004176221132635049531] [] [httpReq-58]
INFO c.a.o.a.h.s.f.AclFilter - HTTP Request - URL: /health, Method: GET, Params: {}
```

**Key Log Categories:**
- `AclFilter`: HTTP request authorization and access control
- `SchedulerHandlerClient`: Job scheduling operations
- `SchedulerExecuteServiceImpl`: Job execution logic
- `ExecuteInstanceScheduleHandler`: Job instance management
- `GenerateInstanceScheduleHandler`: Job generation logic

### Scheduler Operations

**Execution Cycle:**
```
Every 60 seconds:
1. Acquire distributed lock (IP: 172.18.0.4)
2. Check periodic jobs → Generate new instances
3. Check unfinished instances → Execute pending jobs
4. Release lock after completion
```

**Current Scheduler State:**
- Periodic Jobs: 0 active
- Unfinished Instances: 0 pending
- Execution Time: ~1ms per cycle
- Lock Management: Successful acquisition/release

---

## Integration Guide

### Connecting to OpenSPG Server

**From AEON-UI:**
```javascript
// Frontend configuration
const OPENSPG_API_BASE = 'http://172.18.0.4:8887';

// Example API call
fetch(`${OPENSPG_API_BASE}/api/schema/project/list`, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
});
```

**Direct API Access:**
```bash
# Health check
curl http://172.18.0.4:8887/health

# List projects (requires authentication)
curl -X GET http://172.18.0.4:8887/api/schema/project/list \
  -H "Content-Type: application/json"
```

### Database Connections

**MySQL Connection:**
```yaml
Host: openspg-mysql (172.18.0.5)
Port: 3306
Database: openspg
Purpose: Schema metadata, jobs, authentication
```

**Neo4j Connection:**
```yaml
Host: openspg-neo4j (172.18.0.3)
Port: 7687 (Bolt protocol)
Purpose: Knowledge graph storage
```

**MinIO Connection:**
```yaml
Host: openspg-minio (172.18.0.2)
Port: 9000 (API), 9001 (Console)
Purpose: Object storage for files and artifacts
```

**Qdrant Connection:**
```yaml
Host: openspg-qdrant (172.18.0.6)
Port: 6333
Purpose: Vector embeddings and similarity search
```

---

## Configuration Parameters

### Java Runtime

```properties
Heap Memory:
  Initial (Xms): 2048 MB
  Maximum (Xmx): 8192 MB

System Properties:
  file.encoding: UTF-8
  user.timezone: Asia/Shanghai

Python Environment:
  Miniconda: /home/admin/miniconda3
  Path: Included in system PATH
```

### Environment Variables

```bash
# Locale and encoding
LANG=C.UTF-8
DEBIAN_FRONTEND=noninteractive

# Timezone
TZ=Asia/Shanghai

# Java options
JAVA_OPTS=-Xms2048m -Xmx8192m -Dfile.encoding=UTF-8

# Application path
PATH=/home/admin/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

### Volume Persistence

```yaml
Logs Volume:
  Name: openspg-server-logs
  Mount: /app/logs
  Access: Read-Write
  Purpose: Application logging

Shared Data Volume:
  Name: openspg-shared-data
  Mount: /shared
  Access: Read-Write
  Purpose: Cross-container data sharing

Time Sync:
  Source: /etc/localtime (host)
  Mount: /etc/localtime
  Access: Read-Only
  Purpose: Timezone synchronization
```

---

## Operations Guide

### Starting the Service

```bash
# Start OpenSPG Server
docker start openspg-server

# Verify startup
docker logs -f openspg-server

# Check health
curl http://172.18.0.4:8887/health
```

### Monitoring

```bash
# Check container status
docker ps --filter name=openspg-server

# View real-time logs
docker logs -f --tail 100 openspg-server

# Inspect configuration
docker inspect openspg-server

# Network connectivity
docker exec openspg-server ping -c 3 openspg-mysql
docker exec openspg-server ping -c 3 openspg-neo4j
```

### Troubleshooting

**Health Check Issues:**
```bash
# Current issue: Health marked as unhealthy
# Symptom: Service functions normally, health check fails
# Investigation:
#   1. Health endpoint responds successfully (200 OK)
#   2. Logs show normal operations
#   3. No error patterns detected
#
# Likely cause: Docker health check configuration
# Recommendation: Review Dockerfile HEALTHCHECK directive

# Verify endpoint manually
curl -v http://172.18.0.4:8887/health

# Check internal health from container
docker exec openspg-server curl -s localhost:8887/health
```

**Connection Issues:**
```bash
# Test database connectivity
docker exec openspg-server ping -c 3 openspg-mysql
docker exec openspg-server ping -c 3 openspg-neo4j

# Verify network
docker network inspect openspg-network
```

**Performance Monitoring:**
```bash
# Container resource usage
docker stats openspg-server

# Java heap usage (if JMX enabled)
docker exec openspg-server jstat -gc 1

# Active threads
docker exec openspg-server jstack 1 | grep "java.lang.Thread.State"
```

---

## Security Considerations

### Access Control

- **ACL Filter:** All HTTP requests pass through ACL-based authorization
- **Session Management:** Correlation IDs track all requests
- **Public Endpoints:** Health checks exempt from authentication
- **Authentication Required:** Most API endpoints require valid credentials

### Network Security

```
Isolation:
  - Container network: openspg-network (isolated bridge)
  - Internal communication only
  - No direct external exposure

Port Exposure:
  - Host: 0.0.0.0:8887 (accessible from host network)
  - Container: 8887/tcp

Recommendations:
  - Use reverse proxy (Traefik/Nginx) for production
  - Enable HTTPS/TLS
  - Implement rate limiting
  - Add IP whitelisting if needed
```

---

## Performance Characteristics

### Response Times

```
Health Endpoint: 2-3 ms average
Scheduler Operations: ~1 ms per cycle
Lock Acquisition: < 10 ms
Database Queries: Varies by complexity
```

### Resource Usage

```
Memory:
  Allocated: 2048-8192 MB (Java heap)
  Typical Usage: Moderate (depends on workload)

CPU:
  Baseline: Low (scheduler and health checks)
  Peak: High (during bulk operations)

Network:
  Inbound: API requests, database queries
  Outbound: Database writes, object storage
```

### Scalability

- Distributed lock coordination supports multiple instances
- Scheduler designed for distributed execution
- Stateless API design enables horizontal scaling
- Shared storage (MySQL, Neo4j, MinIO) as bottleneck

---

## Development and API Reference

### API Architecture

**Design Patterns:**
- RESTful endpoints
- JSON request/response format
- Correlation ID tracking
- Filter-based middleware (ACL)
- Error handling standardization

**Request Flow:**
```
Client Request
    ↓
AclFilter (Authorization)
    ↓
Controller (Routing)
    ↓
Service Layer (Business Logic)
    ↓
Repository (Data Access)
    ↓
Database (MySQL/Neo4j/MinIO/Qdrant)
```

### Common Endpoints

```
GET  /health                      - Service health check
GET  /api/schema/project/list     - List all projects
POST /api/schema/project          - Create new project
GET  /api/schema/project/{id}     - Get project details
PUT  /api/schema/project/{id}     - Update project
DEL  /api/schema/project/{id}     - Delete project

GET  /api/graph/entity/{id}       - Get entity
POST /api/graph/entity            - Create entity
PUT  /api/graph/entity/{id}       - Update entity
DEL  /api/graph/entity/{id}       - Delete entity

POST /api/data/import             - Import data
GET  /api/data/export             - Export data

GET  /api/job/list                - List scheduled jobs
POST /api/job                     - Create job
GET  /api/job/{id}/status         - Job status
```

---

## Related Components

### Backend Services
- [[MySQL]] - Relational database for metadata and configuration
- [[Neo4j-Database]] - Graph database for knowledge storage
- [[MinIO-Storage]] - Object storage for files and artifacts
- [[Qdrant]] - Vector database for semantic search

### Frontend
- [[AEON-UI]] - Web interface for OpenSPG management

### Infrastructure
- Docker containerization
- openspg-network bridge network
- Shared volume storage

---

## Maintenance and Operations

### Backup Strategy

```bash
# Backup logs
docker run --rm \
  --volumes-from openspg-server \
  -v $(pwd):/backup \
  alpine tar czf /backup/openspg-server-logs-$(date +%Y%m%d).tar.gz /app/logs

# Backup shared data
docker run --rm \
  --volumes-from openspg-server \
  -v $(pwd):/backup \
  alpine tar czf /backup/openspg-shared-data-$(date +%Y%m%d).tar.gz /shared
```

### Upgrade Procedure

```bash
# 1. Backup current state
docker commit openspg-server openspg-server-backup

# 2. Stop container
docker stop openspg-server

# 3. Pull new image
docker pull spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-server:latest

# 4. Remove old container
docker rm openspg-server

# 5. Recreate with same configuration
# (Use original docker run command)

# 6. Verify operation
docker logs openspg-server
curl http://172.18.0.4:8887/health
```

### Log Rotation

```bash
# Manual log cleanup
docker exec openspg-server sh -c "cd /app/logs && find . -name '*.log' -mtime +30 -delete"

# Automated with cron
# Add to host crontab:
# 0 2 * * * docker exec openspg-server sh -c "cd /app/logs && find . -name '*.log' -mtime +30 -delete"
```

---

## Future Enhancements

**Planned Improvements:**
1. Health check configuration fix
2. API documentation (Swagger/OpenAPI)
3. Metrics endpoint (Prometheus format)
4. Distributed tracing (OpenTelemetry)
5. Advanced monitoring dashboard
6. Cache layer (Redis) for performance
7. GraphQL endpoint support
8. WebSocket support for real-time updates

**Optimization Opportunities:**
- Connection pooling tuning
- Query optimization
- Caching strategy implementation
- Load balancing for multiple instances
- Database index optimization

---

## Technical Specifications

```yaml
Component: OpenSPG Server
Type: Backend API Service
Language: Java
Framework: Spring Boot (inferred)
Communication: REST API
Data Format: JSON
Authentication: ACL-based
Logging: SLF4J/Logback
Packaging: Docker container

Dependencies:
  - MySQL: Primary data store
  - Neo4j: Graph database
  - MinIO: Object storage
  - Qdrant: Vector database
  - Python: Miniconda environment

Port: 8887
Network: openspg-network (172.18.0.4)
Image: spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-server:latest

Performance:
  Memory: 2-8 GB (configurable)
  Response Time: 2-50ms (endpoint dependent)
  Concurrency: Thread-pool based
  Scalability: Horizontal (with load balancer)
```

---

## Contact and Support

**Component Owner:** AEON Digital Twin Project
**Documentation:** This file
**Related Systems:** MySQL, Neo4j, MinIO, Qdrant, AEON-UI
**Network:** openspg-network (172.18.0.0/16)

**For Issues:**
- Check logs: `docker logs openspg-server`
- Verify health: `curl http://172.18.0.4:8887/health`
- Review database connectivity
- Consult related component documentation

---

**Document Information:**
- **Last Updated:** 2025-11-03 17:12:04 CST
- **Status:** Active and operational
- **Health Investigation:** In progress
- **Next Review:** After health check resolution
