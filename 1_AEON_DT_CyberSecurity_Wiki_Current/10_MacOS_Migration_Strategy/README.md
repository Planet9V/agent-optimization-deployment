# AEON Digital Twin - macOS Migration Strategy

**File:** README.md
**Created:** 2025-12-04 14:30:00 UTC
**Purpose:** Comprehensive guide to moving AEON project from WSL2 to macOS
**Status:** PLANNING & DOCUMENTATION COMPLETE - Ready for execution
**Total Duration:** 3-5 hours (6 phases)
**Risk Level:** LOW (with proper preparation)

---

## 📋 Quick Navigation

### For Quick Overview
👉 Start here: **[00_MIGRATION_MASTER_PLAN.md](00_MIGRATION_MASTER_PLAN_2025-12-04.md)** (5 min read)
- Executive summary
- Project inventory
- Strategy selection
- Phase overview

### For Step-by-Step Execution
Follow these guides in order:

1. **[01_PRE_MIGRATION_CHECKLIST.md](01_PRE_MIGRATION_CHECKLIST.md)** (30-45 min)
   - Verify WSL2 system is ready
   - Identify blocking issues
   - Prepare USB drive

2. **[02_DATA_EXPORT_PROCEDURES.md](02_DATA_EXPORT_PROCEDURES.md)** (45-90 min)
   - Export Neo4j database
   - Export MySQL database
   - Copy NER11 models
   - Create Git bundle

3. **[03_MAC_SETUP_GUIDE.md](03_MAC_SETUP_GUIDE.md)** (2-3 hours)
   - Install development tools
   - Configure Docker
   - Prepare environment
   - Mount and verify USB

4. **[04_DATA_RESTORATION_GUIDE.md](04_DATA_RESTORATION_GUIDE.md)** (60-90 min)
   - Start database services
   - Restore Neo4j data
   - Restore MySQL data
   - Extract models and code

5. **[05_VALIDATION_PROCEDURES.md](05_VALIDATION_PROCEDURES.md)** (45-60 min)
   - Validate all databases
   - Test models
   - Test APIs
   - Sign-off

---

## 🎯 Project Overview

### Current Status
- **Location:** WSL2 Linux
- **Size:** 12+ GB (4.5 GB critical)
- **Complexity:** Medium-High
- **Data:** 251+ API endpoints, 20,739 Neo4j nodes, 3.5 GB models

### Target Status
- **Location:** macOS
- **Approach:** Hybrid (Code via Git, Data via USB)
- **Timeline:** 3-5 hours
- **Risk:** LOW (comprehensive backup strategy)

### Success Criteria
✅ All code transferred with complete history
✅ All databases restored (20,739 nodes intact)
✅ NER11 models extracted and operational
✅ All 251+ API endpoints functional
✅ Zero data loss or corruption
✅ Development environment ready

---

## 📦 What's Being Transferred

### Critical Components (Must Transfer: 4.5 GB)

| Component | Size | Type | Status |
|-----------|------|------|--------|
| NER11 Models | 976 MB | ML Models | ✅ In archive |
| Training Data | 2.1 GB | Datasets | ✅ Available |
| Neo4j Backup | ~500 MB | Database | ✅ Can dump |
| MySQL Backup | ~50 MB | Database | ✅ Can backup |
| Git Code | ~100 MB | Source | ✅ In GitHub |

### Optional Components (Nice to Have: 400 MB)
- Qdrant vector database
- MinIO object storage
- Redis cache (can rebuild)

### Regenerable (Skip: 3.3 GB)
- node_modules
- Build artifacts
- Caches and temp files

---

## 🚀 Phase Overview

### Phase 1: Planning & Preparation (30-45 min)
**Objective:** Verify system ready, identify blocking issues
- Run pre-migration checklist
- Resolve blocking issues (uncommitted files, etc.)
- Prepare USB drive
**Success:** All checklist items passed

