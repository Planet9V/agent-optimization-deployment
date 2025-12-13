/home/jim/.local/lib/python3.12/site-packages/requests/__init__.py:102: RequestsDependencyWarning: urllib3 (1.26.20) or chardet (5.2.0)/charset_normalizer (2.0.12) doesn't match a supported version!
  warnings.warn("urllib3 ({}) or chardet ({})/charset_normalizer ({}) doesn't match a supported "
# COMPLETE API AUDIT - ALL SERVICES

**Audit Date**: 2025-12-12
**Audit Time**: 19:34:48
**Auditor**: Automated Testing System
**Method**: Fresh testing - no previous results used

## AUDIT SCOPE

- ner11-gold-api (8000): 140 APIs
- aeon-saas-dev (3000): 41 APIs

**TOTAL APIs TO AUDIT**: 181

## COMPLETE AUDIT RESULTS

| # | Service | Port | Method | Endpoint | Description | Status | HTTP Code | Time (s) | Working? | Why Not Working | How To Access |
|---|---------|------|--------|----------|-------------|--------|-----------|----------|----------|-----------------|---------------|
| 1 | ner11-gold-api | 8000 | POST | `/api/v2/sbom/sboms` | Create Sbom | ⚠️ VALIDATION | 422 | 0.12 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/sbom/sboms -H 'x-customer-id: dev' -d ` |
| 2 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/sboms` | List Sboms | ✅ PASS | 200 | 0.11 | YES | - | `curl -X GET http://localhost:8000/api/v2/sbom/sboms -H 'x-customer-id: dev'` |
| 3 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/sboms/{sbom_id}` | Get Sbom | ❌ NOT_FOUND | 404 | 0.13 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/sbom/sboms/{sbom_id}` |
| 4 | ner11-gold-api | 8000 | DELETE | `/api/v2/sbom/sboms/{sbom_id}` | Delete Sbom | ⚠️ FORBIDDEN | 403 | 0.11 | NO | Requires WRITE access level | `curl -X DELETE http://localhost:8000/api/v2/sbom/sboms/{sbom_id} -H 'x-access-le` |
| 5 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/sboms/{sbom_id}/risk-summary` | Get Sbom Risk Summary | ❌ ERROR | 500 | 0.11 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/risk-summary` |
| 6 | ner11-gold-api | 8000 | POST | `/api/v2/sbom/components` | Create Component | ⚠️ VALIDATION | 422 | 0.12 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/sbom/components -H 'x-customer-id: dev` |
| 7 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/components/{component_id}` | Get Component | ❌ NOT_FOUND | 404 | 0.12 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/sbom/components/{component_id}` |
| 8 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/components/search` | Search Components | ❌ NOT_FOUND | 404 | 0.12 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/sbom/components/search` |
| 9 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/components/vulnerable` | Get Vulnerable Components | ❌ NOT_FOUND | 404 | 0.10 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/sbom/components/vulnerable` |
| 10 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/components/high-risk` | Get High Risk Components | ❌ NOT_FOUND | 404 | 0.10 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/sbom/components/high-risk` |
| 11 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/sboms/{sbom_id}/components` | Get Components By Sbom | ❌ ERROR | 500 | 0.11 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/components` |
| 12 | ner11-gold-api | 8000 | POST | `/api/v2/sbom/dependencies` | Create Dependency | ⚠️ VALIDATION | 422 | 0.14 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/sbom/dependencies -H 'x-customer-id: d` |
| 13 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/components/{component_id}/dependencies` | Get Dependency Tree | ✅ PASS | 200 | 0.12 | YES | - | `curl -X GET http://localhost:8000/api/v2/sbom/components/{component_id}/dependen` |
| 14 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/components/{component_id}/dependents` | Get Dependents | ❌ ERROR | 500 | 0.11 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/sbom/components/{component_id}/dependen` |
| 15 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/components/{component_id}/impact` | Get Impact Analysis | ✅ PASS | 200 | 0.38 | YES | - | `curl -X GET http://localhost:8000/api/v2/sbom/components/{component_id}/impact -` |
| 16 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/sboms/{sbom_id}/cycles` | Detect Cycles | ✅ PASS | 200 | 0.11 | YES | - | `curl -X GET http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/cycles -H 'x-custo` |
| 17 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/dependencies/path` | Find Dependency Path | ⚠️ VALIDATION | 422 | 0.11 | PARTIAL | Needs correct parameters/body | `curl -X GET http://localhost:8000/api/v2/sbom/dependencies/path -H 'x-customer-i` |
| 18 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/sboms/{sbom_id}/graph-stats` | Get Graph Stats | ✅ PASS | 200 | 0.11 | YES | - | `curl -X GET http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/graph-stats -H 'x-` |
| 19 | ner11-gold-api | 8000 | POST | `/api/v2/sbom/vulnerabilities` | Create Vulnerability | ⚠️ VALIDATION | 422 | 0.10 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/sbom/vulnerabilities -H 'x-customer-id` |
| 20 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/vulnerabilities/{vulnerability_id}` | Get Vulnerability | ❌ NOT_FOUND | 404 | 0.10 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/sbom/vulnerabilities/{vulnerability_id}` |
| 21 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/vulnerabilities/search` | Search Vulnerabilities | ❌ NOT_FOUND | 404 | 0.10 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/sbom/vulnerabilities/search` |
| 22 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/vulnerabilities/critical` | Get Critical Vulnerabilities | ❌ NOT_FOUND | 404 | 0.10 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/sbom/vulnerabilities/critical` |
| 23 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/vulnerabilities/kev` | Get Kev Vulnerabilities | ❌ NOT_FOUND | 404 | 0.10 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/sbom/vulnerabilities/kev` |
| 24 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/vulnerabilities/epss-prioritized` | Get Epss Prioritized Vulns | ❌ NOT_FOUND | 404 | 0.10 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/sbom/vulnerabilities/epss-prioritized` |
| 25 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/vulnerabilities/by-apt` | Get Apt Vulnerability Report | ❌ NOT_FOUND | 404 | 0.10 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/sbom/vulnerabilities/by-apt` |
| 26 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/components/{component_id}/vulnerabilities` | Get Vulnerabilities By Component | ❌ ERROR | 500 | 0.10 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/sbom/components/{component_id}/vulnerab` |
| 27 | ner11-gold-api | 8000 | POST | `/api/v2/sbom/vulnerabilities/{vulnerability_id}/acknowledge` | Acknowledge Vulnerability | ⚠️ VALIDATION | 422 | 0.10 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/sbom/vulnerabilities/{vulnerability_id` |
| 28 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/sboms/{sbom_id}/remediation` | Get Remediation Report | ✅ PASS | 200 | 0.13 | YES | - | `curl -X GET http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/remediation -H 'x-` |
| 29 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/sboms/{sbom_id}/license-compliance` | Get License Compliance | ❌ ERROR | 500 | 0.10 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/license-compliance` |
| 30 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/dashboard/summary` | Get Dashboard Summary | ✅ PASS | 200 | 0.12 | YES | - | `curl -X GET http://localhost:8000/api/v2/sbom/dashboard/summary -H 'x-customer-i` |
| 31 | ner11-gold-api | 8000 | GET | `/api/v2/sbom/sboms/{sbom_id}/vulnerable-paths` | Get Vulnerable Paths | ✅ PASS | 200 | 0.12 | YES | - | `curl -X GET http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/vulnerable-paths -` |
| 32 | ner11-gold-api | 8000 | POST | `/api/v2/sbom/sboms/{sbom_id}/correlate-equipment` | Correlate With Equipment | ⚠️ VALIDATION | 422 | 0.12 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/correlate-equipme` |
| 33 | ner11-gold-api | 8000 | POST | `/api/v2/vendor-equipment/vendors` | Create Vendor | ⚠️ VALIDATION | 422 | 0.11 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/vendor-equipment/vendors -H 'x-custome` |
| 34 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/vendors` | Search Vendors | ✅ PASS | 200 | 0.11 | YES | - | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/vendors -H 'x-customer` |
| 35 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/vendors/{vendor_id}` | Get Vendor | ❌ NOT_FOUND | 404 | 0.10 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/vendors/{vendor_id}` |
| 36 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/vendors/{vendor_id}/risk-summary` | Get Vendor Risk Summary | ❌ NOT_FOUND | 404 | 0.10 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/vendors/{vendor_id}/ri` |
| 37 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/vendors/high-risk` | Get High Risk Vendors | ❌ NOT_FOUND | 404 | 0.12 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/vendors/high-risk` |
| 38 | ner11-gold-api | 8000 | POST | `/api/v2/vendor-equipment/equipment` | Create Equipment | ⚠️ VALIDATION | 422 | 0.10 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/vendor-equipment/equipment -H 'x-custo` |
| 39 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/equipment` | Search Equipment | ✅ PASS | 200 | 0.11 | YES | - | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/equipment -H 'x-custom` |
| 40 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/equipment/{model_id}` | Get Equipment | ❌ NOT_FOUND | 404 | 0.13 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/equipment/{model_id}` |
| 41 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/equipment/approaching-eol` | Get Equipment Approaching Eol | ❌ NOT_FOUND | 404 | 0.12 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/equipment/approaching-` |
| 42 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/equipment/eol` | Get Eol Equipment | ❌ NOT_FOUND | 404 | 0.11 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/equipment/eol` |
| 43 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/maintenance-schedule` | Get Maintenance Schedule | ✅ PASS | 200 | 0.11 | YES | - | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/maintenance-schedule -` |
| 44 | ner11-gold-api | 8000 | POST | `/api/v2/vendor-equipment/vulnerabilities/flag` | Flag Vendor Vulnerability | ⚠️ VALIDATION | 422 | 0.12 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/vendor-equipment/vulnerabilities/flag ` |
| 45 | ner11-gold-api | 8000 | POST | `/api/v2/vendor-equipment/maintenance-windows` | Create Maintenance Window | ⚠️ VALIDATION | 422 | 0.11 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/vendor-equipment/maintenance-windows -` |
| 46 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/maintenance-windows` | List Maintenance Windows | ❌ ERROR | 500 | 0.11 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/maintenance-windows` |
| 47 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/maintenance-windows/{window_id}` | Get Maintenance Window | ❌ NOT_FOUND | 404 | 0.12 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/maintenance-windows/{w` |
| 48 | ner11-gold-api | 8000 | DELETE | `/api/v2/vendor-equipment/maintenance-windows/{window_id}` | Delete Maintenance Window | ❌ ERROR | 500 | 0.11 | NO | Server error (500) | `curl -X DELETE http://localhost:8000/api/v2/vendor-equipment/maintenance-windows` |
| 49 | ner11-gold-api | 8000 | POST | `/api/v2/vendor-equipment/maintenance-windows/check-conflict` | Check Maintenance Conflict | ⚠️ VALIDATION | 422 | 0.13 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/vendor-equipment/maintenance-windows/c` |
| 50 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/predictive-maintenance/{equipment_id}` | Predict Maintenance | ✅ PASS | 200 | 0.12 | YES | - | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/predictive-maintenance` |
| 51 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/predictive-maintenance/forecast` | Get Maintenance Forecast | ✅ PASS | 200 | 0.10 | YES | - | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/predictive-maintenance` |
| 52 | ner11-gold-api | 8000 | POST | `/api/v2/vendor-equipment/work-orders` | Create Work Order | ⚠️ VALIDATION | 422 | 0.10 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/vendor-equipment/work-orders -H 'x-cus` |
| 53 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/work-orders` | List Work Orders | ❌ ERROR | 500 | 0.12 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/work-orders` |
| 54 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/work-orders/{work_order_id}` | Get Work Order | ❌ NOT_FOUND | 404 | 0.11 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/work-orders/{work_orde` |
| 55 | ner11-gold-api | 8000 | PATCH | `/api/v2/vendor-equipment/work-orders/{work_order_id}/status` | Update Work Order Status | ⚠️ VALIDATION | 422 | 0.11 | PARTIAL | Needs correct parameters/body | `curl -X PATCH http://localhost:8000/api/v2/vendor-equipment/work-orders/{work_or` |
| 56 | ner11-gold-api | 8000 | GET | `/api/v2/vendor-equipment/work-orders/summary` | Get Work Order Summary | ❌ NOT_FOUND | 404 | 0.10 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/vendor-equipment/work-orders/summary` |
| 57 | ner11-gold-api | 8000 | POST | `/api/v2/threat-intel/actors` | Create Threat Actor | ⚠️ VALIDATION | 422 | 1.26 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/threat-intel/actors -H 'x-customer-id:` |
| 58 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/actors/{actor_id}` | Get Threat Actor | ❌ NOT_FOUND | 404 | 1.15 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/threat-intel/actors/{actor_id}` |
| 59 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/actors/search` | Search Threat Actors | ❌ NOT_FOUND | 404 | 1.27 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/threat-intel/actors/search` |
| 60 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/actors/active` | Get Active Threat Actors | ❌ NOT_FOUND | 404 | 1.35 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/threat-intel/actors/active` |
| 61 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/actors/by-sector/{sector}` | Get Actors By Sector | ✅ PASS | 200 | 1.25 | YES | - | `curl -X GET http://localhost:8000/api/v2/threat-intel/actors/by-sector/{sector} ` |
| 62 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/actors/{actor_id}/campaigns` | Get Actor Campaigns | ✅ PASS | 200 | 1.31 | YES | - | `curl -X GET http://localhost:8000/api/v2/threat-intel/actors/{actor_id}/campaign` |
| 63 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/actors/{actor_id}/cves` | Get Actor Cves | ✅ PASS | 200 | 1.28 | YES | - | `curl -X GET http://localhost:8000/api/v2/threat-intel/actors/{actor_id}/cves -H ` |
| 64 | ner11-gold-api | 8000 | POST | `/api/v2/threat-intel/campaigns` | Create Campaign | ⚠️ VALIDATION | 422 | 1.15 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/threat-intel/campaigns -H 'x-customer-` |
| 65 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/campaigns/{campaign_id}` | Get Campaign | ❌ NOT_FOUND | 404 | 1.18 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/threat-intel/campaigns/{campaign_id}` |
| 66 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/campaigns/search` | Search Campaigns | ❌ NOT_FOUND | 404 | 1.18 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/threat-intel/campaigns/search` |
| 67 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/campaigns/active` | Get Active Campaigns | ❌ NOT_FOUND | 404 | 1.22 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/threat-intel/campaigns/active` |
| 68 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/campaigns/{campaign_id}/iocs` | Get Campaign Iocs | ✅ PASS | 200 | 1.18 | YES | - | `curl -X GET http://localhost:8000/api/v2/threat-intel/campaigns/{campaign_id}/io` |
| 69 | ner11-gold-api | 8000 | POST | `/api/v2/threat-intel/mitre/mappings` | Create Mitre Mapping | ⚠️ VALIDATION | 422 | 1.18 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/threat-intel/mitre/mappings -H 'x-cust` |
| 70 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/mitre/mappings/entity/{entity_type}/{entity_id}` | Get Entity Mitre Mappings | ✅ PASS | 200 | 1.24 | YES | - | `curl -X GET http://localhost:8000/api/v2/threat-intel/mitre/mappings/entity/{ent` |
| 71 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/mitre/techniques/{technique_id}/actors` | Get Actors Using Technique | ✅ PASS | 200 | 1.28 | YES | - | `curl -X GET http://localhost:8000/api/v2/threat-intel/mitre/techniques/{techniqu` |
| 72 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/mitre/coverage` | Get Mitre Coverage | ✅ PASS | 200 | 1.21 | YES | - | `curl -X GET http://localhost:8000/api/v2/threat-intel/mitre/coverage -H 'x-custo` |
| 73 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/mitre/gaps` | Get Mitre Gaps | ✅ PASS | 200 | 1.22 | YES | - | `curl -X GET http://localhost:8000/api/v2/threat-intel/mitre/gaps -H 'x-customer-` |
| 74 | ner11-gold-api | 8000 | POST | `/api/v2/threat-intel/iocs` | Create Ioc | ⚠️ VALIDATION | 422 | 1.18 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/threat-intel/iocs -H 'x-customer-id: d` |
| 75 | ner11-gold-api | 8000 | POST | `/api/v2/threat-intel/iocs/bulk` | Bulk Import Iocs | ⚠️ VALIDATION | 422 | 1.18 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/threat-intel/iocs/bulk -H 'x-customer-` |
| 76 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/iocs/search` | Search Iocs | ✅ PASS | 200 | 1.35 | YES | - | `curl -X GET http://localhost:8000/api/v2/threat-intel/iocs/search -H 'x-customer` |
| 77 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/iocs/active` | Get Active Iocs | ✅ PASS | 200 | 1.21 | YES | - | `curl -X GET http://localhost:8000/api/v2/threat-intel/iocs/active -H 'x-customer` |
| 78 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/iocs/by-type/{ioc_type}` | Get Iocs By Type | ✅ PASS | 200 | 1.16 | YES | - | `curl -X GET http://localhost:8000/api/v2/threat-intel/iocs/by-type/{ioc_type} -H` |
| 79 | ner11-gold-api | 8000 | POST | `/api/v2/threat-intel/feeds` | Create Threat Feed | ⚠️ VALIDATION | 422 | 1.25 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/threat-intel/feeds -H 'x-customer-id: ` |
| 80 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/feeds` | List Threat Feeds | ❌ ERROR | 500 | 1.20 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/threat-intel/feeds` |
| 81 | ner11-gold-api | 8000 | PUT | `/api/v2/threat-intel/feeds/{feed_id}/refresh` | Trigger Feed Refresh | ⚠️ FORBIDDEN | 403 | 1.15 | NO | Requires WRITE access level | `curl -X PUT http://localhost:8000/api/v2/threat-intel/feeds/{feed_id}/refresh -H` |
| 82 | ner11-gold-api | 8000 | GET | `/api/v2/threat-intel/dashboard/summary` | Get Threat Intel Summary | ✅ PASS | 200 | 1.17 | YES | - | `curl -X GET http://localhost:8000/api/v2/threat-intel/dashboard/summary -H 'x-cu` |
| 83 | ner11-gold-api | 8000 | POST | `/api/v2/risk/scores` | Calculate Risk Score | ⚠️ VALIDATION | 422 | 0.12 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/risk/scores -H 'x-customer-id: dev' -d` |
| 84 | ner11-gold-api | 8000 | GET | `/api/v2/risk/scores/{entity_type}/{entity_id}` | Get Risk Score | ❌ ERROR | 500 | 0.12 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/risk/scores/{entity_type}/{entity_id}` |
| 85 | ner11-gold-api | 8000 | GET | `/api/v2/risk/scores/high-risk` | Get High Risk Entities | ✅ PASS | 200 | 0.11 | YES | - | `curl -X GET http://localhost:8000/api/v2/risk/scores/high-risk -H 'x-customer-id` |
| 86 | ner11-gold-api | 8000 | GET | `/api/v2/risk/scores/trending` | Get Trending Entities | ⚠️ VALIDATION | 400 | 0.11 | PARTIAL | Needs correct parameters/body | `curl -X GET http://localhost:8000/api/v2/risk/scores/trending -H 'x-customer-id:` |
| 87 | ner11-gold-api | 8000 | GET | `/api/v2/risk/scores/search` | Search Risk Scores | ✅ PASS | 200 | 0.11 | YES | - | `curl -X GET http://localhost:8000/api/v2/risk/scores/search -H 'x-customer-id: d` |
| 88 | ner11-gold-api | 8000 | POST | `/api/v2/risk/scores/recalculate/{entity_type}/{entity_id}` | Recalculate Risk Score | ❌ ERROR | 500 | 0.10 | NO | Server error (500) | `curl -X POST http://localhost:8000/api/v2/risk/scores/recalculate/{entity_type}/` |
| 89 | ner11-gold-api | 8000 | GET | `/api/v2/risk/scores/history/{entity_type}/{entity_id}` | Get Risk History | ❌ ERROR | 500 | 0.11 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/risk/scores/history/{entity_type}/{enti` |
| 90 | ner11-gold-api | 8000 | POST | `/api/v2/risk/assets/criticality` | Set Asset Criticality | ⚠️ VALIDATION | 422 | 0.10 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/risk/assets/criticality -H 'x-customer` |
| 91 | ner11-gold-api | 8000 | GET | `/api/v2/risk/assets/{asset_id}/criticality` | Get Asset Criticality | ❌ NOT_FOUND | 404 | 0.10 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/risk/assets/{asset_id}/criticality` |
| 92 | ner11-gold-api | 8000 | PUT | `/api/v2/risk/assets/{asset_id}/criticality` | Update Asset Criticality | ⚠️ VALIDATION | 422 | 0.10 | PARTIAL | Needs correct parameters/body | `curl -X PUT http://localhost:8000/api/v2/risk/assets/{asset_id}/criticality -H '` |
| 93 | ner11-gold-api | 8000 | GET | `/api/v2/risk/assets/mission-critical` | Get Mission Critical Assets | ✅ PASS | 200 | 0.10 | YES | - | `curl -X GET http://localhost:8000/api/v2/risk/assets/mission-critical -H 'x-cust` |
| 94 | ner11-gold-api | 8000 | GET | `/api/v2/risk/assets/by-criticality/{level}` | Get Assets By Criticality | ⚠️ VALIDATION | 400 | 0.10 | PARTIAL | Needs correct parameters/body | `curl -X GET http://localhost:8000/api/v2/risk/assets/by-criticality/{level} -H '` |
| 95 | ner11-gold-api | 8000 | GET | `/api/v2/risk/assets/criticality/summary` | Get Criticality Summary | ✅ PASS | 200 | 0.10 | YES | - | `curl -X GET http://localhost:8000/api/v2/risk/assets/criticality/summary -H 'x-c` |
| 96 | ner11-gold-api | 8000 | POST | `/api/v2/risk/exposure` | Calculate Exposure Score | ⚠️ VALIDATION | 422 | 0.10 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/risk/exposure -H 'x-customer-id: dev' ` |
| 97 | ner11-gold-api | 8000 | GET | `/api/v2/risk/exposure/{asset_id}` | Get Exposure Score | ❌ NOT_FOUND | 404 | 0.11 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/risk/exposure/{asset_id}` |
| 98 | ner11-gold-api | 8000 | GET | `/api/v2/risk/exposure/internet-facing` | Get Internet Facing Assets | ❌ NOT_FOUND | 404 | 0.11 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/risk/exposure/internet-facing` |
| 99 | ner11-gold-api | 8000 | GET | `/api/v2/risk/exposure/high-exposure` | Get High Exposure Assets | ❌ NOT_FOUND | 404 | 0.12 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/risk/exposure/high-exposure` |
| 100 | ner11-gold-api | 8000 | GET | `/api/v2/risk/exposure/attack-surface` | Get Attack Surface Summary | ❌ NOT_FOUND | 404 | 0.11 | NO | No data for this query | `curl -X GET http://localhost:8000/api/v2/risk/exposure/attack-surface` |
| 101 | ner11-gold-api | 8000 | GET | `/api/v2/risk/aggregation/by-vendor` | Get Risk By Vendor | ✅ PASS | 200 | 0.11 | YES | - | `curl -X GET http://localhost:8000/api/v2/risk/aggregation/by-vendor -H 'x-custom` |
| 102 | ner11-gold-api | 8000 | GET | `/api/v2/risk/aggregation/by-sector` | Get Risk By Sector | ✅ PASS | 200 | 0.10 | YES | - | `curl -X GET http://localhost:8000/api/v2/risk/aggregation/by-sector -H 'x-custom` |
| 103 | ner11-gold-api | 8000 | GET | `/api/v2/risk/aggregation/by-asset-type` | Get Risk By Asset Type | ✅ PASS | 200 | 0.10 | YES | - | `curl -X GET http://localhost:8000/api/v2/risk/aggregation/by-asset-type -H 'x-cu` |
| 104 | ner11-gold-api | 8000 | GET | `/api/v2/risk/aggregation/{aggregation_type}/{group_id}` | Get Risk Aggregation | ⚠️ VALIDATION | 400 | 0.11 | PARTIAL | Needs correct parameters/body | `curl -X GET http://localhost:8000/api/v2/risk/aggregation/{aggregation_type}/{gr` |
| 105 | ner11-gold-api | 8000 | GET | `/api/v2/risk/dashboard/summary` | Get Dashboard Summary | ✅ PASS | 200 | 0.10 | YES | - | `curl -X GET http://localhost:8000/api/v2/risk/dashboard/summary -H 'x-customer-i` |
| 106 | ner11-gold-api | 8000 | GET | `/api/v2/risk/dashboard/risk-matrix` | Get Risk Matrix | ✅ PASS | 200 | 0.10 | YES | - | `curl -X GET http://localhost:8000/api/v2/risk/dashboard/risk-matrix -H 'x-custom` |
| 107 | ner11-gold-api | 8000 | POST | `/api/v2/remediation/tasks` | Create Task | ⚠️ VALIDATION | 422 | 0.00 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/remediation/tasks -H 'x-customer-id: d` |
| 108 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/tasks/{task_id}` | Get Task | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/tasks/{task_id}` |
| 109 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/tasks/search` | Search Tasks | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/tasks/search` |
| 110 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/tasks/open` | Get Open Tasks | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/tasks/open` |
| 111 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/tasks/overdue` | Get Overdue Tasks | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/tasks/overdue` |
| 112 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/tasks/by-priority/{priority}` | Get Tasks By Priority | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/tasks/by-priority/{priority` |
| 113 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/tasks/by-status/{status}` | Get Tasks By Status | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/tasks/by-status/{status}` |
| 114 | ner11-gold-api | 8000 | PUT | `/api/v2/remediation/tasks/{task_id}/status` | Update Task Status | ⚠️ VALIDATION | 422 | 0.00 | PARTIAL | Needs correct parameters/body | `curl -X PUT http://localhost:8000/api/v2/remediation/tasks/{task_id}/status -H '` |
| 115 | ner11-gold-api | 8000 | PUT | `/api/v2/remediation/tasks/{task_id}/assign` | Assign Task | ⚠️ VALIDATION | 422 | 0.00 | PARTIAL | Needs correct parameters/body | `curl -X PUT http://localhost:8000/api/v2/remediation/tasks/{task_id}/assign -H '` |
| 116 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/tasks/{task_id}/history` | Get Task History | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/tasks/{task_id}/history` |
| 117 | ner11-gold-api | 8000 | POST | `/api/v2/remediation/plans` | Create Plan | ⚠️ VALIDATION | 422 | 0.00 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/remediation/plans -H 'x-customer-id: d` |
| 118 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/plans` | List Plans | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/plans` |
| 119 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/plans/{plan_id}` | Get Plan | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/plans/{plan_id}` |
| 120 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/plans/active` | Get Active Plans | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/plans/active` |
| 121 | ner11-gold-api | 8000 | PUT | `/api/v2/remediation/plans/{plan_id}/status` | Update Plan Status | ⚠️ VALIDATION | 422 | 0.01 | PARTIAL | Needs correct parameters/body | `curl -X PUT http://localhost:8000/api/v2/remediation/plans/{plan_id}/status -H '` |
| 122 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/plans/{plan_id}/progress` | Get Plan Progress | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/plans/{plan_id}/progress` |
| 123 | ner11-gold-api | 8000 | POST | `/api/v2/remediation/sla/policies` | Create Sla Policy | ⚠️ VALIDATION | 422 | 0.00 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/api/v2/remediation/sla/policies -H 'x-custome` |
| 124 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/sla/policies` | List Sla Policies | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/sla/policies` |
| 125 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/sla/policies/{policy_id}` | Get Sla Policy | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/sla/policies/{policy_id}` |
| 126 | ner11-gold-api | 8000 | PUT | `/api/v2/remediation/sla/policies/{policy_id}` | Update Sla Policy | ⚠️ VALIDATION | 422 | 0.00 | PARTIAL | Needs correct parameters/body | `curl -X PUT http://localhost:8000/api/v2/remediation/sla/policies/{policy_id} -H` |
| 127 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/sla/breaches` | Get Sla Breaches | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/sla/breaches` |
| 128 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/sla/at-risk` | Get At Risk Tasks | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/sla/at-risk` |
| 129 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/metrics/summary` | Get Metrics Summary | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/metrics/summary` |
| 130 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/metrics/mttr` | Get Mttr By Severity | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/metrics/mttr` |
| 131 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/metrics/sla-compliance` | Get Sla Compliance | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/metrics/sla-compliance` |
| 132 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/metrics/backlog` | Get Backlog Metrics | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/metrics/backlog` |
| 133 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/metrics/trends` | Get Remediation Trends | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/metrics/trends` |
| 134 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/dashboard/summary` | Get Dashboard Summary | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/dashboard/summary` |
| 135 | ner11-gold-api | 8000 | GET | `/api/v2/remediation/dashboard/workload` | Get Workload Distribution | ❌ ERROR | 500 | 0.00 | NO | Server error (500) | `curl -X GET http://localhost:8000/api/v2/remediation/dashboard/workload` |
| 136 | ner11-gold-api | 8000 | POST | `/ner` | Extract Entities | ⚠️ VALIDATION | 422 | 0.00 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/ner -H 'x-customer-id: dev' -d '{...}'` |
| 137 | ner11-gold-api | 8000 | POST | `/search/semantic` | Semantic Search | ⚠️ VALIDATION | 422 | 0.00 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/search/semantic -H 'x-customer-id: dev' -d '{` |
| 138 | ner11-gold-api | 8000 | POST | `/search/hybrid` | Hybrid Search | ⚠️ VALIDATION | 422 | 0.00 | PARTIAL | Needs correct parameters/body | `curl -X POST http://localhost:8000/search/hybrid -H 'x-customer-id: dev' -d '{..` |
| 139 | ner11-gold-api | 8000 | GET | `/health` | Health Check | ✅ PASS | 200 | 0.00 | YES | - | `curl -X GET http://localhost:8000/health` |
| 140 | ner11-gold-api | 8000 | GET | `/info` | Model Info | ✅ PASS | 200 | 0.00 | YES | - | `curl -X GET http://localhost:8000/info` |
| 141 | aeon-saas-dev | 3000 | GET | `/api/pipeline/status/[jobId]` | Next.js API route | ❌ NOT_FOUND | 404 | 2.27 | NO | No data for this query | `curl -X GET http://localhost:3000/api/pipeline/status/[jobId]` |
| 142 | aeon-saas-dev | 3000 | GET | `/api/pipeline/process` | Next.js API route | ❌ ERROR | 401 | 1.15 | NO | Server error (401) | `curl -X GET http://localhost:3000/api/pipeline/process` |
| 143 | aeon-saas-dev | 3000 | GET | `/api/query-control/queries` | Next.js API route | ❌ TIMEOUT | - | >5 | NO | Connection timeout | - |
| 144 | aeon-saas-dev | 3000 | GET | `/api/query-control/queries/[queryId]/checkpoints` | Next.js API route | ❌ ERROR | 500 | 2.59 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/query-control/queries/[queryId]/checkpoint` |
| 145 | aeon-saas-dev | 3000 | GET | `/api/query-control/queries/[queryId]/model` | Next.js API route | ❌ ERROR | 500 | 0.44 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/query-control/queries/[queryId]/model` |
| 146 | aeon-saas-dev | 3000 | GET | `/api/query-control/queries/[queryId]` | Next.js API route | ❌ ERROR | 500 | 0.46 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/query-control/queries/[queryId]` |
| 147 | aeon-saas-dev | 3000 | GET | `/api/query-control/queries/[queryId]/permissions` | Next.js API route | ❌ ERROR | 500 | 0.48 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/query-control/queries/[queryId]/permission` |
| 148 | aeon-saas-dev | 3000 | GET | `/api/query-control/queries/[queryId]/resume` | Next.js API route | ❌ ERROR | 500 | 0.49 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/query-control/queries/[queryId]/resume` |
| 149 | aeon-saas-dev | 3000 | GET | `/api/query-control/queries/[queryId]/pause` | Next.js API route | ❌ ERROR | 500 | 0.48 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/query-control/queries/[queryId]/pause` |
| 150 | aeon-saas-dev | 3000 | GET | `/api/dashboard/metrics` | Next.js API route | ❌ ERROR | 500 | 0.47 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/dashboard/metrics` |
| 151 | aeon-saas-dev | 3000 | GET | `/api/dashboard/distribution` | Next.js API route | ❌ ERROR | 500 | 0.57 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/dashboard/distribution` |
| 152 | aeon-saas-dev | 3000 | GET | `/api/dashboard/activity` | Next.js API route | ❌ ERROR | 500 | 0.64 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/dashboard/activity` |
| 153 | aeon-saas-dev | 3000 | GET | `/api/search` | Next.js API route | ❌ ERROR | 500 | 2.49 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/search` |
| 154 | aeon-saas-dev | 3000 | GET | `/api/chat` | Next.js API route | ❌ ERROR | 500 | 1.18 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/chat` |
| 155 | aeon-saas-dev | 3000 | GET | `/api/threats/geographic` | Next.js API route | ❌ ERROR | 500 | 0.63 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/threats/geographic` |
| 156 | aeon-saas-dev | 3000 | GET | `/api/threats/ics` | Next.js API route | ❌ ERROR | 500 | 0.72 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/threats/ics` |
| 157 | aeon-saas-dev | 3000 | GET | `/api/customers/[id]` | Next.js API route | ❌ ERROR | 500 | 0.65 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/customers/[id]` |
| 158 | aeon-saas-dev | 3000 | GET | `/api/customers` | Next.js API route | ❌ ERROR | 500 | 0.80 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/customers` |
| 159 | aeon-saas-dev | 3000 | GET | `/api/backend/test` | Next.js API route | ❌ ERROR | 500 | 0.74 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/backend/test` |
| 160 | aeon-saas-dev | 3000 | GET | `/api/upload` | Next.js API route | ❌ ERROR | 500 | 0.76 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/upload` |
| 161 | aeon-saas-dev | 3000 | GET | `/api/activity/recent` | Next.js API route | ❌ ERROR | 500 | 1.34 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/activity/recent` |
| 162 | aeon-saas-dev | 3000 | GET | `/api/health` | Next.js API route | ❌ ERROR | 500 | 0.03 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/health` |
| 163 | aeon-saas-dev | 3000 | GET | `/api/analytics/timeseries` | Next.js API route | ❌ ERROR | 500 | 0.78 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/analytics/timeseries` |
| 164 | aeon-saas-dev | 3000 | GET | `/api/analytics/metrics` | Next.js API route | ❌ ERROR | 500 | 0.78 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/analytics/metrics` |
| 165 | aeon-saas-dev | 3000 | GET | `/api/analytics/trends/threat-timeline` | Next.js API route | ❌ ERROR | 500 | 0.87 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/analytics/trends/threat-timeline` |
| 166 | aeon-saas-dev | 3000 | GET | `/api/analytics/trends/cve` | Next.js API route | ❌ ERROR | 500 | 0.80 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/analytics/trends/cve` |
| 167 | aeon-saas-dev | 3000 | GET | `/api/analytics/trends/seasonality` | Next.js API route | ❌ ERROR | 500 | 0.88 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/analytics/trends/seasonality` |
| 168 | aeon-saas-dev | 3000 | GET | `/api/analytics/export` | Next.js API route | ❌ ERROR | 500 | 0.86 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/analytics/export` |
| 169 | aeon-saas-dev | 3000 | GET | `/api/threat-intel/ics` | Next.js API route | ❌ ERROR | 500 | 0.83 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/threat-intel/ics` |
| 170 | aeon-saas-dev | 3000 | GET | `/api/threat-intel/landscape` | Next.js API route | ❌ ERROR | 500 | 0.94 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/threat-intel/landscape` |
| 171 | aeon-saas-dev | 3000 | GET | `/api/threat-intel/analytics` | Next.js API route | ❌ ERROR | 500 | 0.80 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/threat-intel/analytics` |
| 172 | aeon-saas-dev | 3000 | GET | `/api/threat-intel/vulnerabilities` | Next.js API route | ❌ ERROR | 500 | 1.00 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/threat-intel/vulnerabilities` |
| 173 | aeon-saas-dev | 3000 | GET | `/api/tags/[id]` | Next.js API route | ❌ ERROR | 500 | 0.92 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/tags/[id]` |
| 174 | aeon-saas-dev | 3000 | GET | `/api/tags` | Next.js API route | ❌ ERROR | 500 | 0.92 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/tags` |
| 175 | aeon-saas-dev | 3000 | GET | `/api/tags/assign` | Next.js API route | ❌ ERROR | 500 | 1.04 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/tags/assign` |
| 176 | aeon-saas-dev | 3000 | GET | `/api/observability/performance` | Next.js API route | ❌ ERROR | 500 | 1.13 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/observability/performance` |
| 177 | aeon-saas-dev | 3000 | GET | `/api/observability/system` | Next.js API route | ❌ ERROR | 500 | 1.06 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/observability/system` |
| 178 | aeon-saas-dev | 3000 | GET | `/api/observability/agents` | Next.js API route | ❌ ERROR | 500 | 1.03 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/observability/agents` |
| 179 | aeon-saas-dev | 3000 | GET | `/api/graph/query` | Next.js API route | ❌ ERROR | 500 | 0.99 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/graph/query` |
| 180 | aeon-saas-dev | 3000 | GET | `/api/neo4j/statistics` | Next.js API route | ❌ ERROR | 500 | 1.07 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/neo4j/statistics` |
| 181 | aeon-saas-dev | 3000 | GET | `/api/neo4j/cyber-statistics` | Next.js API route | ❌ ERROR | 500 | 1.02 | NO | Server error (500) | `curl -X GET http://localhost:3000/api/neo4j/cyber-statistics` |

## AUDIT SUMMARY

- **Total APIs Audited**: 181
- **Passed (200/201)**: 36 (19%)
- **Failed (404/5xx)**: 106 (58%)
- **Validation (4xx)**: 39 (21%)

**Audit Started**: 2025-12-12 19:34:48
**Audit Completed**: 2025-12-12 19:36:12
**Total Duration**: 83.1 seconds

## AUDIT CERTIFICATION

This audit certifies that:
- ✅ ALL APIs across all services were tested
- ✅ Each API was tested with fresh HTTP requests
- ✅ No previous results were used
- ✅ Complete Pass/Fail status documented
- ✅ Failure reasons provided
- ✅ Access methods documented

**Auditor**: Automated System
**Audit ID**: AUDIT-20251212-193448
