---
title: Multi-User Concurrent Access Configuration - Part 2 of 2
category: 05_Integration_Guides/04_Multi_User
last_updated: 2025-10-25
line_count: 274
status: published
tags: [multi-user, monitoring, testing, performance, deployment]
part: 2
total_parts: 2
series: MULTI_USER_CONFIGURATION
---

# Multi-User Concurrent Access Configuration - Part 2 of 2

**Series**: Multi-User Configuration Guide
**Navigation**: [Previous Part](./01_Multi_User_Setup.md)

---

### Step 6: Add Application-Level Rate Limiting

**Purpose**: Prevent single user from overwhelming services

**For AgentZero** (if applicable):
```python
from ratelimit import limits, sleep_and_retry

# 30 requests per minute per user
@sleep_and_retry
@limits(calls=30, period=60)
def call_api():
    # Your API call here
    pass
```

**For n8n Workflows**:
Add rate limit nodes to workflows:
```yaml
- type: n8n-nodes-base.wait
  parameters:
    time: 1
    unit: seconds
```

**For Neo4j**:
```cypher
// Add query timeout (5 seconds)
CALL db.queryJmx('org.neo4j:instance=kernel#0,name=Configuration')
YIELD attributes
WITH attributes
CALL db.setProperty('dbms.transaction.timeout', '5s')
```

---

### Step 7: Add Monitoring for Multi-User

**Option A: Basic Monitoring** (Quick)
```bash
# Monitor resource usage
watch -n 5 'docker stats --no-stream'

# Monitor connections
docker exec postgres-shared psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"
docker exec neo4j cypher-shell -u neo4j -p agentzero123 "CALL dbms.listConnections();"
```

**Option B: Prometheus + Grafana** (Recommended)
Add to `docker-compose.yml`:

```yaml
prometheus:
  image: prom/prometheus:latest
  container_name: prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
    - prometheus-data:/prometheus
  networks:
    - agentzero-network

grafana:
  image: grafana/grafana:latest
  container_name: grafana
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
  volumes:
    - grafana-data:/var/lib/grafana
  networks:
    - agentzero-network

cadvisor:
  image: gcr.io/cadvisor/cadvisor:latest
  container_name: cadvisor
  ports:
    - "8081:8080"
  volumes:
    - /:/rootfs:ro
    - /var/run:/var/run:ro
    - /sys:/sys:ro
    - /var/lib/docker/:/var/lib/docker:ro
  networks:
    - agentzero-network
```

**Create `prometheus.yml`**:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```

---

## 📊 Expected Capacity with Configuration

### With Resource Limits Applied

**Estimated Concurrent Users**:
```
Conservative: 5 users
Moderate:     8 users
Optimistic:   10 users
```

**Per-User Resource Estimate**:
```
AgentZero:     300MB per active session
Neo4j:         100MB per active query
PostgreSQL:    50MB per connection
Qdrant:        50MB per search operation
n8n:           30MB per active workflow
```

**Total Per Active User**: ~530MB
**System Capacity**: 7.65GB
**Realistic Concurrent Users**: 8-10 (with 2GB overhead)

---

## 🧪 Testing Multi-User Setup

### Test 1: Concurrent Database Connections

**PostgreSQL**:
```bash
# Open 10 concurrent connections
for i in {1..10}; do
  docker exec postgres-shared psql -U agentzero -d agentzero -c "SELECT pg_sleep(5), 'User $i';" &
done
wait
```

**Neo4j**:
```bash
# Run 10 concurrent queries
for i in {1..10}; do
  docker exec neo4j cypher-shell -u neo4j -p agentzero123 "RETURN 'User $i' as user;" &
done
wait
```

### Test 2: Concurrent n8n Workflows
```bash
# Trigger workflow 10 times concurrently
for i in {1..10}; do
  curl -X POST -H "X-N8N-API-KEY: eyJhbG..." http://localhost:5678/webhook/test &
done
wait
```

### Test 3: Monitor Resource Usage
```bash
# Before concurrent test
docker stats --no-stream

# During concurrent test (in another terminal)
watch -n 1 'docker stats --no-stream'

# After concurrent test
docker stats --no-stream
```

---

## ⚠️ Limitations and Considerations

### Known Limitations
1. **Neo4j Community Edition**: No clustering (single instance only)
2. **Memory Constraints**: 7.65GB total system memory
3. **Single Host**: No distributed architecture
4. **No Load Balancer**: Direct service access

### Scaling Beyond 10 Users

**Option A: Vertical Scaling**
- Increase system RAM (16GB+ recommended)
- Add more CPU cores
- Use SSD storage for better I/O

**Option B: Horizontal Scaling** (Major Change)
- Migrate to Kubernetes
- Use Neo4j Enterprise (clustering)
- Add PostgreSQL read replicas
- Deploy multiple AgentZero instances with load balancer

---

## 🎯 Quick Start Implementation

**Minimal Configuration** (15 minutes):
```bash
cd /Users/jim/Documents/5_AgentZero/container_agentzero

# 1. Add resource limits to docker-compose.yml
# (Copy limits from Step 1 above)

# 2. Restart services
docker-compose down
docker-compose up -d

# 3. Verify resource limits
docker inspect agentzero | grep -A 10 Memory

# 4. Test concurrent access
# (Run Test 1, 2, or 3 from Testing section)

# 5. Monitor during test
docker stats --no-stream
```

**Full Configuration** (2-3 hours):
1. Add resource limits (15 min)
2. Configure PostgreSQL pooling (30 min)
3. Optimize Neo4j settings (15 min)
4. Enable n8n user management (30 min)
5. Deploy monitoring stack (60 min)
6. Run comprehensive tests (30 min)

---

## 📋 Configuration Checklist

```
Multi-User Readiness:
[ ] Resource limits added to all services
[ ] PostgreSQL connection pooling configured
[ ] Neo4j concurrent settings optimized
[ ] n8n user management enabled (optional)
[ ] Monitoring stack deployed (optional)
[ ] Concurrent access tests passed
[ ] Resource usage under 80% during peak load
[ ] All services remain healthy under load
```

---

## 🎉 Conclusion

**Current Status**: ✅ Ready for multi-user with minimal configuration

**Minimum Requirements** (for 5-10 users):
- ✅ Add resource limits (CRITICAL - 15 minutes)
- ⚠️ Test concurrent access (RECOMMENDED - 30 minutes)
- 🟢 Deploy monitoring (OPTIONAL - 60 minutes)

**Recommended Path**:
1. **Today**: Add resource limits and test (45 minutes)
2. **This Week**: Deploy monitoring stack (60 minutes)
3. **Optional**: Enable n8n user management (30 minutes)

**Expected Result**:
- 5-10 concurrent users supported
- Resource usage stays under 80%
- No service degradation under normal load
- Graceful handling of resource constraints

---

**Navigation**: [Previous Part](./01_Multi_User_Setup.md)
**Line Range**: 276-549 of 549 total lines

**Next Step**: Add resource limits to docker-compose.yml from Step 1

**Generated**: 2025-10-17 15:45 UTC
**Last Updated**: 2025-10-25
**Implementation Time**: 15 minutes (minimal) to 3 hours (full)
**Risk Level**: Low (reversible changes)
