# ICE PRIORITIZATION MATRIX - ALL 196 PLANNED APIs

**File:** ICE_PRIORITIZATION_MATRIX.md
**Created:** 2025-12-12 18:45 UTC
**Version:** 1.0.0
**Status:** COMPLETE - ACTIONABLE DEVELOPMENT ROADMAP

---

## Executive Summary

**Total APIs Analyzed:** 196 planned endpoints (Phase B2-B5)
**Prioritization Method:** ICE Score = (Impact × Confidence × Ease) / 100
**Implementation Horizon:** 11+ Sprints (22+ weeks)

**Quick Wins (Tier 1):** 47 APIs - ICE Score > 8.0 → Sprints 1-2 (4 weeks)
**High Priority (Tier 2):** 62 APIs - ICE Score 6.0-8.0 → Sprints 3-5 (6 weeks)
**Medium Priority (Tier 3):** 58 APIs - ICE Score 4.0-6.0 → Sprints 6-10 (10 weeks)
**Low Priority (Tier 4):** 29 APIs - ICE Score < 4.0 → Sprint 11+ (2+ weeks)

---

## Scoring Methodology

### Impact Score (1-10)
- **10**: Critical business value, direct revenue impact, foundational capability
- **8-9**: High business value, significant user benefit, competitive advantage
- **6-7**: Moderate value, important but not critical, incremental improvement
- **4-5**: Nice-to-have, edge case coverage, minor improvement
- **1-3**: Minimal value, rarely used, experimental feature

### Confidence Score (1-10)
- **10**: Fully understood, clear requirements, proven patterns, existing similar implementation
- **8-9**: Well-defined, minor unknowns, standard technology, clear approach
- **6-7**: Moderate uncertainty, some research needed, achievable with effort
- **4-5**: Significant unknowns, requires exploration, new technology
- **1-3**: High uncertainty, major research needed, unproven approach

### Ease Score (1-10)
- **10**: < 2 days, minimal code, no dependencies, trivial implementation
- **8-9**: 2-5 days, straightforward logic, few dependencies, standard patterns
- **6-7**: 1-2 weeks, moderate complexity, some dependencies, requires design
- **4-5**: 2-4 weeks, complex logic, many dependencies, significant effort
- **1-3**: 4+ weeks, very complex, major dependencies, architectural changes

### ICE Score Calculation
```
ICE Score = (Impact × Confidence × Ease) / 100

Example:
Impact: 9, Confidence: 8, Ease: 9
ICE = (9 × 8 × 9) / 100 = 648 / 100 = 6.48
```

---

## TIER 1: QUICK WINS (ICE > 8.0) - SPRINTS 1-2

**Total:** 47 APIs | **Timeline:** 4 weeks | **Team Size:** 3-4 developers

### Phase B2: SBOM & Vendor Equipment (15 APIs)

#### E03: SBOM Analysis (8 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 1 | POST /sbom/analyze | 10 | 9 | 9 | 8.1 | 3d | File parser, Neo4j |
| 2 | GET /sbom/{sbom_id} | 9 | 10 | 10 | 9.0 | 1d | Neo4j query |
| 3 | GET /sbom/components/{id}/vulnerabilities | 10 | 9 | 8 | 7.2 | 4d | CVE correlation |
| 4 | POST /sbom/dependencies/map | 9 | 8 | 8 | 5.76 | 5d | Graph traversal |
| 5 | GET /sbom/licenses | 8 | 9 | 9 | 6.48 | 2d | License DB |
| 6 | GET /sbom/summary | 8 | 10 | 10 | 8.0 | 1d | Aggregation |
| 7 | GET /sbom/components/search | 9 | 9 | 9 | 7.29 | 2d | Semantic search |
| 8 | GET /sbom/export | 7 | 10 | 10 | 7.0 | 1d | JSON export |

**Sprint 1 Focus:** Core SBOM ingestion (APIs 1-4) - Foundation for dependency analysis
**Business Value:** Enable SBOM-based vulnerability management (critical for compliance)

#### E15: Vendor Equipment (7 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 9 | POST /equipment | 9 | 9 | 9 | 7.29 | 2d | Equipment schema |
| 10 | GET /equipment/{equipment_id} | 9 | 10 | 10 | 9.0 | 1d | Neo4j query |
| 11 | GET /equipment/search | 9 | 9 | 8 | 6.48 | 3d | Semantic search |
| 12 | PUT /equipment/{id}/lifecycle | 8 | 9 | 9 | 6.48 | 2d | State machine |
| 13 | GET /equipment/eol-report | 10 | 8 | 8 | 6.4 | 4d | Vendor data sync |
| 14 | GET /equipment/summary | 8 | 10 | 10 | 8.0 | 1d | Aggregation |
| 15 | GET /equipment/by-vendor | 7 | 10 | 10 | 7.0 | 1d | Grouping query |

**Sprint 1 Focus:** Equipment CRUD + EOL tracking (APIs 9-13)
**Business Value:** Track vendor equipment lifecycle, prevent EOL vulnerabilities

### Phase B3: Threat Intelligence (18 APIs)

#### E04: Threat Actors & Campaigns (12 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 16 | POST /threat-intel/actors | 9 | 9 | 9 | 7.29 | 2d | Actor schema |
| 17 | GET /threat-intel/actors/{id} | 9 | 10 | 10 | 9.0 | 1d | Neo4j query |
| 18 | GET /threat-intel/actors/search | 10 | 9 | 8 | 7.2 | 3d | Semantic search |
| 19 | GET /threat-intel/actors/active | 9 | 9 | 9 | 7.29 | 2d | Time-based filter |
| 20 | GET /threat-intel/actors/by-sector/{sector} | 9 | 9 | 8 | 6.48 | 3d | Sector mapping |
| 21 | GET /threat-intel/actors/{id}/campaigns | 8 | 9 | 9 | 6.48 | 2d | Graph traversal |
| 22 | GET /threat-intel/actors/{id}/cves | 10 | 8 | 8 | 6.4 | 4d | CVE correlation |
| 23 | POST /threat-intel/campaigns | 8 | 9 | 9 | 6.48 | 2d | Campaign schema |
| 24 | GET /threat-intel/campaigns/{id} | 8 | 10 | 10 | 8.0 | 1d | Neo4j query |
| 25 | GET /threat-intel/campaigns/search | 9 | 9 | 8 | 6.48 | 3d | Semantic search |
| 26 | GET /threat-intel/campaigns/active | 8 | 9 | 9 | 6.48 | 2d | Active filter |
| 27 | GET /threat-intel/campaigns/{id}/iocs | 9 | 8 | 8 | 5.76 | 4d | IOC extraction |

