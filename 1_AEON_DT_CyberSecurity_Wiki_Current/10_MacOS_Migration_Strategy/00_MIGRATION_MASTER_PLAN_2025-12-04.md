# AEON Digital Twin - macOS Migration Master Plan
**File:** 00_MIGRATION_MASTER_PLAN_2025-12-04.md
**Created:** 2025-12-04 11:45:00 UTC
**Purpose:** Comprehensive strategy for moving from WSL2 Linux to macOS
**Status:** PLANNING PHASE - Not executed yet
**Author:** Claude Code Architecture Team

---

## Executive Summary

**Migration Objective:** Move AEON Digital Twin development environment from WSL2 to macOS **without disrupting current development** and **preserving all critical data and models**.

**Complexity Level:** MEDIUM-HIGH
**Total Data to Transfer:** ~4.5-5.5 GB critical data
**Estimated Migration Time:** 3-5 hours (6 phases)
**Risk Level:** LOW (with proper preparation)
**Data Loss Risk:** MINIMAL (with comprehensive backups)

### Key Constraints
- **Cannot disrupt current development** - WSL2 system must remain stable
- **USB drive (E:) is the transfer medium** - Must fit all critical files
- **Large files NOT in git** - 3.5 GB NER11 models + training data
- **Docker volumes contain crucial state** - 20K+ Neo4j nodes must be preserved
- **Recent commits not yet pushed** - E10/E11/E12 APIs need git commit first

### Success Criteria
✅ All 251+ API endpoints functional on macOS
✅ Neo4j restored with 20,739 nodes intact
✅ NER11 model available and operational
✅ Docker containers running and healthy
✅ Frontend development environment ready
✅ All tests passing on macOS
✅ Zero data loss or corruption

---

## Project Inventory Analysis

### Current System State (WSL2 Linux)

**Total Files:** 110,680
**Total Size:** 12+ GB
**Git-Tracked:** 10,698 files (9.7%)
**Non-Tracked:** ~100,000 files (90.3%)

### File Breakdown by Category

#### CRITICAL - Must Transfer
| Component | Size | Type | Location | Status |
|-----------|------|------|----------|--------|
| **NER11 Models** | 976 MB | ML Models | `5_NER11_Gold_Model/models/ner11_v3/` | ⚠️ NOT IN GIT |
| **Training Data** | 2.1 GB | Datasets | `5_NER11_Gold_Model/training_data/` | ⚠️ NOT IN GIT |
| **Neo4j Database** | ~500 MB (dump) | Graph DB | Docker volume | ✅ Backed up |
| **MySQL Metadata** | ~50 MB | Relational DB | Docker volume | ✅ Backed up |
| **MinIO Storage** | ~100 MB | Object Store | Docker volume | ⚠️ Optional |
| **Git Repository** | ~100 MB | Source Code | GitHub | ✅ IN GIT |
| **Documentation** | ~150 MB | Markdown | `1_AEON_DT_CyberSecurity_Wiki_Current/` | ✅ Mostly in git |

**Total Critical:** ~4.5 GB

#### IMPORTANT - Should Transfer
| Component | Size | Type | Status |
|-----------|------|------|--------|
| Qdrant Vector DB | ~200 MB | Vector embeddings | ⚠️ Can regenerate |
| Redis Cache | ~10 MB | Session data | ❌ Skip - rebuild |
| API Code (E10/E11/E12) | 2.4 MB | Source code | ⚠️ Need git commit |
| Test Suites | 1.2 MB | Tests | ⚠️ Need git commit |
| Frontend Guides | 200 MB | Documentation | ✅ Mostly in git |

**Total Important:** ~400 MB

#### REGENERABLE - Can Skip
| Component | Size | Type | Status |
|-----------|------|------|--------|
| node_modules | 894 MB | Dependencies | ❌ npm install |
| Import Archives | 1.9 GB | Old migration data | ❌ Already processed |
| Training data archive | 202 MB | Superseded | ❌ Excluded |
| Temp files | 54 MB | Runtime | ❌ Skip |
| __pycache__ | ~200 MB | Python cache | ❌ Regenerate |
| Build artifacts | ~100 MB | Build output | ❌ npm run build |

**Total Regenerable:** ~3.3 GB

### Docker Volume Analysis

**Current Active Volumes:**
```
✅ HEALTHY:
  - openspg-neo4j-data (20,739 nodes)
  - openspg-mysql-data (OpenSPG schema)
  - openspg-minio-data (object storage)
  - openspg-redis-data (cache)
  - aeon-postgres-dev (frontend DB)

⚠️ NEEDS VERIFICATION:
  - openspg-qdrant-data (vector DB)

📊 SIZES:
  - Neo4j: ~500 MB (estimated from node count)
  - MySQL: ~50 MB
  - MinIO: ~100 MB
  - Redis: ~10 MB
  - PostgreSQL: ~20 MB
```

### Container Dependencies

**Network:** `openspg-network` (shared by all services)

**Services:**
1. openspg-server (OpenSPG platform)
2. openspg-mysql (Metadata)
3. openspg-neo4j (Graph Database) ⭐ CRITICAL
4. openspg-minio (Object Storage)
5. openspg-qdrant (Vector Database) ⭐ CRITICAL
6. openspg-redis (Cache)
7. ner11-gold-api (NER Model API) ⭐ CRITICAL
8. aeon-saas-dev (Frontend)
9. aeon-postgres-dev (Frontend DB)

---

## Recommended Migration Strategy: Hybrid Approach

### Strategy Selection Matrix

