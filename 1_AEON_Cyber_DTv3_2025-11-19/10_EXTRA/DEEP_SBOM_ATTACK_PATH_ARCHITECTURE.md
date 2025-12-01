# Deep SBOM Attack Path Architecture
**File:** DEEP_SBOM_ATTACK_PATH_ARCHITECTURE.md
**Created:** 2025-11-19 (Current System Date)
**Modified:** 2025-11-19
**Version:** v1.0.0
**Author:** System Architecture Designer
**Purpose:** Library-level cyber digital twin with MITRE ATT&CK integration and psychohistory prediction
**Status:** ACTIVE

## Executive Summary

This architecture extends the cyber digital twin to its deepest level: **library-level granularity** with complete attack path modeling and predictive threat intelligence. It enables answering questions like "Which OpenSSL versions are running across our infrastructure and what attack paths do they enable?" and "What's the predicted impact of the next OpenSSL CVE based on our current version distribution?"

### Key Capabilities
- **SBOM-Level Detail**: Track individual software libraries (OpenSSL 1.0.2k vs 3.0.1) across equipment instances
- **Vulnerability Variation**: Model how identical equipment types have different risks based on software versions
- **MITRE ATT&CK Integration**: Complete kill chain modeling from initial access to impact
- **NOW/NEXT/NEVER Prioritization**: Risk-based threat triage framework
- **Library-Level Psychohistory**: Predict future threats based on version distribution and sector patterns

---

## 1. SBOM Detail Architecture

### 1.1 Core Problem Statement

**Current State**: Most cybersecurity models track vulnerabilities at the equipment level ("Cisco ASA 5500 has 12 CVEs").

**Reality**: Vulnerabilities exist at the **library level**. Two identical Cisco ASA 5500 firewalls can have vastly different risk profiles:
- Plant A: Firmware 9.8.4, OpenSSL 1.0.2k → 12 HIGH severity CVEs
- Plant B: Firmware 9.12.2, OpenSSL 3.0.1 → 2 LOW severity CVEs

**Solution**: Model Software Bill of Materials (SBOM) for each equipment instance, tracking individual libraries and their dependencies.

### 1.2 Node Type Definitions

```cypher
// SBOM Node - Software Bill of Materials for specific equipment instance
CREATE CONSTRAINT sbom_id IF NOT EXISTS FOR (s:SBOM) REQUIRE s.sbomId IS UNIQUE;

(:SBOM {
  sbomId: "SBOM-FW-LAW-001-20251119",              // Unique identifier
  equipmentInstanceId: "FW-LAW-001",                // Links to equipment
  generatedDate: datetime("2025-11-19T10:30:00"),  // When SBOM was generated
  format: "SPDX-2.3",                               // SBOM format standard
  toolUsed: "Syft 0.98.0",                          // SBOM generation tool
  completeness: "COMPLETE",                         // COMPLETE | PARTIAL | UNKNOWN
  componentCount: 247,                              // Total software components
  vulnerabilityCount: 12,                           // Total CVEs found
  riskScore: 87.3,                                  // Aggregate risk (0-100)
  lastScanned: datetime("2025-11-19T10:30:00"),    // Last vulnerability scan
  nextScanDue: datetime("2025-11-26T10:30:00")     // Weekly scanning schedule
})

// Software Node - Operating system, firmware, application
CREATE CONSTRAINT software_id IF NOT EXISTS FOR (s:Software) REQUIRE s.softwareId IS UNIQUE;

(:Software {
  softwareId: "SW-CISCO-ASA-9.8.4",
  name: "Cisco ASA Operating System",
  version: "9.8.4",
  vendor: "Cisco Systems",
  productType: "FIRMWARE",                          // FIRMWARE | OS | APPLICATION | SERVICE
  installDate: datetime("2023-03-15T09:00:00"),
  patchStatus: "OUT_OF_DATE",                       // CURRENT | OUT_OF_DATE | EOL
  supportStatus: "DEPRECATED",                      // SUPPORTED | DEPRECATED | EOL
  eolDate: date("2024-12-31"),                      // End of life date
  latestVersion: "9.18.3",                          // Most current version available
  patchVelocity: 180.5,                             // Avg days to patch (sector baseline)
  dependencyCount: 23,                              // Number of library dependencies
  cveCount: 12,                                     // CVEs in this software version
  criticalCveCount: 3                               // Critical severity CVEs
})

// Library Node - Dependency libraries (OpenSSL, zlib, etc.)
CREATE CONSTRAINT library_id IF NOT EXISTS FOR (l:Library) REQUIRE l.libraryId IS UNIQUE;

(:Library {
  libraryId: "LIB-OPENSSL-1.0.2k",
  name: "OpenSSL",
  version: "1.0.2k",
  versionMajor: 1,
  versionMinor: 0,
  versionPatch: 2,
  versionBuild: "k",
  vendor: "OpenSSL Software Foundation",
  language: "C",
  license: "Apache-2.0",                            // License type
  releaseDate: date("2017-01-26"),                  // When this version released
  age_days: 2854,                                   // Days since release (calculated)
  supportStatus: "EOL",                             // SUPPORTED | DEPRECATED | EOL
  eolDate: date("2019-12-31"),                      // End of life
  latestVersion: "3.2.0",                           // Most current version
  versionsBehind: 25,                               // How many major versions behind
  cveCount: 47,                                     // Total CVEs ever in this library
  activeCveCount: 12,                               // CVEs in THIS version
  criticalCveCount: 3,                              // Critical CVEs in this version
  exploitedCveCount: 2,                             // CVEs with known exploits
  patchAvailable: true,                             // Can upgrade to fix?
  patchComplexity: "MEDIUM",                        // EASY | MEDIUM | HARD | BREAKING
  usageCount: 1247,                                 // How many equipment instances use this
  riskScore: 92.7                                   // Composite risk (0-100)
})

// Dependency Relationship - Tracks what depends on what
(:Software)-[:DEPENDS_ON {
  dependencyType: "REQUIRED",                       // REQUIRED | OPTIONAL | DEV | TEST
  versionConstraint: ">=1.0.2",                     // Version requirement
  directDependency: true,                           // Direct vs transitive
  introducedDate: datetime("2023-03-15T09:00:00"), // When dependency added
  canUpgrade: false,                                // Can upgrade without breaking?
  upgradeBlocker: "Cisco firmware compatibility",   // Why can't upgrade?
  riskContribution: 87.3                            // Risk this dep contributes (0-100)
}]->(:Library)

// Library Dependencies - Libraries depend on other libraries
(:Library)-[:REQUIRES {
  versionConstraint: ">=2.7",
  optional: false,
  purpose: "Compression support"
}]->(:Library)
```

### 1.3 Complete Equipment Instance to CVE Chain

```cypher
// Full dependency chain from equipment to vulnerability
(:EquipmentInstance {equipmentId: "FW-LAW-001"})
  -[:HAS_SBOM]->
  (:SBOM {sbomId: "SBOM-FW-LAW-001-20251119"})
  -[:CONTAINS_SOFTWARE]->
  (:Software {softwareId: "SW-CISCO-ASA-9.8.4", version: "9.8.4"})
  -[:DEPENDS_ON {dependencyType: "REQUIRED"}]->
  (:Library {libraryId: "LIB-OPENSSL-1.0.2k", version: "1.0.2k"})
  -[:HAS_CVE]->
  (:CVE {cveId: "CVE-2022-0778", severity: "HIGH", epss: 0.873})
```

### 1.4 Sample Data - LA Water Treatment Scenario

```cypher
// Plant A - High Risk (Outdated Firmware)
MERGE (eqA:EquipmentInstance {
  equipmentId: "FW-LAW-PLANT-A",
  facilityName: "LA Water Treatment Plant A",
  criticality: 95
})

MERGE (sbomA:SBOM {
  sbomId: "SBOM-FW-LAW-PLANT-A-20251119",
  equipmentInstanceId: "FW-LAW-PLANT-A",
  vulnerabilityCount: 12,
  riskScore: 87.3
})

MERGE (swA:Software {
  softwareId: "SW-CISCO-ASA-9.8.4",
  version: "9.8.4",
  patchStatus: "OUT_OF_DATE",
  cveCount: 12
})

MERGE (libA:Library {
  libraryId: "LIB-OPENSSL-1.0.2k",
  version: "1.0.2k",
  activeCveCount: 12,
  riskScore: 92.7
})

MERGE (eqA)-[:HAS_SBOM]->(sbomA)
MERGE (sbomA)-[:CONTAINS_SOFTWARE]->(swA)
MERGE (swA)-[:DEPENDS_ON {dependencyType: "REQUIRED"}]->(libA)

// Plant B - Low Risk (Current Firmware)
MERGE (eqB:EquipmentInstance {
  equipmentId: "FW-LAW-PLANT-B",
  facilityName: "LA Water Treatment Plant B",
  criticality: 95
})

MERGE (sbomB:SBOM {
  sbomId: "SBOM-FW-LAW-PLANT-B-20251119",
  equipmentInstanceId: "FW-LAW-PLANT-B",
  vulnerabilityCount: 2,
  riskScore: 23.1
})

MERGE (swB:Software {
  softwareId: "SW-CISCO-ASA-9.12.2",
  version: "9.12.2",
  patchStatus: "CURRENT",
  cveCount: 2
})

MERGE (libB:Library {
  libraryId: "LIB-OPENSSL-3.0.1",
  version: "3.0.1",
  activeCveCount: 2,
  riskScore: 18.4
})

MERGE (eqB)-[:HAS_SBOM]->(sbomB)
MERGE (sbomB)-[:CONTAINS_SOFTWARE]->(swB)
MERGE (swB)-[:DEPENDS_ON {dependencyType: "REQUIRED"}]->(libB)
```

### 1.5 Key Queries for SBOM Analysis

```cypher
// Q1: Find all equipment with vulnerable OpenSSL versions
MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(:SBOM)
      -[:CONTAINS_SOFTWARE]->(:Software)
      -[:DEPENDS_ON]->(lib:Library)
WHERE lib.name = "OpenSSL"
  AND lib.version < "3.0.0"
RETURN eq.equipmentId, eq.facilityName, lib.version, lib.activeCveCount
ORDER BY lib.riskScore DESC;

// Q2: Vulnerability distribution across equipment fleet
MATCH (prod:EquipmentProduct {name: "Cisco ASA 5500"})
      <-[:INSTANCE_OF]-(eq:EquipmentInstance)
      -[:HAS_SBOM]->(sbom:SBOM)
WITH prod,
     COUNT(eq) AS totalInstances,
     AVG(sbom.vulnerabilityCount) AS avgCves,
     MIN(sbom.vulnerabilityCount) AS minCves,
     MAX(sbom.vulnerabilityCount) AS maxCves
RETURN prod.name, totalInstances, avgCves, minCves, maxCves;

// Q3: Library version distribution (for psychohistory)
MATCH (lib:Library {name: "OpenSSL"})
WITH lib.version AS version, COUNT(*) AS instances
RETURN version, instances
ORDER BY instances DESC;

// Q4: Find equipment most behind on patches
MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(:SBOM)
      -[:CONTAINS_SOFTWARE]->(sw:Software)
WHERE sw.patchStatus = "OUT_OF_DATE"
WITH eq, sw, duration.between(sw.installDate, datetime()).days AS daysBehind
RETURN eq.equipmentId, eq.facilityName, sw.name, sw.version,
       sw.latestVersion, daysBehind
ORDER BY daysBehind DESC
LIMIT 20;

// Q5: Dependency explosion - transitive dependencies
MATCH path = (sw:Software)-[:DEPENDS_ON*1..5]->(lib:Library)
WHERE sw.softwareId = "SW-CISCO-ASA-9.8.4"
RETURN sw.name, LENGTH(path) AS depth,
       COLLECT(DISTINCT lib.name) AS dependencies;
```

---

## 2. Vulnerability Variation Modeling

### 2.1 Problem: Same Equipment, Different Risks

**Challenge**: Equipment product (Cisco ASA 5500) has a generic risk profile, but individual instances have vastly different actual risks based on software versions.

**Solution**: Multi-level risk aggregation with instance-level variation tracking.

### 2.2 Risk Aggregation Levels

```
Level 1: EquipmentProduct (Generic/Average)
  ├─ Aggregates risk across ALL instances
  └─ Properties: avgRiskScore, minRiskScore, maxRiskScore, riskVariance

Level 2: EquipmentInstance (Actual/Specific)
  ├─ Specific risk based on actual SBOM
  └─ Properties: riskScore (from SBOM analysis)

Level 3: Software/Library (Component)
  ├─ Risk contributed by each component
  └─ Properties: componentRiskScore
```

