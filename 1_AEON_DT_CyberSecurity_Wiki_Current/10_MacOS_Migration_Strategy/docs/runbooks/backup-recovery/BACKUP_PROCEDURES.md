# Backup and Recovery Procedures

**File:** BACKUP_PROCEDURES.md
**Created:** 2025-12-04
**Version:** v1.0.0
**Purpose:** Comprehensive backup and recovery procedures
**Status:** ACTIVE

## Executive Summary

Complete procedures for automated daily backups, manual backup creation, restoration procedures, and backup verification for database, models, code, and configuration.

**Retention Policy:**
- Daily backups: 7 days
- Weekly backups: 4 weeks
- Monthly backups: 12 months
- Critical backups: Indefinite

---

## Backup Strategy Overview

```
┌─────────────────────────────────────────────────┐
│                BACKUP COMPONENTS                │
├─────────────────────────────────────────────────┤
│ 1. Database (PostgreSQL)      - Daily, Weekly   │
│ 2. ML Models & Weights        - After training  │
│ 3. Code Repository (Git)      - Continuous      │
│ 4. Configuration Files        - On change       │
│ 5. Docker Volumes             - Daily           │
│ 6. Application Logs           - Weekly          │
└─────────────────────────────────────────────────┘
```

**Backup Storage Locations:**
- Local: `/backups/ner11/` (7-day retention)
- Remote: AWS S3 / Azure Blob (long-term retention)
- Offsite: External drive mounted at `/mnt/backup_drive/`

---

## 1. Database Backup Procedures

### Daily Automated Database Backup

**Automated Script:** `scripts/backup_database.sh`

```bash
#!/bin/bash
# save as: scripts/backup_database.sh

set -euo pipefail

# Configuration
BACKUP_DIR="/backups/ner11/database"
RETENTION_DAYS=7
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="ner11_db_${TIMESTAMP}.sql.gz"
DB_NAME="ner11_db"
DB_USER="postgres"

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "🗄️  Starting database backup: $BACKUP_FILE"

# Create compressed backup using pg_dump
docker-compose exec -T postgres pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_DIR/$BACKUP_FILE"

# Verify backup file created and not empty
if [ -s "$BACKUP_DIR/$BACKUP_FILE" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
    echo "✅ Backup created successfully: $BACKUP_SIZE"

    # Calculate checksum for integrity verification
    SHA256=$(sha256sum "$BACKUP_DIR/$BACKUP_FILE" | cut -d' ' -f1)
    echo "$SHA256  $BACKUP_FILE" > "$BACKUP_DIR/${BACKUP_FILE}.sha256"
    echo "🔐 Checksum: $SHA256"
else
    echo "❌ Backup failed: file is empty or missing"
    exit 1
fi

# Test backup integrity by attempting to extract
echo "🔍 Verifying backup integrity..."
gunzip -t "$BACKUP_DIR/$BACKUP_FILE"
if [ $? -eq 0 ]; then
    echo "✅ Backup integrity verified"
else
    echo "❌ Backup integrity check failed"
    exit 1
fi

# Clean up old backups (keep last 7 days)
echo "🧹 Cleaning up old backups (keeping last $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "ner11_db_*.sql.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "ner11_db_*.sha256" -mtime +$RETENTION_DAYS -delete

# List current backups
echo "📦 Current backups:"
ls -lh "$BACKUP_DIR" | grep -E "\.sql\.gz$|\.sha256$"

# Optional: Upload to remote storage
if [ -n "${AWS_S3_BUCKET:-}" ]; then
    echo "☁️  Uploading to S3..."
    aws s3 cp "$BACKUP_DIR/$BACKUP_FILE" "s3://$AWS_S3_BUCKET/ner11/database/"
    aws s3 cp "$BACKUP_DIR/${BACKUP_FILE}.sha256" "s3://$AWS_S3_BUCKET/ner11/database/"
    echo "✅ Uploaded to S3"
fi

echo "✅ Database backup complete: $BACKUP_FILE"
```

**Setup Automated Daily Backup:**

```bash
# Make script executable
chmod +x scripts/backup_database.sh

# Add to crontab (runs daily at 2 AM)
crontab -e

# Add this line:
0 2 * * * /path/to/project/scripts/backup_database.sh >> /var/log/ner11_backup.log 2>&1
```

