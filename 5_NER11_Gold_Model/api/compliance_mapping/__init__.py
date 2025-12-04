"""
Compliance Mapping API Module
==============================

API module for E07: Compliance Framework Mapping.
Provides compliance control management, framework mappings, assessments,
evidence tracking, and gap analysis.

Version: 1.0.0
Created: 2025-12-04
"""

from .compliance_router import router as compliance_router
from .compliance_service import ComplianceService, ControlSearchRequest, AssessmentSearchRequest

__all__ = [
    "compliance_router",
    "ComplianceService",
    "ControlSearchRequest",
    "AssessmentSearchRequest",
]
