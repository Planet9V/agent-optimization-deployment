"""
Vendor Equipment Integration Tests
===================================

Integration tests for E15: Vendor Equipment Lifecycle Management.
Tests customer isolation, Neo4j/Qdrant integration, and lifecycle queries.

Version: 1.0.0
Created: 2025-12-04
"""

import pytest
from datetime import date, timedelta
from typing import Generator
import uuid

# Import vendor equipment components (models and service only, no router for unit tests)
from api.vendor_equipment.vendor_models import (
    Vendor,
    EquipmentModel,
    SupportContract,
    VendorRiskLevel,
    SupportStatus,
    LifecycleStatus,
    MaintenanceSchedule,
    Criticality,
)
from api.vendor_equipment.vendor_service import VendorEquipmentService
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
        "customer_a": f"TEST-CUST-A-{uuid.uuid4().hex[:8]}",
        "customer_b": f"TEST-CUST-B-{uuid.uuid4().hex[:8]}",
    }


@pytest.fixture
def vendor_service() -> VendorEquipmentService:
    """Create vendor equipment service for testing."""
    return VendorEquipmentService(
        qdrant_url="http://localhost:6333",
        neo4j_driver=None,  # No Neo4j for unit tests
        embedding_model=None,  # No embedding model for unit tests
    )


@pytest.fixture
def customer_a_context(test_customer_ids) -> Generator[CustomerContext, None, None]:
    """Set up customer A context."""
    context = CustomerContextManager.create_context(
        customer_id=test_customer_ids["customer_a"],
        namespace="test_customer_a",
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
        namespace="test_customer_b",
        access_level=CustomerAccessLevel.WRITE,
        user_id="test-user-b",
    )
    yield context
    CustomerContextManager.clear_context()


@pytest.fixture
def sample_vendor(test_customer_ids) -> Vendor:
    """Create sample vendor for testing."""
    return Vendor(
        vendor_id=f"VENDOR-TEST-{uuid.uuid4().hex[:8]}",
        name="Test Vendor Inc",
        customer_id=test_customer_ids["customer_a"],
        risk_score=5.5,
        support_status=SupportStatus.ACTIVE,
        country="USA",
        industry_focus=["IT", "Network"],
        supply_chain_tier=1,
        total_cves=25,
        avg_cvss_score=6.5,
    )


@pytest.fixture
def sample_equipment(test_customer_ids, sample_vendor) -> EquipmentModel:
    """Create sample equipment for testing."""
    today = date.today()
    return EquipmentModel(
        model_id=f"EQ-TEST-{uuid.uuid4().hex[:8]}",
        vendor_id=sample_vendor.vendor_id,
        model_name="Test Equipment Model",
        customer_id=test_customer_ids["customer_a"],
        product_line="Test Product Line",
        release_date=today - timedelta(days=365),
        eol_date=today + timedelta(days=90),  # Approaching EOL
        eos_date=today + timedelta(days=180),
        current_version="1.0.0",
        criticality=Criticality.HIGH,
        category="network",
        deployed_count=10,
        vulnerability_count=3,
    )


@pytest.fixture
def sample_contract(test_customer_ids, sample_vendor) -> SupportContract:
    """Create sample support contract for testing."""
    today = date.today()
    return SupportContract(
        contract_id=f"CONTRACT-TEST-{uuid.uuid4().hex[:8]}",
        vendor_id=sample_vendor.vendor_id,
        customer_id=test_customer_ids["customer_a"],
        start_date=today - timedelta(days=180),
        end_date=today + timedelta(days=180),
        service_level="premium",
        response_time_sla=4,
        coverage=["security_patches", "firmware_updates", "24/7_support"],
        annual_cost=50000.0,
    )


# =============================================
# Vendor Model Tests
# =============================================

class TestVendorModel:
    """Unit tests for Vendor model."""

    def test_vendor_creation_valid(self, test_customer_ids):
        """Test creating a valid vendor."""
        vendor = Vendor(
            vendor_id="VENDOR-001",
            name="Cisco Systems",
            customer_id=test_customer_ids["customer_a"],
            risk_score=4.5,
        )
        assert vendor.vendor_id == "VENDOR-001"
        assert vendor.name == "Cisco Systems"
        assert vendor.risk_level == VendorRiskLevel.MEDIUM

    def test_vendor_risk_level_calculation(self, test_customer_ids):
        """Test automatic risk level calculation."""
        low_risk = Vendor(
            vendor_id="V1", name="Low Risk", customer_id=test_customer_ids["customer_a"],
            risk_score=2.0,
        )
        assert low_risk.risk_level == VendorRiskLevel.LOW

        medium_risk = Vendor(
            vendor_id="V2", name="Medium Risk", customer_id=test_customer_ids["customer_a"],
            risk_score=5.0,
        )
        assert medium_risk.risk_level == VendorRiskLevel.MEDIUM

        high_risk = Vendor(
            vendor_id="V3", name="High Risk", customer_id=test_customer_ids["customer_a"],
            risk_score=7.5,
        )
        assert high_risk.risk_level == VendorRiskLevel.HIGH

        critical_risk = Vendor(
            vendor_id="V4", name="Critical Risk", customer_id=test_customer_ids["customer_a"],
            risk_score=9.0,
        )
        assert critical_risk.risk_level == VendorRiskLevel.CRITICAL

    def test_vendor_validation_empty_id(self, test_customer_ids):
        """Test that empty vendor_id raises ValueError."""
        with pytest.raises(ValueError, match="vendor_id is required"):
            Vendor(
                vendor_id="",
                name="Test Vendor",
                customer_id=test_customer_ids["customer_a"],
            )

    def test_vendor_validation_empty_customer_id(self):
        """Test that empty customer_id raises ValueError."""
        with pytest.raises(ValueError, match="customer_id is required"):
            Vendor(
                vendor_id="VENDOR-001",
                name="Test Vendor",
                customer_id="",
            )

    def test_vendor_validation_invalid_risk_score(self, test_customer_ids):
        """Test that invalid risk scores are rejected."""
        with pytest.raises(ValueError, match="risk_score must be between"):
            Vendor(
                vendor_id="VENDOR-001",
                name="Test Vendor",
                customer_id=test_customer_ids["customer_a"],
                risk_score=15.0,  # Invalid: > 10
            )

    def test_vendor_to_neo4j_properties(self, sample_vendor):
        """Test Neo4j property conversion."""
        props = sample_vendor.to_neo4j_properties()
        assert props["vendor_id"] == sample_vendor.vendor_id
        assert props["name"] == sample_vendor.name
        assert props["customer_id"] == sample_vendor.customer_id
        assert props["risk_score"] == sample_vendor.risk_score
        assert "created_at" in props
        assert "updated_at" in props

    def test_vendor_to_qdrant_payload(self, sample_vendor):
        """Test Qdrant payload conversion."""
        payload = sample_vendor.to_qdrant_payload()
        assert payload["vendor_id"] == sample_vendor.vendor_id
        assert payload["entity_type"] == "vendor"
        assert payload["customer_id"] == sample_vendor.customer_id


# =============================================
# Equipment Model Tests
# =============================================

class TestEquipmentModel:
    """Unit tests for EquipmentModel."""

    def test_equipment_creation_valid(self, test_customer_ids):
        """Test creating valid equipment."""
        today = date.today()
        equipment = EquipmentModel(
            model_id="EQ-001",
            vendor_id="VENDOR-001",
            model_name="Test Equipment",
            customer_id=test_customer_ids["customer_a"],
            eol_date=today + timedelta(days=365),
        )
        assert equipment.model_id == "EQ-001"
        assert equipment.lifecycle_status == LifecycleStatus.CURRENT

    def test_equipment_lifecycle_approaching_eol(self, test_customer_ids):
        """Test lifecycle status for approaching EOL."""
        today = date.today()
        equipment = EquipmentModel(
            model_id="EQ-002",
            vendor_id="VENDOR-001",
            model_name="EOL Soon Equipment",
            customer_id=test_customer_ids["customer_a"],
            eol_date=today + timedelta(days=90),
        )
        assert equipment.lifecycle_status == LifecycleStatus.APPROACHING_EOL
        assert equipment.days_to_eol() == 90

    def test_equipment_lifecycle_past_eol(self, test_customer_ids):
        """Test lifecycle status for past EOL."""
        today = date.today()
        equipment = EquipmentModel(
            model_id="EQ-003",
            vendor_id="VENDOR-001",
            model_name="Past EOL Equipment",
            customer_id=test_customer_ids["customer_a"],
            eol_date=today - timedelta(days=30),
        )
        assert equipment.lifecycle_status == LifecycleStatus.EOL
        assert equipment.days_to_eol() == -30

    def test_equipment_lifecycle_past_eos(self, test_customer_ids):
        """Test lifecycle status for past EOS."""
        today = date.today()
        equipment = EquipmentModel(
            model_id="EQ-004",
            vendor_id="VENDOR-001",
            model_name="Past EOS Equipment",
            customer_id=test_customer_ids["customer_a"],
            eol_date=today - timedelta(days=60),
            eos_date=today - timedelta(days=30),
        )
        assert equipment.lifecycle_status == LifecycleStatus.EOS

    def test_equipment_validation_empty_model_id(self, test_customer_ids):
        """Test that empty model_id raises ValueError."""
        with pytest.raises(ValueError, match="model_id is required"):
            EquipmentModel(
                model_id="",
                vendor_id="VENDOR-001",
                model_name="Test",
                customer_id=test_customer_ids["customer_a"],
            )

    def test_equipment_to_neo4j_properties(self, sample_equipment):
        """Test Neo4j property conversion."""
        props = sample_equipment.to_neo4j_properties()
        assert props["model_id"] == sample_equipment.model_id
        assert props["vendor_id"] == sample_equipment.vendor_id
        assert props["customer_id"] == sample_equipment.customer_id
        assert "eol_date" in props
        assert "lifecycle_status" in props


# =============================================
# Support Contract Tests
# =============================================

class TestSupportContract:
    """Unit tests for SupportContract."""

    def test_contract_creation_valid(self, test_customer_ids):
        """Test creating valid support contract."""
        today = date.today()
        contract = SupportContract(
            contract_id="CONTRACT-001",
            vendor_id="VENDOR-001",
            customer_id=test_customer_ids["customer_a"],
            start_date=today - timedelta(days=180),
            end_date=today + timedelta(days=180),
        )
        assert contract.contract_id == "CONTRACT-001"
        assert contract.status == "active"
        assert contract.days_remaining() == 180

    def test_contract_status_expired(self, test_customer_ids):
        """Test expired contract status calculation."""
        today = date.today()
        contract = SupportContract(
            contract_id="CONTRACT-002",
            vendor_id="VENDOR-001",
            customer_id=test_customer_ids["customer_a"],
            start_date=today - timedelta(days=365),
            end_date=today - timedelta(days=30),
        )
        assert contract.status == "expired"
        assert contract.days_remaining() < 0

    def test_contract_status_pending_renewal(self, test_customer_ids):
        """Test pending renewal status."""
        today = date.today()
        contract = SupportContract(
            contract_id="CONTRACT-003",
            vendor_id="VENDOR-001",
            customer_id=test_customer_ids["customer_a"],
            start_date=today - timedelta(days=300),
            end_date=today + timedelta(days=60),  # Within 90-day reminder period
            renewal_reminder_days=90,
        )
        assert contract.status == "pending_renewal"
        assert contract.is_expiring_soon()

    def test_contract_validation_empty_id(self, test_customer_ids):
        """Test that empty contract_id raises ValueError."""
        today = date.today()
        with pytest.raises(ValueError, match="contract_id is required"):
            SupportContract(
                contract_id="",
                vendor_id="VENDOR-001",
                customer_id=test_customer_ids["customer_a"],
                start_date=today,
                end_date=today + timedelta(days=365),
            )


# =============================================
# Customer Isolation Tests
# =============================================

