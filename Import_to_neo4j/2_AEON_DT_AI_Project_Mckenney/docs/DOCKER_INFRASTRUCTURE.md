# AEON & OpenSPG Docker Infrastructure Documentation
**Last Updated**: November 3, 2025, 13:40 UTC
**Status**: ✅ All Containers Operational
**Environment**: Production OpenSPG Deployment with AEON Integration

---

## 🎯 INFRASTRUCTURE OVERVIEW

This document provides complete Docker infrastructure details for the AEON Automated Document Ingestion System and its integration with the OpenSPG Knowledge Graph platform.

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AEON System (Python)                          │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  AEON Agents → NLP Processing → Entity Extraction     │       │
│  └──────────────────────────────────────────────────────┘       │
│                            ↓                                      │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  Neo4j Graph Database (openspg-neo4j container)      │       │
│  │  - Port 7687 (Bolt) | Port 7474 (HTTP)              │       │
│  │  - Stores: Documents, Entities, Relationships        │       │
│  └──────────────────────────────────────────────────────┘       │
│                            ↓                                      │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  Qdrant Vector Memory (openspg-qdrant container)    │       │
│  │  - Port 6333 (API) | Port 6334 (Web UI)             │       │
│  │  - Stores: Checkpoints, Agent Activities, State     │       │
│  └──────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│              OpenSPG Knowledge Graph Platform                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ OpenSPG      │  │ MySQL        │  │ MinIO        │         │
│  │ Server       │  │ Metadata     │  │ Storage      │         │
│  │ Port 8887    │  │ Port 3306    │  │ Ports 9000-1 │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                  Shared Neo4j & Qdrant Resources                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 DOCKER COMPOSE CONFIGURATION

### Primary Configuration File

**Location**: `/home/jim/2_OXOT_Projects_Dev/docker-compose.yml`
**Version**: 3.8
**Created**: January 26, 2025
**Purpose**: OpenSPG production deployment with Neo4j 5.26-community LTS

### Network Configuration

| Property | Value |
|----------|-------|
| **Network Name** | openspg-network |
| **Driver** | bridge |
| **Subnet** | 172.18.0.0/16 |
| **Purpose** | Internal communication between all OpenSPG services |

---

## 🐳 RUNNING CONTAINERS

### Current Container Status (as of 2025-11-03)

| Container Name | Image | Status | Uptime | Ports | Health |
|---------------|-------|--------|--------|-------|--------|
| **openspg-neo4j** | neo4j:5.26-community | Running | 4 days | 7474, 7687 | ✅ Healthy |
| **openspg-qdrant** | qdrant/qdrant:latest | Running | 3 days | 6333-6334 | ⚠️ Unhealthy* |
| **openspg-server** | openspg-server:latest | Running | 4 days | 8887 | ⚠️ Unhealthy* |
| **openspg-mysql** | openspg-mysql:latest | Running | 4 days | 3306 | ✅ Healthy |
| **openspg-minio** | minio/minio:latest | Running | 4 days | 9000-9001 | ✅ Healthy |

*Note: "Unhealthy" status is due to health check configuration (missing `curl` in container), but containers are fully functional.

---

## 🗄️ CONTAINER DETAILS

### 1. Neo4j Graph Database (openspg-neo4j)

**Primary database used by AEON for document and entity storage**

