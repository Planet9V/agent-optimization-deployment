# Enhancement 12: NOW/NEXT/NEVER Prioritization Framework

**File:** Enhancement_12_NOW_NEXT_NEVER/README.md
**Created:** 2025-11-25 14:30:00 UTC
**Version:** 1.0.0
**Status:** ACTIVE
**Author:** AEON Digital Twin Development Team

---

## Executive Summary

The NOW/NEXT/NEVER Prioritization Framework implements a risk-based threat triage system that categorizes the 316,000+ CVE vulnerabilities in the AEON knowledge graph into actionable priority categories. This framework combines technical vulnerability metrics (CVSS, EPSS) with organizational psychological factors (cognitive biases, patch velocity, risk tolerance) to optimize resource allocation and predict sector-specific urgency levels.

**Key Innovation**: Integration of behavioral economics and cognitive psychology into technical vulnerability prioritization, enabling predictions like "CVE-X is NOW for Energy sector, NEXT for Water sector, NEVER for Commercial facilities."

---

## Problem Statement

### Current Challenges

**Vulnerability Overload Crisis**:
- **316,000+ CVE records** in knowledge graph
- **New CVEs**: ~25,000 per year (68 per day)
- **Patch Capacity**: Most organizations can address <500 vulnerabilities per year
- **Prioritization Gap**: 99.8% of vulnerabilities must be deferred or accepted

**Cognitive Bias Impact on Patching**:
- **Normalcy Bias**: Organizations delay patching assuming "it won't happen to us"
- **Availability Heuristic**: Recent breaches receive disproportionate attention
- **Sunk Cost Fallacy**: Continue using vulnerable legacy systems due to prior investment
- **Status Quo Bias**: Resistance to patching due to operational stability concerns

**Sector-Specific Risk Tolerance**:
- **Energy/Water**: Zero tolerance for operational disruptions
- **Healthcare**: Balance between uptime and patient safety
- **Commercial**: Cost-driven decisions, higher risk acceptance
- **Defense**: Maximum security posture regardless of operational impact

---

## NOW/NEXT/NEVER Framework

### Prioritization Categories

#### NOW - Immediate Action Required
**Definition**: Patch/remediate within 24-48 hours

**Technical Triggers**:
- **Active Exploitation**: EPSS ≥ 0.70 (70%+ probability of exploitation within 30 days)
- **Critical CVSS**: Base score ≥ 9.0 with network vector
- **Critical Equipment**: Affects Tier 1 systems (power generation, water treatment, emergency response)
- **Wormable**: Self-propagating vulnerabilities (e.g., EternalBlue, Log4Shell)

**Psychological Indicators**:
- **High Organizational Risk Aversion**: Recent breach history, regulatory pressure
- **Low Normalcy Bias**: Organization with mature security culture
- **High Patch Velocity**: Historical mean time to patch <7 days

**Example Scenarios**:
- CVE-2021-44228 (Log4Shell) in Energy sector SCADA systems
- CVE-2017-0144 (EternalBlue) in Healthcare patient data systems
- CVE-2023-34362 (MOVEit Transfer) in Defense contractor networks

#### NEXT - Scheduled Remediation
**Definition**: Address during next maintenance window (30-90 days)

**Technical Triggers**:
- **Moderate CVSS**: Base score 7.0-8.9
- **Exploitable but Not Exploited**: EPSS 0.30-0.69
- **Tier 2 Equipment**: Important but not critical systems
- **Mitigated Risk**: Compensating controls in place (network segmentation, IDS/IPS)

**Psychological Indicators**:
- **Moderate Risk Tolerance**: Balanced security posture
- **Operational Stability Priority**: Prefer controlled maintenance windows
- **Medium Patch Velocity**: Historical mean time to patch 7-30 days

**Example Scenarios**:
- CVE-2023-XXXXX affecting non-critical business systems in Commercial sector
- Vulnerabilities in segmented IT networks with monitoring
- Older CVEs with available patches but low exploitation probability

#### NEVER - Risk Acceptance
**Definition**: Defer indefinitely or formally accept risk

**Technical Triggers**:
- **Low CVSS**: Base score <7.0
- **Theoretical Vulnerability**: EPSS <0.30, no public exploits
- **Tier 3 Equipment**: Non-critical, isolated systems
- **Legacy Systems**: End-of-life equipment scheduled for replacement

**Psychological Indicators**:
- **High Risk Tolerance**: Cost-driven decision making
- **High Sunk Cost Bias**: Large investment in legacy infrastructure
- **Status Quo Bias**: Operational stability prioritized over security updates