### 2.3 Enhanced EquipmentProduct Node

```cypher
// Add aggregated vulnerability statistics
MATCH (prod:EquipmentProduct)<-[:INSTANCE_OF]-(eq:EquipmentInstance)
      -[:HAS_SBOM]->(sbom:SBOM)
WITH prod,
     COUNT(eq) AS instanceCount,
     AVG(sbom.riskScore) AS avgRisk,
     MIN(sbom.riskScore) AS minRisk,
     MAX(sbom.riskScore) AS maxRisk,
     STDEV(sbom.riskScore) AS riskStdDev,
     PERCENTILE_CONT(sbom.riskScore, 0.50) AS medianRisk,
     PERCENTILE_CONT(sbom.riskScore, 0.95) AS p95Risk
SET prod.instanceCount = instanceCount,
    prod.avgRiskScore = avgRisk,
    prod.minRiskScore = minRisk,
    prod.maxRiskScore = maxRisk,
    prod.riskVariance = riskStdDev,
    prod.medianRiskScore = medianRisk,
    prod.p95RiskScore = p95Risk;

// Classification by risk level
MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(sbom:SBOM)
SET eq.riskCategory =
  CASE
    WHEN sbom.riskScore >= 80 THEN "HIGH"
    WHEN sbom.riskScore >= 40 THEN "MEDIUM"
    ELSE "LOW"
  END;
```

### 2.4 Variation Analysis Queries

```cypher
// Q1: Show all ASA 5500s with HIGH risk
MATCH (prod:EquipmentProduct {name: "Cisco ASA 5500"})
      <-[:INSTANCE_OF]-(eq:EquipmentInstance)
WHERE eq.riskCategory = "HIGH"
RETURN eq.equipmentId, eq.facilityName, eq.riskScore
ORDER BY eq.riskScore DESC;

// Q2: Risk distribution histogram
MATCH (prod:EquipmentProduct {name: "Cisco ASA 5500"})
      <-[:INSTANCE_OF]-(eq:EquipmentInstance)
WITH eq.riskCategory AS category, COUNT(*) AS count
RETURN category, count
ORDER BY
  CASE category
    WHEN "HIGH" THEN 1
    WHEN "MEDIUM" THEN 2
    WHEN "LOW" THEN 3
  END;

// Q3: Version adoption breakdown
MATCH (prod:EquipmentProduct {name: "Cisco ASA 5500"})
      <-[:INSTANCE_OF]-(eq:EquipmentInstance)
      -[:HAS_SBOM]->(:SBOM)-[:CONTAINS_SOFTWARE]->(sw:Software)
WITH sw.version AS version, COUNT(eq) AS instances,
     AVG(eq.riskScore) AS avgRisk
RETURN version, instances, avgRisk
ORDER BY instances DESC;

// Q4: Outlier detection - instances with unusually high risk
MATCH (prod:EquipmentProduct)<-[:INSTANCE_OF]-(eq:EquipmentInstance)
WHERE eq.riskScore > prod.avgRiskScore + (2 * prod.riskVariance)
RETURN eq.equipmentId, eq.riskScore, prod.avgRiskScore,
       (eq.riskScore - prod.avgRiskScore) AS deviationFromMean;

// Q5: Software version lag analysis
MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(:SBOM)
      -[:CONTAINS_SOFTWARE]->(sw:Software)
WITH sw.name AS software,
     sw.latestVersion AS latestVersion,
     COUNT(DISTINCT CASE WHEN sw.version = sw.latestVersion THEN eq END) AS currentCount,
     COUNT(DISTINCT CASE WHEN sw.version <> sw.latestVersion THEN eq END) AS outdatedCount,
     COUNT(DISTINCT eq) AS totalCount
RETURN software, latestVersion,
       currentCount, outdatedCount, totalCount,
       ROUND(100.0 * currentCount / totalCount, 1) AS pctCurrent;
```

---

## 3. MITRE ATT&CK Attack Path Integration

### 3.1 MITRE ATT&CK Framework Overview

MITRE ATT&CK is a knowledge base of adversary tactics and techniques based on real-world observations:
- **14 Tactics**: Strategic goals (Initial Access, Execution, Persistence, etc.)
- **193 Techniques**: Methods to achieve tactical goals (T1190, T1059, etc.)
- **400+ Sub-Techniques**: Specific variants of techniques
- **130+ Groups**: Threat actor organizations
- **700+ Software**: Malware and tools used by attackers

### 3.2 Node Type Definitions

```cypher
// Tactic Node - Strategic goals in attack lifecycle
CREATE CONSTRAINT tactic_id IF NOT EXISTS FOR (t:Tactic) REQUIRE t.tacticId IS UNIQUE;

(:Tactic {
  tacticId: "TA0001",
  name: "Initial Access",
  description: "Techniques to gain initial foothold in network",
  orderInKillChain: 1,
  techniqueCount: 9,
  prevalenceScore: 0.87,                            // How common in attacks (0-1)
  detectionDifficulty: "MEDIUM"                     // EASY | MEDIUM | HARD
})

// Technique Node - Specific attack methods
CREATE CONSTRAINT technique_id IF NOT EXISTS FOR (t:Technique) REQUIRE t.techniqueId IS UNIQUE;

(:Technique {
  techniqueId: "T1190",
  name: "Exploit Public-Facing Application",
  description: "Exploit weaknesses in Internet-facing systems",
  tacticId: "TA0001",
  platforms: ["Windows", "Linux", "Network"],
  dataSourcesRequired: ["Application Log", "Network Traffic"],
  mitigations: ["Network Segmentation", "Privileged Account Management"],
  detectionMethods: ["IDS/IPS", "WAF", "Log Analysis"],
  prevalence: 0.73,                                 // How often used (0-1)
  sophistication: "MEDIUM",                         // LOW | MEDIUM | HIGH | EXPERT
  impactScore: 85.0,                                // Potential impact (0-100)
  detectability: 0.62,                              // How easy to detect (0-1, higher = easier)
  cveCount: 1247,                                   // CVEs associated with this technique
  threatGroupsUsing: 47                             // Number of groups using this
})

// Sub-Technique Node - Specific variants
CREATE CONSTRAINT subtechnique_id IF NOT EXISTS FOR (s:SubTechnique)
  REQUIRE s.subTechniqueId IS UNIQUE;

(:SubTechnique {
  subTechniqueId: "T1190.001",
  name: "Exploit Firewall Vulnerability",
  parentTechniqueId: "T1190",
  description: "Exploit known vulnerabilities in firewall software",
  targetEquipmentTypes: ["Firewall", "UTM", "Next-Gen Firewall"],
  commonCVEs: ["CVE-2022-0778", "CVE-2023-20198"],
  prevalence: 0.41,
  sophistication: "MEDIUM"
})

// Threat Group Node - APT groups and threat actors
CREATE CONSTRAINT threat_group_id IF NOT EXISTS FOR (g:ThreatGroup)
  REQUIRE g.groupId IS UNIQUE;

(:ThreatGroup {
  groupId: "G0016",
  name: "APT29",
  aliases: ["Cozy Bear", "The Dukes"],
  country: "Russia",
  motivation: "ESPIONAGE",                          // ESPIONAGE | FINANCIAL | SABOTAGE
  sophistication: "EXPERT",
  active: true,
  firstSeen: date("2008-01-01"),
  lastActivity: date("2025-10-15"),
  targetedSectors: ["Government", "Energy", "Healthcare"],
  targetedCountries: ["USA", "UK", "Germany"],
  techniquesUsed: 47,
  campaignCount: 23
})

// Procedure Node - How groups use techniques
(:Procedure {
  procedureId: "PROC-APT29-T1190-2025",
  groupId: "G0016",
  techniqueId: "T1190",
  description: "APT29 exploits CVE-2022-0778 in OpenSSL",
  cveExploited: ["CVE-2022-0778"],
  firstObserved: date("2025-03-15"),
  lastObserved: date("2025-10-15"),
  targetEquipment: ["Cisco ASA", "Palo Alto", "Fortinet"],
  successRate: 0.67,                                // Estimated success rate
  detectionRate: 0.31                               // How often detected
})
```

### 3.3 Attack Path Relationships

```cypher
// Tactic → Technique relationship
(:Tactic {tacticId: "TA0001"})-[:HAS_TECHNIQUE]->(:Technique {techniqueId: "T1190"})

// Technique → Sub-Technique
(:Technique {techniqueId: "T1190"})-[:HAS_SUB_TECHNIQUE]->(:SubTechnique {subTechniqueId: "T1190.001"})

// Technique → CVE (what CVEs enable this technique)
(:Technique {techniqueId: "T1190"})-[:EXPLOITS_CVE {
  commonality: 0.87,                                // How often this CVE used for technique
  effectiveness: 0.92,                              // How effective the exploit is
  complexity: "MEDIUM"                              // Exploit complexity
}]->(:CVE {cveId: "CVE-2022-0778"})

// CVE → Library (what libraries have this CVE)
(:CVE {cveId: "CVE-2022-0778"})-[:AFFECTS_LIBRARY]->(:Library {libraryId: "LIB-OPENSSL-1.0.2k"})

// Technique → Equipment (what equipment types are targets)
(:Technique {techniqueId: "T1190"})-[:TARGETS_EQUIPMENT {
  effectiveness: 0.85,
  prevalence: 0.73
}]->(:EquipmentProduct {name: "Cisco ASA 5500"})

// Threat Group → Technique (what groups use what techniques)
(:ThreatGroup {groupId: "G0016"})-[:USES_TECHNIQUE {
  proficiency: "EXPERT",
  frequency: "COMMON",
  firstSeen: date("2023-01-01"),
  lastSeen: date("2025-10-15")
}]->(:Technique {techniqueId: "T1190"})

// Kill Chain Sequence - tactics follow each other
(:Tactic {tacticId: "TA0001", name: "Initial Access"})
  -[:LEADS_TO {probability: 0.87}]->
  (:Tactic {tacticId: "TA0002", name: "Execution"})
  -[:LEADS_TO {probability: 0.73}]->
  (:Tactic {tacticId: "TA0003", name: "Persistence"})
  -[:LEADS_TO {probability: 0.68}]->
  (:Tactic {tacticId: "TA0008", name: "Lateral Movement"})
  -[:LEADS_TO {probability: 0.59}]->
  (:Tactic {tacticId: "TA0040", name: "Impact"})
```

### 3.4 Complete Attack Path Example

```cypher
// LA Water Treatment Plant Attack Scenario
// Complete kill chain from CVE to Impact

// Step 1: Initial Access via CVE-2022-0778
MATCH attackPath =
  (tactic1:Tactic {tacticId: "TA0001", name: "Initial Access"})
  -[:HAS_TECHNIQUE]->
  (tech1:Technique {techniqueId: "T1190", name: "Exploit Public-Facing Application"})
  -[:EXPLOITS_CVE]->
  (cve:CVE {cveId: "CVE-2022-0778"})
  -[:AFFECTS_LIBRARY]->
  (lib:Library {libraryId: "LIB-OPENSSL-1.0.2k"})
  <-[:DEPENDS_ON]-
  (sw:Software {softwareId: "SW-CISCO-ASA-9.8.4"})
  <-[:CONTAINS_SOFTWARE]-
  (:SBOM)
  <-[:HAS_SBOM]-
  (eq:EquipmentInstance {equipmentId: "FW-LAW-PLANT-A"})
  -[:LOCATED_AT]->
  (facility:Facility {name: "LA Water Treatment Plant A"})
  -[:OWNED_BY]->
  (org:Organization {name: "LADWP"})
  -[:OPERATES_IN_SECTOR]->
  (sector:Sector {name: "Water and Wastewater Systems"})

// Step 2: Execution (T1059 - Command and Scripting Interpreter)
  (tactic1)-[:LEADS_TO]->(tactic2:Tactic {tacticId: "TA0002", name: "Execution"})
  -[:HAS_TECHNIQUE]->(tech2:Technique {techniqueId: "T1059"})

// Step 3: Persistence (T1098 - Account Manipulation)
  (tactic2)-[:LEADS_TO]->(tactic3:Tactic {tacticId: "TA0003", name: "Persistence"})
  -[:HAS_TECHNIQUE]->(tech3:Technique {techniqueId: "T1098"})

// Step 4: Impact (T1485 - Data Destruction)
  (tactic3)-[:LEADS_TO]->(tactic4:Tactic {tacticId: "TA0040", name: "Impact"})
  -[:HAS_TECHNIQUE]->(tech4:Technique {techniqueId: "T1485"})

RETURN attackPath;
```

