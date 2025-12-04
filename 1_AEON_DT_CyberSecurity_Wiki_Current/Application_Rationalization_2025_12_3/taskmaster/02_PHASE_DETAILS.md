# PHASE DETAILS - Option B: Balanced Foundation MVP

**Version:** 1.0.1
**Last Updated:** 2025-12-04T03:20:00Z
**Decision:** OPTION B Selected
**Total MVP Duration:** 62 Days
**Total MVP Enhancements:** 6

---

## Decision Rationale

**Option B: Balanced Foundation MVP** was selected for the following reasons:

1. **Clean Architecture** - No tech debt from skipping foundational work
2. **SBOM Dependency Graphs** - High-visibility frontend feature (npm/PyPI visualization)
3. **Real Economic Data** - IBM Breach Report, FRED API integration
4. **NOW/NEXT/NEVER** - 99.8% CVE reduction for actionable prioritization
5. **Frontend-First** - All 6 enhancements have visible UI components

---

## MVP Timeline Overview

```
Phase B1: Foundation     [Day 1-20]    ████████████████████░░░░░░░░░░ 20 days
Phase B2: Supply Chain   [Day 21-44]   ░░░░░░░░░░░░░░░░░░░░████████████████████████ 24 days
Phase B3: Prioritization [Day 45-62]   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████████████████ 18 days
```

---

## Phase B1: Structural Foundation

**Duration:** Days 1-20 (20 days)
**Goal:** Establish multi-tenant isolation and industrial safety classification
**Status:** NOT STARTED
**Priority:** CRITICAL

### Enhancements in This Phase

| Order | Enhancement | Days | ICE | Priority | Dependencies |
|-------|-------------|------|-----|----------|--------------|
| 1 | Customer Labels (Multi-Tenant) | 5 | 9.5 | CRITICAL | None |
| 2 | E07 IEC 62443 Safety | 15 | 8.7 | CRITICAL | Customer Labels |

### CUSTOMER_LABELS - Multi-Tenant Isolation (Days 1-5)

**Objective:** Implement comprehensive multi-tenant security framework

**Key Deliverables:**
1. `CustomerLabel` node type in Neo4j
2. `BELONGS_TO_CUSTOMER` relationships
3. Customer isolation middleware
4. Query filters for customer context
5. Audit trail per customer

**Frontend Components:**
- Customer selector dropdown
- Data isolation indicators
- Customer-scoped dashboards

**Tests Required:**
- Unit: Schema validation
- Integration: Cross-customer isolation
- Security: Data leakage prevention

**Acceptance Criteria:**
- GIVEN a query with customer context
- WHEN executed against Neo4j
- THEN only data belonging to that customer is returned

---

### E07 - IEC 62443 Industrial Safety Integration (Days 6-20)

**Objective:** Implement IEC 62443 safety zone architecture

**Key Deliverables:**
1. `SecurityZone` node type (SL0-SL4)
2. `Conduit` relationship modeling
3. FR1-FR7 compliance tracking
4. SL-C vs SL-T gap analysis queries
5. Equipment certification status
6. ROI-optimized remediation roadmap

**Frontend Components:**
- Safety zone hierarchy display
- SL level badges (SL0-SL4)
- Compliance gap indicators
- Zone-based filtering

**Data Sources:**
- IEC 62443 documentation (7 source files)

**Tests Required:**
- Unit: Zone assignment
- Integration: Equipment mapping
- Acceptance: Compliance validation

---

### Phase B1 Milestone Criteria

- [ ] CustomerLabel nodes created and validated
- [ ] Customer isolation middleware deployed
- [ ] Cross-customer data leakage tests passing
- [ ] SecurityZone hierarchy established (SL0-SL4)
- [ ] Equipment mapped to zones
- [ ] Compliance gap queries functional
- [ ] Frontend customer selector working
- [ ] Safety zone badges displaying

### Rollback Procedures

1. **Customer Labels Rollback:**
   ```cypher
   MATCH (n) REMOVE n.customer_id
   ```

2. **E07 Safety Rollback:**
   ```cypher
   MATCH (sz:SecurityZone) DETACH DELETE sz
   MATCH (n) REMOVE n.safety_level, n.iec_zone
   ```

---

## Phase B2: Supply Chain

