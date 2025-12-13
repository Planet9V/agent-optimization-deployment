# Pre-Migration Checklist & Verification
**File:** 01_PRE_MIGRATION_CHECKLIST.md
**Created:** 2025-12-04
**Purpose:** Verify WSL2 system is ready for macOS migration
**Status:** DETAILED PROCEDURES READY

---

## ⚠️ CRITICAL: Do These FIRST

### 1. Git Cleanup - BLOCKING ISSUE
**Status:** ⚠️ 20 UNCOMMITTED FILES IDENTIFIED

These files will NOT transfer to macOS without git commit:
- E10, E11, E12 API implementations (3 directories)
- Test suites for new APIs
- Recent documentation

**IMMEDIATE ACTION REQUIRED:**

```bash
cd /home/jim/2_OXOT_Projects_Dev

# Check current status
git status --short
# Output will show uncommitted files

# Add all changes
git add .

# Review what will be committed
git status

# Commit with detailed message
git commit -m "feat(phase-b5): Complete E10/E11/E12 APIs and migration prep

Implemented:
- E10 Economic Impact API (27 endpoints)
- E11 Demographics API (24 endpoints)
- E12 Prioritization API (28 endpoints)
- Complete test suites for all new APIs
- Frontend developer guides and cheatsheets
- Migration documentation for macOS transition

This commit represents the final Phase B5 deliverable and
prepares the codebase for macOS development migration."

# Push to remote
git push origin gap-002-clean-VERIFIED

# Verify clean working directory
git status
# Expected output: "nothing to commit, working tree clean"
```

**Success Criteria:**
- ✅ All 20 files committed to git
- ✅ Changes pushed to origin
- ✅ `git status` shows clean working directory
- ✅ `git log --oneline -1` shows your commit

**If this fails:** DO NOT PROCEED with migration

---

## Detailed Pre-Migration Verification

### Task 1.1: System Inventory

**Purpose:** Confirm what needs to transfer and what can be skipped

```bash
cd /home/jim/2_OXOT_Projects_Dev

# Total project size
du -sh .
# Expected: ~12 GB

# Git-tracked files
git ls-files | wc -l
# Expected: ~10,698 files

# Non-tracked files (these won't transfer)
find . -type f ! -path "./.git/*" ! -path "./.git" | wc -l | \
  xargs -I {} echo "Total files: {}"
# Expected: ~110,680 files total (100K non-tracked)

# Largest directories (to understand what's NOT in git)
du -sh 5_NER11_Gold_Model/
du -sh 1_AEON_DT_CyberSecurity_Wiki_Current/
du -sh 1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1/
du -sh node_modules/
```

**Expected Results:**
```
Total project: ~12 GB
5_NER11_Gold_Model: ~3.5 GB (critical)
Wiki: ~150 MB (mostly in git)
Frontend: ~1.3 MB (in git)
node_modules: ~894 MB (regenerable - skip)
```

**Verification:**
- [ ] Total size confirmed
- [ ] Git-tracked count matches
- [ ] Large directories identified

---

### Task 1.2: NER11 Model Archive Verification

**Purpose:** Ensure NER11 models are available and uncorrupted

```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model

# Check if archive exists
ls -lh NER11_Gold_Model.tar.gz
# Expected: -rw-r--r-- 1 jim jim 439M [date] NER11_Gold_Model.tar.gz

# Verify archive integrity
tar -tzf NER11_Gold_Model.tar.gz > /tmp/tar_list.txt 2>&1
if [ $? -eq 0 ]; then
  echo "✅ Archive is readable and intact"
  wc -l /tmp/tar_list.txt  # Count files in archive
else
  echo "❌ Archive is CORRUPTED - ABORT MIGRATION"
  tar -tzf NER11_Gold_Model.tar.gz 2>&1 | tail -20
fi

# List first 20 files to spot check
tar -tzf NER11_Gold_Model.tar.gz | head -20
# Expected: models/, training_data/ directories

# Check if extracted models also exist
if [ -d "models/ner11_v3/model-best" ]; then
  echo "✅ Extracted models also present"
  du -sh models/
else
  echo "⚠️ Extracted models not present (will be extracted from archive on Mac)"
fi
```

