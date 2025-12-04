# Phase B3 API Capabilities Reference

**Document ID**: WIKI_API_PHASE_B3_2025-12-04
**Generated**: 2025-12-04 19:30:00 UTC
**Status**: PRODUCTION READY
**Phase**: B3 - Advanced Security Intelligence

---

## Overview

Phase B3 extends the AEON platform with advanced threat intelligence, risk scoring, and remediation workflow capabilities. These APIs integrate with Qdrant vector database for semantic search and are fully isolated per customer.

### What's New in Phase B3

| Enhancement | API Prefix | Endpoints | Status |
|-------------|-----------|-----------|--------|
| E04 Threat Intelligence | `/api/v2/threat-intel` | 27 | LIVE |
| E05 Risk Scoring Engine | `/api/v2/risk` | 26 | LIVE |
| E06 Remediation Workflow | `/api/v2/remediation` | 29 | LIVE |

**Total New Endpoints**: 82

---

## E04: Threat Intelligence Correlation API

### Purpose

Correlate threat intelligence data including APT groups, campaigns, MITRE ATT&CK mappings, and IOCs (Indicators of Compromise).

### Base Path

```
/api/v2/threat-intel
```

### Key Capabilities

| Capability | Description | Endpoints |
|------------|-------------|-----------|
| **APT Tracking** | Threat actor profiles, aliases, motivations | 7 endpoints |
| **Campaign Management** | Track ongoing and historical campaigns | 5 endpoints |
| **MITRE ATT&CK** | Technique mappings, coverage analysis | 5 endpoints |
| **IOC Management** | Indicators of compromise tracking | 5 endpoints |
| **Threat Feeds** | External intelligence feed integration | 3 endpoints |
| **Dashboard** | Threat intelligence summary | 2 endpoints |

### Threat Actor Model

```
ActorType: APT, CRIMINAL, HACKTIVIST, STATE_SPONSORED, INSIDER, UNKNOWN
Motivation: ESPIONAGE, FINANCIAL, DISRUPTION, DESTRUCTION, IDEOLOGICAL
ThreatScore: Calculated 0-10 based on activity, TTPs, and associated CVEs
```

### MITRE ATT&CK Integration

```
Detection Coverage: 0-1 (percentage of techniques with detection)
Mitigation Status: NOT_COVERED, PARTIAL, COVERED, MONITORING_ONLY
Coverage Gaps: Automatic identification of unmonitored techniques
```

### Example: Get Active Threat Actors Targeting Energy Sector

```bash
curl -X GET "https://api.aeon.local/api/v2/threat-intel/actors/by-sector/energy" \
  -H "X-Customer-ID: acme-corp"
```

Response:
```json
{
  "total_results": 5,
  "customer_id": "acme-corp",
  "results": [
    {
      "threat_actor_id": "apt-sandworm",
      "name": "Sandworm Team",
      "aliases": ["Voodoo Bear", "IRIDIUM", "Electrum"],
      "actor_type": "state_sponsored",
      "motivation": "disruption",
      "origin_country": "RU",
      "target_sectors": ["energy", "government", "telecommunications"],
      "ttps": ["T1189", "T1190", "T1059.001"],
      "associated_cves": ["CVE-2023-38831", "CVE-2022-30190"],
      "threat_score": 9.2,
      "is_active": true
    }
  ]
}
```

---

## E05: Risk Scoring Engine API

### Purpose

Calculate and manage multi-factor risk scores for entities, assess asset criticality, and measure attack surface exposure.

### Base Path

```
/api/v2/risk
```

### Key Capabilities

| Capability | Description | Endpoints |
|------------|-------------|-----------|
| **Risk Scoring** | Multi-factor composite risk calculation | 7 endpoints |
| **Asset Criticality** | Business impact and data classification | 6 endpoints |
| **Exposure Scoring** | Attack surface and internet exposure | 5 endpoints |
| **Risk Aggregation** | Aggregate risk by vendor, sector, type | 4 endpoints |
| **Dashboard** | Risk matrix and summary views | 4 endpoints |

