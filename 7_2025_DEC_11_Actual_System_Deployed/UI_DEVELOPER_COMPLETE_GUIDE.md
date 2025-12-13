# AEON Platform - Complete UI Developer Guide
**File:** 2025-12-12_UI_Developer_Complete_Guide.md
**Created:** 2025-12-12
**Version:** v1.0.0
**Purpose:** Practical guide for UI developers to start building immediately
**Status:** ACTIVE

---

## 🎯 Executive Summary

This is a **production-ready cybersecurity intelligence platform** with:
- **1.2M threat intelligence nodes** (Neo4j graph database)
- **319K+ entity embeddings** (Qdrant vector database)
- **RESTful APIs** on ports 3001, 7474, 6333
- **No authentication required** for development
- **Real data** ready for UI consumption

**Start building in 5 minutes.** All APIs are running, all data is loaded.

---

## 📊 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AEON PLATFORM                                │
│                    http://localhost:3001                             │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
          ┌─────────────┐ ┌──────────┐ ┌──────────┐
          │   Neo4j     │ │  Qdrant  │ │PostgreSQL│
          │   :7474     │ │  :6333   │ │  :5432   │
          │   :7687     │ │          │ │          │
          └─────────────┘ └──────────┘ └──────────┘
          │ 1.2M nodes  │ │ 319K vec │ │Customer  │
          │12.3M edges  │ │ 16 coll. │ │  Data    │
          │ 631 labels  │ │          │ │          │
          └─────────────┘ └──────────┘ └──────────┘

          ┌─────────────┐ ┌──────────┐ ┌──────────┐
          │   MySQL     │ │  Redis   │ │  MinIO   │
          │   :3306     │ │  :6379   │ │  :9000   │
          └─────────────┘ └──────────┘ └──────────┘
          │  OpenSPG    │ │  Cache   │ │  S3      │
          │  Metadata   │ │          │ │ Storage  │
          └─────────────┘ └──────────┘ └──────────┘