### 3.5 Attack Path Analysis Queries

```cypher
// Q1: Find all attack paths to critical infrastructure
MATCH path = (tech:Technique)-[:EXPLOITS_CVE]->(:CVE)
             -[:AFFECTS_LIBRARY]->(:Library)<-[:DEPENDS_ON]-
             (:Software)<-[:CONTAINS_SOFTWARE]-(:SBOM)
             <-[:HAS_SBOM]-(eq:EquipmentInstance)
WHERE eq.criticality >= 90
RETURN tech.name, LENGTH(path) AS pathLength,
       COLLECT(DISTINCT eq.equipmentId) AS vulnerableEquipment
ORDER BY pathLength;

// Q2: Sector-specific attack techniques
MATCH (sector:Sector {name: "Water and Wastewater Systems"})
      <-[:OPERATES_IN_SECTOR]-(:Organization)<-[:OWNED_BY]-
      (:Facility)<-[:LOCATED_AT]-(eq:EquipmentInstance)
      <-[:TARGETS_EQUIPMENT]-(tech:Technique)
WITH tech, COUNT(DISTINCT eq) AS targetCount
RETURN tech.techniqueId, tech.name, targetCount
ORDER BY targetCount DESC
LIMIT 10;

// Q3: Most dangerous CVEs based on attack path accessibility
MATCH (cve:CVE)<-[:EXPLOITS_CVE]-(tech:Technique)<-[:USES_TECHNIQUE]-(group:ThreatGroup)
WHERE group.active = true
WITH cve, COUNT(DISTINCT tech) AS techniqueCount,
     COUNT(DISTINCT group) AS threatGroupCount
MATCH (cve)-[:AFFECTS_LIBRARY]->(:Library)<-[:DEPENDS_ON]-
      (:Software)<-[:CONTAINS_SOFTWARE]-(:SBOM)<-[:HAS_SBOM]-(eq:EquipmentInstance)
WITH cve, techniqueCount, threatGroupCount, COUNT(DISTINCT eq) AS exposedEquipment
RETURN cve.cveId, techniqueCount, threatGroupCount, exposedEquipment,
       (techniqueCount * threatGroupCount * exposedEquipment) AS dangerScore
ORDER BY dangerScore DESC
LIMIT 20;

// Q4: Simulate attack from Initial Access to Impact
MATCH path = (tactic1:Tactic {name: "Initial Access"})
             -[:LEADS_TO*1..5]->(tacticN:Tactic {name: "Impact"})
WITH path, [t IN nodes(path) | t.name] AS tactics,
     REDUCE(prob = 1.0, rel IN relationships(path) | prob * rel.probability) AS pathProbability
RETURN tactics, pathProbability
ORDER BY pathProbability DESC
LIMIT 5;

// Q5: Find equipment vulnerable to specific threat group's TTPs
MATCH (group:ThreatGroup {groupId: "G0016"})
      -[:USES_TECHNIQUE]->(tech:Technique)
      -[:EXPLOITS_CVE]->(cve:CVE)
      -[:AFFECTS_LIBRARY]->(:Library)<-[:DEPENDS_ON]-
      (:Software)<-[:CONTAINS_SOFTWARE]-(:SBOM)
      <-[:HAS_SBOM]-(eq:EquipmentInstance)
RETURN group.name, COUNT(DISTINCT tech) AS techniques,
       COUNT(DISTINCT cve) AS cves,
       COUNT(DISTINCT eq) AS vulnerableEquipment,
       COLLECT(DISTINCT eq.equipmentId)[0..10] AS sampleEquipment;

// Q6: Detection coverage analysis
MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(:SBOM)
      -[:CONTAINS_SOFTWARE]->(:Software)-[:DEPENDS_ON]->
      (:Library)<-[:AFFECTS_LIBRARY]-(cve:CVE)
      <-[:EXPLOITS_CVE]-(tech:Technique)
WITH eq, tech, cve,
     CASE WHEN tech.detectability > 0.7 THEN "EASY"
          WHEN tech.detectability > 0.4 THEN "MEDIUM"
          ELSE "HARD"
     END AS detectionDifficulty
RETURN eq.equipmentId,
       COUNT(DISTINCT CASE WHEN detectionDifficulty = "HARD" THEN cve END) AS hardToDetect,
       COUNT(DISTINCT cve) AS totalCves,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN detectionDifficulty = "HARD" THEN cve END) /
             COUNT(DISTINCT cve), 1) AS pctHardToDetect;
```

---

## 4. NOW/NEXT/NEVER Prioritization Framework

### 4.1 Prioritization Philosophy

**Problem**: Not all vulnerabilities are equal. Organizations have limited resources and must triage threats effectively.

**Solution**: Multi-factor scoring system that considers:
- **Criticality**: How important is the equipment?
- **Exploitability**: How likely is the vulnerability to be exploited?
- **Impact**: What's the business impact if compromised?
- **Exposure**: Is it public-facing or internal?

### 4.2 Scoring Algorithm

```cypher
// Priority Score Calculation
// Score = (Criticality × 0.30) + (Exploitability × 0.35) + (Impact × 0.25) + (Exposure × 0.10)

// Component Scores (all 0-100):

// 1. Criticality Score (Equipment Importance)
Criticality = equipment.criticality                 // Pre-defined based on role
  × (1 + sectorMultiplier)                          // Critical infrastructure bonus
  × (1 + redundancyPenalty)                         // Reduce if redundant systems exist

// 2. Exploitability Score
Exploitability = (
    cve.epss × 100                                  // EPSS score (0-1) → (0-100)
  + (exploitAvailable ? 30 : 0)                     // Known exploit exists
  + (exploitedInWild ? 40 : 0)                      // Actively exploited
  + (threatGroupsTargeting × 5)                     // APT interest
) / 170 × 100                                       // Normalize to 0-100

// 3. Impact Score
Impact = (
    sector.baseImpactScore                          // Sector baseline (Water = 90)
  + (affectsPublicSafety ? 30 : 0)                  // Life safety concerns
  + (affectsRevenue ? 20 : 0)                       // Financial impact
  + (regulatoryPenalties ? 25 : 0)                  // Compliance issues
) / 165 × 100                                       // Normalize to 0-100

// 4. Exposure Score
Exposure =
    (isPublicFacing ? 100 : 30)                     // Internet exposure
  + (hasRemoteAccess ? 20 : 0)                      // VPN/remote accessible
  - (networkSegmentation ? 20 : 0)                  // Mitigated by segmentation
  - (firewallProtection ? 15 : 0)                   // Mitigated by firewall

// Final Priority Score
PriorityScore =
    (Criticality × 0.30)
  + (Exploitability × 0.35)
  + (Impact × 0.25)
  + (Exposure × 0.10)

// Classification
IF PriorityScore >= 80 THEN "NOW"                   // Immediate action required
ELSE IF PriorityScore >= 40 THEN "NEXT"             // Plan and monitor
ELSE "NEVER"                                        // Accept risk
```

### 4.3 Priority Node Properties

```cypher
// Add priority properties to EquipmentInstance
MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(:SBOM)
      -[:CONTAINS_SOFTWARE]->(:Software)-[:DEPENDS_ON]->
      (:Library)-[:HAS_CVE]->(cve:CVE)
WITH eq, cve,
     // Criticality (from equipment properties)
     eq.criticality AS criticalityScore,

     // Exploitability
     (cve.epss * 100 +
      CASE WHEN cve.exploitAvailable THEN 30 ELSE 0 END +
      CASE WHEN cve.exploitedInWild THEN 40 ELSE 0 END) / 170 * 100 AS exploitabilityScore,

     // Impact (from sector and equipment)
     90.0 AS impactScore,                           // Water sector baseline

     // Exposure
     CASE WHEN eq.isPublicFacing THEN 100 ELSE 30 END AS exposureScore

// Calculate weighted priority
WITH eq, cve,
     (criticalityScore * 0.30 +
      exploitabilityScore * 0.35 +
      impactScore * 0.25 +
      exposureScore * 0.10) AS priorityScore

// Classify
SET eq.priorityScore = priorityScore,
    eq.actionCategory =
      CASE
        WHEN priorityScore >= 80 THEN "NOW"
        WHEN priorityScore >= 40 THEN "NEXT"
        ELSE "NEVER"
      END,
    eq.deadline =
      CASE
        WHEN priorityScore >= 80 THEN datetime() + duration({days: 7})
        WHEN priorityScore >= 40 THEN datetime() + duration({days: 30})
        ELSE NULL
      END;
```

### 4.4 NOW/NEXT/NEVER Queries

```cypher
// Q1: All NOW items requiring immediate action
MATCH (eq:EquipmentInstance {actionCategory: "NOW"})
      -[:HAS_SBOM]->(:SBOM)-[:CONTAINS_SOFTWARE]->(:Software)
      -[:DEPENDS_ON]->(lib:Library)-[:HAS_CVE]->(cve:CVE)
RETURN eq.equipmentId, eq.facilityName, eq.priorityScore, eq.deadline,
       lib.name, lib.version, cve.cveId, cve.severity
ORDER BY eq.priorityScore DESC, eq.deadline ASC;

// Q2: NEXT items for planning
MATCH (eq:EquipmentInstance {actionCategory: "NEXT"})
WITH eq.sector AS sector, COUNT(eq) AS count, AVG(eq.priorityScore) AS avgPriority
RETURN sector, count, avgPriority
ORDER BY count DESC;

// Q3: NEVER items (accepted risk)
MATCH (eq:EquipmentInstance {actionCategory: "NEVER"})
      -[:HAS_SBOM]->(:SBOM)-[:CONTAINS_SOFTWARE]->
      (:Software)-[:DEPENDS_ON]->(lib:Library)-[:HAS_CVE]->(cve:CVE)
RETURN eq.equipmentId, cve.cveId, eq.priorityScore,
       "Mitigated by: " +
       CASE
         WHEN eq.networkSegmentation THEN "Network segmentation, "
         ELSE ""
       END +
       CASE
         WHEN eq.firewallProtection THEN "Firewall protection"
         ELSE ""
       END AS mitigations;

// Q4: Priority distribution by sector
MATCH (eq:EquipmentInstance)-[:LOCATED_AT]->(:Facility)
      -[:OWNED_BY]->(:Organization)-[:OPERATES_IN_SECTOR]->(sector:Sector)
WITH sector.name AS sector, eq.actionCategory AS category, COUNT(eq) AS count
RETURN sector,
       SUM(CASE WHEN category = "NOW" THEN count ELSE 0 END) AS nowCount,
       SUM(CASE WHEN category = "NEXT" THEN count ELSE 0 END) AS nextCount,
       SUM(CASE WHEN category = "NEVER" THEN count ELSE 0 END) AS neverCount
ORDER BY nowCount DESC;

// Q5: Overdue items (past deadline)
MATCH (eq:EquipmentInstance)
WHERE eq.deadline < datetime() AND eq.actionCategory = "NOW"
WITH eq, duration.between(eq.deadline, datetime()).days AS daysOverdue
RETURN eq.equipmentId, eq.facilityName, eq.priorityScore, daysOverdue
ORDER BY daysOverdue DESC;

// Q6: Resource allocation planning
MATCH (eq:EquipmentInstance)
WHERE eq.actionCategory IN ["NOW", "NEXT"]
WITH eq.actionCategory AS category,
     COUNT(eq) AS equipmentCount,
     SUM(eq.remediationCostEstimate) AS totalCost,
     SUM(eq.remediationHoursEstimate) AS totalHours
RETURN category, equipmentCount, totalCost, totalHours,
       ROUND(totalCost / equipmentCount, 0) AS avgCostPerEquipment,
       ROUND(totalHours / equipmentCount, 1) AS avgHoursPerEquipment;
```

---

## 5. Library-Level Psychohistory (Predictive Threat Intelligence)

### 5.1 Psychohistory Concept

**Inspired by**: Isaac Asimov's Foundation series - predicting future trends based on statistical analysis of large populations.

**Application to Cybersecurity**: Predict future vulnerabilities and attack patterns based on:
- Current software version distribution across infrastructure
- Historical patch velocity by sector
- Vulnerability discovery patterns in popular libraries
- Threat actor targeting preferences
- Mathematical modeling of attack probability

### 5.2 Prediction Node Types

