"""
Remediation Workflow Models
============================

Data models for E06: Remediation Workflow API.
Includes RemediationTask, RemediationPlan, SLAPolicy, and RemediationMetrics entities.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional, List, Dict, Any


# =============================================================================
# Enums for Remediation Workflow
# =============================================================================


class TaskType(Enum):
    """Types of remediation tasks."""
    PATCH = "patch"                 # Apply security patch
    UPGRADE = "upgrade"             # Version upgrade
    CONFIGURATION = "configuration" # Configuration change
    WORKAROUND = "workaround"       # Temporary workaround
    MITIGATION = "mitigation"       # Mitigating controls
    REPLACEMENT = "replacement"     # Equipment replacement


class TaskStatus(Enum):
    """Remediation task lifecycle status."""
    OPEN = "open"                       # Newly created, unassigned
    IN_PROGRESS = "in_progress"         # Currently being worked on
    PENDING_VERIFICATION = "pending_verification"  # Awaiting verification
    VERIFIED = "verified"               # Verified as resolved
    CLOSED = "closed"                   # Closed and complete
    WONT_FIX = "wont_fix"              # Accepted risk, won't fix
    FALSE_POSITIVE = "false_positive"   # Not a real vulnerability


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = "low"             # Non-critical, schedule normally
    MEDIUM = "medium"       # Standard priority
    HIGH = "high"           # High priority, expedite
    CRITICAL = "critical"   # Critical, immediate action
    EMERGENCY = "emergency" # Emergency response required


class SLAStatus(Enum):
    """SLA compliance status."""
    WITHIN_SLA = "within_sla"   # On track to meet SLA
    AT_RISK = "at_risk"         # In danger of breaching SLA
    BREACHED = "breached"       # SLA deadline missed


class EscalationAction(Enum):
    """Actions to take during escalation."""
    NOTIFY = "notify"                       # Send notification only
    ESCALATE_MANAGER = "escalate_manager"   # Escalate to manager
    ESCALATE_EXECUTIVE = "escalate_executive"  # Escalate to executive
    AUTO_ASSIGN = "auto_assign"             # Automatically assign resource


class RemediationActionType(Enum):
    """Types of remediation actions for audit trail."""
    CREATED = "created"                 # Task created
    ASSIGNED = "assigned"               # Task assigned to user/team
    STATUS_CHANGE = "status_change"     # Status updated
    PRIORITY_CHANGE = "priority_change" # Priority changed
    COMMENT = "comment"                 # Comment added
    ESCALATED = "escalated"             # Task escalated
    VERIFIED = "verified"               # Verification completed
    CLOSED = "closed"                   # Task closed


# =============================================================================
# Core Data Models
# =============================================================================


@dataclass
class RemediationTask:
    """
    Remediation Task entity for vulnerability fix tracking.

    Represents a specific remediation task for fixing one or more vulnerabilities
    with SLA tracking, assignment, and verification workflow.
    """
    task_id: str
    customer_id: str  # For multi-tenant isolation
    title: str
    description: str

    # Vulnerability linkage
    vulnerability_id: Optional[str] = None
    cve_id: Optional[str] = None  # Optional CVE reference
    asset_ids: List[str] = field(default_factory=list)  # Affected assets

    # Task classification
    task_type: TaskType = TaskType.PATCH
    status: TaskStatus = TaskStatus.OPEN
    priority: TaskPriority = TaskPriority.MEDIUM

    # Severity from original vulnerability
    severity_source: float = 0.0  # CVSS score from vulnerability

    # Timeline
    due_date: Optional[date] = None
    start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    verification_date: Optional[datetime] = None

    # SLA tracking
    sla_deadline: Optional[datetime] = None
    sla_status: SLAStatus = SLAStatus.WITHIN_SLA

    # Assignment
    assigned_to: Optional[str] = None
    assigned_team: Optional[str] = None
    created_by: Optional[str] = None

    # Effort tracking
    effort_estimate_hours: float = 0.0
    actual_effort_hours: float = 0.0

    # Notes
    notes: Optional[str] = None
    verification_notes: Optional[str] = None

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate remediation task data."""
        if not self.task_id or not self.task_id.strip():
            raise ValueError("task_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.title or not self.title.strip():
            raise ValueError("title is required")
        if not self.description or not self.description.strip():
            raise ValueError("description is required")

        # Normalize values
        self.task_id = self.task_id.strip()
        self.customer_id = self.customer_id.strip()
        self.title = self.title.strip()
        self.description = self.description.strip()

        # Update SLA status if we have a deadline
        if self.sla_deadline:
            self.sla_status = self._calculate_sla_status()

    def _calculate_sla_status(self) -> SLAStatus:
        """Calculate SLA status based on deadline and current time."""
        if not self.sla_deadline:
            return SLAStatus.WITHIN_SLA

        now = datetime.utcnow()
        time_remaining = (self.sla_deadline - now).total_seconds()
        total_time = (self.sla_deadline - self.created_at).total_seconds()

        # If past deadline
        if time_remaining < 0:
            return SLAStatus.BREACHED

        # Calculate percentage of time remaining
        if total_time > 0:
            percent_remaining = (time_remaining / total_time) * 100

            # At risk if less than 20% time remaining
            if percent_remaining < 20:
                return SLAStatus.AT_RISK

        return SLAStatus.WITHIN_SLA

    @property
    def is_overdue(self) -> bool:
        """Check if task is past SLA deadline."""
        return self.sla_status == SLAStatus.BREACHED

    @property
    def is_critical_priority(self) -> bool:
        """Check if task is critical or emergency priority."""
        return self.priority in {TaskPriority.CRITICAL, TaskPriority.EMERGENCY}

    @property
    def is_completed(self) -> bool:
        """Check if task is in a completed state."""
        return self.status in {TaskStatus.VERIFIED, TaskStatus.CLOSED,
                               TaskStatus.WONT_FIX, TaskStatus.FALSE_POSITIVE}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "task_id": self.task_id,
            "customer_id": self.customer_id,
            "title": self.title,
            "description": self.description,
            "vulnerability_id": self.vulnerability_id,
            "cve_id": self.cve_id,
            "asset_ids": self.asset_ids,
            "task_type": self.task_type.value,
            "status": self.status.value,
            "priority": self.priority.value,
            "severity_source": self.severity_source,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "completion_date": self.completion_date.isoformat() if self.completion_date else None,
            "verification_date": self.verification_date.isoformat() if self.verification_date else None,
            "sla_deadline": self.sla_deadline.isoformat() if self.sla_deadline else None,
            "sla_status": self.sla_status.value,
            "assigned_to": self.assigned_to,
            "assigned_team": self.assigned_team,
            "created_by": self.created_by,
            "effort_estimate_hours": self.effort_estimate_hours,
            "actual_effort_hours": self.actual_effort_hours,
            "notes": self.notes,
            "verification_notes": self.verification_notes,
            "is_overdue": self.is_overdue,
            "is_critical_priority": self.is_critical_priority,
            "is_completed": self.is_completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "task_id": self.task_id,
            "customer_id": self.customer_id,
            "entity_type": "remediation_task",
            "title": self.title,
            "vulnerability_id": self.vulnerability_id,
            "cve_id": self.cve_id,
            "asset_ids": self.asset_ids,
            "task_type": self.task_type.value,
            "status": self.status.value,
            "priority": self.priority.value,
            "severity_source": self.severity_source,
            "sla_status": self.sla_status.value,
            "sla_deadline": self.sla_deadline.isoformat() if self.sla_deadline else None,
            "assigned_to": self.assigned_to,
            "assigned_team": self.assigned_team,
            "is_overdue": self.is_overdue,
            "is_critical_priority": self.is_critical_priority,
            "is_completed": self.is_completed,
        }


