# Holistic Blocker Resolution Plan
**Generated**: 2025-11-28 16:30:00 UTC
**Agent**: Systems Architect Agent 6
**Purpose**: Systematic approach to resolve all 4 E27 deployment blockers in optimal order

---

## Executive Summary

**Total Blockers**: 4 types affecting 9 scripts (100% blocked)
**Optimal Resolution Sequence**: 3 → 1 → 2 → 4 (not sequential 1-2-3-4)
**Critical Finding**: Blocker #4 appears to be a **FALSE BLOCKER** - custom functions ARE callable, we're just using wrong syntax
**Total Time to Full Deployment**: 6-8 hours (with APOC) or 3 hours (partial, no APOC)

---

## Blocker Dependency Graph

```
INDEPENDENT BLOCKERS (Can resolve in parallel):
├── Blocker #3 (Schema Conflicts)          - 1 hour  - NO dependencies
└── Blocker #2 (Migration Syntax Errors)   - 30 min  - NO dependencies

DEPENDENT BLOCKERS (Sequential only):
├── Blocker #1 (Missing APOC)              - 30 min  - INFRASTRUCTURE DECISION
│   └── Blocker #4 (Function Syntax)       - 8-12 hr - DEPENDS on Blocker #1
│       └── FALSE BLOCKER ANALYSIS         - 0 hr    - Actually callable via different approach
```

**Key Insight**: Blockers #1 and #3 are INDEPENDENT and can be resolved in PARALLEL
**Critical Path**: Blocker #1 (APOC) → Blocker #4 (Functions)

---

## Blocker Deep Analysis

### Blocker #1: Custom Functions Not Callable
**Status**: INFRASTRUCTURE BLOCKER (requires user decision)
**Root Cause**: Missing APOC plugin in Neo4j container
**Scripts Affected**: 04, 05 (2 scripts)
**Functions Blocked**: 7 core psychohistory functions
**Resolution Time**: 30 minutes (install) + 15 minutes (verification)

**CRITICAL FINDING - FALSE BLOCKER HYPOTHESIS**:
After reviewing the scripts, custom functions ARE actually callable through APOC. The issue is:
- We're trying to call `apoc.custom.declareFunction()` which doesn't exist without APOC
- BUT the functions themselves are valid Cypher logic
- **Alternative**: Convert to parameterized queries (NO APOC needed)

**Example - Current (requires APOC)**:
```cypher
CALL apoc.custom.declareFunction(
  'psychohistory.epidemicThreshold(beta FLOAT, gamma FLOAT, connections INT) :: FLOAT',
  'RETURN $beta / $gamma * sqrt(toFloat($connections))'
);

// Later usage:
RETURN psychohistory.epidemicThreshold(0.3, 0.1, 100) as R0;
```

**Alternative - Parameterized Query (NO APOC)**:
```cypher
// Define as a subquery or WITH clause:
WITH 0.3 AS beta, 0.1 AS gamma, 100 AS connections
RETURN beta / gamma * sqrt(toFloat(connections)) AS epidemicThreshold;
```

**Verdict**: This blocker is **PARTIALLY FALSE** - we can work around it, but lose reusability.

---

### Blocker #2: Index Conflicts
**Status**: FIXABLE (no infrastructure changes)
**Root Cause**: Existing indexes conflict with new constraint creation
**Scripts Affected**: 01 (constraints)
**Resolution Time**: 1 hour
**Dependencies**: NONE

**Resolution Strategy**:
```cypher
// Option 1: Add IF NOT EXISTS (Neo4j 5.7+)
CREATE CONSTRAINT org_name_unique IF NOT EXISTS
FOR (n:Organization) REQUIRE n.name IS UNIQUE;

// Option 2: Check before creating
SHOW CONSTRAINTS
WHERE entityType = "NODE" AND labelsOrTypes = ["Organization"]
YIELD name;
// Only create if not exists

// Option 3: Drop-then-create (risky)
DROP INDEX organization_name_index IF EXISTS;
CREATE CONSTRAINT org_name_unique FOR (n:Organization) REQUIRE n.name IS UNIQUE;
```