**Sprint 1-2 Focus:** Threat actor CRUD + campaign tracking (APIs 16-27)
**Business Value:** Core threat intelligence capabilities for proactive defense

#### E04: MITRE ATT&CK Mapping (6 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 28 | POST /threat-intel/mitre/mappings | 10 | 8 | 7 | 5.6 | 5d | MITRE framework |
| 29 | GET /threat-intel/mitre/mappings/entity/{type}/{id} | 9 | 9 | 8 | 6.48 | 3d | Graph query |
| 30 | GET /threat-intel/mitre/techniques/{id}/actors | 9 | 9 | 8 | 6.48 | 3d | Actor correlation |
| 31 | GET /threat-intel/mitre/coverage | 10 | 7 | 7 | 4.9 | 6d | Coverage calc |
| 32 | GET /threat-intel/mitre/gaps | 10 | 7 | 7 | 4.9 | 6d | Gap analysis |
| 33 | GET /threat-intel/mitre/dashboard | 8 | 9 | 9 | 6.48 | 2d | Visualization |

**Sprint 2 Focus:** MITRE mapping integration (APIs 28-33)
**Business Value:** Map threats to MITRE ATT&CK for standardized defense

### Phase B5: Economic Impact (14 APIs)

#### E10: Cost & ROI Analysis (14 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 34 | GET /economic-impact/costs/summary | 9 | 8 | 9 | 6.48 | 3d | Cost aggregation |
| 35 | GET /economic-impact/costs/by-category | 8 | 9 | 9 | 6.48 | 2d | Category grouping |
| 36 | GET /economic-impact/costs/{id}/breakdown | 8 | 9 | 9 | 6.48 | 2d | Detail query |
| 37 | POST /economic-impact/costs/calculate | 9 | 7 | 8 | 5.04 | 5d | Cost modeling |
| 38 | GET /economic-impact/costs/historical | 8 | 8 | 9 | 5.76 | 3d | Time-series |
| 39 | GET /economic-impact/roi/summary | 9 | 8 | 9 | 6.48 | 3d | ROI aggregation |
| 40 | GET /economic-impact/roi/{id} | 8 | 10 | 10 | 8.0 | 1d | Single query |
| 41 | POST /economic-impact/roi/calculate | 10 | 7 | 7 | 4.9 | 6d | ROI formulas |
| 42 | GET /economic-impact/roi/by-category | 8 | 9 | 9 | 6.48 | 2d | Category ROI |
| 43 | GET /economic-impact/roi/projections | 9 | 6 | 7 | 3.78 | 7d | Forecasting |
| 44 | POST /economic-impact/roi/comparison | 8 | 8 | 8 | 5.12 | 4d | Comparison logic |
| 45 | GET /economic-impact/dashboard/summary | 9 | 9 | 9 | 7.29 | 2d | Dashboard agg |
| 46 | GET /economic-impact/dashboard/trends | 8 | 9 | 9 | 6.48 | 2d | Trend analysis |
| 47 | GET /economic-impact/dashboard/kpis | 9 | 9 | 9 | 7.29 | 2d | KPI calc |

**Sprint 2 Focus:** Cost/ROI dashboards (APIs 34-47)
**Business Value:** Financial justification for security investments (critical for executive buy-in)

---

## TIER 2: HIGH PRIORITY (ICE 6.0-8.0) - SPRINTS 3-5

**Total:** 62 APIs | **Timeline:** 6 weeks | **Team Size:** 4-5 developers

### Phase B3: Risk & Remediation (32 APIs)

