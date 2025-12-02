# Enhancement 27 Deployment Blocker Report
**Date**: 2025-11-28 21:50:00 UTC
**Agent**: Implementation Agent
**Status**: MULTIPLE CRITICAL BLOCKERS IDENTIFIED

## Executive Summary
Cannot deploy Enhancement 27 Cypher scripts due to **3 critical infrastructure blockers**:
1. Missing APOC procedures
2. Invalid Cypher syntax (CREATE OR REPLACE FUNCTION not supported)
3. Existing schema conflicts

---

## Script-by-Script Analysis

| Script | Status | Blocker Type | Details |
|--------|--------|--------------|---------|
| 01_constraints.cypher | BLOCKED | Schema Conflict | Organization.name index exists, prevents constraint creation |
| 02_indexes.cypher | TESTABLE | None | Likely has similar conflicts but syntax is valid |
| 03_migration_24_to_16.cypher | BLOCKED | Syntax Error | CASE statements in SET clauses need WITH aliases |
| 04_psychohistory_equations.cypher | BLOCKED | Missing APOC | Requires `apoc.custom.declareFunction` - APOC not available |
| 05_seldon_crisis_detection.cypher | BLOCKED | Missing APOC | Requires `apoc.custom.declareFunction` - APOC not available |
| 04_granovetter_CORRECTED.cypher | BLOCKED | Invalid Syntax | `CREATE OR REPLACE FUNCTION` not valid Cypher |
| 05_autocorrelation_COMPUTED.cypher | BLOCKED | Invalid Syntax | `CREATE OR REPLACE FUNCTION` not valid Cypher |
| 06_autocorrelation_DETRENDED.cypher | BLOCKED | Invalid Syntax | `CREATE OR REPLACE FUNCTION` not valid Cypher |
| 07_confidence_intervals.cypher | BLOCKED | Invalid Syntax | `CREATE OR REPLACE FUNCTION` not valid Cypher |

---

## Blocker Details

### BLOCKER 1: Missing APOC Procedures
**Scripts Affected**: 04, 05
**Issue**: Scripts call `apoc.custom.declareFunction()` but APOC is not installed/configured in Neo4j

**Evidence**:
```cypher
CALL apoc.custom.declareFunction(
  'psychohistory.epidemicThreshold(beta FLOAT, gamma FLOAT, connections INT) :: FLOAT',
  'RETURN $beta / $gamma * sqrt(toFloat($connections))'
);
```

**Resolution Required**:
- Install APOC plugin in Neo4j container
- Configure `dbms.security.procedures.unrestricted=apoc.*`
- Restart Neo4j
- OR: Rewrite functions as parameterized queries

---

### BLOCKER 2: Invalid Cypher Syntax (CREATE OR REPLACE FUNCTION)
**Scripts Affected**: 06, 07, 08, 09
**Issue**: Neo4j does not support `CREATE OR REPLACE FUNCTION` syntax - this appears to be from a different database system

**Evidence**:
```cypher
CREATE OR REPLACE FUNCTION psychohistory.bootstrapSampleIndices(n_samples INTEGER, seed INTEGER)
RETURNS LIST<INTEGER>
LANGUAGE cypher
AS $$
  ...
$$;
```

**Problem**: This is PostgreSQL-style user-defined function syntax, NOT valid Neo4j Cypher

**Resolution Required**:
- Rewrite as APOC procedures (requires Blocker 1 resolved)
- OR: Rewrite as parameterized Cypher queries
- OR: Implement in application layer (Python/Java)

---

### BLOCKER 3: Schema Conflicts
**Scripts Affected**: 01 (constraints), 02 (indexes)
**Issue**: Attempting to create constraints where indexes already exist

**Example Error**:
```
There already exists an index (:Organization {name}).
A constraint cannot be created until the index has been dropped.
```

**Existing Conflicts**:
- Organization.name (index exists)
- ThreatActor.name (constraint constraint_338f9f7b exists)
- AttackPattern.name (constraint constraint_24c3e18c exists)
- Vulnerability.name (constraint constraint_903461f9 exists)
- Asset.name (constraint constraint_368ca986 exists)
- Multiple others...

**Resolution Required**:
- Modify scripts to use `IF NOT EXISTS` (Neo4j 5.7+)
- OR: Drop existing indexes before creating constraints
- OR: Skip creation if already exists

---

### BLOCKER 4: Syntax Errors in Migration Script
**Script**: 03_migration_24_to_16.cypher
**Issue**: CASE statements in SET clauses without intermediate WITH

**Problem Code** (lines 19-26):
```cypher
MATCH (n:ThreatActor)
WHERE n.actorType IS NULL
SET n.actorType = CASE
  WHEN n.type IS NOT NULL THEN n.type
  WHEN n.name CONTAINS 'APT' THEN 'apt'
  WHEN n.name CONTAINS 'State' THEN 'nation_state'
  ELSE 'unknown'
END;
```

