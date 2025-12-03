# Neo4j Security Taxonomy Schema - AEON Cyber DT v4.0

**File**: 08_NEO4J_SECURITY_TAXONOMY_SCHEMA_v4.0_2025-12-02.md
**Created**: 2025-12-02 22:00:00 UTC
**Modified**: 2025-12-03 15:30:00 UTC
**Version**: v4.1.0
**Author**: AEON Architecture Team
**Purpose**: Complete Neo4j schema for all loaded security taxonomy data sources
**Status**: ACTIVE

---

## Overview

This document specifies the complete Neo4j schema for all security taxonomy data loaded into the AEON Cyber Digital Twin, including CVE, CWE, CAPEC, MITRE ATT&CK (Enterprise/Mobile/ICS), EMB3D, EPSS, and VulnCheck KEV data sources.

**Current Database State (2025-12-02)**:
- **Total Nodes**: 332,750
- **Total Relationships**: 11,232,122
- **EPSS Coverage**: 94.9%
- **CVSS Coverage**: 98.2%

---

## 1. Node Types (Labels)

### 1.1 CVE (Common Vulnerabilities and Exposures)

**Node Count**: 316,552

```cypher
(:CVE {
    id: "CVE-2024-12345",           // Primary key (unique)
    description: "...",              // Vulnerability description (max 2000 chars)
    published: "2024-01-15",         // Publication date
    last_modified: "2024-02-20",     // Last modification date
    epss_score: 0.00234,             // EPSS probability (0-1)
    epss_percentile: 0.45,           // EPSS percentile (0-1)
    cvss_score: 7.5,                 // CVSS base score (0-10)
    cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
    priority_tier: "Tier2",          // Tier1/Tier2/Tier3/Tier4
    created_at: timestamp(),         // Neo4j timestamp
    updated_at: timestamp()          // Last update timestamp
})
```

**Priority Tier Calculation**:
| Tier | Criteria | Action Required |
|------|----------|-----------------|
| Tier1 | EPSS > 0.5 OR CVSS >= 9.0 | Immediate remediation |
| Tier2 | EPSS > 0.1 OR CVSS >= 7.0 | Remediate within 30 days |
| Tier3 | EPSS > 0.01 OR CVSS >= 4.0 | Remediate within 90 days |
| Tier4 | All others | Monitor and schedule |

**Constraints**:
```cypher
CREATE CONSTRAINT cve_id_unique IF NOT EXISTS
FOR (c:CVE) REQUIRE c.id IS UNIQUE;
```

---

### 1.2 CWE (Common Weakness Enumeration)

**Node Count**: 969

```cypher
(:CWE {
    id: "cwe-79",                    // Primary key (lowercase, unique)
    name: "Cross-site Scripting (XSS)",
    description: "...",              // Weakness description
    abstraction: "Variant",          // Pillar/Class/Base/Variant/Compound
    status: "Stable",                // Draft/Incomplete/Stable/Deprecated
    created: timestamp()
})
```

**Abstraction Levels**:
- **Pillar**: Most abstract (e.g., CWE-664 Improper Control)
- **Class**: Abstract, language-independent
- **Base**: Abstract, technology-independent
- **Variant**: Specific to technology/language
- **Compound**: Composite of multiple weaknesses

**Constraints**:
```cypher
CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS
FOR (w:CWE) REQUIRE w.id IS UNIQUE;
```

---

### 1.3 CAPEC (Common Attack Pattern Enumeration)

**Node Count**: 615

```cypher
(:CAPEC {
    id: "capec-86",                  // Primary key (lowercase, unique)
    name: "XSS Through HTTP Headers",
    description: "...",              // Attack pattern description
    abstraction: "Standard",         // Meta/Standard/Detailed
    status: "Draft",                 // Draft/Stable/Deprecated
    likelihood: "High",              // Very Low/Low/Medium/High/Very High
    severity: "High",                // Very Low/Low/Medium/High/Very High
    created: timestamp()
})
```

**Abstraction Levels**:
- **Meta**: High-level category
- **Standard**: Specific attack pattern
- **Detailed**: Precise implementation details

