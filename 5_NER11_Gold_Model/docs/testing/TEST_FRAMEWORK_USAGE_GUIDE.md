# AEON Enhancement Test Framework Usage Guide

**Document Version**: 1.0
**Created**: $(date '+%Y-%m-%d')
**Purpose**: Guide for using the comprehensive test framework templates

---

## Overview

The AEON test framework provides four standardized templates for ensuring quality across all enhancements:

1. **Unit Test Template**: Component-level testing
2. **Integration Test Template**: Cross-system testing
3. **Acceptance Test Template**: Business requirement validation
4. **Audit Checklist Template**: Quality and security review

---

## Quick Start

### 1. Setting Up Tests for a New Enhancement

```bash
# Navigate to enhancement directory
cd /path/to/enhancement/{{ENHANCEMENT_ID}}

# Copy templates
cp tests/templates/unit_test_template.md tests/unit/test_{{ENHANCEMENT_ID}}.md
cp tests/templates/integration_test_template.md tests/integration/test_{{ENHANCEMENT_ID}}_integration.md
cp tests/templates/acceptance_test_template.md tests/acceptance/test_{{ENHANCEMENT_ID}}_acceptance.md
cp tests/templates/audit_checklist_template.md tests/audit/{{ENHANCEMENT_ID}}_audit_checklist.md

# Customize templates with your enhancement details
./scripts/customize_test_templates.sh {{ENHANCEMENT_ID}}
```

### 2. Customizing Templates

Replace these placeholder variables in all templates:

| Placeholder | Example Value | Description |
|-------------|---------------|-------------|
| `{{ENHANCEMENT_ID}}` | `E30` | Enhancement identifier |
| `{{ENHANCEMENT_NAME}}` | `Temporal Tracking` | Human-readable name |
| `{{NEO4J_LABELS}}` | `["Entity", "TemporalEvent"]` | Node labels used |
| `{{KEY_FUNCTIONS}}` | `temporal_tracking.core` | Main module path |
| `{{EXPECTED_NODE_COUNT}}` | `10000` | Minimum expected nodes |

---

## Template Usage Details

### Unit Test Template

**Purpose**: Test individual components in isolation

**When to Use**:
- Testing core algorithms
- Validating data transformations
- Verifying Neo4j schema operations
- Checking edge case handling

**Typical Test Structure**:
```python
# 1. Neo4j Schema Validation
def test_node_labels_exist()
def test_relationship_types_exist()

# 2. Data Ingestion
def test_input_data_format_validation()
def test_duplicate_detection()

# 3. Algorithm Correctness
def test_core_algorithm_basic()
def test_algorithm_mathematical_correctness()

# 4. Edge Cases
def test_empty_input_handling()
def test_special_characters_handling()
```

**Running Unit Tests**:
```bash
# Run all unit tests
pytest tests/unit/test_{{ENHANCEMENT_ID}}.py -v

# Run with coverage
pytest tests/unit/test_{{ENHANCEMENT_ID}}.py --cov={{KEY_FUNCTIONS}} --cov-report=html

# Run specific category
pytest tests/unit/test_{{ENHANCEMENT_ID}}.py -k "schema" -v
```

**Coverage Requirements**:
- Overall: ≥ 80%
- Core algorithms: ≥ 95%
- Data transformations: ≥ 90%
- Error handling: ≥ 85%

---

### Integration Test Template

**Purpose**: Test cross-component and cross-system interactions

**When to Use**:
- Testing API endpoints
- Validating cross-enhancement data flow
- Performance benchmarking
- Scalability assessment

**Typical Test Structure**:
```python
# 1. Cross-Enhancement Compatibility
def test_required_enhancements_present()
def test_cross_enhancement_data_integrity()

# 2. API Endpoint Testing
def test_api_health_check()
def test_entity_retrieval_endpoint()

# 3. Data Flow Validation
def test_full_ingestion_pipeline()
def test_data_transformation_pipeline()

# 4. Performance Benchmarks
def test_single_entity_query_performance()
def test_bulk_insert_performance()
```

**Running Integration Tests**:
```bash
# Setup environment first
./scripts/setup_integration_tests.sh

# Run integration tests
pytest tests/integration/test_{{ENHANCEMENT_ID}}_integration.py -v

# Run performance tests only
pytest tests/integration/test_{{ENHANCEMENT_ID}}_integration.py -k "performance" -v

# Cleanup
./scripts/cleanup_integration_tests.sh
```

**Performance Thresholds**:
- Single query: < 50ms (p95)
- Complex traversal: < 1s (p95)
- Bulk insert (1000): < 5s
- API response: < 200ms (p95)

