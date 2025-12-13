# Master API Reference

**NER11 Gold Standard API v3.3.0**

**Total Endpoints:** 263

**Base URL:** `http://localhost:8000`

---

## API Overview

High-performance Named Entity Recognition API with Hierarchical Semantic Search and Neo4j Graph Expansion.

## Endpoint Summary by Phase

| Phase | Paths (Operations) | Description |
|-------|-----------|-------------|
| **B2: SBOM & Vendor** | 59 (65) | Software Bill of Materials and vendor management |
| **B3: Threat & Risk** | 79 (82) | Vulnerability, threat intelligence, risk assessment |
| **B4: Compliance & Alerts** | 60 (60) | Compliance frameworks and alert management |
| **B5: Economic & Demographics** | 27 (27) | Economic impact, demographics, psychometrics |
| **Core NER11** | 5 (5) | Health check, NER extraction, semantic search |

**Total**: 230 paths, 263 operations

**Note**: Some paths support multiple HTTP methods (GET, POST, PUT, DELETE) creating additional operations

---


## Phase B2: SBOM Analysis APIs

**Total Endpoints:** 36


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

## Phase B3: Threat, Risk & Remediation APIs

**Total Endpoints:** 81


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

## Phase B4: Compliance & Audit APIs

**Total Endpoints:** 28


## GET /api/v2/compliance/assessments

**Summary:** List Assessments

**Operation ID:** `list_assessments_api_v2_compliance_assessments_get`

**Description:**
List assessments with optional filters.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `control_id` | string/null | ⬜ No | query | Filter by control |
| `status` | string/null | ⬜ No | query | Filter by status |
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
curl -X GET "http://localhost:8000/api/v2/compliance/assessments" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/compliance/assessments

**Summary:** Create Assessment

**Operation ID:** `create_assessment_api_v2_compliance_assessments_post`

**Description:**
Create a new compliance assessment.

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
  "assessment_id": "<assessment_id>",
  "control_id": "<control_id>",
  "assessment_date": "<assessment_date>",
  "assessor": "<assessor>",
  "status": "<status>",
  "compliance_score": 1,
  "findings": [],
  "recommendations": [],
  "evidence_ids": []
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "assessment_id": "<assessment_id>",
  "customer_id": "<customer_id>",
  "control_id": "<control_id>",
  "assessment_date": "<assessment_date>",
  "assessor": "<assessor>",
  "status": "<status>",
  "compliance_score": 1,
  "findings_count": 1,
  "evidence_count": 1
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
curl -X POST "http://localhost:8000/api/v2/compliance/assessments" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "assessment_id": "<assessment_id>",
  "control_id": "<control_id>",
  "assessment_date": "<assessment_date>",
  "assessor": "<assessor>",
  "status": "<status>",
  "compliance_score": 1,
  "findings": [],
  "recommendations": [],
  "evidence_ids": []
}' 
```

---

## GET /api/v2/compliance/assessments/by-framework/{framework}

**Summary:** Get Assessments By Framework

**Operation ID:** `get_assessments_by_framework_api_v2_compliance_assessments_by_framework__framework__get`

**Description:**
Get assessments for a specific framework.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `framework` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/compliance/assessments/by-framework/{framework}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/compliance/assessments/{assessment_id}

**Summary:** Get Assessment

**Operation ID:** `get_assessment_api_v2_compliance_assessments__assessment_id__get`

**Description:**
Get assessment by ID with customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `assessment_id` | string | ✅ Yes | path |  |
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
  "assessment_id": "<assessment_id>",
  "customer_id": "<customer_id>",
  "control_id": "<control_id>",
  "assessment_date": "<assessment_date>",
  "assessor": "<assessor>",
  "status": "<status>",
  "compliance_score": 1,
  "findings_count": 1,
  "evidence_count": 1
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
curl -X GET "http://localhost:8000/api/v2/compliance/assessments/{assessment_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## PUT /api/v2/compliance/assessments/{assessment_id}

**Summary:** Update Assessment

**Operation ID:** `update_assessment_api_v2_compliance_assessments__assessment_id__put`

**Description:**
Update an existing assessment.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `assessment_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "assessment_id": "<assessment_id>",
  "control_id": "<control_id>",
  "assessment_date": "<assessment_date>",
  "assessor": "<assessor>",
  "status": "<status>",
  "compliance_score": 1,
  "findings": [],
  "recommendations": [],
  "evidence_ids": []
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "assessment_id": "<assessment_id>",
  "customer_id": "<customer_id>",
  "control_id": "<control_id>",
  "assessment_date": "<assessment_date>",
  "assessor": "<assessor>",
  "status": "<status>",
  "compliance_score": 1,
  "findings_count": 1,
  "evidence_count": 1
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
curl -X PUT "http://localhost:8000/api/v2/compliance/assessments/{assessment_id}" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "assessment_id": "<assessment_id>",
  "control_id": "<control_id>",
  "assessment_date": "<assessment_date>",
  "assessor": "<assessor>",
  "status": "<status>",
  "compliance_score": 1,
  "findings": [],
  "recommendations": [],
  "evidence_ids": []
}' 
```

---

## POST /api/v2/compliance/assessments/{assessment_id}/complete

**Summary:** Complete Assessment

**Operation ID:** `complete_assessment_api_v2_compliance_assessments__assessment_id__complete_post`

**Description:**
Mark an assessment as completed.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `assessment_id` | string | ✅ Yes | path |  |
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
curl -X POST "http://localhost:8000/api/v2/compliance/assessments/{assessment_id}/complete" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/compliance/controls

**Summary:** List Controls

**Operation ID:** `list_controls_api_v2_compliance_controls_get`

**Description:**
List controls with optional filters.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `framework` | string/null | ⬜ No | query | Filter by framework |
| `control_family` | string/null | ⬜ No | query | Filter by control family |
| `priority` | string/null | ⬜ No | query | Filter by priority |
| `implementation_status` | string/null | ⬜ No | query | Filter by implementation status |
| `limit` | integer | ⬜ No | query | Maximum results |
| `include_system` | boolean | ⬜ No | query | Include SYSTEM controls |
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
curl -X GET "http://localhost:8000/api/v2/compliance/controls" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/compliance/controls

**Summary:** Create Control

**Operation ID:** `create_control_api_v2_compliance_controls_post`

**Description:**
Create a new compliance control.

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
  "control_id": "<control_id>",
  "control_number": "<control_number>",
  "framework": "<framework>",
  "title": "<title>",
  "description": "<description>",
  "control_family": "<control_family>",
  "priority": "<priority>",
  "implementation_status": "<implementation_status>",
  "control_type": "<control_type>",
  "automated": true
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "control_id": "<control_id>",
  "control_number": "<control_number>",
  "customer_id": "<customer_id>",
  "framework": "<framework>",
  "title": "<title>",
  "control_family": "<control_family>",
  "priority": "<priority>",
  "implementation_status": "<implementation_status>",
  "control_type": "<control_type>",
  "automated": true
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
curl -X POST "http://localhost:8000/api/v2/compliance/controls" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "control_id": "<control_id>",
  "control_number": "<control_number>",
  "framework": "<framework>",
  "title": "<title>",
  "description": "<description>",
  "control_family": "<control_family>",
  "priority": "<priority>",
  "implementation_status": "<implementation_status>",
  "control_type": "<control_type>",
  "automated": true
}' 
```