**Example Scenarios**:
- Low-severity vulnerabilities in isolated development environments
- Theoretical attacks requiring physical access in secure facilities
- Legacy SCADA systems scheduled for decommissioning within 6 months

---

## Scoring Algorithm

### Technical Score Calculation

**Formula**:
```
Technical Score = (CVSS_Base / 10) × EPSS × Equipment_Criticality_Weight

Where:
- CVSS_Base: 0.0 - 10.0 (from NVD)
- EPSS: 0.0 - 1.0 (probability of exploitation within 30 days)
- Equipment_Criticality_Weight:
  * Tier 1 (Critical): 1.0
  * Tier 2 (Important): 0.7
  * Tier 3 (Standard): 0.4
```

**Example Calculation**:
- **CVE-2021-44228 (Log4Shell)** affecting critical power generation system:
  - CVSS_Base: 10.0
  - EPSS: 0.97 (97% exploitation probability)
  - Equipment: Tier 1 Critical (1.0)
  - **Technical Score**: (10.0/10) × 0.97 × 1.0 = **0.97**

### Psychological Score Calculation

**Formula**:
```
Psychological Score = (Org_Bias_Factor × Patch_Velocity_Score × Risk_Tolerance_Inverse) / Normalization_Factor

Where:
- Org_Bias_Factor: 0.3 - 1.0 (inverse of bias severity)
  * Low Bias: 1.0
  * Moderate Bias: 0.65
  * High Bias: 0.3

- Patch_Velocity_Score: 0.0 - 1.0
  * <7 days (Fast): 1.0
  * 7-30 days (Medium): 0.6
  * >30 days (Slow): 0.3

- Risk_Tolerance_Inverse: 0.0 - 1.0
  * Low Tolerance (Energy/Water): 1.0
  * Medium Tolerance (Healthcare): 0.65
  * High Tolerance (Commercial): 0.3

- Normalization_Factor: 3.0 (scales result to 0-1 range)
```

**Example Calculation**:
- **Energy Sector Organization** with Log4Shell:
  - Org_Bias_Factor: 0.65 (moderate normalcy bias from recent breach)
  - Patch_Velocity_Score: 1.0 (historically fast patching)
  - Risk_Tolerance_Inverse: 1.0 (critical infrastructure)
  - **Psychological Score**: (0.65 × 1.0 × 1.0) / 3.0 = **0.217**

### Combined Priority Score

**Formula**:
```
Combined Score = (Technical_Score × 0.6) + (Psychological_Score × 0.4)

Priority Assignment:
- NOW: Combined Score ≥ 8.0 on 10-point scale
- NEXT: 5.0 ≤ Combined Score < 8.0
- NEVER: Combined Score < 5.0
```

**Scale Conversion**:
```
10-Point Scale = Combined_Score × 10

Example:
- Technical: 0.97
- Psychological: 0.217
- Combined: (0.97 × 0.6) + (0.217 × 0.4) = 0.582 + 0.087 = 0.669
- 10-Point: 0.669 × 10 = 6.69
- Priority: NEXT (but bordering on NOW due to high technical score)
```

**Refinement for Critical Systems**:
For Tier 1 critical equipment, apply override logic:
```
IF Technical_Score ≥ 0.85 AND Equipment = Tier 1:
    Priority = NOW (override psychological factors)
```

This ensures critical vulnerabilities affecting essential systems receive immediate attention regardless of organizational behavior patterns.

---

## Implementation Architecture

### Neo4j Graph Schema Extensions

#### New Node Label: `PriorityAssessment`
```cypher
CREATE (pa:PriorityAssessment {
    assessmentId: "PA-2025-001",
    timestamp: datetime(),
    cveId: "CVE-2021-44228",
    organizationId: "ORG-ENERGY-001",
    sectorType: "Energy",

    // Technical Scores
    cvssBase: 10.0,
    epssScore: 0.97,
    equipmentCriticality: 1.0,
    technicalScore: 0.97,

    // Psychological Scores
    orgBiasFactor: 0.65,
    patchVelocityScore: 1.0,
    riskToleranceInverse: 1.0,
    psychologicalScore: 0.217,

    // Combined Assessment
    combinedScore: 0.669,
    combinedScore10Point: 6.69,
    priorityCategory: "NEXT", // NOW, NEXT, NEVER
    overrideApplied: true,
    finalPriority: "NOW",

    // Rationale
    priorityJustification: "Critical CVSS + High EPSS + Tier 1 Equipment triggered override to NOW despite moderate psychological factors",

    // Operational Metadata
    estimatedPatchWindow: "24-48 hours",
    compensatingControls: [],
    approvalRequired: true,
    approvalStatus: "pending"
})
```

