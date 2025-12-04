"""
Threat Intelligence Models
===========================

Data models for E04: Threat Intelligence Correlation API.
Includes ThreatActor, ThreatCampaign, MITREMapping, ThreatIntelFeed, and IOC entities.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional, List, Dict, Any


# =============================================================================
# Enums for Threat Intelligence
# =============================================================================


class ActorType(Enum):
    """Threat actor classification types."""
    APT = "apt"                           # Advanced Persistent Threat
    CRIMINAL = "criminal"                 # Cybercriminal group
    HACKTIVIST = "hacktivist"             # Ideologically motivated
    STATE_SPONSORED = "state_sponsored"   # Nation-state actor
    INSIDER = "insider"                   # Insider threat
    UNKNOWN = "unknown"                   # Unattributed


class ActorMotivation(Enum):
    """Primary motivations for threat actors."""
    ESPIONAGE = "espionage"               # Intelligence gathering
    FINANCIAL = "financial"               # Financial gain
    DISRUPTION = "disruption"             # Service disruption
    DESTRUCTION = "destruction"           # Data/system destruction
    IDEOLOGICAL = "ideological"           # Political/ideological goals


class CampaignStatus(Enum):
    """Status of threat campaigns."""
    ACTIVE = "active"         # Currently ongoing
    CONCLUDED = "concluded"   # Completed campaign
    SUSPECTED = "suspected"   # Suspected but not confirmed


class IOCType(Enum):
    """Types of Indicators of Compromise."""
    IP = "ip"                   # IP address
    DOMAIN = "domain"           # Domain name
    URL = "url"                 # Full URL
    HASH_MD5 = "hash_md5"       # MD5 file hash
    HASH_SHA1 = "hash_sha1"     # SHA1 file hash
    HASH_SHA256 = "hash_sha256" # SHA256 file hash
    EMAIL = "email"             # Email address
    FILE_NAME = "file_name"     # File name pattern


class MitigationStatus(Enum):
    """Status of MITRE ATT&CK technique mitigation."""
    NOT_COVERED = "not_covered"         # No detection/mitigation
    PARTIAL = "partial"                 # Partial coverage
    COVERED = "covered"                 # Fully covered
    MONITORING_ONLY = "monitoring_only" # Detection only, no prevention


class FeedType(Enum):
    """Types of threat intelligence feeds."""
    COMMERCIAL = "commercial"   # Commercial threat feed
    OPEN_SOURCE = "open_source" # Public/open source feed
    GOVERNMENT = "government"   # Government-provided feed
    COMMUNITY = "community"     # Community-sourced feed
    INTERNAL = "internal"       # Internal threat intel


# =============================================================================
# Core Data Models
# =============================================================================


@dataclass
class ThreatActor:
    """
    Threat Actor entity for APT group tracking.

    Represents a threat actor (APT, criminal group, etc.) with their
    tactics, techniques, and targeting information.
    """
    threat_actor_id: str
    customer_id: str  # For multi-tenant isolation
    name: str

    # Actor classification
    aliases: List[str] = field(default_factory=list)
    actor_type: ActorType = ActorType.UNKNOWN
    motivation: ActorMotivation = ActorMotivation.UNKNOWN

    # Attribution
    origin_country: Optional[str] = None
    target_sectors: List[str] = field(default_factory=list)  # ['energy', 'healthcare', 'finance']
    target_regions: List[str] = field(default_factory=list)  # ['North America', 'Europe', 'Asia']

    # Activity timeline
    active_since: Optional[date] = None
    last_seen: Optional[date] = None
    confidence_level: float = 0.0  # 0.0-1.0 confidence in attribution

    # TTPs (Tactics, Techniques, Procedures)
    ttps: List[str] = field(default_factory=list)  # MITRE ATT&CK IDs: ['T1566', 'T1059']
    malware_used: List[str] = field(default_factory=list)  # ['Cobalt Strike', 'Mimikatz']

    # Campaign linkage
    associated_campaigns: List[str] = field(default_factory=list)  # Campaign IDs
    associated_cves: List[str] = field(default_factory=list)  # CVEs exploited by this actor

    # Metadata
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate threat actor data on creation."""
        if not self.threat_actor_id or not self.threat_actor_id.strip():
            raise ValueError("threat_actor_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")
        if not 0.0 <= self.confidence_level <= 1.0:
            raise ValueError("confidence_level must be between 0.0 and 1.0")

        # Normalize values
        self.threat_actor_id = self.threat_actor_id.strip()
        self.customer_id = self.customer_id.strip()
        self.name = self.name.strip()

    @property
    def is_active(self) -> bool:
        """Check if actor has recent activity (within 365 days)."""
        if not self.last_seen:
            return False
        days_since_activity = (date.today() - self.last_seen).days
        return days_since_activity <= 365

    @property
    def threat_score(self) -> float:
        """Calculate threat score based on activity and sophistication (0.0-10.0)."""
        score = 0.0

        # Activity factor (0-3 points)
        if self.is_active:
            score += 3.0
        elif self.last_seen:
            days_since = (date.today() - self.last_seen).days
            if days_since <= 730:  # Within 2 years
                score += 1.5

        # Attribution confidence (0-2 points)
        score += self.confidence_level * 2.0

        # Sophistication indicators (0-5 points)
        if self.actor_type in {ActorType.APT, ActorType.STATE_SPONSORED}:
            score += 2.0
        if len(self.ttps) > 10:
            score += 1.5
        if len(self.malware_used) > 5:
            score += 1.0
        if len(self.associated_cves) > 10:
            score += 0.5

        return min(score, 10.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "threat_actor_id": self.threat_actor_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "aliases": self.aliases,
            "actor_type": self.actor_type.value,
            "motivation": self.motivation.value,
            "origin_country": self.origin_country,
            "target_sectors": self.target_sectors,
            "target_regions": self.target_regions,
            "active_since": self.active_since.isoformat() if self.active_since else None,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "confidence_level": self.confidence_level,
            "ttps": self.ttps,
            "malware_used": self.malware_used,
            "associated_campaigns": self.associated_campaigns,
            "associated_cves": self.associated_cves,
            "description": self.description,
            "is_active": self.is_active,
            "threat_score": self.threat_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "threat_actor_id": self.threat_actor_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "entity_type": "threat_actor",
            "aliases": self.aliases,
            "actor_type": self.actor_type.value,
            "motivation": self.motivation.value,
            "origin_country": self.origin_country,
            "target_sectors": self.target_sectors,
            "target_regions": self.target_regions,
            "confidence_level": self.confidence_level,
            "ttps": self.ttps,
            "malware_used": self.malware_used,
            "is_active": self.is_active,
            "threat_score": self.threat_score,
            "ttp_count": len(self.ttps),
            "malware_count": len(self.malware_used),
            "campaign_count": len(self.associated_campaigns),
            "cve_count": len(self.associated_cves),
        }


