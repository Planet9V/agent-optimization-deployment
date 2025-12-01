# OpenSPG Docker Volumes Guide

## 📦 Volume Architecture

OpenSPG uses **Docker named volumes** for persistent data storage across container restarts and updates.

### Volume Types

#### 1. **Shared Volume** (New!)
```yaml
shared-data → /shared  # Mounted in ALL containers
```
- **Purpose**: Cross-container data exchange
- **Access**: All 4 containers (openspg-server, mysql, neo4j, minio)
- **Use cases**:
  - Import/export data between services
  - Shared configuration files
  - Temporary processing files
  - Cross-service file exchange

#### 2. **Service-Specific Volumes**
```yaml
mysql-data → /var/lib/mysql          # MySQL database files
mysql-logs → /var/log/mysql          # MySQL logs
neo4j-data → /data                   # Neo4j graph database
neo4j-logs → /logs                   # Neo4j logs
neo4j-import → /var/lib/neo4j/import # Neo4j import directory
neo4j-plugins → /plugins             # Neo4j APOC plugins
minio-data → /data                   # MinIO object storage
openspg-logs → /app/logs             # OpenSPG application logs
```

---

## 🔄 Data Persistence

### How Persistence Works

All volumes are **Docker named volumes** with `local` driver:
```yaml
volumes:
  shared-data:
    driver: local
    name: openspg-shared-data
```

**Persistence Guarantees:**
- ✅ Data survives `docker-compose stop`
- ✅ Data survives `docker-compose restart`
- ✅ Data survives `docker-compose up -d` (container recreation)
- ✅ Data survives container crashes
- ❌ Data deleted ONLY with `docker-compose down -v` or manual volume deletion

### Volume Locations

Docker stores named volumes in:
```bash
# Linux
/var/lib/docker/volumes/openspg-*/

# macOS (Docker Desktop)
~/Library/Containers/com.docker.docker/Data/vms/0/volumes/openspg-*/

# Windows (WSL2)
\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\openspg-*\
```

---

## 🔍 Inspect Volumes

### List All OpenSPG Volumes
```bash
docker volume ls | grep openspg
```

**Expected output:**
```
local     openspg-shared-data
local     openspg-mysql-data
local     openspg-mysql-logs
local     openspg-neo4j-data
local     openspg-neo4j-logs
local     openspg-neo4j-import
local     openspg-neo4j-plugins
local     openspg-minio-data
local     openspg-server-logs
```

### Inspect Specific Volume
```bash
docker volume inspect openspg-neo4j-data
```

**Output shows:**
```json
[
    {
        "CreatedAt": "2025-01-26T20:00:00Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "openspg",
            "com.docker.compose.volume": "neo4j-data"
        },
        "Mountpoint": "/var/lib/docker/volumes/openspg-neo4j-data/_data",
        "Name": "openspg-neo4j-data",
        "Options": null,
        "Scope": "local"
    }
]
```

### Check Volume Size
```bash
docker run --rm -v openspg-neo4j-data:/data alpine du -sh /data
```

### Check All Volume Sizes
```bash
for vol in $(docker volume ls --format "{{.Name}}" | grep openspg); do
  size=$(docker run --rm -v $vol:/data alpine du -sh /data 2>/dev/null | cut -f1)
  echo "$vol: $size"
done
```

---

## 🔄 Using Shared Volume

### Access Shared Volume from Container

**From OpenSPG Server:**
```bash
docker exec openspg-server ls -la /shared
docker exec openspg-server touch /shared/test.txt
```

**From Neo4j:**
```bash
docker exec openspg-neo4j ls -la /shared
docker exec openspg-neo4j cat /shared/test.txt
```

**From MySQL:**
```bash
docker exec openspg-mysql ls -la /shared
```

**From MinIO:**
```bash
docker exec openspg-minio ls -la /shared
```

### Example: Share Data Between Containers

```bash
# 1. Write file from OpenSPG
docker exec openspg-server sh -c 'echo "Hello from OpenSPG" > /shared/message.txt'

# 2. Read from Neo4j
docker exec openspg-neo4j cat /shared/message.txt

# 3. Read from MySQL
docker exec openspg-mysql cat /shared/message.txt

# 4. Read from MinIO
docker exec openspg-minio cat /shared/message.txt
```

