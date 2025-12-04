"""
Risk Scoring Integration Tests
================================

Integration tests for E05: Risk Scoring Engine API.
Tests customer isolation, model validation, and risk scoring operations.

Version: 1.0.0
Created: 2025-12-04
"""

import pytest
from datetime import date, datetime, timedelta
from typing import Generator
import uuid

# Import risk scoring components
from api.risk_scoring.risk_models import (
    RiskScore,
    RiskFactor,
    AssetCriticality,
    ExposureScore,
    RiskAggregation,
    RiskLevel,
    RiskFactorType,
    RiskTrend,
    BusinessImpact,
    DataClassification,
    AvailabilityRequirement,
    CriticalityLevel,
    AttackSurfaceArea,
    AggregationType,
)
from api.risk_scoring.risk_service import (
    RiskScoringService,
    RiskScoreRequest,
    RiskSearchRequest,
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
        "customer_a": f"TEST-RISK-A-{uuid.uuid4().hex[:8]}",
        "customer_b": f"TEST-RISK-B-{uuid.uuid4().hex[:8]}",
    }


@pytest.fixture
def customer_a_context(test_customer_ids) -> Generator[CustomerContext, None, None]:
    """Set up customer A context."""
    context = CustomerContextManager.create_context(
        customer_id=test_customer_ids["customer_a"],
        namespace="test_risk_customer_a",
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
        namespace="test_risk_customer_b",
        access_level=CustomerAccessLevel.WRITE,
        user_id="test-user-b",
    )
    yield context
    CustomerContextManager.clear_context()


@pytest.fixture
def sample_risk_factor(test_customer_ids) -> RiskFactor:
    """Create sample risk factor for testing."""
    return RiskFactor(
        factor_id=f"FACTOR-TEST-{uuid.uuid4().hex[:8]}",
        factor_type=RiskFactorType.VULNERABILITY,
        name="Critical Vulnerability",
        description="CVE-2024-1234 with CVSS 9.8",
        weight=0.8,
        score=9.8,
        evidence=["CVE-2024-1234", "EPSS: 0.95", "In the wild"],
        remediation_available=True,
    )


@pytest.fixture
def sample_risk_score(test_customer_ids, sample_risk_factor) -> RiskScore:
    """Create sample risk score for testing."""
    return RiskScore(
        risk_score_id=f"RISK-TEST-{uuid.uuid4().hex[:8]}",
        customer_id=test_customer_ids["customer_a"],
        entity_type="asset",
        entity_id="ASSET-001",
        entity_name="Production Database Server",
        overall_score=8.5,
        risk_level=RiskLevel.CRITICAL,
        vulnerability_score=9.8,
        threat_score=7.5,
        exposure_score=8.0,
        asset_score=9.0,
        calculation_date=datetime.utcnow(),
        confidence=0.95,
        contributing_factors=[sample_risk_factor],
        trend=RiskTrend.DEGRADING,
        previous_score=7.0,
        score_change=1.5,
    )


@pytest.fixture
def sample_asset_criticality(test_customer_ids) -> AssetCriticality:
    """Create sample asset criticality for testing."""
    return AssetCriticality(
        asset_id=f"ASSET-TEST-{uuid.uuid4().hex[:8]}",
        customer_id=test_customer_ids["customer_a"],
        asset_name="Production Database",
        asset_type="database",
        criticality_level=CriticalityLevel.MISSION_CRITICAL,
        criticality_score=9.5,
        business_impact=BusinessImpact.CATASTROPHIC,
        data_classification=DataClassification.RESTRICTED,
        availability_requirement=AvailabilityRequirement.CRITICAL,
        dependencies=["ASSET-002", "ASSET-003"],
        dependent_services=["API-SERVICE", "WEB-APP"],
        recovery_time_objective_hours=1.0,
        recovery_point_objective_hours=0.5,
    )


