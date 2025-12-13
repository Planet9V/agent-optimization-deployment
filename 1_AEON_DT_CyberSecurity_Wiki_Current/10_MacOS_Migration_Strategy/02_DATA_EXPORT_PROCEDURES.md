# Data Export Procedures - Phase 2 Data Collection & Export

**File:** 02_DATA_EXPORT_PROCEDURES.md
**Created:** 2025-12-04 12:15:00 UTC
**Purpose:** Step-by-step procedures to export critical data from WSL2 to USB
**Status:** PLANNING PHASE - Ready for execution after pre-migration checklist passes
**Phase:** 2 of 6 (Data Collection & Export)
**Estimated Duration:** 45-90 minutes
**Preconditions:** All items in 01_PRE_MIGRATION_CHECKLIST.md must be completed

---

## ⚠️ Pre-Execution Requirements

### Verify Preconditions
Before starting any export procedures, confirm:
- ✅ Pre-migration checklist FULLY COMPLETED
- ✅ Git working directory CLEAN (all 20 files committed and pushed)
- ✅ NER11 archive verified as uncorrupted
- ✅ All Docker containers HEALTHY
- ✅ USB drive mounted at `/mnt/e` with >8 GB free
- ✅ System snapshot documented

### Safety Checkpoints
- **Checkpoint A:** Before starting exports (verify preconditions)
- **Checkpoint B:** After each major component export (verify checksum)
- **Checkpoint C:** After all exports complete (verify USB contents)

---

## Phase 2 Overview

**Objective:** Export all critical data from WSL2 Docker volumes and file system to USB

**Components to Export:**
1. Neo4j database dump (20K+ nodes)
2. MySQL OpenSPG schema
3. MinIO object storage (optional)
4. Qdrant vector database (optional)
5. NER11 model archive
6. Git repository bundle (code backup)
7. Checksums and manifest file

**Success Criteria:**
- All components successfully exported to USB
- Checksums verified for integrity
- Manifest file created with file inventory
- USB space usage <8 GB
- Recovery instructions documented

---

## Task 2.1: Create Staging Directory Structure

### Purpose
Create organized directories on USB to store exports with clear naming and organization.

### Procedure

```bash
# 1. Navigate to USB staging directory
cd /mnt/e/AEON_Transfer

# 2. Create subdirectories for each component
mkdir -p database/{neo4j,mysql}
mkdir -p models/ner11
mkdir -p git_backup
mkdir -p checksums
mkdir -p manifests

# 3. Create timestamp for this migration session
MIGRATION_DATE=$(date +%Y-%m-%d_%H-%M-%S)
mkdir -p "$MIGRATION_DATE"

# 4. Create README for USB contents
cat > /mnt/e/AEON_Transfer/README_USB_CONTENTS.txt << 'EOF'
AEON Digital Twin - macOS Migration USB Contents
================================================

Created: $(date)
Migration Type: WSL2 to macOS
Source System: Linux WSL2
Target System: macOS

DIRECTORY STRUCTURE:
-------------------
database/neo4j/          → Neo4j database dump files
database/mysql/         → MySQL backup files
models/ner11/          → NER11 model archive and extracted models
git_backup/            → Git repository bundle and clones
checksums/             → SHA256 checksums for verification
manifests/             → File inventory and metadata

TOTAL SIZE: [Will be populated after export]

NEXT STEPS:
-----------
1. After transferring to macOS, read 03_MAC_SETUP_GUIDE.md
2. Follow procedures in 04_DATA_RESTORATION_GUIDE.md
3. Verify restoration with 05_VALIDATION_PROCEDURES.md

CRITICAL FILES:
---------------
- manifest.txt                 → Complete file inventory
- checksums.sha256            → Integrity verification
- MIGRATION_NOTES.md          → This migration's notes

STORAGE ALLOCATION (Estimated):
- Neo4j dump: 500 MB
- MySQL dump: 50 MB
- NER11 models: 976 MB (archive) + 3.5 GB (extracted)
- Git backup: 100 MB
- Other: 100 MB
TOTAL: ~5.5 GB
EOF

# 5. Verify structure
ls -la /mnt/e/AEON_Transfer/

echo "✅ Staging directory structure created successfully"
```

