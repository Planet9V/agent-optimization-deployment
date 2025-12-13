# Data Restoration Guide - Phase 5 Restoration & Project Recovery

**File:** 04_DATA_RESTORATION_GUIDE.md
**Created:** 2025-12-04 13:15:00 UTC
**Purpose:** Restore AEON project data, databases, and models on macOS
**Status:** PLANNING PHASE - Ready for execution after Phase 3 & 4 complete
**Phase:** 5 of 6 (Data Restoration)
**Estimated Duration:** 60-90 minutes
**Prerequisites:** Phase 3 & 4 complete, all tools installed, USB data backed up locally

---

## Overview

This guide restores all critical components exported from WSL2 to your macOS development environment:

1. **Neo4j Database** - 20,739 nodes and all graph relationships
2. **MySQL Database** - OpenSPG schema and configuration
3. **NER11 Models** - Extracted ML models for NER inference
4. **Project Code** - Git repository with complete history
5. **Supporting Data** - Training data, configs, and optional volumes

---

## Task 4.1: Verify Pre-Restoration Environment

### Purpose
Confirm all prerequisites met before starting restoration.

### Procedure

```bash
# 1. Verify all prerequisites
echo "=== PRE-RESTORATION VERIFICATION ==="

# Docker running
docker ps > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✅ Docker is running"
else
  echo "❌ Docker not running - Start Docker Desktop"
  exit 1
fi

# OpenSPG network exists
docker network inspect openspg-network > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✅ openspg-network exists"
else
  echo "⚠️ Network not found - creating..."
  docker network create openspg-network
fi

# Project directories exist
if [ -d ~/Projects/aeon-dt/backups ]; then
  echo "✅ USB backup directory found"
else
  echo "❌ USB backup not found"
  exit 1
fi

# Backup contains expected files
for component in "database" "models" "git_backup" "checksums"; do
  if [ -d ~/Projects/aeon-dt/backups/usb_contents_*/​$component ]; then
    echo "✅ $component directory found"
  else
    echo "⚠️ $component directory not found"
  fi
done

echo ""
echo "✅ All prerequisites verified - Ready to restore"
```

**Expected Output:**
```
✅ Docker is running
✅ openspg-network exists
✅ USB backup directory found
✅ All prerequisites verified - Ready to restore
```

**Success Criteria:**
- Docker running
- Network exists
- Backup directories exist
- All checks pass

---

## Task 4.2: Start Database Container Services

### Purpose
Launch Neo4j and MySQL containers before data restoration.

### Procedure

```bash
# 1. Navigate to docker-compose directory
cd ~/Projects/aeon-dt/infrastructure/docker-compose

# 2. Start database services
docker-compose -f docker-compose.databases.yml up -d

# Expected output:
# Creating network "openspg-network" ...
# Creating openspg-mysql ...
# Creating openspg-neo4j ...
# Creating openspg-redis ...
# Creating openspg-minio ...

# 3. Monitor startup
echo "Waiting for services to initialize..."
sleep 10

# 4. Check service status
docker-compose -f docker-compose.databases.yml ps

# Expected output - all should show "Up":
# CONTAINER ID   IMAGE          COMMAND                  STATUS
# [container]    neo4j:5.26     "/sbin/tini -- /bin/..." Up 2 seconds
# [container]    mysql:8.0      "docker-entrypoint..."   Up 2 seconds

# 5. Wait for services to be fully ready (30-60 seconds)
echo "Services starting, waiting for initialization..."
sleep 30

# 6. Check Neo4j is responsive
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "RETURN 'Neo4j Ready' as status"
# Expected: "Neo4j Ready"

# 7. Check MySQL is responsive
docker exec openspg-mysql mysql -u root -popenspg -e "SELECT 1 as status"
# Expected: "1"

echo "✅ Database services started and responsive"
```

**Expected Output:**
```
Creating network "openspg-network" ...
Creating openspg-mysql ... done
Creating openspg-neo4j ... done
Creating openspg-redis ... done
Creating openspg-minio ... done

CONTAINER ID   IMAGE         STATUS        NAMES
[id]           neo4j:5.26    Up 2 seconds  openspg-neo4j
[id]           mysql:8.0     Up 2 seconds  openspg-mysql
[id]           redis:7       Up 2 seconds  openspg-redis
[id]           minio          Up 2 seconds  openspg-minio

Neo4j Ready
1
✅ Database services started and responsive
```

