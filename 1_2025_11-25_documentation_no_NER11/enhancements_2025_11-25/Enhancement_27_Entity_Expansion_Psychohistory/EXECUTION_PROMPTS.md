# Enhancement 27: Exact Execution Prompts

**File:** EXECUTION_PROMPTS.md
**Created:** 2025-11-27 05:00:00 UTC
**Version:** v1.0.0
**Purpose:** Copy-paste prompts for every task with Claude Code

---

## 🚀 SESSION START (New or Resumed)

### If Starting Fresh Session

**PROMPT TO CLAUDE CODE:**
```
I'm starting Enhancement 27 implementation. Initialize the environment:

1. Change to E27 directory
2. Initialize claude-flow memory with Qdrant
3. Check if we have any stored checkpoint states
4. Show me the current Neo4j database status (labels, constraints, indexes)
5. Display any previous task completion from memory

Directory: /home/jim/2_OXOT_Projects_Dev/1_2025_11-25_documentation_no_NER11/enhancements/Enhancement_27_Entity_Expansion_Psychohistory

DO THE ACTUAL WORK - run the commands and show me real output.
```

**EXPECTED OUTPUT:**
- Current directory confirmation
- Qdrant memory initialization status
- List of any stored checkpoint keys
- Neo4j status (current label count, constraint count)
- Previous task states (if resuming)

---

### If Resuming After Interruption

**PROMPT TO CLAUDE CODE:**
```
Resume Enhancement 27 implementation:

1. Query Qdrant memory for all "checkpoint_*" and "task_*" keys
2. Show me the last completed checkpoint
3. Show me which tasks are marked as complete
4. Verify the current Neo4j state matches the last checkpoint
5. Tell me which task I should start next

Use: npx claude-flow@alpha memory retrieve --reasoningbank

DO THE ACTUAL WORK - query memory and show results.
```

---

## PHASE 1: SCHEMA DEPLOYMENT

### Task 1.1: Backup Current Database

**PROMPT TO CLAUDE CODE:**
```
Execute Task 1.1 - Database Backup:

1. Create backup directory if needed: /backup/
2. Run Neo4j backup command:
   CALL apoc.export.cypher.all('/backup/pre_e27_backup_2025-11-27.cypher', {format: 'cypher-shell'})
3. Verify backup file exists and get size
4. Get line count of backup file
5. Store in memory: npx claude-flow@alpha memory store "task_1.1_backup" '{"file":"/backup/pre_e27_backup.cypher","size":"[ACTUAL]","lines":"[ACTUAL]","timestamp":"[ISO]"}' --reasoningbank

Show me the actual file size and line count.

EVIDENCE REQUIRED:
- File exists: YES/NO
- File size in bytes: [ACTUAL NUMBER]
- Line count: [ACTUAL NUMBER]
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```bash
# COPY THIS COMMAND TO VERIFY MANUALLY (optional):
ls -lh /backup/pre_e27_backup_2025-11-27.cypher
wc -l /backup/pre_e27_backup_2025-11-27.cypher
```

---

### Task 1.2: Create Super Label Constraints

**PROMPT TO CLAUDE CODE:**
```
Execute Task 1.2 - Create 16 Super Label Constraints:

1. Execute the constraint creation script: cypher/01_constraints.cypher
2. Verify exactly 16 uniqueness constraints were created
3. Run verification query:
   SHOW CONSTRAINTS WHERE type = 'UNIQUENESS' RETURN count(*) AS constraint_count;
4. List all constraint names to confirm they match our 16 Super Labels
5. Store in memory: npx claude-flow@alpha memory store "task_1.2_constraints" '{"count":"[ACTUAL]","labels":"[LIST]","status":"PASS/FAIL"}' --reasoningbank

Show me the actual constraint count and list all constraint names.

EVIDENCE REQUIRED:
- Constraint count: [ACTUAL NUMBER] (must be 16)
- Status: PASS/FAIL

Expected constraints for:
ThreatActor, AttackPattern, Vulnerability, Malware, Control, Asset, Organization, Location, Software, Indicator, Event, Campaign, PsychTrait, EconomicMetric, Role, Protocol
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```bash
# COPY THIS COMMAND TO VERIFY MANUALLY:
echo "SHOW CONSTRAINTS WHERE type = 'UNIQUENESS' RETURN count(*) AS count;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]
```

---

### Task 1.3: Create Performance Indexes

**PROMPT TO CLAUDE CODE:**
```
Execute Task 1.3 - Create Performance Indexes:

1. Execute the index creation script: cypher/02_indexes.cypher
2. Count total indexes created (RANGE + FULLTEXT)
3. Run verification query:
   SHOW INDEXES WHERE type IN ['RANGE', 'FULLTEXT'] RETURN count(*) AS index_count;
4. List all index names
5. Store in memory: npx claude-flow@alpha memory store "task_1.3_indexes" '{"count":"[ACTUAL]","status":"PASS/FAIL"}' --reasoningbank

Show me the actual index count.

EVIDENCE REQUIRED:
- Index count: [ACTUAL NUMBER] (must be >= 12)
- Status: PASS/FAIL
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```bash
# COPY THIS COMMAND TO VERIFY MANUALLY:
echo "SHOW INDEXES YIELD type, name RETURN type, count(*) AS count;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]
```

---

### CHECKPOINT 1: Schema Foundation

**PROMPT TO CLAUDE CODE:**
```
Execute CHECKPOINT 1 - Schema Foundation Verification:

Deploy multi-agent verification:
1. Run: npx claude-flow@alpha task orchestrate --task "schema_verification" --agents "code-analyzer,tester" --memory-enabled
2. Execute verification queries:
   - Total constraints: SHOW CONSTRAINTS YIELD * RETURN count(*)
   - Total indexes: SHOW INDEXES YIELD * RETURN count(*)
   - All labels: CALL db.labels() YIELD label RETURN collect(label)
3. Check backup file still exists
4. Generate checkpoint report with actual values:

CHECKPOINT 1 GATE:
| Check | Required | Actual | Status |
|-------|----------|--------|--------|
| Backup exists | YES | [?] | PASS/FAIL |
| Constraints | 16 | [?] | PASS/FAIL |
| Indexes | 12+ | [?] | PASS/FAIL |

5. Store in memory: npx claude-flow@alpha memory store "checkpoint_1" '{"backup":"[YES/NO]","constraints":"[COUNT]","indexes":"[COUNT]","status":"PASS/FAIL"}' --reasoningbank

IF ANY CHECK FAILS: STOP and show me the failure details.
IF ALL PASS: Display "✅ CHECKPOINT 1 PASSED - Proceed to Phase 2"

Show me the actual checkpoint table with real numbers.
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```
═══════════════════════════════════════
CHECKPOINT 1 RESULTS
═══════════════════════════════════════
Backup exists: YES
Constraints: 16
Indexes: 14
Status: ✅ PASS

COPY THIS COMMAND TO VERIFY MANUALLY:
echo "SHOW CONSTRAINTS YIELD * RETURN count(*) AS constraints; SHOW INDEXES YIELD * RETURN count(*) AS indexes;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]

✅ CHECKPOINT 1 PASSED - Ready for Phase 2
```

---

## PHASE 2: LABEL MIGRATION

### Task 2.1: Migrate Deprecated Labels

**PROMPT TO CLAUDE CODE:**
```
Execute Task 2.1 - Migrate 24 Labels to 16 Super Labels:

1. Execute migration script: cypher/03_migration_24_to_16.cypher
2. Count nodes migrated for each deprecated label:
   - AttackTechnique → AttackPattern
   - CVE → Vulnerability
   - Exploit → Vulnerability
   - Substation → Asset
   - TransmissionLine → Asset
   - EnergyDevice → Asset
   (continue for all deprecated labels)
3. Verify NO deprecated labels remain:
   CALL db.labels() YIELD label
   WHERE label IN ['AttackTechnique', 'CVE', 'Exploit', 'Substation', 'TransmissionLine', 'EnergyDevice', 'MalwareVariant']
   RETURN count(label) AS deprecated_count;
4. Verify Super Labels exist:
   CALL db.labels() YIELD label
   WHERE label IN ['ThreatActor', 'AttackPattern', 'Vulnerability', 'Malware', 'Control', 'Asset', 'Organization', 'Location', 'Software', 'Indicator', 'Event', 'Campaign', 'PsychTrait', 'EconomicMetric', 'Role', 'Protocol']
   RETURN count(label) AS super_label_count;
5. Store in memory

EVIDENCE REQUIRED:
- Deprecated label count: [ACTUAL] (must be 0)
- Super label count: [ACTUAL] (must be 16 or fewer depending on data)
- Migration status: PASS/FAIL

Show me both counts.
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```bash
# COPY THIS COMMAND TO VERIFY NO DEPRECATED LABELS:
echo "CALL db.labels() YIELD label WHERE label IN ['AttackTechnique','CVE','Exploit'] RETURN count(label) AS deprecated;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]

# Expected output: deprecated | 0
```

---

### Task 2.2: Add Discriminator Properties

**PROMPT TO CLAUDE CODE:**
```
Execute Task 2.2 - Add Discriminator Properties:

1. Add discriminator properties to all nodes:
   MATCH (n:Asset) WHERE n.assetClass IS NULL SET n.assetClass = 'IT';
   MATCH (n:Asset) WHERE n.deviceType IS NULL SET n.deviceType = 'generic';
   MATCH (n:Vulnerability) WHERE n.vulnType IS NULL SET n.vulnType = 'generic';
   (continue for all Super Labels)

2. Verify NO nodes missing discriminators:
   MATCH (n:Asset) WHERE n.assetClass IS NULL OR n.deviceType IS NULL RETURN count(n);
   MATCH (n:Vulnerability) WHERE n.vulnType IS NULL RETURN count(n);
   (continue for all)

3. Show me actual counts of nodes missing discriminators

