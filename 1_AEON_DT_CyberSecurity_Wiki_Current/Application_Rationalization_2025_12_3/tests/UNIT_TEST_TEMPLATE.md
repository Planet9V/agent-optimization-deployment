# Unit Test Template

**Enhancement ID**: {{ENHANCEMENT_ID}}
**Component**: {{COMPONENT_NAME}}
**Date**: {{DATE}}
**Author**: {{AUTHOR}}
**Test Framework**: pytest/unittest

---

## Test Naming Convention

`test_[component]_[scenario]_[expected_outcome]`

**Examples**:
- `test_cypher_query_valid_input_returns_results`
- `test_temporal_filter_invalid_date_raises_error`
- `test_transform_entity_missing_field_uses_default`

---

## 1. Neo4j Cypher Query Tests

### Template Structure
```python
import pytest
from neo4j import GraphDatabase
from {{MODULE_PATH}} import {{QUERY_FUNCTION}}

class TestCypherQueries:
    """Unit tests for Cypher queries in {{ENHANCEMENT_ID}}"""

    @pytest.fixture
    def neo4j_session(self):
        """Mock Neo4j session for testing"""
        # Setup mock or test database connection
        driver = GraphDatabase.driver("bolt://localhost:7687",
                                     auth=("neo4j", "test"))
        session = driver.session()
        yield session
        session.close()
        driver.close()

    def test_{{QUERY_NAME}}_valid_params_returns_results(self, neo4j_session):
        """
        GIVEN: Valid query parameters
        WHEN: {{QUERY_FUNCTION}} is called
        THEN: Returns expected result structure
        """
        # Arrange
        params = {
            "entity_id": "test-001",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31"
        }

        # Act
        result = {{QUERY_FUNCTION}}(neo4j_session, **params)

        # Assert
        assert result is not None
        assert len(result) > 0
        assert "entity_id" in result[0]
        assert result[0]["entity_id"] == params["entity_id"]

    def test_{{QUERY_NAME}}_empty_result_returns_empty_list(self, neo4j_session):
        """
        GIVEN: Query parameters that match no records
        WHEN: {{QUERY_FUNCTION}} is called
        THEN: Returns empty list
        """
        # Arrange
        params = {"entity_id": "nonexistent-999"}

        # Act
        result = {{QUERY_FUNCTION}}(neo4j_session, **params)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    def test_{{QUERY_NAME}}_invalid_params_raises_validation_error(self, neo4j_session):
        """
        GIVEN: Invalid query parameters
        WHEN: {{QUERY_FUNCTION}} is called
        THEN: Raises ValidationError
        """
        # Arrange
        params = {"entity_id": None}  # Invalid parameter

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            {{QUERY_FUNCTION}}(neo4j_session, **params)
        assert "entity_id" in str(exc_info.value)

    def test_{{QUERY_NAME}}_performance_within_threshold(self, neo4j_session):
        """
        GIVEN: Standard query parameters
        WHEN: {{QUERY_FUNCTION}} is called
        THEN: Completes within {{THRESHOLD_MS}}ms
        """
        import time

        # Arrange
        params = {"entity_id": "test-001"}
        threshold_ms = {{THRESHOLD_MS}}

        # Act
        start = time.time()
        result = {{QUERY_FUNCTION}}(neo4j_session, **params)
        duration_ms = (time.time() - start) * 1000

        # Assert
        assert duration_ms < threshold_ms, f"Query took {duration_ms}ms (threshold: {threshold_ms}ms)"
```

---

## 2. Data Transformation Tests

