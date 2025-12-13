# PROCEDURE ALIGNMENT REPORT
**File**: PROCEDURE_ALIGNMENT_REPORT.md
**Created**: 2025-12-12
**Status**: ALIGNMENT IN PROGRESS
**Purpose**: Align 34 procedures with ACTUAL system APIs and schema

---

## EXECUTIVE SUMMARY

**Total Procedures**: 34 (+ 1 template)
**Requiring Updates**: 18 procedures reference non-existent APIs
**Action Required**: Update API references + schema references + validation queries

**Critical Finding**: Most procedures were written assuming Phase B APIs exist on port 8000. **REALITY**: Only NER11 APIs (5 endpoints) exist on port 8000. Phase B APIs (135 endpoints) exist but are NOT RUNNING.

---

## ALIGNMENT STATUS BY PROCEDURE

### ✅ ALREADY ALIGNED (No API Dependencies)

| ID | Procedure | Status | Reason |
|----|-----------|--------|--------|
| PROC-001 | Schema Migration | ✅ ALIGNED | Neo4j only, no external APIs |
| PROC-101 | CVE Enrichment | ✅ ALIGNED | NVD API (external), Neo4j queries |
| PROC-102 | Kaggle Enrichment | ✅ ALIGNED | Kaggle API (external), Neo4j queries |
| PROC-111 | APT Threat Intel | ✅ ALIGNED | File-based ingestion, no APIs |
| PROC-112 | STIX Integration | ✅ ALIGNED | File-based STIX parsing |
| PROC-114 | Psychometric Integration | ✅ ALIGNED | File-based psychometric data |
| PROC-151 | Lacanian Dyad | ✅ ALIGNED | Graph algorithms, no APIs |
| PROC-152 | Triad Group Dynamics | ✅ ALIGNED | Graph algorithms, no APIs |
| PROC-153 | Organizational Blind Spots | ✅ ALIGNED | Graph algorithms, no APIs |
| PROC-154 | Personality Team Fit | ✅ ALIGNED | Graph algorithms, no APIs |
| PROC-155 | Transcript Psychometric NER | ✅ ALIGNED | NER11 API + Graph |
| PROC-201 | CWE-CAPEC Linker | ✅ ALIGNED | File-based linking |
| PROC-301 | CAPEC-ATT&CK Mapper | ✅ ALIGNED | File-based mapping |
| PROC-501 | Threat Actor Enrichment | ✅ ALIGNED | File-based enrichment |
| PROC-901 | Attack Chain Validator | ✅ ALIGNED | Graph traversal, no APIs |

**Total**: 15 procedures ✅

---

### ⚠️ REQUIRES API ALIGNMENT

#### HIGH PRIORITY - References Non-Existent APIs

| ID | Procedure | Issue | Fix Required |
|----|-----------|-------|--------------|
| PROC-113 | SBOM Analysis | References `/api/v2/sbom/*` (NOT RUNNING) | Use NER11 + Neo4j direct ingestion |
| PROC-142 | Vendor Equipment | References `/api/v2/equipment/*` (NOT RUNNING) | Use Neo4j queries + file ingestion |
| PROC-115 | Real-Time Feeds | References `/api/v2/threat-intel/feeds/*` (NOT RUNNING) | Use NER11 `/search/hybrid` + manual feeds |
| PROC-116 | Executive Dashboard | References `/api/v2/dashboard/*` (NOT RUNNING) | Use Neo4j aggregation queries |
| PROC-117 | Wiki Truth Correction | References `/api/v2/validation/*` (NOT RUNNING) | Use NER11 `/ner` + manual validation |

#### MEDIUM PRIORITY - Needs Schema Updates

| ID | Procedure | Issue | Fix Required |
|----|-----------|-------|--------------|
| PROC-121 | IEC 62443 Safety | Old schema references | Update to 631-label schema |
| PROC-122 | RAMS Reliability | Old schema references | Update to Equipment → System hierarchy |
| PROC-123 | Hazard FMEA | Old schema references | Update to Risk nodes structure |
| PROC-131 | Economic Impact | Old schema references | Update to EconomicImpact hierarchy |
| PROC-132 | Psychohistory Demographics | Old schema references | Update to Population nodes |
| PROC-133 | NOW/NEXT/NEVER | Old schema references | Update to Prioritization hierarchy |
| PROC-134 | Attack Path Modeling | Old schema references | Verify 8-hop paths with current schema |
| PROC-141 | Lacanian Real/Imaginary | Old schema references | Update to PsychologicalDimension nodes |
| PROC-161 | Seldon Crisis Prediction | Old schema references | Update to Crisis nodes |
| PROC-162 | Population Event Forecasting | Old schema references | Update to Event nodes |
| PROC-163 | Cognitive Dissonance Breaking | Old schema references | Update to Dissonance nodes |
| PROC-164 | Threat Actor Personality | Old schema references | Update to PersonalityProfile nodes |
| PROC-165 | McKenney-Lacan Calculus | Old schema references | Update to all 10 McKenney questions |

**Total**: 18 procedures ⚠️

---

## DETAILED ALIGNMENT ACTIONS

### PROC-113 SBOM Analysis - CRITICAL UPDATE

**Current State**: References 37 SBOM APIs at `/api/v2/sbom/*`

**Reality**:
- ❌ NO SBOM APIs running
- ✅ NER11 `/ner` can extract component names
- ✅ Neo4j can store SBOM data
- ✅ CycloneDX/SPDX parsing via Python