### Risk Calculation Formula

```
Overall Risk = (Vulnerability × Weight_V + Threat × Weight_T +
                Exposure × Weight_E + Asset × Weight_A) × Multipliers

Where:
- Vulnerability Score (0-10): Based on CVE count and severity
- Threat Score (0-10): Based on APT targeting and IOC matches
- Exposure Score (0-10): Based on internet-facing services
- Asset Score (0-10): Based on criticality and data classification
- Multipliers: Criticality multiplier, exposure multiplier
```

### Risk Level Mapping

```
Risk Score → Risk Level:
  0.0 - 2.5  → LOW
  2.5 - 5.0  → MEDIUM
  5.0 - 7.5  → HIGH
  7.5 - 10.0 → CRITICAL
```

### Asset Criticality Levels

```
Criticality Level | RTO Threshold | Impact Level
MISSION_CRITICAL  | < 4 hours     | CATASTROPHIC
CRITICAL          | < 24 hours    | SEVERE
HIGH              | < 72 hours    | SIGNIFICANT
MEDIUM            | < 1 week      | MODERATE
LOW               | > 1 week      | MINIMAL
```

### Example: Get Risk Dashboard Summary

```bash
curl -X GET "https://api.aeon.local/api/v2/risk/dashboard/summary" \
  -H "X-Customer-ID: acme-corp"
```

Response:
```json
{
  "customer_id": "acme-corp",
  "summary": {
    "total_entities": 1250,
    "average_risk_score": 4.8,
    "critical_risk_count": 12,
    "high_risk_count": 45,
    "medium_risk_count": 234,
    "low_risk_count": 959,
    "trending_degrading": 23,
    "trending_improving": 67,
    "mission_critical_assets": 8,
    "internet_facing_assets": 156,
    "risk_score_distribution": {
      "0-2": 450,
      "2-4": 509,
      "4-6": 179,
      "6-8": 87,
      "8-10": 25
    }
  },
  "generated_at": "2025-12-04T19:30:00Z"
}
```

---

## E06: Remediation Workflow API

### Purpose

Track vulnerability remediation tasks, manage SLA compliance, and monitor remediation metrics.

### Base Path

```
/api/v2/remediation
```

### Key Capabilities

| Capability | Description | Endpoints |
|------------|-------------|-----------|
| **Task Management** | Create, track, assign remediation tasks | 11 endpoints |
| **Plan Management** | Multi-task remediation plans | 6 endpoints |
| **SLA Management** | SLA policies and compliance tracking | 6 endpoints |
| **Metrics** | MTTR, compliance rates, backlogs | 4 endpoints |
| **Dashboard** | Workload and summary views | 2 endpoints |

### Task Status Flow

```
OPEN → IN_PROGRESS → PENDING_VERIFICATION → VERIFIED → CLOSED
  ↓                                            ↓
WONT_FIX ←─────────────────────────── FALSE_POSITIVE
```

### SLA Configuration

```yaml
severity_thresholds:
  critical: 24    # hours to remediate
  high: 72
  medium: 168     # 7 days
  low: 720        # 30 days

escalation_levels:
  - level: 1
    threshold_percentage: 50   # 50% of SLA elapsed
    action: NOTIFY
  - level: 2
    threshold_percentage: 75
    action: ESCALATE_MANAGER
  - level: 3
    threshold_percentage: 100
    action: ESCALATE_EXECUTIVE
```

### SLA Status Calculation

```
Current Time vs SLA Deadline:
  < 75% elapsed  → WITHIN_SLA
  75-100% elapsed → AT_RISK
  > 100% elapsed → BREACHED
```

### Example: Get Overdue Tasks

```bash
curl -X GET "https://api.aeon.local/api/v2/remediation/tasks/overdue" \
  -H "X-Customer-ID: acme-corp"
```

