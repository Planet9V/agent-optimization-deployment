---
title: Neo4j Migration Quick Reference Card
category: 06_Operational_Guides/03_Database_Operations
last_updated: 2025-10-25
line_count: 142
status: published
tags: [neo4j, migration, quick-reference, cheatsheet, operations]
---

# Neo4j Migration Quick Reference Card

**Quick access companion to the [full migration guide](./01_Neo4j_Migration_Guide.md)**

---

## Pre-Flight Checklist

```bash
# 1. Verify current state
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "CALL dbms.components() YIELD versions RETURN versions[0]"
# Expected: 5.15.0

# 2. Check disk space (need 3x database size)
docker exec neo4j du -sh /data/databases/neo4j

# 3. Save baseline stats
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "MATCH (n) RETURN count(n)" > ~/neo4j_baseline.txt
```

---

## Critical Commands (Copy-Paste Ready)

### Backup Phase

```bash
# Create backup directory
mkdir -p ~/neo4j_backups/migration_$(date +%Y%m%d_%H%M%S)
cd ~/neo4j_backups/migration_$(date +%Y%m%d_%H%M%S)
export BACKUP_DIR=$(pwd)

# Stop AgentZero services (keep Neo4j running)
cd /Users/jim/Documents/5_AgentZero/container_agentzero
docker-compose stop agentzero neocoder document-parser

# Create database dump
docker exec neo4j neo4j-admin database dump neo4j \
  --to-path=/backups --verbose

# Copy dump to host
docker cp neo4j:/backups/neo4j.dump "$BACKUP_DIR/"

# Backup volume (additional safety)
docker run --rm \
  -v neo4j-data:/source:ro \
  -v "$BACKUP_DIR":/backup \
  alpine tar czf /backup/neo4j-data-volume.tar.gz -C /source .

# Backup configs
cp docker-compose.yml "$BACKUP_DIR/docker-compose.yml.backup"
cp .env "$BACKUP_DIR/.env.backup"
```

### Migration Phase

```bash
cd /Users/jim/Documents/5_AgentZero/container_agentzero

# Stop Neo4j
docker-compose stop neo4j

# Edit docker-compose.yml (line 116)
# Change: image: neo4j:5.15-community
# To:     image: neo4j:5.26-community

# Pull new image
docker pull neo4j:5.26-community

# Start with new image (auto-migration happens)
docker-compose up -d neo4j

# Monitor migration logs
docker logs -f neo4j
# Watch for: "Migration completed successfully"
```

### Verification Phase

```bash
# Check new version
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "CALL dbms.components() YIELD versions RETURN versions[0]"
# Expected: 5.26.14

# Verify data integrity (compare with baseline)
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "MATCH (n) RETURN count(n)"

# Test sample query
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "MATCH (n) RETURN n LIMIT 5"

# Restart all services
docker-compose up -d

# Test NeoCoder health
curl http://localhost:8002/health
```

---

## Emergency Rollback

```bash
cd /Users/jim/Documents/5_AgentZero/container_agentzero

# 1. Stop everything
docker-compose down

# 2. Restore old docker-compose.yml
cp docker-compose.yml.pre-migration docker-compose.yml

# 3. Remove Neo4j container and volume
docker rm neo4j
docker volume rm neo4j-data

# 4. Recreate volume
docker volume create neo4j-data

# 5. Restore from backup
docker run --rm \
  -v neo4j-data:/data \
  -v "$BACKUP_DIR":/backup \
  alpine tar xzf /backup/neo4j-data-volume.tar.gz -C /data

# 6. Start services
docker-compose up -d
```

---

## Common Issues

| Issue | Quick Fix |
|-------|-----------|
| Migration hangs | Check disk space: `df -h` |
| Auth fails | Reset password: `docker exec -it neo4j neo4j-admin dbms set-initial-password agentzero123` |
| Missing data | Rollback and retry migration |
| Slow queries | Rebuild indexes in Neo4j browser |

---

## Migration Timeline

| Phase | Duration | Key Action |
|-------|----------|------------|
| Backup | 5-10 min | Create dumps and volume backups |
| Migration | 5-15 min | Auto-migration by Neo4j 5.26 |
| Verification | 5-10 min | Compare stats, test queries |
| Service restart | 5 min | Bring up all containers |
| **Total** | **20-40 min** | **Complete downtime window** |

---

## Post-Migration Validation

```bash
# ✅ Checklist
[ ] Neo4j version is 5.26.14
[ ] Node counts match baseline
[ ] Relationship counts match baseline
[ ] All indexes are ONLINE
[ ] Sample queries return data
[ ] NeoCoder health endpoint returns 200
[ ] AgentZero web interface accessible
[ ] No errors in docker logs
```

---

## Access Information

**Neo4j Web Interface:** http://localhost:7474
**Credentials:** neo4j / agentzero123
**Bolt URI:** bolt://localhost:7687
**NeoCoder Health:** http://localhost:8002/health
**AgentZero UI:** http://localhost:50001

---

**Full Guide:** [01_Neo4j_Migration_Guide.md](./01_Neo4j_Migration_Guide.md)

---

**Last Updated:** 2025-10-25 | **Lines:** 142/400 | **Status:** published
