# AEON Digital Twin - Frontend Developer Requirements Guide

**File:** FRONTEND_DEVELOPER_REQUIREMENTS_2025-12-04.md
**Created:** 2025-12-04 11:50:00 UTC
**Purpose:** Comprehensive onboarding guide for frontend developers new to AEON codebase
**Status:** OPERATIONAL (315+ APIs deployed)

---

## Executive Summary

You're joining a **cybersecurity digital twin platform** with **11 operational APIs** covering SBOM analysis, threat intelligence, risk scoring, compliance, scanning, alerts, economic impact, demographics, and prioritization. This guide answers every question you'll have in your first week.

**Quick Stats:**
- **315+ REST endpoints** operational across 11 APIs
- **Multi-tenant architecture** with customer isolation
- **FastAPI backend** with automatic OpenAPI/Swagger docs
- **Neo4j graph database** (1.1M+ nodes) + **Qdrant vector search**
- **Real-time updates** via SSE (Server-Sent Events)
- **~300ms average response time** for complex queries

---

## 1. WHAT WOULD A FRONTEND DEVELOPER NEED TO KNOW FIRST?

### 1.1 Backend Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     AEON Digital Twin                       │
│                    Frontend Interface                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│              FastAPI REST API Gateway                       │
│              http://localhost:8000                          │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Phase B2: Supply Chain (2 APIs, 65 endpoints)       │  │
│  │  - E03: SBOM Analysis                                │  │
│  │  - E15: Vendor Equipment Management                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Phase B3: Security Operations (3 APIs, 82 endpoints)│  │
│  │  - E04: Threat Intelligence Correlation              │  │
│  │  - E05: Risk Scoring Engine                          │  │
│  │  - E06: Remediation Workflow                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Phase B4: Compliance & Monitoring (3 APIs, 90 ep.)  │  │
│  │  - E07: Compliance Framework Mapping                 │  │
│  │  - E08: Automated Scanning Integration               │  │
│  │  - E09: Alert Management System                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Phase B5: Analytics & Prioritization (3 APIs, 78 ep)│  │
│  │  - E10: Economic Impact Modeling                     │  │
│  │  - E11: Demographics Baseline Analytics              │  │
│  │  - E12: NOW-NEXT-NEVER Prioritization                │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         ↓                           ↓
┌──────────────────┐      ┌──────────────────┐
│   Neo4j Graph    │      │  Qdrant Vector   │
│     Database     │      │     Search       │
│   1.1M+ nodes    │      │  670+ entities   │
│  232K+ relations │      │   384 dims       │
│ bolt://localhost │      │ http://localhost │
│     :7687        │      │     :6333        │
└──────────────────┘      └──────────────────┘
```

### 1.2 API Discovery: Where to Start

**Instant API Documentation:**
```bash
# Open interactive API docs (Swagger UI)
http://localhost:8000/docs

# Alternative: ReDoc documentation
http://localhost:8000/redoc

# Health check
curl http://localhost:8000/health
```

**Explore APIs by Phase:**

**Phase B2 - Supply Chain (Start Here):**
```bash
# SBOM Analysis
curl -H "X-Customer-ID: demo" http://localhost:8000/api/v2/sbom/dashboard/summary

# Vendor Equipment
curl -H "X-Customer-ID: demo" http://localhost:8000/api/v2/vendor-equipment/dashboard/supply-chain
```

**Phase B3 - Security Operations:**
```bash
# Threat Intelligence
curl -H "X-Customer-ID: demo" http://localhost:8000/api/v2/threat-intel/dashboard/summary

# Risk Scoring
curl -H "X-Customer-ID: demo" http://localhost:8000/api/v2/risk/dashboard/summary

# Remediation Workflow
curl -H "X-Customer-ID: demo" http://localhost:8000/api/v2/remediation/dashboard/summary
```

**Phase B4 - Compliance & Monitoring:**
```bash
# Compliance
curl -H "X-Customer-ID: demo" http://localhost:8000/api/v2/compliance/dashboard/summary

# Scanning
curl -H "X-Customer-ID: demo" http://localhost:8000/api/v2/scanning/dashboard/summary

# Alerts
curl -H "X-Customer-ID: demo" http://localhost:8000/api/v2/alerts/dashboard/summary
```

**Phase B5 - Analytics & Prioritization:**
```bash
# Economic Impact
curl -H "X-Customer-ID: demo" http://localhost:8000/api/v2/economic-impact/dashboard/summary

# Demographics
curl -H "X-Customer-ID: demo" http://localhost:8000/api/v2/demographics/dashboard/baseline

# Prioritization (NOW-NEXT-NEVER)
curl -H "X-Customer-ID: demo" http://localhost:8000/api/v2/prioritization/dashboard/summary
```

### 1.3 Authentication & Authorization

**Current Status:** ⚠️ Authentication in development

**Required Header for ALL Requests:**
```typescript
headers: {
  "X-Customer-ID": "your-customer-id"  // REQUIRED for multi-tenant isolation
}
```

**Future Authentication (When Implemented):**
```typescript
headers: {
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIs...",
  "X-Customer-ID": "your-customer-id"
}
```

**Access Levels (Planned):**
| Level | Permissions | Typical Usage |
|-------|-------------|---------------|
| `READ` | View dashboards, summaries, lists | Analysts, viewers |
| `WRITE` | Create, update, delete entities | Security teams |
| `ADMIN` | Configure settings, manage users | System administrators |

### 1.4 Data Structures You'll Work With

**Core Entity Types Across All APIs:**

```typescript
// Common response wrapper
interface APIResponse<T> {
  success: boolean;
  data: T;
  message: string;
  timestamp: string;
}

// Pagination (used by all list endpoints)
interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

// Multi-tenant isolation
interface TenantEntity {
  customer_id: string;  // ALWAYS present
  created_at: string;
  updated_at: string;
}
```

**Phase-Specific Data Structures:**

**Phase B2: Supply Chain**
```typescript
interface SBOMComponent {
  component_id: string;
  customer_id: string;
  name: string;
  version: string;
  supplier: string;
  vulnerabilities: VulnerabilityReference[];
  license: string;
  risk_score: number;
}

