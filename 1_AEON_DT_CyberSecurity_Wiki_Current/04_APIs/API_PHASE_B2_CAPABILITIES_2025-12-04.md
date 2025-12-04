# Phase B2 API Capabilities Reference

**Document ID**: WIKI_API_PHASE_B2_2025-12-04
**Generated**: 2025-12-04 18:30:00 UTC
**Status**: PRODUCTION READY
**Phase**: B2 - Supply Chain Security

---

## Overview

This document describes the new API capabilities added during Phase B2 development. These APIs are production-ready and fully integrated with the NER11 Gold Model.

### What's New

| Enhancement | API Prefix | Endpoints | Status |
|-------------|-----------|-----------|--------|
| E15 Vendor Equipment | `/api/v2/vendor-equipment` | 28 | ✅ LIVE |
| E03 SBOM Analysis | `/api/v2/sbom` | 32 | ✅ LIVE |
| Customer Semantic Search | `/api/v2/search` | 5 | ✅ LIVE |

**Total New Endpoints**: 65

---

## E15: Vendor Equipment Lifecycle API

### Purpose

Track vendor risk, equipment lifecycle (EOL/EOS), maintenance scheduling, and supply chain vulnerabilities.

### Base Path

```
/api/v2/vendor-equipment
```

### Key Capabilities

| Capability | Description | Endpoints |
|------------|-------------|-----------|
| **Vendor Management** | Create, search, risk assessment | 5 endpoints |
| **Equipment Tracking** | EOL/EOS lifecycle, criticality | 6 endpoints |
| **CVE Integration** | Vendor vulnerability tracking | 4 endpoints |
| **Maintenance Windows** | Schedule, predict, work orders | 9 endpoints |
| **Dashboard** | Supply chain risk overview | 2 endpoints |

### Vendor Risk Model

```
Risk Score → Risk Level Mapping:
  0.0 - 2.5  → LOW
  2.5 - 5.0  → MEDIUM
  5.0 - 7.5  → HIGH
  7.5 - 10.0 → CRITICAL
```

### Lifecycle Status Flow

```
ACTIVE → APPROACHING_EOL (180 days) → AT_EOL → PAST_EOL
                                    ↓
                         APPROACHING_EOS → PAST_EOS
```

### Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/vendors/search` | Semantic vendor search |
| GET | `/vendors/{id}/risk-summary` | Complete risk analysis |
| GET | `/equipment/approaching-eol` | Equipment near end-of-life |
| POST | `/vendors/vulnerability` | Flag vendor CVE |
| GET | `/cves/critical` | Critical vulnerabilities |
| POST | `/maintenance-windows` | Schedule maintenance |
| GET | `/equipment/{id}/predictions` | AI maintenance predictions |
| POST | `/work-orders` | Create maintenance work order |

### Example: Get High-Risk Vendors

```bash
curl -X GET "https://api.aeon.local/api/v2/vendor-equipment/vendors/high-risk" \
  -H "X-Customer-ID: acme-corp"
```

Response:
```json
{
  "total_results": 3,
  "customer_id": "acme-corp",
  "results": [
    {
      "vendor_id": "vendor-obsolete",
      "name": "Legacy Systems Inc",
      "risk_score": 8.5,
      "risk_level": "critical",
      "total_cves": 45,
      "equipment_at_eol": 12
    }
  ]
}
```

---

## E03: SBOM Dependency & Vulnerability API

### Purpose

Software Bill of Materials management, dependency graph analysis, vulnerability correlation, and license compliance.

### Base Path

```
/api/v2/sbom
```

### Key Capabilities

| Capability | Description | Endpoints |
|------------|-------------|-----------|
| **SBOM Management** | CycloneDX/SPDX import/export | 5 endpoints |
| **Component Tracking** | Package identification (purl, cpe) | 6 endpoints |
| **Dependency Graph** | Tree, cycles, paths, impact | 6 endpoints |
| **Vulnerability Correlation** | CVE, EPSS, KEV, APT tracking | 9 endpoints |
| **License Compliance** | Risk analysis, conflicts | 2 endpoints |
| **Dashboard** | Customer-wide overview | 2 endpoints |

