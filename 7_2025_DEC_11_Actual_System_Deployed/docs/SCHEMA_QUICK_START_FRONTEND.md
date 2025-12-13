# Neo4j Schema Quick Start for Frontend Developers

**Last Updated**: 2025-12-12
**Status**: ✅ PRODUCTION-READY

---

## 🚀 Quick Start

### 1. Get Complete Schema Documentation

**From Qdrant** (Recommended):
```python
from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)
result = client.retrieve(
    collection_name="frontend-package",
    ids=["b9062c00-b301-5c05-a00f-5e9fc62b369c"]
)

schema_doc = result[0].payload['content']
# Full documentation with all 631 labels, 183 relationships, and examples
```

**From File**:
```bash
cat /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/COMPLETE_SCHEMA_REFERENCE_ENHANCED.md
```

---

## 📊 Schema Overview

### Database Stats

| Metric | Count |
|--------|-------|
| Total Nodes | 1,207,069 |
| Total Relationships | 12,344,852 |
| Labels | 631 |
| Relationship Types | 183 |
| Super Labels | 17 |

### Hierarchical Structure

```
TIER 1 (Domain) → TIER 2 (Super Label) → LABEL (Implementation)

5 Domains:
- TECHNICAL (28.9%)
- CONTEXTUAL (25.0%)
- ASSET (16.7%)
- OPERATIONAL (5.6%)
- ORGANIZATIONAL (4.7%)

17 Super Labels:
- Vulnerability, Measurement, Asset, Control, Organization,
  Indicator, ThreatActor, Protocol, Location, Technique,
  Event, Software, Malware, PsychTrait, EconomicMetric,
  Role, Campaign
```

---

## 🎯 Top 10 Most Important Labels

| Rank | Label | Count | Super Label | Use Case |
|------|-------|-------|-------------|----------|
| 1 | CVE | 316,552 | Vulnerability | Security vulnerabilities |
| 2 | Measurement | 275,458 | Measurement | Sensor/monitoring data |
| 3 | Asset | 90,113 | Asset | Infrastructure assets |
| 4 | SBOM | 140,000 | Asset | Software bill of materials |
| 5 | Equipment | 48,288 | Asset | Industrial equipment |
| 6 | Device | 48,400 | Asset | Physical devices |
| 7 | Control | 61,167 | Control | Security controls |
| 8 | Threat | 9,875 | ThreatActor | Threat actors |
| 9 | Indicator | 6,601 | Indicator | IOCs (indicators of compromise) |
| 10 | Technique | 3,526 | Technique | ATT&CK techniques |

---

## 🔍 Essential Queries

### 1. Find Critical Vulnerabilities

```cypher
MATCH (cve:CVE)-[:IMPACTS]->(asset:Asset)
WHERE cve.cvssV31BaseSeverity = 'CRITICAL'
  AND cve.epss_score > 0.5
RETURN cve.id, cve.description, cve.epss_score,
       collect(asset.device_name)[0..5] as affected_assets
ORDER BY cve.epss_score DESC
LIMIT 20
```

### 2. Get Infrastructure by Sector

```cypher
MATCH (asset:Asset)
WHERE asset.subsector = 'Energy_Transmission'
RETURN asset.device_name, asset.device_type, asset.status
LIMIT 100
```

### 3. Threat Actor Techniques

```cypher
MATCH (ta:ThreatActor)-[:USES_TECHNIQUE]->(tech:Technique)
WHERE ta.sophistication = 'advanced'
RETURN ta.name, collect(tech.name) as techniques
```

### 4. Software Supply Chain

```cypher
MATCH (sbom:SBOM)-[:SBOM_CONTAINS]->(comp:Software_Component)
      -[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.cvssV31BaseSeverity IN ['HIGH', 'CRITICAL']
RETURN sbom.name, comp.name, collect(cve.id) as vulnerabilities
```

### 5. Real-time Measurements

```cypher
MATCH (m:Measurement)
WHERE m.timestamp > datetime() - duration('PT1H')
  AND m.subsector = 'Energy_Transmission'
RETURN m.measurement_type, m.value, m.unit, m.timestamp
ORDER BY m.timestamp DESC
LIMIT 100
```

---

## 🎨 UI Component Recommendations

### 1. Vulnerability Dashboard

**Data Source**: CVE nodes + IMPACTS relationships

**Key Metrics**:
- Total CVEs: 316,552
- Critical CVEs: Filter by `cvssV31BaseSeverity = 'CRITICAL'`
- High Exploit Probability: Filter by `epss_score > 0.7`
- Affected Assets: Count via `IMPACTS` relationships

**Sample Query**:
```cypher
MATCH (cve:CVE)
RETURN cve.cvssV31BaseSeverity as severity,
       count(cve) as count
ORDER BY severity DESC
```

### 2. Infrastructure Map

