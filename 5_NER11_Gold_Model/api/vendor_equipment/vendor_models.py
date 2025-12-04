"""
Vendor Equipment Models
=======================

Data models for E15: Vendor Equipment Lifecycle Management.
Includes Vendor, EquipmentModel, and SupportContract entities.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional, List, Dict, Any


class VendorRiskLevel(Enum):
    """Vendor risk classification levels."""
    LOW = "low"           # Risk score 0.0-3.0
    MEDIUM = "medium"     # Risk score 3.1-6.0
    HIGH = "high"         # Risk score 6.1-8.0
    CRITICAL = "critical" # Risk score 8.1-10.0


class SupportStatus(Enum):
    """Vendor support status for products."""
    ACTIVE = "active"       # Full support available
    LIMITED = "limited"     # Reduced support, security patches only
    EOL = "eol"             # End of Life, no support
    DEPRECATED = "deprecated"  # Deprecated, migration recommended


class LifecycleStatus(Enum):
    """Equipment lifecycle status."""
    CURRENT = "current"             # Within supported lifecycle
    APPROACHING_EOL = "approaching_eol"  # Within 180 days of EOL
    EOL = "eol"                     # Past EOL date
    EOS = "eos"                     # Past End of Support date
    RETIRED = "retired"             # Decommissioned


class MaintenanceSchedule(Enum):
    """Maintenance frequency schedules."""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUAL = "semi_annual"
    ANNUAL = "annual"
    ON_DEMAND = "on_demand"


class ServiceLevel(Enum):
    """Support contract service levels."""
    BASIC = "basic"           # Email support only
    STANDARD = "standard"     # 8x5 support
    PREMIUM = "premium"       # 24x7 support
    ENTERPRISE = "enterprise" # Dedicated support team


class Criticality(Enum):
    """Asset criticality levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Vendor:
    """
    Vendor entity for supply chain tracking.

    Represents a technology vendor with risk assessment and support status.
    """
    vendor_id: str
    name: str
    customer_id: str  # For multi-tenant isolation

    # Risk assessment
    risk_score: float = 0.0  # 0.0-10.0 scale
    risk_level: VendorRiskLevel = VendorRiskLevel.LOW

    # Support and status
    support_status: SupportStatus = SupportStatus.ACTIVE
    country: Optional[str] = None
    industry_focus: List[str] = field(default_factory=list)  # ['ICS', 'IT', 'Medical', 'IoT']
    supply_chain_tier: int = 1  # 1=direct, 2=indirect, 3=tertiary

    # Vulnerability metrics
    last_incident_date: Optional[date] = None
    total_cves: int = 0
    avg_cvss_score: float = 0.0
    critical_cve_count: int = 0

    # Metadata
    website: Optional[str] = None
    contact_email: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate vendor data on creation."""
        if not self.vendor_id or not self.vendor_id.strip():
            raise ValueError("vendor_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not 0.0 <= self.risk_score <= 10.0:
            raise ValueError("risk_score must be between 0.0 and 10.0")

        # Normalize values
        self.vendor_id = self.vendor_id.strip()
        self.name = self.name.strip()
        self.customer_id = self.customer_id.strip()

        # Calculate risk level from score
        self.risk_level = self._calculate_risk_level(self.risk_score)

    @staticmethod
    def _calculate_risk_level(score: float) -> VendorRiskLevel:
        """Calculate risk level from numeric score."""
        if score <= 3.0:
            return VendorRiskLevel.LOW
        elif score <= 6.0:
            return VendorRiskLevel.MEDIUM
        elif score <= 8.0:
            return VendorRiskLevel.HIGH
        else:
            return VendorRiskLevel.CRITICAL

    def to_neo4j_properties(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "vendor_id": self.vendor_id,
            "name": self.name,
            "customer_id": self.customer_id,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level.value,
            "support_status": self.support_status.value,
            "country": self.country,
            "industry_focus": self.industry_focus,
            "supply_chain_tier": self.supply_chain_tier,
            "last_incident_date": self.last_incident_date.isoformat() if self.last_incident_date else None,
            "total_cves": self.total_cves,
            "avg_cvss_score": self.avg_cvss_score,
            "critical_cve_count": self.critical_cve_count,
            "website": self.website,
            "contact_email": self.contact_email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "vendor_id": self.vendor_id,
            "name": self.name,
            "customer_id": self.customer_id,
            "entity_type": "vendor",
            "risk_score": self.risk_score,
            "risk_level": self.risk_level.value,
            "support_status": self.support_status.value,
            "country": self.country,
            "industry_focus": self.industry_focus,
            "supply_chain_tier": self.supply_chain_tier,
            "total_cves": self.total_cves,
            "avg_cvss_score": self.avg_cvss_score,
        }


@dataclass
class EquipmentModel:
    """
    Equipment Model entity for asset lifecycle tracking.

    Represents a specific equipment model from a vendor with EOL/EOS dates.
    """
    model_id: str
    vendor_id: str
    model_name: str
    customer_id: str  # For multi-tenant isolation

    # Product information
    product_line: Optional[str] = None
    release_date: Optional[date] = None
    eol_date: Optional[date] = None  # End of Life
    eos_date: Optional[date] = None  # End of Support

    # Version tracking
    current_version: Optional[str] = None
    supported_versions: List[str] = field(default_factory=list)

    # Maintenance
    maintenance_schedule: MaintenanceSchedule = MaintenanceSchedule.QUARTERLY
    criticality: Criticality = Criticality.MEDIUM
    lifecycle_status: LifecycleStatus = LifecycleStatus.CURRENT

    # Asset counts
    deployed_count: int = 0
    vulnerability_count: int = 0

    # Metadata
    description: Optional[str] = None
    category: Optional[str] = None  # 'network', 'server', 'workstation', 'iot', 'scada'
    firmware_version: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate equipment model data."""
        if not self.model_id or not self.model_id.strip():
            raise ValueError("model_id is required")
        if not self.vendor_id or not self.vendor_id.strip():
            raise ValueError("vendor_id is required")
        if not self.model_name or not self.model_name.strip():
            raise ValueError("model_name is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")

        # Normalize values
        self.model_id = self.model_id.strip()
        self.vendor_id = self.vendor_id.strip()
        self.model_name = self.model_name.strip()
        self.customer_id = self.customer_id.strip()

        # Calculate lifecycle status
        self.lifecycle_status = self._calculate_lifecycle_status()

    def _calculate_lifecycle_status(self) -> LifecycleStatus:
        """Calculate lifecycle status based on dates."""
        today = date.today()

        # Check EOS first (more severe)
        if self.eos_date and today > self.eos_date:
            return LifecycleStatus.EOS

        # Check EOL
        if self.eol_date:
            if today > self.eol_date:
                return LifecycleStatus.EOL
            # Check if approaching EOL (within 180 days)
            days_to_eol = (self.eol_date - today).days
            if days_to_eol <= 180:
                return LifecycleStatus.APPROACHING_EOL

        return LifecycleStatus.CURRENT

    def days_to_eol(self) -> Optional[int]:
        """Calculate days until EOL, or negative if past."""
        if not self.eol_date:
            return None
        return (self.eol_date - date.today()).days

    def days_to_eos(self) -> Optional[int]:
        """Calculate days until EOS, or negative if past."""
        if not self.eos_date:
            return None
        return (self.eos_date - date.today()).days

    def to_neo4j_properties(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "model_id": self.model_id,
            "vendor_id": self.vendor_id,
            "model_name": self.model_name,
            "customer_id": self.customer_id,
            "product_line": self.product_line,
            "release_date": self.release_date.isoformat() if self.release_date else None,
            "eol_date": self.eol_date.isoformat() if self.eol_date else None,
            "eos_date": self.eos_date.isoformat() if self.eos_date else None,
            "current_version": self.current_version,
            "supported_versions": self.supported_versions,
            "maintenance_schedule": self.maintenance_schedule.value,
            "criticality": self.criticality.value,
            "lifecycle_status": self.lifecycle_status.value,
            "deployed_count": self.deployed_count,
            "vulnerability_count": self.vulnerability_count,
            "description": self.description,
            "category": self.category,
            "firmware_version": self.firmware_version,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "model_id": self.model_id,
            "vendor_id": self.vendor_id,
            "model_name": self.model_name,
            "customer_id": self.customer_id,
            "entity_type": "equipment_model",
            "product_line": self.product_line,
            "eol_date": self.eol_date.isoformat() if self.eol_date else None,
            "eos_date": self.eos_date.isoformat() if self.eos_date else None,
            "lifecycle_status": self.lifecycle_status.value,
            "criticality": self.criticality.value,
            "category": self.category,
            "deployed_count": self.deployed_count,
            "vulnerability_count": self.vulnerability_count,
        }