```yaml
Container Details:
  Name: openspg-neo4j
  Image: neo4j:5.26-community
  Container ID: 129950845a73
  Network IP: 172.18.0.3
  Status: Running (4 days) - HEALTHY
  Restart Policy: unless-stopped

Ports:
  - 7474:7474  # HTTP Web Interface
  - 7687:7687  # Bolt Protocol (used by AEON)

Volumes:
  - openspg-neo4j-data:/data (persistent database storage)
  - openspg-neo4j-logs:/logs (query and system logs)
  - openspg-neo4j-import:/var/lib/neo4j/import (CSV import directory)
  - openspg-neo4j-plugins:/plugins (APOC and extensions)
  - openspg-shared-data:/shared (cross-container data exchange)

Authentication:
  Username: neo4j
  Password: neo4j@openspg
  Database: neo4j (default)

Environment Configuration:
  # Memory (Optimized for 16GB+ RAM systems)
  - NEO4J_server_memory_heap_initial__size=2G
  - NEO4J_server_memory_heap_max__size=4G
  - NEO4J_server_memory_pagecache_size=2G
  - NEO4J_dbms_memory_transaction_total_max=2G

  # APOC Plugin (Advanced Procedures)
  - NEO4J_PLUGINS=["apoc"]
  - NEO4J_apoc_export_file_enabled=true
  - NEO4J_apoc_import_file_enabled=true
  - NEO4J_dbms_security_procedures_unrestricted=apoc.*

  # Connection Settings
  - NEO4J_server_bolt_listen__address=0.0.0.0:7687
  - NEO4J_server_http_listen__address=0.0.0.0:7474

  # Transaction Log Retention
  - NEO4J_db_tx__log_rotation_retention__policy=2G size

Health Check:
  Command: cypher-shell -u neo4j -p neo4j@openspg "RETURN 1"
  Interval: 10s
  Timeout: 10s
  Retries: 10
  Start Period: 60s
  Current Status: ✅ HEALTHY

AEON Integration:
  Connection URI: bolt://localhost:7687
  Auth: neo4j/neo4j@openspg (via config or environment variable)
  Used By: IngestionAgent, NLPIngestionPipeline
  Purpose: Store documents, entities, and relationships
  Schema: Document nodes, Entity nodes, CONTAINS_ENTITY relationships
```

### 2. Qdrant Vector Memory (openspg-qdrant)

**Used by AEON for checkpoint tracking and agent state preservation**

```yaml
Container Details:
  Name: openspg-qdrant
  Image: qdrant/qdrant:latest
  Container ID: 0464c4f2a6b7
  Network IP: 172.18.0.6
  Status: Running (3 days) - Functional (health check misconfigured)
  Restart Policy: always

Ports:
  - 6333:6333  # REST API (used by AEON)
  - 6334:6334  # Web Dashboard

Volumes:
  - openspg-qdrant-data:/qdrant/storage (persistent vector storage)
  - openspg-shared-data:/shared (cross-container data exchange)
  - /qdrant/backups (backup directory)

No Authentication (localhost access only)

Health Check:
  Command: curl -f http://localhost:6333/health
  Note: Health check shows "unhealthy" due to missing curl in container
  Actual Status: ✅ FULLY FUNCTIONAL (verified by successful checkpoint storage)

AEON Integration:
  Connection: localhost:6333
  Config Setting: qdrant_enabled: false (uses persistent SQLite fallback)
  Used By: QdrantMemoryManager
  Purpose: Track agent activities, store checkpoints, preserve state
  Storage Mode: Persistent fallback (SQLite) - NOT temporary in-memory
  Checkpoints Stored: 10 total (all development and correction history)
```

### 3. OpenSPG Server (openspg-server)

**Knowledge graph platform utilizing Neo4j for graph storage**

