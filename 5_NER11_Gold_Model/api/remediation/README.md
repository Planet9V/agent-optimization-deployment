# E06: Remediation Workflow API - Data Models

**Version:** 1.0.0
**Created:** 2025-12-04
**Status:** Complete

## Overview

Complete data models for E06: Remediation Workflow API, providing vulnerability remediation tracking, SLA management, and performance metrics.

## Data Models

### 1. RemediationTask
**Purpose:** Track individual vulnerability remediation tasks with SLA and assignment.

**Key Fields:**
- `task_id`, `customer_id`, `title`, `description`
- `vulnerability_id`, `cve_id`, `asset_ids` - Linkage to vulnerabilities and assets
- `task_type` - PATCH, UPGRADE, CONFIGURATION, WORKAROUND, MITIGATION, REPLACEMENT
- `status` - OPEN, IN_PROGRESS, PENDING_VERIFICATION, VERIFIED, CLOSED, WONT_FIX, FALSE_POSITIVE
- `priority` - LOW, MEDIUM, HIGH, CRITICAL, EMERGENCY
- `severity_source` - Original CVSS score from vulnerability
- `sla_deadline`, `sla_status` - SLA tracking (WITHIN_SLA, AT_RISK, BREACHED)
- `assigned_to`, `assigned_team`, `created_by` - Assignment tracking
- `effort_estimate_hours`, `actual_effort_hours` - Effort tracking
- Timeline: `due_date`, `start_date`, `completion_date`, `verification_date`

**Computed Properties:**
- `is_overdue` - Check if past SLA deadline
- `is_critical_priority` - Check if critical/emergency
- `is_completed` - Check if in completed state

**Methods:**
- `to_dict()` - API response format
- `to_qdrant_payload()` - Qdrant storage format

### 2. RemediationPlan
**Purpose:** Group multiple tasks into coordinated remediation plans.

**Key Fields:**
- `plan_id`, `customer_id`, `name`, `description`
- `status` - DRAFT, ACTIVE, COMPLETED, CANCELLED
- `task_ids`, `total_tasks`, `completed_tasks` - Task tracking
- `start_date`, `target_completion_date`, `actual_completion_date` - Timeline
- `owner`, `stakeholders` - Ownership
- `risk_reduction_target`, `actual_risk_reduction` - Risk metrics

**Computed Properties:**
- `completion_percentage` - Calculate % complete
- `is_completed` - Check if fully done
- `is_on_track` - Check if meeting target date

**Methods:**
- `to_dict()` - API response format

### 3. SLAPolicy
**Purpose:** Configure SLA policies and escalation rules.

**Key Fields:**
- `policy_id`, `customer_id`, `name`, `description`
- `severity_thresholds` - Dict mapping severity to hours (e.g., {"critical": 24, "high": 72})
- `escalation_levels` - List of EscalationLevel objects
- `working_hours_only`, `timezone` - Time calculation config
- `business_critical_multiplier` - Reduce SLA time for critical assets (default 0.5)
- `active` - Enable/disable policy

**Methods:**
- `get_sla_hours(severity, is_business_critical)` - Calculate SLA hours for severity
- `get_escalation_for_percentage(elapsed_percentage)` - Get escalation level
- `to_dict()` - API response format

### 4. EscalationLevel
**Purpose:** Define escalation thresholds and actions within SLA policy.

**Key Fields:**
- `level` - Escalation level number (1, 2, 3...)
- `threshold_percentage` - % of SLA elapsed to trigger (0.0-1.0)
- `notify_roles`, `notify_emails` - Notification targets
- `action` - NOTIFY, ESCALATE_MANAGER, ESCALATE_EXECUTIVE, AUTO_ASSIGN

**Methods:**
- `to_dict()` - API response format

### 5. RemediationMetrics
**Purpose:** Aggregate performance metrics for remediation activities.

**Key Fields:**
- `metrics_id`, `customer_id`
- `period_start`, `period_end` - Time period
- Task counts: `total_tasks`, `completed_tasks`, `open_tasks`, `overdue_tasks`
- `mttr_hours` - Mean Time To Remediate (overall)
- `mttr_by_severity` - MTTR breakdown by severity
- `sla_compliance_rate` - % of tasks meeting SLA (0.0-1.0)
- `sla_breaches` - Count of SLA breaches
- `tasks_by_status`, `tasks_by_priority` - Distribution dicts
- `vulnerability_backlog`, `backlog_trend` - Backlog tracking

**Computed Properties:**
- `completion_rate` - % of tasks completed
- `overdue_rate` - % of open tasks that are overdue

**Methods:**
- `to_dict()` - API response format

### 6. RemediationAction
**Purpose:** Audit trail for all actions on remediation tasks.

