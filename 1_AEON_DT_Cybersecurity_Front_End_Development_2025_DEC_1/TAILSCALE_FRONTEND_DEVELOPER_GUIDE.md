# Front-End Developer Guide - Tailscale Remote Access
**Date**: 2025-12-13
**System**: AEON Digital Twin Cybersecurity Platform
**API Version**: 3.3.0

---

## System Overview

You will be building a comprehensive front-end UI for the AEON Digital Twin Cybersecurity Platform, accessing the backend API via Tailscale VPN.

### Current System State

**Backend API:**
- Total Endpoints: 230 paths (263 operations including HTTP method variants)
- API Version: 3.3.0
- OpenAPI Version: 3.1.0
- Container: ner11-gold-api
- Port: 8000

**Modules Available:**
1. SBOM Analysis (33 endpoints) - Software Bill of Materials
2. Economic Impact (27 endpoints) - Financial analysis
3. Remediation (26 endpoints) - Vulnerability remediation workflows
4. Threat Intelligence (25 endpoints) - Threat actors, campaigns, IOCs
5. Demographics (24 endpoints) - Organizational demographics
6. Risk Scoring (23 endpoints) - Risk assessments
7. Compliance (21 endpoints) - Compliance frameworks (NIST, ISO, PCI, etc.)
8. Vendor Equipment (19 endpoints) - Equipment lifecycle management
9. Alerts (19 endpoints) - Alert management and correlation
10. Psychometrics (8 endpoints) - Psychological profiling
11. Core Services (5 endpoints) - Health, NER, search

---

## Tailscale Access Setup

### 1. Get Tailscale Connection Details

**You will receive:**
- Tailscale IP address (e.g., 100.x.x.x)
- Tailscale hostname (e.g., aeon-backend.tailnet-name.ts.net)
- Access credentials (if required)

### 2. Tailscale Installation

**Linux/Mac:**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

**Windows:**
Download from: https://tailscale.com/download/windows

### 3. Backend Connection

Once connected to Tailscale network:

**Base URL:**
```
http://<TAILSCALE_IP>:8000
# OR
http://<TAILSCALE_HOSTNAME>:8000
```

**Example:**
```bash
# Replace with actual Tailscale address
export API_BASE_URL="http://100.64.0.1:8000"

# Test connection
curl $API_BASE_URL/health
```

---

## API Access Pattern

### Authentication

**Required Header:**
```
X-Customer-ID: <customer-id>
```

All API requests MUST include this header. Use a consistent customer ID for testing (e.g., "customer-001").

### Example Request

```bash
curl -X GET "http://<TAILSCALE_IP>:8000/api/v2/sbom/dashboard/summary" \
  -H "X-Customer-ID: customer-001"
```

```javascript
// JavaScript example
const response = await fetch('http://<TAILSCALE_IP>:8000/api/v2/sbom/dashboard/summary', {
  headers: {
    'X-Customer-ID': 'customer-001'
  }
});
const data = await response.json();
```

---

## Interactive API Documentation

### Swagger UI (Recommended for Exploration)

**URL:** `http://<TAILSCALE_IP>:8000/docs`

Features:
- Interactive endpoint testing
- Request/response schemas
- Try-it-out functionality
- Authentication configuration

### OpenAPI Specification

**URL:** `http://<TAILSCALE_IP>:8000/openapi.json`

Use for:
- Code generation
- Client SDK generation
- Type definitions
- API contract reference

---

## Front-End Architecture

### Recommended Stack

**Framework Options:**
1. **React** (Recommended) - Component-based, large ecosystem
2. **Vue.js** - Simpler learning curve, reactive
3. **Angular** - Full-featured, enterprise-ready

**UI Libraries:**
1. **Ant Design** - Professional, data-heavy UIs
2. **Material-UI** - Google Material Design
3. **Chakra UI** - Modern, accessible
4. **Tailwind CSS** - Utility-first styling

**State Management:**
1. **Redux Toolkit** (React) - Predictable state container
2. **Zustand** (React) - Lightweight alternative
3. **Pinia** (Vue) - Vue 3 state management
4. **NgRx** (Angular) - Redux for Angular

