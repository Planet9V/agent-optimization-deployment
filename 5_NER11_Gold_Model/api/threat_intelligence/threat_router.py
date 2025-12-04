"""
Threat Intelligence Correlation API Router
==========================================

FastAPI router for E04: Threat Intelligence Correlation.
Provides REST endpoints for threat actors, campaigns, IOCs, and MITRE ATT&CK mappings.

Version: 1.0.0
Created: 2025-12-04
"""

from datetime import date, datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Header, Depends
from pydantic import BaseModel, Field
import logging

from ..customer_isolation import (
    CustomerContext,
    CustomerContextManager,
    CustomerAccessLevel,
)
from .threat_service import (
    ThreatIntelligenceService,
    ThreatActorSearchRequest,
    CampaignSearchRequest,
    IOCSearchRequest,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/threat-intel", tags=["threat-intelligence"])


# =============================================================================
# Pydantic Request/Response Models
# =============================================================================


# ===== Threat Actor Models =====

class ThreatActorCreate(BaseModel):
    """Request model for threat actor creation."""
    actor_id: str = Field(..., description="Unique actor identifier")
    name: str = Field(..., description="Threat actor name")
    aliases: List[str] = Field(default_factory=list, description="Known aliases")
    actor_type: str = Field("apt", description="Type: apt, cybercrime, hacktivism, nation_state, insider")
    country: Optional[str] = Field(None, description="Country of origin")
    motivation: List[str] = Field(default_factory=list, description="Motivations: financial, espionage, disruption, etc.")
    sophistication: str = Field("medium", description="Sophistication: low, medium, high, advanced")
    target_sectors: List[str] = Field(default_factory=list, description="Target industry sectors")
    target_regions: List[str] = Field(default_factory=list, description="Target geographic regions")
    first_seen: Optional[date] = Field(None, description="First observed date")
    description: Optional[str] = Field(None, description="Actor description")


class ThreatActorResponse(BaseModel):
    """Response model for threat actor data."""
    actor_id: str
    name: str
    customer_id: str
    aliases: List[str]
    actor_type: str
    country: Optional[str]
    motivation: List[str]
    sophistication: str
    target_sectors: List[str]
    target_regions: List[str]
    first_seen: Optional[date]
    is_active: bool
    campaign_count: int
    cve_count: int
    ioc_count: int


class ThreatActorSearchResponse(BaseModel):
    """Response for threat actor search results."""
    total_results: int
    customer_id: str
    results: List[ThreatActorResponse]


# ===== Campaign Models =====

class CampaignCreate(BaseModel):
    """Request model for campaign creation."""
    campaign_id: str = Field(..., description="Unique campaign identifier")
    name: str = Field(..., description="Campaign name")
    threat_actor_ids: List[str] = Field(default_factory=list, description="Associated threat actors")
    start_date: Optional[date] = Field(None, description="Campaign start date")
    end_date: Optional[date] = Field(None, description="Campaign end date (if concluded)")
    target_sectors: List[str] = Field(default_factory=list, description="Target sectors")
    target_regions: List[str] = Field(default_factory=list, description="Target regions")
    description: Optional[str] = Field(None, description="Campaign description")
    ttps: List[str] = Field(default_factory=list, description="MITRE ATT&CK technique IDs")


class CampaignResponse(BaseModel):
    """Response model for campaign data."""
    campaign_id: str
    name: str
    customer_id: str
    threat_actor_ids: List[str]
    start_date: Optional[date]
    end_date: Optional[date]
    target_sectors: List[str]
    target_regions: List[str]
    is_active: bool
    ioc_count: int
    cve_count: int


class CampaignSearchResponse(BaseModel):
    """Response for campaign search results."""
    total_results: int
    customer_id: str
    results: List[CampaignResponse]


# ===== IOC Models =====

class IOCCreate(BaseModel):
    """Request model for IOC creation."""
    ioc_id: str = Field(..., description="Unique IOC identifier")
    ioc_type: str = Field(..., description="Type: ip, domain, url, hash, email, file_path, registry_key")
    value: str = Field(..., description="IOC value")
    threat_actor_id: Optional[str] = Field(None, description="Associated threat actor")
    campaign_id: Optional[str] = Field(None, description="Associated campaign")
    first_seen: Optional[date] = Field(None, description="First observed date")
    last_seen: Optional[date] = Field(None, description="Last observed date")
    confidence: int = Field(50, ge=0, le=100, description="Confidence score 0-100")
    description: Optional[str] = Field(None, description="IOC description")
    tags: List[str] = Field(default_factory=list, description="Classification tags")


class IOCResponse(BaseModel):
    """Response model for IOC data."""
    ioc_id: str
    customer_id: str
    ioc_type: str
    value: str
    threat_actor_id: Optional[str]
    campaign_id: Optional[str]
    first_seen: Optional[date]
    last_seen: Optional[date]
    confidence: int
    is_active: bool
    tags: List[str]


class IOCSearchResponse(BaseModel):
    """Response for IOC search results."""
    total_results: int
    customer_id: str
    results: List[IOCResponse]


class IOCBulkImport(BaseModel):
    """Request for bulk IOC import."""
    iocs: List[IOCCreate] = Field(..., description="List of IOCs to import")


class IOCBulkImportResponse(BaseModel):
    """Response for bulk IOC import."""
    imported_count: int
    failed_count: int
    failed_iocs: List[dict]


# ===== MITRE ATT&CK Models =====

class MITREMappingCreate(BaseModel):
    """Request model for MITRE ATT&CK mapping creation."""
    mapping_id: str = Field(..., description="Unique mapping identifier")
    technique_id: str = Field(..., description="MITRE technique ID (e.g., T1566)")
    technique_name: str = Field(..., description="Technique name")
    tactic: str = Field(..., description="MITRE tactic")
    entity_type: str = Field(..., description="Entity type: threat_actor, campaign, cve")
    entity_id: str = Field(..., description="Entity ID")
    description: Optional[str] = Field(None, description="Usage description")


class MITREMappingResponse(BaseModel):
    """Response model for MITRE mapping."""
    mapping_id: str
    customer_id: str
    technique_id: str
    technique_name: str
    tactic: str
    entity_type: str
    entity_id: str


class MITREMappingSearchResponse(BaseModel):
    """Response for MITRE mapping search results."""
    total_results: int
    customer_id: str
    results: List[MITREMappingResponse]


class MITRECoverageResponse(BaseModel):
    """Response for MITRE ATT&CK coverage summary."""
    customer_id: str
    total_techniques: int
    covered_techniques: int
    coverage_percentage: float
    tactics_coverage: dict
    top_techniques: List[dict]


class MITREGapsResponse(BaseModel):
    """Response for MITRE coverage gaps."""
    customer_id: str
    uncovered_techniques: int
    critical_gaps: List[dict]
    recommendations: List[str]


# ===== Threat Feed Models =====

class ThreatFeedCreate(BaseModel):
    """Request model for threat feed creation."""
    feed_id: str = Field(..., description="Unique feed identifier")
    name: str = Field(..., description="Feed name")
    feed_url: str = Field(..., description="Feed URL")
    feed_type: str = Field("osint", description="Type: osint, commercial, internal, custom")
    refresh_interval: int = Field(3600, ge=60, description="Refresh interval in seconds")
    enabled: bool = Field(True, description="Is feed enabled?")


class ThreatFeedResponse(BaseModel):
    """Response model for threat feed."""
    feed_id: str
    name: str
    customer_id: str
    feed_url: str
    feed_type: str
    refresh_interval: int
    enabled: bool
    last_refresh: Optional[datetime]


class ThreatFeedListResponse(BaseModel):
    """Response for listing threat feeds."""
    total_results: int
    customer_id: str
    feeds: List[ThreatFeedResponse]


# ===== Dashboard Models =====

class ThreatIntelSummaryResponse(BaseModel):
    """Response for threat intelligence dashboard summary."""
    customer_id: str
    total_threat_actors: int
    active_campaigns: int
    total_iocs: int
    active_iocs: int
    total_cves: int
    mitre_coverage: float
    high_confidence_iocs: int
    recent_activity_count: int


# =============================================================================
# Dependencies
# =============================================================================


def get_service() -> ThreatIntelligenceService:
    """Get threat intelligence service instance."""
    return ThreatIntelligenceService()


def require_customer_context(
    x_customer_id: str = Header(..., description="Customer identifier"),
    x_namespace: Optional[str] = Header(None, description="Customer namespace"),
    x_user_id: Optional[str] = Header(None, description="User identifier"),
    x_access_level: Optional[str] = Header("read", description="Access level"),
) -> CustomerContext:
    """Extract and set customer context from headers."""
    try:
        access_level = CustomerAccessLevel(x_access_level.lower())
    except ValueError:
        access_level = CustomerAccessLevel.READ

    context = CustomerContextManager.create_context(
        customer_id=x_customer_id,
        namespace=x_namespace,
        access_level=access_level,
        user_id=x_user_id,
    )
    return context


# =============================================================================
# Threat Actor Endpoints
# =============================================================================


@router.post("/actors", response_model=ThreatActorResponse, status_code=201)
async def create_threat_actor(
    actor_data: ThreatActorCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """
    Create a new threat actor.

    Requires WRITE access level.
    """
    try:
        from .threat_models import ThreatActor, ActorType, SophisticationLevel

        actor = ThreatActor(
            actor_id=actor_data.actor_id,
            name=actor_data.name,
            customer_id=context.customer_id,
            aliases=actor_data.aliases,
            actor_type=ActorType(actor_data.actor_type),
            country=actor_data.country,
            motivation=actor_data.motivation,
            sophistication=SophisticationLevel(actor_data.sophistication),
            target_sectors=actor_data.target_sectors,
            target_regions=actor_data.target_regions,
            first_seen=actor_data.first_seen,
            description=actor_data.description,
        )
        created = service.create_threat_actor(actor)

        return ThreatActorResponse(
            actor_id=created.actor_id,
            name=created.name,
            customer_id=created.customer_id,
            aliases=created.aliases,
            actor_type=created.actor_type.value,
            country=created.country,
            motivation=created.motivation,
            sophistication=created.sophistication.value,
            target_sectors=created.target_sectors,
            target_regions=created.target_regions,
            first_seen=created.first_seen,
            is_active=created.is_active,
            campaign_count=created.campaign_count,
            cve_count=created.cve_count,
            ioc_count=created.ioc_count,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/actors/{actor_id}", response_model=ThreatActorResponse)
async def get_threat_actor(
    actor_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get threat actor by ID with customer isolation."""
    actor = service.get_threat_actor(actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail=f"Threat actor {actor_id} not found")

    return ThreatActorResponse(
        actor_id=actor.actor_id,
        name=actor.name,
        customer_id=actor.customer_id,
        aliases=actor.aliases,
        actor_type=actor.actor_type.value if hasattr(actor.actor_type, 'value') else actor.actor_type,
        country=actor.country,
        motivation=actor.motivation,
        sophistication=actor.sophistication.value if hasattr(actor.sophistication, 'value') else actor.sophistication,
        target_sectors=actor.target_sectors,
        target_regions=actor.target_regions,
        first_seen=actor.first_seen,
        is_active=actor.is_active,
        campaign_count=actor.campaign_count,
        cve_count=actor.cve_count,
        ioc_count=actor.ioc_count,
    )


@router.get("/actors/search", response_model=ThreatActorSearchResponse)
async def search_threat_actors(
    query: Optional[str] = Query(None, description="Semantic search query"),
    actor_type: Optional[str] = Query(None, description="Filter by actor type"),
    country: Optional[str] = Query(None, description="Filter by country"),
    target_sector: Optional[str] = Query(None, description="Filter by target sector"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    include_system: bool = Query(True, description="Include SYSTEM actors"),
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Search threat actors with semantic search and filters."""
    try:
        request = ThreatActorSearchRequest(
            query=query,
            customer_id=context.customer_id,
            actor_type=actor_type,
            country=country,
            target_sector=target_sector,
            is_active=is_active,
            limit=limit,
            include_system=include_system,
        )
        results = service.search_threat_actors(request)

        actor_responses = [
            ThreatActorResponse(
                actor_id=r.actor.actor_id,
                name=r.actor.name,
                customer_id=r.actor.customer_id,
                aliases=r.actor.aliases,
                actor_type=r.actor.actor_type.value if hasattr(r.actor.actor_type, 'value') else r.actor.actor_type,
                country=r.actor.country,
                motivation=r.actor.motivation,
                sophistication=r.actor.sophistication.value if hasattr(r.actor.sophistication, 'value') else r.actor.sophistication,
                target_sectors=r.actor.target_sectors,
                target_regions=r.actor.target_regions,
                first_seen=r.actor.first_seen,
                is_active=r.actor.is_active,
                campaign_count=r.actor.campaign_count,
                cve_count=r.actor.cve_count,
                ioc_count=r.actor.ioc_count,
            )
            for r in results
        ]

        return ThreatActorSearchResponse(
            total_results=len(actor_responses),
            customer_id=context.customer_id,
            results=actor_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/actors/active", response_model=ThreatActorSearchResponse)
async def get_active_threat_actors(
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get all currently active threat actors."""
    results = service.get_active_threat_actors()

    actor_responses = [
        ThreatActorResponse(
            actor_id=r.actor.actor_id,
            name=r.actor.name,
            customer_id=r.actor.customer_id,
            aliases=r.actor.aliases,
            actor_type=r.actor.actor_type.value if hasattr(r.actor.actor_type, 'value') else r.actor.actor_type,
            country=r.actor.country,
            motivation=r.actor.motivation,
            sophistication=r.actor.sophistication.value if hasattr(r.actor.sophistication, 'value') else r.actor.sophistication,
            target_sectors=r.actor.target_sectors,
            target_regions=r.actor.target_regions,
            first_seen=r.actor.first_seen,
            is_active=r.actor.is_active,
            campaign_count=r.actor.campaign_count,
            cve_count=r.actor.cve_count,
            ioc_count=r.actor.ioc_count,
        )
        for r in results
    ]

    return ThreatActorSearchResponse(
        total_results=len(actor_responses),
        customer_id=context.customer_id,
        results=actor_responses,
    )


@router.get("/actors/by-sector/{sector}", response_model=ThreatActorSearchResponse)
async def get_actors_by_sector(
    sector: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get threat actors targeting a specific sector."""
    results = service.get_actors_by_sector(sector)

    actor_responses = [
        ThreatActorResponse(
            actor_id=r.actor.actor_id,
            name=r.actor.name,
            customer_id=r.actor.customer_id,
            aliases=r.actor.aliases,
            actor_type=r.actor.actor_type.value if hasattr(r.actor.actor_type, 'value') else r.actor.actor_type,
            country=r.actor.country,
            motivation=r.actor.motivation,
            sophistication=r.actor.sophistication.value if hasattr(r.actor.sophistication, 'value') else r.actor.sophistication,
            target_sectors=r.actor.target_sectors,
            target_regions=r.actor.target_regions,
            first_seen=r.actor.first_seen,
            is_active=r.actor.is_active,
            campaign_count=r.actor.campaign_count,
            cve_count=r.actor.cve_count,
            ioc_count=r.actor.ioc_count,
        )
        for r in results
    ]

    return ThreatActorSearchResponse(
        total_results=len(actor_responses),
        customer_id=context.customer_id,
        results=actor_responses,
    )


@router.get("/actors/{actor_id}/campaigns")
async def get_actor_campaigns(
    actor_id: str,
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get campaigns associated with a threat actor."""
    campaigns = service.get_actor_campaigns(actor_id, limit)

    return {
        "actor_id": actor_id,
        "customer_id": context.customer_id,
        "total_campaigns": len(campaigns),
        "campaigns": campaigns,
    }


@router.get("/actors/{actor_id}/cves")
async def get_actor_cves(
    actor_id: str,
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get CVEs associated with a threat actor."""
    cves = service.get_actor_cves(actor_id, limit)

    return {
        "actor_id": actor_id,
        "customer_id": context.customer_id,
        "total_cves": len(cves),
        "cves": cves,
    }


# =============================================================================
# Campaign Endpoints
# =============================================================================


@router.post("/campaigns", response_model=CampaignResponse, status_code=201)
async def create_campaign(
    campaign_data: CampaignCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """
    Create a new campaign.

    Requires WRITE access level.
    """
    try:
        from .threat_models import ThreatCampaign

        campaign = ThreatCampaign(
            campaign_id=campaign_data.campaign_id,
            name=campaign_data.name,
            customer_id=context.customer_id,
            threat_actor_ids=campaign_data.threat_actor_ids,
            start_date=campaign_data.start_date,
            end_date=campaign_data.end_date,
            target_sectors=campaign_data.target_sectors,
            target_regions=campaign_data.target_regions,
            description=campaign_data.description,
            ttps=campaign_data.ttps,
        )
        created = service.create_campaign(campaign)

        return CampaignResponse(
            campaign_id=created.campaign_id,
            name=created.name,
            customer_id=created.customer_id,
            threat_actor_ids=created.threat_actor_ids,
            start_date=created.start_date,
            end_date=created.end_date,
            target_sectors=created.target_sectors,
            target_regions=created.target_regions,
            is_active=created.is_active,
            ioc_count=created.ioc_count,
            cve_count=created.cve_count,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/campaigns/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get campaign by ID with customer isolation."""
    campaign = service.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail=f"Campaign {campaign_id} not found")

    return CampaignResponse(
        campaign_id=campaign.campaign_id,
        name=campaign.name,
        customer_id=campaign.customer_id,
        threat_actor_ids=campaign.threat_actor_ids,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        target_sectors=campaign.target_sectors,
        target_regions=campaign.target_regions,
        is_active=campaign.is_active,
        ioc_count=campaign.ioc_count,
        cve_count=campaign.cve_count,
    )


@router.get("/campaigns/search", response_model=CampaignSearchResponse)
async def search_campaigns(
    query: Optional[str] = Query(None, description="Semantic search query"),
    threat_actor_id: Optional[str] = Query(None, description="Filter by threat actor"),
    target_sector: Optional[str] = Query(None, description="Filter by target sector"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    include_system: bool = Query(True, description="Include SYSTEM campaigns"),
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Search campaigns with semantic search and filters."""
    try:
        request = CampaignSearchRequest(
            query=query,
            customer_id=context.customer_id,
            threat_actor_id=threat_actor_id,
            target_sector=target_sector,
            is_active=is_active,
            limit=limit,
            include_system=include_system,
        )
        results = service.search_campaigns(request)

        campaign_responses = [
            CampaignResponse(
                campaign_id=r.campaign.campaign_id,
                name=r.campaign.name,
                customer_id=r.campaign.customer_id,
                threat_actor_ids=r.campaign.threat_actor_ids,
                start_date=r.campaign.start_date,
                end_date=r.campaign.end_date,
                target_sectors=r.campaign.target_sectors,
                target_regions=r.campaign.target_regions,
                is_active=r.campaign.is_active,
                ioc_count=r.campaign.ioc_count,
                cve_count=r.campaign.cve_count,
            )
            for r in results
        ]

        return CampaignSearchResponse(
            total_results=len(campaign_responses),
            customer_id=context.customer_id,
            results=campaign_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/campaigns/active", response_model=CampaignSearchResponse)
async def get_active_campaigns(
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get all currently active campaigns."""
    results = service.get_active_campaigns()

    campaign_responses = [
        CampaignResponse(
            campaign_id=r.campaign.campaign_id,
            name=r.campaign.name,
            customer_id=r.campaign.customer_id,
            threat_actor_ids=r.campaign.threat_actor_ids,
            start_date=r.campaign.start_date,
            end_date=r.campaign.end_date,
            target_sectors=r.campaign.target_sectors,
            target_regions=r.campaign.target_regions,
            is_active=r.campaign.is_active,
            ioc_count=r.campaign.ioc_count,
            cve_count=r.campaign.cve_count,
        )
        for r in results
    ]

    return CampaignSearchResponse(
        total_results=len(campaign_responses),
        customer_id=context.customer_id,
        results=campaign_responses,
    )


@router.get("/campaigns/{campaign_id}/iocs")
async def get_campaign_iocs(
    campaign_id: str,
    limit: int = Query(100, ge=1, le=500, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get IOCs associated with a campaign."""
    iocs = service.get_campaign_iocs(campaign_id, limit)

    return {
        "campaign_id": campaign_id,
        "customer_id": context.customer_id,
        "total_iocs": len(iocs),
        "iocs": iocs,
    }


# =============================================================================
# MITRE ATT&CK Endpoints
# =============================================================================


@router.post("/mitre/mappings", response_model=MITREMappingResponse, status_code=201)
async def create_mitre_mapping(
    mapping_data: MITREMappingCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """
    Create a new MITRE ATT&CK mapping.

    Requires WRITE access level.
    """
    try:
        from .threat_models import MITREMapping

        mapping = MITREMapping(
            mapping_id=mapping_data.mapping_id,
            customer_id=context.customer_id,
            technique_id=mapping_data.technique_id,
            technique_name=mapping_data.technique_name,
            tactic=mapping_data.tactic,
            entity_type=mapping_data.entity_type,
            entity_id=mapping_data.entity_id,
            description=mapping_data.description,
        )
        created = service.create_mitre_mapping(mapping)

        return MITREMappingResponse(
            mapping_id=created.mapping_id,
            customer_id=created.customer_id,
            technique_id=created.technique_id,
            technique_name=created.technique_name,
            tactic=created.tactic,
            entity_type=created.entity_type,
            entity_id=created.entity_id,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/mitre/mappings/entity/{entity_type}/{entity_id}", response_model=MITREMappingSearchResponse)
async def get_entity_mitre_mappings(
    entity_type: str,
    entity_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get MITRE ATT&CK mappings for an entity."""
    mappings = service.get_entity_mitre_mappings(entity_type, entity_id)

    mapping_responses = [
        MITREMappingResponse(
            mapping_id=m.mapping_id,
            customer_id=m.customer_id,
            technique_id=m.technique_id,
            technique_name=m.technique_name,
            tactic=m.tactic,
            entity_type=m.entity_type,
            entity_id=m.entity_id,
        )
        for m in mappings
    ]

    return MITREMappingSearchResponse(
        total_results=len(mapping_responses),
        customer_id=context.customer_id,
        results=mapping_responses,
    )


@router.get("/mitre/techniques/{technique_id}/actors")
async def get_actors_using_technique(
    technique_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get threat actors using a specific MITRE ATT&CK technique."""
    actors = service.get_actors_using_technique(technique_id)

    return {
        "technique_id": technique_id,
        "customer_id": context.customer_id,
        "total_actors": len(actors),
        "actors": actors,
    }


@router.get("/mitre/coverage", response_model=MITRECoverageResponse)
async def get_mitre_coverage(
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get MITRE ATT&CK coverage summary."""
    coverage = service.get_mitre_coverage()

    return MITRECoverageResponse(
        customer_id=context.customer_id,
        total_techniques=coverage.get("total_techniques", 0),
        covered_techniques=coverage.get("covered_techniques", 0),
        coverage_percentage=coverage.get("coverage_percentage", 0.0),
        tactics_coverage=coverage.get("tactics_coverage", {}),
        top_techniques=coverage.get("top_techniques", []),
    )


@router.get("/mitre/gaps", response_model=MITREGapsResponse)
async def get_mitre_gaps(
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get MITRE ATT&CK coverage gaps."""
    gaps = service.get_mitre_gaps()

    return MITREGapsResponse(
        customer_id=context.customer_id,
        uncovered_techniques=gaps.get("uncovered_techniques", 0),
        critical_gaps=gaps.get("critical_gaps", []),
        recommendations=gaps.get("recommendations", []),
    )


# =============================================================================
# IOC Endpoints
# =============================================================================


@router.post("/iocs", response_model=IOCResponse, status_code=201)
async def create_ioc(
    ioc_data: IOCCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """
    Create a new IOC.

    Requires WRITE access level.
    """
    try:
        from .threat_models import IOC, IOCType

        ioc = IOC(
            ioc_id=ioc_data.ioc_id,
            customer_id=context.customer_id,
            ioc_type=IOCType(ioc_data.ioc_type),
            value=ioc_data.value,
            threat_actor_id=ioc_data.threat_actor_id,
            campaign_id=ioc_data.campaign_id,
            first_seen=ioc_data.first_seen,
            last_seen=ioc_data.last_seen,
            confidence=ioc_data.confidence,
            description=ioc_data.description,
            tags=ioc_data.tags,
        )
        created = service.create_ioc(ioc)

        return IOCResponse(
            ioc_id=created.ioc_id,
            customer_id=created.customer_id,
            ioc_type=created.ioc_type.value,
            value=created.value,
            threat_actor_id=created.threat_actor_id,
            campaign_id=created.campaign_id,
            first_seen=created.first_seen,
            last_seen=created.last_seen,
            confidence=created.confidence,
            is_active=created.is_active,
            tags=created.tags,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/iocs/bulk", response_model=IOCBulkImportResponse)
async def bulk_import_iocs(
    bulk_data: IOCBulkImport,
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """
    Bulk import IOCs.

    Requires WRITE access level.
    """
    try:
        result = service.bulk_import_iocs(bulk_data.iocs)

        return IOCBulkImportResponse(
            imported_count=result.get("imported_count", 0),
            failed_count=result.get("failed_count", 0),
            failed_iocs=result.get("failed_iocs", []),
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/iocs/search", response_model=IOCSearchResponse)
async def search_iocs(
    query: Optional[str] = Query(None, description="Semantic search query"),
    ioc_type: Optional[str] = Query(None, description="Filter by IOC type"),
    threat_actor_id: Optional[str] = Query(None, description="Filter by threat actor"),
    campaign_id: Optional[str] = Query(None, description="Filter by campaign"),
    min_confidence: Optional[int] = Query(None, ge=0, le=100, description="Minimum confidence"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    limit: int = Query(50, ge=1, le=500, description="Maximum results"),
    include_system: bool = Query(True, description="Include SYSTEM IOCs"),
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Search IOCs with semantic search and filters."""
    try:
        request = IOCSearchRequest(
            query=query,
            customer_id=context.customer_id,
            ioc_type=ioc_type,
            threat_actor_id=threat_actor_id,
            campaign_id=campaign_id,
            min_confidence=min_confidence,
            is_active=is_active,
            limit=limit,
            include_system=include_system,
        )
        results = service.search_iocs(request)

        ioc_responses = [
            IOCResponse(
                ioc_id=r.ioc.ioc_id,
                customer_id=r.ioc.customer_id,
                ioc_type=r.ioc.ioc_type.value if hasattr(r.ioc.ioc_type, 'value') else r.ioc.ioc_type,
                value=r.ioc.value,
                threat_actor_id=r.ioc.threat_actor_id,
                campaign_id=r.ioc.campaign_id,
                first_seen=r.ioc.first_seen,
                last_seen=r.ioc.last_seen,
                confidence=r.ioc.confidence,
                is_active=r.ioc.is_active,
                tags=r.ioc.tags,
            )
            for r in results
        ]

        return IOCSearchResponse(
            total_results=len(ioc_responses),
            customer_id=context.customer_id,
            results=ioc_responses,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/iocs/active", response_model=IOCSearchResponse)
async def get_active_iocs(
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get all currently active IOCs."""
    results = service.get_active_iocs()

    ioc_responses = [
        IOCResponse(
            ioc_id=r.ioc.ioc_id,
            customer_id=r.ioc.customer_id,
            ioc_type=r.ioc.ioc_type.value if hasattr(r.ioc.ioc_type, 'value') else r.ioc.ioc_type,
            value=r.ioc.value,
            threat_actor_id=r.ioc.threat_actor_id,
            campaign_id=r.ioc.campaign_id,
            first_seen=r.ioc.first_seen,
            last_seen=r.ioc.last_seen,
            confidence=r.ioc.confidence,
            is_active=r.ioc.is_active,
            tags=r.ioc.tags,
        )
        for r in results
    ]

    return IOCSearchResponse(
        total_results=len(ioc_responses),
        customer_id=context.customer_id,
        results=ioc_responses,
    )


@router.get("/iocs/by-type/{ioc_type}", response_model=IOCSearchResponse)
async def get_iocs_by_type(
    ioc_type: str,
    limit: int = Query(100, ge=1, le=500, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get IOCs by type."""
    results = service.get_iocs_by_type(ioc_type, limit)

    ioc_responses = [
        IOCResponse(
            ioc_id=r.ioc.ioc_id,
            customer_id=r.ioc.customer_id,
            ioc_type=r.ioc.ioc_type.value if hasattr(r.ioc.ioc_type, 'value') else r.ioc.ioc_type,
            value=r.ioc.value,
            threat_actor_id=r.ioc.threat_actor_id,
            campaign_id=r.ioc.campaign_id,
            first_seen=r.ioc.first_seen,
            last_seen=r.ioc.last_seen,
            confidence=r.ioc.confidence,
            is_active=r.ioc.is_active,
            tags=r.ioc.tags,
        )
        for r in results
    ]

    return IOCSearchResponse(
        total_results=len(ioc_responses),
        customer_id=context.customer_id,
        results=ioc_responses,
    )


# =============================================================================
# Threat Feed Endpoints
# =============================================================================


@router.post("/feeds", response_model=ThreatFeedResponse, status_code=201)
async def create_threat_feed(
    feed_data: ThreatFeedCreate,
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """
    Create a new threat feed.

    Requires WRITE access level.
    """
    try:
        from .threat_models import ThreatFeed, FeedType

        feed = ThreatFeed(
            feed_id=feed_data.feed_id,
            name=feed_data.name,
            customer_id=context.customer_id,
            feed_url=feed_data.feed_url,
            feed_type=FeedType(feed_data.feed_type),
            refresh_interval=feed_data.refresh_interval,
            enabled=feed_data.enabled,
        )
        created = service.create_threat_feed(feed)

        return ThreatFeedResponse(
            feed_id=created.feed_id,
            name=created.name,
            customer_id=created.customer_id,
            feed_url=created.feed_url,
            feed_type=created.feed_type.value,
            refresh_interval=created.refresh_interval,
            enabled=created.enabled,
            last_refresh=created.last_refresh,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/feeds", response_model=ThreatFeedListResponse)
async def list_threat_feeds(
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """List threat feeds."""
    feeds = service.list_threat_feeds(limit)

    feed_responses = [
        ThreatFeedResponse(
            feed_id=f.feed_id,
            name=f.name,
            customer_id=f.customer_id,
            feed_url=f.feed_url,
            feed_type=f.feed_type.value if hasattr(f.feed_type, 'value') else f.feed_type,
            refresh_interval=f.refresh_interval,
            enabled=f.enabled,
            last_refresh=f.last_refresh,
        )
        for f in feeds
    ]

    return ThreatFeedListResponse(
        total_results=len(feed_responses),
        customer_id=context.customer_id,
        feeds=feed_responses,
    )


@router.put("/feeds/{feed_id}/refresh")
async def trigger_feed_refresh(
    feed_id: str,
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """
    Trigger threat feed refresh.

    Requires WRITE access level.
    """
    try:
        success = service.refresh_threat_feed(feed_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Threat feed {feed_id} not found")

        return {"feed_id": feed_id, "message": "Feed refresh triggered successfully"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# =============================================================================
# Dashboard Endpoint
# =============================================================================


@router.get("/dashboard/summary", response_model=ThreatIntelSummaryResponse)
async def get_threat_intel_summary(
    context: CustomerContext = Depends(require_customer_context),
    service: ThreatIntelligenceService = Depends(get_service),
):
    """Get threat intelligence dashboard summary."""
    summary = service.get_dashboard_summary()

    return ThreatIntelSummaryResponse(
        customer_id=context.customer_id,
        total_threat_actors=summary.get("total_threat_actors", 0),
        active_campaigns=summary.get("active_campaigns", 0),
        total_iocs=summary.get("total_iocs", 0),
        active_iocs=summary.get("active_iocs", 0),
        total_cves=summary.get("total_cves", 0),
        mitre_coverage=summary.get("mitre_coverage", 0.0),
        high_confidence_iocs=summary.get("high_confidence_iocs", 0),
        recent_activity_count=summary.get("recent_activity_count", 0),
    )
