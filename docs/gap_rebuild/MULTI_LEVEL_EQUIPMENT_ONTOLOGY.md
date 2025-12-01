# Multi-Level Equipment Ontology Architecture
## Digital Twin Psychohistory Modeling - Equipment & Instance Design

**File**: MULTI_LEVEL_EQUIPMENT_ONTOLOGY.md
**Created**: 2025-11-19 (based on system date)
**Purpose**: Comprehensive ontology design for multi-level equipment representation
**Status**: ARCHITECTURE SPECIFICATION

---

## Executive Summary

This document presents a **6-level ontology architecture** that solves the fundamental challenge of representing equipment across multiple abstraction levels:

- **Reference Architecture**: Generic equipment types used across all 16 critical infrastructure sectors
- **Customer Instances**: Specific equipment installations with unique asset IDs and configurations
- **20-Hop Relationships**: Deep traversal paths for psychohistory modeling and predictive analytics
- **Zero Duplication**: Single canonical representation of each equipment model with multiple instances
- **Dual Analysis**: Support both sector-level patterns and customer-specific impact assessment

**Core Innovation**: Separation of **Equipment Product** (template/reference) from **Equipment Instance** (deployment) with rich relationship semantics enabling both cross-sector analysis and customer-specific threat correlation.

---

## Problem Statement & Requirements

### The Fundamental Challenge

**Current Problem**:
- A "Cisco ASA 5500 Firewall" exists in Water, Healthcare, Chemical, Manufacturing sectors
- Creating separate equipment nodes per sector → **16x duplication**
- Each customer has specific instances with different:
  - Firmware versions (9.8 vs 9.12)
  - Configurations (different ACLs, VPN configs)
  - Vulnerability exposure (patched vs unpatched)
  - Physical locations (LA Water Plant vs Chicago Hospital)

**Required Capabilities**:
1. **Query**: "What equipment types are common in Water sector?" (reference architecture)
2. **Query**: "Show Customer X's specific equipment inventory" (instance details)
3. **Query**: "Which customers are affected by CVE-2024-1234 in Cisco ASA?" (threat correlation)
4. **Query**: "Predict future attack patterns on Healthcare sector" (psychohistory)
5. **Scale**: Support 16 sectors × 500 equipment types × 100 customers = **800,000+ instances**

### McKenney's 8 Critical Questions Mapping

| Question | Ontology Support |
|----------|------------------|
| **What happened?** | HistoricalIncident → EquipmentInstance → Organization |
| **Who did it?** | ThreatActor → ATTACKTechnique → TargetedEquipment |
| **How did they do it?** | CVE → SoftwareComponent → EquipmentInstance |
| **What assets are at risk?** | EquipmentProduct → Instances → Sector → Criticality |
| **What's the business impact?** | EquipmentInstance → Facility → Organization → Operations |
| **What patterns exist?** | HistoricalIncident aggregation by Sector/Equipment |
| **What will happen next?** | PredictiveModel trained on Equipment×Threat patterns |
| **How do we prevent it?** | SecurityControl → EquipmentInstance → Mitigation |

---

## Multi-Level Architecture Design

### Level 0: Equipment Taxonomy (Reference Classification)

**Purpose**: Hierarchical classification of all equipment types across sectors

```cypher
// Equipment Taxonomy Structure
(:EquipmentCategory {
  categoryId: "NET_SECURITY",
  name: "Network Security Equipment",
  description: "Equipment protecting network boundaries"
})
  → [:HAS_SUBCATEGORY] →
(:EquipmentSubcategory {
  subcategoryId: "FIREWALL",
  name: "Firewall",
  description: "Network packet filtering and access control"
})
  → [:HAS_PRODUCT_LINE] →
(:ProductLine {
  lineId: "CISCO_ASA",
  manufacturer: "Cisco Systems",
  name: "Adaptive Security Appliance (ASA)",
  firstRelease: "2005-05-01"
})
  → [:HAS_PRODUCT] →
(:EquipmentProduct {
  productId: "cisco-asa-5500",
  manufacturer: "Cisco Systems",
  model: "ASA 5500-X Series",
  category: "Firewall",
  productLine: "ASA",
  endOfLife: "2025-12-31",
  supportStatus: "active"
})
```

**Key Properties**:
```yaml
EquipmentCategory:
  - categoryId: Unique identifier
  - name: Human-readable name
  - description: Classification purpose

EquipmentSubcategory:
  - subcategoryId: Unique identifier
  - name: Subcategory name
  - commonUses: ["perimeter defense", "internal segmentation"]

ProductLine:
  - lineId: Product line identifier
  - manufacturer: Vendor name
  - evolutionPath: Timeline of product development

EquipmentProduct:
  - productId: Canonical unique identifier (PRIMARY KEY)
  - manufacturer: Vendor name
  - model: Product model number
  - specifications: {cpu, memory, throughput, ports}
  - certifications: ["FIPS 140-2", "Common Criteria"]
```

### Level 1: Equipment Instances (Customer Deployments)

**Purpose**: Specific physical/virtual equipment installations with unique identities

```cypher
// Equipment Instance - Specific Deployment
(:EquipmentInstance {
  assetId: "FW-LAW-001",              // Unique asset identifier
  hostname: "la-water-fw-primary",    // Network hostname
  serialNumber: "JAD214801ABC",       // Hardware serial
  ipAddress: "10.50.10.1",            // Management IP
  installDate: "2020-03-15",          // Deployment date
  status: "operational",              // Current status
  criticality: "high",                // Business criticality
  maintenanceWindow: "Sunday 02:00-06:00",
  lastAudit: "2025-10-15"
})
  → [:INSTANCE_OF] → (:EquipmentProduct {productId: "cisco-asa-5500"})
  → [:INSTALLED_AT] → (:Facility {facilityId: "LAW-TP-001"})
  → [:OWNED_BY] → (:Organization {orgId: "LADWP"})
  → [:MANAGED_BY] → (:Team {teamId: "LAW-IT-SECURITY"})
  → [:HAS_CONFIGURATION] → (:Configuration {configId: "cfg-fw-law-001"})
```

**Instance Lifecycle States**:
```yaml
status_values:
  - operational: Normal production operation
  - maintenance: Scheduled maintenance window
  - degraded: Operating with reduced capability
  - offline: Not operational
  - decommissioned: Removed from service

criticality_levels:
  - critical: Failure causes immediate service disruption
  - high: Failure impacts multiple systems
  - medium: Failure impacts single system
  - low: Failure has minimal impact
```

### Level 2: Software Components (SBOM Integration)

**Purpose**: Software installed on equipment with version tracking and vulnerability correlation

```cypher
// Software Component on Equipment Instance
(:SoftwareComponent {
  componentId: "sw-cisco-asa-os-9.8.4",
  name: "Cisco ASA Operating System",
  version: "9.8.4.25",
  vendor: "Cisco Systems",
  cpe: "cpe:2.3:o:cisco:adaptive_security_appliance:9.8.4",
  releaseDate: "2019-11-15",
  supportEnds: "2024-12-31",
  knownVulnerabilities: 12
})
  → [:INSTALLED_ON] → (:EquipmentInstance {assetId: "FW-LAW-001"})
  → [:HAS_VULNERABILITY] → (:CVE {cveId: "CVE-2024-1234"})
  → [:PART_OF_SBOM] → (:SBOM {
      sbomId: "sbom-fw-law-001-v1",
      format: "CycloneDX",
      generated: "2025-10-01",
      components: 47
    })
  → [:DEPENDS_ON] → (:SoftwareComponent {name: "OpenSSL", version: "1.0.2k"})
```

**SBOM Relationships**:
```cypher
// Software Dependency Chain
(:SoftwareComponent {name: "Cisco ASA OS"})
  → [:DEPENDS_ON] → (:SoftwareComponent {name: "OpenSSL"})
    → [:HAS_VULNERABILITY] → (:CVE {cveId: "CVE-2022-0778"})
      → [:AFFECTS_INSTANCE] → (:EquipmentInstance)
        → [:OWNED_BY] → (:Organization)

// Version Progression
(:SoftwareComponent {version: "9.8.4"})
  → [:SUPERSEDED_BY] → (:SoftwareComponent {version: "9.12.3"})
    → [:FIXES_CVE] → (:CVE {cveId: "CVE-2024-1234"})
```

### Level 3: Organizational Hierarchy

**Purpose**: Map equipment to facilities, organizations, business units, and sectors

```cypher
// Complete Organizational Hierarchy
(:EquipmentInstance {assetId: "FW-LAW-001"})
  → [:INSTALLED_AT] →
(:Facility {
  facilityId: "LAW-TP-001",
  name: "LA Water Treatment Plant - Sylmar",
  type: "water_treatment",
  address: "13600 Glenoaks Blvd, Sylmar, CA 91342",
  coordinates: {lat: 34.3194, lon: -118.4358},
  capacity: "600 MGD",
  population_served: 4000000,
  regulatory_tier: "Tier 1 - Critical"
})
  → [:OPERATED_BY] →
(:Organization {
  orgId: "LADWP",
  name: "Los Angeles Department of Water and Power",
  type: "municipal_utility",
  employees: 10000,
  established: "1902",
  regulatoryId: "CA-WATER-001"
})
  → [:PART_OF] →
(:BusinessUnit {
  unitId: "LADWP-WATER-OPS",
  name: "Water Operations Division",
  budget: "$2.1B",
  facilities_count: 47
})
  → [:WITHIN_SECTOR] →
(:Sector {
  sectorId: "WATER",
  name: "Water and Wastewater Systems Sector",
  cisaDesignation: "Critical Infrastructure Sector #16",
  nationalPriority: "high",
  regulatoryFramework: ["SDWA", "CWA", "AWIA"]
})
```

**Multi-Tenancy Support**:
```cypher
// Equipment Owned by Multiple Organizations (Shared Infrastructure)
(:EquipmentInstance {assetId: "SHARED-SCADA-01"})
  → [:OWNED_BY {percentage: 60}] → (:Organization {name: "City Water"})
  → [:OWNED_BY {percentage: 40}] → (:Organization {name: "County Water"})
  → [:MANAGED_BY] → (:ManagedServiceProvider {name: "SCADA MSP Inc"})
```

### Level 4: Threat Intelligence Integration

**Purpose**: Connect equipment to threat actors, techniques, and vulnerabilities

```cypher
// Threat Intelligence Chain
(:CVE {
  cveId: "CVE-2024-1234",
  cvss: 9.8,
  description: "Remote code execution in Cisco ASA web interface",
  published: "2024-01-15",
  exploitAvailable: true,
  exploitPublished: "2024-01-20",
  patchAvailable: true,
  patchVersion: "9.8.4.30"
})
  → [:AFFECTS_VERSION] → (:SoftwareComponent {version: "9.8.4.25"})
    → [:INSTALLED_ON] → (:EquipmentInstance {assetId: "FW-LAW-001"})
      → [:TARGETED_BY] → (:ThreatActor {
          actorId: "APT28",
          aliases: ["Fancy Bear", "Sofacy"],
          motivation: "espionage",
          targetSectors: ["water", "energy", "government"]
        })
        → [:USES_TECHNIQUE] → (:ATTACKTechnique {
            techniqueId: "T1190",
            name: "Exploit Public-Facing Application",
            tactic: "Initial Access"
          })
          → [:EXPLOITS_WEAKNESS] → (:CWE {
              cweId: "CWE-78",
              name: "OS Command Injection"
            })

// Historical Incident Pattern
(:HistoricalIncident {
  incidentId: "INC-2023-0847",
  date: "2023-06-15",
  sector: "water",
  targetedEquipment: "Cisco ASA",
  attackVector: "CVE exploitation",
  impactLevel: "high"
})
  → [:SIMILAR_TO] → (:PredictedIncident {
      predictionId: "PRED-2025-0023",
      probability: 0.78,
      targetSector: "water",
      targetEquipment: "Cisco ASA",
      timeframe: "Q1 2025"
    })
```

### Level 5: Predictive Analytics (Psychohistory Layer)

**Purpose**: Enable future threat prediction through pattern analysis