---

## GET /api/v2/compliance/controls/by-framework/{framework}

**Summary:** Get Controls By Framework

**Operation ID:** `get_controls_by_framework_api_v2_compliance_controls_by_framework__framework__get`

**Description:**
Get controls for a specific framework.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `framework` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/compliance/controls/by-framework/{framework}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/compliance/controls/search

**Summary:** Search Controls Semantic

**Operation ID:** `search_controls_semantic_api_v2_compliance_controls_search_post`

**Description:**
Semantic search controls.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `query` | string | ✅ Yes | query | Semantic search query |
| `framework` | string/null | ⬜ No | query | Filter by framework |
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
curl -X POST "http://localhost:8000/api/v2/compliance/controls/search" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## DELETE /api/v2/compliance/controls/{control_id}

**Summary:** Delete Control

**Operation ID:** `delete_control_api_v2_compliance_controls__control_id__delete`

**Description:**
Delete a control.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `control_id` | string | ✅ Yes | path |  |
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
curl -X DELETE "http://localhost:8000/api/v2/compliance/controls/{control_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/compliance/controls/{control_id}

**Summary:** Get Control

**Operation ID:** `get_control_api_v2_compliance_controls__control_id__get`

**Description:**
Get control by ID with customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `control_id` | string | ✅ Yes | path |  |
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
  "control_id": "<control_id>",
  "control_number": "<control_number>",
  "customer_id": "<customer_id>",
  "framework": "<framework>",
  "title": "<title>",
  "control_family": "<control_family>",
  "priority": "<priority>",
  "implementation_status": "<implementation_status>",
  "control_type": "<control_type>",
  "automated": true
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
curl -X GET "http://localhost:8000/api/v2/compliance/controls/{control_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## PUT /api/v2/compliance/controls/{control_id}

**Summary:** Update Control

**Operation ID:** `update_control_api_v2_compliance_controls__control_id__put`

**Description:**
Update an existing control.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `control_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "control_id": "<control_id>",
  "control_number": "<control_number>",
  "framework": "<framework>",
  "title": "<title>",
  "description": "<description>",
  "control_family": "<control_family>",
  "priority": "<priority>",
  "implementation_status": "<implementation_status>",
  "control_type": "<control_type>",
  "automated": true
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "control_id": "<control_id>",
  "control_number": "<control_number>",
  "customer_id": "<customer_id>",
  "framework": "<framework>",
  "title": "<title>",
  "control_family": "<control_family>",
  "priority": "<priority>",
  "implementation_status": "<implementation_status>",
  "control_type": "<control_type>",
  "automated": true
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
curl -X PUT "http://localhost:8000/api/v2/compliance/controls/{control_id}" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "control_id": "<control_id>",
  "control_number": "<control_number>",
  "framework": "<framework>",
  "title": "<title>",
  "description": "<description>",
  "control_family": "<control_family>",
  "priority": "<priority>",
  "implementation_status": "<implementation_status>",
  "control_type": "<control_type>",
  "automated": true
}' 
```

---

## GET /api/v2/compliance/dashboard/posture

**Summary:** Get Compliance Posture

**Operation ID:** `get_compliance_posture_api_v2_compliance_dashboard_posture_get`

