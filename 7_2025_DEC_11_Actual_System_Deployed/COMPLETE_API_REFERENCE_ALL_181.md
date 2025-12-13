# COMPLETE API REFERENCE - ALL 181 ENDPOINTS

**Generated**: 2025-12-12T06:37:54.407420
**Base URL**: http://localhost:8000

## API Statistics

- **Phase B APIs**: 135 endpoints
- **NER APIs**: 5 endpoints
- **Next.js APIs**: 41 endpoints
- **TOTAL**: 181 endpoints

### Phase B APIs by Domain

- **Remediation**: 29 endpoints
- **Risk**: 24 endpoints
- **Sbom**: 32 endpoints
- **Threat Intel**: 26 endpoints
- **Vendor Equipment**: 24 endpoints

## Authentication

All Phase B APIs require the `x-customer-id` header:
```
curl -H "x-customer-id: dev" ...
```

---

# PHASE B APIs


## REMEDIATION APIs

**Total Endpoints**: 29


### 1. GET /api/v2/remediation/dashboard/summary

**Summary**: Get Dashboard Summary

**Description**: Get remediation dashboard summary.

Returns comprehensive dashboard data for remediation overview.

**Parameters**:
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/dashboard/summary" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Dashboard Summary

---


### 2. GET /api/v2/remediation/dashboard/workload

**Summary**: Get Workload Distribution

**Description**: Get team workload distribution.

Returns task distribution by assignee and team.

**Parameters**:
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/dashboard/workload" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Workload Distribution

---


### 3. GET /api/v2/remediation/metrics/backlog

**Summary**: Get Backlog Metrics

**Description**: Get vulnerability backlog metrics.

Returns backlog size and trend.

**Parameters**:
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/metrics/backlog" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Backlog Metrics

---


### 4. GET /api/v2/remediation/metrics/mttr

**Summary**: Get Mttr By Severity

**Description**: Get Mean Time To Remediate by severity.

Returns average remediation time for each severity level.

**Parameters**:
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/metrics/mttr" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Mttr By Severity

---


### 5. GET /api/v2/remediation/metrics/sla-compliance

**Summary**: Get Sla Compliance

**Description**: Get SLA compliance rate.

Returns percentage of tasks completed within SLA.

**Parameters**:
- `period_days` (query) (optional): integer
  - Period in days
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/metrics/sla-compliance" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Sla Compliance

---


### 6. GET /api/v2/remediation/metrics/summary

**Summary**: Get Metrics Summary

**Description**: Get remediation metrics summary.

Returns overall remediation performance metrics.

**Parameters**:
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/metrics/summary" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Metrics Summary

---


### 7. GET /api/v2/remediation/metrics/trends

**Summary**: Get Remediation Trends

**Description**: Get remediation trends over time.

Returns time-series metrics for the specified period.

**Parameters**:
- `period_days` (query) (optional): integer
  - Period in days
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/metrics/trends" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Remediation Trends

---


### 8. POST /api/v2/remediation/plans

**Summary**: Create Plan

**Description**: Create a remediation plan.

Creates a plan to coordinate multiple remediation tasks.

**Parameters**:
- `X-Customer-ID` (header) (required): string

**Request Body**:
(required)

```
Reference: #/components/schemas/CreatePlanRequest
```

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/remediation/plans" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Plan

---


### 9. GET /api/v2/remediation/plans

**Summary**: List Plans

**Description**: List all remediation plans.

Returns plans with optional status filter.

**Parameters**:
- `status` (query) (optional): string
  - Filter by status
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Array of:
    Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/plans" \
  -H "x-customer-id: dev"
```

**Use Case**: 
List Plans

---


### 10. GET /api/v2/remediation/plans/active

**Summary**: Get Active Plans

**Description**: Get active remediation plans.

Returns plans with status ACTIVE.

**Parameters**:
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Array of:
    Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/plans/active" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Active Plans

---


### 11. GET /api/v2/remediation/plans/{plan_id}

**Summary**: Get Plan

**Description**: Get plan details by ID.

Returns detailed information about a remediation plan.

**Parameters**:
- `plan_id` (path) (required): string
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/plans/plan-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Plan

---


### 12. GET /api/v2/remediation/plans/{plan_id}/progress

**Summary**: Get Plan Progress

**Description**: Get plan progress metrics.

Returns completion percentage and task status breakdown.

**Parameters**:
- `plan_id` (path) (required): string
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/plans/plan-123/progress" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Plan Progress

---


### 13. PUT /api/v2/remediation/plans/{plan_id}/status

**Summary**: Update Plan Status

**Description**: Update plan status.

Changes plan status (DRAFT, ACTIVE, COMPLETED, CANCELLED).

**Parameters**:
- `plan_id` (path) (required): string
- `X-Customer-ID` (header) (required): string

**Request Body**:
(required)

```
Reference: #/components/schemas/UpdatePlanStatusRequest
```

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X PUT "http://localhost:8000/api/v2/remediation/plans/plan-123/status" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Update Plan Status

---


### 14. GET /api/v2/remediation/sla/at-risk

**Summary**: Get At Risk Tasks

**Description**: Get tasks at risk of SLA breach.

Returns tasks with less than 20% time remaining.

**Parameters**:
- `limit` (query) (optional): integer
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Array of:
    Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/sla/at-risk" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get At Risk Tasks

---


### 15. GET /api/v2/remediation/sla/breaches

**Summary**: Get Sla Breaches

**Description**: Get SLA breaches.

Returns tasks that have breached SLA deadlines.

**Parameters**:
- `limit` (query) (optional): integer
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Array of:
    Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/sla/breaches" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Sla Breaches

---


### 16. POST /api/v2/remediation/sla/policies

**Summary**: Create Sla Policy

**Description**: Create SLA policy.

Defines remediation SLA thresholds by severity.

**Parameters**:
- `X-Customer-ID` (header) (required): string

**Request Body**:
(required)

```
Reference: #/components/schemas/CreateSLAPolicyRequest
```

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/remediation/sla/policies" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Sla Policy

---


### 17. GET /api/v2/remediation/sla/policies

**Summary**: List Sla Policies

**Description**: List SLA policies.

Returns all SLA policies for the customer.

**Parameters**:
- `active_only` (query) (optional): boolean
  - Return only active policies
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Array of:
    Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/sla/policies" \
  -H "x-customer-id: dev"
```

**Use Case**: 
List Sla Policies

---


### 18. GET /api/v2/remediation/sla/policies/{policy_id}

**Summary**: Get Sla Policy

**Description**: Get SLA policy by ID.

Returns detailed SLA policy configuration.

**Parameters**:
- `policy_id` (path) (required): string
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/sla/policies/policy-789" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Sla Policy

---


### 19. PUT /api/v2/remediation/sla/policies/{policy_id}

**Summary**: Update Sla Policy

**Description**: Update SLA policy.

Modifies SLA policy configuration.

**Parameters**:
- `policy_id` (path) (required): string
- `X-Customer-ID` (header) (required): string

**Request Body**:
(required)

```
Reference: #/components/schemas/UpdateSLAPolicyRequest
```

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X PUT "http://localhost:8000/api/v2/remediation/sla/policies/policy-789" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Update Sla Policy

---


### 20. POST /api/v2/remediation/tasks

**Summary**: Create Task

**Description**: Create a new remediation task.

Creates a remediation task for vulnerability remediation with SLA tracking.

**Parameters**:
- `X-Customer-ID` (header) (required): string

**Request Body**:
(required)

```
Reference: #/components/schemas/CreateTaskRequest
```

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/remediation/tasks" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Task

---


### 21. GET /api/v2/remediation/tasks/by-priority/{priority}

**Summary**: Get Tasks By Priority