```cypher
// Psychohistory Modeling
(:PredictiveModel {
  modelId: "PSYCH-WATER-FIREWALL-v3",
  algorithm: "Temporal Graph Neural Network",
  trained: "2025-10-01",
  accuracy: 0.82,
  trainingPeriod: "2020-2025",
  incidentsAnalyzed: 1247
})
  → [:ANALYZES_PATTERN] →
(:AttackPattern {
  patternId: "AP-WATER-001",
  name: "Water Sector Firewall Exploitation",
  frequency: "monthly",
  seasonality: "summer_peak",
  confidence: 0.85
})
  → [:TARGETS_EQUIPMENT_TYPE] → (:EquipmentProduct {model: "ASA 5500"})
    → [:HAS_VULNERABLE_INSTANCES] → (:EquipmentInstance)
      → [:GENERATES_FORECAST] →
(:ThreatForecast {
  forecastId: "FC-2025-Q1-WATER",
  period: "2025-Q1",
  predictedAttacks: 23,
  highestRiskOrgs: ["LADWP", "SF Water", "Seattle Water"],
  recommendedActions: ["patch_asa_firmware", "enhanced_monitoring"]
})
```

### Level 6: Defensive Posture & Controls

**Purpose**: Map security controls and defensive capabilities to equipment

```cypher
// Security Controls Applied to Equipment
(:SecurityControl {
  controlId: "SC-7",
  framework: "NIST 800-53",
  name: "Boundary Protection",
  implementation: "Cisco ASA Firewall"
})
  → [:IMPLEMENTED_BY] → (:EquipmentInstance {assetId: "FW-LAW-001"})
    → [:HAS_CONFIGURATION] →
(:Configuration {
  configId: "cfg-fw-law-001",
  version: "v2.3",
  lastUpdate: "2025-09-15",
  approvedBy: "Security Team",
  complianceStatus: "compliant"
})
  → [:INCLUDES_RULE] →
(:FirewallRule {
  ruleId: "rule-001",
  action: "deny",
  source: "any",
  destination: "SCADA_VLAN",
  port: "any",
  protocol: "any",
  log: true
})

// Defensive Capability Assessment
(:Organization {name: "LADWP"})
  → [:HAS_DEFENSIVE_POSTURE] →
(:DefensiveCapability {
  maturityLevel: "Level 3 - Defined",
  framework: "CMMC",
  lastAssessment: "2025-08-01",
  strengths: ["network_security", "monitoring"],
  gaps: ["endpoint_detection", "threat_hunting"]
})
```

---

## 20-Hop Relationship Paths

### Path 1: SBOM → Customer Impact (14 hops)

**Use Case**: "Trace a vulnerable software component to all affected customers"

```cypher
MATCH path = (sbom:SBOM)
  -[:CONTAINS]-> (sw:SoftwareComponent)
  -[:HAS_VERSION]-> (ver:Version)
  -[:HAS_VULNERABILITY]-> (cve:CVE)
  -[:EXPLOITED_BY]-> (ta:ThreatActor)
  -[:USES_TECHNIQUE]-> (att:ATTACKTechnique)
  -[:INSTALLED_ON]-> (ei:EquipmentInstance)
  -[:INSTANCE_OF]-> (ep:EquipmentProduct)
  -[:LOCATED_AT]-> (f:Facility)
  -[:OPERATED_BY]-> (o:Organization)
  -[:PART_OF]-> (bu:BusinessUnit)
  -[:WITHIN_SECTOR]-> (s:Sector)
  -[:SUBJECT_TO]-> (reg:Regulation)
  -[:ENFORCED_BY]-> (rb:RegulatoryBody)
WHERE cve.cvss > 7.0
RETURN path
```

### Path 2: Threat Actor → Vulnerable Equipment (16 hops)

**Use Case**: "Identify equipment targeted by specific threat actor campaigns"

```cypher
MATCH path = (ta:ThreatActor)
  -[:CONDUCTS_CAMPAIGN]-> (tc:ThreatCampaign)
  -[:USES_TECHNIQUE]-> (att:ATTACKTechnique)
  -[:EXPLOITS_CVE]-> (cve:CVE)
  -[:AFFECTS_SOFTWARE]-> (sw:SoftwareComponent)
  -[:INSTALLED_ON]-> (ei:EquipmentInstance)
  -[:INSTANCE_OF]-> (ep:EquipmentProduct)
  -[:COMMON_IN_SECTOR]-> (s:Sector)
  -[:HAS_THREAT_LANDSCAPE]-> (tl:ThreatLandscape)
  -[:INCLUDES_ACTOR]-> (ta2:ThreatActor)
  -[:TARGETS_TECHNOLOGY]-> (tech:Technology)
  -[:USED_IN_PRODUCT]-> (ep2:EquipmentProduct)
  -[:HAS_INSTANCE]-> (ei2:EquipmentInstance)
  -[:OWNED_BY]-> (o:Organization)
  -[:HAS_RISK_PROFILE]-> (rp:RiskProfile)
  -[:PREDICTS_INCIDENT]-> (pi:PredictedIncident)
WHERE ta.name = "APT28"
RETURN path
```

### Path 3: Equipment → Psychohistory Prediction (20 hops - FULL CHAIN)

**Use Case**: "Generate predictive threat forecast from equipment vulnerability patterns"

```cypher
MATCH path = (ep:EquipmentProduct)
  -[:HAS_INSTANCE]-> (ei:EquipmentInstance)                    // 1
  -[:INSTALLED_AT]-> (f:Facility)                              // 2
  -[:OPERATED_BY]-> (o:Organization)                           // 3
  -[:WITHIN_SECTOR]-> (s:Sector)                               // 4
  -[:HAS_THREAT_LANDSCAPE]-> (tl:ThreatLandscape)              // 5
  -[:INCLUDES_ACTOR]-> (ta:ThreatActor)                        // 6
  -[:USES_TECHNIQUE]-> (att:ATTACKTechnique)                   // 7
  -[:EXPLOITS_WEAKNESS]-> (cwe:CWE)                            // 8
  -[:MANIFESTS_AS]-> (cve:CVE)                                 // 9
  -[:AFFECTS_SOFTWARE]-> (sw:SoftwareComponent)                // 10
  -[:PART_OF_SBOM]-> (sbom:SBOM)                               // 11
  -[:DESCRIBES_EQUIPMENT]-> (ei2:EquipmentInstance)            // 12
  -[:INVOLVED_IN_INCIDENT]-> (hi:HistoricalIncident)           // 13
  -[:EXHIBITS_PATTERN]-> (ap:AttackPattern)                    // 14
  -[:ANALYZED_BY]-> (pm:PredictiveModel)                       // 15
  -[:GENERATES_FORECAST]-> (tf:ThreatForecast)                 // 16
  -[:RECOMMENDS_CONTROL]-> (sc:SecurityControl)                // 17
  -[:IMPLEMENTED_BY_EQUIPMENT]-> (ei3:EquipmentInstance)       // 18
  -[:HAS_DEFENSIVE_CAPABILITY]-> (dc:DefensiveCapability)      // 19
  -[:ENABLES_RESILIENCE]-> (rp:ResilienceProfile)              // 20
WHERE ep.model = "ASA 5500"
RETURN path
```

### Path 4: CVE → Cross-Sector Impact Analysis (18 hops)

**Use Case**: "Analyze how a single CVE affects multiple sectors through equipment propagation"

```cypher
MATCH path = (cve:CVE)
  -[:AFFECTS_VERSION]-> (sw:SoftwareComponent)                 // 1
  -[:INSTALLED_ON]-> (ei:EquipmentInstance)                    // 2
  -[:INSTANCE_OF]-> (ep:EquipmentProduct)                      // 3
  -[:DEPLOYED_IN_SECTOR]-> (s1:Sector)                         // 4
  -[:SHARES_INFRASTRUCTURE]-> (s2:Sector)                      // 5
  -[:HAS_ORGANIZATION]-> (o:Organization)                      // 6
  -[:OPERATES_FACILITY]-> (f:Facility)                         // 7
  -[:CONTAINS_EQUIPMENT]-> (ei2:EquipmentInstance)             // 8
  -[:HAS_SOFTWARE]-> (sw2:SoftwareComponent)                   // 9
  -[:DEPENDS_ON]-> (sw3:SoftwareComponent)                     // 10
  -[:HAS_VULNERABILITY]-> (cve2:CVE)                           // 11
  -[:CHAINED_WITH]-> (cve)                                     // 12 (back to original)
  -[:EXPLOITABLE_BY]-> (ta:ThreatActor)                        // 13
  -[:TARGETS_SECTOR]-> (s3:Sector)                             // 14
  -[:HAS_CRITICAL_ASSET]-> (ca:CriticalAsset)                  // 15
  -[:SUPPORTED_BY_EQUIPMENT]-> (ei3:EquipmentInstance)         // 16
  -[:FAILURE_IMPACTS]-> (bi:BusinessImpact)                    // 17
  -[:REQUIRES_RESPONSE]-> (ir:IncidentResponse)                // 18
WHERE cve.cvss >= 9.0
RETURN path,
       COUNT(DISTINCT s1) as affectedSectors,
       COUNT(DISTINCT o) as affectedOrganizations
```

---

## Anti-Duplication Strategy

### Problem: Equipment Used Across Multiple Sectors

**Scenario**: A "Cisco ASA 5500 Firewall" is used in:
- Water sector (LA Water Plant)
- Healthcare sector (Chicago Hospital)
- Chemical sector (Texas Refinery)
- Manufacturing sector (Detroit Auto Plant)

**❌ WRONG APPROACH - Creates Duplication**:
```cypher
// Creating separate equipment nodes per sector
CREATE (w:Equipment {name: "Cisco ASA 5500", sector: "Water"})
CREATE (h:Equipment {name: "Cisco ASA 5500", sector: "Healthcare"})
CREATE (c:Equipment {name: "Cisco ASA 5500", sector: "Chemical"})
// Result: 16 duplicate nodes for same equipment model
```

**✅ CORRECT APPROACH - Single Canonical Product**:
```cypher
// Create ONE canonical product
MERGE (ep:EquipmentProduct {productId: "cisco-asa-5500"})
  SET ep.manufacturer = "Cisco Systems",
      ep.model = "ASA 5500-X Series",
      ep.category = "Firewall"

// Create multiple instances pointing to same product
CREATE (ei1:EquipmentInstance {
  assetId: "FW-LAW-001",
  sector: "Water"
})
  -[:INSTANCE_OF]-> (ep)

CREATE (ei2:EquipmentInstance {
  assetId: "FW-CHH-047",
  sector: "Healthcare"
})
  -[:INSTANCE_OF]-> (ep)

// Result: 1 product node, N instance nodes
```

### Uniqueness Constraints

```cypher
// Ensure canonical equipment products
CREATE CONSTRAINT equipment_product_unique
  FOR (ep:EquipmentProduct)
  REQUIRE ep.productId IS UNIQUE;

// Ensure unique asset identifiers
CREATE CONSTRAINT equipment_instance_unique
  FOR (ei:EquipmentInstance)
  REQUIRE ei.assetId IS UNIQUE;

// Ensure unique SBOM identifiers
CREATE CONSTRAINT sbom_unique
  FOR (s:SBOM)
  REQUIRE s.sbomId IS UNIQUE;

// Composite key for software components
CREATE CONSTRAINT software_component_unique
  FOR (sw:SoftwareComponent)
  REQUIRE (sw.name, sw.version, sw.vendor) IS UNIQUE;
```

### Sector Association Strategy

**Approach**: Associate equipment with sectors **through relationships**, not properties

```cypher
// WRONG: Sector as property (requires duplication)
(:Equipment {model: "ASA 5500", sector: "Water"})

// CORRECT: Sector through relationship chain
(:EquipmentInstance)
  -[:OWNED_BY]-> (:Organization)
  -[:WITHIN_SECTOR]-> (:Sector {name: "Water"})

// Query equipment common in a sector
MATCH (s:Sector {name: "Water"})
      <-[:WITHIN_SECTOR]-(o:Organization)
      <-[:OWNED_BY]-(ei:EquipmentInstance)
      -[:INSTANCE_OF]->(ep:EquipmentProduct)
WITH ep, COUNT(DISTINCT ei) as deployments
WHERE deployments > 5
RETURN ep.manufacturer, ep.model, deployments
ORDER BY deployments DESC
```

