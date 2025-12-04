# Acceptance Test Template: {{ENHANCEMENT_ID}} - {{ENHANCEMENT_NAME}}

**Enhancement ID**: {{ENHANCEMENT_ID}}
**Enhancement Name**: {{ENHANCEMENT_NAME}}
**Test Type**: Acceptance Testing
**Created**: $(date '+%Y-%m-%d')

---

## 1. Business Requirement Verification

### 1.1 Requirement Traceability Matrix

| Requirement ID | Description | Test Case ID | Status | McKenney Question Link |
|----------------|-------------|--------------|--------|------------------------|
| REQ-{{ENHANCEMENT_ID}}-001 | Core functionality | AC-001 | ⏳ Pending | MQ-001, MQ-005 |
| REQ-{{ENHANCEMENT_ID}}-002 | Data quality | AC-002 | ⏳ Pending | MQ-002, MQ-008 |
| REQ-{{ENHANCEMENT_ID}}-003 | Performance | AC-003 | ⏳ Pending | MQ-011, MQ-013 |
| REQ-{{ENHANCEMENT_ID}}-004 | Integration | AC-004 | ⏳ Pending | MQ-009, MQ-014 |

### 1.2 Acceptance Criteria Definition
```gherkin
Feature: {{ENHANCEMENT_NAME}} - Core Functionality
  As a AEON system administrator
  I want to {{ENHANCEMENT_DESCRIPTION}}
  So that I can {{BUSINESS_VALUE}}

  Background:
    Given the AEON system is running
    And the Neo4j database is connected
    And enhancement {{ENHANCEMENT_ID}} is installed

  Scenario: AC-001 - Successful entity ingestion
    Given I have a valid data source with 100 entities
    When I execute the ingestion pipeline
    Then all 100 entities should be created in Neo4j
    And each entity should have required properties
    And entities should be linked according to hierarchy
    And the process should complete within 30 seconds

  Scenario: AC-002 - Data quality validation
    Given I have ingested 1000 entities
    When I run the data quality check
    Then there should be no duplicate entities
    And all relationships should be valid
    And all required fields should be populated
    And data freshness should be within 24 hours

  Scenario: AC-003 - Performance under load
    Given the system has 10,000 existing entities
    When I query for specific entity types
    Then response time should be under 100ms
    And the system should handle 50 concurrent queries
    And memory usage should remain under 2GB

  Scenario: AC-004 - Cross-enhancement integration
    Given enhancement E01 (Wikidata) is installed
    When I create {{ENHANCEMENT_NAME}} entities
    Then they should link correctly to Wikidata entities
    And shared properties should be synchronized
    And no data conflicts should occur
```

---

## 2. McKenney Question Coverage

### 2.1 Core McKenney Questions (MQ-001 to MQ-005)

#### MQ-001: What is the basic functionality?
**Acceptance Test**: AC-MQ001
```python
def test_basic_functionality():
    """Verify core enhancement functionality works as described."""
    # Test setup
    from {{KEY_FUNCTIONS}}.core import main_function

    # Execute basic operation
    result = main_function(test_input="sample_data")

    # Verify expected behavior
    assert result["success"] == True
    assert result["entities_processed"] > 0
    assert result["execution_time"] < 5.0  # seconds

    # Verify data was persisted
    query = "MATCH (n:{{NEO4J_LABELS}}) RETURN count(n) as count"
    db_count = neo4j_session.run(query).single()["count"]
    assert db_count == result["entities_processed"]
```

**Success Criteria**:
- [x] Basic functionality executes without errors
- [x] Output matches expected format
- [x] Data is correctly persisted to Neo4j
- [x] Execution completes within time constraints

---

#### MQ-002: How does it handle invalid data?
**Acceptance Test**: AC-MQ002
```python
def test_invalid_data_handling():
    """Verify system handles invalid inputs gracefully."""
    from {{KEY_FUNCTIONS}}.core import main_function

    invalid_inputs = [
        None,
        {},
        {"invalid": "structure"},
        {"id": None, "name": ""},
        {"id": "Q" * 10000}  # Extremely long
    ]

    for invalid_input in invalid_inputs:
        result = main_function(test_input=invalid_input)

        # Should not crash
        assert result is not None
        # Should report error
        assert result["success"] == False
        # Should provide error details
        assert "error" in result
        # Should not corrupt database
        verify_database_integrity()
```

**Success Criteria**:
- [x] System handles malformed data without crashing
- [x] Clear error messages are provided
- [x] Database integrity is maintained
- [x] Partial failures don't corrupt valid data

