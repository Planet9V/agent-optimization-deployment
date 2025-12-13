# AEON Project Mac Migration Architecture
**File:** AEON_MAC_MIGRATION_ARCHITECTURE.md
**Created:** 2025-12-04
**Version:** 1.0.0
**Author:** System Architecture Designer
**Purpose:** Comprehensive migration strategy for moving AEON project from Linux/WSL to macOS
**Status:** ACTIVE

## Executive Summary

This document provides multiple migration strategies for transitioning the AEON cybersecurity knowledge graph project from Windows WSL/Linux environment to macOS. The project consists of 12GB total size, including Docker infrastructure (Neo4j, MySQL, MinIO, Qdrant, Redis), a 3.5GB NER11 machine learning model, and frontend/backend code.

**Recommended Approach**: Hybrid Strategy (Option C) with risk mitigation through staging validation.

---

## 1. Current System Analysis

### 1.1 Project Inventory

```yaml
total_project_size: 12GB
working_directory: /home/jim/2_OXOT_Projects_Dev

code_repositories:
  git_remote: https://github.com/Planet9V/agent-optimization-deployment.git
  git_branch: gap-002-clean-VERIFIED
  python_files: 118
  javascript_typescript_files: 863

key_directories:
  - 5_NER11_Gold_Model: 3.5GB (includes 976MB trained models)
  - 1_AEON_DT_CyberSecurity_Wiki_Current: Documentation
  - 1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1: Frontend (1.3MB)
  - openspg-official_neo4j: Configuration (1.8MB)
  - docs: 20MB+ documentation
  - scripts: Automation utilities

docker_infrastructure:
  containers_active:
    - openspg-neo4j: Graph database (Neo4j 5.26-community)
    - openspg-mysql: Metadata storage
    - openspg-minio: Object storage (S3-compatible)
    - openspg-qdrant: Vector database
    - openspg-redis: Caching layer
    - ner11-gold-api: ML model API (29.6GB image)
    - aeon-saas-dev: Frontend application
    - aeon-postgres-dev: Development database

  critical_volumes:
    - openspg-neo4j-data: Graph database state (~135MB runtime, potentially larger with data)
    - openspg-mysql-data: Metadata (~29KB runtime)
    - openspg-minio-data: Object storage (~33MB runtime)
    - openspg-qdrant-data: Vector embeddings (~29KB runtime)
    - aeon-redis-data: Cache data (~12KB runtime)
    - aeon-postgres-dev: Development DB (~25KB runtime)

ml_models:
  ner11_v3:
    size: 976MB
    location: 5_NER11_Gold_Model/models/ner11_v3/
    components:
      - model-best: Production model
      - model-last: Latest training checkpoint
    dependencies: spaCy, transformers, torch
```

### 1.2 Current WSL Environment

```yaml
platform: Linux 5.15.167.4-microsoft-standard-WSL2
mounted_drives:
  - /mnt/c: Windows C: drive
  - /mnt/d: Windows D: drive

docker_environment: Docker Desktop for Windows (WSL2 backend)
node_version: Present (package.json exists)
python_version: Present (requirements.txt exists)
```

---

## 2. Mac-Specific Considerations

### 2.1 Docker Architecture Differences

| Aspect | Linux/WSL | macOS |
|--------|-----------|-------|
| **Docker Backend** | Native kernel | VM-based (HyperKit/Virtualization.framework) |
| **Performance** | Native speed | 10-30% slower I/O |
| **Volume Access** | Direct | Virtualized with osxfs/VirtioFS |
| **File Watching** | Efficient | Can be slow with large projects |
| **Memory** | Direct allocation | Shared with host OS |

### 2.2 Docker Options for Mac

**Option A: Docker Desktop for Mac**
- ✅ Official, well-supported
- ✅ GUI management
- ✅ File sharing works out-of-box
- ❌ Requires subscription for large teams
- ❌ Higher resource usage
- ⚠️ Performance slower than Linux

**Option B: Colima (Container Linux for macOS)**
- ✅ Open source, free
- ✅ Lower resource usage
- ✅ Compatible with Docker CLI
- ❌ Less GUI tooling
- ❌ Manual configuration needed
- ⚠️ Newer, less mature

**Option C: OrbStack** (Recommended)
- ✅ Fast, lightweight
- ✅ Better performance than Docker Desktop
- ✅ Native macOS integration
- ✅ Rosetta 2 support for Intel images on Apple Silicon
- ❌ Paid product (free tier available)
- ✅ Best choice for Apple Silicon Macs

**Recommendation**: OrbStack for Apple Silicon Macs (M1/M2/M3), Docker Desktop for Intel Macs.

### 2.3 File System Differences

| Item | Linux/WSL | macOS |
|------|-----------|-------|
| **File System** | ext4 | APFS |
| **Case Sensitivity** | Yes (by default) | No (by default, can enable) |
| **Path Separators** | `/` | `/` (same) |
| **USB Mount Path** | `/mnt/e:` or `/media/usb` | `/Volumes/[USB_NAME]` |
| **Max Filename Length** | 255 bytes | 255 characters |
| **Extended Attributes** | xattr | xattr (compatible) |

**Migration Impact**:
- File paths are mostly compatible
- USB drive detection is automatic on Mac
- Docker volume backup/restore works cross-platform

### 2.4 Apple Silicon Considerations

```yaml
apple_silicon_advantages:
  - Better battery life
  - Faster ML inference (Metal GPU acceleration)
  - Rosetta 2 for Intel Docker images (transparent)

apple_silicon_considerations:
  - ner11-gold-api image: 29.6GB (uses NVIDIA CUDA)
    resolution: Rebuild for ARM64 or use Rosetta 2 emulation
  - Neo4j 5.26: Native ARM64 support (no issues)
  - Other containers: All have ARM64 variants

intel_mac:
  - Full compatibility with existing Docker images
  - No rebuild required
  - Slightly slower than Apple Silicon for CPU tasks
```

---

## 3. Migration Strategy Options

### Option A: USB Drive Migration (Sequential Transfer)

**Approach**: Copy entire project to USB drive, then transfer to Mac.

