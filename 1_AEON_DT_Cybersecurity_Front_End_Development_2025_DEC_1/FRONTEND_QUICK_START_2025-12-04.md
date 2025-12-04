# AEON Frontend Developer Quick Start

**Document ID**: FRONTEND_QUICK_START_2025-12-04
**Generated**: 2025-12-04 18:30:00 UTC
**For**: UI/Frontend Developers

---

## TL;DR - Get Started in 5 Minutes

### 1. API Base URL
```typescript
const API_BASE = "http://localhost:8000";  // Development
// Production: "https://api.aeon-ner11.com"
```

### 2. Required Header (EVERY Request)
```typescript
headers: {
  "X-Customer-ID": "your-customer-id"  // REQUIRED
}
```

### 3. Test Connection
```bash
curl http://localhost:8000/api/v2/search/health
# Expected: { "status": "healthy", ... }
```

### 4. Your First API Call
```typescript
// TypeScript/React example
const response = await fetch(
  `${API_BASE}/api/v2/vendor-equipment/vendors/search?query=cisco&limit=10`,
  { headers: { "X-Customer-ID": "demo-customer" } }
);
const data = await response.json();
```

---

## Available APIs (65 Endpoints)

| API | Path | Endpoints | Purpose |
|-----|------|-----------|---------|
| Vendor Equipment | `/api/v2/vendor-equipment` | 28 | Supply chain tracking |
| SBOM Analysis | `/api/v2/sbom` | 32 | Software dependencies |
| Semantic Search | `/api/v2/search` | 5 | Entity search |

---

## Key Endpoints for Frontend

### Dashboard Data

```typescript
// Supply chain dashboard
GET /api/v2/vendor-equipment/dashboard/supply-chain

// SBOM customer summary
GET /api/v2/sbom/dashboard/summary

// Vendor risk summary
GET /api/v2/vendor-equipment/vendors/{vendor_id}/risk-summary

// SBOM risk summary
GET /api/v2/sbom/sboms/{sbom_id}/risk-summary
```

### Search

```typescript
// Semantic search (natural language)
POST /api/v2/search/semantic?query=ransomware&limit=20

// Vendor search
GET /api/v2/vendor-equipment/vendors/search?query=cisco

// Component search
GET /api/v2/sbom/components/search?query=log4j
```

### Lists & Tables

```typescript
// High-risk vendors
GET /api/v2/vendor-equipment/vendors/high-risk

// Equipment approaching EOL
GET /api/v2/vendor-equipment/equipment/approaching-eol?days=180

// Critical vulnerabilities
GET /api/v2/sbom/vulnerabilities/critical

// EPSS-prioritized vulnerabilities
GET /api/v2/sbom/vulnerabilities/epss-prioritized
```

---

## TypeScript Interfaces

```typescript
// Install: npm i -D typescript

interface Vendor {
  vendor_id: string;
  name: string;
  customer_id: string;
  risk_score: number;  // 0-10
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  total_cves: number;
}

interface Equipment {
  model_id: string;
  vendor_id: string;
  model_name: string;
  lifecycle_status: 'active' | 'approaching_eol' | 'at_eol' | 'past_eol';
  days_to_eol?: number;
}

interface SoftwareComponent {
  component_id: string;
  name: string;
  version: string;
  purl?: string;  // e.g., "pkg:npm/lodash@4.17.21"
  vulnerability_count: number;
  max_cvss_score: number;
}

interface Vulnerability {
  cve_id: string;
  cvss_v3_score: number;
  severity: 'none' | 'low' | 'medium' | 'high' | 'critical';
  epss_score?: number;  // 0-1 exploitation probability
  cisa_kev: boolean;    // Known exploited
  fixed_version?: string;
}
```

---

## React Integration Example