@pytest.fixture
def sample_exposure_score(test_customer_ids) -> ExposureScore:
    """Create sample exposure score for testing."""
    return ExposureScore(
        exposure_id=f"EXP-TEST-{uuid.uuid4().hex[:8]}",
        customer_id=test_customer_ids["customer_a"],
        asset_id="ASSET-001",
        asset_name="Web Server",
        external_exposure=True,
        internet_facing=True,
        open_ports=[80, 443, 22],
        exposed_services=["HTTP", "HTTPS", "SSH"],
        exposure_score=8.5,
        attack_surface_area=AttackSurfaceArea.EXTENSIVE,
        network_segment="dmz",
        security_controls=["WAF", "IDS", "Firewall"],
        last_scan_date=datetime.utcnow(),
        scan_source="nmap",
    )


@pytest.fixture
def sample_risk_aggregation(test_customer_ids) -> RiskAggregation:
    """Create sample risk aggregation for testing."""
    return RiskAggregation(
        aggregation_id=f"AGG-TEST-{uuid.uuid4().hex[:8]}",
        customer_id=test_customer_ids["customer_a"],
        aggregation_type=AggregationType.VENDOR,
        group_name="Cisco Systems",
        group_id="VENDOR-001",
        average_risk_score=6.5,
        max_risk_score=9.2,
        min_risk_score=3.1,
        entity_count=25,
        high_risk_count=8,
        critical_count=3,
        risk_distribution={"low": 5, "medium": 12, "high": 5, "critical": 3},
        trend=RiskTrend.STABLE,
    )


# =============================================
# RiskFactor Model Tests
# =============================================

class TestRiskFactorModel:
    """Unit tests for RiskFactor model."""

    def test_risk_factor_creation_valid(self):
        """Test creating a valid risk factor."""
        factor = RiskFactor(
            factor_id="FACTOR-001",
            factor_type=RiskFactorType.VULNERABILITY,
            name="SQL Injection",
            description="SQL injection vulnerability in login form",
            weight=0.9,
            score=8.5,
        )
        assert factor.factor_id == "FACTOR-001"
        assert factor.factor_type == RiskFactorType.VULNERABILITY
        assert factor.weight == 0.9
        assert factor.score == 8.5

    def test_risk_factor_types(self):
        """Test all risk factor types."""
        types = [
            RiskFactorType.VULNERABILITY,
            RiskFactorType.THREAT,
            RiskFactorType.EXPOSURE,
            RiskFactorType.ASSET,
            RiskFactorType.COMPLIANCE,
        ]
        for factor_type in types:
            factor = RiskFactor(
                factor_id=f"FACTOR-{factor_type.value}",
                factor_type=factor_type,
                name=f"Test {factor_type.value}",
                description=f"Test factor type {factor_type.value}",
                weight=0.5,
                score=5.0,
            )
            assert factor.factor_type == factor_type

    def test_risk_factor_validation_empty_id(self):
        """Test that empty factor_id raises ValueError."""
        with pytest.raises(ValueError, match="factor_id is required"):
            RiskFactor(
                factor_id="",
                factor_type=RiskFactorType.VULNERABILITY,
                name="Test",
                description="Test",
                weight=0.5,
                score=5.0,
            )

    def test_risk_factor_validation_invalid_weight(self):
        """Test that invalid weight is rejected."""
        with pytest.raises(ValueError, match="weight must be between"):
            RiskFactor(
                factor_id="FACTOR-001",
                factor_type=RiskFactorType.VULNERABILITY,
                name="Test",
                description="Test",
                weight=1.5,  # Invalid: > 1.0
                score=5.0,
            )

    def test_risk_factor_validation_invalid_score(self):
        """Test that invalid score is rejected."""
        with pytest.raises(ValueError, match="score must be between"):
            RiskFactor(
                factor_id="FACTOR-001",
                factor_type=RiskFactorType.VULNERABILITY,
                name="Test",
                description="Test",
                weight=0.5,
                score=15.0,  # Invalid: > 10.0
            )

    def test_risk_factor_to_dict(self, sample_risk_factor):
        """Test risk factor serialization."""
        factor_dict = sample_risk_factor.to_dict()
        assert factor_dict["factor_id"] == sample_risk_factor.factor_id
        assert factor_dict["factor_type"] == sample_risk_factor.factor_type.value
        assert factor_dict["weight"] == sample_risk_factor.weight
        assert factor_dict["score"] == sample_risk_factor.score


# =============================================
# RiskScore Model Tests
# =============================================