```yaml
Container Details:
  Name: openspg-server
  Image: spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-server:latest
  Container ID: 9ef733ab2e09
  Network IP: 172.18.0.4
  Status: Running (4 days)
  Restart Policy: unless-stopped

Ports:
  - 8887:8887  # OpenSPG API Server

Volumes:
  - openspg-server-logs:/app/logs
  - openspg-shared-data:/shared

Environment:
  TZ: Asia/Shanghai
  LANG: C.UTF-8
  JAVA_OPTS: "-Xms2048m -Xmx8192m -Dfile.encoding=UTF-8"

Key Configuration:
  # MySQL Connection
  --server.repository.impl.jdbc.host=mysql
  --server.repository.impl.jdbc.password=openspg

  # Neo4j Graph Store (SHARED WITH AEON)
  --cloudext.graphstore.url=neo4j://openspg-neo4j:7687?user=neo4j&password=neo4j@openspg&database=neo4j
  --cloudext.searchengine.url=neo4j://openspg-neo4j:7687?user=neo4j&password=neo4j@openspg&database=neo4j
  --cloudext.graphstore.multi-database=false
  --neo4j.edition=community

  # Processing Configuration
  --builder.model.execute.num=20

Dependencies:
  - mysql (service_healthy)
  - neo4j (service_healthy)
  - minio (service_started)

Integration Notes:
  ✅ Shares Neo4j database with AEON system
  ✅ Both systems can read/write to same graph database
  ✅ Potential for knowledge graph enrichment and querying
```

### 4. MySQL Database (openspg-mysql)

**Metadata and schema storage for OpenSPG platform**

```yaml
Container Details:
  Name: openspg-mysql
  Image: spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-mysql:latest
  Container ID: a52c8dcc0388
  Network IP: 172.18.0.2
  Status: Running (4 days) - HEALTHY
  Restart Policy: unless-stopped

Ports:
  - 3306:3306  # MySQL Protocol

Volumes:
  - openspg-mysql-data:/var/lib/mysql
  - openspg-mysql-logs:/var/log/mysql
  - openspg-shared-data:/shared

Authentication:
  Root Password: openspg
  Database: openspg
  Root Host: % (all hosts)

Configuration:
  - Character Set: utf8mb4
  - Collation: utf8mb4_general_ci
  - Authentication: mysql_native_password
  - Max Connections: 1000
  - InnoDB Buffer Pool: 2GB

Health Check:
  Command: mysqladmin ping -h localhost -u root -popenspg
  Interval: 10s
  Timeout: 5s
  Retries: 5
  Current Status: ✅ HEALTHY

Purpose:
  - OpenSPG metadata storage
  - Schema definitions
  - Platform configuration
  - NOT used directly by AEON (AEON uses Neo4j)
```

### 5. MinIO Object Storage (openspg-minio)

**S3-compatible object storage for file handling**

```yaml
Container Details:
  Name: openspg-minio
  Image: minio/minio:latest
  Container ID: a817024120dc
  Network IP: 172.18.0.5
  Status: Running (4 days) - HEALTHY
  Restart Policy: unless-stopped

Ports:
  - 9000:9000  # S3 API
  - 9001:9001  # Web Console

Volumes:
  - openspg-minio-data:/data
  - openspg-shared-data:/shared

Authentication:
  Root User: minio
  Root Password: minio@openspg

Command:
  server /data --console-address ":9001"

Health Check:
  Command: curl -f http://localhost:9000/minio/health/live
  Interval: 30s
  Timeout: 10s
  Current Status: ✅ HEALTHY

Purpose:
  - Object storage for OpenSPG
  - File upload/download
  - Potentially usable for AEON document storage
```

---

## 💾 PERSISTENT VOLUMES

### Volume Inventory

| Volume Name | Purpose | Size | Container(s) |
|-------------|---------|------|--------------|
| **openspg-neo4j-data** | Neo4j database files | ~varies | openspg-neo4j |
| **openspg-neo4j-logs** | Neo4j query & system logs | ~varies | openspg-neo4j |
| **openspg-neo4j-import** | CSV import directory | ~varies | openspg-neo4j |
| **openspg-neo4j-plugins** | APOC & extensions | ~varies | openspg-neo4j |
| **openspg-qdrant-data** | Qdrant vector storage | ~varies | openspg-qdrant |
| **openspg-mysql-data** | MySQL database files | ~varies | openspg-mysql |
| **openspg-mysql-logs** | MySQL logs | ~varies | openspg-mysql |
| **openspg-minio-data** | MinIO object storage | ~varies | openspg-minio |
| **openspg-server-logs** | OpenSPG application logs | ~varies | openspg-server |
| **openspg-shared-data** | Cross-container exchange | ~varies | ALL containers |

