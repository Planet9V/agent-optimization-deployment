# AEON Frontend Developer Complete Guide

**File:** FRONTEND_DEVELOPER_GUIDE_2025-12-04.md
**Created:** 2025-12-04 22:30:00 UTC
**Version:** 1.0.0
**For:** React/Next.js Frontend Developers NEW to AEON Backend

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Development Environment Setup](#2-development-environment-setup)
3. [API Integration Guide](#3-api-integration-guide)
4. [Available APIs (11 APIs, 315+ Endpoints)](#4-available-apis)
5. [Authentication & Headers](#5-authentication--headers)
6. [Common Patterns](#6-common-patterns)
7. [What Needs To Be Built](#7-what-needs-to-be-built)
8. [Quick Reference](#8-quick-reference)

---

## 1. Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Frontend (You Build This)                              │
│  React/Next.js @ localhost:3000                         │
│  Container: aeon-saas-dev:3000                          │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ HTTP/REST API Calls
                 ↓
┌─────────────────────────────────────────────────────────┐
│  Backend API Server (Running)                           │
│  FastAPI @ localhost:8000                               │
│  Container: ner11-gold-api:8000                         │
│  • 315+ REST endpoints across 11 APIs                   │
│  • Multi-tenant isolation via X-Customer-ID             │
│  • Customer context management                          │
└────────────────┬────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ↓                 ↓
┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │   Qdrant     │
│  Port: 5432  │  │   Vector DB  │
│  aeon-db     │  │   Port: 6333 │
└──────────────┘  └──────────────┘
```

### Container Details

| Container | Port | Purpose | Status |
|-----------|------|---------|--------|
| **aeon-saas-dev** | 3000 | Frontend React/Next.js app | ⏳ TO BUILD |
| **ner11-gold-api** | 8000 | Backend FastAPI server | ✅ RUNNING |
| **aeon-postgres-dev** | 5432 | PostgreSQL database | ✅ RUNNING |
| **qdrant** | 6333 | Vector database | ✅ RUNNING |

### Key Concepts

**Multi-Tenancy**: Every API call requires `X-Customer-ID` header for data isolation.

**API Phases**:
- **Phase B2**: SBOM Analysis, Vendor Equipment (65 endpoints)
- **Phase B3**: Threat Intel, Risk Scoring, Remediation (82 endpoints)
- **Phase B4**: Compliance, Scanning, Alerts (90 endpoints)
- **Phase B5**: Economic Impact, Demographics, Prioritization (78 endpoints)

---

## 2. Development Environment Setup

### Access the Frontend

```bash
# Frontend URL (when running)
http://localhost:3000

# Backend API URL (currently running)
http://localhost:8000
```

### Frontend Folder Structure

```
/1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1/
├── src/                          # TO CREATE
│   ├── components/               # React components
│   │   ├── dashboard/
│   │   ├── sbom/
│   │   ├── threats/
│   │   ├── compliance/
│   │   └── shared/
│   ├── pages/                    # Page components
│   ├── hooks/                    # Custom React hooks
│   │   ├── useApi.ts
│   │   ├── useSBOM.ts
│   │   ├── useThreatIntel.ts
│   │   └── useCompliance.ts
│   ├── services/                 # API service layer
│   │   ├── api.ts                # Base API client
│   │   ├── sbom.ts
│   │   ├── threatIntel.ts
│   │   └── compliance.ts
│   ├── types/                    # TypeScript definitions
│   │   ├── sbom.ts
│   │   ├── threat.ts
│   │   └── compliance.ts
│   └── utils/
│       ├── auth.ts
│       └── constants.ts
├── public/
├── package.json                  # Dependencies
├── tsconfig.json                 # TypeScript config
├── next.config.js                # Next.js config
└── .env.local                    # Environment variables
```

### Environment Variables

Create `.env.local`:

```bash
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=30000

# Multi-tenancy
NEXT_PUBLIC_DEFAULT_CUSTOMER_ID=demo-customer

# Development
NEXT_PUBLIC_ENV=development
NEXT_PUBLIC_DEBUG=true
```

### Install Dependencies

```bash
cd /1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1

# Install React/Next.js dependencies
npm install next react react-dom
npm install --save-dev typescript @types/react @types/node

# Install API client
npm install axios

# Install UI libraries (recommended)
npm install @tanstack/react-query  # Data fetching
npm install zustand                # State management
npm install recharts               # Charts
npm install @headlessui/react      # UI components
npm install clsx tailwind-merge    # Utilities
```

---

## 3. API Integration Guide

### Base API Client Setup

Create `src/services/api.ts`:

```typescript
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;
  private customerId: string;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Get customer ID from environment or localStorage
    this.customerId = process.env.NEXT_PUBLIC_DEFAULT_CUSTOMER_ID || 'demo-customer';

    // Request interceptor - add X-Customer-ID to every request
    this.client.interceptors.request.use((config) => {
      config.headers['X-Customer-ID'] = this.customerId;
      return config;
    });

    // Response interceptor - handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', {
          url: error.config?.url,
          status: error.response?.status,
          message: error.response?.data?.detail || error.message,
        });
        return Promise.reject(error);
      }
    );
  }

  setCustomerId(customerId: string) {
    this.customerId = customerId;
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }
}

export const apiClient = new ApiClient();
```

### React Query Setup (Recommended)

Create `src/services/queryClient.ts`:

```typescript
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});
```

In `_app.tsx` or `layout.tsx`:

```typescript
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '@/services/queryClient';

