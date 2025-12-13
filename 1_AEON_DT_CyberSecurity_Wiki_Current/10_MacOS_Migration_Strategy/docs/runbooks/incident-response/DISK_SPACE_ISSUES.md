# Incident Response: Disk Space Issues

**File:** DISK_SPACE_ISSUES.md
**Created:** 2025-12-04
**Version:** v1.0.0
**Purpose:** Emergency disk space recovery and expansion procedures
**Status:** ACTIVE

## Incident Classification

**Severity:** CRITICAL (when <5% free)
**Response Time:** 10 minutes
**Escalation:** After 15 minutes if unresolved

---

## Symptoms

- Services failing to start with "No space left on device"
- Database write failures
- Log files can't be created
- Docker build failures
- System becoming unresponsive

---

## Immediate Response (Emergency Cleanup)

```bash
# IMMEDIATE: Check disk usage critical status
df -h | grep -E "9[0-9]%|100%"

# If any filesystem at 90%+, execute emergency cleanup immediately:

# 1. Stop log-heavy services temporarily
docker-compose logs > /tmp/current_logs_$(date +%Y%m%d_%H%M%S).log
docker-compose down

# 2. Emergency Docker cleanup (FAST - recovers most space quickly)
docker system prune -af --volumes
# WARNING: Removes all unused containers, networks, images, and volumes
# Typically recovers 50-80% of Docker disk usage

# 3. Remove old log files
find /var/log -type f -name "*.log" -mtime +7 -delete
find /var/log -type f -name "*.gz" -mtime +30 -delete

# 4. Clear system journal logs
sudo journalctl --vacuum-time=7d

# 5. Check space recovered
df -h

# 6. Restart services
docker-compose up -d
```

---

## Diagnostic Procedure

### Step 1: Identify Space Consumption

```bash
# Check all filesystem usage
df -h

# Expected output analysis:
# - Root (/) should be <80% used
# - /var should be <80% used
# - Docker volumes should be <80% used

# Find largest directories (top 10)
du -h / --max-depth=1 2>/dev/null | sort -rh | head -10

# Common space consumers:
# /var/lib/docker - Docker images and volumes
# /var/log - System and application logs
# /tmp - Temporary files
# /home - User data
```

---

### Step 2: Analyze Docker Space Usage

```bash
# Docker system disk usage breakdown
docker system df

# Expected output:
# TYPE            TOTAL   ACTIVE  SIZE      RECLAIMABLE
# Images          15      5       3.2GB     2.1GB (65%)
# Containers      8       3       1.2MB     800KB (66%)
# Local Volumes   10      3       5.6GB     3.2GB (57%)
# Build Cache     0       0       0B        0B

# Identify unused images
docker images -f "dangling=true"

# Identify stopped containers
docker ps -a -f status=exited

# Identify unused volumes
docker volume ls -f dangling=true
```

---

### Step 3: Analyze Log Files

```bash
# Find largest log files
find /var/log -type f -exec du -h {} + | sort -rh | head -20

# Check Docker container logs size
du -sh /var/lib/docker/containers/*/*-json.log | sort -rh | head -10

# Check application logs
du -sh logs/

# Check system journal size
journalctl --disk-usage
```

---

### Step 4: Analyze Database Size

```bash
# Check PostgreSQL data directory size
docker-compose exec postgres du -sh /var/lib/postgresql/data

# Check individual database sizes
docker-compose exec postgres psql -U postgres -c "
SELECT
  datname,
  pg_size_pretty(pg_database_size(datname)) AS size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;
"

# Check table sizes
docker-compose exec postgres psql -U postgres ner11_db -c "
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
  pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS index_size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

---

## Cleanup Procedures

### Cleanup 1: Safe Docker Cleanup (Preserves Running Services)

```bash
# Remove unused images (not referenced by containers)
docker image prune -a --filter "until=72h"
# This removes images older than 3 days that aren't in use

# Remove stopped containers
docker container prune
# Removes all stopped containers

# Remove unused volumes (⚠️  WARNING: May delete data if volumes orphaned)
docker volume prune
# ONLY run if you've verified volumes aren't needed

# Remove unused networks
docker network prune

# Check space recovered
docker system df
df -h
```

---

### Cleanup 2: Aggressive Docker Cleanup (Stops Services)

```bash
# ⚠️  WARNING: This will stop all services and remove everything unused

# 1. Backup critical data first
./scripts/backup_database.sh
./scripts/backup_models.sh

