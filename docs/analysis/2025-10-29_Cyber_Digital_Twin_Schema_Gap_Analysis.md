# Cyber Digital Twin Neo4j Schema - Gap Analysis

**File:** 2025-10-29_Cyber_Digital_Twin_Schema_Gap_Analysis.md
**Created:** 2025-10-29 02:15:00 UTC
**Version:** v1.0.0
**Author:** Code Analyzer Agent
**Purpose:** Comprehensive gap analysis between CURRENT Neo4j database state and REQUIRED Cyber Digital Twin capabilities
**Status:** ACTIVE

---

## Executive Summary

**Current Database State:**
- 267,487 CVE nodes (imported)
- 2,214 CWE nodes (imported)
- 615 CAPEC nodes (imported)
- 834 ATT&CK Technique nodes (imported)
- CVE→CWE, CVE→CAPEC relationships (basic threat intelligence)
- **NO asset hierarchy** (Organization→Train→BrakeController→Software)
- **NO network topology** (IP addresses, security zones, conduits)
- **NO reachability modeling** (attack path analysis impossible)
- **NO CPE nodes** (cannot link CVEs to real assets)

**Schema Status:**
- ✅ **Defined**: 8-layer comprehensive schema with 24+ node types
- ⚠️ **Deployed**: Only Layer 4 (Vulnerability/Threat) partially implemented
- ❌ **Missing**: Layers 1-3, 5-8 completely absent from database

**Critical Gap:** Only **16.7%** of required schema is implemented. Cannot perform:
- Asset-to-vulnerability correlation
- Attack path analysis
- Now/Next/Never prioritization
- Customer-specific risk assessment
- Network reachability analysis

---

## 1. Missing Node Types Analysis

### 1.1 Layer 1: Physical Asset Layer (100% Missing)

| Node Type | Status | Current Count | Required Properties | Impact |
|-----------|--------|---------------|-------------------|--------|
| `PhysicalAsset` | ❌ MISSING | 0 | id, name, type, customer_namespace, location, operational_status | **CRITICAL** - No asset hierarchy possible |
| `Device` | ❌ MISSING | 0 | id, name, manufacturer, model, serialNumber, cpe, firmwareVersion, criticalityLevel, deviceType | **CRITICAL** - Cannot link CVEs to real hardware |
| `HardwareComponent` | ❌ MISSING | 0 | id, name, componentType, manufacturer, partNumber, cpe, firmwareVersion, interface_type | **HIGH** - No component-level vulnerability tracking |
| `Location` | ❌ MISSING | 0 | id, name, locationType, coordinates, address, parent_location | **MEDIUM** - No geographic/physical context |

**Capability Gap:**
- ❌ Cannot model train fleet → consist → car → brake controller hierarchy
- ❌ Cannot identify which physical assets are affected by CVEs
- ❌ Cannot calculate fleet-wide vulnerability exposure
- ❌ No criticality-based asset prioritization

**Required Before:**
- Attack surface analysis
- Asset-based risk scoring
- Fleet-wide impact assessment
- Customer-specific vulnerability correlation

---

### 1.2 Layer 2: Network & Communication Layer (100% Missing)

| Node Type | Status | Current Count | Required Properties | Impact |
|-----------|--------|---------------|-------------------|--------|
| `SecurityZone` | ❌ MISSING | 0 | id, name, securityLevel, zone_type, customer_namespace | **CRITICAL** - No IEC 62443 security zone modeling |
| `Conduit` | ❌ MISSING | 0 | id, name, conduit_type, security_controls, authentication_required, encryption_enabled | **CRITICAL** - Cannot model zone-to-zone communication |
| `Network` | ❌ MISSING | 0 | id, name, network_type, cidr, vlan_id, protocol | **HIGH** - No network topology |
| `NetworkInterface` | ❌ MISSING | 0 | id, name, interface_type, mac_address, ip_address, port, status | **HIGH** - Cannot map device IP addresses |

**Capability Gap:**
- ❌ Cannot determine which devices are internet-facing (DMZ vs Control Zone)
- ❌ No network reachability analysis (attacker lateral movement)
- ❌ Cannot validate zone-to-zone communication paths (IEC 62443 compliance)
- ❌ No identification of unauthorized zone crossings
- ❌ Cannot calculate network-based exposure scores

**Required Before:**
- Attack path analysis
- Network segmentation validation
- IEC 62443 compliance audits
- Lateral movement risk assessment
- Internet exposure identification

---

### 1.3 Layer 3: Software & Application Layer (80% Missing)

| Node Type | Status | Current Count | Required Properties | Impact |
|-----------|--------|---------------|-------------------|--------|
| `Software` | ⚠️ PARTIAL | ~652 (NLP docs) | id, name, vendor, product, version, **cpe**, packageUrl, software_type, customer_namespace | **CRITICAL** - CPE missing, cannot link to CVEs |
| `SoftwareComponent` | ❌ MISSING | 0 | id, name, version, packageUrl, cpe, component_type, supplier, license, hash_sha256, sbom_source | **CRITICAL** - No SBOM integration |
| `Firmware` | ❌ MISSING | 0 | id, name, version, manufacturer, release_date, hash_sha256, cpe | **HIGH** - Cannot link firmware CVEs to devices |
| `Application` | ❌ MISSING | 0 | id, name, application_type, business_criticality, customer_namespace | **MEDIUM** - No business application mapping |

**Capability Gap:**
- ❌ No CPE-based CVE→Software correlation (e.g., CVE-2021-44228 → Log4j 2.14.1)
- ❌ Cannot identify which devices run vulnerable software versions
- ❌ No SBOM dependency graph analysis (transitive vulnerabilities)
- ❌ No firmware vulnerability correlation to PLCs/RTUs/HMIs
- ❌ Cannot calculate software-based attack paths

**Required Before:**
- CVE→Asset correlation
- SBOM vulnerability analysis
- Firmware patching prioritization
- Supply chain risk assessment

---

### 1.4 Layer 4: Vulnerability & Threat Layer (60% Present)

| Node Type | Status | Current Count | Required Properties | Impact |
|-----------|--------|---------------|-------------------|--------|
| `CVE` | ✅ PRESENT | 267,487 | cveId, description, cvssV3BaseScore, cvssV3Severity, hasExploit, exploitMaturity | **COMPLETE** - Fully imported from NVD |
| `CWE` | ✅ PRESENT | 2,214 | cweId, name, description, abstraction, likelihood | **COMPLETE** - Fully imported |
| `CAPEC` | ✅ PRESENT | 615 | capecId, name, description, abstraction, likelihood, severity, prerequisites | **COMPLETE** - Fully imported |
| `Technique` | ✅ PRESENT | 834 | techniqueId, name, description, tactic, platform, detection, mitigation | **COMPLETE** - ATT&CK data imported |
| `ThreatActor` | ❌ MISSING | 0 | id, name, aliases, sophistication, resource_level, targeted_sectors, targeted_countries | **MEDIUM** - No threat actor correlation |
| `ThreatActorProfile` | ❌ MISSING | 0 | id, intent_primary, modus_operandi, preferred_tools, operational_tempo, risk_tolerance | **LOW** - Psychometric profiling absent |
| `Exploit` | ❌ MISSING | 0 | id, name, cveId, exploit_type, source, metasploit_module, verified, reliability | **HIGH** - No weaponized exploit tracking |

