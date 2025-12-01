# API Gap Closure Roadmap

**File:** 02_API_GAP_CLOSURE_ROADMAP.md
**Created:** 2025-11-29
**Purpose:** Implementation plan to close 10 API documentation gaps for 26 enhancements
**Status:** ACTIVE - IMPLEMENTATION GUIDE

---

## Executive Summary

**Gap Analysis:** 10 of 26 enhancements lack dedicated API documentation
**Impact:** Frontend developers cannot build complete UI for these features
**Solution:** Create 4 new API specification documents + extend 2 existing APIs

### Quick Reference

| Gap | Enhancement | New API File | Priority | Effort |
|-----|-------------|--------------|----------|--------|
| 1 | E3: SBOM Analysis | `API_SBOM.md` | P2 | 2-3 days |
| 2-4 | E7-E9: Safety/RAMS/FMEA | `API_SAFETY_COMPLIANCE.md` | P2 | 4-5 days |
| 5 | E13: Attack Paths | `API_ATTACK_PATHS.md` | P2 | 3-4 days |
| 6 | E16: Protocols | `API_PROTOCOLS.md` | P3 | 2-3 days |
| 7-10 | E14,E17-E19: Lacanian | Extend `E27_PSYCHOHISTORY_API.md` | P3 | 1-2 days |

**Total Effort:** 12-17 days documentation work

---

## Gap 1: SBOM API (Enhancement 3)

### Current Status
- **Enhancement Docs:** `08_Planned_Enhancements/Enhancement_03_SBOM_Analysis/`
- **Wiki API Docs:** ❌ NOT DOCUMENTED
- **Neo4j Schema:** NOT YET IMPLEMENTED (pending enhancement execution)

### Purpose
Enable frontend developers to:
- Upload and parse SBOM files (CycloneDX, SPDX, package.json)
- View package dependency trees
- Query package→CVE relationships
- Generate remediation reports

### Requirements from Enhancement

**Data Model (from E3 README):**
```yaml
Package:
  id: "npm:react:18.2.0"
  name: "react"
  ecosystem: "npm|pypi|maven|nuget"
  version: "18.2.0"
  dependencies: [...]
  vulnerability_context:
    cve_count: N
    severity_distribution: {...}

CVEMapping:
  cve_id: "CVE-2021-43565"
  package_id: "npm:axios:0.21.1"
  cvss_score: 7.5
  epss_score: 0.89
  remediation:
    recommended_version: "0.26.1"
```

### API Specification Required

**File:** `API_SBOM.md`

**Endpoints:**

```yaml
# SBOM Upload & Parse
POST /api/v1/sbom/upload
  Request: multipart/form-data (SBOM file)
  Response: { analysis_id, package_count, vulnerability_summary }

# Package Queries
GET /api/v1/sbom/packages
  Query: ecosystem, name, version_range, has_vulnerabilities
  Response: { packages[], pagination }

GET /api/v1/sbom/packages/:packageId
  Response: { package, dependencies[], vulnerabilities[] }

GET /api/v1/sbom/packages/:packageId/dependencies
  Query: depth (1-10), include_transitive
  Response: { dependency_tree }

GET /api/v1/sbom/packages/:packageId/vulnerabilities
  Response: { cves[], remediation_paths[] }

# Vulnerability Analysis
POST /api/v1/sbom/analyze
  Request: { sbom_content | sbom_url }
  Response: { analysis_id }

GET /api/v1/sbom/analysis/:analysisId
  Response: { status, vulnerability_summary, remediation_roadmap }

# Remediation
GET /api/v1/sbom/remediation/:packageId
  Response: { upgrade_paths[], breaking_changes[], effort_estimate }
```

**Cypher Backend:**
```cypher
// Package with CVE relationships
MATCH (p:Package {id: $package_id})
OPTIONAL MATCH (p)-[:HAS_VULNERABILITY]->(c:CVE)
RETURN p, collect(c) as vulnerabilities

// Dependency tree
MATCH path = (p:Package {id: $package_id})-[:DEPENDS_ON*1..5]->(dep:Package)
RETURN path

// Vulnerable dependencies
MATCH (p:Package {id: $package_id})-[:DEPENDS_ON*1..5]->(dep:Package)-[:HAS_VULNERABILITY]->(c:CVE)
WHERE c.cvss_score >= 7.0
RETURN dep, c
```