### Equipment Taxonomy Benefits

**Hierarchical Classification Prevents Duplication**:

```cypher
// Single taxonomy, multiple associations
(:EquipmentCategory {name: "Network Security"})
  -[:HAS_SUBCATEGORY]-> (:Subcategory {name: "Firewall"})
    -[:HAS_PRODUCT]-> (:EquipmentProduct {model: "ASA 5500"})
      -[:INSTANCE_OF]<- (:EquipmentInstance {assetId: "FW-001"})
        -[:OWNED_BY]-> (:Organization {sector: "Water"})
      -[:INSTANCE_OF]<- (:EquipmentInstance {assetId: "FW-047"})
        -[:OWNED_BY]-> (:Organization {sector: "Healthcare"})

// ONE taxonomy tree, multiple deployment branches
```

---

## Query Examples for Dual Analysis

### Query 1: Reference Architecture - Typical Equipment in Water Sector

**Use Case**: "What equipment types are commonly deployed in Water sector?"

```cypher
// Aggregate equipment by type across Water sector
MATCH (s:Sector {name: "Water and Wastewater Systems Sector"})
      <-[:WITHIN_SECTOR]-(o:Organization)
      <-[:OWNED_BY]-(ei:EquipmentInstance)
      -[:INSTANCE_OF]->(ep:EquipmentProduct)
WITH ep,
     COUNT(DISTINCT ei) as instanceCount,
     COUNT(DISTINCT o) as organizationCount,
     COLLECT(DISTINCT o.name)[..5] as sampleOrgs
RETURN ep.manufacturer as Manufacturer,
       ep.model as Model,
       ep.category as Category,
       instanceCount as TotalInstances,
       organizationCount as Organizations,
       (instanceCount * 1.0 / organizationCount) as AvgPerOrg,
       sampleOrgs as ExampleOrganizations
ORDER BY instanceCount DESC
LIMIT 50

// Expected Output:
// Manufacturer    Model           Category    Instances  Orgs  AvgPerOrg
// Cisco Systems   ASA 5500        Firewall    234        87    2.69
// Schneider       SCADA RTU       PLC         189        45    4.20
// Siemens         S7-1500         PLC         156        62    2.52
```

### Query 2: Instance Architecture - Customer X's Specific Equipment

**Use Case**: "Show detailed inventory for Los Angeles Dept of Water"

```cypher
// Customer-specific equipment inventory
MATCH (o:Organization {orgId: "LADWP"})
      <-[:OWNED_BY]-(ei:EquipmentInstance)
      -[:INSTANCE_OF]->(ep:EquipmentProduct)
OPTIONAL MATCH (ei)-[:HAS_SOFTWARE]->(sw:SoftwareComponent)
OPTIONAL MATCH (ei)-[:INSTALLED_AT]->(f:Facility)
OPTIONAL MATCH (sw)-[:HAS_VULNERABILITY]->(cve:CVE)
WITH ei, ep, f,
     COLLECT(DISTINCT sw.name + " " + sw.version) as software,
     COUNT(DISTINCT cve) as vulnCount,
     MAX(cve.cvss) as maxCVSS
RETURN ei.assetId as AssetID,
       ei.hostname as Hostname,
       ep.manufacturer + " " + ep.model as Equipment,
       f.name as Facility,
       ei.status as Status,
       ei.criticality as Criticality,
       software as InstalledSoftware,
       vulnCount as Vulnerabilities,
       maxCVSS as HighestCVSS
ORDER BY ei.criticality DESC, vulnCount DESC

// Expected Output:
// AssetID      Hostname            Equipment         Facility              Status      Crit    Software                      Vulns  MaxCVSS
// FW-LAW-001   la-water-fw-01      Cisco ASA 5500    LA Water Plant        operational high    ["Cisco ASA OS 9.8.4"]        3      9.8
// SCADA-001    la-scada-primary    Schneider RTU     LA SCADA Center       operational critical["Modicon OS 2.1"]            0      0.0
```

### Query 3: Threat Correlation - CVE Impact Analysis

**Use Case**: "Which customers are affected by CVE-2024-1234?"

```cypher
// CVE impact across customer base
MATCH (cve:CVE {cveId: "CVE-2024-1234"})
      -[:AFFECTS_VERSION]->(sw:SoftwareComponent)
      <-[:HAS_SOFTWARE]-(ei:EquipmentInstance)
      -[:OWNED_BY]->(o:Organization)
      -[:WITHIN_SECTOR]->(s:Sector)
OPTIONAL MATCH (ei)-[:INSTALLED_AT]->(f:Facility)
OPTIONAL MATCH (ei)-[:INSTANCE_OF]->(ep:EquipmentProduct)
WITH o, s, cve,
     COUNT(DISTINCT ei) as affectedAssets,
     COLLECT(DISTINCT ei.assetId) as assetIds,
     COLLECT(DISTINCT f.name) as facilities,
     COLLECT(DISTINCT ep.model) as equipmentModels,
     MAX(ei.criticality) as highestCriticality
RETURN o.name as Customer,
       s.name as Sector,
       affectedAssets as AffectedAssets,
       assetIds as AssetIDs,
       facilities as Facilities,
       equipmentModels as EquipmentTypes,
       highestCriticality as MaxCriticality,
       cve.cvss as CVSSScore,
       cve.exploitAvailable as ExploitPublic
ORDER BY affectedAssets DESC, cve.cvss DESC

// Expected Output:
// Customer                          Sector      Assets  AssetIDs              Facilities                MaxCrit   CVSS  ExploitPublic
// LA Dept of Water and Power        Water       12      ["FW-LAW-001", ...]   ["LA Water Plant", ...]   critical  9.8   true
// SF Public Utilities Commission    Water       8       ["FW-SF-003", ...]    ["SF Treatment", ...]     high      9.8   true
// Chicago Dept of Water Management  Water       6       ["FW-CHI-012", ...]   ["Chicago Plant 1", ...]  high      9.8   true
```

### Query 4: Psychohistory - Predictive Threat Analysis

**Use Case**: "Predict future attack patterns on Healthcare sector"

```cypher
// Predictive threat modeling for Healthcare sector
MATCH (s:Sector {name: "Healthcare and Public Health"})
      <-[:WITHIN_SECTOR]-(o:Organization)
      <-[:OWNED_BY]-(ei:EquipmentInstance)
      -[:INSTANCE_OF]->(ep:EquipmentProduct)
      <-[:USED_IN_INCIDENT]-(hi:HistoricalIncident)
      -[:USED_TECHNIQUE]->(att:ATTACKTechnique)
      <-[:USES_TECHNIQUE]-(ta:ThreatActor)
OPTIONAL MATCH (ei)-[:HAS_SOFTWARE]->(sw:SoftwareComponent)
                   -[:HAS_VULNERABILITY]->(cve:CVE)
WITH s, ep, ta, att,
     COUNT(DISTINCT hi) as historicalIncidents,
     COUNT(DISTINCT ei) as deployedInstances,
     COUNT(DISTINCT cve) as knownVulnerabilities,
     AVG(cve.cvss) as avgSeverity,
     MAX(hi.date) as lastIncident
WHERE knownVulnerabilities > 0
WITH s, ep, ta, att, historicalIncidents, deployedInstances,
     knownVulnerabilities, avgSeverity, lastIncident,
     (knownVulnerabilities * deployedInstances * avgSeverity / 100.0) as threatScore
ORDER BY threatScore DESC
LIMIT 20
RETURN ep.category as EquipmentType,
       ep.manufacturer + " " + ep.model as Product,
       deployedInstances as Deployments,
       knownVulnerabilities as Vulnerabilities,
       avgSeverity as AvgCVSS,
       historicalIncidents as PastAttacks,
       lastIncident as MostRecentAttack,
       threatScore as PredictiveThreatScore,
       COLLECT(DISTINCT ta.name)[..3] as ThreateningActors,
       COLLECT(DISTINCT att.name)[..3] as CommonTechniques

// Expected Output:
// EquipmentType    Product              Deployments  Vulns  AvgCVSS  Attacks  Recent      ThreatScore  Actors                    Techniques
// PACS System      GE Centricity 5.0    2,341        23     8.2      47       2025-09-12  442.8        ["APT28","Lazarus","..."] ["T1190","T1078","..."]
// Medical Device   Philips IntelliVue   1,892        18     7.8      32       2025-08-23  265.4        ["APT41","Sandworm"]      ["T1210","T1021"]
// EHR Server       Epic Systems 2023    1,456        12     8.9      28       2025-10-01  155.2        ["FIN7","APT29"]          ["T1133","T1566"]
```

### Query 5: Cross-Sector Equipment Analysis

**Use Case**: "Show equipment models used across multiple sectors"

```cypher
// Identify equipment with cross-sector deployment
MATCH (ei:EquipmentInstance)-[:INSTANCE_OF]->(ep:EquipmentProduct),
      (ei)-[:OWNED_BY]->(o:Organization)-[:WITHIN_SECTOR]->(s:Sector)
WITH ep,
     COLLECT(DISTINCT s.name) as sectors,
     COUNT(DISTINCT s) as sectorCount,
     COUNT(DISTINCT ei) as totalInstances,
     COUNT(DISTINCT o) as orgCount
WHERE sectorCount > 1
RETURN ep.manufacturer as Manufacturer,
       ep.model as Model,
       ep.category as Category,
       sectorCount as SectorsUsedIn,
       sectors as SectorList,
       totalInstances as TotalDeployments,
       orgCount as Organizations
ORDER BY sectorCount DESC, totalInstances DESC
LIMIT 25

// Expected Output:
// Manufacturer      Model            Category    Sectors  SectorList                              Deployments  Orgs
// Cisco Systems     ASA 5500         Firewall    16       ["Water","Healthcare","Chemical",...]   3,247        1,023
// Schneider         Modicon M580     PLC         14       ["Water","Energy","Chemical",...]       2,891        876
// Palo Alto         PA-5200          Firewall    13       ["Healthcare","Finance","Energy",...]   2,134        654
```

### Query 6: Equipment Lifecycle & Upgrade Path

**Use Case**: "Identify equipment reaching end-of-life requiring replacement"

```cypher
// Equipment approaching end-of-life analysis
MATCH (ei:EquipmentInstance)-[:INSTANCE_OF]->(ep:EquipmentProduct),
      (ei)-[:OWNED_BY]->(o:Organization),
      (ei)-[:INSTALLED_AT]->(f:Facility)
WHERE ep.endOfLife < date("2026-12-31")
OPTIONAL MATCH (ep)-[:SUPERSEDED_BY]->(ep_new:EquipmentProduct)
WITH o, f, ei, ep, ep_new,
     duration.between(date(), date(ep.endOfLife)).months as monthsRemaining
RETURN o.name as Organization,
       f.name as Facility,
       ei.assetId as AssetID,
       ep.manufacturer + " " + ep.model as CurrentEquipment,
       ep.endOfLife as EndOfLife,
       monthsRemaining as MonthsRemaining,
       ei.criticality as Criticality,
       COALESCE(ep_new.model, "No replacement identified") as RecommendedReplacement,
       CASE
         WHEN monthsRemaining < 6 THEN "URGENT"
         WHEN monthsRemaining < 12 THEN "HIGH"
         WHEN monthsRemaining < 24 THEN "MEDIUM"
         ELSE "LOW"
       END as UpgradePriority
ORDER BY monthsRemaining ASC, ei.criticality DESC

// Expected Output:
// Organization    Facility          AssetID      CurrentEquipment     EOL         Months  Crit     Replacement        Priority
// LADWP          LA Water Plant    FW-LAW-001   Cisco ASA 5500       2025-12-31  1       critical  ASA 5500-X v2     URGENT
// SF Water       SF Treatment      RTU-SF-012   Schneider M340       2026-03-31  4       high      Modicon M580      URGENT
```

