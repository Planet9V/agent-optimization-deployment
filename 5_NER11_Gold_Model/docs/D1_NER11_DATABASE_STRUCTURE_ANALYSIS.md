# NER11 Gold Model - Data Structure & Collection Analysis Report

**Report Date:** 2025-12-03  
**Report Generated:** 2025-12-03 (Automated Analysis)  
**Scope:** Qdrant + Neo4j Integration Analysis  

---

## Executive Summary

The NER11 hierarchical entity extraction system comprises two complementary databases:

- **Qdrant Vector Database**: 221,078 named entities with semantic embeddings (384-dim, cosine similarity)
- **Neo4j Graph Database**: 1,150,171 nodes representing complex relationships in cybersecurity/critical infrastructure domains

These systems work together to provide:
1. **Semantic Search** via Qdrant embeddings
2. **Relationship Modeling** via Neo4j's property graph
3. **Temporal Tracking** of entity mentions across documents
4. **Multi-label Entity Classification** (68 distinct entity types)

---

## QDRANT VECTOR DATABASE ANALYSIS

### Collection Metadata

| Property | Value |
|----------|-------|
| **Collection Name** | `ner11_entities_hierarchical` |
| **Total Points** | 221,078 |
| **Indexed Vectors** | 218,455 |
| **Vector Dimension** | 384 |
| **Distance Metric** | Cosine Similarity |
| **Status** | GREEN (healthy) |
| **Segments** | 4 |
| **Replication Factor** | 1 |
| **Payload Storage** | On-disk |

### Payload Schema

The Qdrant points contain 13 distinct payload fields:

```
Core Fields:
  • text (string) - The extracted entity text
  • label (string) - Entity type classification
  • ner_label (string) - Original NER label (when different from label)
  
Source Tracking:
  • source_file (string) - Document filename
  • source_dir (string) - Document directory path
  • source (string) - Legacy source field
  
Temporal Tracking:
  • created_at (datetime) - Entity first extraction timestamp
  • first_seen (datetime) - First occurrence in corpus
  • last_seen (datetime) - Most recent occurrence
  • seen_count (integer) - Total occurrences across documents
  
Metadata:
  • entity_id (string) - Unique entity identifier
  • description (string) - Entity description/context
  • tier2_type (string) - Secondary classification
```

### Temporal Tracking Coverage

| Field | Count | Coverage % |
|-------|-------|-----------|
| created_at | 221,078 | 100% |
| first_seen | 161,437 | 73.0% |
| last_seen | 161,437 | 73.0% |
| seen_count | 161,437 | 73.0% |

**Insight**: Approximately 73% of entities have temporal tracking enabled, indicating phased ingestion or filtering by frequency threshold.

### Entity Type Distribution (68 Types Total)

#### Top 15 Entity Types by Frequency

| Rank | Label | Count | % | Use Case |
|------|-------|-------|---|----------|
| 1 | CARDINAL | 26,350 | 11.9% | Numerical quantities (3, 10, 52) |
| 2 | ORG | 24,960 | 11.3% | Organizations (Vendor A, company names) |
| 3 | DATE | 23,306 | 10.5% | Temporal references (2025, January, recent) |
| 4 | PERCENT | 22,466 | 10.2% | Percentage values (52%, 75%) |
| 5 | PRODUCT | 13,558 | 6.1% | Software/products (GrimPlant, malware) |
| 6 | ATTRIBUTES | 7,145 | 3.2% | System attributes (Supply chain) |
| 7 | UNKNOWN | 6,709 | 3.0% | Unclassified entities |
| 8 | SECTORS | 5,804 | 2.6% | Industry sectors |
| 9 | GPE | 5,591 | 2.5% | Geopolitical entities (India, countries) |
| 10 | CONTROLS | 4,950 | 2.2% | Control mechanisms |
| 11 | MONEY | 4,853 | 2.2% | Monetary values |
| 12 | META | 4,151 | 1.9% | Metadata references |
| 13 | THREAT_PERCEPTION | 3,598 | 1.6% | Threat characterizations |
| 14 | HAZARD_ANALYSIS | 3,416 | 1.5% | Risk/hazard references |
| 15 | PERSON | 3,218 | 1.5% | Named individuals |

