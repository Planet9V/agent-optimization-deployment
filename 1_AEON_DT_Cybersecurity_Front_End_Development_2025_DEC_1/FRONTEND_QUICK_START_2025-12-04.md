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

**Generated**: 2025-12-04 18:30:00 UTC
**AEON Digital Twin Cybersecurity Platform**