---

#### MQ-003: What are the data quality metrics?
**Acceptance Test**: AC-MQ003
```python
def test_data_quality_metrics():
    """Verify data quality meets minimum standards."""
    from {{KEY_FUNCTIONS}}.quality import calculate_quality_metrics

    # Ingest test dataset
    test_data = load_test_dataset(size=1000)
    ingest_result = run_ingestion(test_data)

    # Calculate quality metrics
    quality_metrics = calculate_quality_metrics(
        enhancement_id="{{ENHANCEMENT_ID}}"
    )

    # Verify quality thresholds
    assert quality_metrics["completeness"] >= 0.95  # 95% complete
    assert quality_metrics["accuracy"] >= 0.90  # 90% accurate
    assert quality_metrics["consistency"] >= 0.95  # 95% consistent
    assert quality_metrics["timeliness"] >= 0.90  # 90% timely
    assert quality_metrics["duplicates"] == 0  # No duplicates

    # Verify specific quality checks
    assert quality_metrics["missing_required_fields"] == 0
    assert quality_metrics["invalid_relationships"] == 0
    assert quality_metrics["orphaned_nodes"] == 0
```

**Success Criteria**:
- [x] Completeness ≥ 95%
- [x] Accuracy ≥ 90%
- [x] Consistency ≥ 95%
- [x] Zero duplicates
- [x] All required fields populated

---

#### MQ-004: How does it scale?
**Acceptance Test**: AC-MQ004
```python
def test_scalability():
    """Verify system scales to production volumes."""
    from {{KEY_FUNCTIONS}}.core import main_function
    import time

    # Test with increasing data volumes
    volumes = [100, 1000, 10000, 50000]
    results = []

    for volume in volumes:
        test_data = generate_test_data(size=volume)

        start_time = time.time()
        result = main_function(test_input=test_data)
        elapsed = time.time() - start_time

        results.append({
            "volume": volume,
            "time": elapsed,
            "throughput": volume / elapsed
        })

    # Verify linear or sub-linear scaling
    for i in range(1, len(results)):
        ratio = results[i]["time"] / results[i-1]["time"]
        volume_ratio = volumes[i] / volumes[i-1]

        # Time should not grow faster than volume
        assert ratio <= volume_ratio * 1.5, \
            f"Scaling worse than linear: {ratio} vs {volume_ratio}"

    # Verify minimum throughput
    assert results[-1]["throughput"] >= 100, \
        "Throughput below minimum 100 entities/second"
```

**Success Criteria**:
- [x] Handles 50,000+ entities
- [x] Scaling is linear or sub-linear
- [x] Throughput ≥ 100 entities/second
- [x] No memory leaks under load

---

#### MQ-005: What are the dependencies?
**Acceptance Test**: AC-MQ005
```python
def test_dependency_satisfaction():
    """Verify all dependencies are met and functional."""
    from {{KEY_FUNCTIONS}}.dependencies import verify_dependencies

    # Check prerequisite enhancements
    required_enhancements = ["E01", "E02", "E10"]  # Example
    for enhancement_id in required_enhancements:
        assert check_enhancement_installed(enhancement_id), \
            f"Missing required enhancement: {enhancement_id}"

    # Check Python dependencies
    required_packages = [
        "neo4j>=5.15.0",
        "pandas>=2.0.0",
        "requests>=2.31.0"
    ]
    for package in required_packages:
        assert check_package_installed(package), \
            f"Missing required package: {package}"

    # Check external services
    assert check_neo4j_connection(), "Neo4j not accessible"
    assert check_wikidata_api(), "Wikidata API not accessible"

    # Verify dependency versions compatible
    compatibility = verify_dependencies()
    assert compatibility["all_compatible"] == True
    assert len(compatibility["conflicts"]) == 0
```

**Success Criteria**:
- [x] All prerequisite enhancements installed
- [x] All Python packages at correct versions
- [x] External services accessible
- [x] No version conflicts detected

---

### 2.2 Data Quality Questions (MQ-006 to MQ-010)

#### MQ-006: What is the data completeness?
**Acceptance Test**: AC-MQ006
```python
def test_data_completeness():
    """Verify data completeness meets requirements."""
    query = """
    MATCH (n:{{NEO4J_LABELS}})
    RETURN
        count(n) as total,
        count(n.id) as has_id,
        count(n.name) as has_name,
        count(n.type) as has_type,
        count(n.description) as has_description
    """
    result = neo4j_session.run(query).single()

    # Calculate completeness
    total = result["total"]
    completeness = {
        "id": result["has_id"] / total,
        "name": result["has_name"] / total,
        "type": result["has_type"] / total,
        "description": result["has_description"] / total
    }

    # Verify thresholds
    assert completeness["id"] == 1.0  # 100% required
    assert completeness["name"] >= 0.95  # 95% required
    assert completeness["type"] >= 0.90  # 90% required
    assert completeness["description"] >= 0.80  # 80% acceptable
```