**Success Criteria:**
- ✅ Archive exists and is 439 MB
- ✅ Archive is readable (no corruption)
- ✅ Contains expected files (models/, training_data/)
- ✅ If extracted, directory is >900 MB

**If archive is corrupted:**
```bash
# Recreate archive if models are extracted
tar -czf NER11_Gold_Model_$(date +%Y%m%d_%H%M%S).tar.gz \
  models/ training_data/ \
  --exclude='*.pyc' --exclude='__pycache__' \
  --exclude='.git'

ls -lh NER11_Gold_Model_*.tar.gz
```

**Verification:**
- [ ] Archive exists and is readable
- [ ] Archive size confirmed (~439 MB)
- [ ] No corruption detected

---

### Task 1.3: Docker System Status Check

**Purpose:** Verify all containers are healthy before backup

```bash
# List all containers and their status
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Expected output (all should be "Up" or "Healthy"):
# NAME                 STATUS                         PORTS
# ner11-gold-api       Up 3 hours                     0.0.0.0:8000->8000/tcp
# openspg-redis        Up 3 hours                     0.0.0.0:6379->6379/tcp
# openspg-qdrant       Up 3 hours (health: starting)  0.0.0.0:6333->6333/tcp, 0.0.0.0:6334->6334/tcp
# openspg-server       Up 3 hours                     0.0.0.0:8887->8887/tcp
# openspg-minio        Up 3 hours                     0.0.0.0:9000->9000/tcp, 0.0.0.0:9001->9001/tcp
# openspg-mysql        Healthy (3 seconds ago)        0.0.0.0:3306->3306/tcp
# openspg-neo4j        Healthy (3 seconds ago)        0.0.0.0:7474->7474/tcp, 0.0.0.0:7687->7687/tcp
# aeon-saas-dev        Up 3 hours                     0.0.0.0:3000->3000/tcp
# aeon-postgres-dev    Up 3 hours                     0.0.0.0:5432->5432/tcp

# Detailed health check for critical containers
echo "=== Neo4j Health Check ==="
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n) as total_nodes LIMIT 1"
# Expected: 20739

echo "=== MySQL Health Check ==="
docker exec openspg-mysql mysql -u root -popenspg -e \
  "SELECT VERSION(); SELECT COUNT(*) as databases FROM information_schema.schemata;"
# Expected: MySQL version and count of databases

echo "=== Qdrant Health Check ==="
curl -s http://localhost:6333/health | jq .
# Expected: {"status": "ok"} or similar

echo "=== Redis Health Check ==="
docker exec openspg-redis redis-cli ping
# Expected: PONG

echo "=== MinIO Health Check ==="
curl -s http://localhost:9000/minio/health/live
# Expected: HTTP 200

echo "=== NER11 API Health Check ==="
curl -s http://localhost:8000/health
# Expected: JSON response or message
```

**Verification Checklist:**
- [ ] All 9 containers are "Up" or "Healthy"
- [ ] No containers in "Exited" or "Restarting" state
- [ ] Neo4j responds with 20,739 nodes
- [ ] MySQL is Healthy
- [ ] Redis responds to PING
- [ ] MinIO is accessible
- [ ] NER11 API responds

**If containers are unhealthy:**
```bash
# Restart Docker daemon
systemctl restart docker

# Or restart individual container
docker restart openspg-neo4j

# Check logs if still failing
docker logs openspg-neo4j
```

---

### Task 1.4: USB Drive Preparation

**Purpose:** Verify USB drive is ready for data transfer

