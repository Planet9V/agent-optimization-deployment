"""
Vendor Equipment Module for NER11 Gold Model
=============================================

E15: Vendor Equipment Lifecycle Management
Phase B2 - Supply Chain

Provides comprehensive vendor equipment tracking and lifecycle management,
including EOL monitoring, vendor risk assessment, and supply chain vulnerability tracking.

Version: 1.0.0
Created: 2025-12-04
"""

from .vendor_models import (
    Vendor,
    EquipmentModel,
    SupportContract,
    VendorRiskLevel,
    SupportStatus,
    LifecycleStatus,
    MaintenanceSchedule,
    AlertSeverity,
    AlertType,
    EOLAlert,
    # Day 7-9: Maintenance Scheduling
    MaintenanceWindowType,
    MaintenanceWindow,
    MaintenancePrediction,
    WorkOrderStatus,
    WorkOrderPriority,
    MaintenanceWorkOrder,
)
from .vendor_service import (
    VendorEquipmentService,
    CVERecord,
    VulnerabilityAlert,
    SemanticSearchResult,
    SimilarityMatch,
    VendorSearchRequest,
    VendorSearchResult,
    EquipmentSearchRequest,
    EquipmentSearchResult,
    VendorRiskSummary,
)
from .embedding_service import EmbeddingService, get_embedding_service

# Optional FastAPI router (only import if FastAPI is available)
try:
    from .vendor_router import router as vendor_router
    _FASTAPI_AVAILABLE = True
except ImportError:
    vendor_router = None
    _FASTAPI_AVAILABLE = False

__all__ = [
    # Models
    "Vendor",
    "EquipmentModel",
    "SupportContract",
    "VendorRiskLevel",
    "SupportStatus",
    "LifecycleStatus",
    "MaintenanceSchedule",
    "AlertSeverity",
    "AlertType",
    "EOLAlert",
    # Day 7-9: Maintenance Scheduling
    "MaintenanceWindowType",
    "MaintenanceWindow",
    "MaintenancePrediction",
    "WorkOrderStatus",
    "WorkOrderPriority",
    "MaintenanceWorkOrder",
    # Services
    "VendorEquipmentService",
    "EmbeddingService",
    "get_embedding_service",
    # CVE Types
    "CVERecord",
    "VulnerabilityAlert",
    "SemanticSearchResult",
    "SimilarityMatch",
    "VendorSearchRequest",
    "VendorSearchResult",
    "EquipmentSearchRequest",
    "EquipmentSearchResult",
    "VendorRiskSummary",
    # Router (optional)
    "vendor_router",
]