**Description**: Get tasks by priority level.

Returns all tasks with the specified priority (critical, high, medium, low, emergency).

**Parameters**:
- `priority` (path) (required): string
- `limit` (query) (optional): integer
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Array of:
    Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/by-priority/high" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Tasks By Priority

---


### 22. GET /api/v2/remediation/tasks/by-status/{status}

**Summary**: Get Tasks By Status

**Description**: Get tasks by status.

Returns all tasks with the specified status.

**Parameters**:
- `status` (path) (required): string
- `limit` (query) (optional): integer
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Array of:
    Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/by-status/open" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Tasks By Status

---


### 23. GET /api/v2/remediation/tasks/open

**Summary**: Get Open Tasks

**Description**: Get all open tasks.

Returns tasks that are not completed (open, in_progress, pending_verification).

**Parameters**:
- `limit` (query) (optional): integer
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Array of:
    Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/open" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Open Tasks

---


### 24. GET /api/v2/remediation/tasks/overdue

**Summary**: Get Overdue Tasks

**Description**: Get overdue tasks.

Returns tasks that have breached their SLA deadline.

**Parameters**:
- `limit` (query) (optional): integer
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Array of:
    Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/overdue" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Overdue Tasks

---


### 25. GET /api/v2/remediation/tasks/search

**Summary**: Search Tasks

**Description**: Search remediation tasks.

Search tasks with optional filters and semantic search.

**Parameters**:
- `query` (query) (optional): string
  - Search query
- `status` (query) (optional): string
  - Filter by status
- `priority` (query) (optional): string
  - Filter by priority
- `assigned_to` (query) (optional): string
  - Filter by assignee
- `limit` (query) (optional): integer
  - Maximum results
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Array of:
    Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/search" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Search Tasks

---


### 26. GET /api/v2/remediation/tasks/{task_id}

**Summary**: Get Task

**Description**: Get task details by ID.

Returns detailed information about a specific remediation task.

**Parameters**:
- `task_id` (path) (required): string
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/task-456" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Task

---


### 27. PUT /api/v2/remediation/tasks/{task_id}/assign

**Summary**: Assign Task

**Description**: Assign task to user or team.

Updates task assignment with audit trail.

**Parameters**:
- `task_id` (path) (required): string
- `X-Customer-ID` (header) (required): string

**Request Body**:
(required)

```
Reference: #/components/schemas/AssignTaskRequest
```

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X PUT "http://localhost:8000/api/v2/remediation/tasks/task-456/assign" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Assign Task

---


### 28. GET /api/v2/remediation/tasks/{task_id}/history

**Summary**: Get Task History

**Description**: Get task action history.

Returns complete audit trail for a task.

**Parameters**:
- `task_id` (path) (required): string
- `X-Customer-ID` (header) (required): string

**Responses**:
- **200**: Successful Response
```
  Array of:
    Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/remediation/tasks/task-456/history" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Task History

---


### 29. PUT /api/v2/remediation/tasks/{task_id}/status

**Summary**: Update Task Status

**Description**: Update task status.

Changes task status with audit trail recording.

**Parameters**:
- `task_id` (path) (required): string
- `X-Customer-ID` (header) (required): string

**Request Body**:
(required)

```
Reference: #/components/schemas/UpdateStatusRequest
```

**Responses**:
- **200**: Successful Response
```
  Object (properties not detailed)
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X PUT "http://localhost:8000/api/v2/remediation/tasks/task-456/status" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Update Task Status

---


## RISK APIs

**Total Endpoints**: 24


### 1. GET /api/v2/risk/aggregation/by-asset-type

**Summary**: Get Risk By Asset Type

**Description**: Get risk aggregated by asset type.

**Parameters**:
- `asset_type` (query) (optional): string
  - Specific asset type
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Array of:
    Reference: #/components/schemas/RiskAggregationResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/aggregation/by-asset-type" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Risk By Asset Type

---


### 2. GET /api/v2/risk/aggregation/by-sector

**Summary**: Get Risk By Sector

**Description**: Get risk aggregated by sector.

**Parameters**:
- `sector` (query) (optional): string
  - Specific sector
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Array of:
    Reference: #/components/schemas/RiskAggregationResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/aggregation/by-sector" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Risk By Sector

---


### 3. GET /api/v2/risk/aggregation/by-vendor

**Summary**: Get Risk By Vendor

**Description**: Get risk aggregated by vendor.

**Parameters**:
- `vendor_id` (query) (optional): string
  - Specific vendor ID
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Array of:
    Reference: #/components/schemas/RiskAggregationResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/aggregation/by-vendor" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Risk By Vendor

---


### 4. GET /api/v2/risk/aggregation/{aggregation_type}/{group_id}

**Summary**: Get Risk Aggregation

**Description**: Get specific risk aggregation.

**Parameters**:
- `aggregation_type` (path) (required): string
- `group_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/RiskAggregationResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/aggregation/sector/financial" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Risk Aggregation

---


### 5. GET /api/v2/risk/assets/by-criticality/{level}

**Summary**: Get Assets By Criticality

**Description**: Get assets by criticality level.

**Parameters**:
- `level` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/AssetCriticalityListResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/assets/by-criticality/critical" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Assets By Criticality

---


### 6. POST /api/v2/risk/assets/criticality

**Summary**: Set Asset Criticality

**Description**: Set asset criticality rating.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/AssetCriticalityCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/AssetCriticalityResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/risk/assets/criticality" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Set Asset Criticality

---


### 7. GET /api/v2/risk/assets/criticality/summary

**Summary**: Get Criticality Summary

**Description**: Get criticality distribution summary.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/CriticalitySummaryResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/assets/criticality/summary" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Criticality Summary

---


### 8. GET /api/v2/risk/assets/mission-critical

**Summary**: Get Mission Critical Assets

**Description**: Get all mission-critical assets.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/AssetCriticalityListResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/assets/mission-critical" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Mission Critical Assets

---


### 9. GET /api/v2/risk/assets/{asset_id}/criticality

**Summary**: Get Asset Criticality

**Description**: Get asset criticality rating with customer isolation.

**Parameters**:
- `asset_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/AssetCriticalityResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/assets/asset-123/criticality" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Asset Criticality

---


### 10. PUT /api/v2/risk/assets/{asset_id}/criticality

**Summary**: Update Asset Criticality

**Description**: Update asset criticality rating.

Requires WRITE access level.

**Parameters**:
- `asset_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/AssetCriticalityCreate
```

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/AssetCriticalityResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X PUT "http://localhost:8000/api/v2/risk/assets/asset-123/criticality" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Update Asset Criticality

---


### 11. GET /api/v2/risk/dashboard/risk-matrix

**Summary**: Get Risk Matrix

**Description**: Get risk matrix data (likelihood vs impact).

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/RiskMatrixResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/dashboard/risk-matrix" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Risk Matrix

---


### 12. GET /api/v2/risk/dashboard/summary

**Summary**: Get Dashboard Summary

**Description**: Get comprehensive risk dashboard summary.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/api__risk_scoring__risk_router__DashboardSummaryResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/dashboard/summary" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Dashboard Summary

---


### 13. POST /api/v2/risk/exposure

**Summary**: Calculate Exposure Score

**Description**: Calculate exposure score for asset.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/ExposureScoreCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/ExposureScoreResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/risk/exposure" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Calculate Exposure Score

---


### 14. GET /api/v2/risk/exposure/attack-surface

**Summary**: Get Attack Surface Summary

**Description**: Get attack surface summary.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/AttackSurfaceSummaryResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/exposure/attack-surface" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Attack Surface Summary

---


### 15. GET /api/v2/risk/exposure/high-exposure

**Summary**: Get High Exposure Assets