#### E05: Risk Scoring Engine (26 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 48 | POST /risk/scores | 10 | 7 | 6 | 4.2 | 8d | Risk algorithm |
| 49 | GET /risk/scores/{type}/{id} | 9 | 9 | 9 | 7.29 | 2d | Score query |
| 50 | GET /risk/scores/high-risk | 10 | 8 | 8 | 6.4 | 4d | Risk filter |
| 51 | GET /risk/scores/trending | 9 | 7 | 7 | 4.41 | 6d | Trend calc |
| 52 | GET /risk/scores/search | 9 | 9 | 8 | 6.48 | 3d | Search impl |
| 53 | POST /risk/scores/recalculate/{type}/{id} | 8 | 8 | 7 | 4.48 | 5d | Recalc logic |
| 54 | GET /risk/scores/history/{type}/{id} | 8 | 9 | 8 | 5.76 | 4d | Time-series |
| 55 | POST /risk/assets/criticality | 9 | 8 | 8 | 5.76 | 4d | Criticality model |
| 56 | GET /risk/assets/{id}/criticality | 8 | 10 | 10 | 8.0 | 1d | Query impl |
| 57 | GET /risk/assets/mission-critical | 10 | 9 | 8 | 7.2 | 3d | Critical filter |
| 58 | GET /risk/assets/by-criticality/{level} | 8 | 9 | 9 | 6.48 | 2d | Level grouping |
| 59 | PUT /risk/assets/{id}/criticality | 8 | 9 | 9 | 6.48 | 2d | Update impl |
| 60 | GET /risk/assets/criticality/summary | 8 | 9 | 9 | 6.48 | 2d | Summary agg |
| 61 | POST /risk/exposure | 9 | 7 | 6 | 3.78 | 8d | Exposure calc |
| 62 | GET /risk/exposure/{id} | 8 | 9 | 9 | 6.48 | 2d | Exposure query |
| 63 | GET /risk/exposure/internet-facing | 10 | 8 | 7 | 5.6 | 5d | Internet filter |
| 64 | GET /risk/exposure/high-exposure | 9 | 8 | 8 | 5.76 | 4d | Exposure filter |
| 65 | GET /risk/exposure/attack-surface | 10 | 7 | 6 | 4.2 | 8d | Surface calc |
| 66 | GET /risk/aggregation/by-vendor | 9 | 8 | 8 | 5.76 | 4d | Vendor agg |
| 67 | GET /risk/aggregation/by-sector | 9 | 8 | 8 | 5.76 | 4d | Sector agg |
| 68 | GET /risk/aggregation/by-asset-type | 8 | 9 | 8 | 5.76 | 4d | Asset agg |
| 69 | GET /risk/aggregation/{type}/{id} | 8 | 9 | 9 | 6.48 | 2d | Generic agg |
| 70 | GET /risk/dashboard/summary | 9 | 9 | 8 | 6.48 | 3d | Dashboard impl |
| 71 | GET /risk/dashboard/risk-matrix | 10 | 7 | 6 | 4.2 | 8d | Matrix calc |
| 72 | GET /risk/dashboard/alerts | 8 | 9 | 9 | 6.48 | 2d | Alert query |
| 73 | GET /risk/dashboard/trends | 8 | 8 | 8 | 5.12 | 4d | Trend analysis |

**Sprint 3-4 Focus:** Risk scoring engine (APIs 48-73)
**Business Value:** Quantify cyber risk for prioritized remediation

#### E06: Remediation Workflow (6 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 74 | POST /remediation/remediation-plans | 9 | 8 | 7 | 5.04 | 5d | Workflow engine |
| 75 | GET /remediation/remediation-plans/{id} | 8 | 10 | 10 | 8.0 | 1d | Query impl |
| 76 | GET /remediation/remediation-plans/search | 8 | 9 | 8 | 5.76 | 4d | Search impl |
| 77 | PUT /remediation/remediation-plans/{id}/execute | 10 | 6 | 5 | 3.0 | 10d | Execution engine |
| 78 | GET /remediation/remediation-plans/{id}/progress | 9 | 8 | 8 | 5.76 | 4d | Progress track |
| 79 | GET /remediation/remediation-plans/dashboard | 8 | 9 | 9 | 6.48 | 2d | Dashboard impl |

**Sprint 4-5 Focus:** Remediation planning (APIs 74-79)
**Business Value:** Automated remediation workflows for faster response

### Phase B3: IOCs & Threat Feeds (12 APIs)

#### E04: Indicators of Compromise (12 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 80 | POST /threat-intel/iocs | 9 | 8 | 8 | 5.76 | 4d | IOC schema |
| 81 | POST /threat-intel/iocs/bulk | 10 | 7 | 6 | 4.2 | 8d | Bulk processing |
| 82 | GET /threat-intel/iocs/search | 9 | 9 | 8 | 6.48 | 3d | Search impl |
| 83 | GET /threat-intel/iocs/active | 9 | 9 | 9 | 7.29 | 2d | Active filter |
| 84 | GET /threat-intel/iocs/by-type/{type} | 8 | 9 | 9 | 6.48 | 2d | Type filter |
| 85 | GET /threat-intel/iocs/recent | 8 | 10 | 10 | 8.0 | 1d | Time filter |
| 86 | GET /threat-intel/iocs/by-severity | 8 | 9 | 9 | 6.48 | 2d | Severity sort |
| 87 | POST /threat-intel/feeds | 8 | 7 | 7 | 3.92 | 7d | Feed integration |
| 88 | GET /threat-intel/feeds | 7 | 10 | 10 | 7.0 | 1d | Feed list |
| 89 | PUT /threat-intel/feeds/{id}/refresh | 9 | 6 | 6 | 3.24 | 9d | Feed sync |
| 90 | GET /threat-intel/feeds/status | 7 | 9 | 9 | 5.67 | 3d | Status check |
| 91 | GET /threat-intel/dashboard/summary | 9 | 9 | 8 | 6.48 | 3d | Dashboard impl |

**Sprint 5 Focus:** IOC management + threat feeds (APIs 80-91)
**Business Value:** Integrate external threat intelligence for detection

### Phase B4: Compliance & Scanning (12 APIs)

#### E07: Compliance Frameworks (8 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 92 | POST /compliance/frameworks | 9 | 7 | 7 | 4.41 | 6d | Framework data |
| 93 | GET /compliance/frameworks/{framework} | 9 | 9 | 8 | 6.48 | 3d | Framework query |
| 94 | GET /compliance/frameworks/gap-analysis | 10 | 6 | 5 | 3.0 | 10d | Gap algorithm |
| 95 | POST /compliance/requirements | 8 | 8 | 7 | 4.48 | 5d | Requirement map |
| 96 | GET /compliance/requirements/coverage | 9 | 7 | 7 | 4.41 | 6d | Coverage calc |
| 97 | GET /compliance/frameworks/list | 7 | 10 | 10 | 7.0 | 1d | List query |
| 98 | GET /compliance/dashboard/summary | 9 | 9 | 8 | 6.48 | 3d | Dashboard impl |
| 99 | GET /compliance/dashboard/status | 8 | 9 | 9 | 6.48 | 2d | Status agg |

**Sprint 5 Focus:** Compliance framework mapping (APIs 92-99)
**Business Value:** Demonstrate compliance with NIST, ISO, IEC standards