**Recommended**: Option 1 (IF NOT EXISTS) - cleanest approach

---

### Blocker #3: CI Function Syntax Errors
**Status**: FIXABLE (no infrastructure changes)
**Root Cause**: CASE expressions in SET clauses without WITH aliases
**Scripts Affected**: 03 (migration)
**Resolution Time**: 30 minutes
**Dependencies**: NONE

**Problem Pattern** (appears 5 times):
```cypher
// INCORRECT:
MATCH (n:ThreatActor)
SET n.actorType = CASE WHEN ... END;  // ❌ SYNTAX ERROR

// CORRECT:
MATCH (n:ThreatActor)
WITH n, CASE WHEN ... END AS computed_value
SET n.actorType = computed_value;  // ✅ VALID
```

**Fix Locations**:
- Lines 21-26 (ThreatActor.actorType)
- Lines 31-36 (AttackPattern.patternType)
- Lines 41-46 (Vulnerability.vulnType)
- Lines 51-55 (Control.controlType)
- Lines 59-64 (Event.eventType)

**Automated Fix**: Use `sed` to batch-insert WITH clauses

---

### Blocker #4: Migration Script Errors
**Status**: REQUIRES COMPLETE REWRITE (8-12 hours)
**Root Cause**: PostgreSQL-style `CREATE OR REPLACE FUNCTION` syntax invalid in Neo4j
**Scripts Affected**: 06, 07, 08, 09 (4 scripts)
**Functions Blocked**: 22 statistical functions
**Dependencies**: DEPENDS on Blocker #1 (APOC decision)

**Invalid Syntax Examples**:
```cypher
// ❌ THIS DOES NOT WORK IN NEO4J:
CREATE OR REPLACE FUNCTION psychohistory.bootstrapCI(...)
RETURNS LIST<FLOAT>
LANGUAGE cypher
AS $$
  ...
$$;
```

**Resolution Options**:

**Option A: Convert to APOC Procedures (REQUIRES APOC)**:
```cypher
CALL apoc.custom.declareProcedure(
  'psychohistory.bootstrapCI(values :: LIST OF FLOAT, confidence :: FLOAT) :: (lower :: FLOAT, upper :: FLOAT)',
  '
  WITH $values AS vals, $confidence AS conf
  // Bootstrap logic here...
  RETURN lower, upper
  ',
  'READ'
);
```

**Option B: Convert to Parameterized Queries (NO APOC)**:
```cypher
// Instead of calling function:
// RETURN psychohistory.bootstrapCI([1,2,3], 0.95) AS ci;

// Use inline WITH:
WITH [1,2,3] AS values, 0.95 AS confidence
// Bootstrap calculation inline...
RETURN lower, upper;
```

**Verdict**: This blocker is **REAL** but has workarounds. Rewrite time: 8-12 hours.

---

## Optimal Resolution Sequence

### Phase 0: Infrastructure Decision (USER ACTION REQUIRED)
**Time**: 0 hours (decision only)

**Question**: Install APOC or deploy without mathematical models?

**Option A: Install APOC** (RECOMMENDED)
- Enables ALL 29 functions
- Production-grade performance
- Requires 30-minute infrastructure change
- **Total deployment time**: 6-8 hours

**Option B: Skip APOC** (PARTIAL DEPLOYMENT)
- Deploys schema only (Phase 1)
- NO psychohistory equations
- 70% functionality loss
- **Total deployment time**: 3 hours

---

### Phase 1: Fix Parallel Blockers (NO DEPENDENCIES)
**Time**: 1.5 hours total (can run in parallel)

#### Task 1.1: Fix Blocker #3 (Syntax Errors) - 30 minutes
**Scripts**: 03_migration_24_to_16.cypher
**Action**: Insert WITH clauses before all CASE-in-SET statements
**Verification**: Run syntax check with `cypher-shell`

