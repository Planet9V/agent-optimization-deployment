# AEON System Migration Plan: WSL2/Ubuntu → macOS

**Created**: 2025-12-04
**Version**: 1.0
**Status**: READY FOR EXECUTION

---

## 📊 EXECUTIVE SUMMARY

### Current System Inventory
- **Project Directory**: `/home/jim/2_OXOT_Projects_Dev`
- **Total Size**: ~5.0 GB
  - 5_NER11_Gold_Model: 3.5 GB (976 MB models)
  - 1_AEON_DT_CyberSecurity_Wiki_Current: 142 MB
  - 1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1: 1.3 MB

### Active Docker Resources
- **Containers**: 15 total (11 running, 4 stopped)
- **Critical Volumes**:
  - openspg-neo4j-data
  - openspg-qdrant-data
  - active_neo4j_data
  - active_qdrant_data
  - aeon_postgres_dev_data
- **Images**: 12 relevant (largest: ner11-gold-api at 29.6 GB)

### Git Repository Status
- **Branch**: gap-002-clean-VERIFIED
- **Uncommitted Changes**: 7 modified files, 19 untracked files
- **Action Required**: Commit/stash before migration

### USB Drive Requirements
- **Minimum Required**: 8 GB (for compressed data only)
- **Recommended**: 32 GB (for full data + Docker volumes)
- **Optimal**: 64 GB+ (for safety margin + Docker images)

---

## 🎯 PHASE 1: PLANNING & PREPARATION (Before Migration)

**Duration**: 30-45 minutes
**Risk Level**: LOW
**Prerequisites**: None

### Task 1.1: Inventory & Verification
**Command**:
```bash
# Create inventory script
cat > /tmp/migration_inventory.sh << 'EOF'
#!/bin/bash
echo "=== AEON MIGRATION INVENTORY ===" > ~/migration_inventory.txt
echo "Date: $(date)" >> ~/migration_inventory.txt
echo "" >> ~/migration_inventory.txt

# Project sizes
echo "PROJECT DIRECTORIES:" >> ~/migration_inventory.txt
du -sh ~/2_OXOT_Projects_Dev/5_NER11_Gold_Model >> ~/migration_inventory.txt
du -sh ~/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current >> ~/migration_inventory.txt
du -sh ~/2_OXOT_Projects_Dev/1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1 >> ~/migration_inventory.txt

# Git status
echo "" >> ~/migration_inventory.txt
echo "GIT STATUS:" >> ~/migration_inventory.txt
cd ~/2_OXOT_Projects_Dev && git status --short >> ~/migration_inventory.txt

# Docker containers
echo "" >> ~/migration_inventory.txt
echo "DOCKER CONTAINERS:" >> ~/migration_inventory.txt
docker ps -a --format "{{.Names}}: {{.Status}}" >> ~/migration_inventory.txt

# Docker volumes
echo "" >> ~/migration_inventory.txt
echo "DOCKER VOLUMES:" >> ~/migration_inventory.txt
docker volume ls --format "{{.Name}}" | grep -E "openspg|active|aeon" >> ~/migration_inventory.txt

# Model files
echo "" >> ~/migration_inventory.txt
echo "MODEL FILES:" >> ~/migration_inventory.txt
find ~/2_OXOT_Projects_Dev/5_NER11_Gold_Model/models -type f -exec ls -lh {} \; >> ~/migration_inventory.txt

echo "" >> ~/migration_inventory.txt
echo "INVENTORY COMPLETE" >> ~/migration_inventory.txt
EOF

chmod +x /tmp/migration_inventory.sh
/tmp/migration_inventory.sh
cat ~/migration_inventory.txt
```

**Success Criteria**:
- Inventory file created at `~/migration_inventory.txt`
- All directories listed with sizes
- Git status captured
- Docker resources enumerated

**Recovery**: Re-run script if incomplete

**Time Estimate**: 5 minutes

---

### Task 1.2: USB Drive Capacity Check
**Command**:
```bash
# Assuming USB mounted at /mnt/usb or similar
# Adjust mount point as needed

# Check USB capacity
df -h /mnt/usb

# Calculate total data to transfer
TOTAL_SIZE=$(du -sb ~/2_OXOT_Projects_Dev | awk '{print $1}')
VOLUME_SIZE=$(docker volume ls -q | grep -E "openspg|active" | xargs docker volume inspect | grep -A1 "Mountpoint" | grep -v "Mountpoint" | xargs sudo du -sb | awk '{sum+=$1} END {print sum}')

echo "Total project size: $(echo $TOTAL_SIZE | numfmt --to=iec-i)"
echo "Total Docker volumes: $(echo $VOLUME_SIZE | numfmt --to=iec-i)"
echo "Total required: $(echo $(($TOTAL_SIZE + $VOLUME_SIZE)) | numfmt --to=iec-i)"
```

**Success Criteria**:
- USB drive mounted and accessible
- Free space > 10 GB (minimum)
- Free space > 35 GB (recommended)

**Recovery**:
- If insufficient space, use compression (see Phase 3)
- Consider splitting across multiple USBs
- Use network transfer as alternative

**Time Estimate**: 2 minutes

---

### Task 1.3: Git Repository Cleanup
**Command**:
```bash
cd ~/2_OXOT_Projects_Dev

# Create a pre-migration commit
git add -A
git commit -m "Pre-migration snapshot: WSL2 state before Mac migration

- 7 modified files from recent development
- 19 untracked files in documentation/logs
- All containers healthy and running
- Branch: gap-002-clean-VERIFIED
- Date: $(date)"

# Tag for easy reference
git tag -a pre-mac-migration-$(date +%Y%m%d) -m "State before migrating to Mac"

# Verify commit
git log -1 --oneline
git status
```

**Success Criteria**:
- All changes committed
- Tag created
- `git status` shows clean working directory
- Commit hash recorded

**Recovery**:
```bash
# If commit fails
git stash save "pre-migration-backup-$(date +%Y%m%d-%H%M)"
```

**Time Estimate**: 5 minutes

---

### Task 1.4: Create System Snapshot Documentation
**Command**:
```bash
cat > ~/SYSTEM_SNAPSHOT_$(date +%Y%m%d).md << 'EOF'
# AEON System Snapshot

## Environment
- **OS**: $(lsb_release -d | cut -f2)
- **Kernel**: $(uname -r)
- **Docker Version**: $(docker --version)
- **Docker Compose**: $(docker-compose --version)
- **Python**: $(python3 --version)
- **Node**: $(node --version 2>/dev/null || echo "Not installed")

## Active Services
$(docker ps --format "- {{.Names}}: {{.Status}}")

## Environment Variables
$(env | grep -E "DOCKER|NVIDIA|MODEL|API|DATABASE" | sort)

## Network Configuration
$(docker network ls)

## Port Mappings
$(docker ps --format "{{.Names}}: {{.Ports}}")

## Critical Paths
- Project Root: ~/2_OXOT_Projects_Dev
- Models: ~/2_OXOT_Projects_Dev/5_NER11_Gold_Model/models/ner11_v3
- Docker Volumes: /var/lib/docker/volumes
EOF

# Execute the template
cat ~/SYSTEM_SNAPSHOT_$(date +%Y%m%d).md | bash
```

**Success Criteria**:
- Snapshot document created
- All environment details captured
- Service configurations documented

**Recovery**: Manual documentation if script fails

