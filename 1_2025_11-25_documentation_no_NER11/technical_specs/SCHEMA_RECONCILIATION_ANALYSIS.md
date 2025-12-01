# SCHEMA RECONCILIATION ANALYSIS - AEON Cyber Digital Twin

**Generated**: 2025-11-26
**Purpose**: Compare ACTUAL Neo4j schema with documented TARGET schema
**Data Source**: `active_neo4j_data` Docker volume (1.8GB)

---

## EXECUTIVE SUMMARY

| Dimension | Actual (active_neo4j_data) | Target (00_constraints_indexes.cypher) | Gap |
|-----------|---------------------------|----------------------------------------|-----|
| **Total Nodes** | 1,618,130 | 1,107,664 | +46% (exceeded) |
| **Total Relationships** | 15,599,563 | 3,322,992 | +369% (exceeded) |
| **Node Labels** | 25 | 35+ | -29% (some missing) |
| **Relationship Types** | 3 | 30+ | -90% (critical gap) |

**Bottom Line**: The database has MORE raw data than target but LESS structural richness. CVE-CPE linkage is excellent; CVE-CWE-CAPEC chain is broken.

---

## PART 1: NODE LABEL COMPARISON

### 1.1 Labels Present in BOTH (Actual ✅ Target)

| Label | Actual Count | Target Requirement | Status |
|-------|--------------|-------------------|--------|
| **CVE** | 307,322 | 267,487 | ✅ EXCEEDS (+15%) |
| **CAPEC** | 706 | Required | ✅ PRESENT |
| **CWE** | 10 | Required | ⚠️ MINIMAL |
| **ThreatActor** | 4 (sample) | Required | ⚠️ MINIMAL |
| **Organization** | 11 | 5,000 | ❌ DEFICIT |
| **Location** | 15 | 15,000 | ❌ DEFICIT |
| **Equipment** | 10 | Required | ⚠️ MINIMAL |
| **Document** | 4 | Required | ⚠️ MINIMAL |

### 1.2 Labels in ACTUAL Only (Not in Target Schema)

| Label | Actual Count | Purpose | Recommendation |
|-------|--------------|---------|----------------|
| **CPE** | 1,309,730 | Common Platform Enumeration | ✅ KEEP - Essential for CVE→Software mapping |
| **AttackTechnique** | - | MITRE ATT&CK | ✅ KEEP - Rename to `Technique` for consistency |
| **Software** (MITRE) | 760 | MITRE software catalog | ✅ KEEP - Merge into Layer 3 Software |
| **Mitigation** | 285 | MITRE mitigations | ✅ KEEP - Maps to Layer 8 |
| **ThreatReport** | 276 | Threat intelligence | ✅ KEEP - Valuable context |
| **Cybersecurity** | 29 | Domain concepts | EVALUATE - May be redundant |
| **TechnicalSpec** | 8 | Specifications | ✅ KEEP |
| **CIM_Root/SAREF_Root/GRID2ONTO_Root** | 2 each | Ontology roots | ✅ KEEP - Ontology integration |
| **CAPEC_Category/CAPEC_View** | - | CAPEC taxonomy | ✅ KEEP |

### 1.3 Labels MISSING from Actual (In Target, Not in DB)

| Missing Label | Target Layer | Priority | Data Source |
|---------------|--------------|----------|-------------|
| **Device** | Layer 1 - Physical | CRITICAL | Customer SBOM/Asset Inventory |
| **HardwareComponent** | Layer 1 | HIGH | Equipment Catalog |
| **PhysicalAsset** | Layer 1 | HIGH | ICS-CERT |
| **NetworkInterface** | Layer 2 | HIGH | Network Scans |
| **Network** | Layer 2 | MEDIUM | Architecture Diagrams |
| **SecurityZone** | Layer 2 | MEDIUM | IEC 62443 Zones |
| **Conduit** | Layer 2 | MEDIUM | IEC 62443 Conduits |
| **Software** (Layer 3) | Layer 3 | CRITICAL | SBOM Data |
| **SoftwareComponent** | Layer 3 | HIGH | SBOM Dependencies |
| **Application** | Layer 3 | HIGH | Application Inventory |
| **Firmware** | Layer 3 | HIGH | Device Firmware |
| **Technique** | Layer 4 | PRESENT (as AttackTechnique) | MITRE ATT&CK |
| **Exploit** | Layer 4 | MEDIUM | Exploit-DB/Metasploit |
| **ThreatActorProfile** | Layer 4 | HIGH | E25 Enhancement |
| **AttackSurface** | Layer 5 | HIGH | Assessment Results |
| **AttackPath** | Layer 5 | HIGH | Graph Analysis |
| **AttackPathStep** | Layer 5 | MEDIUM | Path Decomposition |
| **BusinessProcess** | Layer 6 | MEDIUM | Business Analysis |
| **Compliance** | Layer 6 | MEDIUM | NERC CIP Mapping |
| **FailureMode** | Layer 7 | MEDIUM | FMEA Analysis |
| **FailureScenario** | Layer 7 | MEDIUM | Simulation |
| **Impact** | Layer 7 | HIGH | Risk Assessment |
| **Mitigation** (Layer 8) | Layer 8 | PRESENT | MITRE Data |
| **Priority** | Layer 8 | MEDIUM | NOW/NEXT/NEVER |

