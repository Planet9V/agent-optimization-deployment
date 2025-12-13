# Additional API Features Design - 52 New Endpoints
**Generated**: 2025-12-13 14:17 UTC
**Status**: COMPREHENSIVE DESIGN COMPLETE
**Current System**: 62 working APIs → **Target**: 114 APIs

---

## Executive Summary

This design adds **52 advanced API features** to address gaps in the current 62-API system. Features are prioritized for maximum business impact with 18 quick-win endpoints implementable in a single day.

### Focus Areas
1. **Advanced SBOM Analytics** (12 endpoints) - Trend analysis, risk scoring, health metrics
2. **Cross-Domain Correlation** (15 endpoints) - Threat-vuln correlation, asset-risk mapping
3. **Real-Time Alert Aggregation** (8 endpoints) - Alert streaming, deduplication, prioritization
4. **Enhanced Compliance Reporting** (10 endpoints) - Multi-framework mapping, evidence collection
5. **Economic Impact Modeling** (7 endpoints) - Cost calculation, ROI analysis, breach simulation

---

## Priority Breakdown

### P0 - Critical (15 endpoints) - Week 1
**Focus**: Core correlation and analytics features
**Implementation Time**: 12-15 hours

**Key Endpoints**:
- Component Risk Scoring
- Threat-Vulnerability Correlation
- Asset-Risk-Vulnerability Mapping
- Multi-Domain Risk Rollup
- Alert Priority Scoring
- Vulnerability Cost Calculator
- Remediation ROI Calculator

### P1 - High Priority (22 endpoints) - Weeks 2-3
**Focus**: Enhanced features and reporting
**Implementation Time**: 18-22 hours

**Key Endpoints**:
- SBOM Trend Analysis
- Vulnerability Exploit Prediction
- Remediation-Risk Optimization
- Compliance Evidence Collection
- Alert Correlation Graph

### P2 - Nice to Have (15 endpoints) - Week 4
**Focus**: ML/AI features and advanced analytics
**Implementation Time**: 15-18 hours

**Key Endpoints**:
- Component Popularity Metrics
- Alert ML Insights
- Compliance Forecasting
- Breach Impact Simulator
- Cyber Insurance Premium Estimator

---

## Quick Wins - 18 Endpoints (<30 min each)

**Total Implementation**: ~7.5 hours | **Delivery**: Single day sprint

### Immediate Impact Features
1. SBOM Trend Analysis (30 min)
2. License Compliance Dashboard (25 min)
3. SBOM Health Score (30 min)
4. Alert Stream API (30 min)
5. Alert Aggregation Dashboard (20 min)
6. Multi-Domain Risk Rollup (25 min)
7. Compliance Timeline Report (30 min)
8. Cost-Benefit Analysis Dashboard (30 min)
9. SBOM Batch Operations (25 min)
10. Alert Deduplication (25 min)
11. Continuous Compliance Monitoring (25 min)
12. Compliance Benchmark Comparison (30 min)
13. Industry Benchmark Economics (25 min)
14. Component Age Analysis (20 min)
15. SBOM Export/Import (20 min)
16. Alert Correlation Engine (30 min)
17. Compliance-Remediation Tracking (35 min)
18. Compliance Evidence Dashboard (25 min)

---

## Detailed Feature Specifications

## 1. ADVANCED SBOM ANALYTICS (12 Endpoints)

### 1.1 SBOM Trend Analysis ⚡ Quick Win
**Priority**: P0 | **Time**: 30 min | **Complexity**: Low

```http
GET /api/v2/sbom/analytics/trends?period=30d
```

**Response**:
```json
{
  "period": "30d",
  "data_points": [
    {"date": "2025-12-01", "critical": 5, "high": 12, "medium": 23},
    {"date": "2025-12-08", "critical": 3, "high": 15, "medium": 20}
  ],
  "trend_analysis": {
    "critical_change": "-40%",
    "high_change": "+25%",
    "overall_risk_score": 72.5
  }
}
```

