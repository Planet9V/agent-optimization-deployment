# API Enhancement Coverage Matrix

**File:** 01_API_ENHANCEMENT_COVERAGE_MATRIX.md
**Created:** 2025-11-29
**Updated:** 2025-11-30
**Purpose:** Map all 26 enhancements to required APIs for frontend developer access
**Status:** AUTHORITATIVE REFERENCE - ALL GAPS CLOSED

---

## Executive Summary

**Source:** `4_AEON_DT_CyberDTc3_2025_11_25` (26 Enhancements)
**Target:** `1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs` (27 API files)

### Coverage Status

| Category | Total | Documented | Gap |
|----------|-------|------------|-----|
| Enhancements | 26 | **26** | **0** |
| API Files | 27 | 27 | **0** |
| Database APIs | 4 | **4** | **0** |

### Gap Closure Summary (2025-11-30)

| Gap ID | API Created | Enhancements Covered | Status |
|--------|-------------|---------------------|--------|
| GAP-001 | `Neo4j-Graph-Database.md` | All (Primary DB) | ✅ CLOSED |
| GAP-002 | `API_SBOM.md` | E3 | ✅ CLOSED |
| GAP-003 | `API_SAFETY_COMPLIANCE.md` | E7, E8, E9 | ✅ CLOSED |
| GAP-004 | `API_ATTACK_PATHS.md` | E13 | ✅ CLOSED |
| GAP-005 | `API_PROTOCOLS.md` | E16 | ✅ CLOSED |
| GAP-006 | `E27_PSYCHOHISTORY_API.md` (Extended) | E14, E17, E18, E19 | ✅ CLOSED |

---

## Enhancement → API Mapping

### CATEGORY A: THREAT INTELLIGENCE (E1-E2)

| Enhancement | Required API | Status | Wiki File |
|-------------|--------------|--------|-----------|
| **E1: APT Threat Intel** | STIX API, Threat Actor Endpoints | ✅ COVERED | `API_STIX.md` |
| **E2: STIX 2.1 Integration** | STIX API | ✅ COVERED | `API_STIX.md` |

**Frontend Access:**
```javascript
// APT Threat Actors
GET /api/v1/stix/threat-actors
GET /api/v1/stix/indicators
GET /api/v1/stix/campaigns

// IoC Queries
POST /api/v1/stix/query
```

---

### CATEGORY B: SUPPLY CHAIN (E3)

| Enhancement | Required API | Status | Wiki File |
|-------------|--------------|--------|-----------|
| **E3: SBOM Analysis** | SBOM API | ✅ COVERED | `API_SBOM.md` |

**Frontend Access:**
```javascript
// SBOM Upload & Analysis
POST /api/v1/sbom/upload
GET /api/v1/sbom/packages/{packageId}
GET /api/v1/sbom/packages/{packageId}/vulnerabilities
GET /api/v1/sbom/packages/{packageId}/dependencies
POST /api/v1/sbom/analyze
GET /api/v1/sbom/risk/{applicationId}
GET /api/v1/sbom/license-compliance/{applicationId}
```

---

### CATEGORY C: PSYCHOLOGY & BEHAVIOR (E4, E11, E14, E17-E26)

| Enhancement | Required API | Status | Wiki File |
|-------------|--------------|--------|-----------|
| **E4: Psychometric Integration** | Psychohistory API | ✅ COVERED | `E27_PSYCHOHISTORY_API.md` |
| **E11: Psychohistory Demographics** | Psychohistory API | ✅ COVERED | `E27_PSYCHOHISTORY_API.md` |
| **E14: Lacanian Real/Imaginary** | Psychohistory API | ✅ COVERED | `E27_PSYCHOHISTORY_API.md` (§15) |
| **E17: Lacanian Dyad Analysis** | Psychohistory API | ✅ COVERED | `E27_PSYCHOHISTORY_API.md` (§16) |
| **E18: Triad Group Dynamics** | Psychohistory API | ✅ COVERED | `E27_PSYCHOHISTORY_API.md` (§17) |
| **E19: Organizational Blind Spots** | Psychohistory API | ✅ COVERED | `E27_PSYCHOHISTORY_API.md` (§18) |
| **E20: Personality Team Fit** | Psychohistory API | ✅ COVERED | `E27_PSYCHOHISTORY_API.md` |
| **E21: Transcript Psychometric NER** | Psychohistory API | ✅ COVERED | `E27_PSYCHOHISTORY_API.md` |
| **E22: Seldon Crisis Prediction** | Psychohistory API | ✅ COVERED | `E27_PSYCHOHISTORY_API.md` |
| **E23: Population Event Forecasting** | Psychohistory API | ✅ COVERED | `E27_PSYCHOHISTORY_API.md` |
| **E24: Cognitive Dissonance Breaking** | Psychohistory API | ✅ COVERED | `E27_PSYCHOHISTORY_API.md` |
| **E25: Threat Actor Personality** | Psychohistory API | ✅ COVERED | `E27_PSYCHOHISTORY_API.md` |
| **E26: McKenney-Lacan Calculus** | Psychohistory API | ✅ COVERED | `E27_PSYCHOHISTORY_API.md` |

