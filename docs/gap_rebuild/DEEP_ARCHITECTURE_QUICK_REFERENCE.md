# Deep SBOM Attack Path Architecture - Quick Reference

**File:** DEEP_ARCHITECTURE_QUICK_REFERENCE.md
**Created:** 2025-11-19
**Version:** v1.0.0
**Purpose:** Quick navigation guide for deep architecture document
**Status:** ACTIVE

## Document Overview

The complete architecture is documented in **DEEP_SBOM_ATTACK_PATH_ARCHITECTURE.md** (100+ pages).

This quick reference helps you navigate to specific sections based on your needs.

---

## Quick Navigation by Role

### Security Analysts
**Need to understand**: Attack paths and threat prioritization

**Key Sections**:
- Section 3: MITRE ATT&CK Attack Path Integration (pages 30-42)
- Section 4: NOW/NEXT/NEVER Prioritization (pages 43-49)
- Section 7: McKenney's 8 Questions (pages 60-70)
- Appendix A: Sample Attack Scenario (pages 90-100)

**Essential Queries**:
```cypher
// Q1: Find all attack paths to critical infrastructure
// See Section 3.5, Query 1

// Q2: What are my NOW priorities?
// See Section 4.4, Query 1

// Q3: What threats is APT29 targeting?
// See Section 7, Question 4
```

### Vulnerability Management Teams
**Need to understand**: SBOM tracking and vulnerability variation

**Key Sections**:
- Section 1: SBOM Detail Architecture (pages 5-15)
- Section 2: Vulnerability Variation Modeling (pages 16-22)
- Section 4: NOW/NEXT/NEVER Prioritization (pages 43-49)
- Section 7: McKenney's 8 Questions (pages 60-70)

**Essential Queries**:
```cypher
// Q1: Find all equipment with vulnerable OpenSSL
// See Section 1.5, Query 1

// Q2: Show vulnerability distribution across fleet
// See Section 2.4, Query 3

// Q3: What can we do about high priority CVEs?
// See Section 7, Question 7
```

### Threat Intelligence Teams
**Need to understand**: Predictive modeling and threat forecasting

**Key Sections**:
- Section 5: Library-Level Psychohistory (pages 50-59)
- Section 3: MITRE ATT&CK Integration (pages 30-42)
- Section 2: Vulnerability Variation Modeling (pages 16-22)

**Essential Queries**:
```cypher
// Q1: What libraries will likely have CVEs in next 6 months?
// See Section 5.4, Query 1

// Q2: Predict blast radius of next OpenSSL CVE
// See Section 5.4, Query 4

// Q3: Which sectors are most at risk?
// See Section 5.4, Query 2
```

### System Architects
**Need to understand**: Schema design and implementation roadmap

**Key Sections**:
- Section 6: Complete Neo4j Schema (pages 71-75)
- Section 8: Implementation Roadmap (pages 81-84)
- Section 9: Architecture Decision Records (pages 85-88)
- Section 10: Scaling Considerations (pages 89-92)

**Essential Content**:
- All node types and properties (Section 6.1)
- All relationship types (Section 6.2)
- Constraints and indexes (Section 6.3)
- Performance targets (Section 10.3)

### Executive Leadership
**Need to understand**: Business value and strategic decisions

**Key Sections**:
- Executive Summary (page 1)
- Section 4: NOW/NEXT/NEVER Prioritization (pages 43-49)
- Section 7: McKenney's 8 Questions (pages 60-70)
- Section 11: Conclusion and Next Steps (pages 93-95)

**Key Metrics**:
- Reduce reactive work by 30% through predictive intelligence
- Prioritization accuracy: 80% of NOW items addressed first
- Time to threat assessment: <1 hour (down from days)
- Prediction accuracy: >70% within 90 days

---

## Quick Navigation by Use Case

### Use Case 1: "What's my immediate risk?"
**Path**: Section 4.4, Query 1 → NOW items requiring immediate action

### Use Case 2: "How vulnerable is my OpenSSL fleet?"
**Path**: Section 1.5, Query 1 → All equipment with vulnerable OpenSSL versions

### Use Case 3: "What attack paths threaten my water treatment plants?"
**Path**: Section 3.5, Query 1 → Attack paths to critical infrastructure

### Use Case 4: "What threats are coming in Q1 2026?"
**Path**: Section 5.4, Query 1 → Predicted threats in next 6 months

### Use Case 5: "How do I prioritize 1000 vulnerabilities?"
**Path**: Section 4 → Complete prioritization framework with NOW/NEXT/NEVER

### Use Case 6: "Did our patching efforts reduce risk?"
**Path**: Section 7, Question 8 → Before/after risk measurement

### Use Case 7: "What's the blast radius of CVE-2022-0778?"
**Path**: Section 5.4, Query 4 → Predict blast radius query

### Use Case 8: "Which threat groups target my sector?"
**Path**: Section 3.5, Query 5 → Equipment vulnerable to threat group TTPs

