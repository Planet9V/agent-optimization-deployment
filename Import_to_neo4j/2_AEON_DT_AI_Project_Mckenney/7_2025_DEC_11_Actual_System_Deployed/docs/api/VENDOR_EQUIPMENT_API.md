# Vendor & Equipment Management APIs

**Total Endpoints:** 23

**Base URL:** `http://localhost:8000`

---

## Table of Contents

1. [POST /api/v2/vendor-equipment/vendors](#post--api-v2-vendor-equipment-vendors): Create Vendor
2. [GET /api/v2/vendor-equipment/vendors](#get--api-v2-vendor-equipment-vendors): Search Vendors
3. [GET /api/v2/vendor-equipment/vendors/{vendor_id}](#get--api-v2-vendor-equipment-vendors-vendor_id): Get Vendor
4. [GET /api/v2/vendor-equipment/vendors/high-risk](#get--api-v2-vendor-equipment-vendors-high-risk): Get High Risk Vendors
5. [POST /api/v2/vendor-equipment/equipment](#post--api-v2-vendor-equipment-equipment): Create Equipment
6. [GET /api/v2/vendor-equipment/equipment](#get--api-v2-vendor-equipment-equipment): Search Equipment
7. [GET /api/v2/vendor-equipment/equipment/{model_id}](#get--api-v2-vendor-equipment-equipment-model_id): Get Equipment
8. [GET /api/v2/vendor-equipment/equipment/approaching-eol](#get--api-v2-vendor-equipment-equipment-approaching-eol): Get Equipment Approaching Eol
9. [GET /api/v2/vendor-equipment/equipment/eol](#get--api-v2-vendor-equipment-equipment-eol): Get Eol Equipment
10. [GET /api/v2/vendor-equipment/maintenance-schedule](#get--api-v2-vendor-equipment-maintenance-schedule): Get Maintenance Schedule
11. [POST /api/v2/vendor-equipment/vulnerabilities/flag](#post--api-v2-vendor-equipment-vulnerabilities-flag): Flag Vendor Vulnerability
12. [POST /api/v2/vendor-equipment/maintenance-windows](#post--api-v2-vendor-equipment-maintenance-windows): Create Maintenance Window
13. [GET /api/v2/vendor-equipment/maintenance-windows](#get--api-v2-vendor-equipment-maintenance-windows): List Maintenance Windows
14. [GET /api/v2/vendor-equipment/maintenance-windows/{window_id}](#get--api-v2-vendor-equipment-maintenance-windows-window_id): Get Maintenance Window
15. [DELETE /api/v2/vendor-equipment/maintenance-windows/{window_id}](#delete--api-v2-vendor-equipment-maintenance-windows-window_id): Delete Maintenance Window
16. [POST /api/v2/vendor-equipment/maintenance-windows/check-conflict](#post--api-v2-vendor-equipment-maintenance-windows-check-conflict): Check Maintenance Conflict
17. [GET /api/v2/vendor-equipment/predictive-maintenance/{equipment_id}](#get--api-v2-vendor-equipment-predictive-maintenance-equipment_id): Predict Maintenance
18. [GET /api/v2/vendor-equipment/predictive-maintenance/forecast](#get--api-v2-vendor-equipment-predictive-maintenance-forecast): Get Maintenance Forecast
19. [POST /api/v2/vendor-equipment/work-orders](#post--api-v2-vendor-equipment-work-orders): Create Work Order
20. [GET /api/v2/vendor-equipment/work-orders](#get--api-v2-vendor-equipment-work-orders): List Work Orders
21. [GET /api/v2/vendor-equipment/work-orders/{work_order_id}](#get--api-v2-vendor-equipment-work-orders-work_order_id): Get Work Order
22. [PATCH /api/v2/vendor-equipment/work-orders/{work_order_id}/status](#patch--api-v2-vendor-equipment-work-orders-work_order_id-status): Update Work Order Status
23. [GET /api/v2/vendor-equipment/work-orders/summary](#get--api-v2-vendor-equipment-work-orders-summary): Get Work Order Summary

---

# Endpoint Details


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