### Implementation Steps

1. **Create Neo4j Schema** (from E3 execution)
   - Package nodes with ecosystem, version properties
   - DEPENDS_ON relationships with transitive depth
   - HAS_VULNERABILITY relationships to CVE nodes

2. **Write API_SBOM.md**
   - Full endpoint specification
   - Request/response schemas
   - Error codes
   - Rate limits

3. **Update API_OVERVIEW.md**
   - Add SBOM section to endpoint catalog

---

## Gap 2-4: Safety Compliance APIs (Enhancements 7-9)

### Current Status
- **Enhancement Docs:**
  - `08_Planned_Enhancements/Enhancement_07_IEC62443_Safety/` (1,600+ lines)
  - E8 RAMS: Empty directory
  - E9 FMEA: Empty directory
- **Wiki API Docs:** ❌ NOT DOCUMENTED
- **Neo4j Schema:** NOT YET IMPLEMENTED

### Purpose
Enable frontend developers to:
- Query IEC 62443 security zones and levels (SL1-SL4)
- View equipment compliance status
- Generate compliance gap reports
- Access RAMS reliability metrics
- Query FMEA failure mode analysis

### Requirements from Enhancement 7

**Data Model (from E7 README):**
```yaml
SafetyZone:
  zone_id: "ZONE-001"
  name: "Control System Network"
  security_level_target: 3  # SL-T
  security_level_achieved: 2  # SL-A
  security_level_gap: 1
  criticality: "HIGH"
  asset_count: 156

FoundationalRequirement:
  requirement_id: "FR1-FR7"
  name: "Identification and Authentication Control"
  security_level: 3
  compliance_percentage: 66.7

Conduit:
  conduit_id: "CONDUIT-A12"
  protocol: "Modbus TCP"
  encryption: true/false
  security_level: 1-4
```

### API Specification Required

**File:** `API_SAFETY_COMPLIANCE.md`

**Endpoints:**

```yaml
# IEC 62443 Zones
GET /api/v1/safety/zones
  Query: security_level, compliance_status, criticality
  Response: { zones[], summary }

GET /api/v1/safety/zones/:zoneId
  Response: { zone, equipment[], conduits[], compliance }

GET /api/v1/safety/zones/:zoneId/gap-analysis
  Response: { sl_target, sl_achieved, gap, remediation_cost, roi }

# Foundational Requirements
GET /api/v1/safety/requirements
  Response: { fr1-fr7 with compliance status }

GET /api/v1/safety/requirements/:frId/controls
  Query: security_level (1-4)
  Response: { controls[], implementation_status[] }

# Conduits
GET /api/v1/safety/conduits
  Query: zone_id, protocol, encryption_status
  Response: { conduits[] }

GET /api/v1/safety/conduits/:conduitId/vulnerabilities
  Response: { vulnerabilities[], risk_score }

# Equipment Compliance
GET /api/v1/safety/equipment/:equipmentId/compliance
  Response: { iec62443_certified, component_security_level, certification_details }

# RAMS (E8)
GET /api/v1/rams/equipment/:equipmentId
  Response: { mtbf, mttr, availability, sil_rating }

GET /api/v1/rams/sector/:sectorId/reliability
  Response: { sector_reliability, weakest_links[], prediction }

POST /api/v1/rams/predict-failure
  Request: { equipment_ids[], time_horizon }
  Response: { failure_probabilities[], maintenance_schedule }

# FMEA (E9)
GET /api/v1/fmea/equipment/:equipmentId/failure-modes
  Response: { failure_modes[], rpn_scores }

GET /api/v1/fmea/sector/:sectorId/critical-failures
  Query: rpn_threshold (default: 100)
  Response: { critical_failures[], mitigation_options }

POST /api/v1/fmea/analyze
  Request: { equipment_id, cyber_attack_scenario }
  Response: { cyber_induced_failures[], cascade_risk }
```