---

## PART 2: RELATIONSHIP TYPE COMPARISON

### 2.1 Relationships in ACTUAL Database

| Type | Count | Pattern | Assessment |
|------|-------|---------|------------|
| **MATCHES** | 15,599,445 | (CVE)-[:MATCHES]->(CPE) | ✅ EXCELLENT - Core vulnerability mapping |
| **MENTIONED_IN** | 106 | Entity→Document | ✅ PRESENT - Needs expansion |
| **RELATIONSHIP** | 12 | Generic | ⚠️ REVIEW - Should be typed |

### 2.2 Relationships MISSING (Critical for 8-Hop Queries)

| Missing Relationship | Pattern | Priority | Data Source |
|---------------------|---------|----------|-------------|
| **IS_WEAKNESS_TYPE** | (CVE)-[:IS_WEAKNESS_TYPE]->(CWE) | 🔴 CRITICAL | NVD API |
| **ENABLES_ATTACK_PATTERN** | (CVE)-[:ENABLES_ATTACK_PATTERN]->(CAPEC) | 🔴 CRITICAL | CAPEC Database |
| **EXPLOITS_WEAKNESS** | (CAPEC)-[:EXPLOITS_WEAKNESS]->(CWE) | 🔴 CRITICAL | CAPEC Database |
| **MAPS_TO_TECHNIQUE** | (CAPEC)-[:MAPS_TO_TECHNIQUE]->(Technique) | 🔴 CRITICAL | CAPEC-ATT&CK Mapping |
| **HAS_EXPLOIT** | (CVE)-[:HAS_EXPLOIT]->(Exploit) | HIGH | Exploit-DB |
| **USED_BY_THREAT_ACTOR** | (Exploit)-[:USED_BY_THREAT_ACTOR]->(ThreatActor) | HIGH | Threat Intel |
| **USES_TTP** | (ThreatActor)-[:USES_TTP]->(Technique) | HIGH | MITRE ATT&CK |
| **HAS_PROFILE** | (ThreatActor)-[:HAS_PROFILE]->(ThreatActorProfile) | MEDIUM | E25 Enhancement |
| **HAS_VULNERABILITY** | (Software)-[:HAS_VULNERABILITY]->(CVE) | 🔴 CRITICAL | CVE-CPE Transform |
| **RUNS_ON** | (Software)-[:RUNS_ON]->(Device) | HIGH | SBOM |
| **LOCATED_IN** | (Device)-[:LOCATED_IN]->(SecurityZone) | HIGH | IEC 62443 |
| **CONNECTS_TO** | (Device)-[:CONNECTS_TO]->(NetworkInterface) | HIGH | Network Scan |
| **CAN_REACH** | (AttackPath)-[:CAN_REACH]->(Device) | MEDIUM | Graph Analysis |
| **MITIGATES** | (Mitigation)-[:MITIGATES]->(CVE) | HIGH | MITRE Data |
| **OPERATED_BY** | (Device)-[:OPERATED_BY]->(Organization) | MEDIUM | Asset Registry |

---

## PART 3: PROPERTY SCHEMA COMPARISON

### 3.1 CVE Properties