**Constraints**:
```cypher
CREATE CONSTRAINT capec_id_unique IF NOT EXISTS
FOR (a:CAPEC) REQUIRE a.id IS UNIQUE;
```

---

### 1.4 Technique (MITRE ATT&CK)

**Node Count**: 1,023

```cypher
(:Technique {
    id: "T1566",                     // Primary key (unique)
    name: "Phishing",
    description: "...",              // Technique description
    domain: "enterprise-attack",     // enterprise-attack/mobile-attack/ics-attack
    is_subtechnique: false,          // True for sub-techniques like T1566.001
    detection: "...",                // Detection guidance
    platforms: ["Windows", "macOS", "Linux"],
    created: timestamp()
})
```

**Domain Distribution**:
| Domain | Count | Description |
|--------|-------|-------------|
| enterprise-attack | 625 | Enterprise IT attacks |
| mobile-attack | 186 | Mobile device attacks |
| ics-attack | 212 | Industrial Control Systems |

**Constraints**:
```cypher
CREATE CONSTRAINT technique_id_unique IF NOT EXISTS
FOR (t:Technique) REQUIRE t.id IS UNIQUE;
```

---

### 1.5 Tactic (MITRE ATT&CK)

**Node Count**: 40

```cypher
(:Tactic {
    id: "TA0001",                    // Primary key (unique)
    name: "Initial Access",
    description: "...",              // Tactic description
    shortname: "initial-access",     // URL-friendly name
    domain: "enterprise-attack",     // Domain this tactic belongs to
    created: timestamp()
})
```

**Tactic Distribution by Domain**:
| Domain | Tactics | Examples |
|--------|---------|----------|
| Enterprise | 14 | Reconnaissance, Initial Access, Execution, Persistence, ... |
| Mobile | 14 | Initial Access, Execution, Persistence, Privilege Escalation, ... |
| ICS | 12 | Initial Access, Execution, Persistence, Evasion, ... |

**Constraints**:
```cypher
CREATE CONSTRAINT tactic_id_unique IF NOT EXISTS
FOR (t:Tactic) REQUIRE t.id IS UNIQUE;
```

---

### 1.6 EMB3D Threat

**Node Count**: 81

```cypher
(:EMB3DThreat {
    id: "TID-001",                   // Primary key (unique)
    name: "Compromise Boot Process",
    description: "...",              // Threat description
    type: "vulnerability",           // EMB3D uses 'vulnerability' type in STIX
    created: timestamp()
})
```

**Important Note**: EMB3D uses `vulnerability` type in STIX 2.0, NOT `attack-pattern`.

**Constraints**:
```cypher
CREATE CONSTRAINT emb3d_threat_id_unique IF NOT EXISTS
FOR (t:EMB3DThreat) REQUIRE t.id IS UNIQUE;
```

---

### 1.7 EMB3D Mitigation

**Node Count**: 89

```cypher
(:EMB3DMitigation {
    id: "MIT-001",                   // Primary key (unique)
    name: "Secure Boot Implementation",
    description: "...",              // Mitigation description
    created: timestamp()
})
```

**Constraints**:
```cypher
CREATE CONSTRAINT emb3d_mitigation_id_unique IF NOT EXISTS
FOR (m:EMB3DMitigation) REQUIRE m.id IS UNIQUE;
```

---

### 1.8 EMB3D Property

**Node Count**: 118

```cypher
(:EMB3DProperty {
    id: "PROP-001",                  // Primary key (unique)
    name: "Boot Process Security",
    description: "...",              // Property description
    created: timestamp()
})
```

**Constraints**:
```cypher
CREATE CONSTRAINT emb3d_property_id_unique IF NOT EXISTS
FOR (p:EMB3DProperty) REQUIRE p.id IS UNIQUE;
```

---

### 1.9 KEV (Known Exploited Vulnerabilities)

**Node Count**: 10 (from VulnCheck KEV)