**Description:**
Get compliance posture analysis.

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
  "overall_posture": "<overall_posture>",
  "risk_level": "<risk_level>",
  "top_gaps": [],
  "recommendations": [],
  "trend": "<trend>"
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
curl -X GET "http://localhost:8000/api/v2/compliance/dashboard/posture" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/compliance/dashboard/summary

**Summary:** Get Compliance Summary

**Operation ID:** `get_compliance_summary_api_v2_compliance_dashboard_summary_get`

**Description:**
Get compliance dashboard summary.

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
  "total_controls": 1,
  "implemented_controls": 1,
  "in_progress_controls": 1,
  "not_started_controls": 1,
  "total_assessments": 1,
  "total_gaps": 1,
  "critical_gaps": 1
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
curl -X GET "http://localhost:8000/api/v2/compliance/dashboard/summary" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/compliance/evidence

**Summary:** Upload Evidence

**Operation ID:** `upload_evidence_api_v2_compliance_evidence_post`

**Description:**
Upload compliance evidence.

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
  "evidence_id": "<evidence_id>",
  "control_id": "<control_id>",
  "evidence_type": "<evidence_type>",
  "title": "<title>",
  "collection_date": "<collection_date>"
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "evidence_id": "<evidence_id>",
  "customer_id": "<customer_id>",
  "control_id": "<control_id>",
  "evidence_type": "<evidence_type>",
  "title": "<title>",
  "collection_date": "<collection_date>",
  "is_expired": true
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
curl -X POST "http://localhost:8000/api/v2/compliance/evidence" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "evidence_id": "<evidence_id>",
  "control_id": "<control_id>",
  "evidence_type": "<evidence_type>",
  "title": "<title>",
  "collection_date": "<collection_date>"
}' 
```

---

## GET /api/v2/compliance/evidence/by-control/{control_id}

**Summary:** Get Evidence For Control

**Operation ID:** `get_evidence_for_control_api_v2_compliance_evidence_by_control__control_id__get`

**Description:**
Get evidence for a specific control.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `control_id` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/compliance/evidence/by-control/{control_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## DELETE /api/v2/compliance/evidence/{evidence_id}

**Summary:** Delete Evidence

**Operation ID:** `delete_evidence_api_v2_compliance_evidence__evidence_id__delete`

**Description:**
Delete evidence.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `evidence_id` | string | ✅ Yes | path |  |
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
curl -X DELETE "http://localhost:8000/api/v2/compliance/evidence/{evidence_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/compliance/evidence/{evidence_id}

**Summary:** Get Evidence

**Operation ID:** `get_evidence_api_v2_compliance_evidence__evidence_id__get`

**Description:**
Get evidence by ID with customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `evidence_id` | string | ✅ Yes | path |  |
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
  "evidence_id": "<evidence_id>",
  "customer_id": "<customer_id>",
  "control_id": "<control_id>",
  "evidence_type": "<evidence_type>",
  "title": "<title>",
  "collection_date": "<collection_date>",
  "is_expired": true
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
curl -X GET "http://localhost:8000/api/v2/compliance/evidence/{evidence_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/compliance/gaps

**Summary:** List Gaps

**Operation ID:** `list_gaps_api_v2_compliance_gaps_get`

**Description:**
List gaps with optional filters.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `control_id` | string/null | ⬜ No | query | Filter by control |
| `severity` | string/null | ⬜ No | query | Filter by severity |
| `status` | string/null | ⬜ No | query | Filter by status |
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
curl -X GET "http://localhost:8000/api/v2/compliance/gaps" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/compliance/gaps

**Summary:** Create Gap

**Operation ID:** `create_gap_api_v2_compliance_gaps_post`

**Description:**
Create a new compliance gap.

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
  "gap_id": "<gap_id>",
  "control_id": "<control_id>",
  "gap_type": "<gap_type>",
  "severity": "<severity>",
  "description": "<description>",
  "impact": "<impact>",
  "status": "<status>"
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "gap_id": "<gap_id>",
  "customer_id": "<customer_id>",
  "control_id": "<control_id>",
  "gap_type": "<gap_type>",
  "severity": "<severity>",
  "impact": "<impact>",
  "status": "<status>"
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
curl -X POST "http://localhost:8000/api/v2/compliance/gaps" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "gap_id": "<gap_id>",
  "control_id": "<control_id>",
  "gap_type": "<gap_type>",
  "severity": "<severity>",
  "description": "<description>",
  "impact": "<impact>",
  "status": "<status>"
}' 
```

---

## GET /api/v2/compliance/gaps/by-framework/{framework}

**Summary:** Get Gaps By Framework

**Operation ID:** `get_gaps_by_framework_api_v2_compliance_gaps_by_framework__framework__get`

**Description:**
Get gaps for a specific framework.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `framework` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/compliance/gaps/by-framework/{framework}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## PUT /api/v2/compliance/gaps/{gap_id}/remediate

**Summary:** Update Gap Remediation

**Operation ID:** `update_gap_remediation_api_v2_compliance_gaps__gap_id__remediate_put`

**Description:**
Update gap remediation status.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `gap_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "status": "<status>",
  "remediation_notes": "<remediation_notes>",
  "evidence_ids": []
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
curl -X PUT "http://localhost:8000/api/v2/compliance/gaps/{gap_id}/remediate" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "status": "<status>",
  "remediation_notes": "<remediation_notes>",
  "evidence_ids": []
}' 
```

---

