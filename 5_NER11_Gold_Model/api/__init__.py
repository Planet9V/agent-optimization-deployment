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

Version: 4.0.0
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
]