### Use Cases for Shared Volume

**1. Data Import/Export**
```bash
# Copy data to shared volume from host
docker cp mydata.csv openspg-server:/shared/

# Access from Neo4j import
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "LOAD CSV FROM 'file:///shared/mydata.csv' AS row ..."
```

**2. Backup Staging**
```bash
# Dump Neo4j to shared volume
docker exec openspg-neo4j neo4j-admin database dump neo4j --to-path=/shared

# Backup from shared volume to host
docker cp openspg-neo4j:/shared/neo4j.dump ./backups/
```

**3. Configuration Sharing**
```bash
# Place config in shared volume
docker cp config.yaml openspg-server:/shared/

# All containers can read it
docker exec openspg-mysql cat /shared/config.yaml
docker exec openspg-neo4j cat /shared/config.yaml
```

---

## 💾 Backup & Restore

### Backup Single Volume

```bash
# Backup Neo4j data
docker run --rm \
  -v openspg-neo4j-data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/neo4j-$(date +%Y%m%d).tar.gz /data

# Backup shared volume
docker run --rm \
  -v openspg-shared-data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/shared-$(date +%Y%m%d).tar.gz /data
```

### Backup All Volumes

```bash
#!/bin/bash
BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

for vol in $(docker volume ls --format "{{.Name}}" | grep openspg); do
  echo "Backing up $vol..."
  docker run --rm \
    -v $vol:/data \
    -v $(pwd)/$BACKUP_DIR:/backup \
    alpine tar czf /backup/${vol}.tar.gz /data
done

echo "Backup complete: $BACKUP_DIR"
```

### Restore Single Volume

```bash
# Stop services first
docker-compose stop

# Restore Neo4j data
docker run --rm \
  -v openspg-neo4j-data:/data \
  -v $(pwd)/backups:/backup \
  alpine sh -c "cd /data && tar xzf /backup/neo4j-20250126.tar.gz --strip 1"

# Restart services
docker-compose start
```

### Restore All Volumes

```bash
#!/bin/bash
BACKUP_DIR="./backups/20250126_120000"

# Stop services
docker-compose stop

# Restore each volume
for backup in $BACKUP_DIR/*.tar.gz; do
  vol=$(basename $backup .tar.gz)
  echo "Restoring $vol..."
  docker run --rm \
    -v $vol:/data \
    -v $(pwd)/$BACKUP_DIR:/backup \
    alpine sh -c "cd /data && tar xzf /backup/${vol}.tar.gz --strip 1"
done

# Restart services
docker-compose start
```

---

## 🗑️ Volume Management

### Remove Single Volume

```bash
# Stop services first
docker-compose stop

# Remove volume (⚠️ data loss!)
docker volume rm openspg-shared-data

# Recreate and restart
docker-compose up -d
```

### Remove All Volumes

```bash
# ⚠️ WARNING: Deletes ALL data!
docker-compose down -v
```

### Clean Unused Volumes

```bash
# Remove volumes not used by any container
docker volume prune

# Force removal without confirmation
docker volume prune -f
```

### Recreate Corrupted Volume

```bash
# 1. Stop container using the volume
docker-compose stop neo4j

# 2. Backup if possible
docker run --rm -v openspg-neo4j-data:/data -v $(pwd):/backup alpine tar czf /backup/neo4j-emergency.tar.gz /data

# 3. Remove corrupted volume
docker volume rm openspg-neo4j-data

# 4. Recreate volume (will be empty)
docker volume create openspg-neo4j-data

# 5. Restore from backup
docker run --rm -v openspg-neo4j-data:/data -v $(pwd):/backup alpine sh -c "cd /data && tar xzf /backup/neo4j-emergency.tar.gz --strip 1"

# 6. Restart service
docker-compose start neo4j
```

---

## 📊 Monitoring Volume Usage

### Disk Space by Volume

```bash
# Detailed size for each volume
for vol in $(docker volume ls --format "{{.Name}}" | grep openspg); do
  echo "=== $vol ==="
  docker run --rm -v $vol:/data alpine du -h -d 1 /data
  echo ""
done
```

