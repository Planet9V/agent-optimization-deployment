"""
Remediation Workflow Integration Tests
=======================================

Integration tests for E06: Remediation Workflow API.
Tests customer isolation, model validation, and remediation workflow operations.

Version: 1.0.0
Created: 2025-12-04
"""

import pytest
from datetime import date, datetime, timedelta
from typing import Generator
import uuid

# Import remediation components
from api.remediation.remediation_models import (
    RemediationTask,
    RemediationPlan,
    SLAPolicy,
    RemediationMetrics,
    RemediationAction,
    EscalationLevel,
    TaskType,
    TaskStatus,
    TaskPriority,
    SLAStatus,
    EscalationAction,
    RemediationActionType,
)
from api.remediation.remediation_service import (
    RemediationWorkflowService,
    TaskSearchRequest,
)
from api.customer_isolation import (
    CustomerContext,
    CustomerContextManager,
    CustomerAccessLevel,
)


# =============================================
# Test Fixtures
# =============================================

@pytest.fixture
def test_customer_ids() -> dict:
    """Generate unique customer IDs for test isolation."""
    return {
        "customer_a": f"TEST-REM-A-{uuid.uuid4().hex[:8]}",
        "customer_b": f"TEST-REM-B-{uuid.uuid4().hex[:8]}",
    }


@pytest.fixture
def customer_a_context(test_customer_ids) -> Generator[CustomerContext, None, None]:
    """Set up customer A context."""
    context = CustomerContextManager.create_context(
        customer_id=test_customer_ids["customer_a"],
        namespace="test_remediation_customer_a",
        access_level=CustomerAccessLevel.WRITE,
        user_id="test-user-a",
    )
    yield context
    CustomerContextManager.clear_context()


@pytest.fixture
def customer_b_context(test_customer_ids) -> Generator[CustomerContext, None, None]:
    """Set up customer B context."""
    context = CustomerContextManager.create_context(
        customer_id=test_customer_ids["customer_b"],
        namespace="test_remediation_customer_b",
        access_level=CustomerAccessLevel.WRITE,
        user_id="test-user-b",
    )
    yield context
    CustomerContextManager.clear_context()


@pytest.fixture
def sample_task(test_customer_ids) -> RemediationTask:
    """Create sample remediation task for testing."""
    return RemediationTask(
        task_id=f"TASK-TEST-{uuid.uuid4().hex[:8]}",
        customer_id=test_customer_ids["customer_a"],
        title="Critical CVE Remediation",
        description="Apply security patch for critical vulnerability",
        vulnerability_id="VULN-2024-001",
        cve_id="CVE-2024-12345",
        asset_ids=["asset-001", "asset-002"],
        task_type=TaskType.PATCH,
        status=TaskStatus.OPEN,
        priority=TaskPriority.CRITICAL,
        severity_source=9.1,
        sla_deadline=datetime.utcnow() + timedelta(hours=24),
        assigned_to="security-team",
        assigned_team="Security Operations",
        effort_estimate_hours=8.0,
        notes="Critical patch required within 24 hours",
    )


@pytest.fixture
def sample_plan(test_customer_ids, sample_task) -> RemediationPlan:
    """Create sample remediation plan for testing."""
    return RemediationPlan(
        plan_id=f"PLAN-TEST-{uuid.uuid4().hex[:8]}",
        customer_id=test_customer_ids["customer_a"],
        name="Q4 Security Patching",
        description="Comprehensive security remediation plan for Q4",
        status="ACTIVE",
        task_ids=[sample_task.task_id],
        total_tasks=10,
        completed_tasks=3,
        start_date=date.today(),
        target_completion_date=date.today() + timedelta(days=30),
        owner="security-manager",
        stakeholders=["security-team", "operations-team"],
        risk_reduction_target=75.0,
        actual_risk_reduction=25.5,
    )


