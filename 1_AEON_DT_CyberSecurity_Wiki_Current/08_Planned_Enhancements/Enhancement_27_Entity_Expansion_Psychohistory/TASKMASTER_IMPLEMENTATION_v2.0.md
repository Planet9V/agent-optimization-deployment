# TASKMASTER: Enhancement 27 Implementation Guide v2.0

**File:** TASKMASTER_IMPLEMENTATION_v2.0.md
**Created:** 2025-11-27 04:30:00 UTC
**Version:** v2.0.0
**Purpose:** Production deployment guide with anti-theater verification gates
**Status:** READY FOR EXECUTION

---

## CONSTITUTION

### IRON LAWS (NEVER VIOLATE)

```
╔════════════════════════════════════════════════════════════════════════════╗
║  1. DO THE ACTUAL WORK - Never build frameworks to do the work            ║
║  2. VERIFY BEFORE CLAIMING COMPLETE - Every task has a verification step  ║
║  3. NO THEATER - If it's not in the database, it doesn't exist            ║
║  4. PRESERVE THE CODEBASE - Never break existing functionality            ║
║  5. EVIDENCE > CLAIMS - Show grep/count output, not descriptions          ║
╚════════════════════════════════════════════════════════════════════════════╝
```

### QUALITY STANDARDS

| Metric | Minimum | Target | Method |
|--------|---------|--------|--------|
| Academic Citations | 35 | 50+ | DOI grep count |
| Mathematical Correctness | 100% | 100% | Formula verification |
| NER11 Coverage | 100% | 100% | MERGE statement count |
| Test Coverage | 80% | 95% | Cypher test execution |
| Documentation | Complete | Comprehensive | File existence + size |

---

## EXECUTION FRAMEWORK

### Claude-Flow Integration

**MANDATORY for all tasks:**
```bash
# Initialize swarm with Qdrant memory
npx claude-flow@alpha memory init --reasoningbank

# Store task state before execution
npx claude-flow@alpha memory store "task_[ID]_start" '{"status":"IN_PROGRESS","timestamp":"[ISO]"}' --reasoningbank

# After completion, store verification result
npx claude-flow@alpha memory store "task_[ID]_complete" '{"status":"VERIFIED","evidence":"[actual_output]"}' --reasoningbank
```

### Anti-Theater Verification Protocol

**Every task MUST include:**
1. **PRE-CHECK**: Verify prerequisites exist
2. **EXECUTION**: Do the actual work
3. **VERIFICATION**: Grep/count/query to prove completion
4. **EVIDENCE**: Store actual command output in memory
5. **CHECKPOINT**: Every 4 tasks, run full audit

---

## PHASE 1: NEO4J SCHEMA DEPLOYMENT

### Task 1.1: Backup Current Database

**Prerequisites:** Neo4j running, APOC installed

**Execution:**
```cypher
// 1.1.1: Create full backup
CALL apoc.export.cypher.all('/backup/pre_e27_backup_2025-11-27.cypher', {format: 'cypher-shell'})
YIELD file, nodes, relationships, properties
RETURN file, nodes, relationships, properties;
```

**Verification:**
```bash
# MUST return actual values, not placeholders
ls -la /backup/pre_e27_backup_2025-11-27.cypher
wc -l /backup/pre_e27_backup_2025-11-27.cypher
```

**Evidence Required:**
- File exists: YES/NO
- File size: [bytes]
- Line count: [number]

**Memory Store:**
```bash
npx claude-flow@alpha memory store "task_1.1_backup" '{"file":"/backup/pre_e27_backup.cypher","size":"[bytes]","lines":"[count]"}' --reasoningbank
```

**Rollback:**
```bash
cypher-shell -u neo4j -p [password] < /backup/pre_e27_backup_2025-11-27.cypher
```

---

### Task 1.2: Create 16 Super Labels with Constraints

**Prerequisites:** Task 1.1 backup verified

