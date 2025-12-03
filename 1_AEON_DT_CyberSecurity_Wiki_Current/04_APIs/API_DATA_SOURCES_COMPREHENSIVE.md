# AEON Cyber Digital Twin - Comprehensive Data Sources API Reference

**Version**: 2.0.0
**Last Updated**: 2025-12-02
**Status**: Production Ready

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Data Source Overview](#2-data-source-overview)
3. [CVE - Common Vulnerabilities and Exposures](#3-cve---common-vulnerabilities-and-exposures)
4. [CWE - Common Weakness Enumeration](#4-cwe---common-weakness-enumeration)
5. [CAPEC - Common Attack Pattern Enumeration](#5-capec---common-attack-pattern-enumeration)
6. [MITRE ATT&CK Framework](#6-mitre-attck-framework)
7. [EMB3D - Embedded Device Threat Model](#7-emb3d---embedded-device-threat-model)
8. [EPSS - Exploit Prediction Scoring System](#8-epss---exploit-prediction-scoring-system)
9. [VulnCheck KEV](#9-vulncheck-kev)
10. [Neo4j Entity Labels and Relationships](#10-neo4j-entity-labels-and-relationships)
11. [API Endpoints for Updates](#11-api-endpoints-for-updates)
12. [Update Procedures](#12-update-procedures)
13. [Query Patterns for Frontend](#13-query-patterns-for-frontend)

---

## 1. Executive Summary

The AEON Cyber Digital Twin integrates **9 major cybersecurity data sources** into a unified Neo4j graph database, providing comprehensive threat intelligence, vulnerability data, and attack pattern analysis.

### Current Database Statistics (2025-12-02)

| Node Type | Count | Source |
|-----------|-------|--------|
| CVE | 316,552 | NVD API |
| CWE | 969 | MITRE CWE |
| CAPEC | 615 | MITRE CAPEC |
| Technique | 1,023 | MITRE ATT&CK |
| Tactic | 40 | MITRE ATT&CK |
| EMB3DThreat | 81 | EMB3D STIX |
| EMB3DMitigation | 89 | EMB3D STIX |
| EMB3DProperty | 118 | EMB3D STIX |
| KEV | 10 | VulnCheck |
| Entity | 13,135 | NER11 Extraction |
| Document | 118 | Wiki Ingestion |
| **TOTAL** | **332,750** | |

### Relationship Statistics

- **Total Relationships**: 11,232,122
- **Technique→Tactic Links**: 2,945
- **EPSS Coverage**: 94.9% (300,461 / 316,552 CVEs)

---

## 2. Data Source Overview

### Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL DATA SOURCES                         │
├─────────────────────────────────────────────────────────────────┤
│  NVD API          FIRST.org API      MITRE GitHub               │
│  (CVE Data)       (EPSS Scores)      (ATT&CK, CAPEC, CWE)       │
│                                                                  │
│  EMB3D STIX       VulnCheck API                                 │
│  (Embedded Threats) (KEV Data)                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INGESTION PIPELINE                            │
├─────────────────────────────────────────────────────────────────┤
│  scripts/load_comprehensive_taxonomy.py                         │
│  scripts/update_cve_taxonomy.py                                 │
│  NER11 API (localhost:8000)                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA STORAGE LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  Neo4j (bolt://localhost:7687)                                  │
│  Qdrant (localhost:6333)                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. CVE - Common Vulnerabilities and Exposures

### What It Is
CVE (Common Vulnerabilities and Exposures) is a dictionary of publicly known cybersecurity vulnerabilities. Each CVE entry has a unique ID (CVE-YYYY-NNNNN) and describes a specific vulnerability.

### Data Source
- **Primary API**: NVD (National Vulnerability Database)
- **Endpoint**: `https://services.nvd.nist.gov/rest/json/cves/2.0`
- **Update Frequency**: Daily (new CVEs), Weekly (score updates)
- **Current Count**: 316,552 CVEs

### Neo4j Schema

```cypher
(:CVE {
  id: "CVE-2024-12345",           // Primary identifier
  description: "...",             // Vulnerability description (max 2000 chars)
  published: "2024-01-15T...",    // Publication date
  last_modified: "2024-02-01T...", // Last modification date
  epss_score: 0.85,               // EPSS probability (0.0-1.0)
  epss_percentile: 0.97,          // EPSS percentile
  cvss_score: 9.8,                // CVSS base score (0.0-10.0)
  cvss_vector: "CVSS:3.1/AV:N/AC:L/...",  // CVSS vector string
  priority_tier: "Tier1",         // Priority: Tier1/Tier2/Tier3/Tier4
  created_at: timestamp(),
  updated_at: timestamp()
})
```

### Priority Tier Calculation
```
Tier1 (Critical): EPSS > 0.5 OR CVSS >= 9.0
Tier2 (High):     EPSS > 0.1 OR CVSS >= 7.0
Tier3 (Medium):   EPSS > 0.01 OR CVSS >= 4.0
Tier4 (Low):      Everything else
```

### Relationships
```cypher
(CVE)-[:HAS_WEAKNESS]->(CWE)         // CVE exploits specific weaknesses
(CVE)-[:IN_KEV]->(KEV)               // CVE is in Known Exploited list
(CVE)-[:AFFECTS]->(Equipment)        // CVE affects specific equipment
(CVE)-[:EXPLOITED_BY]->(Technique)   // CVE exploited by ATT&CK technique
```

### Query Examples

```cypher
// Get critical CVEs (Tier1)
MATCH (c:CVE {priority_tier: "Tier1"})
RETURN c.id, c.description, c.cvss_score, c.epss_score
ORDER BY c.epss_score DESC
LIMIT 100

// Get CVEs with high EPSS that affect specific CWE
MATCH (c:CVE)-[:HAS_WEAKNESS]->(w:CWE {id: "CWE-79"})
WHERE c.epss_score > 0.5
RETURN c.id, c.description, c.epss_score
```

### Update API Call (Python)
```python
import requests

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Get CVEs from last 7 days
params = {
    "pubStartDate": "2025-11-25T00:00:00.000",
    "pubEndDate": "2025-12-02T23:59:59.999",
    "resultsPerPage": 2000
}
response = requests.get(NVD_API, params=params, timeout=60)
cves = response.json().get("vulnerabilities", [])
```

---

## 4. CWE - Common Weakness Enumeration

### What It Is
CWE is a community-developed list of common software and hardware weakness types. CWEs describe categories of vulnerabilities (e.g., CWE-79 is Cross-Site Scripting).

### Data Source
- **Source File**: `cwec_v4.18.xml`
- **Download**: https://cwe.mitre.org/data/downloads.html
- **Format**: XML with CWE namespace
- **Current Count**: 969 weaknesses

### Neo4j Schema

```cypher
(:CWE {
  id: "cwe-79",                    // Lowercase ID
  name: "Improper Neutralization of Input During Web Page Generation",
  description: "...",              // Full description
  abstraction: "Base",             // Pillar/Class/Base/Variant
  status: "Draft",                 // Draft/Stable/Incomplete/Deprecated
  created: timestamp()
})
```

### Relationships
```cypher
(CWE)-[:CHILD_OF]->(CWE)           // Hierarchy relationship
(CVE)-[:HAS_WEAKNESS]->(CWE)        // CVEs exploit this weakness
(CAPEC)-[:EXPLOITS]->(CWE)          // Attack patterns exploit weakness
(Technique)-[:EXPLOITS]->(CWE)      // ATT&CK techniques exploit weakness
```

### Query Examples

```cypher
// Get top CWEs by CVE count
MATCH (c:CVE)-[:HAS_WEAKNESS]->(w:CWE)
RETURN w.id, w.name, count(c) as cve_count
ORDER BY cve_count DESC
LIMIT 20

// Get CWE hierarchy
MATCH path = (child:CWE)-[:CHILD_OF*1..3]->(parent:CWE)
WHERE child.id = "cwe-79"
RETURN path
```

### XML Parsing Code
```python
import xml.etree.ElementTree as ET

CWE_NS = {'cwe': 'http://cwe.mitre.org/cwe-7'}
tree = ET.parse('cwec_v4.18.xml')
root = tree.getroot()

for weakness in root.findall('.//cwe:Weakness', CWE_NS):
    cwe_id = f"cwe-{weakness.get('ID')}"
    name = weakness.get('Name')
    abstraction = weakness.get('Abstraction')
```

---

## 5. CAPEC - Common Attack Pattern Enumeration

### What It Is
CAPEC is a comprehensive dictionary of known attack patterns used by adversaries to exploit weaknesses in applications and systems.

### Data Source
- **Source File**: `capec_v3.9.xml`
- **Download**: https://capec.mitre.org/data/downloads.html
- **Format**: XML with CAPEC namespace
- **Current Count**: 615 attack patterns

### Neo4j Schema

```cypher
(:CAPEC {
  id: "capec-1",                   // CAPEC ID
  name: "Accessing Functionality Not Properly Constrained by ACLs",
  description: "...",
  severity: "High",                // Very Low/Low/Medium/High/Very High
  likelihood: "Medium",            // Very Low/Low/Medium/High/Very High
  created: timestamp()
})
```

### Relationships
```cypher
(CAPEC)-[:CHILD_OF]->(CAPEC)        // Attack pattern hierarchy
(CAPEC)-[:EXPLOITS]->(CWE)          // Exploits specific weaknesses
(CAPEC)-[:RELATED_TO]->(Technique)  // Related ATT&CK techniques
```

### Query Examples

```cypher
// Get high-severity attack patterns
MATCH (a:CAPEC)
WHERE a.severity = "High"
RETURN a.id, a.name, a.description
ORDER BY a.id

// Get attack patterns that exploit specific CWE
MATCH (a:CAPEC)-[:EXPLOITS]->(w:CWE {id: "cwe-89"})
RETURN a.id, a.name
```

---

## 6. MITRE ATT&CK Framework

### What It Is
ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge) is a knowledge base of adversary behaviors based on real-world observations. It covers:
- **Enterprise**: Windows, macOS, Linux, Cloud, Network, Containers
- **Mobile**: Android, iOS
- **ICS**: Industrial Control Systems

### Data Sources
- **Enterprise**: `enterprise-attack.json` (STIX 2.0)
- **Mobile**: `mobile-attack.json` (STIX 2.0)
- **ICS**: `ics-attack.json` (STIX 2.0)
- **Download**: https://github.com/mitre-attack/attack-stix-data

### Neo4j Schema - Techniques

```cypher
(:Technique {
  id: "T1059",                      // ATT&CK ID
  stix_id: "attack-pattern--...",   // STIX identifier
  name: "Command and Scripting Interpreter",
  description: "...",
  kill_chain_phases: ["execution"], // Tactic phases
  platform: ["Windows", "Linux", "macOS"],
  detection: "...",                 // Detection guidance
  domain: "enterprise-attack",      // enterprise/mobile/ics
  created: timestamp()
})
```

### Neo4j Schema - Tactics

```cypher
(:Tactic {
  id: "TA0002",                     // Tactic ID
  stix_id: "x-mitre-tactic--...",   // STIX identifier
  name: "Execution",
  description: "...",
  shortname: "execution",           // URL-safe name
  domain: "enterprise-attack",
  created: timestamp()
})
```

### Relationships
```cypher
(Technique)-[:BELONGS_TO]->(Tactic)     // Technique implements tactic
(Technique)-[:SUBTECHNIQUE_OF]->(Technique) // Sub-technique hierarchy
(Technique)-[:USES]->(Software)         // Technique uses software
(Technique)-[:EXPLOITS]->(CWE)          // Exploits weaknesses
(Group)-[:USES]->(Technique)            // Threat groups use techniques
```

### Tactic Distribution
| Domain | Tactic Count |
|--------|--------------|
| Enterprise | 14 |
| Mobile | 14 |
| ICS | 12 |
| **Total** | **40** |

### Query Examples

```cypher
// Get all techniques for a tactic
MATCH (tech:Technique)-[:BELONGS_TO]->(tac:Tactic {name: "Execution"})
RETURN tech.id, tech.name, tech.description

// Get technique to tactic mapping
MATCH (tech:Technique)-[:BELONGS_TO]->(tac:Tactic)
RETURN tech.id, tech.name, collect(tac.name) as tactics
```

---

## 7. EMB3D - Embedded Device Threat Model

### What It Is
EMB3D is a threat model specifically for embedded devices, identifying threats, mitigations, and device properties relevant to IoT/OT security.

### Data Source
- **Source File**: `emb3d-stix-2.0.1.json`
- **Format**: STIX 2.0.1 (JSON)
- **Download**: https://emb3d.mitre.org/

### Key Discovery
**EMB3D uses `vulnerability` type, NOT `attack-pattern`** for threats. This is different from ATT&CK which uses `attack-pattern`.

### Neo4j Schema - EMB3D Threats

```cypher
(:EMB3DThreat {
  id: "EMB3D-001",                  // EMB3D threat ID
  name: "Firmware Extraction",
  description: "...",
  type: "vulnerability",            // STIX type
  created: timestamp()
})
```

### Neo4j Schema - EMB3D Mitigations

```cypher
(:EMB3DMitigation {
  id: "M-001",                      // Mitigation ID
  name: "Secure Boot",
  description: "...",
  created: timestamp()
})
```

### Neo4j Schema - EMB3D Properties

```cypher
(:EMB3DProperty {
  id: "P-001",                      // Property ID
  name: "Debug Interface Exposed",
  description: "...",
  created: timestamp()
})
```

### Object Counts
| Type | Count |
|------|-------|
| EMB3DThreat (vulnerability) | 81 |
| EMB3DMitigation (course-of-action) | 89 |
| EMB3DProperty (x-mitre-emb3d-property) | 118 |
| Relationships | 343 |

### Relationships
```cypher
(EMB3DThreat)-[:MITIGATED_BY]->(EMB3DMitigation)
(EMB3DThreat)-[:EXPLOITS]->(EMB3DProperty)
(EMB3DProperty)-[:ENABLES]->(EMB3DThreat)
```

### Query Examples

```cypher
// Get EMB3D threats with mitigations
MATCH (t:EMB3DThreat)-[:MITIGATED_BY]->(m:EMB3DMitigation)
RETURN t.name, collect(m.name) as mitigations

// Get properties that enable threats
MATCH (p:EMB3DProperty)-[:ENABLES]->(t:EMB3DThreat)
RETURN p.name, collect(t.name) as enabled_threats
```

---

## 8. EPSS - Exploit Prediction Scoring System

### What It Is
EPSS provides a probability score (0.0-1.0) indicating the likelihood that a CVE will be exploited in the wild within the next 30 days.

### Data Source
- **Primary API**: FIRST.org
- **Endpoint**: `https://api.first.org/data/v1/epss`
- **Bulk File**: `epss_scores-YYYY-MM-DD.csv.gz`
- **Update Frequency**: Daily
- **Coverage**: 94.9% of CVEs

### API Usage

```python
import requests

EPSS_API = "https://api.first.org/data/v1/epss"

# Get EPSS for specific CVEs
cve_list = ["CVE-2024-12345", "CVE-2024-12346"]
response = requests.get(f"{EPSS_API}?cve={','.join(cve_list)}")
data = response.json()

for item in data.get("data", []):
    cve_id = item.get("cve")
    epss_score = float(item.get("epss", 0))
    percentile = float(item.get("percentile", 0))
```

### Bulk CSV Format
```csv
cve,epss,percentile
CVE-2024-12345,0.85234,0.97654
CVE-2024-12346,0.00123,0.12345
```

### Neo4j Integration
EPSS scores are stored directly on CVE nodes:
```cypher
MATCH (c:CVE {id: "CVE-2024-12345"})
SET c.epss_score = 0.85234,
    c.epss_percentile = 0.97654
```

### Query Examples

```cypher
// Get CVEs most likely to be exploited
MATCH (c:CVE)
WHERE c.epss_score > 0.5
RETURN c.id, c.description, c.epss_score, c.cvss_score
ORDER BY c.epss_score DESC
LIMIT 50

// Get EPSS statistics
MATCH (c:CVE)
WHERE c.epss_score > 0
RETURN
  count(c) as total_with_epss,
  avg(c.epss_score) as avg_epss,
  max(c.epss_score) as max_epss,
  percentileCont(c.epss_score, 0.9) as p90_epss
```

---

## 9. VulnCheck KEV

### What It Is
VulnCheck KEV (Known Exploited Vulnerabilities) is an enhanced list of vulnerabilities known to be actively exploited, similar to CISA KEV but with additional context.

### Data Source
- **Source File**: `vulncheck-kev.json`
- **API**: https://vulncheck.com/api
- **Current Count**: 10 entries (sample)

### Neo4j Schema

```cypher
(:KEV {
  id: "VCK-001",                    // VulnCheck ID
  cve_id: "CVE-2024-12345",         // Associated CVE
  name: "...",
  description: "...",
  date_added: "2024-01-15",
  due_date: "2024-01-22",           // Remediation deadline
  vendor: "Microsoft",
  product: "Windows",
  created: timestamp()
})
```

### Relationships
```cypher
(CVE)-[:IN_KEV]->(KEV)              // CVE is in KEV list
(KEV)-[:AFFECTS]->(Vendor)          // KEV affects vendor
```

### Query Examples

```cypher
// Get all KEV entries with CVE details
MATCH (c:CVE)-[:IN_KEV]->(k:KEV)
RETURN c.id, c.description, k.date_added, k.due_date
ORDER BY k.date_added DESC

// Find CVEs that are both high EPSS and in KEV
MATCH (c:CVE)-[:IN_KEV]->(k:KEV)
WHERE c.epss_score > 0.5
RETURN c.id, c.epss_score, c.cvss_score, k.due_date
```

---

## 10. Neo4j Entity Labels and Relationships

### Complete Label Reference

| Label | Count | Description |
|-------|-------|-------------|
| CVE | 316,552 | Vulnerability entries |
| CWE | 969 | Weakness categories |
| CAPEC | 615 | Attack patterns |
| Technique | 1,023 | ATT&CK techniques |
| Tactic | 40 | ATT&CK tactics |
| EMB3DThreat | 81 | Embedded device threats |
| EMB3DMitigation | 89 | EMB3D mitigations |
| EMB3DProperty | 118 | EMB3D device properties |
| KEV | 10 | Known exploited vulns |
| Entity | 13,135 | NER-extracted entities |
| Document | 118 | Ingested documents |

### Complete Relationship Reference

| Relationship | Source | Target | Description |
|--------------|--------|--------|-------------|
| HAS_WEAKNESS | CVE | CWE | CVE exploits weakness |
| CHILD_OF | CWE | CWE | Weakness hierarchy |
| CHILD_OF | CAPEC | CAPEC | Attack pattern hierarchy |
| EXPLOITS | CAPEC | CWE | Attack exploits weakness |
| BELONGS_TO | Technique | Tactic | Technique in tactic |
| SUBTECHNIQUE_OF | Technique | Technique | Sub-technique |
| USES | Technique | Software | Technique uses tool |
| MITIGATED_BY | EMB3DThreat | EMB3DMitigation | Threat mitigation |
| IN_KEV | CVE | KEV | CVE in KEV list |
| EXTRACTED_FROM | Entity | Document | Entity source |
| MENTIONS | Document | CVE/CWE/etc | Document references |

---

## 11. API Endpoints for Updates

### NVD API (CVE Data)

```
Base URL: https://services.nvd.nist.gov/rest/json/cves/2.0

Parameters:
- pubStartDate: Start date (ISO 8601)
- pubEndDate: End date (ISO 8601)
- cveId: Specific CVE ID
- resultsPerPage: Max 2000
- startIndex: Pagination offset

Rate Limit: 5 requests / 30 seconds (free tier)
API Key: Optional (higher limits with key)
```

### FIRST.org EPSS API

```
Base URL: https://api.first.org/data/v1/epss

Parameters:
- cve: Comma-separated CVE IDs (max 100)
- date: Specific date for historical scores
- offset: Pagination offset
- limit: Results per page

Rate Limit: Reasonable use (no strict limit)
Authentication: None required
```

### MITRE ATT&CK Data

```
GitHub Repository: https://github.com/mitre-attack/attack-stix-data

Files:
- enterprise-attack/enterprise-attack.json
- mobile-attack/mobile-attack.json
- ics-attack/ics-attack.json

Format: STIX 2.0 JSON bundles
Update: Check releases for new versions
```

### CWE/CAPEC Downloads

```
CWE: https://cwe.mitre.org/data/downloads.html
  - cwec_v{version}.xml (Full XML)

CAPEC: https://capec.mitre.org/data/downloads.html
  - capec_v{version}.xml (Full XML)

Format: Custom XML with namespaces
Update: Check quarterly releases
```

---

## 12. Update Procedures

### Weekly CVE Update

```bash
# Run the CVE taxonomy update script
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
python3 scripts/update_cve_taxonomy.py --days 7

# Or for specific CVE
python3 scripts/update_cve_taxonomy.py --cve CVE-2024-12345

# Cron setup (every Sunday at midnight)
0 0 * * 0 cd /path/to/project && python3 scripts/update_cve_taxonomy.py --days 7 >> logs/cve_update.log 2>&1
```

### Full Taxonomy Reload

```bash
# Comprehensive reload of all data sources
python3 scripts/load_comprehensive_taxonomy.py --all

# Individual sources
python3 scripts/load_comprehensive_taxonomy.py --source cve
python3 scripts/load_comprehensive_taxonomy.py --source cwe
python3 scripts/load_comprehensive_taxonomy.py --source capec
python3 scripts/load_comprehensive_taxonomy.py --source attack
python3 scripts/load_comprehensive_taxonomy.py --source emb3d
python3 scripts/load_comprehensive_taxonomy.py --source epss
python3 scripts/load_comprehensive_taxonomy.py --source kev
```

### EPSS Daily Update

```python
import requests
import gzip
from datetime import datetime

# Download daily EPSS file
date_str = datetime.now().strftime("%Y-%m-%d")
url = f"https://epss.cyentia.com/epss_scores-{date_str}.csv.gz"

response = requests.get(url)
with gzip.open('epss_scores.csv.gz', 'wb') as f:
    f.write(response.content)

# Parse and update Neo4j
import csv
with gzip.open('epss_scores.csv.gz', 'rt') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cve_id = row['cve']
        epss = float(row['epss'])
        percentile = float(row['percentile'])
        # Update Neo4j...
```

---

## 13. Query Patterns for Frontend

### Dashboard Queries

```cypher
// Get vulnerability overview stats
MATCH (c:CVE)
WITH count(c) as total,
     sum(CASE WHEN c.priority_tier = 'Tier1' THEN 1 ELSE 0 END) as critical,
     sum(CASE WHEN c.priority_tier = 'Tier2' THEN 1 ELSE 0 END) as high,
     sum(CASE WHEN c.epss_score > 0 THEN 1 ELSE 0 END) as with_epss
RETURN total, critical, high, with_epss

// Get technique coverage by tactic
MATCH (tech:Technique)-[:BELONGS_TO]->(tac:Tactic)
RETURN tac.name, count(tech) as technique_count
ORDER BY technique_count DESC
```

### Search Queries

```cypher
// Full-text CVE search
MATCH (c:CVE)
WHERE c.description CONTAINS $searchTerm
RETURN c.id, c.description, c.cvss_score, c.epss_score
LIMIT 50

// Search across all entity types
CALL {
  MATCH (c:CVE) WHERE c.description CONTAINS $term RETURN c.id as id, 'CVE' as type, c.description as text
  UNION
  MATCH (w:CWE) WHERE w.name CONTAINS $term RETURN w.id as id, 'CWE' as type, w.name as text
  UNION
  MATCH (a:CAPEC) WHERE a.name CONTAINS $term RETURN a.id as id, 'CAPEC' as type, a.name as text
  UNION
  MATCH (t:Technique) WHERE t.name CONTAINS $term RETURN t.id as id, 'Technique' as type, t.name as text
}
RETURN id, type, text
LIMIT 100
```

### Attack Path Queries

```cypher
// Get attack path from CWE to CVE
MATCH path = (cwe:CWE)<-[:EXPLOITS]-(capec:CAPEC)-[:RELATED_TO]->(tech:Technique)-[:BELONGS_TO]->(tac:Tactic)
WHERE cwe.id = $cweId
RETURN path
LIMIT 10

// Get full CVE context
MATCH (c:CVE {id: $cveId})
OPTIONAL MATCH (c)-[:HAS_WEAKNESS]->(w:CWE)
OPTIONAL MATCH (c)-[:IN_KEV]->(k:KEV)
OPTIONAL MATCH (capec:CAPEC)-[:EXPLOITS]->(w)
OPTIONAL MATCH (tech:Technique)-[:EXPLOITS]->(w)
RETURN c, collect(DISTINCT w) as weaknesses,
       collect(DISTINCT k) as kev,
       collect(DISTINCT capec) as attack_patterns,
       collect(DISTINCT tech) as techniques
```

### Trending/Priority Queries

```cypher
// Get trending high-risk CVEs
MATCH (c:CVE)
WHERE c.epss_score > 0.3 AND c.cvss_score >= 7.0
RETURN c.id, c.description, c.epss_score, c.cvss_score, c.priority_tier
ORDER BY c.epss_score DESC
LIMIT 20

// Get most referenced CWEs
MATCH (c:CVE)-[:HAS_WEAKNESS]->(w:CWE)
WITH w, count(c) as cve_count
ORDER BY cve_count DESC
LIMIT 10
MATCH (w)<-[:EXPLOITS]-(a:CAPEC)
RETURN w.id, w.name, cve_count, count(a) as attack_patterns
```

---

## Appendix A: Connection Details

### Neo4j
- **URI**: `bolt://localhost:7687`
- **User**: `neo4j`
- **Password**: `neo4j@openspg`
- **Database**: `neo4j`

### Qdrant
- **Host**: `localhost`
- **Port**: `6333`
- **Collection**: `ner11_entities_hierarchical`

### NER11 API
- **URL**: `http://localhost:8000`
- **Health**: `GET /health`
- **NER**: `POST /ner` with `{"text": "..."}`

---

## Appendix B: Data File Locations

```
/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/
└── NVS Full CVE CAPEC CWE EMBED/
    ├── capec_latest/
    │   └── capec_v3.9.xml           # CAPEC attack patterns
    ├── cwec_v4.18.xml               # CWE weaknesses
    ├── emb3d-stix-2.0.1.json        # EMB3D threats
    ├── enterprise-attack.json        # ATT&CK Enterprise
    ├── mobile-attack.json            # ATT&CK Mobile
    ├── ics-attack.json               # ATT&CK ICS
    ├── vulncheck-kev.json           # VulnCheck KEV
    ├── epss_scores-2025-12-02.csv   # EPSS scores
    └── first_how_to/
        └── first_org_how_to.md      # FIRST API docs
```