### SBOM Formats Supported

- **CycloneDX** (v1.4, v1.5)
- **SPDX** (v2.2, v2.3)
- **SWID Tags**
- **Syft Output**
- **Custom JSON**

### Vulnerability Prioritization

The API supports multiple prioritization methods:

1. **CVSS Score** (Traditional)
   - CRITICAL: 9.0-10.0
   - HIGH: 7.0-8.9
   - MEDIUM: 4.0-6.9
   - LOW: 0.1-3.9

2. **EPSS Score** (Exploit Probability)
   - Probability of exploitation in next 30 days
   - Score: 0.0-1.0
   - Higher EPSS = prioritize even if low CVSS

3. **CISA KEV** (Known Exploited)
   - Automatically critical priority
   - Active exploitation confirmed

4. **APT Group Association**
   - Track which threat actors use CVEs
   - Correlate with threat intelligence

### Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/sboms` | Create new SBOM |
| GET | `/sboms/{id}/risk-summary` | Complete risk summary |
| GET | `/components/search` | Semantic component search |
| GET | `/components/{id}/dependencies` | Dependency tree |
| GET | `/components/{id}/impact` | Impact analysis |
| GET | `/sboms/{id}/cycles` | Detect circular deps |
| GET | `/vulnerabilities/epss-prioritized` | EPSS-sorted vulns |
| GET | `/vulnerabilities/kev` | CISA KEV list |
| GET | `/vulnerabilities/by-apt` | APT group report |
| GET | `/sboms/{id}/license-compliance` | License analysis |

### Example: EPSS-Prioritized Vulnerabilities

```bash
curl -X GET "https://api.aeon.local/api/v2/sbom/vulnerabilities/epss-prioritized?limit=10" \
  -H "X-Customer-ID: acme-corp"
```

Response:
```json
{
  "total_results": 127,
  "customer_id": "acme-corp",
  "results": [
    {
      "cve_id": "CVE-2024-21762",
      "cvss_v3_score": 9.8,
      "epss_score": 0.974,
      "epss_percentile": 99.9,
      "in_the_wild": true,
      "cisa_kev": true,
      "component_name": "fortios",
      "fixed_version": "7.4.3",
      "apt_groups": ["APT28", "Sandworm"]
    }
  ]
}
```

### Example: Impact Analysis

```bash
curl -X GET "https://api.aeon.local/api/v2/sbom/components/comp-log4j/impact" \
  -H "X-Customer-ID: acme-corp"
```

Response:
```json
{
  "component_id": "comp-log4j",
  "component_name": "log4j-core",
  "direct_dependents": 45,
  "transitive_dependents": 234,
  "vulnerability_exposure": 3,
  "sboms_affected": ["sbom-web-app", "sbom-api-gateway", "sbom-microservices"],
  "max_cvss_propagated": 10.0,
  "remediation_urgency": "critical"
}
```

---

## Customer Semantic Search API

### Purpose

Multi-tenant isolated semantic search across all NER11 entity types.

### Base Path

```
/api/v2/search
```

### Hierarchical Filtering

```
Tier 1: 60 NER Labels
  │
  └─► Tier 2: 566 Fine-Grained Types
```

**Example Tier 1 Labels:**
- VULNERABILITY, MALWARE, ATTACK_PATTERN
- THREAT_ACTOR, TOOL, CAMPAIGN
- SOFTWARE, HARDWARE, PROTOCOL
- ORGANIZATION, LOCATION, SECTOR

**Example Tier 2 Types (MALWARE):**
- RANSOMWARE, TROJAN, WORM, SPYWARE
- ROOTKIT, BACKDOOR, KEYLOGGER, RAT

### Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/semantic` | Query-param search |
| POST | `/semantic/body` | JSON body search |
| GET | `/labels` | Available labels/types |
| GET | `/collections` | Qdrant collections |
| GET | `/health` | Service health |

### Example: Search with Filters

```bash
curl -X POST "https://api.aeon.local/api/v2/search/semantic?query=supply+chain+attack&limit=20&label_filter=ATTACK_PATTERN" \
  -H "X-Customer-ID: acme-corp"
```

Response:
```json
{
  "query": "supply chain attack",
  "total_results": 8,
  "customer_id": "acme-corp",
  "results": [
    {
      "entity_id": "capec-437",
      "text": "Supply Chain Infection",
      "label": "ATTACK_PATTERN",
      "fine_grained_type": "SUPPLY_CHAIN_COMPROMISE",
      "confidence": 0.92,
      "metadata": {
        "capec_id": "CAPEC-437",
        "mitre_attack": "T1195"
      }
    }
  ],
  "execution_time_ms": 23
}
```

---

## Authentication & Customer Isolation

### Required Header

All endpoints require the `X-Customer-ID` header:

```http
X-Customer-ID: your-customer-id
```

### Multi-Tenant Isolation

- All data automatically filtered by customer_id
- SYSTEM entities (shared CVEs, CWEs, ATT&CK) included by default
- No cross-customer data access possible
- Full audit trail for compliance

### Optional Headers

```http
X-User-ID: user@example.com    # For audit trail
X-Namespace: custom_namespace  # Data partitioning
```

---

## Integration with Existing APIs

### E15 + E03 Correlation

The `/api/v2/sbom/sboms/{id}/correlate-equipment` endpoint links:
- Software vulnerabilities → Physical equipment
- SBOM dependencies → Vendor equipment models
- CVE impact → Business-critical systems

```bash
curl -X POST "https://api.aeon.local/api/v2/sbom/sboms/sbom-001/correlate-equipment" \
  -H "X-Customer-ID: acme-corp" \
  -H "Content-Type: application/json" \
  -d '{"equipment_ids": ["equip-001", "equip-002"]}'
```

### Dashboard Aggregation

Both APIs provide dashboard endpoints:

- `/api/v2/vendor-equipment/dashboard/supply-chain`
- `/api/v2/sbom/dashboard/summary`

These can be combined for unified supply chain security views.

---

## Qdrant Collections

| Collection | Vectors | Purpose |
|------------|---------|---------|
| `ner11_entities_hierarchical` | 384-dim | Main entity storage |
| `ner11_vendor_equipment` | 384-dim | E15 vendor/equipment |
| `ner11_sbom` | 384-dim | E03 SBOM/components |

All use `sentence-transformers/all-MiniLM-L6-v2` for embeddings.

---

## Test Coverage

| API | Tests | Status |
|-----|-------|--------|
| E15 Vendor Equipment | 155/155 | ✅ PASSING |
| E03 SBOM Analysis | 54/54 | ✅ PASSING |
| Customer Semantic Search | 17/17 | ✅ PASSING |

**Total**: 226 tests passing

---

## Frontend Integration

See complete documentation in:

```
1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1/
├── API_REFERENCE_2025-12-04_1830.md     # Complete API reference
├── DATA_MODELS.ts                        # TypeScript interfaces
└── API_ACCESS_GUIDE.md                   # Quick start guide
```

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-04 18:30 | 2.0.0 | E03 SBOM + E15 Vendor complete |
| 2025-12-04 06:20 | 1.7.0 | E15 Day 11 maintenance scheduling |
| 2025-12-04 03:40 | 1.0.0 | Customer Labels Phase B1 |

---

**Document**: WIKI_API_PHASE_B2_2025-12-04
**Generated**: 2025-12-04 18:30:00 UTC
**AEON Digital Twin Cybersecurity Platform**
