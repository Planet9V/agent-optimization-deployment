---
title: Docker Optimization - Part 1 - Configuration Optimization
category: 06_Operational_Guides/01_Docker_Optimization
last_updated: 2025-10-25
line_count: 432
status: published
tags: [docker, optimization, health-checks, memory-limits, security, backups, logging]
part: 1
total_parts: 2
---

# Docker Stack Optimization Recommendations - Part 1: Configuration Optimization

**Navigation:**
- **Current**: Part 1 - Configuration Optimization (Critical & High Priority)
- **Next**: [Part 2 - Performance & Security](02_Performance_Security.md)

---

**Analysis Date**: 2025-10-17
**Stack Version**: 1.0.0
**Services**: 7 (AgentZero, Neo4j, Qdrant, PostgreSQL, n8n, Spacy, Transformers)
**Current Status**: All services functional, 2 health checks failing cosmetically

---

## Executive Summary

The current AgentZero stack is **fully operational** with 7 services consuming ~3.8GB of 7.7GB available memory (50% utilization). All services are communicating correctly despite 2 cosmetic health check issues. This analysis identifies **15 prioritized recommendations** using the ICE framework (Impact × Confidence ÷ Ease).

### Current Resource Usage
```
Service            Memory      CPU      Status
─────────────────────────────────────────────────
agentzero          1.9GB       1.01%    ✅ Healthy
neo4j              779MB       0.48%    ✅ Healthy
spacy-nlp          480MB       0.07%    ⚠️ Unhealthy (functional)
n8n                293MB       0.01%    ✅ Running
qdrant             284MB       0.23%    ⚠️ Unhealthy (functional)
postgres-shared    54MB        0.00%    ✅ Healthy
transformers-nlp   17MB        0.04%    ✅ Running
─────────────────────────────────────────────────
TOTAL              3.8GB       1.84%    85% Functional
```

---

## ICE Prioritized Recommendations

**Formula**: `ICE Score = (Impact × Confidence) / Ease`
**Range**: Higher score = higher priority
**Scoring**: Impact (1-10), Confidence (1-10), Ease (1-5, lower = easier)

### 🔴 CRITICAL (ICE > 20) - Immediate Action

#### 1. Fix Qdrant Health Check ⚠️
**ICE Score: 50** (Impact: 5, Confidence: 10, Ease: 1)

**Problem**: Health check uses `/health` endpoint which doesn't exist (returns 404). Qdrant is fully functional but shows "unhealthy".

**Root Cause**:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:6333/health"]  # ❌ Wrong endpoint
```

Qdrant logs show: `GET /health HTTP/1.1" 404` but root endpoint works: `GET / HTTP/1.1" 200`

**Fix**:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:6333/"]  # ✅ Correct endpoint
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 10s
```

**Impact**: Fixes cosmetic "unhealthy" status, improves monitoring accuracy, no functional change.

**Risk**: None - only changes health check endpoint.

---

#### 2. Fix Spacy Health Check ⚠️
**ICE Score: 45** (Impact: 5, Confidence: 9, Ease: 1)

**Problem**: Health check tests `http://localhost:80/` but nginx may not respond correctly to HEAD requests from curl.

**Current**:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:80/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

**Fix**: Use GET request with output suppression:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "-o", "/dev/null", "-s", "http://localhost:80/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 90s  # Extended startup time
```

**Impact**: Fixes "unhealthy" status for Spacy container.

**Risk**: Minimal - only adjusts health check method.

---

#### 3. Add Memory Limits to All Containers 🛡️
**ICE Score: 40** (Impact: 10, Confidence: 8, Ease: 2)

**Problem**: No memory limits configured. If any service has memory leak, it could consume all system memory and crash host.

**Current State**: No resource limits = unlimited memory consumption possible.

**Recommended Limits** (based on current usage + 50% headroom):
```yaml
agentzero:
  deploy:
    resources:
      limits:
        memory: 3G        # Current: 1.9GB
        cpus: '2.0'
      reservations:
        memory: 1.5G

neo4j:
  deploy:
    resources:
      limits:
        memory: 2.5G      # Current: 779MB, needs room for caching
        cpus: '1.5'
      reservations:
        memory: 512M

spacy-nlp:
  deploy:
    resources:
      limits:
        memory: 1G        # Current: 480MB, NLP models need room
        cpus: '1.0'
      reservations:
        memory: 256M