#### E08: Automated Scanning (4 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 100 | POST /scanning/scans | 9 | 6 | 5 | 2.7 | 12d | Scanner integration |
| 101 | GET /scanning/scans/{id} | 8 | 9 | 9 | 6.48 | 2d | Scan query |
| 102 | GET /scanning/scans/history | 8 | 9 | 9 | 6.48 | 2d | History query |
| 103 | POST /scanning/scans/schedule | 9 | 7 | 6 | 3.78 | 8d | Scheduler impl |

**Sprint 5 Focus:** Basic scanning APIs (APIs 100-103)
**Business Value:** Automated vulnerability scanning integration

### Phase B5: Business Value & Demographics (8 APIs)

#### E10: Business Value Metrics (5 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 104 | GET /economic-impact/value/metrics | 8 | 8 | 8 | 5.12 | 4d | Value calc |
| 105 | GET /economic-impact/value/{id}/assessment | 9 | 7 | 7 | 4.41 | 6d | Assessment logic |
| 106 | POST /economic-impact/value/calculate | 9 | 7 | 6 | 3.78 | 8d | Value algorithm |
| 107 | GET /economic-impact/value/risk-adjusted | 10 | 6 | 6 | 3.6 | 9d | Risk adjustment |
| 108 | GET /economic-impact/value/by-sector | 8 | 8 | 8 | 5.12 | 4d | Sector grouping |

**Sprint 5 Focus:** Business value assessment (APIs 104-108)
**Business Value:** Quantify security investment value

#### E11: Demographics Baseline (3 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 109 | GET /demographics/summary | 7 | 8 | 8 | 4.48 | 5d | Demographics data |
| 110 | GET /demographics/teams | 7 | 8 | 8 | 4.48 | 5d | Team data |
| 111 | GET /demographics/competency-matrix | 8 | 7 | 7 | 3.92 | 7d | Skills matrix |

**Sprint 5 Focus:** Basic demographics (APIs 109-111)
**Business Value:** Understand organizational security capabilities

---

## TIER 3: MEDIUM PRIORITY (ICE 4.0-6.0) - SPRINTS 6-10

**Total:** 58 APIs | **Timeline:** 10 weeks | **Team Size:** 3-4 developers

### Phase B4: Alert Management (15 APIs)

#### E09: Alert Lifecycle (15 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 112 | POST /alerts/alerts | 8 | 7 | 7 | 3.92 | 7d | Alert schema |
| 113 | GET /alerts/alerts | 8 | 9 | 8 | 5.76 | 4d | Alert list |
| 114 | PUT /alerts/alerts/{id}/acknowledge | 7 | 9 | 9 | 5.67 | 3d | State update |
| 115 | PUT /alerts/alerts/{id}/resolve | 8 | 9 | 9 | 6.48 | 2d | Resolution logic |
| 116 | GET /alerts/alerts/dashboard | 8 | 8 | 8 | 5.12 | 4d | Dashboard impl |
| 117 | GET /alerts/alerts/by-severity | 7 | 9 | 9 | 5.67 | 3d | Severity filter |
| 118 | GET /alerts/alerts/unresolved | 8 | 9 | 9 | 6.48 | 2d | Status filter |
| 119 | GET /alerts/alerts/history | 7 | 9 | 9 | 5.67 | 3d | History query |
| 120 | POST /alerts/rules | 8 | 6 | 6 | 2.88 | 10d | Rule engine |
| 121 | GET /alerts/rules | 6 | 9 | 9 | 4.86 | 4d | Rule list |
| 122 | PUT /alerts/rules/{id} | 6 | 8 | 8 | 3.84 | 6d | Rule update |
| 123 | DELETE /alerts/rules/{id} | 5 | 10 | 10 | 5.0 | 2d | Rule delete |
| 124 | GET /alerts/analytics/trends | 7 | 7 | 7 | 3.43 | 8d | Trend analysis |
| 125 | GET /alerts/analytics/by-type | 6 | 8 | 8 | 3.84 | 6d | Type analytics |
| 126 | GET /alerts/export | 6 | 9 | 9 | 4.86 | 4d | Export impl |

**Sprint 6-7 Focus:** Alert management system (APIs 112-126)
**Business Value:** Centralized alert handling and response

### Phase B5: Impact Modeling & Prioritization (15 APIs)

#### E10: Financial Impact Modeling (10 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 127 | POST /economic-impact/impact/model | 9 | 5 | 4 | 1.8 | 15d | Impact models |
| 128 | GET /economic-impact/impact/scenarios | 8 | 7 | 7 | 3.92 | 7d | Scenario data |
| 129 | POST /economic-impact/impact/simulate | 10 | 4 | 3 | 1.2 | 20d | Monte Carlo |
| 130 | GET /economic-impact/impact/{id}/results | 7 | 8 | 8 | 4.48 | 5d | Result query |
| 131 | GET /economic-impact/impact/historical | 7 | 7 | 8 | 3.92 | 7d | Historical data |
| 132 | GET /economic-impact/dashboard/alerts | 7 | 9 | 9 | 5.67 | 3d | Alert query |
| 133 | GET /economic-impact/dashboard/executive | 9 | 7 | 7 | 4.41 | 6d | Executive view |
| 134 | POST /economic-impact/scenarios/create | 7 | 6 | 6 | 2.52 | 11d | Scenario builder |
| 135 | GET /economic-impact/scenarios/compare | 7 | 7 | 7 | 3.43 | 8d | Comparison logic |
| 136 | GET /economic-impact/forecasts | 8 | 5 | 5 | 2.0 | 14d | Forecasting |

**Sprint 7-9 Focus:** Financial impact modeling (APIs 127-136)
**Business Value:** Quantify potential breach impacts for risk-based decisions