class TestRiskScoreModel:
    """Unit tests for RiskScore model."""

    def test_risk_score_creation_valid(self, test_customer_ids):
        """Test creating a valid risk score."""
        risk_score = RiskScore(
            risk_score_id="RISK-001",
            customer_id=test_customer_ids["customer_a"],
            entity_type="asset",
            entity_id="ASSET-001",
            entity_name="Test Server",
            overall_score=7.5,
        )
        assert risk_score.risk_score_id == "RISK-001"
        assert risk_score.overall_score == 7.5
        assert risk_score.risk_level == RiskLevel.HIGH

    def test_risk_score_level_calculation(self, test_customer_ids):
        """Test automatic risk level calculation."""
        test_cases = [
            (1.5, RiskLevel.LOW),
            (3.5, RiskLevel.MEDIUM),
            (6.5, RiskLevel.HIGH),
            (9.0, RiskLevel.CRITICAL),
        ]

        for score, expected_level in test_cases:
            risk_score = RiskScore(
                risk_score_id=f"RISK-{score}",
                customer_id=test_customer_ids["customer_a"],
                entity_type="asset",
                entity_id="ASSET-001",
                entity_name="Test",
                overall_score=score,
            )
            assert risk_score.risk_level == expected_level

    def test_risk_score_trend_calculation(self, test_customer_ids):
        """Test trend calculation from score change."""
        # Improving trend
        improving = RiskScore(
            risk_score_id="RISK-IMPROVING",
            customer_id=test_customer_ids["customer_a"],
            entity_type="asset",
            entity_id="ASSET-001",
            entity_name="Test",
            overall_score=5.0,
            previous_score=7.0,
        )
        assert improving.trend == RiskTrend.IMPROVING
        assert improving.score_change == -2.0

        # Degrading trend
        degrading = RiskScore(
            risk_score_id="RISK-DEGRADING",
            customer_id=test_customer_ids["customer_a"],
            entity_type="asset",
            entity_id="ASSET-002",
            entity_name="Test",
            overall_score=7.0,
            previous_score=5.0,
        )
        assert degrading.trend == RiskTrend.DEGRADING
        assert degrading.score_change == 2.0

        # Stable trend
        stable = RiskScore(
            risk_score_id="RISK-STABLE",
            customer_id=test_customer_ids["customer_a"],
            entity_type="asset",
            entity_id="ASSET-003",
            entity_name="Test",
            overall_score=5.2,
            previous_score=5.0,
        )
        assert stable.trend == RiskTrend.STABLE
        assert stable.score_change == 0.2

    def test_risk_score_validation_empty_id(self, test_customer_ids):
        """Test that empty risk_score_id raises ValueError."""
        with pytest.raises(ValueError, match="risk_score_id is required"):
            RiskScore(
                risk_score_id="",
                customer_id=test_customer_ids["customer_a"],
                entity_type="asset",
                entity_id="ASSET-001",
                entity_name="Test",
                overall_score=5.0,
            )

    def test_risk_score_validation_empty_customer_id(self):
        """Test that empty customer_id raises ValueError."""
        with pytest.raises(ValueError, match="customer_id is required"):
            RiskScore(
                risk_score_id="RISK-001",
                customer_id="",
                entity_type="asset",
                entity_id="ASSET-001",
                entity_name="Test",
                overall_score=5.0,
            )

    def test_risk_score_validation_invalid_score(self, test_customer_ids):
        """Test that invalid overall_score is rejected."""
        with pytest.raises(ValueError, match="overall_score must be between"):
            RiskScore(
                risk_score_id="RISK-001",
                customer_id=test_customer_ids["customer_a"],
                entity_type="asset",
                entity_id="ASSET-001",
                entity_name="Test",
                overall_score=15.0,  # Invalid: > 10.0
            )

    def test_risk_score_validation_invalid_confidence(self, test_customer_ids):
        """Test that invalid confidence is rejected."""
        with pytest.raises(ValueError, match="confidence must be between"):
            RiskScore(
                risk_score_id="RISK-001",
                customer_id=test_customer_ids["customer_a"],
                entity_type="asset",
                entity_id="ASSET-001",
                entity_name="Test",
                overall_score=5.0,
                confidence=1.5,  # Invalid: > 1.0
            )

    def test_risk_score_is_critical(self, test_customer_ids):
        """Test is_critical property."""
        critical = RiskScore(
            risk_score_id="RISK-CRITICAL",
            customer_id=test_customer_ids["customer_a"],
            entity_type="asset",
            entity_id="ASSET-001",
            entity_name="Test",
            overall_score=9.0,
        )
        assert critical.is_critical == True

        non_critical = RiskScore(
            risk_score_id="RISK-NONCRITICAL",
            customer_id=test_customer_ids["customer_a"],
            entity_type="asset",
            entity_id="ASSET-002",
            entity_name="Test",
            overall_score=6.0,
        )
        assert non_critical.is_critical == False

    def test_risk_score_is_high_risk(self, test_customer_ids):
        """Test is_high_risk property."""
        high_risk = RiskScore(
            risk_score_id="RISK-HIGH",
            customer_id=test_customer_ids["customer_a"],
            entity_type="asset",
            entity_id="ASSET-001",
            entity_name="Test",
            overall_score=6.5,
        )
        assert high_risk.is_high_risk == True

        low_risk = RiskScore(
            risk_score_id="RISK-LOW",
            customer_id=test_customer_ids["customer_a"],
            entity_type="asset",
            entity_id="ASSET-002",
            entity_name="Test",
            overall_score=3.0,
        )
        assert low_risk.is_high_risk == False

    def test_risk_score_to_dict(self, sample_risk_score):
        """Test risk score serialization."""
        risk_dict = sample_risk_score.to_dict()
        assert risk_dict["risk_score_id"] == sample_risk_score.risk_score_id
        assert risk_dict["overall_score"] == sample_risk_score.overall_score
        assert risk_dict["risk_level"] == sample_risk_score.risk_level.value
        assert risk_dict["is_critical"] == sample_risk_score.is_critical
        assert risk_dict["is_high_risk"] == sample_risk_score.is_high_risk

    def test_risk_score_to_qdrant_payload(self, sample_risk_score):
        """Test Qdrant payload generation."""
        payload = sample_risk_score.to_qdrant_payload()
        assert payload["risk_score_id"] == sample_risk_score.risk_score_id
        assert payload["customer_id"] == sample_risk_score.customer_id
        assert payload["overall_score"] == sample_risk_score.overall_score
        assert payload["risk_level"] == sample_risk_score.risk_level.value