---

#### MQ-007: What is the data accuracy?
**Acceptance Test**: AC-MQ007
```python
def test_data_accuracy():
    """Verify data accuracy through sampling validation."""
    from {{KEY_FUNCTIONS}}.validation import validate_entity

    # Sample 100 random entities
    query = """
    MATCH (n:{{NEO4J_LABELS}})
    WITH n, rand() as random
    ORDER BY random
    LIMIT 100
    RETURN n
    """
    sample = neo4j_session.run(query)

    accurate = 0
    total = 0

    for record in sample:
        entity = record["n"]
        # Validate against source of truth
        is_accurate = validate_entity(entity)
        if is_accurate:
            accurate += 1
        total += 1

    accuracy = accurate / total
    assert accuracy >= 0.90, f"Accuracy {accuracy:.2%} below 90% threshold"
```

---

#### MQ-008: How is data freshness maintained?
**Acceptance Test**: AC-MQ008
```python
def test_data_freshness():
    """Verify data freshness meets requirements."""
    from datetime import datetime, timedelta

    query = """
    MATCH (n:{{NEO4J_LABELS}})
    WHERE n.last_updated IS NOT NULL
    RETURN
        n.last_updated as updated,
        datetime() as now
    """
    results = neo4j_session.run(query)

    threshold = timedelta(hours=24)
    stale_count = 0
    total_count = 0

    for record in results:
        updated = datetime.fromisoformat(record["updated"])
        now = datetime.now()
        age = now - updated

        if age > threshold:
            stale_count += 1
        total_count += 1

    freshness = (total_count - stale_count) / total_count
    assert freshness >= 0.90, f"Only {freshness:.2%} of data is fresh (< 24h)"
```

---

### 2.3 Integration Questions (MQ-011 to MQ-015)

#### MQ-011: How does it integrate with existing enhancements?
**Acceptance Test**: AC-MQ011
```python
def test_enhancement_integration():
    """Verify integration with existing enhancements."""
    # Test E01 (Wikidata) integration
    query = """
    MATCH (e1:{{NEO4J_LABELS}})-[r:LINKS_TO]->(e2:WikidataEntity)
    RETURN count(r) as links
    """
    result = neo4j_session.run(query).single()
    assert result["links"] > 0, "No integration with Wikidata entities"

    # Test E02 (Hierarchy) integration
    query = """
    MATCH (e1:{{NEO4J_LABELS}})-[r:HIERARCHY]->(e2)
    RETURN count(r) as hierarchies
    """
    result = neo4j_session.run(query).single()
    assert result["hierarchies"] > 0, "No hierarchical relationships"

    # Verify no data conflicts
    query = """
    MATCH (e1:{{NEO4J_LABELS}})-[r]->(e2)
    WHERE NOT EXISTS(e2.id)
    RETURN count(r) as broken
    """
    result = neo4j_session.run(query).single()
    assert result["broken"] == 0, "Found broken relationships"
```

---

## 3. User Story Completion

### 3.1 Primary User Stories

#### User Story 1: Data Ingestion
```gherkin
As a: Data Administrator
I want: To ingest {{ENHANCEMENT_NAME}} data from external sources
So that: The AEON knowledge graph is enriched with new entity types

Acceptance Criteria:
- [ ] Can specify data source (file, API, database)
- [ ] Ingestion validates data format
- [ ] Progress is reported during ingestion
- [ ] Failed records are logged for review
- [ ] Successful ingestion creates audit trail

Test Implementation:
```python
def test_user_story_data_ingestion():
    """Verify data administrator can ingest data successfully."""
    from {{KEY_FUNCTIONS}}.ingest import IngestManager

    # Initialize ingestion
    manager = IngestManager()

    # Specify data source
    source = manager.add_source(
        type="file",
        path="/data/test_entities.json"
    )
    assert source is not None

    # Execute ingestion with progress tracking
    results = []
    def progress_callback(status):
        results.append(status)

    ingestion = manager.run_ingestion(
        source=source,
        progress_callback=progress_callback
    )

    # Verify progress was reported
    assert len(results) > 0
    assert results[-1]["status"] == "complete"

    # Verify audit trail created
    audit = manager.get_audit_trail(ingestion_id=ingestion["id"])
    assert audit["records_processed"] > 0
    assert "start_time" in audit
    assert "end_time" in audit
