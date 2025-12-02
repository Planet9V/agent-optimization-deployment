# Enhancement 12: NOW/NEXT/NEVER Prioritization Framework - Prerequisites

**File:** PREREQUISITES.md
**Created:** 2025-11-25 14:45:00 UTC
**Version:** 1.0.0
**Status:** ACTIVE
**Purpose:** Document all data prerequisites, schema dependencies, and system requirements for Enhancement 12

---

## Executive Summary

Enhancement 12 requires a comprehensive data foundation spanning vulnerability intelligence (316,000+ CVEs), organizational psychology (30 cognitive biases), equipment criticality (50,000+ assets), and behavioral analytics (patch velocity, risk tolerance). This document catalogs all prerequisite nodes, relationships, properties, and data quality requirements necessary for successful implementation.

**Critical Success Factor**: 95%+ data coverage across all prerequisite categories ensures accurate prioritization. Missing data can be accommodated with defaults, but reduces prioritization precision.

---

## Category 1: Vulnerability Intelligence Data

### 1.1 CVE Nodes (316,000+ Required)

**Node Label**: `CVE`

**Required Properties**:
```cypher
(:CVE {
    cveId: "CVE-2021-44228",                    // REQUIRED: Unique identifier
    description: "Apache Log4j2 JNDI features...", // REQUIRED: Vulnerability description
    cvssBase: 10.0,                             // REQUIRED: Base CVSS score (0.0-10.0)
    cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/...", // OPTIONAL: CVSS vector string
    epssScore: 0.97,                            // REQUIRED: EPSS score (0.0-1.0)
    epssPercentile: 99.8,                       // OPTIONAL: EPSS percentile rank
    publishDate: date("2021-12-10"),            // REQUIRED: CVE publication date
    cisaKevListed: true,                        // OPTIONAL: CISA Known Exploited Vulnerability
    exploitAvailable: true,                     // OPTIONAL: Public exploit exists
    epssLastUpdated: date("2025-11-18")         // REQUIRED: Last EPSS update date
})
```

**Data Quality Requirements**:
- **CVSS Coverage**: 100% of CVEs must have `cvssBase` property
  - Source: National Vulnerability Database (NVD)
  - Validation: `MATCH (cve:CVE) WHERE cve.cvssBase IS NULL RETURN COUNT(*)` should return 0

- **EPSS Coverage**: ≥95% of CVEs should have `epssScore` property
  - Source: FIRST.org EPSS API
  - Missing EPSS: Default to 0.05 (conservative estimate)
  - Validation: `MATCH (cve:CVE) WHERE cve.epssScore IS NULL RETURN COUNT(*) / 316000.0 AS missingPercent` should return <0.05

- **Temporal Coverage**: CVEs from 1999-present required
  - Prioritization focuses on CVEs with CVSS ≥7.0 AND EPSS ≥0.3 (estimated 45,000-60,000 CVEs)
  - Very old CVEs (<2010) may have limited EPSS data

**Required Relationships**:
```cypher
// CVE affects Equipment
(:CVE)-[:AFFECTS {
    detectedDate: datetime(),
    confirmationSource: "NVD CPE matching"
}]->(:Equipment)

// CVE exploited by ThreatActor (optional, enhances prioritization)
(:CVE)-[:EXPLOITED_BY {
    firstObserved: date(),
    campaignName: "Operation XYZ"
}]->(:ThreatActor)
```

**Data Sources**:
- **Primary**: National Vulnerability Database (NVD) - https://nvd.nist.gov/
- **EPSS Scores**: FIRST.org EPSS API - https://api.first.org/data/v1/epss
- **CISA KEV**: CISA Known Exploited Vulnerabilities - https://www.cisa.gov/known-exploited-vulnerabilities-catalog

**Validation Queries**:
```cypher
// Validate CVSS coverage
MATCH (cve:CVE)
RETURN COUNT(*) AS totalCVEs,
       SUM(CASE WHEN cve.cvssBase IS NULL THEN 1 ELSE 0 END) AS missingCVSS,
       100.0 * SUM(CASE WHEN cve.cvssBase IS NULL THEN 1 ELSE 0 END) / COUNT(*) AS missingCVSSPercent

// Validate EPSS coverage
MATCH (cve:CVE)
RETURN COUNT(*) AS totalCVEs,
       SUM(CASE WHEN cve.epssScore IS NULL THEN 1 ELSE 0 END) AS missingEPSS,
       100.0 * SUM(CASE WHEN cve.epssScore IS NULL THEN 1 ELSE 0 END) / COUNT(*) AS missingEPSSPercent

// Validate CVE-Equipment relationships
MATCH (cve:CVE)-[:AFFECTS]->(eq:Equipment)
RETURN COUNT(DISTINCT cve) AS cvesAffectingEquipment,
       COUNT(*) AS totalAffectsRelationships,
       COUNT(*) / COUNT(DISTINCT cve) AS avgEquipmentPerCVE
```

---

## Category 2: Equipment and Asset Data

