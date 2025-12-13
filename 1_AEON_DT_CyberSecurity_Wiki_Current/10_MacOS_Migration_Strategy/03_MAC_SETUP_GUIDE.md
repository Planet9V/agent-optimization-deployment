# macOS Setup Guide - Phase 3 & 4 Environment Preparation

**File:** 03_MAC_SETUP_GUIDE.md
**Created:** 2025-12-04 12:45:00 UTC
**Purpose:** Complete macOS environment setup before data restoration
**Status:** PLANNING PHASE - Ready for execution after USB transfer
**Phases:** 3 (Infrastructure Preparation) & 4 (macOS Setup)
**Estimated Duration:** 2-3 hours
**Prerequisites:** USB with all exported data, USB connected to macOS

---

## Overview

This guide walks through preparing a macOS development environment to receive AEON Digital Twin project data. After completing these steps, your Mac will have:

- ✅ Homebrew package manager (macOS software installation)
- ✅ Docker Desktop (containerization for databases and APIs)
- ✅ Python 3.10+ (for NER11 model and FastAPI)
- ✅ Node.js 18+ (for frontend development)
- ✅ Git (for repository management)
- ✅ Project directories (organized folder structure)
- ✅ USB data mounted and verified

---

## Task 3.1: Install Homebrew (macOS Package Manager)

### Purpose
Homebrew is macOS's package manager - necessary to install most development tools.

### Procedure

```bash
# 1. Check if Homebrew already installed
which brew

# If not found, proceed with installation

# 2. Install Homebrew (one command)
# Copy-paste the entire line below into Terminal
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 3. Wait for installation (5-10 minutes)
# Follow any on-screen prompts

# 4. Verify installation
brew --version
# Expected: Homebrew 3.x.x

# 5. Add Homebrew to PATH (if on Apple Silicon M1/M2/M3)
# For Apple Silicon Macs:
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# For Intel Macs:
# (Usually already in PATH)

# 6. Update Homebrew
brew update
```

**Expected Output:**
```
==> Installation successful!
Homebrew 3.x.x
```

**Success Criteria:** `brew --version` returns version number

---

## Task 3.2: Install Docker Desktop for macOS

### Purpose
Docker Desktop provides containerization for Neo4j, MySQL, and other services.

### Options

**Option A: Docker Desktop (Official - Recommended)**
```bash
# 1. Download Docker Desktop from:
# https://www.docker.com/products/docker-desktop

# 2. Choose correct version:
# - Apple Silicon (M1/M2/M3): "Apple Silicon" download
# - Intel Mac: "Intel Chip" download

# 3. Install by dragging Docker.app to Applications folder

# 4. Launch Docker Desktop from Applications
# Wait for "Docker is running" notification

# 5. Verify installation
docker --version
# Expected: Docker version 24.x.x

docker ps
# Expected: Shows empty container list (no error)
```

**Option B: OrbStack (Alternative - Faster)**
```bash
# OrbStack is a faster, lighter Docker alternative for macOS
brew install orbstack

# Verify
orbctl info
```

### Complete Docker Setup

```bash
# 1. Verify Docker is running
docker ps
# Should return successfully with no containers

# 2. Check Docker resources
docker stats --no-stream
# Verify CPU/Memory available

# 3. Increase Docker memory for databases
# Docker Desktop → Preferences → Resources
# Set Memory: 8 GB (minimum 6 GB)
# Set CPUs: 4 (minimum 2)
# Swap: 2 GB

# 4. Test Docker with simple container
docker run hello-world
# Should output "Hello from Docker!"

# 5. Create Docker network for OpenSPG services
docker network create openspg-network
# This network will be used for database containers
```

**Expected Output:**
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
(empty list - no containers yet)
```

**Success Criteria:**
- `docker --version` returns version
- `docker ps` returns without error
- `docker network create openspg-network` succeeds

---

## Task 3.3: Install Python 3.10+

### Purpose
Python is required for NER11 model and FastAPI backend.

### Procedure

```bash
# 1. Check if Python already installed
python3 --version
# Should be 3.10 or higher

# If already 3.10+, skip to task 3.4

# 2. Install Python via Homebrew
brew install python@3.11

# 3. Link Python installation
brew link python@3.11

# 4. Verify installation
python3 --version
# Expected: Python 3.11.x

# 5. Install pip (Python package manager)
python3 -m pip install --upgrade pip
# Expected: Successfully upgraded pip

