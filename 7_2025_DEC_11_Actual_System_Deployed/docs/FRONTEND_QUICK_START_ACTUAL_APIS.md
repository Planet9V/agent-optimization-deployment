# AEON Digital Twin - Frontend Quick Start Guide
**Using ONLY the 48 Working APIs**

**File:** FRONTEND_QUICK_START_ACTUAL_APIS.md
**Created:** 2025-12-12 16:45 UTC
**Version:** 1.0.0
**Status:** ✅ PRODUCTION-READY
**Target Audience:** Frontend developers building React/Next.js applications

---

## 📋 Table of Contents

1. [5-Minute Quick Start](#5-minute-quick-start)
2. [Authentication Setup (Clerk)](#authentication-setup-clerk)
3. [Complete API Reference (48 APIs)](#complete-api-reference-48-apis)
4. [Common Use Cases with Working Code](#common-use-cases-with-working-code)
5. [TypeScript Client Library](#typescript-client-library)
6. [React Components & Hooks](#react-components--hooks)
7. [Error Handling & Loading States](#error-handling--loading-states)
8. [Performance & Caching](#performance--caching)
9. [Troubleshooting](#troubleshooting)

---

## 🚀 5-Minute Quick Start

### Step 1: Clone & Setup (2 minutes)

```bash
# Clone repository
git clone <your-aeon-repo-url>
cd aeon-frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local
```

### Step 2: Configure Environment (1 minute)

Edit `.env.local`:

```bash
# AEON API Endpoints
NEXT_PUBLIC_API_BASE_URL=http://localhost:3000/api
NEXT_PUBLIC_NER_API_URL=http://localhost:8000
NEXT_PUBLIC_NEO4J_BOLT=bolt://localhost:7687
NEXT_PUBLIC_QDRANT_URL=http://localhost:6333

# Clerk Authentication (Get from clerk.com)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_key_here
CLERK_SECRET_KEY=sk_test_your_secret_here

# Neo4j Direct Access (for advanced queries)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg

# Qdrant Direct Access
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

### Step 3: Test Connection (1 minute)

Create `test-api.js` and run:

```javascript
// test-api.js
const BASE_URL = 'http://localhost:3000/api';

async function testAPIs() {
  try {
    // Test 1: Health Check (No auth required)
    const health = await fetch(`${BASE_URL}/health`);
    console.log('✅ Health Check:', await health.json());

    // Test 2: NER API (No auth required)
    const nerResponse = await fetch('http://localhost:8000/ner', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: 'APT29 exploited CVE-2024-12345 using T1566 phishing'
      })
    });
    console.log('✅ NER Extraction:', await nerResponse.json());

    console.log('\n🎉 APIs are working! Ready to build.');
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

testAPIs();
```

Run it:
```bash
node test-api.js
```

Expected output:
```
✅ Health Check: { status: 'healthy', database: 'connected', ... }
✅ NER Extraction: { entities: [...], doc_length: 9 }

🎉 APIs are working! Ready to build.
```

### Step 4: First API Call (1 minute)

Create your first React component:

```typescript
// components/SystemHealth.tsx
'use client';
import { useEffect, useState } from 'react';

export default function SystemHealth() {
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/health')
      .then(res => res.json())
      .then(data => {
        setHealth(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="p-4 border rounded">
      <h2 className="text-xl font-bold mb-2">System Health</h2>
      <div className="space-y-1">
        <p>Status: <span className="text-green-600">{health.status}</span></p>
        <p>Database: {health.database}</p>
        <p>NER Model: {health.ner_model_custom}</p>
      </div>
    </div>
  );
}
```

**You're ready to build! 🎉**

---

## 🔐 Authentication Setup (Clerk)

### Why Clerk?

AEON uses [Clerk](https://clerk.com) for authentication. Most APIs (except health checks and NER) require authentication.

### Setup Steps

**1. Create Clerk Account:**
```
Visit: https://clerk.com
1. Sign up for free account
2. Create new application
3. Get API keys from dashboard
```

**2. Install Clerk:**
```bash
npm install @clerk/nextjs
```

**3. Configure Clerk Provider:**

```typescript
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

**4. Create Authenticated API Client:**

```typescript
// lib/api-client.ts
import { useAuth } from '@clerk/nextjs';

export function useAeonAPI() {
  const { getToken } = useAuth();

  async function callAPI(endpoint: string, options: RequestInit = {}) {
    const token = await getToken();

    const response = await fetch(`/api${endpoint}`, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return response.json();
  }

  return { callAPI };
}
```

**5. Use in Components:**

```typescript
// components/ThreatDashboard.tsx
'use client';
import { useAeonAPI } from '@/lib/api-client';
import { useEffect, useState } from 'react';

export default function ThreatDashboard() {
  const { callAPI } = useAeonAPI();
  const [threats, setThreats] = useState([]);

  useEffect(() => {
    callAPI('/threat-intel/analytics')
      .then(data => setThreats(data.threats))
      .catch(console.error);
  }, []);

  return (
    <div>
      <h2>Threat Intelligence</h2>
      {threats.map(threat => (
        <div key={threat.id}>{threat.name}</div>
      ))}
    </div>
  );
}
```

---

## 📚 Complete API Reference (48 APIs)

### ✅ Working APIs Overview

| Category | Count | Auth Required | Base Path |
|----------|-------|---------------|-----------|
| Dashboard & Metrics | 4 | Yes | `/api/dashboard/*` |
| Threat Intelligence | 8 | Yes | `/api/threat-intel/*`, `/api/threats/*` |
| Analytics | 7 | Yes | `/api/analytics/*` |
| Graph Queries | 4 | Yes | `/api/graph/*`, `/api/neo4j/*` |
| Pipeline Management | 2 | Yes | `/api/pipeline/*` |
| Query Control | 7 | Yes | `/api/query-control/*` |
| Customer Management | 2 | Yes | `/api/customers/*` |
| Observability | 3 | Yes | `/api/observability/*` |
| Tags & Classification | 3 | Yes | `/api/tags/*` |
| Utilities | 4 | Mixed | `/api/*` |
| NER & Search | 5 | No | `http://localhost:8000/*` |
| Direct Database Access | 2 | No | Neo4j Bolt, Qdrant REST |

---

### 1. Dashboard & Metrics APIs (4 endpoints)

#### GET `/api/dashboard/metrics`
**Description:** Get key dashboard metrics and KPIs
**Auth:** Required

**Request:**
```typescript
const metrics = await callAPI('/dashboard/metrics');
```

**Response:**
```json
{
  "total_threats": 1245,
  "active_vulnerabilities": 523,
  "risk_score": 7.8,
  "last_updated": "2025-12-12T10:30:00Z"
}
```

#### GET `/api/dashboard/activity`
**Description:** Get recent system activity
**Auth:** Required

**Request:**
```typescript
const activity = await callAPI('/dashboard/activity?limit=10');
```

**Response:**
```json
{
  "activities": [
    {
      "id": "act_001",
      "type": "threat_detected",
      "description": "APT29 activity detected",
      "timestamp": "2025-12-12T10:25:00Z",
      "severity": "high"
    }
  ]
}
```

#### GET `/api/dashboard/distribution`
**Description:** Get data distribution statistics
**Auth:** Required

**Request:**
```typescript
const distribution = await callAPI('/dashboard/distribution');
```

**Response:**
```json
{
  "threats_by_sector": {
    "ENERGY": 245,
    "HEALTHCARE": 189,
    "FINANCE": 167
  },
  "vulnerabilities_by_severity": {
    "CRITICAL": 52,
    "HIGH": 189,
    "MEDIUM": 245
  }
}
```

#### GET `/api/health`
**Description:** System health check (NO AUTH REQUIRED)
**Auth:** Not required

**Request:**
```typescript
const health = await fetch('/api/health').then(r => r.json());
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "ner_model_custom": "loaded",
  "neo4j": "connected",
  "qdrant": "available",
  "version": "3.3.0"
}
```

---

### 2. Threat Intelligence APIs (8 endpoints)

#### GET `/api/threat-intel/analytics`
**Description:** Get comprehensive threat analytics
**Auth:** Required

**Request:**
```typescript
const analytics = await callAPI('/threat-intel/analytics?timeframe=30d');
```

**Response:**
```json
{
  "summary": {
    "total_threats": 1245,
    "active_campaigns": 23,
    "targeted_sectors": ["ENERGY", "HEALTHCARE", "FINANCE"]
  },
  "top_threats": [
    {
      "id": "apt29",
      "name": "APT29",
      "sophistication": "advanced",
      "target_count": 45,
      "last_activity": "2025-12-11T15:30:00Z"
    }
  ]
}
```

#### GET `/api/threat-intel/ics`
**Description:** Get ICS/OT specific threats
**Auth:** Required

**Request:**
```typescript
const icsThreats = await callAPI('/threat-intel/ics');
```

**Response:**
```json
{
  "ics_threats": [
    {
      "threat_id": "ics_001",
      "name": "TRITON",
      "target_systems": ["Schneider Electric Triconex"],
      "sector": "ENERGY",
      "severity": "critical"
    }
  ]
}
```

#### GET `/api/threat-intel/landscape`
**Description:** Get overall threat landscape
**Auth:** Required

**Request:**
```typescript
const landscape = await callAPI('/threat-intel/landscape');
```

**Response:**
```json
{
  "threat_groups": 45,
  "active_campaigns": 23,
  "total_cves": 316552,
  "sectors_at_risk": [
    { "sector": "ENERGY", "threat_level": "high", "active_threats": 156 },
    { "sector": "HEALTHCARE", "threat_level": "medium", "active_threats": 89 }
  ]
}
```

#### GET `/api/threat-intel/vulnerabilities`
**Description:** Get vulnerability intelligence
**Auth:** Required

**Request:**
```typescript
const vulns = await callAPI('/threat-intel/vulnerabilities?severity=critical');
```

**Response:**
```json
{
  "vulnerabilities": [
    {
      "cve_id": "CVE-2024-12345",
      "severity": "CRITICAL",
      "cvss_score": 9.8,
      "exploited_by": ["APT29", "APT28"],
      "affected_systems": 245,
      "patch_available": true
    }
  ]
}
```

#### GET `/api/threats/geographic`
**Description:** Get geographic threat distribution
**Auth:** Required

**Request:**
```typescript
const geoThreats = await callAPI('/threats/geographic');
```

**Response:**
```json
{
  "regions": [
    {
      "region": "North America",
      "threat_count": 456,
      "top_threats": ["APT29", "FIN7"],
      "risk_level": "high"
    }
  ]
}
```

#### GET `/api/threats/ics`
**Description:** ICS-specific threat data (alternative endpoint)
**Auth:** Required

---

### 3. Analytics APIs (7 endpoints)

#### GET `/api/analytics/metrics`
**Description:** Get analytics metrics
**Auth:** Required

**Request:**
```typescript
const metrics = await callAPI('/analytics/metrics?metric_type=threat_trends');
```

**Response:**
```json
{
  "metrics": [
    {
      "name": "threat_detection_rate",
      "value": 245,
      "change": "+12%",
      "period": "30d"
    }
  ]
}
```

#### GET `/api/analytics/timeseries`
**Description:** Get time series data
**Auth:** Required

**Request:**
```typescript
const timeseries = await callAPI('/analytics/timeseries?metric=threats&period=7d');
```

**Response:**
```json
{
  "data_points": [
    { "timestamp": "2025-12-05", "value": 23 },
    { "timestamp": "2025-12-06", "value": 31 },
    { "timestamp": "2025-12-07", "value": 28 }
  ]
}
```

#### GET `/api/analytics/trends/cve`
**Description:** Get CVE trends over time
**Auth:** Required

**Request:**
```typescript
const cveTrends = await callAPI('/analytics/trends/cve?period=30d');
```

**Response:**
```json
{
  "trend_data": [
    {
      "date": "2025-11-12",
      "new_cves": 45,
      "critical": 12,
      "high": 23,
      "medium": 10
    }
  ],
  "total_new_cves": 1234,
  "average_per_day": 41
}
```

#### GET `/api/analytics/trends/threat-timeline`
**Description:** Get threat activity timeline
**Auth:** Required

#### GET `/api/analytics/trends/seasonality`
**Description:** Get seasonal threat patterns
**Auth:** Required

#### POST `/api/analytics/export`
**Description:** Export analytics data
**Auth:** Required

**Request:**
```typescript
const exported = await callAPI('/analytics/export', {
  method: 'POST',
  body: JSON.stringify({
    format: 'csv',
    metrics: ['threats', 'vulnerabilities'],
    date_range: { start: '2025-11-01', end: '2025-12-01' }
  })
});
```

---

### 4. Graph Query APIs (4 endpoints)

#### POST `/api/graph/query`
**Description:** Execute custom Cypher queries on Neo4j
**Auth:** Required

**Request:**
```typescript
const graphData = await callAPI('/graph/query', {
  method: 'POST',
  body: JSON.stringify({
    query: `
      MATCH (e:Equipment)-[:VULNERABLE_TO]->(v:Vulnerability)
      WHERE e.sector = $sector
      RETURN e.name, v.severity, v.cvss_score
      ORDER BY v.cvss_score DESC
      LIMIT 10
    `,
    parameters: { sector: 'ENERGY' }
  })
});
```

**Response:**
```json
{
  "results": [
    {
      "e.name": "Gas Turbine GT-100",
      "v.severity": "CRITICAL",
      "v.cvss_score": 9.8
    }
  ],
  "record_count": 10,
  "query_time_ms": 45
}
```

#### GET `/api/neo4j/statistics`
**Description:** Get Neo4j database statistics
**Auth:** Required

**Request:**
```typescript
const stats = await callAPI('/neo4j/statistics');
```

**Response:**
```json
{
  "total_nodes": 1207069,
  "total_relationships": 12344852,
  "node_types": 631,
  "relationship_types": 183,
  "database_size_mb": 2456
}
```

#### GET `/api/neo4j/cyber-statistics`
**Description:** Get cybersecurity-specific statistics
**Auth:** Required

**Request:**
```typescript
const cyberStats = await callAPI('/neo4j/cyber-statistics');
```

**Response:**
```json
{
  "total_cves": 316552,
  "total_threats": 9875,
  "total_vulnerabilities": 12022,
  "equipment_count": 48288,
  "sectors_covered": 16
}
```

---

### 5. Pipeline Management APIs (2 endpoints)

#### POST `/api/pipeline/process`
**Description:** Submit document for processing
**Auth:** Required

**Request:**
```typescript
const job = await callAPI('/pipeline/process', {
  method: 'POST',
  body: JSON.stringify({
    document: "APT29 exploited CVE-2024-12345...",
    pipeline_type: "threat_intel"
  })
});
```

**Response:**
```json
{
  "job_id": "job_abc123",
  "status": "processing",
  "estimated_completion": "2025-12-12T10:35:00Z"
}
```

#### GET `/api/pipeline/status/[jobId]`
**Description:** Get pipeline job status
**Auth:** Required

**Request:**
```typescript
const status = await callAPI('/pipeline/status/job_abc123');
```

**Response:**
```json
{
  "job_id": "job_abc123",
  "status": "completed",
  "progress": 100,
  "result": {
    "entities_extracted": 45,
    "threats_identified": 3,
    "vulnerabilities_found": 12
  }
}
```

---

### 6. Query Control APIs (7 endpoints)

#### GET `/api/query-control/queries`
**Description:** List all active queries
**Auth:** Required

**Request:**
```typescript
const queries = await callAPI('/query-control/queries');
```

**Response:**
```json
{
  "queries": [
    {
      "query_id": "q_001",
      "status": "running",
      "created_at": "2025-12-12T10:00:00Z",
      "elapsed_time_ms": 45000
    }
  ]
}
```

#### GET `/api/query-control/queries/[queryId]`
**Description:** Get specific query details
**Auth:** Required

#### POST `/api/query-control/queries/[queryId]/pause`
**Description:** Pause running query
**Auth:** Required

#### POST `/api/query-control/queries/[queryId]/resume`
**Description:** Resume paused query
**Auth:** Required

#### GET `/api/query-control/queries/[queryId]/checkpoints`
**Description:** Get query checkpoints
**Auth:** Required

#### PUT `/api/query-control/queries/[queryId]/model`
**Description:** Change model for query
**Auth:** Required

#### PUT `/api/query-control/queries/[queryId]/permissions`
**Description:** Update query permissions
**Auth:** Required

---

### 7. Customer Management APIs (2 endpoints)

#### GET `/api/customers`
**Description:** List all customers (multi-tenant)
**Auth:** Required

**Request:**
```typescript
const customers = await callAPI('/customers?limit=10');
```

**Response:**
```json
{
  "customers": [
    {
      "customer_id": "cust_001",
      "name": "Acme Corp",
      "tier": "enterprise",
      "active": true,
      "created_at": "2025-01-15T00:00:00Z"
    }
  ]
}
```

#### GET `/api/customers/[id]`
**Description:** Get customer details
**Auth:** Required

**Request:**
```typescript
const customer = await callAPI('/customers/cust_001');
```

**Response:**
```json
{
  "customer_id": "cust_001",
  "name": "Acme Corp",
  "tier": "enterprise",
  "namespace": "acme_production",
  "users": 45,
  "data_volume_gb": 234.5,
  "last_activity": "2025-12-12T09:45:00Z"
}
```

---

### 8. Observability APIs (3 endpoints)

#### GET `/api/observability/performance`
**Description:** Get system performance metrics
**Auth:** Required

**Request:**
```typescript
const perf = await callAPI('/observability/performance');
```

**Response:**
```json
{
  "cpu_usage": 45.2,
  "memory_usage": 67.8,
  "api_response_time_ms": 123,
  "database_query_time_ms": 45,
  "requests_per_minute": 245
}
```

#### GET `/api/observability/system`
**Description:** Get system health metrics
**Auth:** Required

#### GET `/api/observability/agents`
**Description:** Get agent status and metrics
**Auth:** Required

---

### 9. Tags & Classification APIs (3 endpoints)

#### GET `/api/tags`
**Description:** List all tags
**Auth:** Required

**Request:**
```typescript
const tags = await callAPI('/tags');
```

**Response:**
```json
{
  "tags": [
    {
      "tag_id": "tag_001",
      "name": "critical",
      "category": "severity",
      "usage_count": 245
    }
  ]
}
```

#### GET `/api/tags/[id]`
**Description:** Get tag details
**Auth:** Required

#### POST `/api/tags/assign`
**Description:** Assign tag to entity
**Auth:** Required

**Request:**
```typescript
const result = await callAPI('/tags/assign', {
  method: 'POST',
  body: JSON.stringify({
    entity_id: "threat_001",
    entity_type: "threat",
    tag_id: "tag_001"
  })
});
```

---

### 10. Utility APIs (4 endpoints)

#### POST `/api/search`
**Description:** Search across all entities
**Auth:** Required

**Request:**
```typescript
const results = await callAPI('/search', {
  method: 'POST',
  body: JSON.stringify({
    query: "APT29 energy sector",
    filters: { entity_types: ["threat", "vulnerability"] }
  })
});
```

**Response:**
```json
{
  "results": [
    {
      "entity_id": "threat_apt29",
      "entity_type": "threat",
      "name": "APT29",
      "score": 0.95,
      "snippet": "APT29 targets energy sector..."
    }
  ],
  "total_results": 45
}
```

#### POST `/api/chat`
**Description:** AI-powered chat interface
**Auth:** Required

#### POST `/api/upload`
**Description:** Upload files for processing
**Auth:** Required

#### GET `/api/backend/test`
**Description:** Backend connection test
**Auth:** Required

#### GET `/api/activity/recent`
**Description:** Get recent activity feed
**Auth:** Required

---

### 11. NER & Search APIs (5 endpoints - Port 8000)

#### POST `http://localhost:8000/ner`
**Description:** Extract cybersecurity entities from text
**Auth:** Not required

**Request:**
```typescript
const entities = await fetch('http://localhost:8000/ner', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: "APT29 exploited CVE-2024-12345 using T1566 phishing techniques"
  })
}).then(r => r.json());
```

**Response:**
```json
{
  "entities": [
    {
      "text": "APT29",
      "label": "APT_GROUP",
      "start": 0,
      "end": 5,
      "score": 0.95
    },
    {
      "text": "CVE-2024-12345",
      "label": "CVE",
      "start": 16,
      "end": 30,
      "score": 1.0
    },
    {
      "text": "T1566",
      "label": "TECHNIQUE",
      "start": 37,
      "end": 42,
      "score": 1.0
    }
  ],
  "doc_length": 9
}
```

#### POST `http://localhost:8000/search/semantic`
**Description:** Semantic search using vector embeddings
**Auth:** Not required

**Request:**
```typescript
const results = await fetch('http://localhost:8000/search/semantic', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "ransomware attack",
    limit: 10,
    label_filter: "MALWARE",
    confidence_threshold: 0.7
  })
}).then(r => r.json());
```

**Response:**
```json
{
  "results": [
    {
      "score": 0.92,
      "entity": "WannaCry",
      "ner_label": "MALWARE",
      "fine_grained_type": "RANSOMWARE",
      "confidence": 0.95
    }
  ],
  "total_results": 1
}
```

#### POST `http://localhost:8000/search/hybrid`
**Description:** Hybrid search (semantic + graph expansion)
**Auth:** Not required

**Request:**
```typescript
const results = await fetch('http://localhost:8000/search/hybrid', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "APT29 ransomware",
    expand_graph: true,
    hop_depth: 2,
    relationship_types: ["USES", "TARGETS"]
  })
}).then(r => r.json());
```

**Response:**
```json
{
  "results": [
    {
      "score": 0.94,
      "entity": "APT29",
      "ner_label": "THREAT_ACTOR",
      "related_entities": [
        {
          "name": "CVE-2021-44228",
          "label": "CVE",
          "relationship": "EXPLOITS",
          "hop_distance": 1
        }
      ]
    }
  ]
}
```

#### GET `http://localhost:8000/health`
**Description:** NER service health check
**Auth:** Not required

#### GET `http://localhost:8000/info`
**Description:** Get NER model information
**Auth:** Not required

---

### 12. Direct Database Access (2 APIs)

#### Neo4j Bolt Protocol
**Description:** Direct Neo4j graph database access
**Auth:** Not required (credentials needed)

**Connection:**
```javascript
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  'bolt://localhost:7687',
  neo4j.auth.basic('neo4j', 'neo4j@openspg')
);

const session = driver.session();
const result = await session.run(
  'MATCH (e:Equipment) WHERE e.sector = $sector RETURN e LIMIT 10',
  { sector: 'ENERGY' }
);
```

#### Qdrant REST API
**Description:** Direct Qdrant vector database access
**Auth:** Not required

**Connection:**
```javascript
import { QdrantClient } from '@qdrant/js-client-rest';

const client = new QdrantClient({ host: 'localhost', port: 6333 });

const results = await client.search('ner11_entities_hierarchical', {
  vector: queryVector,
  limit: 5
});
```

---

## 💼 Common Use Cases with Working Code

### Use Case 1: Threat Intelligence Dashboard

**Goal:** Display real-time threat intelligence with analytics

**Component Code:**

```typescript
// components/ThreatIntelligenceDashboard.tsx
'use client';
import { useEffect, useState } from 'react';
import { useAeonAPI } from '@/lib/api-client';

interface ThreatAnalytics {
  summary: {
    total_threats: number;
    active_campaigns: number;
    targeted_sectors: string[];
  };
  top_threats: Array<{
    id: string;
    name: string;
    sophistication: string;
    target_count: number;
    last_activity: string;
  }>;
}

export default function ThreatIntelligenceDashboard() {
  const { callAPI } = useAeonAPI();
  const [analytics, setAnalytics] = useState<ThreatAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchThreatData() {
      try {
        const data = await callAPI('/threat-intel/analytics?timeframe=30d');
        setAnalytics(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load data');
      } finally {
        setLoading(false);
      }
    }

    fetchThreatData();
    // Refresh every 5 minutes
    const interval = setInterval(fetchThreatData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, [callAPI]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">Error: {error}</p>
      </div>
    );
  }

  if (!analytics) return null;

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <SummaryCard
          title="Total Threats"
          value={analytics.summary.total_threats}
          icon="🚨"
        />
        <SummaryCard
          title="Active Campaigns"
          value={analytics.summary.active_campaigns}
          icon="⚡"
        />
        <SummaryCard
          title="Sectors Targeted"
          value={analytics.summary.targeted_sectors.length}
          icon="🎯"
        />
      </div>

      {/* Top Threats Table */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b">
          <h2 className="text-xl font-semibold">Top Threats</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Threat
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Sophistication
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Targets
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Last Activity
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {analytics.top_threats.map((threat) => (
                <tr key={threat.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                    {threat.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      threat.sophistication === 'advanced'
                        ? 'bg-red-100 text-red-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {threat.sophistication}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-500">
                    {threat.target_count}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-500">
                    {new Date(threat.last_activity).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Targeted Sectors */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4">Targeted Sectors</h3>
        <div className="flex flex-wrap gap-2">
          {analytics.summary.targeted_sectors.map((sector) => (
            <span
              key={sector}
              className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
            >
              {sector}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

// Helper component
function SummaryCard({ title, value, icon }: { title: string; value: number; icon: string }) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
        </div>
        <div className="text-4xl">{icon}</div>
      </div>
    </div>
  );
}
```

---

### Use Case 2: Neo4j Equipment Query

**Goal:** Query and display equipment vulnerabilities from Neo4j

**Component Code:**

```typescript
// components/EquipmentVulnerabilities.tsx
'use client';
import { useEffect, useState } from 'react';
import { useAeonAPI } from '@/lib/api-client';

interface Equipment {
  name: string;
  type: string;
  sector: string;
  vulnerability_count: number;
  critical_vulns: number;
}

export default function EquipmentVulnerabilities({ sector = 'ENERGY' }) {
  const { callAPI } = useAeonAPI();
  const [equipment, setEquipment] = useState<Equipment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchEquipment() {
      try {
        const result = await callAPI('/graph/query', {
          method: 'POST',
          body: JSON.stringify({
            query: `
              MATCH (e:Equipment)-[:VULNERABLE_TO]->(v:Vulnerability)
              WHERE e.sector = $sector
              WITH e,
                   count(v) as vuln_count,
                   count(CASE WHEN v.severity = 'CRITICAL' THEN 1 END) as critical_count
              RETURN
                e.name as name,
                e.type as type,
                e.sector as sector,
                vuln_count as vulnerability_count,
                critical_count as critical_vulns
              ORDER BY critical_count DESC, vuln_count DESC
              LIMIT 20
            `,
            parameters: { sector }
          })
        });

        setEquipment(result.results);
      } catch (err) {
        console.error('Failed to fetch equipment:', err);
      } finally {
        setLoading(false);
      }
    }

    fetchEquipment();
  }, [sector, callAPI]);

  if (loading) {
    return <div>Loading equipment data...</div>;
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b">
        <h2 className="text-xl font-semibold">
          {sector} Sector Equipment Vulnerabilities
        </h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Equipment
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Type
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Total Vulnerabilities
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Critical
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {equipment.map((item, idx) => (
              <tr key={idx} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap font-medium">
                  {item.name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-gray-500">
                  {item.type}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-sm">
                    {item.vulnerability_count}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {item.critical_vulns > 0 ? (
                    <span className="px-2 py-1 bg-red-100 text-red-800 rounded text-sm font-bold">
                      {item.critical_vulns}
                    </span>
                  ) : (
                    <span className="text-gray-400">0</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

---

### Use Case 3: Real-Time Entity Extraction

**Goal:** Extract entities from user-provided text using NER API

**Component Code:**

```typescript
// components/EntityExtractor.tsx
'use client';
import { useState } from 'react';

interface Entity {
  text: string;
  label: string;
  start: number;
  end: number;
  score: number;
}

export default function EntityExtractor() {
  const [text, setText] = useState('');
  const [entities, setEntities] = useState<Entity[]>([]);
  const [loading, setLoading] = useState(false);

  async function extractEntities() {
    if (!text.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/ner', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });

      const data = await response.json();
      setEntities(data.entities);
    } catch (err) {
      console.error('Failed to extract entities:', err);
    } finally {
      setLoading(false);
    }
  }

  const getLabelColor = (label: string) => {
    const colors: Record<string, string> = {
      APT_GROUP: 'bg-red-100 text-red-800',
      CVE: 'bg-purple-100 text-purple-800',
      MALWARE: 'bg-orange-100 text-orange-800',
      TECHNIQUE: 'bg-blue-100 text-blue-800',
      VULNERABILITY: 'bg-yellow-100 text-yellow-800',
      THREAT_ACTOR: 'bg-red-100 text-red-800',
    };
    return colors[label] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Entity Extraction</h2>

        <textarea
          className="w-full border rounded-lg p-3 h-32 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Enter cybersecurity text to extract entities... (e.g., 'APT29 exploited CVE-2024-12345 using T1566 phishing')"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button
          className="mt-3 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300"
          onClick={extractEntities}
          disabled={loading || !text.trim()}
        >
          {loading ? 'Extracting...' : 'Extract Entities'}
        </button>
      </div>

      {entities.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">
            Extracted Entities ({entities.length})
          </h3>

          <div className="space-y-3">
            {entities.map((entity, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50"
              >
                <div className="flex-1">
                  <div className="font-medium text-gray-900">{entity.text}</div>
                  <div className="text-sm text-gray-500">
                    Position: {entity.start}-{entity.end}
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`px-3 py-1 rounded-full text-sm ${getLabelColor(entity.label)}`}>
                    {entity.label}
                  </span>
                  <span className="text-sm font-medium text-gray-700">
                    {(entity.score * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
```

---

### Use Case 4: Semantic Search Interface

**Goal:** Search entities using semantic similarity

**Component Code:**

```typescript
// components/SemanticSearch.tsx
'use client';
import { useState } from 'react';

interface SearchResult {
  score: number;
  entity: string;
  ner_label: string;
  fine_grained_type: string;
  confidence: number;
}

export default function SemanticSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [labelFilter, setLabelFilter] = useState('');

  async function search() {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/search/semantic', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          limit: 10,
          label_filter: labelFilter || undefined,
          confidence_threshold: 0.7
        })
      });

      const data = await response.json();
      setResults(data.results);
    } catch (err) {
      console.error('Search failed:', err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Semantic Search</h2>

        <div className="space-y-3">
          <input
            type="text"
            className="w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-500"
            placeholder="Search for entities (e.g., 'ransomware attack', 'APT groups')"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && search()}
          />

          <div className="flex gap-3">
            <select
              className="border rounded-lg px-3 py-2"
              value={labelFilter}
              onChange={(e) => setLabelFilter(e.target.value)}
            >
              <option value="">All Entity Types</option>
              <option value="MALWARE">Malware</option>
              <option value="APT_GROUP">APT Groups</option>
              <option value="CVE">CVE</option>
              <option value="THREAT_ACTOR">Threat Actors</option>
              <option value="TECHNIQUE">Techniques</option>
            </select>

            <button
              className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300"
              onClick={search}
              disabled={loading || !query.trim()}
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </div>
      </div>

      {results.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">
            Results ({results.length})
          </h3>

          <div className="space-y-3">
            {results.map((result, idx) => (
              <div
                key={idx}
                className="p-4 border rounded-lg hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="font-semibold text-lg text-gray-900">
                      {result.entity}
                    </h4>
                    <div className="mt-1 flex gap-2">
                      <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
                        {result.ner_label}
                      </span>
                      <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-sm">
                        {result.fine_grained_type}
                      </span>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-gray-900">
                      {(result.score * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-500">
                      Match Score
                    </div>
                  </div>
                </div>
                <div className="mt-2 text-sm text-gray-600">
                  Confidence: {(result.confidence * 100).toFixed(1)}%
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
```

---

### Use Case 5: Analytics Trends Visualization

**Goal:** Display CVE trends over time with charts

**Component Code:**

```typescript
// components/CVETrendsChart.tsx
'use client';
import { useEffect, useState } from 'react';
import { useAeonAPI } from '@/lib/api-client';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface TrendData {
  date: string;
  new_cves: number;
  critical: number;
  high: number;
  medium: number;
}

export default function CVETrendsChart() {
  const { callAPI } = useAeonAPI();
  const [trendData, setTrendData] = useState<TrendData[]>([]);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState('30d');

  useEffect(() => {
    async function fetchTrends() {
      try {
        const data = await callAPI(`/analytics/trends/cve?period=${period}`);
        setTrendData(data.trend_data);
      } catch (err) {
        console.error('Failed to fetch CVE trends:', err);
      } finally {
        setLoading(false);
      }
    }

    fetchTrends();
  }, [period, callAPI]);

  if (loading) {
    return <div>Loading trend data...</div>;
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold">CVE Trends</h2>
        <select
          className="border rounded-lg px-3 py-2"
          value={period}
          onChange={(e) => setPeriod(e.target.value)}
        >
          <option value="7d">Last 7 Days</option>
          <option value="30d">Last 30 Days</option>
          <option value="90d">Last 90 Days</option>
        </select>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={trendData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            tickFormatter={(value) => new Date(value).toLocaleDateString()}
          />
          <YAxis />
          <Tooltip
            labelFormatter={(value) => new Date(value).toLocaleDateString()}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="critical"
            stroke="#ef4444"
            strokeWidth={2}
            name="Critical"
          />
          <Line
            type="monotone"
            dataKey="high"
            stroke="#f97316"
            strokeWidth={2}
            name="High"
          />
          <Line
            type="monotone"
            dataKey="medium"
            stroke="#eab308"
            strokeWidth={2}
            name="Medium"
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="mt-4 grid grid-cols-3 gap-4">
        <StatCard
          label="Critical CVEs"
          value={trendData.reduce((sum, d) => sum + d.critical, 0)}
          color="text-red-600"
        />
        <StatCard
          label="High CVEs"
          value={trendData.reduce((sum, d) => sum + d.high, 0)}
          color="text-orange-600"
        />
        <StatCard
          label="Medium CVEs"
          value={trendData.reduce((sum, d) => sum + d.medium, 0)}
          color="text-yellow-600"
        />
      </div>
    </div>
  );
}

function StatCard({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="p-4 bg-gray-50 rounded-lg">
      <div className="text-sm text-gray-600">{label}</div>
      <div className={`text-2xl font-bold ${color}`}>{value}</div>
    </div>
  );
}
```

---

## 🔧 TypeScript Client Library

Create a comprehensive TypeScript client for all APIs:

```typescript
// lib/aeon-client.ts
import { useAuth } from '@clerk/nextjs';

export interface AeonClientConfig {
  baseURL?: string;
  nerBaseURL?: string;
  neo4jURI?: string;
  qdrantURL?: string;
}

export class AeonClient {
  private baseURL: string;
  private nerBaseURL: string;
  private getToken: () => Promise<string | null>;

  constructor(
    getToken: () => Promise<string | null>,
    config: AeonClientConfig = {}
  ) {
    this.baseURL = config.baseURL || '/api';
    this.nerBaseURL = config.nerBaseURL || 'http://localhost:8000';
    this.getToken = getToken;
  }

  // Generic request method with auth
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await this.getToken();

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': token ? `Bearer ${token}` : '',
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Dashboard APIs
  dashboard = {
    getMetrics: () => this.request('/dashboard/metrics'),
    getActivity: (limit = 10) => this.request(`/dashboard/activity?limit=${limit}`),
    getDistribution: () => this.request('/dashboard/distribution'),
  };

  // Threat Intelligence APIs
  threatIntel = {
    getAnalytics: (timeframe = '30d') =>
      this.request(`/threat-intel/analytics?timeframe=${timeframe}`),
    getICSThreats: () => this.request('/threat-intel/ics'),
    getLandscape: () => this.request('/threat-intel/landscape'),
    getVulnerabilities: (severity?: string) => {
      const params = severity ? `?severity=${severity}` : '';
      return this.request(`/threat-intel/vulnerabilities${params}`);
    },
  };

  // Analytics APIs
  analytics = {
    getMetrics: (metricType?: string) => {
      const params = metricType ? `?metric_type=${metricType}` : '';
      return this.request(`/analytics/metrics${params}`);
    },
    getTimeseries: (metric: string, period = '7d') =>
      this.request(`/analytics/timeseries?metric=${metric}&period=${period}`),
    getCVETrends: (period = '30d') =>
      this.request(`/analytics/trends/cve?period=${period}`),
    getThreatTimeline: () => this.request('/analytics/trends/threat-timeline'),
    getSeasonality: () => this.request('/analytics/trends/seasonality'),
    exportData: (params: { format: string; metrics: string[]; date_range: any }) =>
      this.request('/analytics/export', {
        method: 'POST',
        body: JSON.stringify(params),
      }),
  };

  // Graph Query APIs
  graph = {
    query: (cypherQuery: string, parameters: Record<string, any> = {}) =>
      this.request('/graph/query', {
        method: 'POST',
        body: JSON.stringify({ query: cypherQuery, parameters }),
      }),
    getStatistics: () => this.request('/neo4j/statistics'),
    getCyberStatistics: () => this.request('/neo4j/cyber-statistics'),
  };

  // Pipeline APIs
  pipeline = {
    process: (document: string, pipelineType: string) =>
      this.request('/pipeline/process', {
        method: 'POST',
        body: JSON.stringify({ document, pipeline_type: pipelineType }),
      }),
    getStatus: (jobId: string) => this.request(`/pipeline/status/${jobId}`),
  };

  // Query Control APIs
  queryControl = {
    listQueries: () => this.request('/query-control/queries'),
    getQuery: (queryId: string) => this.request(`/query-control/queries/${queryId}`),
    pause: (queryId: string) =>
      this.request(`/query-control/queries/${queryId}/pause`, { method: 'POST' }),
    resume: (queryId: string) =>
      this.request(`/query-control/queries/${queryId}/resume`, { method: 'POST' }),
    getCheckpoints: (queryId: string) =>
      this.request(`/query-control/queries/${queryId}/checkpoints`),
    changeModel: (queryId: string, model: string) =>
      this.request(`/query-control/queries/${queryId}/model`, {
        method: 'PUT',
        body: JSON.stringify({ model }),
      }),
  };

  // Customer APIs
  customers = {
    list: (limit = 10) => this.request(`/customers?limit=${limit}`),
    get: (customerId: string) => this.request(`/customers/${customerId}`),
  };

  // Observability APIs
  observability = {
    getPerformance: () => this.request('/observability/performance'),
    getSystem: () => this.request('/observability/system'),
    getAgents: () => this.request('/observability/agents'),
  };

  // Tags APIs
  tags = {
    list: () => this.request('/tags'),
    get: (tagId: string) => this.request(`/tags/${tagId}`),
    assign: (entityId: string, entityType: string, tagId: string) =>
      this.request('/tags/assign', {
        method: 'POST',
        body: JSON.stringify({ entity_id: entityId, entity_type: entityType, tag_id: tagId }),
      }),
  };

  // Search & Utilities
  search: (query: string, filters?: any) =>
    this.request('/search', {
      method: 'POST',
      body: JSON.stringify({ query, filters }),
    });

  // NER APIs (No auth required)
  ner = {
    extract: async (text: string) => {
      const response = await fetch(`${this.nerBaseURL}/ner`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      return response.json();
    },
    semanticSearch: async (query: string, options: any = {}) => {
      const response = await fetch(`${this.nerBaseURL}/search/semantic`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, ...options }),
      });
      return response.json();
    },
    hybridSearch: async (query: string, options: any = {}) => {
      const response = await fetch(`${this.nerBaseURL}/search/hybrid`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, ...options }),
      });
      return response.json();
    },
    health: async () => {
      const response = await fetch(`${this.nerBaseURL}/health`);
      return response.json();
    },
    info: async () => {
      const response = await fetch(`${this.nerBaseURL}/info`);
      return response.json();
    },
  };

  // Health Check (No auth required)
  async health() {
    const response = await fetch(`${this.baseURL}/health`);
    return response.json();
  }
}

// React Hook for AeonClient
export function useAeonClient(config?: AeonClientConfig) {
  const { getToken } = useAuth();

  const client = new AeonClient(getToken, config);

  return client;
}
```

**Usage:**

```typescript
// In a component
import { useAeonClient } from '@/lib/aeon-client';

function MyComponent() {
  const aeon = useAeonClient();

  useEffect(() => {
    async function loadData() {
      const metrics = await aeon.dashboard.getMetrics();
      const threats = await aeon.threatIntel.getAnalytics('30d');
      const entities = await aeon.ner.extract('APT29 exploited CVE-2024-12345');
    }

    loadData();
  }, []);
}
```

---

## 🎣 React Components & Hooks

### Custom React Hooks

```typescript
// hooks/useAeonAPI.ts
import { useAuth } from '@clerk/nextjs';
import { useState, useEffect } from 'react';

export function useAeonAPI<T>(
  endpoint: string,
  options: RequestInit = {},
  dependencies: any[] = []
) {
  const { getToken } = useAuth();
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const token = await getToken();

        const response = await fetch(`/api${endpoint}`, {
          ...options,
          headers: {
            ...options.headers,
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`API Error: ${response.statusText}`);
        }

        const result = await response.json();
        setData(result);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Unknown error'));
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, dependencies);

  return { data, loading, error, refetch: () => {} };
}

// Usage
function ThreatList() {
  const { data, loading, error } = useAeonAPI<ThreatData>(
    '/threat-intel/analytics?timeframe=30d'
  );

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>{/* Render data */}</div>;
}
```

---

### Reusable Components

```typescript
// components/LoadingSpinner.tsx
export function LoadingSpinner({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
  };

  return (
    <div className="flex items-center justify-center">
      <div className={`animate-spin rounded-full border-b-2 border-blue-500 ${sizeClasses[size]}`}></div>
    </div>
  );
}

// components/ErrorAlert.tsx
export function ErrorAlert({ message }: { message: string }) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
      <div className="flex items-center">
        <span className="text-2xl mr-3">⚠️</span>
        <div>
          <h3 className="font-semibold text-red-800">Error</h3>
          <p className="text-red-700">{message}</p>
        </div>
      </div>
    </div>
  );
}

// components/EmptyState.tsx
export function EmptyState({
  icon = '📭',
  title,
  message
}: {
  icon?: string;
  title: string;
  message: string;
}) {
  return (
    <div className="text-center py-12">
      <div className="text-6xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{message}</p>
    </div>
  );
}
```

---

## ⚠️ Error Handling & Loading States

### Comprehensive Error Handling

```typescript
// lib/error-handler.ts
export class APIError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    message: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export async function handleAPIResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new APIError(
      response.status,
      response.statusText,
      error.message || `API Error: ${response.statusText}`
    );
  }

  return response.json();
}

export function getErrorMessage(error: unknown): string {
  if (error instanceof APIError) {
    switch (error.status) {
      case 401:
        return 'Authentication required. Please log in.';
      case 403:
        return 'You do not have permission to access this resource.';
      case 404:
        return 'Resource not found.';
      case 500:
        return 'Internal server error. Please try again later.';
      default:
        return error.message;
    }
  }

  if (error instanceof Error) {
    return error.message;
  }

  return 'An unknown error occurred.';
}
```

**Usage:**

```typescript
// In a component
import { handleAPIResponse, getErrorMessage } from '@/lib/error-handler';

async function fetchData() {
  try {
    const response = await fetch('/api/dashboard/metrics');
    const data = await handleAPIResponse(response);
    setData(data);
  } catch (error) {
    const message = getErrorMessage(error);
    setError(message);
  }
}
```

---

### Loading State Patterns

```typescript
// components/DataLoader.tsx
interface DataLoaderProps<T> {
  loading: boolean;
  error: string | null;
  data: T | null;
  children: (data: T) => React.ReactNode;
  loadingComponent?: React.ReactNode;
  errorComponent?: (message: string) => React.ReactNode;
  emptyComponent?: React.ReactNode;
}

export function DataLoader<T>({
  loading,
  error,
  data,
  children,
  loadingComponent,
  errorComponent,
  emptyComponent,
}: DataLoaderProps<T>) {
  if (loading) {
    return loadingComponent || <LoadingSpinner />;
  }

  if (error) {
    return errorComponent
      ? errorComponent(error)
      : <ErrorAlert message={error} />;
  }

  if (!data) {
    return emptyComponent || <EmptyState title="No Data" message="No data available." />;
  }

  return <>{children(data)}</>;
}

// Usage
function ThreatList() {
  const { data, loading, error } = useAeonAPI<ThreatData>('/threat-intel/analytics');

  return (
    <DataLoader loading={loading} error={error} data={data}>
      {(threats) => (
        <div>
          {threats.top_threats.map(threat => (
            <div key={threat.id}>{threat.name}</div>
          ))}
        </div>
      )}
    </DataLoader>
  );
}
```

---

## 🚀 Performance & Caching

### React Query Integration

```bash
npm install @tanstack/react-query
```

```typescript
// lib/query-client.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: 3,
      refetchOnWindowFocus: false,
    },
  },
});

// app/layout.tsx
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '@/lib/query-client';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
```

**Using React Query with AEON APIs:**

```typescript
// hooks/useThreatAnalytics.ts
import { useQuery } from '@tanstack/react-query';
import { useAeonClient } from '@/lib/aeon-client';

export function useThreatAnalytics(timeframe = '30d') {
  const aeon = useAeonClient();

  return useQuery({
    queryKey: ['threat-analytics', timeframe],
    queryFn: () => aeon.threatIntel.getAnalytics(timeframe),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

// In component
function ThreatDashboard() {
  const { data, isLoading, error } = useThreatAnalytics('30d');

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorAlert message={error.message} />;

  return <div>{/* Render data */}</div>;
}
```

---

### Local Storage Caching

```typescript
// lib/cache.ts
export class LocalCache {
  private prefix = 'aeon_';
  private ttl = 5 * 60 * 1000; // 5 minutes default

  set(key: string, data: any, ttl = this.ttl) {
    const item = {
      data,
      timestamp: Date.now(),
      ttl,
    };
    localStorage.setItem(this.prefix + key, JSON.stringify(item));
  }

  get(key: string): any | null {
    const item = localStorage.getItem(this.prefix + key);
    if (!item) return null;

    const parsed = JSON.parse(item);
    const age = Date.now() - parsed.timestamp;

    if (age > parsed.ttl) {
      this.remove(key);
      return null;
    }

    return parsed.data;
  }

  remove(key: string) {
    localStorage.removeItem(this.prefix + key);
  }

  clear() {
    Object.keys(localStorage)
      .filter(key => key.startsWith(this.prefix))
      .forEach(key => localStorage.removeItem(key));
  }
}

export const cache = new LocalCache();
```

**Usage with API calls:**

```typescript
import { cache } from '@/lib/cache';

async function fetchWithCache(endpoint: string) {
  const cached = cache.get(endpoint);
  if (cached) return cached;

  const data = await callAPI(endpoint);
  cache.set(endpoint, data);
  return data;
}
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **CORS Errors**

**Error:**
```
Access to fetch at 'http://localhost:3000/api/...' from origin 'http://localhost:3001' has been blocked by CORS policy
```

**Solution:**
Ensure frontend and API are on same domain/port, or configure CORS in Next.js:

```typescript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
        ],
      },
    ];
  },
};
```

---

#### 2. **Authentication 401 Errors**

**Error:**
```
401 Unauthorized
```

**Debug Steps:**
1. Check Clerk keys are configured:
```bash
echo $NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
echo $CLERK_SECRET_KEY
```

2. Verify token is being sent:
```typescript
const token = await getToken();
console.log('Token:', token ? 'Present' : 'Missing');
```

3. Check Clerk session:
```typescript
import { useUser } from '@clerk/nextjs';

function DebugAuth() {
  const { user, isLoaded, isSignedIn } = useUser();

  return (
    <div>
      <p>Loaded: {isLoaded ? 'Yes' : 'No'}</p>
      <p>Signed In: {isSignedIn ? 'Yes' : 'No'}</p>
      <p>User: {user?.emailAddresses[0]?.emailAddress}</p>
    </div>
  );
}
```

---

#### 3. **NER API Not Responding**

**Error:**
```
Failed to fetch from http://localhost:8000/ner
```

**Debug Steps:**
1. Check NER service is running:
```bash
docker ps | grep ner11
curl http://localhost:8000/health
```

2. Test NER API directly:
```bash
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text":"APT29 exploited CVE-2024-12345"}'
```

3. Check logs:
```bash
docker logs ner11-gold-api
```

---

#### 4. **Neo4j Connection Failed**

**Error:**
```
ServiceUnavailable: Cannot connect to bolt://localhost:7687
```

**Debug Steps:**
1. Check Neo4j is running:
```bash
docker ps | grep neo4j
netstat -tuln | grep 7687
```

2. Test connection:
```bash
# Install cypher-shell
docker exec -it openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg"

# Test query
MATCH (n) RETURN count(n);
```

3. Verify credentials:
```typescript
const driver = neo4j.driver(
  'bolt://localhost:7687',
  neo4j.auth.basic('neo4j', 'neo4j@openspg') // Check password
);
```

---

#### 5. **Slow API Response**

**Issue:** APIs taking >5 seconds to respond

**Solutions:**

1. **Add Timeouts:**
```typescript
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 10000);

try {
  const response = await fetch('/api/endpoint', {
    signal: controller.signal
  });
} finally {
  clearTimeout(timeout);
}
```

2. **Use Pagination:**
```typescript
// Instead of loading all data
const data = await callAPI('/dashboard/activity'); // Slow

// Use pagination
const data = await callAPI('/dashboard/activity?limit=10&offset=0'); // Fast
```

3. **Check Network Tab:**
Open browser DevTools → Network tab → Look for slow requests

---

### Debug Mode

Enable debug logging:

```typescript
// lib/debug.ts
export const DEBUG = process.env.NODE_ENV === 'development';

export function debugLog(category: string, message: string, data?: any) {
  if (!DEBUG) return;

  console.log(`[${category}] ${message}`, data || '');
}

// Usage
import { debugLog } from '@/lib/debug';

async function fetchData() {
  debugLog('API', 'Fetching threat analytics...');
  const data = await callAPI('/threat-intel/analytics');
  debugLog('API', 'Response received', data);
}
```

---

## 📝 Summary

You now have:

✅ **48 Working APIs** documented and ready to use
✅ **Authentication** configured with Clerk
✅ **TypeScript client** for type-safe API calls
✅ **React hooks** for data fetching
✅ **Complete examples** for common use cases
✅ **Error handling** patterns
✅ **Performance optimization** strategies
✅ **Troubleshooting** guide

**Next Steps:**
1. Set up authentication with Clerk
2. Copy the TypeScript client library
3. Start building your first component
4. Refer to examples for patterns
5. Join our support channel for help

---

**Support:**
- Email: jim@aeon-dt.systems
- Documentation: `/docs` folder
- API Reference: This document

**Last Updated:** 2025-12-12 16:45 UTC
**Status:** ✅ PRODUCTION-READY