### 2.1 Equipment Nodes (50,000+ Required)

**Node Label**: `Equipment`

**Required Properties**:
```cypher
(:Equipment {
    equipmentId: "EQ-ENERGY-001",               // REQUIRED: Unique identifier
    equipmentName: "Siemens S7-1500 PLC",       // REQUIRED: Human-readable name
    equipmentType: "Programmable Logic Controller", // REQUIRED: Equipment category
    manufacturer: "Siemens",                    // REQUIRED: OEM vendor
    model: "S7-1500",                           // REQUIRED: Model number
    firmwareVersion: "V2.8.3",                  // OPTIONAL: Current firmware
    criticalityTier: 1,                         // REQUIRED: 1 (Critical), 2 (Important), 3 (Standard)
    criticalityWeight: 1.0,                     // REQUIRED: Pre-calculated weight (1.0, 0.7, 0.4)
    sectorName: "Energy",                       // REQUIRED: Sector context
    facilityId: "FAC-ENERGY-01",                // REQUIRED: Facility location
    installDate: date("2020-03-15"),            // OPTIONAL: Deployment date
    lastModified: datetime()                    // REQUIRED: Last update timestamp
})
```

**Criticality Tier Classification**:

**Tier 1 - Critical Equipment (Weight: 1.0)**:
- **Definition**: Equipment whose compromise or failure directly threatens life safety, national security, or critical infrastructure operation
- **Examples**:
  - Power generation controls (turbine governors, reactor safety systems)
  - Water treatment controls (chemical dosing, filtration systems)
  - Hospital life support equipment (ventilators, anesthesia machines, dialysis)
  - Emergency response communication systems (911 dispatch, first responder radios)
  - Nuclear reactor safety systems (ECCS, containment monitoring)
  - Air traffic control systems (radar, navigation aids)
- **Expected Count**: 5-10% of total equipment (~2,500-5,000 assets)
- **Priority Override**: CVEs affecting Tier 1 equipment with technical score ≥0.85 automatically escalated to NOW

**Tier 2 - Important Equipment (Weight: 0.7)**:
- **Definition**: Business-critical systems whose compromise significantly impacts operations or security
- **Examples**:
  - Business application servers (ERP, CRM, financial systems)
  - Financial transaction processing systems (payment gateways, ATMs)
  - Manufacturing control systems (non-safety PLCs, robotic arms)
  - Building management systems (HVAC, lighting, access control)
  - IT infrastructure (Active Directory, DNS, email servers)
  - Healthcare patient data systems (EHR, PACS, lab systems)
- **Expected Count**: 30-40% of total equipment (~15,000-20,000 assets)
- **Patching Priority**: Balance operational needs with security requirements

**Tier 3 - Standard Equipment (Weight: 0.4)**:
- **Definition**: General-purpose systems with limited impact if compromised
- **Examples**:
  - Development and test environments
  - Office productivity systems (file servers, printers)
  - Non-critical business applications (internal wikis, time tracking)
  - Guest wireless networks
  - End-user workstations
  - Non-production IoT devices
- **Expected Count**: 50-65% of total equipment (~25,000-32,500 assets)
- **Patching Priority**: Low urgency, defer to maintenance windows

**Data Quality Requirements**:
- **Criticality Tier Coverage**: 100% of equipment must have valid `criticalityTier` (1, 2, or 3)
  - Validation: `MATCH (eq:Equipment) WHERE eq.criticalityTier NOT IN [1,2,3] RETURN COUNT(*)`

- **Sector Assignment**: 100% of equipment must have `sectorName` property
  - Required for sector-specific prioritization
  - Validation: `MATCH (eq:Equipment) WHERE eq.sectorName IS NULL RETURN COUNT(*)`

- **Equipment-CVE Relationships**: Average 50-100 CVEs per equipment expected
  - Based on typical software/firmware vulnerability density
  - Validation: `MATCH (eq:Equipment)<-[:AFFECTS]-(cve:CVE) RETURN eq.equipmentName, COUNT(cve) AS cveCount ORDER BY cveCount DESC LIMIT 20`

**Required Relationships**:
```cypher
// Sector contains Equipment
(:Sector {sectorName: "Energy"})-[:CONTAINS_EQUIPMENT]->(:Equipment)

// Organization operates Equipment
(:Organization {orgId: "ORG-001"})-[:OPERATES]->(:Equipment)

// Equipment located at Facility
(:Equipment)-[:LOCATED_AT]->(:Facility {facilityId: "FAC-ENERGY-01"})

// CVE affects Equipment (bidirectional reference)
(:CVE)-[:AFFECTS]->(:Equipment)
```

