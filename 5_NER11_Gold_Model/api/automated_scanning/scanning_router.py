"""
E08 Automated Scanning API Router
Provides 30 REST endpoints for automated security scanning operations
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

from .scanning_service import ScanningService


# Enums
class ScanType(str, Enum):
    VULNERABILITY = "vulnerability"
    COMPLIANCE = "compliance"
    MALWARE = "malware"
    CONFIGURATION = "configuration"
    NETWORK = "network"


class ScanStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class FindingSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingStatus(str, Enum):
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


class ScheduleFrequency(str, Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


# Request/Response Models
class ScanProfileCreate(BaseModel):
    name: str = Field(..., description="Profile name")
    scan_type: ScanType = Field(..., description="Type of scan")
    description: Optional[str] = Field(None, description="Profile description")
    configuration: dict = Field(..., description="Scan configuration parameters")
    enabled: bool = Field(True, description="Whether profile is active")


class ScanProfileUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    configuration: Optional[dict] = None
    enabled: Optional[bool] = None


class ScanProfileResponse(BaseModel):
    profile_id: str
    customer_id: str
    name: str
    scan_type: ScanType
    description: Optional[str]
    configuration: dict
    enabled: bool
    created_at: datetime
    updated_at: datetime


class ScheduleCreate(BaseModel):
    name: str = Field(..., description="Schedule name")
    profile_id: str = Field(..., description="Scan profile to execute")
    frequency: ScheduleFrequency = Field(..., description="Execution frequency")
    target_ids: List[str] = Field(..., description="Target IDs to scan")
    cron_expression: Optional[str] = Field(None, description="Custom cron expression")
    enabled: bool = Field(True, description="Whether schedule is active")


class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[ScheduleFrequency] = None
    target_ids: Optional[List[str]] = None
    cron_expression: Optional[str] = None
    enabled: Optional[bool] = None


class ScheduleResponse(BaseModel):
    schedule_id: str
    customer_id: str
    name: str
    profile_id: str
    frequency: ScheduleFrequency
    target_ids: List[str]
    cron_expression: Optional[str]
    enabled: bool
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class ScanJobCreate(BaseModel):
    profile_id: str = Field(..., description="Scan profile to use")
    target_ids: List[str] = Field(..., description="Targets to scan")
    priority: int = Field(5, ge=1, le=10, description="Job priority (1-10)")
    scheduled: bool = Field(False, description="Whether job is scheduled")


class ScanJobResponse(BaseModel):
    job_id: str
    customer_id: str
    profile_id: str
    target_ids: List[str]
    status: ScanStatus
    priority: int
    scheduled: bool
    progress: float
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    findings_count: int
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime


class FindingResponse(BaseModel):
    finding_id: str
    customer_id: str
    job_id: str
    target_id: str
    severity: FindingSeverity
    status: FindingStatus
    title: str
    description: str
    affected_resource: str
    recommendation: str
    cve_ids: List[str]
    references: List[str]
    first_detected: datetime
    last_detected: datetime
    created_at: datetime
    updated_at: datetime


class FindingStatusUpdate(BaseModel):
    status: FindingStatus = Field(..., description="New finding status")
    notes: Optional[str] = Field(None, description="Status change notes")


class FindingSearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    severity: Optional[List[FindingSeverity]] = None
    status: Optional[List[FindingStatus]] = None
    target_ids: Optional[List[str]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    limit: int = Field(100, ge=1, le=1000)


class TargetCreate(BaseModel):
    name: str = Field(..., description="Target name")
    target_type: str = Field(..., description="Type of target (host, network, application)")
    address: str = Field(..., description="Target address or identifier")
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class TargetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None


class TargetResponse(BaseModel):
    target_id: str
    customer_id: str
    name: str
    target_type: str
    address: str
    description: Optional[str]
    tags: List[str]
    metadata: dict
    last_scanned: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class DashboardSummary(BaseModel):
    total_profiles: int
    active_profiles: int
    total_schedules: int
    active_schedules: int
    running_jobs: int
    completed_jobs_24h: int
    failed_jobs_24h: int
    total_findings: int
    critical_findings: int
    high_findings: int
    medium_findings: int
    low_findings: int
    findings_by_status: dict
    recent_jobs: List[ScanJobResponse]


# Router setup
router = APIRouter(prefix="/api/v2/scanning", tags=["E08 Automated Scanning"])


def get_customer_id(x_customer_id: str = Header(...)) -> str:
    """Extract and validate customer ID from header"""
    if not x_customer_id:
        raise HTTPException(status_code=400, detail="X-Customer-ID header is required")
    return x_customer_id


def get_scanning_service() -> ScanningService:
    """Dependency to get scanning service instance"""
    return ScanningService()


# ============================================================================
# SCAN PROFILES ENDPOINTS (7 endpoints)
# ============================================================================

@router.post("/profiles", response_model=ScanProfileResponse, status_code=201)
async def create_scan_profile(
    profile: ScanProfileCreate,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Create a new scan profile"""
    return await service.create_profile(customer_id, profile)


