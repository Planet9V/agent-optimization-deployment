# AEON Frontend Developer Cheatsheet

**File:** FRONTEND_CHEATSHEET_2025-12-04.md
**Created:** 2025-12-04 22:30:00 UTC
**Purpose:** Copy-Paste Ready Examples

---

## Quick Start (5 Minutes)

### 1. API Base URL

```bash
export API_BASE=http://localhost:8000
```

### 2. Test Connection

```bash
curl $API_BASE/health
# Expected: {"status":"healthy"}
```

### 3. Your First API Call

```bash
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/sbom/dashboard/summary
```

---

## Environment Variables

Copy to `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_DEFAULT_CUSTOMER_ID=demo-customer
NEXT_PUBLIC_ENV=development
```

---

## Base API Client (Copy Entire File)

**File:** `src/services/api.ts`

```typescript
import axios, { AxiosInstance } from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;
  private customerId: string;

  constructor() {
    this.customerId = process.env.NEXT_PUBLIC_DEFAULT_CUSTOMER_ID || 'demo-customer';

    this.client = axios.create({
      baseURL: API_BASE,
      timeout: 30000,
      headers: { 'Content-Type': 'application/json' },
    });

    this.client.interceptors.request.use((config) => {
      config.headers['X-Customer-ID'] = this.customerId;
      return config;
    });

    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error.response?.data?.detail || error.message);
        return Promise.reject(error);
      }
    );
  }

  async get<T>(url: string): Promise<T> {
    const response = await this.client.get<T>(url);
    return response.data;
  }

  async post<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.post<T>(url, data);
    return response.data;
  }

  async put<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.put<T>(url, data);
    return response.data;
  }

  async patch<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.patch<T>(url, data);
    return response.data;
  }

  async delete<T>(url: string): Promise<T> {
    const response = await this.client.delete<T>(url);
    return response.data;
  }
}

export const api = new ApiClient();
```

---

## Curl Commands (All 11 APIs)

### E03: SBOM Analysis

```bash
# Dashboard
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/sbom/dashboard/summary

# List SBOMs
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/sbom/sboms?limit=10

# Search components
curl -H "X-Customer-ID: demo-customer" \
  "$API_BASE/api/v2/sbom/components/search?query=log4j&limit=10"

# Critical vulnerabilities
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/sbom/vulnerabilities/critical
```

### E04: Threat Intelligence

```bash
# Dashboard
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/threat-intel/dashboard/summary

# Threat actors
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/threat-intel/actors?limit=10

# Search threat actors
curl -H "X-Customer-ID: demo-customer" \
  "$API_BASE/api/v2/threat-intel/actors/search?query=APT29"

# Active campaigns
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/threat-intel/campaigns/active
```

### E05: Risk Scoring

```bash
# Dashboard
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/risk/dashboard/summary

# Risk scores
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/risk/scores?limit=10

# Calculate risk (POST)
curl -X POST -H "X-Customer-ID: demo-customer" \
  -H "Content-Type: application/json" \
  -d '{"entity_id":"asset-123","entity_type":"asset"}' \
  $API_BASE/api/v2/risk/scores/calculate
```

### E06: Remediation

```bash
# Dashboard
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/remediation/dashboard/summary

# Tasks
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/remediation/tasks?limit=10

# Overdue tasks
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/remediation/tasks/overdue

# Create task (POST)
curl -X POST -H "X-Customer-ID: demo-customer" \
  -H "Content-Type: application/json" \
  -d '{"title":"Fix CVE-2024-1234","priority":"high"}' \
  $API_BASE/api/v2/remediation/tasks
```

### E07: Compliance

```bash
# Dashboard
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/compliance/dashboard/summary

# Frameworks
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/compliance/frameworks

# Controls
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/compliance/controls?limit=10

# Gap analysis (POST)
curl -X POST -H "X-Customer-ID: demo-customer" \
  -H "Content-Type: application/json" \
  -d '{"framework":"NIST_CSF"}' \
  $API_BASE/api/v2/compliance/gap-analysis
```

### E08: Scanning

