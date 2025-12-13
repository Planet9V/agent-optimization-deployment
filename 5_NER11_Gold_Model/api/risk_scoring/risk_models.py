"""
Risk Scoring Models
===================

Data models for E05: Risk Scoring Engine API.
Includes RiskScore, RiskFactor, AssetCriticality, ExposureScore, and RiskAggregation entities.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional, List, Dict, Any


# =============================================================================
# Enums for Risk Scoring
# =============================================================================


class RiskLevel(Enum):
    """Risk severity levels."""
    LOW = "low"           # 0.0-2.5
    MEDIUM = "medium"     # 2.6-5.0
    HIGH = "high"         # 5.1-7.5
    CRITICAL = "critical" # 7.6-10.0


class RiskFactorType(Enum):
    """Types of risk factors contributing to overall score."""
    VULNERABILITY = "vulnerability"   # Known vulnerabilities
    THREAT = "threat"                 # Active threat presence
    EXPOSURE = "exposure"             # Attack surface exposure
    ASSET = "asset"                   # Asset criticality
    COMPLIANCE = "compliance"         # Compliance violations


class RiskTrend(Enum):
    """Risk score trend indicators."""
    IMPROVING = "improving"     # Risk decreasing
    STABLE = "stable"           # Risk unchanged
    DEGRADING = "degrading"     # Risk increasing
    INCREASING = "degrading"    # Alias for DEGRADING (backward compatibility)
    DECREASING = "improving"    # Alias for IMPROVING (backward compatibility)


class BusinessImpact(Enum):
    """Business impact levels for asset criticality."""
    MINIMAL = "minimal"             # Minimal business disruption
    MODERATE = "moderate"           # Some business disruption
    SIGNIFICANT = "significant"     # Major business disruption
    SEVERE = "severe"               # Critical business disruption
    CATASTROPHIC = "catastrophic"   # Complete business failure


class DataClassification(Enum):
    """Data classification levels."""
    PUBLIC = "public"               # Public information
    INTERNAL = "internal"           # Internal use only
    CONFIDENTIAL = "confidential"   # Confidential data
    RESTRICTED = "restricted"       # Restricted access
    TOP_SECRET = "top_secret"       # Top secret/critical


class AvailabilityRequirement(Enum):
    """Availability requirement levels."""
    STANDARD = "standard"       # Standard availability (99%)
    IMPORTANT = "important"     # High availability (99.9%)
    ESSENTIAL = "essential"     # Very high availability (99.99%)
    CRITICAL = "critical"       # Mission-critical (99.999%)


class CriticalityLevel(Enum):
    """Asset criticality levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    MISSION_CRITICAL = "mission_critical"


class AttackSurfaceArea(Enum):
    """Attack surface area classification."""
    MINIMAL = "minimal"       # Very limited exposure
    LIMITED = "limited"       # Limited exposure
    MODERATE = "moderate"     # Moderate exposure
    EXTENSIVE = "extensive"   # Extensive exposure
    CRITICAL = "critical"     # Critical exposure level


class AggregationType(Enum):
    """Types of risk aggregation groupings."""
    VENDOR = "vendor"
    SECTOR = "sector"
    ASSET_TYPE = "asset_type"
    DEPARTMENT = "department"


# =============================================================================
# Core Data Models
# =============================================================================


