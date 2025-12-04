"""
E11 Psychohistory Demographics Baseline API Router
===================================================

FastAPI router for demographics baseline with 24 endpoints.
Provides population analytics, workforce modeling, and organization structure analysis.

Version: 1.0.0
Created: 2025-12-04
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Header, Depends
from pydantic import BaseModel, Field
import logging

from ..customer_isolation import (
    CustomerContext,
    CustomerContextManager,
    CustomerAccessLevel,
)
from .service import DemographicsService
from .schemas import (
    PopulationSummaryResponse,
    PopulationDistributionResponse,
    PopulationTrendsResponse,
    PopulationQueryRequest,
    WorkforceCompositionResponse,
    SkillsInventoryResponse,
    TurnoverMetricsResponse,
    TeamProfileResponse,
    CapacityMetricsResponse,
    OrganizationHierarchyResponse,
    OrganizationUnitsResponse,
    UnitDetailsResponse,
    OrganizationRelationshipsResponse,
    OrganizationAnalysisRequest,
    RoleDistributionResponse,
    RoleDemographicsResponse,
    SecurityRolesResponse,
    AccessPatternsResponse,
    DashboardSummaryResponse,
    BaselineMetricsResponse,
    DemographicIndicatorsResponse,
    DemographicAlertsResponse,
    TrendAnalysisResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/demographics", tags=["demographics-baseline"])


# ===== Dependencies =====

def get_service() -> DemographicsService:
    """Get demographics service instance."""
    return DemographicsService()


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


# ===== Population Metrics Endpoints (5) =====

@router.get("/population/summary", response_model=PopulationSummaryResponse)
async def get_population_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/population/summary

    Get population demographics summary.

    Returns total population, active employees, contractors, growth rate,
    and stability index.
    """
    try:
        summary = service.get_population_summary()
        return PopulationSummaryResponse(**summary)
    except Exception as e:
        logger.error(f"Error getting population summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/population/distribution", response_model=PopulationDistributionResponse)
