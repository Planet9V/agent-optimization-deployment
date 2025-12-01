# Schema Change Specifications for VulnCheck Integration

**File**: SCHEMA_CHANGE_SPECIFICATIONS.md
**Created**: 2025-11-01
**Version**: 1.0.0
**Author**: Schema-Architect Agent
**Purpose**: Complete DDL specifications for three VulnCheck integration recommendations
**Status**: ACTIVE

---

## Executive Summary

This document provides complete Neo4j DDL (Data Definition Language via Cypher) specifications for implementing three VulnCheck integration recommendations to enhance the AEON cybersecurity threat intelligence schema.

**Current Database State**:
- 267,487 CVE nodes (existing)
- 200,000 orphaned SBOM nodes (SoftwareComponent)
- 15 existing node types
- 25 existing relationship types
- 2.2M total nodes

**Schema Enhancement Summary**:
| Recommendation | New Node Types | New Relationship Types | Property Additions | Index/Constraint Changes |
|----------------|----------------|------------------------|-------------------|--------------------------|
| **1. Essential Exploitability** | 0 | 0 | 8 properties to CVE | 2 indexes |
| **2. Advanced Threat Intel** | 1 (ExploitCode) | 1 (HAS_EXPLOIT_CODE) | 8 properties to CVE, 10 to ExploitCode | 2 constraints, 3 indexes |
| **3. SBOM CPE Matching** | 1 (CPE) | 2 (MATCHES_CPE, AFFECTS) | 8 properties to CPE, 5 to relationships | 1 constraint, 4 indexes |

---

## Recommendation 1: Essential Exploitability Enrichment

### Overview
Enrich all 267,487 CVE nodes with EPSS exploitability scores, KEV (Known Exploited Vulnerabilities) flags, and calculated priority tiers for NOW/NEXT/NEVER classification.

### Schema Changes

#### 1.1 CVE Node Property Additions

**No new node types required** - Property enrichment only.

```cypher
// Properties to add to existing CVE nodes
(:CVE {
    // Existing properties preserved
    id: string,
    cvssScore: float,
    severity: string,
    description: string,
    published: datetime,

    // NEW PROPERTIES - EPSS (Exploit Prediction Scoring System)
    epss_score: float,              // 0.0-1.0 probability of exploitation in 30 days
    epss_percentile: float,         // 0.0-1.0 percentile ranking among all CVEs
    epss_date: date,                // Date of EPSS score calculation
    epss_last_updated: datetime,    // Last refresh timestamp for incremental updates

    // NEW PROPERTIES - KEV (Known Exploited Vulnerabilities)
    in_cisa_kev: boolean,           // In CISA official KEV catalog
    in_vulncheck_kev: boolean,      // In VulnCheck extended KEV catalog
    kev_date_added: datetime,       // When added to KEV
    kev_due_date: datetime,         // CISA remediation deadline (if applicable)
    kev_required_action: string,    // Remediation guidance text
    kev_ransomware_use: string,     // "Known"|"Unknown" ransomware association
    exploited_in_wild: boolean,     // Confirmed exploitation flag
    kev_last_updated: datetime,     // Last KEV check timestamp

    // NEW PROPERTIES - Priority Framework
    priority_tier: string,          // "NOW"|"NEXT"|"NEVER" classification
    priority_score: float,          // 0-200 composite risk score
    priority_factors: string,       // JSON map of contributing factors
    priority_reason: string,        // Human-readable explanation
    priority_calculated_at: datetime // Last priority calculation timestamp
})
```

**Data Types**:
- `float`: Neo4j double precision (64-bit)
- `boolean`: Neo4j boolean
- `string`: Neo4j string (UTF-8)
- `date`: Neo4j date (without time)
- `datetime`: Neo4j datetime (with timezone)

#### 1.2 Indexes

```cypher
// Index 1: EPSS Score for Priority Filtering
CREATE INDEX cve_epss_score IF NOT EXISTS
FOR (c:CVE) ON (c.epss_score);

// Index 2: EPSS Percentile for High-Risk Queries
CREATE INDEX cve_epss_percentile IF NOT EXISTS
FOR (c:CVE) ON (c.epss_percentile);

// Index 3: CISA KEV Flag for NOW-tier Filtering
CREATE INDEX cve_in_cisa_kev IF NOT EXISTS
FOR (c:CVE) ON (c.in_cisa_kev);

// Index 4: VulnCheck KEV Flag for Extended Coverage
CREATE INDEX cve_in_vulncheck_kev IF NOT EXISTS
FOR (c:CVE) ON (c.in_vulncheck_kev);

// Index 5: Exploited in Wild Flag for Active Threats
CREATE INDEX cve_exploited_in_wild IF NOT EXISTS
FOR (c:CVE) ON (c.exploited_in_wild);

// Index 6: Priority Tier for Dashboard Filtering
CREATE INDEX cve_priority_tier IF NOT EXISTS
FOR (c:CVE) ON (c.priority_tier);

// Index 7: Priority Score for Ranking
CREATE INDEX cve_priority_score IF NOT EXISTS
FOR (c:CVE) ON (c.priority_score);
```

**Index Rationale**:
- Boolean indexes (in_cisa_kev, in_vulncheck_kev, exploited_in_wild) enable fast filtering for NOW-tier CVEs
- Float indexes (epss_score, epss_percentile, priority_score) support range queries and ORDER BY operations
- String index (priority_tier) supports categorical filtering

**Index Performance Impact**:
- Index size: ~50MB per index for 267,487 CVEs
- Total storage overhead: ~350MB for 7 indexes
- Query performance improvement: 10-100x faster for filtered queries

#### 1.3 Constraints

**No new constraints required** - Leveraging existing CVE.id constraint.

```cypher
// Existing constraint (already present)
CREATE CONSTRAINT cve_id IF NOT EXISTS
FOR (c:CVE) REQUIRE c.id IS UNIQUE;
```

#### 1.4 Data Volume Impact

| Metric | Value | Calculation |
|--------|-------|-------------|
| **Nodes Affected** | 267,487 CVEs | All existing CVE nodes |
| **Property Additions** | 16 properties × 267,487 nodes | 4,279,792 property values |
| **Estimated Storage Increase** | ~150 MB | Avg 60 bytes/property × 16 × 267,487 |
| **Index Storage** | ~350 MB | 7 indexes × ~50MB each |
| **Total Storage Impact** | ~500 MB | Property + index storage |
| **Percentage of Existing DB** | ~5% | Assuming current DB ~10GB |

**Per-Node Storage Breakdown**:
```
EPSS properties: 4 properties × 8 bytes avg = 32 bytes
KEV properties: 7 properties × 12 bytes avg = 84 bytes
Priority properties: 5 properties × 15 bytes avg = 75 bytes
Total per CVE: ~191 bytes per node
Total for 267,487 CVEs: ~51 MB (actual property data)
```

**Neo4j Property Storage**:
- Strings stored inline (< 32 bytes) or in property store
- Floats/booleans: 8 bytes each
- Datetime: 16 bytes each
- JSON strings (priority_factors): variable, avg ~200 bytes

#### 1.5 Migration DDL Script