```tsx
// hooks/useVendors.ts
import { useState, useEffect } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function useVendorSearch(query: string, customerId: string) {
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!query) return;

    setLoading(true);
    fetch(`${API_BASE}/api/v2/vendor-equipment/vendors/search?query=${encodeURIComponent(query)}`, {
      headers: { 'X-Customer-ID': customerId }
    })
      .then(res => res.json())
      .then(data => setVendors(data.results))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [query, customerId]);

  return { vendors, loading, error };
}

// components/VendorList.tsx
export function VendorList({ customerId }: { customerId: string }) {
  const [search, setSearch] = useState('');
  const { vendors, loading, error } = useVendorSearch(search, customerId);

  return (
    <div>
      <input
        placeholder="Search vendors..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      <ul>
        {vendors.map(v => (
          <li key={v.vendor_id}>
            {v.name} - Risk: {v.risk_level} ({v.total_cves} CVEs)
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## Documentation Files

| File | Content |
|------|---------|
| `API_REFERENCE_2025-12-04_1830.md` | Complete API reference (65 endpoints) |
| `DATA_MODELS.ts` | TypeScript interfaces |
| `API_ACCESS_GUIDE.md` | Authentication guide |
| `BACKEND_COMPLETE_REFERENCE.md` | Full backend details |

---

## Environment Variables

```bash
# .env.local (Next.js)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_DEFAULT_CUSTOMER_ID=demo-customer
```

---

## Common Patterns

### Error Handling

```typescript
try {
  const response = await fetch(url, { headers });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'API Error');
  }
  return response.json();
} catch (error) {
  console.error('API call failed:', error);
  throw error;
}
```

### Pagination

```typescript
// Most list endpoints support limit/offset
GET /api/v2/vendor-equipment/vendors?limit=20&offset=0
GET /api/v2/sbom/components?limit=50&offset=100
```

### Filtering

```typescript
// Risk level filter
GET /api/v2/vendor-equipment/vendors?risk_level=high

// Severity filter
GET /api/v2/sbom/vulnerabilities?severity=critical

// Date range (equipment EOL)
GET /api/v2/vendor-equipment/equipment/approaching-eol?days=365
```

---

## Key Metrics for Dashboards

```typescript
// Risk Summary Response
{
  total_vendors: 45,
  high_risk_vendors: 3,
  total_equipment: 234,
  equipment_at_eol: 12,
  total_cves: 567,
  critical_cves: 23,
  avg_cvss: 6.4
}

// SBOM Summary Response
{
  total_sboms: 8,
  total_components: 1234,
  vulnerable_components: 89,
  critical_vulns: 12,
  kev_count: 3,
  remediation_available: 78
}
```

---

## Support

- **Full API Docs**: `API_REFERENCE_2025-12-04_1830.md`
- **Wiki**: `1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/`
- **TypeScript Types**: `DATA_MODELS.ts`

---

**Generated**: 2025-12-04 21:30:00 UTC
**AEON Digital Twin Cybersecurity Platform**

---

## 🚀 PHASE B3/B4 NEW APIs (Added 2025-12-04 21:30:00 UTC)

**172 NEW ENDPOINTS** deployed with full multi-tenant customer isolation.

### Updated API Count (237+ Endpoints)

| API | Path | Endpoints | Purpose | Phase |
|-----|------|-----------|---------|-------|
| Vendor Equipment | `/api/v2/vendor-equipment` | 28 | Supply chain tracking | B2 |
| SBOM Analysis | `/api/v2/sbom` | 32 | Software dependencies | B2 |
| Semantic Search | `/api/v2/search` | 5 | Entity search | B2 |
| **Threat Intelligence** | `/api/v2/threat-intel` | **27** | APT tracking, MITRE ATT&CK | **B3** |
| **Risk Scoring** | `/api/v2/risk` | **26** | Multi-factor risk calculation | **B3** |
| **Remediation** | `/api/v2/remediation` | **29** | Task management, SLA | **B3** |
| **Compliance** | `/api/v2/compliance` | **28** | Framework mapping, controls | **B4** |
| **Scanning** | `/api/v2/scanning` | **30** | Vulnerability scanning | **B4** |
| **Alerts** | `/api/v2/alerts` | **32** | Alert lifecycle | **B4** |

---

## Phase B3/B4 Dashboard Endpoints

```typescript
// Threat Intelligence Dashboard
GET /api/v2/threat-intel/dashboard/summary

