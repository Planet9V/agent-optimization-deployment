# Integration Test Template: {{ENHANCEMENT_ID}} - {{ENHANCEMENT_NAME}}

**Enhancement ID**: {{ENHANCEMENT_ID}}
**Enhancement Name**: {{ENHANCEMENT_NAME}}
**Test Type**: Integration Testing
**Created**: $(date '+%Y-%m-%d')

---

## 1. Cross-Enhancement Compatibility Tests

### 1.1 Enhancement Dependency Validation
```python
import pytest
from neo4j import GraphDatabase

def test_required_enhancements_present(neo4j_session):
    """Verify prerequisite enhancements are installed and operational."""
    required_enhancements = ["E01", "E02", "E10"]  # Customize dependencies

    for enhancement_id in required_enhancements:
        # Check if enhancement nodes/labels exist
        query = f"""
        MATCH (n:Enhancement {{id: '{enhancement_id}'}})
        RETURN count(n) as count
        """
        result = neo4j_session.run(query).single()
        assert result["count"] > 0, f"Required enhancement {enhancement_id} not found"

def test_cross_enhancement_data_integrity(neo4j_session):
    """Verify data relationships between enhancements are valid."""
    # Example: E30 (Temporal) should link properly to E01 (Wikidata) entities
    query = """
    MATCH (e1:Entity)-[:TEMPORAL_LINK]->(e2:WikidataEntity)
    WHERE e1.enhancement_id = '{{ENHANCEMENT_ID}}'
    RETURN count(*) as link_count
    """
    result = neo4j_session.run(query).single()
    link_count = result["link_count"]

    assert link_count > 0, "No cross-enhancement links found"

def test_enhancement_version_compatibility(neo4j_session):
    """Verify enhancement versions are compatible."""
    query = """
    MATCH (e:Enhancement)
    WHERE e.id IN ['E01', 'E02', '{{ENHANCEMENT_ID}}']
    RETURN e.id as id, e.version as version
    """
    results = neo4j_session.run(query)

    versions = {record["id"]: record["version"] for record in results}

    # Add version compatibility checks
    assert versions.get("{{ENHANCEMENT_ID}}") is not None
    # Example: E30 v2.0 requires E01 >= v1.5
    # assert compare_versions(versions["E01"], "1.5") >= 0
```

### 1.2 Shared Resource Access
```python
def test_shared_memory_access():
    """Verify enhancement can access shared memory correctly."""
    from {{KEY_FUNCTIONS}}.memory import get_shared_data, set_shared_data

    # Write to shared memory
    test_data = {"enhancement_id": "{{ENHANCEMENT_ID}}", "status": "active"}
    set_shared_data("test_key", test_data)

    # Read from shared memory
    retrieved_data = get_shared_data("test_key")
    assert retrieved_data == test_data

def test_concurrent_database_access(neo4j_session):
    """Verify multiple enhancements can access database concurrently."""
    import threading
    import time

    def write_operation(session, thread_id):
        query = """
        CREATE (n:TestNode {id: $id, enhancement: '{{ENHANCEMENT_ID}}', thread: $thread})
        """
        session.run(query, id=f"test_{thread_id}", thread=thread_id)

    # Launch concurrent writes
    threads = []
    for i in range(5):
        thread = threading.Thread(target=write_operation, args=(neo4j_session, i))
        threads.append(thread)
        thread.start()

    # Wait for completion
    for thread in threads:
        thread.join()

    # Verify all writes succeeded
    query = "MATCH (n:TestNode {enhancement: '{{ENHANCEMENT_ID}}'}) RETURN count(n) as count"
    result = neo4j_session.run(query).single()
    assert result["count"] == 5
```

---

## 2. API Endpoint Testing

### 2.1 REST API Integration
```python
import requests
import pytest

BASE_URL = "http://localhost:8000/api"  # Adjust to actual API URL

def test_api_health_check():
    """Verify API is running and responsive."""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_enhancement_endpoint_availability():
    """Verify enhancement-specific endpoints are available."""
    endpoints = [
        f"{BASE_URL}/{{ENHANCEMENT_ID}}/entities",
        f"{BASE_URL}/{{ENHANCEMENT_ID}}/query",
        f"{BASE_URL}/{{ENHANCEMENT_ID}}/stats"
    ]

    for endpoint in endpoints:
        response = requests.get(endpoint)
        assert response.status_code in [200, 401], f"Endpoint {endpoint} not available"

def test_entity_retrieval_endpoint():
    """Test entity retrieval through API."""
    response = requests.get(f"{BASE_URL}/{{ENHANCEMENT_ID}}/entities/Q123")

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data
    assert data["enhancement_id"] == "{{ENHANCEMENT_ID}}"

def test_entity_creation_endpoint():
    """Test entity creation through API."""
    new_entity = {
        "id": "TEST_001",
        "name": "Test Entity",
        "type": "Organization",
        "enhancement_id": "{{ENHANCEMENT_ID}}"
    }

    response = requests.post(
        f"{BASE_URL}/{{ENHANCEMENT_ID}}/entities",
        json=new_entity
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "TEST_001"

def test_query_endpoint_performance():
    """Verify query endpoint meets performance requirements."""
    import time

    start = time.time()
    response = requests.get(f"{BASE_URL}/{{ENHANCEMENT_ID}}/query?limit=100")
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 2.0, f"Query took {elapsed:.2f}s (threshold: 2.0s)"
```