---

## Neo4j Schema Implementation

### Complete Cypher Schema

```cypher
// ============================================================================
// MULTI-LEVEL EQUIPMENT ONTOLOGY - COMPLETE NEO4J SCHEMA
// ============================================================================

// ----------------------------------------------------------------------------
// LEVEL 0: EQUIPMENT TAXONOMY (Reference Classification)
// ----------------------------------------------------------------------------

// Equipment Categories
CREATE (category_net_sec:EquipmentCategory {
  categoryId: "NET_SECURITY",
  name: "Network Security Equipment",
  description: "Equipment protecting network boundaries and traffic"
});

CREATE (category_control:EquipmentCategory {
  categoryId: "CONTROL_SYSTEMS",
  name: "Industrial Control Systems",
  description: "SCADA, PLC, DCS, and industrial automation equipment"
});

CREATE (category_server:EquipmentCategory {
  categoryId: "SERVERS",
  name: "Server Infrastructure",
  description: "Physical and virtual servers, databases, application servers"
});

// Equipment Subcategories
CREATE (subcat_firewall:EquipmentSubcategory {
  subcategoryId: "FIREWALL",
  name: "Firewall",
  description: "Network packet filtering and access control"
})
  -[:PARENT_CATEGORY]-> (category_net_sec);

CREATE (subcat_ids:EquipmentSubcategory {
  subcategoryId: "IDS_IPS",
  name: "Intrusion Detection/Prevention System",
  description: "Network traffic monitoring and threat detection"
})
  -[:PARENT_CATEGORY]-> (category_net_sec);

CREATE (subcat_plc:EquipmentSubcategory {
  subcategoryId: "PLC",
  name: "Programmable Logic Controller",
  description: "Industrial automation control systems"
})
  -[:PARENT_CATEGORY]-> (category_control);

CREATE (subcat_scada:EquipmentSubcategory {
  subcategoryId: "SCADA",
  name: "Supervisory Control and Data Acquisition",
  description: "Process monitoring and control systems"
})
  -[:PARENT_CATEGORY]-> (category_control);

// Product Lines
CREATE (line_cisco_asa:ProductLine {
  lineId: "CISCO_ASA",
  manufacturer: "Cisco Systems",
  name: "Adaptive Security Appliance (ASA)",
  firstRelease: "2005-05-01",
  status: "active"
})
  -[:PRODUCT_LINE_TYPE]-> (subcat_firewall);

CREATE (line_schneider_modicon:ProductLine {
  lineId: "SCHNEIDER_MODICON",
  manufacturer: "Schneider Electric",
  name: "Modicon PLC Family",
  firstRelease: "1968-01-01",
  status: "active"
})
  -[:PRODUCT_LINE_TYPE]-> (subcat_plc);

CREATE (line_siemens_s7:ProductLine {
  lineId: "SIEMENS_S7",
  manufacturer: "Siemens",
  name: "SIMATIC S7 Controller Series",
  firstRelease: "1994-01-01",
  status: "active"
})
  -[:PRODUCT_LINE_TYPE]-> (subcat_plc);

// Equipment Products (Canonical Templates)
CREATE (prod_asa_5500:EquipmentProduct {
  productId: "cisco-asa-5500",
  manufacturer: "Cisco Systems",
  model: "ASA 5500-X Series",
  category: "Firewall",
  productLine: "ASA",
  releaseDate: "2012-06-01",
  endOfLife: "2025-12-31",
  supportStatus: "active",
  specifications: {
    throughput: "10 Gbps",
    maxConnections: 500000,
    formFactor: "1U rack-mount",
    powerConsumption: "300W"
  },
  certifications: ["FIPS 140-2", "Common Criteria EAL4+"]
})
  -[:PRODUCT_IN_LINE]-> (line_cisco_asa);

CREATE (prod_modicon_m580:EquipmentProduct {
  productId: "schneider-modicon-m580",
  manufacturer: "Schneider Electric",
  model: "Modicon M580",
  category: "PLC",
  productLine: "Modicon",
  releaseDate: "2012-01-01",
  endOfLife: "2030-12-31",
  supportStatus: "active",
  specifications: {
    cpu: "1.2 GHz",
    memory: "64 MB",
    ioModules: 32,
    communicationPorts: ["Ethernet", "Modbus", "USB"]
  },
  certifications: ["IEC 61131-3", "IEC 61508 SIL3"]
})
  -[:PRODUCT_IN_LINE]-> (line_schneider_modicon);

CREATE (prod_siemens_s7_1500:EquipmentProduct {
  productId: "siemens-s7-1500",
  manufacturer: "Siemens",
  model: "SIMATIC S7-1500",
  category: "PLC",
  productLine: "SIMATIC S7",
  releaseDate: "2013-01-01",
  endOfLife: "2032-12-31",
  supportStatus: "active",
  specifications: {
    cpu: "1.5 GHz",
    memory: "2 MB work + 8 MB load",
    executionTime: "1 ns per instruction",
    displayType: "Built-in display"
  },
  certifications: ["IEC 61131-3", "IEC 61508 SIL3", "ISO 13849 PLe"]
})
  -[:PRODUCT_IN_LINE]-> (line_siemens_s7);

// ----------------------------------------------------------------------------
// LEVEL 1: ORGANIZATIONAL STRUCTURE
// ----------------------------------------------------------------------------

// Sectors
CREATE (sector_water:Sector {
  sectorId: "WATER",
  name: "Water and Wastewater Systems Sector",
  cisaDesignation: "Critical Infrastructure Sector #16",
  regulatoryFramework: ["SDWA", "CWA", "AWIA"],
  nationalPriority: "high",
  assetCount: 153000,
  population: "325 million served"
});

CREATE (sector_healthcare:Sector {
  sectorId: "HEALTHCARE",
  name: "Healthcare and Public Health Sector",
  cisaDesignation: "Critical Infrastructure Sector #8",
  regulatoryFramework: ["HIPAA", "HITECH", "405(d)"],
  nationalPriority: "critical",
  economicImpact: "18% of GDP"
});

CREATE (sector_energy:Sector {
  sectorId: "ENERGY",
  name: "Energy Sector",
  cisaDesignation: "Critical Infrastructure Sector #3",
  regulatoryFramework: ["NERC CIP", "TSA Pipeline Security"],
  nationalPriority: "critical",
  description: "Electricity, oil, natural gas infrastructure"
});

// Organizations
CREATE (org_ladwp:Organization {
  orgId: "LADWP",
  name: "Los Angeles Department of Water and Power",
  type: "municipal_utility",
  established: "1902",
  employees: 10000,
  customers: 4000000,
  regulatoryId: "CA-WATER-001",
  criticalTier: "Tier 1"
})
  -[:WITHIN_SECTOR]-> (sector_water);

CREATE (org_sfwater:Organization {
  orgId: "SFPUC",
  name: "San Francisco Public Utilities Commission",
  type: "municipal_utility",
  established: "1932",
  employees: 2300,
  customers: 2700000,
  regulatoryId: "CA-WATER-002",
  criticalTier: "Tier 1"
})
  -[:WITHIN_SECTOR]-> (sector_water);

CREATE (org_ucsf:Organization {
  orgId: "UCSF",
  name: "University of California San Francisco Medical Center",
  type: "academic_medical_center",
  established: "1864",
  employees: 25000,
  beds: 1545,
  regulatoryId: "CA-HCA-001",
  traumaLevel: "Level 1"
})
  -[:WITHIN_SECTOR]-> (sector_healthcare);

// Business Units
CREATE (bu_water_ops:BusinessUnit {
  unitId: "LADWP-WATER-OPS",
  name: "Water Operations Division",
  budget: "$2.1B",
  facilitiesCount: 47,
  description: "Water treatment, distribution, and infrastructure"
})
  -[:PART_OF_ORGANIZATION]-> (org_ladwp);

CREATE (bu_power_ops:BusinessUnit {
  unitId: "LADWP-POWER-OPS",
  name: "Power System Operations",
  budget: "$3.8B",
  facilitiesCount: 86,
  description: "Electricity generation and distribution"
})
  -[:PART_OF_ORGANIZATION]-> (org_ladwp);

// Facilities
CREATE (fac_law_sylmar:Facility {
  facilityId: "LAW-TP-001",
  name: "LA Water Treatment Plant - Sylmar",
  type: "water_treatment",
  address: "13600 Glenoaks Blvd, Sylmar, CA 91342",
  coordinates: {lat: 34.3194, lon: -118.4358},
  capacity: "600 MGD",
  populationServed: 4000000,
  regulatoryTier: "Tier 1 - Critical",
  scadaEnabled: true,
  securityLevel: "high"
})
  -[:OPERATED_BY]-> (org_ladwp)
  -[:WITHIN_BUSINESS_UNIT]-> (bu_water_ops);

CREATE (fac_law_scada:Facility {
  facilityId: "LAW-SCADA-001",
  name: "LA Water SCADA Control Center",
  type: "control_center",
  address: "111 N Hope St, Los Angeles, CA 90012",
  coordinates: {lat: 34.0556, lon: -118.2500},
  description: "Centralized SCADA monitoring for water system",
  securityLevel: "critical",
  redundancy: "N+1"
})
  -[:OPERATED_BY]-> (org_ladwp)
  -[:WITHIN_BUSINESS_UNIT]-> (bu_water_ops);

CREATE (fac_sf_water:Facility {
  facilityId: "SF-TP-001",
  name: "San Francisco Water Treatment - Sunol Valley",
  type: "water_treatment",
  address: "Sunol Valley, CA",
  capacity: "400 MGD",
  populationServed: 2700000,
  regulatoryTier: "Tier 1 - Critical"
})
  -[:OPERATED_BY]-> (org_sfwater);

CREATE (fac_ucsf_main:Facility {
  facilityId: "UCSF-MAIN-001",
  name: "UCSF Medical Center - Parnassus",
  type: "hospital",
  address: "505 Parnassus Ave, San Francisco, CA 94143",
  beds: 879,
  traumaLevel: "Level 1",
  services: ["Emergency", "Surgery", "Cardiology", "Oncology"]
})
  -[:OPERATED_BY]-> (org_ucsf);

// ----------------------------------------------------------------------------
// LEVEL 2: EQUIPMENT INSTANCES (Customer-Specific Deployments)
// ----------------------------------------------------------------------------

// Equipment Instances - LA Water
CREATE (inst_fw_law_001:EquipmentInstance {
  assetId: "FW-LAW-001",
  hostname: "la-water-fw-primary",
  serialNumber: "JAD214801ABC",
  ipAddress: "10.50.10.1",
  installDate: "2020-03-15",
  warrantyExpires: "2025-03-15",
  status: "operational",
  criticality: "critical",
  maintenanceWindow: "Sunday 02:00-06:00",
  lastAudit: "2025-10-15",
  complianceStatus: "compliant"
})
  -[:INSTANCE_OF]-> (prod_asa_5500)
  -[:INSTALLED_AT]-> (fac_law_sylmar)
  -[:OWNED_BY]-> (org_ladwp)
  -[:MANAGED_BY]-> (bu_water_ops);

CREATE (inst_fw_law_002:EquipmentInstance {
  assetId: "FW-LAW-002",
  hostname: "la-water-fw-secondary",
  serialNumber: "JAD214802DEF",
  ipAddress: "10.50.10.2",
  installDate: "2020-03-15",
  status: "operational",
  criticality: "critical",
  role: "redundant_backup"
})
  -[:INSTANCE_OF]-> (prod_asa_5500)
  -[:INSTALLED_AT]-> (fac_law_sylmar)
  -[:OWNED_BY]-> (org_ladwp)
  -[:REDUNDANT_PAIR]-> (inst_fw_law_001);

CREATE (inst_plc_law_001:EquipmentInstance {
  assetId: "PLC-LAW-001",
  hostname: "la-water-plc-treatment-01",
  serialNumber: "SE-M580-12345",
  ipAddress: "192.168.100.10",
  installDate: "2018-06-20",
  status: "operational",
  criticality: "critical",
  processControlled: ["chemical_dosing", "filtration", "ph_balance"]
})
  -[:INSTANCE_OF]-> (prod_modicon_m580)
  -[:INSTALLED_AT]-> (fac_law_sylmar)
  -[:OWNED_BY]-> (org_ladwp);

CREATE (inst_plc_law_002:EquipmentInstance {
  assetId: "PLC-LAW-002",
  hostname: "la-water-plc-distribution-01",
  serialNumber: "SE-M580-12346",
  ipAddress: "192.168.100.11",
  installDate: "2019-01-10",
  status: "operational",
  criticality: "high",
  processControlled: ["pump_control", "pressure_monitoring", "valve_actuation"]
})
  -[:INSTANCE_OF]-> (prod_modicon_m580)
  -[:INSTALLED_AT]-> (fac_law_sylmar)
  -[:OWNED_BY]-> (org_ladwp);

// Equipment Instances - SF Water
CREATE (inst_fw_sf_003:EquipmentInstance {
  assetId: "FW-SF-003",
  hostname: "sf-water-fw-01",
  serialNumber: "JAD218803GHI",
  ipAddress: "10.60.10.1",
  installDate: "2021-08-20",
  status: "operational",
  criticality: "high"
})
  -[:INSTANCE_OF]-> (prod_asa_5500)
  -[:INSTALLED_AT]-> (fac_sf_water)
  -[:OWNED_BY]-> (org_sfwater);

CREATE (inst_plc_sf_001:EquipmentInstance {
  assetId: "PLC-SF-001",
  hostname: "sf-water-plc-treatment-01",
  serialNumber: "SI-S7-67890",
  ipAddress: "192.168.200.10",
  installDate: "2019-04-15",
  status: "operational",
  criticality: "critical"
})
  -[:INSTANCE_OF]-> (prod_siemens_s7_1500)
  -[:INSTALLED_AT]-> (fac_sf_water)
  -[:OWNED_BY]-> (org_sfwater);

// Equipment Instances - UCSF Healthcare
CREATE (inst_fw_ucsf_001:EquipmentInstance {
  assetId: "FW-UCSF-001",
  hostname: "ucsf-parnassus-fw-01",
  serialNumber: "JAD220804JKL",
  ipAddress: "10.70.10.1",
  installDate: "2022-01-10",
  status: "operational",
  criticality: "critical",
  protectsNetworks: ["EMR", "PACS", "Lab", "Admin"]
})
  -[:INSTANCE_OF]-> (prod_asa_5500)
  -[:INSTALLED_AT]-> (fac_ucsf_main)
  -[:OWNED_BY]-> (org_ucsf);

// ----------------------------------------------------------------------------
// LEVEL 3: SOFTWARE COMPONENTS (SBOM Integration)
// ----------------------------------------------------------------------------

// Software Components
CREATE (sw_asa_os_9_8_4:SoftwareComponent {
  componentId: "sw-cisco-asa-os-9.8.4",
  name: "Cisco ASA Operating System",
  version: "9.8.4.25",
  vendor: "Cisco Systems",
  cpe: "cpe:2.3:o:cisco:adaptive_security_appliance:9.8.4",
  releaseDate: "2019-11-15",
  supportEnds: "2024-12-31",
  licenseType: "proprietary"
});

CREATE (sw_asa_os_9_12_3:SoftwareComponent {
  componentId: "sw-cisco-asa-os-9.12.3",
  name: "Cisco ASA Operating System",
  version: "9.12.3.12",
  vendor: "Cisco Systems",
  cpe: "cpe:2.3:o:cisco:adaptive_security_appliance:9.12.3",
  releaseDate: "2020-08-20",
  supportEnds: "2027-12-31",
  licenseType: "proprietary"
})
  -[:SUPERSEDES]-> (sw_asa_os_9_8_4);

CREATE (sw_openssl:SoftwareComponent {
  componentId: "sw-openssl-1.0.2k",
  name: "OpenSSL",
  version: "1.0.2k",
  vendor: "OpenSSL Project",
  cpe: "cpe:2.3:a:openssl:openssl:1.0.2k",
  releaseDate: "2017-01-26",
  supportEnds: "2019-12-31",
  licenseType: "Apache-style"
});

CREATE (sw_modicon_os:SoftwareComponent {
  componentId: "sw-schneider-modicon-os-2.1",
  name: "Modicon Operating System",
  version: "2.1.0",
  vendor: "Schneider Electric",
  cpe: "cpe:2.3:o:schneider_electric:modicon_m580:2.1.0",
  releaseDate: "2018-03-01",
  supportEnds: "2028-12-31",
  licenseType: "proprietary"
});

CREATE (sw_siemens_tia:SoftwareComponent {
  componentId: "sw-siemens-tia-portal-16",
  name: "TIA Portal",
  version: "16.0",
  vendor: "Siemens",
  cpe: "cpe:2.3:a:siemens:tia_portal:16.0",
  releaseDate: "2019-06-01",
  supportEnds: "2029-12-31",
  licenseType: "proprietary"
});

// Software-Equipment Relationships
CREATE (inst_fw_law_001)-[:HAS_SOFTWARE]->(sw_asa_os_9_8_4);
CREATE (inst_fw_law_002)-[:HAS_SOFTWARE]->(sw_asa_os_9_8_4);
CREATE (inst_fw_sf_003)-[:HAS_SOFTWARE]->(sw_asa_os_9_12_3);
CREATE (inst_fw_ucsf_001)-[:HAS_SOFTWARE]->(sw_asa_os_9_12_3);

CREATE (inst_plc_law_001)-[:HAS_SOFTWARE]->(sw_modicon_os);
CREATE (inst_plc_law_002)-[:HAS_SOFTWARE]->(sw_modicon_os);
CREATE (inst_plc_sf_001)-[:HAS_SOFTWARE]->(sw_siemens_tia);

// Software Dependencies
CREATE (sw_asa_os_9_8_4)-[:DEPENDS_ON]->(sw_openssl);

// SBOM Documents
CREATE (sbom_fw_law_001:SBOM {
  sbomId: "sbom-fw-law-001-v1",
  format: "CycloneDX",
  specVersion: "1.4",
  generated: "2025-10-01",
  tool: "Cisco SBOM Generator",
  componentCount: 47,
  vulnerabilityCount: 3
})
  -[:DESCRIBES_EQUIPMENT]-> (inst_fw_law_001)
  -[:CONTAINS]-> (sw_asa_os_9_8_4)
  -[:CONTAINS]-> (sw_openssl);

CREATE (sbom_plc_law_001:SBOM {
  sbomId: "sbom-plc-law-001-v1",
  format: "SPDX",
  specVersion: "2.3",
  generated: "2025-10-15",
  tool: "Schneider SBOM Tool",
  componentCount: 23,
  vulnerabilityCount: 0
})
  -[:DESCRIBES_EQUIPMENT]-> (inst_plc_law_001)
  -[:CONTAINS]-> (sw_modicon_os);

// ----------------------------------------------------------------------------
// LEVEL 4: VULNERABILITY & THREAT INTELLIGENCE
// ----------------------------------------------------------------------------

// CVEs
CREATE (cve_2024_1234:CVE {
  cveId: "CVE-2024-1234",
  cvss: 9.8,
  cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
  description: "Remote code execution vulnerability in Cisco ASA web services interface",
  published: "2024-01-15",
  lastModified: "2024-02-01",
  exploitAvailable: true,
  exploitPublished: "2024-01-20",
  exploitMaturity: "functional",
  patchAvailable: true,
  patchVersion: "9.8.4.30"
});

CREATE (cve_2022_0778:CVE {
  cveId: "CVE-2022-0778",
  cvss: 7.5,
  cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
  description: "Infinite loop in BN_mod_sqrt() in OpenSSL (DoS)",
  published: "2022-03-15",
  exploitAvailable: true,
  patchAvailable: true
});

// CWEs
CREATE (cwe_78:CWE {
  cweId: "CWE-78",
  name: "OS Command Injection",
  description: "Improper neutralization of special elements in OS commands",
  severity: "high",
  category: "injection"
});

CREATE (cwe_835:CWE {
  cweId: "CWE-835",
  name: "Loop with Unreachable Exit Condition (Infinite Loop)",
  severity: "medium",
  category: "availability"
});

// CVE-Software Relationships
CREATE (cve_2024_1234)-[:AFFECTS_VERSION]->(sw_asa_os_9_8_4);
CREATE (cve_2024_1234)-[:FIXED_IN_VERSION]->(sw_asa_os_9_12_3);
CREATE (cve_2024_1234)-[:EXPLOITS_WEAKNESS]->(cwe_78);

CREATE (cve_2022_0778)-[:AFFECTS_VERSION]->(sw_openssl);
CREATE (cve_2022_0778)-[:EXPLOITS_WEAKNESS]->(cwe_835);

// MITRE ATT&CK Techniques
CREATE (att_t1190:ATTACKTechnique {
  techniqueId: "T1190",
  name: "Exploit Public-Facing Application",
  tactic: "Initial Access",
  description: "Adversaries exploit software vulnerabilities in Internet-facing systems",
  mitigation: ["Network Segmentation", "Application Isolation", "Patch Management"]
});

CREATE (att_t1210:ATTACKTechnique {
  techniqueId: "T1210",
  name: "Exploitation of Remote Services",
  tactic: "Lateral Movement",
  description: "Adversaries exploit remote services to gain access to internal systems"
});

// Threat Actors
CREATE (ta_apt28:ThreatActor {
  actorId: "APT28",
  name: "APT28",
  aliases: ["Fancy Bear", "Sofacy", "Pawn Storm"],
  origin: "Russia",
  motivation: "espionage",
  targetSectors: ["water", "energy", "government", "military"],
  firstSeen: "2007",
  sophistication: "advanced",
  resources: "government"
});

CREATE (ta_sandworm:ThreatActor {
  actorId: "SANDWORM",
  name: "Sandworm Team",
  aliases: ["VOODOO BEAR", "BlackEnergy Group"],
  origin: "Russia",
  motivation: "sabotage",
  targetSectors: ["energy", "water", "industrial"],
  firstSeen: "2009",
  sophistication: "advanced",
  icsCapability: true
});

// Threat Actor Relationships
CREATE (ta_apt28)-[:USES_TECHNIQUE]->(att_t1190);
CREATE (ta_apt28)-[:EXPLOITS_CVE]->(cve_2024_1234);
CREATE (ta_apt28)-[:TARGETS_SECTOR]->(sector_water);
CREATE (ta_apt28)-[:TARGETS_SECTOR]->(sector_energy);

CREATE (ta_sandworm)-[:USES_TECHNIQUE]->(att_t1190);
CREATE (ta_sandworm)-[:USES_TECHNIQUE]->(att_t1210);
CREATE (ta_sandworm)-[:TARGETS_SECTOR]->(sector_water);
CREATE (ta_sandworm)-[:TARGETS_EQUIPMENT_TYPE]->(prod_modicon_m580);

// Historical Incidents
CREATE (hi_2023_0847:HistoricalIncident {
  incidentId: "INC-2023-0847",
  date: "2023-06-15",
  title: "Water Utility Firewall Compromise",
  sector: "water",
  targetedEquipment: "Cisco ASA Firewall",
  attackVector: "CVE exploitation",
  impactLevel: "high",
  downtime: "6 hours",
  affectedOrganizations: ["Municipal Water District"]
})
  -[:TARGETED_EQUIPMENT_TYPE]-> (prod_asa_5500)
  -[:USED_TECHNIQUE]-> (att_t1190)
  -[:ATTRIBUTED_TO]-> (ta_apt28)
  -[:AFFECTED_SECTOR]-> (sector_water);

// ----------------------------------------------------------------------------
// LEVEL 5: PREDICTIVE ANALYTICS (Psychohistory Layer)
// ----------------------------------------------------------------------------

// Attack Patterns
CREATE (ap_water_001:AttackPattern {
  patternId: "AP-WATER-001",
  name: "Water Sector Firewall Exploitation Pattern",
  frequency: "monthly",
  seasonality: "summer_peak",
  confidence: 0.85,
  observedInstances: 34,
  timespan: "2020-2025",
  description: "Pattern of firewall attacks on water utilities during high-demand periods"
})
  -[:TARGETS_EQUIPMENT_TYPE]-> (prod_asa_5500)
  -[:TARGETS_SECTOR]-> (sector_water)
  -[:USES_CVE_CLASS]-> (cwe_78)
  -[:OBSERVED_IN_INCIDENT]-> (hi_2023_0847);

// Predictive Models
CREATE (pm_water_fw:PredictiveModel {
  modelId: "PSYCH-WATER-FIREWALL-v3",
  name: "Water Sector Firewall Threat Prediction Model",
  algorithm: "Temporal Graph Neural Network",
  trained: "2025-10-01",
  accuracy: 0.82,
  precision: 0.78,
  recall: 0.86,
  trainingPeriod: "2020-2025",
  incidentsAnalyzed: 1247,
  featuresUsed: ["equipment_age", "patch_level", "sector", "vulnerability_count", "threat_actor_activity"]
})
  -[:ANALYZES_PATTERN]-> (ap_water_001)
  -[:TRAINED_ON_INCIDENTS]-> (hi_2023_0847);

// Threat Forecasts
CREATE (tf_2025_q1:ThreatForecast {
  forecastId: "FC-2025-Q1-WATER",
  period: "2025-Q1",
  generatedDate: "2025-11-01",
  predictedAttacks: 23,
  confidence: 0.78,
  highestRiskOrgs: ["LADWP", "SFPUC", "Seattle Water"],
  targetEquipment: ["Cisco ASA 5500", "Palo Alto PA-5200"],
  likelyCVEs: ["CVE-2024-1234"],
  recommendedActions: [
    "patch_asa_firmware_to_9.12.3",
    "enhanced_monitoring_deployment",
    "network_segmentation_review",
    "incident_response_drill"
  ]
})
  -[:GENERATED_BY_MODEL]-> (pm_water_fw)
  -[:FORECASTS_RISK_FOR]-> (sector_water)
  -[:IDENTIFIES_HIGH_RISK]-> (org_ladwp)
  -[:IDENTIFIES_HIGH_RISK]-> (org_sfwater)
  -[:IDENTIFIES_VULNERABLE_EQUIPMENT]-> (prod_asa_5500);

// ----------------------------------------------------------------------------
// LEVEL 6: DEFENSIVE POSTURE & CONTROLS
// ----------------------------------------------------------------------------

// Security Controls
CREATE (sc_boundary:SecurityControl {
  controlId: "SC-7",
  framework: "NIST 800-53",
  name: "Boundary Protection",
  controlFamily: "System and Communications Protection",
  priority: "P1",
  description: "Monitor and control communications at external boundaries"
})
  -[:IMPLEMENTED_BY_EQUIPMENT_TYPE]-> (prod_asa_5500);

CREATE (sc_audit:SecurityControl {
  controlId: "AU-2",
  framework: "NIST 800-53",
  name: "Audit Events",
  controlFamily: "Audit and Accountability",
  priority: "P1",
  description: "Identify events to be audited and maintain audit records"
});

// Equipment Configurations
CREATE (config_fw_law_001:Configuration {
  configId: "cfg-fw-law-001",
  version: "v2.3",
  lastUpdate: "2025-09-15",
  approvedBy: "Security Team",
  approver: "John Smith",
  complianceStatus: "compliant",
  frameworks: ["NIST 800-53", "NERC CIP"],
  reviewCycle: "quarterly"
})
  -[:APPLIES_TO]-> (inst_fw_law_001)
  -[:IMPLEMENTS_CONTROL]-> (sc_boundary)
  -[:IMPLEMENTS_CONTROL]-> (sc_audit);

// Firewall Rules (sample)
CREATE (rule_001:FirewallRule {
  ruleId: "rule-001",
  priority: 1,
  action: "deny",
  source: "any",
  destination: "SCADA_VLAN",
  port: "any",
  protocol: "any",
  log: true,
  description: "Deny all traffic to SCADA VLAN by default"
})
  -[:PART_OF_CONFIG]-> (config_fw_law_001);

CREATE (rule_002:FirewallRule {
  ruleId: "rule-002",
  priority: 10,
  action: "allow",
  source: "ADMIN_VLAN",
  destination: "SCADA_VLAN",
  port: "502",
  protocol: "tcp",
  log: true,
  description: "Allow Modbus TCP from admin network"
})
  -[:PART_OF_CONFIG]-> (config_fw_law_001);

// Defensive Capabilities
CREATE (dc_ladwp:DefensiveCapability {
  capabilityId: "DC-LADWP-001",
  organization: "LADWP",
  maturityLevel: "Level 3 - Defined",
  framework: "CMMC",
  lastAssessment: "2025-08-01",
  nextAssessment: "2026-08-01",
  strengths: ["network_security", "continuous_monitoring", "incident_response"],
  gaps: ["endpoint_detection", "threat_hunting", "deception_technology"],
  budget: "$12M",
  staffing: 45
})
  -[:DEFENSIVE_POSTURE_OF]-> (org_ladwp);

// Resilience Profiles
CREATE (rp_water:ResilienceProfile {
  profileId: "RP-WATER-001",
  sector: "water",
  recoveryTimeObjective: "4 hours",
  recoveryPointObjective: "1 hour",
  redundancyLevel: "N+1",
  backupFrequency: "hourly",
  disasterRecoveryPlan: true,
  lastTested: "2025-09-01",
  successfulFailover: true
})
  -[:RESILIENCE_FOR_SECTOR]-> (sector_water);

// ============================================================================
// INDEXES AND CONSTRAINTS
// ============================================================================

// Uniqueness Constraints
CREATE CONSTRAINT equipment_product_unique IF NOT EXISTS
  FOR (ep:EquipmentProduct)
  REQUIRE ep.productId IS UNIQUE;

CREATE CONSTRAINT equipment_instance_unique IF NOT EXISTS
  FOR (ei:EquipmentInstance)
  REQUIRE ei.assetId IS UNIQUE;

CREATE CONSTRAINT sbom_unique IF NOT EXISTS
  FOR (s:SBOM)
  REQUIRE s.sbomId IS UNIQUE;

CREATE CONSTRAINT cve_unique IF NOT EXISTS
  FOR (c:CVE)
  REQUIRE c.cveId IS UNIQUE;

CREATE CONSTRAINT sector_unique IF NOT EXISTS
  FOR (s:Sector)
  REQUIRE s.sectorId IS UNIQUE;

CREATE CONSTRAINT organization_unique IF NOT EXISTS
  FOR (o:Organization)
  REQUIRE o.orgId IS UNIQUE;

CREATE CONSTRAINT facility_unique IF NOT EXISTS
  FOR (f:Facility)
  REQUIRE f.facilityId IS UNIQUE;

// Performance Indexes
CREATE INDEX equipment_product_model IF NOT EXISTS
  FOR (ep:EquipmentProduct) ON (ep.model);

CREATE INDEX equipment_instance_hostname IF NOT EXISTS
  FOR (ei:EquipmentInstance) ON (ei.hostname);

CREATE INDEX equipment_instance_criticality IF NOT EXISTS
  FOR (ei:EquipmentInstance) ON (ei.criticality);

CREATE INDEX software_component_name_version IF NOT EXISTS
  FOR (sw:SoftwareComponent) ON (sw.name, sw.version);

CREATE INDEX cve_cvss IF NOT EXISTS
  FOR (c:CVE) ON (c.cvss);

CREATE INDEX organization_name IF NOT EXISTS
  FOR (o:Organization) ON (o.name);

CREATE INDEX sector_name IF NOT EXISTS
  FOR (s:Sector) ON (s.name);

// Full-text Search Indexes
CREATE FULLTEXT INDEX equipment_product_search IF NOT EXISTS
  FOR (ep:EquipmentProduct)
  ON EACH [ep.manufacturer, ep.model, ep.category];

CREATE FULLTEXT INDEX cve_description_search IF NOT EXISTS
  FOR (c:CVE)
  ON EACH [c.description];
```

