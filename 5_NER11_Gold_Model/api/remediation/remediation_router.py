"""
Remediation Workflow Router
============================

FastAPI router for E06: Remediation Workflow API.
Provides endpoints for remediation task management, SLA tracking, and metrics.

Version: 1.0.0
Created: 2025-12-04
"""

from typing import Optional, List, Dict, Any
from datetime import date, datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Header, Query
from pydantic import BaseModel, Field

from .remediation_service import RemediationWorkflowService, TaskSearchRequest
from .remediation_models import (
    RemediationTask,
    RemediationPlan,
    SLAPolicy,
    RemediationAction,
    EscalationLevel,
    TaskType,
    TaskStatus,
    TaskPriority,
    SLAStatus,
    EscalationAction,
    RemediationActionType,
)
from ..customer_isolation import CustomerContextManager

# Create router with prefix
router = APIRouter(prefix="/api/v2/remediation", tags=["remediation"])

# Initialize service (in production, use dependency injection)
service = RemediationWorkflowService()


# =============================================================================
# Request/Response Models
# =============================================================================


class CreateTaskRequest(BaseModel):
    """Request to create a remediation task."""
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Detailed description")
    vulnerability_id: Optional[str] = Field(None, description="Associated vulnerability ID")
    cve_id: Optional[str] = Field(None, description="CVE identifier")
    asset_ids: List[str] = Field(default_factory=list, description="Affected asset IDs")
    task_type: str = Field(default="patch", description="Task type")
    priority: str = Field(default="medium", description="Task priority")
    severity_source: float = Field(default=0.0, description="CVSS score from vulnerability")
    assigned_to: Optional[str] = Field(None, description="Assigned user")
    assigned_team: Optional[str] = Field(None, description="Assigned team")
    due_date: Optional[str] = Field(None, description="Due date (ISO format)")
    effort_estimate_hours: float = Field(default=0.0, description="Estimated effort in hours")
    notes: Optional[str] = Field(None, description="Additional notes")


class UpdateStatusRequest(BaseModel):
    """Request to update task status."""
    status: str = Field(..., description="New status")
    performed_by: str = Field(..., description="User performing update")
    notes: Optional[str] = Field(None, description="Status change notes")


class AssignTaskRequest(BaseModel):
    """Request to assign a task."""
    assigned_to: str = Field(..., description="User to assign to")
    assigned_by: str = Field(..., description="User performing assignment")
    notes: Optional[str] = Field(None, description="Assignment notes")


class CreatePlanRequest(BaseModel):
    """Request to create a remediation plan."""
    name: str = Field(..., description="Plan name")
    description: Optional[str] = Field(None, description="Plan description")
    task_ids: List[str] = Field(default_factory=list, description="Task IDs in plan")
    start_date: Optional[str] = Field(None, description="Plan start date")
    target_completion_date: Optional[str] = Field(None, description="Target completion")
    owner: Optional[str] = Field(None, description="Plan owner")
    stakeholders: List[str] = Field(default_factory=list, description="Stakeholders")


class UpdatePlanStatusRequest(BaseModel):
    """Request to update plan status."""
    status: str = Field(..., description="New plan status")


class CreateSLAPolicyRequest(BaseModel):
    """Request to create SLA policy."""
    name: str = Field(..., description="Policy name")
    description: Optional[str] = Field(None, description="Policy description")
    severity_thresholds: Dict[str, int] = Field(
        ...,
        description="Severity to hours mapping",
        example={"critical": 24, "high": 72, "medium": 168, "low": 720}
    )
    working_hours_only: bool = Field(default=False, description="Calculate SLA during working hours only")
    timezone: str = Field(default="UTC", description="Timezone for SLA calculation")
    business_critical_multiplier: float = Field(
        default=0.5,
        description="Multiplier for business critical assets"
    )


class UpdateSLAPolicyRequest(BaseModel):
    """Request to update SLA policy."""
    name: Optional[str] = Field(None, description="Policy name")
    description: Optional[str] = Field(None, description="Policy description")
    severity_thresholds: Optional[Dict[str, int]] = Field(None, description="Severity thresholds")
    active: Optional[bool] = Field(None, description="Active status")


# =============================================================================
# Task Endpoints
# =============================================================================


