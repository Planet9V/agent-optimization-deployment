"""
Alert Management API Module
============================

E09: Alert Management API for NER11 Gold Model.
Provides alert lifecycle management, rules, notifications, escalation,
and correlation capabilities with customer isolation.

Version: 1.0.0
Created: 2025-12-04
"""

from .alert_router import router as alert_router
from .alert_service import AlertService

__all__ = [
    "alert_router",
    "AlertService",
]