**Execution:**
```cypher
// Execute from: cypher/01_constraints.cypher

// 1.2.1: Create uniqueness constraints for all 16 Super Labels
CREATE CONSTRAINT threat_actor_id IF NOT EXISTS FOR (n:ThreatActor) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT attack_pattern_id IF NOT EXISTS FOR (n:AttackPattern) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT vulnerability_id IF NOT EXISTS FOR (n:Vulnerability) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT malware_id IF NOT EXISTS FOR (n:Malware) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT control_id IF NOT EXISTS FOR (n:Control) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT asset_id IF NOT EXISTS FOR (n:Asset) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT organization_id IF NOT EXISTS FOR (n:Organization) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT location_id IF NOT EXISTS FOR (n:Location) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT software_id IF NOT EXISTS FOR (n:Software) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT indicator_id IF NOT EXISTS FOR (n:Indicator) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT event_id IF NOT EXISTS FOR (n:Event) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT campaign_id IF NOT EXISTS FOR (n:Campaign) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT psych_trait_id IF NOT EXISTS FOR (n:PsychTrait) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT economic_metric_id IF NOT EXISTS FOR (n:EconomicMetric) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT role_id IF NOT EXISTS FOR (n:Role) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT protocol_id IF NOT EXISTS FOR (n:Protocol) REQUIRE n.id IS UNIQUE;
```

**Verification:**
```cypher
// MUST return exactly 16 constraints
SHOW CONSTRAINTS
WHERE type = 'UNIQUENESS'
RETURN count(*) AS constraint_count;
```

**Evidence Required:**
- constraint_count = 16: YES/NO
- If NO, list missing constraints

**Anti-Theater Check:**
```bash
# Run this grep on the constraint output - MUST show 16 lines
echo "SHOW CONSTRAINTS" | cypher-shell -u neo4j -p [password] | grep -c "UNIQUENESS"
```

---

### Task 1.3: Create Performance Indexes

**Prerequisites:** Task 1.2 constraints verified (count = 16)

**Execution:**
```cypher
// Execute from: cypher/02_indexes.cypher

// Composite indexes for common query patterns
CREATE INDEX asset_class_type IF NOT EXISTS FOR (n:Asset) ON (n.assetClass, n.deviceType);
CREATE INDEX threat_actor_sophistication IF NOT EXISTS FOR (n:ThreatActor) ON (n.sophistication, n.motivation);
CREATE INDEX vulnerability_severity IF NOT EXISTS FOR (n:Vulnerability) ON (n.severity, n.cvssScore);
CREATE INDEX event_timestamp IF NOT EXISTS FOR (n:Event) ON (n.timestamp, n.eventType);
CREATE INDEX indicator_type IF NOT EXISTS FOR (n:Indicator) ON (n.indicatorType, n.confidence);
CREATE INDEX psych_trait_type IF NOT EXISTS FOR (n:PsychTrait) ON (n.traitType, n.intensity);
CREATE INDEX economic_metric_type IF NOT EXISTS FOR (n:EconomicMetric) ON (n.metricType, n.currency);
CREATE INDEX control_type IF NOT EXISTS FOR (n:Control) ON (n.controlType, n.effectiveness);
CREATE INDEX malware_family IF NOT EXISTS FOR (n:Malware) ON (n.malwareFamily, n.variant);
CREATE INDEX campaign_attribution IF NOT EXISTS FOR (n:Campaign) ON (n.attribution, n.confidence);

// Full-text search indexes
CREATE FULLTEXT INDEX threat_actor_search IF NOT EXISTS FOR (n:ThreatActor) ON EACH [n.name, n.aliases, n.description];
CREATE FULLTEXT INDEX vulnerability_search IF NOT EXISTS FOR (n:Vulnerability) ON EACH [n.name, n.description, n.cveId];
```

**Verification:**
```cypher
SHOW INDEXES WHERE type IN ['RANGE', 'FULLTEXT']
RETURN count(*) AS index_count;
```

**Evidence Required:**
- index_count >= 12: YES/NO

---

### 🔍 CHECKPOINT 1: Schema Foundation Verification

**Run after Tasks 1.1-1.3**

```bash
# Execute comprehensive schema check
npx claude-flow@alpha task orchestrate --task "schema_verification" --agents "code-analyzer,tester" --memory-enabled

# Store checkpoint result
npx claude-flow@alpha memory store "checkpoint_1" '{"backup":"[verified]","constraints":"[count]","indexes":"[count]"}' --reasoningbank
```