#### Process Flow
```
1. Windows/WSL → USB Drive → Mac
2. Export Docker volumes → USB → Mac → Import
3. Validate on Mac → Remove Windows copy
```

#### Steps
```yaml
phase_1_preparation:
  - Commit all Git changes
  - Export Docker volumes to tar archives
  - Stop all containers
  - Tar project directory

phase_2_usb_transfer:
  - Mount USB drive (exFAT or ext4 format)
  - Copy project tar to USB (~12GB)
  - Copy Docker volume archives to USB (~500MB estimated)
  - Safely eject USB

phase_3_mac_import:
  - Mount USB on Mac (/Volumes/[NAME])
  - Extract project to ~/Projects/AEON
  - Install Docker (OrbStack recommended)
  - Import Docker volumes
  - Rebuild ner11-gold-api for ARM64 (if Apple Silicon)
  - Start containers and validate

phase_4_validation:
  - Health checks for all services
  - Frontend API connectivity test
  - Neo4j graph query test
  - NER11 model inference test
```

#### Pros & Cons
```yaml
pros:
  - Simple, straightforward process
  - Complete data portability
  - No network dependency
  - Full offline capability
  - Easy rollback (keep USB copy)

cons:
  - Requires USB drive (16GB+ recommended)
  - Sequential process (longer total time)
  - Windows environment disrupted during copy
  - Single point of failure (USB drive)
  - Manual verification at each step

time_estimate: 3-4 hours
risk_level: LOW
recommended_for: ["single-user", "offline-environment", "simple-setup"]
```

---

### Option B: Network Transfer (rsync/SSH)

**Approach**: Direct network transfer from Windows/WSL to Mac using rsync.

#### Process Flow
```
1. Windows/WSL ⟷ Mac (over network)
2. Incremental file sync with rsync
3. Docker volumes transferred separately
```

#### Prerequisites
```yaml
mac_setup:
  - Enable Remote Login (System Preferences → Sharing → Remote Login)
  - Get Mac IP address: ifconfig en0 | grep inet
  - Ensure SSH key authentication (optional but recommended)

wsl_setup:
  - Install rsync: sudo apt install rsync
  - Test SSH connection: ssh user@mac-ip
```

#### Steps
```yaml
phase_1_initial_sync:
  command: |
    rsync -avz --progress /home/jim/2_OXOT_Projects_Dev/ user@mac-ip:~/Projects/AEON/
  notes:
    - First sync takes longest (~12GB)
    - Subsequent syncs are incremental
    - Can run while working on Windows

phase_2_docker_volumes:
  export_volumes:
    - docker run --rm -v openspg-neo4j-data:/data -v $(pwd):/backup alpine tar czf /backup/neo4j-data.tar.gz -C /data .
    - docker run --rm -v openspg-mysql-data:/data -v $(pwd):/backup alpine tar czf /backup/mysql-data.tar.gz -C /data .
    - docker run --rm -v openspg-minio-data:/data -v $(pwd):/backup alpine tar czf /backup/minio-data.tar.gz -C /data .

  transfer_volumes:
    - rsync -avz --progress *.tar.gz user@mac-ip:~/Projects/AEON/docker-volumes/

phase_3_mac_import:
  import_volumes:
    - docker volume create openspg-neo4j-data
    - docker run --rm -v openspg-neo4j-data:/data -v ~/Projects/AEON/docker-volumes:/backup alpine sh -c "cd /data && tar xzf /backup/neo4j-data.tar.gz"

  start_services:
    - cd ~/Projects/AEON
    - docker compose up -d
```

#### Pros & Cons
```yaml
pros:
  - No USB drive required
  - Incremental sync capability
  - Can continue working during initial sync
  - Faster for multiple iterations
  - Automatic resume on network interruption

cons:
  - Requires network connectivity
  - SSH configuration required
  - Both machines must be on simultaneously
  - Slower initial transfer over WiFi
  - Potential security considerations

time_estimate: 2-3 hours (depends on network speed)
risk_level: MEDIUM
recommended_for: ["network-available", "iterative-migration", "experienced-users"]
```

---

### Option C: Hybrid Strategy (Git + USB + Rebuild) ⭐ RECOMMENDED

**Approach**: Use Git for code, USB for data, rebuild/download models on Mac.

#### Philosophy
```
Code → Git (version control, already done)
Data → USB transfer (Docker volumes)
Models → Download fresh on Mac OR transfer if bandwidth-constrained
```

#### Process Flow
```
1. Commit and push all code to GitHub
2. Export critical Docker volumes to USB
3. On Mac: Clone Git repo
4. Import Docker volumes from USB
5. Download/rebuild ML models
6. Validate complete system
```