```cypher
// ============================================
// RECOMMENDATION 1: ESSENTIAL EXPLOITABILITY
// Migration Script for Property Additions
// ============================================

// Step 1: Add EPSS properties with default null values
MATCH (cve:CVE)
SET cve.epss_score = null,
    cve.epss_percentile = null,
    cve.epss_date = null,
    cve.epss_last_updated = null;

// Step 2: Add KEV properties with default null/false values
MATCH (cve:CVE)
SET cve.in_cisa_kev = false,
    cve.in_vulncheck_kev = false,
    cve.kev_date_added = null,
    cve.kev_due_date = null,
    cve.kev_required_action = null,
    cve.kev_ransomware_use = 'Unknown',
    cve.exploited_in_wild = false,
    cve.kev_last_updated = null;

// Step 3: Add Priority Framework properties
MATCH (cve:CVE)
SET cve.priority_tier = null,
    cve.priority_score = null,
    cve.priority_factors = null,
    cve.priority_reason = null,
    cve.priority_calculated_at = null;

// Step 4: Create all indexes (idempotent)
CREATE INDEX cve_epss_score IF NOT EXISTS
FOR (c:CVE) ON (c.epss_score);

CREATE INDEX cve_epss_percentile IF NOT EXISTS
FOR (c:CVE) ON (c.epss_percentile);

CREATE INDEX cve_in_cisa_kev IF NOT EXISTS
FOR (c:CVE) ON (c.in_cisa_kev);

CREATE INDEX cve_in_vulncheck_kev IF NOT EXISTS
FOR (c:CVE) ON (c.in_vulncheck_kev);

CREATE INDEX cve_exploited_in_wild IF NOT EXISTS
FOR (c:CVE) ON (c.exploited_in_wild);

CREATE INDEX cve_priority_tier IF NOT EXISTS
FOR (c:CVE) ON (c.priority_tier);

CREATE INDEX cve_priority_score IF NOT EXISTS
FOR (c:CVE) ON (c.priority_score);

// Step 5: Verification Queries
// Check property addition
MATCH (cve:CVE)
WHERE cve.id = 'CVE-2021-44228'  // Log4Shell test case
RETURN cve.id,
       exists(cve.epss_score) AS has_epss,
       exists(cve.in_cisa_kev) AS has_kev,
       exists(cve.priority_tier) AS has_priority;

// Count total CVEs affected
MATCH (cve:CVE)
RETURN count(*) AS total_cves,
       sum(CASE WHEN exists(cve.epss_score) THEN 1 ELSE 0 END) AS cves_with_epss_structure;
// Expected: 267,487 total, 267,487 with structure (null values initially)

// Check indexes created
SHOW INDEXES YIELD name, type, labelsOrTypes, properties
WHERE 'CVE' IN labelsOrTypes
RETURN name, type, properties
ORDER BY name;
// Expected: 7 indexes on CVE properties
```

**Migration Execution Strategy**:
1. **Batch Size**: Process in batches of 10,000 nodes to avoid transaction memory limits
2. **Estimated Duration**: 10-15 minutes for property additions (267,487 nodes)
3. **Index Creation**: 5-10 minutes per index (7 indexes = ~50 minutes total)
4. **Total Migration Time**: ~60-65 minutes
5. **Rollback Strategy**: Properties can be removed with `REMOVE cve.epss_score` etc.

**Production Migration Script** (Batched):
```cypher
// Batched migration to avoid transaction limits
CALL apoc.periodic.iterate(
  "MATCH (cve:CVE) RETURN cve",
  "SET cve.epss_score = null,
       cve.epss_percentile = null,
       cve.epss_date = null,
       cve.epss_last_updated = null,
       cve.in_cisa_kev = false,
       cve.in_vulncheck_kev = false,
       cve.kev_date_added = null,
       cve.kev_due_date = null,
       cve.kev_required_action = null,
       cve.kev_ransomware_use = 'Unknown',
       cve.exploited_in_wild = false,
       cve.kev_last_updated = null,
       cve.priority_tier = null,
       cve.priority_score = null,
       cve.priority_factors = null,
       cve.priority_reason = null,
       cve.priority_calculated_at = null",
  {batchSize: 10000, parallel: false}
);
```

#### 1.6 Performance Considerations

**Query Performance Impact**:
- **Before Indexes**: Full CVE scan for filtering = ~5-10 seconds
- **After Indexes**: Index lookup + node retrieval = ~50-200ms
- **Improvement**: 25-200x faster for priority-based queries

**Write Performance Impact**:
- **Property Updates**: Minimal overhead (~1-2% slower writes)
- **Index Maintenance**: Automatically maintained by Neo4j
- **Batch Operations**: Recommended batch size 1,000-10,000 nodes

**Example Query Performance** (with indexes):
```cypher
// Query: Find all NOW-tier CVEs (estimated 1,000-2,000 results)
MATCH (cve:CVE)
WHERE cve.priority_tier = 'NOW'
RETURN cve.id, cve.cvssScore, cve.epss_score, cve.priority_score
ORDER BY cve.priority_score DESC
LIMIT 100;

// Performance with index:
// - Index scan: 1,000-2,000 nodes
// - Sort: In-memory
// - Total time: ~50-100ms

// Performance without index:
// - Full node scan: 267,487 nodes
// - Filter: 267,487 comparisons
// - Sort: 1,000-2,000 nodes
// - Total time: ~5,000-8,000ms
```

#### 1.7 Validation Queries

```cypher
// Validation 1: Verify property structure added to all CVEs
MATCH (cve:CVE)
RETURN count(*) AS total_cves,
       sum(CASE WHEN cve.epss_score IS NULL THEN 1 ELSE 0 END) AS epss_null_count,
       sum(CASE WHEN cve.in_cisa_kev = false THEN 1 ELSE 0 END) AS kev_false_count,
       sum(CASE WHEN cve.priority_tier IS NULL THEN 1 ELSE 0 END) AS priority_null_count;
// Expected: 267,487 total, all null/false initially

// Validation 2: Check index existence and schema
SHOW INDEXES YIELD name, type, labelsOrTypes, properties, state
WHERE 'CVE' IN labelsOrTypes
  AND name STARTS WITH 'cve_'
RETURN name, type, properties, state;
// Expected: 7 indexes, all state = 'ONLINE'

// Validation 3: Test index performance
PROFILE
MATCH (cve:CVE)
WHERE cve.in_cisa_kev = true
RETURN count(*);
// Expected: Uses index scan (db hit = 0 initially, since all false)

// Validation 4: Verify no data loss in existing properties
MATCH (cve:CVE)
WHERE cve.id = 'CVE-2021-44228'
RETURN cve.id, cve.cvssScore, cve.severity, cve.description;
// Expected: Existing properties unchanged
```

---

## Recommendation 2: Advanced Threat Intelligence

### Overview
Extend Recommendation 1 with exploit code intelligence (VulnCheck XDB), community assessments (AttackerKB), and trending alerts (CVEmon). Introduces new ExploitCode node type and HAS_EXPLOIT_CODE relationship.

### Schema Changes

#### 2.1 New Node Type: ExploitCode

```cypher
// New node type for proof-of-concept exploit code
CREATE CONSTRAINT exploit_code_id IF NOT EXISTS
FOR (ec:ExploitCode) REQUIRE ec.xdb_id IS UNIQUE;

(:ExploitCode {
    xdb_id: string,                  // VulnCheck XDB identifier (REQUIRED, UNIQUE)
    xdb_url: string,                 // VulnCheck XDB page URL
    clone_ssh_url: string,           // Git repository clone URL
    exploit_type: string,            // "initial-access"|"privilege-escalation"|"lateral-movement"|"dos"
    date_added: datetime,            // When exploit was indexed by VulnCheck
    maturity: string,                // "poc"|"functional"|"weaponized" (inferred)
    repository_stars: int,           // GitHub stars (popularity indicator)
    last_commit_date: datetime,      // Repository activity timestamp
    language: string,                // Programming language (e.g., "python", "ruby", "c")
    is_validated: boolean,           // Human-reviewed by VulnCheck analysts
    created_at: datetime,            // Node creation timestamp
    updated_at: datetime             // Node last update timestamp
})
```

**Property Rationale**:
- `xdb_id`: Unique identifier from VulnCheck (e.g., "xdb_12345")
- `exploit_type`: MITRE ATT&CK-aligned categorization
- `maturity`: Critical for threat assessment (PoC < Functional < Weaponized)
- `repository_stars`: Indicator of community interest and quality
- `is_validated`: VulnCheck human validation increases confidence

**Indexes**:
```cypher
// Index 1: Exploit Type for Filtering
CREATE INDEX exploit_code_type IF NOT EXISTS
FOR (ec:ExploitCode) ON (ec.exploit_type);

// Index 2: Maturity Level for Risk Assessment
CREATE INDEX exploit_code_maturity IF NOT EXISTS
FOR (ec:ExploitCode) ON (ec.maturity);

// Index 3: Validation Status
CREATE INDEX exploit_code_validated IF NOT EXISTS
FOR (ec:ExploitCode) ON (ec.is_validated);
```

#### 2.2 New Relationship Type: HAS_EXPLOIT_CODE