@router.get("/profiles/{profile_id}", response_model=ScanProfileResponse)
async def get_scan_profile(
    profile_id: str,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Get scan profile by ID"""
    return await service.get_profile(customer_id, profile_id)


@router.put("/profiles/{profile_id}", response_model=ScanProfileResponse)
async def update_scan_profile(
    profile_id: str,
    profile_update: ScanProfileUpdate,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Update scan profile"""
    return await service.update_profile(customer_id, profile_id, profile_update)


@router.delete("/profiles/{profile_id}", status_code=204)
async def delete_scan_profile(
    profile_id: str,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Delete scan profile"""
    await service.delete_profile(customer_id, profile_id)


@router.get("/profiles", response_model=List[ScanProfileResponse])
async def list_scan_profiles(
    customer_id: str = Depends(get_customer_id),
    scan_type: Optional[ScanType] = None,
    enabled: Optional[bool] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: ScanningService = Depends(get_scanning_service)
):
    """List scan profiles with optional filters"""
    return await service.list_profiles(customer_id, scan_type, enabled, limit, offset)


@router.get("/profiles/by-type/{scan_type}", response_model=List[ScanProfileResponse])
async def get_profiles_by_type(
    scan_type: ScanType,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Get all profiles of a specific scan type"""
    return await service.get_profiles_by_type(customer_id, scan_type)


@router.post("/profiles/{profile_id}/clone", response_model=ScanProfileResponse, status_code=201)
async def clone_scan_profile(
    profile_id: str,
    new_name: str = Query(..., description="Name for cloned profile"),
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Clone an existing scan profile"""
    return await service.clone_profile(customer_id, profile_id, new_name)


# ============================================================================
# SCHEDULES ENDPOINTS (7 endpoints)
# ============================================================================

@router.post("/schedules", response_model=ScheduleResponse, status_code=201)
async def create_schedule(
    schedule: ScheduleCreate,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Create a new scan schedule"""
    return await service.create_schedule(customer_id, schedule)


@router.get("/schedules/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: str,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Get schedule by ID"""
    return await service.get_schedule(customer_id, schedule_id)


@router.put("/schedules/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: str,
    schedule_update: ScheduleUpdate,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Update scan schedule"""
    return await service.update_schedule(customer_id, schedule_id, schedule_update)


@router.delete("/schedules/{schedule_id}", status_code=204)
async def delete_schedule(
    schedule_id: str,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Delete scan schedule"""
    await service.delete_schedule(customer_id, schedule_id)


@router.get("/schedules", response_model=List[ScheduleResponse])
async def list_schedules(
    customer_id: str = Depends(get_customer_id),
    enabled: Optional[bool] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: ScanningService = Depends(get_scanning_service)
):
    """List scan schedules with optional filters"""
    return await service.list_schedules(customer_id, enabled, limit, offset)


@router.post("/schedules/{schedule_id}/enable", response_model=ScheduleResponse)
async def enable_schedule(
    schedule_id: str,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Enable a scan schedule"""
    return await service.toggle_schedule(customer_id, schedule_id, enabled=True)


@router.post("/schedules/{schedule_id}/disable", response_model=ScheduleResponse)
async def disable_schedule(
    schedule_id: str,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Disable a scan schedule"""
    return await service.toggle_schedule(customer_id, schedule_id, enabled=False)


# ============================================================================
# SCAN JOBS ENDPOINTS (7 endpoints)
# ============================================================================

@router.post("/jobs", response_model=ScanJobResponse, status_code=201)
async def start_scan_job(
    job: ScanJobCreate,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Start a new scan job"""
    return await service.start_job(customer_id, job)


@router.get("/jobs/{job_id}", response_model=ScanJobResponse)
async def get_scan_job_status(
    job_id: str,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Get scan job status and details"""
    return await service.get_job(customer_id, job_id)


@router.get("/jobs", response_model=List[ScanJobResponse])
async def list_scan_jobs(
    customer_id: str = Depends(get_customer_id),
    status: Optional[ScanStatus] = None,
    profile_id: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: ScanningService = Depends(get_scanning_service)
):
    """List scan jobs with optional filters"""
    return await service.list_jobs(customer_id, status, profile_id, limit, offset)


@router.post("/jobs/{job_id}/cancel", response_model=ScanJobResponse)
async def cancel_scan_job(
    job_id: str,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Cancel a running scan job"""
    return await service.cancel_job(customer_id, job_id)


@router.get("/jobs/{job_id}/findings", response_model=List[FindingResponse])
async def get_job_findings(
    job_id: str,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Get all findings for a specific job"""
    return await service.get_job_findings(customer_id, job_id)


@router.get("/jobs/running", response_model=List[ScanJobResponse])
async def list_running_jobs(
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """List all currently running scan jobs"""
    return await service.list_running_jobs(customer_id)


# ============================================================================
# FINDINGS ENDPOINTS (6 endpoints)
# ============================================================================

@router.get("/findings", response_model=List[FindingResponse])
async def list_findings(
    customer_id: str = Depends(get_customer_id),
    severity: Optional[List[FindingSeverity]] = Query(None),
    status: Optional[List[FindingStatus]] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: ScanningService = Depends(get_scanning_service)
):
    """List all findings with optional filters"""
    return await service.list_findings(customer_id, severity, status, limit, offset)


@router.get("/findings/{finding_id}", response_model=FindingResponse)
async def get_finding(
    finding_id: str,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Get finding by ID"""
    return await service.get_finding(customer_id, finding_id)


@router.put("/findings/{finding_id}/status", response_model=FindingResponse)
async def update_finding_status(
    finding_id: str,
    status_update: FindingStatusUpdate,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Update finding status"""
    return await service.update_finding_status(customer_id, finding_id, status_update)


@router.get("/findings/by-severity/{severity}", response_model=List[FindingResponse])
async def get_findings_by_severity(
    severity: FindingSeverity,
    customer_id: str = Depends(get_customer_id),
    limit: int = Query(100, ge=1, le=1000),
    service: ScanningService = Depends(get_scanning_service)
):
    """Get findings by severity level"""
    return await service.get_findings_by_severity(customer_id, severity, limit)


@router.post("/findings/search", response_model=List[FindingResponse])
async def search_findings(
    search_request: FindingSearchRequest,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Search findings with advanced filters"""
    return await service.search_findings(customer_id, search_request)


# ============================================================================
# TARGETS ENDPOINTS (4 endpoints)
# ============================================================================

@router.post("/targets", response_model=TargetResponse, status_code=201)
async def create_target(
    target: TargetCreate,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Create a new scan target"""
    return await service.create_target(customer_id, target)


@router.get("/targets", response_model=List[TargetResponse])
async def list_targets(
    customer_id: str = Depends(get_customer_id),
    target_type: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: ScanningService = Depends(get_scanning_service)
):
    """List scan targets with optional filters"""
    return await service.list_targets(customer_id, target_type, limit, offset)


@router.put("/targets/{target_id}", response_model=TargetResponse)
async def update_target(
    target_id: str,
    target_update: TargetUpdate,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Update scan target"""
    return await service.update_target(customer_id, target_id, target_update)


@router.delete("/targets/{target_id}", status_code=204)
async def delete_target(
    target_id: str,
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Delete scan target"""
    await service.delete_target(customer_id, target_id)


# ============================================================================
# DASHBOARD ENDPOINT (1 endpoint)
# ============================================================================

@router.get("/dashboard/summary", response_model=DashboardSummary)
async def get_dashboard_summary(
    customer_id: str = Depends(get_customer_id),
    service: ScanningService = Depends(get_scanning_service)
):
    """Get comprehensive scanning dashboard summary"""
    return await service.get_dashboard_summary(customer_id)