```bash
# Check USB drive capacity and mount point
df -h | grep -E "(mnt|Volumes|media)"
# Expected output example:
# /dev/sdb1         8.0G  1.2G  6.8G  15% /mnt/e

# Check available space
AVAILABLE=$(df /mnt/e | awk 'NR==2 {print $4}')
if [ $AVAILABLE -gt 8388608 ]; then  # 8 GB in KB
  echo "✅ USB has sufficient space (>8 GB free)"
else
  echo "❌ USB insufficient space - need >8 GB, have $(($AVAILABLE/1024))MB"
fi

# Check file system type
df -T /mnt/e | awk 'NR==2 {print $2}'
# Expected: vfat, ntfs, or exfat (all work on Mac)

# Create transfer staging directory
mkdir -p /mnt/e/AEON_Transfer

# Set permissions
chmod 755 /mnt/e/AEON_Transfer

# Verify staging directory
ls -la /mnt/e/AEON_Transfer
# Expected: Empty directory is ready
```

**Verification Checklist:**
- [ ] USB drive mounted and accessible
- [ ] Free space >8 GB (recommended 16 GB)
- [ ] File system is NTFS, ExFAT, or vfat
- [ ] Staging directory created
- [ ] Permissions allow read/write

**If USB issues:**
```bash
# Unmount and check
umount /mnt/e

# Format USB (WARNING: Data loss!)
# Only if USB is new or empty data is okay
# mkfs.exfat /dev/sdb1
# mkfs.vfat /dev/sdb1

# Re-mount
mount /dev/sdb1 /mnt/e

# Verify
mount | grep /mnt/e
```

---

### Task 1.5: Git Repository Verification

**Purpose:** Ensure git history is complete and backed up

```bash
# Check git status
cd /home/jim/2_OXOT_Projects_Dev
git status
# Expected: "nothing to commit, working tree clean"

# Check git history
git log --oneline -10
# Expected: At least 10 commits visible

# Verify remote is configured
git remote -v
# Expected: origin points to GitHub repository

# Check that branch tracks remote
git branch -v
# Expected: gap-002-clean-VERIFIED [...] ahead/up to date with origin/gap-002-clean-VERIFIED

# Create a backup tag
git tag -a "pre-mac-migration-$(date +%Y%m%d-%H%M%S)" \
  -m "Pre-macOS migration backup point"

# Push tag to remote
git push origin "pre-mac-migration-$(date +%Y%m%d-%H%M%S)"

# Verify tag exists
git tag -l | grep pre-mac
```

**Verification Checklist:**
- [ ] Working directory clean
- [ ] Git history visible (10+ commits)
- [ ] Remote configured (origin → GitHub)
- [ ] Branch tracking remote
- [ ] Backup tag created and pushed

---

### Task 1.6: System Snapshot Documentation

**Purpose:** Document current state for reference during migration

```bash
# Create snapshot document
cat > /tmp/PRE_MIGRATION_SNAPSHOT.txt << 'EOF'
AEON Digital Twin - Pre-Migration System Snapshot
================================================

Date: $(date '+%Y-%m-%d %H:%M:%S')
System: WSL2 Linux
Git Branch: gap-002-clean-VERIFIED

GIT STATUS
----------
EOF

cd /home/jim/2_OXOT_Projects_Dev
git log --oneline -5 >> /tmp/PRE_MIGRATION_SNAPSHOT.txt

echo -e "\n\nDOCKER CONTAINERS" >> /tmp/PRE_MIGRATION_SNAPSHOT.txt
docker ps --format "{{.Names}}\t{{.Status}}" >> /tmp/PRE_MIGRATION_SNAPSHOT.txt

echo -e "\n\nDATABASE SIZES" >> /tmp/PRE_MIGRATION_SNAPSHOT.txt
echo "Neo4j nodes:" >> /tmp/PRE_MIGRATION_SNAPSHOT.txt
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n)" >> /tmp/PRE_MIGRATION_SNAPSHOT.txt 2>&1

echo -e "\n\nDISK USAGE" >> /tmp/PRE_MIGRATION_SNAPSHOT.txt
du -sh /home/jim/2_OXOT_Projects_Dev >> /tmp/PRE_MIGRATION_SNAPSHOT.txt
du -sh /home/jim/2_OXOT_Projects_Dev/* >> /tmp/PRE_MIGRATION_SNAPSHOT.txt

# Copy snapshot to USB as well
cp /tmp/PRE_MIGRATION_SNAPSHOT.txt /mnt/e/AEON_Transfer/

# Display snapshot
cat /tmp/PRE_MIGRATION_SNAPSHOT.txt
```