**Capability Gap:**
- ✅ Basic CVE→CWE→CAPEC→Technique chain present
- ❌ No threat actor attribution (APT29, Lazarus Group, etc.)
- ❌ No exploit tracking (Metasploit modules, Exploit-DB)
- ❌ Cannot correlate specific threat actors to customer's sector/geography
- ❌ No psychometric threat modeling (intent, modus operandi)

**Required Before:**
- Threat actor-specific risk assessment
- Exploit likelihood scoring
- APT campaign correlation
- Nation-state threat analysis

---

### 1.5 Layer 5: Attack Surface & Exposure Layer (100% Missing)

| Node Type | Status | Current Count | Required Properties | Impact |
|-----------|--------|---------------|-------------------|--------|
| `AttackSurface` | ❌ MISSING | 0 | id, surface_type, exposure_level, reachability, last_assessed | **CRITICAL** - No attack surface identification |
| `AttackPath` | ❌ MISSING | 0 | id, name, path_type, complexity, exploitability_score, total_hops | **CRITICAL** - Cannot model multi-hop attack chains |
| `AttackPathStep` | ❌ MISSING | 0 | id, step_number, technique_used, vulnerability_exploited, privilege_level | **CRITICAL** - No step-by-step attack modeling |

**Capability Gap:**
- ❌ Cannot calculate attack paths from internet → DMZ → control zone → safety systems
- ❌ No identification of internet-exposed vulnerable devices
- ❌ Cannot model lateral movement through network zones
- ❌ No CVSS temporal/environmental score adjustments based on reachability
- ❌ Cannot prioritize vulnerabilities based on attack surface exposure

**Required Before:**
- Attack path analysis (20+ hop queries)
- Now/Next/Never prioritization
- Penetration testing simulation
- Red team campaign modeling

---

### 1.6 Layer 6: Organizational & Business Layer (100% Missing)

| Node Type | Status | Current Count | Required Properties | Impact |
|-----------|--------|---------------|-------------------|--------|
| `Organization` | ❌ MISSING | 0 | id, name, organization_type, criticality, customer_namespace | **HIGH** - No customer isolation |
| `BusinessProcess` | ❌ MISSING | 0 | id, name, criticality, regulatory_requirements, downtime_tolerance | **MEDIUM** - No business impact modeling |
| `Compliance` | ❌ MISSING | 0 | id, framework, requirements, attestation_status, audit_date | **MEDIUM** - No compliance tracking (IEC 62443, NERC CIP, TSA SD) |

**Capability Gap:**
- ❌ No multi-tenancy (customer namespace isolation)
- ❌ Cannot correlate vulnerabilities to business process impact
- ❌ No compliance framework validation
- ❌ Cannot calculate business-weighted risk scores
- ❌ No regulatory requirement tracking

**Required Before:**
- Multi-customer deployment
- Business impact analysis
- Compliance auditing
- Executive risk reporting

---

### 1.7 Layer 7: Failure Propagation & Impact Layer (100% Missing)

| Node Type | Status | Current Count | Required Properties | Impact |
|-----------|--------|---------------|-------------------|--------|
| `FailureMode` | ❌ MISSING | 0 | id, name, failure_type, likelihood, detection_method | **MEDIUM** - No FMEA integration |
| `FailureScenario` | ❌ MISSING | 0 | id, name, trigger_conditions, propagation_path, cascading_effects | **MEDIUM** - No cascading failure modeling |
| `Impact` | ❌ MISSING | 0 | id, impact_type, severity, affected_systems, business_cost, safety_risk | **HIGH** - No impact quantification |

**Capability Gap:**
- ❌ Cannot model cascading failures (brake controller → train derailment)
- ❌ No FMEA (Failure Mode Effects Analysis) integration
- ❌ Cannot calculate safety vs security trade-offs
- ❌ No business cost estimation for vulnerability exploitation
- ❌ Cannot identify single points of failure

**Required Before:**
- Safety-critical system risk assessment
- Business continuity planning
- Insurance risk modeling
- Safety vs security trade-off analysis

---

### 1.8 Layer 8: Mitigation & Remediation Layer (100% Missing)

| Node Type | Status | Current Count | Required Properties | Impact |
|-----------|--------|---------------|-------------------|--------|
| `Mitigation` | ❌ MISSING | 0 | id, name, mitigation_type, implementation_effort, effectiveness, requires_downtime, estimated_hours, cost_estimate | **CRITICAL** - No remediation tracking |
| `Priority` | ❌ MISSING | 0 | id, type (NOW/NEXT/NEVER), score, rationale, deadline, assigned_to, status | **CRITICAL** - Cannot prioritize patches |

**Capability Gap:**
- ❌ No Now/Next/Never prioritization algorithm
- ❌ Cannot calculate risk-based priority scores
- ❌ No mitigation strategy recommendations
- ❌ No patch deployment tracking
- ❌ Cannot estimate remediation effort/cost
- ❌ No compensating control modeling

**Required Before:**
- Now/Next/Never prioritization
- Patch management workflows
- Resource allocation planning
- Remediation progress tracking

---

## 2. Missing Relationship Types Analysis

### 2.1 Asset Hierarchy Relationships (100% Missing)

| Relationship | Source → Target | Status | Properties | Impact |
|--------------|----------------|--------|-----------|--------|
| `CONTAINS_DEVICE` | PhysicalAsset → Device | ❌ | none | **CRITICAL** - No asset containment hierarchy |
| `HAS_COMPONENT` | Device → HardwareComponent | ❌ | installation_date | **HIGH** - No component tracking |
| `LOCATED_AT` | Device → Location | ❌ | since | **MEDIUM** - No geographic context |
| `INSTALLED_IN` | HardwareComponent → Device | ❌ | slot_number | **HIGH** - No component-device mapping |
| `PART_OF_SUBSYSTEM` | Device → PhysicalAsset | ❌ | subsystem_type | **CRITICAL** - No multi-hop hierarchy |
| `PART_OF_CONSIST` | PhysicalAsset → PhysicalAsset | ❌ | position | **CRITICAL** - No train consist modeling |
| `PART_OF_FLEET` | PhysicalAsset → PhysicalAsset | ❌ | commissioned_date | **CRITICAL** - No fleet aggregation |

**Query Impact:**
```cypher
// CANNOT RUN: Find all brake controllers in fleet (5-hop query)
MATCH path = (comp:HardwareComponent {name: "Brake Controller"})
  -[:INSTALLED_IN]->(device:Device)
  -[:PART_OF_SUBSYSTEM]->(car:PhysicalAsset)
  -[:PART_OF_CONSIST]->(train:PhysicalAsset)
  -[:PART_OF_FLEET]->(fleet:PhysicalAsset {id: 'asset-fleet-regional'})
RETURN comp, length(path) AS hops
// ERROR: No relationships exist
```

---

### 2.2 Network Topology Relationships (100% Missing)