**Validation Queries**:
```cypher
// Validate criticality tier distribution
MATCH (eq:Equipment)
RETURN eq.criticalityTier AS Tier,
       COUNT(*) AS Count,
       100.0 * COUNT(*) / 50000 AS Percentage
ORDER BY eq.criticalityTier

// Expected Results:
// Tier 1: ~2,500-5,000 (5-10%)
// Tier 2: ~15,000-20,000 (30-40%)
// Tier 3: ~25,000-32,500 (50-65%)

// Validate equipment-CVE relationships
MATCH (eq:Equipment)<-[:AFFECTS]-(cve:CVE)
WITH eq, COUNT(cve) AS cveCount
RETURN MIN(cveCount) AS minCVEs,
       AVG(cveCount) AS avgCVEs,
       MAX(cveCount) AS maxCVEs,
       PERCENTILE_DISC(cveCount, 0.5) AS medianCVEs

// Identify equipment missing criticality tiers
MATCH (eq:Equipment)
WHERE eq.criticalityTier IS NULL
   OR eq.criticalityTier NOT IN [1,2,3]
RETURN COUNT(*) AS invalidTierCount,
       COLLECT(eq.equipmentName)[..10] AS examples
```

---

## Category 3: Cognitive Bias and Psychological Data

### 3.1 CognitiveBias Nodes (30 Required)

**Node Label**: `CognitiveBias`

**Required Properties**:
```cypher
(:CognitiveBias {
    biasId: "BIAS-001",                         // REQUIRED: Unique identifier
    biasName: "Normalcy Bias",                  // REQUIRED: Formal bias name
    category: "Risk Perception",                // REQUIRED: Bias category
    severityScore: 0.85,                        // REQUIRED: Security impact (0.0-1.0)
    description: "Tendency to underestimate threat likelihood...", // REQUIRED
    impactOnSecurity: "Delays patching of critical vulnerabilities", // REQUIRED
    researchReferences: ["Weinstein 1980", "Slovic 1987"], // OPTIONAL
    detectionHeuristics: {                      // OPTIONAL: How to detect bias
        patchDelayThreshold: 30,                // Days to patch critical CVEs
        minCVSS: 9.0,
        minEPSS: 0.7
    }
})
```

**Required 30 Cognitive Biases** (from cognitive psychology and security research):

**High Impact Biases (Severity ≥0.7)** - Directly delay critical patching:
1. **Normalcy Bias** (0.85): "It won't happen to us" - Underestimate threat likelihood
2. **Status Quo Bias** (0.78): "Changing systems is risky" - Resistance to security updates
3. **Sunk Cost Fallacy** (0.72): "Too much invested in legacy" - Continue using vulnerable systems

**Moderate Impact Biases (Severity 0.4-0.7)** - Influence prioritization decisions:
4. **Availability Heuristic** (0.63): Recent breaches disproportionately influential
5. **Confirmation Bias** (0.58): Seek information confirming existing security beliefs
6. **Optimism Bias** (0.55): "We're more secure than average organization"
7. **Anchoring Bias** (0.52): Over-rely on initial CVSS scores despite EPSS updates
8. **Authority Bias** (0.49): Over-trust vendor security recommendations
9. **Bandwagon Effect** (0.47): "Everyone uses this software, must be secure"
10. **Base Rate Fallacy** (0.45): Ignore statistical likelihood of exploitation

**Low Impact Biases (Severity <0.4)** - Minimal direct patching impact:
11. **Recency Bias** (0.35): Overweight recent security events
12. **Hindsight Bias** (0.33): "We should have seen that breach coming"
13. **Ingroup Bias** (0.31): Trust security decisions from similar organizations
14. **Fundamental Attribution Error** (0.29): Blame individuals for systemic security failures
15. **Framing Effect** (0.27): Security decisions influenced by information presentation
16. **Groupthink** (0.25): Security consensus overrides individual concerns
17. **False Consensus Effect** (0.23): Overestimate agreement on security priorities
18. **Attentional Bias** (0.21): Focus on visible threats, ignore silent vulnerabilities
19. **Selective Attention** (0.19): Focus on familiar attack vectors, ignore novel threats
20. **Change Blindness** (0.17): Fail to notice gradual security degradation
21. **Inattentional Blindness** (0.15): Miss security issues due to cognitive overload
22. **Cocktail Party Effect** (0.13): Selective attention to relevant security alerts
23. **Hot Hand Fallacy** (0.11): Believe security success streak will continue
24. **Gambler's Fallacy** (0.09): "We've been breached recently, unlikely to happen again"
25. **Conjunction Fallacy** (0.08): Overestimate likelihood of compound security scenarios
26. **Sample Size Neglect** (0.07): Draw security conclusions from insufficient data
27. **Regression to Mean** (0.06): Misattribute security improvements to interventions
28. **Peak-End Rule** (0.05): Security experiences judged by peaks and final moments
29. **Rosy Retrospection** (0.04): Remember past security state as better than reality
30. **Source Confusion** (0.03): Misattribute source of security information

**Data Quality Requirements**:
- **Severity Score Validation**: All biases must have `severityScore` between 0.0-1.0
  - Validation: `MATCH (cb:CognitiveBias) WHERE cb.severityScore < 0.0 OR cb.severityScore > 1.0 RETURN COUNT(*)`