@dataclass
class RiskFactor:
    """
    Individual risk factor contributing to overall risk score.

    Represents a single factor (vulnerability, threat, exposure) that
    contributes to an entity's overall risk calculation.
    """
    factor_id: str
    factor_type: RiskFactorType
    name: str
    description: str

    # Scoring
    weight: float  # 0.0-1.0 importance weight
    score: float   # 0.0-10.0 factor score

    # Evidence and remediation
    evidence: List[str] = field(default_factory=list)  # Supporting evidence/data
    remediation_available: bool = False

    def __post_init__(self):
        """Validate risk factor data."""
        if not self.factor_id or not self.factor_id.strip():
            raise ValueError("factor_id is required")
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError("weight must be between 0.0 and 1.0")
        if not 0.0 <= self.score <= 10.0:
            raise ValueError("score must be between 0.0 and 10.0")

        self.factor_id = self.factor_id.strip()
        self.name = self.name.strip() if self.name else ""
        self.description = self.description.strip() if self.description else ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "factor_id": self.factor_id,
            "factor_type": self.factor_type.value,
            "name": self.name,
            "description": self.description,
            "weight": self.weight,
            "score": self.score,
            "evidence": self.evidence,
            "remediation_available": self.remediation_available,
        }


@dataclass
class RiskScore:
    """
    Multi-factor risk calculation for entities.

    Represents comprehensive risk assessment combining vulnerability,
    threat, exposure, and asset criticality factors.
    """
    risk_score_id: str
    customer_id: str  # For multi-tenant isolation
    entity_type: str  # 'asset', 'vendor', 'network', 'application'
    entity_id: str
    entity_name: str

    # Overall risk scoring
    overall_score: float  # 0.0-10.0 composite risk score
    risk_level: RiskLevel = RiskLevel.LOW

    # Component risk scores (0.0-10.0 each)
    vulnerability_score: float = 0.0
    threat_score: float = 0.0
    exposure_score: float = 0.0
    asset_score: float = 0.0  # Asset criticality contribution

    # Calculation metadata
    calculation_date: datetime = field(default_factory=datetime.utcnow)
    confidence: float = 0.0  # 0.0-1.0 confidence in calculation

    # Contributing factors
    contributing_factors: List[RiskFactor] = field(default_factory=list)

    # Trend analysis
    trend: RiskTrend = RiskTrend.STABLE
    previous_score: Optional[float] = None
    score_change: float = 0.0  # Change from previous score

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate risk score data."""
        if not self.risk_score_id or not self.risk_score_id.strip():
            raise ValueError("risk_score_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.entity_id or not self.entity_id.strip():
            raise ValueError("entity_id is required")
        if not 0.0 <= self.overall_score <= 10.0:
            raise ValueError("overall_score must be between 0.0 and 10.0")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")

        # Normalize values
        self.risk_score_id = self.risk_score_id.strip()
        self.customer_id = self.customer_id.strip()
        self.entity_id = self.entity_id.strip()
        self.entity_name = self.entity_name.strip() if self.entity_name else ""

        # Calculate risk level from score
        self.risk_level = self._calculate_risk_level()

        # Calculate trend if previous score available
        if self.previous_score is not None:
            self.score_change = self.overall_score - self.previous_score
            self.trend = self._calculate_trend()

    def _calculate_risk_level(self) -> RiskLevel:
        """Calculate risk level from overall score."""
        if self.overall_score <= 2.5:
            return RiskLevel.LOW
        elif self.overall_score <= 5.0:
            return RiskLevel.MEDIUM
        elif self.overall_score <= 7.5:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL

    def _calculate_trend(self) -> RiskTrend:
        """Calculate trend from score change."""
        if self.score_change < -0.5:
            return RiskTrend.IMPROVING
        elif self.score_change > 0.5:
            return RiskTrend.DEGRADING
        else:
            return RiskTrend.STABLE

    @property
    def is_critical(self) -> bool:
        """Check if risk level is critical."""
        return self.risk_level == RiskLevel.CRITICAL

    @property
    def is_high_risk(self) -> bool:
        """Check if risk is high or critical."""
        return self.risk_level in {RiskLevel.HIGH, RiskLevel.CRITICAL}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "risk_score_id": self.risk_score_id,
            "customer_id": self.customer_id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "entity_name": self.entity_name,
            "overall_score": self.overall_score,
            "risk_level": self.risk_level.value,
            "vulnerability_score": self.vulnerability_score,
            "threat_score": self.threat_score,
            "exposure_score": self.exposure_score,
            "asset_score": self.asset_score,
            "calculation_date": self.calculation_date.isoformat(),
            "confidence": self.confidence,
            "contributing_factors": [f.to_dict() for f in self.contributing_factors],
            "trend": self.trend.value,
            "previous_score": self.previous_score,
            "score_change": self.score_change,
            "is_critical": self.is_critical,
            "is_high_risk": self.is_high_risk,
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "risk_score_id": self.risk_score_id,
            "customer_id": self.customer_id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "entity_name": self.entity_name,
            "overall_score": self.overall_score,
            "risk_level": self.risk_level.value,
            "vulnerability_score": self.vulnerability_score,
            "threat_score": self.threat_score,
            "exposure_score": self.exposure_score,
            "asset_score": self.asset_score,
            "calculation_date": self.calculation_date.isoformat(),
            "confidence": self.confidence,
            "trend": self.trend.value,
            "score_change": self.score_change,
            "is_critical": self.is_critical,
            "is_high_risk": self.is_high_risk,
        }


@dataclass
class AssetCriticality:
    """
    Asset criticality assessment for risk calculation.

    Evaluates business criticality, data sensitivity, and availability
    requirements to determine asset importance in risk scoring.
    """
    asset_id: str
    customer_id: str  # For multi-tenant isolation
    asset_name: str
    asset_type: str  # 'server', 'network', 'application', 'database'

    # Criticality assessment
    criticality_level: CriticalityLevel = CriticalityLevel.MEDIUM
    criticality_score: float = 5.0  # 0.0-10.0

    # Business impact
    business_impact: BusinessImpact = BusinessImpact.MODERATE
    data_classification: DataClassification = DataClassification.INTERNAL
    availability_requirement: AvailabilityRequirement = AvailabilityRequirement.STANDARD

    # Dependencies
    dependencies: List[str] = field(default_factory=list)  # Asset IDs this depends on
    dependent_services: List[str] = field(default_factory=list)  # Services depending on this

    # Recovery objectives
    recovery_time_objective_hours: Optional[float] = None  # RTO in hours
    recovery_point_objective_hours: Optional[float] = None  # RPO in hours

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate asset criticality data."""
        if not self.asset_id or not self.asset_id.strip():
            raise ValueError("asset_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not 0.0 <= self.criticality_score <= 10.0:
            raise ValueError("criticality_score must be between 0.0 and 10.0")

        # Normalize values
        self.asset_id = self.asset_id.strip()
        self.customer_id = self.customer_id.strip()
        self.asset_name = self.asset_name.strip() if self.asset_name else ""

        # Calculate criticality level from score if needed
        if self.criticality_score >= 0:
            self.criticality_level = self._calculate_criticality_level()

    def _calculate_criticality_level(self) -> CriticalityLevel:
        """Calculate criticality level from score."""
        if self.criticality_score <= 2.0:
            return CriticalityLevel.LOW
        elif self.criticality_score <= 4.0:
            return CriticalityLevel.MEDIUM
        elif self.criticality_score <= 7.0:
            return CriticalityLevel.HIGH
        elif self.criticality_score <= 9.0:
            return CriticalityLevel.CRITICAL
        else:
            return CriticalityLevel.MISSION_CRITICAL

    @property
    def is_mission_critical(self) -> bool:
        """Check if asset is mission critical."""
        return self.criticality_level == CriticalityLevel.MISSION_CRITICAL

    @property
    def has_strict_rto(self) -> bool:
        """Check if asset has strict recovery time objective (<4 hours)."""
        return self.recovery_time_objective_hours is not None and self.recovery_time_objective_hours < 4.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "asset_id": self.asset_id,
            "customer_id": self.customer_id,
            "asset_name": self.asset_name,
            "asset_type": self.asset_type,
            "criticality_level": self.criticality_level.value,
            "criticality_score": self.criticality_score,
            "business_impact": self.business_impact.value,
            "data_classification": self.data_classification.value,
            "availability_requirement": self.availability_requirement.value,
            "dependencies": self.dependencies,
            "dependent_services": self.dependent_services,
            "recovery_time_objective_hours": self.recovery_time_objective_hours,
            "recovery_point_objective_hours": self.recovery_point_objective_hours,
            "is_mission_critical": self.is_mission_critical,
            "has_strict_rto": self.has_strict_rto,
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "asset_id": self.asset_id,
            "customer_id": self.customer_id,
            "asset_name": self.asset_name,
            "entity_type": "asset_criticality",
            "asset_type": self.asset_type,
            "criticality_level": self.criticality_level.value,
            "criticality_score": self.criticality_score,
            "business_impact": self.business_impact.value,
            "data_classification": self.data_classification.value,
            "availability_requirement": self.availability_requirement.value,
            "recovery_time_objective_hours": self.recovery_time_objective_hours,
            "is_mission_critical": self.is_mission_critical,
        }