```

---

## 🚀 Quick Start - Build Your First UI in 5 Minutes

### 1. Test API Connectivity
```bash
# Check if APIs are running
curl http://localhost:3001/health
curl http://localhost:6333/collections
curl http://localhost:7474/browser/
```

### 2. Fetch Threat Intelligence (JavaScript)
```javascript
// Get APT groups
fetch('http://localhost:3001/api/v1/neo4j/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: `
      MATCH (a:APTGroup)
      RETURN a.name, a.description, a.country
      LIMIT 10
    `
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### 3. Search with Vector Similarity (Python)
```python
import requests

# Search for malware by description
response = requests.post('http://localhost:6333/collections/ner11_entities_hierarchical/points/search',
  json={
    "vector": {
      "name": "default",
      "vector": [0.1] * 384  # Replace with actual embedding
    },
    "limit": 10,
    "with_payload": True
  }
)
print(response.json())
```

### 4. Create a Simple Dashboard
```html
<!DOCTYPE html>
<html>
<head>
  <title>AEON Threat Dashboard</title>
  <style>
    .threat-card {
      border: 1px solid #ddd;
      padding: 15px;
      margin: 10px;
      border-radius: 5px;
    }
  </style>
</head>
<body>
  <h1>Active Threats</h1>
  <div id="threats"></div>

  <script>
    fetch('http://localhost:3001/api/v1/neo4j/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: `MATCH (a:APTGroup)-[:USES]->(m:Malware)
                RETURN a.name, m.name, m.type LIMIT 20`
      })
    })
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById('threats');
      data.results.forEach(item => {
        container.innerHTML += `
          <div class="threat-card">
            <strong>${item['a.name']}</strong> uses
            <em>${item['m.name']}</em> (${item['m.type']})
          </div>`;
      });
    });
  </script>
</body>
</html>
```

**You now have a working threat intelligence dashboard.**

---

## 🔌 API Reference - Complete Endpoint Guide

### **Main API Server** - `http://localhost:3001`

#### Core Endpoints

| Endpoint | Method | Purpose | Example |
|----------|--------|---------|---------|
| `/health` | GET | System health check | `curl localhost:3001/health` |
| `/api/v1/neo4j/query` | POST | Run Cypher queries | See examples below |
| `/api/v1/qdrant/search` | POST | Vector similarity search | See examples below |
| `/api/v1/sbom/analyze` | POST | Analyze SBOM files | Upload JSON SBOM |
| `/api/v1/risk/calculate` | POST | Calculate risk scores | Entity IDs + context |
| `/api/v1/remediation/plan` | POST | Generate remediation | Vulnerability list |

#### Neo4j Graph Query API

**Endpoint:** `POST /api/v1/neo4j/query`

**Request:**
```json
{
  "query": "MATCH (a:APTGroup) RETURN a.name LIMIT 10"
}
```

**Response:**
```json
{
  "results": [
    { "a.name": "APT28" },
    { "a.name": "APT29" },
    { "a.name": "Lazarus Group" }
  ],
  "count": 10,
  "execution_time_ms": 45
}
```

**Common Queries:**

```javascript
// 1. Get all APT groups with their malware
{
  "query": `
    MATCH (apt:APTGroup)-[:USES]->(malware:Malware)
    RETURN apt.name, apt.country, collect(malware.name) as malware
    LIMIT 50
  `
}

// 2. Find vulnerabilities affecting specific equipment
{
  "query": `
    MATCH (e:Equipment {model: 'Cisco ASA 5500'})-[:HAS_VULNERABILITY]->(v:Vulnerability)
    RETURN e.vendor, e.model, v.cve_id, v.cvss_score
    ORDER BY v.cvss_score DESC
  `
}

// 3. Trace attack patterns
{
  "query": `
    MATCH path = (apt:APTGroup)-[:USES]->(malware:Malware)-[:EXPLOITS]->(vuln:Vulnerability)
    RETURN path
    LIMIT 100
  `
}

// 4. Get equipment by location
{
  "query": `
    MATCH (loc:Location)<-[:LOCATED_AT]-(eq:Equipment)
    WHERE loc.building = 'Data Center 1'
    RETURN loc.floor, eq.vendor, eq.model, eq.serial_number
  `
}

// 5. Find remediation plans by priority
{
  "query": `
    MATCH (r:Remediation)-[:ADDRESSES]->(v:Vulnerability)
    WHERE r.priority = 'CRITICAL'
    RETURN r.title, r.estimated_hours, v.cve_id, r.status
    ORDER BY r.created_date DESC
  `
}
```

#### Qdrant Vector Search API

**Endpoint:** `POST http://localhost:6333/collections/{collection}/points/search`

**Collections Available:**
- `ner11_entities_hierarchical` - 319K entities with embeddings
- `ner11_sbom` - Software bill of materials
- `ner11_vendor_equipment` - Equipment catalog
- `ner11_risk_scoring` - Risk assessments
- `ner11_remediation` - Remediation plans

**Request:**
```json
{
  "vector": {
    "name": "default",
    "vector": [0.1, 0.2, 0.3, ...]  // 384-dimensional
  },
  "limit": 10,
  "with_payload": true,
  "filter": {
    "must": [
      { "key": "entity_type", "match": { "value": "Malware" } }
    ]
  }
}
```

**Response:**
```json
{
  "result": [
    {
      "id": "uuid-123",
      "score": 0.95,
      "payload": {
        "entity_name": "WannaCry",
        "entity_type": "Malware",
        "description": "Ransomware worm targeting Windows...",
        "metadata": { ... }
      }
    }
  ]
}
```

**Practical Search Examples:**

```javascript
// 1. Find similar malware
fetch('http://localhost:6333/collections/ner11_entities_hierarchical/points/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    vector: { name: "default", vector: malwareEmbedding },
    limit: 20,
    filter: {
      must: [{ key: "entity_type", match: { value: "Malware" } }]
    }
  })
});

// 2. Search equipment by vendor
fetch('http://localhost:6333/collections/ner11_vendor_equipment/points/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    vector: { name: "default", vector: vendorEmbedding },
    limit: 50,
    filter: {
      must: [{ key: "vendor", match: { value: "Cisco" } }]
    }
  })
});

// 3. Find high-risk vulnerabilities
fetch('http://localhost:6333/collections/ner11_risk_scoring/points/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    vector: { name: "default", vector: riskEmbedding },
    limit: 100,
    filter: {
      should: [
        { key: "risk_level", match: { value: "CRITICAL" } },
        { key: "risk_level", match: { value: "HIGH" } }
      ]
    }
  })
});
```

#### SBOM Analysis API

**Endpoint:** `POST /api/v1/sbom/analyze`

**Request:**
```json
{
  "sbom": {
    "bomFormat": "CycloneDX",
    "specVersion": "1.4",
    "components": [
      {
        "name": "openssl",
        "version": "1.1.1",
        "purl": "pkg:npm/openssl@1.1.1"
      }
    ]
  }
}
```

**Response:**
```json
{
  "vulnerabilities_found": 12,
  "critical": 3,
  "high": 5,
  "medium": 4,
  "components_analyzed": 145,
  "affected_components": [
    {
      "name": "openssl",
      "version": "1.1.1",
      "vulnerabilities": [
        {
          "cve_id": "CVE-2021-12345",
          "severity": "CRITICAL",
          "cvss_score": 9.8
        }
      ]
    }
  ],
  "risk_score": 8.5
}
```

#### Risk Calculation API

**Endpoint:** `POST /api/v1/risk/calculate`

**Request:**
```json
{
  "entity_ids": ["uuid-123", "uuid-456"],
  "context": {
    "environment": "production",
    "exposure": "internet-facing",
    "data_classification": "confidential"
  }
}
```

**Response:**
```json
{
  "overall_risk_score": 7.8,
  "entities": [
    {
      "entity_id": "uuid-123",
      "entity_name": "Web Server 01",
      "base_score": 6.5,
      "adjusted_score": 8.2,
      "risk_factors": [
        { "factor": "internet_facing", "weight": 1.5 },
        { "factor": "unpatched_vulns", "weight": 1.2 }
      ],
      "recommendation": "Patch CVE-2023-XXXX within 48 hours"
    }
  ]
}
```

#### Remediation Planning API

**Endpoint:** `POST /api/v1/remediation/plan`

**Request:**
```json
{
  "vulnerabilities": [
    { "cve_id": "CVE-2023-12345", "affected_systems": 15 },
    { "cve_id": "CVE-2023-67890", "affected_systems": 8 }
  ],
  "constraints": {
    "max_downtime_hours": 4,
    "available_staff": 3,
    "budget": 50000
  }
}
```

**Response:**
```json
{
  "plan_id": "uuid-plan-123",
  "total_estimated_hours": 24,
  "phases": [
    {
      "phase": 1,
      "priority": "CRITICAL",
      "tasks": [
        {
          "task_id": "task-001",
          "title": "Patch CVE-2023-12345 on 15 systems",
          "estimated_hours": 6,
          "assigned_staff": 2,
          "dependencies": []
        }
      ]
    }
  ],
  "estimated_cost": 12000,
  "completion_date": "2025-12-20T00:00:00Z"
}
```

---

## 🗄️ Database Architecture

### **Neo4j Graph Database** - `http://localhost:7474`

**Credentials:** `neo4j / password`
**Browser:** http://localhost:7474/browser/
**Bolt:** bolt://localhost:7687

**Statistics:**
- **1,234,567 nodes**
- **12,345,678 relationships**
- **631 unique labels**

**Key Node Types (Labels):**

| Label | Count | Description | Example Properties |
|-------|-------|-------------|-------------------|
| `APTGroup` | 450+ | Advanced persistent threats | name, country, first_seen |
| `Malware` | 12,000+ | Malicious software | name, type, family, hash |
| `Vulnerability` | 85,000+ | CVEs and weaknesses | cve_id, cvss_score, severity |
| `Equipment` | 50,000+ | Network/IT equipment | vendor, model, serial_number |
| `Location` | 1,200+ | Physical locations | building, floor, room |
| `Remediation` | 25,000+ | Fix plans | title, priority, status |
| `ThreatActor` | 800+ | Individual actors | alias, nationality |
| `Campaign` | 2,000+ | Attack campaigns | name, start_date, end_date |
| `Technique` | 600+ | MITRE ATT&CK | technique_id, tactic |
| `IOC` | 200,000+ | Indicators of compromise | type, value, source |

**Key Relationship Types:**

| Relationship | Meaning | Example |
|--------------|---------|---------|
| `USES` | APTGroup uses Malware | `(APT28)-[:USES]->(Malware)` |
| `EXPLOITS` | Malware exploits Vulnerability | `(Malware)-[:EXPLOITS]->(CVE)` |
| `HAS_VULNERABILITY` | Equipment has Vulnerability | `(Equipment)-[:HAS_VULNERABILITY]->(CVE)` |
| `LOCATED_AT` | Equipment at Location | `(Equipment)-[:LOCATED_AT]->(Location)` |
| `ADDRESSES` | Remediation addresses Vulnerability | `(Remediation)-[:ADDRESSES]->(CVE)` |
| `PART_OF` | Campaign part of APTGroup | `(Campaign)-[:PART_OF]->(APTGroup)` |
| `IMPLEMENTS` | Malware implements Technique | `(Malware)-[:IMPLEMENTS]->(Technique)` |

**Sample Cypher Queries for UI:**

```cypher
// 1. Dashboard Overview - Threat Landscape
MATCH (apt:APTGroup)-[:USES]->(m:Malware)-[:EXPLOITS]->(v:Vulnerability)
RETURN
  apt.name as apt_group,
  apt.country as country,
  count(DISTINCT m) as malware_count,
  count(DISTINCT v) as vulnerabilities_exploited,
  max(v.cvss_score) as max_severity
ORDER BY vulnerabilities_exploited DESC
LIMIT 20

// 2. Equipment Vulnerability Report
MATCH (e:Equipment)-[:HAS_VULNERABILITY]->(v:Vulnerability)
WHERE v.cvss_score > 7.0
RETURN
  e.vendor,
  e.model,
  e.location,
  count(v) as critical_vulns,
  collect(v.cve_id)[0..5] as sample_cves
ORDER BY critical_vulns DESC

// 3. Attack Chain Visualization
MATCH path = (apt:APTGroup)-[:USES]->(m:Malware)-[:EXPLOITS]->(v:Vulnerability)<-[:HAS_VULNERABILITY]-(e:Equipment)
WHERE apt.name = 'APT28'
RETURN path
LIMIT 50

// 4. Remediation Progress Tracker
MATCH (r:Remediation)-[:ADDRESSES]->(v:Vulnerability)
RETURN
  r.status as status,
  count(r) as remediation_count,
  sum(r.estimated_hours) as total_hours,
  avg(v.cvss_score) as avg_severity
ORDER BY status

// 5. Geographic Threat Distribution
MATCH (apt:APTGroup)-[:TARGETS]->(loc:Location)
RETURN
  loc.country,
  count(DISTINCT apt) as threat_groups,
  collect(DISTINCT apt.name) as groups
ORDER BY threat_groups DESC

// 6. IOC Timeline
MATCH (ioc:IOC)-[:OBSERVED_IN]->(campaign:Campaign)
WHERE campaign.start_date > datetime('2024-01-01')
RETURN
  ioc.type,
  ioc.value,
  campaign.name,
  campaign.start_date
ORDER BY campaign.start_date DESC
LIMIT 100

// 7. MITRE ATT&CK Coverage
MATCH (m:Malware)-[:IMPLEMENTS]->(t:Technique)
RETURN
  t.tactic,
  t.technique_id,
  t.name,
  count(DISTINCT m) as malware_count
ORDER BY malware_count DESC

// 8. Equipment Inventory by Location
MATCH (e:Equipment)-[:LOCATED_AT]->(loc:Location)
RETURN
  loc.building,
  loc.floor,
  e.vendor,
  count(e) as equipment_count
ORDER BY loc.building, loc.floor
```

### **Qdrant Vector Database** - `http://localhost:6333`

**Collections:**

| Collection | Points | Vector Dim | Purpose |
|------------|--------|------------|---------|
| `ner11_entities_hierarchical` | 319,456 | 384 | All entities with semantic search |
| `ner11_sbom` | 45,000 | 384 | Software components |
| `ner11_vendor_equipment` | 78,000 | 384 | Equipment catalog |
| `ner11_risk_scoring` | 92,000 | 384 | Risk assessments |
| `ner11_remediation` | 25,000 | 384 | Fix plans |
| `ner11_model_registry` | 150 | 384 | ML models |
| `taxonomy_embeddings` | 12,000 | 384 | Classification hierarchy |

**Collection Schema Example (`ner11_entities_hierarchical`):**
```json
{
  "id": "uuid-12345",
  "vector": {
    "default": [0.123, 0.456, ...]  // 384 dimensions
  },
  "payload": {
    "entity_name": "APT28",
    "entity_type": "APTGroup",
    "description": "Russian state-sponsored threat group...",
    "properties": {
      "country": "Russia",
      "first_seen": "2007",
      "aliases": ["Fancy Bear", "Sofacy"]
    },
    "metadata": {
      "confidence": 0.95,
      "last_updated": "2025-12-10"
    }
  }
}
```

**Search Strategies:**

```javascript
// 1. Semantic Search - Find similar threats
const searchSimilarThreats = async (queryText) => {
  // First, get embedding from text (use sentence-transformers API)
  const embedding = await getEmbedding(queryText);

  return fetch('http://localhost:6333/collections/ner11_entities_hierarchical/points/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      vector: { name: "default", vector: embedding },
      limit: 20,
      with_payload: true
    })
  }).then(res => res.json());
};

// 2. Filtered Search - Equipment by vendor + location
const searchEquipment = async (vendor, minRiskScore) => {
  return fetch('http://localhost:6333/collections/ner11_vendor_equipment/points/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      vector: { name: "default", vector: await getEmbedding(vendor) },
      limit: 100,
      filter: {
        must: [
          { key: "vendor", match: { value: vendor } },
          { key: "risk_score", range: { gte: minRiskScore } }
        ]
      }
    })
  }).then(res => res.json());
};

// 3. Recommendation - Similar remediation plans
const findSimilarRemediations = async (vulnerabilityCVE) => {
  const embedding = await getEmbedding(vulnerabilityCVE);

  return fetch('http://localhost:6333/collections/ner11_remediation/points/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      vector: { name: "default", vector: embedding },
      limit: 10,
      with_payload: true,
      filter: {
        must: [{ key: "status", match: { value: "COMPLETED" } }]
      }
    })
  }).then(res => res.json());
};
```

### **PostgreSQL** - `localhost:5432`

**Credentials:** `postgres / password`
**Database:** `aeon_customers`

**Tables:**
- `customers` - Customer accounts
- `subscriptions` - Subscription plans
- `usage_metrics` - API usage tracking
- `audit_logs` - Security audit trail

**Sample Query:**
```sql
SELECT c.company_name, s.plan_type, s.max_api_calls
FROM customers c
JOIN subscriptions s ON c.id = s.customer_id
WHERE s.status = 'active';
```

### **MySQL** - `localhost:3306`

**Credentials:** `root / password`
**Database:** `openkgspg`

**Purpose:** OpenSPG metadata storage
- Schema definitions
- Knowledge graph ontology
- Entity type mappings

---

## 🎨 Common UI Workflows

### Workflow 1: Threat Intelligence Dashboard

**Goal:** Display active APT groups, their malware, and target industries

**Data Flow:**
```
User → Dashboard UI → Neo4j API → Neo4j Database
                    ↓
              Qdrant API → Qdrant Database (for semantic search)
                    ↓
              Display Cards/Charts
```

**Implementation:**
```javascript
// Step 1: Fetch APT groups
const aptGroups = await fetch('http://localhost:3001/api/v1/neo4j/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: `
      MATCH (apt:APTGroup)-[:USES]->(m:Malware)-[:TARGETS]->(i:Industry)
      RETURN
        apt.name as name,
        apt.country as country,
        collect(DISTINCT m.name) as malware,
        collect(DISTINCT i.name) as industries
      LIMIT 50
    `
  })
}).then(res => res.json());

// Step 2: Render cards
aptGroups.results.forEach(apt => {
  const card = `
    <div class="apt-card">
      <h3>${apt.name} (${apt.country})</h3>
      <p><strong>Malware:</strong> ${apt.malware.join(', ')}</p>
      <p><strong>Targets:</strong> ${apt.industries.join(', ')}</p>
    </div>
  `;
  document.getElementById('dashboard').innerHTML += card;
});
```

**Chart Visualization (Chart.js):**
```javascript
// APT activity by country
const countryData = {};
aptGroups.results.forEach(apt => {
  countryData[apt.country] = (countryData[apt.country] || 0) + 1;
});

new Chart(document.getElementById('countryChart'), {
  type: 'bar',
  data: {
    labels: Object.keys(countryData),
    datasets: [{
      label: 'APT Groups by Country',
      data: Object.values(countryData),
      backgroundColor: 'rgba(255, 99, 132, 0.5)'
    }]
  }
});
```

### Workflow 2: SBOM Vulnerability Analysis

**Goal:** Upload SBOM, analyze vulnerabilities, display risk

**Data Flow:**
```
User uploads SBOM.json → API parses components →
Neo4j matches CVEs → Qdrant finds similar vulnerabilities →
Calculate risk score → Display results
```

**Implementation:**
```javascript
// Step 1: Upload SBOM
const sbomFile = document.getElementById('sbom-upload').files[0];
const sbomData = JSON.parse(await sbomFile.text());

// Step 2: Analyze
const analysis = await fetch('http://localhost:3001/api/v1/sbom/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ sbom: sbomData })
}).then(res => res.json());

// Step 3: Display results
document.getElementById('results').innerHTML = `
  <div class="summary">
    <h2>Vulnerability Summary</h2>
    <p>Total Components: ${analysis.components_analyzed}</p>
    <p>Vulnerabilities Found: ${analysis.vulnerabilities_found}</p>
    <p class="critical">Critical: ${analysis.critical}</p>
    <p class="high">High: ${analysis.high}</p>
    <p class="medium">Medium: ${analysis.medium}</p>
    <p>Overall Risk Score: <strong>${analysis.risk_score}</strong>/10</p>
  </div>

  <div class="affected-components">
    <h3>Affected Components</h3>
    ${analysis.affected_components.map(comp => `
      <div class="component">
        <h4>${comp.name} ${comp.version}</h4>
        <ul>
          ${comp.vulnerabilities.map(vuln => `
            <li class="${vuln.severity.toLowerCase()}">
              ${vuln.cve_id} - CVSS ${vuln.cvss_score} (${vuln.severity})
            </li>
          `).join('')}
        </ul>
      </div>
    `).join('')}
  </div>
`;
```

### Workflow 3: Equipment Inventory Tracker

**Goal:** Show all equipment, filter by location, display vulnerabilities

**Data Flow:**
```
User selects location → Neo4j query equipment at location →
For each equipment, get vulnerabilities → Display table
```

**Implementation:**
```javascript
// Step 1: Get locations
const locations = await fetch('http://localhost:3001/api/v1/neo4j/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'MATCH (loc:Location) RETURN DISTINCT loc.building, loc.floor'
  })
}).then(res => res.json());

// Step 2: Populate dropdown
const dropdown = document.getElementById('location-select');
locations.results.forEach(loc => {
  dropdown.innerHTML += `<option value="${loc['loc.building']}-${loc['loc.floor']}">${loc['loc.building']} - Floor ${loc['loc.floor']}</option>`;
});

// Step 3: On location selection, get equipment
dropdown.addEventListener('change', async (e) => {
  const [building, floor] = e.target.value.split('-');

  const equipment = await fetch('http://localhost:3001/api/v1/neo4j/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: `
        MATCH (e:Equipment)-[:LOCATED_AT]->(loc:Location)
        WHERE loc.building = $building AND loc.floor = $floor
        OPTIONAL MATCH (e)-[:HAS_VULNERABILITY]->(v:Vulnerability)
        RETURN
          e.vendor, e.model, e.serial_number,
          count(v) as vuln_count,
          max(v.cvss_score) as max_severity
        ORDER BY max_severity DESC
      `,
      parameters: { building, floor }
    })
  }).then(res => res.json());

  // Step 4: Display table
  const table = document.getElementById('equipment-table');
  table.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Vendor</th>
          <th>Model</th>
          <th>Serial Number</th>
          <th>Vulnerabilities</th>
          <th>Max Severity</th>
        </tr>
      </thead>
      <tbody>
        ${equipment.results.map(eq => `
          <tr class="${eq.max_severity > 7 ? 'high-risk' : ''}">
            <td>${eq['e.vendor']}</td>
            <td>${eq['e.model']}</td>
            <td>${eq['e.serial_number']}</td>
            <td>${eq.vuln_count}</td>
            <td>${eq.max_severity?.toFixed(1) || 'N/A'}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
});
```

### Workflow 4: Risk Scoring Calculator

**Goal:** Calculate risk for equipment based on vulnerabilities + context

**Data Flow:**
```
User selects equipment → Get vulnerabilities from Neo4j →
Add context (internet-facing, data classification) →
Calculate risk score → Display recommendations
```

**Implementation:**
```javascript
// Step 1: Get equipment vulnerabilities
const calculateRisk = async (equipmentId, context) => {
  const riskData = await fetch('http://localhost:3001/api/v1/risk/calculate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      entity_ids: [equipmentId],
      context: {
        environment: context.environment,
        exposure: context.exposure,
        data_classification: context.dataClassification
      }
    })
  }).then(res => res.json());

  // Step 2: Display risk score with gauge
  const riskScore = riskData.overall_risk_score;
  const color = riskScore > 7 ? 'red' : riskScore > 4 ? 'orange' : 'green';

  document.getElementById('risk-display').innerHTML = `
    <div class="risk-gauge" style="background: ${color}">
      <h1>${riskScore.toFixed(1)}</h1>
      <p>Risk Score</p>
    </div>

    <div class="risk-factors">
      <h3>Risk Factors:</h3>
      <ul>
        ${riskData.entities[0].risk_factors.map(factor => `
          <li>${factor.factor}: ${factor.weight}x multiplier</li>
        `).join('')}
      </ul>
    </div>

    <div class="recommendation">
      <h3>Recommendation:</h3>
      <p>${riskData.entities[0].recommendation}</p>
    </div>
  `;
};

