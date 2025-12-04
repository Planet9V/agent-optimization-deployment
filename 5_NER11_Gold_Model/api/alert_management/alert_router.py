"""
Alert Management API Router
============================

FastAPI router for E09: Alert Management.
Provides REST endpoints for alerts, alert rules, notification rules,
escalation policies, alert correlations, and dashboard summary.

Version: 1.0.0
Created: 2025-12-04
"""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Header, Depends
from pydantic import BaseModel, Field
import logging

from ..customer_isolation import (
    CustomerContext,
    CustomerContextManager,
    CustomerAccessLevel,
)
from .alert_service import (
    AlertService,
    AlertSearchRequest,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/alerts", tags=["alert-management"])


# =============================================================================
# Pydantic Request/Response Models
# =============================================================================


# ===== Alert Models =====

class AlertCreate(BaseModel):
    """Request model for alert creation."""
    alert_id: str = Field(..., description="Unique alert identifier")
    title: str = Field(..., description="Alert title")
    description: Optional[str] = Field(None, description="Alert description")
    severity: str = Field("medium", description="Severity: low, medium, high, critical")
    status: str = Field("open", description="Status: open, acknowledged, investigating, resolved, closed")
    source: str = Field(..., description="Alert source system")
    event_type: str = Field(..., description="Type of event")
    affected_assets: List[str] = Field(default_factory=list, description="Affected asset IDs")
    tags: List[str] = Field(default_factory=list, description="Classification tags")
    metadata: dict = Field(default_factory=dict, description="Additional metadata")


class AlertUpdate(BaseModel):
    """Request model for alert update."""
    title: Optional[str] = Field(None, description="Alert title")
    description: Optional[str] = Field(None, description="Alert description")
    severity: Optional[str] = Field(None, description="Severity level")
    status: Optional[str] = Field(None, description="Alert status")
    tags: Optional[List[str]] = Field(None, description="Classification tags")
    metadata: Optional[dict] = Field(None, description="Additional metadata")


class AlertResponse(BaseModel):
    """Response model for alert data."""
    alert_id: str
    customer_id: str
    title: str
    description: Optional[str]
    severity: str
    status: str
    source: str
    event_type: str
    affected_assets: List[str]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    assigned_to: Optional[str]
    acknowledged_at: Optional[datetime]
    resolved_at: Optional[datetime]


class AlertSearchResponse(BaseModel):
    """Response for alert search results."""
    total_results: int
    customer_id: str
    results: List[AlertResponse]


class AlertAssignment(BaseModel):
    """Request model for alert assignment."""
    assigned_to: str = Field(..., description="User ID to assign alert to")
    notes: Optional[str] = Field(None, description="Assignment notes")


# ===== Alert Rule Models =====

class AlertRuleCreate(BaseModel):
    """Request model for alert rule creation."""
    rule_id: str = Field(..., description="Unique rule identifier")
    name: str = Field(..., description="Rule name")
    description: Optional[str] = Field(None, description="Rule description")
    enabled: bool = Field(True, description="Is rule enabled?")
    severity: str = Field("medium", description="Alert severity to generate")
    conditions: dict = Field(..., description="Rule conditions (JSON)")
    actions: List[dict] = Field(default_factory=list, description="Actions to execute")


class AlertRuleUpdate(BaseModel):
    """Request model for alert rule update."""
    name: Optional[str] = Field(None, description="Rule name")
    description: Optional[str] = Field(None, description="Rule description")
    enabled: Optional[bool] = Field(None, description="Is rule enabled?")
    severity: Optional[str] = Field(None, description="Alert severity")
    conditions: Optional[dict] = Field(None, description="Rule conditions")
    actions: Optional[List[dict]] = Field(None, description="Actions to execute")


class AlertRuleResponse(BaseModel):
    """Response model for alert rule."""
    rule_id: str
    customer_id: str
    name: str
    description: Optional[str]
    enabled: bool
    severity: str
    conditions: dict
    actions: List[dict]
    created_at: datetime
    updated_at: datetime
    triggered_count: int


class AlertRuleListResponse(BaseModel):
    """Response for listing alert rules."""
    total_results: int
    customer_id: str
    rules: List[AlertRuleResponse]


# ===== Notification Rule Models =====

class NotificationRuleCreate(BaseModel):
    """Request model for notification rule creation."""
    notification_id: str = Field(..., description="Unique notification rule identifier")
    name: str = Field(..., description="Notification rule name")
    enabled: bool = Field(True, description="Is notification enabled?")
    channels: List[str] = Field(..., description="Notification channels: email, slack, webhook, sms")
    severity_filter: Optional[List[str]] = Field(None, description="Filter by severities")
    event_type_filter: Optional[List[str]] = Field(None, description="Filter by event types")
    recipients: List[str] = Field(..., description="Recipient identifiers")
    configuration: dict = Field(default_factory=dict, description="Channel-specific configuration")


class NotificationRuleUpdate(BaseModel):
    """Request model for notification rule update."""
    name: Optional[str] = Field(None, description="Notification rule name")
    enabled: Optional[bool] = Field(None, description="Is notification enabled?")
    channels: Optional[List[str]] = Field(None, description="Notification channels")
    severity_filter: Optional[List[str]] = Field(None, description="Severity filter")
    event_type_filter: Optional[List[str]] = Field(None, description="Event type filter")
    recipients: Optional[List[str]] = Field(None, description="Recipients")
    configuration: Optional[dict] = Field(None, description="Channel configuration")


class NotificationRuleResponse(BaseModel):
    """Response model for notification rule."""
    notification_id: str
    customer_id: str
    name: str
    enabled: bool
    channels: List[str]
    severity_filter: Optional[List[str]]
    event_type_filter: Optional[List[str]]
    recipients: List[str]
    configuration: dict
    created_at: datetime
    sent_count: int


class NotificationRuleListResponse(BaseModel):
    """Response for listing notification rules."""
    total_results: int
    customer_id: str
    notifications: List[NotificationRuleResponse]


# ===== Escalation Policy Models =====

class EscalationPolicyCreate(BaseModel):
    """Request model for escalation policy creation."""
    policy_id: str = Field(..., description="Unique policy identifier")
    name: str = Field(..., description="Policy name")
    description: Optional[str] = Field(None, description="Policy description")
    enabled: bool = Field(True, description="Is policy enabled?")
    escalation_levels: List[dict] = Field(..., description="Escalation level configurations")
    severity_filter: Optional[List[str]] = Field(None, description="Apply to specific severities")


class EscalationPolicyUpdate(BaseModel):
    """Request model for escalation policy update."""
    name: Optional[str] = Field(None, description="Policy name")
    description: Optional[str] = Field(None, description="Policy description")
    enabled: Optional[bool] = Field(None, description="Is policy enabled?")
    escalation_levels: Optional[List[dict]] = Field(None, description="Escalation levels")
    severity_filter: Optional[List[str]] = Field(None, description="Severity filter")


class EscalationPolicyResponse(BaseModel):
    """Response model for escalation policy."""
    policy_id: str
    customer_id: str
    name: str
    description: Optional[str]
    enabled: bool
    escalation_levels: List[dict]
    severity_filter: Optional[List[str]]
    created_at: datetime
    triggered_count: int


class EscalationPolicyListResponse(BaseModel):
    """Response for listing escalation policies."""
    total_results: int
    customer_id: str
    policies: List[EscalationPolicyResponse]


# ===== Correlation Models =====

class AlertCorrelationCreate(BaseModel):
    """Request model for alert correlation creation."""
    correlation_id: str = Field(..., description="Unique correlation identifier")
    name: str = Field(..., description="Correlation name")
    alert_ids: List[str] = Field(..., description="Correlated alert IDs")
    correlation_type: str = Field("pattern", description="Type: pattern, time, asset, causality")
    confidence: float = Field(0.8, ge=0.0, le=1.0, description="Correlation confidence")
    root_cause_alert_id: Optional[str] = Field(None, description="Root cause alert ID")
    description: Optional[str] = Field(None, description="Correlation description")


class AlertCorrelationResponse(BaseModel):
    """Response model for alert correlation."""
    correlation_id: str
    customer_id: str
    name: str
    alert_ids: List[str]
    correlation_type: str
    confidence: float
    root_cause_alert_id: Optional[str]
    created_at: datetime


class AlertCorrelationListResponse(BaseModel):
    """Response for listing alert correlations."""
    total_results: int
    customer_id: str
    correlations: List[AlertCorrelationResponse]


# ===== Dashboard Models =====

class AlertSummaryResponse(BaseModel):
    """Response for alert dashboard summary."""
    customer_id: str
    total_alerts: int
    open_alerts: int
    acknowledged_alerts: int
    investigating_alerts: int
    resolved_alerts: int
    critical_alerts: int
    high_alerts: int
    medium_alerts: int
    low_alerts: int
    alerts_last_24h: int
    active_correlations: int
    avg_resolution_time_minutes: float


# =============================================================================
# Dependencies
# =============================================================================


def get_service() -> AlertService:
    """Get alert service instance."""
    return AlertService()


def require_customer_context(
    x_customer_id: str = Header(..., description="Customer identifier"),
    x_namespace: Optional[str] = Header(None, description="Customer namespace"),
    x_user_id: Optional[str] = Header(None, description="User identifier"),
    x_access_level: Optional[str] = Header("read", description="Access level"),
) -> CustomerContext:
    """Extract and set customer context from headers."""
    try:
        access_level = CustomerAccessLevel(x_access_level.lower())
    except ValueError:
        access_level = CustomerAccessLevel.READ

    context = CustomerContextManager.create_context(
        customer_id=x_customer_id,
        namespace=x_namespace,
        access_level=access_level,
        user_id=x_user_id,
    )
    return context


# =============================================================================
# Alert Endpoints
# =============================================================================


@router.post("", response_model=AlertResponse, status_code=201)
async def create_alert(
    alert_data: AlertCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Create a new alert.

    Requires WRITE access level.
    """
    try:
        from .alert_models import Alert, AlertSeverity, AlertStatus

        alert = Alert(
            alert_id=alert_data.alert_id,
            customer_id=context.customer_id,
            title=alert_data.title,
            description=alert_data.description,
            severity=AlertSeverity(alert_data.severity),
            status=AlertStatus(alert_data.status),
            source=alert_data.source,
            event_type=alert_data.event_type,
            affected_assets=alert_data.affected_assets,
            tags=alert_data.tags,
            metadata=alert_data.metadata,
        )
        created = service.create_alert(alert)

        return AlertResponse(
            alert_id=created.alert_id,
            customer_id=created.customer_id,
            title=created.title,
            description=created.description,
            severity=created.severity.value,
            status=created.status.value,
            source=created.source,
            event_type=created.event_type,
            affected_assets=created.affected_assets,
            tags=created.tags,
            created_at=created.created_at,
            updated_at=created.updated_at,
            assigned_to=created.assigned_to,
            acknowledged_at=created.acknowledged_at,
            resolved_at=created.resolved_at,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """Get alert by ID with customer isolation."""
    alert = service.get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")

    return AlertResponse(
        alert_id=alert.alert_id,
        customer_id=alert.customer_id,
        title=alert.title,
        description=alert.description,
        severity=alert.severity.value if hasattr(alert.severity, 'value') else alert.severity,
        status=alert.status.value if hasattr(alert.status, 'value') else alert.status,
        source=alert.source,
        event_type=alert.event_type,
        affected_assets=alert.affected_assets,
        tags=alert.tags,
        created_at=alert.created_at,
        updated_at=alert.updated_at,
        assigned_to=alert.assigned_to,
        acknowledged_at=alert.acknowledged_at,
        resolved_at=alert.resolved_at,
    )


@router.put("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: str,
    update_data: AlertUpdate,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Update an existing alert.

    Requires WRITE access level.
    """
    try:
        updated = service.update_alert(alert_id, update_data.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")

        return AlertResponse(
            alert_id=updated.alert_id,
            customer_id=updated.customer_id,
            title=updated.title,
            description=updated.description,
            severity=updated.severity.value if hasattr(updated.severity, 'value') else updated.severity,
            status=updated.status.value if hasattr(updated.status, 'value') else updated.status,
            source=updated.source,
            event_type=updated.event_type,
            affected_assets=updated.affected_assets,
            tags=updated.tags,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
            assigned_to=updated.assigned_to,
            acknowledged_at=updated.acknowledged_at,
            resolved_at=updated.resolved_at,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{alert_id}", status_code=204)
async def delete_alert(
    alert_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Delete an alert.

    Requires ADMIN access level.
    """
    try:
        success = service.delete_alert(alert_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("", response_model=AlertSearchResponse)
async def list_alerts(
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: Optional[str] = Query(None, description="Filter by status"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    limit: int = Query(50, ge=1, le=500, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """List alerts with optional filters."""
    try:
        request = AlertSearchRequest(
            customer_id=context.customer_id,
            severity=severity,
            status=status,
            event_type=event_type,
            limit=limit,
        )
        results = service.search_alerts(request)

        alert_responses = [
            AlertResponse(
                alert_id=r.alert.alert_id,
                customer_id=r.alert.customer_id,
                title=r.alert.title,
                description=r.alert.description,
                severity=r.alert.severity.value if hasattr(r.alert.severity, 'value') else r.alert.severity,
                status=r.alert.status.value if hasattr(r.alert.status, 'value') else r.alert.status,
                source=r.alert.source,
                event_type=r.alert.event_type,
                affected_assets=r.alert.affected_assets,
                tags=r.alert.tags,
                created_at=r.alert.created_at,
                updated_at=r.alert.updated_at,
                assigned_to=r.alert.assigned_to,
                acknowledged_at=r.alert.acknowledged_at,
                resolved_at=r.alert.resolved_at,
            )
            for r in results
        ]

        return AlertSearchResponse(
            total_results=len(alert_responses),
            customer_id=context.customer_id,
            results=alert_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/by-severity/{severity}", response_model=AlertSearchResponse)
async def get_alerts_by_severity(
    severity: str,
    limit: int = Query(100, ge=1, le=500, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """Get alerts by severity level."""
    results = service.get_alerts_by_severity(severity, limit)

    alert_responses = [
        AlertResponse(
            alert_id=r.alert.alert_id,
            customer_id=r.alert.customer_id,
            title=r.alert.title,
            description=r.alert.description,
            severity=r.alert.severity.value if hasattr(r.alert.severity, 'value') else r.alert.severity,
            status=r.alert.status.value if hasattr(r.alert.status, 'value') else r.alert.status,
            source=r.alert.source,
            event_type=r.alert.event_type,
            affected_assets=r.alert.affected_assets,
            tags=r.alert.tags,
            created_at=r.alert.created_at,
            updated_at=r.alert.updated_at,
            assigned_to=r.alert.assigned_to,
            acknowledged_at=r.alert.acknowledged_at,
            resolved_at=r.alert.resolved_at,
        )
        for r in results
    ]

    return AlertSearchResponse(
        total_results=len(alert_responses),
        customer_id=context.customer_id,
        results=alert_responses,
    )


@router.get("/by-status/{status}", response_model=AlertSearchResponse)
async def get_alerts_by_status(
    status: str,
    limit: int = Query(100, ge=1, le=500, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """Get alerts by status."""
    results = service.get_alerts_by_status(status, limit)

    alert_responses = [
        AlertResponse(
            alert_id=r.alert.alert_id,
            customer_id=r.alert.customer_id,
            title=r.alert.title,
            description=r.alert.description,
            severity=r.alert.severity.value if hasattr(r.alert.severity, 'value') else r.alert.severity,
            status=r.alert.status.value if hasattr(r.alert.status, 'value') else r.alert.status,
            source=r.alert.source,
            event_type=r.alert.event_type,
            affected_assets=r.alert.affected_assets,
            tags=r.alert.tags,
            created_at=r.alert.created_at,
            updated_at=r.alert.updated_at,
            assigned_to=r.alert.assigned_to,
            acknowledged_at=r.alert.acknowledged_at,
            resolved_at=r.alert.resolved_at,
        )
        for r in results
    ]

    return AlertSearchResponse(
        total_results=len(alert_responses),
        customer_id=context.customer_id,
        results=alert_responses,
    )


@router.post("/{alert_id}/acknowledge", response_model=AlertResponse)
async def acknowledge_alert(
    alert_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Acknowledge an alert.

    Requires WRITE access level.
    """
    try:
        acknowledged = service.acknowledge_alert(alert_id, context.user_id)
        if not acknowledged:
            raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")

        return AlertResponse(
            alert_id=acknowledged.alert_id,
            customer_id=acknowledged.customer_id,
            title=acknowledged.title,
            description=acknowledged.description,
            severity=acknowledged.severity.value if hasattr(acknowledged.severity, 'value') else acknowledged.severity,
            status=acknowledged.status.value if hasattr(acknowledged.status, 'value') else acknowledged.status,
            source=acknowledged.source,
            event_type=acknowledged.event_type,
            affected_assets=acknowledged.affected_assets,
            tags=acknowledged.tags,
            created_at=acknowledged.created_at,
            updated_at=acknowledged.updated_at,
            assigned_to=acknowledged.assigned_to,
            acknowledged_at=acknowledged.acknowledged_at,
            resolved_at=acknowledged.resolved_at,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert(
    alert_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Resolve an alert.

    Requires WRITE access level.
    """
    try:
        resolved = service.resolve_alert(alert_id)
        if not resolved:
            raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")

        return AlertResponse(
            alert_id=resolved.alert_id,
            customer_id=resolved.customer_id,
            title=resolved.title,
            description=resolved.description,
            severity=resolved.severity.value if hasattr(resolved.severity, 'value') else resolved.severity,
            status=resolved.status.value if hasattr(resolved.status, 'value') else resolved.status,
            source=resolved.source,
            event_type=resolved.event_type,
            affected_assets=resolved.affected_assets,
            tags=resolved.tags,
            created_at=resolved.created_at,
            updated_at=resolved.updated_at,
            assigned_to=resolved.assigned_to,
            acknowledged_at=resolved.acknowledged_at,
            resolved_at=resolved.resolved_at,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/{alert_id}/assign", response_model=AlertResponse)
async def assign_alert(
    alert_id: str,
    assignment: AlertAssignment,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Assign an alert to a user.

    Requires WRITE access level.
    """
    try:
        assigned = service.assign_alert(alert_id, assignment.assigned_to)
        if not assigned:
            raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")

        return AlertResponse(
            alert_id=assigned.alert_id,
            customer_id=assigned.customer_id,
            title=assigned.title,
            description=assigned.description,
            severity=assigned.severity.value if hasattr(assigned.severity, 'value') else assigned.severity,
            status=assigned.status.value if hasattr(assigned.status, 'value') else assigned.status,
            source=assigned.source,
            event_type=assigned.event_type,
            affected_assets=assigned.affected_assets,
            tags=assigned.tags,
            created_at=assigned.created_at,
            updated_at=assigned.updated_at,
            assigned_to=assigned.assigned_to,
            acknowledged_at=assigned.acknowledged_at,
            resolved_at=assigned.resolved_at,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/search", response_model=AlertSearchResponse)
async def search_alerts_semantic(
    query: str = Query(..., description="Semantic search query"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """Semantic search for alerts."""
    try:
        request = AlertSearchRequest(
            query=query,
            customer_id=context.customer_id,
            limit=limit,
        )
        results = service.search_alerts(request)

        alert_responses = [
            AlertResponse(
                alert_id=r.alert.alert_id,
                customer_id=r.alert.customer_id,
                title=r.alert.title,
                description=r.alert.description,
                severity=r.alert.severity.value if hasattr(r.alert.severity, 'value') else r.alert.severity,
                status=r.alert.status.value if hasattr(r.alert.status, 'value') else r.alert.status,
                source=r.alert.source,
                event_type=r.alert.event_type,
                affected_assets=r.alert.affected_assets,
                tags=r.alert.tags,
                created_at=r.alert.created_at,
                updated_at=r.alert.updated_at,
                assigned_to=r.alert.assigned_to,
                acknowledged_at=r.alert.acknowledged_at,
                resolved_at=r.alert.resolved_at,
            )
            for r in results
        ]

        return AlertSearchResponse(
            total_results=len(alert_responses),
            customer_id=context.customer_id,
            results=alert_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =============================================================================
# Alert Rule Endpoints
# =============================================================================


@router.post("/rules", response_model=AlertRuleResponse, status_code=201)
async def create_alert_rule(
    rule_data: AlertRuleCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Create a new alert rule.

    Requires WRITE access level.
    """
    try:
        from .alert_models import AlertRule

        rule = AlertRule(
            rule_id=rule_data.rule_id,
            customer_id=context.customer_id,
            name=rule_data.name,
            description=rule_data.description,
            enabled=rule_data.enabled,
            severity=rule_data.severity,
            conditions=rule_data.conditions,
            actions=rule_data.actions,
        )
        created = service.create_alert_rule(rule)

        return AlertRuleResponse(
            rule_id=created.rule_id,
            customer_id=created.customer_id,
            name=created.name,
            description=created.description,
            enabled=created.enabled,
            severity=created.severity,
            conditions=created.conditions,
            actions=created.actions,
            created_at=created.created_at,
            updated_at=created.updated_at,
            triggered_count=created.triggered_count,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/rules/{rule_id}", response_model=AlertRuleResponse)
async def get_alert_rule(
    rule_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """Get alert rule by ID."""
    rule = service.get_alert_rule(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail=f"Alert rule {rule_id} not found")

    return AlertRuleResponse(
        rule_id=rule.rule_id,
        customer_id=rule.customer_id,
        name=rule.name,
        description=rule.description,
        enabled=rule.enabled,
        severity=rule.severity,
        conditions=rule.conditions,
        actions=rule.actions,
        created_at=rule.created_at,
        updated_at=rule.updated_at,
        triggered_count=rule.triggered_count,
    )


@router.put("/rules/{rule_id}", response_model=AlertRuleResponse)
async def update_alert_rule(
    rule_id: str,
    update_data: AlertRuleUpdate,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Update an alert rule.

    Requires WRITE access level.
    """
    try:
        updated = service.update_alert_rule(rule_id, update_data.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404, detail=f"Alert rule {rule_id} not found")

        return AlertRuleResponse(
            rule_id=updated.rule_id,
            customer_id=updated.customer_id,
            name=updated.name,
            description=updated.description,
            enabled=updated.enabled,
            severity=updated.severity,
            conditions=updated.conditions,
            actions=updated.actions,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
            triggered_count=updated.triggered_count,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/rules/{rule_id}", status_code=204)
async def delete_alert_rule(
    rule_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Delete an alert rule.

    Requires ADMIN access level.
    """
    try:
        success = service.delete_alert_rule(rule_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Alert rule {rule_id} not found")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/rules", response_model=AlertRuleListResponse)
async def list_alert_rules(
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """List alert rules."""
    rules = service.list_alert_rules(limit)

    rule_responses = [
        AlertRuleResponse(
            rule_id=r.rule_id,
            customer_id=r.customer_id,
            name=r.name,
            description=r.description,
            enabled=r.enabled,
            severity=r.severity,
            conditions=r.conditions,
            actions=r.actions,
            created_at=r.created_at,
            updated_at=r.updated_at,
            triggered_count=r.triggered_count,
        )
        for r in rules
    ]

    return AlertRuleListResponse(
        total_results=len(rule_responses),
        customer_id=context.customer_id,
        rules=rule_responses,
    )


@router.post("/rules/{rule_id}/enable", response_model=AlertRuleResponse)
async def enable_alert_rule(
    rule_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Enable an alert rule.

    Requires WRITE access level.
    """
    try:
        enabled = service.enable_alert_rule(rule_id)
        if not enabled:
            raise HTTPException(status_code=404, detail=f"Alert rule {rule_id} not found")

        return AlertRuleResponse(
            rule_id=enabled.rule_id,
            customer_id=enabled.customer_id,
            name=enabled.name,
            description=enabled.description,
            enabled=enabled.enabled,
            severity=enabled.severity,
            conditions=enabled.conditions,
            actions=enabled.actions,
            created_at=enabled.created_at,
            updated_at=enabled.updated_at,
            triggered_count=enabled.triggered_count,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/rules/{rule_id}/disable", response_model=AlertRuleResponse)
async def disable_alert_rule(
    rule_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Disable an alert rule.

    Requires WRITE access level.
    """
    try:
        disabled = service.disable_alert_rule(rule_id)
        if not disabled:
            raise HTTPException(status_code=404, detail=f"Alert rule {rule_id} not found")

        return AlertRuleResponse(
            rule_id=disabled.rule_id,
            customer_id=disabled.customer_id,
            name=disabled.name,
            description=disabled.description,
            enabled=disabled.enabled,
            severity=disabled.severity,
            conditions=disabled.conditions,
            actions=disabled.actions,
            created_at=disabled.created_at,
            updated_at=disabled.updated_at,
            triggered_count=disabled.triggered_count,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# =============================================================================
# Notification Rule Endpoints
# =============================================================================


@router.post("/notifications", response_model=NotificationRuleResponse, status_code=201)
async def create_notification_rule(
    notification_data: NotificationRuleCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Create a new notification rule.

    Requires WRITE access level.
    """
    try:
        from .alert_models import NotificationRule

        notification = NotificationRule(
            notification_id=notification_data.notification_id,
            customer_id=context.customer_id,
            name=notification_data.name,
            enabled=notification_data.enabled,
            channels=notification_data.channels,
            severity_filter=notification_data.severity_filter,
            event_type_filter=notification_data.event_type_filter,
            recipients=notification_data.recipients,
            configuration=notification_data.configuration,
        )
        created = service.create_notification_rule(notification)

        return NotificationRuleResponse(
            notification_id=created.notification_id,
            customer_id=created.customer_id,
            name=created.name,
            enabled=created.enabled,
            channels=created.channels,
            severity_filter=created.severity_filter,
            event_type_filter=created.event_type_filter,
            recipients=created.recipients,
            configuration=created.configuration,
            created_at=created.created_at,
            sent_count=created.sent_count,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/notifications/{notification_id}", response_model=NotificationRuleResponse)
async def get_notification_rule(
    notification_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """Get notification rule by ID."""
    notification = service.get_notification_rule(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail=f"Notification rule {notification_id} not found")

    return NotificationRuleResponse(
        notification_id=notification.notification_id,
        customer_id=notification.customer_id,
        name=notification.name,
        enabled=notification.enabled,
        channels=notification.channels,
        severity_filter=notification.severity_filter,
        event_type_filter=notification.event_type_filter,
        recipients=notification.recipients,
        configuration=notification.configuration,
        created_at=notification.created_at,
        sent_count=notification.sent_count,
    )


@router.put("/notifications/{notification_id}", response_model=NotificationRuleResponse)
async def update_notification_rule(
    notification_id: str,
    update_data: NotificationRuleUpdate,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Update a notification rule.

    Requires WRITE access level.
    """
    try:
        updated = service.update_notification_rule(notification_id, update_data.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404, detail=f"Notification rule {notification_id} not found")

        return NotificationRuleResponse(
            notification_id=updated.notification_id,
            customer_id=updated.customer_id,
            name=updated.name,
            enabled=updated.enabled,
            channels=updated.channels,
            severity_filter=updated.severity_filter,
            event_type_filter=updated.event_type_filter,
            recipients=updated.recipients,
            configuration=updated.configuration,
            created_at=updated.created_at,
            sent_count=updated.sent_count,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/notifications/{notification_id}", status_code=204)
async def delete_notification_rule(
    notification_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Delete a notification rule.

    Requires ADMIN access level.
    """
    try:
        success = service.delete_notification_rule(notification_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Notification rule {notification_id} not found")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/notifications", response_model=NotificationRuleListResponse)
async def list_notification_rules(
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """List notification rules."""
    notifications = service.list_notification_rules(limit)

    notification_responses = [
        NotificationRuleResponse(
            notification_id=n.notification_id,
            customer_id=n.customer_id,
            name=n.name,
            enabled=n.enabled,
            channels=n.channels,
            severity_filter=n.severity_filter,
            event_type_filter=n.event_type_filter,
            recipients=n.recipients,
            configuration=n.configuration,
            created_at=n.created_at,
            sent_count=n.sent_count,
        )
        for n in notifications
    ]

    return NotificationRuleListResponse(
        total_results=len(notification_responses),
        customer_id=context.customer_id,
        notifications=notification_responses,
    )


# =============================================================================
# Escalation Policy Endpoints
# =============================================================================


@router.post("/escalations", response_model=EscalationPolicyResponse, status_code=201)
async def create_escalation_policy(
    policy_data: EscalationPolicyCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Create a new escalation policy.

    Requires WRITE access level.
    """
    try:
        from .alert_models import EscalationPolicy

        policy = EscalationPolicy(
            policy_id=policy_data.policy_id,
            customer_id=context.customer_id,
            name=policy_data.name,
            description=policy_data.description,
            enabled=policy_data.enabled,
            escalation_levels=policy_data.escalation_levels,
            severity_filter=policy_data.severity_filter,
        )
        created = service.create_escalation_policy(policy)

        return EscalationPolicyResponse(
            policy_id=created.policy_id,
            customer_id=created.customer_id,
            name=created.name,
            description=created.description,
            enabled=created.enabled,
            escalation_levels=created.escalation_levels,
            severity_filter=created.severity_filter,
            created_at=created.created_at,
            triggered_count=created.triggered_count,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/escalations/{policy_id}", response_model=EscalationPolicyResponse)
async def get_escalation_policy(
    policy_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """Get escalation policy by ID."""
    policy = service.get_escalation_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail=f"Escalation policy {policy_id} not found")

    return EscalationPolicyResponse(
        policy_id=policy.policy_id,
        customer_id=policy.customer_id,
        name=policy.name,
        description=policy.description,
        enabled=policy.enabled,
        escalation_levels=policy.escalation_levels,
        severity_filter=policy.severity_filter,
        created_at=policy.created_at,
        triggered_count=policy.triggered_count,
    )


@router.put("/escalations/{policy_id}", response_model=EscalationPolicyResponse)
async def update_escalation_policy(
    policy_id: str,
    update_data: EscalationPolicyUpdate,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Update an escalation policy.

    Requires WRITE access level.
    """
    try:
        updated = service.update_escalation_policy(policy_id, update_data.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404, detail=f"Escalation policy {policy_id} not found")

        return EscalationPolicyResponse(
            policy_id=updated.policy_id,
            customer_id=updated.customer_id,
            name=updated.name,
            description=updated.description,
            enabled=updated.enabled,
            escalation_levels=updated.escalation_levels,
            severity_filter=updated.severity_filter,
            created_at=updated.created_at,
            triggered_count=updated.triggered_count,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/escalations/{policy_id}", status_code=204)
async def delete_escalation_policy(
    policy_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Delete an escalation policy.

    Requires ADMIN access level.
    """
    try:
        success = service.delete_escalation_policy(policy_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Escalation policy {policy_id} not found")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/escalations", response_model=EscalationPolicyListResponse)
async def list_escalation_policies(
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """List escalation policies."""
    policies = service.list_escalation_policies(limit)

    policy_responses = [
        EscalationPolicyResponse(
            policy_id=p.policy_id,
            customer_id=p.customer_id,
            name=p.name,
            description=p.description,
            enabled=p.enabled,
            escalation_levels=p.escalation_levels,
            severity_filter=p.severity_filter,
            created_at=p.created_at,
            triggered_count=p.triggered_count,
        )
        for p in policies
    ]

    return EscalationPolicyListResponse(
        total_results=len(policy_responses),
        customer_id=context.customer_id,
        policies=policy_responses,
    )


# =============================================================================
# Alert Correlation Endpoints
# =============================================================================


@router.post("/correlations", response_model=AlertCorrelationResponse, status_code=201)
async def create_alert_correlation(
    correlation_data: AlertCorrelationCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """
    Create a new alert correlation.

    Requires WRITE access level.
    """
    try:
        from .alert_models import AlertCorrelation

        correlation = AlertCorrelation(
            correlation_id=correlation_data.correlation_id,
            customer_id=context.customer_id,
            name=correlation_data.name,
            alert_ids=correlation_data.alert_ids,
            correlation_type=correlation_data.correlation_type,
            confidence=correlation_data.confidence,
            root_cause_alert_id=correlation_data.root_cause_alert_id,
            description=correlation_data.description,
        )
        created = service.create_alert_correlation(correlation)

        return AlertCorrelationResponse(
            correlation_id=created.correlation_id,
            customer_id=created.customer_id,
            name=created.name,
            alert_ids=created.alert_ids,
            correlation_type=created.correlation_type,
            confidence=created.confidence,
            root_cause_alert_id=created.root_cause_alert_id,
            created_at=created.created_at,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/correlations", response_model=AlertCorrelationListResponse)
async def list_alert_correlations(
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """List alert correlations."""
    correlations = service.list_alert_correlations(limit)

    correlation_responses = [
        AlertCorrelationResponse(
            correlation_id=c.correlation_id,
            customer_id=c.customer_id,
            name=c.name,
            alert_ids=c.alert_ids,
            correlation_type=c.correlation_type,
            confidence=c.confidence,
            root_cause_alert_id=c.root_cause_alert_id,
            created_at=c.created_at,
        )
        for c in correlations
    ]

    return AlertCorrelationListResponse(
        total_results=len(correlation_responses),
        customer_id=context.customer_id,
        correlations=correlation_responses,
    )


@router.get("/correlations/{correlation_id}", response_model=AlertCorrelationResponse)
async def get_alert_correlation(
    correlation_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """Get alert correlation by ID."""
    correlation = service.get_alert_correlation(correlation_id)
    if not correlation:
        raise HTTPException(status_code=404, detail=f"Alert correlation {correlation_id} not found")

    return AlertCorrelationResponse(
        correlation_id=correlation.correlation_id,
        customer_id=correlation.customer_id,
        name=correlation.name,
        alert_ids=correlation.alert_ids,
        correlation_type=correlation.correlation_type,
        confidence=correlation.confidence,
        root_cause_alert_id=correlation.root_cause_alert_id,
        created_at=correlation.created_at,
    )


# =============================================================================
# Dashboard Endpoint
# =============================================================================


@router.get("/dashboard/summary", response_model=AlertSummaryResponse)
async def get_alert_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: AlertService = Depends(get_service),
):
    """Get alert dashboard summary."""
    summary = service.get_dashboard_summary()

    return AlertSummaryResponse(
        customer_id=context.customer_id,
        total_alerts=summary.get("total_alerts", 0),
        open_alerts=summary.get("open_alerts", 0),
        acknowledged_alerts=summary.get("acknowledged_alerts", 0),
        investigating_alerts=summary.get("investigating_alerts", 0),
        resolved_alerts=summary.get("resolved_alerts", 0),
        critical_alerts=summary.get("critical_alerts", 0),
        high_alerts=summary.get("high_alerts", 0),
        medium_alerts=summary.get("medium_alerts", 0),
        low_alerts=summary.get("low_alerts", 0),
        alerts_last_24h=summary.get("alerts_last_24h", 0),
        active_correlations=summary.get("active_correlations", 0),
        avg_resolution_time_minutes=summary.get("avg_resolution_time_minutes", 0.0),
    )
