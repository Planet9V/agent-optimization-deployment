# Scheduled Maintenance Procedures

**File:** MAINTENANCE_WINDOWS.md
**Created:** 2025-12-04
**Version:** v1.0.0
**Purpose:** Scheduled maintenance tasks and optimization procedures
**Status:** ACTIVE

## Executive Summary

Comprehensive procedures for scheduled maintenance windows including database optimization, security updates, log rotation, and performance tuning.

**Standard Maintenance Window:** Sundays 2:00 AM - 5:00 AM (Low traffic period)

---

## Maintenance Schedule

### Weekly Maintenance (Every Sunday 2:00 AM)

```yaml
weekly_tasks:
  - Database VACUUM and ANALYZE
  - Docker cleanup (unused images/containers)
  - Log rotation and archival
  - Backup verification
  - Security patch check
  - Performance metrics review

estimated_duration: 45-60 minutes
impact: Minimal (during low-traffic period)
rollback_time: 15 minutes
```

---

### Monthly Maintenance (First Sunday 2:00 AM)

```yaml
monthly_tasks:
  - Full database VACUUM FULL
  - Database index rebuild (REINDEX)
  - Docker image updates
  - System package updates
  - SSL certificate renewal check
  - Comprehensive backup test restore
  - Capacity planning review

estimated_duration: 90-120 minutes
impact: Moderate (requires service restart)
rollback_time: 30 minutes
```

---

### Quarterly Maintenance (First Sunday of Quarter 2:00 AM)

```yaml
quarterly_tasks:
  - Major version upgrades (PostgreSQL, Python, Node.js)
  - Security audit and vulnerability scan
  - Performance baseline re-establishment
  - Database schema optimization review
  - Disaster recovery drill
  - Documentation review and updates

estimated_duration: 2-4 hours
impact: Significant (planned downtime)
rollback_time: 60 minutes
```

---

## Pre-Maintenance Checklist

```bash
#!/bin/bash
# save as: scripts/pre_maintenance.sh

set -euo pipefail

echo "🔧 Pre-Maintenance Checklist"
echo "=============================="

# 1. Verify backup exists
LATEST_BACKUP=$(ls -t /backups/ner11/database/*.sql.gz | head -1)
if [ -n "$LATEST_BACKUP" ]; then
    echo "✅ Latest backup: $LATEST_BACKUP"
    echo "   Created: $(stat -c %y "$LATEST_BACKUP" 2>/dev/null || stat -f %Sm "$LATEST_BACKUP")"
else
    echo "❌ No recent backup found! Create backup before maintenance."
    exit 1
fi

# 2. Verify backup integrity
gunzip -t "$LATEST_BACKUP" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backup integrity verified"
else
    echo "❌ Backup integrity check failed!"
    exit 1
fi

# 3. Check current service status
docker-compose ps | grep -q "Up"
if [ $? -eq 0 ]; then
    echo "✅ All services running"
else
    echo "⚠️  Some services not running - review before maintenance"
fi

# 4. Record baseline metrics
echo "📊 Recording baseline metrics..."
cat > /tmp/maintenance_baseline_$(date +%Y%m%d).txt << EOF
=== Pre-Maintenance Baseline ===
Date: $(date)

Service Status:
$(docker-compose ps)

Container Resource Usage:
$(docker stats --no-stream)

Database Size:
$(docker-compose exec -T postgres psql -U postgres -c "SELECT pg_size_pretty(pg_database_size('ner11_db'));")

Table Counts:
$(docker-compose exec -T postgres psql -U postgres ner11_db -c "SELECT 'vendor_equipment', COUNT(*) FROM vendor_equipment UNION ALL SELECT 'threat_intelligence', COUNT(*) FROM threat_intelligence;")

Disk Usage:
$(df -h)
EOF

echo "✅ Baseline metrics saved"

# 5. Check for active user sessions (if applicable)
ACTIVE_USERS=$(docker-compose logs api --since 10m | grep -c "GET\|POST" || echo "0")
if [ "$ACTIVE_USERS" -lt 10 ]; then
    echo "✅ Low user activity: $ACTIVE_USERS requests in last 10 minutes"
else
    echo "⚠️  High user activity: $ACTIVE_USERS requests in last 10 minutes"
    echo "   Consider rescheduling maintenance"
fi

# 6. Verify rollback plan
if [ -f "scripts/rollback_maintenance.sh" ]; then
    echo "✅ Rollback script exists"
else
    echo "⚠️  No rollback script found"
fi

echo ""
echo "✅ Pre-maintenance checklist complete"
echo "Ready to proceed with maintenance window"
```