- **Category Classification**: All biases categorized by psychological domain
  - Categories: "Risk Perception", "Decision Making", "Memory", "Social", "Attention"

- **Research-Backed**: High-impact biases (≥0.7) must have research references
  - Sources: Academic journals, security psychology studies

**Required Relationships**:
```cypher
// Organization exhibits Cognitive Bias
(:Organization)-[:HAS_BIAS {
    detectedDate: date(),
    evidenceSource: "patch_velocity_analysis",
    confidenceScore: 0.85                       // Detection confidence (0.0-1.0)
}]->(:CognitiveBias)

// PriorityAssessment influenced by Cognitive Bias
(:PriorityAssessment)-[:INFLUENCED_BY {
    biasImpact: "delayed_patch_decision"
}]->(:CognitiveBias)
```

**Validation Queries**:
```cypher
// Validate all 30 biases exist
MATCH (cb:CognitiveBias)
RETURN COUNT(*) AS totalBiases,
       COUNT(CASE WHEN cb.severityScore >= 0.7 THEN 1 END) AS highImpact,
       COUNT(CASE WHEN cb.severityScore >= 0.4 AND cb.severityScore < 0.7 THEN 1 END) AS moderateImpact,
       COUNT(CASE WHEN cb.severityScore < 0.4 THEN 1 END) AS lowImpact

// Expected: 30 total, 3 high, 7 moderate, 20 low

// Validate bias-organization relationships
MATCH (org:Organization)-[r:HAS_BIAS]->(cb:CognitiveBias)
RETURN COUNT(DISTINCT org) AS orgsWithBiases,
       COUNT(*) AS totalBiasRelationships,
       AVG(r.confidenceScore) AS avgConfidence
```

---

## Category 4: Organizational and Behavioral Data

### 4.1 Organization Nodes (800+ Required)

**Node Label**: `Organization`

**Required Properties**:
```cypher
(:Organization {
    orgId: "ORG-ENERGY-001",                    // REQUIRED: Unique identifier
    orgName: "Midwest Power Cooperative",       // REQUIRED: Organization name
    sectorType: "Energy",                       // REQUIRED: Sector classification
    organizationType: "Utility",                // REQUIRED: Organization type
    employeeCount: 450,                         // OPTIONAL: Organization size

    // Patch Behavior Metrics (REQUIRED for accurate prioritization)
    historicalMeanPatchDays: 18.4,              // REQUIRED: Average days to patch
    patchVelocityStdDev: 12.7,                  // OPTIONAL: Patch consistency
    fastestPatchDays: 2,                        // OPTIONAL: Best-case patching
    slowestPatchDays: 89,                       // OPTIONAL: Worst-case patching
    totalPatchesAnalyzed: 247,                  // REQUIRED: Sample size for metrics

    // Risk Profile
    riskTolerance: "Low",                       // OPTIONAL: Qualitative assessment
    regulatoryCompliance: ["NERC CIP", "FERC"], // OPTIONAL: Compliance requirements
    recentBreaches: false,                      // OPTIONAL: Breach history (5 years)

    lastUpdated: datetime()                     // REQUIRED: Profile freshness
})
```

**Patch Velocity Classification**:
- **Fast (<7 days)**: `patchVelocityScore` = 1.0
  - Typical: Defense contractors, financial institutions, healthcare (clinical systems)
- **Medium (7-30 days)**: `patchVelocityScore` = 0.6
  - Typical: Energy utilities, water utilities, manufacturing
- **Slow (>30 days)**: `patchVelocityScore` = 0.3
  - Typical: Small businesses, commercial facilities, legacy system operators

**Data Quality Requirements**:
- **Patch History**: Organizations need ≥50 historical patch events for accurate velocity calculation
  - Organizations with <50 patches use sector-level defaults
  - Validation: `MATCH (org:Organization) WHERE org.totalPatchesAnalyzed < 50 RETURN COUNT(*)`

- **Sector Assignment**: 100% of organizations must have valid `sectorType`
  - Required for sector-specific risk tolerance and prioritization
  - Validation: `MATCH (org:Organization) WHERE org.sectorType IS NULL RETURN COUNT(*)`

**Required Relationships**:
```cypher
// Organization operates in Sector
(:Organization)-[:OPERATES_IN]->(:Sector {sectorName: "Energy"})

// Organization operates Equipment
(:Organization)-[:OPERATES]->(:Equipment)

// Organization patched CVE (historical data)
(:Organization)-[:PATCHED {
    patchDate: date("2024-01-15"),
    patchDuration: 18,                          // Days from CVE publish to patch
    patchMethod: "automated"                    // automated, manual, emergency
}]->(:CVE)
```

### 4.2 OrganizationalProfile Nodes (800+ Required)

**Node Label**: `OrganizationalProfile`

**Purpose**: Pre-calculated behavioral profile for each organization, combining bias factors, patch velocity, and risk tolerance.

