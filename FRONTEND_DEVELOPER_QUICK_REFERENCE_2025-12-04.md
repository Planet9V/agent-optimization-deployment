# Frontend Developer Quick Reference
**For**: AEON Frontend Team | **Date**: 2025-12-04

---

## TL;DR - You Can Start TODAY

✅ **API Status**: 251+ endpoints LIVE at `http://localhost:8000`
✅ **Data Available**: 1.15M+ Neo4j nodes, 14,585+ vectors
✅ **Auth Ready**: Clerk OAuth 2.0 configured
✅ **No Blockers**: Everything you need is ready

**Start Time**: NOW

---

## 1. Setup (Week 1 - 56 hours)

### Day 1-2: Environment Setup (8 hours)

```bash
# Clone and install
git clone [your-repo]
cd aeon-frontend
npm install

# Configure environment
cp .env.example .env.local
# Set these values:
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=[from-clerk-dashboard]
CLERK_SECRET_KEY=[from-clerk-dashboard]

# Start development
npm run dev
# Open http://localhost:3000
```

### Day 3: Learn the APIs (8 hours)

**Read These First**:
1. `FRONTEND_QUICK_START_2025-12-04.md` (15 min)
2. `/api/v2/search/health` - Check API health
3. Test 5 endpoints with Postman/curl
4. Understand `X-Customer-ID` header requirement

**Test Calls**:
```bash
# Test health
curl http://localhost:8000/api/v2/search/health

# Test vendor search (Example E15)
curl -H "X-Customer-ID: demo" \
  "http://localhost:8000/api/v2/vendor-equipment/vendors/search?query=cisco"

# Test SBOM list (Example E03)
curl -H "X-Customer-ID: demo" \
  "http://localhost:8000/api/v2/sbom/sboms"

# Test semantic search (Example search)
curl -X POST -H "X-Customer-ID: demo" \
  -H "Content-Type: application/json" \
  -d '{"query":"ransomware detection","limit":10}' \
  http://localhost:8000/api/v2/search/semantic
```

### Day 4: Auth Setup (8 hours)

```typescript
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html>
        <body>{children}</body>
      </html>
    </ClerkProvider>
  )
}

// app/page.tsx
import { UserButton, useAuth } from '@clerk/nextjs'

export default function Home() {
  return (
    <div>
      <UserButton />
      {/* Your app content */}
    </div>
  )
}
```

### Day 5: API Client (8 hours)

```typescript
// lib/api-client.ts
import axios from 'axios'
import { useAuth } from '@clerk/nextjs'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export function useApiClient() {
  const { userId } = useAuth()

  const client = axios.create({
    baseURL: API_BASE,
    headers: {
      'X-Customer-ID': userId || 'demo-customer',
      'Content-Type': 'application/json',
    },
  })

  client.interceptors.response.use(
    response => response,
    error => {
      console.error('API Error:', error.response?.data || error.message)
      return Promise.reject(error)
    }
  )

  return client
}

// hooks/useVendors.ts
import { useApiClient } from '@/lib/api-client'
import { useState, useEffect } from 'react'

interface Vendor {
  vendor_id: string
  name: string
  risk_level: 'low' | 'medium' | 'high' | 'critical'
  total_cves: number
}

export function useVendors(search?: string) {
  const client = useApiClient()
  const [vendors, setVendors] = useState<Vendor[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!search) return

    setLoading(true)
    client
      .get('/api/v2/vendor-equipment/vendors/search', {
        params: { query: search, limit: 10 }
      })
      .then(res => setVendors(res.data.results))
      .finally(() => setLoading(false))
  }, [search, client])

  return { vendors, loading }
}
```

### Day 6-7: Tailwind + shadcn/ui (4 hours)

```bash
# Install Tailwind
npx tailwindcss init -p

# Add shadcn/ui
npx shadcn-ui@latest init

# Choose:
# - TypeScript: Yes
# - Style: New York
# - Base color: Slate
# - CSS variables: Yes

# Install first components
npx shadcn-ui@latest add button card input
```

---

## 2. Available APIs by Enhancement

### E03 SBOM Analysis (22 endpoints)