**Implementation**: Aggregate existing SBOM vulnerability data by date

---

### 1.2 Component Risk Scoring
**Priority**: P0 | **Time**: 45 min | **Complexity**: Medium

```http
POST /api/v2/sbom/components/risk-score
Content-Type: application/json

{
  "component_id": "pkg:npm/express@4.17.1",
  "factors": ["vulnerabilities", "age", "maintenance", "popularity", "kev_status"]
}
```

**Response**:
```json
{
  "component_id": "pkg:npm/express@4.17.1",
  "risk_score": 68.5,
  "breakdown": {
    "vulnerability_risk": 25.0,
    "age_risk": 15.0,
    "maintenance_risk": 10.5,
    "popularity_bonus": -5.0,
    "kev_penalty": 23.0
  },
  "recommendation": "UPDATE_RECOMMENDED",
  "alternatives": ["express@4.18.2", "fastify@4.10.0"]
}
```

**Dependencies**: SBOM, vulnerability, threat intel data

---

### 1.3 SBOM Health Score ⚡ Quick Win
**Priority**: P0 | **Time**: 30 min | **Complexity**: Low

```http
GET /api/v2/sbom/{sbom_id}/health-score
```

**Response**:
```json
{
  "sbom_id": "prod-v1.0.0",
  "health_score": 72.5,
  "grade": "B",
  "factors": {
    "vulnerability_score": 65.0,
    "license_compliance": 95.0,
    "component_freshness": 55.0,
    "maintenance_status": 80.0,
    "dependency_depth": 70.0
  },
  "recommendations": [
    "Update 15 components with known vulnerabilities",
    "Replace 3 components with better-maintained alternatives"
  ]
}
```

---

### 1.4 Dependency Chain Analysis
**Priority**: P0 | **Time**: 50 min | **Complexity**: Medium

```http
GET /api/v2/sbom/dependencies/chain/{component_id}
```

**Response**:
```json
{
  "component": "pkg:npm/express@4.17.1",
  "dependency_depth": 5,
  "total_dependencies": 48,
  "vulnerable_path": [
    {
      "level": 0,
      "component": "express@4.17.1",
      "vulnerabilities": []
    },
    {
      "level": 2,
      "component": "qs@6.7.0",
      "vulnerabilities": ["CVE-2022-24999"]
    }
  ],
  "remediation_options": [
    "Upgrade express to 4.18.2 (removes vulnerable path)",
    "Direct patch qs to 6.11.0"
  ]
}
```

---

### 1.5 License Compliance Dashboard ⚡ Quick Win
**Priority**: P1 | **Time**: 25 min | **Complexity**: Low

```http
GET /api/v2/sbom/licenses/compliance-summary
```

**Response**:
```json
{
  "total_components": 1250,
  "license_distribution": {
    "MIT": 450,
    "Apache-2.0": 320,
    "GPL-3.0": 15,
    "proprietary": 25,
    "unknown": 10
  },
  "compliance_issues": [
    {
      "component": "libfoo@1.2.3",
      "license": "GPL-3.0",
      "conflict_with": "proprietary-license",
      "severity": "HIGH"
    }
  ],
  "risk_score": 45.2
}
```

---

### 1.6-1.12 Additional SBOM Features
- **SBOM Comparison API** (P1, 45 min)
- **Component Age Analysis** (P2, 20 min) ⚡
- **Vulnerability Exploit Prediction** (P1, 90 min)
- **Component Popularity Metrics** (P2, 40 min)
- **SBOM Batch Operations** (P1, 25 min) ⚡
- **Component Substitution Recommendations** (P1, 50 min)
- **SBOM Export/Import** (P2, 20 min) ⚡

---

## 2. CROSS-DOMAIN CORRELATION (15 Endpoints)

