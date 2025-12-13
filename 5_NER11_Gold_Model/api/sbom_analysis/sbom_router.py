"""
SBOM Analysis API Router
========================

FastAPI router for E03: SBOM Dependency & Vulnerability Tracking.
Provides REST endpoints for SBOM, component, and vulnerability operations.

Version: 1.0.0
Created: 2025-12-04
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
from .sbom_models import (
    SBOMFormat,
    ComponentType,
    LicenseType,
    LicenseRisk,
    DependencyType,
    DependencyScope,
    VulnerabilitySeverity,
    ExploitMaturity,
    RemediationType,
    ComponentStatus,
)
from .sbom_service import (
    SBOMAnalysisService,
    ComponentSearchRequest,
    VulnerabilitySearchRequest,
    SBOMSearchRequest,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/sbom", tags=["sbom-analysis"])


# =============================================================================
# Pydantic Request/Response Models
# =============================================================================


# ===== SBOM Models =====

class SBOMCreate(BaseModel):
    """Request model for SBOM creation."""
    sbom_id: str = Field(..., description="Unique SBOM identifier")
    name: str = Field(..., description="SBOM name")
    format: str = Field("cyclonedx", description="SBOM format: cyclonedx, spdx, swid, syft, custom")
    format_version: Optional[str] = Field(None, description="Format version (e.g., 1.4)")
    target_system_id: Optional[str] = Field(None, description="Target system identifier")
    target_system_name: Optional[str] = Field(None, description="Target system name")
    tool_name: Optional[str] = Field(None, description="Tool used to generate SBOM")
    tool_version: Optional[str] = Field(None, description="Tool version")
    serial_number: Optional[str] = Field(None, description="SBOM serial number")


class SBOMResponse(BaseModel):
    """Response model for SBOM data."""
    sbom_id: str
    name: str
    customer_id: str
    format: str
    format_version: Optional[str]
    target_system_id: Optional[str]
    target_system_name: Optional[str]
    total_components: int
    direct_dependencies: int
    transitive_dependencies: int
    total_vulnerabilities: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    generated_at: Optional[str]


class SBOMSearchResponse(BaseModel):
    """Response for SBOM search results."""
    total_results: int
    customer_id: str
    results: List[SBOMResponse]


class SBOMRiskSummaryResponse(BaseModel):
    """Response for SBOM risk summary."""
    sbom_id: str
    sbom_name: str
    total_components: int
    vulnerable_components: int
    critical_vulns: int
    high_vulns: int
    max_cvss: float
    avg_cvss: float
    license_risk_high_count: int
    copyleft_count: int
    remediation_available: int
    kev_count: int
    exploitable_count: int


# ===== Component Models =====

class ComponentCreate(BaseModel):
    """Request model for component creation."""
    component_id: str = Field(..., description="Unique component identifier")
    sbom_id: str = Field(..., description="Parent SBOM ID")
    name: str = Field(..., description="Component/package name")
    version: str = Field(..., description="Component version")
    component_type: str = Field("library", description="Type: application, library, framework, container, os, firmware, file, device, machine_learning, data")
    purl: Optional[str] = Field(None, description="Package URL (e.g., pkg:npm/lodash@4.17.21)")
    cpe: Optional[str] = Field(None, description="CPE identifier")
    supplier: Optional[str] = Field(None, description="Supplier/vendor name")
    publisher: Optional[str] = Field(None, description="Publisher name")
    group: Optional[str] = Field(None, description="Group/namespace (e.g., org.apache.commons)")
    license_type: Optional[str] = Field(None, description="License type: mit, apache_2, gpl_2, etc.")
    license_expression: Optional[str] = Field(None, description="SPDX license expression")
    description: Optional[str] = Field(None, description="Component description")


class ComponentResponse(BaseModel):
    """Response model for component data."""
    component_id: str
    sbom_id: str
    customer_id: str
    name: str
    version: str
    component_type: str
    purl: Optional[str]
    cpe: Optional[str]
    supplier: Optional[str]
    license_type: Optional[str]
    license_risk: Optional[str]
    status: str
    vulnerability_count: int
    critical_vuln_count: int
    max_cvss_score: float
    is_high_risk: bool


class ComponentSearchResponse(BaseModel):
    """Response for component search results."""
    total_results: int
    customer_id: str
    results: List[ComponentResponse]


class DependencyTreeResponse(BaseModel):
    """Response for dependency tree."""
    component_id: str
    component_name: str
    depth: int
    children: List["DependencyTreeResponse"]
    dependencies_count: int
    dependents_count: int


DependencyTreeResponse.model_rebuild()  # For recursive model


class DependencyGraphStatsResponse(BaseModel):
    """Response for dependency graph statistics."""
    total_components: int
    total_dependencies: int
    direct_dependencies: int
    transitive_dependencies: int
    max_depth: int
    avg_depth: float
    root_nodes: int
    leaf_nodes: int
    cyclic_dependencies: int
    graph_density: float


# ===== Vulnerability Models =====

class VulnerabilityCreate(BaseModel):
    """Request model for vulnerability creation."""
    vulnerability_id: str = Field(..., description="Unique vulnerability ID")
    cve_id: str = Field(..., description="CVE identifier (e.g., CVE-2024-1234)")
    component_id: str = Field(..., description="Affected component ID")
    title: Optional[str] = Field(None, description="Vulnerability title")
    description: Optional[str] = Field(None, description="Detailed description")
    cvss_v3_score: float = Field(..., ge=0.0, le=10.0, description="CVSS v3 score")
    cvss_v3_vector: Optional[str] = Field(None, description="CVSS v3 vector string")
    epss_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="EPSS score (0-1)")
    epss_percentile: Optional[float] = Field(None, ge=0.0, le=100.0, description="EPSS percentile")
    exploit_available: bool = Field(False, description="Is exploit available?")
    in_the_wild: bool = Field(False, description="Is exploited in the wild?")
    cisa_kev: bool = Field(False, description="Is in CISA KEV catalog?")
    apt_groups: List[str] = Field(default_factory=list, description="APT groups using this CVE")
    fixed_version: Optional[str] = Field(None, description="Fixed version if available")
    patch_url: Optional[str] = Field(None, description="Patch/remediation URL")


class VulnerabilityResponse(BaseModel):
    """Response model for vulnerability data."""
    vulnerability_id: str
    cve_id: str
    component_id: str
    customer_id: str
    title: Optional[str]
    severity: str
    cvss_v3_score: float
    cvss_v3_vector: Optional[str]
    epss_score: Optional[float]
    epss_percentile: Optional[float]
    exploit_available: bool
    in_the_wild: bool
    cisa_kev: bool
    apt_groups: List[str]
    fixed_version: Optional[str]
    remediation_type: Optional[str]
    is_critical: bool
    has_fix: bool
    acknowledged: bool
    acknowledged_by: Optional[str]


class VulnerabilitySearchResponse(BaseModel):
    """Response for vulnerability search results."""
    total_results: int
    customer_id: str
    results: List[VulnerabilityResponse]


class VulnerabilityAcknowledgeRequest(BaseModel):
    """Request to acknowledge a vulnerability."""
    acknowledged_by: str = Field(..., description="User/team acknowledging")
    notes: str = Field("", description="Acknowledgment notes")
    risk_accepted: bool = Field(False, description="Is risk formally accepted?")


class APTReportResponse(BaseModel):
    """Response for APT vulnerability report."""
    total_apt_groups: int
    total_vulnerabilities: int
    customer_id: str
    apt_breakdown: List[dict]


class RemediationReportResponse(BaseModel):
    """Response for remediation report."""
    sbom_id: str
    customer_id: str
    total_vulnerabilities: int
    critical_vulns: int
    with_patches: int
    with_upgrades: int
    no_fix_available: int
    prioritized_actions: List[dict]


# ===== Dependency Models =====

class DependencyCreate(BaseModel):
    """Request model for dependency relation creation."""
    source_component_id: str = Field(..., description="Source component ID")
    target_component_id: str = Field(..., description="Target component ID (dependency)")
    dependency_type: str = Field("direct", description="Type: direct, transitive, optional, dev, peer, build, test, provided")
    scope: str = Field("runtime", description="Scope: compile, runtime, test, provided, system, import")
    version_requirement: Optional[str] = Field(None, description="Version requirement (e.g., ^2.0.0)")


class DependencyResponse(BaseModel):
    """Response model for dependency relation."""
    source_component_id: str
    target_component_id: str
    dependency_type: str
    scope: str
    depth: int
    is_direct: bool


class DependencyPathResponse(BaseModel):
    """Response for dependency path."""
    path: List[str]
    path_names: List[str]
    depth: int
    has_vulnerabilities: bool
    max_cvss_in_path: float


class ImpactAnalysisResponse(BaseModel):
    """Response for component impact analysis."""
    component_id: str
    component_name: str
    direct_dependents: int
    total_dependents: int
    affected_sboms: List[str]
    vulnerability_exposure: int


# ===== License Models =====

class LicenseComplianceResponse(BaseModel):
    """Response for license compliance analysis."""
    sbom_id: str
    customer_id: str
    is_compliant: bool
    compliant_count: int
    non_compliant_count: int
    copyleft_count: int
    high_risk_count: int
    license_conflicts: List[str]
    recommendations: List[str]


# ===== Dashboard Models =====

class DashboardSummaryResponse(BaseModel):
    """Response for customer-wide dashboard summary."""
    customer_id: str
    total_sboms: int
    total_components: int
    total_vulnerabilities: int
    critical_vulns: int
    high_vulns: int
    kev_vulns: int
    exploitable_vulns: int
    high_risk_components: int
    sboms_with_vulns: int
    avg_cvss: float


# =============================================================================
# Dependencies
# =============================================================================


def get_service() -> SBOMAnalysisService:
    """Get SBOM analysis service instance."""
    return SBOMAnalysisService()


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
# SBOM Endpoints
# =============================================================================


@router.post("/sboms", response_model=SBOMResponse, status_code=201)
async def create_sbom(
    sbom_data: SBOMCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """
    Create a new SBOM for the customer.

    Requires WRITE access level.
    """
    from .sbom_models import SBOM, SBOMFormat

    try:
        sbom = SBOM(
            sbom_id=sbom_data.sbom_id,
            name=sbom_data.name,
            customer_id=context.customer_id,
            format=SBOMFormat(sbom_data.format),
            format_version=sbom_data.format_version,
            target_system_id=sbom_data.target_system_id,
            target_system_name=sbom_data.target_system_name,
            tool_name=sbom_data.tool_name,
            tool_version=sbom_data.tool_version,
            serial_number=sbom_data.serial_number,
        )
        created_id = service.create_sbom(sbom)

        return SBOMResponse(
            sbom_id=sbom.sbom_id,
            name=sbom.name,
            customer_id=sbom.customer_id,
            format=sbom.format.value,
            format_version=sbom.format_version,
            target_system_id=sbom.target_system_id,
            target_system_name=sbom.target_system_name,
            total_components=sbom.total_components,
            direct_dependencies=sbom.direct_dependencies,
            transitive_dependencies=sbom.transitive_dependencies,
            total_vulnerabilities=sbom.total_vulnerabilities,
            critical_count=sbom.critical_count,
            high_count=sbom.high_count,
            medium_count=sbom.medium_count,
            low_count=sbom.low_count,
            generated_at=sbom.generated_at.isoformat() if sbom.generated_at else None,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sboms/{sbom_id}", response_model=SBOMResponse)
async def get_sbom(
    sbom_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get SBOM by ID with customer isolation."""
    sbom = service.get_sbom(sbom_id)
    if not sbom:
        raise HTTPException(status_code=404, detail=f"SBOM {sbom_id} not found")

    return SBOMResponse(
        sbom_id=sbom.sbom_id,
        name=sbom.name,
        customer_id=sbom.customer_id,
        format=sbom.format.value if hasattr(sbom.format, 'value') else sbom.format,
        format_version=sbom.format_version,
        target_system_id=sbom.target_system_id,
        target_system_name=sbom.target_system_name,
        total_components=sbom.total_components,
        direct_dependencies=sbom.direct_dependencies,
        transitive_dependencies=sbom.transitive_dependencies,
        total_vulnerabilities=sbom.total_vulnerabilities,
        critical_count=sbom.critical_count,
        high_count=sbom.high_count,
        medium_count=sbom.medium_count,
        low_count=sbom.low_count,
        generated_at=sbom.generated_at.isoformat() if sbom.generated_at else None,
    )