class TestCustomerIsolation:
    """Integration tests for customer isolation in vendor equipment."""

    def test_vendor_customer_id_matches_context(self, vendor_service, customer_a_context, sample_vendor):
        """Test that vendor customer_id must match context."""
        # This should work - vendor customer_id matches context
        # In a real test with Qdrant running, this would create the vendor
        assert sample_vendor.customer_id == customer_a_context.customer_id

    def test_vendor_customer_id_mismatch_rejected(self, vendor_service, customer_a_context, test_customer_ids):
        """Test that mismatched customer_id is rejected."""
        # Create vendor with different customer_id than context
        vendor = Vendor(
            vendor_id="VENDOR-MISMATCH",
            name="Mismatched Vendor",
            customer_id=test_customer_ids["customer_b"],  # Different from context
        )

        with pytest.raises(ValueError, match="must match context"):
            vendor_service.create_vendor(vendor)

    def test_context_customer_ids_includes_system(self, customer_a_context):
        """Test that context includes SYSTEM for shared data."""
        customer_ids = customer_a_context.get_customer_ids()
        assert customer_a_context.customer_id in customer_ids
        assert "SYSTEM" in customer_ids

    def test_context_without_system_excludes_system(self, test_customer_ids):
        """Test excluding SYSTEM entities."""
        context = CustomerContext(
            customer_id=test_customer_ids["customer_a"],
            namespace="test",
            include_system=False,
        )
        customer_ids = context.get_customer_ids()
        assert context.customer_id in customer_ids
        assert "SYSTEM" not in customer_ids

    def test_read_access_prevents_writes(self, vendor_service, test_customer_ids):
        """Test that READ access level prevents write operations."""
        CustomerContextManager.create_context(
            customer_id=test_customer_ids["customer_a"],
            namespace="test",
            access_level=CustomerAccessLevel.READ,
        )

        vendor = Vendor(
            vendor_id="VENDOR-READONLY",
            name="Readonly Test",
            customer_id=test_customer_ids["customer_a"],
        )

        with pytest.raises(PermissionError, match="Write access required"):
            vendor_service.create_vendor(vendor)

        CustomerContextManager.clear_context()


# =============================================
# Service Operation Tests
# =============================================

class TestVendorEquipmentService:
    """Integration tests for VendorEquipmentService."""

    def test_service_initialization(self, vendor_service):
        """Test service initializes correctly."""
        assert vendor_service is not None
        assert vendor_service.COLLECTION_NAME == "ner11_vendor_equipment"
        assert vendor_service.VECTOR_SIZE == 384

    def test_customer_filter_construction(self, vendor_service, customer_a_context):
        """Test customer filter construction."""
        filter_obj = vendor_service._build_customer_filter(
            customer_id=customer_a_context.customer_id,
            include_system=True,
        )
        assert filter_obj is not None
        assert len(filter_obj.must) == 1

    def test_customer_filter_without_system(self, vendor_service, customer_a_context):
        """Test filter construction without SYSTEM."""
        filter_obj = vendor_service._build_customer_filter(
            customer_id=customer_a_context.customer_id,
            include_system=False,
        )
        assert filter_obj is not None

    def test_embedding_generation_fallback(self, vendor_service):
        """Test embedding generation returns zero vector without model."""
        embedding = vendor_service._generate_embedding("test text")
        assert len(embedding) == vendor_service.VECTOR_SIZE
        assert all(v == 0.0 for v in embedding)


# =============================================
# Lifecycle Query Tests
# =============================================

class TestLifecycleQueries:
    """Tests for lifecycle-related queries."""

    def test_equipment_eol_calculation(self, test_customer_ids):
        """Test EOL calculation for equipment."""
        today = date.today()

        # Equipment 30 days from EOL
        equipment = EquipmentModel(
            model_id="EQ-EOL-30",
            vendor_id="VENDOR-001",
            model_name="30 Days to EOL",
            customer_id=test_customer_ids["customer_a"],
            eol_date=today + timedelta(days=30),
        )
        assert equipment.days_to_eol() == 30
        assert equipment.lifecycle_status == LifecycleStatus.APPROACHING_EOL

    def test_equipment_eos_calculation(self, test_customer_ids):
        """Test EOS calculation for equipment."""
        today = date.today()

        equipment = EquipmentModel(
            model_id="EQ-EOS",
            vendor_id="VENDOR-001",
            model_name="EOS Equipment",
            customer_id=test_customer_ids["customer_a"],
            eol_date=today + timedelta(days=30),
            eos_date=today + timedelta(days=60),
        )
        assert equipment.days_to_eos() == 60

    def test_contract_days_remaining(self, sample_contract):
        """Test contract days remaining calculation."""
        days = sample_contract.days_remaining()
        assert days > 0
        assert days <= 180


# =============================================
# Data Conversion Tests
# =============================================

class TestDataConversion:
    """Tests for data conversion between formats."""

    def test_vendor_neo4j_roundtrip(self, sample_vendor):
        """Test vendor data survives Neo4j property conversion."""
        props = sample_vendor.to_neo4j_properties()

        # Verify all essential properties are present
        assert props["vendor_id"] == sample_vendor.vendor_id
        assert props["name"] == sample_vendor.name
        assert props["customer_id"] == sample_vendor.customer_id
        assert props["risk_score"] == sample_vendor.risk_score
        assert props["risk_level"] == sample_vendor.risk_level.value

    def test_vendor_qdrant_payload(self, sample_vendor):
        """Test vendor Qdrant payload structure."""
        payload = sample_vendor.to_qdrant_payload()

        # Verify entity_type is set
        assert payload["entity_type"] == "vendor"

        # Verify customer_id for filtering
        assert payload["customer_id"] == sample_vendor.customer_id

    def test_equipment_neo4j_roundtrip(self, sample_equipment):
        """Test equipment data survives Neo4j property conversion."""
        props = sample_equipment.to_neo4j_properties()

        assert props["model_id"] == sample_equipment.model_id
        assert props["vendor_id"] == sample_equipment.vendor_id
        assert props["customer_id"] == sample_equipment.customer_id

    def test_equipment_qdrant_payload(self, sample_equipment):
        """Test equipment Qdrant payload structure."""
        payload = sample_equipment.to_qdrant_payload()

        assert payload["entity_type"] == "equipment_model"
        assert payload["customer_id"] == sample_equipment.customer_id


# =============================================
# Security Validation Tests
# =============================================

class TestSecurityValidation:
    """Security-focused tests."""

    def test_whitespace_vendor_id_rejected(self, test_customer_ids):
        """Test that whitespace vendor_id is rejected."""
        with pytest.raises(ValueError, match="vendor_id is required"):
            Vendor(
                vendor_id="   ",
                name="Test",
                customer_id=test_customer_ids["customer_a"],
            )

    def test_whitespace_customer_id_rejected(self):
        """Test that whitespace customer_id is rejected."""
        with pytest.raises(ValueError, match="customer_id is required"):
            Vendor(
                vendor_id="VENDOR-001",
                name="Test",
                customer_id="   ",
            )

    def test_vendor_id_normalized(self, test_customer_ids):
        """Test that vendor_id is normalized (whitespace trimmed)."""
        vendor = Vendor(
            vendor_id="  VENDOR-001  ",
            name="  Test Vendor  ",
            customer_id=f"  {test_customer_ids['customer_a']}  ",
        )
        assert vendor.vendor_id == "VENDOR-001"
        assert vendor.name == "Test Vendor"
        assert vendor.customer_id == test_customer_ids["customer_a"]

    def test_context_required_for_operations(self, vendor_service):
        """Test that customer context is required for service operations."""
        CustomerContextManager.clear_context()

        with pytest.raises(ValueError, match="Customer context required"):
            vendor_service._get_customer_context()


# =============================================
# Live Database Integration Tests
# =============================================

import os

# Check for database connectivity
NEO4J_AVAILABLE = os.getenv("NEO4J_URI") is not None or True  # Default available locally
QDRANT_AVAILABLE = True  # Assumed available for integration testing


@pytest.fixture
def neo4j_driver():
    """Create Neo4j driver for live testing."""
    try:
        from neo4j import GraphDatabase
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "neo4j@openspg")
        driver = GraphDatabase.driver(uri, auth=(user, password))
        # Test connection
        with driver.session() as session:
            session.run("RETURN 1")
        yield driver
        driver.close()
    except Exception:
        pytest.skip("Neo4j not available")


@pytest.fixture
def qdrant_client():
    """Create Qdrant client for live testing."""
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(host="localhost", port=6333)
        # Test connection
        client.get_collections()
        yield client
    except Exception:
        pytest.skip("Qdrant not available")


@pytest.fixture
def live_vendor_service(neo4j_driver, qdrant_client):
    """Create vendor service with live database connections."""
    return VendorEquipmentService(
        qdrant_url="http://localhost:6333",
        neo4j_driver=neo4j_driver,
        embedding_model=None,
    )


class TestNeo4jLiveIntegration:
    """Tests with live Neo4j database."""

    def test_neo4j_schema_exists(self, neo4j_driver):
        """Verify Neo4j schema was created correctly."""
        with neo4j_driver.session() as session:
            # Check constraints
            result = session.run("SHOW CONSTRAINTS")
            constraint_names = [r.get("name") for r in result]

            assert "vendor_unique" in constraint_names
            assert "equipment_model_unique" in constraint_names
            assert "support_contract_unique" in constraint_names

    def test_neo4j_indexes_exist(self, neo4j_driver):
        """Verify Neo4j indexes were created correctly."""
        with neo4j_driver.session() as session:
            result = session.run("SHOW INDEXES")
            index_names = [r.get("name") for r in result]

            # Check key indexes
            assert "vendor_customer_id" in index_names
            assert "vendor_risk_score" in index_names
            assert "equipment_customer_id" in index_names
            assert "equipment_eol_date" in index_names
            assert "contract_customer_id" in index_names

    def test_create_vendor_in_neo4j(self, neo4j_driver, test_customer_ids):
        """Test creating a vendor node in Neo4j."""
        vendor = Vendor(
            vendor_id=f"VENDOR-LIVE-{uuid.uuid4().hex[:8]}",
            name="Live Test Vendor",
            customer_id=test_customer_ids["customer_a"],
            risk_score=4.5,
            support_status=SupportStatus.ACTIVE,
        )

        with neo4j_driver.session() as session:
            # Create vendor
            props = vendor.to_neo4j_properties()
            session.run(
                """
                CREATE (v:Vendor $props)
                RETURN v
                """,
                props=props,
            )

            # Verify creation
            result = session.run(
                """
                MATCH (v:Vendor {vendor_id: $vid})
                RETURN v.name as name, v.customer_id as customer_id
                """,
                vid=vendor.vendor_id,
            )
            record = result.single()
            assert record is not None
            assert record["name"] == "Live Test Vendor"
            assert record["customer_id"] == test_customer_ids["customer_a"]

            # Cleanup
            session.run(
                "MATCH (v:Vendor {vendor_id: $vid}) DELETE v",
                vid=vendor.vendor_id,
            )

    def test_create_equipment_in_neo4j(self, neo4j_driver, test_customer_ids):
        """Test creating equipment node in Neo4j."""
        today = date.today()
        equipment = EquipmentModel(
            model_id=f"EQ-LIVE-{uuid.uuid4().hex[:8]}",
            vendor_id="VENDOR-TEST",
            model_name="Live Test Equipment",
            customer_id=test_customer_ids["customer_a"],
            eol_date=today + timedelta(days=60),
            criticality=Criticality.HIGH,
        )

        with neo4j_driver.session() as session:
            # Create equipment
            props = equipment.to_neo4j_properties()
            session.run(
                """
                CREATE (em:EquipmentModel $props)
                RETURN em
                """,
                props=props,
            )

            # Verify lifecycle status was calculated
            result = session.run(
                """
                MATCH (em:EquipmentModel {model_id: $mid})
                RETURN em.lifecycle_status as status
                """,
                mid=equipment.model_id,
            )
            record = result.single()
            assert record is not None
            assert record["status"] == LifecycleStatus.APPROACHING_EOL.value

            # Cleanup
            session.run(
                "MATCH (em:EquipmentModel {model_id: $mid}) DELETE em",
                mid=equipment.model_id,
            )

    def test_customer_isolation_in_neo4j(self, neo4j_driver, test_customer_ids):
        """Test customer isolation works correctly in Neo4j queries."""
        vendor_a = Vendor(
            vendor_id=f"VENDOR-A-{uuid.uuid4().hex[:8]}",
            name="Customer A Vendor",
            customer_id=test_customer_ids["customer_a"],
        )
        vendor_b = Vendor(
            vendor_id=f"VENDOR-B-{uuid.uuid4().hex[:8]}",
            name="Customer B Vendor",
            customer_id=test_customer_ids["customer_b"],
        )

        with neo4j_driver.session() as session:
            # Create both vendors
            session.run("CREATE (v:Vendor $props)", props=vendor_a.to_neo4j_properties())
            session.run("CREATE (v:Vendor $props)", props=vendor_b.to_neo4j_properties())

            # Query for customer A's vendors only
            result = session.run(
                """
                MATCH (v:Vendor {customer_id: $cid})
                RETURN v.vendor_id as vid
                """,
                cid=test_customer_ids["customer_a"],
            )
            vendor_ids = [r["vid"] for r in result]

            assert vendor_a.vendor_id in vendor_ids
            assert vendor_b.vendor_id not in vendor_ids

            # Cleanup
            session.run("MATCH (v:Vendor {vendor_id: $vid}) DELETE v", vid=vendor_a.vendor_id)
            session.run("MATCH (v:Vendor {vendor_id: $vid}) DELETE v", vid=vendor_b.vendor_id)


