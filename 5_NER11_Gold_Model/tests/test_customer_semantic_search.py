"""
Tests for Customer-Isolated Semantic Search API
================================================

Comprehensive unit tests for NER30 semantic search with customer isolation.

Version: 1.0.0
Created: 2025-12-04
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

# Import modules under test
import sys
sys.path.insert(0, "..")

from api.customer_isolation.customer_context import (
    CustomerContext,
    CustomerAccessLevel,
    CustomerContextManager,
    get_customer_context,
    require_customer_context,
)
from api.customer_isolation.isolated_semantic_service import (
    CustomerIsolatedSemanticService,
    CustomerSemanticSearchRequest,
    CustomerSemanticSearchResponse,
    CustomerSemanticSearchResult,
)


# ============================================================================
# CUSTOMER CONTEXT TESTS
# ============================================================================

class TestCustomerContext:
    """Tests for CustomerContext dataclass."""

    def test_create_valid_context(self):
        """Test creating valid customer context."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="acme_corp",
            access_level=CustomerAccessLevel.READ,
        )

        assert context.customer_id == "CUST-001"
        assert context.namespace == "acme_corp"
        assert context.access_level == CustomerAccessLevel.READ
        assert context.include_system is True

    def test_create_context_requires_customer_id(self):
        """Test that customer_id is required."""
        with pytest.raises(ValueError, match="customer_id is required"):
            CustomerContext(customer_id="", namespace="test")

    def test_create_context_requires_namespace(self):
        """Test that namespace is required."""
        with pytest.raises(ValueError, match="namespace is required"):
            CustomerContext(customer_id="CUST-001", namespace="")

    def test_get_customer_ids_with_system(self):
        """Test getting customer IDs including SYSTEM."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
            include_system=True,
        )

        ids = context.get_customer_ids()
        assert ids == ["CUST-001", "SYSTEM"]

    def test_get_customer_ids_without_system(self):
        """Test getting customer IDs excluding SYSTEM."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
            include_system=False,
        )

        ids = context.get_customer_ids()
        assert ids == ["CUST-001"]

    def test_can_write_with_read_access(self):
        """Test write permission check with READ access."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
            access_level=CustomerAccessLevel.READ,
        )

        assert context.can_write() is False

    def test_can_write_with_write_access(self):
        """Test write permission check with WRITE access."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
            access_level=CustomerAccessLevel.WRITE,
        )

        assert context.can_write() is True

    def test_can_admin(self):
        """Test admin permission check."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
            access_level=CustomerAccessLevel.ADMIN,
        )

        assert context.can_admin() is True
        assert context.can_write() is True

    def test_to_audit_dict(self):
        """Test converting context to audit dictionary."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
            access_level=CustomerAccessLevel.READ,
            user_id="user-123",
        )

        audit = context.to_audit_dict()

        assert audit["customer_id"] == "CUST-001"
        assert audit["namespace"] == "test"
        assert audit["access_level"] == "read"
        assert audit["user_id"] == "user-123"
        assert "timestamp" in audit


class TestCustomerContextManager:
    """Tests for CustomerContextManager."""

    def test_set_and_get_context(self):
        """Test setting and getting context."""
        context = CustomerContext(customer_id="CUST-001", namespace="test")

        CustomerContextManager.set_context(context)
        retrieved = CustomerContextManager.get_context()

        assert retrieved == context

        # Cleanup
        CustomerContextManager.clear_context()

    def test_clear_context(self):
        """Test clearing context."""
        context = CustomerContext(customer_id="CUST-001", namespace="test")
        CustomerContextManager.set_context(context)
        CustomerContextManager.clear_context()

        assert CustomerContextManager.get_context() is None

    def test_require_context_raises_when_not_set(self):
        """Test that require_context raises when no context."""
        CustomerContextManager.clear_context()

        with pytest.raises(ValueError, match="Customer context required"):
            CustomerContextManager.require_context()

    def test_require_context_returns_when_set(self):
        """Test that require_context returns context when set."""
        context = CustomerContext(customer_id="CUST-001", namespace="test")
        CustomerContextManager.set_context(context)

        retrieved = CustomerContextManager.require_context()
        assert retrieved == context

        CustomerContextManager.clear_context()

    def test_create_context(self):
        """Test creating and setting context in one call."""
        context = CustomerContextManager.create_context(
            customer_id="CUST-002",
            namespace="new_namespace",
            access_level=CustomerAccessLevel.WRITE,
        )

        assert context.customer_id == "CUST-002"
        assert context.namespace == "new_namespace"
        assert context.access_level == CustomerAccessLevel.WRITE

        # Verify it was also set
        retrieved = CustomerContextManager.get_context()
        assert retrieved == context

        CustomerContextManager.clear_context()


# ============================================================================
# ISOLATED SEMANTIC SERVICE TESTS
# ============================================================================