#### Steps
```yaml
phase_1_windows_preparation:
  git_operations:
    - git add .
    - git commit -m "Pre-migration checkpoint"
    - git push origin gap-002-clean-VERIFIED
    - Verify GitHub remote is accessible

  docker_volume_export:
    neo4j: |
      docker run --rm -v openspg-neo4j-data:/data -v /mnt/e:/backup alpine \
        tar czf /backup/aeon-neo4j-$(date +%Y%m%d).tar.gz -C /data .

    mysql: |
      docker run --rm -v openspg-mysql-data:/data -v /mnt/e:/backup alpine \
        tar czf /backup/aeon-mysql-$(date +%Y%m%d).tar.gz -C /data .

    minio: |
      docker run --rm -v openspg-minio-data:/data -v /mnt/e:/backup alpine \
        tar czf /backup/aeon-minio-$(date +%Y%m%d).tar.gz -C /data .

    qdrant: |
      docker run --rm -v openspg-qdrant-data:/data -v /mnt/e:/backup alpine \
        tar czf /backup/aeon-qdrant-$(date +%Y%m%d).tar.gz -C /data .

  model_decision:
    if_bandwidth_unlimited: "Download fresh on Mac (spaCy models, transformers)"
    if_bandwidth_limited: "Copy 5_NER11_Gold_Model/models to USB (976MB)"

phase_2_mac_setup:
  development_environment:
    - Install Homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    - Install Git: brew install git
    - Install Docker:
        - OrbStack (Apple Silicon): brew install orbstack
        - Docker Desktop (Intel): brew install --cask docker
    - Install Node.js: brew install node
    - Install Python: brew install python@3.11

  project_setup:
    - mkdir -p ~/Projects
    - cd ~/Projects
    - git clone https://github.com/Planet9V/agent-optimization-deployment.git AEON
    - cd AEON
    - git checkout gap-002-clean-VERIFIED

  python_environment:
    - python3 -m venv venv
    - source venv/bin/activate
    - pip install -r requirements.txt

  node_environment:
    - npm install

phase_3_docker_volume_import:
  volume_restoration:
    neo4j: |
      docker volume create openspg-neo4j-data
      docker run --rm -v openspg-neo4j-data:/data \
        -v /Volumes/YOUR_USB/:/backup alpine \
        sh -c "cd /data && tar xzf /backup/aeon-neo4j-*.tar.gz"

    mysql: |
      docker volume create openspg-mysql-data
      docker run --rm -v openspg-mysql-data:/data \
        -v /Volumes/YOUR_USB/:/backup alpine \
        sh -c "cd /data && tar xzf /backup/aeon-mysql-*.tar.gz"

    minio: |
      docker volume create openspg-minio-data
      docker run --rm -v openspg-minio-data:/data \
        -v /Volumes/YOUR_USB/:/backup alpine \
        sh -c "cd /data && tar xzf /backup/aeon-minio-*.tar.gz"

    qdrant: |
      docker volume create openspg-qdrant-data
      docker run --rm -v openspg-qdrant-data:/data \
        -v /Volumes/YOUR_USB/:/backup alpine \
        sh -c "cd /data && tar xzf /backup/aeon-qdrant-*.tar.gz"

phase_4_docker_rebuild:
  apple_silicon_specific:
    ner11_api_rebuild: |
      cd ~/Projects/AEON/5_NER11_Gold_Model/docker
      # Edit Dockerfile to use ARM64 base image
      docker build --platform linux/arm64 -t ner11-gold-api:latest .

    or_use_rosetta: |
      # In docker-compose.yml, add:
      # platform: linux/amd64
      # OrbStack will use Rosetta 2 automatically

  network_creation:
    - docker network create openspg-network

  container_startup:
    - cd ~/Projects/AEON
    - docker compose up -d

phase_5_validation:
  health_checks:
    - docker ps  # Verify all containers running
    - docker logs openspg-neo4j | tail -20
    - docker logs openspg-server | tail -20
    - docker logs ner11-gold-api | tail -20

  connectivity_tests:
    neo4j: "Open http://localhost:7474 (user: neo4j, pass: neo4j@openspg)"
    openspg: "curl http://localhost:8887/health"
    ner11_api: "curl http://localhost:8000/health"
    frontend: "Open http://localhost:3000"

  functional_tests:
    - Run Neo4j query: "MATCH (n) RETURN count(n) LIMIT 1"
    - Test NER11 API: "curl -X POST http://localhost:8000/api/extract ..."
    - Verify frontend loads
```

#### Pros & Cons
```yaml
pros:
  - Clean separation: code vs data
  - Version control ensures code integrity
  - Flexibility in model handling
  - Can skip unnecessary data
  - Fresh Mac environment (no cruft)
  - Easy to verify each component
  - Best practice for production

cons:
  - Multiple steps (more complex)
  - Requires GitHub access
  - Need to rebuild Docker images
  - Model download time (if not copied)
  - More initial setup on Mac

time_estimate: 2-3 hours (first time), 30 minutes (subsequent)
risk_level: LOW (most resilient)
recommended_for: ["production-environment", "clean-migration", "best-practice"]
```

---

### Option D: Cloud Staging (S3/MinIO Intermediate)

**Approach**: Upload to cloud storage, download on Mac.

#### Process Flow
```
1. Windows/WSL → AWS S3 or other cloud
2. Mac ← Download from S3
3. Clean up cloud storage
```

#### When to Use
```yaml
use_cases:
  - Multiple machines need same data
  - Long-term backup desired
  - Fast internet connection available
  - Team collaboration needed

requirements:
  - AWS account or cloud storage
  - s3cmd or AWS CLI installed
  - Sufficient bandwidth (upload + download 12GB)
```

#### Pros & Cons
```yaml
pros:
  - Geographic independence
  - Backup created as side effect
  - Can share with team
  - Versioning available (S3)
  - No USB drive needed

cons:
  - Costs money (AWS S3 charges)
  - Requires cloud account
  - Upload + download time (double transfer)
  - Security considerations (encryption needed)
  - Bandwidth consumption

time_estimate: 4-6 hours (depends on bandwidth)
risk_level: MEDIUM-HIGH (data security)
recommended_for: ["team-environment", "cloud-first", "backup-desired"]
```

---

## 4. Critical Path Analysis

### 4.1 Must Have on Day 1 (Priority 1)

```yaml
essential_for_development:
  git_repository:
    - All source code
    - package.json, requirements.txt
    - docker-compose.yml
    - Configuration files
    transfer_method: Git clone

  docker_volumes_critical:
    - openspg-neo4j-data: Contains graph database state
    - openspg-mysql-data: Schema and metadata
    transfer_method: USB or network export/import

  development_tools:
    - Docker runtime (OrbStack/Docker Desktop)
    - Node.js + npm
    - Python 3.11 + pip
    - Git
    transfer_method: Fresh install on Mac
```

### 4.2 Can Download on Mac (Priority 2)

```yaml
downloadable_fresh:
  ml_models:
    - spaCy language models: python -m spacy download en_core_web_trf
    - Hugging Face transformers: Auto-downloaded on first use
    - PyTorch: pip install torch
    estimated_size: 2-3GB
    estimated_time: 20-30 minutes

  docker_images:
    - neo4j:5.26-community: 500MB
    - redis:7-alpine: 30MB
    - minio/minio:latest: 100MB
    - qdrant/qdrant:latest: 200MB
    estimated_time: 15-20 minutes

  node_dependencies:
    - npm install: Downloads from npmjs.com
    estimated_size: 200MB
    estimated_time: 5 minutes
```

### 4.3 USB Transfer Needed (Priority 1)