```cypher
// FutureThreat Node - Predicted future vulnerabilities
CREATE CONSTRAINT future_threat_id IF NOT EXISTS
  FOR (ft:FutureThreat) REQUIRE ft.threatId IS UNIQUE;

(:FutureThreat {
  threatId: "FT-2026-Q1-OPENSSL",
  libraryName: "OpenSSL",
  predictedVersionAffected: "<=3.0.x",
  predictionDate: date("2025-11-19"),
  predictedDiscoveryDate: date("2026-01-15"),          // Q1 2026
  confidenceScore: 0.73,                                // 0-1 confidence
  predictionBasis: "HISTORICAL_PATTERN",                // HISTORICAL_PATTERN | TREND_ANALYSIS | EXPERT_INPUT
  historicalPrecedent: "CVE discovered every 6mo avg",
  affectedEquipmentEstimate: 1247,                      // Equipment count prediction
  affectedSectors: ["Water", "Healthcare", "Energy"],
  attackProbability: 0.73,                              // Prob of attack within 90 days
  attackWindow: 90,                                     // Days from disclosure to attack
  predictionModel: "EXPONENTIAL_SMOOTHING",
  modelAccuracy: 0.67,                                  // Historical accuracy of model
  recommendedAction: "Accelerate OpenSSL upgrade planning",
  estimatedImpact: 87.3                                 // 0-100 impact score
})

// PredictedIncident Node - Forecasted security events
(:PredictedIncident {
  incidentId: "PI-2026-WATER-OPENSSL",
  predictionDate: date("2025-11-19"),
  predictedOccurrenceDate: date("2026-03-01"),
  targetSector: "Water and Wastewater Systems",
  attackVector: "CVE-2026-XXXXX in OpenSSL <=3.0",
  affectedOrganizations: 23,                            // Estimated count
  estimatedLoss: 45000000,                              // USD
  confidenceScore: 0.68,
  mitigationRecommendations: [
    "Upgrade all OpenSSL to 3.1+",
    "Enhanced monitoring for OpenSSL exploitation",
    "Incident response drill for water sector"
  ],
  similarHistoricalIncidents: ["INC-2022-OPENSSL", "INC-2014-HEARTBLEED"]
})

// VersionDistribution Node - Track version adoption trends
(:VersionDistribution {
  distributionId: "VD-OPENSSL-2025-11-19",
  libraryName: "OpenSSL",
  snapshotDate: date("2025-11-19"),
  totalInstances: 4723,
  versionBreakdown: {
    "3.2.x": 247,     // 5.2%
    "3.1.x": 521,     // 11.0%
    "3.0.x": 892,     // 18.9%
    "1.1.1x": 1456,   // 30.8%
    "1.1.0x": 894,    // 18.9%
    "1.0.2x": 713     // 15.1% ← VULNERABLE
  },
  vulnerableInstances: 713,                             // Count with known CVEs
  pctVulnerable: 15.1,
  patchVelocity: 180.5,                                 // Avg days to patch
  adoptionRate: 0.023,                                  // New version adoption rate/month
  projectedVulnerableIn90Days: 645,                     // Predicted count
  projectedVulnerableIn180Days: 589
})

// SectorPatchProfile Node - Sector-specific patching behavior
(:SectorPatchProfile {
  profileId: "SPP-WATER-2025",
  sectorName: "Water and Wastewater Systems",
  observationPeriod: "2020-2025",
  avgPatchVelocity: 180.5,                              // Days to patch
  medianPatchVelocity: 165.0,
  p95PatchVelocity: 425.0,                              // Slowest 5%
  patchCompletionRate: 0.67,                            // 67% eventually patch
  criticalPatchVelocity: 45.0,                          // For CRITICAL CVEs
  riskTolerance: "MEDIUM",                              // LOW | MEDIUM | HIGH
  budgetConstraints: "HIGH",                            // Budget limitations
  staffingLevel: "UNDERSTAFFED",
  maturityLevel: "DEVELOPING"                           // INITIAL | DEVELOPING | DEFINED | MANAGED | OPTIMIZING
})
```

### 5.3 Prediction Algorithms

```cypher
// Algorithm 1: Historical Pattern Prediction
// Predicts next CVE based on historical discovery frequency

MATCH (lib:Library {name: "OpenSSL"})<-[:AFFECTS_LIBRARY]-(cve:CVE)
WITH lib, cve
ORDER BY cve.publishedDate DESC
WITH lib, COLLECT(cve) AS cves,
     // Calculate average time between CVE discoveries
     AVG(duration.between(
       [c IN cves | c.publishedDate][1..],
       [c IN cves | c.publishedDate][0..-1]
     ).days) AS avgDaysBetweenCves

WITH lib, avgDaysBetweenCves,
     // Last CVE date
     MAX([c IN cves | c.publishedDate]) AS lastCveDate,
     // Predict next CVE date
     MAX([c IN cves | c.publishedDate]) + duration({days: toInteger(avgDaysBetweenCves)}) AS predictedNextCveDate

MERGE (ft:FutureThreat {
  threatId: "FT-" + toString(date(predictedNextCveDate)) + "-" + lib.name
})
SET ft.libraryName = lib.name,
    ft.predictedDiscoveryDate = predictedNextCveDate,
    ft.predictionBasis = "HISTORICAL_PATTERN",
    ft.historicalPrecedent = "CVE every " + toString(toInteger(avgDaysBetweenCves)) + " days avg";

// Algorithm 2: Version Distribution Impact Forecast
// Estimates how many equipment instances will be affected by next CVE

MATCH (lib:Library {name: "OpenSSL"})
WITH lib,
     // Count instances by major version
     COUNT(CASE WHEN lib.versionMajor < 3 THEN 1 END) AS oldVersionCount,
     COUNT(CASE WHEN lib.versionMajor >= 3 THEN 1 END) AS newVersionCount,
     COUNT(*) AS totalCount

MATCH (ft:FutureThreat {libraryName: "OpenSSL"})
SET ft.affectedEquipmentEstimate = oldVersionCount,
    ft.pctFleetAffected = ROUND(100.0 * oldVersionCount / totalCount, 1);

// Algorithm 3: Sector Attack Probability
// Calculates probability of successful attack based on sector patch velocity

MATCH (sector:Sector {name: "Water and Wastewater Systems"})
      <-[:OPERATES_IN_SECTOR]-(:Organization)<-[:OWNED_BY]-
      (:Facility)<-[:LOCATED_AT]-(eq:EquipmentInstance)
      -[:HAS_SBOM]->(:SBOM)-[:CONTAINS_SOFTWARE]->(:Software)
      -[:DEPENDS_ON]->(lib:Library {name: "OpenSSL"})
WHERE lib.versionMajor < 3                              // Vulnerable versions

WITH sector, COUNT(DISTINCT eq) AS vulnerableCount,
     // Get sector patch velocity
     180.5 AS sectorPatchVelocity

// Attack probability model:
// P(attack) = 1 - exp(-λt) where λ = attack_rate, t = patch_velocity
// Higher patch velocity = more time vulnerable = higher probability
WITH sector, vulnerableCount,
     1 - exp(-0.005 * sectorPatchVelocity) AS attackProbability

MERGE (pi:PredictedIncident {
  incidentId: "PI-2026-" + sector.name + "-OPENSSL"
})
SET pi.targetSector = sector.name,
    pi.affectedOrganizations = vulnerableCount,
    pi.attackProbability = attackProbability,
    pi.predictionBasis = "Sector patch velocity: " + toString(sectorPatchVelocity) + " days";

// Algorithm 4: Exponential Smoothing for Trend Forecasting
// Predicts future vulnerable instance count using exponential smoothing

MATCH (vd:VersionDistribution {libraryName: "OpenSSL"})
WITH vd
ORDER BY vd.snapshotDate
WITH COLLECT(vd) AS distributions

// Simple exponential smoothing: S_t = α×Y_t + (1-α)×S_{t-1}
WITH distributions,
     0.3 AS alpha,                                      // Smoothing factor (0-1)
     [d IN distributions | d.vulnerableInstances] AS observations

WITH distributions, alpha, observations,
     REDUCE(s = [toFloat(observations[0])], obs IN observations[1..] |
       s + [alpha * obs + (1 - alpha) * s[-1]]
     ) AS smoothed

WITH distributions[-1] AS latest,
     smoothed[-1] AS currentSmoothed,
     alpha

// Forecast next period
WITH latest, currentSmoothed + alpha * (latest.vulnerableInstances - currentSmoothed) AS forecast90Days

SET latest.projectedVulnerableIn90Days = toInteger(forecast90Days);
```

### 5.4 Psychohistory Queries

```cypher
// Q1: What libraries will likely have CVEs in next 6 months?
MATCH (ft:FutureThreat)
WHERE ft.predictedDiscoveryDate >= date()
  AND ft.predictedDiscoveryDate <= date() + duration({months: 6})
RETURN ft.libraryName, ft.predictedDiscoveryDate, ft.confidenceScore,
       ft.affectedEquipmentEstimate, ft.attackProbability
ORDER BY ft.attackProbability DESC, ft.affectedEquipmentEstimate DESC;

// Q2: Which sectors are most at risk from predicted threats?
MATCH (ft:FutureThreat)-[:THREATENS_SECTOR]->(sector:Sector)
WITH sector,
     COUNT(ft) AS threatCount,
     AVG(ft.attackProbability) AS avgAttackProb,
     SUM(ft.affectedEquipmentEstimate) AS totalExposure
RETURN sector.name, threatCount, avgAttackProb, totalExposure,
       (avgAttackProb * totalExposure) AS riskScore
ORDER BY riskScore DESC;

// Q3: Patch velocity trends - are we getting faster or slower?
MATCH (vd:VersionDistribution {libraryName: "OpenSSL"})
WITH vd
ORDER BY vd.snapshotDate
WITH COLLECT({
  date: vd.snapshotDate,
  patchVelocity: vd.patchVelocity
}) AS timeline

// Calculate trend (simple linear regression)
WITH timeline,
     AVG([t IN timeline | t.patchVelocity]) AS avgVelocity,
     [t IN timeline | t.patchVelocity][0] AS initialVelocity,
     [t IN timeline | t.patchVelocity][-1] AS currentVelocity

RETURN avgVelocity, initialVelocity, currentVelocity,
       currentVelocity - initialVelocity AS velocityChange,
       CASE
         WHEN currentVelocity < initialVelocity THEN "IMPROVING (faster patching)"
         WHEN currentVelocity > initialVelocity THEN "DEGRADING (slower patching)"
         ELSE "STABLE"
       END AS trend;

// Q4: Predict blast radius of next OpenSSL CVE
MATCH (lib:Library {name: "OpenSSL"})
WHERE lib.versionMajor < 3                              // Assume affects <3.0
WITH COUNT(lib) AS vulnerableLibraries

MATCH (lib:Library {name: "OpenSSL"})-[:DEPENDS_ON*0..1]-(sw:Software)
      <-[:CONTAINS_SOFTWARE]-(:SBOM)<-[:HAS_SBOM]-(eq:EquipmentInstance)
WHERE lib.versionMajor < 3
WITH vulnerableLibraries,
     COUNT(DISTINCT eq) AS vulnerableEquipment,
     COUNT(DISTINCT sw) AS vulnerableSoftware

MATCH (eq:EquipmentInstance)-[:LOCATED_AT]->(fac:Facility)
      -[:OWNED_BY]->(org:Organization)
      -[:OPERATES_IN_SECTOR]->(sector:Sector)
WHERE EXISTS {
  MATCH (eq)-[:HAS_SBOM]->(:SBOM)-[:CONTAINS_SOFTWARE]->(:Software)
        -[:DEPENDS_ON]->(lib:Library {name: "OpenSSL"})
  WHERE lib.versionMajor < 3
}
WITH vulnerableLibraries, vulnerableEquipment, vulnerableSoftware,
     COUNT(DISTINCT org) AS vulnerableOrganizations,
     COUNT(DISTINCT sector) AS affectedSectors

RETURN {
  libraryInstances: vulnerableLibraries,
  softwarePackages: vulnerableSoftware,
  equipmentInstances: vulnerableEquipment,
  organizations: vulnerableOrganizations,
  sectors: affectedSectors,
  estimatedImpact: vulnerableEquipment * 10000        // $10K avg remediation cost
} AS blastRadius;

// Q5: Proactive mitigation opportunities
MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(:SBOM)
      -[:CONTAINS_SOFTWARE]->(:Software)-[:DEPENDS_ON]->(lib:Library)
WHERE lib.name IN ["OpenSSL", "zlib", "curl"]           // Common vulnerable libs
  AND lib.supportStatus IN ["DEPRECATED", "EOL"]

MATCH (ft:FutureThreat)
WHERE ft.libraryName = lib.name
  AND ft.predictedDiscoveryDate <= date() + duration({months: 6})

WITH eq, lib, ft,
     // Calculate time to upgrade before predicted CVE
     duration.between(date(), ft.predictedDiscoveryDate).days AS daysUntilThreat

RETURN eq.equipmentId, eq.facilityName,
       lib.name AS library,
       lib.version AS currentVersion,
       lib.latestVersion AS recommendedVersion,
       ft.predictedDiscoveryDate AS threatDate,
       daysUntilThreat,
       CASE
         WHEN daysUntilThreat < 90 THEN "URGENT - upgrade immediately"
         WHEN daysUntilThreat < 180 THEN "HIGH - plan upgrade soon"
         ELSE "MEDIUM - include in next maintenance window"
       END AS recommendation
ORDER BY daysUntilThreat ASC;

// Q6: Historical prediction accuracy
MATCH (ft:FutureThreat)
WHERE ft.predictionDate < date() - duration({months: 3})  // Old enough to validate

// Check if actual CVE appeared
OPTIONAL MATCH (ft)-[:PREDICTED_CVE]->(actual:CVE)
WHERE actual.publishedDate >= ft.predictedDiscoveryDate - duration({days: 30})
  AND actual.publishedDate <= ft.predictedDiscoveryDate + duration({days: 30})

WITH ft, actual,
     CASE WHEN actual IS NOT NULL THEN 1 ELSE 0 END AS hit

WITH COUNT(ft) AS totalPredictions,
     SUM(hit) AS successfulPredictions,
     AVG(ft.confidenceScore) AS avgConfidence

RETURN totalPredictions, successfulPredictions,
       ROUND(100.0 * successfulPredictions / totalPredictions, 1) AS accuracyPct,
       avgConfidence,
       CASE
         WHEN accuracyPct >= 70 THEN "HIGH - trust predictions"
         WHEN accuracyPct >= 50 THEN "MEDIUM - use with caution"
         ELSE "LOW - refine prediction model"
       END AS modelQuality;
```