## POST /api/v2/compliance/mappings

**Summary:** Create Mapping

**Operation ID:** `create_mapping_api_v2_compliance_mappings_post`

**Description:**
Create a new framework mapping.

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
  "source_framework": "<source_framework>",
  "source_control_id": "<source_control_id>",
  "target_framework": "<target_framework>",
  "target_control_id": "<target_control_id>",
  "relationship_type": "<relationship_type>",
  "confidence": 1
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "mapping_id": "<mapping_id>",
  "customer_id": "<customer_id>",
  "source_framework": "<source_framework>",
  "source_control_id": "<source_control_id>",
  "target_framework": "<target_framework>",
  "target_control_id": "<target_control_id>",
  "relationship_type": "<relationship_type>",
  "confidence": 1
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
curl -X POST "http://localhost:8000/api/v2/compliance/mappings" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "mapping_id": "<mapping_id>",
  "source_framework": "<source_framework>",
  "source_control_id": "<source_control_id>",
  "target_framework": "<target_framework>",
  "target_control_id": "<target_control_id>",
  "relationship_type": "<relationship_type>",
  "confidence": 1
}' 
```

---

## POST /api/v2/compliance/mappings/auto-map

**Summary:** Auto Generate Mappings

**Operation ID:** `auto_generate_mappings_api_v2_compliance_mappings_auto_map_post`

**Description:**
Auto-generate framework mappings using semantic similarity.

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
  "source_framework": "<source_framework>",
  "target_framework": "<target_framework>",
  "min_confidence": 1
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
curl -X POST "http://localhost:8000/api/v2/compliance/mappings/auto-map" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "source_framework": "<source_framework>",
  "target_framework": "<target_framework>",
  "min_confidence": 1
}' 
```

---

## GET /api/v2/compliance/mappings/between/{source}/{target}

**Summary:** Get Cross Framework Mappings

**Operation ID:** `get_cross_framework_mappings_api_v2_compliance_mappings_between__source___target__get`

**Description:**
Get cross-framework mappings.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `source` | string | ✅ Yes | path |  |
| `target` | string | ✅ Yes | path |  |
| `min_confidence` | integer | ⬜ No | query | Minimum confidence |
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
curl -X GET "http://localhost:8000/api/v2/compliance/mappings/between/{source}/{target}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/compliance/mappings/by-control/{control_id}

**Summary:** Get Mappings For Control

**Operation ID:** `get_mappings_for_control_api_v2_compliance_mappings_by_control__control_id__get`

**Description:**
Get all mappings for a control.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `control_id` | string | ✅ Yes | path |  |
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
curl -X GET "http://localhost:8000/api/v2/compliance/mappings/by-control/{control_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/compliance/mappings/{mapping_id}

**Summary:** Get Mapping

**Operation ID:** `get_mapping_api_v2_compliance_mappings__mapping_id__get`

**Description:**
Get mapping by ID with customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `mapping_id` | string | ✅ Yes | path |  |
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
  "mapping_id": "<mapping_id>",
  "customer_id": "<customer_id>",
  "source_framework": "<source_framework>",
  "source_control_id": "<source_control_id>",
  "target_framework": "<target_framework>",
  "target_control_id": "<target_control_id>",
  "relationship_type": "<relationship_type>",
  "confidence": 1
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
curl -X GET "http://localhost:8000/api/v2/compliance/mappings/{mapping_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## Phase B5: Alerts, Demographics & Economic APIs

**Total Endpoints:** 82


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

## Psychometric Assessment APIs

**Total Endpoints:** 8


## GET /api/v2/psychometrics/actors/by-trait/{trait_id}

**Summary:** Get Actors By Trait

**Operation ID:** `get_actors_by_trait_api_v2_psychometrics_actors_by_trait__trait_id__get`

**Description:**
Get all actors exhibiting a specific trait

Returns threat actors associated with the given trait

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `trait_id` | string | ✅ Yes | path |  |
| `limit` | integer | ⬜ No | query | Maximum number of results |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{}]
```

### 404 - Not found
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/actors/by-trait/{trait_id}"
```

---

## GET /api/v2/psychometrics/actors/{actor_id}/profile

**Summary:** Get Actor Profile

**Operation ID:** `get_actor_profile_api_v2_psychometrics_actors__actor_id__profile_get`

**Description:**
Get psychological profile for a threat actor

Returns all traits associated with the actor

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `actor_id` | string | ✅ Yes | path |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "actor_id": "<actor_id>",
  "actor_name": "<actor_name>",
  "traits": [],
  "dominant_traits": []
}
```

### 404 - Not found
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/actors/{actor_id}/profile"
```

---

## GET /api/v2/psychometrics/biases

**Summary:** List Biases

**Operation ID:** `list_biases_api_v2_psychometrics_biases_get`

**Description:**
List all cognitive biases

Returns all Cognitive_Bias nodes with optional filtering

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `category` | string/null | ⬜ No | query | Filter by category |
| `limit` | integer | ⬜ No | query | Maximum number of results |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{
  "bias_id": "<bias_id>",
  "name": "<name>"
}]
```

### 404 - Not found
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/biases"
```

---

## GET /api/v2/psychometrics/biases/{bias_id}

**Summary:** Get Bias Details

**Operation ID:** `get_bias_details_api_v2_psychometrics_biases__bias_id__get`

**Description:**
Get detailed information about a specific cognitive bias