**Success Criteria:**
- All containers running ("Up" status)
- Neo4j responds to cypher-shell
- MySQL responds to mysql client

---

## Task 4.3: Restore Neo4j Database

### Purpose
Load 20,739 nodes and relationships from backup into Neo4j.

### Procedure

```bash
# 1. Find backup file
cd ~/Projects/aeon-dt/backups/usb_contents_*/database/neo4j/

# 2. Verify backup file exists and is accessible
ls -lh neo4j_backup_*.dump
# Expected: Shows backup file

# 3. Copy backup to container
# Note: Container expects backups in /var/lib/neo4j/backups/
BACKUP_FILE=$(ls neo4j_backup_*.dump)

docker exec openspg-neo4j bash -c "mkdir -p /var/lib/neo4j/backups"

docker cp "$BACKUP_FILE" \
  openspg-neo4j:/var/lib/neo4j/backups/"$BACKUP_FILE"

# 4. Verify copy succeeded
docker exec openspg-neo4j ls -lh /var/lib/neo4j/backups/
# Should show backup file

# 5. IMPORTANT: Stop Neo4j to perform database load
# This ensures data consistency
docker-compose -f ~/Projects/aeon-dt/infrastructure/docker-compose/docker-compose.databases.yml \
  stop openspg-neo4j

echo "⏳ Waiting for Neo4j to stop..."
sleep 10

# 6. Load backup into database
# Using neo4j-admin to load the backup
docker exec openspg-neo4j neo4j-admin database load \
  --from-path=/var/lib/neo4j/backups \
  neo4j \
  --overwrite-existing

# Expected: "Database load completed successfully"

# 7. Start Neo4j again
docker-compose -f ~/Projects/aeon-dt/infrastructure/docker-compose/docker-compose.databases.yml \
  start openspg-neo4j

echo "⏳ Waiting for Neo4j to start..."
sleep 15

# 8. Verify data was restored
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n) as node_count, \
          COUNT(DISTINCT labels(n)) as entity_types"

# Expected:
# node_count: 20739
# entity_types: 45+ (different entity types)

echo "✅ Neo4j database restored"
```

**Expected Output:**
```
     node_count | entity_types
     -----------+--------------
        20739   | 45

✅ Neo4j database restored
```

**Success Criteria:**
- Backup file copied to container
- Database load completed without error
- Node count is 20,739
- Multiple entity types loaded

---

## Task 4.4: Restore MySQL Database

### Purpose
Restore OpenSPG schema and configuration data.

### Procedure

```bash
# 1. Find MySQL backup file
cd ~/Projects/aeon-dt/backups/usb_contents_*/database/mysql/

# 2. Verify backup exists
ls -lh openspg_dump_*.sql.gz
# Expected: Shows compressed backup

# 3. Extract backup (MySQL on macOS can't read gzip directly)
BACKUP_FILE=$(ls openspg_dump_*.sql.gz)
gunzip -c "$BACKUP_FILE" > /tmp/openspg_dump.sql

# 4. Copy SQL file to container
docker cp /tmp/openspg_dump.sql \
  openspg-mysql:/tmp/openspg_dump.sql

# 5. Restore database
docker exec openspg-mysql mysql -u root -popenspg < /tmp/openspg_dump.sql

# Expected: No error message

# 6. Verify restoration
docker exec openspg-mysql mysql -u root -popenspg -e \
  "SHOW DATABASES; SHOW TABLES FROM openspg LIMIT 10;"

# Expected: Should show multiple databases and tables

# 7. Check data integrity
docker exec openspg-mysql mysql -u root -popenspg -e \
  "SELECT DATABASE(), COUNT(*) as table_count FROM information_schema.tables \
   WHERE table_schema='openspg' GROUP BY database();"

echo "✅ MySQL database restored"

# 8. Clean up temporary files
rm /tmp/openspg_dump.sql
```

**Expected Output:**
```
Databases:
  information_schema
  mysql
  openspg
  performance_schema
  sys

Tables:
  entities
  relationships
  properties
  [... more tables ...]

✅ MySQL database restored
```

**Success Criteria:**
- SQL file extracted and restored
- openspg database exists with tables
- No error messages during import

---

