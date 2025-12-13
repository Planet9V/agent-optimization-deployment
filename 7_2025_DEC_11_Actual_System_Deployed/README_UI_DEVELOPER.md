# AEON Platform - UI Developer Quick Start

**Created:** 2025-12-12
**Status:** Production Ready
**Version:** v1.0.0

---

## 📚 What You Get

This directory contains **everything a UI developer needs** to start building interfaces for the AEON cybersecurity intelligence platform.

### Files in This Directory

1. **`UI_DEVELOPER_COMPLETE_GUIDE.md`** - 📖 Comprehensive 200+ section guide
   - System architecture diagrams
   - Complete API reference with examples
   - Database schemas and query examples
   - 5 complete UI workflows
   - React/Vue component examples
   - Performance tips and troubleshooting

2. **`test_ui_connection.html`** - 🧪 Interactive connection tester
   - Tests all API endpoints
   - Displays live threat intelligence
   - Shows system statistics
   - Beautiful dashboard example
   - **Open in browser to verify everything works**

3. **`retrieve_ui_guide.sh`** - 🔍 Qdrant retrieval script
   - Fetch guide sections from vector database
   - Demonstrates semantic search
   - Shows how to use Qdrant API

---

## ⚡ 5-Minute Quick Start

### Step 1: Verify System is Running
```bash
# Check all services
docker ps | grep -E "aeon|neo4j|qdrant"

# Test API
curl http://localhost:3001/health

# Test Neo4j
curl http://localhost:7474/

# Test Qdrant
curl http://localhost:6333/collections
```

### Step 2: Open Test Dashboard
```bash
# Linux
xdg-open test_ui_connection.html

# Mac
open test_ui_connection.html

# Windows
start test_ui_connection.html
```

**Expected Result:** Beautiful dashboard showing:
- ✓ API health check
- ✓ 10+ APT groups from Neo4j
- ✓ 16 Qdrant collections
- ✓ 20 active threats with malware
- ✓ System statistics (APT groups, malware, vulnerabilities, equipment)

### Step 3: Build Your First Query

**JavaScript (in browser console):**
```javascript
fetch('http://localhost:3001/api/v1/neo4j/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'MATCH (apt:APTGroup)-[:USES]->(m:Malware) RETURN apt.name, m.name LIMIT 10'
  })
})
.then(res => res.json())
.then(data => console.table(data.results));
```

**Python:**
```python
import requests

response = requests.post('http://localhost:3001/api/v1/neo4j/query',
  json={'query': 'MATCH (apt:APTGroup) RETURN apt.name LIMIT 10'}
)
print(response.json())
```

**curl:**
```bash
curl -X POST http://localhost:3001/api/v1/neo4j/query \
  -H "Content-Type: application/json" \
  -d '{"query": "MATCH (apt:APTGroup) RETURN apt.name LIMIT 10"}'
```

---

## 🎯 What Can You Build?

### 1. Threat Intelligence Dashboard
**Data:** 450+ APT groups, 12,000+ malware families, 85,000+ CVEs
**APIs:** Neo4j graph queries, Qdrant semantic search
**Example:** `test_ui_connection.html` (already implemented!)

### 2. SBOM Vulnerability Analyzer
**Data:** Software components with CVE matching
**APIs:** POST `/api/v1/sbom/analyze`
**Use Case:** Upload SBOM, get vulnerability report with risk scores

### 3. Equipment Inventory Tracker
**Data:** 50,000+ network/IT equipment with locations
**APIs:** Neo4j queries for equipment and vulnerabilities
**Features:** Filter by location, display vulnerabilities, calculate risk

### 4. Risk Calculator
**Data:** CVSS scores + contextual risk factors
**APIs:** POST `/api/v1/risk/calculate`
**Features:** Real-time risk scoring, remediation recommendations

### 5. Remediation Planner
**Data:** Vulnerability priorities, resource constraints
**APIs:** POST `/api/v1/remediation/plan`
**Features:** Generate prioritized fix plans, Gantt charts, cost estimates

---

## 🗄️ Data You Have Access To

### Neo4j Graph Database (1.2M nodes, 12.3M relationships)

**Node Types:**
- `APTGroup` - 450+ advanced persistent threats
- `Malware` - 12,000+ malicious software families
- `Vulnerability` - 85,000+ CVEs
- `Equipment` - 50,000+ IT/network assets
- `Location` - 1,200+ physical locations
- `Remediation` - 25,000+ fix plans
- `ThreatActor` - 800+ individual actors
- `Campaign` - 2,000+ attack campaigns
- `Technique` - 600+ MITRE ATT&CK techniques
- `IOC` - 200,000+ indicators of compromise