**Duration:** Days 21-44 (24 days)
**Goal:** Vendor tracking and SBOM analysis for complete supply chain visibility
**Status:** NOT STARTED
**Priority:** HIGH

### Enhancements in This Phase

| Order | Enhancement | Days | ICE | Priority | Dependencies |
|-------|-------------|------|-----|----------|--------------|
| 3 | E15 Vendor Equipment Tracking | 12 | 7.0 | HIGH | CUSTOMER_LABELS, E07 |
| 4 | E03 SBOM Dependency Analysis | 12 | 8.0 | HIGH | E15 |

### E15 - Vendor Equipment Tracking (Days 21-32)

**Objective:** Enable supply chain risk management through vendor tracking

**Key Deliverables:**
1. `Vendor` node type in Neo4j
2. `MANUFACTURED_BY` relationships
3. Vendor-vulnerability correlation
4. Equipment lifecycle tracking
5. Vendor risk scoring

**Frontend Components:**
- Vendor filter dropdowns
- Vendor risk badges
- Equipment-vendor relationships

**Data Sources:**
- Existing equipment nodes (29,774)
- Vendor catalogs

**Tests Required:**
- Unit: Vendor CRUD operations
- Integration: Equipment linking
- Acceptance: Coverage >95%

---

### E03 - SBOM Dependency Analysis (Days 33-44)

**Objective:** Software Bill of Materials for supply chain vulnerability detection

**Key Deliverables:**
1. SBOM ingestion framework (CycloneDX, SPDX)
2. `Package` node type
3. `DEPENDS_ON` relationships (transitive)
4. CVE-to-package correlation
5. Vulnerability impact analysis
6. Remediation roadmap generator

**Frontend Components:**
- SBOM dependency graph visualization
- Package vulnerability indicators
- Transitive dependency explorer

**Data Sources:**
- npm Registry API
- PyPI API
- NVD
- OSV
- GHSA

**Tests Required:**
- Unit: SBOM parsing (CycloneDX, SPDX)
- Integration: CVE correlation
- Acceptance: 316K CVE coverage

---

### Phase B2 Milestone Criteria

- [ ] Vendor nodes created (>95% equipment coverage)
- [ ] MANUFACTURED_BY relationships established
- [ ] Vendor risk scores calculated
- [ ] SBOM ingestion pipeline functional
- [ ] Package dependency graphs in Neo4j
- [ ] CVE-to-package correlation working
- [ ] Frontend vendor filters operational
- [ ] SBOM graph visualization rendering

### Rollback Procedures

1. **E15 Vendor Rollback:**
   ```cypher
   MATCH (v:Vendor) DETACH DELETE v
   ```

2. **E03 SBOM Rollback:**
   ```cypher
   MATCH (p:Package) DETACH DELETE p
   MATCH (s:SBOM) DETACH DELETE s
   ```

---

## Phase B3: Prioritization

**Duration:** Days 45-62 (18 days)
**Goal:** Economic modeling and actionable CVE prioritization
**Status:** NOT STARTED
**Priority:** HIGH

### Enhancements in This Phase

| Order | Enhancement | Days | ICE | Priority | Dependencies |
|-------|-------------|------|-----|----------|--------------|
| 5 | E10 Economic Impact Analysis | 10 | 7.8 | HIGH | E03, E15 |
| 6 | E12 NOW/NEXT/NEVER | 8 | 8.5 | CRITICAL | E10, E03 |

### E10 - Economic Impact Analysis (Days 45-54)

**Objective:** Quantify breach costs and ROI for security investments

**Key Deliverables:**
1. Breach cost calculator
2. ROI modeling functions
3. Sector-specific impact estimates
4. Investment prioritization framework
5. Economic impact dashboards

**Frontend Components:**
- Economic impact dashboard
- ROI calculator widget
- Sector comparison charts

**Data Sources:**
- IBM Breach Report 2025 ($4.44M avg)
- FRED API
- World Bank indicators
- Kaggle breach datasets

**Tests Required:**
- Unit: Cost calculations
- Integration: Sector mapping
- Acceptance: ROI validation

---

### E12 - NOW/NEXT/NEVER Prioritization (Days 55-62)

**Objective:** Reduce 316K CVEs to actionable priorities

