# Docker Infrastructure Architecture

**File:** Docker-Architecture.md
**Created:** 2025-11-03 17:09:06 CST
**Version:** v1.0.0
**Author:** System Architecture Analysis
**Purpose:** Comprehensive documentation of AEON Docker infrastructure
**Status:** ACTIVE

**Tags:** #docker #infrastructure #architecture #networking #containers

---

## Executive Summary

The AEON Docker infrastructure consists of 7 containers orchestrated on a dedicated bridge network (`openspg-network`). The architecture follows a microservices pattern with specialized containers for UI, backend services, databases, vector storage, and object storage. All containers communicate over an isolated network (172.18.0.0/16) ensuring secure inter-service communication.

**Last Updated:** 2025-11-03 17:09:06 CST

---

## Network Topology

### Network Configuration

**Network Name:** `openspg-network`
**Network ID:** `ec46b9ce8213e95e2849dd6deee8325d871a25d6e28dc825793b02198eb1eade`
**Driver:** bridge
**Subnet:** 172.18.0.0/16
**Gateway:** 172.18.0.1
**Created:** 2025-10-27 02:15:41 UTC

### Network Topology Diagram

```
                    Docker Bridge Network: openspg-network
                           172.18.0.0/16
                                 │
                           Gateway: 172.18.0.1
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   ┌────┴────┐            ┌─────┴──────┐          ┌─────┴──────┐
   │ Storage │            │  Database  │          │  Services  │
   │  Layer  │            │   Layer    │          │   Layer    │
   └────┬────┘            └─────┬──────┘          └─────┬──────┘
        │                       │                        │
  ┌─────┼──────────┐      ┌────┼─────┬─────────┐  ┌────┼─────┬──────────┐
  │     │          │      │    │     │         │  │    │     │          │
MinIO  Qdrant   Neo4j   MySQL  │     │   OpenSPG  │   AEON-UI  Agent-Zero
.0.2    .0.6     .0.3    .0.5   │     │   Server   │    .0.8      .0.7
                                 │     │    .0.4    │
                           Graph Store  Relational   Web UI   AI Agent
                           Vector DB    Database     Layer    Layer
```

---

## Container Inventory

### Complete Container List

| Container Name | IP Address | Image | Status | Ports | Role |
|----------------|------------|-------|--------|-------|------|
| **openspg-minio** | 172.18.0.2 | minio/minio:latest | running | 9000, 9001 | Object Storage |
| **openspg-neo4j** | 172.18.0.3 | neo4j:5.26-community | running | 7473, 7474, 7687 | Graph Database |
| **openspg-server** | 172.18.0.4 | spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-server:latest | running | 8887 | Backend API Server |
| **openspg-mysql** | 172.18.0.5 | spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-mysql:latest | running | 3306 | Relational Database |
| **openspg-qdrant** | 172.18.0.6 | qdrant/qdrant:latest | running | 6333, 6334 | Vector Database |
| **agent-zero-main** | 172.18.0.7 | (Custom) | running | N/A | AI Agent Service |
| **aeon-ui** | 172.18.0.8 | aeon-ui:latest | running | 3000 | Web User Interface |

### Container Details

#### 1. OpenSPG MinIO (172.18.0.2)
**Purpose:** S3-compatible object storage for files, documents, and binary data
**Image:** `minio/minio:latest`
**Exposed Ports:**
- 9000/tcp - S3 API endpoint
- 9001/tcp - MinIO Console (web UI)

**Function:** Provides distributed object storage for the knowledge graph system, storing raw documents, processed files, and binary assets.

**Backlinks:** [[Object-Storage]] [[MinIO-Configuration]] [[Data-Storage-Strategy]]

---

#### 2. OpenSPG Neo4j (172.18.0.3)
**Purpose:** Graph database for knowledge graph storage and traversal
**Image:** `neo4j:5.26-community`
**Exposed Ports:**
- 7473/tcp - HTTPS endpoint
- 7474/tcp - HTTP endpoint (web UI)
- 7687/tcp - Bolt protocol

**Function:** Core graph database storing entities, relationships, and knowledge graph structures. Provides Cypher query interface and graph analytics.

**Backlinks:** [[Graph-Database]] [[Neo4j-Configuration]] [[Knowledge-Graph-Schema]]

---

#### 3. OpenSPG Server (172.18.0.4)
**Purpose:** Backend API server and orchestration layer
**Image:** `spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-server:latest`
**Exposed Ports:**
- 8887/tcp - REST API endpoint

**Environment Configuration:**
- **Java Heap:** -Xms2048m -Xmx8192m (2GB-8GB)
- **Character Encoding:** UTF-8

**Function:** Central backend service coordinating knowledge graph operations, API endpoints, and inter-service communication. Manages business logic and data processing workflows.

**Backlinks:** [[Backend-API]] [[OpenSPG-Server-Configuration]] [[API-Endpoints]]

---

#### 4. OpenSPG MySQL (172.18.0.5)
**Purpose:** Relational database for structured metadata and application state
**Image:** `spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-mysql:latest`
**Exposed Ports:**
- 3306/tcp - MySQL protocol