```yaml
custom_or_stateful:
  docker_volumes:
    - openspg-neo4j-data: Custom graph data
    - openspg-mysql-data: Application schema
    - openspg-minio-data: Uploaded objects (if any)
    - openspg-qdrant-data: Vector embeddings
    estimated_size: 500MB-1GB

  trained_models:
    - 5_NER11_Gold_Model/models/ner11_v3/: 976MB
    decision: Transfer if bandwidth limited, otherwise retrain/download
```

### 4.4 Can Rebuild on Mac (Priority 3)

```yaml
rebuildable:
  redis_cache: Empty on startup (acceptable)
  docker_images: Rebuild from Dockerfile
  node_modules: npm install
  python_venv: pip install -r requirements.txt

reasoning: These have no persistent state or can be regenerated
```

---

## 5. Docker Volume Strategy

### 5.1 Volume Identification

```yaml
critical_volumes:
  openspg-neo4j-data:
    purpose: Graph database storage
    estimated_size: 135MB runtime (can grow to GB with data)
    backup_priority: CRITICAL

  openspg-mysql-data:
    purpose: Application metadata and schema
    estimated_size: 29KB runtime
    backup_priority: CRITICAL

  openspg-minio-data:
    purpose: S3-compatible object storage
    estimated_size: 33MB runtime
    backup_priority: HIGH

  openspg-qdrant-data:
    purpose: Vector embeddings for semantic search
    estimated_size: 29KB runtime
    backup_priority: HIGH

  aeon-redis-data:
    purpose: Cache layer
    estimated_size: 12KB runtime
    backup_priority: LOW (can rebuild)

  aeon-postgres-dev:
    purpose: Development database
    estimated_size: 25KB runtime
    backup_priority: MEDIUM
```

### 5.2 Export Process

```bash
#!/bin/bash
# export_docker_volumes.sh
# Run on Windows/WSL before migration

BACKUP_DIR="/mnt/e/aeon-backup"  # Adjust to your USB drive path
mkdir -p "$BACKUP_DIR"

# Export Neo4j (most critical)
echo "Exporting Neo4j data..."
docker run --rm \
  -v openspg-neo4j-data:/data \
  -v "$BACKUP_DIR":/backup \
  alpine \
  tar czf /backup/neo4j-data-$(date +%Y%m%d).tar.gz -C /data .

# Export MySQL
echo "Exporting MySQL data..."
docker run --rm \
  -v openspg-mysql-data:/data \
  -v "$BACKUP_DIR":/backup \
  alpine \
  tar czf /backup/mysql-data-$(date +%Y%m%d).tar.gz -C /data .

# Export MinIO
echo "Exporting MinIO data..."
docker run --rm \
  -v openspg-minio-data:/data \
  -v "$BACKUP_DIR":/backup \
  alpine \
  tar czf /backup/minio-data-$(date +%Y%m%d).tar.gz -C /data .

# Export Qdrant
echo "Exporting Qdrant data..."
docker run --rm \
  -v openspg-qdrant-data:/data \
  -v "$BACKUP_DIR":/backup \
  alpine \
  tar czf /backup/qdrant-data-$(date +%Y%m%d).tar.gz -C /data .

echo "Export complete! Backup location: $BACKUP_DIR"
ls -lh "$BACKUP_DIR"
```

### 5.3 Import Process on Mac

```bash
#!/bin/bash
# import_docker_volumes.sh
# Run on Mac after Docker installation

USB_PATH="/Volumes/YOUR_USB_NAME/aeon-backup"  # Adjust to your USB name
BACKUP_DATE="20251204"  # Adjust to your backup date

# Create volumes first
docker volume create openspg-neo4j-data
docker volume create openspg-mysql-data
docker volume create openspg-minio-data
docker volume create openspg-qdrant-data

# Import Neo4j
echo "Importing Neo4j data..."
docker run --rm \
  -v openspg-neo4j-data:/data \
  -v "$USB_PATH":/backup \
  alpine \
  sh -c "cd /data && tar xzf /backup/neo4j-data-${BACKUP_DATE}.tar.gz"

# Import MySQL
echo "Importing MySQL data..."
docker run --rm \
  -v openspg-mysql-data:/data \
  -v "$USB_PATH":/backup \
  alpine \
  sh -c "cd /data && tar xzf /backup/mysql-data-${BACKUP_DATE}.tar.gz"

# Import MinIO
echo "Importing MinIO data..."
docker run --rm \
  -v openspg-minio-data:/data \
  -v "$USB_PATH":/backup \
  alpine \
  sh -c "cd /data && tar xzf /backup/minio-data-${BACKUP_DATE}.tar.gz"

# Import Qdrant
echo "Importing Qdrant data..."
docker run --rm \
  -v openspg-qdrant-data:/data \
  -v "$USB_PATH":/backup \
  alpine \
  sh -c "cd /data && tar xzf /backup/qdrant-data-${BACKUP_DATE}.tar.gz"

echo "Import complete!"
docker volume ls | grep openspg
```

### 5.4 Verification

```bash
# Verify volume data imported correctly
docker run --rm -v openspg-neo4j-data:/data alpine ls -lah /data
docker run --rm -v openspg-mysql-data:/data alpine ls -lah /data
docker run --rm -v openspg-minio-data:/data alpine ls -lah /data
docker run --rm -v openspg-qdrant-data:/data alpine ls -lah /data
```

---

## 6. File Organization on Mac

### 6.1 Recommended Directory Structure

```
~/Projects/
├── AEON/                          # Main project (from Git)
│   ├── .git/                      # Git repository
│   ├── docker-compose.yml         # Docker orchestration
│   ├── 5_NER11_Gold_Model/        # ML model code
│   │   ├── api/                   # FastAPI routes
│   │   ├── models/                # Trained models (976MB)
│   │   ├── tests/                 # Unit tests
│   │   └── docker/                # Dockerfile for API
│   ├── 1_AEON_DT_CyberSecurity_Wiki_Current/  # Documentation
│   ├── scripts/                   # Automation
│   ├── src/                       # Source code
│   ├── tests/                     # Test suites
│   ├── docs/                      # Architecture docs
│   └── venv/                      # Python virtual environment (created on Mac)
│
├── AEON-backups/                  # Backup location
│   └── docker-volumes/            # Exported volume archives
│
└── AEON-data/                     # Large datasets (optional)
    └── external-datasets/         # Symlink target for USB storage
```