export default function App({ Component, pageProps }) {
  return (
    <QueryClientProvider client={queryClient}>
      <Component {...pageProps} />
    </QueryClientProvider>
  );
}
```

---

## 4. Available APIs

### Phase B2: Supply Chain (65 Endpoints)

#### E03: SBOM Analysis API (32 endpoints)
**Base Path:** `/api/v2/sbom`

**Key Endpoints:**
```typescript
// Dashboard
GET /api/v2/sbom/dashboard/summary

// SBOMs
GET /api/v2/sbom/sboms                    // List all SBOMs
GET /api/v2/sbom/sboms/{sbom_id}          // Get SBOM details
POST /api/v2/sbom/sboms                   // Upload new SBOM
GET /api/v2/sbom/sboms/{sbom_id}/risk-summary

// Components
GET /api/v2/sbom/components               // List components
GET /api/v2/sbom/components/search?query=log4j
GET /api/v2/sbom/components/{id}/vulnerabilities

// Vulnerabilities
GET /api/v2/sbom/vulnerabilities/critical
GET /api/v2/sbom/vulnerabilities/epss-prioritized
GET /api/v2/sbom/vulnerabilities/{cve_id}
```

**TypeScript Types:**
```typescript
interface SBOM {
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

interface SoftwareComponent {
  component_id: string;
  sbom_id: string;
  name: string;
  version: string;
  purl?: string;  // Package URL: pkg:npm/lodash@4.17.21
  vulnerability_count: number;
  max_cvss_score: number;
  license?: string;
}

interface Vulnerability {
  cve_id: string;
  cvss_v3_score: number;
  severity: 'none' | 'low' | 'medium' | 'high' | 'critical';
  epss_score?: number;      // Exploitation probability (0-1)
  cisa_kev: boolean;        // Known Exploited Vulnerability
  published_date: string;
  fixed_version?: string;
}
```

**React Hook Example:**
```typescript
// src/hooks/useSBOM.ts
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/services/api';

export function useSBOMs() {
  return useQuery({
    queryKey: ['sboms'],
    queryFn: () => apiClient.get<SBOM[]>('/api/v2/sbom/sboms'),
  });
}

export function useSBOMDashboard() {
  return useQuery({
    queryKey: ['sbom-dashboard'],
    queryFn: () => apiClient.get('/api/v2/sbom/dashboard/summary'),
    refetchInterval: 60000, // Refresh every minute
  });
}

// Component usage:
function SBOMDashboard() {
  const { data, isLoading, error } = useSBOMDashboard();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div>
      <h2>SBOM Dashboard</h2>
      <p>Total SBOMs: {data.total_sboms}</p>
      <p>Vulnerable Components: {data.vulnerable_components}</p>
      <p>Critical Vulnerabilities: {data.critical_vulns}</p>
    </div>
  );
}
```

#### E15: Vendor Equipment API (28 endpoints)
**Base Path:** `/api/v2/vendor-equipment`

**Key Endpoints:**
```typescript
// Dashboard
GET /api/v2/vendor-equipment/dashboard/supply-chain