@router.get("/sboms", response_model=SBOMSearchResponse)
async def list_sboms(
    query: Optional[str] = Query(None, description="Search query"),
    format: Optional[str] = Query(None, description="Filter by SBOM format"),
    has_vulnerabilities: Optional[bool] = Query(None, description="Filter by vulnerability presence"),
    target_system_id: Optional[str] = Query(None, description="Filter by target system"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    include_system: bool = Query(True, description="Include SYSTEM SBOMs"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """List SBOMs with filters and customer isolation."""
    try:
        request = SBOMSearchRequest(
            query=query,
            customer_id=context.customer_id,
            format=SBOMFormat(format) if format else None,
            has_vulnerabilities=has_vulnerabilities,
            target_system_id=target_system_id,
            limit=limit,
            include_system=include_system,
        )
        results = service.list_sboms(
            format=request.format,
            limit=request.limit,
        )

        sbom_responses = [
            SBOMResponse(
                sbom_id=sbom.sbom_id,
                name=sbom.name,
                customer_id=sbom.customer_id,
                format=sbom.format.value if hasattr(sbom.format, 'value') else sbom.format,
                format_version=sbom.format_version,
                target_system_id=sbom.target_system_id,
                target_system_name=sbom.target_system_name,
                total_components=sbom.total_components,
                direct_dependencies=sbom.direct_dependencies,
                transitive_dependencies=sbom.transitive_dependencies,
                total_vulnerabilities=sbom.total_vulnerabilities,
                critical_count=sbom.critical_count,
                high_count=sbom.high_count,
                medium_count=sbom.medium_count,
                low_count=sbom.low_count,
                generated_at=sbom.generated_at.isoformat() if sbom.generated_at else None,
            )
            for sbom in results
        ]

        return SBOMSearchResponse(
            total_results=len(sbom_responses),
            customer_id=context.customer_id,
            results=sbom_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/sboms/{sbom_id}")
async def delete_sbom(
    sbom_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """
    Delete an SBOM and all its components.

    Requires WRITE access level.
    """
    try:
        deleted = service.delete_sbom(sbom_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"SBOM {sbom_id} not found")

        return {"message": f"SBOM {sbom_id} and all components deleted successfully"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/sboms/{sbom_id}/risk-summary", response_model=SBOMRiskSummaryResponse)
async def get_sbom_risk_summary(
    sbom_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get comprehensive risk summary for an SBOM."""
    summary = service.get_sbom_risk_summary(sbom_id)
    if not summary:
        raise HTTPException(status_code=404, detail=f"SBOM {sbom_id} not found")

    return SBOMRiskSummaryResponse(
        sbom_id=sbom_id,
        sbom_name=summary.get("sbom_name", ""),
        total_components=summary.get("total_components", 0),
        vulnerable_components=summary.get("vulnerable_components", 0),
        critical_vulns=summary.get("critical_vulns", 0),
        high_vulns=summary.get("high_vulns", 0),
        max_cvss=summary.get("max_cvss", 0.0),
        avg_cvss=summary.get("avg_cvss", 0.0),
        license_risk_high_count=summary.get("license_risk_high_count", 0),
        copyleft_count=summary.get("copyleft_count", 0),
        remediation_available=summary.get("remediation_available", 0),
        kev_count=summary.get("kev_count", 0),
        exploitable_count=summary.get("exploitable_count", 0),
    )


# =============================================================================
# Component Endpoints
# =============================================================================


@router.post("/components", response_model=ComponentResponse, status_code=201)
async def create_component(
    component_data: ComponentCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """
    Create a new software component.

    Requires WRITE access level.
    """
    from .sbom_models import SoftwareComponent, ComponentType, LicenseType

    try:
        component = SoftwareComponent(
            component_id=component_data.component_id,
            sbom_id=component_data.sbom_id,
            customer_id=context.customer_id,
            name=component_data.name,
            version=component_data.version,
            component_type=ComponentType(component_data.component_type),
            purl=component_data.purl,
            cpe=component_data.cpe,
            supplier=component_data.supplier,
            publisher=component_data.publisher,
            group=component_data.group,
            license_type=LicenseType(component_data.license_type) if component_data.license_type else None,
            license_expression=component_data.license_expression,
            description=component_data.description,
        )
        created_id = service.create_component(component)

        return ComponentResponse(
            component_id=component.component_id,
            sbom_id=component.sbom_id,
            customer_id=component.customer_id,
            name=component.name,
            version=component.version,
            component_type=component.component_type.value if hasattr(component.component_type, 'value') else component.component_type,
            purl=component.purl,
            cpe=component.cpe,
            supplier=component.supplier,
            license_type=component.license_type.value if component.license_type and hasattr(component.license_type, 'value') else None,
            license_risk=component.license_risk.value if component.license_risk and hasattr(component.license_risk, 'value') else None,
            status=component.status.value if hasattr(component.status, 'value') else component.status,
            vulnerability_count=component.vulnerability_count,
            critical_vuln_count=component.critical_vuln_count,
            max_cvss_score=component.max_cvss_score,
            is_high_risk=component.is_high_risk,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/components/{component_id}", response_model=ComponentResponse)
async def get_component(
    component_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get component by ID with customer isolation."""
    component = service.get_component(component_id)
    if not component:
        raise HTTPException(status_code=404, detail=f"Component {component_id} not found")

    return ComponentResponse(
        component_id=component.component_id,
        sbom_id=component.sbom_id,
        customer_id=component.customer_id,
        name=component.name,
        version=component.version,
        component_type=component.component_type.value if hasattr(component.component_type, 'value') else component.component_type,
        purl=component.purl,
        cpe=component.cpe,
        supplier=component.supplier,
        license_type=component.license_type.value if component.license_type and hasattr(component.license_type, 'value') else None,
        license_risk=component.license_risk.value if component.license_risk and hasattr(component.license_risk, 'value') else None,
        status=component.status.value if hasattr(component.status, 'value') else component.status,
        vulnerability_count=component.vulnerability_count,
        critical_vuln_count=component.critical_vuln_count,
        max_cvss_score=component.max_cvss_score,
        is_high_risk=component.is_high_risk,
    )


@router.get("/components/search", response_model=ComponentSearchResponse)
async def search_components(
    query: Optional[str] = Query(None, description="Semantic search query"),
    sbom_id: Optional[str] = Query(None, description="Filter by SBOM"),
    component_type: Optional[str] = Query(None, description="Filter by component type"),
    license_risk: Optional[str] = Query(None, description="Filter by license risk"),
    has_vulnerabilities: Optional[bool] = Query(None, description="Filter by vulnerability presence"),
    min_cvss: Optional[float] = Query(None, ge=0, le=10, description="Minimum CVSS score"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    include_system: bool = Query(True, description="Include SYSTEM components"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Search components with semantic search and filters."""
    try:
        request = ComponentSearchRequest(
            query=query,
            customer_id=context.customer_id,
            sbom_id=sbom_id,
            component_type=ComponentType(component_type) if component_type else None,
            license_risk=LicenseRisk(license_risk) if license_risk else None,
            has_vulnerabilities=has_vulnerabilities,
            min_cvss=min_cvss,
            status=ComponentStatus(status) if status else None,
            limit=limit,
            include_system=include_system,
        )
        results = service.search_components(request)

        component_responses = [
            ComponentResponse(
                component_id=r.component.component_id,
                sbom_id=r.component.sbom_id,
                customer_id=r.component.customer_id,
                name=r.component.name,
                version=r.component.version,
                component_type=r.component.component_type.value if hasattr(r.component.component_type, 'value') else r.component.component_type,
                purl=r.component.purl,
                cpe=r.component.cpe,
                supplier=r.component.supplier,
                license_type=r.component.license_type.value if r.component.license_type and hasattr(r.component.license_type, 'value') else None,
                license_risk=r.component.license_risk.value if r.component.license_risk and hasattr(r.component.license_risk, 'value') else None,
                status=r.component.status.value if hasattr(r.component.status, 'value') else r.component.status,
                vulnerability_count=r.component.vulnerability_count,
                critical_vuln_count=r.component.critical_vuln_count,
                max_cvss_score=r.component.max_cvss_score,
                is_high_risk=r.component.is_high_risk,
            )
            for r in results
        ]

        return ComponentSearchResponse(
            total_results=len(component_responses),
            customer_id=context.customer_id,
            results=component_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/components/vulnerable", response_model=ComponentSearchResponse)
async def get_vulnerable_components(
    min_cvss: float = Query(7.0, ge=0, le=10, description="Minimum CVSS threshold"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get all components with vulnerabilities above CVSS threshold."""
    results = service.get_vulnerable_components(min_cvss)

    component_responses = [
        ComponentResponse(
            component_id=r.component.component_id,
            sbom_id=r.component.sbom_id,
            customer_id=r.component.customer_id,
            name=r.component.name,
            version=r.component.version,
            component_type=r.component.component_type.value if hasattr(r.component.component_type, 'value') else r.component.component_type,
            purl=r.component.purl,
            cpe=r.component.cpe,
            supplier=r.component.supplier,
            license_type=r.component.license_type.value if r.component.license_type and hasattr(r.component.license_type, 'value') else None,
            license_risk=r.component.license_risk.value if r.component.license_risk and hasattr(r.component.license_risk, 'value') else None,
            status=r.component.status.value if hasattr(r.component.status, 'value') else r.component.status,
            vulnerability_count=r.component.vulnerability_count,
            critical_vuln_count=r.component.critical_vuln_count,
            max_cvss_score=r.component.max_cvss_score,
            is_high_risk=r.component.is_high_risk,
        )
        for r in results
    ]

    return ComponentSearchResponse(
        total_results=len(component_responses),
        customer_id=context.customer_id,
        results=component_responses,
    )


@router.get("/components/high-risk", response_model=ComponentSearchResponse)
async def get_high_risk_components(
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get all high-risk components (critical vulns, high license risk, or deprecated)."""
    results = service.get_high_risk_components()

    component_responses = [
        ComponentResponse(
            component_id=r.component.component_id,
            sbom_id=r.component.sbom_id,
            customer_id=r.component.customer_id,
            name=r.component.name,
            version=r.component.version,
            component_type=r.component.component_type.value if hasattr(r.component.component_type, 'value') else r.component.component_type,
            purl=r.component.purl,
            cpe=r.component.cpe,
            supplier=r.component.supplier,
            license_type=r.component.license_type.value if r.component.license_type and hasattr(r.component.license_type, 'value') else None,
            license_risk=r.component.license_risk.value if r.component.license_risk and hasattr(r.component.license_risk, 'value') else None,
            status=r.component.status.value if hasattr(r.component.status, 'value') else r.component.status,
            vulnerability_count=r.component.vulnerability_count,
            critical_vuln_count=r.component.critical_vuln_count,
            max_cvss_score=r.component.max_cvss_score,
            is_high_risk=r.component.is_high_risk,
        )
        for r in results
    ]

    return ComponentSearchResponse(
        total_results=len(component_responses),
        customer_id=context.customer_id,
        results=component_responses,
    )


@router.get("/sboms/{sbom_id}/components", response_model=ComponentSearchResponse)
async def get_components_by_sbom(
    sbom_id: str,
    limit: int = Query(100, ge=1, le=500, description="Maximum components"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get all components for a specific SBOM."""
    results = service.get_components_by_sbom(sbom_id, limit)

    component_responses = [
        ComponentResponse(
            component_id=c.component_id,
            sbom_id=c.sbom_id,
            customer_id=c.customer_id,
            name=c.name,
            version=c.version,
            component_type=c.component_type.value if hasattr(c.component_type, 'value') else c.component_type,
            purl=c.purl,
            cpe=c.cpe,
            supplier=c.supplier,
            license_type=c.license_type.value if c.license_type and hasattr(c.license_type, 'value') else None,
            license_risk=c.license_risk.value if c.license_risk and hasattr(c.license_risk, 'value') else None,
            status=c.status.value if hasattr(c.status, 'value') else c.status,
            vulnerability_count=c.vulnerability_count,
            critical_vuln_count=c.critical_vuln_count,
            max_cvss_score=c.max_cvss_score,
            is_high_risk=c.is_high_risk,
        )
        for c in results
    ]

    return ComponentSearchResponse(
        total_results=len(component_responses),
        customer_id=context.customer_id,
        results=component_responses,
    )


# =============================================================================
# Dependency Endpoints
# =============================================================================


@router.post("/dependencies", response_model=DependencyResponse, status_code=201)
async def create_dependency(
    dependency_data: DependencyCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """
    Create a new dependency relation.

    Requires WRITE access level.
    """
    from .sbom_models import DependencyRelation, DependencyType, DependencyScope

    try:
        relation = DependencyRelation(
            relation_id=f"dep_{dependency_data.source_component_id}_{dependency_data.target_component_id}",
            source_component_id=dependency_data.source_component_id,
            target_component_id=dependency_data.target_component_id,
            customer_id=context.customer_id,
            dependency_type=DependencyType(dependency_data.dependency_type),
            scope=DependencyScope(dependency_data.scope),
            version_requirement=dependency_data.version_requirement,
        )
        created_id = service.create_dependency(relation)

        return DependencyResponse(
            source_component_id=relation.source_component_id,
            target_component_id=relation.target_component_id,
            dependency_type=relation.dependency_type.value if hasattr(relation.dependency_type, 'value') else relation.dependency_type,
            scope=relation.scope.value if hasattr(relation.scope, 'value') else relation.scope,
            depth=relation.depth,
            is_direct=relation.is_direct,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/components/{component_id}/dependencies", response_model=DependencyTreeResponse)
async def get_dependency_tree(
    component_id: str,
    max_depth: int = Query(10, ge=1, le=50, description="Maximum tree depth"),
    include_dev: bool = Query(False, description="Include dev dependencies"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get dependency tree for a component."""
    tree = service.build_dependency_tree(component_id, max_depth, include_dev)
    if not tree:
        raise HTTPException(status_code=404, detail=f"Component {component_id} not found")

    def node_to_response(node) -> DependencyTreeResponse:
        return DependencyTreeResponse(
            component_id=node.component_id,
            component_name=node.component_name,
            depth=node.depth,
            children=[node_to_response(c) for c in node.children],
            dependencies_count=node.dependencies_count,
            dependents_count=node.dependents_count,
        )

    return node_to_response(tree)


@router.get("/components/{component_id}/dependents")
async def get_dependents(
    component_id: str,
    limit: int = Query(50, ge=1, le=200, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get all components that depend on this component (reverse dependencies)."""
    dependents = service.get_dependents(component_id, limit)

    return {
        "component_id": component_id,
        "customer_id": context.customer_id,
        "total_dependents": len(dependents),
        "dependents": [
            {
                "source_component_id": d.source_component_id,
                "target_component_id": d.target_component_id,
                "dependency_type": d.dependency_type.value if hasattr(d.dependency_type, 'value') else d.dependency_type,
                "scope": d.scope.value if hasattr(d.scope, 'value') else d.scope,
                "depth": d.depth,
            }
            for d in dependents
        ],
    }


@router.get("/components/{component_id}/impact", response_model=ImpactAnalysisResponse)
async def get_impact_analysis(
    component_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Analyze the impact if a component has a vulnerability."""
    impact = service.get_impact_analysis(component_id)
    if not impact:
        raise HTTPException(status_code=404, detail=f"Component {component_id} not found")

    return ImpactAnalysisResponse(
        component_id=impact.component_id,
        component_name=impact.component_name,
        direct_dependents=impact.direct_dependents,
        total_dependents=impact.total_dependents,
        affected_sboms=impact.affected_sboms,
        vulnerability_exposure=impact.vulnerability_exposure,
    )


@router.get("/sboms/{sbom_id}/cycles")
async def detect_cycles(
    sbom_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Detect circular dependencies in an SBOM."""
    cycles = service.detect_cycles(sbom_id)

    return {
        "sbom_id": sbom_id,
        "customer_id": context.customer_id,
        "has_cycles": len(cycles) > 0,
        "cycle_count": len(cycles),
        "cycles": cycles,
    }


@router.get("/dependencies/path")
async def find_dependency_path(
    source_id: str = Query(..., description="Source component ID"),
    target_id: str = Query(..., description="Target component ID"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Find shortest dependency path between two components."""
    path = service.find_shortest_path(source_id, target_id)
    if not path:
        return {
            "source_id": source_id,
            "target_id": target_id,
            "path_found": False,
            "path": None,
        }

    return {
        "source_id": source_id,
        "target_id": target_id,
        "path_found": True,
        "path": {
            "component_ids": path.path,
            "component_names": path.path_names,
            "depth": path.depth,
            "has_vulnerabilities": path.has_vulnerabilities,
            "max_cvss": path.max_cvss_in_path,
        },
    }


@router.get("/sboms/{sbom_id}/graph-stats", response_model=DependencyGraphStatsResponse)
async def get_graph_stats(
    sbom_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get comprehensive dependency graph statistics for an SBOM."""
    stats = service.get_dependency_graph_stats(sbom_id)
    if not stats:
        raise HTTPException(status_code=404, detail=f"SBOM {sbom_id} not found")

    return DependencyGraphStatsResponse(
        total_components=stats.get("total_components", 0),
        total_dependencies=stats.get("total_dependencies", 0),
        direct_dependencies=stats.get("direct_dependencies", 0),
        transitive_dependencies=stats.get("transitive_dependencies", 0),
        max_depth=stats.get("max_depth", 0),
        avg_depth=stats.get("avg_depth", 0.0),
        root_nodes=stats.get("root_nodes", 0),
        leaf_nodes=stats.get("leaf_nodes", 0),
        cyclic_dependencies=stats.get("cyclic_dependencies", 0),
        graph_density=stats.get("density", 0.0),
    )


# =============================================================================
# Vulnerability Endpoints
# =============================================================================


@router.post("/vulnerabilities", response_model=VulnerabilityResponse, status_code=201)
async def create_vulnerability(
    vuln_data: VulnerabilityCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """
    Create a new vulnerability record.

    Requires WRITE access level.
    """
    from .sbom_models import SoftwareVulnerability, VulnerabilitySeverity, ExploitMaturity, RemediationType

    try:
        # Determine severity from CVSS
        if vuln_data.cvss_v3_score >= 9.0:
            severity = VulnerabilitySeverity.CRITICAL
        elif vuln_data.cvss_v3_score >= 7.0:
            severity = VulnerabilitySeverity.HIGH
        elif vuln_data.cvss_v3_score >= 4.0:
            severity = VulnerabilitySeverity.MEDIUM
        elif vuln_data.cvss_v3_score > 0:
            severity = VulnerabilitySeverity.LOW
        else:
            severity = VulnerabilitySeverity.NONE

        # Determine exploit maturity
        if vuln_data.in_the_wild or vuln_data.cisa_kev:
            maturity = ExploitMaturity.WEAPONIZED
        elif vuln_data.exploit_available:
            maturity = ExploitMaturity.FUNCTIONAL
        else:
            maturity = ExploitMaturity.UNPROVEN

        vuln = SoftwareVulnerability(
            vulnerability_id=vuln_data.vulnerability_id,
            cve_id=vuln_data.cve_id,
            component_id=vuln_data.component_id,
            customer_id=context.customer_id,
            title=vuln_data.title,
            description=vuln_data.description,
            severity=severity,
            cvss_v3_score=vuln_data.cvss_v3_score,
            cvss_v3_vector=vuln_data.cvss_v3_vector,
            epss_score=vuln_data.epss_score,
            epss_percentile=vuln_data.epss_percentile,
            exploit_available=vuln_data.exploit_available,
            in_the_wild=vuln_data.in_the_wild,
            cisa_kev=vuln_data.cisa_kev,
            exploit_maturity=maturity,
            apt_groups=vuln_data.apt_groups,
            fixed_version=vuln_data.fixed_version,
            patch_url=vuln_data.patch_url,
            remediation_type=RemediationType.PATCH if vuln_data.patch_url else (RemediationType.UPGRADE if vuln_data.fixed_version else RemediationType.NO_FIX),
        )
        created_id = service.create_vulnerability(vuln)

        return VulnerabilityResponse(
            vulnerability_id=vuln.vulnerability_id,
            cve_id=vuln.cve_id,
            component_id=vuln.component_id,
            customer_id=vuln.customer_id,
            title=vuln.title,
            severity=vuln.severity.value if hasattr(vuln.severity, 'value') else vuln.severity,
            cvss_v3_score=vuln.cvss_v3_score,
            cvss_v3_vector=vuln.cvss_v3_vector,
            epss_score=vuln.epss_score,
            epss_percentile=vuln.epss_percentile,
            exploit_available=vuln.exploit_available,
            in_the_wild=vuln.in_the_wild,
            cisa_kev=vuln.cisa_kev,
            apt_groups=vuln.apt_groups,
            fixed_version=vuln.fixed_version,
            remediation_type=vuln.remediation_type.value if vuln.remediation_type and hasattr(vuln.remediation_type, 'value') else None,
            is_critical=vuln.is_critical,
            has_fix=vuln.has_fix,
            acknowledged=vuln.acknowledged,
            acknowledged_by=vuln.acknowledged_by,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/vulnerabilities/{vulnerability_id}", response_model=VulnerabilityResponse)
async def get_vulnerability(
    vulnerability_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get vulnerability by ID."""
    vuln = service.get_vulnerability(vulnerability_id)
    if not vuln:
        raise HTTPException(status_code=404, detail=f"Vulnerability {vulnerability_id} not found")

    return VulnerabilityResponse(
        vulnerability_id=vuln.vulnerability_id,
        cve_id=vuln.cve_id,
        component_id=vuln.component_id,
        customer_id=vuln.customer_id,
        title=vuln.title,
        severity=vuln.severity.value if hasattr(vuln.severity, 'value') else vuln.severity,
        cvss_v3_score=vuln.cvss_v3_score,
        cvss_v3_vector=vuln.cvss_v3_vector,
        epss_score=vuln.epss_score,
        epss_percentile=vuln.epss_percentile,
        exploit_available=vuln.exploit_available,
        in_the_wild=vuln.in_the_wild,
        cisa_kev=vuln.cisa_kev,
        apt_groups=vuln.apt_groups,
        fixed_version=vuln.fixed_version,
        remediation_type=vuln.remediation_type.value if vuln.remediation_type and hasattr(vuln.remediation_type, 'value') else None,
        is_critical=vuln.is_critical,
        has_fix=vuln.has_fix,
        acknowledged=vuln.acknowledged,
        acknowledged_by=vuln.acknowledged_by,
    )


@router.get("/vulnerabilities/search", response_model=VulnerabilitySearchResponse)
async def search_vulnerabilities(
    query: Optional[str] = Query(None, description="Semantic search query"),
    component_id: Optional[str] = Query(None, description="Filter by component"),
    min_cvss: Optional[float] = Query(None, ge=0, le=10, description="Minimum CVSS score"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    exploit_available: Optional[bool] = Query(None, description="Has exploit available"),
    cisa_kev: Optional[bool] = Query(None, description="Is in CISA KEV"),
    has_fix: Optional[bool] = Query(None, description="Has fix available"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results"),
    include_system: bool = Query(True, description="Include SYSTEM vulnerabilities"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Search vulnerabilities with semantic search and filters."""
    try:
        request = VulnerabilitySearchRequest(
            query=query,
            customer_id=context.customer_id,
            component_id=component_id,
            min_cvss=min_cvss,
            severity=VulnerabilitySeverity(severity) if severity else None,
            exploit_available=exploit_available,
            cisa_kev=cisa_kev,
            has_fix=has_fix,
            limit=limit,
            include_system=include_system,
        )
        results = service.search_vulnerabilities(request)

        vuln_responses = [
            VulnerabilityResponse(
                vulnerability_id=r.vulnerability.vulnerability_id,
                cve_id=r.vulnerability.cve_id,
                component_id=r.vulnerability.component_id,
                customer_id=r.vulnerability.customer_id,
                title=r.vulnerability.title,
                severity=r.vulnerability.severity.value if hasattr(r.vulnerability.severity, 'value') else r.vulnerability.severity,
                cvss_v3_score=r.vulnerability.cvss_v3_score,
                cvss_v3_vector=r.vulnerability.cvss_v3_vector,
                epss_score=r.vulnerability.epss_score,
                epss_percentile=r.vulnerability.epss_percentile,
                exploit_available=r.vulnerability.exploit_available,
                in_the_wild=r.vulnerability.in_the_wild,
                cisa_kev=r.vulnerability.cisa_kev,
                apt_groups=r.vulnerability.apt_groups,
                fixed_version=r.vulnerability.fixed_version,
                remediation_type=r.vulnerability.remediation_type.value if r.vulnerability.remediation_type and hasattr(r.vulnerability.remediation_type, 'value') else None,
                is_critical=r.vulnerability.is_critical,
                has_fix=r.vulnerability.has_fix,
                acknowledged=r.vulnerability.acknowledged,
                acknowledged_by=r.vulnerability.acknowledged_by,
            )
            for r in results
        ]

        return VulnerabilitySearchResponse(
            total_results=len(vuln_responses),
            customer_id=context.customer_id,
            results=vuln_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/vulnerabilities/critical", response_model=VulnerabilitySearchResponse)
async def get_critical_vulnerabilities(
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get all critical vulnerabilities (CISA KEV, in-the-wild, or CVSS >= 9.0)."""
    results = service.get_critical_vulnerabilities()

    vuln_responses = [
        VulnerabilityResponse(
            vulnerability_id=v.vulnerability_id,
            cve_id=v.cve_id,
            component_id=v.component_id,
            customer_id=v.customer_id,
            title=v.title,
            severity=v.severity.value if hasattr(v.severity, 'value') else v.severity,
            cvss_v3_score=v.cvss_v3_score,
            cvss_v3_vector=v.cvss_v3_vector,
            epss_score=v.epss_score,
            epss_percentile=v.epss_percentile,
            exploit_available=v.exploit_available,
            in_the_wild=v.in_the_wild,
            cisa_kev=v.cisa_kev,
            apt_groups=v.apt_groups,
            fixed_version=v.fixed_version,
            remediation_type=v.remediation_type.value if v.remediation_type and hasattr(v.remediation_type, 'value') else None,
            is_critical=v.is_critical,
            has_fix=v.has_fix,
            acknowledged=v.acknowledged,
            acknowledged_by=v.acknowledged_by,
        )
        for v in results
    ]

    return VulnerabilitySearchResponse(
        total_results=len(vuln_responses),
        customer_id=context.customer_id,
        results=vuln_responses,
    )


@router.get("/vulnerabilities/kev", response_model=VulnerabilitySearchResponse)
async def get_kev_vulnerabilities(
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get all CISA Known Exploited Vulnerabilities (KEV)."""
    results = service.get_kev_vulnerabilities()

    vuln_responses = [
        VulnerabilityResponse(
            vulnerability_id=v.vulnerability_id,
            cve_id=v.cve_id,
            component_id=v.component_id,
            customer_id=v.customer_id,
            title=v.title,
            severity=v.severity.value if hasattr(v.severity, 'value') else v.severity,
            cvss_v3_score=v.cvss_v3_score,
            cvss_v3_vector=v.cvss_v3_vector,
            epss_score=v.epss_score,
            epss_percentile=v.epss_percentile,
            exploit_available=v.exploit_available,
            in_the_wild=v.in_the_wild,
            cisa_kev=v.cisa_kev,
            apt_groups=v.apt_groups,
            fixed_version=v.fixed_version,
            remediation_type=v.remediation_type.value if v.remediation_type and hasattr(v.remediation_type, 'value') else None,
            is_critical=v.is_critical,
            has_fix=v.has_fix,
            acknowledged=v.acknowledged,
            acknowledged_by=v.acknowledged_by,
        )
        for v in results
    ]

    return VulnerabilitySearchResponse(
        total_results=len(vuln_responses),
        customer_id=context.customer_id,
        results=vuln_responses,
    )


@router.get("/vulnerabilities/epss-prioritized", response_model=VulnerabilitySearchResponse)
async def get_epss_prioritized_vulns(
    min_epss: float = Query(0.1, ge=0, le=1, description="Minimum EPSS score"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get vulnerabilities prioritized by EPSS score (exploit probability)."""
    results = service.get_epss_prioritized_vulns(min_epss, limit)

    vuln_responses = [
        VulnerabilityResponse(
            vulnerability_id=v.vulnerability_id,
            cve_id=v.cve_id,
            component_id=v.component_id,
            customer_id=v.customer_id,
            title=v.title,
            severity=v.severity.value if hasattr(v.severity, 'value') else v.severity,
            cvss_v3_score=v.cvss_v3_score,
            cvss_v3_vector=v.cvss_v3_vector,
            epss_score=v.epss_score,
            epss_percentile=v.epss_percentile,
            exploit_available=v.exploit_available,
            in_the_wild=v.in_the_wild,
            cisa_kev=v.cisa_kev,
            apt_groups=v.apt_groups,
            fixed_version=v.fixed_version,
            remediation_type=v.remediation_type.value if v.remediation_type and hasattr(v.remediation_type, 'value') else None,
            is_critical=v.is_critical,
            has_fix=v.has_fix,
            acknowledged=v.acknowledged,
            acknowledged_by=v.acknowledged_by,
        )
        for v in results
    ]

    return VulnerabilitySearchResponse(
        total_results=len(vuln_responses),
        customer_id=context.customer_id,
        results=vuln_responses,
    )


@router.get("/vulnerabilities/by-apt", response_model=APTReportResponse)
async def get_apt_vulnerability_report(
    apt_group: Optional[str] = Query(None, description="Filter by specific APT group"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get vulnerability report grouped by APT groups."""
    report = service.get_apt_vulnerability_report()

    # Filter by APT group if specified
    apt_breakdown = report.get("apt_groups", [])
    if apt_group:
        apt_breakdown = [g for g in apt_breakdown if g.get("apt_group") == apt_group]

    return APTReportResponse(
        total_apt_groups=len(apt_breakdown),
        total_vulnerabilities=report.get("total_vulnerabilities", 0),
        customer_id=context.customer_id,
        apt_breakdown=apt_breakdown,
    )


@router.get("/components/{component_id}/vulnerabilities", response_model=VulnerabilitySearchResponse)
async def get_vulnerabilities_by_component(
    component_id: str,
    limit: int = Query(50, ge=1, le=200, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get all vulnerabilities for a specific component."""
    results = service.get_vulnerabilities_by_component(component_id, limit)

    vuln_responses = [
        VulnerabilityResponse(
            vulnerability_id=v.vulnerability_id,
            cve_id=v.cve_id,
            component_id=v.component_id,
            customer_id=v.customer_id,
            title=v.title,
            severity=v.severity.value if hasattr(v.severity, 'value') else v.severity,
            cvss_v3_score=v.cvss_v3_score,
            cvss_v3_vector=v.cvss_v3_vector,
            epss_score=v.epss_score,
            epss_percentile=v.epss_percentile,
            exploit_available=v.exploit_available,
            in_the_wild=v.in_the_wild,
            cisa_kev=v.cisa_kev,
            apt_groups=v.apt_groups,
            fixed_version=v.fixed_version,
            remediation_type=v.remediation_type.value if v.remediation_type and hasattr(v.remediation_type, 'value') else None,
            is_critical=v.is_critical,
            has_fix=v.has_fix,
            acknowledged=v.acknowledged,
            acknowledged_by=v.acknowledged_by,
        )
        for v in results
    ]

    return VulnerabilitySearchResponse(
        total_results=len(vuln_responses),
        customer_id=context.customer_id,
        results=vuln_responses,
    )


@router.post("/vulnerabilities/{vulnerability_id}/acknowledge")
async def acknowledge_vulnerability(
    vulnerability_id: str,
    ack_request: VulnerabilityAcknowledgeRequest,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """
    Acknowledge a vulnerability (mark as reviewed).

    Requires WRITE access level.
    """
    try:
        success = service.acknowledge_vulnerability(
            vulnerability_id=vulnerability_id,
            acknowledged_by=ack_request.acknowledged_by,
            notes=ack_request.notes,
            risk_accepted=ack_request.risk_accepted,
        )

        if not success:
            raise HTTPException(status_code=404, detail=f"Vulnerability {vulnerability_id} not found")

        return {
            "vulnerability_id": vulnerability_id,
            "acknowledged": True,
            "acknowledged_by": ack_request.acknowledged_by,
            "risk_accepted": ack_request.risk_accepted,
            "message": "Vulnerability acknowledged successfully",
        }
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/sboms/{sbom_id}/remediation", response_model=RemediationReportResponse)
async def get_remediation_report(
    sbom_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Generate remediation report for an SBOM."""
    report = service.get_remediation_report(sbom_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"SBOM {sbom_id} not found")

    return RemediationReportResponse(
        sbom_id=sbom_id,
        customer_id=context.customer_id,
        total_vulnerabilities=report.get("total_vulnerabilities", 0),
        critical_vulns=report.get("critical_vulns", 0),
        with_patches=report.get("with_patches", 0),
        with_upgrades=report.get("with_upgrades", 0),
        no_fix_available=report.get("no_fix_available", 0),
        prioritized_actions=report.get("prioritized_actions", []),
    )


# =============================================================================
# License Compliance Endpoints
# =============================================================================


@router.get("/sboms/{sbom_id}/license-compliance", response_model=LicenseComplianceResponse)
async def get_license_compliance(
    sbom_id: str,
    allowed_licenses: List[str] = Query(default=[], description="Allowed license types"),
    denied_licenses: List[str] = Query(default=[], description="Denied license types"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get license compliance analysis for an SBOM."""
    # Convert license strings to enums
    allowed = [LicenseType(l) for l in allowed_licenses] if allowed_licenses else None
    denied = [LicenseType(l) for l in denied_licenses] if denied_licenses else None

    result = service.get_license_compliance(sbom_id, allowed, denied)
    if not result:
        raise HTTPException(status_code=404, detail=f"SBOM {sbom_id} not found")

    return LicenseComplianceResponse(
        sbom_id=sbom_id,
        customer_id=context.customer_id,
        is_compliant=result.is_compliant,
        compliant_count=result.compliant_count,
        non_compliant_count=result.non_compliant_count,
        copyleft_count=result.copyleft_count if hasattr(result, 'copyleft_count') else 0,
        high_risk_count=result.high_risk_count if hasattr(result, 'high_risk_count') else 0,
        license_conflicts=result.license_conflicts,
        recommendations=result.recommendations,
    )


# =============================================================================
# Dashboard Endpoints
# =============================================================================


@router.get("/dashboard/summary", response_model=DashboardSummaryResponse)
async def get_dashboard_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Get customer-wide dashboard summary."""
    summary = service.get_dashboard_summary()

    return DashboardSummaryResponse(
        customer_id=context.customer_id,
        total_sboms=summary.get("total_sboms", 0),
        total_components=summary.get("total_components", 0),
        total_vulnerabilities=summary.get("total_vulnerabilities", 0),
        critical_vulns=summary.get("critical_vulns", 0),
        high_vulns=summary.get("high_vulns", 0),
        kev_vulns=summary.get("kev_vulns", 0),
        exploitable_vulns=summary.get("exploitable_vulns", 0),
        high_risk_components=summary.get("high_risk_components", 0),
        sboms_with_vulns=summary.get("sboms_with_vulns", 0),
        avg_cvss=summary.get("avg_cvss", 0.0),
    )


@router.get("/sboms/{sbom_id}/vulnerable-paths")
async def get_vulnerable_paths(
    sbom_id: str,
    min_cvss: float = Query(7.0, ge=0, le=10, description="Minimum CVSS threshold"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """Find all paths to vulnerable components in an SBOM."""
    paths = service.get_vulnerable_paths(sbom_id, min_cvss)

    return {
        "sbom_id": sbom_id,
        "customer_id": context.customer_id,
        "min_cvss": min_cvss,
        "total_paths": len(paths),
        "paths": paths,
    }


@router.post("/sboms/{sbom_id}/correlate-equipment")
async def correlate_with_equipment(
    sbom_id: str,
    equipment_id: str = Query(..., description="E15 Equipment ID to correlate"),
    context: CustomerContext = Depends(require_customer_context),
    service: SBOMAnalysisService = Depends(get_service),
):
    """
    Correlate SBOM vulnerabilities with E15 equipment.

    Links software vulnerabilities to physical equipment for risk assessment.
    """
    result = service.correlate_vulns_with_equipment(sbom_id, equipment_id)

    return {
        "sbom_id": sbom_id,
        "equipment_id": equipment_id,
        "customer_id": context.customer_id,
        "correlation": result,
    }