**Expected Output:**
```
drwxr-xr-x database
drwxr-xr-x models
drwxr-xr-x git_backup
drwxr-xr-x checksums
drwxr-xr-x manifests
-rw-r--r-- README_USB_CONTENTS.txt
```

**Success Criteria:** All directories created, README file written

---

## Task 2.2: Export Neo4j Database

### Purpose
Dump Neo4j database with 20,739 nodes to preservable format for macOS restoration.

### Important Notes
- **Online Export:** Does NOT require stopping Neo4j container
- **Consistency:** Neo4j backup ensures transactional consistency
- **Size:** Expected ~500 MB dump file
- **Format:** Binary backup format (can be restored directly)

### Procedure

```bash
# 1. Get Neo4j container ID
NEO4J_CONTAINER=$(docker ps --filter "name=openspg-neo4j" --format "{{.ID}}")
echo "Neo4j Container ID: $NEO4J_CONTAINER"

# 2. Verify Neo4j is healthy and has data
docker exec $NEO4J_CONTAINER cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n) as node_count, \
          COUNT(DISTINCT labels(n)) as entity_types"
# Expected: node_count: 20739, entity_types: 45+

# 3. Create backup directory
mkdir -p /mnt/e/AEON_Transfer/database/neo4j/backups

# 4. Get current date for backup naming
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)

# 5. Create backup using neo4j admin tool
# Method A: Full backup (recommended)
docker exec $NEO4J_CONTAINER neo4j-admin database dump neo4j \
  /backups/neo4j_backup_${BACKUP_DATE}.dump

# 6. Copy backup from container to USB
docker cp $NEO4J_CONTAINER:/backups/neo4j_backup_${BACKUP_DATE}.dump \
  /mnt/e/AEON_Transfer/database/neo4j/

# 7. Verify backup file
ls -lh /mnt/e/AEON_Transfer/database/neo4j/neo4j_backup_${BACKUP_DATE}.dump

# 8. Create backup metadata
cat > /mnt/e/AEON_Transfer/database/neo4j/BACKUP_METADATA.txt << EOF
Neo4j Database Backup
====================
Date: $(date)
Container: $NEO4J_CONTAINER
Database Name: neo4j
Node Count: 20739 (verified)
Backup Format: neo4j-admin dump
File: neo4j_backup_${BACKUP_DATE}.dump

RESTORATION PROCEDURE:
1. Place this file in /var/lib/neo4j/backups/
2. Run: neo4j-admin database load neo4j
3. Restart Neo4j container

NOTES:
- Includes all 45+ entity types
- Includes all relationships
- Binary format (requires neo4j-admin to restore)
- Transactionally consistent at backup time
EOF

# 9. Calculate checksum
sha256sum /mnt/e/AEON_Transfer/database/neo4j/neo4j_backup_${BACKUP_DATE}.dump \
  > /mnt/e/AEON_Transfer/checksums/neo4j_backup_${BACKUP_DATE}.sha256

# 10. Display confirmation
echo "✅ Neo4j backup completed"
echo "📦 Backup file: neo4j_backup_${BACKUP_DATE}.dump"
du -h /mnt/e/AEON_Transfer/database/neo4j/neo4j_backup_${BACKUP_DATE}.dump

# 11. Verify integrity
cat /mnt/e/AEON_Transfer/checksums/neo4j_backup_${BACKUP_DATE}.sha256
```

**Expected Output:**
```
✅ Neo4j backup completed
📦 Backup file: neo4j_backup_20251204_121500.dump
500M /mnt/e/AEON_Transfer/database/neo4j/neo4j_backup_20251204_121500.dump
```

**Success Criteria:**
- Backup file created and visible on USB
- Checksum file generated
- Metadata file created with restoration instructions

