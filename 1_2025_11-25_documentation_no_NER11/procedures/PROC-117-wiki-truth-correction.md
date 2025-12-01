# PROCEDURE: [PROC-117] Wiki Truth Correction & Data Validation

**Procedure ID**: PROC-117
**Version**: 1.0.0
**Created**: 2025-11-26
**Last Modified**: 2025-11-26
**Author**: AEON ETL Agent System
**Status**: APPROVED

---

## 1. METADATA

| Field | Value |
|-------|-------|
| **Category** | VALIDATION |
| **Frequency** | ON-DEMAND / MONTHLY |
| **Priority** | CRITICAL |
| **Estimated Duration** | 30-60 minutes |
| **Risk Level** | MEDIUM |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Correct documented claims in wiki/documentation against actual Neo4j database reality using evidence-based verification queries. Addresses GAP-002 (Documentation-Reality Divergence).

### 2.2 Business Objectives
- [x] Validate all quantitative claims (node counts, relationship counts)
- [x] Identify and document discrepancies (e.g., Equipment sector count: 537,043 claimed vs 29,774 actual)
- [x] Update documentation with verified numbers
- [x] Establish audit trail for truth verification

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q1: What equipment do we have? | Correct equipment inventory counts |
| Q3: What do attackers know? | Accurate CVE coverage claims |
| Q8: What should we do? | Evidence-based recommendations |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running, accessible | `docker ps \| grep neo4j` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query/Command | Expected Result |
|-----------|---------------------------|-----------------|
| Database populated | `MATCH (n) RETURN count(n)` | >= 1,000,000 |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format |
|-------------|------|----------|--------|
| Neo4j Production DB | Graph Database | localhost:7687 | Cypher |
| Wiki Documentation | Markdown | `wiki/` directory | Text |

### 4.2 Evidence Queries

#### Query 1: Total Node Count

**Purpose**: Verify "1,104,066 total nodes" claim

**Cypher Query**:
```cypher
MATCH (n)
RETURN count(n) AS total_nodes;
```

**Expected Result**: 1,104,066 (from E06b DATA_SOURCES evidence)

#### Query 2: Equipment with Sector Classification

**Purpose**: Correct "537,043 equipment entities" claim

**Cypher Query**:
```cypher
MATCH (n:Equipment)
WHERE n.sector IS NOT NULL
RETURN count(n) AS equipment_with_sector;
```

**Verified Result**: 29,774 (NOT 537,043)

**Root Cause Analysis**: Likely counted equipment × relationships instead of unique equipment

#### Query 3: InformationEvent Nodes

**Cypher Query**:
```cypher
MATCH (n:InformationEvent)
RETURN count(n) AS event_count;
```

**Verified Result**: 5,001

#### Query 4: HistoricalPattern Nodes

**Cypher Query**:
```cypher
MATCH (n:HistoricalPattern)
RETURN count(n) AS pattern_count;
```

**Verified Result**: 14,985

#### Query 5: FutureThreat Nodes

**Cypher Query**:
```cypher
MATCH (n:FutureThreat)
RETURN count(n) AS threat_count;
```

**Verified Result**: 8,900

#### Query 6: WhatIfScenario Nodes

**Cypher Query**:
```cypher
MATCH (n:WhatIfScenario)
RETURN count(n) AS scenario_count;
```

**Verified Result**: 524

---

## 5. DESTINATION

### 5.1 Target System

| Field | Value |
|-------|-------|
| **System** | Documentation files + ValidationReport node |
| **Format** | Markdown + Neo4j |

### 5.2 Target Schema

#### Node Types Created

| Label | Properties | Purpose |
|-------|-----------|---------|
| ValidationReport | report_date, claims_verified, discrepancies_found, accuracy_score | Audit trail |
| DataClaim | claim_text, claimed_value, actual_value, source_query, verified_date | Individual claim tracking |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Discrepancy Detection

| Claim Type | Detection Logic | Action |
|------------|----------------|--------|
| Node Count | abs(claimed - actual) > 100 | Flag as DISCREPANCY |
| Percentage | abs(claimed% - actual%) > 5% | Flag as MINOR |
| Boolean | claimed XOR actual | Flag as ERROR |

### 6.2 Accuracy Scoring

```
Accuracy Score = (verified_claims / total_claims) × 100
Target: >= 95%
```

---

## 7. EXECUTION STEPS

### 7.1 Step-by-Step Execution

#### Step 1: Run Verification Query Suite

**Command**:
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" --format plain \
  --file /scripts/verification_queries.cypher > /tmp/verification_results.txt