### 2.2 GraphQL Integration
```python
def test_graphql_schema_validation():
    """Verify GraphQL schema includes enhancement types."""
    query = """
    {
        __schema {
            types {
                name
            }
        }
    }
    """

    response = requests.post(
        f"{BASE_URL}/graphql",
        json={"query": query}
    )

    assert response.status_code == 200
    types = [t["name"] for t in response.json()["data"]["__schema"]["types"]]
    assert "{{ENHANCEMENT_NAME}}Entity" in types

def test_graphql_entity_query():
    """Test entity retrieval through GraphQL."""
    query = """
    query {
        {{ENHANCEMENT_ID}}Entity(id: "Q123") {
            id
            name
            type
            relationships {
                type
                target
            }
        }
    }
    """

    response = requests.post(
        f"{BASE_URL}/graphql",
        json={"query": query}
    )

    assert response.status_code == 200
    data = response.json()["data"]["{{ENHANCEMENT_ID}}Entity"]
    assert data["id"] == "Q123"
```

---

## 3. Data Flow Validation

### 3.1 End-to-End Data Pipeline
```python
def test_full_ingestion_pipeline(neo4j_session):
    """Test complete data flow from source to database."""
    from {{KEY_FUNCTIONS}}.pipeline import run_full_pipeline

    # Prepare test data
    source_data = [
        {"id": "Q1000", "name": "Test Entity 1"},
        {"id": "Q1001", "name": "Test Entity 2"},
        {"id": "Q1002", "name": "Test Entity 3"}
    ]

    # Run pipeline
    result = run_full_pipeline(source_data)

    assert result["success"] == True
    assert result["processed"] == 3
    assert result["failed"] == 0

    # Verify data in database
    query = """
    MATCH (n:Entity)
    WHERE n.id IN ['Q1000', 'Q1001', 'Q1002']
    RETURN count(n) as count
    """
    db_result = neo4j_session.run(query).single()
    assert db_result["count"] == 3

def test_data_transformation_pipeline():
    """Verify data transformations work correctly in pipeline."""
    from {{KEY_FUNCTIONS}}.pipeline import transform_stage

    input_data = {
        "raw_data": {"wikidata_id": "Q123", "label": "Test"},
        "source": "wikidata"
    }

    output_data = transform_stage(input_data)

    assert "id" in output_data
    assert output_data["id"] == "Q123"
    assert "name" in output_data
    assert output_data["source"] == "wikidata"

def test_error_propagation_in_pipeline():
    """Verify errors are handled correctly throughout pipeline."""
    from {{KEY_FUNCTIONS}}.pipeline import run_full_pipeline

    # Include intentionally malformed data
    mixed_data = [
        {"id": "Q1000", "name": "Valid"},
        {"id": None, "name": "Invalid"},  # Should fail
        {"id": "Q1001", "name": "Valid"}
    ]

    result = run_full_pipeline(mixed_data, continue_on_error=True)

    assert result["processed"] == 2
    assert result["failed"] == 1
    assert len(result["errors"]) == 1
```

### 3.2 Data Consistency Validation
```python
def test_referential_integrity(neo4j_session):
    """Verify referential integrity across related data."""
    # All relationships should point to existing nodes
    query = """
    MATCH (n)-[r]->(m)
    WHERE n.enhancement_id = '{{ENHANCEMENT_ID}}'
    AND NOT EXISTS(m.id)
    RETURN count(r) as broken_links
    """
    result = neo4j_session.run(query).single()
    assert result["broken_links"] == 0, "Found broken relationships"

def test_data_version_consistency(neo4j_session):
    """Verify data version tracking is consistent."""
    query = """
    MATCH (n:Entity {enhancement_id: '{{ENHANCEMENT_ID}}'})
    WHERE n.version IS NULL OR n.last_updated IS NULL
    RETURN count(n) as missing_version
    """
    result = neo4j_session.run(query).single()
    assert result["missing_version"] == 0, "Found entities without version info"

def test_duplicate_prevention(neo4j_session):
    """Verify no duplicate entities were created."""
    query = """
    MATCH (n:Entity {enhancement_id: '{{ENHANCEMENT_ID}}'})
    WITH n.id as entity_id, count(n) as count
    WHERE count > 1
    RETURN collect(entity_id) as duplicates
    """
    result = neo4j_session.run(query).single()
    duplicates = result["duplicates"]
    assert len(duplicates) == 0, f"Found duplicate entities: {duplicates}"
```

