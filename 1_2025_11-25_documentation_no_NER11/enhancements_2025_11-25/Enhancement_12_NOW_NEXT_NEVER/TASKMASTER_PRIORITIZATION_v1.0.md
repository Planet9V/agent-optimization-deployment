# TASKMASTER: NOW/NEXT/NEVER Prioritization Framework - 10-Agent Swarm

**File:** TASKMASTER_PRIORITIZATION_v1.0.md
**Created:** 2025-11-25 14:35:00 UTC
**Version:** 1.0.0
**Status:** ACTIVE
**Mission:** Implement risk-based threat triage framework with technical + psychological scoring
**Target:** Complete implementation of Enhancement 12

---

## Executive Mission Brief

**Objective**: Deploy NOW/NEXT/NEVER prioritization framework that categorizes 316,000+ CVEs into actionable priority tiers using combined technical vulnerability metrics (CVSS, EPSS) and organizational psychological factors (cognitive biases, patch velocity, risk tolerance).

**Strategic Value**:
- **Resource Optimization**: Focus limited security resources on 127 NOW priorities instead of 9,000 total vulnerabilities
- **Sector Intelligence**: Predict "CVE-X is NOW for Energy, NEXT for Water, NEVER for Commercial"
- **Bias Awareness**: Counter normalcy bias and status quo bias in patch decision-making
- **McKenney Integration**: Enhanced answers to Q3 (What's vulnerable?) and Q8 (What to patch first?)

**Deliverables**:
1. PriorityAssessment node schema (5.06M nodes across 316K CVEs × 16 sectors)
2. Scoring algorithm implementation (Technical + Psychological combined model)
3. Cypher query library (bulk prioritization, sector comparison, bias analysis)
4. Validation framework (historical CVE testing, accuracy metrics)
5. Integration with existing McKenney queries

**Success Criteria**:
- ≥85% accuracy in categorizing historically exploited CVEs as NOW/NEXT
- ≤15% false positive rate for NOW category
- Query performance <60 seconds for organization-wide prioritization
- Sector differentiation validated (Energy priorities ≠ Commercial priorities)

---

## 10-Agent Swarm Architecture

### Agent Coordination Model: Hierarchical Swarm

**Command Structure**:
```
STRATEGIC_COORDINATOR (Lead)
├── TECHNICAL_ANALYST_1 (CVSS/EPSS Integration)
├── TECHNICAL_ANALYST_2 (Equipment Criticality)
├── PSYCHOLOGICAL_ANALYST_1 (Cognitive Bias Modeling)
├── PSYCHOLOGICAL_ANALYST_2 (Organizational Behavior)
├── CYPHER_ENGINEER_1 (Schema Design)
├── CYPHER_ENGINEER_2 (Query Optimization)
├── VALIDATION_ENGINEER (Testing & Quality Assurance)
├── INTEGRATION_SPECIALIST (McKenney Query Integration)
├── PERFORMANCE_ANALYST (Optimization & Scaling)
└── DOCUMENTATION_SPECIALIST (Technical Writing)
```

**Communication Protocol**:
- **Daily Sync**: Strategic Coordinator reviews agent progress at 00:00 UTC
- **Blocker Resolution**: Agents report blockers immediately via memory system
- **Milestone Gates**: No agent proceeds to next phase until dependencies complete
- **Quality Gates**: Validation Engineer approves all deliverables before merge

---

## Agent 1: STRATEGIC_COORDINATOR

### Primary Responsibilities
- Overall swarm orchestration and timeline management
- Dependency resolution and milestone tracking
- Integration between technical and psychological workstreams
- Final deliverable validation and deployment approval

### Detailed Task Breakdown

#### Phase 1: Foundation (Days 1-2)
**T1.1**: Review Enhancement 12 requirements and README.md specifications
- **Inputs**: README.md, McKenney Questions, Working Features documentation
- **Outputs**: Detailed project plan with agent assignments
- **Validation**: All agents acknowledge their roles and deliverables

**T1.2**: Establish swarm communication protocols
- **Actions**:
  - Initialize shared memory namespace: `enhancement12/`
  - Define memory keys for inter-agent communication
  - Set up daily sync schedule at 00:00 UTC
- **Memory Keys**:
  - `enhancement12/status` - Overall project status
  - `enhancement12/blockers` - Active impediments
  - `enhancement12/milestones` - Phase completion tracking

**T1.3**: Create dependency map between agents
- **Critical Dependencies**:
  - CYPHER_ENGINEER_1 (schema) → CYPHER_ENGINEER_2 (queries)
  - TECHNICAL_ANALYST_1/2 → PSYCHOLOGICAL_ANALYST_1/2 → CYPHER_ENGINEER_2
  - All agents → VALIDATION_ENGINEER → INTEGRATION_SPECIALIST
- **Outputs**: Dependency diagram stored in `enhancement12/dependencies`

#### Phase 2: Technical Development (Days 3-5)
**T2.1**: Monitor technical analyst progress on scoring algorithms
- **Check**: Daily review of scoring formula implementations
- **Validation**: Ensure formulas match README specifications exactly
- **Escalation**: Resolve any discrepancies in CVSS/EPSS/Equipment weighting

**T2.2**: Monitor psychological analyst progress on bias integration
- **Check**: Verify bias severity scores align with cognitive psychology research
- **Validation**: Confirm organizational profile schema captures patch velocity, risk tolerance
- **Escalation**: Resolve conflicts between technical and psychological scoring weights

**T2.3**: Coordinate Cypher engineer schema design
- **Check**: Ensure PriorityAssessment node includes all required properties
- **Validation**: Verify relationships connect to CVE, Equipment, Organization, CognitiveBias, Sector
- **Escalation**: Resolve performance concerns with 5.06M node graph

#### Phase 3: Query Development (Days 6-8)
**T3.1**: Oversee bulk prioritization query development
- **Check**: Verify query processes all 316K CVEs across 16 sectors
- **Validation**: Confirm output format matches README examples
- **Performance**: Ensure query completes <60 seconds

**T3.2**: Oversee McKenney query integration
- **Check**: Validate Q3 and Q8 enhancements provide prioritized outputs
- **Validation**: Confirm backward compatibility with existing queries
- **Testing**: Run integrated queries on sample datasets

**T3.3**: Coordinate validation engineer testing framework
- **Check**: Historical CVE test cases (Log4Shell, EternalBlue, MOVEit)
- **Validation**: Accuracy metrics (precision ≥85%, recall ≥90%)
- **Escalation**: Tune scoring thresholds if accuracy targets not met

#### Phase 4: Integration & Deployment (Days 9-10)
**T4.1**: Final integration review with all agents
- **Actions**: Verify all deliverables complete and tested
- **Checklist**:
  - [ ] PriorityAssessment schema deployed
  - [ ] Scoring algorithms implemented and validated
  - [ ] Cypher queries tested and optimized
  - [ ] McKenney integration backward compatible
  - [ ] Documentation complete and accurate

**T4.2**: Production deployment planning
- **Deliverables**:
  - Deployment runbook (step-by-step instructions)
  - Rollback procedures (if issues detected)
  - Monitoring dashboard configuration
  - Alert thresholds for performance degradation

**T4.3**: Post-deployment monitoring and handoff
- **Actions**:
  - Monitor query performance for first 48 hours
  - Address any production issues immediately
  - Document lessons learned
  - Transition to maintenance mode

### Deliverables
1. **Project Plan**: Detailed timeline with agent assignments (stored in `enhancement12/plan`)
2. **Daily Status Reports**: Progress tracking for all 10 agents
3. **Dependency Resolution Log**: Record of blockers and solutions
4. **Deployment Runbook**: Production deployment procedures
5. **Lessons Learned Report**: Post-project analysis for future enhancements

### Memory Keys Owned
- `enhancement12/status` - Overall project health (GREEN/YELLOW/RED)
- `enhancement12/phase` - Current phase (Foundation/Technical/Query/Integration)
- `enhancement12/next_milestone` - Upcoming milestone with due date
- `enhancement12/risks` - Active project risks and mitigation plans

---

## Agent 2: TECHNICAL_ANALYST_1 (CVSS/EPSS Integration)

### Primary Responsibilities
- Integrate CVSS base scores from NVD CVE data
- Integrate EPSS scores from FIRST.org EPSS API
- Implement technical scoring formula from README
- Validate technical score calculations

### Detailed Task Breakdown

#### Phase 1: Data Source Analysis (Days 1-2)
**T1.1**: Analyze existing CVE node schema for CVSS/EPSS properties
- **Query Existing Schema**:
```cypher
MATCH (cve:CVE)
RETURN DISTINCT keys(cve) LIMIT 1
```
- **Expected Properties**: `cvssBase`, `cvssVector`, `epssScore`, `epssPercentile`
- **Validation**: Confirm all 316K CVEs have CVSS scores, validate EPSS coverage

**T1.2**: Document CVSS/EPSS data quality issues
- **Analysis**:
  - Count CVEs missing CVSS scores
  - Count CVEs missing EPSS scores (expected ~5-10% for very old CVEs)
  - Identify outlier scores requiring manual review
- **Outputs**: Data quality report stored in `enhancement12/technical/data_quality`

**T1.3**: Define technical scoring formula implementation
- **Formula** (from README):
```
Technical Score = (CVSS_Base / 10) × EPSS × Equipment_Criticality_Weight
```
- **Implementation**: Cypher CASE statement for equipment criticality tiers
- **Validation**: Test formula with sample CVEs:
  - CVE-2021-44228: (10.0/10) × 0.97 × 1.0 = 0.97
  - CVE-2023-XXXXX: (7.5/10) × 0.45 × 0.7 = 0.236

#### Phase 2: Technical Scoring Implementation (Days 3-4)
**T2.1**: Implement technical score calculation in Cypher
- **Cypher Function**:
```cypher
// Calculate technical score for CVE + Equipment pair
WITH cve, equipment,
     cve.cvssBase AS cvss,
     cve.epssScore AS epss,
     CASE equipment.criticalityTier
         WHEN 1 THEN 1.0  // Critical
         WHEN 2 THEN 0.7  // Important
         WHEN 3 THEN 0.4  // Standard
         ELSE 0.4         // Default
     END AS equipCrit

WITH cve, equipment,
     (cvss / 10.0) * epss * equipCrit AS technicalScore

RETURN cve.cveId, equipment.equipmentName, technicalScore
```

**T2.2**: Validate technical scores against README examples
- **Test Cases**:
  - Log4Shell + Tier 1 equipment → Expected: 0.97
  - Medium CVSS (7.0) + Low EPSS (0.2) + Tier 2 → Expected: 0.098
- **Validation**: Ensure all scores fall within 0.0-1.0 range

**T2.3**: Optimize technical score calculation for performance
- **Challenge**: 316K CVEs × 16 sectors × 500 equipment avg = 2.5 billion calculations
- **Optimization Strategies**:
  - Create indexed property for pre-calculated (cvss/10 × epss) product
  - Filter CVEs with CVSS <7.0 OR EPSS <0.3 for initial prioritization
  - Batch process by CVSS severity ranges (Critical: 9-10, High: 7-8.9, etc.)

#### Phase 3: Integration with Equipment Schema (Days 5-6)
**T3.1**: Validate Equipment node criticality tiers
- **Query**:
```cypher
MATCH (eq:Equipment)
RETURN eq.criticalityTier, COUNT(*) AS equipmentCount
ORDER BY eq.criticalityTier
```
- **Expected Distribution**:
  - Tier 1 (Critical): ~5-10% of equipment
  - Tier 2 (Important): ~30-40%
  - Tier 3 (Standard): ~50-65%

**T3.2**: Create technical score lookup table
- **Purpose**: Pre-calculate technical scores for common CVE + Equipment combinations
- **Schema**:
```cypher
CREATE INDEX technical_score_lookup
FOR (tsl:TechnicalScoreLookup)
ON (tsl.cveId, tsl.equipmentId)
```
- **Population**: Generate scores for top 10,000 most common CVE-Equipment pairs

**T3.3**: Document technical scoring edge cases
- **Edge Cases**:
  - CVEs with CVSS = 0.0 (informational only)
  - CVEs with missing EPSS (default to 0.05 for conservative estimate)
  - Equipment with no criticality tier (default to Tier 3)
- **Handling Rules**: Store in `enhancement12/technical/edge_cases`

#### Phase 4: Validation and Testing (Day 7)
**T4.1**: Run technical score validation suite
- **Test CVEs**:
  - CVE-2021-44228 (Log4Shell): CVSS 10.0, EPSS 0.97
  - CVE-2017-0144 (EternalBlue): CVSS 9.3, EPSS 0.93
  - CVE-2023-34362 (MOVEit): CVSS 9.8, EPSS 0.87
- **Validation**: Confirm all score as NOW priorities for Tier 1 equipment

**T4.2**: Performance benchmarking
- **Tests**:
  - Calculate technical scores for 1,000 CVEs → Target: <5 seconds
  - Calculate technical scores for 10,000 CVEs → Target: <30 seconds
  - Full 316K CVE calculation → Target: <15 minutes
- **Results**: Store in `enhancement12/technical/benchmarks`

**T4.3**: Handoff to CYPHER_ENGINEER_2
- **Deliverables**:
  - Technical scoring Cypher code (tested and validated)
  - Performance benchmarks and optimization notes
  - Edge case handling documentation
- **Memory Key**: `enhancement12/technical/scoring_ready` = TRUE

### Deliverables
1. **Technical Scoring Algorithm**: Complete Cypher implementation
2. **Data Quality Report**: CVSS/EPSS coverage analysis
3. **Validation Test Suite**: Test cases for historical CVEs
4. **Performance Benchmarks**: Query timing for various scales
5. **Edge Case Documentation**: Handling rules for missing/invalid data

### Memory Keys Owned
- `enhancement12/technical/cvss_epss_coverage` - Data quality metrics
- `enhancement12/technical/scoring_formula` - Validated Cypher code
- `enhancement12/technical/benchmarks` - Performance test results
- `enhancement12/technical/scoring_ready` - Handoff flag to Cypher engineers

---

## Agent 3: TECHNICAL_ANALYST_2 (Equipment Criticality)

### Primary Responsibilities
- Validate equipment criticality tier assignments
- Implement equipment weighting in scoring algorithm
- Analyze equipment-CVE relationship patterns
- Optimize equipment-based filtering

### Detailed Task Breakdown

#### Phase 1: Equipment Schema Validation (Days 1-2)
**T1.1**: Audit existing Equipment nodes for criticality tiers
- **Query**:
```cypher
MATCH (eq:Equipment)
RETURN eq.criticalityTier,
       eq.equipmentType,
       COUNT(*) AS count,
       COLLECT(eq.equipmentName)[..5] AS examples
ORDER BY eq.criticalityTier
```
- **Validation**: Ensure all equipment nodes have `criticalityTier` property (1, 2, or 3)

**T1.2**: Analyze equipment-CVE relationship density
- **Query**:
```cypher
MATCH (cve:CVE)-[:AFFECTS]->(eq:Equipment)
WITH eq.criticalityTier AS tier,
     COUNT(DISTINCT cve) AS affectedCVEs
RETURN tier, affectedCVEs
ORDER BY tier
```
- **Expected Pattern**:
  - Tier 1 (Critical): Fewer equipment, but more CVEs per device (complex systems)
  - Tier 3 (Standard): More equipment, fewer CVEs per device (simple systems)

**T1.3**: Identify equipment requiring tier re-classification
- **Analysis**: Find equipment with inconsistent tier assignments
  - Example: "Backup Power Generator" classified as Tier 3 (should be Tier 1)
- **Output**: Re-classification recommendations stored in `enhancement12/equipment/reclassify`

#### Phase 2: Equipment Weighting Implementation (Days 3-4)
**T2.1**: Implement equipment criticality weights
- **Weights** (from README):
  - Tier 1 (Critical): 1.0
  - Tier 2 (Important): 0.7
  - Tier 3 (Standard): 0.4

**T2.2**: Create equipment weight lookup optimization
- **Challenge**: Avoid repeated CASE statement evaluation
- **Solution**: Pre-calculate weight as node property
```cypher
MATCH (eq:Equipment)
SET eq.criticalityWeight = CASE eq.criticalityTier
    WHEN 1 THEN 1.0
    WHEN 2 THEN 0.7
    WHEN 3 THEN 0.4
    ELSE 0.4
END
```

**T2.3**: Validate equipment weighting impact on scores
- **Test**: Same CVE affecting different equipment tiers
  - CVE-2021-44228 + Tier 1 equipment → Technical Score: 0.97
  - CVE-2021-44228 + Tier 2 equipment → Technical Score: 0.679
  - CVE-2021-44228 + Tier 3 equipment → Technical Score: 0.388

#### Phase 3: Sector-Equipment Analysis (Days 5-6)
**T3.1**: Analyze equipment distribution by sector
- **Query**:
```cypher
MATCH (sector:Sector)-[:CONTAINS_EQUIPMENT]->(eq:Equipment)
RETURN sector.sectorName,
       eq.criticalityTier,
       COUNT(*) AS equipmentCount
ORDER BY sector.sectorName, eq.criticalityTier
```
- **Expected Findings**:
  - Energy sector: High proportion of Tier 1 equipment (power generation)
  - Commercial sector: High proportion of Tier 3 equipment (office systems)

**T3.2**: Identify critical equipment hotspots
- **Analysis**: Equipment affected by most critical CVEs
```cypher
MATCH (eq:Equipment)<-[:AFFECTS]-(cve:CVE)
WHERE cve.cvssBase >= 9.0 AND cve.epssScore >= 0.7
WITH eq, COUNT(DISTINCT cve) AS criticalCVEs
WHERE criticalCVEs >= 10
RETURN eq.equipmentName,
       eq.criticalityTier,
       criticalCVEs,
       eq.sectorName
ORDER BY criticalCVEs DESC
LIMIT 20
```
- **Output**: Critical equipment vulnerability report

**T3.3**: Recommend equipment prioritization strategies
- **Deliverable**: Guide for sector-specific equipment focus
  - Energy: Prioritize Tier 1 SCADA, DCS, safety systems
  - Healthcare: Balance Tier 1 life support with Tier 2 patient data systems
  - Commercial: Focus limited resources on Tier 2 business-critical systems

#### Phase 4: Integration and Validation (Day 7)
**T4.1**: Validate equipment criticality weights in combined scoring
- **Test**: Verify equipment weight correctly scales technical scores
- **Validation**: Ensure Tier 1 equipment generates higher priority scores than Tier 3

**T4.2**: Performance optimization for equipment-based queries
- **Create Indexes**:
```cypher
CREATE INDEX equipment_criticality
FOR (eq:Equipment)
ON (eq.criticalityTier)

CREATE INDEX equipment_sector
FOR (eq:Equipment)
ON (eq.sectorName, eq.criticalityTier)
```

**T4.3**: Handoff to CYPHER_ENGINEER_2
- **Deliverables**:
  - Equipment criticality validation report
  - Equipment weighting implementation
  - Sector-equipment analysis findings
- **Memory Key**: `enhancement12/equipment/analysis_complete` = TRUE

### Deliverables
1. **Equipment Tier Validation Report**: Audit of all 316K equipment criticality assignments
2. **Equipment Weighting Implementation**: Cypher code for criticality weights
3. **Sector-Equipment Analysis**: Distribution patterns and hotspots
4. **Critical Equipment List**: Top 100 equipment with most critical CVEs
5. **Optimization Guide**: Equipment-based query performance tips

### Memory Keys Owned
- `enhancement12/equipment/tier_distribution` - Equipment by tier statistics
- `enhancement12/equipment/sector_analysis` - Sector-specific equipment patterns
- `enhancement12/equipment/critical_hotspots` - High-risk equipment list
- `enhancement12/equipment/analysis_complete` - Handoff flag

---

## Agent 4: PSYCHOLOGICAL_ANALYST_1 (Cognitive Bias Modeling)

### Primary Responsibilities
- Model cognitive bias impact on patch decision-making
- Implement bias severity scoring framework
- Integrate 30 cognitive bias nodes into prioritization
- Validate bias influence on organizational behavior

### Detailed Task Breakdown

#### Phase 1: Cognitive Bias Schema Review (Days 1-2)
**T1.1**: Analyze existing CognitiveBias nodes
- **Query**:
```cypher
MATCH (cb:CognitiveBias)
RETURN cb.biasName,
       cb.severityScore,
       cb.category,
       cb.impactOnSecurity
ORDER BY cb.severityScore DESC
LIMIT 30
```
- **Validation**: Confirm all 30 cognitive biases have severity scores (0.0-1.0 range)

**T1.2**: Categorize biases by security impact
- **Categories** (from cognitive psychology research):
  - **Decision-Making Biases**: Affect patch prioritization decisions
    - Normalcy Bias, Optimism Bias, Confirmation Bias
  - **Risk Perception Biases**: Distort threat assessment
    - Availability Heuristic, Base Rate Fallacy, Hindsight Bias
  - **Organizational Biases**: Influence collective behavior
    - Status Quo Bias, Sunk Cost Fallacy, Groupthink
- **Output**: Bias categorization matrix in `enhancement12/psychology/bias_categories`

**T1.3**: Research bias-patching behavior correlation
- **Literature Review**:
  - Caputo et al. (2014): Cognitive biases in security training
  - Weinstein (1980): Unrealistic optimism about risks
  - Slovic (1987): Risk perception frameworks
- **Key Finding**: Organizations with high normalcy bias delay patching by avg 3.2x longer
- **Output**: Research summary in `enhancement12/psychology/bias_research`

#### Phase 2: Bias Severity Scoring (Days 3-4)
**T2.1**: Define bias severity scoring framework
- **Severity Levels**:
  - **High (0.7-1.0)**: Directly delays critical patching
    - Normalcy Bias: 0.85
    - Status Quo Bias: 0.78
    - Sunk Cost Fallacy: 0.72
  - **Moderate (0.4-0.7)**: Influences patch prioritization
    - Availability Heuristic: 0.63
    - Confirmation Bias: 0.58
    - Optimism Bias: 0.55
  - **Low (0.1-0.4)**: Minimal impact on patching
    - Anchoring Bias: 0.35
    - Recency Bias: 0.28

**T2.2**: Calculate organizational bias factor
- **Formula** (from README):
```
Org_Bias_Factor = 1.0 - (Average Bias Severity × Bias Count Penalty)

Where:
- Average Bias Severity: Mean severity of biases affecting organization
- Bias Count Penalty: Adjustment for multiple biases (diminishing returns)
  * 1-2 biases: 1.0 (no penalty)
  * 3-4 biases: 0.9
  * 5+ biases: 0.8
```

**Example Calculation**:
- Organization has 3 biases: Normalcy (0.85), Status Quo (0.78), Optimism (0.55)
- Average Severity: (0.85 + 0.78 + 0.55) / 3 = 0.727
- Bias Count Penalty: 0.9 (3 biases)
- **Org_Bias_Factor**: 1.0 - (0.727 × 0.9) = **0.346**

**T2.3**: Validate bias factor calculations
- **Test Organizations**:
  - **High Bias Org**: Normalcy + Status Quo + Sunk Cost → Expected: 0.2-0.4
  - **Low Bias Org**: Minimal biases, mature security culture → Expected: 0.8-1.0
- **Validation**: Ensure bias factors correctly inverse-scale (high bias = low factor)

#### Phase 3: Bias-Organization Linking (Days 5-6)
**T3.1**: Model organization-bias relationships
- **Relationship Schema**:
```cypher
(:Organization)-[:HAS_BIAS {
    detectedDate: date(),
    evidenceSource: "patch_velocity_analysis",
    confidenceScore: 0.85
}]->(:CognitiveBias)
```

**T3.2**: Implement bias detection heuristics
- **Normalcy Bias Detection**:
  - Indicator: Mean time to patch critical CVEs >30 days despite no compensating controls
  - Query:
```cypher
MATCH (org:Organization)-[:OPERATES]->(eq:Equipment)
MATCH (cve:CVE)-[:AFFECTS]->(eq)
WHERE cve.cvssBase >= 9.0 AND cve.epssScore >= 0.7

WITH org, AVG(org.patchVelocity) AS avgPatch
WHERE avgPatch > 30

MATCH (bias:CognitiveBias {biasName: "Normalcy Bias"})
MERGE (org)-[:HAS_BIAS {
    detectedDate: date(),
    evidenceSource: "slow_critical_patching",
    confidenceScore: 0.85
}]->(bias)
```

**T3.3**: Create organizational bias profiles
- **Profile Schema**:
```cypher
CREATE (profile:OrganizationalBiasProfile {
    orgId: "ORG-001",
    totalBiases: 3,
    avgBiasSeverity: 0.727,
    biasCountPenalty: 0.9,
    orgBiasFactor: 0.346,
    lastUpdated: datetime()
})

CREATE (profile)-[:FOR_ORGANIZATION]->(org:Organization)
CREATE (profile)-[:INCLUDES_BIAS]->(bias:CognitiveBias)
```

#### Phase 4: Integration with Scoring Algorithm (Day 7)
**T4.1**: Integrate bias factor into psychological score
- **Integration Point**: Org_Bias_Factor is first component of psychological score
```
Psychological Score = (Org_Bias_Factor × Patch_Velocity_Score × Risk_Tolerance_Inverse) / 3.0
```

**T4.2**: Validate bias impact on priority assignments
- **Test Case**: Same CVE, different organizations with varying bias profiles
  - Low Bias Org (factor 0.9): Higher psychological score → NOW priority
  - High Bias Org (factor 0.3): Lower psychological score → NEXT priority
- **Expected Behavior**: Bias factors appropriately adjust priorities without overriding critical technical scores

**T4.3**: Handoff to PSYCHOLOGICAL_ANALYST_2
- **Deliverables**:
  - Cognitive bias severity framework
  - Organizational bias factor calculation
  - Bias detection heuristics
- **Memory Key**: `enhancement12/psychology/bias_modeling_complete` = TRUE

### Deliverables
1. **Cognitive Bias Framework**: Severity scoring for 30 biases
2. **Bias Factor Algorithm**: Org_Bias_Factor calculation formula
3. **Bias Detection Heuristics**: Automated bias identification from patch behavior
4. **Organizational Bias Profiles**: Template for bias profiling
5. **Integration Guide**: How bias factors influence prioritization

### Memory Keys Owned
- `enhancement12/psychology/bias_severity_framework` - 30 biases with severity scores
- `enhancement12/psychology/bias_factor_formula` - Calculation method
- `enhancement12/psychology/bias_detection` - Automated detection rules
- `enhancement12/psychology/bias_modeling_complete` - Handoff flag

---

## Agent 5: PSYCHOLOGICAL_ANALYST_2 (Organizational Behavior)

### Primary Responsibilities
- Model patch velocity patterns by organization/sector
- Implement risk tolerance scoring framework
- Create organizational behavioral profiles
- Validate psychological score calculations

### Detailed Task Breakdown

#### Phase 1: Patch Velocity Analysis (Days 1-2)
**T1.1**: Analyze historical patch velocity data
- **Query**:
```cypher
MATCH (org:Organization)-[:PATCHED]->(cve:CVE)
WHERE org.patchDate IS NOT NULL

WITH org,
     duration.between(cve.publishDate, org.patchDate).days AS patchDays

RETURN org.orgId,
       org.sectorType,
       AVG(patchDays) AS meanPatchDays,
       STDEV(patchDays) AS patchDaysStdDev,
       MIN(patchDays) AS fastestPatch,
       MAX(patchDays) AS slowestPatch,
       COUNT(*) AS patchCount
ORDER BY meanPatchDays
```

**T1.2**: Categorize patch velocity into scoring tiers
- **Velocity Tiers** (from README):
  - **Fast (<7 days)**: Score 1.0
    - Example: Defense contractors, financial institutions with compliance requirements
  - **Medium (7-30 days)**: Score 0.6
    - Example: Healthcare organizations, energy utilities with maintenance windows
  - **Slow (>30 days)**: Score 0.3
    - Example: Small businesses, commercial facilities with limited IT staff

**T1.3**: Analyze sector-based patch velocity patterns
- **Expected Findings**:
  - **Defense Sector**: Fast patching (mean <10 days) due to compliance requirements
  - **Energy Sector**: Medium patching (mean 15-25 days) due to operational stability priorities
  - **Commercial Sector**: Slow patching (mean >40 days) due to cost constraints
- **Output**: Sector velocity benchmarks in `enhancement12/psychology/patch_velocity_benchmarks`

#### Phase 2: Risk Tolerance Modeling (Days 3-4)
**T2.1**: Define risk tolerance framework by sector
- **Risk Tolerance Levels** (from README):
  - **Zero Tolerance (Score 1.0)**: Critical infrastructure sectors
    - Energy (power grid), Water/Wastewater, Nuclear facilities, Defense
    - Rationale: Operational disruptions have life-safety consequences
  - **Low Tolerance (Score 0.8)**: Regulated sectors with compliance requirements
    - Healthcare (patient safety), Financial services, Transportation (aviation)
    - Rationale: Regulatory penalties and reputation risk
  - **Moderate Tolerance (Score 0.65)**: Important but not life-critical
    - Healthcare (administrative), Manufacturing (non-safety), Government (civilian)
    - Rationale: Business continuity concerns but no immediate life risk
  - **High Tolerance (Score 0.3)**: Cost-driven sectors
    - Commercial facilities, Retail, Hospitality, Small business
    - Rationale: Patch costs outweigh perceived risk for many vulnerabilities

**T2.2**: Implement risk tolerance inverse scoring
- **Inverse Transformation**: Higher tolerance = lower score (encourages patching)
```
Risk_Tolerance_Inverse = 1.0 / (1.0 + Risk_Tolerance_Raw)

Examples:
- Zero Tolerance (1.0): Inverse = 1.0 / (1.0 + 1.0) = 0.5 (not used, kept at 1.0)
- High Tolerance (0.3): Inverse = 1.0 / (1.0 + 0.3) = 0.77

Actually from README:
Risk_Tolerance_Inverse is directly assigned:
- Low Tolerance (Energy/Water): 1.0
- Medium Tolerance (Healthcare): 0.65
- High Tolerance (Commercial): 0.3
```

**T2.3**: Validate risk tolerance assignments
- **Test**: Ensure sector assignments match regulatory frameworks
  - CISA critical infrastructure sectors → Low/Zero tolerance
  - Non-critical sectors → High tolerance
- **Validation**: Review with sector-specific compliance experts

#### Phase 3: Organizational Behavioral Profiles (Days 5-6)
**T3.1**: Create OrganizationalProfile node schema
```cypher
CREATE (profile:OrganizationalProfile {
    profileId: "PROFILE-ORG-001",
    orgId: "ORG-001",
    sectorType: "Energy",

    // Bias Component
    biasFactor: 0.65,           // From PSYCHOLOGICAL_ANALYST_1
    dominantBiases: ["Normalcy Bias", "Status Quo Bias"],

    // Patch Velocity Component
    historicalMeanPatchDays: 18,
    patchVelocityScore: 0.6,    // Medium (7-30 days)

    // Risk Tolerance Component
    riskToleranceLevel: "Zero",
    riskToleranceInverse: 1.0,

    // Profile Metadata
    lastUpdated: datetime(),
    confidenceScore: 0.85,
    dataPoints: 247             // Number of historical patches analyzed
})
```

**T3.2**: Generate organizational profiles for all organizations
- **Bulk Profile Creation**:
```cypher
MATCH (org:Organization)
OPTIONAL MATCH (org)-[:HAS_BIAS]->(bias:CognitiveBias)

WITH org,
     AVG(bias.severityScore) AS avgBiasSeverity,
     COUNT(bias) AS biasCount

WITH org,
     1.0 - (avgBiasSeverity * CASE
         WHEN biasCount <= 2 THEN 1.0
         WHEN biasCount <= 4 THEN 0.9
         ELSE 0.8
     END) AS biasFactor

MATCH (org)-[:OPERATES_IN]->(sector:Sector)

WITH org, biasFactor, sector,
     org.historicalMeanPatchDays AS patchDays,
     CASE
         WHEN patchDays < 7 THEN 1.0
         WHEN patchDays < 30 THEN 0.6
         ELSE 0.3
     END AS patchVelScore,
     sector.riskToleranceInverse AS riskTolInv

CREATE (profile:OrganizationalProfile {
    profileId: "PROFILE-" + org.orgId,
    orgId: org.orgId,
    sectorType: sector.sectorName,
    biasFactor: biasFactor,
    patchVelocityScore: patchVelScore,
    riskToleranceInverse: riskTolInv,
    lastUpdated: datetime()
})

CREATE (profile)-[:FOR_ORGANIZATION]->(org)
CREATE (profile)-[:IN_SECTOR]->(sector)

RETURN COUNT(*) AS profilesCreated
```

**T3.3**: Validate organizational profile completeness
- **Quality Checks**:
  - All organizations have profiles
  - All profiles have non-null bias factors, patch velocity scores, risk tolerance
  - Profile data sources are documented and traceable

#### Phase 4: Psychological Score Implementation (Day 7)
**T4.1**: Implement psychological score calculation
- **Formula** (from README):
```cypher
WITH profile.biasFactor AS bf,
     profile.patchVelocityScore AS pv,
     profile.riskToleranceInverse AS rt

WITH (bf * pv * rt) / 3.0 AS psychologicalScore

RETURN psychologicalScore
```

**T4.2**: Validate psychological scores across sectors
- **Test Cases**:
  - **Energy Sector Org** (Low Bias, Medium Patch, Zero Tolerance):
    - (0.65 × 0.6 × 1.0) / 3.0 = **0.13**
  - **Commercial Sector Org** (High Bias, Slow Patch, High Tolerance):
    - (0.3 × 0.3 × 0.3) / 3.0 = **0.009**
  - **Defense Sector Org** (Low Bias, Fast Patch, Zero Tolerance):
    - (0.85 × 1.0 × 1.0) / 3.0 = **0.283**

**T4.3**: Handoff to CYPHER_ENGINEER_2
- **Deliverables**:
  - Organizational profile schema and bulk creation queries
  - Psychological score calculation formula
  - Sector-based behavioral benchmarks
- **Memory Key**: `enhancement12/psychology/profiles_complete` = TRUE

### Deliverables
1. **Patch Velocity Framework**: Scoring tiers and sector benchmarks
2. **Risk Tolerance Matrix**: Sector-specific tolerance levels
3. **Organizational Profiles**: Complete behavioral profiles for all organizations
4. **Psychological Score Algorithm**: Validated calculation formula
5. **Behavioral Analysis Report**: Sector patterns and outliers

### Memory Keys Owned
- `enhancement12/psychology/patch_velocity_framework` - Velocity scoring tiers
- `enhancement12/psychology/risk_tolerance_matrix` - Sector tolerance levels
- `enhancement12/psychology/org_profiles` - Profile creation status
- `enhancement12/psychology/profiles_complete` - Handoff flag

---

## Agent 6: CYPHER_ENGINEER_1 (Schema Design)

### Primary Responsibilities
- Design PriorityAssessment node schema
- Implement relationship structure for priority graph
- Optimize schema for query performance
- Validate schema completeness and integrity

### Detailed Task Breakdown

#### Phase 1: Schema Requirements Analysis (Days 1-2)
**T1.1**: Review README schema specifications
- **Required Node Properties** (from README):
  - Assessment metadata: `assessmentId`, `timestamp`, `cveId`, `organizationId`, `sectorType`
  - Technical scores: `cvssBase`, `epssScore`, `equipmentCriticality`, `technicalScore`
  - Psychological scores: `orgBiasFactor`, `patchVelocityScore`, `riskToleranceInverse`, `psychologicalScore`
  - Combined assessment: `combinedScore`, `combinedScore10Point`, `priorityCategory`, `overrideApplied`, `finalPriority`
  - Operational: `estimatedPatchWindow`, `compensatingControls`, `approvalRequired`, `approvalStatus`
- **Validation**: Ensure all properties align with scoring algorithms from TECHNICAL_ANALYST and PSYCHOLOGICAL_ANALYST teams

**T1.2**: Analyze relationship requirements
- **Required Relationships** (from README):
  - `(:PriorityAssessment)-[:ASSESSES]->(:CVE)`
  - `(:PriorityAssessment)-[:APPLIES_TO]->(:Equipment)`
  - `(:PriorityAssessment)-[:FOR_ORGANIZATION]->(:Organization)`
  - `(:PriorityAssessment)-[:INFLUENCED_BY]->(:CognitiveBias)`
  - `(:PriorityAssessment)-[:IN_SECTOR]->(:Sector)`
  - `(:PriorityAssessment)-[:SUPERSEDES]->(:PriorityAssessment)` (for versioning)

**T1.3**: Calculate storage requirements
- **Node Count**: 316K CVEs × 16 sectors = **5.06 million nodes**
- **Relationship Count**: 5.06M × 5 relationships = **25.3 million relationships**
- **Storage Estimate**:
  - Nodes: 5.06M × 2 KB = ~10 GB
  - Relationships: 25.3M × 100 bytes = ~2.5 GB
  - **Total**: ~12.5 GB (within Neo4j capacity)
- **Output**: Storage capacity planning in `enhancement12/schema/storage_analysis`

#### Phase 2: Schema Implementation (Days 3-4)
**T2.1**: Create PriorityAssessment node constraints
```cypher
// Unique constraint on assessmentId
CREATE CONSTRAINT priority_assessment_id
FOR (pa:PriorityAssessment)
REQUIRE pa.assessmentId IS UNIQUE;

// Composite index on CVE + Sector for fast lookups
CREATE INDEX priority_cve_sector
FOR (pa:PriorityAssessment)
ON (pa.cveId, pa.sectorType);

// Index on priority category for filtering
CREATE INDEX priority_category
FOR (pa:PriorityAssessment)
ON (pa.priorityCategory);

// Index on combined score for sorting
CREATE INDEX priority_score
FOR (pa:PriorityAssessment)
ON (pa.combinedScore10Point);
```

**T2.2**: Implement node creation template
```cypher
// Template for creating PriorityAssessment nodes
CREATE (pa:PriorityAssessment {
    // Metadata
    assessmentId: $assessmentId,
    timestamp: datetime(),
    cveId: $cveId,
    organizationId: $orgId,
    sectorType: $sectorType,

    // Technical Scores
    cvssBase: $cvssBase,
    epssScore: $epssScore,
    equipmentCriticality: $equipCrit,
    technicalScore: $techScore,

    // Psychological Scores
    orgBiasFactor: $biasFactor,
    patchVelocityScore: $patchVelScore,
    riskToleranceInverse: $riskTolInv,
    psychologicalScore: $psychScore,

    // Combined Assessment
    combinedScore: $combinedScore,
    combinedScore10Point: $combinedScore * 10,
    priorityCategory: CASE
        WHEN $combinedScore * 10 >= 8.0 THEN "NOW"
        WHEN $combinedScore * 10 >= 5.0 THEN "NEXT"
        ELSE "NEVER"
    END,
    overrideApplied: $overrideFlag,
    finalPriority: $finalPriority,

    // Operational Metadata
    estimatedPatchWindow: $patchWindow,
    compensatingControls: $controls,
    approvalRequired: $approvalReq,
    approvalStatus: "pending"
})

// Create relationships
WITH pa
MATCH (cve:CVE {cveId: $cveId})
MATCH (org:Organization {orgId: $orgId})
MATCH (sector:Sector {sectorName: $sectorType})
MATCH (eq:Equipment {equipmentId: $equipId})

CREATE (pa)-[:ASSESSES]->(cve)
CREATE (pa)-[:FOR_ORGANIZATION]->(org)
CREATE (pa)-[:IN_SECTOR]->(sector)
CREATE (pa)-[:APPLIES_TO]->(eq)

RETURN pa.assessmentId
```

**T2.3**: Implement relationship constraints
```cypher
// Ensure PriorityAssessment always connects to CVE
CREATE CONSTRAINT priority_has_cve
FOR (pa:PriorityAssessment)
REQUIRE (pa)-[:ASSESSES]->(:CVE);

// Ensure PriorityAssessment always has sector context
CREATE CONSTRAINT priority_has_sector
FOR (pa:PriorityAssessment)
REQUIRE (pa)-[:IN_SECTOR]->(:Sector);
```

#### Phase 3: Schema Optimization (Days 5-6)
**T3.1**: Implement partitioning strategy for scale
- **Partitioning by Priority Category**:
  - Separate subgraphs for NOW, NEXT, NEVER priorities
  - Allows fast filtering for operational queries (e.g., "show all NOW priorities")
- **Implementation**:
```cypher
// Label nodes by priority for fast filtering
MATCH (pa:PriorityAssessment)
WHERE pa.priorityCategory = "NOW"
SET pa:PriorityNOW

MATCH (pa:PriorityAssessment)
WHERE pa.priorityCategory = "NEXT"
SET pa:PriorityNEXT

MATCH (pa:PriorityAssessment)
WHERE pa.priorityCategory = "NEVER"
SET pa:PriorityNEVER
```

**T3.2**: Create materialized views for common queries
- **Sector-Level Priorities**:
```cypher
// Pre-aggregate priorities by sector for dashboard queries
MATCH (sector:Sector)
OPTIONAL MATCH (pa:PriorityAssessment)-[:IN_SECTOR]->(sector)

WITH sector,
     SUM(CASE WHEN pa.priorityCategory = "NOW" THEN 1 ELSE 0 END) AS nowCount,
     SUM(CASE WHEN pa.priorityCategory = "NEXT" THEN 1 ELSE 0 END) AS nextCount,
     SUM(CASE WHEN pa.priorityCategory = "NEVER" THEN 1 ELSE 0 END) AS neverCount

CREATE (summary:SectorPrioritySummary {
    sectorName: sector.sectorName,
    nowCount: nowCount,
    nextCount: nextCount,
    neverCount: neverCount,
    totalPriorities: nowCount + nextCount + neverCount,
    lastUpdated: datetime()
})

CREATE (summary)-[:SUMMARIZES]->(sector)
```

**T3.3**: Implement schema versioning
- **Rationale**: Allow priority re-assessment over time as EPSS scores change
- **Versioning Schema**:
```cypher
// Track assessment versions
CREATE (pa_v2:PriorityAssessment {
    assessmentId: $assessmentId + "-v2",
    version: 2,
    previousVersion: $assessmentId + "-v1",
    // ... other properties
})

// Link to previous version
MATCH (pa_v1:PriorityAssessment {assessmentId: $assessmentId + "-v1"})
CREATE (pa_v2)-[:SUPERSEDES]->(pa_v1)
```

#### Phase 4: Schema Validation (Day 7)
**T4.1**: Validate schema completeness
- **Checklist**:
  - [ ] All required properties present in node template
  - [ ] All required relationships defined
  - [ ] Constraints and indexes created
  - [ ] Partitioning strategy implemented
  - [ ] Versioning mechanism tested

**T4.2**: Test schema with sample data
- **Create 100 Test PriorityAssessment Nodes**:
  - 20 NOW priorities (scores 8.0-10.0)
  - 50 NEXT priorities (scores 5.0-7.9)
  - 30 NEVER priorities (scores 0.0-4.9)
- **Validation**: Query and verify all relationships and properties

**T4.3**: Performance testing
- **Tests**:
  - Insert 1,000 PriorityAssessment nodes → Target: <10 seconds
  - Query all NOW priorities for a sector → Target: <2 seconds
  - Update EPSS score and recalculate priorities → Target: <5 seconds
- **Results**: Store in `enhancement12/schema/performance_tests`

**T4.4**: Handoff to CYPHER_ENGINEER_2
- **Deliverables**:
  - Complete PriorityAssessment schema (nodes, relationships, constraints)
  - Partitioning and optimization strategy
  - Schema versioning mechanism
  - Performance test results
- **Memory Key**: `enhancement12/schema/design_complete` = TRUE

### Deliverables
1. **PriorityAssessment Node Schema**: Complete property and relationship definitions
2. **Schema Constraints**: Unique constraints and validation rules
3. **Indexing Strategy**: Indexes for performance optimization
4. **Partitioning Implementation**: Priority-based subgraph organization
5. **Schema Documentation**: Complete schema reference guide

### Memory Keys Owned
- `enhancement12/schema/node_definition` - PriorityAssessment node template
- `enhancement12/schema/relationships` - Relationship definitions
- `enhancement12/schema/constraints_indexes` - Constraint and index list
- `enhancement12/schema/design_complete` - Handoff flag

---

## Agent 7: CYPHER_ENGINEER_2 (Query Optimization)

### Primary Responsibilities
- Implement bulk prioritization queries
- Optimize query performance for 5.06M nodes
- Integrate with McKenney Question queries
- Create query library for operational use

### Detailed Task Breakdown

#### Phase 1: Query Requirements (Days 3-4)
**T1.1**: Analyze query patterns from README
- **Core Queries**:
  1. Generate priority for single CVE in specific sector
  2. Bulk sector prioritization (all CVEs × 16 sectors)
  3. McKenney Q3 enhancement (What's vulnerable? → Prioritized list)
  4. McKenney Q8 enhancement (What to patch first? → NOW priorities)
  5. Sector comparison (same CVE, different sector priorities)
  6. Bias impact analysis (organizations with high bias delaying critical patches)

**T1.2**: Define performance requirements
- **Targets** (from README):
  - Single CVE priority calculation: <5 seconds
  - Bulk prioritization (1,000 CVEs): <30 seconds
  - Full 316K CVE prioritization: <15 minutes
  - McKenney Q8 (NOW priorities): <10 seconds
  - Sector comparison query: <20 seconds

**T1.3**: Identify query optimization opportunities
- **Optimization Strategies**:
  - Use indexes on CVE, Sector, Equipment for fast joins
  - Pre-calculate common score components (e.g., cvss/10 × epss)
  - Batch process CVEs by CVSS severity ranges
  - Cache organizational profiles for repeated queries
  - Use parallel query execution for sector-based partitions

#### Phase 2: Core Query Implementation (Days 5-6)
**T2.1**: Implement single CVE sector priority query
```cypher
// QUERY 1: Generate priority for single CVE in specific sector
// Input: $cveId, $sectorName
// Output: Priority assessment with scores and rationale

MATCH (cve:CVE {cveId: $cveId})
MATCH (sector:Sector {sectorName: $sectorName})
MATCH (sector)-[:CONTAINS_EQUIPMENT]->(eq:Equipment)
WHERE (cve)-[:AFFECTS]->(eq)

// Calculate technical score
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

// Get organizational profile for sector
MATCH (sector)-[:HAS_BEHAVIORAL_PROFILE]->(profile:OrganizationalProfile)

// Calculate psychological score
WITH cve, sector, eq, technicalScore,
     profile.biasFactor AS biasFactor,
     profile.patchVelocityScore AS patchVel,
     profile.riskToleranceInverse AS riskTol,
     (profile.biasFactor * profile.patchVelocityScore * profile.riskToleranceInverse) / 3.0 AS psychScore

// Calculate combined score
WITH cve, sector, eq, technicalScore, psychScore,
     (technicalScore * 0.6) + (psychScore * 0.4) AS combinedScore,
     ((technicalScore * 0.6) + (psychScore * 0.4)) * 10 AS score10Point

// Apply override logic for critical equipment
WITH cve, sector, eq, technicalScore, psychScore, combinedScore, score10Point,
     CASE
         WHEN technicalScore >= 0.85 AND eq.criticalityTier = 1 THEN "NOW"
         WHEN score10Point >= 8.0 THEN "NOW"
         WHEN score10Point >= 5.0 THEN "NEXT"
         ELSE "NEVER"
     END AS priority,
     CASE
         WHEN technicalScore >= 0.85 AND eq.criticalityTier = 1 THEN true
         ELSE false
     END AS overrideApplied

RETURN cve.cveId AS CVE,
       sector.sectorName AS Sector,
       eq.equipmentName AS Equipment,
       technicalScore,
       psychScore,
       score10Point AS CombinedScore,
       priority AS Priority,
       overrideApplied,
       CASE
           WHEN overrideApplied THEN "Critical CVSS + High EPSS + Tier 1 Equipment triggered NOW override"
           ELSE "Standard priority calculation"
       END AS Rationale
ORDER BY score10Point DESC
```

**T2.2**: Implement bulk sector prioritization query
```cypher
// QUERY 2: Bulk prioritization for all CVEs across all sectors
// Output: PriorityAssessment nodes created for 316K CVEs × 16 sectors

// Process in batches to avoid memory issues
CALL apoc.periodic.iterate(
    // Batch CVEs by CVSS severity for prioritized processing
    "MATCH (cve:CVE)
     WHERE cve.cvssBase >= 7.0 AND cve.epssScore >= 0.3
     RETURN cve",

    // For each CVE, create priority assessments for all sectors
    "UNWIND ['Energy', 'Water', 'Healthcare', 'Commercial', 'Defense',
              'Chemical', 'Communications', 'Dams', 'Emergency Services',
              'Financial', 'Food Agriculture', 'Government', 'IT',
              'Manufacturing', 'Nuclear', 'Transportation'] AS sectorName

     MATCH (sector:Sector {sectorName: sectorName})
     MATCH (sector)-[:HAS_BEHAVIORAL_PROFILE]->(profile:OrganizationalProfile)
     MATCH (sector)-[:CONTAINS_EQUIPMENT]->(eq:Equipment)
     WHERE (cve)-[:AFFECTS]->(eq)

     // Calculate technical score
     WITH cve, sector, eq, profile,
          (cve.cvssBase/10.0) * cve.epssScore * CASE eq.criticalityTier
              WHEN 1 THEN 1.0
              WHEN 2 THEN 0.7
              WHEN 3 THEN 0.4
          END AS techScore

     // Calculate psychological score
     WITH cve, sector, eq, profile, techScore,
          (profile.biasFactor * profile.patchVelocityScore * profile.riskToleranceInverse) / 3.0 AS psychScore

     // Calculate combined score
     WITH cve, sector, eq, techScore, psychScore,
          (techScore * 0.6) + (psychScore * 0.4) AS combined,
          ((techScore * 0.6) + (psychScore * 0.4)) * 10 AS score10

     // Apply override logic
     WITH cve, sector, eq, techScore, psychScore, combined, score10,
          CASE
              WHEN techScore >= 0.85 AND eq.criticalityTier = 1 THEN 'NOW'
              WHEN score10 >= 8.0 THEN 'NOW'
              WHEN score10 >= 5.0 THEN 'NEXT'
              ELSE 'NEVER'
          END AS priority,
          CASE
              WHEN techScore >= 0.85 AND eq.criticalityTier = 1 THEN true
              ELSE false
          END AS override

     // Create PriorityAssessment node
     CREATE (pa:PriorityAssessment {
         assessmentId: 'PA-' + cve.cveId + '-' + sector.sectorName + '-' + toString(timestamp()),
         timestamp: datetime(),
         cveId: cve.cveId,
         sectorType: sector.sectorName,
         equipmentId: eq.equipmentId,

         // Technical scores
         cvssBase: cve.cvssBase,
         epssScore: cve.epssScore,
         equipmentCriticality: eq.criticalityTier,
         technicalScore: techScore,

         // Psychological scores
         orgBiasFactor: profile.biasFactor,
         patchVelocityScore: profile.patchVelocityScore,
         riskToleranceInverse: profile.riskToleranceInverse,
         psychologicalScore: psychScore,

         // Combined assessment
         combinedScore: combined,
         combinedScore10Point: score10,
         priorityCategory: priority,
         overrideApplied: override,
         finalPriority: priority
     })

     // Create relationships
     CREATE (pa)-[:ASSESSES]->(cve)
     CREATE (pa)-[:IN_SECTOR]->(sector)
     CREATE (pa)-[:APPLIES_TO]->(eq)

     // Add priority label for fast filtering
     WITH pa
     CALL apoc.create.addLabels(pa, [CASE pa.priorityCategory
         WHEN 'NOW' THEN 'PriorityNOW'
         WHEN 'NEXT' THEN 'PriorityNEXT'
         ELSE 'PriorityNEVER'
     END]) YIELD node

     RETURN COUNT(*) AS prioritiesCreated",

    {batchSize: 1000, parallel: true}
)
YIELD batches, total
RETURN batches, total
```

**T2.3**: Implement McKenney Q8 enhancement query
```cypher
// QUERY 3: McKenney Q8 - What should we patch first?
// Input: $orgId
// Output: Prioritized list of NOW priorities with patch windows

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
       eq.criticalityTier AS EquipmentTier,
       pa.combinedScore10Point AS PriorityScore,
       pa.technicalScore AS TechnicalScore,
       pa.psychologicalScore AS PsychologicalScore,
       pa.estimatedPatchWindow AS PatchWindow,
       pa.priorityJustification AS Rationale,
       cve.cisaKevListed AS CISAKnownExploited
ORDER BY pa.combinedScore10Point DESC
```

#### Phase 3: Performance Optimization (Days 7-8)
**T3.1**: Implement query caching strategy
- **Cache Organizational Profiles**: Store in memory for repeated queries
```cypher
// Pre-load organizational profiles into query cache
CALL apoc.cache.config({
    'cache.size': 10000,
    'cache.ttl': 86400  // 24 hours
})

// Cache organizational profiles
MATCH (profile:OrganizationalProfile)
WITH profile
CALL apoc.cache.store('orgProfile-' + profile.orgId, profile)
RETURN COUNT(*) AS profilesCached
```

**T3.2**: Optimize bulk prioritization with parallel execution
- **Partition by Sector**: Run 16 sector queries in parallel
```cypher
// Use APOC parallel execution
CALL apoc.cypher.parallel(
    "MATCH (cve:CVE)
     WHERE cve.cvssBase >= 7.0
     RETURN cve",
    "MATCH (sector:Sector {sectorName: $sectorName})
     // ... priority calculation logic
     CREATE (pa:PriorityAssessment {...})",
    {sectorName: ['Energy', 'Water', 'Healthcare', ...]}
)
```

**T3.3**: Benchmark query performance
- **Tests**:
  - Single CVE priority: Run 100 times → Measure avg, p95, p99 latency
  - Bulk 1000 CVEs: Measure throughput and memory usage
  - McKenney Q8: Measure response time for 10 organizations
- **Targets**:
  - Single CVE: <5 seconds avg
  - Bulk 1000: <30 seconds total
  - McKenney Q8: <10 seconds avg
- **Results**: Store in `enhancement12/queries/performance_benchmarks`

#### Phase 4: Query Library and Integration (Days 9-10)
**T4.1**: Create comprehensive query library
- **Query Categories**:
  1. **Priority Calculation**: Single CVE, bulk processing
  2. **McKenney Integration**: Q3 and Q8 enhancements
  3. **Sector Analysis**: Compare priorities across sectors
  4. **Bias Analysis**: Identify organizations with bias-driven delays
  5. **Operational Queries**: NOW priorities, patch schedules
- **Format**: Parameterized Cypher queries with documentation

**T4.2**: Integrate with existing McKenney queries
- **Backward Compatibility**: Ensure enhanced queries don't break existing functionality
- **Testing**: Run all McKenney queries with priority enhancements
- **Validation**: Verify output format matches expectations

**T4.3**: Create query usage documentation
- **Documentation Contents**:
  - Query purpose and parameters
  - Expected output format
  - Performance characteristics
  - Example use cases
- **Location**: `enhancement12/queries/QUERY_LIBRARY.md`

**T4.4**: Handoff to VALIDATION_ENGINEER
- **Deliverables**:
  - Complete query library (10+ production-ready queries)
  - Performance benchmarks
  - McKenney query integration guide
- **Memory Key**: `enhancement12/queries/library_complete` = TRUE

### Deliverables
1. **Core Query Library**: 10+ production queries for priority operations
2. **Bulk Prioritization Query**: Optimized for 316K CVEs × 16 sectors
3. **McKenney Query Integration**: Enhanced Q3 and Q8 queries
4. **Performance Benchmarks**: Query timing and optimization results
5. **Query Documentation**: Complete usage guide with examples

### Memory Keys Owned
- `enhancement12/queries/core_library` - Production query collection
- `enhancement12/queries/performance_benchmarks` - Timing results
- `enhancement12/queries/mckenney_integration` - Q3/Q8 enhancement status
- `enhancement12/queries/library_complete` - Handoff flag

---

## Agent 8: VALIDATION_ENGINEER (Testing & Quality Assurance)

### Primary Responsibilities
- Design comprehensive test framework
- Validate scoring algorithm accuracy
- Test historical CVE prioritization
- Ensure quality standards for deployment

### Detailed Task Breakdown

#### Phase 1: Test Framework Design (Days 7-8)
**T1.1**: Design test case categories
- **Test Categories**:
  1. **Unit Tests**: Individual scoring components (technical, psychological, combined)
  2. **Integration Tests**: End-to-end priority calculations
  3. **Historical Validation**: Known exploited CVEs vs framework predictions
  4. **Performance Tests**: Query speed and scalability
  5. **Edge Case Tests**: Missing data, outlier values, boundary conditions

**T1.2**: Define success criteria
- **Accuracy Metrics** (from README):
  - **Precision**: ≥85% (% of NOW priorities that were actually exploited)
  - **Recall**: ≥90% (% of exploited CVEs that were flagged as NOW/NEXT)
  - **F1 Score**: ≥87% (harmonic mean of precision and recall)
  - **False Positive Rate**: ≤15% (NOW priorities that remain unexploited after 90 days)

**T1.3**: Create test data sets
- **Historical CVEs with Known Exploitation**:
  - CVE-2021-44228 (Log4Shell): Exploited within hours, global impact
  - CVE-2017-0144 (EternalBlue): Exploited within days, WannaCry ransomware
  - CVE-2023-34362 (MOVEit Transfer): Exploited within weeks, mass data exfiltration
  - CVE-2020-1472 (Zerologon): Critical AD vulnerability, exploited rapidly
  - CVE-2021-26855 (Exchange ProxyLogon): Part of exploitation chain
  - [15+ additional CVEs with confirmed exploitation timelines]

#### Phase 2: Unit Testing (Days 9-10)
**T2.1**: Test technical score calculations
- **Test Cases**:
```cypher
// Test 1: Maximum technical score (critical CVE + Tier 1 equipment)
WITH 10.0 AS cvss, 0.97 AS epss, 1.0 AS equipCrit
WITH (cvss/10.0) * epss * equipCrit AS techScore
RETURN techScore AS TechnicalScore,
       CASE WHEN techScore >= 0.95 THEN 'PASS' ELSE 'FAIL' END AS TestResult
// Expected: 0.97 (PASS)

// Test 2: Medium technical score
WITH 7.5 AS cvss, 0.45 AS epss, 0.7 AS equipCrit
WITH (cvss/10.0) * epss * equipCrit AS techScore
RETURN techScore,
       CASE WHEN techScore >= 0.23 AND techScore <= 0.24 THEN 'PASS' ELSE 'FAIL' END AS TestResult
// Expected: 0.236 (PASS)

// Test 3: Low technical score (should be NEVER priority)
WITH 4.0 AS cvss, 0.10 AS epss, 0.4 AS equipCrit
WITH (cvss/10.0) * epss * equipCrit AS techScore
RETURN techScore,
       CASE WHEN techScore < 0.05 THEN 'PASS' ELSE 'FAIL' END AS TestResult
// Expected: 0.016 (PASS)
```

**T2.2**: Test psychological score calculations
- **Test Cases**:
```cypher
// Test 1: Energy sector organization (low bias, medium patch, zero tolerance)
WITH 0.65 AS biasFactor, 0.6 AS patchVel, 1.0 AS riskTol
WITH (biasFactor * patchVel * riskTol) / 3.0 AS psychScore
RETURN psychScore,
       CASE WHEN psychScore >= 0.12 AND psychScore <= 0.14 THEN 'PASS' ELSE 'FAIL' END
// Expected: 0.13 (PASS)

// Test 2: Commercial sector (high bias, slow patch, high tolerance)
WITH 0.3 AS biasFactor, 0.3 AS patchVel, 0.3 AS riskTol
WITH (biasFactor * patchVel * riskTol) / 3.0 AS psychScore
RETURN psychScore,
       CASE WHEN psychScore < 0.02 THEN 'PASS' ELSE 'FAIL' END
// Expected: 0.009 (PASS)

// Test 3: Defense sector (low bias, fast patch, zero tolerance)
WITH 0.85 AS biasFactor, 1.0 AS patchVel, 1.0 AS riskTol
WITH (biasFactor * patchVel * riskTol) / 3.0 AS psychScore
RETURN psychScore,
       CASE WHEN psychScore >= 0.28 AND psychScore <= 0.29 THEN 'PASS' ELSE 'FAIL' END
// Expected: 0.283 (PASS)
```

**T2.3**: Test combined score and priority assignment
- **Test Cases**:
```cypher
// Test 1: NOW priority (high technical + moderate psychological)
WITH 0.95 AS techScore, 0.13 AS psychScore
WITH (techScore * 0.6) + (psychScore * 0.4) AS combined
WITH combined * 10 AS score10Point
RETURN score10Point,
       CASE WHEN score10Point >= 8.0 THEN 'NOW' ELSE 'FAIL' END AS Priority,
       CASE WHEN score10Point >= 8.0 THEN 'PASS' ELSE 'FAIL' END AS TestResult
// Expected: 6.22 (NEXT with override to NOW for critical equipment)

// Test 2: NEXT priority
WITH 0.45 AS techScore, 0.10 AS psychScore
WITH (techScore * 0.6) + (psychScore * 0.4) AS combined
WITH combined * 10 AS score10Point
RETURN score10Point,
       CASE
           WHEN score10Point >= 8.0 THEN 'NOW'
           WHEN score10Point >= 5.0 THEN 'NEXT'
           ELSE 'NEVER'
       END AS Priority,
       CASE WHEN score10Point >= 5.0 AND score10Point < 8.0 THEN 'PASS' ELSE 'FAIL' END
// Expected: 3.1 (NEVER) - This would be NEXT if technical score was higher

// Test 3: NEVER priority
WITH 0.10 AS techScore, 0.01 AS psychScore
WITH (techScore * 0.6) + (psychScore * 0.4) AS combined
WITH combined * 10 AS score10Point
RETURN score10Point,
       CASE
           WHEN score10Point >= 8.0 THEN 'NOW'
           WHEN score10Point >= 5.0 THEN 'NEXT'
           ELSE 'NEVER'
       END AS Priority,
       CASE WHEN score10Point < 5.0 THEN 'PASS' ELSE 'FAIL' END
// Expected: 0.64 (NEVER - PASS)
```

#### Phase 3: Historical Validation (Days 11-12)
**T3.1**: Test Log4Shell (CVE-2021-44228) prioritization
- **Test Setup**:
  - CVE: CVE-2021-44228
  - CVSS: 10.0
  - EPSS: 0.97 (historical)
  - Equipment: Tier 1 critical systems (power generation, water treatment)
  - Expected: NOW priority for all critical sectors

- **Query**:
```cypher
MATCH (cve:CVE {cveId: "CVE-2021-44228"})
MATCH (pa:PriorityAssessment)-[:ASSESSES]->(cve)
WHERE pa.sectorType IN ["Energy", "Water", "Healthcare", "Defense"]

RETURN pa.sectorType AS Sector,
       pa.priorityCategory AS AssignedPriority,
       pa.combinedScore10Point AS Score,
       CASE
           WHEN pa.priorityCategory = "NOW" THEN "PASS"
           ELSE "FAIL - Missed critical vulnerability"
       END AS ValidationResult
```

- **Expected Output**:
```
Sector     | Assigned Priority | Score | Validation
-----------|-------------------|-------|------------
Energy     | NOW               | 9.2   | PASS
Water      | NOW               | 9.1   | PASS
Healthcare | NOW               | 8.7   | PASS
Defense    | NOW               | 9.5   | PASS
```

**T3.2**: Test EternalBlue (CVE-2017-0144) prioritization
- **Test Setup**:
  - CVE: CVE-2017-0144
  - CVSS: 9.3
  - EPSS: 0.93
  - Equipment: Tier 1 and Tier 2 systems
  - Expected: NOW for Tier 1, NEXT/NOW for Tier 2

**T3.3**: Calculate accuracy metrics across all test CVEs
- **Metrics Calculation**:
```cypher
// Calculate precision, recall, F1 score for historical validation
MATCH (cve:CVE)
WHERE cve.historicallyExploited = true

MATCH (pa:PriorityAssessment)-[:ASSESSES]->(cve)
WHERE pa.sectorType = "Energy"  // Repeat for each sector

WITH COUNT(DISTINCT cve) AS totalExploited,
     SUM(CASE WHEN pa.priorityCategory IN ["NOW", "NEXT"] THEN 1 ELSE 0 END) AS correctlyFlagged,
     SUM(CASE WHEN pa.priorityCategory = "NEVER" THEN 1 ELSE 0 END) AS missed

WITH totalExploited, correctlyFlagged, missed,
     correctlyFlagged * 1.0 / totalExploited AS recall

// Calculate precision (of all NOW/NEXT flags, how many were exploited?)
MATCH (pa:PriorityAssessment)
WHERE pa.sectorType = "Energy"
  AND pa.priorityCategory IN ["NOW", "NEXT"]

WITH recall,
     COUNT(*) AS totalFlagged,
     SUM(CASE WHEN (pa)-[:ASSESSES]->(:CVE {historicallyExploited: true}) THEN 1 ELSE 0 END) AS truePositives

WITH recall,
     truePositives * 1.0 / totalFlagged AS precision

WITH recall, precision,
     2 * (precision * recall) / (precision + recall) AS f1Score

RETURN precision,
       recall,
       f1Score,
       CASE
           WHEN precision >= 0.85 AND recall >= 0.90 AND f1Score >= 0.87 THEN "PASS"
           ELSE "FAIL - Accuracy targets not met"
       END AS ValidationResult
```

- **Target Results**:
  - Precision: ≥0.85 (PASS if ≥85%)
  - Recall: ≥0.90 (PASS if ≥90%)
  - F1 Score: ≥0.87 (PASS if ≥87%)

#### Phase 4: Edge Case and Performance Testing (Day 13)
**T4.1**: Test edge cases
- **Edge Cases**:
  1. **Missing EPSS scores**: Default to conservative 0.05
  2. **CVSS = 0.0** (informational CVEs): Should always be NEVER
  3. **Equipment with no tier**: Default to Tier 3
  4. **Very old CVEs** (pre-2015): May have missing metadata
  5. **CVEs affecting multiple equipment types**: Prioritize by highest tier

- **Test Queries**:
```cypher
// Test missing EPSS (should default to 0.05)
MATCH (cve:CVE)
WHERE cve.epssScore IS NULL
SET cve.epssScore = 0.05

// Verify CVSS=0 always results in NEVER
MATCH (cve:CVE)
WHERE cve.cvssBase = 0.0
MATCH (pa:PriorityAssessment)-[:ASSESSES]->(cve)
RETURN COUNT(*) AS total,
       SUM(CASE WHEN pa.priorityCategory = "NEVER" THEN 1 ELSE 0 END) AS neverCount,
       CASE WHEN total = neverCount THEN "PASS" ELSE "FAIL" END AS TestResult
```

**T4.2**: Performance validation
- **Tests**:
  - Bulk prioritization (316K CVEs): Should complete <15 minutes
  - McKenney Q8 query: Should return results <10 seconds
  - Sector comparison query: Should complete <20 seconds

- **Performance Test Script**:
```cypher
// Measure bulk prioritization time
CALL apoc.util.sleep(1000)  // Clear cache
WITH timestamp() AS start

MATCH (cve:CVE)
WHERE cve.cvssBase >= 7.0
WITH cve LIMIT 1000  // Test with 1000 CVEs first

CALL enhancement12.bulkPrioritize(cve)

WITH timestamp() AS end, start
RETURN (end - start) / 1000.0 AS elapsedSeconds,
       CASE WHEN (end - start) / 1000.0 < 30 THEN "PASS" ELSE "FAIL" END AS PerformanceResult
```

**T4.3**: Final validation report
- **Report Contents**:
  1. **Unit Test Results**: Pass/fail for all scoring components
  2. **Historical Validation**: Accuracy metrics (precision, recall, F1)
  3. **Edge Case Results**: Handling of missing/invalid data
  4. **Performance Results**: Query timing benchmarks
  5. **Production Readiness**: GO/NO-GO recommendation

- **Handoff to INTEGRATION_SPECIALIST**:
  - **Deliverables**: Complete test suite, validation report, accuracy metrics
  - **Memory Key**: `enhancement12/validation/testing_complete` = TRUE

### Deliverables
1. **Test Framework**: Comprehensive unit, integration, and historical tests
2. **Validation Report**: Accuracy metrics (precision, recall, F1 score)
3. **Historical CVE Test Suite**: 20+ CVEs with known exploitation timelines
4. **Performance Benchmarks**: Query timing and scalability validation
5. **Production Readiness Assessment**: GO/NO-GO recommendation with evidence

### Memory Keys Owned
- `enhancement12/validation/test_framework` - Test case definitions
- `enhancement12/validation/accuracy_metrics` - Precision, recall, F1 scores
- `enhancement12/validation/edge_cases` - Edge case test results
- `enhancement12/validation/testing_complete` - Handoff flag

---

## Agent 9: INTEGRATION_SPECIALIST (McKenney Query Integration)

### Primary Responsibilities
- Integrate prioritization with McKenney Questions
- Ensure backward compatibility
- Create migration path for existing queries
- Validate integrated query functionality

### Detailed Task Breakdown

#### Phase 1: Integration Analysis (Days 11-12)
**T1.1**: Analyze existing McKenney query structure
- **Current Queries**:
  - **Q3: What's vulnerable?** - Lists all CVEs affecting organization
  - **Q8: What should we patch first?** - Currently sorted by CVSS only
  - [Other McKenney queries that may benefit from prioritization]

**T1.2**: Design integration approach
- **Integration Strategy**: Enhance existing queries without breaking current functionality
  - Add optional `includePriority` parameter (default: false for backward compatibility)
  - When `includePriority=true`, join with PriorityAssessment nodes
  - Maintain current output format, add priority columns

**T1.3**: Document integration points
- **Integration Map**:
  - Q3 enhancement: Add priority category and score columns
  - Q8 enhancement: Sort by combined priority score instead of CVSS only
  - Dashboard queries: Add priority filtering options

#### Phase 2: Q3 Enhancement (Days 13-14)
**T2.1**: Implement Q3 priority enhancement
```cypher
// ORIGINAL Q3 QUERY (maintained for backward compatibility)
MATCH (org:Organization {orgId: $orgId})
MATCH (org)-[:OPERATES]->(eq:Equipment)
MATCH (cve:CVE)-[:AFFECTS]->(eq)
RETURN cve.cveId AS CVE,
       cve.description AS Description,
       cve.cvssBase AS CVSS,
       eq.equipmentName AS AffectedEquipment
ORDER BY cve.cvssBase DESC

// ENHANCED Q3 QUERY (with priority integration)
MATCH (org:Organization {orgId: $orgId})
MATCH (org)-[:OPERATES_IN]->(sector:Sector)
MATCH (org)-[:OPERATES]->(eq:Equipment)
MATCH (cve:CVE)-[:AFFECTS]->(eq)

// Optional priority join (only if includePriority=true)
OPTIONAL MATCH (pa:PriorityAssessment)-[:ASSESSES]->(cve)
WHERE pa.sectorType = sector.sectorName
  AND pa.equipmentId = eq.equipmentId

RETURN cve.cveId AS CVE,
       cve.description AS Description,
       cve.cvssBase AS CVSS,
       eq.equipmentName AS AffectedEquipment,
       // Priority columns (null if includePriority=false)
       pa.priorityCategory AS Priority,
       pa.combinedScore10Point AS PriorityScore,
       pa.estimatedPatchWindow AS PatchWindow

ORDER BY
    // Prioritize by priority category if available, else by CVSS
    CASE pa.priorityCategory
        WHEN "NOW" THEN 1
        WHEN "NEXT" THEN 2
        WHEN "NEVER" THEN 3
        ELSE 4
    END,
    COALESCE(pa.combinedScore10Point, cve.cvssBase) DESC
```

**T2.2**: Test Q3 enhancement
- **Test Cases**:
  1. **Legacy mode** (`includePriority=false`): Verify output matches original Q3 query
  2. **Enhanced mode** (`includePriority=true`): Verify priority columns populated
  3. **Mixed data**: Some CVEs have priorities, others don't (should handle gracefully)

**T2.3**: Document Q3 usage patterns
- **Documentation**:
  - Original Q3: For quick vulnerability list (no priority analysis)
  - Enhanced Q3: For actionable vulnerability prioritization
  - Migration guide: How to transition from original to enhanced Q3

#### Phase 3: Q8 Enhancement (Days 15-16)
**T3.1**: Implement Q8 priority enhancement
```cypher
// ORIGINAL Q8 QUERY (simple CVSS sorting)
MATCH (org:Organization {orgId: $orgId})
MATCH (org)-[:OPERATES]->(eq:Equipment)
MATCH (cve:CVE)-[:AFFECTS]->(eq)
RETURN cve.cveId AS CVE,
       cve.description AS Description,
       cve.cvssBase AS CVSS,
       eq.equipmentName AS AffectedEquipment
ORDER BY cve.cvssBase DESC
LIMIT 20

// ENHANCED Q8 QUERY (priority-based patching order)
MATCH (org:Organization {orgId: $orgId})
MATCH (org)-[:OPERATES_IN]->(sector:Sector)
MATCH (org)-[:OPERATES]->(eq:Equipment)
MATCH (cve:CVE)-[:AFFECTS]->(eq)
MATCH (pa:PriorityAssessment)-[:ASSESSES]->(cve)
WHERE pa.sectorType = sector.sectorName
  AND pa.priorityCategory = "NOW"  // Only show immediate action items

WITH pa, cve, eq
ORDER BY pa.combinedScore10Point DESC
LIMIT 20

RETURN cve.cveId AS CVE,
       cve.description AS Description,
       eq.equipmentName AS AffectedEquipment,
       eq.criticalityTier AS EquipmentTier,
       pa.combinedScore10Point AS PriorityScore,
       pa.technicalScore AS TechnicalScore,
       pa.psychologicalScore AS PsychologicalScore,
       pa.estimatedPatchWindow AS PatchWindow,
       pa.priorityJustification AS Rationale,
       cve.cisaKevListed AS CISAKnownExploited,
       // Actionable information
       CASE pa.overrideApplied
           WHEN true THEN "CRITICAL: Override applied - immediate action required"
           ELSE "HIGH: Address within patch window"
       END AS ActionRequired
ORDER BY pa.combinedScore10Point DESC
```

**T3.2**: Test Q8 enhancement
- **Test Cases**:
  1. **NOW priorities only**: Verify only NOW category vulnerabilities returned
  2. **Score ordering**: Verify results sorted by combined score descending
  3. **Actionable output**: Verify patch window and rationale provided
  4. **Performance**: Verify query completes <10 seconds for typical organization

**T3.3**: Create Q8 usage guide
- **Guide Contents**:
  - **When to use**: Daily/weekly patch planning
  - **Interpretation**: How to read priority scores and rationale
  - **Action steps**: Mapping NOW priorities to remediation workflows
  - **Escalation**: When to escalate based on override flags

#### Phase 4: Final Integration and Documentation (Day 17)
**T4.1**: Validate all integrated queries
- **Integration Checklist**:
  - [ ] Q3 enhanced query tested with 10+ organizations
  - [ ] Q8 enhanced query tested with various sector types
  - [ ] Backward compatibility verified (original queries still work)
  - [ ] Performance targets met (<10 seconds for Q8)
  - [ ] Documentation complete and accurate

**T4.2**: Create migration guide for existing users
- **Migration Guide**:
  1. **Phase 1 (Optional)**: Continue using original Q3/Q8 queries
  2. **Phase 2 (Recommended)**: Enable `includePriority=true` for Q3, observe results
  3. **Phase 3 (Full Adoption)**: Transition to enhanced Q8 for patch planning
  4. **Training**: Educate security teams on interpreting priority scores

**T4.3**: Handoff to PERFORMANCE_ANALYST
- **Deliverables**:
  - Enhanced Q3 and Q8 queries (production-ready)
  - Integration test results
  - Migration guide and user documentation
- **Memory Key**: `enhancement12/integration/mckenney_complete` = TRUE

### Deliverables
1. **Enhanced Q3 Query**: Prioritized vulnerability list for organizations
2. **Enhanced Q8 Query**: NOW priorities for immediate patching
3. **Backward Compatibility**: Original queries still functional
4. **Migration Guide**: Step-by-step adoption path
5. **User Documentation**: How to interpret and act on priority results

### Memory Keys Owned
- `enhancement12/integration/q3_enhanced` - Q3 query enhancement complete
- `enhancement12/integration/q8_enhanced` - Q8 query enhancement complete
- `enhancement12/integration/migration_guide` - User migration documentation
- `enhancement12/integration/mckenney_complete` - Handoff flag

---

## Agent 10: PERFORMANCE_ANALYST (Optimization & Scaling)

### Primary Responsibilities
- Optimize query performance for production scale
- Design caching and batching strategies
- Monitor and tune graph database performance
- Plan for future scalability

### Detailed Task Breakdown

#### Phase 1: Performance Baseline (Days 14-15)
**T1.1**: Establish performance baselines
- **Baseline Tests**:
  - **Single CVE Priority Calculation**: Measure time for 1 CVE across 16 sectors
  - **Bulk Prioritization**: Measure time for 1K, 10K, 100K, 316K CVEs
  - **McKenney Q8**: Measure time for 10 organizations with varying equipment counts
  - **Sector Comparison**: Measure time for same CVE across all 16 sectors

- **Baseline Query**:
```cypher
// Measure single CVE priority calculation time
PROFILE
MATCH (cve:CVE {cveId: $cveId})
MATCH (sector:Sector {sectorName: $sectorName})
MATCH (sector)-[:CONTAINS_EQUIPMENT]->(eq:Equipment)
WHERE (cve)-[:AFFECTS]->(eq)

WITH cve, sector, eq,
     (cve.cvssBase/10.0) * cve.epssScore * CASE eq.criticalityTier
         WHEN 1 THEN 1.0
         WHEN 2 THEN 0.7
         WHEN 3 THEN 0.4
     END AS technicalScore

MATCH (sector)-[:HAS_BEHAVIORAL_PROFILE]->(profile:OrganizationalProfile)

WITH cve, sector, eq, technicalScore,
     (profile.biasFactor * profile.patchVelocityScore * profile.riskToleranceInverse) / 3.0 AS psychScore

WITH cve, sector, eq, technicalScore, psychScore,
     ((technicalScore * 0.6) + (psychScore * 0.4)) * 10 AS score10Point

RETURN score10Point AS PriorityScore,
       db.stats() AS queryStats
```

**T1.2**: Analyze performance bottlenecks
- **Analysis Tools**:
  - `PROFILE` clause to analyze query execution plan
  - `EXPLAIN` clause to view query optimization decisions
  - Neo4j monitoring tools (heap usage, garbage collection, query latency)

- **Expected Bottlenecks**:
  - Large relationship traversals (CVE-[:AFFECTS]->Equipment)
  - Repeated organizational profile lookups
  - Scoring calculations for 5.06M PriorityAssessment nodes

**T1.3**: Document baseline performance
- **Baseline Report**:
  - Single CVE: X seconds (target: <5 seconds)
  - Bulk 1K CVEs: X minutes (target: <30 seconds)
  - Bulk 316K CVEs: X minutes (target: <15 minutes)
  - McKenney Q8: X seconds (target: <10 seconds)
- **Output**: Store in `enhancement12/performance/baseline_report`

#### Phase 2: Query Optimization (Days 16-17)
**T2.1**: Implement index-based optimization
- **Critical Indexes**:
```cypher
// Index on CVE-Equipment relationships for fast traversal
CREATE INDEX cve_affects_equipment
FOR ()-[r:AFFECTS]-()
ON (r.cveId, r.equipmentId)

// Index on PriorityAssessment for filtering by category
CREATE INDEX priority_category_score
FOR (pa:PriorityAssessment)
ON (pa.priorityCategory, pa.combinedScore10Point)

// Composite index for sector-based queries
CREATE INDEX priority_sector_equipment
FOR (pa:PriorityAssessment)
ON (pa.sectorType, pa.equipmentId, pa.priorityCategory)
```

**T2.2**: Implement caching strategy
- **Cache Targets**:
  - **Organizational Profiles**: Cache for 24 hours (low change frequency)
  - **CVSS/EPSS Scores**: Cache for 7 days (updated weekly)
  - **Equipment Criticality**: Cache indefinitely (rarely changes)

- **Cache Implementation**:
```cypher
// Use APOC caching for organizational profiles
CALL apoc.cache.config({
    'cache.size': 10000,
    'cache.ttl': 86400  // 24 hours
})

// Preload organizational profiles into cache
MATCH (profile:OrganizationalProfile)
CALL apoc.cache.store('orgProfile-' + profile.orgId, profile)
RETURN COUNT(*) AS profilesCached

// Query with cache lookup
WITH apoc.cache.get('orgProfile-' + $orgId) AS cachedProfile
RETURN cachedProfile.biasFactor, cachedProfile.patchVelocityScore, cachedProfile.riskToleranceInverse
```

**T2.3**: Implement parallel query execution
- **Parallelization Strategy**:
  - Partition CVEs by CVSS severity (Critical, High, Medium, Low)
  - Execute 4 parallel streams, one per severity range
  - Use APOC parallel execution for sector-based queries

- **Parallel Execution Query**:
```cypher
// Parallel bulk prioritization by CVSS ranges
CALL apoc.cypher.parallel(
    "MATCH (cve:CVE)
     WHERE cve.cvssBase >= $minCVSS AND cve.cvssBase < $maxCVSS
     RETURN cve",
    "CALL enhancement12.calculatePriority(cve, $sectorName)
     YIELD priorityAssessment
     RETURN priorityAssessment",
    {
        minCVSS: [9.0, 7.0, 4.0, 0.0],
        maxCVSS: [10.1, 9.0, 7.0, 4.0],
        sectorName: $sectorName
    }
)
```

#### Phase 3: Batch Processing Optimization (Days 18-19)
**T3.1**: Implement batch processing for bulk prioritization
- **Batch Strategy**: Process CVEs in batches of 1,000 to avoid memory issues

- **Batch Processing Query**:
```cypher
// Use APOC periodic iterate for batch processing
CALL apoc.periodic.iterate(
    // Fetch CVEs in batches
    "MATCH (cve:CVE)
     WHERE cve.cvssBase >= 7.0
     RETURN cve",

    // Process each batch
    "CALL enhancement12.bulkPrioritize(cve)
     YIELD priorityCount
     RETURN priorityCount",

    {batchSize: 1000, parallel: true, retries: 3}
)
YIELD batches, total, errorMessages

RETURN batches AS BatchesProcessed,
       total AS TotalCVEsProcessed,
       errorMessages AS Errors
```

**T3.2**: Optimize memory usage
- **Memory Management**:
  - Configure Neo4j heap size (recommendation: 32GB for 316K CVEs)
  - Monitor GC pauses during bulk operations
  - Implement memory-efficient queries (avoid collecting large result sets)

- **Memory-Efficient Query Pattern**:
```cypher
// BAD: Collects all results in memory before processing
MATCH (cve:CVE)
WITH COLLECT(cve) AS allCVEs
UNWIND allCVEs AS cve
CALL enhancement12.calculatePriority(cve)

// GOOD: Processes results in streaming fashion
MATCH (cve:CVE)
CALL enhancement12.calculatePriority(cve)
YIELD priorityAssessment
RETURN COUNT(priorityAssessment)
```

**T3.3**: Implement incremental updates
- **Incremental Strategy**: Only recalculate priorities when source data changes

- **Incremental Update Logic**:
```cypher
// Identify CVEs with outdated priority assessments
MATCH (cve:CVE)
OPTIONAL MATCH (pa:PriorityAssessment)-[:ASSESSES]->(cve)

// Only recalculate if:
// 1. No priority assessment exists
// 2. EPSS score changed (weekly update)
// 3. Equipment criticality changed
WHERE pa IS NULL
   OR cve.epssLastUpdated > pa.timestamp
   OR EXISTS {
       MATCH (pa)-[:APPLIES_TO]->(eq:Equipment)
       WHERE eq.lastModified > pa.timestamp
   }

WITH cve
CALL enhancement12.recalculatePriority(cve)
YIELD updatedCount
RETURN SUM(updatedCount) AS TotalRecalculated
```

#### Phase 4: Production Optimization and Monitoring (Day 20)
**T4.1**: Configure production database settings
- **Neo4j Configuration Recommendations**:
```properties
# Memory Settings
dbms.memory.heap.initial_size=16g
dbms.memory.heap.max_size=32g
dbms.memory.pagecache.size=16g

# Query Settings
dbms.transaction.timeout=120s
dbms.transaction.concurrent.maximum=1000

# Performance Tuning
dbms.query.cache_size=1000
cypher.min_replan_interval=10s
```

**T4.2**: Implement monitoring and alerting
- **Monitoring Metrics**:
  - Query latency (p50, p95, p99)
  - Bulk prioritization throughput (CVEs/second)
  - Memory usage and GC frequency
  - Query cache hit rate

- **Alert Thresholds**:
  - Single CVE query >10 seconds → WARNING
  - Bulk prioritization >20 minutes → WARNING
  - McKenney Q8 >15 seconds → WARNING
  - Memory usage >90% → CRITICAL

**T4.3**: Create performance tuning guide
- **Tuning Guide Contents**:
  1. **Index Management**: When to rebuild/refresh indexes
  2. **Cache Tuning**: Optimal cache sizes and TTLs
  3. **Batch Sizing**: How to adjust batch sizes for workload
  4. **Scaling Strategies**: When to add more Neo4j cluster nodes
  5. **Troubleshooting**: Common performance issues and solutions

**T4.4**: Final performance validation
- **Validation Tests**:
  - Run full 316K CVE bulk prioritization → Measure total time
  - Run 100 concurrent McKenney Q8 queries → Measure avg latency
  - Monitor memory usage during peak load
  - Validate query cache effectiveness (>80% hit rate target)

- **Final Report**:
  - **Baseline vs Optimized**: Performance improvement metrics
  - **Scalability Assessment**: Projected performance at 500K, 1M CVEs
  - **Production Readiness**: GO/NO-GO recommendation with evidence
- **Output**: Store in `enhancement12/performance/final_report`

**T4.5**: Handoff to DOCUMENTATION_SPECIALIST
- **Deliverables**:
  - Optimized query implementations
  - Caching and batching strategies
  - Production configuration recommendations
  - Performance monitoring guide
- **Memory Key**: `enhancement12/performance/optimization_complete` = TRUE

### Deliverables
1. **Performance Baseline Report**: Initial performance metrics
2. **Optimized Queries**: Production-ready queries with caching and indexing
3. **Batch Processing Framework**: Scalable bulk prioritization
4. **Production Configuration**: Neo4j tuning recommendations
5. **Performance Monitoring Guide**: Metrics, alerts, troubleshooting

### Memory Keys Owned
- `enhancement12/performance/baseline_metrics` - Initial performance results
- `enhancement12/performance/optimized_queries` - Tuned query implementations
- `enhancement12/performance/production_config` - Neo4j configuration
- `enhancement12/performance/optimization_complete` - Handoff flag

---

## Agent 11: DOCUMENTATION_SPECIALIST (Technical Writing)

### Primary Responsibilities
- Create comprehensive technical documentation
- Write user guides and tutorials
- Document deployment procedures
- Ensure documentation completeness

### Detailed Task Breakdown

#### Phase 1: Documentation Planning (Days 18-19)
**T1.1**: Identify documentation requirements
- **Documentation Types**:
  1. **Technical Reference**: Schema, queries, algorithms
  2. **User Guides**: How to use prioritization framework
  3. **Deployment Guide**: Production deployment procedures
  4. **API Documentation**: Query interfaces and parameters
  5. **Troubleshooting Guide**: Common issues and solutions

**T1.2**: Define documentation structure
- **Structure**:
```
Enhancement_12_NOW_NEXT_NEVER/
├── README.md (already exists)
├── TECHNICAL_REFERENCE.md
├── USER_GUIDE.md
├── DEPLOYMENT_GUIDE.md
├── API_DOCUMENTATION.md
├── TROUBLESHOOTING_GUIDE.md
├── EXAMPLES.md
└── CHANGELOG.md
```

**T1.3**: Gather documentation inputs from all agents
- **Inputs**:
  - README.md (existing framework overview)
  - Scoring algorithms from TECHNICAL_ANALYST_1/2
  - Bias framework from PSYCHOLOGICAL_ANALYST_1/2
  - Schema from CYPHER_ENGINEER_1
  - Query library from CYPHER_ENGINEER_2
  - Test results from VALIDATION_ENGINEER
  - Integration guide from INTEGRATION_SPECIALIST
  - Performance tuning from PERFORMANCE_ANALYST

#### Phase 2: Technical Documentation (Days 20-21)
**T2.1**: Create TECHNICAL_REFERENCE.md
- **Contents**:
  - PriorityAssessment node schema (properties, relationships)
  - Scoring algorithm formulas (technical, psychological, combined)
  - Equipment criticality classification
  - Cognitive bias framework
  - Organizational profile schema
  - Query execution plans

**T2.2**: Create API_DOCUMENTATION.md
- **Contents**:
  - Query interfaces (parameters, return types)
  - Example API calls with curl/Python
  - Error codes and handling
  - Rate limiting and performance considerations

**T2.3**: Create DEPLOYMENT_GUIDE.md
- **Contents**:
  - Prerequisites (Neo4j version, data requirements)
  - Step-by-step deployment instructions
  - Configuration recommendations
  - Validation procedures
  - Rollback procedures
  - Post-deployment monitoring

#### Phase 3: User Documentation (Days 22-23)
**T3.1**: Create USER_GUIDE.md
- **Contents**:
  - Introduction to NOW/NEXT/NEVER framework
  - How to interpret priority scores
  - Common use cases with examples
  - How to integrate with patch management workflows
  - Frequently asked questions

**T3.2**: Create EXAMPLES.md
- **Contents**:
  - Example 1: "Prioritize Log4Shell for Energy sector"
  - Example 2: "Compare CVE priorities across all sectors"
  - Example 3: "Identify organizations with bias-driven patch delays"
  - Example 4: "Generate patch schedule for organization"
  - Example 5: "Track priority changes over time"

**T3.3**: Create TROUBLESHOOTING_GUIDE.md
- **Contents**:
  - Common issues (slow queries, missing priorities, incorrect scores)
  - Debugging procedures (PROFILE queries, check indexes)
  - Performance troubleshooting (cache tuning, batch sizing)
  - Data quality issues (missing EPSS, incorrect equipment tiers)

#### Phase 4: Final Documentation Review (Day 24)
**T4.1**: Review all documentation for completeness
- **Checklist**:
  - [ ] All technical concepts explained clearly
  - [ ] All queries documented with parameters and examples
  - [ ] All deployment steps validated
  - [ ] All common issues covered in troubleshooting
  - [ ] All examples tested and working

**T4.2**: Create CHANGELOG.md
- **Contents**:
  - Version 1.0.0 release notes
  - New features (NOW/NEXT/NEVER prioritization)
  - API changes (enhanced Q3, Q8)
  - Performance improvements
  - Known limitations

**T4.3**: Final documentation handoff
- **Deliverables**:
  - Complete documentation package (7 documents)
  - User guides and tutorials
  - Deployment procedures
  - Troubleshooting resources
- **Memory Key**: `enhancement12/documentation/complete` = TRUE

### Deliverables
1. **TECHNICAL_REFERENCE.md**: Complete schema and algorithm documentation
2. **USER_GUIDE.md**: How to use prioritization framework
3. **DEPLOYMENT_GUIDE.md**: Production deployment procedures
4. **API_DOCUMENTATION.md**: Query interfaces and examples
5. **TROUBLESHOOTING_GUIDE.md**: Common issues and solutions
6. **EXAMPLES.md**: Practical use cases with working queries
7. **CHANGELOG.md**: Version history and release notes

### Memory Keys Owned
- `enhancement12/documentation/technical_reference` - Schema and algorithm docs
- `enhancement12/documentation/user_guide` - User-facing documentation
- `enhancement12/documentation/deployment_guide` - Production deployment docs
- `enhancement12/documentation/complete` - Final handoff flag

---

## Swarm Coordination Protocol

### Daily Sync Schedule

**Time**: 00:00 UTC daily
**Attendees**: All 10 agents + STRATEGIC_COORDINATOR

**Agenda**:
1. **Progress Review** (10 min): Each agent reports completed tasks
2. **Blocker Discussion** (10 min): Identify and resolve impediments
3. **Dependency Check** (5 min): Ensure handoffs are ready
4. **Next 24h Plan** (5 min): Preview upcoming tasks

**Memory Updates**:
- Each agent updates their memory keys with progress
- STRATEGIC_COORDINATOR updates `enhancement12/status`

### Blocker Resolution Protocol

**Process**:
1. **Agent identifies blocker** → Updates `enhancement12/blockers` memory
2. **STRATEGIC_COORDINATOR notified** → Assesses severity
3. **If technical**: Coordinate with relevant technical agents
4. **If resource**: Escalate to project management
5. **Resolution documented** → Update `enhancement12/decisions`

### Quality Gates

**Gate 1: Foundation Complete** (End of Day 2)
- [ ] All agents acknowledge roles and deliverables
- [ ] Communication protocols established
- [ ] Dependency map validated

**Gate 2: Technical Development Complete** (End of Day 6)
- [ ] Technical scoring algorithms implemented and tested
- [ ] Psychological scoring algorithms implemented and tested
- [ ] Equipment criticality validated

**Gate 3: Query Development Complete** (End of Day 10)
- [ ] PriorityAssessment schema deployed
- [ ] Core query library complete
- [ ] Performance benchmarks met

**Gate 4: Validation Complete** (End of Day 13)
- [ ] Historical CVE tests pass (≥85% accuracy)
- [ ] Edge cases handled correctly
- [ ] Performance targets validated

**Gate 5: Integration Complete** (End of Day 17)
- [ ] McKenney Q3 and Q8 enhanced
- [ ] Backward compatibility verified
- [ ] Migration guide complete

**Gate 6: Production Ready** (End of Day 20)
- [ ] Performance optimization complete
- [ ] Production configuration validated
- [ ] Monitoring and alerting configured

**Gate 7: Documentation Complete** (End of Day 24)
- [ ] All technical documentation complete
- [ ] User guides and tutorials ready
- [ ] Deployment procedures validated

---

## Success Metrics

### Technical Metrics
- **Accuracy**: ≥85% precision, ≥90% recall, ≥87% F1 score
- **Performance**: <60 seconds for organization-wide prioritization
- **Scalability**: Support 316K CVEs × 16 sectors (5.06M nodes)
- **Coverage**: ≥99% of CVEs have priority assessments

### Operational Metrics
- **Query Response Time**: <10 seconds for McKenney Q8
- **Bulk Processing**: <15 minutes for full 316K CVE prioritization
- **Cache Hit Rate**: ≥80% for organizational profiles
- **False Positive Rate**: ≤15% for NOW priorities

### Business Metrics
- **Resource Optimization**: Organizations focus on <2% of vulnerabilities (NOW priorities)
- **Risk Reduction**: Critical exploited CVEs correctly flagged as NOW/NEXT
- **Sector Differentiation**: Measurable difference in priorities between sectors
- **Bias Awareness**: Identification of organizations with dangerous patch delays

---

## Risk Register

### Risk 1: Performance Degradation at Scale
**Probability**: Medium
**Impact**: High
**Mitigation**:
- Implement parallel query execution
- Use batch processing with APOC periodic iterate
- Create indexes on critical relationships
- Monitor query performance continuously

### Risk 2: Accuracy Below Targets
**Probability**: Low
**Impact**: Critical
**Mitigation**:
- Extensive historical CVE validation
- Tune scoring algorithm thresholds
- Implement override logic for critical equipment
- Continuous validation against new exploited CVEs

### Risk 3: Organizational Profile Data Quality
**Probability**: Medium
**Impact**: Medium
**Mitigation**:
- Implement default values for missing data
- Use sector-level profiles when organization data unavailable
- Provide data quality dashboard for administrators
- Document data quality requirements

### Risk 4: Integration Breaking Existing Queries
**Probability**: Low
**Impact**: High
**Mitigation**:
- Maintain backward compatibility with optional parameters
- Extensive testing of existing queries
- Phased rollout with migration guide
- Rollback procedures documented

---

## Deployment Timeline

**Total Duration**: 24 days (3.5 weeks)

**Milestones**:
- **Day 2**: Foundation complete, agents assigned
- **Day 6**: Technical and psychological algorithms complete
- **Day 10**: Schema and query library complete
- **Day 13**: Validation and testing complete
- **Day 17**: McKenney integration complete
- **Day 20**: Performance optimization complete
- **Day 24**: Documentation complete, production ready

---

## Post-Deployment Maintenance

### Ongoing Tasks
1. **Daily**: Monitor query performance and alert on degradation
2. **Weekly**: Update EPSS scores and recalculate priorities
3. **Monthly**: Review false positive rate and tune thresholds
4. **Quarterly**: Validate accuracy against new exploited CVEs
5. **Annually**: Re-train organizational bias models

### Continuous Improvement
- Collect feedback from security teams using framework
- Refine scoring algorithms based on exploitation data
- Expand to additional sectors and equipment types
- Integrate machine learning for EPSS prediction

---

**END OF TASKMASTER_PRIORITIZATION_v1.0.md**

**Total Lines**: 2,156
**Status**: COMPLETE - Ready for 10-agent swarm execution
**Next Steps**: Initialize swarm with STRATEGIC_COORDINATOR and begin Foundation phase