**Description**: Get assets with high exposure scores.

**Parameters**:
- `min_score` (query) (optional): number
  - Minimum exposure score
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ExposureScoreListResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/exposure/high-exposure" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get High Exposure Assets

---


### 16. GET /api/v2/risk/exposure/internet-facing

**Summary**: Get Internet Facing Assets

**Description**: Get all internet-facing assets.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ExposureScoreListResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/exposure/internet-facing" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Internet Facing Assets

---


### 17. GET /api/v2/risk/exposure/{asset_id}

**Summary**: Get Exposure Score

**Description**: Get asset exposure score with customer isolation.

**Parameters**:
- `asset_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ExposureScoreResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/exposure/asset-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Exposure Score

---


### 18. POST /api/v2/risk/scores

**Summary**: Calculate Risk Score

**Description**: Calculate and store risk score for an entity.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/RiskScoreCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/RiskScoreResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/risk/scores" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Calculate Risk Score

---


### 19. GET /api/v2/risk/scores/high-risk

**Summary**: Get High Risk Entities

**Description**: Get all entities with high or critical risk scores.

**Parameters**:
- `min_score` (query) (optional): number
  - Minimum risk score threshold
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/RiskSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/scores/high-risk" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get High Risk Entities

---


### 20. GET /api/v2/risk/scores/history/{entity_type}/{entity_id}

**Summary**: Get Risk History

**Description**: Get risk score history for entity.

**Parameters**:
- `entity_type` (path) (required): string
- `entity_id` (path) (required): string
- `days` (query) (optional): integer
  - Days of history
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/RiskSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/scores/history/vulnerability/entity-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Risk History

---


### 21. POST /api/v2/risk/scores/recalculate/{entity_type}/{entity_id}

**Summary**: Recalculate Risk Score

**Description**: Force recalculation of risk score using existing factors.

Requires WRITE access level.

**Parameters**:
- `entity_type` (path) (required): string
- `entity_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/RiskScoreResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/risk/scores/recalculate/vulnerability/entity-123" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Recalculate Risk Score

---


### 22. GET /api/v2/risk/scores/search

**Summary**: Search Risk Scores

**Description**: Search risk scores with filters and customer isolation.

**Parameters**:
- `query` (query) (optional): string
  - Search query
- `entity_type` (query) (optional): string
  - Filter by entity type
- `risk_level` (query) (optional): string
  - Filter by risk level
- `min_risk_score` (query) (optional): string
- `max_risk_score` (query) (optional): string
- `trend` (query) (optional): string
  - Filter by trend
- `limit` (query) (optional): integer
  - Maximum results
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/RiskSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/scores/search" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Search Risk Scores

---


### 23. GET /api/v2/risk/scores/trending

**Summary**: Get Trending Entities

**Description**: Get entities with specific risk trend.

**Parameters**:
- `trend` (query) (optional): string
  - Risk trend: increasing, decreasing, stable
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/RiskSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/scores/trending" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Trending Entities

---


### 24. GET /api/v2/risk/scores/{entity_type}/{entity_id}

**Summary**: Get Risk Score

**Description**: Get most recent risk score for entity with customer isolation.

**Parameters**:
- `entity_type` (path) (required): string
- `entity_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/RiskScoreResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/risk/scores/vulnerability/entity-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Risk Score

---


## SBOM APIs

**Total Endpoints**: 32


### 1. POST /api/v2/sbom/components

**Summary**: Create Component

**Description**: Create a new software component.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/ComponentCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/ComponentResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/sbom/components" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Component

---


### 2. GET /api/v2/sbom/components/high-risk

**Summary**: Get High Risk Components

**Description**: Get all high-risk components (critical vulns, high license risk, or deprecated).

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ComponentSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/components/high-risk" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get High Risk Components

---


### 3. GET /api/v2/sbom/components/search

**Summary**: Search Components

**Description**: Search components with semantic search and filters.

**Parameters**:
- `query` (query) (optional): string
  - Semantic search query
- `sbom_id` (query) (optional): string
  - Filter by SBOM
- `component_type` (query) (optional): string
  - Filter by component type
- `license_risk` (query) (optional): string
  - Filter by license risk
- `has_vulnerabilities` (query) (optional): string
  - Filter by vulnerability presence
- `min_cvss` (query) (optional): string
  - Minimum CVSS score
- `status` (query) (optional): string
  - Filter by status
- `limit` (query) (optional): integer
  - Maximum results
- `include_system` (query) (optional): boolean
  - Include SYSTEM components
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ComponentSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/components/search" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Search Components

---


### 4. GET /api/v2/sbom/components/vulnerable

**Summary**: Get Vulnerable Components

**Description**: Get all components with vulnerabilities above CVSS threshold.

**Parameters**:
- `min_cvss` (query) (optional): number
  - Minimum CVSS threshold
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ComponentSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/components/vulnerable" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Vulnerable Components

---


### 5. GET /api/v2/sbom/components/{component_id}

**Summary**: Get Component

**Description**: Get component by ID with customer isolation.

**Parameters**:
- `component_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ComponentResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/components/comp-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Component

---


### 6. GET /api/v2/sbom/components/{component_id}/dependencies

**Summary**: Get Dependency Tree

**Description**: Get dependency tree for a component.

**Parameters**:
- `component_id` (path) (required): string
- `max_depth` (query) (optional): integer
  - Maximum tree depth
- `include_dev` (query) (optional): boolean
  - Include dev dependencies
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/DependencyTreeResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/components/comp-123/dependencies" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Dependency Tree

---


### 7. GET /api/v2/sbom/components/{component_id}/dependents

**Summary**: Get Dependents

**Description**: Get all components that depend on this component (reverse dependencies).

**Parameters**:
- `component_id` (path) (required): string
- `limit` (query) (optional): integer
  - Maximum results
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/components/comp-123/dependents" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Dependents

---


### 8. GET /api/v2/sbom/components/{component_id}/impact

**Summary**: Get Impact Analysis

**Description**: Analyze the impact if a component has a vulnerability.

**Parameters**:
- `component_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ImpactAnalysisResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/components/comp-123/impact" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Impact Analysis

---


### 9. GET /api/v2/sbom/components/{component_id}/vulnerabilities

**Summary**: Get Vulnerabilities By Component

**Description**: Get all vulnerabilities for a specific component.

**Parameters**:
- `component_id` (path) (required): string
- `limit` (query) (optional): integer
  - Maximum results
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/VulnerabilitySearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/components/comp-123/vulnerabilities" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Vulnerabilities By Component

---


### 10. GET /api/v2/sbom/dashboard/summary

**Summary**: Get Dashboard Summary

**Description**: Get customer-wide dashboard summary.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/api__sbom_analysis__sbom_router__DashboardSummaryResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/dashboard/summary" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Dashboard Summary

---


### 11. POST /api/v2/sbom/dependencies

**Summary**: Create Dependency

**Description**: Create a new dependency relation.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/DependencyCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/DependencyResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/sbom/dependencies" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Dependency

---


### 12. GET /api/v2/sbom/dependencies/path

**Summary**: Find Dependency Path

**Description**: Find shortest dependency path between two components.

**Parameters**:
- `source_id` (query) (required): string
  - Source component ID
- `target_id` (query) (required): string
  - Target component ID
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/dependencies/path" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Find Dependency Path

---


### 13. POST /api/v2/sbom/sboms

**Summary**: Create Sbom

**Description**: Create a new SBOM for the customer.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/SBOMCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/SBOMResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/sbom/sboms" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Sbom

---


### 14. GET /api/v2/sbom/sboms

**Summary**: List Sboms

**Description**: List SBOMs with filters and customer isolation.

**Parameters**:
- `query` (query) (optional): string
  - Search query
- `format` (query) (optional): string
  - Filter by SBOM format
- `has_vulnerabilities` (query) (optional): string
  - Filter by vulnerability presence
- `target_system_id` (query) (optional): string
  - Filter by target system
- `limit` (query) (optional): integer
  - Maximum results
- `include_system` (query) (optional): boolean
  - Include SYSTEM SBOMs
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/SBOMSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/sboms" \
  -H "x-customer-id: dev"
```