| Strategy | Git | USB | Models | Speed | Risk | Disruption |
|----------|-----|-----|--------|-------|------|-----------|
| **A: Sequential USB** | ✅ | ✅ | ✅ | Slow | Low | High |
| **B: Network Transfer** | ✅ | ❌ | ⚠️ | Fast | Med | High |
| **C: Hybrid (RECOMMENDED)** | ✅ | ✅ | ✅ | Fast | Low | Low |
| **D: Cloud Staging** | ✅ | ❌ | ✅ | Fast | High | Med |

### **Selected: Option C - Hybrid Strategy** ⭐

**Approach:**
1. **Code & Git History:** Clone from GitHub (clean, version-controlled)
2. **Docker Volumes:** Export on WSL2, restore on macOS via USB
3. **NER11 Models:** Transfer via USB (faster than download)
4. **Dependencies:** Install fresh on macOS (cleaner environment)

**Advantages:**
- ✅ Minimal WSL2 disruption (no code moves)
- ✅ Clean macOS setup (fresh dependencies)
- ✅ Version control maintained (git history preserved)
- ✅ Fallback options available (GitHub, cloud backup)
- ✅ Parallelizable (export while preparing Mac)

**Timeline:** 3-5 hours total

---

## Critical Pre-Migration Tasks

### ⚠️ BLOCKING ISSUES - Must Resolve First

**Issue 1: Uncommitted Code (20 files)**
- Location: Phase B5 APIs (E10, E11, E12)
- Risk: These files will NOT transfer to Mac without git commit
- Action: **COMMIT AND PUSH TO GIT BEFORE MIGRATION**

**Issue 2: Documentation Not in Git**
- Recent: FRONTEND_DEVELOPER_GUIDE_2025-12-04.md, etc.
- Action: **ADD TO GIT BEFORE MIGRATION**

**Issue 3: NER11 Model Archive (439 MB)**
- Status: Archive exists but verify integrity before transfer
- Action: **VERIFY ARCHIVE: `tar tzf NER11_Gold_Model.tar.gz | wc -l`**

**Issue 4: GPU Dependency**
- Current: CUDA 11.x (NVIDIA-specific)
- Mac: No CUDA available
- Action: **PLAN FOR CPU-ONLY or MPS (Metal) mode**

---

## Phase-by-Phase Migration Plan

### Phase 1: Planning & Preparation (30-45 minutes)
**Goal:** Verify readiness and create backup

#### Task 1.1: System Inventory
```bash
# Check git status for uncommitted files
cd /home/jim/2_OXOT_Projects_Dev
git status --short | wc -l
# Expected: Should be 0 after all commits done

# Check project size
du -sh /home/jim/2_OXOT_Projects_Dev
# Expected: ~12 GB total, ~4.5 GB critical for transfer

# Verify NER11 archive exists
ls -lh 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz
# Expected: ~439 MB
```

**Success Criteria:**
- ✅ All critical files identified
- ✅ Project size <12 GB
- ✅ NER11 archive verified
- ✅ Git status clean (or commits planned)

**Risk Level:** LOW
**Recovery:** N/A (no changes yet)

---

#### Task 1.2: USB Drive Verification
```bash
# Check USB drive capacity
df -h /mnt/e
# Expected: Minimum 8 GB free, 16 GB recommended

# Check file system
mount | grep e:
# Expected: NTFS or ExFAT (works on Mac)

# Create transfer staging directory
mkdir -p /mnt/e/AEON_Transfer
ls -la /mnt/e/AEON_Transfer
```

**Success Criteria:**
- ✅ USB drive has 8+ GB free space
- ✅ File system is NTFS or ExFAT
- ✅ Staging directory created
- ✅ USB write permissions verified

**Risk Level:** LOW
**Recovery:** Use different USB drive if needed

---

#### Task 1.3: Git Cleanup & Tagging
```bash
# Commit all outstanding changes
cd /home/jim/2_OXOT_Projects_Dev
git add .
git status --short  # Review what will be committed

# Create meaningful commit message
git commit -m "feat(phase-b5): Add E10/E11/E12 APIs + Complete documentation

- E10 Economic Impact API (27 endpoints)
- E11 Demographics API (24 endpoints)
- E12 Prioritization API (28 endpoints)
- Complete frontend developer guides
- Migration preparation documentation"

# Push to origin
git push origin gap-002-clean-VERIFIED

# Create migration tag
git tag -a "mac-migration-2025-12-04" -m "Pre-Mac migration snapshot"
git push origin mac-migration-2025-12-04
```

**Success Criteria:**
- ✅ All changes committed to git
- ✅ Pushed to remote (origin)
- ✅ Migration tag created
- ✅ `git status` shows clean working directory

**Risk Level:** LOW
**Recovery:** Revert commits if needed (git reset --hard tag)

---

#### Task 1.4: Docker Container Status Check
```bash
# List all containers
docker ps -a

# Check health status
docker ps --format "table {{.Names}}\t{{.Status}}"

# Expected output (all HEALTHY or Up):
# NAME                 STATUS
# ner11-gold-api       Up 3 hours
# openspg-redis        Up 3 hours
# openspg-qdrant       Up 3 hours (or check health)
# openspg-server       Up 3 hours
# openspg-minio        Up 3 hours
# openspg-mysql        Healthy (3 seconds ago)
# openspg-neo4j        Healthy (3 seconds ago)
# aeon-saas-dev        Up 3 hours
# aeon-postgres-dev    Up 3 hours

# Verify Neo4j is responsive
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1"
# Expected: (no output means success)
```