| Property | Actual Name | Target Name | Status |
|----------|-------------|-------------|--------|
| Unique ID | `cve_id` | `cveId` | ⚠️ NAME MISMATCH |
| Description | `descriptions` (List) | `description` (String) | ⚠️ TYPE MISMATCH |
| Published Date | `date_published` | `publishedDate` | ⚠️ NAME MISMATCH |
| CVSS Score | `base_score` | `cvssV3BaseScore` | ⚠️ NAME MISMATCH |
| Severity | `severity` | `cvssV3Severity` | ✅ ALIGNED |
| Vector String | `vector_string` | `cvssV3Vector` | ⚠️ NAME MISMATCH |
| Exploitability | NOT PRESENT | `exploitabilityScore` | ❌ MISSING |
| Impact Score | NOT PRESENT | `impactScore` | ❌ MISSING |
| Has Exploit | NOT PRESENT | `hasExploit` | ❌ MISSING |
| Exploit Maturity | NOT PRESENT | `exploitMaturity` | ❌ MISSING |
| Is Shared | NOT PRESENT | `is_shared` | ❌ MISSING |
| Customer Namespace | NOT PRESENT | `customer_namespace` | ❌ MISSING |

### 3.2 CVE Severity Distribution Analysis

**Actual Data Quality Issue**:
| Severity | Count | Percentage |
|----------|-------|------------|
| (empty/unknown) | 215,780 | 70.2% |
| MEDIUM | 44,812 | 14.6% |
| HIGH | 33,813 | 11.0% |
| CRITICAL | 6,879 | 2.2% |
| LOW | 6,019 | 2.0% |
| NONE | 19 | <0.1% |

**Root Cause**: Older CVEs lack CVSS v3.1 scores (pre-2015)
**Resolution**: NVD API enrichment for 215,780 CVEs

---

## PART 4: 8-LAYER ARCHITECTURE ALIGNMENT

### Current State vs Target Architecture

| Layer | Target Requirement | Actual Implementation | Gap % |
|-------|-------------------|----------------------|-------|
| **L0: Equipment Catalog** | 48,288 nodes | ~10 Equipment nodes | 99.9% GAP |
| **L1: Customer Equipment** | 289,728 nodes | 0 Device nodes | 100% GAP |
| **L2: Network & Communication** | Required | 0 Network nodes | 100% GAP |
| **L3: Software & Application** | Required | 1,309,730 CPE | ✅ EXCEEDED (raw data) |
| **L4: Vulnerability & Threat** | 318,592 nodes | 307,322 CVE + 706 CAPEC + 10 CWE | ✅ 97% PRESENT |
| **L5: Attack Surface** | Required | 0 AttackSurface nodes | 100% GAP |
| **L6: Organizational** | 5,000 org | 11 Organization | 99.8% GAP |
| **L7: Failure Propagation** | Required | 0 nodes | 100% GAP |
| **L8: Mitigation** | Required | 285 Mitigation (MITRE) | ⚠️ PARTIAL |

### Critical Finding

**The 8-hop query chain is BROKEN:**

```
Target Chain (8 hops):
Software → CVE → CWE → CAPEC → Technique → ThreatActor → Campaign → Profile

Actual Chain (2 hops max):
CVE → CPE (via MATCHES)
```

**Missing Links:**
1. CVE → CWE (0 relationships exist)
2. CVE → CAPEC (0 relationships exist)
3. CAPEC → Technique (0 relationships exist)
4. ThreatActor → Technique (0 relationships exist)

---

## PART 5: RECONCILIATION PLAN

### Phase 1: Data Quality (Week 1)
1. **CVE Property Alignment**
   - Rename properties to match target schema
   - Add missing properties (exploitabilityScore, impactScore, hasExploit)
   - Set `customer_namespace = "shared:nvd"` for all CVEs

2. **CVE Severity Enrichment**
   - Use NVD API to fetch CVSS v3.1 for 215,780 CVEs missing severity
   - Batch process 1,000 CVEs/hour (API rate limits)

### Phase 2: Relationship Building (Week 2-3)
1. **CVE → CWE Relationships**
   - Source: NVD API `weaknesses` field
   - Create `IS_WEAKNESS_TYPE` relationships
   - Expected: ~200,000+ relationships

2. **CWE → CAPEC Relationships**
   - Source: CAPEC XML download
   - Create `EXPLOITS_WEAKNESS` relationships
   - Expected: ~3,000+ relationships

3. **CAPEC → Technique Relationships**
   - Source: CAPEC XML + ATT&CK STIX
   - Create `MAPS_TO_TECHNIQUE` relationships
   - Expected: ~1,500+ relationships

### Phase 3: Attack Chain Completion (Week 4)
1. **ThreatActor → Technique**
   - Source: MITRE ATT&CK Groups STIX
   - Create `USES_TTP` relationships
   - Expand from 4 ThreatActors to 187 (already have from MITRE load)