**Time Estimate**: 3 minutes

---

### Task 1.5: Pre-Migration Backup Safety Check
**Command**:
```bash
# Create backup checklist
cat > ~/pre_migration_checklist.txt << 'EOF'
PRE-MIGRATION SAFETY CHECKLIST
================================

[ ] Git repository fully committed
[ ] All containers healthy (docker ps shows "healthy")
[ ] No critical processes running
[ ] USB drive mounted and tested
[ ] Sufficient USB space verified
[ ] System snapshot created
[ ] Container health verified
[ ] Volume data accessible
[ ] Network connectivity confirmed
[ ] Recovery procedures documented

PROCEED ONLY IF ALL CHECKED
EOF

cat ~/pre_migration_checklist.txt

# Automated checks
echo ""
echo "AUTOMATED VERIFICATION:"
echo "======================="

# Git clean check
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ Git repository clean"
else
    echo "❌ Git has uncommitted changes"
fi

# Container health
UNHEALTHY=$(docker ps --filter "health=unhealthy" --format "{{.Names}}")
if [ -z "$UNHEALTHY" ]; then
    echo "✅ All containers healthy"
else
    echo "❌ Unhealthy containers: $UNHEALTHY"
fi

# Docker daemon
if docker info > /dev/null 2>&1; then
    echo "✅ Docker daemon running"
else
    echo "❌ Docker daemon not accessible"
fi
```

**Success Criteria**:
- All checklist items verified
- No unhealthy containers
- Git status clean
- Docker accessible

**Recovery**: Address any failing checks before proceeding

**Time Estimate**: 5 minutes

---

## 🔄 PHASE 2: DATA COLLECTION (On Current Machine)

**Duration**: 45-90 minutes
**Risk Level**: MEDIUM
**Prerequisites**: Phase 1 complete, USB mounted

### Task 2.1: Stop Non-Essential Containers
**Command**:
```bash
# Stop containers that aren't needed for extraction
docker stop aeon-site-3 aeon-site-aeoncyberdt aeon-site-2 aeon-nginx-proxy ner11_training_env neo4j-explore

# Verify critical containers still running
docker ps --filter "name=ner11-gold-api" --filter "name=openspg" --filter "name=aeon-saas-dev"
```

**Success Criteria**:
- 6 containers stopped
- Critical containers (ner11-gold-api, openspg-*, aeon-saas-dev) still running
- No error messages

**Recovery**: `docker start <container-name>` for any accidentally stopped

**Time Estimate**: 2 minutes

---

### Task 2.2: Export Docker Volumes (Critical Data)
**Command**:
```bash
# Create export directory on USB
USB_PATH="/mnt/usb"  # Adjust as needed
mkdir -p $USB_PATH/aeon_migration/docker_volumes

# Export Neo4j data (OpenSPG)
docker run --rm \
  -v openspg-neo4j-data:/data \
  -v $USB_PATH/aeon_migration/docker_volumes:/backup \
  alpine tar czf /backup/openspg-neo4j-data.tar.gz -C /data .

# Export Qdrant data (OpenSPG)
docker run --rm \
  -v openspg-qdrant-data:/data \
  -v $USB_PATH/aeon_migration/docker_volumes:/backup \
  alpine tar czf /backup/openspg-qdrant-data.tar.gz -C /data .

# Export active Neo4j data
docker run --rm \
  -v active_neo4j_data:/data \
  -v $USB_PATH/aeon_migration/docker_volumes:/backup \
  alpine tar czf /backup/active-neo4j-data.tar.gz -C /data .

# Export active Qdrant data
docker run --rm \
  -v active_qdrant_data:/data \
  -v $USB_PATH/aeon_migration/docker_volumes:/backup \
  alpine tar czf /backup/active-qdrant-data.tar.gz -C /data .

# Export Postgres data
docker run --rm \
  -v aeon_postgres_dev_data:/data \
  -v $USB_PATH/aeon_migration/docker_volumes:/backup \
  alpine tar czf /backup/aeon-postgres-data.tar.gz -C /data .

# Export Redis data
docker run --rm \
  -v openspg-redis-data:/data \
  -v $USB_PATH/aeon_migration/docker_volumes:/backup \
  alpine tar czf /backup/openspg-redis-data.tar.gz -C /data .

# Verify exports
ls -lh $USB_PATH/aeon_migration/docker_volumes/*.tar.gz
```

**Success Criteria**:
- 6 .tar.gz files created
- Each file > 0 bytes
- No error messages during export
- Total size reasonable (< 5 GB for all)

**Recovery**:
```bash
# Re-run specific volume export if failed
# Example for Neo4j:
docker run --rm -v openspg-neo4j-data:/data -v /mnt/usb/aeon_migration/docker_volumes:/backup alpine tar czf /backup/openspg-neo4j-data.tar.gz -C /data .
```

**Time Estimate**: 15-30 minutes (depends on volume size)

---

### Task 2.3: Copy Project Files
**Command**:
```bash
USB_PATH="/mnt/usb"
mkdir -p $USB_PATH/aeon_migration/project

# Copy main project directory (exclude node_modules, __pycache__, .git large objects)
rsync -av --progress \
  --exclude='.git/objects/pack/*.pack' \
  --exclude='node_modules/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='.pytest_cache/' \
  --exclude='venv/' \
  --exclude='.venv/' \
  ~/2_OXOT_Projects_Dev/ \
  $USB_PATH/aeon_migration/project/

# Verify copy
du -sh $USB_PATH/aeon_migration/project
ls -la $USB_PATH/aeon_migration/project/5_NER11_Gold_Model/models/ner11_v3/
```

**Success Criteria**:
- rsync completes with "100%" progress
- Project directory size matches source (~5 GB)
- Model files present in destination
- No "failed" or "error" messages

**Recovery**:
```bash
# Resume failed rsync (it's resumable by default)
rsync -av --progress ~/2_OXOT_Projects_Dev/ $USB_PATH/aeon_migration/project/
```

**Time Estimate**: 10-20 minutes (USB 3.0 speed dependent)

---

### Task 2.4: Export Git Repository State
**Command**:
```bash
USB_PATH="/mnt/usb"
cd ~/2_OXOT_Projects_Dev

# Create full git bundle (includes all branches and history)
git bundle create $USB_PATH/aeon_migration/aeon-project.bundle --all

# Export current branch info
git branch --show-current > $USB_PATH/aeon_migration/current_branch.txt
git log -1 --format="%H" > $USB_PATH/aeon_migration/current_commit.txt

# Export remote URLs
git remote -v > $USB_PATH/aeon_migration/git_remotes.txt

# Verify bundle
git bundle verify $USB_PATH/aeon_migration/aeon-project.bundle
```

**Success Criteria**:
- Bundle file created (size > 10 MB)
- Bundle verification shows "The bundle records a complete history"
- Branch and commit files created

**Recovery**:
```bash
# Re-create bundle if corrupted
git bundle create $USB_PATH/aeon_migration/aeon-project-backup.bundle --all
```

**Time Estimate**: 5 minutes

---