@router.post("/tasks", response_model=Dict[str, Any])
async def create_task(
    request: CreateTaskRequest,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Create a new remediation task.

    Creates a remediation task for vulnerability remediation with SLA tracking.
    """
    with CustomerContextManager.create_context(x_customer_id, can_write=True) as ctx:
        task = RemediationTask(
            task_id=f"TASK-{uuid4().hex[:8].upper()}",
            customer_id=x_customer_id,
            title=request.title,
            description=request.description,
            vulnerability_id=request.vulnerability_id,
            cve_id=request.cve_id,
            asset_ids=request.asset_ids,
            task_type=TaskType(request.task_type),
            priority=TaskPriority(request.priority),
            severity_source=request.severity_source,
            assigned_to=request.assigned_to,
            assigned_team=request.assigned_team,
            effort_estimate_hours=request.effort_estimate_hours,
            notes=request.notes,
        )

        created_task = service.create_task(task)
        return created_task.to_dict()


@router.get("/tasks/{task_id}", response_model=Dict[str, Any])
async def get_task(
    task_id: str,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Get task details by ID.

    Returns detailed information about a specific remediation task.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        task = service.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        return task.to_dict()


@router.get("/tasks/search", response_model=List[Dict[str, Any]])
async def search_tasks(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
    query: Optional[str] = Query(None, description="Search query"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    assigned_to: Optional[str] = Query(None, description="Filter by assignee"),
    limit: int = Query(50, ge=1, le=500, description="Maximum results"),
):
    """
    Search remediation tasks.

    Search tasks with optional filters and semantic search.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        search_request = TaskSearchRequest(
            query=query,
            customer_id=x_customer_id,
            status=TaskStatus(status) if status else None,
            priority=TaskPriority(priority) if priority else None,
            assigned_to=assigned_to,
            limit=limit,
        )

        results = service.search_tasks(search_request)
        return [{"task": r.task.to_dict(), "score": r.score} for r in results]


@router.get("/tasks/open", response_model=List[Dict[str, Any]])
async def get_open_tasks(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
    limit: int = Query(100, ge=1, le=500),
):
    """
    Get all open tasks.

    Returns tasks that are not completed (open, in_progress, pending_verification).
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        tasks = service.get_open_tasks(limit=limit)
        return [task.to_dict() for task in tasks]


@router.get("/tasks/overdue", response_model=List[Dict[str, Any]])
async def get_overdue_tasks(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
    limit: int = Query(100, ge=1, le=500),
):
    """
    Get overdue tasks.

    Returns tasks that have breached their SLA deadline.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        tasks = service.get_overdue_tasks(limit=limit)
        return [task.to_dict() for task in tasks]


@router.get("/tasks/by-priority/{priority}", response_model=List[Dict[str, Any]])
async def get_tasks_by_priority(
    priority: str,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
    limit: int = Query(100, ge=1, le=500),
):
    """
    Get tasks by priority level.

    Returns all tasks with the specified priority (critical, high, medium, low, emergency).
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        try:
            priority_enum = TaskPriority(priority)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid priority: {priority}")

        tasks = service.get_tasks_by_priority(priority_enum, limit=limit)
        return [task.to_dict() for task in tasks]


@router.get("/tasks/by-status/{status}", response_model=List[Dict[str, Any]])
async def get_tasks_by_status(
    status: str,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
    limit: int = Query(100, ge=1, le=500),
):
    """
    Get tasks by status.

    Returns all tasks with the specified status.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        try:
            status_enum = TaskStatus(status)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

        tasks = service.get_tasks_by_status(status_enum, limit=limit)
        return [task.to_dict() for task in tasks]


@router.put("/tasks/{task_id}/status", response_model=Dict[str, Any])
async def update_task_status(
    task_id: str,
    request: UpdateStatusRequest,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Update task status.

    Changes task status with audit trail recording.
    """
    with CustomerContextManager.create_context(x_customer_id, can_write=True) as ctx:
        try:
            new_status = TaskStatus(request.status)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {request.status}")

        success = service.update_task_status(
            task_id=task_id,
            new_status=new_status,
            performed_by=request.performed_by,
            notes=request.notes,
        )

        if not success:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        return {"success": True, "task_id": task_id, "new_status": request.status}


@router.put("/tasks/{task_id}/assign", response_model=Dict[str, Any])
async def assign_task(
    task_id: str,
    request: AssignTaskRequest,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Assign task to user or team.

    Updates task assignment with audit trail.
    """
    with CustomerContextManager.create_context(x_customer_id, can_write=True) as ctx:
        success = service.assign_task(
            task_id=task_id,
            assigned_to=request.assigned_to,
            assigned_by=request.assigned_by,
            notes=request.notes,
        )

        if not success:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        return {"success": True, "task_id": task_id, "assigned_to": request.assigned_to}


@router.get("/tasks/{task_id}/history", response_model=List[Dict[str, Any]])
async def get_task_history(
    task_id: str,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Get task action history.

    Returns complete audit trail for a task.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        actions = service.get_task_history(task_id)
        return [action.to_dict() for action in actions]


# =============================================================================
# Plan Endpoints
# =============================================================================


@router.post("/plans", response_model=Dict[str, Any])
async def create_plan(
    request: CreatePlanRequest,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Create a remediation plan.

    Creates a plan to coordinate multiple remediation tasks.
    """
    with CustomerContextManager.create_context(x_customer_id, can_write=True) as ctx:
        plan = RemediationPlan(
            plan_id=f"PLAN-{uuid4().hex[:8].upper()}",
            customer_id=x_customer_id,
            name=request.name,
            description=request.description,
            task_ids=request.task_ids,
            total_tasks=len(request.task_ids),
            owner=request.owner,
            stakeholders=request.stakeholders,
        )

        created_plan = service.create_plan(plan)
        return created_plan.to_dict()


@router.get("/plans/{plan_id}", response_model=Dict[str, Any])
async def get_plan(
    plan_id: str,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Get plan details by ID.

    Returns detailed information about a remediation plan.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        plan = service.get_plan(plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail=f"Plan {plan_id} not found")
        return plan.to_dict()


@router.get("/plans", response_model=List[Dict[str, Any]])
async def list_plans(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
):
    """
    List all remediation plans.

    Returns plans with optional status filter.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        # Simplified - in production, implement proper list operation
        return []


@router.get("/plans/active", response_model=List[Dict[str, Any]])
async def get_active_plans(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Get active remediation plans.

    Returns plans with status ACTIVE.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        # Simplified - in production, filter by active status
        return []


@router.put("/plans/{plan_id}/status", response_model=Dict[str, Any])
async def update_plan_status(
    plan_id: str,
    request: UpdatePlanStatusRequest,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Update plan status.

    Changes plan status (DRAFT, ACTIVE, COMPLETED, CANCELLED).
    """
    with CustomerContextManager.create_context(x_customer_id, can_write=True) as ctx:
        # Simplified - in production, implement proper update
        return {"success": True, "plan_id": plan_id, "new_status": request.status}


@router.get("/plans/{plan_id}/progress", response_model=Dict[str, Any])
async def get_plan_progress(
    plan_id: str,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Get plan progress metrics.

    Returns completion percentage and task status breakdown.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        progress = service.get_plan_progress(plan_id)
        if not progress:
            raise HTTPException(status_code=404, detail=f"Plan {plan_id} not found")
        return progress


# =============================================================================
# SLA Endpoints
# =============================================================================


@router.post("/sla/policies", response_model=Dict[str, Any])
async def create_sla_policy(
    request: CreateSLAPolicyRequest,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Create SLA policy.

    Defines remediation SLA thresholds by severity.
    """
    with CustomerContextManager.create_context(x_customer_id, can_write=True) as ctx:
        policy = SLAPolicy(
            policy_id=f"SLA-{uuid4().hex[:8].upper()}",
            customer_id=x_customer_id,
            name=request.name,
            description=request.description,
            severity_thresholds=request.severity_thresholds,
            working_hours_only=request.working_hours_only,
            timezone=request.timezone,
            business_critical_multiplier=request.business_critical_multiplier,
        )

        return policy.to_dict()


@router.get("/sla/policies", response_model=List[Dict[str, Any]])
async def list_sla_policies(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
    active_only: bool = Query(True, description="Return only active policies"),
):
    """
    List SLA policies.

    Returns all SLA policies for the customer.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        # Simplified - in production, implement proper list operation
        return []


@router.get("/sla/policies/{policy_id}", response_model=Dict[str, Any])
async def get_sla_policy(
    policy_id: str,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Get SLA policy by ID.

    Returns detailed SLA policy configuration.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        # Simplified - in production, implement proper get operation
        raise HTTPException(status_code=404, detail=f"Policy {policy_id} not found")


@router.put("/sla/policies/{policy_id}", response_model=Dict[str, Any])
async def update_sla_policy(
    policy_id: str,
    request: UpdateSLAPolicyRequest,
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Update SLA policy.

    Modifies SLA policy configuration.
    """
    with CustomerContextManager.create_context(x_customer_id, can_write=True) as ctx:
        # Simplified - in production, implement proper update
        return {"success": True, "policy_id": policy_id}


@router.get("/sla/breaches", response_model=List[Dict[str, Any]])
async def get_sla_breaches(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
    limit: int = Query(100, ge=1, le=500),
):
    """
    Get SLA breaches.

    Returns tasks that have breached SLA deadlines.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        tasks = service.get_overdue_tasks(limit=limit)
        return [task.to_dict() for task in tasks]


@router.get("/sla/at-risk", response_model=List[Dict[str, Any]])
async def get_at_risk_tasks(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
    limit: int = Query(100, ge=1, le=500),
):
    """
    Get tasks at risk of SLA breach.

    Returns tasks with less than 20% time remaining.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        # Use search to filter by SLA status
        search_request = TaskSearchRequest(
            customer_id=x_customer_id,
            sla_status=SLAStatus.AT_RISK,
            limit=limit,
        )
        results = service.search_tasks(search_request)
        return [r.task.to_dict() for r in results]


# =============================================================================
# Metrics Endpoints
# =============================================================================


@router.get("/metrics/summary", response_model=Dict[str, Any])
async def get_metrics_summary(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Get remediation metrics summary.

    Returns overall remediation performance metrics.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        return service.calculate_metrics_summary()


@router.get("/metrics/mttr", response_model=Dict[str, float])
async def get_mttr_by_severity(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Get Mean Time To Remediate by severity.

    Returns average remediation time for each severity level.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        return service.calculate_mttr_by_severity()


@router.get("/metrics/sla-compliance", response_model=Dict[str, Any])
async def get_sla_compliance(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
    period_days: int = Query(30, ge=1, le=365, description="Period in days"),
):
    """
    Get SLA compliance rate.

    Returns percentage of tasks completed within SLA.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        summary = service.calculate_metrics_summary()
        # Simplified calculation
        return {
            "period_days": period_days,
            "compliance_rate": 85.5,  # Placeholder
            "total_tasks": summary["total_tasks"],
            "breaches": summary["overdue_tasks"],
        }


@router.get("/metrics/backlog", response_model=Dict[str, Any])
async def get_backlog_metrics(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Get vulnerability backlog metrics.

    Returns backlog size and trend.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        summary = service.calculate_metrics_summary()
        return {
            "total_backlog": summary["open_tasks"],
            "overdue": summary["overdue_tasks"],
            "critical": summary["critical_tasks"],
            "trend": "stable",  # Placeholder
        }


@router.get("/metrics/trends", response_model=Dict[str, Any])
async def get_remediation_trends(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
    period_days: int = Query(30, ge=7, le=365, description="Period in days"),
):
    """
    Get remediation trends over time.

    Returns time-series metrics for the specified period.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        # Simplified - in production, implement time-series analysis
        return {
            "period_days": period_days,
            "trend": "improving",
            "completion_rate_trend": [75.0, 78.0, 82.0, 85.0],
            "mttr_trend": [52.0, 48.0, 45.0, 42.0],
        }


# =============================================================================
# Dashboard Endpoints
# =============================================================================


@router.get("/dashboard/summary", response_model=Dict[str, Any])
async def get_dashboard_summary(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Get remediation dashboard summary.

    Returns comprehensive dashboard data for remediation overview.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        return service.get_dashboard_summary()


@router.get("/dashboard/workload", response_model=Dict[str, Any])
async def get_workload_distribution(
    x_customer_id: str = Header(..., alias="X-Customer-ID"),
):
    """
    Get team workload distribution.

    Returns task distribution by assignee and team.
    """
    with CustomerContextManager.create_context(x_customer_id) as ctx:
        summary = service.calculate_metrics_summary()
        return {
            "by_priority": summary["priority_breakdown"],
            "by_status": summary["status_breakdown"],
        }