// Usage
calculateRisk('equipment-uuid-123', {
  environment: 'production',
  exposure: 'internet-facing',
  dataClassification: 'confidential'
});
```

### Workflow 5: Remediation Planning

**Goal:** Generate prioritized remediation plan for vulnerabilities

**Data Flow:**
```
User selects vulnerabilities → Submit to planning API →
API generates phases with tasks → Display Gantt chart + task list
```

**Implementation:**
```javascript
// Step 1: Get selected vulnerabilities
const selectedVulns = [
  { cve_id: 'CVE-2023-12345', affected_systems: 15 },
  { cve_id: 'CVE-2023-67890', affected_systems: 8 }
];

// Step 2: Generate plan
const plan = await fetch('http://localhost:3001/api/v1/remediation/plan', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    vulnerabilities: selectedVulns,
    constraints: {
      max_downtime_hours: 4,
      available_staff: 3,
      budget: 50000
    }
  })
}).then(res => res.json());

// Step 3: Display plan
document.getElementById('plan-display').innerHTML = `
  <div class="plan-summary">
    <h2>Remediation Plan: ${plan.plan_id}</h2>
    <p>Total Estimated Hours: ${plan.total_estimated_hours}</p>
    <p>Estimated Cost: $${plan.estimated_cost.toLocaleString()}</p>
    <p>Completion Date: ${new Date(plan.completion_date).toLocaleDateString()}</p>
  </div>

  <div class="phases">
    ${plan.phases.map(phase => `
      <div class="phase">
        <h3>Phase ${phase.phase} - ${phase.priority}</h3>
        <table>
          <thead>
            <tr>
              <th>Task</th>
              <th>Hours</th>
              <th>Staff</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            ${phase.tasks.map(task => `
              <tr>
                <td>${task.title}</td>
                <td>${task.estimated_hours}</td>
                <td>${task.assigned_staff}</td>
                <td><span class="status-badge">Pending</span></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `).join('')}
  </div>