Includes related actors and examples

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bias_id` | string | ✅ Yes | path |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 404 - Not found
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/biases/{bias_id}"
```

---

## GET /api/v2/psychometrics/dashboard

**Summary:** Get Dashboard

**Operation ID:** `get_dashboard_api_v2_psychometrics_dashboard_get`

**Description:**
Get psychometric dashboard statistics

Returns comprehensive overview of all psychometric data

### Parameters

No parameters required.

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_psych_traits": 1,
  "total_personality_traits": 1,
  "total_cognitive_biases": 1,
  "total_actor_profiles": 1,
  "top_traits": []
}
```

### 404 - Not found

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/dashboard"
```

---

## GET /api/v2/psychometrics/lacanian/registers

**Summary:** Get Lacanian Registers

**Operation ID:** `get_lacanian_registers_api_v2_psychometrics_lacanian_registers_get`

**Description:**
Get Lacanian psychoanalytic framework registers

Returns the three registers: Real, Imaginary, Symbolic with associated traits

### Parameters

No parameters required.

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{
  "register_type": "<register_type>",
  "description": "<description>",
  "traits": [],
  "count": 1
}]
```

### 404 - Not found

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/lacanian/registers"
```

---

## GET /api/v2/psychometrics/traits

**Summary:** List Traits

**Operation ID:** `list_traits_api_v2_psychometrics_traits_get`

**Description:**
List all psychological traits

Returns all PsychTrait nodes with optional filtering

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `category` | string/null | ⬜ No | query | Filter by category |
| `limit` | integer | ⬜ No | query | Maximum number of results |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{
  "trait_id": "<trait_id>",
  "name": "<name>"
}]
```

### 404 - Not found
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/traits"
```

---

## GET /api/v2/psychometrics/traits/{trait_id}

**Summary:** Get Trait Details

**Operation ID:** `get_trait_details_api_v2_psychometrics_traits__trait_id__get`

**Description:**
Get detailed information about a specific trait

Includes related actors and trait relationships

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `trait_id` | string | ✅ Yes | path |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 404 - Not found
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/traits/{trait_id}"
```

---

## Vendor & Equipment Management APIs

**Total Endpoints:** 23


## GET /api/v2/vendor-equipment/equipment

**Summary:** Search Equipment

**Operation ID:** `search_equipment_api_v2_vendor_equipment_equipment_get`

**Description:**
Search equipment with filters and customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `query` | string/null | ⬜ No | query | Search query |
| `vendor_id` | string/null | ⬜ No | query | Filter by vendor |
| `lifecycle_status` | string/null | ⬜ No | query | Filter by lifecycle status |
| `category` | string/null | ⬜ No | query | Filter by category |
| `criticality` | string/null | ⬜ No | query | Filter by criticality |
| `approaching_eol_days` | integer/null | ⬜ No | query | Find equipment within N days of EOL |
| `limit` | integer | ⬜ No | query | Maximum results |
| `include_system` | boolean | ⬜ No | query | Include SYSTEM equipment |
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/equipment" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/vendor-equipment/equipment

**Summary:** Create Equipment

**Operation ID:** `create_equipment_api_v2_vendor_equipment_equipment_post`

**Description:**
Create a new equipment model for the customer.

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
  "model_id": "<model_id>",
  "vendor_id": "<vendor_id>",
  "model_name": "<model_name>",
  "maintenance_schedule": "<maintenance_schedule>",
  "criticality": "<criticality>"
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "model_id": "<model_id>",
  "vendor_id": "<vendor_id>",
  "model_name": "<model_name>",
  "customer_id": "<customer_id>",
  "lifecycle_status": "<lifecycle_status>",
  "criticality": "<criticality>"
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
curl -X POST "http://localhost:8000/api/v2/vendor-equipment/equipment" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "model_id": "<model_id>",
  "vendor_id": "<vendor_id>",
  "model_name": "<model_name>",
  "maintenance_schedule": "<maintenance_schedule>",
  "criticality": "<criticality>"
}' 
```

---

## GET /api/v2/vendor-equipment/equipment/approaching-eol

**Summary:** Get Equipment Approaching Eol

**Operation ID:** `get_equipment_approaching_eol_api_v2_vendor_equipment_equipment_approaching_eol_get`

**Description:**
Get all equipment approaching EOL within specified days.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `days` | integer | ⬜ No | query | Days threshold for EOL |
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/equipment/approaching-eol" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/vendor-equipment/equipment/eol

**Summary:** Get Eol Equipment

**Operation ID:** `get_eol_equipment_api_v2_vendor_equipment_equipment_eol_get`

**Description:**
Get all equipment that has passed EOL.

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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/equipment/eol" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/vendor-equipment/equipment/{model_id}

**Summary:** Get Equipment

**Operation ID:** `get_equipment_api_v2_vendor_equipment_equipment__model_id__get`