// Risk Scoring Dashboard
GET /api/v2/risk/dashboard/summary

// Remediation Metrics
GET /api/v2/remediation/dashboard/summary

// Compliance Dashboard
GET /api/v2/compliance/dashboard/summary

// Scanning Summary
GET /api/v2/scanning/dashboard/summary

// Alert Dashboard
GET /api/v2/alerts/dashboard/summary
```

---

## Phase B3/B4 TypeScript Interfaces

```typescript
interface ThreatActor {
  threat_actor_id: string;
  name: string;
  aliases: string[];
  actor_type: 'apt' | 'criminal' | 'hacktivist' | 'state_sponsored' | 'insider' | 'unknown';
  motivation: 'espionage' | 'financial' | 'disruption' | 'destruction' | 'ideological';
  target_sectors: string[];
  ttps: string[];  // MITRE ATT&CK IDs
  threat_score: number;  // 0-10
  is_active: boolean;
  customer_id: string;
}

interface RiskScore {
  entity_id: string;
  customer_id: string;
  overall_risk_score: number;  // 0-10
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  vulnerability_score: number;
  threat_score: number;
  exposure_score: number;
  risk_trend: 'improving' | 'stable' | 'degrading';
}

interface RemediationTask {
  task_id: string;
  customer_id: string;
  title: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  status: 'open' | 'in_progress' | 'pending_verification' | 'verified' | 'closed';
  sla_status: 'within_sla' | 'at_risk' | 'breached';
  sla_deadline: string;
}

interface ComplianceControl {
  control_id: string;
  customer_id: string;
  framework: string;
  control_number: string;
  implementation_status: 'not_implemented' | 'partial' | 'implemented';
  compliance_status: 'compliant' | 'non_compliant' | 'partially_compliant';
}

interface ScanResult {
  result_id: string;
  customer_id: string;
  scan_id: string;
  cve_id?: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'informational';
  cvss_score?: number;
  status: 'new' | 'open' | 'remediated' | 'false_positive';
}

interface Alert {
  alert_id: string;
  customer_id: string;
  title: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  status: 'new' | 'acknowledged' | 'in_progress' | 'resolved' | 'closed';
  sla_status: 'within_sla' | 'at_risk' | 'breached';
}
```

---

## Unified Security Dashboard Query

```typescript
// Fetch all dashboard summaries in parallel
const headers = { 'X-Customer-ID': customerId };

const dashboards = await Promise.all([
  fetch(`${API_BASE}/api/v2/threat-intel/dashboard/summary`, { headers }),
  fetch(`${API_BASE}/api/v2/risk/dashboard/summary`, { headers }),
  fetch(`${API_BASE}/api/v2/remediation/dashboard/summary`, { headers }),
  fetch(`${API_BASE}/api/v2/compliance/dashboard/summary`, { headers }),
  fetch(`${API_BASE}/api/v2/scanning/dashboard/summary`, { headers }),
  fetch(`${API_BASE}/api/v2/alerts/dashboard/summary`, { headers }),
  fetch(`${API_BASE}/api/v2/sbom/dashboard/summary`, { headers }),
  fetch(`${API_BASE}/api/v2/vendor-equipment/dashboard/supply-chain`, { headers }),
]);