@dataclass
class SupportContract:
    """
    Support Contract entity for vendor service tracking.

    Tracks support agreements between customers and vendors.
    """
    contract_id: str
    vendor_id: str
    customer_id: str  # For multi-tenant isolation

    # Contract dates
    start_date: date
    end_date: date

    # Service details
    service_level: ServiceLevel = ServiceLevel.STANDARD
    response_time_sla: int = 24  # hours
    coverage: List[str] = field(default_factory=list)  # ['security_patches', 'firmware_updates', '24/7_support']

    # Status
    status: str = "active"  # 'active', 'expired', 'pending_renewal'

    # Financial
    annual_cost: float = 0.0
    currency: str = "USD"

    # Equipment covered
    covered_model_ids: List[str] = field(default_factory=list)

    # Metadata
    contract_reference: Optional[str] = None
    renewal_reminder_days: int = 90
    auto_renew: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate support contract data."""
        if not self.contract_id or not self.contract_id.strip():
            raise ValueError("contract_id is required")
        if not self.vendor_id or not self.vendor_id.strip():
            raise ValueError("vendor_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")

        # Normalize values
        self.contract_id = self.contract_id.strip()
        self.vendor_id = self.vendor_id.strip()
        self.customer_id = self.customer_id.strip()

        # Update status based on dates
        self.status = self._calculate_status()

    def _calculate_status(self) -> str:
        """Calculate contract status based on dates."""
        today = date.today()

        if today > self.end_date:
            return "expired"

        days_remaining = (self.end_date - today).days
        if days_remaining <= self.renewal_reminder_days:
            return "pending_renewal"

        return "active"

    def days_remaining(self) -> int:
        """Calculate days remaining on contract."""
        return (self.end_date - date.today()).days

    def is_expiring_soon(self) -> bool:
        """Check if contract is expiring within reminder period."""
        return 0 < self.days_remaining() <= self.renewal_reminder_days

    def to_neo4j_properties(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "contract_id": self.contract_id,
            "vendor_id": self.vendor_id,
            "customer_id": self.customer_id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "service_level": self.service_level.value,
            "response_time_sla": self.response_time_sla,
            "coverage": self.coverage,
            "status": self.status,
            "annual_cost": self.annual_cost,
            "currency": self.currency,
            "covered_model_ids": self.covered_model_ids,
            "contract_reference": self.contract_reference,
            "renewal_reminder_days": self.renewal_reminder_days,
            "auto_renew": self.auto_renew,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "contract_id": self.contract_id,
            "vendor_id": self.vendor_id,
            "customer_id": self.customer_id,
            "entity_type": "support_contract",
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "service_level": self.service_level.value,
            "status": self.status,
            "annual_cost": self.annual_cost,
        }


class AlertSeverity(Enum):
    """Alert severity levels for EOL/EOS notifications."""
    INFO = "info"          # Informational, >90 days
    WARNING = "warning"    # Attention needed, 30-90 days
    HIGH = "high"          # Action required, 7-30 days
    CRITICAL = "critical"  # Immediate action, <7 days or past due


class AlertType(Enum):
    """Types of lifecycle alerts."""
    EOL_APPROACHING = "eol_approaching"
    EOL_PAST = "eol_past"
    EOS_APPROACHING = "eos_approaching"
    EOS_PAST = "eos_past"
    CONTRACT_EXPIRING = "contract_expiring"
    CONTRACT_EXPIRED = "contract_expired"
    VENDOR_RISK_INCREASED = "vendor_risk_increased"
    VULNERABILITY_DETECTED = "vulnerability_detected"


@dataclass
class EOLAlert:
    """
    End of Life Alert for equipment lifecycle management.

    Provides structured alerting for EOL/EOS dates and contract expirations.
    """
    alert_id: str
    alert_type: AlertType
    severity: AlertSeverity
    customer_id: str

    # Related entity
    entity_type: str  # 'equipment_model', 'support_contract', 'vendor'
    entity_id: str
    entity_name: str

    # Alert details
    message: str
    days_remaining: int  # Negative if past due
    target_date: Optional[date] = None  # EOL/EOS/expiration date

    # Context
    vendor_id: Optional[str] = None
    vendor_name: Optional[str] = None
    affected_asset_count: int = 0

    # Recommendations
    recommended_action: Optional[str] = None
    replacement_model_ids: List[str] = field(default_factory=list)

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate alert and auto-calculate severity if not provided."""
        if not self.alert_id or not self.alert_id.strip():
            raise ValueError("alert_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.entity_id or not self.entity_id.strip():
            raise ValueError("entity_id is required")

        # Auto-calculate severity from days_remaining if needed
        if self.severity is None:
            self.severity = self._calculate_severity()

    def _calculate_severity(self) -> AlertSeverity:
        """Calculate severity based on days remaining."""
        if self.days_remaining < 0:
            return AlertSeverity.CRITICAL  # Past due
        elif self.days_remaining <= 7:
            return AlertSeverity.CRITICAL
        elif self.days_remaining <= 30:
            return AlertSeverity.HIGH
        elif self.days_remaining <= 90:
            return AlertSeverity.WARNING
        else:
            return AlertSeverity.INFO

    @classmethod
    def from_equipment_model(
        cls,
        model: "EquipmentModel",
        alert_type: AlertType,
        vendor_name: Optional[str] = None,
    ) -> "EOLAlert":
        """Create alert from EquipmentModel."""
        import uuid

        # Determine target date and days remaining
        if alert_type in (AlertType.EOL_APPROACHING, AlertType.EOL_PAST):
            target_date = model.eol_date
            days_remaining = model.days_to_eol() or 0
        elif alert_type in (AlertType.EOS_APPROACHING, AlertType.EOS_PAST):
            target_date = model.eos_date
            days_remaining = model.days_to_eos() or 0
        else:
            target_date = None
            days_remaining = 0

        # Calculate severity
        if days_remaining < 0:
            severity = AlertSeverity.CRITICAL
        elif days_remaining <= 7:
            severity = AlertSeverity.CRITICAL
        elif days_remaining <= 30:
            severity = AlertSeverity.HIGH
        elif days_remaining <= 90:
            severity = AlertSeverity.WARNING
        else:
            severity = AlertSeverity.INFO

        # Generate message
        if days_remaining < 0:
            message = f"{model.model_name} is {abs(days_remaining)} days past {alert_type.value.replace('_', ' ')}"
        else:
            message = f"{model.model_name} {alert_type.value.replace('_', ' ')} in {days_remaining} days"

        return cls(
            alert_id=f"ALERT-{uuid.uuid4().hex[:8].upper()}",
            alert_type=alert_type,
            severity=severity,
            customer_id=model.customer_id,
            entity_type="equipment_model",
            entity_id=model.model_id,
            entity_name=model.model_name,
            message=message,
            days_remaining=days_remaining,
            target_date=target_date,
            vendor_id=model.vendor_id,
            vendor_name=vendor_name,
            affected_asset_count=model.deployed_count,
            recommended_action="Plan migration to supported equipment" if days_remaining <= 90 else None,
        )

    @classmethod
    def from_support_contract(
        cls,
        contract: "SupportContract",
        vendor_name: Optional[str] = None,
    ) -> "EOLAlert":
        """Create alert from SupportContract."""
        import uuid

        days_remaining = contract.days_remaining()

        if days_remaining < 0:
            alert_type = AlertType.CONTRACT_EXPIRED
            severity = AlertSeverity.CRITICAL
            message = f"Support contract {contract.contract_id} expired {abs(days_remaining)} days ago"
        else:
            alert_type = AlertType.CONTRACT_EXPIRING
            if days_remaining <= 7:
                severity = AlertSeverity.CRITICAL
            elif days_remaining <= 30:
                severity = AlertSeverity.HIGH
            elif days_remaining <= 90:
                severity = AlertSeverity.WARNING
            else:
                severity = AlertSeverity.INFO
            message = f"Support contract {contract.contract_id} expires in {days_remaining} days"

        return cls(
            alert_id=f"ALERT-{uuid.uuid4().hex[:8].upper()}",
            alert_type=alert_type,
            severity=severity,
            customer_id=contract.customer_id,
            entity_type="support_contract",
            entity_id=contract.contract_id,
            entity_name=f"Contract {contract.contract_id}",
            message=message,
            days_remaining=days_remaining,
            target_date=contract.end_date,
            vendor_id=contract.vendor_id,
            vendor_name=vendor_name,
            affected_asset_count=len(contract.covered_model_ids),
            recommended_action="Initiate contract renewal process" if days_remaining <= 90 else None,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary for API response."""
        return {
            "alert_id": self.alert_id,
            "alert_type": self.alert_type.value,
            "severity": self.severity.value,
            "customer_id": self.customer_id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "entity_name": self.entity_name,
            "message": self.message,
            "days_remaining": self.days_remaining,
            "target_date": self.target_date.isoformat() if self.target_date else None,
            "vendor_id": self.vendor_id,
            "vendor_name": self.vendor_name,
            "affected_asset_count": self.affected_asset_count,
            "recommended_action": self.recommended_action,
            "replacement_model_ids": self.replacement_model_ids,
            "created_at": self.created_at.isoformat(),
            "acknowledged": self.acknowledged,
            "acknowledged_by": self.acknowledged_by,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload for alert storage."""
        return {
            "alert_id": self.alert_id,
            "alert_type": self.alert_type.value,
            "severity": self.severity.value,
            "customer_id": self.customer_id,
            "entity_type": "eol_alert",
            "entity_id": self.entity_id,
            "entity_name": self.entity_name,
            "days_remaining": self.days_remaining,
            "target_date": self.target_date.isoformat() if self.target_date else None,
            "vendor_id": self.vendor_id,
            "acknowledged": self.acknowledged,
        }


# =========================================================================
# Maintenance Scheduling Models (Days 7-9)
# =========================================================================


class MaintenanceWindowType(Enum):
    """Types of maintenance windows."""
    SCHEDULED = "scheduled"       # Regular scheduled maintenance
    EMERGENCY = "emergency"       # Emergency maintenance window
    CHANGE_FREEZE = "change_freeze"  # No changes allowed
    PATCHING = "patching"         # Security patching window
    FIRMWARE = "firmware"         # Firmware update window


class WorkOrderStatus(Enum):
    """Work order lifecycle status."""
    DRAFT = "draft"           # Work order being created
    PENDING = "pending"       # Awaiting approval
    APPROVED = "approved"     # Approved, not started
    IN_PROGRESS = "in_progress"  # Currently executing
    ON_HOLD = "on_hold"       # Temporarily paused
    COMPLETED = "completed"   # Successfully completed
    CANCELLED = "cancelled"   # Cancelled before completion
    FAILED = "failed"         # Failed during execution


class WorkOrderPriority(Enum):
    """Work order priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class MaintenanceWindow:
    """
    Maintenance Window for scheduling equipment maintenance activities.

    Defines allowed time windows for maintenance operations on equipment.
    """
    window_id: str
    customer_id: str
    name: str
    window_type: MaintenanceWindowType = MaintenanceWindowType.SCHEDULED

    # Time window definition
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    duration_hours: int = 4  # Default 4-hour window

    # Recurrence
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None  # 'daily', 'weekly', 'monthly', 'quarterly'
    recurrence_day: Optional[int] = None  # Day of week (0-6) or month (1-31)

    # Scope
    equipment_ids: List[str] = field(default_factory=list)  # Specific equipment
    vendor_ids: List[str] = field(default_factory=list)     # All equipment from vendors
    categories: List[str] = field(default_factory=list)     # Equipment categories

    # Status
    is_active: bool = True
    approved_by: Optional[str] = None
    approval_date: Optional[datetime] = None

    # Metadata
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate maintenance window data."""
        if not self.window_id or not self.window_id.strip():
            raise ValueError("window_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")

        self.window_id = self.window_id.strip()
        self.customer_id = self.customer_id.strip()
        self.name = self.name.strip()

        # Calculate end_time if not provided
        if self.end_time is None:
            from datetime import timedelta
            self.end_time = self.start_time + timedelta(hours=self.duration_hours)

    def is_in_window(self, check_time: Optional[datetime] = None) -> bool:
        """Check if a given time falls within this maintenance window."""
        if check_time is None:
            check_time = datetime.utcnow()
        return self.start_time <= check_time <= self.end_time

    def get_next_occurrence(self, after: Optional[datetime] = None) -> Optional[datetime]:
        """Get next occurrence of recurring window."""
        if not self.is_recurring:
            if after is None or self.start_time > after:
                return self.start_time
            return None

        from datetime import timedelta

        if after is None:
            after = datetime.utcnow()

        next_start = self.start_time
        while next_start <= after:
            if self.recurrence_pattern == "daily":
                next_start += timedelta(days=1)
            elif self.recurrence_pattern == "weekly":
                next_start += timedelta(weeks=1)
            elif self.recurrence_pattern == "monthly":
                # Add approximately one month
                next_start += timedelta(days=30)
            elif self.recurrence_pattern == "quarterly":
                next_start += timedelta(days=90)
            else:
                break

        return next_start

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "window_id": self.window_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "window_type": self.window_type.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_hours": self.duration_hours,
            "is_recurring": self.is_recurring,
            "recurrence_pattern": self.recurrence_pattern,
            "recurrence_day": self.recurrence_day,
            "equipment_ids": self.equipment_ids,
            "vendor_ids": self.vendor_ids,
            "categories": self.categories,
            "is_active": self.is_active,
            "approved_by": self.approved_by,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "window_id": self.window_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "entity_type": "maintenance_window",
            "window_type": self.window_type.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "is_recurring": self.is_recurring,
            "recurrence_pattern": self.recurrence_pattern,
            "is_active": self.is_active,
            "equipment_ids": self.equipment_ids,
            "vendor_ids": self.vendor_ids,
            "categories": self.categories,
        }


@dataclass
class MaintenancePrediction:
    """
    Predictive Maintenance result for equipment.

    Based on maintenance history, failure patterns, and equipment age.
    """
    equipment_id: str
    equipment_name: str
    customer_id: str

    # Prediction results
    next_maintenance_date: date
    confidence_score: float  # 0.0-1.0
    prediction_reason: str

    # Risk factors
    days_until_maintenance: int
    risk_score: float  # 0.0-10.0
    risk_factors: List[str] = field(default_factory=list)

    # Historical data
    last_maintenance_date: Optional[date] = None
    maintenance_count: int = 0
    avg_days_between_maintenance: Optional[float] = None
    failure_count: int = 0

    # Recommendations
    recommended_tasks: List[str] = field(default_factory=list)
    estimated_downtime_hours: float = 0.0
    estimated_cost: float = 0.0

    # Metadata
    prediction_date: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "equipment_id": self.equipment_id,
            "equipment_name": self.equipment_name,
            "customer_id": self.customer_id,
            "next_maintenance_date": self.next_maintenance_date.isoformat(),
            "confidence_score": self.confidence_score,
            "prediction_reason": self.prediction_reason,
            "days_until_maintenance": self.days_until_maintenance,
            "risk_score": self.risk_score,
            "risk_factors": self.risk_factors,
            "last_maintenance_date": self.last_maintenance_date.isoformat() if self.last_maintenance_date else None,
            "maintenance_count": self.maintenance_count,
            "avg_days_between_maintenance": self.avg_days_between_maintenance,
            "failure_count": self.failure_count,
            "recommended_tasks": self.recommended_tasks,
            "estimated_downtime_hours": self.estimated_downtime_hours,
            "estimated_cost": self.estimated_cost,
            "prediction_date": self.prediction_date.isoformat(),
        }