**Cypher Backend:**
```cypher
// Zone with compliance status
MATCH (zone:SafetyZone {zone_id: $zone_id})
OPTIONAL MATCH (zone)-[:CONTAINS]->(e:Equipment)
OPTIONAL MATCH (zone)-[:IMPLEMENTS]->(fr:FoundationalRequirement)
RETURN zone, count(e) as assets, collect(fr) as requirements

// Security level gap analysis
MATCH (zone:SafetyZone)
WHERE zone.security_level_gap > 0
RETURN zone.name, zone.security_level_target,
       zone.security_level_achieved, zone.security_level_gap

// Equipment certification status
MATCH (e:Equipment {id: $equipment_id})
RETURN e.iec62443_certified, e.component_security_level,
       e.certification_body, e.certificate_expiry
```

### Implementation Steps

1. **Create Neo4j Schema** (from E7 execution)
   - SafetyZone nodes with SL properties
   - FoundationalRequirement nodes (FR1-FR7)
   - Conduit relationships with security properties
   - RAMS/FMEA properties on Equipment nodes

2. **Write API_SAFETY_COMPLIANCE.md**
   - IEC 62443 zone endpoints
   - RAMS reliability endpoints
   - FMEA failure mode endpoints
   - Compliance reporting endpoints

3. **Update API_OVERVIEW.md**
   - Add Safety/Compliance section

---

## Gap 5: Attack Paths API (Enhancement 13)

### Current Status
- **Enhancement Docs:** `Enhancement_13_Attack_Path_Modeling/` - Empty
- **Wiki API Docs:** ❌ NOT DOCUMENTED
- **Neo4j Schema:** Partial (CVE→CWE→CAPEC→Technique chains exist)

### Purpose
Enable frontend developers to:
- Enumerate attack paths from source to target
- Calculate path probabilities
- Visualize attack chains
- Identify mitigation points with ROI

### Requirements (from Master Catalog)

**Capability:** 20-hop attack path enumeration
**Data:** Existing 316K CVEs, 691 MITRE techniques, 48K equipment
**Output:** Complete attack chains (CVE → Technique → Equipment → Sector → Impact)

### API Specification Required

**File:** `API_ATTACK_PATHS.md`

**Endpoints:**

```yaml
# Path Discovery
GET /api/v1/attack-paths/from/:sourceId/to/:targetId
  Query: max_hops (1-20), path_type (shortest|all|critical)
  Response: { paths[], probability_distribution }

POST /api/v1/attack-paths/enumerate
  Request: {
    source: "CVE-2024-1234" | "external_network",
    target: "equipment:PLC-001" | "sector:energy",
    constraints: { max_hops, required_techniques[], blocked_vectors[] }
  }
  Response: { paths[], analysis_id }

GET /api/v1/attack-paths/:pathId
  Response: { nodes[], edges[], probability, techniques_used }

# Path Analysis
GET /api/v1/attack-paths/:pathId/probability
  Response: { total_probability, edge_probabilities[], confidence_interval }

GET /api/v1/attack-paths/:pathId/mitigations
  Response: { mitigation_points[], roi_analysis[], recommended_actions }

# Bulk Analysis
POST /api/v1/attack-paths/sector/:sectorId/analyze
  Request: { threat_actors[], time_horizon }
  Response: { critical_paths[], risk_summary, investment_recommendations }

# Visualization
GET /api/v1/attack-paths/:pathId/graph
  Query: format (d3|cytoscape|graphviz)
  Response: { nodes[], edges[], layout_hints }
```

**Cypher Backend:**
```cypher
// Find attack paths from CVE to sector
MATCH path = (c:CVE {id: $cve_id})-[:EXPLOITED_BY]->(cwe:CWE)
              -[:ENABLES]->(capec:CAPEC)-[:USES]->(t:ATT_CK_Technique)
              -[:TARGETS]->(e:Equipment)-[:LOCATED_IN]->(s:Sector {id: $sector_id})
RETURN path, length(path) as hops
ORDER BY hops ASC
LIMIT 10

// Calculate path probability
MATCH path = (start)-[rels*1..10]->(end)
WITH path, reduce(prob = 1.0, r in rels | prob * r.probability) as total_prob
RETURN path, total_prob
ORDER BY total_prob DESC

// Find mitigation points
MATCH path = (c:CVE)-[*1..10]->(target:Equipment)
WITH path, nodes(path) as path_nodes
UNWIND path_nodes as node
MATCH (node)-[:MITIGATED_BY]->(m:Mitigation)
RETURN node, m, m.effectiveness, m.cost
```