**Relationship Types:**
- `USES` - APTGroup uses Malware
- `EXPLOITS` - Malware exploits Vulnerability
- `HAS_VULNERABILITY` - Equipment has Vulnerability
- `LOCATED_AT` - Equipment at Location
- `ADDRESSES` - Remediation addresses Vulnerability
- ... and 631 total label types!

### Qdrant Vector Database (319K+ entity embeddings)

**Collections:**
- `ner11_entities_hierarchical` - 319K entities with semantic search
- `ner11_sbom` - Software bill of materials
- `ner11_vendor_equipment` - Equipment catalog
- `ner11_risk_scoring` - Risk assessments
- `ner11_remediation` - Remediation plans
- `aeon-final` - UI developer guide (this documentation!)

---

## 📖 Complete Documentation

**Read the full guide:**
```bash
cat UI_DEVELOPER_COMPLETE_GUIDE.md
```

**Or view specific sections:**
```bash
# System architecture
./retrieve_ui_guide.sh architecture

# API reference
./retrieve_ui_guide.sh api_reference

# UI workflows
./retrieve_ui_guide.sh workflows

# React/Vue components
./retrieve_ui_guide.sh components
```

**Search semantically in Qdrant:**
```bash
./retrieve_ui_guide.sh quick_start
```

---

## 🚀 API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | System health check |
| `/api/v1/neo4j/query` | POST | Run Cypher queries |
| `/api/v1/qdrant/search` | POST | Vector similarity search |
| `/api/v1/sbom/analyze` | POST | Analyze SBOM files |
| `/api/v1/risk/calculate` | POST | Calculate risk scores |
| `/api/v1/remediation/plan` | POST | Generate remediation plans |

**Neo4j:** http://localhost:7474 (neo4j/password)
**Qdrant:** http://localhost:6333 (no auth)
**API:** http://localhost:3001 (no auth for dev)

---

## 🎨 Example Queries

### Get Top Threats
```javascript
{
  "query": `
    MATCH (apt:APTGroup)-[:USES]->(m:Malware)-[:EXPLOITS]->(v:Vulnerability)
    WHERE v.cvss_score > 7.0
    RETURN apt.name, apt.country, count(v) as critical_vulns
    ORDER BY critical_vulns DESC
    LIMIT 20
  `
}
```

### Equipment by Location
```javascript
{
  "query": `
    MATCH (e:Equipment)-[:LOCATED_AT]->(loc:Location)
    WHERE loc.building = 'Data Center 1'
    RETURN loc.floor, e.vendor, e.model, count(e) as equipment_count
    ORDER BY loc.floor
  `
}
```

### Vector Search for Similar Malware
```javascript
POST http://localhost:6333/collections/ner11_entities_hierarchical/points/search
{
  "vector": { "name": "default", "vector": [0.1, 0.2, ...] },
  "limit": 20,
  "filter": {
    "must": [{ "key": "entity_type", "match": { "value": "Malware" } }]
  }
}
```

---

## 🐛 Troubleshooting

**API not responding:**
```bash
docker logs aeon-saas-dev
docker restart aeon-saas-dev
```

**Neo4j connection error:**
```bash
curl http://localhost:7474/
docker restart neo4j
```

**Empty Qdrant results:**
```bash
curl http://localhost:6333/collections/ner11_entities_hierarchical
```

**CORS errors:**
Add proxy to `package.json`:
```json
{ "proxy": "http://localhost:3001" }
```

---

## ✅ Validation Checklist

Before you start building, verify:

- [ ] All Docker containers running (`docker ps`)
- [ ] Neo4j accessible (http://localhost:7474)
- [ ] Qdrant accessible (http://localhost:6333)
- [ ] API health check passes (`curl localhost:3001/health`)
- [ ] Test dashboard displays data (`test_ui_connection.html`)
- [ ] Sample Neo4j query returns results
- [ ] Qdrant collections list shows 16+ collections

---

## 🎯 Next Steps

1. **Read the complete guide:** `UI_DEVELOPER_COMPLETE_GUIDE.md`
2. **Test the connection:** Open `test_ui_connection.html`
3. **Try example queries:** Copy from guide, modify, test
4. **Build your first component:** Start with threat cards
5. **Add semantic search:** Use Qdrant for smart search
6. **Create dashboard:** Combine graph + vector data

---

## 📚 Additional Resources

**In the guide:**
- 50+ Cypher query examples
- 10+ Qdrant search patterns
- 5 complete UI workflows
- React/Vue component templates
- Performance optimization tips
- Troubleshooting guide

**External:**
- Neo4j Cypher Manual: https://neo4j.com/docs/cypher-manual/
- Qdrant API Docs: https://qdrant.tech/documentation/
- MITRE ATT&CK: https://attack.mitre.org/

---

**You have REAL DATA and WORKING APIs. Start building! 🚀**

For questions, check `UI_DEVELOPER_COMPLETE_GUIDE.md` or the troubleshooting section.