@dataclass
class MaintenanceWorkOrder:
    """
    Work Order for maintenance activities.

    Tracks planned and executed maintenance tasks on equipment.
    """
    work_order_id: str
    customer_id: str
    title: str

    # Equipment scope
    equipment_ids: List[str] = field(default_factory=list)
    vendor_id: Optional[str] = None

    # Status and priority
    status: WorkOrderStatus = WorkOrderStatus.DRAFT
    priority: WorkOrderPriority = WorkOrderPriority.MEDIUM

    # Scheduling
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    maintenance_window_id: Optional[str] = None

    # Work details
    description: Optional[str] = None
    tasks: List[str] = field(default_factory=list)  # List of task descriptions
    required_parts: List[str] = field(default_factory=list)
    estimated_hours: float = 0.0
    actual_hours: float = 0.0

    # Assignment
    assigned_to: Optional[str] = None
    assigned_team: Optional[str] = None

    # Approvals
    requested_by: Optional[str] = None
    approved_by: Optional[str] = None
    approval_date: Optional[datetime] = None

    # Completion
    completion_notes: Optional[str] = None
    issues_found: List[str] = field(default_factory=list)
    follow_up_required: bool = False
    follow_up_work_order_id: Optional[str] = None

    # Costs
    estimated_cost: float = 0.0
    actual_cost: float = 0.0

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate work order data."""
        if not self.work_order_id or not self.work_order_id.strip():
            raise ValueError("work_order_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.title or not self.title.strip():
            raise ValueError("title is required")

        self.work_order_id = self.work_order_id.strip()
        self.customer_id = self.customer_id.strip()
        self.title = self.title.strip()

    def get_duration_hours(self) -> Optional[float]:
        """Calculate actual duration in hours."""
        if self.actual_start and self.actual_end:
            delta = self.actual_end - self.actual_start
            return delta.total_seconds() / 3600
        return None

    def is_overdue(self) -> bool:
        """Check if work order is overdue."""
        if self.status in [WorkOrderStatus.COMPLETED, WorkOrderStatus.CANCELLED]:
            return False
        if self.scheduled_end:
            return datetime.utcnow() > self.scheduled_end
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "work_order_id": self.work_order_id,
            "customer_id": self.customer_id,
            "title": self.title,
            "equipment_ids": self.equipment_ids,
            "vendor_id": self.vendor_id,
            "status": self.status.value,
            "priority": self.priority.value,
            "scheduled_start": self.scheduled_start.isoformat() if self.scheduled_start else None,
            "scheduled_end": self.scheduled_end.isoformat() if self.scheduled_end else None,
            "actual_start": self.actual_start.isoformat() if self.actual_start else None,
            "actual_end": self.actual_end.isoformat() if self.actual_end else None,
            "maintenance_window_id": self.maintenance_window_id,
            "description": self.description,
            "tasks": self.tasks,
            "required_parts": self.required_parts,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "assigned_to": self.assigned_to,
            "assigned_team": self.assigned_team,
            "requested_by": self.requested_by,
            "approved_by": self.approved_by,
            "approval_date": self.approval_date.isoformat() if self.approval_date else None,
            "completion_notes": self.completion_notes,
            "issues_found": self.issues_found,
            "follow_up_required": self.follow_up_required,
            "estimated_cost": self.estimated_cost,
            "actual_cost": self.actual_cost,
            "is_overdue": self.is_overdue(),
            "duration_hours": self.get_duration_hours(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "work_order_id": self.work_order_id,
            "customer_id": self.customer_id,
            "title": self.title,
            "entity_type": "work_order",
            "equipment_ids": self.equipment_ids,
            "vendor_id": self.vendor_id,
            "status": self.status.value,
            "priority": self.priority.value,
            "scheduled_start": self.scheduled_start.isoformat() if self.scheduled_start else None,
            "scheduled_end": self.scheduled_end.isoformat() if self.scheduled_end else None,
            "maintenance_window_id": self.maintenance_window_id,
            "assigned_to": self.assigned_to,
            "follow_up_required": self.follow_up_required,
        }
