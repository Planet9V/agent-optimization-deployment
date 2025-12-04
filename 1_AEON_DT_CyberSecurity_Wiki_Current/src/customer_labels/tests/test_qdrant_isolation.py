"""
CUSTOMER_LABELS: Unit Tests for Qdrant Customer Isolation
Phase B1 - Order 1 of 6 MVP Enhancements
Version: 1.0.0
Created: 2025-12-04

Tests for Qdrant vector store customer isolation.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import numpy as np

from src.customer_labels.qdrant.customer_vector_store import (
    CustomerVectorContext,
    CustomerIsolatedVectorStore,
    CustomerVectorStoreFactory,
    QdrantAuditLogger
)


# ============================================================
# SECTION 1: CustomerVectorContext Tests
# ============================================================

class TestCustomerVectorContext:
    """Tests for CustomerVectorContext dataclass."""

    def test_context_creation(self):
        """Test creating a context with all fields."""
        context = CustomerVectorContext(
            customer_id="CUST-001",
            include_system=True,
            access_level="admin"
        )

        assert context.customer_id == "CUST-001"
        assert context.include_system is True
        assert context.access_level == "admin"

    def test_context_defaults(self):
        """Test context default values."""
        context = CustomerVectorContext(customer_id="CUST-002")

        assert context.include_system is True
        assert context.access_level == "read"

    def test_get_customer_ids_with_system(self):
        """Test customer IDs include SYSTEM when enabled."""
        context = CustomerVectorContext(
            customer_id="CUST-001",
            include_system=True
        )

        ids = context.get_customer_ids()

        assert "CUST-001" in ids
        assert "SYSTEM" in ids
        assert len(ids) == 2

    def test_get_customer_ids_without_system(self):
        """Test customer IDs exclude SYSTEM when disabled."""
        context = CustomerVectorContext(
            customer_id="CUST-001",
            include_system=False
        )

        ids = context.get_customer_ids()

        assert "CUST-001" in ids
        assert "SYSTEM" not in ids
        assert len(ids) == 1


# ============================================================
# SECTION 2: CustomerIsolatedVectorStore Tests
# ============================================================

class TestCustomerIsolatedVectorStore:
    """Tests for CustomerIsolatedVectorStore."""

    @pytest.fixture
    def mock_qdrant_client(self):
        """Create mock Qdrant client."""
        client = MagicMock()
        client.get_collections.return_value.collections = []
        client.search.return_value = []
        client.count.return_value.count = 0
        return client

    @pytest.fixture
    def vector_store(self, mock_qdrant_client):
        """Create vector store with mock client."""
        with patch('src.customer_labels.qdrant.customer_vector_store.QdrantClient') as mock_class:
            mock_class.return_value = mock_qdrant_client
            store = CustomerIsolatedVectorStore(
                url="localhost:6333",
                collection="test_entities"
            )
            store.client = mock_qdrant_client
            return store

    @pytest.fixture
    def customer_context(self):
        """Create test customer context."""
        return CustomerVectorContext(
            customer_id="CUST-TEST",
            include_system=True
        )

    def test_set_and_clear_context(self, vector_store, customer_context):
        """Test setting and clearing customer context."""
        # Initially no context
        assert vector_store._context is None

        # Set context
        vector_store.set_context(customer_context)
        assert vector_store._context == customer_context

        # Clear context
        vector_store.clear_context()
        assert vector_store._context is None

    def test_context_property_raises_without_context(self, vector_store):
        """Test context property raises error without context."""
        with pytest.raises(ValueError, match="Customer context not set"):
            _ = vector_store.context

    def test_build_customer_filter(self, vector_store, customer_context):
        """Test building filter with customer isolation."""
        vector_store.set_context(customer_context)

        filter_obj = vector_store._build_customer_filter()

        assert filter_obj is not None
        assert len(filter_obj.must) >= 1

    def test_build_customer_filter_with_additional(self, vector_store, customer_context):
        """Test filter with additional conditions."""
        from qdrant_client.models import FieldCondition, MatchValue

        vector_store.set_context(customer_context)

        additional = [
            FieldCondition(key="entity_type", match=MatchValue(value="CVE"))
        ]

        filter_obj = vector_store._build_customer_filter(additional)

        assert len(filter_obj.must) == 2  # customer_id + entity_type

    def test_upsert_entity_adds_customer_id(self, vector_store, customer_context, mock_qdrant_client):
        """Test that upsert adds customer_id to payload."""
        vector_store.set_context(customer_context)

        test_embedding = [0.1] * 384
        test_payload = {"name": "Test Entity"}

        vector_store.upsert_entity(
            entity_id="test-123",
            embedding=test_embedding,
            payload=test_payload
        )

        # Verify upsert was called with customer_id in payload
        call_args = mock_qdrant_client.upsert.call_args
        points = call_args[1]['points']

        assert len(points) == 1
        assert points[0].payload['customer_id'] == "CUST-TEST"
        assert points[0].payload['name'] == "Test Entity"

    def test_batch_upsert_adds_customer_id(self, vector_store, customer_context, mock_qdrant_client):
        """Test batch upsert adds customer_id to all entities."""
        vector_store.set_context(customer_context)

        entities = [
            {'id': 'e1', 'embedding': [0.1] * 384, 'payload': {'name': 'Entity 1'}},
            {'id': 'e2', 'embedding': [0.2] * 384, 'payload': {'name': 'Entity 2'}}
        ]

        count = vector_store.batch_upsert(entities, batch_size=10)

        assert count == 2
        mock_qdrant_client.upsert.assert_called()

    def test_search_similar_applies_customer_filter(self, vector_store, customer_context, mock_qdrant_client):
        """Test search applies customer filter."""
        vector_store.set_context(customer_context)

        # Mock search results
        mock_result = MagicMock()
        mock_result.id = "result-1"
        mock_result.score = 0.95
        mock_result.payload = {"name": "Found Entity"}
        mock_qdrant_client.search.return_value = [mock_result]

        results = vector_store.search_similar(
            query_embedding=[0.1] * 384,
            limit=10
        )

        # Verify search was called with filter
        call_args = mock_qdrant_client.search.call_args
        assert call_args[1]['query_filter'] is not None

        # Verify results
        assert len(results) == 1
        assert results[0]['id'] == "result-1"
        assert results[0]['score'] == 0.95

    def test_search_with_entity_type_filter(self, vector_store, customer_context, mock_qdrant_client):
        """Test search with entity type filter."""
        vector_store.set_context(customer_context)
        mock_qdrant_client.search.return_value = []

        results = vector_store.search_similar(
            query_embedding=[0.1] * 384,
            limit=10,
            entity_type="CVE"
        )

        # Verify filter includes entity_type
        call_args = mock_qdrant_client.search.call_args
        filter_obj = call_args[1]['query_filter']

        assert len(filter_obj.must) == 2  # customer_id + entity_type

    def test_get_customer_entity_count(self, vector_store, customer_context, mock_qdrant_client):
        """Test counting entities for customer."""
        vector_store.set_context(customer_context)
        mock_qdrant_client.count.return_value.count = 150

        count = vector_store.get_customer_entity_count()

        assert count == 150
        mock_qdrant_client.count.assert_called()


# ============================================================
# SECTION 3: CustomerVectorStoreFactory Tests
# ============================================================

class TestCustomerVectorStoreFactory:
    """Tests for CustomerVectorStoreFactory."""

    def test_get_store_creates_new_instance(self):
        """Test factory creates new store instance."""
        with patch('src.customer_labels.qdrant.customer_vector_store.QdrantClient'):
            # Clear cached instances
            CustomerVectorStoreFactory._instances = {}

            store = CustomerVectorStoreFactory.get_store(
                customer_id="CUST-001",
                url="localhost:6333",
                collection="test_entities"
            )

            assert store is not None
            assert store.context.customer_id == "CUST-001"

    def test_get_store_reuses_instance(self):
        """Test factory reuses existing store for same URL/collection."""
        with patch('src.customer_labels.qdrant.customer_vector_store.QdrantClient'):
            # Clear cached instances
            CustomerVectorStoreFactory._instances = {}

            store1 = CustomerVectorStoreFactory.get_store(
                customer_id="CUST-001",
                url="localhost:6333",
                collection="test_entities"
            )

            store2 = CustomerVectorStoreFactory.get_store(
                customer_id="CUST-002",
                url="localhost:6333",
                collection="test_entities"
            )

            # Same store instance, different context
            assert store1 is store2
            assert store2.context.customer_id == "CUST-002"


# ============================================================
# SECTION 4: Isolation Verification Tests
# ============================================================

class TestIsolationVerification:
    """Tests for customer isolation verification."""

    @pytest.fixture
    def configured_store(self):
        """Create configured store with mock client."""
        with patch('src.customer_labels.qdrant.customer_vector_store.QdrantClient') as mock_class:
            mock_client = MagicMock()
            mock_client.get_collections.return_value.collections = []
            mock_client.count.return_value.count = 100
            mock_class.return_value = mock_client

            store = CustomerIsolatedVectorStore(
                url="localhost:6333",
                collection="test_entities"
            )
            store.client = mock_client
            store.set_context(CustomerVectorContext(
                customer_id="CUST-001",
                include_system=True
            ))
            return store

    def test_verify_isolation_same_customer(self, configured_store):
        """Test isolation check with same customer."""
        result = configured_store.verify_isolation("CUST-001")

        assert result['valid'] is True
        assert "Same customer" in result['message']

    def test_verify_isolation_system_allowed(self, configured_store):
        """Test SYSTEM access is allowed when include_system=True."""
        result = configured_store.verify_isolation("SYSTEM")

        assert result['valid'] is True
        assert "SYSTEM access is allowed" in result['message']

    def test_verify_isolation_different_customer(self, configured_store):
        """Test isolation verification against different customer."""
        result = configured_store.verify_isolation("CUST-002")

        assert result['valid'] is True
        assert result['current_customer'] == "CUST-001"
        assert result['target_customer'] == "CUST-002"


# ============================================================
# SECTION 5: QdrantAuditLogger Tests
# ============================================================

class TestQdrantAuditLogger:
    """Tests for Qdrant audit logging."""

    def test_log_operation(self, caplog):
        """Test audit logging captures operations."""
        with patch('src.customer_labels.qdrant.customer_vector_store.QdrantClient'):
            store = CustomerIsolatedVectorStore(
                url="localhost:6333",
                collection="test_entities"
            )
            store.set_context(CustomerVectorContext(customer_id="CUST-001"))

            logger = QdrantAuditLogger(store)

            with caplog.at_level('INFO'):
                logger.log_operation(
                    operation="search",
                    entity_count=10,
                    metadata={"query_type": "similarity"}
                )

            assert "QDRANT_AUDIT" in caplog.text
            assert "CUST-001" in caplog.text


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