#### Relationships
```cypher
// Link to CVE
(:PriorityAssessment)-[:ASSESSES]->(:CVE)

// Link to Equipment
(:PriorityAssessment)-[:APPLIES_TO]->(:Equipment)

// Link to Organization
(:PriorityAssessment)-[:FOR_ORGANIZATION]->(:Organization)

// Link to Cognitive Biases
(:PriorityAssessment)-[:INFLUENCED_BY]->(:CognitiveBias)

// Link to Sector
(:PriorityAssessment)-[:IN_SECTOR]->(:Sector)

// Historical Context
(:PriorityAssessment)-[:SUPERSEDES]->(:PriorityAssessment {version: "previous"})
```

### Query Patterns

#### Generate Priority for CVE in Specific Sector
```cypher
MATCH (cve:CVE {cveId: $cveId})
MATCH (sector:Sector {sectorName: $sectorName})
MATCH (sector)-[:CONTAINS_EQUIPMENT]->(eq:Equipment)
WHERE (cve)-[:AFFECTS]->(eq)

WITH cve, sector, eq,
     cve.cvssBase AS cvss,
     cve.epssScore AS epss,
     CASE eq.criticalityTier
         WHEN 1 THEN 1.0
         WHEN 2 THEN 0.7
         WHEN 3 THEN 0.4
     END AS equipCrit

WITH cve, sector, eq, cvss, epss, equipCrit,
     (cvss/10.0) * epss * equipCrit AS technicalScore

MATCH (sector)-[:HAS_BEHAVIORAL_PROFILE]->(profile:OrganizationalProfile)
WITH cve, sector, eq, cvss, epss, equipCrit, technicalScore,
     profile.biasFactor AS biasFactor,
     profile.patchVelocityScore AS patchVel,
     profile.riskToleranceInverse AS riskTol,
     (profile.biasFactor * profile.patchVelocityScore * profile.riskToleranceInverse) / 3.0 AS psychScore

WITH cve, sector, eq, technicalScore, psychScore,
     (technicalScore * 0.6) + (psychScore * 0.4) AS combinedScore,
     ((technicalScore * 0.6) + (psychScore * 0.4)) * 10 AS score10Point

RETURN cve.cveId AS CVE,
       sector.sectorName AS Sector,
       eq.equipmentName AS Equipment,
       technicalScore,
       psychScore,
       score10Point,
       CASE
           WHEN score10Point >= 8.0 THEN "NOW"
           WHEN score10Point >= 5.0 THEN "NEXT"
           ELSE "NEVER"
       END AS Priority
ORDER BY score10Point DESC
```

#### Bulk Sector Prioritization
```cypher
MATCH (cve:CVE)
WHERE cve.cvssBase >= 7.0 AND cve.epssScore >= 0.3

UNWIND ["Energy", "Water", "Healthcare", "Commercial", "Defense"] AS sectorName

MATCH (sector:Sector {sectorName: sectorName})
MATCH (sector)-[:HAS_BEHAVIORAL_PROFILE]->(profile:OrganizationalProfile)

WITH cve, sector, profile,
     (cve.cvssBase/10.0) * cve.epssScore * 1.0 AS techScore,
     (profile.biasFactor * profile.patchVelocityScore * profile.riskToleranceInverse) / 3.0 AS psychScore

WITH cve, sector,
     (techScore * 0.6) + (psychScore * 0.4) AS combined,
     ((techScore * 0.6) + (psychScore * 0.4)) * 10 AS score10

CREATE (pa:PriorityAssessment {
    assessmentId: "PA-" + cve.cveId + "-" + sector.sectorName,
    timestamp: datetime(),
    cveId: cve.cveId,
    sectorType: sector.sectorName,
    combinedScore10Point: score10,
    priorityCategory: CASE
        WHEN score10 >= 8.0 THEN "NOW"
        WHEN score10 >= 5.0 THEN "NEXT"
        ELSE "NEVER"
    END
})

CREATE (pa)-[:ASSESSES]->(cve)
CREATE (pa)-[:IN_SECTOR]->(sector)

RETURN cve.cveId AS CVE,
       sector.sectorName AS Sector,
       pa.priorityCategory AS Priority,
       score10 AS Score
ORDER BY score10 DESC
LIMIT 100
```

