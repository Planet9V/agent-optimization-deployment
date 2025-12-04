"""
Prioritization Data Models
==========================

Data models for E12: NOW-NEXT-NEVER Prioritization Framework.
Includes priority categories, scoring factors, and configuration.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any


# =============================================================================
# Enums for Prioritization
# =============================================================================


class PriorityCategory(Enum):
    """Priority categories for triage."""
    NOW = "NOW"       # Immediate action required
    NEXT = "NEXT"     # Scheduled for next action cycle
    NEVER = "NEVER"   # No action planned (low priority/low value)


class EntityType(Enum):
    """Types of entities that can be prioritized."""
    VULNERABILITY = "vulnerability"
    REMEDIATION = "remediation"
    COMPLIANCE = "compliance"
    RISK = "risk"
    INCIDENT = "incident"


class SLAStatus(Enum):
    """SLA compliance status."""
    WITHIN_SLA = "within_sla"       # Well within SLA
    AT_RISK = "at_risk"             # Approaching SLA breach
    BREACHED = "breached"           # SLA breached


class UrgencyType(Enum):
    """Types of urgency factors."""
    EXPLOIT_AVAILABLE = "exploit_available"
    ACTIVE_CAMPAIGN = "active_campaign"
    COMPLIANCE_DEADLINE = "compliance_deadline"
    BUSINESS_CRITICAL = "business_critical"
    SLA_BREACH = "sla_breach"
    REGULATORY = "regulatory"


class ImpactType(Enum):
    """Types of business impact."""
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    REPUTATIONAL = "reputational"
    COMPLIANCE = "compliance"
    DATA_BREACH = "data_breach"


# =============================================================================
# Core Data Models
# =============================================================================


@dataclass
class UrgencyFactor:
    """
    Individual urgency factor contributing to priority.

    Represents time-sensitive factors that elevate priority
    (exploits, active attacks, deadlines).
    """
    factor_type: UrgencyType
    weight: float  # 0.0-1.0 importance weight
    value: float   # 0.0-10.0 urgency value
    description: str
    deadline: Optional[datetime] = None
    evidence: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate urgency factor data."""
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError("weight must be between 0.0 and 1.0")
        if not 0.0 <= self.value <= 10.0:
            raise ValueError("value must be between 0.0 and 10.0")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "factor_type": self.factor_type.value,
            "weight": self.weight,
            "value": self.value,
            "description": self.description,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "evidence": self.evidence,
        }


@dataclass
class RiskFactor:
    """
    Risk factor contributing to priority.

    Represents risk-based factors from E05 risk scoring.
    """
    factor_type: str  # vulnerability, threat, exposure, asset
    weight: float  # 0.0-1.0
    value: float   # 0.0-10.0
    description: str

    def __post_init__(self):
        """Validate risk factor data."""
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError("weight must be between 0.0 and 1.0")
        if not 0.0 <= self.value <= 10.0:
            raise ValueError("value must be between 0.0 and 10.0")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "factor_type": self.factor_type,
            "weight": self.weight,
            "value": self.value,
            "description": self.description,
        }


@dataclass
class EconomicFactor:
    """
    Economic factor contributing to priority.

    Represents cost-benefit factors from E10 economic module.
    """
    factor_type: str  # roi, cost_savings, risk_reduction_value
    weight: float  # 0.0-1.0
    value: float   # Economic value (can be negative for costs)
    description: str
    currency: str = "USD"

    def __post_init__(self):
        """Validate economic factor data."""
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError("weight must be between 0.0 and 1.0")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "factor_type": self.factor_type,
            "weight": self.weight,
            "value": self.value,
            "description": self.description,
            "currency": self.currency,
        }


@dataclass
class ScoringFactor:
    """
    Generic scoring factor for priority calculation.
    """
    factor_name: str
    factor_category: str  # risk, urgency, impact, effort, roi
    weight: float  # 0.0-1.0
    value: float   # 0.0-10.0 or economic value
    description: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "factor_name": self.factor_name,
            "factor_category": self.factor_category,
            "weight": self.weight,
            "value": self.value,
            "description": self.description,
        }