const [
  threatIntel,
  riskScoring,
  remediation,
  compliance,
  scanning,
  alerts,
  sbom,
  supplyChain
] = await Promise.all(dashboards.map(r => r.json()));
```

---

## Key Phase B3/B4 Features

### Threat Intelligence (E04)
- APT tracking with threat scores
- Campaign management
- MITRE ATT&CK technique mapping
- IOC management
- Threat feed integration

### Risk Scoring (E05)
- Multi-factor risk calculation
- Asset criticality levels
- Exposure scoring
- Risk trend analysis
- Configurable weights and thresholds

### Remediation Workflow (E06)
- Task management with SLA tracking
- Remediation plan coordination
- MTTR metrics
- Vulnerability backlog tracking

### Compliance Mapping (E07)
- NIST CSF, ISO 27001, SOC 2, PCI DSS, NERC CIP support
- Cross-framework control mapping
- Evidence management
- Automated gap analysis

### Scanning Integration (E08)
- Nessus, Qualys, Rapid7, Tenable support
- Scheduled scans
- Result aggregation
- Coverage reporting

### Alert Management (E09)
- Alert rules with conditions
- Multi-channel notifications (email, Slack, Teams, PagerDuty)
- Escalation policies
- SLA tracking

---

## Updated Documentation Files

| File | Content |
|------|---------|
| `API_REFERENCE_2025-12-04_1830.md` | Original 65 endpoints |
| `API_ACCESS_GUIDE.md` | **UPDATED** with 172 new endpoints |
| `COMPREHENSIVE_CAPABILITIES_CATALOG.md` | **UPDATED** with Phase B3/B4 |
| `README.md` | **UPDATED** with full API listing |
| `DATA_MODELS.ts` | TypeScript interfaces |

---

## Test Coverage

| API | Tests | Status |
|-----|-------|--------|
| E04 Threat Intelligence | 85/85 | ✅ PASSING |
| E05 Risk Scoring | 85/85 | ✅ PASSING |
| E06 Remediation Workflow | 85/85 | ✅ PASSING |
| E07 Compliance Mapping | 85/85 | ✅ PASSING |
| E08 Scanning Integration | 85/85 | ✅ PASSING |
| E09 Alert Management | 85/85 | ✅ PASSING |

**Phase B3/B4 Total**: 510 tests passing

---

**Phase B3/B4 Documentation Added**: 2025-12-04 21:30:00 UTC

---

## 🚀 PHASE B5 - ADVANCED ANALYTICS (Added 2025-12-04 22:00:00 UTC)

**78 NEW ENDPOINTS** for advanced analytics and intelligent prioritization.

### Updated API Count (315+ Endpoints)

| API | Path | Endpoints | Purpose | Phase |
|-----|------|-----------|---------|-------|
| **Economic Impact** | `/api/v2/economic-impact` | **26** | ROI, cost analysis, financial modeling | **B5** |
| **Demographics Baseline** | `/api/v2/demographics` | **24** | Workforce analytics, psychohistory baseline | **B5** |
| **Prioritization** | `/api/v2/prioritization` | **28** | NOW-NEXT-NEVER risk-adjusted prioritization | **B5** |

---

## Phase B5 Dashboard Endpoints

```typescript
// Economic Impact
GET /api/v2/economic-impact/dashboard/summary
GET /api/v2/economic-impact/roi/summary
POST /api/v2/economic-impact/roi/calculate

// Demographics Baseline
GET /api/v2/demographics/dashboard/summary
GET /api/v2/demographics/dashboard/baseline  // Psychohistory metrics
GET /api/v2/demographics/workforce/composition

// Prioritization (NOW-NEXT-NEVER)
GET /api/v2/prioritization/dashboard/summary
GET /api/v2/prioritization/now/items         // Immediate action
GET /api/v2/prioritization/next/items        // Scheduled
GET /api/v2/prioritization/never/items       // Low priority
POST /api/v2/prioritization/score/calculate   // Calculate priority score
```

---

## Phase B5 TypeScript Interfaces

```typescript
// E10 Economic Impact
interface ROICalculation {
  investment_id: string;
  customer_id: string;
  name: string;
  initial_investment: number;
  annual_benefits: number;
  annual_costs: number;
  roi_percentage: number;
  npv: number;               // Net Present Value
  irr: number;               // Internal Rate of Return
  payback_period_months: number;
  risk_adjusted_roi: number;
  confidence_score: number;
}

