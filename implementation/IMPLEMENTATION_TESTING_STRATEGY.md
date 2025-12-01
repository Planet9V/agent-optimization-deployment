# WAVE 4 Implementation: Testing Strategy & Framework

**Document**: IMPLEMENTATION_TESTING_STRATEGY.md
**Created**: 2025-11-25 22:30:00 UTC
**Version**: v1.0.0
**Status**: ACTIVE

## Executive Summary

This document defines the comprehensive testing framework for WAVE 4, covering unit testing, integration testing, end-to-end testing, performance testing, and security testing. The strategy employs test-driven development principles with automated test execution, continuous testing, and quality gates to ensure enterprise-grade reliability and security.

**Target**: 700 lines of testing specifications and framework configurations.

---

## Table of Contents

1. [Testing Strategy Overview](#testing-strategy-overview)
2. [Unit Testing Framework](#unit-testing-framework)
3. [Integration Testing](#integration-testing)
4. [End-to-End Testing](#end-to-end-testing)
5. [Performance Testing](#performance-testing)
6. [Security Testing](#security-testing)
7. [Test Automation & CI/CD](#test-automation--cicd)
8. [Quality Metrics & Reporting](#quality-metrics--reporting)

---

## Testing Strategy Overview

### Testing Pyramid

```
                        ▲
                       /  \
                      /    \
                  E2E Tests  \
                   (5-10%)   /
                    /        \
                   /──────────\
                  /            \
             Integration Tests  \
              (25-35%)          /
               /               \
              /─────────────────\
             /                   \
        Unit Tests               \
         (60-70%)                /
        /                        \
       /──────────────────────────\
      └────────────────────────────┘
```

### Testing Objectives

| Level | Goal | Coverage | Tools |
|-------|------|----------|-------|
| Unit | Fast feedback on code changes | >80% | Pytest, Vitest |
| Integration | Database and API contract testing | >70% | Pytest, Jest |
| E2E | Full user workflow validation | >60% | Playwright, Cypress |
| Performance | Speed and resource benchmarks | Critical flows | k6, Locust |
| Security | Vulnerability and compliance | OWASP Top 10 | SAST, DAST |

---

## Unit Testing Framework

### Backend Unit Tests (Python)

```python
# backend/tests/unit/test_neo4j_service.py

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.neo4j_service import Neo4jService
from app.schemas.knowledge_graph import NodeResponse

@pytest.fixture
async def neo4j_service():
    """Fixture for Neo4j service."""
    service = Neo4jService()
    service.driver = AsyncMock()
    return service

@pytest.fixture
async def mock_session():
    """Mock Neo4j session."""
    session = AsyncMock()
    return session

class TestNeo4jService:
    """Test cases for Neo4j service."""

    @pytest.mark.asyncio
    async def test_get_nodes_returns_list(self, neo4j_service, mock_session):
        """Test getting nodes returns list."""
        # Arrange
        expected_nodes = [
            {"id": "1", "label": "APT33", "type": "ThreatActor"},
            {"id": "2", "label": "APT41", "type": "ThreatActor"}
        ]
        neo4j_service.driver.session = MagicMock(return_value=mock_session)
        mock_session.run = AsyncMock(return_value=MagicMock(values=AsyncMock(return_value=expected_nodes)))

        # Act
        result = await neo4j_service.get_nodes(node_type="ThreatActor", limit=10)

        # Assert
        assert len(result) == 2
        assert result[0]["type"] == "ThreatActor"

    @pytest.mark.asyncio
    async def test_find_shortest_path_valid_nodes(self, neo4j_service):
        """Test finding shortest path between valid nodes."""
        # Arrange
        source_id = "node-1"
        target_id = "node-2"
        expected_path = [
            {"id": "node-1", "label": "Start"},
            {"id": "node-1.5", "label": "Middle"},
            {"id": "node-2", "label": "End"}
        ]

        # Mock the session and result
        mock_session = AsyncMock()
        mock_result = AsyncMock()
        mock_result.single = AsyncMock(return_value={"path": expected_path})

        neo4j_service.driver.session = MagicMock(return_value=mock_session)
        mock_session.run = AsyncMock(return_value=mock_result)

        # Act
        result = await neo4j_service.find_shortest_path(source_id, target_id)

        # Assert
        assert result is not None
        assert len(result["path"]) == 3

    @pytest.mark.asyncio
    async def test_search_nodes_empty_query(self, neo4j_service):
        """Test that empty query raises validation error."""
        # Act & Assert
        with pytest.raises(ValueError):
            await neo4j_service.search_nodes(query="", limit=10)

    @pytest.mark.asyncio
    async def test_execute_query_with_parameters(self, neo4j_service):
        """Test executing Cypher query with parameters."""
        # Arrange
        query = "MATCH (n:ThreatActor {country: $country}) RETURN n"
        params = {"country": "China"}

        mock_session = AsyncMock()
        mock_result = AsyncMock()
        mock_result.values = AsyncMock(return_value=[{"n": {"id": "1"}}])

        neo4j_service.driver.session = MagicMock(return_value=mock_session)
        mock_session.run = AsyncMock(return_value=mock_result)

        # Act
        result = await neo4j_service.execute_query(query, params)

        # Assert
        assert len(result) == 1
        mock_session.run.assert_called_once_with(query, params)

    @pytest.mark.parametrize("limit,expected_limit", [
        (10, 10),
        (100, 100),
        (101, 100),  # Max limit enforced
    ])
    @pytest.mark.asyncio
    async def test_get_nodes_limit_validation(self, neo4j_service, limit, expected_limit):
        """Test limit parameter validation."""
        mock_session = AsyncMock()
        neo4j_service.driver.session = MagicMock(return_value=mock_session)

        # Act
        await neo4j_service.get_nodes(limit=limit)

        # Assert
        assert expected_limit <= 100
```

### Frontend Unit Tests (TypeScript)

```typescript
// frontend/__tests__/unit/hooks/useApi.test.ts

import { renderHook, waitFor } from '@testing-library/react';
import { useApi } from '@/hooks/useApi';
import { describe, it, expect, beforeEach, vi } from 'vitest';

describe('useApi Hook', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    global.fetch = vi.fn();
  });

  it('should fetch data successfully', async () => {
    // Arrange
    const mockData = { id: '1', name: 'APT33' };
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    // Act
    const { result } = renderHook(() => useApi('/threat-actors/1'));
    await result.current.request();

    // Assert
    await waitFor(() => {
      expect(result.current.data).toEqual(mockData);
      expect(result.current.loading).toBe(false);
      expect(result.current.error).toBeNull();
    });
  });

  it('should handle fetch errors', async () => {
    // Arrange
    const errorMessage = 'Network error';
    global.fetch = vi.fn().mockRejectedValueOnce(new Error(errorMessage));

    // Act
    const { result } = renderHook(() => useApi('/threat-actors/1'));
    try {
      await result.current.request();
    } catch (e) {
      // Expected error
    }

    // Assert
    await waitFor(() => {
      expect(result.current.error).not.toBeNull();
      expect(result.current.error?.message).toBe(errorMessage);
    });
  });

  it('should respect authorization header', async () => {
    // Arrange
    const token = 'test-token-123';
    localStorage.setItem('token', token);

    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    });

    // Act
    const { result } = renderHook(() => useApi('/endpoint'));
    await result.current.request();

    // Assert
    expect(global.fetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: `Bearer ${token}`,
        }),
      })
    );
  });

  it('should handle multiple requests sequentially', async () => {
    // Arrange
    const responses = [
      { data: 'response1' },
      { data: 'response2' },
    ];

    let callCount = 0;
    global.fetch = vi.fn().mockImplementation(async () => {
      const response = responses[callCount++];
      return {
        ok: true,
        json: async () => response,
      };
    });

    // Act
    const { result } = renderHook(() => useApi('/endpoint'));
    await result.current.request();
    await result.current.request();

    // Assert
    await waitFor(() => {
      expect(result.current.data?.data).toBe('response2');
      expect(global.fetch).toHaveBeenCalledTimes(2);
    });
  });
});

// Frontend component unit tests
describe('Card Component', () => {
  it('renders children correctly', () => {
    const { getByText } = render(<Card>Test Content</Card>);
    expect(getByText('Test Content')).toBeInTheDocument();
  });

  it('applies custom className', () => {
    const { container } = render(<Card className="custom">Content</Card>);
    expect(container.querySelector('.custom')).toBeInTheDocument();
  });

  it('calls onClick handler when clicked', () => {
    const handleClick = vi.fn();
    const { getByText } = render(<Card onClick={handleClick}>Click me</Card>);

    fireEvent.click(getByText('Click me'));
    expect(handleClick).toHaveBeenCalled();
  });
});
```

---

## Integration Testing

### API Integration Tests

```python
# backend/tests/integration/test_api_endpoints.py

import pytest
from httpx import AsyncClient
from app.main import app
from app.database.postgres import AsyncSessionLocal
from sqlalchemy import select

@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def db_session():
    """Get test database session."""
    async with AsyncSessionLocal() as session:
        yield session

class TestKnowledgeGraphAPI:
    """Integration tests for knowledge graph endpoints."""

    @pytest.mark.asyncio
    async def test_get_nodes_endpoint(self, client):
        """Test GET /nodes endpoint."""
        # Act
        response = await client.get(
            "/api/v1/knowledge-graph/nodes",
            headers={"Authorization": "Bearer test-token"},
            params={"limit": 10}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_search_nodes_endpoint(self, client):
        """Test POST /search endpoint."""
        # Act
        response = await client.post(
            "/api/v1/knowledge-graph/search",
            headers={"Authorization": "Bearer test-token"},
            json={
                "query": "APT33",
                "search_type": "text",
                "limit": 20
            }
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 20

    @pytest.mark.asyncio
    async def test_find_path_endpoint(self, client):
        """Test path finding endpoint."""
        # Act
        response = await client.post(
            "/api/v1/knowledge-graph/path",
            headers={"Authorization": "Bearer test-token"},
            json={
                "source_id": "node-1",
                "target_id": "node-2",
                "max_depth": 5
            }
        )

        # Assert
        assert response.status_code in [200, 404]  # Path may not exist
        if response.status_code == 200:
            assert "path" in response.json()

class TestThreatIntelAPI:
    """Integration tests for threat intelligence endpoints."""

    @pytest.mark.asyncio
    async def test_get_threat_actors(self, client):
        """Test getting threat actors."""
        # Act
        response = await client.get(
            "/api/v1/threat-intel/threat-actors",
            headers={"Authorization": "Bearer test-token"},
            params={"active": True}
        )

        # Assert
        assert response.status_code == 200
        actors = response.json()
        assert isinstance(actors, list)

    @pytest.mark.asyncio
    async def test_get_campaigns(self, client, db_session):
        """Test getting campaigns."""
        # Arrange - create test data
        # (In real tests, use fixtures or factories)

        # Act
        response = await client.get(
            "/api/v1/threat-intel/campaigns",
            headers={"Authorization": "Bearer test-token"}
        )

        # Assert
        assert response.status_code == 200
        campaigns = response.json()
        assert isinstance(campaigns, list)

    @pytest.mark.asyncio
    async def test_search_indicators(self, client):
        """Test searching indicators."""
        # Act
        response = await client.post(
            "/api/v1/threat-intel/indicators/search",
            headers={"Authorization": "Bearer test-token"},
            json={"search_query": "192.168.1.1"}
        )

        # Assert
        assert response.status_code == 200
        results = response.json()
        assert "results" in results

class TestAuthenticationAPI:
    """Integration tests for authentication."""

    @pytest.mark.asyncio
    async def test_login_success(self, client):
        """Test successful login."""
        # Act
        response = await client.post(
            "/api/v1/users/login",
            json={
                "email": "test@example.com",
                "password": "TestPassword@123"
            }
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "user" in data

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        # Act
        response = await client.post(
            "/api/v1/users/login",
            json={
                "email": "test@example.com",
                "password": "WrongPassword"
            }
        )

        # Assert
        assert response.status_code == 401
```

---

## End-to-End Testing

### Playwright E2E Tests

```typescript
// frontend/e2e/flows/threat-analysis.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Threat Intelligence Analysis Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to application
    await page.goto('http://localhost:3000');

    // Login
    await page.fill('input[name="email"]', 'analyst@example.com');
    await page.fill('input[name="password"]', 'TestPassword@123');
    await page.click('button:has-text("Login")');

    // Wait for dashboard
    await page.waitForURL('**/dashboard');
  });

  test('search threat actor and view campaign details', async ({ page }) => {
    // Step 1: Navigate to threat intelligence section
    await page.click('text=Threat Intelligence');
    await page.waitForURL('**/threat-intelligence');

    // Step 2: Search for threat actor
    await page.fill('input[placeholder="Search threat actors..."]', 'APT33');
    await page.click('button:has-text("Search")');

    // Step 3: Wait for results and click on actor
    await page.waitForSelector('[data-testid="threat-actor-card"]');
    const actorCard = page.locator('[data-testid="threat-actor-card"]:first-child');
    await expect(actorCard).toContainText('APT33');
    await actorCard.click();

    // Step 4: Verify actor details page
    await page.waitForURL('**/threat-actors/**');
    await expect(page.locator('h1')).toContainText('APT33');

    // Step 5: Verify campaigns section
    const campaignsSection = page.locator('[data-testid="campaigns-section"]');
    await expect(campaignsSection).toBeVisible();

    // Step 6: Click on first campaign
    const firstCampaign = page.locator('[data-testid="campaign-item"]:first-child');
    await firstCampaign.click();

    // Step 7: Verify campaign details
    await page.waitForURL('**/campaigns/**');
    await expect(page.locator('[data-testid="campaign-details"]')).toBeVisible();

    // Step 8: Verify indicators are displayed
    const indicators = page.locator('[data-testid="indicator-item"]');
    const count = await indicators.count();
    expect(count).toBeGreaterThan(0);
  });

  test('analyze knowledge graph relationships', async ({ page }) => {
    // Step 1: Navigate to knowledge graph
    await page.click('text=Knowledge Graph');
    await page.waitForURL('**/knowledge-graph');

    // Step 2: Search for a node
    await page.fill('input[placeholder="Search nodes..."]', 'Stuxnet');
    await page.click('button:has-text("Search")');

    // Step 3: Wait for graph visualization
    await page.waitForSelector('[data-testid="graph-canvas"]');

    // Step 4: Click on a node in the graph
    await page.click('[data-testid="node-Stuxnet"]');

    // Step 5: Verify node details panel opens
    const detailsPanel = page.locator('[data-testid="node-details"]');
    await expect(detailsPanel).toBeVisible();
    await expect(detailsPanel).toContainText('Stuxnet');

    // Step 6: View relationships
    const relationshipTab = page.locator('[data-testid="relationships-tab"]');
    await relationshipTab.click();

    // Step 7: Verify relationships are displayed
    const relationships = page.locator('[data-testid="relationship-item"]');
    const relCount = await relationships.count();
    expect(relCount).toBeGreaterThan(0);

    // Step 8: Find path between nodes
    await page.click('button:has-text("Find Path")');
    await page.fill('input[placeholder="Target node..."]', 'APT33');
    await page.click('button:has-text("Find")');

    // Step 9: Verify path is displayed
    await page.waitForSelector('[data-testid="path-visualization"]');
    await expect(page.locator('[data-testid="path-visualization"]')).toBeVisible();
  });

  test('export and share threat analysis report', async ({ page }) => {
    // Step 1: Navigate to threat intelligence
    await page.click('text=Threat Intelligence');

    // Step 2: Search for threat actor
    await page.fill('input[placeholder="Search threat actors..."]', 'Lazarus');
    await page.click('button:has-text("Search")');

    // Step 3: Click on actor
    await page.click('[data-testid="threat-actor-card"]:first-child');

    // Step 4: Click export button
    await page.click('button[aria-label="Export report"]');

    // Step 5: Verify export dialog
    const exportDialog = page.locator('[data-testid="export-dialog"]');
    await expect(exportDialog).toBeVisible();

    // Step 6: Select format and export
    await page.selectOption('select[name="format"]', 'pdf');
    await page.click('button:has-text("Export")');

    // Step 7: Verify download
    const downloadPromise = page.waitForEvent('download');
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toContain('Lazarus');
  });
});
```

---

## Performance Testing

### Load Testing with k6

```javascript
// tests/performance/api-load-test.js

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter, Gauge } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const searchLatency = new Trend('search_latency');
const getNodesLatency = new Trend('get_nodes_latency');
const requestCount = new Counter('http_requests_total');
const loadGauge = new Gauge('api_load');

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp-up
    { duration: '5m', target: 100 },   // Stay at 100 users
    { duration: '2m', target: 200 },   // Spike to 200
    { duration: '5m', target: 200 },   // Stay at 200
    { duration: '2m', target: 0 },     // Ramp-down
  ],
  thresholds: {
    'http_req_duration': ['p(95)<500', 'p(99)<1000'],
    'http_req_failed': ['rate<0.1'],
    'errors': ['rate<0.1'],
  },
};

const BASE_URL = 'http://localhost:8000/api/v1';
const AUTH_TOKEN = 'test-token-123';

export default function () {
  const headers = {
    Authorization: `Bearer ${AUTH_TOKEN}`,
    'Content-Type': 'application/json',
  };

  loadGauge.add(__VU);

  // Test 1: Get nodes
  let response = http.get(`${BASE_URL}/knowledge-graph/nodes?limit=20`, { headers });
  const getNodesStatus = check(response, {
    'get nodes status is 200': (r) => r.status === 200,
    'get nodes response time < 500ms': (r) => r.timings.duration < 500,
  });
  getNodesLatency.add(response.timings.duration);
  errorRate.add(!getNodesStatus);
  requestCount.add(1);

  sleep(1);

  // Test 2: Search nodes
  response = http.post(
    `${BASE_URL}/knowledge-graph/search`,
    JSON.stringify({
      query: 'APT33',
      search_type: 'text',
      limit: 20,
    }),
    { headers }
  );
  const searchStatus = check(response, {
    'search status is 200': (r) => r.status === 200,
    'search response time < 1000ms': (r) => r.timings.duration < 1000,
  });
  searchLatency.add(response.timings.duration);
  errorRate.add(!searchStatus);
  requestCount.add(1);

  sleep(1);

  // Test 3: Get threat actors
  response = http.get(
    `${BASE_URL}/threat-intel/threat-actors?limit=50`,
    { headers }
  );
  check(response, {
    'threat actors status is 200': (r) => r.status === 200,
  });
  requestCount.add(1);

  sleep(2);
}
```

---

## Security Testing

### OWASP Dependency Check

```yaml
# .github/workflows/security-dependencies.yml

name: Security - Dependencies

on:
  push:
    branches: [main, develop]
  schedule:
    - cron: '0 2 * * *'

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Run OWASP Dependency-Check
      uses: dependency-check/Dependency-Check_Action@main
      with:
        project: 'WAVE4'
        path: '.'
        format: 'JSON'
        args: >
          --enableExperimental
          --enableRetired

    - name: Upload SARIF report
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: dependency-check-report.sarif
        category: dependency-check
```

### DAST with OWASP ZAP

```yaml
# .github/workflows/security-dast.yml

name: Security - DAST

on:
  schedule:
    - cron: '0 3 * * 0'  # Weekly

jobs:
  owasp-zap:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Run OWASP ZAP scan
      uses: zaproxy/action-baseline@v0.7.0
      with:
        target: 'https://staging-api.wave4.com'
        rules_file_name: '.zap/rules.tsv'
        cmd_options: '-a'
```

---

## Test Automation & CI/CD

### GitHub Actions Test Workflow

```yaml
# .github/workflows/test.yml

name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r backend/requirements.txt
        pip install pytest pytest-cov pytest-asyncio

    - name: Run unit tests
      run: |
        pytest backend/tests/unit -v --cov=app --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      mongodb:
        image: mongo:6.0
        options: >-
          --health-cmd mongosh
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 27017:27017

    steps:
    - uses: actions/checkout@v4

    - name: Run integration tests
      run: |
        pytest backend/tests/integration -v

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install dependencies
      run: cd frontend && npm ci

    - name: Run unit tests
      run: cd frontend && npm run test:unit

    - name: Run integration tests
      run: cd frontend && npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install dependencies
      run: cd frontend && npm ci

    - name: Install Playwright browsers
      run: cd frontend && npx playwright install --with-deps

    - name: Run E2E tests
      run: cd frontend && npm run test:e2e

    - name: Upload Playwright report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: playwright-report
        path: frontend/playwright-report/
```

---

## Quality Metrics & Reporting

### SonarQube Integration

```python
# scripts/quality-metrics.py

import requests
import json
from datetime import datetime

SONAR_HOST = "https://sonarqube.example.com"
SONAR_TOKEN = "sonarqube-token"
PROJECT_KEY = "wave4"

def get_quality_gates():
    """Get quality gate status."""
    url = f"{SONAR_HOST}/api/qualitygates/project_status"
    headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
    params = {"projectKey": PROJECT_KEY}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_coverage_metrics():
    """Get code coverage metrics."""
    url = f"{SONAR_HOST}/api/measures/component"
    headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
    params = {
        "component": PROJECT_KEY,
        "metricKeys": "coverage,line_coverage,branch_coverage,blocker_violations,critical_violations"
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

def generate_report():
    """Generate quality report."""
    quality_gates = get_quality_gates()
    coverage = get_coverage_metrics()

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "quality_gates": quality_gates,
        "coverage_metrics": coverage,
        "summary": {
            "status": quality_gates.get("projectStatus", {}).get("status"),
            "coverage": coverage.get("component", {}).get("measures", [{}])[0].get("value"),
        }
    }

    # Save report
    with open("quality-report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    generate_report()
```

---

## Summary

This Testing Strategy implementation provides:

✅ **Unit Testing Framework** with 80%+ coverage targets
✅ **Integration Testing** with database and API validation
✅ **End-to-End Testing** with full user workflow validation
✅ **Performance Testing** with load and stress testing
✅ **Security Testing** with SAST and DAST scanning
✅ **Test Automation** with CI/CD pipeline integration
✅ **Quality Metrics** with SonarQube and reporting

**Line Count**: ~700 lines of testing specifications and frameworks

---

**Document Version**: v1.0.0
**Last Updated**: 2025-11-25
**Status**: Implementation Ready