EVIDENCE REQUIRED:
- Nodes missing discriminators: [ACTUAL] (must be 0)
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```bash
# COPY THIS COMMAND TO VERIFY ALL HAVE DISCRIMINATORS:
echo "MATCH (n:Asset) WHERE n.assetClass IS NULL RETURN count(n) AS missing;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]

# Expected output: missing | 0
```

---

### CHECKPOINT 2: Migration Verification

**PROMPT TO CLAUDE CODE:**
```
Execute CHECKPOINT 2 - Migration Verification:

Deploy multi-agent verification:
1. Run: npx claude-flow@alpha task orchestrate --task "migration_verification" --agents "code-analyzer,reviewer" --memory-enabled

2. Execute comprehensive audit:
   CALL db.labels() YIELD label
   WITH collect(label) AS all_labels
   RETURN
     size([l IN all_labels WHERE l IN ['ThreatActor','AttackPattern','Vulnerability','Malware','Control','Asset','Organization','Location','Software','Indicator','Event','Campaign','PsychTrait','EconomicMetric','Role','Protocol']]) AS super_labels,
     size([l IN all_labels WHERE l IN ['AttackTechnique','CVE','Exploit','Substation','TransmissionLine']]) AS deprecated_labels;

3. Check discriminator coverage for each Super Label

CHECKPOINT 2 GATE:
| Check | Required | Actual | Status |
|-------|----------|--------|--------|
| Super Labels | 16 | [?] | PASS/FAIL |
| Deprecated | 0 | [?] | PASS/FAIL |
| Discriminators | 100% | [?] | PASS/FAIL |

4. Store checkpoint result in memory

IF ANY FAIL: STOP
IF ALL PASS: Display "✅ CHECKPOINT 2 PASSED - Proceed to Phase 3"

Show me the actual checkpoint table.
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```
═══════════════════════════════════════
CHECKPOINT 2 RESULTS
═══════════════════════════════════════
Super Labels: 16
Deprecated: 0
Discriminators: 100%
Status: ✅ PASS

✅ CHECKPOINT 2 PASSED - Ready for Phase 3
```

---

## PHASE 3: PSYCHOHISTORY EQUATIONS

### Task 3.1: Deploy Epidemic Threshold (R₀)

**PROMPT TO CLAUDE CODE:**
```
Execute Task 3.1 - Deploy Epidemic Threshold Equation:

1. Execute psychohistory equations script: cypher/04_psychohistory_equations.cypher
   (Focus on R₀ functions first)

2. Verify R₀ function exists:
   SHOW FUNCTIONS YIELD name WHERE name STARTS WITH 'psychohistory.epidemic'
   RETURN name;

3. Test R₀ calculation with known values:
   WITH 0.3 AS beta, 0.1 AS gamma, 2.5 AS eigenvalue
   RETURN psychohistory.epidemicThreshold(beta, gamma, eigenvalue) AS R0;
   Expected result: 7.5

4. Test practical R₀ estimation:
   RETURN psychohistory.estimateR0(100, 900, 50, 10) AS result;

5. Store verification in memory

EVIDENCE REQUIRED:
- R₀ function exists: YES/NO
- Test calculation result: [ACTUAL] (expected 7.5)
- Function works: PASS/FAIL

Show me the actual test result.
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```bash
# COPY THIS COMMAND TO TEST R₀ MANUALLY:
echo "WITH 0.3 AS beta, 0.1 AS gamma, 2.5 AS eigenvalue RETURN psychohistory.epidemicThreshold(beta, gamma, eigenvalue) AS R0;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]

# Expected output: R0 | 7.5
```

---

### Task 3.2: Deploy Granovetter Cascade (CORRECTED)

**PROMPT TO CLAUDE CODE:**
```
Execute Task 3.2 - Deploy CORRECTED Granovetter Cascade:

CRITICAL: This uses UNIFORM CDF, NOT exponential.

1. Execute corrected script: remediation/04_granovetter_CORRECTED.cypher

2. Verify function exists:
   SHOW FUNCTIONS YIELD name WHERE name = 'psychohistory.granovetterCascadeUniform'
   RETURN name;

3. Test cascade ABOVE threshold (should trigger full cascade):
   WITH 25 AS adopters, 100 AS population, 0.25 AS threshold
   RETURN psychohistory.granovetterCascadeUniform(adopters, population, threshold) AS next_adopters;
   Expected result: 100

4. Test cascade BELOW threshold (should have partial adoption):
   WITH 10 AS adopters, 100 AS population, 0.25 AS threshold
   RETURN psychohistory.granovetterCascadeUniform(adopters, population, threshold) AS next_adopters;
   Expected result: 40

5. ANTI-THEATER CHECK: Verify NO exponential CDF in production code:
   grep -c "exp(" remediation/04_granovetter_CORRECTED.cypher
   (Should only appear in OLD/deprecated sections, not in actual function)

6. Store verification in memory

EVIDENCE REQUIRED:
- Function exists: YES/NO
- Test 1 result: [ACTUAL] (expected 100)
- Test 2 result: [ACTUAL] (expected 40)
- No exp() in production function: VERIFIED/FAIL

Show me both test results.
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```bash
# COPY THESE COMMANDS TO TEST GRANOVETTER MANUALLY:

# Test 1 (above threshold - should cascade to 100):
echo "WITH 25 AS adopters, 100 AS population, 0.25 AS threshold RETURN psychohistory.granovetterCascadeUniform(adopters, population, threshold) AS next;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]
# Expected: next | 100

# Test 2 (below threshold - should be 40):
echo "WITH 10 AS adopters, 100 AS population, 0.25 AS threshold RETURN psychohistory.granovetterCascadeUniform(adopters, population, threshold) AS next;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]
# Expected: next | 40

# Verify NO exponential in production:
grep "exp(" remediation/04_granovetter_CORRECTED.cypher | grep -v "// " | wc -l
# Expected: 0 (all exp() should be in comments/documentation)
```

---

### Task 3.3: Deploy Critical Slowing WITH Detrending

**PROMPT TO CLAUDE CODE:**
```
Execute Task 3.3 - Deploy Critical Slowing with Detrending:

CRITICAL: Must include detrending per Dakos et al. (2012).

1. Execute detrending script: remediation/06_autocorrelation_DETRENDED.cypher

2. Verify detrending function exists:
   SHOW FUNCTIONS YIELD name WHERE name = 'psychohistory.detrendMovingAverage'
   RETURN name;

3. Verify critical slowing function exists:
   SHOW FUNCTIONS YIELD name WHERE name = 'psychohistory.criticalSlowingDetrended'
   RETURN name;

4. Test with stable time series:
   WITH [10.0, 10.2, 10.1, 10.5, 10.3, 10.8, 10.6, 11.0, 10.9, 11.2] AS stable_series
   RETURN psychohistory.criticalSlowingDetrended(stable_series, 0.25) AS result;
   Should show: detrended: true, interpretation: "STABLE"

5. Test with volatile time series:
   WITH [10.0, 12.0, 8.0, 14.0, 6.0, 16.0, 4.0, 18.0, 2.0, 20.0] AS volatile_series
   RETURN psychohistory.criticalSlowingDetrended(volatile_series, 0.25) AS result;
   Should show higher CSI and WARNING/CRITICAL status

6. ANTI-THEATER CHECK: Count "detrend" references in file:
   grep -c -i "detrend" remediation/06_autocorrelation_DETRENDED.cypher
   Should be 60+

7. Store verification in memory

EVIDENCE REQUIRED:
- Detrend function exists: YES/NO
- Critical slowing function exists: YES/NO
- Stable test shows "STABLE": YES/NO
- Volatile test shows "WARNING" or "CRITICAL": YES/NO
- Detrend references: [COUNT] (must be 60+)

Show me both test results.
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```bash
# COPY THIS COMMAND TO TEST CRITICAL SLOWING:
echo "WITH [10.0, 10.2, 10.1, 10.5, 10.3, 10.8, 10.6, 11.0, 10.9, 11.2] AS stable RETURN psychohistory.criticalSlowingDetrended(stable, 0.25) AS result;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]

# Check result.detrended = true and result.interpretation contains "STABLE"

# Verify detrending is implemented:
grep -c "detrend" remediation/06_autocorrelation_DETRENDED.cypher
# Expected: 60+ references
```

---

### Task 3.4: Deploy Confidence Intervals

**PROMPT TO CLAUDE CODE:**
```
Execute Task 3.4 - Deploy Confidence Interval Functions:

1. Execute CI script: remediation/07_confidence_intervals.cypher

2. Count all CI functions deployed:
   SHOW FUNCTIONS YIELD name WHERE name STARTS WITH 'psychohistory' AND name CONTAINS 'CI'
   RETURN count(*) AS ci_function_count;
   Expected: At least 7 functions

3. Test autocorrelation CI:
   RETURN psychohistory.autocorrelationCI(0.7, 100, 0.05) AS ci;
   Should return {lower: [value], upper: [value], point_estimate: 0.7}

4. Test bootstrap CI (if implemented):
   WITH [10.0, 10.5, 11.0, 10.2, 10.8] AS sample_data
   RETURN psychohistory.bootstrapCI(sample_data, 'mean', 1000, 0.05) AS ci;

5. Store verification in memory

EVIDENCE REQUIRED:
- CI function count: [ACTUAL] (must be >= 7)
- AutocorrelationCI test works: YES/NO
- Bootstrap CI test works: YES/NO

Show me function count and test results.
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```bash
# COPY THIS COMMAND TO VERIFY CI FUNCTIONS:
echo "SHOW FUNCTIONS YIELD name WHERE name STARTS WITH 'psychohistory' RETURN count(*) AS total;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]

# Should show at least 7 functions total (R0, Granovetter, Critical Slowing, CIs)

# Test autocorrelation CI:
echo "RETURN psychohistory.autocorrelationCI(0.7, 100, 0.05) AS ci;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]
```

---

### CHECKPOINT 3: Psychohistory Verification

**PROMPT TO CLAUDE CODE:**
```
Execute CHECKPOINT 3 - Psychohistory Equations Verification:

Deploy multi-agent verification:
1. Run: npx claude-flow@alpha task orchestrate --task "psychohistory_verification" --agents "code-analyzer,tester,reviewer" --memory-enabled

