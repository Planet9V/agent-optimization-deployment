"""
Alert Management Models
=======================

Data models for E09: Alert Management & Response API.
Includes Alert, AlertRule, NotificationRule, EscalationPolicy, and AlertCorrelation entities.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Dict, Any


# =============================================================================
# Enums for Alert Management
# =============================================================================


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(Enum):
    """Alert lifecycle status."""
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"
    FALSE_POSITIVE = "false_positive"


class AlertCategory(Enum):
    """Alert category classifications."""
    SECURITY = "security"
    COMPLIANCE = "compliance"
    OPERATIONAL = "operational"
    PERFORMANCE = "performance"
    AVAILABILITY = "availability"


class NotificationChannel(Enum):
    """Available notification delivery channels."""
    EMAIL = "email"
    SMS = "sms"
    SLACK = "slack"
    TEAMS = "teams"
    PAGERDUTY = "pagerduty"
    WEBHOOK = "webhook"
    SYSLOG = "syslog"


class EscalationAction(Enum):
    """Actions that can be taken during escalation."""
    NOTIFY = "notify"
    REASSIGN = "reassign"
    ESCALATE_MANAGER = "escalate_manager"
    ESCALATE_EXECUTIVE = "escalate_executive"
    AUTO_REMEDIATE = "auto_remediate"


class AlertSource(Enum):
    """Source systems that generate alerts."""
    SIEM = "siem"
    IDS = "ids"
    EDR = "edr"
    SCANNER = "scanner"
    MONITORING = "monitoring"
    MANUAL = "manual"
    API = "api"


# =============================================================================
# Core Data Models
# =============================================================================


@dataclass
class Alert:
    """
    Alert entity for security and operational alerts.

    Represents a single alert with full lifecycle tracking,
    assignment, and resolution capabilities.
    """
    alert_id: str
    customer_id: str  # For multi-tenant isolation
    title: str
    description: str

    # Classification
    severity: AlertSeverity = AlertSeverity.INFO
    category: AlertCategory = AlertCategory.OPERATIONAL
    source: AlertSource = AlertSource.MANUAL
    source_id: Optional[str] = None  # ID in source system

    # Affected resources
    affected_assets: List[str] = field(default_factory=list)  # Asset IDs or names
    indicators: Dict[str, Any] = field(default_factory=dict)  # IOCs, symptoms, etc.

    # Lifecycle
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    status: AlertStatus = AlertStatus.NEW

    # Assignment and handling
    assigned_to: Optional[str] = None  # User ID
    acknowledged_by: Optional[str] = None  # User ID
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None

    # Correlation
    related_alerts: List[str] = field(default_factory=list)  # Alert IDs
    tags: List[str] = field(default_factory=list)

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate alert data on creation."""
        if not self.alert_id or not self.alert_id.strip():
            raise ValueError("alert_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.title or not self.title.strip():
            raise ValueError("title is required")
        if not self.description or not self.description.strip():
            raise ValueError("description is required")

        # Normalize values
        self.alert_id = self.alert_id.strip()
        self.customer_id = self.customer_id.strip()
        self.title = self.title.strip()
        self.description = self.description.strip()

    @property
    def is_open(self) -> bool:
        """Check if alert is still open (not resolved or closed)."""
        return self.status in {AlertStatus.NEW, AlertStatus.ACKNOWLEDGED, AlertStatus.INVESTIGATING}

    @property
    def time_to_acknowledge(self) -> Optional[timedelta]:
        """Calculate time from creation to acknowledgment."""
        if not self.acknowledged_at:
            return None
        return self.acknowledged_at - self.created_at

    @property
    def time_to_resolve(self) -> Optional[timedelta]:
        """Calculate time from creation to resolution."""
        if not self.resolved_at:
            return None
        return self.resolved_at - self.created_at

    @property
    def age_minutes(self) -> float:
        """Calculate age of alert in minutes."""
        return (datetime.utcnow() - self.created_at).total_seconds() / 60

    @property
    def priority_score(self) -> float:
        """Calculate priority score based on severity, age, and category (0.0-10.0)."""
        score = 0.0

        # Severity factor (0-5 points)
        severity_scores = {
            AlertSeverity.INFO: 1.0,
            AlertSeverity.LOW: 2.0,
            AlertSeverity.MEDIUM: 3.0,
            AlertSeverity.HIGH: 4.0,
            AlertSeverity.CRITICAL: 5.0
        }
        score += severity_scores[self.severity]

        # Category factor (0-2 points)
        if self.category == AlertCategory.SECURITY:
            score += 2.0
        elif self.category == AlertCategory.COMPLIANCE:
            score += 1.5
        elif self.category == AlertCategory.AVAILABILITY:
            score += 1.0

        # Age factor (0-3 points)
        age_hours = self.age_minutes / 60
        if age_hours < 1:
            score += 0.5
        elif age_hours < 4:
            score += 1.5
        elif age_hours < 24:
            score += 2.5
        else:
            score += 3.0

        return min(score, 10.0)

    def validate(self) -> bool:
        """Validate alert data consistency."""
        # Status transitions
        if self.status in {AlertStatus.RESOLVED, AlertStatus.CLOSED} and not self.resolved_at:
            raise ValueError("resolved_at required for resolved/closed status")

        if self.acknowledged_by and not self.acknowledged_at:
            raise ValueError("acknowledged_at required when acknowledged_by is set")

        if self.resolved_at and not self.resolution_notes:
            raise ValueError("resolution_notes recommended for resolved alerts")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "alert_id": self.alert_id,
            "customer_id": self.customer_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "category": self.category.value,
            "source": self.source.value,
            "source_id": self.source_id,
            "affected_assets": self.affected_assets,
            "indicators": self.indicators,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "status": self.status.value,
            "assigned_to": self.assigned_to,
            "acknowledged_by": self.acknowledged_by,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "resolution_notes": self.resolution_notes,
            "related_alerts": self.related_alerts,
            "tags": self.tags,
            "is_open": self.is_open,
            "time_to_acknowledge_minutes": self.time_to_acknowledge.total_seconds() / 60 if self.time_to_acknowledge else None,
            "time_to_resolve_minutes": self.time_to_resolve.total_seconds() / 60 if self.time_to_resolve else None,
            "age_minutes": self.age_minutes,
            "priority_score": self.priority_score,
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "alert_id": self.alert_id,
            "customer_id": self.customer_id,
            "entity_type": "alert",
            "title": self.title,
            "severity": self.severity.value,
            "category": self.category.value,
            "source": self.source.value,
            "status": self.status.value,
            "affected_assets": self.affected_assets,
            "tags": self.tags,
            "is_open": self.is_open,
            "priority_score": self.priority_score,
            "age_minutes": self.age_minutes,
            "assigned_to": self.assigned_to,
            "related_alert_count": len(self.related_alerts),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Alert":
        """Create Alert from dictionary."""
        # Convert enum strings to enum types
        if isinstance(data.get("severity"), str):
            data["severity"] = AlertSeverity(data["severity"])
        if isinstance(data.get("category"), str):
            data["category"] = AlertCategory(data["category"])
        if isinstance(data.get("source"), str):
            data["source"] = AlertSource(data["source"])
        if isinstance(data.get("status"), str):
            data["status"] = AlertStatus(data["status"])

        # Convert ISO strings to datetime
        for field_name in ["created_at", "updated_at", "acknowledged_at", "resolved_at"]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(data[field_name])

        return cls(**data)


@dataclass
class AlertRule:
    """
    Alert Rule entity for automated alert generation.

    Defines conditions and actions for automatic alert creation
    based on events from various sources.
    """
    rule_id: str
    customer_id: str  # For multi-tenant isolation
    name: str
    description: str

    # Rule configuration
    enabled: bool = True
    conditions: Dict[str, Any] = field(default_factory=dict)  # Rule logic
    severity_mapping: Dict[str, str] = field(default_factory=dict)  # Condition -> severity

    # Alert generation
    category: AlertCategory = AlertCategory.OPERATIONAL
    notification_channels: List[NotificationChannel] = field(default_factory=list)
    escalation_policy_id: Optional[str] = None

    # Rate limiting
    suppression_window: int = 0  # Minutes to suppress duplicate alerts
    rate_limit: int = 0  # Max alerts per hour (0 = unlimited)

    # Metadata
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate rule data on creation."""
        if not self.rule_id or not self.rule_id.strip():
            raise ValueError("rule_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")

        # Normalize values
        self.rule_id = self.rule_id.strip()
        self.customer_id = self.customer_id.strip()
        self.name = self.name.strip()

    def validate(self) -> bool:
        """Validate rule configuration."""
        if not self.conditions:
            raise ValueError("conditions cannot be empty")

        if self.suppression_window < 0:
            raise ValueError("suppression_window cannot be negative")

        if self.rate_limit < 0:
            raise ValueError("rate_limit cannot be negative")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "rule_id": self.rule_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "conditions": self.conditions,
            "severity_mapping": self.severity_mapping,
            "category": self.category.value,
            "notification_channels": [ch.value for ch in self.notification_channels],
            "escalation_policy_id": self.escalation_policy_id,
            "suppression_window": self.suppression_window,
            "rate_limit": self.rate_limit,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "rule_id": self.rule_id,
            "customer_id": self.customer_id,
            "entity_type": "alert_rule",
            "name": self.name,
            "enabled": self.enabled,
            "category": self.category.value,
            "notification_channels": [ch.value for ch in self.notification_channels],
            "has_escalation_policy": self.escalation_policy_id is not None,
            "suppression_window": self.suppression_window,
            "rate_limit": self.rate_limit,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AlertRule":
        """Create AlertRule from dictionary."""
        # Convert enum strings to enum types
        if isinstance(data.get("category"), str):
            data["category"] = AlertCategory(data["category"])

        if "notification_channels" in data:
            data["notification_channels"] = [
                NotificationChannel(ch) if isinstance(ch, str) else ch
                for ch in data["notification_channels"]
            ]

        # Convert ISO strings to datetime
        for field_name in ["created_at", "updated_at"]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(data[field_name])

        return cls(**data)


@dataclass
class NotificationRule:
    """
    Notification Rule entity for alert notifications.

    Defines who gets notified and how based on alert characteristics.
    """
    notification_id: str
    customer_id: str  # For multi-tenant isolation
    name: str

    # Notification configuration
    channels: List[NotificationChannel] = field(default_factory=list)
    recipients: Dict[str, List[str]] = field(default_factory=dict)  # {channel: [recipients]}

    # Filtering
    severity_filter: List[AlertSeverity] = field(default_factory=list)  # Empty = all
    category_filter: List[AlertCategory] = field(default_factory=list)  # Empty = all

    # Scheduling
    schedule: Optional[Dict[str, Any]] = None  # Business hours, on-call schedule
    enabled: bool = True

    # Template and rate limiting
    template_id: Optional[str] = None  # Notification template
    rate_limit_minutes: int = 0  # Min time between notifications (0 = no limit)

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate notification rule data on creation."""
        if not self.notification_id or not self.notification_id.strip():
            raise ValueError("notification_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")

        # Normalize values
        self.notification_id = self.notification_id.strip()
        self.customer_id = self.customer_id.strip()
        self.name = self.name.strip()

    def validate(self) -> bool:
        """Validate notification rule configuration."""
        if not self.channels:
            raise ValueError("At least one notification channel required")

        if not self.recipients:
            raise ValueError("At least one recipient required")

        if self.rate_limit_minutes < 0:
            raise ValueError("rate_limit_minutes cannot be negative")

        return True

    def matches_alert(self, alert: Alert) -> bool:
        """Check if this notification rule applies to the given alert."""
        # Check severity filter
        if self.severity_filter and alert.severity not in self.severity_filter:
            return False

        # Check category filter
        if self.category_filter and alert.category not in self.category_filter:
            return False

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "notification_id": self.notification_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "channels": [ch.value for ch in self.channels],
            "recipients": self.recipients,
            "severity_filter": [sev.value for sev in self.severity_filter],
            "category_filter": [cat.value for cat in self.category_filter],
            "schedule": self.schedule,
            "enabled": self.enabled,
            "template_id": self.template_id,
            "rate_limit_minutes": self.rate_limit_minutes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "notification_id": self.notification_id,
            "customer_id": self.customer_id,
            "entity_type": "notification_rule",
            "name": self.name,
            "channels": [ch.value for ch in self.channels],
            "enabled": self.enabled,
            "severity_filter": [sev.value for sev in self.severity_filter],
            "category_filter": [cat.value for cat in self.category_filter],
            "has_schedule": self.schedule is not None,
            "rate_limit_minutes": self.rate_limit_minutes,
            "channel_count": len(self.channels),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NotificationRule":
        """Create NotificationRule from dictionary."""
        # Convert enum strings to enum types
        if "channels" in data:
            data["channels"] = [
                NotificationChannel(ch) if isinstance(ch, str) else ch
                for ch in data["channels"]
            ]

        if "severity_filter" in data:
            data["severity_filter"] = [
                AlertSeverity(sev) if isinstance(sev, str) else sev
                for sev in data["severity_filter"]
            ]

        if "category_filter" in data:
            data["category_filter"] = [
                AlertCategory(cat) if isinstance(cat, str) else cat
                for cat in data["category_filter"]
            ]

        # Convert ISO strings to datetime
        for field_name in ["created_at", "updated_at"]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(data[field_name])

        return cls(**data)


@dataclass
class EscalationLevel:
    """
    Escalation level configuration.

    Defines a single level in an escalation policy with timeout and actions.
    """
    level: int  # 1, 2, 3, etc.
    timeout_minutes: int  # Time before escalating to next level
    action: EscalationAction
    notify_users: List[str] = field(default_factory=list)  # User IDs
    notify_groups: List[str] = field(default_factory=list)  # Group IDs
    notify_oncall: Optional[str] = None  # On-call schedule ID

    def __post_init__(self):
        """Validate escalation level data."""
        if self.level < 1:
            raise ValueError("level must be >= 1")
        if self.timeout_minutes < 0:
            raise ValueError("timeout_minutes cannot be negative")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "level": self.level,
            "timeout_minutes": self.timeout_minutes,
            "action": self.action.value,
            "notify_users": self.notify_users,
            "notify_groups": self.notify_groups,
            "notify_oncall": self.notify_oncall,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EscalationLevel":
        """Create EscalationLevel from dictionary."""
        if isinstance(data.get("action"), str):
            data["action"] = EscalationAction(data["action"])
        return cls(**data)


@dataclass
class EscalationPolicy:
    """
    Escalation Policy entity for alert escalation.

    Defines multi-level escalation paths for unresolved alerts.
    """
    policy_id: str
    customer_id: str  # For multi-tenant isolation
    name: str
    description: str

    # Escalation levels
    levels: List[EscalationLevel] = field(default_factory=list)
    default_timeout_minutes: int = 30  # Default if level doesn't specify

    # Configuration
    business_hours_only: bool = False  # Only escalate during business hours
    enabled: bool = True

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate escalation policy data on creation."""
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

    def validate(self) -> bool:
        """Validate escalation policy configuration."""
        if not self.levels:
            raise ValueError("At least one escalation level required")

        if self.default_timeout_minutes < 0:
            raise ValueError("default_timeout_minutes cannot be negative")

        # Validate levels are sequential
        level_numbers = [level.level for level in self.levels]
        if sorted(level_numbers) != list(range(1, len(level_numbers) + 1)):
            raise ValueError("Escalation levels must be sequential starting from 1")

        return True

    def get_level(self, level_num: int) -> Optional[EscalationLevel]:
        """Get escalation level by number."""
        for level in self.levels:
            if level.level == level_num:
                return level
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "policy_id": self.policy_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "description": self.description,
            "levels": [level.to_dict() for level in self.levels],
            "default_timeout_minutes": self.default_timeout_minutes,
            "business_hours_only": self.business_hours_only,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "policy_id": self.policy_id,
            "customer_id": self.customer_id,
            "entity_type": "escalation_policy",
            "name": self.name,
            "enabled": self.enabled,
            "business_hours_only": self.business_hours_only,
            "level_count": len(self.levels),
            "default_timeout_minutes": self.default_timeout_minutes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EscalationPolicy":
        """Create EscalationPolicy from dictionary."""
        # Convert levels
        if "levels" in data:
            data["levels"] = [
                EscalationLevel.from_dict(level) if isinstance(level, dict) else level
                for level in data["levels"]
            ]

        # Convert ISO strings to datetime
        for field_name in ["created_at", "updated_at"]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(data[field_name])

        return cls(**data)


@dataclass
class AlertCorrelation:
    """
    Alert Correlation entity for related alert grouping.

    Groups related alerts together based on correlation logic
    to reduce alert fatigue and identify patterns.
    """
    correlation_id: str
    customer_id: str  # For multi-tenant isolation
    name: str

    # Correlated alerts
    alert_ids: List[str] = field(default_factory=list)
    correlation_type: str = "unknown"  # 'time_based', 'asset_based', 'pattern_based', etc.
    confidence_score: float = 0.0  # 0.0-1.0 confidence in correlation

    # Analysis
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "active"  # 'active', 'resolved', 'archived'
    analyst_notes: Optional[str] = None

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate correlation data on creation."""
        if not self.correlation_id or not self.correlation_id.strip():
            raise ValueError("correlation_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")
        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValueError("confidence_score must be between 0.0 and 1.0")

        # Normalize values
        self.correlation_id = self.correlation_id.strip()
        self.customer_id = self.customer_id.strip()
        self.name = self.name.strip()

    @property
    def alert_count(self) -> int:
        """Get number of correlated alerts."""
        return len(self.alert_ids)

    @property
    def is_active(self) -> bool:
        """Check if correlation is active."""
        return self.status == "active"

    def validate(self) -> bool:
        """Validate correlation data."""
        if len(self.alert_ids) < 2:
            raise ValueError("At least 2 alerts required for correlation")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "correlation_id": self.correlation_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "alert_ids": self.alert_ids,
            "correlation_type": self.correlation_type,
            "confidence_score": self.confidence_score,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "analyst_notes": self.analyst_notes,
            "alert_count": self.alert_count,
            "is_active": self.is_active,
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "correlation_id": self.correlation_id,
            "customer_id": self.customer_id,
            "entity_type": "alert_correlation",
            "name": self.name,
            "alert_ids": self.alert_ids,
            "correlation_type": self.correlation_type,
            "confidence_score": self.confidence_score,
            "status": self.status,
            "alert_count": self.alert_count,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AlertCorrelation":
        """Create AlertCorrelation from dictionary."""
        # Convert ISO strings to datetime
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])

        return cls(**data)
