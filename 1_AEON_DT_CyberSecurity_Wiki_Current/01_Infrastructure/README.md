# AEON Cyber Digital Twin - Infrastructure Documentation

**Last Updated**: 2025-12-01 21:00 UTC
**Directory Status**: CURRENT - Record of Note for all AEON Infrastructure

This directory contains operational infrastructure documentation for deployed AEON platform enhancements.

---

## Infrastructure Documents

### E27: Psychohistory Framework Infrastructure ✅ DEPLOYED
**File**: `E27_INFRASTRUCTURE.md` (1,521 lines, v1.0.0)

**Deployment Date**: 2025-11-28
**Status**: OPERATIONAL

**Infrastructure Components**:
- Neo4j 5.26 Cluster (3 core + 2 read replicas recommended)
- 16 Super Labels (consolidated from 24)
- 5 Psychohistory APOC Functions (R₀, Ising, Granovetter, Bifurcation, Crisis Velocity)
- 3 Seldon Crisis Detection Frameworks (SC001, SC002, SC003)
- Performance monitoring (Prometheus + Grafana)
- Backup strategy (6-hour full, 15-min incremental)

**Key Sections**:
1. Infrastructure Overview
2. Neo4j Configuration (APOC, memory, network)
3. Deployment Architecture (dev/staging/production)
4. Scaling Strategy (horizontal/vertical)
5. Performance Requirements (query SLAs)
6. Monitoring & Observability (metrics, alerting)
7. Backup & Recovery (APOC export, restore procedures)
8. Security Hardening (auth, encryption, firewall)
9. Operational Procedures (deployment, rollback)
10. Resource Requirements (compute, storage, network)
11. Cost Analysis (AWS deployment example: $1,732/month)
12. Disaster Recovery (failure scenarios, playbooks)

**Current Production Metrics**:
- Query Response Time (indexed lookup): 18ms avg (target: <25ms) ✅
- Psychohistory Function Execution: 73ms avg (target: <100ms) ✅
- Seldon Crisis Query: 2,247ms avg (target: <3000ms) ✅
- Custom Function Availability: 100% (5/5 operational) ✅

---

### E30: NER11 Gold Hierarchical Integration Infrastructure ✅ 71% OPERATIONAL
**File**: `E30_NER11_INFRASTRUCTURE.md` (365 lines, v1.0.0)

**Deployment Date**: 2025-12-01
**Status**: OPERATIONAL (Phases 1-3 Complete)

**Infrastructure Components**:
- NER11 Gold Standard API v3.0.0 (FastAPI + spaCy)
- Hierarchical Entity Processor (60 labels → 566 fine-grained types)
- Qdrant Vector Database (384-dim, COSINE distance, 670+ entities)
- Neo4j Knowledge Graph Integration (1.1M+ nodes preserved)
- Hybrid Search Engine (semantic + graph with re-ranking)

**Key Sections**:
1. Infrastructure Overview
2. Component Architecture (service matrix, dependencies)
3. Network Configuration (aeon-net, port mappings)
4. Service Dependencies (startup order, health checks)
5. Performance Requirements (response time SLAs, throughput)
6. Monitoring & Health Checks (metrics, alerting)
7. Backup & Recovery (Qdrant snapshots, Neo4j export)
8. Operational Procedures (deployment, updates, scaling)
9. Troubleshooting (common issues, log locations)

**Current Production Metrics**:
- Semantic Search Latency (p95): 142ms (target: <150ms) ✅
- Hybrid Search Latency (p95): 487ms (target: <500ms) ✅
- Graph Expansion (2-hop, p95): 293ms (target: <300ms) ✅
- Re-ranking (10 results): 12ms (target: <50ms) ✅
- Neo4j Node Preservation: 1,104,066 nodes (target: ≥1,104,066) ✅

**Service URLs**:
```bash
# NER11 Gold API
http://localhost:8000                    # Base URL
http://localhost:8000/docs               # Swagger UI
http://localhost:8000/search/semantic    # Semantic search
http://localhost:8000/search/hybrid      # Hybrid search (NEW)

# Qdrant
http://localhost:6333                    # HTTP API
http://localhost:6333/collections        # Collection management

# Neo4j
bolt://localhost:7687                    # Bolt protocol
http://localhost:7474                    # HTTP browser
```

---

### Supporting Infrastructure Documents

#### Docker Architecture
**File**: `Docker-Architecture.md`

**Purpose**: Docker container architecture and orchestration

#### Network Topology
**File**: `Network-Topology.md`

**Purpose**: Network architecture and connectivity

#### Clerk Quick Start
**File**: `Clerk_Quick_Start.md`

**Purpose**: Clerk authentication integration (if applicable)

---

## Infrastructure Integration Matrix

### Enhancement Dependencies

```
E27 (Psychohistory) ───┐
                       ├──→ Neo4j 5.26 (Shared)
E30 (NER11 Search) ────┘

E30 Components:
  ├─ NER11 API ──→ Standalone service
  ├─ Qdrant ──→ Standalone vector DB
  └─ Neo4j ──→ Shared with E27 (hierarchical properties added)
```

### Shared vs Dedicated Resources

| Resource | E27 Usage | E30 Usage | Shared? |
|----------|-----------|-----------|---------|
| **Neo4j Database** | 16 Super Labels, psychohistory functions | Hierarchical properties, graph expansion | ✅ SHARED |
| **Docker Network** | aeon-net | aeon-net | ✅ SHARED |
| **Monitoring** | Prometheus + Grafana | Same metrics stack | ✅ SHARED |
| **Qdrant** | Not used | Dedicated vector search | ❌ E30 only |
| **NER11 API** | Not used | Dedicated entity extraction | ❌ E30 only |