#### Complete Entity Type Breakdown

**Cybersecurity-Specific Types** (27.2% of total):
- THREAT_PERCEPTION (1.6%) - Qualitative threat assessments
- VULNERABILITY (1.3%) - Security vulnerabilities
- MALWARE (1.3%) - Malware families
- ATTACK_TECHNIQUE (1.4%) - Offensive techniques
- THREAT_ACTOR (0.5%) - Adversary groups
- APT_GROUP (0.2%) - Advanced persistent threats
- CVE (0.7%) - CVE identifiers
- CWE (0.1%) - Weakness classifications

**Quantitative Types** (32.3% of total):
- CARDINAL (11.9%) - Numbers
- PERCENT (10.2%) - Percentages
- DATE (10.5%) - Temporal expressions
- MONEY (2.2%) - Financial amounts
- QUANTITY (1.1%) - Measurements

**Infrastructure/Operational Types** (18.7%):
- SECTORS (2.6%) - Industry sectors
- DEVICE (0.8%) - Computing devices
- NETWORK (0.6%) - Network infrastructure
- PROTOCOL (1.2%) - Communication protocols
- PROCESS (1.2%) - Business processes
- SOFTWARE_COMPONENT (0.9%) - Code components

**Governance/Control Types** (7.5%):
- CONTROLS (2.2%) - Control mechanisms
- LAW (0.8%) - Legal references
- ROLES (1.1%) - Actor roles
- IEC_62443 (0.3%) - Control standards
- DETERMINISTIC_CONTROL (0.2%) - Control theory

**Organizational Types** (15.4%):
- ORG (11.3%) - Organizations
- GPE (2.5%) - Geographic/political entities
- PERSON (1.5%) - Named individuals

### Document Source Distribution

**Top 20 Source Files:**

| File | Entity Count | Domain |
|------|-------------|--------|
| OCTOBER_2025_CYBERSECURITY_THREAT_LANDSCAPE.md | 895 | Threat landscape |
| APT29 Midnight Blizzard... .md | 577 | Threat analysis |
| cybersecurity_magazine_multi_vector_menace.md | 516 | Threat analysis |
| BAUXITE, GRAPHITE, VOLTZITE Analysis.md | 399 | Threat group analysis |
| Energy Sector Threat Modeling.md | 398 | Critical infrastructure |
| Threat Model for Endeavor Energy.md | 398 | Risk assessment |
| petroleum-refining-downstream.md | 397 | Sector analysis |
| NCCGroup-Threat-Monitor-Report-2023.md | 389 | Threat intelligence |
| SonicWall-Cyber-Threat-Report-2023.md | 385 | Threat intelligence |
| threat_intelligence_v2_enhanced.md | 384 | Threat analysis |

**Source File Count**: 900+ unique documents  
**Primary Domain**: Cybersecurity and critical infrastructure threat analysis

---

## NEO4J GRAPH DATABASE ANALYSIS

### Graph Statistics

| Metric | Value |
|--------|-------|
| **Total Nodes** | 1,150,171 |
| **Total Relationships** | 11,732,715 |
| **Relationship Types** | 50+ distinct types |
| **Avg Relationships per Node** | 10.2 |
| **Primary Node Type** | CVE (316,552 nodes - 27.5%) |
| **Database Status** | OPERATIONAL |

### Node Type Distribution (Top 30)