### Phase 2: Data Collection & Export (45-90 min)
**Objective:** Export all critical data to USB
- Dump Neo4j database
- Backup MySQL schema
- Copy NER11 models and training data
- Create Git bundle
- Verify checksums
**Success:** All exports verified and checksummed

### Phase 3 & 4: macOS Environment Setup (2-3 hours)
**Objective:** Prepare macOS for data restoration
- Install Homebrew, Docker, Python, Node.js
- Configure Docker for database services
- Create project directory structure
- Mount and verify USB drive
**Success:** All tools installed and verified

### Phase 5: Data Restoration (60-90 min)
**Objective:** Restore all data to macOS
- Start database containers
- Load Neo4j backup
- Restore MySQL database
- Extract NER11 models
- Clone project code from Git bundle
- Configure development environments
**Success:** All data restored and accessible

### Phase 6: Validation (45-60 min)
**Objective:** Verify all systems operational
- Test database connectivity
- Validate NER11 model inference
- Test API endpoints
- Build and test frontend
- Confirm data integrity
- Generate sign-off
**Success:** All systems validated, ready for development

---

## ⚠️ Critical Prerequisites

### Before Starting
✅ WSL2 system must be operational
✅ Docker containers must be healthy (all 9 running)
✅ USB drive must have 8+ GB free space
✅ All recent code must be git-committed (20 uncommitted files blocking)
✅ NER11 archive must be intact (tar integrity verified)

### Blocking Issues (Must Resolve First)
❌ **20 uncommitted files** - E10/E11/E12 APIs not in git → Must commit
❌ **Corrupted archive** - NER11_Gold_Model.tar.gz unreadable → Must fix
❌ **Unhealthy containers** - Neo4j/MySQL down → Must restart
❌ **Insufficient USB** - Less than 8 GB free → Must use larger drive

**Reference:** See `01_PRE_MIGRATION_CHECKLIST.md` for detailed blocking issue resolution

---

## 🛠️ Tools Required

### On WSL2 (for export)
- Docker (already running)
- Bash/Terminal
- Git
- tar/gzip utilities
- USB mount support

### On macOS (for setup & restoration)
- **Homebrew** - Package manager (install first)
- **Docker Desktop** - Container runtime
- **Python 3.10+** - NER11 model and API
- **Node.js 18+** - Frontend development
- **Git 2.x** - Version control
- **VSCode/IDE** - Code editor (optional)

---

## 📊 Migration Strategy Comparison

### Considered Approaches

**Option A: Full Disk Clone** ❌
- Pro: Fastest, complete copy
- Con: Disrupts WSL2, large data (10+ GB to USB)
- Verdict: Too risky for active development

**Option B: Everything to GitHub** ⚠️
- Pro: No USB needed
- Con: 3.5 GB models exceed GitHub limits
- Verdict: Not viable for large files

**Option C: Hybrid (Code via Git, Data via USB)** ✅ **SELECTED**
- Pro: Code tracked, data intact, preserves WSL2
- Con: Multi-step process
- Verdict: Best balance of safety and completeness

**Option D: Docker Image Export** ❌
- Pro: Preserves exact state
- Con: Very large, complex to setup on Mac
- Verdict: Overcomplicated

### Selected Approach: Hybrid Option C
- **Code:** Git bundle (complete history)
- **Data:** USB drive (all databases, models, configs)
- **Workflow:** No WSL2 disruption, parallel setup possible

---

## 📈 Time Breakdown

| Phase | Duration | Main Tasks |
|-------|----------|-----------|
| 1. Planning | 30-45 min | Pre-flight checklist, issue resolution |
| 2. Export | 45-90 min | Database dumps, model copy, Git bundle |
| 3 & 4. Setup | 2-3 hours | Tool installation, environment prep |
| 5. Restoration | 60-90 min | Data loading, code cloning, config |
| 6. Validation | 45-60 min | Testing, verification, sign-off |
| **Total** | **3-5 hours** | **Complete migration** |