---

## Task 2.3: Export MySQL Database

### Purpose
Backup MySQL OpenSPG schema for restoration on macOS.

### Procedure

```bash
# 1. Get MySQL container ID
MYSQL_CONTAINER=$(docker ps --filter "name=openspg-mysql" --format "{{.ID}}")
echo "MySQL Container ID: $MYSQL_CONTAINER"

# 2. Get current date
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)

# 3. Create MySQL dump (includes all schemas and data)
docker exec $MYSQL_CONTAINER mysqldump -u root -popenspg \
  --all-databases \
  --single-transaction \
  --quick \
  --lock-tables=false \
  > /mnt/e/AEON_Transfer/database/mysql/openspg_dump_${BACKUP_DATE}.sql

# 4. Compress to save space
gzip /mnt/e/AEON_Transfer/database/mysql/openspg_dump_${BACKUP_DATE}.sql

# 5. Verify backup
ls -lh /mnt/e/AEON_Transfer/database/mysql/openspg_dump_${BACKUP_DATE}.sql.gz

# 6. Create metadata
cat > /mnt/e/AEON_Transfer/database/mysql/BACKUP_METADATA.txt << EOF
MySQL Database Backup
====================
Date: $(date)
Container: $MYSQL_CONTAINER
Backup Type: Full schema dump
Format: SQL (gzipped)
File: openspg_dump_${BACKUP_DATE}.sql.gz

RESTORATION PROCEDURE:
1. Decompress: gunzip openspg_dump_${BACKUP_DATE}.sql.gz
2. Import: mysql -u root -p < openspg_dump_${BACKUP_DATE}.sql
3. Verify schemas loaded

NOTES:
- Includes all databases created by OpenSPG
- Single transaction for consistency
- Can be imported to fresh MySQL instance
EOF

# 7. Calculate checksum
sha256sum /mnt/e/AEON_Transfer/database/mysql/openspg_dump_${BACKUP_DATE}.sql.gz \
  > /mnt/e/AEON_Transfer/checksums/mysql_dump_${BACKUP_DATE}.sha256

# 8. Display confirmation
echo "✅ MySQL backup completed"
du -h /mnt/e/AEON_Transfer/database/mysql/openspg_dump_${BACKUP_DATE}.sql.gz
```

**Expected Output:**
```
✅ MySQL backup completed
50M /mnt/e/AEON_Transfer/database/mysql/openspg_dump_20251204_121500.sql.gz
```

**Success Criteria:**
- Compressed dump file created
- Checksum generated
- Metadata documented

---

## Task 2.4: Copy NER11 Model Archive

### Purpose
Transfer NER11 Gold Model archive to USB (439 MB compressed, ~3.5 GB extracted).

### Procedure