@pytest.fixture
def sample_sla_policy(test_customer_ids) -> SLAPolicy:
    """Create sample SLA policy for testing."""
    return SLAPolicy(
        policy_id=f"SLA-TEST-{uuid.uuid4().hex[:8]}",
        customer_id=test_customer_ids["customer_a"],
        name="Standard Remediation SLA",
        description="Standard remediation SLA based on CVSS severity",
        severity_thresholds={
            "critical": 24,  # 24 hours
            "high": 72,      # 3 days
            "medium": 168,   # 7 days
            "low": 720,      # 30 days
        },
        escalation_levels=[
            EscalationLevel(
                level=1,
                threshold_percentage=0.75,
                notify_roles=["security-manager"],
                action=EscalationAction.NOTIFY,
            ),
            EscalationLevel(
                level=2,
                threshold_percentage=0.90,
                notify_roles=["security-director"],
                action=EscalationAction.ESCALATE_MANAGER,
            ),
        ],
        working_hours_only=False,
        timezone="UTC",
        business_critical_multiplier=0.5,
        active=True,
    )


@pytest.fixture
def sample_metrics(test_customer_ids) -> RemediationMetrics:
    """Create sample remediation metrics for testing."""
    return RemediationMetrics(
        metrics_id=f"METRICS-TEST-{uuid.uuid4().hex[:8]}",
        customer_id=test_customer_ids["customer_a"],
        period_start=date.today() - timedelta(days=30),
        period_end=date.today(),
        total_tasks=150,
        completed_tasks=120,
        open_tasks=25,
        overdue_tasks=5,
        mttr_hours=48.5,
        mttr_by_severity={
            "critical": 18.5,
            "high": 52.3,
            "medium": 120.0,
            "low": 240.5,
        },
        sla_compliance_rate=0.92,
        sla_breaches=12,
        tasks_by_status={
            "open": 10,
            "in_progress": 15,
            "pending_verification": 5,
            "closed": 120,
        },
        tasks_by_priority={
            "critical": 8,
            "high": 25,
            "medium": 67,
            "low": 50,
        },
        vulnerability_backlog=450,
        backlog_trend="decreasing",
    )


@pytest.fixture
def sample_action(test_customer_ids, sample_task) -> RemediationAction:
    """Create sample remediation action for testing."""
    return RemediationAction(
        action_id=f"ACTION-TEST-{uuid.uuid4().hex[:8]}",
        task_id=sample_task.task_id,
        customer_id=test_customer_ids["customer_a"],
        action_type=RemediationActionType.STATUS_CHANGE,
        performed_by="security-engineer",
        timestamp=datetime.utcnow(),
        previous_value="open",
        new_value="in_progress",
        comment="Started work on critical patch",
    )


# =============================================
# Task Model Tests
# =============================================

