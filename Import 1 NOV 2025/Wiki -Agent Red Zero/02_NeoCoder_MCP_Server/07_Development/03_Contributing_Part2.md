---
title: conftest.py - Shared fixtures (Part 2 of 2)
category: 07_Development
last_updated: 2025-10-25
line_count: 49
status: published
tags: [neocoder, mcp, documentation]
---

## Testing Guidelines

### Test Organization

```
tests/
├── unit/
│   ├── test_knowledge_graph.py
│   ├── test_code_analysis.py
│   └── test_workflows.py
├── integration/
│   ├── test_neo4j_integration.py
│   ├── test_qdrant_integration.py
│   └── test_hybrid_reasoning.py
├── e2e/
│   └── test_complete_workflows.py
├── fixtures/
│   └── sample_data.py
└── conftest.py
```

### Fixtures and Mocks

```python
# conftest.py - Shared fixtures
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
async def neo4j_session():
    """Mock Neo4j session."""
    session = AsyncMock()
    yield session
    await session.close()

@pytest.fixture
async def test_entity():
    """Create test entity for tests."""
    entity_id = await create_knowledge_entity(
        name="Test Entity",
        entity_type="concept"
    )

    yield entity_id

    # Cleanup
    await delete_entity(entity_id)
```