**Verification Queries:**
```cypher
// Query 1: Count all constraints
SHOW CONSTRAINTS YIELD * RETURN count(*) AS total_constraints;

// Query 2: Count all indexes
SHOW INDEXES YIELD * RETURN count(*) AS total_indexes;

// Query 3: Verify no orphaned labels
CALL db.labels() YIELD label RETURN label ORDER BY label;
```

**CHECKPOINT GATE:**
| Check | Required | Actual | Status |
|-------|----------|--------|--------|
| Backup exists | YES | [?] | PASS/FAIL |
| Constraints | 16 | [?] | PASS/FAIL |
| Indexes | 12+ | [?] | PASS/FAIL |

**IF ANY FAIL: STOP. Do not proceed. Fix issues first.**

---

## PHASE 2: LABEL MIGRATION (24 → 16)

### Task 2.1: Migrate Deprecated Labels

**Prerequisites:** Checkpoint 1 PASSED

**Execution:**
```cypher
// Execute from: cypher/03_migration_24_to_16.cypher

// 2.1.1: Migrate AttackTechnique → AttackPattern
MATCH (n:AttackTechnique)
SET n:AttackPattern, n.patternType = 'technique'
REMOVE n:AttackTechnique
RETURN count(n) AS migrated_attack_techniques;

// 2.1.2: Migrate CVE → Vulnerability
MATCH (n:CVE)
SET n:Vulnerability, n.vulnType = 'cve'
REMOVE n:CVE
RETURN count(n) AS migrated_cves;

// 2.1.3: Migrate Exploit → Vulnerability
MATCH (n:Exploit)
SET n:Vulnerability, n.vulnType = 'exploit'
REMOVE n:Exploit
RETURN count(n) AS migrated_exploits;

// 2.1.4: Migrate OT Assets → Asset
MATCH (n:Substation)
SET n:Asset, n.assetClass = 'OT', n.deviceType = 'substation'
REMOVE n:Substation
RETURN count(n) AS migrated_substations;

MATCH (n:TransmissionLine)
SET n:Asset, n.assetClass = 'OT', n.deviceType = 'transmission_line'
REMOVE n:TransmissionLine
RETURN count(n) AS migrated_transmission;

MATCH (n:EnergyDevice)
SET n:Asset, n.assetClass = 'OT', n.deviceType = 'energy_device'
REMOVE n:EnergyDevice
RETURN count(n) AS migrated_energy;

// Continue for all deprecated labels...
```

**Verification:**
```cypher
// MUST return exactly 16 labels (or fewer if some have no nodes)
CALL db.labels() YIELD label
WITH label WHERE label IN ['ThreatActor', 'AttackPattern', 'Vulnerability', 'Malware',
                           'Control', 'Asset', 'Organization', 'Location', 'Software',
                           'Indicator', 'Event', 'Campaign', 'PsychTrait', 'EconomicMetric',
                           'Role', 'Protocol']
RETURN count(label) AS super_label_count;

// MUST return 0 deprecated labels
CALL db.labels() YIELD label
WITH label WHERE label IN ['AttackTechnique', 'CVE', 'Exploit', 'Substation',
                           'TransmissionLine', 'EnergyDevice', 'MalwareVariant']
RETURN count(label) AS deprecated_count;
```

**Evidence Required:**
- super_label_count = 16: YES/NO
- deprecated_count = 0: YES/NO

**Anti-Theater Check:**
```bash
# Must return 0 deprecated labels
echo "CALL db.labels() YIELD label WHERE label IN ['AttackTechnique','CVE','Exploit'] RETURN count(label)" | cypher-shell | grep -c "0"
```

---

### Task 2.2: Add Discriminator Properties

**Prerequisites:** Task 2.1 migration verified

**Execution:**
```cypher
// Ensure all nodes have discriminator properties
MATCH (n:Asset) WHERE n.assetClass IS NULL SET n.assetClass = 'IT';
MATCH (n:Asset) WHERE n.deviceType IS NULL SET n.deviceType = 'generic';
MATCH (n:Vulnerability) WHERE n.vulnType IS NULL SET n.vulnType = 'generic';
MATCH (n:Control) WHERE n.controlType IS NULL SET n.controlType = 'generic';
MATCH (n:Indicator) WHERE n.indicatorType IS NULL SET n.indicatorType = 'generic';
MATCH (n:Event) WHERE n.eventType IS NULL SET n.eventType = 'generic';
MATCH (n:PsychTrait) WHERE n.traitType IS NULL SET n.traitType = 'generic';
MATCH (n:EconomicMetric) WHERE n.metricType IS NULL SET n.metricType = 'generic';
```