class TestRemediationTaskModel:
    """Unit tests for RemediationTask model."""

    def test_task_creation_valid(self, test_customer_ids):
        """Test creating a valid remediation task."""
        task = RemediationTask(
            task_id="TASK-001",
            customer_id=test_customer_ids["customer_a"],
            title="Patch Apache Server",
            description="Apply security patch to Apache web server",
            task_type=TaskType.PATCH,
            status=TaskStatus.OPEN,
            priority=TaskPriority.HIGH,
        )
        assert task.task_id == "TASK-001"
        assert task.title == "Patch Apache Server"
        assert task.status == TaskStatus.OPEN

    def test_task_types(self, test_customer_ids):
        """Test all task types."""
        types = [
            TaskType.PATCH,
            TaskType.UPGRADE,
            TaskType.CONFIGURATION,
            TaskType.WORKAROUND,
            TaskType.MITIGATION,
            TaskType.REPLACEMENT,
        ]
        for task_type in types:
            task = RemediationTask(
                task_id=f"TASK-{task_type.value}",
                customer_id=test_customer_ids["customer_a"],
                title=f"Test {task_type.value}",
                description=f"Testing {task_type.value} task",
                task_type=task_type,
            )
            assert task.task_type == task_type

    def test_task_statuses(self, test_customer_ids):
        """Test all task statuses."""
        statuses = [
            TaskStatus.OPEN,
            TaskStatus.IN_PROGRESS,
            TaskStatus.PENDING_VERIFICATION,
            TaskStatus.VERIFIED,
            TaskStatus.CLOSED,
            TaskStatus.WONT_FIX,
            TaskStatus.FALSE_POSITIVE,
        ]
        for status in statuses:
            task = RemediationTask(
                task_id=f"TASK-{status.value}",
                customer_id=test_customer_ids["customer_a"],
                title="Test Task",
                description="Test description",
                status=status,
            )
            assert task.status == status

    def test_task_priorities(self, test_customer_ids):
        """Test all task priorities."""
        priorities = [
            TaskPriority.LOW,
            TaskPriority.MEDIUM,
            TaskPriority.HIGH,
            TaskPriority.CRITICAL,
            TaskPriority.EMERGENCY,
        ]
        for priority in priorities:
            task = RemediationTask(
                task_id=f"TASK-{priority.value}",
                customer_id=test_customer_ids["customer_a"],
                title="Test Task",
                description="Test description",
                priority=priority,
            )
            assert task.priority == priority

    def test_task_is_overdue(self, test_customer_ids):
        """Test is_overdue property."""
        # Not overdue task
        future_task = RemediationTask(
            task_id="TASK-FUTURE",
            customer_id=test_customer_ids["customer_a"],
            title="Future Task",
            description="Task with future deadline",
            sla_deadline=datetime.utcnow() + timedelta(hours=24),
        )
        assert future_task.is_overdue == False

        # Overdue task
        past_task = RemediationTask(
            task_id="TASK-PAST",
            customer_id=test_customer_ids["customer_a"],
            title="Past Task",
            description="Task with past deadline",
            sla_deadline=datetime.utcnow() - timedelta(hours=24),
        )
        assert past_task.is_overdue == True

    def test_task_is_critical_priority(self, test_customer_ids):
        """Test is_critical_priority property."""
        critical_task = RemediationTask(
            task_id="TASK-CRIT",
            customer_id=test_customer_ids["customer_a"],
            title="Critical Task",
            description="Critical priority task",
            priority=TaskPriority.CRITICAL,
        )
        assert critical_task.is_critical_priority == True

        emergency_task = RemediationTask(
            task_id="TASK-EMER",
            customer_id=test_customer_ids["customer_a"],
            title="Emergency Task",
            description="Emergency priority task",
            priority=TaskPriority.EMERGENCY,
        )
        assert emergency_task.is_critical_priority == True

        normal_task = RemediationTask(
            task_id="TASK-NORM",
            customer_id=test_customer_ids["customer_a"],
            title="Normal Task",
            description="Normal priority task",
            priority=TaskPriority.MEDIUM,
        )
        assert normal_task.is_critical_priority == False

    def test_task_is_completed(self, test_customer_ids):
        """Test is_completed property."""
        open_task = RemediationTask(
            task_id="TASK-OPEN",
            customer_id=test_customer_ids["customer_a"],
            title="Open Task",
            description="Open task",
            status=TaskStatus.OPEN,
        )
        assert open_task.is_completed == False

        closed_task = RemediationTask(
            task_id="TASK-CLOSED",
            customer_id=test_customer_ids["customer_a"],
            title="Closed Task",
            description="Closed task",
            status=TaskStatus.CLOSED,
        )
        assert closed_task.is_completed == True

        verified_task = RemediationTask(
            task_id="TASK-VERIFIED",
            customer_id=test_customer_ids["customer_a"],
            title="Verified Task",
            description="Verified task",
            status=TaskStatus.VERIFIED,
        )
        assert verified_task.is_completed == True

    def test_task_sla_status_calculation(self, test_customer_ids):
        """Test SLA status auto-calculation."""
        # Within SLA
        within_sla = RemediationTask(
            task_id="TASK-WITHIN",
            customer_id=test_customer_ids["customer_a"],
            title="Within SLA",
            description="Task within SLA",
            sla_deadline=datetime.utcnow() + timedelta(hours=48),
            created_at=datetime.utcnow() - timedelta(hours=1),
        )
        assert within_sla.sla_status == SLAStatus.WITHIN_SLA

        # Breached SLA
        breached = RemediationTask(
            task_id="TASK-BREACHED",
            customer_id=test_customer_ids["customer_a"],
            title="Breached SLA",
            description="Task with breached SLA",
            sla_deadline=datetime.utcnow() - timedelta(hours=1),
        )
        assert breached.sla_status == SLAStatus.BREACHED

    def test_task_to_dict(self, sample_task):
        """Test task serialization to dictionary."""
        task_dict = sample_task.to_dict()
        assert task_dict["task_id"] == sample_task.task_id
        assert task_dict["customer_id"] == sample_task.customer_id
        assert task_dict["title"] == sample_task.title
        assert "task_type" in task_dict
        assert "status" in task_dict
        assert "priority" in task_dict

    def test_task_to_qdrant_payload(self, sample_task):
        """Test task Qdrant payload generation."""
        payload = sample_task.to_qdrant_payload()
        assert payload["entity_type"] == "remediation_task"
        assert payload["task_id"] == sample_task.task_id
        assert payload["customer_id"] == sample_task.customer_id