---

## Migration Plan from Current Structure

### Phase 1: Assessment & Preparation (Week 1-2)

**Tasks**:
1. **Inventory Current Equipment Nodes**: Identify all equipment-related nodes and their properties
2. **Analyze Duplication**: Find duplicate equipment across sectors
3. **Map Current Relationships**: Document existing relationship patterns
4. **Identify Data Quality Issues**: Missing properties, inconsistent naming, orphaned nodes

**Cypher Queries**:
```cypher
// Find potential duplicate equipment
MATCH (e:Equipment)
WITH e.manufacturer + " " + e.model as equipmentName,
     COLLECT(e) as nodes,
     COUNT(e) as count
WHERE count > 1
RETURN equipmentName, count, nodes
ORDER BY count DESC;

// Identify equipment with sector properties (needs refactoring)
MATCH (e:Equipment)
WHERE e.sector IS NOT NULL
RETURN e.manufacturer, e.model, e.sector
LIMIT 100;

// Find orphaned equipment (not connected to organizations/facilities)
MATCH (e:Equipment)
WHERE NOT EXISTS {
  (e)-[]->(:Organization|:Facility)
}
RETURN COUNT(e) as orphanedCount;
```

### Phase 2: Create New Taxonomy Structure (Week 3-4)

**Tasks**:
1. **Build Equipment Taxonomy**: Create Categories → Subcategories → Product Lines
2. **Create Canonical Products**: Deduplicate equipment into single EquipmentProduct nodes
3. **Establish Constraints**: Add uniqueness constraints and indexes

