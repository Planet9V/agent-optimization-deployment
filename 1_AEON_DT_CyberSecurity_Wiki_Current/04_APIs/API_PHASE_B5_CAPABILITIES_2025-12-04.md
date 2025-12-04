# Phase B5 - Advanced Analytics & Reporting APIs

**Document ID:** WIKI_API_PHASE_B5_2025-12-04
**Generated:** 2025-12-04 22:00:00 UTC
**Status:** PRODUCTION READY
**Phase:** B5 - Advanced Analytics & Reporting
**Version:** 1.0.0

---

## Overview

Phase B5 delivers three advanced analytics and reporting APIs for economic impact modeling, demographics baseline analytics, and intelligent prioritization. These APIs enable data-driven decision making through ROI calculations, workforce analytics, and risk-adjusted prioritization using the NOW-NEXT-NEVER framework.

### Phase B5 APIs Summary

| API | Base Path | Endpoints | Purpose | Status |
|-----|-----------|-----------|---------|--------|
| **E10 Economic Impact** | `/api/v2/economic-impact` | 26 | ROI calculations, cost analysis, financial impact modeling | ✅ Production |
| **E11 Demographics Baseline** | `/api/v2/demographics` | 24 | Population analytics, workforce modeling, organizational structure | ✅ Production |
| **E12 Prioritization** | `/api/v2/prioritization` | 28 | NOW-NEXT-NEVER risk-adjusted prioritization framework | ✅ Production |
| **TOTAL** | - | **78** | Complete analytics and prioritization capabilities | ✅ Production |

---

## E10 Economic Impact Modeling API

### Purpose
Calculate ROI, cost analysis, and financial impact for security investments. Provides comprehensive economic modeling including NPV, IRR, payback period calculations, and impact simulations for security scenarios.

### Base Path
```
/api/v2/economic-impact
```

### Qdrant Collection
```
Collection: ner11_economic_impact
Dimensions: 384
Model: sentence-transformers/all-MiniLM-L6-v2
```

### Capabilities

| Capability | Endpoints | Description |
|------------|-----------|-------------|
| **Cost Analysis** | 5 | Cost summary, by-category, entity breakdown, calculation, historical |
| **ROI Calculations** | 6 | ROI summary, by-id, calculate, by-category, projections, comparison |
| **Business Value** | 5 | Metrics, assessment, calculate, risk-adjusted, by-sector |
| **Impact Modeling** | 5 | Model, scenarios, simulate, results, historical |
| **Dashboard** | 5 | Summary, trends, KPIs, alerts, executive |

### Endpoint Reference

#### Cost Analysis (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/costs/summary` | Get cost summary dashboard for specified period |
| `GET` | `/costs/by-category` | Get costs grouped by category (equipment, personnel, downtime) |
| `GET` | `/costs/{entity_id}/breakdown` | Get detailed cost breakdown for specific entity |
| `POST` | `/costs/calculate` | Calculate costs for scenario with direct, indirect, opportunity costs |
| `GET` | `/costs/historical` | Get historical cost trends with direction and percentage change |

#### ROI Calculations (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/roi/summary` | Get aggregated ROI metrics, best/worst performers |
| `GET` | `/roi/{investment_id}` | Get detailed ROI for specific investment |
| `POST` | `/roi/calculate` | Calculate ROI percentage, NPV, IRR, payback period |
| `GET` | `/roi/by-category` | Get average ROI for each investment type |
| `GET` | `/roi/projections` | Get future ROI projections with confidence intervals |
| `POST` | `/roi/comparison` | Side-by-side comparison of investment options |

#### Business Value (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/value/metrics` | Get business value metrics dashboard |
| `GET` | `/value/{asset_id}/assessment` | Get value assessment for specific asset |
| `POST` | `/value/calculate` | Calculate business value from multiple factors |
| `GET` | `/value/risk-adjusted` | Get risk-adjusted business value (E08 integration) |
| `GET` | `/value/by-sector` | Get value metrics by industry sector |