**Function:** Stores relational data, user accounts, application configuration, and structured metadata that complements the graph database.

**Backlinks:** [[Relational-Database]] [[MySQL-Schema]] [[Database-Backup-Strategy]]

---

#### 5. OpenSPG Qdrant (172.18.0.6)
**Purpose:** Vector database for semantic search and embeddings
**Image:** `qdrant/qdrant:latest`
**Exposed Ports:**
- 6333/tcp - HTTP API
- 6334/tcp - gRPC API

**Function:** High-performance vector database storing document embeddings for semantic search, similarity matching, and AI-powered retrieval operations.

**Backlinks:** [[Vector-Database]] [[Semantic-Search]] [[Embeddings-Strategy]]

---

#### 6. Agent Zero Main (172.18.0.7)
**Purpose:** AI agent orchestration and autonomous task execution
**Image:** Custom implementation
**Status:** Running

**Function:** Autonomous AI agent system for automated analysis, decision-making, and task orchestration within the knowledge graph ecosystem.

**Backlinks:** [[AI-Agents]] [[Agent-Zero-Architecture]] [[Autonomous-Systems]]

---

#### 7. AEON UI (172.18.0.8)
**Purpose:** Web-based user interface
**Image:** `aeon-ui:latest`
**Exposed Ports:**
- 3000/tcp - Web server

**Function:** Frontend web application providing user interface for knowledge graph visualization, management, and interaction.

**Backlinks:** [[Frontend-UI]] [[Web-Interface]] [[User-Experience]]

---

## Inter-Container Communication Patterns

### Communication Matrix

| Source Container | Target Container(s) | Protocol | Purpose |
|------------------|---------------------|----------|---------|
| **aeon-ui** (172.18.0.8) | openspg-server (172.18.0.4) | HTTP/REST | API requests, data queries |
| **openspg-server** (172.18.0.4) | openspg-neo4j (172.18.0.3) | Bolt (7687) | Graph queries and updates |
| **openspg-server** (172.18.0.4) | openspg-mysql (172.18.0.5) | MySQL (3306) | Relational data operations |
| **openspg-server** (172.18.0.4) | openspg-qdrant (172.18.0.6) | HTTP/gRPC | Vector search queries |
| **openspg-server** (172.18.0.4) | openspg-minio (172.18.0.2) | S3 API (9000) | Object storage operations |
| **agent-zero-main** (172.18.0.7) | openspg-server (172.18.0.4) | HTTP/REST | Agent task execution |
| **agent-zero-main** (172.18.0.7) | openspg-qdrant (172.18.0.6) | HTTP | Direct vector operations |

### Data Flow Patterns

#### 1. User Query Flow
```
User → AEON UI (172.18.0.8:3000)
     → OpenSPG Server (172.18.0.4:8887)
     → Neo4j (172.18.0.3:7687) [Graph Data]
     → Qdrant (172.18.0.6:6333) [Semantic Search]
     → MySQL (172.18.0.5:3306) [Metadata]
     → Response to User
```

#### 2. Document Ingestion Flow
```
Document Upload → AEON UI
               → OpenSPG Server
               → MinIO (172.18.0.2:9000) [Store Binary]
               → Processing Pipeline
               → Qdrant [Store Embeddings]
               → Neo4j [Store Graph]
               → MySQL [Store Metadata]
```

#### 3. AI Agent Workflow
```
Agent Zero (172.18.0.7)
  → Retrieve embeddings from Qdrant
  → Query knowledge graph from Neo4j (via Server)
  → Execute autonomous tasks
  → Update results via OpenSPG Server
```

---

## Network Security Architecture

### Network Isolation
- **Isolated Bridge Network:** All containers operate on dedicated `openspg-network` (172.18.0.0/16)
- **No Direct Host Access:** Containers cannot directly access host network without explicit port mapping
- **Internal DNS:** Docker provides automatic service discovery via container names

### Port Exposure Strategy

**Externally Exposed Ports** (mapped to host):
- Check individual container port mappings for public access

**Internal-Only Ports** (network-isolated):
- All container-to-container communication remains within 172.18.0.0/16 subnet
- Inter-service communication does not traverse public network

### Security Considerations

1. **Network Segmentation:** Containers operate in isolated network namespace
2. **Credential Management:** Database credentials should use Docker secrets or environment variables
3. **TLS/SSL:** HTTPS endpoints (Neo4j 7473) for encrypted communication
4. **Access Control:** MySQL, Neo4j, MinIO require authentication
5. **Firewall Rules:** Host firewall should restrict access to exposed container ports

**Backlinks:** [[Network-Security]] [[Container-Security]] [[Security-Best-Practices]]

---

## Resource Allocation

### Java Heap Configuration (OpenSPG Server)
- **Minimum Heap:** 2048 MB (-Xms2048m)
- **Maximum Heap:** 8192 MB (-Xmx8192m)
- **Recommendation:** Monitor memory usage and adjust based on workload

### Database Storage
- **Neo4j:** Graph data persistence
- **MySQL:** Relational data persistence
- **Qdrant:** Vector index persistence
- **MinIO:** Object storage persistence