---

### Manual Database Backup (On-Demand)

```bash
# Full database backup
docker-compose exec -T postgres pg_dump -U postgres ner11_db > /backups/ner11/database/manual_backup_$(date +%Y%m%d_%H%M%S).sql

# Compressed backup (recommended)
docker-compose exec -T postgres pg_dump -U postgres ner11_db | gzip > /backups/ner11/database/manual_backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Backup specific table only
docker-compose exec -T postgres pg_dump -U postgres -t vendor_equipment ner11_db | gzip > /backups/ner11/database/vendor_equipment_$(date +%Y%m%d_%H%M%S).sql.gz

# Backup with custom format (faster restore, allows selective restore)
docker-compose exec -T postgres pg_dump -U postgres -Fc ner11_db > /backups/ner11/database/manual_backup_$(date +%Y%m%d_%H%M%S).dump
```

---

### Database Backup Verification

```bash
# Verify backup file integrity
gunzip -t /backups/ner11/database/ner11_db_20251204_020000.sql.gz
# Expected: No errors (silent success)

# Check backup file size (should be >1MB for populated database)
ls -lh /backups/ner11/database/ner11_db_20251204_020000.sql.gz
# Expected: Size in megabytes

# Verify checksum
sha256sum -c /backups/ner11/database/ner11_db_20251204_020000.sql.gz.sha256
# Expected: "ner11_db_20251204_020000.sql.gz: OK"

# Test restore to temporary database (advanced verification)
docker-compose exec -T postgres psql -U postgres -c "CREATE DATABASE ner11_test_restore;"
gunzip -c /backups/ner11/database/ner11_db_20251204_020000.sql.gz | docker-compose exec -T postgres psql -U postgres ner11_test_restore

# Verify row counts match
docker-compose exec postgres psql -U postgres -c "SELECT COUNT(*) FROM ner11_test_restore.vendor_equipment;"
# Compare with production count

# Clean up test database
docker-compose exec postgres psql -U postgres -c "DROP DATABASE ner11_test_restore;"
```

---

## 2. Database Restoration Procedures

### Full Database Restore

```bash
# ⚠️  WARNING: This will REPLACE the entire database

# Step 1: Stop API to prevent new connections
docker-compose stop api

# Step 2: Terminate existing connections
docker-compose exec postgres psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'ner11_db' AND pid <> pg_backend_pid();"

# Step 3: Drop existing database
docker-compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS ner11_db;"

# Step 4: Create fresh database
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE ner11_db OWNER postgres;"

# Step 5: Restore from backup
gunzip -c /backups/ner11/database/ner11_db_20251204_020000.sql.gz | docker-compose exec -T postgres psql -U postgres ner11_db

# Step 6: Verify restoration
docker-compose exec postgres psql -U postgres ner11_db -c "SELECT COUNT(*) FROM vendor_equipment;"
# Expected: Row count matching pre-backup state

# Step 7: Restart API
docker-compose up -d api

# Step 8: Verify API database connectivity
sleep 10
curl -X GET http://localhost:8000/api/v1/db/health
# Expected: {"database": "connected"}
```

---

### Selective Table Restore

```bash
# Restore single table without affecting others
# Extract table from backup
gunzip -c /backups/ner11/database/ner11_db_20251204_020000.sql.gz | grep -A 10000 "CREATE TABLE vendor_equipment" > /tmp/vendor_equipment_restore.sql

# Truncate existing table (keeps schema)
docker-compose exec postgres psql -U postgres ner11_db -c "TRUNCATE TABLE vendor_equipment CASCADE;"

# Restore table data
cat /tmp/vendor_equipment_restore.sql | docker-compose exec -T postgres psql -U postgres ner11_db

# Verify
docker-compose exec postgres psql -U postgres ner11_db -c "SELECT COUNT(*) FROM vendor_equipment;"

# Clean up temp file
rm /tmp/vendor_equipment_restore.sql
```

---

## 3. ML Model Backup and Versioning

### Model Backup Script