#### Impact Modeling (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/impact/model` | Model financial impact of security incident |
| `GET` | `/impact/scenarios` | List available impact scenarios |
| `POST` | `/impact/simulate` | Run Monte Carlo impact simulation |
| `GET` | `/impact/{scenario_id}/results` | Get simulation results for scenario |
| `GET` | `/impact/historical` | Get actual vs estimated costs from past incidents |

#### Dashboard (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/dashboard/summary` | Comprehensive dashboard with all key metrics |
| `GET` | `/dashboard/trends` | Time-series data for costs, ROI, value, impacts |
| `GET` | `/dashboard/kpis` | Critical KPIs for security investment performance |
| `GET` | `/dashboard/alerts` | Active alerts for budget overruns, low ROI |
| `GET` | `/dashboard/executive` | Executive summary for reporting |

### Data Models

```typescript
enum CostCategory {
  EQUIPMENT = "equipment",
  PERSONNEL = "personnel",
  DOWNTIME = "downtime",
  INCIDENT_RESPONSE = "incident_response",
  REMEDIATION = "remediation",
  COMPLIANCE = "compliance",
  TRAINING = "training",
  INFRASTRUCTURE = "infrastructure"
}

enum InvestmentCategory {
  SECURITY_TOOLS = "security_tools",
  INFRASTRUCTURE = "infrastructure",
  TRAINING = "training",
  COMPLIANCE = "compliance",
  INCIDENT_RESPONSE = "incident_response",
  PERSONNEL = "personnel"
}

interface ROICalculation {
  investment_id: string;
  customer_id: string;
  name: string;
  initial_investment: number;
  annual_benefits: number;
  annual_costs: number;
  roi_percentage: number;
  npv: number;               // Net Present Value
  irr: number;               // Internal Rate of Return
  payback_period_months: number;
  risk_adjusted_roi: number;
  confidence_score: number;
}

interface ImpactSimulation {
  scenario_id: string;
  customer_id: string;
  scenario_type: string;
  total_impact: number;
  direct_costs: number;
  indirect_costs: number;
  opportunity_costs: number;
  recovery_time_hours: number;
  confidence_low: number;
  confidence_high: number;
}
```

### Example: Calculate ROI

**Request:**
```bash
curl -X POST "https://api.ner11.com/api/v2/economic-impact/roi/calculate" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Customer-ID: customer_123" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SIEM Platform Investment",
    "initial_investment": 500000,
    "annual_benefits": 250000,
    "annual_costs": 50000,
    "years": 5,
    "discount_rate": 0.08,
    "category": "security_tools"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "investment_id": "inv-2024-001",
    "customer_id": "customer_123",
    "name": "SIEM Platform Investment",
    "roi_percentage": 300.0,
    "npv": 475234.56,
    "irr": 0.42,
    "payback_period_months": 30,
    "risk_adjusted_roi": 285.0,
    "confidence_score": 0.85
  },
  "message": "ROI calculated: 300.00%"
}
```

---

## E11 Demographics Baseline API

### Purpose
Provide population analytics, workforce modeling, and organizational structure analysis for psychohistory baseline metrics. Supports GDPR-compliant personnel analytics with integration to E09 Alert Management.

### Base Path
```
/api/v2/demographics
```

### Qdrant Collection
```
Collection: ner11_demographics
Dimensions: 384
Model: sentence-transformers/all-MiniLM-L6-v2
```

### Capabilities

| Capability | Endpoints | Description |
|------------|-----------|-------------|
| **Population Metrics** | 5 | Summary, distribution, profile, trends, query |
| **Workforce Analytics** | 5 | Composition, skills, turnover, team profile, capacity |
| **Organization Structure** | 5 | Hierarchy, units, details, relationships, analyze |
| **Role Analysis** | 4 | Distribution, demographics, security-relevant, access patterns |
| **Dashboard** | 5 | Summary, baseline, indicators, alerts, trends |

### Endpoint Reference

#### Population Metrics (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/population/summary` | Total population, active employees, growth rate, stability index |
| `GET` | `/population/distribution` | Distribution by age group, tenure, education, department |
| `GET` | `/population/{org_unit_id}/profile` | Demographic profile for organizational unit |
| `GET` | `/population/trends` | Historical trends and 90-day forecast |
| `POST` | `/population/query` | Execute custom population query with filters |