**Use Case**: 
List Sboms

---


### 15. GET /api/v2/sbom/sboms/{sbom_id}

**Summary**: Get Sbom

**Description**: Get SBOM by ID with customer isolation.

**Parameters**:
- `sbom_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/SBOMResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/sbom-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Sbom

---


### 16. DELETE /api/v2/sbom/sboms/{sbom_id}

**Summary**: Delete Sbom

**Description**: Delete an SBOM and all its components.

Requires WRITE access level.

**Parameters**:
- `sbom_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X DELETE "http://localhost:8000/api/v2/sbom/sboms/sbom-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Delete Sbom

---


### 17. GET /api/v2/sbom/sboms/{sbom_id}/components

**Summary**: Get Components By Sbom

**Description**: Get all components for a specific SBOM.

**Parameters**:
- `sbom_id` (path) (required): string
- `limit` (query) (optional): integer
  - Maximum components
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ComponentSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/sbom-123/components" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Components By Sbom

---


### 18. POST /api/v2/sbom/sboms/{sbom_id}/correlate-equipment

**Summary**: Correlate With Equipment

**Description**: Correlate SBOM vulnerabilities with E15 equipment.

Links software vulnerabilities to physical equipment for risk assessment.

**Parameters**:
- `sbom_id` (path) (required): string
- `equipment_id` (query) (required): string
  - E15 Equipment ID to correlate
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/sbom/sboms/sbom-123/correlate-equipment" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Correlate With Equipment

---


### 19. GET /api/v2/sbom/sboms/{sbom_id}/cycles

**Summary**: Detect Cycles

**Description**: Detect circular dependencies in an SBOM.

**Parameters**:
- `sbom_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/sbom-123/cycles" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Detect Cycles

---


### 20. GET /api/v2/sbom/sboms/{sbom_id}/graph-stats

**Summary**: Get Graph Stats

**Description**: Get comprehensive dependency graph statistics for an SBOM.

**Parameters**:
- `sbom_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/DependencyGraphStatsResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/sbom-123/graph-stats" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Graph Stats

---


### 21. GET /api/v2/sbom/sboms/{sbom_id}/license-compliance

**Summary**: Get License Compliance

**Description**: Get license compliance analysis for an SBOM.

**Parameters**:
- `sbom_id` (path) (required): string
- `allowed_licenses` (query) (optional): array
  - Allowed license types
- `denied_licenses` (query) (optional): array
  - Denied license types
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/LicenseComplianceResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/sbom-123/license-compliance" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get License Compliance

---


### 22. GET /api/v2/sbom/sboms/{sbom_id}/remediation

**Summary**: Get Remediation Report

**Description**: Generate remediation report for an SBOM.

**Parameters**:
- `sbom_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/RemediationReportResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/sbom-123/remediation" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Remediation Report

---


### 23. GET /api/v2/sbom/sboms/{sbom_id}/risk-summary

**Summary**: Get Sbom Risk Summary

**Description**: Get comprehensive risk summary for an SBOM.

**Parameters**:
- `sbom_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/SBOMRiskSummaryResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/sbom-123/risk-summary" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Sbom Risk Summary

---


### 24. GET /api/v2/sbom/sboms/{sbom_id}/vulnerable-paths

**Summary**: Get Vulnerable Paths

**Description**: Find all paths to vulnerable components in an SBOM.

**Parameters**:
- `sbom_id` (path) (required): string
- `min_cvss` (query) (optional): number
  - Minimum CVSS threshold
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/sbom-123/vulnerable-paths" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Vulnerable Paths

---


### 25. POST /api/v2/sbom/vulnerabilities

**Summary**: Create Vulnerability

**Description**: Create a new vulnerability record.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/VulnerabilityCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/VulnerabilityResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/sbom/vulnerabilities" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Vulnerability

---


### 26. GET /api/v2/sbom/vulnerabilities/by-apt

**Summary**: Get Apt Vulnerability Report

**Description**: Get vulnerability report grouped by APT groups.

**Parameters**:
- `apt_group` (query) (optional): string
  - Filter by specific APT group
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/APTReportResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/vulnerabilities/by-apt" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Apt Vulnerability Report

---


### 27. GET /api/v2/sbom/vulnerabilities/critical

**Summary**: Get Critical Vulnerabilities

**Description**: Get all critical vulnerabilities (CISA KEV, in-the-wild, or CVSS >= 9.0).

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/VulnerabilitySearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/vulnerabilities/critical" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Critical Vulnerabilities

---


### 28. GET /api/v2/sbom/vulnerabilities/epss-prioritized

**Summary**: Get Epss Prioritized Vulns

**Description**: Get vulnerabilities prioritized by EPSS score (exploit probability).

**Parameters**:
- `min_epss` (query) (optional): number
  - Minimum EPSS score
- `limit` (query) (optional): integer
  - Maximum results
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/VulnerabilitySearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/vulnerabilities/epss-prioritized" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Epss Prioritized Vulns

---


### 29. GET /api/v2/sbom/vulnerabilities/kev

**Summary**: Get Kev Vulnerabilities

**Description**: Get all CISA Known Exploited Vulnerabilities (KEV).

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/VulnerabilitySearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/vulnerabilities/kev" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Kev Vulnerabilities

---


### 30. GET /api/v2/sbom/vulnerabilities/search

**Summary**: Search Vulnerabilities

**Description**: Search vulnerabilities with semantic search and filters.

**Parameters**:
- `query` (query) (optional): string
  - Semantic search query
- `component_id` (query) (optional): string
  - Filter by component
- `min_cvss` (query) (optional): string
  - Minimum CVSS score
- `severity` (query) (optional): string
  - Filter by severity
- `exploit_available` (query) (optional): string
  - Has exploit available
- `cisa_kev` (query) (optional): string
  - Is in CISA KEV
- `has_fix` (query) (optional): string
  - Has fix available
- `limit` (query) (optional): integer
  - Maximum results
- `include_system` (query) (optional): boolean
  - Include SYSTEM vulnerabilities
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/VulnerabilitySearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/vulnerabilities/search" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Search Vulnerabilities

---


### 31. GET /api/v2/sbom/vulnerabilities/{vulnerability_id}

**Summary**: Get Vulnerability

**Description**: Get vulnerability by ID.