interface VendorEquipment {
  equipment_id: string;
  customer_id: string;
  vendor_name: string;
  model: string;
  sbom_components: string[];  // Component IDs
  compliance_status: ComplianceStatus;
  risk_level: RiskLevel;
}
```

**Phase B3: Security Operations**
```typescript
interface ThreatActor {
  threat_actor_id: string;
  customer_id: string;
  name: string;
  aliases: string[];
  actor_type: "apt" | "criminal" | "hacktivist" | "state_sponsored";
  motivation: "espionage" | "financial" | "disruption";
  targeted_sectors: string[];
  ttp_ids: string[];  // MITRE ATT&CK techniques
}

interface RiskScore {
  entity_id: string;
  customer_id: string;
  entity_type: "asset" | "component" | "vendor";
  risk_score: number;  // 0-10
  severity: "critical" | "high" | "medium" | "low";
  cvss_score: number;
  exploitability: number;
  calculated_at: string;
}

interface RemediationTask {
  task_id: string;
  customer_id: string;
  title: string;
  status: "open" | "in_progress" | "completed" | "blocked";
  priority: "critical" | "high" | "medium" | "low";
  assigned_to: string;
  due_date: string;
  vulnerability_ids: string[];
}
```

**Phase B4: Compliance & Monitoring**
```typescript
interface ComplianceControl {
  control_id: string;
  customer_id: string;
  framework: "nist_csf" | "iso_27001" | "cis" | "nerc_cip";
  control_number: string;
  implementation_status: "implemented" | "partial" | "not_implemented";
  evidence_count: number;
  last_assessment: string;
}

interface ScanResult {
  scan_id: string;
  customer_id: string;
  scanner_type: "vulnerability" | "compliance" | "configuration";
  target: string;
  findings_count: number;
  critical_findings: number;
  scan_date: string;
  status: "completed" | "in_progress" | "failed";
}

interface Alert {
  alert_id: string;
  customer_id: string;
  severity: "critical" | "high" | "medium" | "low";
  alert_type: "security" | "compliance" | "operational";
  status: "new" | "acknowledged" | "investigating" | "resolved";
  created_at: string;
  sla_deadline: string;
  is_sla_breached: boolean;
}
```

**Phase B5: Analytics & Prioritization**
```typescript
interface ROICalculation {
  investment_id: string;
  customer_id: string;
  name: string;
  roi_percentage: number;
  npv: number;  // Net Present Value
  irr: number;  // Internal Rate of Return
  payback_period_months: number;
  risk_adjusted_roi: number;
}

interface BaselineMetrics {
  customer_id: string;
  population_stability_index: number;  // 0-1
  role_diversity_score: number;        // 0-1
  skill_concentration_risk: number;    // 0-10
  succession_coverage: number;         // 0-1
  insider_threat_baseline: number;     // 0-10
}

interface PriorityItem {
  item_id: string;
  customer_id: string;
  entity_type: "vulnerability" | "remediation_task";
  priority_category: "NOW" | "NEXT" | "NEVER";
  priority_score: number;  // 0-100
  sla_status: "within_sla" | "at_risk" | "breached";
  deadline: string;
}
```

---

## 2. WHAT WOULD FRUSTRATE A FRONTEND DEVELOPER?

### 2.1 Missing Multi-Tenant Header

**Problem:**
```typescript
// ❌ This will fail with 400 Bad Request
fetch('http://localhost:8000/api/v2/risk/dashboard/summary')
```

**Error Response:**
```json
{
  "detail": "X-Customer-ID header is required"
}
```

**Solution:**
```typescript
// ✅ Always include customer ID header
const headers = {
  'X-Customer-ID': customerId  // Get from auth context
};

fetch('http://localhost:8000/api/v2/risk/dashboard/summary', { headers })
```

**Create Helper Function:**
```typescript
// api/client.ts
export const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

export function getHeaders(customerId: string): HeadersInit {
  return {
    'Content-Type': 'application/json',
    'X-Customer-ID': customerId,
    // Future: 'Authorization': `Bearer ${token}`
  };
}

export async function apiGet<T>(endpoint: string, customerId: string): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: getHeaders(customerId)
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}
```

### 2.2 Unknown Response Formats

**Problem:** Not knowing what data structure to expect

**Solution: Use Swagger UI to Explore**

```bash
# Open Swagger docs
http://localhost:8000/docs

# Click any endpoint → "Try it out" → See response schema
```

**Generate TypeScript Interfaces:**
```bash
# Install OpenAPI TypeScript generator
npm install -D openapi-typescript-codegen

# Generate types from OpenAPI spec
npx openapi-typescript-codegen --input http://localhost:8000/openapi.json --output ./src/types/api
```

**Result:**
```typescript
// Auto-generated types from OpenAPI spec
import { DashboardSummaryResponse, RiskScoreResponse } from './types/api';

// Now TypeScript knows the exact shape
const dashboard: DashboardSummaryResponse = await apiGet(...);
console.log(dashboard.total_items);  // Type-safe!
```

### 2.3 Unclear Error Handling

**Problem:** Backend errors aren't standardized

**Backend Error Format (FastAPI Standard):**
```json
{
  "detail": "Entity not found",
  "status_code": 404,
  "timestamp": "2025-12-04T11:50:00Z"
}
```

**Frontend Error Handler:**
```typescript
// api/errors.ts
export class APIError extends Error {
  constructor(
    public status: number,
    public detail: string,
    public timestamp?: string
  ) {
    super(detail);
    this.name = 'APIError';
  }
}

export async function handleAPIResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json();
    throw new APIError(
      response.status,
      error.detail || 'Unknown error',
      error.timestamp
    );
  }
  return response.json();
}