---

## 6. Complete Neo4j Schema

### 6.1 All Node Types Summary

```cypher
// Equipment Hierarchy
(:EquipmentProduct)        // Generic equipment type
(:EquipmentInstance)       // Specific equipment instance
(:Facility)                // Physical location
(:Organization)            // Owner/operator
(:Sector)                  // Industry sector

// SBOM Detail
(:SBOM)                    // Software Bill of Materials
(:Software)                // OS, firmware, applications
(:Library)                 // Dependencies (OpenSSL, zlib)

// Vulnerability
(:CVE)                     // Common Vulnerabilities and Exposures
(:CWE)                     // Common Weakness Enumeration
(:CAPEC)                   // Common Attack Pattern Enumeration

// MITRE ATT&CK
(:Tactic)                  // Strategic goals (14 tactics)
(:Technique)               // Attack methods (193 techniques)
(:SubTechnique)            // Technique variants (400+)
(:ThreatGroup)             // APT groups, threat actors
(:Procedure)               // How groups use techniques

// Psychohistory / Prediction
(:FutureThreat)            // Predicted vulnerabilities
(:PredictedIncident)       // Forecasted security events
(:VersionDistribution)     // Software version adoption trends
(:SectorPatchProfile)      // Sector-specific patching behavior
```

### 6.2 All Relationship Types

```cypher
// Equipment relationships
(:EquipmentInstance)-[:INSTANCE_OF]->(:EquipmentProduct)
(:EquipmentInstance)-[:LOCATED_AT]->(:Facility)
(:Facility)-[:OWNED_BY]->(:Organization)
(:Organization)-[:OPERATES_IN_SECTOR]->(:Sector)

// SBOM relationships
(:EquipmentInstance)-[:HAS_SBOM]->(:SBOM)
(:SBOM)-[:CONTAINS_SOFTWARE]->(:Software)
(:Software)-[:DEPENDS_ON]->(:Library)
(:Library)-[:REQUIRES]->(:Library)                      // Transitive dependencies

// Vulnerability relationships
(:Library)-[:HAS_CVE]->(:CVE)
(:Software)-[:HAS_CVE]->(:CVE)
(:CVE)-[:AFFECTS_LIBRARY]->(:Library)
(:CVE)-[:CATEGORIZED_AS]->(:CWE)
(:CAPEC)-[:EXPLOITS_CWE]->(:CWE)

// MITRE ATT&CK relationships
(:Tactic)-[:HAS_TECHNIQUE]->(:Technique)
(:Technique)-[:HAS_SUB_TECHNIQUE]->(:SubTechnique)
(:Technique)-[:EXPLOITS_CVE]->(:CVE)
(:Technique)-[:TARGETS_EQUIPMENT]->(:EquipmentProduct)
(:ThreatGroup)-[:USES_TECHNIQUE]->(:Technique)
(:ThreatGroup)-[:TARGETS_SECTOR]->(:Sector)
(:Tactic)-[:LEADS_TO]->(:Tactic)                        // Kill chain sequence

// Prediction relationships
(:FutureThreat)-[:PREDICTS_CVE_IN]->(:Library)
(:FutureThreat)-[:THREATENS_SECTOR]->(:Sector)
(:PredictedIncident)-[:TARGETS_ORGANIZATION]->(:Organization)
(:VersionDistribution)-[:TRACKS_LIBRARY]->(:Library)
```

### 6.3 Constraints and Indexes

```cypher
// Uniqueness constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (eq:EquipmentInstance) REQUIRE eq.equipmentId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (prod:EquipmentProduct) REQUIRE prod.productId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (sbom:SBOM) REQUIRE sbom.sbomId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (sw:Software) REQUIRE sw.softwareId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (lib:Library) REQUIRE lib.libraryId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (cve:CVE) REQUIRE cve.cveId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (tactic:Tactic) REQUIRE tactic.tacticId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (tech:Technique) REQUIRE tech.techniqueId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (group:ThreatGroup) REQUIRE group.groupId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ft:FutureThreat) REQUIRE ft.threatId IS UNIQUE;

// Performance indexes
CREATE INDEX IF NOT EXISTS FOR (eq:EquipmentInstance) ON (eq.criticality);
CREATE INDEX IF NOT EXISTS FOR (eq:EquipmentInstance) ON (eq.riskCategory);
CREATE INDEX IF NOT EXISTS FOR (eq:EquipmentInstance) ON (eq.actionCategory);
CREATE INDEX IF NOT EXISTS FOR (sbom:SBOM) ON (sbom.riskScore);
CREATE INDEX IF NOT EXISTS FOR (lib:Library) ON (lib.name);
CREATE INDEX IF NOT EXISTS FOR (lib:Library) ON (lib.version);
CREATE INDEX IF NOT EXISTS FOR (lib:Library) ON (lib.supportStatus);
CREATE INDEX IF NOT EXISTS FOR (cve:CVE) ON (cve.epss);
CREATE INDEX IF NOT EXISTS FOR (cve:CVE) ON (cve.severity);
CREATE INDEX IF NOT EXISTS FOR (tech:Technique) ON (tech.prevalence);
CREATE INDEX IF NOT EXISTS FOR (ft:FutureThreat) ON (ft.predictedDiscoveryDate);

// Full-text indexes for search
CREATE FULLTEXT INDEX libraryNameSearch IF NOT EXISTS
  FOR (lib:Library) ON EACH [lib.name];
CREATE FULLTEXT INDEX softwareNameSearch IF NOT EXISTS
  FOR (sw:Software) ON EACH [sw.name];
CREATE FULLTEXT INDEX techniqueNameSearch IF NOT EXISTS
  FOR (tech:Technique) ON EACH [tech.name, tech.description];
```

---

## 7. McKenney's 8 Questions Mapped to Deep Queries

### Question 1: What equipment do we have?

```cypher
// SBOM-enhanced equipment inventory
MATCH (eq:EquipmentInstance)-[:INSTANCE_OF]->(prod:EquipmentProduct)
OPTIONAL MATCH (eq)-[:HAS_SBOM]->(sbom:SBOM)
OPTIONAL MATCH (sbom)-[:CONTAINS_SOFTWARE]->(sw:Software)
RETURN eq.equipmentId, prod.name, eq.facilityName,
       sbom.componentCount AS softwareComponents,
       sbom.vulnerabilityCount AS knownVulnerabilities,
       sbom.riskScore AS riskScore,
       COLLECT(DISTINCT sw.name)[0..5] AS sampleSoftware
ORDER BY sbom.riskScore DESC;
```

### Question 2: What vulnerabilities does that equipment have?

```cypher
// Library-level vulnerability breakdown
MATCH (eq:EquipmentInstance {equipmentId: "FW-LAW-PLANT-A"})
      -[:HAS_SBOM]->(:SBOM)-[:CONTAINS_SOFTWARE]->(sw:Software)
      -[:DEPENDS_ON]->(lib:Library)-[:HAS_CVE]->(cve:CVE)
RETURN sw.name AS software,
       lib.name AS library,
       lib.version AS version,
       COUNT(DISTINCT cve) AS cveCount,
       COLLECT(cve.cveId)[0..10] AS sampleCves,
       AVG(cve.epss) AS avgEpss,
       MAX(CASE WHEN cve.severity = "CRITICAL" THEN 1 ELSE 0 END) AS hasCritical
ORDER BY cveCount DESC;
```

### Question 3: What are the consequences of those vulnerabilities?

```cypher
// Attack path and impact analysis
MATCH (eq:EquipmentInstance {equipmentId: "FW-LAW-PLANT-A"})
      -[:HAS_SBOM]->(:SBOM)-[:CONTAINS_SOFTWARE]->(:Software)
      -[:DEPENDS_ON]->(:Library)-[:HAS_CVE]->(cve:CVE)
      <-[:EXPLOITS_CVE]-(tech:Technique)<-[:HAS_TECHNIQUE]-(tactic:Tactic)

// Find complete attack chains leading to Impact
MATCH path = (tactic)-[:LEADS_TO*0..5]->(impactTactic:Tactic {name: "Impact"})

WITH eq, cve, tech, tactic, impactTactic, path,
     REDUCE(prob = 1.0, rel IN relationships(path) | prob * rel.probability) AS attackProb

RETURN cve.cveId,
       tech.name AS initialTechnique,
       [t IN nodes(path) | t.name] AS attackPath,
       attackProb AS successProbability,
       eq.criticality * attackProb * 100 AS impactScore
ORDER BY impactScore DESC
LIMIT 10;
```

### Question 4: What is the threat?

```cypher
// Threat actor targeting analysis
MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(:SBOM)
      -[:CONTAINS_SOFTWARE]->(:Software)-[:DEPENDS_ON]->(:Library)
      -[:HAS_CVE]->(cve:CVE)<-[:EXPLOITS_CVE]-(tech:Technique)
      <-[:USES_TECHNIQUE]-(group:ThreatGroup)
WHERE group.active = true
  AND eq.sector IN group.targetedSectors

WITH group,
     COUNT(DISTINCT cve) AS exploitableCves,
     COUNT(DISTINCT tech) AS techniques,
     COUNT(DISTINCT eq) AS vulnerableEquipment

RETURN group.name, group.country, group.motivation,
       group.sophistication, exploitableCves, techniques,
       vulnerableEquipment,
       group.lastActivity AS lastSeenActive
ORDER BY vulnerableEquipment DESC, exploitableCves DESC;
```

### Question 5: What is the likelihood that threat will be realized?

```cypher
// Likelihood scoring with psychohistory
MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(:SBOM)
      -[:CONTAINS_SOFTWARE]->(:Software)-[:DEPENDS_ON]->(lib:Library)
      -[:HAS_CVE]->(cve:CVE)

// Factors affecting likelihood
WITH eq, cve, lib,
     cve.epss AS exploitProbability,                    // 0-1
     CASE WHEN cve.exploitAvailable THEN 0.8 ELSE 0.2 END AS exploitAvailability,
     CASE WHEN cve.exploitedInWild THEN 0.9 ELSE 0.1 END AS activeExploitation,
     CASE WHEN eq.isPublicFacing THEN 0.9 ELSE 0.3 END AS exposure

// Combined likelihood
WITH eq, cve, lib,
     (exploitProbability * 0.40 +
      exploitAvailability * 0.25 +
      activeExploitation * 0.25 +
      exposure * 0.10) AS likelihood

RETURN eq.equipmentId, cve.cveId, lib.name, lib.version,
       likelihood,
       CASE
         WHEN likelihood >= 0.7 THEN "VERY LIKELY (>70%)"
         WHEN likelihood >= 0.4 THEN "LIKELY (40-70%)"
         WHEN likelihood >= 0.2 THEN "POSSIBLE (20-40%)"
         ELSE "UNLIKELY (<20%)"
       END AS likelihoodCategory
ORDER BY likelihood DESC;
```