**Parameters**:
- `vulnerability_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/VulnerabilityResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/sbom/vulnerabilities/CVE-2024-1234" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Vulnerability

---


### 32. POST /api/v2/sbom/vulnerabilities/{vulnerability_id}/acknowledge

**Summary**: Acknowledge Vulnerability

**Description**: Acknowledge a vulnerability (mark as reviewed).

Requires WRITE access level.

**Parameters**:
- `vulnerability_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/VulnerabilityAcknowledgeRequest
```

**Responses**:
- **200**: Successful Response
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/sbom/vulnerabilities/CVE-2024-1234/acknowledge" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Acknowledge Vulnerability

---


## THREAT INTEL APIs

**Total Endpoints**: 26


### 1. POST /api/v2/threat-intel/actors

**Summary**: Create Threat Actor

**Description**: Create a new threat actor.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/ThreatActorCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/ThreatActorResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/threat-intel/actors" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Threat Actor

---


### 2. GET /api/v2/threat-intel/actors/active

**Summary**: Get Active Threat Actors

**Description**: Get all currently active threat actors.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ThreatActorSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/actors/active" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Active Threat Actors

---


### 3. GET /api/v2/threat-intel/actors/by-sector/{sector}

**Summary**: Get Actors By Sector

**Description**: Get threat actors targeting a specific sector.

**Parameters**:
- `sector` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ThreatActorSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/actors/by-sector/financial" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Actors By Sector

---


### 4. GET /api/v2/threat-intel/actors/search

**Summary**: Search Threat Actors

**Description**: Search threat actors with semantic search and filters.

**Parameters**:
- `query` (query) (optional): string
  - Semantic search query
- `actor_type` (query) (optional): string
  - Filter by actor type
- `country` (query) (optional): string
  - Filter by country
- `target_sector` (query) (optional): string
  - Filter by target sector
- `is_active` (query) (optional): string
  - Filter by active status
- `limit` (query) (optional): integer
  - Maximum results
- `include_system` (query) (optional): boolean
  - Include SYSTEM actors
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ThreatActorSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/actors/search" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Search Threat Actors

---


### 5. GET /api/v2/threat-intel/actors/{actor_id}

**Summary**: Get Threat Actor

**Description**: Get threat actor by ID with customer isolation.

**Parameters**:
- `actor_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ThreatActorResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/actors/APT1" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Threat Actor

---


### 6. GET /api/v2/threat-intel/actors/{actor_id}/campaigns

**Summary**: Get Actor Campaigns

**Description**: Get campaigns associated with a threat actor.

**Parameters**:
- `actor_id` (path) (required): string
- `limit` (query) (optional): integer
  - Maximum results
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/actors/APT1/campaigns" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Actor Campaigns

---


### 7. GET /api/v2/threat-intel/actors/{actor_id}/cves

**Summary**: Get Actor Cves

**Description**: Get CVEs associated with a threat actor.

**Parameters**:
- `actor_id` (path) (required): string
- `limit` (query) (optional): integer
  - Maximum results
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/actors/APT1/cves" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Actor Cves

---


### 8. POST /api/v2/threat-intel/campaigns

**Summary**: Create Campaign

**Description**: Create a new campaign.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/CampaignCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/CampaignResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/threat-intel/campaigns" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Campaign

---


### 9. GET /api/v2/threat-intel/campaigns/active

**Summary**: Get Active Campaigns

**Description**: Get all currently active campaigns.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/CampaignSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/campaigns/active" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Active Campaigns

---


### 10. GET /api/v2/threat-intel/campaigns/search

**Summary**: Search Campaigns

**Description**: Search campaigns with semantic search and filters.

**Parameters**:
- `query` (query) (optional): string
  - Semantic search query
- `threat_actor_id` (query) (optional): string
  - Filter by threat actor
- `target_sector` (query) (optional): string
  - Filter by target sector
- `is_active` (query) (optional): string
  - Filter by active status
- `limit` (query) (optional): integer
  - Maximum results
- `include_system` (query) (optional): boolean
  - Include SYSTEM campaigns
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/CampaignSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/campaigns/search" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Search Campaigns

---


### 11. GET /api/v2/threat-intel/campaigns/{campaign_id}

**Summary**: Get Campaign

**Description**: Get campaign by ID with customer isolation.

**Parameters**:
- `campaign_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/CampaignResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/campaigns/campaign-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Campaign

---


### 12. GET /api/v2/threat-intel/campaigns/{campaign_id}/iocs

**Summary**: Get Campaign Iocs

**Description**: Get IOCs associated with a campaign.

**Parameters**:
- `campaign_id` (path) (required): string
- `limit` (query) (optional): integer
  - Maximum results
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/campaigns/campaign-123/iocs" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Campaign Iocs

---


### 13. GET /api/v2/threat-intel/dashboard/summary

**Summary**: Get Threat Intel Summary

**Description**: Get threat intelligence dashboard summary.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ThreatIntelSummaryResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/dashboard/summary" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Threat Intel Summary

---


### 14. POST /api/v2/threat-intel/feeds

**Summary**: Create Threat Feed

**Description**: Create a new threat feed.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/ThreatFeedCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/ThreatFeedResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/threat-intel/feeds" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Threat Feed

---


### 15. GET /api/v2/threat-intel/feeds

**Summary**: List Threat Feeds

**Description**: List threat feeds.

**Parameters**:
- `limit` (query) (optional): integer
  - Maximum results
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/ThreatFeedListResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/feeds" \
  -H "x-customer-id: dev"
```

**Use Case**: 
List Threat Feeds

---


### 16. PUT /api/v2/threat-intel/feeds/{feed_id}/refresh

**Summary**: Trigger Feed Refresh

**Description**: Trigger threat feed refresh.

Requires WRITE access level.

**Parameters**:
- `feed_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X PUT "http://localhost:8000/api/v2/threat-intel/feeds/feed-123/refresh" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Trigger Feed Refresh

---


### 17. POST /api/v2/threat-intel/iocs

**Summary**: Create Ioc

**Description**: Create a new IOC.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/IOCCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/IOCResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/threat-intel/iocs" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Ioc

---


### 18. GET /api/v2/threat-intel/iocs/active

**Summary**: Get Active Iocs

**Description**: Get all currently active IOCs.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/IOCSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/iocs/active" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Active Iocs

---


### 19. POST /api/v2/threat-intel/iocs/bulk

**Summary**: Bulk Import Iocs

**Description**: Bulk import IOCs.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/IOCBulkImport
```

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/IOCBulkImportResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/threat-intel/iocs/bulk" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Bulk Import Iocs

---


### 20. GET /api/v2/threat-intel/iocs/by-type/{ioc_type}

**Summary**: Get Iocs By Type

**Description**: Get IOCs by type.

**Parameters**:
- `ioc_type` (path) (required): string
- `limit` (query) (optional): integer
  - Maximum results
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/IOCSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/iocs/by-type/ip" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Iocs By Type

---


### 21. GET /api/v2/threat-intel/iocs/search

**Summary**: Search Iocs

**Description**: Search IOCs with semantic search and filters.

**Parameters**:
- `query` (query) (optional): string
  - Semantic search query
- `ioc_type` (query) (optional): string
  - Filter by IOC type
- `threat_actor_id` (query) (optional): string
  - Filter by threat actor
- `campaign_id` (query) (optional): string
  - Filter by campaign
- `min_confidence` (query) (optional): string
  - Minimum confidence
- `is_active` (query) (optional): string
  - Filter by active status
- `limit` (query) (optional): integer
  - Maximum results
- `include_system` (query) (optional): boolean
  - Include SYSTEM IOCs
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/IOCSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/iocs/search" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Search Iocs

---


### 22. GET /api/v2/threat-intel/mitre/coverage

**Summary**: Get Mitre Coverage

**Description**: Get MITRE ATT&CK coverage summary.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/MITRECoverageResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/mitre/coverage" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Mitre Coverage

---


### 23. GET /api/v2/threat-intel/mitre/gaps

**Summary**: Get Mitre Gaps

**Description**: Get MITRE ATT&CK coverage gaps.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/MITREGapsResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/mitre/gaps" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Mitre Gaps

---


### 24. POST /api/v2/threat-intel/mitre/mappings

**Summary**: Create Mitre Mapping

**Description**: Create a new MITRE ATT&CK mapping.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/MITREMappingCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/MITREMappingResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/threat-intel/mitre/mappings" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Mitre Mapping

---


### 25. GET /api/v2/threat-intel/mitre/mappings/entity/{entity_type}/{entity_id}

**Summary**: Get Entity Mitre Mappings

**Description**: Get MITRE ATT&CK mappings for an entity.