**Verification:**
```cypher
// Must return 0 nodes missing discriminators
MATCH (n:Asset) WHERE n.assetClass IS NULL OR n.deviceType IS NULL RETURN count(n) AS missing_asset_discriminators;
MATCH (n:Vulnerability) WHERE n.vulnType IS NULL RETURN count(n) AS missing_vuln_discriminators;
```

---

### 🔍 CHECKPOINT 2: Migration Verification

**Run after Tasks 2.1-2.2**

```bash
npx claude-flow@alpha task orchestrate --task "migration_verification" --agents "code-analyzer,reviewer" --memory-enabled
```

**Verification Script:**
```cypher
// Complete migration audit
CALL db.labels() YIELD label
WITH collect(label) AS all_labels
RETURN
  size([l IN all_labels WHERE l IN ['ThreatActor','AttackPattern','Vulnerability','Malware','Control','Asset','Organization','Location','Software','Indicator','Event','Campaign','PsychTrait','EconomicMetric','Role','Protocol']]) AS super_labels,
  size([l IN all_labels WHERE l IN ['AttackTechnique','CVE','Exploit','Substation','TransmissionLine']]) AS deprecated_labels;
```

**CHECKPOINT GATE:**
| Check | Required | Actual | Status |
|-------|----------|--------|--------|
| Super Labels | 16 | [?] | PASS/FAIL |
| Deprecated | 0 | [?] | PASS/FAIL |
| Discriminators | 100% | [?] | PASS/FAIL |

---

## PHASE 3: PSYCHOHISTORY EQUATIONS

### Task 3.1: Deploy Epidemic Threshold (R₀)

**Prerequisites:** Checkpoint 2 PASSED

**Academic Basis:**
- Kermack & McKendrick (1927) DOI: 10.1098/rspa.1927.0118
- Pastor-Satorras & Vespignani (2001) DOI: 10.1103/PhysRevLett.86.3200

**Execution:**
```cypher
// Execute from: cypher/04_psychohistory_equations.cypher

// R₀ = β/γ × λ₁(A) where λ₁ = largest eigenvalue of adjacency matrix
CALL apoc.custom.declareFunction(
  'psychohistory.epidemicThreshold(beta :: FLOAT, gamma :: FLOAT, eigenvalue :: FLOAT) :: FLOAT',
  '
  WITH $beta AS transmission_rate,
       $gamma AS recovery_rate,
       $eigenvalue AS lambda_max
  RETURN (transmission_rate / recovery_rate) * lambda_max AS R0
  '
);

// Practical R₀ estimation from network
CALL apoc.custom.declareFunction(
  'psychohistory.estimateR0(infected :: INTEGER, susceptible :: INTEGER, recovered :: INTEGER, time_days :: FLOAT) :: MAP',
  '
  WITH $infected AS I, $susceptible AS S, $recovered AS R, $time_days AS t
  WITH I, S, R, t, (I + S + R) AS N
  WITH I, S, R, t, N,
       CASE WHEN R > 0 THEN toFloat(I) / R ELSE 0.0 END AS simple_ratio,
       CASE WHEN S > 0 AND t > 0 THEN (toFloat(I) * N) / (S * t) ELSE 0.0 END AS sir_estimate
  RETURN {
    simple_R0: simple_ratio,
    sir_R0: sir_estimate,
    interpretation: CASE
      WHEN sir_estimate > 1.0 THEN \"SPREADING - Epidemic will grow\"
      WHEN sir_estimate = 1.0 THEN \"ENDEMIC - Stable infection rate\"
      ELSE \"DECLINING - Epidemic dying out\"
    END
  }
  '
);
```

**Verification:**
```cypher
// Test R₀ calculation
WITH 0.3 AS beta, 0.1 AS gamma, 2.5 AS eigenvalue
RETURN psychohistory.epidemicThreshold(beta, gamma, eigenvalue) AS R0;
// Expected: 7.5 (because 0.3/0.1 * 2.5 = 7.5)

// Verify function exists
SHOW FUNCTIONS YIELD name WHERE name STARTS WITH 'psychohistory'
RETURN name;
```

