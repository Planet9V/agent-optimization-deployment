---
title: Multi-User Concurrent Access Configuration - Part 1 of 2
category: 05_Integration_Guides/04_Multi_User
last_updated: 2025-10-25
line_count: 275
status: published
tags: [multi-user, configuration, docker, resources, postgresql, neo4j]
part: 1
total_parts: 2
series: MULTI_USER_CONFIGURATION
---

# Multi-User Concurrent Access Configuration - Part 1 of 2

**Series**: Multi-User Configuration Guide
**Navigation**: [Next Part](./02_Multi_User_Advanced.md)

---

**Purpose**: Enable multiple users to access AgentZero stack simultaneously
**Current Status**: Single-user configuration
**Target**: 5-10 concurrent users
**Date**: 2025-10-17

---

## 📊 Current Configuration Analysis

### Resource Availability
```
Current Usage:  3.14GB / 7.65GB (41%)
Available:      4.51GB free
CPU Usage:      1.30% (very low)
```

**Capacity Assessment**:
- ✅ Memory: Sufficient for 5-10 users with current usage
- ✅ CPU: Minimal usage, plenty of headroom
- ⚠️ No resource limits: Risk of runaway processes

---

## 🚀 Multi-User Readiness Checklist

### ✅ Already Configured
- [x] Shared PostgreSQL database (supports concurrent connections)
- [x] Neo4j community edition (supports multiple concurrent sessions)
- [x] Qdrant vector database (thread-safe, concurrent operations)
- [x] n8n workflow automation (supports multiple users via API)
- [x] Docker network (all services can communicate)
- [x] Persistent volumes (data shared across services)

### ⚠️ Needs Configuration
- [ ] Resource limits (prevent one user from consuming all resources)
- [ ] Connection pooling (optimize database connections)
- [ ] Rate limiting (prevent API abuse)
- [ ] Monitoring (track per-user resource usage)
- [ ] User session management (optional)

---

## 🔧 Implementation Steps

### Step 1: Add Resource Limits (CRITICAL)

**Purpose**: Prevent single user/process from consuming all resources

**Edit `docker-compose.yml`** and add resource limits to each service:

```yaml
agentzero:
  deploy:
    resources:
      limits:
        memory: 3G        # Max 3GB per container
        cpus: '2.0'       # Max 2 CPU cores
      reservations:
        memory: 1.5G      # Guaranteed 1.5GB
        cpus: '1.0'       # Guaranteed 1 core

neo4j:
  deploy:
    resources:
      limits:
        memory: 2.5G
        cpus: '1.5'
      reservations:
        memory: 512M
        cpus: '0.5'

qdrant:
  deploy:
    resources:
      limits:
        memory: 1G
        cpus: '1.0'
      reservations:
        memory: 256M
        cpus: '0.25'

postgres-shared:
  deploy:
    resources:
      limits:
        memory: 1G
        cpus: '1.0'
      reservations:
        memory: 256M
        cpus: '0.25'

n8n:
  deploy:
    resources:
      limits:
        memory: 512M
        cpus: '0.5'
      reservations:
        memory: 128M
        cpus: '0.25'

spacy-nlp:
  deploy:
    resources:
      limits:
        memory: 1G
        cpus: '1.0'
      reservations:
        memory: 256M
        cpus: '0.25'

transformers-nlp:
  deploy:
    resources:
      limits:
        memory: 2G
        cpus: '1.0'
      reservations:
        memory: 256M
        cpus: '0.25'
```

**Total Limits**: 11GB (current system has 7.65GB available)
**Note**: These are CAPS, not allocations. Docker shares unused memory between containers.

**Apply Changes**:
```bash
cd /Users/jim/Documents/5_AgentZero/container_agentzero
docker-compose up -d
```

---

### Step 2: Configure PostgreSQL Connection Pooling

**Purpose**: Optimize database connections for multiple concurrent users

**Current PostgreSQL Config**: Default (100 max connections)

**Recommended Settings**:
Edit `docker-compose.yml` PostgreSQL environment:

```yaml
postgres-shared:
  environment:
    # Existing config...
    - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-agentzero123}

    # Add connection pooling settings
    - POSTGRES_MAX_CONNECTIONS=200        # Increased from 100
    - POSTGRES_SHARED_BUFFERS=256MB       # Memory for caching
    - POSTGRES_EFFECTIVE_CACHE_SIZE=1GB   # OS cache estimate
    - POSTGRES_WORK_MEM=16MB              # Per-operation memory
```

**Alternative**: Use PgBouncer connection pooler:
```yaml
pgbouncer:
  image: pgbouncer/pgbouncer:latest
  container_name: pgbouncer
  ports:
    - "6432:6432"
  environment:
    - DATABASES_HOST=postgres-shared
    - DATABASES_PORT=5432
    - DATABASES_USER=postgres
    - DATABASES_PASSWORD=agentzero123
    - POOL_MODE=transaction
    - MAX_CLIENT_CONN=500
    - DEFAULT_POOL_SIZE=25
  networks:
    - agentzero-network
```

---

### Step 3: Configure Neo4j for Concurrent Sessions

**Current Neo4j Config**: Default settings

**Recommended Multi-User Settings**:
Edit `docker-compose.yml` Neo4j environment:

```yaml
neo4j:
  environment:
    # Existing memory config...
    - NEO4J_dbms_memory_pagecache_size=1G
    - NEO4J_dbms_memory_heap_initial__size=768M
    - NEO4J_dbms_memory_heap_max__size=1536M

    # Add concurrency settings
    - NEO4J_dbms_connector_bolt_thread__pool__min__size=5
    - NEO4J_dbms_connector_bolt_thread__pool__max__size=400
    - NEO4J_dbms_threads_worker__count=8
    - NEO4J_dbms_transaction_concurrent_maximum=1000
```

**Connection Pool in Application**:
```python
from neo4j import GraphDatabase

# Configure connection pool
driver = GraphDatabase.driver(
    "bolt://neo4j:7687",
    auth=("neo4j", "agentzero123"),
    max_connection_pool_size=50,    # Max connections in pool
    connection_acquisition_timeout=60,  # 60 sec timeout
    max_transaction_retry_time=30   # Retry failed transactions
)
```

---

### Step 4: Configure Qdrant for Concurrent Access

**Current Status**: Already thread-safe and concurrent-ready

**Optimization** (Optional):
Edit `docker-compose.yml` Qdrant environment:

```yaml
qdrant:
  environment:
    - QDRANT__SERVICE__GRPC_PORT=6334
    - QDRANT__SERVICE__HTTP_PORT=6333

    # Add performance tuning
    - QDRANT__SERVICE__MAX_REQUEST_SIZE_MB=32
    - QDRANT__STORAGE__PERFORMANCE__MAX_SEARCH_THREADS=0  # Auto-detect
    - QDRANT__STORAGE__OPTIMIZERS__DEFAULT_SEGMENT_NUMBER=4
```

**No additional configuration needed** - Qdrant is designed for concurrent access.

---

### Step 5: Configure n8n for Multi-User

**Option A: Single Shared User** (Current - Simple)
```yaml
n8n:
  environment:
    - N8N_BASIC_AUTH_ACTIVE=true
    - N8N_BASIC_AUTH_USER=jims67mustang
    - N8N_BASIC_AUTH_PASSWORD=Jimmy123$
```
**Pros**: Simple, already configured
**Cons**: No user-specific workflows, shared credentials

**Option B: Enable User Management** (Recommended)
```yaml
n8n:
  environment:
    # Remove basic auth
    # - N8N_BASIC_AUTH_ACTIVE=false

    # Enable user management
    - N8N_USER_MANAGEMENT_DISABLED=false
    - N8N_PUBLIC_API_DISABLED=false
```

**Then create users via UI**:
1. First user becomes admin
2. Admin can invite additional users
3. Each user has separate workspace

**Option C: API Key Per User**
Generate separate API keys for each user via n8n UI:
```bash
Settings → API → Create API Key → Copy key
```

---

**Navigation**: [Next Part](./02_Multi_User_Advanced.md)
**Line Range**: 1-275 of 549 total lines