**Success Criteria:**
- ✅ All containers running or healthy
- ✅ Neo4j responds to queries
- ✅ Database connectivity verified

**Risk Level:** LOW
**Recovery:** Start containers if stopped (`docker-compose up -d`)

---

#### Task 1.5: Pre-Migration Safety Checklist
```bash
# Create snapshot of current state
date > /tmp/migration_start.txt
git log --oneline -5 >> /tmp/migration_start.txt
docker ps --format "{{.Names}}" >> /tmp/migration_start.txt
cp /tmp/migration_start.txt /mnt/e/AEON_Transfer/PRE_MIGRATION_STATE.txt

# Verify git is clean
if [ -z "$(git status --short)" ]; then
  echo "✅ Git is clean - safe to proceed"
else
  echo "❌ Uncommitted changes remain - ABORT MIGRATION"
  exit 1
fi

# Summary
echo "✅ Pre-migration checks PASSED"
echo "System ready for Phase 2"
```

**Success Criteria:**
- ✅ Pre-migration state documented
- ✅ Git is clean
- ✅ All checks passed

**Risk Level:** LOW
**Recovery:** Abort and fix any issues before proceeding

---

### Phase 2: Data Collection & Export (45-90 minutes)
**Goal:** Extract all critical data from Docker and filesystem

#### Task 2.1: Export Neo4j Database
```bash
# Create export directory
mkdir -p /tmp/neo4j_export

# Stop Neo4j container to ensure consistent backup
docker stop openspg-neo4j

# Export Neo4j database (on-disk backup)
docker run --rm \
  -v openspg-neo4j-data:/data \
  -v /tmp/neo4j_export:/export \
  neo4j:5.26-community \
  neo4j-admin database dump neo4j --to-path=/export

# Start Neo4j again
docker start openspg-neo4j

# Verify export
ls -lh /tmp/neo4j_export/
du -sh /tmp/neo4j_export/
# Expected: neo4j.dump file, ~500 MB

# Copy to USB
cp /tmp/neo4j_export/neo4j.dump /mnt/e/AEON_Transfer/neo4j_backup.dump
```

**Success Criteria:**
- ✅ Neo4j database dumped successfully
- ✅ Dump file readable and >100 MB
- ✅ Copied to USB
- ✅ Neo4j restarted and healthy

**Risk Level:** MEDIUM
**Recovery:** If export fails, Neo4j still running - data intact

---

#### Task 2.2: Export MySQL Database
```bash
# Create export directory
mkdir -p /tmp/mysql_export

# Dump all MySQL databases
docker exec openspg-mysql mysqldump \
  -u root -popenspg \
  --all-databases \
  --routines \
  --triggers \
  --events \
  > /tmp/mysql_export/mysql_full_backup.sql

# Verify export
ls -lh /tmp/mysql_export/
wc -l /tmp/mysql_export/mysql_full_backup.sql
# Expected: SQL file, 50+ MB, 10000+ lines

# Copy to USB
cp /tmp/mysql_export/mysql_full_backup.sql /mnt/e/AEON_Transfer/
```

**Success Criteria:**
- ✅ MySQL dump created
- ✅ File size >50 MB
- ✅ Copied to USB
- ✅ No errors in export

**Risk Level:** LOW
**Recovery:** MySQL still running - data intact

---

#### Task 2.3: Export MinIO Objects
```bash
# Create export directory
mkdir -p /tmp/minio_export

# Export MinIO data via volume
docker run --rm \
  -v openspg-minio-data:/minio_data \
  -v /tmp/minio_export:/export \
  busybox tar czf /export/minio_data.tar.gz -C /minio_data .

# Verify export
ls -lh /tmp/minio_export/
# Expected: minio_data.tar.gz, ~100 MB

# Copy to USB
cp /tmp/minio_export/minio_data.tar.gz /mnt/e/AEON_Transfer/
```

**Success Criteria:**
- ✅ MinIO data exported
- ✅ Tarball created and readable
- ✅ Copied to USB

**Risk Level:** LOW
**Recovery:** MinIO can be rebuilt from scratch

---

#### Task 2.4: Export Qdrant Vector Database
```bash
# Create export directory
mkdir -p /tmp/qdrant_export

# Check Qdrant health first
curl -s http://localhost:6333/health | jq .
# Expected: {"status": "ok"}

# Export Qdrant collections via API (if data exists)
curl -X POST http://localhost:6333/snapshots/create \
  -H "Content-Type: application/json" \
  > /tmp/qdrant_export/snapshot_create.json

# Check snapshot creation
cat /tmp/qdrant_export/snapshot_create.json
# If successful: {"snapshot_description": {...}}

# If snapshots exist, download them
# Otherwise, Qdrant will be rebuilt from Neo4j data on Mac

# Alternative: Export raw volume data
docker run --rm \
  -v openspg-qdrant-data:/qdrant_data \
  -v /tmp/qdrant_export:/export \
  busybox tar czf /export/qdrant_data.tar.gz -C /qdrant_data .

# Copy to USB
cp /tmp/qdrant_export/qdrant_data.tar.gz /mnt/e/AEON_Transfer/ || true
```

**Success Criteria:**
- ✅ Qdrant snapshot created (or marked as optional)
- ✅ Volume data exported (if exists)
- ✅ Copied to USB (if exists)

**Risk Level:** LOW
**Recovery:** Qdrant can be regenerated from Neo4j data

---