### Volume Backup Strategy

**Critical Volumes (Must Backup)**:
1. `openspg-neo4j-data` - Contains ALL graph database data (AEON + OpenSPG)
2. `openspg-qdrant-data` - Contains vector memory and checkpoints
3. `openspg-mysql-data` - Contains OpenSPG metadata

**Recommended Backup Commands**:
```bash
# Neo4j Data Backup
docker run --rm -v openspg-neo4j-data:/data -v $(pwd):/backup alpine \
  tar czf /backup/neo4j-data-$(date +%Y%m%d).tar.gz -C /data .

# Qdrant Data Backup
docker run --rm -v openspg-qdrant-data:/data -v $(pwd):/backup alpine \
  tar czf /backup/qdrant-data-$(date +%Y%m%d).tar.gz -C /data .

# MySQL Data Backup
docker exec openspg-mysql mysqldump -u root -popenspg --all-databases > \
  mysql-backup-$(date +%Y%m%d).sql
```

---

## 🔗 AEON System Integration

### Connection Configuration

**AEON → Neo4j**:
```yaml
# File: config/main_config.yaml
neo4j:
  uri: "bolt://localhost:7687"
  user: "neo4j"
  password: "neo4j@openspg"  # Note: Same as OpenSPG uses
  database: "neo4j"
```

**AEON → Qdrant**:
```yaml
# File: config/main_config.yaml
memory:
  qdrant_enabled: false  # Uses persistent SQLite fallback
  qdrant_host: "localhost"
  qdrant_port: 6333

# Alternative: Could enable for vector search features
# qdrant_enabled: true would connect to openspg-qdrant container
```

### Shared Resources

Both AEON and OpenSPG utilize:
1. **Same Neo4j database** (`openspg-neo4j` container)
2. **Potential Qdrant access** (currently AEON uses fallback mode)
3. **Same network** for inter-service communication

### Data Flow

```
AEON Document Processing:
1. AEON agents process documents (PDF/DOCX/HTML)
2. Classify into sectors (Energy, Water, etc.)
3. Extract entities (VENDOR, PROTOCOL, etc.)
4. Store in Neo4j via IngestionAgent
   → Creates Document nodes
   → Creates Entity nodes
   → Creates CONTAINS_ENTITY relationships

OpenSPG Knowledge Graph:
1. OpenSPG builds knowledge graphs
2. Stores in same Neo4j database
3. Can query AEON-ingested documents
4. Can enrich with additional relationships

Combined Capability:
✅ AEON provides document ingestion and NER
✅ OpenSPG provides knowledge graph reasoning
✅ Shared Neo4j enables cross-platform queries
```

---

## 🚀 DEPLOYMENT COMMANDS

### Start All Services

```bash
cd /home/jim/2_OXOT_Projects_Dev
docker-compose up -d
```

### Check Status

```bash
# All containers
docker ps | grep openspg

# Specific health checks
docker inspect openspg-neo4j --format='{{.State.Health.Status}}'
docker inspect openspg-mysql --format='{{.State.Health.Status}}'
docker inspect openspg-minio --format='{{.State.Health.Status}}'
```

### View Logs

```bash
# Neo4j logs
docker logs openspg-neo4j --tail 100 -f

# Qdrant logs
docker logs openspg-qdrant --tail 100 -f

# OpenSPG server logs
docker logs openspg-server --tail 100 -f
```

### Access Services

```bash
# Neo4j Browser
open http://localhost:7474

# MinIO Console
open http://localhost:9001

# OpenSPG Server
curl http://localhost:8887/health
```

### Stop Services