// Usage in components
try {
  const data = await apiGet('/api/v2/risk/dashboard/summary', customerId);
  setDashboard(data);
} catch (error) {
  if (error instanceof APIError) {
    if (error.status === 401) {
      // Redirect to login
    } else if (error.status === 403) {
      toast.error('You do not have permission to view this');
    } else if (error.status === 404) {
      toast.error('Data not found');
    } else {
      toast.error(error.detail);
    }
  }
}
```

### 2.4 No Example Code in Documentation

**THIS DOCUMENT SOLVES THAT - See Section 5 below for complete examples!**

### 2.5 Unknown Rate Limits or Quotas

**Current Status:** No rate limiting implemented yet

**When Implemented (Planned):**
```
Rate Limits:
  - 1000 requests/hour per customer
  - 100 requests/minute per customer

Response Headers:
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 847
  X-RateLimit-Reset: 1733317200
```

**Frontend Handling:**
```typescript
// Check rate limit headers
const remaining = response.headers.get('X-RateLimit-Remaining');
const reset = response.headers.get('X-RateLimit-Reset');

if (remaining && parseInt(remaining) < 10) {
  console.warn('Approaching rate limit');
}

// Handle 429 Too Many Requests
if (response.status === 429) {
  const retryAfter = response.headers.get('Retry-After');
  toast.warning(`Rate limit exceeded. Retry after ${retryAfter} seconds`);
}
```

---

## 3. WHAT TOOLS/LIBRARIES DO THEY NEED?

### 3.1 HTTP Client & State Management

**Recommended Stack:**

```json
{
  "dependencies": {
    "axios": "^1.6.0",
    "react-query": "^3.39.3",
    "zustand": "^4.4.7"
  }
}
```

**Why These Choices:**

**Axios** - Better than fetch for API calls:
```typescript
// api/axios-client.ts
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_BASE || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Automatic customer ID injection
apiClient.interceptors.request.use((config) => {
  const customerId = localStorage.getItem('customerId');
  if (customerId) {
    config.headers['X-Customer-ID'] = customerId;
  }
  return config;
});

// Automatic error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

**React Query** - Perfect for AEON's dashboard-heavy UI:
```typescript
// hooks/useDashboard.ts
import { useQuery } from 'react-query';
import { apiClient } from '../api/axios-client';

export function useRiskDashboard(customerId: string) {
  return useQuery(
    ['risk-dashboard', customerId],
    async () => {
      const response = await apiClient.get('/api/v2/risk/dashboard/summary');
      return response.data;
    },
    {
      staleTime: 5 * 60 * 1000,  // Fresh for 5 minutes
      refetchInterval: 60 * 1000, // Auto-refresh every minute
      refetchOnWindowFocus: true,
    }
  );
}

// Usage in component
function RiskDashboard() {
  const customerId = useCustomerId();
  const { data, isLoading, error, refetch } = useRiskDashboard(customerId);

  if (isLoading) return <Spinner />;
  if (error) return <ErrorBanner error={error} />;

  return (
    <div>
      <h1>Risk Dashboard</h1>
      <button onClick={() => refetch()}>Refresh</button>
      <RiskSummary data={data.summary} />
      <RiskMatrix data={data.matrix} />
    </div>
  );
}
```

**Zustand** - Lightweight global state:
```typescript
// store/customerStore.ts
import create from 'zustand';

interface CustomerState {
  customerId: string | null;
  setCustomerId: (id: string) => void;
}

export const useCustomerStore = create<CustomerState>((set) => ({
  customerId: localStorage.getItem('customerId'),
  setCustomerId: (id) => {
    localStorage.setItem('customerId', id);
    set({ customerId: id });
  },
}));

// Usage anywhere
function Component() {
  const customerId = useCustomerStore((state) => state.customerId);
  // ...
}
```

### 3.2 Data Visualization

**For 11 Dashboards + Charts:**

```json
{
  "dependencies": {
    "recharts": "^2.10.0",
    "react-chartjs-2": "^5.2.0",
    "chart.js": "^4.4.0",
    "d3": "^7.8.5",
    "@nivo/core": "^0.84.0",
    "@nivo/bar": "^0.84.0",
    "@nivo/line": "^0.84.0"
  }
}
```

**Recommendation: Start with Recharts**

**Why:** Simple API, responsive, works great for dashboards

```typescript
// components/RiskTrendChart.tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

interface Props {
  data: Array<{ date: string; risk_score: number }>;
}

export function RiskTrendChart({ data }: Props) {
  return (
    <LineChart width={600} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis domain={[0, 10]} />
      <Tooltip />
      <Legend />
      <Line
        type="monotone"
        dataKey="risk_score"
        stroke="#8884d8"
        strokeWidth={2}
      />
    </LineChart>
  );
}
```

**For Neo4j Graph Visualization:**

```json
{
  "dependencies": {
    "react-force-graph": "^1.44.0",
    "vis-network": "^9.1.9"
  }
}
```

**Example: Attack Path Visualization**
```typescript
// components/AttackPathGraph.tsx
import { ForceGraph2D } from 'react-force-graph';

interface Node {
  id: string;
  name: string;
  type: 'threat_actor' | 'malware' | 'vulnerability' | 'asset';
}

interface Link {
  source: string;
  target: string;
  relationship: string;
}

export function AttackPathGraph({ nodes, links }: { nodes: Node[], links: Link[] }) {
  return (
    <ForceGraph2D
      graphData={{ nodes, links }}
      nodeLabel="name"
      nodeColor={(node) => nodeColorByType[node.type]}
      linkLabel="relationship"
      linkDirectionalArrowLength={6}
      linkDirectionalArrowRelPos={1}
      linkCurvature={0.25}
    />
  );
}
```

### 3.3 Form Handling

**For Creating/Editing Entities:**

```json
{
  "dependencies": {
    "react-hook-form": "^7.48.0",
    "zod": "^3.22.0",
    "@hookform/resolvers": "^3.3.0"
  }
}
```

**Example: Create Remediation Task**
```typescript
// forms/RemediationTaskForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  title: z.string().min(1, 'Title is required'),
  priority: z.enum(['critical', 'high', 'medium', 'low']),
  assigned_to: z.string().email(),
  due_date: z.string(),
  vulnerability_ids: z.array(z.string()).min(1),
});

type FormData = z.infer<typeof schema>;

export function RemediationTaskForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('title')} placeholder="Task title" />
      {errors.title && <span>{errors.title.message}</span>}

      <select {...register('priority')}>
        <option value="critical">Critical</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>

      <input {...register('assigned_to')} type="email" placeholder="Email" />
      <input {...register('due_date')} type="date" />

      <button type="submit">Create Task</button>
    </form>
  );
}
```