```bash
# 1. Verify archive exists and is intact (should be done in pre-migration)
if [ -f "5_NER11_Gold_Model/NER11_Gold_Model.tar.gz" ]; then
  echo "✅ Archive exists"
  ls -lh 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz
else
  echo "❌ Archive not found - ABORT"
  exit 1
fi

# 2. Verify archive integrity
tar -tzf 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✅ Archive integrity verified"
else
  echo "❌ Archive corrupted - ABORT"
  exit 1
fi

# 3. Copy archive to USB
cp 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz \
   /mnt/e/AEON_Transfer/models/ner11/

# 4. Copy extracted models directory (optional but recommended)
# This saves extraction time on macOS
if [ -d "5_NER11_Gold_Model/models/ner11_v3/model-best" ]; then
  echo "Copying extracted models directory..."
  cp -r 5_NER11_Gold_Model/models \
        /mnt/e/AEON_Transfer/models/ner11/models_extracted
  cp -r 5_NER11_Gold_Model/training_data \
        /mnt/e/AEON_Transfer/models/ner11/training_data_copy
fi

# 5. Verify copies
echo "Archive size:"
ls -lh /mnt/e/AEON_Transfer/models/ner11/NER11_Gold_Model.tar.gz

if [ -d "/mnt/e/AEON_Transfer/models/ner11/models_extracted" ]; then
  echo "Extracted models size:"
  du -sh /mnt/e/AEON_Transfer/models/ner11/models_extracted
fi

# 6. Calculate checksums
cd /mnt/e/AEON_Transfer/models/ner11/
sha256sum NER11_Gold_Model.tar.gz \
  > /mnt/e/AEON_Transfer/checksums/ner11_archive.sha256

# 7. Create model metadata
cat > /mnt/e/AEON_Transfer/models/ner11/MODEL_METADATA.txt << 'EOF'
NER11 Gold Model Archive
========================
Date Created: 2025-12-04
Archive Format: tar.gz (compressed)
Archive Size: 439 MB
Extracted Size: 3.5 GB
Compression Ratio: 7.96x

CONTENTS:
- models/ner11_v3/model-best/         → Trained spaCy transformer model
- models/ner11_v3/config.cfg          → Model configuration
- training_data/                      → Training datasets and vectors
  └── *.txt, *.csv files for NER training

TECHNICAL SPECS:
- Framework: spaCy 3.x
- Model Type: Transformer-based NER
- Training: GPU-trained (CUDA 11.x)
- Performance: >95% F1 on test set
- Deployment: Works CPU-only (no GPU required)

RESTORATION OPTIONS:
1. Using archive (recommended for transfer):
   tar -xzf NER11_Gold_Model.tar.gz -C /path/to/project/

2. Using extracted copy (if included on USB):
   cp -r models_extracted/* /path/to/project/5_NER11_Gold_Model/models/

USAGE ON MACOS:
python -m spacy info models/ner11_v3/model-best
python -c "import spacy; nlp = spacy.load('models/ner11_v3/model-best')"
EOF

echo "✅ NER11 models exported successfully"
```

**Expected Output:**
```
✅ Archive exists
✅ Archive integrity verified
Archive size:
439M /mnt/e/AEON_Transfer/models/ner11/NER11_Gold_Model.tar.gz
Extracted models size:
3.5G /mnt/e/AEON_Transfer/models/ner11/models_extracted
✅ NER11 models exported successfully
```

**Success Criteria:**
- Archive copied to USB
- Checksums generated
- Metadata documented
- (Optionally) Extracted models also copied

---

## Task 2.5: Create Git Repository Bundle

### Purpose
Create a complete Git repository bundle as backup/transfer mechanism for code.

### Procedure

```bash
# 1. Navigate to project root
cd /home/jim/2_OXOT_Projects_Dev

# 2. Verify clean git status
git status
# Expected: "nothing to commit, working tree clean"

# 3. Verify all commits are pushed
git log --oneline -1
# Show the latest commit

# 4. Create git bundle (includes all branches and history)
BUNDLE_DATE=$(date +%Y%m%d_%H%M%S)
git bundle create /mnt/e/AEON_Transfer/git_backup/aeon_complete_${BUNDLE_DATE}.bundle \
  --all \
  --branches \
  --tags

# 5. Verify bundle size and contents
ls -lh /mnt/e/AEON_Transfer/git_backup/aeon_complete_${BUNDLE_DATE}.bundle

# 6. Verify bundle integrity
git bundle verify /mnt/e/AEON_Transfer/git_backup/aeon_complete_${BUNDLE_DATE}.bundle

# 7. Create bundle metadata
cat > /mnt/e/AEON_Transfer/git_backup/BUNDLE_METADATA.txt << EOF
Git Repository Bundle
===================
Date Created: $(date)
Project: AEON Digital Twin
Repository: gap-002-clean-VERIFIED branch
File: aeon_complete_${BUNDLE_DATE}.bundle

CONTENTS:
- All branches
- All tags
- Complete commit history
- All remote references

RESTORATION PROCEDURE (macOS):
1. Create new directory: mkdir -p ~/Projects/aeon-dt
2. Clone from bundle: git clone aeon_complete_${BUNDLE_DATE}.bundle ~/Projects/aeon-dt
3. Navigate: cd ~/Projects/aeon-dt
4. Add remote: git remote add origin https://github.com/[repo-url]
5. Fetch from GitHub: git fetch origin

NOTES:
- Bundle is self-contained (doesn't require GitHub access)
- Can be used as complete backup
- Can be transferred to any machine with git installed
- Includes full history for git blame, git bisect, etc.
EOF

# 8. Calculate checksum
sha256sum /mnt/e/AEON_Transfer/git_backup/aeon_complete_${BUNDLE_DATE}.bundle \
  > /mnt/e/AEON_Transfer/checksums/git_bundle_${BUNDLE_DATE}.sha256

# 9. Display confirmation
echo "✅ Git bundle created successfully"
git log --oneline -10 | head -1
echo "Latest commit bundled"
```

