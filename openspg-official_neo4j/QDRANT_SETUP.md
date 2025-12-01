# QDRANT VECTOR DATABASE INTEGRATION
**File:** QDRANT_SETUP.md
**Created:** 2025-10-31
**Version:** v1.0.0
**Purpose:** Production deployment guide for Qdrant integration with OpenSPG
**Status:** ACTIVE

---

## Executive Summary

Qdrant vector database is deployed as a **separate Docker Compose service** that integrates seamlessly with the OpenSPG cybersecurity platform. This architecture provides:

✅ **Zero risk to OpenSPG production** (separate compose file)
✅ **Cross-container accessibility** (shared network)
✅ **Persistent storage** (dedicated volume)
✅ **Data exchange** (shared volume)
✅ **Disaster recovery** (host-mounted backups)
✅ **API key authentication** (secure)
✅ **Resource limits** (prevents contention)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│ docker-compose.yml (EXISTING - UNTOUCHED)           │
│ ├─ openspg-server     (port 8887)                   │
│ ├─ openspg-mysql      (port 3306)                   │
│ ├─ openspg-neo4j      (ports 7474, 7687)            │
│ └─ openspg-minio      (ports 9000, 9001)            │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ openspg-network (bridge)
                   │
┌──────────────────┴──────────────────────────────────┐
│ docker-compose.qdrant.yml (NEW - SEPARATE)          │
│ └─ openspg-qdrant     (ports 6333, 6334)            │
│    ├─ Volume: openspg-qdrant-data (persistent)      │
│    ├─ Volume: openspg-shared-data (exchange)        │
│    └─ Volume: $HOME/qdrant-backups (host backup)    │
└─────────────────────────────────────────────────────┘
```

### Network Configuration
- **Network:** `openspg-network` (external, shared with OpenSPG)
- **DNS Name:** `openspg-qdrant`
- **Accessible From:**
  - Host: `localhost:6333`
  - OpenSPG containers: `openspg-qdrant:6333`
  - Other Docker containers: Join `openspg-network`

### Volume Strategy

| Volume | Purpose | Location | Persistence |
|--------|---------|----------|-------------|
| `openspg-qdrant-data` | Qdrant internal database | `/qdrant/storage` | **CRITICAL** - dedicated persistent |
| `openspg-shared-data` | Data exchange | `/shared` | Shared with OpenSPG |
| `$HOME/qdrant-backups` | Disaster recovery | `/qdrant/backups` | Host-mounted |

---

## Quick Start

### Prerequisites
- OpenSPG deployment running (`docker-compose ps` shows 4 services)
- Docker Compose 1.27+ installed
- 16GB+ RAM available (24GB recommended)

### Installation (5 minutes)

```bash
# Navigate to OpenSPG directory
cd /home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j

# Run automated startup script
./start-qdrant.sh
```

**Expected Output:**
```
✓ Docker installed
✓ OpenSPG network exists
✓ Shared volume exists
✓ Configuration file exists
✓ Backup directory exists
✓ No conflicting containers

Starting Qdrant Vector Database...
✓ Qdrant is healthy!
✓ Host → Qdrant: SUCCESS
✓ DNS resolution: openspg-qdrant is reachable

Qdrant Deployment Successful!
```

### Manual Deployment (Alternative)

```bash
# 1. Start Qdrant
docker-compose -f docker-compose.qdrant.yml up -d

# 2. Wait for health check (30 seconds)
docker-compose -f docker-compose.qdrant.yml ps

# 3. Verify connectivity
source .env.qdrant
curl -H "api-key: $QDRANT_API_KEY" http://localhost:6333/health
```

---

## Usage Guide

### Daily Operations

```bash
# Check Qdrant status
docker-compose -f docker-compose.qdrant.yml ps

# View logs (live)
docker-compose -f docker-compose.qdrant.yml logs -f

# View last 100 lines
docker-compose -f docker-compose.qdrant.yml logs --tail=100

# Restart Qdrant (zero impact on OpenSPG)
docker-compose -f docker-compose.qdrant.yml restart

# Stop Qdrant
docker-compose -f docker-compose.qdrant.yml down

# Update Qdrant image
docker-compose -f docker-compose.qdrant.yml pull
docker-compose -f docker-compose.qdrant.yml up -d
```

### Resource Monitoring

```bash
# Monitor resource usage
docker stats openspg-qdrant

# Check volume size
docker system df -v | grep qdrant

# Verify memory limits
docker inspect openspg-qdrant --format='{{.HostConfig.Memory}}'
```

---

## Integration Examples

### Python Client (From OpenSPG Server Container)

```python
from qdrant_client import QdrantClient
import os

# Connect using container DNS name
client = QdrantClient(
    url="http://openspg-qdrant:6333",
    api_key=os.getenv("QDRANT_API_KEY")
)

