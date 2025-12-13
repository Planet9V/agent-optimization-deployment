# API Quick Reference - 52 New Endpoints
**Priority Legend**: P0=Critical | P1=High | P2=Nice-to-Have
**⚡ = Quick Win** (<30 min implementation)

---

## SBOM Analytics (12 endpoints)

| # | Endpoint | Priority | Time | Method |
|---|----------|----------|------|--------|
| 1 | `/api/v2/sbom/analytics/trends` ⚡ | P0 | 30m | GET |
| 2 | `/api/v2/sbom/components/risk-score` | P0 | 45m | POST |
| 3 | `/api/v2/sbom/licenses/compliance-summary` ⚡ | P1 | 25m | GET |
| 4 | `/api/v2/sbom/dependencies/chain/{component_id}` | P0 | 50m | GET |
| 5 | `/api/v2/sbom/compare` | P1 | 45m | POST |
| 6 | `/api/v2/sbom/components/age-analysis` ⚡ | P2 | 20m | GET |
| 7 | `/api/v2/sbom/{sbom_id}/health-score` ⚡ | P0 | 30m | GET |
| 8 | `/api/v2/sbom/vulnerabilities/exploit-prediction` | P1 | 90m | POST |
| 9 | `/api/v2/sbom/components/{component_id}/popularity` | P2 | 40m | GET |
| 10 | `/api/v2/sbom/batch/analyze` ⚡ | P1 | 25m | POST |
| 11 | `/api/v2/sbom/components/{component_id}/alternatives` | P1 | 50m | GET |
| 12 | `/api/v2/sbom/{sbom_id}/export/{format}` ⚡ | P2 | 20m | GET |

---

## Cross-Domain Correlation (15 endpoints)

| # | Endpoint | Priority | Time | Method |
|---|----------|----------|------|--------|
| 13 | `/api/v2/correlation/threat-vulnerability` | P0 | 60m | POST |
| 14 | `/api/v2/correlation/asset-risk-map` | P0 | 55m | GET |
| 15 | `/api/v2/correlation/compliance-gaps` | P1 | 50m | POST |
| 16 | `/api/v2/correlation/campaign-impact` | P0 | 60m | POST |
| 17 | `/api/v2/correlation/remediation-optimization` | P1 | 75m | POST |
| 18 | `/api/v2/correlation/vendor-vulnerabilities` | P1 | 45m | GET |
| 19 | `/api/v2/correlation/psychometric-risk` | P2 | 90m | POST |
| 20 | `/api/v2/correlation/alerts/correlate` ⚡ | P0 | 30m | POST |
| 21 | `/api/v2/correlation/temporal/{entity_type}/{entity_id}` | P1 | 50m | GET |
| 22 | `/api/v2/correlation/threat-propagation` | P1 | 80m | POST |
| 23 | `/api/v2/correlation/compliance-remediation` ⚡ | P1 | 35m | GET |
| 24 | `/api/v2/correlation/geo-threats` | P2 | 45m | GET |
| 25 | `/api/v2/correlation/supply-chain-risk` | P0 | 70m | POST |
| 26 | `/api/v2/correlation/incident-forensics` | P1 | 55m | POST |
| 27 | `/api/v2/correlation/risk-rollup` ⚡ | P0 | 25m | GET |

---

## Alert Aggregation (8 endpoints)

| # | Endpoint | Priority | Time | Method |
|---|----------|----------|------|--------|
| 28 | `/api/v2/alerts/stream` ⚡ | P0 | 30m | GET (SSE) |
| 29 | `/api/v2/alerts/priority-score` | P0 | 60m | POST |
| 30 | `/api/v2/alerts/deduplicate` ⚡ | P1 | 25m | POST |
| 31 | `/api/v2/alerts/escalation-rules` | P1 | 45m | POST |
| 32 | `/api/v2/alerts/dashboard` ⚡ | P0 | 20m | GET |
| 33 | `/api/v2/alerts/{alert_id}/correlation-graph` | P1 | 50m | GET |
| 34 | `/api/v2/alerts/{alert_id}/execute-playbook` | P2 | 90m | POST |
| 35 | `/api/v2/alerts/ml-insights` | P2 | 85m | GET |

---

## Compliance Reporting (10 endpoints)

