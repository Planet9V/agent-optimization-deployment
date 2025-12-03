# PROCEDURE: [PROC-001] Schema Migration and Constraint Setup

**Procedure ID**: PROC-001
**Version**: 1.0.0
**Created**: 2025-11-26
**Last Modified**: 2025-11-26
**Author**: AEON ETL Agent System
**Status**: APPROVED

---

## 1. METADATA

| Field | Value |
|-------|-------|
| **Category** | SCHEMA |
| **Frequency** | ON-DEMAND (schema changes) |
| **Priority** | CRITICAL |
| **Estimated Duration** | 15-30 minutes |
| **Risk Level** | MEDIUM |
| **Rollback Available** | PARTIAL |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Initialize and maintain the Neo4j schema for the AEON Cyber Digital Twin by creating constraints, indexes, and verifying the 8-layer architecture. **This procedure MUST run before any other ETL procedures.**

### 2.2 Business Objectives
- [x] Create all uniqueness constraints for node types
- [x] Create performance indexes for query optimization
- [x] Verify schema compliance with 8-layer architecture
- [x] Enable multi-tenant support via customer_namespace

### 2.3 Schema Layers (8-Layer Architecture)

| Layer | Node Types | Purpose |
|-------|-----------|---------|
| L0 | Asset, Device | Physical infrastructure |
| L1 | NetworkDevice, Subnet | Network topology |
| L2 | Software, CPE | Software inventory |
| L3 | CVE, CWE | Vulnerability data |
| L4 | CAPEC, Technique | Attack patterns |
| L5 | ThreatActor, Campaign | Threat intelligence |
| L6 | FailureScenario | Risk modeling |
| L7 | Mitigation, Patch | Defense measures |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running | `docker ps \| grep neo4j` |
| Disk Space | > 2GB free | `docker exec neo4j df -h /data` |

### 3.2 Prior Procedures Required

**NONE** - This is the first procedure in the pipeline.

---

## 4. SCHEMA DEFINITIONS

### 4.1 Uniqueness Constraints

```cypher
// Layer 3 - Vulnerability
CREATE CONSTRAINT cve_id_unique IF NOT EXISTS FOR (c:CVE) REQUIRE c.cve_id IS UNIQUE;
CREATE CONSTRAINT cpe_uri_unique IF NOT EXISTS FOR (c:CPE) REQUIRE c.cpe_uri IS UNIQUE;
CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS FOR (c:CWE) REQUIRE c.id IS UNIQUE;

// Layer 4 - Attack Surface
CREATE CONSTRAINT capec_pattern_id IF NOT EXISTS FOR (c:CAPEC) REQUIRE c.capec_id IS UNIQUE;
CREATE CONSTRAINT technique_id_unique IF NOT EXISTS FOR (t:Technique) REQUIRE t.technique_id IS UNIQUE;

// Layer 5 - Organizational
CREATE CONSTRAINT actor_id_unique IF NOT EXISTS FOR (a:ThreatActor) REQUIRE a.actor_id IS UNIQUE;
CREATE CONSTRAINT profile_id_unique IF NOT EXISTS FOR (p:ThreatActorProfile) REQUIRE p.profile_id IS UNIQUE;

// Layer 0 - Physical
CREATE CONSTRAINT asset_id_unique IF NOT EXISTS FOR (a:Asset) REQUIRE a.asset_id IS UNIQUE;

// Layer 7 - Mitigation
CREATE CONSTRAINT mitigation_id_unique IF NOT EXISTS FOR (m:Mitigation) REQUIRE m.mitigation_id IS UNIQUE;
```

### 4.2 Performance Indexes

```cypher
// CVE indexes
CREATE INDEX cve_severity_idx IF NOT EXISTS FOR (c:CVE) ON (c.cvssV3Severity);
CREATE INDEX cve_score_idx IF NOT EXISTS FOR (c:CVE) ON (c.cvssV3BaseScore);
CREATE INDEX cve_enriched_idx IF NOT EXISTS FOR (c:CVE) ON (c.enriched_timestamp);

// CPE indexes
CREATE INDEX cpe_vendor_idx IF NOT EXISTS FOR (c:CPE) ON (c.vendor);
CREATE INDEX cpe_product_idx IF NOT EXISTS FOR (c:CPE) ON (c.product);

// Name indexes
CREATE INDEX cwe_name_idx IF NOT EXISTS FOR (c:CWE) ON (c.name);
CREATE INDEX capec_name_idx IF NOT EXISTS FOR (c:CAPEC) ON (c.name);
CREATE INDEX technique_name_idx IF NOT EXISTS FOR (t:Technique) ON (t.name);
CREATE INDEX actor_name_idx IF NOT EXISTS FOR (a:ThreatActor) ON (a.name);

// Multi-tenant support
CREATE INDEX cve_namespace_idx IF NOT EXISTS FOR (c:CVE) ON (c.customer_namespace);
```

---

## 5. EXECUTION STEPS

### Step 1: Verify Neo4j Connectivity
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1 AS test"
```

### Step 2: List Existing Constraints
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "SHOW CONSTRAINTS"
```

