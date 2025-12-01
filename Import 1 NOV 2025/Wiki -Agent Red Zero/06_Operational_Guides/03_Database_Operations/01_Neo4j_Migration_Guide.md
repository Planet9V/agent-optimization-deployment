---
title: Neo4j 5.15 to 5.26 Migration Guide - AgentZero Platform
category: 06_Operational_Guides/03_Database_Operations
last_updated: 2025-10-25
line_count: 398
status: published
tags: [neo4j, migration, database, upgrade, operations, backup, docker]
---

# Neo4j 5.15 to 5.26 Migration Guide

## Overview

This guide provides step-by-step instructions for migrating your AgentZero platform's Neo4j graph database from **version 5.15-community** to **5.26-community** (current LTS release).

**Migration Complexity:** Moderate
**Estimated Time:** 30-60 minutes
**Downtime Required:** Yes (all services stopped during migration)
**Risk Level:** Medium (backup required, testing essential)

### Why Upgrade?

- **Security:** 11 minor versions of security patches and bug fixes
- **Performance:** Improved query optimization and memory management
- **LTS Support:** Version 5.26.x supported until November 2028
- **Features:** Enhanced APOC procedures, better monitoring, improved stability

### Migration Path

```
Current: neo4j:5.15-community (Docker image)
Target:  neo4j:5.26-community (Docker image)
Method:  Backup → Stop → Image Update → Auto-Migration → Verify
```

---

## Prerequisites

### System Requirements

✅ **Before starting, verify:**
- [ ] Sufficient disk space (3x current Neo4j data size recommended)
- [ ] Current Neo4j database is healthy (`docker logs neo4j` shows no errors)
- [ ] All AgentZero services are functioning normally
- [ ] You have shell access to the Docker host
- [ ] You understand the 30-60 minute downtime window

### Current Configuration

**Your AgentZero Neo4j Setup:**
```yaml
Image: neo4j:5.15-community
Container: neo4j
Ports: 7474 (HTTP), 7687 (Bolt)
Username: neo4j
Password: agentzero123
Memory: 4G limit, 2G reservation
CPU: 8.0 limit, 4.0 reservation
```

**Data Volumes:**
```
neo4j-data:/data              # Database files (persistent)
neo4j-logs:/logs              # Log files
neo4j-import:/var/lib/neo4j/import
neo4j-plugins:/plugins
shared-data:/shared           # Inter-service communication
```

---

## Phase 1: Pre-Migration Preparation

### Step 1: Verify Current State

**Check Neo4j is healthy:**
```bash
cd /Users/jim/Documents/5_AgentZero/container_agentzero

# Check container status
docker ps | grep neo4j

# Verify Neo4j is responding
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "CALL dbms.components() YIELD name, versions, edition"

# Check current database size
docker exec neo4j du -sh /data/databases/neo4j
```

**Expected Output:**
```
neo4j   up   5.15.0   community
[Database size output, e.g., 2.3G]
```

### Step 2: Document Current Statistics

**Capture baseline metrics:**
```bash
# Node count
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "MATCH (n) RETURN count(n) as total_nodes"

# Relationship count
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "MATCH ()-[r]->() RETURN count(r) as total_relationships"

# Index status
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "SHOW INDEXES"

# Constraint status
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "SHOW CONSTRAINTS"
```

**Save this output to a file for post-migration verification:**
```bash
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "MATCH (n) RETURN count(n)" > ~/neo4j_pre_migration_stats.txt
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "MATCH ()-[r]->() RETURN count(r)" >> ~/neo4j_pre_migration_stats.txt
```

### Step 3: Create Backup Directory

**Prepare backup location:**
```bash
# Create backup directory on host
mkdir -p ~/neo4j_backups/migration_$(date +%Y%m%d_%H%M%S)
cd ~/neo4j_backups/migration_$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=$(pwd)
echo "Backup directory: $BACKUP_DIR"
```

---

## Phase 2: Database Backup

### Step 4: Stop All AgentZero Services (EXCEPT Neo4j)

**Stop dependent services first:**
```bash
cd /Users/jim/Documents/5_AgentZero/container_agentzero

# Stop services that depend on Neo4j
docker-compose stop agentzero
docker-compose stop neocoder
docker-compose stop document-parser

# Verify only Neo4j is running
docker ps --filter "name=neo4j"
```

**Why this order?**
- Prevents data writes during backup
- Ensures database consistency
- Reduces backup size (no active transactions)

### Step 5: Create Neo4j Database Dump

**Using neo4j-admin dump (recommended method):**
```bash
# Dump the neo4j database
docker exec neo4j neo4j-admin database dump neo4j \
  --to-path=/backups \
  --verbose

# Copy dump to host backup directory
docker cp neo4j:/backups/neo4j.dump "$BACKUP_DIR/"

# Verify dump file exists and check size
ls -lh "$BACKUP_DIR/neo4j.dump"
```

