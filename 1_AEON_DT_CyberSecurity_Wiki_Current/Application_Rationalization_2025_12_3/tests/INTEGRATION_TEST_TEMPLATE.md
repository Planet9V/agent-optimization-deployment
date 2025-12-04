# Integration Test Template

**Enhancement ID**: {{ENHANCEMENT_ID}}
**Integration Scope**: {{INTEGRATION_SCOPE}}
**Date**: {{DATE}}
**Author**: {{AUTHOR}}
**Test Framework**: pytest + Docker Compose

---

## Test Environment Setup

### Docker Compose Configuration
```yaml
# docker-compose.test.yml
version: '3.8'

services:
  neo4j:
    image: neo4j:5.13.0
    environment:
      NEO4J_AUTH: neo4j/test_password
      NEO4J_PLUGINS: '["apoc", "graph-data-science"]'
    ports:
      - "7687:7687"
      - "7474:7474"
    volumes:
      - ./test-data/neo4j:/data

  qdrant:
    image: qdrant/qdrant:v1.7.0
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./test-data/qdrant:/qdrant/storage

  api:
    build: .
    environment:
      NEO4J_URI: bolt://neo4j:7687
      QDRANT_URL: http://qdrant:6333
      TEST_MODE: "true"
    ports:
      - "8000:8000"
    depends_on:
      - neo4j
      - qdrant
```

### Environment Setup Script
```python
import pytest
import docker
import time
from neo4j import GraphDatabase
from qdrant_client import QdrantClient

@pytest.fixture(scope="session")
def docker_services():
    """Start Docker services for integration tests"""
    client = docker.from_env()
    compose_file = "docker-compose.test.yml"

    # Start services
    client.compose.up(detach=True)

    # Wait for services to be ready
    time.sleep(10)

    yield client

    # Cleanup
    client.compose.down(volumes=True)

@pytest.fixture(scope="session")
def neo4j_driver(docker_services):
    """Neo4j driver for integration tests"""
    driver = GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("neo4j", "test_password")
    )

    # Verify connection
    with driver.session() as session:
        session.run("RETURN 1")

    yield driver
    driver.close()

@pytest.fixture(scope="session")
def qdrant_client(docker_services):
    """Qdrant client for integration tests"""
    client = QdrantClient(url="http://localhost:6333")

    # Verify connection
    client.get_collections()

    yield client
```

---

## 1. Neo4j ↔ Qdrant Integration Tests