```cypher
// Relationship from CVE to ExploitCode
CREATE (cve:CVE)-[r:HAS_EXPLOIT_CODE]->(ec:ExploitCode)

// Relationship properties
(:HAS_EXPLOIT_CODE {
    confidence: float,               // 0.0-1.0 mapping confidence
    verified: boolean,               // VulnCheck validation status
    date_discovered: datetime,       // When exploit was linked to CVE
    threat_level: string            // "high"|"medium"|"low" based on maturity
})
```

**Relationship Rationale**:
- `confidence`: VulnCheck provides mapping confidence for CVE-to-exploit links
- `threat_level`: Derived from ExploitCode.maturity for quick filtering
- `date_discovered`: Tracks exploitation timeline

**Relationship Index**:
```cypher
// Index on relationship properties for performance
// Note: Neo4j 5.x supports relationship property indexes
CREATE INDEX has_exploit_code_threat_level IF NOT EXISTS
FOR ()-[r:HAS_EXPLOIT_CODE]-() ON (r.threat_level);
```

#### 2.3 CVE Node Property Additions (Recommendation 2)

```cypher
// Additional properties to CVE nodes (extends Recommendation 1)
(:CVE {
    // All Recommendation 1 properties, PLUS:

    // Exploit Intelligence Summary Properties
    exploit_available: boolean,         // Quick flag: has any exploit
    exploit_count: int,                 // Number of ExploitCode nodes linked
    has_weaponized_exploit: boolean,    // Quick flag: maturity = "weaponized"

    // AttackerKB Community Assessment
    attackerkb_score: float,            // 0-10 community rating
    attackerkb_assessment_count: int,   // Number of assessments
    attackerkb_topic_id: string,        // AttackerKB topic ID for API lookups
    attackerkb_rapid_7_assessed: boolean, // Rapid7 official assessment exists
    attackerkb_last_updated: datetime,  // Last AttackerKB sync

    // CVEmon Trending Intelligence
    trending_rank: int,                 // 1-10 ranking in CVEmon top 10
    hype_score: int,                    // 0-100 social media hype score
    trending_date: datetime             // When trending was recorded
})
```

**Property Rationale**:
- **Summary Properties** (exploit_available, exploit_count, has_weaponized_exploit): Denormalized for fast filtering without relationship traversal
- **AttackerKB**: Community-driven real-world exploitability insights
- **Trending**: Early warning system from social media monitoring

**Additional Indexes**:
```cypher
// Index for exploit availability filtering
CREATE INDEX cve_exploit_available IF NOT EXISTS
FOR (c:CVE) ON (c.exploit_available);

// Index for weaponized exploit filtering
CREATE INDEX cve_has_weaponized_exploit IF NOT EXISTS
FOR (c:CVE) ON (c.has_weaponized_exploit);

// Index for AttackerKB score filtering
CREATE INDEX cve_attackerkb_score IF NOT EXISTS
FOR (c:CVE) ON (c.attackerkb_score);

// Index for trending CVEs
CREATE INDEX cve_trending_rank IF NOT EXISTS
FOR (c:CVE) ON (c.trending_rank);
```

#### 2.4 Data Volume Impact

| Metric | Value | Calculation |
|--------|-------|-------------|
| **New Nodes (ExploitCode)** | 13,000-27,000 nodes | 5-10% of CVEs have exploits |
| **New Relationships** | 15,000-30,000 relationships | Some CVEs have multiple exploits |
| **CVE Property Additions** | 11 properties × 267,487 nodes | ~2.9M property values |
| **Estimated Storage Increase** | ~300 MB | ExploitCode nodes + relationships + properties |
| **Percentage of Existing DB** | ~3% | Assuming current DB ~10GB |

**Per-Node Storage Breakdown**:
```
ExploitCode node: ~250 bytes per node
  - xdb_id: 20 bytes
  - xdb_url: 80 bytes
  - clone_ssh_url: 100 bytes
  - Other properties: 50 bytes

HAS_EXPLOIT_CODE relationship: ~50 bytes per relationship
  - Relationship structure: 30 bytes
  - Properties: 20 bytes

CVE property additions: ~150 bytes per CVE
  - 11 properties × ~13 bytes avg
```

**Storage Calculation**:
```
ExploitCode nodes: 20,000 nodes × 250 bytes = 5 MB
Relationships: 22,500 relationships × 50 bytes = 1.1 MB
CVE properties: 267,487 nodes × 150 bytes = 40 MB
Indexes: 7 indexes × ~20 MB each = 140 MB
Total: ~186 MB (rounded to ~200 MB)
```

#### 2.5 Migration DDL Script

```cypher
// ============================================
// RECOMMENDATION 2: ADVANCED THREAT INTELLIGENCE
// Migration Script
// ============================================

// Step 1: Create ExploitCode constraint
CREATE CONSTRAINT exploit_code_id IF NOT EXISTS
FOR (ec:ExploitCode) REQUIRE ec.xdb_id IS UNIQUE;

// Step 2: Create ExploitCode indexes
CREATE INDEX exploit_code_type IF NOT EXISTS
FOR (ec:ExploitCode) ON (ec.exploit_type);

CREATE INDEX exploit_code_maturity IF NOT EXISTS
FOR (ec:ExploitCode) ON (ec.maturity);

CREATE INDEX exploit_code_validated IF NOT EXISTS
FOR (ec:ExploitCode) ON (ec.is_validated);

// Step 3: Add exploit intelligence properties to CVE nodes
MATCH (cve:CVE)
SET cve.exploit_available = false,
    cve.exploit_count = 0,
    cve.has_weaponized_exploit = false,
    cve.attackerkb_score = null,
    cve.attackerkb_assessment_count = 0,
    cve.attackerkb_topic_id = null,
    cve.attackerkb_rapid_7_assessed = false,
    cve.attackerkb_last_updated = null,
    cve.trending_rank = null,
    cve.hype_score = null,
    cve.trending_date = null;

// Step 4: Create CVE indexes for new properties
CREATE INDEX cve_exploit_available IF NOT EXISTS
FOR (c:CVE) ON (c.exploit_available);

CREATE INDEX cve_has_weaponized_exploit IF NOT EXISTS
FOR (c:CVE) ON (c.has_weaponized_exploit);

CREATE INDEX cve_attackerkb_score IF NOT EXISTS
FOR (c:CVE) ON (c.attackerkb_score);

CREATE INDEX cve_trending_rank IF NOT EXISTS
FOR (c:CVE) ON (c.trending_rank);

// Step 5: Create relationship property index (Neo4j 5.x)
CREATE INDEX has_exploit_code_threat_level IF NOT EXISTS
FOR ()-[r:HAS_EXPLOIT_CODE]-() ON (r.threat_level);

// Step 6: Verification Queries
// Check ExploitCode constraint
SHOW CONSTRAINTS YIELD name, type, labelsOrTypes, properties
WHERE 'ExploitCode' IN labelsOrTypes
RETURN name, type, properties;
// Expected: 1 constraint on xdb_id

// Check all indexes created
SHOW INDEXES YIELD name, type, labelsOrTypes, properties
WHERE 'ExploitCode' IN labelsOrTypes OR name STARTS WITH 'cve_exploit' OR name STARTS WITH 'cve_has_weaponized' OR name STARTS WITH 'cve_attackerkb' OR name STARTS WITH 'cve_trending'
RETURN name, type, labelsOrTypes, properties;
// Expected: 8 indexes total (3 ExploitCode + 4 CVE + 1 relationship)

// Check CVE property additions
MATCH (cve:CVE)
WHERE cve.id = 'CVE-2021-44228'
RETURN cve.id,
       exists(cve.exploit_available) AS has_exploit_flag,
       exists(cve.attackerkb_score) AS has_akb_structure;
// Expected: All flags present (false/null initially)
```

**Batched Migration Script**:
```cypher
// Batched CVE property updates
CALL apoc.periodic.iterate(
  "MATCH (cve:CVE) RETURN cve",
  "SET cve.exploit_available = false,
       cve.exploit_count = 0,
       cve.has_weaponized_exploit = false,
       cve.attackerkb_score = null,
       cve.attackerkb_assessment_count = 0,
       cve.attackerkb_topic_id = null,
       cve.attackerkb_rapid_7_assessed = false,
       cve.attackerkb_last_updated = null,
       cve.trending_rank = null,
       cve.hype_score = null,
       cve.trending_date = null",
  {batchSize: 10000, parallel: false}
);
```