### 6.2 USB Mounting Conventions

```yaml
macos_usb_mounting:
  auto_mount_location: /Volumes/[USB_DRIVE_NAME]
  examples:
    - /Volumes/AEON_DATA
    - /Volumes/Untitled  # Default for unnamed drives

  mount_verification:
    - ls /Volumes/
    - df -h | grep Volumes

  eject_safely:
    - diskutil unmount /Volumes/[NAME]
    - Or use Finder → Right-click → Eject
```

### 6.3 Symlink Strategy

```bash
# For large datasets on external USB (optional)
# Keeps project directory clean, data on fast external SSD

# On Mac with USB mounted
ln -s /Volumes/AEON_DATA/training-datasets ~/Projects/AEON/data/external

# Verify symlink
ls -la ~/Projects/AEON/data/external
# Should show -> /Volumes/AEON_DATA/training-datasets
```

### 6.4 .gitignore Additions for Mac

```gitignore
# macOS specific
.DS_Store
.AppleDouble
.LSOverride

# Thumbnails
._*

# Files that might appear on external disks
.Spotlight-V100
.Trashes

# Python virtual environment (Mac-specific paths)
venv/
.venv/
.Python

# Docker volume backups (don't commit to Git)
docker-volumes/*.tar.gz

# Large model files (use Git LFS or external storage)
5_NER11_Gold_Model/models/*.bin
5_NER11_Gold_Model/models/*.pt
```

---

## 7. Validation Strategy

### 7.1 Pre-Migration Checklist

```yaml
windows_wsl_verification:
  - [ ] All code committed to Git: git status
  - [ ] All branches pushed: git push --all
  - [ ] Docker containers healthy: docker ps
  - [ ] Export all Docker volumes: ./export_docker_volumes.sh
  - [ ] Verify backup archives created: ls -lh /mnt/e/aeon-backup/
  - [ ] Test one volume restore (dry run)
  - [ ] Document any custom configurations
  - [ ] Export environment variables: env | grep -E "(NEO4J|MYSQL|MINIO)" > env-backup.txt
```

### 7.2 Post-Migration Validation Matrix

```yaml
level_1_infrastructure:
  docker_installation:
    - [ ] Docker engine running: docker version
    - [ ] Docker Compose available: docker compose version
    - [ ] Volumes imported: docker volume ls | grep openspg
    - [ ] Network created: docker network ls | grep openspg

  development_tools:
    - [ ] Node.js installed: node --version (>= 18.x)
    - [ ] Python installed: python3 --version (>= 3.11)
    - [ ] Git configured: git config --list
    - [ ] npm packages installed: npm list --depth=0
    - [ ] Python packages installed: pip list

level_2_services:
  container_health:
    - [ ] Neo4j running: docker ps | grep openspg-neo4j
    - [ ] MySQL running: docker ps | grep openspg-mysql
    - [ ] MinIO running: docker ps | grep openspg-minio
    - [ ] Qdrant running: docker ps | grep openspg-qdrant
    - [ ] Redis running: docker ps | grep openspg-redis
    - [ ] NER11 API running: docker ps | grep ner11-gold-api
    - [ ] Frontend running: docker ps | grep aeon-saas-dev

  health_endpoints:
    - [ ] Neo4j browser: http://localhost:7474 (responds)
    - [ ] OpenSPG API: curl http://localhost:8887/health
    - [ ] NER11 API: curl http://localhost:8000/health
    - [ ] MinIO console: http://localhost:9001 (login successful)
    - [ ] Qdrant API: curl http://localhost:6333/healthz
    - [ ] Frontend: http://localhost:3000 (loads)

level_3_functionality:
  neo4j_tests:
    - [ ] Connect via Bolt: cypher-shell -u neo4j -p neo4j@openspg
    - [ ] Basic query: MATCH (n) RETURN count(n) LIMIT 1
    - [ ] Multi-hop query: MATCH path=(a)-[*1..3]-(b) RETURN path LIMIT 5
    - [ ] APOC available: RETURN apoc.version()

  api_tests:
    - [ ] NER11 extraction: curl -X POST localhost:8000/api/extract -d '{"text":"..."}'
    - [ ] Vendor API: curl localhost:8000/api/vendor/list
    - [ ] SBOM API: curl localhost:8000/api/sbom/analyze
    - [ ] Threat Intel API: curl localhost:8000/api/threat/correlate

  frontend_tests:
    - [ ] Home page loads
    - [ ] API connection established
    - [ ] Graph visualization renders
    - [ ] Search functionality works

level_4_performance:
  benchmarks:
    - [ ] Neo4j query response < 500ms
    - [ ] NER11 inference < 2s for 100 words
    - [ ] Frontend load time < 3s
    - [ ] Docker volume I/O acceptable

  resource_usage:
    - [ ] Memory usage < 80% (docker stats)
    - [ ] CPU usage reasonable
    - [ ] Disk I/O not thrashing
```

### 7.3 Health Check Script