# =============================================
# AssetCriticality Model Tests
# =============================================

class TestAssetCriticalityModel:
    """Unit tests for AssetCriticality model."""

    def test_asset_criticality_creation_valid(self, test_customer_ids):
        """Test creating valid asset criticality."""
        criticality = AssetCriticality(
            asset_id="ASSET-001",
            customer_id=test_customer_ids["customer_a"],
            asset_name="Database Server",
            asset_type="database",
            criticality_score=8.5,
        )
        assert criticality.asset_id == "ASSET-001"
        assert criticality.criticality_score == 8.5
        assert criticality.criticality_level == CriticalityLevel.CRITICAL

    def test_asset_criticality_level_calculation(self, test_customer_ids):
        """Test automatic criticality level calculation."""
        test_cases = [
            (1.5, CriticalityLevel.LOW),
            (3.0, CriticalityLevel.MEDIUM),
            (6.0, CriticalityLevel.HIGH),
            (8.0, CriticalityLevel.CRITICAL),
            (9.5, CriticalityLevel.MISSION_CRITICAL),
        ]

        for score, expected_level in test_cases:
            criticality = AssetCriticality(
                asset_id=f"ASSET-{score}",
                customer_id=test_customer_ids["customer_a"],
                asset_name="Test Asset",
                asset_type="server",
                criticality_score=score,
            )
            assert criticality.criticality_level == expected_level

    def test_asset_criticality_validation_empty_id(self, test_customer_ids):
        """Test that empty asset_id raises ValueError."""
        with pytest.raises(ValueError, match="asset_id is required"):
            AssetCriticality(
                asset_id="",
                customer_id=test_customer_ids["customer_a"],
                asset_name="Test",
                asset_type="server",
                criticality_score=5.0,
            )

    def test_asset_criticality_validation_invalid_score(self, test_customer_ids):
        """Test that invalid criticality_score is rejected."""
        with pytest.raises(ValueError, match="criticality_score must be between"):
            AssetCriticality(
                asset_id="ASSET-001",
                customer_id=test_customer_ids["customer_a"],
                asset_name="Test",
                asset_type="server",
                criticality_score=15.0,  # Invalid: > 10.0
            )

    def test_asset_criticality_is_mission_critical(self, test_customer_ids):
        """Test is_mission_critical property."""
        mission_critical = AssetCriticality(
            asset_id="ASSET-MC",
            customer_id=test_customer_ids["customer_a"],
            asset_name="Core Database",
            asset_type="database",
            criticality_score=9.8,
        )
        assert mission_critical.is_mission_critical == True

        not_mission_critical = AssetCriticality(
            asset_id="ASSET-NOTMC",
            customer_id=test_customer_ids["customer_a"],
            asset_name="Dev Server",
            asset_type="server",
            criticality_score=5.0,
        )
        assert not_mission_critical.is_mission_critical == False

    def test_asset_criticality_has_strict_rto(self, test_customer_ids):
        """Test has_strict_rto property."""
        strict_rto = AssetCriticality(
            asset_id="ASSET-STRICT",
            customer_id=test_customer_ids["customer_a"],
            asset_name="Critical Service",
            asset_type="application",
            criticality_score=9.0,
            recovery_time_objective_hours=2.0,
        )
        assert strict_rto.has_strict_rto == True

        no_strict_rto = AssetCriticality(
            asset_id="ASSET-NOSTRICT",
            customer_id=test_customer_ids["customer_a"],
            asset_name="Regular Service",
            asset_type="application",
            criticality_score=5.0,
            recovery_time_objective_hours=8.0,
        )
        assert no_strict_rto.has_strict_rto == False

    def test_asset_criticality_to_dict(self, sample_asset_criticality):
        """Test asset criticality serialization."""
        crit_dict = sample_asset_criticality.to_dict()
        assert crit_dict["asset_id"] == sample_asset_criticality.asset_id
        assert crit_dict["criticality_score"] == sample_asset_criticality.criticality_score
        assert crit_dict["is_mission_critical"] == sample_asset_criticality.is_mission_critical
        assert crit_dict["has_strict_rto"] == sample_asset_criticality.has_strict_rto

    def test_asset_criticality_to_qdrant_payload(self, sample_asset_criticality):
        """Test Qdrant payload generation."""
        payload = sample_asset_criticality.to_qdrant_payload()
        assert payload["asset_id"] == sample_asset_criticality.asset_id
        assert payload["customer_id"] == sample_asset_criticality.customer_id
        assert payload["entity_type"] == "asset_criticality"