# Verify connection
print(client.get_collections())
```

### Python Client (From Host)

```python
from qdrant_client import QdrantClient

# Connect to localhost
client = QdrantClient(
    url="http://localhost:6333",
    api_key="deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ="
)

# Create collection
from qdrant_client.models import Distance, VectorParams

client.create_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)
```

### cURL Examples

```bash
# Source API key
source .env.qdrant

# Health check
curl -H "api-key: $QDRANT_API_KEY" http://localhost:6333/health

# List collections
curl -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections

# Get collection info
curl -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections/schema_knowledge

# Web UI (no auth needed for local access)
open http://localhost:6333/dashboard
```

---

## Backup & Disaster Recovery

### Automated Daily Snapshots (Recommended)

Create cron job:
```bash
# Edit crontab
crontab -e

# Add daily snapshot at 2 AM
0 2 * * * docker exec openspg-qdrant curl -X POST http://localhost:6333/snapshots/create > /dev/null 2>&1
```

### Manual Snapshot

```bash
# Create snapshot
docker exec openspg-qdrant curl -X POST http://localhost:6333/snapshots/create

# List snapshots
docker exec openspg-qdrant ls -lh /qdrant/storage/snapshots/

# Copy snapshot to host backup
docker cp openspg-qdrant:/qdrant/storage/snapshots/ $HOME/qdrant-backups/snapshots/
```

### Restore from Snapshot

```bash
# 1. Stop Qdrant
docker-compose -f docker-compose.qdrant.yml down

# 2. Clear data volume (CAREFUL!)
docker volume rm openspg-qdrant-data

# 3. Recreate volume
docker volume create openspg-qdrant-data

# 4. Start Qdrant
docker-compose -f docker-compose.qdrant.yml up -d

# 5. Copy snapshot to container
docker cp $HOME/qdrant-backups/snapshots/latest.snapshot openspg-qdrant:/qdrant/storage/snapshots/

# 6. Restore snapshot
docker exec openspg-qdrant curl -X PUT http://localhost:6333/collections/schema_knowledge/snapshots/restore
```

### Export Collections (Alternative Backup)

```bash
# Export collection to shared volume
docker exec openspg-qdrant curl -X POST \
  -H "api-key: $QDRANT_API_KEY" \
  http://localhost:6333/collections/schema_knowledge/snapshots/upload

# Backup shared volume
tar -czf qdrant-export-$(date +%Y%m%d).tar.gz \
  /var/lib/docker/volumes/openspg-shared-data/_data/qdrant-exports/
```

---

## Troubleshooting

### Issue: Container Won't Start

**Symptoms:**
```bash
docker-compose -f docker-compose.qdrant.yml ps
# Shows: Restarting or Exited
```

**Diagnosis:**
```bash
# Check logs
docker-compose -f docker-compose.qdrant.yml logs

# Common causes:
# 1. Port conflict (6333 already in use)
# 2. Volume permission issues
# 3. Memory limits too low
```

**Solutions:**
```bash
# Fix port conflict
docker ps -a | grep 6333  # Find conflicting container
docker stop <container-name>

# Fix volume permissions
docker volume rm openspg-qdrant-data
docker volume create openspg-qdrant-data

# Increase memory limits (edit .env.qdrant)
QDRANT_MEMORY_LIMIT=6G
QDRANT_MEMORY_RESERVATION=4G
```

---

### Issue: OpenSPG Can't Connect to Qdrant

**Symptoms:**
```python
# From openspg-server:
QdrantException: Connection refused
```

**Diagnosis:**
```bash
# Verify network connectivity
docker exec openspg-server ping -c 3 openspg-qdrant

# Check if both on same network
docker network inspect openspg-network --format '{{range .Containers}}{{.Name}} {{end}}'
```

**Solutions:**
```bash
# Restart Qdrant
docker-compose -f docker-compose.qdrant.yml restart

# Check firewall
sudo ufw status

# Verify API key
source .env.qdrant && echo $QDRANT_API_KEY
```

---

### Issue: Health Check Failing

**Symptoms:**
```bash
docker inspect openspg-qdrant --format='{{.State.Health.Status}}'
# Shows: unhealthy
```

**Diagnosis:**
```bash
# Check health check logs
docker inspect openspg-qdrant --format='{{json .State.Health}}' | jq

# Manual health check
docker exec openspg-qdrant curl http://localhost:6333/health
```

**Solutions:**
```bash
# Increase start_period in docker-compose.qdrant.yml
healthcheck:
  start_period: 60s  # Increase from 30s

# Restart
docker-compose -f docker-compose.qdrant.yml restart
```

---

### Issue: Performance Degradation

**Symptoms:**
- Slow query response times (>2 seconds)
- High CPU usage (>80%)
- High memory usage (approaching limit)

**Diagnosis:**
```bash
# Check resource usage
docker stats openspg-qdrant