```bash
#!/bin/bash
# health_check_mac.sh
# Comprehensive validation script for Mac migration

echo "=== AEON Mac Migration Health Check ==="
echo ""

# Infrastructure
echo "1. Docker Infrastructure"
docker --version && echo "✅ Docker installed" || echo "❌ Docker missing"
docker compose version && echo "✅ Docker Compose available" || echo "❌ Docker Compose missing"
docker volume ls | grep -q openspg-neo4j-data && echo "✅ Neo4j volume exists" || echo "❌ Neo4j volume missing"
docker network ls | grep -q openspg-network && echo "✅ OpenSPG network exists" || echo "❌ Network missing"
echo ""

# Services
echo "2. Container Health"
for container in openspg-neo4j openspg-mysql openspg-minio openspg-qdrant openspg-redis ner11-gold-api aeon-saas-dev; do
    if docker ps | grep -q "$container"; then
        health=$(docker inspect --format='{{.State.Health.Status}}' "$container" 2>/dev/null || echo "no-healthcheck")
        echo "✅ $container: running ($health)"
    else
        echo "❌ $container: not running"
    fi
done
echo ""

# API Endpoints
echo "3. API Health Checks"
curl -sf http://localhost:7474 > /dev/null && echo "✅ Neo4j browser responsive" || echo "❌ Neo4j browser unreachable"
curl -sf http://localhost:8887/health > /dev/null && echo "✅ OpenSPG API healthy" || echo "❌ OpenSPG API down"
curl -sf http://localhost:8000/health > /dev/null && echo "✅ NER11 API healthy" || echo "❌ NER11 API down"
curl -sf http://localhost:9001 > /dev/null && echo "✅ MinIO console accessible" || echo "❌ MinIO console down"
curl -sf http://localhost:6333/healthz > /dev/null && echo "✅ Qdrant healthy" || echo "❌ Qdrant down"
curl -sf http://localhost:3000 > /dev/null && echo "✅ Frontend accessible" || echo "❌ Frontend down"
echo ""

# Functionality
echo "4. Functional Tests"
docker exec openspg-neo4j cypher-shell -u neo4j -p neo4j@openspg "RETURN 1" > /dev/null 2>&1 && \
    echo "✅ Neo4j query execution works" || echo "❌ Neo4j query failed"

echo ""
echo "=== Health Check Complete ==="
```

---

## 8. Recommended Migration Plan

### 8.1 Executive Summary

**Recommended Strategy**: **Option C - Hybrid Strategy** (Git + USB + Selective Rebuild)

**Rationale**:
- ✅ Cleanest separation of code vs. data
- ✅ Leverages version control (Git) for code integrity
- ✅ USB transfer for stateful data (Docker volumes)
- ✅ Flexibility in handling large ML models
- ✅ Lowest risk (can rollback at any step)
- ✅ Best practice for production environments
- ✅ Easy to document and repeat

### 8.2 Timeline

```yaml
day_1_preparation: (2 hours)
  - Commit all changes to Git
  - Push to GitHub
  - Export Docker volumes to USB
  - Verify backup integrity

day_2_mac_setup: (1 hour)
  - Install development tools (Homebrew, OrbStack, Node, Python)
  - Clone Git repository
  - Set up Python/Node environments

day_3_docker_migration: (2 hours)
  - Import Docker volumes from USB
  - Create Docker network
  - Start containers (rebuild if needed)
  - Run health checks

day_4_validation: (1 hour)
  - Comprehensive functional testing
  - Performance benchmarking
  - Documentation update

total_time: 6 hours (can be split over multiple days)
```

### 8.3 Risk Mitigation

```yaml
backup_strategy:
  - Keep Windows/WSL environment intact until Mac fully validated
  - USB drive becomes permanent backup
  - GitHub serves as code backup
  - Can recreate environment from scratch if needed

rollback_plan:
  - If Mac migration fails, Windows/WSL still operational
  - USB contains complete Docker volume snapshots
  - Git history allows reverting to any previous state

validation_gates:
  - Stage 1: Infrastructure (Docker, tools) must pass before proceeding
  - Stage 2: Services (containers) must be healthy before testing
  - Stage 3: Functionality tests must pass before production use
  - Stage 4: Performance must be acceptable before Windows decommission
```

### 8.4 Success Criteria

```yaml
migration_complete_when:
  infrastructure:
    - Docker running on Mac (OrbStack or Docker Desktop)
    - All development tools installed (Node, Python, Git)
    - Project cloned from Git

  services:
    - All Docker containers running and healthy
    - All volumes imported successfully
    - Network connectivity established

  functionality:
    - Neo4j queries execute successfully
    - NER11 API responds to inference requests
    - Frontend loads and connects to backend
    - All API endpoints return valid responses

  performance:
    - Query response times acceptable (< 500ms for simple queries)
    - ML inference time reasonable (< 2s for 100 words)
    - No excessive CPU/memory usage
    - Docker I/O not bottlenecked

  validation:
    - Comprehensive test suite passes
    - Health check script returns all green
    - Documentation updated
    - Backup verified
```

---

## 9. Apple Silicon Specific Guidance

### 9.1 Architecture Differences

```yaml
apple_silicon_m1_m2_m3:
  architecture: ARM64 (aarch64)
  advantages:
    - Better battery life (2-3x vs Intel)
    - Faster CPU for single-thread tasks
    - Superior ML inference (Metal acceleration)
    - Cooler, quieter operation

  docker_compatibility:
    native_arm64: "Most images have ARM64 variants"
    rosetta2_emulation: "Transparent for Intel images (some performance penalty)"
    performance_impact: "5-15% slower for emulated images"

intel_mac:
  architecture: x86_64
  advantages:
    - 100% compatibility with existing Docker images
    - No rebuild required for any containers
    - Proven compatibility

  considerations:
    - Slower than Apple Silicon for most tasks
    - Higher power consumption
    - May thermal throttle under load
```

### 9.2 Container Rebuild for Apple Silicon

```yaml
requires_rebuild:
  ner11_gold_api:
    reason: "Uses NVIDIA CUDA base image (x86_64 only)"
    solution_1_rebuild: |
      # Update 5_NER11_Gold_Model/docker/Dockerfile
      # Change FROM to ARM64-compatible base
      FROM python:3.11-slim-bookworm
      # Remove NVIDIA-specific layers
      # Use Metal acceleration or CPU

    solution_2_rosetta: |
      # In docker-compose.yml, add:
      platform: linux/amd64
      # OrbStack will use Rosetta 2 automatically

    recommendation: "Use Rosetta 2 initially, rebuild for native ARM64 later if performance critical"

no_rebuild_needed:
  - neo4j:5.26-community (has ARM64 variant)
  - redis:7-alpine (multi-arch)
  - minio/minio:latest (multi-arch)
  - qdrant/qdrant:latest (multi-arch)
  - postgres:16-alpine (multi-arch)
  - nginx:alpine (multi-arch)
```

### 9.3 Performance Optimization