| Relationship | Source → Target | Status | Properties | Impact |
|--------------|----------------|--------|-----------|--------|
| `HAS_INTERFACE` | Device → NetworkInterface | ❌ | interface_name | **CRITICAL** - No network connectivity |
| `CONNECTED_TO` | NetworkInterface → Network | ❌ | connection_speed | **CRITICAL** - No topology mapping |
| `PART_OF` | Network → SecurityZone | ❌ | vlan_id | **CRITICAL** - No zone assignment |
| `COMMUNICATES_VIA` | SecurityZone → Conduit | ❌ | bidirectional | **HIGH** - No zone-to-zone paths |
| `TO_ZONE` | Conduit → SecurityZone | ❌ | allowed_protocols | **HIGH** - No conduit destinations |

**Query Impact:**
```cypher
// CANNOT RUN: Find internet-facing devices with critical CVEs
MATCH (device:Device)-[:HAS_INTERFACE]->(netif:NetworkInterface)
  -[:CONNECTED_TO]->(network:Network)
  -[:PART_OF]->(zone:SecurityZone {zone_type: 'DMZ'})
WHERE device.criticalityLevel = 'CRITICAL'
  AND EXISTS {
    MATCH (device)-[:RUNS_SOFTWARE]->(:Software)
      -[:HAS_VULNERABILITY]->(cve:CVE)
    WHERE cve.cvssV3Severity = 'CRITICAL'
  }
RETURN device.name, zone.securityLevel
// ERROR: No network relationships exist
```

---

### 2.3 Software-to-Asset Relationships (95% Missing)

| Relationship | Source → Target | Status | Properties | Impact |
|--------------|----------------|--------|-----------|--------|
| `RUNS_SOFTWARE` | Device → Software | ❌ | installed_date, version | **CRITICAL** - Cannot link software to devices |
| `RUNS_FIRMWARE` | Device → Firmware | ❌ | flashed_date, hash_sha256 | **CRITICAL** - Cannot link firmware to PLCs |
| `HAS_COMPONENT` | Software → SoftwareComponent | ❌ | dependency_type, scope | **CRITICAL** - No SBOM relationships |
| `DEPENDS_ON` | SoftwareComponent → SoftwareComponent | ❌ | dependency_type, scope | **HIGH** - No transitive dependencies |
| `DEPENDS_ON_SOFTWARE` | Application → Software | ❌ | required_version | **MEDIUM** - No app→software mapping |

**Query Impact:**
```cypher
// CANNOT RUN: Find all devices with Log4Shell vulnerability
MATCH (device:Device)-[:RUNS_SOFTWARE]->(software:Software)
  -[:HAS_COMPONENT]->(comp:SoftwareComponent {name: 'Apache Log4j'})
  -[:HAS_VULNERABILITY]->(cve:CVE {cveId: 'CVE-2021-44228'})
WHERE comp.version IN ['2.0-beta9', '2.14.1']
RETURN device.name, software.name, comp.version, cve.cvssV3BaseScore
// ERROR: No software→device relationships exist
```

---

### 2.4 Vulnerability-to-Asset Correlation (100% Missing)

| Relationship | Source → Target | Status | Properties | Impact |
|--------------|----------------|--------|-----------|--------|
| `HAS_VULNERABILITY` | Software → CVE | ❌ | affected_versions, fixed_in_version, patch_available | **CRITICAL** - Cannot link CVEs to software |
| `HAS_VULNERABILITY` | Firmware → CVE | ❌ | affected_versions, fixed_in_version | **CRITICAL** - Cannot link CVEs to firmware |
| `HAS_VULNERABILITY` | SoftwareComponent → CVE | ❌ | affected_versions, fixed_in_version | **CRITICAL** - No SBOM→CVE correlation |

**Current State:**
- ✅ CVE→CWE relationships present (2,214 links)
- ✅ CVE→CAPEC relationships present (615 links)
- ✅ CAPEC→Technique relationships present (834 links)
- ❌ **NO CVE→Software/Firmware relationships** (0 links)

**Query Impact:**
```cypher
// CANNOT RUN: Find all Siemens S7-1500 PLCs with critical firmware CVEs
MATCH (device:Device {manufacturer: 'Siemens', model: 'S7-1500'})
  -[:RUNS_FIRMWARE]->(fw:Firmware)
  -[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.cvssV3Severity = 'CRITICAL'
  AND cve.hasExploit = true
RETURN device.name, fw.version, cve.cveId, cve.cvssV3BaseScore
// ERROR: No firmware→CVE relationships exist
```

---

### 2.5 Attack Path Relationships (100% Missing)

| Relationship | Source → Target | Status | Properties | Impact |
|--------------|----------------|--------|-----------|--------|
| `EXPOSES` | Device → AttackSurface | ❌ | exposure_type, reachability | **CRITICAL** - No attack surface mapping |
| `HAS_ATTACK_PATH` | AttackSurface → AttackPath | ❌ | likelihood, complexity | **CRITICAL** - No attack path modeling |
| `HAS_STEP` | AttackPath → AttackPathStep | ❌ | step_number, required_technique | **CRITICAL** - No step-by-step paths |
| `EXPLOITS` | AttackPathStep → CVE | ❌ | success_probability | **HIGH** - No CVE→path correlation |
| `USES_TECHNIQUE` | AttackPathStep → Technique | ❌ | detection_difficulty | **HIGH** - No ATT&CK technique mapping |
| `CROSSES_ZONE` | AttackPathStep → SecurityZone | ❌ | permission_required | **HIGH** - No zone traversal tracking |

**Query Impact:**
```cypher
// CANNOT RUN: Find 8+ hop attack paths from internet to safety systems
MATCH path = (internet:SecurityZone {zone_type: 'DMZ'})
  -[:HAS_ATTACK_PATH]->(:AttackPath)
  -[:HAS_STEP*8..]->(step:AttackPathStep)
  -[:CROSSES_ZONE]->(safety:SecurityZone {zone_type: 'SAFETY'})
WHERE ALL(s IN nodes(path) WHERE s:AttackPathStep)
RETURN path, length(path) AS hops
// ERROR: No attack path relationships exist
```

---

### 2.6 Threat Intelligence Relationships (60% Missing)

| Relationship | Source → Target | Status | Properties | Impact |
|--------------|----------------|--------|-----------|--------|
| `IS_WEAKNESS_TYPE` | CVE → CWE | ✅ PRESENT | confidence | **COMPLETE** - 2,214 links |
| `ENABLES_ATTACK_PATTERN` | CVE → CAPEC | ✅ PRESENT | relevance_score | **COMPLETE** - 615 links |
| `EXPLOITS_WEAKNESS` | CAPEC → CWE | ✅ PRESENT | exploitation_method | **COMPLETE** - Present |
| `MAPS_TO_TECHNIQUE` | CAPEC → Technique | ✅ PRESENT | mapping_confidence | **COMPLETE** - 834 links |
| `HAS_EXPLOIT` | CVE → Exploit | ❌ | availability_date | **HIGH** - No exploit tracking |
| `USED_BY_THREAT_ACTOR` | Exploit → ThreatActor | ❌ | first_observed, last_observed | **MEDIUM** - No threat actor links |
| `USES_TTP` | ThreatActor → Technique | ❌ | frequency, campaigns | **MEDIUM** - No TTP correlation |
| `HAS_PROFILE` | ThreatActor → ThreatActorProfile | ❌ | profile_confidence | **LOW** - No psychometric data |