### Task 2.5: Export Docker Images (Optional but Recommended)
**Command**:
```bash
USB_PATH="/mnt/usb"
mkdir -p $USB_PATH/aeon_migration/docker_images

# Export critical images (WARNING: Large files)
# Only export if USB has 30+ GB free space

# Option A: Export ner11-gold-api image (29.6 GB - LARGE!)
docker save ner11-gold-api:latest | gzip > $USB_PATH/aeon_migration/docker_images/ner11-gold-api.tar.gz

# Option B: Skip image export, rebuild on Mac (RECOMMENDED)
echo "Image rebuild required on Mac" > $USB_PATH/aeon_migration/docker_images/REBUILD_REQUIRED.txt
echo "ner11-gold-api:latest" >> $USB_PATH/aeon_migration/docker_images/REBUILD_REQUIRED.txt

# Export smaller images
docker save aeon-saas-dev:latest | gzip > $USB_PATH/aeon_migration/docker_images/aeon-saas-dev.tar.gz
docker save openspg-server:latest | gzip > $USB_PATH/aeon_migration/docker_images/openspg-server.tar.gz

# Note: OpenSPG images can be pulled from registry on Mac
```

**Success Criteria**:
- Decision made: export images OR plan for rebuild
- If exporting: .tar.gz files created
- If rebuilding: REBUILD_REQUIRED.txt created with image list

**Recovery**:
```bash
# If export fails due to space, skip and rebuild on Mac
echo "Rebuild on Mac due to space constraints" > $USB_PATH/aeon_migration/docker_images/REBUILD_REQUIRED.txt
```

**Time Estimate**: 5 minutes (documentation) OR 60-90 minutes (full export)

---

### Task 2.6: Export Configuration Files
**Command**:
```bash
USB_PATH="/mnt/usb"
mkdir -p $USB_PATH/aeon_migration/configs

# Copy Docker Compose files
find ~/2_OXOT_Projects_Dev -name "docker-compose*.yml" -exec cp {} $USB_PATH/aeon_migration/configs/ \;

# Copy Dockerfiles
find ~/2_OXOT_Projects_Dev -name "Dockerfile*" -exec cp --parents {} $USB_PATH/aeon_migration/configs/ \;

# Copy requirements.txt files
find ~/2_OXOT_Projects_Dev -name "requirements*.txt" -exec cp --parents {} $USB_PATH/aeon_migration/configs/ \;

# Copy environment files (if any)
find ~/2_OXOT_Projects_Dev -name ".env*" -exec cp {} $USB_PATH/aeon_migration/configs/ \; 2>/dev/null || true

# Copy package.json files
find ~/2_OXOT_Projects_Dev -name "package*.json" -exec cp --parents {} $USB_PATH/aeon_migration/configs/ \;

# List what was copied
ls -R $USB_PATH/aeon_migration/configs/
```

**Success Criteria**:
- docker-compose.yml files present
- requirements.txt files present
- Dockerfile files present
- package.json files present (if applicable)

**Recovery**: Manual copy if find commands fail

**Time Estimate**: 3 minutes

---

### Task 2.7: Create Size Verification Manifest
**Command**:
```bash
USB_PATH="/mnt/usb"

cat > $USB_PATH/aeon_migration/MANIFEST.txt << EOF
AEON MIGRATION MANIFEST
=======================
Date: $(date)
Source: $(hostname)
Destination: macOS

FILE INVENTORY:
==============

Project Files:
$(du -sh $USB_PATH/aeon_migration/project)
$(find $USB_PATH/aeon_migration/project -type f | wc -l) files

Docker Volumes:
$(ls -lh $USB_PATH/aeon_migration/docker_volumes/*.tar.gz)

Git Bundle:
$(ls -lh $USB_PATH/aeon_migration/aeon-project.bundle)

Docker Images:
$(ls -lh $USB_PATH/aeon_migration/docker_images/ 2>/dev/null || echo "Image rebuild required on Mac")

Configuration Files:
$(find $USB_PATH/aeon_migration/configs -type f | wc -l) files

CHECKSUMS:
==========
$(cd $USB_PATH/aeon_migration && find . -type f -name "*.tar.gz" -o -name "*.bundle" | xargs md5sum)

TOTAL SIZE:
===========
$(du -sh $USB_PATH/aeon_migration)

VERIFICATION COMPLETE: $(date)
EOF

cat $USB_PATH/aeon_migration/MANIFEST.txt
```

**Success Criteria**:
- MANIFEST.txt created
- All sections populated
- Checksums generated
- Total size within USB capacity

**Recovery**: Manual manifest creation if script fails

**Time Estimate**: 2 minutes

---

## 📦 PHASE 3: USB TRANSFER

**Duration**: 5-10 minutes
**Risk Level**: LOW
**Prerequisites**: Phase 2 complete

### Task 3.1: Final USB Verification
**Command**:
```bash
USB_PATH="/mnt/usb"

# Verify all critical files exist
echo "Checking critical files..."

FILES_TO_CHECK=(
  "$USB_PATH/aeon_migration/MANIFEST.txt"
  "$USB_PATH/aeon_migration/aeon-project.bundle"
  "$USB_PATH/aeon_migration/docker_volumes/openspg-neo4j-data.tar.gz"
  "$USB_PATH/aeon_migration/docker_volumes/openspg-qdrant-data.tar.gz"
  "$USB_PATH/aeon_migration/docker_volumes/active-neo4j-data.tar.gz"
  "$USB_PATH/aeon_migration/docker_volumes/active-qdrant-data.tar.gz"
  "$USB_PATH/aeon_migration/docker_volumes/aeon-postgres-data.tar.gz"
  "$USB_PATH/aeon_migration/project/5_NER11_Gold_Model/models/ner11_v3"
)

ALL_GOOD=true
for file in "${FILES_TO_CHECK[@]}"; do
  if [ -e "$file" ]; then
    echo "✅ $file"
  else
    echo "❌ MISSING: $file"
    ALL_GOOD=false
  fi
done

if [ "$ALL_GOOD" = true ]; then
  echo ""
  echo "✅ ALL CRITICAL FILES VERIFIED"
  echo "Safe to unmount USB"
else
  echo ""
  echo "❌ MISSING FILES - DO NOT UNMOUNT"
  echo "Re-run failed tasks from Phase 2"
fi
```

**Success Criteria**:
- All critical files present
- No "MISSING" messages
- Script outputs "Safe to unmount USB"

**Recovery**: Return to Phase 2, re-run failed tasks

**Time Estimate**: 2 minutes

---

### Task 3.2: Sync and Unmount USB
**Command**:
```bash
USB_PATH="/mnt/usb"

# Force sync to ensure all data written
sync
sleep 5
sync

# Unmount USB safely
cd ~
sudo umount $USB_PATH

# Verify unmount
if mountpoint -q $USB_PATH; then
  echo "❌ USB still mounted - do not remove"
else
  echo "✅ USB safely unmounted - safe to remove"
fi
```

**Success Criteria**:
- sync completes
- umount successful
- "safe to remove" message displayed

**Recovery**:
```bash
# If unmount fails (device busy)
sudo fuser -km $USB_PATH
sudo umount -f $USB_PATH
```

**Time Estimate**: 1 minute

---