**Description:**
Get equipment model by ID with customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `model_id` | string | ✅ Yes | path |  |
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
  "model_id": "<model_id>",
  "vendor_id": "<vendor_id>",
  "model_name": "<model_name>",
  "customer_id": "<customer_id>",
  "lifecycle_status": "<lifecycle_status>",
  "criticality": "<criticality>"
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/equipment/{model_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/vendor-equipment/maintenance-schedule

**Summary:** Get Maintenance Schedule

**Operation ID:** `get_maintenance_schedule_api_v2_vendor_equipment_maintenance_schedule_get`

**Description:**
Get prioritized maintenance schedule.

Prioritized by:
1. EOL proximity
2. Vulnerability count
3. Criticality

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `limit` | integer | ⬜ No | query | Maximum items |
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
  "total_items": 1,
  "items": []
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/maintenance-schedule" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/vendor-equipment/maintenance-windows

**Summary:** List Maintenance Windows

**Operation ID:** `list_maintenance_windows_api_v2_vendor_equipment_maintenance_windows_get`

**Description:**
List maintenance windows with optional filters.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `window_type` | string/null | ⬜ No | query | Filter by window type |
| `equipment_id` | string/null | ⬜ No | query | Filter by affected equipment |
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
  "windows": []
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/maintenance-windows" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/vendor-equipment/maintenance-windows

**Summary:** Create Maintenance Window

**Operation ID:** `create_maintenance_window_api_v2_vendor_equipment_maintenance_windows_post`

**Description:**
Create a new maintenance window.

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
  "window_id": "<window_id>",
  "name": "<name>",
  "window_type": "<window_type>",
  "start_time": "<start_time>",
  "end_time": "<end_time>",
  "affected_equipment_ids": []
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "window_id": "<window_id>",
  "name": "<name>",
  "customer_id": "<customer_id>",
  "window_type": "<window_type>",
  "start_time": "<start_time>",
  "end_time": "<end_time>",
  "affected_equipment_ids": [],
  "is_active": true
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
curl -X POST "http://localhost:8000/api/v2/vendor-equipment/maintenance-windows" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "window_id": "<window_id>",
  "name": "<name>",
  "window_type": "<window_type>",
  "start_time": "<start_time>",
  "end_time": "<end_time>",
  "affected_equipment_ids": []
}' 
```

---

## POST /api/v2/vendor-equipment/maintenance-windows/check-conflict

**Summary:** Check Maintenance Conflict

**Operation ID:** `check_maintenance_conflict_api_v2_vendor_equipment_maintenance_windows_check_conflict_post`

**Description:**
Check for scheduling conflicts with existing maintenance windows.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `proposed_start` | string | ✅ Yes | query | Proposed start time |
| `proposed_end` | string | ✅ Yes | query | Proposed end time |
| `equipment_ids` | array | ⬜ No | query | Equipment IDs to check |
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
  "has_conflict": true,
  "conflicting_windows": []
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
curl -X POST "http://localhost:8000/api/v2/vendor-equipment/maintenance-windows/check-conflict" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## DELETE /api/v2/vendor-equipment/maintenance-windows/{window_id}

**Summary:** Delete Maintenance Window

**Operation ID:** `delete_maintenance_window_api_v2_vendor_equipment_maintenance_windows__window_id__delete`

**Description:**
Delete a maintenance window.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `window_id` | string | ✅ Yes | path |  |
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
curl -X DELETE "http://localhost:8000/api/v2/vendor-equipment/maintenance-windows/{window_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/vendor-equipment/maintenance-windows/{window_id}

**Summary:** Get Maintenance Window

**Operation ID:** `get_maintenance_window_api_v2_vendor_equipment_maintenance_windows__window_id__get`

**Description:**
Get maintenance window by ID.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `window_id` | string | ✅ Yes | path |  |
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
  "window_id": "<window_id>",
  "name": "<name>",
  "customer_id": "<customer_id>",
  "window_type": "<window_type>",
  "start_time": "<start_time>",
  "end_time": "<end_time>",
  "affected_equipment_ids": [],
  "is_active": true
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/maintenance-windows/{window_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/vendor-equipment/predictive-maintenance/forecast

**Summary:** Get Maintenance Forecast

**Operation ID:** `get_maintenance_forecast_api_v2_vendor_equipment_predictive_maintenance_forecast_get`

**Description:**
Get comprehensive maintenance forecast.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `months_ahead` | integer | ⬜ No | query | Months ahead for forecast |
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
  "forecast_months": 1,
  "customer_id": "<customer_id>",
  "generated_at": "<generated_at>",
  "monthly_breakdown": []
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/predictive-maintenance/forecast" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/vendor-equipment/predictive-maintenance/{equipment_id}

**Summary:** Predict Maintenance

**Operation ID:** `predict_maintenance_api_v2_vendor_equipment_predictive_maintenance__equipment_id__get`

**Description:**
Get maintenance predictions for specific equipment.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `equipment_id` | string | ✅ Yes | path |  |
| `days_ahead` | integer | ⬜ No | query | Days ahead to predict |
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
  "total_predictions": 1,
  "customer_id": "<customer_id>",
  "predictions": []
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/predictive-maintenance/{equipment_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/vendor-equipment/vendors

**Summary:** Search Vendors

**Operation ID:** `search_vendors_api_v2_vendor_equipment_vendors_get`

**Description:**
Search vendors with filters and customer isolation.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `query` | string/null | ⬜ No | query | Search query |
| `risk_level` | string/null | ⬜ No | query | Filter by risk level |
| `min_risk_score` | number/null | ⬜ No | query | Minimum risk score |
| `support_status` | string/null | ⬜ No | query | Filter by support status |
| `supply_chain_tier` | integer/null | ⬜ No | query | Supply chain tier |
| `limit` | integer | ⬜ No | query | Maximum results |
| `include_system` | boolean | ⬜ No | query | Include SYSTEM vendors |
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/vendors" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/vendor-equipment/vendors

**Summary:** Create Vendor

**Operation ID:** `create_vendor_api_v2_vendor_equipment_vendors_post`

**Description:**
Create a new vendor for the customer.

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
  "vendor_id": "<vendor_id>",
  "name": "<name>",
  "support_status": "<support_status>",
  "industry_focus": [],
  "supply_chain_tier": 1
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "vendor_id": "<vendor_id>",
  "name": "<name>",
  "customer_id": "<customer_id>",
  "risk_level": "<risk_level>",
  "support_status": "<support_status>",
  "industry_focus": [],
  "supply_chain_tier": 1,
  "total_cves": 1
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
curl -X POST "http://localhost:8000/api/v2/vendor-equipment/vendors" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "vendor_id": "<vendor_id>",
  "name": "<name>",
  "support_status": "<support_status>",
  "industry_focus": [],
  "supply_chain_tier": 1
}' 
```

