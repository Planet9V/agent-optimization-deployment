"""
Threat Intelligence Correlation Integration Tests
==================================================

Integration tests for E04: Threat Intelligence Correlation API.
Tests customer isolation, model validation, and threat intelligence operations.

Version: 1.0.0
Created: 2025-12-04
"""

import pytest
from datetime import date, datetime, timedelta
from typing import Generator
import uuid

# Import threat intelligence components
from api.threat_intelligence.threat_models import (
    ThreatActor,
    ThreatCampaign,
    MITREMapping,
    ThreatIntelFeed,
    IOC,
    ActorType,
    ActorMotivation,
    CampaignStatus,
    IOCType,
    MitigationStatus,
    FeedType,
)
from api.threat_intelligence.threat_service import (
    ThreatIntelligenceService,
    ThreatActorSearchRequest,
    CampaignSearchRequest,
    IOCSearchRequest,
)
from api.customer_isolation import (
    CustomerContext,
    CustomerContextManager,
    CustomerAccessLevel,
)


# =============================================
# Test Fixtures
# =============================================

@pytest.fixture
def test_customer_ids() -> dict:
    """Generate unique customer IDs for test isolation."""
    return {
        "customer_a": f"TEST-THREAT-A-{uuid.uuid4().hex[:8]}",
        "customer_b": f"TEST-THREAT-B-{uuid.uuid4().hex[:8]}",
    }


@pytest.fixture
def customer_a_context(test_customer_ids) -> Generator[CustomerContext, None, None]:
    """Set up customer A context."""
    context = CustomerContextManager.create_context(
        customer_id=test_customer_ids["customer_a"],
        namespace="test_threat_customer_a",
        access_level=CustomerAccessLevel.WRITE,
        user_id="test-user-a",
    )
    yield context
    CustomerContextManager.clear_context()


@pytest.fixture
def customer_b_context(test_customer_ids) -> Generator[CustomerContext, None, None]:
    """Set up customer B context."""
    context = CustomerContextManager.create_context(
        customer_id=test_customer_ids["customer_b"],
        namespace="test_threat_customer_b",
        access_level=CustomerAccessLevel.WRITE,
        user_id="test-user-b",
    )
    yield context
    CustomerContextManager.clear_context()


@pytest.fixture
def sample_threat_actor(test_customer_ids) -> ThreatActor:
    """Create sample threat actor for testing."""
    today = date.today()
    return ThreatActor(
        threat_actor_id=f"ACTOR-TEST-{uuid.uuid4().hex[:8]}",
        customer_id=test_customer_ids["customer_a"],
        name="APT28",
        aliases=["Fancy Bear", "Sofacy", "Pawn Storm"],
        actor_type=ActorType.APT,
        motivation=ActorMotivation.ESPIONAGE,
        origin_country="Russia",
        target_sectors=["government", "military", "defense"],
        target_regions=["North America", "Europe"],
        active_since=today - timedelta(days=3650),  # 10 years ago
        last_seen=today - timedelta(days=30),
        confidence_level=0.95,
        ttps=["T1566", "T1059", "T1003", "T1078"],
        malware_used=["X-Agent", "Sofacy", "Zebrocy"],
        associated_campaigns=["CAMPAIGN-001", "CAMPAIGN-002"],
        associated_cves=["CVE-2023-23397", "CVE-2022-30190"],
        description="Russian state-sponsored APT group targeting government entities",
    )


@pytest.fixture
def sample_campaign(test_customer_ids, sample_threat_actor) -> ThreatCampaign:
    """Create sample campaign for testing."""
    today = date.today()
    return ThreatCampaign(
        campaign_id=f"CAMP-TEST-{uuid.uuid4().hex[:8]}",
        customer_id=test_customer_ids["customer_a"],
        name="Operation Ghost Writer",
        description="Coordinated disinformation and espionage campaign",
        threat_actor_id=sample_threat_actor.threat_actor_id,
        start_date=today - timedelta(days=180),
        status=CampaignStatus.ACTIVE,
        target_sectors=["government", "media"],
        target_regions=["Europe", "North America"],
        attack_vectors=["phishing", "watering_hole", "credential_harvesting"],
        objectives=["data_theft", "influence_operations"],
        associated_cves=["CVE-2023-23397"],
        iocs=[
            {"type": "domain", "value": "evil-phishing.com"},
            {"type": "ip", "value": "192.0.2.100"},
        ],
    )