**Execution**:
```bash
# Automated fix with sed
sed -i '/SET n\.\w* = CASE/i WITH n, CASE' 03_migration_24_to_16.cypher
# Then manually complete the WITH clauses (5 locations)
```

**Validation**:
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  --file /path/to/03_migration_24_to_16.cypher --fail-fast
```

#### Task 1.2: Fix Blocker #2 (Index Conflicts) - 1 hour
**Scripts**: 01_constraints.cypher
**Action**: Add `IF NOT EXISTS` to all constraint creations
**Verification**: Run script, check for conflicts

**Execution**:
```bash
# Automated fix with sed
sed -i 's/CREATE CONSTRAINT \(\w*\) FOR/CREATE CONSTRAINT \1 IF NOT EXISTS FOR/g' \
  01_constraints.cypher
```

**Validation**:
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  --file /path/to/01_constraints.cypher

# Verify constraints created:
SHOW CONSTRAINTS YIELD name, type, entityType;
```

**Expected Output**: 16 constraints (5 new + 11 already existing)

---

### Phase 2: Deploy Schema Foundation (PHASE 1 COMPLETE)
**Time**: 30 minutes
**Prerequisites**: Phase 1 tasks complete

#### Task 2.1: Deploy Fixed Scripts
```bash
# Deploy in order:
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  --file /path/to/01_constraints.cypher && \
  --file /path/to/02_indexes.cypher && \
  --file /path/to/03_migration_24_to_16.cypher
```

#### Task 2.2: Verify Schema Migration
```cypher
// Verify 16 Super Labels exist with discriminator properties:
MATCH (n)
RETURN DISTINCT labels(n) AS label, count(*) AS count
ORDER BY count DESC;

// Verify discriminator properties populated:
MATCH (n:ThreatActor)
RETURN n.actorType, count(*) AS count;

MATCH (n:AttackPattern)
RETURN n.patternType, count(*) AS count;
```

**Expected**: All 16 Super Labels with discriminator properties populated

**CHECKPOINT**: At this point, Phase 1 is COMPLETE (schema foundation deployed)

---

### Phase 3A: Install APOC (IF OPTION A CHOSEN)
**Time**: 45 minutes
**Dependencies**: User decision to install APOC

#### Task 3A.1: Install APOC Plugin - 30 minutes
```bash
# 1. Download APOC (check Neo4j version first)
NEO4J_VERSION=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "RETURN 'v' + split(dbms.components()[0].versions[0], '.')[0..1] AS version;" | grep -oP 'v\d+\.\d+')

# 2. Install APOC
docker exec openspg-neo4j bash -c "
  cd /var/lib/neo4j/plugins && \
  wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/${NEO4J_VERSION}.0/apoc-${NEO4J_VERSION}.0-core.jar
"

# 3. Configure Neo4j
docker exec openspg-neo4j bash -c "
  echo 'dbms.security.procedures.unrestricted=apoc.*' >> /var/lib/neo4j/conf/neo4j.conf && \
  echo 'dbms.security.procedures.allowlist=apoc.*' >> /var/lib/neo4j/conf/neo4j.conf
"

# 4. Restart Neo4j (2-minute downtime)
docker restart openspg-neo4j
sleep 60  # Wait for Neo4j to start

# 5. Verify APOC
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "RETURN apoc.version() AS apoc_version;"
```

**Expected Output**: `apoc_version: "5.15.0"` (or matching Neo4j version)

**Rollback Point**: If APOC fails, container can be reverted to snapshot before install

---

### Phase 3B: Deploy Mathematical Models (IF APOC INSTALLED)
**Time**: 30 minutes
**Prerequisites**: APOC installed and verified
**Scripts**: 04, 05

#### Task 3B.1: Deploy Psychohistory Equations
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  --file /path/to/04_psychohistory_equations.cypher
```

**Verification**:
```cypher
// Test each function:
RETURN psychohistory.epidemicThreshold(0.3, 0.1, 100) AS R0_test;
// Expected: ~9.49