# 6. Install common development packages
python3 -m pip install \
  virtualenv \
  setuptools \
  wheel

# 7. Test Python
python3 -c "import sys; print(f'Python {sys.version}')"
```

**Expected Output:**
```
Python 3.11.x (...)
```

**Success Criteria:**
- `python3 --version` shows 3.10+
- `pip --version` works
- Test import succeeds

---

## Task 3.4: Install Node.js and npm

### Purpose
Node.js/npm are required for frontend development (React/Next.js).

### Procedure

```bash
# 1. Check if Node.js already installed
node --version
npm --version
# Should be Node 18+ and npm 9+

# If already 18+, skip to task 3.5

# 2. Install Node.js via Homebrew
brew install node

# 3. Verify installation
node --version
# Expected: v18.x.x or higher

npm --version
# Expected: 9.x.x or higher

# 4. Update npm to latest
npm install -g npm@latest

# 5. Install common npm packages
npm install -g \
  typescript \
  yarn \
  pnpm

# 6. Test Node.js
node -e "console.log('Node.js working:', process.version)"
```

**Expected Output:**
```
v18.x.x or higher
9.x.x or higher
```

**Success Criteria:**
- `node --version` shows 18+
- `npm --version` shows 9+
- Global packages installed

---

## Task 3.5: Install Git

### Purpose
Git is required for repository cloning and version control.

### Procedure

```bash
# 1. Check if Git already installed
git --version
# Should be 2.x or higher

# If already 2.x, skip to task 3.6

# 2. Install Git via Homebrew
brew install git

# 3. Verify installation
git --version
# Expected: git version 2.x.x

# 4. Configure Git (if not already done)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 5. Generate SSH key for GitHub (optional but recommended)
ssh-keygen -t ed25519 -C "your.email@example.com"
# Press Enter for default location
# Press Enter twice for no passphrase (or set one)

# 6. Add SSH key to GitHub
# Copy public key:
cat ~/.ssh/id_ed25519.pub
# Paste into GitHub Settings → SSH and GPG keys → New SSH key

# 7. Test GitHub connection
ssh -T git@github.com
# Expected: "Hi username! You've successfully authenticated..."
```

**Expected Output:**
```
git version 2.x.x
Hi username! You've successfully authenticated...
```

**Success Criteria:**
- `git --version` shows 2.x+
- Git configured globally
- SSH authentication works (or HTTPS alternative)

---

## Task 3.6: Create Project Directory Structure

### Purpose
Create organized folders to receive AEON project data.

### Procedure

```bash
# 1. Create projects directory in home
mkdir -p ~/Projects
mkdir -p ~/Projects/aeon-dt

# 2. Create subdirectories for project organization
mkdir -p ~/Projects/aeon-dt/{source,data,models,logs,backups}

# 3. Create development workspace
mkdir -p ~/Projects/aeon-dt/source/{backend,frontend,infrastructure}
mkdir -p ~/Projects/aeon-dt/data/{databases,vectors,configs}
mkdir -p ~/Projects/aeon-dt/models/ner11

# 4. List structure
tree -L 3 ~/Projects/aeon-dt/
# Or if tree not installed:
find ~/Projects/aeon-dt -type d | head -20

# 5. Verify permissions
ls -la ~/Projects/aeon-dt/
# Should show your user as owner
```

**Expected Output:**
```
~/Projects/aeon-dt/
├── source/
│   ├── backend/
│   ├── frontend/
│   └── infrastructure/
├── data/
│   ├── databases/
│   ├── vectors/
│   └── configs/
├── models/
│   └── ner11/
├── logs/
└── backups/
```

**Success Criteria:**
- All directories created
- Directory structure is organized
- User has write permissions

---

## Task 3.7: Mount and Verify USB Drive

### Purpose
Prepare USB drive containing exported data for restoration.

### Procedure

```bash
# 1. Connect USB drive to macOS
# Physically connect the USB drive to Mac

# 2. List mounted drives
diskutil list
# Look for USB device (usually /dev/disk2 or similar)

# 3. Get USB device identifier
# Note the identifier from diskutil list output
USB_DEVICE="/dev/disk2"  # Example - adjust based on output

# 4. Create mount point
sudo mkdir -p /mnt/aeon_usb

# 5. Mount USB drive
# Option A: If already mounted in Finder, find mount point
mount | grep USB
# Usually something like /Volumes/[USB_Name]