@dataclass
class ExposureScore:
    """
    Attack surface exposure assessment.

    Evaluates external exposure, internet-facing services, open ports,
    and network positioning to determine exposure risk.
    """
    exposure_id: str
    customer_id: str  # For multi-tenant isolation
    asset_id: str
    asset_name: str

    # Exposure assessment
    external_exposure: bool = False  # Exposed to internet
    internet_facing: bool = False    # Directly internet-facing

    # Attack surface details
    open_ports: List[int] = field(default_factory=list)
    exposed_services: List[str] = field(default_factory=list)

    # Exposure scoring
    exposure_score: float = 0.0  # 0.0-10.0
    attack_surface_area: AttackSurfaceArea = AttackSurfaceArea.MINIMAL

    # Network context
    network_segment: Optional[str] = None  # 'dmz', 'internal', 'production', 'dev'
    security_controls: List[str] = field(default_factory=list)  # Firewalls, WAF, IPS, etc.

    # Scan metadata
    last_scan_date: Optional[datetime] = None
    scan_source: Optional[str] = None  # 'nmap', 'nessus', 'qualys', etc.

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate exposure score data."""
        if not self.exposure_id or not self.exposure_id.strip():
            raise ValueError("exposure_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.asset_id or not self.asset_id.strip():
            raise ValueError("asset_id is required")
        if not 0.0 <= self.exposure_score <= 10.0:
            raise ValueError("exposure_score must be between 0.0 and 10.0")

        # Normalize values
        self.exposure_id = self.exposure_id.strip()
        self.customer_id = self.customer_id.strip()
        self.asset_id = self.asset_id.strip()
        self.asset_name = self.asset_name.strip() if self.asset_name else ""

        # Calculate attack surface area from score
        self.attack_surface_area = self._calculate_attack_surface()

    def _calculate_attack_surface(self) -> AttackSurfaceArea:
        """Calculate attack surface area from exposure score."""
        if self.exposure_score <= 2.0:
            return AttackSurfaceArea.MINIMAL
        elif self.exposure_score <= 4.0:
            return AttackSurfaceArea.LIMITED
        elif self.exposure_score <= 6.0:
            return AttackSurfaceArea.MODERATE
        elif self.exposure_score <= 8.0:
            return AttackSurfaceArea.EXTENSIVE
        else:
            return AttackSurfaceArea.CRITICAL

    @property
    def is_high_exposure(self) -> bool:
        """Check if exposure is high or critical."""
        return self.attack_surface_area in {AttackSurfaceArea.EXTENSIVE, AttackSurfaceArea.CRITICAL}

    @property
    def open_port_count(self) -> int:
        """Get count of open ports."""
        return len(self.open_ports)

    @property
    def has_security_controls(self) -> bool:
        """Check if security controls are in place."""
        return len(self.security_controls) > 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "exposure_id": self.exposure_id,
            "customer_id": self.customer_id,
            "asset_id": self.asset_id,
            "asset_name": self.asset_name,
            "external_exposure": self.external_exposure,
            "internet_facing": self.internet_facing,
            "open_ports": self.open_ports,
            "exposed_services": self.exposed_services,
            "exposure_score": self.exposure_score,
            "attack_surface_area": self.attack_surface_area.value,
            "network_segment": self.network_segment,
            "security_controls": self.security_controls,
            "last_scan_date": self.last_scan_date.isoformat() if self.last_scan_date else None,
            "scan_source": self.scan_source,
            "is_high_exposure": self.is_high_exposure,
            "open_port_count": self.open_port_count,
            "has_security_controls": self.has_security_controls,
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "exposure_id": self.exposure_id,
            "customer_id": self.customer_id,
            "asset_id": self.asset_id,
            "asset_name": self.asset_name,
            "entity_type": "exposure_score",
            "external_exposure": self.external_exposure,
            "internet_facing": self.internet_facing,
            "open_ports": self.open_ports,
            "exposed_services": self.exposed_services,
            "exposure_score": self.exposure_score,
            "attack_surface_area": self.attack_surface_area.value,
            "network_segment": self.network_segment,
            "security_controls": self.security_controls,
            "last_scan_date": self.last_scan_date.isoformat() if self.last_scan_date else None,
            "is_high_exposure": self.is_high_exposure,
        }


@dataclass
class RiskAggregation:
    """
    Aggregated risk assessment for groups of entities.

    Provides rollup risk metrics for vendors, sectors, asset types,
    or departments for portfolio-level risk management.
    """
    aggregation_id: str
    customer_id: str  # For multi-tenant isolation
    aggregation_type: AggregationType
    group_name: str
    group_id: str

    # Aggregated scores
    average_risk_score: float = 0.0  # Mean risk score
    max_risk_score: float = 0.0      # Highest risk in group
    min_risk_score: float = 0.0      # Lowest risk in group

    # Entity counts
    entity_count: int = 0
    high_risk_count: int = 0      # High or critical risk
    critical_count: int = 0       # Critical risk only

    # Risk distribution
    risk_distribution: Dict[str, int] = field(default_factory=dict)  # {level: count}

    # Trend
    trend: RiskTrend = RiskTrend.STABLE

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate risk aggregation data."""
        if not self.aggregation_id or not self.aggregation_id.strip():
            raise ValueError("aggregation_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.group_id or not self.group_id.strip():
            raise ValueError("group_id is required")

        # Normalize values
        self.aggregation_id = self.aggregation_id.strip()
        self.customer_id = self.customer_id.strip()
        self.group_id = self.group_id.strip()
        self.group_name = self.group_name.strip() if self.group_name else ""

    @property
    def high_risk_percentage(self) -> float:
        """Calculate percentage of high-risk entities."""
        if self.entity_count == 0:
            return 0.0
        return (self.high_risk_count / self.entity_count) * 100

    @property
    def critical_percentage(self) -> float:
        """Calculate percentage of critical entities."""
        if self.entity_count == 0:
            return 0.0
        return (self.critical_count / self.entity_count) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "aggregation_id": self.aggregation_id,
            "customer_id": self.customer_id,
            "aggregation_type": self.aggregation_type.value,
            "group_name": self.group_name,
            "group_id": self.group_id,
            "average_risk_score": self.average_risk_score,
            "max_risk_score": self.max_risk_score,
            "min_risk_score": self.min_risk_score,
            "entity_count": self.entity_count,
            "high_risk_count": self.high_risk_count,
            "critical_count": self.critical_count,
            "risk_distribution": self.risk_distribution,
            "trend": self.trend.value,
            "high_risk_percentage": self.high_risk_percentage,
            "critical_percentage": self.critical_percentage,
        }