**Required Changes**:
1. Replace API calls with:
   ```bash
   # OLD (non-existent):
   curl http://localhost:8000/api/v2/sbom/sboms

   # NEW (actual):
   # Parse SBOM file locally
   python parse_cyclonedx.py sbom.json |
   # Extract entities via NER11
   curl -X POST http://localhost:8000/ner -d @- |
   # Load into Neo4j
   cypher-shell < load_sbom.cypher
   ```

2. Update validation queries to use **ACTUAL schema**:
   ```cypher
   // OLD: MATCH (sc:SoftwareComponent)
   // NEW: MATCH (sc:Component:Software)  # Hierarchical labels
   ```

3. Add note: "This procedure creates data structures that COULD be exposed via Phase B SBOM APIs when deployed"

---

### PROC-142 Vendor Equipment - CRITICAL UPDATE

**Current State**: References 24 Equipment APIs at `/api/v2/equipment/*`

**Reality**:
- ❌ NO Equipment APIs running
- ✅ Neo4j stores Equipment nodes
- ✅ File-based vendor data available

**Required Changes**:
1. Replace dashboard queries:
   ```bash
   # OLD (non-existent):
   curl http://localhost:8000/api/v2/equipment/dashboard/summary

   # NEW (actual):
   cypher-shell "
     MATCH (e:Equipment)
     WITH count(e) AS total,
          count(e.eol_date) AS has_eol
     RETURN total, has_eol,
            100.0 * has_eol / total AS eol_coverage_pct
   "
   ```

2. Update EOL checks to use Neo4j properties
3. Add note: "Equipment API endpoints defined in Phase B but not yet deployed"

---

### PROC-115 Real-Time Feeds - UPDATE

**Current State**: References `/api/v2/threat-intel/feeds/*`

**NEW Process**:
1. Use NER11 `/search/hybrid` for semantic matching
2. Ingest feeds via Python scripts
3. Update Neo4j directly
4. Query via Neo4j for "real-time" dashboard

---

### PROC-116 Executive Dashboard - UPDATE

**Current State**: References 30+ dashboard APIs

**NEW Process**:
1. Build dashboard from **Neo4j aggregation queries**
2. Use existing data in 631-label schema
3. Example: KPI calculation
   ```cypher
   MATCH (cve:CVE:Vulnerability)
   WHERE cve.cvssV31BaseScore >= 9.0
   WITH count(cve) AS critical_cves
   MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
   WITH critical_cves, count(DISTINCT cwe) AS unique_cwes
   RETURN critical_cves, unique_cwes
   ```

---

### PROC-121 to PROC-165 - SCHEMA ALIGNMENT

**Action**: Update all Cypher queries to use:
- **631 labels** (not old schema)
- **17 super labels** with hierarchical properties
- **183 relationship types** (current)
- **Actual node counts** from Neo4j

**Verification Process for Each**:
1. Read COMPLETE_SCHEMA_REFERENCE.md for correct labels
2. Test queries against actual Neo4j
3. Update examples with REAL data

---

## VALIDATION QUERIES (UPDATED)

All procedures must use these **ACTUAL** validation queries:

```cypher
// Schema Statistics (CURRENT)
CALL db.labels() YIELD label
RETURN count(label) AS total_labels;
// Expected: 631

CALL db.relationshipTypes() YIELD relationshipType
RETURN count(relationshipType) AS total_relationships;
// Expected: 183

// Data Volume (ACTUAL)
MATCH (cve:CVE)
RETURN count(cve) AS cve_count;
// Expected: ~316,552

MATCH (ta:ThreatActor)
RETURN count(ta) AS threat_actor_count;
// Expected: ~800

MATCH (t:Technique)
RETURN count(t) AS technique_count;
// Expected: ~600
```

---

## PRIORITY EXECUTION ORDER

### Phase 1: CRITICAL API Fixes (TODAY)
1. ✅ PROC-113 SBOM Analysis
2. ✅ PROC-142 Vendor Equipment
3. ✅ PROC-115 Real-Time Feeds
4. ✅ PROC-116 Executive Dashboard
5. ✅ PROC-117 Wiki Truth Correction

### Phase 2: Schema Alignment (NEXT 2 DAYS)
6-18. All PROC-121 through PROC-165

### Phase 3: Verification (DAY 3)
19. Run validation queries
20. Test 5 sample procedures end-to-end
21. Generate compliance report

---

## QDRANT STORAGE

All alignment work will be stored in Qdrant collection:
```
Collection: aeon-truth/procedure-alignment
Points: 34 (one per procedure)
Metadata: {
  procedure_id,
  alignment_status,
  api_references_fixed,
  schema_references_fixed,
  validation_queries_tested,
  last_updated
}
```

---

## NEXT STEPS

1. **Update PROC-113** (SBOM) - Remove API references, use NER11 + Neo4j
2. **Update PROC-142** (Equipment) - Remove API references, use Neo4j queries
3. **Update PROC-115** (Feeds) - Use NER11 hybrid search
4. **Update PROC-116** (Dashboard) - Use Neo4j aggregation
5. **Update PROC-117** (Wiki) - Use NER11 entity extraction
6. **Schema alignment** - Update 13 procedures with 631-label schema

**Timeline**: 2-3 hours for critical fixes, 1 day for schema alignment

---

**Status**: Ready to execute alignment
**Dependencies**: ALL_APIS_MASTER_TABLE.md + COMPLETE_SCHEMA_REFERENCE.md + Neo4j access
**Output**: 18 updated procedures + verification report