#### Task 2.5: Copy NER11 Models & Training Data
```bash
# Verify archive exists
ls -lh 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz
# Expected: ~439 MB

# Verify archive integrity
tar -tzf 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz | head -20
# Expected: List of model and training files

# Copy to USB (this is large, may take time)
cp 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz /mnt/e/AEON_Transfer/
# Estimated time: 5-10 minutes

# Verify copy
ls -lh /mnt/e/AEON_Transfer/NER11_Gold_Model.tar.gz
# Expected: ~439 MB
```

**Success Criteria:**
- ✅ NER11 archive copied to USB
- ✅ File size matches original
- ✅ Archive integrity verified

**Risk Level:** LOW
**Recovery:** Archive can be recreated from extracted models

---

#### Task 2.6: Create Git Bundle (Full History)
```bash
# Create git bundle with full history
mkdir -p /tmp/git_export

cd /home/jim/2_OXOT_Projects_Dev
git bundle create /tmp/git_export/aeon_complete_history.bundle --all

# Verify bundle
git bundle verify /tmp/git_export/aeon_complete_history.bundle
# Expected: "ok" message

# Copy to USB
cp /tmp/git_export/aeon_complete_history.bundle /mnt/e/AEON_Transfer/

# Also create a simple tar.gz of the .git directory
tar -czf /tmp/git_export/aeon_git_directory.tar.gz .git

# Copy to USB as backup
cp /tmp/git_export/aeon_git_directory.tar.gz /mnt/e/AEON_Transfer/
```

**Success Criteria:**
- ✅ Git bundle created and verified
- ✅ Bundle copied to USB
- ✅ Full git history preserved

**Risk Level:** LOW
**Recovery:** Can clone from GitHub instead

---

#### Task 2.7: Create Migration Manifest & Checksums
```bash
# Create manifest file listing all transferred files
cat > /mnt/e/AEON_Transfer/MIGRATION_MANIFEST.txt << 'EOF'
AEON Digital Twin - macOS Migration Package
Created: 2025-12-04
Source System: WSL2 Linux
Target System: macOS

=== CRITICAL FILES (MUST RESTORE) ===

neo4j_backup.dump
  Description: Neo4j database dump (20,739 nodes)
  Size: ~500 MB
  Restore: On macOS, import into Docker volume

mysql_full_backup.sql
  Description: MySQL database with OpenSPG schema
  Size: ~50 MB
  Restore: On macOS, import into Docker container

NER11_Gold_Model.tar.gz
  Description: Trained NER11 model + training data
  Size: ~439 MB
  Restore: Extract to 5_NER11_Gold_Model/ on macOS

aeon_complete_history.bundle
  Description: Git repository with full history
  Size: ~100 MB
  Restore: Clone on macOS using git bundle

=== OPTIONAL FILES (CAN REGENERATE) ===

minio_data.tar.gz
  Description: MinIO object storage
  Size: ~100 MB
  Note: Can rebuild from scratch if needed

qdrant_data.tar.gz
  Description: Qdrant vector database
  Size: ~200 MB
  Note: Can regenerate from Neo4j data

=== VERIFICATION ===

Total size: ~1.4 GB (fits on USB)
USB required: 8 GB minimum
Transfer time: 10-20 minutes via USB 3.0

EOF

# Create checksums for verification
cd /mnt/e/AEON_Transfer
sha256sum * > CHECKSUMS.txt

# Display manifest
cat MIGRATION_MANIFEST.txt
```

**Success Criteria:**
- ✅ Manifest file created
- ✅ Checksums calculated for all files
- ✅ Total size documented (<8 GB)

**Risk Level:** LOW
**Recovery:** Manually verify files if checksums fail

---

### Phase 3: USB Transfer & Validation (10-15 minutes)
**Goal:** Safely transfer data to USB and validate

#### Task 3.1: Final Verification Before USB Unmounting
```bash
# Verify all critical files on USB
echo "=== Verifying USB Contents ==="
ls -lh /mnt/e/AEON_Transfer/ | tee /tmp/usb_contents.txt

# Check total size
du -sh /mnt/e/AEON_Transfer/
# Expected: ~1.4 GB total

# Verify checksums
cd /mnt/e/AEON_Transfer
sha256sum -c CHECKSUMS.txt
# Expected: All files "OK"

# Count files
ls /mnt/e/AEON_Transfer/ | wc -l
# Expected: 7-10 files
```

**Success Criteria:**
- ✅ All critical files present on USB
- ✅ Total size <8 GB
- ✅ All checksums verified
- ✅ No corrupted files

**Risk Level:** LOW
**Recovery:** Rerun export tasks for failed files

---

#### Task 3.2: Safe USB Unmounting
```bash
# Sync filesystem to ensure all data written
sync

# Unmount USB drive safely
umount /mnt/e
# On Windows/WSL: or right-click "Eject" in File Explorer

# Verify unmounted
mount | grep -E "(e:|E:)" && echo "Still mounted!" || echo "✅ Safely unmounted"

# Physical USB drive is now safe to transfer to Mac
```

**Success Criteria:**
- ✅ USB safely ejected
- ✅ No longer visible in mount list
- ✅ Ready for physical transfer to Mac

**Risk Level:** LOW
**Recovery:** Re-mount if needed

---