---

## Key Concepts Explained

### Library-Level Granularity
**What**: Track individual software libraries (OpenSSL 1.0.2k) instead of just equipment types
**Why**: Two identical Cisco ASA 5500 firewalls can have vastly different risk profiles based on library versions
**Where**: Section 1 - SBOM Detail Architecture

### SBOM (Software Bill of Materials)
**What**: Complete inventory of all software components in a piece of equipment
**Format**: SPDX-2.3 or CycloneDX standard
**Example**: Equipment → SBOM → Software → Library → CVE
**Where**: Section 1.2 - Node Type Definitions

### Vulnerability Variation
**What**: Same equipment product has different vulnerabilities across instances
**Example**:
- Cisco ASA 5500 Instance A (firmware 9.8.4): 12 CVEs, HIGH risk
- Cisco ASA 5500 Instance B (firmware 9.12.2): 2 CVEs, LOW risk
**Where**: Section 2 - Vulnerability Variation Modeling

### MITRE ATT&CK Attack Paths
**What**: Complete kill chain from Initial Access → Execution → Persistence → Impact
**Example**: CVE-2022-0778 (OpenSSL) → T1190 (Exploit Public-Facing App) → ... → T1485 (Data Destruction)
**Where**: Section 3 - MITRE ATT&CK Integration

### NOW/NEXT/NEVER Prioritization
**What**: Risk-based triage framework
**Scoring**: Criticality × Exploitability × Impact × Exposure
**Thresholds**:
- NOW (>80): Immediate action within 7 days
- NEXT (40-80): Plan and monitor within 30 days
- NEVER (<40): Accept risk with mitigations
**Where**: Section 4 - NOW/NEXT/NEVER Framework

### Psychohistory (Predictive Intelligence)
**What**: Predict future vulnerabilities based on patterns
**Based on**:
- Current version distribution
- Historical patch velocity
- Vulnerability discovery patterns
- Threat actor targeting
**Example**: "Predict next OpenSSL CVE in Q1 2026 will affect 60% of water sector"
**Where**: Section 5 - Library-Level Psychohistory

---

## Data Model Layers

### Layer 1: Organizational Context
```
Sector → Organization → Facility → EquipmentInstance
```
**Purpose**: Understand business context and criticality

### Layer 2: Equipment Detail
```
EquipmentInstance → SBOM → Software → Library
```
**Purpose**: Track software composition at granular level

### Layer 3: Vulnerability
```
Library → CVE → CWE → CAPEC
```
**Purpose**: Link software components to vulnerabilities

### Layer 4: Attack Modeling
```
Tactic → Technique → CVE → Library → Equipment → Impact
```
**Purpose**: Simulate adversary attack paths

### Layer 5: Prediction
```
VersionDistribution → FutureThreat → PredictedIncident
```
**Purpose**: Forecast future threats and incidents

---

## Critical Queries Cheat Sheet

### Immediate Action Items
```cypher
MATCH (eq:EquipmentInstance {actionCategory: "NOW"})
RETURN eq.equipmentId, eq.facilityName, eq.priorityScore, eq.deadline
ORDER BY eq.deadline ASC;
```

### Equipment with Specific Library Version
```cypher
MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(:SBOM)
      -[:CONTAINS_SOFTWARE]->(:Software)
      -[:DEPENDS_ON]->(lib:Library)
WHERE lib.name = "OpenSSL" AND lib.version < "3.0.0"
RETURN eq.equipmentId, lib.version, lib.activeCveCount;
```

### Attack Path from CVE to Impact
```cypher
MATCH path = (cve:CVE {cveId: "CVE-2022-0778"})
             <-[:EXPLOITS_CVE]-(:Technique)
             <-[:HAS_TECHNIQUE]-(tactic:Tactic)
             -[:LEADS_TO*0..5]->(impactTactic:Tactic {name: "Impact"})
RETURN path;
```

### Predicted Threats Next Quarter
```cypher
MATCH (ft:FutureThreat)
WHERE ft.predictedDiscoveryDate >= date()
  AND ft.predictedDiscoveryDate <= date() + duration({months: 3})
RETURN ft.libraryName, ft.predictedDiscoveryDate, ft.attackProbability
ORDER BY ft.attackProbability DESC;
```

### Risk Trend Analysis
```cypher
MATCH (eq:EquipmentInstance)-[:HAS_SBOM]->(sbomNew:SBOM)
WHERE sbomNew.generatedDate = date()
MATCH (eq)-[:HAS_SBOM]->(sbomOld:SBOM)
WHERE sbomOld.generatedDate = date() - duration({days: 30})
RETURN eq.equipmentId,
       sbomOld.riskScore AS oldRisk,
       sbomNew.riskScore AS newRisk,
       sbomNew.riskScore - sbomOld.riskScore AS riskDelta;
```

---

## Implementation Quick Start

