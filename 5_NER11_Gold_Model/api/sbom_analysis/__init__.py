"""
SBOM Analysis Module
====================

E03: SBOM Dependency & Vulnerability Tracking for NER11 Gold Model.

This module provides:
- SoftwareComponent: Individual software package tracking with purl/cpe
- SBOM: Software Bill of Materials document management
- SoftwareVulnerability: CVE tracking with CVSS and EPSS scoring
- DependencyRelation: Dependency graph relationships
- License compliance analysis
- Vulnerability correlation with equipment
- SBOMAnalysisService: Full CRUD and analytics with Qdrant
- FastAPI Router: REST API endpoints for all operations

Version: 1.4.0
Created: 2025-12-04
Updated: 2025-12-04 - Added FastAPI router (Day 5)
"""

from api.sbom_analysis.sbom_models import (
    # Enums
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
    # Core Models
    SoftwareComponent,
    SBOM,
    SoftwareVulnerability,
    DependencyRelation,
    LicenseComplianceResult,
    DependencyGraphNode,
)

from api.sbom_analysis.sbom_service import (
    # Service
    SBOMAnalysisService,
    # Request/Response Types
    ComponentSearchRequest,
    ComponentSearchResult,
    VulnerabilitySearchRequest,
    VulnerabilitySearchResult,
    SBOMSearchRequest,
    SBOMSearchResult,
    DependencyPath,
    ImpactAnalysis,
    RiskSummary,
)

# Router import is conditional - FastAPI may not be installed
try:
    from api.sbom_analysis.sbom_router import router as sbom_router
    _ROUTER_AVAILABLE = True
except ImportError:
    sbom_router = None
    _ROUTER_AVAILABLE = False

__all__ = [
    # Enums
    "SBOMFormat",
    "ComponentType",
    "LicenseType",
    "LicenseRisk",
    "DependencyType",
    "DependencyScope",
    "VulnerabilitySeverity",
    "ExploitMaturity",
    "RemediationType",
    "ComponentStatus",
    # Core Models
    "SoftwareComponent",
    "SBOM",
    "SoftwareVulnerability",
    "DependencyRelation",
    "LicenseComplianceResult",
    "DependencyGraphNode",
    # Service
    "SBOMAnalysisService",
    # Request/Response Types
    "ComponentSearchRequest",
    "ComponentSearchResult",
    "VulnerabilitySearchRequest",
    "VulnerabilitySearchResult",
    "SBOMSearchRequest",
    "SBOMSearchResult",
    "DependencyPath",
    "ImpactAnalysis",
    "RiskSummary",
    # Router (conditional)
    "sbom_router",
]

__version__ = "1.4.0"
