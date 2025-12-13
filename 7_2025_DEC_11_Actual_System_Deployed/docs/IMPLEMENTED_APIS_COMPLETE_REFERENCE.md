# AEON SaaS - Complete API Reference
**File:** IMPLEMENTED_APIS_COMPLETE_REFERENCE.md
**Created:** 2025-12-12
**Version:** v1.0.0
**Container:** aeon-saas-dev
**Base URL:** http://localhost:3000/api

## Table of Contents
1. [Threat Intelligence APIs](#threat-intelligence-apis) (8 APIs)
2. [Dashboard & Metrics APIs](#dashboard--metrics-apis) (4 APIs)
3. [Analytics APIs](#analytics-apis) (7 APIs)
4. [Graph & Neo4j APIs](#graph--neo4j-apis) (3 APIs)
5. [Pipeline APIs](#pipeline-apis) (2 APIs)
6. [Query Control APIs](#query-control-apis) (7 APIs)
7. [Customer Management APIs](#customer-management-apis) (2 APIs)
8. [Observability APIs](#observability-apis) (3 APIs)
9. [Tags APIs](#tags-apis) (3 APIs)
10. [Utility APIs](#utility-apis) (5 APIs)

---

## Threat Intelligence APIs

### 1. GET /api/threat-intel/analytics
**Purpose:** Attack analytics data for MITRE ATT&CK, Kill Chain, Malware, and IOC statistics

**Authentication:** Required (Clerk)

**Query Parameters:** None

**Response Schema:**
```typescript
interface AnalyticsResponse {
  mitreTactics: Array<{
    tactic: string;
    techniques: number;
    campaigns: number;
    color: string;
  }>;
  killChain: Array<{
    stage: string;
    attacks: number;
    percent: number;
  }>;
  malware: Array<{
    name: string;
    instances: number;
    type: string;
    risk: 'critical' | 'high' | 'medium' | 'low';
    attributedActors: string[];
  }>;
  iocStats: Array<{
    label: string;
    count: number;
  }>;
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:3000/api/threat-intel/analytics \
  -H "Authorization: Bearer YOUR_CLERK_TOKEN"
```

**Example JavaScript:**
```javascript
const response = await fetch('/api/threat-intel/analytics', {
  headers: { 'Authorization': `Bearer ${clerkToken}` }
});
const analytics = await response.json();
```

**Graph Queries Used:**
- Query 3.1: MITRE ATT&CK Tactic Frequency (3-5 hops)
- Query 3.2: Cyber Kill Chain Analysis (4-6 hops)
- Query 3.3: Malware Family Attribution (5-7 hops)
- Query 3.4: IOC Statistics (2-3 hops)

---

### 2. GET /api/threat-intel/ics
**Purpose:** ICS/SCADA critical infrastructure threat intelligence

**Authentication:** Required (Clerk)

**Query Parameters:**
- `minCVSS` (float, optional): Minimum CVSS score (default: 7.0)
- `sectorFilter` (string, optional): Filter by infrastructure sector

**Response Schema:**
```typescript
interface ICSResponse {
  sectors: Array<{
    name: string;
    threatScore: number;
    assets: number;
    color: string;
  }>;
  vulnerabilities: Array<{
    id: string;
    system: string;
    vendor: string;
    cvss: number;
    description: string;
    affected: number;
  }>;
  mitigations: Array<{
    title: string;
    priority: 'critical' | 'high' | 'medium';
    implemented: number;
    description: string;
  }>;
  totalAssets: number;
  criticalVulns: number;
  responseTime: number;
}
```

**Example cURL:**
```bash
curl -X GET "http://localhost:3000/api/threat-intel/ics?minCVSS=8.0&sectorFilter=Energy" \
  -H "Authorization: Bearer YOUR_CLERK_TOKEN"
```

**Graph Queries Used:**
- Query 4.1: Sector Threat Assessment (6-8 hops)
- Query 4.2: ICS/SCADA Critical Vulnerabilities (5-7 hops)
- Query 4.3: Security Control Coverage (4-5 hops)

---

### 3. GET /api/threat-intel/landscape
**Purpose:** Threat landscape overview with actors, industries, and campaigns

**Authentication:** Required (Clerk)

**Response Schema:**
```typescript
interface LandscapeResponse {
  threatActors: Array<{
    name: string;
    location: string;
    campaigns: number;
    status: 'active' | 'monitoring' | 'dormant';
    campaignNames: string[];
    impactedSectors: string[][];
    lastActivity: string | null;
  }>;
  industries: Array<{
    name: string;
    attacks: number;
    percent: number;
  }>;
  campaigns: Array<{
    name: string;
    actor: string;
    started: string;
    severity: 'critical' | 'high' | 'medium' | 'low';
    ttpCount: number;
  }>;
  totalActors: number;
  activeCampaigns: number;
}
```

**Example Python:**
```python
import requests

response = requests.get(
    'http://localhost:3000/api/threat-intel/landscape',
    headers={'Authorization': f'Bearer {clerk_token}'}
)
landscape = response.json()
```

**Graph Queries Used:**
- Query 1.1: Threat Actor Campaign Summary (4-6 hops)
- Query 1.2: Industry Targeting Analysis (5-7 hops)
- Query 1.3: Recent Campaigns with Attribution (3-4 hops)

---

### 4. GET /api/threat-intel/vulnerabilities
**Purpose:** CVE vulnerability data with exploitation intelligence

**Authentication:** Required (Clerk)

**Query Parameters:**
- `minCVSS` (float, optional): Minimum CVSS score (default: 7.0)
- `exploited` (boolean, optional): Filter by exploitation status
- `patched` (boolean, optional): Filter by patch availability
- `limit` (int, optional): Max results (default: 50)

**Response Schema:**
```typescript
interface VulnerabilityResponse {
  cves: Array<{
    id: string;
    cvss: number;
    description: string;
    exploited: boolean;
    patched: boolean;
    attackPatterns: number;
    threatActors: number;
    activeCampaigns: string[];
    attributedActors: string[];
  }>;
  distribution: Array<{
    range: string;
    count: number;
  }>;
  patchStatus: {
    patchedPercent: number;
    availablePercent: number;
    noPatchPercent: number;
  };
  totalCVEs: number;
}
```

**Example cURL:**
```bash
curl -X GET "http://localhost:3000/api/threat-intel/vulnerabilities?minCVSS=9.0&exploited=true" \
  -H "Authorization: Bearer YOUR_CLERK_TOKEN"
```

**Graph Queries Used:**
- Query 2.1: CVE Exploitation Intelligence (6-8 hops)
- Query 2.2: CVSS Score Distribution
- Query 2.3: Patch Status Analysis

---

### 5. GET /api/threats/geographic
**Purpose:** Geographic threat distribution for world map visualization

**Authentication:** Required (Clerk)

**Response Schema:**
```typescript
interface GeographicResponse {
  threats: Array<{
    id: string;
    name: string;
    latitude: number;
    longitude: number;
    threatLevel: 'critical' | 'high' | 'medium' | 'low';
    count: number;
    types: string[];
  }>;
}
```

**Example JavaScript:**
```javascript
const response = await fetch('/api/threats/geographic');
const geoThreats = await response.json();
```

---

### 6. GET /api/threats/ics
**Purpose:** ICS threat data (alternative endpoint)

**Authentication:** Not required

**Response Schema:**
```typescript
interface ICSThreatsResponse {
  sectors: Array<{
    name: string;
    threatScore: number;
    assets: number;
    color: string;
  }>;
  vulnerabilities: Array<{
    id: string;
    system: string;
    vendor: string;
    cvss: number;
    description: string;
    affected: number;
  }>;
  mitigations: Array<{
    title: string;
    priority: string;
    implemented: number;
    description: string;
  }>;
}
```

---

## Dashboard & Metrics APIs

### 7. GET /api/dashboard/activity
**Purpose:** Time-series activity data for threat, vulnerability, and incident trends

**Authentication:** Required (Clerk)

**Response Schema:**
```typescript
type ActivityData = Array<{
  date: string;
  threats: number;
  vulnerabilities: number;
  incidents: number;
}>;
```

**Example cURL:**
```bash
curl -X GET http://localhost:3000/api/dashboard/activity \
  -H "Authorization: Bearer YOUR_CLERK_TOKEN"
```

**Returns:** Last 7 days of activity data

---

### 8. GET /api/dashboard/distribution
**Purpose:** Threat distribution by type for donut chart visualization

**Authentication:** Required (Clerk)

**Response Schema:**
```typescript
type DistributionData = Array<{
  name: string;
  value: number;
}>;
```

**Example JavaScript:**
```javascript
const response = await fetch('/api/dashboard/distribution');
const distribution = await response.json();
// Returns: [
//   { name: 'Malware', value: 892 },
//   { name: 'Threat Actors', value: 156 },
//   ...
// ]
```

---

### 9. GET /api/dashboard/metrics
**Purpose:** High-level dashboard metrics (entities, threats, CVEs, system status)

**Authentication:** Required (Clerk)

**Response Schema:**
```typescript
interface DashboardMetrics {
  documentGrowth: {
    current: number;
    previous: number;
    percentageChange: number;
  };
  entitiesAdded: {
    current: number;
    previous: number;
    percentageChange: number;
  };
  processSuccess: {
    current: number;
    percentageChange: number;
  };
  avgQuality: {
    current: number;
    previous: number;
    percentageChange: number;
  };
  totalEntities: number;
  activeThreats: number;
  recentCVEs: number;
  systemStatus: string;
}
```

**Example Python:**
```python
response = requests.get(
    'http://localhost:3000/api/dashboard/metrics',
    headers={'Authorization': f'Bearer {clerk_token}'}
)
metrics = response.json()
print(f"Active Threats: {metrics['activeThreats']}")
```

---

### 10. GET /api/activity/recent
**Purpose:** Recent system activity (uploads, customer operations)

**Authentication:** Not required

**Query Parameters:**
- `limit` (int, optional): Max results (default: 10)

**Response Schema:**
```typescript
interface RecentActivityResponse {
  activities: Array<{
    id: string;
    type: 'upload' | 'processed';
    title: string;
    description: string;
    timestamp: Date;
    user: string;
  }>;
  total: number;
  timestamp: string;
}
```

**Example cURL:**
```bash
curl -X GET "http://localhost:3000/api/activity/recent?limit=20"
```

---

## Analytics APIs

### 11. POST /api/analytics/export
**Purpose:** Export analytics data in CSV, JSON, or PDF formats

**Authentication:** Not required

**Request Body:**
```typescript
{
  format: 'csv' | 'json' | 'pdf';
  timeRange?: '7d' | '30d' | '90d';
  customerId?: string;
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:3000/api/analytics/export \
  -H "Content-Type: application/json" \
  -d '{"format": "csv", "timeRange": "30d"}' \
  --output analytics.csv
```

**Returns:** Downloadable file (CSV/JSON/TXT)

---

### 12. GET /api/analytics/metrics
**Purpose:** Analytics metrics with time-based comparisons

**Authentication:** Not required

**Query Parameters:**
- `timeRange` (string, optional): '7d', '30d', '90d' (default: '30d')
- `customerId` (string, optional): Filter by customer

**Response Schema:**
```typescript
interface MetricsResponse {
  documentGrowth: {
    current: number;
    previous: number;
    percentageChange: number;
  };
  entitiesAdded: {
    current: number;
    previous: number;
    percentageChange: number;
  };
  processSuccess: {
    current: number;
    percentageChange: number;
  };
  avgQuality: {
    current: number;
    previous: number;
    percentageChange: number;
  };
}
```

**Example JavaScript:**
```javascript
const response = await fetch('/api/analytics/metrics?timeRange=90d');
const metrics = await response.json();
```

---

### 13. GET /api/analytics/timeseries
**Purpose:** Time-series data for documents, entities, and customer activity

**Authentication:** Not required

**Query Parameters:**
- `timeRange` (string, optional): '7d', '30d', '90d'
- `customerId` (string, optional): Filter by customer

**Response Schema:**
```typescript
interface TimeSeriesData {
  documentsOverTime: Array<{ date: string; count: number }>;
  entitiesByType: Array<{ name: string; value: number }>;
  customerActivity: Array<{
    name: string;
    documents: number;
    entities: number;
  }>;
}
```

**Example Python:**
```python
response = requests.get('http://localhost:3000/api/analytics/timeseries?timeRange=7d')
timeseries = response.json()
```

---

### 14. GET /api/analytics/trends/cve
**Purpose:** CVE trend analysis by severity over time

**Authentication:** Not required

**Query Parameters:**
- `startDate` (string, optional): ISO date
- `endDate` (string, optional): ISO date

**Response Schema:**
```typescript
interface CVETrendsResponse {
  monthlyTrends: Array<{
    month: string;
    critical: number;
    high: number;
    medium: number;
    low: number;
    avgSystemsAffected?: number;
  }>;
  totalCount: number;
  percentChange: number;
  totalSystemsAffected?: number;
}
```

**Example cURL:**
```bash
curl -X GET "http://localhost:3000/api/analytics/trends/cve?startDate=2024-01-01&endDate=2024-12-31"
```

---

### 15. GET /api/analytics/trends/seasonality
**Purpose:** Campaign seasonality pattern analysis (heatmap data)

**Authentication:** Not required

**Response Schema:**
```typescript
interface SeasonalityResponse {
  heatmap: Array<{
    year: number;
    month: number;
    count: number;
    campaigns: string[];
  }>;
  years: number[];
  months: number[];
  maxCount: number;
}
```

**Example JavaScript:**
```javascript
const response = await fetch('/api/analytics/trends/seasonality');
const seasonality = await response.json();
// Use for heatmap visualization
```

---

### 16. GET /api/analytics/trends/threat-timeline
**Purpose:** Threat actor campaign timeline analysis

**Authentication:** Not required

**Query Parameters:**
- `startDate` (string, optional): ISO date
- `endDate` (string, optional): ISO date

**Response Schema:**
```typescript
interface ThreatTimelineResponse {
  timeline: Array<{
    month: string;
    threatActor: string;
    campaigns: number;
    campaignDetails: Array<{
      name: string;
      firstSeen: string;
      lastSeen: string;
      durationDays: number;
    }>;
  }>;
  totalActors: number;
  totalCampaigns: number;
}
```

**Example Python:**
```python
response = requests.get('http://localhost:3000/api/analytics/trends/threat-timeline')
timeline = response.json()
print(f"Total Threat Actors: {timeline['totalActors']}")
```

---

## Graph & Neo4j APIs

### 17. POST /api/graph/query
**Purpose:** Execute custom Cypher queries (read-only for safety)

**Authentication:** Not required

**Request Body:**
```typescript
{
  query: string;  // Cypher query
}
```

**Security:** Blocks DELETE, REMOVE, SET, CREATE, MERGE, DROP, ALTER

**Example cURL:**
```bash
curl -X POST http://localhost:3000/api/graph/query \
  -H "Content-Type: application/json" \
  -d '{"query": "MATCH (n:ThreatActor) RETURN n LIMIT 10"}'
```

**Response:**
```typescript
{
  records: Array<Record<string, any>>;
  summary: {
    counters: any;
    query: { text: string };
  };
}
```

---

### 17b. GET /api/graph/query
**Purpose:** Fetch subgraph with filters

**Query Parameters:**
- `nodeTypes` (string, optional): Comma-separated node labels
- `relationshipTypes` (string, optional): Comma-separated relationship types
- `customers` (string, optional): Filter by customer
- `tags` (string, optional): Filter by tags
- `confidenceMin` (float, optional): Minimum confidence score
- `dateStart` (string, optional): ISO date
- `dateEnd` (string, optional): ISO date

**Response:**
```typescript
{
  nodes: Array<{
    id: string;
    labels: string[];
    properties: Record<string, any>;
  }>;
  relationships: Array<{
    id: string;
    type: string;
    startNode: string;
    endNode: string;
    properties: Record<string, any>;
  }>;
}
```

**Example cURL:**
```bash
curl -X GET "http://localhost:3000/api/graph/query?nodeTypes=ThreatActor,Campaign&limit=100"
```

---

### 18. GET /api/neo4j/cyber-statistics
**Purpose:** Cybersecurity-specific statistics from Neo4j

**Authentication:** Not required

**Response Schema:**
```typescript
interface CyberStatistics {
  cves: {
    total: number;
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  threatActors: number;
  malware: number;
  campaigns: number;
  attackTechniques: number;
  icsAssets: number;
  cweWeaknesses: number;
  responseTime: number;
  timestamp: string;
}
```

**Example JavaScript:**
```javascript
const response = await fetch('/api/neo4j/cyber-statistics');
const stats = await response.json();
console.log(`Total CVEs: ${stats.cves.total}`);
```

---

### 19. GET /api/neo4j/statistics
**Purpose:** General Neo4j statistics (customers, documents, tags)

**Authentication:** Not required

**Response Schema:**
```typescript
interface Neo4jStatistics {
  totalCustomers: number;
  totalDocuments: number;
  totalTags: number;
  totalSharedDocuments: number;
  responseTime: number;
  timestamp: string;
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:3000/api/neo4j/statistics
```

---

## Pipeline APIs

### 20. POST /api/pipeline/process
**Purpose:** Submit files for processing (in-memory queue)

**Authentication:** Required (Clerk)

**Request Body:**
```typescript
{
  files: Array<{
    path: string;
    name: string;
    size: number;
    type: string;
  }>;
  customer: string;
  tags: string[];
  classification: {
    sector: string;
    subsector?: string;
  };
}
```

**File Size Limit:** 100MB per file

**Rate Limiting:** 100 requests per 15 minutes

**Example cURL:**
```bash
curl -X POST http://localhost:3000/api/pipeline/process \
  -H "Authorization: Bearer YOUR_CLERK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "files": [{
      "path": "/uploads/doc.pdf",
      "name": "doc.pdf",
      "size": 1024000,
      "type": "application/pdf"
    }],
    "customer": "customer-123",
    "tags": ["threat-intel"],
    "classification": {"sector": "Energy"}
  }'
```

**Response:**
```typescript
{
  success: boolean;
  jobs: Array<{
    jobId: string;
    status: 'queued';
    progress: number;
    message: string;
    fileName: string;
  }>;
  message: string;
}
```

---

### 20b. GET /api/pipeline/process
**Purpose:** Get job status or queue status

**Query Parameters:**
- `jobId` (string, optional): Get specific job status

**Response:**
```typescript
{
  success: boolean;
  job?: JobStatus;
  jobs: JobStatus[];
  queueStatus: {
    waiting: number;
    active: number;
    completed: number;
    failed: number;
  };
}
```

---

### 21. GET /api/pipeline/status/[jobId]
**Purpose:** Get processing job status by ID

**Authentication:** Not required

**Response Schema:**
```typescript
{
  success: boolean;
  jobId: string;
  fileName: string;
  status: 'queued' | 'processing' | 'complete' | 'failed' | 'cancelled';
  progress: number;
  message: string;
  createdAt: Date;
  completedAt?: Date;
  steps: string[];
  customer: string;
  tags: string[];
  classification: object;
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:3000/api/pipeline/status/job-uuid-123
```

---

### 21b. DELETE /api/pipeline/status/[jobId]
**Purpose:** Cancel processing job

**Response:**
```typescript
{
  success: boolean;
  message: string;
  jobId: string;
}
```

---

## Query Control APIs

### 22. GET /api/query-control/queries
**Purpose:** List all active queries with state breakdown

**Authentication:** Not required

**Query Parameters:**
- `state` (string, optional): Filter by QueryState
- `limit` (int, optional): Max results (default: 100)
- `offset` (int, optional): Pagination offset (default: 0)

**Response Schema:**
```typescript
{
  queries: Array<QueryInfo>;
  total: number;
  states: Record<QueryState, number>;
  pagination: {
    limit: number;
    offset: number;
    hasMore: boolean;
  };
}
```

**Example cURL:**
```bash
curl -X GET "http://localhost:3000/api/query-control/queries?state=RUNNING&limit=50"
```

---

### 22b. POST /api/query-control/queries
**Purpose:** Create new query (placeholder - returns 501)

**Request Body:**
```typescript
{
  prompt: string;
  model?: 'sonnet' | 'opus' | 'haiku';
  permissionMode?: 'default' | 'acceptEdits' | 'bypassPermissions' | 'plan';
}
```

**Response:** HTTP 501 Not Implemented

---

### 23. GET /api/query-control/queries/[queryId]
**Purpose:** Get query details including state, model, checkpoints

**Response Schema:**
```typescript
{
  query: QueryInfo;
  timestamp: string;
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:3000/api/query-control/queries/query-uuid-123
```

---

### 23b. DELETE /api/query-control/queries/[queryId]
**Purpose:** Terminate a query

**Response:**
```typescript
{
  success: boolean;
  queryId: string;
  finalState: string;
  terminateTimeMs: number;
  timestamp: string;
}
```

---

### 24. GET /api/query-control/queries/[queryId]/checkpoints
**Purpose:** List all checkpoints for a query

**Query Parameters:**
- `limit` (int, optional): Max results (default: 50)
- `offset` (int, optional): Pagination offset

**Response Schema:**
```typescript
{
  queryId: string;
  checkpoints: Array<{
    id: string;
    queryId: string;
    state: string;
    timestamp: number;
    timestampISO: string;
    model: string;
    permissionMode: string;
    hasExecutionContext: boolean;
  }>;
  total: number;
  latest?: Checkpoint;
  pagination: object;
}
```

**Example JavaScript:**
```javascript
const response = await fetch('/api/query-control/queries/query-123/checkpoints');
const checkpoints = await response.json();
```

---

### 25. POST /api/query-control/queries/[queryId]/model
**Purpose:** Hot-swap AI model for query

**Request Body:**
```typescript
{
  model: 'sonnet' | 'opus' | 'haiku';
}
```

**Response:**
```typescript
{
  success: boolean;
  queryId: string;
  previousModel: string;
  newModel: string;
  switchTimeMs: number;
  timestamp: string;
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:3000/api/query-control/queries/query-123/model \
  -H "Content-Type: application/json" \
  -d '{"model": "opus"}'
```

---

### 26. POST /api/query-control/queries/[queryId]/pause
**Purpose:** Pause running query and create checkpoint

**Response:**
```typescript
{
  success: boolean;
  queryId: string;
  checkpointId?: string;
  state: string;
  pauseTimeMs: number;
  timestamp: string;
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:3000/api/query-control/queries/query-123/pause
```

---

### 27. POST /api/query-control/queries/[queryId]/resume
**Purpose:** Resume paused query from checkpoint

**Query Parameters:**
- `checkpointId` (string, optional): Specific checkpoint to resume from

**Response:**
```typescript
{
  success: boolean;
  queryId: string;
  resumedFrom?: string;
  state: string;
  resumeTimeMs: number;
  checkpoint?: object;
  timestamp: string;
}
```

**Example JavaScript:**
```javascript
const response = await fetch('/api/query-control/queries/query-123/resume', {
  method: 'POST'
});
const result = await response.json();
```

---

### 28. POST /api/query-control/queries/[queryId]/permissions
**Purpose:** Switch permission mode for query

**Request Body:**
```typescript
{
  permissionMode: 'default' | 'acceptEdits' | 'bypassPermissions' | 'plan';
}
```

**Response:**
```typescript
{
  success: boolean;
  queryId: string;
  previousMode: string;
  newMode: string;
  switchTimeMs: number;
  timestamp: string;
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:3000/api/query-control/queries/query-123/permissions \
  -H "Content-Type: application/json" \
  -d '{"permissionMode": "bypassPermissions"}'
```

---

## Customer Management APIs

### 29. GET /api/customers
**Purpose:** List all customers with document counts

**Authentication:** Not required

**Response Schema:**
```typescript
{
  success: boolean;
  customers: Array<{
    name: string;
    email?: string;
    phone?: string;
    company?: string;
    address?: string;
    notes?: string;
    id: string;
    documentCount: number;
    createdAt: string;
  }>;
  count: number;
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:3000/api/customers
```

---

### 29b. POST /api/customers
**Purpose:** Create new customer

**Request Body:**
```typescript
{
  name: string;  // Required
  email?: string;
  phone?: string;
  company?: string;
  address?: string;
  notes?: string;
}
```

**Response:**
```typescript
{
  success: boolean;
  customer: object;
  message: string;
}
```

**Example JavaScript:**
```javascript
const response = await fetch('/api/customers', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Acme Corp',
    email: 'contact@acme.com',
    company: 'Acme Corporation'
  })
});
```

---

### 30. GET /api/customers/[id]
**Purpose:** Get customer details with associated documents

**Response Schema:**
```typescript
{
  success: boolean;
  customer: object;
  documents: Array<object>;
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:3000/api/customers/customer-uuid-123
```

---

### 30b. PUT /api/customers/[id]
**Purpose:** Update customer

**Request Body:** Same as POST /api/customers

**Response:**
```typescript
{
  success: boolean;
  customer: object;
  message: string;
}
```

---

### 30c. DELETE /api/customers/[id]
**Purpose:** Delete customer (fails if documents exist)

**Response:**
```typescript
{
  success: boolean;
  message: string;
}
```

**Constraint:** Cannot delete customer with associated documents

---

## Observability APIs

### 31. GET /api/observability/agents
**Purpose:** Agent activity metrics (active, completed, failed tasks)

**Authentication:** Not required

**Response Schema:**
```typescript
{
  activeAgents: number;
  completedTasks: number;
  failedTasks: number;
  averageDuration: number;
}
```

**Example JavaScript:**
```javascript
const response = await fetch('/api/observability/agents');
const metrics = await response.json();
```

---

### 31b. POST /api/observability/agents
**Purpose:** Update agent activity metrics

**Request Body:**
```typescript
{
  action: 'spawn' | 'complete';
  agentId: string;
  duration?: number;
  status?: 'success' | 'failure';
}
```

---

### 32. GET /api/observability/performance
**Purpose:** Performance metrics (response time, throughput, error rate)

**Authentication:** Not required

**Response Schema:**
```typescript
{
  avgResponseTime: number;
  p95ResponseTime: number;
  throughput: number;
  errorRate: number;
  generatedAt: string;
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:3000/api/observability/performance
```

---

### 33. GET /api/observability/system
**Purpose:** Real-time system metrics (memory, CPU, uptime)

**Authentication:** Not required

**Response Schema:**
```typescript
{
  timestamp: string;
  memory: {
    heapUsed: number;
    heapTotal: number;
    rss: number;
    external: number;
    percentage: number;
  };
  cpu: {
    user: number;
    system: number;
  };
  uptime: number;
  status: 'healthy' | 'warning' | 'critical';
}
```

**Example Python:**
```python
response = requests.get('http://localhost:3000/api/observability/system')
system = response.json()
print(f"Memory Usage: {system['memory']['percentage']:.2f}%")
```

---

## Tags APIs

### 34. GET /api/tags
**Purpose:** List all tags with optional category filter

**Authentication:** Not required

**Query Parameters:**
- `category` (string, optional): Filter by category

**Response Schema:**
```typescript
{
  success: boolean;
  data: Array<{
    name: string;
    category: string;
    color: string;
    description?: string;
    usageCount: number;
  }>;
  count: number;
}
```

**Example cURL:**
```bash
curl -X GET "http://localhost:3000/api/tags?category=threat-intel"
```

---

### 34b. POST /api/tags
**Purpose:** Create new tag

**Request Body:**
```typescript
{
  name: string;  // Required
  category: string;  // Required
  color: string;  // Required
  description?: string;
}
```

**Response:**
```typescript
{
  success: boolean;
  data: object;
  message: string;
}
```

**Example JavaScript:**
```javascript
const response = await fetch('/api/tags', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'APT',
    category: 'threat-actor',
    color: '#FF0000',
    description: 'Advanced Persistent Threat'
  })
});
```

---

### 34c. DELETE /api/tags
**Purpose:** Bulk delete tags

**Request Body:**
```typescript
{
  tagNames: string[];
}
```

**Response:**
```typescript
{
  success: boolean;
  data: {
    deleted: number;
    failed: number;
    total: number;
  };
  message: string;
}
```

---

### 35. GET /api/tags/[id]
**Purpose:** Get tag details with usage count

**Response Schema:**
```typescript
{
  success: boolean;
  data: {
    name: string;
    category: string;
    color: string;
    description?: string;
    usageCount: number;
  };
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:3000/api/tags/APT
```

---

### 35b. PUT /api/tags/[id]
**Purpose:** Update tag

**Request Body:**
```typescript
{
  category?: string;
  color?: string;
  description?: string;
}
```

---

### 35c. DELETE /api/tags/[id]
**Purpose:** Delete tag

**Response:**
```typescript
{
  success: boolean;
  message: string;
}
```

---

### 36. POST /api/tags/assign
**Purpose:** Assign multiple tags to document/entity

**Request Body:**
```typescript
{
  documentId: string;  // Required
  tagNames: string[];  // Required
  taggedBy?: string;
}
```

**Response:**
```typescript
{
  success: boolean;
  data: {
    documentId: string;
    assignedTags: string[];
    allTags: string[];
  };
  message: string;
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:3000/api/tags/assign \
  -H "Content-Type: application/json" \
  -d '{
    "documentId": "doc-123",
    "tagNames": ["APT", "Malware"],
    "taggedBy": "user-456"
  }'
```

---

### 36b. DELETE /api/tags/assign
**Purpose:** Remove tags from document

**Request Body:**
```typescript
{
  documentId: string;
  tagNames: string[];
}
```

**Response:**
```typescript
{
  success: boolean;
  data: {
    documentId: string;
    removedTags: string[];
    remainingTags: string[];
  };
  message: string;
}
```

---

## Utility APIs

### 37. POST /api/search
**Purpose:** Hybrid search across Neo4j and Qdrant

**Authentication:** Not required

**Request Body:**
```typescript
{
  query: string;  // Required
  mode?: 'fulltext' | 'semantic' | 'hybrid';  // Default: 'hybrid'
  limit?: number;  // Max: 100, Default: 10
  k?: number;  // RRF parameter, Default: 60
  filters?: {
    customer?: string;
    tags?: string[];
    dateFrom?: string;
    dateTo?: string;
    nodeTypes?: string[];
    cvssSeverity?: string;
    mitreTactic?: string;
    severities?: string[];
    types?: string[];
  };
}
```

**Response Schema:**
```typescript
{
  success: boolean;
  query: string;
  mode: string;
  filters?: object;
  results: Array<SearchResult>;
  count: number;
  timestamp: string;
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "ransomware attacks",
    "mode": "hybrid",
    "filters": {
      "nodeTypes": ["Malware", "Campaign"],
      "cvssSeverity": "critical"
    }
  }'
```

**Example JavaScript:**
```javascript
const response = await fetch('/api/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'APT campaigns targeting energy sector',
    mode: 'semantic',
    limit: 20
  })
});
const results = await response.json();
```

---

### 37b. GET /api/search/health
**Purpose:** Check search services health

**Response:**
```typescript
{
  status: 'healthy' | 'degraded' | 'error';
  services: {
    neo4j: boolean;
    qdrant: boolean;
    openai: boolean;
  };
  timestamp: string;
}
```

---

### 38. POST /api/upload
**Purpose:** Document upload endpoint

**Authentication:** Not required

**Request:** Multipart form data with files

**Response:**
```typescript
{
  success: boolean;
  files: Array<{
    filename: string;
    path: string;
    size: number;
  }>;
}
```

*(Implementation details not provided in route files)*

---

### 39. POST /api/chat
**Purpose:** AI-powered chat with multi-source data orchestration

**Authentication:** Not required

**Request Body:**
```typescript
{
  messages: Array<{
    role: 'user' | 'assistant';
    content: string;
  }>;
  dataSources: {
    neo4j?: boolean;
    qdrant?: boolean;
    internet?: boolean;
  };
  context: {
    customer?: string;
    scope?: string;
    projectId?: string;
  };
}
```

**Response:** Server-Sent Events (SSE) stream

**Stream Events:**
```typescript
// Sources metadata
data: {"type": "sources", "sources": [...]}

// AI response chunks
data: {"type": "text", "content": "..."}

// Completion signal
data: [DONE]
```

**Example JavaScript:**
```javascript
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    messages: [{
      role: 'user',
      content: 'What are the latest APT campaigns?'
    }],
    dataSources: { neo4j: true, qdrant: true },
    context: { customer: 'acme-corp' }
  })
});

// Handle SSE stream
const reader = response.body.getReader();
const decoder = new TextDecoder();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  const text = decoder.decode(value);
  console.log(text);
}
```

---

### 40. GET /api/backend/test
**Purpose:** Test connectivity to all backend services

**Authentication:** Not required (diagnostic endpoint)

**Response Schema:**
```typescript
{
  timestamp: string;
  services: {
    neo4j: { status: 'connected' | 'error'; error: string | null };
    qdrant: { status: 'connected' | 'error'; error: string | null };
    mysql: { status: 'connected' | 'error'; error: string | null };
    minio: { status: 'connected' | 'error'; error: string | null };
    openspg: { status: 'connected' | 'error'; error: string | null };
  };
  overall: 'all_connected' | 'partial' | 'all_failed';
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:3000/api/backend/test
```

---

### 41. GET /api/health
**Purpose:** Comprehensive health check with service response times

**Authentication:** Not required

**Response Schema:**
```typescript
{
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  services: {
    neo4j: {
      status: 'ok' | 'error' | 'timeout';
      responseTime?: number;
      message?: string;
      details?: object;
    };
    mysql: ServiceHealth;
    qdrant: ServiceHealth;
    minio: ServiceHealth;
  };
  overallHealth: string;
  metadata?: {
    environment: string;
    nodeVersion: string;
  };
}
```

**HTTP Status Codes:**
- 200: All services healthy
- 207: Degraded (partial failure)
- 503: Unhealthy (majority failure)

**Example Python:**
```python
response = requests.get('http://localhost:3000/api/health')
health = response.json()
print(f"System Status: {health['status']}")
print(f"Overall Health: {health['overallHealth']}")
for service, data in health['services'].items():
    print(f"{service}: {data['status']} ({data.get('responseTime', 'N/A')}ms)")
```

---

## Summary Statistics

**Total APIs Documented:** 41

**By Category:**
- Threat Intelligence: 8 APIs (19.5%)
- Dashboard & Metrics: 4 APIs (9.8%)
- Analytics: 7 APIs (17.1%)
- Graph & Neo4j: 3 APIs (7.3%)
- Pipeline: 2 APIs (4.9%)
- Query Control: 7 APIs (17.1%)
- Customer Management: 2 APIs (4.9%)
- Observability: 3 APIs (7.3%)
- Tags: 3 APIs (7.3%)
- Utility: 5 APIs (12.2%)

**Authentication:**
- Required (Clerk): 9 APIs
- Not Required: 32 APIs

**HTTP Methods Used:**
- GET: 30 endpoints
- POST: 15 endpoints
- PUT: 2 endpoints
- DELETE: 7 endpoints

**Key Technologies:**
- Next.js 15 App Router
- Neo4j (bolt://openspg-neo4j:7687)
- Qdrant (http://openspg-qdrant:6333)
- MySQL (openspg-mysql:3306)
- MinIO (openspg-minio:9000)
- OpenAI API (embeddings & chat)
- Clerk (authentication)

---

**Document Version:** v1.0.0
**Last Updated:** 2025-12-12
**Maintainer:** AEON Digital Twin Team
**Container:** aeon-saas-dev
**Base URL:** http://localhost:3000/api
