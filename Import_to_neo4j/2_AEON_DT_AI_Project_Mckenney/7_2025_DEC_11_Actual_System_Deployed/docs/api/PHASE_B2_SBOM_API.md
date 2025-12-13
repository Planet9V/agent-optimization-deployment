# Phase B2 - SBOM Analysis APIs

**Total Endpoints:** 36

**Base URL:** `http://localhost:8000`

---

## Table of Contents

1. [POST /api/v2/sbom/sboms](#post--api-v2-sbom-sboms): Create Sbom
2. [GET /api/v2/sbom/sboms](#get--api-v2-sbom-sboms): List Sboms
3. [GET /api/v2/sbom/sboms/{sbom_id}](#get--api-v2-sbom-sboms-sbom_id): Get Sbom
4. [DELETE /api/v2/sbom/sboms/{sbom_id}](#delete--api-v2-sbom-sboms-sbom_id): Delete Sbom
5. [GET /api/v2/sbom/sboms/{sbom_id}/risk-summary](#get--api-v2-sbom-sboms-sbom_id-risk-summary): Get Sbom Risk Summary
6. [POST /api/v2/sbom/components](#post--api-v2-sbom-components): Create Component
7. [GET /api/v2/sbom/components/{component_id}](#get--api-v2-sbom-components-component_id): Get Component
8. [GET /api/v2/sbom/components/search](#get--api-v2-sbom-components-search): Search Components
9. [POST /api/v2/sbom/components/search](#post--api-v2-sbom-components-search): Semantic search for SBOM components
10. [GET /api/v2/sbom/components/vulnerable](#get--api-v2-sbom-components-vulnerable): Get Vulnerable Components
11. [GET /api/v2/sbom/components/high-risk](#get--api-v2-sbom-components-high-risk): Get High Risk Components
12. [GET /api/v2/sbom/sboms/{sbom_id}/components](#get--api-v2-sbom-sboms-sbom_id-components): Get Components By Sbom
13. [POST /api/v2/sbom/dependencies](#post--api-v2-sbom-dependencies): Create Dependency
14. [GET /api/v2/sbom/components/{component_id}/dependencies](#get--api-v2-sbom-components-component_id-dependencies): Get Dependency Tree
15. [GET /api/v2/sbom/components/{component_id}/dependents](#get--api-v2-sbom-components-component_id-dependents): Get Dependents
16. [GET /api/v2/sbom/components/{component_id}/impact](#get--api-v2-sbom-components-component_id-impact): Get Impact Analysis
17. [GET /api/v2/sbom/sboms/{sbom_id}/cycles](#get--api-v2-sbom-sboms-sbom_id-cycles): Detect Cycles
18. [GET /api/v2/sbom/dependencies/path](#get--api-v2-sbom-dependencies-path): Find Dependency Path
19. [GET /api/v2/sbom/sboms/{sbom_id}/graph-stats](#get--api-v2-sbom-sboms-sbom_id-graph-stats): Get Graph Stats
20. [POST /api/v2/sbom/vulnerabilities](#post--api-v2-sbom-vulnerabilities): Create Vulnerability
21. [GET /api/v2/sbom/vulnerabilities/{vulnerability_id}](#get--api-v2-sbom-vulnerabilities-vulnerability_id): Get Vulnerability
22. [GET /api/v2/sbom/vulnerabilities/search](#get--api-v2-sbom-vulnerabilities-search): Search Vulnerabilities
23. [GET /api/v2/sbom/vulnerabilities/critical](#get--api-v2-sbom-vulnerabilities-critical): Get Critical Vulnerabilities
24. [GET /api/v2/sbom/vulnerabilities/kev](#get--api-v2-sbom-vulnerabilities-kev): Get Kev Vulnerabilities
25. [GET /api/v2/sbom/vulnerabilities/epss-prioritized](#get--api-v2-sbom-vulnerabilities-epss-prioritized): Get Epss Prioritized Vulns
26. [GET /api/v2/sbom/vulnerabilities/by-apt](#get--api-v2-sbom-vulnerabilities-by-apt): Get Apt Vulnerability Report
27. [GET /api/v2/sbom/components/{component_id}/vulnerabilities](#get--api-v2-sbom-components-component_id-vulnerabilities): Get Vulnerabilities By Component
28. [POST /api/v2/sbom/vulnerabilities/{vulnerability_id}/acknowledge](#post--api-v2-sbom-vulnerabilities-vulnerability_id-acknowledge): Acknowledge Vulnerability
29. [GET /api/v2/sbom/sboms/{sbom_id}/remediation](#get--api-v2-sbom-sboms-sbom_id-remediation): Get Remediation Report
30. [GET /api/v2/sbom/sboms/{sbom_id}/license-compliance](#get--api-v2-sbom-sboms-sbom_id-license-compliance): Get License Compliance
31. [GET /api/v2/sbom/dashboard/summary](#get--api-v2-sbom-dashboard-summary): Get Dashboard Summary
32. [GET /api/v2/sbom/sboms/{sbom_id}/vulnerable-paths](#get--api-v2-sbom-sboms-sbom_id-vulnerable-paths): Get Vulnerable Paths
33. [POST /api/v2/sbom/sboms/{sbom_id}/correlate-equipment](#post--api-v2-sbom-sboms-sbom_id-correlate-equipment): Correlate With Equipment
34. [POST /api/v2/sbom/analyze](#post--api-v2-sbom-analyze): Analyze and store SBOM
35. [GET /api/v2/sbom/{sbom_id}](#get--api-v2-sbom-sbom_id): Get SBOM details
36. [GET /api/v2/sbom/summary](#get--api-v2-sbom-summary): Get SBOM summary statistics

---

# Endpoint Details


## POST /api/v2/sbom/sboms

**Summary:** Create Sbom

**Operation ID:** `create_sbom_api_v2_sbom_sboms_post`

**Description:**
Create a new SBOM for the customer.

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
  "sbom_id": "<sbom_id>",
  "name": "<name>",
  "format": "<format>"
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "sbom_id": "<sbom_id>",
  "name": "<name>",
  "customer_id": "<customer_id>",
  "format": "<format>",
  "total_components": 1,
  "direct_dependencies": 1,
  "transitive_dependencies": 1,
  "total_vulnerabilities": 1,
  "critical_count": 1,
  "high_count": 1,
  "medium_count": 1,
  "low_count": 1
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
curl -X POST "http://localhost:8000/api/v2/sbom/sboms" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "sbom_id": "<sbom_id>",
  "name": "<name>",
  "format": "<format>"
}' 
```

---

## GET /api/v2/sbom/sboms

**Summary:** List Sboms

**Operation ID:** `list_sboms_api_v2_sbom_sboms_get`

**Description:**
List SBOMs with filters and customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `query` | string/null | ⬜ No | query | Search query |
| `format` | string/null | ⬜ No | query | Filter by SBOM format |
| `has_vulnerabilities` | boolean/null | ⬜ No | query | Filter by vulnerability presence |
| `target_system_id` | string/null | ⬜ No | query | Filter by target system |
| `limit` | integer | ⬜ No | query | Maximum results |
| `include_system` | boolean | ⬜ No | query | Include SYSTEM SBOMs |
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
curl -X GET "http://localhost:8000/api/v2/sbom/sboms" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/sboms/{sbom_id}

**Summary:** Get Sbom

**Operation ID:** `get_sbom_api_v2_sbom_sboms__sbom_id__get`

**Description:**
Get SBOM by ID with customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sbom_id` | string | ✅ Yes | path |  |
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
  "sbom_id": "<sbom_id>",
  "name": "<name>",
  "customer_id": "<customer_id>",
  "format": "<format>",
  "total_components": 1,
  "direct_dependencies": 1,
  "transitive_dependencies": 1,
  "total_vulnerabilities": 1,
  "critical_count": 1,
  "high_count": 1,
  "medium_count": 1,
  "low_count": 1
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
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/{sbom_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## DELETE /api/v2/sbom/sboms/{sbom_id}

**Summary:** Delete Sbom

**Operation ID:** `delete_sbom_api_v2_sbom_sboms__sbom_id__delete`

**Description:**
Delete an SBOM and all its components.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sbom_id` | string | ✅ Yes | path |  |
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
curl -X DELETE "http://localhost:8000/api/v2/sbom/sboms/{sbom_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/sboms/{sbom_id}/risk-summary

**Summary:** Get Sbom Risk Summary

**Operation ID:** `get_sbom_risk_summary_api_v2_sbom_sboms__sbom_id__risk_summary_get`

**Description:**
Get comprehensive risk summary for an SBOM.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sbom_id` | string | ✅ Yes | path |  |
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
  "sbom_id": "<sbom_id>",
  "sbom_name": "<sbom_name>",
  "total_components": 1,
  "vulnerable_components": 1,
  "critical_vulns": 1,
  "high_vulns": 1,
  "license_risk_high_count": 1,
  "copyleft_count": 1,
  "remediation_available": 1,
  "kev_count": 1,
  "exploitable_count": 1
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
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/risk-summary" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/sbom/components

**Summary:** Create Component

**Operation ID:** `create_component_api_v2_sbom_components_post`

**Description:**
Create a new software component.

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
  "component_id": "<component_id>",
  "sbom_id": "<sbom_id>",
  "name": "<name>",
  "version": "<version>",
  "component_type": "<component_type>"
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "component_id": "<component_id>",
  "sbom_id": "<sbom_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "version": "<version>",
  "component_type": "<component_type>",
  "status": "<status>",
  "vulnerability_count": 1,
  "critical_vuln_count": 1,
  "is_high_risk": true
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
curl -X POST "http://localhost:8000/api/v2/sbom/components" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "component_id": "<component_id>",
  "sbom_id": "<sbom_id>",
  "name": "<name>",
  "version": "<version>",
  "component_type": "<component_type>"
}' 
```

---

## GET /api/v2/sbom/components/{component_id}

**Summary:** Get Component

**Operation ID:** `get_component_api_v2_sbom_components__component_id__get`

**Description:**
Get component by ID with customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `component_id` | string | ✅ Yes | path |  |
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
  "component_id": "<component_id>",
  "sbom_id": "<sbom_id>",
  "customer_id": "<customer_id>",
  "name": "<name>",
  "version": "<version>",
  "component_type": "<component_type>",
  "status": "<status>",
  "vulnerability_count": 1,
  "critical_vuln_count": 1,
  "is_high_risk": true
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
curl -X GET "http://localhost:8000/api/v2/sbom/components/{component_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/components/search

**Summary:** Search Components

**Operation ID:** `search_components_api_v2_sbom_components_search_get`

**Description:**
Search components with semantic search and filters.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `query` | string/null | ⬜ No | query | Semantic search query |
| `sbom_id` | string/null | ⬜ No | query | Filter by SBOM |
| `component_type` | string/null | ⬜ No | query | Filter by component type |
| `license_risk` | string/null | ⬜ No | query | Filter by license risk |
| `has_vulnerabilities` | boolean/null | ⬜ No | query | Filter by vulnerability presence |
| `min_cvss` | number/null | ⬜ No | query | Minimum CVSS score |
| `status` | string/null | ⬜ No | query | Filter by status |
| `limit` | integer | ⬜ No | query | Maximum results |
| `include_system` | boolean | ⬜ No | query | Include SYSTEM components |
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
curl -X GET "http://localhost:8000/api/v2/sbom/components/search" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/sbom/components/search

**Summary:** Semantic search for SBOM components

**Operation ID:** `search_components_api_v2_sbom_components_search_post`

**Description:**
Semantic search across SBOM components using Qdrant vector similarity.
    Enables natural language queries like "find all Apache components with vulnerabilities".

    **ICE Score: 7.29**
    - Impact: 8 (Useful for discovery)
    - Confidence: 9 (Proven vector search)
    - Ease: 8 (Qdrant integration)

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string/null | ⬜ No | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "query": "<query>",
  "limit": 1
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "results": [],
  "total_results": 1,
  "query": "<query>",
  "customer_id": "<customer_id>"
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
curl -X POST "http://localhost:8000/api/v2/sbom/components/search" \
  -H "Content-Type: application/json" \
  -d '{
  "query": "<query>",
  "limit": 1
}' 
```

---

## GET /api/v2/sbom/components/vulnerable

**Summary:** Get Vulnerable Components

**Operation ID:** `get_vulnerable_components_api_v2_sbom_components_vulnerable_get`

**Description:**
Get all components with vulnerabilities above CVSS threshold.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `min_cvss` | number | ⬜ No | query | Minimum CVSS threshold |
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
curl -X GET "http://localhost:8000/api/v2/sbom/components/vulnerable" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/components/high-risk

**Summary:** Get High Risk Components

**Operation ID:** `get_high_risk_components_api_v2_sbom_components_high_risk_get`

**Description:**
Get all high-risk components (critical vulns, high license risk, or deprecated).

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
curl -X GET "http://localhost:8000/api/v2/sbom/components/high-risk" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/sboms/{sbom_id}/components

**Summary:** Get Components By Sbom

**Operation ID:** `get_components_by_sbom_api_v2_sbom_sboms__sbom_id__components_get`

**Description:**
Get all components for a specific SBOM.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sbom_id` | string | ✅ Yes | path |  |
| `limit` | integer | ⬜ No | query | Maximum components |
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
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/components" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/sbom/dependencies

**Summary:** Create Dependency

**Operation ID:** `create_dependency_api_v2_sbom_dependencies_post`

**Description:**
Create a new dependency relation.

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
  "source_component_id": "<source_component_id>",
  "target_component_id": "<target_component_id>",
  "dependency_type": "<dependency_type>",
  "scope": "<scope>"
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "source_component_id": "<source_component_id>",
  "target_component_id": "<target_component_id>",
  "dependency_type": "<dependency_type>",
  "scope": "<scope>",
  "depth": 1,
  "is_direct": true
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
curl -X POST "http://localhost:8000/api/v2/sbom/dependencies" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "source_component_id": "<source_component_id>",
  "target_component_id": "<target_component_id>",
  "dependency_type": "<dependency_type>",
  "scope": "<scope>"
}' 
```

---

## GET /api/v2/sbom/components/{component_id}/dependencies

**Summary:** Get Dependency Tree

**Operation ID:** `get_dependency_tree_api_v2_sbom_components__component_id__dependencies_get`

**Description:**
Get dependency tree for a component.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `component_id` | string | ✅ Yes | path |  |
| `max_depth` | integer | ⬜ No | query | Maximum tree depth |
| `include_dev` | boolean | ⬜ No | query | Include dev dependencies |
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
  "component_id": "<component_id>",
  "component_name": "<component_name>",
  "depth": 1,
  "children": [],
  "dependencies_count": 1,
  "dependents_count": 1
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
curl -X GET "http://localhost:8000/api/v2/sbom/components/{component_id}/dependencies" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/components/{component_id}/dependents

**Summary:** Get Dependents

**Operation ID:** `get_dependents_api_v2_sbom_components__component_id__dependents_get`

**Description:**
Get all components that depend on this component (reverse dependencies).

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `component_id` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/sbom/components/{component_id}/dependents" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/components/{component_id}/impact

**Summary:** Get Impact Analysis

**Operation ID:** `get_impact_analysis_api_v2_sbom_components__component_id__impact_get`

**Description:**
Analyze the impact if a component has a vulnerability.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `component_id` | string | ✅ Yes | path |  |
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
  "component_id": "<component_id>",
  "component_name": "<component_name>",
  "direct_dependents": 1,
  "total_dependents": 1,
  "affected_sboms": [],
  "vulnerability_exposure": 1
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
curl -X GET "http://localhost:8000/api/v2/sbom/components/{component_id}/impact" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/sboms/{sbom_id}/cycles

**Summary:** Detect Cycles

**Operation ID:** `detect_cycles_api_v2_sbom_sboms__sbom_id__cycles_get`

**Description:**
Detect circular dependencies in an SBOM.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sbom_id` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/cycles" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/dependencies/path

**Summary:** Find Dependency Path

**Operation ID:** `find_dependency_path_api_v2_sbom_dependencies_path_get`

**Description:**
Find shortest dependency path between two components.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `source_id` | string | ✅ Yes | query | Source component ID |
| `target_id` | string | ✅ Yes | query | Target component ID |
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
curl -X GET "http://localhost:8000/api/v2/sbom/dependencies/path" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/sboms/{sbom_id}/graph-stats

**Summary:** Get Graph Stats

**Operation ID:** `get_graph_stats_api_v2_sbom_sboms__sbom_id__graph_stats_get`

**Description:**
Get comprehensive dependency graph statistics for an SBOM.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sbom_id` | string | ✅ Yes | path |  |
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
  "total_components": 1,
  "total_dependencies": 1,
  "direct_dependencies": 1,
  "transitive_dependencies": 1,
  "max_depth": 1,
  "root_nodes": 1,
  "leaf_nodes": 1,
  "cyclic_dependencies": 1
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
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/graph-stats" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/sbom/vulnerabilities

**Summary:** Create Vulnerability

**Operation ID:** `create_vulnerability_api_v2_sbom_vulnerabilities_post`

**Description:**
Create a new vulnerability record.

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
  "vulnerability_id": "<vulnerability_id>",
  "cve_id": "<cve_id>",
  "component_id": "<component_id>",
  "exploit_available": true,
  "in_the_wild": true,
  "cisa_kev": true,
  "apt_groups": []
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "vulnerability_id": "<vulnerability_id>",
  "cve_id": "<cve_id>",
  "component_id": "<component_id>",
  "customer_id": "<customer_id>",
  "severity": "<severity>",
  "exploit_available": true,
  "in_the_wild": true,
  "cisa_kev": true,
  "apt_groups": [],
  "is_critical": true,
  "has_fix": true,
  "acknowledged": true
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
curl -X POST "http://localhost:8000/api/v2/sbom/vulnerabilities" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "vulnerability_id": "<vulnerability_id>",
  "cve_id": "<cve_id>",
  "component_id": "<component_id>",
  "exploit_available": true,
  "in_the_wild": true,
  "cisa_kev": true,
  "apt_groups": []
}' 
```

---

## GET /api/v2/sbom/vulnerabilities/{vulnerability_id}

**Summary:** Get Vulnerability

**Operation ID:** `get_vulnerability_api_v2_sbom_vulnerabilities__vulnerability_id__get`

**Description:**
Get vulnerability by ID.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `vulnerability_id` | string | ✅ Yes | path |  |
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
  "vulnerability_id": "<vulnerability_id>",
  "cve_id": "<cve_id>",
  "component_id": "<component_id>",
  "customer_id": "<customer_id>",
  "severity": "<severity>",
  "exploit_available": true,
  "in_the_wild": true,
  "cisa_kev": true,
  "apt_groups": [],
  "is_critical": true,
  "has_fix": true,
  "acknowledged": true
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
curl -X GET "http://localhost:8000/api/v2/sbom/vulnerabilities/{vulnerability_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/vulnerabilities/search

**Summary:** Search Vulnerabilities

**Operation ID:** `search_vulnerabilities_api_v2_sbom_vulnerabilities_search_get`

**Description:**
Search vulnerabilities with semantic search and filters.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `query` | string/null | ⬜ No | query | Semantic search query |
| `component_id` | string/null | ⬜ No | query | Filter by component |
| `min_cvss` | number/null | ⬜ No | query | Minimum CVSS score |
| `severity` | string/null | ⬜ No | query | Filter by severity |
| `exploit_available` | boolean/null | ⬜ No | query | Has exploit available |
| `cisa_kev` | boolean/null | ⬜ No | query | Is in CISA KEV |
| `has_fix` | boolean/null | ⬜ No | query | Has fix available |
| `limit` | integer | ⬜ No | query | Maximum results |
| `include_system` | boolean | ⬜ No | query | Include SYSTEM vulnerabilities |
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
curl -X GET "http://localhost:8000/api/v2/sbom/vulnerabilities/search" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/vulnerabilities/critical

**Summary:** Get Critical Vulnerabilities

**Operation ID:** `get_critical_vulnerabilities_api_v2_sbom_vulnerabilities_critical_get`

**Description:**
Get all critical vulnerabilities (CISA KEV, in-the-wild, or CVSS >= 9.0).

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
curl -X GET "http://localhost:8000/api/v2/sbom/vulnerabilities/critical" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/vulnerabilities/kev

**Summary:** Get Kev Vulnerabilities

**Operation ID:** `get_kev_vulnerabilities_api_v2_sbom_vulnerabilities_kev_get`

**Description:**
Get all CISA Known Exploited Vulnerabilities (KEV).

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
curl -X GET "http://localhost:8000/api/v2/sbom/vulnerabilities/kev" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/vulnerabilities/epss-prioritized

**Summary:** Get Epss Prioritized Vulns

**Operation ID:** `get_epss_prioritized_vulns_api_v2_sbom_vulnerabilities_epss_prioritized_get`

**Description:**
Get vulnerabilities prioritized by EPSS score (exploit probability).

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `min_epss` | number | ⬜ No | query | Minimum EPSS score |
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
curl -X GET "http://localhost:8000/api/v2/sbom/vulnerabilities/epss-prioritized" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/vulnerabilities/by-apt

**Summary:** Get Apt Vulnerability Report

**Operation ID:** `get_apt_vulnerability_report_api_v2_sbom_vulnerabilities_by_apt_get`

**Description:**
Get vulnerability report grouped by APT groups.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `apt_group` | string/null | ⬜ No | query | Filter by specific APT group |
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
  "total_apt_groups": 1,
  "total_vulnerabilities": 1,
  "customer_id": "<customer_id>",
  "apt_breakdown": []
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
curl -X GET "http://localhost:8000/api/v2/sbom/vulnerabilities/by-apt" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/components/{component_id}/vulnerabilities

**Summary:** Get Vulnerabilities By Component

**Operation ID:** `get_vulnerabilities_by_component_api_v2_sbom_components__component_id__vulnerabilities_get`

**Description:**
Get all vulnerabilities for a specific component.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `component_id` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/sbom/components/{component_id}/vulnerabilities" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/sbom/vulnerabilities/{vulnerability_id}/acknowledge

**Summary:** Acknowledge Vulnerability

**Operation ID:** `acknowledge_vulnerability_api_v2_sbom_vulnerabilities__vulnerability_id__acknowledge_post`

**Description:**
Acknowledge a vulnerability (mark as reviewed).

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `vulnerability_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "acknowledged_by": "<acknowledged_by>",
  "notes": "<notes>",
  "risk_accepted": true
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
curl -X POST "http://localhost:8000/api/v2/sbom/vulnerabilities/{vulnerability_id}/acknowledge" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "acknowledged_by": "<acknowledged_by>",
  "notes": "<notes>",
  "risk_accepted": true
}' 
```

---

## GET /api/v2/sbom/sboms/{sbom_id}/remediation

**Summary:** Get Remediation Report

**Operation ID:** `get_remediation_report_api_v2_sbom_sboms__sbom_id__remediation_get`

**Description:**
Generate remediation report for an SBOM.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sbom_id` | string | ✅ Yes | path |  |
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
  "sbom_id": "<sbom_id>",
  "customer_id": "<customer_id>",
  "total_vulnerabilities": 1,
  "critical_vulns": 1,
  "with_patches": 1,
  "with_upgrades": 1,
  "no_fix_available": 1,
  "prioritized_actions": []
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
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/remediation" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/sboms/{sbom_id}/license-compliance

**Summary:** Get License Compliance

**Operation ID:** `get_license_compliance_api_v2_sbom_sboms__sbom_id__license_compliance_get`

**Description:**
Get license compliance analysis for an SBOM.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sbom_id` | string | ✅ Yes | path |  |
| `allowed_licenses` | array | ⬜ No | query | Allowed license types |
| `denied_licenses` | array | ⬜ No | query | Denied license types |
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
  "sbom_id": "<sbom_id>",
  "customer_id": "<customer_id>",
  "is_compliant": true,
  "compliant_count": 1,
  "non_compliant_count": 1,
  "copyleft_count": 1,
  "high_risk_count": 1,
  "license_conflicts": [],
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
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/license-compliance" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/dashboard/summary

**Summary:** Get Dashboard Summary

**Operation ID:** `get_dashboard_summary_api_v2_sbom_dashboard_summary_get`

**Description:**
Get customer-wide dashboard summary.

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
  "total_sboms": 1,
  "total_components": 1,
  "total_vulnerabilities": 1,
  "critical_vulns": 1,
  "high_vulns": 1,
  "kev_vulns": 1,
  "exploitable_vulns": 1,
  "high_risk_components": 1,
  "sboms_with_vulns": 1
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
curl -X GET "http://localhost:8000/api/v2/sbom/dashboard/summary" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/sbom/sboms/{sbom_id}/vulnerable-paths

**Summary:** Get Vulnerable Paths

**Operation ID:** `get_vulnerable_paths_api_v2_sbom_sboms__sbom_id__vulnerable_paths_get`

**Description:**
Find all paths to vulnerable components in an SBOM.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sbom_id` | string | ✅ Yes | path |  |
| `min_cvss` | number | ⬜ No | query | Minimum CVSS threshold |
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
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/vulnerable-paths" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/sbom/sboms/{sbom_id}/correlate-equipment

**Summary:** Correlate With Equipment

**Operation ID:** `correlate_with_equipment_api_v2_sbom_sboms__sbom_id__correlate_equipment_post`

**Description:**
Correlate SBOM vulnerabilities with E15 equipment.

Links software vulnerabilities to physical equipment for risk assessment.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sbom_id` | string | ✅ Yes | path |  |
| `equipment_id` | string | ✅ Yes | query | E15 Equipment ID to correlate |
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
curl -X POST "http://localhost:8000/api/v2/sbom/sboms/{sbom_id}/correlate-equipment" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/sbom/analyze

**Summary:** Analyze and store SBOM

**Operation ID:** `analyze_sbom_api_v2_sbom_analyze_post`

**Description:**
Parse SBOM file (CycloneDX or SPDX format), extract components and dependencies,
    store in Neo4j graph database, and create Qdrant embeddings for semantic search.

    **ICE Score: 8.1**
    - Impact: 9 (Critical for vulnerability tracking)
    - Confidence: 9 (Well-defined SBOM standards)
    - Ease: 7 (Complex parsing and storage)

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string/null | ⬜ No | header |  |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "format": "<format>",
  "project_name": "<project_name>"
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "sbom_id": "<sbom_id>",
  "project_name": "<project_name>",
  "components_count": 1,
  "vulnerabilities_count": 1,
  "created_at": "<created_at>",
  "customer_id": "<customer_id>",
  "message": "<message>"
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
curl -X POST "http://localhost:8000/api/v2/sbom/analyze" \
  -H "Content-Type: application/json" \
  -d '{
  "format": "<format>",
  "project_name": "<project_name>"
}' 
```

---

## GET /api/v2/sbom/{sbom_id}

**Summary:** Get SBOM details

**Operation ID:** `get_sbom_api_v2_sbom__sbom_id__get`

**Description:**
Retrieve detailed SBOM information including components, vulnerabilities, and metadata.

    **ICE Score: 9.0**
    - Impact: 9 (Essential for SBOM inspection)
    - Confidence: 10 (Straightforward graph query)
    - Ease: 9 (Simple Neo4j query)

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `sbom_id` | string | ✅ Yes | path |  |
| `X-Customer-ID` | string/null | ⬜ No | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "sbom_id": "<sbom_id>",
  "project_name": "<project_name>",
  "project_version": "<project_version>",
  "format": "<format>",
  "components_count": 1,
  "vulnerabilities_count": 1,
  "high_severity_count": 1,
  "critical_severity_count": 1,
  "created_at": "<created_at>",
  "customer_id": "<customer_id>",
  "components": []
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
curl -X GET "http://localhost:8000/api/v2/sbom/{sbom_id}"
```

---

## GET /api/v2/sbom/summary

**Summary:** Get SBOM summary statistics

**Operation ID:** `get_sbom_summary_api_v2_sbom_summary_get`

**Description:**
Aggregate SBOM statistics including total counts and vulnerability risk levels.

    **ICE Score: 8.0**
    - Impact: 8 (Important for dashboards)
    - Confidence: 10 (Simple aggregation)
    - Ease: 8 (Straightforward query)

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `X-Customer-ID` | string/null | ⬜ No | header |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_sboms": 1,
  "total_components": 1,
  "total_vulnerabilities": 1,
  "critical_vulnerabilities": 1,
  "high_vulnerabilities": 1,
  "medium_vulnerabilities": 1,
  "low_vulnerabilities": 1,
  "customer_id": "<customer_id>",
  "last_updated": "<last_updated>"
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
curl -X GET "http://localhost:8000/api/v2/sbom/summary"
```

---