**Verification Checklist:**
- [ ] Snapshot created
- [ ] Git history documented
- [ ] Container status documented
- [ ] Database size documented
- [ ] Snapshot saved to USB

---

## Final Pre-Migration Checklist

### Code Preparation
- [ ] **CRITICAL:** All uncommitted files committed to git
- [ ] Commits pushed to origin (GitHub)
- [ ] Migration tag created and pushed
- [ ] `git status` shows clean working directory
- [ ] `git log --oneline -1` shows recent commit

### Docker System
- [ ] All 9 containers are Up or Healthy
- [ ] Neo4j has 20,739 nodes
- [ ] MySQL is Healthy
- [ ] No containers in Exited state
- [ ] All critical services responding

### Files & Data
- [ ] NER11 archive exists (439 MB)
- [ ] Archive integrity verified
- [ ] Project size confirmed (~12 GB total)
- [ ] Large directories identified

### USB Drive
- [ ] USB mounted at /mnt/e
- [ ] Free space >8 GB
- [ ] Staging directory created
- [ ] File system is NTFS/ExFAT
- [ ] Permissions allow read/write

### Documentation
- [ ] Pre-migration snapshot created
- [ ] System state documented
- [ ] Checklist completed
- [ ] Next steps clear

---

## ⚠️ BLOCKING ISSUES - MUST RESOLVE

### Issue 1: Uncommitted Files
**Status:** BLOCKING - Migration cannot proceed
**Files Affected:** E10, E11, E12 API implementations
**Resolution:** Commit and push all files to git

**Check:**
```bash
git status --short
# If output is NOT empty, files are uncommitted
```

**Fix:**
```bash
git add .
git commit -m "feat: Phase B5 completion and migration prep"
git push origin gap-002-clean-VERIFIED
git status  # Should show "nothing to commit"
```

### Issue 2: Corrupted Archive
**Status:** BLOCKING if archive is corrupted
**File:** 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz
**Resolution:** Recreate archive if corrupted

**Check:**
```bash
tar -tzf 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz > /dev/null
echo $?  # Should be 0 (success)
```

### Issue 3: Unhealthy Containers
**Status:** BLOCKING if critical containers fail
**Critical:** Neo4j, MySQL
**Resolution:** Restart containers or troubleshoot

**Check:**
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n)"
# Should return 20739
```

### Issue 4: Insufficient USB Space
**Status:** BLOCKING if USB <8 GB free
**Solution:** Use larger USB or exclude regenerable files

**Check:**
```bash
df -h /mnt/e | awk 'NR==2 {print $4}'
# Should be >8GB (8388608 KB)
```

---

## Go/No-Go Decision

**Ready to proceed to Phase 2?**

### ALL of the following must be TRUE:

1. ✅ Git is clean (all changes committed)
2. ✅ All containers are healthy
3. ✅ NER11 archive is intact
4. ✅ USB has >8 GB free space
5. ✅ No blocking issues identified
6. ✅ Pre-migration checklist completed

### If ANY are FALSE:

**STOP** - Do not proceed to Phase 2
**FIX** - Resolve the blocking issue
**RETRY** - Come back to this checklist

### If ALL are TRUE:

**✅ PROCEED to Phase 2: Data Collection & Export**
**Next Document:** 02_DATA_EXPORT_PROCEDURES.md

---

*Complete this checklist before proceeding.*
*Do not skip any verification steps.*
*Resolution of blocking issues is MANDATORY.*