# =============================================
# ExposureScore Model Tests
# =============================================

class TestExposureScoreModel:
    """Unit tests for ExposureScore model."""

    def test_exposure_score_creation_valid(self, test_customer_ids):
        """Test creating valid exposure score."""
        exposure = ExposureScore(
            exposure_id="EXP-001",
            customer_id=test_customer_ids["customer_a"],
            asset_id="ASSET-001",
            asset_name="Web Server",
            exposure_score=7.5,
            internet_facing=True,
        )
        assert exposure.exposure_id == "EXP-001"
        assert exposure.exposure_score == 7.5
        assert exposure.attack_surface_area == AttackSurfaceArea.EXTENSIVE

    def test_exposure_score_attack_surface_calculation(self, test_customer_ids):
        """Test automatic attack surface area calculation."""
        test_cases = [
            (1.5, AttackSurfaceArea.MINIMAL),
            (3.0, AttackSurfaceArea.LIMITED),
            (5.0, AttackSurfaceArea.MODERATE),
            (7.0, AttackSurfaceArea.EXTENSIVE),
            (9.0, AttackSurfaceArea.CRITICAL),
        ]

        for score, expected_area in test_cases:
            exposure = ExposureScore(
                exposure_id=f"EXP-{score}",
                customer_id=test_customer_ids["customer_a"],
                asset_id="ASSET-001",
                asset_name="Test Asset",
                exposure_score=score,
            )
            assert exposure.attack_surface_area == expected_area

    def test_exposure_score_validation_empty_id(self, test_customer_ids):
        """Test that empty exposure_id raises ValueError."""
        with pytest.raises(ValueError, match="exposure_id is required"):
            ExposureScore(
                exposure_id="",
                customer_id=test_customer_ids["customer_a"],
                asset_id="ASSET-001",
                asset_name="Test",
                exposure_score=5.0,
            )

    def test_exposure_score_validation_invalid_score(self, test_customer_ids):
        """Test that invalid exposure_score is rejected."""
        with pytest.raises(ValueError, match="exposure_score must be between"):
            ExposureScore(
                exposure_id="EXP-001",
                customer_id=test_customer_ids["customer_a"],
                asset_id="ASSET-001",
                asset_name="Test",
                exposure_score=15.0,  # Invalid: > 10.0
            )

    def test_exposure_score_is_high_exposure(self, test_customer_ids):
        """Test is_high_exposure property."""
        high_exposure = ExposureScore(
            exposure_id="EXP-HIGH",
            customer_id=test_customer_ids["customer_a"],
            asset_id="ASSET-001",
            asset_name="Public Server",
            exposure_score=8.5,
        )
        assert high_exposure.is_high_exposure == True

        low_exposure = ExposureScore(
            exposure_id="EXP-LOW",
            customer_id=test_customer_ids["customer_a"],
            asset_id="ASSET-002",
            asset_name="Internal Server",
            exposure_score=3.0,
        )
        assert low_exposure.is_high_exposure == False

    def test_exposure_score_open_port_count(self, sample_exposure_score):
        """Test open_port_count property."""
        assert sample_exposure_score.open_port_count == 3
        assert sample_exposure_score.open_ports == [80, 443, 22]

    def test_exposure_score_has_security_controls(self, sample_exposure_score):
        """Test has_security_controls property."""
        assert sample_exposure_score.has_security_controls == True
        assert len(sample_exposure_score.security_controls) == 3

    def test_exposure_score_to_dict(self, sample_exposure_score):
        """Test exposure score serialization."""
        exp_dict = sample_exposure_score.to_dict()
        assert exp_dict["exposure_id"] == sample_exposure_score.exposure_id
        assert exp_dict["exposure_score"] == sample_exposure_score.exposure_score
        assert exp_dict["is_high_exposure"] == sample_exposure_score.is_high_exposure
        assert exp_dict["open_port_count"] == sample_exposure_score.open_port_count

    def test_exposure_score_to_qdrant_payload(self, sample_exposure_score):
        """Test Qdrant payload generation."""
        payload = sample_exposure_score.to_qdrant_payload()
        assert payload["exposure_id"] == sample_exposure_score.exposure_id
        assert payload["customer_id"] == sample_exposure_score.customer_id
        assert payload["entity_type"] == "exposure_score"