---

### 2.7 Mitigation & Prioritization Relationships (100% Missing)

| Relationship | Source → Target | Status | Properties | Impact |
|--------------|----------------|--------|-----------|--------|
| `MITIGATED_BY` | CVE → Mitigation | ❌ | effectiveness_rating, recommended | **CRITICAL** - No remediation options |
| `HAS_PRIORITY` | Mitigation → Priority | ❌ | calculation_date | **CRITICAL** - No Now/Next/Never |
| `BLOCKS` | Priority → Priority | ❌ | blocking_reason | **HIGH** - No dependency tracking |
| `HAS_PRIORITY_SCORE` | CVE → Priority | ❌ | score, rationale | **CRITICAL** - No CVE prioritization |

**Query Impact:**
```cypher
// CANNOT RUN: Generate Now/Next/Never dashboard
MATCH (p:Priority)
OPTIONAL MATCH (p)<-[:HAS_PRIORITY]-(m:Mitigation)
OPTIONAL MATCH (m)<-[:MITIGATED_BY]-(cve:CVE)
RETURN p.type AS priority_level,
       count(DISTINCT m) AS mitigation_count,
       count(DISTINCT cve) AS cve_count,
       sum(m.estimated_hours) AS total_effort_hours
ORDER BY CASE p.type
  WHEN 'NOW' THEN 1
  WHEN 'NEXT' THEN 2
  WHEN 'NEVER' THEN 3
END
// ERROR: No mitigation/priority relationships exist
```

---

## 3. Missing Properties on Existing Nodes

### 3.1 CVE Node Enhancements Needed

| Property | Status | Required For | Impact |
|----------|--------|--------------|--------|
| `customer_namespace` | ❌ MISSING | Multi-tenancy isolation | **CRITICAL** - Cannot isolate customer CVE priorities |
| `exploitMaturity` | ❌ MISSING | CVSS temporal scoring | **HIGH** - No exploit maturity tracking |
| `remediationLevel` | ❌ MISSING | CVSS temporal scoring | **HIGH** - No patch availability tracking |
| `reportConfidence` | ❌ MISSING | CVSS temporal scoring | **MEDIUM** - No confidence assessment |
| `cpeMatchStrings` | ❌ MISSING | CPE-based asset correlation | **CRITICAL** - Cannot link CVEs to devices via CPE |
| `references` | ❌ MISSING | Threat intelligence sources | **MEDIUM** - No external reference tracking |
| `affectedProducts` | ❌ MISSING | Product filtering | **HIGH** - Cannot search by vendor/product |

**Current CVE Properties:**
```cypher
(cve:CVE {
  cveId: "CVE-2022-22954",           // ✅ Present
  description: "...",                 // ✅ Present
  cvssV3BaseScore: 9.8,              // ✅ Present
  cvssV3Severity: "CRITICAL",        // ✅ Present
  publishedDate: date('2022-04-06'), // ✅ Present
  hasExploit: true                   // ✅ Present
  // ❌ Missing: CPE match strings, affected products, temporal scores
})
```

---

### 3.2 Software Node Enhancements Needed

| Property | Status | Required For | Impact |
|----------|--------|--------------|--------|
| `cpe` | ❌ MISSING | CVE correlation | **CRITICAL** - Cannot match CVEs to software |
| `packageUrl` | ❌ MISSING | SBOM PURL correlation | **HIGH** - Cannot link SBOM components |
| `vendor` | ❌ MISSING | Vendor filtering | **HIGH** - Cannot search by vendor |
| `version` | ❌ MISSING | Version-specific CVE matching | **CRITICAL** - Cannot determine vulnerable versions |
| `customer_namespace` | ❌ MISSING | Multi-tenancy | **CRITICAL** - Cannot isolate customer software |

---

### 3.3 Device Node Properties (All Missing - Node Doesn't Exist)

**Required Properties:**
```cypher
(device:Device {
  id: UUID,                    // ❌ Missing
  name: string,                // ❌ Missing
  manufacturer: string,        // ❌ Missing
  model: string,              // ❌ Missing
  serialNumber: string,       // ❌ Missing
  cpe: string,                // ❌ Missing - CRITICAL for CVE correlation
  firmwareVersion: string,    // ❌ Missing
  criticalityLevel: enum,     // ❌ Missing - CRITICAL for prioritization
  deviceType: enum,           // ❌ Missing
  customer_namespace: string, // ❌ Missing - CRITICAL for multi-tenancy
  installation_date: date,    // ❌ Missing
  last_maintenance: date      // ❌ Missing
})
```

---

## 4. Missing Indexes for Performance

### 4.1 Critical Missing Indexes

| Index Name | Node Type | Properties | Purpose | Impact |
|------------|-----------|-----------|---------|--------|
| `device_cpe` | Device | cpe | CVE→Device correlation via CPE | **CRITICAL** - O(n) scan without |
| `software_cpe` | Software | cpe | CVE→Software correlation | **CRITICAL** - O(n) scan without |
| `software_purl` | Software | packageUrl | SBOM PURL matching | **HIGH** - SBOM correlation slow |
| `cve_cpe_match` | CVE | cpeMatchStrings | CPE-based vulnerability lookup | **CRITICAL** - Cannot find affected CVEs |
| `device_customer_namespace` | Device | customer_namespace | Multi-tenant isolation | **CRITICAL** - Slow customer queries |
| `software_customer_namespace` | Software | customer_namespace | Multi-tenant isolation | **CRITICAL** - Slow customer queries |
| `network_interface_ip` | NetworkInterface | ip_address | IP-based device lookup | **HIGH** - Network queries slow |
| `security_zone_level` | SecurityZone | securityLevel | Zone-based filtering | **MEDIUM** - Present in schema, not deployed |
| `priority_score` | Priority | score | Now/Next/Never sorting | **CRITICAL** - Priority queries slow |

**Currently Present Indexes:**
```cypher
// ✅ Deployed indexes
CREATE INDEX cve_cvss_score IF NOT EXISTS
FOR (c:CVE) ON (c.cvssV3BaseScore);

CREATE INDEX cve_published_date IF NOT EXISTS
FOR (c:CVE) ON (c.publishedDate);

CREATE INDEX cve_exploitability IF NOT EXISTS
FOR (c:CVE) ON (c.exploitabilityScore);
```

**Missing Critical Indexes:**
```cypher
// ❌ NOT deployed (schema defined, not executed)
CREATE INDEX device_cpe IF NOT EXISTS
FOR (d:Device) ON (d.cpe);  // CRITICAL - CVE correlation

CREATE INDEX software_cpe IF NOT EXISTS
FOR (s:Software) ON (s.cpe);  // CRITICAL - CVE correlation

CREATE INDEX device_namespace IF NOT EXISTS
FOR (d:Device) ON (d.customer_namespace);  // CRITICAL - Multi-tenancy
```

---

### 4.2 Composite Index Requirements