**Expected Output:**
```
✅ Git bundle created successfully
[Latest commit hash] Latest commit message
```

**Success Criteria:**
- Bundle file created on USB
- Bundle integrity verified
- Metadata documented

---

## Task 2.6: Create Checksum Manifest

### Purpose
Create comprehensive checksum file for integrity verification on macOS.

### Procedure

```bash
# 1. Navigate to USB checksums directory
cd /mnt/e/AEON_Transfer/checksums

# 2. Create combined checksum file from all individual files
cat > CHECKSUMS_COMPLETE.sha256 << 'EOF'
# AEON Digital Twin - Migration USB Checksums
# Created: $(date)
# For verification: sha256sum -c CHECKSUMS_COMPLETE.sha256
# This file contains SHA256 checksums for all critical data files

EOF

# 3. Add Neo4j backup checksums
cat neo4j_backup_*.sha256 >> CHECKSUMS_COMPLETE.sha256

# 4. Add MySQL backup checksums
cat mysql_dump_*.sha256 >> CHECKSUMS_COMPLETE.sha256

# 5. Add NER11 archive checksums
cat ner11_archive.sha256 >> CHECKSUMS_COMPLETE.sha256

# 6. Add Git bundle checksums
cat git_bundle_*.sha256 >> CHECKSUMS_COMPLETE.sha256

# 7. Create master checksum file
sha256sum CHECKSUMS_COMPLETE.sha256 > CHECKSUMS_COMPLETE.sha256.master

# 8. Verify all checksums are valid on USB
sha256sum -c CHECKSUMS_COMPLETE.sha256
# Expected: All files OK

# 9. Display summary
echo "✅ Checksum manifest created"
echo ""
echo "Total files in manifest:"
wc -l CHECKSUMS_COMPLETE.sha256

# 10. Create human-readable checksum report
cat > CHECKSUM_REPORT.txt << 'EOF'
AEON Digital Twin - USB Checksum Verification Report
===================================================
Created: $(date)

CHECKSUM VERIFICATION:
To verify file integrity on macOS:

1. Navigate to USB root directory
2. Run: sha256sum -c checksums/CHECKSUMS_COMPLETE.sha256

Expected output: All files should show "OK"

INDIVIDUAL FILE VERIFICATION:
If you need to verify individual files:

Neo4j Backup:
  sha256sum -c checksums/neo4j_backup_*.sha256

MySQL Backup:
  sha256sum -c checksums/mysql_dump_*.sha256

NER11 Archive:
  sha256sum -c checksums/ner11_archive.sha256

Git Bundle:
  sha256sum -c checksums/git_bundle_*.sha256

MASTER CHECKSUM (Verify Checksum File Itself):
  sha256sum -c checksums/CHECKSUMS_COMPLETE.sha256.master

NOTES:
- All files should return "OK" if transfer was successful
- If any file fails verification, DO NOT proceed with restoration
- Investigate failed file and retry transfer
- Contact support if persistent failures occur
EOF

echo "✅ Checksum report generated"
```

**Success Criteria:**
- Master checksum file created
- All individual files checksummed
- All checksums verified locally
- Report documentation created

---