# Check collection sizes
curl -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections | jq
```

**Solutions:**
```bash
# Increase resource limits (.env.qdrant)
QDRANT_MEMORY_LIMIT=8G
QDRANT_CPU_LIMIT=4.0

# Optimize indices
docker exec openspg-qdrant curl -X POST \
  -H "api-key: $QDRANT_API_KEY" \
  http://localhost:6333/collections/schema_knowledge/optimize

# Restart to apply changes
docker-compose -f docker-compose.qdrant.yml up -d --force-recreate
```

---

## Security Best Practices

### API Key Management

```bash
# NEVER commit .env.qdrant to git
echo ".env.qdrant" >> .gitignore

# Rotate API key every 90 days
openssl rand -base64 32 > .env.qdrant.new
# Update docker-compose
docker-compose -f docker-compose.qdrant.yml up -d
```

### Network Isolation (Advanced)

```yaml
# Create internal network for backend services
networks:
  openspg-backend:
    driver: bridge
    internal: true  # No external access

  openspg-frontend:
    driver: bridge

# Qdrant only on backend network
qdrant:
  networks:
    - openspg-backend
```

---

## Performance Tuning

### Recommended Settings for 12-Wave Implementation

**For 267K CVE vectors + documentation:**

```bash
# .env.qdrant
QDRANT_MEMORY_LIMIT=6G
QDRANT_MEMORY_RESERVATION=4G
QDRANT_CPU_LIMIT=4.0
QDRANT_CPU_RESERVATION=2.0

# HNSW index parameters (balance speed vs accuracy)
QDRANT_COLLECTION_DEFAULT_HNSW_EF_CONSTRUCT=100
QDRANT_COLLECTION_DEFAULT_HNSW_M=16
```

**Expected Performance:**
- Semantic search: 50-200ms
- Hybrid search (vector + filter): 100-500ms
- Collection creation: 1-5 seconds
- 267K vector indexing: 10-30 minutes (one-time)

---

## Integration with Option B (12-Wave Implementation)

### Phase 1: Schema Knowledge Retrieval
**Status:** Ready for execution

**Collections:**
- `schema_knowledge` (400 chunks from 34 markdown files)
- `query_patterns` (Cypher query examples)

**Benefits:** 60x faster agent documentation lookup

### Phase 2: Agent Coordination
**Status:** Ready after Phase 1

**Collections:**
- `agent_shared_memory` (cross-agent findings)

**Benefits:** 3x swarm coordination efficiency

### Phase 3: Decision Tracking
**Status:** Ready after Phase 2

**Collections:**
- `implementation_decisions` (architectural decisions)

**Benefits:** 50% faster implementation through pattern reuse

---

## Monitoring & Metrics

### Key Metrics to Track

```bash
# Collection sizes
curl -s -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections | \
  jq '.result.collections[] | {name: .name, vectors: .vectors_count}'

# Memory usage
docker stats openspg-qdrant --no-stream --format \
  "table {{.Container}}\t{{.MemUsage}}\t{{.MemPerc}}"

# Query latency (from logs)
docker-compose -f docker-compose.qdrant.yml logs | grep "search_duration"
```

### Success Criteria
- [ ] Uptime: >99.5%
- [ ] Query latency p95: <500ms
- [ ] Memory usage: <4GB (under limit)
- [ ] CPU usage: <50% average
- [ ] No OOM errors in logs

---

## FAQ

**Q: Will Qdrant impact OpenSPG performance?**
A: No. Resource limits (2-4GB RAM, 1-2 CPUs) ensure Qdrant doesn't compete with OpenSPG services (Neo4j uses 6GB).

**Q: What happens if Qdrant crashes?**
A: OpenSPG continues operating normally. Qdrant is optional for current operations and critical for 12-wave implementation.

**Q: How much disk space does Qdrant need?**
A: ~2-3GB for 267K CVE vectors + indices. Grows ~100MB/month with agent memory.

**Q: Can I access Qdrant from other Docker containers?**
A: Yes. Add your container to `openspg-network` and use DNS name `openspg-qdrant:6333`.

**Q: How do I update Qdrant to a newer version?**
A: `docker-compose -f docker-compose.qdrant.yml pull && docker-compose -f docker-compose.qdrant.yml up -d`

---

## References

- **Qdrant Integration Plan:** `QDRANT_INTEGRATION_PLAN.md` (148KB, comprehensive research)
- **12-Wave Implementation:** `01_VERSION_2_ENHANCEMENT_MASTER_PLAN.md`
- **Qdrant Documentation:** https://qdrant.tech/documentation/
- **Docker Compose Reference:** https://docs.docker.com/compose/

---

**Document Status:** COMPLETE
**Last Updated:** 2025-10-31
**Maintained By:** AEON Digital Twin Cybersecurity Team
**Review Schedule:** Monthly