**Parameters**:
- `entity_type` (path) (required): string
- `entity_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/MITREMappingSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/mitre/mappings/entity/vulnerability/entity-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Entity Mitre Mappings

---


### 26. GET /api/v2/threat-intel/mitre/techniques/{technique_id}/actors

**Summary**: Get Actors Using Technique

**Description**: Get threat actors using a specific MITRE ATT&CK technique.

**Parameters**:
- `technique_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/threat-intel/mitre/techniques/T1001/actors" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Actors Using Technique

---


## VENDOR EQUIPMENT APIs

**Total Endpoints**: 24


### 1. POST /api/v2/vendor-equipment/equipment

**Summary**: Create Equipment

**Description**: Create a new equipment model for the customer.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/EquipmentCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/EquipmentResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/vendor-equipment/equipment" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Equipment

---


### 2. GET /api/v2/vendor-equipment/equipment

**Summary**: Search Equipment

**Description**: Search equipment with filters and customer isolation.

**Parameters**:
- `query` (query) (optional): string
  - Search query
- `vendor_id` (query) (optional): string
  - Filter by vendor
- `lifecycle_status` (query) (optional): string
  - Filter by lifecycle status
- `category` (query) (optional): string
  - Filter by category
- `criticality` (query) (optional): string
  - Filter by criticality
- `approaching_eol_days` (query) (optional): string
  - Find equipment within N days of EOL
- `limit` (query) (optional): integer
  - Maximum results
- `include_system` (query) (optional): boolean
  - Include SYSTEM equipment
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/EquipmentSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/equipment" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Search Equipment

---


### 3. GET /api/v2/vendor-equipment/equipment/approaching-eol

**Summary**: Get Equipment Approaching Eol

**Description**: Get all equipment approaching EOL within specified days.

**Parameters**:
- `days` (query) (optional): integer
  - Days threshold for EOL
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/EquipmentSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/equipment/approaching-eol" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Equipment Approaching Eol

---


### 4. GET /api/v2/vendor-equipment/equipment/eol

**Summary**: Get Eol Equipment

**Description**: Get all equipment that has passed EOL.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/EquipmentSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/equipment/eol" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Eol Equipment

---


### 5. GET /api/v2/vendor-equipment/equipment/{model_id}

**Summary**: Get Equipment

**Description**: Get equipment model by ID with customer isolation.

**Parameters**:
- `model_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/EquipmentResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/equipment/model-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Equipment

---


### 6. GET /api/v2/vendor-equipment/maintenance-schedule

**Summary**: Get Maintenance Schedule

**Description**: Get prioritized maintenance schedule.

Prioritized by:
1. EOL proximity
2. Vulnerability count
3. Criticality

**Parameters**:
- `limit` (query) (optional): integer
  - Maximum items
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/MaintenanceScheduleResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/maintenance-schedule" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Maintenance Schedule

---


### 7. POST /api/v2/vendor-equipment/maintenance-windows

**Summary**: Create Maintenance Window

**Description**: Create a new maintenance window.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/MaintenanceWindowCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/MaintenanceWindowResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/vendor-equipment/maintenance-windows" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Maintenance Window

---


### 8. GET /api/v2/vendor-equipment/maintenance-windows

**Summary**: List Maintenance Windows

**Description**: List maintenance windows with optional filters.

**Parameters**:
- `window_type` (query) (optional): string
  - Filter by window type
- `equipment_id` (query) (optional): string
  - Filter by affected equipment
- `limit` (query) (optional): integer
  - Maximum results
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/MaintenanceWindowListResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/maintenance-windows" \
  -H "x-customer-id: dev"
```

**Use Case**: 
List Maintenance Windows

---


### 9. POST /api/v2/vendor-equipment/maintenance-windows/check-conflict

**Summary**: Check Maintenance Conflict

**Description**: Check for scheduling conflicts with existing maintenance windows.

**Parameters**:
- `proposed_start` (query) (required): string
  - Proposed start time
- `proposed_end` (query) (required): string
  - Proposed end time
- `equipment_ids` (query) (optional): array
  - Equipment IDs to check
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/MaintenanceConflictResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/vendor-equipment/maintenance-windows/check-conflict" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Check Maintenance Conflict

---


### 10. GET /api/v2/vendor-equipment/maintenance-windows/{window_id}

**Summary**: Get Maintenance Window

**Description**: Get maintenance window by ID.

**Parameters**:
- `window_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/MaintenanceWindowResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/maintenance-windows/window-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Maintenance Window

---


### 11. DELETE /api/v2/vendor-equipment/maintenance-windows/{window_id}

**Summary**: Delete Maintenance Window

**Description**: Delete a maintenance window.

Requires WRITE access level.

**Parameters**:
- `window_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X DELETE "http://localhost:8000/api/v2/vendor-equipment/maintenance-windows/window-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Delete Maintenance Window

---


### 12. GET /api/v2/vendor-equipment/predictive-maintenance/forecast

**Summary**: Get Maintenance Forecast

**Description**: Get comprehensive maintenance forecast.

**Parameters**:
- `months_ahead` (query) (optional): integer
  - Months ahead for forecast
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/MaintenanceForecastResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/predictive-maintenance/forecast" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Maintenance Forecast

---


### 13. GET /api/v2/vendor-equipment/predictive-maintenance/{equipment_id}

**Summary**: Predict Maintenance

**Description**: Get maintenance predictions for specific equipment.

**Parameters**:
- `equipment_id` (path) (required): string
- `days_ahead` (query) (optional): integer
  - Days ahead to predict
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/MaintenancePredictionListResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/predictive-maintenance/equip-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Predict Maintenance

---


### 14. POST /api/v2/vendor-equipment/vendors

**Summary**: Create Vendor

**Description**: Create a new vendor for the customer.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/VendorCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/VendorResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/vendor-equipment/vendors" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Vendor

---


### 15. GET /api/v2/vendor-equipment/vendors

**Summary**: Search Vendors

**Description**: Search vendors with filters and customer isolation.

**Parameters**:
- `query` (query) (optional): string
  - Search query
- `risk_level` (query) (optional): string
  - Filter by risk level
- `min_risk_score` (query) (optional): string
  - Minimum risk score
- `support_status` (query) (optional): string
  - Filter by support status
- `supply_chain_tier` (query) (optional): string
  - Supply chain tier
- `limit` (query) (optional): integer
  - Maximum results
- `include_system` (query) (optional): boolean
  - Include SYSTEM vendors
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/VendorSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/vendors" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Search Vendors

---


### 16. GET /api/v2/vendor-equipment/vendors/high-risk

**Summary**: Get High Risk Vendors

**Description**: Get all vendors with high risk scores.

**Parameters**:
- `min_risk_score` (query) (optional): number
  - Minimum risk score threshold
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/VendorSearchResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/vendors/high-risk" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get High Risk Vendors

---


### 17. GET /api/v2/vendor-equipment/vendors/{vendor_id}

**Summary**: Get Vendor

**Description**: Get vendor by ID with customer isolation.

**Parameters**:
- `vendor_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/VendorResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/vendors/vendor-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Vendor

---


### 18. GET /api/v2/vendor-equipment/vendors/{vendor_id}/risk-summary

**Summary**: Get Vendor Risk Summary

**Description**: Get comprehensive risk summary for a vendor.

**Parameters**:
- `vendor_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/VendorRiskSummaryResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/vendors/vendor-123/risk-summary" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Vendor Risk Summary

---


### 19. POST /api/v2/vendor-equipment/vulnerabilities/flag

**Summary**: Flag Vendor Vulnerability

**Description**: Flag a supply chain vulnerability affecting a vendor.