# 2. Stop services
docker-compose down

# 3. Remove ALL unused Docker resources
docker system prune -af --volumes

# 4. Rebuild and restart
docker-compose build --no-cache
docker-compose up -d

# 5. Verify services healthy
./scripts/startup_verify.sh

# Space typically recovered: 50-80%
```

---

### Cleanup 3: Log File Cleanup

```bash
# Archive old logs before deletion
mkdir -p /backups/logs/archive_$(date +%Y%m%d)
find /var/log -name "*.log" -mtime +7 -exec cp {} /backups/logs/archive_$(date +%Y%m%d)/ \;

# Delete old log files
find /var/log -name "*.log" -mtime +30 -delete
find /var/log -name "*.gz" -mtime +60 -delete

# Truncate large log files (preserves file but clears content)
find /var/log -name "*.log" -size +100M -exec truncate -s 0 {} \;

# Rotate Docker container logs
for container in $(docker ps -q); do
    docker inspect --format='{{.LogPath}}' $container | xargs truncate -s 0
done

# Clear system journal
sudo journalctl --vacuum-time=14d
sudo journalctl --vacuum-size=500M

# Check space recovered
df -h /var/log
```

---

### Cleanup 4: Database Cleanup (VACUUM)

```bash
# Stop API to prevent new writes during VACUUM
docker-compose stop api

# Run VACUUM FULL (reclaims space but requires downtime)
docker-compose exec postgres psql -U postgres ner11_db -c "VACUUM FULL VERBOSE;"

# Alternative: VACUUM without FULL (faster, less space recovered)
docker-compose exec postgres psql -U postgres ner11_db -c "VACUUM VERBOSE;"

# Reindex to improve performance
docker-compose exec postgres psql -U postgres ner11_db -c "REINDEX DATABASE ner11_db;"

# Check space recovered
docker-compose exec postgres du -sh /var/lib/postgresql/data