**Required Properties**:
```cypher
(:OrganizationalProfile {
    profileId: "PROFILE-ORG-ENERGY-001",        // REQUIRED: Unique identifier
    orgId: "ORG-ENERGY-001",                    // REQUIRED: Link to Organization
    sectorType: "Energy",                       // REQUIRED: Sector context

    // Bias Component
    biasFactor: 0.65,                           // REQUIRED: Org_Bias_Factor (0.0-1.0)
    totalBiases: 3,                             // REQUIRED: Count of detected biases
    avgBiasSeverity: 0.727,                     // REQUIRED: Mean bias severity
    biasCountPenalty: 0.9,                      // REQUIRED: Penalty for multiple biases
    dominantBiases: ["Normalcy Bias", "Status Quo Bias"], // OPTIONAL

    // Patch Velocity Component
    historicalMeanPatchDays: 18.4,              // REQUIRED: From Organization node
    patchVelocityScore: 0.6,                    // REQUIRED: Medium (7-30 days)

    // Risk Tolerance Component
    riskToleranceLevel: "Low",                  // REQUIRED: Zero, Low, Moderate, High
    riskToleranceInverse: 1.0,                  // REQUIRED: Inverse for scoring

    // Profile Metadata
    lastUpdated: datetime(),                    // REQUIRED: Profile freshness
    confidenceScore: 0.85,                      // REQUIRED: Profile reliability (0.0-1.0)
    dataPoints: 247                             // REQUIRED: Sample size
})
```

**Calculation Formulas**:
```
Org_Bias_Factor = 1.0 - (avgBiasSeverity × biasCountPenalty)

Where:
- avgBiasSeverity = Average severity of detected biases
- biasCountPenalty:
  * 1-2 biases: 1.0
  * 3-4 biases: 0.9
  * 5+ biases: 0.8
```

**Data Quality Requirements**:
- **Profile Coverage**: ≥90% of organizations should have profiles
  - Organizations without profiles use sector-level defaults
  - Validation: `MATCH (org:Organization) OPTIONAL MATCH (org)<-[:FOR_ORGANIZATION]-(profile:OrganizationalProfile) WHERE profile IS NULL RETURN COUNT(org)`

- **Confidence Score**: Profiles with confidence <0.6 should be flagged for review
  - Low confidence indicates insufficient historical data
  - Validation: `MATCH (profile:OrganizationalProfile) WHERE profile.confidenceScore < 0.6 RETURN COUNT(*)`

**Required Relationships**:
```cypher
// Profile belongs to Organization
(:OrganizationalProfile)-[:FOR_ORGANIZATION]->(:Organization)

// Profile belongs to Sector
(:OrganizationalProfile)-[:IN_SECTOR]->(:Sector)

// Profile includes Cognitive Biases
(:OrganizationalProfile)-[:INCLUDES_BIAS]->(:CognitiveBias)
```

**Validation Queries**:
```cypher
// Validate profile coverage
MATCH (org:Organization)
OPTIONAL MATCH (org)<-[:FOR_ORGANIZATION]-(profile:OrganizationalProfile)
RETURN COUNT(org) AS totalOrgs,
       COUNT(profile) AS orgsWithProfiles,
       100.0 * COUNT(profile) / COUNT(org) AS coveragePercent

// Expected: ≥90% coverage

// Validate profile confidence distribution
MATCH (profile:OrganizationalProfile)
RETURN AVG(profile.confidenceScore) AS avgConfidence,
       MIN(profile.confidenceScore) AS minConfidence,
       COUNT(CASE WHEN profile.confidenceScore >= 0.8 THEN 1 END) AS highConfidence,
       COUNT(CASE WHEN profile.confidenceScore < 0.6 THEN 1 END) AS lowConfidence
```

---

## Category 5: Sector and Infrastructure Data

### 5.1 Sector Nodes (16 Required)

**Node Label**: `Sector`

**Required Properties**:
```cypher
(:Sector {
    sectorId: "SECTOR-ENERGY",                  // REQUIRED: Unique identifier
    sectorName: "Energy",                       // REQUIRED: Sector name
    cisaCritical: true,                         // REQUIRED: CISA critical infrastructure?

    // Risk Tolerance Settings
    riskToleranceLevel: "Zero",                 // REQUIRED: Zero, Low, Moderate, High
    riskToleranceInverse: 1.0,                  // REQUIRED: Scoring weight
    riskRationale: "Life-safety consequences of operational disruptions",

    // Sector Characteristics
    regulatoryFramework: ["NERC CIP", "FERC"], // OPTIONAL: Compliance standards
    typicalPatchWindow: "Monthly maintenance",  // OPTIONAL: Patching culture

    lastUpdated: datetime()                     // REQUIRED
})
```