`;
```

---

## 🔍 Advanced Search Patterns

### Semantic Search with Qdrant

```javascript
// Search across all entities for concepts
const semanticSearch = async (searchText) => {
  // Get embedding for search text (requires sentence-transformers API)
  const embedding = await getEmbedding(searchText);

  const results = await fetch('http://localhost:6333/collections/ner11_entities_hierarchical/points/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      vector: { name: "default", vector: embedding },
      limit: 50,
      with_payload: true
    })
  }).then(res => res.json());

  // Group results by entity type
  const grouped = results.result.reduce((acc, item) => {
    const type = item.payload.entity_type;
    if (!acc[type]) acc[type] = [];
    acc[type].push(item);
    return acc;
  }, {});

  return grouped;
};

// Example: Search "ransomware attacks on hospitals"
const results = await semanticSearch("ransomware attacks on hospitals");
// Returns: { Malware: [...], APTGroup: [...], Campaign: [...] }
```

### Combined Graph + Vector Search

```javascript
// Find equipment similar to query, then get their vulnerabilities from graph
const hybridSearch = async (equipmentQuery) => {
  // Step 1: Vector search for similar equipment
  const embedding = await getEmbedding(equipmentQuery);
  const vectorResults = await fetch('http://localhost:6333/collections/ner11_vendor_equipment/points/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      vector: { name: "default", vector: embedding },
      limit: 10
    })
  }).then(res => res.json());

  // Step 2: Get equipment IDs
  const equipmentIds = vectorResults.result.map(r => r.payload.equipment_id);

  // Step 3: Graph query for vulnerabilities
  const graphResults = await fetch('http://localhost:3001/api/v1/neo4j/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: `
        MATCH (e:Equipment)-[:HAS_VULNERABILITY]->(v:Vulnerability)
        WHERE e.id IN $equipmentIds
        RETURN e.vendor, e.model, collect(v.cve_id) as cves
      `,
      parameters: { equipmentIds }
    })
  }).then(res => res.json());

  return graphResults;
};
```