**Migration Script**:
```cypher
// Step 1: Create canonical EquipmentProduct from existing Equipment nodes
MATCH (old:Equipment)
WITH old.manufacturer as manufacturer,
     old.model as model,
     old.category as category,
     COLLECT(old) as oldNodes
MERGE (ep:EquipmentProduct {
  productId: toLower(manufacturer + "-" + replace(model, " ", "-"))
})
  SET ep.manufacturer = manufacturer,
      ep.model = model,
      ep.category = category,
      ep.migrated = true,
      ep.oldNodeCount = SIZE(oldNodes)
RETURN ep.productId, ep.manufacturer, ep.model, ep.oldNodeCount;

// Step 2: Verify no duplicates in new structure
MATCH (ep:EquipmentProduct)
WITH ep.manufacturer + " " + ep.model as equipName,
     COLLECT(ep) as products,
     COUNT(ep) as count
WHERE count > 1
RETURN equipName, count, [p IN products | p.productId];
```

### Phase 3: Transform Equipment to Instances (Week 5-6)

**Tasks**:
1. **Create Equipment Instances**: Convert sector/customer-specific equipment to instances
2. **Link Instances to Products**: Establish [:INSTANCE_OF] relationships
3. **Migrate Properties**: Move instance-specific properties (assetId, hostname, IP address)
4. **Preserve Existing Relationships**: Maintain connections to Organizations, Facilities

**Migration Script**:
```cypher
// Transform existing Equipment nodes into Instances
MATCH (old:Equipment)
MATCH (ep:EquipmentProduct {
  manufacturer: old.manufacturer,
  model: old.model
})
CREATE (ei:EquipmentInstance {
  assetId: COALESCE(old.assetId, "MIGRATED-" + id(old)),
  hostname: old.hostname,
  ipAddress: old.ipAddress,
  installDate: old.installDate,
  status: COALESCE(old.status, "unknown"),
  criticality: COALESCE(old.criticality, "medium"),
  migratedFrom: id(old)
})
  -[:INSTANCE_OF]-> (ep)

// Migrate existing relationships
WITH old, ei
OPTIONAL MATCH (old)-[r:OWNED_BY]->(o:Organization)
FOREACH (_ IN CASE WHEN o IS NOT NULL THEN [1] ELSE [] END |
  CREATE (ei)-[:OWNED_BY]->(o)
)

WITH old, ei
OPTIONAL MATCH (old)-[r:INSTALLED_AT]->(f:Facility)
FOREACH (_ IN CASE WHEN f IS NOT NULL THEN [1] ELSE [] END |
  CREATE (ei)-[:INSTALLED_AT]->(f)
)

RETURN COUNT(ei) as instancesCreated;
```

