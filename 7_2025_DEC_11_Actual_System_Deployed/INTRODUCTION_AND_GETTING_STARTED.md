# AEON CYBERSECURITY KNOWLEDGE GRAPH - Complete Introduction & Developer Guide

**Version**: 3.3.0
**Last Updated**: 2025-12-12
**Status**: Production Development System

---

## 📖 TABLE OF CONTENTS

1. [What is AEON?](#what-is-aeon)
2. [System Overview](#system-overview)
3. [Infrastructure Components](#infrastructure-components)
4. [Data & Capabilities](#data--capabilities)
5. [How to Access Everything](#how-to-access-everything)
6. [Getting Started (5 Minutes)](#getting-started-5-minutes)
7. [Developer Workflows](#developer-workflows)
8. [Architecture Deep Dive](#architecture-deep-dive)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

---

## 🎯 WHAT IS AEON?

**AEON** (Advanced Entity Ontology Network) is a **cybersecurity knowledge graph platform** that combines:
- **Named Entity Recognition** (NER Gold v3.1 model - 60 entity types, 566 fine-grained classifications)
- **Graph Database** (Neo4j with 1.2M nodes, 12.3M relationships, 631 labels)
- **Vector Search** (Qdrant with 319K+ entities, 16 collections, 384-dimensional embeddings)
- **Multi-hop Reasoning** (20-hop graph traversal capabilities)
- **Threat Intelligence** (10,599 threat actors, 316,552 CVEs, 11,601 IOCs)
- **Risk Analysis** (Multi-factor risk scoring across 16 critical infrastructure sectors)

**Purpose**: Enable cybersecurity teams to:
- Analyze threats with AI-powered entity extraction
- Track vulnerabilities across software supply chains (140K SBOM components)
- Assess risk for critical infrastructure (48,288 equipment instances)
- Predict threats using psychometric and behavioral analysis
- Query 20-hop relationship chains for attack path modeling

---

## 🏗️ SYSTEM OVERVIEW

### **The Big Picture**

AEON is built on a **6-level architecture**:

```
Level 1: Equipment Taxonomy
    └─ Categories, types, classifications (16 critical infrastructure sectors)

Level 2: Equipment Instances
    └─ Physical/virtual assets (48,288 devices tracked)

Level 3: Software & SBOM
    └─ Components, dependencies, licenses (140,000+ components)

Level 4: Organizational Context & Threat Intelligence
    └─ Threats, vulnerabilities, campaigns (316K CVEs, 10K actors)

Level 5: Psychometric & Behavioral Analysis
    └─ Personality traits, cognitive biases, insider risk

Level 6: Predictive Analytics
    └─ Crisis prediction, population forecasting, threat evolution
```

**Current Status**:
- Levels 1-4: **60-85% operational** ✅
- Level 5: **15% operational** ⏳ (infrastructure only)
- Level 6: **5% operational** ⏳ (conceptual)

---

## 🐳 INFRASTRUCTURE COMPONENTS

### **9 Docker Containers** (All on `openspg-network`)

#### **1. ner11-gold-api** 🧠 (Port 8000)
**Purpose**: Core NER and Phase B APIs

**What it does**:
- Extracts named entities from text (threat actors, malware, CVEs, IOCs)
- Provides semantic search via Qdrant vector similarity
- Hybrid search combining vectors + Neo4j graph expansion
- Serves 128 Phase B enhancement APIs (SBOM, threat intel, risk, etc.)

**APIs**:
- 5 NER APIs: `/ner`, `/search/semantic`, `/search/hybrid`, `/health`, `/info`
- 123 Phase B APIs: `/api/v2/*` (SBOM, vendor, threat, risk, remediation, etc.)
- **Total**: 128 endpoints

**Access**:
```bash
# Health check
curl http://localhost:8000/health

# Extract entities
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text":"APT29 exploited CVE-2024-12345"}'

# Swagger docs
open http://localhost:8000/docs
```

---

#### **2. aeon-saas-dev** 🖥️ (Port 3000)
**Purpose**: Next.js frontend application with integrated APIs

**What it does**:
- Serves React-based cybersecurity dashboard UI
- Provides 41 Next.js API routes for frontend integration
- Handles user authentication via Clerk
- Multi-tenant customer management

**APIs**:
- Dashboard APIs (4): metrics, activity, distribution, health
- Threat Intel APIs (8): analytics, landscape, ICS, vulnerabilities
- Analytics APIs (7): timeseries, trends, CVE patterns, exports
- Graph APIs (3): Neo4j queries, statistics
- Pipeline APIs (2): document processing, job status
- Query Control APIs (7): pause, resume, checkpoints
- Observability APIs (3): performance, system, agents
- Plus: customers, tags, search, chat, upload

**Total**: 41 endpoints

**Access**:
```bash
# Health check
curl http://localhost:3000/api/health

# View UI
open http://localhost:3000
```

---

#### **3. openspg-neo4j** 🕸️ (Ports 7474, 7687)
**Purpose**: Graph database - core knowledge store

**What it does**:
- Stores 1,207,069 nodes across 631 entity types
- Manages 12,344,852 relationships (183 types)
- Supports Cypher query language
- Hierarchical schema with 17 super labels
- 20-hop multi-hop traversal

**Data Categories**:
- Vulnerabilities: 316,552 CVE nodes (64.65% with CVSS scores)
- Assets: 206,075 equipment/software nodes
- Threats: 10,599 threat actors, 11,601 IOCs, 1,016 malware
- SBOM: 140,000 software components with dependencies
- Compliance: 66,391 controls, 32,907 compliance nodes
- Measurements: 297,858 sensor/telemetry nodes

**Access**:
```bash
# Neo4j Browser (visual query interface)
open http://localhost:7474
# Login: neo4j / neo4j@openspg

# Cypher Shell (command-line)
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j

# Example query
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (c:CVE) WHERE c.cvssV31BaseScore > 9.0 RETURN c.id, c.cvssV31BaseScore LIMIT 10"

# Bolt protocol (from code)
bolt://localhost:7687
```

---

#### **4. openspg-qdrant** 🔍 (Ports 6333-6334)
**Purpose**: Vector database for semantic search

**What it does**:
- Stores 319,456+ entity embeddings (384 dimensions)
- Enables semantic similarity search
- Supports hybrid retrieval (vector + graph)
- 16 collections for different entity types

**Collections**:
- `ner11_entities_hierarchical` - Main entity collection
- `ner11_threat_intel` - Threat-specific entities
- `ner11_vulnerabilities` - CVE embeddings
- `ner11_equipment` - Asset embeddings
- Plus 12 more specialized collections

**Access**:
```bash
# REST API
curl http://localhost:6333/collections

# Search example
curl -X POST http://localhost:6333/collections/ner11_entities_hierarchical/points/search \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.1, 0.2, ...],
    "limit": 10,
    "with_payload": true
  }'

# Web UI
open http://localhost:6333/dashboard
```

---

#### **5. openspg-server** 🤖 (Port 8887)
**Purpose**: OpenSPG knowledge graph reasoning engine

**What it does**:
- Advanced graph reasoning with KAG (Knowledge Augmented Generation)
- Semantic entity linking
- Intelligent path selection for multi-hop queries
- Hybrid reasoning (retrieval + graph traversal + symbolic logic)

**Capabilities**:
- Proven 33.5% improvement on multi-hop reasoning benchmarks
- Natural language to graph query translation
- Progressive depth exploration (avoid combinatorial explosion)
- Confidence scoring for results

**Access**:
```bash
curl http://localhost:8887/
```

**Status**: Deployed but needs authentication configuration (8-16 hours to integrate)

---

#### **6. aeon-postgres-dev** 💾 (Port 5432)
**Purpose**: Application database for SaaS functionality

**What it does**:
- Stores customer/tenant data
- User accounts and sessions
- Application metadata
- Multi-tenant isolation

**Access**:
```bash
docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev

# Connection string
postgresql://postgres:postgres@localhost:5432/aeon_saas_dev
```

---

#### **7. openspg-mysql** 📦 (Port 3306)
**Purpose**: OpenSPG metadata storage

**What it does**:
- Stores OpenSPG schema definitions
- Knowledge graph metadata
- Entity type registrations

**Access**:
```bash
docker exec openspg-mysql mysql -u root -p"openspg" -e "SHOW DATABASES;"

# Connection string
mysql://root:openspg@localhost:3306/openspg
```

---

#### **8. openspg-minio** 📁 (Ports 9000-9001)
**Purpose**: Object storage (S3-compatible)

**What it does**:
- Stores uploaded files (SBOMs, documents, reports)
- Backup storage
- Large binary data

**Access**:
```bash
# Web console
open http://localhost:9001
# Login: minio / minio@openspg

# API
http://localhost:9000
```

---

#### **9. openspg-redis** ⚡ (Port 6379)
**Purpose**: Caching and session storage

**What it does**:
- API response caching
- Session management
- Rate limiting counters
- Temporary data storage

**Access**:
```bash
docker exec openspg-redis redis-cli

# Test
docker exec openspg-redis redis-cli PING
# Returns: PONG
```

---

## 📊 DATA & CAPABILITIES

### **Neo4j Knowledge Graph**

**Scale**:
- **1,207,069 nodes** across **631 labels**
- **12,344,852 relationships** across **183 types**
- **80.95% hierarchical** (977,166 nodes with tier properties)

**17 Super Labels** (Hierarchical Organization):
1. **Vulnerability** (314,538 nodes) - CVEs, CWEs, weaknesses
2. **Measurement** (297,858 nodes) - Sensors, telemetry, metrics
3. **Asset** (206,075 nodes) - Equipment, devices, infrastructure
4. **Control** (66,391 nodes) - Security controls, mitigations
5. **Organization** (56,144 nodes) - Companies, entities
6. **Protocol** (13,336 nodes) - Network protocols
7. **Indicator** (11,601 nodes) - IOCs, observables
8. **ThreatActor** (10,599 nodes) - APT groups, adversaries
9. **Location** (4,830 nodes) - Geographic data
10. **Technique** (4,360 nodes) - MITRE ATT&CK techniques
11. **Event** (2,291 nodes) - Security events, incidents
12. **Software** (1,694 nodes) - Applications, systems
13. **Malware** (1,016 nodes) - Malware families
14. **Campaign** (163 nodes) - Threat campaigns
15. **PsychTrait** (161 nodes) - Psychological traits
16. **EconomicMetric** (39 nodes) - Economic indicators
17. **Role** (15 nodes) - Organizational roles

**Key Entity Counts**:
- **CVEs**: 316,552 (with 64.65% CVSS coverage)
- **Equipment**: 48,288 devices across 16 critical infrastructure sectors
- **SBOM Components**: 140,000 software components
- **Threat Actors**: 10,599 APT groups and adversaries
- **IOCs**: 11,601 indicators of compromise
- **CWE Weaknesses**: 707 weakness types

**Relationship Types** (Top 10 by volume):
1. IMPACTS (4.78M) - Vulnerability impact chains
2. VULNERABLE_TO (3.12M) - Asset-vulnerability mappings
3. INSTALLED_ON (968K) - Equipment installation
4. MONITORS_EQUIPMENT (289K) - Sensor monitoring
5. CONSUMES_FROM (289K) - Data flow
6. IS_WEAKNESS_TYPE (225K) - CVE-CWE mappings
7. HAS_COMPONENT (140K) - SBOM component relationships
8. DEPENDS_ON (89K) - Dependencies
9. HAS_VULNERABILITY (82K) - Component vulnerabilities
10. USES (31K) - Threat actor TTPs

---

### **Qdrant Vector Database**

**Collections** (16 total):
1. `ner11_entities_hierarchical` - Main entity embeddings
2. `ner11_threat_intel` - Threat-specific vectors
3. `ner11_vulnerabilities` - CVE embeddings
4. `ner11_equipment` - Asset embeddings
5. `ner11_sbom` - Component embeddings
6-16. Additional specialized collections

**Capabilities**:
- Semantic similarity search
- Fuzzy matching
- Entity deduplication
- Recommendation systems
- Anomaly detection

---

## 🎯 CAPABILITIES

### **1. Entity Extraction** (NER Gold v3.1)

**What it does**: Extracts 60 entity types from unstructured text

**Entity Types**:
- **Threats**: APT_GROUP, THREAT_ACTOR, MALWARE, RANSOMWARE
- **Vulnerabilities**: CVE, CWE, CAPEC
- **Infrastructure**: DEVICE, EQUIPMENT, SOFTWARE, PROTOCOL
- **Organizations**: COMPANY, GOVERNMENT, ORGANIZATION
- **Locations**: COUNTRY, REGION, CITY
- **Technical**: IP_ADDRESS, DOMAIN, HASH, URL
- Plus 40+ more types

**How to use**:
```bash
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{
    "text": "APT29 exploited CVE-2024-12345 in Microsoft Exchange servers using PowerShell"
  }'

# Returns:
# - APT29 (APT_GROUP)
# - CVE-2024-12345 (CVE)
# - Microsoft Exchange (SOFTWARE)
# - PowerShell (TECHNIQUE)
```

---

### **2. Semantic Search**

**What it does**: Find similar entities using vector embeddings

**How to use**:
```bash
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "ransomware",
    "limit": 10,
    "tier1_filter": "TECHNICAL"
  }'

# Returns: Top 10 most similar entities to "ransomware"
```

---

### **3. Hybrid Search** (Vector + Graph)

**What it does**: Combines semantic search with graph traversal (up to 20 hops)

**How to use**:
```bash
curl -X POST http://localhost:8000/search/hybrid \
  -H "Content-Type: application/json" \
  -d '{
    "query": "APT29",
    "expand_graph": true,
    "hop_depth": 3,
    "relationship_types": ["USES", "TARGETS", "EXPLOITS"]
  }'

# Returns: APT29 + related malware + targeted systems + exploited CVEs
```

---

### **4. Threat Intelligence** (12 Working APIs)

**Capabilities**:
- Track active IOCs (indicators of compromise)
- MITRE ATT&CK coverage analysis
- Threat actor relationship graphs
- Campaign tracking
- Kill chain analysis

**Example**:
```bash
# Get MITRE ATT&CK coverage
curl http://localhost:8000/api/v2/threat-intel/mitre/coverage \
  -H "x-customer-id: dev"

# Get active IOCs
curl http://localhost:8000/api/v2/threat-intel/iocs/active \
  -H "x-customer-id: dev"
```

---

### **5. Risk Scoring** (9 Working APIs)

**Capabilities**:
- Multi-factor risk calculation
- Sector-specific risk assessment
- Vendor risk analysis
- Asset criticality scoring
- Trending risk identification

**Example**:
```bash
# Get high-risk assets
curl http://localhost:8000/api/v2/risk/high \
  -H "x-customer-id: dev"

# Risk by sector
curl http://localhost:8000/api/v2/risk/by-sector/energy \
  -H "x-customer-id: dev"
```

---

### **6. SBOM Analysis** (8 Working APIs)

**Capabilities**:
- Software Bill of Materials parsing
- Component vulnerability tracking
- Dependency graph analysis
- License compliance checking
- Supply chain risk assessment

**Example**:
```bash
# SBOM dashboard
curl http://localhost:8000/api/v2/sbom/dashboard/summary \
  -H "x-customer-id: dev"

# Component risk analysis
curl http://localhost:8000/api/v2/sbom/analysis/component-risk \
  -H "x-customer-id: dev"
```

---

### **7. Equipment & Asset Management** (5 Working APIs)

**Capabilities**:
- Track 48,288 equipment instances
- Monitor end-of-life (EOL) status
- Vendor risk assessment
- Vulnerability correlation
- Sector-specific analysis (16 critical infrastructure sectors)

**Example**:
```bash
# Equipment dashboard
curl http://localhost:8000/api/v2/equipment/dashboard/summary \
  -H "x-customer-id: dev"

# Equipment by sector
curl http://localhost:8000/api/v2/equipment/dashboard/by-sector \
  -H "x-customer-id: dev"
```

---

## 🚀 GETTING STARTED (5 Minutes)

### **Step 1: Verify System Health** (1 minute)

```bash
# Navigate to system folder
cd /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed

# Run health check
./SYSTEM_HEALTH_CHECK.sh

# Or open visual dashboard
open SYSTEM_HEALTH_DASHBOARD.html
```

**Expected**: 7-9 containers healthy, key APIs responding

---

### **Step 2: Test Core APIs** (2 minutes)

```bash
# Test NER API
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text":"APT29 exploited CVE-2024-12345"}'

# Expected: JSON with entities array

# Test Threat Intel
curl http://localhost:8000/api/v2/threat-intel/dashboard/summary \
  -H "x-customer-id: dev"

# Expected: JSON with threat statistics
```

---

### **Step 3: Query Neo4j** (1 minute)

```bash
# Open Neo4j Browser
open http://localhost:7474
# Login: neo4j / neo4j@openspg

# Run query in browser:
MATCH (c:CVE)
WHERE c.cvssV31BaseScore > 9.0
RETURN c.id, c.cvssV31BaseScore, c.description
LIMIT 10
```

**Expected**: List of critical CVEs with CVSS scores

---

### **Step 4: Test Qdrant** (1 minute)

```bash
# List collections
curl http://localhost:6333/collections

# Expected: List of 9-16 collections

# Check main collection
curl http://localhost:6333/collections/ner11_entities_hierarchical

# Expected: Collection info with point count
```

---

### **Step 5: Review Documentation** (<1 minute)

```bash
# Open master index
cat docs/UI_DEVELOPER_MASTER_INDEX.md

# Or open README
cat README.md
```

**You're ready!** ✅

---

## 👨‍💻 DEVELOPER WORKFLOWS

### **Workflow 1: Build Threat Intelligence Dashboard**

**Goal**: Display active threats, CVEs, and MITRE ATT&CK coverage

**APIs to use**:
1. `GET /api/v2/threat-intel/dashboard/summary` - Overview stats
2. `GET /api/v2/threat-intel/iocs/active` - Active IOCs
3. `GET /api/v2/threat-intel/mitre/coverage` - ATT&CK heatmap
4. `GET /api/v2/threat-intel/mitre/gaps` - Coverage gaps

**Sample React Component**:
```javascript
import React, { useEffect, useState } from 'react';

function ThreatDashboard() {
  const [threats, setThreats] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/v2/threat-intel/dashboard/summary', {
      headers: { 'x-customer-id': 'dev' }
    })
    .then(r => r.json())
    .then(data => setThreats(data))
    .catch(err => console.error(err));
  }, []);

  if (!threats) return <div>Loading...</div>;

  return (
    <div>
      <h1>Threat Intelligence</h1>
      <div>Active IOCs: {threats.active_iocs}</div>
      <div>Total Threat Actors: {threats.total_actors}</div>
      <div>Active Campaigns: {threats.active_campaigns}</div>
    </div>
  );
}
```

---

### **Workflow 2: Query Equipment Vulnerabilities**

**Goal**: Show vulnerabilities for critical infrastructure equipment

**Neo4j Query**:
```cypher
// Find SCADA equipment with critical vulnerabilities
MATCH (e:Equipment)-[:HAS_VULNERABILITY]->(c:CVE)
WHERE e.sector = 'ENERGY'
  AND c.cvssV31BaseScore > 7.0
RETURN e.name, e.sector, c.id, c.cvssV31BaseScore, c.description
ORDER BY c.cvssV31BaseScore DESC
LIMIT 50
```

**Using Neo4j Driver** (JavaScript):
```javascript
const neo4j = require('neo4j-driver');

const driver = neo4j.driver(
  'bolt://localhost:7687',
  neo4j.auth.basic('neo4j', 'neo4j@openspg')
);

const session = driver.session({ database: 'neo4j' });

const result = await session.run(`
  MATCH (e:Equipment)-[:HAS_VULNERABILITY]->(c:CVE)
  WHERE e.sector = $sector AND c.cvssV31BaseScore > $threshold
  RETURN e, c
  LIMIT 50
`, { sector: 'ENERGY', threshold: 7.0 });

session.close();
driver.close();
```

---

### **Workflow 3: Real-time Entity Extraction**

**Goal**: Extract entities from user input in real-time

**Implementation**:
```javascript
async function extractEntities(text) {
  const response = await fetch('http://localhost:8000/ner', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });

  const { entities } = await response.json();

  // entities = [
  //   {text: "APT29", label: "APT_GROUP", score: 0.95, start: 0, end: 5},
  //   {text: "CVE-2024-12345", label: "CVE", score: 1.0, start: 16, end: 30}
  // ]

  return entities;
}

// Usage in UI
const handleTextSubmit = async (inputText) => {
  const entities = await extractEntities(inputText);
  highlightEntitiesInText(inputText, entities);
  displayEntityList(entities);
};
```

---

### **Workflow 4: SBOM Supply Chain Analysis**

**Goal**: Visualize software dependencies and vulnerabilities

**APIs**:
```bash
# Get SBOM summary
curl http://localhost:8000/api/v2/sbom/dashboard/summary -H "x-customer-id: dev"

# Analyze dependencies
curl http://localhost:8000/api/v2/sbom/analysis/dependencies -H "x-customer-id: dev"

# Check license risks
curl http://localhost:8000/api/v2/sbom/analysis/license-risk -H "x-customer-id: dev"
```

---

## 🏛️ ARCHITECTURE DEEP DIVE

### **Data Flow**

```
User Input (Text/File)
    ↓
NER11 API (Extract Entities)
    ↓
Neo4j (Store in Graph) ←→ Qdrant (Create Embeddings)
    ↓
Phase B APIs (Enrich & Analyze)
    ↓
Frontend UI (Visualize)
```

### **Multi-Hop Reasoning Flow**

```
Query: "Show me APT29's attack path"
    ↓
1. Qdrant: Find APT29 entity (semantic search)
    ↓
2. Neo4j: Traverse relationships
   APT29 -[USES]→ Malware -[EXPLOITS]→ CVE -[AFFECTS]→ Software -[INSTALLED_ON]→ Equipment
    ↓
3. Return: Complete attack path with all nodes and relationships
```

### **Enrichment Pipeline**

```
1. E30 Bulk Ingestion
   Documents → NER11 → Entities → Neo4j + Qdrant

2. PROC-102 Kaggle Enrichment
   CVEs → Kaggle Dataset → CVSS Scores → Neo4j (278K enriched)

3. Hierarchical Classification
   Entities → NER11 Taxonomy (566 types) → Neo4j Properties
```

---

## 🔐 CREDENTIALS & ACCESS

### **All Services**:

| Service | URL | Username | Password | Database |
|---------|-----|----------|----------|----------|
| Neo4j | bolt://localhost:7687 | neo4j | neo4j@openspg | neo4j |
| Neo4j Browser | http://localhost:7474 | neo4j | neo4j@openspg | - |
| Qdrant | http://localhost:6333 | - | (no auth) | - |
| PostgreSQL | localhost:5432 | postgres | postgres | aeon_saas_dev |
| MySQL | localhost:3306 | root | openspg | openspg |
| MinIO Console | http://localhost:9001 | minio | minio@openspg | - |
| MinIO API | http://localhost:9000 | minio | minio@openspg | - |
| Redis | localhost:6379 | - | (no auth) | - |
| NER11 API | http://localhost:8000 | - | (no auth) | - |
| Next.js App | http://localhost:3000 | - | (Clerk auth) | - |

**⚠️ Security Note**: This is a development environment. For production:
- Change all passwords
- Enable authentication on all services
- Add SSL/TLS
- Implement API keys

---

## 🛠️ COMMON DEVELOPMENT TASKS

### **Task: Add New Data to Neo4j**

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "neo4j@openspg")
)

with driver.session(database="neo4j") as session:
    session.run("""
        MERGE (ta:ThreatActor {name: $name})
        SET ta.country = $country,
            ta.first_seen = datetime($first_seen)
        RETURN ta
    """, name="APT99", country="Unknown", first_seen="2025-01-01T00:00:00Z")

driver.close()
```

---

### **Task: Search Qdrant for Similar Entities**

```python
from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)

# Search for entities similar to "ransomware"
results = client.search(
    collection_name="ner11_entities_hierarchical",
    query_vector=[0.1, 0.2, ...],  # Get from embedding model
    limit=10,
    with_payload=True
)

for result in results:
    print(f"{result.payload['text']}: {result.score}")
```

---

### **Task: Run Data Enrichment Procedure**

```bash
# Execute PROC-101: NVD API Enrichment (fill remaining CVSS gaps)
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
./scripts/proc_101_nvd_enrichment.sh

# This will:
# 1. Query NVD API for missing CVEs
# 2. Extract CVSS scores
# 3. Update Neo4j nodes
# 4. Validate enrichment

# Expected: 37,994 CVEs enriched (12% gap filled)
```

---

## 📚 DOCUMENTATION GUIDE

### **For UI Developers**:
1. **START**: `README.md` (you're here!)
2. **NEXT**: `docs/UI_DEVELOPER_MASTER_INDEX.md` - Complete navigation hub
3. **QUICKSTART**: `FRONTEND_QUICKSTART_COMPLETE.md` - 5-minute setup
4. **APIS**: `WORKING_APIS_FOR_UI_DEVELOPERS.md` - 37 verified endpoints
5. **SCHEMA**: `docs/COMPLETE_SCHEMA_REFERENCE_ENHANCED.md` - All 631 labels

### **For Backend Developers**:
6. **ARCHITECTURE**: `COMPREHENSIVE_APPLICATION_RATING.md` - System design
7. **APIS**: `COMPLETE_API_REFERENCE_FINAL.md` - All 232 APIs
8. **TESTING**: `COMPREHENSIVE_API_TESTING_PLAN.md` - Test framework

### **For DevOps**:
9. **HEALTH**: `SYSTEM_HEALTH_CHECK.sh` - Automated diagnostics
10. **STATUS**: `FINAL_ACCURATE_STATUS.md` - Current state

### **For Data Engineers**:
11. **PROCEDURES**: `13_procedures/` folder - 35 ETL procedures
12. **PIPELINE**: Pipeline documentation (E30 bulk ingestion, NER Gold v3.1)

---

## 🐛 TROUBLESHOOTING

### **Issue: API returns "Customer context required"**

**Solution**:
```bash
# Add header to all Phase B API requests
curl http://localhost:8000/api/v2/sbom/sboms \
  -H "x-customer-id: dev"
```

---

### **Issue: Container not running**

**Solution**:
```bash
# Check container status
docker ps -a | grep [container-name]

# Start container
docker start [container-name]

# Check logs
docker logs [container-name]
```

---

### **Issue: Neo4j connection refused**

**Solution**:
```bash
# Verify Neo4j is running
docker ps | grep neo4j

# Test connection
curl http://localhost:7474

# Restart if needed
docker restart openspg-neo4j
```

---

### **Issue: Qdrant unhealthy**

**Solution**:
```bash
# Check Qdrant status
curl http://localhost:6333/collections

# Restart
docker restart openspg-qdrant

# Wait 30 seconds
sleep 30
```

---

## 📈 SYSTEM STATUS

**Current Rating**: **5.8/10** (Fair)

**What's Working**:
- ✅ 37 APIs operational (16%)
- ✅ Neo4j database with 1.2M nodes
- ✅ Qdrant vector search
- ✅ NER entity extraction
- ✅ Basic dashboards buildable

**What Needs Work**:
- ⚠️ 84% APIs need testing/fixes
- ⚠️ Security (no auth, no SSL)
- ⚠️ Testing (97% APIs untested)
- ⚠️ Production readiness (no HA, monitoring)

**Timeline to Production Ready (8/10)**: 3-4 months

---

## 🎯 NEXT STEPS

### **For UI Developers (Start Building)**:
1. Read `docs/UI_DEVELOPER_MASTER_INDEX.md`
2. Open `SYSTEM_HEALTH_DASHBOARD.html` to verify system
3. Copy code examples from `FRONTEND_QUICKSTART_COMPLETE.md`
4. Build threat intelligence dashboard (APIs 3-14)
5. Build risk management dashboard (APIs 15-23)

### **For Backend Developers (Improve System)**:
1. Execute `IMMEDIATE_EXECUTION_PLAN.md` (fixes)
2. Test all 232 APIs systematically
3. Fix customer context bugs
4. Add authentication
5. Create automated test suite

### **For DevOps (Production Prep)**:
1. Create docker-compose.yml
2. Add SSL/TLS certificates
3. Set up monitoring (Prometheus + Grafana)
4. Configure backups and disaster recovery
5. Load testing and optimization

---

## 📞 SUPPORT & RESOURCES

**Documentation Location**: `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/`

**Key Files**:
- This document: `INTRODUCTION_AND_GETTING_STARTED.md`
- API Reference: `WORKING_APIS_FOR_UI_DEVELOPERS.md`
- Schema Reference: `docs/COMPLETE_SCHEMA_REFERENCE_ENHANCED.md`
- Health Checks: `SYSTEM_HEALTH_CHECK.sh` / `SYSTEM_HEALTH_DASHBOARD.html`

**Qdrant Memory**: Stored in `frontend-package` collection

**Git Repository**: All committed (15 total commits)

---

## ✅ SYSTEM READY FOR

- ✅ UI Development (37 working APIs)
- ✅ Data Exploration (1.2M nodes, 12.3M relationships)
- ✅ Threat Analysis (316K CVEs, 10K actors)
- ✅ Research & Development
- ⏳ Production Deployment (needs security hardening)

---

**Welcome to AEON!** 🚀

Start building cybersecurity intelligence dashboards with the world's most comprehensive threat knowledge graph.
