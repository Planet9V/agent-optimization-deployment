"""
CUSTOMER_LABELS: Unit Tests for Customer Isolation
Phase B1 - Order 1 of 6 MVP Enhancements
Version: 1.0.0
Created: 2025-12-04

Minimum Coverage Target: 80% for multi-tenant logic
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

# Import the module under test
from src.customer_labels.middleware.customer_context import (
    CustomerContext,
    CustomerAccessLevel,
    CustomerContextManager,
    CustomerIsolatedSession,
    CustomerIsolationError,
    require_customer_context,
    CUSTOMER_QUERY_PATTERNS
)


# ============================================================
# SECTION 1: CustomerContext Tests
# ============================================================

class TestCustomerContext:
    """Tests for CustomerContext dataclass."""

    def test_customer_context_creation(self):
        """Test creating a CustomerContext with all fields."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="acme_corp",
            access_level=CustomerAccessLevel.READ,
            user_id="user-123",
            session_id="session-abc",
            include_system=True
        )

        assert context.customer_id == "CUST-001"
        assert context.namespace == "acme_corp"
        assert context.access_level == CustomerAccessLevel.READ
        assert context.user_id == "user-123"
        assert context.session_id == "session-abc"
        assert context.include_system is True

    def test_customer_context_defaults(self):
        """Test CustomerContext default values."""
        context = CustomerContext(
            customer_id="CUST-002",
            namespace="beta_inc"
        )

        assert context.access_level == CustomerAccessLevel.READ
        assert context.user_id is None
        assert context.session_id is None
        assert context.include_system is True

    def test_customer_context_to_dict(self):
        """Test CustomerContext serialization."""
        context = CustomerContext(
            customer_id="CUST-003",
            namespace="gamma_llc",
            access_level=CustomerAccessLevel.ADMIN
        )

        result = context.to_dict()

        assert result['customer_id'] == "CUST-003"
        assert result['namespace'] == "gamma_llc"
        assert result['access_level'] == "admin"
        assert result['include_system'] is True


# ============================================================
# SECTION 2: CustomerContextManager Tests
# ============================================================