**Data Fetching:**
1. **TanStack Query (React Query)** - Caching, background updates
2. **SWR** - Lightweight, React hooks
3. **Apollo Client** - If GraphQL needed later
4. **Axios** - HTTP client library

### Recommended Project Structure

```
frontend/
├── src/
│   ├── api/                    # API client layer
│   │   ├── client.ts           # Base API client
│   │   ├── sbom.ts             # SBOM endpoints
│   │   ├── threats.ts          # Threat intelligence
│   │   ├── compliance.ts       # Compliance endpoints
│   │   └── ...                 # Other modules
│   ├── components/             # Reusable components
│   │   ├── common/             # Buttons, inputs, cards
│   │   ├── dashboard/          # Dashboard widgets
│   │   ├── charts/             # Data visualizations
│   │   └── tables/             # Data tables
│   ├── pages/                  # Page components
│   │   ├── Dashboard.tsx       # Main dashboard
│   │   ├── SBOM/               # SBOM pages
│   │   ├── ThreatIntel/        # Threat pages
│   │   └── ...                 # Other pages
│   ├── hooks/                  # Custom React hooks
│   │   ├── useAPI.ts           # API hook
│   │   ├── useAuth.ts          # Authentication
│   │   └── ...
│   ├── store/                  # State management
│   │   ├── sbomSlice.ts
│   │   ├── threatSlice.ts
│   │   └── ...
│   ├── types/                  # TypeScript types
│   │   ├── api.ts              # API response types
│   │   ├── models.ts           # Data models
│   │   └── ...
│   ├── utils/                  # Utility functions
│   │   ├── formatters.ts       # Data formatting
│   │   ├── validators.ts       # Input validation
│   │   └── ...
│   └── App.tsx                 # Root component
├── public/                     # Static assets
├── package.json
├── tsconfig.json
└── vite.config.ts              # Build config
```

---

## API Client Implementation

### Base Client (TypeScript)

```typescript
// src/api/client.ts
import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const CUSTOMER_ID = import.meta.env.VITE_CUSTOMER_ID || 'customer-001';

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'X-Customer-ID': CUSTOMER_ID,
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle authentication error
      console.error('Authentication failed');
    }
    return Promise.reject(error);
  }
);
```

### Environment Configuration

```bash
# .env.development
VITE_API_BASE_URL=http://<TAILSCALE_IP>:8000
VITE_CUSTOMER_ID=customer-001

# .env.production
VITE_API_BASE_URL=https://api.aeon-platform.com
VITE_CUSTOMER_ID=prod-customer
```

### Module-Specific API Client

```typescript
// src/api/sbom.ts
import { apiClient } from './client';

export interface SBOMSummary {
  total_sboms: number;
  total_components: number;
  total_vulnerabilities: number;
  critical_vulnerabilities: number;
  high_vulnerabilities: number;
  // ... other fields
}

export const sbomAPI = {
  getDashboardSummary: async (): Promise<SBOMSummary> => {
    const response = await apiClient.get('/api/v2/sbom/dashboard/summary');
    return response.data;
  },

  listSBOMs: async () => {
    const response = await apiClient.get('/api/v2/sbom/sboms');
    return response.data;
  },

  searchComponents: async (query: string) => {
    const response = await apiClient.post('/api/v2/sbom/components/search', {
      query,
      limit: 50,
    });
    return response.data;
  },
};
```

---

## Data Visualization

### Chart Libraries

**Recommended: Recharts (React)**
```bash
npm install recharts
```

**Alternative: Apache ECharts**
```bash
npm install echarts echarts-for-react
```

### Dashboard Example

```typescript
// src/pages/Dashboard.tsx
import { useQuery } from '@tanstack/react-query';
import { sbomAPI } from '../api/sbom';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

export function Dashboard() {
  const { data, isLoading } = useQuery({
    queryKey: ['sbom-summary'],
    queryFn: sbomAPI.getDashboardSummary,
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      <h1>AEON Cybersecurity Dashboard</h1>

      {/* Metrics Cards */}
      <div className="metrics-grid">
        <MetricCard
          title="Total SBOMs"
          value={data.total_sboms}
          icon="📦"
        />
        <MetricCard
          title="Components"
          value={data.total_components}
          icon="🔧"
        />
        <MetricCard
          title="Critical Vulnerabilities"
          value={data.critical_vulnerabilities}
          trend="up"
          icon="🚨"
        />
      </div>

      {/* Vulnerability Chart */}
      <VulnerabilityChart data={data} />
    </div>
  );
}
```