2. Count all psychohistory functions:
   SHOW FUNCTIONS YIELD name WHERE name STARTS WITH 'psychohistory'
   RETURN count(*) AS function_count, collect(name) AS functions;

3. Run all verification tests:
   - R₀ calculation test (expected: 7.5)
   - Granovetter above threshold (expected: 100)
   - Granovetter below threshold (expected: 40)
   - Critical slowing stable (expected: STABLE)
   - AutocorrelationCI (expected: returns CI object)

CHECKPOINT 3 GATE:
| Check | Required | Actual | Status |
|-------|----------|--------|--------|
| Functions deployed | 7+ | [?] | PASS/FAIL |
| R₀ test | 7.5 | [?] | PASS/FAIL |
| Granovetter test 1 | 100 | [?] | PASS/FAIL |
| Granovetter test 2 | 40 | [?] | PASS/FAIL |
| Detrending present | YES | [?] | PASS/FAIL |
| CI functions work | YES | [?] | PASS/FAIL |

4. Store checkpoint in memory

IF ANY FAIL: STOP
IF ALL PASS: Display "✅ CHECKPOINT 3 PASSED - Proceed to Phase 4"

Show me the checkpoint table with actual test results.
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```
═══════════════════════════════════════
CHECKPOINT 3 RESULTS
═══════════════════════════════════════
Functions deployed: 12
R₀ test: 7.5 ✅
Granovetter test 1: 100 ✅
Granovetter test 2: 40 ✅
Detrending present: YES ✅
CI functions work: YES ✅
Status: ✅ PASS

✅ CHECKPOINT 3 PASSED - Ready for Phase 4
```

---

## PHASE 4: NER11 ENTITY MAPPING

### Task 4.1: Execute NER11 Mapping

**PROMPT TO CLAUDE CODE:**
```
Execute Task 4.1 - NER11 Entity Mapping (197 entities):

CRITICAL: This creates actual nodes in Neo4j.

1. Verify source file exists and count MERGE statements:
   grep -c "MERGE" /home/jim/2_OXOT_Projects_Dev/docs/NER11_UNMAPPED_TIERS_CYPHER.cypher
   Expected: 197

2. Execute NER11 mapping script:
   cypher-shell -u neo4j -p [password] < /home/jim/2_OXOT_Projects_Dev/docs/NER11_UNMAPPED_TIERS_CYPHER.cypher

3. Count nodes by Super Label after mapping:
   MATCH (n)
   WHERE any(label IN labels(n) WHERE label IN ['PsychTrait', 'Control', 'Indicator', 'Event', 'EconomicMetric'])
   WITH labels(n)[0] AS label, count(n) AS node_count
   RETURN label, node_count
   ORDER BY node_count DESC;

4. Verify TIER counts:
   MATCH (n) WHERE n.ner11_tier = 5 RETURN 'TIER 5' AS tier, count(n) AS count
   UNION ALL
   MATCH (n) WHERE n.ner11_tier = 7 RETURN 'TIER 7' AS tier, count(n) AS count
   UNION ALL
   MATCH (n) WHERE n.ner11_tier = 8 RETURN 'TIER 8' AS tier, count(n) AS count
   UNION ALL
   MATCH (n) WHERE n.ner11_tier = 9 RETURN 'TIER 9' AS tier, count(n) AS count;

5. Store verification in memory

EVIDENCE REQUIRED:
| Tier | Expected | Actual | Status |
|------|----------|--------|--------|
| TIER 5 | 47 | [?] | PASS/FAIL |
| TIER 7 | 63 | [?] | PASS/FAIL |
| TIER 8 | 42 | [?] | PASS/FAIL |
| TIER 9 | 45 | [?] | PASS/FAIL |
| TOTAL | 197 | [?] | PASS/FAIL |

Show me the actual tier counts.
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```bash
# COPY THIS COMMAND TO VERIFY NER11 MAPPING:
echo "MATCH (n) WHERE n.ner11_tier IN [5,7,8,9] WITH n.ner11_tier AS tier, count(n) AS cnt RETURN tier, cnt ORDER BY tier;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]

# Expected output:
# tier | cnt
# 5    | 47
# 7    | 63
# 8    | 42
# 9    | 45

# Verify source file has 197 MERGE statements:
grep -c "MERGE" /home/jim/2_OXOT_Projects_Dev/docs/NER11_UNMAPPED_TIERS_CYPHER.cypher
# Expected: 197
```

---

### CHECKPOINT 4: NER11 Verification

**PROMPT TO CLAUDE CODE:**
```
Execute CHECKPOINT 4 - NER11 Mapping Verification:

1. Run multi-agent verification:
   npx claude-flow@alpha task orchestrate --task "ner11_verification" --agents "code-analyzer" --memory-enabled

2. Execute comprehensive NER11 audit:
   MATCH (n) WHERE n.ner11_tier IS NOT NULL
   WITH n.ner11_tier AS tier, count(n) AS count
   RETURN tier, count
   ORDER BY tier;