### 2.1 Threat-Vulnerability Correlation
**Priority**: P0 | **Time**: 60 min | **Complexity**: Medium

```http
POST /api/v2/correlation/threat-vulnerability
Content-Type: application/json

{
  "threat_actor_id": "APT28",
  "time_range": "30d"
}
```

**Response**:
```json
{
  "threat_actor": "APT28",
  "matched_vulnerabilities": [
    {
      "cve_id": "CVE-2023-12345",
      "affected_components": ["pkg:npm/axios@0.19.0"],
      "campaign_ids": ["camp_001", "camp_003"],
      "exploitation_evidence": "CONFIRMED",
      "affected_sboms": ["prod-v1", "staging-v2"],
      "risk_score": 95.0
    }
  ],
  "total_at_risk_assets": 45,
  "recommended_actions": [
    "Immediate patching of affected components",
    "Isolate affected systems",
    "Enable enhanced monitoring"
  ]
}
```

**Dependencies**: Threat intel + SBOM data

---

### 2.2 Asset-Risk-Vulnerability Mapping
**Priority**: P0 | **Time**: 55 min | **Complexity**: Medium

```http
GET /api/v2/correlation/asset-risk-map
```

**Response**:
```json
{
  "total_assets": 150,
  "correlation_matrix": [
    {
      "asset_id": "server-prod-01",
      "sbom_id": "prod-v1.0.0",
      "critical_vulns": 3,
      "high_vulns": 8,
      "associated_threats": ["APT28", "Lazarus"],
      "risk_score": 88.5,
      "priority": "IMMEDIATE"
    }
  ],
  "heat_map_data": [...],
  "top_risks": [...]
}
```

---

### 2.3 Multi-Domain Risk Rollup ⚡ Quick Win
**Priority**: P0 | **Time**: 25 min | **Complexity**: Low

```http
GET /api/v2/correlation/risk-rollup
```

**Response**:
```json
{
  "overall_risk_score": 72.5,
  "domain_breakdown": {
    "sbom_risk": 68.0,
    "threat_intel_risk": 75.0,
    "compliance_risk": 45.0,
    "vendor_risk": 82.0,
    "remediation_backlog_risk": 70.0
  },
  "top_risk_factors": [
    "15 critical vulnerabilities unpatched >90 days",
    "Active threat campaigns targeting organization",
    "12 compliance controls failing"
  ],
  "trend": "IMPROVING"
}
```

---

### 2.4 Threat Campaign Impact Assessment
**Priority**: P0 | **Time**: 60 min | **Complexity**: Medium

```http
POST /api/v2/correlation/campaign-impact
Content-Type: application/json

{
  "campaign_id": "camp_001",
  "scope": "all_assets"
}
```

**Response**:
```json
{
  "campaign": "Operation XYZ",
  "campaign_id": "camp_001",
  "ttps": ["T1190", "T1210", "T1059"],
  "vulnerable_assets": 45,
  "vulnerable_components": [
    {
      "component": "pkg:npm/express@4.17.1",
      "cve": "CVE-2023-12345",
      "asset_count": 12,
      "exploitation_likelihood": 0.85
    }
  ],
  "economic_impact": 1250000,
  "recommended_priority": "CRITICAL"
}
```

---

### 2.5 Supply Chain Risk Correlation
**Priority**: P0 | **Time**: 70 min | **Complexity**: High

```http
POST /api/v2/correlation/supply-chain-risk
```

**Response**:
```json
{
  "total_vendors": 25,
  "high_risk_vendors": 3,
  "supply_chain_risks": [
    {
      "vendor": "Vendor XYZ",
      "components_supplied": 45,
      "vulnerabilities": 12,
      "threat_intel_mentions": 5,
      "risk_score": 85.0,
      "mitigation": "DIVERSIFY_SUPPLIERS"
    }
  ]
}
```

---