**Frontend Access (Psychohistory Core):**
```javascript
// Seldon Crisis & Predictions
POST /api/v1/predict/seldon-crisis
POST /api/v1/predict/epidemic
POST /api/v1/predict/cascade
POST /api/v1/predict/critical-slowing

// McKenney Questions
GET /api/v1/mckenney/q1-who-threatens
GET /api/v1/mckenney/q6-impact
GET /api/v1/mckenney/q7-future-threats
GET /api/v1/mckenney/q8-patch-priority

// Entity Psychometrics
GET /api/v1/entities/psychtraits
GET /api/v1/entities/economic-metrics
```

**Frontend Access (Lacanian Extensions v1.1.0):**
```javascript
// E14: Real-Imaginary-Symbolic Analysis
POST /api/v1/predict/lacanian-real-imaginary

// E17: Dyad Dynamics (attacker-defender, vendor-customer)
POST /api/v1/predict/dyad-dynamics

// E18: Triad Dynamics (vendor-client-regulator)
POST /api/v1/predict/triad-dynamics

// E19: Blind Spot Detection
GET /api/v1/predict/blind-spots/{teamId}
```

---

### CATEGORY D: SAFETY & RELIABILITY (E7-E9)

| Enhancement | Required API | Status | Wiki File |
|-------------|--------------|--------|-----------|
| **E7: IEC 62443 Safety** | Safety Compliance API | ✅ COVERED | `API_SAFETY_COMPLIANCE.md` |
| **E8: RAMS Reliability** | Safety Compliance API | ✅ COVERED | `API_SAFETY_COMPLIANCE.md` |
| **E9: Hazard FMEA** | Safety Compliance API | ✅ COVERED | `API_SAFETY_COMPLIANCE.md` |

**Frontend Access (IEC 62443):**
```javascript
// Zone & Conduit Management
GET /api/v1/safety/zones
GET /api/v1/safety/zones/{zoneId}
GET /api/v1/safety/conduits
GET /api/v1/safety/conduits/{conduitId}

// Security Level Analysis
GET /api/v1/safety/zones/{zoneId}/gap-analysis
GET /api/v1/safety/requirements/{frId}/controls

// Compliance Assessment
POST /api/v1/safety/compliance/assess
GET /api/v1/safety/compliance/report/{assessmentId}
```

**Frontend Access (RAMS Reliability):**
```javascript
// Equipment Reliability
GET /api/v1/safety/rams/equipment/{equipmentId}
GET /api/v1/safety/rams/sector/{sectorId}/availability

// Failure Prediction
POST /api/v1/safety/rams/predict-failure
GET /api/v1/safety/rams/maintenance-schedule/{equipmentId}
```

**Frontend Access (FMEA Analysis):**
```javascript
// Failure Mode Analysis
GET /api/v1/safety/fmea/equipment/{equipmentId}/failure-modes
GET /api/v1/safety/fmea/rpn-scores
POST /api/v1/safety/fmea/analyze

// Risk Priority
GET /api/v1/safety/fmea/high-risk-modes
```

---

### CATEGORY E: ECONOMIC & BUSINESS (E10)

| Enhancement | Required API | Status | Wiki File |
|-------------|--------------|--------|-----------|
| **E10: Economic Impact** | Predictions API | ✅ COVERED | `API_PREDICTIONS.md` |

**Frontend Access:**
```javascript
// Economic Impact (in Predictions API)
GET /api/v1/predictions/economic-impact/:sectorId
POST /api/v1/predictions/breach-cost
GET /api/v1/predictions/roi/:mitigationId
```

---

### CATEGORY F: CONTINUOUS ENRICHMENT (E5)