#### Task 3.3: Create Handoff Documentation
```bash
# Create README for Mac migration
cat > /home/jim/2_OXOT_Projects_Dev/MAC_MIGRATION_CHECKLIST.md << 'EOF'
# macOS Migration Checklist

**Date:** 2025-12-04
**Status:** WSL2 to macOS transfer

## What's on the USB Drive (8+ GB):

✅ **neo4j_backup.dump** (~500 MB)
   - 20,739 Neo4j nodes
   - Restore on macOS

✅ **mysql_full_backup.sql** (~50 MB)
   - OpenSPG schema and data
   - Import on macOS

✅ **NER11_Gold_Model.tar.gz** (~439 MB)
   - Trained NER11 model
   - Training data (2.1 GB when extracted)

✅ **aeon_complete_history.bundle** (~100 MB)
   - Full git history
   - Use for repository setup

## macOS Setup Steps:

1. Install Docker Desktop for Mac (or OrbStack)
2. Install Python 3.11, Node.js, Homebrew
3. Mount USB drive
4. Follow 01_MAC_SETUP.md
5. Follow 02_DATA_RESTORATION.md
6. Follow 03_VALIDATION.md

## Expected Outcome:

- ✅ All 251+ API endpoints functional
- ✅ Neo4j with 20,739 nodes restored
- ✅ NER11 model operational
- ✅ All Docker containers healthy
- ✅ Development ready on macOS

EOF

# Copy to USB as well
cp /home/jim/2_OXOT_Projects_Dev/MAC_MIGRATION_CHECKLIST.md /mnt/e/AEON_Transfer/
```

**Success Criteria:**
- ✅ Handoff documentation created
- ✅ Checklist ready for Mac team member
- ✅ Clear next steps documented

**Risk Level:** LOW
**Recovery:** N/A

---

### Phase 4: macOS Setup (30-60 minutes)
**Goal:** Prepare macOS environment for data restoration

#### Task 4.1: Install Homebrew & Docker Desktop
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Docker Desktop for Mac (RECOMMENDED)
brew install --cask docker

# Alternative: Install OrbStack (faster, better for M1/M2/M3)
# brew install --cask orbstack

# Verify Docker installation
docker --version
docker ps
# Expected: "Docker version 24.x.x" and container list
```

**Success Criteria:**
- ✅ Homebrew installed
- ✅ Docker Desktop (or alternative) installed
- ✅ Docker commands work

**Risk Level:** LOW
**Recovery:** Reinstall if needed

---

#### Task 4.2: Install Development Tools
```bash
# Install Python 3.11
brew install python@3.11

# Install Node.js
brew install node@18

# Install Git (usually pre-installed on Mac)
brew install git

# Install other useful tools
brew install git-lfs
brew install jq
brew install curl

# Verify installations
python3 --version  # Python 3.11.x
node --version     # v18.x.x
npm --version      # 9.x.x
```

**Success Criteria:**
- ✅ Python 3.11 installed
- ✅ Node.js 18+ installed
- ✅ Git installed
- ✅ All versions verified

**Risk Level:** LOW
**Recovery:** Reinstall individual tools if needed

---

#### Task 4.3: Create Project Directory Structure
```bash
# Create main project directory
mkdir -p ~/Projects/AEON_DT_Project
cd ~/Projects/AEON_DT_Project

# Create subdirectories
mkdir -p {backups,docker_volumes,logs,temp}

# Verify structure
tree -L 1
# Expected: backups, docker_volumes, logs, temp directories
```

**Success Criteria:**
- ✅ Project directory created
- ✅ Subdirectories for data organization
- ✅ Ready for data restoration

**Risk Level:** LOW
**Recovery:** Create manually if script fails

---

#### Task 4.4: Mount USB Drive & Verify Contents
```bash
# USB will be automatically mounted on Mac when plugged in
# Usually appears as /Volumes/[USB_NAME]/

# Find USB mount point
df -h | grep -E "Volumes"
# Expected: /Volumes/[Name] with 8+ GB

# Navigate to USB
cd /Volumes/[USB_NAME]/AEON_Transfer

# Verify contents
ls -lh
# Expected: All critical files listed

# Verify checksums
sha256sum -c CHECKSUMS.txt
# Expected: All files "OK"
```

**Success Criteria:**
- ✅ USB drive mounted
- ✅ All files visible
- ✅ Checksums verified (all OK)
- ✅ Data integrity confirmed

**Risk Level:** LOW
**Recovery:** Re-mount USB if needed

---

#### Task 4.5: Create Docker Network & Volumes
```bash
# Create Docker network (must match original)
docker network create openspg-network

# Create Docker volumes
docker volume create openspg-neo4j-data
docker volume create openspg-mysql-data
docker volume create openspg-minio-data
docker volume create openspg-qdrant-data
docker volume create openspg-redis-data
docker volume create aeon-postgres-dev

# Verify volumes created
docker volume ls | grep openspg
# Expected: 6 openspg volumes listed
```

**Success Criteria:**
- ✅ Docker network created
- ✅ All volumes created
- ✅ Network and volumes verified

**Risk Level:** LOW
**Recovery:** Delete and recreate if needed

---

### Phase 5: Data Restoration (45-90 minutes)
**Goal:** Restore all data from USB to macOS

#### Task 5.1: Restore Git Repository
```bash
# Option 1: Use git bundle (fastest)
cd ~/Projects/AEON_DT_Project

git clone -b gap-002-clean-VERIFIED \
  /Volumes/[USB_NAME]/AEON_Transfer/aeon_complete_history.bundle \
  .

# Option 2: Clone from GitHub (if bundle fails)
git clone https://github.com/Planet9V/agent-optimization-deployment.git .
git checkout gap-002-clean-VERIFIED

# Verify git history
git log --oneline -5
# Expected: Recent commits visible including Phase B5

# Verify status is clean
git status
# Expected: "nothing to commit, working tree clean"
```

**Success Criteria:**
- ✅ Repository cloned
- ✅ Full git history available
- ✅ On correct branch
- ✅ Clean working directory

**Risk Level:** MEDIUM
**Recovery:** Clone from GitHub instead

---

#### Task 5.2: Extract NER11 Models & Training Data
```bash
cd ~/Projects/AEON_DT_Project/5_NER11_Gold_Model