### Task 3.3: Create Handoff Document
**Command**:
```bash
cat > ~/MAC_MIGRATION_HANDOFF.md << 'EOF'
# AEON Mac Migration Handoff

## Phase 2 Complete ✅
- All data extracted from WSL2 Ubuntu
- Docker volumes exported
- Project files copied
- Git repository bundled
- USB drive prepared and unmounted

## What's on the USB
1. **docker_volumes/**: 6 compressed volume backups
2. **project/**: Complete project directory (5 GB)
3. **aeon-project.bundle**: Full git history
4. **configs/**: Docker Compose, Dockerfiles, requirements
5. **MANIFEST.txt**: File inventory and checksums

## Next Steps (On Mac)
1. Mount USB drive
2. Verify MANIFEST.txt checksums
3. Follow Phase 4: Mac Setup
4. Follow Phase 5: Data Restoration
5. Follow Phase 6: Verification

## Critical Information
- **Current Branch**: gap-002-clean-VERIFIED
- **Last Commit**: $(git log -1 --format="%H")
- **Models Location**: 5_NER11_Gold_Model/models/ner11_v3/
- **Docker Network**: aeon-net (external)
- **GPU Requirements**: NVIDIA GPU support needed for ner11-gold-api

## Rollback Plan
- WSL2 system remains intact
- Can continue working if Mac setup fails
- USB contains complete backup for retry

## Support Contacts
- Migration Date: $(date)
- Source System: $(hostname)
- Kernel: $(uname -r)
EOF

cat ~/MAC_MIGRATION_HANDOFF.md
```

**Success Criteria**:
- Handoff document created
- All critical info captured
- Ready for Mac phase

**Recovery**: N/A (documentation only)

**Time Estimate**: 2 minutes

---

## 🍎 PHASE 4: MAC SETUP (Initial)

**Duration**: 30-60 minutes
**Risk Level**: MEDIUM
**Prerequisites**: Mac with admin access, USB drive, internet connection

### Task 4.1: Install Homebrew
**Command** (on Mac):
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add Homebrew to PATH (for Apple Silicon Macs)
if [[ $(uname -m) == 'arm64' ]]; then
  echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Verify installation
brew --version
```

**Success Criteria**:
- Homebrew installed
- `brew --version` shows version number
- No error messages

**Recovery**: Visit https://brew.sh for manual installation help

**Time Estimate**: 5-10 minutes

---

### Task 4.2: Install Docker Desktop for Mac
**Command** (on Mac):
```bash
# Install Docker Desktop via Homebrew
brew install --cask docker

# Wait for installation to complete
echo "Docker Desktop installed. Please:"
echo "1. Open Docker Desktop from Applications"
echo "2. Accept the license agreement"
echo "3. Wait for Docker engine to start (whale icon in menu bar)"
echo "4. Return here and press Enter when Docker is running"
read

# Verify Docker is running
docker --version
docker compose version
docker ps
```

**Success Criteria**:
- Docker Desktop installed
- Docker engine running (whale icon in menu bar)
- `docker ps` returns empty list (no errors)
- `docker compose` command available

**Recovery**:
- Manual download from https://www.docker.com/products/docker-desktop
- Ensure Docker Desktop is started and resources allocated (Settings > Resources)

**Time Estimate**: 10-15 minutes

---

### Task 4.3: Install Development Dependencies
**Command** (on Mac):
```bash
# Install Python 3
brew install python@3.11

# Install Node.js (for frontend development)
brew install node

# Install git (usually pre-installed on Mac)
brew install git

# Install additional tools
brew install wget rsync

# Verify installations
python3 --version
node --version
npm --version
git --version
```

**Success Criteria**:
- All tools installed
- Version commands return numbers
- No error messages

**Recovery**: Individual package installation via `brew install <package>`

**Time Estimate**: 5-10 minutes

---

### Task 4.4: Create Directory Structure
**Command** (on Mac):
```bash
# Create main project directory
mkdir -p ~/Projects/AEON

# Create temporary migration directory
mkdir -p ~/Projects/AEON/migration_temp

# Mount USB (macOS auto-mounts to /Volumes/<USB_NAME>)
# Find USB name
ls /Volumes/

# Set USB path (adjust USB name as needed)
USB_NAME="Untitled"  # Change to your USB name
USB_PATH="/Volumes/$USB_NAME"

# Verify USB access
ls -la $USB_PATH/aeon_migration/
```

**Success Criteria**:
- ~/Projects/AEON directory created
- USB drive visible in /Volumes/
- aeon_migration directory accessible on USB

**Recovery**:
```bash
# If USB not auto-mounted, use Disk Utility to mount
open /System/Applications/Utilities/Disk\ Utility.app
```

**Time Estimate**: 2 minutes

---

### Task 4.5: Verify USB Data Integrity
**Command** (on Mac):
```bash
USB_PATH="/Volumes/<USB_NAME>"  # Adjust USB name

# Verify manifest exists
cat $USB_PATH/aeon_migration/MANIFEST.txt

# Verify checksums (if md5sum available on Mac)
cd $USB_PATH/aeon_migration
find . -type f -name "*.tar.gz" -o -name "*.bundle" | xargs md5 > checksums_mac.txt

# Compare with original checksums
echo "Original checksums from WSL2:"
grep -E "tar.gz|bundle" MANIFEST.txt

echo ""
echo "Mac checksums:"
cat checksums_mac.txt

echo ""
echo "Manually verify checksums match"
```

**Success Criteria**:
- MANIFEST.txt readable
- Checksums generated on Mac
- Checksums match WSL2 originals (visual verification)

**Recovery**:
```bash
# If checksums don't match, re-copy specific files from WSL2
# Priority: git bundle, docker volumes
```

**Time Estimate**: 3 minutes

---

## 🔄 PHASE 5: DATA RESTORATION (On Mac)

**Duration**: 45-90 minutes
**Risk Level**: MEDIUM
**Prerequisites**: Phase 4 complete, Docker running

### Task 5.1: Restore Project Files
**Command** (on Mac):
```bash
USB_PATH="/Volumes/<USB_NAME>"  # Adjust USB name

# Copy project directory from USB to Mac
rsync -av --progress \
  $USB_PATH/aeon_migration/project/ \
  ~/Projects/AEON/

# Verify copy
du -sh ~/Projects/AEON
ls -la ~/Projects/AEON/5_NER11_Gold_Model/models/ner11_v3/

# Set proper permissions
chmod -R u+w ~/Projects/AEON
```

**Success Criteria**:
- Project directory copied (~5 GB)
- Model files present
- Directory writable

**Recovery**: Re-run rsync (it's resumable)

**Time Estimate**: 10-15 minutes

---

### Task 5.2: Restore Git Repository
**Command** (on Mac):
```bash
USB_PATH="/Volumes/<USB_NAME>"

cd ~/Projects/AEON

# Clone from bundle
git clone $USB_PATH/aeon_migration/aeon-project.bundle .

# Restore branch
BRANCH=$(cat $USB_PATH/aeon_migration/current_branch.txt)
git checkout $BRANCH

# Restore remotes
while read -r line; do
  if [[ $line == *"(fetch)"* ]]; then
    REMOTE=$(echo $line | awk '{print $1}')
    URL=$(echo $line | awk '{print $2}')
    git remote add $REMOTE $URL 2>/dev/null || git remote set-url $REMOTE $URL
  fi
done < $USB_PATH/aeon_migration/git_remotes.txt

# Verify
git status
git log -1
git remote -v
```

**Success Criteria**:
- Git repository cloned
- Correct branch checked out
- Remotes configured
- Git status shows clean state

**Recovery**:
```bash
# If clone fails
rm -rf .git
git init
git bundle unbundle $USB_PATH/aeon_migration/aeon-project.bundle
```

**Time Estimate**: 5 minutes

---

### Task 5.3: Create Docker Network
**Command** (on Mac):
```bash
# Create external network (required by docker-compose)
docker network create aeon-net