**Migration Execution**:
- **Estimated Duration**: 15-20 minutes (constraints + indexes + property additions)
- **Rollback Strategy**:
  - Drop constraint: `DROP CONSTRAINT exploit_code_id`
  - Remove properties: `MATCH (cve:CVE) REMOVE cve.exploit_available, cve.exploit_count, ...`
  - Delete ExploitCode nodes: `MATCH (ec:ExploitCode) DETACH DELETE ec`

#### 2.6 Example ExploitCode Node Creation

```cypher
// Example: Create ExploitCode node and link to CVE
MERGE (ec:ExploitCode {xdb_id: 'xdb_12345'})
ON CREATE SET
    ec.xdb_url = 'https://vulncheck.com/xdb/xdb_12345',
    ec.clone_ssh_url = 'git@github.com:exploitdb/CVE-2021-44228.git',
    ec.exploit_type = 'initial-access',
    ec.date_added = datetime('2021-12-10T14:30:00Z'),
    ec.maturity = 'weaponized',
    ec.repository_stars = 1250,
    ec.last_commit_date = datetime('2021-12-15T09:22:00Z'),
    ec.language = 'python',
    ec.is_validated = true,
    ec.created_at = datetime()
ON MATCH SET
    ec.updated_at = datetime()

WITH ec
MATCH (cve:CVE {id: 'CVE-2021-44228'})
MERGE (cve)-[r:HAS_EXPLOIT_CODE]->(ec)
ON CREATE SET
    r.confidence = 1.0,
    r.verified = true,
    r.date_discovered = datetime(),
    r.threat_level = 'high'

// Update CVE summary properties
WITH cve
OPTIONAL MATCH (cve)-[:HAS_EXPLOIT_CODE]->(exploits:ExploitCode)
WITH cve, count(exploits) AS exploit_cnt,
     max(CASE WHEN exploits.maturity = 'weaponized' THEN 1 ELSE 0 END) AS has_weaponized
SET cve.exploit_available = (exploit_cnt > 0),
    cve.exploit_count = exploit_cnt,
    cve.has_weaponized_exploit = (has_weaponized = 1);
```

#### 2.7 Performance Considerations

**Query Performance Examples**:

```cypher
// Query 1: Find CVEs with weaponized exploits (using denormalized property)
MATCH (cve:CVE)
WHERE cve.has_weaponized_exploit = true
RETURN cve.id, cve.cvssScore, cve.epss_score
ORDER BY cve.priority_score DESC
LIMIT 50;
// Performance: ~50ms (index scan, no relationship traversal)

// Query 2: Find exploit details for high-priority CVEs (with relationship)
MATCH (cve:CVE)-[r:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
WHERE cve.priority_tier = 'NOW'
  AND ec.maturity IN ['functional', 'weaponized']
RETURN cve.id, ec.xdb_url, ec.exploit_type, ec.maturity, r.threat_level
ORDER BY cve.priority_score DESC
LIMIT 100;
// Performance: ~150ms (index scan + relationship traversal + index filter)

// Query 3: AttackerKB community-validated CVEs
MATCH (cve:CVE)
WHERE cve.attackerkb_score >= 7.0
  AND cve.attackerkb_assessment_count >= 3
RETURN cve.id, cve.attackerkb_score, cve.epss_score, cve.cvssScore
ORDER BY cve.attackerkb_score DESC;
// Performance: ~80ms (index range scan)
```

**Write Performance**:
- **ExploitCode Creation**: ~5-10ms per node (with constraint check)
- **Relationship Creation**: ~3-5ms per relationship
- **CVE Summary Update**: ~2-3ms per node
- **Batch Operations**: Process 1,000 nodes in ~10-15 seconds

---

## Recommendation 3: SBOM CPE Matching

### Overview
Resolve 200,000 orphaned SBOM nodes by creating CPE (Common Platform Enumeration) bridge entities and matching SoftwareComponent nodes to CVEs via CPE-to-CVE relationships.

### Schema Changes

#### 3.1 New Node Type: CPE

```cypher
// CPE (Common Platform Enumeration) bridge entity
CREATE CONSTRAINT cpe_uri IF NOT EXISTS
FOR (cpe:CPE) REQUIRE cpe.uri IS UNIQUE;

(:CPE {
    uri: string,                    // CPE 2.3 URI (REQUIRED, UNIQUE)
                                    // Format: cpe:2.3:part:vendor:product:version:update:edition:language:sw_edition:target_sw:target_hw:other
    vendor: string,                 // Normalized vendor name (e.g., "apache")
    product: string,                // Normalized product name (e.g., "log4j")
    version: string,                // Version string (e.g., "2.14.1")
    update: string,                 // Update/patch level (e.g., "p1")
    edition: string,                // Edition (e.g., "enterprise")
    language: string,               // Language (e.g., "en")
    part: string,                   // 'a' (application), 'o' (OS), 'h' (hardware)
    source: string,                 // 'nvd'|'vulncheck_nvd_plus'|'cpe_dict'
    created_at: datetime,           // Node creation timestamp
    updated_at: datetime            // Node last update timestamp
})
```

**Property Rationale**:
- `uri`: Full CPE 2.3 URI as unique identifier
- `vendor`, `product`, `version`: Parsed components for matching algorithms
- `part`: Differentiates application CPEs from OS/hardware CPEs
- `source`: Tracks origin (NVD vs VulnCheck enhanced data)

**CPE Indexes**:
```cypher
// Index 1: Vendor for exact match queries
CREATE INDEX cpe_vendor IF NOT EXISTS
FOR (cpe:CPE) ON (cpe.vendor);

// Index 2: Product for exact match queries
CREATE INDEX cpe_product IF NOT EXISTS
FOR (cpe:CPE) ON (cpe.product);

// Index 3: Version for range queries
CREATE INDEX cpe_version IF NOT EXISTS
FOR (cpe:CPE) ON (cpe.version);

// Index 4: Composite index for vendor+product matching
CREATE INDEX cpe_vendor_product IF NOT EXISTS
FOR (cpe:CPE) ON (cpe.vendor, cpe.product);
```

#### 3.2 New Relationship Type: MATCHES_CPE

```cypher
// Relationship from SoftwareComponent to CPE
CREATE (sbom:SoftwareComponent)-[r:MATCHES_CPE]->(cpe:CPE)

// Relationship properties
(:MATCHES_CPE {
    match_confidence: float,        // 0.0-1.0 matching confidence score
    match_method: string,           // "exact"|"fuzzy"|"vendor_verified"|"version_range"
    version_comparison: string,     // "exact"|"greater"|"range"|"semantic"
    matched_at: datetime,           // When match was created
    match_metadata: string          // JSON: additional matching details
})
```

**Relationship Rationale**:
- `match_confidence`: Critical for filtering false positives (recommend threshold 0.7+)
- `match_method`: Documents matching algorithm used (for audit and tuning)
- `version_comparison`: Explains version matching logic (exact vs range)

#### 3.3 New Relationship Type: AFFECTS

```cypher
// Relationship from CPE to CVE
CREATE (cpe:CPE)-[r:AFFECTS]->(cve:CVE)

// Relationship properties
(:AFFECTS {
    vulnerable_version_range: string,  // ">=1.0.0, <2.0.0" (CPE version range)
    cvss_score: float,                 // CVSS score for this CPE configuration
    severity: string,                  // "low"|"medium"|"high"|"critical"
    source: string,                    // 'nvd'|'vulncheck_nvd_plus'
    date_added: datetime               // When relationship was created
})
```

**Relationship Rationale**:
- `vulnerable_version_range`: Stores CPE version applicability from NVD
- `cvss_score`: CPE-specific CVSS (can differ from CVE base score)
- `source`: Distinguishes NVD data from VulnCheck enhancements

#### 3.4 SoftwareComponent Node Property Additions

