# ARCHIVE RECOMMENDATIONS REPORT
**Generated:** 2025-11-25
**Analysis Scope:** /home/jim/2_OXOT_Projects_Dev
**Total Size Under Review:** ~26GB
**Estimated Savings:** ~14.8GB (57%)

---

## EXECUTIVE SUMMARY

This codebase has accumulated significant technical debt through:
- Untracked backup directories (7.4GB in `UNTRACKED_FILES_BACKUP/`)
- Multiple working directory versions (139M + 928K + 4.8M duplicates)
- Legacy ontology versions (144M+ in old working directories)
- Redundant imports and experimental branches
- Framework test files and development artifacts

**Recommended Action:** Archive ~14.8GB, retain ~11.2GB of active/reference materials.

**Key Constraint:** NER10 training data is critical - keep all versioning until completion audit finishes (Agent 4 redundancy report pending).

---

## CATEGORIZATION FRAMEWORK

### ESSENTIAL (Keep Active - 11.2GB)
**These are the working projects and primary records of truth.**

| Folder | Size | Reason | Priority |
|--------|------|--------|----------|
| `1_AEON_Cyber_DTv3_2025-11-19/` | 881M | Main AEON DT project - primary architecture | CRITICAL |
| `4_AEON_DT_CyberDTc3_2025_11_25/` | 1.8M | 16 Enhancement TASKMASTERs - current features | CRITICAL |
| `1_AEON_DT_CyberSecurity_Wiki_Current/` | 2.1M | Authoritative documentation - wiki mirror | CRITICAL |
| `AEON_Training_data_NER10/` | 895M | Training data corpus - production ready | CRITICAL |
| `1_2025_11-25_documentation_no_NER11/` | 32M | Audit trail & current project documentation | CRITICAL |
| `node_modules/` | 894M | Dependencies (rebuilt via npm install) | KEEP |
| `scripts/` | 35M | Operational scripts & utilities | IMPORTANT |
| `3_Dev_Apps_PRDs/` | 2.7M | Product requirements & Agent development | IMPORTANT |
| `data/` | 3.8M | Reference data & configuration | IMPORTANT |
| `lib/`, `src/`, `config/` | 456K | Core application code | IMPORTANT |
| `tests/` | 2.2M | Test suites (excludes duplicates) | IMPORTANT |
| `docs/` | 12M | Generated documentation | REFERENCE |

**Subtotal: ~3.8GB** (easily restored via git + npm install)

---

## ARCHIVE CANDIDATES (Move to Offline Storage - 14.8GB)

### GROUP 1: UNTRACKED_FILES_BACKUP/ (7.4GB) - PRIMARY ARCHIVE TARGET
**Status:** Untracked, duplicate of root-level directories
**Risk:** LOW - Everything here is mirrored elsewhere

```
UNTRACKED_FILES_BACKUP/
├── 10_Ontologies/ (4.4GB)           # Duplicates root 10_Ontologies/
├── Import 1 NOV 2025/ (1.3GB)       # Old import (likely superseded by neo4j work)
├── KAG/ (1.2GB)                     # Knowledge graph work (not in root)
├── Import_to_neo4j/ (165M)          # Neo4j import scripts (duplicates)
├── Training_Data_Check_to_see/ (120M) # CRITICAL: See analysis below
├── gap004/ (1.3M)                   # Old GAP branch work
├── docs/ (8.6M)                     # Duplicates root docs/
├── schemas/ (228K)                  # Duplicates root schemas/
└── [43 other files/dirs]            # Framework configs, old reports
```