@dataclass
class RemediationPlan:
    """
    Remediation Plan entity for multi-task plan tracking.

    Groups multiple remediation tasks into a coordinated plan with
    overall status tracking and completion metrics.
    """
    plan_id: str
    customer_id: str  # For multi-tenant isolation
    name: str
    description: Optional[str] = None

    # Plan status
    status: str = "DRAFT"  # DRAFT, ACTIVE, COMPLETED, CANCELLED

    # Task tracking
    task_ids: List[str] = field(default_factory=list)
    total_tasks: int = 0
    completed_tasks: int = 0

    # Timeline
    start_date: Optional[date] = None
    target_completion_date: Optional[date] = None
    actual_completion_date: Optional[date] = None

    # Ownership
    owner: Optional[str] = None
    stakeholders: List[str] = field(default_factory=list)

    # Risk reduction metrics
    risk_reduction_target: float = 0.0  # Target risk score reduction
    actual_risk_reduction: float = 0.0  # Actual achieved reduction

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate remediation plan data."""
        if not self.plan_id or not self.plan_id.strip():
            raise ValueError("plan_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")

        # Normalize values
        self.plan_id = self.plan_id.strip()
        self.customer_id = self.customer_id.strip()
        self.name = self.name.strip()

        # Update totals from task_ids if not set
        if self.total_tasks == 0 and self.task_ids:
            self.total_tasks = len(self.task_ids)

    @property
    def completion_percentage(self) -> float:
        """Calculate plan completion percentage."""
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.total_tasks) * 100

    @property
    def is_completed(self) -> bool:
        """Check if plan is fully completed."""
        return self.status == "COMPLETED" and self.completed_tasks == self.total_tasks

    @property
    def is_on_track(self) -> bool:
        """Check if plan is on track to meet target date."""
        if not self.target_completion_date or not self.start_date:
            return True  # Can't determine if no dates

        today = date.today()
        if today > self.target_completion_date:
            return False  # Past target

        total_days = (self.target_completion_date - self.start_date).days
        elapsed_days = (today - self.start_date).days

        if total_days <= 0:
            return True

        expected_completion = (elapsed_days / total_days) * 100
        return self.completion_percentage >= expected_completion

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "plan_id": self.plan_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "task_ids": self.task_ids,
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "completion_percentage": self.completion_percentage,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "target_completion_date": self.target_completion_date.isoformat() if self.target_completion_date else None,
            "actual_completion_date": self.actual_completion_date.isoformat() if self.actual_completion_date else None,
            "owner": self.owner,
            "stakeholders": self.stakeholders,
            "risk_reduction_target": self.risk_reduction_target,
            "actual_risk_reduction": self.actual_risk_reduction,
            "is_completed": self.is_completed,
            "is_on_track": self.is_on_track,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class EscalationLevel:
    """
    Escalation Level for SLA policy.

    Defines a specific escalation level with threshold and actions.
    """
    level: int  # 1, 2, 3, etc.
    threshold_percentage: float  # % of SLA elapsed (e.g., 0.75 = 75%)
    notify_roles: List[str] = field(default_factory=list)
    notify_emails: List[str] = field(default_factory=list)
    action: EscalationAction = EscalationAction.NOTIFY

    def __post_init__(self):
        """Validate escalation level data."""
        if not 0.0 <= self.threshold_percentage <= 1.0:
            raise ValueError("threshold_percentage must be between 0.0 and 1.0")
        if self.level < 1:
            raise ValueError("level must be >= 1")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "level": self.level,
            "threshold_percentage": self.threshold_percentage,
            "notify_roles": self.notify_roles,
            "notify_emails": self.notify_emails,
            "action": self.action.value,
        }


@dataclass
class SLAPolicy:
    """
    SLA Policy entity for remediation timeline configuration.

    Defines Service Level Agreement policies for remediation tasks
    based on severity levels and business criticality.
    """
    policy_id: str
    customer_id: str  # For multi-tenant isolation
    name: str
    description: Optional[str] = None

    # Severity thresholds (severity -> hours to remediate)
    severity_thresholds: Dict[str, int] = field(default_factory=dict)
    # Example: {"critical": 24, "high": 72, "medium": 168, "low": 720}

    # Escalation levels
    escalation_levels: List[EscalationLevel] = field(default_factory=list)

    # Working hours configuration
    working_hours_only: bool = False
    timezone: str = "UTC"

    # Business critical multiplier (reduce SLA time by this factor)
    business_critical_multiplier: float = 0.5  # 50% reduction for critical assets

    # Status
    active: bool = True

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate SLA policy data."""
        if not self.policy_id or not self.policy_id.strip():
            raise ValueError("policy_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")

        # Normalize values
        self.policy_id = self.policy_id.strip()
        self.customer_id = self.customer_id.strip()
        self.name = self.name.strip()

    def get_sla_hours(self, severity: str, is_business_critical: bool = False) -> Optional[int]:
        """Get SLA hours for a given severity level."""
        base_hours = self.severity_thresholds.get(severity.lower())
        if base_hours is None:
            return None

        if is_business_critical:
            return int(base_hours * self.business_critical_multiplier)

        return base_hours

    def get_escalation_for_percentage(self, elapsed_percentage: float) -> Optional[EscalationLevel]:
        """Get appropriate escalation level for elapsed time percentage."""
        applicable_levels = [
            level for level in self.escalation_levels
            if elapsed_percentage >= level.threshold_percentage
        ]

        if not applicable_levels:
            return None

        # Return highest level that applies
        return max(applicable_levels, key=lambda x: x.level)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "policy_id": self.policy_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "description": self.description,
            "severity_thresholds": self.severity_thresholds,
            "escalation_levels": [level.to_dict() for level in self.escalation_levels],
            "working_hours_only": self.working_hours_only,
            "timezone": self.timezone,
            "business_critical_multiplier": self.business_critical_multiplier,
            "active": self.active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class RemediationMetrics:
    """
    Remediation Metrics entity for performance tracking.

    Aggregates key performance indicators for remediation activities
    over a specific time period.
    """
    metrics_id: str
    customer_id: str  # For multi-tenant isolation

    # Time period
    period_start: date
    period_end: date

    # Task counts
    total_tasks: int = 0
    completed_tasks: int = 0
    open_tasks: int = 0
    overdue_tasks: int = 0

    # Mean Time To Remediate
    mttr_hours: float = 0.0  # Overall MTTR
    mttr_by_severity: Dict[str, float] = field(default_factory=dict)
    # Example: {"critical": 18.5, "high": 65.2, "medium": 148.0}

    # SLA compliance
    sla_compliance_rate: float = 0.0  # 0.0-1.0 (percentage as decimal)
    sla_breaches: int = 0

    # Task distribution
    tasks_by_status: Dict[str, int] = field(default_factory=dict)
    tasks_by_priority: Dict[str, int] = field(default_factory=dict)

    # Backlog metrics
    vulnerability_backlog: int = 0  # Total unresolved vulnerabilities
    backlog_trend: str = "stable"  # "increasing", "decreasing", "stable"

    # Timestamps
    calculated_at: datetime = field(default_factory=datetime.utcnow)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate remediation metrics data."""
        if not self.metrics_id or not self.metrics_id.strip():
            raise ValueError("metrics_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not 0.0 <= self.sla_compliance_rate <= 1.0:
            raise ValueError("sla_compliance_rate must be between 0.0 and 1.0")

        # Normalize values
        self.metrics_id = self.metrics_id.strip()
        self.customer_id = self.customer_id.strip()

    @property
    def completion_rate(self) -> float:
        """Calculate task completion rate."""
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.total_tasks) * 100

    @property
    def overdue_rate(self) -> float:
        """Calculate percentage of tasks that are overdue."""
        if self.open_tasks == 0:
            return 0.0
        return (self.overdue_tasks / self.open_tasks) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "metrics_id": self.metrics_id,
            "customer_id": self.customer_id,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "open_tasks": self.open_tasks,
            "overdue_tasks": self.overdue_tasks,
            "completion_rate": self.completion_rate,
            "overdue_rate": self.overdue_rate,
            "mttr_hours": self.mttr_hours,
            "mttr_by_severity": self.mttr_by_severity,
            "sla_compliance_rate": self.sla_compliance_rate,
            "sla_breaches": self.sla_breaches,
            "tasks_by_status": self.tasks_by_status,
            "tasks_by_priority": self.tasks_by_priority,
            "vulnerability_backlog": self.vulnerability_backlog,
            "backlog_trend": self.backlog_trend,
            "calculated_at": self.calculated_at.isoformat(),
        }


@dataclass
class RemediationAction:
    """
    Remediation Action entity for audit trail.

    Records all actions taken on remediation tasks for compliance
    and audit purposes.
    """
    action_id: str
    task_id: str
    customer_id: str  # For multi-tenant isolation

    # Action details
    action_type: RemediationActionType
    performed_by: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    # Change tracking
    previous_value: Optional[str] = None
    new_value: Optional[str] = None
    comment: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate remediation action data."""
        if not self.action_id or not self.action_id.strip():
            raise ValueError("action_id is required")
        if not self.task_id or not self.task_id.strip():
            raise ValueError("task_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.performed_by or not self.performed_by.strip():
            raise ValueError("performed_by is required")

        # Normalize values
        self.action_id = self.action_id.strip()
        self.task_id = self.task_id.strip()
        self.customer_id = self.customer_id.strip()
        self.performed_by = self.performed_by.strip()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "action_id": self.action_id,
            "task_id": self.task_id,
            "customer_id": self.customer_id,
            "action_type": self.action_type.value,
            "performed_by": self.performed_by,
            "timestamp": self.timestamp.isoformat(),
            "previous_value": self.previous_value,
            "new_value": self.new_value,
            "comment": self.comment,
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "action_id": self.action_id,
            "task_id": self.task_id,
            "customer_id": self.customer_id,
            "entity_type": "remediation_action",
            "action_type": self.action_type.value,
            "performed_by": self.performed_by,
            "timestamp": self.timestamp.isoformat(),
            "previous_value": self.previous_value,
            "new_value": self.new_value,
        }