### 3.4 Testing

```json
{
  "devDependencies": {
    "@testing-library/react": "^14.1.0",
    "@testing-library/jest-dom": "^6.1.0",
    "@testing-library/user-event": "^14.5.0",
    "msw": "^2.0.0"
  }
}
```

**Mock Service Worker for API Testing:**
```typescript
// mocks/handlers.ts
import { rest } from 'msw';

export const handlers = [
  rest.get('http://localhost:8000/api/v2/risk/dashboard/summary', (req, res, ctx) => {
    return res(
      ctx.json({
        customer_id: 'demo',
        total_items: 150,
        high_risk_count: 25,
        average_risk_score: 6.2,
      })
    );
  }),
];

// Component test
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { RiskDashboard } from './RiskDashboard';

test('renders risk dashboard', async () => {
  const queryClient = new QueryClient();
  render(
    <QueryClientProvider client={queryClient}>
      <RiskDashboard />
    </QueryClientProvider>
  );

  expect(await screen.findByText('Risk Dashboard')).toBeInTheDocument();
  expect(await screen.findByText('150')).toBeInTheDocument();
});
```

---

## 4. WHAT COMPONENTS WOULD THEY BUILD?

### 4.1 Dashboard Components (11 Primary Dashboards)

**One dashboard per API + unified overview:**

```
src/
├── components/
│   ├── dashboards/
│   │   ├── UnifiedDashboard.tsx          # Aggregate view of all APIs
│   │   ├── SBOMDashboard.tsx             # E03: SBOM Analysis
│   │   ├── VendorEquipmentDashboard.tsx  # E15: Vendor Equipment
│   │   ├── ThreatIntelDashboard.tsx      # E04: Threat Intelligence
│   │   ├── RiskDashboard.tsx             # E05: Risk Scoring
│   │   ├── RemediationDashboard.tsx      # E06: Remediation Workflow
│   │   ├── ComplianceDashboard.tsx       # E07: Compliance Mapping
│   │   ├── ScanningDashboard.tsx         # E08: Automated Scanning
│   │   ├── AlertsDashboard.tsx           # E09: Alert Management
│   │   ├── EconomicImpactDashboard.tsx   # E10: Economic Impact
│   │   ├── DemographicsDashboard.tsx     # E11: Demographics Baseline
│   │   └── PrioritizationDashboard.tsx   # E12: NOW-NEXT-NEVER
```

**Example: Unified Dashboard Structure**
```typescript
// dashboards/UnifiedDashboard.tsx
import { useQuery } from 'react-query';
import { Grid, Card } from '@mui/material';

export function UnifiedDashboard() {
  const customerId = useCustomerId();

  // Fetch all 11 dashboards in parallel
  const dashboards = useQueries([
    { queryKey: ['sbom-dashboard'], queryFn: () => fetchSBOMDashboard(customerId) },
    { queryKey: ['vendor-dashboard'], queryFn: () => fetchVendorDashboard(customerId) },
    { queryKey: ['threat-dashboard'], queryFn: () => fetchThreatDashboard(customerId) },
    { queryKey: ['risk-dashboard'], queryFn: () => fetchRiskDashboard(customerId) },
    { queryKey: ['remediation-dashboard'], queryFn: () => fetchRemediationDashboard(customerId) },
    { queryKey: ['compliance-dashboard'], queryFn: () => fetchComplianceDashboard(customerId) },
    { queryKey: ['scanning-dashboard'], queryFn: () => fetchScanningDashboard(customerId) },
    { queryKey: ['alerts-dashboard'], queryFn: () => fetchAlertsDashboard(customerId) },
    { queryKey: ['economic-dashboard'], queryFn: () => fetchEconomicDashboard(customerId) },
    { queryKey: ['demographics-dashboard'], queryFn: () => fetchDemographicsDashboard(customerId) },
    { queryKey: ['prioritization-dashboard'], queryFn: () => fetchPrioritizationDashboard(customerId) },
  ]);

  const isLoading = dashboards.some((q) => q.isLoading);
  const errors = dashboards.filter((q) => q.error);

  if (isLoading) return <DashboardSkeleton />;
  if (errors.length > 0) return <ErrorBoundary errors={errors} />;

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={4}>
        <KPICard
          title="High Risk Items"
          value={dashboards[3].data.high_risk_count}
          trend="+12%"
        />
      </Grid>
      <Grid item xs={12} md={4}>
        <KPICard
          title="Critical Alerts"
          value={dashboards[7].data.critical_alerts}
          trend="-5%"
        />
      </Grid>
      <Grid item xs={12} md={4}>
        <KPICard
          title="NOW Priority Items"
          value={dashboards[10].data.now_count}
          trend="+8%"
        />
      </Grid>

      {/* Individual dashboard cards */}
      <Grid item xs={12} md={6}>
        <Card>
          <h3>Risk Overview</h3>
          <RiskSummaryWidget data={dashboards[3].data} />
        </Card>
      </Grid>

      <Grid item xs={12} md={6}>
        <Card>
          <h3>Alert Status</h3>
          <AlertStatusWidget data={dashboards[7].data} />
        </Card>
      </Grid>

      {/* More dashboard cards... */}
    </Grid>
  );
}
```

### 4.2 Data Tables with Sorting/Filtering

**Reusable Data Table Component:**