#### Workforce Analytics (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/workforce/composition` | Composition by role, department, turnover metrics |
| `GET` | `/workforce/skills` | Skills inventory by category, critical skills, gaps |
| `GET` | `/workforce/turnover` | Turnover rate, predictions, high-risk employees |
| `GET` | `/workforce/{team_id}/profile` | Team demographics, cohesion score, diversity index |
| `GET` | `/workforce/capacity` | Total capacity, utilization, overutilized teams |

#### Organization Structure (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/organization/hierarchy` | Complete organizational structure with units |
| `GET` | `/organization/units` | List all units with employee counts |
| `GET` | `/organization/{unit_id}/details` | Detailed unit information with demographics |
| `GET` | `/organization/relationships` | Inter-unit relationships |
| `POST` | `/organization/analyze` | Span of control, depth, bottleneck detection |

#### Role Analysis (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/roles/distribution` | All roles with counts and security relevance |
| `GET` | `/roles/{role_id}/demographics` | Demographics for employees in role |
| `GET` | `/roles/security-relevant` | Roles with security implications |
| `GET` | `/roles/access-patterns` | Normal access patterns and anomalies |

#### Dashboard (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/dashboard/summary` | Comprehensive demographics dashboard |
| `GET` | `/dashboard/baseline` | Key metrics for psychohistory calculations |
| `GET` | `/dashboard/indicators` | Monitored indicators with thresholds |
| `GET` | `/dashboard/alerts` | Demographic alerts and anomalies |
| `GET` | `/dashboard/trends` | Trend analysis with forecasting |

### Data Models

```typescript
interface PopulationSummary {
  customer_id: string;
  total_population: number;
  active_employees: number;
  contractors: number;
  growth_rate: number;
  stability_index: number;
  by_department: Record<string, number>;
  by_location: Record<string, number>;
}

interface WorkforceComposition {
  customer_id: string;
  by_role: Record<string, number>;
  by_department: Record<string, number>;
  average_tenure_months: number;
  turnover_rate: number;
  headcount_trend: "growing" | "stable" | "declining";
}

interface BaselineMetrics {
  customer_id: string;
  population_stability_index: number;  // 0-1
  role_diversity_score: number;        // 0-1
  skill_concentration_risk: number;    // 0-10
  succession_coverage: number;         // 0-1
  insider_threat_baseline: number;     // 0-10
  calculated_at: string;
}

interface TeamProfile {
  team_id: string;
  customer_id: string;
  team_name: string;
  member_count: number;
  average_tenure_months: number;
  cohesion_score: number;
  diversity_index: number;
  skill_coverage: Record<string, number>;
  risk_factors: string[];
}
```

### Example: Get Baseline Metrics

**Request:**
```bash
curl -X GET "https://api.ner11.com/api/v2/demographics/dashboard/baseline" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Customer-ID: customer_123"
```

**Response:**
```json
{
  "customer_id": "customer_123",
  "population_stability_index": 0.87,
  "role_diversity_score": 0.72,
  "skill_concentration_risk": 3.5,
  "succession_coverage": 0.65,
  "insider_threat_baseline": 2.1,
  "indicators": [
    {"name": "turnover_rate", "value": 0.12, "threshold": 0.15, "status": "healthy"},
    {"name": "skill_gaps", "value": 5, "threshold": 10, "status": "healthy"},
    {"name": "key_person_risk", "value": 8, "threshold": 5, "status": "warning"}
  ],
  "calculated_at": "2025-12-04T22:00:00Z"
}
```

---

## E12 NOW-NEXT-NEVER Prioritization API

### Purpose
Implement risk-adjusted prioritization using the NOW-NEXT-NEVER framework for remediation sequencing. Calculates priority scores based on urgency, risk, impact, effort, and ROI factors.

### Base Path
```
/api/v2/prioritization
```

### Qdrant Collection
```
Collection: ner11_prioritization
Dimensions: 384
Model: sentence-transformers/all-MiniLM-L6-v2
```

### Priority Scoring Formula

