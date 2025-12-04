"""
E11 Psychohistory Demographics Baseline API
============================================

FastAPI module for psychohistory demographics baseline.
Provides population analytics, workforce modeling, organization structure analysis.

Foundation for advanced psychometric modules (E19-E25).

Version: 1.0.0
Created: 2025-12-04
"""

from .router import router as demographics_router
from .service import DemographicsService
from .schemas import (
    PopulationProfile,
    WorkforceComposition,
    OrganizationUnit,
    BaselineMetrics,
)

__all__ = [
    "demographics_router",
    "DemographicsService",
    "PopulationProfile",
    "WorkforceComposition",
    "OrganizationUnit",
    "BaselineMetrics",
]