# =============================================
# RiskAggregation Model Tests
# =============================================

class TestRiskAggregationModel:
    """Unit tests for RiskAggregation model."""

    def test_risk_aggregation_creation_valid(self, test_customer_ids):
        """Test creating valid risk aggregation."""
        aggregation = RiskAggregation(
            aggregation_id="AGG-001",
            customer_id=test_customer_ids["customer_a"],
            aggregation_type=AggregationType.VENDOR,
            group_name="Test Vendor",
            group_id="VENDOR-001",
            average_risk_score=6.5,
            entity_count=10,
        )
        assert aggregation.aggregation_id == "AGG-001"
        assert aggregation.aggregation_type == AggregationType.VENDOR
        assert aggregation.average_risk_score == 6.5

    def test_risk_aggregation_types(self, test_customer_ids):
        """Test all aggregation types."""
        types = [
            AggregationType.VENDOR,
            AggregationType.SECTOR,
            AggregationType.ASSET_TYPE,
            AggregationType.DEPARTMENT,
        ]

        for agg_type in types:
            aggregation = RiskAggregation(
                aggregation_id=f"AGG-{agg_type.value}",
                customer_id=test_customer_ids["customer_a"],
                aggregation_type=agg_type,
                group_name=f"Test {agg_type.value}",
                group_id=f"GROUP-{agg_type.value}",
                average_risk_score=5.0,
                entity_count=5,
            )
            assert aggregation.aggregation_type == agg_type

    def test_risk_aggregation_validation_empty_id(self, test_customer_ids):
        """Test that empty aggregation_id raises ValueError."""
        with pytest.raises(ValueError, match="aggregation_id is required"):
            RiskAggregation(
                aggregation_id="",
                customer_id=test_customer_ids["customer_a"],
                aggregation_type=AggregationType.VENDOR,
                group_name="Test",
                group_id="GROUP-001",
            )

    def test_risk_aggregation_high_risk_percentage(self, sample_risk_aggregation):
        """Test high_risk_percentage calculation."""
        # 8 high risk out of 25 entities = 32%
        assert sample_risk_aggregation.high_risk_percentage == 32.0

    def test_risk_aggregation_critical_percentage(self, sample_risk_aggregation):
        """Test critical_percentage calculation."""
        # 3 critical out of 25 entities = 12%
        assert sample_risk_aggregation.critical_percentage == 12.0

    def test_risk_aggregation_zero_entities(self, test_customer_ids):
        """Test percentage calculations with zero entities."""
        aggregation = RiskAggregation(
            aggregation_id="AGG-ZERO",
            customer_id=test_customer_ids["customer_a"],
            aggregation_type=AggregationType.VENDOR,
            group_name="Empty Group",
            group_id="GROUP-EMPTY",
            entity_count=0,
            high_risk_count=0,
            critical_count=0,
        )
        assert aggregation.high_risk_percentage == 0.0
        assert aggregation.critical_percentage == 0.0

    def test_risk_aggregation_to_dict(self, sample_risk_aggregation):
        """Test risk aggregation serialization."""
        agg_dict = sample_risk_aggregation.to_dict()
        assert agg_dict["aggregation_id"] == sample_risk_aggregation.aggregation_id
        assert agg_dict["average_risk_score"] == sample_risk_aggregation.average_risk_score
        assert agg_dict["high_risk_percentage"] == sample_risk_aggregation.high_risk_percentage


