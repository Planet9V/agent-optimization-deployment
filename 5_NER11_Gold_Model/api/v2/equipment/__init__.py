"""
Equipment API v2 Module
File: __init__.py
Created: 2025-12-12 05:00:00 UTC
Version: v1.0.0
Purpose: Equipment management API endpoints
"""

from .create import router as create_router
from .retrieve import router as retrieve_router
from .summary import router as summary_router
from .eol_report import router as eol_router

__all__ = ['create_router', 'retrieve_router', 'summary_router', 'eol_router']