# Copy archive from USB
cp /Volumes/[USB_NAME]/AEON_Transfer/NER11_Gold_Model.tar.gz .

# Extract (this creates 3.5 GB of files)
tar xzf NER11_Gold_Model.tar.gz
# Expected: 2-3 minute extraction time

# Verify extraction
ls -la models/ner11_v3/model-best/
# Expected: Model files present

# Verify training data
ls -la training_data/
# Expected: Custom data, external data directories

# Remove archive copy (now on disk)
rm NER11_Gold_Model.tar.gz
```

**Success Criteria:**
- ✅ Archive extracted
- ✅ Model files present
- ✅ Training data accessible
- ✅ Disk space sufficient (~3.5 GB)

**Risk Level:** MEDIUM
**Recovery:** Re-extract from USB if needed

---

#### Task 5.3: Restore Neo4j Database
```bash
# Copy backup from USB
cp /Volumes/[USB_NAME]/AEON_Transfer/neo4j_backup.dump \
   ~/Projects/AEON_DT_Project/backups/

# Pull Neo4j image
docker pull neo4j:5.26-community

# Restore Neo4j database from dump
docker run --rm \
  -v openspg-neo4j-data:/data \
  -v ~/Projects/AEON_DT_Project/backups:/backups \
  neo4j:5.26-community \
  neo4j-admin database load neo4j \
  --from-path=/backups

# Start Neo4j container
docker run -d \
  --name openspg-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -v openspg-neo4j-data:/data \
  -e NEO4J_AUTH=neo4j/neo4j@openspg \
  neo4j:5.26-community

# Wait for Neo4j to start (30 seconds)
sleep 30

# Verify Neo4j is healthy
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n) as total_nodes"
# Expected: 20739 (matches original)
```

**Success Criteria:**
- ✅ Neo4j backup restored
- ✅ Container started
- ✅ All 20,739 nodes present
- ✅ Database queries work

**Risk Level:** MEDIUM
**Recovery:** Re-load from backup if corruption detected

---

#### Task 5.4: Restore MySQL Database
```bash
# Copy backup from USB
cp /Volumes/[USB_NAME]/AEON_Transfer/mysql_full_backup.sql \
   ~/Projects/AEON_DT_Project/backups/

# Pull MySQL image
docker pull mysql:8.0

# Start MySQL container
docker run -d \
  --name openspg-mysql \
  -p 3306:3306 \
  -v openspg-mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=openspg \
  -e MYSQL_DATABASE=openspg \
  mysql:8.0

# Wait for MySQL to start (30 seconds)
sleep 30

# Restore MySQL database
docker exec -i openspg-mysql mysql \
  -u root -popenspg < ~/Projects/AEON_DT_Project/backups/mysql_full_backup.sql

# Verify MySQL is healthy
docker exec openspg-mysql mysql \
  -u root -popenspg -e "SHOW DATABASES;"
# Expected: openspg and other databases listed
```

**Success Criteria:**
- ✅ MySQL backup restored
- ✅ Container started
- ✅ Database accessible
- ✅ Schema verified

**Risk Level:** MEDIUM
**Recovery:** Re-import from backup if needed

---

#### Task 5.5: Restore Other Docker Volumes (Optional)
```bash
# MinIO (optional)
if [ -f /Volumes/[USB_NAME]/AEON_Transfer/minio_data.tar.gz ]; then
  docker run --rm \
    -v openspg-minio-data:/data \
    -v /Volumes/[USB_NAME]/AEON_Transfer:/backup \
    busybox tar xzf /backup/minio_data.tar.gz -C /data
fi

# Qdrant (optional - can regenerate)
if [ -f /Volumes/[USB_NAME]/AEON_Transfer/qdrant_data.tar.gz ]; then
  docker run --rm \
    -v openspg-qdrant-data:/data \
    -v /Volumes/[USB_NAME]/AEON_Transfer:/backup \
    busybox tar xzf /backup/qdrant_data.tar.gz -C /data
fi
```

**Success Criteria:**
- ✅ Optional volumes restored (or skipped)
- ✅ If skipped, can be rebuilt on Mac

**Risk Level:** LOW
**Recovery:** Regenerate from Neo4j data if needed

---

#### Task 5.6: Setup Python Environment
```bash
cd ~/Projects/AEON_DT_Project/5_NER11_Gold_Model

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Create Mac-specific requirements (no CUDA)
cat > requirements.mac.txt << 'EOF'
spacy>=3.7.0
spacy-transformers
torch>=2.0.0
pandas
numpy
tqdm
fastapi
uvicorn
requests
neo4j
sentence-transformers
qdrant-client
pydantic
EOF

# Install dependencies
pip install -r requirements.mac.txt
# Expected: 10-20 minutes installation time

# Download spaCy models
python -m spacy download en_core_web_sm
```

**Success Criteria:**
- ✅ Virtual environment created
- ✅ All Python dependencies installed
- ✅ spaCy models downloaded
- ✅ No errors during installation

**Risk Level:** MEDIUM
**Recovery:** Recreate venv if installation fails

---

### Phase 6: Verification & Validation (30-45 minutes)
**Goal:** Verify all systems working correctly on macOS

#### Task 6.1: Database Health Checks
```bash
# Neo4j health
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n:Threat) RETURN COUNT(n) as threat_count"
# Expected: 9875 threats

