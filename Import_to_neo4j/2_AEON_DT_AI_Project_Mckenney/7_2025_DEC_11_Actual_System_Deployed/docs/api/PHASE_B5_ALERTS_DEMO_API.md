# Phase B5 - Alerts, Demographics & Economic APIs

**Total Endpoints:** 82

**Base URL:** `http://localhost:8000`

---

## Table of Contents

1. [POST /api/v2/alerts](#post--api-v2-alerts): Create Alert
2. [GET /api/v2/alerts](#get--api-v2-alerts): List Alerts
3. [GET /api/v2/alerts/{alert_id}](#get--api-v2-alerts-alert_id): Get Alert
4. [PUT /api/v2/alerts/{alert_id}](#put--api-v2-alerts-alert_id): Update Alert
5. [DELETE /api/v2/alerts/{alert_id}](#delete--api-v2-alerts-alert_id): Delete Alert
6. [GET /api/v2/alerts/by-severity/{severity}](#get--api-v2-alerts-by-severity-severity): Get Alerts By Severity
7. [GET /api/v2/alerts/by-status/{status}](#get--api-v2-alerts-by-status-status): Get Alerts By Status
8. [POST /api/v2/alerts/{alert_id}/acknowledge](#post--api-v2-alerts-alert_id-acknowledge): Acknowledge Alert
9. [POST /api/v2/alerts/{alert_id}/resolve](#post--api-v2-alerts-alert_id-resolve): Resolve Alert
10. [POST /api/v2/alerts/{alert_id}/assign](#post--api-v2-alerts-alert_id-assign): Assign Alert
11. [POST /api/v2/alerts/search](#post--api-v2-alerts-search): Search Alerts Semantic
12. [POST /api/v2/alerts/rules](#post--api-v2-alerts-rules): Create Alert Rule
13. [GET /api/v2/alerts/rules](#get--api-v2-alerts-rules): List Alert Rules
14. [GET /api/v2/alerts/rules/{rule_id}](#get--api-v2-alerts-rules-rule_id): Get Alert Rule
15. [PUT /api/v2/alerts/rules/{rule_id}](#put--api-v2-alerts-rules-rule_id): Update Alert Rule
16. [DELETE /api/v2/alerts/rules/{rule_id}](#delete--api-v2-alerts-rules-rule_id): Delete Alert Rule
17. [POST /api/v2/alerts/rules/{rule_id}/enable](#post--api-v2-alerts-rules-rule_id-enable): Enable Alert Rule
18. [POST /api/v2/alerts/rules/{rule_id}/disable](#post--api-v2-alerts-rules-rule_id-disable): Disable Alert Rule
19. [POST /api/v2/alerts/notifications](#post--api-v2-alerts-notifications): Create Notification Rule
20. [GET /api/v2/alerts/notifications](#get--api-v2-alerts-notifications): List Notification Rules
21. [GET /api/v2/alerts/notifications/{notification_id}](#get--api-v2-alerts-notifications-notification_id): Get Notification Rule
22. [PUT /api/v2/alerts/notifications/{notification_id}](#put--api-v2-alerts-notifications-notification_id): Update Notification Rule
23. [DELETE /api/v2/alerts/notifications/{notification_id}](#delete--api-v2-alerts-notifications-notification_id): Delete Notification Rule
24. [POST /api/v2/alerts/escalations](#post--api-v2-alerts-escalations): Create Escalation Policy
25. [GET /api/v2/alerts/escalations](#get--api-v2-alerts-escalations): List Escalation Policies
26. [GET /api/v2/alerts/escalations/{policy_id}](#get--api-v2-alerts-escalations-policy_id): Get Escalation Policy
27. [PUT /api/v2/alerts/escalations/{policy_id}](#put--api-v2-alerts-escalations-policy_id): Update Escalation Policy
28. [DELETE /api/v2/alerts/escalations/{policy_id}](#delete--api-v2-alerts-escalations-policy_id): Delete Escalation Policy
29. [POST /api/v2/alerts/correlations](#post--api-v2-alerts-correlations): Create Alert Correlation
30. [GET /api/v2/alerts/correlations](#get--api-v2-alerts-correlations): List Alert Correlations
31. [GET /api/v2/alerts/correlations/{correlation_id}](#get--api-v2-alerts-correlations-correlation_id): Get Alert Correlation
32. [GET /api/v2/alerts/dashboard/summary](#get--api-v2-alerts-dashboard-summary): Get Alert Summary
33. [GET /api/v2/demographics/population/summary](#get--api-v2-demographics-population-summary): Get Population Summary
34. [GET /api/v2/demographics/population/distribution](#get--api-v2-demographics-population-distribution): Get Population Distribution
35. [GET /api/v2/demographics/population/{org_unit_id}/profile](#get--api-v2-demographics-population-org_unit_id-profile): Get Org Unit Population Profile
36. [GET /api/v2/demographics/population/trends](#get--api-v2-demographics-population-trends): Get Population Trends
37. [POST /api/v2/demographics/population/query](#post--api-v2-demographics-population-query): Query Population
38. [GET /api/v2/demographics/workforce/composition](#get--api-v2-demographics-workforce-composition): Get Workforce Composition
39. [GET /api/v2/demographics/workforce/skills](#get--api-v2-demographics-workforce-skills): Get Skills Inventory
40. [GET /api/v2/demographics/workforce/turnover](#get--api-v2-demographics-workforce-turnover): Get Turnover Metrics
41. [GET /api/v2/demographics/workforce/{team_id}/profile](#get--api-v2-demographics-workforce-team_id-profile): Get Team Profile
42. [GET /api/v2/demographics/workforce/capacity](#get--api-v2-demographics-workforce-capacity): Get Capacity Metrics
43. [GET /api/v2/demographics/organization/hierarchy](#get--api-v2-demographics-organization-hierarchy): Get Organization Hierarchy
44. [GET /api/v2/demographics/organization/units](#get--api-v2-demographics-organization-units): List Organization Units
45. [GET /api/v2/demographics/organization/{unit_id}/details](#get--api-v2-demographics-organization-unit_id-details): Get Unit Details
46. [GET /api/v2/demographics/organization/relationships](#get--api-v2-demographics-organization-relationships): Get Organization Relationships
47. [POST /api/v2/demographics/organization/analyze](#post--api-v2-demographics-organization-analyze): Analyze Organization Structure
48. [GET /api/v2/demographics/roles/distribution](#get--api-v2-demographics-roles-distribution): Get Role Distribution
49. [GET /api/v2/demographics/roles/{role_id}/demographics](#get--api-v2-demographics-roles-role_id-demographics): Get Role Demographics
50. [GET /api/v2/demographics/roles/security-relevant](#get--api-v2-demographics-roles-security-relevant): Get Security Relevant Roles
51. [GET /api/v2/demographics/roles/access-patterns](#get--api-v2-demographics-roles-access-patterns): Get Access Patterns
52. [GET /api/v2/demographics/dashboard/summary](#get--api-v2-demographics-dashboard-summary): Get Dashboard Summary
53. [GET /api/v2/demographics/dashboard/baseline](#get--api-v2-demographics-dashboard-baseline): Get Baseline Metrics
54. [GET /api/v2/demographics/dashboard/indicators](#get--api-v2-demographics-dashboard-indicators): Get Demographic Indicators
55. [GET /api/v2/demographics/dashboard/alerts](#get--api-v2-demographics-dashboard-alerts): Get Demographic Alerts
56. [GET /api/v2/demographics/dashboard/trends](#get--api-v2-demographics-dashboard-trends): Get Trend Analysis
57. [GET /api/v2/economic-impact/costs/summary](#get--api-v2-economic-impact-costs-summary): Get Cost Summary
58. [GET /api/v2/economic-impact/costs/by-category](#get--api-v2-economic-impact-costs-by-category): Get Costs By Category
59. [GET /api/v2/economic-impact/costs/{entity_id}/breakdown](#get--api-v2-economic-impact-costs-entity_id-breakdown): Get Entity Cost Breakdown
60. [POST /api/v2/economic-impact/costs/calculate](#post--api-v2-economic-impact-costs-calculate): Calculate Costs
61. [GET /api/v2/economic-impact/costs/historical](#get--api-v2-economic-impact-costs-historical): Get Historical Costs
62. [GET /api/v2/economic-impact/roi/summary](#get--api-v2-economic-impact-roi-summary): Get Roi Summary
63. [GET /api/v2/economic-impact/roi/{investment_id}](#get--api-v2-economic-impact-roi-investment_id): Get Roi By Id
64. [POST /api/v2/economic-impact/roi/calculate](#post--api-v2-economic-impact-roi-calculate): Calculate Roi
65. [GET /api/v2/economic-impact/roi/by-category](#get--api-v2-economic-impact-roi-by-category): Get Roi By Category
66. [GET /api/v2/economic-impact/roi/projections](#get--api-v2-economic-impact-roi-projections): Get Roi Projections
67. [POST /api/v2/economic-impact/roi/comparison](#post--api-v2-economic-impact-roi-comparison): Compare Investments
68. [GET /api/v2/economic-impact/value/metrics](#get--api-v2-economic-impact-value-metrics): Get Value Metrics
69. [GET /api/v2/economic-impact/value/{asset_id}/assessment](#get--api-v2-economic-impact-value-asset_id-assessment): Get Value Assessment
70. [POST /api/v2/economic-impact/value/calculate](#post--api-v2-economic-impact-value-calculate): Calculate Business Value
71. [GET /api/v2/economic-impact/value/by-sector](#get--api-v2-economic-impact-value-by-sector): Get Value By Sector
72. [POST /api/v2/economic-impact/impact/model](#post--api-v2-economic-impact-impact-model): Model Impact
73. [GET /api/v2/economic-impact/impact/scenarios](#get--api-v2-economic-impact-impact-scenarios): List Impact Scenarios
74. [POST /api/v2/economic-impact/impact/simulate](#post--api-v2-economic-impact-impact-simulate): Run Impact Simulation
75. [GET /api/v2/economic-impact/impact/{scenario_id}/results](#get--api-v2-economic-impact-impact-scenario_id-results): Get Simulation Results
76. [GET /api/v2/economic-impact/impact/historical](#get--api-v2-economic-impact-impact-historical): Get Historical Impacts
77. [GET /api/v2/economic-impact/dashboard/summary](#get--api-v2-economic-impact-dashboard-summary): Get Dashboard Summary
78. [GET /api/v2/economic-impact/dashboard/trends](#get--api-v2-economic-impact-dashboard-trends): Get Dashboard Trends
79. [GET /api/v2/economic-impact/dashboard/kpis](#get--api-v2-economic-impact-dashboard-kpis): Get Dashboard Kpis
80. [GET /api/v2/economic-impact/dashboard/alerts](#get--api-v2-economic-impact-dashboard-alerts): Get Dashboard Alerts
81. [GET /api/v2/economic-impact/dashboard/executive](#get--api-v2-economic-impact-dashboard-executive): Get Executive Summary
82. [GET /api/v2/economic-impact/health](#get--api-v2-economic-impact-health): Health Check

---

# Endpoint Details


## POST /api/v2/alerts

**Summary:** Create Alert

**Operation ID:** `create_alert_api_v2_alerts_post`

**Description:**
Create a new alert.

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
  "alert_id": "<alert_id>",
  "title": "<title>",
  "severity": "<severity>",
  "status": "<status>",
  "source": "<source>",
  "event_type": "<event_type>",
  "affected_assets": [],
  "tags": []
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "alert_id": "<alert_id>",
  "customer_id": "<customer_id>",
  "title": "<title>",
  "severity": "<severity>",
  "status": "<status>",
  "source": "<source>",
  "event_type": "<event_type>",
  "affected_assets": [],
  "tags": [],
  "created_at": "<created_at>",
  "updated_at": "<updated_at>"
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
curl -X POST "http://localhost:8000/api/v2/alerts" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "alert_id": "<alert_id>",
  "title": "<title>",
  "severity": "<severity>",
  "status": "<status>",
  "source": "<source>",
  "event_type": "<event_type>",
  "affected_assets": [],
  "tags": []
}' 
```

---

## GET /api/v2/alerts

**Summary:** List Alerts

**Operation ID:** `list_alerts_api_v2_alerts_get`

**Description:**
List alerts with optional filters.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `severity` | string/null | ⬜ No | query | Filter by severity |
| `status` | string/null | ⬜ No | query | Filter by status |
| `event_type` | string/null | ⬜ No | query | Filter by event type |
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
curl -X GET "http://localhost:8000/api/v2/alerts" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/alerts/{alert_id}

**Summary:** Get Alert

**Operation ID:** `get_alert_api_v2_alerts__alert_id__get`

**Description:**
Get alert by ID with customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `alert_id` | string | ✅ Yes | path |  |
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
  "alert_id": "<alert_id>",
  "customer_id": "<customer_id>",
  "title": "<title>",
  "severity": "<severity>",
  "status": "<status>",
  "source": "<source>",
  "event_type": "<event_type>",
  "affected_assets": [],
  "tags": [],
  "created_at": "<created_at>",
  "updated_at": "<updated_at>"
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
curl -X GET "http://localhost:8000/api/v2/alerts/{alert_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## PUT /api/v2/alerts/{alert_id}

**Summary:** Update Alert

**Operation ID:** `update_alert_api_v2_alerts__alert_id__put`

**Description:**
Update an existing alert.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `alert_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

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
{
  "alert_id": "<alert_id>",
  "customer_id": "<customer_id>",
  "title": "<title>",
  "severity": "<severity>",
  "status": "<status>",
  "source": "<source>",
  "event_type": "<event_type>",
  "affected_assets": [],
  "tags": [],
  "created_at": "<created_at>",
  "updated_at": "<updated_at>"
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
curl -X PUT "http://localhost:8000/api/v2/alerts/{alert_id}" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{}' 
```

---

## DELETE /api/v2/alerts/{alert_id}

**Summary:** Delete Alert

**Operation ID:** `delete_alert_api_v2_alerts__alert_id__delete`

**Description:**
Delete an alert.

Requires ADMIN access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `alert_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 204 - Successful Response
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X DELETE "http://localhost:8000/api/v2/alerts/{alert_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/alerts/by-severity/{severity}

**Summary:** Get Alerts By Severity

**Operation ID:** `get_alerts_by_severity_api_v2_alerts_by_severity__severity__get`

**Description:**
Get alerts by severity level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `severity` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/alerts/by-severity/{severity}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/alerts/by-status/{status}

**Summary:** Get Alerts By Status

**Operation ID:** `get_alerts_by_status_api_v2_alerts_by_status__status__get`

**Description:**
Get alerts by status.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `status` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/alerts/by-status/{status}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/alerts/{alert_id}/acknowledge

**Summary:** Acknowledge Alert

**Operation ID:** `acknowledge_alert_api_v2_alerts__alert_id__acknowledge_post`

**Description:**
Acknowledge an alert.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `alert_id` | string | ✅ Yes | path |  |
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
  "alert_id": "<alert_id>",
  "customer_id": "<customer_id>",
  "title": "<title>",
  "severity": "<severity>",
  "status": "<status>",
  "source": "<source>",
  "event_type": "<event_type>",
  "affected_assets": [],
  "tags": [],
  "created_at": "<created_at>",
  "updated_at": "<updated_at>"
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
curl -X POST "http://localhost:8000/api/v2/alerts/{alert_id}/acknowledge" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/alerts/{alert_id}/resolve

**Summary:** Resolve Alert

**Operation ID:** `resolve_alert_api_v2_alerts__alert_id__resolve_post`

**Description:**
Resolve an alert.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `alert_id` | string | ✅ Yes | path |  |
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
  "alert_id": "<alert_id>",
  "customer_id": "<customer_id>",
  "title": "<title>",
  "severity": "<severity>",
  "status": "<status>",
  "source": "<source>",
  "event_type": "<event_type>",
  "affected_assets": [],
  "tags": [],
  "created_at": "<created_at>",
  "updated_at": "<updated_at>"
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
curl -X POST "http://localhost:8000/api/v2/alerts/{alert_id}/resolve" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/alerts/{alert_id}/assign

**Summary:** Assign Alert

**Operation ID:** `assign_alert_api_v2_alerts__alert_id__assign_post`

**Description:**
Assign an alert to a user.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `alert_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "assigned_to": "<assigned_to>"
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "alert_id": "<alert_id>",
  "customer_id": "<customer_id>",
  "title": "<title>",
  "severity": "<severity>",
  "status": "<status>",
  "source": "<source>",
  "event_type": "<event_type>",
  "affected_assets": [],
  "tags": [],
  "created_at": "<created_at>",
  "updated_at": "<updated_at>"
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
curl -X POST "http://localhost:8000/api/v2/alerts/{alert_id}/assign" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "assigned_to": "<assigned_to>"
}' 
```

---

## POST /api/v2/alerts/search

**Summary:** Search Alerts Semantic

**Operation ID:** `search_alerts_semantic_api_v2_alerts_search_post`

**Description:**
Semantic search for alerts.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `query` | string | ✅ Yes | query | Semantic search query |
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
curl -X POST "http://localhost:8000/api/v2/alerts/search" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/alerts/rules

**Summary:** Create Alert Rule

**Operation ID:** `create_alert_rule_api_v2_alerts_rules_post`

**Description:**
Create a new alert rule.

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
  "rule_id": "<rule_id>",
  "name": "<name>",
  "enabled": true,
  "severity": "<severity>",
  "actions": []
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "rule_id": "<rule_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "enabled": true,
  "severity": "<severity>",
  "actions": [],
  "created_at": "<created_at>",
  "updated_at": "<updated_at>",
  "triggered_count": 1
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
curl -X POST "http://localhost:8000/api/v2/alerts/rules" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "rule_id": "<rule_id>",
  "name": "<name>",
  "enabled": true,
  "severity": "<severity>",
  "actions": []
}' 
```

---

## GET /api/v2/alerts/rules

**Summary:** List Alert Rules

**Operation ID:** `list_alert_rules_api_v2_alerts_rules_get`

**Description:**
List alert rules.

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
  "rules": []
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
curl -X GET "http://localhost:8000/api/v2/alerts/rules" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/alerts/rules/{rule_id}

**Summary:** Get Alert Rule

**Operation ID:** `get_alert_rule_api_v2_alerts_rules__rule_id__get`

**Description:**
Get alert rule by ID.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `rule_id` | string | ✅ Yes | path |  |
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
  "rule_id": "<rule_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "enabled": true,
  "severity": "<severity>",
  "actions": [],
  "created_at": "<created_at>",
  "updated_at": "<updated_at>",
  "triggered_count": 1
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
curl -X GET "http://localhost:8000/api/v2/alerts/rules/{rule_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## PUT /api/v2/alerts/rules/{rule_id}

**Summary:** Update Alert Rule

**Operation ID:** `update_alert_rule_api_v2_alerts_rules__rule_id__put`

**Description:**
Update an alert rule.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `rule_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

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
{
  "rule_id": "<rule_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "enabled": true,
  "severity": "<severity>",
  "actions": [],
  "created_at": "<created_at>",
  "updated_at": "<updated_at>",
  "triggered_count": 1
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
curl -X PUT "http://localhost:8000/api/v2/alerts/rules/{rule_id}" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{}' 
```

---

## DELETE /api/v2/alerts/rules/{rule_id}

**Summary:** Delete Alert Rule

**Operation ID:** `delete_alert_rule_api_v2_alerts_rules__rule_id__delete`

**Description:**
Delete an alert rule.

Requires ADMIN access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `rule_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 204 - Successful Response
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X DELETE "http://localhost:8000/api/v2/alerts/rules/{rule_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/alerts/rules/{rule_id}/enable

**Summary:** Enable Alert Rule

**Operation ID:** `enable_alert_rule_api_v2_alerts_rules__rule_id__enable_post`

**Description:**
Enable an alert rule.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `rule_id` | string | ✅ Yes | path |  |
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
  "rule_id": "<rule_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "enabled": true,
  "severity": "<severity>",
  "actions": [],
  "created_at": "<created_at>",
  "updated_at": "<updated_at>",
  "triggered_count": 1
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
curl -X POST "http://localhost:8000/api/v2/alerts/rules/{rule_id}/enable" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/alerts/rules/{rule_id}/disable

**Summary:** Disable Alert Rule

**Operation ID:** `disable_alert_rule_api_v2_alerts_rules__rule_id__disable_post`

**Description:**
Disable an alert rule.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `rule_id` | string | ✅ Yes | path |  |
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
  "rule_id": "<rule_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "enabled": true,
  "severity": "<severity>",
  "actions": [],
  "created_at": "<created_at>",
  "updated_at": "<updated_at>",
  "triggered_count": 1
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
curl -X POST "http://localhost:8000/api/v2/alerts/rules/{rule_id}/disable" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/alerts/notifications

**Summary:** Create Notification Rule

**Operation ID:** `create_notification_rule_api_v2_alerts_notifications_post`

**Description:**
Create a new notification rule.

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
  "notification_id": "<notification_id>",
  "name": "<name>",
  "enabled": true,
  "channels": [],
  "recipients": []
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "notification_id": "<notification_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "enabled": true,
  "channels": [],
  "recipients": [],
  "created_at": "<created_at>",
  "sent_count": 1
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
curl -X POST "http://localhost:8000/api/v2/alerts/notifications" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "notification_id": "<notification_id>",
  "name": "<name>",
  "enabled": true,
  "channels": [],
  "recipients": []
}' 
```

---

## GET /api/v2/alerts/notifications

**Summary:** List Notification Rules

**Operation ID:** `list_notification_rules_api_v2_alerts_notifications_get`

**Description:**
List notification rules.

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
  "notifications": []
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
curl -X GET "http://localhost:8000/api/v2/alerts/notifications" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/alerts/notifications/{notification_id}

**Summary:** Get Notification Rule

**Operation ID:** `get_notification_rule_api_v2_alerts_notifications__notification_id__get`

**Description:**
Get notification rule by ID.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `notification_id` | string | ✅ Yes | path |  |
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
  "notification_id": "<notification_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "enabled": true,
  "channels": [],
  "recipients": [],
  "created_at": "<created_at>",
  "sent_count": 1
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
curl -X GET "http://localhost:8000/api/v2/alerts/notifications/{notification_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## PUT /api/v2/alerts/notifications/{notification_id}

**Summary:** Update Notification Rule

**Operation ID:** `update_notification_rule_api_v2_alerts_notifications__notification_id__put`

**Description:**
Update a notification rule.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `notification_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

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
{
  "notification_id": "<notification_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "enabled": true,
  "channels": [],
  "recipients": [],
  "created_at": "<created_at>",
  "sent_count": 1
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
curl -X PUT "http://localhost:8000/api/v2/alerts/notifications/{notification_id}" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{}' 
```

---

## DELETE /api/v2/alerts/notifications/{notification_id}

**Summary:** Delete Notification Rule

**Operation ID:** `delete_notification_rule_api_v2_alerts_notifications__notification_id__delete`

**Description:**
Delete a notification rule.

Requires ADMIN access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `notification_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 204 - Successful Response
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X DELETE "http://localhost:8000/api/v2/alerts/notifications/{notification_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/alerts/escalations

**Summary:** Create Escalation Policy

**Operation ID:** `create_escalation_policy_api_v2_alerts_escalations_post`

**Description:**
Create a new escalation policy.

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
  "policy_id": "<policy_id>",
  "name": "<name>",
  "enabled": true,
  "escalation_levels": []
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "policy_id": "<policy_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "enabled": true,
  "escalation_levels": [],
  "created_at": "<created_at>",
  "triggered_count": 1
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
curl -X POST "http://localhost:8000/api/v2/alerts/escalations" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "policy_id": "<policy_id>",
  "name": "<name>",
  "enabled": true,
  "escalation_levels": []
}' 
```

---

## GET /api/v2/alerts/escalations

**Summary:** List Escalation Policies

**Operation ID:** `list_escalation_policies_api_v2_alerts_escalations_get`

**Description:**
List escalation policies.

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
  "policies": []
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
curl -X GET "http://localhost:8000/api/v2/alerts/escalations" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/alerts/escalations/{policy_id}

**Summary:** Get Escalation Policy

**Operation ID:** `get_escalation_policy_api_v2_alerts_escalations__policy_id__get`

**Description:**
Get escalation policy by ID.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `policy_id` | string | ✅ Yes | path |  |
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
  "policy_id": "<policy_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "enabled": true,
  "escalation_levels": [],
  "created_at": "<created_at>",
  "triggered_count": 1
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
curl -X GET "http://localhost:8000/api/v2/alerts/escalations/{policy_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## PUT /api/v2/alerts/escalations/{policy_id}

**Summary:** Update Escalation Policy

**Operation ID:** `update_escalation_policy_api_v2_alerts_escalations__policy_id__put`

**Description:**
Update an escalation policy.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `policy_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

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
{
  "policy_id": "<policy_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "enabled": true,
  "escalation_levels": [],
  "created_at": "<created_at>",
  "triggered_count": 1
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
curl -X PUT "http://localhost:8000/api/v2/alerts/escalations/{policy_id}" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{}' 
```

---

## DELETE /api/v2/alerts/escalations/{policy_id}

**Summary:** Delete Escalation Policy

**Operation ID:** `delete_escalation_policy_api_v2_alerts_escalations__policy_id__delete`

**Description:**
Delete an escalation policy.

Requires ADMIN access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `policy_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

No request body required.

### Responses

### 204 - Successful Response
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X DELETE "http://localhost:8000/api/v2/alerts/escalations/{policy_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/alerts/correlations

**Summary:** Create Alert Correlation

**Operation ID:** `create_alert_correlation_api_v2_alerts_correlations_post`

**Description:**
Create a new alert correlation.

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
  "correlation_id": "<correlation_id>",
  "name": "<name>",
  "alert_ids": [],
  "correlation_type": "<correlation_type>"
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "correlation_id": "<correlation_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "alert_ids": [],
  "correlation_type": "<correlation_type>",
  "created_at": "<created_at>"
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
curl -X POST "http://localhost:8000/api/v2/alerts/correlations" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "correlation_id": "<correlation_id>",
  "name": "<name>",
  "alert_ids": [],
  "correlation_type": "<correlation_type>"
}' 
```

---

## GET /api/v2/alerts/correlations

**Summary:** List Alert Correlations

**Operation ID:** `list_alert_correlations_api_v2_alerts_correlations_get`

**Description:**
List alert correlations.

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
  "correlations": []
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
curl -X GET "http://localhost:8000/api/v2/alerts/correlations" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/alerts/correlations/{correlation_id}

**Summary:** Get Alert Correlation

**Operation ID:** `get_alert_correlation_api_v2_alerts_correlations__correlation_id__get`

**Description:**
Get alert correlation by ID.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `correlation_id` | string | ✅ Yes | path |  |
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
  "correlation_id": "<correlation_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "alert_ids": [],
  "correlation_type": "<correlation_type>",
  "created_at": "<created_at>"
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
curl -X GET "http://localhost:8000/api/v2/alerts/correlations/{correlation_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/alerts/dashboard/summary

**Summary:** Get Alert Summary

**Operation ID:** `get_alert_summary_api_v2_alerts_dashboard_summary_get`

**Description:**
Get alert dashboard summary.

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
  "total_alerts": 1,
  "open_alerts": 1,
  "acknowledged_alerts": 1,
  "investigating_alerts": 1,
  "resolved_alerts": 1,
  "critical_alerts": 1,
  "high_alerts": 1,
  "medium_alerts": 1,
  "low_alerts": 1,
  "alerts_last_24h": 1,
  "active_correlations": 1
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
curl -X GET "http://localhost:8000/api/v2/alerts/dashboard/summary" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/population/summary

**Summary:** Get Population Summary

**Operation ID:** `get_population_summary_api_v2_demographics_population_summary_get`

**Description:**
GET /api/v2/demographics/population/summary

Get population demographics summary.

Returns total population, active employees, contractors, growth rate,
and stability index.

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
  "total_population": 1,
  "active_employees": 1,
  "contractors": 1
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
curl -X GET "http://localhost:8000/api/v2/demographics/population/summary" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/population/distribution

**Summary:** Get Population Distribution

**Operation ID:** `get_population_distribution_api_v2_demographics_population_distribution_get`

**Description:**
GET /api/v2/demographics/population/distribution

Get population distribution by category.

Returns distribution by age group, tenure, education, and department.

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
curl -X GET "http://localhost:8000/api/v2/demographics/population/distribution" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/population/{org_unit_id}/profile

**Summary:** Get Org Unit Population Profile

**Operation ID:** `get_org_unit_population_profile_api_v2_demographics_population__org_unit_id__profile_get`

**Description:**
GET /api/v2/demographics/population/{org_unit_id}/profile

Get organization unit population profile.

Returns demographic profile for specific organizational unit.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `org_unit_id` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/demographics/population/{org_unit_id}/profile" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/population/trends

**Summary:** Get Population Trends

**Operation ID:** `get_population_trends_api_v2_demographics_population_trends_get`

**Description:**
GET /api/v2/demographics/population/trends

Get population trend analysis.

Returns historical trends and 90-day forecast.

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
  "trends": []
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
curl -X GET "http://localhost:8000/api/v2/demographics/population/trends" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/demographics/population/query

**Summary:** Query Population

**Operation ID:** `query_population_api_v2_demographics_population_query_post`

**Description:**
POST /api/v2/demographics/population/query

Execute custom population query.

Supports filters, grouping, and aggregations for flexible querying.

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
curl -X POST "http://localhost:8000/api/v2/demographics/population/query" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{}' 
```

---

## GET /api/v2/demographics/workforce/composition

**Summary:** Get Workforce Composition

**Operation ID:** `get_workforce_composition_api_v2_demographics_workforce_composition_get`

**Description:**
GET /api/v2/demographics/workforce/composition

Get workforce composition breakdown.

Returns composition by role, department, and turnover metrics.

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
  "org_unit_id": "<org_unit_id>",
  "org_unit_name": "<org_unit_name>",
  "customer_id": "<customer_id>",
  "total_employees": 1,
  "by_role": [],
  "by_department": []
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
curl -X GET "http://localhost:8000/api/v2/demographics/workforce/composition" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/workforce/skills

**Summary:** Get Skills Inventory

**Operation ID:** `get_skills_inventory_api_v2_demographics_workforce_skills_get`

**Description:**
GET /api/v2/demographics/workforce/skills

Get skills inventory and distribution.

Returns skills by category, critical skills, and skill gaps.

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
  "total_skills": 1,
  "critical_skills": [],
  "skill_gaps": []
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
curl -X GET "http://localhost:8000/api/v2/demographics/workforce/skills" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/workforce/turnover

**Summary:** Get Turnover Metrics

**Operation ID:** `get_turnover_metrics_api_v2_demographics_workforce_turnover_get`

**Description:**
GET /api/v2/demographics/workforce/turnover

Get turnover metrics and predictions.

Returns current turnover rate, predictions, and high-risk employees.

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
  "high_risk_employees": 1
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
curl -X GET "http://localhost:8000/api/v2/demographics/workforce/turnover" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/workforce/{team_id}/profile

**Summary:** Get Team Profile

**Operation ID:** `get_team_profile_api_v2_demographics_workforce__team_id__profile_get`

**Description:**
GET /api/v2/demographics/workforce/{team_id}/profile

Get team demographic profile.

Returns team demographics, cohesion score, and diversity index.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `team_id` | string | ✅ Yes | path |  |
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
  "team_id": "<team_id>",
  "team_name": "<team_name>",
  "customer_id": "<customer_id>",
  "member_count": 1
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
curl -X GET "http://localhost:8000/api/v2/demographics/workforce/{team_id}/profile" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/workforce/capacity

**Summary:** Get Capacity Metrics

**Operation ID:** `get_capacity_metrics_api_v2_demographics_workforce_capacity_get`

**Description:**
GET /api/v2/demographics/workforce/capacity

Get capacity and utilization metrics.

Returns total capacity, utilization, and overutilized teams.

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
  "total_capacity_hours": 1,
  "overutilized_teams": []
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
curl -X GET "http://localhost:8000/api/v2/demographics/workforce/capacity" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/organization/hierarchy

**Summary:** Get Organization Hierarchy

**Operation ID:** `get_organization_hierarchy_api_v2_demographics_organization_hierarchy_get`

**Description:**
GET /api/v2/demographics/organization/hierarchy

Get organization hierarchy map.

Returns complete organizational structure with units and relationships.

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
  "root_units": [],
  "total_units": 1,
  "max_depth": 1
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
curl -X GET "http://localhost:8000/api/v2/demographics/organization/hierarchy" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/organization/units

**Summary:** List Organization Units

**Operation ID:** `list_organization_units_api_v2_demographics_organization_units_get`

**Description:**
GET /api/v2/demographics/organization/units

List all organizational units.

Returns all units with basic information and employee counts.

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
  "units": [],
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
curl -X GET "http://localhost:8000/api/v2/demographics/organization/units" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/organization/{unit_id}/details

**Summary:** Get Unit Details

**Operation ID:** `get_unit_details_api_v2_demographics_organization__unit_id__details_get`

**Description:**
GET /api/v2/demographics/organization/{unit_id}/details

Get organization unit details with demographics.

Returns detailed unit information including demographics and criticality.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `unit_id` | string | ✅ Yes | path |  |
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
  "unit_id": "<unit_id>",
  "name": "<name>",
  "customer_id": "<customer_id>",
  "level": 1,
  "employee_count": 1,
  "criticality": "<criticality>",
  "security_roles_count": 1
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
curl -X GET "http://localhost:8000/api/v2/demographics/organization/{unit_id}/details" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/organization/relationships

**Summary:** Get Organization Relationships

**Operation ID:** `get_organization_relationships_api_v2_demographics_organization_relationships_get`

**Description:**
GET /api/v2/demographics/organization/relationships

Get inter-unit relationships.

Returns relationships between organizational units.

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
  "relationships": [],
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
curl -X GET "http://localhost:8000/api/v2/demographics/organization/relationships" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/demographics/organization/analyze

**Summary:** Analyze Organization Structure

**Operation ID:** `analyze_organization_structure_api_v2_demographics_organization_analyze_post`

**Description:**
POST /api/v2/demographics/organization/analyze

Analyze organization structure.

Supports various analysis types: span of control, depth analysis,
bottleneck detection, communication efficiency.

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
  "analysis_type": "<analysis_type>"
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
curl -X POST "http://localhost:8000/api/v2/demographics/organization/analyze" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "analysis_type": "<analysis_type>"
}' 
```

---

## GET /api/v2/demographics/roles/distribution

**Summary:** Get Role Distribution

**Operation ID:** `get_role_distribution_api_v2_demographics_roles_distribution_get`

**Description:**
GET /api/v2/demographics/roles/distribution

Get role distribution across organization.

Returns all roles with counts and security relevance.

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
  "total_roles": 1,
  "security_relevant_roles": 1,
  "roles": []
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
curl -X GET "http://localhost:8000/api/v2/demographics/roles/distribution" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/roles/{role_id}/demographics

**Summary:** Get Role Demographics

**Operation ID:** `get_role_demographics_api_v2_demographics_roles__role_id__demographics_get`

**Description:**
GET /api/v2/demographics/roles/{role_id}/demographics

Get demographics for specific role.

Returns demographic profile for employees in the specified role.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `role_id` | string | ✅ Yes | path |  |
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
  "role_id": "<role_id>",
  "role_name": "<role_name>",
  "customer_id": "<customer_id>",
  "employee_count": 1
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
curl -X GET "http://localhost:8000/api/v2/demographics/roles/{role_id}/demographics" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/roles/security-relevant

**Summary:** Get Security Relevant Roles

**Operation ID:** `get_security_relevant_roles_api_v2_demographics_roles_security_relevant_get`

**Description:**
GET /api/v2/demographics/roles/security-relevant

Get security-relevant roles analysis.

Returns roles with security implications and coverage metrics.

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
  "total_security_roles": 1,
  "roles": []
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
curl -X GET "http://localhost:8000/api/v2/demographics/roles/security-relevant" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/roles/access-patterns

**Summary:** Get Access Patterns

**Operation ID:** `get_access_patterns_api_v2_demographics_roles_access_patterns_get`

**Description:**
GET /api/v2/demographics/roles/access-patterns

Get role-based access patterns.

Returns normal access patterns and detected anomalies.

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
  "patterns": [],
  "anomalies": []
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
curl -X GET "http://localhost:8000/api/v2/demographics/roles/access-patterns" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/dashboard/summary

**Summary:** Get Dashboard Summary

**Operation ID:** `get_dashboard_summary_api_v2_demographics_dashboard_summary_get`

**Description:**
GET /api/v2/demographics/dashboard/summary

Get demographics dashboard summary.

Returns comprehensive dashboard with population, workforce, and
organization summaries.

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
curl -X GET "http://localhost:8000/api/v2/demographics/dashboard/summary" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/dashboard/baseline

**Summary:** Get Baseline Metrics

**Operation ID:** `get_baseline_metrics_api_v2_demographics_dashboard_baseline_get`

**Description:**
GET /api/v2/demographics/dashboard/baseline

Get baseline metrics for psychohistory.

Returns key metrics used for psychohistory calculations:
- Population stability index
- Role diversity score
- Skill concentration risk
- Succession coverage
- Insider threat baseline

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
curl -X GET "http://localhost:8000/api/v2/demographics/dashboard/baseline" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/dashboard/indicators

**Summary:** Get Demographic Indicators

**Operation ID:** `get_demographic_indicators_api_v2_demographics_dashboard_indicators_get`

**Description:**
GET /api/v2/demographics/dashboard/indicators

Get key demographic indicators.

Returns monitored indicators with thresholds and health status.

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
  "indicators": [],
  "warnings": []
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
curl -X GET "http://localhost:8000/api/v2/demographics/dashboard/indicators" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/dashboard/alerts

**Summary:** Get Demographic Alerts

**Operation ID:** `get_demographic_alerts_api_v2_demographics_dashboard_alerts_get`

**Description:**
GET /api/v2/demographics/dashboard/alerts

Get demographic alerts and anomalies.

Returns active alerts for demographic concerns requiring attention.

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
  "alerts": [],
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
curl -X GET "http://localhost:8000/api/v2/demographics/dashboard/alerts" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/demographics/dashboard/trends

**Summary:** Get Trend Analysis

**Operation ID:** `get_trend_analysis_api_v2_demographics_dashboard_trends_get`

**Description:**
GET /api/v2/demographics/dashboard/trends

Get demographic trend analysis.

Returns trend analysis with forecasting for key demographic metrics.

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
  "trends": []
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
curl -X GET "http://localhost:8000/api/v2/demographics/dashboard/trends" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/economic-impact/costs/summary

**Summary:** Get Cost Summary

**Operation ID:** `get_cost_summary_api_v2_economic_impact_costs_summary_get`

**Description:**
Get cost summary dashboard

Shows total costs, breakdown by category, and trends for specified period.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `period_days` | integer | ⬜ No | query |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/costs/summary" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/costs/by-category

**Summary:** Get Costs By Category

**Operation ID:** `get_costs_by_category_api_v2_economic_impact_costs_by_category_get`

**Description:**
Get costs by category (equipment, personnel, downtime, etc.)

Groups all costs by category with detailed breakdown.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `category` | null | ⬜ No | query |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/costs/by-category" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/costs/{entity_id}/breakdown

**Summary:** Get Entity Cost Breakdown

**Operation ID:** `get_entity_cost_breakdown_api_v2_economic_impact_costs__entity_id__breakdown_get`

**Description:**
Get detailed cost breakdown for specific entity

Shows direct costs, indirect costs, and allocated overhead.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `entity_id` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/costs/{entity_id}/breakdown" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## POST /api/v2/economic-impact/costs/calculate

**Summary:** Calculate Costs

**Operation ID:** `calculate_costs_api_v2_economic_impact_costs_calculate_post`

**Description:**
Calculate costs for scenario

Estimates direct, indirect, and opportunity costs for given scenario.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |
| `X-Namespace` | string/null | ⬜ No | header |  |
| `X-Access-Level` | string/null | ⬜ No | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "customer_id": "<customer_id>",
  "scenario_type": "<scenario_type>",
  "affected_systems": [],
  "personnel_count": 1
}
```

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
curl -X POST "http://localhost:8000/api/v2/economic-impact/costs/calculate" \
  -H "X-Customer-ID: <your_X_Customer_ID>" \
  -H "Content-Type: application/json" \
  -d '{
  "customer_id": "<customer_id>",
  "scenario_type": "<scenario_type>",
  "affected_systems": [],
  "personnel_count": 1
}' 
```

---

## GET /api/v2/economic-impact/costs/historical

**Summary:** Get Historical Costs

**Operation ID:** `get_historical_costs_api_v2_economic_impact_costs_historical_get`

**Description:**
Get historical cost trends

Shows cost trends over time with direction and percentage change.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `category` | null | ⬜ No | query |  |
| `days` | integer | ⬜ No | query |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/costs/historical" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/roi/summary

**Summary:** Get Roi Summary

**Operation ID:** `get_roi_summary_api_v2_economic_impact_roi_summary_get`

**Description:**
Get ROI summary for all investments

Shows aggregated ROI metrics, best/worst performers, and category breakdown.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/roi/summary" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/roi/{investment_id}

**Summary:** Get Roi By Id

**Operation ID:** `get_roi_by_id_api_v2_economic_impact_roi__investment_id__get`

**Description:**
Get ROI for specific investment

Returns detailed ROI calculation including NPV, IRR, and payback period.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `investment_id` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/roi/{investment_id}" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## POST /api/v2/economic-impact/roi/calculate

**Summary:** Calculate Roi

**Operation ID:** `calculate_roi_api_v2_economic_impact_roi_calculate_post`

**Description:**
Calculate ROI for proposed investment

Calculates ROI percentage, NPV, IRR, and payback period for investment proposal.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |
| `X-Namespace` | string/null | ⬜ No | header |  |
| `X-Access-Level` | string/null | ⬜ No | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "customer_id": "<customer_id>",
  "investment_name": "<investment_name>",
  "project_lifetime_years": 1
}
```

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
curl -X POST "http://localhost:8000/api/v2/economic-impact/roi/calculate" \
  -H "X-Customer-ID: <your_X_Customer_ID>" \
  -H "Content-Type: application/json" \
  -d '{
  "customer_id": "<customer_id>",
  "investment_name": "<investment_name>",
  "project_lifetime_years": 1
}' 
```

---

## GET /api/v2/economic-impact/roi/by-category

**Summary:** Get Roi By Category

**Operation ID:** `get_roi_by_category_api_v2_economic_impact_roi_by_category_get`

**Description:**
Get ROI grouped by investment category

Shows average ROI for each investment type (security tools, infrastructure, etc.)

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `category` | null | ⬜ No | query |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/roi/by-category" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/roi/projections

**Summary:** Get Roi Projections

**Operation ID:** `get_roi_projections_api_v2_economic_impact_roi_projections_get`

**Description:**
Get future ROI projections

Projects future ROI with confidence intervals based on growth assumptions.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `investment_id` | string | ✅ Yes | query |  |
| `years` | integer | ⬜ No | query |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/roi/projections" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## POST /api/v2/economic-impact/roi/comparison

**Summary:** Compare Investments

**Operation ID:** `compare_investments_api_v2_economic_impact_roi_comparison_post`

**Description:**
Compare multiple investment options

Side-by-side comparison with ranking and recommendations.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |
| `X-Namespace` | string/null | ⬜ No | header |  |
| `X-Access-Level` | string/null | ⬜ No | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
[{}]
```

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
curl -X POST "http://localhost:8000/api/v2/economic-impact/roi/comparison" \
  -H "X-Customer-ID: <your_X_Customer_ID>" \
  -H "Content-Type: application/json" \
  -d '[{}]' 
```

---

## GET /api/v2/economic-impact/value/metrics

**Summary:** Get Value Metrics

**Operation ID:** `get_value_metrics_api_v2_economic_impact_value_metrics_get`

**Description:**
Get business value metrics dashboard

Shows total asset value, critical assets, and value distribution.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/value/metrics" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/value/{asset_id}/assessment

**Summary:** Get Value Assessment

**Operation ID:** `get_value_assessment_api_v2_economic_impact_value__asset_id__assessment_get`

**Description:**
Get value assessment for specific asset

Detailed business value calculation with confidence score.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `asset_id` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/value/{asset_id}/assessment" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## POST /api/v2/economic-impact/value/calculate

**Summary:** Calculate Business Value

**Operation ID:** `calculate_business_value_api_v2_economic_impact_value_calculate_post`

**Description:**
Calculate business value for entity

Calculates total business value from multiple factors.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |
| `X-Namespace` | string/null | ⬜ No | header |  |
| `X-Access-Level` | string/null | ⬜ No | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "customer_id": "<customer_id>",
  "entity_id": "<entity_id>",
  "entity_type": "<entity_type>",
  "regulatory_requirements": [],
  "ip_patents": 1
}
```

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
curl -X POST "http://localhost:8000/api/v2/economic-impact/value/calculate" \
  -H "X-Customer-ID: <your_X_Customer_ID>" \
  -H "Content-Type: application/json" \
  -d '{
  "customer_id": "<customer_id>",
  "entity_id": "<entity_id>",
  "entity_type": "<entity_type>",
  "regulatory_requirements": [],
  "ip_patents": 1
}' 
```

---

## GET /api/v2/economic-impact/value/by-sector

**Summary:** Get Value By Sector

**Operation ID:** `get_value_by_sector_api_v2_economic_impact_value_by_sector_get`

**Description:**
Get value metrics by industry sector

Industry-specific value analysis with benchmarking.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sector` | string/null | ⬜ No | query |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/value/by-sector" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## POST /api/v2/economic-impact/impact/model

**Summary:** Model Impact

**Operation ID:** `model_impact_api_v2_economic_impact_impact_model_post`

**Description:**
Model financial impact of incident

Simulates financial impact of security incident with detailed breakdown.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string | ✅ Yes | header |  |
| `X-Namespace` | string/null | ⬜ No | header |  |
| `X-Access-Level` | string/null | ⬜ No | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "customer_id": "<customer_id>",
  "include_indirect_costs": true,
  "include_reputation_impact": true,
  "time_horizon_days": 1
}
```

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
curl -X POST "http://localhost:8000/api/v2/economic-impact/impact/model" \
  -H "X-Customer-ID: <your_X_Customer_ID>" \
  -H "Content-Type: application/json" \
  -d '{
  "customer_id": "<customer_id>",
  "include_indirect_costs": true,
  "include_reputation_impact": true,
  "time_horizon_days": 1
}' 
```

---

## GET /api/v2/economic-impact/impact/scenarios

**Summary:** List Impact Scenarios

**Operation ID:** `list_impact_scenarios_api_v2_economic_impact_impact_scenarios_get`

**Description:**
List available impact scenarios

Shows all defined impact scenarios with estimated costs.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scenario_type` | string/null | ⬜ No | query |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/impact/scenarios" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## POST /api/v2/economic-impact/impact/simulate

**Summary:** Run Impact Simulation

**Operation ID:** `run_impact_simulation_api_v2_economic_impact_impact_simulate_post`

**Description:**
Run Monte Carlo impact simulation

Runs multiple simulations to establish confidence intervals.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `iterations` | integer | ⬜ No | query |  |
| `X-Customer-ID` | string | ✅ Yes | header |  |
| `X-Namespace` | string/null | ⬜ No | header |  |
| `X-Access-Level` | string/null | ⬜ No | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "customer_id": "<customer_id>",
  "include_indirect_costs": true,
  "include_reputation_impact": true,
  "time_horizon_days": 1
}
```

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
curl -X POST "http://localhost:8000/api/v2/economic-impact/impact/simulate" \
  -H "X-Customer-ID: <your_X_Customer_ID>" \
  -H "Content-Type: application/json" \
  -d '{
  "customer_id": "<customer_id>",
  "include_indirect_costs": true,
  "include_reputation_impact": true,
  "time_horizon_days": 1
}' 
```

---

## GET /api/v2/economic-impact/impact/{scenario_id}/results

**Summary:** Get Simulation Results

**Operation ID:** `get_simulation_results_api_v2_economic_impact_impact__scenario_id__results_get`

**Description:**
Get simulation results for scenario

Retrieves detailed results from previous simulation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scenario_id` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/impact/{scenario_id}/results" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/impact/historical

**Summary:** Get Historical Impacts

**Operation ID:** `get_historical_impacts_api_v2_economic_impact_impact_historical_get`

**Description:**
Get historical impact data

Shows actual vs estimated costs from past incidents.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scenario_type` | string/null | ⬜ No | query |  |
| `limit` | integer | ⬜ No | query |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/impact/historical" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/dashboard/summary

**Summary:** Get Dashboard Summary

**Operation ID:** `get_dashboard_summary_api_v2_economic_impact_dashboard_summary_get`

**Description:**
Get economic dashboard summary

Comprehensive dashboard with all key economic metrics.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/dashboard/summary" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/dashboard/trends

**Summary:** Get Dashboard Trends

**Operation ID:** `get_dashboard_trends_api_v2_economic_impact_dashboard_trends_get`

**Description:**
Get economic trends over time

Time-series data for costs, ROI, value, and incident impacts.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `period` | string | ⬜ No | query |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/dashboard/trends" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/dashboard/kpis

**Summary:** Get Dashboard Kpis

**Operation ID:** `get_dashboard_kpis_api_v2_economic_impact_dashboard_kpis_get`

**Description:**
Get key performance indicators

Critical KPIs for security investment performance.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/dashboard/kpis" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/dashboard/alerts

**Summary:** Get Dashboard Alerts

**Operation ID:** `get_dashboard_alerts_api_v2_economic_impact_dashboard_alerts_get`

**Description:**
Get economic alerts and threshold violations

Active alerts for budget overruns, low ROI, high risk exposure.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `severity` | string/null | ⬜ No | query |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/dashboard/alerts" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/dashboard/executive

**Summary:** Get Executive Summary

**Operation ID:** `get_executive_summary_api_v2_economic_impact_dashboard_executive_get`

**Description:**
Get executive summary view

High-level summary for executive reporting and decision-making.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `period` | string | ⬜ No | query |  |
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
curl -X GET "http://localhost:8000/api/v2/economic-impact/dashboard/executive" \
  -H "X-Customer-ID: <your_X_Customer_ID>"
```

---

## GET /api/v2/economic-impact/health

**Summary:** Health Check

**Operation ID:** `health_check_api_v2_economic_impact_health_get`

**Description:**
Health check endpoint

### Parameters

No parameters required.

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/economic-impact/health"
```

---