### Question 6: What would be the impact if realized?

```cypher
// Multi-dimensional impact analysis
MATCH (eq:EquipmentInstance)-[:LOCATED_AT]->(fac:Facility)
      -[:OWNED_BY]->(org:Organization)
      -[:OPERATES_IN_SECTOR]->(sector:Sector)
MATCH (eq)-[:HAS_SBOM]->(:SBOM)-[:CONTAINS_SOFTWARE]->(:Software)
      -[:DEPENDS_ON]->(:Library)-[:HAS_CVE]->(cve:CVE)

WITH eq, fac, org, sector, cve,
     // Impact dimensions
     eq.criticality AS equipmentCriticality,            // 0-100
     sector.publicSafetyImpact AS safetyImpact,         // 0-100
     org.annualRevenue * 0.001 AS financialImpact,      // $M at risk
     sector.regulatoryPenaltyRisk AS complianceImpact,  // 0-100
     eq.dependentSystemsCount * 10 AS cascadeImpact     // Ripple effects

// Aggregate impact score
WITH eq, cve,
     (equipmentCriticality * 0.30 +
      safetyImpact * 0.35 +
      financialImpact * 0.15 +
      complianceImpact * 0.10 +
      cascadeImpact * 0.10) AS totalImpact

RETURN eq.equipmentId, eq.facilityName, cve.cveId,
       totalImpact,
       CASE
         WHEN totalImpact >= 80 THEN "CATASTROPHIC"
         WHEN totalImpact >= 60 THEN "SEVERE"
         WHEN totalImpact >= 40 THEN "MODERATE"
         WHEN totalImpact >= 20 THEN "MINOR"
         ELSE "NEGLIGIBLE"
       END AS impactCategory
ORDER BY totalImpact DESC;
```

### Question 7: What can we do about it?

```cypher
// Remediation options with cost-benefit analysis
MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(sbom:SBOM)
      -[:CONTAINS_SOFTWARE]->(sw:Software)
      -[:DEPENDS_ON]->(lib:Library)-[:HAS_CVE]->(cve:CVE)
WHERE cve.severity IN ["CRITICAL", "HIGH"]

// Remediation strategies
WITH eq, lib, COUNT(DISTINCT cve) AS cveCount,
     lib.latestVersion AS patchVersion,
     lib.patchComplexity AS patchComplexity

RETURN eq.equipmentId,
       lib.name AS library,
       lib.version AS currentVersion,
       patchVersion AS targetVersion,
       cveCount AS cvesResolved,
       patchComplexity,
       CASE patchComplexity
         WHEN "EASY" THEN "Patch immediately (1-2 hours)"
         WHEN "MEDIUM" THEN "Schedule maintenance window (4-8 hours)"
         WHEN "HARD" THEN "Plan upgrade project (1-2 weeks)"
         WHEN "BREAKING" THEN "Major migration required (1-3 months)"
       END AS recommendation,
       CASE patchComplexity
         WHEN "EASY" THEN 500
         WHEN "MEDIUM" THEN 2000
         WHEN "HARD" THEN 10000
         WHEN "BREAKING" THEN 50000
       END AS estimatedCost,
       cveCount * 10000 AS riskReduction                // $10K per CVE avoided
ORDER BY riskReduction DESC, estimatedCost ASC;
```

### Question 8: Did our actions make a difference?

```cypher
// Before/after risk measurement
// Assumes temporal tracking of SBOM snapshots

MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(sbomNew:SBOM)
WHERE sbomNew.generatedDate = date()

MATCH (eq)-[:HAS_SBOM]->(sbomOld:SBOM)
WHERE sbomOld.generatedDate = date() - duration({days: 30})

WITH eq,
     sbomOld.vulnerabilityCount AS oldVulnCount,
     sbomNew.vulnerabilityCount AS newVulnCount,
     sbomOld.riskScore AS oldRiskScore,
     sbomNew.riskScore AS newRiskScore

WITH eq, oldVulnCount, newVulnCount, oldRiskScore, newRiskScore,
     newVulnCount - oldVulnCount AS vulnDelta,
     newRiskScore - oldRiskScore AS riskDelta,
     CASE
       WHEN newRiskScore < oldRiskScore THEN "IMPROVED"
       WHEN newRiskScore > oldRiskScore THEN "DEGRADED"
       ELSE "UNCHANGED"
     END AS trend

RETURN eq.equipmentId,
       oldVulnCount, newVulnCount, vulnDelta,
       oldRiskScore, newRiskScore, riskDelta,
       trend,
       CASE
         WHEN riskDelta < -20 THEN "SIGNIFICANT IMPROVEMENT"
         WHEN riskDelta < -5 THEN "MODERATE IMPROVEMENT"
         WHEN riskDelta BETWEEN -5 AND 5 THEN "MINIMAL CHANGE"
         WHEN riskDelta > 5 THEN "DEGRADATION - ACTION NEEDED"
       END AS assessment
ORDER BY riskDelta ASC;
```

---

## 8. Implementation Roadmap

### Phase 1: SBOM Foundation (Weeks 1-4)

**Objectives**:
- Implement SBOM, Software, Library nodes
- Build SBOM generation pipeline
- Establish dependency tracking

**Deliverables**:
1. SBOM schema implementation in Neo4j
2. SBOM generation automation (using Syft/SPDX)
3. Library dependency graph construction
4. CVE-to-Library mapping

**Success Criteria**:
- 100% of critical equipment has SBOM
- Library-level vulnerability tracking operational
- Queries return results in <2 seconds

### Phase 2: Vulnerability Variation Modeling (Weeks 5-8)

**Objectives**:
- Implement risk aggregation algorithms
- Build variation analysis queries
- Deploy risk classification system

**Deliverables**:
1. Risk scoring algorithm implementation
2. Equipment classification (HIGH/MEDIUM/LOW)
3. Version distribution tracking
4. Patch lag analysis

**Success Criteria**:
- Risk scores accurate within ±10%
- Can identify all equipment with specific library versions
- Variation analysis queries complete in <5 seconds

### Phase 3: MITRE ATT&CK Integration (Weeks 9-14)

**Objectives**:
- Import MITRE ATT&CK framework
- Build attack path modeling
- Link CVEs to techniques

**Deliverables**:
1. Tactic/Technique/SubTechnique nodes populated
2. ThreatGroup data imported
3. CVE-to-Technique mapping
4. Attack path simulation queries
5. Kill chain probability models

**Success Criteria**:
- Complete MITRE ATT&CK data coverage
- Can simulate attack paths from CVE to Impact
- Threat group targeting analysis operational

### Phase 4: NOW/NEXT/NEVER Prioritization (Weeks 15-18)

**Objectives**:
- Implement prioritization framework
- Build scoring algorithms
- Deploy actionable dashboards

**Deliverables**:
1. Priority scoring algorithm
2. NOW/NEXT/NEVER classification
3. Remediation planning tools
4. Executive dashboards

**Success Criteria**:
- All equipment has priority classification
- NOW items have deadline tracking
- Resource allocation planning tools operational

### Phase 5: Psychohistory Prediction Engine (Weeks 19-24)

**Objectives**:
- Build prediction models
- Implement forecasting algorithms
- Deploy proactive alerting

**Deliverables**:
1. FutureThreat prediction nodes
2. Version distribution tracking
3. Sector patch profile analysis
4. Incident forecasting
5. Proactive mitigation recommendations

**Success Criteria**:
- Predictions generated monthly
- Model accuracy >60% within 90 days
- Proactive recommendations reduce reactive work by 30%

### Phase 6: Validation and Optimization (Weeks 25-30)

**Objectives**:
- Validate against real incidents
- Optimize query performance
- Refine prediction models

**Deliverables**:
1. Historical validation report
2. Query optimization (all <10 seconds)
3. Model accuracy improvements
4. Production deployment

**Success Criteria**:
- Model accuracy >70%
- All queries meet performance SLA
- Production stability >99.5%

---

## 9. Architecture Decision Records (ADRs)

### ADR-001: SBOM Granularity - Library Level vs File Level

**Status**: ACCEPTED

**Context**: SBOM standards support multiple levels of granularity from file-level to library-level to product-level.

**Decision**: Model at **library level** (OpenSSL 1.0.2k) rather than file level (libssl.so.1.0.2k).

**Rationale**:
- Library level provides sufficient granularity for vulnerability management
- File-level tracking creates excessive node count (10-100x more nodes)
- Most CVEs are assigned to library versions, not individual files
- Query performance degradation at file level
- Industry standards (SPDX, CycloneDX) emphasize component/library level

**Consequences**:
- ✅ Manageable graph size (~10M nodes at scale)
- ✅ Fast queries (<10 seconds for complex paths)
- ✅ Aligns with CVE assignment practices
- ❌ Cannot track specific binary file vulnerabilities
- ❌ Loses some precision for compiled vs source analysis

**Alternatives Considered**:
- File-level: Too granular, performance issues
- Product-level only: Too coarse, misses variation
- Hybrid approach: Complexity without benefit

---

### ADR-002: Attack Path Storage - Pre-computed vs Real-time

**Status**: ACCEPTED

**Context**: Attack paths from CVE to Impact can be pre-computed or calculated on-demand.

**Decision**: **Real-time calculation** with aggressive caching of common patterns.

**Rationale**:
- Pre-computing all possible paths creates combinatorial explosion
- Most attack path queries are exploratory and unique
- Graph database is optimized for path traversal
- Caching handles common queries (e.g., "all paths to water sector")
- Flexibility to adjust probability models without recomputation

**Consequences**:
- ✅ Flexible - can change probability models
- ✅ No pre-computation overhead
- ✅ Always current with latest data
- ❌ First query is slower (2-5 seconds)
- ❌ Requires query optimization
- ✅ Subsequent queries are cached (<1 second)

**Alternatives Considered**:
- Pre-computed paths: Storage explosion, inflexible
- Materialized views: Maintenance overhead
- Hybrid: Complexity not justified

---

### ADR-003: Psychohistory Model - Statistical vs Machine Learning

**Status**: ACCEPTED

**Context**: Prediction models can use simple statistical methods or complex ML models.

**Decision**: Start with **statistical methods** (exponential smoothing, linear regression), evolve to ML when data volume justifies.

**Rationale**:
- Initial data volume insufficient for ML (need >1000 incidents)
- Statistical models are interpretable and explainable
- Faster to implement and validate
- Lower computational overhead
- Can evolve to ML as data accumulates

**Consequences**:
- ✅ Fast implementation (weeks vs months)
- ✅ Interpretable results
- ✅ Low computational cost
- ❌ Lower accuracy than potential ML models (60-70% vs 80-90%)
- ✅ Establishes baseline for ML comparison
- ✅ Can hybrid approach later

**Evolution Path**:
- Phase 1: Statistical models (exponential smoothing)
- Phase 2: Ensemble methods (combine multiple statistical models)
- Phase 3: Machine learning (once >1000 validated predictions)
- Phase 4: Deep learning (if accuracy justifies complexity)

---

### ADR-004: NOW/NEXT/NEVER Thresholds - Fixed vs Dynamic

**Status**: ACCEPTED

**Context**: Priority thresholds (80 for NOW, 40 for NEXT) can be fixed or adaptive based on resource capacity.

**Decision**: **Fixed thresholds** with quarterly review and manual adjustment.

**Rationale**:
- Predictable - stakeholders know what NOW means
- Simpler to implement and communicate
- Avoids "moving goalpost" problem
- Can still adjust based on resource capacity
- Annual review allows for calibration

**Consequences**:
- ✅ Consistent prioritization
- ✅ Clear communication
- ✅ Simpler implementation
- ❌ May over/under-allocate resources
- ❌ Doesn't adapt to changing threat landscape automatically
- ✅ Quarterly review mitigates staleness

**Future Enhancement**:
Consider dynamic thresholds when:
- Historical data shows threshold effectiveness
- Resource capacity fluctuates significantly
- Threat landscape changes rapidly

---

