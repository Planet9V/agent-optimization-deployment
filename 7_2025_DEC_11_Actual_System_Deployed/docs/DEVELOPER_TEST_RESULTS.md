# DEVELOPER API TEST RESULTS - SYSTEMATIC EXECUTION

**Date**: 2025-12-12
**Tester**: Backend Developer Agent
**Status**: TESTING IN PROGRESS

---

## TEST RESULTS

| # | API Name | Status | HTTP Code | Time | Endpoint |
|---|----------|--------|-----------|------|----------|
| 1 | Next.js Health Check | ✅ PASS | 200 | 0.062066s | GET /api/health |
| 2 | Neo4j Statistics | ⚠️ CLIENT ERROR | 404 | 0.086250s | GET /api/neo4j/stats |
| 3 | MySQL Statistics | ⚠️ CLIENT ERROR | 404 | 0.069434s | GET /api/mysql/stats |
| 4 | Qdrant Collections | ⚠️ CLIENT ERROR | 404 | 0.074700s | GET /api/qdrant/collections |
| 5 | MinIO Buckets | ⚠️ CLIENT ERROR | 404 | 0.158058s | GET /api/minio/buckets |
| 6 | Remediation Dashboard Summary | ❌ SERVER ERROR | 500 | 0.001533s | GET /api/v2/remediation/dashboard/summary |
| 7 | Remediation Workload | ❌ SERVER ERROR | 500 | 0.001491s | GET /api/v2/remediation/dashboard/workload |
| 8 | List Remediation Tasks | ⚠️ CLIENT ERROR | 405 | 0.001903s | GET /api/v2/remediation/tasks |
| 9 | Open Remediation Tasks | ❌ SERVER ERROR | 500 | 0.002101s | GET /api/v2/remediation/tasks/open |
| 10 | Overdue Remediation Tasks | ❌ SERVER ERROR | 500 | 0.001590s | GET /api/v2/remediation/tasks/overdue |
| 11 | List Remediation Plans | ❌ SERVER ERROR | 500 | 0.001891s | GET /api/v2/remediation/plans |
| 12 | Active Remediation Plans | ❌ SERVER ERROR | 500 | 0.001564s | GET /api/v2/remediation/plans/active |
| 13 | Remediation Metrics Summary | ❌ SERVER ERROR | 500 | 0.001986s | GET /api/v2/remediation/metrics/summary |
| 14 | Mean Time To Remediate | ❌ SERVER ERROR | 500 | 0.006193s | GET /api/v2/remediation/metrics/mttr |
| 15 | SLA Compliance Metrics | ❌ SERVER ERROR | 500 | 0.002087s | GET /api/v2/remediation/metrics/sla-compliance |
| 16 | Risk Dashboard Summary | ❌ SERVER ERROR | 500 | 0.124561s | GET /api/v2/risk/dashboard/summary |
| 17 | Risk Scores List | ⚠️ CLIENT ERROR | 405 | 0.007056s | GET /api/v2/risk/scores |
| 18 | Risk Alerts List | ⚠️ CLIENT ERROR | 404 | 0.001841s | GET /api/v2/risk/alerts |
| 19 | Active Risk Alerts | ⚠️ CLIENT ERROR | 404 | 0.001527s | GET /api/v2/risk/alerts/active |
| 20 | Risk Trends by Severity | ⚠️ CLIENT ERROR | 404 | 0.001414s | GET /api/v2/risk/trends/by-severity |
| 21 | Risk Aggregation by Vendor | ✅ PASS | 200 | 0.109581s | GET /api/v2/risk/aggregation/by-vendor |
| 22 | Risk Aggregation by Sector | ✅ PASS | 200 | 0.100488s | GET /api/v2/risk/aggregation/by-sector |
| 23 | Risk Aggregation by Asset Type | ✅ PASS | 200 | 0.108909s | GET /api/v2/risk/aggregation/by-asset-type |
| 24 | List SBOMs | ⚠️ CLIENT ERROR | 400 | 0.105420s | GET /api/v2/sbom/sboms |
| 25 | Search SBOM Components | ⚠️ CLIENT ERROR | 404 | 0.001637s | POST /api/v2/sbom/search |
| 26 | Analyze SBOM | ⚠️ CLIENT ERROR | 404 | 0.001747s | POST /api/v2/sbom/analyze |
| 27 | Threat Intel Dashboard | ❌ SERVER ERROR | 500 | 1.193274s | GET /api/v2/threat-intel/dashboard/summary |
| 28 | List Threat Feeds | ❌ SERVER ERROR | 500 | 1.174971s | GET /api/v2/threat-intel/feeds |
| 29 | List Threat Indicators | ⚠️ CLIENT ERROR | 404 | 0.001614s | GET /api/v2/threat-intel/indicators |
| 30 | List Threat Reports | ⚠️ CLIENT ERROR | 404 | 0.001494s | GET /api/v2/threat-intel/reports |
| 31 | List Vendors | ⚠️ CLIENT ERROR | 400 | 0.108852s | GET /api/v2/vendor-equipment/vendors |
| 32 | List Equipment | ⚠️ CLIENT ERROR | 400 | 0.112635s | GET /api/v2/vendor-equipment/equipment |
| 33 | Equipment Dashboard | ⚠️ CLIENT ERROR | 404 | 0.005671s | GET /api/v2/vendor-equipment/dashboard/summary |

---

## SUMMARY

**Total Tests**: 33
**Passed**: 4 (12%)
**Client Errors**: 17
**Server Errors**: 12

**Test Log**: /tmp/api_test_log.txt
**Generated**: 2025-12-12 14:26:56