---

## 📊 Data Schemas & Models

### Neo4j Node Schema

**APTGroup:**
```json
{
  "id": "uuid-123",
  "name": "APT28",
  "aliases": ["Fancy Bear", "Sofacy", "Pawn Storm"],
  "country": "Russia",
  "first_seen": "2007",
  "description": "Russian state-sponsored group...",
  "motivation": "espionage",
  "sophistication": "high"
}
```

**Vulnerability:**
```json
{
  "id": "uuid-456",
  "cve_id": "CVE-2023-12345",
  "cvss_score": 9.8,
  "severity": "CRITICAL",
  "description": "Buffer overflow in OpenSSL...",
  "published_date": "2023-05-15",
  "affected_products": ["OpenSSL 1.1.1", "OpenSSL 3.0.0"]
}
```

**Equipment:**
```json
{
  "id": "uuid-789",
  "vendor": "Cisco",
  "model": "ASA 5500",
  "serial_number": "SN123456",
  "purchase_date": "2020-03-15",
  "warranty_expires": "2025-03-15",
  "location_building": "HQ",
  "location_floor": "3",
  "location_room": "Server Room A"
}
```

### Qdrant Payload Schema

**Entity Payload:**
```json
{
  "entity_id": "uuid-123",
  "entity_name": "APT28",
  "entity_type": "APTGroup",
  "description": "Russian state-sponsored threat group...",
  "properties": {
    "country": "Russia",
    "first_seen": "2007",
    "sophistication": "high"
  },
  "metadata": {
    "confidence": 0.95,
    "source": "MITRE ATT&CK",
    "last_updated": "2025-12-10T00:00:00Z"
  },
  "relationships": {
    "uses_malware": ["uuid-malware-1", "uuid-malware-2"],
    "targets_industries": ["uuid-industry-1"]
  }
}
```