```cypher
// Properties to add to existing SoftwareComponent nodes (optional, for performance)
(:SoftwareComponent {
    // Existing properties preserved
    name: string,
    vendor: string,
    version: string,

    // NEW PROPERTIES - Vulnerability Summary (Denormalized for Performance)
    vuln_count: int,                // Total CVEs affecting this component
    high_risk_vuln_count: int,      // CVEs with epss_score > 0.2
    epss_avg: float,                // Average EPSS score of linked CVEs
    priority_tier: string,          // Aggregate: "NOW"|"NEXT"|"NEVER"
    cpe_match_count: int,           // Number of CPE matches
    cpe_match_confidence_avg: float, // Average match confidence
    vulnerability_last_updated: datetime // Last vulnerability analysis timestamp
})
```

**Property Rationale**:
- **Denormalization**: Avoids expensive multi-hop traversals for component risk queries
- **Aggregate Scores**: Pre-calculated component-level risk assessment
- **Priority Tier**: Component-level NOW/NEXT/NEVER classification

**SoftwareComponent Indexes**:
```cypher
// Index for vulnerability count filtering
CREATE INDEX sbom_vuln_count IF NOT EXISTS
FOR (s:SoftwareComponent) ON (s.vuln_count);

// Index for high-risk component filtering
CREATE INDEX sbom_high_risk_vuln_count IF NOT EXISTS
FOR (s:SoftwareComponent) ON (s.high_risk_vuln_count);

// Index for priority tier filtering
CREATE INDEX sbom_priority_tier IF NOT EXISTS
FOR (s:SoftwareComponent) ON (s.priority_tier);
```

#### 3.5 Data Volume Impact

| Metric | Value | Calculation |
|--------|-------|-------------|
| **New Nodes (CPE)** | 50,000-100,000 nodes | Unique CPE URIs from NVD + VulnCheck |
| **MATCHES_CPE Relationships** | 120,000-170,000 | 60-85% of 200K SBOM nodes matched |
| **AFFECTS Relationships** | 500,000-800,000 | Each CVE has 2-3 CPE configurations avg |
| **SoftwareComponent Property Additions** | 7 properties × 200,000 nodes | 1.4M property values |
| **Estimated Storage Increase** | ~1.2 GB | CPE nodes + relationships + properties |
| **Percentage of Existing DB** | ~12% | Assuming current DB ~10GB |

**Storage Breakdown**:
```
CPE nodes: 75,000 nodes × 300 bytes = 22.5 MB
MATCHES_CPE relationships: 145,000 rels × 60 bytes = 8.7 MB
AFFECTS relationships: 650,000 rels × 70 bytes = 45.5 MB
SoftwareComponent properties: 200,000 nodes × 100 bytes = 20 MB
Indexes: 7 indexes × ~100 MB each = 700 MB
Total: ~797 MB (rounded to ~800 MB)
```

**Relationship Count Explanation**:
- **MATCHES_CPE**: 60-85% match rate on 200K orphans = 120K-170K relationships
- **AFFECTS**: 267,487 CVEs × 2.5 CPE configs avg = ~668K relationships

#### 3.6 Migration DDL Script

```cypher
// ============================================
// RECOMMENDATION 3: SBOM CPE MATCHING
// Migration Script
// ============================================

// Step 1: Create CPE constraint
CREATE CONSTRAINT cpe_uri IF NOT EXISTS
FOR (cpe:CPE) REQUIRE cpe.uri IS UNIQUE;

// Step 2: Create CPE indexes
CREATE INDEX cpe_vendor IF NOT EXISTS
FOR (cpe:CPE) ON (cpe.vendor);

CREATE INDEX cpe_product IF NOT EXISTS
FOR (cpe:CPE) ON (cpe.product);

CREATE INDEX cpe_version IF NOT EXISTS
FOR (cpe:CPE) ON (cpe.version);

CREATE INDEX cpe_vendor_product IF NOT EXISTS
FOR (cpe:CPE) ON (cpe.vendor, cpe.product);

// Step 3: Add vulnerability summary properties to SoftwareComponent nodes
MATCH (sbom:SoftwareComponent)
SET sbom.vuln_count = 0,
    sbom.high_risk_vuln_count = 0,
    sbom.epss_avg = null,
    sbom.priority_tier = null,
    sbom.cpe_match_count = 0,
    sbom.cpe_match_confidence_avg = null,
    sbom.vulnerability_last_updated = null;

// Step 4: Create SoftwareComponent indexes
CREATE INDEX sbom_vuln_count IF NOT EXISTS
FOR (s:SoftwareComponent) ON (s.vuln_count);

CREATE INDEX sbom_high_risk_vuln_count IF NOT EXISTS
FOR (s:SoftwareComponent) ON (s.high_risk_vuln_count);

CREATE INDEX sbom_priority_tier IF NOT EXISTS
FOR (s:SoftwareComponent) ON (s.priority_tier);

// Step 5: Verification Queries
// Check CPE constraint
SHOW CONSTRAINTS YIELD name, type, labelsOrTypes, properties
WHERE 'CPE' IN labelsOrTypes
RETURN name, type, properties;
// Expected: 1 constraint on uri

// Check CPE indexes
SHOW INDEXES YIELD name, type, labelsOrTypes, properties
WHERE 'CPE' IN labelsOrTypes
RETURN name, type, properties;
// Expected: 4 indexes (vendor, product, version, vendor_product)

// Check SoftwareComponent property additions
MATCH (sbom:SoftwareComponent)
RETURN count(*) AS total_sbom_nodes,
       sum(CASE WHEN exists(sbom.vuln_count) THEN 1 ELSE 0 END) AS nodes_with_vuln_structure;
// Expected: 200,000 total, 200,000 with structure

// Check SoftwareComponent indexes
SHOW INDEXES YIELD name, type, labelsOrTypes, properties
WHERE 'SoftwareComponent' IN labelsOrTypes
RETURN name, type, properties;
// Expected: 3 indexes (vuln_count, high_risk_vuln_count, priority_tier)
```

**Batched Migration Script**:
```cypher
// Batched SoftwareComponent property updates
CALL apoc.periodic.iterate(
  "MATCH (sbom:SoftwareComponent) RETURN sbom",
  "SET sbom.vuln_count = 0,
       sbom.high_risk_vuln_count = 0,
       sbom.epss_avg = null,
       sbom.priority_tier = null,
       sbom.cpe_match_count = 0,
       sbom.cpe_match_confidence_avg = null,
       sbom.vulnerability_last_updated = null",
  {batchSize: 10000, parallel: false}
);
```

**Migration Execution**:
- **Estimated Duration**: 30-40 minutes (constraints + indexes + property additions)
- **Rollback Strategy**:
  - Drop CPE nodes: `MATCH (cpe:CPE) DETACH DELETE cpe`
  - Remove SBOM properties: `MATCH (sbom:SoftwareComponent) REMOVE sbom.vuln_count, ...`
  - Drop indexes: `DROP INDEX cpe_vendor`

#### 3.7 CPE Matching Algorithm Implementation

**Exact Match Strategy**:
```cypher
// Strategy 1: Exact vendor + product + version match
MATCH (sbom:SoftwareComponent)
MATCH (cpe:CPE)
WHERE toLower(sbom.vendor) = toLower(cpe.vendor)
  AND toLower(sbom.name) = toLower(cpe.product)
  AND sbom.version = cpe.version
MERGE (sbom)-[r:MATCHES_CPE]->(cpe)
ON CREATE SET
    r.match_confidence = 1.0,
    r.match_method = 'exact',
    r.version_comparison = 'exact',
    r.matched_at = datetime(),
    r.match_metadata = '{"algorithm": "exact_vendor_product_version"}';

// Update SBOM summary
WITH sbom
SET sbom.cpe_match_count = sbom.cpe_match_count + 1;
```

**Fuzzy Match Strategy** (using APOC or custom function):
```cypher
// Strategy 2: Fuzzy product name match with version range
MATCH (sbom:SoftwareComponent)
MATCH (cpe:CPE)
WHERE toLower(sbom.vendor) = toLower(cpe.vendor)
  AND (
    toLower(sbom.name) = toLower(cpe.product)
    OR sbom.name CONTAINS cpe.product
    OR cpe.product CONTAINS sbom.name
    OR apoc.text.levenshteinSimilarity(sbom.name, cpe.product) >= 0.8
  )
  // Version range check (pseudocode - implement in application logic)
  AND check_version_in_range(sbom.version, cpe.version)
MERGE (sbom)-[r:MATCHES_CPE]->(cpe)
ON CREATE SET
    r.match_confidence = 0.85,
    r.match_method = 'fuzzy',
    r.version_comparison = 'range',
    r.matched_at = datetime(),
    r.match_metadata = apoc.convert.toJson({
        algorithm: 'fuzzy_levenshtein',
        similarity: apoc.text.levenshteinSimilarity(sbom.name, cpe.product)
    });
```