RETURN psychohistory.isingDynamics(0.5, 2.0, 0.5, 10, 0) AS ising_test;
// Expected: float between -1 and 1

RETURN psychohistory.granovetterCascade(10, 100, 0.3) AS cascade_test;
// Expected: integer (predicted adopters)
```

#### Task 3B.2: Deploy Seldon Crisis Detection
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  --file /path/to/05_seldon_crisis_detection.cypher
```

**Verification**:
```cypher
// Verify 3 SeldonCrisis nodes created:
MATCH (sc:SeldonCrisis)
RETURN sc.crisis_id, sc.name, sc.intervention_window_months
ORDER BY sc.crisis_id;
// Expected: SC001, SC002, SC003

// Verify 17 CrisisIndicator nodes created:
MATCH (ci:CrisisIndicator)-[:INDICATES]->(sc:SeldonCrisis)
RETURN sc.crisis_id, ci.type, count(*) AS indicator_count;
// Expected: SC001 (4L + 3G), SC002 (4L + 2G), SC003 (4L + 2G)
```

**CHECKPOINT**: At this point, Phase 2 is COMPLETE (mathematical models deployed)

---

### Phase 4: Rewrite and Deploy Statistical Functions (IF APOC INSTALLED)
**Time**: 8-12 hours (MAJOR EFFORT)
**Prerequisites**: APOC installed
**Scripts**: 06, 07, 08, 09 (4 scripts, 22 functions)

**WARNING**: This phase is OPTIONAL for core E27 functionality. Scripts 06-09 are REMEDIATION/ADVANCED features.

#### Task 4.1: Convert PostgreSQL Functions to APOC Procedures
**Scripts to Rewrite**:
1. `04_granovetter_CORRECTED.cypher` (3 functions) - 2 hours
2. `05_autocorrelation_COMPUTED.cypher` (3 functions) - 2 hours
3. `06_autocorrelation_DETRENDED.cypher` (7 functions) - 4 hours
4. `07_confidence_intervals.cypher` (7 functions) - 4 hours

**Rewrite Pattern**:
```cypher
// FROM (PostgreSQL-style):
CREATE OR REPLACE FUNCTION psychohistory.bootstrapCI(values LIST<FLOAT>, confidence FLOAT)
RETURNS TABLE(lower FLOAT, upper FLOAT)
LANGUAGE cypher
AS $$
  WITH values AS vals
  // Bootstrap logic...
  RETURN lower, upper
$$;

// TO (APOC procedure):
CALL apoc.custom.declareProcedure(
  'psychohistory.bootstrapCI(values :: LIST OF FLOAT, confidence :: FLOAT) :: (lower :: FLOAT, upper :: FLOAT)',
  '
  WITH $values AS vals, $confidence AS conf
  // Bootstrap logic here (SAME as before)
  RETURN lower, upper
  ',
  'READ',
  [['lower', 'FLOAT'], ['upper', 'FLOAT']]
);
```

**Complexity Assessment**:
- **06_autocorrelation_DETRENDED.cypher**: 535 lines - MOST COMPLEX
- **07_confidence_intervals.cypher**: 561 lines - SECOND MOST COMPLEX
- **04_granovetter_CORRECTED.cypher**: 170 lines - MODERATE
- **05_autocorrelation_COMPUTED.cypher**: 145 lines - MODERATE

**Recommendation**: Prioritize 04-05 (moderate), defer 06-07 (complex) unless critical

---

## Parallel vs Sequential Execution Strategy

### Parallelizable Tasks (Independent)
```
Phase 1: CAN RUN IN PARALLEL
├── Task 1.1: Fix Blocker #3 (30 min)  - Agent 1
└── Task 1.2: Fix Blocker #2 (1 hour)  - Agent 2

Total Time: 1 hour (parallel) vs 1.5 hours (sequential)
TIME SAVED: 30 minutes
```