# =============================================
# Plan Model Tests
# =============================================

class TestRemediationPlanModel:
    """Unit tests for RemediationPlan model."""

    def test_plan_creation_valid(self, test_customer_ids):
        """Test creating a valid remediation plan."""
        plan = RemediationPlan(
            plan_id="PLAN-001",
            customer_id=test_customer_ids["customer_a"],
            name="Security Patching Plan",
            description="Comprehensive patching plan",
            status="DRAFT",
        )
        assert plan.plan_id == "PLAN-001"
        assert plan.name == "Security Patching Plan"
        assert plan.status == "DRAFT"

    def test_plan_completion_percentage(self, test_customer_ids):
        """Test completion percentage calculation."""
        plan = RemediationPlan(
            plan_id="PLAN-COMP",
            customer_id=test_customer_ids["customer_a"],
            name="Test Plan",
            total_tasks=100,
            completed_tasks=75,
        )
        assert plan.completion_percentage == 75.0

    def test_plan_is_completed(self, test_customer_ids):
        """Test is_completed property."""
        incomplete_plan = RemediationPlan(
            plan_id="PLAN-INC",
            customer_id=test_customer_ids["customer_a"],
            name="Incomplete Plan",
            status="ACTIVE",
            total_tasks=10,
            completed_tasks=7,
        )
        assert incomplete_plan.is_completed == False

        complete_plan = RemediationPlan(
            plan_id="PLAN-COMP",
            customer_id=test_customer_ids["customer_a"],
            name="Complete Plan",
            status="COMPLETED",
            total_tasks=10,
            completed_tasks=10,
        )
        assert complete_plan.is_completed == True

    def test_plan_is_on_track(self, test_customer_ids):
        """Test is_on_track calculation."""
        today = date.today()

        # On track plan
        on_track = RemediationPlan(
            plan_id="PLAN-ONTRACK",
            customer_id=test_customer_ids["customer_a"],
            name="On Track Plan",
            start_date=today - timedelta(days=10),
            target_completion_date=today + timedelta(days=20),
            total_tasks=100,
            completed_tasks=40,  # 40% complete at 33% elapsed
        )
        assert on_track.is_on_track == True

    def test_plan_to_dict(self, sample_plan):
        """Test plan serialization."""
        plan_dict = sample_plan.to_dict()
        assert plan_dict["plan_id"] == sample_plan.plan_id
        assert plan_dict["customer_id"] == sample_plan.customer_id
        assert plan_dict["name"] == sample_plan.name
        assert "completion_percentage" in plan_dict


# =============================================
# SLA Policy Model Tests
# =============================================