### Phase 4: Migrate SBOM & Software Components (Week 7-8)

**Tasks**:
1. **Extract Software Information**: Create SoftwareComponent nodes from existing data
2. **Link Software to Instances**: Establish [:HAS_SOFTWARE] relationships
3. **Create SBOM Documents**: Generate SBOM nodes where data exists
4. **Link CVEs to Software**: Connect vulnerabilities to specific software versions

**Migration Script**:
```cypher
// Create SoftwareComponent nodes from existing data
MATCH (ei:EquipmentInstance)
WHERE ei.softwareVersion IS NOT NULL
MERGE (sw:SoftwareComponent {
  name: ei.softwareName,
  version: ei.softwareVersion,
  vendor: ei.manufacturer
})
  ON CREATE SET
    sw.componentId = toLower(ei.softwareName + "-" + ei.softwareVersion),
    sw.migrated = true

CREATE (ei)-[:HAS_SOFTWARE]->(sw)

RETURN COUNT(sw) as softwareComponentsCreated;

// Link existing CVEs to SoftwareComponents
MATCH (cve:CVE)
MATCH (sw:SoftwareComponent)
WHERE cve.affectedProduct = sw.name
  AND cve.affectedVersion = sw.version
CREATE (cve)-[:AFFECTS_VERSION]->(sw)
RETURN COUNT(*) as cveLinksCreated;
```

### Phase 5: Cleanup & Validation (Week 9-10)

**Tasks**:
1. **Validate New Structure**: Run comprehensive validation queries
2. **Performance Testing**: Test query performance on new structure
3. **Data Quality Checks**: Verify all data migrated correctly
4. **Remove Old Nodes**: Archive or delete old Equipment nodes after validation

**Validation Queries**:
```cypher
// Validation Query 1: All instances have products
MATCH (ei:EquipmentInstance)
WHERE NOT EXISTS {
  (ei)-[:INSTANCE_OF]->(:EquipmentProduct)
}
RETURN COUNT(ei) as instancesWithoutProducts;
// Expected: 0

// Validation Query 2: All instances have owners
MATCH (ei:EquipmentInstance)
WHERE NOT EXISTS {
  (ei)-[:OWNED_BY]->(:Organization)
}
RETURN COUNT(ei) as instancesWithoutOwners;
// Expected: 0

// Validation Query 3: No duplicate products
MATCH (ep:EquipmentProduct)
WITH ep.manufacturer + " " + ep.model as equipName,
     COLLECT(ep) as products,
     COUNT(ep) as count
WHERE count > 1
RETURN equipName, count;
// Expected: No results

// Validation Query 4: Compare counts before/after
MATCH (old:Equipment {migrated: true})
WITH COUNT(old) as oldCount
MATCH (ei:EquipmentInstance)
WITH oldCount, COUNT(ei) as newCount
RETURN oldCount, newCount,
       CASE WHEN oldCount = newCount THEN "PASS" ELSE "FAIL" END as status;
```

**Cleanup Script**:
```cypher
// Mark old Equipment nodes as archived
MATCH (old:Equipment)
WHERE EXISTS {
  (ei:EquipmentInstance {migratedFrom: id(old)})
}
SET old:Archived, old.archivedDate = datetime()
RETURN COUNT(old) as archivedNodes;

// After validation period, optionally delete archived nodes
// MATCH (old:Equipment:Archived)
// WHERE old.archivedDate < datetime() - duration('P30D')
// DETACH DELETE old
// RETURN COUNT(old) as deletedNodes;
```

---

## Performance Optimization Strategies

### Indexing Strategy

```cypher
// Critical path indexes for common queries

// 1. Equipment lookup by product
CREATE INDEX equipment_product_lookup IF NOT EXISTS
  FOR (ep:EquipmentProduct) ON (ep.manufacturer, ep.model);

// 2. Instance lookup by asset ID
CREATE INDEX instance_asset_id IF NOT EXISTS
  FOR (ei:EquipmentInstance) ON (ei.assetId);

// 3. Sector-based aggregation
CREATE INDEX organization_sector IF NOT EXISTS
  FOR (o:Organization) ON (o.sector);

// 4. Vulnerability severity filtering
CREATE INDEX cve_severity IF NOT EXISTS
  FOR (c:CVE) ON (c.cvss);

// 5. Software component lookup
CREATE INDEX software_cpe IF NOT EXISTS
  FOR (sw:SoftwareComponent) ON (sw.cpe);
```

### Query Optimization Patterns

```cypher
// Pattern 1: Use MERGE instead of CREATE for canonical entities
MERGE (ep:EquipmentProduct {productId: "cisco-asa-5500"})
  ON CREATE SET ep.manufacturer = "Cisco Systems", ep.model = "ASA 5500"
  ON MATCH SET ep.lastQueried = datetime()

// Pattern 2: Use WITH clause to filter early
MATCH (s:Sector {name: "Water"})
WITH s
MATCH (s)<-[:WITHIN_SECTOR]-(o:Organization)
WITH o
MATCH (o)<-[:OWNED_BY]-(ei:EquipmentInstance)
WHERE ei.criticality = "critical"
RETURN ei

// Pattern 3: Use EXISTS for relationship checks (faster than OPTIONAL MATCH)
MATCH (ei:EquipmentInstance)
WHERE EXISTS {
  (ei)-[:HAS_SOFTWARE]->(:SoftwareComponent)-[:HAS_VULNERABILITY]->(:CVE {cvss: ">= 7.0"})
}
RETURN ei

// Pattern 4: Use aggregation to reduce result set size
MATCH (ei:EquipmentInstance)-[:INSTANCE_OF]->(ep:EquipmentProduct)
WITH ep, COUNT(ei) as instances
WHERE instances > 10
RETURN ep.manufacturer, ep.model, instances
```

### Caching Strategy

```yaml
caching_layers:
  level_1_hot_data:
    - Frequently accessed EquipmentProduct nodes
    - Active EquipmentInstances (status = "operational")
    - High-severity CVEs (cvss >= 7.0)
    - Critical organizations and facilities

  level_2_warm_data:
    - Historical incidents (last 2 years)
    - Sector taxonomies
    - Threat actor profiles

  level_3_cold_data:
    - Archived equipment instances
    - Old software versions (unsupported)
    - Historical incidents (>2 years old)

query_result_caching:
  sector_equipment_aggregations: 1 hour
  customer_inventory_snapshots: 15 minutes
  cve_impact_analysis: 30 minutes
  threat_forecasts: 24 hours
```

---

## Validation & Quality Assurance

### Data Quality Rules

```cypher
// Rule 1: Every EquipmentInstance must have an EquipmentProduct
MATCH (ei:EquipmentInstance)
WHERE NOT EXISTS {
  (ei)-[:INSTANCE_OF]->(:EquipmentProduct)
}
RETURN ei.assetId as orphanedInstance
// Expected: 0 results

// Rule 2: Every EquipmentInstance must have an Organization owner
MATCH (ei:EquipmentInstance)
WHERE NOT EXISTS {
  (ei)-[:OWNED_BY]->(:Organization)
}
RETURN ei.assetId as unownedInstance
// Expected: 0 results

// Rule 3: AssetIds must be unique
MATCH (ei:EquipmentInstance)
WITH ei.assetId as assetId, COLLECT(ei) as instances, COUNT(ei) as count
WHERE count > 1
RETURN assetId, count
// Expected: 0 results

// Rule 4: Critical equipment must have facility location
MATCH (ei:EquipmentInstance {criticality: "critical"})
WHERE NOT EXISTS {
  (ei)-[:INSTALLED_AT]->(:Facility)
}
RETURN ei.assetId as criticalWithoutLocation
// Expected: 0 results

// Rule 5: ProductIds must follow naming convention
MATCH (ep:EquipmentProduct)
WHERE NOT ep.productId =~ "^[a-z0-9]+-[a-z0-9-]+$"
RETURN ep.productId as invalidProductId
// Expected: 0 results

// Rule 6: Software components must have CPE identifiers
MATCH (sw:SoftwareComponent)
WHERE sw.cpe IS NULL OR sw.cpe = ""
RETURN sw.name, sw.version as missingCPE
// Alert if count > 10%

// Rule 7: CVEs must have CVSS scores
MATCH (c:CVE)
WHERE c.cvss IS NULL
RETURN c.cveId as missingCVSS
// Expected: 0 results
```

### Relationship Integrity Checks

```cypher
// Check 1: Bidirectional consistency (if A->B exists, B<-A should exist)
MATCH (ei:EquipmentInstance)-[:INSTANCE_OF]->(ep:EquipmentProduct)
WHERE NOT EXISTS {
  (ep)<-[:INSTANCE_OF]-(ei)
}
RETURN ei.assetId, ep.productId as inconsistentRelationship
// Expected: 0 results

// Check 2: Circular dependencies
MATCH path = (sw1:SoftwareComponent)-[:DEPENDS_ON*]->(sw1)
RETURN path
// Expected: 0 results (no circular dependencies)

// Check 3: Orphaned nodes (no incoming or outgoing relationships)
MATCH (n)
WHERE NOT EXISTS {(n)-[]-()}
RETURN LABELS(n) as nodeType, COUNT(n) as orphanedCount
// Expected: 0 for critical node types

// Check 4: Validate multi-hop paths work
MATCH path = (cve:CVE)-[:AFFECTS_VERSION]->(:SoftwareComponent)
             -[:INSTALLED_ON]->(:EquipmentInstance)
             -[:OWNED_BY]->(:Organization)
             -[:WITHIN_SECTOR]->(:Sector)
WITH COUNT(path) as pathCount
RETURN CASE
  WHEN pathCount > 0 THEN "PASS"
  ELSE "FAIL - No complete CVE->Sector paths found"
END as pathValidation
```

---

## McKenney's 8 Critical Questions - Implementation

### Question 1: What happened? (Historical Analysis)

```cypher
// Query: Comprehensive incident analysis with equipment context
MATCH (hi:HistoricalIncident)
      -[:TARGETED_EQUIPMENT_TYPE]->(ep:EquipmentProduct)
      <-[:INSTANCE_OF]-(ei:EquipmentInstance)
      -[:OWNED_BY]->(o:Organization)
      -[:WITHIN_SECTOR]->(s:Sector)
OPTIONAL MATCH (hi)-[:USED_TECHNIQUE]->(att:ATTACKTechnique)
OPTIONAL MATCH (hi)-[:EXPLOITED_CVE]->(cve:CVE)
OPTIONAL MATCH (hi)-[:ATTRIBUTED_TO]->(ta:ThreatActor)
RETURN hi.date as IncidentDate,
       hi.title as Incident,
       s.name as Sector,
       o.name as Organization,
       ep.manufacturer + " " + ep.model as TargetedEquipment,
       COUNT(DISTINCT ei) as AffectedInstances,
       COLLECT(DISTINCT att.name) as Techniques,
       COLLECT(DISTINCT cve.cveId) as ExploitedCVEs,
       COLLECT(DISTINCT ta.name) as AttributedActors,
       hi.impactLevel as Impact
ORDER BY hi.date DESC
```

### Question 2: Who did it? (Attribution)

```cypher
// Query: Threat actor targeting patterns by equipment type
MATCH (ta:ThreatActor)
      -[:TARGETS_EQUIPMENT_TYPE]->(ep:EquipmentProduct)
      <-[:INSTANCE_OF]-(ei:EquipmentInstance)
      -[:OWNED_BY]->(o:Organization)
      -[:WITHIN_SECTOR]->(s:Sector)
OPTIONAL MATCH (ta)-[:USES_TECHNIQUE]->(att:ATTACKTechnique)
WITH ta, ep, s,
     COUNT(DISTINCT ei) as potentialTargets,
     COLLECT(DISTINCT att.name) as techniques
RETURN ta.name as ThreatActor,
       ta.origin as Origin,
       ta.motivation as Motivation,
       ep.category as TargetEquipmentType,
       ep.manufacturer + " " + ep.model as SpecificModels,
       s.name as TargetSector,
       potentialTargets as PotentialTargets,
       techniques as KnownTechniques
ORDER BY potentialTargets DESC
```