**Data Source**: Asset nodes + sector properties

**Filters**:
- Sector: 16 critical infrastructure sectors
- Asset Type: Device, Equipment, SCADA, etc.
- Status: operational, degraded, offline

**Sample Query**:
```cypher
MATCH (asset:Asset)
RETURN asset.subsector, asset.device_type, count(asset) as count
ORDER BY count DESC
```

### 3. Threat Intelligence Feed

**Data Source**: ThreatActor, Indicator, Technique nodes

**Features**:
- APT Group Profiles
- Malware Attribution
- IOC Tracking (11,601 indicators)
- Attack Techniques (3,526 techniques)

**Sample Query**:
```cypher
MATCH (ioc:Indicator)-[:INDICATES]->(ta:ThreatActor)
WHERE ioc.threat_level = 'High'
RETURN ioc.indicatorValue, ioc.indicatorType, ta.name
ORDER BY ioc.firstSeen DESC
LIMIT 100
```

### 4. Measurement Monitor

**Data Source**: 297K Measurement nodes

**Types**:
- uptime (~27,000)
- temperature (~18,000)
- pressure (~15,000)
- radiation (~18,000)
- transaction (~17,000)
- response_time (~17,000)

**Sample Query**:
```cypher
MATCH (equipment:Equipment)-[:GENERATES_MEASUREMENT]->(m:Measurement)
WHERE m.timestamp > datetime() - duration('P1D')
RETURN equipment.device_name,
       m.measurement_type,
       avg(m.value) as avg_value,
       m.unit
GROUP BY equipment.device_name, m.measurement_type, m.unit
```

### 5. Compliance Tracker

**Data Source**: Control, ComplianceCertification, NERCCIPStandard nodes

**Sample Query**:
```cypher
MATCH (asset:Asset)-[:COMPLIES_WITH]->(standard:NERCCIPStandard)
RETURN standard.name, standard.level, count(asset) as compliant_count
ORDER BY standard.level DESC
```

---

## 🔗 Key Relationships for UI

### Top 10 Relationships by Count

| Rank | Relationship | Count | UI Use Case |
|------|--------------|-------|-------------|
| 1 | IMPACTS | 4,780,563 | CVE → Asset: Show affected systems |
| 2 | VULNERABLE_TO | 3,117,735 | Asset → CVE: Show vulnerabilities |
| 3 | INSTALLED_ON | 968,125 | Software → Location: Physical topology |
| 4 | TRACKS_PROCESS | 344,256 | Measurement → Process: Process monitoring |
| 5 | MONITORS_EQUIPMENT | 289,233 | Sensor → Equipment: Equipment health |
| 6 | CONSUMES_FROM | 289,050 | Equipment → Resource: Dependency tracking |
| 7 | PROCESSES_THROUGH | 270,203 | Material → Equipment: Production flow |
| 8 | MITIGATES | 250,782 | Control → CVE: Security controls |
| 9 | CHAINS_TO | 225,358 | Technique → Technique: Attack paths |
| 10 | DELIVERS_TO | 216,126 | Equipment → Location: Supply chain |

---

## 🚦 Filtering Patterns

### By Super Label (Fast - 81% coverage)

```cypher
MATCH (n)
WHERE n.super_label = 'Vulnerability'
RETURN n
LIMIT 1000
```

### By Label (Fastest - 100% coverage)

```cypher
MATCH (cve:CVE)
WHERE cve.cvssV31BaseSeverity = 'CRITICAL'
RETURN cve
```

### By Tier (Fast)

```cypher
MATCH (n)
WHERE n.tier1 = 'TECHNICAL'
RETURN n.super_label, count(n) as count
```

### By Sector (Domain-specific)

```cypher
MATCH (n)
WHERE n.subsector = 'Energy_Transmission'
RETURN labels(n) as node_type, count(n) as count
```

---

## 📈 Property Cheat Sheet

### Common Properties (Present on Most Nodes)

```javascript
{
  // Hierarchy (81% of nodes)
  tier1: "TECHNICAL" | "CONTEXTUAL" | "ASSET" | "OPERATIONAL" | "ORGANIZATIONAL",
  tier2: String,           // Super label
  super_label: String,     // Same as tier2
  fine_grained_type: String,

  // Identity
  id: String,
  name: String,

  // Metadata
  node_type: String        // Implementation label
}
```

### CVE Properties

```javascript
{
  id: "CVE-YYYY-NNNN",
  description: String,
  cvssV2BaseScore: Float,
  cvssV31BaseSeverity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
  epss_score: Float,       // 0.0-1.0 (exploit probability)
  epss_percentile: Float,  // 0.0-1.0
  priority_tier: "NEVER" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
  cpe_vendors: [String],
  cpe_products: [String],
  published_date: DateTime,
  modified_date: DateTime
}
```

### Asset Properties