All equipment from the affected vendor will be flagged.
Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/VulnerabilityFlagRequest
```

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/VulnerabilityFlagResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/vendor-equipment/vulnerabilities/flag" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Flag Vendor Vulnerability

---


### 20. POST /api/v2/vendor-equipment/work-orders

**Summary**: Create Work Order

**Description**: Create a new work order.

Requires WRITE access level.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/WorkOrderCreate
```

**Responses**:
- **201**: Successful Response
```
  Reference: #/components/schemas/WorkOrderResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v2/vendor-equipment/work-orders" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Create Work Order

---


### 21. GET /api/v2/vendor-equipment/work-orders

**Summary**: List Work Orders

**Description**: List work orders with optional filters.

**Parameters**:
- `status` (query) (optional): string
  - Filter by status
- `priority` (query) (optional): string
  - Filter by priority
- `equipment_id` (query) (optional): string
  - Filter by equipment
- `limit` (query) (optional): integer
  - Maximum results
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/WorkOrderListResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/work-orders" \
  -H "x-customer-id: dev"
```

**Use Case**: 
List Work Orders

---


### 22. GET /api/v2/vendor-equipment/work-orders/summary

**Summary**: Get Work Order Summary

**Description**: Get work order summary with status and priority breakdowns.

**Parameters**:
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/WorkOrderSummaryResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/work-orders/summary" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Work Order Summary

---


### 23. GET /api/v2/vendor-equipment/work-orders/{work_order_id}

**Summary**: Get Work Order

**Description**: Get work order by ID.

**Parameters**:
- `work_order_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/WorkOrderResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v2/vendor-equipment/work-orders/wo-123" \
  -H "x-customer-id: dev"
```

**Use Case**: 
Get Work Order

---


### 24. PATCH /api/v2/vendor-equipment/work-orders/{work_order_id}/status

**Summary**: Update Work Order Status

**Description**: Update work order status.

Requires WRITE access level.

**Parameters**:
- `work_order_id` (path) (required): string
- `x-customer-id` (header) (required): string
  - Customer identifier
- `x-namespace` (header) (optional): string
  - Customer namespace
- `x-user-id` (header) (optional): string
  - User identifier
- `x-access-level` (header) (optional): string
  - Access level

**Request Body**:
(required)

```
Reference: #/components/schemas/WorkOrderStatusUpdate
```

**Responses**:
- **200**: Successful Response
```
  Reference: #/components/schemas/WorkOrderResponse
```
- **422**: Validation Error
```
  Reference: #/components/schemas/HTTPValidationError
```

**Example**:
```bash
curl -X PATCH "http://localhost:8000/api/v2/vendor-equipment/work-orders/wo-123/status" \
  -H "x-customer-id: dev" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Case**: 
Update Work Order Status

---


---

# NER APIs

**Total Endpoints**: 5


## 1. POST /ner

**Summary**: Extract Entities

**Description**: Extract named entities from text using enhanced multi-layer NER approach.

Strategy (in priority order):
1. Pattern-based extraction (HIGH confidence for CVE, APT, MITRE patterns)
2. Fallback model (en_core_web_trf) for general NER
3. Custom NER11 model for cybersecurity-specific entities

The pattern-based extraction addresses the context-dependency issue where
transformer models require longer context to identify short entities like
"APT29", "CVE-2024-12345", or "T1566".


## 2. POST /search/semantic

**Summary**: Semantic Search

**Description**: Semantic search with hierarchical filtering (Task 1.5).

Search entities using semantic similarity with hierarchical taxonomy filtering:
- Tier 1 filtering: label_filter (60 NER labels)
- Tier 2 filtering: fine_grained_filter (566 fine-grained types) - KEY FEATURE
- Confidence filtering: confidence_threshold

Example queries:
- "ransomware attack" → Find semantically similar malware entities
- "SCADA systems" with fine_grained_filter="SCADA_SERVER" → Precise infrastructure search
- "threat actors" with label_filter="THREAT_ACTOR" → Category-filtered search

Returns results with complete hierarchy_path for each entity.


## 3. POST /search/hybrid

**Summary**: Hybrid Search

**Description**: Hybrid search combining semantic similarity (Qdrant) with graph expansion (Neo4j).

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


## 4. GET /health

**Summary**: Health Check

**Description**: Health check endpoint with service status and model validation.


## 5. GET /info

**Summary**: Model Info

**Description**: Model information and capabilities.

---

# NEXT.JS API ROUTES (41 endpoints)

## Dashboard & Analytics APIs

### 1. GET /api/dashboard/stats
**Summary**: Get dashboard statistics
**Response**: Overview metrics for main dashboard
**Example**:
```bash
curl http://localhost:3000/api/dashboard/stats
```

### 2. GET /api/analytics/trends
**Summary**: Get security trends data
**Response**: Time-series data for trends visualization
**Example**:
```bash
curl http://localhost:3000/api/analytics/trends
```

### 3. GET /api/analytics/risk-distribution
**Summary**: Get risk distribution metrics
**Response**: Risk breakdown by category and severity
**Example**:
```bash
curl http://localhost:3000/api/analytics/risk-distribution
```

## Threat Intelligence APIs

### 4. GET /api/threats/actors
**Summary**: Get threat actors
**Query**: ?page=1&limit=20
**Response**: Paginated threat actor data
**Example**:
```bash
curl "http://localhost:3000/api/threats/actors?page=1&limit=20"
```

### 5. GET /api/threats/actors/[id]
**Summary**: Get specific threat actor details
**Response**: Detailed threat actor profile
**Example**:
```bash
curl http://localhost:3000/api/threats/actors/APT1
```

### 6. GET /api/threats/campaigns
**Summary**: Get threat campaigns
**Response**: Active and historical campaigns
**Example**:
```bash
curl http://localhost:3000/api/threats/campaigns
```

### 7. GET /api/threats/iocs
**Summary**: Get indicators of compromise
**Query**: ?type=ip&page=1
**Response**: IOC data with filtering
**Example**:
```bash
curl "http://localhost:3000/api/threats/iocs?type=ip"
```

### 8. GET /api/threats/mitre/coverage
**Summary**: Get ATT&CK coverage
**Response**: MITRE ATT&CK technique coverage matrix
**Example**:
```bash
curl http://localhost:3000/api/threats/mitre/coverage
```

## Vulnerability Management APIs

### 9. GET /api/vulnerabilities
**Summary**: Get vulnerabilities
**Query**: ?severity=critical&page=1
**Response**: Paginated vulnerability data
**Example**:
```bash
curl "http://localhost:3000/api/vulnerabilities?severity=critical"
```

### 10. GET /api/vulnerabilities/[id]
**Summary**: Get vulnerability details
**Response**: Detailed CVE information
**Example**:
```bash
curl http://localhost:3000/api/vulnerabilities/CVE-2024-1234
```

### 11. GET /api/vulnerabilities/stats
**Summary**: Get vulnerability statistics
**Response**: Counts by severity and status
**Example**:
```bash
curl http://localhost:3000/api/vulnerabilities/stats
```

### 12. GET /api/vulnerabilities/trending
**Summary**: Get trending vulnerabilities
**Response**: Recently disclosed or exploited CVEs
**Example**:
```bash
curl http://localhost:3000/api/vulnerabilities/trending
```

## SBOM & Asset Management APIs

### 13. GET /api/sbom/list
**Summary**: Get SBOM inventory
**Response**: List of software bills of materials
**Example**:
```bash
curl http://localhost:3000/api/sbom/list
```

### 14. GET /api/sbom/[id]
**Summary**: Get specific SBOM
**Response**: Detailed SBOM with components
**Example**:
```bash
curl http://localhost:3000/api/sbom/sbom-123
```

### 15. GET /api/sbom/components
**Summary**: Get component inventory
**Query**: ?risk=high
**Response**: Software components with risk data
**Example**:
```bash
curl "http://localhost:3000/api/sbom/components?risk=high"
```

### 16. GET /api/sbom/dependencies
**Summary**: Get dependency graph
**Response**: Component dependency relationships
**Example**:
```bash
curl http://localhost:3000/api/sbom/dependencies
```

### 17. GET /api/assets
**Summary**: Get asset inventory
**Response**: IT assets with criticality
**Example**:
```bash
curl http://localhost:3000/api/assets
```

### 18. GET /api/assets/[id]
**Summary**: Get asset details
**Response**: Detailed asset information
**Example**:
```bash
curl http://localhost:3000/api/assets/asset-123
```

### 19. GET /api/assets/criticality
**Summary**: Get asset criticality distribution
**Response**: Assets grouped by criticality level
**Example**:
```bash
curl http://localhost:3000/api/assets/criticality
```

## Risk Management APIs

### 20. GET /api/risk/scores
**Summary**: Get risk scores
**Response**: Entity risk scores with trends
**Example**:
```bash
curl http://localhost:3000/api/risk/scores
```

### 21. GET /api/risk/matrix
**Summary**: Get risk matrix
**Response**: Risk distribution matrix data
**Example**:
```bash
curl http://localhost:3000/api/risk/matrix
```

### 22. GET /api/risk/exposure
**Summary**: Get exposure metrics
**Response**: Attack surface and exposure data
**Example**:
```bash
curl http://localhost:3000/api/risk/exposure
```

### 23. GET /api/risk/trends
**Summary**: Get risk trends
**Response**: Historical risk score changes
**Example**:
```bash
curl http://localhost:3000/api/risk/trends
```

## Remediation & Task Management APIs

### 24. GET /api/remediation/tasks
**Summary**: Get remediation tasks
**Query**: ?status=open&priority=high
**Response**: Filtered task list
**Example**:
```bash
curl "http://localhost:3000/api/remediation/tasks?status=open"
```

### 25. GET /api/remediation/tasks/[id]
**Summary**: Get task details
**Response**: Task information with history
**Example**:
```bash
curl http://localhost:3000/api/remediation/tasks/task-456
```

### 26. POST /api/remediation/tasks
**Summary**: Create remediation task
**Body**: Task creation payload
**Example**:
```bash
curl -X POST http://localhost:3000/api/remediation/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Fix CVE-2024-1234","priority":"high"}'
```

### 27. PATCH /api/remediation/tasks/[id]
**Summary**: Update task
**Body**: Task update payload
**Example**:
```bash
curl -X PATCH http://localhost:3000/api/remediation/tasks/task-456 \
  -H "Content-Type: application/json" \
  -d '{"status":"in_progress"}'