#### E12: Vulnerability Prioritization (5 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 137 | POST /prioritization/prioritize | 10 | 6 | 5 | 3.0 | 10d | Priority algorithm |
| 138 | GET /prioritization/rankings | 8 | 8 | 8 | 5.12 | 4d | Ranking query |
| 139 | POST /prioritization/urgency-score | 9 | 6 | 5 | 2.7 | 12d | Urgency calc |
| 140 | GET /prioritization/critical-path | 10 | 5 | 4 | 2.0 | 15d | Path algorithm |
| 141 | GET /prioritization/dashboard | 8 | 8 | 8 | 5.12 | 4d | Dashboard impl |

**Sprint 9-10 Focus:** Vulnerability prioritization (APIs 137-141)
**Business Value:** Intelligent remediation prioritization (EPSS + CVSS + business context)

### Phase B2: Extended SBOM & Equipment (15 APIs)

#### E03: Advanced SBOM Features (8 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 142 | GET /sbom/components/{id}/dependencies | 7 | 8 | 7 | 3.92 | 7d | Dep graph |
| 143 | GET /sbom/vulnerabilities/critical | 8 | 9 | 8 | 5.76 | 4d | Crit filter |
| 144 | POST /sbom/validate | 7 | 7 | 7 | 3.43 | 8d | Validation logic |
| 145 | GET /sbom/diff/{id1}/{id2} | 6 | 7 | 6 | 2.52 | 11d | Diff algorithm |
| 146 | GET /sbom/compliance | 7 | 7 | 7 | 3.43 | 8d | Compliance check |
| 147 | POST /sbom/upload | 8 | 8 | 7 | 4.48 | 5d | File upload |
| 148 | GET /sbom/statistics | 6 | 9 | 9 | 4.86 | 4d | Stats agg |
| 149 | GET /sbom/dashboard | 7 | 8 | 8 | 4.48 | 5d | Dashboard impl |

**Sprint 8-9 Focus:** Advanced SBOM analytics (APIs 142-149)
**Business Value:** Deep SBOM analysis for supply chain security

#### E15: Equipment Analytics (7 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 150 | GET /equipment/analytics/age-distribution | 7 | 8 | 8 | 4.48 | 5d | Age calc |
| 151 | GET /equipment/analytics/vendor-coverage | 7 | 8 | 8 | 4.48 | 5d | Vendor stats |
| 152 | GET /equipment/vulnerabilities | 8 | 7 | 7 | 3.92 | 7d | Vuln correlation |
| 153 | POST /equipment/bulk-import | 7 | 7 | 6 | 2.94 | 10d | Bulk processing |
| 154 | GET /equipment/lifecycle/transitions | 6 | 8 | 8 | 3.84 | 6d | State history |
| 155 | GET /equipment/dashboard | 7 | 8 | 8 | 4.48 | 5d | Dashboard impl |
| 156 | GET /equipment/export | 6 | 9 | 9 | 4.86 | 4d | Export impl |

**Sprint 9-10 Focus:** Equipment analytics (APIs 150-156)
**Business Value:** Equipment lifecycle analytics and reporting

### Phase B4: Extended Scanning & Compliance (13 APIs)

#### E08: Advanced Scanning (9 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 157 | GET /scanning/scans/findings | 8 | 8 | 7 | 4.48 | 5d | Finding query |
| 158 | GET /scanning/scans/findings/{id} | 7 | 9 | 9 | 5.67 | 3d | Detail query |
| 159 | PUT /scanning/scans/{id}/remediate | 8 | 6 | 5 | 2.4 | 13d | Remediation link |
| 160 | POST /scanning/policies | 7 | 7 | 6 | 2.94 | 10d | Policy engine |
| 161 | GET /scanning/policies | 6 | 9 | 9 | 4.86 | 4d | Policy list |
| 162 | PUT /scanning/policies/{id} | 6 | 8 | 8 | 3.84 | 6d | Policy update |
| 163 | GET /scanning/dashboard | 7 | 8 | 8 | 4.48 | 5d | Dashboard impl |
| 164 | GET /scanning/trends | 7 | 7 | 7 | 3.43 | 8d | Trend analysis |
| 165 | GET /scanning/export | 6 | 9 | 9 | 4.86 | 4d | Export impl |

**Sprint 8-9 Focus:** Advanced scanning features (APIs 157-165)
**Business Value:** Comprehensive vulnerability scanning and policy enforcement

#### E07: Advanced Compliance (4 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 166 | POST /compliance/evidence | 7 | 6 | 6 | 2.52 | 11d | Evidence collection |
| 167 | GET /compliance/evidence/{id} | 6 | 9 | 9 | 4.86 | 4d | Evidence query |
| 168 | GET /compliance/reports/{framework} | 8 | 7 | 6 | 3.36 | 9d | Report generation |
| 169 | POST /compliance/attestations | 7 | 7 | 7 | 3.43 | 8d | Attestation logic |

**Sprint 9-10 Focus:** Compliance evidence and reporting (APIs 166-169)
**Business Value:** Audit trail and compliance reporting

---

## TIER 4: LOW PRIORITY (ICE < 4.0) - SPRINT 11+

**Total:** 29 APIs | **Timeline:** 2+ weeks | **Team Size:** 2-3 developers

### Phase B5: Advanced Economics & Demographics (10 APIs)

#### E11: Demographics Predictions (1 API)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 170 | POST /demographics/predict-churn | 6 | 4 | 4 | 0.96 | 18d | ML models |

**Sprint 11+ Focus:** Predictive demographics (API 170)
**Business Value:** Team churn prediction (experimental feature)

#### E10: Advanced Economic Analytics (9 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 171 | GET /economic-impact/impact/what-if | 7 | 4 | 4 | 1.12 | 17d | What-if analysis |
| 172 | POST /economic-impact/benchmarks | 6 | 5 | 5 | 1.5 | 15d | Benchmark data |
| 173 | GET /economic-impact/benchmarks/industry | 7 | 5 | 5 | 1.75 | 14d | Industry data |
| 174 | POST /economic-impact/optimize | 8 | 4 | 3 | 0.96 | 20d | Optimization engine |
| 175 | GET /economic-impact/recommendations | 7 | 5 | 4 | 1.4 | 16d | Recommendation AI |
| 176 | POST /economic-impact/sensitivity | 7 | 4 | 4 | 1.12 | 17d | Sensitivity analysis |
| 177 | GET /economic-impact/correlations | 6 | 5 | 5 | 1.5 | 15d | Correlation calc |
| 178 | GET /economic-impact/insights | 7 | 4 | 4 | 1.12 | 17d | AI insights |
| 179 | POST /economic-impact/custom-metrics | 6 | 5 | 5 | 1.5 | 15d | Custom metrics |