```
```

---

#### User Story 2: Entity Query
```gherkin
As a: Research Analyst
I want: To query {{ENHANCEMENT_NAME}} entities by various attributes
So that: I can find relevant information for my analysis

Acceptance Criteria:
- [ ] Can query by ID, name, type, or properties
- [ ] Query results are returned within 2 seconds
- [ ] Results are paginated for large result sets
- [ ] Can export results to CSV/JSON
- [ ] Query history is saved for reuse

Test Implementation:
```python
def test_user_story_entity_query():
    """Verify analyst can query entities effectively."""
    from {{KEY_FUNCTIONS}}.query import QueryEngine

    engine = QueryEngine()

    # Query by ID
    result = engine.query(entity_id="Q123")
    assert result is not None
    assert result["id"] == "Q123"

    # Query by type
    results = engine.query(entity_type="Organization")
    assert len(results) > 0
    assert all(r["type"] == "Organization" for r in results)

    # Verify response time
    import time
    start = time.time()
    engine.query(entity_type="Organization", limit=100)
    elapsed = time.time() - start
    assert elapsed < 2.0, f"Query took {elapsed:.2f}s (threshold: 2.0s)"

    # Verify pagination
    page1 = engine.query(entity_type="Organization", page=1, per_page=10)
    page2 = engine.query(entity_type="Organization", page=2, per_page=10)
    assert page1[0]["id"] != page2[0]["id"]

    # Export results
    export = engine.export(results, format="csv")
    assert export is not None
    assert export.startswith("id,name,type")
```
```

---

#### User Story 3: Relationship Visualization
```gherkin
As a: Knowledge Engineer
I want: To visualize relationships between {{ENHANCEMENT_NAME}} entities
So that: I can understand entity connections and hierarchies

Acceptance Criteria:
- [ ] Can generate graph visualization for entity
- [ ] Visualization shows multiple relationship types
- [ ] Can control depth of relationship traversal
- [ ] Visualization loads within 5 seconds
- [ ] Can export visualization as image

Test Implementation:
```python
def test_user_story_relationship_visualization():
    """Verify engineer can visualize entity relationships."""
    from {{KEY_FUNCTIONS}}.visualization import GraphVisualizer

    viz = GraphVisualizer()

    # Generate visualization
    graph = viz.generate_graph(
        entity_id="Q123",
        depth=2,
        relationship_types=["LINKS_TO", "HIERARCHY"]
    )

    # Verify graph structure
    assert "nodes" in graph
    assert "edges" in graph
    assert len(graph["nodes"]) > 1
    assert len(graph["edges"]) > 0

    # Verify performance
    import time
    start = time.time()
    viz.generate_graph(entity_id="Q123", depth=3)
    elapsed = time.time() - start
    assert elapsed < 5.0, f"Visualization took {elapsed:.2f}s (threshold: 5.0s)"

    # Export capability
    image = viz.export_image(graph, format="png")
    assert image is not None
    assert len(image) > 0
```
```

---

## 4. Documentation Accuracy

### 4.1 Documentation Completeness Checklist

- [ ] **README**: Installation and quick start guide
- [ ] **API Documentation**: All endpoints documented with examples
- [ ] **Data Schema**: Neo4j node/relationship schemas documented
- [ ] **Configuration**: All config options explained
- [ ] **User Guide**: Step-by-step usage instructions
- [ ] **Developer Guide**: Extension and customization guide
- [ ] **Troubleshooting**: Common issues and solutions
- [ ] **Change Log**: Version history and breaking changes

### 4.2 Documentation Validation Tests
```python
def test_documentation_completeness():
    """Verify all required documentation exists and is current."""
    import os
    from datetime import datetime, timedelta

    required_docs = [
        "README.md",
        "docs/API.md",
        "docs/SCHEMA.md",
        "docs/CONFIGURATION.md",
        "docs/USER_GUIDE.md",
        "docs/DEVELOPER_GUIDE.md",
        "docs/TROUBLESHOOTING.md",
        "CHANGELOG.md"
    ]

    for doc in required_docs:
        assert os.path.exists(doc), f"Missing documentation: {doc}"

        # Verify documentation is recent (updated within 90 days)
        mod_time = os.path.getmtime(doc)
        age = datetime.now() - datetime.fromtimestamp(mod_time)
        assert age < timedelta(days=90), f"Documentation outdated: {doc}"

def test_code_example_validity():
    """Verify code examples in documentation actually work."""
    import re

    # Extract code examples from documentation
    with open("README.md") as f:
        content = f.read()

    # Find Python code blocks
    code_blocks = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)

    for i, code in enumerate(code_blocks):
        try:
            # Execute code example
            exec(code)
        except Exception as e:
            pytest.fail(f"Code example {i+1} in README.md fails: {e}")
```