**16 Critical Infrastructure Sectors** (per CISA classification):
1. **Energy** (riskToleranceInverse: 1.0) - Zero tolerance
2. **Water/Wastewater** (1.0) - Zero tolerance
3. **Nuclear** (1.0) - Zero tolerance
4. **Defense Industrial Base** (1.0) - Zero tolerance
5. **Healthcare (Clinical)** (0.8) - Low tolerance
6. **Financial Services** (0.8) - Low tolerance
7. **Transportation** (0.8) - Low tolerance
8. **Chemical** (0.8) - Low tolerance
9. **Communications** (0.65) - Moderate tolerance
10. **Dams** (0.65) - Moderate tolerance
11. **Emergency Services** (0.65) - Moderate tolerance
12. **Manufacturing** (0.65) - Moderate tolerance
13. **Healthcare (Administrative)** (0.65) - Moderate tolerance
14. **Government** (0.65) - Moderate tolerance
15. **Commercial Facilities** (0.3) - High tolerance
16. **Information Technology** (0.3) - High tolerance

**Data Quality Requirements**:
- **All 16 Sectors Present**: `MATCH (s:Sector) RETURN COUNT(*)` should return 16
- **Risk Tolerance Assigned**: All sectors must have valid `riskToleranceInverse`
  - Validation: `MATCH (s:Sector) WHERE s.riskToleranceInverse IS NULL RETURN COUNT(*)`

**Required Relationships**:
```cypher
// Sector contains Equipment
(:Sector)-[:CONTAINS_EQUIPMENT]->(:Equipment)

// Sector has Behavioral Profile
(:Sector)-[:HAS_BEHAVIORAL_PROFILE]->(:OrganizationalProfile)
```

**Validation Queries**:
```cypher
// Validate all 16 sectors present
MATCH (s:Sector)
RETURN s.sectorName AS Sector,
       s.riskToleranceLevel AS RiskTolerance,
       s.riskToleranceInverse AS InverseScore
ORDER BY s.riskToleranceInverse DESC

// Validate sector-equipment relationships
MATCH (s:Sector)-[:CONTAINS_EQUIPMENT]->(eq:Equipment)
RETURN s.sectorName AS Sector,
       COUNT(eq) AS EquipmentCount,
       AVG(eq.criticalityTier) AS AvgCriticalityTier
ORDER BY EquipmentCount DESC
```

---

## Category 6: System Requirements

### 6.1 Neo4j Database Requirements

**Version**: Neo4j 5.x or later
- **Reason**: Advanced Cypher features (CALL subqueries, multiple labels)
- **Recommended**: Neo4j Enterprise 5.13+ for production deployment

**Hardware Requirements**:
- **Memory**: 64GB RAM minimum (128GB recommended)
  - Heap: 32GB (for 5.06M PriorityAssessment nodes)
  - Page Cache: 16GB (for relationship traversal)
- **Storage**: 100GB SSD minimum
  - Database: ~50GB (with indexes)
  - Backups: ~50GB (daily snapshots)
- **CPU**: 16 cores minimum (32 cores recommended for parallel queries)

**Configuration Settings**:
```properties
# Memory Settings
dbms.memory.heap.initial_size=32g
dbms.memory.heap.max_size=32g
dbms.memory.pagecache.size=16g

# Query Settings
dbms.transaction.timeout=120s
dbms.transaction.concurrent.maximum=1000

# Performance Tuning
dbms.query.cache_size=1000
cypher.min_replan_interval=10s
```

### 6.2 Required Neo4j Plugins

**APOC (Awesome Procedures on Cypher)**:
- **Version**: APOC Core 5.x
- **Purpose**: Batch processing, parallel execution, caching
- **Installation**: `neo4j-admin plugin install apoc`
- **Required Procedures**:
  - `apoc.periodic.iterate` - Batch processing for 316K CVE prioritization
  - `apoc.cypher.parallel` - Parallel query execution (4x throughput)
  - `apoc.cache.store/get` - Organizational profile caching

**Graph Data Science (GDS)** (Optional):
- **Version**: GDS 2.x
- **Purpose**: Future enhancements (graph algorithms, ML models)
- **Installation**: `neo4j-admin plugin install graph-data-science`

### 6.3 External Data Sources

**National Vulnerability Database (NVD)**:
- **URL**: https://nvd.nist.gov/
- **API**: https://services.nvd.nist.gov/rest/json/cves/2.0
- **Update Frequency**: Daily
- **Rate Limit**: 5 requests per 30 seconds (public API key)
- **Data Coverage**: 316,000+ CVEs from 1999-present

**EPSS (Exploit Prediction Scoring System)**:
- **URL**: https://www.first.org/epss/
- **API**: https://api.first.org/data/v1/epss
- **Update Frequency**: Daily
- **Rate Limit**: No official limit, but recommend <10 req/sec
- **Data Coverage**: ~95% of CVEs (missing very old CVEs)

**CISA Known Exploited Vulnerabilities (KEV)**:
- **URL**: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- **API**: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
- **Update Frequency**: As threats emerge (check daily)
- **Rate Limit**: No official limit
- **Data Coverage**: ~1,000 CVEs with confirmed exploitation

---

## Data Loading Procedures

### Phase 1: Core Infrastructure (Days 1-2)