```

#### Step 2: Compare Results Against Documentation

**Script**:
```python
import re

claims = {
    "Total nodes": {"claimed": 1104066, "query": "MATCH (n) RETURN count(n)"},
    "Equipment with sector": {"claimed": 537043, "query": "MATCH (e:Equipment) WHERE e.sector IS NOT NULL RETURN count(e)"},
    "InformationEvent": {"claimed": 5001, "query": "MATCH (n:InformationEvent) RETURN count(n)"},
    "HistoricalPattern": {"claimed": 14985, "query": "MATCH (n:HistoricalPattern) RETURN count(n)"},
    "FutureThreat": {"claimed": 8900, "query": "MATCH (n:FutureThreat) RETURN count(n)"},
    "WhatIfScenario": {"claimed": 524, "query": "MATCH (n:WhatIfScenario) RETURN count(n)"}
}

discrepancies = []
for claim_name, claim_data in claims.items():
    actual = query_neo4j(claim_data["query"])
    if abs(claim_data["claimed"] - actual) > 100:
        discrepancies.append({
            "claim": claim_name,
            "claimed": claim_data["claimed"],
            "actual": actual,
            "delta": actual - claim_data["claimed"]
        })
```

#### Step 3: Create ValidationReport Node

**Command**:
```cypher
CREATE (report:ValidationReport {
  report_date: date(),
  claims_verified: 6,
  discrepancies_found: 1,
  accuracy_score: 83.3,
  timestamp: datetime()
});

// Create DataClaim nodes for each verification
CREATE (claim:DataClaim {
  claim_text: "Equipment with sector classification",
  claimed_value: 537043,
  actual_value: 29774,
  discrepancy: true,
  source_query: "MATCH (e:Equipment) WHERE e.sector IS NOT NULL RETURN count(e)",
  verified_date: date()
});
```

#### Step 4: Update Documentation Files

**Command**:
```bash
# Update wiki files with corrected numbers
sed -i 's/537,043 equipment/29,774 equipment/g' wiki/system_overview.md
sed -i 's/537043/29774/g' wiki/metrics.md
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

#### Verify ValidationReport Created

```cypher
MATCH (r:ValidationReport)
WHERE r.report_date = date()
RETURN r.claims_verified, r.discrepancies_found, r.accuracy_score;
```

#### View Discrepancies

```cypher
MATCH (claim:DataClaim {discrepancy: true})
RETURN claim.claim_text, claim.claimed_value, claim.actual_value,
       (claim.actual_value - claim.claimed_value) AS delta
ORDER BY abs(delta) DESC;
```

### 8.2 Success Criteria

| Criterion | Measurement | Threshold | Actual |
|-----------|-------------|-----------|--------|
| Claims verified | Count of DataClaim nodes | >= 6 | [To fill] |
| Accuracy score | (verified / total) × 100 | >= 95% | [To fill] |
| Documentation updated | File modification timestamps | < 1 hour old | [To fill] |

---

## 9. ROLLBACK PROCEDURE

### 9.1 Rollback Steps

```cypher
// Remove validation artifacts
MATCH (r:ValidationReport)
WHERE r.report_date = date()
DETACH DELETE r;

MATCH (c:DataClaim)
WHERE c.verified_date = date()
DELETE c;
```

```bash
# Restore documentation from git
git checkout wiki/system_overview.md wiki/metrics.md
```

---

## 10. SCHEDULING & AUTOMATION

### 10.1 Cron Schedule

```cron
# Monthly validation on 1st at 2 AM
0 2 1 * * /home/jim/scripts/etl/proc_117_truth_correction.sh >> /var/log/aeon/proc_117.log 2>&1
```

---

## 11. MONITORING & ALERTING

### 11.1 Metrics to Monitor

| Metric | Threshold | Alert |
|--------|-----------|-------|
| Accuracy score | < 95% | ERROR |
| Discrepancies | > 2 | WARN |

---

## 12. KNOWN DISCREPANCIES

### Critical Discrepancy: Equipment Count

**Claimed**: 537,043 equipment entities with sector classification
**Actual**: 29,774 equipment nodes with sector property
**Delta**: -507,269 (-94.5%)

**Root Cause Hypothesis** (from E06b DATA_SOURCES):
```
Equipment nodes (29,774) × Average relationships per equipment (~18) ≈ 536,132
```

**Resolution**: Update all documentation to reflect 29,774 as the correct equipment count. The 537K number likely represents relationship count, not node count.

---

## 13. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL Agent | Initial version based on E06b verification data |

---

**End of Procedure PROC-117**