```javascript
{
  device_name: String,
  device_type: String,
  manufacturer: String,
  model: String,
  status: "operational" | "degraded" | "offline" | "maintenance",
  ip_address: String,
  install_date: DateTime,
  subsector: String        // Critical infrastructure sector
}
```

### Measurement Properties

```javascript
{
  value: Float | Integer,
  unit: String,            // %, degrees, psi, etc.
  quality: "poor" | "fair" | "good" | "excellent",
  timestamp: DateTime,
  measurement_type: String, // uptime, temperature, pressure, etc.
  subsector: String
}
```

---

## ⚡ Performance Tips

### Use Indexes

The following properties are indexed for fast queries:
- `super_label`
- `tier1`, `tier2`
- CVE: `id`, `cvssV31BaseSeverity`, `epss_score`
- Asset: `subsector`, `device_type`
- Measurement: `timestamp`, `measurement_type`

### Limit Relationship Depth

```cypher
// GOOD: Limited depth
MATCH path = (a)-[*1..3]-(b)
RETURN path

// BAD: Unbounded (can crash)
MATCH path = (a)-[*]-(b)
RETURN path
```

### Use Label Filters

```cypher
// FAST: Uses label index
MATCH (cve:CVE)
WHERE cve.cvssV31BaseSeverity = 'CRITICAL'

// SLOWER: Property filter on all nodes
MATCH (n)
WHERE n.super_label = 'Vulnerability'
  AND n.cvssV31BaseSeverity = 'CRITICAL'
```

---

## 🎯 Common UI Patterns

### 1. Hierarchical Navigation

```javascript
// Level 1: Tier 1 domains
const domains = ['TECHNICAL', 'CONTEXTUAL', 'ASSET', 'OPERATIONAL', 'ORGANIZATIONAL'];

// Level 2: Super labels for selected domain
MATCH (n) WHERE n.tier1 = $selectedDomain
RETURN DISTINCT n.super_label, count(n) as count

// Level 3: Labels for selected super label
MATCH (n) WHERE n.super_label = $selectedSuperLabel
RETURN DISTINCT labels(n) as node_labels, count(n) as count
```

### 2. Search Across All Nodes

```cypher
// Full-text search (requires index)
MATCH (n)
WHERE toLower(n.name) CONTAINS toLower($searchTerm)
   OR toLower(n.description) CONTAINS toLower($searchTerm)
RETURN labels(n) as type, n.name, n.description
LIMIT 50
```

### 3. Time Series Chart

```cypher
// Aggregate measurements by hour
MATCH (m:Measurement)
WHERE m.timestamp > datetime() - duration('P1D')
  AND m.measurement_type = 'temperature'
RETURN datetime({
         year: m.timestamp.year,
         month: m.timestamp.month,
         day: m.timestamp.day,
         hour: m.timestamp.hour
       }) as hour,
       avg(m.value) as avg_temp,
       min(m.value) as min_temp,
       max(m.value) as max_temp
ORDER BY hour
```

### 4. Relationship Graph

```cypher
// Get subgraph for visualization
MATCH path = (cve:CVE)-[:IMPACTS]->(asset:Asset)-[:VULNERABLE_TO]->(cve2:CVE)
WHERE cve.cvssV31BaseSeverity = 'CRITICAL'
RETURN path
LIMIT 20
```

---

## 📚 Additional Resources

- **Full Documentation**: `COMPLETE_SCHEMA_REFERENCE_ENHANCED.md` (42KB, no truncation)
- **Verification Report**: `SCHEMA_VERIFICATION_REPORT.md`
- **Qdrant Storage**: Collection `frontend-package`, UUID `b9062c00-b301-5c05-a00f-5e9fc62b369c`
- **Database**: `bolt://localhost:7687` (openspg-neo4j)

---

## 🐛 Known Issues

1. **Super Label Coverage**: 19% of nodes (229,920) lack `super_label` property
   - **Workaround**: Use label-based queries for 100% coverage

2. **Technique Misclassification**: Some Technique nodes have `super_label="ThreatActor"`
   - **Workaround**: Filter by both label and super_label: `MATCH (n:Technique) OR (n) WHERE n.super_label = 'Technique'`

---

## 🎓 Learning Path

1. **Start**: Read Sections 1-2 of COMPLETE_SCHEMA_REFERENCE_ENHANCED.md (hierarchical structure, super labels)
2. **Practice**: Run the 5 essential queries above
3. **Build**: Implement one UI component (e.g., Vulnerability Dashboard)
4. **Optimize**: Review Section 8 (Performance Optimization)
5. **Advanced**: Explore multi-hop queries (Section 6.7)

---

**Questions?** Consult COMPLETE_SCHEMA_REFERENCE_ENHANCED.md or SCHEMA_VERIFICATION_REPORT.md

**Status**: ✅ PRODUCTION-READY
**Last Verified**: 2025-12-12