```bash
# Dashboard
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/scanning/dashboard/summary

# Scans
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/scanning/scans?limit=10

# Create scan (POST)
curl -X POST -H "X-Customer-ID: demo-customer" \
  -H "Content-Type: application/json" \
  -d '{"name":"Weekly Scan","scanner_integration":"nessus"}' \
  $API_BASE/api/v2/scanning/scans
```

### E09: Alerts

```bash
# Dashboard
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/alerts/dashboard/summary

# Active alerts
curl -H "X-Customer-ID: demo-customer" \
  "$API_BASE/api/v2/alerts?status=new&limit=10"

# Acknowledge alert (PATCH)
curl -X PATCH -H "X-Customer-ID: demo-customer" \
  -H "Content-Type: application/json" \
  -d '{"acknowledged_by":"user-123"}' \
  $API_BASE/api/v2/alerts/alert-123/acknowledge
```

### E10: Economic Impact

```bash
# Dashboard
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/economic-impact/dashboard/summary

# ROI summary
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/economic-impact/roi/summary

# Calculate ROI (POST)
curl -X POST -H "X-Customer-ID: demo-customer" \
  -H "Content-Type: application/json" \
  -d '{"investment_name":"SIEM","initial_investment":100000,"annual_benefits":50000}' \
  $API_BASE/api/v2/economic-impact/roi/calculate
```

### E11: Demographics

```bash
# Dashboard
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/demographics/dashboard/summary

# Baseline metrics (Psychohistory)
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/demographics/dashboard/baseline

# Workforce composition
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/demographics/workforce/composition
```

### E12: Prioritization

```bash
# Dashboard
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/prioritization/dashboard/summary

# NOW items (urgent)
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/prioritization/now/items?limit=20

# NEXT items (planned)
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/prioritization/next/items?limit=20

# Calculate priority (POST)
curl -X POST -H "X-Customer-ID: demo-customer" \
  -H "Content-Type: application/json" \
  -d '{"entity_type":"vulnerability","entity_id":"CVE-2024-1234"}' \
  $API_BASE/api/v2/prioritization/score/calculate
```

### E15: Vendor Equipment

```bash
# Dashboard
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/vendor-equipment/dashboard/supply-chain

# Search vendors
curl -H "X-Customer-ID: demo-customer" \
  "$API_BASE/api/v2/vendor-equipment/vendors/search?query=cisco"

# High-risk vendors
curl -H "X-Customer-ID: demo-customer" \
  $API_BASE/api/v2/vendor-equipment/vendors/high-risk

# Equipment approaching EOL
curl -H "X-Customer-ID: demo-customer" \
  "$API_BASE/api/v2/vendor-equipment/equipment/approaching-eol?days=180"
```

---

## React Hooks (Copy & Paste)

### Dashboard Hook

```typescript
// src/hooks/useDashboard.ts
import { useQuery } from '@tanstack/react-query';
import { api } from '@/services/api';

export function useUnifiedDashboard() {
  return useQuery({
    queryKey: ['unified-dashboard'],
    queryFn: async () => {
      const [sbom, threat, risk, compliance, alerts, economic, demographics, priority] =
        await Promise.all([
          api.get('/api/v2/sbom/dashboard/summary'),
          api.get('/api/v2/threat-intel/dashboard/summary'),
          api.get('/api/v2/risk/dashboard/summary'),
          api.get('/api/v2/compliance/dashboard/summary'),
          api.get('/api/v2/alerts/dashboard/summary'),
          api.get('/api/v2/economic-impact/dashboard/summary'),
          api.get('/api/v2/demographics/dashboard/baseline'),
          api.get('/api/v2/prioritization/dashboard/summary'),
        ]);

      return { sbom, threat, risk, compliance, alerts, economic, demographics, priority };
    },
    refetchInterval: 60000, // Refresh every minute
  });
}
```

### SBOM Hook