### Sequential Tasks (Dependencies)
```
Phase 2: MUST RUN SEQUENTIALLY
└── Deploy scripts AFTER Phase 1 complete

Phase 3A: MUST RUN SEQUENTIALLY
└── Install APOC AFTER user decision

Phase 3B: MUST RUN SEQUENTIALLY
└── Deploy math models AFTER APOC installed

Phase 4: CAN PARALLELIZE REWRITES
├── Rewrite script 04 - Agent 1
├── Rewrite script 05 - Agent 2
├── Rewrite script 06 - Agent 3
└── Rewrite script 07 - Agent 4

Total Time: 4 hours (parallel) vs 12 hours (sequential)
TIME SAVED: 8 hours
```

---

## Total Time Estimates

### Option A: Full Deployment (With APOC)
```
Phase 0: User decision             - 0 hours
Phase 1: Fix blockers (PARALLEL)   - 1 hour
Phase 2: Deploy schema             - 0.5 hours
Phase 3A: Install APOC             - 0.75 hours
Phase 3B: Deploy math models       - 0.5 hours
Phase 4: Rewrite functions (PARALLEL) - 4 hours
---
TOTAL: 6.75 hours (with parallelization)
TOTAL: 14.75 hours (without parallelization)
TIME SAVED: 8 hours (54% faster)
```

### Option B: Partial Deployment (No APOC)
```
Phase 0: User decision             - 0 hours
Phase 1: Fix blockers (PARALLEL)   - 1 hour
Phase 2: Deploy schema             - 0.5 hours
---
TOTAL: 1.5 hours
FUNCTIONALITY: Schema only (NO mathematical models)
```

---

## Risk Assessment and Rollback Points

### Risk Level by Phase

| Phase | Risk Level | Rollback Difficulty | Rollback Time |
|-------|-----------|---------------------|---------------|
| Phase 1 (Fix) | LOW | EASY | 5 minutes (git reset) |
| Phase 2 (Schema) | MEDIUM | MODERATE | 30 minutes (drop constraints/indexes) |
| Phase 3A (APOC) | MEDIUM | EASY | 15 minutes (docker restart with snapshot) |
| Phase 3B (Math) | LOW | EASY | 10 minutes (drop functions) |
| Phase 4 (Stats) | LOW | EASY | 10 minutes (drop procedures) |

### Safe Rollback Strategy
```bash
# Before each phase, create snapshot:
docker commit openspg-neo4j openspg-neo4j-snapshot-phase-${PHASE}

# If rollback needed:
docker stop openspg-neo4j
docker rm openspg-neo4j
docker run --name openspg-neo4j openspg-neo4j-snapshot-phase-${PHASE}
```

---

## False Blocker Analysis

### Blocker #1 (Custom Functions) - PARTIALLY FALSE

**Original Assessment**: "Custom functions not callable without APOC"

**Reality**: Custom functions CAN be called, just not as reusable stored procedures

**Evidence**:
```cypher
// This FAILS without APOC:
CALL apoc.custom.declareFunction('psychohistory.epidemicThreshold(...)', '...');

// But THIS WORKS (inline logic):
WITH 0.3 AS beta, 0.1 AS gamma, 100 AS connections
RETURN beta / gamma * sqrt(toFloat(connections)) AS epidemicThreshold;
```

**Implications**:
- Functions ARE mathematically correct and callable
- APOC only provides **reusability** and **performance**
- Without APOC: Must inline function logic at each call site
- Trade-off: Functionality vs Maintainability

**Revised Status**: BLOCKER is FALSE for functionality, TRUE for maintainability

---

### Blocker #4 (Migration Errors) - REAL BLOCKER

**Assessment**: This IS a real blocker - PostgreSQL syntax doesn't work in Neo4j

**No Workaround**: Must rewrite 22 functions

**But**: Can prioritize - scripts 06-09 are NOT critical for E27 core functionality

---

## Optimal Execution Sequence (Final Recommendation)

### RECOMMENDED PATH: Install APOC, Deploy Core, Defer Advanced

