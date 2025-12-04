"""
Demographics Baseline Data Models
==================================

Pydantic models and dataclasses for E11 Psychohistory Demographics.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ===== Enums =====

class CriticalityLevel(str, Enum):
    """Organization unit criticality."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TurnoverRisk(str, Enum):
    """Employee turnover risk levels."""
    MINIMAL = "minimal"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class SkillCategory(str, Enum):
    """Skill classification categories."""
    TECHNICAL = "technical"
    SECURITY = "security"
    MANAGEMENT = "management"
    OPERATIONAL = "operational"
    ANALYTICAL = "analytical"
    SPECIALIZED = "specialized"


# ===== Dataclasses for Domain Models =====

@dataclass
class PopulationSegment:
    """Population demographic segment."""
    segment_id: str
    name: str
    count: int
    percentage: float
    characteristics: Dict[str, Any]


@dataclass
class DemographicDistribution:
    """Distribution of demographic characteristics."""
    by_age_group: Dict[str, int]
    by_tenure: Dict[str, int]
    by_education: Dict[str, int]
    by_department: Dict[str, int]


@dataclass
class BaselineMetrics:
    """Psychohistory baseline metrics."""
    population_stability_index: float  # 0-1, higher is more stable
    role_diversity_score: float  # 0-1, measures role distribution
    skill_concentration_risk: float  # 0-1, higher is riskier
    succession_coverage: float  # 0-1, percentage with succession plans
    insider_threat_baseline: float  # 0-10, baseline threat level

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            "population_stability_index": self.population_stability_index,
            "role_diversity_score": self.role_diversity_score,
            "skill_concentration_risk": self.skill_concentration_risk,
            "succession_coverage": self.succession_coverage,
            "insider_threat_baseline": self.insider_threat_baseline,
        }


@dataclass
class RoleBreakdown:
    """Role breakdown statistics."""
    role_id: str
    role_name: str
    count: int
    percentage: float
    security_relevant: bool
    criticality: CriticalityLevel


@dataclass
class DepartmentBreakdown:
    """Department breakdown statistics."""
    department_id: str
    department_name: str
    count: int
    percentage: float
    turnover_rate: float


@dataclass
class SkillDistribution:
    """Skill distribution across workforce."""
    category: SkillCategory
    skill_name: str
    employee_count: int
    proficiency_avg: float
    criticality: CriticalityLevel


@dataclass
class PopulationProfile:
    """Complete population demographic profile."""
    customer_id: str
    total_population: int
    segments: List[PopulationSegment]
    distribution: DemographicDistribution
    baseline_metrics: BaselineMetrics
    generated_at: datetime

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant payload."""
        return {
            "record_type": "population_profile",
            "customer_id": self.customer_id,
            "total_population": self.total_population,
            "segments": [
                {
                    "segment_id": s.segment_id,
                    "name": s.name,
                    "count": s.count,
                    "percentage": s.percentage,
                    "characteristics": s.characteristics,
                }
                for s in self.segments
            ],
            "distribution": {
                "by_age_group": self.distribution.by_age_group,
                "by_tenure": self.distribution.by_tenure,
                "by_education": self.distribution.by_education,
                "by_department": self.distribution.by_department,
            },
            "baseline_metrics": self.baseline_metrics.to_dict(),
            "generated_at": self.generated_at.isoformat(),
        }


@dataclass
class WorkforceComposition:
    """Workforce composition and analytics."""
    org_unit_id: str
    org_unit_name: str
    customer_id: str
    total_employees: int
    by_role: List[RoleBreakdown]
    by_department: List[DepartmentBreakdown]
    skill_distribution: List[SkillDistribution]
    turnover_rate: float
    generated_at: datetime

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant payload."""
        return {
            "record_type": "workforce_composition",
            "org_unit_id": self.org_unit_id,
            "org_unit_name": self.org_unit_name,
            "customer_id": self.customer_id,
            "total_employees": self.total_employees,
            "by_role": [
                {
                    "role_id": r.role_id,
                    "role_name": r.role_name,
                    "count": r.count,
                    "percentage": r.percentage,
                    "security_relevant": r.security_relevant,
                    "criticality": r.criticality.value,
                }
                for r in self.by_role
            ],
            "by_department": [
                {
                    "department_id": d.department_id,
                    "department_name": d.department_name,
                    "count": d.count,
                    "percentage": d.percentage,
                    "turnover_rate": d.turnover_rate,
                }
                for d in self.by_department
            ],
            "skill_distribution": [
                {
                    "category": s.category.value,
                    "skill_name": s.skill_name,
                    "employee_count": s.employee_count,
                    "proficiency_avg": s.proficiency_avg,
                    "criticality": s.criticality.value,
                }
                for s in self.skill_distribution
            ],
            "turnover_rate": self.turnover_rate,
            "generated_at": self.generated_at.isoformat(),
        }