```cypher
(:KEV {
    id: "CVE-2024-XXXXX",            // CVE ID (unique)
    name: "...",
    vendor: "...",
    product: "...",
    date_added: "2024-01-15",        // Date added to KEV
    due_date: "2024-02-15",          // Remediation deadline
    ransomware_campaign: "Yes",       // Known ransomware use
    created: timestamp()
})
```

**Constraints**:
```cypher
CREATE CONSTRAINT kev_id_unique IF NOT EXISTS
FOR (k:KEV) REQUIRE k.id IS UNIQUE;
```

---

### 1.10 Entity (NER11 Extracted Entities)

**Node Count**: ~140,000+ (from document ingestion)

```cypher
(:Entity {
    text: "APT29",                   // Entity text
    label: "THREAT_ACTOR",           // NER11 entity type
    source_file: "report.md",        // Source document
    created_at: timestamp(),
    last_seen: timestamp()
})
```

**Note**: Entity data is also stored in Qdrant with enhanced temporal tracking. See Section 7.1 for Qdrant schema details.

**NER11 Entity Types**:
| Label | Description | Examples |
|-------|-------------|----------|
| THREAT_ACTOR | Threat actors/groups | APT29, Lazarus Group, FIN7 |
| MALWARE | Malware families | Cobalt Strike, Emotet, TrickBot |
| CVE | Vulnerability IDs | CVE-2024-12345 |
| TECHNIQUE | Attack techniques | Phishing, SQL Injection |
| TOOL | Software tools | Mimikatz, BloodHound |
| INDUSTRY | Industry sectors | Healthcare, Energy |
| COUNTRY | Geographic locations | Russia, China, USA |
| CAMPAIGN | Attack campaigns | SolarWinds, NotPetya |

---

## 2. Relationship Types

### 2.1 CVE Relationships

```cypher
// CVE to CWE
(c:CVE)-[:HAS_WEAKNESS {created_at: timestamp()}]->(w:CWE)

// CVE to KEV
(c:CVE)-[:IN_KEV {date_added: "2024-01-15"}]->(k:KEV)
```

**Relationship Count**: ~890,000 CVE→CWE relationships

---

### 2.2 CAPEC Relationships

```cypher
// CAPEC to CWE (exploits weakness)
(a:CAPEC)-[:EXPLOITS_WEAKNESS]->(w:CWE)

// CAPEC to Technique (maps to ATT&CK)
(a:CAPEC)-[:MAPS_TO_TECHNIQUE]->(t:Technique)

// CAPEC hierarchy
(child:CAPEC)-[:CHILD_OF]->(parent:CAPEC)
```

**Relationship Count**: ~2,400 CAPEC relationships

---

### 2.3 CWE Relationships

```cypher
// CWE hierarchy
(child:CWE)-[:CHILD_OF]->(parent:CWE)

// CWE abstraction chain
(specific:CWE)-[:ABSTRACTION_OF]->(general:CWE)
```

**Relationship Count**: ~1,200 CWE relationships

---

### 2.4 MITRE ATT&CK Relationships

```cypher
// Technique to Tactic
(t:Technique)-[:BELONGS_TO]->(tac:Tactic)

// Sub-technique to parent
(sub:Technique)-[:SUBTECHNIQUE_OF]->(parent:Technique)

// Technique to Mitigation
(t:Technique)-[:MITIGATED_BY]->(m:Mitigation)
```

**Relationship Count**: 2,945 Technique→Tactic relationships

---

### 2.5 EMB3D Relationships

```cypher
// Threat to Mitigation
(t:EMB3DThreat)-[:MITIGATED_BY]->(m:EMB3DMitigation)

// Threat to Property
(t:EMB3DThreat)-[:AFFECTS_PROPERTY]->(p:EMB3DProperty)

// Generic EMB3D relationship
(s)-[:EMB3D_REL {type: "RELATED_TO"}]->(t)
```

---

### 2.6 Entity Relationships

```cypher
// Entity to Entity (extracted from documents)
(e1:Entity)-[:RELATED_TO {source: "document.md", weight: 0.85}]->(e2:Entity)

// Entity to CVE (linked)
(e:Entity)-[:MENTIONS]->(c:CVE)

// Entity to Technique
(e:Entity)-[:USES_TECHNIQUE]->(t:Technique)
```