```yaml
orbstack_configuration:
  memory_allocation: "8-12GB for AEON project"
  cpu_cores: "4-6 cores"
  disk_space: "50GB minimum"
  virtualization_framework: "Rosetta 2 enabled"

docker_desktop_alternative:
  why_orbstack_better:
    - 50% less memory usage
    - Faster container startup
    - Better ARM64 support
    - More efficient virtualization
    - Native macOS integration

metal_acceleration:
  pytorch_metal: |
    # Enable Metal acceleration for PyTorch on Apple Silicon
    pip install torch torchvision torchaudio
    # Auto-detects Metal, no code changes needed

  tensorflow_metal: |
    # If using TensorFlow
    pip install tensorflow-metal
```

---

## 10. Troubleshooting Guide

### 10.1 Common Issues

```yaml
issue_docker_volumes_not_importing:
  symptom: "tar: Error opening archive: Failed to open '/backup/*.tar.gz'"
  causes:
    - USB drive not mounted
    - Incorrect path in command
    - Backup file corrupted
  solutions:
    - Verify USB mount: ls /Volumes/
    - Check file exists: ls -la /Volumes/YOUR_USB/aeon-backup/
    - Test archive integrity: tar tzf /Volumes/YOUR_USB/aeon-backup/neo4j-data-*.tar.gz
    - Re-export from Windows if corrupted

issue_neo4j_wont_start:
  symptom: "Container exits immediately or health check fails"
  causes:
    - Volume data corrupted
    - Memory allocation insufficient
    - Port conflict (7474/7687 already in use)
  solutions:
    - Check logs: docker logs openspg-neo4j
    - Verify volume: docker run --rm -v openspg-neo4j-data:/data alpine ls -la /data
    - Check ports: lsof -i :7474,7687
    - Increase Docker memory: OrbStack Settings → Resources → Memory

issue_ner11_api_failing_apple_silicon:
  symptom: "exec /usr/bin/python3: exec format error"
  causes:
    - x86_64 image on ARM64 without Rosetta
  solutions:
    - Enable Rosetta in OrbStack: Settings → Features → Rosetta
    - Or add to docker-compose.yml:
      ```yaml
      ner11-gold-api:
        platform: linux/amd64
      ```
    - Or rebuild for ARM64 (see section 9.2)

issue_slow_docker_performance:
  symptom: "Containers respond slowly, high CPU usage"
  causes:
    - Insufficient resources allocated
    - Volume I/O bottleneck
    - Rosetta emulation overhead
  solutions:
    - Increase OrbStack memory/CPU allocation
    - Use VirtioFS for better I/O: OrbStack Settings → Features → VirtioFS
    - Consider rebuilding images for native ARM64
    - Check Activity Monitor for resource hogs

issue_frontend_cant_connect_to_api:
  symptom: "Network error, CORS issues"
  causes:
    - Containers on different networks
    - Firewall blocking localhost
    - Environment variables incorrect
  solutions:
    - Verify network: docker network inspect openspg-network
    - Check .env files in frontend project
    - Test API directly: curl http://localhost:8000/health
    - Restart frontend container: docker restart aeon-saas-dev
```

### 10.2 Validation Failures

```yaml
neo4j_query_fails:
  - Verify authentication: cypher-shell -u neo4j -p neo4j@openspg
  - Check database exists: SHOW DATABASES
  - Ensure APOC installed: RETURN apoc.version()
  - Restart Neo4j: docker restart openspg-neo4j

api_endpoints_timeout:
  - Check container logs: docker logs <container-name>
  - Verify dependencies running: docker ps
  - Test individual services: curl http://localhost:<port>/health
  - Check firewall: sudo pfctl -d (temporarily disable)

model_inference_errors:
  - Verify model files exist: ls -la 5_NER11_Gold_Model/models/ner11_v3/
  - Check Python environment: docker exec ner11-gold-api pip list
  - Download missing models: docker exec ner11-gold-api python -m spacy download en_core_web_trf
  - Rebuild container: docker compose up -d --build ner11-gold-api
```

---

## 11. Post-Migration Optimization

### 11.1 Performance Tuning

```yaml
docker_optimization:
  orbstack_settings:
    - Enable VirtioFS for faster I/O
    - Allocate 8-12GB RAM
    - Use 4-6 CPU cores
    - Enable Rosetta 2 for Intel images

  docker_compose_adjustments:
    neo4j:
      - Reduce heap if Mac has < 16GB RAM: NEO4J_server_memory_heap_max__size=4G
      - Use SSD for volumes (default on Mac)

    ner11_api:
      - Consider rebuilding for ARM64 if slow
      - Use Metal acceleration for PyTorch

mac_system_optimization:
  - Close unnecessary apps during development
  - Use Activity Monitor to identify resource hogs
  - Consider external SSD for Docker volumes (Thunderbolt 3/4)
  - Enable "Reduce Motion" for better performance (Accessibility settings)
```

### 11.2 Development Workflow

```yaml
recommended_tools:
  - Orbiter: GUI for OrbStack (included)
  - Docker Desktop Dashboard: Alternative (if using Docker Desktop)
  - TablePlus: Database GUI (Neo4j, MySQL, PostgreSQL)
  - Postman/Insomnia: API testing
  - Neo4j Browser: Built-in graph visualization

ide_configuration:
  vscode:
    - Install "Remote - Containers" extension
    - Configure Python interpreter: venv/bin/python
    - Set Node.js version: use nvm

  pycharm:
    - Configure Docker interpreter
    - Set up remote debugging for containers

git_workflow:
  - Branches: Always use feature branches
  - Commits: Frequent, small commits
  - Remote: Keep GitHub remote up-to-date
  - Backup: USB drive + GitHub = redundant backup
```

---

## 12. Cost Analysis

### 12.1 Software Costs

```yaml
free_options:
  docker_runtime:
    - OrbStack: Free tier available (sufficient for single user)
    - Colima: Fully free and open source
  development_tools:
    - Homebrew: Free
    - Node.js, Python, Git: Free
    - VS Code: Free

paid_options:
  docker_desktop:
    cost: "$5-21/month per user (for organizations)"
    when_required: "Companies with >250 employees or >$10M revenue"

  orbstack:
    cost: "$8/month or $96/year"
    recommendation: "Free tier sufficient for AEON project"

  ide:
    - VS Code: Free
    - PyCharm Professional: $89/year (not required, Community Edition is free)
```

