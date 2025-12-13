# AEON API Complete Reference

**API Version:** 3.3.0
**Base URL:** `http://localhost:8000`
**Authentication:** X-Customer-ID header required
**Total Endpoints:** 230
**Last Updated:** 2025-12-13

---

## Table of Contents

1. [Authentication](#authentication)
2. [Phase B2: SBOM Management (33 endpoints)](#phase-b2-sbom-management)
3. [Phase B2: Vendor & Equipment (19 endpoints)](#phase-b2-vendor--equipment)
4. [Phase B3: Threat Intelligence (25 endpoints)](#phase-b3-threat-intelligence)
5. [Phase B3: Risk Management (27 endpoints)](#phase-b3-risk-management)
6. [Phase B3: Remediation (26 endpoints)](#phase-b3-remediation)
7. [Phase B4: Compliance (21 endpoints)](#phase-b4-compliance)
8. [Phase B5: Alerts (19 endpoints)](#phase-b5-alerts)
9. [Phase B5: Demographics (24 endpoints)](#phase-b5-demographics)
10. [Phase B5: Economic Analysis (27 endpoints)](#phase-b5-economic-analysis)
11. [Psychometric Analysis (8 endpoints)](#psychometric-analysis)
12. [Search Services (3 endpoints)](#search-services)
13. [System Health (1 endpoint)](#system-health)

---

## Authentication

All API endpoints require the `X-Customer-ID` header:

```bash
curl -H "X-Customer-ID: your-customer-id" \
     http://localhost:8000/api/v2/sbom/sboms
```

---

## Phase B2: SBOM Management

**Total Endpoints:** 33
**Purpose:** Software Bill of Materials management, component tracking, vulnerability analysis

### Core SBOM Operations

#### `GET, POST` /api/v2/sbom/sboms
List all SBOMs or create new SBOM

**GET Example:**
```bash
curl -H "X-Customer-ID: customer123" http://localhost:8000/api/v2/sbom/sboms
```

**POST Example:**
```bash
curl -X POST -H "X-Customer-ID: customer123" \
     -H "Content-Type: application/json" \
     -d '{"name": "myapp-v1.0", "format": "cyclonedx"}' \
     http://localhost:8000/api/v2/sbom/sboms
```

#### `GET, DELETE` /api/v2/sbom/sboms/{sbom_id}
Get or delete specific SBOM

#### `GET` /api/v2/sbom/sboms/{sbom_id}/risk-summary
Get risk summary for SBOM

#### `GET` /api/v2/sbom/sboms/{sbom_id}/components
List all components in SBOM

#### `GET` /api/v2/sbom/sboms/{sbom_id}/graph-stats
Get graph statistics for SBOM

#### `GET` /api/v2/sbom/sboms/{sbom_id}/cycles
Detect dependency cycles

#### `GET` /api/v2/sbom/sboms/{sbom_id}/vulnerable-paths
Find vulnerable dependency paths

#### `GET` /api/v2/sbom/sboms/{sbom_id}/remediation
Get remediation guidance

#### `GET` /api/v2/sbom/sboms/{sbom_id}/license-compliance
Check license compliance

#### `POST` /api/v2/sbom/sboms/{sbom_id}/correlate-equipment
Correlate SBOM with equipment

### Component Management

#### `POST` /api/v2/sbom/components
Create new component

#### `GET` /api/v2/sbom/components/{component_id}
Get component details

#### `GET, POST` /api/v2/sbom/components/search
Search components

#### `GET` /api/v2/sbom/components/vulnerable
List vulnerable components

#### `GET` /api/v2/sbom/components/high-risk
List high-risk components

#### `GET` /api/v2/sbom/components/{component_id}/dependencies
Get component dependencies

#### `GET` /api/v2/sbom/components/{component_id}/dependents
Get components depending on this

#### `GET` /api/v2/sbom/components/{component_id}/impact
Assess impact of component

#### `GET` /api/v2/sbom/components/{component_id}/vulnerabilities
List vulnerabilities in component

### Dependency Management

#### `POST` /api/v2/sbom/dependencies
Create dependency relationship

#### `GET` /api/v2/sbom/dependencies/path
Find dependency path between components

### Vulnerability Management

#### `POST` /api/v2/sbom/vulnerabilities
Create vulnerability record

#### `GET` /api/v2/sbom/vulnerabilities/{vulnerability_id}
Get vulnerability details

#### `GET` /api/v2/sbom/vulnerabilities/search
Search vulnerabilities

#### `GET` /api/v2/sbom/vulnerabilities/critical
List critical vulnerabilities

#### `GET` /api/v2/sbom/vulnerabilities/kev
List Known Exploited Vulnerabilities (KEV)

#### `GET` /api/v2/sbom/vulnerabilities/epss-prioritized
List vulnerabilities prioritized by EPSS score

#### `GET` /api/v2/sbom/vulnerabilities/by-apt
List vulnerabilities by APT group

#### `POST` /api/v2/sbom/vulnerabilities/{vulnerability_id}/acknowledge
Acknowledge vulnerability

### Dashboard & Analysis

#### `GET` /api/v2/sbom/dashboard/summary
Get SBOM dashboard summary

#### `POST` /api/v2/sbom/analyze
Analyze SBOM file

---

## Phase B2: Vendor & Equipment

**Total Endpoints:** 19
**Purpose:** Vendor risk management, equipment lifecycle tracking, maintenance scheduling

### Vendor Management

#### `GET, POST` /api/v2/vendor-equipment/vendors
List vendors or create new vendor

**Example:**
```bash
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/vendor-equipment/vendors
```

#### `GET` /api/v2/vendor-equipment/vendors/{vendor_id}
Get vendor details

#### `GET` /api/v2/vendor-equipment/vendors/{vendor_id}/risk-summary
Get vendor risk summary

#### `GET` /api/v2/vendor-equipment/vendors/high-risk
List high-risk vendors

### Equipment Management

#### `GET, POST` /api/v2/vendor-equipment/equipment
List equipment or register new equipment

#### `GET` /api/v2/vendor-equipment/equipment/{model_id}
Get equipment model details

#### `GET` /api/v2/vendor-equipment/equipment/approaching-eol
List equipment approaching End-of-Life

#### `GET` /api/v2/vendor-equipment/equipment/eol
List End-of-Life equipment

### Maintenance Management

#### `GET` /api/v2/vendor-equipment/maintenance-schedule
Get maintenance schedule

#### `GET, POST` /api/v2/vendor-equipment/maintenance-windows
Manage maintenance windows

#### `GET, DELETE` /api/v2/vendor-equipment/maintenance-windows/{window_id}
Get or delete maintenance window

#### `POST` /api/v2/vendor-equipment/maintenance-windows/check-conflict
Check for maintenance conflicts

#### `GET` /api/v2/vendor-equipment/predictive-maintenance/{equipment_id}
Get predictive maintenance insights

#### `GET` /api/v2/vendor-equipment/predictive-maintenance/forecast
Forecast maintenance needs

### Work Order Management

#### `GET, POST` /api/v2/vendor-equipment/work-orders
List or create work orders

#### `GET` /api/v2/vendor-equipment/work-orders/{work_order_id}
Get work order details

#### `PATCH` /api/v2/vendor-equipment/work-orders/{work_order_id}/status
Update work order status

#### `GET` /api/v2/vendor-equipment/work-orders/summary
Get work order summary

### Vulnerability Flagging

#### `POST` /api/v2/vendor-equipment/vulnerabilities/flag
Flag equipment vulnerability

---

## Phase B3: Threat Intelligence

**Total Endpoints:** 25
**Purpose:** Threat actor tracking, campaign monitoring, IOC management, MITRE ATT&CK mapping

### Threat Actor Management

#### `POST` /api/v2/threat-intel/actors
Create threat actor profile

#### `GET` /api/v2/threat-intel/actors/{actor_id}
Get threat actor details

#### `GET` /api/v2/threat-intel/actors/search
Search threat actors

#### `GET` /api/v2/threat-intel/actors/active
List active threat actors

#### `GET` /api/v2/threat-intel/actors/by-sector/{sector}
List actors targeting sector

#### `GET` /api/v2/threat-intel/actors/{actor_id}/campaigns
Get campaigns by actor

#### `GET` /api/v2/threat-intel/actors/{actor_id}/cves
Get CVEs associated with actor

### Campaign Management

#### `POST` /api/v2/threat-intel/campaigns
Create campaign record

#### `GET` /api/v2/threat-intel/campaigns/{campaign_id}
Get campaign details

#### `GET` /api/v2/threat-intel/campaigns/search
Search campaigns

#### `GET` /api/v2/threat-intel/campaigns/active
List active campaigns

#### `GET` /api/v2/threat-intel/campaigns/{campaign_id}/iocs
Get IOCs from campaign

### MITRE ATT&CK Mapping

#### `POST` /api/v2/threat-intel/mitre/mappings
Create MITRE ATT&CK mapping

#### `GET` /api/v2/threat-intel/mitre/mappings/entity/{entity_type}/{entity_id}
Get MITRE mappings for entity

#### `GET` /api/v2/threat-intel/mitre/techniques/{technique_id}/actors
Get actors using technique

#### `GET` /api/v2/threat-intel/mitre/coverage
Get MITRE ATT&CK coverage

#### `GET` /api/v2/threat-intel/mitre/gaps
Identify MITRE coverage gaps

### Indicator of Compromise (IOC) Management

#### `POST` /api/v2/threat-intel/iocs
Create IOC

#### `POST` /api/v2/threat-intel/iocs/bulk
Bulk import IOCs

#### `GET` /api/v2/threat-intel/iocs/search
Search IOCs

#### `GET` /api/v2/threat-intel/iocs/active
List active IOCs

#### `GET` /api/v2/threat-intel/iocs/by-type/{ioc_type}
List IOCs by type

### Threat Feeds

#### `GET, POST` /api/v2/threat-intel/feeds
Manage threat intelligence feeds

#### `PUT` /api/v2/threat-intel/feeds/{feed_id}/refresh
Refresh threat feed

### Dashboard

#### `GET` /api/v2/threat-intel/dashboard/summary
Get threat intelligence dashboard

---

## Phase B3: Risk Management

**Total Endpoints:** 27
**Purpose:** Risk scoring, asset criticality, exposure analysis, risk aggregation

### Risk Scoring

#### `POST` /api/v2/risk/scores
Create risk score

#### `GET` /api/v2/risk/scores/{entity_type}/{entity_id}
Get risk score for entity

#### `GET` /api/v2/risk/scores/high-risk
List high-risk entities

#### `GET` /api/v2/risk/scores/trending
Get trending risk scores

#### `GET` /api/v2/risk/scores/search
Search risk scores

#### `POST` /api/v2/risk/scores/recalculate/{entity_type}/{entity_id}
Recalculate risk score

#### `GET` /api/v2/risk/scores/history/{entity_type}/{entity_id}
Get risk score history

### Asset Criticality

#### `POST` /api/v2/risk/assets/criticality
Set asset criticality

#### `GET, PUT` /api/v2/risk/assets/{asset_id}/criticality
Manage asset criticality

#### `GET` /api/v2/risk/assets/mission-critical
List mission-critical assets

#### `GET` /api/v2/risk/assets/by-criticality/{level}
List assets by criticality level

#### `GET` /api/v2/risk/assets/criticality/summary
Get criticality summary

### Exposure Analysis

#### `POST` /api/v2/risk/exposure
Create exposure record

#### `GET` /api/v2/risk/exposure/{asset_id}
Get asset exposure

#### `GET` /api/v2/risk/exposure/internet-facing
List internet-facing assets

#### `GET` /api/v2/risk/exposure/high-exposure
List high-exposure assets

#### `GET` /api/v2/risk/exposure/attack-surface
Get attack surface analysis

### Risk Aggregation

#### `GET` /api/v2/risk/aggregation/by-vendor
Aggregate risk by vendor

#### `GET` /api/v2/risk/aggregation/by-sector
Aggregate risk by sector

#### `GET` /api/v2/risk/aggregation/by-asset-type
Aggregate risk by asset type

#### `GET` /api/v2/risk/aggregation/{aggregation_type}/{group_id}
Get custom risk aggregation

### Dashboard

#### `GET` /api/v2/risk/dashboard/summary
Get risk dashboard summary

#### `GET` /api/v2/risk/dashboard/risk-matrix
Get risk matrix visualization

---

## Phase B3: Remediation

**Total Endpoints:** 26
**Purpose:** Remediation planning, patch management, mitigation tracking, compensating controls

### Remediation Plans

#### `GET, POST` /api/v2/remediation/plans
List or create remediation plans

#### `GET` /api/v2/remediation/plans/{plan_id}
Get remediation plan details

#### `GET` /api/v2/remediation/plans/active
List active remediation plans

#### `GET` /api/v2/remediation/plans/overdue
List overdue remediation plans

#### `GET` /api/v2/remediation/plans/{plan_id}/components
Get plan components

#### `PATCH` /api/v2/remediation/plans/{plan_id}/status
Update plan status

### Patch Management

#### `GET, POST` /api/v2/remediation/patches
Manage patches

#### `GET` /api/v2/remediation/patches/{patch_id}
Get patch details

#### `GET` /api/v2/remediation/patches/available
List available patches

#### `GET` /api/v2/remediation/patches/critical
List critical patches

#### `GET` /api/v2/remediation/patches/{vulnerability_id}/recommended
Get recommended patches

#### `POST` /api/v2/remediation/patches/{patch_id}/apply
Apply patch

### Mitigation Strategies

#### `GET, POST` /api/v2/remediation/mitigations
Manage mitigations

#### `GET` /api/v2/remediation/mitigations/{mitigation_id}
Get mitigation details

#### `GET` /api/v2/remediation/mitigations/active
List active mitigations

#### `GET` /api/v2/remediation/mitigations/{vulnerability_id}/strategies
Get mitigation strategies

#### `POST` /api/v2/remediation/mitigations/{mitigation_id}/validate
Validate mitigation effectiveness

### Compensating Controls

#### `GET, POST` /api/v2/remediation/compensating-controls
Manage compensating controls

#### `GET` /api/v2/remediation/compensating-controls/{control_id}
Get control details

#### `GET` /api/v2/remediation/compensating-controls/{vulnerability_id}/applicable
Get applicable controls

#### `POST` /api/v2/remediation/compensating-controls/{control_id}/assess
Assess control effectiveness

### Workflow Management

#### `GET, POST` /api/v2/remediation/workflows
Manage remediation workflows

#### `GET` /api/v2/remediation/workflows/{workflow_id}
Get workflow details

#### `POST` /api/v2/remediation/workflows/{workflow_id}/execute
Execute workflow

### Dashboard

#### `GET` /api/v2/remediation/dashboard/summary
Get remediation dashboard

---

## Phase B4: Compliance

**Total Endpoints:** 21
**Purpose:** Compliance framework management, assessments, controls, evidence collection

### Compliance Assessments

#### `GET, POST` /api/v2/compliance/assessments
List or create assessments

#### `GET` /api/v2/compliance/assessments/{assessment_id}
Get assessment details

#### `GET` /api/v2/compliance/assessments/by-framework/{framework}
List assessments by framework

#### `POST` /api/v2/compliance/assessments/{assessment_id}/complete
Complete assessment

### Control Management

#### `GET, POST` /api/v2/compliance/controls
Manage compliance controls

#### `GET` /api/v2/compliance/controls/{control_id}
Get control details

#### `GET` /api/v2/compliance/controls/by-framework/{framework}
List controls by framework

#### `GET` /api/v2/compliance/controls/search
Search controls

### Evidence Management

#### `GET, POST` /api/v2/compliance/evidence
Manage compliance evidence

#### `GET` /api/v2/compliance/evidence/{evidence_id}
Get evidence details

#### `GET` /api/v2/compliance/evidence/{control_id}/artifacts
Get evidence artifacts

#### `POST` /api/v2/compliance/evidence/{evidence_id}/verify
Verify evidence

### Gap Analysis

#### `GET` /api/v2/compliance/gaps
Identify compliance gaps

#### `GET` /api/v2/compliance/gaps/{framework}
Get gaps for framework

#### `GET` /api/v2/compliance/gaps/critical
List critical gaps

### Compliance Mapping

#### `POST` /api/v2/compliance/mappings
Create compliance mapping

#### `GET` /api/v2/compliance/mappings/{framework1}/{framework2}
Map between frameworks

### Dashboard

#### `GET` /api/v2/compliance/dashboard/summary
Get compliance dashboard

#### `GET` /api/v2/compliance/dashboard/posture
Get compliance posture

---

## Phase B5: Alerts

**Total Endpoints:** 19
**Purpose:** Alert management, notification routing, rule engines, escalation policies

### Alert Management

#### `GET, POST` /api/v2/alerts
List or create alerts

#### `GET` /api/v2/alerts/{alert_id}
Get alert details

#### `GET` /api/v2/alerts/by-severity/{severity}
List alerts by severity

#### `GET` /api/v2/alerts/by-status/{status}
List alerts by status

#### `GET` /api/v2/alerts/search
Search alerts

#### `POST` /api/v2/alerts/{alert_id}/acknowledge
Acknowledge alert

#### `POST` /api/v2/alerts/{alert_id}/assign
Assign alert to user

#### `POST` /api/v2/alerts/{alert_id}/resolve
Resolve alert

### Alert Rules

#### `GET, POST` /api/v2/alerts/rules
Manage alert rules

#### `GET` /api/v2/alerts/rules/{rule_id}
Get rule details

#### `POST` /api/v2/alerts/rules/{rule_id}/enable
Enable alert rule

#### `POST` /api/v2/alerts/rules/{rule_id}/disable
Disable alert rule

### Alert Correlations

#### `GET, POST` /api/v2/alerts/correlations
Manage alert correlations

#### `GET` /api/v2/alerts/correlations/{correlation_id}
Get correlation details

### Notifications

#### `GET, POST` /api/v2/alerts/notifications
Manage notifications

#### `GET` /api/v2/alerts/notifications/{notification_id}
Get notification details

### Escalation Policies

#### `GET, POST` /api/v2/alerts/escalations
Manage escalation policies

#### `GET` /api/v2/alerts/escalations/{policy_id}
Get policy details

### Dashboard

#### `GET` /api/v2/alerts/dashboard/summary
Get alerts dashboard

---

## Phase B5: Demographics

**Total Endpoints:** 24
**Purpose:** Human factors analysis, behavior patterns, access patterns, user profiling

### Demographics Analysis

#### `GET, POST` /api/v2/demographics/profiles
Manage demographic profiles

#### `GET` /api/v2/demographics/profiles/{profile_id}
Get profile details

#### `GET` /api/v2/demographics/profiles/search
Search profiles

#### `GET` /api/v2/demographics/profiles/{profile_id}/behavior
Get behavior patterns

### Geographic Analysis

#### `GET` /api/v2/demographics/geographic/distribution
Get geographic distribution

#### `GET` /api/v2/demographics/geographic/risk-zones
Identify high-risk zones

#### `GET` /api/v2/demographics/geographic/access-patterns
Analyze geographic access patterns

### Temporal Patterns

#### `GET` /api/v2/demographics/temporal/activity
Get activity patterns

#### `GET` /api/v2/demographics/temporal/anomalies
Detect temporal anomalies

#### `GET` /api/v2/demographics/temporal/peak-hours
Identify peak activity hours

### Role-Based Analysis

#### `GET` /api/v2/demographics/roles/analysis
Analyze role behavior

#### `GET` /api/v2/demographics/roles/{role_id}/typical-behavior
Get typical role behavior

#### `GET` /api/v2/demographics/roles/{role_id}/deviations
Detect role deviations

### Access Pattern Analysis

#### `GET` /api/v2/demographics/access-patterns/analysis
Analyze access patterns

#### `GET` /api/v2/demographics/access-patterns/unusual
Detect unusual access

#### `GET` /api/v2/demographics/access-patterns/{user_id}/baseline
Get user baseline

### Cohort Analysis

#### `GET, POST` /api/v2/demographics/cohorts
Manage cohorts

#### `GET` /api/v2/demographics/cohorts/{cohort_id}
Get cohort details

#### `GET` /api/v2/demographics/cohorts/{cohort_id}/behavior
Analyze cohort behavior

### Dashboard

#### `GET` /api/v2/demographics/dashboard/summary
Get demographics dashboard

#### `GET` /api/v2/demographics/dashboard/insights
Get demographic insights

---

## Phase B5: Economic Analysis

**Total Endpoints:** 27
**Purpose:** Financial impact analysis, cost-benefit, ROI calculations, budget tracking

### Cost Analysis

#### `GET, POST` /api/v2/economic/costs
Manage cost records

#### `GET` /api/v2/economic/costs/{cost_id}
Get cost details

#### `GET` /api/v2/economic/costs/by-category/{category}
List costs by category

#### `GET` /api/v2/economic/costs/total
Get total costs

### Impact Assessment

#### `POST` /api/v2/economic/impact/assess
Assess economic impact

#### `GET` /api/v2/economic/impact/{entity_type}/{entity_id}
Get impact for entity

#### `GET` /api/v2/economic/impact/potential-loss
Calculate potential loss

#### `GET` /api/v2/economic/impact/breach-cost
Estimate breach cost

### ROI Calculations

#### `POST` /api/v2/economic/roi/calculate
Calculate ROI

#### `GET` /api/v2/economic/roi/{investment_id}
Get ROI details

#### `GET` /api/v2/economic/roi/security-investments
Analyze security ROI

### Budget Management

#### `GET, POST` /api/v2/economic/budgets
Manage budgets

#### `GET` /api/v2/economic/budgets/{budget_id}
Get budget details

#### `GET` /api/v2/economic/budgets/{budget_id}/utilization
Get budget utilization

#### `GET` /api/v2/economic/budgets/forecast
Forecast budget needs

### Value Analysis

#### `GET` /api/v2/economic/value/security-controls
Calculate control value

#### `GET` /api/v2/economic/value/risk-reduction
Calculate risk reduction value

#### `GET` /api/v2/economic/value/efficiency-gains
Calculate efficiency gains

### Insurance & Transfer

#### `GET, POST` /api/v2/economic/insurance
Manage cyber insurance

#### `GET` /api/v2/economic/insurance/{policy_id}
Get policy details

#### `GET` /api/v2/economic/insurance/recommendations
Get insurance recommendations

### Cost-Benefit Analysis

#### `POST` /api/v2/economic/cost-benefit/analyze
Perform cost-benefit analysis

#### `GET` /api/v2/economic/cost-benefit/{analysis_id}
Get analysis results

### Dashboard

#### `GET` /api/v2/economic/dashboard/summary
Get economic dashboard

#### `GET` /api/v2/economic/dashboard/trends
Get economic trends

---

## Psychometric Analysis

**Total Endpoints:** 8
**Purpose:** Behavioral assessment, psychological profiling, stress indicators

### Psychometric Profiles

#### `GET, POST` /api/v2/psychometric/profiles
Manage psychometric profiles

#### `GET` /api/v2/psychometric/profiles/{profile_id}
Get profile details

### Behavioral Assessment

#### `POST` /api/v2/psychometric/assessments
Create behavioral assessment

#### `GET` /api/v2/psychometric/assessments/{assessment_id}
Get assessment results

### Risk Indicators

#### `GET` /api/v2/psychometric/risk-indicators/{user_id}
Get psychological risk indicators

### Stress Analysis

#### `GET` /api/v2/psychometric/stress-analysis/{user_id}
Analyze stress levels

### Behavioral Anomalies

#### `GET` /api/v2/psychometric/anomalies/{user_id}
Detect behavioral anomalies

### Dashboard

#### `GET` /api/v2/psychometric/dashboard/summary
Get psychometric dashboard

---

## Search Services

**Total Endpoints:** 3
**Purpose:** Semantic search, hybrid search, NER processing

### Named Entity Recognition

#### `POST` /ner
Extract named entities from text

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"text": "Microsoft Azure vulnerability CVE-2023-1234"}' \
     http://localhost:8000/ner
```

### Semantic Search

#### `POST` /search/semantic
Perform semantic search

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"query": "critical vulnerabilities", "limit": 10}' \
     http://localhost:8000/search/semantic
```

### Hybrid Search

#### `POST` /search/hybrid
Perform hybrid (semantic + keyword) search

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"query": "ransomware attacks", "limit": 20}' \
     http://localhost:8000/search/hybrid
```

---

## System Health

**Total Endpoints:** 1
**Purpose:** System health monitoring

### Health Check

#### `GET` /health
Get system health status

**Example:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "3.3.0",
  "timestamp": "2025-12-13T10:30:00Z",
  "services": {
    "neo4j": "connected",
    "qdrant": "connected",
    "api": "operational"
  }
}
```

---

## Common Query Parameters

### Pagination
```
?skip=0&limit=100
```

### Filtering
```
?severity=critical
?status=active
?start_date=2025-01-01&end_date=2025-12-31
```

### Sorting
```
?sort_by=created_at&sort_order=desc
```

### Search
```
?q=search_term
?search=keyword
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "X-Customer-ID header required"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "error": "Error message"
}
```

---

## Rate Limiting

- **Default:** 1000 requests per hour per customer
- **Burst:** Up to 100 requests per minute
- **Headers:**
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

---

## WebSocket Support

Real-time updates available for:
- Alert notifications
- Risk score changes
- Compliance status updates

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

---

## OpenAPI Specification

Complete OpenAPI 3.0 specification available at:
```
http://localhost:8000/openapi.json
```

Interactive API documentation:
```
http://localhost:8000/docs
```

---

## Support

For issues or questions:
- GitHub: [aeon-cybersecurity](https://github.com/your-org/aeon)
- Email: support@aeon-cyber.com
- Documentation: http://docs.aeon-cyber.com

---

**Generated:** 2025-12-13
**API Version:** 3.3.0
**Documentation Version:** 1.0.0