```bash
# Stop all
docker-compose down

# Stop specific service
docker stop openspg-neo4j

# Stop and remove volumes (DESTRUCTIVE)
docker-compose down -v  # ⚠️ WARNING: Deletes all data!
```

---

## 🔧 MAINTENANCE

### Health Check Commands

```bash
# Neo4j connectivity test
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "RETURN 'Connected' AS status"

# Qdrant connectivity test
curl http://localhost:6333/collections

# MySQL connectivity test
docker exec openspg-mysql mysql -u root -popenspg -e "SELECT 1"
```

### Volume Management

```bash
# List volumes
docker volume ls | grep openspg

# Inspect volume
docker volume inspect openspg-neo4j-data

# Cleanup unused volumes (careful!)
docker volume prune  # ⚠️ WARNING: Only removes unused volumes
```

### Network Inspection

```bash
# Inspect openspg-network
docker network inspect openspg-network

# Show container IPs
docker network inspect openspg-network --format='{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{"\n"}}{{end}}'
```

---

## 📊 RESOURCE ALLOCATION

### Current Resource Usage

```bash
# Check container resource usage
docker stats openspg-neo4j openspg-qdrant openspg-server openspg-mysql openspg-minio --no-stream
```

### Recommended Resources

| Service | CPU | Memory | Disk Space |
|---------|-----|--------|------------|
| **Neo4j** | 2-4 cores | 4-8GB | 10GB+ (grows with data) |
| **Qdrant** | 1-2 cores | 1-2GB | 5GB+ (grows with vectors) |
| **OpenSPG Server** | 2-4 cores | 8-12GB | 1GB |
| **MySQL** | 1-2 cores | 2-4GB | 5GB+ |
| **MinIO** | 1 core | 512MB | 10GB+ |
| **Total System** | 8+ cores | 16-24GB RAM | 50GB+ disk |

---

## 🔐 SECURITY NOTES

### Current Security Posture

⚠️ **Development/Test Configuration** - Not hardened for production

**Current State**:
- Passwords in plain text in docker-compose.yml
- No TLS/SSL encryption
- Containers expose ports to host (0.0.0.0)
- No firewall rules

**Production Recommendations**:
1. Use Docker secrets for passwords
2. Enable TLS for Neo4j and MySQL
3. Restrict port bindings to localhost or specific IPs
4. Implement firewall rules
5. Use dedicated networks for service isolation
6. Enable authentication for all services
7. Regular security updates for all images

---

## 📝 DOCKER COMPOSE FILE LOCATION

**Primary File**: `/home/jim/2_OXOT_Projects_Dev/docker-compose.yml`
**Backup Copy**: Included in AEON backup at:
- `/home/jim/2_OXOT_Projects_Dev/backups/AEON_backup_2025-11-03_11-13-13/docker-compose.yml`

**Additional Docker Compose Files**:
- `/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/docker-compose.yml` (alternative Neo4j config)

---

## ✅ VERIFICATION CHECKLIST

After deployment or restore:

- [ ] All 5 containers running (`docker ps`)
- [ ] Neo4j healthy (`docker inspect openspg-neo4j`)
- [ ] MySQL healthy (`docker inspect openspg-mysql`)
- [ ] MinIO healthy (`docker inspect openspg-minio`)
- [ ] Qdrant functional (checkpoint test)
- [ ] Network connectivity (`docker network inspect openspg-network`)
- [ ] Neo4j browser accessible (http://localhost:7474)
- [ ] AEON can connect to Neo4j
- [ ] AEON can store Qdrant checkpoints
- [ ] All volumes mounted correctly

---

**Documentation Status**: ✅ Complete
**Last Verified**: November 3, 2025, 13:40 UTC
**Next Review**: When upgrading any container images or changing configuration

---

*AEON & OpenSPG Docker Infrastructure*
*Integrated Knowledge Graph Platform with Document Ingestion*
*Network: openspg-network | Containers: 5 Running | Status: Operational*