# Verify
docker network ls | grep aeon-net
```

**Success Criteria**:
- aeon-net network created
- No error messages

**Recovery**:
```bash
# Remove and recreate if exists with wrong config
docker network rm aeon-net
docker network create aeon-net
```

**Time Estimate**: 1 minute

---

### Task 5.4: Restore Docker Volumes
**Command** (on Mac):
```bash
USB_PATH="/Volumes/<USB_NAME>"

# Create volumes
docker volume create openspg-neo4j-data
docker volume create openspg-qdrant-data
docker volume create active_neo4j_data
docker volume create active_qdrant_data
docker volume create aeon_postgres_dev_data
docker volume create openspg-redis-data

# Restore Neo4j (OpenSPG)
docker run --rm \
  -v openspg-neo4j-data:/data \
  -v $USB_PATH/aeon_migration/docker_volumes:/backup \
  alpine sh -c "cd /data && tar xzf /backup/openspg-neo4j-data.tar.gz"

# Restore Qdrant (OpenSPG)
docker run --rm \
  -v openspg-qdrant-data:/data \
  -v $USB_PATH/aeon_migration/docker_volumes:/backup \
  alpine sh -c "cd /data && tar xzf /backup/openspg-qdrant-data.tar.gz"

# Restore Neo4j (Active)
docker run --rm \
  -v active_neo4j_data:/data \
  -v $USB_PATH/aeon_migration/docker_volumes:/backup \
  alpine sh -c "cd /data && tar xzf /backup/active-neo4j-data.tar.gz"

# Restore Qdrant (Active)
docker run --rm \
  -v active_qdrant_data:/data \
  -v $USB_PATH/aeon_migration/docker_volumes:/backup \
  alpine sh -c "cd /data && tar xzf /backup/active-qdrant-data.tar.gz"

# Restore Postgres
docker run --rm \
  -v aeon_postgres_dev_data:/data \
  -v $USB_PATH/aeon_migration/docker_volumes:/backup \
  alpine sh -c "cd /data && tar xzf /backup/aeon-postgres-data.tar.gz"

# Restore Redis
docker run --rm \
  -v openspg-redis-data:/data \
  -v $USB_PATH/aeon_migration/docker_volumes:/backup \
  alpine sh -c "cd /data && tar xzf /backup/openspg-redis-data.tar.gz"

# Verify volumes restored
docker volume ls
```

**Success Criteria**:
- All 6 volumes created
- Data extracted into volumes
- No error messages

**Recovery**:
```bash
# Re-run specific volume restore if failed
docker volume rm <volume-name>
docker volume create <volume-name>
# Re-run restore command for that volume
```

**Time Estimate**: 10-15 minutes

---

### Task 5.5: Rebuild Docker Images (If Not Exported)
**Command** (on Mac):
```bash
cd ~/Projects/AEON/5_NER11_Gold_Model/docker

# Build ner11-gold-api image
docker build -t ner11-gold-api:latest -f Dockerfile .

# Pull OpenSPG images from registry
docker pull spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-server:latest
docker pull spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-mysql:latest
docker pull neo4j:4.4.12
docker pull qdrant/qdrant:latest
docker pull redis:alpine
docker pull minio/minio:latest

# Verify images
docker images | grep -E "ner11|openspg|neo4j|qdrant"
```

**Success Criteria**:
- ner11-gold-api built successfully (may take 30-60 minutes)
- All required images pulled
- `docker images` shows all images

**Recovery**:
```bash
# If build fails, check build logs
docker build -t ner11-gold-api:latest -f Dockerfile . 2>&1 | tee build.log

# Check for missing dependencies
cat build.log | grep -i error
```

**Time Estimate**: 30-60 minutes (first build), 5 minutes (pulls only)

---

### Task 5.6: Configure Docker Compose for Mac
**Command** (on Mac):
```bash
cd ~/Projects/AEON/5_NER11_Gold_Model/docker

# Mac doesn't support NVIDIA GPU in Docker by default
# Modify docker-compose.yml to comment out GPU sections

cat > docker-compose.mac.yml << 'EOF'
version: '3.8'

services:
  ner11-gold-api:
    build:
      context: .
      dockerfile: Dockerfile
    image: ner11-gold-api:latest
    container_name: ner11-gold-api
    ports:
      - "8000:8000"
    volumes:
      - ../:/app
    working_dir: /app
    # GPU support commented out for Mac
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: all
    #           capabilities: [ gpu ]
    shm_size: '8gb'
    environment:
      # - NVIDIA_VISIBLE_DEVICES=all
      # - NVIDIA_DRIVER_CAPABILITIES=compute,utility
      - MODEL_PATH=models/ner11_v3/model-best
    networks:
      - aeon-net

networks:
  aeon-net:
    external: true
EOF

echo "Mac-compatible docker-compose.mac.yml created"
echo "Use: docker compose -f docker-compose.mac.yml up -d"
```

**Success Criteria**:
- docker-compose.mac.yml created
- GPU sections commented out
- Network configuration preserved

**Recovery**: Manual editing of docker-compose.yml

**Time Estimate**: 3 minutes

---

## ✅ PHASE 6: VERIFICATION & VALIDATION

**Duration**: 30-45 minutes
**Risk Level**: LOW
**Prerequisites**: Phase 5 complete

### Task 6.1: Start Database Containers
**Command** (on Mac):
```bash
cd ~/Projects/AEON

# Start Neo4j (OpenSPG)
docker run -d \
  --name openspg-neo4j \
  --network aeon-net \
  -p 7474:7474 -p 7687:7687 \
  -v openspg-neo4j-data:/data \
  -v openspg-neo4j-logs:/logs \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:4.4.12

# Start Qdrant (OpenSPG)
docker run -d \
  --name openspg-qdrant \
  --network aeon-net \
  -p 6333:6333 -p 6334:6334 \
  -v openspg-qdrant-data:/qdrant/storage \
  qdrant/qdrant:latest

# Start Redis
docker run -d \
  --name openspg-redis \
  --network aeon-net \
  -p 6379:6379 \
  -v openspg-redis-data:/data \
  redis:alpine

# Start MySQL (OpenSPG)
docker run -d \
  --name openspg-mysql \
  --network aeon-net \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=openspg \
  -e MYSQL_DATABASE=openspg \
  -v openspg-mysql-data:/var/lib/mysql \
  spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-mysql:latest

# Start Postgres
docker run -d \
  --name aeon-postgres-dev \
  --network aeon-net \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgres \
  -v aeon_postgres_dev_data:/var/lib/postgresql/data \
  postgres:14-alpine

# Wait for databases to initialize
echo "Waiting 30 seconds for databases to initialize..."
sleep 30

# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"
```

**Success Criteria**:
- All 5 database containers running
- No "Exited" or "Restarting" status
- Ports accessible

**Recovery**:
```bash
# Check logs for failed containers
docker logs <container-name>

# Restart if needed
docker restart <container-name>
```

**Time Estimate**: 3 minutes + 30 seconds wait

---

### Task 6.2: Start OpenSPG Server
**Command** (on Mac):
```bash
# Start Minio (object storage for OpenSPG)
docker run -d \
  --name openspg-minio \
  --network aeon-net \
  -p 9000:9000 -p 9001:9001 \
  -v openspg-minio-data:/data \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  minio/minio:latest server /data --console-address ":9001"