| Rank | Node Type | Count | Domain |
|------|-----------|-------|--------|
| 1 | CVE | 316,552 | Vulnerability |
| 2 | Measurement + Manufacturing | 72,800 | IoT/Industrial |
| 3 | Entity | 55,569 | Generic |
| 4 | Dependency + SBOM | 30,000 | Software supply chain |
| 5 | Measurement + Defense | 25,200 | Critical infrastructure |
| 6 | SoftwareComponent + SBOM | 20,000 | Supply chain |
| 7 | Measurement + Water | 19,000 | Water systems |
| 8 | Measurement + Transportation | 18,200 | Transportation |
| 9 | Healthcare + Measurement | 18,200 | Healthcare systems |
| 10 | Measurement + IT | 18,000 | Information systems |
| 11 | Measurement + Radiation | 18,000 | Nuclear |
| 12 | Measurement + Energy | 18,000 | Power systems |
| 13 | Measurement + Communications | 15,527 | Telecom |
| 14 | HistoricalPattern | 14,985 | Analytics |
| 15 | Equipment + Dams | 14,074 | Water infrastructure |
| 16-30 | [Various sector-specific] | ~150,000+ | Multi-domain |

### Relationship Type Analysis

#### Top 20 Relationship Types

| Type | Count | Direction | Semantic Meaning |
|------|-------|-----------|-----------------|
| IMPACTS | 4,780,563 | Multi | Consequence relationships |
| VULNERABLE_TO | 3,117,735 | Vulnerability | CVE to asset mapping |
| INSTALLED_ON | 968,125 | Component-Host | Deployment topology |
| TRACKS_PROCESS | 344,256 | Monitoring | Process monitoring |
| MONITORS_EQUIPMENT | 289,233 | Observation | Equipment monitoring |
| CONSUMES_FROM | 289,050 | Dependency | Data consumption |
| PROCESSES_THROUGH | 270,203 | Flow | Data processing flow |
| CHAINS_TO | 225,358 | Sequencing | Sequential relationships |
| DELIVERS_TO | 216,126 | Flow | Delivery pipelines |
| MONITORS | 195,265 | Observation | Generic monitoring |
| MEASURES | 165,400 | Observation | Measurement relationships |
| USES_SOFTWARE | 149,949 | Dependency | Software usage |
| HAS_MEASUREMENT | 117,936 | Property | Measurement assignment |
| GOVERNS | 53,862 | Control | Policy governance |
| RELATED_TO | 49,232 | Generic | General association |
| HAS_PROPERTY | 42,052 | Property | Attribute assignment |
| HAS_ENERGY_PROPERTY | 30,000 | Property | Energy-specific attributes |
| BASED_ON_PATTERN | 29,970 | Analytics | Pattern references |
| THREATENS | 24,192 | Threat | Threat relationships |
| CONTROLS | 22,706 | Command | Control relationships |

#### Relationship Density

```
Total Relationships: 11,732,715
Total Possible (complete graph): 1,150,171² = 1.3T
Graph Density: ~0.00089 (highly sparse)

Interpretation: Efficient, non-redundant relationship model
with strategic connections rather than complete interconnection
```

### CVE Node Properties

**Sample CVE Node** (id: CVE-1999-0095):

```json
{
  "id": "CVE-1999-0095",
  "description": "The debug command in Sendmail is enabled, allowing attackers to execute commands as root.",
  "published_date": "1988-10-01",
  "modified_date": "2025-04-03",
  "cpe_vendors": ["Eric Allman"],
  "cpe_products": ["Sendmail"],
  "cpe_uris": ["cpe:2.3:a:eric_allman:sendmail:5.58:*:*:*:*:*:*:*"],
  "priority_tier": "NEVER",
  "epss_score": 0.0838,
  "epss_percentile": 0.91934,
  "epss_date": "2025-11-02",
  "epss_last_updated": "2025-11-02T17:21:46.323344Z",
  "priority_calculated_at": "2025-11-02T17:40:03.653Z"
}
```

**CVE Data Coverage**:
- **Enrichment**: CPE product/vendor mapping enabled
- **Risk Scoring**: EPSS scores with percentile rankings
- **Temporal Tracking**: Published, modified, and calculated dates
- **Priority Tiers**: NEVER, UNLIKELY, POSSIBLE, LIKELY, CRITICAL

---

## DATA INTEGRATION PATTERNS