# Option B: Mount manually
sudo mount -t exfat /dev/disk2s1 /mnt/aeon_usb
# Or for other file systems:
# sudo mount -t ntfs /dev/disk2s1 /mnt/aeon_usb  # For NTFS
# sudo mount -t vfat /dev/disk2s1 /mnt/aeon_usb  # For FAT32

# 6. Verify mount
mount | grep aeon
ls -la /mnt/aeon_usb/

# Expected to see: database/, models/, git_backup/, checksums/, etc.

# 7. Copy USB contents to backup location
# Creates local backup while keeping USB intact
cp -r /mnt/aeon_usb/AEON_Transfer ~/Projects/aeon-dt/backups/usb_contents_$(date +%Y%m%d)

# 8. Verify USB contents
ls -la ~/Projects/aeon-dt/backups/
# Should see database/, models/, git_backup/, checksums/
```

**Expected Output:**
```
/dev/disk2 (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                         *8.0 GB     disk2
   1:                        EFI                         209.7 MB    disk2s1
   2:           Microsoft Basic Data AEON_USB             7.8 GB     disk2s2

mount | grep aeon:
/mnt/aeon_usb on /dev/disk2s2 (exfat, local, nodev, nosuid, noowners)

ls -la /mnt/aeon_usb/:
total X
drwxr-xr-x database
drwxr-xr-x models
drwxr-xr-x git_backup
drwxr-xr-x checksums
...
```

**Success Criteria:**
- USB mounted successfully
- All exported directories visible
- Contents backed up locally

---

## Task 3.8: Verify USB Integrity on macOS

### Purpose
Confirm data integrity after USB transfer from WSL2 to macOS.

### Procedure

```bash
# 1. Navigate to USB backup
cd ~/Projects/aeon-dt/backups/usb_contents_[date]/

# 2. Verify checksums
cd checksums/
sha256sum -c CHECKSUMS_COMPLETE.sha256

# Expected: All files OK

# 3. Check individual components
echo "=== Checking Database Backups ==="
ls -lh ../database/neo4j/neo4j_backup_*.dump
ls -lh ../database/mysql/openspg_dump_*.sql.gz

echo "=== Checking NER11 Archive ==="
ls -lh ../models/ner11/NER11_Gold_Model.tar.gz

echo "=== Checking Git Bundle ==="
ls -lh ../git_backup/aeon_complete_*.bundle

# 4. Test archive integrity
tar -tzf ../models/ner11/NER11_Gold_Model.tar.gz > /dev/null
echo "✅ NER11 archive integrity verified"

# 5. Test git bundle
git bundle verify ../git_backup/aeon_complete_*.bundle
# Expected: The bundle is valid

# 6. Create verification report
cat > VERIFICATION_MACOS.txt << 'EOF'
AEON USB Verification on macOS
=============================
Date: $(date)
System: macOS

VERIFICATION STEPS COMPLETED:
✅ Checksums verified - All files intact
✅ Database backups verified
✅ NER11 archive integrity verified
✅ Git bundle verified

STATUS: ✅ USB Data Ready for Restoration

NEXT STEPS:
1. Proceed to 04_DATA_RESTORATION_GUIDE.md
2. Follow database restoration procedures
3. Restore project code from git bundle
4. Run 05_VALIDATION_PROCEDURES.md
EOF

cat VERIFICATION_MACOS.txt
```

**Expected Output:**
```
sha256sum -c CHECKSUMS_COMPLETE.sha256:
[All files]: OK

✅ NER11 archive integrity verified
The bundle is valid.

✅ USB Data Ready for Restoration
```

**Success Criteria:**
- All checksums verified
- All components verified
- Verification report created

---

## Task 3.9: Final Environment Verification

### Purpose
Confirm all tools are installed and working before data restoration.

### Procedure

```bash
# 1. Create comprehensive environment check script
cat > ~/check_environment.sh << 'EOF'
#!/bin/bash

echo "=== AEON macOS Environment Verification ==="
echo ""

# Check Homebrew
echo "Checking Homebrew..."
if command -v brew &> /dev/null; then
  echo "✅ Homebrew: $(brew --version)"
else
  echo "❌ Homebrew: NOT FOUND"
fi

# Check Docker
echo ""
echo "Checking Docker..."
if command -v docker &> /dev/null; then
  echo "✅ Docker: $(docker --version)"
  docker ps > /dev/null 2>&1 && echo "✅ Docker daemon running" || echo "⚠️ Docker daemon not running"
else
  echo "❌ Docker: NOT FOUND"
fi

# Check Python
echo ""
echo "Checking Python..."
if command -v python3 &> /dev/null; then
  PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
  echo "✅ Python: $PYTHON_VERSION"
  [[ "$PYTHON_VERSION" > "3.10" ]] && echo "✅ Version 3.10+ compatible" || echo "⚠️ Version older than 3.10"
else
  echo "❌ Python: NOT FOUND"
fi

# Check Node.js
echo ""
echo "Checking Node.js..."
if command -v node &> /dev/null; then
  echo "✅ Node.js: $(node --version)"
  echo "✅ npm: $(npm --version)"
else
  echo "❌ Node.js: NOT FOUND"
fi

# Check Git
echo ""
echo "Checking Git..."
if command -v git &> /dev/null; then
  echo "✅ Git: $(git --version)"
else
  echo "❌ Git: NOT FOUND"
fi

# Check project directories
echo ""
echo "Checking Project Directories..."
if [ -d ~/Projects/aeon-dt ]; then
  echo "✅ Project directory: ~/Projects/aeon-dt"
  echo "   Size: $(du -sh ~/Projects/aeon-dt | awk '{print $1}')"
else
  echo "❌ Project directory: NOT FOUND"
fi

# Check USB backup
echo ""
echo "Checking USB Backup..."
if [ -d ~/Projects/aeon-dt/backups ]; then
  echo "✅ Backup directory found"
  ls -1 ~/Projects/aeon-dt/backups/
else
  echo "⚠️ Backup directory not yet created"
fi

echo ""
echo "=== Verification Complete ==="
EOF

# 2. Make script executable
chmod +x ~/check_environment.sh

# 3. Run environment check
~/check_environment.sh

# 4. Example output processing
# If any items show ❌, install using Homebrew:
# brew install [missing-tool]
```

**Expected Output:**
```
=== AEON macOS Environment Verification ===

Checking Homebrew...
✅ Homebrew 3.x.x

Checking Docker...
✅ Docker version 24.x.x
✅ Docker daemon running

Checking Python...
✅ Python: 3.11.x
✅ Version 3.10+ compatible

Checking Node.js...
✅ Node.js: v18.x.x
✅ npm: 9.x.x

Checking Git...
✅ Git version 2.x.x

Checking Project Directories...
✅ Project directory: ~/Projects/aeon-dt

Checking USB Backup...
✅ Backup directory found
usb_contents_20251204

=== Verification Complete ===
```

**Success Criteria:**
- All tools show ✅
- All directories exist
- No ❌ items (all installations complete)

---

## Task 3.10: Prepare Docker Compose for Database Restoration

### Purpose
Pre-create Docker configuration files needed for database container restoration.

### Procedure

```bash
# 1. Create docker-compose directory
mkdir -p ~/Projects/aeon-dt/infrastructure/docker-compose

# 2. Create docker-compose.yml for database services
cat > ~/Projects/aeon-dt/infrastructure/docker-compose/docker-compose.databases.yml << 'EOF'
version: '3.8'

services:
  # Neo4j Graph Database
  openspg-neo4j:
    image: neo4j:5.26-community
    container_name: openspg-neo4j
    environment:
      NEO4J_ACCEPT_LICENSE_AGREEMENT: "yes"
      NEO4J_AUTH: neo4j/neo4j@openspg
    ports:
      - "7474:7474"  # Web UI
      - "7687:7687"  # Bolt protocol
    volumes:
      - openspg-neo4j-data:/var/lib/neo4j/data
      - ./backups:/var/lib/neo4j/backups
    networks:
      - openspg-network
    restart: unless-stopped

  # MySQL Database
  openspg-mysql:
    image: mysql:8.0
    container_name: openspg-mysql
    environment:
      MYSQL_ROOT_PASSWORD: openspg
      MYSQL_DATABASE: openspg
    ports:
      - "3306:3306"
    volumes:
      - openspg-mysql-data:/var/lib/mysql
    networks:
      - openspg-network
    restart: unless-stopped

  # Redis Cache (optional)
  openspg-redis:
    image: redis:7-alpine
    container_name: openspg-redis
    ports:
      - "6379:6379"
    volumes:
      - openspg-redis-data:/data
    networks:
      - openspg-network
    restart: unless-stopped

  # MinIO Object Storage (optional)
  openspg-minio:
    image: minio/minio:latest
    container_name: openspg-minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - openspg-minio-data:/data
    networks:
      - openspg-network
    restart: unless-stopped

volumes:
  openspg-neo4j-data:
  openspg-mysql-data:
  openspg-redis-data:
  openspg-minio-data:

networks:
  openspg-network:
    driver: bridge
EOF

# 3. Create docker-compose.yml for application services
cat > ~/Projects/aeon-dt/infrastructure/docker-compose/docker-compose.services.yml << 'EOF'
version: '3.8'

services:
  # NER11 API
  ner11-gold-api:
    image: ner11-gold-api:latest
    build:
      context: ../../source/backend
      dockerfile: Dockerfile
    container_name: ner11-gold-api
    ports:
      - "8000:8000"
    environment:
      PYTHONUNBUFFERED: "1"
    depends_on:
      - openspg-neo4j
      - openspg-mysql
    networks:
      - openspg-network
    volumes:
      - ../../models/ner11:/app/models
    restart: unless-stopped

  # Frontend Application
  aeon-frontend:
    image: aeon-frontend:latest
    build:
      context: ../../source/frontend
      dockerfile: Dockerfile
    container_name: aeon-frontend
    ports:
      - "3000:3000"
    depends_on:
      - ner11-gold-api
    networks:
      - openspg-network
    restart: unless-stopped

networks:
  openspg-network:
    external: true
EOF

# 4. Display files created
echo "✅ Docker Compose files created at:"
ls -la ~/Projects/aeon-dt/infrastructure/docker-compose/

# 5. Create restoration instructions
cat > ~/Projects/aeon-dt/infrastructure/RESTORATION_NOTES.md << 'EOF'
# Docker Service Restoration Instructions

## Pre-Restoration Checklist
- [ ] Docker Desktop is running
- [ ] Docker network 'openspg-network' is created
- [ ] Database backup files are in expected location
- [ ] NER11 models are extracted in ~/Projects/aeon-dt/models/ner11/

## Step 1: Create Docker Network
```bash
docker network create openspg-network
```

## Step 2: Start Database Services
```bash
cd ~/Projects/aeon-dt/infrastructure/docker-compose
docker-compose -f docker-compose.databases.yml up -d
```

## Step 3: Wait for Services to Initialize
```bash
docker-compose -f docker-compose.databases.yml ps
# Wait until all services are "Up"
```

## Step 4: Restore Data (See 04_DATA_RESTORATION_GUIDE.md)

## Step 5: Verify Restoration
```bash
docker-compose -f docker-compose.databases.yml logs neo4j | tail -20
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n)"
```

## Troubleshooting
- Check logs: `docker-compose logs [service-name]`
- Restart service: `docker-compose restart [service-name]`
- Remove and restart: `docker-compose down && docker-compose up -d`
EOF

echo "✅ Restoration notes created"
```

**Expected Output:**
```
✅ Docker Compose files created at:
total X
docker-compose.databases.yml
docker-compose.services.yml
RESTORATION_NOTES.md

✅ Restoration notes created
```

**Success Criteria:**
- Docker Compose files created
- All configuration templates ready
- Restoration notes documented

---

## Phase 3 & 4 Complete: Checkpoint Summary

### Verification Checklist

```bash
# Run final comprehensive check
echo "=== PHASE 3 & 4 COMPLETION CHECKLIST ==="
echo ""
echo "☐ Homebrew installed"
echo "☐ Docker Desktop installed and running"
echo "☐ Docker network 'openspg-network' created"
echo "☐ Python 3.10+ installed"
echo "☐ Node.js 18+ installed"
echo "☐ Git installed and configured"
echo "☐ Project directories created"
echo "☐ USB mounted and verified"
echo "☐ USB backup copied locally"
echo "☐ All checksums verified"
echo "☐ Docker Compose files prepared"
echo "☐ Environment check script passing"
echo ""
echo "If all items above are ✅, proceed to:"
echo "04_DATA_RESTORATION_GUIDE.md"
```

---

## Next Steps

**After completing Phase 3 & 4 (this guide):**

1. ✅ macOS environment fully prepared
2. ✅ All development tools installed
3. ✅ Docker ready for container services
4. ✅ Project directories created
5. ✅ USB data verified and backed up

**Proceed to:** `04_DATA_RESTORATION_GUIDE.md` to restore databases and project code

</content>