# Wait for Minio
sleep 10

# Start OpenSPG Server
docker run -d \
  --name openspg-server \
  --network aeon-net \
  -p 8887:8887 \
  -v openspg-shared-data:/app/data \
  -v openspg-server-logs:/app/logs \
  -e NEO4J_URI=bolt://openspg-neo4j:7687 \
  -e NEO4J_USER=neo4j \
  -e NEO4J_PASSWORD=password \
  -e QDRANT_HOST=openspg-qdrant \
  -e QDRANT_PORT=6333 \
  -e MYSQL_HOST=openspg-mysql \
  -e MYSQL_PORT=3306 \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=openspg \
  -e REDIS_HOST=openspg-redis \
  -e REDIS_PORT=6379 \
  -e MINIO_ENDPOINT=openspg-minio:9000 \
  spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-server:latest

# Wait for server initialization
echo "Waiting 30 seconds for OpenSPG server to initialize..."
sleep 30

# Check status
docker ps --filter "name=openspg"
docker logs openspg-server | tail -20
```

**Success Criteria**:
- openspg-server container running
- Logs show no critical errors
- Server responding (check logs for "started" message)

**Recovery**:
```bash
# Check detailed logs
docker logs openspg-server

# Restart if needed
docker restart openspg-server
```

**Time Estimate**: 2 minutes + 30 seconds wait

---

### Task 6.3: Start NER11 Gold API
**Command** (on Mac):
```bash
cd ~/Projects/AEON/5_NER11_Gold_Model/docker

# Start using Mac-compatible compose file
docker compose -f docker-compose.mac.yml up -d

# Wait for API to initialize
echo "Waiting 45 seconds for NER11 API to initialize..."
sleep 45

# Check status
docker ps --filter "name=ner11-gold-api"
docker logs ner11-gold-api | tail -30
```

**Success Criteria**:
- ner11-gold-api container running and healthy
- Logs show "Application startup complete"
- No critical errors in logs

**Recovery**:
```bash
# Check full logs
docker logs ner11-gold-api > ner11_startup.log
cat ner11_startup.log | grep -i error

# Restart if needed
docker compose -f docker-compose.mac.yml restart ner11-gold-api
```

**Time Estimate**: 2 minutes + 45 seconds wait

---

### Task 6.4: Health Check - Database Connectivity
**Command** (on Mac):
```bash
echo "=== DATABASE CONNECTIVITY CHECKS ==="

# Neo4j health check
echo "Neo4j:"
docker exec openspg-neo4j cypher-shell -u neo4j -p password "RETURN 'Connected' as status;" 2>/dev/null && echo "✅ Connected" || echo "❌ Failed"

# Qdrant health check
echo "Qdrant:"
curl -s http://localhost:6333/healthz | grep -q "ok" && echo "✅ Healthy" || echo "❌ Unhealthy"

# Redis health check
echo "Redis:"
docker exec openspg-redis redis-cli ping | grep -q "PONG" && echo "✅ Connected" || echo "❌ Failed"

# MySQL health check
echo "MySQL:"
docker exec openspg-mysql mysql -uroot -popenspg -e "SELECT 'Connected' as status;" 2>/dev/null && echo "✅ Connected" || echo "❌ Failed"

# Postgres health check
echo "Postgres:"
docker exec aeon-postgres-dev psql -U postgres -c "SELECT 'Connected' as status;" 2>/dev/null && echo "✅ Connected" || echo "❌ Failed"
```

**Success Criteria**:
- All 5 databases return "Connected" or "Healthy"
- No "Failed" messages

**Recovery**:
```bash
# For failed database, check logs and restart
docker logs <failed-container>
docker restart <failed-container>
sleep 15
# Re-run health check
```

**Time Estimate**: 2 minutes

---

### Task 6.5: Health Check - API Endpoints
**Command** (on Mac):
```bash
echo "=== API ENDPOINT CHECKS ==="

# NER11 Gold API health check
echo "NER11 Gold API:"
curl -s http://localhost:8000/health | jq '.' 2>/dev/null && echo "✅ Responding" || echo "❌ Not responding"

# OpenSPG Server health check
echo "OpenSPG Server:"
curl -s http://localhost:8887/health | jq '.' 2>/dev/null && echo "✅ Responding" || echo "❌ Not responding"

# Test NER11 API endpoint
echo ""
echo "Testing NER11 API endpoint:"
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Test network device from Cisco", "entity_types": ["ORG", "PRODUCT"]}' \
  | jq '.'
```

**Success Criteria**:
- Both APIs responding with 200 status
- Health endpoints return valid JSON
- Test API call returns results

**Recovery**:
```bash
# Check API logs
docker logs ner11-gold-api | grep -i error
docker logs openspg-server | grep -i error

# Restart if needed
docker restart ner11-gold-api
docker restart openspg-server
```

**Time Estimate**: 3 minutes

---

### Task 6.6: Verify Model Files
**Command** (on Mac):
```bash
echo "=== MODEL FILES VERIFICATION ==="

cd ~/Projects/AEON/5_NER11_Gold_Model

# Check model directory structure
echo "Model directory structure:"
ls -lh models/ner11_v3/

# Check model files
echo ""
echo "Model files:"
find models/ner11_v3 -type f -name "*.bin" -o -name "*.pkl" -o -name "config.cfg" | xargs ls -lh

# Verify model is loaded in container
echo ""
echo "Model loaded in container:"
docker exec ner11-gold-api ls -la /app/models/ner11_v3/model-best/
```

**Success Criteria**:
- models/ner11_v3/model-best/ exists
- Model files present (vocab/lookups.bin, config.cfg, etc.)
- Container can access model files

**Recovery**:
```bash
# If model files missing, re-copy from USB
USB_PATH="/Volumes/<USB_NAME>"
rsync -av $USB_PATH/aeon_migration/project/5_NER11_Gold_Model/models/ ~/Projects/AEON/5_NER11_Gold_Model/models/

# Restart API container
docker restart ner11-gold-api
```

**Time Estimate**: 2 minutes

---

### Task 6.7: Frontend Setup Verification
**Command** (on Mac):
```bash
cd ~/Projects/AEON/1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1

# Check if package.json exists
if [ -f "package.json" ]; then
  echo "Frontend project found"

  # Install dependencies
  npm install

  # Verify installation
  npm list --depth=0

  echo ""
  echo "Frontend setup complete"
  echo "To start development server: npm run dev"
else
  echo "No frontend package.json found - may need separate setup"
fi
```

**Success Criteria**:
- npm install completes successfully
- No critical dependency errors
- Ready for `npm run dev`

**Recovery**:
```bash
# Clear npm cache and retry
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**Time Estimate**: 5-10 minutes (npm install time)

---