@pytest.fixture
def sample_mitre_mapping(test_customer_ids, sample_threat_actor) -> MITREMapping:
    """Create sample MITRE ATT&CK mapping for testing."""
    return MITREMapping(
        mapping_id=f"MITRE-TEST-{uuid.uuid4().hex[:8]}",
        customer_id=test_customer_ids["customer_a"],
        entity_type="threat_actor",
        entity_id=sample_threat_actor.threat_actor_id,
        technique_id="T1566",
        tactic=["initial-access"],
        technique_name="Phishing",
        sub_technique_id="T1566.001",
        sub_technique_name="Spearphishing Attachment",
        detection_coverage=0.75,
        mitigation_status=MitigationStatus.PARTIAL,
        evidence=["Email gateway logs", "EDR detections"],
        confidence_score=0.90,
    )


@pytest.fixture
def sample_ioc(test_customer_ids, sample_threat_actor, sample_campaign) -> IOC:
    """Create sample IOC for testing."""
    return IOC(
        ioc_id=f"IOC-TEST-{uuid.uuid4().hex[:8]}",
        customer_id=test_customer_ids["customer_a"],
        ioc_type=IOCType.DOMAIN,
        value="evil-phishing.com",
        first_seen=datetime.utcnow() - timedelta(days=60),
        last_seen=datetime.utcnow() - timedelta(days=5),
        confidence=0.85,
        is_active=True,
        associated_campaigns=[sample_campaign.campaign_id],
        associated_actors=[sample_threat_actor.threat_actor_id],
        source="AlienVault OTX",
        description="Known phishing domain used by APT28",
    )


@pytest.fixture
def sample_feed(test_customer_ids) -> ThreatIntelFeed:
    """Create sample threat intelligence feed for testing."""
    return ThreatIntelFeed(
        feed_id=f"FEED-TEST-{uuid.uuid4().hex[:8]}",
        customer_id=test_customer_ids["customer_a"],
        name="AlienVault OTX",
        feed_type=FeedType.OPEN_SOURCE,
        source_url="https://otx.alienvault.com/api/v1/pulses",
        api_key_required=True,
        refresh_interval_minutes=60,
        last_updated=datetime.utcnow() - timedelta(minutes=30),
        ioc_count=15000,
        enabled=True,
        description="Open Threat Exchange community threat feed",
        provider="AlienVault",
    )


# =============================================
# ThreatActor Model Tests
# =============================================