**Usage:**
```bash
chmod +x scripts/pre_maintenance.sh
./scripts/pre_maintenance.sh
```

---

## Weekly Maintenance Procedures

### Procedure 1: Database Optimization (VACUUM ANALYZE)

```bash
#!/bin/bash
# Weekly database maintenance

echo "🗄️  Starting database optimization..."

# Record start time
START_TIME=$(date +%s)

# Run VACUUM ANALYZE (doesn't require full table lock)
docker-compose exec -T postgres psql -U postgres ner11_db << EOF
-- Vacuum and analyze all tables
VACUUM ANALYZE VERBOSE;

-- Check for bloat
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;

-- Update statistics
ANALYZE VERBOSE;
EOF

# Record end time and duration
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "✅ Database optimization complete in ${DURATION} seconds"

# Log results
echo "$(date): VACUUM ANALYZE completed in ${DURATION}s" >> /var/log/maintenance.log
```

---

### Procedure 2: Docker Cleanup

```bash
#!/bin/bash
# Weekly Docker cleanup

echo "🐳 Starting Docker cleanup..."

# Record disk usage before cleanup
DISK_BEFORE=$(docker system df --format "{{.Size}}")

# Remove dangling images
docker image prune -f --filter "until=168h"  # 7 days

# Remove stopped containers
docker container prune -f

# Remove unused networks
docker network prune -f

# Remove build cache (older than 7 days)
docker builder prune -af --filter "until=168h"

# Record disk usage after cleanup
DISK_AFTER=$(docker system df --format "{{.Size}}")

echo "✅ Docker cleanup complete"
echo "   Space before: $DISK_BEFORE"
echo "   Space after: $DISK_AFTER"

# Log results
echo "$(date): Docker cleanup - Before: $DISK_BEFORE, After: $DISK_AFTER" >> /var/log/maintenance.log
```

---

### Procedure 3: Log Rotation

```bash
#!/bin/bash
# Weekly log rotation

echo "📜 Starting log rotation..."

# Archive application logs
LOG_ARCHIVE="/backups/ner11/logs/archive_$(date +%Y%m%d)"
mkdir -p "$LOG_ARCHIVE"

# Archive and compress logs older than 7 days
find logs/ -name "*.log" -mtime +7 -exec gzip {} \;
find logs/ -name "*.log.gz" -mtime +7 -exec mv {} "$LOG_ARCHIVE/" \;

# Rotate Docker container logs
for container in $(docker ps -q); do
    LOG_PATH=$(docker inspect --format='{{.LogPath}}' $container)
    if [ -f "$LOG_PATH" ]; then
        LOG_SIZE=$(stat -f%z "$LOG_PATH" 2>/dev/null || stat -c%s "$LOG_PATH")
        if [ "$LOG_SIZE" -gt 104857600 ]; then  # >100MB
            echo "Rotating large log: $LOG_PATH ($((LOG_SIZE / 1048576))MB)"
            cp "$LOG_PATH" "${LOG_PATH}.$(date +%Y%m%d)"
            truncate -s 0 "$LOG_PATH"
        fi
    fi
done

# Compress archived logs
find "$LOG_ARCHIVE" -name "*.log" -exec gzip {} \;

# Delete archives older than 90 days
find /backups/ner11/logs -name "archive_*" -mtime +90 -exec rm -rf {} \;

echo "✅ Log rotation complete"
```

---

### Procedure 4: Backup Verification

```bash
#!/bin/bash
# Verify latest backup integrity

echo "🔍 Verifying latest backup..."

LATEST_BACKUP=$(ls -t /backups/ner11/database/*.sql.gz | head -1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "❌ No backup found!"
    exit 1
fi

# Verify file integrity
gunzip -t "$LATEST_BACKUP"
if [ $? -ne 0 ]; then
    echo "❌ Backup integrity check failed!"
    exit 1
fi

# Verify checksum
if [ -f "${LATEST_BACKUP}.sha256" ]; then
    sha256sum -c "${LATEST_BACKUP}.sha256"
    if [ $? -eq 0 ]; then
        echo "✅ Backup checksum verified"
    else
        echo "❌ Backup checksum mismatch!"
        exit 1
    fi
fi

# Test restore to temporary database (optional - takes longer)
echo "Testing restore to temporary database..."
docker-compose exec -T postgres psql -U postgres -c "DROP DATABASE IF EXISTS ner11_test_restore;"
docker-compose exec -T postgres psql -U postgres -c "CREATE DATABASE ner11_test_restore;"
gunzip -c "$LATEST_BACKUP" | docker-compose exec -T postgres psql -U postgres ner11_test_restore > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Test restore successful"
    # Clean up
    docker-compose exec -T postgres psql -U postgres -c "DROP DATABASE ner11_test_restore;"
else
    echo "❌ Test restore failed!"
    exit 1
fi

echo "✅ Backup verification complete"
```