```
priority_score = (
    urgency_score × 25% × 100 +
    risk_score × 30% × 10 +
    impact_score × 25% × 10 +
    (10 - effort_score) × 10% × 10 +
    roi_score × 10% × 10
)

Thresholds:
  NOW:   score >= 70
  NEXT:  score >= 40 AND score < 70
  NEVER: score < 40
```

### Capabilities

| Capability | Endpoints | Description |
|------------|-----------|-------------|
| **NOW Category** | 6 | Items, summary, details, escalate, SLA-status, complete |
| **NEXT Category** | 6 | Items, summary, details, schedule, queue, promote |
| **NEVER Category** | 4 | Items, summary, classify, reconsider |
| **Priority Scoring** | 6 | Calculate, breakdown, factors, weights, thresholds, batch |
| **Dashboard** | 6 | Summary, distribution, trends, efficiency, backlog, executive |

### Endpoint Reference

#### NOW Category (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/now/items` | Get all items requiring immediate action |
| `GET` | `/now/summary` | NOW category summary with SLA metrics |
| `GET` | `/now/{item_id}/details` | Detailed item information with urgency factors |
| `POST` | `/now/escalate` | Escalate item to NOW priority |
| `GET` | `/now/sla-status` | Get NOW items by SLA status |
| `POST` | `/now/complete` | Mark NOW item as complete (archive) |

#### NEXT Category (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/next/items` | Get all items scheduled for next action cycle |
| `GET` | `/next/summary` | NEXT category summary |
| `GET` | `/next/{item_id}/details` | Detailed NEXT item with scheduling |
| `POST` | `/next/schedule` | Schedule item for NEXT priority |
| `GET` | `/next/queue` | Get ordered NEXT queue by priority score |
| `POST` | `/next/promote` | Promote NEXT item to NOW priority |

#### NEVER Category (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/never/items` | Get all items designated as NEVER |
| `GET` | `/never/summary` | NEVER category summary |
| `POST` | `/never/classify` | Classify item as NEVER priority |
| `POST` | `/never/reconsider` | Move NEVER item for reconsideration |

#### Priority Scoring (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/score/calculate` | Calculate priority score for entity |
| `GET` | `/score/{entity_id}/breakdown` | Get priority score breakdown by factors |
| `GET` | `/score/factors` | List all available scoring factors |
| `POST` | `/score/weights` | Configure scoring weights for customer |
| `GET` | `/score/thresholds` | Get priority thresholds configuration |
| `POST` | `/score/batch` | Batch priority calculation for multiple entities |

#### Dashboard (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/dashboard/summary` | Comprehensive prioritization dashboard |
| `GET` | `/dashboard/distribution` | NOW/NEXT/NEVER distribution |
| `GET` | `/dashboard/trends` | Priority trends over time |
| `GET` | `/dashboard/efficiency` | Remediation efficiency metrics |
| `GET` | `/dashboard/backlog` | Backlog analysis with aging buckets |
| `GET` | `/dashboard/executive` | Executive prioritization view |

### Data Models

```typescript
enum PriorityCategory {
  NOW = "NOW",      // Immediate action required (score >= 70)
  NEXT = "NEXT",    // Scheduled for next cycle (40 <= score < 70)
  NEVER = "NEVER"   // Low priority or accepted risk (score < 40)
}

enum SLAStatus {
  WITHIN_SLA = "within_sla",
  AT_RISK = "at_risk",
  BREACHED = "breached"
}

enum EntityType {
  VULNERABILITY = "vulnerability",
  REMEDIATION_TASK = "remediation_task",
  ASSET = "asset",
  THREAT = "threat",
  COMPLIANCE_GAP = "compliance_gap"
}

interface PriorityItem {
  item_id: string;
  customer_id: string;
  entity_type: EntityType;
  entity_id: string;
  entity_name: string;
  priority_category: PriorityCategory;
  priority_score: number;
  urgency_factors: UrgencyFactor[];
  risk_factors: RiskFactor[];
  economic_factors: EconomicFactor[];
  deadline: string | null;
  sla_status: SLAStatus;
  sla_deadline: string | null;
  calculated_at: string;
}

interface UrgencyFactor {
  factor_type: string;   // exploit_available, active_campaign, compliance_deadline, business_critical
  weight: number;
  value: number;
  description: string;
  deadline: string | null;
  evidence: string[];
}

interface ScoringFactor {
  category: string;
  factors: {
    risk: string[];      // vulnerability_score, threat_score, exposure_score, asset_score
    urgency: string[];   // exploit_available, active_campaign, compliance_deadline
    impact: string[];    // financial, operational, reputational, compliance
    effort: string[];    // complexity, resource_requirements, dependencies
    roi: string[];       // cost_savings, risk_reduction_value, business_value
  }
}
```