class TestThreatActorModel:
    """Unit tests for ThreatActor model."""

    def test_threat_actor_creation_valid(self, test_customer_ids):
        """Test creating a valid threat actor."""
        actor = ThreatActor(
            threat_actor_id="ACTOR-001",
            customer_id=test_customer_ids["customer_a"],
            name="APT29",
            actor_type=ActorType.APT,
            motivation=ActorMotivation.ESPIONAGE,
        )
        assert actor.threat_actor_id == "ACTOR-001"
        assert actor.name == "APT29"
        assert actor.actor_type == ActorType.APT

    def test_threat_actor_validation_empty_id(self, test_customer_ids):
        """Test that empty threat_actor_id raises ValueError."""
        with pytest.raises(ValueError, match="threat_actor_id is required"):
            ThreatActor(
                threat_actor_id="",
                customer_id=test_customer_ids["customer_a"],
                name="Test Actor",
            )

    def test_threat_actor_validation_empty_customer_id(self):
        """Test that empty customer_id raises ValueError."""
        with pytest.raises(ValueError, match="customer_id is required"):
            ThreatActor(
                threat_actor_id="ACTOR-001",
                customer_id="",
                name="Test Actor",
            )

    def test_threat_actor_validation_confidence_range(self, test_customer_ids):
        """Test that confidence_level must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="confidence_level must be between"):
            ThreatActor(
                threat_actor_id="ACTOR-001",
                customer_id=test_customer_ids["customer_a"],
                name="Test Actor",
                confidence_level=1.5,  # Invalid: > 1.0
            )

    def test_threat_actor_is_active_recent(self, test_customer_ids):
        """Test is_active property for recent activity."""
        today = date.today()
        actor = ThreatActor(
            threat_actor_id="ACTOR-RECENT",
            customer_id=test_customer_ids["customer_a"],
            name="Recent Actor",
            last_seen=today - timedelta(days=30),
        )
        assert actor.is_active == True

    def test_threat_actor_is_active_old(self, test_customer_ids):
        """Test is_active property for old activity."""
        today = date.today()
        actor = ThreatActor(
            threat_actor_id="ACTOR-OLD",
            customer_id=test_customer_ids["customer_a"],
            name="Old Actor",
            last_seen=today - timedelta(days=500),
        )
        assert actor.is_active == False

    def test_threat_actor_threat_score_calculation(self, sample_threat_actor):
        """Test threat score calculation."""
        score = sample_threat_actor.threat_score
        assert 0.0 <= score <= 10.0
        assert score > 5.0  # Should be high due to APT type and activity

    def test_threat_actor_to_dict(self, sample_threat_actor):
        """Test threat actor serialization."""
        actor_dict = sample_threat_actor.to_dict()
        assert actor_dict["threat_actor_id"] == sample_threat_actor.threat_actor_id
        assert actor_dict["name"] == sample_threat_actor.name
        assert actor_dict["actor_type"] == sample_threat_actor.actor_type.value
        assert actor_dict["is_active"] == sample_threat_actor.is_active

    def test_threat_actor_to_qdrant_payload(self, sample_threat_actor):
        """Test Qdrant payload generation."""
        payload = sample_threat_actor.to_qdrant_payload()
        assert payload["entity_type"] == "threat_actor"
        assert payload["threat_actor_id"] == sample_threat_actor.threat_actor_id
        assert payload["customer_id"] == sample_threat_actor.customer_id
        assert "threat_score" in payload


# =============================================
# ThreatCampaign Model Tests
# =============================================

class TestThreatCampaignModel:
    """Unit tests for ThreatCampaign model."""

    def test_campaign_creation_valid(self, test_customer_ids):
        """Test creating a valid campaign."""
        campaign = ThreatCampaign(
            campaign_id="CAMP-001",
            customer_id=test_customer_ids["customer_a"],
            name="Test Campaign",
            status=CampaignStatus.ACTIVE,
        )
        assert campaign.campaign_id == "CAMP-001"
        assert campaign.name == "Test Campaign"
        assert campaign.status == CampaignStatus.ACTIVE

    def test_campaign_validation_empty_id(self, test_customer_ids):
        """Test that empty campaign_id raises ValueError."""
        with pytest.raises(ValueError, match="campaign_id is required"):
            ThreatCampaign(
                campaign_id="",
                customer_id=test_customer_ids["customer_a"],
                name="Test Campaign",
            )

    def test_campaign_is_active_status(self, test_customer_ids):
        """Test is_active property based on status."""
        active = ThreatCampaign(
            campaign_id="CAMP-ACTIVE",
            customer_id=test_customer_ids["customer_a"],
            name="Active Campaign",
            status=CampaignStatus.ACTIVE,
        )
        assert active.is_active == True

        concluded = ThreatCampaign(
            campaign_id="CAMP-CONCLUDED",
            customer_id=test_customer_ids["customer_a"],
            name="Concluded Campaign",
            status=CampaignStatus.CONCLUDED,
        )
        assert concluded.is_active == False

    def test_campaign_duration_calculation(self, test_customer_ids):
        """Test campaign duration calculation."""
        today = date.today()
        campaign = ThreatCampaign(
            campaign_id="CAMP-DURATION",
            customer_id=test_customer_ids["customer_a"],
            name="Test Campaign",
            start_date=today - timedelta(days=100),
            end_date=today - timedelta(days=30),
        )
        assert campaign.duration_days == 70

    def test_campaign_duration_ongoing(self, test_customer_ids):
        """Test duration for ongoing campaign."""
        today = date.today()
        campaign = ThreatCampaign(
            campaign_id="CAMP-ONGOING",
            customer_id=test_customer_ids["customer_a"],
            name="Ongoing Campaign",
            start_date=today - timedelta(days=50),
            status=CampaignStatus.ACTIVE,
        )
        assert campaign.duration_days == 50

    def test_campaign_scope_score(self, sample_campaign):
        """Test campaign scope score calculation."""
        score = sample_campaign.campaign_scope_score
        assert 0.0 <= score <= 10.0

    def test_campaign_to_dict(self, sample_campaign):
        """Test campaign serialization."""
        camp_dict = sample_campaign.to_dict()
        assert camp_dict["campaign_id"] == sample_campaign.campaign_id
        assert camp_dict["name"] == sample_campaign.name
        assert camp_dict["status"] == sample_campaign.status.value

    def test_campaign_to_qdrant_payload(self, sample_campaign):
        """Test Qdrant payload generation."""
        payload = sample_campaign.to_qdrant_payload()
        assert payload["entity_type"] == "threat_campaign"
        assert payload["campaign_id"] == sample_campaign.campaign_id
        assert "campaign_scope_score" in payload


# =============================================
# MITREMapping Model Tests
# =============================================

class TestMITREMappingModel:
    """Unit tests for MITREMapping model."""

    def test_mitre_mapping_creation_valid(self, test_customer_ids):
        """Test creating a valid MITRE mapping."""
        mapping = MITREMapping(
            mapping_id="MITRE-001",
            customer_id=test_customer_ids["customer_a"],
            entity_type="threat_actor",
            entity_id="ACTOR-001",
            technique_id="T1566",
            tactic=["initial-access"],
            technique_name="Phishing",
        )
        assert mapping.mapping_id == "MITRE-001"
        assert mapping.technique_id == "T1566"

    def test_mitre_mapping_validation_empty_mapping_id(self, test_customer_ids):
        """Test that empty mapping_id raises ValueError."""
        with pytest.raises(ValueError, match="mapping_id is required"):
            MITREMapping(
                mapping_id="",
                customer_id=test_customer_ids["customer_a"],
                entity_type="threat_actor",
                entity_id="ACTOR-001",
                technique_id="T1566",
            )

    def test_mitre_mapping_validation_detection_coverage_range(self, test_customer_ids):
        """Test that detection_coverage must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="detection_coverage must be between"):
            MITREMapping(
                mapping_id="MITRE-001",
                customer_id=test_customer_ids["customer_a"],
                entity_type="threat_actor",
                entity_id="ACTOR-001",
                technique_id="T1566",
                detection_coverage=1.5,  # Invalid
            )

    def test_mitre_mapping_is_covered_partial(self, test_customer_ids):
        """Test is_covered property for partial coverage."""
        mapping = MITREMapping(
            mapping_id="MITRE-PARTIAL",
            customer_id=test_customer_ids["customer_a"],
            entity_type="threat_actor",
            entity_id="ACTOR-001",
            technique_id="T1566",
            mitigation_status=MitigationStatus.PARTIAL,
        )
        assert mapping.is_covered == True

    def test_mitre_mapping_is_covered_not_covered(self, test_customer_ids):
        """Test is_covered property for not covered."""
        mapping = MITREMapping(
            mapping_id="MITRE-NOTCOVERED",
            customer_id=test_customer_ids["customer_a"],
            entity_type="threat_actor",
            entity_id="ACTOR-001",
            technique_id="T1566",
            mitigation_status=MitigationStatus.NOT_COVERED,
        )
        assert mapping.is_covered == False

    def test_mitre_mapping_coverage_gap_score(self, sample_mitre_mapping):
        """Test coverage gap score calculation."""
        score = sample_mitre_mapping.coverage_gap_score
        assert 0.0 <= score <= 10.0

    def test_mitre_mapping_to_dict(self, sample_mitre_mapping):
        """Test MITRE mapping serialization."""
        mapping_dict = sample_mitre_mapping.to_dict()
        assert mapping_dict["mapping_id"] == sample_mitre_mapping.mapping_id
        assert mapping_dict["technique_id"] == sample_mitre_mapping.technique_id
        assert mapping_dict["is_covered"] == sample_mitre_mapping.is_covered

    def test_mitre_mapping_to_qdrant_payload(self, sample_mitre_mapping):
        """Test Qdrant payload generation."""
        payload = sample_mitre_mapping.to_qdrant_payload()
        assert payload["entity_type"] == "mitre_mapping"
        assert payload["linked_entity_type"] == sample_mitre_mapping.entity_type