#### McKenney Question 8: "What should we patch first?"
```cypher
MATCH (org:Organization {orgId: $orgId})
MATCH (org)-[:OPERATES_IN]->(sector:Sector)
MATCH (org)-[:OPERATES]->(eq:Equipment)
MATCH (cve:CVE)-[:AFFECTS]->(eq)
MATCH (pa:PriorityAssessment)-[:ASSESSES]->(cve)
WHERE pa.sectorType = sector.sectorName
  AND pa.priorityCategory = "NOW"

WITH pa, cve, eq
ORDER BY pa.combinedScore10Point DESC
LIMIT 20

RETURN cve.cveId AS CVE,
       cve.description AS Description,
       eq.equipmentName AS AffectedEquipment,
       pa.combinedScore10Point AS PriorityScore,
       pa.estimatedPatchWindow AS PatchWindow,
       pa.priorityJustification AS Rationale
```

---

## Use Cases

### Use Case 1: Sector-Specific Prioritization Predictions

**Scenario**: Security analyst needs to predict how different sectors should prioritize CVE-2023-XXXXX

**Query**:
```cypher
MATCH (cve:CVE {cveId: "CVE-2023-XXXXX"})
MATCH (pa:PriorityAssessment)-[:ASSESSES]->(cve)
RETURN pa.sectorType AS Sector,
       pa.priorityCategory AS Priority,
       pa.combinedScore10Point AS Score,
       pa.priorityJustification AS Rationale
ORDER BY pa.combinedScore10Point DESC
```

**Expected Output**:
```
Sector       | Priority | Score | Rationale
-------------|----------|-------|------------------------------------------
Energy       | NOW      | 8.7   | Critical SCADA system + High EPSS + Low Risk Tolerance
Water        | NOW      | 8.4   | Water treatment control + Active Exploitation
Healthcare   | NEXT     | 6.9   | Patient systems affected but compensating controls
Defense      | NOW      | 9.1   | Classified network access + Zero Tolerance Policy
Commercial   | NEXT     | 5.8   | Business impact moderate + Cost constraints
```

**Insight**: Same CVE receives different priority levels based on sector risk tolerance and equipment criticality.

### Use Case 2: Cognitive Bias Impact Analysis

**Scenario**: Identify organizations with high normalcy bias that may be under-prioritizing critical vulnerabilities

**Query**:
```cypher
MATCH (org:Organization)-[:HAS_BIAS]->(bias:CognitiveBias {biasName: "Normalcy Bias"})
WHERE bias.severityScore >= 0.7

MATCH (org)-[:OPERATES]->(eq:Equipment)
MATCH (cve:CVE)-[:AFFECTS]->(eq)
MATCH (pa:PriorityAssessment)-[:ASSESSES]->(cve)
WHERE pa.priorityCategory = "NOW"

WITH org, COUNT(DISTINCT cve) AS criticalCVEs,
     AVG(org.historicalPatchVelocity) AS avgPatchTime

WHERE avgPatchTime > 30 // Slow patching despite critical vulnerabilities

RETURN org.orgName AS Organization,
       org.sectorType AS Sector,
       criticalCVEs AS UnpatchedNOWPriorityCVEs,
       avgPatchTime AS AvgPatchTimeDays,
       "High Normalcy Bias causing dangerous patch delays" AS RiskAssessment
ORDER BY criticalCVEs DESC
```

**Expected Output**:
```
Organization          | Sector     | Unpatched NOW CVEs | Avg Patch Time | Risk Assessment
----------------------|------------|--------------------| ---------------|----------------------------------
Regional Power Coop   | Energy     | 47                 | 62 days        | High Normalcy Bias causing dangerous patch delays
County Water District | Water      | 31                 | 58 days        | High Normalcy Bias causing dangerous patch delays
Rural Hospital Network| Healthcare | 28                 | 73 days        | High Normalcy Bias causing dangerous patch delays
```

**Insight**: Organizations with high normalcy bias consistently delay patching critical vulnerabilities, creating systemic risk.

### Use Case 3: Resource Allocation Optimization

**Scenario**: CISO needs to allocate limited security budget across 1,000+ vulnerabilities