*Times vary based on system speed and file sizes*

---

## 🔒 Safety & Data Protection

### Backup Strategy
✅ **Multiple backups:** USB, local copy, GitHub repository
✅ **Checksums verified:** SHA256 for integrity confirmation
✅ **No data loss:** All files copied, none deleted
✅ **Rollback possible:** WSL2 remains intact until migration verified

### Risk Mitigation
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| USB corruption | Low | High | Checksum verification |
| Database inconsistency | Very Low | Medium | Offline backup, transactions |
| Model extraction failure | Very Low | Medium | Archive integrity verified |
| WSL2 disruption | Very Low | Medium | No deletion, export only |
| Missing dependencies | Low | Low | Comprehensive tool setup |

---

## 💾 Data Inventory

### Git-Tracked Files (9.7%)
- Source code: 172 base endpoints + 79 new endpoints
- Frontend application
- Configuration files
- Documentation
- **Location:** GitHub repository + USB bundle

### Non-Tracked Critical Files (4.5 GB)
- **NER11 Models:** 976 MB (not in git - too large)
- **Training Data:** 2.1 GB (not in git)
- **Neo4j Data:** 20,739 nodes, relationships
- **MySQL Schema:** OpenSPG configuration
- **Location:** Exported to USB via Docker volume dumps

### Non-Tracked Regenerable (3.3 GB)
- node_modules: 894 MB
- Build artifacts: 100+ MB
- Caches: 200+ MB
- Temp files: 54 MB
- **Action:** Skip during migration, regenerate on macOS

---

## 📝 Before You Start

### Preparation Checklist

**Step 1: Read Master Plan (5 min)**
- [ ] Understand overall strategy
- [ ] Review timeline and phases
- [ ] Note potential blockers

**Step 2: Verify Prerequisites (10 min)**
- [ ] WSL2 system is healthy
- [ ] Docker containers running
- [ ] USB drive available (8+ GB)
- [ ] Git status clean OR plan commits

**Step 3: Review Blocking Issues (5 min)**
- [ ] Check 01_PRE_MIGRATION_CHECKLIST.md
- [ ] Resolve any blocking items
- [ ] Verify USB and container health

**Step 4: Plan Timing (5 min)**
- [ ] Block 3-5 hours for migration
- [ ] Ensure uninterrupted time for Phase 2-6
- [ ] Have macOS ready for Phase 3

**Step 5: Begin Migration (When ready)**
- [ ] Start with Phase 1: PRE_MIGRATION_CHECKLIST.md
- [ ] Follow guides sequentially
- [ ] Complete each phase before next

---

## 🎓 Key Concepts

### Why USB Instead of Just Using GitHub?
- NER11 models: 3.5 GB (GitHub limit is 100 MB per file)
- Training data: 2.1 GB (no versioning needed)
- Database: 500+ MB (binary format, not text)
- **Solution:** USB drive can handle large files, GitHub handles code

### Why Neo4j Backup Instead of Live Transfer?
- **Consistency:** Offline backup ensures no mid-transfer changes
- **Performance:** Dump once, restore multiple times if needed
- **Simplicity:** Binary format, direct restoration via neo4j-admin
- **Safety:** Can restart Neo4j without data loss risk

### Why Virtual Environment for Python?
- **Isolation:** Project dependencies don't conflict with system
- **Reproducibility:** Can recreate exact environment
- **Safety:** System Python untouched
- **Portability:** Easy to move between machines

---

## 🆘 Troubleshooting Quick Links

### Common Issues

**"20 uncommitted files blocking migration"**
→ See: 01_PRE_MIGRATION_CHECKLIST.md, Section "Git Cleanup - BLOCKING ISSUE"

**"NER11 archive corrupted"**
→ See: 01_PRE_MIGRATION_CHECKLIST.md, Task 1.2 "NER11 Archive Verification"