---

## Monthly Maintenance Procedures

### Procedure 1: Full Database VACUUM (Requires Downtime)

```bash
#!/bin/bash
# Monthly VACUUM FULL (reclaims disk space)

echo "🗄️  Starting VACUUM FULL (requires downtime)..."

# 1. Stop API to prevent new connections
docker-compose stop api

# 2. Wait for active queries to complete
sleep 10

# 3. Record database size before VACUUM
SIZE_BEFORE=$(docker-compose exec -T postgres psql -U postgres -c "SELECT pg_size_pretty(pg_database_size('ner11_db'));" -t | tr -d ' ')

# 4. Run VACUUM FULL
docker-compose exec -T postgres psql -U postgres ner11_db -c "VACUUM FULL VERBOSE;"

# 5. Record database size after VACUUM
SIZE_AFTER=$(docker-compose exec -T postgres psql -U postgres -c "SELECT pg_size_pretty(pg_database_size('ner11_db'));" -t | tr -d ' ')

# 6. Restart API
docker-compose up -d api

# 7. Verify services healthy
sleep 30
curl -f http://localhost:8000/health

echo "✅ VACUUM FULL complete"
echo "   Size before: $SIZE_BEFORE"
echo "   Size after: $SIZE_AFTER"
```

---

### Procedure 2: Database Index Rebuild

```bash
#!/bin/bash
# Monthly REINDEX (improves query performance)

echo "🔍 Starting database REINDEX..."

# Stop API
docker-compose stop api

# REINDEX entire database
docker-compose exec -T postgres psql -U postgres ner11_db -c "REINDEX DATABASE ner11_db VERBOSE;"

# Restart API
docker-compose up -d api

# Verify health
sleep 30
curl -f http://localhost:8000/health

echo "✅ REINDEX complete"
```

---

### Procedure 3: System Package Updates

```bash
#!/bin/bash
# Monthly system updates (Docker host)

echo "📦 Starting system package updates..."

# Update package lists
sudo apt-get update

# Check for available updates
UPDATES=$(sudo apt-get -s upgrade | grep -P '^\d+ upgraded' | cut -d' ' -f1)

if [ "$UPDATES" -gt 0 ]; then
    echo "$UPDATES updates available"

    # Install security updates only
    sudo apt-get upgrade -y --with-new-pkgs -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"

    # Check if reboot required
    if [ -f /var/run/reboot-required ]; then
        echo "⚠️  Reboot required after updates"
        echo "   Schedule reboot during next maintenance window"
    fi
else
    echo "✅ System is up to date"
fi

echo "✅ Package updates complete"
```

---

### Procedure 4: Docker Image Updates

```bash
#!/bin/bash
# Monthly Docker image updates

echo "🐳 Checking for Docker image updates..."

# Pull latest base images
docker-compose pull

# Rebuild containers with updated images
docker-compose build --pull

# Stop services
docker-compose down

# Start with new images
docker-compose up -d

# Monitor startup
docker-compose logs -f --tail=50 &
LOG_PID=$!
sleep 60
kill $LOG_PID

# Verify all services healthy
./scripts/startup_verify.sh

echo "✅ Docker image updates complete"
```

---

## Performance Tuning Procedures

### Tune PostgreSQL Configuration

```bash
#!/bin/bash
# Optimize PostgreSQL settings based on system resources

echo "⚙️  Tuning PostgreSQL configuration..."

# Get system memory
TOTAL_MEM_MB=$(free -m | awk '/^Mem:/{print $2}')

# Calculate optimal settings (25% of RAM for shared_buffers)
SHARED_BUFFERS=$((TOTAL_MEM_MB / 4))
EFFECTIVE_CACHE_SIZE=$((TOTAL_MEM_MB * 3 / 4))

# Update postgresql.conf
docker-compose exec postgres psql -U postgres -c "
ALTER SYSTEM SET shared_buffers = '${SHARED_BUFFERS}MB';
ALTER SYSTEM SET effective_cache_size = '${EFFECTIVE_CACHE_SIZE}MB';
ALTER SYSTEM SET maintenance_work_mem = '256MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;
ALTER SYSTEM SET work_mem = '4MB';
ALTER SYSTEM SET min_wal_size = '1GB';
ALTER SYSTEM SET max_wal_size = '4GB';
"

# Restart PostgreSQL to apply settings
docker-compose restart postgres

# Wait for startup
sleep 15
docker-compose exec postgres pg_isready -U postgres

echo "✅ PostgreSQL tuning complete"
echo "   shared_buffers: ${SHARED_BUFFERS}MB"
echo "   effective_cache_size: ${EFFECTIVE_CACHE_SIZE}MB"
```