### ADR-005: MITRE ATT&CK Version - Fixed Snapshot vs Continuous Update

**Status**: ACCEPTED

**Context**: MITRE ATT&CK framework is updated quarterly with new techniques and groups.

**Decision**: **Quarterly snapshot updates** with version tracking.

**Rationale**:
- Quarterly cadence matches MITRE release schedule
- Version tracking allows historical analysis
- Continuous updates create inconsistency in analysis
- Batch updates are easier to validate and test

**Consequences**:
- ✅ Consistent framework across quarter
- ✅ Easier to validate updates
- ✅ Historical comparisons possible
- ❌ Up to 3-month lag on new techniques
- ✅ Can hotfix critical updates if needed

**Implementation**:
```cypher
(:Technique {
  techniqueId: "T1190",
  mitreVersion: "v14.1",
  lastUpdated: date("2025-10-15")
})
```

---

## 10. Scaling Considerations

### 10.1 Expected Data Volumes

**Assumptions**:
- Large critical infrastructure organization
- 100,000 equipment instances
- Average 50 software components per SBOM
- Average 10 library dependencies per software
- 200,000 known CVEs
- 14 tactics, 193 techniques, 400 sub-techniques

**Node Counts**:
```
EquipmentInstance:      100,000
SBOM:                   100,000
Software:               500,000   (avg 5 unique software versions × 100K equipment)
Library:              2,000,000   (avg 20 unique library versions × 100K equipment)
CVE:                    200,000
Tactic:                      14
Technique:                  193
SubTechnique:               400
ThreatGroup:                130
----------------------------------
Total Nodes:         ~2,900,000
```

**Relationship Counts**:
```
HAS_SBOM:               100,000
CONTAINS_SOFTWARE:      500,000
DEPENDS_ON:           5,000,000   (avg 10 deps per software)
HAS_CVE:              1,000,000   (avg 0.5 CVEs per library)
EXPLOITS_CVE:           100,000   (avg 0.5 techniques per CVE)
----------------------------------
Total Relationships: ~6,700,000
```

**Total Graph Size**: ~10M nodes + relationships

### 10.2 Performance Optimization Strategies

**1. Indexing Strategy**:
```cypher
// Property indexes on frequently queried fields
CREATE INDEX eq_criticality FOR (eq:EquipmentInstance) ON (eq.criticality);
CREATE INDEX eq_risk_category FOR (eq:EquipmentInstance) ON (eq.riskCategory);
CREATE INDEX lib_name FOR (lib:Library) ON (lib.name);
CREATE INDEX lib_version FOR (lib:Library) ON (lib.version);
CREATE INDEX cve_epss FOR (cve:CVE) ON (cve.epss);

// Composite indexes for common query patterns
CREATE INDEX lib_name_version FOR (lib:Library) ON (lib.name, lib.version);
CREATE INDEX eq_criticality_category FOR (eq:EquipmentInstance) ON (eq.criticality, eq.riskCategory);

// Full-text indexes
CREATE FULLTEXT INDEX lib_search FOR (lib:Library) ON EACH [lib.name, lib.vendor];
```

**2. Query Optimization Patterns**:
```cypher
// ❌ SLOW: Unbounded traversal
MATCH path = (eq:EquipmentInstance)-[*]-(cve:CVE)
RETURN path;

// ✅ FAST: Bounded traversal with filters
MATCH path = (eq:EquipmentInstance)-[:HAS_SBOM]->(:SBOM)
             -[:CONTAINS_SOFTWARE]->(:Software)
             -[:DEPENDS_ON]->(lib:Library)
             -[:HAS_CVE]->(cve:CVE)
WHERE eq.criticality > 80 AND cve.severity = "CRITICAL"
RETURN path;

// ❌ SLOW: Multiple separate queries
MATCH (eq:EquipmentInstance {equipmentId: "FW-001"})...
MATCH (eq:EquipmentInstance {equipmentId: "FW-001"})...

// ✅ FAST: Single query with OPTIONAL MATCH
MATCH (eq:EquipmentInstance {equipmentId: "FW-001"})
OPTIONAL MATCH (eq)-[:HAS_SBOM]->(sbom:SBOM)
OPTIONAL MATCH (sbom)-[:CONTAINS_SOFTWARE]->(sw:Software)
RETURN eq, sbom, sw;
```

**3. Caching Strategy**:
- Cache common attack path queries (1 hour TTL)
- Cache version distribution snapshots (24 hour TTL)
- Cache sector aggregations (6 hour TTL)
- Invalidate on data update

**4. Partitioning Strategy**:
```cypher
// Partition by sector for large deployments
(:EquipmentInstance {sector: "Water"})-[:HAS_SBOM]->(:SBOM {sector: "Water"})

// Query only relevant partition
MATCH (eq:EquipmentInstance {sector: "Water"})-[:HAS_SBOM]->...
```

**5. Read Replicas**:
- Primary: Write operations, real-time updates
- Replica 1: Dashboard queries, reporting
- Replica 2: Analytics, psychohistory calculations
- Replica 3: Attack path simulation, exploration

### 10.3 Performance Targets

```yaml
Query Performance SLAs:
  simple_lookup: <100ms              # Single equipment by ID
  sbom_detail: <500ms                # Equipment SBOM with libraries
  vulnerability_list: <1s            # All CVEs for equipment
  attack_path: <3s                   # CVE to Impact path
  sector_aggregation: <5s            # Sector-wide statistics
  prediction_generation: <10s        # Psychohistory forecast

Write Performance SLAs:
  sbom_import: <30s                  # Import single SBOM
  batch_sbom_import: <10min          # Import 1000 SBOMs
  cve_update: <5s                    # Update CVE data

Resource Limits:
  max_memory: 64GB                   # Neo4j heap + page cache
  max_query_time: 30s                # Kill runaway queries
  concurrent_queries: 100            # Max simultaneous queries
```

---

## 11. Conclusion and Next Steps

### 11.1 Architecture Summary

This deep SBOM attack path architecture achieves:

1. **Library-Level Granularity**: Tracks individual software libraries (OpenSSL 1.0.2k) across equipment instances, enabling precise vulnerability variation modeling.

2. **Complete Attack Path Modeling**: Integrates MITRE ATT&CK framework to simulate full kill chains from Initial Access (CVE exploitation) to Impact (infrastructure disruption).

3. **Intelligent Prioritization**: NOW/NEXT/NEVER framework provides risk-based triage using multi-factor scoring (Criticality × Exploitability × Impact × Exposure).

4. **Predictive Threat Intelligence**: Psychohistory engine forecasts future vulnerabilities based on version distribution trends, sector patch velocity, and historical patterns.

5. **Operational Excellence**: Answers McKenney's 8 essential questions with evidence-based queries, enabling data-driven cybersecurity decisions.

### 11.2 Key Innovations

**Beyond Traditional Vulnerability Management**:
- Most systems track CVEs at equipment level ("Cisco ASA has 12 CVEs")
- This architecture tracks at library level ("OpenSSL 1.0.2k has 12 CVEs in Cisco ASA 9.8.4 on Plant A firewall")

**Beyond Static Risk Assessment**:
- Most systems provide point-in-time risk scores
- This architecture predicts future threats and attack probabilities

**Beyond Isolated Vulnerability Data**:
- Most systems treat CVEs as isolated data points
- This architecture models complete attack paths showing how adversaries chain techniques

### 11.3 Immediate Next Steps

**Week 1-2: Validation**
1. Review architecture with cybersecurity stakeholders
2. Validate risk scoring algorithm with historical incidents
3. Refine NOW/NEXT/NEVER thresholds based on organizational capacity

**Week 3-4: Proof of Concept**
1. Implement schema in Neo4j development environment
2. Import SBOM data for 10 representative equipment instances
3. Load MITRE ATT&CK data (tactics, techniques)
4. Execute sample queries and validate results

**Week 5-8: Pilot Deployment**
1. Expand to 100 critical equipment instances
2. Build SBOM generation automation
3. Implement priority scoring algorithm
4. Create executive dashboard for NOW/NEXT/NEVER items

**Week 9-12: Production Rollout**
1. Scale to full equipment inventory
2. Deploy psychohistory prediction engine
3. Integrate with security operations workflows
4. Establish quarterly review cadence

### 11.4 Success Metrics

**Technical Metrics**:
- Query performance: 95% of queries <5 seconds
- Data completeness: 100% of critical equipment has SBOM
- Prediction accuracy: >60% within 90 days (improving to >70% by end of year)

**Business Metrics**:
- Reduce reactive vulnerability response by 30% (through proactive mitigation)
- Prioritization accuracy: 80% of NOW items are actually addressed first
- Time to threat assessment: <1 hour (down from days)
- Executive confidence: Quantified risk scores replace gut feelings