```typescript
// components/DataTable.tsx
import { DataGrid, GridColDef } from '@mui/x-data-grid';

interface Props<T> {
  rows: T[];
  columns: GridColDef[];
  loading?: boolean;
  onRowClick?: (row: T) => void;
}

export function DataTable<T extends { id: string }>({
  rows,
  columns,
  loading,
  onRowClick
}: Props<T>) {
  return (
    <DataGrid
      rows={rows}
      columns={columns}
      loading={loading}
      pageSize={25}
      rowsPerPageOptions={[25, 50, 100]}
      checkboxSelection
      disableSelectionOnClick
      onRowClick={(params) => onRowClick?.(params.row)}
      autoHeight
    />
  );
}

// Usage: Remediation Tasks Table
const columns: GridColDef[] = [
  { field: 'title', headerName: 'Task', flex: 1 },
  { field: 'priority', headerName: 'Priority', width: 120 },
  { field: 'status', headerName: 'Status', width: 120 },
  { field: 'assigned_to', headerName: 'Assigned To', width: 200 },
  { field: 'due_date', headerName: 'Due Date', width: 150 },
];

function RemediationTasksTable() {
  const { data, isLoading } = useRemediationTasks();

  return (
    <DataTable
      rows={data?.items || []}
      columns={columns}
      loading={isLoading}
      onRowClick={(task) => navigate(`/remediation/tasks/${task.task_id}`)}
    />
  );
}
```

### 4.3 Charts and Graphs

**Risk Trend Chart:**
```typescript
// components/charts/RiskTrendChart.tsx
import { Line } from 'react-chartjs-2';

export function RiskTrendChart({ data }: { data: TrendData[] }) {
  const chartData = {
    labels: data.map(d => d.date),
    datasets: [
      {
        label: 'Average Risk Score',
        data: data.map(d => d.risk_score),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        tension: 0.4,
      },
      {
        label: 'Critical Count',
        data: data.map(d => d.critical_count),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.4,
      }
    ]
  };

  return <Line data={chartData} options={{ responsive: true }} />;
}
```

**Risk Matrix Heatmap:**
```typescript
// components/charts/RiskMatrixHeatmap.tsx
interface Cell {
  likelihood: number;
  impact: number;
  count: number;
}

export function RiskMatrixHeatmap({ cells }: { cells: Cell[] }) {
  return (
    <div className="risk-matrix">
      {[5, 4, 3, 2, 1].map(likelihood => (
        <div key={likelihood} className="matrix-row">
          {[1, 2, 3, 4, 5].map(impact => {
            const cell = cells.find(c => c.likelihood === likelihood && c.impact === impact);
            const riskLevel = likelihood * impact;
            const color = riskLevel >= 15 ? 'critical' :
                         riskLevel >= 10 ? 'high' :
                         riskLevel >= 5 ? 'medium' : 'low';

            return (
              <div key={impact} className={`matrix-cell ${color}`}>
                {cell?.count || 0}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
```

### 4.4 Forms for Data Entry

**Create SBOM Component Form:**
```typescript
// forms/SBOMComponentForm.tsx
import { useForm } from 'react-hook-form';
import { useMutation, useQueryClient } from 'react-query';

export function SBOMComponentForm() {
  const queryClient = useQueryClient();
  const { register, handleSubmit } = useForm();

  const createComponent = useMutation(
    (data: ComponentData) => apiClient.post('/api/v2/sbom/components', data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['sbom-components']);
        toast.success('Component created successfully');
      }
    }
  );

  return (
    <form onSubmit={handleSubmit(createComponent.mutate)}>
      <input {...register('name')} placeholder="Component name" required />
      <input {...register('version')} placeholder="Version" required />
      <input {...register('supplier')} placeholder="Supplier" required />
      <input {...register('license')} placeholder="License" />

      <button type="submit" disabled={createComponent.isLoading}>
        {createComponent.isLoading ? 'Creating...' : 'Create Component'}
      </button>
    </form>
  );
}
```

### 4.5 Real-Time Alerts

**Alert Notification System:**
```typescript
// components/AlertNotifications.tsx
import { useEffect, useState } from 'react';
import { toast } from 'react-hot-toast';

export function AlertNotifications() {
  const customerId = useCustomerId();

  useEffect(() => {
    // Server-Sent Events for real-time alerts
    const eventSource = new EventSource(
      `http://localhost:8000/api/v2/alerts/stream?customer_id=${customerId}`
    );

    eventSource.addEventListener('new_alert', (event) => {
      const alert = JSON.parse(event.data);

      if (alert.severity === 'critical') {
        toast.error(`🚨 Critical Alert: ${alert.title}`, {
          duration: 10000,
          position: 'top-right',
        });
      } else if (alert.severity === 'high') {
        toast.warning(`⚠️ High Alert: ${alert.title}`);
      }
    });

    return () => eventSource.close();
  }, [customerId]);

  return null; // No visual component, just side effects
}

// Add to App.tsx
function App() {
  return (
    <>
      <AlertNotifications />
      <Toaster />
      {/* Rest of app */}
    </>
  );
}
```

### 4.6 Search Interfaces

**Global Entity Search:**
```typescript
// components/GlobalSearch.tsx
import { useState } from 'react';
import { useDebounce } from 'use-debounce';