@dataclass
class ThreatCampaign:
    """
    Threat Campaign entity for campaign tracking.

    Represents a coordinated series of attacks with shared objectives,
    infrastructure, and/or attribution.
    """
    campaign_id: str
    customer_id: str  # For multi-tenant isolation
    name: str

    # Campaign details
    description: Optional[str] = None
    threat_actor_id: Optional[str] = None  # Link to ThreatActor

    # Timeline
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: CampaignStatus = CampaignStatus.SUSPECTED

    # Targeting
    target_sectors: List[str] = field(default_factory=list)  # ['energy', 'finance']
    target_regions: List[str] = field(default_factory=list)  # ['US', 'EU']
    target_organizations: List[str] = field(default_factory=list)  # Specific orgs targeted

    # Attack details
    attack_vectors: List[str] = field(default_factory=list)  # ['phishing', 'exploit']
    objectives: List[str] = field(default_factory=list)  # ['data_theft', 'ransomware']

    # Technical indicators
    associated_cves: List[str] = field(default_factory=list)  # CVEs used in campaign
    iocs: List[Dict[str, Any]] = field(default_factory=list)  # IOC dicts with type/value

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate campaign data on creation."""
        if not self.campaign_id or not self.campaign_id.strip():
            raise ValueError("campaign_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")

        # Normalize values
        self.campaign_id = self.campaign_id.strip()
        self.customer_id = self.customer_id.strip()
        self.name = self.name.strip()

    @property
    def is_active(self) -> bool:
        """Check if campaign is currently active."""
        return self.status == CampaignStatus.ACTIVE

    @property
    def duration_days(self) -> Optional[int]:
        """Calculate campaign duration in days."""
        if not self.start_date:
            return None
        end = self.end_date if self.end_date else date.today()
        return (end - self.start_date).days

    @property
    def campaign_scope_score(self) -> float:
        """Calculate campaign scope/severity score (0.0-10.0)."""
        score = 0.0

        # Status factor (0-2 points)
        if self.status == CampaignStatus.ACTIVE:
            score += 2.0
        elif self.status == CampaignStatus.CONCLUDED:
            score += 1.0

        # Scale factors (0-4 points)
        score += min(len(self.target_sectors) * 0.5, 2.0)
        score += min(len(self.target_organizations) * 0.2, 2.0)

        # Technical sophistication (0-4 points)
        score += min(len(self.associated_cves) * 0.2, 2.0)
        score += min(len(self.iocs) * 0.01, 2.0)

        return min(score, 10.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "campaign_id": self.campaign_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "description": self.description,
            "threat_actor_id": self.threat_actor_id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status.value,
            "target_sectors": self.target_sectors,
            "target_regions": self.target_regions,
            "target_organizations": self.target_organizations,
            "attack_vectors": self.attack_vectors,
            "objectives": self.objectives,
            "associated_cves": self.associated_cves,
            "iocs": self.iocs,
            "is_active": self.is_active,
            "duration_days": self.duration_days,
            "campaign_scope_score": self.campaign_scope_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "campaign_id": self.campaign_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "entity_type": "threat_campaign",
            "threat_actor_id": self.threat_actor_id,
            "status": self.status.value,
            "target_sectors": self.target_sectors,
            "target_regions": self.target_regions,
            "attack_vectors": self.attack_vectors,
            "objectives": self.objectives,
            "is_active": self.is_active,
            "campaign_scope_score": self.campaign_scope_score,
            "cve_count": len(self.associated_cves),
            "ioc_count": len(self.iocs),
        }


@dataclass
class MITREMapping:
    """
    MITRE ATT&CK Mapping entity.

    Maps security events, vulnerabilities, or campaigns to MITRE ATT&CK
    framework techniques and tactics.
    """
    mapping_id: str
    customer_id: str  # For multi-tenant isolation

    # Entity linkage
    entity_type: str  # 'vulnerability', 'campaign', 'threat_actor', 'alert'
    entity_id: str    # ID of the linked entity

    # MITRE ATT&CK information
    technique_id: str  # T1566 (Phishing)
    tactic: List[str] = field(default_factory=list)  # ['initial-access', 'defense-evasion']
    technique_name: str = ""

    # Sub-technique (optional)
    sub_technique_id: Optional[str] = None  # T1566.001 (Spearphishing Attachment)
    sub_technique_name: Optional[str] = None

    # Detection and mitigation
    detection_coverage: float = 0.0  # 0.0-1.0 coverage level
    mitigation_status: MitigationStatus = MitigationStatus.NOT_COVERED

    # Evidence and confidence
    evidence: List[str] = field(default_factory=list)  # Evidence for this mapping
    confidence_score: float = 0.0  # 0.0-1.0 confidence in mapping

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate MITRE mapping data on creation."""
        if not self.mapping_id or not self.mapping_id.strip():
            raise ValueError("mapping_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.entity_type or not self.entity_type.strip():
            raise ValueError("entity_type is required")
        if not self.entity_id or not self.entity_id.strip():
            raise ValueError("entity_id is required")
        if not self.technique_id or not self.technique_id.strip():
            raise ValueError("technique_id is required")
        if not 0.0 <= self.detection_coverage <= 1.0:
            raise ValueError("detection_coverage must be between 0.0 and 1.0")
        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValueError("confidence_score must be between 0.0 and 1.0")

        # Normalize values
        self.mapping_id = self.mapping_id.strip()
        self.customer_id = self.customer_id.strip()
        self.entity_type = self.entity_type.strip()
        self.entity_id = self.entity_id.strip()
        self.technique_id = self.technique_id.strip().upper()

    @property
    def is_covered(self) -> bool:
        """Check if technique has detection/mitigation coverage."""
        return self.mitigation_status in {MitigationStatus.COVERED, MitigationStatus.PARTIAL}

    @property
    def coverage_gap_score(self) -> float:
        """Calculate coverage gap severity (0.0-10.0)."""
        # Base severity on lack of coverage
        gap_score = (1.0 - self.detection_coverage) * 5.0

        # Increase score if no mitigation
        if self.mitigation_status == MitigationStatus.NOT_COVERED:
            gap_score += 3.0
        elif self.mitigation_status == MitigationStatus.MONITORING_ONLY:
            gap_score += 1.5

        # Reduce score based on confidence (if mapping is uncertain, gap is less severe)
        gap_score *= self.confidence_score

        return min(gap_score, 10.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "mapping_id": self.mapping_id,
            "customer_id": self.customer_id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "technique_id": self.technique_id,
            "tactic": self.tactic,
            "technique_name": self.technique_name,
            "sub_technique_id": self.sub_technique_id,
            "sub_technique_name": self.sub_technique_name,
            "detection_coverage": self.detection_coverage,
            "mitigation_status": self.mitigation_status.value,
            "evidence": self.evidence,
            "confidence_score": self.confidence_score,
            "is_covered": self.is_covered,
            "coverage_gap_score": self.coverage_gap_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "mapping_id": self.mapping_id,
            "customer_id": self.customer_id,
            "entity_type": "mitre_mapping",
            "linked_entity_type": self.entity_type,
            "linked_entity_id": self.entity_id,
            "technique_id": self.technique_id,
            "tactic": self.tactic,
            "technique_name": self.technique_name,
            "sub_technique_id": self.sub_technique_id,
            "detection_coverage": self.detection_coverage,
            "mitigation_status": self.mitigation_status.value,
            "confidence_score": self.confidence_score,
            "is_covered": self.is_covered,
            "coverage_gap_score": self.coverage_gap_score,
        }


@dataclass
class ThreatIntelFeed:
    """
    Threat Intelligence Feed entity.

    Represents an external threat intelligence feed source with
    configuration and status tracking.
    """
    feed_id: str
    customer_id: str  # For multi-tenant isolation
    name: str

    # Feed configuration
    feed_type: FeedType = FeedType.OPEN_SOURCE
    source_url: Optional[str] = None
    api_key_required: bool = False
    refresh_interval_minutes: int = 60  # How often to refresh

    # Feed status
    last_updated: Optional[datetime] = None
    ioc_count: int = 0  # Total IOCs from this feed
    enabled: bool = True

    # Metadata
    description: Optional[str] = None
    provider: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate feed data on creation."""
        if not self.feed_id or not self.feed_id.strip():
            raise ValueError("feed_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")

        # Normalize values
        self.feed_id = self.feed_id.strip()
        self.customer_id = self.customer_id.strip()
        self.name = self.name.strip()

    @property
    def is_stale(self) -> bool:
        """Check if feed data is stale (not updated within 2x refresh interval)."""
        if not self.last_updated:
            return True
        from datetime import timedelta
        stale_threshold = timedelta(minutes=self.refresh_interval_minutes * 2)
        return datetime.utcnow() - self.last_updated > stale_threshold

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "feed_id": self.feed_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "feed_type": self.feed_type.value,
            "source_url": self.source_url,
            "api_key_required": self.api_key_required,
            "refresh_interval_minutes": self.refresh_interval_minutes,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "ioc_count": self.ioc_count,
            "enabled": self.enabled,
            "is_stale": self.is_stale,
            "description": self.description,
            "provider": self.provider,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class IOC:
    """
    Indicator of Compromise (IOC) entity.

    Represents a single IOC (IP, domain, hash, etc.) with tracking
    and confidence scoring.
    """
    ioc_id: str
    customer_id: str  # For multi-tenant isolation

    # IOC details
    ioc_type: IOCType
    value: str  # The actual IOC value (IP, hash, domain, etc.)

    # Timeline
    first_seen: datetime = field(default_factory=datetime.utcnow)
    last_seen: datetime = field(default_factory=datetime.utcnow)

    # Confidence and validity
    confidence: float = 0.5  # 0.0-1.0 confidence this is a real threat
    is_active: bool = True

    # Attribution
    associated_campaigns: List[str] = field(default_factory=list)  # Campaign IDs
    associated_actors: List[str] = field(default_factory=list)  # Threat actor IDs

    # Source tracking
    source: Optional[str] = None  # Feed ID or source name

    # Metadata
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate IOC data on creation."""
        if not self.ioc_id or not self.ioc_id.strip():
            raise ValueError("ioc_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.value or not self.value.strip():
            raise ValueError("value is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")

        # Normalize values
        self.ioc_id = self.ioc_id.strip()
        self.customer_id = self.customer_id.strip()
        self.value = self.value.strip()

    @property
    def age_days(self) -> int:
        """Calculate age of IOC in days since first seen."""
        return (datetime.utcnow() - self.first_seen).days

    @property
    def is_recent(self) -> bool:
        """Check if IOC has been seen recently (within 30 days)."""
        days_since_last_seen = (datetime.utcnow() - self.last_seen).days
        return days_since_last_seen <= 30

    @property
    def threat_score(self) -> float:
        """Calculate threat score based on confidence, recency, and attribution (0.0-10.0)."""
        score = 0.0

        # Confidence factor (0-4 points)
        score += self.confidence * 4.0

        # Recency factor (0-3 points)
        if self.is_recent:
            score += 3.0
        elif self.age_days <= 90:
            score += 1.5

        # Attribution factor (0-3 points)
        if len(self.associated_actors) > 0:
            score += 2.0
        if len(self.associated_campaigns) > 0:
            score += 1.0

        return min(score, 10.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "ioc_id": self.ioc_id,
            "customer_id": self.customer_id,
            "ioc_type": self.ioc_type.value,
            "value": self.value,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "confidence": self.confidence,
            "is_active": self.is_active,
            "associated_campaigns": self.associated_campaigns,
            "associated_actors": self.associated_actors,
            "source": self.source,
            "description": self.description,
            "age_days": self.age_days,
            "is_recent": self.is_recent,
            "threat_score": self.threat_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "ioc_id": self.ioc_id,
            "customer_id": self.customer_id,
            "entity_type": "ioc",
            "ioc_type": self.ioc_type.value,
            "value": self.value,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "confidence": self.confidence,
            "is_active": self.is_active,
            "associated_campaigns": self.associated_campaigns,
            "associated_actors": self.associated_actors,
            "source": self.source,
            "is_recent": self.is_recent,
            "threat_score": self.threat_score,
            "age_days": self.age_days,
        }