## Task 2.7: Create USB Inventory Manifest

### Purpose
Document all files on USB for reference and completeness verification.

### Procedure

```bash
# 1. Create detailed inventory
cd /mnt/e/AEON_Transfer

# 2. Generate directory tree
find . -type f -exec ls -lh {} \; > INVENTORY_FILES.txt

# 3. Create structured manifest
cat > MANIFEST.json << 'EOF'
{
  "migration": {
    "date": "$(date -Iseconds)",
    "source": "WSL2 Linux",
    "target": "macOS",
    "project": "AEON Digital Twin"
  },
  "components": {
    "database": {
      "neo4j": {
        "description": "Neo4j graph database backup with 20,739 nodes",
        "format": "neo4j-admin dump (binary)",
        "size_estimated": "500 MB"
      },
      "mysql": {
        "description": "MySQL OpenSPG schema and data",
        "format": "SQL dump (gzipped)",
        "size_estimated": "50 MB"
      }
    },
    "models": {
      "ner11": {
        "description": "NER11 Gold Model - spaCy transformer NER",
        "archive": "NER11_Gold_Model.tar.gz",
        "archive_size": "439 MB",
        "extracted_size": "3.5 GB",
        "format": "tar.gz + extracted copies"
      }
    },
    "code": {
      "git_bundle": {
        "description": "Complete Git repository with all history",
        "format": "Git bundle",
        "branches": "All branches and tags included",
        "size": "~100 MB"
      }
    }
  },
  "checksums": {
    "location": "checksums/",
    "master_file": "CHECKSUMS_COMPLETE.sha256",
    "verification": "sha256sum -c checksums/CHECKSUMS_COMPLETE.sha256"
  },
  "next_steps": {
    "1": "Transfer USB to macOS",
    "2": "Read 03_MAC_SETUP_GUIDE.md",
    "3": "Follow 04_DATA_RESTORATION_GUIDE.md",
    "4": "Verify with 05_VALIDATION_PROCEDURES.md"
  }
}
EOF

# 4. Create human-readable manifest
cat > MANIFEST_READABLE.txt << 'EOF'
AEON Digital Twin - USB Migration Contents
==========================================

Created: $(date)
Source: WSL2 Linux
Target: macOS
Project: AEON Digital Twin Development Environment

CRITICAL DATA INCLUDED:
======================

1. DATABASE BACKUPS
   Location: database/

   Neo4j Graph Database (database/neo4j/):
   - Backup file: neo4j_backup_[timestamp].dump
   - Size: ~500 MB
   - Nodes: 20,739
   - Contains: All threat intelligence, vulnerability, compliance data

   MySQL Relational Database (database/mysql/):
   - Backup file: openspg_dump_[timestamp].sql.gz
   - Size: ~50 MB
   - Contains: OpenSPG schema and configuration data

2. MACHINE LEARNING MODELS
   Location: models/ner11/

   NER11 Gold Model Archive:
   - Archive: NER11_Gold_Model.tar.gz (439 MB)
   - Extracted models: models_extracted/ (3.5 GB - optional)
   - Training data: training_data_copy/ (optional)
   - Framework: spaCy 3.x transformer
   - Performance: >95% F1 on test set

3. SOURCE CODE BACKUP
   Location: git_backup/

   Git Repository Bundle:
   - File: aeon_complete_[timestamp].bundle
   - Size: ~100 MB
   - Contains: Complete repository with all branches, tags, history
   - Independent: Can be used without GitHub access

4. CHECKSUMS & VERIFICATION
   Location: checksums/

   Master Checksum: CHECKSUMS_COMPLETE.sha256
   - Verify all files: sha256sum -c CHECKSUMS_COMPLETE.sha256
   - Ensures data integrity after USB transfer

TOTAL SIZE: ~5.5 GB

NEXT STEPS (ON MACOS):
=====================
1. Mount USB drive
2. Read: 03_MAC_SETUP_GUIDE.md (environment setup)
3. Follow: 04_DATA_RESTORATION_GUIDE.md (restore data)
4. Verify: 05_VALIDATION_PROCEDURES.md (confirm working)

CRITICAL: Do not proceed to macOS setup until USB contents
          are verified and understood.

QUESTIONS?
==========
Refer to MIGRATION_NOTES.md in the migration date folder
or contact the development team for clarification.
EOF

# 5. Create space usage report
du -sh * > SPACE_USAGE.txt

# 6. Display final summary
echo "✅ USB Manifest created"
echo ""
echo "SPACE USAGE SUMMARY:"
cat SPACE_USAGE.txt
echo ""
echo "Total USB Usage:"
du -sh /mnt/e/AEON_Transfer
echo ""
echo "Free Space:"
df -h /mnt/e | awk 'NR==2 {print $4}'
```