---

## Operational Status

### Current Deployment State

**Timestamp**: 2025-12-01 21:00 UTC

**Services Running**:
- ✅ Neo4j 5.26 (1.1M+ nodes, 3.3M+ relationships)
- ✅ Qdrant (670+ vectors, 8 payload indexes)
- ✅ NER11 Gold API v3.0.0 (FastAPI)
- ✅ E27 Psychohistory Functions (5/5 operational)
- ✅ E30 Hierarchical Entity Processor
- ✅ E30 Hybrid Search Engine

**Endpoints Operational**:
```bash
# NER11 Endpoints (E30)
✅ POST http://localhost:8000/ner                    # Entity extraction
✅ POST http://localhost:8000/search/semantic        # Semantic search
✅ POST http://localhost:8000/search/hybrid          # Hybrid search

# Neo4j Endpoints (E27 + E30)
✅ bolt://localhost:7687                             # Bolt protocol
✅ http://localhost:7474                             # HTTP browser

# Qdrant Endpoints (E30)
✅ http://localhost:6333                             # HTTP API
✅ http://localhost:6333/collections                 # Collection management
```

**Performance Verification**:
- All response time SLAs: ✅ MEETING TARGETS
- All throughput targets: ✅ MEETING MINIMUM
- Resource utilization: ✅ WITHIN LIMITS
- Data preservation: ✅ 1.1M nodes intact

---

## Quick Reference Commands

### Health Checks

**Check All E30 Services**:
```bash
# Run comprehensive health check
bash /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/scripts/check_e30_health.sh

# Expected output:
# ✅ NER11 API responding
# ✅ NER11 model loaded
# ✅ Qdrant operational
# ✅ Qdrant points: 670+
# ✅ Neo4j operational
# ✅ Neo4j nodes: 1,104,066+
# ✅ Node preservation verified
```

**Individual Service Checks**:
```bash
# NER11 API
curl http://localhost:8000/health

# Qdrant
curl http://localhost:6333/collections/ner11_entities_hierarchical

# Neo4j
cypher-shell -u neo4j -p neo4j@openspg "MATCH (n) RETURN count(n)"
```

### Monitoring

**View Current Metrics**:
```bash
# NER11 API metrics (if Prometheus endpoint enabled)
curl http://localhost:8000/metrics

# Neo4j system metrics
cypher-shell -u neo4j -p neo4j@openspg <<'EOF'
CALL dbms.queryJmx("org.neo4j:*")
YIELD attributes
RETURN attributes.HeapMemoryUsage, attributes.PageCacheHitRatio;
EOF

# Qdrant collection stats
curl http://localhost:6333/collections/ner11_entities_hierarchical \
  | python3 -m json.tool
```

### Backup Commands

**Create Backups**:
```bash
# Qdrant snapshot
curl -X POST http://localhost:6333/collections/ner11_entities_hierarchical/snapshots

# Neo4j hierarchical entities
cypher-shell -u neo4j -p neo4j@openspg <<'EOF'
CALL apoc.export.cypher.query(
  "MATCH (n) WHERE n.ner_label IS NOT NULL OPTIONAL MATCH (n)-[r]->(m) RETURN n,r,m",
  '/backup/e30_ner11_backup.cypher',
  {format: 'cypher-shell'}
);
EOF
```

---

## Troubleshooting Guide

### Common Issues Reference

| Issue | Severity | Quick Fix | Full Doc Reference |
|-------|----------|-----------|-------------------|
| Hybrid search returns 503 | 🔴 HIGH | Restart Neo4j: `docker restart openspg-neo4j` | E30_INFRASTRUCTURE.md §9 |
| Semantic search empty results | 🟡 MEDIUM | Check Qdrant points: `curl http://localhost:6333/...` | E30_INFRASTRUCTURE.md §9 |
| Node count decreased | 🔴 CRITICAL | STOP ingestion, restore backup | E30_INFRASTRUCTURE.md §9 |
| Tier2 == Tier1 (hierarchy broken) | 🔴 HIGH | Fix processor, re-run classification | E30_INFRASTRUCTURE.md §9 |
| Neo4j query slow | 🟡 MEDIUM | Check indexes: `SHOW INDEXES` | E27_INFRASTRUCTURE.md §5 |
| Cluster replication lag | 🔴 HIGH | Check network/disk I/O | E27_INFRASTRUCTURE.md §6 |

### Log Analysis

**Find Errors in Logs**:
```bash
# NER11 API errors
docker logs ner11-gold-api 2>&1 | grep -i error

# Qdrant errors
docker logs openspg-qdrant 2>&1 | grep -i error

# Neo4j errors
docker logs openspg-neo4j 2>&1 | grep -i error
```

---

## Document Maintenance

**This README Must Be Updated When**:
- New infrastructure document added
- Enhancement deployment status changes
- Service URLs or ports change
- Performance baselines updated
- New operational procedures added

**Update Checklist**:
- [ ] Update "Last Updated" timestamp
- [ ] Update service status (PLANNED → OPERATIONAL)
- [ ] Update performance metrics if changed
- [ ] Update quick reference commands if changed
- [ ] Commit changes to git with descriptive message

---

**This directory is the RECORD OF NOTE** for:
- Infrastructure deployment procedures
- Operational monitoring and alerting
- Backup and recovery procedures
- Performance baselines and SLAs
- Troubleshooting and incident response

All infrastructure documentation in this directory must be kept current with deployed systems.

---

**End of Infrastructure Directory README**