### Step 3: Create Constraints
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" <<'CYPHER'
CREATE CONSTRAINT cve_id_unique IF NOT EXISTS FOR (c:CVE) REQUIRE c.cve_id IS UNIQUE;
CREATE CONSTRAINT cpe_uri_unique IF NOT EXISTS FOR (c:CPE) REQUIRE c.cpe_uri IS UNIQUE;
CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS FOR (c:CWE) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT capec_pattern_id IF NOT EXISTS FOR (c:CAPEC) REQUIRE c.capec_id IS UNIQUE;
CREATE CONSTRAINT technique_id_unique IF NOT EXISTS FOR (t:Technique) REQUIRE t.technique_id IS UNIQUE;
CREATE CONSTRAINT actor_id_unique IF NOT EXISTS FOR (a:ThreatActor) REQUIRE a.actor_id IS UNIQUE;
CYPHER
```

### Step 4: Create Indexes
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" <<'CYPHER'
CREATE INDEX cve_severity_idx IF NOT EXISTS FOR (c:CVE) ON (c.cvssV3Severity);
CREATE INDEX cve_score_idx IF NOT EXISTS FOR (c:CVE) ON (c.cvssV3BaseScore);
CREATE INDEX cpe_vendor_idx IF NOT EXISTS FOR (c:CPE) ON (c.vendor);
CREATE INDEX technique_name_idx IF NOT EXISTS FOR (t:Technique) ON (t.name);
CYPHER
```

### Step 5: Verify Schema Setup
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "SHOW CONSTRAINTS YIELD name RETURN count(*) AS constraint_count"
```

---

## 6. POST-EXECUTION VERIFICATION

```cypher
SHOW CONSTRAINTS YIELD name, type, labelsOrTypes, properties
RETURN name, type, labelsOrTypes, properties ORDER BY name;
```

### Success Criteria

| Criterion | Threshold |
|-----------|-----------|
| Constraints created | >= 9 |
| Indexes created | >= 12 |
| All indexes ONLINE | 100% |

---

## 7. ROLLBACK PROCEDURE

**WARNING**: Dropping constraints may fail if data exists.

```cypher
DROP CONSTRAINT cve_id_unique IF EXISTS;
DROP CONSTRAINT cpe_uri_unique IF EXISTS;
DROP CONSTRAINT cwe_id_unique IF EXISTS;
DROP CONSTRAINT capec_pattern_id IF EXISTS;
DROP CONSTRAINT technique_id_unique IF EXISTS;
DROP CONSTRAINT actor_id_unique IF EXISTS;
```

---

## 8. SCHEDULING

This procedure runs:
- **Initial setup**: Once per environment
- **Schema changes**: When adding new node types
- **Post-recovery**: After database restore

### Pipeline Position
```
PROC-001 (THIS - FIRST) → PROC-101 → PROC-201 → PROC-301 → PROC-501 → PROC-901
```

---

## 9. COMPLETE SCRIPT

```bash
#!/bin/bash
# PROCEDURE: PROC-001 - Schema Migration
set -e

NEO4J_CONTAINER="${NEO4J_CONTAINER:-openspg-neo4j}"
NEO4J_PASS="${NEO4J_PASSWORD:-neo4j@openspg}"

cypher_query() {
    docker exec "$NEO4J_CONTAINER" cypher-shell -u neo4j -p "$NEO4J_PASS" "$1"
}

echo "[INFO] Starting PROC-001: Schema Migration"

# Constraints
cypher_query "CREATE CONSTRAINT cve_id_unique IF NOT EXISTS FOR (c:CVE) REQUIRE c.cve_id IS UNIQUE"
cypher_query "CREATE CONSTRAINT cpe_uri_unique IF NOT EXISTS FOR (c:CPE) REQUIRE c.cpe_uri IS UNIQUE"
cypher_query "CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS FOR (c:CWE) REQUIRE c.id IS UNIQUE"
cypher_query "CREATE CONSTRAINT capec_pattern_id IF NOT EXISTS FOR (c:CAPEC) REQUIRE c.capec_id IS UNIQUE"
cypher_query "CREATE CONSTRAINT technique_id_unique IF NOT EXISTS FOR (t:Technique) REQUIRE t.technique_id IS UNIQUE"
cypher_query "CREATE CONSTRAINT actor_id_unique IF NOT EXISTS FOR (a:ThreatActor) REQUIRE a.actor_id IS UNIQUE"

# Indexes
cypher_query "CREATE INDEX cve_severity_idx IF NOT EXISTS FOR (c:CVE) ON (c.cvssV3Severity)"
cypher_query "CREATE INDEX cve_score_idx IF NOT EXISTS FOR (c:CVE) ON (c.cvssV3BaseScore)"
cypher_query "CREATE INDEX cpe_vendor_idx IF NOT EXISTS FOR (c:CPE) ON (c.vendor)"

echo "[INFO] PROC-001 completed successfully"
```

---

## 10. CHANGE HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-26 | Initial version |

---

**End of Procedure PROC-001**