---

### Acceptance Test Template

**Purpose**: Validate business requirements and user stories

**When to Use**:
- Before marking enhancement complete
- For stakeholder sign-off
- Validating McKenney Questions coverage
- User story verification

**Typical Test Structure**:
```gherkin
# 1. Business Requirements
Feature: Core Functionality
  Scenario: Successful entity ingestion
  Scenario: Data quality validation

# 2. McKenney Questions
Test: MQ-001 Basic functionality
Test: MQ-002 Invalid data handling
Test: MQ-003 Data quality metrics

# 3. User Stories
Story: Data administrator ingests data
Story: Analyst queries entities
Story: Engineer visualizes relationships
```

**Running Acceptance Tests**:
```bash
# Run acceptance test suite
./scripts/run_acceptance_tests.sh

# View HTML report
open reports/acceptance_report.html

# Check coverage
open reports/acceptance_coverage/index.html
```

**Acceptance Criteria**:
- All user stories: ✅ Complete
- All McKenney questions: ✅ Addressed
- Business requirements: ✅ Met
- All acceptance tests: ✅ Pass

---

### Audit Checklist Template

**Purpose**: Comprehensive quality and security review

**When to Use**:
- Before production deployment
- For security certification
- Quality gate validation
- Periodic compliance reviews

**Checklist Categories**:

1. **Code Review** (35 points)
   - Structure and organization
   - Readability
   - Documentation
   - Error handling
   - Testing coverage

2. **Security Review** (70 points)
   - OWASP Top 10 compliance
   - Access control
   - Cryptography
   - Injection prevention
   - Vulnerability scanning

3. **Performance** (20 points)
   - Response time thresholds
   - Throughput requirements
   - Resource utilization
   - Scalability assessment

4. **Documentation** (20 points)
   - User documentation
   - Developer documentation
   - Operational documentation
   - Documentation quality

**Conducting Audit**:
```bash
# Generate audit report
python scripts/generate_audit_report.py --enhancement {{ENHANCEMENT_ID}}

# Run security scan
bandit -r src/{{KEY_FUNCTIONS}} -f html -o reports/security_scan.html

# Check dependencies
pip-audit --format=html --output=reports/dependency_audit.html

# Performance profiling
pytest tests/integration/ --profile --profile-svg
```

**Audit Scoring**:
- 37-41/41: ⭐⭐⭐⭐⭐ Excellent (Production ready)
- 32-36/41: ⭐⭐⭐⭐ Good (Minor improvements)
- 27-31/41: ⭐⭐⭐ Acceptable (Significant work needed)
- <27/41: ⭐⭐ Needs Improvement (Not ready)

---

## Best Practices

### 1. Test-Driven Development (TDD)

**Recommended Flow**:
```
1. Write acceptance tests (define "done")
2. Write unit tests (define behavior)
3. Implement code to pass tests
4. Run integration tests
5. Conduct audit review
```

### 2. Continuous Testing

**CI/CD Integration**:
```yaml
# .github/workflows/test-pipeline.yml
stages:
  - name: Unit Tests
    run: pytest tests/unit/ --cov

  - name: Integration Tests
    run: pytest tests/integration/
    requires: [Unit Tests]

  - name: Acceptance Tests
    run: ./scripts/run_acceptance_tests.sh
    requires: [Integration Tests]
    manual: true  # Requires approval

  - name: Security Audit
    run: bandit -r src/ && pip-audit
    requires: [Acceptance Tests]
```

### 3. Test Data Management

**Test Data Strategy**:
- Use fixtures for common test data
- Generate test data programmatically for scale tests
- Clean up test data after each test
- Use separate test database instances
- Document test data requirements

**Example Fixture**:
```python
# conftest.py
@pytest.fixture
def sample_entities():
    """Provide sample entity data for testing."""
    return [
        {"id": "Q1000", "name": "Test Entity 1", "type": "Organization"},
        {"id": "Q1001", "name": "Test Entity 2", "type": "Person"},
        {"id": "Q1002", "name": "Test Entity 3", "type": "Location"}
    ]

@pytest.fixture(scope="session")
def neo4j_test_driver():
    """Create Neo4j driver for entire test session."""
    driver = GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("neo4j", "testpassword")
    )
    yield driver
    driver.close()
```

### 4. Test Maintenance

**Regular Tasks**:
- [ ] Update tests when requirements change
- [ ] Review test coverage monthly
- [ ] Update performance baselines quarterly
- [ ] Refresh test data annually
- [ ] Archive obsolete tests
- [ ] Document test failures and resolutions