**Version Range Matching** (application logic):
```python
def check_version_in_range(sbom_version, cpe_version):
    """
    Check if SBOM version falls within CPE version range.
    Supports semantic versioning comparisons.
    """
    from packaging import version

    try:
        sbom_ver = version.parse(sbom_version)
        cpe_ver = version.parse(cpe_version)

        # Simple comparison (can be extended with range parsing)
        return sbom_ver >= cpe_ver
    except:
        # Fallback to string comparison
        return sbom_version == cpe_version
```

#### 3.8 CPE Creation from VulnCheck NVD++

```cypher
// Example: Create CPE node from VulnCheck data
MERGE (cpe:CPE {uri: 'cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*'})
ON CREATE SET
    cpe.vendor = 'apache',
    cpe.product = 'log4j',
    cpe.version = '2.14.1',
    cpe.update = '*',
    cpe.edition = '*',
    cpe.language = '*',
    cpe.part = 'a',
    cpe.source = 'vulncheck_nvd_plus',
    cpe.created_at = datetime()
ON MATCH SET
    cpe.updated_at = datetime()

WITH cpe
MATCH (cve:CVE {id: 'CVE-2021-44228'})
MERGE (cpe)-[r:AFFECTS]->(cve)
ON CREATE SET
    r.vulnerable_version_range = '>=2.0.0, <2.15.0',
    r.cvss_score = 10.0,
    r.severity = 'critical',
    r.source = 'vulncheck_nvd_plus',
    r.date_added = datetime();
```

#### 3.9 SBOM Component Risk Aggregation

```cypher
// Calculate aggregate vulnerability metrics for SBOM components
MATCH (sbom:SoftwareComponent)-[:MATCHES_CPE]->(cpe:CPE)-[:AFFECTS]->(cve:CVE)
WITH sbom,
     count(DISTINCT cve) AS vuln_cnt,
     sum(CASE WHEN cve.epss_score > 0.2 THEN 1 ELSE 0 END) AS high_risk_cnt,
     avg(cve.epss_score) AS avg_epss,
     collect(DISTINCT cve.priority_tier) AS priority_tiers
SET sbom.vuln_count = vuln_cnt,
    sbom.high_risk_vuln_count = high_risk_cnt,
    sbom.epss_avg = avg_epss,
    sbom.priority_tier = CASE
        WHEN 'NOW' IN priority_tiers THEN 'NOW'
        WHEN 'NEXT' IN priority_tiers THEN 'NEXT'
        ELSE 'NEVER'
    END,
    sbom.vulnerability_last_updated = datetime();

// Update CPE match count and confidence
MATCH (sbom:SoftwareComponent)-[r:MATCHES_CPE]->(cpe:CPE)
WITH sbom, count(r) AS match_cnt, avg(r.match_confidence) AS avg_conf
SET sbom.cpe_match_count = match_cnt,
    sbom.cpe_match_confidence_avg = avg_conf;
```

#### 3.10 Performance Considerations

**Query Performance Examples**:

```cypher
// Query 1: Find SBOM components with NOW-tier vulnerabilities (using denormalized property)
MATCH (sbom:SoftwareComponent)
WHERE sbom.priority_tier = 'NOW'
RETURN sbom.name, sbom.vendor, sbom.version, sbom.vuln_count, sbom.high_risk_vuln_count
ORDER BY sbom.high_risk_vuln_count DESC
LIMIT 50;
// Performance: ~100ms (index scan, no traversal)

// Query 2: SBOM component with full CVE details (multi-hop traversal)
MATCH path = (sbom:SoftwareComponent)-[:MATCHES_CPE]->(cpe:CPE)-[:AFFECTS]->(cve:CVE)
WHERE sbom.name = 'log4j'
  AND cve.priority_tier = 'NOW'
RETURN sbom.name, sbom.version, cve.id, cve.cvssScore, cve.epss_score, cve.priority_score
ORDER BY cve.priority_score DESC;
// Performance: ~300ms (index scan + 2-hop traversal + filtering)

// Query 3: SBOM dependency tree with vulnerability propagation
MATCH path = (root:SoftwareComponent {isRootComponent: true})
             -[:DEPENDS_ON*1..3]->(dep:SoftwareComponent)
             -[:MATCHES_CPE]->(:CPE)-[:AFFECTS]->(cve:CVE)
WHERE cve.priority_tier = 'NOW'
RETURN path, length(path) AS dependency_depth, cve.id, cve.priority_score
ORDER BY dependency_depth DESC, cve.priority_score DESC
LIMIT 20;
// Performance: ~1-2 seconds (variable-length path + multi-hop traversal + filtering)
```

**Batch Processing Performance**:
```cypher
// Batch CPE creation: 75,000 CPE nodes
// Estimated time: 10-15 minutes (constraint checks + property sets)

// Batch MATCHES_CPE creation: 145,000 relationships
// Estimated time: 15-20 minutes (index lookups + relationship creation)

// Batch AFFECTS creation: 650,000 relationships
// Estimated time: 30-40 minutes (index lookups + relationship creation)

// Total CPE matching pipeline: ~55-75 minutes
```

**Optimization Strategies**:
1. **Batch by Vendor**: Process CPE matching vendor-by-vendor to reduce search space
2. **Parallel Processing**: Use APOC periodic iterate with parallel: true
3. **Indexing**: Ensure all indexes built before relationship creation
4. **Caching**: Cache frequently accessed vendor/product combinations

---

## Combined Impact Summary

### Total Schema Changes (All 3 Recommendations)

| Category | Count | Details |
|----------|-------|---------|
| **New Node Types** | 2 | ExploitCode, CPE |
| **New Relationship Types** | 3 | HAS_EXPLOIT_CODE, MATCHES_CPE, AFFECTS |
| **Property Additions to CVE** | 27 | 16 (Rec 1) + 11 (Rec 2) |
| **Property Additions to SBOM** | 7 | Vulnerability summary properties |
| **Properties on ExploitCode** | 12 | All new node properties |
| **Properties on CPE** | 10 | All new node properties |
| **New Constraints** | 2 | ExploitCode.xdb_id, CPE.uri |
| **New Indexes** | 21 | 7 (Rec 1) + 8 (Rec 2) + 7 (Rec 3) |

### Total Data Volume Impact

| Metric | Value | Percentage of Existing DB (assumed 10GB) |
|--------|-------|------------------------------------------|
| **Nodes Added** | 88,000-127,000 | ExploitCode (20K) + CPE (75K) |
| **Relationships Added** | 635,000-985,000 | HAS_EXPLOIT_CODE (22.5K) + MATCHES_CPE (145K) + AFFECTS (650K) |
| **Property Values Added** | ~8.6M | CVE (7.2M) + SBOM (1.4M) + New nodes (0.5M) |
| **Estimated Storage Increase** | ~2 GB | Property data + relationships + indexes |
| **Percentage Increase** | ~20% | Significant but manageable |

### Total Implementation Effort

| Phase | Duration | Cumulative Time |
|-------|----------|-----------------|
| **Recommendation 1 Migration** | ~1 hour | 1 hour |
| **Recommendation 2 Migration** | ~20 minutes | 1h 20m |
| **Recommendation 3 Migration** | ~40 minutes | 2 hours |
| **Recommendation 3 CPE Matching** | ~1-2 hours | 3-4 hours |
| **Total Migration Time** | **3-4 hours** | All DDL + basic data population |

**Note**: Time estimates for schema changes only. Data enrichment (EPSS, KEV, XDB, CPE matching) requires additional ETL time (estimated 13 days development, see integration analysis document).

---

## Rollback Strategy

### Complete Rollback Script