### 2.6-2.15 Additional Correlation Features
- **Compliance-Vulnerability Gap Analysis** (P1, 50 min)
- **Remediation-Risk Optimization** (P1, 75 min)
- **Vendor-Equipment-Vulnerability Correlation** (P1, 45 min)
- **Alert Correlation Engine** (P0, 30 min) ⚡
- **Temporal Correlation Analysis** (P1, 50 min)
- **Dependency-Threat Propagation** (P1, 80 min)
- **Compliance-Remediation Tracking** (P1, 35 min) ⚡
- **Geo-Threat Correlation** (P2, 45 min)
- **Psychometric-Risk Correlation** (P2, 90 min)
- **Incident-Vulnerability Forensics** (P1, 55 min)

---

## 3. REAL-TIME ALERT AGGREGATION (8 Endpoints)

### 3.1 Alert Stream API ⚡ Quick Win
**Priority**: P0 | **Time**: 30 min | **Complexity**: Low

```http
GET /api/v2/alerts/stream
Accept: text/event-stream
```

**Response**: Server-Sent Events stream
```
event: alert
data: {"alert_id": "alert_001", "severity": "CRITICAL", ...}

event: alert
data: {"alert_id": "alert_002", "severity": "HIGH", ...}
```

**Implementation**: Use FastAPI StreamingResponse with async generator

---

### 3.2 Alert Priority Scoring
**Priority**: P0 | **Time**: 60 min | **Complexity**: Medium

```http
POST /api/v2/alerts/priority-score
Content-Type: application/json

{
  "alert_id": "alert_001"
}
```

**Response**:
```json
{
  "alert_id": "alert_001",
  "original_severity": "HIGH",
  "calculated_priority": 92.5,
  "factors": {
    "vulnerability_severity": 85.0,
    "asset_criticality": 95.0,
    "threat_intel_correlation": 90.0,
    "exploit_availability": 100.0,
    "affected_users": 1000
  },
  "recommended_sla": "1 hour"
}
```

---

### 3.3 Alert Aggregation Dashboard ⚡ Quick Win
**Priority**: P0 | **Time**: 20 min | **Complexity**: Low

```http
GET /api/v2/alerts/dashboard
```

**Response**:
```json
{
  "total_active_alerts": 52,
  "by_severity": {
    "CRITICAL": 5,
    "HIGH": 15,
    "MEDIUM": 22,
    "LOW": 10
  },
  "by_category": {
    "vulnerability": 30,
    "threat": 12,
    "compliance": 10
  },
  "avg_resolution_time": "4.2 hours",
  "alerts_last_24h": 145
}
```

---

### 3.4-3.8 Additional Alert Features
- **Alert Deduplication** (P1, 25 min) ⚡
- **Alert Escalation Rules** (P1, 45 min)
- **Alert Correlation Graph** (P1, 50 min)
- **Alert Playbook Automation** (P2, 90 min)
- **Alert ML Insights** (P2, 85 min)

---

## 4. ENHANCED COMPLIANCE REPORTING (10 Endpoints)

### 4.1 Multi-Framework Mapping
**Priority**: P0 | **Time**: 55 min | **Complexity**: Medium

```http
POST /api/v2/compliance/multi-framework-map
Content-Type: application/json

{
  "source_framework": "NIST_CSF",
  "target_frameworks": ["ISO27001", "PCI-DSS", "SOC2"]
}
```

**Response**:
```json
{
  "mappings": [
    {
      "source_control": "PR.IP-12",
      "mapped_controls": {
        "ISO27001": ["A.12.6.1"],
        "PCI-DSS": ["6.2"],
        "SOC2": ["CC7.1"]
      },
      "unified_status": "PASSING"
    }
  ]
}
```

---

### 4.2 Compliance Gap Prioritization
**Priority**: P0 | **Time**: 50 min | **Complexity**: Medium

```http
GET /api/v2/compliance/gaps/prioritized
```