```typescript
// Key endpoints
GET    /api/v2/sbom/sboms              // List SBOMs
POST   /api/v2/sbom/upload             // Upload SBOM file
GET    /api/v2/sbom/components         // List components
GET    /api/v2/sbom/vulnerabilities    // List vulnerabilities
GET    /api/v2/sbom/licenses           // Analyze licenses
GET    /api/v2/sbom/dashboard/summary  // Dashboard data

// Example usage
const { data } = await client.get('/api/v2/sbom/dashboard/summary')
console.log(data)
// {
//   total_sboms: 42,
//   total_components: 1200,
//   critical_vulnerabilities: 15,
//   license_violations: 3,
//   avg_severity: 5.2
// }
```

### E04 Threat Intelligence (28 endpoints)

```typescript
// Key endpoints
GET    /api/v2/threat/actors           // List threat actors
GET    /api/v2/threat/campaigns        // List campaigns
GET    /api/v2/threat/ttps             // MITRE ATT&CK
GET    /api/v2/threat/malware          // Malware families
POST   /api/v2/threat/search           // Full-text search

// Example usage
const { data } = await client.get('/api/v2/threat/actors', {
  params: { limit: 20 }
})
// Returns list of threat actors with motivation/region
```

### E05 Risk Scoring (25 endpoints)

```typescript
// Key endpoints
POST   /api/v2/risk/score/calculate    // Calculate risk
GET    /api/v2/risk/matrix             // Risk matrix
GET    /api/v2/risk/trending           // Trends
GET    /api/v2/risk/dashboard          // Dashboard

// Example usage
const { data } = await client.post('/api/v2/risk/score/calculate', {
  entity_type: 'vulnerability',
  entity_id: 'CVE-2024-1234',
  urgency_factors: [{
    factor_type: 'exploit_available',
    weight: 1.0,
    value: 9.0
  }],
  risk_factors: [{
    factor_type: 'vulnerability',
    weight: 1.0,
    value: 9.2
  }]
})
// Returns priority score and category
```

### E06 Remediation (27 endpoints)

```typescript
// Key endpoints
GET    /api/v2/remediation/actions     // Remediation steps
POST   /api/v2/remediation/plan        // Create plan
GET    /api/v2/remediation/timeline    // Timeline
GET    /api/v2/remediation/roi         // ROI analysis

// Example usage
const { data } = await client.post('/api/v2/remediation/plan', {
  vulnerability_id: 'CVE-2024-1234',
  priority: 'critical'
})
// Returns step-by-step remediation plan
```

### E07 Compliance (24 endpoints)

```typescript
// Key endpoints
GET    /api/v2/compliance/frameworks   // NIST/PCI/HIPAA/GDPR
GET    /api/v2/compliance/controls     // Control details
POST   /api/v2/compliance/assess       // Assessment
GET    /api/v2/compliance/gaps         // Gap analysis

// Example usage
const { data } = await client.get('/api/v2/compliance/frameworks')
// Returns status of all compliance frameworks
```

### E08 Scanning (27 endpoints)

```typescript
// Key endpoints
POST   /api/v2/scanning/scan           // Start scan
GET    /api/v2/scanning/results        // Results
GET    /api/v2/scanning/findings       // Findings
GET    /api/v2/scanning/dashboard      // Dashboard

// Example usage
const { data } = await client.post('/api/v2/scanning/scan', {
  target: '10.0.0.0/24',
  scan_type: 'vulnerability'
})
// Returns scan job ID
```

### E09 Alerts (18 endpoints)

```typescript
// Key endpoints
GET    /api/v2/alerts/feed             // Real-time feed
POST   /api/v2/alerts/assign           // Assign alert
GET    /api/v2/alerts/grouped          // Grouped
GET    /api/v2/alerts/sla              // SLA tracking
GET    /api/v2/alerts/dashboard        // Dashboard

// Example usage
const { data } = await client.get('/api/v2/alerts/feed', {
  params: { limit: 50 }
})
// Returns real-time alert feed
```

### E10 Economic Impact (27 endpoints)

```typescript
// Key endpoints
GET    /api/v2/economic/breach-cost    // Cost estimates
GET    /api/v2/economic/roi            // ROI analysis
GET    /api/v2/economic/budget         // Budget projection
GET    /api/v2/economic/dashboard      // Executive dashboard

// Example usage
const { data } = await client.get('/api/v2/economic/breach-cost', {
  params: { industry: 'financial' }
})
// Returns breach cost estimates
```

### E11 Demographics (24 endpoints)

```typescript
// Key endpoints
GET    /api/v2/demographics/organization    // Org profile
GET    /api/v2/demographics/workforce       // Workforce
GET    /api/v2/demographics/roles           // Roles
GET    /api/v2/demographics/departments     // Departments

// Example usage
const { data } = await client.get('/api/v2/demographics/organization')
// Returns organization profile
```

