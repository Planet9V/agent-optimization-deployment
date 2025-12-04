"""
Threat Intelligence API Module
===============================

API module for E04: Threat Intelligence Correlation.
Provides threat actor tracking, campaign analysis, MITRE ATT&CK mapping,
and IOC management.

Version: 1.0.0
Created: 2025-12-04
"""

from .threat_models import (
    # Enums
    ActorType,
    ActorMotivation,
    CampaignStatus,
    IOCType,
    MitigationStatus,
    FeedType,

    # Models
    ThreatActor,
    ThreatCampaign,
    MITREMapping,
    ThreatIntelFeed,
    IOC,
)

__all__ = [
    # Enums
    "ActorType",
    "ActorMotivation",
    "CampaignStatus",
    "IOCType",
    "MitigationStatus",
    "FeedType",

    # Models
    "ThreatActor",
    "ThreatCampaign",
    "MITREMapping",
    "ThreatIntelFeed",
    "IOC",
]