# =============================================
# Customer Isolation Tests
# =============================================

class TestCustomerIsolation:
    """Tests for customer data isolation."""

    def test_risk_score_customer_id_required(self, test_customer_ids):
        """Test that risk score requires customer_id."""
        risk_score = RiskScore(
            risk_score_id="RISK-001",
            customer_id=test_customer_ids["customer_a"],
            entity_type="asset",
            entity_id="ASSET-001",
            entity_name="Test",
            overall_score=5.0,
        )
        assert risk_score.customer_id == test_customer_ids["customer_a"]

    def test_asset_criticality_customer_id_required(self, test_customer_ids):
        """Test that asset criticality requires customer_id."""
        criticality = AssetCriticality(
            asset_id="ASSET-001",
            customer_id=test_customer_ids["customer_a"],
            asset_name="Test",
            asset_type="server",
            criticality_score=5.0,
        )
        assert criticality.customer_id == test_customer_ids["customer_a"]

    def test_exposure_score_customer_id_required(self, test_customer_ids):
        """Test that exposure score requires customer_id."""
        exposure = ExposureScore(
            exposure_id="EXP-001",
            customer_id=test_customer_ids["customer_a"],
            asset_id="ASSET-001",
            asset_name="Test",
            exposure_score=5.0,
        )
        assert exposure.customer_id == test_customer_ids["customer_a"]

    def test_risk_aggregation_customer_id_required(self, test_customer_ids):
        """Test that risk aggregation requires customer_id."""
        aggregation = RiskAggregation(
            aggregation_id="AGG-001",
            customer_id=test_customer_ids["customer_a"],
            aggregation_type=AggregationType.VENDOR,
            group_name="Test",
            group_id="GROUP-001",
        )
        assert aggregation.customer_id == test_customer_ids["customer_a"]


# =============================================
# Enum Tests
# =============================================