**Expected Output:**
```
-rw-r--r-- 1 neo4j neo4j 1.2G Oct 25 12:00 neo4j.dump
```

### Step 6: Backup Docker Volumes (Additional Safety)

**Copy entire Neo4j data volume:**
```bash
# Create volume backup using Docker
docker run --rm \
  -v neo4j-data:/source:ro \
  -v "$BACKUP_DIR":/backup \
  alpine tar czf /backup/neo4j-data-volume.tar.gz -C /source .

# Verify volume backup
ls -lh "$BACKUP_DIR/neo4j-data-volume.tar.gz"
```

### Step 7: Backup Configuration Files

**Save docker-compose.yml and .env:**
```bash
cd /Users/jim/Documents/5_AgentZero/container_agentzero

# Backup docker-compose.yml
cp docker-compose.yml "$BACKUP_DIR/docker-compose.yml.backup"

# Backup .env (contains credentials)
cp .env "$BACKUP_DIR/.env.backup"

# List backup contents
ls -lh "$BACKUP_DIR/"
```

**Your backup directory should now contain:**
```
neo4j.dump                    # Database dump (primary backup)
neo4j-data-volume.tar.gz      # Full volume backup (safety)
docker-compose.yml.backup     # Configuration
.env.backup                   # Credentials
```

---

## Phase 3: Migration Execution

### Step 8: Stop Neo4j Container

```bash
cd /Users/jim/Documents/5_AgentZero/container_agentzero

# Stop Neo4j gracefully
docker-compose stop neo4j

# Verify Neo4j is stopped
docker ps -a | grep neo4j
```

**Expected Status:** `Exited (0)`

### Step 9: Update Docker Compose Configuration

**Edit docker-compose.yml to use Neo4j 5.26:**
```bash
# Backup current docker-compose.yml (additional safety)
cp docker-compose.yml docker-compose.yml.pre-migration

# Update Neo4j image version
# Change line 116: image: neo4j:5.15-community
# To:             image: neo4j:5.26-community
```

**Use this Edit command:**
```yaml
# Find this section (around line 116):
  neo4j:
    platform: linux/amd64
    image: neo4j:5.15-community  # ← CHANGE THIS LINE
    container_name: neo4j

# Change to:
  neo4j:
    platform: linux/amd64
    image: neo4j:5.26-community  # ← NEW VERSION
    container_name: neo4j
```

### Step 10: Pull New Neo4j Image

```bash
# Pull Neo4j 5.26 image
docker pull neo4j:5.26-community

# Verify image download
docker images | grep neo4j
```

**Expected Output:**
```
neo4j    5.26-community    <image-id>    <size>    <date>
neo4j    5.15-community    <image-id>    <size>    <date>
```

### Step 11: Start Neo4j with New Image

```bash
cd /Users/jim/Documents/5_AgentZero/container_agentzero

# Start Neo4j container with new image
docker-compose up -d neo4j

# Monitor migration logs in real-time
docker logs -f neo4j
```

**Watch for these log messages:**
```
INFO  Starting Neo4j
INFO  Detected upgrade from 5.15.x to 5.26.x
INFO  Migrating database format...
INFO  Migration completed successfully
INFO  Started
INFO  Bolt enabled on bolt://0.0.0.0:7687
```

**Migration typically takes 5-15 minutes depending on database size.**

---

## Phase 4: Post-Migration Verification

### Step 12: Verify Neo4j Health

**Check Neo4j web interface:**
```bash
# Open in browser
open http://localhost:7474

# Or use curl to verify HTTP interface
curl -I http://localhost:7474
```

**Login credentials:**
- Username: `neo4j`
- Password: `agentzero123`

### Step 13: Verify Database Version

```bash
# Check Neo4j version
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "CALL dbms.components() YIELD name, versions, edition RETURN name, versions[0] as version, edition"
```

**Expected Output:**
```
name    version    edition
Neo4j   5.26.14    community
```

### Step 14: Verify Data Integrity

**Compare with pre-migration statistics:**
```bash
# Node count
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "MATCH (n) RETURN count(n) as total_nodes"

# Relationship count
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "MATCH ()-[r]->() RETURN count(r) as total_relationships"

# Compare with saved stats
cat ~/neo4j_pre_migration_stats.txt
```

**Node and relationship counts MUST match pre-migration values.**

### Step 15: Verify Indexes and Constraints

```bash
# Check indexes
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "SHOW INDEXES"

# Check constraints
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "SHOW CONSTRAINTS"
```

**All indexes should be ONLINE, all constraints should be present.**

### Step 16: Test Sample Queries

```bash
# Test a simple query
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "MATCH (n) RETURN n LIMIT 5"

# Test a relationship query
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "MATCH (a)-[r]->(b) RETURN type(r), count(r) LIMIT 10"
```

**Queries should return data without errors.**

---

## Phase 5: Restart AgentZero Services

### Step 17: Start NeoCoder MCP Server