| Enhancement | Required API | Status | Wiki File |
|-------------|--------------|--------|-----------|
| **E5: Real-Time Feeds** | Events API, VulnCheck API | ✅ COVERED | `API_EVENTS.md`, `API_VULNCHECK.md` |

**Frontend Access:**
```javascript
// Real-Time Events
GET /api/v1/events/stream
WebSocket /ws/events/subscribe
GET /api/v1/vulncheck/recent

// NVD/CISA Updates
GET /api/v1/cve/recent?hours=24
GET /api/v1/kev/updates
```

---

### CATEGORY G: OPERATIONAL EXCELLENCE (E12-E13, E15-E16)

| Enhancement | Required API | Status | Wiki File |
|-------------|--------------|--------|-----------|
| **E12: NOW/NEXT/NEVER** | Vulnerabilities API | ✅ COVERED | `API_VULNERABILITIES.md` |
| **E13: Attack Path Modeling** | Attack Path API | ✅ COVERED | `API_ATTACK_PATHS.md` |
| **E15: Vendor Equipment** | Equipment API | ✅ COVERED | `API_EQUIPMENT.md` |
| **E16: Protocol Analysis** | Protocol API | ✅ COVERED | `API_PROTOCOLS.md` |

**Frontend Access (Attack Paths):**
```javascript
// Path Enumeration
POST /api/v1/attack-paths/enumerate
GET /api/v1/attack-paths/from/{sourceId}/to/{targetId}

// Path Analysis
GET /api/v1/attack-paths/{pathId}/probability
GET /api/v1/attack-paths/{pathId}/mitigations
GET /api/v1/attack-paths/{pathId}/hops

// Attack Surface
GET /api/v1/attack-paths/attack-surface/{targetId}
GET /api/v1/attack-paths/chokepoints/{sectorId}

// Sector-Specific
GET /api/v1/attack-paths/sector/{sectorId}/paths
GET /api/v1/attack-paths/sector/{sectorId}/critical-assets
```

**Frontend Access (Protocols):**
```javascript
// Protocol Catalog
GET /api/v1/protocols
GET /api/v1/protocols/{protocolId}

// Vulnerability & Security
GET /api/v1/protocols/{protocolId}/vulnerabilities
GET /api/v1/protocols/{protocolId}/hardening

// Equipment Integration
GET /api/v1/protocols/{protocolId}/equipment

// Risk Assessment
POST /api/v1/protocols/risk-assessment
```

---

### CATEGORY H: CONSTITUTIONAL COMPLIANCE (E6)

| Enhancement | Required API | Status | Wiki File |
|-------------|--------------|--------|-----------|
| **E6: Wiki Truth Correction** | Query API | ✅ COVERED | `API_QUERY.md` |

---

## Database API Coverage

### All Databases Documented (4/4)

| Database | API File | Status | Key Features |
|----------|----------|--------|--------------|
| **Neo4j** | `02_Databases/Neo4j-Graph-Database.md` | ✅ COMPLETE | Bolt/HTTP, Cypher patterns |
| **MinIO** | `02_Databases/MinIO-Object-Storage.md` | ✅ COMPLETE | S3 API compatible |
| **MySQL** | `02_Databases/MySQL-Database.md` | ✅ COMPLETE | Schema documented |
| **Qdrant** | `02_Databases/Qdrant-Vector-Database.md` | ✅ COMPLETE | REST/gRPC API |

**Neo4j Access (Primary Database):**
```javascript
// Connection
Bolt Protocol: bolt://localhost:7687
HTTP API: http://localhost:7474
Browser: http://localhost:7474/browser

// Credentials
Username: neo4j
Password: neo4j@openspg

// Cypher Query Execution
POST /db/neo4j/tx/commit
```

---

## Specification Coverage

### 03_SPECIFICATIONS

| File | Covers | Status |
|------|--------|--------|
| `01_TECHNICAL_SPECS.md` | Core API specs, CVE scoring | ✅ |
| `E27_PSYCHOMETRIC_PREDICTIONS.md` | Psychohistory predictions | ✅ |
| `MCKENNEY_LACAN_CALCULUS.md` | McKenney-Lacan framework | ✅ |

---

## Application Coverage

### 03_Applications

| File | Covers | Status |
|------|--------|--------|
| `AEON-UI-Application.md` | Frontend app specs | ✅ |
| `AEON-UI-Enhancement-Design.md` | UI enhancement design | ✅ |
| `OpenSPG-Server.md` | OpenSPG backend | ✅ |

---

## Complete API File Inventory