export function GlobalSearch() {
  const [query, setQuery] = useState('');
  const [debouncedQuery] = useDebounce(query, 300);

  const { data, isLoading } = useQuery(
    ['global-search', debouncedQuery],
    () => apiClient.get('/api/v2/search', { params: { q: debouncedQuery } }),
    { enabled: debouncedQuery.length > 2 }
  );

  return (
    <div className="search-container">
      <input
        type="text"
        placeholder="Search vulnerabilities, assets, threats..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      {isLoading && <Spinner />}

      {data && (
        <div className="search-results">
          {data.results.map((result) => (
            <SearchResult key={result.id} result={result} />
          ))}
        </div>
      )}
    </div>
  );
}
```

### 4.7 Export/Download Features

**Export Dashboard Data:**
```typescript
// utils/export.ts
export function exportToCSV(data: any[], filename: string) {
  const headers = Object.keys(data[0]);
  const csv = [
    headers.join(','),
    ...data.map(row => headers.map(h => JSON.stringify(row[h])).join(','))
  ].join('\n');

  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${filename}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

// Usage in dashboard
function ExportButton({ data }: { data: any[] }) {
  return (
    <button onClick={() => exportToCSV(data, 'risk-dashboard')}>
      Export to CSV
    </button>
  );
}
```

---

## 5. WHAT SAMPLE CODE WOULD HELP MOST?

### 5.1 Complete API Call Examples in React Hooks

**Example 1: Fetch Risk Dashboard**
```typescript
// hooks/useRiskDashboard.ts
import { useQuery } from 'react-query';
import { apiClient } from '../api/axios-client';

interface RiskDashboard {
  customer_id: string;
  total_items: number;
  high_risk_count: number;
  critical_risk_count: number;
  average_risk_score: number;
  risk_distribution: Record<string, number>;
  trend: 'increasing' | 'stable' | 'decreasing';
}

export function useRiskDashboard(customerId: string) {
  return useQuery<RiskDashboard>(
    ['risk-dashboard', customerId],
    async () => {
      const response = await apiClient.get('/api/v2/risk/dashboard/summary');
      return response.data;
    },
    {
      staleTime: 5 * 60 * 1000,  // Data fresh for 5 minutes
      refetchInterval: 60 * 1000, // Auto-refresh every minute
      retry: 3,
      onError: (error) => {
        console.error('Failed to fetch risk dashboard:', error);
      }
    }
  );
}

// Usage in component
function RiskDashboardPage() {
  const customerId = useCustomerId();
  const { data, isLoading, error, refetch } = useRiskDashboard(customerId);

  if (isLoading) return <Skeleton variant="rectangular" height={400} />;
  if (error) return <Alert severity="error">Failed to load dashboard</Alert>;

  return (
    <Container>
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Typography variant="h4">Risk Dashboard</Typography>
        <Button onClick={() => refetch()}>Refresh</Button>
      </Box>

      <Grid container spacing={3} mt={2}>
        <Grid item xs={12} md={3}>
          <StatCard
            title="Total Items"
            value={data.total_items}
            icon={<AssessmentIcon />}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatCard
            title="High Risk"
            value={data.high_risk_count}
            color="warning"
            icon={<WarningIcon />}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatCard
            title="Critical Risk"
            value={data.critical_risk_count}
            color="error"
            icon={<ErrorIcon />}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatCard
            title="Average Score"
            value={data.average_risk_score.toFixed(1)}
            subtitle="/10"
          />
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Risk Distribution</Typography>
            <RiskDistributionChart data={data.risk_distribution} />
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Trend</Typography>
            <TrendIndicator trend={data.trend} />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}
```

**Example 2: Create Remediation Task with Error Handling**
```typescript
// hooks/useCreateRemediationTask.ts
import { useMutation, useQueryClient } from 'react-query';
import { apiClient } from '../api/axios-client';
import { toast } from 'react-hot-toast';

interface CreateTaskData {
  title: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  assigned_to: string;
  due_date: string;
  vulnerability_ids: string[];
}

export function useCreateRemediationTask() {
  const queryClient = useQueryClient();

  return useMutation(
    async (data: CreateTaskData) => {
      const response = await apiClient.post('/api/v2/remediation/tasks', data);
      return response.data;
    },
    {
      onSuccess: (data) => {
        // Invalidate and refetch tasks list
        queryClient.invalidateQueries(['remediation-tasks']);
        toast.success(`Task "${data.title}" created successfully`);
      },
      onError: (error: any) => {
        const message = error.response?.data?.detail || 'Failed to create task';
        toast.error(message);
      }
    }
  );
}

// Usage in form component
function CreateTaskForm() {
  const createTask = useCreateRemediationTask();
  const { register, handleSubmit, formState: { errors } } = useForm<CreateTaskData>();

  const onSubmit = (data: CreateTaskData) => {
    createTask.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <TextField
        {...register('title', { required: 'Title is required' })}
        label="Task Title"
        fullWidth
        error={!!errors.title}
        helperText={errors.title?.message}
      />

      <Select {...register('priority')} label="Priority">
        <MenuItem value="critical">Critical</MenuItem>
        <MenuItem value="high">High</MenuItem>
        <MenuItem value="medium">Medium</MenuItem>
        <MenuItem value="low">Low</MenuItem>
      </Select>

      <TextField
        {...register('assigned_to', { required: 'Assignee required' })}
        label="Assign To"
        type="email"
      />

      <TextField
        {...register('due_date', { required: 'Due date required' })}
        label="Due Date"
        type="date"
        InputLabelProps={{ shrink: true }}
      />

      <Button
        type="submit"
        variant="contained"
        disabled={createTask.isLoading}
      >
        {createTask.isLoading ? 'Creating...' : 'Create Task'}
      </Button>
    </form>
  );
}
```

### 5.2 Error Handling Patterns

**Centralized Error Handler:**
```typescript
// api/error-handler.ts
import axios from 'axios';
import { toast } from 'react-hot-toast';

export function handleAPIError(error: unknown) {
  if (axios.isAxiosError(error)) {
    const status = error.response?.status;
    const detail = error.response?.data?.detail || 'An error occurred';

    switch (status) {
      case 400:
        toast.error(`Bad Request: ${detail}`);
        break;
      case 401:
        toast.error('Unauthorized. Please log in.');
        window.location.href = '/login';
        break;
      case 403:
        toast.error('You do not have permission to perform this action.');
        break;
      case 404:
        toast.error('Resource not found.');
        break;
      case 422:
        toast.error(`Validation Error: ${detail}`);
        break;
      case 429:
        toast.error('Too many requests. Please try again later.');
        break;
      case 500:
        toast.error('Server error. Please contact support.');
        break;
      default:
        toast.error(detail);
    }
  } else {
    toast.error('An unexpected error occurred');
    console.error(error);
  }
}

// Usage in hooks
export function useRiskScores() {
  return useQuery(
    ['risk-scores'],
    fetchRiskScores,
    {
      onError: handleAPIError  // Automatic error handling
    }
  );
}
```

### 5.3 Loading States

**Skeleton Loaders:**
```typescript
// components/skeletons/DashboardSkeleton.tsx
import { Skeleton, Grid, Card } from '@mui/material';

export function DashboardSkeleton() {
  return (
    <Grid container spacing={3}>
      {[1, 2, 3, 4].map((i) => (
        <Grid key={i} item xs={12} md={3}>
          <Card sx={{ p: 2 }}>
            <Skeleton variant="text" width="60%" />
            <Skeleton variant="rectangular" height={60} />
          </Card>
        </Grid>
      ))}
      <Grid item xs={12}>
        <Card sx={{ p: 2 }}>
          <Skeleton variant="rectangular" height={300} />
        </Card>
      </Grid>
    </Grid>
  );
}
```

### 5.4 Data Transformation

**Transform API Response to Chart Data:**
```typescript
// utils/chartTransforms.ts
import { RiskTrendData, ChartDataPoint } from '../types';

export function transformRiskTrendToChartData(
  apiData: RiskTrendData[]
): ChartDataPoint[] {
  return apiData.map(item => ({
    date: new Date(item.timestamp).toLocaleDateString(),
    value: item.risk_score,
    label: `Risk Score: ${item.risk_score.toFixed(1)}`,
  }));
}

// Usage
function RiskTrendChart() {
  const { data } = useRiskTrend();
  const chartData = data ? transformRiskTrendToChartData(data.trends) : [];

  return <LineChart data={chartData} />;
}
```

### 5.5 Caching Strategies

**React Query Cache Configuration:**
```typescript
// api/queryClient.ts
import { QueryClient } from 'react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Cache data for 5 minutes
      staleTime: 5 * 60 * 1000,
      // Keep unused data in cache for 10 minutes
      cacheTime: 10 * 60 * 1000,
      // Retry failed requests 3 times
      retry: 3,
      // Refetch on window focus
      refetchOnWindowFocus: true,
      // Don't refetch on mount if data is fresh
      refetchOnMount: false,
    },
  },
});