```cypher
// ============================================
// COMPLETE ROLLBACK SCRIPT
// Reverts all 3 recommendations
// ============================================

// RECOMMENDATION 3 ROLLBACK
// Step 1: Remove SBOM property additions
MATCH (sbom:SoftwareComponent)
REMOVE sbom.vuln_count,
       sbom.high_risk_vuln_count,
       sbom.epss_avg,
       sbom.priority_tier,
       sbom.cpe_match_count,
       sbom.cpe_match_confidence_avg,
       sbom.vulnerability_last_updated;

// Step 2: Delete CPE nodes and relationships
MATCH (cpe:CPE)
DETACH DELETE cpe;

// Step 3: Drop CPE indexes
DROP INDEX cpe_vendor IF EXISTS;
DROP INDEX cpe_product IF EXISTS;
DROP INDEX cpe_version IF EXISTS;
DROP INDEX cpe_vendor_product IF EXISTS;
DROP INDEX sbom_vuln_count IF EXISTS;
DROP INDEX sbom_high_risk_vuln_count IF EXISTS;
DROP INDEX sbom_priority_tier IF EXISTS;

// Step 4: Drop CPE constraint
DROP CONSTRAINT cpe_uri IF EXISTS;

// RECOMMENDATION 2 ROLLBACK
// Step 5: Remove CVE property additions (Rec 2)
MATCH (cve:CVE)
REMOVE cve.exploit_available,
       cve.exploit_count,
       cve.has_weaponized_exploit,
       cve.attackerkb_score,
       cve.attackerkb_assessment_count,
       cve.attackerkb_topic_id,
       cve.attackerkb_rapid_7_assessed,
       cve.attackerkb_last_updated,
       cve.trending_rank,
       cve.hype_score,
       cve.trending_date;

// Step 6: Delete ExploitCode nodes and relationships
MATCH (ec:ExploitCode)
DETACH DELETE ec;

// Step 7: Drop ExploitCode indexes
DROP INDEX exploit_code_type IF EXISTS;
DROP INDEX exploit_code_maturity IF EXISTS;
DROP INDEX exploit_code_validated IF EXISTS;
DROP INDEX cve_exploit_available IF EXISTS;
DROP INDEX cve_has_weaponized_exploit IF EXISTS;
DROP INDEX cve_attackerkb_score IF EXISTS;
DROP INDEX cve_trending_rank IF EXISTS;
DROP INDEX has_exploit_code_threat_level IF EXISTS;

// Step 8: Drop ExploitCode constraint
DROP CONSTRAINT exploit_code_id IF EXISTS;

// RECOMMENDATION 1 ROLLBACK
// Step 9: Remove CVE property additions (Rec 1)
MATCH (cve:CVE)
REMOVE cve.epss_score,
       cve.epss_percentile,
       cve.epss_date,
       cve.epss_last_updated,
       cve.in_cisa_kev,
       cve.in_vulncheck_kev,
       cve.kev_date_added,
       cve.kev_due_date,
       cve.kev_required_action,
       cve.kev_ransomware_use,
       cve.exploited_in_wild,
       cve.kev_last_updated,
       cve.priority_tier,
       cve.priority_score,
       cve.priority_factors,
       cve.priority_reason,
       cve.priority_calculated_at;

// Step 10: Drop CVE indexes (Rec 1)
DROP INDEX cve_epss_score IF EXISTS;
DROP INDEX cve_epss_percentile IF EXISTS;
DROP INDEX cve_in_cisa_kev IF EXISTS;
DROP INDEX cve_in_vulncheck_kev IF EXISTS;
DROP INDEX cve_exploited_in_wild IF EXISTS;
DROP INDEX cve_priority_tier IF EXISTS;
DROP INDEX cve_priority_score IF EXISTS;

// VERIFICATION
// Check rollback completeness
MATCH (cve:CVE)
WHERE cve.id = 'CVE-2021-44228'
RETURN cve.id,
       exists(cve.epss_score) AS has_epss,
       exists(cve.priority_tier) AS has_priority,
       exists(cve.exploit_available) AS has_exploit_flag;
// Expected: All false

MATCH (ec:ExploitCode)
RETURN count(*) AS exploit_code_count;
// Expected: 0

MATCH (cpe:CPE)
RETURN count(*) AS cpe_count;
// Expected: 0

SHOW CONSTRAINTS YIELD name
WHERE name IN ['exploit_code_id', 'cpe_uri']
RETURN name;
// Expected: Empty result
```

**Rollback Execution Time**: ~15-20 minutes

---

## Testing & Validation

### Unit Test Queries

```cypher
// Test 1: Verify CVE property structure (Recommendation 1)
MATCH (cve:CVE)
WHERE cve.id = 'CVE-2021-44228'
RETURN cve.id,
       cve.epss_score,
       cve.in_cisa_kev,
       cve.priority_tier,
       exists(cve.priority_factors) AS has_priority_factors;

// Test 2: Verify ExploitCode node and relationship (Recommendation 2)
MATCH (cve:CVE {id: 'CVE-2021-44228'})-[r:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
RETURN cve.id, ec.xdb_id, ec.maturity, r.threat_level, r.confidence;

// Test 3: Verify CPE matching (Recommendation 3)
MATCH (sbom:SoftwareComponent {name: 'log4j', version: '2.14.1'})
      -[m:MATCHES_CPE]->(cpe:CPE)
      -[a:AFFECTS]->(cve:CVE)
RETURN sbom.name, sbom.version,
       cpe.uri,
       m.match_confidence, m.match_method,
       cve.id, cve.priority_tier;

// Test 4: Verify SBOM aggregate properties
MATCH (sbom:SoftwareComponent)
WHERE sbom.vuln_count > 0
RETURN sbom.name, sbom.version,
       sbom.vuln_count,
       sbom.high_risk_vuln_count,
       sbom.priority_tier
ORDER BY sbom.high_risk_vuln_count DESC
LIMIT 10;
```

### Integration Test Queries

```cypher
// Integration Test 1: End-to-end NOW-tier CVE query
MATCH (sbom:SoftwareComponent)-[:MATCHES_CPE]->(cpe:CPE)-[:AFFECTS]->(cve:CVE)
WHERE cve.priority_tier = 'NOW'
  AND cve.in_cisa_kev = true
OPTIONAL MATCH (cve)-[:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
RETURN sbom.name, sbom.version,
       cve.id, cve.cvssScore, cve.epss_score, cve.priority_score,
       count(ec) AS exploit_count,
       collect(ec.maturity) AS exploit_maturities
ORDER BY cve.priority_score DESC
LIMIT 20;

// Integration Test 2: Verify data completeness
MATCH (cve:CVE)
WITH count(*) AS total_cves,
     sum(CASE WHEN exists(cve.epss_score) THEN 1 ELSE 0 END) AS epss_enriched,
     sum(CASE WHEN cve.in_cisa_kev OR cve.in_vulncheck_kev THEN 1 ELSE 0 END) AS kev_flagged,
     sum(CASE WHEN exists(cve.priority_tier) THEN 1 ELSE 0 END) AS priority_classified
RETURN total_cves,
       epss_enriched,
       toFloat(epss_enriched) / total_cves * 100 AS epss_coverage_pct,
       kev_flagged,
       priority_classified,
       toFloat(priority_classified) / total_cves * 100 AS priority_coverage_pct;
// Expected: 100% EPSS coverage, ~0.7% KEV flagged, 100% priority classified

// Integration Test 3: Verify SBOM matching success rate
MATCH (sbom:SoftwareComponent)
WITH count(*) AS total_sbom,
     sum(CASE WHEN sbom.cpe_match_count > 0 THEN 1 ELSE 0 END) AS matched_sbom,
     sum(CASE WHEN sbom.vuln_count > 0 THEN 1 ELSE 0 END) AS sbom_with_vulns
RETURN total_sbom,
       matched_sbom,
       toFloat(matched_sbom) / total_sbom * 100 AS match_rate_pct,
       sbom_with_vulns,
       toFloat(sbom_with_vulns) / matched_sbom * 100 AS vuln_rate_pct;
// Expected: 60-85% match rate, varies % with vulnerabilities

// Integration Test 4: Performance benchmark
PROFILE
MATCH (cve:CVE)
WHERE cve.priority_tier = 'NOW'
  AND cve.epss_score > 0.7
  AND cve.in_cisa_kev = true
RETURN count(*);
// Expected: Uses indexes, db hits < 5000, time < 100ms
```

