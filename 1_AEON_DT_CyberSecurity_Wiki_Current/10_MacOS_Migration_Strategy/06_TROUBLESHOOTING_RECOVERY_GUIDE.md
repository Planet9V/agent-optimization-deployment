# AEON Digital Twin macOS Migration - Troubleshooting & Recovery Guide

**File:** 06_TROUBLESHOOTING_RECOVERY_GUIDE.md
**Created:** 2025-12-04 15:30:00 UTC
**Version:** 1.0.0
**Purpose:** Comprehensive troubleshooting procedures for all migration phases with disaster recovery and rollback procedures
**Status:** COMPLETE - Ready for Execution

---

## 📋 Quick Navigation

- [Phase 1 Troubleshooting](#phase-1-pre-migration-checklist-troubleshooting)
- [Phase 2 Troubleshooting](#phase-2-data-export-troubleshooting)
- [Phase 5 Troubleshooting](#phase-5-data-restoration-troubleshooting)
- [Phase 6 Troubleshooting](#phase-6-validation-troubleshooting)
- [Disaster Recovery](#disaster-recovery-scenarios)
- [Rollback Procedures](#rollback-procedures)
- [Error Code Reference](#error-code-reference)

---

## PHASE 1: Pre-Migration Checklist Troubleshooting

### Common Failure Modes

**1. Uncommitted Git Files (CRITICAL)**
```bash
# Detection
git status --short | wc -l
# Expected: 0 (clean state)
# Problem: Returns 20 or higher

# Resolution
git add .
git commit -m "feat(phase-b5): Complete E10/E11/E12 APIs and migration prep

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin gap-002-clean-VERIFIED

# Verification
git status
# Expected: "On branch gap-002-clean-VERIFIED, nothing to commit"
```

**2. NER11 Archive Corruption**
```bash
# Detection
tar -tzf 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz > /dev/null
# Expected: Exit code 0 (success)
# Problem: Non-zero exit code, error messages

# Resolution - Option A: Use existing archive if recent
ls -lh 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz
# If file is recent (today) and Git has no modifications, it's likely OK

# Resolution - Option B: Recreate archive
cd 5_NER11_Gold_Model
tar -czf NER11_Gold_Model_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
  models/ training_data/ \
  --exclude='*.pyc' --exclude='__pycache__' \
  --exclude='*.egg-info' --exclude='.git'

# Verification
tar -tzf NER11_Gold_Model_backup_*.tar.gz > /dev/null
echo "Archive integrity: $?"
# Expected: 0
```

**3. Unhealthy Docker Containers**
```bash
# Detection
docker ps -a
# Expected: All containers HEALTHY or RUNNING
# Problem: Any container marked UNHEALTHY, EXITED, or ERROR

# Check Neo4j specifically (critical)
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n) as node_count"
# Expected: node_count = 20739
# Problem: Connection refused, timeout, or wrong count

# Resolution - Neo4j
docker logs openspg-neo4j | tail -20
# Look for: error, exception, out of memory
docker restart openspg-neo4j
sleep 30

# Verification
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n) as node_count"
# Expected: 20739
```

**4. Insufficient USB Space**
```bash
# Detection
df -h /mnt/e | awk 'NR==2 {print $4}'
# Expected: 8G or higher
# Problem: Less than 8G

# Check required space
du -sh 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz
du -sh 5_NER11_Gold_Model/training_data
# Expected: Total ~3.5 GB compressed

# Resolution
# Option A: Delete USB contents and retry with larger USB
# Option B: Skip regenerable files (identified in Phase 2)
# Option C: Use external hard drive instead

# Verification
df -h /mnt/e
# Look for "8G" or "16G" or higher in Avail column
```

**5-10. Other Failures (Git Remote, Branch Tracking, USB Mount, Environment)**
See [Error Code Reference](#error-code-reference) section for complete list.

---

## PHASE 2: Data Export Troubleshooting

### Common Failure Modes

**1. Neo4j Export Fails**
```bash
# Detection
mkdir -p /mnt/e/neo4j_backup
docker exec openspg-neo4j neo4j-admin dump \
  --to-path=/var/lib/neo4j/data/dumps \
  --database=neo4j 2>&1 | head -20

# Resolution - Check Neo4j logs
docker logs openspg-neo4j | grep -i "error\|exception" | tail -10

# Solution: Ensure sufficient disk space
docker exec openspg-neo4j df -h /var/lib/neo4j
# Expected: >1GB free

# Restart and retry
docker restart openspg-neo4j
sleep 30
docker exec openspg-neo4j neo4j-admin dump \
  --to-path=/var/lib/neo4j/data/dumps \
  --database=neo4j
```

**2. MySQL Dump Incomplete**
```bash
# Detection
docker exec openspg-mysql mysqldump \
  -u root -p"${MYSQL_PASSWORD}" \
  --all-databases > /tmp/mysql_backup.sql 2>&1
# Check if file created and has content
wc -l /tmp/mysql_backup.sql
# Expected: >1000 lines

# Resolution - Check MySQL container
docker exec openspg-mysql mysql -u root -p"${MYSQL_PASSWORD}" -e "SHOW DATABASES;"

# If issues, restart container
docker restart openspg-mysql
sleep 10

# Retry with explicit error output
docker exec openspg-mysql mysqldump \
  -u root -p"${MYSQL_PASSWORD}" \
  --all-databases \
  --single-transaction \
  --quick 2>&1 | tee /tmp/mysql_dump.log
```

**3. USB Write Errors**
```bash
# Detection
cp large_file.tar.gz /mnt/e/
# Error: Permission denied or No space left on device

# Resolution - Check mount options
mount | grep /mnt/e
# Expected: rw (read-write)

# Fix permissions if needed
sudo umount /mnt/e
sudo mount -o remount,uid=$(id -u),gid=$(id -g) /mnt/e

# Retry copy with verbose output
cp -v large_file.tar.gz /mnt/e/
# Check result
ls -lh /mnt/e/large_file.tar.gz
```

**4. Checksum Mismatches**
```bash
# Detection
sha256sum 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz > before.sha256
cp 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz /mnt/e/
sha256sum /mnt/e/NER11_Gold_Model.tar.gz > after.sha256
diff before.sha256 after.sha256
# Expected: Files identical
# Problem: Checksums differ

# Resolution - USB may be unstable
sync  # Force filesystem sync
umount /mnt/e
# Physically reseat USB if possible
mount /mnt/e
# Retry copy
cp 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz /mnt/e/NER11_Gold_Model.tar.gz

# Verify again
sha256sum 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz
sha256sum /mnt/e/NER11_Gold_Model.tar.gz
# Both should match
```

---

## PHASE 5: Data Restoration Troubleshooting

### Common Failure Modes

**1. Neo4j Restore Fails**
```bash
# Detection
docker exec openspg-neo4j neo4j-admin load \
  --from-path=/mnt/usb_mount/neo4j_backup \
  --database=neo4j \
  --force
# Error: Cannot load, database exists, permission denied

# Resolution - Stop Neo4j, delete existing database
docker stop openspg-neo4j
docker exec openspg-neo4j rm -rf /var/lib/neo4j/data/databases/neo4j
docker start openspg-neo4j
sleep 10

# Retry load
docker exec openspg-neo4j neo4j-admin load \
  --from-path=/var/lib/neo4j/data/dumps \
  --database=neo4j \
  --force

# Verification - Check node count
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n) as total_nodes"
# Expected: 20739
```

**2. MySQL Import Errors**
```bash
# Detection
docker exec openspg-mysql mysql -u root -p"${MYSQL_PASSWORD}" < /mnt/usb_mount/mysql_backup.sql
# Error: Syntax error, foreign key constraint, database exists

# Resolution - Drop and recreate
docker exec openspg-mysql mysql -u root -p"${MYSQL_PASSWORD}" -e "DROP DATABASE IF EXISTS openspg;"
docker exec openspg-mysql mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE DATABASE openspg CHARACTER SET utf8mb4;"

# Retry import
docker exec openspg-mysql mysql -u root -p"${MYSQL_PASSWORD}" openspg < /mnt/usb_mount/mysql_backup.sql

# Verification
docker exec openspg-mysql mysql -u root -p"${MYSQL_PASSWORD}" -e "USE openspg; SHOW TABLES;" | wc -l
# Expected: 18+ tables
```

**3. NER11 Extract Timeout**
```bash
# Detection
tar -xzf /mnt/usb_mount/NER11_Gold_Model.tar.gz -C 5_NER11_Gold_Model/
# Takes >5 minutes or appears stuck

# Resolution - Extract with verbose output to monitor
tar -xzvf /mnt/usb_mount/NER11_Gold_Model.tar.gz -C 5_NER11_Gold_Model/ | tail -20

# If truly stuck (no output for 10+ seconds):
# Press Ctrl+C (safe to interrupt tar)

# Partial recovery - list contents
tar -tzf /mnt/usb_mount/NER11_Gold_Model.tar.gz | head -20

# Re-extract with different options
tar -xzf /mnt/usb_mount/NER11_Gold_Model.tar.gz \
  -C 5_NER11_Gold_Model/ \
  --checkpoint=.100  # Print progress every 100 files

# Verification
ls -lh 5_NER11_Gold_Model/models/
# Expected: ner11_model, spacy_model directories
```

**4. Python venv Creation Fails**
```bash
# Detection
python3 -m venv venv
# Error: Command not found, permission denied, ensurepip failed

# Resolution - Check Python version
python3 --version
# Expected: Python 3.10+ on macOS

# Ensure pip is available
python3 -m pip --version

# Create venv with explicit pip setup
python3 -m venv venv --upgrade-deps

# Verify venv
source venv/bin/activate
python --version
pip --version
```

---

## PHASE 6: Validation Troubleshooting

### Common Failure Modes

**1. Neo4j Node Count Mismatch**
```bash
# Detection
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n) as node_count"
# Expected: 20739
# Problem: Different count (e.g., 0, partial, corrupted)

# Diagnosis
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN labels(n) as types, COUNT(*) as count GROUP BY types ORDER BY count DESC LIMIT 10"

# Resolution - Check database health
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "CALL db.stats.retrieve('graph.counts.node')"

# If significantly corrupted, restore from backup
docker stop openspg-neo4j
docker volume rm openspg-neo4j
docker start openspg-neo4j
# Re-run Phase 5 restoration
```

**2. NER11 Model Won't Load**
```bash
# Detection
cd 5_NER11_Gold_Model
python -c "import spacy; nlp = spacy.load('ner11')"
# Error: Model not found, incompatible version, corrupt

# Diagnosis
python -m spacy info
spacy-cleaner --info

# Resolution - Check model files
ls -lh models/ner11/
# Expected: model-best, meta.json, tokenizer, vocab files

# Test with simpler model first
python -c "import spacy; nlp = spacy.load('en_core_web_sm')"
# If this works, NER11 model specifically damaged

# Restore model from USB
rm -rf models/ner11
cd /mnt/usb_mount/NER11_Gold_Model && tar -xzf *.tar.gz models/
cp -r models/ner11 ~/Projects/aeon-dt/5_NER11_Gold_Model/models/

# Retry load
python -c "import spacy; nlp = spacy.load('ner11'); print('Loaded successfully')"
```

**3. API Endpoints Not Responding**
```bash
# Detection
curl http://localhost:8000/health
# Error: Connection refused, timeout

# Diagnosis
docker ps | grep api
# Check if API container running
docker logs openspg-server | tail -20
# Look for startup errors

# Check port conflicts
lsof -i :8000
# Expected: Python process running api

# Resolution
docker restart openspg-server
sleep 5

# Verify
curl -v http://localhost:8000/health
# Expected: {"status": "healthy"}

# If still failing
docker logs openspg-server --tail=100 | grep -i "error\|exception"
```

---

## Disaster Recovery Scenarios

### Scenario 1: USB Corruption Mid-Transfer

**Detection:** Checksums fail during Phase 3 verification
**Impact:** CRITICAL - All exported data potentially lost
**Recovery Time:** 45-90 minutes

```bash
# STOP immediately - DO NOT proceed to macOS

# Step 1: Re-mount USB and verify
sudo umount /mnt/e
sudo mount /mnt/e
ls -lh /mnt/e/

# Step 2: Check which files corrupted
cd /mnt/e
sha256sum * > current.sha256

# Step 3: Compare with exported list
cat MIGRATION_MANIFEST.txt | grep "sha256" > expected.sha256
diff expected.sha256 current.sha256

# Step 4: Delete all USB content
rm -rf /mnt/e/*

# Step 5: Re-run Phase 2 (Data Export) completely
# Follow: 02_DATA_EXPORT_PROCEDURES.md from beginning

# Step 6: Re-verify checksums before proceeding
sha256sum -c /mnt/e/MIGRATION_MANIFEST.txt
# Expected: All OK
```

### Scenario 2: Partial Data Transfer (Network Interruption)

**Detection:** Not all files on macOS after USB transfer
**Impact:** HIGH - Missing critical data
**Recovery Time:** 15-30 minutes

```bash
# Step 1: Identify missing files
ls /mnt/usb_mount/ > transferred_files.txt
cat /mnt/usb_mount/MIGRATION_MANIFEST.txt | grep "File:" > expected_files.txt
diff expected_files.txt transferred_files.txt

# Step 2: Copy missing files individually
for file in $(diff expected_files.txt transferred_files.txt | grep ">" | awk '{print $NF}'); do
  cp /mnt/e/"$file" /mnt/usb_mount/
done

# Step 3: Verify checksums for newly copied files
sha256sum /mnt/usb_mount/missing_file_1.tar.gz
# Compare with expected in MIGRATION_MANIFEST.txt

# Step 4: Proceed with Phase 5 (Data Restoration)
```

### Scenario 3: Database Inconsistency After Restore

**Detection:** Neo4j has wrong node count or MySQL missing tables
**Impact:** CRITICAL - Data integrity compromised
**Recovery Time:** 30-45 minutes

```bash
# Step 1: Verify damage extent
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n)"
# If returns 0 or <10000, database empty or corrupted

docker exec openspg-mysql mysql -u root -p"${MYSQL_PASSWORD}" \
  -e "SELECT COUNT(*) FROM openspg.* \G"
# If returns 0 for all tables, schema lost

# Step 2: Stop all services
docker-compose -f docker-compose.databases.yml stop

# Step 3: Delete corrupt volumes
docker volume rm openspg-neo4j openspg-mysql

# Step 4: Restart services with fresh volumes
docker-compose -f docker-compose.databases.yml up -d

# Step 5: Re-restore from USB backups
# Follow: 04_DATA_RESTORATION_GUIDE.md Phase 5 again

# Step 6: Full validation before use
# Follow: 05_VALIDATION_PROCEDURES.md Phase 6
```

### Scenario 4: Lost Files (USB Disconnected Prematurely)

**Detection:** Files missing from USB or corrupted manifest
**Impact:** CRITICAL - Migration cannot proceed
**Recovery Time:** 45-90 minutes

```bash
# Step 1: Check manifest integrity
cat /mnt/e/MIGRATION_MANIFEST.txt
# If file missing or incomplete, export was interrupted

# Step 2: Verify USB was actually disconnected
ls -lh /mnt/e/
# If newest files are from >2 hours ago, likely interrupted

# Step 3: Return to WSL2
# macOS setup can be paused, WSL2 system untouched

# Step 4: Re-run Phase 2 completely
# Do NOT attempt partial re-export
# Complete export from scratch ensures consistency

# Step 5: Run full verification
sha256sum -c /mnt/e/MIGRATION_MANIFEST.txt
# Expected: All OK before returning to macOS
```

---

## Rollback Procedures

### Phase 1 Rollback (Complete)
If Phase 1 validation fails with multiple issues, abort migration:
```bash
# No changes made yet, simply resolve issues and retry
git status  # Ensure clean
docker ps   # Ensure containers healthy
df -h /mnt/e  # Ensure USB has 8GB+
# Then: Start Phase 1 Pre-Migration Checklist again
```

### Phase 2 Rollback (Safe - No Deletion)
If Phase 2 export fails, WSL2 system intact:
```bash
# Clean USB and retry
rm -rf /mnt/e/*

# WSL2 containers still running with data intact
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n)"
# Expected: Still 20739 (no data loss)

# Restart Phase 2 from beginning
# 02_DATA_EXPORT_PROCEDURES.md
```

### Phase 5 Rollback (Partial Recovery Possible)
If restoration fails partially:
```bash
# Option 1: Partial rollback - restore single component
docker volume rm openspg-neo4j  # Delete only Neo4j
docker volume create openspg-neo4j
# Re-run Neo4j restoration only

# Option 2: Complete rollback - delete everything and restart
docker-compose down -v
docker-compose up -d
# Re-run Phase 5 completely from USB backups

# WSL2 system still intact - no impact
```

### Complete Abort (Return to WSL2)
If multiple critical failures occur:
```bash
# On macOS - simply STOP working
# Do NOT delete or modify files

# Return to WSL2 system
# All data, code, and models remain intact
docker ps  # Verify all containers still healthy
git status  # Verify no changes lost

# Option to retry migration later with different approach
```

---

## Error Code Reference

### Git Errors (G001-G005)

| Error | Pattern | Severity | Resolution |
|-------|---------|----------|-----------|
| G001 | Uncommitted files block migration | CRITICAL | `git add . && git commit && git push` |
| G002 | Remote not configured | HIGH | `git remote add origin <url>` |
| G003 | Branch not tracking remote | MEDIUM | `git branch --set-upstream-to=origin/branch` |
| G004 | Bundle verification fails | CRITICAL | Recreate from clean repository |
| G005 | Clone fails on macOS | HIGH | Check SSH keys or use HTTPS |

### Docker Errors (D001-D006)

| Error | Pattern | Severity | Resolution |
|-------|---------|----------|-----------|
| D001 | Container won't start | CRITICAL | Check logs, verify volumes |
| D002 | Neo4j dump/restore fails | CRITICAL | Stop container, retry backup |
| D003 | MySQL import errors | HIGH | Check foreign key constraints |
| D004 | Volume creation fails | HIGH | Check Docker permissions |
| D005 | Port conflicts | MEDIUM | Kill process on port |
| D006 | Network creation fails | MEDIUM | Delete existing, recreate |

### Database Errors (DB001-DB005)

| Error | Pattern | Severity | Resolution |
|-------|---------|----------|-----------|
| DB001 | Neo4j node count mismatch | CRITICAL | Restore from backup |
| DB002 | MySQL schema missing | CRITICAL | Re-import from backup |
| DB003 | Cypher query timeout | HIGH | Restart Neo4j, check resources |
| DB004 | Foreign key violations | MEDIUM | Import in correct order |
| DB005 | Qdrant collection missing | LOW | Regenerate from Neo4j |

### File System Errors (FS001-FS005)

| Error | Pattern | Severity | Resolution |
|-------|---------|----------|-----------|
| FS001 | USB write permission denied | CRITICAL | Check mount options |
| FS002 | Archive corruption | CRITICAL | Re-create archive |
| FS003 | Checksum mismatch | CRITICAL | Re-copy files to USB |
| FS004 | USB unmount fails | MEDIUM | `sudo umount -f /mnt/e` |
| FS005 | Insufficient disk space | CRITICAL | Use larger drive |

### Network Errors (N001-N004)

| Error | Pattern | Severity | Resolution |
|-------|---------|----------|-----------|
| N001 | Port already in use | HIGH | Kill conflicting process |
| N002 | Docker network conflict | MEDIUM | Delete and recreate |
| N003 | API not accessible | HIGH | Check firewall, port |
| N004 | Neo4j connection timeout | CRITICAL | Verify container running |

### Permission Errors (P001-P003)

| Error | Pattern | Severity | Resolution |
|-------|---------|----------|-----------|
| P001 | Docker volume ownership | HIGH | `sudo chown -R $USER:$USER` |
| P002 | venv permission denied | MEDIUM | Use `--user` flag |
| P003 | USB write permission | CRITICAL | Re-mount with correct permissions |

### Resource Errors (R001-R003)

| Error | Pattern | Severity | Resolution |
|-------|---------|----------|-----------|
| R001 | Insufficient RAM | HIGH | Close applications |
| R002 | Disk space exhausted | CRITICAL | Clean temporary files |
| R003 | CPU throttling | LOW | Reduce concurrent operations |

---

## When to Stop and Get Help

**ABORT MIGRATION IF:**
- 🔴 Any CRITICAL error that cannot be resolved in 30 minutes
- 🔴 Data corruption detected (failed checksums that persist after retry)
- 🔴 Multiple systems failing simultaneously (Neo4j + MySQL + models)
- 🔴 Uncertain about rollback safety

**ESCALATION CONTACTS:**
- DevOps: Check Docker logs for infrastructure issues
- Database Admin: Neo4j/MySQL consistency issues
- ML Engineer: NER11 model problems
- Migration Lead: Multiple component failures

---

## Key Principles

✅ **Verify after every step** - Checksum, node count, file count
✅ **Never delete until verified** - Keep backups until complete
✅ **WSL2 remains intact** - All data safe, never lost
✅ **Rollback always possible** - No point of no return
✅ **Take detailed logs** - Screenshots, command output, error messages

---

**Status:** COMPLETE - Ready for execution
**Last Updated:** 2025-12-04 15:30:00 UTC
**Version:** 1.0.0

🚀 Reference this guide if ANY issues arise during migration execution