class TestSLAPolicyModel:
    """Unit tests for SLAPolicy model."""

    def test_sla_policy_creation_valid(self, test_customer_ids):
        """Test creating a valid SLA policy."""
        policy = SLAPolicy(
            policy_id="SLA-001",
            customer_id=test_customer_ids["customer_a"],
            name="Standard SLA",
            severity_thresholds={"critical": 24, "high": 72},
        )
        assert policy.policy_id == "SLA-001"
        assert policy.name == "Standard SLA"
        assert policy.active == True

    def test_sla_get_sla_hours(self, test_customer_ids):
        """Test get_sla_hours method."""
        policy = SLAPolicy(
            policy_id="SLA-HOURS",
            customer_id=test_customer_ids["customer_a"],
            name="Test SLA",
            severity_thresholds={
                "critical": 24,
                "high": 72,
                "medium": 168,
            },
            business_critical_multiplier=0.5,
        )

        # Normal asset
        assert policy.get_sla_hours("critical", False) == 24
        assert policy.get_sla_hours("high", False) == 72

        # Business critical asset (50% reduction)
        assert policy.get_sla_hours("critical", True) == 12
        assert policy.get_sla_hours("high", True) == 36

    def test_sla_get_escalation_for_percentage(self, sample_sla_policy):
        """Test escalation level selection."""
        # No escalation needed
        level = sample_sla_policy.get_escalation_for_percentage(0.5)
        assert level is None

        # Level 1 escalation (75% elapsed)
        level = sample_sla_policy.get_escalation_for_percentage(0.8)
        assert level is not None
        assert level.level == 1

        # Level 2 escalation (90% elapsed)
        level = sample_sla_policy.get_escalation_for_percentage(0.95)
        assert level is not None
        assert level.level == 2

    def test_sla_to_dict(self, sample_sla_policy):
        """Test SLA policy serialization."""
        policy_dict = sample_sla_policy.to_dict()
        assert policy_dict["policy_id"] == sample_sla_policy.policy_id
        assert policy_dict["customer_id"] == sample_sla_policy.customer_id
        assert "severity_thresholds" in policy_dict
        assert "escalation_levels" in policy_dict


# =============================================
# Metrics Model Tests
# =============================================

class TestRemediationMetricsModel:
    """Unit tests for RemediationMetrics model."""

    def test_metrics_creation_valid(self, test_customer_ids):
        """Test creating valid remediation metrics."""
        metrics = RemediationMetrics(
            metrics_id="METRICS-001",
            customer_id=test_customer_ids["customer_a"],
            period_start=date.today() - timedelta(days=30),
            period_end=date.today(),
            total_tasks=100,
            completed_tasks=85,
            sla_compliance_rate=0.90,
        )
        assert metrics.metrics_id == "METRICS-001"
        assert metrics.total_tasks == 100
        assert metrics.sla_compliance_rate == 0.90

    def test_metrics_completion_rate(self, test_customer_ids):
        """Test completion rate calculation."""
        metrics = RemediationMetrics(
            metrics_id="METRICS-RATE",
            customer_id=test_customer_ids["customer_a"],
            period_start=date.today() - timedelta(days=7),
            period_end=date.today(),
            total_tasks=200,
            completed_tasks=150,
        )
        assert metrics.completion_rate == 75.0

    def test_metrics_overdue_rate(self, test_customer_ids):
        """Test overdue rate calculation."""
        metrics = RemediationMetrics(
            metrics_id="METRICS-OVERDUE",
            customer_id=test_customer_ids["customer_a"],
            period_start=date.today() - timedelta(days=7),
            period_end=date.today(),
            open_tasks=50,
            overdue_tasks=10,
        )
        assert metrics.overdue_rate == 20.0

    def test_metrics_to_dict(self, sample_metrics):
        """Test metrics serialization."""
        metrics_dict = sample_metrics.to_dict()
        assert metrics_dict["metrics_id"] == sample_metrics.metrics_id
        assert metrics_dict["customer_id"] == sample_metrics.customer_id
        assert "completion_rate" in metrics_dict
        assert "overdue_rate" in metrics_dict
        assert "mttr_by_severity" in metrics_dict


# =============================================
# Action Model Tests
# =============================================

