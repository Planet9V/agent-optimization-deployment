"""
Vendor Equipment API Router
===========================

FastAPI router for E15: Vendor Equipment Lifecycle Management.
Provides REST endpoints for vendor and equipment operations.

Version: 1.6.0
Created: 2025-12-04
Updated: 2025-12-04 - Added maintenance scheduling endpoints (Days 10-11)
"""

from datetime import date, datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Header, Depends
from pydantic import BaseModel, Field
import logging

from ..customer_isolation import (
    CustomerContext,
    CustomerContextManager,
    CustomerAccessLevel,
)
from .vendor_models import (
    VendorRiskLevel,
    SupportStatus,
    LifecycleStatus,
    MaintenanceSchedule,
    ServiceLevel,
    Criticality,
    MaintenanceWindowType,
    MaintenanceWindow,
    MaintenancePrediction,
    WorkOrderStatus,
    WorkOrderPriority,
    MaintenanceWorkOrder,
)
from .vendor_service import (
    VendorEquipmentService,
    VendorSearchRequest,
    EquipmentSearchRequest,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/vendor-equipment", tags=["vendor-equipment"])


# ===== Pydantic Models =====

class VendorCreate(BaseModel):
    """Request model for vendor creation."""
    vendor_id: str = Field(..., description="Unique vendor identifier")
    name: str = Field(..., description="Vendor name")
    risk_score: float = Field(0.0, ge=0.0, le=10.0, description="Risk score 0-10")
    support_status: str = Field("active", description="Support status")
    country: Optional[str] = None
    industry_focus: List[str] = Field(default_factory=list)
    supply_chain_tier: int = Field(1, ge=1, le=3)
    website: Optional[str] = None
    contact_email: Optional[str] = None


class VendorResponse(BaseModel):
    """Response model for vendor data."""
    vendor_id: str
    name: str
    customer_id: str
    risk_score: float
    risk_level: str
    support_status: str
    country: Optional[str]
    industry_focus: List[str]
    supply_chain_tier: int
    total_cves: int
    avg_cvss_score: float


class EquipmentCreate(BaseModel):
    """Request model for equipment creation."""
    model_id: str = Field(..., description="Unique model identifier")
    vendor_id: str = Field(..., description="Associated vendor ID")
    model_name: str = Field(..., description="Equipment model name")
    product_line: Optional[str] = None
    release_date: Optional[date] = None
    eol_date: Optional[date] = None
    eos_date: Optional[date] = None
    current_version: Optional[str] = None
    maintenance_schedule: str = Field("quarterly")
    criticality: str = Field("medium")
    category: Optional[str] = None
    description: Optional[str] = None


class EquipmentResponse(BaseModel):
    """Response model for equipment data."""
    model_id: str
    vendor_id: str
    model_name: str
    customer_id: str
    product_line: Optional[str]
    eol_date: Optional[date]
    eos_date: Optional[date]
    lifecycle_status: str
    criticality: str
    category: Optional[str]
    days_to_eol: Optional[int]
    days_to_eos: Optional[int]


class VendorSearchResponse(BaseModel):
    """Response for vendor search results."""
    total_results: int
    customer_id: str
    results: List[VendorResponse]


class EquipmentSearchResponse(BaseModel):
    """Response for equipment search results."""
    total_results: int
    customer_id: str
    results: List[EquipmentResponse]


class VendorRiskSummaryResponse(BaseModel):
    """Response for vendor risk summary."""
    vendor_id: str
    vendor_name: str
    total_equipment: int
    total_cves: int
    avg_cvss: float
    critical_cves: int
    equipment_at_eol: int
    equipment_approaching_eol: int
    risk_score: float
    risk_level: str


class MaintenanceScheduleItem(BaseModel):
    """Single maintenance schedule item."""
    model_id: str
    model_name: str
    vendor_id: str
    lifecycle_status: str
    days_to_eol: Optional[int]
    criticality: str
    recommendation: str


class MaintenanceScheduleResponse(BaseModel):
    """Response for maintenance schedule."""
    customer_id: str
    total_items: int
    items: List[MaintenanceScheduleItem]


class VulnerabilityFlagRequest(BaseModel):
    """Request to flag vendor vulnerability."""
    vendor_id: str
    cve_id: str
    cvss_score: float = Field(..., ge=0.0, le=10.0)
    description: str


class VulnerabilityFlagResponse(BaseModel):
    """Response for vulnerability flagging."""
    vendor_id: str
    cve_id: str
    affected_equipment_count: int
    message: str


# ===== Maintenance Window Models =====

class MaintenanceWindowCreate(BaseModel):
    """Request model for maintenance window creation."""
    window_id: str = Field(..., description="Unique window identifier")
    name: str = Field(..., description="Window name")
    window_type: str = Field("scheduled", description="Window type: scheduled, emergency, recurring, blackout")
    start_time: datetime = Field(..., description="Window start time")
    end_time: datetime = Field(..., description="Window end time")
    affected_equipment_ids: List[str] = Field(default_factory=list, description="Equipment IDs affected")
    recurrence_pattern: Optional[str] = Field(None, description="Recurrence pattern for recurring windows")
    notes: Optional[str] = Field(None, description="Additional notes")


class MaintenanceWindowResponse(BaseModel):
    """Response model for maintenance window."""
    window_id: str
    name: str
    customer_id: str
    window_type: str
    start_time: datetime
    end_time: datetime
    affected_equipment_ids: List[str]
    recurrence_pattern: Optional[str]
    notes: Optional[str]
    is_active: bool


class MaintenanceWindowListResponse(BaseModel):
    """Response for listing maintenance windows."""
    total_results: int
    customer_id: str
    windows: List[MaintenanceWindowResponse]


class MaintenanceConflictResponse(BaseModel):
    """Response for maintenance conflict check."""
    has_conflict: bool
    conflicting_windows: List[MaintenanceWindowResponse]


# ===== Predictive Maintenance Models =====

class MaintenancePredictionResponse(BaseModel):
    """Response model for maintenance prediction."""
    equipment_id: str
    equipment_name: str
    customer_id: str
    predicted_date: date
    confidence_score: float
    risk_level: str
    maintenance_type: str
    recommendation: str


class MaintenancePredictionListResponse(BaseModel):
    """Response for list of predictions."""
    total_predictions: int
    customer_id: str
    predictions: List[MaintenancePredictionResponse]


class MaintenanceForecastResponse(BaseModel):
    """Response for maintenance forecast."""
    forecast_months: int
    customer_id: str
    generated_at: str
    monthly_breakdown: List[dict]


# ===== Work Order Models =====

class WorkOrderCreate(BaseModel):
    """Request model for work order creation."""
    work_order_id: Optional[str] = Field(None, description="Work order ID (auto-generated if not provided)")
    equipment_id: str = Field(..., description="Equipment ID")
    equipment_name: str = Field(..., description="Equipment name")
    title: str = Field(..., description="Work order title")
    description: Optional[str] = Field(None, description="Detailed description")
    priority: str = Field("medium", description="Priority: low, medium, high, critical")
    scheduled_start: datetime = Field(..., description="Scheduled start time")
    scheduled_end: datetime = Field(..., description="Scheduled end time")
    assigned_technician: Optional[str] = Field(None, description="Assigned technician")
    maintenance_window_id: Optional[str] = Field(None, description="Associated maintenance window")


class WorkOrderResponse(BaseModel):
    """Response model for work order."""
    work_order_id: str
    customer_id: str
    equipment_id: str
    equipment_name: str
    title: str
    description: Optional[str]
    priority: str
    status: str
    scheduled_start: datetime
    scheduled_end: datetime
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]
    assigned_technician: Optional[str]
    maintenance_window_id: Optional[str]
    notes: Optional[str]
    is_overdue: bool