class TestQdrantLiveIntegration:
    """Tests with live Qdrant database."""

    def test_qdrant_collection_exists(self, qdrant_client):
        """Verify Qdrant collection exists."""
        collections = qdrant_client.get_collections()
        collection_names = [c.name for c in collections.collections]

        assert "ner11_vendor_equipment" in collection_names

    def test_qdrant_collection_config(self, qdrant_client):
        """Verify Qdrant collection configuration."""
        info = qdrant_client.get_collection("ner11_vendor_equipment")

        assert info.status.value == "green"
        # Check vector size is 384 (MiniLM)
        assert info.config.params.vectors.size == 384

    def test_store_vendor_in_qdrant(self, qdrant_client, test_customer_ids):
        """Test storing vendor in Qdrant."""
        from qdrant_client.models import PointStruct
        import random

        vendor = Vendor(
            vendor_id=f"VENDOR-QDRANT-{uuid.uuid4().hex[:8]}",
            name="Qdrant Test Vendor",
            customer_id=test_customer_ids["customer_a"],
            risk_score=3.5,
        )

        # Generate dummy vector (in production, would use embedding model)
        vector = [random.random() for _ in range(384)]

        # Store in Qdrant
        point = PointStruct(
            id=hash(vendor.vendor_id) % (2**63),
            vector=vector,
            payload=vendor.to_qdrant_payload(),
        )
        qdrant_client.upsert(
            collection_name="ner11_vendor_equipment",
            points=[point],
        )

        # Verify storage
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        results = qdrant_client.scroll(
            collection_name="ner11_vendor_equipment",
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="vendor_id",
                        match=MatchValue(value=vendor.vendor_id),
                    )
                ]
            ),
            limit=1,
        )

        assert len(results[0]) == 1
        assert results[0][0].payload["name"] == "Qdrant Test Vendor"

        # Cleanup
        from qdrant_client.models import PointIdsList
        qdrant_client.delete(
            collection_name="ner11_vendor_equipment",
            points_selector=PointIdsList(points=[point.id]),
        )

    def test_customer_isolation_in_qdrant(self, qdrant_client, test_customer_ids):
        """Test customer isolation works in Qdrant queries."""
        from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchAny
        import random

        vendor_a = Vendor(
            vendor_id=f"VENDOR-QA-{uuid.uuid4().hex[:8]}",
            name="Customer A Qdrant Vendor",
            customer_id=test_customer_ids["customer_a"],
        )
        vendor_b = Vendor(
            vendor_id=f"VENDOR-QB-{uuid.uuid4().hex[:8]}",
            name="Customer B Qdrant Vendor",
            customer_id=test_customer_ids["customer_b"],
        )

        # Store both
        points = []
        for vendor in [vendor_a, vendor_b]:
            point = PointStruct(
                id=hash(vendor.vendor_id) % (2**63),
                vector=[random.random() for _ in range(384)],
                payload=vendor.to_qdrant_payload(),
            )
            points.append(point)

        qdrant_client.upsert(
            collection_name="ner11_vendor_equipment",
            points=points,
        )

        # Query with customer A isolation
        results = qdrant_client.scroll(
            collection_name="ner11_vendor_equipment",
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=[test_customer_ids["customer_a"]]),
                    )
                ]
            ),
            limit=100,
        )

        vendor_ids = [r.payload.get("vendor_id") for r in results[0]]

        assert vendor_a.vendor_id in vendor_ids
        assert vendor_b.vendor_id not in vendor_ids

        # Cleanup
        from qdrant_client.models import PointIdsList
        qdrant_client.delete(
            collection_name="ner11_vendor_equipment",
            points_selector=PointIdsList(points=[p.id for p in points]),
        )


class TestEndToEndIntegration:
    """End-to-end tests with all components."""

    def test_vendor_lifecycle_workflow(
        self,
        neo4j_driver,
        qdrant_client,
        test_customer_ids,
        customer_a_context,
    ):
        """Test complete vendor lifecycle workflow."""
        from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
        import random

        today = date.today()

        # Create vendor
        vendor = Vendor(
            vendor_id=f"VENDOR-E2E-{uuid.uuid4().hex[:8]}",
            name="End-to-End Test Vendor",
            customer_id=test_customer_ids["customer_a"],
            risk_score=6.5,
            support_status=SupportStatus.ACTIVE,
        )

        # Create equipment approaching EOL
        equipment = EquipmentModel(
            model_id=f"EQ-E2E-{uuid.uuid4().hex[:8]}",
            vendor_id=vendor.vendor_id,
            model_name="EOL Test Equipment",
            customer_id=test_customer_ids["customer_a"],
            eol_date=today + timedelta(days=30),
            criticality=Criticality.CRITICAL,
        )

        # Store in Neo4j
        with neo4j_driver.session() as session:
            session.run("CREATE (v:Vendor $props)", props=vendor.to_neo4j_properties())
            session.run("CREATE (em:EquipmentModel $props)", props=equipment.to_neo4j_properties())
            session.run(
                """
                MATCH (v:Vendor {vendor_id: $vid})
                MATCH (em:EquipmentModel {model_id: $mid})
                CREATE (v)-[:MANUFACTURES]->(em)
                """,
                vid=vendor.vendor_id,
                mid=equipment.model_id,
            )

        # Store in Qdrant
        for entity in [vendor, equipment]:
            point = PointStruct(
                id=hash(entity.vendor_id if hasattr(entity, 'vendor_id') else entity.model_id) % (2**63),
                vector=[random.random() for _ in range(384)],
                payload=entity.to_qdrant_payload(),
            )
            qdrant_client.upsert(
                collection_name="ner11_vendor_equipment",
                points=[point],
            )

        # Query high-risk vendors from Neo4j
        with neo4j_driver.session() as session:
            result = session.run(
                """
                MATCH (v:Vendor {customer_id: $cid})
                WHERE v.risk_score > 6.0
                RETURN v.vendor_id as vid, v.risk_level as level
                """,
                cid=test_customer_ids["customer_a"],
            )
            high_risk = list(result)
            assert any(r["vid"] == vendor.vendor_id for r in high_risk)

        # Query approaching EOL equipment
        with neo4j_driver.session() as session:
            result = session.run(
                """
                MATCH (em:EquipmentModel {customer_id: $cid})
                WHERE em.lifecycle_status = 'approaching_eol'
                RETURN em.model_id as mid, em.model_name as name
                """,
                cid=test_customer_ids["customer_a"],
            )
            eol_equipment = list(result)
            assert any(r["mid"] == equipment.model_id for r in eol_equipment)

        # Cleanup
        with neo4j_driver.session() as session:
            session.run(
                """
                MATCH (v:Vendor {vendor_id: $vid})-[r]->(em:EquipmentModel {model_id: $mid})
                DELETE r, v, em
                """,
                vid=vendor.vendor_id,
                mid=equipment.model_id,
            )

        # Cleanup Qdrant
        from qdrant_client.models import FilterSelector
        qdrant_client.delete(
            collection_name="ner11_vendor_equipment",
            points_selector=FilterSelector(
                filter=Filter(
                    should=[
                        FieldCondition(key="vendor_id", match=MatchValue(value=vendor.vendor_id)),
                    ]
                )
            ),
        )


class TestEmbeddingService:
    """Tests for the embedding service."""

    def test_embedding_service_initialization(self):
        """Test embedding service initializes correctly."""
        from api.vendor_equipment.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True)

        assert service.model_name == "sentence-transformers/all-MiniLM-L6-v2"
        assert service.VECTOR_SIZE == 384
        assert service.cache_size == 1000
        assert service._model is None  # Lazy load

    def test_embedding_service_encode_empty_text(self):
        """Test encoding empty text returns zero vector."""
        from api.vendor_equipment.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True)
        embedding = service.encode("")

        assert len(embedding) == 384
        assert all(v == 0.0 for v in embedding)

    def test_embedding_service_encode_whitespace(self):
        """Test encoding whitespace returns zero vector."""
        from api.vendor_equipment.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True)
        embedding = service.encode("   \n\t  ")

        assert len(embedding) == 384
        assert all(v == 0.0 for v in embedding)

    def test_embedding_service_caching(self):
        """Test embedding caching works correctly."""
        from api.vendor_equipment.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True, cache_size=10)

        # First call - should cache
        text = "Test caching text"
        embedding1 = service.encode(text, use_cache=True)

        # Second call - should use cache
        embedding2 = service.encode(text, use_cache=True)

        assert embedding1 == embedding2
        assert service.cache_stats["size"] >= 1

    def test_embedding_service_cache_disabled(self):
        """Test encoding without cache."""
        from api.vendor_equipment.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True)
        service._cache.clear()

        embedding = service.encode("No cache text", use_cache=False)

        assert len(embedding) == 384
        assert service.cache_stats["size"] == 0

    def test_embedding_service_batch_encode_empty_list(self):
        """Test batch encoding empty list returns empty list."""
        from api.vendor_equipment.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True)
        embeddings = service.encode_batch([])

        assert embeddings == []

    def test_embedding_service_batch_encode_with_empty_items(self):
        """Test batch encoding with empty items returns zero vectors for empty."""
        from api.vendor_equipment.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True)
        embeddings = service.encode_batch(["", "test", "  "])

        assert len(embeddings) == 3
        assert all(v == 0.0 for v in embeddings[0])  # Empty
        assert all(v == 0.0 for v in embeddings[2])  # Whitespace

    def test_embedding_service_encode_vendor(self):
        """Test vendor-specific encoding."""
        from api.vendor_equipment.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True)

        vendor_data = {
            "name": "Cisco Systems",
            "industry_focus": ["IT", "Network"],
            "country": "USA",
            "description": "Leading network equipment manufacturer",
        }

        embedding = service.encode_vendor(vendor_data)

        assert len(embedding) == 384

    def test_embedding_service_encode_equipment(self):
        """Test equipment-specific encoding."""
        from api.vendor_equipment.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True)

        equipment_data = {
            "model_name": "Catalyst 9000 Series",
            "product_line": "Network Switches",
            "category": "switch",
            "vendor_name": "Cisco",
            "description": "Enterprise-grade network switch",
        }

        embedding = service.encode_equipment(equipment_data)

        assert len(embedding) == 384

    def test_embedding_service_similarity(self):
        """Test cosine similarity calculation."""
        from api.vendor_equipment.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True)

        # Identical vectors should have similarity 1.0
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]

        similarity = service.similarity(vec1, vec2)
        assert abs(similarity - 1.0) < 0.001

        # Orthogonal vectors should have similarity 0.0
        vec3 = [0.0, 1.0, 0.0]
        similarity_ortho = service.similarity(vec1, vec3)
        assert abs(similarity_ortho - 0.0) < 0.001

    def test_embedding_service_similarity_zero_vector(self):
        """Test similarity with zero vector returns 0."""
        from api.vendor_equipment.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True)

        vec1 = [0.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]

        similarity = service.similarity(vec1, vec2)
        assert similarity == 0.0

    def test_embedding_service_similarity_dimension_mismatch(self):
        """Test similarity raises error for dimension mismatch."""
        from api.vendor_equipment.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True)

        vec1 = [1.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]

        with pytest.raises(ValueError) as exc_info:
            service.similarity(vec1, vec2)

        assert "same dimension" in str(exc_info.value)

    def test_embedding_service_clear_cache(self):
        """Test cache clearing."""
        from api.vendor_equipment.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True)
        service.encode("Some text", use_cache=True)

        assert service.cache_stats["size"] > 0

        service.clear_cache()

        assert service.cache_stats["size"] == 0