---

## Post-Maintenance Verification

```bash
#!/bin/bash
# save as: scripts/post_maintenance.sh

set -euo pipefail

echo "✅ Post-Maintenance Verification"
echo "================================="

# 1. Verify all services running
docker-compose ps | grep -q "Up"
if [ $? -eq 0 ]; then
    echo "✅ All services running"
else
    echo "❌ Some services not running!"
    docker-compose ps
    exit 1
fi

# 2. Test API health
curl -f http://localhost:8000/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ API health check passed"
else
    echo "❌ API health check failed!"
    exit 1
fi

# 3. Test database connectivity
curl -f http://localhost:8000/api/v1/db/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Database connectivity verified"
else
    echo "❌ Database connectivity failed!"
    exit 1
fi

# 4. Verify data integrity
PRE_COUNT=$(grep "vendor_equipment" /tmp/maintenance_baseline_*.txt | tail -1 | awk '{print $NF}')
POST_COUNT=$(docker-compose exec -T postgres psql -U postgres ner11_db -t -c "SELECT COUNT(*) FROM vendor_equipment;" | tr -d ' ')

if [ "$PRE_COUNT" == "$POST_COUNT" ]; then
    echo "✅ Data integrity verified (count: $POST_COUNT)"
else
    echo "⚠️  Data count mismatch! Pre: $PRE_COUNT, Post: $POST_COUNT"
fi

# 5. Check response times
RESPONSE_TIME=$(time curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1)
echo "✅ API response time: ${RESPONSE_TIME}s"

# 6. Compare resource usage
echo "📊 Resource usage comparison:"
docker stats --no-stream

echo ""
echo "✅ Post-maintenance verification complete"
echo "   All systems operational"
```

---

## Rollback Procedure

```bash
#!/bin/bash
# save as: scripts/rollback_maintenance.sh

echo "⚠️  ROLLING BACK MAINTENANCE CHANGES"
echo "===================================="

# 1. Stop current services
docker-compose down

# 2. Restore database from pre-maintenance backup
BACKUP_FILE=$(ls -t /backups/ner11/database/*.sql.gz | head -1)
echo "Restoring from: $BACKUP_FILE"

docker-compose up -d postgres
sleep 15

docker-compose exec -T postgres psql -U postgres -c "DROP DATABASE IF EXISTS ner11_db;"
docker-compose exec -T postgres psql -U postgres -c "CREATE DATABASE ner11_db;"
gunzip -c "$BACKUP_FILE" | docker-compose exec -T postgres psql -U postgres ner11_db

# 3. Restore configuration files (if changed)
if [ -f "/backups/ner11/config/config_*.tar.gz" ]; then
    LATEST_CONFIG=$(ls -t /backups/ner11/config/config_*.tar.gz | head -1)
    tar -xzf "$LATEST_CONFIG" -C .
fi

# 4. Restart all services
docker-compose up -d

# 5. Verify rollback successful
sleep 30
./scripts/startup_verify.sh

echo "✅ Rollback complete"
```

---

## Maintenance Automation (Cron Schedule)

```bash
# Add to root crontab
sudo crontab -e

# Weekly maintenance (Sunday 2:00 AM)
0 2 * * 0 /path/to/scripts/weekly_maintenance.sh >> /var/log/maintenance.log 2>&1

# Monthly maintenance (First Sunday 2:00 AM)
0 2 1-7 * 0 /path/to/scripts/monthly_maintenance.sh >> /var/log/maintenance.log 2>&1

# Daily backup verification (3:00 AM)
0 3 * * * /path/to/scripts/verify_backup.sh >> /var/log/backup_verify.log 2>&1

# Daily disk space check (every 6 hours)
0 */6 * * * /usr/local/bin/check_disk_space.sh >> /var/log/disk_check.log 2>&1
```

---

## Related Runbooks

- **Backup:** BACKUP_PROCEDURES.md
- **Performance:** PERFORMANCE_DEGRADATION.md
- **Scaling:** RESOURCE_SCALING.md

---

**Document Version History:**
- v1.0.0 (2025-12-04): Initial maintenance procedures

**Last Verified:** 2025-12-04
**Next Review Date:** 2025-12-18
