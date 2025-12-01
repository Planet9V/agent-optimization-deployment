---
title: Contributing to NeoCoder (Part 1 of 2)
category: 07_Development
last_updated: 2025-10-25
line_count: 464
status: published
tags: [neocoder, mcp, documentation]
---


# Contributing to NeoCoder

[← Back to Creating Templates](02_Creating_Templates.md) | [Next: Cypher Patterns →](../08_Reference/01_Cypher_Patterns.md)

## Overview

NeoCoder welcomes contributions from the community. This guide covers contribution workflows, coding standards, testing requirements, and review processes.

**Repository**: https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow

## Getting Started

### Development Environment Setup

```bash
# Clone repository
git clone https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow.git
cd NeoCoder-neo4j-ai-workflow

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Install pre-commit hooks
pre-commit install
```

### Database Setup

```bash
# Start Neo4j (Docker)
docker run \
  --name neocoder-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your-password \
  neo4j:latest

# Start Qdrant (Docker)
docker run \
  --name neocoder-qdrant \
  -p 6333:6333 \
  qdrant/qdrant:latest

# Initialize Neo4j schema
python scripts/init_schema.py

# Initialize Qdrant collections
python scripts/init_qdrant.py
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**.env Configuration**:
```bash
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
NEO4J_DATABASE=neo4j

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Optional

# OpenAI (for embeddings)
OPENAI_API_KEY=your-api-key

# MCP Server
MCP_SERVER_NAME=neocoder
MCP_SERVER_VERSION=1.0.0

# Logging
LOG_LEVEL=INFO
LOG_FILE=neocoder.log
```

## Contribution Workflow

### 1. Find or Create Issue

**Browse existing issues**: https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues

**Create new issue**:
```markdown
# Bug Report Template
**Description**: Clear description of the bug
**Steps to Reproduce**: Numbered steps to reproduce
**Expected Behavior**: What should happen
**Actual Behavior**: What actually happens
**Environment**: Python version, OS, Neo4j version, etc.

# Feature Request Template
**Feature Description**: What you want to add
**Use Case**: Why it's needed
**Proposed Implementation**: High-level approach
**Alternatives Considered**: Other possible solutions
```

### 2. Create Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

**Branch Naming Conventions**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or fixes

### 3. Implement Changes

**Code Standards**:
```python
# Follow PEP 8 style guide
# Use type hints
# Write docstrings for all public functions

async def create_entity(
    name: str,
    entity_type: str,
    description: str = ""
) -> Dict[str, Any]:
    """
    Create a new knowledge entity.

    Args:
        name: Entity name
        entity_type: Type of entity
        description: Optional description

    Returns:
        Dict containing entity_id and success status

    Raises:
        ValueError: If parameters are invalid
        DatabaseError: If database operation fails
    """
    pass
```

**Commit Standards**:
```bash
# Use conventional commits format
git commit -m "feat: add hybrid search capability"
git commit -m "fix: resolve Neo4j connection timeout"
git commit -m "docs: update installation guide"
git commit -m "test: add unit tests for F-Contraction"
git commit -m "refactor: simplify tool registration logic"
```

**Commit Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or changes
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `chore:` - Maintenance tasks

### 4. Write Tests

**Test Coverage Requirements**:
- **Minimum**: 80% code coverage for new code
- **Unit Tests**: All new functions and classes
- **Integration Tests**: Database interactions
- **End-to-End Tests**: Complete workflows

**Test Example**:
```python
import pytest
from unittest.mock import AsyncMock, patch

class TestKnowledgeEntityCreation:
    """Test suite for knowledge entity creation."""

    @pytest.mark.asyncio
    async def test_create_entity_success(self):
        """Test successful entity creation."""
        result = await create_knowledge_entity(
            name="Test Entity",
            entity_type="concept",
            description="Test description"
        )

        assert result["success"] is True
        assert "entity_id" in result

    @pytest.mark.asyncio
    async def test_create_entity_invalid_type(self):
        """Test validation error for invalid type."""
        result = await create_knowledge_entity(
            name="Test",
            entity_type="invalid_type"
        )

        assert result["success"] is False
        assert "error" in result

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_create_entity_database(self):
        """Test entity creation with real database."""
        # Requires test Neo4j instance
        result = await create_knowledge_entity(
            name="Integration Test Entity",
            entity_type="concept"
        )

        # Verify in database
        async with get_neo4j_session() as session:
            verify = await session.run("""
                MATCH (e:KnowledgeEntity {id: $id})
                RETURN e
            """, {"id": result["entity_id"]})

            entity = await verify.single()
            assert entity is not None

        # Cleanup
        await cleanup_test_entity(result["entity_id"])