**Query**:
```cypher
MATCH (org:Organization {orgId: $orgId})
MATCH (org)-[:OPERATES]->(eq:Equipment)
MATCH (cve:CVE)-[:AFFECTS]->(eq)
MATCH (pa:PriorityAssessment)-[:ASSESSES]->(cve)

WITH pa.priorityCategory AS Priority,
     COUNT(DISTINCT cve) AS VulnCount,
     SUM(CASE WHEN pa.priorityCategory = "NOW" THEN 1 ELSE 0 END) AS NowCount,
     SUM(CASE WHEN pa.priorityCategory = "NEXT" THEN 1 ELSE 0 END) AS NextCount,
     SUM(CASE WHEN pa.priorityCategory = "NEVER" THEN 1 ELSE 0 END) AS NeverCount

RETURN NowCount AS ImmediateAction,
       NextCount AS ScheduledMaintenance,
       NeverCount AS RiskAcceptance,
       VulnCount AS TotalVulnerabilities,
       ROUND(100.0 * NowCount / VulnCount, 2) AS PercentImmediate,
       ROUND(100.0 * NextCount / VulnCount, 2) AS PercentScheduled,
       ROUND(100.0 * NeverCount / VulnCount, 2) AS PercentDeferred
```

**Expected Output**:
```
Immediate Action | Scheduled Maint | Risk Acceptance | Total Vulns | % Immediate | % Scheduled | % Deferred
-----------------|-----------------|-----------------|-------------|-------------|-------------|------------
127              | 431             | 8,442           | 9,000       | 1.41%       | 4.79%       | 93.80%
```

**Resource Allocation Decision**:
- **70% of budget** → 127 NOW priorities (immediate patching, emergency contractors)
- **20% of budget** → 431 NEXT priorities (scheduled maintenance, automation tools)
- **10% of budget** → Monitoring and compensating controls for NEVER category

### Use Case 4: Predictive Modeling for New CVEs

**Scenario**: New CVE published with CVSS 9.8, EPSS 0.02 (no active exploitation yet). Predict future priority shifts.

**Query**:
```cypher
MATCH (cve:CVE {cveId: "CVE-2025-NEW"})
SET cve.cvssBase = 9.8,
    cve.epssScore = 0.02,
    cve.publishDate = date()

// Calculate initial priority
MATCH (sector:Sector)
MATCH (sector)-[:HAS_BEHAVIORAL_PROFILE]->(profile:OrganizationalProfile)

WITH cve, sector, profile,
     (cve.cvssBase/10.0) * cve.epssScore * 1.0 AS initialTech,
     (profile.biasFactor * profile.patchVelocityScore * profile.riskToleranceInverse) / 3.0 AS psychScore

CREATE (pa:PriorityAssessment {
    assessmentId: "PA-" + cve.cveId + "-" + sector.sectorName + "-INITIAL",
    timestamp: datetime(),
    cveId: cve.cveId,
    sectorType: sector.sectorName,
    combinedScore10Point: ((initialTech * 0.6) + (psychScore * 0.4)) * 10,
    priorityCategory: CASE
        WHEN ((initialTech * 0.6) + (psychScore * 0.4)) * 10 >= 8.0 THEN "NOW"
        WHEN ((initialTech * 0.6) + (psychScore * 0.4)) * 10 >= 5.0 THEN "NEXT"
        ELSE "NEVER"
    END,
    predictionNote: "Initial EPSS low, expect escalation to NOW within 30 days if exploitation observed"
})

RETURN sector.sectorName AS Sector,
       pa.priorityCategory AS CurrentPriority,
       pa.combinedScore10Point AS CurrentScore,
       pa.predictionNote AS Prediction
```

**Expected Output (Day 0)**:
```
Sector     | Current Priority | Current Score | Prediction
-----------|------------------|---------------|--------------------------------------------------
Energy     | NEXT             | 6.2           | Initial EPSS low, expect escalation to NOW within 30 days
Water      | NEXT             | 6.1           | Initial EPSS low, expect escalation to NOW within 30 days
Healthcare | NEXT             | 5.7           | Initial EPSS low, monitor for exploitation trends
Commercial | NEVER            | 4.8           | Low initial risk, may escalate if widely exploited
```

**After 14 Days (EPSS rises to 0.65 due to active exploitation)**:
```
Sector     | Updated Priority | Updated Score | Status Change
-----------|------------------|---------------|---------------------------
Energy     | NOW              | 8.9           | ESCALATED - Active exploitation detected
Water      | NOW              | 8.7           | ESCALATED - Active exploitation detected
Healthcare | NOW              | 8.1           | ESCALATED - Patient data at risk
Commercial | NEXT             | 6.8           | ESCALATED - Widespread exploitation observed
```

---

## Integration with McKenney Questions

### Question 3: What's Vulnerable?
**Enhancement**: Prioritize vulnerability lists by NOW/NEXT/NEVER categories

**Before Enhancement**:
```
Q3 Query returns: 9,000 CVEs affecting organization
```