**Response**:
```json
{
  "total_gaps": 23,
  "prioritized_gaps": [
    {
      "control_id": "PR.IP-12",
      "framework": "NIST_CSF",
      "business_impact_score": 92.5,
      "remediation_effort": "MEDIUM",
      "regulatory_risk": "HIGH",
      "priority": "P0"
    }
  ]
}
```

---

### 4.3 Compliance Timeline Report ⚡ Quick Win
**Priority**: P1 | **Time**: 30 min | **Complexity**: Low

```http
GET /api/v2/compliance/timeline?framework=NIST_CSF&period=90d
```

**Response**:
```json
{
  "framework": "NIST_CSF",
  "timeline": [
    {
      "date": "2025-12-01",
      "compliance_score": 78.5,
      "passing_controls": 85,
      "failing_controls": 23
    },
    {
      "date": "2025-12-13",
      "compliance_score": 85.2,
      "passing_controls": 96,
      "failing_controls": 12
    }
  ]
}
```

---

### 4.4-4.10 Additional Compliance Features
- **Compliance Evidence Collection** (P1, 60 min)
- **Continuous Compliance Monitoring** (P1, 25 min) ⚡
- **Regulatory Change Impact** (P2, 75 min)
- **Compliance Report Generation** (P1, 45 min)
- **Control Effectiveness Scoring** (P1, 50 min)
- **Compliance Forecasting** (P2, 80 min)
- **Compliance Benchmark Comparison** (P1, 30 min) ⚡

---

## 5. ECONOMIC IMPACT MODELING (7 Endpoints)

### 5.1 Vulnerability Cost Calculator
**Priority**: P0 | **Time**: 55 min | **Complexity**: Medium

```http
POST /api/v2/economic/vulnerability-cost
Content-Type: application/json

{
  "vulnerability_id": "CVE-2023-12345",
  "affected_assets": ["server-01", "server-02"],
  "organization_size": "medium",
  "industry": "finance"
}
```

**Response**:
```json
{
  "total_risk_exposure": 1250000,
  "breakdown": {
    "data_breach_risk": 500000,
    "business_disruption": 400000,
    "regulatory_fines": 250000,
    "reputation_damage": 100000
  },
  "probability_of_exploitation": 0.65,
  "expected_loss": 812500
}
```

---

### 5.2 Remediation ROI Calculator
**Priority**: P0 | **Time**: 50 min | **Complexity**: Medium

```http
POST /api/v2/economic/remediation-roi
Content-Type: application/json

{
  "remediation_cost": 50000,
  "vulnerabilities_addressed": ["CVE-2023-12345", "CVE-2023-67890"]
}
```

**Response**:
```json
{
  "investment": 50000,
  "risk_reduction": 1750000,
  "roi": 3400,
  "payback_period": "0.3 years",
  "net_present_value": 1650000,
  "recommendation": "HIGH_PRIORITY_INVESTMENT"
}
```

---

### 5.3 Cost-Benefit Analysis Dashboard ⚡ Quick Win
**Priority**: P0 | **Time**: 30 min | **Complexity**: Low

```http
GET /api/v2/economic/cost-benefit-dashboard
```

**Response**:
```json
{
  "total_security_spend": 1000000,
  "risk_exposure_prevented": 5000000,
  "roi": 400,
  "cost_per_incident_prevented": 50000,
  "incidents_prevented": 20
}
```

---

### 5.4-5.7 Additional Economic Features
- **Breach Impact Simulator** (P1, 70 min)
- **Security Investment Portfolio** (P1, 75 min)
- **Cyber Insurance Premium Estimator** (P2, 60 min)
- **Industry Benchmark Economics** (P1, 25 min) ⚡

---

## Implementation Strategy

### Week 1: Quick Wins + P0 Critical
**Day 1**: Implement 18 quick-win endpoints (7.5 hours)
**Days 2-5**: Implement 15 P0 critical endpoints (12-15 hours)
**Deliverable**: 33 new working APIs