---

## 4. Performance Benchmarks

### 4.1 Query Performance Tests
```python
import time
import pytest

def test_single_entity_query_performance(neo4j_session):
    """Verify single entity queries meet performance threshold."""
    query = "MATCH (n:Entity {id: 'Q123'}) RETURN n"

    times = []
    for _ in range(10):
        start = time.time()
        neo4j_session.run(query).single()
        elapsed = time.time() - start
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    assert avg_time < 0.05, f"Average query time {avg_time:.3f}s exceeds 50ms threshold"

def test_complex_traversal_performance(neo4j_session):
    """Verify complex graph traversals meet performance requirements."""
    query = """
    MATCH path = (n:Entity {id: 'Q123'})-[*1..3]->(m)
    RETURN count(path) as paths
    """

    start = time.time()
    result = neo4j_session.run(query).single()
    elapsed = time.time() - start

    assert elapsed < 1.0, f"Traversal took {elapsed:.2f}s (threshold: 1.0s)"
    assert result["paths"] > 0

def test_aggregation_performance(neo4j_session):
    """Verify aggregation queries perform acceptably."""
    query = """
    MATCH (n:Entity {enhancement_id: '{{ENHANCEMENT_ID}}'})
    RETURN count(n) as total,
           collect(distinct n.type) as types,
           avg(size((n)-->())) as avg_connections
    """

    start = time.time()
    neo4j_session.run(query).single()
    elapsed = time.time() - start

    assert elapsed < 2.0, f"Aggregation took {elapsed:.2f}s (threshold: 2.0s)"
```

### 4.2 Scalability Tests
```python
def test_bulk_insert_performance(neo4j_session):
    """Verify bulk insert operations scale linearly."""
    from {{KEY_FUNCTIONS}}.bulk_ops import bulk_insert

    sizes = [100, 500, 1000]
    times = []

    for size in sizes:
        entities = [{"id": f"TEST_{i}", "name": f"Entity {i}"} for i in range(size)]

        start = time.time()
        bulk_insert(neo4j_session, entities)
        elapsed = time.time() - start
        times.append(elapsed)

        # Cleanup
        neo4j_session.run("MATCH (n:Entity) WHERE n.id STARTS WITH 'TEST_' DELETE n")

    # Verify near-linear scaling
    ratio_1 = times[1] / times[0]  # 500 vs 100
    ratio_2 = times[2] / times[1]  # 1000 vs 500

    assert ratio_2 < ratio_1 * 1.5, "Bulk insert doesn't scale linearly"

def test_concurrent_query_performance(neo4j_session):
    """Verify system handles concurrent queries efficiently."""
    import threading

    def run_query(session):
        query = "MATCH (n:Entity {enhancement_id: '{{ENHANCEMENT_ID}}'}) RETURN count(n)"
        session.run(query).single()

    start = time.time()
    threads = [threading.Thread(target=run_query, args=(neo4j_session,)) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    elapsed = time.time() - start

    assert elapsed < 5.0, f"10 concurrent queries took {elapsed:.2f}s (threshold: 5.0s)"
```

### 4.3 Memory and Resource Tests
```python
def test_memory_usage_under_load():
    """Verify memory usage remains acceptable under load."""
    import tracemalloc
    from {{KEY_FUNCTIONS}}.pipeline import run_full_pipeline

    tracemalloc.start()

    # Process large dataset
    large_dataset = [{"id": f"Q{i}", "name": f"Entity {i}"} for i in range(5000)]
    run_full_pipeline(large_dataset)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Memory should stay under 500MB for 5000 entities
    assert peak < 500 * 1024 * 1024, f"Peak memory {peak / 1024 / 1024:.2f}MB exceeds 500MB"

def test_database_connection_pooling():
    """Verify database connection pool is used efficiently."""
    from {{KEY_FUNCTIONS}}.db import get_connection_pool_stats

    # Run multiple operations
    for _ in range(100):
        # Simulate database operations
        pass

    stats = get_connection_pool_stats()

    # Should reuse connections rather than creating new ones
    assert stats["reused"] > stats["created"], "Connection pooling not working efficiently"
```

---

## 5. Integration Configuration