**Operational Metrics**:
- Mean time to vulnerability assessment: <30 minutes
- False positive rate: <10% (NOW items that weren't actually critical)
- Resource utilization: 90% of security team time on HIGH/MEDIUM items

---

## Appendix A: Sample Data - Complete LA Water Scenario

```cypher
// Complete LA Water Treatment Plant scenario with full data

// Organizations and Sectors
MERGE (sector:Sector {
  name: "Water and Wastewater Systems",
  sectorCode: "WWS",
  publicSafetyImpact: 95,
  regulatoryPenaltyRisk: 85,
  criticalInfrastructure: true
})

MERGE (org:Organization {
  name: "Los Angeles Department of Water and Power",
  abbreviation: "LADWP",
  annualRevenue: 4200000000,              // $4.2B
  employeeCount: 10000,
  customerCount: 4000000
})

MERGE (org)-[:OPERATES_IN_SECTOR]->(sector)

// Facilities
MERGE (facA:Facility {
  facilityId: "FAC-LADWP-WTP-A",
  name: "LA Water Treatment Plant A",
  address: "123 Water St, Los Angeles, CA 90012",
  capacity: 500000000,                    // 500M gallons/day
  populationServed: 2000000,
  criticalityLevel: "TIER1"               // Critical infrastructure tier
})

MERGE (facB:Facility {
  facilityId: "FAC-LADWP-WTP-B",
  name: "LA Water Treatment Plant B",
  address: "456 Water Ave, Los Angeles, CA 90013",
  capacity: 300000000,                    // 300M gallons/day
  populationServed: 1200000,
  criticalityLevel: "TIER1"
})

MERGE (facA)-[:OWNED_BY]->(org)
MERGE (facB)-[:OWNED_BY]->(org)

// Equipment Product
MERGE (prod:EquipmentProduct {
  productId: "PROD-CISCO-ASA5500",
  name: "Cisco ASA 5500",
  vendor: "Cisco Systems",
  category: "Firewall",
  avgRiskScore: 55.2,
  minRiskScore: 23.1,
  maxRiskScore: 87.3,
  riskVariance: 24.7
})

// Plant A Equipment (High Risk - Outdated)
MERGE (eqA:EquipmentInstance {
  equipmentId: "FW-LAW-PLANT-A",
  serialNumber: "FCH2134G0QY",
  installDate: date("2018-03-15"),
  criticality: 95,
  isPublicFacing: true,
  networkSegmentation: false,
  firewallProtection: false,
  dependentSystemsCount: 15,
  remediationCostEstimate: 15000,
  remediationHoursEstimate: 40
})

MERGE (eqA)-[:INSTANCE_OF]->(prod)
MERGE (eqA)-[:LOCATED_AT]->(facA)

// Plant B Equipment (Low Risk - Current)
MERGE (eqB:EquipmentInstance {
  equipmentId: "FW-LAW-PLANT-B",
  serialNumber: "FCH2247G1XZ",
  installDate: date("2024-06-20"),
  criticality: 95,
  isPublicFacing: true,
  networkSegmentation: true,
  firewallProtection: true,
  dependentSystemsCount: 12,
  remediationCostEstimate: 3000,
  remediationHoursEstimate: 8
})

MERGE (eqB)-[:INSTANCE_OF]->(prod)
MERGE (eqB)-[:LOCATED_AT]->(facB)

// SBOM for Plant A
MERGE (sbomA:SBOM {
  sbomId: "SBOM-FW-LAW-PLANT-A-20251119",
  equipmentInstanceId: "FW-LAW-PLANT-A",
  generatedDate: datetime("2025-11-19T10:30:00"),
  format: "SPDX-2.3",
  toolUsed: "Syft 0.98.0",
  completeness: "COMPLETE",
  componentCount: 247,
  vulnerabilityCount: 12,
  riskScore: 87.3,
  lastScanned: datetime("2025-11-19T10:30:00"),
  nextScanDue: datetime("2025-11-26T10:30:00")
})

MERGE (eqA)-[:HAS_SBOM]->(sbomA)

// SBOM for Plant B
MERGE (sbomB:SBOM {
  sbomId: "SBOM-FW-LAW-PLANT-B-20251119",
  equipmentInstanceId: "FW-LAW-PLANT-B",
  generatedDate: datetime("2025-11-19T11:15:00"),
  format: "SPDX-2.3",
  toolUsed: "Syft 0.98.0",
  completeness: "COMPLETE",
  componentCount: 289,
  vulnerabilityCount: 2,
  riskScore: 23.1,
  lastScanned: datetime("2025-11-19T11:15:00"),
  nextScanDue: datetime("2025-11-26T11:15:00")
})

MERGE (eqB)-[:HAS_SBOM]->(sbomB)

// Software for Plant A (Outdated)
MERGE (swA:Software {
  softwareId: "SW-CISCO-ASA-9.8.4",
  name: "Cisco ASA Operating System",
  version: "9.8.4",
  vendor: "Cisco Systems",
  productType: "FIRMWARE",
  installDate: datetime("2018-03-15T09:00:00"),
  patchStatus: "OUT_OF_DATE",
  supportStatus: "DEPRECATED",
  eolDate: date("2024-12-31"),
  latestVersion: "9.18.3",
  patchVelocity: 180.5,
  dependencyCount: 23,
  cveCount: 12,
  criticalCveCount: 3
})

MERGE (sbomA)-[:CONTAINS_SOFTWARE]->(swA)

// Software for Plant B (Current)
MERGE (swB:Software {
  softwareId: "SW-CISCO-ASA-9.12.2",
  name: "Cisco ASA Operating System",
  version: "9.12.2",
  vendor: "Cisco Systems",
  productType: "FIRMWARE",
  installDate: datetime("2024-06-20T14:00:00"),
  patchStatus: "CURRENT",
  supportStatus: "SUPPORTED",
  eolDate: date("2028-06-30"),
  latestVersion: "9.18.3",
  patchVelocity: 45.0,
  dependencyCount: 27,
  cveCount: 2,
  criticalCveCount: 0
})

MERGE (sbomB)-[:CONTAINS_SOFTWARE]->(swB)

// Libraries for Plant A (Vulnerable OpenSSL)
MERGE (libA_openssl:Library {
  libraryId: "LIB-OPENSSL-1.0.2k",
  name: "OpenSSL",
  version: "1.0.2k",
  versionMajor: 1,
  versionMinor: 0,
  versionPatch: 2,
  versionBuild: "k",
  vendor: "OpenSSL Software Foundation",
  language: "C",
  license: "Apache-2.0",
  releaseDate: date("2017-01-26"),
  age_days: 2854,
  supportStatus: "EOL",
  eolDate: date("2019-12-31"),
  latestVersion: "3.2.0",
  versionsBehind: 25,
  cveCount: 47,
  activeCveCount: 12,
  criticalCveCount: 3,
  exploitedCveCount: 2,
  patchAvailable: true,
  patchComplexity: "HARD",
  usageCount: 1247,
  riskScore: 92.7
})

MERGE (swA)-[:DEPENDS_ON {
  dependencyType: "REQUIRED",
  versionConstraint: ">=1.0.2",
  directDependency: true,
  introducedDate: datetime("2018-03-15T09:00:00"),
  canUpgrade: false,
  upgradeBlocker: "Cisco firmware compatibility requires ASA OS upgrade",
  riskContribution: 87.3
}]->(libA_openssl)

// Libraries for Plant B (Current OpenSSL)
MERGE (libB_openssl:Library {
  libraryId: "LIB-OPENSSL-3.0.1",
  name: "OpenSSL",
  version: "3.0.1",
  versionMajor: 3,
  versionMinor: 0,
  versionPatch: 1,
  vendor: "OpenSSL Software Foundation",
  language: "C",
  license: "Apache-2.0",
  releaseDate: date("2022-03-15"),
  age_days: 1345,
  supportStatus: "SUPPORTED",
  eolDate: date("2027-03-15"),
  latestVersion: "3.2.0",
  versionsBehind: 2,
  cveCount: 8,
  activeCveCount: 2,
  criticalCveCount: 0,
  exploitedCveCount: 0,
  patchAvailable: true,
  patchComplexity: "EASY",
  usageCount: 892,
  riskScore: 18.4
})

MERGE (swB)-[:DEPENDS_ON {
  dependencyType: "REQUIRED",
  versionConstraint: ">=3.0",
  directDependency: true,
  introducedDate: datetime("2024-06-20T14:00:00"),
  canUpgrade: true,
  upgradeBlocker: NULL,
  riskContribution: 12.1
}]->(libB_openssl)

// CVE that affects Plant A
MERGE (cve:CVE {
  cveId: "CVE-2022-0778",
  publishedDate: date("2022-03-15"),
  severity: "HIGH",
  cvssScore: 7.5,
  cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
  epss: 0.873,
  exploitAvailable: true,
  exploitedInWild: true,
  description: "Infinite loop in BN_mod_sqrt() reachable when parsing certificates",
  affectedVersions: "OpenSSL <1.0.2zd, 1.1.1 <1.1.1n, 3.0 <3.0.2"
})

MERGE (libA_openssl)-[:HAS_CVE]->(cve)
MERGE (cve)-[:AFFECTS_LIBRARY]->(libA_openssl)

// MITRE ATT&CK Tactics
MERGE (tactic1:Tactic {
  tacticId: "TA0001",
  name: "Initial Access",
  description: "Adversary trying to get into your network",
  orderInKillChain: 1,
  techniqueCount: 9,
  prevalenceScore: 0.87,
  detectionDifficulty: "MEDIUM"
})

MERGE (tactic2:Tactic {
  tacticId: "TA0002",
  name: "Execution",
  description: "Adversary trying to run malicious code",
  orderInKillChain: 2,
  techniqueCount: 13,
  prevalenceScore: 0.91,
  detectionDifficulty: "MEDIUM"
})

MERGE (tactic3:Tactic {
  tacticId: "TA0003",
  name: "Persistence",
  description: "Adversary trying to maintain their foothold",
  orderInKillChain: 3,
  techniqueCount: 19,
  prevalenceScore: 0.78,
  detectionDifficulty: "HARD"
})

MERGE (tactic4:Tactic {
  tacticId: "TA0040",
  name: "Impact",
  description: "Adversary trying to manipulate, interrupt, or destroy systems and data",
  orderInKillChain: 14,
  techniqueCount: 13,
  prevalenceScore: 0.65,
  detectionDifficulty: "EASY"
})

// Kill chain progression
MERGE (tactic1)-[:LEADS_TO {probability: 0.87}]->(tactic2)
MERGE (tactic2)-[:LEADS_TO {probability: 0.73}]->(tactic3)
MERGE (tactic3)-[:LEADS_TO {probability: 0.59}]->(tactic4)

// MITRE ATT&CK Techniques
MERGE (tech1:Technique {
  techniqueId: "T1190",
  name: "Exploit Public-Facing Application",
  description: "Adversaries may attempt to exploit weaknesses in Internet-facing systems",
  tacticId: "TA0001",
  platforms: ["Windows", "Linux", "Network"],
  dataSourcesRequired: ["Application Log", "Network Traffic"],
  mitigations: ["Network Segmentation", "Privileged Account Management", "Update Software"],
  detectionMethods: ["IDS/IPS", "WAF", "Log Analysis"],
  prevalence: 0.73,
  sophistication: "MEDIUM",
  impactScore: 85.0,
  detectability: 0.62,
  cveCount: 1247,
  threatGroupsUsing: 47
})

MERGE (tech2:Technique {
  techniqueId: "T1059",
  name: "Command and Scripting Interpreter",
  description: "Adversaries may abuse command and script interpreters to execute commands",
  tacticId: "TA0002",
  platforms: ["Windows", "Linux", "macOS"],
  prevalence: 0.89,
  sophistication: "LOW",
  impactScore: 65.0,
  detectability: 0.58
})

MERGE (tech3:Technique {
  techniqueId: "T1098",
  name: "Account Manipulation",
  description: "Adversaries may manipulate accounts to maintain access to victim systems",
  tacticId: "TA0003",
  platforms: ["Windows", "Linux", "Azure AD", "Office 365"],
  prevalence: 0.54,
  sophistication: "MEDIUM",
  impactScore: 75.0,
  detectability: 0.45
})

MERGE (tech4:Technique {
  techniqueId: "T1485",
  name: "Data Destruction",
  description: "Adversaries may destroy data and files on specific systems or in large numbers",
  tacticId: "TA0040",
  platforms: ["Windows", "Linux", "macOS"],
  prevalence: 0.31,
  sophistication: "LOW",
  impactScore: 95.0,
  detectability: 0.72
})

// Link tactics to techniques
MERGE (tactic1)-[:HAS_TECHNIQUE]->(tech1)
MERGE (tactic2)-[:HAS_TECHNIQUE]->(tech2)
MERGE (tactic3)-[:HAS_TECHNIQUE]->(tech3)
MERGE (tactic4)-[:HAS_TECHNIQUE]->(tech4)

// Link technique to CVE
MERGE (tech1)-[:EXPLOITS_CVE {
  commonality: 0.87,
  effectiveness: 0.92,
  complexity: "MEDIUM"
}]->(cve)

// Link technique to equipment type
MERGE (tech1)-[:TARGETS_EQUIPMENT {
  effectiveness: 0.85,
  prevalence: 0.73
}]->(prod)

// Threat Group
MERGE (group:ThreatGroup {
  groupId: "G0016",
  name: "APT29",
  aliases: ["Cozy Bear", "The Dukes"],
  country: "Russia",
  motivation: "ESPIONAGE",
  sophistication: "EXPERT",
  active: true,
  firstSeen: date("2008-01-01"),
  lastActivity: date("2025-10-15"),
  targetedSectors: ["Government", "Energy", "Water", "Healthcare"],
  targetedCountries: ["USA", "UK", "Germany", "France"],
  techniquesUsed: 47,
  campaignCount: 23
})

MERGE (group)-[:USES_TECHNIQUE {
  proficiency: "EXPERT",
  frequency: "COMMON",
  firstSeen: date("2022-01-01"),
  lastSeen: date("2025-10-15")
}]->(tech1)

MERGE (group)-[:TARGETS_SECTOR]->(sector)

// Calculate and set priority scores for equipment
MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(sbom:SBOM)
SET eq.priorityScore =
  CASE eq.equipmentId
    WHEN "FW-LAW-PLANT-A" THEN 87.3      // NOW - immediate action
    WHEN "FW-LAW-PLANT-B" THEN 32.1      // NEVER - accept risk
  END,
  eq.actionCategory =
    CASE eq.equipmentId
      WHEN "FW-LAW-PLANT-A" THEN "NOW"
      WHEN "FW-LAW-PLANT-B" THEN "NEVER"
    END,
  eq.deadline =
    CASE eq.equipmentId
      WHEN "FW-LAW-PLANT-A" THEN datetime() + duration({days: 7})
      ELSE NULL
    END;

// Future Threat Prediction
MERGE (ft:FutureThreat {
  threatId: "FT-2026-Q1-OPENSSL",
  libraryName: "OpenSSL",
  predictedVersionAffected: "<=3.0.x",
  predictionDate: date("2025-11-19"),
  predictedDiscoveryDate: date("2026-01-15"),
  confidenceScore: 0.73,
  predictionBasis: "HISTORICAL_PATTERN",
  historicalPrecedent: "OpenSSL CVE discovered every 180 days avg since 2014",
  affectedEquipmentEstimate: 1247,
  affectedSectors: ["Water", "Healthcare", "Energy"],
  attackProbability: 0.73,
  attackWindow: 90,
  predictionModel: "EXPONENTIAL_SMOOTHING",
  modelAccuracy: 0.67,
  recommendedAction: "Accelerate OpenSSL upgrade planning for all <3.0 versions",
  estimatedImpact: 87.3
})

MERGE (ft)-[:PREDICTS_CVE_IN]->(libA_openssl)
MERGE (ft)-[:THREATENS_SECTOR]->(sector);
```

---

**End of Architecture Document**

This architecture provides the deepest level of cyber digital twin modeling, enabling true library-level threat intelligence with predictive capabilities. It answers not just "What equipment do we have?" but "What attack paths exist through our infrastructure, which threats will emerge next quarter, and how should we prioritize our limited resources?"