# Restart API
docker-compose up -d api
```

---

### Cleanup 5: Temporary Files

```bash
# Clear system temporary files
sudo rm -rf /tmp/*
sudo rm -rf /var/tmp/*

# Clear user cache (npm, pip, etc.)
rm -rf ~/.cache/*
rm -rf ~/.npm/_cacache
rm -rf ~/.local/share/virtualenvs/*/lib/python*/site-packages/*.dist-info

# Clear Docker build cache
docker builder prune -af

# Check space recovered
df -h /tmp /var/tmp
```

---

## Growth Investigation

### Identify What Caused Growth

```bash
# Find files created in last 24 hours (growth pattern)
find / -type f -mtime -1 -exec du -h {} + 2>/dev/null | sort -rh | head -20

# Find rapidly growing files
#!/bin/bash
for file in $(find /var/log -type f -name "*.log"); do
    size1=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file")
    sleep 60
    size2=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file")
    growth=$((size2 - size1))
    if [ $growth -gt 1048576 ]; then  # >1MB/minute
        echo "$file: Growing at $(($growth / 1048576))MB/min"
    fi
done

# Check Docker image layer sizes
docker history ner11_api_1 --human --format "{{.Size}}\t{{.CreatedBy}}" | sort -rh | head -10

# Identify database table growth
docker-compose exec postgres psql -U postgres ner11_db -c "
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
  (SELECT count(*) FROM information_schema.columns WHERE table_name = tablename) AS column_count
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

---

## Expansion Procedures

### Expand Docker Volume (PostgreSQL Data)

```bash
# Method 1: Create new larger volume and migrate

# 1. Stop services
docker-compose down

# 2. Backup current data
docker run --rm \
    -v ner11_postgres_data:/source:ro \
    -v /backups:/backup \
    alpine \
    tar -czf /backup/postgres_data_$(date +%Y%m%d).tar.gz -C /source .

# 3. Create new larger volume
docker volume create ner11_postgres_data_new --opt size=20GB

# 4. Copy data to new volume
docker run --rm \
    -v ner11_postgres_data:/source:ro \
    -v ner11_postgres_data_new:/target \
    alpine \
    sh -c "cp -a /source/. /target/"

# 5. Update docker-compose.yml to use new volume
# Edit docker-compose.yml: Replace ner11_postgres_data with ner11_postgres_data_new

# 6. Restart services
docker-compose up -d

# 7. Verify data intact
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM vendor_equipment;"

# 8. Remove old volume after verification
# docker volume rm ner11_postgres_data
```

---

### Expand System Disk (Cloud/VM)

```bash
# AWS/Azure/GCP: Resize disk through cloud console first, then:

# 1. Check current disk size
lsblk

# 2. Resize partition (example for /dev/sda1)
sudo growpart /dev/sda 1

# 3. Resize filesystem
# For ext4:
sudo resize2fs /dev/sda1

# For XFS:
sudo xfs_growfs /

# 4. Verify expansion
df -h
```

---

## Prevention Measures

### Automated Cleanup Cron Jobs

```bash
# Add to crontab
crontab -e

# Weekly Docker cleanup (Sundays at 2 AM)
0 2 * * 0 docker system prune -af --filter "until=168h" >> /var/log/docker_cleanup.log 2>&1

# Daily log rotation (2 AM)
0 2 * * * find /var/log -name "*.log" -mtime +7 -exec gzip {} \; >> /var/log/log_rotation.log 2>&1

# Daily old log deletion (3 AM)
0 3 * * * find /var/log -name "*.gz" -mtime +30 -delete

# Weekly database VACUUM (Sundays at 3 AM)
0 3 * * 0 docker-compose exec -T postgres psql -U postgres ner11_db -c "VACUUM ANALYZE;" >> /var/log/postgres_vacuum.log 2>&1
```

---

### Docker Log Rotation Configuration

**Configure in docker-compose.yml:**

```yaml
services:
  api:
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"

  postgres:
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "5"

  frontend:
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"
```

---

### Monitoring and Alerting

```bash
# Add disk space monitoring script
cat > /usr/local/bin/check_disk_space.sh << 'EOF'
#!/bin/bash
THRESHOLD=80
CRITICAL=90

df -h | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{print $5 " " $6}' | while read output; do
    usage=$(echo $output | awk '{print $1}' | sed 's/%//')
    partition=$(echo $output | awk '{print $2}')

    if [ $usage -ge $CRITICAL ]; then
        echo "CRITICAL: Disk usage on $partition is ${usage}%"
        # Send alert
        echo "Disk ${usage}% on $partition" | mail -s "CRITICAL Disk Alert" admin@example.com
    elif [ $usage -ge $THRESHOLD ]; then
        echo "WARNING: Disk usage on $partition is ${usage}%"
        echo "Disk ${usage}% on $partition" | mail -s "Disk Warning" admin@example.com
    fi
done
EOF

chmod +x /usr/local/bin/check_disk_space.sh

# Add to cron (check every 5 minutes)
crontab -e
# Add: */5 * * * * /usr/local/bin/check_disk_space.sh
```

---

### Capacity Planning

```bash
# Track disk growth rate
#!/bin/bash
# save as: scripts/track_disk_growth.sh

METRICS_FILE="/var/log/disk_metrics.csv"

# Record current usage
TIMESTAMP=$(date +%Y-%m-%d_%H:%M:%S)
USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
AVAILABLE=$(df -h / | tail -1 | awk '{print $4}')

echo "$TIMESTAMP,$USAGE,$AVAILABLE" >> $METRICS_FILE

# Calculate growth trend (30-day average)
if [ $(wc -l < $METRICS_FILE) -gt 30 ]; then
    echo "30-day disk usage trend:"
    tail -30 $METRICS_FILE | awk -F',' '{sum+=$2} END {print "Average: " sum/NR "%"}'
fi

# Add to cron: 0 0 * * * /path/to/track_disk_growth.sh
```

---

## Quick Reference Commands

```bash
# Check disk usage
df -h

# Emergency cleanup (FAST)
docker system prune -af --volumes

# Find largest directories
du -h / --max-depth=1 2>/dev/null | sort -rh | head -10

# Clean logs
find /var/log -name "*.log" -mtime +7 -delete

# VACUUM database
docker-compose exec postgres psql -U postgres ner11_db -c "VACUUM FULL;"

# Check Docker disk usage
docker system df

# Clear Docker build cache
docker builder prune -af

# Truncate large logs
truncate -s 0 /var/log/large_file.log
```

---

## Related Runbooks

- **Performance:** PERFORMANCE_DEGRADATION.md
- **Database:** DATABASE_CONNECTION_ISSUES.md
- **Maintenance:** MAINTENANCE_WINDOWS.md

---

**Document Version History:**
- v1.0.0 (2025-12-04): Initial disk space procedures

**Last Verified:** 2025-12-04
**Next Review Date:** 2025-12-18