3. Verify 197 total entities:
   MATCH (n) WHERE n.ner11_tier IN [5,7,8,9]
   RETURN count(n) AS total_mapped;

4. Verify Super Label distribution:
   MATCH (n) WHERE n.ner11_tier IS NOT NULL
   WITH labels(n)[0] AS label, count(n) AS count
   RETURN label, count
   ORDER BY count DESC;

CHECKPOINT 4 GATE:
| Check | Required | Actual | Status |
|-------|----------|--------|--------|
| TIER 5 | 47 | [?] | PASS/FAIL |
| TIER 7 | 63 | [?] | PASS/FAIL |
| TIER 8 | 42 | [?] | PASS/FAIL |
| TIER 9 | 45 | [?] | PASS/FAIL |
| TOTAL | 197 | [?] | PASS/FAIL |

5. Store checkpoint evidence in memory:
   npx claude-flow@alpha memory store "checkpoint_4_ner11" '{"tier5":"[COUNT]","tier7":"[COUNT]","tier8":"[COUNT]","tier9":"[COUNT]","total":"[COUNT]"}' --reasoningbank

IF ANY FAIL: STOP
IF ALL PASS: Display "✅ CHECKPOINT 4 PASSED - Proceed to Phase 5"

Show me the checkpoint table with actual counts.
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```
═══════════════════════════════════════
CHECKPOINT 4 RESULTS
═══════════════════════════════════════
TIER 5: 47 ✅
TIER 7: 63 ✅
TIER 8: 42 ✅
TIER 9: 45 ✅
TOTAL: 197 ✅
Status: ✅ PASS

✅ CHECKPOINT 4 PASSED - Ready for Phase 5
```

---

## PHASE 5: SELDON CRISIS DETECTION

### Task 5.1: Deploy Seldon Crisis Frameworks

**PROMPT TO CLAUDE CODE:**
```
Execute Task 5.1 - Deploy 3 Seldon Crisis Detection Frameworks:

1. Execute Seldon crisis script: cypher/05_seldon_crisis_detection.cypher

2. Verify 3 Seldon Crisis nodes created:
   MATCH (sc:SeldonCrisis)
   RETURN count(sc) AS crisis_count, collect(sc.id) AS crises;
   Expected: 3 crises (SC001, SC002, SC003)

3. Verify crisis detection function exists:
   SHOW FUNCTIONS YIELD name WHERE name = 'psychohistory.detectSeldonCrisis'
   RETURN name;

4. Test crisis detection function:
   RETURN psychohistory.detectSeldonCrisis('SC001') AS result;
   Should return crisis info with intervention window

5. List all 3 crises with details:
   MATCH (sc:SeldonCrisis)
   RETURN sc.id AS id, sc.name AS name, sc.intervention_window_months AS window, sc.indicators AS indicators
   ORDER BY sc.id;

6. Store verification in memory

EVIDENCE REQUIRED:
- Crisis count: [ACTUAL] (must be 3)
- Crisis IDs: [LIST] (must be SC001, SC002, SC003)
- Detection function exists: YES/NO
- Test function works: YES/NO

Show me the crisis list and test result.
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```bash
# COPY THIS COMMAND TO VERIFY SELDON CRISES:
echo "MATCH (sc:SeldonCrisis) RETURN count(sc) AS count, collect(sc.id) AS ids;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]

# Expected output:
# count | ids
# 3     | ["SC001", "SC002", "SC003"]

# Test detection function:
echo "RETURN psychohistory.detectSeldonCrisis('SC001') AS result;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]
```

---

## PHASE 6: TESTING & VALIDATION

### Task 6.1: Execute Test Suite

**PROMPT TO CLAUDE CODE:**
```
Execute Task 6.1 - Run Complete Test Suite:

1. Execute label creation tests:
   cypher-shell -u neo4j -p [password] < tests/test_label_creation.cypher

2. Execute psychohistory equation tests:
   cypher-shell -u neo4j -p [password] < tests/test_psychohistory_equations.cypher

3. Summarize test results:
   MATCH (t:TestResult)
   RETURN t.suite AS suite,
          sum(CASE WHEN t.passed THEN 1 ELSE 0 END) AS passed,
          sum(CASE WHEN NOT t.passed THEN 1 ELSE 0 END) AS failed,
          (sum(CASE WHEN t.passed THEN 1 ELSE 0 END) * 100.0) / count(t) AS pass_rate;

4. Show any failed tests:
   MATCH (t:TestResult) WHERE NOT t.passed
   RETURN t.suite AS suite, t.test_name AS test, t.error AS error;

5. Store test results in memory

EVIDENCE REQUIRED:
- Total tests: [ACTUAL]
- Passed: [ACTUAL]
- Failed: [ACTUAL]
- Pass rate: [ACTUAL]% (must be >= 95%)

Show me the test summary and any failures.
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```bash
# COPY THIS COMMAND TO VERIFY TEST RESULTS:
echo "MATCH (t:TestResult) RETURN sum(CASE WHEN t.passed THEN 1 ELSE 0 END) AS passed, sum(CASE WHEN NOT t.passed THEN 1 ELSE 0 END) AS failed;" | cypher-shell -u neo4j -p [YOUR_PASSWORD]
```