---

## Maintenance Operations

### Regular Maintenance Queries

```cypher
// Maintenance 1: Refresh SBOM vulnerability aggregates (weekly)
MATCH (sbom:SoftwareComponent)-[:MATCHES_CPE]->(cpe:CPE)-[:AFFECTS]->(cve:CVE)
WITH sbom,
     count(DISTINCT cve) AS vuln_cnt,
     sum(CASE WHEN cve.epss_score > 0.2 THEN 1 ELSE 0 END) AS high_risk_cnt,
     avg(cve.epss_score) AS avg_epss,
     collect(DISTINCT cve.priority_tier) AS priority_tiers
SET sbom.vuln_count = vuln_cnt,
    sbom.high_risk_vuln_count = high_risk_cnt,
    sbom.epss_avg = avg_epss,
    sbom.priority_tier = CASE
        WHEN 'NOW' IN priority_tiers THEN 'NOW'
        WHEN 'NEXT' IN priority_tiers THEN 'NEXT'
        ELSE 'NEVER'
    END,
    sbom.vulnerability_last_updated = datetime();

// Maintenance 2: Update CVE exploit summary properties (weekly)
MATCH (cve:CVE)
OPTIONAL MATCH (cve)-[:HAS_EXPLOIT_CODE]->(exploits:ExploitCode)
WITH cve, count(exploits) AS exploit_cnt,
     max(CASE WHEN exploits.maturity = 'weaponized' THEN 1 ELSE 0 END) AS has_weaponized
SET cve.exploit_available = (exploit_cnt > 0),
    cve.exploit_count = exploit_cnt,
    cve.has_weaponized_exploit = (has_weaponized = 1);

// Maintenance 3: Identify stale data (data older than 30 days)
MATCH (cve:CVE)
WHERE duration.between(cve.epss_last_updated, datetime()).days > 30
RETURN count(*) AS stale_epss_count;

MATCH (cve:CVE)
WHERE duration.between(cve.kev_last_updated, datetime()).days > 30
  AND (cve.in_cisa_kev OR cve.in_vulncheck_kev)
RETURN count(*) AS stale_kev_count;

// Maintenance 4: Index maintenance (check for missing indexes)
SHOW INDEXES YIELD name, type, state, populationPercent
WHERE state <> 'ONLINE' OR populationPercent < 100
RETURN name, type, state, populationPercent;
// Expected: Empty result (all indexes online and 100% populated)
```

### Database Statistics Queries

```cypher
// Statistics 1: Node and relationship counts
MATCH (n)
RETURN labels(n) AS label, count(*) AS count
ORDER BY count DESC;

MATCH ()-[r]->()
RETURN type(r) AS relationship_type, count(*) AS count
ORDER BY count DESC;

// Statistics 2: Storage size estimates (requires APOC)
CALL apoc.meta.stats() YIELD nodeCount, relCount, labelCount, propertyKeyCount, nodeTypeCount, relTypeCount
RETURN nodeCount, relCount, labelCount, propertyKeyCount, nodeTypeCount, relTypeCount;

// Statistics 3: Priority tier distribution
MATCH (cve:CVE)
RETURN cve.priority_tier AS tier,
       count(*) AS count,
       toFloat(count(*)) / 267487 * 100 AS percentage
ORDER BY CASE tier
  WHEN 'NOW' THEN 1
  WHEN 'NEXT' THEN 2
  WHEN 'NEVER' THEN 3
  ELSE 4
END;

// Statistics 4: SBOM vulnerability distribution
MATCH (sbom:SoftwareComponent)
WHERE sbom.vuln_count > 0
RETURN
  CASE
    WHEN sbom.vuln_count = 0 THEN '0 vulns'
    WHEN sbom.vuln_count <= 5 THEN '1-5 vulns'
    WHEN sbom.vuln_count <= 10 THEN '6-10 vulns'
    WHEN sbom.vuln_count <= 20 THEN '11-20 vulns'
    ELSE '20+ vulns'
  END AS vuln_range,
  count(*) AS component_count
ORDER BY vuln_range;
```

---

## Production Deployment Checklist

### Pre-Deployment

- [ ] **Backup Database**: Full Neo4j backup before any schema changes
- [ ] **Test in Non-Production**: Execute all DDL in dev/staging environment first
- [ ] **Verify Disk Space**: Ensure ~2GB free space for schema additions
- [ ] **Review Indexes**: Confirm all indexes are necessary and not duplicated
- [ ] **Performance Baseline**: Run benchmark queries before changes

### Deployment

- [ ] **Execute Recommendation 1 DDL**: Property additions + indexes
- [ ] **Validate Recommendation 1**: Run test queries
- [ ] **Execute Recommendation 2 DDL**: ExploitCode node type + relationships
- [ ] **Validate Recommendation 2**: Verify constraint and indexes
- [ ] **Execute Recommendation 3 DDL**: CPE node type + SBOM properties
- [ ] **Validate Recommendation 3**: Check CPE structure

### Post-Deployment

- [ ] **Verify All Indexes Online**: Check index population status
- [ ] **Run Integration Tests**: Execute end-to-end test queries
- [ ] **Performance Validation**: Compare query times to baseline
- [ ] **Monitor Database Metrics**: CPU, memory, disk I/O for anomalies
- [ ] **Document Changes**: Update schema documentation with version

### Rollback Plan

- [ ] **Rollback Script Ready**: Keep complete rollback script accessible
- [ ] **Rollback Trigger**: Define conditions for rollback (e.g., >10% performance degradation)
- [ ] **Communication Plan**: Notify stakeholders of deployment status

---

## Summary & Recommendations

### Recommendation Priorities

Based on complexity, impact, and effort:

| Rank | Recommendation | Complexity | Effort | Impact | Priority |
|------|----------------|------------|--------|--------|----------|
| **1** | Essential Exploitability | 🟢 LOW | 1 hour | 🟢 VERY HIGH | **IMMEDIATE** |
| **2** | Advanced Threat Intel | 🟡 MEDIUM | 20 min | 🟡 HIGH | **Phase 2** |
| **3** | SBOM CPE Matching | 🟠 MEDIUM-HIGH | 2 hours | 🟢 VERY HIGH | **Phase 3** |

### Implementation Approach

**Sequential Phased Deployment** (Recommended):
1. **Week 1**: Recommendation 1 (schema + data enrichment)
2. **Week 2**: Recommendation 2 (schema + data enrichment)
3. **Week 3-4**: Recommendation 3 (schema + CPE matching)

**Benefits**:
- Validate each phase before proceeding
- Incremental value delivery (NOW/NEXT/NEVER available after Week 1)
- Easier rollback if issues detected

### Key Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| **Index creation locks database** | Schedule during low-usage window, use background index creation if available |
| **Property additions slow writes** | Batch operations, monitor write performance, adjust batch sizes |
| **CPE matching produces false positives** | Manual validation of sample matches, tune confidence thresholds |
| **Storage growth exceeds estimates** | Monitor disk usage, provision additional storage proactively |
| **Query performance degradation** | Verify all indexes online, analyze slow queries with PROFILE |

---

## Document Status

- **File Location**: `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DR_Cybersec_Threat_Intelv2/SCHEMA_CHANGE_SPECIFICATIONS.md`
- **Total Impact Summary**:
  - **2 new node types** (ExploitCode, CPE)
  - **3 new relationship types** (HAS_EXPLOIT_CODE, MATCHES_CPE, AFFECTS)
  - **46 property additions** across CVE, SBOM, ExploitCode, CPE nodes
  - **21 new indexes**
  - **2 new constraints**
  - **~2GB storage increase** (~20% of existing DB)
  - **3-4 hours total migration time** (schema changes only)

- **Ready for Implementation**: ✅ All DDL specifications complete
- **Next Steps**:
  1. Review DDL with database administrator
  2. Execute in non-production environment for validation
  3. Schedule production deployment window
  4. Begin Phase 1 data enrichment (EPSS + KEV) after schema deployment

**Document Prepared By**: Schema-Architect Agent
**Date**: 2025-11-01
**Version**: 1.0.0
