# API Current State - Definitive Facts
**Date**: 2025-12-13 08:40:00 CST
**Verification**: Direct system query

## System Identity

- **API Title**: NER11 Gold Standard API
- **API Version**: 3.3.0
- **OpenAPI Spec**: 3.1.0
- **Container**: ner11-gold-api
- **Port**: 8000

## Total Endpoints

**230 paths = 263 operations**

*Note: Some paths support multiple HTTP methods (GET, POST, PUT, DELETE), resulting in more operations than paths.*

## Modules (10 total)

| # | Module | Endpoints | Percentage |
|---|--------|-----------|------------|
| 1 | sbom | 33 | 14.3% |
| 2 | economic-impact | 27 | 11.7% |
| 3 | remediation | 26 | 11.3% |
| 4 | threat-intel | 25 | 10.9% |
| 5 | demographics | 24 | 10.4% |
| 6 | risk | 23 | 10.0% |
| 7 | compliance | 21 | 9.1% |
| 8 | vendor-equipment | 19 | 8.3% |
| 9 | alerts | 19 | 8.3% |
| 10 | psychometrics | 8 | 3.5% |
| - | Core/Other | 5 | 2.2% |

## Phase Organization

**Phase B2: SBOM + Vendor Equipment**
- sbom: 33 endpoints
- vendor-equipment: 19 endpoints
- **Total**: 52 endpoints

**Phase B3: Threat Intelligence + Risk + Remediation**
- threat-intel: 25 endpoints
- risk: 23 endpoints
- remediation: 26 endpoints
- **Total**: 74 endpoints

**Phase B4: Compliance + Alerts**
- compliance: 21 endpoints
- alerts: 19 endpoints
- **Total**: 40 endpoints

**Phase B5: Demographics + Economic Impact + Psychometrics**
- demographics: 24 endpoints
- economic-impact: 27 endpoints
- psychometrics: 8 endpoints
- **Total**: 59 endpoints

**Core Services**
- Health, NER, Search: 5 endpoints

## Authentication

**Required Header:**
```
X-Customer-ID: <customer-id>
```

All endpoints require this header for multi-tenant isolation.

## Base URL Patterns

```
http://<host>:8000/api/v2/<module>/<resource>
```

Examples:
- `/api/v2/sbom/dashboard/summary`
- `/api/v2/threat-intel/actors`
- `/api/v2/compliance/frameworks`

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **OpenAPI JSON**: http://localhost:8000/openapi.json
- **Health Check**: http://localhost:8000/health

## Status

✅ All 230 paths operational
✅ All 10 modules active
✅ All phases (B2-B5) registered and functional
✅ Documentation verified accurate

**Last Verification**: 2025-12-13 08:40:00 CST