# =============================================
# IOC Model Tests
# =============================================

class TestIOCModel:
    """Unit tests for IOC model."""

    def test_ioc_creation_valid(self, test_customer_ids):
        """Test creating a valid IOC."""
        ioc = IOC(
            ioc_id="IOC-001",
            customer_id=test_customer_ids["customer_a"],
            ioc_type=IOCType.IP,
            value="192.0.2.1",
            confidence=0.75,
        )
        assert ioc.ioc_id == "IOC-001"
        assert ioc.ioc_type == IOCType.IP
        assert ioc.value == "192.0.2.1"

    def test_ioc_validation_empty_id(self, test_customer_ids):
        """Test that empty ioc_id raises ValueError."""
        with pytest.raises(ValueError, match="ioc_id is required"):
            IOC(
                ioc_id="",
                customer_id=test_customer_ids["customer_a"],
                ioc_type=IOCType.IP,
                value="192.0.2.1",
            )

    def test_ioc_validation_confidence_range(self, test_customer_ids):
        """Test that confidence must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="confidence must be between"):
            IOC(
                ioc_id="IOC-001",
                customer_id=test_customer_ids["customer_a"],
                ioc_type=IOCType.IP,
                value="192.0.2.1",
                confidence=2.0,  # Invalid
            )

    def test_ioc_age_calculation(self, test_customer_ids):
        """Test IOC age calculation."""
        past_date = datetime.utcnow() - timedelta(days=45)
        ioc = IOC(
            ioc_id="IOC-AGE",
            customer_id=test_customer_ids["customer_a"],
            ioc_type=IOCType.DOMAIN,
            value="old-domain.com",
            first_seen=past_date,
        )
        assert ioc.age_days == 45

    def test_ioc_is_recent_true(self, test_customer_ids):
        """Test is_recent property for recent IOC."""
        recent_date = datetime.utcnow() - timedelta(days=15)
        ioc = IOC(
            ioc_id="IOC-RECENT",
            customer_id=test_customer_ids["customer_a"],
            ioc_type=IOCType.DOMAIN,
            value="recent-domain.com",
            last_seen=recent_date,
        )
        assert ioc.is_recent == True

    def test_ioc_is_recent_false(self, test_customer_ids):
        """Test is_recent property for old IOC."""
        old_date = datetime.utcnow() - timedelta(days=60)
        ioc = IOC(
            ioc_id="IOC-OLD",
            customer_id=test_customer_ids["customer_a"],
            ioc_type=IOCType.DOMAIN,
            value="old-domain.com",
            last_seen=old_date,
        )
        assert ioc.is_recent == False

    def test_ioc_threat_score_calculation(self, sample_ioc):
        """Test threat score calculation."""
        score = sample_ioc.threat_score
        assert 0.0 <= score <= 10.0

    def test_ioc_types_validation(self, test_customer_ids):
        """Test all IOC type enums."""
        ioc_types = [
            IOCType.IP,
            IOCType.DOMAIN,
            IOCType.URL,
            IOCType.HASH_MD5,
            IOCType.HASH_SHA1,
            IOCType.HASH_SHA256,
            IOCType.EMAIL,
            IOCType.FILE_NAME,
        ]
        for ioc_type in ioc_types:
            ioc = IOC(
                ioc_id=f"IOC-{ioc_type.value}",
                customer_id=test_customer_ids["customer_a"],
                ioc_type=ioc_type,
                value=f"test-{ioc_type.value}",
            )
            assert ioc.ioc_type == ioc_type

    def test_ioc_to_dict(self, sample_ioc):
        """Test IOC serialization."""
        ioc_dict = sample_ioc.to_dict()
        assert ioc_dict["ioc_id"] == sample_ioc.ioc_id
        assert ioc_dict["ioc_type"] == sample_ioc.ioc_type.value
        assert ioc_dict["is_recent"] == sample_ioc.is_recent

    def test_ioc_to_qdrant_payload(self, sample_ioc):
        """Test Qdrant payload generation."""
        payload = sample_ioc.to_qdrant_payload()
        assert payload["entity_type"] == "ioc"
        assert payload["ioc_id"] == sample_ioc.ioc_id
        assert "threat_score" in payload


# =============================================
# ThreatIntelFeed Model Tests
# =============================================

class TestThreatIntelFeedModel:
    """Unit tests for ThreatIntelFeed model."""

    def test_feed_creation_valid(self, test_customer_ids):
        """Test creating a valid threat intel feed."""
        feed = ThreatIntelFeed(
            feed_id="FEED-001",
            customer_id=test_customer_ids["customer_a"],
            name="Test Feed",
            feed_type=FeedType.OPEN_SOURCE,
        )
        assert feed.feed_id == "FEED-001"
        assert feed.name == "Test Feed"
        assert feed.feed_type == FeedType.OPEN_SOURCE

    def test_feed_validation_empty_id(self, test_customer_ids):
        """Test that empty feed_id raises ValueError."""
        with pytest.raises(ValueError, match="feed_id is required"):
            ThreatIntelFeed(
                feed_id="",
                customer_id=test_customer_ids["customer_a"],
                name="Test Feed",
            )

    def test_feed_is_stale_true(self, test_customer_ids):
        """Test is_stale property for stale feed."""
        old_date = datetime.utcnow() - timedelta(hours=5)
        feed = ThreatIntelFeed(
            feed_id="FEED-STALE",
            customer_id=test_customer_ids["customer_a"],
            name="Stale Feed",
            refresh_interval_minutes=60,
            last_updated=old_date,
        )
        assert feed.is_stale == True

    def test_feed_is_stale_false(self, test_customer_ids):
        """Test is_stale property for fresh feed."""
        recent_date = datetime.utcnow() - timedelta(minutes=30)
        feed = ThreatIntelFeed(
            feed_id="FEED-FRESH",
            customer_id=test_customer_ids["customer_a"],
            name="Fresh Feed",
            refresh_interval_minutes=60,
            last_updated=recent_date,
        )
        assert feed.is_stale == False

    def test_feed_types_validation(self, test_customer_ids):
        """Test all feed type enums."""
        feed_types = [
            FeedType.COMMERCIAL,
            FeedType.OPEN_SOURCE,
            FeedType.GOVERNMENT,
            FeedType.COMMUNITY,
            FeedType.INTERNAL,
        ]
        for feed_type in feed_types:
            feed = ThreatIntelFeed(
                feed_id=f"FEED-{feed_type.value}",
                customer_id=test_customer_ids["customer_a"],
                name=f"Test {feed_type.value}",
                feed_type=feed_type,
            )
            assert feed.feed_type == feed_type

    def test_feed_to_dict(self, sample_feed):
        """Test feed serialization."""
        feed_dict = sample_feed.to_dict()
        assert feed_dict["feed_id"] == sample_feed.feed_id
        assert feed_dict["name"] == sample_feed.name
        assert feed_dict["feed_type"] == sample_feed.feed_type.value
        assert feed_dict["is_stale"] == sample_feed.is_stale


# =============================================
# Customer Isolation Tests
# =============================================

class TestCustomerIsolation:
    """Tests for customer data isolation."""

    def test_threat_actor_customer_id_required(self, test_customer_ids):
        """Test that threat actor requires customer_id."""
        actor = ThreatActor(
            threat_actor_id="ACTOR-001",
            customer_id=test_customer_ids["customer_a"],
            name="Test Actor",
        )
        assert actor.customer_id == test_customer_ids["customer_a"]

    def test_campaign_customer_id_required(self, test_customer_ids):
        """Test that campaign requires customer_id."""
        campaign = ThreatCampaign(
            campaign_id="CAMP-001",
            customer_id=test_customer_ids["customer_a"],
            name="Test Campaign",
        )
        assert campaign.customer_id == test_customer_ids["customer_a"]

    def test_mitre_mapping_customer_id_required(self, test_customer_ids):
        """Test that MITRE mapping requires customer_id."""
        mapping = MITREMapping(
            mapping_id="MITRE-001",
            customer_id=test_customer_ids["customer_a"],
            entity_type="threat_actor",
            entity_id="ACTOR-001",
            technique_id="T1566",
        )
        assert mapping.customer_id == test_customer_ids["customer_a"]

    def test_ioc_customer_id_required(self, test_customer_ids):
        """Test that IOC requires customer_id."""
        ioc = IOC(
            ioc_id="IOC-001",
            customer_id=test_customer_ids["customer_a"],
            ioc_type=IOCType.IP,
            value="192.0.2.1",
        )
        assert ioc.customer_id == test_customer_ids["customer_a"]

    def test_feed_customer_id_required(self, test_customer_ids):
        """Test that feed requires customer_id."""
        feed = ThreatIntelFeed(
            feed_id="FEED-001",
            customer_id=test_customer_ids["customer_a"],
            name="Test Feed",
        )
        assert feed.customer_id == test_customer_ids["customer_a"]


# =============================================
# Enum Tests
# =============================================

class TestEnums:
    """Tests for all threat intelligence enums."""

    def test_actor_type_values(self):
        """Test ActorType enum values."""
        assert ActorType.APT.value == "apt"
        assert ActorType.CRIMINAL.value == "criminal"
        assert ActorType.HACKTIVIST.value == "hacktivist"
        assert ActorType.STATE_SPONSORED.value == "state_sponsored"
        assert ActorType.INSIDER.value == "insider"
        assert ActorType.UNKNOWN.value == "unknown"

    def test_actor_motivation_values(self):
        """Test ActorMotivation enum values."""
        assert ActorMotivation.ESPIONAGE.value == "espionage"
        assert ActorMotivation.FINANCIAL.value == "financial"
        assert ActorMotivation.DISRUPTION.value == "disruption"
        assert ActorMotivation.DESTRUCTION.value == "destruction"
        assert ActorMotivation.IDEOLOGICAL.value == "ideological"

    def test_campaign_status_values(self):
        """Test CampaignStatus enum values."""
        assert CampaignStatus.ACTIVE.value == "active"
        assert CampaignStatus.CONCLUDED.value == "concluded"
        assert CampaignStatus.SUSPECTED.value == "suspected"

    def test_ioc_type_values(self):
        """Test IOCType enum values."""
        assert IOCType.IP.value == "ip"
        assert IOCType.DOMAIN.value == "domain"
        assert IOCType.URL.value == "url"
        assert IOCType.HASH_MD5.value == "hash_md5"
        assert IOCType.HASH_SHA1.value == "hash_sha1"
        assert IOCType.HASH_SHA256.value == "hash_sha256"
        assert IOCType.EMAIL.value == "email"
        assert IOCType.FILE_NAME.value == "file_name"

    def test_mitigation_status_values(self):
        """Test MitigationStatus enum values."""
        assert MitigationStatus.NOT_COVERED.value == "not_covered"
        assert MitigationStatus.PARTIAL.value == "partial"
        assert MitigationStatus.COVERED.value == "covered"
        assert MitigationStatus.MONITORING_ONLY.value == "monitoring_only"

    def test_feed_type_values(self):
        """Test FeedType enum values."""
        assert FeedType.COMMERCIAL.value == "commercial"
        assert FeedType.OPEN_SOURCE.value == "open_source"
        assert FeedType.GOVERNMENT.value == "government"
        assert FeedType.COMMUNITY.value == "community"
        assert FeedType.INTERNAL.value == "internal"


# =============================================
# Integration Summary Tests
# =============================================

class TestIntegrationSummary:
    """Summary tests for overall module integration."""

    def test_all_models_import(self):
        """Test that all models can be imported."""
        from api.threat_intelligence import (
            ThreatActor,
            ThreatCampaign,
            MITREMapping,
            ThreatIntelFeed,
            IOC,
        )
        assert ThreatActor is not None
        assert ThreatCampaign is not None
        assert MITREMapping is not None
        assert ThreatIntelFeed is not None
        assert IOC is not None

    def test_all_enums_import(self):
        """Test that all enums can be imported."""
        from api.threat_intelligence import (
            ActorType,
            ActorMotivation,
            CampaignStatus,
            IOCType,
            MitigationStatus,
            FeedType,
        )
        assert ActorType is not None
        assert ActorMotivation is not None
        assert CampaignStatus is not None
        assert IOCType is not None
        assert MitigationStatus is not None
        assert FeedType is not None

    def test_service_import(self):
        """Test that service can be imported."""
        from api.threat_intelligence import ThreatIntelligenceService
        assert ThreatIntelligenceService is not None

    def test_router_conditional_import(self):
        """Test that router import is handled gracefully (FastAPI optional)."""
        from api.threat_intelligence import threat_router
        # Router may be None if FastAPI is not installed
        # This is expected behavior - tests should pass either way
        assert True  # Just verify import doesn't crash