---

## FINAL CHECKPOINT: Production Readiness

**PROMPT TO CLAUDE CODE:**
```
Execute FINAL CHECKPOINT - Production Readiness Verification:

Deploy comprehensive multi-agent validation:
1. Run: npx claude-flow@alpha task orchestrate --task "production_readiness" --agents "production-validator,reviewer,code-analyzer" --memory-enabled

2. Execute ALL verification queries:

Schema:
- SHOW CONSTRAINTS YIELD * RETURN count(*) AS constraints;
- SHOW INDEXES YIELD * RETURN count(*) AS indexes;
- CALL db.labels() YIELD label RETURN count(label) AS label_count;

Migration:
- CALL db.labels() YIELD label WHERE label IN ['AttackTechnique','CVE','Exploit'] RETURN count(label) AS deprecated;

Functions:
- SHOW FUNCTIONS YIELD name WHERE name STARTS WITH 'psychohistory' RETURN count(*) AS function_count;

NER11:
- MATCH (n) WHERE n.ner11_tier IN [5,7,8,9] RETURN count(n) AS ner11_total;

Crises:
- MATCH (sc:SeldonCrisis) RETURN count(sc) AS crisis_count;

Tests:
- MATCH (t:TestResult) RETURN (sum(CASE WHEN t.passed THEN 1 ELSE 0 END) * 100.0) / count(t) AS pass_rate;

Backup:
- Verify /backup/pre_e27_backup_2025-11-27.cypher exists

3. Generate FINAL GATE report:

FINAL PRODUCTION GATE:
| Category | Check | Required | Actual | Status |
|----------|-------|----------|--------|--------|
| Schema | Super Labels | 16 | [?] | PASS/FAIL |
| Schema | Constraints | 16 | [?] | PASS/FAIL |
| Schema | Indexes | 12+ | [?] | PASS/FAIL |
| Migration | Deprecated removed | 0 | [?] | PASS/FAIL |
| Equations | Functions deployed | 7+ | [?] | PASS/FAIL |
| Equations | All tests pass | YES | [?] | PASS/FAIL |
| NER11 | Entities mapped | 197 | [?] | PASS/FAIL |
| Crisis | Seldon Crises | 3 | [?] | PASS/FAIL |
| Tests | Pass rate | 95%+ | [?] | PASS/FAIL |
| Backup | Exists | YES | [?] | PASS/FAIL |

4. Store final verification in memory:
   npx claude-flow@alpha memory store "final_verification" '{"status":"[PASS/FAIL]","constraints":"[COUNT]","functions":"[COUNT]","ner11":"[COUNT]","tests":"[RATE]"}' --reasoningbank

5. If ALL PASS, generate Production Approval Certificate:

╔════════════════════════════════════════════════════════════════╗
║          ENHANCEMENT 27 PRODUCTION APPROVAL                     ║
╠════════════════════════════════════════════════════════════════╣
║  Status:              PRODUCTION READY                          ║
║  Score:               8.5/10                                    ║
║  All Gates:           PASSED                                    ║
║  Theater Detected:    NO                                        ║
║  Approval Date:       [ISO TIMESTAMP]                           ║
╚════════════════════════════════════════════════════════════════╝

IF ANY FAIL: Show failure details and STOP

Show me the complete final gate table with all actual values.
```

**AT END OF TASK, CLAUDE WILL DISPLAY:**
```
═══════════════════════════════════════════════════════════════
FINAL PRODUCTION GATE RESULTS
═══════════════════════════════════════════════════════════════

Schema:
  Super Labels: 16 ✅
  Constraints: 16 ✅
  Indexes: 14 ✅

Migration:
  Deprecated removed: 0 ✅

Equations:
  Functions deployed: 12 ✅
  All tests pass: YES ✅

NER11:
  Entities mapped: 197 ✅

Crisis:
  Seldon Crises: 3 ✅

Tests:
  Pass rate: 98.5% ✅

Backup:
  Exists: YES ✅

═══════════════════════════════════════════════════════════════

╔════════════════════════════════════════════════════════════════╗
║          ENHANCEMENT 27 PRODUCTION APPROVAL                     ║
╠════════════════════════════════════════════════════════════════╣
║  Status:              ✅ PRODUCTION READY                        ║
║  Score:               8.5/10                                    ║
║  All Gates:           ✅ PASSED (10/10)                          ║
║  Theater Detected:    NO                                        ║
║  Approval Date:       2025-11-27T06:00:00Z                     ║
╚════════════════════════════════════════════════════════════════╝

COPY THIS COMMAND TO VERIFY FINAL STATUS:
echo "SHOW CONSTRAINTS YIELD * RETURN count(*); SHOW FUNCTIONS YIELD name WHERE name STARTS WITH 'psychohistory' RETURN count(*); MATCH (n) WHERE n.ner11_tier IN [5,7,8,9] RETURN count(n);" | cypher-shell -u neo4j -p [YOUR_PASSWORD]
```

---

## ROLLBACK PROCEDURES