**Evidence Required:**
- R0 calculation returns 7.5: YES/NO
- Function count: [number]

---

### Task 3.2: Deploy Granovetter Cascade (CORRECTED)

**Academic Basis:**
- Granovetter (1978) DOI: 10.1086/226707
- Watts (2002) DOI: 10.1073/pnas.082090499

**CRITICAL: Use UNIFORM CDF, NOT exponential**

**Execution:**
```cypher
// Execute from: remediation/04_granovetter_CORRECTED.cypher

// CORRECT implementation with uniform CDF
CALL apoc.custom.declareFunction(
  'psychohistory.granovetterCascadeUniform(adopters :: INTEGER, population :: INTEGER, threshold_max :: FLOAT) :: INTEGER',
  '
  // Granovetter (1978) equilibrium: r* = N × F(r*/N)
  // With uniform CDF: F(x) = min(x / threshold_max, 1.0)

  WITH $adopters AS current_adopters,
       $population AS N,
       $threshold_max AS theta_max

  WITH current_adopters, N, theta_max,
       toFloat(current_adopters) / N AS adoption_fraction

  WITH N, theta_max, adoption_fraction,
       CASE
         WHEN adoption_fraction < theta_max
         THEN adoption_fraction / theta_max
         ELSE 1.0
       END AS cdf_value

  RETURN toInteger(N * cdf_value)
  '
);
```

**Verification:**
```cypher
// Test cascade prediction
WITH 25 AS adopters, 100 AS population, 0.25 AS threshold
RETURN psychohistory.granovetterCascadeUniform(adopters, population, threshold) AS next_adopters;
// Expected: 100 (full cascade because 25% >= 25% threshold)

// Test below threshold
WITH 10 AS adopters, 100 AS population, 0.25 AS threshold
RETURN psychohistory.granovetterCascadeUniform(adopters, population, threshold) AS next_adopters;
// Expected: 40 (partial cascade: 10/100 = 0.1, 0.1/0.25 = 0.4, 100*0.4 = 40)
```

**Anti-Theater Check:**
```bash
# Verify NO exponential CDF in production code
grep -c "exp(" /home/jim/2_OXOT_Projects_Dev/1_2025_11-25_documentation_no_NER11/enhancements/Enhancement_27_Entity_Expansion_Psychohistory/remediation/04_granovetter_CORRECTED.cypher
# Should return only comparison/documentation references, not in actual function
```

---

### Task 3.3: Deploy Critical Slowing (WITH DETRENDING)

**Academic Basis:**
- Scheffer et al. (2009) DOI: 10.1038/nature08227
- Dakos et al. (2012) DOI: 10.1371/journal.pone.0041010

**CRITICAL: Must detrend BEFORE computing autocorrelation**

**Execution:**
```cypher
// Execute from: remediation/06_autocorrelation_DETRENDED.cypher

// Detrending function (moving average)
CALL apoc.custom.declareFunction(
  'psychohistory.detrendMovingAverage(values :: LIST OF FLOAT, window :: INTEGER) :: LIST OF FLOAT',
  '
  WITH $values AS vals, $window AS w
  WITH vals, w, size(vals) AS n
  WITH vals, w, n,
       [i IN range(0, n-1) |
         vals[i] - reduce(s = 0.0, j IN range(
           CASE WHEN i - w/2 < 0 THEN 0 ELSE i - w/2 END,
           CASE WHEN i + w/2 >= n THEN n-1 ELSE i + w/2 END
         ) | s + vals[j]) / (CASE WHEN i + w/2 >= n THEN n - (CASE WHEN i - w/2 < 0 THEN 0 ELSE i - w/2 END) ELSE w + 1 END)
       ] AS detrended
  RETURN detrended
  '
);

// Critical slowing with detrending
CALL apoc.custom.declareFunction(
  'psychohistory.criticalSlowingDetrended(values :: LIST OF FLOAT, bandwidth :: FLOAT) :: MAP',
  '
  WITH $values AS vals, $bandwidth AS bw
  WHERE size(vals) >= 10

  // Step 1: Detrend
  WITH vals, bw, size(vals) AS n,
       toInteger(size(vals) * bw) AS window

  // ... [full implementation from 06_autocorrelation_DETRENDED.cypher]

  RETURN {
    variance: variance,
    autocorrelation: autocorr,
    critical_slowing_indicator: csi,
    detrended: true,
    bandwidth: bw,
    interpretation: CASE
      WHEN autocorr > 0.8 AND variance > 10 THEN \"CRITICAL - High risk of transition\"
      WHEN autocorr > 0.6 AND variance > 5 THEN \"WARNING - Elevated risk\"
      WHEN autocorr > 0.4 THEN \"CAUTION - Monitor closely\"
      ELSE \"STABLE - Normal operating range\"
    END
  }
  '
);
```