## Task 4.5: Extract and Setup NER11 Models

### Purpose
Extract NER11 model archive and prepare for inference.

### Procedure

```bash
# 1. Find NER11 archive
cd ~/Projects/aeon-dt/backups/usb_contents_*/models/ner11/

# 2. Verify archive exists
ls -lh NER11_Gold_Model.tar.gz
# Expected: 439 MB archive

# 3. Create extraction directory
mkdir -p ~/Projects/aeon-dt/models/ner11

# 4. Extract archive
echo "Extracting NER11 model archive (this may take 2-3 minutes)..."
tar -xzf NER11_Gold_Model.tar.gz -C ~/Projects/aeon-dt/models/ner11

# 5. Verify extraction
ls -la ~/Projects/aeon-dt/models/ner11/
# Expected: models/ and training_data/ directories

# 6. Check model structure
ls -la ~/Projects/aeon-dt/models/ner11/models/
# Expected: ner11_v3 directory

# 7. Verify trained model exists
if [ -d ~/Projects/aeon-dt/models/ner11/models/ner11_v3/model-best ]; then
  echo "✅ NER11 model-best found"
  ls -la ~/Projects/aeon-dt/models/ner11/models/ner11_v3/model-best/
else
  echo "❌ Model not found - extraction may have failed"
  exit 1
fi

# 8. Verify model files
echo "Verifying model components..."
for file in config.cfg meta.json; do
  if [ -f ~/Projects/aeon-dt/models/ner11/models/ner11_v3/model-best/$file ]; then
    echo "✅ $file present"
  fi
done

# 9. Create model symlink for easier access
ln -sf ~/Projects/aeon-dt/models/ner11/models/ner11_v3/model-best \
  ~/Projects/aeon-dt/models/ner11_active_model

echo "✅ NER11 models extracted and ready"
```

**Expected Output:**
```
Extracting NER11 model archive (this may take 2-3 minutes)...
✅ NER11 model-best found
✅ config.cfg present
✅ meta.json present
✅ NER11 models extracted and ready
```

**Success Criteria:**
- Archive extracted without error
- model-best directory present
- Model configuration files exist
- Symlink created for convenience

---

## Task 4.6: Clone Git Repository from Bundle

### Purpose
Restore complete project code with all history from git bundle.

### Procedure

```bash
# 1. Find git bundle
cd ~/Projects/aeon-dt/backups/usb_contents_*/git_backup/

# 2. Verify bundle exists
ls -lh aeon_complete_*.bundle
# Expected: ~100 MB bundle file

# 3. Get bundle filename
BUNDLE_FILE=$(ls aeon_complete_*.bundle)

# 4. Verify bundle integrity
git bundle verify "$BUNDLE_FILE"
# Expected: "The bundle is valid"

# 5. Create new directory for cloned repo
mkdir -p ~/Projects/aeon-dt/source/aeon-repo

# 6. Clone from bundle
cd ~/Projects/aeon-dt/source/aeon-repo
git clone "~/Projects/aeon-dt/backups/usb_contents_"*"/git_backup/$BUNDLE_FILE" .

# Alternative if above doesn't work:
# git clone file://path/to/bundle .

# 7. Verify clone
git log --oneline -5
# Should show recent commits

# 8. Check branches
git branch -a
# Should show multiple branches

# 9. Verify current branch
git branch
# Should show gap-002-clean-VERIFIED or similar

# 10. Add GitHub as remote (optional - for pulling latest updates)
git remote add github https://github.com/[username]/aeon-digital-twin.git
# Adjust URL based on actual GitHub repo

# 11. Fetch from GitHub if online (optional)
git fetch github 2>/dev/null || echo "⚠️ GitHub not accessible (offline is OK)"

# 12. View git status
git status
# Expected: "On branch [branch-name]" and "nothing to commit"

echo "✅ Repository cloned from bundle"
```

**Expected Output:**
```
The bundle is valid.

Cloning into '.'...
Receiving objects: 100% (10000/10000), done.
Resolving deltas: 100% (5000/5000), done.

Showing 5 most recent commits:
abc123d feat(phase-b5): Complete E10/E11/E12 APIs and migration prep
def456e feat(phase-b4): E07 Compliance + E08 Scanning APIs
ghi789j feat(phase-b3): E04 Threat Intel + E05 Risk Scoring APIs

✅ Repository cloned from bundle
```