```typescript
// src/hooks/useSBOM.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/services/api';

export function useSBOMs(limit = 20, offset = 0) {
  return useQuery({
    queryKey: ['sboms', limit, offset],
    queryFn: () => api.get(`/api/v2/sbom/sboms?limit=${limit}&offset=${offset}`),
  });
}

export function useSBOMDetail(sbomId: string) {
  return useQuery({
    queryKey: ['sbom', sbomId],
    queryFn: () => api.get(`/api/v2/sbom/sboms/${sbomId}`),
    enabled: !!sbomId,
  });
}

export function useComponentSearch(query: string) {
  return useQuery({
    queryKey: ['components', query],
    queryFn: () => api.get(`/api/v2/sbom/components/search?query=${query}&limit=20`),
    enabled: query.length > 2,
  });
}
```

### Threat Intelligence Hook

```typescript
// src/hooks/useThreatIntel.ts
import { useQuery } from '@tanstack/react-query';
import { api } from '@/services/api';

export function useThreatActors(limit = 20) {
  return useQuery({
    queryKey: ['threat-actors', limit],
    queryFn: () => api.get(`/api/v2/threat-intel/actors?limit=${limit}`),
  });
}

export function useThreatActorSearch(query: string) {
  return useQuery({
    queryKey: ['threat-actors', 'search', query],
    queryFn: () => api.get(`/api/v2/threat-intel/actors/search?query=${query}`),
    enabled: query.length > 2,
  });
}

export function useActiveCampaigns() {
  return useQuery({
    queryKey: ['campaigns', 'active'],
    queryFn: () => api.get('/api/v2/threat-intel/campaigns/active'),
    refetchInterval: 300000, // Refresh every 5 minutes
  });
}
```

### Remediation Hook

```typescript
// src/hooks/useRemediation.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/services/api';

export function useRemediationTasks(status?: string) {
  return useQuery({
    queryKey: ['remediation-tasks', status],
    queryFn: () => {
      const url = status
        ? `/api/v2/remediation/tasks?status=${status}`
        : '/api/v2/remediation/tasks';
      return api.get(url);
    },
  });
}

export function useCreateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (task: CreateTaskRequest) =>
      api.post('/api/v2/remediation/tasks', task),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['remediation-tasks'] });
    },
  });
}

export function useUpdateTaskStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ taskId, status }: { taskId: string; status: string }) =>
      api.patch(`/api/v2/remediation/tasks/${taskId}/status`, { status }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['remediation-tasks'] });
    },
  });
}
```

### Alert Hook

```typescript
// src/hooks/useAlerts.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/services/api';

export function useAlerts(status?: string) {
  return useQuery({
    queryKey: ['alerts', status],
    queryFn: () => {
      const url = status
        ? `/api/v2/alerts?status=${status}&limit=50`
        : '/api/v2/alerts?limit=50';
      return api.get(url);
    },
    refetchInterval: 30000, // Refresh every 30 seconds
  });
}

export function useAcknowledgeAlert() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ alertId, userId }: { alertId: string; userId: string }) =>
      api.patch(`/api/v2/alerts/${alertId}/acknowledge`, { acknowledged_by: userId }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    },
  });
}
```

### Prioritization Hook

```typescript
// src/hooks/usePrioritization.ts
import { useQuery, useMutation } from '@tanstack/react-query';
import { api } from '@/services/api';

export function useNowItems() {
  return useQuery({
    queryKey: ['priority', 'NOW'],
    queryFn: () => api.get('/api/v2/prioritization/now/items?limit=50'),
  });
}

export function useNextItems() {
  return useQuery({
    queryKey: ['priority', 'NEXT'],
    queryFn: () => api.get('/api/v2/prioritization/next/items?limit=50'),
  });
}

export function useCalculatePriority() {
  return useMutation({
    mutationFn: (request: PriorityScoreRequest) =>
      api.post('/api/v2/prioritization/score/calculate', request),
  });
}
```

---

## React Components (Copy & Paste)

### Dashboard Component

```typescript
// src/components/Dashboard.tsx
import { useUnifiedDashboard } from '@/hooks/useDashboard';

export function Dashboard() {
  const { data, isLoading, error } = useUnifiedDashboard();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <DashboardCard title="SBOM Analysis" data={data.sbom} />
      <DashboardCard title="Threat Intel" data={data.threat} />
      <DashboardCard title="Risk Scoring" data={data.risk} />
      <DashboardCard title="Compliance" data={data.compliance} />
      <DashboardCard title="Alerts" data={data.alerts} />
      <DashboardCard title="Economic Impact" data={data.economic} />
      <DashboardCard title="Demographics" data={data.demographics} />
      <DashboardCard title="Prioritization" data={data.priority} />
    </div>
  );
}

function DashboardCard({ title, data }: { title: string; data: any }) {
  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <pre className="text-sm">{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
```