### 12.2 Hardware Recommendations

```yaml
minimum_specs:
  mac: "MacBook Air M1 (8GB RAM)"
  usb_drive: "16GB USB 3.0 flash drive"
  estimated_cost: "$0 (use existing hardware)"

recommended_specs:
  mac: "MacBook Pro M2/M3 (16GB RAM)"
  usb_drive: "128GB USB-C SSD (for future backups)"
  external_storage: "1TB Thunderbolt SSD (optional, for large datasets)"
  estimated_cost: "$0-150 (USB SSD if needed)"

optimal_specs:
  mac: "Mac Studio M2 Ultra (64GB RAM)"
  storage: "2TB internal SSD + 2TB Thunderbolt RAID"
  estimated_cost: "$200+ (external storage)"
```

---

## 13. Appendix

### 13.1 Quick Reference Commands

```bash
# === Windows/WSL Export ===
# Export all volumes to USB drive
docker run --rm -v VOLUME_NAME:/data -v /mnt/e:/backup alpine \
  tar czf /backup/VOLUME-$(date +%Y%m%d).tar.gz -C /data .

# === Mac Import ===
# Create and import volume
docker volume create VOLUME_NAME
docker run --rm -v VOLUME_NAME:/data -v /Volumes/USB:/backup alpine \
  sh -c "cd /data && tar xzf /backup/VOLUME-*.tar.gz"

# === Docker Management ===
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down

# Remove all volumes (CAUTION!)
docker volume rm $(docker volume ls -q)

# === Health Checks ===
# Check container status
docker ps --format "table {{.Names}}\t{{.Status}}"

# Test Neo4j
docker exec openspg-neo4j cypher-shell -u neo4j -p neo4j@openspg "RETURN 1"

# Test NER11 API
curl http://localhost:8000/health

# === Mac USB Management ===
# List mounted volumes
ls /Volumes/

# Unmount USB safely
diskutil unmount /Volumes/USB_NAME
```

### 13.2 Environment Variables

```bash
# ~/.zshrc or ~/.bash_profile additions for Mac

# AEON Project Environment
export AEON_PROJECT_HOME="$HOME/Projects/AEON"
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="neo4j@openspg"
export NER_API_URL="http://localhost:8000"

# Python Virtual Environment
export VIRTUAL_ENV="$AEON_PROJECT_HOME/venv"
alias aeon-activate="source $AEON_PROJECT_HOME/venv/bin/activate"

# Docker Shortcuts
alias dps="docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
alias dlogs="docker compose logs -f"
alias dup="docker compose up -d"
alias ddown="docker compose down"
```

### 13.3 Docker Compose Override (Mac-Specific)

```yaml
# docker-compose.override.yml
# Place in project root for Mac-specific overrides

version: "3.8"

services:
  # Apple Silicon: Force Rosetta 2 for Intel images
  ner11-gold-api:
    platform: linux/amd64
    environment:
      - PYTORCH_ENABLE_MPS_FALLBACK=1  # Metal Performance Shaders fallback

  # Adjust resource limits for Mac
  neo4j:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 12G
        reservations:
          cpus: '2'
          memory: 8G
```

### 13.4 Backup Checklist

```yaml
before_migration:
  - [ ] Git status clean: git status
  - [ ] All branches pushed: git push --all
  - [ ] Docker volumes exported
  - [ ] Environment variables documented
  - [ ] USB drive formatted (exFAT or APFS)
  - [ ] Backup verified

after_migration:
  - [ ] All services running
  - [ ] Health checks passing
  - [ ] Functional tests passing
  - [ ] Performance acceptable
  - [ ] Documentation updated
  - [ ] Windows environment can be decommissioned
```

---

## 14. Decision Matrix

```yaml
choose_option_a_usb_sequential:
  if:
    - Simple, straightforward migration preferred
    - No network available or unreliable
    - USB drive available (16GB+)
    - Single-user environment
  time: 3-4 hours
  risk: LOW
  complexity: LOW

choose_option_b_network_transfer:
  if:
    - Reliable network available
    - Want to continue working during migration
    - SSH experience available
    - Need incremental sync capability
  time: 2-3 hours
  risk: MEDIUM
  complexity: MEDIUM

choose_option_c_hybrid_git_usb:
  if:
    - Best practice desired
    - Clean environment important
    - Git workflow already established
    - Team collaboration possible in future
  time: 2-3 hours (initial), 30 min (repeat)
  risk: LOW
  complexity: MEDIUM
  recommendation: ⭐ RECOMMENDED

choose_option_d_cloud_staging:
  if:
    - Team environment
    - Backup desired as side effect
    - Budget for cloud storage available
    - Multiple machines need same data
  time: 4-6 hours
  risk: MEDIUM-HIGH
  complexity: HIGH
```

---

## 15. Conclusion

The **Hybrid Strategy (Option C)** provides the best balance of:
- **Risk mitigation** (Git + USB redundancy)
- **Clean separation** (code vs. data)
- **Production readiness** (best practices)
- **Flexibility** (selective component transfer)
- **Repeatability** (documented, scriptable)

### Next Steps

1. **Review this document** with stakeholders
2. **Schedule migration window** (6 hours, can be split)
3. **Execute Windows preparation** (Phase 1)
4. **Set up Mac environment** (Phase 2)
5. **Import and validate** (Phases 3-5)
6. **Decommission Windows environment** (after validation)

### Success Metrics

- ✅ All containers running and healthy
- ✅ All API endpoints responsive
- ✅ Neo4j queries execute successfully
- ✅ NER11 model inference works
- ✅ Frontend loads and functions
- ✅ Performance acceptable (< 500ms query response)
- ✅ Documentation updated

---

**End of Document**

**Version History**:
- v1.0.0 (2025-12-04): Initial architecture design

**References**:
- Docker Documentation: https://docs.docker.com/
- OrbStack Documentation: https://docs.orbstack.dev/
- Neo4j Operations Manual: https://neo4j.com/docs/
- Apple Silicon Docker Guide: https://docs.docker.com/desktop/mac/apple-silicon/
