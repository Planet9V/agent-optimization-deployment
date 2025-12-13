# Phase B3 - Threat, Risk & Remediation APIs

**Total Endpoints:** 81

**Base URL:** `http://localhost:8000`

---

## Table of Contents

1. [GET /api/v2/vendor-equipment/vendors/{vendor_id}/risk-summary](#get--api-v2-vendor-equipment-vendors-vendor_id-risk-summary): Get Vendor Risk Summary
2. [POST /api/v2/threat-intel/actors](#post--api-v2-threat-intel-actors): Create Threat Actor
3. [GET /api/v2/threat-intel/actors/{actor_id}](#get--api-v2-threat-intel-actors-actor_id): Get Threat Actor
4. [GET /api/v2/threat-intel/actors/search](#get--api-v2-threat-intel-actors-search): Search Threat Actors
5. [GET /api/v2/threat-intel/actors/active](#get--api-v2-threat-intel-actors-active): Get Active Threat Actors
6. [GET /api/v2/threat-intel/actors/by-sector/{sector}](#get--api-v2-threat-intel-actors-by-sector-sector): Get Actors By Sector
7. [GET /api/v2/threat-intel/actors/{actor_id}/campaigns](#get--api-v2-threat-intel-actors-actor_id-campaigns): Get Actor Campaigns
8. [GET /api/v2/threat-intel/actors/{actor_id}/cves](#get--api-v2-threat-intel-actors-actor_id-cves): Get Actor Cves
9. [POST /api/v2/threat-intel/campaigns](#post--api-v2-threat-intel-campaigns): Create Campaign
10. [GET /api/v2/threat-intel/campaigns/{campaign_id}](#get--api-v2-threat-intel-campaigns-campaign_id): Get Campaign
11. [GET /api/v2/threat-intel/campaigns/search](#get--api-v2-threat-intel-campaigns-search): Search Campaigns
12. [GET /api/v2/threat-intel/campaigns/active](#get--api-v2-threat-intel-campaigns-active): Get Active Campaigns
13. [GET /api/v2/threat-intel/campaigns/{campaign_id}/iocs](#get--api-v2-threat-intel-campaigns-campaign_id-iocs): Get Campaign Iocs
14. [POST /api/v2/threat-intel/mitre/mappings](#post--api-v2-threat-intel-mitre-mappings): Create Mitre Mapping
15. [GET /api/v2/threat-intel/mitre/mappings/entity/{entity_type}/{entity_id}](#get--api-v2-threat-intel-mitre-mappings-entity-entity_type-entity_id): Get Entity Mitre Mappings
16. [GET /api/v2/threat-intel/mitre/techniques/{technique_id}/actors](#get--api-v2-threat-intel-mitre-techniques-technique_id-actors): Get Actors Using Technique
17. [GET /api/v2/threat-intel/mitre/coverage](#get--api-v2-threat-intel-mitre-coverage): Get Mitre Coverage
18. [GET /api/v2/threat-intel/mitre/gaps](#get--api-v2-threat-intel-mitre-gaps): Get Mitre Gaps
19. [POST /api/v2/threat-intel/iocs](#post--api-v2-threat-intel-iocs): Create Ioc
20. [POST /api/v2/threat-intel/iocs/bulk](#post--api-v2-threat-intel-iocs-bulk): Bulk Import Iocs
21. [GET /api/v2/threat-intel/iocs/search](#get--api-v2-threat-intel-iocs-search): Search Iocs
22. [GET /api/v2/threat-intel/iocs/active](#get--api-v2-threat-intel-iocs-active): Get Active Iocs
23. [GET /api/v2/threat-intel/iocs/by-type/{ioc_type}](#get--api-v2-threat-intel-iocs-by-type-ioc_type): Get Iocs By Type
24. [POST /api/v2/threat-intel/feeds](#post--api-v2-threat-intel-feeds): Create Threat Feed
25. [GET /api/v2/threat-intel/feeds](#get--api-v2-threat-intel-feeds): List Threat Feeds
26. [PUT /api/v2/threat-intel/feeds/{feed_id}/refresh](#put--api-v2-threat-intel-feeds-feed_id-refresh): Trigger Feed Refresh
27. [GET /api/v2/threat-intel/dashboard/summary](#get--api-v2-threat-intel-dashboard-summary): Get Threat Intel Summary
28. [POST /api/v2/risk/scores](#post--api-v2-risk-scores): Calculate Risk Score
29. [GET /api/v2/risk/scores/{entity_type}/{entity_id}](#get--api-v2-risk-scores-entity_type-entity_id): Get Risk Score
30. [GET /api/v2/risk/scores/high-risk](#get--api-v2-risk-scores-high-risk): Get High Risk Entities
31. [GET /api/v2/risk/scores/trending](#get--api-v2-risk-scores-trending): Get Trending Entities
32. [GET /api/v2/risk/scores/search](#get--api-v2-risk-scores-search): Search Risk Scores
33. [POST /api/v2/risk/scores/recalculate/{entity_type}/{entity_id}](#post--api-v2-risk-scores-recalculate-entity_type-entity_id): Recalculate Risk Score
34. [GET /api/v2/risk/scores/history/{entity_type}/{entity_id}](#get--api-v2-risk-scores-history-entity_type-entity_id): Get Risk History
35. [POST /api/v2/risk/assets/criticality](#post--api-v2-risk-assets-criticality): Set Asset Criticality
36. [GET /api/v2/risk/assets/{asset_id}/criticality](#get--api-v2-risk-assets-asset_id-criticality): Get Asset Criticality
37. [PUT /api/v2/risk/assets/{asset_id}/criticality](#put--api-v2-risk-assets-asset_id-criticality): Update Asset Criticality
38. [GET /api/v2/risk/assets/mission-critical](#get--api-v2-risk-assets-mission-critical): Get Mission Critical Assets
39. [GET /api/v2/risk/assets/by-criticality/{level}](#get--api-v2-risk-assets-by-criticality-level): Get Assets By Criticality
40. [GET /api/v2/risk/assets/criticality/summary](#get--api-v2-risk-assets-criticality-summary): Get Criticality Summary
41. [POST /api/v2/risk/exposure](#post--api-v2-risk-exposure): Calculate Exposure Score
42. [GET /api/v2/risk/exposure/{asset_id}](#get--api-v2-risk-exposure-asset_id): Get Exposure Score
43. [GET /api/v2/risk/exposure/internet-facing](#get--api-v2-risk-exposure-internet-facing): Get Internet Facing Assets
44. [GET /api/v2/risk/exposure/high-exposure](#get--api-v2-risk-exposure-high-exposure): Get High Exposure Assets
45. [GET /api/v2/risk/exposure/attack-surface](#get--api-v2-risk-exposure-attack-surface): Get Attack Surface Summary
46. [GET /api/v2/risk/aggregation/by-vendor](#get--api-v2-risk-aggregation-by-vendor): Get Risk By Vendor
47. [GET /api/v2/risk/aggregation/by-sector](#get--api-v2-risk-aggregation-by-sector): Get Risk By Sector
48. [GET /api/v2/risk/aggregation/by-asset-type](#get--api-v2-risk-aggregation-by-asset-type): Get Risk By Asset Type
49. [GET /api/v2/risk/aggregation/{aggregation_type}/{group_id}](#get--api-v2-risk-aggregation-aggregation_type-group_id): Get Risk Aggregation
50. [GET /api/v2/risk/dashboard/summary](#get--api-v2-risk-dashboard-summary): Get Dashboard Summary
51. [GET /api/v2/risk/dashboard/risk-matrix](#get--api-v2-risk-dashboard-risk-matrix): Get Risk Matrix
52. [POST /api/v2/remediation/tasks](#post--api-v2-remediation-tasks): Create Task
53. [GET /api/v2/remediation/tasks/{task_id}](#get--api-v2-remediation-tasks-task_id): Get Task
54. [GET /api/v2/remediation/tasks/search](#get--api-v2-remediation-tasks-search): Search Tasks
55. [GET /api/v2/remediation/tasks/open](#get--api-v2-remediation-tasks-open): Get Open Tasks
56. [GET /api/v2/remediation/tasks/overdue](#get--api-v2-remediation-tasks-overdue): Get Overdue Tasks
57. [GET /api/v2/remediation/tasks/by-priority/{priority}](#get--api-v2-remediation-tasks-by-priority-priority): Get Tasks By Priority
58. [GET /api/v2/remediation/tasks/by-status/{status}](#get--api-v2-remediation-tasks-by-status-status): Get Tasks By Status
59. [PUT /api/v2/remediation/tasks/{task_id}/status](#put--api-v2-remediation-tasks-task_id-status): Update Task Status
60. [PUT /api/v2/remediation/tasks/{task_id}/assign](#put--api-v2-remediation-tasks-task_id-assign): Assign Task
61. [GET /api/v2/remediation/tasks/{task_id}/history](#get--api-v2-remediation-tasks-task_id-history): Get Task History
62. [POST /api/v2/remediation/plans](#post--api-v2-remediation-plans): Create Plan
63. [GET /api/v2/remediation/plans](#get--api-v2-remediation-plans): List Plans
64. [GET /api/v2/remediation/plans/{plan_id}](#get--api-v2-remediation-plans-plan_id): Get Plan
65. [GET /api/v2/remediation/plans/active](#get--api-v2-remediation-plans-active): Get Active Plans
66. [PUT /api/v2/remediation/plans/{plan_id}/status](#put--api-v2-remediation-plans-plan_id-status): Update Plan Status
67. [GET /api/v2/remediation/plans/{plan_id}/progress](#get--api-v2-remediation-plans-plan_id-progress): Get Plan Progress
68. [POST /api/v2/remediation/sla/policies](#post--api-v2-remediation-sla-policies): Create Sla Policy
69. [GET /api/v2/remediation/sla/policies](#get--api-v2-remediation-sla-policies): List Sla Policies
70. [GET /api/v2/remediation/sla/policies/{policy_id}](#get--api-v2-remediation-sla-policies-policy_id): Get Sla Policy
71. [PUT /api/v2/remediation/sla/policies/{policy_id}](#put--api-v2-remediation-sla-policies-policy_id): Update Sla Policy
72. [GET /api/v2/remediation/sla/breaches](#get--api-v2-remediation-sla-breaches): Get Sla Breaches
73. [GET /api/v2/remediation/sla/at-risk](#get--api-v2-remediation-sla-at-risk): Get At Risk Tasks
74. [GET /api/v2/remediation/metrics/summary](#get--api-v2-remediation-metrics-summary): Get Metrics Summary
75. [GET /api/v2/remediation/metrics/mttr](#get--api-v2-remediation-metrics-mttr): Get Mttr By Severity
76. [GET /api/v2/remediation/metrics/sla-compliance](#get--api-v2-remediation-metrics-sla-compliance): Get Sla Compliance
77. [GET /api/v2/remediation/metrics/backlog](#get--api-v2-remediation-metrics-backlog): Get Backlog Metrics
78. [GET /api/v2/remediation/metrics/trends](#get--api-v2-remediation-metrics-trends): Get Remediation Trends
79. [GET /api/v2/remediation/dashboard/summary](#get--api-v2-remediation-dashboard-summary): Get Dashboard Summary
80. [GET /api/v2/remediation/dashboard/workload](#get--api-v2-remediation-dashboard-workload): Get Workload Distribution
81. [GET /api/v2/economic-impact/value/risk-adjusted](#get--api-v2-economic-impact-value-risk-adjusted): Get Risk Adjusted Value

---

# Endpoint Details


## GET /api/v2/vendor-equipment/vendors/{vendor_id}/risk-summary

**Summary:** Get Vendor Risk Summary

**Operation ID:** `get_vendor_risk_summary_api_v2_vendor_equipment_vendors__vendor_id__risk_summary_get`

**Description:**
Get comprehensive risk summary for a vendor.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `vendor_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "vendor_id": "<vendor_id>",
  "vendor_name": "<vendor_name>",
  "total_equipment": 1,
  "total_cves": 1,
  "critical_cves": 1,
  "equipment_at_eol": 1,
  "equipment_approaching_eol": 1,
  "risk_level": "<risk_level>"
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/vendors/{vendor_id}/risk-summary" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/threat-intel/actors

**Summary:** Create Threat Actor

**Operation ID:** `create_threat_actor_api_v2_threat_intel_actors_post`

**Description:**
Create a new threat actor.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "actor_id": "<actor_id>",
  "name": "<name>",
  "aliases": [],
  "actor_type": "<actor_type>",
  "motivation": [],
  "sophistication": "<sophistication>",
  "target_sectors": [],
  "target_regions": []
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "actor_id": "<actor_id>",
  "name": "<name>",
  "customer_id": "<customer_id>",
  "aliases": [],
  "actor_type": "<actor_type>",
  "motivation": [],
  "sophistication": "<sophistication>",
  "target_sectors": [],
  "target_regions": [],
  "is_active": true,
  "campaign_count": 1,
  "cve_count": 1,
  "ioc_count": 1
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X POST "http://localhost:8000/api/v2/threat-intel/actors" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "actor_id": "<actor_id>",
  "name": "<name>",
  "aliases": [],
  "actor_type": "<actor_type>",
  "motivation": [],
  "sophistication": "<sophistication>",
  "target_sectors": [],
  "target_regions": []
}' 
```

---

## GET /api/v2/threat-intel/actors/{actor_id}

**Summary:** Get Threat Actor

**Operation ID:** `get_threat_actor_api_v2_threat_intel_actors__actor_id__get`

**Description:**
Get threat actor by ID with customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `actor_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "actor_id": "<actor_id>",
  "name": "<name>",
  "customer_id": "<customer_id>",
  "aliases": [],
  "actor_type": "<actor_type>",
  "motivation": [],
  "sophistication": "<sophistication>",
  "target_sectors": [],
  "target_regions": [],
  "is_active": true,
  "campaign_count": 1,
  "cve_count": 1,
  "ioc_count": 1
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/actors/{actor_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/actors/search

**Summary:** Search Threat Actors

**Operation ID:** `search_threat_actors_api_v2_threat_intel_actors_search_get`

**Description:**
Search threat actors with semantic search and filters.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `query` | string/null | ⬜ No | query | Semantic search query |
| `actor_type` | string/null | ⬜ No | query | Filter by actor type |
| `country` | string/null | ⬜ No | query | Filter by country |
| `target_sector` | string/null | ⬜ No | query | Filter by target sector |
| `is_active` | boolean/null | ⬜ No | query | Filter by active status |
| `limit` | integer | ⬜ No | query | Maximum results |
| `include_system` | boolean | ⬜ No | query | Include SYSTEM actors |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "results": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/actors/search" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/actors/active

**Summary:** Get Active Threat Actors

**Operation ID:** `get_active_threat_actors_api_v2_threat_intel_actors_active_get`

**Description:**
Get all currently active threat actors.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "results": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/actors/active" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/actors/by-sector/{sector}

**Summary:** Get Actors By Sector

**Operation ID:** `get_actors_by_sector_api_v2_threat_intel_actors_by_sector__sector__get`

**Description:**
Get threat actors targeting a specific sector.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sector` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "results": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/actors/by-sector/{sector}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/actors/{actor_id}/campaigns

**Summary:** Get Actor Campaigns

**Operation ID:** `get_actor_campaigns_api_v2_threat_intel_actors__actor_id__campaigns_get`

**Description:**
Get campaigns associated with a threat actor.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `actor_id` | string | ✅ Yes | path |  |
| `limit` | integer | ⬜ No | query | Maximum results |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/actors/{actor_id}/campaigns" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/actors/{actor_id}/cves

**Summary:** Get Actor Cves

**Operation ID:** `get_actor_cves_api_v2_threat_intel_actors__actor_id__cves_get`

**Description:**
Get CVEs associated with a threat actor.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `actor_id` | string | ✅ Yes | path |  |
| `limit` | integer | ⬜ No | query | Maximum results |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/actors/{actor_id}/cves" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/threat-intel/campaigns

**Summary:** Create Campaign

**Operation ID:** `create_campaign_api_v2_threat_intel_campaigns_post`

**Description:**
Create a new campaign.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "campaign_id": "<campaign_id>",
  "name": "<name>",
  "threat_actor_ids": [],
  "target_sectors": [],
  "target_regions": [],
  "ttps": []
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "campaign_id": "<campaign_id>",
  "name": "<name>",
  "customer_id": "<customer_id>",
  "threat_actor_ids": [],
  "target_sectors": [],
  "target_regions": [],
  "is_active": true,
  "ioc_count": 1,
  "cve_count": 1
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X POST "http://localhost:8000/api/v2/threat-intel/campaigns" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "campaign_id": "<campaign_id>",
  "name": "<name>",
  "threat_actor_ids": [],
  "target_sectors": [],
  "target_regions": [],
  "ttps": []
}' 
```

---

## GET /api/v2/threat-intel/campaigns/{campaign_id}

**Summary:** Get Campaign

**Operation ID:** `get_campaign_api_v2_threat_intel_campaigns__campaign_id__get`

**Description:**
Get campaign by ID with customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `campaign_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "campaign_id": "<campaign_id>",
  "name": "<name>",
  "customer_id": "<customer_id>",
  "threat_actor_ids": [],
  "target_sectors": [],
  "target_regions": [],
  "is_active": true,
  "ioc_count": 1,
  "cve_count": 1
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/campaigns/{campaign_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/campaigns/search

**Summary:** Search Campaigns

**Operation ID:** `search_campaigns_api_v2_threat_intel_campaigns_search_get`

**Description:**
Search campaigns with semantic search and filters.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `query` | string/null | ⬜ No | query | Semantic search query |
| `threat_actor_id` | string/null | ⬜ No | query | Filter by threat actor |
| `target_sector` | string/null | ⬜ No | query | Filter by target sector |
| `is_active` | boolean/null | ⬜ No | query | Filter by active status |
| `limit` | integer | ⬜ No | query | Maximum results |
| `include_system` | boolean | ⬜ No | query | Include SYSTEM campaigns |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "results": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/campaigns/search" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/campaigns/active

**Summary:** Get Active Campaigns

**Operation ID:** `get_active_campaigns_api_v2_threat_intel_campaigns_active_get`

**Description:**
Get all currently active campaigns.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "results": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/campaigns/active" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/campaigns/{campaign_id}/iocs

**Summary:** Get Campaign Iocs

**Operation ID:** `get_campaign_iocs_api_v2_threat_intel_campaigns__campaign_id__iocs_get`

**Description:**
Get IOCs associated with a campaign.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `campaign_id` | string | ✅ Yes | path |  |
| `limit` | integer | ⬜ No | query | Maximum results |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/campaigns/{campaign_id}/iocs" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/threat-intel/mitre/mappings

**Summary:** Create Mitre Mapping

**Operation ID:** `create_mitre_mapping_api_v2_threat_intel_mitre_mappings_post`

**Description:**
Create a new MITRE ATT&CK mapping.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "mapping_id": "<mapping_id>",
  "technique_id": "<technique_id>",
  "technique_name": "<technique_name>",
  "tactic": "<tactic>",
  "entity_type": "<entity_type>",
  "entity_id": "<entity_id>"
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "mapping_id": "<mapping_id>",
  "customer_id": "<customer_id>",
  "technique_id": "<technique_id>",
  "technique_name": "<technique_name>",
  "tactic": "<tactic>",
  "entity_type": "<entity_type>",
  "entity_id": "<entity_id>"
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X POST "http://localhost:8000/api/v2/threat-intel/mitre/mappings" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "mapping_id": "<mapping_id>",
  "technique_id": "<technique_id>",
  "technique_name": "<technique_name>",
  "tactic": "<tactic>",
  "entity_type": "<entity_type>",
  "entity_id": "<entity_id>"
}' 
```

---

## GET /api/v2/threat-intel/mitre/mappings/entity/{entity_type}/{entity_id}

**Summary:** Get Entity Mitre Mappings

**Operation ID:** `get_entity_mitre_mappings_api_v2_threat_intel_mitre_mappings_entity__entity_type___entity_id__get`

**Description:**
Get MITRE ATT&CK mappings for an entity.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `entity_type` | string | ✅ Yes | path |  |
| `entity_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "results": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/mitre/mappings/entity/{entity_type}/{entity_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/mitre/techniques/{technique_id}/actors

**Summary:** Get Actors Using Technique

**Operation ID:** `get_actors_using_technique_api_v2_threat_intel_mitre_techniques__technique_id__actors_get`

**Description:**
Get threat actors using a specific MITRE ATT&CK technique.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `technique_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/mitre/techniques/{technique_id}/actors" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/mitre/coverage

**Summary:** Get Mitre Coverage

**Operation ID:** `get_mitre_coverage_api_v2_threat_intel_mitre_coverage_get`

**Description:**
Get MITRE ATT&CK coverage summary.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "customer_id": "<customer_id>",
  "total_techniques": 1,
  "covered_techniques": 1,
  "top_techniques": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/mitre/coverage" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/mitre/gaps

**Summary:** Get Mitre Gaps

**Operation ID:** `get_mitre_gaps_api_v2_threat_intel_mitre_gaps_get`

**Description:**
Get MITRE ATT&CK coverage gaps.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "customer_id": "<customer_id>",
  "uncovered_techniques": 1,
  "critical_gaps": [],
  "recommendations": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/mitre/gaps" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/threat-intel/iocs

**Summary:** Create Ioc

**Operation ID:** `create_ioc_api_v2_threat_intel_iocs_post`

**Description:**
Create a new IOC.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "ioc_id": "<ioc_id>",
  "ioc_type": "<ioc_type>",
  "value": "<value>",
  "confidence": 1,
  "tags": []
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "ioc_id": "<ioc_id>",
  "customer_id": "<customer_id>",
  "ioc_type": "<ioc_type>",
  "value": "<value>",
  "confidence": 1,
  "is_active": true,
  "tags": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X POST "http://localhost:8000/api/v2/threat-intel/iocs" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "ioc_id": "<ioc_id>",
  "ioc_type": "<ioc_type>",
  "value": "<value>",
  "confidence": 1,
  "tags": []
}' 
```

---

## POST /api/v2/threat-intel/iocs/bulk

**Summary:** Bulk Import Iocs

**Operation ID:** `bulk_import_iocs_api_v2_threat_intel_iocs_bulk_post`

**Description:**
Bulk import IOCs.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "iocs": []
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "imported_count": 1,
  "failed_count": 1,
  "failed_iocs": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X POST "http://localhost:8000/api/v2/threat-intel/iocs/bulk" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "iocs": []
}' 
```

---

## GET /api/v2/threat-intel/iocs/search

**Summary:** Search Iocs

**Operation ID:** `search_iocs_api_v2_threat_intel_iocs_search_get`

**Description:**
Search IOCs with semantic search and filters.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `query` | string/null | ⬜ No | query | Semantic search query |
| `ioc_type` | string/null | ⬜ No | query | Filter by IOC type |
| `threat_actor_id` | string/null | ⬜ No | query | Filter by threat actor |
| `campaign_id` | string/null | ⬜ No | query | Filter by campaign |
| `min_confidence` | integer/null | ⬜ No | query | Minimum confidence |
| `is_active` | boolean/null | ⬜ No | query | Filter by active status |
| `limit` | integer | ⬜ No | query | Maximum results |
| `include_system` | boolean | ⬜ No | query | Include SYSTEM IOCs |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "results": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/iocs/search" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/iocs/active

**Summary:** Get Active Iocs

**Operation ID:** `get_active_iocs_api_v2_threat_intel_iocs_active_get`

**Description:**
Get all currently active IOCs.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "results": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/iocs/active" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/iocs/by-type/{ioc_type}

**Summary:** Get Iocs By Type

**Operation ID:** `get_iocs_by_type_api_v2_threat_intel_iocs_by_type__ioc_type__get`

**Description:**
Get IOCs by type.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `ioc_type` | string | ✅ Yes | path |  |
| `limit` | integer | ⬜ No | query | Maximum results |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "results": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/iocs/by-type/{ioc_type}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/threat-intel/feeds

**Summary:** Create Threat Feed

**Operation ID:** `create_threat_feed_api_v2_threat_intel_feeds_post`

**Description:**
Create a new threat feed.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "feed_id": "<feed_id>",
  "name": "<name>",
  "feed_url": "<feed_url>",
  "feed_type": "<feed_type>",
  "refresh_interval": 1,
  "enabled": true
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "feed_id": "<feed_id>",
  "name": "<name>",
  "customer_id": "<customer_id>",
  "feed_url": "<feed_url>",
  "feed_type": "<feed_type>",
  "refresh_interval": 1,
  "enabled": true
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X POST "http://localhost:8000/api/v2/threat-intel/feeds" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "feed_id": "<feed_id>",
  "name": "<name>",
  "feed_url": "<feed_url>",
  "feed_type": "<feed_type>",
  "refresh_interval": 1,
  "enabled": true
}' 
```

---

## GET /api/v2/threat-intel/feeds

**Summary:** List Threat Feeds

**Operation ID:** `list_threat_feeds_api_v2_threat_intel_feeds_get`

**Description:**
List threat feeds.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `limit` | integer | ⬜ No | query | Maximum results |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "feeds": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/feeds" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## PUT /api/v2/threat-intel/feeds/{feed_id}/refresh

**Summary:** Trigger Feed Refresh

**Operation ID:** `trigger_feed_refresh_api_v2_threat_intel_feeds__feed_id__refresh_put`

**Description:**
Trigger threat feed refresh.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `feed_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X PUT "http://localhost:8000/api/v2/threat-intel/feeds/{feed_id}/refresh" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/threat-intel/dashboard/summary

**Summary:** Get Threat Intel Summary

**Operation ID:** `get_threat_intel_summary_api_v2_threat_intel_dashboard_summary_get`

**Description:**
Get threat intelligence dashboard summary.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "customer_id": "<customer_id>",
  "total_threat_actors": 1,
  "active_campaigns": 1,
  "total_iocs": 1,
  "active_iocs": 1,
  "total_cves": 1,
  "high_confidence_iocs": 1,
  "recent_activity_count": 1
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/dashboard/summary" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/risk/scores

**Summary:** Calculate Risk Score

**Operation ID:** `calculate_risk_score_api_v2_risk_scores_post`

**Description:**
Calculate and store risk score for an entity.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "entity_type": "<entity_type>",
  "entity_id": "<entity_id>",
  "entity_name": "<entity_name>",
  "factors": []
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "risk_id": "<risk_id>",
  "entity_type": "<entity_type>",
  "entity_id": "<entity_id>",
  "entity_name": "<entity_name>",
  "customer_id": "<customer_id>",
  "risk_level": "<risk_level>",
  "factors": [],
  "calculated_at": "<calculated_at>"
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X POST "http://localhost:8000/api/v2/risk/scores" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "entity_type": "<entity_type>",
  "entity_id": "<entity_id>",
  "entity_name": "<entity_name>",
  "factors": []
}' 
```

---

## GET /api/v2/risk/scores/{entity_type}/{entity_id}

**Summary:** Get Risk Score

**Operation ID:** `get_risk_score_api_v2_risk_scores__entity_type___entity_id__get`

**Description:**
Get most recent risk score for entity with customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `entity_type` | string | ✅ Yes | path |  |
| `entity_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "risk_id": "<risk_id>",
  "entity_type": "<entity_type>",
  "entity_id": "<entity_id>",
  "entity_name": "<entity_name>",
  "customer_id": "<customer_id>",
  "risk_level": "<risk_level>",
  "factors": [],
  "calculated_at": "<calculated_at>"
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/scores/{entity_type}/{entity_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/scores/high-risk

**Summary:** Get High Risk Entities

**Operation ID:** `get_high_risk_entities_api_v2_risk_scores_high_risk_get`

**Description:**
Get all entities with high or critical risk scores.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `min_score` | number | ⬜ No | query | Minimum risk score threshold |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "results": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/scores/high-risk" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/scores/trending

**Summary:** Get Trending Entities

**Operation ID:** `get_trending_entities_api_v2_risk_scores_trending_get`

**Description:**
Get entities with specific risk trend.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `trend` | string | ⬜ No | query | Risk trend: increasing, decreasing, stable |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "results": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/scores/trending" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/scores/search

**Summary:** Search Risk Scores

**Operation ID:** `search_risk_scores_api_v2_risk_scores_search_get`

**Description:**
Search risk scores with filters and customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `query` | string/null | ⬜ No | query | Search query |
| `entity_type` | string/null | ⬜ No | query | Filter by entity type |
| `risk_level` | string/null | ⬜ No | query | Filter by risk level |
| `min_risk_score` | number/null | ⬜ No | query |  |
| `max_risk_score` | number/null | ⬜ No | query |  |
| `trend` | string/null | ⬜ No | query | Filter by trend |
| `limit` | integer | ⬜ No | query | Maximum results |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "results": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/scores/search" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/risk/scores/recalculate/{entity_type}/{entity_id}

**Summary:** Recalculate Risk Score

**Operation ID:** `recalculate_risk_score_api_v2_risk_scores_recalculate__entity_type___entity_id__post`

**Description:**
Force recalculation of risk score using existing factors.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `entity_type` | string | ✅ Yes | path |  |
| `entity_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "risk_id": "<risk_id>",
  "entity_type": "<entity_type>",
  "entity_id": "<entity_id>",
  "entity_name": "<entity_name>",
  "customer_id": "<customer_id>",
  "risk_level": "<risk_level>",
  "factors": [],
  "calculated_at": "<calculated_at>"
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X POST "http://localhost:8000/api/v2/risk/scores/recalculate/{entity_type}/{entity_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/scores/history/{entity_type}/{entity_id}

**Summary:** Get Risk History

**Operation ID:** `get_risk_history_api_v2_risk_scores_history__entity_type___entity_id__get`

**Description:**
Get risk score history for entity.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `entity_type` | string | ✅ Yes | path |  |
| `entity_id` | string | ✅ Yes | path |  |
| `days` | integer | ⬜ No | query | Days of history |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "results": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/scores/history/{entity_type}/{entity_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/risk/assets/criticality

**Summary:** Set Asset Criticality

**Operation ID:** `set_asset_criticality_api_v2_risk_assets_criticality_post`

**Description:**
Set asset criticality rating.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "asset_id": "<asset_id>",
  "asset_name": "<asset_name>",
  "criticality_level": "<criticality_level>"
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "asset_id": "<asset_id>",
  "asset_name": "<asset_name>",
  "customer_id": "<customer_id>",
  "criticality_level": "<criticality_level>"
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X POST "http://localhost:8000/api/v2/risk/assets/criticality" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "asset_id": "<asset_id>",
  "asset_name": "<asset_name>",
  "criticality_level": "<criticality_level>"
}' 
```

---

## GET /api/v2/risk/assets/{asset_id}/criticality

**Summary:** Get Asset Criticality

**Operation ID:** `get_asset_criticality_api_v2_risk_assets__asset_id__criticality_get`

**Description:**
Get asset criticality rating with customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `asset_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "asset_id": "<asset_id>",
  "asset_name": "<asset_name>",
  "customer_id": "<customer_id>",
  "criticality_level": "<criticality_level>"
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/assets/{asset_id}/criticality" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## PUT /api/v2/risk/assets/{asset_id}/criticality

**Summary:** Update Asset Criticality

**Operation ID:** `update_asset_criticality_api_v2_risk_assets__asset_id__criticality_put`

**Description:**
Update asset criticality rating.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `asset_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "asset_id": "<asset_id>",
  "asset_name": "<asset_name>",
  "criticality_level": "<criticality_level>"
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "asset_id": "<asset_id>",
  "asset_name": "<asset_name>",
  "customer_id": "<customer_id>",
  "criticality_level": "<criticality_level>"
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X PUT "http://localhost:8000/api/v2/risk/assets/{asset_id}/criticality" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "asset_id": "<asset_id>",
  "asset_name": "<asset_name>",
  "criticality_level": "<criticality_level>"
}' 
```

---

## GET /api/v2/risk/assets/mission-critical

**Summary:** Get Mission Critical Assets

**Operation ID:** `get_mission_critical_assets_api_v2_risk_assets_mission_critical_get`

**Description:**
Get all mission-critical assets.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "assets": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/assets/mission-critical" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/assets/by-criticality/{level}

**Summary:** Get Assets By Criticality

**Operation ID:** `get_assets_by_criticality_api_v2_risk_assets_by_criticality__level__get`

**Description:**
Get assets by criticality level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `level` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "assets": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/assets/by-criticality/{level}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/assets/criticality/summary

**Summary:** Get Criticality Summary

**Operation ID:** `get_criticality_summary_api_v2_risk_assets_criticality_summary_get`

**Description:**
Get criticality distribution summary.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "customer_id": "<customer_id>",
  "mission_critical": 1,
  "high": 1,
  "medium": 1,
  "low": 1,
  "informational": 1,
  "total": 1
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/assets/criticality/summary" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/risk/exposure

**Summary:** Calculate Exposure Score

**Operation ID:** `calculate_exposure_score_api_v2_risk_exposure_post`

**Description:**
Calculate exposure score for asset.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "asset_id": "<asset_id>",
  "asset_name": "<asset_name>",
  "is_internet_facing": true,
  "attack_surface": "<attack_surface>",
  "open_ports": [],
  "unpatched_vulnerabilities": 1
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "asset_id": "<asset_id>",
  "asset_name": "<asset_name>",
  "customer_id": "<customer_id>",
  "is_internet_facing": true,
  "attack_surface": "<attack_surface>",
  "open_ports": [],
  "unpatched_vulnerabilities": 1
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X POST "http://localhost:8000/api/v2/risk/exposure" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "asset_id": "<asset_id>",
  "asset_name": "<asset_name>",
  "is_internet_facing": true,
  "attack_surface": "<attack_surface>",
  "open_ports": [],
  "unpatched_vulnerabilities": 1
}' 
```

---

## GET /api/v2/risk/exposure/{asset_id}

**Summary:** Get Exposure Score

**Operation ID:** `get_exposure_score_api_v2_risk_exposure__asset_id__get`

**Description:**
Get asset exposure score with customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `asset_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "asset_id": "<asset_id>",
  "asset_name": "<asset_name>",
  "customer_id": "<customer_id>",
  "is_internet_facing": true,
  "attack_surface": "<attack_surface>",
  "open_ports": [],
  "unpatched_vulnerabilities": 1
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/exposure/{asset_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/exposure/internet-facing

**Summary:** Get Internet Facing Assets

**Operation ID:** `get_internet_facing_assets_api_v2_risk_exposure_internet_facing_get`

**Description:**
Get all internet-facing assets.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "exposures": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/exposure/internet-facing" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/exposure/high-exposure

**Summary:** Get High Exposure Assets

**Operation ID:** `get_high_exposure_assets_api_v2_risk_exposure_high_exposure_get`

**Description:**
Get assets with high exposure scores.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `min_score` | number | ⬜ No | query | Minimum exposure score |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_results": 1,
  "customer_id": "<customer_id>",
  "exposures": []
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/exposure/high-exposure" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/exposure/attack-surface

**Summary:** Get Attack Surface Summary

**Operation ID:** `get_attack_surface_summary_api_v2_risk_exposure_attack_surface_get`

**Description:**
Get attack surface summary.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "customer_id": "<customer_id>",
  "total_assets": 1,
  "internet_facing": 1,
  "high_exposure_count": 1
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/exposure/attack-surface" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/aggregation/by-vendor

**Summary:** Get Risk By Vendor

**Operation ID:** `get_risk_by_vendor_api_v2_risk_aggregation_by_vendor_get`

**Description:**
Get risk aggregated by vendor.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `vendor_id` | string/null | ⬜ No | query | Specific vendor ID |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{
  "aggregation_id": "<aggregation_id>",
  "aggregation_type": "<aggregation_type>",
  "group_id": "<group_id>",
  "customer_id": "<customer_id>",
  "total_entities": 1,
  "risk_level": "<risk_level>",
  "calculated_at": "<calculated_at>"
}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/aggregation/by-vendor" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/aggregation/by-sector

**Summary:** Get Risk By Sector

**Operation ID:** `get_risk_by_sector_api_v2_risk_aggregation_by_sector_get`

**Description:**
Get risk aggregated by sector.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sector` | string/null | ⬜ No | query | Specific sector |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{
  "aggregation_id": "<aggregation_id>",
  "aggregation_type": "<aggregation_type>",
  "group_id": "<group_id>",
  "customer_id": "<customer_id>",
  "total_entities": 1,
  "risk_level": "<risk_level>",
  "calculated_at": "<calculated_at>"
}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/aggregation/by-sector" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/aggregation/by-asset-type

**Summary:** Get Risk By Asset Type

**Operation ID:** `get_risk_by_asset_type_api_v2_risk_aggregation_by_asset_type_get`

**Description:**
Get risk aggregated by asset type.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `asset_type` | string/null | ⬜ No | query | Specific asset type |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{
  "aggregation_id": "<aggregation_id>",
  "aggregation_type": "<aggregation_type>",
  "group_id": "<group_id>",
  "customer_id": "<customer_id>",
  "total_entities": 1,
  "risk_level": "<risk_level>",
  "calculated_at": "<calculated_at>"
}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/aggregation/by-asset-type" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/aggregation/{aggregation_type}/{group_id}

**Summary:** Get Risk Aggregation

**Operation ID:** `get_risk_aggregation_api_v2_risk_aggregation__aggregation_type___group_id__get`

**Description:**
Get specific risk aggregation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `aggregation_type` | string | ✅ Yes | path |  |
| `group_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "aggregation_id": "<aggregation_id>",
  "aggregation_type": "<aggregation_type>",
  "group_id": "<group_id>",
  "customer_id": "<customer_id>",
  "total_entities": 1,
  "risk_level": "<risk_level>",
  "calculated_at": "<calculated_at>"
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/aggregation/{aggregation_type}/{group_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/dashboard/summary

**Summary:** Get Dashboard Summary

**Operation ID:** `get_dashboard_summary_api_v2_risk_dashboard_summary_get`

**Description:**
Get comprehensive risk dashboard summary.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "customer_id": "<customer_id>",
  "total_entities": 1,
  "critical_count": 1,
  "high_count": 1,
  "generated_at": "<generated_at>"
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/dashboard/summary" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/risk/dashboard/risk-matrix

**Summary:** Get Risk Matrix

**Operation ID:** `get_risk_matrix_api_v2_risk_dashboard_risk_matrix_get`

**Description:**
Get risk matrix data (likelihood vs impact).

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "customer_id": "<customer_id>",
  "generated_at": "<generated_at>"
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/risk/dashboard/risk-matrix" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/remediation/tasks

**Summary:** Create Task

**Operation ID:** `create_task_api_v2_remediation_tasks_post`

**Description:**
Create a new remediation task.

Creates a remediation task for vulnerability remediation with SLA tracking.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "title": "<title>",
  "description": "<description>",
  "asset_ids": [],
  "task_type": "<task_type>",
  "priority": "<priority>"
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X POST "http://localhost:8000/api/v2/remediation/tasks" \
  -H "X-Customer-ID: <your_X_Customer_ID>" \
  -H "Content-Type: application/json" \
  -d '{
  "title": "<title>",
  "description": "<description>",
  "asset_ids": [],
  "task_type": "<task_type>",
  "priority": "<priority>"
}' 
```

---

## GET /api/v2/remediation/tasks/{task_id}

**Summary:** Get Task

**Operation ID:** `get_task_api_v2_remediation_tasks__task_id__get`

**Description:**
Get task details by ID.

Returns detailed information about a specific remediation task.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `task_id` | string | ✅ Yes | path |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/{task_id}" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/tasks/search

**Summary:** Search Tasks

**Operation ID:** `search_tasks_api_v2_remediation_tasks_search_get`

**Description:**
Search remediation tasks.

Search tasks with optional filters and semantic search.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `query` | string/null | ⬜ No | query | Search query |
| `status` | string/null | ⬜ No | query | Filter by status |
| `priority` | string/null | ⬜ No | query | Filter by priority |
| `assigned_to` | string/null | ⬜ No | query | Filter by assignee |
| `limit` | integer | ⬜ No | query | Maximum results |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/search" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/tasks/open

**Summary:** Get Open Tasks

**Operation ID:** `get_open_tasks_api_v2_remediation_tasks_open_get`

**Description:**
Get all open tasks.

Returns tasks that are not completed (open, in_progress, pending_verification).

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `limit` | integer | ⬜ No | query |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/open" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/tasks/overdue

**Summary:** Get Overdue Tasks

**Operation ID:** `get_overdue_tasks_api_v2_remediation_tasks_overdue_get`

**Description:**
Get overdue tasks.

Returns tasks that have breached their SLA deadline.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `limit` | integer | ⬜ No | query |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/overdue" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/tasks/by-priority/{priority}

**Summary:** Get Tasks By Priority

**Operation ID:** `get_tasks_by_priority_api_v2_remediation_tasks_by_priority__priority__get`

**Description:**
Get tasks by priority level.

Returns all tasks with the specified priority (critical, high, medium, low, emergency).

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `priority` | string | ✅ Yes | path |  |
| `limit` | integer | ⬜ No | query |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/by-priority/{priority}" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/tasks/by-status/{status}

**Summary:** Get Tasks By Status

**Operation ID:** `get_tasks_by_status_api_v2_remediation_tasks_by_status__status__get`

**Description:**
Get tasks by status.

Returns all tasks with the specified status.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `status` | string | ✅ Yes | path |  |
| `limit` | integer | ⬜ No | query |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/by-status/{status}" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## PUT /api/v2/remediation/tasks/{task_id}/status

**Summary:** Update Task Status

**Operation ID:** `update_task_status_api_v2_remediation_tasks__task_id__status_put`

**Description:**
Update task status.

Changes task status with audit trail recording.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `task_id` | string | ✅ Yes | path |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "status": "<status>",
  "performed_by": "<performed_by>"
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X PUT "http://localhost:8000/api/v2/remediation/tasks/{task_id}/status" \
  -H "X-Customer-ID: <your_X_Customer_ID>" \
  -H "Content-Type: application/json" \
  -d '{
  "status": "<status>",
  "performed_by": "<performed_by>"
}' 
```

---

## PUT /api/v2/remediation/tasks/{task_id}/assign

**Summary:** Assign Task

**Operation ID:** `assign_task_api_v2_remediation_tasks__task_id__assign_put`

**Description:**
Assign task to user or team.

Updates task assignment with audit trail.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `task_id` | string | ✅ Yes | path |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "assigned_to": "<assigned_to>",
  "assigned_by": "<assigned_by>"
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X PUT "http://localhost:8000/api/v2/remediation/tasks/{task_id}/assign" \
  -H "X-Customer-ID: <your_X_Customer_ID>" \
  -H "Content-Type: application/json" \
  -d '{
  "assigned_to": "<assigned_to>",
  "assigned_by": "<assigned_by>"
}' 
```

---

## GET /api/v2/remediation/tasks/{task_id}/history

**Summary:** Get Task History

**Operation ID:** `get_task_history_api_v2_remediation_tasks__task_id__history_get`

**Description:**
Get task action history.

Returns complete audit trail for a task.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `task_id` | string | ✅ Yes | path |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/{task_id}/history" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## POST /api/v2/remediation/plans

**Summary:** Create Plan

**Operation ID:** `create_plan_api_v2_remediation_plans_post`

**Description:**
Create a remediation plan.

Creates a plan to coordinate multiple remediation tasks.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "name": "<name>",
  "task_ids": [],
  "stakeholders": []
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X POST "http://localhost:8000/api/v2/remediation/plans" \
  -H "X-Customer-ID: <your_X_Customer_ID>" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "<name>",
  "task_ids": [],
  "stakeholders": []
}' 
```

---

## GET /api/v2/remediation/plans

**Summary:** List Plans

**Operation ID:** `list_plans_api_v2_remediation_plans_get`

**Description:**
List all remediation plans.

Returns plans with optional status filter.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `status` | string/null | ⬜ No | query | Filter by status |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/plans" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/plans/{plan_id}

**Summary:** Get Plan

**Operation ID:** `get_plan_api_v2_remediation_plans__plan_id__get`

**Description:**
Get plan details by ID.

Returns detailed information about a remediation plan.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plan_id` | string | ✅ Yes | path |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/plans/{plan_id}" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/plans/active

**Summary:** Get Active Plans

**Operation ID:** `get_active_plans_api_v2_remediation_plans_active_get`

**Description:**
Get active remediation plans.

Returns plans with status ACTIVE.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/plans/active" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## PUT /api/v2/remediation/plans/{plan_id}/status

**Summary:** Update Plan Status

**Operation ID:** `update_plan_status_api_v2_remediation_plans__plan_id__status_put`

**Description:**
Update plan status.

Changes plan status (DRAFT, ACTIVE, COMPLETED, CANCELLED).

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plan_id` | string | ✅ Yes | path |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "status": "<status>"
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X PUT "http://localhost:8000/api/v2/remediation/plans/{plan_id}/status" \
  -H "X-Customer-ID: <your_X_Customer_ID>" \
  -H "Content-Type: application/json" \
  -d '{
  "status": "<status>"
}' 
```

---

## GET /api/v2/remediation/plans/{plan_id}/progress

**Summary:** Get Plan Progress

**Operation ID:** `get_plan_progress_api_v2_remediation_plans__plan_id__progress_get`

**Description:**
Get plan progress metrics.

Returns completion percentage and task status breakdown.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plan_id` | string | ✅ Yes | path |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/plans/{plan_id}/progress" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## POST /api/v2/remediation/sla/policies

**Summary:** Create Sla Policy

**Operation ID:** `create_sla_policy_api_v2_remediation_sla_policies_post`

**Description:**
Create SLA policy.

Defines remediation SLA thresholds by severity.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "name": "<name>",
  "severity_thresholds": {
    "critical": 24,
    "high": 72,
    "low": 720,
    "medium": 168
  },
  "working_hours_only": true,
  "timezone": "<timezone>"
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X POST "http://localhost:8000/api/v2/remediation/sla/policies" \
  -H "X-Customer-ID: <your_X_Customer_ID>" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "<name>",
  "severity_thresholds": {
    "critical": 24,
    "high": 72,
    "low": 720,
    "medium": 168
  },
  "working_hours_only": true,
  "timezone": "<timezone>"
}' 
```

---

## GET /api/v2/remediation/sla/policies

**Summary:** List Sla Policies

**Operation ID:** `list_sla_policies_api_v2_remediation_sla_policies_get`

**Description:**
List SLA policies.

Returns all SLA policies for the customer.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `active_only` | boolean | ⬜ No | query | Return only active policies |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/sla/policies" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/sla/policies/{policy_id}

**Summary:** Get Sla Policy

**Operation ID:** `get_sla_policy_api_v2_remediation_sla_policies__policy_id__get`

**Description:**
Get SLA policy by ID.

Returns detailed SLA policy configuration.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `policy_id` | string | ✅ Yes | path |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/sla/policies/{policy_id}" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## PUT /api/v2/remediation/sla/policies/{policy_id}

**Summary:** Update Sla Policy

**Operation ID:** `update_sla_policy_api_v2_remediation_sla_policies__policy_id__put`

**Description:**
Update SLA policy.

Modifies SLA policy configuration.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `policy_id` | string | ✅ Yes | path |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X PUT "http://localhost:8000/api/v2/remediation/sla/policies/{policy_id}" \
  -H "X-Customer-ID: <your_X_Customer_ID>" \
  -H "Content-Type: application/json" \
  -d '{}' 
```

---

## GET /api/v2/remediation/sla/breaches

**Summary:** Get Sla Breaches

**Operation ID:** `get_sla_breaches_api_v2_remediation_sla_breaches_get`

**Description:**
Get SLA breaches.

Returns tasks that have breached SLA deadlines.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `limit` | integer | ⬜ No | query |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/sla/breaches" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/sla/at-risk

**Summary:** Get At Risk Tasks

**Operation ID:** `get_at_risk_tasks_api_v2_remediation_sla_at_risk_get`

**Description:**
Get tasks at risk of SLA breach.

Returns tasks with less than 20% time remaining.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `limit` | integer | ⬜ No | query |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{}]
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/sla/at-risk" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/metrics/summary

**Summary:** Get Metrics Summary

**Operation ID:** `get_metrics_summary_api_v2_remediation_metrics_summary_get`

**Description:**
Get remediation metrics summary.

Returns overall remediation performance metrics.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/metrics/summary" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/metrics/mttr

**Summary:** Get Mttr By Severity

**Operation ID:** `get_mttr_by_severity_api_v2_remediation_metrics_mttr_get`

**Description:**
Get Mean Time To Remediate by severity.

Returns average remediation time for each severity level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/metrics/mttr" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/metrics/sla-compliance

**Summary:** Get Sla Compliance

**Operation ID:** `get_sla_compliance_api_v2_remediation_metrics_sla_compliance_get`

**Description:**
Get SLA compliance rate.

Returns percentage of tasks completed within SLA.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `period_days` | integer | ⬜ No | query | Period in days |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/metrics/sla-compliance" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/metrics/backlog

**Summary:** Get Backlog Metrics

**Operation ID:** `get_backlog_metrics_api_v2_remediation_metrics_backlog_get`

**Description:**
Get vulnerability backlog metrics.

Returns backlog size and trend.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/metrics/backlog" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/metrics/trends

**Summary:** Get Remediation Trends

**Operation ID:** `get_remediation_trends_api_v2_remediation_metrics_trends_get`

**Description:**
Get remediation trends over time.

Returns time-series metrics for the specified period.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `period_days` | integer | ⬜ No | query | Period in days |
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/metrics/trends" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/dashboard/summary

**Summary:** Get Dashboard Summary

**Operation ID:** `get_dashboard_summary_api_v2_remediation_dashboard_summary_get`

**Description:**
Get remediation dashboard summary.

Returns comprehensive dashboard data for remediation overview.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/dashboard/summary" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/remediation/dashboard/workload

**Summary:** Get Workload Distribution

**Operation ID:** `get_workload_distribution_api_v2_remediation_dashboard_workload_get`

**Description:**
Get team workload distribution.

Returns task distribution by assignee and team.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/remediation/dashboard/workload" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/value/risk-adjusted

**Summary:** Get Risk Adjusted Value

**Operation ID:** `get_risk_adjusted_value_api_v2_economic_impact_value_risk_adjusted_get`

**Description:**
Get risk-adjusted business value

Adjusts business value based on risk exposure and vulnerability.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `entity_id` | string/null | ⬜ No | query |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |
| `X-Namespace` | string/null | ⬜ No | header |  |
| `X-Access-Level` | string/null | ⬜ No | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "success": true,
  "timestamp": "<timestamp>"
}
```

### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/economic-impact/value/risk-adjusted" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---