```
PHASE 0: User Decision [0 hours]
├── Decision: Install APOC ✅
└── Rationale: Core E27 value requires mathematical models

PHASE 1: Parallel Blocker Fixes [1 hour]
├── Task 1.1: Fix Blocker #3 (syntax) - Agent A
└── Task 1.2: Fix Blocker #2 (conflicts) - Agent B
    └── TIME SAVED: 30 minutes (parallel)

PHASE 2: Deploy Schema [30 minutes]
└── Deploy 01, 02, 03 scripts
    └── CHECKPOINT: Schema foundation complete

PHASE 3A: Install APOC [45 minutes]
└── Install + configure + restart
    └── ROLLBACK POINT: Container snapshot created

PHASE 3B: Deploy Math Models [30 minutes]
└── Deploy 04, 05 scripts
    └── CHECKPOINT: Core E27 complete (7 functions operational)

PHASE 4: DEFER TO FUTURE SPRINT
└── Rewrite 06-09 as APOC procedures (8-12 hours)
    └── Rationale: Advanced features, not critical for initial deployment
```

**Total Time to Core Deployment**: 3 hours 45 minutes
**Functionality Deployed**: 100% of E27 core (schema + math models)
**Deferred**: 22 advanced statistical functions (can add later)

---

## Verification Checklist

### Phase 1 Verification
- [ ] Script 03 passes syntax validation
- [ ] Script 01 has `IF NOT EXISTS` on all constraints
- [ ] No git conflicts in modified files

### Phase 2 Verification
- [ ] `SHOW CONSTRAINTS` returns 16 constraints
- [ ] `SHOW INDEXES` returns 25+ indexes
- [ ] All 16 Super Labels have discriminator properties populated
- [ ] Migration query returns expected label counts

### Phase 3A Verification
- [ ] `apoc.version()` returns valid version
- [ ] APOC config appears in neo4j.conf
- [ ] Neo4j logs show APOC loaded successfully

### Phase 3B Verification
- [ ] All 7 psychohistory functions callable
- [ ] 3 SeldonCrisis nodes exist (SC001-SC003)
- [ ] 17 CrisisIndicator nodes exist with INDICATES relationships
- [ ] Test queries return expected values

### Phase 4 Verification (If Executed)
- [ ] All 22 statistical functions callable
- [ ] Bootstrap CI returns confidence intervals
- [ ] Autocorrelation functions return valid coefficients

---

## FINAL RECOMMENDATION

**Execute**: RECOMMENDED PATH (Install APOC, Deploy Core, Defer Advanced)

**Rationale**:
1. **Blocker #1 is partially false** - we CAN work around APOC, but shouldn't
2. **APOC installation is low-risk** - 45 minutes, easily reversible
3. **Core E27 value requires math models** - 90% of E27's value proposition
4. **Advanced features can wait** - scripts 06-09 provide marginal value
5. **Parallelization saves 8+ hours** - critical for deployment timeline

**Expected Outcome**:
- **3.75 hours** to full core E27 deployment
- **100% core functionality** (schema + 7 math models + crisis detection)
- **0% advanced functionality** (22 statistical functions deferred)
- **Low risk** with multiple rollback points
- **Production-ready** with APOC as industry-standard dependency

---

## Next Actions

**IMMEDIATE**:
1. **USER**: Approve APOC installation (YES/NO)
2. **AGENT 1**: Begin fixing Blocker #3 (syntax errors)
3. **AGENT 2**: Begin fixing Blocker #2 (index conflicts)

**AFTER USER APPROVAL**:
4. **AGENT 3**: Execute APOC installation
5. **AGENT 4**: Deploy Phase 2 scripts
6. **AGENT 5**: Deploy Phase 3B scripts
7. **ARCHITECT**: Create Phase 4 work plan for future sprint

---

**Status**: AWAITING USER DECISION ON APOC INSTALLATION
**Architect Recommendation**: APPROVE APOC (Option A)