### Implementation Steps

1. **Verify Neo4j Schema**
   - Ensure CVE→CWE→CAPEC→Technique→Equipment chain exists
   - Add probability properties to relationships
   - Add Mitigation nodes with ROI properties

2. **Write API_ATTACK_PATHS.md**
   - Path enumeration endpoints
   - Probability calculation endpoints
   - Visualization data endpoints

3. **Update API_OVERVIEW.md**
   - Add Attack Path section

---

## Gap 6: Protocols API (Enhancement 16)

### Current Status
- **Enhancement Docs:** `Enhancement_16_Protocol_Analysis/` - Empty
- **Wiki API Docs:** ❌ NOT DOCUMENTED
- **Neo4j Schema:** NOT YET IMPLEMENTED

### Purpose
Enable frontend developers to:
- Query industrial protocol information (Modbus, DNP3, OPC UA, etc.)
- View protocol-specific vulnerabilities
- Map protocols to equipment
- Access protocol security recommendations

### Requirements (from Master Catalog)

**Data:** Protocol_Training_Data/ (11 protocols: Modbus, DNP3, OPC UA, ETCS, etc.)
**Output:** Protocol vulnerability catalog, 92+ tracked vulnerabilities

### API Specification Required

**File:** `API_PROTOCOLS.md`

**Endpoints:**

```yaml
# Protocol Catalog
GET /api/v1/protocols
  Query: category (industrial|network|safety), security_level
  Response: { protocols[] }

GET /api/v1/protocols/:protocolId
  Response: { protocol_details, security_properties, common_misconfigurations }

# Protocol Vulnerabilities
GET /api/v1/protocols/:protocolId/vulnerabilities
  Query: severity, exploited_in_wild
  Response: { cves[], attack_patterns[] }

GET /api/v1/protocols/:protocolId/attack-vectors
  Response: { vectors[], mitre_techniques[], detection_methods }

# Equipment Mapping
GET /api/v1/protocols/:protocolId/equipment
  Query: sector, manufacturer
  Response: { equipment[], deployment_count }

GET /api/v1/equipment/:equipmentId/protocols
  Response: { protocols[], security_configurations[] }

# Security Analysis
POST /api/v1/protocols/analyze
  Request: { protocol_id, deployment_context, network_topology }
  Response: { risk_score, recommendations[], hardening_guide }

GET /api/v1/protocols/:protocolId/hardening
  Response: { hardening_steps[], configuration_templates }
```

**Protocols to Document:**

| Protocol | Category | CVE Count | Risk Level |
|----------|----------|-----------|------------|
| Modbus TCP/RTU | Industrial | 45+ | HIGH |
| DNP3 | Industrial | 23+ | HIGH |
| OPC UA | Industrial | 12+ | MEDIUM |
| PROFINET | Industrial | 8+ | MEDIUM |
| EtherNet/IP | Industrial | 15+ | HIGH |
| BACnet | Building | 6+ | MEDIUM |
| ETCS | Railway | 4+ | CRITICAL |
| ADS-B | Aviation | 3+ | CRITICAL |
| Modbus Serial | Industrial | 10+ | HIGH |
| HART | Process | 5+ | MEDIUM |
| Profibus | Industrial | 7+ | MEDIUM |

### Implementation Steps

1. **Create Neo4j Schema**
   - Protocol nodes with security properties
   - USES_PROTOCOL relationships to Equipment
   - Protocol→CVE vulnerability mappings

2. **Write API_PROTOCOLS.md**
   - Protocol catalog endpoints
   - Vulnerability query endpoints
   - Equipment mapping endpoints

3. **Update API_OVERVIEW.md**
   - Add Protocols section

---

## Gaps 7-10: Extended Psychohistory APIs (E14, E17-E19)

### Current Status
- **Enhancement Docs:** All documented in `08_Planned_Enhancements/`
- **Wiki API Docs:** Partially covered by `E27_PSYCHOHISTORY_API.md`
- **Neo4j Schema:** E27 implementation covers base structure

### Purpose
Extend existing Psychohistory API to cover:
- E14: Lacanian Real vs Imaginary threat analysis
- E17: Lacanian Dyad analysis
- E18: Triad group dynamics
- E19: Organizational blind spot detection

### API Extensions Required