**After Enhancement**:
```
Q3 Query returns:
- 127 NOW priorities (patch within 48 hours)
- 431 NEXT priorities (schedule for maintenance)
- 8,442 NEVER priorities (defer or accept risk)
```

### Question 8: What Should We Patch First?
**Enhancement**: Provide sector-specific, bias-aware prioritization

**Before Enhancement**:
```
Q8 Query returns: CVEs sorted by CVSS score only
```

**After Enhancement**:
```
Q8 Query returns:
1. CVE-2021-44228 (NOW) - Energy sector, Score 9.1, Override applied
2. CVE-2023-XXXXX (NOW) - Water sector, Score 8.7, Active exploitation
3. CVE-2024-YYYYY (NOW) - Healthcare, Score 8.4, Patient safety risk
...
[Automatically adjusts for organizational biases and sector risk tolerance]
```

### Question 10: How do we measure success?
**Enhancement**: Track prioritization effectiveness metrics

**New Metrics**:
- **Mean Time to Patch (MTTP)** by priority category:
  - NOW priorities: Target <48 hours
  - NEXT priorities: Target <30 days
  - NEVER priorities: Monitored but not patched

- **Prioritization Accuracy**: Percentage of NOW priorities that were exploited vs NEVER priorities that were exploited
  - Target: >90% of exploited CVEs were correctly flagged as NOW/NEXT

- **False Positive Rate**: Percentage of NOW priorities that remain unexploited after 90 days
  - Target: <15% false alarm rate

---

## Validation and Testing

### Test Case 1: Historical Validation
**Method**: Apply framework to historical CVEs with known exploitation timelines

**Test CVEs**:
- CVE-2021-44228 (Log4Shell) - Known exploitation within hours
- CVE-2017-0144 (EternalBlue) - Known exploitation within days
- CVE-2023-34362 (MOVEit) - Known exploitation within weeks

**Expected Results**:
- Framework should categorize all three as NOW for critical sectors
- EPSS scores should have indicated high exploitation probability
- Psychological factors for Energy/Water sectors should reinforce NOW priority

**Validation Query**:
```cypher
MATCH (cve:CVE)
WHERE cve.cveId IN ["CVE-2021-44228", "CVE-2017-0144", "CVE-2023-34362"]

MATCH (pa:PriorityAssessment)-[:ASSESSES]->(cve)
WHERE pa.sectorType IN ["Energy", "Water", "Healthcare"]

RETURN cve.cveId AS CVE,
       pa.sectorType AS Sector,
       pa.priorityCategory AS AssignedPriority,
       pa.combinedScore10Point AS Score,
       CASE
           WHEN pa.priorityCategory = "NOW" THEN "CORRECT"
           ELSE "MISSED CRITICAL VULNERABILITY"
       END AS ValidationResult
```

### Test Case 2: Cognitive Bias Sensitivity Analysis
**Method**: Test framework behavior under different organizational bias profiles

**Bias Profiles**:
1. **Low Bias Organization**: Fast patching, low risk tolerance, mature security culture
2. **Moderate Bias Organization**: Balanced approach, operational concerns
3. **High Bias Organization**: Slow patching, high normalcy bias, cost-focused

**Test CVE**: CVE-2024-TEST (CVSS 8.5, EPSS 0.55, Tier 1 equipment)

**Expected Results**:
- Low Bias Org → NOW priority (score ~8.3)
- Moderate Bias Org → NEXT priority (score ~6.8)
- High Bias Org → NEXT priority (score ~5.9), but with warning flag

**Validation**: Ensure psychological factors appropriately adjust technical scores without overriding critical vulnerabilities.

### Test Case 3: Sector Prediction Accuracy
**Method**: Compare framework predictions against actual sector responses to new CVEs

**Data Collection**:
- Track 50 new CVEs published in Q1 2025
- Record actual patch timelines by sector
- Compare against framework priority assignments

**Metrics**:
- **Precision**: % of NOW priorities that were patched within 48 hours
- **Recall**: % of vulnerabilities patched within 48 hours that were flagged as NOW
- **F1 Score**: Harmonic mean of precision and recall

**Target Performance**:
- Precision: ≥85%
- Recall: ≥90%
- F1 Score: ≥87%

---

## Performance Considerations

### Computational Complexity

**Priority Calculation**:
- **Time Complexity**: O(C × S × E)
  - C = CVE count (316,000)
  - S = Sector count (16)
  - E = Equipment per sector (avg 500)
  - Total: ~2.5 billion calculations