**Sprint 11+ Focus:** Advanced economic analytics (APIs 171-179)
**Business Value:** Advanced financial modeling (requires ML/AI capabilities)

### Phase B3: Advanced Threat Intelligence (8 APIs)

#### E04: Extended Threat Features (8 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 180 | POST /threat-intel/correlate | 7 | 4 | 4 | 1.12 | 17d | Correlation engine |
| 181 | GET /threat-intel/predictions | 8 | 3 | 3 | 0.72 | 22d | Predictive ML |
| 182 | POST /threat-intel/enrich | 7 | 5 | 4 | 1.4 | 16d | Enrichment services |
| 183 | GET /threat-intel/relationships/visualize | 6 | 6 | 5 | 1.8 | 14d | Graph viz |
| 184 | POST /threat-intel/simulate | 8 | 3 | 3 | 0.72 | 22d | Attack simulation |
| 185 | GET /threat-intel/attribution | 7 | 4 | 4 | 1.12 | 17d | Attribution logic |
| 186 | GET /threat-intel/recommendations | 7 | 4 | 4 | 1.12 | 17d | Recommendation AI |
| 187 | POST /threat-intel/custom-indicators | 6 | 5 | 5 | 1.5 | 15d | Custom IOC logic |

**Sprint 11+ Focus:** AI-powered threat intelligence (APIs 180-187)
**Business Value:** Advanced threat prediction and correlation (experimental)

### Phase B4: Extended Alert Analytics (6 APIs)

#### E09: Advanced Alert Features (6 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 188 | POST /alerts/correlate | 7 | 4 | 4 | 1.12 | 17d | Alert correlation |
| 189 | GET /alerts/patterns | 6 | 5 | 5 | 1.5 | 15d | Pattern detection |
| 190 | POST /alerts/auto-respond | 8 | 3 | 3 | 0.72 | 22d | Auto-response |
| 191 | GET /alerts/recommendations | 7 | 4 | 4 | 1.12 | 17d | AI recommendations |
| 192 | POST /alerts/ml-tuning | 6 | 4 | 4 | 0.96 | 18d | ML tuning |
| 193 | GET /alerts/false-positive-rate | 6 | 5 | 5 | 1.5 | 15d | FP analysis |

**Sprint 11+ Focus:** AI-powered alert management (APIs 188-193)
**Business Value:** Intelligent alert correlation and auto-response

### Phase B2: Advanced Equipment Features (5 APIs)

#### E15: Extended Equipment Analytics (5 APIs)

| # | Endpoint | Impact | Confidence | Ease | ICE | Time | Dependencies |
|---|----------|--------|------------|------|-----|------|--------------|
| 194 | POST /equipment/predict-failures | 7 | 3 | 3 | 0.63 | 24d | Predictive maintenance |
| 195 | GET /equipment/optimization/recommendations | 6 | 4 | 4 | 0.96 | 18d | Optimization AI |
| 196 | POST /equipment/capacity-planning | 7 | 4 | 3 | 0.84 | 20d | Capacity models |

**Sprint 11+ Focus:** Predictive equipment management (APIs 194-196)
**Business Value:** AI-powered equipment lifecycle optimization

---

## IMPLEMENTATION TIMELINE

### Sprint 1 (Week 1-2): Foundation - SBOM & Equipment Core
**Team:** 3 developers | **APIs:** 15 | **Focus:** Quick wins, data ingestion

**Deliverables:**
- SBOM analysis (APIs 1-8): Ingest, parse, query SBOMs
- Equipment CRUD (APIs 9-15): Basic lifecycle tracking
- Database schemas for SBOM components and equipment
- Initial API documentation and Swagger specs

**Dependencies:** Neo4j schemas, file upload handlers, customer isolation headers

**Success Criteria:**
- Upload SBOM file and extract vulnerabilities
- Create equipment records and track EOL status
- Multi-tenant data isolation verified

---

### Sprint 2 (Week 3-4): Threat Intelligence Foundation
**Team:** 4 developers | **APIs:** 32 | **Focus:** Threat actors, campaigns, economic dashboards

**Deliverables:**
- Threat actors (APIs 16-22): CRUD + sector targeting
- Campaigns (APIs 23-27): Campaign tracking
- MITRE mapping (APIs 28-33): ATT&CK integration
- Economic dashboards (APIs 34-47): Cost/ROI visibility

**Dependencies:** MITRE ATT&CK data ingestion, cost calculation models

**Success Criteria:**
- Create threat actors and link to campaigns
- Map threats to MITRE techniques
- Display cost/ROI dashboards for executives

---

### Sprint 3-4 (Week 5-8): Risk Scoring Engine
**Team:** 5 developers | **APIs:** 26 | **Focus:** Comprehensive risk quantification

**Deliverables:**
- Risk scores (APIs 48-54): Calculate and track risk
- Asset criticality (APIs 55-60): Mission-critical asset identification
- Exposure scores (APIs 61-65): Internet-facing risk
- Risk aggregation (APIs 66-73): Vendor/sector/asset type views

**Dependencies:** Risk calculation algorithms, CVSS/EPSS integration, asset inventory

**Success Criteria:**
- Calculate risk scores for all assets
- Identify mission-critical assets
- Generate risk dashboards by vendor and sector

---