class WorkOrderListResponse(BaseModel):
    """Response for listing work orders."""
    total_results: int
    customer_id: str
    work_orders: List[WorkOrderResponse]


class WorkOrderStatusUpdate(BaseModel):
    """Request to update work order status."""
    status: str = Field(..., description="New status: pending, scheduled, in_progress, completed, cancelled")
    notes: Optional[str] = Field(None, description="Status update notes")


class WorkOrderSummaryResponse(BaseModel):
    """Response for work order summary."""
    customer_id: str
    total: int
    status_breakdown: dict
    priority_breakdown: dict
    overdue_count: int


# ===== Dependencies =====

def get_service() -> VendorEquipmentService:
    """Get vendor equipment service instance."""
    # In production, this would be injected/configured
    return VendorEquipmentService()


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


# ===== Vendor Endpoints =====

@router.post("/vendors", response_model=VendorResponse, status_code=201)
async def create_vendor(
    vendor_data: VendorCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """
    Create a new vendor for the customer.

    Requires WRITE access level.
    """
    from .vendor_models import Vendor, SupportStatus

    try:
        vendor = Vendor(
            vendor_id=vendor_data.vendor_id,
            name=vendor_data.name,
            customer_id=context.customer_id,
            risk_score=vendor_data.risk_score,
            support_status=SupportStatus(vendor_data.support_status),
            country=vendor_data.country,
            industry_focus=vendor_data.industry_focus,
            supply_chain_tier=vendor_data.supply_chain_tier,
            website=vendor_data.website,
            contact_email=vendor_data.contact_email,
        )
        created = service.create_vendor(vendor)

        return VendorResponse(
            vendor_id=created.vendor_id,
            name=created.name,
            customer_id=created.customer_id,
            risk_score=created.risk_score,
            risk_level=created.risk_level.value,
            support_status=created.support_status.value,
            country=created.country,
            industry_focus=created.industry_focus,
            supply_chain_tier=created.supply_chain_tier,
            total_cves=created.total_cves,
            avg_cvss_score=created.avg_cvss_score,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/vendors/{vendor_id}", response_model=VendorResponse)
async def get_vendor(
    vendor_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Get vendor by ID with customer isolation."""
    vendor = service.get_vendor(vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail=f"Vendor {vendor_id} not found")

    return VendorResponse(
        vendor_id=vendor.vendor_id,
        name=vendor.name,
        customer_id=vendor.customer_id,
        risk_score=vendor.risk_score,
        risk_level=vendor.risk_level.value,
        support_status=vendor.support_status.value,
        country=vendor.country,
        industry_focus=vendor.industry_focus,
        supply_chain_tier=vendor.supply_chain_tier,
        total_cves=vendor.total_cves,
        avg_cvss_score=vendor.avg_cvss_score,
    )


@router.get("/vendors", response_model=VendorSearchResponse)
async def search_vendors(
    query: Optional[str] = Query(None, description="Search query"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    min_risk_score: Optional[float] = Query(None, ge=0, le=10, description="Minimum risk score"),
    support_status: Optional[str] = Query(None, description="Filter by support status"),
    supply_chain_tier: Optional[int] = Query(None, ge=1, le=3, description="Supply chain tier"),
    limit: int = Query(10, ge=1, le=100, description="Maximum results"),
    include_system: bool = Query(True, description="Include SYSTEM vendors"),
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Search vendors with filters and customer isolation."""
    try:
        request = VendorSearchRequest(
            query=query,
            customer_id=context.customer_id,
            risk_level=VendorRiskLevel(risk_level) if risk_level else None,
            min_risk_score=min_risk_score,
            support_status=SupportStatus(support_status) if support_status else None,
            supply_chain_tier=supply_chain_tier,
            limit=limit,
            include_system=include_system,
        )
        results = service.search_vendors(request)

        vendor_responses = [
            VendorResponse(
                vendor_id=r.vendor.vendor_id,
                name=r.vendor.name,
                customer_id=r.vendor.customer_id,
                risk_score=r.vendor.risk_score,
                risk_level=r.vendor.risk_level.value,
                support_status=r.vendor.support_status.value,
                country=r.vendor.country,
                industry_focus=r.vendor.industry_focus,
                supply_chain_tier=r.vendor.supply_chain_tier,
                total_cves=r.vendor.total_cves,
                avg_cvss_score=r.vendor.avg_cvss_score,
            )
            for r in results
        ]

        return VendorSearchResponse(
            total_results=len(vendor_responses),
            customer_id=context.customer_id,
            results=vendor_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/vendors/{vendor_id}/risk-summary", response_model=VendorRiskSummaryResponse)
async def get_vendor_risk_summary(
    vendor_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Get comprehensive risk summary for a vendor."""
    summary = service.get_vendor_risk_summary(vendor_id)
    if not summary:
        raise HTTPException(status_code=404, detail=f"Vendor {vendor_id} not found")

    return VendorRiskSummaryResponse(
        vendor_id=summary.vendor_id,
        vendor_name=summary.vendor_name,
        total_equipment=summary.total_equipment,
        total_cves=summary.total_cves,
        avg_cvss=summary.avg_cvss,
        critical_cves=summary.critical_cves,
        equipment_at_eol=summary.equipment_at_eol,
        equipment_approaching_eol=summary.equipment_approaching_eol,
        risk_score=summary.risk_score,
        risk_level=summary.risk_level.value,
    )


@router.get("/vendors/high-risk", response_model=VendorSearchResponse)
async def get_high_risk_vendors(
    min_risk_score: float = Query(7.0, ge=0, le=10, description="Minimum risk score threshold"),
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Get all vendors with high risk scores."""
    results = service.get_high_risk_vendors(min_risk_score)

    vendor_responses = [
        VendorResponse(
            vendor_id=r.vendor.vendor_id,
            name=r.vendor.name,
            customer_id=r.vendor.customer_id,
            risk_score=r.vendor.risk_score,
            risk_level=r.vendor.risk_level.value,
            support_status=r.vendor.support_status.value,
            country=r.vendor.country,
            industry_focus=r.vendor.industry_focus,
            supply_chain_tier=r.vendor.supply_chain_tier,
            total_cves=r.vendor.total_cves,
            avg_cvss_score=r.vendor.avg_cvss_score,
        )
        for r in results
    ]

    return VendorSearchResponse(
        total_results=len(vendor_responses),
        customer_id=context.customer_id,
        results=vendor_responses,
    )


# ===== Equipment Endpoints =====

@router.post("/equipment", response_model=EquipmentResponse, status_code=201)
async def create_equipment(
    equipment_data: EquipmentCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """
    Create a new equipment model for the customer.

    Requires WRITE access level.
    """
    from .vendor_models import EquipmentModel, MaintenanceSchedule, Criticality

    try:
        equipment = EquipmentModel(
            model_id=equipment_data.model_id,
            vendor_id=equipment_data.vendor_id,
            model_name=equipment_data.model_name,
            customer_id=context.customer_id,
            product_line=equipment_data.product_line,
            release_date=equipment_data.release_date,
            eol_date=equipment_data.eol_date,
            eos_date=equipment_data.eos_date,
            current_version=equipment_data.current_version,
            maintenance_schedule=MaintenanceSchedule(equipment_data.maintenance_schedule),
            criticality=Criticality(equipment_data.criticality),
            category=equipment_data.category,
            description=equipment_data.description,
        )
        created = service.create_equipment(equipment)

        return EquipmentResponse(
            model_id=created.model_id,
            vendor_id=created.vendor_id,
            model_name=created.model_name,
            customer_id=created.customer_id,
            product_line=created.product_line,
            eol_date=created.eol_date,
            eos_date=created.eos_date,
            lifecycle_status=created.lifecycle_status.value,
            criticality=created.criticality.value if hasattr(created.criticality, 'value') else created.criticality,
            category=created.category,
            days_to_eol=created.days_to_eol(),
            days_to_eos=created.days_to_eos(),
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/equipment/{model_id}", response_model=EquipmentResponse)
async def get_equipment(
    model_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Get equipment model by ID with customer isolation."""
    equipment = service.get_equipment(model_id)
    if not equipment:
        raise HTTPException(status_code=404, detail=f"Equipment {model_id} not found")

    return EquipmentResponse(
        model_id=equipment.model_id,
        vendor_id=equipment.vendor_id,
        model_name=equipment.model_name,
        customer_id=equipment.customer_id,
        product_line=equipment.product_line,
        eol_date=equipment.eol_date,
        eos_date=equipment.eos_date,
        lifecycle_status=equipment.lifecycle_status.value,
        criticality=equipment.criticality.value if hasattr(equipment.criticality, 'value') else equipment.criticality,
        category=equipment.category,
        days_to_eol=equipment.days_to_eol(),
        days_to_eos=equipment.days_to_eos(),
    )


@router.get("/equipment", response_model=EquipmentSearchResponse)
async def search_equipment(
    query: Optional[str] = Query(None, description="Search query"),
    vendor_id: Optional[str] = Query(None, description="Filter by vendor"),
    lifecycle_status: Optional[str] = Query(None, description="Filter by lifecycle status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    criticality: Optional[str] = Query(None, description="Filter by criticality"),
    approaching_eol_days: Optional[int] = Query(None, ge=1, description="Find equipment within N days of EOL"),
    limit: int = Query(10, ge=1, le=100, description="Maximum results"),
    include_system: bool = Query(True, description="Include SYSTEM equipment"),
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Search equipment with filters and customer isolation."""
    try:
        request = EquipmentSearchRequest(
            query=query,
            customer_id=context.customer_id,
            vendor_id=vendor_id,
            lifecycle_status=LifecycleStatus(lifecycle_status) if lifecycle_status else None,
            approaching_eol_days=approaching_eol_days,
            category=category,
            criticality=criticality,
            limit=limit,
            include_system=include_system,
        )
        results = service.search_equipment(request)

        equipment_responses = [
            EquipmentResponse(
                model_id=r.equipment.model_id,
                vendor_id=r.equipment.vendor_id,
                model_name=r.equipment.model_name,
                customer_id=r.equipment.customer_id,
                product_line=r.equipment.product_line,
                eol_date=r.equipment.eol_date,
                eos_date=r.equipment.eos_date,
                lifecycle_status=r.equipment.lifecycle_status.value,
                criticality=r.equipment.criticality.value if hasattr(r.equipment.criticality, 'value') else r.equipment.criticality,
                category=r.equipment.category,
                days_to_eol=r.days_to_eol,
                days_to_eos=r.days_to_eos,
            )
            for r in results
        ]

        return EquipmentSearchResponse(
            total_results=len(equipment_responses),
            customer_id=context.customer_id,
            results=equipment_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/equipment/approaching-eol", response_model=EquipmentSearchResponse)
async def get_equipment_approaching_eol(
    days: int = Query(180, ge=1, le=365, description="Days threshold for EOL"),
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Get all equipment approaching EOL within specified days."""
    results = service.get_equipment_approaching_eol(days)

    equipment_responses = [
        EquipmentResponse(
            model_id=r.equipment.model_id,
            vendor_id=r.equipment.vendor_id,
            model_name=r.equipment.model_name,
            customer_id=r.equipment.customer_id,
            product_line=r.equipment.product_line,
            eol_date=r.equipment.eol_date,
            eos_date=r.equipment.eos_date,
            lifecycle_status=r.equipment.lifecycle_status.value,
            criticality=r.equipment.criticality.value if hasattr(r.equipment.criticality, 'value') else r.equipment.criticality,
            category=r.equipment.category,
            days_to_eol=r.days_to_eol,
            days_to_eos=r.days_to_eos,
        )
        for r in results
    ]

    return EquipmentSearchResponse(
        total_results=len(equipment_responses),
        customer_id=context.customer_id,
        results=equipment_responses,
    )


@router.get("/equipment/eol", response_model=EquipmentSearchResponse)
async def get_eol_equipment(
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Get all equipment that has passed EOL."""
    results = service.get_eol_equipment()

    equipment_responses = [
        EquipmentResponse(
            model_id=r.equipment.model_id,
            vendor_id=r.equipment.vendor_id,
            model_name=r.equipment.model_name,
            customer_id=r.equipment.customer_id,
            product_line=r.equipment.product_line,
            eol_date=r.equipment.eol_date,
            eos_date=r.equipment.eos_date,
            lifecycle_status=r.equipment.lifecycle_status.value,
            criticality=r.equipment.criticality.value if hasattr(r.equipment.criticality, 'value') else r.equipment.criticality,
            category=r.equipment.category,
            days_to_eol=r.days_to_eol,
            days_to_eos=r.days_to_eos,
        )
        for r in results
    ]

    return EquipmentSearchResponse(
        total_results=len(equipment_responses),
        customer_id=context.customer_id,
        results=equipment_responses,
    )


# ===== Maintenance Schedule Endpoints =====

@router.get("/maintenance-schedule", response_model=MaintenanceScheduleResponse)
async def get_maintenance_schedule(
    limit: int = Query(50, ge=1, le=100, description="Maximum items"),
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """
    Get prioritized maintenance schedule.

    Prioritized by:
    1. EOL proximity
    2. Vulnerability count
    3. Criticality
    """
    results = service.get_maintenance_schedule(limit)

    items = [
        MaintenanceScheduleItem(
            model_id=eq_result.equipment.model_id,
            model_name=eq_result.equipment.model_name,
            vendor_id=eq_result.equipment.vendor_id,
            lifecycle_status=eq_result.equipment.lifecycle_status.value,
            days_to_eol=eq_result.days_to_eol,
            criticality=eq_result.equipment.criticality.value if hasattr(eq_result.equipment.criticality, 'value') else eq_result.equipment.criticality,
            recommendation=recommendation,
        )
        for eq_result, recommendation in results
    ]

    return MaintenanceScheduleResponse(
        customer_id=context.customer_id,
        total_items=len(items),
        items=items,
    )


# ===== Supply Chain Vulnerability Endpoints =====

@router.post("/vulnerabilities/flag", response_model=VulnerabilityFlagResponse)
async def flag_vendor_vulnerability(
    request: VulnerabilityFlagRequest,
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """
    Flag a supply chain vulnerability affecting a vendor.

    All equipment from the affected vendor will be flagged.
    Requires WRITE access level.
    """
    try:
        affected_count = service.flag_vendor_vulnerability(
            vendor_id=request.vendor_id,
            cve_id=request.cve_id,
            cvss_score=request.cvss_score,
            description=request.description,
        )

        return VulnerabilityFlagResponse(
            vendor_id=request.vendor_id,
            cve_id=request.cve_id,
            affected_equipment_count=affected_count,
            message=f"Flagged {affected_count} equipment models as affected by {request.cve_id}",
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# ===== Maintenance Window Endpoints (Day 10) =====

@router.post("/maintenance-windows", response_model=MaintenanceWindowResponse, status_code=201)
async def create_maintenance_window(
    window_data: MaintenanceWindowCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """
    Create a new maintenance window.

    Requires WRITE access level.
    """
    try:
        window = MaintenanceWindow(
            window_id=window_data.window_id,
            name=window_data.name,
            customer_id=context.customer_id,
            window_type=MaintenanceWindowType(window_data.window_type),
            start_time=window_data.start_time,
            end_time=window_data.end_time,
            affected_equipment_ids=window_data.affected_equipment_ids,
            recurrence_pattern=window_data.recurrence_pattern,
            notes=window_data.notes,
        )
        window_id = service.create_maintenance_window(window)

        return MaintenanceWindowResponse(
            window_id=window.window_id,
            name=window.name,
            customer_id=window.customer_id,
            window_type=window.window_type.value,
            start_time=window.start_time,
            end_time=window.end_time,
            affected_equipment_ids=window.affected_equipment_ids,
            recurrence_pattern=window.recurrence_pattern,
            notes=window.notes,
            is_active=window.is_in_window(),
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/maintenance-windows/{window_id}", response_model=MaintenanceWindowResponse)
async def get_maintenance_window(
    window_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Get maintenance window by ID."""
    window = service.get_maintenance_window(window_id)
    if not window:
        raise HTTPException(status_code=404, detail=f"Maintenance window {window_id} not found")

    return MaintenanceWindowResponse(
        window_id=window.window_id,
        name=window.name,
        customer_id=window.customer_id,
        window_type=window.window_type.value if hasattr(window.window_type, 'value') else window.window_type,
        start_time=window.start_time,
        end_time=window.end_time,
        affected_equipment_ids=window.affected_equipment_ids,
        recurrence_pattern=window.recurrence_pattern,
        notes=window.notes,
        is_active=window.is_in_window(),
    )


@router.get("/maintenance-windows", response_model=MaintenanceWindowListResponse)
async def list_maintenance_windows(
    window_type: Optional[str] = Query(None, description="Filter by window type"),
    equipment_id: Optional[str] = Query(None, description="Filter by affected equipment"),
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """List maintenance windows with optional filters."""
    try:
        wt = MaintenanceWindowType(window_type) if window_type else None
        windows = service.list_maintenance_windows(
            window_type=wt,
            equipment_id=equipment_id,
            limit=limit,
        )

        window_responses = [
            MaintenanceWindowResponse(
                window_id=w.window_id,
                name=w.name,
                customer_id=w.customer_id,
                window_type=w.window_type.value if hasattr(w.window_type, 'value') else w.window_type,
                start_time=w.start_time,
                end_time=w.end_time,
                affected_equipment_ids=w.affected_equipment_ids,
                recurrence_pattern=w.recurrence_pattern,
                notes=w.notes,
                is_active=w.is_in_window(),
            )
            for w in windows
        ]

        return MaintenanceWindowListResponse(
            total_results=len(window_responses),
            customer_id=context.customer_id,
            windows=window_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/maintenance-windows/{window_id}")
async def delete_maintenance_window(
    window_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """
    Delete a maintenance window.

    Requires WRITE access level.
    """
    try:
        deleted = service.delete_maintenance_window(window_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Maintenance window {window_id} not found")

        return {"message": f"Maintenance window {window_id} deleted successfully"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/maintenance-windows/check-conflict", response_model=MaintenanceConflictResponse)
async def check_maintenance_conflict(
    proposed_start: datetime = Query(..., description="Proposed start time"),
    proposed_end: datetime = Query(..., description="Proposed end time"),
    equipment_ids: List[str] = Query(default=[], description="Equipment IDs to check"),
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Check for scheduling conflicts with existing maintenance windows."""
    conflicts = service.check_maintenance_conflict(
        proposed_start=proposed_start,
        proposed_end=proposed_end,
        equipment_ids=equipment_ids,
    )

    conflict_responses = [
        MaintenanceWindowResponse(
            window_id=w.window_id,
            name=w.name,
            customer_id=w.customer_id,
            window_type=w.window_type.value if hasattr(w.window_type, 'value') else w.window_type,
            start_time=w.start_time,
            end_time=w.end_time,
            affected_equipment_ids=w.affected_equipment_ids,
            recurrence_pattern=w.recurrence_pattern,
            notes=w.notes,
            is_active=w.is_in_window(),
        )
        for w in conflicts
    ]

    return MaintenanceConflictResponse(
        has_conflict=len(conflicts) > 0,
        conflicting_windows=conflict_responses,
    )


# ===== Predictive Maintenance Endpoints (Day 10-11) =====

@router.get("/predictive-maintenance/{equipment_id}", response_model=MaintenancePredictionListResponse)
async def predict_maintenance(
    equipment_id: str,
    days_ahead: int = Query(90, ge=1, le=365, description="Days ahead to predict"),
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Get maintenance predictions for specific equipment."""
    predictions = service.predict_maintenance(
        equipment_id=equipment_id,
        days_ahead=days_ahead,
    )

    if predictions is None:
        predictions = []

    prediction_responses = [
        MaintenancePredictionResponse(
            equipment_id=p.equipment_id,
            equipment_name=p.equipment_name,
            customer_id=p.customer_id,
            predicted_date=p.predicted_date,
            confidence_score=p.confidence_score,
            risk_level=p.risk_level,
            maintenance_type=p.maintenance_type,
            recommendation=p.recommendation,
        )
        for p in predictions
    ]

    return MaintenancePredictionListResponse(
        total_predictions=len(prediction_responses),
        customer_id=context.customer_id,
        predictions=prediction_responses,
    )


@router.get("/predictive-maintenance/forecast", response_model=MaintenanceForecastResponse)
async def get_maintenance_forecast(
    months_ahead: int = Query(6, ge=1, le=12, description="Months ahead for forecast"),
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Get comprehensive maintenance forecast."""
    forecast = service.get_maintenance_forecast(months_ahead=months_ahead)

    return MaintenanceForecastResponse(
        forecast_months=forecast.get("forecast_months", months_ahead),
        customer_id=context.customer_id,
        generated_at=forecast.get("generated_at", ""),
        monthly_breakdown=forecast.get("monthly_breakdown", []),
    )


# ===== Work Order Endpoints (Day 11) =====

@router.post("/work-orders", response_model=WorkOrderResponse, status_code=201)
async def create_work_order(
    work_order_data: WorkOrderCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """
    Create a new work order.

    Requires WRITE access level.
    """
    try:
        import uuid

        work_order = MaintenanceWorkOrder(
            work_order_id=work_order_data.work_order_id or f"WO-{uuid.uuid4().hex[:8].upper()}",
            customer_id=context.customer_id,
            equipment_id=work_order_data.equipment_id,
            equipment_name=work_order_data.equipment_name,
            title=work_order_data.title,
            description=work_order_data.description,
            priority=WorkOrderPriority(work_order_data.priority),
            status=WorkOrderStatus.PENDING,
            scheduled_start=work_order_data.scheduled_start,
            scheduled_end=work_order_data.scheduled_end,
            assigned_technician=work_order_data.assigned_technician,
            maintenance_window_id=work_order_data.maintenance_window_id,
        )
        wo_id = service.create_work_order(work_order)

        return WorkOrderResponse(
            work_order_id=work_order.work_order_id,
            customer_id=work_order.customer_id,
            equipment_id=work_order.equipment_id,
            equipment_name=work_order.equipment_name,
            title=work_order.title,
            description=work_order.description,
            priority=work_order.priority.value,
            status=work_order.status.value,
            scheduled_start=work_order.scheduled_start,
            scheduled_end=work_order.scheduled_end,
            actual_start=work_order.actual_start,
            actual_end=work_order.actual_end,
            assigned_technician=work_order.assigned_technician,
            maintenance_window_id=work_order.maintenance_window_id,
            notes=work_order.notes,
            is_overdue=work_order.is_overdue(),
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/work-orders/{work_order_id}", response_model=WorkOrderResponse)
async def get_work_order(
    work_order_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Get work order by ID."""
    wo = service.get_work_order(work_order_id)
    if not wo:
        raise HTTPException(status_code=404, detail=f"Work order {work_order_id} not found")

    return WorkOrderResponse(
        work_order_id=wo.work_order_id,
        customer_id=wo.customer_id,
        equipment_id=wo.equipment_id,
        equipment_name=wo.equipment_name,
        title=wo.title,
        description=wo.description,
        priority=wo.priority.value if hasattr(wo.priority, 'value') else wo.priority,
        status=wo.status.value if hasattr(wo.status, 'value') else wo.status,
        scheduled_start=wo.scheduled_start,
        scheduled_end=wo.scheduled_end,
        actual_start=wo.actual_start,
        actual_end=wo.actual_end,
        assigned_technician=wo.assigned_technician,
        maintenance_window_id=wo.maintenance_window_id,
        notes=wo.notes,
        is_overdue=wo.is_overdue(),
    )


@router.get("/work-orders", response_model=WorkOrderListResponse)
async def list_work_orders(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    equipment_id: Optional[str] = Query(None, description="Filter by equipment"),
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """List work orders with optional filters."""
    try:
        wo_status = WorkOrderStatus(status) if status else None
        wo_priority = WorkOrderPriority(priority) if priority else None

        work_orders = service.list_work_orders(
            status=wo_status,
            priority=wo_priority,
            equipment_id=equipment_id,
            limit=limit,
        )

        wo_responses = [
            WorkOrderResponse(
                work_order_id=wo.work_order_id,
                customer_id=wo.customer_id,
                equipment_id=wo.equipment_id,
                equipment_name=wo.equipment_name,
                title=wo.title,
                description=wo.description,
                priority=wo.priority.value if hasattr(wo.priority, 'value') else wo.priority,
                status=wo.status.value if hasattr(wo.status, 'value') else wo.status,
                scheduled_start=wo.scheduled_start,
                scheduled_end=wo.scheduled_end,
                actual_start=wo.actual_start,
                actual_end=wo.actual_end,
                assigned_technician=wo.assigned_technician,
                maintenance_window_id=wo.maintenance_window_id,
                notes=wo.notes,
                is_overdue=wo.is_overdue(),
            )
            for wo in work_orders
        ]

        return WorkOrderListResponse(
            total_results=len(wo_responses),
            customer_id=context.customer_id,
            work_orders=wo_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/work-orders/{work_order_id}/status", response_model=WorkOrderResponse)
async def update_work_order_status(
    work_order_id: str,
    status_update: WorkOrderStatusUpdate,
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """
    Update work order status.

    Requires WRITE access level.
    """
    try:
        new_status = WorkOrderStatus(status_update.status)
        updated = service.update_work_order_status(
            work_order_id=work_order_id,
            new_status=new_status,
            notes=status_update.notes,
        )

        if not updated:
            raise HTTPException(status_code=404, detail=f"Work order {work_order_id} not found")

        # Fetch updated work order
        wo = service.get_work_order(work_order_id)

        return WorkOrderResponse(
            work_order_id=wo.work_order_id,
            customer_id=wo.customer_id,
            equipment_id=wo.equipment_id,
            equipment_name=wo.equipment_name,
            title=wo.title,
            description=wo.description,
            priority=wo.priority.value if hasattr(wo.priority, 'value') else wo.priority,
            status=wo.status.value if hasattr(wo.status, 'value') else wo.status,
            scheduled_start=wo.scheduled_start,
            scheduled_end=wo.scheduled_end,
            actual_start=wo.actual_start,
            actual_end=wo.actual_end,
            assigned_technician=wo.assigned_technician,
            maintenance_window_id=wo.maintenance_window_id,
            notes=wo.notes,
            is_overdue=wo.is_overdue(),
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/work-orders/summary", response_model=WorkOrderSummaryResponse)
async def get_work_order_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: VendorEquipmentService = Depends(get_service),
):
    """Get work order summary with status and priority breakdowns."""
    summary = service.get_work_order_summary()

    return WorkOrderSummaryResponse(
        customer_id=context.customer_id,
        total=summary.get("total", 0),
        status_breakdown=summary.get("status_breakdown", {}),
        priority_breakdown=summary.get("priority_breakdown", {}),
        overdue_count=summary.get("overdue_count", 0),
    )