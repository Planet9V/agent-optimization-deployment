"""
Risk Scoring Engine API Router
===============================

FastAPI router for E05: Risk Scoring Engine.
Provides REST endpoints for risk assessment operations.

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
from .risk_models import (
    RiskLevel,
    RiskFactorType,
    RiskTrend,
    CriticalityLevel,
    BusinessImpact,
    DataClassification,
    AvailabilityRequirement,
    AttackSurfaceArea,
    AggregationType,
)
from .risk_service import (
    RiskScoringService,
    RiskScoreRequest,
    RiskSearchRequest,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/risk", tags=["risk-scoring"])


# ===== Pydantic Models =====

class RiskFactorCreate(BaseModel):
    """Request model for risk factor."""
    factor_type: str = Field(..., description="Type of risk factor")
    value: float = Field(..., ge=0.0, le=10.0, description="Factor value 0-10")
    weight: float = Field(1.0, ge=0.0, le=1.0, description="Factor weight")
    description: Optional[str] = None


class RiskScoreCreate(BaseModel):
    """Request model for risk score calculation."""
    entity_type: str = Field(..., description="Entity type: asset, vulnerability, threat, vendor")
    entity_id: str = Field(..., description="Entity identifier")
    entity_name: str = Field(..., description="Entity name")
    factors: List[RiskFactorCreate] = Field(..., description="Risk factors")
    asset_criticality: Optional[float] = Field(None, ge=0.0, le=10.0)
    exposure_score: Optional[float] = Field(None, ge=0.0, le=10.0)


class RiskScoreResponse(BaseModel):
    """Response model for risk score."""
    risk_id: str
    entity_type: str
    entity_id: str
    entity_name: str
    customer_id: str
    risk_score: float
    risk_level: str
    factors: List[dict]
    calculated_at: str
    trend: Optional[str] = None


class RiskSearchResponse(BaseModel):
    """Response for risk search results."""
    total_results: int
    customer_id: str
    results: List[RiskScoreResponse]


class AssetCriticalityCreate(BaseModel):
    """Request model for asset criticality."""
    asset_id: str = Field(..., description="Asset identifier")
    asset_name: str = Field(..., description="Asset name")
    criticality_level: str = Field(..., description="Criticality level")
    criticality_score: float = Field(..., ge=0.0, le=10.0)
    business_impact: Optional[str] = None
    data_classification: Optional[str] = None
    availability_requirement: Optional[str] = None
    justification: Optional[str] = None


class AssetCriticalityResponse(BaseModel):
    """Response model for asset criticality."""
    asset_id: str
    asset_name: str
    customer_id: str
    criticality_level: str
    criticality_score: float
    business_impact: Optional[str]
    data_classification: Optional[str]
    availability_requirement: Optional[str]
    justification: Optional[str]


class AssetCriticalityListResponse(BaseModel):
    """Response for listing asset criticality."""
    total_results: int
    customer_id: str
    assets: List[AssetCriticalityResponse]


class CriticalitySummaryResponse(BaseModel):
    """Response for criticality distribution."""
    customer_id: str
    mission_critical: int
    high: int
    medium: int
    low: int
    informational: int
    total: int


class ExposureScoreCreate(BaseModel):
    """Request model for exposure score."""
    asset_id: str = Field(..., description="Asset identifier")
    asset_name: str = Field(..., description="Asset name")
    is_internet_facing: bool = Field(False, description="Internet facing")
    attack_surface: str = Field(..., description="Attack surface area")
    open_ports: List[int] = Field(default_factory=list)
    unpatched_vulnerabilities: int = Field(0, ge=0)
    network_exposure: Optional[str] = Field(None, description="public, dmz, internal, isolated")


class ExposureScoreResponse(BaseModel):
    """Response model for exposure score."""
    asset_id: str
    asset_name: str
    customer_id: str
    is_internet_facing: bool
    attack_surface: str
    open_ports: List[int]
    unpatched_vulnerabilities: int
    network_exposure: Optional[str]
    exposure_score: float


class ExposureScoreListResponse(BaseModel):
    """Response for listing exposure scores."""
    total_results: int
    customer_id: str
    exposures: List[ExposureScoreResponse]


class AttackSurfaceSummaryResponse(BaseModel):
    """Response for attack surface summary."""
    customer_id: str
    total_assets: int
    internet_facing: int
    high_exposure_count: int
    avg_exposure_score: float


class RiskAggregationResponse(BaseModel):
    """Response model for risk aggregation."""
    aggregation_id: str
    aggregation_type: str
    group_id: str
    customer_id: str
    total_entities: int
    avg_risk_score: float
    max_risk_score: float
    risk_level: str
    risk_distribution: dict
    calculated_at: str


class DashboardSummaryResponse(BaseModel):
    """Response for risk dashboard summary."""
    customer_id: str
    total_entities: int
    avg_risk_score: float
    risk_distribution: dict
    critical_count: int
    high_count: int
    generated_at: str


class RiskMatrixResponse(BaseModel):
    """Response for risk matrix data."""
    customer_id: str
    matrix: dict
    generated_at: str


# ===== Dependencies =====

def get_service() -> RiskScoringService:
    """Get risk scoring service instance."""
    return RiskScoringService()


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


# ===== Risk Score Endpoints =====

@router.post("/scores", response_model=RiskScoreResponse, status_code=201)
async def calculate_risk_score(
    score_data: RiskScoreCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """
    Calculate and store risk score for an entity.

    Requires WRITE access level.
    """
    from .risk_models import RiskFactor

    try:
        factors = [
            RiskFactor(
                factor_type=RiskFactorType(f.factor_type),
                value=f.value,
                weight=f.weight,
                description=f.description,
            )
            for f in score_data.factors
        ]

        request = RiskScoreRequest(
            entity_type=score_data.entity_type,
            entity_id=score_data.entity_id,
            entity_name=score_data.entity_name,
            factors=factors,
            asset_criticality=score_data.asset_criticality,
            exposure_score=score_data.exposure_score,
        )

        risk_score = service.calculate_risk_score(request)

        return RiskScoreResponse(
            risk_id=risk_score.risk_id,
            entity_type=risk_score.entity_type,
            entity_id=risk_score.entity_id,
            entity_name=risk_score.entity_name,
            customer_id=risk_score.customer_id,
            risk_score=risk_score.risk_score,
            risk_level=risk_score.risk_level.value,
            factors=[f.__dict__ for f in risk_score.factors],
            calculated_at=risk_score.calculated_at.isoformat(),
            trend=risk_score.trend.value if risk_score.trend else None,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/scores/{entity_type}/{entity_id}", response_model=RiskScoreResponse)
async def get_risk_score(
    entity_type: str,
    entity_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get most recent risk score for entity with customer isolation."""
    risk_score = service.get_risk_score(entity_type, entity_id)
    if not risk_score:
        raise HTTPException(
            status_code=404,
            detail=f"Risk score for {entity_type}/{entity_id} not found"
        )

    return RiskScoreResponse(
        risk_id=risk_score.risk_id,
        entity_type=risk_score.entity_type,
        entity_id=risk_score.entity_id,
        entity_name=risk_score.entity_name,
        customer_id=risk_score.customer_id,
        risk_score=risk_score.risk_score,
        risk_level=risk_score.risk_level.value,
        factors=[f.__dict__ for f in risk_score.factors],
        calculated_at=risk_score.calculated_at.isoformat(),
        trend=risk_score.trend.value if risk_score.trend else None,
    )