### Template Structure
```python
class TestDataTransformations:
    """Unit tests for data transformation logic"""

    def test_transform_{{ENTITY_TYPE}}_complete_data_returns_valid_structure(self):
        """
        GIVEN: Complete entity data
        WHEN: transform_{{ENTITY_TYPE}} is called
        THEN: Returns valid transformed structure
        """
        # Arrange
        input_data = {
            "id": "ent-001",
            "name": "Test Entity",
            "properties": {"key": "value"},
            "metadata": {"created": "2024-01-01"}
        }

        # Act
        result = transform_{{ENTITY_TYPE}}(input_data)

        # Assert
        assert result["id"] == input_data["id"]
        assert result["name"] == input_data["name"]
        assert "normalized_properties" in result
        assert result["metadata"]["created"] == "2024-01-01"

    def test_transform_{{ENTITY_TYPE}}_missing_optional_field_uses_default(self):
        """
        GIVEN: Entity data missing optional fields
        WHEN: transform_{{ENTITY_TYPE}} is called
        THEN: Uses default values for missing fields
        """
        # Arrange
        input_data = {
            "id": "ent-002",
            "name": "Minimal Entity"
            # Missing optional fields
        }

        # Act
        result = transform_{{ENTITY_TYPE}}(input_data)

        # Assert
        assert result["properties"] == {}  # Default empty dict
        assert "metadata" in result
        assert result["metadata"]["created"] is not None

    def test_transform_{{ENTITY_TYPE}}_malformed_data_raises_error(self):
        """
        GIVEN: Malformed entity data
        WHEN: transform_{{ENTITY_TYPE}} is called
        THEN: Raises DataTransformationError
        """
        # Arrange
        input_data = {"invalid": "structure"}

        # Act & Assert
        with pytest.raises(DataTransformationError):
            transform_{{ENTITY_TYPE}}(input_data)
```

---

## 3. Algorithm Correctness Tests

### Template Structure
```python
class TestAlgorithms:
    """Unit tests for algorithm correctness"""

    def test_{{ALGORITHM_NAME}}_known_input_produces_expected_output(self):
        """
        GIVEN: Known input with verified expected output
        WHEN: {{ALGORITHM_NAME}} is executed
        THEN: Produces exact expected output
        """
        # Arrange
        input_data = [1, 2, 3, 4, 5]
        expected_output = [2, 4, 6, 8, 10]

        # Act
        result = {{ALGORITHM_NAME}}(input_data)

        # Assert
        assert result == expected_output

    def test_{{ALGORITHM_NAME}}_edge_case_empty_input_returns_empty(self):
        """
        GIVEN: Empty input
        WHEN: {{ALGORITHM_NAME}} is executed
        THEN: Returns empty result
        """
        # Arrange
        input_data = []

        # Act
        result = {{ALGORITHM_NAME}}(input_data)

        # Assert
        assert result == []

    def test_{{ALGORITHM_NAME}}_large_dataset_completes_within_time_limit(self):
        """
        GIVEN: Large dataset (10,000+ items)
        WHEN: {{ALGORITHM_NAME}} is executed
        THEN: Completes within {{TIME_LIMIT}}s
        """
        import time

        # Arrange
        input_data = list(range(10000))
        time_limit = {{TIME_LIMIT}}

        # Act
        start = time.time()
        result = {{ALGORITHM_NAME}}(input_data)
        duration = time.time() - start

        # Assert
        assert duration < time_limit
        assert len(result) == len(input_data)
```

---

## 4. API Endpoint Tests

### Template Structure
```python
from fastapi.testclient import TestClient
from {{APP_MODULE}} import app

class TestAPIEndpoints:
    """Unit tests for API endpoints"""

    @pytest.fixture
    def client(self):
        """Test client for API"""
        return TestClient(app)

    def test_get_{{ENDPOINT_NAME}}_valid_id_returns_200(self, client):
        """
        GIVEN: Valid entity ID
        WHEN: GET /{{ENDPOINT_PATH}}/{id} is called
        THEN: Returns 200 with entity data
        """
        # Arrange
        entity_id = "test-001"

        # Act
        response = client.get(f"/{{ENDPOINT_PATH}}/{entity_id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == entity_id
        assert "name" in data

    def test_get_{{ENDPOINT_NAME}}_invalid_id_returns_404(self, client):
        """
        GIVEN: Invalid entity ID
        WHEN: GET /{{ENDPOINT_PATH}}/{id} is called
        THEN: Returns 404 with error message
        """
        # Arrange
        entity_id = "nonexistent-999"

        # Act
        response = client.get(f"/{{ENDPOINT_PATH}}/{entity_id}")

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_post_{{ENDPOINT_NAME}}_valid_data_returns_201(self, client):
        """
        GIVEN: Valid entity data
        WHEN: POST /{{ENDPOINT_PATH}} is called
        THEN: Returns 201 with created entity
        """
        # Arrange
        payload = {
            "name": "New Entity",
            "properties": {"key": "value"}
        }

        # Act
        response = client.post("/{{ENDPOINT_PATH}}", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == payload["name"]
        assert "id" in data
```

---

## 5. Component Isolation Tests (Mocking)