| Index Name | Node Type | Properties | Query Pattern | Impact |
|------------|-----------|-----------|---------------|--------|
| `device_criticality_namespace` | Device | (criticalityLevel, customer_namespace) | Critical devices per customer | **HIGH** |
| `cve_severity_exploitable` | CVE | (cvssV3BaseScore, hasExploit) | Exploitable high-severity CVEs | **HIGH** |
| `software_vendor_product_version` | Software | (vendor, product, version) | Exact software matching | **CRITICAL** |
| `entity_text_label` | Entity | (text, label) | NLP entity MERGE operations | **MEDIUM** - From NLP pipeline |

---

## 5. Missing Constraints for Data Quality

### 5.1 Critical Missing Constraints

| Constraint | Node Type | Property | Purpose | Impact |
|------------|-----------|----------|---------|--------|
| `device_id` | Device | id | Prevent duplicate devices | **CRITICAL** - Node doesn't exist |
| `software_id` | Software | id | Prevent duplicate software | **HIGH** - Weak identity |
| `firmware_id` | Firmware | id | Prevent duplicate firmware | **HIGH** - Node doesn't exist |
| `security_zone_id` | SecurityZone | id | Prevent duplicate zones | **CRITICAL** - Node doesn't exist |
| `mitigation_id` | Mitigation | id | Prevent duplicate mitigations | **CRITICAL** - Node doesn't exist |
| `priority_id` | Priority | id | Prevent duplicate priorities | **CRITICAL** - Node doesn't exist |

**Currently Present Constraints:**
```cypher
// ✅ Deployed constraints
CREATE CONSTRAINT cve_id IF NOT EXISTS
FOR (c:CVE) REQUIRE c.cveId IS UNIQUE;

CREATE CONSTRAINT cwe_id IF NOT EXISTS
FOR (c:CWE) REQUIRE c.cweId IS UNIQUE;

CREATE CONSTRAINT capec_id IF NOT EXISTS
FOR (c:CAPEC) REQUIRE c.capecId IS UNIQUE;

CREATE CONSTRAINT technique_id IF NOT EXISTS
FOR (t:Technique) REQUIRE t.techniqueId IS UNIQUE;
```

**Missing Constraints (Defined but Not Deployed):**
```cypher
// ❌ Schema defined, but nodes don't exist
CREATE CONSTRAINT device_id IF NOT EXISTS
FOR (d:Device) REQUIRE d.id IS UNIQUE;

CREATE CONSTRAINT software_id IF NOT EXISTS
FOR (s:Software) REQUIRE s.id IS UNIQUE;

CREATE CONSTRAINT mitigation_id IF NOT EXISTS
FOR (m:Mitigation) REQUIRE m.id IS UNIQUE;
```

---

## 6. Query Capabilities Gap

### 6.1 Queries That CANNOT Be Run Today

#### Query 1: Find All Devices Affected by CVE-2021-44228 (Log4Shell)
```cypher
// ❌ CANNOT RUN - No Device nodes or relationships
MATCH (device:Device)-[:RUNS_SOFTWARE]->(software:Software)
  -[:HAS_COMPONENT]->(comp:SoftwareComponent {name: 'Apache Log4j'})
  -[:HAS_VULNERABILITY]->(cve:CVE {cveId: 'CVE-2021-44228'})
WHERE comp.version IN ['2.0-beta9', '2.14.1']
RETURN device.name AS affected_device,
       device.manufacturer AS vendor,
       device.criticalityLevel AS criticality,
       software.name AS vulnerable_software,
       comp.version AS log4j_version
ORDER BY device.criticalityLevel DESC
```

**Missing Components:**
- ❌ Device nodes
- ❌ RUNS_SOFTWARE relationships
- ❌ SoftwareComponent nodes
- ❌ HAS_COMPONENT relationships
- ❌ HAS_VULNERABILITY relationships (Software→CVE)

---

#### Query 2: Calculate 8-Hop Attack Path from Internet to Safety Systems
```cypher
// ❌ CANNOT RUN - No network topology or attack path nodes
MATCH path = (start:SecurityZone {zone_type: 'DMZ'})
  <-[:PART_OF]-(dmz_net:Network)
  <-[:CONNECTED_TO]-(dmz_iface:NetworkInterface)
  <-[:HAS_INTERFACE]-(dmz_device:Device)
  -[:RUNS_SOFTWARE]->(vuln_software:Software)
  -[:HAS_VULNERABILITY]->(cve:CVE {cvssV3Severity: 'CRITICAL'})
  <-[:EXPLOITS]-(attack_step:AttackPathStep)
  -[:CROSSES_ZONE]->(control_zone:SecurityZone {zone_type: 'CONTROL'})
  <-[:PART_OF]-(control_net:Network)
  <-[:CONNECTED_TO]-(safety_iface:NetworkInterface)
  <-[:HAS_INTERFACE]-(safety_device:Device {deviceType: 'PLC'})
WHERE cve.hasExploit = true
RETURN path,
       length(path) AS total_hops,
       [node IN nodes(path) WHERE node:Device | node.name] AS devices_in_path,
       [node IN nodes(path) WHERE node:CVE | node.cveId] AS vulnerabilities_exploited
```

**Missing Components:**
- ❌ SecurityZone nodes
- ❌ Network nodes
- ❌ NetworkInterface nodes
- ❌ Device nodes
- ❌ AttackPathStep nodes
- ❌ All network topology relationships
- ❌ All attack path relationships

---

#### Query 3: Generate Now/Next/Never Priority Dashboard
```cypher
// ❌ CANNOT RUN - No Priority or Mitigation nodes
MATCH (p:Priority)
OPTIONAL MATCH (p)<-[:HAS_PRIORITY]-(m:Mitigation)
OPTIONAL MATCH (m)<-[:MITIGATED_BY]-(cve:CVE)
OPTIONAL MATCH (cve)<-[:HAS_VULNERABILITY]-(software:Software)
  <-[:RUNS_SOFTWARE]-(device:Device)
WHERE device.customer_namespace = 'customer:RailOperator-XYZ'
  AND device.criticalityLevel IN ['CRITICAL', 'HIGH']
RETURN p.type AS priority_level,
       count(DISTINCT m) AS mitigation_count,
       count(DISTINCT cve) AS cve_count,
       sum(m.estimated_hours) AS total_effort_hours,
       sum(m.cost_estimate) AS total_budget,
       min(p.deadline) AS earliest_deadline
ORDER BY
  CASE p.type
    WHEN 'NOW' THEN 1
    WHEN 'NEXT' THEN 2
    WHEN 'NEVER' THEN 3
  END
```

**Missing Components:**
- ❌ Priority nodes
- ❌ Mitigation nodes
- ❌ HAS_PRIORITY relationships
- ❌ MITIGATED_BY relationships
- ❌ HAS_VULNERABILITY relationships (Software→CVE)
- ❌ RUNS_SOFTWARE relationships (Device→Software)

---