@dataclass
class PriorityItem:
    """
    Entity with priority categorization and scoring.

    Represents any entity (vulnerability, remediation, etc.) that
    requires prioritization for resource allocation.
    """
    item_id: str
    customer_id: str  # For multi-tenant isolation
    entity_type: EntityType
    entity_id: str
    entity_name: str

    # Priority classification
    priority_category: PriorityCategory
    priority_score: float  # 0-100 composite score

    # Contributing factors
    urgency_factors: List[UrgencyFactor] = field(default_factory=list)
    risk_factors: List[RiskFactor] = field(default_factory=list)
    economic_factors: List[EconomicFactor] = field(default_factory=list)

    # Deadline and SLA
    deadline: Optional[datetime] = None
    sla_status: SLAStatus = SLAStatus.WITHIN_SLA
    sla_deadline: Optional[datetime] = None

    # Calculated at
    calculated_at: datetime = field(default_factory=datetime.utcnow)

    # Additional metadata
    assigned_to: Optional[str] = None
    remediation_plan: Optional[str] = None
    estimated_effort_hours: Optional[float] = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate priority item data."""
        if not self.item_id or not self.item_id.strip():
            raise ValueError("item_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.entity_id or not self.entity_id.strip():
            raise ValueError("entity_id is required")
        if not 0.0 <= self.priority_score <= 100.0:
            raise ValueError("priority_score must be between 0.0 and 100.0")

        # Normalize values
        self.item_id = self.item_id.strip()
        self.customer_id = self.customer_id.strip()
        self.entity_id = self.entity_id.strip()

    @property
    def is_now(self) -> bool:
        """Check if item is NOW priority."""
        return self.priority_category == PriorityCategory.NOW

    @property
    def is_sla_at_risk(self) -> bool:
        """Check if SLA is at risk or breached."""
        return self.sla_status in {SLAStatus.AT_RISK, SLAStatus.BREACHED}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "item_id": self.item_id,
            "customer_id": self.customer_id,
            "entity_type": self.entity_type.value,
            "entity_id": self.entity_id,
            "entity_name": self.entity_name,
            "priority_category": self.priority_category.value,
            "priority_score": self.priority_score,
            "urgency_factors": [f.to_dict() for f in self.urgency_factors],
            "risk_factors": [f.to_dict() for f in self.risk_factors],
            "economic_factors": [f.to_dict() for f in self.economic_factors],
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "sla_status": self.sla_status.value,
            "sla_deadline": self.sla_deadline.isoformat() if self.sla_deadline else None,
            "calculated_at": self.calculated_at.isoformat(),
            "assigned_to": self.assigned_to,
            "remediation_plan": self.remediation_plan,
            "estimated_effort_hours": self.estimated_effort_hours,
            "is_now": self.is_now,
            "is_sla_at_risk": self.is_sla_at_risk,
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "item_id": self.item_id,
            "customer_id": self.customer_id,
            "entity_type": self.entity_type.value,
            "entity_id": self.entity_id,
            "entity_name": self.entity_name,
            "priority_category": self.priority_category.value,
            "priority_score": self.priority_score,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "sla_status": self.sla_status.value,
            "calculated_at": self.calculated_at.isoformat(),
            "is_now": self.is_now,
            "is_sla_at_risk": self.is_sla_at_risk,
        }


@dataclass
class PriorityScore:
    """
    Detailed priority score breakdown.

    Shows how priority score was calculated from individual factors.
    """
    entity_id: str
    customer_id: str
    overall_score: float  # 0-100
    category: PriorityCategory

    # Score breakdown
    score_breakdown: Dict[str, float] = field(default_factory=dict)
    confidence: float = 0.0  # 0.0-1.0

    # Contributing factors
    factors: List[ScoringFactor] = field(default_factory=list)

    def __post_init__(self):
        """Validate priority score data."""
        if not 0.0 <= self.overall_score <= 100.0:
            raise ValueError("overall_score must be between 0.0 and 100.0")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "entity_id": self.entity_id,
            "customer_id": self.customer_id,
            "overall_score": self.overall_score,
            "category": self.category.value,
            "score_breakdown": self.score_breakdown,
            "confidence": self.confidence,
            "factors": [f.to_dict() for f in self.factors],
        }


@dataclass
class PrioritizationConfig:
    """
    Customer-specific prioritization configuration.

    Defines scoring weights and thresholds for NOW/NEXT/NEVER categorization.
    """
    customer_id: str

    # Scoring weights (must sum to 1.0)
    scoring_weights: Dict[str, float] = field(default_factory=lambda: {
        "risk_weight": 0.30,
        "urgency_weight": 0.25,
        "impact_weight": 0.25,
        "effort_weight": 0.10,
        "roi_weight": 0.10,
    })

    # Thresholds for categorization
    thresholds: Dict[str, float] = field(default_factory=lambda: {
        "now_threshold": 70.0,    # Score >= 70 = NOW
        "next_threshold": 40.0,   # Score >= 40 = NEXT, < 40 = NEVER
    })

    # SLA configuration (hours)
    sla_config: Dict[str, float] = field(default_factory=lambda: {
        "now_sla_hours": 24.0,
        "next_sla_hours": 168.0,  # 7 days
    })

    def __post_init__(self):
        """Validate configuration."""
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")

        # Validate weights sum to 1.0
        weight_sum = sum(self.scoring_weights.values())
        if not 0.99 <= weight_sum <= 1.01:  # Allow for floating point precision
            raise ValueError(f"Scoring weights must sum to 1.0, got {weight_sum}")

        # Validate thresholds
        if self.thresholds["now_threshold"] <= self.thresholds["next_threshold"]:
            raise ValueError("now_threshold must be greater than next_threshold")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "customer_id": self.customer_id,
            "scoring_weights": self.scoring_weights,
            "thresholds": self.thresholds,
            "sla_config": self.sla_config,
        }