### Qdrant ↔ Neo4j Integration Model

```
┌─────────────────────────────────────────────────────────┐
│ SEMANTIC LAYER (Qdrant - 221K entities)                 │
├─────────────────────────────────────────────────────────┤
│ • Vector embeddings (384-dim, cosine)                    │
│ • Entity text normalization                              │
│ • Temporal tracking (first/last seen)                    │
│ • Multi-label classification (68 types)                  │
│ • Document source tracking                               │
└────────────┬────────────────────────────────────────────┘
             │ Entity matching
             ↓
┌─────────────────────────────────────────────────────────┐
│ RELATIONSHIP LAYER (Neo4j - 1.1M nodes, 11.7M edges)    │
├─────────────────────────────────────────────────────────┤
│ • CVE vulnerability mapping (316K nodes)                 │
│ • Asset topology (device, software, component)           │
│ • Risk propagation (VULNERABLE_TO, IMPACTS)             │
│ • Critical infrastructure modeling                        │
│ • Supply chain dependencies (SBOM)                       │
│ • Sector-specific threat modeling                        │
└─────────────────────────────────────────────────────────┘
```

### Key Integration Points

1. **Entity Resolution**: Qdrant vectors enable fuzzy matching of entity variants found in Neo4j relationships

2. **Temporal Correlation**: Qdrant's `seen_count` tracks extraction frequency; Neo4j tracks relationship prevalence

3. **Classification Hierarchy**: 
   - Qdrant: 68 entity types (fine-grained NER labels)
   - Neo4j: Node labels represent domain roles (CVE, Device, Organization, etc.)

4. **Source Attribution**: 
   - Qdrant tracks original document source
   - Neo4j can link relationships back to source via intermediate nodes

---

## DATA QUALITY & CHARACTERISTICS

### Qdrant Quality Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| **Vector Coverage** | 98.8% | Excellent (218.4K/221K indexed) |
| **Payload Completeness** | 100% | All points have complete payload |
| **Temporal Tracking** | 73% | Good (161K with temporal data) |
| **Deduplication** | Unknown | May contain variant mentions |
| **Freshness** | Current | Latest: 2025-12-03 |

### Neo4j Quality Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| **Node Count** | 1.15M | Large-scale |
| **Relationship Density** | 0.089% | Sparse (efficient) |
| **CVE Enrichment** | 100% | EPSS scores present |
| **Data Freshness** | Current | CVE data updated 2025-11-02 |
| **Domain Coverage** | Multi-sector | 16+ critical infrastructure domains |

---

## APPLICATION FEATURE DEVELOPMENT RECOMMENDATIONS

### Tier 1: Semantic Search Features (Using Qdrant)

✅ **Vector similarity search** - Find entities semantically similar to query
✅ **Temporal entity analytics** - Track entity occurrence trends
✅ **Source document mapping** - Trace entities back to original documents
✅ **Multi-label classification** - Filter by entity type combinations
✅ **Entity deduplication** - Find variant mentions of same entity

### Tier 2: Risk Propagation Features (Using Neo4j)

✅ **CVE impact assessment** - Calculate blast radius of vulnerabilities
✅ **Dependency chain analysis** - Map supply chain risks
✅ **Critical path identification** - Find cascading failure risks
✅ **Sector-specific threat profiling** - Risk models by infrastructure sector
✅ **Asset inventory mapping** - Complete topology of systems/components

### Tier 3: Cross-Database Features (Hybrid)

✅ **Semantic relationship discovery** - Find mentions that should connect
✅ **Temporal threat intelligence** - Track threat evolution across sources
✅ **Risk scoring by entity** - Combine semantic + structural risk
✅ **Automated entity linking** - Match Qdrant extracts to Neo4j entities
✅ **Drill-down from text to topology** - Document → entity → graph

### Tier 4: Advanced Analytics (Integrated)