**Optimization Strategies**:

1. **Incremental Updates**: Only recalculate priorities when:
   - New CVE published
   - EPSS score updated (weekly)
   - Equipment criticality changed
   - Organizational profile updated

2. **Batch Processing**: Process CVEs in priority order:
   - High CVSS (≥9.0) processed first
   - Active EPSS (≥0.7) processed next
   - Remaining CVEs processed in background

3. **Caching**: Cache calculated scores for common queries:
   - Sector-level priorities cached for 24 hours
   - Equipment-specific priorities cached for 7 days
   - Organization priorities cached until profile changes

4. **Parallel Processing**: Distribute calculations across:
   - Sector-based sharding (16 parallel streams)
   - CVE severity ranges (4 parallel streams: Critical, High, Medium, Low)

### Storage Requirements

**Node Storage**:
- PriorityAssessment nodes: 316K CVEs × 16 sectors = **5.06 million nodes**
- Average node size: ~2 KB
- Total storage: ~10 GB for priority assessments

**Relationship Storage**:
- Relationships per assessment: 5 (ASSESSES, APPLIES_TO, FOR_ORGANIZATION, INFLUENCED_BY, IN_SECTOR)
- Total relationships: 5.06M × 5 = **25.3 million relationships**
- Average relationship size: ~100 bytes
- Total storage: ~2.5 GB for relationships

**Total Storage Overhead**: ~12.5 GB (manageable for Neo4j Enterprise)

---

## Deployment Strategy

### Phase 1: Proof of Concept (Weeks 1-2)
**Scope**: Implement framework for single sector (Energy) with 100 test CVEs

**Deliverables**:
- PriorityAssessment node schema
- Basic scoring algorithm implementation
- 100 historical CVEs with known exploitation data
- Validation against actual Energy sector breach timelines

**Success Criteria**:
- Framework correctly categorizes ≥85% of exploited CVEs as NOW/NEXT
- ≤15% false positive rate for NOW category
- Query performance <5 seconds for 100 CVEs

### Phase 2: Multi-Sector Validation (Weeks 3-4)
**Scope**: Expand to 5 sectors (Energy, Water, Healthcare, Commercial, Defense) with 1,000 CVEs

**Deliverables**:
- Sector-specific organizational profiles
- Cognitive bias integration
- Bulk prioritization queries
- Comparative sector analysis reports

**Success Criteria**:
- Accurate sector differentiation (e.g., Energy NOW ≠ Commercial NOW)
- Psychological factors demonstrably influence priorities
- Query performance <30 seconds for 1,000 CVEs across 5 sectors

### Phase 3: Full Deployment (Weeks 5-8)
**Scope**: Deploy framework for all 316,000 CVEs across 16 sectors

**Deliverables**:
- Complete PriorityAssessment node graph (5.06M nodes)
- Automated daily EPSS updates
- Integration with McKenney Question queries
- Dashboards and reporting tools

**Success Criteria**:
- All CVEs categorized within 24 hours of publication
- Real-time priority updates based on EPSS changes
- Query performance <60 seconds for organization-wide prioritization

### Phase 4: Continuous Improvement (Ongoing)
**Scope**: Machine learning enhancements and feedback loops

**Deliverables**:
- ML model for EPSS prediction refinement
- Automated bias detection from patch behavior
- Continuous validation against breach data
- Quarterly accuracy reports

**Success Criteria**:
- Prediction accuracy improves ≥5% per quarter
- False positive rate decreases ≤10% per quarter
- Framework adoption by ≥80% of organizations

---

## Future Enhancements

### Enhancement 1: Machine Learning EPSS Refinement
**Description**: Train ML model to predict EPSS score evolution based on CVE characteristics and historical exploitation patterns.

**Data Sources**:
- Historical EPSS scores (2021-present)
- CVE metadata (attack vector, complexity, privileges required)
- Exploit availability (Exploit-DB, Metasploit)
- Threat actor activity (MITRE ATT&CK)

**Expected Benefit**: Improve NOW/NEXT predictions by 15-20% through earlier detection of exploitation trends.

### Enhancement 2: Real-Time Threat Intelligence Integration
**Description**: Integrate live threat feeds (e.g., CISA KEV, AlienVault OTX) to dynamically adjust priorities.

**Implementation**:
```cypher
// Real-time threat feed ingestion
MATCH (cve:CVE {cveId: $cveId})
MATCH (pa:PriorityAssessment)-[:ASSESSES]->(cve)

// Update EPSS based on active exploitation
SET cve.epssScore = $newEpssScore,
    cve.cisaKevListed = true,
    cve.activeExploitationConfirmed = true,
    pa.priorityCategory = "NOW",
    pa.lastUpdated = datetime()

RETURN pa.priorityCategory AS UpdatedPriority
```