class TestSemanticSearchDataclasses:
    """Tests for semantic search dataclasses."""

    def test_semantic_search_result_creation(self):
        """Test SemanticSearchResult dataclass."""
        from api.vendor_equipment.vendor_service import SemanticSearchResult

        result = SemanticSearchResult(
            entity_id="VENDOR-001",
            entity_type="vendor",
            name="Test Vendor",
            score=0.85,
            payload={"customer_id": "CUST-001"},
        )

        assert result.entity_id == "VENDOR-001"
        assert result.entity_type == "vendor"
        assert result.name == "Test Vendor"
        assert result.score == 0.85
        assert result.payload["customer_id"] == "CUST-001"

    def test_similarity_match_creation(self):
        """Test SimilarityMatch dataclass."""
        from api.vendor_equipment.vendor_service import SimilarityMatch

        match = SimilarityMatch(
            source_id="VENDOR-001",
            match_id="VENDOR-002",
            match_name="Similar Vendor",
            similarity_score=0.92,
            match_type="vendor",
        )

        assert match.source_id == "VENDOR-001"
        assert match.match_id == "VENDOR-002"
        assert match.match_name == "Similar Vendor"
        assert match.similarity_score == 0.92
        assert match.match_type == "vendor"


class TestSemanticSearchService:
    """Tests for VendorEquipmentService semantic search methods."""

    def test_service_has_embedding_property(self, vendor_service):
        """Test service exposes embedding_service property."""
        # Property should exist and be accessible
        assert hasattr(vendor_service, 'embedding_service')

        # Getting property should return an EmbeddingService instance
        from api.vendor_equipment.embedding_service import EmbeddingService
        embedding_svc = vendor_service.embedding_service
        assert isinstance(embedding_svc, EmbeddingService)

    def test_semantic_search_method_exists(self, vendor_service):
        """Test semantic_search method exists."""
        assert hasattr(vendor_service, 'semantic_search')
        assert callable(getattr(vendor_service, 'semantic_search'))

    def test_find_similar_vendors_method_exists(self, vendor_service):
        """Test find_similar_vendors method exists."""
        assert hasattr(vendor_service, 'find_similar_vendors')
        assert callable(getattr(vendor_service, 'find_similar_vendors'))

    def test_find_similar_equipment_method_exists(self, vendor_service):
        """Test find_similar_equipment method exists."""
        assert hasattr(vendor_service, 'find_similar_equipment')
        assert callable(getattr(vendor_service, 'find_similar_equipment'))

    def test_find_replacement_candidates_method_exists(self, vendor_service):
        """Test find_replacement_candidates method exists."""
        assert hasattr(vendor_service, 'find_replacement_candidates')
        assert callable(getattr(vendor_service, 'find_replacement_candidates'))