**File:** Extend `E27_PSYCHOHISTORY_API.md`

**Additional Endpoints:**

```yaml
# E14: Lacanian Real/Imaginary
POST /api/v1/psychohistory/lacanian/real-imaginary
  Request: { threat_id, perception_data }
  Response: { real_score, imaginary_score, symbolic_gap, misallocation_cost }

GET /api/v1/psychohistory/lacanian/fear-reality-gap/:sectorId
  Response: { threats[], perceived_vs_actual[], investment_recommendations }

# E17: Dyad Analysis
POST /api/v1/psychohistory/lacanian/dyad
  Request: { entity_a, entity_b, relationship_type }
  Response: { dyad_dynamics, power_balance, vulnerability_vectors }

# E18: Triad Dynamics
POST /api/v1/psychohistory/triad
  Request: { entities[3], context }
  Response: { coalition_stability, betrayal_risk, mediation_points }

# E19: Blind Spot Detection
GET /api/v1/psychohistory/blind-spots/:organizationId
  Response: { blind_spots[], unconscious_biases[], remediation_steps }

POST /api/v1/psychohistory/blind-spots/scan
  Request: { organization_context, decision_history }
  Response: { detected_blind_spots[], confidence_scores }
```

### Implementation Steps

1. **Review E27 Schema**
   - Verify Lacanian entity support
   - Add dyad/triad relationship types
   - Add blind spot detection properties

2. **Extend E27_PSYCHOHISTORY_API.md**
   - Add Lacanian section
   - Add Dyad/Triad section
   - Add Blind Spot section

3. **Update API_OVERVIEW.md**
   - Update Psychohistory section

---

## Implementation Roadmap

### Phase 1: Critical Path (Week 1-2)

| Day | Task | Output |
|-----|------|--------|
| 1-2 | Create API_SBOM.md | SBOM API specification |
| 3-5 | Create API_SAFETY_COMPLIANCE.md | IEC62443/RAMS/FMEA API spec |
| 6-7 | Update API_OVERVIEW.md | Integrated catalog |

### Phase 2: Attack Analysis (Week 2-3)

| Day | Task | Output |
|-----|------|--------|
| 8-10 | Create API_ATTACK_PATHS.md | Attack path API spec |
| 11-12 | Create API_PROTOCOLS.md | Protocol API spec |
| 13-14 | Update API_OVERVIEW.md | Complete catalog |

### Phase 3: Extended Coverage (Week 3-4)

| Day | Task | Output |
|-----|------|--------|
| 15-16 | Extend E27_PSYCHOHISTORY_API.md | Lacanian/Dyad/Triad endpoints |
| 17 | Final review and cross-references | Validated documentation |

---

## Verification Checklist

### Per API File

- [ ] All endpoints documented with request/response schemas
- [ ] Error codes specified (400, 401, 403, 404, 429, 500)
- [ ] Rate limits defined
- [ ] Authentication requirements stated
- [ ] Cypher query examples provided
- [ ] TypeScript interfaces generated
- [ ] OpenAPI 3.0 schema included

### Cross-References

- [ ] API_OVERVIEW.md updated with new endpoints
- [ ] 01_API_ENHANCEMENT_COVERAGE_MATRIX.md updated
- [ ] 00_API_STATUS_AND_ROADMAP.md updated
- [ ] Related database docs reference APIs

### Frontend Developer Validation

- [ ] Mock data examples for each endpoint
- [ ] UI component mapping documented
- [ ] Integration patterns provided
- [ ] Testing scenarios specified

---

## Success Criteria

**Gap Closure Complete When:**

1. All 26 enhancements have documented API access
2. Frontend developers can design UI for all features
3. Mock data available for parallel development
4. API_OVERVIEW.md has complete 50+ endpoint catalog
5. All APIs follow consistent patterns (auth, pagination, errors)

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Enhancement schemas not finalized | API specs may change | Document as "PLANNED" with version control |
| Neo4j schema changes | API queries break | Use abstraction layer, version endpoints |
| Feature scope creep | Documentation delays | Strict MVP scope per API |
| Frontend-backend sync | Integration issues | Share OpenAPI specs early |

---

**RECORD OF NOTE:** This roadmap ensures systematic closure of all API gaps before API layer implementation begins.