**Expected Output:**
```
✅ USB Manifest created

SPACE USAGE SUMMARY:
500M database/neo4j/
50M  database/mysql/
3.5G models/ner11/
100M git_backup/

Total USB Usage:
5.5G /mnt/e/AEON_Transfer

Free Space:
2.5G
```

**Success Criteria:**
- JSON manifest created
- Readable manifest created
- Space usage documented
- USB has sufficient space for all files

---

## Task 2.8: Final USB Verification & Checkpoint C

### Purpose
Verify all exports completed successfully before disconnecting USB.

### Procedure

```bash
# 1. Verify all expected files exist
echo "=== VERIFYING EXPORTS ==="

# Check Neo4j backup
if [ -f "/mnt/e/AEON_Transfer/database/neo4j/neo4j_backup_*.dump" ]; then
  echo "✅ Neo4j backup found"
  ls -lh /mnt/e/AEON_Transfer/database/neo4j/neo4j_backup_*.dump
else
  echo "❌ Neo4j backup MISSING"
  exit 1
fi

# Check MySQL backup
if [ -f "/mnt/e/AEON_Transfer/database/mysql/openspg_dump_*.sql.gz" ]; then
  echo "✅ MySQL backup found"
  ls -lh /mnt/e/AEON_Transfer/database/mysql/openspg_dump_*.sql.gz
else
  echo "❌ MySQL backup MISSING"
  exit 1
fi

# Check NER11 archive
if [ -f "/mnt/e/AEON_Transfer/models/ner11/NER11_Gold_Model.tar.gz" ]; then
  echo "✅ NER11 archive found"
  ls -lh /mnt/e/AEON_Transfer/models/ner11/NER11_Gold_Model.tar.gz
else
  echo "❌ NER11 archive MISSING"
  exit 1
fi

# Check Git bundle
if [ -f "/mnt/e/AEON_Transfer/git_backup/aeon_complete_*.bundle" ]; then
  echo "✅ Git bundle found"
  ls -lh /mnt/e/AEON_Transfer/git_backup/aeon_complete_*.bundle
else
  echo "❌ Git bundle MISSING"
  exit 1
fi

# Check checksums
if [ -f "/mnt/e/AEON_Transfer/checksums/CHECKSUMS_COMPLETE.sha256" ]; then
  echo "✅ Checksum manifest found"
else
  echo "❌ Checksum manifest MISSING"
  exit 1
fi

# 2. Verify all checksums on USB
echo ""
echo "=== VERIFYING CHECKSUMS ==="
cd /mnt/e/AEON_Transfer/checksums
sha256sum -c CHECKSUMS_COMPLETE.sha256
CHECKSUM_RESULT=$?

if [ $CHECKSUM_RESULT -eq 0 ]; then
  echo "✅ All checksums VERIFIED - Files are intact"
else
  echo "❌ Checksum verification FAILED - File corruption detected"
  echo "DO NOT PROCEED - Retry export"
  exit 1
fi

# 3. Verify USB space
echo ""
echo "=== USB SPACE VERIFICATION ==="
TOTAL_USED=$(du -sh /mnt/e/AEON_Transfer | awk '{print $1}')
FREE_SPACE=$(df -h /mnt/e | awk 'NR==2 {print $4}')

echo "Total Used: $TOTAL_USED"
echo "Free Space: $FREE_SPACE"

if (( $(echo "$TOTAL_USED < 6" | bc -l) )); then
  echo "✅ Space usage acceptable"
else
  echo "⚠️ Space usage high - monitor free space"
fi

# 4. Create final verification report
cat > /mnt/e/AEON_Transfer/VERIFICATION_REPORT.txt << EOF
AEON USB Export - Final Verification Report
==========================================
Date: $(date)

EXPORTS COMPLETED:
✅ Neo4j database dump
✅ MySQL database backup
✅ NER11 model archive
✅ Git repository bundle
✅ Checksum files
✅ Documentation

INTEGRITY VERIFICATION:
✅ All checksums verified - Files are INTACT

SPACE ALLOCATION:
Total USB Used: $TOTAL_USED
Free Space: $FREE_SPACE

STATUS: ✅ READY FOR TRANSFER TO MACOS

NEXT STEPS:
1. Safely eject USB from WSL2
2. Connect USB to macOS
3. Follow 03_MAC_SETUP_GUIDE.md
4. Follow 04_DATA_RESTORATION_GUIDE.md

DO NOT PROCEED if any exports are missing or checksums failed.
EOF

# 5. Display final summary
echo ""
echo "✅ ALL EXPORTS VERIFIED SUCCESSFULLY"
echo ""
echo "USB is ready for transfer to macOS"
echo ""
echo "Contents Summary:"
tree -L 2 /mnt/e/AEON_Transfer/ 2>/dev/null || find /mnt/e/AEON_Transfer -maxdepth 2 -type d

# 6. Final instruction
echo ""
echo "⚠️  IMPORTANT:"
echo "Before disconnecting USB:"
echo "1. Ensure all files are not being accessed"
echo "2. Safely eject: sudo umount /mnt/e"
echo "3. Verify eject was successful: df | grep /mnt/e (should not appear)"
echo "4. Physically disconnect USB"
```