### Question 3: How did they do it? (TTPs & CVEs)

```cypher
// Query: Attack chain from CVE to equipment compromise
MATCH path = (ta:ThreatActor)
      -[:EXPLOITS_CVE]->(cve:CVE)
      -[:AFFECTS_VERSION]->(sw:SoftwareComponent)
      -[:INSTALLED_ON]->(ei:EquipmentInstance)
      -[:OWNED_BY]->(o:Organization)
OPTIONAL MATCH (ta)-[:USES_TECHNIQUE]->(att:ATTACKTechnique)
OPTIONAL MATCH (cve)-[:EXPLOITS_WEAKNESS]->(cwe:CWE)
RETURN ta.name as ThreatActor,
       cve.cveId as CVE,
       cve.cvss as Severity,
       cve.description as Vulnerability,
       cwe.name as Weakness,
       att.name as Technique,
       sw.name + " " + sw.version as VulnerableSoftware,
       COUNT(DISTINCT ei) as AffectedAssets,
       COLLECT(DISTINCT o.name)[..5] as AffectedOrganizations
ORDER BY cve.cvss DESC, COUNT(DISTINCT ei) DESC
```

### Question 4: What assets are at risk? (Risk Assessment)

```cypher
// Query: At-risk equipment based on vulnerabilities and threat actor interest
MATCH (ei:EquipmentInstance)
      -[:INSTANCE_OF]->(ep:EquipmentProduct)
      <-[:TARGETS_EQUIPMENT_TYPE]-(ta:ThreatActor)
MATCH (ei)-[:HAS_SOFTWARE]->(sw:SoftwareComponent)
            -[:HAS_VULNERABILITY]->(cve:CVE)
MATCH (ei)-[:OWNED_BY]->(o:Organization)
            -[:WITHIN_SECTOR]->(s:Sector)
WITH ei, ep, o, s,
     COUNT(DISTINCT cve) as vulnCount,
     MAX(cve.cvss) as maxSeverity,
     AVG(cve.cvss) as avgSeverity,
     COUNT(DISTINCT ta) as threateningActors,
     COLLECT(DISTINCT ta.name)[..3] as actors
WHERE vulnCount > 0
WITH ei, ep, o, s, vulnCount, maxSeverity, avgSeverity, threateningActors, actors,
     (vulnCount * maxSeverity * threateningActors / 10.0) as riskScore
RETURN ei.assetId as AssetID,
       ei.hostname as Hostname,
       o.name as Organization,
       s.name as Sector,
       ep.manufacturer + " " + ep.model as Equipment,
       ei.criticality as BusinessCriticality,
       vulnCount as Vulnerabilities,
       maxSeverity as HighestCVSS,
       avgSeverity as AvgCVSS,
       threateningActors as ThreatActorInterest,
       actors as ThreateningActors,
       riskScore as CalculatedRiskScore
ORDER BY riskScore DESC
LIMIT 50
```

### Question 5: What's the business impact? (Impact Analysis)

```cypher
// Query: Business impact assessment from equipment failure
MATCH (ei:EquipmentInstance {criticality: "critical"})
      -[:INSTALLED_AT]->(f:Facility)
      -[:OPERATED_BY]->(o:Organization)
      -[:WITHIN_SECTOR]->(s:Sector)
OPTIONAL MATCH (ei)-[:HAS_SOFTWARE]->(sw:SoftwareComponent)
                   -[:HAS_VULNERABILITY]->(cve:CVE {exploitAvailable: true})
WITH ei, f, o, s,
     COUNT(DISTINCT cve) as exploitableCVEs,
     f.populationServed as population,
     f.capacity as capacity
RETURN o.name as Organization,
       s.name as Sector,
       f.name as Facility,
       f.type as FacilityType,
       ei.assetId as CriticalAsset,
       ei.hostname as Hostname,
       population as PopulationServed,
       capacity as Capacity,
       exploitableCVEs as ExploitableVulnerabilities,
       CASE s.name
         WHEN "Water and Wastewater Systems Sector"
           THEN "Loss of clean water supply, potential public health emergency"
         WHEN "Healthcare and Public Health Sector"
           THEN "Patient care disruption, potential life safety impact"
         WHEN "Energy Sector"
           THEN "Power outages, cascading infrastructure failures"
         ELSE "Sector-specific operational disruption"
       END as PotentialImpact
ORDER BY exploitableCVEs DESC, population DESC
```

### Question 6: What patterns exist? (Pattern Analysis)

```cypher
// Query: Attack pattern identification across sectors and equipment
MATCH (hi:HistoricalIncident)
      -[:TARGETED_EQUIPMENT_TYPE]->(ep:EquipmentProduct)
MATCH (hi)-[:AFFECTED_SECTOR]->(s:Sector)
OPTIONAL MATCH (hi)-[:USED_TECHNIQUE]->(att:ATTACKTechnique)
OPTIONAL MATCH (hi)-[:ATTRIBUTED_TO]->(ta:ThreatActor)
WITH s, ep, att, ta,
     COUNT(DISTINCT hi) as incidentCount,
     MIN(hi.date) as firstSeen,
     MAX(hi.date) as lastSeen,
     AVG(duration.between(date(hi.date), date()).days) as avgDaysSince
WHERE incidentCount >= 3  // Pattern threshold
RETURN s.name as Sector,
       ep.category as EquipmentType,
       ep.manufacturer + " " + ep.model as SpecificEquipment,
       incidentCount as Incidents,
       firstSeen as FirstIncident,
       lastSeen as MostRecentIncident,
       avgDaysSince as AvgDaysBetweenIncidents,
       COLLECT(DISTINCT att.name) as CommonTechniques,
       COLLECT(DISTINCT ta.name) as FrequentActors,
       CASE
         WHEN avgDaysSince < 90 THEN "HIGH FREQUENCY"
         WHEN avgDaysSince < 180 THEN "MODERATE FREQUENCY"
         ELSE "LOW FREQUENCY"
       END as PatternFrequency
ORDER BY incidentCount DESC, lastSeen DESC
```

### Question 7: What will happen next? (Predictive Analysis)

```cypher
// Query: Predictive threat forecast using psychohistory model
MATCH (pm:PredictiveModel {modelId: "PSYCH-WATER-FIREWALL-v3"})
      -[:ANALYZES_PATTERN]->(ap:AttackPattern)
      -[:TARGETS_EQUIPMENT_TYPE]->(ep:EquipmentProduct)
      <-[:INSTANCE_OF]-(ei:EquipmentInstance)
      -[:OWNED_BY]->(o:Organization)
      -[:WITHIN_SECTOR]->(s:Sector)
MATCH (pm)-[:GENERATES_FORECAST]->(tf:ThreatForecast)
OPTIONAL MATCH (ei)-[:HAS_SOFTWARE]->(sw:SoftwareComponent)
                   -[:HAS_VULNERABILITY]->(cve:CVE)
WITH o, s, ei, ep, ap, tf, pm,
     COUNT(DISTINCT cve) as currentVulnerabilities,
     MAX(cve.cvss) as maxSeverity
WHERE o.name IN tf.highestRiskOrgs
RETURN tf.period as ForecastPeriod,
       tf.predictedAttacks as PredictedAttacks,
       tf.confidence as ModelConfidence,
       pm.accuracy as ModelAccuracy,
       o.name as HighRiskOrganization,
       s.name as Sector,
       COUNT(DISTINCT ei) as VulnerableAssets,
       ep.manufacturer + " " + ep.model as TargetEquipment,
       currentVulnerabilities as CurrentVulnerabilities,
       maxSeverity as HighestCVSS,
       ap.confidence as PatternConfidence,
       tf.likelyCVEs as LikelyExploitedCVEs,
       tf.recommendedActions as RecommendedActions
ORDER BY tf.confidence DESC, currentVulnerabilities DESC
```

### Question 8: How do we prevent it? (Mitigation & Controls)

```cypher
// Query: Gap analysis between current controls and recommended mitigations
MATCH (ei:EquipmentInstance)
      -[:HAS_SOFTWARE]->(sw:SoftwareComponent)
      -[:HAS_VULNERABILITY]->(cve:CVE {cvss: ">= 7.0"})
MATCH (ei)-[:OWNED_BY]->(o:Organization)
            -[:WITHIN_SECTOR]->(s:Sector)
OPTIONAL MATCH (ei)<-[:APPLIES_TO]-(config:Configuration)
                   -[:IMPLEMENTS_CONTROL]->(sc:SecurityControl)
OPTIONAL MATCH (cve)-[:MITIGATED_BY]->(recommended_sc:SecurityControl)
WITH ei, o, s, cve,
     COLLECT(DISTINCT sc.controlId) as currentControls,
     COLLECT(DISTINCT recommended_sc.controlId) as recommendedControls
WITH ei, o, s,
     COUNT(DISTINCT cve) as highSeverityCVEs,
     currentControls,
     recommendedControls,
     [x IN recommendedControls WHERE NOT x IN currentControls] as missingControls
WHERE SIZE(missingControls) > 0
RETURN o.name as Organization,
       s.name as Sector,
       ei.assetId as Asset,
       highSeverityCVEs as HighSeverityVulnerabilities,
       currentControls as CurrentControls,
       recommendedControls as RecommendedControls,
       missingControls as ControlGaps,
       SIZE(missingControls) as GapCount
ORDER BY highSeverityCVEs DESC, GapCount DESC
```

---

## Summary & Benefits

### Key Innovations

1. **Zero Duplication Architecture**: Single canonical EquipmentProduct per model, infinite instances across sectors
2. **Multi-Level Abstraction**: Taxonomy → Product → Instance → Software → Vulnerability chain
3. **20-Hop Capability**: Deep relationship traversal for psychohistory modeling
4. **Dual Analysis Support**: Both reference architecture queries AND customer-specific impact assessment
5. **Sector Agnostic**: Equipment associations through relationships, not properties
6. **SBOM Integration**: Complete software supply chain visibility
7. **Predictive Analytics**: Native support for threat forecasting and pattern recognition

### Scalability Characteristics

```yaml
current_scale:
  sectors: 16
  organizations: 100+
  facilities: 500+
  equipment_products: 500
  equipment_instances: 10,000+
  software_components: 5,000+
  cves: 50,000+

projected_scale:
  sectors: 16
  organizations: 1,000
  facilities: 10,000
  equipment_products: 5,000
  equipment_instances: 1,000,000
  software_components: 100,000
  cves: 200,000+

performance_targets:
  sector_equipment_query: < 500ms
  customer_inventory_query: < 200ms
  cve_impact_analysis: < 1000ms
  20_hop_traversal: < 2000ms
  predictive_forecast: < 3000ms
```

### Benefits Realization

1. **Eliminates Equipment Duplication**: 16x reduction in duplicate nodes
2. **Enables Cross-Sector Analysis**: Identify common equipment vulnerabilities across sectors
3. **Supports Customer-Specific Intelligence**: "Which of MY assets are affected by CVE-X?"
4. **Enables Psychohistory Modeling**: Deep pattern analysis for predictive capabilities
5. **Facilitates Regulatory Compliance**: Track equipment, software, vulnerabilities by organization
6. **Improves Query Performance**: Indexed structure optimized for common query patterns
7. **Provides Migration Path**: Clear upgrade path from existing structure

---

**Document Status**: ARCHITECTURE SPECIFICATION COMPLETE
**Implementation Readiness**: READY FOR REVIEW AND PHASED DEPLOYMENT
**Estimated Implementation Time**: 10 weeks (2 weeks per phase)
**Risk Level**: MEDIUM (requires careful migration planning and validation)

---

*This ontology design represents a comprehensive solution to the multi-level equipment challenge, enabling both reference architecture analysis and customer-specific threat intelligence while maintaining scalability and performance characteristics required for McKenney's psychohistory vision.*