### Template Structure
```python
class TestNeo4jQdrantIntegration:
    """Integration tests for Neo4j and Qdrant synchronization"""

    def test_entity_created_in_neo4j_syncs_to_qdrant(self, neo4j_driver, qdrant_client):
        """
        GIVEN: New entity created in Neo4j
        WHEN: Synchronization process runs
        THEN: Entity appears in Qdrant with correct embedding
        """
        # Arrange
        entity_data = {
            "id": "test-ent-001",
            "name": "Test Entity",
            "description": "Integration test entity"
        }

        with neo4j_driver.session() as session:
            # Act - Create entity in Neo4j
            session.run("""
                CREATE (e:Entity {
                    id: $id,
                    name: $name,
                    description: $description,
                    created_at: datetime()
                })
            """, **entity_data)

        # Trigger synchronization
        from {{SYNC_MODULE}} import sync_neo4j_to_qdrant
        sync_neo4j_to_qdrant(entity_data["id"])

        # Assert - Check Qdrant
        points = qdrant_client.retrieve(
            collection_name="{{COLLECTION_NAME}}",
            ids=[entity_data["id"]]
        )

        assert len(points) == 1
        assert points[0].payload["name"] == entity_data["name"]
        assert points[0].vector is not None
        assert len(points[0].vector) == {{EMBEDDING_DIM}}

    def test_entity_updated_in_neo4j_updates_qdrant(self, neo4j_driver, qdrant_client):
        """
        GIVEN: Existing entity in both Neo4j and Qdrant
        WHEN: Entity is updated in Neo4j
        THEN: Qdrant reflects the updated data and embedding
        """
        # Arrange - Create initial entity
        entity_id = "test-ent-002"
        self._create_synced_entity(neo4j_driver, qdrant_client, entity_id)

        # Get initial embedding
        initial_point = qdrant_client.retrieve(
            collection_name="{{COLLECTION_NAME}}",
            ids=[entity_id]
        )[0]
        initial_embedding = initial_point.vector

        # Act - Update entity in Neo4j
        with neo4j_driver.session() as session:
            session.run("""
                MATCH (e:Entity {id: $id})
                SET e.description = $new_desc,
                    e.updated_at = datetime()
            """, id=entity_id, new_desc="Updated description")

        # Trigger synchronization
        from {{SYNC_MODULE}} import sync_neo4j_to_qdrant
        sync_neo4j_to_qdrant(entity_id)

        # Assert
        updated_point = qdrant_client.retrieve(
            collection_name="{{COLLECTION_NAME}}",
            ids=[entity_id]
        )[0]

        assert updated_point.payload["description"] == "Updated description"
        # Embedding should change due to content change
        assert updated_point.vector != initial_embedding

    def test_entity_deleted_in_neo4j_removes_from_qdrant(self, neo4j_driver, qdrant_client):
        """
        GIVEN: Existing entity in both systems
        WHEN: Entity is deleted from Neo4j
        THEN: Entity is removed from Qdrant
        """
        # Arrange
        entity_id = "test-ent-003"
        self._create_synced_entity(neo4j_driver, qdrant_client, entity_id)

        # Act - Delete from Neo4j
        with neo4j_driver.session() as session:
            session.run("MATCH (e:Entity {id: $id}) DELETE e", id=entity_id)

        # Trigger synchronization
        from {{SYNC_MODULE}} import sync_deletions
        sync_deletions()

        # Assert
        points = qdrant_client.retrieve(
            collection_name="{{COLLECTION_NAME}}",
            ids=[entity_id]
        )
        assert len(points) == 0

    def test_bulk_sync_handles_large_dataset(self, neo4j_driver, qdrant_client):
        """
        GIVEN: 1000+ entities in Neo4j
        WHEN: Bulk synchronization is triggered
        THEN: All entities synced within {{TIMEOUT_SECONDS}}s
        """
        import time

        # Arrange - Create bulk entities
        entity_count = 1000
        entity_ids = [f"bulk-{i:04d}" for i in range(entity_count)]

        with neo4j_driver.session() as session:
            session.run("""
                UNWIND $ids AS id
                CREATE (e:Entity {
                    id: id,
                    name: 'Bulk Entity ' + id,
                    created_at: datetime()
                })
            """, ids=entity_ids)

        # Act
        from {{SYNC_MODULE}} import bulk_sync_neo4j_to_qdrant
        start = time.time()
        bulk_sync_neo4j_to_qdrant()
        duration = time.time() - start

        # Assert
        assert duration < {{TIMEOUT_SECONDS}}

        # Verify sync completeness
        collection_info = qdrant_client.get_collection("{{COLLECTION_NAME}}")
        assert collection_info.points_count >= entity_count
```

---

## 2. API ↔ Database Integration Tests

### Template Structure
```python
from fastapi.testclient import TestClient
from {{APP_MODULE}} import app

class TestAPIDatabaseIntegration:
    """Integration tests for API and database layers"""

    @pytest.fixture
    def client(self, neo4j_driver, qdrant_client):
        """API test client with real database connections"""
        # Inject real database connections
        app.state.neo4j_driver = neo4j_driver
        app.state.qdrant_client = qdrant_client
        return TestClient(app)

    def test_create_entity_via_api_persists_to_databases(self, client, neo4j_driver, qdrant_client):
        """
        GIVEN: Valid entity payload
        WHEN: POST /entities is called
        THEN: Entity persists to Neo4j and Qdrant
        """
        # Arrange
        payload = {
            "name": "API Test Entity",
            "entity_type": "Software",
            "description": "Created via API"
        }

        # Act
        response = client.post("/entities", json=payload)

        # Assert API response
        assert response.status_code == 201
        entity_id = response.json()["id"]

        # Assert Neo4j persistence
        with neo4j_driver.session() as session:
            result = session.run(
                "MATCH (e:Entity {id: $id}) RETURN e",
                id=entity_id
            ).single()
            assert result is not None
            assert result["e"]["name"] == payload["name"]

        # Assert Qdrant persistence
        points = qdrant_client.retrieve(
            collection_name="{{COLLECTION_NAME}}",
            ids=[entity_id]
        )
        assert len(points) == 1
        assert points[0].payload["name"] == payload["name"]

    def test_search_entities_via_api_queries_both_databases(self, client, neo4j_driver, qdrant_client):
        """
        GIVEN: Entities in both databases
        WHEN: GET /entities/search is called
        THEN: Returns hybrid results from Neo4j graph + Qdrant vector search
        """
        # Arrange - Seed test data
        self._seed_search_test_data(neo4j_driver, qdrant_client)

        # Act
        response = client.get("/entities/search", params={
            "query": "test entity",
            "limit": 10,
            "hybrid": True
        })

        # Assert
        assert response.status_code == 200
        results = response.json()

        assert "graph_results" in results
        assert "vector_results" in results
        assert "hybrid_score" in results[0]
        assert len(results) <= 10

    def test_transaction_rollback_on_partial_failure(self, client, neo4j_driver, qdrant_client):
        """
        GIVEN: Entity creation that fails at Qdrant stage
        WHEN: POST /entities is called
        THEN: Neo4j transaction is rolled back (atomic operation)
        """
        # Arrange - Mock Qdrant failure
        with patch.object(qdrant_client, 'upsert', side_effect=Exception("Qdrant error")):
            payload = {
                "name": "Rollback Test",
                "entity_type": "Software"
            }

            # Act
            response = client.post("/entities", json=payload)

            # Assert API returns error
            assert response.status_code == 500

            # Assert Neo4j transaction rolled back
            with neo4j_driver.session() as session:
                result = session.run(
                    "MATCH (e:Entity {name: $name}) RETURN count(e) as count",
                    name=payload["name"]
                ).single()
                assert result["count"] == 0
```