class TestCustomerContextManager:
    """Tests for CustomerContextManager."""

    @pytest.fixture
    def mock_driver(self):
        """Create mock Neo4j driver."""
        driver = MagicMock()
        session = MagicMock()
        driver.session.return_value.__enter__ = Mock(return_value=session)
        driver.session.return_value.__exit__ = Mock(return_value=None)
        return driver

    @pytest.fixture
    def context_manager(self, mock_driver):
        """Create CustomerContextManager with mock driver."""
        return CustomerContextManager(mock_driver, audit_enabled=True)

    def test_push_and_pop_context(self, context_manager):
        """Test context stack operations."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test"
        )

        # Initially no context
        assert context_manager.current_context is None

        # Push context
        context_manager.push_context(context)
        assert context_manager.current_context == context

        # Pop context
        popped = context_manager.pop_context()
        assert popped == context
        assert context_manager.current_context is None

    def test_nested_contexts(self, context_manager):
        """Test nested customer contexts."""
        context1 = CustomerContext(customer_id="CUST-001", namespace="test1")
        context2 = CustomerContext(customer_id="CUST-002", namespace="test2")

        context_manager.push_context(context1)
        context_manager.push_context(context2)

        assert context_manager.current_context == context2

        context_manager.pop_context()
        assert context_manager.current_context == context1

        context_manager.pop_context()
        assert context_manager.current_context is None

    def test_get_filter_params_with_system(self, context_manager):
        """Test filter params include SYSTEM when configured."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
            include_system=True
        )
        context_manager.push_context(context)

        params = context_manager.get_customer_filter_params()

        assert params['customer_id'] == "CUST-001"
        assert 'SYSTEM' in params['customer_ids']
        assert 'CUST-001' in params['customer_ids']

    def test_get_filter_params_without_system(self, context_manager):
        """Test filter params exclude SYSTEM when configured."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
            include_system=False
        )
        context_manager.push_context(context)

        params = context_manager.get_customer_filter_params()

        assert params['customer_id'] == "CUST-001"
        assert 'SYSTEM' not in params['customer_ids']

    def test_get_filter_params_no_context_raises(self, context_manager):
        """Test error when getting params without context."""
        with pytest.raises(CustomerIsolationError):
            context_manager.get_customer_filter_params()


# ============================================================
# SECTION 3: CustomerIsolatedSession Tests
# ============================================================

class TestCustomerIsolatedSession:
    """Tests for CustomerIsolatedSession."""

    @pytest.fixture
    def mock_driver(self):
        """Create mock Neo4j driver."""
        driver = MagicMock()
        session = MagicMock()
        result = MagicMock()
        session.run.return_value = result
        driver.session.return_value = session
        return driver

    @pytest.fixture
    def customer_context(self):
        """Create test customer context."""
        return CustomerContext(
            customer_id="CUST-TEST",
            namespace="test_namespace",
            user_id="user-test"
        )

    def test_session_context_manager(self, mock_driver, customer_context):
        """Test session as context manager."""
        with CustomerIsolatedSession(mock_driver, customer_context) as session:
            assert session._session is not None

    def test_session_run_adds_filter_params(self, mock_driver, customer_context):
        """Test that run() adds customer filter parameters."""
        with CustomerIsolatedSession(mock_driver, customer_context) as session:
            session.run("MATCH (n) RETURN n", limit=10)

        # Verify session.run was called with customer params
        call_args = mock_driver.session.return_value.run.call_args
        params = call_args[1] if call_args[1] else call_args[0][1] if len(call_args[0]) > 1 else {}

        assert 'customer_id' in params or 'customer_ids' in params


# ============================================================
# SECTION 4: Decorator Tests
# ============================================================

class TestRequireCustomerContext:
    """Tests for require_customer_context decorator."""

    def test_decorator_allows_with_context(self):
        """Test decorator allows execution with context."""
        mock_manager = MagicMock(spec=CustomerContextManager)
        mock_manager.current_context = CustomerContext(
            customer_id="CUST-001",
            namespace="test"
        )

        @require_customer_context
        def test_func(manager: CustomerContextManager):
            return "success"

        result = test_func(mock_manager)
        assert result == "success"

    def test_decorator_raises_without_context(self):
        """Test decorator raises error without context."""
        mock_manager = MagicMock(spec=CustomerContextManager)
        mock_manager.current_context = None

        @require_customer_context
        def test_func(manager: CustomerContextManager):
            return "success"

        with pytest.raises(CustomerIsolationError):
            test_func(mock_manager)


# ============================================================
# SECTION 5: Integration Tests (Mock-based)
# ============================================================

class TestCustomerIsolationIntegration:
    """Integration tests for customer isolation."""

    def test_cross_customer_query_blocked(self):
        """Test that cross-customer data access is blocked."""
        # Create context for CUST-001
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="customer_one",
            include_system=False
        )

        # Verify filter params only allow CUST-001
        manager = CustomerContextManager(MagicMock())
        manager.push_context(context)

        params = manager.get_customer_filter_params()

        # Should not contain any other customer ID
        assert params['customer_ids'] == ["CUST-001"]
        assert "CUST-002" not in params['customer_ids']

    def test_system_data_accessible_when_enabled(self):
        """Test SYSTEM data is accessible when include_system=True."""
        context = CustomerContext(
            customer_id="CUST-001",
            namespace="customer_one",
            include_system=True
        )

        manager = CustomerContextManager(MagicMock())
        manager.push_context(context)

        params = manager.get_customer_filter_params()

        assert "SYSTEM" in params['customer_ids']
        assert "CUST-001" in params['customer_ids']

    def test_audit_logging(self):
        """Test audit logging captures customer access."""
        mock_driver = MagicMock()
        manager = CustomerContextManager(mock_driver, audit_enabled=True)

        context = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
            user_id="user-123",
            session_id="session-abc"
        )
        manager.push_context(context)

        # This should log without error
        manager.audit_access(
            action="READ",
            entity_type="CVE",
            entity_ids=["CVE-2024-0001", "CVE-2024-0002"],
            result_count=2
        )


# ============================================================
# SECTION 6: Query Pattern Tests
# ============================================================

class TestQueryPatterns:
    """Tests for customer query patterns."""

    def test_all_patterns_have_customer_filter(self):
        """Verify all query patterns include customer filtering."""
        for name, query in CUSTOMER_QUERY_PATTERNS.items():
            assert 'customer_id' in query.lower() or '$customer_ids' in query, \
                f"Query pattern '{name}' missing customer filter"

    def test_get_customer_entities_pattern(self):
        """Test get_customer_entities query pattern."""
        pattern = CUSTOMER_QUERY_PATTERNS['get_customer_entities']
        assert 'customer_ids' in pattern
        assert 'LIMIT' in pattern

    def test_get_customer_cves_pattern(self):
        """Test get_customer_cves query pattern."""
        pattern = CUSTOMER_QUERY_PATTERNS['get_customer_cves']
        assert ':CVE' in pattern
        assert 'cvssV3BaseScore' in pattern
        assert 'ORDER BY' in pattern


# ============================================================
# SECTION 7: Access Level Tests
# ============================================================

class TestAccessLevels:
    """Tests for CustomerAccessLevel enum."""

    def test_access_level_values(self):
        """Test all access levels have correct values."""
        assert CustomerAccessLevel.NONE.value == "none"
        assert CustomerAccessLevel.READ.value == "read"
        assert CustomerAccessLevel.WRITE.value == "write"
        assert CustomerAccessLevel.ADMIN.value == "admin"
        assert CustomerAccessLevel.SUPERADMIN.value == "superadmin"

    def test_access_level_comparison(self):
        """Test access level can be used in comparisons."""
        context_read = CustomerContext(
            customer_id="CUST-001",
            namespace="test",
            access_level=CustomerAccessLevel.READ
        )

        context_admin = CustomerContext(
            customer_id="CUST-002",
            namespace="test",
            access_level=CustomerAccessLevel.ADMIN
        )

        assert context_read.access_level != context_admin.access_level


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
