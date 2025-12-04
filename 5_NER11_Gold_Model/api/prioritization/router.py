"""
Prioritization API Router
=========================

FastAPI router for E12: NOW-NEXT-NEVER Prioritization Framework.
Provides 28 REST endpoints for priority management operations.

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
from .schemas import (
    PriorityItem,
    PriorityScore,
    PriorityCategory,
    EntityType,
    SLAStatus,
    UrgencyType,
    UrgencyFactor,
    RiskFactor,
    EconomicFactor,
    ScoringFactor,
    PrioritizationConfig,
)
from .service import PrioritizationService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/prioritization", tags=["prioritization"])


# ===== Pydantic Request/Response Models =====


class UrgencyFactorCreate(BaseModel):
    """Request model for urgency factor."""
    factor_type: str = Field(..., description="Urgency factor type")
    weight: float = Field(1.0, ge=0.0, le=1.0)
    value: float = Field(..., ge=0.0, le=10.0)
    description: str
    deadline: Optional[str] = None
    evidence: List[str] = Field(default_factory=list)


class RiskFactorCreate(BaseModel):
    """Request model for risk factor."""
    factor_type: str
    weight: float = Field(1.0, ge=0.0, le=1.0)
    value: float = Field(..., ge=0.0, le=10.0)
    description: str


class EconomicFactorCreate(BaseModel):
    """Request model for economic factor."""
    factor_type: str
    weight: float = Field(1.0, ge=0.0, le=1.0)
    value: float
    description: str
    currency: str = "USD"


class PriorityCalculateRequest(BaseModel):
    """Request to calculate priority score."""
    entity_type: str
    entity_id: str
    entity_name: str
    urgency_factors: List[UrgencyFactorCreate] = Field(default_factory=list)
    risk_factors: List[RiskFactorCreate] = Field(default_factory=list)
    economic_factors: List[EconomicFactorCreate] = Field(default_factory=list)


class PriorityItemResponse(BaseModel):
    """Response model for priority item."""
    item_id: str
    customer_id: str
    entity_type: str
    entity_id: str
    entity_name: str
    priority_category: str
    priority_score: float
    deadline: Optional[str]
    sla_status: str
    sla_deadline: Optional[str]
    calculated_at: str
    is_now: bool
    is_sla_at_risk: bool


class PriorityItemListResponse(BaseModel):
    """Response for listing priority items."""
    total_results: int
    customer_id: str
    items: List[PriorityItemResponse]


class PrioritySummaryResponse(BaseModel):
    """Response for category summary."""
    customer_id: str
    category: str
    total_items: int
    avg_priority_score: float
    sla_breached_count: int
    sla_at_risk_count: int


class PriorityItemDetailResponse(BaseModel):
    """Detailed response with all factors."""
    item_id: str
    customer_id: str
    entity_type: str
    entity_id: str
    entity_name: str
    priority_category: str
    priority_score: float
    urgency_factors: List[dict]
    risk_factors: List[dict]
    economic_factors: List[dict]
    deadline: Optional[str]
    sla_status: str
    sla_deadline: Optional[str]
    calculated_at: str


class EscalateRequest(BaseModel):
    """Request to escalate item."""
    item_id: str
    reason: str


class ScheduleRequest(BaseModel):
    """Request to schedule item for NEXT."""
    item_id: str
    scheduled_date: Optional[str] = None


class ClassifyNeverRequest(BaseModel):
    """Request to classify as NEVER."""
    item_id: str
    reason: str


class PriorityScoreResponse(BaseModel):
    """Response for priority score calculation."""
    entity_id: str
    customer_id: str
    overall_score: float
    category: str
    score_breakdown: dict
    confidence: float
    factors: List[dict]


class ScoreWeightsRequest(BaseModel):
    """Request to configure scoring weights."""
    risk_weight: float = Field(..., ge=0.0, le=1.0)
    urgency_weight: float = Field(..., ge=0.0, le=1.0)
    impact_weight: float = Field(..., ge=0.0, le=1.0)
    effort_weight: float = Field(..., ge=0.0, le=1.0)
    roi_weight: float = Field(..., ge=0.0, le=1.0)


class ThresholdsResponse(BaseModel):
    """Response for priority thresholds."""
    customer_id: str
    now_threshold: float
    next_threshold: float


class DashboardSummaryResponse(BaseModel):
    """Response for prioritization dashboard."""
    customer_id: str
    total_items: int
    distribution: dict
    sla_breached: int
    sla_at_risk: int
    generated_at: str


class DistributionResponse(BaseModel):
    """Response for NOW/NEXT/NEVER distribution."""
    customer_id: str
    now_count: int
    next_count: int
    never_count: int
    total: int


class TrendDataPoint(BaseModel):
    """Data point for trend analysis."""
    date: str
    now_count: int
    next_count: int
    never_count: int
    avg_priority_score: float


class TrendsResponse(BaseModel):
    """Response for priority trends."""
    customer_id: str
    period: str
    data_points: List[TrendDataPoint]


class EfficiencyMetrics(BaseModel):
    """Response for remediation efficiency."""
    customer_id: str
    now_completion_rate: float
    next_completion_rate: float
    avg_resolution_time_hours: float
    sla_compliance_rate: float


class BacklogAnalysis(BaseModel):
    """Response for backlog analysis."""
    customer_id: str
    total_backlog: int
    aging_buckets: dict
    priority_distribution: dict


class ExecutiveView(BaseModel):
    """Response for executive prioritization view."""
    customer_id: str
    critical_items_count: int
    sla_at_risk: int
    top_priorities: List[dict]
    risk_summary: dict


# ===== Dependencies =====


def get_service() -> PrioritizationService:
    """Get prioritization service instance."""
    return PrioritizationService()


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


# ===== NOW Category Endpoints (6) =====


@router.get("/now/items", response_model=PriorityItemListResponse)
async def get_now_items(
    limit: int = Query(100, ge=1, le=500, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """Get all items requiring immediate action (NOW category)."""
    items = service.get_now_items(limit=limit)

    item_responses = [
        PriorityItemResponse(
            item_id=item.item_id,
            customer_id=item.customer_id,
            entity_type=item.entity_type.value,
            entity_id=item.entity_id,
            entity_name=item.entity_name,
            priority_category=item.priority_category.value,
            priority_score=item.priority_score,
            deadline=item.deadline.isoformat() if item.deadline else None,
            sla_status=item.sla_status.value,
            sla_deadline=item.sla_deadline.isoformat() if item.sla_deadline else None,
            calculated_at=item.calculated_at.isoformat(),
            is_now=item.is_now,
            is_sla_at_risk=item.is_sla_at_risk,
        )
        for item in items
    ]

    return PriorityItemListResponse(
        total_results=len(item_responses),
        customer_id=context.customer_id,
        items=item_responses,
    )


@router.get("/now/summary", response_model=PrioritySummaryResponse)
async def get_now_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """Get NOW category summary with SLA metrics."""
    items = service.get_now_items()

    avg_score = sum(i.priority_score for i in items) / len(items) if items else 0.0
    breached = len([i for i in items if i.sla_status == SLAStatus.BREACHED])
    at_risk = len([i for i in items if i.sla_status == SLAStatus.AT_RISK])

    return PrioritySummaryResponse(
        customer_id=context.customer_id,
        category="NOW",
        total_items=len(items),
        avg_priority_score=avg_score,
        sla_breached_count=breached,
        sla_at_risk_count=at_risk,
    )


@router.get("/now/{item_id}/details", response_model=PriorityItemDetailResponse)
async def get_now_item_details(
    item_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """Get detailed item information with urgency factors."""
    # Retrieve from Qdrant
    result = service.client.retrieve(
        collection_name=service.COLLECTION_NAME,
        ids=[item_id],
    )

    if not result or result[0].payload["customer_id"] != context.customer_id:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    item = service._payload_to_priority_item(result[0].payload)

    return PriorityItemDetailResponse(
        item_id=item.item_id,
        customer_id=item.customer_id,
        entity_type=item.entity_type.value,
        entity_id=item.entity_id,
        entity_name=item.entity_name,
        priority_category=item.priority_category.value,
        priority_score=item.priority_score,
        urgency_factors=[f.to_dict() for f in item.urgency_factors],
        risk_factors=[f.to_dict() for f in item.risk_factors],
        economic_factors=[f.to_dict() for f in item.economic_factors],
        deadline=item.deadline.isoformat() if item.deadline else None,
        sla_status=item.sla_status.value,
        sla_deadline=item.sla_deadline.isoformat() if item.sla_deadline else None,
        calculated_at=item.calculated_at.isoformat(),
    )


@router.post("/now/escalate", response_model=PriorityItemResponse)
async def escalate_to_now(
    request: EscalateRequest,
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """
    Escalate item to NOW priority.

    Requires WRITE access level.
    """
    try:
        item = service.escalate_to_now(request.item_id)

        return PriorityItemResponse(
            item_id=item.item_id,
            customer_id=item.customer_id,
            entity_type=item.entity_type.value,
            entity_id=item.entity_id,
            entity_name=item.entity_name,
            priority_category=item.priority_category.value,
            priority_score=item.priority_score,
            deadline=item.deadline.isoformat() if item.deadline else None,
            sla_status=item.sla_status.value,
            sla_deadline=item.sla_deadline.isoformat() if item.sla_deadline else None,
            calculated_at=item.calculated_at.isoformat(),
            is_now=item.is_now,
            is_sla_at_risk=item.is_sla_at_risk,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/now/sla-status", response_model=PriorityItemListResponse)
async def get_now_sla_status(
    status: str = Query(..., description="SLA status: within_sla, at_risk, breached"),
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """Get NOW items by SLA status."""
    try:
        sla_status = SLAStatus(status)
        items = service.get_sla_status_items(sla_status)

        # Filter for NOW items only
        now_items = [i for i in items if i.priority_category == PriorityCategory.NOW]

        item_responses = [
            PriorityItemResponse(
                item_id=item.item_id,
                customer_id=item.customer_id,
                entity_type=item.entity_type.value,
                entity_id=item.entity_id,
                entity_name=item.entity_name,
                priority_category=item.priority_category.value,
                priority_score=item.priority_score,
                deadline=item.deadline.isoformat() if item.deadline else None,
                sla_status=item.sla_status.value,
                sla_deadline=item.sla_deadline.isoformat() if item.sla_deadline else None,
                calculated_at=item.calculated_at.isoformat(),
                is_now=item.is_now,
                is_sla_at_risk=item.is_sla_at_risk,
            )
            for item in now_items
        ]

        return PriorityItemListResponse(
            total_results=len(item_responses),
            customer_id=context.customer_id,
            items=item_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/now/complete", response_model=PriorityItemResponse)
async def complete_now_item(
    item_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """
    Mark NOW item as complete (archives it).

    Requires WRITE access level.
    """
    try:
        # In production, this would archive the item
        # For now, we'll move it to NEVER category
        item = service.classify_as_never(item_id, reason="Completed")

        return PriorityItemResponse(
            item_id=item.item_id,
            customer_id=item.customer_id,
            entity_type=item.entity_type.value,
            entity_id=item.entity_id,
            entity_name=item.entity_name,
            priority_category=item.priority_category.value,
            priority_score=item.priority_score,
            deadline=item.deadline.isoformat() if item.deadline else None,
            sla_status=item.sla_status.value,
            sla_deadline=item.sla_deadline.isoformat() if item.sla_deadline else None,
            calculated_at=item.calculated_at.isoformat(),
            is_now=item.is_now,
            is_sla_at_risk=item.is_sla_at_risk,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ===== NEXT Category Endpoints (6) =====


@router.get("/next/items", response_model=PriorityItemListResponse)
async def get_next_items(
    limit: int = Query(100, ge=1, le=500),
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """Get all items scheduled for next action cycle."""
    items = service.get_next_items(limit=limit)

    item_responses = [
        PriorityItemResponse(
            item_id=item.item_id,
            customer_id=item.customer_id,
            entity_type=item.entity_type.value,
            entity_id=item.entity_id,
            entity_name=item.entity_name,
            priority_category=item.priority_category.value,
            priority_score=item.priority_score,
            deadline=item.deadline.isoformat() if item.deadline else None,
            sla_status=item.sla_status.value,
            sla_deadline=item.sla_deadline.isoformat() if item.sla_deadline else None,
            calculated_at=item.calculated_at.isoformat(),
            is_now=item.is_now,
            is_sla_at_risk=item.is_sla_at_risk,
        )
        for item in items
    ]

    return PriorityItemListResponse(
        total_results=len(item_responses),
        customer_id=context.customer_id,
        items=item_responses,
    )


@router.get("/next/summary", response_model=PrioritySummaryResponse)
async def get_next_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """Get NEXT category summary."""
    items = service.get_next_items()

    avg_score = sum(i.priority_score for i in items) / len(items) if items else 0.0
    breached = len([i for i in items if i.sla_status == SLAStatus.BREACHED])
    at_risk = len([i for i in items if i.sla_status == SLAStatus.AT_RISK])

    return PrioritySummaryResponse(
        customer_id=context.customer_id,
        category="NEXT",
        total_items=len(items),
        avg_priority_score=avg_score,
        sla_breached_count=breached,
        sla_at_risk_count=at_risk,
    )


@router.get("/next/{item_id}/details", response_model=PriorityItemDetailResponse)
async def get_next_item_details(
    item_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """Get detailed NEXT item information with scheduling."""
    result = service.client.retrieve(
        collection_name=service.COLLECTION_NAME,
        ids=[item_id],
    )

    if not result or result[0].payload["customer_id"] != context.customer_id:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    item = service._payload_to_priority_item(result[0].payload)

    return PriorityItemDetailResponse(
        item_id=item.item_id,
        customer_id=item.customer_id,
        entity_type=item.entity_type.value,
        entity_id=item.entity_id,
        entity_name=item.entity_name,
        priority_category=item.priority_category.value,
        priority_score=item.priority_score,
        urgency_factors=[f.to_dict() for f in item.urgency_factors],
        risk_factors=[f.to_dict() for f in item.risk_factors],
        economic_factors=[f.to_dict() for f in item.economic_factors],
        deadline=item.deadline.isoformat() if item.deadline else None,
        sla_status=item.sla_status.value,
        sla_deadline=item.sla_deadline.isoformat() if item.sla_deadline else None,
        calculated_at=item.calculated_at.isoformat(),
    )


@router.post("/next/schedule", response_model=PriorityItemResponse)
async def schedule_for_next(
    request: ScheduleRequest,
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """
    Schedule item for NEXT priority.

    Requires WRITE access level.
    """
    # Implementation similar to escalate but sets NEXT category
    # For now, return placeholder
    raise HTTPException(status_code=501, detail="Schedule for NEXT not yet implemented")


@router.get("/next/queue", response_model=PriorityItemListResponse)
async def get_next_queue(
    limit: int = Query(50, ge=1, le=200),
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """Get ordered NEXT queue by priority score."""
    items = service.get_next_items(limit=limit)

    # Sort by priority score descending
    sorted_items = sorted(items, key=lambda x: x.priority_score, reverse=True)

    item_responses = [
        PriorityItemResponse(
            item_id=item.item_id,
            customer_id=item.customer_id,
            entity_type=item.entity_type.value,
            entity_id=item.entity_id,
            entity_name=item.entity_name,
            priority_category=item.priority_category.value,
            priority_score=item.priority_score,
            deadline=item.deadline.isoformat() if item.deadline else None,
            sla_status=item.sla_status.value,
            sla_deadline=item.sla_deadline.isoformat() if item.sla_deadline else None,
            calculated_at=item.calculated_at.isoformat(),
            is_now=item.is_now,
            is_sla_at_risk=item.is_sla_at_risk,
        )
        for item in sorted_items
    ]

    return PriorityItemListResponse(
        total_results=len(item_responses),
        customer_id=context.customer_id,
        items=item_responses,
    )


@router.post("/next/promote", response_model=PriorityItemResponse)
async def promote_next_to_now(
    item_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """
    Promote NEXT item to NOW priority.

    Requires WRITE access level.
    """
    try:
        item = service.promote_next_to_now(item_id)

        return PriorityItemResponse(
            item_id=item.item_id,
            customer_id=item.customer_id,
            entity_type=item.entity_type.value,
            entity_id=item.entity_id,
            entity_name=item.entity_name,
            priority_category=item.priority_category.value,
            priority_score=item.priority_score,
            deadline=item.deadline.isoformat() if item.deadline else None,
            sla_status=item.sla_status.value,
            sla_deadline=item.sla_deadline.isoformat() if item.sla_deadline else None,
            calculated_at=item.calculated_at.isoformat(),
            is_now=item.is_now,
            is_sla_at_risk=item.is_sla_at_risk,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ===== NEVER Category Endpoints (4) =====


@router.get("/never/items", response_model=PriorityItemListResponse)
async def get_never_items(
    limit: int = Query(100, ge=1, le=500),
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """Get all items designated as NEVER priority."""
    items = service.get_never_items(limit=limit)

    item_responses = [
        PriorityItemResponse(
            item_id=item.item_id,
            customer_id=item.customer_id,
            entity_type=item.entity_type.value,
            entity_id=item.entity_id,
            entity_name=item.entity_name,
            priority_category=item.priority_category.value,
            priority_score=item.priority_score,
            deadline=item.deadline.isoformat() if item.deadline else None,
            sla_status=item.sla_status.value,
            sla_deadline=item.sla_deadline.isoformat() if item.sla_deadline else None,
            calculated_at=item.calculated_at.isoformat(),
            is_now=item.is_now,
            is_sla_at_risk=item.is_sla_at_risk,
        )
        for item in items
    ]

    return PriorityItemListResponse(
        total_results=len(item_responses),
        customer_id=context.customer_id,
        items=item_responses,
    )


@router.get("/never/summary", response_model=PrioritySummaryResponse)
async def get_never_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """Get NEVER category summary."""
    items = service.get_never_items()

    avg_score = sum(i.priority_score for i in items) / len(items) if items else 0.0

    return PrioritySummaryResponse(
        customer_id=context.customer_id,
        category="NEVER",
        total_items=len(items),
        avg_priority_score=avg_score,
        sla_breached_count=0,
        sla_at_risk_count=0,
    )


@router.post("/never/classify", response_model=PriorityItemResponse)
async def classify_as_never(
    request: ClassifyNeverRequest,
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """
    Classify item as NEVER priority.

    Requires WRITE access level.
    """
    try:
        item = service.classify_as_never(request.item_id, request.reason)

        return PriorityItemResponse(
            item_id=item.item_id,
            customer_id=item.customer_id,
            entity_type=item.entity_type.value,
            entity_id=item.entity_id,
            entity_name=item.entity_name,
            priority_category=item.priority_category.value,
            priority_score=item.priority_score,
            deadline=item.deadline.isoformat() if item.deadline else None,
            sla_status=item.sla_status.value,
            sla_deadline=item.sla_deadline.isoformat() if item.sla_deadline else None,
            calculated_at=item.calculated_at.isoformat(),
            is_now=item.is_now,
            is_sla_at_risk=item.is_sla_at_risk,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/never/reconsider", response_model=PriorityItemResponse)
async def reconsider_never_item(
    item_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """
    Move NEVER item for reconsideration (promotes to NEXT).

    Requires WRITE access level.
    """
    # Implementation would promote NEVER to NEXT
    raise HTTPException(status_code=501, detail="Reconsider not yet implemented")


# ===== Priority Scoring Endpoints (6) =====


@router.post("/score/calculate", response_model=PriorityItemResponse, status_code=201)
async def calculate_priority_score(
    request: PriorityCalculateRequest,
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """
    Calculate priority score for entity.

    Requires WRITE access level.
    """
    try:
        # Convert request to domain models
        urgency_factors = [
            UrgencyFactor(
                factor_type=UrgencyType(f.factor_type),
                weight=f.weight,
                value=f.value,
                description=f.description,
                deadline=datetime.fromisoformat(f.deadline) if f.deadline else None,
                evidence=f.evidence,
            )
            for f in request.urgency_factors
        ]

        risk_factors = [
            RiskFactor(
                factor_type=f.factor_type,
                weight=f.weight,
                value=f.value,
                description=f.description,
            )
            for f in request.risk_factors
        ]

        economic_factors = [
            EconomicFactor(
                factor_type=f.factor_type,
                weight=f.weight,
                value=f.value,
                description=f.description,
                currency=f.currency,
            )
            for f in request.economic_factors
        ]

        item = service.calculate_priority_score(
            entity_type=EntityType(request.entity_type),
            entity_id=request.entity_id,
            entity_name=request.entity_name,
            urgency_factors=urgency_factors,
            risk_factors=risk_factors,
            economic_factors=economic_factors,
        )

        return PriorityItemResponse(
            item_id=item.item_id,
            customer_id=item.customer_id,
            entity_type=item.entity_type.value,
            entity_id=item.entity_id,
            entity_name=item.entity_name,
            priority_category=item.priority_category.value,
            priority_score=item.priority_score,
            deadline=item.deadline.isoformat() if item.deadline else None,
            sla_status=item.sla_status.value,
            sla_deadline=item.sla_deadline.isoformat() if item.sla_deadline else None,
            calculated_at=item.calculated_at.isoformat(),
            is_now=item.is_now,
            is_sla_at_risk=item.is_sla_at_risk,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/score/{entity_id}/breakdown", response_model=PriorityScoreResponse)
async def get_score_breakdown(
    entity_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """Get priority score breakdown by factors."""
    # Retrieve item and return detailed breakdown
    raise HTTPException(status_code=501, detail="Score breakdown not yet implemented")


@router.get("/score/factors")
async def list_scoring_factors(
    context: CustomerContext = Depends(require_customer_context),
):
    """List all available scoring factors and their weights."""
    return {
        "customer_id": context.customer_id,
        "factor_categories": {
            "risk": ["vulnerability_score", "threat_score", "exposure_score", "asset_score"],
            "urgency": ["exploit_available", "active_campaign", "compliance_deadline", "business_critical"],
            "impact": ["financial", "operational", "reputational", "compliance"],
            "effort": ["complexity", "resource_requirements", "dependencies"],
            "roi": ["cost_savings", "risk_reduction_value", "business_value"],
        },
    }


@router.post("/score/weights")
async def configure_scoring_weights(
    request: ScoreWeightsRequest,
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """
    Configure scoring weights for customer.

    Requires ADMIN access level.
    """
    # Store customer-specific weights
    raise HTTPException(status_code=501, detail="Configure weights not yet implemented")


@router.get("/score/thresholds", response_model=ThresholdsResponse)
async def get_priority_thresholds(
    context: CustomerContext = Depends(require_customer_context),
):
    """Get priority thresholds configuration."""
    config = PrioritizationConfig(customer_id=context.customer_id)

    return ThresholdsResponse(
        customer_id=context.customer_id,
        now_threshold=config.thresholds["now_threshold"],
        next_threshold=config.thresholds["next_threshold"],
    )


@router.post("/score/batch")
async def batch_priority_calculation(
    requests: List[PriorityCalculateRequest],
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """
    Batch priority calculation for multiple entities.

    Requires WRITE access level.
    """
    raise HTTPException(status_code=501, detail="Batch calculation not yet implemented")


# ===== Dashboard Endpoints (6) =====


@router.get("/dashboard/summary", response_model=DashboardSummaryResponse)
async def get_dashboard_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """Get comprehensive prioritization dashboard summary."""
    summary = service.get_dashboard_summary()

    return DashboardSummaryResponse(
        customer_id=summary["customer_id"],
        total_items=summary["total_items"],
        distribution=summary["distribution"],
        sla_breached=summary["sla_breached"],
        sla_at_risk=summary["sla_at_risk"],
        generated_at=summary["generated_at"],
    )


@router.get("/dashboard/distribution", response_model=DistributionResponse)
async def get_priority_distribution(
    context: CustomerContext = Depends(require_customer_context),
    service: PrioritizationService = Depends(get_service),
):
    """Get NOW/NEXT/NEVER distribution."""
    summary = service.get_dashboard_summary()
    dist = summary["distribution"]

    return DistributionResponse(
        customer_id=context.customer_id,
        now_count=dist["NOW"],
        next_count=dist["NEXT"],
        never_count=dist["NEVER"],
        total=summary["total_items"],
    )


@router.get("/dashboard/trends", response_model=TrendsResponse)
async def get_priority_trends(
    days: int = Query(30, ge=1, le=365, description="Days of trend data"),
    context: CustomerContext = Depends(require_customer_context),
):
    """Get priority trends over time."""
    # Generate trend data
    raise HTTPException(status_code=501, detail="Trends not yet implemented")


@router.get("/dashboard/efficiency", response_model=EfficiencyMetrics)
async def get_remediation_efficiency(
    context: CustomerContext = Depends(require_customer_context),
):
    """Get remediation efficiency metrics."""
    raise HTTPException(status_code=501, detail="Efficiency metrics not yet implemented")


@router.get("/dashboard/backlog", response_model=BacklogAnalysis)
async def get_backlog_analysis(
    context: CustomerContext = Depends(require_customer_context),
):
    """Get backlog analysis with aging buckets."""
    raise HTTPException(status_code=501, detail="Backlog analysis not yet implemented")


@router.get("/dashboard/executive", response_model=ExecutiveView)
async def get_executive_view(
    context: CustomerContext = Depends(require_customer_context),
):
    """Get executive prioritization dashboard view."""
    raise HTTPException(status_code=501, detail="Executive view not yet implemented")
