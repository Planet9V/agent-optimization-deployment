# AEON MASTER API TABLE - ALL 181 ENDPOINTS

**Generated**: 2025-12-12
**Total APIs**: 181 (5 NER + 135 Phase B + 41 Next.js)
**Status**: Production Ready

---

## QUICK REFERENCE

| Service | Port | APIs | Auth Required | Status |
|---------|------|------|---------------|--------|
| NER11 Model | 8000 | 5 | ❌ No | ✅ Active |
| Phase B APIs | 8000 | 135 | ✅ Yes (`x-customer-id`) | ✅ Active |
| Next.js APIs | 3000 | 41 | ✅ Yes (Clerk) | ✅ Active |

---

## TABLE OF CONTENTS

1. [NER11 APIs (5)](#ner11-apis-port-8000---no-auth)
2. [Phase B2 - SBOM APIs (32)](#phase-b2---sbom-apis-32)
3. [Phase B2 - Vendor Equipment APIs (24)](#phase-b2---vendor-equipment-apis-24)
4. [Phase B3 - Threat Intel APIs (26)](#phase-b3---threat-intel-apis-26)
5. [Phase B3 - Risk Scoring APIs (24)](#phase-b3---risk-scoring-apis-24)
6. [Phase B3 - Remediation APIs (29)](#phase-b3---remediation-apis-29)
7. [Phase B4 - Scanning APIs (30)](#phase-b4---scanning-apis-30)
8. [Phase B4 - Alerts APIs (30)](#phase-b4---alerts-apis-30)
9. [Phase B4 - Compliance APIs (28)](#phase-b4---compliance-apis-28)
10. [Phase B5 - Economic Impact APIs (27)](#phase-b5---economic-impact-apis-27)
11. [Phase B5 - Demographics APIs (24)](#phase-b5---demographics-apis-24)
12. [Phase B5 - Prioritization APIs (28)](#phase-b5---prioritization-apis-28)
13. [Next.js APIs (41)](#nextjs-apis-port-3000)

---

# CORE APIs

## NER11 APIs (Port 8000 - No Auth)

| # | Name | Method | Endpoint | Description | Access Example | Use For |
|---|------|--------|----------|-------------|----------------|---------|
| 1 | Extract Entities | POST | /ner | Extract named entities from text (60 types) | `curl -X POST http://localhost:8000/ner -H "Content-Type: application/json" -d '{"text":"APT29 exploited CVE-2024-12345"}'` | Entity extraction in UI, threat analysis |
| 2 | Semantic Search | POST | /search/semantic | Search entities using vector similarity | `curl -X POST http://localhost:8000/search/semantic -H "Content-Type: application/json" -d '{"query":"ransomware","limit":10}'` | Find similar threats, search knowledge base |
| 3 | Hybrid Search | POST | /search/hybrid | Combined vector + graph search (up to 20-hop traversal) | `curl -X POST http://localhost:8000/search/hybrid -H "Content-Type: application/json" -d '{"query":"APT29","expand_graph":true,"hop_depth":2}'` | Explore threat relationships, campaign analysis |
| 4 | Health Check | GET | /health | Check NER service health and capabilities | `curl http://localhost:8000/health` | Health monitoring, service verification |
| 5 | Model Info | GET | /info | Get model capabilities and label information | `curl http://localhost:8000/info` | Discover available entity types, model version |

---

# PHASE B APIS (Port 8000 - Auth Required)

**Auth Header**: All Phase B APIs require: `-H "x-customer-id: your-customer-id"`

## Phase B2 - SBOM APIs (32)

| # | Name | Method | Endpoint | Description | Access Example | Use For |
|---|------|--------|----------|-------------|----------------|---------|
| 6 | List SBOMs | GET | /api/v2/sbom/sboms | List all Software Bill of Materials | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/sboms` | View all SBOMs |
| 7 | Get SBOM | GET | /api/v2/sbom/sboms/{sbom_id} | Get specific SBOM details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/sboms/sbom-123` | View SBOM details |
| 8 | Create SBOM | POST | /api/v2/sbom/sboms | Create new SBOM | `curl -X POST -H "x-customer-id: dev" -H "Content-Type: application/json" http://localhost:8000/api/v2/sbom/sboms -d '{}'` | Import SBOM data |
| 9 | Update SBOM | PUT | /api/v2/sbom/sboms/{sbom_id} | Update SBOM | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/sboms/sbom-123` | Modify SBOM |
| 10 | Delete SBOM | DELETE | /api/v2/sbom/sboms/{sbom_id} | Delete SBOM | `curl -X DELETE -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/sboms/sbom-123` | Remove SBOM |
| 11 | List Components | GET | /api/v2/sbom/components | List all software components | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/components` | View components |
| 12 | Get Component | GET | /api/v2/sbom/components/{component_id} | Get component details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/components/comp-123` | Component details |
| 13 | Create Component | POST | /api/v2/sbom/components | Create new component | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/components` | Add component |
| 14 | Update Component | PUT | /api/v2/sbom/components/{component_id} | Update component | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/components/comp-123` | Modify component |
| 15 | Delete Component | DELETE | /api/v2/sbom/components/{component_id} | Delete component | `curl -X DELETE -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/components/comp-123` | Remove component |
| 16 | Component Vulnerabilities | GET | /api/v2/sbom/components/{component_id}/vulnerabilities | Get component vulnerabilities | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/components/comp-123/vulnerabilities` | Check vulnerabilities |
| 17 | Component Dependencies | GET | /api/v2/sbom/components/{component_id}/dependencies | Get component dependencies | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/components/comp-123/dependencies` | View dependencies |
| 18 | Component License | GET | /api/v2/sbom/components/{component_id}/license | Get component license | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/components/comp-123/license` | Check license |
| 19 | List Licenses | GET | /api/v2/sbom/licenses | List all licenses | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/licenses` | View licenses |
| 20 | Get License | GET | /api/v2/sbom/licenses/{license_id} | Get license details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/licenses/lic-123` | License details |
| 21 | License Compliance | GET | /api/v2/sbom/licenses/{license_id}/compliance | Get license compliance | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/licenses/lic-123/compliance` | Check compliance |
| 22 | List Vulnerabilities | GET | /api/v2/sbom/vulnerabilities | List all vulnerabilities | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/vulnerabilities` | View vulnerabilities |
| 23 | Get Vulnerability | GET | /api/v2/sbom/vulnerabilities/{vuln_id} | Get vulnerability details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/vulnerabilities/vuln-123` | Vulnerability details |
| 24 | Vulnerability Patch Status | GET | /api/v2/sbom/vulnerabilities/{vuln_id}/patch-status | Get patch availability | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/vulnerabilities/vuln-123/patch-status` | Check patches |
| 25 | Vulnerability Affected Components | GET | /api/v2/sbom/vulnerabilities/{vuln_id}/affected-components | Get affected components | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/vulnerabilities/vuln-123/affected-components` | View impact |
| 26 | SBOM Summary | GET | /api/v2/sbom/dashboard/summary | Get SBOM dashboard summary | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/dashboard/summary` | Dashboard overview |
| 27 | Vulnerability Dashboard | GET | /api/v2/sbom/dashboard/vulnerabilities | Get vulnerability dashboard | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/dashboard/vulnerabilities` | Vuln overview |
| 28 | License Dashboard | GET | /api/v2/sbom/dashboard/licenses | Get license dashboard | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/dashboard/licenses` | License overview |
| 29 | Component Risk Analysis | GET | /api/v2/sbom/analysis/component-risk | Analyze component risk | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/analysis/component-risk` | Risk analysis |
| 30 | Dependency Analysis | GET | /api/v2/sbom/analysis/dependencies | Analyze dependencies | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/analysis/dependencies` | Dependency check |
| 31 | License Risk Analysis | GET | /api/v2/sbom/analysis/license-risk | Analyze license risk | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/analysis/license-risk` | License risk |
| 32 | SBOM Comparison | POST | /api/v2/sbom/analysis/compare | Compare two SBOMs | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/analysis/compare` | Compare versions |
| 33 | Export SBOM | GET | /api/v2/sbom/export/{sbom_id} | Export SBOM (CycloneDX, SPDX) | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/export/sbom-123` | Export data |
| 34 | Import SBOM | POST | /api/v2/sbom/import | Import SBOM from file | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/import` | Import SBOM |
| 35 | SBOM Validation | POST | /api/v2/sbom/validate | Validate SBOM format | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/validate` | Validate SBOM |
| 36 | SBOM Stats | GET | /api/v2/sbom/stats | Get SBOM statistics | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/stats` | View stats |
| 37 | Recent Activity | GET | /api/v2/sbom/activity/recent | Get recent SBOM activity | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/sbom/activity/recent` | Activity log |

## Phase B2 - Vendor Equipment APIs (24)

| # | Name | Method | Endpoint | Description | Access Example | Use For |
|---|------|--------|----------|-------------|----------------|---------|
| 38 | List Equipment | GET | /api/v2/equipment/equipment | List all equipment | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/equipment` | View equipment |
| 39 | Get Equipment | GET | /api/v2/equipment/equipment/{equip_id} | Get equipment details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/equipment/eq-123` | Equipment details |
| 40 | Create Equipment | POST | /api/v2/equipment/equipment | Create new equipment | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/equipment` | Add equipment |
| 41 | Update Equipment | PUT | /api/v2/equipment/equipment/{equip_id} | Update equipment | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/equipment/eq-123` | Modify equipment |
| 42 | Delete Equipment | DELETE | /api/v2/equipment/equipment/{equip_id} | Delete equipment | `curl -X DELETE -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/equipment/eq-123` | Remove equipment |
| 43 | Equipment Vulnerabilities | GET | /api/v2/equipment/equipment/{equip_id}/vulnerabilities | Get equipment vulnerabilities | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/equipment/eq-123/vulnerabilities` | Check vulns |
| 44 | Equipment EOL Status | GET | /api/v2/equipment/equipment/{equip_id}/eol-status | Get end-of-life status | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/equipment/eq-123/eol-status` | EOL check |
| 45 | List Vendors | GET | /api/v2/equipment/vendors | List all vendors | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/vendors` | View vendors |
| 46 | Get Vendor | GET | /api/v2/equipment/vendors/{vendor_id} | Get vendor details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/vendors/ven-123` | Vendor details |
| 47 | Vendor Equipment | GET | /api/v2/equipment/vendors/{vendor_id}/equipment | Get vendor equipment | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/vendors/ven-123/equipment` | Vendor assets |
| 48 | Vendor Security Rating | GET | /api/v2/equipment/vendors/{vendor_id}/security-rating | Get vendor security rating | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/vendors/ven-123/security-rating` | Vendor rating |
| 49 | Equipment Dashboard | GET | /api/v2/equipment/dashboard/summary | Get equipment dashboard | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/dashboard/summary` | Dashboard view |
| 50 | EOL Report | GET | /api/v2/equipment/dashboard/eol-report | Get EOL report | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/dashboard/eol-report` | EOL overview |
| 51 | Vulnerability Report | GET | /api/v2/equipment/dashboard/vulnerability-report | Get vulnerability report | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/dashboard/vulnerability-report` | Vuln report |
| 52 | Equipment Risk Analysis | GET | /api/v2/equipment/analysis/risk | Analyze equipment risk | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/analysis/risk` | Risk analysis |
| 53 | EOL Analysis | GET | /api/v2/equipment/analysis/eol | Analyze EOL equipment | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/analysis/eol` | EOL analysis |
| 54 | Patch Coverage | GET | /api/v2/equipment/analysis/patch-coverage | Analyze patch coverage | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/analysis/patch-coverage` | Patch status |
| 55 | Maintenance Schedule | GET | /api/v2/equipment/maintenance/schedule | Get maintenance schedule | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/maintenance/schedule` | Maintenance plan |
| 56 | Upcoming Maintenance | GET | /api/v2/equipment/maintenance/upcoming | Get upcoming maintenance | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/maintenance/upcoming` | Next maintenance |
| 57 | Maintenance History | GET | /api/v2/equipment/maintenance/history | Get maintenance history | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/maintenance/history` | Past maintenance |
| 58 | Equipment Export | GET | /api/v2/equipment/export | Export equipment data | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/export` | Export data |
| 59 | Equipment Import | POST | /api/v2/equipment/import | Import equipment data | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/import` | Import data |
| 60 | Equipment Stats | GET | /api/v2/equipment/stats | Get equipment statistics | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/stats` | View stats |
| 61 | Recent Activity | GET | /api/v2/equipment/activity/recent | Get recent equipment activity | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/equipment/activity/recent` | Activity log |

## Phase B3 - Threat Intel APIs (26)

| # | Name | Method | Endpoint | Description | Access Example | Use For |
|---|------|--------|----------|-------------|----------------|---------|
| 62 | List Threat Actors | GET | /api/v2/threat-intel/actors | List all threat actors | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/actors` | View actors |
| 63 | Get Threat Actor | GET | /api/v2/threat-intel/actors/{actor_id} | Get threat actor details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/actors/apt29` | Actor details |
| 64 | Actor TTPs | GET | /api/v2/threat-intel/actors/{actor_id}/ttps | Get actor TTPs | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/actors/apt29/ttps` | View tactics |
| 65 | Actor Campaigns | GET | /api/v2/threat-intel/actors/{actor_id}/campaigns | Get actor campaigns | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/actors/apt29/campaigns` | View campaigns |
| 66 | List Campaigns | GET | /api/v2/threat-intel/campaigns | List all campaigns | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/campaigns` | View campaigns |
| 67 | Get Campaign | GET | /api/v2/threat-intel/campaigns/{campaign_id} | Get campaign details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/campaigns/camp-123` | Campaign details |
| 68 | Campaign Timeline | GET | /api/v2/threat-intel/campaigns/{campaign_id}/timeline | Get campaign timeline | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/campaigns/camp-123/timeline` | View timeline |
| 69 | Campaign Indicators | GET | /api/v2/threat-intel/campaigns/{campaign_id}/indicators | Get campaign indicators | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/campaigns/camp-123/indicators` | View IOCs |
| 70 | List IOCs | GET | /api/v2/threat-intel/iocs | List all indicators | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/iocs` | View IOCs |
| 71 | Get IOC | GET | /api/v2/threat-intel/iocs/{ioc_id} | Get IOC details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/iocs/ioc-123` | IOC details |
| 72 | IOC Enrichment | GET | /api/v2/threat-intel/iocs/{ioc_id}/enrichment | Get IOC enrichment data | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/iocs/ioc-123/enrichment` | Enrich IOC |
| 73 | List TTPs | GET | /api/v2/threat-intel/ttps | List all TTPs | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/ttps` | View TTPs |
| 74 | Get TTP | GET | /api/v2/threat-intel/ttps/{ttp_id} | Get TTP details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/ttps/t1566` | TTP details |
| 75 | TTP Detection | GET | /api/v2/threat-intel/ttps/{ttp_id}/detection | Get TTP detection methods | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/ttps/t1566/detection` | Detection rules |
| 76 | TTP Mitigation | GET | /api/v2/threat-intel/ttps/{ttp_id}/mitigation | Get TTP mitigation | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/ttps/t1566/mitigation` | Mitigations |
| 77 | Threat Dashboard | GET | /api/v2/threat-intel/dashboard/summary | Get threat intel dashboard | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/dashboard/summary` | Dashboard view |
| 78 | Active Campaigns | GET | /api/v2/threat-intel/dashboard/active-campaigns | Get active campaigns | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/dashboard/active-campaigns` | Active threats |
| 79 | Trending TTPs | GET | /api/v2/threat-intel/dashboard/trending-ttps | Get trending TTPs | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/dashboard/trending-ttps` | Trending tactics |
| 80 | Threat Landscape | GET | /api/v2/threat-intel/analysis/threat-landscape | Analyze threat landscape | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/analysis/threat-landscape` | Landscape view |
| 81 | Actor Attribution | POST | /api/v2/threat-intel/analysis/attribution | Analyze actor attribution | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/analysis/attribution` | Attribute attack |
| 82 | IOC Correlation | POST | /api/v2/threat-intel/analysis/ioc-correlation | Correlate IOCs | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/analysis/ioc-correlation` | Find patterns |
| 83 | Export Intel | GET | /api/v2/threat-intel/export | Export threat intelligence | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/export` | Export data |
| 84 | Import Intel | POST | /api/v2/threat-intel/import | Import threat intelligence | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/import` | Import feeds |
| 85 | Intel Feed Status | GET | /api/v2/threat-intel/feeds/status | Get intel feed status | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/feeds/status` | Check feeds |
| 86 | Update Intel Feed | POST | /api/v2/threat-intel/feeds/update | Update intel feed | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/feeds/update` | Refresh feeds |
| 87 | Recent Activity | GET | /api/v2/threat-intel/activity/recent | Get recent threat activity | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/threat-intel/activity/recent` | Activity log |

## Phase B3 - Risk Scoring APIs (24)

| # | Name | Method | Endpoint | Description | Access Example | Use For |
|---|------|--------|----------|-------------|----------------|---------|
| 88 | List Risk Scores | GET | /api/v2/risk/scores | List all risk scores | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/scores` | View risk scores |
| 89 | Get Risk Score | GET | /api/v2/risk/scores/{entity_id} | Get entity risk score | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/scores/ent-123` | Check risk |
| 90 | Calculate Risk | POST | /api/v2/risk/scores/calculate | Calculate risk score | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/scores/calculate` | Score entity |
| 91 | High Risk Entities | GET | /api/v2/risk/scores/high-risk | Get high risk entities | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/scores/high-risk` | Critical risks |
| 92 | Risk Trends | GET | /api/v2/risk/trends | Get risk trends | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/trends` | View trends |
| 93 | Risk by Severity | GET | /api/v2/risk/trends/by-severity | Get risk by severity | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/trends/by-severity` | Severity breakdown |
| 94 | Risk Timeline | GET | /api/v2/risk/trends/timeline | Get risk timeline | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/trends/timeline` | Historical risk |
| 95 | Risk Dashboard | GET | /api/v2/risk/dashboard/summary | Get risk dashboard | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/dashboard/summary` | Dashboard view |
| 96 | Risk Heatmap | GET | /api/v2/risk/dashboard/heatmap | Get risk heatmap | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/dashboard/heatmap` | Visual heatmap |
| 97 | Top Risks | GET | /api/v2/risk/dashboard/top-risks | Get top risks | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/dashboard/top-risks` | Critical items |
| 98 | Risk by Category | GET | /api/v2/risk/analysis/by-category | Analyze risk by category | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/analysis/by-category` | Category breakdown |
| 99 | Risk Factors | GET | /api/v2/risk/analysis/risk-factors | Get risk factors | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/analysis/risk-factors` | Factor analysis |
| 100 | Impact Assessment | POST | /api/v2/risk/analysis/impact-assessment | Assess impact | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/analysis/impact-assessment` | Impact analysis |
| 101 | Likelihood Analysis | POST | /api/v2/risk/analysis/likelihood | Analyze likelihood | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/analysis/likelihood` | Probability calc |
| 102 | List Risk Models | GET | /api/v2/risk/models | List risk models | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/models` | View models |
| 103 | Get Risk Model | GET | /api/v2/risk/models/{model_id} | Get risk model | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/models/model-123` | Model details |
| 104 | Create Risk Model | POST | /api/v2/risk/models | Create risk model | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/models` | New model |
| 105 | Update Risk Model | PUT | /api/v2/risk/models/{model_id} | Update risk model | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/models/model-123` | Modify model |
| 106 | Risk Acceptance | POST | /api/v2/risk/acceptance | Accept risk | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/acceptance` | Accept risk |
| 107 | Accepted Risks | GET | /api/v2/risk/acceptance/list | List accepted risks | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/acceptance/list` | View accepted |
| 108 | Risk Export | GET | /api/v2/risk/export | Export risk data | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/export` | Export data |
| 109 | Risk Report | GET | /api/v2/risk/reports/summary | Generate risk report | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/reports/summary` | Report generation |
| 110 | Risk Stats | GET | /api/v2/risk/stats | Get risk statistics | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/stats` | View stats |
| 111 | Recent Activity | GET | /api/v2/risk/activity/recent | Get recent risk activity | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/risk/activity/recent` | Activity log |

## Phase B3 - Remediation APIs (29)

| # | Name | Method | Endpoint | Description | Access Example | Use For |
|---|------|--------|----------|-------------|----------------|---------|
| 112 | Dashboard Summary | GET | /api/v2/remediation/dashboard/summary | Get remediation dashboard | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/dashboard/summary` | Dashboard view |
| 113 | Workload Distribution | GET | /api/v2/remediation/dashboard/workload | Get team workload | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/dashboard/workload` | Team capacity |
| 114 | Backlog Metrics | GET | /api/v2/remediation/metrics/backlog | Get backlog metrics | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/metrics/backlog` | Backlog size |
| 115 | MTTR by Severity | GET | /api/v2/remediation/metrics/mttr | Get MTTR by severity | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/metrics/mttr` | Response time |
| 116 | SLA Compliance | GET | /api/v2/remediation/metrics/sla-compliance | Get SLA compliance | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/metrics/sla-compliance` | SLA tracking |
| 117 | Metrics Summary | GET | /api/v2/remediation/metrics/summary | Get metrics summary | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/metrics/summary` | Overall metrics |
| 118 | Remediation Trends | GET | /api/v2/remediation/metrics/trends | Get remediation trends | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/metrics/trends` | Trend analysis |
| 119 | Create Plan | POST | /api/v2/remediation/plans | Create remediation plan | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/plans` | New plan |
| 120 | List Plans | GET | /api/v2/remediation/plans | List remediation plans | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/plans` | View plans |
| 121 | Active Plans | GET | /api/v2/remediation/plans/active | Get active plans | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/plans/active` | Current plans |
| 122 | Get Plan | GET | /api/v2/remediation/plans/{plan_id} | Get plan details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/plans/plan-123` | Plan details |
| 123 | Plan Progress | GET | /api/v2/remediation/plans/{plan_id}/progress | Get plan progress | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/plans/plan-123/progress` | Track progress |
| 124 | Update Plan Status | PUT | /api/v2/remediation/plans/{plan_id}/status | Update plan status | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/plans/plan-123/status` | Change status |
| 125 | At Risk Tasks | GET | /api/v2/remediation/sla/at-risk | Get at-risk tasks | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/sla/at-risk` | SLA violations |
| 126 | SLA Violations | GET | /api/v2/remediation/sla/violations | Get SLA violations | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/sla/violations` | Missed SLAs |
| 127 | Create Task | POST | /api/v2/remediation/tasks | Create remediation task | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/tasks` | New task |
| 128 | List Tasks | GET | /api/v2/remediation/tasks | List remediation tasks | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/tasks` | View tasks |
| 129 | High Priority Tasks | GET | /api/v2/remediation/tasks/high-priority | Get high priority tasks | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/tasks/high-priority` | Critical tasks |
| 130 | Overdue Tasks | GET | /api/v2/remediation/tasks/overdue | Get overdue tasks | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/tasks/overdue` | Late tasks |
| 131 | Get Task | GET | /api/v2/remediation/tasks/{task_id} | Get task details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/tasks/task-123` | Task details |
| 132 | Assign Task | PUT | /api/v2/remediation/tasks/{task_id}/assign | Assign task | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/tasks/task-123/assign` | Assign work |
| 133 | Update Task Status | PUT | /api/v2/remediation/tasks/{task_id}/status | Update task status | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/tasks/task-123/status` | Change status |
| 134 | Template Library | GET | /api/v2/remediation/templates | List task templates | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/templates` | View templates |
| 135 | Get Template | GET | /api/v2/remediation/templates/{template_id} | Get template | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/templates/tmp-123` | Template details |
| 136 | Remediation History | GET | /api/v2/remediation/timeline/history | Get remediation history | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/timeline/history` | Historical data |
| 137 | Team Performance | GET | /api/v2/remediation/teams/performance | Get team performance | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/teams/performance` | Team metrics |
| 138 | Export Remediation | GET | /api/v2/remediation/export | Export remediation data | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/export` | Export data |
| 139 | Remediation Stats | GET | /api/v2/remediation/stats | Get statistics | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/stats` | View stats |
| 140 | Recent Activity | GET | /api/v2/remediation/activity/recent | Get recent activity | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/remediation/activity/recent` | Activity log |

## Phase B4 - Scanning APIs (30)

| # | Name | Method | Endpoint | Description | Access Example | Use For |
|---|------|--------|----------|-------------|----------------|---------|
| 141 | List Scans | GET | /api/v2/scanning/scans | List all scans | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/scans` | View scans |
| 142 | Create Scan | POST | /api/v2/scanning/scans | Create new scan | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/scans` | Start scan |
| 143 | Get Scan | GET | /api/v2/scanning/scans/{scan_id} | Get scan details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/scans/scan-123` | Scan details |
| 144 | Scan Results | GET | /api/v2/scanning/scans/{scan_id}/results | Get scan results | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/scans/scan-123/results` | View findings |
| 145 | Scan Status | GET | /api/v2/scanning/scans/{scan_id}/status | Get scan status | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/scans/scan-123/status` | Check progress |
| 146 | Stop Scan | PUT | /api/v2/scanning/scans/{scan_id}/stop | Stop running scan | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/scans/scan-123/stop` | Cancel scan |
| 147 | Active Scans | GET | /api/v2/scanning/scans/active | Get active scans | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/scans/active` | Running scans |
| 148 | Scheduled Scans | GET | /api/v2/scanning/scans/scheduled | Get scheduled scans | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/scans/scheduled` | Future scans |
| 149 | Scan Dashboard | GET | /api/v2/scanning/dashboard/summary | Get scan dashboard | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/dashboard/summary` | Dashboard view |
| 150 | Coverage Report | GET | /api/v2/scanning/dashboard/coverage | Get coverage report | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/dashboard/coverage` | Scan coverage |
| 151 | Findings Summary | GET | /api/v2/scanning/dashboard/findings | Get findings summary | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/dashboard/findings` | Finding stats |
| 152 | Create Schedule | POST | /api/v2/scanning/schedules | Create scan schedule | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/schedules` | Schedule scan |
| 153 | List Schedules | GET | /api/v2/scanning/schedules | List scan schedules | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/schedules` | View schedules |
| 154 | Get Schedule | GET | /api/v2/scanning/schedules/{schedule_id} | Get schedule details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/schedules/sched-123` | Schedule details |
| 155 | Update Schedule | PUT | /api/v2/scanning/schedules/{schedule_id} | Update schedule | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/schedules/sched-123` | Modify schedule |
| 156 | Delete Schedule | DELETE | /api/v2/scanning/schedules/{schedule_id} | Delete schedule | `curl -X DELETE -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/schedules/sched-123` | Remove schedule |
| 157 | Create Target | POST | /api/v2/scanning/targets | Create scan target | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/targets` | Add target |
| 158 | List Targets | GET | /api/v2/scanning/targets | List scan targets | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/targets` | View targets |
| 159 | Get Target | GET | /api/v2/scanning/targets/{target_id} | Get target details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/targets/tgt-123` | Target details |
| 160 | Update Target | PUT | /api/v2/scanning/targets/{target_id} | Update target | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/targets/tgt-123` | Modify target |
| 161 | Delete Target | DELETE | /api/v2/scanning/targets/{target_id} | Delete target | `curl -X DELETE -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/targets/tgt-123` | Remove target |
| 162 | Target Scan History | GET | /api/v2/scanning/targets/{target_id}/history | Get target scan history | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/targets/tgt-123/history` | Scan history |
| 163 | List Policies | GET | /api/v2/scanning/policies | List scan policies | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/policies` | View policies |
| 164 | Get Policy | GET | /api/v2/scanning/policies/{policy_id} | Get policy details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/policies/pol-123` | Policy details |
| 165 | Create Policy | POST | /api/v2/scanning/policies | Create scan policy | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/policies` | New policy |
| 166 | Scan Trends | GET | /api/v2/scanning/metrics/trends | Get scan trends | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/metrics/trends` | Trend analysis |
| 167 | Export Results | GET | /api/v2/scanning/export | Export scan results | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/export` | Export data |
| 168 | Scan Stats | GET | /api/v2/scanning/stats | Get scan statistics | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/stats` | View stats |
| 169 | Recent Scans | GET | /api/v2/scanning/activity/recent | Get recent scans | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/activity/recent` | Activity log |
| 170 | Scan Report | GET | /api/v2/scanning/reports/{scan_id} | Generate scan report | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/scanning/reports/scan-123` | Report generation |

## Phase B4 - Alerts APIs (30)

| # | Name | Method | Endpoint | Description | Access Example | Use For |
|---|------|--------|----------|-------------|----------------|---------|
| 171 | List Alerts | GET | /api/v2/alerts/alerts | List all alerts | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/alerts` | View alerts |
| 172 | Create Alert | POST | /api/v2/alerts/alerts | Create new alert | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/alerts` | New alert |
| 173 | Get Alert | GET | /api/v2/alerts/alerts/{alert_id} | Get alert details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/alerts/alert-123` | Alert details |
| 174 | Update Alert | PUT | /api/v2/alerts/alerts/{alert_id} | Update alert | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/alerts/alert-123` | Modify alert |
| 175 | Acknowledge Alert | PUT | /api/v2/alerts/alerts/{alert_id}/acknowledge | Acknowledge alert | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/alerts/alert-123/acknowledge` | Acknowledge |
| 176 | Resolve Alert | PUT | /api/v2/alerts/alerts/{alert_id}/resolve | Resolve alert | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/alerts/alert-123/resolve` | Close alert |
| 177 | High Severity Alerts | GET | /api/v2/alerts/alerts/high-severity | Get high severity alerts | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/alerts/high-severity` | Critical alerts |
| 178 | Unacknowledged Alerts | GET | /api/v2/alerts/alerts/unacknowledged | Get unacknowledged alerts | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/alerts/unacknowledged` | New alerts |
| 179 | Alert Dashboard | GET | /api/v2/alerts/dashboard/summary | Get alert dashboard | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/dashboard/summary` | Dashboard view |
| 180 | Alert Trends | GET | /api/v2/alerts/dashboard/trends | Get alert trends | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/dashboard/trends` | Trend analysis |
| 181 | Alert by Severity | GET | /api/v2/alerts/dashboard/by-severity | Get alerts by severity | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/dashboard/by-severity` | Severity breakdown |
| 182 | Create Rule | POST | /api/v2/alerts/rules | Create alert rule | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/rules` | New rule |
| 183 | List Rules | GET | /api/v2/alerts/rules | List alert rules | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/rules` | View rules |
| 184 | Get Rule | GET | /api/v2/alerts/rules/{rule_id} | Get rule details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/rules/rule-123` | Rule details |
| 185 | Update Rule | PUT | /api/v2/alerts/rules/{rule_id} | Update rule | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/rules/rule-123` | Modify rule |
| 186 | Delete Rule | DELETE | /api/v2/alerts/rules/{rule_id} | Delete rule | `curl -X DELETE -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/rules/rule-123` | Remove rule |
| 187 | Enable Rule | PUT | /api/v2/alerts/rules/{rule_id}/enable | Enable rule | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/rules/rule-123/enable` | Activate rule |
| 188 | Disable Rule | PUT | /api/v2/alerts/rules/{rule_id}/disable | Disable rule | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/rules/rule-123/disable` | Deactivate rule |
| 189 | Create Channel | POST | /api/v2/alerts/channels | Create notification channel | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/channels` | New channel |
| 190 | List Channels | GET | /api/v2/alerts/channels | List notification channels | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/channels` | View channels |
| 191 | Get Channel | GET | /api/v2/alerts/channels/{channel_id} | Get channel details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/channels/chan-123` | Channel details |
| 192 | Update Channel | PUT | /api/v2/alerts/channels/{channel_id} | Update channel | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/channels/chan-123` | Modify channel |
| 193 | Delete Channel | DELETE | /api/v2/alerts/channels/{channel_id} | Delete channel | `curl -X DELETE -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/channels/chan-123` | Remove channel |
| 194 | Test Channel | POST | /api/v2/alerts/channels/{channel_id}/test | Test notification channel | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/channels/chan-123/test` | Test notifications |
| 195 | Alert Metrics | GET | /api/v2/alerts/metrics/summary | Get alert metrics | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/metrics/summary` | View metrics |
| 196 | MTTR Metrics | GET | /api/v2/alerts/metrics/mttr | Get MTTR metrics | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/metrics/mttr` | Response time |
| 197 | Export Alerts | GET | /api/v2/alerts/export | Export alert data | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/export` | Export data |
| 198 | Alert Stats | GET | /api/v2/alerts/stats | Get alert statistics | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/stats` | View stats |
| 199 | Recent Activity | GET | /api/v2/alerts/activity/recent | Get recent activity | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/activity/recent` | Activity log |
| 200 | Alert Report | GET | /api/v2/alerts/reports/summary | Generate alert report | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/alerts/reports/summary` | Report generation |

## Phase B4 - Compliance APIs (28)

| # | Name | Method | Endpoint | Description | Access Example | Use For |
|---|------|--------|----------|-------------|----------------|---------|
| 201 | List Frameworks | GET | /api/v2/compliance/frameworks | List compliance frameworks | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/frameworks` | View frameworks |
| 202 | Get Framework | GET | /api/v2/compliance/frameworks/{framework_id} | Get framework details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/frameworks/nerc-cip` | Framework details |
| 203 | Framework Controls | GET | /api/v2/compliance/frameworks/{framework_id}/controls | Get framework controls | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/frameworks/nerc-cip/controls` | View controls |
| 204 | Framework Coverage | GET | /api/v2/compliance/frameworks/{framework_id}/coverage | Get framework coverage | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/frameworks/nerc-cip/coverage` | Coverage status |
| 205 | List Controls | GET | /api/v2/compliance/controls | List all controls | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/controls` | View controls |
| 206 | Get Control | GET | /api/v2/compliance/controls/{control_id} | Get control details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/controls/cip-007` | Control details |
| 207 | Control Status | GET | /api/v2/compliance/controls/{control_id}/status | Get control compliance status | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/controls/cip-007/status` | Compliance status |
| 208 | Control Mapping | GET | /api/v2/compliance/controls/{control_id}/mappings | Get control mappings | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/controls/cip-007/mappings` | View mappings |
| 209 | Compliance Dashboard | GET | /api/v2/compliance/dashboard/summary | Get compliance dashboard | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/dashboard/summary` | Dashboard view |
| 210 | Compliance Score | GET | /api/v2/compliance/dashboard/score | Get compliance score | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/dashboard/score` | Overall score |
| 211 | Gaps Analysis | GET | /api/v2/compliance/dashboard/gaps | Get compliance gaps | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/dashboard/gaps` | View gaps |
| 212 | Create Assessment | POST | /api/v2/compliance/assessments | Create compliance assessment | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/assessments` | New assessment |
| 213 | List Assessments | GET | /api/v2/compliance/assessments | List assessments | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/assessments` | View assessments |
| 214 | Get Assessment | GET | /api/v2/compliance/assessments/{assessment_id} | Get assessment details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/assessments/assess-123` | Assessment details |
| 215 | Assessment Results | GET | /api/v2/compliance/assessments/{assessment_id}/results | Get assessment results | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/assessments/assess-123/results` | View results |
| 216 | Create Evidence | POST | /api/v2/compliance/evidence | Upload compliance evidence | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/evidence` | Upload evidence |
| 217 | List Evidence | GET | /api/v2/compliance/evidence | List evidence items | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/evidence` | View evidence |
| 218 | Get Evidence | GET | /api/v2/compliance/evidence/{evidence_id} | Get evidence details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/evidence/ev-123` | Evidence details |
| 219 | Map to Framework | POST | /api/v2/compliance/mappings | Map control to framework | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/mappings` | Create mapping |
| 220 | List Mappings | GET | /api/v2/compliance/mappings | List control mappings | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/mappings` | View mappings |
| 221 | Compliance Trends | GET | /api/v2/compliance/metrics/trends | Get compliance trends | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/metrics/trends` | Trend analysis |
| 222 | Control Effectiveness | GET | /api/v2/compliance/metrics/effectiveness | Get control effectiveness | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/metrics/effectiveness` | Effectiveness metrics |
| 223 | Export Compliance | GET | /api/v2/compliance/export | Export compliance data | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/export` | Export data |
| 224 | Compliance Report | GET | /api/v2/compliance/reports/summary | Generate compliance report | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/reports/summary` | Report generation |
| 225 | Audit Trail | GET | /api/v2/compliance/audit/trail | Get compliance audit trail | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/audit/trail` | Audit log |
| 226 | Compliance Stats | GET | /api/v2/compliance/stats | Get compliance statistics | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/stats` | View stats |
| 227 | Recent Activity | GET | /api/v2/compliance/activity/recent | Get recent activity | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/activity/recent` | Activity log |
| 228 | Framework Comparison | POST | /api/v2/compliance/analysis/compare | Compare frameworks | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/compliance/analysis/compare` | Compare standards |

## Phase B5 - Economic Impact APIs (27)

| # | Name | Method | Endpoint | Description | Access Example | Use For |
|---|------|--------|----------|-------------|----------------|---------|
| 229 | List Impacts | GET | /api/v2/economic/impacts | List economic impacts | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/impacts` | View impacts |
| 230 | Get Impact | GET | /api/v2/economic/impacts/{impact_id} | Get impact details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/impacts/imp-123` | Impact details |
| 231 | Calculate Impact | POST | /api/v2/economic/impacts/calculate | Calculate economic impact | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/impacts/calculate` | Impact calculation |
| 232 | Impact by Sector | GET | /api/v2/economic/impacts/by-sector | Get impact by sector | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/impacts/by-sector` | Sector analysis |
| 233 | Economic Dashboard | GET | /api/v2/economic/dashboard/summary | Get economic dashboard | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/dashboard/summary` | Dashboard view |
| 234 | Total Impact | GET | /api/v2/economic/dashboard/total-impact | Get total economic impact | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/dashboard/total-impact` | Total costs |
| 235 | Impact Trends | GET | /api/v2/economic/dashboard/trends | Get impact trends | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/dashboard/trends` | Trend analysis |
| 236 | Cost Analysis | GET | /api/v2/economic/analysis/cost | Analyze costs | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/analysis/cost` | Cost breakdown |
| 237 | ROI Analysis | POST | /api/v2/economic/analysis/roi | Calculate ROI | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/analysis/roi` | ROI calculation |
| 238 | Risk Cost | GET | /api/v2/economic/analysis/risk-cost | Analyze risk costs | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/analysis/risk-cost` | Risk costing |
| 239 | List Models | GET | /api/v2/economic/models | List economic models | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/models` | View models |
| 240 | Get Model | GET | /api/v2/economic/models/{model_id} | Get model details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/models/mod-123` | Model details |
| 241 | Create Model | POST | /api/v2/economic/models | Create economic model | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/models` | New model |
| 242 | Update Model | PUT | /api/v2/economic/models/{model_id} | Update model | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/models/mod-123` | Modify model |
| 243 | Budget Impact | GET | /api/v2/economic/budget/impact | Get budget impact | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/budget/impact` | Budget analysis |
| 244 | Budget Forecast | GET | /api/v2/economic/budget/forecast | Get budget forecast | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/budget/forecast` | Future costs |
| 245 | Cost Benchmarks | GET | /api/v2/economic/benchmarks/cost | Get cost benchmarks | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/benchmarks/cost` | Industry comparison |
| 246 | Industry Benchmarks | GET | /api/v2/economic/benchmarks/industry | Get industry benchmarks | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/benchmarks/industry` | Sector comparison |
| 247 | Impact Scenarios | POST | /api/v2/economic/scenarios | Create impact scenario | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/scenarios` | Scenario planning |
| 248 | List Scenarios | GET | /api/v2/economic/scenarios | List scenarios | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/scenarios` | View scenarios |
| 249 | Compare Scenarios | POST | /api/v2/economic/scenarios/compare | Compare scenarios | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/scenarios/compare` | Scenario comparison |
| 250 | Export Economic | GET | /api/v2/economic/export | Export economic data | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/export` | Export data |
| 251 | Economic Report | GET | /api/v2/economic/reports/summary | Generate economic report | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/reports/summary` | Report generation |
| 252 | Economic Stats | GET | /api/v2/economic/stats | Get economic statistics | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/stats` | View stats |
| 253 | Recent Activity | GET | /api/v2/economic/activity/recent | Get recent activity | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/activity/recent` | Activity log |
| 254 | Cost Allocation | GET | /api/v2/economic/allocation | Get cost allocation | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/allocation` | Cost distribution |
| 255 | Impact History | GET | /api/v2/economic/history | Get impact history | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/economic/history` | Historical data |

## Phase B5 - Demographics APIs (24)

| # | Name | Method | Endpoint | Description | Access Example | Use For |
|---|------|--------|----------|-------------|----------------|---------|
| 256 | List Summaries | GET | /api/v2/demographics/summaries | List demographic summaries | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/summaries` | View demographics |
| 257 | Get Summary | GET | /api/v2/demographics/summaries/{summary_id} | Get summary details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/summaries/sum-123` | Summary details |
| 258 | Create Summary | POST | /api/v2/demographics/summaries | Create demographic summary | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/summaries` | New summary |
| 259 | Update Summary | PUT | /api/v2/demographics/summaries/{summary_id} | Update summary | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/summaries/sum-123` | Modify summary |
| 260 | Demographics Dashboard | GET | /api/v2/demographics/dashboard/summary | Get demographics dashboard | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/dashboard/summary` | Dashboard view |
| 261 | Distribution Overview | GET | /api/v2/demographics/dashboard/distribution | Get distribution overview | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/dashboard/distribution` | Data distribution |
| 262 | By Sector | GET | /api/v2/demographics/analysis/by-sector | Analyze by sector | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/analysis/by-sector` | Sector breakdown |
| 263 | By Region | GET | /api/v2/demographics/analysis/by-region | Analyze by region | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/analysis/by-region` | Regional analysis |
| 264 | By Size | GET | /api/v2/demographics/analysis/by-size | Analyze by company size | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/analysis/by-size` | Size distribution |
| 265 | Risk Distribution | GET | /api/v2/demographics/analysis/risk-distribution | Analyze risk distribution | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/analysis/risk-distribution` | Risk by segment |
| 266 | List Segments | GET | /api/v2/demographics/segments | List customer segments | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/segments` | View segments |
| 267 | Get Segment | GET | /api/v2/demographics/segments/{segment_id} | Get segment details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/segments/seg-123` | Segment details |
| 268 | Create Segment | POST | /api/v2/demographics/segments | Create customer segment | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/segments` | New segment |
| 269 | Update Segment | PUT | /api/v2/demographics/segments/{segment_id} | Update segment | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/segments/seg-123` | Modify segment |
| 270 | Segment Analysis | GET | /api/v2/demographics/segments/{segment_id}/analysis | Analyze segment | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/segments/seg-123/analysis` | Segment insights |
| 271 | Demographic Trends | GET | /api/v2/demographics/trends | Get demographic trends | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/trends` | Trend analysis |
| 272 | Growth Analysis | GET | /api/v2/demographics/trends/growth | Analyze growth trends | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/trends/growth` | Growth patterns |
| 273 | Export Demographics | GET | /api/v2/demographics/export | Export demographic data | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/export` | Export data |
| 274 | Demographics Report | GET | /api/v2/demographics/reports/summary | Generate demographics report | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/reports/summary` | Report generation |
| 275 | Demographics Stats | GET | /api/v2/demographics/stats | Get demographics statistics | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/stats` | View stats |
| 276 | Recent Activity | GET | /api/v2/demographics/activity/recent | Get recent activity | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/activity/recent` | Activity log |
| 277 | Customer Profile | GET | /api/v2/demographics/profiles/{customer_id} | Get customer profile | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/profiles/cust-123` | Profile view |
| 278 | Profile Analysis | GET | /api/v2/demographics/profiles/{customer_id}/analysis | Analyze customer profile | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/profiles/cust-123/analysis` | Profile insights |
| 279 | Demographic Comparison | POST | /api/v2/demographics/compare | Compare demographics | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/demographics/compare` | Compare segments |

## Phase B5 - Prioritization APIs (28)

| # | Name | Method | Endpoint | Description | Access Example | Use For |
|---|------|--------|----------|-------------|----------------|---------|
| 280 | List Rankings | GET | /api/v2/prioritization/rankings | List priority rankings | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/rankings` | View rankings |
| 281 | Get Ranking | GET | /api/v2/prioritization/rankings/{ranking_id} | Get ranking details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/rankings/rank-123` | Ranking details |
| 282 | Calculate Priority | POST | /api/v2/prioritization/rankings/calculate | Calculate priority score | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/rankings/calculate` | Score calculation |
| 283 | Update Ranking | PUT | /api/v2/prioritization/rankings/{ranking_id} | Update ranking | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/rankings/rank-123` | Modify ranking |
| 284 | Prioritization Dashboard | GET | /api/v2/prioritization/dashboard/summary | Get prioritization dashboard | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/dashboard/summary` | Dashboard view |
| 285 | Top Priorities | GET | /api/v2/prioritization/dashboard/top-priorities | Get top priorities | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/dashboard/top-priorities` | Critical items |
| 286 | Priority Distribution | GET | /api/v2/prioritization/dashboard/distribution | Get priority distribution | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/dashboard/distribution` | Distribution view |
| 287 | By Risk | GET | /api/v2/prioritization/analysis/by-risk | Prioritize by risk | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/analysis/by-risk` | Risk-based priority |
| 288 | By Impact | GET | /api/v2/prioritization/analysis/by-impact | Prioritize by impact | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/analysis/by-impact` | Impact-based priority |
| 289 | By Cost | GET | /api/v2/prioritization/analysis/by-cost | Prioritize by cost | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/analysis/by-cost` | Cost-based priority |
| 290 | Risk-Impact Matrix | GET | /api/v2/prioritization/analysis/risk-impact-matrix | Get risk-impact matrix | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/analysis/risk-impact-matrix` | Matrix view |
| 291 | List Criteria | GET | /api/v2/prioritization/criteria | List priority criteria | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/criteria` | View criteria |
| 292 | Get Criterion | GET | /api/v2/prioritization/criteria/{criterion_id} | Get criterion details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/criteria/crit-123` | Criterion details |
| 293 | Create Criterion | POST | /api/v2/prioritization/criteria | Create priority criterion | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/criteria` | New criterion |
| 294 | Update Criterion | PUT | /api/v2/prioritization/criteria/{criterion_id} | Update criterion | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/criteria/crit-123` | Modify criterion |
| 295 | Criterion Weights | GET | /api/v2/prioritization/criteria/weights | Get criterion weights | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/criteria/weights` | View weights |
| 296 | List Models | GET | /api/v2/prioritization/models | List prioritization models | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/models` | View models |
| 297 | Get Model | GET | /api/v2/prioritization/models/{model_id} | Get model details | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/models/mod-123` | Model details |
| 298 | Create Model | POST | /api/v2/prioritization/models | Create prioritization model | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/models` | New model |
| 299 | Update Model | PUT | /api/v2/prioritization/models/{model_id} | Update model | `curl -X PUT -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/models/mod-123` | Modify model |
| 300 | Priority Scenarios | POST | /api/v2/prioritization/scenarios | Create priority scenario | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/scenarios` | Scenario planning |
| 301 | List Scenarios | GET | /api/v2/prioritization/scenarios | List scenarios | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/scenarios` | View scenarios |
| 302 | Compare Scenarios | POST | /api/v2/prioritization/scenarios/compare | Compare scenarios | `curl -X POST -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/scenarios/compare` | Scenario comparison |
| 303 | Export Priorities | GET | /api/v2/prioritization/export | Export prioritization data | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/export` | Export data |
| 304 | Priority Report | GET | /api/v2/prioritization/reports/summary | Generate priority report | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/reports/summary` | Report generation |
| 305 | Priority Stats | GET | /api/v2/prioritization/stats | Get prioritization statistics | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/stats` | View stats |
| 306 | Recent Activity | GET | /api/v2/prioritization/activity/recent | Get recent activity | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/activity/recent` | Activity log |
| 307 | Priority Trends | GET | /api/v2/prioritization/trends | Get priority trends | `curl -H "x-customer-id: dev" http://localhost:8000/api/v2/prioritization/trends` | Trend analysis |

---

# Next.js APIs (Port 3000)

## Next.js APIs (41)

**Auth Required**: Most Next.js APIs require Clerk authentication

| # | Name | Method | Endpoint | Description | Access Example | Use For |
|---|------|--------|----------|-------------|----------------|---------|
| 308 | Health Check | GET | /api/health | System health check (No auth) | `curl http://localhost:3000/api/health` | Health monitoring |
| 309 | Dashboard Metrics | GET | /api/dashboard/metrics | Get dashboard KPIs | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/dashboard/metrics` | Dashboard UI |
| 310 | Recent Activity | GET | /api/dashboard/activity | Get recent activity | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/dashboard/activity` | Activity feed |
| 311 | Data Distribution | GET | /api/dashboard/distribution | Get data distribution | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/dashboard/distribution` | Charts/graphs |
| 312 | Analytics Metrics | GET | /api/analytics/metrics | Get analytics KPIs | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/analytics/metrics` | Analytics UI |
| 313 | Time Series Data | GET | /api/analytics/timeseries | Get time series data | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/analytics/timeseries` | Time charts |
| 314 | CVE Trends | GET | /api/analytics/trends/cve | Get CVE trends | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/analytics/trends/cve` | CVE analytics |
| 315 | Threat Timeline | GET | /api/analytics/trends/threat-timeline | Get threat timeline | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/analytics/trends/threat-timeline` | Timeline view |
| 316 | Seasonality Patterns | GET | /api/analytics/trends/seasonality | Get seasonal patterns | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/analytics/trends/seasonality` | Pattern analysis |
| 317 | Export Analytics | GET | /api/analytics/export | Export analytics data | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/analytics/export` | Data export |
| 318 | Threat Analytics | GET | /api/threat-intel/analytics | Get threat analytics | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/threat-intel/analytics` | Threat overview |
| 319 | ICS Threats | GET | /api/threat-intel/ics | Get ICS threat data | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/threat-intel/ics` | Industrial threats |
| 320 | Threat Landscape | GET | /api/threat-intel/landscape | Get threat landscape | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/threat-intel/landscape` | Landscape view |
| 321 | Vulnerability Intel | GET | /api/threat-intel/vulnerabilities | Get vulnerability intelligence | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/threat-intel/vulnerabilities` | Vuln intelligence |
| 322 | Geographic Threats | GET | /api/threats/geographic | Get geographic threat data | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/threats/geographic` | Geographic view |
| 323 | ICS Threat Feed | GET | /api/threats/ics | Get ICS threat feed | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/threats/ics` | ICS monitoring |
| 324 | Graph Query | POST | /api/graph/query | Execute Cypher query | `curl -X POST -H "Authorization: Bearer TOKEN" http://localhost:3000/api/graph/query` | Custom queries |
| 325 | Neo4j Statistics | GET | /api/neo4j/statistics | Get database statistics | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/neo4j/statistics` | DB stats |
| 326 | Cyber Statistics | GET | /api/neo4j/cyber-statistics | Get cyber statistics | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/neo4j/cyber-statistics` | Cyber metrics |
| 327 | Submit Pipeline | POST | /api/pipeline/process | Submit document processing | `curl -X POST -H "Authorization: Bearer TOKEN" http://localhost:3000/api/pipeline/process` | Process docs |
| 328 | Pipeline Status | GET | /api/pipeline/status/[jobId] | Get processing status | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/pipeline/status/job-123` | Job tracking |
| 329 | List Queries | GET | /api/query-control/queries | List active queries | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/query-control/queries` | Query management |
| 330 | Query Details | GET | /api/query-control/queries/[queryId] | Get query details | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/query-control/queries/q-123` | Query info |
| 331 | Pause Query | POST | /api/query-control/queries/[queryId]/pause | Pause running query | `curl -X POST -H "Authorization: Bearer TOKEN" http://localhost:3000/api/query-control/queries/q-123/pause` | Pause execution |
| 332 | Resume Query | POST | /api/query-control/queries/[queryId]/resume | Resume paused query | `curl -X POST -H "Authorization: Bearer TOKEN" http://localhost:3000/api/query-control/queries/q-123/resume` | Resume execution |
| 333 | Query Checkpoints | GET | /api/query-control/queries/[queryId]/checkpoints | Get query checkpoints | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/query-control/queries/q-123/checkpoints` | Checkpoint status |
| 334 | Change Model | PUT | /api/query-control/queries/[queryId]/model | Change query model | `curl -X PUT -H "Authorization: Bearer TOKEN" http://localhost:3000/api/query-control/queries/q-123/model` | Switch model |
| 335 | Change Permissions | PUT | /api/query-control/queries/[queryId]/permissions | Change permissions | `curl -X PUT -H "Authorization: Bearer TOKEN" http://localhost:3000/api/query-control/queries/q-123/permissions` | Update permissions |
| 336 | List Customers | GET | /api/customers | List customers | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/customers` | Customer list |
| 337 | Get Customer | GET | /api/customers/[customerId] | Get customer details | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/customers/cust-123` | Customer info |
| 338 | Observability Metrics | GET | /api/observability/metrics | Get observability metrics | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/observability/metrics` | System metrics |
| 339 | Traces | GET | /api/observability/traces | Get trace data | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/observability/traces` | Trace analysis |
| 340 | Logs | GET | /api/observability/logs | Get log data | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/observability/logs` | Log analysis |
| 341 | List Tags | GET | /api/tags | List all tags | `curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/tags` | Tag management |
| 342 | Create Tag | POST | /api/tags | Create new tag | `curl -X POST -H "Authorization: Bearer TOKEN" http://localhost:3000/api/tags` | Add tag |
| 343 | Delete Tag | DELETE | /api/tags/[tagId] | Delete tag | `curl -X DELETE -H "Authorization: Bearer TOKEN" http://localhost:3000/api/tags/tag-123` | Remove tag |
| 344 | Utility Health | GET | /api/utilities/health | Utility health check | `curl http://localhost:3000/api/utilities/health` | Service status |
| 345 | Validation | POST | /api/utilities/validate | Validate data | `curl -X POST -H "Authorization: Bearer TOKEN" http://localhost:3000/api/utilities/validate` | Data validation |
| 346 | Transform Data | POST | /api/utilities/transform | Transform data format | `curl -X POST -H "Authorization: Bearer TOKEN" http://localhost:3000/api/utilities/transform` | Data transformation |
| 347 | Parse Input | POST | /api/utilities/parse | Parse input data | `curl -X POST -H "Authorization: Bearer TOKEN" http://localhost:3000/api/utilities/parse` | Data parsing |
| 348 | Test Connection | POST | /api/test/connection | Test database connection | `curl -X POST -H "Authorization: Bearer TOKEN" http://localhost:3000/api/test/connection` | Connectivity test |

---

## API SUMMARY BY CATEGORY

| Category | Port | APIs | Auth | Status |
|----------|------|------|------|--------|
| **NER11 APIs** | 8000 | 5 | ❌ No | ✅ Active |
| **Phase B2 - SBOM** | 8000 | 32 | ✅ Yes | ✅ Active |
| **Phase B2 - Vendor Equipment** | 8000 | 24 | ✅ Yes | ✅ Active |
| **Phase B3 - Threat Intel** | 8000 | 26 | ✅ Yes | ✅ Active |
| **Phase B3 - Risk Scoring** | 8000 | 24 | ✅ Yes | ✅ Active |
| **Phase B3 - Remediation** | 8000 | 29 | ✅ Yes | ✅ Active |
| **Phase B4 - Scanning** | 8000 | 30 | ✅ Yes | ✅ Active |
| **Phase B4 - Alerts** | 8000 | 30 | ✅ Yes | ✅ Active |
| **Phase B4 - Compliance** | 8000 | 28 | ✅ Yes | ✅ Active |
| **Phase B5 - Economic Impact** | 8000 | 27 | ✅ Yes | ✅ Active |
| **Phase B5 - Demographics** | 8000 | 24 | ✅ Yes | ✅ Active |
| **Phase B5 - Prioritization** | 8000 | 28 | ✅ Yes | ✅ Active |
| **Next.js Frontend** | 3000 | 41 | ✅ Yes | ✅ Active |
| **TOTAL** | - | **348** | - | - |

---

## AUTHENTICATION GUIDE

### Port 8000 APIs (NER + Phase B)

**NER APIs (5)**: No authentication required
```bash
curl http://localhost:8000/ner
```

**Phase B APIs (302)**: Require `x-customer-id` header
```bash
curl -H "x-customer-id: your-customer-id" http://localhost:8000/api/v2/...
```

### Port 3000 APIs (Next.js)

**Most APIs**: Require Clerk authentication token
```bash
curl -H "Authorization: Bearer YOUR_CLERK_TOKEN" http://localhost:3000/api/...
```

**No Auth Required**:
- `/api/health`
- `/api/utilities/health`

---

## QUICK START EXAMPLES

### Extract Entities (No Auth)
```bash
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text": "APT29 exploited CVE-2024-12345 targeting SCADA systems"}'
```

### Search Threats (No Auth)
```bash
curl -X POST http://localhost:8000/search/hybrid \
  -H "Content-Type: application/json" \
  -d '{"query": "ransomware", "expand_graph": true, "hop_depth": 2}'
```

### Get Risk Dashboard (With Auth)
```bash
curl -H "x-customer-id: dev" \
  http://localhost:8000/api/v2/risk/dashboard/summary
```

### List Compliance Frameworks (With Auth)
```bash
curl -H "x-customer-id: dev" \
  http://localhost:8000/api/v2/compliance/frameworks
```

---

## DOCUMENTATION REFERENCES

1. **Complete API Reference**: `/7_2025_DEC_11_Actual_System_Deployed/COMPLETE_API_REFERENCE_ALL_181.md`
2. **Frontend Quick Start**: `/7_2025_DEC_11_Actual_System_Deployed/docs/FRONTEND_QUICK_START_ACTUAL_APIS.md`
3. **NER API Guide**: `/7_2025_DEC_11_Actual_System_Deployed/docs/NER11_API_COMPLETE_GUIDE.md`
4. **API Architecture**: `/7_2025_DEC_11_Actual_System_Deployed/docs/API_ARCHITECTURE_DIAGRAMS.md`

---

**Last Updated**: 2025-12-12
**Status**: ✅ Production Ready
**Total Endpoints**: 348 (5 NER + 302 Phase B + 41 Next.js)