```bash
cd /Users/jim/Documents/5_AgentZero/container_agentzero

# Start NeoCoder (depends on Neo4j)
docker-compose up -d neocoder

# Monitor NeoCoder logs
docker logs -f neocoder
```

**Watch for successful Neo4j connection:**
```
INFO: Connected to Neo4j at bolt://neo4j:7687
INFO: NeoCoder MCP Server started on port 8002
```

### Step 18: Start Document Parser

```bash
# Start document parser
docker-compose up -d document-parser

# Verify health
docker logs document-parser | tail -20
```

### Step 19: Start AgentZero Core

```bash
# Start main AgentZero service
docker-compose up -d agentzero

# Monitor startup
docker logs -f agentzero
```

### Step 20: Start Remaining Services

```bash
# Start all remaining services
docker-compose up -d

# Verify all services are running
docker ps
```

**All containers should show status: `Up`**

---

## Phase 6: Integration Testing

### Step 21: Test NeoCoder Integration

```bash
# Test NeoCoder health endpoint
curl http://localhost:8002/health

# Expected response:
{"status": "healthy", "neo4j": "connected", "qdrant": "connected"}
```

### Step 22: Test AgentZero Functionality

**Via AgentZero web interface:**
1. Access http://localhost:50001
2. Send test query to verify Neo4j integration
3. Check that knowledge graph queries work
4. Verify document processing functions

### Step 23: Monitor System Logs

```bash
# Check all service logs for errors
docker-compose logs --tail=50

# Monitor Neo4j specifically
docker logs neo4j | grep -i error
docker logs neo4j | grep -i warn
```

**No ERROR or CRITICAL messages should appear.**

---

## Rollback Procedure (If Migration Fails)

### Emergency Rollback Steps

**If migration fails or data is corrupted:**

```bash
# 1. Stop all services
cd /Users/jim/Documents/5_AgentZero/container_agentzero
docker-compose down

# 2. Restore docker-compose.yml to 5.15
cp docker-compose.yml.pre-migration docker-compose.yml

# 3. Remove Neo4j container and volume
docker rm neo4j
docker volume rm neo4j-data

# 4. Recreate volume
docker volume create neo4j-data

# 5. Restore volume from backup
docker run --rm \
  -v neo4j-data:/data \
  -v "$BACKUP_DIR":/backup \
  alpine tar xzf /backup/neo4j-data-volume.tar.gz -C /data

# 6. Start Neo4j 5.15
docker-compose up -d neo4j

# 7. Verify database is accessible
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "MATCH (n) RETURN count(n)"

# 8. Start remaining services
docker-compose up -d
```

---

## Troubleshooting

### Issue: Migration Hangs or Takes Too Long

**Symptoms:** Neo4j logs show no progress after 30 minutes

**Solution:**
1. Check disk space: `df -h`
2. Check memory: `docker stats neo4j`
3. Increase Neo4j memory in docker-compose.yml if needed:
   ```yaml
   NEO4J_dbms_memory_heap_max__size=4G  # increase from 3G
   ```

### Issue: Authentication Failed After Migration

**Symptoms:** `cypher-shell` returns "authentication failed"

**Solution:**
```bash
# Reset password
docker exec -it neo4j neo4j-admin dbms set-initial-password agentzero123

# Restart Neo4j
docker-compose restart neo4j
```

### Issue: Missing Data After Migration

**Symptoms:** Node/relationship counts don't match

**Solution:**
1. Check migration logs: `docker logs neo4j | grep -i migrate`
2. Verify backup integrity: `file "$BACKUP_DIR/neo4j.dump"`
3. If corrupted, perform rollback and retry migration

### Issue: Performance Degradation

**Symptoms:** Queries are slower after migration

**Solution:**
```bash
# Rebuild indexes
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "CALL db.indexes() YIELD name RETURN name"

# Check query planning
docker exec neo4j cypher-shell -u neo4j -p agentzero123 \
  "EXPLAIN MATCH (n) RETURN n LIMIT 1"
```

---

## Post-Migration Cleanup

### After Successful Migration

**Once migration is verified successful (after 24-48 hours):**

```bash
# Optional: Remove old Neo4j 5.15 image to save space
docker rmi neo4j:5.15-community

# Keep backups for 30 days, then remove
# DO NOT delete backups immediately!
```

### Backup Retention Policy

**Recommended:**
- Keep migration backups for 30 days
- Schedule regular backups weekly after migration
- Test restore procedure quarterly

---

## Related Documentation

- [Neo4j Official Upgrade Guide](https://neo4j.com/docs/upgrade-migration-guide/)
- [Docker Optimization Guide](../01_Docker_Optimization/01_Resource_Management.md)
- [NeoCoder Installation](../../02_NeoCoder_MCP_Server/01_Getting_Started/01_Installation.md)

---

**Last Updated:** 2025-10-25 | **Lines:** 398/400 | **Status:** published