### If Something Goes Wrong

**PROMPT TO CLAUDE CODE:**
```
EMERGENCY: Rollback Enhancement 27 to pre-implementation state:

1. Verify backup exists:
   ls -lh /backup/pre_e27_backup_2025-11-27.cypher

2. Execute complete rollback:
   cypher-shell -u neo4j -p [password] < /backup/pre_e27_backup_2025-11-27.cypher

3. Verify rollback success:
   - Count labels: CALL db.labels() YIELD label RETURN count(label);
   - Count constraints: SHOW CONSTRAINTS YIELD * RETURN count(*);
   - Count indexes: SHOW INDEXES YIELD * RETURN count(*);

4. Store rollback event in memory:
   npx claude-flow@alpha memory store "rollback_event" '{"timestamp":"[ISO]","reason":"[REASON]","status":"complete"}' --reasoningbank

Show me the post-rollback database state.
```

---

### Partial Rollback (Functions Only)

**PROMPT TO CLAUDE CODE:**
```
Rollback ONLY psychohistory functions (keep schema changes):

1. List all psychohistory functions:
   CALL apoc.custom.list() YIELD name WHERE name STARTS WITH 'psychohistory' RETURN name;

2. Remove each function:
   CALL apoc.custom.list() YIELD name
   WHERE name STARTS WITH 'psychohistory'
   CALL apoc.custom.removeFunction(name)
   RETURN name + ' removed' AS status;

3. Verify functions removed:
   SHOW FUNCTIONS YIELD name WHERE name STARTS WITH 'psychohistory' RETURN count(*);
   Expected: 0

Show me the removal status for each function.
```

---

## APPENDIX: Quick Reference Commands

### Check Current State

**PROMPT TO CLAUDE CODE:**
```
Show me the current Enhancement 27 implementation state:

1. Label count: CALL db.labels() YIELD label RETURN count(label);
2. Constraint count: SHOW CONSTRAINTS YIELD * RETURN count(*);
3. Index count: SHOW INDEXES YIELD * RETURN count(*);
4. Function count: SHOW FUNCTIONS YIELD name WHERE name STARTS WITH 'psychohistory' RETURN count(*);
5. NER11 entity count: MATCH (n) WHERE n.ner11_tier IN [5,7,8,9] RETURN count(n);
6. Seldon crisis count: MATCH (sc:SeldonCrisis) RETURN count(sc);
7. Retrieve last checkpoint from memory: npx claude-flow@alpha memory retrieve "checkpoint_" --reasoningbank --pattern

Display a summary table.
```

---

### Query Memory for Audit Trail

**PROMPT TO CLAUDE CODE:**
```
Show me the complete Enhancement 27 audit trail from Qdrant memory:

1. List all checkpoint keys:
   npx claude-flow@alpha memory list --reasoningbank | grep checkpoint

2. List all task completion keys:
   npx claude-flow@alpha memory list --reasoningbank | grep task_

3. Retrieve each checkpoint and show status:
   - checkpoint_1
   - checkpoint_2
   - checkpoint_3
   - checkpoint_4
   - final_verification

4. Generate timeline report showing:
   - When each checkpoint was passed
   - What tasks were completed
   - Final production approval status

Display the complete audit trail.
```

---

**END OF EXECUTION PROMPTS**

═══════════════════════════════════════════════════════════════

## 📌 QUICK START SUMMARY

**Copy these in order:**

1. **Session Start:**
   "I'm starting Enhancement 27 implementation. Initialize the environment..."

2. **Phase 1 - Schema:**
   "Execute Task 1.1 - Database Backup..."
   "Execute Task 1.2 - Create 16 Super Label Constraints..."
   "Execute Task 1.3 - Create Performance Indexes..."
   "Execute CHECKPOINT 1 - Schema Foundation Verification..."

3. **Phase 2 - Migration:**
   "Execute Task 2.1 - Migrate 24 Labels to 16 Super Labels..."
   "Execute Task 2.2 - Add Discriminator Properties..."
   "Execute CHECKPOINT 2 - Migration Verification..."

4. **Phase 3 - Equations:**
   "Execute Task 3.1 - Deploy Epidemic Threshold Equation..."
   "Execute Task 3.2 - Deploy CORRECTED Granovetter Cascade..."
   "Execute Task 3.3 - Deploy Critical Slowing with Detrending..."
   "Execute Task 3.4 - Deploy Confidence Interval Functions..."
   "Execute CHECKPOINT 3 - Psychohistory Equations Verification..."

5. **Phase 4 - NER11:**
   "Execute Task 4.1 - NER11 Entity Mapping (197 entities)..."
   "Execute CHECKPOINT 4 - NER11 Mapping Verification..."

6. **Phase 5 - Crisis:**
   "Execute Task 5.1 - Deploy 3 Seldon Crisis Detection Frameworks..."

7. **Phase 6 - Testing:**
   "Execute Task 6.1 - Run Complete Test Suite..."

8. **Final Gate:**
   "Execute FINAL CHECKPOINT - Production Readiness Verification..."

═══════════════════════════════════════════════════════════════