**Step 1**: Load 16 Sector nodes
```cypher
UNWIND [
    {name: "Energy", tolerance: 1.0, level: "Zero"},
    {name: "Water", tolerance: 1.0, level: "Zero"},
    // ... all 16 sectors
] AS sectorData

CREATE (s:Sector {
    sectorId: "SECTOR-" + toUpper(sectorData.name),
    sectorName: sectorData.name,
    riskToleranceLevel: sectorData.level,
    riskToleranceInverse: sectorData.tolerance,
    lastUpdated: datetime()
})
```

**Step 2**: Load 30 CognitiveBias nodes
```cypher
UNWIND [
    {name: "Normalcy Bias", severity: 0.85, category: "Risk Perception"},
    {name: "Status Quo Bias", severity: 0.78, category: "Decision Making"},
    // ... all 30 biases
] AS biasData

CREATE (cb:CognitiveBias {
    biasId: "BIAS-" + replace(biasData.name, " ", "-"),
    biasName: biasData.name,
    severityScore: biasData.severity,
    category: biasData.category,
    lastUpdated: datetime()
})
```

### Phase 2: Vulnerability Data (Days 3-5)

**Step 3**: Import CVE nodes from NVD
```cypher
// Use APOC for batch loading
CALL apoc.periodic.iterate(
    "CALL apoc.load.json('nvd_cves.json') YIELD value RETURN value",
    "CREATE (cve:CVE {
        cveId: value.cveId,
        description: value.description,
        cvssBase: value.cvssBase,
        publishDate: date(value.publishDate)
    })",
    {batchSize: 1000}
)
```

**Step 4**: Update CVE nodes with EPSS scores
```cypher
// Load EPSS scores from daily feed
CALL apoc.periodic.iterate(
    "CALL apoc.load.json('epss_scores.json') YIELD value RETURN value",
    "MATCH (cve:CVE {cveId: value.cveId})
     SET cve.epssScore = value.epss,
         cve.epssPercentile = value.percentile,
         cve.epssLastUpdated = date()",
    {batchSize: 1000}
)
```

### Phase 3: Equipment and Organizations (Days 6-8)

**Step 5**: Load Equipment nodes
```cypher
CALL apoc.periodic.iterate(
    "CALL apoc.load.csv('equipment_inventory.csv') YIELD map RETURN map",
    "CREATE (eq:Equipment {
        equipmentId: map.equipmentId,
        equipmentName: map.equipmentName,
        criticalityTier: toInteger(map.criticalityTier),
        criticalityWeight: CASE toInteger(map.criticalityTier)
            WHEN 1 THEN 1.0
            WHEN 2 THEN 0.7
            WHEN 3 THEN 0.4
        END,
        sectorName: map.sectorName
    })",
    {batchSize: 1000}
)
```

**Step 6**: Load Organization nodes with patch history
```cypher
CALL apoc.periodic.iterate(
    "CALL apoc.load.csv('organizations.csv') YIELD map RETURN map",
    "CREATE (org:Organization {
        orgId: map.orgId,
        orgName: map.orgName,
        sectorType: map.sectorType,
        historicalMeanPatchDays: toFloat(map.avgPatchDays),
        totalPatchesAnalyzed: toInteger(map.patchCount)
    })",
    {batchSize: 100}
)
```

### Phase 4: Relationships (Days 9-10)

**Step 7**: Create CVE-Equipment relationships
```cypher
CALL apoc.periodic.iterate(
    "CALL apoc.load.csv('cve_equipment_mapping.csv') YIELD map RETURN map",
    "MATCH (cve:CVE {cveId: map.cveId})
     MATCH (eq:Equipment {equipmentId: map.equipmentId})
     CREATE (cve)-[:AFFECTS]->(eq)",
    {batchSize: 5000}
)
```

**Step 8**: Create Organization-Bias relationships
```cypher
// Detect biases from patch behavior
MATCH (org:Organization)
WHERE org.historicalMeanPatchDays > 30

MATCH (bias:CognitiveBias {biasName: "Normalcy Bias"})

CREATE (org)-[:HAS_BIAS {
    detectedDate: date(),
    evidenceSource: "slow_critical_patching",
    confidenceScore: 0.85
}]->(bias)
```

### Phase 5: Organizational Profiles (Day 11)

**Step 9**: Generate OrganizationalProfile nodes
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

CREATE (profile:OrganizationalProfile {
    profileId: "PROFILE-" + org.orgId,
    orgId: org.orgId,
    sectorType: sector.sectorName,
    biasFactor: biasFactor,
    patchVelocityScore: CASE
        WHEN org.historicalMeanPatchDays < 7 THEN 1.0
        WHEN org.historicalMeanPatchDays < 30 THEN 0.6
        ELSE 0.3
    END,
    riskToleranceInverse: sector.riskToleranceInverse,
    lastUpdated: datetime(),
    confidenceScore: CASE
        WHEN org.totalPatchesAnalyzed >= 100 THEN 0.95
        WHEN org.totalPatchesAnalyzed >= 50 THEN 0.85
        ELSE 0.60
    END
})