#### Query 4: Find All Brake Controllers in Regional Fleet with Critical CVEs
```cypher
// ❌ CANNOT RUN - No asset hierarchy nodes
MATCH path = (comp:HardwareComponent {componentType: 'CPU_MODULE'})
  -[:INSTALLED_IN]->(brake_system:Device {deviceType: 'ACTUATOR'})
  -[:PART_OF_SUBSYSTEM]->(train_car:PhysicalAsset {type: 'VEHICLE'})
  -[:PART_OF_CONSIST]->(train:PhysicalAsset)
  -[:PART_OF_FLEET]->(fleet:PhysicalAsset {id: 'asset-fleet-regional'})
WHERE comp.name CONTAINS 'Brake'
  AND EXISTS {
    MATCH (brake_system)-[:RUNS_FIRMWARE]->(fw:Firmware)
      -[:HAS_VULNERABILITY]->(cve:CVE)
    WHERE cve.cvssV3Severity = 'CRITICAL'
  }
RETURN comp.name AS component,
       comp.manufacturer AS vendor,
       brake_system.name AS brake_system,
       train_car.name AS train_car,
       train.name AS train,
       length(path) AS hierarchy_depth,
       collect(DISTINCT cve.cveId) AS critical_vulnerabilities
```

**Missing Components:**
- ❌ HardwareComponent nodes
- ❌ PhysicalAsset nodes
- ❌ Device nodes (brake systems)
- ❌ Firmware nodes
- ❌ All asset hierarchy relationships
- ❌ HAS_VULNERABILITY relationships (Firmware→CVE)

---

#### Query 5: Identify Internet-Exposed Devices with Critical CVEs
```cypher
// ❌ CANNOT RUN - No network topology
MATCH (device:Device)-[:HAS_INTERFACE]->(netif:NetworkInterface)
  -[:CONNECTED_TO]->(network:Network)
  -[:PART_OF]->(zone:SecurityZone)
WHERE zone.zone_type IN ['DMZ', 'ENTERPRISE']
  AND zone.securityLevel IN ['SL1', 'SL2']
  AND EXISTS {
    MATCH (device)-[:RUNS_SOFTWARE]->(software:Software)
      -[:HAS_VULNERABILITY]->(cve:CVE)
    WHERE cve.cvssV3BaseScore >= 9.0
      AND cve.hasExploit = true
  }
RETURN device.name AS exposed_device,
       device.manufacturer AS vendor,
       device.deviceType AS type,
       netif.ip_address AS ip_address,
       zone.name AS security_zone,
       zone.securityLevel AS security_level,
       collect(DISTINCT cve.cveId) AS critical_cves
ORDER BY zone.securityLevel ASC, device.criticalityLevel DESC
```

**Missing Components:**
- ❌ Device nodes
- ❌ NetworkInterface nodes
- ❌ Network nodes
- ❌ SecurityZone nodes
- ❌ All network topology relationships
- ❌ HAS_VULNERABILITY relationships (Software→CVE)

---

### 6.2 Queries That CAN Run Today (Limited Threat Intelligence)

#### Query 1: Find Critical CVEs Published in Last 30 Days ✅
```cypher
// ✅ CAN RUN - Uses only CVE nodes
MATCH (cve:CVE)
WHERE cve.publishedDate >= date() - duration({days: 30})
  AND cve.cvssV3Severity = 'CRITICAL'
  AND cve.hasExploit = true
RETURN cve.cveId,
       cve.description,
       cve.cvssV3BaseScore,
       cve.publishedDate
ORDER BY cve.cvssV3BaseScore DESC
LIMIT 50
```

---

#### Query 2: Map CVE → CWE → CAPEC → ATT&CK Technique Chain ✅
```cypher
// ✅ CAN RUN - Uses threat intelligence relationships
MATCH path = (cve:CVE {cveId: 'CVE-2022-22954'})
  -[:IS_WEAKNESS_TYPE]->(cwe:CWE)
  <-[:EXPLOITS_WEAKNESS]-(capec:CAPEC)
  -[:MAPS_TO_TECHNIQUE]->(technique:Technique)
RETURN cve.cveId AS vulnerability,
       cve.cvssV3BaseScore AS severity,
       cwe.cweId AS weakness,
       capec.capecId AS attack_pattern,
       technique.techniqueId AS attack_technique,
       technique.name AS technique_name,
       technique.tactic AS tactic,
       length(path) AS hop_count
```

---

#### Query 3: Find All CWEs Associated with ATT&CK Technique T1190 ✅
```cypher
// ✅ CAN RUN - Uses CAPEC→Technique and CAPEC→CWE relationships
MATCH (technique:Technique {techniqueId: 'T1190'})
  <-[:MAPS_TO_TECHNIQUE]-(capec:CAPEC)
  -[:EXPLOITS_WEAKNESS]->(cwe:CWE)
RETURN technique.name AS technique,
       collect(DISTINCT capec.name) AS attack_patterns,
       collect(DISTINCT cwe.cweId) AS weaknesses,
       count(DISTINCT cwe) AS weakness_count
```

---

## 7. Priority Assessment

### 7.1 CRITICAL Priority (Implement First)

| Gap Category | Impact | Effort | Priority Score |
|-------------|--------|--------|---------------|
| **Missing CPE nodes** | 10/10 | 4/10 | **P0 CRITICAL** |
| **Missing Device nodes** | 10/10 | 6/10 | **P0 CRITICAL** |
| **Missing Software→CVE relationships** | 10/10 | 5/10 | **P0 CRITICAL** |
| **Missing customer_namespace isolation** | 9/10 | 3/10 | **P0 CRITICAL** |
| **Missing device_cpe index** | 9/10 | 2/10 | **P0 CRITICAL** |
| **Missing Priority/Mitigation nodes** | 9/10 | 7/10 | **P0 CRITICAL** |

**Justification:**
- Cannot correlate CVEs to real assets without CPE/Device nodes
- Cannot build Now/Next/Never prioritization without Priority nodes
- Cannot isolate customer data without namespace implementation
- Cannot run any asset-to-vulnerability queries

---

### 7.2 HIGH Priority (Implement Next)

| Gap Category | Impact | Effort | Priority Score |
|-------------|--------|--------|---------------|
| **Missing SecurityZone/Network nodes** | 8/10 | 7/10 | **P1 HIGH** |
| **Missing Firmware nodes** | 8/10 | 5/10 | **P1 HIGH** |
| **Missing SoftwareComponent/SBOM** | 8/10 | 8/10 | **P1 HIGH** |
| **Missing AttackPath nodes** | 8/10 | 9/10 | **P1 HIGH** |
| **Missing ThreatActor/Exploit nodes** | 7/10 | 6/10 | **P1 HIGH** |

**Justification:**
- Network topology required for attack path analysis
- SBOM integration critical for supply chain risk
- Attack path modeling enables penetration testing simulation

---

### 7.3 MEDIUM Priority (Implement Later)

| Gap Category | Impact | Effort | Priority Score |
|-------------|--------|--------|---------------|
| **Missing PhysicalAsset hierarchy** | 7/10 | 8/10 | **P2 MEDIUM** |
| **Missing Organization/BusinessProcess** | 6/10 | 5/10 | **P2 MEDIUM** |
| **Missing FailureMode/Impact nodes** | 6/10 | 7/10 | **P2 MEDIUM** |
| **Missing Compliance nodes** | 5/10 | 4/10 | **P2 MEDIUM** |

**Justification:**
- Fleet hierarchy useful but not blocking core functionality
- Business impact analysis valuable for executive reporting
- Compliance tracking important for regulated industries

---