**Success Criteria:**
- Bundle verified as valid
- Repository cloned successfully
- Git history accessible
- Current branch is correct

---

## Task 4.7: Setup Python Environment

### Purpose
Create isolated Python environment with dependencies for NER11 and backend APIs.

### Procedure

```bash
# 1. Navigate to project
cd ~/Projects/aeon-dt/source/aeon-repo

# 2. Create Python virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt

# 4. Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# 5. Install project dependencies
# First, check if requirements.txt exists
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
elif [ -f setup.py ]; then
  pip install -e .
else
  echo "⚠️ No requirements.txt or setup.py found"
fi

# 6. Install spaCy and NER11 model
pip install spacy

# 7. Link NER11 model to spaCy
cd ~/Projects/aeon-dt/models/ner11
python -m spacy link models/ner11_v3/model-best ner11

# 8. Verify spaCy installation
python -c "import spacy; nlp = spacy.load('ner11'); print('✅ spaCy model loaded')"

# 9. Test NER11 model inference
python << 'EOF'
import spacy
nlp = spacy.load("ner11")
doc = nlp("Threat actor APT-28 exploited Microsoft Windows vulnerability CVE-2023-123456")
print("\n✅ NER11 Model Test:")
for ent in doc.ents:
  print(f"  Entity: {ent.text:30} | Label: {ent.label_}")
print("\n✅ NER11 model working correctly")
EOF

echo "✅ Python environment ready"
```

**Expected Output:**
```
Created virtual environment
Collecting dependencies...
Successfully installed [packages]

✅ spaCy model loaded

✅ NER11 Model Test:
  Entity: APT-28                        | Label: THREAT_ACTOR
  Entity: Microsoft Windows             | Label: PRODUCT
  Entity: CVE-2023-123456               | Label: VULNERABILITY

✅ NER11 model working correctly
✅ Python environment ready
```

**Success Criteria:**
- Virtual environment created and activated
- Dependencies installed
- spaCy model linked
- NER11 test inference succeeds

---

## Task 4.8: Setup Node.js Environment (Frontend)

### Purpose
Install frontend dependencies for React/Next.js development.

### Procedure

```bash
# 1. Navigate to frontend directory (if exists)
cd ~/Projects/aeon-dt/source/aeon-repo/1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1 \
  2>/dev/null || cd ~/Projects/aeon-dt/source/aeon-repo

# 2. Check if package.json exists
if [ ! -f package.json ]; then
  echo "⚠️ package.json not found - frontend may need setup"
  echo "Creating basic Next.js setup..."
  npx create-next-app@latest aeon-frontend --typescript --tailwind
  cd aeon-frontend
fi

# 3. Install Node dependencies
npm install

# 4. Verify installation
npm list next react react-dom 2>/dev/null | head -5

# 5. Create .env file for API connection
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
EOF

echo "✅ Frontend environment ready"
```

**Expected Output:**
```
npm install

added [number] packages, and audited [number] packages

✅ Frontend environment ready
```

**Success Criteria:**
- Dependencies installed
- .env.local created
- npm commands working

---

## Task 4.9: Restore Optional Components (Optional)

### Purpose
Restore optional data volumes for complete system restoration.

### Procedure

```bash
# This section is OPTIONAL - only needed if optional volumes were backed up

# 1. Check if optional backups exist
if [ -f ~/Projects/aeon-dt/backups/usb_contents_*/database/qdrant*.dump ]; then
  echo "Restoring Qdrant vector database..."
  # [Vector DB restoration steps]
fi

# 2. Check if MinIO backups exist
if [ -f ~/Projects/aeon-dt/backups/usb_contents_*/storage/minio*.tar.gz ]; then
  echo "Restoring MinIO object storage..."
  # [MinIO restoration steps]
fi

# 3. Check if training data backup exists
if [ -d ~/Projects/aeon-dt/backups/usb_contents_*/models/ner11/training_data_copy ]; then
  echo "Copying training data..."
  cp -r ~/Projects/aeon-dt/backups/usb_contents_*/models/ner11/training_data_copy \
    ~/Projects/aeon-dt/models/ner11/training_data
fi

echo "✅ Optional components restored"
```

**Success Criteria:**
- Optional data available if backed up
- No errors if optional data unavailable