**"Docker containers unhealthy"**
→ See: 01_PRE_MIGRATION_CHECKLIST.md, Task 1.3 "Docker System Status"

**"USB not mounting on macOS"**
→ See: 03_MAC_SETUP_GUIDE.md, Task 3.7 "Mount USB Drive"

**"Neo4j won't load backup"**
→ See: 04_DATA_RESTORATION_GUIDE.md, Task 4.3 "Neo4j Restoration"

**"API endpoints not responding"**
→ See: 05_VALIDATION_PROCEDURES.md, Task 6.3 "API Validation"

---

## 📞 Support Resources

### Documentation Files (In Order)
1. **00_MIGRATION_MASTER_PLAN.md** - Strategy & overview
2. **01_PRE_MIGRATION_CHECKLIST.md** - Pre-flight verification
3. **02_DATA_EXPORT_PROCEDURES.md** - Data extraction
4. **03_MAC_SETUP_GUIDE.md** - Environment setup
5. **04_DATA_RESTORATION_GUIDE.md** - Data loading
6. **05_VALIDATION_PROCEDURES.md** - Verification & sign-off

### Key Commands

```bash
# WSL2: Verify system ready
git status && docker ps && df /mnt/e

# WSL2: Export data to USB
cd ~/Projects && tar -tzf 5_NER11_Gold_Model/NER11_Gold_Model.tar.gz > /dev/null

# macOS: Verify Docker ready
docker ps && docker network inspect openspg-network

# macOS: Start services
docker-compose -f ~/Projects/aeon-dt/infrastructure/docker-compose/docker-compose.databases.yml up -d

# macOS: Verify restoration
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "MATCH (n) RETURN COUNT(n)"
```

---

## ✅ Migration Checklist

### Phase 1: Planning
- [ ] Read 00_MIGRATION_MASTER_PLAN.md
- [ ] Run 01_PRE_MIGRATION_CHECKLIST.md
- [ ] Resolve blocking issues
- [ ] Commit all code to git
- [ ] Verify USB ready

### Phase 2: Export
- [ ] Export Neo4j (500 MB)
- [ ] Export MySQL (50 MB)
- [ ] Copy NER11 archive (439 MB)
- [ ] Create Git bundle (100 MB)
- [ ] Verify all checksums
- [ ] USB ready (5.5 GB used, space verified)

### Phase 3 & 4: Setup
- [ ] Homebrew installed
- [ ] Docker Desktop installed
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Git configured
- [ ] Project directories created
- [ ] USB mounted and verified

### Phase 5: Restoration
- [ ] Database services started
- [ ] Neo4j backup loaded (20,739 nodes)
- [ ] MySQL backup restored
- [ ] NER11 extracted (3.5 GB)
- [ ] Git repo cloned
- [ ] Python environment ready
- [ ] Frontend dependencies installed

### Phase 6: Validation
- [ ] Databases responding
- [ ] NER11 model loads
- [ ] API health checks pass
- [ ] Frontend builds successfully
- [ ] All checksums verified
- [ ] Sign-off approved

---

## 🎉 You're Ready!

This comprehensive migration strategy provides:
✅ **Clear roadmap:** 6 phases, detailed procedures
✅ **Risk mitigation:** Multiple backups, checksums, validation
✅ **Complete documentation:** Step-by-step guides
✅ **Troubleshooting:** Common issues and solutions
✅ **Safety:** No WSL2 disruption, data integrity verified

**Next Step:** Open [01_PRE_MIGRATION_CHECKLIST.md](01_PRE_MIGRATION_CHECKLIST.md) and begin Phase 1

---

**Created:** 2025-12-04
**Status:** Planning & Documentation Complete
**Ready for:** Immediate execution (when WSL2 blocking issues resolved)

---

*For questions or issues, refer to the specific phase guide or review troubleshooting sections.*

</content>