### 7.4 LOW Priority (Future Enhancements)

| Gap Category | Impact | Effort | Priority Score |
|-------------|--------|--------|---------------|
| **Missing ThreatActorProfile psychometric data** | 4/10 | 6/10 | **P3 LOW** |
| **Missing Location nodes** | 3/10 | 3/10 | **P3 LOW** |
| **Missing temporal indexes** | 4/10 | 2/10 | **P3 LOW** |
| **Missing entity clustering** | 3/10 | 5/10 | **P3 LOW** |

**Justification:**
- Psychometric profiling is advanced threat intelligence
- Location data useful for geographic analysis but not critical
- Temporal queries can be handled with existing date filters

---

## 8. Implementation Roadmap

### Phase 1: Critical Asset-CVE Correlation (Weeks 1-2)

**Objective:** Enable basic CVE→Asset correlation queries

**Tasks:**
1. Create CPE nodes (extract from NVD CVE data)
2. Create Device node schema
3. Implement customer_namespace isolation
4. Add device_cpe and software_cpe indexes
5. Create HAS_VULNERABILITY relationships (CVE→Software via CPE)
6. Import sample device data (10-20 test devices)

**Validation Queries:**
```cypher
// Test Query 1: Find devices affected by CVE-2021-44228
MATCH (device:Device {cpe: 'cpe:2.3:a:vmware:workspace_one_access:21.08.0.0:*:*:*:*:*:*:*'})
  -[:RUNS_SOFTWARE]->(software:Software)
  -[:HAS_VULNERABILITY]->(cve:CVE {cveId: 'CVE-2021-44228'})
RETURN device.name, software.name, cve.cvssV3BaseScore

// Expected Result: 1+ devices returned
```

**Deliverables:**
- ✅ CPE nodes in database
- ✅ Device nodes with CPE properties
- ✅ Customer namespace isolation working
- ✅ CVE→Software correlation functional

---

### Phase 2: Network Topology & Attack Surface (Weeks 3-4)

**Objective:** Enable network-based attack surface analysis

**Tasks:**
1. Create SecurityZone, Network, NetworkInterface nodes
2. Create Conduit nodes for zone-to-zone communication
3. Implement IEC 62443 security level mapping
4. Add network_interface_ip, security_zone_level indexes
5. Create network topology relationships
6. Import sample network topology (enterprise + DMZ + control + safety zones)

**Validation Queries:**
```cypher
// Test Query 2: Find internet-facing devices with critical CVEs
MATCH (device:Device)-[:HAS_INTERFACE]->(netif:NetworkInterface)
  -[:CONNECTED_TO]->(network:Network)
  -[:PART_OF]->(zone:SecurityZone {zone_type: 'DMZ'})
WHERE EXISTS {
  MATCH (device)-[:RUNS_SOFTWARE]->(:Software)
    -[:HAS_VULNERABILITY]->(cve:CVE)
  WHERE cve.cvssV3Severity = 'CRITICAL'
}
RETURN device.name, netif.ip_address, zone.securityLevel

// Expected Result: 1+ internet-exposed devices returned
```

**Deliverables:**
- ✅ Network topology nodes deployed
- ✅ SecurityZone hierarchy functional
- ✅ IP-based device lookup working
- ✅ Zone-to-zone communication paths mapped

---

### Phase 3: Now/Next/Never Prioritization (Weeks 5-6)

**Objective:** Enable risk-based vulnerability prioritization

**Tasks:**
1. Create Priority, Mitigation nodes
2. Implement priority scoring algorithm (CVSS + exploit + exposure)
3. Create MITIGATED_BY, HAS_PRIORITY relationships
4. Add priority_score, priority_type indexes
5. Implement Now/Next/Never calculation logic
6. Generate priority scores for all CVEs

**Validation Queries:**
```cypher
// Test Query 3: Generate Now/Next/Never dashboard
MATCH (p:Priority)
OPTIONAL MATCH (p)<-[:HAS_PRIORITY]-(m:Mitigation)
OPTIONAL MATCH (m)<-[:MITIGATED_BY]-(cve:CVE)
RETURN p.type AS priority,
       count(DISTINCT m) AS mitigations,
       count(DISTINCT cve) AS vulnerabilities,
       sum(m.estimated_hours) AS effort_hours
ORDER BY CASE p.type
  WHEN 'NOW' THEN 1
  WHEN 'NEXT' THEN 2
  WHEN 'NEVER' THEN 3
END

// Expected Result: NOW/NEXT/NEVER breakdown with counts
```

**Deliverables:**
- ✅ Priority nodes with Now/Next/Never categorization
- ✅ Mitigation options linked to CVEs
- ✅ Risk-based scoring algorithm functional
- ✅ Dashboard queries returning results

---

### Phase 4: SBOM & Software Supply Chain (Weeks 7-8)

**Objective:** Enable SBOM-based vulnerability analysis

**Tasks:**
1. Create SoftwareComponent, Firmware nodes
2. Implement SBOM PURL parsing (CycloneDX, SPDX)
3. Create HAS_COMPONENT, DEPENDS_ON relationships
4. Add software_purl index
5. Import sample SBOMs (3-5 applications)
6. Build transitive dependency graph

**Validation Queries:**
```cypher
// Test Query 4: Find transitive Log4j dependencies
MATCH path = (software:Software {name: 'VMware Workspace ONE Access'})
  -[:HAS_COMPONENT*1..3]->(comp:SoftwareComponent)
WHERE comp.name CONTAINS 'log4j'
  AND EXISTS {
    MATCH (comp)-[:HAS_VULNERABILITY]->(cve:CVE)
    WHERE cve.cvssV3Severity IN ['HIGH', 'CRITICAL']
  }
RETURN software.name,
       [c IN nodes(path) WHERE c:SoftwareComponent | c.name] AS dependency_chain,
       length(path) AS dependency_depth

// Expected Result: Dependency chains to Log4j
```

**Deliverables:**
- ✅ SoftwareComponent nodes from SBOMs
- ✅ Dependency graph constructed
- ✅ Transitive vulnerability tracking working
- ✅ PURL-based correlation functional

---

### Phase 5: Attack Path Analysis (Weeks 9-10)

**Objective:** Enable multi-hop attack path modeling

**Tasks:**
1. Create AttackSurface, AttackPath, AttackPathStep nodes
2. Implement attack path generation algorithm
3. Create path relationships (EXPOSES, HAS_ATTACK_PATH, HAS_STEP)
4. Add attack path complexity scoring
5. Generate sample attack paths (internet → safety systems)
6. Validate 8+ hop queries

**Validation Queries:**
```cypher
// Test Query 5: Find 8-hop attack paths to safety systems
MATCH path = (dmz:SecurityZone {zone_type: 'DMZ'})
  -[:HAS_ATTACK_PATH]->(:AttackPath)
  -[:HAS_STEP*8..]->(step:AttackPathStep)
  -[:CROSSES_ZONE]->(safety:SecurityZone {zone_type: 'SAFETY'})
WHERE ALL(s IN nodes(path) WHERE s:AttackPathStep)
RETURN path,
       length(path) AS total_hops,
       [n IN nodes(path) WHERE n:AttackPathStep | n.technique_used] AS techniques
LIMIT 10

// Expected Result: Multi-hop attack paths returned
```

