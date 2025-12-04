"""
Compliance Mapping API Router
==============================

FastAPI router for E07: Compliance Framework Mapping.
Provides REST endpoints for controls, framework mappings, assessments,
evidence management, gap analysis, and compliance dashboards.

Version: 1.0.0
Created: 2025-12-04
"""

from datetime import date, datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Header, Depends, UploadFile, File
from pydantic import BaseModel, Field
import logging

from ..customer_isolation import (
    CustomerContext,
    CustomerContextManager,
    CustomerAccessLevel,
)
from .compliance_service import (
    ComplianceService,
    ControlSearchRequest,
    AssessmentSearchRequest,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/compliance", tags=["compliance"])


# =============================================================================
# Pydantic Request/Response Models
# =============================================================================


# ===== Control Models =====

class ControlCreate(BaseModel):
    """Request model for control creation."""
    control_id: str = Field(..., description="Unique control identifier")
    control_number: str = Field(..., description="Control number (e.g., AC-2)")
    framework: str = Field(..., description="Framework: nist_800_53, iso27001, cis, pci_dss, sox, hipaa, gdpr")
    title: str = Field(..., description="Control title")
    description: str = Field(..., description="Control description")
    control_family: str = Field(..., description="Control family/category")
    priority: str = Field("medium", description="Priority: low, medium, high, critical")
    implementation_status: str = Field("not_started", description="Status: not_started, planned, in_progress, implemented, verified")
    control_type: str = Field("preventive", description="Type: preventive, detective, corrective, directive")
    automated: bool = Field(False, description="Is control automated?")
    responsible_party: Optional[str] = Field(None, description="Responsible party/role")
    review_frequency: Optional[str] = Field(None, description="Review frequency (days)")


class ControlResponse(BaseModel):
    """Response model for control data."""
    control_id: str
    control_number: str
    customer_id: str
    framework: str
    title: str
    control_family: str
    priority: str
    implementation_status: str
    control_type: str
    automated: bool
    responsible_party: Optional[str]
    last_assessment: Optional[date]


class ControlSearchResponse(BaseModel):
    """Response for control search results."""
    total_results: int
    customer_id: str
    results: List[ControlResponse]


# ===== Framework Mapping Models =====

class FrameworkMappingCreate(BaseModel):
    """Request model for framework mapping creation."""
    mapping_id: str = Field(..., description="Unique mapping identifier")
    source_framework: str = Field(..., description="Source framework")
    source_control_id: str = Field(..., description="Source control ID")
    target_framework: str = Field(..., description="Target framework")
    target_control_id: str = Field(..., description="Target control ID")
    relationship_type: str = Field("equivalent", description="Type: equivalent, similar, related, complementary")
    confidence: int = Field(80, ge=0, le=100, description="Mapping confidence 0-100")
    notes: Optional[str] = Field(None, description="Mapping notes")


class FrameworkMappingResponse(BaseModel):
    """Response model for framework mapping."""
    mapping_id: str
    customer_id: str
    source_framework: str
    source_control_id: str
    target_framework: str
    target_control_id: str
    relationship_type: str
    confidence: int


class MappingSearchResponse(BaseModel):
    """Response for mapping search results."""
    total_results: int
    customer_id: str
    results: List[FrameworkMappingResponse]


class AutoMapRequest(BaseModel):
    """Request for automatic mapping generation."""
    source_framework: str = Field(..., description="Source framework")
    target_framework: str = Field(..., description="Target framework")
    min_confidence: int = Field(60, ge=0, le=100, description="Minimum confidence threshold")


# ===== Assessment Models =====

class AssessmentCreate(BaseModel):
    """Request model for assessment creation."""
    assessment_id: str = Field(..., description="Unique assessment identifier")
    control_id: str = Field(..., description="Control being assessed")
    assessment_date: date = Field(..., description="Assessment date")
    assessor: str = Field(..., description="Assessor name/ID")
    status: str = Field("in_progress", description="Status: in_progress, completed, failed")
    compliance_score: int = Field(0, ge=0, le=100, description="Compliance score 0-100")
    findings: List[str] = Field(default_factory=list, description="Assessment findings")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    evidence_ids: List[str] = Field(default_factory=list, description="Evidence document IDs")


class AssessmentResponse(BaseModel):
    """Response model for assessment data."""
    assessment_id: str
    customer_id: str
    control_id: str
    assessment_date: date
    assessor: str
    status: str
    compliance_score: int
    findings_count: int
    evidence_count: int


class AssessmentSearchResponse(BaseModel):
    """Response for assessment search results."""
    total_results: int
    customer_id: str
    results: List[AssessmentResponse]


# ===== Evidence Models =====

class EvidenceCreate(BaseModel):
    """Request model for evidence upload."""
    evidence_id: str = Field(..., description="Unique evidence identifier")
    control_id: str = Field(..., description="Associated control ID")
    evidence_type: str = Field(..., description="Type: document, screenshot, log, report, certification")
    title: str = Field(..., description="Evidence title")
    description: Optional[str] = Field(None, description="Evidence description")
    file_path: Optional[str] = Field(None, description="File storage path")
    collection_date: date = Field(..., description="Collection date")
    expiration_date: Optional[date] = Field(None, description="Expiration date")


class EvidenceResponse(BaseModel):
    """Response model for evidence data."""
    evidence_id: str
    customer_id: str
    control_id: str
    evidence_type: str
    title: str
    collection_date: date
    expiration_date: Optional[date]
    is_expired: bool


class EvidenceSearchResponse(BaseModel):
    """Response for evidence search results."""
    total_results: int
    customer_id: str
    results: List[EvidenceResponse]


# ===== Gap Models =====

class GapCreate(BaseModel):
    """Request model for gap creation."""
    gap_id: str = Field(..., description="Unique gap identifier")
    control_id: str = Field(..., description="Control with gap")
    gap_type: str = Field(..., description="Type: implementation, documentation, testing, process")
    severity: str = Field("medium", description="Severity: low, medium, high, critical")
    description: str = Field(..., description="Gap description")
    impact: str = Field(..., description="Business impact")
    remediation_plan: Optional[str] = Field(None, description="Remediation plan")
    target_date: Optional[date] = Field(None, description="Target remediation date")
    status: str = Field("open", description="Status: open, in_progress, resolved, accepted")


class GapResponse(BaseModel):
    """Response model for gap data."""
    gap_id: str
    customer_id: str
    control_id: str
    gap_type: str
    severity: str
    impact: str
    status: str
    target_date: Optional[date]


class GapSearchResponse(BaseModel):
    """Response for gap search results."""
    total_results: int
    customer_id: str
    results: List[GapResponse]


class RemediationUpdate(BaseModel):
    """Request model for gap remediation update."""
    status: str = Field(..., description="New status: in_progress, resolved, accepted")
    remediation_notes: str = Field(..., description="Remediation notes")
    completion_date: Optional[date] = Field(None, description="Completion date")
    evidence_ids: List[str] = Field(default_factory=list, description="Supporting evidence IDs")


# ===== Dashboard Models =====

class ComplianceSummaryResponse(BaseModel):
    """Response for compliance dashboard summary."""
    customer_id: str
    total_controls: int
    implemented_controls: int
    in_progress_controls: int
    not_started_controls: int
    average_compliance_score: float
    total_assessments: int
    total_gaps: int
    critical_gaps: int
    framework_breakdown: dict


class CompliancePostureResponse(BaseModel):
    """Response for compliance posture analysis."""
    customer_id: str
    overall_posture: str
    posture_score: float
    risk_level: str
    framework_compliance: dict
    top_gaps: List[dict]
    recommendations: List[str]
    trend: str


# =============================================================================
# Dependencies
# =============================================================================


def get_service() -> ComplianceService:
    """Get compliance service instance."""
    return ComplianceService()


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


# =============================================================================
# Controls Management Endpoints
# =============================================================================


@router.post("/controls", response_model=ControlResponse, status_code=201)
async def create_control(
    control_data: ControlCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """
    Create a new compliance control.

    Requires WRITE access level.
    """
    try:
        from .compliance_models import ComplianceControl, ControlPriority, ImplementationStatus, ControlType

        control = ComplianceControl(
            control_id=control_data.control_id,
            control_number=control_data.control_number,
            customer_id=context.customer_id,
            framework=control_data.framework,
            title=control_data.title,
            description=control_data.description,
            control_family=control_data.control_family,
            priority=ControlPriority(control_data.priority),
            implementation_status=ImplementationStatus(control_data.implementation_status),
            control_type=ControlType(control_data.control_type),
            automated=control_data.automated,
            responsible_party=control_data.responsible_party,
            review_frequency=control_data.review_frequency,
        )
        created = service.create_control(control)

        return ControlResponse(
            control_id=created.control_id,
            control_number=created.control_number,
            customer_id=created.customer_id,
            framework=created.framework,
            title=created.title,
            control_family=created.control_family,
            priority=created.priority.value,
            implementation_status=created.implementation_status.value,
            control_type=created.control_type.value,
            automated=created.automated,
            responsible_party=created.responsible_party,
            last_assessment=created.last_assessment,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/controls/{control_id}", response_model=ControlResponse)
async def get_control(
    control_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """Get control by ID with customer isolation."""
    control = service.get_control(control_id)
    if not control:
        raise HTTPException(status_code=404, detail=f"Control {control_id} not found")

    return ControlResponse(
        control_id=control.control_id,
        control_number=control.control_number,
        customer_id=control.customer_id,
        framework=control.framework,
        title=control.title,
        control_family=control.control_family,
        priority=control.priority.value if hasattr(control.priority, 'value') else control.priority,
        implementation_status=control.implementation_status.value if hasattr(control.implementation_status, 'value') else control.implementation_status,
        control_type=control.control_type.value if hasattr(control.control_type, 'value') else control.control_type,
        automated=control.automated,
        responsible_party=control.responsible_party,
        last_assessment=control.last_assessment,
    )


@router.put("/controls/{control_id}", response_model=ControlResponse)
async def update_control(
    control_id: str,
    control_data: ControlCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """
    Update an existing control.

    Requires WRITE access level.
    """
    try:
        from .compliance_models import ComplianceControl, ControlPriority, ImplementationStatus, ControlType

        control = ComplianceControl(
            control_id=control_id,
            control_number=control_data.control_number,
            customer_id=context.customer_id,
            framework=control_data.framework,
            title=control_data.title,
            description=control_data.description,
            control_family=control_data.control_family,
            priority=ControlPriority(control_data.priority),
            implementation_status=ImplementationStatus(control_data.implementation_status),
            control_type=ControlType(control_data.control_type),
            automated=control_data.automated,
            responsible_party=control_data.responsible_party,
            review_frequency=control_data.review_frequency,
        )
        updated = service.update_control(control)

        return ControlResponse(
            control_id=updated.control_id,
            control_number=updated.control_number,
            customer_id=updated.customer_id,
            framework=updated.framework,
            title=updated.title,
            control_family=updated.control_family,
            priority=updated.priority.value,
            implementation_status=updated.implementation_status.value,
            control_type=updated.control_type.value,
            automated=updated.automated,
            responsible_party=updated.responsible_party,
            last_assessment=updated.last_assessment,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/controls/{control_id}", status_code=204)
async def delete_control(
    control_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """
    Delete a control.

    Requires WRITE access level.
    """
    try:
        success = service.delete_control(control_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Control {control_id} not found")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/controls", response_model=ControlSearchResponse)
async def list_controls(
    framework: Optional[str] = Query(None, description="Filter by framework"),
    control_family: Optional[str] = Query(None, description="Filter by control family"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    implementation_status: Optional[str] = Query(None, description="Filter by implementation status"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results"),
    include_system: bool = Query(True, description="Include SYSTEM controls"),
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """List controls with optional filters."""
    try:
        request = ControlSearchRequest(
            query=None,
            customer_id=context.customer_id,
            framework=framework,
            control_family=control_family,
            priority=priority,
            implementation_status=implementation_status,
            limit=limit,
            include_system=include_system,
        )
        results = service.search_controls(request)

        control_responses = [
            ControlResponse(
                control_id=r.control.control_id,
                control_number=r.control.control_number,
                customer_id=r.control.customer_id,
                framework=r.control.framework,
                title=r.control.title,
                control_family=r.control.control_family,
                priority=r.control.priority.value if hasattr(r.control.priority, 'value') else r.control.priority,
                implementation_status=r.control.implementation_status.value if hasattr(r.control.implementation_status, 'value') else r.control.implementation_status,
                control_type=r.control.control_type.value if hasattr(r.control.control_type, 'value') else r.control.control_type,
                automated=r.control.automated,
                responsible_party=r.control.responsible_party,
                last_assessment=r.control.last_assessment,
            )
            for r in results
        ]

        return ControlSearchResponse(
            total_results=len(control_responses),
            customer_id=context.customer_id,
            results=control_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/controls/by-framework/{framework}", response_model=ControlSearchResponse)
async def get_controls_by_framework(
    framework: str,
    limit: int = Query(100, ge=1, le=200, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """Get controls for a specific framework."""
    results = service.get_controls_by_framework(framework, limit)

    control_responses = [
        ControlResponse(
            control_id=r.control.control_id,
            control_number=r.control.control_number,
            customer_id=r.control.customer_id,
            framework=r.control.framework,
            title=r.control.title,
            control_family=r.control.control_family,
            priority=r.control.priority.value if hasattr(r.control.priority, 'value') else r.control.priority,
            implementation_status=r.control.implementation_status.value if hasattr(r.control.implementation_status, 'value') else r.control.implementation_status,
            control_type=r.control.control_type.value if hasattr(r.control.control_type, 'value') else r.control.control_type,
            automated=r.control.automated,
            responsible_party=r.control.responsible_party,
            last_assessment=r.control.last_assessment,
        )
        for r in results
    ]

    return ControlSearchResponse(
        total_results=len(control_responses),
        customer_id=context.customer_id,
        results=control_responses,
    )


@router.post("/controls/search", response_model=ControlSearchResponse)
async def search_controls_semantic(
    query: str = Query(..., description="Semantic search query"),
    framework: Optional[str] = Query(None, description="Filter by framework"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """Semantic search controls."""
    try:
        request = ControlSearchRequest(
            query=query,
            customer_id=context.customer_id,
            framework=framework,
            limit=limit,
            include_system=True,
        )
        results = service.search_controls(request)

        control_responses = [
            ControlResponse(
                control_id=r.control.control_id,
                control_number=r.control.control_number,
                customer_id=r.control.customer_id,
                framework=r.control.framework,
                title=r.control.title,
                control_family=r.control.control_family,
                priority=r.control.priority.value if hasattr(r.control.priority, 'value') else r.control.priority,
                implementation_status=r.control.implementation_status.value if hasattr(r.control.implementation_status, 'value') else r.control.implementation_status,
                control_type=r.control.control_type.value if hasattr(r.control.control_type, 'value') else r.control.control_type,
                automated=r.control.automated,
                responsible_party=r.control.responsible_party,
                last_assessment=r.control.last_assessment,
            )
            for r in results
        ]

        return ControlSearchResponse(
            total_results=len(control_responses),
            customer_id=context.customer_id,
            results=control_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =============================================================================
# Framework Mappings Endpoints
# =============================================================================


@router.post("/mappings", response_model=FrameworkMappingResponse, status_code=201)
async def create_mapping(
    mapping_data: FrameworkMappingCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """
    Create a new framework mapping.

    Requires WRITE access level.
    """
    try:
        from .compliance_models import FrameworkMapping, RelationshipType

        mapping = FrameworkMapping(
            mapping_id=mapping_data.mapping_id,
            customer_id=context.customer_id,
            source_framework=mapping_data.source_framework,
            source_control_id=mapping_data.source_control_id,
            target_framework=mapping_data.target_framework,
            target_control_id=mapping_data.target_control_id,
            relationship_type=RelationshipType(mapping_data.relationship_type),
            confidence=mapping_data.confidence,
            notes=mapping_data.notes,
        )
        created = service.create_mapping(mapping)

        return FrameworkMappingResponse(
            mapping_id=created.mapping_id,
            customer_id=created.customer_id,
            source_framework=created.source_framework,
            source_control_id=created.source_control_id,
            target_framework=created.target_framework,
            target_control_id=created.target_control_id,
            relationship_type=created.relationship_type.value,
            confidence=created.confidence,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/mappings/{mapping_id}", response_model=FrameworkMappingResponse)
async def get_mapping(
    mapping_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """Get mapping by ID with customer isolation."""
    mapping = service.get_mapping(mapping_id)
    if not mapping:
        raise HTTPException(status_code=404, detail=f"Mapping {mapping_id} not found")

    return FrameworkMappingResponse(
        mapping_id=mapping.mapping_id,
        customer_id=mapping.customer_id,
        source_framework=mapping.source_framework,
        source_control_id=mapping.source_control_id,
        target_framework=mapping.target_framework,
        target_control_id=mapping.target_control_id,
        relationship_type=mapping.relationship_type.value if hasattr(mapping.relationship_type, 'value') else mapping.relationship_type,
        confidence=mapping.confidence,
    )


@router.get("/mappings/between/{source}/{target}", response_model=MappingSearchResponse)
async def get_cross_framework_mappings(
    source: str,
    target: str,
    min_confidence: int = Query(0, ge=0, le=100, description="Minimum confidence"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """Get cross-framework mappings."""
    mappings = service.get_cross_framework_mappings(source, target, min_confidence, limit)

    mapping_responses = [
        FrameworkMappingResponse(
            mapping_id=m.mapping_id,
            customer_id=m.customer_id,
            source_framework=m.source_framework,
            source_control_id=m.source_control_id,
            target_framework=m.target_framework,
            target_control_id=m.target_control_id,
            relationship_type=m.relationship_type.value if hasattr(m.relationship_type, 'value') else m.relationship_type,
            confidence=m.confidence,
        )
        for m in mappings
    ]

    return MappingSearchResponse(
        total_results=len(mapping_responses),
        customer_id=context.customer_id,
        results=mapping_responses,
    )


@router.get("/mappings/by-control/{control_id}", response_model=MappingSearchResponse)
async def get_mappings_for_control(
    control_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """Get all mappings for a control."""
    mappings = service.get_mappings_for_control(control_id)

    mapping_responses = [
        FrameworkMappingResponse(
            mapping_id=m.mapping_id,
            customer_id=m.customer_id,
            source_framework=m.source_framework,
            source_control_id=m.source_control_id,
            target_framework=m.target_framework,
            target_control_id=m.target_control_id,
            relationship_type=m.relationship_type.value if hasattr(m.relationship_type, 'value') else m.relationship_type,
            confidence=m.confidence,
        )
        for m in mappings
    ]

    return MappingSearchResponse(
        total_results=len(mapping_responses),
        customer_id=context.customer_id,
        results=mapping_responses,
    )


@router.post("/mappings/auto-map")
async def auto_generate_mappings(
    request: AutoMapRequest,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """
    Auto-generate framework mappings using semantic similarity.

    Requires WRITE access level.
    """
    try:
        result = service.auto_generate_mappings(
            request.source_framework,
            request.target_framework,
            request.min_confidence,
        )
        return {
            "source_framework": request.source_framework,
            "target_framework": request.target_framework,
            "mappings_created": result.get("mappings_created", 0),
            "average_confidence": result.get("average_confidence", 0.0),
            "mappings": result.get("mappings", []),
        }
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =============================================================================
# Assessments Endpoints
# =============================================================================


@router.post("/assessments", response_model=AssessmentResponse, status_code=201)
async def create_assessment(
    assessment_data: AssessmentCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """
    Create a new compliance assessment.

    Requires WRITE access level.
    """
    try:
        from .compliance_models import ComplianceAssessment, AssessmentStatus

        assessment = ComplianceAssessment(
            assessment_id=assessment_data.assessment_id,
            customer_id=context.customer_id,
            control_id=assessment_data.control_id,
            assessment_date=assessment_data.assessment_date,
            assessor=assessment_data.assessor,
            status=AssessmentStatus(assessment_data.status),
            compliance_score=assessment_data.compliance_score,
            findings=assessment_data.findings,
            recommendations=assessment_data.recommendations,
            evidence_ids=assessment_data.evidence_ids,
        )
        created = service.create_assessment(assessment)

        return AssessmentResponse(
            assessment_id=created.assessment_id,
            customer_id=created.customer_id,
            control_id=created.control_id,
            assessment_date=created.assessment_date,
            assessor=created.assessor,
            status=created.status.value,
            compliance_score=created.compliance_score,
            findings_count=len(created.findings),
            evidence_count=len(created.evidence_ids),
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/assessments/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(
    assessment_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """Get assessment by ID with customer isolation."""
    assessment = service.get_assessment(assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail=f"Assessment {assessment_id} not found")

    return AssessmentResponse(
        assessment_id=assessment.assessment_id,
        customer_id=assessment.customer_id,
        control_id=assessment.control_id,
        assessment_date=assessment.assessment_date,
        assessor=assessment.assessor,
        status=assessment.status.value if hasattr(assessment.status, 'value') else assessment.status,
        compliance_score=assessment.compliance_score,
        findings_count=len(assessment.findings),
        evidence_count=len(assessment.evidence_ids),
    )


@router.put("/assessments/{assessment_id}", response_model=AssessmentResponse)
async def update_assessment(
    assessment_id: str,
    assessment_data: AssessmentCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """
    Update an existing assessment.

    Requires WRITE access level.
    """
    try:
        from .compliance_models import ComplianceAssessment, AssessmentStatus

        assessment = ComplianceAssessment(
            assessment_id=assessment_id,
            customer_id=context.customer_id,
            control_id=assessment_data.control_id,
            assessment_date=assessment_data.assessment_date,
            assessor=assessment_data.assessor,
            status=AssessmentStatus(assessment_data.status),
            compliance_score=assessment_data.compliance_score,
            findings=assessment_data.findings,
            recommendations=assessment_data.recommendations,
            evidence_ids=assessment_data.evidence_ids,
        )
        updated = service.update_assessment(assessment)

        return AssessmentResponse(
            assessment_id=updated.assessment_id,
            customer_id=updated.customer_id,
            control_id=updated.control_id,
            assessment_date=updated.assessment_date,
            assessor=updated.assessor,
            status=updated.status.value,
            compliance_score=updated.compliance_score,
            findings_count=len(updated.findings),
            evidence_count=len(updated.evidence_ids),
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/assessments", response_model=AssessmentSearchResponse)
async def list_assessments(
    control_id: Optional[str] = Query(None, description="Filter by control"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """List assessments with optional filters."""
    try:
        request = AssessmentSearchRequest(
            customer_id=context.customer_id,
            control_id=control_id,
            status=status,
            limit=limit,
        )
        results = service.search_assessments(request)

        assessment_responses = [
            AssessmentResponse(
                assessment_id=r.assessment.assessment_id,
                customer_id=r.assessment.customer_id,
                control_id=r.assessment.control_id,
                assessment_date=r.assessment.assessment_date,
                assessor=r.assessment.assessor,
                status=r.assessment.status.value if hasattr(r.assessment.status, 'value') else r.assessment.status,
                compliance_score=r.assessment.compliance_score,
                findings_count=len(r.assessment.findings),
                evidence_count=len(r.assessment.evidence_ids),
            )
            for r in results
        ]

        return AssessmentSearchResponse(
            total_results=len(assessment_responses),
            customer_id=context.customer_id,
            results=assessment_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/assessments/by-framework/{framework}", response_model=AssessmentSearchResponse)
async def get_assessments_by_framework(
    framework: str,
    limit: int = Query(100, ge=1, le=200, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """Get assessments for a specific framework."""
    results = service.get_assessments_by_framework(framework, limit)

    assessment_responses = [
        AssessmentResponse(
            assessment_id=r.assessment.assessment_id,
            customer_id=r.assessment.customer_id,
            control_id=r.assessment.control_id,
            assessment_date=r.assessment.assessment_date,
            assessor=r.assessment.assessor,
            status=r.assessment.status.value if hasattr(r.assessment.status, 'value') else r.assessment.status,
            compliance_score=r.assessment.compliance_score,
            findings_count=len(r.assessment.findings),
            evidence_count=len(r.assessment.evidence_ids),
        )
        for r in results
    ]

    return AssessmentSearchResponse(
        total_results=len(assessment_responses),
        customer_id=context.customer_id,
        results=assessment_responses,
    )


@router.post("/assessments/{assessment_id}/complete")
async def complete_assessment(
    assessment_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """
    Mark an assessment as completed.

    Requires WRITE access level.
    """
    try:
        success = service.complete_assessment(assessment_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Assessment {assessment_id} not found")

        return {"assessment_id": assessment_id, "status": "completed", "message": "Assessment marked as completed"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# =============================================================================
# Evidence Endpoints
# =============================================================================


@router.post("/evidence", response_model=EvidenceResponse, status_code=201)
async def upload_evidence(
    evidence_data: EvidenceCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """
    Upload compliance evidence.

    Requires WRITE access level.
    """
    try:
        from .compliance_models import ComplianceEvidence, EvidenceType

        evidence = ComplianceEvidence(
            evidence_id=evidence_data.evidence_id,
            customer_id=context.customer_id,
            control_id=evidence_data.control_id,
            evidence_type=EvidenceType(evidence_data.evidence_type),
            title=evidence_data.title,
            description=evidence_data.description,
            file_path=evidence_data.file_path,
            collection_date=evidence_data.collection_date,
            expiration_date=evidence_data.expiration_date,
        )
        created = service.create_evidence(evidence)

        return EvidenceResponse(
            evidence_id=created.evidence_id,
            customer_id=created.customer_id,
            control_id=created.control_id,
            evidence_type=created.evidence_type.value,
            title=created.title,
            collection_date=created.collection_date,
            expiration_date=created.expiration_date,
            is_expired=created.is_expired,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/evidence/{evidence_id}", response_model=EvidenceResponse)
async def get_evidence(
    evidence_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """Get evidence by ID with customer isolation."""
    evidence = service.get_evidence(evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail=f"Evidence {evidence_id} not found")

    return EvidenceResponse(
        evidence_id=evidence.evidence_id,
        customer_id=evidence.customer_id,
        control_id=evidence.control_id,
        evidence_type=evidence.evidence_type.value if hasattr(evidence.evidence_type, 'value') else evidence.evidence_type,
        title=evidence.title,
        collection_date=evidence.collection_date,
        expiration_date=evidence.expiration_date,
        is_expired=evidence.is_expired,
    )


@router.get("/evidence/by-control/{control_id}", response_model=EvidenceSearchResponse)
async def get_evidence_for_control(
    control_id: str,
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """Get evidence for a specific control."""
    evidence_list = service.get_evidence_for_control(control_id, limit)

    evidence_responses = [
        EvidenceResponse(
            evidence_id=e.evidence_id,
            customer_id=e.customer_id,
            control_id=e.control_id,
            evidence_type=e.evidence_type.value if hasattr(e.evidence_type, 'value') else e.evidence_type,
            title=e.title,
            collection_date=e.collection_date,
            expiration_date=e.expiration_date,
            is_expired=e.is_expired,
        )
        for e in evidence_list
    ]

    return EvidenceSearchResponse(
        total_results=len(evidence_responses),
        customer_id=context.customer_id,
        results=evidence_responses,
    )


@router.delete("/evidence/{evidence_id}", status_code=204)
async def delete_evidence(
    evidence_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """
    Delete evidence.

    Requires WRITE access level.
    """
    try:
        success = service.delete_evidence(evidence_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Evidence {evidence_id} not found")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# =============================================================================
# Gaps Endpoints
# =============================================================================


@router.post("/gaps", response_model=GapResponse, status_code=201)
async def create_gap(
    gap_data: GapCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """
    Create a new compliance gap.

    Requires WRITE access level.
    """
    try:
        from .compliance_models import ComplianceGap, GapSeverity, GapStatus

        gap = ComplianceGap(
            gap_id=gap_data.gap_id,
            customer_id=context.customer_id,
            control_id=gap_data.control_id,
            gap_type=gap_data.gap_type,
            severity=GapSeverity(gap_data.severity),
            description=gap_data.description,
            impact=gap_data.impact,
            remediation_plan=gap_data.remediation_plan,
            target_date=gap_data.target_date,
            status=GapStatus(gap_data.status),
        )
        created = service.create_gap(gap)

        return GapResponse(
            gap_id=created.gap_id,
            customer_id=created.customer_id,
            control_id=created.control_id,
            gap_type=created.gap_type,
            severity=created.severity.value,
            impact=created.impact,
            status=created.status.value,
            target_date=created.target_date,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/gaps", response_model=GapSearchResponse)
async def list_gaps(
    control_id: Optional[str] = Query(None, description="Filter by control"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """List gaps with optional filters."""
    gaps = service.search_gaps(
        control_id=control_id,
        severity=severity,
        status=status,
        limit=limit,
    )

    gap_responses = [
        GapResponse(
            gap_id=g.gap_id,
            customer_id=g.customer_id,
            control_id=g.control_id,
            gap_type=g.gap_type,
            severity=g.severity.value if hasattr(g.severity, 'value') else g.severity,
            impact=g.impact,
            status=g.status.value if hasattr(g.status, 'value') else g.status,
            target_date=g.target_date,
        )
        for g in gaps
    ]

    return GapSearchResponse(
        total_results=len(gap_responses),
        customer_id=context.customer_id,
        results=gap_responses,
    )


@router.get("/gaps/by-framework/{framework}", response_model=GapSearchResponse)
async def get_gaps_by_framework(
    framework: str,
    limit: int = Query(100, ge=1, le=200, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """Get gaps for a specific framework."""
    gaps = service.get_gaps_by_framework(framework, limit)

    gap_responses = [
        GapResponse(
            gap_id=g.gap_id,
            customer_id=g.customer_id,
            control_id=g.control_id,
            gap_type=g.gap_type,
            severity=g.severity.value if hasattr(g.severity, 'value') else g.severity,
            impact=g.impact,
            status=g.status.value if hasattr(g.status, 'value') else g.status,
            target_date=g.target_date,
        )
        for g in gaps
    ]

    return GapSearchResponse(
        total_results=len(gap_responses),
        customer_id=context.customer_id,
        results=gap_responses,
    )


@router.put("/gaps/{gap_id}/remediate")
async def update_gap_remediation(
    gap_id: str,
    remediation: RemediationUpdate,
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """
    Update gap remediation status.

    Requires WRITE access level.
    """
    try:
        success = service.update_gap_remediation(
            gap_id,
            remediation.status,
            remediation.remediation_notes,
            remediation.completion_date,
            remediation.evidence_ids,
        )
        if not success:
            raise HTTPException(status_code=404, detail=f"Gap {gap_id} not found")

        return {
            "gap_id": gap_id,
            "status": remediation.status,
            "message": "Gap remediation updated successfully",
        }
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# =============================================================================
# Dashboard Endpoints
# =============================================================================


@router.get("/dashboard/summary", response_model=ComplianceSummaryResponse)
async def get_compliance_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """Get compliance dashboard summary."""
    summary = service.get_dashboard_summary()

    return ComplianceSummaryResponse(
        customer_id=context.customer_id,
        total_controls=summary.get("total_controls", 0),
        implemented_controls=summary.get("implemented_controls", 0),
        in_progress_controls=summary.get("in_progress_controls", 0),
        not_started_controls=summary.get("not_started_controls", 0),
        average_compliance_score=summary.get("average_compliance_score", 0.0),
        total_assessments=summary.get("total_assessments", 0),
        total_gaps=summary.get("total_gaps", 0),
        critical_gaps=summary.get("critical_gaps", 0),
        framework_breakdown=summary.get("framework_breakdown", {}),
    )


@router.get("/dashboard/posture", response_model=CompliancePostureResponse)
async def get_compliance_posture(
    context: CustomerContext = Depends(require_customer_context),
    service: ComplianceService = Depends(get_service),
):
    """Get compliance posture analysis."""
    posture = service.get_compliance_posture()

    return CompliancePostureResponse(
        customer_id=context.customer_id,
        overall_posture=posture.get("overall_posture", "unknown"),
        posture_score=posture.get("posture_score", 0.0),
        risk_level=posture.get("risk_level", "unknown"),
        framework_compliance=posture.get("framework_compliance", {}),
        top_gaps=posture.get("top_gaps", []),
        recommendations=posture.get("recommendations", []),
        trend=posture.get("trend", "stable"),
    )