### 04_APIs Directory (27 Files)

| # | File | Enhancements | Endpoints |
|---|------|--------------|-----------|
| 1 | `API_STIX.md` | E1, E2 | 15+ |
| 2 | `API_SBOM.md` | E3 | 12 |
| 3 | `API_VULNERABILITIES.md` | E12 | 20+ |
| 4 | `API_VULNCHECK.md` | E5 | 8 |
| 5 | `API_SAFETY_COMPLIANCE.md` | E7, E8, E9 | 18 |
| 6 | `API_ATTACK_PATHS.md` | E13 | 14 |
| 7 | `API_PROTOCOLS.md` | E16 | 10 |
| 8 | `API_EQUIPMENT.md` | E15 | 12 |
| 9 | `API_SECTORS.md` | General | 8 |
| 10 | `API_EVENTS.md` | E5 | 10 |
| 11 | `API_PREDICTIONS.md` | E10 | 8 |
| 12 | `API_QUERY.md` | E6 | 6 |
| 13 | `API_GRAPHQL.md` | General | GraphQL schema |
| 14 | `API_OPENSPG.md` | General | 15 |
| 15 | `API_AUTH.md` | General | 8 |
| 16 | `API_CAPEC.md` | General | 10 |
| 17 | `E27_PSYCHOHISTORY_API.md` | E4, E11, E14, E17-E26 | 18 |
| 18-27 | Other supporting APIs | Various | Various |

---

## Frontend Developer Quick Reference

### All Available APIs

| API | Purpose | Endpoint Base | Status |
|-----|---------|---------------|--------|
| Auth | Authentication | `/api/v1/auth/*` | ✅ |
| Sectors | 16 CISA sectors | `/api/v1/sectors/*` | ✅ |
| Equipment | 1.1M equipment nodes | `/api/v1/equipment/*` | ✅ |
| CVE/NVD | 315K vulnerabilities | `/api/v1/vulnerabilities/*` | ✅ |
| STIX | Threat intelligence | `/api/v1/stix/*` | ✅ |
| CAPEC | Attack patterns | `/api/v1/capec/*` | ✅ |
| Events | Event tracking | `/api/v1/events/*` | ✅ |
| Predictions | Level 6 predictions | `/api/v1/predictions/*` | ✅ |
| Psychohistory | E27 Seldon/McKenney | `/api/v1/predict/*`, `/api/v1/mckenney/*` | ✅ |
| **SBOM** | Supply chain analysis | `/api/v1/sbom/*` | ✅ NEW |
| **Safety** | IEC 62443/RAMS/FMEA | `/api/v1/safety/*` | ✅ NEW |
| **Attack Paths** | Path enumeration | `/api/v1/attack-paths/*` | ✅ NEW |
| **Protocols** | Industrial protocols | `/api/v1/protocols/*` | ✅ NEW |
| GraphQL | Flexible queries | `/graphql` | ✅ |
| Query | Cypher execution | `/api/v1/query/*` | ✅ |
| OpenSPG | Knowledge graph | `http://localhost:8887/*` | ✅ |
| VulnCheck | Real-time CVE | `/api/v1/vulncheck/*` | ✅ |

### Database Direct Access

| Database | Protocol | Port | Credentials |
|----------|----------|------|-------------|
| Neo4j | Bolt | 7687 | neo4j / neo4j@openspg |
| Neo4j | HTTP | 7474 | neo4j / neo4j@openspg |
| MySQL | MySQL | 3306 | root / openspg |
| Qdrant | REST | 6333 | API-Key header |
| Qdrant | gRPC | 6334 | API-Key header |
| MinIO | S3 | 9000 | minio / minio@openspg |
| OpenSPG | REST | 8887 | None |

---

## Version History

- **v1.0.0** (2025-11-29): Initial matrix with 10 gaps identified
- **v1.1.0** (2025-11-29): Neo4j documentation added (GAP-001 closed)
- **v2.0.0** (2025-11-30): All gaps closed
  - Added `API_SBOM.md` (GAP-002)
  - Added `API_SAFETY_COMPLIANCE.md` (GAP-003)
  - Added `API_ATTACK_PATHS.md` (GAP-004)
  - Added `API_PROTOCOLS.md` (GAP-005)
  - Extended `E27_PSYCHOHISTORY_API.md` with Lacanian endpoints (GAP-006)

---

**RECORD OF COMPLETION:** All 26 enhancements now have documented API access paths for frontend developers. Zero gaps remain.