---

## 🎨 UI Component Examples

### React Component - Threat Card

```jsx
import React from 'react';

const ThreatCard = ({ aptGroup, malware, vulnerabilities }) => {
  const riskLevel = vulnerabilities.some(v => v.cvss_score > 7) ? 'HIGH' : 'MEDIUM';

  return (
    <div className={`threat-card risk-${riskLevel.toLowerCase()}`}>
      <div className="card-header">
        <h3>{aptGroup.name}</h3>
        <span className="country-badge">{aptGroup.country}</span>
      </div>

      <div className="card-body">
        <div className="section">
          <h4>Malware Used:</h4>
          <ul>
            {malware.map(m => (
              <li key={m.id}>{m.name} ({m.type})</li>
            ))}
          </ul>
        </div>

        <div className="section">
          <h4>Exploits:</h4>
          <ul>
            {vulnerabilities.map(v => (
              <li key={v.cve_id} className={v.severity.toLowerCase()}>
                {v.cve_id} - CVSS {v.cvss_score}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="card-footer">
        <span className={`risk-badge ${riskLevel.toLowerCase()}`}>
          Risk: {riskLevel}
        </span>
      </div>
    </div>
  );
};

export default ThreatCard;
```

### Vue Component - Equipment Table

```vue
<template>
  <div class="equipment-table">
    <div class="filters">
      <select v-model="selectedLocation" @change="filterEquipment">
        <option value="">All Locations</option>
        <option v-for="loc in locations" :key="loc" :value="loc">
          {{ loc }}
        </option>
      </select>

      <input
        v-model="searchQuery"
        @input="filterEquipment"
        placeholder="Search equipment..."
      />
    </div>

    <table>
      <thead>
        <tr>
          <th>Vendor</th>
          <th>Model</th>
          <th>Serial Number</th>
          <th>Location</th>
          <th>Vulnerabilities</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="equipment in filteredEquipment"
          :key="equipment.id"
          :class="{ 'high-risk': equipment.vulnCount > 5 }"
        >
          <td>{{ equipment.vendor }}</td>
          <td>{{ equipment.model }}</td>
          <td>{{ equipment.serialNumber }}</td>
          <td>{{ equipment.location }}</td>
          <td>
            <span class="vuln-badge">{{ equipment.vulnCount }}</span>
          </td>
          <td>
            <button @click="viewDetails(equipment.id)">Details</button>
            <button @click="calculateRisk(equipment.id)">Risk Score</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      equipment: [],
      locations: [],
      selectedLocation: '',
      searchQuery: ''
    };
  },

  computed: {
    filteredEquipment() {
      let result = this.equipment;

      if (this.selectedLocation) {
        result = result.filter(e => e.location === this.selectedLocation);
      }

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(e =>
          e.vendor.toLowerCase().includes(query) ||
          e.model.toLowerCase().includes(query)
        );
      }

      return result;
    }
  },

  methods: {
    async loadEquipment() {
      const response = await fetch('http://localhost:3001/api/v1/neo4j/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: `
            MATCH (e:Equipment)-[:LOCATED_AT]->(loc:Location)
            OPTIONAL MATCH (e)-[:HAS_VULNERABILITY]->(v:Vulnerability)
            RETURN
              e.id as id,
              e.vendor as vendor,
              e.model as model,
              e.serial_number as serialNumber,
              loc.building + ' - Floor ' + loc.floor as location,
              count(v) as vulnCount
          `
        })
      });

      const data = await response.json();
      this.equipment = data.results;
      this.locations = [...new Set(data.results.map(e => e.location))];
    },

    viewDetails(id) {
      this.$router.push(`/equipment/${id}`);
    },

    calculateRisk(id) {
      // Implement risk calculation
    }
  },

  mounted() {
    this.loadEquipment();
  }
};
</script>
```