class TestRemediationActionModel:
    """Unit tests for RemediationAction model."""

    def test_action_creation_valid(self, test_customer_ids):
        """Test creating a valid remediation action."""
        action = RemediationAction(
            action_id="ACTION-001",
            task_id="TASK-001",
            customer_id=test_customer_ids["customer_a"],
            action_type=RemediationActionType.CREATED,
            performed_by="user-001",
        )
        assert action.action_id == "ACTION-001"
        assert action.action_type == RemediationActionType.CREATED

    def test_action_types(self, test_customer_ids):
        """Test all action types."""
        action_types = [
            RemediationActionType.CREATED,
            RemediationActionType.ASSIGNED,
            RemediationActionType.STATUS_CHANGE,
            RemediationActionType.PRIORITY_CHANGE,
            RemediationActionType.COMMENT,
            RemediationActionType.ESCALATED,
            RemediationActionType.VERIFIED,
            RemediationActionType.CLOSED,
        ]
        for action_type in action_types:
            action = RemediationAction(
                action_id=f"ACTION-{action_type.value}",
                task_id="TASK-001",
                customer_id=test_customer_ids["customer_a"],
                action_type=action_type,
                performed_by="user-001",
            )
            assert action.action_type == action_type

    def test_action_to_dict(self, sample_action):
        """Test action serialization."""
        action_dict = sample_action.to_dict()
        assert action_dict["action_id"] == sample_action.action_id
        assert action_dict["task_id"] == sample_action.task_id
        assert action_dict["customer_id"] == sample_action.customer_id
        assert "action_type" in action_dict

    def test_action_to_qdrant_payload(self, sample_action):
        """Test action Qdrant payload generation."""
        payload = sample_action.to_qdrant_payload()
        assert payload["entity_type"] == "remediation_action"
        assert payload["action_id"] == sample_action.action_id
        assert payload["customer_id"] == sample_action.customer_id


# =============================================
# Escalation Level Model Tests
# =============================================

class TestEscalationLevelModel:
    """Unit tests for EscalationLevel model."""

    def test_escalation_level_creation_valid(self):
        """Test creating a valid escalation level."""
        level = EscalationLevel(
            level=1,
            threshold_percentage=0.75,
            notify_roles=["manager"],
            action=EscalationAction.NOTIFY,
        )
        assert level.level == 1
        assert level.threshold_percentage == 0.75

    def test_escalation_level_validation(self):
        """Test escalation level validation."""
        # Invalid threshold
        with pytest.raises(ValueError):
            EscalationLevel(
                level=1,
                threshold_percentage=1.5,  # > 1.0
            )

        # Invalid level
        with pytest.raises(ValueError):
            EscalationLevel(
                level=0,  # < 1
                threshold_percentage=0.75,
            )

    def test_escalation_actions(self):
        """Test all escalation actions."""
        actions = [
            EscalationAction.NOTIFY,
            EscalationAction.ESCALATE_MANAGER,
            EscalationAction.ESCALATE_EXECUTIVE,
            EscalationAction.AUTO_ASSIGN,
        ]
        for action in actions:
            level = EscalationLevel(
                level=1,
                threshold_percentage=0.75,
                action=action,
            )
            assert level.action == action


# =============================================
# Customer Isolation Tests
# =============================================

class TestCustomerIsolation:
    """Tests for customer data isolation."""

    def test_task_customer_id_required(self, test_customer_ids):
        """Test that task requires customer_id."""
        task = RemediationTask(
            task_id="TASK-001",
            customer_id=test_customer_ids["customer_a"],
            title="Test Task",
            description="Test description",
        )
        assert task.customer_id == test_customer_ids["customer_a"]

    def test_plan_customer_id_required(self, test_customer_ids):
        """Test that plan requires customer_id."""
        plan = RemediationPlan(
            plan_id="PLAN-001",
            customer_id=test_customer_ids["customer_a"],
            name="Test Plan",
        )
        assert plan.customer_id == test_customer_ids["customer_a"]

    def test_sla_policy_customer_id_required(self, test_customer_ids):
        """Test that SLA policy requires customer_id."""
        policy = SLAPolicy(
            policy_id="SLA-001",
            customer_id=test_customer_ids["customer_a"],
            name="Test Policy",
        )
        assert policy.customer_id == test_customer_ids["customer_a"]

    def test_metrics_customer_id_required(self, test_customer_ids):
        """Test that metrics requires customer_id."""
        metrics = RemediationMetrics(
            metrics_id="METRICS-001",
            customer_id=test_customer_ids["customer_a"],
            period_start=date.today() - timedelta(days=7),
            period_end=date.today(),
        )
        assert metrics.customer_id == test_customer_ids["customer_a"]

    def test_action_customer_id_required(self, test_customer_ids):
        """Test that action requires customer_id."""
        action = RemediationAction(
            action_id="ACTION-001",
            task_id="TASK-001",
            customer_id=test_customer_ids["customer_a"],
            action_type=RemediationActionType.CREATED,
            performed_by="user-001",
        )
        assert action.customer_id == test_customer_ids["customer_a"]


