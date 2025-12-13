# API Executive Summary - AEON Platform

**Date**: 2025-12-12
**Total APIs**: 181 endpoints
**Documentation**: COMPLETE_API_REFERENCE_ALL_181.md

## API Inventory

### Phase B APIs (v2) - 135 endpoints
Backend FastAPI services requiring `x-customer-id: dev` header

| Domain | Count | Purpose |
|--------|-------|---------|
| **Remediation** | 29 | Task management, SLA tracking, remediation plans |
| **Risk Management** | 24 | Risk scoring, exposure analysis, asset criticality |
| **SBOM** | 32 | Software inventory, dependencies, vulnerability tracking |
| **Threat Intelligence** | 26 | Threat actors, campaigns, IOCs, MITRE ATT&CK |
| **Vendor/Equipment** | 24 | Vendor risk, equipment lifecycle, maintenance |

### NER APIs - 5 endpoints
Natural language processing and semantic search

| Endpoint | Purpose |
|----------|---------|
| GET /health | Health check |
| GET /info | System information |
| POST /ner | Named entity recognition |
| GET /search/hybrid | Combined search |
| GET /search/semantic | Semantic search |

### Next.js APIs - 41 endpoints
Frontend API routes for UI integration

| Category | Count | Examples |
|----------|-------|----------|
| Dashboard & Analytics | 3 | Stats, trends, risk distribution |
| Threat Intelligence | 5 | Actors, campaigns, IOCs |
| Vulnerability Management | 4 | CVE data, stats, trending |
| SBOM & Assets | 7 | Component inventory, dependencies |
| Risk Management | 4 | Scores, matrix, exposure, trends |
| Remediation | 6 | Tasks, plans, SLA metrics |
| Vendor/Equipment | 6 | Vendor list, equipment, EOL |
| Search & Export | 5 | Search, reports, exports |
| System | 1 | Health check |

## Quick Start

### Testing Phase B APIs
```bash
# Health check
curl http://localhost:8000/health

# Get dashboard summary
curl -H "x-customer-id: dev" \
  http://localhost:8000/api/v2/remediation/dashboard/summary

# Search threat actors
curl -H "x-customer-id: dev" \
  "http://localhost:8000/api/v2/threat-intel/actors/search?q=APT"

# Get critical vulnerabilities
curl -H "x-customer-id: dev" \
  http://localhost:8000/api/v2/sbom/vulnerabilities/critical
```

### Testing Next.js APIs
```bash
# Dashboard stats
curl http://localhost:3000/api/dashboard/stats

# Search
curl "http://localhost:3000/api/search?q=APT1"

# Get vulnerabilities
curl http://localhost:3000/api/vulnerabilities?severity=critical
```

## Common Patterns

### Pagination
```bash
?page=1&limit=20&offset=0
```

### Filtering
```bash
?status=open&severity=critical&priority=high
```

### Sorting
```bash
?sort=created_at&order=desc
```

## Authentication

| API Type | Method |
|----------|--------|
| Phase B (v2) | Header: `x-customer-id: dev` |
| NER | No authentication |
| Next.js | Session-based (check implementation) |

## Key Endpoints by Use Case

### Security Operations Dashboard
- GET /api/v2/remediation/dashboard/summary
- GET /api/v2/risk/dashboard/summary
- GET /api/v2/sbom/dashboard/summary
- GET /api/v2/threat-intel/dashboard/summary

### Vulnerability Management
- GET /api/v2/sbom/vulnerabilities/critical
- GET /api/v2/sbom/components/vulnerable
- GET /api/v2/remediation/tasks/overdue
- GET /api/v2/risk/scores/high-risk

### Threat Intelligence
- GET /api/v2/threat-intel/actors/search
- GET /api/v2/threat-intel/iocs/active
- GET /api/v2/threat-intel/mitre/coverage
- GET /api/v2/threat-intel/campaigns/active

### Risk Analysis
- GET /api/v2/risk/scores/search
- GET /api/v2/risk/exposure/attack-surface
- GET /api/v2/risk/aggregation/by-sector
- GET /api/v2/risk/dashboard/risk-matrix

### Asset Management
- GET /api/v2/sbom/components/search
- GET /api/v2/risk/assets/mission-critical
- GET /api/v2/vendor-equipment/equipment/eol
- GET /api/v2/vendor-equipment/vendors/high-risk

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 404 | Resource not found |
| 422 | Validation error (missing required fields/headers) |
| 500 | Internal server error |

## Current Status

**Phase B APIs**: Deployed but returning 500 errors (database/service issues)
**NER APIs**: Operational
**Next.js APIs**: Implementation status varies

## Next Steps

1. **Debug Phase B 500 errors** - Check database connections and service logs
2. **Test with proper data** - Load test data into PostgreSQL/Neo4j
3. **Verify authentication** - Ensure customer_id validation works
4. **Integration testing** - Test complete workflows across all API layers
5. **Performance testing** - Load testing for production readiness

## Documentation Location

**Full Reference**: `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/COMPLETE_API_REFERENCE_ALL_181.md`

- 6,158 lines
- 127 KB
- Complete schemas for all 181 endpoints
- Request/response examples
- Use case descriptions
- curl command examples

---

**For Developers**: Start with the Quick Start section, then reference the complete documentation for detailed schemas and parameters.

**For Frontend Teams**: Focus on Next.js API routes (section 3) for UI integration patterns.

**For Backend Teams**: Phase B APIs (section 1) provide the core business logic and data access.

**For DevOps**: Check health endpoints and authentication requirements before deployment.