// Override for specific queries
export function useLiveAlerts() {
  return useQuery(
    ['live-alerts'],
    fetchAlerts,
    {
      staleTime: 0,  // Always fetch fresh
      refetchInterval: 5000,  // Poll every 5 seconds
    }
  );
}
```

---

## 6. ADDITIONAL RESOURCES

### 6.1 Documentation Links

**Official Docs:**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

**Wiki Documentation:**
- **API Status**: `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/00_API_STATUS_AND_ROADMAP.md`
- **Frontend Quick Start**: `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/00_FRONTEND_QUICK_START.md`
- **Phase B2 Capabilities**: `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/API_PHASE_B2_CAPABILITIES_2025-12-04.md`
- **Phase B3 Capabilities**: `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/API_PHASE_B3_CAPABILITIES_2025-12-04.md`
- **Phase B4 Capabilities**: `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/API_PHASE_B4_CAPABILITIES_2025-12-04.md`
- **Phase B5 Capabilities**: `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/API_PHASE_B5_CAPABILITIES_2025-12-04.md`

### 6.2 Development Environment Setup

**Prerequisites:**
```bash
# Node.js 18+ and npm
node --version  # v18.0.0+
npm --version   # 9.0.0+

# Install dependencies
npm install

# Environment variables
cp .env.example .env

# Edit .env
REACT_APP_API_BASE=http://localhost:8000
REACT_APP_DEFAULT_CUSTOMER_ID=demo
```

**Start Development Server:**
```bash
npm start
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Swagger Docs: http://localhost:8000/docs
```

### 6.3 Common Pitfalls & Solutions

| Pitfall | Solution |
|---------|----------|
| **Forgot `X-Customer-ID` header** | Create `apiClient` wrapper that auto-adds header |
| **CORS errors in development** | Use proxy in `package.json`: `"proxy": "http://localhost:8000"` |
| **Slow dashboard loads** | Use React Query caching + parallel requests |
| **Stale data after mutations** | Call `queryClient.invalidateQueries()` after mutations |
| **Type mismatches** | Generate types from OpenAPI spec using `openapi-typescript-codegen` |
| **Large bundle size** | Code-split routes with React.lazy() |

### 6.4 Performance Optimization Checklist

- [ ] Use React Query for data caching
- [ ] Implement pagination for large lists (>100 items)
- [ ] Lazy load routes with React.lazy()
- [ ] Memoize expensive computations with useMemo()
- [ ] Virtualize long lists with react-window
- [ ] Debounce search inputs (300ms)
- [ ] Use Suspense for code splitting
- [ ] Optimize images (WebP format, lazy loading)
- [ ] Monitor bundle size with webpack-bundle-analyzer

### 6.5 Testing Strategy

**Unit Tests (Jest + React Testing Library):**
```bash
npm test

# Coverage report
npm test -- --coverage
```

**Component Tests:**
```typescript
// RiskDashboard.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClientProvider } from 'react-query';
import { RiskDashboard } from './RiskDashboard';
import { queryClient } from '../api/queryClient';

test('displays risk dashboard data', async () => {
  render(
    <QueryClientProvider client={queryClient}>
      <RiskDashboard />
    </QueryClientProvider>
  );

  await waitFor(() => {
    expect(screen.getByText('Risk Dashboard')).toBeInTheDocument();
    expect(screen.getByText('150')).toBeInTheDocument(); // Total items
  });
});
```

**E2E Tests (Cypress):**
```javascript
// cypress/e2e/risk-dashboard.cy.ts
describe('Risk Dashboard', () => {
  it('loads and displays data', () => {
    cy.visit('/risk-dashboard');
    cy.contains('Risk Dashboard');
    cy.get('[data-testid="total-items"]').should('contain', '150');
  });
});
```

---

## 7. QUICK REFERENCE CHEAT SHEET

### API Endpoints by Phase

**Phase B2: Supply Chain**
```
GET  /api/v2/sbom/dashboard/summary
GET  /api/v2/sbom/components
POST /api/v2/sbom/components
GET  /api/v2/vendor-equipment/dashboard/supply-chain
GET  /api/v2/vendor-equipment/vendors
```

**Phase B3: Security Operations**
```
GET  /api/v2/threat-intel/dashboard/summary
GET  /api/v2/threat-intel/actors
GET  /api/v2/risk/dashboard/summary
GET  /api/v2/risk/scores
POST /api/v2/risk/scores
GET  /api/v2/remediation/dashboard/summary
GET  /api/v2/remediation/tasks
POST /api/v2/remediation/tasks
```

**Phase B4: Compliance & Monitoring**
```
GET  /api/v2/compliance/dashboard/summary
GET  /api/v2/compliance/controls
POST /api/v2/compliance/controls
GET  /api/v2/scanning/dashboard/summary
GET  /api/v2/scanning/scans
POST /api/v2/scanning/scans
GET  /api/v2/alerts/dashboard/summary
GET  /api/v2/alerts
POST /api/v2/alerts
GET  /api/v2/alerts/stream  # SSE real-time
```

**Phase B5: Analytics & Prioritization**
```
GET  /api/v2/economic-impact/dashboard/summary
POST /api/v2/economic-impact/roi/calculate
GET  /api/v2/demographics/dashboard/baseline
GET  /api/v2/demographics/population/summary
GET  /api/v2/prioritization/dashboard/summary
GET  /api/v2/prioritization/now/items
GET  /api/v2/prioritization/next/items
GET  /api/v2/prioritization/never/items
POST /api/v2/prioritization/score/calculate
```

### Common HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | OK | Success |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Check request body/headers |
| 401 | Unauthorized | Redirect to login |
| 403 | Forbidden | Show permission error |
| 404 | Not Found | Show "not found" message |
| 422 | Validation Error | Show field-specific errors |
| 429 | Too Many Requests | Implement retry with backoff |
| 500 | Server Error | Contact support |

### TypeScript Type Generation

```bash
# Install OpenAPI generator
npm install -D openapi-typescript-codegen