```bash
#!/bin/bash
# save as: scripts/backup_models.sh

set -euo pipefail

MODEL_DIR="/app/models"
BACKUP_DIR="/backups/ner11/models"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

echo "🧠 Backing up ML models..."

# Backup all model files with metadata
tar -czf "$BACKUP_DIR/models_${TIMESTAMP}.tar.gz" \
    -C "$MODEL_DIR" . \
    --exclude='*.pyc' \
    --exclude='__pycache__'

# Create model manifest
docker-compose exec -T api python -c "
import json
import os
from pathlib import Path

models = []
model_dir = Path('/app/models')
for model_file in model_dir.rglob('*.pkl'):
    stat = model_file.stat()
    models.append({
        'name': str(model_file.relative_to(model_dir)),
        'size': stat.st_size,
        'modified': stat.st_mtime
    })

manifest = {
    'timestamp': '$TIMESTAMP',
    'models': models
}

print(json.dumps(manifest, indent=2))
" > "$BACKUP_DIR/models_${TIMESTAMP}_manifest.json"

# Calculate checksum
sha256sum "$BACKUP_DIR/models_${TIMESTAMP}.tar.gz" > "$BACKUP_DIR/models_${TIMESTAMP}.sha256"

echo "✅ Model backup complete: models_${TIMESTAMP}.tar.gz"
ls -lh "$BACKUP_DIR/models_${TIMESTAMP}.tar.gz"
```

**Usage:**
```bash
chmod +x scripts/backup_models.sh
./scripts/backup_models.sh
```

---

### Model Restoration

```bash
# List available model backups
ls -lh /backups/ner11/models/

# Verify backup integrity
sha256sum -c /backups/ner11/models/models_20251204_100000.sha256

# Stop API before restoration
docker-compose stop api

# Restore models
tar -xzf /backups/ner11/models/models_20251204_100000.tar.gz -C /app/models/

# Verify restoration using manifest
cat /backups/ner11/models/models_20251204_100000_manifest.json

# Restart API and verify model loading
docker-compose up -d api
sleep 20
curl -X GET http://localhost:8000/api/v1/models/status
# Expected: {"models_loaded": true}
```

---

## 4. Code Repository Backup

### Git Repository Verification

```bash
# Verify remote repository is up-to-date
cd /path/to/project
git remote -v
git fetch --all

# Check for uncommitted changes
git status
# Expected: "nothing to commit, working tree clean"

# Verify last push
git log origin/main..HEAD
# Expected: Empty (all commits pushed)

# Create local bundle backup (for offline storage)
git bundle create /backups/ner11/git/ner11_repo_$(date +%Y%m%d).bundle --all

# Verify bundle
git bundle verify /backups/ner11/git/ner11_repo_$(date +%Y%m%d).bundle
# Expected: "The bundle records a complete history"
```

---

### Code Restoration from Bundle

```bash
# Clone from bundle backup
git clone /backups/ner11/git/ner11_repo_20251204.bundle restored_repo
cd restored_repo

# Verify integrity
git log --oneline | head -10
git fsck --full
# Expected: No errors
```

---

## 5. Configuration Files Backup

### Backup Docker Compose and Environment Files

```bash
#!/bin/bash
# save as: scripts/backup_config.sh

BACKUP_DIR="/backups/ner11/config"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

echo "⚙️  Backing up configuration files..."

# Create config backup archive
tar -czf "$BACKUP_DIR/config_${TIMESTAMP}.tar.gz" \
    docker-compose.yml \
    .env \
    api/config.py \
    frontend/package.json \
    scripts/ \
    --exclude='node_modules' \
    --exclude='__pycache__'

# Create config manifest
cat > "$BACKUP_DIR/config_${TIMESTAMP}_manifest.txt" << EOF
Backup Date: $(date)
Files Backed Up:
- docker-compose.yml
- .env (environment variables)
- api/config.py
- frontend/package.json
- scripts/
EOF

echo "✅ Configuration backup complete"
ls -lh "$BACKUP_DIR/config_${TIMESTAMP}.tar.gz"
```

---

## 6. Docker Volumes Backup

### Backup All Docker Volumes