**Required Fix**:
```cypher
MATCH (n:ThreatActor)
WHERE n.actorType IS NULL
WITH n, CASE
  WHEN n.type IS NOT NULL THEN n.type
  WHEN n.name CONTAINS 'APT' THEN 'apt'
  WHEN n.name CONTAINS 'State' THEN 'nation_state'
  ELSE 'unknown'
END AS computed_actorType
SET n.actorType = computed_actorType;
```

**Affected Lines**: 21-26, 31-36, 41-46, 51-55, 59-64

---

## Infrastructure Prerequisites

To deploy Enhancement 27, the following infrastructure changes are REQUIRED:

### Option A: Install APOC (Recommended for Production)
```bash
# 1. Install APOC plugin
docker exec openspg-neo4j bash -c "
  cd /var/lib/neo4j/plugins &&
  wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/5.15.0/apoc-5.15.0-core.jar
"

# 2. Configure Neo4j
docker exec openspg-neo4j bash -c "
  echo 'dbms.security.procedures.unrestricted=apoc.*' >> /var/lib/neo4j/conf/neo4j.conf &&
  echo 'dbms.security.procedures.allowlist=apoc.*' >> /var/lib/neo4j/conf/neo4j.conf
"

# 3. Restart Neo4j
docker restart openspg-neo4j

# 4. Verify APOC installation
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "RETURN apoc.version() AS apoc_version;"
```

### Option B: Rewrite Without APOC (Fallback)
- Convert all stored procedures to parameterized queries
- Implement complex calculations in application layer
- Use Cypher only for data retrieval/storage
- **Tradeoff**: Performance degradation, loss of reusability

---

## Recommended Deployment Strategy

### Phase 1: Schema Foundation (Partial Deployment Possible)
1. **Fix and Deploy 01_constraints.cypher**:
   - Add `IF NOT EXISTS` checks
   - Skip conflicts with existing constraints
   - **Result**: New constraints for PsychTrait, Role, EconomicMetric, Protocol, Campaign

2. **Fix and Deploy 02_indexes.cypher**:
   - Add `IF NOT EXISTS` checks
   - Deploy discriminator property indexes
   - **Result**: Query performance improvements

3. **Fix and Deploy 03_migration_24_to_16.cypher**:
   - Add WITH clauses for CASE expressions
   - **Result**: Schema migrated to 16 Super Labels

### Phase 2: Mathematical Models (REQUIRES APOC)
**BLOCKED until APOC is installed**

4. Deploy 04_psychohistory_equations.cypher
5. Deploy 05_seldon_crisis_detection.cypher

### Phase 3: Remediation Scripts (REQUIRES REWRITE)
**BLOCKED - invalid syntax**

6. Rewrite 04_granovetter_CORRECTED.cypher as APOC procedure
7. Rewrite 05_autocorrelation_COMPUTED.cypher as APOC procedure
8. Rewrite 06_autocorrelation_DETRENDED.cypher as APOC procedure
9. Rewrite 07_confidence_intervals.cypher as APOC procedure

---

## BLOCKER RESOLUTION DECISION REQUIRED

**Question for User**: How should we proceed?

### Option 1: Install APOC (RECOMMENDED)
- **Pros**: Full E27 functionality, production-grade performance
- **Cons**: Requires Neo4j restart, container modification
- **Timeline**: 30 minutes to install and validate

### Option 2: Partial Deployment Only
- **Pros**: Can deploy Phase 1 (schema) immediately
- **Cons**: No psychohistory equations, no mathematical models
- **Timeline**: 1-2 hours to fix and deploy Phase 1

### Option 3: Complete Rewrite Without APOC
- **Pros**: No infrastructure changes needed
- **Cons**: Significant functionality loss, poor performance
- **Timeline**: 8-12 hours to rewrite all mathematical models

---

## Current Deployment Status

| Phase | Scripts | Status | Blocker |
|-------|---------|--------|---------|
| Schema Foundation | 01-03 | FIXABLE | Syntax errors, conflicts |
| Mathematical Models | 04-05 | BLOCKED | Missing APOC |
| Remediation | 06-09 | BLOCKED | Invalid syntax + Missing APOC |

**Overall Status**: **0 of 9 scripts deployed**
**Blockers**: **3 critical infrastructure issues**

---

## Next Actions

**IMMEDIATE**:
1. User decision on APOC installation
2. If APOC approved: Execute Option A installation steps
3. If no APOC: Proceed with Phase 1 partial deployment only

**AFTER BLOCKER RESOLUTION**:
1. Fix syntax errors in 01-03
2. Deploy Phase 1 scripts
3. Deploy Phase 2 scripts (if APOC available)
4. Rewrite Phase 3 scripts (if required)

---

**Agent Status**: AWAITING USER DECISION ON APOC INSTALLATION

**Recommendation**: Install APOC. Enhancement 27's psychohistory equations are the core value proposition and cannot function without stored procedures.