// E11 Demographics Baseline (Psychohistory)
interface BaselineMetrics {
  customer_id: string;
  population_stability_index: number;  // 0-1
  role_diversity_score: number;        // 0-1
  skill_concentration_risk: number;    // 0-10
  succession_coverage: number;         // 0-1
  insider_threat_baseline: number;     // 0-10
  calculated_at: string;
}

// E12 NOW-NEXT-NEVER Prioritization
interface PriorityItem {
  item_id: string;
  customer_id: string;
  entity_type: 'vulnerability' | 'remediation_task' | 'asset' | 'threat' | 'compliance_gap';
  entity_id: string;
  entity_name: string;
  priority_category: 'NOW' | 'NEXT' | 'NEVER';  // NOW >= 70, NEXT >= 40, NEVER < 40
  priority_score: number;
  deadline: string | null;
  sla_status: 'within_sla' | 'at_risk' | 'breached';
  is_now: boolean;
  is_sla_at_risk: boolean;
}
```

---

## Complete Unified Dashboard (All Phases)

```typescript
const headers = { 'X-Customer-ID': customerId };

const allDashboards = await Promise.all([
  // Phase B5 - Advanced Analytics
  fetch(`${API_BASE}/api/v2/economic-impact/dashboard/summary`, { headers }),
  fetch(`${API_BASE}/api/v2/demographics/dashboard/baseline`, { headers }),
  fetch(`${API_BASE}/api/v2/prioritization/dashboard/summary`, { headers }),
  // Phase B4 - Compliance & Automation
  fetch(`${API_BASE}/api/v2/compliance/dashboard/summary`, { headers }),
  fetch(`${API_BASE}/api/v2/scanning/dashboard/summary`, { headers }),
  fetch(`${API_BASE}/api/v2/alerts/dashboard/summary`, { headers }),
  // Phase B3 - Threat & Risk
  fetch(`${API_BASE}/api/v2/threat-intel/dashboard/summary`, { headers }),
  fetch(`${API_BASE}/api/v2/risk/dashboard/summary`, { headers }),
  fetch(`${API_BASE}/api/v2/remediation/dashboard/summary`, { headers }),
  // Phase B2 - Supply Chain
  fetch(`${API_BASE}/api/v2/sbom/dashboard/summary`, { headers }),
  fetch(`${API_BASE}/api/v2/vendor-equipment/dashboard/supply-chain`, { headers }),
]);

const [
  economicImpact,
  demographics,
  prioritization,
  compliance,
  scanning,
  alerts,
  threatIntel,
  riskScoring,
  remediation,
  sbom,
  supplyChain
] = await Promise.all(allDashboards.map(r => r.json()));
```

---

## Phase B5 Test Coverage

| API | Tests | Status |
|-----|-------|--------|
| E10 Economic Impact | 85/85 | ✅ PASSING |
| E11 Demographics Baseline | 85/85 | ✅ PASSING |
| E12 Prioritization | 85/85 | ✅ PASSING |

**Phase B5 Total**: 255 tests passing

---

## Full Documentation Reference

| Phase | APIs | Documentation File |
|-------|------|--------------------|
| B2 | SBOM, Vendor Equipment | `API_REFERENCE_2025-12-04_1830.md` |
| B3 | Threat Intel, Risk, Remediation | `API_PHASE_B3_CAPABILITIES_2025-12-04.md` |
| B4 | Compliance, Scanning, Alerts | `API_PHASE_B4_CAPABILITIES_2025-12-04.md` |
| B5 | Economic, Demographics, Priority | `API_PHASE_B5_CAPABILITIES_2025-12-04.md` |

---

**Phase B5 Documentation Added**: 2025-12-04 22:00:00 UTC
