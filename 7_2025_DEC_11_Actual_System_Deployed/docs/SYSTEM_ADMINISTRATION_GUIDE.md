# AEON System Administration Guide

**File:** SYSTEM_ADMINISTRATION_GUIDE.md
**Created:** 2025-12-12
**Version:** 1.0.0
**Author:** AEON Development Team
**Purpose:** Comprehensive administration guide for AEON cybersecurity knowledge graph system
**Status:** ACTIVE

## Table of Contents

1. [System Overview](#system-overview)
2. [System Components](#system-components)
3. [Credentials & Access](#credentials--access)
4. [Daily Operations](#daily-operations)
5. [Backup & Restore](#backup--restore)
6. [Monitoring & Health Checks](#monitoring--health-checks)
7. [Maintenance Procedures](#maintenance-procedures)
8. [Troubleshooting](#troubleshooting)
9. [Performance Optimization](#performance-optimization)
10. [Security Best Practices](#security-best-practices)

---

## System Overview

### Current Deployment Status

**System Name:** AEON (Advanced Entity Organization Network)
**Environment:** Production
**Database:** Neo4j 5.26.14 Community Edition
**Container Runtime:** Docker
**Host OS:** WSL2 Ubuntu on Windows

### Key Metrics (as of 2025-12-12)

- **Total Nodes:** 1,207,069
- **Total Relationships:** 12,344,852
- **Database Labels:** 631
- **Database Size:** ~7.2 GB (backup size)
- **Memory Usage:** 8.6 GB / 16 GB (54%)
- **CPU Usage:** ~400% (multi-core)
- **Uptime:** 32+ hours (healthy)

---

## System Components

### Primary Services

#### 1. Neo4j Graph Database (openspg-neo4j)

**Container Name:** `openspg-neo4j`
**Image:** neo4j:5.26.14
**Status:** Running (healthy)
**Ports:**
- 7474 (HTTP) - Web interface
- 7687 (Bolt) - Database protocol

**Docker Volumes:**
```
openspg-neo4j-data        → /data (primary database storage)
openspg-neo4j-logs        → /logs (application logs)
openspg-neo4j-plugins     → /plugins (database plugins)
openspg-neo4j-import      → /var/lib/neo4j/import (data import)
openspg-neo4j-conf        → /conf (configuration)
openspg-shared-data       → /shared (shared files)
```

**Volume Locations:**
All volumes are stored in `/var/lib/docker/volumes/` with the pattern:
```
/var/lib/docker/volumes/<volume-name>/_data
```

#### 2. Qdrant Vector Database

**Status:** Currently not running (optional component)
**Volume:** `openspg-qdrant-data`
**Purpose:** Vector similarity search for schema and entity embeddings

#### 3. Supporting Services

Additional OpenSPG infrastructure volumes:
- `openspg-mysql-data` - MySQL database
- `openspg-redis-data` - Redis cache
- `openspg-minio-data` - MinIO object storage
- `openspg-server-logs` - Server application logs

---

## Credentials & Access

### Neo4j Database Credentials

**Connection String:** `bolt://localhost:7687`
**Username:** `neo4j`
**Password:** `neo4j@openspg`

### Web Interface Access

**URL:** http://localhost:7474
**Authentication:** Same as database credentials

### Credential Storage

**Location:** Stored in environment variables or configuration files
- Check `.env` files in project directory
- Docker container environment variables
- Application configuration files

### Changing Credentials

**⚠️ WARNING:** Changing credentials requires coordinated updates across multiple systems.

```bash
# 1. Connect to Neo4j
docker exec -it openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg'

# 2. Change password
ALTER CURRENT USER SET PASSWORD FROM 'neo4j@openspg' TO 'new_password';

# 3. Update application configuration files
# Update all .env files, configuration files, and scripts

# 4. Restart services
docker restart openspg-neo4j
```

**Files to update after password change:**
- Python scripts in `/scripts/` directory
- Configuration files in project root
- Any automation scripts or cron jobs
- Documentation with connection examples

---

## Daily Operations

### Starting the System

```bash
# Start Neo4j container
docker start openspg-neo4j

# Verify it's running
docker ps --filter "name=openspg-neo4j"

# Check health status
docker inspect openspg-neo4j --format='{{.State.Health.Status}}'
```

### Stopping the System

```bash
# Graceful shutdown
docker stop openspg-neo4j

# Force stop (emergency only)
docker kill openspg-neo4j
```

### Restarting the System

```bash
# Restart Neo4j
docker restart openspg-neo4j

# Wait for healthy status (takes ~30 seconds)
watch -n 2 'docker inspect openspg-neo4j --format="{{.State.Health.Status}}"'
```

### Checking System Status

```bash
# Container status
docker ps --filter "name=openspg-neo4j" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Resource usage
docker stats openspg-neo4j --no-stream

# Database version and edition
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "CALL dbms.components() YIELD name, versions, edition RETURN name, versions[0] as version, edition"
```

---

## Backup & Restore

### Manual Backup Procedure

#### Complete Database Backup

```bash
#!/bin/bash
# Location: /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/backup_neo4j.sh

BACKUP_DIR="/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="${BACKUP_DIR}/neo4j-${TIMESTAMP}"

# Create backup directory
mkdir -p "${BACKUP_PATH}"

# Stop database (optional for consistency)
# docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "CALL dbms.checkpoint()"

# Backup using admin dump
docker exec openspg-neo4j neo4j-admin database dump neo4j \
  --to-path=/shared/backup-${TIMESTAMP}.dump

# Copy from container to host
docker cp openspg-neo4j:/shared/backup-${TIMESTAMP}.dump "${BACKUP_PATH}/"

# Backup configuration
docker cp openspg-neo4j:/conf "${BACKUP_PATH}/conf"

# Create metadata
cat > "${BACKUP_PATH}/backup_metadata.txt" << EOF
Backup Date: $(date)
Neo4j Version: $(docker exec openspg-neo4j neo4j --version)
Database: neo4j
Node Count: $(docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "MATCH (n) RETURN count(n) as total" --format plain)
Relationship Count: $(docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "MATCH ()-[r]->() RETURN count(r) as total" --format plain)
EOF

echo "Backup completed: ${BACKUP_PATH}"
du -sh "${BACKUP_PATH}"
```

#### Volume Backup (Alternative Method)

```bash
# Backup Docker volume directly
BACKUP_DIR="/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Stop container for consistent backup
docker stop openspg-neo4j

# Backup data volume
docker run --rm \
  -v openspg-neo4j-data:/source:ro \
  -v "${BACKUP_DIR}:/backup" \
  ubuntu tar czf "/backup/neo4j-data-${TIMESTAMP}.tar.gz" -C /source .

# Backup logs volume
docker run --rm \
  -v openspg-neo4j-logs:/source:ro \
  -v "${BACKUP_DIR}:/backup" \
  ubuntu tar czf "/backup/neo4j-logs-${TIMESTAMP}.tar.gz" -C /source .

# Restart container
docker start openspg-neo4j

echo "Volume backup completed: ${BACKUP_DIR}"
```

### Restore Procedure

#### Restore from Dump

```bash
#!/bin/bash
# Restore from backup dump

BACKUP_FILE="/path/to/backup/neo4j-YYYYMMDD_HHMMSS.dump"

# Stop database
docker stop openspg-neo4j

# Load dump
docker run --rm \
  -v openspg-neo4j-data:/data \
  -v "${BACKUP_FILE}:/backup.dump:ro" \
  neo4j:5.26.14 \
  neo4j-admin database load neo4j --from-path=/backup.dump --overwrite-destination=true

# Start database
docker start openspg-neo4j

# Verify restoration
sleep 30
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (n) RETURN count(n) as nodes"
```

#### Restore from Volume Backup

```bash
# Stop container
docker stop openspg-neo4j

# Remove old volume
docker volume rm openspg-neo4j-data

# Create new volume
docker volume create openspg-neo4j-data

# Restore data
docker run --rm \
  -v openspg-neo4j-data:/target \
  -v "/backup/location:/backup:ro" \
  ubuntu tar xzf /backup/neo4j-data-YYYYMMDD_HHMMSS.tar.gz -C /target

# Start container
docker start openspg-neo4j
```

### Backup Schedule Recommendations

**Daily Backups:**
```bash
# Cron job: Daily at 2 AM
0 2 * * * /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/backup_neo4j.sh
```

**Weekly Backups:**
```bash
# Cron job: Every Sunday at 3 AM (full backup including volumes)
0 3 * * 0 /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/backup_neo4j_full.sh
```

**Retention Policy:**
- Daily backups: Keep 7 days
- Weekly backups: Keep 4 weeks
- Monthly backups: Keep 12 months

**Backup Cleanup Script:**
```bash
#!/bin/bash
BACKUP_DIR="/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/backups"

# Remove backups older than 7 days
find "${BACKUP_DIR}" -type d -name "neo4j-*" -mtime +7 -exec rm -rf {} +

# Keep at least 3 most recent backups
ls -dt "${BACKUP_DIR}"/neo4j-* | tail -n +4 | xargs rm -rf
```

---

## Monitoring & Health Checks

### Database Health Checks

#### Quick Health Check

```bash
# Container health
docker inspect openspg-neo4j --format='{{.State.Health.Status}}'

# Database connectivity
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "RETURN 'Database is responsive' as status"
```

#### Comprehensive Health Check Script

```bash
#!/bin/bash
# Location: /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/health_check.sh

echo "=== AEON System Health Check ==="
echo "Date: $(date)"
echo ""

# Container status
echo "1. Container Status:"
docker ps --filter "name=openspg-neo4j" --format "   Status: {{.Status}}"
echo ""

# Resource usage
echo "2. Resource Usage:"
docker stats openspg-neo4j --no-stream --format "   CPU: {{.CPUPerc}}  Memory: {{.MemUsage}} ({{.MemPerc}})"
echo ""

# Database metrics
echo "3. Database Metrics:"
NODE_COUNT=$(docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (n) RETURN count(n) as total" --format plain | tail -1)
REL_COUNT=$(docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH ()-[r]->() RETURN count(r) as total" --format plain | tail -1)
LABEL_COUNT=$(docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "CALL db.labels() YIELD label RETURN count(label) as total" --format plain | tail -1)

echo "   Nodes: ${NODE_COUNT}"
echo "   Relationships: ${REL_COUNT}"
echo "   Labels: ${LABEL_COUNT}"
echo ""

# Disk space
echo "4. Disk Space:"
df -h /var/lib/docker/volumes/openspg-neo4j-data/_data 2>/dev/null | tail -1 | \
  awk '{print "   Total: "$2"  Used: "$3"  Available: "$4"  Use%: "$5}'
echo ""

# Recent errors
echo "5. Recent Errors:"
ERROR_COUNT=$(docker logs openspg-neo4j --since 24h 2>&1 | grep -i -E "error|exception" | wc -l)
echo "   Errors in last 24h: ${ERROR_COUNT}"
if [ ${ERROR_COUNT} -gt 0 ]; then
  echo "   Recent errors:"
  docker logs openspg-neo4j --since 24h 2>&1 | grep -i -E "error|exception" | tail -5 | sed 's/^/   /'
fi
echo ""

# Database connectivity
echo "6. Database Connectivity:"
if docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "RETURN 'OK' as status" --format plain > /dev/null 2>&1; then
  echo "   ✓ Database is responsive"
else
  echo "   ✗ Database connection failed"
fi
echo ""

echo "=== Health Check Complete ==="
```

### Disk Space Monitoring

```bash
# Check overall disk usage
df -h /var/lib/docker/volumes/

# Check Neo4j data volume specifically
du -sh /var/lib/docker/volumes/openspg-neo4j-data/_data

# Check backup directory
du -sh /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/backups/

# Alert if disk usage > 80%
USAGE=$(df /var/lib/docker/volumes/ | tail -1 | awk '{print $5}' | sed 's/%//')
if [ ${USAGE} -gt 80 ]; then
  echo "WARNING: Disk usage is ${USAGE}%"
fi
```

### Query Performance Monitoring

```bash
# Check slow queries (if query logging enabled)
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "CALL dbms.listQueries() YIELD query, elapsedTimeMillis, allocatedBytes
   WHERE elapsedTimeMillis > 1000
   RETURN query, elapsedTimeMillis, allocatedBytes
   ORDER BY elapsedTimeMillis DESC"

# Monitor transaction statistics
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "CALL dbms.listTransactions() YIELD transactionId, currentQuery, elapsedTimeMillis
   RETURN transactionId, currentQuery, elapsedTimeMillis
   ORDER BY elapsedTimeMillis DESC"
```

### Validation Queries

#### Schema Validation

```cypher
// Count all labels
CALL db.labels() YIELD label
RETURN count(label) as total_labels;

// Count nodes per label (top 20)
CALL db.labels() YIELD label
CALL apoc.cypher.run('MATCH (n:`' + label + '`) RETURN count(n) as count', {})
YIELD value
RETURN label, value.count as node_count
ORDER BY node_count DESC
LIMIT 20;

// Check for nodes without labels
MATCH (n)
WHERE size(labels(n)) = 0
RETURN count(n) as unlabeled_nodes;
```

#### Relationship Validation

```cypher
// Count all relationship types
CALL db.relationshipTypes() YIELD relationshipType
RETURN count(relationshipType) as total_relationship_types;

// Count relationships per type (top 20)
CALL db.relationshipTypes() YIELD relationshipType
CALL apoc.cypher.run('MATCH ()-[r:`' + relationshipType + '`]->() RETURN count(r) as count', {})
YIELD value
RETURN relationshipType, value.count as relationship_count
ORDER BY relationship_count DESC
LIMIT 20;
```

#### Data Integrity Checks

```cypher
// Check for orphaned nodes
MATCH (n)
WHERE NOT (n)--()
RETURN count(n) as orphaned_nodes;

// Check index usage
SHOW INDEXES YIELD name, type, entityType, state, populationPercent
RETURN name, type, entityType, state, populationPercent;

// Check constraint violations
SHOW CONSTRAINTS YIELD name, type, entityType, labelsOrTypes
RETURN name, type, entityType, labelsOrTypes;
```

---

## Maintenance Procedures

### Running Migrations

#### Check Current Schema State

```bash
# Extract current schema
python3 /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/extract_actual_schema.py

# Verify schema in Qdrant (if running)
python3 /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/store_schema_in_qdrant.py
```

#### Re-run Hierarchical Schema Migration

```bash
# Fix hierarchical schema relationships
python3 /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/FIX_HIERARCHICAL_SCHEMA_COMPLETE.py

# Verify hierarchical relationships
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (child)-[:IS_A]->(parent)
   RETURN labels(child)[0] as child_label, labels(parent)[0] as parent_label, count(*) as count
   ORDER BY count DESC LIMIT 20"
```

#### Fix CVE Super Labels

```bash
# Apply CVE label fixes
python3 /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/FIX_CVE_SUPER_LABELS.py

# Verify CVE structure
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (c:CVE) RETURN count(c) as total_cves"
```

### Schema Validation and Repair

```bash
# Run schema validation
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' << 'EOF'
// Check for missing required properties
MATCH (n)
WHERE NOT EXISTS(n.id)
RETURN labels(n) as label, count(n) as nodes_without_id
ORDER BY nodes_without_id DESC;

// Check for duplicate IDs
MATCH (n)
WITH n.id as id, labels(n) as labels, collect(n) as nodes
WHERE size(nodes) > 1
RETURN id, labels, size(nodes) as duplicate_count;
EOF
```

### Data Enrichment Procedures

#### Update CVE Data

```bash
# Safe CVE update procedure
python3 /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/cve_fix_safe.py
```

#### Re-index Database

```cypher
// Rebuild all indexes
CALL db.indexes() YIELD name, state
WHERE state <> 'ONLINE'
WITH name
CALL db.index.fulltext.drop(name)
YIELD name as dropped;

// Recreate failed indexes
CALL db.indexes() YIELD name, labelsOrTypes, properties
WHERE name STARTS WITH 'failed_'
RETURN name, labelsOrTypes, properties;
```

### Database Optimization

#### Statistics Update

```cypher
// Update database statistics
CALL db.stats.clear();
CALL db.stats.collect();
```

#### Index Optimization

```cypher
// Check index effectiveness
CALL db.indexes() YIELD name, uniqueness, state, populationPercent
RETURN name, uniqueness, state, populationPercent
ORDER BY populationPercent ASC;

// Drop unused indexes
CALL db.indexes() YIELD name, state
WHERE state = 'FAILED'
WITH name
CALL db.index.drop(name)
YIELD name as dropped
RETURN dropped;
```

#### Database Compaction

```bash
# Checkpoint and compact
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "CALL dbms.checkpoint()"

# Note: Full compaction requires database shutdown
# See Neo4j documentation for offline compaction procedures
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Container Won't Start

```bash
# Check logs
docker logs openspg-neo4j --tail 100

# Common causes:
# 1. Port already in use
sudo lsof -i :7474
sudo lsof -i :7687

# 2. Corrupted volume
docker volume inspect openspg-neo4j-data

# 3. Insufficient memory
free -h
docker system df

# Solution: Remove and recreate container
docker rm -f openspg-neo4j
# Then recreate with docker-compose or docker run
```

#### Issue: Database Connection Refused

```bash
# Check if Neo4j is listening
docker exec openspg-neo4j netstat -tuln | grep -E '7474|7687'

# Check authentication
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "RETURN 1"

# Check logs for auth failures
docker logs openspg-neo4j --tail 100 | grep -i "authentication\|unauthorized"

# Solution: Reset password
docker exec -it openspg-neo4j cypher-shell -u neo4j
# Then: ALTER CURRENT USER SET PASSWORD FROM 'old' TO 'new';
```

#### Issue: Slow Query Performance

```bash
# Identify slow queries
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "CALL dbms.listQueries() YIELD query, elapsedTimeMillis
   WHERE elapsedTimeMillis > 5000
   RETURN query, elapsedTimeMillis
   ORDER BY elapsedTimeMillis DESC"

# Check missing indexes
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "PROFILE MATCH (n:YourLabel) WHERE n.property = 'value' RETURN n"

# Solution: Create appropriate indexes
# CREATE INDEX index_name FOR (n:Label) ON (n.property);
```

#### Issue: Out of Disk Space

```bash
# Check disk usage
df -h /var/lib/docker/volumes/

# Clear old backups
find /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/backups -mtime +7 -exec rm -rf {} +

# Clean Docker system
docker system prune -a --volumes

# Compact database (requires downtime)
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "CALL dbms.checkpoint()"
```

#### Issue: High Memory Usage

```bash
# Check memory configuration
docker exec openspg-neo4j cat /conf/neo4j.conf | grep -E 'memory|heap'

# Adjust heap size (edit configuration)
# dbms.memory.heap.initial_size=2G
# dbms.memory.heap.max_size=8G

# Restart to apply changes
docker restart openspg-neo4j
```

### Log Analysis

```bash
# View real-time logs
docker logs -f openspg-neo4j

# Search for specific errors
docker logs openspg-neo4j 2>&1 | grep -i "error" | tail -20

# Export logs for analysis
docker logs openspg-neo4j > /tmp/neo4j-logs-$(date +%Y%m%d).log

# Check log size
docker exec openspg-neo4j du -sh /logs/
```

### Emergency Recovery

```bash
#!/bin/bash
# Emergency recovery script

echo "Starting emergency recovery..."

# 1. Stop container
docker stop openspg-neo4j

# 2. Backup current state
EMERGENCY_BACKUP="/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/backups/emergency-$(date +%Y%m%d_%H%M%S)"
mkdir -p "${EMERGENCY_BACKUP}"
docker run --rm -v openspg-neo4j-data:/source:ro -v "${EMERGENCY_BACKUP}:/backup" \
  ubuntu tar czf /backup/data.tar.gz -C /source .

# 3. Try to start with recovery mode
docker run --rm \
  -v openspg-neo4j-data:/data \
  neo4j:5.26.14 \
  neo4j-admin database check neo4j --verbose

# 4. Restart container
docker start openspg-neo4j

echo "Emergency recovery complete. Check logs."
```

---

## Performance Optimization

### Query Optimization

#### Create Appropriate Indexes

```cypher
// Analyze query patterns first
CALL db.stats.retrieve('QUERIES');

// Create indexes for frequently queried properties
CREATE INDEX apt_group_name_idx FOR (n:APT_GROUP) ON (n.name);
CREATE INDEX cve_id_idx FOR (n:CVE) ON (n.id);
CREATE INDEX technique_id_idx FOR (n:Technique) ON (n.id);

// Full-text search indexes
CREATE FULLTEXT INDEX entity_name_fulltext FOR (n:Entity) ON EACH [n.name];
```

#### Query Profiling

```cypher
// Profile query execution
PROFILE
MATCH (a:APT_GROUP)-[:USES]->(t:Technique)
WHERE a.name = 'APT28'
RETURN t.name, t.description;

// Explain query plan
EXPLAIN
MATCH (c:CVE)-[:AFFECTS]->(p:Product)
WHERE c.severity = 'CRITICAL'
RETURN p.name, count(c) as critical_cves
ORDER BY critical_cves DESC
LIMIT 10;
```

### Memory Configuration

```bash
# Edit Neo4j configuration
docker exec -it openspg-neo4j vi /conf/neo4j.conf

# Recommended settings for 16GB system:
# dbms.memory.heap.initial_size=4G
# dbms.memory.heap.max_size=8G
# dbms.memory.pagecache.size=4G

# Restart to apply
docker restart openspg-neo4j
```

### Batch Operations Optimization

```cypher
// Use APOC for batch operations
CALL apoc.periodic.iterate(
  "MATCH (n:OldLabel) RETURN n",
  "SET n:NewLabel",
  {batchSize:10000, parallel:true}
);

// Batch create relationships
CALL apoc.periodic.iterate(
  "MATCH (source:SourceType), (target:TargetType)
   WHERE source.id = target.ref_id
   RETURN source, target",
  "CREATE (source)-[:RELATIONSHIP]->(target)",
  {batchSize:5000, parallel:false}
);
```

---

## Security Best Practices

### Access Control

```cypher
// Create read-only user
CREATE USER readonly SET PASSWORD 'secure_password' CHANGE NOT REQUIRED;
GRANT ROLE reader TO readonly;

// Create analyst user with limited write access
CREATE USER analyst SET PASSWORD 'secure_password' CHANGE NOT REQUIRED;
GRANT ROLE architect TO analyst;

// List all users
SHOW USERS;
```

### Network Security

```bash
# Restrict Neo4j to local access only
# Edit docker run command or docker-compose.yml:
# ports:
#   - "127.0.0.1:7474:7474"
#   - "127.0.0.1:7687:7687"

# Or use firewall rules
sudo ufw allow from 10.0.0.0/8 to any port 7687
sudo ufw deny 7687
```

### Audit Logging

```cypher
// Enable query logging
CALL dbms.setConfigValue('dbms.logs.query.enabled', 'true');
CALL dbms.setConfigValue('dbms.logs.query.threshold', '1s');

// View query log
// Check /logs/query.log in container
```

### Regular Security Tasks

```bash
# 1. Update passwords quarterly
# 2. Review user access monthly
# 3. Check for security updates weekly
# 4. Audit query logs monthly
# 5. Review backup integrity monthly
```

---

## Version History

- **v1.0.0 (2025-12-12)**: Initial administration guide
  - System overview and architecture
  - Backup and restore procedures
  - Monitoring and health checks
  - Maintenance procedures
  - Troubleshooting guide
  - Performance optimization
  - Security best practices

---

## Quick Reference Commands

```bash
# System Status
docker ps --filter "name=openspg-neo4j"
docker stats openspg-neo4j --no-stream

# Database Health
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "RETURN 1"

# Backup
/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/backup_neo4j.sh

# View Logs
docker logs openspg-neo4j --tail 100

# Database Metrics
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (n) RETURN count(n) as nodes"
```

---

## Support and Resources

- **Neo4j Documentation:** https://neo4j.com/docs/
- **Docker Documentation:** https://docs.docker.com/
- **Project Documentation:** `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/`
- **Backup Location:** `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/backups/`
- **Scripts Location:** `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/`

---

**Last Updated:** 2025-12-12
**Maintained By:** AEON Development Team