@router.get("/scores/high-risk", response_model=RiskSearchResponse)
async def get_high_risk_entities(
    min_score: float = Query(7.0, ge=0, le=10, description="Minimum risk score threshold"),
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get all entities with high or critical risk scores."""
    results = service.get_high_risk_entities(min_score)

    risk_responses = [
        RiskScoreResponse(
            risk_id=r.risk_score.risk_id,
            entity_type=r.risk_score.entity_type,
            entity_id=r.risk_score.entity_id,
            entity_name=r.risk_score.entity_name,
            customer_id=r.risk_score.customer_id,
            risk_score=r.risk_score.risk_score,
            risk_level=r.risk_score.risk_level.value,
            factors=[f.__dict__ for f in r.risk_score.factors],
            calculated_at=r.risk_score.calculated_at.isoformat(),
            trend=r.risk_score.trend.value if r.risk_score.trend else None,
        )
        for r in results
    ]

    return RiskSearchResponse(
        total_results=len(risk_responses),
        customer_id=context.customer_id,
        results=risk_responses,
    )


@router.get("/scores/trending", response_model=RiskSearchResponse)
async def get_trending_entities(
    trend: str = Query("increasing", description="Risk trend: increasing, decreasing, stable"),
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get entities with specific risk trend."""
    try:
        risk_trend = RiskTrend(trend)
        results = service.get_trending_entities(risk_trend)

        risk_responses = [
            RiskScoreResponse(
                risk_id=r.risk_score.risk_id,
                entity_type=r.risk_score.entity_type,
                entity_id=r.risk_score.entity_id,
                entity_name=r.risk_score.entity_name,
                customer_id=r.risk_score.customer_id,
                risk_score=r.risk_score.risk_score,
                risk_level=r.risk_score.risk_level.value,
                factors=[f.__dict__ for f in r.risk_score.factors],
                calculated_at=r.risk_score.calculated_at.isoformat(),
                trend=r.risk_score.trend.value if r.risk_score.trend else None,
            )
            for r in results
        ]

        return RiskSearchResponse(
            total_results=len(risk_responses),
            customer_id=context.customer_id,
            results=risk_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/scores/search", response_model=RiskSearchResponse)
async def search_risk_scores(
    query: Optional[str] = Query(None, description="Search query"),
    entity_type: Optional[str] = Query(None, description="Filter by entity type"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    min_risk_score: Optional[float] = Query(None, ge=0, le=10),
    max_risk_score: Optional[float] = Query(None, ge=0, le=10),
    trend: Optional[str] = Query(None, description="Filter by trend"),
    limit: int = Query(10, ge=1, le=100, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Search risk scores with filters and customer isolation."""
    try:
        request = RiskSearchRequest(
            query=query,
            customer_id=context.customer_id,
            entity_type=entity_type,
            risk_level=RiskLevel(risk_level) if risk_level else None,
            min_risk_score=min_risk_score,
            max_risk_score=max_risk_score,
            trend=RiskTrend(trend) if trend else None,
            limit=limit,
        )
        results = service.search_risk_scores(request)

        risk_responses = [
            RiskScoreResponse(
                risk_id=r.risk_score.risk_id,
                entity_type=r.risk_score.entity_type,
                entity_id=r.risk_score.entity_id,
                entity_name=r.risk_score.entity_name,
                customer_id=r.risk_score.customer_id,
                risk_score=r.risk_score.risk_score,
                risk_level=r.risk_score.risk_level.value,
                factors=[f.__dict__ for f in r.risk_score.factors],
                calculated_at=r.risk_score.calculated_at.isoformat(),
                trend=r.risk_score.trend.value if r.risk_score.trend else None,
            )
            for r in results
        ]

        return RiskSearchResponse(
            total_results=len(risk_responses),
            customer_id=context.customer_id,
            results=risk_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/scores/recalculate/{entity_type}/{entity_id}", response_model=RiskScoreResponse)
async def recalculate_risk_score(
    entity_type: str,
    entity_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """
    Force recalculation of risk score using existing factors.

    Requires WRITE access level.
    """
    try:
        risk_score = service.recalculate_risk_score(entity_type, entity_id)
        if not risk_score:
            raise HTTPException(
                status_code=404,
                detail=f"Risk score for {entity_type}/{entity_id} not found"
            )

        return RiskScoreResponse(
            risk_id=risk_score.risk_id,
            entity_type=risk_score.entity_type,
            entity_id=risk_score.entity_id,
            entity_name=risk_score.entity_name,
            customer_id=risk_score.customer_id,
            risk_score=risk_score.risk_score,
            risk_level=risk_score.risk_level.value,
            factors=[f.__dict__ for f in risk_score.factors],
            calculated_at=risk_score.calculated_at.isoformat(),
            trend=risk_score.trend.value if risk_score.trend else None,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/scores/history/{entity_type}/{entity_id}", response_model=RiskSearchResponse)
async def get_risk_history(
    entity_type: str,
    entity_id: str,
    days: int = Query(30, ge=1, le=365, description="Days of history"),
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get risk score history for entity."""
    history = service.get_risk_history(entity_type, entity_id, days)

    risk_responses = [
        RiskScoreResponse(
            risk_id=rs.risk_id,
            entity_type=rs.entity_type,
            entity_id=rs.entity_id,
            entity_name=rs.entity_name,
            customer_id=rs.customer_id,
            risk_score=rs.risk_score,
            risk_level=rs.risk_level.value,
            factors=[f.__dict__ for f in rs.factors],
            calculated_at=rs.calculated_at.isoformat(),
            trend=rs.trend.value if rs.trend else None,
        )
        for rs in history
    ]

    return RiskSearchResponse(
        total_results=len(risk_responses),
        customer_id=context.customer_id,
        results=risk_responses,
    )


# ===== Asset Criticality Endpoints =====

@router.post("/assets/criticality", response_model=AssetCriticalityResponse, status_code=201)
async def set_asset_criticality(
    criticality_data: AssetCriticalityCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """
    Set asset criticality rating.

    Requires WRITE access level.
    """
    from .risk_models import AssetCriticality

    try:
        criticality = AssetCriticality(
            asset_id=criticality_data.asset_id,
            asset_name=criticality_data.asset_name,
            customer_id=context.customer_id,
            criticality_level=CriticalityLevel(criticality_data.criticality_level),
            criticality_score=criticality_data.criticality_score,
            business_impact=criticality_data.business_impact,
            data_classification=criticality_data.data_classification,
            availability_requirement=criticality_data.availability_requirement,
            justification=criticality_data.justification,
        )

        created = service.set_asset_criticality(
            asset_id=criticality_data.asset_id,
            asset_name=criticality_data.asset_name,
            criticality=criticality,
        )

        return AssetCriticalityResponse(
            asset_id=created.asset_id,
            asset_name=created.asset_name,
            customer_id=created.customer_id,
            criticality_level=created.criticality_level.value,
            criticality_score=created.criticality_score,
            business_impact=created.business_impact,
            data_classification=created.data_classification,
            availability_requirement=created.availability_requirement,
            justification=created.justification,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/assets/{asset_id}/criticality", response_model=AssetCriticalityResponse)
async def get_asset_criticality(
    asset_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get asset criticality rating with customer isolation."""
    criticality = service.get_asset_criticality(asset_id)
    if not criticality:
        raise HTTPException(
            status_code=404,
            detail=f"Asset criticality for {asset_id} not found"
        )

    return AssetCriticalityResponse(
        asset_id=criticality.asset_id,
        asset_name=criticality.asset_name,
        customer_id=criticality.customer_id,
        criticality_level=criticality.criticality_level.value,
        criticality_score=criticality.criticality_score,
        business_impact=criticality.business_impact,
        data_classification=criticality.data_classification,
        availability_requirement=criticality.availability_requirement,
        justification=criticality.justification,
    )


@router.get("/assets/mission-critical", response_model=AssetCriticalityListResponse)
async def get_mission_critical_assets(
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get all mission-critical assets."""
    assets = service.get_mission_critical_assets()

    asset_responses = [
        AssetCriticalityResponse(
            asset_id=a.asset_id,
            asset_name=a.asset_name,
            customer_id=a.customer_id,
            criticality_level=a.criticality_level.value,
            criticality_score=a.criticality_score,
            business_impact=a.business_impact,
            data_classification=a.data_classification,
            availability_requirement=a.availability_requirement,
            justification=a.justification,
        )
        for a in assets
    ]

    return AssetCriticalityListResponse(
        total_results=len(asset_responses),
        customer_id=context.customer_id,
        assets=asset_responses,
    )


@router.get("/assets/by-criticality/{level}", response_model=AssetCriticalityListResponse)
async def get_assets_by_criticality(
    level: str,
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get assets by criticality level."""
    try:
        criticality_level = CriticalityLevel(level)
        assets = service.get_assets_by_criticality(criticality_level)

        asset_responses = [
            AssetCriticalityResponse(
                asset_id=a.asset_id,
                asset_name=a.asset_name,
                customer_id=a.customer_id,
                criticality_level=a.criticality_level.value,
                criticality_score=a.criticality_score,
                business_impact=a.business_impact,
                data_classification=a.data_classification,
                availability_requirement=a.availability_requirement,
                justification=a.justification,
            )
            for a in assets
        ]

        return AssetCriticalityListResponse(
            total_results=len(asset_responses),
            customer_id=context.customer_id,
            assets=asset_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/assets/{asset_id}/criticality", response_model=AssetCriticalityResponse)
async def update_asset_criticality(
    asset_id: str,
    criticality_data: AssetCriticalityCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """
    Update asset criticality rating.

    Requires WRITE access level.
    """
    from .risk_models import AssetCriticality

    try:
        criticality = AssetCriticality(
            asset_id=asset_id,
            asset_name=criticality_data.asset_name,
            customer_id=context.customer_id,
            criticality_level=CriticalityLevel(criticality_data.criticality_level),
            criticality_score=criticality_data.criticality_score,
            business_impact=criticality_data.business_impact,
            data_classification=criticality_data.data_classification,
            availability_requirement=criticality_data.availability_requirement,
            justification=criticality_data.justification,
        )

        updated = service.set_asset_criticality(
            asset_id=asset_id,
            asset_name=criticality_data.asset_name,
            criticality=criticality,
        )

        return AssetCriticalityResponse(
            asset_id=updated.asset_id,
            asset_name=updated.asset_name,
            customer_id=updated.customer_id,
            criticality_level=updated.criticality_level.value,
            criticality_score=updated.criticality_score,
            business_impact=updated.business_impact,
            data_classification=updated.data_classification,
            availability_requirement=updated.availability_requirement,
            justification=updated.justification,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/assets/criticality/summary", response_model=CriticalitySummaryResponse)
async def get_criticality_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get criticality distribution summary."""
    summary = service.get_criticality_summary()

    return CriticalitySummaryResponse(
        customer_id=context.customer_id,
        mission_critical=summary["mission_critical"],
        high=summary["high"],
        medium=summary["medium"],
        low=summary["low"],
        informational=summary["informational"],
        total=sum(summary.values()),
    )


# ===== Exposure Score Endpoints =====

@router.post("/exposure", response_model=ExposureScoreResponse, status_code=201)
async def calculate_exposure_score(
    exposure_data: ExposureScoreCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """
    Calculate exposure score for asset.

    Requires WRITE access level.
    """
    from .risk_models import ExposureScore

    try:
        exposure = ExposureScore(
            asset_id=exposure_data.asset_id,
            asset_name=exposure_data.asset_name,
            customer_id=context.customer_id,
            is_internet_facing=exposure_data.is_internet_facing,
            attack_surface=AttackSurfaceArea(exposure_data.attack_surface),
            open_ports=exposure_data.open_ports,
            unpatched_vulnerabilities=exposure_data.unpatched_vulnerabilities,
            network_exposure=exposure_data.network_exposure,
        )

        calculated = service.calculate_exposure_score(
            asset_id=exposure_data.asset_id,
            asset_name=exposure_data.asset_name,
            exposure=exposure,
        )

        return ExposureScoreResponse(
            asset_id=calculated.asset_id,
            asset_name=calculated.asset_name,
            customer_id=calculated.customer_id,
            is_internet_facing=calculated.is_internet_facing,
            attack_surface=calculated.attack_surface.value,
            open_ports=calculated.open_ports,
            unpatched_vulnerabilities=calculated.unpatched_vulnerabilities,
            network_exposure=calculated.network_exposure,
            exposure_score=calculated.exposure_score,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/exposure/{asset_id}", response_model=ExposureScoreResponse)
async def get_exposure_score(
    asset_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get asset exposure score with customer isolation."""
    exposure = service.get_exposure_score(asset_id)
    if not exposure:
        raise HTTPException(
            status_code=404,
            detail=f"Exposure score for asset {asset_id} not found"
        )

    return ExposureScoreResponse(
        asset_id=exposure.asset_id,
        asset_name=exposure.asset_name,
        customer_id=exposure.customer_id,
        is_internet_facing=exposure.is_internet_facing,
        attack_surface=exposure.attack_surface.value,
        open_ports=exposure.open_ports,
        unpatched_vulnerabilities=exposure.unpatched_vulnerabilities,
        network_exposure=exposure.network_exposure,
        exposure_score=exposure.exposure_score,
    )


@router.get("/exposure/internet-facing", response_model=ExposureScoreListResponse)
async def get_internet_facing_assets(
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get all internet-facing assets."""
    exposures = service.get_internet_facing_assets()

    exposure_responses = [
        ExposureScoreResponse(
            asset_id=e.asset_id,
            asset_name=e.asset_name,
            customer_id=e.customer_id,
            is_internet_facing=e.is_internet_facing,
            attack_surface=e.attack_surface.value,
            open_ports=e.open_ports,
            unpatched_vulnerabilities=e.unpatched_vulnerabilities,
            network_exposure=e.network_exposure,
            exposure_score=e.exposure_score,
        )
        for e in exposures
    ]

    return ExposureScoreListResponse(
        total_results=len(exposure_responses),
        customer_id=context.customer_id,
        exposures=exposure_responses,
    )


@router.get("/exposure/high-exposure", response_model=ExposureScoreListResponse)
async def get_high_exposure_assets(
    min_score: float = Query(6.0, ge=0, le=10, description="Minimum exposure score"),
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get assets with high exposure scores."""
    exposures = service.get_high_exposure_assets(min_score)

    exposure_responses = [
        ExposureScoreResponse(
            asset_id=e.asset_id,
            asset_name=e.asset_name,
            customer_id=e.customer_id,
            is_internet_facing=e.is_internet_facing,
            attack_surface=e.attack_surface.value,
            open_ports=e.open_ports,
            unpatched_vulnerabilities=e.unpatched_vulnerabilities,
            network_exposure=e.network_exposure,
            exposure_score=e.exposure_score,
        )
        for e in exposures
    ]

    return ExposureScoreListResponse(
        total_results=len(exposure_responses),
        customer_id=context.customer_id,
        exposures=exposure_responses,
    )


@router.get("/exposure/attack-surface", response_model=AttackSurfaceSummaryResponse)
async def get_attack_surface_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get attack surface summary."""
    summary = service.get_attack_surface_summary()

    return AttackSurfaceSummaryResponse(
        customer_id=context.customer_id,
        total_assets=summary["total_assets"],
        internet_facing=summary["internet_facing"],
        high_exposure_count=summary["high_exposure_count"],
        avg_exposure_score=summary["avg_exposure_score"],
    )


# ===== Aggregation Endpoints =====

@router.get("/aggregation/by-vendor", response_model=List[RiskAggregationResponse])
async def get_risk_by_vendor(
    vendor_id: Optional[str] = Query(None, description="Specific vendor ID"),
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get risk aggregated by vendor."""
    if vendor_id:
        aggregation = service.get_risk_by_vendor(vendor_id)
        if not aggregation:
            raise HTTPException(status_code=404, detail=f"Vendor {vendor_id} not found")

        return [RiskAggregationResponse(
            aggregation_id=aggregation.aggregation_id,
            aggregation_type=aggregation.aggregation_type.value,
            group_id=aggregation.group_id,
            customer_id=aggregation.customer_id,
            total_entities=aggregation.total_entities,
            avg_risk_score=aggregation.avg_risk_score,
            max_risk_score=aggregation.max_risk_score,
            risk_level=aggregation.risk_level.value,
            risk_distribution=aggregation.risk_distribution,
            calculated_at=aggregation.calculated_at.isoformat(),
        )]

    return []


@router.get("/aggregation/by-sector", response_model=List[RiskAggregationResponse])
async def get_risk_by_sector(
    sector: Optional[str] = Query(None, description="Specific sector"),
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get risk aggregated by sector."""
    # Implementation would be similar to vendor aggregation
    return []


@router.get("/aggregation/by-asset-type", response_model=List[RiskAggregationResponse])
async def get_risk_by_asset_type(
    asset_type: Optional[str] = Query(None, description="Specific asset type"),
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get risk aggregated by asset type."""
    # Implementation would be similar to vendor aggregation
    return []


@router.get("/aggregation/{aggregation_type}/{group_id}", response_model=RiskAggregationResponse)
async def get_risk_aggregation(
    aggregation_type: str,
    group_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get specific risk aggregation."""
    # Route to appropriate aggregation method based on type
    if aggregation_type == "vendor":
        aggregation = service.get_risk_by_vendor(group_id)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported aggregation type: {aggregation_type}")

    if not aggregation:
        raise HTTPException(status_code=404, detail=f"Aggregation not found")

    return RiskAggregationResponse(
        aggregation_id=aggregation.aggregation_id,
        aggregation_type=aggregation.aggregation_type.value,
        group_id=aggregation.group_id,
        customer_id=aggregation.customer_id,
        total_entities=aggregation.total_entities,
        avg_risk_score=aggregation.avg_risk_score,
        max_risk_score=aggregation.max_risk_score,
        risk_level=aggregation.risk_level.value,
        risk_distribution=aggregation.risk_distribution,
        calculated_at=aggregation.calculated_at.isoformat(),
    )


# ===== Dashboard Endpoints =====

@router.get("/dashboard/summary", response_model=DashboardSummaryResponse)
async def get_dashboard_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get comprehensive risk dashboard summary."""
    summary = service.get_dashboard_summary()

    return DashboardSummaryResponse(
        customer_id=summary["customer_id"],
        total_entities=summary["total_entities"],
        avg_risk_score=summary["avg_risk_score"],
        risk_distribution=summary["risk_distribution"],
        critical_count=summary["critical_count"],
        high_count=summary["high_count"],
        generated_at=summary["generated_at"],
    )


@router.get("/dashboard/risk-matrix", response_model=RiskMatrixResponse)
async def get_risk_matrix(
    context: CustomerContext = Depends(require_customer_context),
    service: RiskScoringService = Depends(get_service),
):
    """Get risk matrix data (likelihood vs impact)."""
    matrix = service.get_risk_matrix()

    return RiskMatrixResponse(
        customer_id=matrix["customer_id"],
        matrix=matrix["matrix"],
        generated_at=matrix["generated_at"],
    )