**Expected Output:**
```
✅ Neo4j backup found
✅ MySQL backup found
✅ NER11 archive found
✅ Git bundle found
✅ Checksum manifest found

=== VERIFYING CHECKSUMS ===
[All files checked]: OK

✅ All checksums VERIFIED - Files are intact

Total Used: 5.5G
Free Space: 2.5G
✅ Space usage acceptable

✅ ALL EXPORTS VERIFIED SUCCESSFULLY

USB is ready for transfer to macOS
```

**Success Criteria:**
- All exports verified present
- All checksums verified
- Space usage documented
- Verification report created

---

## Checkpoint C - Post-Export Verification

### Before disconnecting USB, verify:

- ✅ All 4 major components exported (Neo4j, MySQL, NER11, Git)
- ✅ All checksums passed verification
- ✅ Space usage <6 GB (target <5.5 GB)
- ✅ Verification report generated
- ✅ All documentation files created

### If ANY checkpoint fails:

1. **Identify failed component**
2. **Review error messages**
3. **Retry export for that component**
4. **Re-verify checksums**
5. **Only proceed after ALL verifications pass**

---

## Safe USB Ejection Procedure

```bash
# 1. Stop all file access
cd /home/jim/2_OXOT_Projects_Dev

# 2. Unmount USB safely
sudo umount /mnt/e

# 3. Verify unmounted
df | grep /mnt/e
# Should return nothing if unmounted

# 4. Physical disconnection
echo "Safe to disconnect USB from WSL2 now"
```

---

## Summary

**Phase 2 Complete When:**
- ✅ All 5 data export tasks completed
- ✅ Checksum manifest created and verified
- ✅ USB inventory and manifest documented
- ✅ Final USB verification passed
- ✅ USB safely ejected

**Time Estimate:** 45-90 minutes

**Next Phase:** Transfer USB to macOS, then proceed with 03_MAC_SETUP_GUIDE.md

</content>