### Phase 1: Proof of Concept (Weeks 1-4)
**Goal**: Validate architecture with 10 equipment instances

**Steps**:
1. Set up Neo4j database
2. Create schema (Section 6.3 constraints/indexes)
3. Import sample data (Appendix A)
4. Execute validation queries (Section 7)
5. Measure query performance (<5 seconds target)

**Success**: All McKenney's 8 questions answered with sample data

### Phase 2: Pilot Deployment (Weeks 5-8)
**Goal**: Expand to 100 critical equipment instances

**Steps**:
1. Build SBOM generation automation (Syft/Trivy)
2. Implement priority scoring (Section 4.2 algorithm)
3. Create NOW/NEXT/NEVER dashboard
4. Import MITRE ATT&CK data (Section 3.2)
5. Train security team on queries

**Success**: Operational dashboard, team trained, priorities assigned

### Phase 3: Production Rollout (Weeks 9-12)
**Goal**: Scale to full equipment inventory

**Steps**:
1. Scale to all equipment (Section 10 scaling strategies)
2. Deploy psychohistory engine (Section 5)
3. Integrate with security workflows (SIEM, ticketing)
4. Establish quarterly review cadence
5. Measure business metrics

**Success**: Full production, predictive alerts, reduced reactive work

---

## Performance Targets

### Query Performance SLAs
```yaml
Simple lookup (by ID):          <100ms
SBOM detail (equipment):         <500ms
Vulnerability list:              <1s
Attack path simulation:          <3s
Sector aggregation:              <5s
Prediction generation:           <10s
```

### Data Quality Targets
```yaml
SBOM coverage (critical):        100%
SBOM completeness:               >95%
CVE mapping accuracy:            >98%
Prediction accuracy (90 days):   >70%
```

### Business Impact Targets
```yaml
Reduce reactive work:            30%
Time to threat assessment:       <1 hour
Prioritization accuracy:         80%
Resource optimization:           25%
```

---

## Getting Help

### Common Questions

**Q: "How do I find all equipment with a specific CVE?"**
A: Section 3.5, Query 1 - Links CVE through library to equipment

**Q: "What's the difference between NOW, NEXT, and NEVER?"**
A: Section 4.2 - NOW (>80 score), NEXT (40-80), NEVER (<40)

**Q: "How accurate are the psychohistory predictions?"**
A: Section 5.4, Query 6 - Historical accuracy measurement, target >70%

**Q: "Can this scale to 100,000+ equipment instances?"**
A: Section 10 - Scaling strategies, tested to 10M nodes

**Q: "What SBOM format should I use?"**
A: SPDX-2.3 or CycloneDX - both supported, SPDX recommended

**Q: "How often should SBOMs be regenerated?"**
A: Weekly for critical equipment, monthly for others

**Q: "What if a library doesn't have CVE data?"**
A: Still track for future CVE discovery, use psychohistory predictions

**Q: "How do I handle transitive dependencies?"**
A: Section 1.2 - REQUIRES relationship, can traverse unlimited depth

---

## Architecture Principles Summary

### 1. Evidence-Based
All claims verifiable through queries, no assumptions

### 2. Granular Precision
Library-level tracking (OpenSSL 1.0.2k) not just product-level (Cisco ASA)

### 3. Attack-Centric
Model from adversary perspective using MITRE ATT&CK

### 4. Predictive Intelligence
Use historical patterns to forecast future threats

### 5. Risk-Based Prioritization
Allocate resources based on multi-factor scoring, not just CVE counts

### 6. Actionable Insights
Every query should enable a decision or action

### 7. Scalable Performance
Designed for millions of nodes with <10 second query times

### 8. Temporal Awareness
Track changes over time, measure improvement

---

## Key Files and Locations

```
/docs/gap_rebuild/
├── DEEP_SBOM_ATTACK_PATH_ARCHITECTURE.md    # Complete architecture (this doc)
├── DEEP_ARCHITECTURE_QUICK_REFERENCE.md     # This navigation guide
└── (future files)
    ├── IMPLEMENTATION_GUIDE.md               # Step-by-step implementation
    ├── QUERY_COOKBOOK.md                     # Common query patterns
    ├── DASHBOARD_DESIGNS.md                  # Visualization specs
    └── VALIDATION_RESULTS.md                 # POC validation data
```

---

## Next Steps

### For Security Teams
1. Read Executive Summary (page 1)
2. Review Section 4: NOW/NEXT/NEVER
3. Execute sample queries against your data
4. Pilot with 10 critical equipment instances

### For Architects
1. Read Section 6: Complete Schema
2. Review Section 9: ADRs
3. Study Section 10: Scaling Considerations
4. Set up development Neo4j instance

### For Management
1. Read Executive Summary and Section 11
2. Review success metrics (page 95)
3. Approve Phase 1 POC budget
4. Establish steering committee

---

**Questions?** Reference the main architecture document section numbers or use the query index above.

**Status**: Architecture design complete, ready for validation and implementation.