---

## 3. Enhancement ↔ Enhancement Integration Tests

### Template Structure
```python
class TestEnhancementIntegration:
    """Integration tests between enhancements"""

    def test_e16_temporal_tracking_integrates_with_e11_relationship_scoring(
        self, neo4j_driver, qdrant_client
    ):
        """
        GIVEN: E16 temporal tracking enabled
        WHEN: E11 relationship scoring runs
        THEN: Scores incorporate temporal decay factors
        """
        # Arrange - Create entities with temporal data
        entity_ids = self._create_temporal_entities(neo4j_driver)

        # Act - Run E11 relationship scoring
        from enhancements.e11 import calculate_relationship_scores
        scores = calculate_relationship_scores(entity_ids)

        # Assert temporal decay applied
        for score_data in scores:
            assert "temporal_score" in score_data
            assert "recency_factor" in score_data
            assert 0.0 <= score_data["temporal_score"] <= 1.0

    def test_e20_neural_embeddings_improve_e09_vector_search(
        self, neo4j_driver, qdrant_client
    ):
        """
        GIVEN: E20 neural embeddings generated
        WHEN: E09 vector search is performed
        THEN: Search results have higher relevance scores
        """
        # Arrange - Generate baseline embeddings (E09)
        baseline_collection = "baseline_embeddings"
        self._create_baseline_embeddings(qdrant_client, baseline_collection)

        # Generate neural embeddings (E20)
        neural_collection = "neural_embeddings"
        from enhancements.e20 import generate_neural_embeddings
        generate_neural_embeddings(qdrant_client, neural_collection)

        # Act - Search both collections
        query = "cybersecurity vulnerability"
        baseline_results = qdrant_client.search(
            collection_name=baseline_collection,
            query_vector=self._get_query_embedding(query),
            limit=10
        )
        neural_results = qdrant_client.search(
            collection_name=neural_collection,
            query_vector=self._get_neural_query_embedding(query),
            limit=10
        )

        # Assert - Neural embeddings have higher average score
        baseline_avg_score = sum(r.score for r in baseline_results) / len(baseline_results)
        neural_avg_score = sum(r.score for r in neural_results) / len(neural_results)

        assert neural_avg_score > baseline_avg_score
        improvement = (neural_avg_score - baseline_avg_score) / baseline_avg_score
        assert improvement >= 0.10  # At least 10% improvement
```

---

## 4. External API Integration Tests

### Template Structure
```python
class TestExternalAPIIntegration:
    """Integration tests with external APIs (NVD, Kaggle)"""

    @pytest.mark.external_api
    def test_nvd_api_integration_fetches_cve_data(self, neo4j_driver):
        """
        GIVEN: Valid CVE ID
        WHEN: NVD API is queried
        THEN: CVE data is fetched and stored in Neo4j
        """
        # Arrange
        cve_id = "CVE-2024-0001"

        # Act
        from integrations.nvd import fetch_and_store_cve
        result = fetch_and_store_cve(neo4j_driver, cve_id)

        # Assert
        assert result["status"] == "success"

        # Verify Neo4j storage
        with neo4j_driver.session() as session:
            cve_node = session.run(
                "MATCH (c:CVE {id: $id}) RETURN c",
                id=cve_id
            ).single()

            assert cve_node is not None
            assert "description" in cve_node["c"]
            assert "severity" in cve_node["c"]

    @pytest.mark.external_api
    @pytest.mark.slow
    def test_kaggle_dataset_integration_imports_security_data(self, neo4j_driver):
        """
        GIVEN: Kaggle dataset configuration
        WHEN: Dataset import is triggered
        THEN: Data is imported and normalized in Neo4j
        """
        # Arrange
        dataset_config = {
            "dataset_id": "security/vulnerabilities",
            "format": "csv",
            "import_batch_size": 1000
        }

        # Act
        from integrations.kaggle import import_dataset
        import_result = import_dataset(neo4j_driver, dataset_config)

        # Assert
        assert import_result["status"] == "success"
        assert import_result["records_imported"] > 0

        # Verify data quality
        with neo4j_driver.session() as session:
            stats = session.run("""
                MATCH (n:SecurityData)
                RETURN count(n) as total,
                       count(DISTINCT n.source) as sources
            """).single()

            assert stats["total"] > 0
            assert stats["sources"] >= 1
```