---

## GET /api/v2/vendor-equipment/vendors/high-risk

**Summary:** Get High Risk Vendors

**Operation ID:** `get_high_risk_vendors_api_v2_vendor_equipment_vendors_high_risk_get`

**Description:**
Get all vendors with high risk scores.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `min_risk_score` | number | ⬜ No | query | Minimum risk score threshold |
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/vendors/high-risk" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/vendor-equipment/vendors/{vendor_id}

**Summary:** Get Vendor

**Operation ID:** `get_vendor_api_v2_vendor_equipment_vendors__vendor_id__get`

**Description:**
Get vendor by ID with customer isolation.

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
  "name": "<name>",
  "customer_id": "<customer_id>",
  "risk_level": "<risk_level>",
  "support_status": "<support_status>",
  "industry_focus": [],
  "supply_chain_tier": 1,
  "total_cves": 1
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/vendors/{vendor_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/vendor-equipment/vulnerabilities/flag

**Summary:** Flag Vendor Vulnerability

**Operation ID:** `flag_vendor_vulnerability_api_v2_vendor_equipment_vulnerabilities_flag_post`

**Description:**
Flag a supply chain vulnerability affecting a vendor.

All equipment from the affected vendor will be flagged.
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
  "vendor_id": "<vendor_id>",
  "cve_id": "<cve_id>",
  "description": "<description>"
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "vendor_id": "<vendor_id>",
  "cve_id": "<cve_id>",
  "affected_equipment_count": 1,
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
curl -X POST "http://localhost:8000/api/v2/vendor-equipment/vulnerabilities/flag" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "vendor_id": "<vendor_id>",
  "cve_id": "<cve_id>",
  "description": "<description>"
}' 
```

---

## GET /api/v2/vendor-equipment/work-orders

**Summary:** List Work Orders

**Operation ID:** `list_work_orders_api_v2_vendor_equipment_work_orders_get`

**Description:**
List work orders with optional filters.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `status` | string/null | ⬜ No | query | Filter by status |
| `priority` | string/null | ⬜ No | query | Filter by priority |
| `equipment_id` | string/null | ⬜ No | query | Filter by equipment |
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
  "work_orders": []
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/work-orders" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## POST /api/v2/vendor-equipment/work-orders

**Summary:** Create Work Order

**Operation ID:** `create_work_order_api_v2_vendor_equipment_work_orders_post`

**Description:**
Create a new work order.

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
  "equipment_id": "<equipment_id>",
  "equipment_name": "<equipment_name>",
  "title": "<title>",
  "priority": "<priority>",
  "scheduled_start": "<scheduled_start>",
  "scheduled_end": "<scheduled_end>"
}
```

### Responses

### 201 - Successful Response

**Response Body:**
```json
{
  "work_order_id": "<work_order_id>",
  "customer_id": "<customer_id>",
  "equipment_id": "<equipment_id>",
  "equipment_name": "<equipment_name>",
  "title": "<title>",
  "priority": "<priority>",
  "status": "<status>",
  "scheduled_start": "<scheduled_start>",
  "scheduled_end": "<scheduled_end>",
  "is_overdue": true
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
curl -X POST "http://localhost:8000/api/v2/vendor-equipment/work-orders" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "equipment_id": "<equipment_id>",
  "equipment_name": "<equipment_name>",
  "title": "<title>",
  "priority": "<priority>",
  "scheduled_start": "<scheduled_start>",
  "scheduled_end": "<scheduled_end>"
}' 
```

---

## GET /api/v2/vendor-equipment/work-orders/summary

**Summary:** Get Work Order Summary

**Operation ID:** `get_work_order_summary_api_v2_vendor_equipment_work_orders_summary_get`

**Description:**
Get work order summary with status and priority breakdowns.

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
  "total": 1,
  "overdue_count": 1
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/work-orders/summary" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## GET /api/v2/vendor-equipment/work-orders/{work_order_id}

**Summary:** Get Work Order

**Operation ID:** `get_work_order_api_v2_vendor_equipment_work_orders__work_order_id__get`

**Description:**
Get work order by ID.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `work_order_id` | string | ✅ Yes | path |  |
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
  "work_order_id": "<work_order_id>",
  "customer_id": "<customer_id>",
  "equipment_id": "<equipment_id>",
  "equipment_name": "<equipment_name>",
  "title": "<title>",
  "priority": "<priority>",
  "status": "<status>",
  "scheduled_start": "<scheduled_start>",
  "scheduled_end": "<scheduled_end>",
  "is_overdue": true
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
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/work-orders/{work_order_id}" \
  -H "x-customer-id: <your_x_customer_id>"
