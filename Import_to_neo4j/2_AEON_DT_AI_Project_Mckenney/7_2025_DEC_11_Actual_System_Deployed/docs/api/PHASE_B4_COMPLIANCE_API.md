# Phase B4 - Compliance & Audit APIs

**Total Endpoints:** 28

**Base URL:** `http://localhost:8000`

---

## Table of Contents

1. [POST /api/v2/compliance/controls](#post--api-v2-compliance-controls): Create Control
2. [GET /api/v2/compliance/controls](#get--api-v2-compliance-controls): List Controls
3. [GET /api/v2/compliance/controls/{control_id}](#get--api-v2-compliance-controls-control_id): Get Control
4. [PUT /api/v2/compliance/controls/{control_id}](#put--api-v2-compliance-controls-control_id): Update Control
5. [DELETE /api/v2/compliance/controls/{control_id}](#delete--api-v2-compliance-controls-control_id): Delete Control
6. [GET /api/v2/compliance/controls/by-framework/{framework}](#get--api-v2-compliance-controls-by-framework-framework): Get Controls By Framework
7. [POST /api/v2/compliance/controls/search](#post--api-v2-compliance-controls-search): Search Controls Semantic
8. [POST /api/v2/compliance/mappings](#post--api-v2-compliance-mappings): Create Mapping
9. [GET /api/v2/compliance/mappings/{mapping_id}](#get--api-v2-compliance-mappings-mapping_id): Get Mapping
10. [GET /api/v2/compliance/mappings/between/{source}/{target}](#get--api-v2-compliance-mappings-between-source-target): Get Cross Framework Mappings
11. [GET /api/v2/compliance/mappings/by-control/{control_id}](#get--api-v2-compliance-mappings-by-control-control_id): Get Mappings For Control
12. [POST /api/v2/compliance/mappings/auto-map](#post--api-v2-compliance-mappings-auto-map): Auto Generate Mappings
13. [POST /api/v2/compliance/assessments](#post--api-v2-compliance-assessments): Create Assessment
14. [GET /api/v2/compliance/assessments](#get--api-v2-compliance-assessments): List Assessments
15. [GET /api/v2/compliance/assessments/{assessment_id}](#get--api-v2-compliance-assessments-assessment_id): Get Assessment
16. [PUT /api/v2/compliance/assessments/{assessment_id}](#put--api-v2-compliance-assessments-assessment_id): Update Assessment
17. [GET /api/v2/compliance/assessments/by-framework/{framework}](#get--api-v2-compliance-assessments-by-framework-framework): Get Assessments By Framework
18. [POST /api/v2/compliance/assessments/{assessment_id}/complete](#post--api-v2-compliance-assessments-assessment_id-complete): Complete Assessment
19. [POST /api/v2/compliance/evidence](#post--api-v2-compliance-evidence): Upload Evidence
20. [GET /api/v2/compliance/evidence/{evidence_id}](#get--api-v2-compliance-evidence-evidence_id): Get Evidence
21. [DELETE /api/v2/compliance/evidence/{evidence_id}](#delete--api-v2-compliance-evidence-evidence_id): Delete Evidence
22. [GET /api/v2/compliance/evidence/by-control/{control_id}](#get--api-v2-compliance-evidence-by-control-control_id): Get Evidence For Control
23. [POST /api/v2/compliance/gaps](#post--api-v2-compliance-gaps): Create Gap
24. [GET /api/v2/compliance/gaps](#get--api-v2-compliance-gaps): List Gaps
25. [GET /api/v2/compliance/gaps/by-framework/{framework}](#get--api-v2-compliance-gaps-by-framework-framework): Get Gaps By Framework
26. [PUT /api/v2/compliance/gaps/{gap_id}/remediate](#put--api-v2-compliance-gaps-gap_id-remediate): Update Gap Remediation
27. [GET /api/v2/compliance/dashboard/summary](#get--api-v2-compliance-dashboard-summary): Get Compliance Summary
28. [GET /api/v2/compliance/dashboard/posture](#get--api-v2-compliance-dashboard-posture): Get Compliance Posture

---

# Endpoint Details


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