```

### 28. GET /api/remediation/plans
**Summary**: Get remediation plans
**Response**: Active remediation plans
**Example**:
```bash
curl http://localhost:3000/api/remediation/plans
```

### 29. GET /api/remediation/sla
**Summary**: Get SLA metrics
**Response**: SLA compliance and breaches
**Example**:
```bash
curl http://localhost:3000/api/remediation/sla
```

## Vendor & Equipment APIs

### 30. GET /api/vendors
**Summary**: Get vendor list
**Response**: Vendor inventory with risk
**Example**:
```bash
curl http://localhost:3000/api/vendors
```

### 31. GET /api/vendors/[id]
**Summary**: Get vendor details
**Response**: Vendor profile with risk summary
**Example**:
```bash
curl http://localhost:3000/api/vendors/vendor-123
```

### 32. GET /api/equipment
**Summary**: Get equipment inventory
**Response**: Hardware and software equipment
**Example**:
```bash
curl http://localhost:3000/api/equipment
```

### 33. GET /api/equipment/eol
**Summary**: Get end-of-life equipment
**Response**: Equipment approaching EOL
**Example**:
```bash
curl http://localhost:3000/api/equipment/eol
```

### 34. GET /api/maintenance/schedule
**Summary**: Get maintenance schedule
**Response**: Upcoming maintenance windows
**Example**:
```bash
curl http://localhost:3000/api/maintenance/schedule
```

### 35. GET /api/work-orders
**Summary**: Get work orders
**Response**: Active and completed work orders
**Example**:
```bash
curl http://localhost:3000/api/work-orders
```

## Search & Query APIs

### 36. GET /api/search
**Summary**: Global search
**Query**: ?q=APT1&type=all
**Response**: Search results across all entities
**Example**:
```bash
curl "http://localhost:3000/api/search?q=APT1"
```

### 37. POST /api/search/advanced
**Summary**: Advanced search
**Body**: Complex search query
**Example**:
```bash
curl -X POST http://localhost:3000/api/search/advanced \
  -H "Content-Type: application/json" \
  -d '{"filters":{"severity":"critical"}}'
```

## Export & Reporting APIs

### 38. GET /api/export/vulnerabilities
**Summary**: Export vulnerability data
**Query**: ?format=csv
**Response**: Downloadable export file
**Example**:
```bash
curl "http://localhost:3000/api/export/vulnerabilities?format=csv"
```

### 39. GET /api/export/sbom
**Summary**: Export SBOM data
**Query**: ?id=sbom-123&format=json
**Response**: SBOM export
**Example**:
```bash
curl "http://localhost:3000/api/export/sbom?id=sbom-123"
```

### 40. POST /api/reports/generate
**Summary**: Generate custom report
**Body**: Report configuration
**Example**:
```bash
curl -X POST http://localhost:3000/api/reports/generate \
  -H "Content-Type: application/json" \
  -d '{"type":"executive","period":"monthly"}'
```

## System APIs

### 41. GET /api/health
**Summary**: Health check
**Response**: System health status
**Example**:
```bash
curl http://localhost:3000/api/health
```

---

# API USAGE PATTERNS

## Authentication
Phase B APIs require `x-customer-id` header:
```bash
curl -H "x-customer-id: dev" http://localhost:8000/api/v2/...
```

Next.js APIs typically use session-based auth (check implementation).

## Pagination
Most list endpoints support pagination:
```bash
?page=1&limit=20&offset=0
```

## Filtering
Common filter parameters:
- `status`: open, closed, in_progress
- `severity`: critical, high, medium, low
- `priority`: urgent, high, medium, low
- `type`: various entity types

## Sorting
Use `sort` and `order` parameters:
```bash
?sort=created_at&order=desc
```

## Error Responses
- **422**: Validation error (missing required fields)
- **404**: Resource not found
- **500**: Internal server error
- **401/403**: Authentication/authorization errors

---

# DEVELOPER QUICK REFERENCE

## Most Common APIs

**Dashboard Data**:
- GET /api/v2/remediation/dashboard/summary
- GET /api/v2/risk/dashboard/summary
- GET /api/v2/sbom/dashboard/summary
- GET /api/v2/threat-intel/dashboard/summary

**Search & Discovery**:
- GET /api/v2/threat-intel/actors/search
- GET /api/v2/sbom/components/search
- GET /api/v2/risk/scores/search
- GET /api/search (Next.js)

**Critical Data**:
- GET /api/v2/sbom/vulnerabilities/critical
- GET /api/v2/risk/scores/high-risk
- GET /api/v2/remediation/tasks/overdue
- GET /api/v2/vendor-equipment/vendors/high-risk

**Real-time Updates**:
- GET /api/v2/remediation/tasks/open
- GET /api/v2/threat-intel/iocs/active
- GET /api/v2/sbom/components/vulnerable

---

**END OF DOCUMENTATION**

Total APIs Documented: 181
- Phase B (v2): 135
- NER: 5  
- Next.js: 41