### Sprint 5 (Week 9-10): Remediation, IOCs, Compliance
**Team:** 4 developers | **APIs:** 30 | **Focus:** Remediation workflows, threat feeds, compliance

**Deliverables:**
- Remediation (APIs 74-79): Workflow automation
- IOCs (APIs 80-91): Threat feed integration
- Compliance (APIs 92-99): Framework mapping
- Scanning (APIs 100-103): Vulnerability scanning
- Business value (APIs 104-111): Value metrics and demographics

**Dependencies:** Workflow engine, threat feed APIs, compliance framework data, scanner integration

**Success Criteria:**
- Create and track remediation plans
- Ingest IOCs from threat feeds
- Map controls to NIST/ISO frameworks
- Schedule automated scans

---

### Sprint 6-7 (Week 11-14): Alert Management
**Team:** 3 developers | **APIs:** 15 | **Focus:** Alert lifecycle and analytics

**Deliverables:**
- Alert CRUD (APIs 112-119): Alert creation and tracking
- Alert rules (APIs 120-123): Custom alert rules
- Alert analytics (APIs 124-126): Trend analysis and export

**Dependencies:** Alert rule engine, notification services

**Success Criteria:**
- Create alerts from vulnerabilities and threats
- Define custom alert rules
- Analyze alert trends over time

---

### Sprint 8-9 (Week 15-18): Advanced Analytics
**Team:** 4 developers | **APIs:** 28 | **Focus:** SBOM analytics, equipment analytics, scanning features

**Deliverables:**
- Advanced SBOM (APIs 142-149): Dependency graphs, compliance
- Equipment analytics (APIs 150-156): Age distribution, vendor coverage
- Advanced scanning (APIs 157-165): Findings management, policies
- Compliance evidence (APIs 166-169): Audit trail

**Dependencies:** Graph algorithms, reporting engines

**Success Criteria:**
- Generate SBOM dependency graphs
- Analyze equipment age distribution
- Create scanning policies and track findings
- Collect compliance evidence for audits

---

### Sprint 10 (Week 19-20): Financial Impact & Prioritization
**Team:** 4 developers | **APIs:** 15 | **Focus:** Impact modeling, vulnerability prioritization

**Deliverables:**
- Impact modeling (APIs 127-136): Financial impact scenarios
- Prioritization (APIs 137-141): Vulnerability ranking

**Dependencies:** Monte Carlo simulation, EPSS data, prioritization algorithms

**Success Criteria:**
- Model financial impact of breaches
- Prioritize vulnerabilities by urgency
- Generate critical remediation path

---

### Sprint 11+ (Week 21+): Advanced AI Features
**Team:** 2-3 developers | **APIs:** 29 | **Focus:** ML-powered predictions, optimization

**Deliverables:**
- Demographics predictions (API 170): Team churn
- Advanced economics (APIs 171-179): What-if analysis, optimization
- Advanced threat intel (APIs 180-187): Attack prediction
- Advanced alerts (APIs 188-193): Auto-response
- Predictive equipment (APIs 194-196): Failure prediction

**Dependencies:** ML models, AI/ML infrastructure, training data

**Success Criteria:**
- Predict team churn with ML
- Optimize security investments with AI
- Predict attacks based on threat intelligence
- Auto-respond to common alerts

---

## RESOURCE ALLOCATION

### Team Structure

**Sprint 1-2 (4 weeks):**
- 1 Tech Lead (API architecture, schema design)
- 2 Backend Developers (SBOM, equipment, threat intel)
- 1 Frontend Developer (dashboard UI for quick wins)
- 1 QA Engineer (API testing, integration tests)

**Sprint 3-5 (6 weeks):**
- 1 Tech Lead (risk algorithms, compliance frameworks)
- 3 Backend Developers (risk scoring, remediation, IOCs)
- 1 Data Engineer (threat feed integration, MITRE data)
- 1 Frontend Developer (risk dashboards)
- 1 QA Engineer (end-to-end testing)

**Sprint 6-10 (10 weeks):**
- 1 Tech Lead (alert engine, analytics)
- 2 Backend Developers (alerts, scanning, analytics)
- 1 Data Engineer (impact modeling, EPSS integration)
- 1 Frontend Developer (analytics dashboards)
- 1 QA Engineer (regression testing)

**Sprint 11+ (2+ weeks):**
- 1 ML Engineer (predictive models, AI features)
- 1 Backend Developer (ML API integration)
- 1 Data Scientist (model training, optimization)

---

## DEPENDENCIES & PREREQUISITES

### Data Dependencies

**Threat Intelligence:**
- MITRE ATT&CK framework data (JSON export)
- Threat feed APIs (STIX/TAXII feeds, commercial feeds)
- CVE/NVD data (NIST NVD API)
- EPSS scores (FIRST.org API)
- KEV catalog (CISA API)

**Compliance:**
- NIST CSF framework mappings
- ISO 27001/27002 control mappings
- IEC 62443 control mappings
- CIS Controls mappings
- PCI-DSS requirements

**Equipment:**
- Vendor EOL databases (API integrations)
- CPE dictionary (NIST)
- Product lifecycle data

**Economic:**
- Industry benchmark data
- Cost models for security controls
- ROI calculation formulas

### Infrastructure Dependencies

**Databases:**
- Neo4j graph database (v5.0+)
- Qdrant vector database (v1.7+)
- PostgreSQL (for transactional data)
- Redis (for caching)

**External Services:**
- Scanner integrations (Nessus, Qualys, OpenVAS)
- Threat feed APIs (AlienVault, ThreatConnect, etc.)
- Notification services (email, Slack, PagerDuty)
- File storage (S3, MinIO)

**Authentication:**
- Clerk (multi-tenant customer isolation)
- RBAC implementation
- API key management

---

## RISK MITIGATION

### High-Risk APIs (Complex Algorithms)