# MySQL health
docker exec openspg-mysql mysql -u root -popenspg -e \
  "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='openspg';"
# Expected: Tables count

# Test API connectivity
curl http://localhost:8000/health
# Expected: JSON response or {"status": "ok"}
```

**Success Criteria:**
- ✅ Neo4j responding with correct node counts
- ✅ MySQL databases accessible
- ✅ APIs responding to health checks

**Risk Level:** LOW
**Recovery:** Check container logs if failures

---

#### Task 6.2: NER11 Model Testing
```bash
cd ~/Projects/AEON_DT_Project/5_NER11_Gold_Model
source venv/bin/activate

# Test model loading
python -c "
import spacy
nlp = spacy.load('models/ner11_v3/model-best')
print('✅ Model loaded successfully')
"

# Test inference
python << 'EOF'
import spacy
nlp = spacy.load('models/ner11_v3/model-best')

text = "CVE-2024-1234 is a critical vulnerability in Apache Struts"
doc = nlp(text)

print("✅ Text processing successful")
print(f"Entities found: {len(doc.ents)}")
for ent in doc.ents:
    print(f"  - {ent.text} ({ent.label_})")
EOF
```

**Success Criteria:**
- ✅ Model loads without errors
- ✅ Inference works
- ✅ Named entities detected
- ✅ No GPU errors (CPU mode works)

**Risk Level:** LOW
**Recovery:** Check model files if loading fails

---

#### Task 6.3: Frontend Development Environment
```bash
cd ~/Projects/AEON_DT_Project/1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1

# Install Node dependencies
npm install
# Expected: 2-5 minutes

# Verify Next.js setup
npm list next
# Expected: next@14.x.x or similar

# Test build (optional)
npm run build
# Expected: Compilation successful
```

**Success Criteria:**
- ✅ npm dependencies installed
- ✅ Next.js configured
- ✅ Frontend code compiles

**Risk Level:** LOW
**Recovery:** Clean npm cache and reinstall if needed

---

#### Task 6.4: Full System Smoke Test
```bash
# Create comprehensive test script
cat > ~/test_aeon_mac.sh << 'EOF'
#!/bin/bash

echo "=== AEON Digital Twin macOS Validation ==="
echo "Date: $(date)"
echo ""

# Test 1: Docker containers
echo "✓ Docker Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}"
echo ""

# Test 2: Neo4j
echo "✓ Neo4j Node Count:"
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n) as count" 2>/dev/null | grep -E "[0-9]+"
echo ""

# Test 3: MySQL
echo "✓ MySQL Status:"
docker exec openspg-mysql mysql -u root -popenspg -e "SELECT VERSION();" 2>/dev/null
echo ""

# Test 4: NER11 Model
echo "✓ NER11 Model Loading:"
cd ~/Projects/AEON_DT_Project/5_NER11_Gold_Model
source venv/bin/activate
python -c "import spacy; nlp = spacy.load('models/ner11_v3/model-best'); print('✓ Model loaded')" 2>/dev/null
cd - > /dev/null
echo ""

# Test 5: API Endpoints
echo "✓ API Endpoints:"
curl -s http://localhost:8000/health | head -1
echo ""

# Test 6: Frontend Code
echo "✓ Frontend Code:"
cd ~/Projects/AEON_DT_Project/1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1
if [ -f "package.json" ]; then
  echo "✓ Frontend project found"
else
  echo "✗ Frontend project missing"
fi
cd - > /dev/null
echo ""

echo "=== Validation Complete ==="
EOF

# Make script executable and run
chmod +x ~/test_aeon_mac.sh
~/test_aeon_mac.sh
```

**Success Criteria:**
- ✅ All Docker containers running
- ✅ Neo4j has 20,739 nodes
- ✅ MySQL accessible
- ✅ NER11 model loads
- ✅ API responds
- ✅ Frontend code present

**Risk Level:** LOW
**Recovery:** Check individual component logs if failures

---

#### Task 6.5: Performance Baseline & Documentation
```bash
# Document macOS system configuration
cat > ~/Projects/AEON_DT_Project/MAC_SETUP_SUMMARY.md << 'EOF'
# macOS Setup Summary

**Date:** $(date)
**System:** macOS [Version]
**Processor:** [Model]
**RAM:** [Amount]
**Disk:** [Amount free]

## Installed Components

- Docker Desktop: [Version]
- Python: [Version]
- Node.js: [Version]
- Git: [Version]

## Database Status

- Neo4j: ✅ Restored (20,739 nodes)
- MySQL: ✅ Restored
- MinIO: ⚠️ [Status]
- Qdrant: ⚠️ [Status]
- Redis: ✅ Running

## Model Status

- NER11: ✅ Loaded (3.5 GB extracted)
- Training data: ✅ Available (2.1 GB)

## Frontend Status

- Next.js: ✅ Configured
- Dependencies: ✅ Installed
- Build: ✅ Passing

## Performance Notes

- Neo4j query time: [measure]
- NER11 inference time (single document): [measure]
- API response time: [measure]

## Known Differences vs WSL2

- ⚠️ No CUDA - using CPU inference (slower)
- ✅ Or: Using Metal GPU (MPS) if M1/M2/M3
- ✅ Docker Desktop (alternative: OrbStack)
- ✅ Native Apple Silicon if applicable

## Next Steps

1. Continue development on macOS
2. Keep WSL2 system as backup until verified
3. Commit Mac-specific configuration changes
4. Update team with setup guide

EOF

