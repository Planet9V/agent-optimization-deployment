"""
E10 Economic Impact Schemas
Data models for economic calculations, ROI analysis, and impact modeling
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Literal, Tuple
from datetime import datetime
from enum import Enum


class CostCategory(str, Enum):
    """Cost categorization types"""
    EQUIPMENT = "equipment"
    PERSONNEL = "personnel"
    DOWNTIME = "downtime"
    REMEDIATION = "remediation"
    COMPLIANCE = "compliance"
    INSURANCE = "insurance"
    TRAINING = "training"
    MAINTENANCE = "maintenance"


class InvestmentCategory(str, Enum):
    """Investment types for ROI calculation"""
    SECURITY_TOOLS = "security_tools"
    INFRASTRUCTURE = "infrastructure"
    PERSONNEL = "personnel"
    TRAINING = "training"
    CONSULTING = "consulting"
    COMPLIANCE = "compliance"
    INSURANCE = "insurance"


class ScenarioType(str, Enum):
    """Impact scenario types"""
    RANSOMWARE = "ransomware"
    DATA_BREACH = "data_breach"
    SYSTEM_OUTAGE = "system_outage"
    SUPPLY_CHAIN = "supply_chain"
    INSIDER_THREAT = "insider_threat"
    DDOS_ATTACK = "ddos_attack"


class Currency(str, Enum):
    """Supported currencies"""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"


# ============================================================================
# Cost Analysis Schemas
# ============================================================================

class CostBreakdownItem(BaseModel):
    """Individual cost item"""
    category: CostCategory
    description: str
    amount: float
    currency: Currency = Currency.USD
    date: datetime
    recurring: bool = False
    frequency: Optional[str] = None  # "monthly", "annual", etc.


class CostSummary(BaseModel):
    """Overall cost summary"""
    customer_id: str
    total_costs: float
    cost_categories: Dict[CostCategory, float]
    period_start: datetime
    period_end: datetime
    currency: Currency = Currency.USD
    trend_percentage: Optional[float] = None


class CostByCategory(BaseModel):
    """Costs grouped by category"""
    customer_id: str
    category: CostCategory
    total_amount: float
    item_count: int
    average_cost: float
    items: List[CostBreakdownItem]
    currency: Currency = Currency.USD


class EntityCostBreakdown(BaseModel):
    """Detailed cost breakdown for specific entity"""
    entity_id: str
    entity_type: str  # asset, process, system, etc.
    total_cost: float
    direct_costs: List[CostBreakdownItem]
    indirect_costs: List[CostBreakdownItem]
    allocated_overhead: float
    currency: Currency = Currency.USD


class CostCalculationRequest(BaseModel):
    """Request for cost calculation"""
    customer_id: str
    scenario_type: str
    duration_hours: float
    affected_systems: List[str]
    personnel_count: int
    equipment_value: float
    revenue_per_hour: Optional[float] = None
    additional_factors: Optional[Dict[str, float]] = None


class HistoricalCostTrend(BaseModel):
    """Historical cost trends"""
    customer_id: str
    data_points: List[Tuple[datetime, float]]
    category: Optional[CostCategory] = None
    trend_direction: Literal["increasing", "decreasing", "stable"]
    percentage_change: float
    currency: Currency = Currency.USD


# ============================================================================
# ROI Calculation Schemas
# ============================================================================

class ROICalculation(BaseModel):
    """ROI calculation results"""
    investment_id: str
    customer_id: str
    investment_name: str
    category: InvestmentCategory
    initial_investment: float
    annual_savings: float
    annual_costs: float
    roi_percentage: float
    payback_period_months: float
    npv: float  # Net Present Value
    irr: float  # Internal Rate of Return
    calculation_date: datetime
    currency: Currency = Currency.USD


class ROICalculationRequest(BaseModel):
    """Request for ROI calculation"""
    customer_id: str
    investment_name: str
    category: InvestmentCategory
    initial_investment: float
    expected_annual_savings: float
    annual_operating_costs: float
    project_lifetime_years: int = 5
    discount_rate: float = 0.10
    currency: Currency = Currency.USD


class ROISummary(BaseModel):
    """Summary of all ROI calculations"""
    customer_id: str
    total_investments: int
    total_invested: float
    total_annual_savings: float
    average_roi_percentage: float
    best_performing: Optional[ROICalculation] = None
    worst_performing: Optional[ROICalculation] = None
    by_category: Dict[InvestmentCategory, float]
    currency: Currency = Currency.USD


class ROIProjection(BaseModel):
    """Future ROI projections"""
    investment_id: str
    customer_id: str
    projections: List[Tuple[int, float]]  # (year, projected_value)
    confidence_interval_low: List[float]
    confidence_interval_high: List[float]
    assumptions: Dict[str, str]


class InvestmentComparison(BaseModel):
    """Comparison between multiple investments"""
    customer_id: str
    investments: List[ROICalculation]
    comparison_metrics: Dict[str, List[float]]
    recommendation: str
    ranking: List[str]  # investment_ids in ranked order


# ============================================================================
# Business Value Schemas
# ============================================================================

class BusinessValue(BaseModel):
    """Business value assessment"""
    entity_id: str
    entity_type: str
    customer_id: str
    replacement_cost: float
    revenue_impact: float
    reputation_value: float
    regulatory_exposure: float
    intellectual_property_value: float
    operational_criticality: float
    total_value: float
    confidence_score: float
    assessment_date: datetime
    currency: Currency = Currency.USD


class ValueMetrics(BaseModel):
    """Business value metrics dashboard"""
    customer_id: str
    total_asset_value: float
    critical_asset_count: int
    at_risk_value: float
    protected_value: float
    value_by_category: Dict[str, float]
    top_value_assets: List[BusinessValue]
    currency: Currency = Currency.USD


class ValueCalculationRequest(BaseModel):
    """Request for business value calculation"""
    customer_id: str
    entity_id: str
    entity_type: str
    replacement_cost: Optional[float] = None
    annual_revenue: Optional[float] = None
    market_share: Optional[float] = None
    customer_base: Optional[int] = None
    regulatory_requirements: List[str] = []
    ip_patents: int = 0
    operational_hours: float = 8760  # 24/7 by default


class RiskAdjustedValue(BaseModel):
    """Risk-adjusted business value"""
    entity_id: str
    customer_id: str
    nominal_value: float
    risk_score: float
    risk_adjusted_value: float
    expected_loss: float
    value_at_risk: float
    confidence_level: float
    currency: Currency = Currency.USD


class ValueBySector(BaseModel):
    """Value metrics by industry sector"""
    customer_id: str
    sector: str
    total_value: float
    asset_count: int
    average_value: float
    risk_level: str
    benchmark_comparison: float
    currency: Currency = Currency.USD


# ============================================================================
# Impact Modeling Schemas
# ============================================================================

class ScenarioParameters(BaseModel):
    """Parameters for impact scenario"""
    affected_systems: List[str]
    duration_hours: float
    severity: Literal["low", "medium", "high", "critical"]
    data_volume_gb: Optional[float] = None
    user_count: Optional[int] = None
    geographic_scope: Optional[str] = None
    regulatory_implications: List[str] = []


class ImpactScenario(BaseModel):
    """Impact scenario definition"""
    scenario_id: str
    customer_id: str
    scenario_type: ScenarioType
    scenario_name: str
    description: str
    parameters: ScenarioParameters
    estimated_cost: float
    confidence_interval: Tuple[float, float]
    probability: float
    created_date: datetime
    currency: Currency = Currency.USD


class ImpactModelRequest(BaseModel):
    """Request to model financial impact"""
    customer_id: str
    scenario_type: ScenarioType
    parameters: ScenarioParameters
    include_indirect_costs: bool = True
    include_reputation_impact: bool = True
    time_horizon_days: int = 365


class ImpactSimulation(BaseModel):
    """Impact simulation results"""
    simulation_id: str
    customer_id: str
    scenario: ImpactScenario
    direct_costs: float
    indirect_costs: float
    opportunity_costs: float
    reputation_impact: float
    regulatory_fines: float
    total_impact: float
    recovery_timeline_days: int
    mitigation_recommendations: List[str]
    currency: Currency = Currency.USD


class HistoricalImpact(BaseModel):
    """Historical impact data"""
    customer_id: str
    incident_date: datetime
    scenario_type: ScenarioType
    actual_cost: float
    estimated_cost: float
    variance_percentage: float
    lessons_learned: List[str]
    currency: Currency = Currency.USD


# ============================================================================
# Dashboard Schemas
# ============================================================================

class EconomicDashboard(BaseModel):
    """Economic dashboard summary"""
    customer_id: str
    timestamp: datetime
    total_costs_ytd: float
    total_investments_ytd: float
    average_roi: float
    at_risk_value: float
    cost_trend: str
    roi_trend: str
    alerts: List[str]
    key_metrics: Dict[str, float]
    currency: Currency = Currency.USD


class EconomicTrends(BaseModel):
    """Economic trends over time"""
    customer_id: str
    period: str
    cost_trend: List[Tuple[datetime, float]]
    roi_trend: List[Tuple[datetime, float]]
    value_trend: List[Tuple[datetime, float]]
    incident_impact_trend: List[Tuple[datetime, float]]
    currency: Currency = Currency.USD


class EconomicKPIs(BaseModel):
    """Key performance indicators"""
    customer_id: str
    security_investment_percentage: float
    roi_average: float
    cost_per_asset: float
    value_protected_ratio: float
    incident_cost_trend: float
    payback_period_average: float
    budget_utilization: float


class EconomicAlert(BaseModel):
    """Economic alert"""
    alert_id: str
    customer_id: str
    alert_type: str
    severity: Literal["info", "warning", "critical"]
    message: str
    threshold_value: float
    current_value: float
    created_date: datetime
    acknowledged: bool = False


class ExecutiveSummary(BaseModel):
    """Executive summary view"""
    customer_id: str
    period: str
    total_security_spend: float
    total_value_protected: float
    roi_on_security: float
    incidents_prevented: int
    cost_avoidance: float
    top_risks: List[str]
    investment_recommendations: List[str]
    executive_insights: str
    currency: Currency = Currency.USD


# ============================================================================
# Integration Schemas (E08, E03, E15)
# ============================================================================

class RAMSIntegration(BaseModel):
    """Integration with E08 RAMS"""
    entity_id: str
    customer_id: str
    reliability_score: float
    availability_score: float
    maintainability_score: float
    safety_score: float
    economic_impact_factor: float
    failure_cost: float


class SBOMIntegration(BaseModel):
    """Integration with E03 SBOM"""
    component_id: str
    customer_id: str
    component_name: str
    vulnerability_count: int
    remediation_cost: float
    replacement_cost: float
    business_impact: float


class VendorEquipmentIntegration(BaseModel):
    """Integration with E15 Vendor Equipment"""
    equipment_id: str
    customer_id: str
    vendor_name: str
    equipment_value: float
    maintenance_cost_annual: float
    replacement_timeline_years: int
    criticality_score: float
    business_value: float


# ============================================================================
# Response Schemas
# ============================================================================

class EconomicImpactResponse(BaseModel):
    """Standard API response"""
    success: bool
    data: Optional[Dict] = None
    message: Optional[str] = None
    errors: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