**Verification:**
```cypher
// Test with sample data
WITH [10.0, 10.2, 10.1, 10.5, 10.3, 10.8, 10.6, 11.0, 10.9, 11.2] AS stable_series
RETURN psychohistory.criticalSlowingDetrended(stable_series, 0.25) AS result;
// Should show detrended: true and STABLE interpretation
```

---

### Task 3.4: Deploy Confidence Intervals

**Academic Basis:**
- Efron & Tibshirani (1993) - Bootstrap Methods
- Fisher (1921) - Z-transform for correlations

**Execution:**
```cypher
// Execute from: remediation/07_confidence_intervals.cypher

// Bootstrap confidence interval
CALL apoc.custom.declareFunction(
  'psychohistory.bootstrapCI(values :: LIST OF FLOAT, statistic :: STRING, n_bootstrap :: INTEGER, alpha :: FLOAT) :: MAP',
  '
  // Implementation provides percentile-based CI
  // statistic: "mean", "median", "variance", "autocorr"
  // Returns: {lower: X, upper: Y, point_estimate: Z, confidence: 1-alpha}
  '
);

// Autocorrelation CI using Fisher Z-transform
CALL apoc.custom.declareFunction(
  'psychohistory.autocorrelationCI(autocorr :: FLOAT, n_samples :: INTEGER, alpha :: FLOAT) :: MAP',
  '
  WITH $autocorr AS r, $n_samples AS n, $alpha AS a
  WITH r, n, a,
       0.5 * log((1 + r) / (1 - r)) AS z,
       1.0 / sqrt(n - 3) AS se
  WITH z, se, a,
       z - 1.96 * se AS z_lower,
       z + 1.96 * se AS z_upper
  RETURN {
    lower: (exp(2 * z_lower) - 1) / (exp(2 * z_lower) + 1),
    upper: (exp(2 * z_upper) - 1) / (exp(2 * z_upper) + 1),
    point_estimate: r,
    confidence: 1 - a
  }
  '
);
```

**Verification:**
```cypher
// Test CI calculation
RETURN psychohistory.autocorrelationCI(0.7, 100, 0.05) AS ci;
// Should return lower and upper bounds around 0.7
```

---

### 🔍 CHECKPOINT 3: Psychohistory Equations Verification

**Run after Tasks 3.1-3.4**

```bash
npx claude-flow@alpha task orchestrate --task "psychohistory_verification" --agents "code-analyzer,tester,reviewer" --memory-enabled
```

**Verification:**
```cypher
// Count all psychohistory functions
SHOW FUNCTIONS YIELD name
WHERE name STARTS WITH 'psychohistory'
RETURN count(*) AS function_count, collect(name) AS functions;
```

**CHECKPOINT GATE:**
| Check | Required | Actual | Status |
|-------|----------|--------|--------|
| Functions deployed | 7+ | [?] | PASS/FAIL |
| R₀ test passes | YES | [?] | PASS/FAIL |
| Cascade test passes | YES | [?] | PASS/FAIL |
| Detrending present | YES | [?] | PASS/FAIL |
| CI functions work | YES | [?] | PASS/FAIL |

---

## PHASE 4: NER11 ENTITY MAPPING

### Task 4.1: Execute NER11 Mapping Script

**Prerequisites:** Checkpoint 3 PASSED

**Source File:** `/home/jim/2_OXOT_Projects_Dev/docs/NER11_UNMAPPED_TIERS_CYPHER.cypher`

**Execution:**
```bash
# Execute the 197 MERGE statements
cypher-shell -u neo4j -p [password] < /home/jim/2_OXOT_Projects_Dev/docs/NER11_UNMAPPED_TIERS_CYPHER.cypher
```