**APIs with High Implementation Risk:**
1. POST /risk/scores (API 48) - Risk calculation algorithm
2. POST /economic-impact/impact/simulate (API 129) - Monte Carlo simulation
3. POST /prioritization/critical-path (API 140) - Path algorithm
4. GET /compliance/frameworks/gap-analysis (API 94) - Gap analysis logic
5. POST /scanning/scans (API 100) - Scanner integration

**Mitigation Strategies:**
- Prototype algorithms in Sprint 0
- Use existing open-source libraries where possible
- Create detailed technical design docs before implementation
- Build incremental versions (v1: basic, v2: advanced)
- Plan for 2x time estimates on first attempt

### API Integration Risks

**External Integrations with Unknown Reliability:**
- Vendor EOL APIs (may not exist)
- Threat feed APIs (rate limits, costs)
- Scanner integrations (diverse APIs)

**Mitigation Strategies:**
- Build mock data generators for development
- Implement circuit breakers and fallbacks
- Cache external data aggressively
- Create adapters for multiple vendor APIs

---

## SUCCESS METRICS

### Sprint-Level KPIs

**Sprint 1-2:**
- ✅ 15 APIs deployed to production
- ✅ SBOM upload and vulnerability extraction working
- ✅ Equipment lifecycle tracking functional
- ✅ Multi-tenant isolation verified

**Sprint 3-5:**
- ✅ 62 additional APIs deployed
- ✅ Risk scores calculated for all assets
- ✅ Remediation workflows automated
- ✅ Compliance dashboard showing framework gaps

**Sprint 6-10:**
- ✅ 58 additional APIs deployed
- ✅ Alert management fully operational
- ✅ Financial impact modeling complete
- ✅ Vulnerability prioritization algorithm validated

**Sprint 11+:**
- ✅ 29 AI-powered APIs deployed
- ✅ Predictive models trained and validated
- ✅ All 196 APIs in production

### Business Value Metrics

**Immediate Value (Sprint 1-2):**
- Time to identify SBOM vulnerabilities: < 5 minutes
- Equipment EOL tracking: 100% coverage
- Threat actor database: 100+ actors cataloged

**Short-Term Value (Sprint 3-5):**
- Risk score coverage: 100% of assets
- Remediation plan automation: 80% reduction in manual effort
- Compliance gap identification: < 1 hour per framework

**Long-Term Value (Sprint 6-10):**
- Alert response time: 50% reduction
- Vulnerability prioritization accuracy: 90%+
- Financial impact modeling: $10M+ potential savings identified

**Strategic Value (Sprint 11+):**
- Team churn prediction: 6-month advance warning
- Attack prediction accuracy: 75%+
- Security investment optimization: 20% ROI improvement

---

## NEXT STEPS

### Immediate Actions (Week 1)

1. **Architecture Review:**
   - Review API specifications with tech leads
   - Validate database schemas (Neo4j, Qdrant, PostgreSQL)
   - Confirm authentication approach (Clerk integration)
   - Design customer isolation strategy

2. **Environment Setup:**
   - Provision development, staging, production environments
   - Set up CI/CD pipelines for API deployment
   - Configure monitoring and observability (Datadog, Sentry)
   - Create API documentation infrastructure (Swagger/OpenAPI)

3. **Team Onboarding:**
   - Assign developers to Sprint 1 APIs
   - Review ICE prioritization with product team
   - Set up daily standups and sprint planning
   - Create ticket/task breakdown in Jira/Linear

4. **Data Acquisition:**
   - Download MITRE ATT&CK data
   - Set up threat feed trial accounts
   - Acquire NIST CSF/ISO 27001 framework mappings
   - Create sample SBOM files for testing

5. **Prototyping:**
   - Build risk scoring algorithm prototype
   - Test Neo4j graph traversal performance
   - Validate Qdrant semantic search accuracy
   - Create API request/response examples

### Sprint Planning (Week 1-2)

**Sprint 1 Kickoff:**
- Break down Tier 1 APIs into development tasks
- Assign SBOM APIs to Developer A
- Assign Equipment APIs to Developer B
- Assign database schema to Tech Lead
- Schedule API design review (Day 3)
- Schedule mid-sprint demo (Day 7)
- Schedule sprint retrospective (Day 14)

---

## APPENDIX: API DEPENDENCY GRAPH

### Critical Path APIs (Must Build First)

**Foundation Layer (Sprint 1):**
1. POST /sbom/analyze → Enables all SBOM features
2. POST /equipment → Enables all equipment features
3. POST /threat-intel/actors → Enables all threat intel features

**Core Analysis Layer (Sprint 2-3):**
4. POST /risk/scores → Enables all risk features
5. POST /threat-intel/mitre/mappings → Enables MITRE coverage
6. POST /economic-impact/costs/calculate → Enables all economic features

**Workflow Layer (Sprint 4-5):**
7. POST /remediation/remediation-plans → Enables remediation
8. POST /threat-intel/iocs → Enables IOC management
9. POST /compliance/frameworks → Enables compliance mapping

**Advanced Features Layer (Sprint 6-10):**
10. POST /alerts/alerts → Enables alert management
11. POST /scanning/scans → Enables scanning features
12. POST /economic-impact/impact/model → Enables impact modeling

**AI/ML Layer (Sprint 11+):**
13. POST /prioritization/prioritize → Enables prioritization
14. POST /demographics/predict-churn → Enables predictions

---

## QDRANT STORAGE

**Namespace:** `aeon-ice`
**Key:** `prioritization-matrix`

**Metadata:**
- total_apis: 196
- tier1_apis: 47
- tier2_apis: 62
- tier3_apis: 58
- tier4_apis: 29
- total_sprints: 11+
- total_weeks: 22+
- created: 2025-12-12T18:45:00Z
- version: 1.0.0

---

**END OF ICE PRIORITIZATION MATRIX**

*This document provides an actionable development roadmap for all 196 planned APIs. Development teams should start with Tier 1 APIs immediately and progress through tiers sequentially for maximum business value delivery.*