# Generate types
npx openapi-typescript-codegen \
  --input http://localhost:8000/openapi.json \
  --output ./src/types/api \
  --client axios

# Use generated types
import { DashboardSummaryResponse } from './types/api';
```

---

## Appendix: Complete Component Example

**Full-Featured Risk Dashboard Component:**

```typescript
// pages/RiskDashboard.tsx
import { useState } from 'react';
import { useQuery, useQueryClient } from 'react-query';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  CircularProgress,
  Alert,
  Box,
  Tabs,
  Tab,
} from '@mui/material';
import { Refresh as RefreshIcon } from '@mui/icons-material';
import { apiClient } from '../api/axios-client';
import { useCustomerId } from '../hooks/useCustomerId';
import { RiskTrendChart } from '../components/charts/RiskTrendChart';
import { RiskMatrix } from '../components/charts/RiskMatrix';
import { HighRiskItemsTable } from '../components/tables/HighRiskItemsTable';
import { StatCard } from '../components/cards/StatCard';

interface RiskDashboardData {
  customer_id: string;
  total_items: number;
  high_risk_count: number;
  critical_risk_count: number;
  average_risk_score: number;
  risk_distribution: Record<string, number>;
  trend: 'increasing' | 'stable' | 'decreasing';
  trends: Array<{ timestamp: string; risk_score: number }>;
  risk_matrix: Array<{ likelihood: number; impact: number; count: number }>;
  high_risk_items: Array<any>;
}

export function RiskDashboard() {
  const customerId = useCustomerId();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState(0);

  // Fetch dashboard data
  const { data, isLoading, error, refetch, isFetching } = useQuery<RiskDashboardData>(
    ['risk-dashboard', customerId],
    async () => {
      const response = await apiClient.get('/api/v2/risk/dashboard/summary');
      return response.data;
    },
    {
      staleTime: 5 * 60 * 1000,
      refetchInterval: 60 * 1000,
      retry: 3,
    }
  );

  const handleRefresh = () => {
    queryClient.invalidateQueries(['risk-dashboard']);
    refetch();
  };

  if (isLoading) {
    return (
      <Container maxWidth="xl" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="xl" sx={{ mt: 4 }}>
        <Alert severity="error">Failed to load risk dashboard. Please try again.</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Risk Dashboard
        </Typography>
        <Button
          variant="outlined"
          startIcon={isFetching ? <CircularProgress size={16} /> : <RefreshIcon />}
          onClick={handleRefresh}
          disabled={isFetching}
        >
          Refresh
        </Button>
      </Box>

      {/* KPI Cards */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} md={3}>
          <StatCard
            title="Total Risk Items"
            value={data.total_items}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatCard
            title="High Risk"
            value={data.high_risk_count}
            color="warning"
            trend={data.trend}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatCard
            title="Critical Risk"
            value={data.critical_risk_count}
            color="error"
            trend={data.trend}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatCard
            title="Average Score"
            value={data.average_risk_score.toFixed(1)}
            subtitle="/10"
            color={data.average_risk_score >= 7 ? 'error' : 'info'}
          />
        </Grid>
      </Grid>

      {/* Tabs */}
      <Box mb={3}>
        <Tabs value={activeTab} onChange={(e, v) => setActiveTab(v)}>
          <Tab label="Overview" />
          <Tab label="Risk Matrix" />
          <Tab label="High Risk Items" />
        </Tabs>
      </Box>

      {/* Tab Panels */}
      {activeTab === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Risk Trend (30 Days)
                </Typography>
                <RiskTrendChart data={data.trends} />
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Risk Distribution
                </Typography>
                {/* Pie chart or bar chart */}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeTab === 1 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Risk Matrix (Likelihood × Impact)
            </Typography>
            <RiskMatrix cells={data.risk_matrix} />
          </CardContent>
        </Card>
      )}

      {activeTab === 2 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              High Risk Items Requiring Attention
            </Typography>
            <HighRiskItemsTable items={data.high_risk_items} />
          </CardContent>
        </Card>
      )}
    </Container>
  );
}
```

---

**END OF DOCUMENT**

**This guide has covered:**
✅ Backend architecture and API discovery
✅ Authentication and data structures
✅ Common frustrations and solutions
✅ Required tools and libraries
✅ Component architecture and examples
✅ Complete sample code with error handling
✅ Performance optimization strategies
✅ Testing approaches
✅ Quick reference cheat sheet

**Next Steps:**
1. Clone the repository
2. Install dependencies: `npm install`
3. Start backend: Verify http://localhost:8000/docs works
4. Start frontend: `npm start`
5. Test API calls with `X-Customer-ID: demo`
6. Build your first dashboard using examples above

**Questions? Check:**
- Swagger UI: http://localhost:8000/docs
- Wiki: `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/`
- This guide: Section-specific examples above