2. **Software → CVE**
   - Transform MATCHES relationships
   - Create `HAS_VULNERABILITY` with affected_versions
   - Derive from existing CPE data

### Phase 4: Layer Population (Week 5-8)
1. **Layer 0-1: Equipment**
   - Await customer asset data or ICS-CERT catalog
   - Schema ready, data source needed

2. **Layer 5: Attack Surface**
   - Run graph analysis algorithms
   - Generate AttackPath from CVE→CPE→Software chains

3. **Layer 7: Failure Propagation**
   - Requires equipment dependencies
   - Blocked until Layer 0-1 populated

---

## PART 6: ETL AGENT REQUIREMENTS

### Agent Architecture for Data Reconciliation

Based on the gap analysis, the ETL pipeline requires these specialized agents:

#### Agent 1: CVE Enrichment Agent
- **Input**: CVE nodes from database
- **Process**: Query NVD API, extract CVSS, CWE mappings
- **Output**: Updated CVE properties, CWE relationships
- **Rate**: 1,000 CVEs/hour (API limit)

#### Agent 2: CWE-CAPEC Linker Agent
- **Input**: CWE nodes, CAPEC XML
- **Process**: Parse CAPEC related_weaknesses, create relationships
- **Output**: EXPLOITS_WEAKNESS relationships
- **Expected**: ~3,000 relationships

#### Agent 3: CAPEC-ATT&CK Mapper Agent
- **Input**: CAPEC nodes, ATT&CK STIX bundle
- **Process**: Map CAPEC attack patterns to techniques
- **Output**: MAPS_TO_TECHNIQUE relationships
- **Expected**: ~1,500 relationships

#### Agent 4: Threat Actor Enrichment Agent
- **Input**: ThreatActor nodes, MITRE Groups STIX
- **Process**: Expand actor profiles, add techniques
- **Output**: Enhanced ThreatActor nodes, USES_TTP relationships
- **Expected**: 187 actors, ~2,000 relationships

#### Agent 5: Schema Migration Agent
- **Input**: Current property names
- **Process**: Rename properties to match target schema
- **Output**: Standardized property names
- **Scope**: 307,322 CVE nodes

#### Agent 6: Attack Chain Builder Agent
- **Input**: All relationship types
- **Process**: Build 8-hop traversal paths
- **Output**: AttackPath nodes, validation reports
- **Validation**: Test McKenney Q1-Q8 queries

---

## PART 7: VALIDATION QUERIES

### Pre-Reconciliation Test (Current State)

```cypher
// This query should return 0 results currently
MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
RETURN count(*) AS cve_cwe_count;
// Expected: 0 (broken chain)

// This query works (our strongest relationship)
MATCH (cve:CVE)-[:MATCHES]->(cpe:CPE)
RETURN count(*) AS cve_cpe_count;
// Expected: 15,599,445
```

### Post-Reconciliation Test (Target State)

```cypher
// 8-hop attack chain query
MATCH path = (s:Software)-[:HAS_VULNERABILITY]->(cve:CVE)
              -[:IS_WEAKNESS_TYPE]->(cwe:CWE)
              <-[:EXPLOITS_WEAKNESS]-(capec:CAPEC)
              -[:MAPS_TO_TECHNIQUE]->(tech:Technique)
              <-[:USES_TTP]-(ta:ThreatActor)
              -[:HAS_PROFILE]->(profile:ThreatActorProfile)
WHERE cve.cvssV3BaseScore >= 9.0
RETURN count(path) AS attack_chains;
// Expected: 1000+ complete chains
```

---

## APPENDIX: DATA SOURCES FOR GAP FILLING

| Gap | Data Source | URL/Access | Format |
|-----|-------------|------------|--------|
| CVE→CWE | NVD API 2.0 | https://nvd.nist.gov/developers/vulnerabilities | JSON |
| CWE→CAPEC | CAPEC Downloads | https://capec.mitre.org/data/xml/capec_latest.xml | XML |
| CAPEC→Technique | CAPEC XML | Same as above | XML |
| ThreatActor→Technique | ATT&CK STIX | https://github.com/mitre/cti | JSON |
| Equipment Catalog | ICS-CERT | Customer-specific | Varies |
| SBOM Data | Customer | Customer-specific | SPDX/CycloneDX |

---

**Document Version**: 1.0
**Generated By**: Schema Reconciliation Analysis Agent
**Date**: 2025-11-26