### Total OpenSPG Storage

```bash
# Total size of all OpenSPG volumes
total=0
for vol in $(docker volume ls --format "{{.Name}}" | grep openspg); do
  size=$(docker run --rm -v $vol:/data alpine du -s /data 2>/dev/null | cut -f1)
  total=$((total + size))
done
echo "Total OpenSPG storage: $((total / 1024))MB"
```

### Real-Time Monitoring

```bash
# Watch volume sizes (updates every 2 seconds)
watch -n 2 'for vol in $(docker volume ls --format "{{.Name}}" | grep openspg); do size=$(docker run --rm -v $vol:/data alpine du -sh /data 2>/dev/null | cut -f1); echo "$vol: $size"; done'
```

---

## 🔒 Volume Security

### Permissions

Volumes inherit permissions from the container processes:
- **MySQL**: `mysql:mysql` (uid 999)
- **Neo4j**: `neo4j:neo4j` (uid 7474)
- **MinIO**: `minio-user` (uid 1000)
- **Shared**: Accessible by all (needs appropriate permissions)

### Set Shared Volume Permissions

```bash
# Make shared volume world-readable/writable
docker run --rm -v openspg-shared-data:/shared alpine chmod 777 /shared

# Or set specific ownership (example: neo4j)
docker run --rm -v openspg-shared-data:/shared alpine chown -R 7474:7474 /shared
```

---

## 📝 Volume Best Practices

### 1. **Regular Backups**
```bash
# Daily backups (add to crontab)
0 2 * * * /path/to/backup-volumes.sh
```

### 2. **Monitor Disk Usage**
```bash
# Alert when volume exceeds 80%
df -h | grep docker
```

### 3. **Use Shared Volume for Temporary Data**
- Don't store permanent data in /shared
- Clean up /shared periodically
- Use service-specific volumes for persistence

### 4. **Test Restores**
```bash
# Monthly restore test
docker-compose down
# Restore from backup
docker-compose up -d
# Verify data integrity
```

### 5. **Document Volume Usage**
- Keep track of what each volume stores
- Document backup frequencies
- Maintain restore procedures

---

## 🎯 Quick Reference

### Volume Mount Points

| Container | Shared | Service-Specific |
|-----------|--------|------------------|
| **openspg-server** | `/shared` | `/app/logs` |
| **mysql** | `/shared` | `/var/lib/mysql`, `/var/log/mysql` |
| **neo4j** | `/shared` | `/data`, `/logs`, `/import`, `/plugins` |
| **minio** | `/shared` | `/data` |

### Common Commands

```bash
# List volumes
docker volume ls | grep openspg

# Inspect volume
docker volume inspect openspg-shared-data

# Check size
docker run --rm -v openspg-shared-data:/data alpine du -sh /data

# Backup volume
docker run --rm -v openspg-shared-data:/data -v $(pwd):/backup alpine tar czf /backup/shared.tar.gz /data

# Restore volume
docker run --rm -v openspg-shared-data:/data -v $(pwd):/backup alpine sh -c "cd /data && tar xzf /backup/shared.tar.gz --strip 1"

# Remove volume
docker volume rm openspg-shared-data

# Clean unused
docker volume prune
```

---

## ✅ Verification

### Test Shared Volume

```bash
# Run verification script
./test-shared-volume.sh
```

Create `test-shared-volume.sh`:
```bash
#!/bin/bash
echo "Testing shared volume access..."

# Write from server
docker exec openspg-server sh -c 'echo "test" > /shared/test.txt'
echo "✓ Write from openspg-server"

# Read from neo4j
docker exec openspg-neo4j cat /shared/test.txt
echo "✓ Read from openspg-neo4j"

# Read from mysql
docker exec openspg-mysql cat /shared/test.txt
echo "✓ Read from openspg-mysql"

# Read from minio
docker exec openspg-minio cat /shared/test.txt
echo "✓ Read from openspg-minio"

# Cleanup
docker exec openspg-server rm /shared/test.txt
echo "✓ Cleanup successful"

echo ""
echo "Shared volume is working correctly!"
```

---

**Document Version:** 1.0.0
**Last Updated:** 2025-01-26
**Maintainer:** OpenSPG Community