```

---

## PATCH /api/v2/vendor-equipment/work-orders/{work_order_id}/status

**Summary:** Update Work Order Status

**Operation ID:** `update_work_order_status_api_v2_vendor_equipment_work_orders__work_order_id__status_patch`

**Description:**
Update work order status.

Requires WRITE access level.

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `work_order_id` | string | ✅ Yes | path |  |
| `x-customer-id` | string | ✅ Yes | header | Customer identifier |
| `x-namespace` | string/null | ⬜ No | header | Customer namespace |
| `x-user-id` | string/null | ⬜ No | header | User identifier |
| `x-access-level` | string/null | ⬜ No | header | Access level |

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
{
  "work_order_id": "<work_order_id>",
  "customer_id": "<customer_id>",
  "equipment_id": "<equipment_id>",
  "equipment_name": "<equipment_name>",
  "title": "<title>",
  "priority": "<priority>",
  "status": "<status>",
  "scheduled_start": "<scheduled_start>",
  "scheduled_end": "<scheduled_end>",
  "is_overdue": true
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
curl -X PATCH "http://localhost:8000/api/v2/vendor-equipment/work-orders/{work_order_id}/status" \
  -H "x-customer-id: <your_x_customer_id>" \
  -H "Content-Type: application/json" \
  -d '{
  "status": "<status>"
}' 
```

---

## System & Utility APIs

**Total Endpoints:** 5


## GET /health

**Summary:** Health Check

**Operation ID:** `health_check_health_get`

**Description:**
Health check endpoint with service status and model validation.

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
curl -X GET "http://localhost:8000/health"
```

---

## GET /info

**Summary:** Model Info

**Operation ID:** `model_info_info_get`

**Description:**
Model information and capabilities.

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
curl -X GET "http://localhost:8000/info"
```

---

## POST /ner

**Summary:** Extract Entities

**Operation ID:** `extract_entities_ner_post`

**Description:**
Extract named entities from text using enhanced multi-layer NER approach.

Strategy (in priority order):
1. Pattern-based extraction (HIGH confidence for CVE, APT, MITRE patterns)
2. Fallback model (en_core_web_trf) for general NER
3. Custom NER11 model for cybersecurity-specific entities

The pattern-based extraction addresses the context-dependency issue where
transformer models require longer context to identify short entities like
"APT29", "CVE-2024-12345", or "T1566".

### Parameters

No parameters required.

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "text": "<text>"
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "entities": [],
  "doc_length": 1
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
curl -X POST "http://localhost:8000/ner" \
  -H "Content-Type: application/json" \
  -d '{
  "text": "<text>"
}' 
```

---

## POST /search/hybrid

**Summary:** Hybrid Search

**Operation ID:** `hybrid_search_search_hybrid_post`

**Description:**
Hybrid search combining semantic similarity (Qdrant) with graph expansion (Neo4j).

This is the core Phase 3 feature that provides:
1. Semantic search via Qdrant vector similarity
2. Graph expansion via Neo4j relationship traversal
3. Re-ranking based on combined scores
4. Hierarchical filtering (Tier 1 + Tier 2)

Example usage:
```
POST /search/hybrid
{
    "query": "APT29 ransomware attack",
    "expand_graph": true,
    "hop_depth": 2,
    "relationship_types": ["USES", "TARGETS", "ATTRIBUTED_TO"]
}
```

Returns entities with their graph context and related entities.
Performance target: <500ms.

### Parameters

No parameters required.

### Request Body

**Content-Type:** `application/json`

**Schema:**
```json
{
  "query": "<query>",
  "limit": 1,
  "expand_graph": true,
  "hop_depth": 1
}
```

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "results": [],
  "query": "<query>",
  "total_semantic_results": 1,
  "total_graph_entities": 1,
  "graph_expansion_enabled": true,
  "hop_depth": 1
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
curl -X POST "http://localhost:8000/search/hybrid" \
  -H "Content-Type: application/json" \
  -d '{
  "query": "<query>",
  "limit": 1,
  "expand_graph": true,
  "hop_depth": 1
}' 
```

---

## POST /search/semantic

**Summary:** Semantic Search

**Operation ID:** `semantic_search_search_semantic_post`

**Description:**
Semantic search with hierarchical filtering (Task 1.5).

Search entities using semantic similarity with hierarchical taxonomy filtering:
- Tier 1 filtering: label_filter (60 NER labels)
- Tier 2 filtering: fine_grained_filter (566 fine-grained types) - KEY FEATURE
- Confidence filtering: confidence_threshold

Example queries:
- "ransomware attack" → Find semantically similar malware entities
- "SCADA systems" with fine_grained_filter="SCADA_SERVER" → Precise infrastructure search
- "threat actors" with label_filter="THREAT_ACTOR" → Category-filtered search

Returns results with complete hierarchy_path for each entity.

### Parameters

No parameters required.

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
  "query": "<query>",
  "total_results": 1
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
curl -X POST "http://localhost:8000/search/semantic" \
  -H "Content-Type: application/json" \
  -d '{
  "query": "<query>",
  "limit": 1
}' 
```

---