### Search Component

```typescript
// src/components/ComponentSearch.tsx
import { useState } from 'react';
import { useComponentSearch } from '@/hooks/useSBOM';
import { useDebounce } from '@/hooks/useDebounce';

export function ComponentSearch() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);
  const { data, isLoading } = useComponentSearch(debouncedQuery);

  return (
    <div>
      <input
        type="text"
        placeholder="Search components..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full px-4 py-2 border rounded"
      />

      {isLoading && <p>Loading...</p>}

      {data && (
        <ul className="mt-4 space-y-2">
          {data.map((component: any) => (
            <li key={component.component_id} className="p-2 border rounded">
              <div className="font-semibold">{component.name} {component.version}</div>
              <div className="text-sm text-gray-600">
                {component.vulnerability_count} vulnerabilities
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### Alert List Component

```typescript
// src/components/AlertList.tsx
import { useAlerts, useAcknowledgeAlert } from '@/hooks/useAlerts';

export function AlertList() {
  const { data: alerts, isLoading } = useAlerts('new');
  const acknowledgeMutation = useAcknowledgeAlert();

  const handleAcknowledge = (alertId: string) => {
    acknowledgeMutation.mutate({ alertId, userId: 'current-user' });
  };

  if (isLoading) return <LoadingSpinner />;

  return (
    <div className="space-y-2">
      {alerts?.map((alert: any) => (
        <div key={alert.alert_id} className="p-4 border rounded">
          <div className="flex justify-between items-start">
            <div>
              <h4 className="font-semibold">{alert.title}</h4>
              <p className="text-sm text-gray-600">{alert.description}</p>
              <div className="mt-2">
                <SeverityBadge severity={alert.severity} />
                <span className="ml-2 text-xs">{alert.created_at}</span>
              </div>
            </div>
            <button
              onClick={() => handleAcknowledge(alert.alert_id)}
              className="px-3 py-1 bg-blue-500 text-white rounded"
            >
              Acknowledge
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
```

### NOW-NEXT-NEVER Component

```typescript
// src/components/PriorityMatrix.tsx
import { useNowItems, useNextItems } from '@/hooks/usePrioritization';

export function PriorityMatrix() {
  const { data: nowItems } = useNowItems();
  const { data: nextItems } = useNextItems();

  return (
    <div className="grid grid-cols-2 gap-4">
      <PriorityColumn title="NOW (Urgent)" items={nowItems} color="red" />
      <PriorityColumn title="NEXT (Planned)" items={nextItems} color="yellow" />
    </div>
  );
}

function PriorityColumn({ title, items, color }: any) {
  return (
    <div className={`border-2 border-${color}-500 rounded-lg p-4`}>
      <h3 className="text-lg font-bold mb-4">{title}</h3>
      <ul className="space-y-2">
        {items?.map((item: any) => (
          <li key={item.item_id} className="p-2 bg-gray-50 rounded">
            <div className="font-semibold">{item.entity_name}</div>
            <div className="text-sm">Score: {item.priority_score}/100</div>
            {item.sla_status === 'breached' && (
              <span className="text-red-600 text-xs">SLA BREACHED</span>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## Utility Components

### Loading Spinner

```typescript
// src/components/LoadingSpinner.tsx
export function LoadingSpinner() {
  return (
    <div className="flex justify-center items-center p-8">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>
  );
}
```

### Error Message

```typescript
// src/components/ErrorMessage.tsx
export function ErrorMessage({ error }: { error: any }) {
  return (
    <div className="p-4 bg-red-50 border border-red-200 rounded">
      <h4 className="font-semibold text-red-800">Error</h4>
      <p className="text-sm text-red-600">
        {error?.response?.data?.detail || error?.message || 'An error occurred'}
      </p>
    </div>
  );
}
```

### Severity Badge

```typescript
// src/components/SeverityBadge.tsx
export function SeverityBadge({ severity }: { severity: string }) {
  const colors = {
    critical: 'bg-red-600 text-white',
    high: 'bg-orange-500 text-white',
    medium: 'bg-yellow-500 text-black',
    low: 'bg-green-500 text-white',
    info: 'bg-blue-500 text-white',
  };

  return (
    <span className={`px-2 py-1 text-xs rounded ${colors[severity] || 'bg-gray-500'}`}>
      {severity.toUpperCase()}
    </span>
  );
}
```

### Debounce Hook

```typescript
// src/hooks/useDebounce.ts
import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}
```

---

## TypeScript Interfaces (Copy All)

```typescript
// src/types/api.ts

// SBOM Types
export interface SBOM {
  sbom_id: string;
  customer_id: string;
  name: string;
  version: string;
  format: 'cyclonedx' | 'spdx' | 'custom';
  component_count: number;
  vulnerability_count: number;
  risk_score: number;
  created_at: string;
}

export interface SoftwareComponent {
  component_id: string;
  sbom_id: string;
  name: string;
  version: string;
  purl?: string;
  vulnerability_count: number;
  max_cvss_score: number;
  license?: string;
}

export interface Vulnerability {
  cve_id: string;
  cvss_v3_score: number;
  severity: 'none' | 'low' | 'medium' | 'high' | 'critical';
  epss_score?: number;
  cisa_kev: boolean;
  published_date: string;
  fixed_version?: string;
}

// Threat Intelligence Types
export interface ThreatActor {
  threat_actor_id: string;
  name: string;
  aliases: string[];
  actor_type: 'apt' | 'criminal' | 'hacktivist' | 'state_sponsored' | 'insider';
  motivation: 'espionage' | 'financial' | 'disruption' | 'destruction';
  target_sectors: string[];
  ttps: string[];
  threat_score: number;
  is_active: boolean;
  customer_id: string;
}

export interface Campaign {
  campaign_id: string;
  name: string;
  threat_actor_id: string;
  start_date: string;
  end_date?: string;
  status: 'active' | 'completed' | 'dormant';
  target_sectors: string[];
  ttps: string[];
  severity: 'low' | 'medium' | 'high' | 'critical';
}

// Risk Scoring Types
export interface RiskScore {
  entity_id: string;
  customer_id: string;
  overall_risk_score: number;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  vulnerability_score: number;
  threat_score: number;
  exposure_score: number;
  impact_score: number;
  risk_trend: 'improving' | 'stable' | 'degrading';
  calculated_at: string;
}

// Remediation Types
export interface RemediationTask {
  task_id: string;
  customer_id: string;
  title: string;
  description: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  status: 'open' | 'in_progress' | 'pending_verification' | 'verified' | 'closed';
  assigned_to?: string;
  sla_deadline: string;
  sla_status: 'within_sla' | 'at_risk' | 'breached';
  created_at: string;
  updated_at: string;
}

// Compliance Types
export interface ComplianceControl {
  control_id: string;
  customer_id: string;
  framework: 'NIST_CSF' | 'ISO_27001' | 'SOC2' | 'PCI_DSS' | 'NERC_CIP';
  control_number: string;
  title: string;
  description: string;
  implementation_status: 'not_implemented' | 'partial' | 'implemented';
  compliance_status: 'compliant' | 'non_compliant' | 'partially_compliant';
  evidence_count: number;
}

// Alert Types
export interface Alert {
  alert_id: string;
  customer_id: string;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  status: 'new' | 'acknowledged' | 'in_progress' | 'resolved' | 'closed';
  source: string;
  entity_type: string;
  entity_id: string;
  sla_deadline?: string;
  sla_status: 'within_sla' | 'at_risk' | 'breached';
  created_at: string;
  acknowledged_at?: string;
  resolved_at?: string;
}

// Economic Impact Types
export interface ROICalculation {
  investment_id: string;
  customer_id: string;
  name: string;
  category: 'security_tools' | 'infrastructure' | 'personnel' | 'training';
  initial_investment: number;
  annual_benefits: number;
  annual_costs: number;
  roi_percentage: number;
  npv: number;
  irr: number;
  payback_period_months: number;
  risk_adjusted_roi: number;
  confidence_score: number;
}

// Demographics Types
export interface BaselineMetrics {
  customer_id: string;
  population_stability_index: number;
  role_diversity_score: number;
  skill_concentration_risk: number;
  succession_coverage: number;
  insider_threat_baseline: number;
  calculated_at: string;
}

// Prioritization Types
export interface PriorityItem {
  item_id: string;
  customer_id: string;
  entity_type: 'vulnerability' | 'remediation_task' | 'asset' | 'threat' | 'compliance_gap';
  entity_id: string;
  entity_name: string;
  priority_category: 'NOW' | 'NEXT' | 'NEVER';
  priority_score: number;
  deadline: string | null;
  sla_status: 'within_sla' | 'at_risk' | 'breached';
  is_now: boolean;
  is_sla_at_risk: boolean;
  urgency_score: number;
  risk_score: number;
  impact_score: number;
}

// Request Types
export interface CreateTaskRequest {
  title: string;
  description: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  assigned_to?: string;
  sla_deadline?: string;
}

export interface PriorityScoreRequest {
  entity_type: string;
  entity_id: string;
  entity_name: string;
  urgency_factors: Array<{
    factor_type: string;
    weight: number;
    value: number;
    description: string;
  }>;
  risk_factors: Array<{
    factor_type: string;
    weight: number;
    value: number;
    description: string;
  }>;
  impact_factors?: Array<{
    factor_type: string;
    weight: number;
    value: number;
    description: string;
  }>;
}
```

---

## Testing Script

Save as `test-apis.sh`:

```bash
#!/bin/bash

API_BASE="http://localhost:8000"
CUSTOMER_ID="demo-customer"

echo "Testing AEON APIs..."
echo ""

# Test each API
apis=(
  "sbom/dashboard/summary"
  "threat-intel/dashboard/summary"
  "risk/dashboard/summary"
  "remediation/dashboard/summary"
  "compliance/dashboard/summary"
  "scanning/dashboard/summary"
  "alerts/dashboard/summary"
  "economic-impact/dashboard/summary"
  "demographics/dashboard/summary"
  "prioritization/dashboard/summary"
  "vendor-equipment/dashboard/supply-chain"
)

for api in "${apis[@]}"; do
  echo "Testing /api/v2/$api"
  curl -s -H "X-Customer-ID: $CUSTOMER_ID" "$API_BASE/api/v2/$api" | jq -r '.success' || echo "FAILED"
  echo ""
done

echo "Testing complete!"
```

Run with:
```bash
chmod +x test-apis.sh
./test-apis.sh
```

---

## Quick Reference Table

| API | Dashboard Endpoint | Key Features |
|-----|-------------------|--------------|
| **E03 SBOM** | `/api/v2/sbom/dashboard/summary` | Components, vulnerabilities, EPSS |
| **E04 Threat Intel** | `/api/v2/threat-intel/dashboard/summary` | APT actors, campaigns, MITRE ATT&CK |
| **E05 Risk** | `/api/v2/risk/dashboard/summary` | Risk scores, trends, breakdowns |
| **E06 Remediation** | `/api/v2/remediation/dashboard/summary` | Tasks, SLA tracking, plans |
| **E07 Compliance** | `/api/v2/compliance/dashboard/summary` | Frameworks, controls, gaps |
| **E08 Scanning** | `/api/v2/scanning/dashboard/summary` | Scans, integrations, results |
| **E09 Alerts** | `/api/v2/alerts/dashboard/summary` | Alerts, rules, notifications |
| **E10 Economic** | `/api/v2/economic-impact/dashboard/summary` | ROI, costs, savings |
| **E11 Demographics** | `/api/v2/demographics/dashboard/summary` | Workforce, baseline metrics |
| **E12 Priority** | `/api/v2/prioritization/dashboard/summary` | NOW-NEXT-NEVER, scoring |
| **E15 Vendor** | `/api/v2/vendor-equipment/dashboard/supply-chain` | Vendors, equipment, EOL |

---

**Generated**: 2025-12-04 22:30:00 UTC
**AEON Digital Twin Cybersecurity Platform**
**Copy, paste, code!**