### Task 6.8: Full System Smoke Test
**Command** (on Mac):
```bash
echo "=== FULL SYSTEM SMOKE TEST ==="

# Container status check
echo "1. Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "ner11|openspg|aeon"

# Network connectivity check
echo ""
echo "2. Network Connectivity:"
docker exec ner11-gold-api ping -c 1 openspg-neo4j > /dev/null 2>&1 && echo "✅ NER11 → Neo4j" || echo "❌ NER11 → Neo4j"
docker exec ner11-gold-api ping -c 1 openspg-qdrant > /dev/null 2>&1 && echo "✅ NER11 → Qdrant" || echo "❌ NER11 → Qdrant"
docker exec openspg-server ping -c 1 openspg-mysql > /dev/null 2>&1 && echo "✅ OpenSPG → MySQL" || echo "❌ OpenSPG → MySQL"

# Data persistence check
echo ""
echo "3. Data Persistence Check:"
docker exec openspg-neo4j cypher-shell -u neo4j -p password "MATCH (n) RETURN count(n) as node_count;" 2>/dev/null && echo "✅ Neo4j data present" || echo "⚠️ Neo4j empty (may be normal)"
curl -s http://localhost:6333/collections | jq '.result.collections | length' && echo "✅ Qdrant collections present" || echo "⚠️ Qdrant empty (may be normal)"

# API integration test
echo ""
echo "4. API Integration Test:"
curl -s -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Cisco router with vulnerability CVE-2023-1234", "entity_types": ["ORG", "PRODUCT", "CVE"]}' \
  | jq -r 'if .entities then "✅ NER extraction working" else "❌ NER extraction failed" end'

# Git repository check
echo ""
echo "5. Git Repository Status:"
cd ~/Projects/AEON
git status | grep -q "nothing to commit" && echo "✅ Git clean" || echo "⚠️ Git has changes"
git log -1 --oneline

echo ""
echo "=== SMOKE TEST COMPLETE ==="
echo "Review any ❌ or ⚠️ items above"
```

**Success Criteria**:
- All containers running
- Network connectivity established
- Databases accessible
- API endpoints responding
- NER extraction working
- Git repository functional

**Recovery**: Address specific failures based on smoke test output

**Time Estimate**: 5 minutes

---

### Task 6.9: Create Mac Environment Documentation
**Command** (on Mac):
```bash
cat > ~/Projects/AEON/MAC_ENVIRONMENT.md << EOF
# AEON Mac Environment Configuration

## Migration Completed
- **Date**: $(date)
- **Source**: WSL2 Ubuntu
- **Destination**: macOS $(sw_vers -productVersion)
- **Docker**: $(docker --version)

## Running Containers
$(docker ps --format "- {{.Names}}: {{.Status}}")

## Volume Status
$(docker volume ls | grep -E "openspg|active|aeon")

## Network Configuration
$(docker network inspect aeon-net | jq -r '.[0].Containers | to_entries[] | "- \(.value.Name): \(.value.IPv4Address)"')

## API Endpoints
- NER11 Gold API: http://localhost:8000
- OpenSPG Server: http://localhost:8887
- Neo4j Browser: http://localhost:7474
- Qdrant Dashboard: http://localhost:6333/dashboard

## Database Credentials
- Neo4j: neo4j/password
- MySQL: root/openspg
- Postgres: postgres/postgres
- Redis: (no password)
- Minio: minioadmin/minioadmin

## Model Location
- Path: ~/Projects/AEON/5_NER11_Gold_Model/models/ner11_v3/model-best
- Container Path: /app/models/ner11_v3/model-best

## Important Notes
- GPU support disabled on Mac (CPU-only inference)
- Use docker-compose.mac.yml for NER11 API
- All data successfully migrated from WSL2
- Frontend requires: npm install && npm run dev

## Next Steps
1. Start frontend: cd 1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1 && npm run dev
2. Access API docs: http://localhost:8000/docs
3. Resume development on branch: $(git branch --show-current)

## Troubleshooting
- Logs: docker logs <container-name>
- Restart: docker restart <container-name>
- Full reset: docker compose down && docker compose up -d
EOF

cat ~/Projects/AEON/MAC_ENVIRONMENT.md
```

**Success Criteria**:
- Documentation created
- All environment info captured
- Ready for development

**Recovery**: N/A (documentation only)

**Time Estimate**: 3 minutes

---

### Task 6.10: Final Migration Validation
**Command** (on Mac):
```bash
echo "=== FINAL MIGRATION VALIDATION ==="

# Checklist
echo "Migration Validation Checklist:"
echo ""

# Project files
[ -d ~/Projects/AEON/5_NER11_Gold_Model ] && echo "✅ Project files migrated" || echo "❌ Project files missing"

# Git repository
cd ~/Projects/AEON
git log -1 > /dev/null 2>&1 && echo "✅ Git repository functional" || echo "❌ Git repository broken"

# Docker containers
RUNNING=$(docker ps | grep -E "ner11|openspg" | wc -l)
[ "$RUNNING" -ge 7 ] && echo "✅ All containers running ($RUNNING/7+)" || echo "⚠️ Some containers not running ($RUNNING/7+)"

# Docker volumes
VOLUMES=$(docker volume ls | grep -E "openspg|active" | wc -l)
[ "$VOLUMES" -ge 6 ] && echo "✅ All volumes restored ($VOLUMES/6+)" || echo "❌ Missing volumes ($VOLUMES/6)"

# Model files
[ -f ~/Projects/AEON/5_NER11_Gold_Model/models/ner11_v3/model-best/config.cfg ] && echo "✅ Model files present" || echo "❌ Model files missing"

# API health
curl -s http://localhost:8000/health > /dev/null 2>&1 && echo "✅ NER11 API healthy" || echo "❌ NER11 API not responding"

# Database connectivity
docker exec openspg-neo4j cypher-shell -u neo4j -p password "RETURN 1;" > /dev/null 2>&1 && echo "✅ Neo4j connected" || echo "❌ Neo4j connection failed"

curl -s http://localhost:6333/healthz | grep -q "ok" && echo "✅ Qdrant healthy" || echo "❌ Qdrant unhealthy"

# Network
docker network inspect aeon-net > /dev/null 2>&1 && echo "✅ Docker network configured" || echo "❌ Docker network missing"

echo ""
echo "=== VALIDATION COMPLETE ==="
echo ""
echo "If all items show ✅, migration is successful!"
echo "If any items show ❌, review Phase 5 tasks for that component."
echo ""
echo "To start development:"
echo "1. cd ~/Projects/AEON"
echo "2. Review MAC_ENVIRONMENT.md"
echo "3. Start frontend if needed"
echo "4. Resume work on branch: $(git branch --show-current)"
```

**Success Criteria**:
- All checklist items show ✅
- System ready for development
- Migration fully successful

**Recovery**: Address specific failures by re-running relevant Phase 5 tasks

**Time Estimate**: 3 minutes

---

## 📚 APPENDICES

### A. Quick Reference Commands

#### WSL2 (Source System)
```bash
# Check project size
du -sh ~/2_OXOT_Projects_Dev

# Export Docker volume
docker run --rm -v <volume>:/data -v /mnt/usb/backup:/backup alpine tar czf /backup/<name>.tar.gz -C /data .

# Git bundle create
git bundle create /path/to/bundle.bundle --all

# Stop all containers
docker stop $(docker ps -q)
```

#### macOS (Destination System)
```bash
# Import Docker volume
docker run --rm -v <volume>:/data -v /Volumes/USB/backup:/backup alpine sh -c "cd /data && tar xzf /backup/<name>.tar.gz"

# Clone from bundle
git clone /path/to/bundle.bundle <directory>

# Start containers
docker compose -f docker-compose.mac.yml up -d

# Check container logs
docker logs <container-name> -f
```

---

### B. Disk Space Requirements