### Enhancement 3: Automated Compensating Control Recommendations
**Description**: Suggest network segmentation, IDS rules, or firewall policies for NEXT/NEVER priorities.

**Example Output**:
```
CVE-2024-XXXXX (NEXT Priority)
Compensating Controls:
- Network Segmentation: Isolate affected systems on VLAN 100
- IDS Rule: Snort signature SID 1234567 (blocks exploit traffic)
- Firewall Policy: Block inbound traffic on TCP port 8080 from internet
- Monitoring: Alert on failed authentication attempts >10 per hour
```

### Enhancement 4: Collaborative Filtering for Sector Benchmarking
**Description**: Use collaborative filtering to recommend priorities based on similar organizations' patch behavior.

**Logic**: "Organizations in Energy sector with similar equipment profiles typically patch CVE-X within 3 days. Your organization's 30-day patch window is an outlier."

---

## References

### Academic Sources
- **EPSS Framework**: Jay Jacobs, Sasha Romanosky, Benjamin Edwards, Michael Roytman, Idris Adjerid. "Enhancing Vulnerability Prioritization: Data-Driven Exploit Predictions with Community-Driven Insights." *Digital Threats: Research and Practice*, 2021.

- **Cognitive Biases in Cybersecurity**: Deanna D. Caputo, Shari Lawrence Pfleeger, Jesse D. Freeman, M. Eric Johnson. "Going Spear Phishing: Exploring Embedded Training and Awareness." *IEEE Security & Privacy*, 2014.

- **Normalcy Bias**: Neil D. Weinstein. "Unrealistic Optimism About Future Life Events." *Journal of Personality and Social Psychology*, 1980.

- **Risk Perception**: Paul Slovic. "Perception of Risk." *Science*, 1987.

### Industry Standards
- **CVSS**: Common Vulnerability Scoring System, FIRST.org
- **EPSS**: Exploit Prediction Scoring System, FIRST.org
- **CISA KEV**: Known Exploited Vulnerabilities Catalog
- **NIST SP 800-40**: Guide to Enterprise Patch Management Technologies

---

## Appendices

### Appendix A: Equipment Criticality Classification

**Tier 1 - Critical (Criticality Weight: 1.0)**:
- Power generation and distribution systems
- Water treatment and distribution controls
- Emergency response communication systems
- Patient life support equipment
- Nuclear reactor safety systems
- Air traffic control systems

**Tier 2 - Important (Criticality Weight: 0.7)**:
- Business-critical application servers
- Financial transaction processing systems
- Manufacturing control systems (non-safety)
- Building management systems
- IT infrastructure (DNS, Active Directory)

**Tier 3 - Standard (Criticality Weight: 0.4)**:
- Development and test environments
- Office productivity systems
- Non-critical business applications
- Guest wireless networks
- End-user workstations

### Appendix B: Cognitive Bias Catalog

**High Impact Biases** (Severity ≥0.7):
- Normalcy Bias: "It won't happen to us"
- Optimism Bias: "We're more secure than average"
- Sunk Cost Fallacy: "We've invested too much to change now"

**Moderate Impact Biases** (Severity 0.4-0.7):
- Availability Heuristic: Recent events disproportionately influential
- Confirmation Bias: Seek information confirming existing beliefs
- Status Quo Bias: Resistance to change

**Low Impact Biases** (Severity <0.4):
- Anchoring: Over-rely on first piece of information
- Recency Bias: Overweight recent information

### Appendix C: Sector Risk Tolerance Profiles

**Zero Tolerance Sectors** (Inverse Score: 1.0):
- Energy (power grid)
- Water/Wastewater
- Nuclear facilities
- Defense/Military

**Low Tolerance Sectors** (Inverse Score: 0.8):
- Healthcare (patient safety)
- Financial services (regulatory requirements)
- Transportation (aviation, rail)

**Moderate Tolerance Sectors** (Inverse Score: 0.65):
- Healthcare (administrative systems)
- Manufacturing (non-safety)
- Government (civilian)

**High Tolerance Sectors** (Inverse Score: 0.3):
- Commercial facilities
- Retail
- Hospitality
- Small business

---

**END OF README.md**

**Document Version**: 1.0.0
**Total Lines**: 847
**Status**: COMPLETE - Ready for TASKMASTER and implementation