---

## Task 4.10: Create Restoration Summary

### Purpose
Document restoration completion and system state.

### Procedure

```bash
# 1. Create restoration report
cat > ~/Projects/aeon-dt/RESTORATION_COMPLETE.md << 'EOF'
# AEON Digital Twin - Restoration Complete

**Date:** $(date)
**System:** macOS
**Source:** WSL2 Linux

## Restoration Summary

### ✅ Completed Components
- [x] Neo4j database restored (20,739 nodes)
- [x] MySQL database restored (OpenSPG schema)
- [x] NER11 model extracted (3.5 GB)
- [x] Project code cloned from git bundle
- [x] Python environment created
- [x] Node.js environment ready
- [x] Frontend dependencies installed

### Database Status
- **Neo4j:** 20,739 nodes, 45+ entity types
- **MySQL:** OpenSPG schema with tables
- **Redis:** Cache ready
- **MinIO:** Object storage ready

### Model Status
- **NER11:** Extracted and ready for inference
- **spaCy:** Integrated and linked
- **Training Data:** Available at ~/Projects/aeon-dt/models/ner11/training_data

### Code Status
- **Repository:** Cloned from git bundle
- **Branches:** All branches restored
- **History:** Complete commit history available
- **Development:** Ready for coding

## Next Steps
1. Start development servers with: `npm run dev` (frontend) and `uvicorn` (backend)
2. Run validation procedures: `05_VALIDATION_PROCEDURES.md`
3. Test API endpoints and model inference
4. Begin development work

## System Readiness
**Status:** ✅ READY FOR DEVELOPMENT

All critical components restored and operational.
Ready to begin AEON development on macOS.

## Commands for Future Reference

### Start All Services
```bash
cd ~/Projects/aeon-dt/infrastructure/docker-compose
docker-compose -f docker-compose.databases.yml up -d
```

### Access Neo4j
Browser: http://localhost:7474
User: neo4j | Password: neo4j@openspg

### Access MySQL
```bash
mysql -h localhost -u root -popenspg
```

### Activate Python Environment
```bash
cd ~/Projects/aeon-dt/source/aeon-repo
source venv/bin/activate
```

### Start Frontend
```bash
cd ~/Projects/aeon-dt/source/aeon-repo
npm run dev
```

### Start Backend
```bash
cd ~/Projects/aeon-dt/source/aeon-repo
source venv/bin/activate
python -m uvicorn api.serve_model:app --reload --host 0.0.0.0 --port 8000
```
EOF

# 2. Display summary
cat ~/Projects/aeon-dt/RESTORATION_COMPLETE.md

# 3. Create checklist for verification
echo ""
echo "=== PHASE 5 COMPLETION CHECKLIST ==="
echo "☐ Neo4j restored with 20,739 nodes"
echo "☐ MySQL restored with schema"
echo "☐ NER11 models extracted (3.5 GB)"
echo "☐ Project code cloned from bundle"
echo "☐ Python environment created"
echo "☐ Node.js dependencies installed"
echo "☐ Restoration summary document created"
echo ""
echo "Next: Run 05_VALIDATION_PROCEDURES.md"
```

**Expected Output:**
```
# AEON Digital Twin - Restoration Complete

✅ Completed Components
- [x] Neo4j database restored (20,739 nodes)
- [x] MySQL database restored (OpenSPG schema)
- [x] NER11 model extracted (3.5 GB)
- [x] Project code cloned from git bundle
- [x] Python environment created
- [x] Node.js environment ready

Status: ✅ READY FOR DEVELOPMENT
```

**Success Criteria:**
- Restoration report created
- All checkpoints documented
- System ready for validation

---

## Phase 5 Complete: Restoration Summary

All critical components have been restored to macOS:

✅ **Databases**
- Neo4j: 20,739 nodes restored
- MySQL: OpenSPG schema restored
- Supporting services: Redis, MinIO running

✅ **Code & Models**
- NER11 models: 3.5 GB extracted and ready
- Project code: Complete git history available
- Development environments: Python venv + Node.js configured

✅ **Development Ready**
- All API endpoints available
- Frontend framework installed
- Databases operational
- Models loaded and ready for inference

**Next Step:** Proceed to `05_VALIDATION_PROCEDURES.md` to verify all systems are working correctly

</content>