### 5.1 Test Environment Setup
```bash
#!/bin/bash
# setup_integration_tests.sh

echo "Setting up integration test environment for {{ENHANCEMENT_ID}}"

# Start Neo4j test instance
docker run -d \
  --name neo4j-test-{{ENHANCEMENT_ID}} \
  -p 7687:7687 -p 7474:7474 \
  -e NEO4J_AUTH=neo4j/testpassword \
  neo4j:5.15

# Wait for Neo4j to be ready
sleep 10

# Install prerequisite enhancements
python scripts/install_enhancement.py E01
python scripts/install_enhancement.py E02
python scripts/install_enhancement.py E10

# Load test data
python scripts/load_test_data.py --enhancement {{ENHANCEMENT_ID}}

# Start API server
python -m uvicorn api.main:app --port 8000 &
API_PID=$!

echo "Integration test environment ready"
echo "Neo4j: localhost:7687"
echo "API: localhost:8000"
echo "API PID: $API_PID"
```

### 5.2 Cleanup Script
```bash
#!/bin/bash
# cleanup_integration_tests.sh

echo "Cleaning up integration test environment for {{ENHANCEMENT_ID}}"

# Stop API server
pkill -f "uvicorn api.main:app"

# Remove test data
python scripts/cleanup_test_data.py --enhancement {{ENHANCEMENT_ID}}

# Stop and remove Neo4j container
docker stop neo4j-test-{{ENHANCEMENT_ID}}
docker rm neo4j-test-{{ENHANCEMENT_ID}}

echo "Cleanup complete"
```

---

## 6. Integration Test Execution

### 6.1 Running Tests
```bash
# Full integration test suite
pytest tests/integration/test_{{ENHANCEMENT_ID}}_integration.py -v

# With coverage
pytest tests/integration/test_{{ENHANCEMENT_ID}}_integration.py \
    --cov={{KEY_FUNCTIONS}} \
    --cov-report=html

# Performance tests only
pytest tests/integration/test_{{ENHANCEMENT_ID}}_integration.py -k "performance" -v

# API tests only
pytest tests/integration/test_{{ENHANCEMENT_ID}}_integration.py -k "api" -v

# With slow test warnings
pytest tests/integration/test_{{ENHANCEMENT_ID}}_integration.py -v --durations=10
```

### 6.2 CI/CD Configuration
```yaml
# .github/workflows/integration-tests.yml
name: Integration Tests - {{ENHANCEMENT_ID}}

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  integration-test:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    services:
      neo4j:
        image: neo4j:5.15
        env:
          NEO4J_AUTH: neo4j/testpassword
        ports:
          - 7687:7687
          - 7474:7474
        options: >-
          --health-cmd "cypher-shell -u neo4j -p testpassword 'RETURN 1'"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-timeout

      - name: Install prerequisite enhancements
        run: |
          python scripts/install_enhancement.py E01
          python scripts/install_enhancement.py E02

      - name: Load test data
        run: python scripts/load_test_data.py --enhancement {{ENHANCEMENT_ID}}

      - name: Start API server
        run: |
          python -m uvicorn api.main:app --port 8000 &
          sleep 5

      - name: Run integration tests
        env:
          NEO4J_URI: bolt://localhost:7687
          NEO4J_USER: neo4j
          NEO4J_PASSWORD: testpassword
          API_BASE_URL: http://localhost:8000
        run: |
          pytest tests/integration/test_{{ENHANCEMENT_ID}}_integration.py \
            --cov --cov-report=xml --timeout=300

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: integration
          name: {{ENHANCEMENT_ID}}-integration

      - name: Cleanup
        if: always()
        run: python scripts/cleanup_test_data.py --enhancement {{ENHANCEMENT_ID}}
```

---

## 7. Performance Thresholds

**Response Time Requirements**:
- Single entity query: < 50ms (p95)
- Complex traversal (3 hops): < 1s (p95)
- Bulk insert (1000 entities): < 5s
- API endpoint response: < 200ms (p95)
- Aggregation queries: < 2s (p95)

**Throughput Requirements**:
- Queries per second: > 100 QPS
- Entities ingested per minute: > 1000 EPM
- Concurrent users supported: > 50

**Resource Limits**:
- Memory usage: < 2GB under normal load
- Database connections: < 50 concurrent
- CPU usage: < 70% average under load

---

## 8. Test Maintenance

### 8.1 Regular Maintenance Tasks
- [ ] Update test data monthly to reflect schema changes
- [ ] Review performance thresholds quarterly
- [ ] Update API endpoint tests when endpoints change
- [ ] Verify cross-enhancement compatibility after major releases
- [ ] Update dependency versions in test environment
- [ ] Clean up obsolete test data and fixtures

### 8.2 Test Quality Metrics
- Integration test coverage: **≥ 70%**
- API endpoint coverage: **100%**
- Cross-enhancement coverage: **≥ 80%**
- Performance test pass rate: **≥ 95%**
- CI/CD pipeline success rate: **≥ 90%**

---

**Template Version**: 1.0
**Last Updated**: $(date '+%Y-%m-%d')
**Maintained By**: AEON Development Team