### Example: Calculate Priority Score

**Request:**
```bash
curl -X POST "https://api.ner11.com/api/v2/prioritization/score/calculate" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Customer-ID: customer_123" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "vulnerability",
    "entity_id": "CVE-2024-21762",
    "entity_name": "FortiOS SSL VPN RCE",
    "urgency_factors": [
      {"factor_type": "exploit_available", "weight": 1.0, "value": 10.0, "description": "Active exploitation in wild"},
      {"factor_type": "active_campaign", "weight": 0.8, "value": 9.0, "description": "APT targeting energy sector"}
    ],
    "risk_factors": [
      {"factor_type": "vulnerability_score", "weight": 1.0, "value": 9.8, "description": "CVSS 9.8 Critical"},
      {"factor_type": "exposure_score", "weight": 0.9, "value": 8.5, "description": "Internet-facing devices"}
    ],
    "economic_factors": [
      {"factor_type": "potential_impact", "weight": 1.0, "value": 5000000, "description": "Estimated breach cost", "currency": "USD"}
    ]
  }'
```

**Response:**
```json
{
  "item_id": "pri-2024-001",
  "customer_id": "customer_123",
  "entity_type": "vulnerability",
  "entity_id": "CVE-2024-21762",
  "entity_name": "FortiOS SSL VPN RCE",
  "priority_category": "NOW",
  "priority_score": 94.5,
  "deadline": null,
  "sla_status": "at_risk",
  "sla_deadline": "2025-12-05T22:00:00Z",
  "calculated_at": "2025-12-04T22:00:00Z",
  "is_now": true,
  "is_sla_at_risk": true
}
```

---

## Cross-API Integration

### Phase B5 Internal Integration

| Source API | Target API | Integration |
|------------|------------|-------------|
| E10 Economic | E12 Prioritization | ROI factors for priority scoring |
| E11 Demographics | E12 Prioritization | Workforce capacity for effort estimation |
| E11 Demographics | E10 Economic | Personnel costs and productivity metrics |

### Integration with Prior Phases

| Source | Target | Integration |
|--------|--------|-------------|
| E08 RAMS (B4) | E10 Economic | Risk scores for impact modeling |
| E06 Remediation (B3) | E12 Prioritization | Task prioritization workflow |
| E05 Risk Scoring (B3) | E12 Prioritization | Risk factors for NOW/NEXT/NEVER |
| E09 Alerts (B4) | E11 Demographics | Alert correlation with insider threats |
| E03 SBOM (B2) | E10 Economic | Component cost analysis |

---

## Authentication & Authorization

### Required Header
```
X-Customer-ID: {customer_id}
```

All Phase B5 endpoints require the `X-Customer-ID` header for multi-tenant customer isolation.

### Access Levels

| Level | Permissions |
|-------|-------------|
| `READ` | View all data, dashboards, summaries |
| `WRITE` | Calculate, escalate, promote, classify |
| `ADMIN` | Configure weights, thresholds, settings |

---

## Test Coverage

| API | Tests | Status |
|-----|-------|--------|
| E10 Economic Impact | 85/85 | ✅ PASSING |
| E11 Demographics Baseline | 85/85 | ✅ PASSING |
| E12 Prioritization | 85/85 | ✅ PASSING |

**Phase B5 Total**: 255 tests passing

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-04 22:00 | 1.0.0 | E10 + E11 + E12 complete (78 endpoints) |

---

**Document**: WIKI_API_PHASE_B5_2025-12-04
**Generated**: 2025-12-04 22:00:00 UTC
**AEON Digital Twin Cybersecurity Platform**