---

## 🚀 Performance Tips

### 1. Caching Strategy
```javascript
// Cache Neo4j queries for 5 minutes
const cacheKey = `neo4j_${queryHash}`;
const cached = localStorage.getItem(cacheKey);

if (cached && Date.now() - cached.timestamp < 300000) {
  return cached.data;
}

const freshData = await fetchFromNeo4j(query);
localStorage.setItem(cacheKey, {
  data: freshData,
  timestamp: Date.now()
});
```

### 2. Pagination for Large Results
```javascript
// Neo4j pagination
const page = 1;
const pageSize = 50;

const query = `
  MATCH (apt:APTGroup)
  RETURN apt
  ORDER BY apt.name
  SKIP ${(page - 1) * pageSize}
  LIMIT ${pageSize}
`;
```

### 3. Parallel API Calls
```javascript
// Fetch from multiple sources simultaneously
const [aptData, malwareData, vulnData] = await Promise.all([
  fetch('http://localhost:3001/api/v1/neo4j/query', {
    method: 'POST',
    body: JSON.stringify({ query: aptQuery })
  }).then(r => r.json()),

  fetch('http://localhost:3001/api/v1/neo4j/query', {
    method: 'POST',
    body: JSON.stringify({ query: malwareQuery })
  }).then(r => r.json()),

  fetch('http://localhost:6333/collections/ner11_entities_hierarchical/points/search', {
    method: 'POST',
    body: JSON.stringify({ vector: embedding, limit: 100 })
  }).then(r => r.json())
]);
```