---

## Data Seeding Procedures

### Seed Script Template
```python
def seed_test_database(neo4j_driver, qdrant_client):
    """Seed test databases with realistic data"""

    # Seed Neo4j
    with neo4j_driver.session() as session:
        session.run("""
            // Create test entities
            UNWIND range(1, 100) AS id
            CREATE (e:Entity {
                id: 'test-' + toString(id),
                name: 'Test Entity ' + toString(id),
                entity_type: CASE id % 3
                    WHEN 0 THEN 'Software'
                    WHEN 1 THEN 'Hardware'
                    ELSE 'Service'
                END,
                created_at: datetime() - duration({days: id})
            })

            // Create relationships
            MATCH (e1:Entity), (e2:Entity)
            WHERE e1.id < e2.id AND rand() < 0.1
            CREATE (e1)-[:RELATED_TO {
                strength: rand(),
                created_at: datetime()
            }]->(e2)
        """)

    # Seed Qdrant
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')

    with neo4j_driver.session() as session:
        entities = session.run("MATCH (e:Entity) RETURN e").data()

    points = []
    for entity in entities:
        text = f"{entity['e']['name']} {entity['e']['entity_type']}"
        embedding = model.encode(text)

        points.append({
            "id": entity['e']['id'],
            "vector": embedding.tolist(),
            "payload": {
                "name": entity['e']['name'],
                "entity_type": entity['e']['entity_type']
            }
        })

    qdrant_client.upsert(
        collection_name="{{COLLECTION_NAME}}",
        points=points
    )

def cleanup_test_database(neo4j_driver, qdrant_client):
    """Clean up test data"""

    # Clean Neo4j
    with neo4j_driver.session() as session:
        session.run("MATCH (n) WHERE n.id STARTS WITH 'test-' DETACH DELETE n")

    # Clean Qdrant
    qdrant_client.delete(
        collection_name="{{COLLECTION_NAME}}",
        points_selector={"filter": {"must": [{"key": "test", "match": {"value": True}}]}}
    )
```

---

## Transaction Management

```python
class TestTransactionManagement:
    """Test transaction handling across systems"""

    def test_distributed_transaction_commits_atomically(self, neo4j_driver, qdrant_client):
        """
        GIVEN: Multi-step operation across Neo4j and Qdrant
        WHEN: All steps succeed
        THEN: All changes are committed atomically
        """
        # Implementation of distributed transaction test
        pass

    def test_distributed_transaction_rolls_back_on_failure(self, neo4j_driver, qdrant_client):
        """
        GIVEN: Multi-step operation that fails midway
        WHEN: Any step fails
        THEN: All changes are rolled back
        """
        # Implementation of rollback test
        pass
```

---

## Performance Benchmarks

```python
class TestPerformanceBenchmarks:
    """Integration performance benchmarks"""

    def test_sync_performance_meets_sla(self, neo4j_driver, qdrant_client):
        """
        GIVEN: 10,000 entities to synchronize
        WHEN: Bulk sync is triggered
        THEN: Completes within {{SLA_SECONDS}}s
        """
        import time

        # Arrange
        entity_count = 10000
        sla_seconds = {{SLA_SECONDS}}

        # Act
        start = time.time()
        from {{SYNC_MODULE}} import bulk_sync
        bulk_sync(neo4j_driver, qdrant_client, entity_count)
        duration = time.time() - start

        # Assert
        assert duration < sla_seconds
        throughput = entity_count / duration
        assert throughput >= {{MIN_THROUGHPUT}}  # entities/sec
```

---

## Test Execution

```bash
# Run all integration tests
pytest tests/integration/ -v

# Run with Docker services
docker-compose -f docker-compose.test.yml up -d
pytest tests/integration/ -v
docker-compose -f docker-compose.test.yml down -v

# Run specific integration suite
pytest tests/integration/test_neo4j_qdrant.py -v

# Run with external API tests (requires API keys)
pytest tests/integration/ -v -m "external_api"

# Skip slow tests
pytest tests/integration/ -v -m "not slow"
```

---

**Template Version**: 1.0
**Last Updated**: {{DATE}}
**Maintained By**: {{TEAM_NAME}}