```

**Run Tests**:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=neocoder --cov-report=html

# Run specific test file
pytest tests/test_knowledge_graph.py

# Run specific test
pytest tests/test_knowledge_graph.py::test_create_entity_success

# Run only unit tests
pytest -m "not integration"

# Run only integration tests
pytest -m integration
```

### 5. Update Documentation

**Documentation Requirements**:
- Update relevant wiki pages
- Add docstrings to new functions
- Update API reference
- Include usage examples
- Update changelog

**Example Wiki Update**:
```markdown
# In relevant wiki page

## New Feature: Hybrid Search

The hybrid search capability combines vector similarity with graph traversal
for comprehensive results.

### Usage

\`\`\`python
from neocoder.search import hybrid_search

results = await hybrid_search(
    query_text="neural network architectures",
    limit=10
)
\`\`\`

### Parameters

- `query_text` (str): Natural language search query
- `limit` (int): Maximum results to return

### Returns

Dict containing search results with similarity scores and graph context.
```

### 6. Submit Pull Request

```bash
# Push feature branch
git push origin feature/your-feature-name

# Create pull request on GitHub
# Visit: https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/compare
```

**Pull Request Template**:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Fixes #123

## Changes Made
- Added hybrid search functionality
- Updated knowledge graph tools
- Added integration tests

## Testing
- [x] Unit tests pass
- [x] Integration tests pass
- [x] Coverage > 80%

## Documentation
- [x] Updated wiki pages
- [x] Added docstrings
- [x] Updated API reference

## Checklist
- [x] Code follows style guidelines
- [x] Self-review completed
- [x] Comments added for complex logic
- [x] Documentation updated
- [x] No new warnings generated
- [x] Tests added and passing
```

### 7. Code Review Process

**Review Criteria**:
1. **Code Quality**: Follows standards, well-structured
2. **Testing**: Adequate test coverage, tests passing
3. **Documentation**: Clear documentation and examples
4. **Performance**: No significant performance degradation
5. **Security**: No security vulnerabilities introduced

**Addressing Review Feedback**:
```bash
# Make requested changes
# ... edit files ...

# Commit changes
git add .
git commit -m "fix: address review feedback"

# Push updates
git push origin feature/your-feature-name

# PR automatically updates
```

### 8. Merge and Cleanup

After PR approval:
```bash
# Maintainer merges PR on GitHub
# PR author can delete branch

git checkout main
git pull origin main
git branch -d feature/your-feature-name
```

## Coding Standards

### Python Style Guide

**Follow PEP 8**:
```python
# Good
def calculate_similarity_score(
    vector_a: List[float],
    vector_b: List[float]
) -> float:
    """Calculate cosine similarity between vectors."""
    pass

# Avoid
def calcSim(a,b):
    pass
```

**Type Hints**:
```python
from typing import Dict, List, Optional, Any

# Always use type hints
async def query_graph(
    query: str,
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """Query knowledge graph with filters."""
    pass
```

**Async/Await**:
```python
# Use async for I/O operations
async def fetch_entity(entity_id: str) -> Dict:
    async with get_neo4j_session() as session:
        result = await session.run(
            "MATCH (e:KnowledgeEntity {id: $id}) RETURN e",
            {"id": entity_id}
        )
        return await result.single()
```

### Cypher Style Guide

**Formatting**:
```cypher
// Good: Clear formatting, uppercase keywords
MATCH (source:KnowledgeEntity {id: $source_id})
MATCH (target:KnowledgeEntity {id: $target_id})
CREATE (source)-[r:RELATES_TO {
  type: $relationship_type,
  created: datetime()
}]->(target)
RETURN r

// Avoid: Poor formatting, inconsistent case
match (source {id:$source_id})-[r:RELATES_TO]->(target {id:$target_id}) return r
```

**Performance**:
```cypher
// Good: Use indexes, limit results
MATCH (e:KnowledgeEntity)
WHERE e.domain = $domain
RETURN e
LIMIT 100

// Avoid: Unbound queries
MATCH (e:KnowledgeEntity)
RETURN e
```