✅ **Threat actor behavior analysis** - Temporal patterns of threat activities
✅ **Vulnerability prediction** - Forecast likely CVE impacts
✅ **Anomaly detection** - Flag unusual entity relationships
✅ **Knowledge graph reasoning** - Infer hidden connections
✅ **Automated report generation** - Risk assessments with evidence chains

---

## TECHNICAL SPECIFICATIONS FOR API DEVELOPMENT

### Qdrant Query Patterns

```python
# Pattern 1: Semantic Search
POST /collections/ner11_entities_hierarchical/points/search
{
  "vector": [384-dim embedding],
  "limit": 100,
  "score_threshold": 0.7,
  "filter": {
    "must": [
      {"key": "label", "match": {"value": "CVE"}}
    ]
  }
}

# Pattern 2: Temporal Analysis
POST /collections/ner11_entities_hierarchical/points/scroll
{
  "filter": {
    "range": {
      "key": "last_seen",
      "gte": "2025-11-01T00:00:00Z"
    }
  }
}

# Pattern 3: Source Aggregation
POST /collections/ner11_entities_hierarchical/points/scroll
{
  "filter": {"match": {"key": "source_file", "value": "*.md"}}
}
```

### Neo4j Query Patterns

```cypher
// Pattern 1: Risk Propagation
MATCH (cve:CVE)-[:VULNERABLE_TO*1..3]->(asset:Device)
RETURN cve.id, asset, LENGTH(path) as hops

// Pattern 2: Dependency Chain
MATCH (component:SoftwareComponent)-[:INSTALLED_ON*1..5]->(host:Equipment)
RETURN component, host, LENGTH(path) as depth

// Pattern 3: Sector Risk
MATCH (threat:Threat)-[:THREATENS]->(sector:COMMUNICATIONS)
RETURN threat, count(sector) as impact_count
ORDER BY impact_count DESC
```

---

## CONSTRAINTS & LIMITATIONS

### Qdrant Constraints

1. **Entity Variants**: Multiple representations of same entity (e.g., "IBM Corp" vs "International Business Machines")
2. **Temporal Gaps**: 27% of entities lack temporal tracking (likely older ingestion batches)
3. **Vector Alignment**: 384-dim embeddings may not capture all semantic nuances
4. **Deduplication**: No built-in duplicate detection across batches

### Neo4j Constraints

1. **Relationship Multiplicity**: 11.7M relationships may create query performance bottlenecks for large traversals
2. **Data Lineage**: Limited information on relationship provenance (which document established it)
3. **Temporal Relationships**: Relationships lack timestamps (static snapshot)
4. **Real-time Updates**: Batch ingestion model, not streaming updates

### Cross-Database Challenges

1. **Entity Matching**: No automated linking between Qdrant entities and Neo4j nodes
2. **Update Synchronization**: Changes in one database don't automatically reflect in other
3. **Version Control**: No explicit versioning/audit trail for entity/relationship changes

---

## DATA REFRESH & MAINTENANCE

### Current State

- **Qdrant**: Last update 2025-12-03 (ongoing ingestion)
- **Neo4j**: CVE data refreshed 2025-11-02
- **Sync Model**: Batch-driven (periodic, not real-time)

### Recommended Practices

1. **Quarterly CVE Updates**: Re-ingest CVE data with latest EPSS scores
2. **Monthly Entity Rebalancing**: Deduplicate and normalize entity variants
3. **Backup Strategy**: Daily snapshots of both collections
4. **Change Tracking**: Maintain audit logs of ingestion timestamps

---

## CONCLUSION

The NER11 system provides a **dual-database architecture** optimized for:

- **Semantic discovery** (Qdrant) of entity mentions in documents
- **Structural analysis** (Neo4j) of complex relationships and dependencies

This enables applications ranging from **threat intelligence** to **supply chain risk analysis** with both **textual evidence** and **network topology** context.

The 221K entities and 1.15M nodes represent a **mature knowledge base** covering cybersecurity, critical infrastructure, and risk management domains.

---

**Report End**  
*For questions or data inquiries, contact the NER11 project team.*