```bash
#!/bin/bash
# save as: scripts/backup_volumes.sh

BACKUP_DIR="/backups/ner11/volumes"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

echo "💾 Backing up Docker volumes..."

# Get list of volumes
VOLUMES=$(docker volume ls -q | grep ner11)

for VOLUME in $VOLUMES; do
    echo "Backing up volume: $VOLUME"

    # Create backup using temporary container
    docker run --rm \
        -v "$VOLUME:/source:ro" \
        -v "$BACKUP_DIR:/backup" \
        alpine \
        tar -czf "/backup/${VOLUME}_${TIMESTAMP}.tar.gz" -C /source .

    # Verify backup
    if [ -s "$BACKUP_DIR/${VOLUME}_${TIMESTAMP}.tar.gz" ]; then
        echo "✅ $VOLUME backed up successfully"
    else
        echo "❌ $VOLUME backup failed"
    fi
done

echo "✅ All volumes backed up"
ls -lh "$BACKUP_DIR/"
```

---

### Restore Docker Volume

```bash
# List available volume backups
ls -lh /backups/ner11/volumes/

# Stop services using the volume
docker-compose down

# Remove existing volume
docker volume rm ner11_postgres_data

# Recreate volume
docker volume create ner11_postgres_data

# Restore from backup
docker run --rm \
    -v ner11_postgres_data:/target \
    -v /backups/ner11/volumes:/backup \
    alpine \
    tar -xzf /backup/ner11_postgres_data_20251204_020000.tar.gz -C /target

# Restart services
docker-compose up -d

# Verify restoration
docker-compose exec postgres psql -U postgres -c "SELECT COUNT(*) FROM vendor_equipment;"
```

---

## 7. Complete System Backup (All Components)

### Full System Backup Script

```bash
#!/bin/bash
# save as: scripts/backup_full_system.sh

set -euo pipefail

BACKUP_ROOT="/backups/ner11"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$BACKUP_ROOT/full_system_$TIMESTAMP"

mkdir -p "$BACKUP_DIR"

echo "🚀 Starting full system backup..."

# 1. Database
echo "1/5 Backing up database..."
./scripts/backup_database.sh
cp /backups/ner11/database/ner11_db_*.sql.gz "$BACKUP_DIR/" | tail -1

# 2. ML Models
echo "2/5 Backing up ML models..."
./scripts/backup_models.sh
cp /backups/ner11/models/models_*.tar.gz "$BACKUP_DIR/" | tail -1

# 3. Configuration
echo "3/5 Backing up configuration..."
./scripts/backup_config.sh
cp /backups/ner11/config/config_*.tar.gz "$BACKUP_DIR/" | tail -1

# 4. Docker Volumes
echo "4/5 Backing up Docker volumes..."
./scripts/backup_volumes.sh
cp /backups/ner11/volumes/*.tar.gz "$BACKUP_DIR/"

# 5. Git Repository
echo "5/5 Backing up Git repository..."
git bundle create "$BACKUP_DIR/git_repo.bundle" --all

# Create backup manifest
cat > "$BACKUP_DIR/MANIFEST.txt" << EOF
NER11 Gold Model - Full System Backup
=====================================
Backup Date: $(date)
Backup Directory: $BACKUP_DIR

Components Backed Up:
---------------------
✅ PostgreSQL Database
✅ ML Models & Weights
✅ Configuration Files
✅ Docker Volumes
✅ Git Repository

Restoration Instructions:
------------------------
See docs/runbooks/backup-recovery/BACKUP_PROCEDURES.md

Verification Commands:
---------------------
sha256sum -c checksums.txt
EOF

# Generate checksums for all backup files
cd "$BACKUP_DIR"
sha256sum *.gz *.bundle > checksums.txt

# Create compressed archive of full backup
cd "$BACKUP_ROOT"
tar -czf "full_system_${TIMESTAMP}.tar.gz" "full_system_${TIMESTAMP}/"

echo "✅ Full system backup complete!"
echo "📦 Backup location: $BACKUP_ROOT/full_system_${TIMESTAMP}.tar.gz"
ls -lh "$BACKUP_ROOT/full_system_${TIMESTAMP}.tar.gz"
```

---

## 8. Backup Monitoring and Verification

### Automated Backup Verification Script