n8n:
  deploy:
    resources:
      limits:
        memory: 512M      # Current: 293MB
        cpus: '0.5'
      reservations:
        memory: 128M

qdrant:
  deploy:
    resources:
      limits:
        memory: 1G        # Current: 284MB, vectors need room
        cpus: '1.0'
      reservations:
        memory: 128M

postgres-shared:
  deploy:
    resources:
      limits:
        memory: 512M      # Current: 54MB, 3 databases
        cpus: '0.5'
      reservations:
        memory: 64M

transformers-nlp:
  deploy:
    resources:
      limits:
        memory: 2G        # Current: 17MB, but model loading needs room
        cpus: '1.0'
      reservations:
        memory: 128M
```

**Total Limits**: 10.5GB (current system: 7.7GB available)
**Note**: These are LIMITS (maximum), not guaranteed allocations. Docker will share unused memory.

**Impact**: Prevents OOM crashes, ensures fair resource distribution, protects host system.

**Risk**: Low - limits are generous with headroom. Monitor first week for adjustments.

---

#### 4. Add Health Checks for n8n and Transformers 📊
**ICE Score: 35** (Impact: 7, Confidence: 10, Ease: 2)

**Problem**: n8n and transformers-nlp have no health checks, making orchestration unreliable.

**Current**: No health checks = no dependency validation = potential race conditions.

**Add to n8n**:
```yaml
n8n:
  healthcheck:
    test: ["CMD", "wget", "--spider", "-q", "http://localhost:5678/healthz"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 60s
```

**Add to transformers-nlp**:
```yaml
transformers-nlp:
  healthcheck:
    test: ["CMD", "python3", "-c", "import http.client; c=http.client.HTTPConnection('localhost:8000'); c.request('GET', '/'); r=c.getresponse(); exit(0 if r.status==200 else 1)"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 60s
```

**Impact**: Enables proper service orchestration, catches startup failures early.

**Risk**: Minimal - only adds monitoring, no functional changes.

---

### 🟡 HIGH PRIORITY (ICE 10-20) - Schedule This Week

#### 5. Change Default Passwords for Production 🔐
**ICE Score: 18** (Impact: 9, Confidence: 10, Ease: 5)

**Problem**: Development passwords are documented everywhere and easily discovered.

**Current Passwords**:
- Neo4j: `agentzero123`
- PostgreSQL admin: `agentzero123`
- n8n: `Jimmy123$`
- All passwords in /shared volume accessible by all containers

**Recommendation**:
1. Generate strong passwords: `openssl rand -base64 32`
2. Store in secure secret management (HashiCorp Vault, AWS Secrets Manager)
3. Use Docker secrets for production: https://docs.docker.com/engine/swarm/secrets/
4. Remove /shared/CREDENTIALS_AND_KEYS.env in production
5. Update MASTER_INDEX.md with secret references instead of actual values

**Example with Docker Secrets**:
```yaml
secrets:
  neo4j_password:
    file: ./secrets/neo4j_password.txt
  postgres_password:
    file: ./secrets/postgres_password.txt

neo4j:
  secrets:
    - neo4j_password
  environment:
    - NEO4J_AUTH=neo4j/run/secrets/neo4j_password
```

**Impact**: Prevents unauthorized access, meets security compliance requirements.

**Risk**: High implementation effort, requires secret management infrastructure.

**Action**: Schedule for production deployment, keep current for development.

---

#### 6. Add Backup Strategy for Persistent Volumes 💾
**ICE Score: 16** (Impact: 10, Confidence: 8, Ease: 5)

**Problem**: No backup strategy = data loss risk. 12 persistent volumes with no recovery plan.

**Current Volumes**:
```
agentzero-data (agent state)
agentzero-knowledge (knowledge base)
agentzero-memory (conversation memory)
neo4j-data (graph database) ← CRITICAL
qdrant-data (vector embeddings) ← CRITICAL
postgres-shared-data (3 databases) ← CRITICAL
n8n-data (workflows) ← CRITICAL
```

**Recommended Strategy**:

**Option A - Volume Backups** (Easier):
```bash
#!/bin/bash
# Backup script: /scripts/backup-volumes.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/$DATE"

# Stop services for consistent backup
docker-compose stop

# Backup critical volumes
docker run --rm -v neo4j-data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/neo4j-data.tar.gz /data
docker run --rm -v qdrant-data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/qdrant-data.tar.gz /data
docker run --rm -v postgres-shared-data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/postgres-data.tar.gz /data
docker run --rm -v n8n-data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/n8n-data.tar.gz /data

# Restart services
docker-compose start

# Retention: keep last 7 days
find /backups -type d -mtime +7 -exec rm -rf {} \;
```

**Option B - Application-Level Backups** (Better):
```bash
#!/bin/bash
# Application-aware backups
DATE=$(date +%Y%m%d_%H%M%S)

# Neo4j backup (online)
docker exec neo4j neo4j-admin backup --backup-dir=/var/lib/neo4j/backups/$DATE

# PostgreSQL backup (online)
docker exec postgres-shared pg_dumpall -U postgres > /backups/postgres_$DATE.sql

# Qdrant backup (via API)
curl -X POST http://localhost:6333/collections/snapshot -o /backups/qdrant_$DATE.snapshot

# n8n backup (database + files)
docker exec postgres-shared pg_dump -U n8n n8n > /backups/n8n_$DATE.sql
docker run --rm -v n8n-data:/data -v /backups:/backup alpine tar czf /backup/n8n-files_$DATE.tar.gz /data
```

**Schedule**: Daily at 2 AM via cron:
```cron
0 2 * * * /scripts/backup-volumes.sh >> /var/log/backups.log 2>&1
```

**Impact**: Protects against data loss, enables disaster recovery.

**Risk**: Requires storage space, adds operational complexity.

---

#### 7. Implement Logging Strategy with Rotation 📝
**ICE Score: 15** (Impact: 6, Confidence: 10, Ease: 4)

**Problem**: No log rotation = logs can fill disk. No centralized logging = debugging difficulty.

**Current**: Docker default JSON logs (unlimited size).

**Recommended Configuration**:
```yaml
# Add to each service in docker-compose.yml
logging:
  driver: "json-file"
  options:
    max-size: "10m"      # Maximum 10MB per log file
    max-file: "3"        # Keep 3 rotated files (30MB total per container)
    compress: "true"     # Compress rotated files
```

**Total Log Space**: 7 containers × 30MB = 210MB maximum.

**Optional - Centralized Logging**:
```yaml
# Add Loki + Grafana for log aggregation
loki:
  image: grafana/loki:latest
  ports:
    - "3100:3100"
  volumes:
    - loki-data:/loki

grafana:
  image: grafana/grafana:latest
  ports:
    - "3000:3000"
  volumes:
    - grafana-data:/var/lib/grafana
```

Update all services:
```yaml
logging:
  driver: "loki"
  options:
    loki-url: "http://loki:3100/loki/api/v1/push"
```

**Impact**: Prevents disk full issues, improves debugging capabilities.

**Risk**: Minimal - rotation is standard practice.

---

#### 8. Add Startup Probes for Slow Services 🕐
**ICE Score: 14** (Impact: 7, Confidence: 10, Ease: 5)

**Problem**: AgentZero and Neo4j take 40+ seconds to start. Current health checks may fail during startup.

**Current**:
- AgentZero: `start_period: 40s`
- Neo4j: `start_period: 40s`
- Health checks start immediately, may mark as "failed" during initialization

**Solution - Add Startup Probes**:
```yaml
agentzero:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:80"]
    interval: 10s
    timeout: 10s
    retries: 3
    start_period: 90s    # Increased from 40s
  # New: Startup probe (checks less frequently during startup)
  # Note: Docker Compose doesn't support startup probes yet (Kubernetes feature)
  # Workaround: Increase start_period and use external health check

neo4j:
  healthcheck:
    test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "agentzero123", "RETURN 1"]
    interval: 10s
    timeout: 10s
    retries: 5
    start_period: 90s    # Increased from 40s
```

**Alternative - Wait Script**:
```yaml
agentzero:
  depends_on:
    neo4j:
      condition: service_healthy
    qdrant:
      condition: service_healthy
  entrypoint: ["/wait-for-services.sh"]  # Custom script to verify connections
  command: ["python", "main.py"]
```

**Impact**: Reduces false startup failures, improves reliability.

**Risk**: Slightly longer startup time, but more reliable.

---

**Navigation:**
- **Current**: Part 1 - Configuration Optimization (Critical & High Priority)
- **Next**: [Part 2 - Performance & Security](02_Performance_Security.md)

---
**Document Version:** 1.0 (Part 1 of 2)
**Last Updated:** 2025-10-25
**Lines:** 432 / 500 limit