### Template Structure
```python
from unittest.mock import Mock, patch, MagicMock

class TestComponentIsolation:
    """Unit tests with mocked dependencies"""

    @patch('{{MODULE_PATH}}.{{DEPENDENCY_CLASS}}')
    def test_{{COMPONENT}}_isolated_from_database(self, mock_db):
        """
        GIVEN: Component with mocked database dependency
        WHEN: Component method is called
        THEN: Works correctly without real database
        """
        # Arrange
        mock_db.query.return_value = [{"id": "1", "name": "Test"}]
        component = {{COMPONENT_CLASS}}(db=mock_db)

        # Act
        result = component.fetch_data("test-query")

        # Assert
        assert len(result) == 1
        mock_db.query.assert_called_once_with("test-query")

    @patch('{{MODULE_PATH}}.external_api_call')
    def test_{{COMPONENT}}_handles_external_api_failure(self, mock_api):
        """
        GIVEN: External API that fails
        WHEN: Component method is called
        THEN: Handles error gracefully
        """
        # Arrange
        mock_api.side_effect = ConnectionError("API unavailable")
        component = {{COMPONENT_CLASS}}()

        # Act
        result = component.fetch_external_data()

        # Assert
        assert result is None or result == []
        # Component should log error but not crash
```

---

## 6. Error Handling Tests

### Template Structure
```python
class TestErrorHandling:
    """Unit tests for error scenarios"""

    def test_{{FUNCTION_NAME}}_network_timeout_raises_timeout_error(self):
        """
        GIVEN: Network operation that times out
        WHEN: {{FUNCTION_NAME}} is called
        THEN: Raises TimeoutError with clear message
        """
        # Arrange
        with patch('{{MODULE_PATH}}.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout()

            # Act & Assert
            with pytest.raises(TimeoutError) as exc_info:
                {{FUNCTION_NAME}}("http://example.com")
            assert "timeout" in str(exc_info.value).lower()

    def test_{{FUNCTION_NAME}}_invalid_input_returns_error_response(self):
        """
        GIVEN: Invalid input data
        WHEN: {{FUNCTION_NAME}} is called
        THEN: Returns error response with details
        """
        # Arrange
        invalid_input = None

        # Act
        result = {{FUNCTION_NAME}}(invalid_input)

        # Assert
        assert result["status"] == "error"
        assert "error" in result
        assert result["error"]["code"] == "INVALID_INPUT"
```

---

## Coverage Requirements

**Minimum Coverage**: 80%
**Target Coverage**: 90%+

### Coverage by Component Type:
- **Cypher Queries**: 85%+
- **Data Transformations**: 90%+
- **Algorithms**: 95%+
- **API Endpoints**: 80%+
- **Error Handlers**: 100%

### Running Coverage
```bash
pytest --cov={{MODULE_NAME}} --cov-report=html --cov-report=term
```

---

## Assertion Patterns

### Common Assertions
```python
# Existence checks
assert result is not None
assert "key" in result

# Type checks
assert isinstance(result, list)
assert isinstance(result[0], dict)

# Value checks
assert result["status"] == "success"
assert len(result) > 0

# Numeric comparisons
assert result["count"] >= 10
assert 0.0 <= result["score"] <= 1.0

# Error checks
with pytest.raises(SpecificError):
    function_that_should_fail()

# Performance checks
assert duration_ms < threshold_ms
```

---

## Fixtures Setup

```python
@pytest.fixture(scope="module")
def test_database():
    """Module-scoped test database"""
    db = setup_test_db()
    yield db
    teardown_test_db(db)

@pytest.fixture
def sample_data():
    """Sample data for testing"""
    return {
        "entities": [...],
        "relationships": [...]
    }

@pytest.fixture
def mock_config():
    """Mock configuration"""
    return {
        "neo4j_uri": "bolt://localhost:7687",
        "qdrant_url": "http://localhost:6333"
    }
```

---

## Test Execution

```bash
# Run all unit tests
pytest tests/unit/

# Run specific test file
pytest tests/unit/test_{{COMPONENT}}.py

# Run specific test
pytest tests/unit/test_{{COMPONENT}}.py::test_{{SPECIFIC_TEST}}

# Run with verbose output
pytest -v tests/unit/

# Run with coverage
pytest --cov={{MODULE}} tests/unit/
```

---

**Template Version**: 1.0
**Last Updated**: {{DATE}}
**Maintained By**: {{TEAM_NAME}}