---

## Key UI Components to Build

### 1. Main Dashboard
- System health overview
- Key metrics (vulnerabilities, assets, threats)
- Recent alerts
- Risk trends
- Quick actions

### 2. SBOM Management
- SBOM list/grid view
- Component explorer
- Dependency graph visualization
- Vulnerability correlation
- License compliance view

### 3. Threat Intelligence
- Threat actor profiles
- Campaign tracking
- IOC management
- Threat timeline
- Attack surface visualization

### 4. Risk Assessment
- Risk score dashboard
- Assessment workflow
- Risk factors analysis
- Mitigation tracking
- Risk trend charts

### 5. Compliance Management
- Framework selection (NIST, ISO, PCI, SOC2)
- Control mapping
- Compliance gap analysis
- Evidence collection
- Audit reports

### 6. Remediation Workflows
- Task management
- Priority queue
- Assignment tracking
- SLA monitoring
- Progress dashboards

### 7. Alert Management
- Alert inbox
- Correlation view
- Priority sorting
- Bulk actions
- Alert history

### 8. Economic Impact
- Cost analysis
- ROI calculations
- Breach simulation
- Budget planning
- Investment optimization

### 9. Vendor/Equipment
- Equipment inventory
- EOL tracking
- Maintenance schedules
- Vendor risk assessment
- Lifecycle management

### 10. Search & Discovery
- Global search
- Semantic search
- Entity relationship explorer
- Graph visualization
- Advanced filters

---

## Data Models (TypeScript)

Generate TypeScript types from OpenAPI spec:

```bash
npm install -g openapi-typescript
openapi-typescript http://<TAILSCALE_IP>:8000/openapi.json --output src/types/api.ts
```

Or manually define:

```typescript
// src/types/models.ts
export interface Vulnerability {
  id: string;
  cve_id: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  cvss_score: number;
  description: string;
  published_date: string;
  affected_components: string[];
}

export interface ThreatActor {
  id: string;
  name: string;
  aliases: string[];
  sophistication: string;
  motivation: string;
  first_seen: string;
  last_seen: string;
}

export interface SBOM {
  id: string;
  project_name: string;
  version: string;
  format: 'cyclonedx' | 'spdx';
  component_count: number;
  vulnerability_count: number;
  created_at: string;
}
```

---

## Real-Time Features

### WebSocket Support (if available)

```typescript
const ws = new WebSocket(`ws://<TAILSCALE_IP>:8000/ws/alerts`);

ws.onmessage = (event) => {
  const alert = JSON.parse(event.data);
  // Update UI with new alert
  store.dispatch(addAlert(alert));
};
```

### Polling Alternative

```typescript
const { data } = useQuery({
  queryKey: ['alerts'],
  queryFn: alertsAPI.getActive,
  refetchInterval: 5000, // Poll every 5 seconds
});
```

---

## Security Considerations

### 1. CORS Configuration

Backend must allow Tailscale frontend:

```python
# Backend CORS settings (already configured)
allow_origins = ["http://<TAILSCALE_IP>:*"]
```

If you encounter CORS issues, contact backend team.

### 2. Secure Storage

```typescript
// Don't store sensitive data in localStorage
// Use sessionStorage for temporary auth tokens
sessionStorage.setItem('customer-id', customerId);
```

### 3. Input Validation

```typescript
import { z } from 'zod';

const searchSchema = z.object({
  query: z.string().min(1).max(500),
  limit: z.number().min(1).max(100).optional(),
});

// Validate before API call
const validated = searchSchema.parse(userInput);
```

---

## Testing Strategy

### 1. API Integration Tests

```typescript
// src/api/__tests__/sbom.test.ts
import { describe, it, expect } from 'vitest';
import { sbomAPI } from '../sbom';

describe('SBOM API', () => {
  it('should fetch dashboard summary', async () => {
    const summary = await sbomAPI.getDashboardSummary();
    expect(summary).toHaveProperty('total_sboms');
    expect(typeof summary.total_sboms).toBe('number');
  });
});
```

### 2. Component Tests

```typescript
import { render, screen } from '@testing-library/react';
import { Dashboard } from '../Dashboard';