Response:
```json
{
  "total_results": 8,
  "customer_id": "acme-corp",
  "results": [
    {
      "task_id": "TASK-2024-001",
      "title": "Patch CVE-2024-21762 on FortiOS devices",
      "cve_id": "CVE-2024-21762",
      "priority": "critical",
      "status": "in_progress",
      "sla_status": "breached",
      "sla_deadline": "2025-12-01T00:00:00Z",
      "days_overdue": 3,
      "assigned_to": "security-team",
      "asset_ids": ["firewall-01", "firewall-02", "firewall-03"],
      "severity_source": 9.8
    }
  ]
}
```

### Example: Get Remediation Metrics

```bash
curl -X GET "https://api.aeon.local/api/v2/remediation/metrics/summary" \
  -H "X-Customer-ID: acme-corp"
```

Response:
```json
{
  "customer_id": "acme-corp",
  "period_start": "2025-11-01",
  "period_end": "2025-12-04",
  "metrics": {
    "total_tasks": 234,
    "completed_tasks": 189,
    "open_tasks": 45,
    "overdue_tasks": 8,
    "mttr_hours": 48.5,
    "mttr_by_severity": {
      "critical": 18.2,
      "high": 42.5,
      "medium": 96.0,
      "low": 168.0
    },
    "sla_compliance_rate": 0.92,
    "sla_breaches": 18,
    "completion_rate": 0.81,
    "vulnerability_backlog": 156
  }
}
```

---

## Integration with Existing APIs

### Cross-API Correlation

The Phase B3 APIs integrate with existing Phase B2 APIs:

| Source API | Target API | Correlation |
|------------|------------|-------------|
| E03 SBOM | E04 Threat Intel | CVE → APT Groups using CVE |
| E03 SBOM | E05 Risk Scoring | Component vulnerabilities → Risk factors |
| E15 Vendor | E05 Risk Scoring | Vendor risk → Asset risk contribution |
| E04 Threat Intel | E06 Remediation | Campaign IOCs → Remediation tasks |
| E05 Risk Scoring | E06 Remediation | High-risk entities → Prioritized tasks |

### Combined Dashboard Query

```typescript
// Unified security posture dashboard
const securityPosture = await Promise.all([
  fetch('/api/v2/threat-intel/dashboard/summary', { headers }),
  fetch('/api/v2/risk/dashboard/summary', { headers }),
  fetch('/api/v2/remediation/dashboard/summary', { headers }),
  fetch('/api/v2/sbom/dashboard/summary', { headers }),
  fetch('/api/v2/vendor-equipment/dashboard/supply-chain', { headers }),
]);
```

---

## Qdrant Collections

| Collection | Vectors | Purpose |
|------------|---------|---------|
| `ner11_entities_hierarchical` | 384-dim | Core NER11 entities |
| `ner11_vendor_equipment` | 384-dim | Vendor and equipment data |
| `ner11_sbom` | 384-dim | SBOM and component data |
| `ner11_threat_intel` | 384-dim | Threat actors, campaigns, IOCs |
| `ner11_risk_scoring` | 384-dim | Risk scores and criticality |
| `ner11_remediation` | 384-dim | Remediation tasks and actions |

All collections use `sentence-transformers/all-MiniLM-L6-v2` for embeddings.

---

## Test Coverage

| API | Tests | Status |
|-----|-------|--------|
| E04 Threat Intelligence | 85/85 | PASSING |
| E05 Risk Scoring | 85/85 | PASSING |
| E06 Remediation Workflow | 85/85 | PASSING |

**Phase B3 Total**: 255 tests passing

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-04 19:30 | 3.0.0 | E04 + E05 + E06 complete |
| 2025-12-04 18:30 | 2.0.0 | E03 SBOM + E15 Vendor complete |
| 2025-12-04 03:40 | 1.0.0 | Customer Labels Phase B1 |

---

**Document**: WIKI_API_PHASE_B3_2025-12-04
**Generated**: 2025-12-04 19:30:00 UTC
**AEON Digital Twin Cybersecurity Platform**