**Deliverables:**
- ✅ Attack path nodes deployed
- ✅ Path generation algorithm functional
- ✅ 8+ hop queries working
- ✅ Attack complexity scoring implemented

---

### Phase 6: Asset Hierarchy & Fleet Management (Weeks 11-12)

**Objective:** Enable fleet-wide vulnerability analysis

**Tasks:**
1. Create PhysicalAsset, HardwareComponent nodes
2. Implement asset hierarchy (fleet → train → car → component)
3. Create asset containment relationships
4. Add customer_namespace to all asset nodes
5. Import sample fleet data (regional rail fleet)
6. Validate 5+ hop asset traversal queries

**Validation Queries:**
```cypher
// Test Query 6: Find all brake controllers in fleet with CVEs
MATCH path = (comp:HardwareComponent {name: 'Brake Controller'})
  -[:INSTALLED_IN]->(device:Device)
  -[:PART_OF_SUBSYSTEM]->(car:PhysicalAsset)
  -[:PART_OF_CONSIST]->(train:PhysicalAsset)
  -[:PART_OF_FLEET]->(fleet:PhysicalAsset {id: 'asset-fleet-regional'})
WHERE EXISTS {
  MATCH (device)-[:RUNS_FIRMWARE]->(fw:Firmware)
    -[:HAS_VULNERABILITY]->(cve:CVE {cvssV3Severity: 'CRITICAL'})
}
RETURN comp.name, device.name, car.name, train.name,
       length(path) AS hierarchy_depth

// Expected Result: Brake controller hierarchy paths
```

**Deliverables:**
- ✅ Asset hierarchy nodes deployed
- ✅ 5+ hop traversal working
- ✅ Fleet-wide queries functional
- ✅ Component-level vulnerability tracking enabled

---

### Phase 7: Threat Intelligence Enhancement (Weeks 13-14)

**Objective:** Add threat actor and exploit tracking

**Tasks:**
1. Create ThreatActor, Exploit, ThreatActorProfile nodes
2. Import threat actor data (APT29, Lazarus Group, etc.)
3. Create HAS_EXPLOIT, USED_BY_THREAT_ACTOR relationships
4. Link exploits to CVEs
5. Add threat actor sector/geography targeting
6. Implement psychometric profiling (optional)

**Validation Queries:**
```cypher
// Test Query 7: Find threat actors targeting customer's sector
MATCH (ta:ThreatActor)-[:USES_TTP]->(tech:Technique)
  <-[:MAPS_TO_TECHNIQUE]-(capec:CAPEC)
  -[:EXPLOITS_WEAKNESS]->(cwe:CWE)
  <-[:IS_WEAKNESS_TYPE]-(cve:CVE)
WHERE 'transportation' IN ta.targeted_sectors
  AND cve.hasExploit = true
RETURN ta.name,
       ta.sophistication,
       collect(DISTINCT cve.cveId) AS relevant_cves,
       collect(DISTINCT tech.name) AS techniques_used

// Expected Result: Threat actors targeting transportation
```

**Deliverables:**
- ✅ Threat actor nodes deployed
- ✅ Exploit tracking functional
- ✅ Sector-specific threat correlation working
- ✅ APT campaign analysis enabled

---

## 9. Validation Metrics

### 9.1 Phase Completion Criteria

| Phase | Success Metric | Target | Current |
|-------|---------------|--------|---------|
| Phase 1 | CVE→Device correlation working | 100% | **0%** ❌ |
| Phase 2 | Network topology queries functional | 100% | **0%** ❌ |
| Phase 3 | Now/Next/Never dashboard operational | 100% | **0%** ❌ |
| Phase 4 | SBOM transitive dependencies tracked | 100% | **0%** ❌ |
| Phase 5 | 8+ hop attack paths generated | 100% | **0%** ❌ |
| Phase 6 | Fleet-wide vulnerability analysis working | 100% | **0%** ❌ |
| Phase 7 | Threat actor correlation functional | 100% | **0%** ❌ |

---

### 9.2 Overall Schema Completeness

| Layer | Nodes | Relationships | Properties | Indexes | Constraints | Completeness |
|-------|-------|---------------|-----------|---------|-------------|--------------|
| Layer 1: Physical Asset | 0/4 | 0/7 | 0/25 | 0/3 | 0/4 | **0%** ❌ |
| Layer 2: Network | 0/4 | 0/5 | 0/20 | 0/2 | 0/4 | **0%** ❌ |
| Layer 3: Software | 1/4 | 0/5 | 3/18 | 0/3 | 1/4 | **17%** ⚠️ |
| Layer 4: Vulnerability | 4/7 | 4/8 | 18/30 | 3/5 | 4/7 | **60%** ⚠️ |
| Layer 5: Attack Surface | 0/3 | 0/6 | 0/15 | 0/2 | 0/3 | **0%** ❌ |
| Layer 6: Organization | 0/3 | 0/3 | 0/12 | 0/2 | 0/3 | **0%** ❌ |
| Layer 7: Failure/Impact | 0/3 | 0/3 | 0/12 | 0/1 | 0/3 | **0%** ❌ |
| Layer 8: Mitigation | 0/2 | 0/4 | 0/15 | 0/2 | 0/2 | **0%** ❌ |
| **TOTAL** | **5/30** | **4/41** | **21/147** | **3/20** | **5/30** | **16.7%** ❌ |

---

## 10. Conclusion

**Current State: 16.7% Schema Implementation**

The Neo4j database currently contains only **threat intelligence data** (CVE, CWE, CAPEC, ATT&CK) with no asset, network, or organizational context. This limits the system to basic vulnerability research queries and prevents:

1. ❌ **Asset-to-vulnerability correlation** (no CPE/Device nodes)
2. ❌ **Network-based risk assessment** (no topology data)
3. ❌ **Attack path analysis** (no reachability modeling)
4. ❌ **Now/Next/Never prioritization** (no scoring algorithm)
5. ❌ **Customer-specific risk assessment** (no namespace isolation)
6. ❌ **SBOM supply chain analysis** (no dependency tracking)
7. ❌ **Fleet-wide vulnerability exposure** (no asset hierarchy)

**Critical Path to Production:**
1. **Weeks 1-2**: Implement CPE/Device correlation (Phase 1)
2. **Weeks 3-4**: Deploy network topology (Phase 2)
3. **Weeks 5-6**: Build Now/Next/Never prioritization (Phase 3)
4. **Weeks 7-8**: Integrate SBOM data (Phase 4)
5. **Weeks 9-10**: Enable attack path analysis (Phase 5)
6. **Weeks 11-12**: Add asset hierarchy (Phase 6)
7. **Weeks 13-14**: Enhance threat intelligence (Phase 7)

**Recommended Immediate Action:**
Start with **Phase 1 (CPE/Device correlation)** as it unblocks all downstream analysis capabilities. Without this foundation, the extensive CVE database cannot be correlated to real-world assets.

---

**Document Version:** v1.0.0
**Last Updated:** 2025-10-29 02:15:00 UTC
**Next Review:** After Phase 1 completion
**Contact:** Code Analyzer Agent