### E12 Prioritization (28 endpoints)

```typescript
// Key endpoints
POST   /api/v2/prioritization/score    // Calculate priority
GET    /api/v2/prioritization/now      // NOW items
GET    /api/v2/prioritization/next     // NEXT items
GET    /api/v2/prioritization/dashboard// Dashboard

// Example usage
const { data } = await client.get('/api/v2/prioritization/dashboard')
// Returns priority distribution and SLA status
```

### E15 Vendor Equipment (25 endpoints)

```typescript
// Key endpoints
GET    /api/v2/vendor-equipment/vendors      // List vendors
GET    /api/v2/vendor-equipment/equipment    // Equipment
GET    /api/v2/vendor-equipment/risk         // Vendor risk
GET    /api/v2/vendor-equipment/eol          // EOL tracking
GET    /api/v2/vendor-equipment/dashboard    // Supply chain view

// Example usage
const { data } = await client.get('/api/v2/vendor-equipment/vendors', {
  params: { limit: 20 }
})
// Returns list of vendors with risk scores
```

### Semantic Search (5 endpoints)

```typescript
// Key endpoints
POST   /api/v2/search/semantic         // Natural language search
GET    /api/v2/search/suggestions      // Auto-complete
GET    /api/v2/search/health           // Service health

// Example usage
const { data } = await client.post('/api/v2/search/semantic', {
  query: 'ransomware detection',
  limit: 20
})
// Returns relevant entities with scores
```

---

## 3. TypeScript Interfaces

```typescript
// Core interfaces
interface Vendor {
  vendor_id: string
  name: string
  risk_score: number  // 0-10
  risk_level: 'low' | 'medium' | 'high' | 'critical'
  total_cves: number
  last_updated: string
}

interface Vulnerability {
  cve_id: string
  cvss_v3_score: number
  severity: 'none' | 'low' | 'medium' | 'high' | 'critical'
  epss_score?: number  // 0-1
  cisa_kev: boolean
  fixed_version?: string
}

interface RiskScore {
  entity_id: string
  score: number  // 0-100
  category: 'NOW' | 'NEXT' | 'NEVER'
  urgency_value: number
  risk_value: number
  impact_value: number
  effort_value: number
}

interface ComplianceStatus {
  framework: 'NIST' | 'PCI' | 'HIPAA' | 'GDPR'
  compliance_percentage: number
  total_controls: number
  compliant_controls: number
  gap_count: number
}

interface Alert {
  alert_id: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  status: 'open' | 'in_progress' | 'resolved'
  created_at: string
  sla_deadline: string
  assigned_to?: string
}
```

---

## 4. Common Component Patterns

### Dashboard Card (Reusable)

```typescript
// components/DashboardCard.tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface DashboardCardProps {
  title: string
  value: string | number
  subtext?: string
  trend?: 'up' | 'down' | 'stable'
  icon?: React.ReactNode
}

export function DashboardCard({
  title,
  value,
  subtext,
  trend,
  icon,
}: DashboardCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon && <div className="h-4 w-4">{icon}</div>}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {subtext && (
          <p className="text-xs text-muted-foreground">{subtext}</p>
        )}
      </CardContent>
    </Card>
  )
}

// Usage
<DashboardCard
  title="Critical CVEs"
  value={15}
  subtext="In your infrastructure"
  trend="up"
/>
```

### Data Table (Reusable)

```typescript
// components/DataTable.tsx
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

interface Column<T> {
  key: keyof T
  label: string
  render?: (value: any) => React.ReactNode
}

interface DataTableProps<T> {
  data: T[]
  columns: Column<T>[]
  loading?: boolean
}

export function DataTable<T extends { id: string }>({
  data,
  columns,
  loading,
}: DataTableProps<T>) {
  if (loading) return <p>Loading...</p>

  return (
    <Table>
      <TableHeader>
        <TableRow>
          {columns.map(col => (
            <TableHead key={String(col.key)}>{col.label}</TableHead>
          ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map(row => (
          <TableRow key={row.id}>
            {columns.map(col => (
              <TableCell key={String(col.key)}>
                {col.render
                  ? col.render(row[col.key])
                  : String(row[col.key])}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

// Usage
<DataTable
  data={vendors}
  columns={[
    { key: 'name', label: 'Vendor' },
    { key: 'risk_level', label: 'Risk', render: (v) => <Badge>{v}</Badge> },
    { key: 'total_cves', label: 'CVEs' },
  ]}
/>
```

