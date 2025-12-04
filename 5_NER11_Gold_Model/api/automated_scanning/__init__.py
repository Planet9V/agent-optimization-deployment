"""
E08 Automated Scanning Module
Provides automated security scanning capabilities with 30 REST endpoints
"""
from .scanning_router import router as scanning_router
from .scanning_service import ScanningService

__all__ = ["scanning_router", "ScanningService"]