---

## 5. Acceptance Test Execution

### 5.1 Test Execution Script
```bash
#!/bin/bash
# run_acceptance_tests.sh

echo "Running Acceptance Tests for {{ENHANCEMENT_ID}} - {{ENHANCEMENT_NAME}}"
echo "=================================================================="

# Setup test environment
echo "Setting up test environment..."
./scripts/setup_acceptance_env.sh

# Run acceptance tests
echo ""
echo "Running acceptance tests..."
pytest tests/acceptance/test_{{ENHANCEMENT_ID}}_acceptance.py \
    --verbose \
    --html=reports/acceptance_report.html \
    --self-contained-html \
    --junitxml=reports/acceptance_junit.xml

# Generate coverage report
echo ""
echo "Generating coverage report..."
pytest tests/acceptance/test_{{ENHANCEMENT_ID}}_acceptance.py \
    --cov={{KEY_FUNCTIONS}} \
    --cov-report=html:reports/acceptance_coverage

# Cleanup
echo ""
echo "Cleaning up test environment..."
./scripts/cleanup_acceptance_env.sh

# Display results
echo ""
echo "=================================================================="
echo "Acceptance Test Results:"
cat reports/acceptance_junit.xml | grep -o 'tests="[0-9]*"' | cut -d'"' -f2 | xargs echo "Total Tests:"
cat reports/acceptance_junit.xml | grep -o 'failures="[0-9]*"' | cut -d'"' -f2 | xargs echo "Failures:"
cat reports/acceptance_junit.xml | grep -o 'errors="[0-9]*"' | cut -d'"' -f2 | xargs echo "Errors:"
echo ""
echo "Full report: reports/acceptance_report.html"
echo "Coverage report: reports/acceptance_coverage/index.html"
```

### 5.2 CI/CD Integration
```yaml
# .github/workflows/acceptance-tests.yml
name: Acceptance Tests - {{ENHANCEMENT_ID}}

on:
  pull_request:
    types: [labeled]

jobs:
  acceptance:
    # Only run when 'ready-for-acceptance' label is added
    if: contains(github.event.pull_request.labels.*.name, 'ready-for-acceptance')

    runs-on: ubuntu-latest
    timeout-minutes: 60

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run acceptance tests
        run: ./scripts/run_acceptance_tests.sh

      - name: Upload test reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: acceptance-reports
          path: reports/

      - name: Comment PR with results
        if: always()
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('reports/acceptance_summary.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });
```

---

## 6. Acceptance Criteria Summary

### 6.1 Sign-Off Checklist

**Functional Acceptance**:
- [ ] All user stories complete and tested
- [ ] All McKenney questions addressed
- [ ] All business requirements met
- [ ] All acceptance tests pass

**Quality Acceptance**:
- [ ] Data completeness ≥ 95%
- [ ] Data accuracy ≥ 90%
- [ ] Data freshness ≥ 90%
- [ ] Zero critical bugs
- [ ] Performance meets SLAs

**Integration Acceptance**:
- [ ] Integrates with all required enhancements
- [ ] No data conflicts or corruption
- [ ] API endpoints functional
- [ ] Cross-enhancement queries work

**Documentation Acceptance**:
- [ ] All required documentation complete
- [ ] Code examples validated
- [ ] Troubleshooting guide accurate
- [ ] Change log updated

**Operational Acceptance**:
- [ ] Monitoring configured
- [ ] Alerting rules defined
- [ ] Backup/restore tested
- [ ] Rollback procedure documented

### 6.2 Final Sign-Off
```
Enhancement: {{ENHANCEMENT_ID}} - {{ENHANCEMENT_NAME}}
Date: ____________________
Version: __________________

Sign-Off:
___ Product Owner: ________________________________ Date: __________
___ Technical Lead: _______________________________ Date: __________
___ QA Lead: ______________________________________ Date: __________
___ Operations Lead: ______________________________ Date: __________

Status: ⏳ Pending / ✅ Approved / ❌ Rejected

Comments:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

**Template Version**: 1.0
**Last Updated**: $(date '+%Y-%m-%d')
**Maintained By**: AEON Development Team