---

## 5. Week-by-Week Tasks

### Week 1: Foundation (56 hours)
- [ ] Clone repo & npm install
- [ ] Test 5 APIs with Postman
- [ ] Setup Clerk authentication
- [ ] Build API client wrapper
- [ ] Configure state management
- [ ] Install & configure Tailwind
- [ ] Create component library
- [ ] Write first test

### Week 2-3: First Dashboard (96 hours)
- [ ] Main dashboard layout
- [ ] Vulnerability card
- [ ] Risk matrix chart
- [ ] Compliance status
- [ ] Alert feed
- [ ] Responsive design

### Week 4-6: Feature Expansion (192 hours)
- [ ] SBOM module
- [ ] Threat intelligence
- [ ] Risk scoring
- [ ] Remediation guidance
- [ ] Compliance details
- [ ] Scanning results

### Week 7-12: Full Application (1,024 hours)
- [ ] All remaining modules
- [ ] Advanced features
- [ ] Performance optimization
- [ ] Testing & QA
- [ ] Documentation
- [ ] Production deployment

---

## 6. Key Endpoints to Bookmark

```typescript
// Always test these first
Health Check:
  GET http://localhost:8000/api/v2/search/health

Dashboard Data (per module):
  GET http://localhost:8000/api/v2/sbom/dashboard/summary
  GET http://localhost:8000/api/v2/threat/dashboard
  GET http://localhost:8000/api/v2/risk/dashboard
  GET http://localhost:8000/api/v2/remediation/dashboard
  GET http://localhost:8000/api/v2/compliance/dashboard
  GET http://localhost:8000/api/v2/alerts/dashboard
  GET http://localhost:8000/api/v2/economic/dashboard
  GET http://localhost:8000/api/v2/demographics/dashboard
  GET http://localhost:8000/api/v2/prioritization/dashboard
  GET http://localhost:8000/api/v2/vendor-equipment/dashboard

Search:
  POST http://localhost:8000/api/v2/search/semantic
```

---

## 7. Common Issues & Solutions

### Issue: "X-Customer-ID required"
**Solution**: Always include header
```typescript
headers: {
  'X-Customer-ID': userId || 'demo-customer'
}
```

### Issue: CORS errors
**Solution**: Make sure API is at `http://localhost:8000`
```typescript
// .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Issue: Auth not working
**Solution**: Check Clerk configuration
```typescript
// Check your env variables
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
CLERK_SECRET_KEY
```

### Issue: Slow API responses
**Solution**: Normal - data is large (1.15M+ nodes). Use pagination
```typescript
// Add pagination
client.get('/api/v2/sbom/components', {
  params: { limit: 20, offset: 0 }
})
```

---

## 8. Resources

📚 **Documentation**:
- `FRONTEND_QUICK_START_2025-12-04.md` - 5-minute startup
- `REMAINING_ENHANCEMENTS_AND_FRONTEND_READINESS_2025-12-04.md` - Full details
- `EXECUTIVE_SUMMARY_ENHANCEMENTS_FRONTEND_2025-12-04.md` - Management summary

🔌 **APIs**:
- Base URL: `http://localhost:8000`
- 251+ endpoints, all documented
- Postman collection available

🛠️ **Tools**:
- Clerk: `https://dashboard.clerk.com`
- Postman: Import API collection
- Next.js: `npm run dev`

---

## 9. Success Checklist

### Day 1
- [ ] Dev environment working
- [ ] API health check passes
- [ ] Clerk auth configured

### Week 1
- [ ] 5 APIs tested successfully
- [ ] API client wrapper working
- [ ] First component built
- [ ] State management configured

### Week 3
- [ ] First dashboard live
- [ ] Data loading from APIs
- [ ] Charts/visualizations working
- [ ] Mobile responsive

### Week 6
- [ ] 12 dashboard components complete
- [ ] Real data flowing through
- [ ] All major APIs integrated
- [ ] Ready for feature modules

### Week 12
- [ ] All 7 modules operational
- [ ] 251+ endpoints integrated
- [ ] 1.15M+ Neo4j queries working
- [ ] Production deployment ready

---

**You're ready. Start Week 1 tasks TODAY.** 🚀

*Questions? Check the detailed docs above or ask your team lead.*