**Key Fields:**
- `action_id`, `task_id`, `customer_id`
- `action_type` - CREATED, ASSIGNED, STATUS_CHANGE, PRIORITY_CHANGE, COMMENT, ESCALATED, VERIFIED, CLOSED
- `performed_by`, `timestamp` - Who and when
- `previous_value`, `new_value`, `comment` - Change tracking

**Methods:**
- `to_dict()` - API response format
- `to_qdrant_payload()` - Qdrant storage format

## Enums

### TaskType
- PATCH, UPGRADE, CONFIGURATION, WORKAROUND, MITIGATION, REPLACEMENT

### TaskStatus
- OPEN, IN_PROGRESS, PENDING_VERIFICATION, VERIFIED, CLOSED, WONT_FIX, FALSE_POSITIVE

### TaskPriority
- LOW, MEDIUM, HIGH, CRITICAL, EMERGENCY

### SLAStatus
- WITHIN_SLA, AT_RISK, BREACHED

### EscalationAction
- NOTIFY, ESCALATE_MANAGER, ESCALATE_EXECUTIVE, AUTO_ASSIGN

### RemediationActionType
- CREATED, ASSIGNED, STATUS_CHANGE, PRIORITY_CHANGE, COMMENT, ESCALATED, VERIFIED, CLOSED

## Usage Example

```python
from api.remediation import (
    RemediationTask, RemediationPlan, SLAPolicy, EscalationLevel,
    TaskType, TaskStatus, TaskPriority, SLAStatus, EscalationAction
)
from datetime import datetime, date, timedelta

# Create SLA Policy
escalation = EscalationLevel(
    level=1,
    threshold_percentage=0.75,
    notify_roles=['security_team'],
    action=EscalationAction.NOTIFY
)

policy = SLAPolicy(
    policy_id='SLA-001',
    customer_id='CUST-A',
    name='Standard Remediation SLA',
    severity_thresholds={
        'critical': 24,
        'high': 72,
        'medium': 168,
        'low': 720
    },
    escalation_levels=[escalation]
)

# Create Remediation Task
task = RemediationTask(
    task_id='TASK-001',
    customer_id='CUST-A',
    title='Patch CVE-2024-1234',
    description='Apply security patch',
    cve_id='CVE-2024-1234',
    task_type=TaskType.PATCH,
    priority=TaskPriority.CRITICAL,
    severity_source=9.8,
    sla_deadline=datetime.utcnow() + timedelta(hours=24)
)

# Check status
if task.is_overdue:
    print(f"Task {task.task_id} is overdue!")

# Create Remediation Plan
plan = RemediationPlan(
    plan_id='PLAN-001',
    customer_id='CUST-A',
    name='Q4 Vulnerability Remediation',
    task_ids=['TASK-001', 'TASK-002'],
    total_tasks=2,
    start_date=date.today()
)

# Track metrics
metrics = RemediationMetrics(
    metrics_id='MET-001',
    customer_id='CUST-A',
    period_start=date.today() - timedelta(days=30),
    period_end=date.today(),
    total_tasks=50,
    completed_tasks=42,
    sla_compliance_rate=0.92
)
```

## File Structure

```
api/remediation/
├── __init__.py              # Package exports
├── remediation_models.py    # Complete data models
└── README.md               # This file
```

## Validation

All models include:
- ✅ Required field validation in `__post_init__`
- ✅ Value normalization (strip whitespace)
- ✅ Computed properties for common queries
- ✅ `to_dict()` method for API responses
- ✅ `to_qdrant_payload()` method for vector storage (where applicable)
- ✅ Multi-tenant isolation via `customer_id`

## Testing

Run validation test:
```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
python3 -c "from api.remediation import *; print('✅ Import successful')"
```

## Integration Points

### With E03: SBOM Analysis
- `RemediationTask.vulnerability_id` links to `SoftwareVulnerability`
- `RemediationTask.cve_id` references CVE from SBOM vulnerabilities

### With E15: Vendor Equipment
- `RemediationTask.asset_ids` references equipment/assets
- Tasks can target specific vendor equipment models

### With Customer Isolation
- All models include `customer_id` for multi-tenant isolation
- Qdrant payloads include customer_id for filtered queries

## Next Steps (E06 API Implementation)

1. **E06_API_Operations.py** - API endpoint handlers
2. **E06_Service_Layer.py** - Business logic and workflows
3. **E06_Repository.py** - Qdrant storage operations
4. **E06_SLA_Calculator.py** - SLA deadline calculation
5. **E06_Escalation_Engine.py** - Automatic escalation handling
6. **E06_Metrics_Aggregator.py** - Performance metrics calculation

---

**Status:** ✅ Complete and validated
**Location:** `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/api/remediation/`