---

## 3. Index Configuration

### Performance Indexes

```cypher
// Full-text search indexes
CREATE FULLTEXT INDEX cve_search IF NOT EXISTS
FOR (c:CVE) ON EACH [c.id, c.description];

CREATE FULLTEXT INDEX technique_search IF NOT EXISTS
FOR (t:Technique) ON EACH [t.id, t.name, t.description];

CREATE FULLTEXT INDEX entity_search IF NOT EXISTS
FOR (e:Entity) ON EACH [e.text, e.label];

// Composite indexes for common queries
CREATE INDEX cve_epss_cvss IF NOT EXISTS
FOR (c:CVE) ON (c.epss_score, c.cvss_score);

CREATE INDEX cve_tier IF NOT EXISTS
FOR (c:CVE) ON (c.priority_tier);

CREATE INDEX technique_domain IF NOT EXISTS
FOR (t:Technique) ON (t.domain);

CREATE INDEX entity_label IF NOT EXISTS
FOR (e:Entity) ON (e.label);
```

---

## 4. Query Patterns for Frontend

### 4.1 High-Priority CVEs

```cypher
// Get top 20 CVEs by priority
MATCH (c:CVE)
WHERE c.priority_tier IN ['Tier1', 'Tier2']
RETURN c.id, c.description, c.epss_score, c.cvss_score, c.priority_tier
ORDER BY c.epss_score DESC
LIMIT 20
```

### 4.2 CVE Impact Analysis

```cypher
// Get CVE with related CWEs, CAPECs, and Techniques
MATCH (c:CVE {id: $cveId})-[:HAS_WEAKNESS]->(w:CWE)
OPTIONAL MATCH (a:CAPEC)-[:EXPLOITS_WEAKNESS]->(w)
OPTIONAL MATCH (a)-[:MAPS_TO_TECHNIQUE]->(t:Technique)
RETURN c, w, a, t
```

### 4.3 Technique by Tactic Matrix

```cypher
// Get ATT&CK matrix view
MATCH (t:Technique)-[:BELONGS_TO]->(tac:Tactic)
WHERE t.domain = 'enterprise-attack'
RETURN tac.name as tactic, collect(t.name) as techniques
ORDER BY tac.id
```

### 4.4 CWE Weakness Chain

```cypher
// Get CWE hierarchy (ancestors)
MATCH path = (w:CWE {id: $cweId})-[:CHILD_OF*1..5]->(ancestor:CWE)
RETURN path
```

### 4.5 Entity Network Analysis

```cypher
// Get entity relationship network
MATCH (e:Entity)-[r:RELATED_TO]->(related:Entity)
WHERE e.label = 'THREAT_ACTOR'
RETURN e, r, related
LIMIT 100
```

---

## 5. Statistics Queries

### Node Counts by Label

```cypher
CALL db.labels() YIELD label
CALL apoc.cypher.run('MATCH (n:`' + label + '`) RETURN count(n) as count', {}) YIELD value
RETURN label, value.count as count
ORDER BY count DESC
```

### Relationship Counts

```cypher
CALL db.relationshipTypes() YIELD relationshipType
CALL apoc.cypher.run('MATCH ()-[r:`' + relationshipType + '`]->() RETURN count(r) as count', {}) YIELD value
RETURN relationshipType, value.count as count
ORDER BY count DESC
```

### EPSS Coverage

```cypher
MATCH (c:CVE)
WITH count(c) as total
MATCH (c:CVE) WHERE c.epss_score > 0
WITH total, count(c) as with_epss
RETURN total, with_epss,
       round(100.0 * with_epss / total, 1) as coverage_pct
```

---

## 6. Data Source Mapping