**Verification:**
```cypher
// Count nodes by Super Label after mapping
MATCH (n)
WHERE any(label IN labels(n) WHERE label IN ['PsychTrait', 'Control', 'Indicator', 'Event', 'EconomicMetric'])
WITH labels(n)[0] AS label, count(n) AS node_count
RETURN label, node_count
ORDER BY node_count DESC;

// Verify TIER counts
MATCH (n) WHERE n.ner11_tier = 5 RETURN 'TIER 5' AS tier, count(n) AS count
UNION ALL
MATCH (n) WHERE n.ner11_tier = 7 RETURN 'TIER 7' AS tier, count(n) AS count
UNION ALL
MATCH (n) WHERE n.ner11_tier = 8 RETURN 'TIER 8' AS tier, count(n) AS count
UNION ALL
MATCH (n) WHERE n.ner11_tier = 9 RETURN 'TIER 9' AS tier, count(n) AS count;
```

**Evidence Required:**
| Tier | Expected | Actual | Status |
|------|----------|--------|--------|
| TIER 5 | 47 | [?] | PASS/FAIL |
| TIER 7 | 63 | [?] | PASS/FAIL |
| TIER 8 | 42 | [?] | PASS/FAIL |
| TIER 9 | 45 | [?] | PASS/FAIL |
| **TOTAL** | **197** | [?] | PASS/FAIL |

**Anti-Theater Check:**
```bash
# Verify 197 MERGE statements in source file
grep -c "MERGE" /home/jim/2_OXOT_Projects_Dev/docs/NER11_UNMAPPED_TIERS_CYPHER.cypher
# MUST return 197
```

---

### 🔍 CHECKPOINT 4: NER11 Mapping Verification

```bash
npx claude-flow@alpha task orchestrate --task "ner11_verification" --agents "code-analyzer" --memory-enabled

# Store evidence
npx claude-flow@alpha memory store "checkpoint_4_ner11" '{"tier5":"[count]","tier7":"[count]","tier8":"[count]","tier9":"[count]","total":"[count]"}' --reasoningbank
```

---

## PHASE 5: SELDON CRISIS DETECTION

### Task 5.1: Deploy Crisis Detection Queries

**Prerequisites:** Checkpoint 4 PASSED

**Execution:**
```cypher
// Execute from: cypher/05_seldon_crisis_detection.cypher

// SC001: Great Resignation Cascade
CREATE (sc:SeldonCrisis {
  id: 'SC001',
  name: 'Great Resignation Cascade',
  description: 'OT expertise retirement + inadequate knowledge transfer + nation-state targeting',
  intervention_window_months: 8,
  indicators: ['retirement_rate', 'knowledge_transfer_score', 'apt_targeting_score']
});

// SC002: Supply Chain Collapse
CREATE (sc:SeldonCrisis {
  id: 'SC002',
  name: 'Supply Chain Collapse',
  description: 'Compromised firmware + JIT manufacturing + regulatory blindspot',
  intervention_window_months: 4,
  indicators: ['firmware_compromise_rate', 'supply_concentration', 'regulatory_gap_score']
});

// SC003: Medical Device Pandemic
CREATE (sc:SeldonCrisis {
  id: 'SC003',
  name: 'Medical Device Pandemic',
  description: 'IoMT ransomware + hospital consolidation + clinician burnout',
  intervention_window_months: 3,
  indicators: ['iomt_vulnerability_score', 'hospital_concentration', 'burnout_index']
});

// Crisis detection composite query
CALL apoc.custom.declareFunction(
  'psychohistory.detectSeldonCrisis(crisis_id :: STRING) :: MAP',
  '
  MATCH (sc:SeldonCrisis {id: $crisis_id})
  MATCH (ind:Indicator)-[:INDICATES]->(sc)
  WITH sc, collect(ind) AS indicators

  // Compute composite crisis score
  WITH sc, indicators,
       reduce(score = 0.0, i IN indicators | score + coalesce(i.current_value, 0)) / size(indicators) AS avg_indicator

  RETURN {
    crisis: sc.name,
    intervention_window: sc.intervention_window_months,
    current_score: avg_indicator,
    status: CASE
      WHEN avg_indicator > 0.8 THEN \"CRITICAL - Immediate action required\"
      WHEN avg_indicator > 0.6 THEN \"WARNING - Elevated risk\"
      WHEN avg_indicator > 0.4 THEN \"CAUTION - Monitor closely\"
      ELSE \"STABLE\"
    END
  }
  '
);
```