### Week 2-3: P1 High Priority
**Implementation**: 22 P1 endpoints (18-22 hours)
**Deliverable**: 55 total new APIs

### Week 4: P2 Nice to Have
**Implementation**: 15 P2 endpoints (15-18 hours)
**Deliverable**: 70+ total new APIs

---

## Technical Dependencies

### Database Schema Extensions
```sql
-- SBOM Analytics
CREATE TABLE sbom_analytics (
    id SERIAL PRIMARY KEY,
    sbom_id VARCHAR(255),
    date DATE,
    critical_count INT,
    high_count INT,
    medium_count INT,
    low_count INT,
    risk_score DECIMAL(5,2)
);

-- Correlation Cache
CREATE TABLE correlation_cache (
    id SERIAL PRIMARY KEY,
    cache_key VARCHAR(255) UNIQUE,
    cache_value JSONB,
    expires_at TIMESTAMP
);

-- Alert Correlation
CREATE TABLE alert_correlation (
    id SERIAL PRIMARY KEY,
    alert_id_1 VARCHAR(255),
    alert_id_2 VARCHAR(255),
    correlation_type VARCHAR(50),
    correlation_score DECIMAL(3,2)
);

-- Compliance Evidence
CREATE TABLE compliance_evidence (
    id SERIAL PRIMARY KEY,
    control_id VARCHAR(100),
    framework VARCHAR(50),
    evidence_type VARCHAR(50),
    evidence_data JSONB,
    collected_at TIMESTAMP
);

-- Economic Models
CREATE TABLE economic_calculations (
    id SERIAL PRIMARY KEY,
    calculation_type VARCHAR(50),
    input_params JSONB,
    result JSONB,
    calculated_at TIMESTAMP
);
```

### External API Integrations
1. **npm Registry API** - Component popularity metrics
2. **GitHub API** - Component health data
3. **EPSS API** - Exploit prediction scores
4. **Industry Benchmark APIs** - Compliance and security spending data

### Infrastructure Requirements
1. **Redis Cache** - Real-time alert streaming and correlation cache
2. **Celery Workers** - Async analysis and batch processing
3. **PostgreSQL** - Additional tables for analytics
4. **ML Model Serving** (Optional for P2) - TensorFlow Serving or similar

---

## Success Metrics

### API Adoption
- **Target**: 80% of new endpoints used within 2 weeks
- **Measure**: API call counts per endpoint tracked in metrics

### Performance
- **Target**: <500ms response time for 95th percentile
- **Target**: <2s for complex correlation queries
- **Measure**: Prometheus metrics + Grafana dashboards

### Business Impact
- **Target**: 25% reduction in remediation time
- **Target**: 30% improvement in risk prioritization accuracy
- **Target**: 50% faster compliance reporting
- **Measure**: Before/after analysis with stakeholder feedback

---

## Risk Mitigation

### Technical Risks
1. **Performance**: Implement caching aggressively for correlation queries
2. **Data Quality**: Validate existing data completeness before rollout
3. **External APIs**: Build fallbacks for npm/GitHub API rate limits

### Operational Risks
1. **User Adoption**: Provide API documentation and examples upfront
2. **Breaking Changes**: Version all endpoints as /api/v2/
3. **Monitoring**: Set up comprehensive alerting for new endpoints

---

## Next Steps

1. **Review & Approval**: Stakeholder review of priorities and scope
2. **Sprint Planning**: Allocate engineering resources for Week 1
3. **Schema Design**: Finalize database schema extensions
4. **API Documentation**: Create OpenAPI/Swagger specs
5. **Implementation**: Begin with Day 1 quick wins

---

**Design Completed**: 2025-12-13 14:17 UTC
**Design Status**: ✅ READY FOR IMPLEMENTATION
**Total New APIs**: 52 endpoints
**System Target**: 114 total APIs (current 62 + new 52)

**Stored in Memory**: `additional_apis_design` key for agent retrieval