| Component | Size | Priority | Notes |
|-----------|------|----------|-------|
| Project Files | ~5 GB | CRITICAL | Includes source code + models |
| Docker Volumes | ~2-4 GB | CRITICAL | Compressed, databases |
| Git Bundle | ~50-100 MB | CRITICAL | Full repository history |
| Docker Images | ~30 GB | OPTIONAL | Can rebuild on Mac |
| Config Files | ~1 MB | CRITICAL | Docker Compose, requirements |
| Documentation | ~1 MB | RECOMMENDED | Handoff docs, snapshots |
| **TOTAL (Minimum)** | **~8 GB** | - | Without Docker images |
| **TOTAL (Recommended)** | **~40 GB** | - | With Docker images |

---

### C. Rollback Procedures

#### If Migration Fails on Mac
1. WSL2 system remains intact and functional
2. Can continue development on WSL2
3. USB drive contains complete backup for retry
4. No data loss on source system

#### Rollback Steps
```bash
# On Mac - if something goes wrong
cd ~/Projects/AEON
rm -rf *  # Remove failed migration

# On WSL2 - verify system still works
docker ps
git status
# Continue working as normal
```

---

### D. Common Issues & Solutions

#### Issue: USB Drive Not Mounting on Mac
**Solution**:
1. Open Disk Utility (Applications > Utilities)
2. Select USB drive from sidebar
3. Click "Mount"
4. If fails, check format (should be exFAT or FAT32)

#### Issue: Docker Volume Import Fails
**Solution**:
```bash
# Verify tar.gz file integrity
tar -tzf /path/to/volume.tar.gz | head

# Try manual extraction
docker volume create <volume-name>
docker run --rm -v <volume-name>:/data alpine sh
# Inside container:
cd /data
# Copy tar.gz manually and extract
```

#### Issue: Git Bundle Clone Fails
**Solution**:
```bash
# Verify bundle integrity
git bundle verify /path/to/bundle.bundle

# List bundle contents
git bundle list-heads /path/to/bundle.bundle

# Try unbundle instead of clone
git init
git bundle unbundle /path/to/bundle.bundle
```

#### Issue: NER11 API Won't Start on Mac
**Solution**:
```bash
# Check if GPU references causing issues
# Edit docker-compose.mac.yml to remove ALL NVIDIA references

# Check model path
docker exec ner11-gold-api ls -la /app/models/ner11_v3/model-best/

# Check logs for specific error
docker logs ner11-gold-api | grep -i error

# Try running without GPU constraints
docker run -it --rm \
  -v ~/Projects/AEON/5_NER11_Gold_Model:/app \
  -p 8000:8000 \
  ner11-gold-api:latest \
  bash
# Test model loading manually inside container
```

#### Issue: OpenSPG Server Can't Connect to Databases
**Solution**:
```bash
# Verify network connectivity
docker network inspect aeon-net

# Check if containers can ping each other
docker exec openspg-server ping openspg-neo4j
docker exec openspg-server ping openspg-mysql

# Verify database credentials
docker exec openspg-neo4j cypher-shell -u neo4j -p password "RETURN 1;"
docker exec openspg-mysql mysql -uroot -popenspg -e "SELECT 1;"

# Restart in correct order
docker restart openspg-neo4j openspg-mysql openspg-redis openspg-qdrant
sleep 15
docker restart openspg-server
```

---

### E. Performance Optimization (Post-Migration)

#### Docker Desktop Settings (Mac)
1. Open Docker Desktop > Preferences > Resources
2. **CPUs**: Allocate 4-8 cores (50-75% of total)
3. **Memory**: Allocate 8-16 GB (NER models need RAM)
4. **Disk**: Allocate 60+ GB for images and volumes
5. **Swap**: 2-4 GB

#### Mac-Specific Optimizations
```bash
# Enable Docker BuildKit for faster builds
echo 'export DOCKER_BUILDKIT=1' >> ~/.zshrc
source ~/.zshrc

# Use Rosetta 2 for x86 containers on Apple Silicon (if needed)
# Docker Desktop > Settings > General > "Use Rosetta for x86/amd64 emulation"

# Optimize Python for Mac (if rebuilding containers)
# In Dockerfile, use:
# FROM python:3.11-slim AS base
# Instead of ubuntu-based images
```

---

### F. Verification Checklist

**Phase 2 Complete (WSL2)**:
- [ ] All Docker volumes exported (6 .tar.gz files)
- [ ] Project files copied to USB (~5 GB)
- [ ] Git bundle created and verified
- [ ] Configuration files backed up
- [ ] MANIFEST.txt created with checksums
- [ ] USB safely unmounted

**Phase 4 Complete (Mac)**:
- [ ] Homebrew installed
- [ ] Docker Desktop installed and running
- [ ] Python 3.11 installed
- [ ] Node.js installed
- [ ] Project directory created
- [ ] USB mounted and verified

**Phase 5 Complete (Mac)**:
- [ ] Project files restored
- [ ] Git repository cloned from bundle
- [ ] Docker network created
- [ ] Docker volumes restored (6 volumes)
- [ ] Docker images built/pulled
- [ ] docker-compose.mac.yml configured

**Phase 6 Complete (Mac)**:
- [ ] All containers running (7+)
- [ ] Neo4j accessible (port 7474, 7687)
- [ ] Qdrant healthy (port 6333)
- [ ] Redis connected (port 6379)
- [ ] MySQL connected (port 3306)
- [ ] Postgres connected (port 5432)
- [ ] NER11 API healthy (port 8000)
- [ ] OpenSPG Server healthy (port 8887)
- [ ] API integration test passing
- [ ] Model files accessible
- [ ] Git repository functional

---

### G. Contact & Support

**Migration Support**:
- Document all errors encountered
- Save log files: `docker logs <container> > container.log`
- Check Docker Desktop logs: Docker Desktop > Troubleshoot > Get Support
- WSL2 remains intact for reference/rollback

**Useful Resources**:
- Docker Desktop for Mac: https://docs.docker.com/desktop/mac/
- Neo4j Operations: https://neo4j.com/docs/operations-manual/
- Qdrant Documentation: https://qdrant.tech/documentation/
- Git Bundle: https://git-scm.com/docs/git-bundle

---

## 🎯 SUMMARY

### Total Estimated Time
- **Phase 1**: 30-45 minutes (Planning)
- **Phase 2**: 45-90 minutes (Data Extraction)
- **Phase 3**: 10 minutes (USB Transfer)
- **Phase 4**: 30-60 minutes (Mac Setup)
- **Phase 5**: 45-90 minutes (Data Restoration)
- **Phase 6**: 30-45 minutes (Verification)

**Total**: **3-5 hours** (depending on USB speed, Docker image rebuild time)

### Critical Success Factors
1. ✅ USB drive capacity (minimum 8 GB, recommended 32+ GB)
2. ✅ Git repository fully committed before migration
3. ✅ Docker volumes successfully exported and imported
4. ✅ Model files intact and accessible
5. ✅ All containers healthy after restoration
6. ✅ API endpoints responding correctly

### Risk Mitigation
- **LOW RISK**: WSL2 system remains intact throughout
- **SAFE ROLLBACK**: Can return to WSL2 if Mac setup fails
- **DATA PRESERVATION**: USB contains complete backup
- **INCREMENTAL VALIDATION**: Each phase verified before next

---

**END OF MIGRATION PLAN**

*Generated: 2025-12-04*
*Version: 1.0*
*Status: READY FOR EXECUTION*
