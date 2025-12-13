"""
Pydantic models for SBOM API
Uses latest Pydantic v2 syntax with ConfigDict
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, ConfigDict
from uuid import uuid4


class Component(BaseModel):
    """Software component in an SBOM"""
    model_config = ConfigDict(str_strip_whitespace=True)

    component_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., min_length=1, max_length=255)
    version: str = Field(..., min_length=1, max_length=100)
    purl: Optional[str] = Field(None, description="Package URL")
    cpe: Optional[str] = Field(None, description="Common Platform Enumeration")
    license: Optional[str] = Field(None, max_length=100)
    supplier: Optional[str] = Field(None, max_length=255)
    dependencies: List[str] = Field(default_factory=list, description="Component IDs this depends on")


class VulnerabilitySummary(BaseModel):
    """Summary of vulnerabilities for a component"""
    model_config = ConfigDict(frozen=False)

    cve_id: str
    cvss_score: float = Field(..., ge=0.0, le=10.0)
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
    exploitability_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    epss_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class SBOMAnalyzeRequest(BaseModel):
    """Request body for SBOM analysis"""
    model_config = ConfigDict(str_strip_whitespace=True)

    format: Literal["cyclonedx", "spdx"] = Field(..., description="SBOM format")
    content: Dict[str, Any] = Field(..., description="SBOM JSON content")
    project_name: str = Field(..., min_length=1, max_length=255)
    project_version: Optional[str] = Field("1.0.0", max_length=50)


class SBOMAnalyzeResponse(BaseModel):
    """Response from SBOM analysis"""
    model_config = ConfigDict(frozen=False)

    sbom_id: str
    project_name: str
    components_count: int = Field(..., ge=0)
    vulnerabilities_count: int = Field(0, ge=0)
    created_at: datetime
    customer_id: str
    message: str = "SBOM analyzed successfully"


class SBOMDetailResponse(BaseModel):
    """Detailed SBOM information"""
    model_config = ConfigDict(frozen=False)

    sbom_id: str
    project_name: str
    project_version: str
    format: str
    components_count: int
    vulnerabilities_count: int
    high_severity_count: int = 0
    critical_severity_count: int = 0
    created_at: datetime
    customer_id: str
    components: List[Component] = Field(default_factory=list)


class SBOMSummaryResponse(BaseModel):
    """Aggregate SBOM statistics"""
    model_config = ConfigDict(frozen=False)

    total_sboms: int = Field(..., ge=0)
    total_components: int = Field(..., ge=0)
    total_vulnerabilities: int = Field(..., ge=0)
    critical_vulnerabilities: int = Field(0, ge=0)
    high_vulnerabilities: int = Field(0, ge=0)
    medium_vulnerabilities: int = Field(0, ge=0)
    low_vulnerabilities: int = Field(0, ge=0)
    customer_id: str
    last_updated: datetime


class ComponentSearchRequest(BaseModel):
    """Request for semantic component search"""
    model_config = ConfigDict(str_strip_whitespace=True)

    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(10, ge=1, le=100)
    similarity_threshold: float = Field(0.7, ge=0.0, le=1.0)


class ComponentSearchResult(BaseModel):
    """Single component search result"""
    model_config = ConfigDict(frozen=False)

    component_id: str
    name: str
    version: str
    sbom_id: str
    project_name: str
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    vulnerabilities_count: int = 0


class ComponentSearchResponse(BaseModel):
    """Response from component search"""
    model_config = ConfigDict(frozen=False)

    results: List[ComponentSearchResult] = Field(default_factory=list)
    total_results: int = Field(..., ge=0)
    query: str
    customer_id: str


class ErrorResponse(BaseModel):
    """Standard error response"""
    model_config = ConfigDict(frozen=False)

    error: str
    detail: Optional[str] = None
    customer_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