**Note:** All containers should have volume mounts for persistent data storage.

**Backlinks:** [[Resource-Management]] [[Performance-Tuning]] [[Capacity-Planning]]

---

## Deployment Metadata

### Docker Compose Configuration
- **Config Hash:** `1ddd0129e1b1fbda225b8a9e7a8434ce6822f5a5cf124ac5f82a25b84716a209`
- **Compose Version:** 2.40.0
- **Project Name:** `2_oxot_projects_dev`
- **Network Creation Date:** 2025-10-27 02:15:41 UTC

### Container Orchestration
All containers are managed via Docker Compose, enabling:
- Single-command deployment (`docker-compose up`)
- Coordinated lifecycle management
- Service dependency management
- Unified networking configuration

**Backlinks:** [[Docker-Compose-Configuration]] [[Deployment-Procedures]]

---

## Architecture Patterns

### Microservices Architecture
The system follows a microservices pattern with:
- **Service Separation:** Each container handles specific domain functionality
- **Loose Coupling:** Services communicate via well-defined APIs
- **Technology Diversity:** Best-of-breed technologies (Neo4j for graphs, Qdrant for vectors)
- **Independent Scaling:** Each service can scale independently

### Data Layer Architecture
Three-tier data storage strategy:
1. **Graph Layer:** Neo4j for relationships and graph traversal
2. **Vector Layer:** Qdrant for semantic search and embeddings
3. **Relational Layer:** MySQL for structured metadata
4. **Object Layer:** MinIO for binary/document storage

**Backlinks:** [[System-Architecture]] [[Microservices-Design]] [[Data-Architecture]]

---

## Monitoring and Observability

### Health Check Endpoints
- **Neo4j:** http://172.18.0.3:7474 (web console)
- **MinIO:** http://172.18.0.2:9001 (console)
- **OpenSPG Server:** http://172.18.0.4:8887/health (if implemented)
- **Qdrant:** http://172.18.0.6:6333/metrics (Prometheus metrics)

### Recommended Monitoring
1. **Container Health:** `docker ps` and `docker stats`
2. **Network Traffic:** Monitor inter-container communication patterns
3. **Resource Usage:** CPU, memory, disk I/O per container
4. **Database Performance:** Query response times, connection pools
5. **Application Logs:** Centralized logging for all containers

**Backlinks:** [[Monitoring-Strategy]] [[Observability]] [[Logging]]

---

## Disaster Recovery

### Backup Strategy
1. **Database Backups:**
   - Neo4j: Graph database dumps
   - MySQL: SQL dumps or binary logs
   - Qdrant: Snapshot exports

2. **Object Storage:**
   - MinIO: S3-compatible backup tools

3. **Configuration:**
   - Docker Compose files
   - Environment configurations
   - Network definitions

### Recovery Procedures
1. Restore Docker network configuration
2. Restore container volumes
3. Restore database backups
4. Restart containers in dependency order
5. Verify inter-service connectivity

**Backlinks:** [[Backup-Procedures]] [[Disaster-Recovery-Plan]] [[Business-Continuity]]

---

## Known Issues and Limitations

### Current Constraints
1. **Single-Host Deployment:** All containers run on single Docker host
2. **No High Availability:** Single-instance containers (no redundancy)
3. **Resource Limits:** Java heap fixed at 8GB maximum for OpenSPG Server
4. **Network Scalability:** Bridge network limited to single-host

### Future Enhancements
1. **Kubernetes Migration:** Multi-host orchestration for high availability
2. **Load Balancing:** Nginx/Traefik reverse proxy for traffic distribution
3. **Service Mesh:** Istio/Linkerd for advanced networking features
4. **Monitoring Stack:** Prometheus + Grafana for comprehensive observability

**Backlinks:** [[Technical-Debt]] [[Roadmap]] [[Infrastructure-Improvements]]

---

## Related Documentation

### Infrastructure Documentation
- [[Network-Configuration]]
- [[Container-Management]]
- [[Docker-Compose-Reference]]
- [[Service-Discovery]]

### Database Documentation
- [[Neo4j-Administration]]
- [[MySQL-Administration]]
- [[Qdrant-Operations]]
- [[MinIO-Operations]]

### Application Documentation
- [[OpenSPG-Server-Documentation]]
- [[AEON-UI-Documentation]]
- [[Agent-Zero-Documentation]]

### Security Documentation
- [[Security-Hardening]]
- [[Access-Control-Policies]]
- [[Network-Security-Rules]]
- [[Credential-Management]]

### Operational Documentation
- [[Deployment-Guide]]
- [[Troubleshooting-Guide]]
- [[Maintenance-Procedures]]
- [[Scaling-Strategy]]

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0.0 | 2025-11-03 | System Analysis | Initial architecture documentation |

---

**Document Status:** ACTIVE
**Review Cycle:** Quarterly
**Next Review:** 2025-02-03
**Owner:** Infrastructure Team
**Classification:** Internal

---

*This documentation was generated from live Docker inspection data on 2025-11-03 17:09:06 CST*