CREATE (profile)-[:FOR_ORGANIZATION]->(org)
CREATE (profile)-[:IN_SECTOR]->(sector)
```

---

## Data Quality Validation Checklist

### Pre-Deployment Validation

- [ ] **CVE Nodes**: 316,000+ CVEs loaded
  - [ ] 100% have CVSS scores
  - [ ] ≥95% have EPSS scores
  - [ ] Missing EPSS defaulted to 0.05

- [ ] **Equipment Nodes**: 50,000+ equipment loaded
  - [ ] 100% have criticality tiers (1, 2, or 3)
  - [ ] 100% have sector assignments
  - [ ] Tier distribution: ~7% Tier 1, ~35% Tier 2, ~58% Tier 3

- [ ] **CognitiveBias Nodes**: All 30 biases loaded
  - [ ] All have severity scores (0.0-1.0)
  - [ ] 3 high impact (≥0.7), 7 moderate (0.4-0.7), 20 low (<0.4)

- [ ] **Organization Nodes**: 800+ organizations loaded
  - [ ] ≥90% have patch history (≥50 events)
  - [ ] 100% have sector assignments

- [ ] **OrganizationalProfile Nodes**: 800+ profiles created
  - [ ] ≥90% of organizations have profiles
  - [ ] All profiles have bias factor, patch velocity score, risk tolerance
  - [ ] Average confidence score ≥0.80

- [ ] **Sector Nodes**: All 16 sectors loaded
  - [ ] All have risk tolerance assignments
  - [ ] Risk tolerance distribution: 4 zero, 4 low, 5 moderate, 3 high

- [ ] **Relationships**:
  - [ ] CVE-Equipment: Avg 50-100 CVEs per equipment
  - [ ] Organization-Equipment: Avg 50-100 equipment per org
  - [ ] Organization-Bias: ~25-40% of orgs have bias relationships

### Post-Deployment Monitoring

- [ ] **Daily**: Update EPSS scores for all CVEs
- [ ] **Weekly**: Re-calculate organizational profiles for orgs with new patch events
- [ ] **Monthly**: Validate data quality metrics (missing data, outliers)
- [ ] **Quarterly**: Review bias detection accuracy, tune heuristics if needed

---

## Missing Data Handling

### Default Values

**Missing EPSS Scores**:
- **Default**: 0.05 (conservative estimate)
- **Rationale**: Very old CVEs may not have EPSS predictions
- **Impact**: Lower technical score, likely NEVER priority unless high CVSS

**Missing Equipment Criticality Tier**:
- **Default**: Tier 3 (Standard)
- **Rationale**: Assume non-critical until proven otherwise
- **Impact**: Lower equipment weight (0.4) in technical score

**Missing Organizational Patch History**:
- **Default**: Use sector-level average
- **Rationale**: Organizations without history inherit sector behavior
- **Impact**: Less personalized prioritization, but still actionable

**Missing Cognitive Bias Data**:
- **Default**: Assume low bias (org_bias_factor = 0.8)
- **Rationale**: Optimistic assumption in absence of evidence
- **Impact**: Slightly higher psychological score

---

## Appendices

### Appendix A: Sample Data Files

**CVE Data Sample** (nvd_cves.json):
```json
{
  "cveId": "CVE-2021-44228",
  "description": "Apache Log4j2 <=2.14.1 JNDI features...",
  "cvssBase": 10.0,
  "cvssVector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
  "publishDate": "2021-12-10"
}
```

**EPSS Data Sample** (epss_scores.json):
```json
{
  "cveId": "CVE-2021-44228",
  "epss": 0.97456,
  "percentile": 99.8,
  "date": "2025-11-25"
}
```

**Equipment Data Sample** (equipment_inventory.csv):
```csv
equipmentId,equipmentName,equipmentType,manufacturer,criticalityTier,sectorName
EQ-ENERGY-001,Siemens S7-1500 PLC,Programmable Logic Controller,Siemens,1,Energy
EQ-WATER-023,Schneider Modicon M580,DCS Controller,Schneider Electric,1,Water
EQ-HEALTHCARE-456,GE Healthcare PACS,Medical Imaging System,GE Healthcare,2,Healthcare
```

**Organization Data Sample** (organizations.csv):
```csv
orgId,orgName,sectorType,avgPatchDays,patchCount
ORG-ENERGY-001,Midwest Power Cooperative,Energy,18.4,247
ORG-WATER-012,County Water District,Water,22.1,189
ORG-HEALTHCARE-089,Regional Hospital Network,Healthcare,14.7,312
```

### Appendix B: Data Loading Scripts

See `scripts/load_prerequisites.sh` for complete data loading automation.

---

**END OF PREREQUISITES.md**

**Total Lines**: 1,087
**Status**: COMPLETE - All data prerequisites documented
**Next Steps**: Validate all prerequisite data before Enhancement 12 implementation