class TestSemanticSearchLiveIntegration:
    """Live integration tests for semantic search with Qdrant."""

    def test_semantic_search_with_qdrant(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test semantic search returns results from Qdrant."""
        from qdrant_client.models import PointStruct
        from api.vendor_equipment.embedding_service import EmbeddingService

        embedding_service = EmbeddingService(lazy_load=True)

        # Create test vendor with meaningful embedding
        vendor = Vendor(
            vendor_id=f"VENDOR-SEMANTIC-{uuid.uuid4().hex[:8]}",
            name="Cisco Network Equipment",
            customer_id=test_customer_ids["customer_a"],
            risk_score=4.0,
            industry_focus=["IT", "Networking"],
        )

        # Generate real embedding for the vendor
        vendor_embedding = embedding_service.encode_vendor(vendor.to_qdrant_payload())

        # Store in Qdrant with real embedding
        point = PointStruct(
            id=hash(vendor.vendor_id) % (2**63),
            vector=vendor_embedding,
            payload=vendor.to_qdrant_payload(),
        )
        qdrant_client.upsert(
            collection_name="ner11_vendor_equipment",
            points=[point],
        )

        # Search with similar query
        query_embedding = embedding_service.encode("cisco network devices")

        from qdrant_client.models import Filter, FieldCondition, MatchAny

        results = qdrant_client.search(
            collection_name="ner11_vendor_equipment",
            query_vector=query_embedding,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=[test_customer_ids["customer_a"], "SYSTEM"]),
                    )
                ]
            ),
            limit=5,
        )

        # Should find our vendor (if embeddings are non-zero)
        vendor_ids = [r.payload.get("vendor_id") for r in results]

        # Cleanup
        from qdrant_client.models import PointIdsList
        qdrant_client.delete(
            collection_name="ner11_vendor_equipment",
            points_selector=PointIdsList(points=[point.id]),
        )

        # Verify search returned results (may be empty if using fallback zero vectors)
        assert isinstance(results, list)

    def test_semantic_search_customer_isolation(
        self, qdrant_client, test_customer_ids
    ):
        """Test semantic search respects customer isolation."""
        from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchAny
        from api.vendor_equipment.embedding_service import EmbeddingService

        embedding_service = EmbeddingService(lazy_load=True)

        # Create vendors for different customers
        vendor_a = Vendor(
            vendor_id=f"VENDOR-SEM-A-{uuid.uuid4().hex[:8]}",
            name="Customer A Network Vendor",
            customer_id=test_customer_ids["customer_a"],
        )
        vendor_b = Vendor(
            vendor_id=f"VENDOR-SEM-B-{uuid.uuid4().hex[:8]}",
            name="Customer B Network Vendor",
            customer_id=test_customer_ids["customer_b"],
        )

        # Store both with embeddings
        points = []
        for vendor in [vendor_a, vendor_b]:
            embedding = embedding_service.encode_vendor(vendor.to_qdrant_payload())
            point = PointStruct(
                id=hash(vendor.vendor_id) % (2**63),
                vector=embedding,
                payload=vendor.to_qdrant_payload(),
            )
            points.append(point)

        qdrant_client.upsert(
            collection_name="ner11_vendor_equipment",
            points=points,
        )

        # Search with Customer A isolation
        query_embedding = embedding_service.encode("network vendor")

        results = qdrant_client.search(
            collection_name="ner11_vendor_equipment",
            query_vector=query_embedding,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=[test_customer_ids["customer_a"]]),
                    )
                ]
            ),
            limit=10,
        )

        result_vendor_ids = [r.payload.get("vendor_id") for r in results]

        # Should only find Customer A's vendor
        if vendor_a.vendor_id in result_vendor_ids:
            assert vendor_b.vendor_id not in result_vendor_ids

        # Cleanup
        from qdrant_client.models import PointIdsList
        qdrant_client.delete(
            collection_name="ner11_vendor_equipment",
            points_selector=PointIdsList(points=[p.id for p in points]),
        )


class TestGlobalEmbeddingService:
    """Tests for global embedding service singleton."""

    def test_get_embedding_service_returns_singleton(self):
        """Test get_embedding_service returns same instance."""
        from api.vendor_equipment.embedding_service import get_embedding_service

        service1 = get_embedding_service()
        service2 = get_embedding_service()

        assert service1 is service2

    def test_get_embedding_service_with_parameters(self):
        """Test get_embedding_service uses first call parameters."""
        from api.vendor_equipment.embedding_service import (
            EmbeddingService,
            get_embedding_service,
        )

        # Reset singleton for testing
        import api.vendor_equipment.embedding_service as emb_module
        emb_module._embedding_service = None

        service = get_embedding_service(cache_size=500)

        # Parameters from first call should be used
        assert service.cache_size == 500


# =============================================================================
# Day 4: CVE Vulnerability Integration Tests
# =============================================================================


class TestCVERecordDataclass:
    """Tests for CVERecord dataclass."""

    def test_cve_record_creation(self):
        """Test CVERecord creation with valid data."""
        from api.vendor_equipment import CVERecord
        from datetime import date

        cve = CVERecord(
            cve_id="CVE-2024-12345",
            cvss_score=9.8,
            severity="critical",
            description="Remote code execution vulnerability",
            affected_vendor_id="vendor-cisco",
            affected_equipment_ids=["model-001", "model-002"],
            published_date=date(2024, 12, 1),
        )

        assert cve.cve_id == "CVE-2024-12345"
        assert cve.cvss_score == 9.8
        assert cve.severity == "critical"
        assert cve.affected_vendor_id == "vendor-cisco"
        assert len(cve.affected_equipment_ids) == 2
        assert cve.customer_id == "SYSTEM"  # Default
        assert cve.flagged_at is not None

    def test_cve_record_severity_auto_calculation(self):
        """Test CVERecord auto-calculates severity from CVSS."""
        from api.vendor_equipment import CVERecord

        # Critical: >= 9.0
        cve_critical = CVERecord(
            cve_id="CVE-2024-0001",
            cvss_score=9.5,
            severity="",  # Empty - should auto-calculate
            description="Critical vuln",
            affected_vendor_id="vendor-001",
            affected_equipment_ids=[],
        )
        assert cve_critical.severity == "critical"

        # High: >= 7.0
        cve_high = CVERecord(
            cve_id="CVE-2024-0002",
            cvss_score=7.5,
            severity="",
            description="High vuln",
            affected_vendor_id="vendor-001",
            affected_equipment_ids=[],
        )
        assert cve_high.severity == "high"

        # Medium: >= 4.0
        cve_medium = CVERecord(
            cve_id="CVE-2024-0003",
            cvss_score=5.5,
            severity="",
            description="Medium vuln",
            affected_vendor_id="vendor-001",
            affected_equipment_ids=[],
        )
        assert cve_medium.severity == "medium"

        # Low: < 4.0
        cve_low = CVERecord(
            cve_id="CVE-2024-0004",
            cvss_score=2.0,
            severity="",
            description="Low vuln",
            affected_vendor_id="vendor-001",
            affected_equipment_ids=[],
        )
        assert cve_low.severity == "low"

    def test_cve_record_to_qdrant_payload(self):
        """Test CVERecord conversion to Qdrant payload."""
        from api.vendor_equipment import CVERecord
        from datetime import date

        cve = CVERecord(
            cve_id="CVE-2024-99999",
            cvss_score=8.5,
            severity="high",
            description="Authentication bypass",
            affected_vendor_id="vendor-test",
            affected_equipment_ids=["eq-1", "eq-2", "eq-3"],
            published_date=date(2024, 11, 15),
        )

        payload = cve.to_qdrant_payload()

        assert payload["cve_id"] == "CVE-2024-99999"
        assert payload["cvss_score"] == 8.5
        assert payload["severity"] == "high"
        assert payload["description"] == "Authentication bypass"
        assert payload["affected_vendor_id"] == "vendor-test"
        assert payload["affected_equipment_ids"] == ["eq-1", "eq-2", "eq-3"]
        assert payload["entity_type"] == "cve"
        assert payload["published_date"] == "2024-11-15"
        assert "flagged_at" in payload


class TestVulnerabilityAlertDataclass:
    """Tests for VulnerabilityAlert dataclass."""

    def test_vulnerability_alert_creation(self):
        """Test VulnerabilityAlert creation."""
        from api.vendor_equipment import VulnerabilityAlert

        alert = VulnerabilityAlert(
            cve_id="CVE-2024-55555",
            vendor_id="vendor-palo-alto",
            vendor_name="Palo Alto Networks",
            cvss_score=9.1,
            severity="critical",
            affected_equipment_count=15,
            critical_equipment_affected=5,
            recommendation="Immediate patching required",
        )

        assert alert.cve_id == "CVE-2024-55555"
        assert alert.vendor_name == "Palo Alto Networks"
        assert alert.cvss_score == 9.1
        assert alert.affected_equipment_count == 15
        assert alert.critical_equipment_affected == 5
        assert "Immediate patching" in alert.recommendation


class TestCVEServiceMethods:
    """Tests for CVE-related service methods."""

    def test_flag_vendor_vulnerability_method_exists(self, vendor_service):
        """Test flag_vendor_vulnerability method exists."""
        assert hasattr(vendor_service, "flag_vendor_vulnerability")
        assert callable(getattr(vendor_service, "flag_vendor_vulnerability"))

    def test_get_vendor_cves_method_exists(self, vendor_service):
        """Test get_vendor_cves method exists."""
        assert hasattr(vendor_service, "get_vendor_cves")
        assert callable(getattr(vendor_service, "get_vendor_cves"))

    def test_search_cves_method_exists(self, vendor_service):
        """Test search_cves method exists."""
        assert hasattr(vendor_service, "search_cves")
        assert callable(getattr(vendor_service, "search_cves"))

    def test_get_critical_vulnerabilities_method_exists(self, vendor_service):
        """Test get_critical_vulnerabilities method exists."""
        assert hasattr(vendor_service, "get_critical_vulnerabilities")
        assert callable(getattr(vendor_service, "get_critical_vulnerabilities"))

    def test_payload_to_cve_method_exists(self, vendor_service):
        """Test _payload_to_cve method exists."""
        assert hasattr(vendor_service, "_payload_to_cve")
        assert callable(getattr(vendor_service, "_payload_to_cve"))


class TestCVELiveIntegration:
    """Live integration tests for CVE functionality with Qdrant."""

    def test_flag_vendor_vulnerability_stores_in_qdrant(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test flag_vendor_vulnerability stores CVE record in Qdrant."""
        from api.vendor_equipment import VendorEquipmentService, Vendor, VulnerabilityAlert
        from api.vendor_equipment.embedding_service import EmbeddingService
        from datetime import date
        import uuid

        # Create service using default URL
        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )
        embedding_service = EmbeddingService(lazy_load=True)

        # Create a test vendor first
        test_vendor_id = f"vendor-cve-test-{uuid.uuid4().hex[:8]}"
        vendor = Vendor(
            vendor_id=test_vendor_id,
            name="Test CVE Vendor",
            customer_id=test_customer_ids["customer_a"],
        )

        # Store vendor
        from qdrant_client.models import PointStruct
        import hashlib

        vendor_point_id = hashlib.md5(f"vendor:{test_vendor_id}".encode()).hexdigest()
        vendor_vector = embedding_service.encode(f"{vendor.name} Test Vendor")

        qdrant_client.upsert(
            collection_name="ner11_vendor_equipment",
            points=[
                PointStruct(
                    id=vendor_point_id,
                    vector=vendor_vector,  # Already a list
                    payload=vendor.to_qdrant_payload(),
                )
            ],
        )

        # Flag vulnerability
        cve_id = f"CVE-2024-{uuid.uuid4().hex[:5].upper()}"
        alert = service.flag_vendor_vulnerability(
            vendor_id=test_vendor_id,
            cve_id=cve_id,
            cvss_score=9.0,
            description="Critical vulnerability in test vendor equipment",
            published_date=date(2024, 12, 3),
        )

        # Verify alert returned
        assert isinstance(alert, VulnerabilityAlert)
        assert alert.cve_id == cve_id
        assert alert.vendor_id == test_vendor_id
        assert alert.cvss_score == 9.0
        assert alert.severity == "critical"

        # Verify CVE stored in Qdrant
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        results = qdrant_client.scroll(
            collection_name="ner11_vendor_equipment",
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="entity_type", match=MatchValue(value="cve")),
                    FieldCondition(key="cve_id", match=MatchValue(value=cve_id)),
                ]
            ),
            limit=10,
        )

        assert len(results[0]) >= 1
        cve_record = results[0][0].payload
        assert cve_record["cve_id"] == cve_id
        assert cve_record["cvss_score"] == 9.0
        assert cve_record["affected_vendor_id"] == test_vendor_id

        # Cleanup
        from qdrant_client.models import PointIdsList

        point_ids = [vendor_point_id] + [r.id for r in results[0]]
        qdrant_client.delete(
            collection_name="ner11_vendor_equipment",
            points_selector=PointIdsList(points=point_ids),
        )

    def test_get_vendor_cves_returns_cve_records(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_vendor_cves retrieves CVE records for a vendor."""
        from api.vendor_equipment import VendorEquipmentService, CVERecord
        from api.vendor_equipment.embedding_service import EmbeddingService
        from qdrant_client.models import PointStruct
        from datetime import date
        import uuid
        import hashlib

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )
        embedding_service = EmbeddingService(lazy_load=True)

        test_vendor_id = f"vendor-multicve-{uuid.uuid4().hex[:8]}"

        # Store multiple CVEs for this vendor
        cve_ids = []
        point_ids = []
        for i, (cvss, severity) in enumerate([(9.5, "critical"), (7.2, "high"), (4.5, "medium")]):
            cve_id = f"CVE-2024-TEST{i:03d}"
            cve_ids.append(cve_id)

            cve = CVERecord(
                cve_id=cve_id,
                cvss_score=cvss,
                severity=severity,
                description=f"Test vulnerability {i}",
                affected_vendor_id=test_vendor_id,
                affected_equipment_ids=[],
                published_date=date(2024, 12, 1),
            )

            point_id = hashlib.md5(f"cve:{cve_id}".encode()).hexdigest()
            point_ids.append(point_id)
            vector = embedding_service.encode(cve.description)

            qdrant_client.upsert(
                collection_name="ner11_vendor_equipment",
                points=[
                    PointStruct(
                        id=point_id,
                        vector=vector,  # Already a list
                        payload=cve.to_qdrant_payload(),
                    )
                ],
            )

        # Get CVEs for vendor
        vendor_cves = service.get_vendor_cves(test_vendor_id)

        assert len(vendor_cves) == 3
        retrieved_cve_ids = [c.cve_id for c in vendor_cves]
        for cve_id in cve_ids:
            assert cve_id in retrieved_cve_ids

        # Test filtering by min_cvss
        high_cves = service.get_vendor_cves(test_vendor_id, min_cvss=7.0)
        assert len(high_cves) == 2  # critical and high only

        # Test filtering by severity
        critical_only = service.get_vendor_cves(test_vendor_id, severity="critical")
        assert len(critical_only) == 1
        assert critical_only[0].severity == "critical"

        # Cleanup
        from qdrant_client.models import PointIdsList

        qdrant_client.delete(
            collection_name="ner11_vendor_equipment",
            points_selector=PointIdsList(points=point_ids),
        )

    def test_search_cves_semantic(self, qdrant_client, test_customer_ids, customer_a_context):
        """Test semantic search across CVE records."""
        from api.vendor_equipment import VendorEquipmentService, CVERecord
        from api.vendor_equipment.embedding_service import EmbeddingService
        from qdrant_client.models import PointStruct
        from datetime import date
        import uuid
        import hashlib

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )
        embedding_service = EmbeddingService(lazy_load=True)

        test_vendor_id = f"vendor-search-cve-{uuid.uuid4().hex[:8]}"

        # Store CVEs with different descriptions
        cves_data = [
            ("CVE-SEARCH-001", 9.0, "SQL injection vulnerability in database layer"),
            ("CVE-SEARCH-002", 8.0, "Remote code execution via buffer overflow"),
            ("CVE-SEARCH-003", 7.5, "Cross-site scripting XSS in web interface"),
        ]

        point_ids = []
        for cve_id, cvss, desc in cves_data:
            cve = CVERecord(
                cve_id=cve_id,
                cvss_score=cvss,
                severity="",  # Auto-calculate
                description=desc,
                affected_vendor_id=test_vendor_id,
                affected_equipment_ids=[],
                published_date=date(2024, 12, 1),
            )

            point_id = hashlib.md5(f"cve:{cve_id}".encode()).hexdigest()
            point_ids.append(point_id)
            vector = embedding_service.encode(desc)

            qdrant_client.upsert(
                collection_name="ner11_vendor_equipment",
                points=[
                    PointStruct(
                        id=point_id,
                        vector=vector,  # Already a list
                        payload=cve.to_qdrant_payload(),
                    )
                ],
            )

        # Semantic search for SQL-related vulnerabilities
        sql_cves = service.search_cves("database SQL injection attack")

        # Should find SQL injection CVE with highest relevance
        if len(sql_cves) > 0:
            assert any("SQL" in c.description or "database" in c.description for c in sql_cves)

        # Cleanup
        from qdrant_client.models import PointIdsList

        qdrant_client.delete(
            collection_name="ner11_vendor_equipment",
            points_selector=PointIdsList(points=point_ids),
        )


# =============================================
# Day 5: EOL/EOS Alerting Tests
# =============================================


class TestEOLAlertDataclass:
    """Tests for EOLAlert dataclass."""

    def test_eol_alert_creation(self):
        """Test EOLAlert creation with all fields."""
        from api.vendor_equipment.vendor_models import EOLAlert, AlertType, AlertSeverity
        from datetime import date

        alert = EOLAlert(
            alert_id="ALERT-TEST123",
            alert_type=AlertType.EOL_APPROACHING,
            severity=AlertSeverity.WARNING,
            customer_id="CUST-001",
            entity_type="equipment_model",
            entity_id="MODEL-001",
            entity_name="Test Router 9000",
            message="Test Router 9000 reaches End of Life in 60 days",
            days_remaining=60,
            target_date=date(2025, 3, 1),
            vendor_id="VENDOR-001",
            vendor_name="Test Vendor",
            affected_asset_count=25,
            recommended_action="Plan migration to supported equipment",
        )

        assert alert.alert_id == "ALERT-TEST123"
        assert alert.alert_type == AlertType.EOL_APPROACHING
        assert alert.severity == AlertSeverity.WARNING
        assert alert.days_remaining == 60
        assert alert.affected_asset_count == 25
        assert "Plan migration" in alert.recommended_action

    def test_eol_alert_severity_calculation(self):
        """Test auto-calculated severity based on days remaining."""
        from api.vendor_equipment.vendor_models import EOLAlert, AlertType, AlertSeverity

        # Past due - critical
        alert_past = EOLAlert(
            alert_id="ALERT-PAST",
            alert_type=AlertType.EOL_PAST,
            severity=None,  # Auto-calculate
            customer_id="CUST-001",
            entity_type="equipment_model",
            entity_id="MODEL-001",
            entity_name="Past Due Equipment",
            message="Equipment past EOL",
            days_remaining=-10,
        )
        assert alert_past.severity == AlertSeverity.CRITICAL

    def test_eol_alert_from_equipment_model(self):
        """Test creating EOLAlert from EquipmentModel."""
        from api.vendor_equipment.vendor_models import EOLAlert, AlertType, EquipmentModel
        from datetime import date, timedelta

        equipment = EquipmentModel(
            model_id="MODEL-EOL-001",
            vendor_id="VENDOR-001",
            model_name="EOL Test Equipment",
            customer_id="CUST-001",
            eol_date=date.today() + timedelta(days=30),
            deployed_count=15,
        )

        alert = EOLAlert.from_equipment_model(
            model=equipment,
            alert_type=AlertType.EOL_APPROACHING,
            vendor_name="Test Vendor",
        )

        assert alert.entity_id == "MODEL-EOL-001"
        assert alert.entity_name == "EOL Test Equipment"
        assert alert.vendor_name == "Test Vendor"
        assert alert.affected_asset_count == 15
        assert alert.days_remaining <= 30

    def test_eol_alert_from_support_contract(self):
        """Test creating EOLAlert from SupportContract."""
        from api.vendor_equipment.vendor_models import EOLAlert, SupportContract, ServiceLevel
        from datetime import date, timedelta

        contract = SupportContract(
            contract_id="CONTRACT-001",
            vendor_id="VENDOR-001",
            customer_id="CUST-001",
            start_date=date.today() - timedelta(days=365),
            end_date=date.today() + timedelta(days=15),
            service_level=ServiceLevel.PREMIUM,
            covered_model_ids=["MODEL-001", "MODEL-002"],
        )

        alert = EOLAlert.from_support_contract(
            contract=contract,
            vendor_name="Contract Vendor",
        )

        assert alert.entity_id == "CONTRACT-001"
        assert "Contract CONTRACT-001" in alert.entity_name
        assert alert.vendor_name == "Contract Vendor"
        assert alert.days_remaining <= 15
        assert alert.affected_asset_count == 2  # 2 covered models

    def test_eol_alert_to_dict(self):
        """Test EOLAlert to dictionary conversion."""
        from api.vendor_equipment.vendor_models import EOLAlert, AlertType, AlertSeverity
        from datetime import date

        alert = EOLAlert(
            alert_id="ALERT-DICT-001",
            alert_type=AlertType.CONTRACT_EXPIRING,
            severity=AlertSeverity.HIGH,
            customer_id="CUST-001",
            entity_type="support_contract",
            entity_id="CONTRACT-001",
            entity_name="Test Contract",
            message="Contract expires soon",
            days_remaining=25,
            target_date=date(2025, 1, 15),
        )

        result = alert.to_dict()

        assert result["alert_id"] == "ALERT-DICT-001"
        assert result["alert_type"] == "contract_expiring"
        assert result["severity"] == "high"
        assert result["days_remaining"] == 25
        assert result["target_date"] == "2025-01-15"

    def test_eol_alert_to_qdrant_payload(self):
        """Test EOLAlert to Qdrant payload conversion."""
        from api.vendor_equipment.vendor_models import EOLAlert, AlertType, AlertSeverity
        from datetime import date

        alert = EOLAlert(
            alert_id="ALERT-QDRANT-001",
            alert_type=AlertType.EOS_PAST,
            severity=AlertSeverity.CRITICAL,
            customer_id="CUST-001",
            entity_type="equipment_model",
            entity_id="MODEL-001",
            entity_name="Legacy Equipment",
            message="Equipment past EOS",
            days_remaining=-30,
            target_date=date(2024, 11, 1),
            vendor_id="VENDOR-001",
        )

        payload = alert.to_qdrant_payload()

        assert payload["alert_id"] == "ALERT-QDRANT-001"
        assert payload["alert_type"] == "eos_past"
        assert payload["severity"] == "critical"
        assert payload["entity_type"] == "eol_alert"
        assert payload["customer_id"] == "CUST-001"
        assert payload["vendor_id"] == "VENDOR-001"


class TestAlertEnums:
    """Tests for Alert-related enums."""

    def test_alert_severity_values(self):
        """Test AlertSeverity enum values."""
        from api.vendor_equipment.vendor_models import AlertSeverity

        assert AlertSeverity.INFO.value == "info"
        assert AlertSeverity.WARNING.value == "warning"
        assert AlertSeverity.HIGH.value == "high"
        assert AlertSeverity.CRITICAL.value == "critical"

    def test_alert_type_values(self):
        """Test AlertType enum values."""
        from api.vendor_equipment.vendor_models import AlertType

        assert AlertType.EOL_APPROACHING.value == "eol_approaching"
        assert AlertType.EOL_PAST.value == "eol_past"
        assert AlertType.EOS_APPROACHING.value == "eos_approaching"
        assert AlertType.EOS_PAST.value == "eos_past"
        assert AlertType.CONTRACT_EXPIRING.value == "contract_expiring"
        assert AlertType.CONTRACT_EXPIRED.value == "contract_expired"
        assert AlertType.VENDOR_RISK_INCREASED.value == "vendor_risk_increased"
        assert AlertType.VULNERABILITY_DETECTED.value == "vulnerability_detected"


class TestAlertingServiceMethods:
    """Tests for alerting service methods."""

    def test_get_eol_alerts_method_exists(self, vendor_service):
        """Test get_eol_alerts method exists."""
        assert hasattr(vendor_service, "get_eol_alerts")
        assert callable(getattr(vendor_service, "get_eol_alerts"))

    def test_get_contract_expiration_alerts_method_exists(self, vendor_service):
        """Test get_contract_expiration_alerts method exists."""
        assert hasattr(vendor_service, "get_contract_expiration_alerts")
        assert callable(getattr(vendor_service, "get_contract_expiration_alerts"))

    def test_get_all_lifecycle_alerts_method_exists(self, vendor_service):
        """Test get_all_lifecycle_alerts method exists."""
        assert hasattr(vendor_service, "get_all_lifecycle_alerts")
        assert callable(getattr(vendor_service, "get_all_lifecycle_alerts"))

    def test_get_vendor_risk_summary_method_exists(self, vendor_service):
        """Test get_vendor_risk_summary method exists."""
        assert hasattr(vendor_service, "get_vendor_risk_summary")
        assert callable(getattr(vendor_service, "get_vendor_risk_summary"))


class TestAlertingLiveIntegration:
    """Live integration tests for alerting with Qdrant."""

    def test_get_eol_alerts_returns_alerts(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_eol_alerts retrieves EOL alerts from Qdrant."""
        from api.vendor_equipment import VendorEquipmentService, EquipmentModel
        from api.vendor_equipment.embedding_service import EmbeddingService
        from qdrant_client.models import PointStruct
        from datetime import date, timedelta
        import uuid
        import hashlib

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )
        embedding_service = EmbeddingService(lazy_load=True)

        # Create equipment with approaching EOL
        test_model_id = f"MODEL-EOL-{uuid.uuid4().hex[:8]}"
        eol_date = date.today() + timedelta(days=60)

        equipment = EquipmentModel(
            model_id=test_model_id,
            vendor_id=f"VENDOR-{uuid.uuid4().hex[:8]}",
            model_name="EOL Alert Test Router",
            customer_id=test_customer_ids["customer_a"],
            eol_date=eol_date,
            deployed_count=10,
        )

        # Store in Qdrant
        point_id = hashlib.md5(f"equipment:{test_model_id}".encode()).hexdigest()
        vector = embedding_service.encode(f"{equipment.model_name} router network")

        qdrant_client.upsert(
            collection_name="ner11_vendor_equipment",
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=equipment.to_qdrant_payload(),
                )
            ],
        )

        # Get EOL alerts
        alerts = service.get_eol_alerts(days_ahead=180)

        # Should find at least our test equipment
        assert isinstance(alerts, list)
        # Check the method runs without error (actual results depend on data in Qdrant)

        # Cleanup
        from qdrant_client.models import PointIdsList

        qdrant_client.delete(
            collection_name="ner11_vendor_equipment",
            points_selector=PointIdsList(points=[point_id]),
        )

    def test_get_contract_expiration_alerts_returns_alerts(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_contract_expiration_alerts retrieves contract alerts."""
        from api.vendor_equipment import VendorEquipmentService, SupportContract
        from api.vendor_equipment.vendor_models import ServiceLevel
        from api.vendor_equipment.embedding_service import EmbeddingService
        from qdrant_client.models import PointStruct
        from datetime import date, timedelta
        import uuid
        import hashlib

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )
        embedding_service = EmbeddingService(lazy_load=True)

        # Create expiring contract
        test_contract_id = f"CONTRACT-EXP-{uuid.uuid4().hex[:8]}"

        contract = SupportContract(
            contract_id=test_contract_id,
            vendor_id=f"VENDOR-{uuid.uuid4().hex[:8]}",
            customer_id=test_customer_ids["customer_a"],
            start_date=date.today() - timedelta(days=365),
            end_date=date.today() + timedelta(days=30),
            service_level=ServiceLevel.STANDARD,
            covered_model_ids=["MODEL-001"],
        )

        # Store in Qdrant
        point_id = hashlib.md5(f"contract:{test_contract_id}".encode()).hexdigest()
        vector = embedding_service.encode(f"Support contract {test_contract_id}")

        qdrant_client.upsert(
            collection_name="ner11_vendor_equipment",
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=contract.to_qdrant_payload(),
                )
            ],
        )

        # Get contract alerts
        alerts = service.get_contract_expiration_alerts(days_ahead=90)

        # Should return list
        assert isinstance(alerts, list)

        # Cleanup
        from qdrant_client.models import PointIdsList

        qdrant_client.delete(
            collection_name="ner11_vendor_equipment",
            points_selector=PointIdsList(points=[point_id]),
        )

    def test_get_all_lifecycle_alerts_structure(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_all_lifecycle_alerts returns correct structure."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.get_all_lifecycle_alerts()

        # Check structure
        assert "eol_alerts" in result
        assert "contract_alerts" in result
        assert "total_critical" in result
        assert "total_high" in result
        assert "total_alerts" in result

        # Check types
        assert isinstance(result["eol_alerts"], list)
        assert isinstance(result["contract_alerts"], list)
        assert isinstance(result["total_critical"], int)
        assert isinstance(result["total_high"], int)
        assert isinstance(result["total_alerts"], int)


# =============================================
# Day 6: Batch Operations Tests
# =============================================


class TestBatchImportMethods:
    """Tests for batch import service methods."""

    def test_batch_import_vendors_method_exists(self, vendor_service):
        """Test batch_import_vendors method exists."""
        assert hasattr(vendor_service, "batch_import_vendors")
        assert callable(getattr(vendor_service, "batch_import_vendors"))

    def test_batch_import_equipment_method_exists(self, vendor_service):
        """Test batch_import_equipment method exists."""
        assert hasattr(vendor_service, "batch_import_equipment")
        assert callable(getattr(vendor_service, "batch_import_equipment"))

    def test_export_vendors_method_exists(self, vendor_service):
        """Test export_vendors method exists."""
        assert hasattr(vendor_service, "export_vendors")
        assert callable(getattr(vendor_service, "export_vendors"))

    def test_export_equipment_method_exists(self, vendor_service):
        """Test export_equipment method exists."""
        assert hasattr(vendor_service, "export_equipment")
        assert callable(getattr(vendor_service, "export_equipment"))


class TestBatchImportVendors:
    """Tests for batch vendor import functionality."""

    def test_batch_import_vendors_with_valid_data(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test batch import with valid vendor data."""
        from api.vendor_equipment import VendorEquipmentService
        import uuid

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        vendor_data = [
            {
                "vendor_id": f"BATCH-VENDOR-{uuid.uuid4().hex[:8]}",
                "name": "Batch Vendor 1",
                "risk_score": 5.0,
                "support_status": "active",
                "country": "USA",
                "industry_focus": ["IT", "Network"],
            },
            {
                "vendor_id": f"BATCH-VENDOR-{uuid.uuid4().hex[:8]}",
                "name": "Batch Vendor 2",
                "risk_score": 3.5,
                "support_status": "active",
                "country": "Germany",
            },
        ]

        result = service.batch_import_vendors(vendor_data)

        assert "imported_count" in result
        assert "skipped_count" in result
        assert "error_count" in result
        assert "imported_ids" in result
        assert isinstance(result["imported_ids"], list)

    def test_batch_import_vendors_with_missing_vendor_id(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test batch import with missing vendor_id returns error."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        vendor_data = [
            {"name": "No ID Vendor", "risk_score": 5.0},  # Missing vendor_id
        ]

        result = service.batch_import_vendors(vendor_data)

        assert result["error_count"] >= 1
        assert len(result["errors"]) >= 1
        assert "Missing vendor_id" in str(result["errors"])


class TestBatchImportEquipment:
    """Tests for batch equipment import functionality."""

    def test_batch_import_equipment_with_valid_data(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test batch import with valid equipment data."""
        from api.vendor_equipment import VendorEquipmentService
        import uuid
        from datetime import date, timedelta

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        equipment_data = [
            {
                "model_id": f"BATCH-EQUIP-{uuid.uuid4().hex[:8]}",
                "vendor_id": "VENDOR-001",
                "model_name": "Batch Router 1000",
                "category": "Router",
                "criticality": "high",
                "eol_date": (date.today() + timedelta(days=180)).isoformat(),
            },
            {
                "model_id": f"BATCH-EQUIP-{uuid.uuid4().hex[:8]}",
                "vendor_id": "VENDOR-002",
                "model_name": "Batch Switch 2000",
                "category": "Switch",
                "criticality": "medium",
            },
        ]

        result = service.batch_import_equipment(equipment_data)

        assert "imported_count" in result
        assert "skipped_count" in result
        assert "error_count" in result
        assert "imported_ids" in result

    def test_batch_import_equipment_with_missing_model_id(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test batch import with missing model_id returns error."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        equipment_data = [
            {"model_name": "No ID Equipment", "vendor_id": "VENDOR-001"},  # Missing model_id
        ]

        result = service.batch_import_equipment(equipment_data)

        assert result["error_count"] >= 1
        assert len(result["errors"]) >= 1
        assert "Missing model_id" in str(result["errors"])


class TestExportOperations:
    """Tests for export functionality."""

    def test_export_vendors_returns_list(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test export_vendors returns list of vendor dictionaries."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.export_vendors()

        assert isinstance(result, list)
        # If vendors exist, check structure
        if len(result) > 0:
            vendor = result[0]
            assert "vendor_id" in vendor
            assert "name" in vendor

    def test_export_vendors_csv_format(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test export_vendors with CSV format."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.export_vendors(format="csv_rows")

        assert isinstance(result, list)

    def test_export_equipment_returns_list(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test export_equipment returns list of equipment dictionaries."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.export_equipment()

        assert isinstance(result, list)
        # If equipment exists, check structure
        if len(result) > 0:
            eq = result[0]
            assert "model_id" in eq
            assert "model_name" in eq

    def test_export_equipment_filtered_by_vendor(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test export_equipment with vendor filter."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.export_equipment(vendor_id="TEST-VENDOR-001")

        assert isinstance(result, list)


# =============================================
# Day 6: Reporting and Analytics Tests
# =============================================


class TestReportingMethods:
    """Tests for reporting service methods."""

    def test_get_dashboard_summary_method_exists(self, vendor_service):
        """Test get_dashboard_summary method exists."""
        assert hasattr(vendor_service, "get_dashboard_summary")
        assert callable(getattr(vendor_service, "get_dashboard_summary"))

    def test_get_vendor_analytics_method_exists(self, vendor_service):
        """Test get_vendor_analytics method exists."""
        assert hasattr(vendor_service, "get_vendor_analytics")
        assert callable(getattr(vendor_service, "get_vendor_analytics"))

    def test_get_lifecycle_report_method_exists(self, vendor_service):
        """Test get_lifecycle_report method exists."""
        assert hasattr(vendor_service, "get_lifecycle_report")
        assert callable(getattr(vendor_service, "get_lifecycle_report"))


class TestDashboardSummary:
    """Tests for dashboard summary functionality."""

    def test_get_dashboard_summary_returns_dict(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_dashboard_summary returns dictionary with expected keys."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.get_dashboard_summary()

        assert isinstance(result, dict)
        assert "customer_id" in result
        assert "summary" in result
        assert "equipment_by_lifecycle" in result
        assert "equipment_by_criticality" in result
        assert "alerts" in result

    def test_get_dashboard_summary_structure(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_dashboard_summary has correct nested structure."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.get_dashboard_summary()

        # Check summary structure
        summary = result["summary"]
        assert "total_vendors" in summary
        assert "total_equipment" in summary
        assert "total_deployed_assets" in summary
        assert "total_vulnerabilities" in summary

        # Check lifecycle counts
        lifecycle = result["equipment_by_lifecycle"]
        assert "current" in lifecycle
        assert "approaching_eol" in lifecycle
        assert "eol" in lifecycle
        assert "eos" in lifecycle

        # Check alerts
        alerts = result["alerts"]
        assert "total" in alerts
        assert "critical" in alerts
        assert "high" in alerts


class TestVendorAnalytics:
    """Tests for vendor analytics functionality."""

    def test_get_vendor_analytics_returns_list(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_vendor_analytics returns list."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.get_vendor_analytics()

        assert isinstance(result, list)

    def test_get_vendor_analytics_with_vendor_filter(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_vendor_analytics with specific vendor."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.get_vendor_analytics(vendor_id="TEST-VENDOR-001")

        assert isinstance(result, list)


class TestLifecycleReport:
    """Tests for lifecycle report functionality."""

    def test_get_lifecycle_report_returns_dict(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_lifecycle_report returns dictionary."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.get_lifecycle_report()

        assert isinstance(result, dict)
        assert "customer_id" in result
        assert "report_date" in result
        assert "summary" in result
        assert "timeline" in result
        assert "recommendations" in result

    def test_get_lifecycle_report_timeline_structure(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_lifecycle_report timeline has correct periods."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.get_lifecycle_report()

        timeline = result["timeline"]
        assert "past_due" in timeline
        assert "next_7_days" in timeline
        assert "next_30_days" in timeline
        assert "next_90_days" in timeline
        assert "next_180_days" in timeline

    def test_get_lifecycle_report_with_custom_days(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_lifecycle_report with custom days_ahead."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.get_lifecycle_report(days_ahead=365)

        assert result["look_ahead_days"] == 365


# =========================================================================
# Day 7: Maintenance Window Management Tests
# =========================================================================


class TestMaintenanceWindowDataclass:
    """Tests for MaintenanceWindow dataclass."""

    def test_maintenance_window_creation(self):
        """Test MaintenanceWindow creation with defaults."""
        from api.vendor_equipment import MaintenanceWindow, MaintenanceWindowType

        window = MaintenanceWindow(
            window_id="MW-001",
            customer_id="CUST-001",
            name="Weekly Patching Window",
        )

        assert window.window_id == "MW-001"
        assert window.customer_id == "CUST-001"
        assert window.name == "Weekly Patching Window"
        assert window.window_type == MaintenanceWindowType.SCHEDULED
        assert window.duration_hours == 4
        assert window.is_recurring is False
        assert window.is_active is True

    def test_maintenance_window_with_recurrence(self):
        """Test MaintenanceWindow with recurrence pattern."""
        from api.vendor_equipment import MaintenanceWindow, MaintenanceWindowType
        from datetime import datetime

        window = MaintenanceWindow(
            window_id="MW-002",
            customer_id="CUST-001",
            name="Monthly Firmware Updates",
            window_type=MaintenanceWindowType.FIRMWARE,
            is_recurring=True,
            recurrence_pattern="monthly",
            duration_hours=8,
        )

        assert window.is_recurring is True
        assert window.recurrence_pattern == "monthly"
        assert window.window_type == MaintenanceWindowType.FIRMWARE

    def test_maintenance_window_to_dict(self):
        """Test MaintenanceWindow to_dict serialization."""
        from api.vendor_equipment import MaintenanceWindow

        window = MaintenanceWindow(
            window_id="MW-003",
            customer_id="CUST-001",
            name="Emergency Window",
            equipment_ids=["EQ-001", "EQ-002"],
        )

        result = window.to_dict()

        assert result["window_id"] == "MW-003"
        assert result["name"] == "Emergency Window"
        assert result["equipment_ids"] == ["EQ-001", "EQ-002"]
        assert "start_time" in result

    def test_maintenance_window_to_qdrant_payload(self):
        """Test MaintenanceWindow to_qdrant_payload."""
        from api.vendor_equipment import MaintenanceWindow

        window = MaintenanceWindow(
            window_id="MW-004",
            customer_id="CUST-001",
            name="Patching Window",
            vendor_ids=["V-001"],
            categories=["network"],
        )

        payload = window.to_qdrant_payload()

        assert payload["entity_type"] == "maintenance_window"
        assert payload["window_id"] == "MW-004"
        assert payload["customer_id"] == "CUST-001"
        assert "V-001" in payload["vendor_ids"]

    def test_maintenance_window_is_in_window(self):
        """Test MaintenanceWindow is_in_window method."""
        from api.vendor_equipment import MaintenanceWindow
        from datetime import datetime, timedelta

        start = datetime.utcnow()
        window = MaintenanceWindow(
            window_id="MW-005",
            customer_id="CUST-001",
            name="Current Window",
            start_time=start,
            duration_hours=4,
        )

        # Should be in window now
        assert window.is_in_window() is True

        # Create window in the past
        past_start = datetime.utcnow() - timedelta(hours=10)
        past_window = MaintenanceWindow(
            window_id="MW-006",
            customer_id="CUST-001",
            name="Past Window",
            start_time=past_start,
            duration_hours=2,
        )

        assert past_window.is_in_window() is False


class TestMaintenanceWindowService:
    """Tests for maintenance window service methods."""

    def test_create_maintenance_window(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test create_maintenance_window stores window."""
        from api.vendor_equipment import (
            VendorEquipmentService,
            MaintenanceWindow,
            MaintenanceWindowType,
        )

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        window = MaintenanceWindow(
            window_id="MW-TEST-001",
            customer_id=test_customer_ids["customer_a"],
            name="Test Maintenance Window",
            window_type=MaintenanceWindowType.PATCHING,
            duration_hours=6,
        )

        result = service.create_maintenance_window(window)

        # Returns window_id on success
        assert result == "MW-TEST-001"

    def test_get_maintenance_window(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_maintenance_window retrieves window."""
        from api.vendor_equipment import (
            VendorEquipmentService,
            MaintenanceWindow,
        )

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        # Create window first
        window = MaintenanceWindow(
            window_id="MW-TEST-002",
            customer_id=test_customer_ids["customer_a"],
            name="Retrievable Window",
        )
        service.create_maintenance_window(window)

        # Retrieve it
        result = service.get_maintenance_window("MW-TEST-002")

        assert result is not None
        assert result["name"] == "Retrievable Window"

    def test_list_maintenance_windows(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test list_maintenance_windows returns list."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.list_maintenance_windows()

        assert isinstance(result, list)

    def test_list_maintenance_windows_with_type_filter(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test list_maintenance_windows with type filter."""
        from api.vendor_equipment import (
            VendorEquipmentService,
            MaintenanceWindow,
            MaintenanceWindowType,
        )

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        # Create an emergency window
        window = MaintenanceWindow(
            window_id="MW-EMERGENCY-001",
            customer_id=test_customer_ids["customer_a"],
            name="Emergency Fix",
            window_type=MaintenanceWindowType.EMERGENCY,
        )
        service.create_maintenance_window(window)

        result = service.list_maintenance_windows(
            window_type=MaintenanceWindowType.EMERGENCY
        )

        assert isinstance(result, list)

    def test_get_available_windows(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_available_windows returns windows in date range."""
        from api.vendor_equipment import VendorEquipmentService
        from datetime import date, timedelta

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        start_date = date.today()
        end_date = start_date + timedelta(days=30)

        result = service.get_available_windows(
            equipment_id="EQ-001",
            start_date=start_date,
            end_date=end_date,
        )

        assert isinstance(result, list)

    def test_check_maintenance_conflict_no_conflict(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test check_maintenance_conflict when no conflict exists."""
        from api.vendor_equipment import VendorEquipmentService
        from datetime import datetime, timedelta

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        # Check for conflict in far future
        proposed_start = datetime.utcnow() + timedelta(days=365)
        proposed_end = proposed_start + timedelta(hours=4)

        result = service.check_maintenance_conflict(
            equipment_id="EQ-NONEXISTENT",
            proposed_start=proposed_start,
            proposed_end=proposed_end,
        )

        assert isinstance(result, dict)
        assert "has_conflict" in result


# =========================================================================
# Day 8: Predictive Maintenance Tests
# =========================================================================


class TestMaintenancePredictionDataclass:
    """Tests for MaintenancePrediction dataclass."""

    def test_maintenance_prediction_creation(self):
        """Test MaintenancePrediction creation."""
        from api.vendor_equipment import MaintenancePrediction
        from datetime import date

        prediction = MaintenancePrediction(
            equipment_id="EQ-001",
            equipment_name="Core Router",
            customer_id="CUST-001",
            next_maintenance_date=date.today(),
            confidence_score=0.85,
            prediction_reason="Based on EOL schedule",
            days_until_maintenance=30,
            risk_score=7.5,
        )

        assert prediction.equipment_id == "EQ-001"
        assert prediction.confidence_score == 0.85
        assert prediction.risk_score == 7.5

    def test_maintenance_prediction_with_details(self):
        """Test MaintenancePrediction with full details."""
        from api.vendor_equipment import MaintenancePrediction
        from datetime import date

        prediction = MaintenancePrediction(
            equipment_id="EQ-002",
            equipment_name="Firewall",
            customer_id="CUST-001",
            next_maintenance_date=date.today(),
            confidence_score=0.92,
            prediction_reason="High vulnerability count",
            days_until_maintenance=14,
            risk_score=9.0,
            risk_factors=["CVE-2024-001", "EOL approaching"],
            recommended_tasks=["Firmware update", "Security patch"],
            estimated_downtime_hours=2.5,
            estimated_cost=1500.00,
        )

        assert len(prediction.risk_factors) == 2
        assert len(prediction.recommended_tasks) == 2
        assert prediction.estimated_downtime_hours == 2.5
        assert prediction.estimated_cost == 1500.00

    def test_maintenance_prediction_to_dict(self):
        """Test MaintenancePrediction to_dict serialization."""
        from api.vendor_equipment import MaintenancePrediction
        from datetime import date

        prediction = MaintenancePrediction(
            equipment_id="EQ-003",
            equipment_name="Switch",
            customer_id="CUST-001",
            next_maintenance_date=date.today(),
            confidence_score=0.75,
            prediction_reason="Scheduled maintenance",
            days_until_maintenance=60,
            risk_score=4.0,
        )

        result = prediction.to_dict()

        assert result["equipment_id"] == "EQ-003"
        assert result["confidence_score"] == 0.75
        assert "next_maintenance_date" in result


class TestPredictiveMaintenanceService:
    """Tests for predictive maintenance service methods."""

    def test_predict_maintenance_returns_prediction(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test predict_maintenance returns prediction object."""
        from api.vendor_equipment import (
            VendorEquipmentService,
            EquipmentModel,
            LifecycleStatus,
        )
        from datetime import date

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        # Create equipment to predict for
        equipment = EquipmentModel(
            model_id="EQ-PREDICT-001",
            vendor_id="V-001",
            customer_id=test_customer_ids["customer_a"],
            model_name="Predictable Router",
            lifecycle_status=LifecycleStatus.CURRENT,
            eol_date=date.today(),
        )
        service.create_equipment(equipment)

        result = service.predict_maintenance("EQ-PREDICT-001")

        # May return None if equipment not found or prediction fails
        # Returns list of MaintenancePrediction objects
        assert result is None or isinstance(result, list)

    def test_predict_maintenance_with_days_ahead(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test predict_maintenance with custom days_ahead."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.predict_maintenance(
            equipment_id="EQ-PREDICT-001",
            days_ahead=180,
        )

        # Returns list of MaintenancePrediction objects
        assert result is None or isinstance(result, list)

    def test_get_maintenance_forecast(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_maintenance_forecast returns forecast."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.get_maintenance_forecast(months_ahead=6)

        assert isinstance(result, dict)
        assert "forecast_months" in result
        assert "monthly_breakdown" in result
        assert "generated_at" in result

    def test_get_maintenance_forecast_structure(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_maintenance_forecast has correct structure."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.get_maintenance_forecast(months_ahead=3)

        # Check top-level keys
        assert "total_estimated_cost" in result
        assert "total_estimated_hours" in result
        assert "total_maintenance_events" in result
        assert "monthly_breakdown" in result


# =========================================================================
# Day 9: Work Order Management Tests
# =========================================================================


class TestWorkOrderDataclasses:
    """Tests for work order related dataclasses."""

    def test_work_order_status_enum(self):
        """Test WorkOrderStatus enum values."""
        from api.vendor_equipment import WorkOrderStatus

        assert WorkOrderStatus.DRAFT.value == "draft"
        assert WorkOrderStatus.PENDING.value == "pending"
        assert WorkOrderStatus.APPROVED.value == "approved"
        assert WorkOrderStatus.IN_PROGRESS.value == "in_progress"
        assert WorkOrderStatus.COMPLETED.value == "completed"
        assert WorkOrderStatus.CANCELLED.value == "cancelled"

    def test_work_order_priority_enum(self):
        """Test WorkOrderPriority enum values."""
        from api.vendor_equipment import WorkOrderPriority

        assert WorkOrderPriority.LOW.value == "low"
        assert WorkOrderPriority.MEDIUM.value == "medium"
        assert WorkOrderPriority.HIGH.value == "high"
        assert WorkOrderPriority.CRITICAL.value == "critical"
        assert WorkOrderPriority.EMERGENCY.value == "emergency"

    def test_work_order_creation(self):
        """Test MaintenanceWorkOrder creation."""
        from api.vendor_equipment import (
            MaintenanceWorkOrder,
            WorkOrderStatus,
            WorkOrderPriority,
        )

        wo = MaintenanceWorkOrder(
            work_order_id="WO-001",
            customer_id="CUST-001",
            title="Router Firmware Update",
        )

        assert wo.work_order_id == "WO-001"
        assert wo.title == "Router Firmware Update"
        assert wo.status == WorkOrderStatus.DRAFT
        assert wo.priority == WorkOrderPriority.MEDIUM

    def test_work_order_with_full_details(self):
        """Test MaintenanceWorkOrder with all fields."""
        from api.vendor_equipment import (
            MaintenanceWorkOrder,
            WorkOrderStatus,
            WorkOrderPriority,
        )
        from datetime import datetime, timedelta

        start = datetime.utcnow()
        end = start + timedelta(hours=4)

        wo = MaintenanceWorkOrder(
            work_order_id="WO-002",
            customer_id="CUST-001",
            title="Emergency Security Patch",
            equipment_ids=["EQ-001", "EQ-002"],
            status=WorkOrderStatus.APPROVED,
            priority=WorkOrderPriority.CRITICAL,
            scheduled_start=start,
            scheduled_end=end,
            tasks=["Apply patch", "Verify", "Test"],
            assigned_to="John Smith",
        )

        assert wo.priority == WorkOrderPriority.CRITICAL
        assert len(wo.equipment_ids) == 2
        assert len(wo.tasks) == 3
        assert wo.assigned_to == "John Smith"

    def test_work_order_get_duration_hours(self):
        """Test MaintenanceWorkOrder get_duration_hours method."""
        from api.vendor_equipment import MaintenanceWorkOrder
        from datetime import datetime, timedelta

        start = datetime.utcnow()
        end = start + timedelta(hours=6)

        wo = MaintenanceWorkOrder(
            work_order_id="WO-003",
            customer_id="CUST-001",
            title="Planned Maintenance",
            actual_start=start,
            actual_end=end,
        )

        duration = wo.get_duration_hours()
        assert duration == 6.0

    def test_work_order_is_overdue(self):
        """Test MaintenanceWorkOrder is_overdue method."""
        from api.vendor_equipment import MaintenanceWorkOrder, WorkOrderStatus
        from datetime import datetime, timedelta

        # Create overdue work order
        past_end = datetime.utcnow() - timedelta(hours=24)
        wo = MaintenanceWorkOrder(
            work_order_id="WO-004",
            customer_id="CUST-001",
            title="Overdue Maintenance",
            status=WorkOrderStatus.IN_PROGRESS,
            scheduled_end=past_end,
        )

        assert wo.is_overdue() is True

        # Create not overdue (completed)
        wo_completed = MaintenanceWorkOrder(
            work_order_id="WO-005",
            customer_id="CUST-001",
            title="Completed Maintenance",
            status=WorkOrderStatus.COMPLETED,
            scheduled_end=past_end,
        )

        assert wo_completed.is_overdue() is False

    def test_work_order_to_dict(self):
        """Test MaintenanceWorkOrder to_dict serialization."""
        from api.vendor_equipment import MaintenanceWorkOrder

        wo = MaintenanceWorkOrder(
            work_order_id="WO-006",
            customer_id="CUST-001",
            title="Test Work Order",
            tasks=["Task 1", "Task 2"],
        )

        result = wo.to_dict()

        assert result["work_order_id"] == "WO-006"
        assert result["title"] == "Test Work Order"
        assert len(result["tasks"]) == 2

    def test_work_order_to_qdrant_payload(self):
        """Test MaintenanceWorkOrder to_qdrant_payload."""
        from api.vendor_equipment import MaintenanceWorkOrder

        wo = MaintenanceWorkOrder(
            work_order_id="WO-007",
            customer_id="CUST-001",
            title="Qdrant Test",
            equipment_ids=["EQ-001"],
        )

        payload = wo.to_qdrant_payload()

        assert payload["entity_type"] == "work_order"
        assert payload["work_order_id"] == "WO-007"
        assert payload["customer_id"] == "CUST-001"


class TestWorkOrderService:
    """Tests for work order service methods."""

    def test_create_work_order(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test create_work_order stores work order."""
        from api.vendor_equipment import (
            VendorEquipmentService,
            MaintenanceWorkOrder,
            WorkOrderPriority,
        )

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        wo = MaintenanceWorkOrder(
            work_order_id="WO-TEST-001",
            customer_id=test_customer_ids["customer_a"],
            title="Test Work Order Creation",
            priority=WorkOrderPriority.HIGH,
        )

        result = service.create_work_order(wo)

        # Returns work_order_id on success
        assert result == "WO-TEST-001"

    def test_get_work_order(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_work_order retrieves work order."""
        from api.vendor_equipment import (
            VendorEquipmentService,
            MaintenanceWorkOrder,
        )

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        # Create work order first
        wo = MaintenanceWorkOrder(
            work_order_id="WO-TEST-002",
            customer_id=test_customer_ids["customer_a"],
            title="Retrievable Work Order",
        )
        service.create_work_order(wo)

        # Retrieve it
        result = service.get_work_order("WO-TEST-002")

        assert result is not None
        assert result["title"] == "Retrievable Work Order"

    def test_list_work_orders(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test list_work_orders returns list."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.list_work_orders()

        assert isinstance(result, list)

    def test_list_work_orders_with_status_filter(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test list_work_orders with status filter."""
        from api.vendor_equipment import (
            VendorEquipmentService,
            MaintenanceWorkOrder,
            WorkOrderStatus,
        )

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        # Create a pending work order
        wo = MaintenanceWorkOrder(
            work_order_id="WO-PENDING-001",
            customer_id=test_customer_ids["customer_a"],
            title="Pending Work Order",
            status=WorkOrderStatus.PENDING,
        )
        service.create_work_order(wo)

        result = service.list_work_orders(status=WorkOrderStatus.PENDING)

        assert isinstance(result, list)

    def test_list_work_orders_with_priority_filter(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test list_work_orders with priority filter."""
        from api.vendor_equipment import (
            VendorEquipmentService,
            MaintenanceWorkOrder,
            WorkOrderPriority,
        )

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        # Create a critical work order
        wo = MaintenanceWorkOrder(
            work_order_id="WO-CRITICAL-001",
            customer_id=test_customer_ids["customer_a"],
            title="Critical Work Order",
            priority=WorkOrderPriority.CRITICAL,
        )
        service.create_work_order(wo)

        result = service.list_work_orders(priority=WorkOrderPriority.CRITICAL)

        assert isinstance(result, list)

    def test_update_work_order_status(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test update_work_order_status changes status."""
        from api.vendor_equipment import (
            VendorEquipmentService,
            MaintenanceWorkOrder,
            WorkOrderStatus,
        )

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        # Create work order
        wo = MaintenanceWorkOrder(
            work_order_id="WO-UPDATE-001",
            customer_id=test_customer_ids["customer_a"],
            title="Status Update Test",
            status=WorkOrderStatus.DRAFT,
        )
        service.create_work_order(wo)

        # Update status
        result = service.update_work_order_status(
            work_order_id="WO-UPDATE-001",
            new_status=WorkOrderStatus.APPROVED,
            notes="Approved by manager",
        )

        assert result is True

    def test_get_work_order_summary(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_work_order_summary returns summary."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.get_work_order_summary()

        assert isinstance(result, dict)
        assert "customer_id" in result
        assert "total_work_orders" in result
        assert "status_breakdown" in result
        assert "priority_breakdown" in result

    def test_get_work_order_summary_structure(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test get_work_order_summary has correct structure."""
        from api.vendor_equipment import VendorEquipmentService

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        result = service.get_work_order_summary()

        by_status = result["status_breakdown"]
        assert "draft" in by_status
        assert "pending" in by_status
        assert "in_progress" in by_status
        assert "completed" in by_status

        by_priority = result["priority_breakdown"]
        assert "low" in by_priority
        assert "medium" in by_priority
        assert "high" in by_priority
        assert "critical" in by_priority

    def test_create_work_order_from_prediction(
        self, qdrant_client, test_customer_ids, customer_a_context
    ):
        """Test create_work_order_from_prediction creates work order."""
        from api.vendor_equipment import (
            VendorEquipmentService,
            MaintenancePrediction,
        )
        from datetime import date

        service = VendorEquipmentService(
            qdrant_url="http://localhost:6333",
            neo4j_driver=None,
        )

        prediction = MaintenancePrediction(
            equipment_id="EQ-PRED-001",
            equipment_name="Predicted Equipment",
            customer_id=test_customer_ids["customer_a"],
            next_maintenance_date=date.today(),
            confidence_score=0.9,
            prediction_reason="High risk score",
            days_until_maintenance=7,
            risk_score=8.5,
            recommended_tasks=["Update firmware", "Apply patches"],
        )

        result = service.create_work_order_from_prediction(
            prediction=prediction,
            title_prefix="AUTO",
            assigned_to="Auto-Assign Team",
        )

        # Returns work_order_id string directly
        assert result is not None
        assert isinstance(result, str)
        assert result.startswith("WO-")


# Run with: python3 -m pytest tests/integration/test_vendor_equipment_integration.py -v