---

## Common Patterns

### Pattern 1: Testing Neo4j Queries

```python
def test_neo4j_query_pattern(neo4j_session):
    """Standard pattern for testing Neo4j queries."""
    # 1. Setup: Create test data
    setup_query = """
    CREATE (n:TestNode {id: 'test123', name: 'Test'})
    """
    neo4j_session.run(setup_query)

    # 2. Execute: Run query under test
    query = "MATCH (n:TestNode {id: 'test123'}) RETURN n"
    result = neo4j_session.run(query).single()

    # 3. Verify: Check results
    assert result is not None
    assert result["n"]["name"] == "Test"

    # 4. Cleanup: Remove test data
    cleanup_query = "MATCH (n:TestNode {id: 'test123'}) DELETE n"
    neo4j_session.run(cleanup_query)
```

### Pattern 2: Testing API Endpoints

```python
def test_api_endpoint_pattern():
    """Standard pattern for testing API endpoints."""
    import requests

    # 1. Setup: Prepare request data
    payload = {"id": "Q123", "name": "Test Entity"}

    # 2. Execute: Make API call
    response = requests.post(
        "http://localhost:8000/api/entities",
        json=payload
    )

    # 3. Verify: Check response
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "Q123"

    # 4. Cleanup: Delete created entity
    requests.delete(f"http://localhost:8000/api/entities/{data['id']}")
```

### Pattern 3: Testing Performance

```python
def test_performance_pattern():
    """Standard pattern for testing performance."""
    import time

    # 1. Setup: Prepare test data
    test_data = [{"id": f"Q{i}", "name": f"Entity {i}"} for i in range(1000)]

    # 2. Execute: Time the operation
    start = time.time()
    result = process_entities(test_data)
    elapsed = time.time() - start

    # 3. Verify: Check performance threshold
    assert elapsed < 5.0, f"Processing took {elapsed:.2f}s (threshold: 5.0s)"
    assert result["processed"] == 1000

    # 4. Report: Log performance metrics
    print(f"Throughput: {1000/elapsed:.0f} entities/second")
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Tests Pass Locally but Fail in CI

**Symptoms**: Tests work on development machine but fail in CI/CD pipeline

**Solutions**:
- Check environment variables are set in CI
- Verify database is initialized before tests
- Ensure test data is available
- Check for timezone differences
- Verify Python/package versions match

#### Issue 2: Flaky Integration Tests

**Symptoms**: Tests pass sometimes, fail randomly

**Solutions**:
- Add wait conditions for async operations
- Increase timeouts for slow operations
- Ensure proper test isolation (cleanup)
- Check for race conditions
- Use retry logic for external API calls

#### Issue 3: Slow Test Execution

**Symptoms**: Test suite takes too long to run

**Solutions**:
- Run tests in parallel: `pytest -n auto`
- Use fixtures with appropriate scope (session vs function)
- Mock external dependencies
- Use smaller test datasets
- Profile tests to find bottlenecks

---

## Reference

### Useful Commands

```bash
# Run all tests with coverage
pytest tests/ --cov=src --cov-report=html

# Run tests in parallel
pytest tests/ -n auto

# Run only failed tests
pytest tests/ --lf

# Generate HTML report
pytest tests/ --html=report.html --self-contained-html

# Profile slow tests
pytest tests/ --durations=10

# Run with verbose output
pytest tests/ -vv

# Run specific test
pytest tests/unit/test_E30.py::test_temporal_ingestion -v

# Debug test
pytest tests/unit/test_E30.py::test_temporal_ingestion -vv -s --pdb
```

### pytest Markers

```python
# Mark slow tests
@pytest.mark.slow
def test_large_dataset():
    pass

# Mark integration tests
@pytest.mark.integration
def test_api_integration():
    pass

# Skip test conditionally
@pytest.mark.skipif(not has_neo4j, reason="Neo4j not available")
def test_database():
    pass

# Expected to fail
@pytest.mark.xfail(reason="Known issue #123")
def test_known_bug():
    pass
```

Run marked tests:
```bash
# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Run slow tests only
pytest -m slow
```

---

## Additional Resources

- **pytest Documentation**: https://docs.pytest.org/
- **Neo4j Testing Guide**: https://neo4j.com/docs/python-manual/current/testing/
- **Python Testing Best Practices**: https://realpython.com/pytest-python-testing/
- **OWASP Testing Guide**: https://owasp.org/www-project-web-security-testing-guide/

---

**Document Version**: 1.0
**Last Updated**: $(date '+%Y-%m-%d')
**Maintained By**: AEON Development Team