// Vendors
GET /api/v2/vendor-equipment/vendors/search?query=cisco
GET /api/v2/vendor-equipment/vendors/high-risk
GET /api/v2/vendor-equipment/vendors/{vendor_id}/risk-summary

// Equipment
GET /api/v2/vendor-equipment/equipment/approaching-eol?days=180
GET /api/v2/vendor-equipment/equipment/{model_id}
```

**TypeScript Types:**
```typescript
interface Vendor {
  vendor_id: string;
  name: string;
  customer_id: string;
  risk_score: number;  // 0-10
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  total_cves: number;
  equipment_count: number;
}

interface Equipment {
  model_id: string;
  vendor_id: string;
  model_name: string;
  lifecycle_status: 'active' | 'approaching_eol' | 'at_eol' | 'past_eol';
  days_to_eol?: number;
  cve_count: number;
}
```

---

### Phase B3: Threat & Risk (82 Endpoints)

#### E04: Threat Intelligence API (27 endpoints)
**Base Path:** `/api/v2/threat-intel`

**Key Endpoints:**
```typescript
// Dashboard
GET /api/v2/threat-intel/dashboard/summary

// Threat Actors
GET /api/v2/threat-intel/actors                    // List APT groups
GET /api/v2/threat-intel/actors/{actor_id}         // Actor details
GET /api/v2/threat-intel/actors/search?query=APT29

// Campaigns
GET /api/v2/threat-intel/campaigns/active
GET /api/v2/threat-intel/campaigns/{campaign_id}/timeline

// MITRE ATT&CK
GET /api/v2/threat-intel/mitre/techniques
GET /api/v2/threat-intel/mitre/tactics
```

**TypeScript Types:**
```typescript
interface ThreatActor {
  threat_actor_id: string;
  name: string;
  aliases: string[];
  actor_type: 'apt' | 'criminal' | 'hacktivist' | 'state_sponsored' | 'insider';
  motivation: 'espionage' | 'financial' | 'disruption' | 'destruction';
  target_sectors: string[];
  ttps: string[];              // MITRE ATT&CK technique IDs
  threat_score: number;        // 0-10
  is_active: boolean;
  customer_id: string;
}