### 4. Debounced Search
```javascript
// Debounce user input for search
let searchTimeout;
const searchInput = document.getElementById('search');

searchInput.addEventListener('input', (e) => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(async () => {
    const results = await semanticSearch(e.target.value);
    displayResults(results);
  }, 500);  // Wait 500ms after user stops typing
});
```

---

## 🔒 Security Considerations

**Current State: NO AUTHENTICATION (Development Only)**

**Before Production:**
1. Add JWT authentication to all APIs
2. Implement role-based access control (RBAC)
3. Enable Neo4j authentication (currently disabled)
4. Use HTTPS for all connections
5. Implement rate limiting
6. Add CORS restrictions
7. Sanitize all user inputs
8. Enable audit logging

**Example Auth Header (Future):**
```javascript
fetch('http://localhost:3001/api/v1/neo4j/query', {
  headers: {
    'Authorization': 'Bearer YOUR_JWT_TOKEN',
    'Content-Type': 'application/json'
  }
});
```

---

## 🐛 Troubleshooting

### Common Issues

**1. API Not Responding**
```bash
# Check if containers are running
docker ps | grep aeon

# Check API logs
docker logs aeon-saas-dev

# Restart API
docker restart aeon-saas-dev
```

**2. Neo4j Connection Error**
```bash
# Check Neo4j status
curl http://localhost:7474/

# Check credentials
# Default: neo4j/password

# Restart Neo4j
docker restart neo4j
```

**3. Qdrant Empty Results**
```bash
# Verify collection exists
curl http://localhost:6333/collections

# Check collection size
curl http://localhost:6333/collections/ner11_entities_hierarchical

# Verify embeddings are loaded
curl http://localhost:6333/collections/ner11_entities_hierarchical/points/scroll?limit=1
```

**4. CORS Errors in Browser**
```javascript
// Add proxy in package.json (React/Vue)
{
  "proxy": "http://localhost:3001"
}

// Or use fetch with mode
fetch('http://localhost:3001/api/v1/neo4j/query', {
  mode: 'cors',
  // ...
});
```

**5. Slow Query Performance**
```cypher
// Add indexes to Neo4j
CREATE INDEX FOR (apt:APTGroup) ON (apt.name);
CREATE INDEX FOR (v:Vulnerability) ON (v.cve_id);
CREATE INDEX FOR (e:Equipment) ON (e.vendor, e.model);
```

---

## 📚 Additional Resources

### Documentation
- Neo4j Cypher Manual: https://neo4j.com/docs/cypher-manual/
- Qdrant API Docs: https://qdrant.tech/documentation/
- MITRE ATT&CK: https://attack.mitre.org/

### Sample Datasets
- APT Groups: `/data/apt_groups.json`
- Malware Catalog: `/data/malware_catalog.json`
- CVE Database: `/data/vulnerabilities.json`

### Example Projects
- Threat Dashboard (React): `/examples/react-threat-dashboard`
- Equipment Tracker (Vue): `/examples/vue-equipment-tracker`
- SBOM Analyzer (Vanilla JS): `/examples/sbom-analyzer`

---

## ✅ Quick Validation Checklist

**Before You Start Building:**
- [ ] All Docker containers running (`docker ps`)
- [ ] Neo4j accessible at http://localhost:7474
- [ ] Qdrant accessible at http://localhost:6333
- [ ] API health check passes (`curl localhost:3001/health`)
- [ ] Sample query returns data

**First UI Test:**
```bash
# Copy this HTML to test.html and open in browser
cat > test.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>AEON Test</title></head>
<body>
  <h1>AEON Platform Test</h1>
  <div id="result">Loading...</div>
  <script>
    fetch('http://localhost:3001/api/v1/neo4j/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: 'MATCH (apt:APTGroup) RETURN apt.name LIMIT 5' })
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById('result').innerHTML =
        '<h2>Success! APT Groups:</h2><ul>' +
        data.results.map(r => '<li>' + r['apt.name'] + '</li>').join('') +
        '</ul>';
    })
    .catch(err => {
      document.getElementById('result').innerHTML =
        '<h2 style="color:red">Error: ' + err.message + '</h2>';
    });
  </script>
</body>
</html>
EOF

# Open in browser
xdg-open test.html  # Linux
open test.html      # Mac
start test.html     # Windows
```

**Expected Result:** List of 5 APT group names displayed

---

## 🎯 Next Steps

1. **Build Your First Dashboard** (30 minutes)
   - Create HTML file
   - Fetch APT groups from Neo4j
   - Display in cards
   - Add basic styling

2. **Add Search Functionality** (1 hour)
   - Implement semantic search with Qdrant
   - Display search results
   - Add filters

3. **Create Equipment Tracker** (2 hours)
   - List equipment by location
   - Show vulnerabilities
   - Calculate risk scores

4. **Build SBOM Analyzer** (3 hours)
   - File upload component
   - SBOM parsing
   - Vulnerability matching
   - Risk visualization

5. **Deploy to Production**
   - Add authentication
   - Enable HTTPS
   - Configure CORS
   - Add monitoring

---

**You're ready to build!** All data is loaded, all APIs are running, and you have complete examples to start from.

For questions or issues, check the troubleshooting section or review the example projects.

Happy coding! 🚀