**Verification:**
```cypher
// Verify 3 Seldon Crises exist
MATCH (sc:SeldonCrisis) RETURN count(sc) AS crisis_count, collect(sc.id) AS crises;

// Test detection function
RETURN psychohistory.detectSeldonCrisis('SC001') AS result;
```

---

## PHASE 6: TESTING & VALIDATION

### Task 6.1: Execute Test Suite

**Execution:**
```bash
# Run all test files
cypher-shell -u neo4j -p [password] < tests/test_label_creation.cypher
cypher-shell -u neo4j -p [password] < tests/test_psychohistory_equations.cypher
```

**Verification:**
```cypher
// Summary of test results
MATCH (t:TestResult)
RETURN t.suite AS suite,
       sum(CASE WHEN t.passed THEN 1 ELSE 0 END) AS passed,
       sum(CASE WHEN NOT t.passed THEN 1 ELSE 0 END) AS failed;
```

---

### 🔍 FINAL CHECKPOINT: Production Readiness

```bash
npx claude-flow@alpha task orchestrate --task "production_readiness" --agents "production-validator,reviewer,code-analyzer" --memory-enabled
```

**FINAL GATE:**
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

**PRODUCTION APPROVAL:**
- [ ] All checkpoints PASSED
- [ ] No FAIL status in any gate
- [ ] Anti-theater verification complete
- [ ] Rollback tested and working

---

## ROLLBACK PROCEDURES

### Complete Rollback
```bash
# Restore from backup
cypher-shell -u neo4j -p [password] < /backup/pre_e27_backup_2025-11-27.cypher
```

### Partial Rollback (Functions Only)
```cypher
// Remove psychohistory functions
CALL apoc.custom.list() YIELD name
WHERE name STARTS WITH 'psychohistory'
CALL apoc.custom.removeFunction(name)
RETURN name + ' removed' AS status;
```

### Partial Rollback (Constraints Only)
```cypher
// List and selectively drop constraints
SHOW CONSTRAINTS YIELD name, type
WHERE type = 'UNIQUENESS'
RETURN name;

// Drop specific constraint
DROP CONSTRAINT [constraint_name];
```

---

## APPENDIX A: FILE LOCATIONS

| File | Purpose | Location |
|------|---------|----------|
| Constraints | Schema setup | `cypher/01_constraints.cypher` |
| Indexes | Performance | `cypher/02_indexes.cypher` |
| Migration | Label consolidation | `cypher/03_migration_24_to_16.cypher` |
| Equations | Psychohistory math | `cypher/04_psychohistory_equations.cypher` |
| Crisis | Seldon detection | `cypher/05_seldon_crisis_detection.cypher` |
| Granovetter Fix | Corrected cascade | `remediation/04_granovetter_CORRECTED.cypher` |
| Autocorr Fix | With detrending | `remediation/06_autocorrelation_DETRENDED.cypher` |
| CI Functions | Confidence intervals | `remediation/07_confidence_intervals.cypher` |
| NER11 Mapping | Entity creation | `/docs/NER11_UNMAPPED_TIERS_CYPHER.cypher` |
| Theory | Academic citations | `remediation/THEORY.md` |
| Calibration | Parameter values | `remediation/CALIBRATION.md` |

---

## APPENDIX B: MEMORY KEYS

| Key | Purpose | When Stored |
|-----|---------|-------------|
| `task_[N]_start` | Task initiation | Before execution |
| `task_[N]_complete` | Task verification | After verification |
| `checkpoint_[N]` | Gate status | After checkpoint |
| `rollback_point_[N]` | Recovery state | Before risky operations |
| `final_verification` | Production approval | Final gate |

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2025-11-26 | Initial TASKMASTER |
| v2.0.0 | 2025-11-27 | Added remediation, anti-theater gates, claude-flow integration |

---

**Document Status:** READY FOR EXECUTION
**Anti-Theater:** ENABLED
**Quality Score Target:** 8.5/10+

---

**END OF TASKMASTER**