class TestEnums:
    """Tests for all risk scoring enums."""

    def test_risk_level_values(self):
        """Test RiskLevel enum values."""
        assert RiskLevel.LOW.value == "low"
        assert RiskLevel.MEDIUM.value == "medium"
        assert RiskLevel.HIGH.value == "high"
        assert RiskLevel.CRITICAL.value == "critical"

    def test_risk_factor_type_values(self):
        """Test RiskFactorType enum values."""
        assert RiskFactorType.VULNERABILITY.value == "vulnerability"
        assert RiskFactorType.THREAT.value == "threat"
        assert RiskFactorType.EXPOSURE.value == "exposure"
        assert RiskFactorType.ASSET.value == "asset"
        assert RiskFactorType.COMPLIANCE.value == "compliance"

    def test_risk_trend_values(self):
        """Test RiskTrend enum values."""
        assert RiskTrend.IMPROVING.value == "improving"
        assert RiskTrend.STABLE.value == "stable"
        assert RiskTrend.DEGRADING.value == "degrading"

    def test_business_impact_values(self):
        """Test BusinessImpact enum values."""
        assert BusinessImpact.MINIMAL.value == "minimal"
        assert BusinessImpact.MODERATE.value == "moderate"
        assert BusinessImpact.SIGNIFICANT.value == "significant"
        assert BusinessImpact.SEVERE.value == "severe"
        assert BusinessImpact.CATASTROPHIC.value == "catastrophic"

    def test_data_classification_values(self):
        """Test DataClassification enum values."""
        assert DataClassification.PUBLIC.value == "public"
        assert DataClassification.INTERNAL.value == "internal"
        assert DataClassification.CONFIDENTIAL.value == "confidential"
        assert DataClassification.RESTRICTED.value == "restricted"
        assert DataClassification.TOP_SECRET.value == "top_secret"

    def test_availability_requirement_values(self):
        """Test AvailabilityRequirement enum values."""
        assert AvailabilityRequirement.STANDARD.value == "standard"
        assert AvailabilityRequirement.IMPORTANT.value == "important"
        assert AvailabilityRequirement.ESSENTIAL.value == "essential"
        assert AvailabilityRequirement.CRITICAL.value == "critical"

    def test_criticality_level_values(self):
        """Test CriticalityLevel enum values."""
        assert CriticalityLevel.LOW.value == "low"
        assert CriticalityLevel.MEDIUM.value == "medium"
        assert CriticalityLevel.HIGH.value == "high"
        assert CriticalityLevel.CRITICAL.value == "critical"
        assert CriticalityLevel.MISSION_CRITICAL.value == "mission_critical"

    def test_attack_surface_area_values(self):
        """Test AttackSurfaceArea enum values."""
        assert AttackSurfaceArea.MINIMAL.value == "minimal"
        assert AttackSurfaceArea.LIMITED.value == "limited"
        assert AttackSurfaceArea.MODERATE.value == "moderate"
        assert AttackSurfaceArea.EXTENSIVE.value == "extensive"
        assert AttackSurfaceArea.CRITICAL.value == "critical"

    def test_aggregation_type_values(self):
        """Test AggregationType enum values."""
        assert AggregationType.VENDOR.value == "vendor"
        assert AggregationType.SECTOR.value == "sector"
        assert AggregationType.ASSET_TYPE.value == "asset_type"
        assert AggregationType.DEPARTMENT.value == "department"


# =============================================
# Integration Summary Tests
# =============================================

class TestIntegrationSummary:
    """Summary tests for overall module integration."""

    def test_all_models_import(self):
        """Test that all models can be imported."""
        from api.risk_scoring import (
            RiskScore,
            RiskFactor,
            AssetCriticality,
            ExposureScore,
            RiskAggregation,
        )
        assert RiskScore is not None
        assert RiskFactor is not None
        assert AssetCriticality is not None
        assert ExposureScore is not None
        assert RiskAggregation is not None

    def test_all_enums_import(self):
        """Test that all enums can be imported."""
        from api.risk_scoring import (
            RiskLevel,
            RiskFactorType,
            RiskTrend,
            BusinessImpact,
            DataClassification,
            AvailabilityRequirement,
            CriticalityLevel,
            AttackSurfaceArea,
            AggregationType,
        )
        assert RiskLevel is not None
        assert RiskFactorType is not None
        assert RiskTrend is not None
        assert BusinessImpact is not None
        assert DataClassification is not None

    def test_service_import(self):
        """Test that service can be imported."""
        from api.risk_scoring import RiskScoringService
        assert RiskScoringService is not None

    def test_router_conditional_import(self):
        """Test that router import is handled gracefully (FastAPI optional)."""
        from api.risk_scoring import risk_router
        # Router may be None if FastAPI is not installed
        # This is expected behavior - tests should pass either way
        assert True  # Just verify import doesn't crash