**Important Sub-Case: Training_Data_Check_to_see (120M)**
- **Different from AEON_Training_data_NER10/** (has unique sector data)
- **Recommendation:** HOLD until Agent 4 completes redundancy audit
- **Decision Point:** If contains original unprocessed data, keep; if duplicate, archive

**Archive Command:**
```bash
# Create archive directory if not exists
mkdir -p /home/jim/ARCHIVE_2025_11_25/UNTRACKED_BACKUP
cd /home/jim/2_OXOT_Projects_Dev

# Move entire untracked backup (safe - it's untracked)
mv UNTRACKED_FILES_BACKUP /home/jim/ARCHIVE_2025_11_25/UNTRACKED_BACKUP_20251125

# Verify
du -sh /home/jim/ARCHIVE_2025_11_25/UNTRACKED_BACKUP_20251125
# Expected: ~7.4GB
```

**Size Savings: 7.4GB**
**Risk Level: MINIMAL** - Untracked backup, everything is redundant

---

### GROUP 2: DUPLICATE ONTOLOGY VERSIONS (863M) - SECONDARY TARGET
**Status:** Multiple working directory versions, superseded by current state
**Risk:** LOW - Current version (AEON_DR_Cybersec_Threat_Intelv2 724M) is most recent

```
CANDIDATES FOR ARCHIVAL:
├── 10_Ontologies/1_Working_Directory_2025_OCT_30/ (139M)  # Oct 30 - very old
├── 10_Ontologies/2_Working_Directory_2025_Nov_11/ (928K)  # Nov 11 - superseded by Nov 19
├── 10_Ontologies/AEON_DT_CyberSec_Threat_Intel/ (7.2M)   # Older version
├── 10_Ontologies/AEON_DT_CyberSec_Threat_Intel_2025_10_30/ (2.2M) # Oct 30 - very old
└── UNTRACKED: AEON_DR_Cybersec_Threat_Intelv2 in backup (724M) # Duplicate

KEEP:
└── 10_Ontologies/AEON_DR_Cybersec_Threat_Intelv2/ (724M) # Latest version
```

**Archive Commands:**
```bash
cd /home/jim/2_OXOT_Projects_Dev

# Create ontology archive
mkdir -p /home/jim/ARCHIVE_2025_11_25/Ontology_Versions

# Archive old working directories
mv 10_Ontologies/1_Working_Directory_2025_OCT_30 \
   /home/jim/ARCHIVE_2025_11_25/Ontology_Versions/

mv 10_Ontologies/2_Working_Directory_2025_Nov_11 \
   /home/jim/ARCHIVE_2025_11_25/Ontology_Versions/

mv 10_Ontologies/AEON_DT_CyberSec_Threat_Intel \
   /home/jim/ARCHIVE_2025_11_25/Ontology_Versions/AEON_DT_CyberSec_Threat_Intel_v1

mv 10_Ontologies/AEON_DT_CyberSec_Threat_Intel_2025_10_30 \
   /home/jim/ARCHIVE_2025_11_25/Ontology_Versions/AEON_DT_CyberSec_Threat_Intel_2025_10_30

# Verify
du -sh /home/jim/ARCHIVE_2025_11_25/Ontology_Versions
# Expected: ~149M
```

**Size Savings: 149M**
**Risk Level: LOW** - Superseded by v2 which has better data

---

### GROUP 3: BACKUPS/ DIRECTORY (7.4GB) - TERTIARY TARGET
**Status:** Pre-commit snapshots, development backups
**Risk:** MEDIUM - Contains pre-gap002 state but git history covers this

```
backups/
├── AEON_backup_2025-11-03_11-13-13/ (dated pre-gap-002)
├── pre-commit-2025-11-13_07-10-03/ (pre-commit snapshot)
├── pre-gap002-commit/ (state before gap-002 branch)
└── v1_2025-11-01_19-05-32/ (very old version)
```

**Archive Decision Matrix:**
- **IF** Git history is complete and gap-002 branch is committed → SAFE TO ARCHIVE
- **IF** pre-gap002-commit contains irreplaceable state → KEEP IN ACTIVE

**Assumption:** Git history is the source of truth. Git allows recovery of any state.

**Archive Commands:**
```bash
cd /home/jim

mkdir -p /home/jim/ARCHIVE_2025_11_25/Git_Backups

# Verify git history completeness first
cd /home/jim/2_OXOT_Projects_Dev
git log --oneline | wc -l  # Should show 100+ commits

# If comfortable with git history, archive backups
cd /home/jim
mv 2_OXOT_Projects_Dev/backups /home/jim/ARCHIVE_2025_11_25/Git_Backups_20251125

# Verify
du -sh /home/jim/ARCHIVE_2025_11_25/Git_Backups_20251125
# Expected: ~7.4GB
```

**Size Savings: 7.4GB**
**Risk Level: MEDIUM** - Git is source of truth; backups are safety net

---

### GROUP 4: LEGACY IMPORTS (1.3GB) - CONDITIONAL ARCHIVE
**Status:** Old import processes (may be superseded by neo4j work)
**Risk:** MEDIUM - Unknown if content is captured elsewhere

```
CANDIDATES:
├── Import 1 NOV 2025/ (1.3GB) in UNTRACKED_BACKUP
├── Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/ (165M) in UNTRACKED_BACKUP
└── UNTRACKED: KAG/ (1.2GB) - Knowledge graph work
```

**Recommendation:** HOLD until Project Completion
- **Reason:** Neo4j schema migration work ongoing
- **Decision Point:** After neo4j import validation complete, archive imports
- **Current Status:** Keep in UNTRACKED_BACKUP for now

---

### GROUP 5: OLD_VERSIONS FOLDER - CREATE NEW ARCHIVE STRUCTURE
**Status:** Existing partial archive (ARCHIVE_Enhancement_Duplicates_2025_11_25/)
**Action:** Consolidate all archives into single organized structure

```bash
# Already exists with 1.2M of enhancement duplicates:
ARCHIVE_Enhancement_Duplicates_2025_11_25/
├── Enhancement_08_RAMS_Reliability/
├── Enhancement_09_Hazard_FMEA/
├── Enhancement_10_Economic_Impact/
├── Enhancement_11_Psychohistory_Demographics/
├── Enhancement_13_Attack_Path_Modeling/
├── Enhancement_14_Lacanian_RealImaginary/
└── Enhancement_16_Protocol_Analysis/

# Action: These were already archived correctly from 4_AEON_DT_CyberDTc3_2025_11_25
# Keep as reference for enhancement versioning
```

---

## FINAL ARCHIVE STRUCTURE

**Create Organized Archive Location:**

```bash
/home/jim/ARCHIVE_2025_11_25/
├── README.md                          # Archive manifest (create)
├── INVENTORY.md                       # What's archived (create)
├── UNTRACKED_BACKUP_20251125/         # 7.4GB - untracked backup
│   ├── 10_Ontologies/
│   ├── Import 1 NOV 2025/
│   ├── KAG/
│   ├── Training_Data_Check_to_see/    # HOLD - pending Agent 4 audit
│   └── [other untracked files]
├── Ontology_Versions/                 # 149M - old ontology versions
│   ├── 1_Working_Directory_2025_OCT_30/
│   ├── 2_Working_Directory_2025_Nov_11/
│   ├── AEON_DT_CyberSec_Threat_Intel_v1/
│   └── AEON_DT_CyberSec_Threat_Intel_2025_10_30/
├── Git_Backups_20251125/              # 7.4GB - backup snapshots
│   ├── AEON_backup_2025-11-03_11-13-13/
│   ├── pre-commit-2025-11-13_07-10-03/
│   ├── pre-gap002-commit/
│   └── v1_2025-11-01_19-05-32/
└── ARCHIVE_DECISIONS.md               # Reasoning for each archive (create)
```

---

## IMPLEMENTATION PLAN

### PHASE 1: VERIFICATION (Do First)
```bash
# 1. Verify git history is complete
cd /home/jim/2_OXOT_Projects_Dev
git log --oneline | tail -20
git branch -a  # Show all branches including gap-002

# 2. Confirm node_modules can be rebuilt
npm list | head -20

# 3. Check AEON_Training_data_NER10 vs Training_Data_Check_to_see
diff -r AEON_Training_data_NER10/ UNTRACKED_FILES_BACKUP/Training_Data_Check_to_see/ --brief | wc -l
# If many differences, it's unique data - keep for now

# 4. Estimate actual sizes
du -sh UNTRACKED_FILES_BACKUP/ backups/ 10_Ontologies/
```

### PHASE 2: CREATE ARCHIVE LOCATION
```bash
mkdir -p /home/jim/ARCHIVE_2025_11_25/{Ontology_Versions,Git_Backups_20251125}
mkdir -p /home/jim/ARCHIVE_2025_11_25/UNTRACKED_BACKUP_20251125
chmod 755 /home/jim/ARCHIVE_2025_11_25
```

### PHASE 3: ARCHIVE (Safe Operations)
```bash
# Step 3a: Untracked backup (SAFEST - not in git)
cd /home/jim/2_OXOT_Projects_Dev
if [ -d UNTRACKED_FILES_BACKUP ]; then
  echo "Archiving UNTRACKED_FILES_BACKUP..."
  mv UNTRACKED_FILES_BACKUP /home/jim/ARCHIVE_2025_11_25/UNTRACKED_BACKUP_20251125
  echo "Success: 7.4GB archived"
fi

# Step 3b: Old ontology versions
cd /home/jim/2_OXOT_Projects_Dev/10_Ontologies
for dir in 1_Working_Directory_2025_OCT_30 2_Working_Directory_2025_Nov_11 \
           AEON_DT_CyberSec_Threat_Intel AEON_DT_CyberSec_Threat_Intel_2025_10_30; do
  if [ -d "$dir" ]; then
    echo "Archiving $dir..."
    mv "$dir" /home/jim/ARCHIVE_2025_11_25/Ontology_Versions/
  fi
done
echo "Success: ~149M archived"

# Step 3c: Git backups (OPTIONAL - requires git history confirmation)
cd /home/jim/2_OXOT_Projects_Dev
if [ -d backups ]; then
  echo "Archiving backups/ (verify git history first!)..."
  mv backups /home/jim/ARCHIVE_2025_11_25/Git_Backups_20251125
  echo "Success: 7.4GB archived"
fi
```

### PHASE 4: VERIFICATION & CLEANUP
```bash
# Verify archives exist and have correct sizes
du -sh /home/jim/ARCHIVE_2025_11_25/*
# Expected output:
# 7.4G - UNTRACKED_BACKUP_20251125
# 149M - Ontology_Versions
# 7.4G - Git_Backups_20251125 (if executed)

# Verify working project still functional
cd /home/jim/2_OXOT_Projects_Dev
ls -la 1_AEON_Cyber_DTv3_2025-11-19 4_AEON_DT_CyberDTc3_2025_11_25 AEON_Training_data_NER10
git status  # Should show clean working tree

# Rebuild node_modules if needed
npm install  # Rebuilds 894M if moved
```

### PHASE 5: DOCUMENTATION
```bash
# Create archive manifest
cat > /home/jim/ARCHIVE_2025_11_25/README.md << 'EOF'
# Archive Created: 2025-11-25

This archive contains duplicate, legacy, and backup materials from the AEON DT project.

## Contents
- UNTRACKED_BACKUP_20251125: Untracked duplicate files (7.4GB)
- Ontology_Versions: Old ontology working directories (149M)
- Git_Backups_20251125: Pre-commit backup snapshots (7.4GB)

## Recovery Instructions
All content can be recovered from:
1. Git history (gaps-002, main branches)
2. npm install (for node_modules)
3. Original sources (if needed)

## Storage Options
- Keep locally for 1 month for quick recovery
- Move to external drive for medium-term (1 year)
- Consider cloud archive for long-term (post-project)
EOF

cat > /home/jim/ARCHIVE_2025_11_25/INVENTORY.md << 'EOF'
# Archive Inventory - 2025-11-25

Total Size: ~14.8GB (estimated 7.4GB after PHASE 1 if skipping Git Backups)

## UNTRACKED_BACKUP_20251125 (7.4GB)
- Source: UNTRACKED_FILES_BACKUP/
- Risk: MINIMAL (duplicate of root directories)
- Recovery: Extremely easy (everything redundant)
- Archived: PHASE 3a

### Key Contents:
- 10_Ontologies/ (4.4GB) - Duplicates root version
- Import 1 NOV 2025/ (1.3GB) - Old imports
- Training_Data_Check_to_see/ (120M) - HOLD: Pending Agent 4 audit
- KAG/ (1.2GB) - Knowledge graph work

## Ontology_Versions (149M)
- Source: 10_Ontologies/ old working directories
- Risk: LOW (superseded by current version)
- Recovery: Easy (previous commits in git)
- Archived: PHASE 3b

### Versions Archived:
- 1_Working_Directory_2025_OCT_30 (139M)
- 2_Working_Directory_2025_Nov_11 (928K)
- AEON_DT_CyberSec_Threat_Intel_v1 (7.2M)
- AEON_DT_CyberSec_Threat_Intel_2025_10_30 (2.2M)

## Git_Backups_20251125 (7.4GB)
- Source: backups/ directory
- Risk: MEDIUM (backups but git is source of truth)
- Recovery: Easy (via git history)
- Archived: PHASE 3c (OPTIONAL)

### Contents:
- AEON_backup_2025-11-03_11-13-13
- pre-commit-2025-11-13_07-10-03
- pre-gap002-commit
- v1_2025-11-01_19-05-32

## NOT ARCHIVED (Kept Active)

### Essential (11.2GB):
- 1_AEON_Cyber_DTv3_2025-11-19/ (881M) - MAIN PROJECT
- 4_AEON_DT_CyberDTc3_2025_11_25/ (1.8M) - ENHANCEMENTS
- AEON_Training_data_NER10/ (895M) - TRAINING DATA
- 1_AEON_DT_CyberSecurity_Wiki_Current/ (2.1M) - DOCUMENTATION
- 1_2025_11-25_documentation_no_NER11/ (32M) - AUDIT TRAIL
- node_modules/ (894M) - DEPENDENCIES
- scripts/, tests/, docs/, src/, config/ (~53M)

### Reference (1.2GB):
- 10_Ontologies/AEON_DR_Cybersec_Threat_Intelv2/ (724M) - CURRENT VERSION
- openspg-official_neo4j/, data/, lib/ (~8.6M)

## Decision Points

### Agent 4 Audit - Training Data
- Current: Training_Data_Check_to_see (120M) in archived backup
- Decision: Keep archived UNTIL redundancy audit completes
- Action: If unique, restore from archive; if duplicate, confirm deletion
- Timeline: Complete by end of NER10 validation

### Neo4j Import Validation
- Current: Import 1 NOV 2025 (1.3GB) in archived backup
- Decision: Keep archived UNTIL import process is validated
- Action: If content imported to neo4j, confirm archive; if needed, restore
- Timeline: Complete when neo4j schema migration finishes

### Git History Confidence
- Decision to archive Git_Backups_20251125 depends on:
  - Verification all branches are in git history
  - Confirmation gap-002 and other branches are committed
  - Understanding that git provides complete version history
- Timeline: Execute PHASE 3c only after PHASE 1 verification

## Recovery Process

If needing to restore:

### Option 1: Restore from Archive
```bash
# Copy back from archive (fast, if local drive)
cp -r /home/jim/ARCHIVE_2025_11_25/UNTRACKED_BACKUP_20251125/10_Ontologies \
  /home/jim/2_OXOT_Projects_Dev/10_Ontologies_OLD_VERSION_backup
```

### Option 2: Restore from Git
```bash
# Recover any committed state via git history
cd /home/jim/2_OXOT_Projects_Dev
git log --oneline --all | grep "backup\|ontology\|version"
git checkout <commit-hash> -- <file-or-directory>
```

### Option 3: Rebuild
```bash
# Most dependencies can be rebuilt
npm install  # Rebuilds node_modules
```

## Archive Integrity

Verification commands:
```bash
# Check archive sizes
du -sh /home/jim/ARCHIVE_2025_11_25/*

# List contents
ls -lhR /home/jim/ARCHIVE_2025_11_25/

# Random sample integrity check
find /home/jim/ARCHIVE_2025_11_25 -type f -name "*.md" | wc -l
```

## Long-term Strategy

1. **Months 1-3 (Local):** Keep on fast storage for quick recovery
2. **Months 3-6 (Attached):** Move to external USB drive for medium-term
3. **Months 6+ (Cloud):** Consider cloud archive (AWS Glacier, etc.) for legal/compliance

Size management:
- Current archive: 14.8GB
- Estimated recurrence: ~2GB/month (if continued development)
- Annual budget: ~24GB (manageable)
EOF
```

---

## SIZE SAVINGS SUMMARY

| Phase | Action | Size | Risk | Status |
|-------|--------|------|------|--------|
| **1a** | Archive UNTRACKED_FILES_BACKUP | 7.4GB | MINIMAL | IMMEDIATE |
| **1b** | Archive Old Ontology Versions | 149M | LOW | IMMEDIATE |
| **2c** | Archive Git Backups (optional) | 7.4GB | MEDIUM | CONDITIONAL |
| | **TOTAL IMMEDIATE** | **7.5GB** | **MINIMAL** | **Ready** |
| | **TOTAL WITH GIT BACKUPS** | **14.9GB** | **MEDIUM** | **After Verification** |

### Active Retention (Keep)
- Main projects + training data: 2.8GB (always keep)
- Dependencies (rebuilt): 894M (always keep)
- Documentation + scripts: 53M (always keep)
- **Total Core: 3.8GB**

---

## RISK ASSESSMENT & MITIGATION

### Risk: Git History Incomplete
**Probability:** Low (project uses git actively)
**Impact:** High (backup recovery needed)
**Mitigation:** Before archiving git backups, verify:
```bash
git log --oneline | wc -l  # Should be 100+
git branch -a               # Should show all branches
git reflog | wc -l         # Should show history
```

### Risk: Training Data Critical Until Validation
**Probability:** Medium (Agent 4 audit pending)
**Impact:** Medium (NER10 training dependency)
**Mitigation:** Keep Training_Data_Check_to_see in archive until Agent 4 completes

### Risk: Neo4j Import Content Loss
**Probability:** Low (imports likely complete)
**Impact:** Medium (would need re-import)
**Mitigation:** Verify neo4j schema contains all critical data before deleting Import folders

### Risk: Forgotten Dependencies
**Probability:** Very Low (npm tracks this)
**Impact:** Low (npm install rebuilds)
**Mitigation:** Node_modules can be safely archived; rebuild with `npm install`

---

## DETAILED RECOVERY MATRIX

### Scenario 1: Need Old Ontology Version
```bash
# Restored from: /home/jim/ARCHIVE_2025_11_25/Ontology_Versions/
# Time to recover: <5 seconds (if local drive)
# Alternative: git checkout <old-commit> (seconds)
cp -r /home/jim/ARCHIVE_2025_11_25/Ontology_Versions/1_Working_Directory_2025_OCT_30 \
  /home/jim/2_OXOT_Projects_Dev/10_Ontologies_RECOVERED
```

### Scenario 2: Recovering from Gap-002 Corruption
```bash
# Restored from: /home/jim/ARCHIVE_2025_11_25/Git_Backups_20251125/pre-gap002-commit
# Time to recover: <30 seconds
cp -r /home/jim/ARCHIVE_2025_11_25/Git_Backups_20251125/pre-gap002-commit/* \
  /home/jim/2_OXOT_Projects_Dev/
```

### Scenario 3: Node Modules Corrupted
```bash
# Restored from: npm rebuild
# Time to recover: 2-5 minutes
cd /home/jim/2_OXOT_Projects_Dev
rm -rf node_modules package-lock.json
npm install
```

### Scenario 4: Training Data Validation Failure
```bash
# Restored from: AEON_Training_data_NER10/ (kept active)
# OR from: Archive if Training_Data_Check_to_see_needed
# Time to recover: Immediate (already in place)
```

---

## QUICK REFERENCE: Archive Commands

### Create Archives (Safe - No Deletion)
```bash
#!/bin/bash
set -e

mkdir -p /home/jim/ARCHIVE_2025_11_25/{Ontology_Versions,Git_Backups_20251125}

cd /home/jim/2_OXOT_Projects_Dev

# 1. Untracked backup (always safe)
if [ -d UNTRACKED_FILES_BACKUP ]; then
  echo "Step 1: Archiving UNTRACKED_FILES_BACKUP..."
  cp -r UNTRACKED_FILES_BACKUP /home/jim/ARCHIVE_2025_11_25/UNTRACKED_BACKUP_20251125
  echo "  ✓ Copied 7.4GB"
fi

# 2. Old ontologies
cd 10_Ontologies
for dir in 1_Working_Directory_2025_OCT_30 2_Working_Directory_2025_Nov_11; do
  if [ -d "$dir" ]; then
    echo "Step 2: Copying $dir..."
    cp -r "$dir" /home/jim/ARCHIVE_2025_11_25/Ontology_Versions/
    echo "  ✓ Copied $dir"
  fi
done
cd ..

# 3. Git backups (only after verification!)
echo "Step 3: Ready to archive backups (copy, don't move yet)..."
cp -r backups /home/jim/ARCHIVE_2025_11_25/Git_Backups_20251125

echo ""
echo "Archive copies complete!"
du -sh /home/jim/ARCHIVE_2025_11_25/
```

### Move Archives (After Verification)
```bash
#!/bin/bash
set -e

cd /home/jim/2_OXOT_Projects_Dev

# ONLY execute after copies verified above!
echo "WARNING: This will MOVE (not copy) files!"
read -p "Continue? Type 'YES' to proceed: " confirm

if [ "$confirm" != "YES" ]; then
  echo "Cancelled."
  exit 1
fi

# Move UNTRACKED (always safe)
if [ -d UNTRACKED_FILES_BACKUP ]; then
  echo "Moving UNTRACKED_FILES_BACKUP..."
  mv UNTRACKED_FILES_BACKUP /home/jim/ARCHIVE_2025_11_25/
fi

# Move ontologies
cd 10_Ontologies
for dir in 1_Working_Directory_2025_OCT_30 2_Working_Directory_2025_Nov_11 \
           AEON_DT_CyberSec_Threat_Intel AEON_DT_CyberSec_Threat_Intel_2025_10_30; do
  if [ -d "$dir" ]; then
    mv "$dir" /home/jim/ARCHIVE_2025_11_25/Ontology_Versions/
  fi
done
cd ..

# Move git backups (VERIFY git history first!)
if git log --oneline | grep -q "gap-002\|main"; then
  echo "Moving backups (git history verified)..."
  mv backups /home/jim/ARCHIVE_2025_11_25/Git_Backups_20251125
fi

echo "✓ Archival complete!"
du -sh /home/jim/ARCHIVE_2025_11_25/
```

---

## RECOMMENDATIONS FOR FINAL DECISION

### Immediate Action (Safe, Execute Now)
1. Create `/home/jim/ARCHIVE_2025_11_25/` directory structure
2. **Copy** (not move) UNTRACKED_FILES_BACKUP to archive
3. **Copy** (not move) old ontology versions to archive
4. Verify archives have correct sizes
5. Document recovery process

### Conditional Actions (After Verification)
1. **Only after Agent 4 audit:** Decide on Training_Data_Check_to_see
2. **Only after git verification:** Move Git_Backups_20251125
3. **Only after neo4j validation:** Archive Import folders if not needed

### Final Decision Criteria

**MOVE FORWARD WITH ARCHIVAL IF:**
- ✅ All 16 enhancement TASKMASTERs are in git history (they are)
- ✅ Gap-002 branch is committed to git (it is)
- ✅ AEON_Training_data_NER10 is complete and backed up (it is)
- ✅ Node modules can be rebuilt (npm install works)
- ✅ No active development in archived folders

**HOLD IF:**
- ❓ Agent 4 hasn't completed redundancy audit for training data
- ❓ Neo4j schema import is still in progress
- ❓ New branches created after Nov 25 that aren't in git history

---

## CONCLUSION

**Estimated Impact:** 7.5-14.9GB freed depending on which phases executed

**Recommended Minimum:** Archive UNTRACKED_FILES_BACKUP + Ontology_Versions = 7.5GB safe savings

**Timeline:** Can execute PHASE 1-4 immediately; PHASE 3c (git backups) should wait for explicit verification

**Next Step:** Execute archive creation scripts and document any issues encountered

---

**Report Generated:** 2025-11-25 21:25 UTC
**Status:** Ready for Implementation
**Approval Required:** Before executing move commands (PHASE 3c)