interface Campaign {
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
```

**React Component Example:**
```typescript
function ThreatActorList() {
  const [search, setSearch] = useState('');

  const { data: actors, isLoading } = useQuery({
    queryKey: ['threat-actors', search],
    queryFn: () =>
      apiClient.get(`/api/v2/threat-intel/actors/search?query=${search}`),
  });

  return (
    <div>
      <input
        placeholder="Search threat actors..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <ul>
          {actors?.map(actor => (
            <li key={actor.threat_actor_id}>
              <h3>{actor.name}</h3>
              <p>Type: {actor.actor_type}</p>
              <p>Threat Score: {actor.threat_score}/10</p>
              <p>TTPs: {actor.ttps.join(', ')}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

#### E05: Risk Scoring API (26 endpoints)
**Base Path:** `/api/v2/risk`

**Key Endpoints:**
```typescript
// Dashboard
GET /api/v2/risk/dashboard/summary

// Risk Scores
GET /api/v2/risk/scores                           // List all scores
GET /api/v2/risk/scores/{entity_id}/breakdown     // Detailed breakdown
POST /api/v2/risk/scores/calculate                // Calculate new score

// Assets
GET /api/v2/risk/assets/critical
GET /api/v2/risk/assets/{asset_id}/risk-profile
```

**TypeScript Types:**
```typescript
interface RiskScore {
  entity_id: string;
  customer_id: string;
  overall_risk_score: number;  // 0-10
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  vulnerability_score: number;
  threat_score: number;
  exposure_score: number;
  impact_score: number;
  risk_trend: 'improving' | 'stable' | 'degrading';
  calculated_at: string;
}

interface RiskBreakdown {
  vulnerability_factors: Array<{
    factor: string;
    weight: number;
    value: number;
  }>;
  threat_factors: Array<{...}>;
  exposure_factors: Array<{...}>;
}
```

#### E06: Remediation API (29 endpoints)
**Base Path:** `/api/v2/remediation`

**Key Endpoints:**
```typescript
// Dashboard
GET /api/v2/remediation/dashboard/summary

// Tasks
GET /api/v2/remediation/tasks                     // List all tasks
GET /api/v2/remediation/tasks/overdue
GET /api/v2/remediation/tasks/{task_id}
POST /api/v2/remediation/tasks                    // Create task
PATCH /api/v2/remediation/tasks/{task_id}/status  // Update status

// Plans
GET /api/v2/remediation/plans
POST /api/v2/remediation/plans
```

**TypeScript Types:**
```typescript
interface RemediationTask {
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
```

---

### Phase B4: Compliance & Automation (90 Endpoints)

#### E07: Compliance Mapping API (28 endpoints)
**Base Path:** `/api/v2/compliance`

**Key Endpoints:**
```typescript
// Dashboard
GET /api/v2/compliance/dashboard/summary

// Frameworks
GET /api/v2/compliance/frameworks                 // NIST, ISO, SOC2, etc.
GET /api/v2/compliance/frameworks/{framework_id}/controls

// Controls
GET /api/v2/compliance/controls
GET /api/v2/compliance/controls/{control_id}/status
POST /api/v2/compliance/controls/{control_id}/evidence

// Gap Analysis
POST /api/v2/compliance/gap-analysis
GET /api/v2/compliance/gaps/summary
```

**TypeScript Types:**
```typescript
interface ComplianceControl {
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

interface ComplianceGap {
  gap_id: string;
  control_id: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  description: string;
  remediation_plan?: string;
  target_date?: string;
}
```

#### E08: Automated Scanning API (30 endpoints)
**Base Path:** `/api/v2/scanning`

**Key Endpoints:**
```typescript
// Dashboard
GET /api/v2/scanning/dashboard/summary

// Scans
GET /api/v2/scanning/scans                        // List scans
POST /api/v2/scanning/scans                       // Schedule scan
GET /api/v2/scanning/scans/{scan_id}/results

// Integrations
GET /api/v2/scanning/integrations                 // Nessus, Qualys, etc.
POST /api/v2/scanning/integrations/test           // Test connection
```

**TypeScript Types:**
```typescript
interface ScanConfiguration {
  scan_id: string;
  customer_id: string;
  name: string;
  scan_type: 'vulnerability' | 'compliance' | 'config';
  scanner_integration: 'nessus' | 'qualys' | 'rapid7' | 'tenable';
  schedule: string;          // Cron expression
  target_assets: string[];
  status: 'active' | 'paused' | 'disabled';
}

interface ScanResult {
  result_id: string;
  scan_id: string;
  cve_id?: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'informational';
  cvss_score?: number;
  status: 'new' | 'open' | 'remediated' | 'false_positive';
}
```

#### E09: Alert Management API (32 endpoints)
**Base Path:** `/api/v2/alerts`

**Key Endpoints:**
```typescript
// Dashboard
GET /api/v2/alerts/dashboard/summary

// Alerts
GET /api/v2/alerts                                // List alerts
GET /api/v2/alerts/{alert_id}
PATCH /api/v2/alerts/{alert_id}/acknowledge
PATCH /api/v2/alerts/{alert_id}/resolve

// Rules
GET /api/v2/alerts/rules
POST /api/v2/alerts/rules                         // Create alert rule

// Notifications
GET /api/v2/alerts/notifications/channels         // Email, Slack, Teams
POST /api/v2/alerts/notifications/test
```

**TypeScript Types:**
```typescript
interface Alert {
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

interface AlertRule {
  rule_id: string;
  name: string;
  conditions: Array<{
    field: string;
    operator: string;
    value: any;
  }>;
  severity: string;
  notification_channels: string[];
  is_active: boolean;
}
```

---

### Phase B5: Advanced Analytics (78 Endpoints)

#### E10: Economic Impact API (26 endpoints)
**Base Path:** `/api/v2/economic-impact`

**Key Endpoints:**
```typescript
// Dashboard
GET /api/v2/economic-impact/dashboard/summary

// ROI Analysis
GET /api/v2/economic-impact/roi/summary
POST /api/v2/economic-impact/roi/calculate

// Cost Analysis
GET /api/v2/economic-impact/costs/summary
POST /api/v2/economic-impact/costs/calculate
GET /api/v2/economic-impact/costs/by-category
```

**TypeScript Types:**
```typescript
interface ROICalculation {
  investment_id: string;
  customer_id: string;
  name: string;
  category: 'security_tools' | 'infrastructure' | 'personnel' | 'training';
  initial_investment: number;
  annual_benefits: number;
  annual_costs: number;
  roi_percentage: number;
  npv: number;                    // Net Present Value
  irr: number;                    // Internal Rate of Return
  payback_period_months: number;
  risk_adjusted_roi: number;
  confidence_score: number;       // 0-1
}

interface CostBreakdown {
  total_costs: number;
  cost_categories: {
    equipment: number;
    personnel: number;
    downtime: number;
    remediation: number;
    incident_response: number;
  };
  period_start: string;
  period_end: string;
  currency: string;
}
```

#### E11: Demographics Baseline API (24 endpoints)
**Base Path:** `/api/v2/demographics`

**Key Endpoints:**
```typescript
// Dashboard
GET /api/v2/demographics/dashboard/summary
GET /api/v2/demographics/dashboard/baseline       // Psychohistory metrics

// Population
GET /api/v2/demographics/population/summary
GET /api/v2/demographics/population/distribution

// Workforce
GET /api/v2/demographics/workforce/composition
GET /api/v2/demographics/workforce/skills
GET /api/v2/demographics/workforce/turnover

// Organization
GET /api/v2/demographics/organization/hierarchy
GET /api/v2/demographics/organization/units
```

**TypeScript Types:**
```typescript
interface BaselineMetrics {
  customer_id: string;
  population_stability_index: number;  // 0-1
  role_diversity_score: number;        // 0-1
  skill_concentration_risk: number;    // 0-10
  succession_coverage: number;         // 0-1
  insider_threat_baseline: number;     // 0-10
  calculated_at: string;
}

interface WorkforceComposition {
  total_workforce: number;
  by_department: Record<string, number>;
  by_role: Record<string, number>;
  by_seniority: Record<string, number>;
  turnover_rate: number;
  average_tenure_years: number;
}
```

#### E12: Prioritization API (28 endpoints)
**Base Path:** `/api/v2/prioritization`

**Key Endpoints:**
```typescript
// Dashboard
GET /api/v2/prioritization/dashboard/summary

// NOW-NEXT-NEVER Categories
GET /api/v2/prioritization/now/items              // Immediate action (score >= 70)
GET /api/v2/prioritization/next/items             // Planned (score 40-69)
GET /api/v2/prioritization/never/items            // Deferred (score < 40)

// Scoring
POST /api/v2/prioritization/score/calculate
GET /api/v2/prioritization/score/{entity_id}/breakdown

// Actions
POST /api/v2/prioritization/now/escalate
POST /api/v2/prioritization/next/promote
```

**TypeScript Types:**
```typescript
interface PriorityItem {
  item_id: string;
  customer_id: string;
  entity_type: 'vulnerability' | 'remediation_task' | 'asset' | 'threat' | 'compliance_gap';
  entity_id: string;
  entity_name: string;
  priority_category: 'NOW' | 'NEXT' | 'NEVER';
  priority_score: number;         // 0-100
  deadline: string | null;
  sla_status: 'within_sla' | 'at_risk' | 'breached';
  is_now: boolean;                // Score >= 70
  is_sla_at_risk: boolean;
  urgency_score: number;
  risk_score: number;
  impact_score: number;
}

interface PriorityScoreRequest {
  entity_type: string;
  entity_id: string;
  entity_name: string;
  urgency_factors: Array<{
    factor_type: 'exploit_available' | 'active_campaign' | 'compliance_deadline';
    weight: number;
    value: number;
    description: string;
  }>;
  risk_factors: Array<{...}>;
  impact_factors: Array<{...}>;
}
```

---

## 5. Authentication & Headers

### Required Headers

**Every API request MUST include:**

```typescript
headers: {
  'X-Customer-ID': 'your-customer-id',  // REQUIRED for multi-tenancy
  'Content-Type': 'application/json',   // For POST/PUT requests
}

// Optional headers:
headers: {
  'X-Access-Level': 'read' | 'write' | 'admin',  // Default: read
  'X-User-ID': 'user-123',                        // For audit trails
  'X-Namespace': 'customer-namespace',            // Custom isolation
}
```

### Customer ID Management

```typescript
// Store customer ID in localStorage
localStorage.setItem('aeon_customer_id', 'customer-123');

// Retrieve in API client
const customerId = localStorage.getItem('aeon_customer_id') || 'demo-customer';
```

### Error Handling

```typescript
try {
  const response = await apiClient.get('/api/v2/sbom/sboms');
  return response;
} catch (error) {
  if (axios.isAxiosError(error)) {
    switch (error.response?.status) {
      case 400:
        console.error('Bad Request:', error.response.data.detail);
        break;
      case 403:
        console.error('Forbidden: Missing X-Customer-ID or insufficient permissions');
        break;
      case 404:
        console.error('Not Found');
        break;
      case 500:
        console.error('Server Error');
        break;
      default:
        console.error('API Error:', error.message);
    }
  }
  throw error;
}
```

---

## 6. Common Patterns

### Pattern 1: Dashboard Data Fetching

```typescript
function UnifiedDashboard() {
  // Fetch all dashboard summaries in parallel
  const customerId = useCustomerId();

  const queries = useQueries({
    queries: [
      {
        queryKey: ['sbom-dashboard', customerId],
        queryFn: () => apiClient.get('/api/v2/sbom/dashboard/summary'),
      },
      {
        queryKey: ['threat-dashboard', customerId],
        queryFn: () => apiClient.get('/api/v2/threat-intel/dashboard/summary'),
      },
      {
        queryKey: ['risk-dashboard', customerId],
        queryFn: () => apiClient.get('/api/v2/risk/dashboard/summary'),
      },
      {
        queryKey: ['compliance-dashboard', customerId],
        queryFn: () => apiClient.get('/api/v2/compliance/dashboard/summary'),
      },
      {
        queryKey: ['alerts-dashboard', customerId],
        queryFn: () => apiClient.get('/api/v2/alerts/dashboard/summary'),
      },
    ],
  });

  const isLoading = queries.some(q => q.isLoading);
  const error = queries.find(q => q.error)?.error;

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  const [sbom, threat, risk, compliance, alerts] = queries.map(q => q.data);

  return (
    <div className="dashboard-grid">
      <SBOMSummary data={sbom} />
      <ThreatSummary data={threat} />
      <RiskSummary data={risk} />
      <ComplianceSummary data={compliance} />
      <AlertsSummary data={alerts} />
    </div>
  );
}
```

### Pattern 2: Search with Debounce

```typescript
import { useState, useEffect } from 'react';
import { useDebounce } from '@/hooks/useDebounce';

function ComponentSearch() {
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 300);

  const { data: components, isLoading } = useQuery({
    queryKey: ['components', debouncedSearch],
    queryFn: () =>
      apiClient.get(`/api/v2/sbom/components/search?query=${debouncedSearch}&limit=20`),
    enabled: debouncedSearch.length > 2, // Only search if 3+ characters
  });

  return (
    <div>
      <input
        type="text"
        placeholder="Search components..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {isLoading && <LoadingSpinner />}

      {components && (
        <ul>
          {components.map(comp => (
            <li key={comp.component_id}>
              {comp.name} {comp.version} - {comp.vulnerability_count} vulns
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### Pattern 3: Mutations (Create/Update)

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

function CreateRemediationTask() {
  const queryClient = useQueryClient();

  const createTask = useMutation({
    mutationFn: (task: CreateTaskRequest) =>
      apiClient.post('/api/v2/remediation/tasks', task),
    onSuccess: () => {
      // Invalidate and refetch tasks list
      queryClient.invalidateQueries({ queryKey: ['remediation-tasks'] });
      toast.success('Task created successfully');
    },
    onError: (error) => {
      toast.error('Failed to create task');
      console.error(error);
    },
  });

  const handleSubmit = (formData: FormData) => {
    createTask.mutate({
      title: formData.get('title'),
      priority: formData.get('priority'),
      description: formData.get('description'),
      // ... other fields
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <button type="submit" disabled={createTask.isPending}>
        {createTask.isPending ? 'Creating...' : 'Create Task'}
      </button>
    </form>
  );
}
```

### Pattern 4: Pagination

```typescript
function PaginatedList() {
  const [page, setPage] = useState(0);
  const limit = 20;

  const { data, isLoading } = useQuery({
    queryKey: ['items', page],
    queryFn: () =>
      apiClient.get(`/api/v2/sbom/sboms?limit=${limit}&offset=${page * limit}`),
  });

  return (
    <div>
      <ItemList items={data?.results} />

      <Pagination
        currentPage={page}
        totalItems={data?.total}
        pageSize={limit}
        onPageChange={setPage}
      />
    </div>
  );
}
```

### Pattern 5: Real-Time Updates

```typescript
function AlertMonitor() {
  const queryClient = useQueryClient();

  // Poll for new alerts every 30 seconds
  const { data: alerts } = useQuery({
    queryKey: ['alerts', 'active'],
    queryFn: () => apiClient.get('/api/v2/alerts?status=new'),
    refetchInterval: 30000, // 30 seconds
  });

  // Show notification when new alerts arrive
  useEffect(() => {
    if (alerts && alerts.length > 0) {
      toast.info(`${alerts.length} new alerts`);
    }
  }, [alerts]);

  return <AlertList alerts={alerts} />;
}
```

---

## 7. What Needs To Be Built

### Priority 1: Core Dashboard (Week 1-2)

**Components:**
- `Dashboard` - Main overview
- `SBOMSummary` - SBOM metrics card
- `ThreatSummary` - Threat intelligence card
- `RiskSummary` - Risk scoring card
- `ComplianceSummary` - Compliance status card
- `AlertsSummary` - Active alerts card

**API Calls:**
```typescript
GET /api/v2/sbom/dashboard/summary
GET /api/v2/threat-intel/dashboard/summary
GET /api/v2/risk/dashboard/summary
GET /api/v2/compliance/dashboard/summary
GET /api/v2/alerts/dashboard/summary
GET /api/v2/economic-impact/dashboard/summary
GET /api/v2/demographics/dashboard/baseline
GET /api/v2/prioritization/dashboard/summary
```

### Priority 2: SBOM Management (Week 3-4)

**Components:**
- `SBOMList` - List all SBOMs
- `SBOMDetail` - SBOM details page
- `ComponentList` - Software components
- `VulnerabilityList` - Vulnerabilities table
- `SBOMUpload` - Upload new SBOM

**API Calls:**
```typescript
GET /api/v2/sbom/sboms
GET /api/v2/sbom/sboms/{sbom_id}
GET /api/v2/sbom/components
GET /api/v2/sbom/vulnerabilities/critical
POST /api/v2/sbom/sboms
```

### Priority 3: Threat Intelligence (Week 5-6)

**Components:**
- `ThreatActorList` - APT groups
- `ThreatActorDetail` - Actor profile
- `CampaignTimeline` - Active campaigns
- `MITREMatrix` - ATT&CK techniques
- `IOCManager` - Indicators of compromise

**API Calls:**
```typescript
GET /api/v2/threat-intel/actors
GET /api/v2/threat-intel/campaigns/active
GET /api/v2/threat-intel/mitre/techniques
GET /api/v2/threat-intel/iocs
```

### Priority 4: Risk & Remediation (Week 7-8)

**Components:**
- `RiskScoreList` - Entity risk scores
- `RiskBreakdown` - Detailed score factors
- `RemediationTaskList` - Task management
- `RemediationTaskDetail` - Task details
- `RemediationPlanner` - Create plans

**API Calls:**
```typescript
GET /api/v2/risk/scores
GET /api/v2/risk/scores/{entity_id}/breakdown
GET /api/v2/remediation/tasks
POST /api/v2/remediation/tasks
PATCH /api/v2/remediation/tasks/{task_id}/status
```

### Priority 5: Compliance (Week 9-10)

**Components:**
- `ComplianceFrameworkList` - NIST, ISO, etc.
- `ControlList` - Framework controls
- `ControlStatus` - Implementation status
- `GapAnalysis` - Compliance gaps
- `EvidenceUpload` - Upload evidence

**API Calls:**
```typescript
GET /api/v2/compliance/frameworks
GET /api/v2/compliance/controls
POST /api/v2/compliance/gap-analysis
POST /api/v2/compliance/controls/{control_id}/evidence
```

### Priority 6: Alerts & Scanning (Week 11-12)

**Components:**
- `AlertList` - Active alerts
- `AlertDetail` - Alert details
- `AlertRuleManager` - Create rules
- `ScanConfiguration` - Configure scans
- `ScanResults` - View results

**API Calls:**
```typescript
GET /api/v2/alerts
PATCH /api/v2/alerts/{alert_id}/acknowledge
GET /api/v2/alerts/rules
POST /api/v2/scanning/scans
GET /api/v2/scanning/scans/{scan_id}/results
```

### Priority 7: Economic & Demographics (Week 13-14)

**Components:**
- `ROICalculator` - Calculate ROI
- `CostAnalysis` - Cost breakdown
- `WorkforceComposition` - Demographics
- `BaselineMetrics` - Psychohistory baseline
- `PrioritizationMatrix` - NOW-NEXT-NEVER

**API Calls:**
```typescript
POST /api/v2/economic-impact/roi/calculate
GET /api/v2/economic-impact/costs/summary
GET /api/v2/demographics/workforce/composition
GET /api/v2/demographics/dashboard/baseline
GET /api/v2/prioritization/now/items
```

### Shared Components

**Needed across all features:**
- `LoadingSpinner` - Loading state
- `ErrorMessage` - Error display
- `DataTable` - Generic table with sort/filter
- `SearchBar` - Debounced search
- `Pagination` - Page navigation
- `StatusBadge` - Status indicator
- `SeverityBadge` - Severity (critical/high/medium/low)
- `RiskScoreDisplay` - Risk score visualization
- `DateRangePicker` - Date selection
- `ExportButton` - Export to CSV/JSON

---

## 8. Quick Reference

### Testing Endpoints

```bash
# Test API connectivity
curl http://localhost:8000/health

# Test SBOM dashboard
curl -H "X-Customer-ID: demo-customer" \
  http://localhost:8000/api/v2/sbom/dashboard/summary

# Test threat intelligence
curl -H "X-Customer-ID: demo-customer" \
  http://localhost:8000/api/v2/threat-intel/actors

# Test prioritization
curl -H "X-Customer-ID: demo-customer" \
  http://localhost:8000/api/v2/prioritization/now/items
```

### Common Response Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Display data |
| 201 | Created | Show success message |
| 400 | Bad Request | Show validation errors |
| 403 | Forbidden | Check X-Customer-ID header |
| 404 | Not Found | Show not found message |
| 500 | Server Error | Retry or contact support |

### Key TypeScript Imports

```typescript
import axios from 'axios';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useState, useEffect } from 'react';
```

### Documentation Files

| File | Purpose |
|------|---------|
| `FRONTEND_QUICK_START_2025-12-04.md` | Quick start (current file) |
| `FRONTEND_CHEATSHEET_2025-12-04.md` | Copy-paste examples |
| `API_ACCESS_GUIDE.md` | Complete API reference |
| `DATA_MODELS.ts` | TypeScript interfaces |
| `BACKEND_COMPLETE_REFERENCE.md` | Backend details |

---

## Next Steps

1. **Set up development environment** (Section 2)
2. **Create base API client** (Section 3)
3. **Build unified dashboard** (Priority 1)
4. **Implement SBOM features** (Priority 2)
5. **Add threat intelligence** (Priority 3)

---

**Questions?**
- Backend API: `http://localhost:8000`
- Documentation: `/1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1/`
- Full API Docs: `API_ACCESS_GUIDE.md`

**Generated**: 2025-12-04 22:30:00 UTC
**AEON Digital Twin Cybersecurity Platform**