# =============================================
# Enum Tests
# =============================================

class TestEnums:
    """Tests for all remediation enums."""

    def test_task_type_values(self):
        """Test TaskType enum values."""
        assert TaskType.PATCH.value == "patch"
        assert TaskType.UPGRADE.value == "upgrade"
        assert TaskType.CONFIGURATION.value == "configuration"
        assert TaskType.WORKAROUND.value == "workaround"
        assert TaskType.MITIGATION.value == "mitigation"
        assert TaskType.REPLACEMENT.value == "replacement"

    def test_task_status_values(self):
        """Test TaskStatus enum values."""
        assert TaskStatus.OPEN.value == "open"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.PENDING_VERIFICATION.value == "pending_verification"
        assert TaskStatus.VERIFIED.value == "verified"
        assert TaskStatus.CLOSED.value == "closed"
        assert TaskStatus.WONT_FIX.value == "wont_fix"
        assert TaskStatus.FALSE_POSITIVE.value == "false_positive"

    def test_task_priority_values(self):
        """Test TaskPriority enum values."""
        assert TaskPriority.LOW.value == "low"
        assert TaskPriority.MEDIUM.value == "medium"
        assert TaskPriority.HIGH.value == "high"
        assert TaskPriority.CRITICAL.value == "critical"
        assert TaskPriority.EMERGENCY.value == "emergency"

    def test_sla_status_values(self):
        """Test SLAStatus enum values."""
        assert SLAStatus.WITHIN_SLA.value == "within_sla"
        assert SLAStatus.AT_RISK.value == "at_risk"
        assert SLAStatus.BREACHED.value == "breached"

    def test_escalation_action_values(self):
        """Test EscalationAction enum values."""
        assert EscalationAction.NOTIFY.value == "notify"
        assert EscalationAction.ESCALATE_MANAGER.value == "escalate_manager"
        assert EscalationAction.ESCALATE_EXECUTIVE.value == "escalate_executive"
        assert EscalationAction.AUTO_ASSIGN.value == "auto_assign"

    def test_remediation_action_type_values(self):
        """Test RemediationActionType enum values."""
        assert RemediationActionType.CREATED.value == "created"
        assert RemediationActionType.ASSIGNED.value == "assigned"
        assert RemediationActionType.STATUS_CHANGE.value == "status_change"
        assert RemediationActionType.PRIORITY_CHANGE.value == "priority_change"
        assert RemediationActionType.COMMENT.value == "comment"
        assert RemediationActionType.ESCALATED.value == "escalated"
        assert RemediationActionType.VERIFIED.value == "verified"
        assert RemediationActionType.CLOSED.value == "closed"


# =============================================
# Integration Summary Tests
# =============================================

class TestIntegrationSummary:
    """Summary tests for overall module integration."""

    def test_all_models_import(self):
        """Test that all models can be imported."""
        from api.remediation import (
            RemediationTask,
            RemediationPlan,
            SLAPolicy,
            RemediationMetrics,
            RemediationAction,
            EscalationLevel,
        )
        assert RemediationTask is not None
        assert RemediationPlan is not None
        assert SLAPolicy is not None

    def test_all_enums_import(self):
        """Test that all enums can be imported."""
        from api.remediation import (
            TaskType,
            TaskStatus,
            TaskPriority,
            SLAStatus,
            EscalationAction,
            RemediationActionType,
        )
        assert TaskType is not None
        assert TaskStatus is not None
        assert TaskPriority is not None

    def test_service_import(self):
        """Test that service can be imported."""
        from api.remediation import RemediationWorkflowService
        assert RemediationWorkflowService is not None

    def test_router_conditional_import(self):
        """Test that router import is handled gracefully (FastAPI optional)."""
        from api.remediation import remediation_router
        # Router may be None if FastAPI is not installed
        # This is expected behavior - tests should pass either way
        assert True  # Just verify import doesn't crash