class TestCustomerIsolatedSemanticService:
    """Tests for CustomerIsolatedSemanticService."""

    @pytest.fixture
    def mock_qdrant_client(self):
        """Create mock Qdrant client."""
        with patch("api.customer_isolation.isolated_semantic_service.QdrantClient") as mock:
            yield mock.return_value

    @pytest.fixture
    def mock_embedding_model(self):
        """Create mock embedding model."""
        model = Mock()
        model.encode.return_value = [[0.1, 0.2, 0.3] * 128]  # 384 dim
        return model

    @pytest.fixture
    def service(self, mock_qdrant_client, mock_embedding_model):
        """Create service with mocks."""
        service = CustomerIsolatedSemanticService(
            qdrant_url="http://localhost:6333",
            collection_name="test_collection",
        )
        service.client = mock_qdrant_client
        service._embedding_model = mock_embedding_model
        return service

    def test_build_customer_filter(self, service):
        """Test building customer filter."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
            include_system=True,
        )

        filter_obj = service._build_customer_filter(context)

        assert filter_obj is not None
        assert len(filter_obj.must) == 1
        assert filter_obj.must[0].key == "customer_id"

    def test_build_customer_filter_with_additional(self, service):
        """Test building customer filter with additional filters."""
        from qdrant_client.models import FieldCondition, MatchValue

        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
        )

        additional = [
            FieldCondition(key="ner_label", match=MatchValue(value="MALWARE"))
        ]

        filter_obj = service._build_customer_filter(context, additional)

        assert len(filter_obj.must) == 2

    def test_build_hierarchy_filters(self, service):
        """Test building hierarchy filters."""
        filters = service._build_hierarchy_filters(
            ner_label="MALWARE",
            fine_grained_type="RANSOMWARE",
            min_confidence=0.8,
        )

        assert len(filters) == 3

    def test_search_applies_customer_filter(self, service, mock_qdrant_client):
        """Test that search applies customer filter."""
        # Setup mock response
        mock_point = Mock()
        mock_point.score = 0.95
        mock_point.payload = {
            "entity": "WannaCry",
            "ner_label": "MALWARE",
            "fine_grained_type": "RANSOMWARE",
            "hierarchy_path": "MALWARE/RANSOMWARE",
            "confidence": 0.98,
            "doc_id": "doc-1",
            "customer_id": "CUST-001",
        }
        mock_qdrant_client.search.return_value = [mock_point]

        # Execute search
        request = CustomerSemanticSearchRequest(
            query="ransomware attack",
            customer_id="CUST-001",
            limit=10,
        )

        response = service.search(request)

        # Verify search was called with customer filter
        mock_qdrant_client.search.assert_called_once()
        call_kwargs = mock_qdrant_client.search.call_args.kwargs
        assert "query_filter" in call_kwargs

        # Verify response
        assert response.customer_id == "CUST-001"
        assert len(response.results) == 1
        assert response.results[0].customer_id == "CUST-001"

    def test_search_marks_system_entities(self, service, mock_qdrant_client):
        """Test that SYSTEM entities are marked correctly."""
        mock_point = Mock()
        mock_point.score = 0.90
        mock_point.payload = {
            "entity": "CVE-2017-0144",
            "ner_label": "CVE",
            "fine_grained_type": "CVE",
            "hierarchy_path": "CVE",
            "confidence": 1.0,
            "doc_id": "system-1",
            "customer_id": "SYSTEM",
        }
        mock_qdrant_client.search.return_value = [mock_point]

        request = CustomerSemanticSearchRequest(
            query="EternalBlue",
            customer_id="CUST-001",
            include_system=True,
        )

        response = service.search(request)

        assert response.results[0].is_system is True
        assert response.results[0].customer_id == "SYSTEM"

    def test_upsert_requires_write_access(self, service):
        """Test that upsert requires write access."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
            access_level=CustomerAccessLevel.READ,
        )

        with pytest.raises(PermissionError, match="does not have write access"):
            service.upsert_entity(
                entity_id="ent-1",
                entity_text="Test entity",
                embedding=[0.1] * 384,
                payload={},
                context=context,
            )

    def test_upsert_adds_customer_id(self, service, mock_qdrant_client):
        """Test that upsert adds customer_id to payload."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
            access_level=CustomerAccessLevel.WRITE,
        )

        service.upsert_entity(
            entity_id="ent-1",
            entity_text="Test entity",
            embedding=[0.1] * 384,
            payload={"ner_label": "MALWARE"},
            context=context,
        )

        # Verify upsert was called with customer_id in payload
        mock_qdrant_client.upsert.assert_called_once()
        call_kwargs = mock_qdrant_client.upsert.call_args.kwargs
        points = call_kwargs["points"]
        assert points[0].payload["customer_id"] == "CUST-001"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestSemanticSearchIntegration:
    """Integration tests for semantic search workflow."""

    def test_end_to_end_isolation(self):
        """Test complete isolation workflow."""
        # Create context for Customer A
        context_a = CustomerContext(
            customer_id="CUST-A",
            namespace="customer_a",
            include_system=True,
        )

        # Create context for Customer B
        context_b = CustomerContext(
            customer_id="CUST-B",
            namespace="customer_b",
            include_system=False,
        )

        # Verify they have different customer IDs in filter
        assert "CUST-A" in context_a.get_customer_ids()
        assert "CUST-B" in context_b.get_customer_ids()
        assert "CUST-A" not in context_b.get_customer_ids()

        # Verify SYSTEM access differs
        assert "SYSTEM" in context_a.get_customer_ids()
        assert "SYSTEM" not in context_b.get_customer_ids()

    def test_context_lifecycle(self):
        """Test context is properly managed through lifecycle."""
        # Initially no context
        assert get_customer_context() is None

        # Create context
        context = CustomerContextManager.create_context(
            customer_id="CUST-TEST",
            namespace="test",
        )

        # Context should be available
        assert get_customer_context() is not None
        assert get_customer_context().customer_id == "CUST-TEST"

        # Clear context
        CustomerContextManager.clear_context()

        # Context should be gone
        assert get_customer_context() is None


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
