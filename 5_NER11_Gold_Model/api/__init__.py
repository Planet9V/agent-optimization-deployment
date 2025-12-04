"""
NER11 Gold Model API Package
============================

FastAPI routes and services for NER11 Gold Standard Model.

Modules:
- customer_isolation: Multi-tenant customer isolation for semantic search
- vendor_equipment: E15 Vendor Equipment Lifecycle Management API
- sbom_analysis: E03 SBOM Dependency & Vulnerability Tracking API
- threat_intelligence: E04 Threat Intelligence Correlation API
- risk_scoring: E05 Risk Scoring Engine API
- remediation: E06 Remediation Workflow API
- compliance_mapping: E07 Compliance & Framework Mapping API
- automated_scanning: E08 Automated Scanning & Testing API
- alert_management: E09 Alert Management API
- economic_impact: E10 Economic Impact Modeling API
- demographics: E11 Psychohistory Demographics Baseline API
- prioritization: E12 Prioritization & Urgency Ranking API

Version: 5.2.0
Updated: 2025-12-04
"""

from .customer_isolation import (
    CustomerContext,
    CustomerAccessLevel,
    CustomerIsolatedSemanticService,
    CustomerSemanticSearchRequest,
    CustomerSemanticSearchResponse,
)

# Phase B2 APIs
from .vendor_equipment import vendor_router, VendorEquipmentService
from .sbom_analysis import sbom_router, SBOMAnalysisService

# Phase B3 APIs
from .threat_intelligence import threat_router, ThreatIntelligenceService
from .risk_scoring import risk_router, RiskScoringService
from .remediation import remediation_router, RemediationService
from .demographics import demographics_router, DemographicsService

# Phase B4 APIs
from .compliance_mapping import compliance_router, ComplianceService
from .automated_scanning import scanning_router, ScanningService
from .alert_management import alert_router, AlertService
from .economic_impact import router as economic_router
from .prioritization import router as prioritization_router

__all__ = [
    # Customer Isolation
    "CustomerContext",
    "CustomerAccessLevel",
    "CustomerIsolatedSemanticService",
    "CustomerSemanticSearchRequest",
    "CustomerSemanticSearchResponse",
    # Phase B2 APIs
    "vendor_router",
    "VendorEquipmentService",
    "sbom_router",
    "SBOMAnalysisService",
    # Phase B3 APIs
    "threat_router",
    "ThreatIntelligenceService",
    "risk_router",
    "RiskScoringService",
    "remediation_router",
    "RemediationService",
    "demographics_router",
    "DemographicsService",
    # Phase B4 APIs
    "compliance_router",
    "ComplianceService",
    "scanning_router",
    "ScanningService",
    "alert_router",
    "AlertService",
    "economic_router",
    "prioritization_router",
]