@dataclass
class OrganizationUnit:
    """Organization unit with demographics."""
    unit_id: str
    name: str
    customer_id: str
    parent_id: Optional[str]
    level: int
    employee_count: int
    criticality: CriticalityLevel
    security_roles_count: int
    children: List[str]

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant payload."""
        return {
            "record_type": "organization_unit",
            "unit_id": self.unit_id,
            "name": self.name,
            "customer_id": self.customer_id,
            "parent_id": self.parent_id,
            "level": self.level,
            "employee_count": self.employee_count,
            "criticality": self.criticality.value,
            "security_roles_count": self.security_roles_count,
            "children": self.children,
        }


# ===== API Request/Response Models =====

class PopulationSummaryResponse(BaseModel):
    """Response for population summary."""
    customer_id: str
    total_population: int
    active_employees: int
    contractors: int
    growth_rate_30d: float
    stability_index: float


class PopulationDistributionResponse(BaseModel):
    """Response for population distribution."""
    customer_id: str
    distribution: Dict[str, Dict[str, int]]
    generated_at: str


class PopulationTrendsResponse(BaseModel):
    """Response for population trends."""
    customer_id: str
    trends: List[Dict[str, Any]]
    forecast_90d: Dict[str, int]


class PopulationQueryRequest(BaseModel):
    """Request for custom population query."""
    filters: Dict[str, Any] = Field(..., description="Query filters")
    group_by: Optional[str] = Field(None, description="Grouping field")
    aggregations: Optional[List[str]] = Field(None, description="Aggregation functions")


class WorkforceCompositionResponse(BaseModel):
    """Response for workforce composition."""
    org_unit_id: str
    org_unit_name: str
    customer_id: str
    total_employees: int
    by_role: List[Dict[str, Any]]
    by_department: List[Dict[str, Any]]
    turnover_rate: float


class SkillsInventoryResponse(BaseModel):
    """Response for skills inventory."""
    customer_id: str
    total_skills: int
    by_category: Dict[str, int]
    critical_skills: List[Dict[str, Any]]
    skill_gaps: List[Dict[str, Any]]


class TurnoverMetricsResponse(BaseModel):
    """Response for turnover metrics."""
    customer_id: str
    current_turnover_rate: float
    predicted_turnover_30d: float
    high_risk_employees: int
    retention_score: float


class TeamProfileResponse(BaseModel):
    """Response for team demographic profile."""
    team_id: str
    team_name: str
    customer_id: str
    member_count: int
    demographics: Dict[str, Any]
    cohesion_score: float
    diversity_index: float


class CapacityMetricsResponse(BaseModel):
    """Response for capacity metrics."""
    customer_id: str
    total_capacity_hours: int
    utilized_capacity: float
    available_capacity: float
    overutilized_teams: List[str]


class OrganizationHierarchyResponse(BaseModel):
    """Response for organization hierarchy."""
    customer_id: str
    root_units: List[Dict[str, Any]]
    total_units: int
    max_depth: int


class OrganizationUnitsResponse(BaseModel):
    """Response for listing organization units."""
    customer_id: str
    units: List[Dict[str, Any]]
    total: int


class UnitDetailsResponse(BaseModel):
    """Response for unit details."""
    unit_id: str
    name: str
    customer_id: str
    parent_id: Optional[str]
    level: int
    employee_count: int
    criticality: str
    security_roles_count: int
    demographics: Dict[str, Any]


class OrganizationRelationshipsResponse(BaseModel):
    """Response for inter-unit relationships."""
    customer_id: str
    relationships: List[Dict[str, Any]]
    total: int


class OrganizationAnalysisRequest(BaseModel):
    """Request for organization structure analysis."""
    analysis_type: str = Field(..., description="Type of analysis")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Analysis parameters")


class RoleDistributionResponse(BaseModel):
    """Response for role distribution."""
    customer_id: str
    total_roles: int
    by_category: Dict[str, int]
    security_relevant_roles: int
    roles: List[Dict[str, Any]]


class RoleDemographicsResponse(BaseModel):
    """Response for role-specific demographics."""
    role_id: str
    role_name: str
    customer_id: str
    employee_count: int
    demographics: Dict[str, Any]
    turnover_rate: float


class SecurityRolesResponse(BaseModel):
    """Response for security-relevant roles."""
    customer_id: str
    total_security_roles: int
    roles: List[Dict[str, Any]]
    coverage_score: float


class AccessPatternsResponse(BaseModel):
    """Response for role-based access patterns."""
    customer_id: str
    patterns: List[Dict[str, Any]]
    anomalies: List[Dict[str, Any]]


class DashboardSummaryResponse(BaseModel):
    """Response for demographics dashboard."""
    customer_id: str
    population_summary: Dict[str, Any]
    workforce_summary: Dict[str, Any]
    organization_summary: Dict[str, Any]
    generated_at: str


class BaselineMetricsResponse(BaseModel):
    """Response for psychohistory baseline metrics."""
    customer_id: str
    population_stability_index: float
    role_diversity_score: float
    skill_concentration_risk: float
    succession_coverage: float
    insider_threat_baseline: float
    generated_at: str


class DemographicIndicatorsResponse(BaseModel):
    """Response for key demographic indicators."""
    customer_id: str
    indicators: List[Dict[str, Any]]
    warnings: List[str]


class DemographicAlertsResponse(BaseModel):
    """Response for demographic alerts."""
    customer_id: str
    alerts: List[Dict[str, Any]]
    total: int


class TrendAnalysisResponse(BaseModel):
    """Response for trend analysis."""
    customer_id: str
    trends: List[Dict[str, Any]]
    forecast: Dict[str, Any]