test('renders dashboard title', () => {
  render(<Dashboard />);
  expect(screen.getByText(/AEON Cybersecurity Dashboard/i)).toBeInTheDocument();
});
```

---

## Performance Optimization

### 1. Code Splitting

```typescript
// Lazy load pages
const SBOM = lazy(() => import('./pages/SBOM'));
const ThreatIntel = lazy(() => import('./pages/ThreatIntel'));

<Suspense fallback={<Loading />}>
  <Routes>
    <Route path="/sbom" element={<SBOM />} />
    <Route path="/threats" element={<ThreatIntel />} />
  </Routes>
</Suspense>
```

### 2. Data Caching

```typescript
// TanStack Query handles caching automatically
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
    },
  },
});
```

### 3. Virtual Scrolling

For large lists (use react-window):

```typescript
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={items.length}
  itemSize={50}
  width="100%"
>
  {Row}
</FixedSizeList>
```

---

## Deployment

### Development Server

```bash
npm run dev
# Frontend runs on http://localhost:5173
# API accessible via Tailscale at http://<TAILSCALE_IP>:8000
```

### Production Build

```bash
npm run build
npm run preview  # Test production build locally
```

### Environment Variables

```bash
# Required for production
VITE_API_BASE_URL=http://<TAILSCALE_IP>:8000
VITE_CUSTOMER_ID=<customer-id>
```

---

## Quick Start Checklist

- [ ] Install Tailscale and connect to network
- [ ] Verify backend access: `curl http://<TAILSCALE_IP>:8000/health`
- [ ] Test API docs: Visit `http://<TAILSCALE_IP>:8000/docs`
- [ ] Set up frontend project (React + Vite + TypeScript)
- [ ] Install dependencies: axios, @tanstack/react-query, recharts
- [ ] Configure API client with Tailscale IP
- [ ] Generate TypeScript types from OpenAPI spec
- [ ] Build main dashboard page
- [ ] Implement module-specific pages
- [ ] Add data visualizations
- [ ] Implement search and filtering
- [ ] Add error handling and loading states
- [ ] Test all major workflows
- [ ] Optimize performance
- [ ] Deploy to staging environment

---

## Support & Resources

### API Documentation Files

1. **Master Reference**: `docs/api/MASTER_API_REFERENCE.md`
   - Complete endpoint catalog with examples

2. **Quick Start**: `docs/api/API_QUICK_START_GUIDE.md`
   - Authentication, common patterns

3. **Phase-Specific Docs**: `docs/api/PHASE_B*_*.md`
   - Detailed module documentation

4. **Interactive Docs**: `http://<TAILSCALE_IP>:8000/docs`
   - Live API testing

### Example Code Repository

```bash
# If available, clone reference implementation
git clone <repository-url>
cd aeon-frontend-reference
npm install
```

### API Endpoint Summary

**All endpoints follow pattern:**
```
http://<TAILSCALE_IP>:8000/api/v2/<module>/<resource>
```

**Example endpoints to test first:**
```bash
# Health check
GET /health

# SBOM dashboard
GET /api/v2/sbom/dashboard/summary

# Risk dashboard
GET /api/v2/risk/dashboard

# List threat actors
GET /api/v2/threat-intel/actors

# Compliance frameworks
GET /api/v2/compliance/frameworks
```

---

## Troubleshooting

### Cannot Connect to Backend

```bash
# Verify Tailscale connection
tailscale status

# Test backend reachability
ping <TAILSCALE_IP>

# Test API specifically
curl http://<TAILSCALE_IP>:8000/health
```

### CORS Errors

Contact backend team to whitlist your origin. Provide your Tailscale IP.

### 422 Validation Errors

Check request parameters match OpenAPI spec. Common issues:
- Missing `X-Customer-ID` header
- Invalid request body format
- Missing required fields

### Performance Issues

- Enable React DevTools Profiler
- Check Network tab for slow requests
- Implement pagination for large datasets
- Use virtual scrolling for long lists

---

**Last Updated**: 2025-12-13
**API Version**: 3.3.0
**Document Version**: 1.0