```bash
#!/bin/bash
# save as: scripts/verify_backups.sh

set -euo pipefail

BACKUP_DIR="/backups/ner11"
TODAY=$(date +%Y%m%d)

echo "🔍 Verifying backups..."

# Check database backup exists for today
DB_BACKUP=$(find "$BACKUP_DIR/database" -name "ner11_db_${TODAY}*.sql.gz" | head -1)
if [ -n "$DB_BACKUP" ]; then
    echo "✅ Database backup found: $DB_BACKUP"

    # Verify integrity
    gunzip -t "$DB_BACKUP" 2>/dev/null && echo "   ✅ Integrity OK" || echo "   ❌ Integrity FAILED"

    # Verify checksum
    sha256sum -c "${DB_BACKUP}.sha256" 2>/dev/null && echo "   ✅ Checksum OK" || echo "   ❌ Checksum FAILED"
else
    echo "❌ No database backup found for today!"
fi

# Check backup sizes (detect anomalies)
DB_SIZE=$(du -h "$DB_BACKUP" 2>/dev/null | cut -f1)
echo "   Size: $DB_SIZE"

# Alert if backup size is unusually small (<1MB could indicate problem)
DB_SIZE_BYTES=$(stat -f%z "$DB_BACKUP" 2>/dev/null || stat -c%s "$DB_BACKUP")
if [ "$DB_SIZE_BYTES" -lt 1048576 ]; then
    echo "   ⚠️  WARNING: Backup size unusually small!"
fi

echo "✅ Backup verification complete"
```

**Add to cron for daily verification:**
```bash
crontab -e
# Add: 0 3 * * * /path/to/scripts/verify_backups.sh >> /var/log/ner11_backup_verify.log 2>&1
```

---

## 9. Disaster Recovery Procedure

### Complete System Restoration from Full Backup

```bash
#!/bin/bash
# DISASTER RECOVERY - Use only when full system restoration needed

set -euo pipefail

BACKUP_FILE="/backups/ner11/full_system_20251204_020000.tar.gz"

echo "🚨 Starting disaster recovery..."

# 1. Extract full backup
tar -xzf "$BACKUP_FILE" -C /tmp/

BACKUP_DIR="/tmp/full_system_20251204_020000"

# 2. Verify checksums
cd "$BACKUP_DIR"
sha256sum -c checksums.txt
if [ $? -ne 0 ]; then
    echo "❌ Checksum verification failed! Backup may be corrupted."
    exit 1
fi

# 3. Stop all services
docker-compose down -v

# 4. Restore Git repository
git clone "$BACKUP_DIR/git_repo.bundle" /path/to/restored_project
cd /path/to/restored_project

# 5. Restore configuration
tar -xzf "$BACKUP_DIR/config_*.tar.gz" -C .

# 6. Restore Docker volumes
docker volume create ner11_postgres_data
docker run --rm \
    -v ner11_postgres_data:/target \
    -v "$BACKUP_DIR:/backup" \
    alpine \
    tar -xzf /backup/ner11_postgres_data_*.tar.gz -C /target

# 7. Start database first
docker-compose up -d postgres
sleep 30

# 8. Restore database
gunzip -c "$BACKUP_DIR/ner11_db_*.sql.gz" | docker-compose exec -T postgres psql -U postgres ner11_db

# 9. Restore ML models
tar -xzf "$BACKUP_DIR/models_*.tar.gz" -C /app/models/

# 10. Start all services
docker-compose up -d

# 11. Verify system
sleep 30
./scripts/startup_verify.sh

echo "✅ Disaster recovery complete!"
```

---

## Backup Schedule Summary

| Component          | Frequency | Retention | Storage Location          |
|--------------------|-----------|-----------|---------------------------|
| Database           | Daily 2AM | 7 days    | Local + S3                |
| ML Models          | On train  | 30 days   | Local + S3                |
| Configuration      | On change | 30 days   | Local + Git               |
| Docker Volumes     | Daily 3AM | 7 days    | Local                     |
| Full System        | Weekly    | 4 weeks   | Local + Offsite           |
| Git Repository     | Continuous| Indefinite| GitHub + Local bundle     |

---

## Related Runbooks

- **Startup:** docs/runbooks/daily/STARTUP_PROCEDURE.md
- **Service Management:** docs/runbooks/service-management/SERVICE_CONTROL.md
- **Disaster Recovery:** docs/runbooks/incident-response/DATA_CORRUPTION.md

---

**Document Version History:**
- v1.0.0 (2025-12-04): Initial backup and recovery procedures

**Last Verified:** 2025-12-04
**Next Review Date:** 2025-12-18