async def get_population_distribution(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/population/distribution

    Get population distribution by category.

    Returns distribution by age group, tenure, education, and department.
    """
    try:
        distribution = service.get_population_distribution()
        return PopulationDistributionResponse(**distribution)
    except Exception as e:
        logger.error(f"Error getting population distribution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/population/{org_unit_id}/profile")
async def get_org_unit_population_profile(
    org_unit_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/population/{org_unit_id}/profile

    Get organization unit population profile.

    Returns demographic profile for specific organizational unit.
    """
    try:
        profile = service.get_org_unit_profile(org_unit_id)
        return profile
    except Exception as e:
        logger.error(f"Error getting org unit profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/population/trends", response_model=PopulationTrendsResponse)
async def get_population_trends(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/population/trends

    Get population trend analysis.

    Returns historical trends and 90-day forecast.
    """
    try:
        trends = service.get_population_trends()
        return PopulationTrendsResponse(**trends)
    except Exception as e:
        logger.error(f"Error getting population trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/population/query")
async def query_population(
    request: PopulationQueryRequest,
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    POST /api/v2/demographics/population/query

    Execute custom population query.

    Supports filters, grouping, and aggregations for flexible querying.
    """
    try:
        if not context.can_write():
            raise PermissionError("Write access required for custom queries")

        results = service.query_population(request.filters)
        return results
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing population query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Workforce Analytics Endpoints (5) =====

@router.get("/workforce/composition", response_model=WorkforceCompositionResponse)
async def get_workforce_composition(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/workforce/composition

    Get workforce composition breakdown.

    Returns composition by role, department, and turnover metrics.
    """
    try:
        composition = service.get_workforce_composition()
        return WorkforceCompositionResponse(**composition)
    except Exception as e:
        logger.error(f"Error getting workforce composition: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workforce/skills", response_model=SkillsInventoryResponse)
async def get_skills_inventory(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/workforce/skills

    Get skills inventory and distribution.

    Returns skills by category, critical skills, and skill gaps.
    """
    try:
        skills = service.get_skills_inventory()
        return SkillsInventoryResponse(**skills)
    except Exception as e:
        logger.error(f"Error getting skills inventory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workforce/turnover", response_model=TurnoverMetricsResponse)
async def get_turnover_metrics(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/workforce/turnover

    Get turnover metrics and predictions.

    Returns current turnover rate, predictions, and high-risk employees.
    """
    try:
        metrics = service.get_turnover_metrics()
        return TurnoverMetricsResponse(**metrics)
    except Exception as e:
        logger.error(f"Error getting turnover metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workforce/{team_id}/profile", response_model=TeamProfileResponse)
async def get_team_profile(
    team_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/workforce/{team_id}/profile

    Get team demographic profile.

    Returns team demographics, cohesion score, and diversity index.
    """
    try:
        profile = service.get_team_profile(team_id)
        return TeamProfileResponse(**profile)
    except Exception as e:
        logger.error(f"Error getting team profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workforce/capacity", response_model=CapacityMetricsResponse)
async def get_capacity_metrics(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/workforce/capacity

    Get capacity and utilization metrics.

    Returns total capacity, utilization, and overutilized teams.
    """
    try:
        metrics = service.get_capacity_metrics()
        return CapacityMetricsResponse(**metrics)
    except Exception as e:
        logger.error(f"Error getting capacity metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Organization Structure Endpoints (5) =====

@router.get("/organization/hierarchy", response_model=OrganizationHierarchyResponse)
async def get_organization_hierarchy(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/organization/hierarchy

    Get organization hierarchy map.

    Returns complete organizational structure with units and relationships.
    """
    try:
        hierarchy = service.get_organization_hierarchy()
        return OrganizationHierarchyResponse(**hierarchy)
    except Exception as e:
        logger.error(f"Error getting organization hierarchy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/organization/units", response_model=OrganizationUnitsResponse)
async def list_organization_units(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/organization/units

    List all organizational units.

    Returns all units with basic information and employee counts.
    """
    try:
        units = service.list_organization_units()
        return OrganizationUnitsResponse(**units)
    except Exception as e:
        logger.error(f"Error listing organization units: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/organization/{unit_id}/details", response_model=UnitDetailsResponse)
async def get_unit_details(
    unit_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/organization/{unit_id}/details

    Get organization unit details with demographics.

    Returns detailed unit information including demographics and criticality.
    """
    try:
        details = service.get_unit_details(unit_id)
        return UnitDetailsResponse(**details)
    except Exception as e:
        logger.error(f"Error getting unit details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/organization/relationships", response_model=OrganizationRelationshipsResponse)
async def get_organization_relationships(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/organization/relationships

    Get inter-unit relationships.

    Returns relationships between organizational units.
    """
    try:
        relationships = service.get_organization_relationships()
        return OrganizationRelationshipsResponse(**relationships)
    except Exception as e:
        logger.error(f"Error getting organization relationships: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/organization/analyze")
async def analyze_organization_structure(
    request: OrganizationAnalysisRequest,
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    POST /api/v2/demographics/organization/analyze

    Analyze organization structure.

    Supports various analysis types: span of control, depth analysis,
    bottleneck detection, communication efficiency.
    """
    try:
        if not context.can_write():
            raise PermissionError("Write access required for organization analysis")

        results = service.analyze_organization_structure(
            request.analysis_type,
            request.parameters,
        )
        return results
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Error analyzing organization structure: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Role Analysis Endpoints (4) =====

@router.get("/roles/distribution", response_model=RoleDistributionResponse)
async def get_role_distribution(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/roles/distribution

    Get role distribution across organization.

    Returns all roles with counts and security relevance.
    """
    try:
        distribution = service.get_role_distribution()
        return RoleDistributionResponse(**distribution)
    except Exception as e:
        logger.error(f"Error getting role distribution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/roles/{role_id}/demographics", response_model=RoleDemographicsResponse)
async def get_role_demographics(
    role_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/roles/{role_id}/demographics

    Get demographics for specific role.

    Returns demographic profile for employees in the specified role.
    """
    try:
        demographics = service.get_role_demographics(role_id)
        return RoleDemographicsResponse(**demographics)
    except Exception as e:
        logger.error(f"Error getting role demographics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/roles/security-relevant", response_model=SecurityRolesResponse)
async def get_security_relevant_roles(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/roles/security-relevant

    Get security-relevant roles analysis.

    Returns roles with security implications and coverage metrics.
    """
    try:
        roles = service.get_security_relevant_roles()
        return SecurityRolesResponse(**roles)
    except Exception as e:
        logger.error(f"Error getting security-relevant roles: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/roles/access-patterns", response_model=AccessPatternsResponse)
async def get_access_patterns(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/roles/access-patterns

    Get role-based access patterns.

    Returns normal access patterns and detected anomalies.
    """
    try:
        patterns = service.get_access_patterns()
        return AccessPatternsResponse(**patterns)
    except Exception as e:
        logger.error(f"Error getting access patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Dashboard Endpoints (5) =====

@router.get("/dashboard/summary", response_model=DashboardSummaryResponse)
async def get_dashboard_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/dashboard/summary

    Get demographics dashboard summary.

    Returns comprehensive dashboard with population, workforce, and
    organization summaries.
    """
    try:
        summary = service.get_dashboard_summary()
        return DashboardSummaryResponse(**summary)
    except Exception as e:
        logger.error(f"Error getting dashboard summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/baseline", response_model=BaselineMetricsResponse)
async def get_baseline_metrics(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/dashboard/baseline

    Get baseline metrics for psychohistory.

    Returns key metrics used for psychohistory calculations:
    - Population stability index
    - Role diversity score
    - Skill concentration risk
    - Succession coverage
    - Insider threat baseline
    """
    try:
        metrics = service.get_baseline_metrics()
        return BaselineMetricsResponse(**metrics)
    except Exception as e:
        logger.error(f"Error getting baseline metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/indicators", response_model=DemographicIndicatorsResponse)
async def get_demographic_indicators(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/dashboard/indicators

    Get key demographic indicators.

    Returns monitored indicators with thresholds and health status.
    """
    try:
        indicators = service.get_demographic_indicators()
        return DemographicIndicatorsResponse(**indicators)
    except Exception as e:
        logger.error(f"Error getting demographic indicators: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/alerts", response_model=DemographicAlertsResponse)
async def get_demographic_alerts(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/dashboard/alerts

    Get demographic alerts and anomalies.

    Returns active alerts for demographic concerns requiring attention.
    """
    try:
        alerts = service.get_demographic_alerts()
        return DemographicAlertsResponse(**alerts)
    except Exception as e:
        logger.error(f"Error getting demographic alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/trends", response_model=TrendAnalysisResponse)
async def get_trend_analysis(
    context: CustomerContext = Depends(require_customer_context),
    service: DemographicsService = Depends(get_service),
):
    """
    GET /api/v2/demographics/dashboard/trends

    Get demographic trend analysis.

    Returns trend analysis with forecasting for key demographic metrics.
    """
    try:
        trends = service.get_trend_analysis()
        return TrendAnalysisResponse(**trends)
    except Exception as e:
        logger.error(f"Error getting trend analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))