| Source | Node Type | Count | Update Frequency |
|--------|-----------|-------|------------------|
| NVD | CVE | 316,552 | Weekly |
| FIRST.org | CVE.epss_* | N/A | Daily |
| MITRE CWE | CWE | 969 | Annual |
| MITRE CAPEC | CAPEC | 615 | Annual |
| MITRE ATT&CK | Technique, Tactic | 1,063 | Quarterly |
| MITRE EMB3D | EMB3DThreat, EMB3DMitigation, EMB3DProperty | 288 | As released |
| VulnCheck | KEV | 10 | Weekly |
| NER11 API | Entity | 140,000+ | Continuous |

---

## 7. Qdrant Vector Database Integration

### 7.1 Qdrant Entity Schema

**Collection**: `ner11_entities_hierarchical`
**Vector Dimension**: 384 (all-MiniLM-L6-v2)
**Distance Metric**: Cosine

```json
{
  "id": "hash(text_label_source) % 2^63",
  "vector": [0.123, -0.456, ...],  // 384-dimensional embedding
  "payload": {
    // Core fields
    "entity": "APT29",
    "ner_label": "THREAT_ACTOR",
    "fine_grained_type": "Nation-State APT",
    "specific_instance": "Russian SVR",
    "hierarchy_path": "THREAT_ACTOR/Nation-State APT/Russian SVR",
    "hierarchy_level": 3,
    "confidence": 0.95,
    "classification_confidence": 0.88,
    "doc_id": "threat_report_2024.md",

    // Enhanced temporal tracking (v1.1, 2025-12-03)
    "first_seen": "2025-11-15T10:30:00Z",  // Original discovery - PRESERVED on re-runs
    "last_seen": "2025-12-03T14:45:00Z",   // Most recent observation - ALWAYS updated
    "seen_count": 15,                       // Observation count - INCREMENTED on re-runs
    "created_at": "2025-11-15T10:30:00Z"   // Backward compatibility
  }
}
```

### 7.2 Temporal Tracking Benefits

| Capability | Implementation | Use Case |
|------------|----------------|----------|
| **Idempotent Re-ingestion** | `MERGE` + temporal fields | Safe to re-run ingestion without data loss |
| **Entity Popularity** | `seen_count` field | Identify frequently referenced entities |
| **Freshness Detection** | `last_seen` timestamp | Find stale entities for review |
| **Discovery History** | `first_seen` preservation | Track when entities were first observed |

### 7.3 Deduplication Strategy

**Point ID Generation**:
```python
point_id = hash(f"{text}_{label}_{source_file}") % (2**63 - 1)
```

This ensures:
- Same entity from same source always has same ID
- Re-ingestion updates existing points (upsert)
- Different sources for same entity create separate points

### 7.4 Example Queries

```python
# Find most frequently seen entities
from qdrant_client import QdrantClient
client = QdrantClient(host="localhost", port=6333)

# Scroll with filter for high seen_count
results = client.scroll(
    collection_name="ner11_entities_hierarchical",
    scroll_filter=Filter(must=[
        FieldCondition(key="seen_count", range=Range(gte=10))
    ]),
    limit=100
)

# Find entities not seen in last 30 days
from datetime import datetime, timedelta
cutoff = (datetime.utcnow() - timedelta(days=30)).isoformat()
stale = client.scroll(
    collection_name="ner11_entities_hierarchical",
    scroll_filter=Filter(must=[
        FieldCondition(key="last_seen", range=Range(lt=cutoff))
    ]),
    limit=100
)
```

---

## 8. Version History

| Version | Date | Changes |
|---------|------|---------|
| v4.0.0 | 2025-12-02 | Added EMB3D, KEV, comprehensive taxonomy schema |
| v3.0.0 | 2025-11-19 | Initial schema with CVE, CWE, CAPEC, ATT&CK |

---

## References

- [NVD API Documentation](https://nvd.nist.gov/developers/vulnerabilities)
- [FIRST.org EPSS API](https://api.first.org/data/v1/epss)
- [MITRE ATT&CK STIX Data](https://github.com/mitre-attack/attack-stix-data)
- [MITRE CWE Downloads](https://cwe.mitre.org/data/downloads.html)
- [MITRE CAPEC Downloads](https://capec.mitre.org/data/downloads.html)
- [MITRE EMB3D](https://github.com/mitre/emb3d)