**Key Deliverables:**
1. NOW/NEXT/NEVER scoring algorithm
2. `PriorityAssessment` node type
3. 5.06M assessment nodes (316K × 16 sectors)
4. Cognitive bias integration
5. Sector-specific thresholds
6. Resource allocation optimization

**Frontend Components:**
- NOW/NEXT/NEVER CVE table
- Priority badges (NOW=red, NEXT=yellow, NEVER=gray)
- Sector-specific views
- Action queue

**Data Sources:**
- NVD CVSS
- EPSS scores
- Organizational profiles

**Tests Required:**
- Unit: Scoring algorithm
- Integration: CVE correlation
- Acceptance: 99.8% NEVER rate validation

---

### Phase B3 Milestone Criteria

- [ ] Economic calculations deployed
- [ ] ROI dashboard functional
- [ ] Sector mappings complete
- [ ] NOW/NEXT/NEVER algorithm implemented
- [ ] 5.06M assessment nodes created
- [ ] 99.8% NEVER rate achieved
- [ ] Priority CVE table rendering
- [ ] Action queue functional

### Rollback Procedures

1. **E10 Economic Rollback:**
   ```cypher
   MATCH (n) REMOVE n.economic_impact, n.dollar_risk, n.roi_score
   ```

2. **E12 N/N/N Rollback:**
   ```cypher
   MATCH (pa:PriorityAssessment) DETACH DELETE pa
   MATCH (n) REMOVE n.priority_class, n.now_next_never
   ```

---

## MVP Completion Criteria

### Technical Requirements
- [ ] All 6 MVP enhancements deployed
- [ ] Unit tests passing (>90% coverage)
- [ ] Integration tests passing
- [ ] Security tests passing (0 data leaks)
- [ ] Performance benchmarks met (<50ms queries)

### Frontend Requirements
- [ ] Customer selector functional
- [ ] Safety zone badges displaying
- [ ] SBOM graph interactive
- [ ] Economic dashboard showing data
- [ ] NOW/NEXT/NEVER table sorting

### Business Requirements
- [ ] Customer isolation verified
- [ ] IEC 62443 compliance visible
- [ ] Supply chain risk quantified
- [ ] CVE overload reduced by 99.8%
- [ ] ROI calculable

---

## Deferred Phases (Post-MVP)

### Phase D1: Safety & Reliability (18 days)
- E08: RAMS Reliability Engineering (10 days)
- E09: Hazard & FMEA Analysis (8 days)

### Phase D2: Advanced Analysis (23 days)
- E11: Psychohistory Demographics (8 days)
- E13: Attack Path Modeling (15 days)

### Phase D3: Psychometric Core (61 days)
- E19: Organizational Blind Spots (12 days)
- E20: Personality-Team Fit (12 days)
- E21: Transcript Psychometric NER (15 days)
- E24: Cognitive Dissonance Breaking (10 days)
- E25: Threat Actor Personality Modeling (12 days)

### Phase D4: Experimental Psychohistory (60 days)
- E17: Lacanian Dyad Analysis (10 days)
- E18: Triad Group Dynamics (12 days)
- E22: Seldon Crisis Prediction (20 days)
- E23: Population Event Forecasting (18 days)

**Note:** Phase D4 enhancements are marked EXPERIMENTAL and require extensive validation.

---

## Resource Requirements

| Phase | Neo4j Nodes (est.) | External APIs | Priority |
|-------|-------------------|---------------|----------|
| B1 | +50,000 | 2 | CRITICAL |
| B2 | +200,000 | 5 | HIGH |
| B3 | +5,200,000 | 3 | HIGH |

---

## Links

- [00_TASKMASTER_MASTER_INDEX.md](00_TASKMASTER_MASTER_INDEX.md) - Master navigation
- [01_IMPLEMENTATION_ORDER.json](01_IMPLEMENTATION_ORDER.json) - Full enhancement details
- [03_TASK_SPECIFICATIONS.md](03_TASK_SPECIFICATIONS.md) - Individual task specs
- [04_PM_CHECKLIST.md](04_PM_CHECKLIST.md) - PM tracking
- [05_SESSION_HANDOFF.md](05_SESSION_HANDOFF.md) - Multi-session handoff
- [../blotter/BLOTTER.md](../blotter/BLOTTER.md) - Activity log

---

**Phase Details v1.0.1 | Option B: Balanced Foundation MVP | Updated 2025-12-04**