# Display summary
cat ~/Projects/AEON_DT_Project/MAC_SETUP_SUMMARY.md
```

**Success Criteria:**
- ✅ Setup documented
- ✅ Performance baseline recorded
- ✅ Known differences documented
- ✅ Next steps clear

**Risk Level:** LOW
**Recovery:** Manually create summary if needed

---

## Migration Checklist & Rollback Plans

### Pre-Migration Checklist (Phase 1)

- [ ] All code committed to git
- [ ] Git pushed to remote (origin)
- [ ] Migration tag created
- [ ] Docker containers healthy
- [ ] NER11 archive verified
- [ ] USB drive formatted and tested
- [ ] USB capacity >8 GB confirmed

### Data Export Checklist (Phase 2)

- [ ] Neo4j dump created (~500 MB)
- [ ] MySQL backup created (~50 MB)
- [ ] MinIO data exported (~100 MB, optional)
- [ ] Qdrant data exported (~200 MB, optional)
- [ ] NER11 models copied (439 MB)
- [ ] Git bundle created (100 MB)
- [ ] All files copied to USB
- [ ] Checksums verified

### Mac Setup Checklist (Phase 4)

- [ ] Homebrew installed
- [ ] Docker Desktop installed
- [ ] Python 3.11 installed
- [ ] Node.js installed
- [ ] Git installed
- [ ] USB drive mounted and verified
- [ ] Docker network created
- [ ] Docker volumes created

### Data Restoration Checklist (Phase 5)

- [ ] Git repository cloned
- [ ] NER11 models extracted
- [ ] Neo4j database restored
- [ ] MySQL database restored
- [ ] Optional volumes restored
- [ ] Python dependencies installed
- [ ] spaCy models downloaded

### Validation Checklist (Phase 6)

- [ ] Neo4j healthy (20,739 nodes)
- [ ] MySQL healthy
- [ ] NER11 model loads
- [ ] API endpoints respond
- [ ] Frontend builds
- [ ] All tests passing
- [ ] Performance documented

---

## Rollback Procedures

### If Export Fails (During Phase 2)
**Action:** Stop, investigate error, re-run failed task
**Recovery:** No changes to WSL2 - data remains intact
**Next:** Fix issue and retry export

### If USB Transfer Fails (During Phase 3)
**Action:** Re-copy failed files from WSL2 to USB
**Recovery:** WSL2 data untouched
**Next:** Verify checksums before proceeding

### If macOS Restoration Fails (During Phase 5)
**Action:** Delete partial restoration and retry
**Recovery:** USB files remain unchanged
**Next:** Re-run restoration task with debugging

### If Validation Fails (During Phase 6)
**Action:** Check container logs and investigate
**Recovery:** WSL2 system still fully operational
**Decision:** Fix on macOS OR continue using WSL2

---

## Disaster Recovery

### If Complete Mac Setup Fails
1. **Keep WSL2 system operational** (primary backup)
2. **Store USB data safely** (secondary backup)
3. **Git repository on GitHub** (tertiary backup)
4. **Restart macOS migration** when issues resolved

### If WSL2 Becomes Corrupted
1. **Data is on USB** - Can restore to Mac or new Linux
2. **Git is on GitHub** - Can reclone repository
3. **Models are archived** - Can be re-extracted

### Data Recovery Priority
1. **Most Critical:** Git repository (in GitHub)
2. **High Priority:** Docker volumes (on USB)
3. **High Priority:** NER11 models (on USB)
4. **Medium Priority:** Training data (on USB)

---

## Estimated Resource Requirements

### WSL2 System (Source)
- **Disk Space:** 5-6 GB free for exports
- **Time:** 1.5-2 hours total
- **Downtime:** Minimal (containers stay running)

### macOS System (Target)
- **Disk Space:** 10 GB minimum (20 GB recommended)
- **RAM:** 16 GB recommended for Docker
- **CPU:** Any Mac from 2018 or newer
- **Internet:** Required for downloads (~2 GB)

### USB Drive
- **Capacity:** 8 GB minimum, 16 GB recommended
- **Format:** NTFS or ExFAT (works on Mac)
- **Speed:** USB 3.0+ recommended for faster transfer

---

## Summary: Key Decisions

**Selected Approach:** Hybrid Strategy (Option C)
- **Code:** Clone from GitHub (clean, versioned)
- **Data:** Export Docker volumes via USB (complete)
- **Models:** Transfer via USB (faster than download)
- **Dependencies:** Fresh install on macOS (cleaner)

**macOS Environment:**
- **Docker:** Docker Desktop (official, well-supported)
- **GPU:** None (CUDA unavailable) → Use CPU or Metal GPU if M1/M2/M3
- **Python:** 3.11 (via Homebrew)
- **Node.js:** 18+ (via Homebrew)

**Timeline:** 3-5 hours total
**Risk Level:** LOW (comprehensive backups, WSL2 stays intact)
**Success Probability:** 95%+ (with proper execution)

---

## Next Document in Series

→ **01_PRE_MIGRATION_CHECKLIST.md** - Detailed checklist before starting
→ **02_DATA_EXPORT_PROCEDURES.md** - Step-by-step export procedures
→ **03_MAC_SETUP_GUIDE.md** - macOS environment setup
→ **04_DATA_RESTORATION_GUIDE.md** - Restore data on Mac
→ **05_VALIDATION_PROCEDURES.md** - Verify everything works

---

*This is a comprehensive planning document. Do NOT execute these commands yet.*
*Follow the detailed guides in separate documents for each phase.*
*Complete all Phase 1 preparation before proceeding to Phase 2.*

**Migration Status:** PLANNING COMPLETE ✅ - Ready for detailed procedure documentation