| # | Endpoint | Priority | Time | Method |
|---|----------|----------|------|--------|
| 36 | `/api/v2/compliance/timeline` ⚡ | P1 | 30m | GET |
| 37 | `/api/v2/compliance/multi-framework-map` | P0 | 55m | POST |
| 38 | `/api/v2/compliance/gaps/prioritized` | P0 | 50m | GET |
| 39 | `/api/v2/compliance/evidence/collect` | P1 | 60m | POST |
| 40 | `/api/v2/compliance/continuous-monitoring` ⚡ | P1 | 25m | GET |
| 41 | `/api/v2/compliance/regulatory-change-impact` | P2 | 75m | POST |
| 42 | `/api/v2/compliance/generate-report` | P1 | 45m | POST |
| 43 | `/api/v2/compliance/control-effectiveness` | P1 | 50m | GET |
| 44 | `/api/v2/compliance/forecast` | P2 | 80m | GET |
| 45 | `/api/v2/compliance/benchmark` ⚡ | P1 | 30m | GET |

---

## Economic Impact (7 endpoints)

| # | Endpoint | Priority | Time | Method |
|---|----------|----------|------|--------|
| 46 | `/api/v2/economic/vulnerability-cost` | P0 | 55m | POST |
| 47 | `/api/v2/economic/remediation-roi` | P0 | 50m | POST |
| 48 | `/api/v2/economic/breach-simulator` | P1 | 70m | POST |
| 49 | `/api/v2/economic/investment-portfolio` | P1 | 75m | GET |
| 50 | `/api/v2/economic/insurance-premium` | P2 | 60m | POST |
| 51 | `/api/v2/economic/cost-benefit-dashboard` ⚡ | P0 | 30m | GET |
| 52 | `/api/v2/economic/industry-benchmark` ⚡ | P1 | 25m | GET |

---

## Implementation Summary

### Day 1 Quick Wins (18 endpoints - 7.5 hours)
**SBOM**: #1, #3, #6, #7, #10, #12
**Correlation**: #20, #23, #27
**Alerts**: #28, #30, #32
**Compliance**: #36, #40, #45, #Evidence Dashboard
**Economic**: #51, #52

### Week 1 P0 Critical (15 endpoints - 12-15 hours)
**SBOM**: #2, #4, #7
**Correlation**: #13, #14, #16, #25, #27
**Alerts**: #28, #29, #32
**Compliance**: #37, #38
**Economic**: #46, #47, #51

### Weeks 2-3 P1 High Priority (22 endpoints - 18-22 hours)
**SBOM**: #1, #3, #5, #8, #10, #11
**Correlation**: #15, #17, #18, #21, #22, #23, #26
**Alerts**: #30, #31, #33
**Compliance**: #36, #39, #40, #42, #43, #45
**Economic**: #52

### Week 4 P2 Nice-to-Have (15 endpoints - 15-18 hours)
**SBOM**: #6, #9, #12
**Correlation**: #19, #24
**Alerts**: #34, #35
**Compliance**: #41, #44
**Economic**: #48, #49, #50

---

## Complexity Distribution

### Low Complexity (18 endpoints - 20-35 min)
⚡ All quick wins plus: #Evidence Dashboard

### Medium Complexity (22 endpoints - 40-60 min)
#2, #4, #5, #8, #11, #13, #14, #15, #16, #18, #21, #22, #26, #31, #33, #37, #38, #39, #42, #43, #46, #47

### High Complexity (12 endpoints - 70-90 min)
#17, #19, #25, #29, #34, #35, #41, #44, #48, #49, #50, #Custom Rules

---

## Authentication Pattern
All endpoints require:
```http
X-Customer-ID: <customer_uuid>
```

## Response Format
All endpoints return:
```json
{
  "success": true,
  "data": {...},
  "metadata": {
    "timestamp": "2025-12-13T14:17:00Z",
    "customer_id": "cust_123"
  }
}
```

## Error Format
All endpoints return errors as:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {...}
  }
}
```

---

## Rate Limits
- **Standard**: 100 requests/minute per customer
- **Quick Wins**: 200 requests/minute (cached)
- **Heavy Compute** (ML): 10 requests/minute

## Performance Targets
- **P0/P1 Endpoints**: <500ms @ 95th percentile
- **P2 Endpoints**: <2s @ 95th percentile
- **Streaming**: <100ms first byte

---

**Total**: 52 new APIs
**Quick Wins**: 18 endpoints (<30 min each)
**Current System**: 62 APIs
**Target System**: 114 APIs ✅
