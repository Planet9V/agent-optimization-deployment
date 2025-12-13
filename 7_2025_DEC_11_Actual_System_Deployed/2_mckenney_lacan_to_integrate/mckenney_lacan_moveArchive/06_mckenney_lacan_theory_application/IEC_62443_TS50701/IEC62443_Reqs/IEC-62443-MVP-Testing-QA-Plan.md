# IEC 62443 Workshop App – Testing & QA Plan

**Version:** 1.0  
**Status:** Ready for Implementation  
**Date:** December 2024  
**Audience:** QA Engineers, Backend Engineers, Product  

---

## Table of Contents

1. [Testing Strategy Overview](#testing-strategy-overview)
2. [Unit Tests](#unit-tests)
3. [Integration Tests](#integration-tests)
4. [End-to-End Tests](#end-to-end-tests)
5. [Performance Tests](#performance-tests)
6. [Security Tests](#security-tests)
7. [Acceptance Criteria](#acceptance-criteria)
8. [Test Data & Fixtures](#test-data--fixtures)
9. [CI/CD Integration](#cicd-integration)
10. [Test Metrics & Reporting](#test-metrics--reporting)

---

## Testing Strategy Overview

### Testing Pyramid

```
                         ▲
                        /|\
                       / | \
                      /  |  \    E2E Tests (10%)
                     /   |   \   - Full user journeys
                    /    |    \  - Browser automation
                   /     |     \ - API integration
                  ┌──────┼──────┐
                 /       |       \
                /        |        \   Integration Tests (30%)
               /         |         \  - API + DB
              /          |          \ - Service mocks
             /           |           \- Cross-service
            ┌────────────┼────────────┐
           /             |             \
          /              |              \  Unit Tests (60%)
         /               |               \ - Functions
        /                |                \- Components
       /                 |                 \- Utilities
      ┌───────────────────┼───────────────────┐
     /                    |                    \
┌──────────────────────────▼────────────────────────────┐
│        Code Base (Next.js, APIs, DB Queries)        │
└──────────────────────────────────────────────────────┘

Target Coverage:
- Unit: 80%+
- Integration: 70%+
- E2E: Happy path + critical error scenarios
```

### Test Environments

| Environment | Purpose | Data | Duration |
|-------------|---------|------|----------|
| **Local** | Developer testing | Fresh fixtures | Continuous |
| **CI (GitHub Actions)** | Automated on PR | Fixtures + test DB | 15–30 min |
| **Staging** | Pre-production validation | Realistic data | Weekly |
| **Production** | Smoke tests (post-deploy) | Read-only queries | 5 min |

---

## Unit Tests

### Frontend Unit Tests (React Components)

**Technology:** Jest + React Testing Library  
**Location:** `app/src/__tests__/components/`

#### Test Structure

```javascript
// app/src/__tests__/components/LoginForm.test.tsx

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from '@/components/LoginForm';

describe('LoginForm Component', () => {
  
  test('renders login form with email and password fields', () => {
    render(<LoginForm />);
    
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  test('shows validation error when username is empty', async () => {
    const user = userEvent.setup();
    render(<LoginForm />);
    
    const submitButton = screen.getByRole('button', { name: /sign in/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/username is required/i)).toBeInTheDocument();
    });
  });

  test('submits form with valid credentials', async () => {
    const user = userEvent.setup();
    const mockSubmit = jest.fn();
    render(<LoginForm onSubmit={mockSubmit} />);
    
    await user.type(screen.getByLabelText(/username/i), 'admin');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /sign in/i }));
    
    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith({
        username: 'admin',
        password: 'password123'
      });
    });
  });

  test('shows error message on failed login', async () => {
    const user = userEvent.setup();
    const mockSubmit = jest.fn().mockRejectedValue(new Error('Invalid credentials'));
    render(<LoginForm onSubmit={mockSubmit} />);
    
    await user.type(screen.getByLabelText(/username/i), 'admin');
    await user.type(screen.getByLabelText(/password/i), 'wrong');
    await user.click(screen.getByRole('button', { name: /sign in/i }));
    
    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });
  });
});
```

#### Key Components to Test

1. **LoginForm** – Validation, submission, error handling
2. **ProjectList** – Rendering, filtering, sorting, create/edit/delete actions
3. **HARAWizard** – Step navigation, data validation, form submission
4. **ThreatCanvas** – Node/edge creation, deletion, layout, selection
5. **AdminConfigPanel** – Form validation, save/reset, connection testing
6. **SearchPanel** – Query input, result display, conversation threading

#### Coverage Goals

```
Statements   : 80%+
Branches     : 75%+
Functions    : 80%+
Lines        : 80%+
```

---

### Backend Unit Tests (Node.js/Express)

**Technology:** Jest + Supertest  
**Location:** `app/src/__tests__/api/`

#### Test Structure

```javascript
// app/src/__tests__/api/projects.test.ts

import request from 'supertest';
import { app } from '@/app';
import { prisma } from '@/lib/prisma';
import { createMockUser, createMockProject } from '@/__tests__/fixtures';

describe('Projects API', () => {
  let authToken: string;
  let testUser: any;

  beforeAll(async () => {
    testUser = await createMockUser({
      username: 'admin',
      password: 'test123'
    });
  });

  beforeEach(async () => {
    const loginRes = await request(app)
      .post('/api/auth/login')
      .send({ username: 'admin', password: 'test123' });
    
    authToken = loginRes.body.token;
  });

  afterEach(async () => {
    // Clean up test data
    await prisma.projects.deleteMany({ where: { owner_id: testUser.id } });
  });

  describe('POST /api/projects', () => {
    test('creates new project with valid data', async () => {
      const res = await request(app)
        .post('/api/projects')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          name: 'Test Project',
          description: 'A test project',
          location: 'Lab',
          criticality: 'HIGH'
        });
      
      expect(res.status).toBe(201);
      expect(res.body.project).toMatchObject({
        name: 'Test Project',
        criticality: 'HIGH',
        status: 'DRAFT'
      });
      expect(res.body.project.id).toBeDefined();
    });

    test('returns 400 when name is missing', async () => {
      const res = await request(app)
        .post('/api/projects')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ description: 'No name' });
      
      expect(res.status).toBe(400);
      expect(res.body.error).toMatch(/name is required/i);
    });

    test('returns 401 when not authenticated', async () => {
      const res = await request(app)
        .post('/api/projects')
        .send({ name: 'Test' });
      
      expect(res.status).toBe(401);
    });
  });

  describe('GET /api/projects/:id', () => {
    test('returns project with related data', async () => {
      const project = await createMockProject({ owner_id: testUser.id });
      
      const res = await request(app)
        .get(`/api/projects/${project.id}`)
        .set('Authorization', `Bearer ${authToken}`);
      
      expect(res.status).toBe(200);
      expect(res.body.project.id).toBe(project.id);
      expect(res.body.phases).toBeInstanceOf(Array);
      expect(res.body.hara_items).toBeInstanceOf(Array);
    });

    test('returns 404 for non-existent project', async () => {
      const res = await request(app)
        .get('/api/projects/non-existent-id')
        .set('Authorization', `Bearer ${authToken}`);
      
      expect(res.status).toBe(404);
    });
  });

  describe('PATCH /api/projects/:id', () => {
    test('updates project name', async () => {
      const project = await createMockProject({ owner_id: testUser.id });
      
      const res = await request(app)
        .patch(`/api/projects/${project.id}`)
        .set('Authorization', `Bearer ${authToken}`)
        .send({ name: 'Updated Name' });
      
      expect(res.status).toBe(200);
      expect(res.body.project.name).toBe('Updated Name');
    });

    test('returns 403 for non-owner', async () => {
      const otherUser = await createMockUser({ username: 'other' });
      const project = await createMockProject({ owner_id: otherUser.id });
      
      const res = await request(app)
        .patch(`/api/projects/${project.id}`)
        .set('Authorization', `Bearer ${authToken}`)
        .send({ name: 'Hacked' });
      
      expect(res.status).toBe(403);
    });
  });

  describe('DELETE /api/projects/:id', () => {
    test('soft-deletes project', async () => {
      const project = await createMockProject({ owner_id: testUser.id });
      
      const res = await request(app)
        .delete(`/api/projects/${project.id}`)
        .set('Authorization', `Bearer ${authToken}`);
      
      expect(res.status).toBe(200);
      
      // Verify soft delete (not in list, but still in DB)
      const listRes = await request(app)
        .get('/api/projects')
        .set('Authorization', `Bearer ${authToken}`);
      
      expect(listRes.body.projects).not.toContainEqual(
        expect.objectContaining({ id: project.id })
      );
    });
  });
});
```

#### Key APIs to Test

1. **Authentication** – login, logout, token refresh, expiration
2. **Projects** – CRUD, status transitions, ownership
3. **HARA** – item creation, risk calculations, category management
4. **Graph** – node/edge CRUD, persistence, relationship validation
5. **Documents** – upload, ingestion status, entity extraction
6. **AI Features** – threat suggestions, query pipeline, caching
7. **Admin Config** – connection testing, secrets encryption

---

## Integration Tests

**Technology:** Jest + Testcontainers (Docker)  
**Location:** `app/src/__tests__/integration/`

### Database Integration Tests

```javascript
// app/src/__tests__/integration/postgres-neo4j-sync.test.ts

import { startPostgres, startNeo4j } from 'testcontainers';
import { syncNodeToNeo4j } from '@/services/neo4j-sync';
import { createGraphNode } from '@/services/graph';

describe('Postgres → Neo4j Sync', () => {
  let pgClient: any;
  let neo4jDriver: any;

  beforeAll(async () => {
    // Start test containers
    pgClient = await startPostgres({
      image: 'postgres:15-alpine'
    });
    neo4jDriver = await startNeo4j({
      image: 'neo4j:5.13-community'
    });
  });

  afterAll(async () => {
    await pgClient.stop();
    await neo4jDriver.stop();
  });

  test('zone node in postgres syncs to neo4j', async () => {
    // 1. Create zone in Postgres
    const zone = await createGraphNode(pgClient, {
      node_type: 'ZONE',
      label: 'OT Network',
      project_id: 'test-proj-1'
    });

    // 2. Trigger sync
    await syncNodeToNeo4j(neo4jDriver, zone.id);

    // 3. Verify in Neo4j
    const result = await neo4jDriver.run(
      'MATCH (z:Zone {id: $id}) RETURN z',
      { id: zone.id }
    );

    expect(result.records.length).toBe(1);
    expect(result.records[0].get('z').properties.label).toBe('OT Network');
  });

  test('edge creation in postgres syncs to neo4j relationship', async () => {
    // Create nodes
    const zone = await createGraphNode(pgClient, {
      node_type: 'ZONE',
      label: 'Zone A'
    });
    const asset = await createGraphNode(pgClient, {
      node_type: 'ASSET',
      label: 'PLC-01'
    });

    // Create edge
    const edge = await createGraphEdge(pgClient, {
      source_id: zone.id,
      target_id: asset.id,
      edge_type: 'asset-in-zone',
      project_id: 'test-proj-1'
    });

    // Sync
    await syncEdgeToNeo4j(neo4jDriver, edge.id);

    // Verify
    const result = await neo4jDriver.run(`
      MATCH (z:Zone {id: $zoneId})-[:HAS_ASSET]->(a:Asset {id: $assetId})
      RETURN z, a
    `, { zoneId: zone.id, assetId: asset.id });

    expect(result.records.length).toBe(1);
  });
});
```

### API Integration Tests

```javascript
// app/src/__tests__/integration/hara-workflow.test.ts

describe('HARA Workflow (End-to-End Integration)', () => {
  test('complete HARA workflow from SuC to risk calculation', async () => {
    const user = await createTestUser();
    const project = await createTestProject(user.id);
    
    // Step 1: Create System Under Consideration
    const sucRes = await request(app)
      .post(`/api/projects/${project.id}/hara/suc`)
      .set('Authorization', `Bearer ${getToken(user)}`)
      .send({
        name: 'Tunnel Control System',
        description: 'IEC 62443 assessment',
        location: 'Underground',
        criticality: 'HIGH'
      });
    expect(sucRes.status).toBe(201);

    // Step 2: Create Impact Categories
    const cat1 = await request(app)
      .post(`/api/projects/${project.id}/hara/categories`)
      .set('Authorization', `Bearer ${getToken(user)}`)
      .send({
        name: 'Safety',
        severity_scale: {
          1: 'Negligible',
          2: 'Minor',
          3: 'Moderate',
          4: 'Major',
          5: 'Catastrophic'
        }
      });
    expect(cat1.status).toBe(201);

    const cat2 = await request(app)
      .post(`/api/projects/${project.id}/hara/categories`)
      .set('Authorization', `Bearer ${getToken(user)}`)
      .send({
        name: 'Environmental',
        severity_scale: {
          1: 'Negligible',
          2: 'Minor',
          3: 'Moderate',
          4: 'Major',
          5: 'Catastrophic'
        }
      });
    expect(cat2.status).toBe(201);

    // Step 3: Add HARA Items
    const item1 = await request(app)
      .post(`/api/projects/${project.id}/hara/items`)
      .set('Authorization', `Bearer ${getToken(user)}`)
      .send({
        name: 'Ventilation System',
        description: 'Primary air exchange',
        impact_ratings: {
          [cat1.body.category.id]: 5,  // Catastrophic safety impact
          [cat2.body.category.id]: 3   // Moderate environmental impact
        }
      });
    expect(item1.status).toBe(201);
    expect(item1.body.hara_item.calculated_risk_level).toBe('CRITICAL');

    const item2 = await request(app)
      .post(`/api/projects/${project.id}/hara/items`)
      .set('Authorization', `Bearer ${getToken(user)}`)
      .send({
        name: 'Electrical System',
        description: 'Power distribution',
        impact_ratings: {
          [cat1.body.category.id]: 3,  // Moderate safety impact
          [cat2.body.category.id]: 2   // Minor environmental impact
        }
      });
    expect(item2.status).toBe(201);
    expect(item2.body.hara_item.calculated_risk_level).toBe('MEDIUM');

    // Step 4: Verify HARA summary
    const haraSummary = await request(app)
      .get(`/api/projects/${project.id}/hara`)
      .set('Authorization', `Bearer ${getToken(user)}`);
    
    expect(haraSummary.status).toBe(200);
    expect(haraSummary.body.hara_items).toHaveLength(2);
    expect(haraSummary.body.hara_items[0].calculated_risk_level).toBe('CRITICAL');
    expect(haraSummary.body.hara_items[1].calculated_risk_level).toBe('MEDIUM');
  });
});
```

### Qdrant Integration Tests

```javascript
// app/src/__tests__/integration/qdrant-search.test.ts

describe('Qdrant Vector Search', () => {
  test('semantic search returns relevant results', async () => {
    // Pre-populate Qdrant with test vectors
    await qdrant.upsertPoints('project_docs', {
      points: [
        {
          id: 1,
          vector: await encode('The SCADA system controls critical infrastructure'),
          payload: { text: 'SCADA systems', doc_id: 'doc-1' }
        },
        {
          id: 2,
          vector: await encode('PLC devices execute control logic'),
          payload: { text: 'PLC devices', doc_id: 'doc-2' }
        },
        {
          id: 3,
          vector: await encode('The weather is sunny today'),  // Unrelated
          payload: { text: 'Weather report', doc_id: 'doc-3' }
        }
      ]
    });

    // Search for "control system"
    const query = await encode('control system');
    const results = await qdrant.search('project_docs', {
      vector: query,
      limit: 2
    });

    expect(results.result).toHaveLength(2);
    expect(results.result[0].payload.text).toMatch(/SCADA|PLC/);
    expect(results.result[0].score).toBeGreaterThan(0.8);  // High similarity
  });
});
```

---

## End-to-End Tests

**Technology:** Playwright + Docker Compose  
**Location:** `e2e/`

### Happy Path E2E Test

```typescript
// e2e/workflows/complete-hara-workshop.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Complete HARA Workshop Workflow', () => {
  let page: Page;

  test.beforeAll(async ({ browser }) => {
    page = await browser.newPage();
    // Wait for app to be ready
    await page.waitForURL('https://localhost');
  });

  test('should complete HARA assessment from login to export', async () => {
    // 1. Login
    await page.goto('https://localhost/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('https://localhost/projects');

    // 2. Create project
    await page.click('button:has-text("New Project")');
    await page.fill('input[name="name"]', 'Tunnel Control System');
    await page.fill('input[name="location"]', 'Underground Facility');
    await page.selectOption('select[name="criticality"]', 'HIGH');
    await page.click('button:has-text("Create")');
    await page.waitForSelector('text=Tunnel Control System');

    // 3. Start HARA wizard
    await page.click('text=Scoping & HARA');
    await page.click('button:has-text("Start HARA")');

    // Step 1: System Under Consideration
    await page.fill('input[name="suc_name"]', 'Tunnel Ventilation System');
    await page.fill('textarea[name="suc_description"]', 'Primary HVAC for tunnel');
    await page.click('button:has-text("Next")');

    // Step 2: Impact Categories
    await page.click('button:has-text("Use Preset: Safety/Environmental/Financial")');
    await page.click('button:has-text("Next")');

    // Step 3: Upload Document
    const filePath = './test-data/RAMS_Sample.pdf';
    await page.setInputFiles('input[type="file"]', filePath);
    await page.waitForText('Ingestion complete');
    await page.click('button:has-text("Next")');

    // Step 4: HARA Workshop Table
    await page.click('button:has-text("Suggest from Documents")');
    await page.waitForSelector('table tbody tr');
    
    const rows = await page.$$('table tbody tr');
    expect(rows.length).toBeGreaterThan(0);
    
    // Add manual row
    await page.click('button:has-text("Add Item")');
    await page.fill('input[name="item_name"]', 'Electrical Subsystem');
    await page.fill('input[name="item_description"]', 'Power distribution for ventilation');
    await page.selectOption('select[name="safety_impact"]', '3');
    await page.selectOption('select[name="environmental_impact"]', '2');
    await page.click('button:has-text("Add")');

    // Submit phase
    await page.click('button:has-text("Submit for Review")');
    await page.waitForText('Phase submitted');

    // 4. Verify Threat Canvas is enabled
    await page.click('text=Zones & Threats');
    await page.waitForSelector('[data-testid="react-flow-canvas"]');

    // Create a zone
    await page.click('button:has-text("Add Zone")');
    await page.click('[data-testid="react-flow-canvas"]', { position: { x: 200, y: 200 } });
    await page.fill('input[name="zone_label"]', 'OT Network');
    await page.click('button:has-text("Create")');

    // Create an asset
    await page.click('button:has-text("Add Asset")');
    await page.click('[data-testid="react-flow-canvas"]', { position: { x: 400, y: 200 } });
    await page.fill('input[name="asset_label"]', 'PLC-01');
    await page.selectOption('select[name="asset_type"]', 'PLC');
    await page.click('button:has-text("Create")');

    // Connect zone to asset
    await page.click('[data-testid="node-zone-0"]');
    await page.keyboard.press('Shift');
    await page.click('[data-testid="node-asset-1"]');
    await page.click('button:has-text("Connect")');

    // 5. Test AI Search
    await page.click('text=AI Search');
    await page.fill('input[name="ai_query"]', 'What are threats to PLC systems?');
    await page.click('button:has-text("Ask")');
    await page.waitForText(/threat|attack|mitigation/i);

    // 6. Export project
    await page.click('button:has-text("Export")');
    await page.waitForEvent('popup');

    // Verify audit log
    await page.click('text=Admin');
    await page.click('text=Audit Log');
    await page.waitForSelector('table');
    
    const auditRows = await page.$$('table tbody tr');
    expect(auditRows.length).toBeGreaterThan(0);
  });
});
```

### Error Scenario E2E Tests

```typescript
// e2e/workflows/error-scenarios.spec.ts

test.describe('Error Handling', () => {
  test('should show validation error for missing required fields', async ({ page }) => {
    await page.goto('https://localhost/');
    await loginAs(page, 'admin', 'admin123');
    
    await page.click('button:has-text("New Project")');
    await page.click('button:has-text("Create")');  // No data filled
    
    expect(await page.isVisible('text=Project name is required')).toBeTruthy();
  });

  test('should handle document upload failure gracefully', async ({ page }) => {
    await setupProject(page);
    
    // Attempt upload with invalid file
    await page.setInputFiles('input[type="file"]', './test-data/invalid.txt');
    await page.waitForText(/unsupported file type|failed/i);
    
    expect(await page.isVisible('[role="alert"]')).toBeTruthy();
  });

  test('should show timeout when AI query takes too long', async ({ page }) => {
    // Mock slow LLM response
    await page.route('**/api/ai/query', async (route) => {
      await new Promise(r => setTimeout(r, 15000));  // 15 sec timeout
      route.abort('timedout');
    });

    await page.click('text=AI Search');
    await page.fill('input[name="ai_query"]', 'test query');
    await page.click('button:has-text("Ask")');
    
    await page.waitForText(/timeout|please try again/i);
  });
});
```

---

## Performance Tests

**Technology:** k6 (load testing)  
**Location:** `tests/performance/`

### Load Test Script

```javascript
// tests/performance/api-load-test.js

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

const loginTrend = new Trend('login_duration');
const projectTrend = new Trend('create_project_duration');
const graphTrend = new Trend('graph_node_duration');
const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '30s', target: 5 },   // Ramp up to 5 users
    { duration: '1m30s', target: 10 }, // Ramp to 10 users
    { duration: '20s', target: 0 }    // Ramp down to 0 users
  ],
  thresholds: {
    'login_duration': ['p(95)<500'],        // 95th percentile < 500ms
    'create_project_duration': ['p(95)<1000'],
    'graph_node_duration': ['p(95)<200'],
    'errors': ['rate<0.1']  // Error rate < 10%
  }
};

let authToken = '';

export default function () {
  // 1. Login
  const loginRes = http.post('https://localhost/api/auth/login', {
    username: `admin-${__VU}`,
    password: 'test123'
  });
  
  check(loginRes, {
    'login status 200': (r) => r.status === 200
  }) || errorRate.add(1);
  
  loginTrend.add(loginRes.timings.duration);
  
  if (loginRes.status === 200) {
    authToken = loginRes.json('token');
  }
  
  sleep(1);

  // 2. Create project
  const params = { headers: { 'Authorization': `Bearer ${authToken}` } };
  const projectRes = http.post('https://localhost/api/projects', {
    name: `Load Test Project ${__VU}-${__ITER}`,
    criticality: 'HIGH'
  }, params);
  
  check(projectRes, {
    'create project status 201': (r) => r.status === 201
  }) || errorRate.add(1);
  
  projectTrend.add(projectRes.timings.duration);
  
  const projectId = projectRes.json('project.id');
  sleep(1);

  // 3. Add graph nodes (simulating threat canvas)
  for (let i = 0; i < 5; i++) {
    const nodeRes = http.post(
      `https://localhost/api/projects/${projectId}/graph/nodes`,
      {
        node_type: 'ASSET',
        label: `Asset-${__VU}-${i}`
      },
      params
    );
    
    check(nodeRes, {
      'create node status 201': (r) => r.status === 201
    }) || errorRate.add(1);
    
    graphTrend.add(nodeRes.timings.duration);
    sleep(0.5);
  }

  sleep(5);
}

export function teardown(data) {
  console.log('Load test complete');
}
```

### Run Performance Test

```bash
# Local k6 test
k6 run tests/performance/api-load-test.js

# Docker k6 test
docker run -i grafana/k6 run - < tests/performance/api-load-test.js

# With output to file
k6 run --out csv=results.csv tests/performance/api-load-test.js
```

### Performance Baselines

**Target metrics (MVP):**

| Operation | Target (p95) | Threshold |
|-----------|--------------|-----------|
| Login | <500 ms | OK |
| Create project | <1000 ms | OK |
| Add graph node | <200 ms | OK |
| Graph render (100 nodes) | <500 ms | OK |
| AI query | <10 sec | OK |
| Document upload (10 MB PDF) | <15 sec | OK |

---

## Security Tests

### OWASP Top 10 Test Cases

```javascript
// tests/security/owasp-top10.test.ts

describe('OWASP Top 10 Security Tests', () => {
  
  // A01: Broken Access Control
  test('should not allow user to access other users projects', async () => {
    const user1Project = await createTestProject({ owner_id: user1.id });
    
    const res = await request(app)
      .get(`/api/projects/${user1Project.id}`)
      .set('Authorization', `Bearer ${user2Token}`);
    
    expect(res.status).toBe(403);
  });

  // A02: Cryptographic Failures
  test('should encrypt sensitive config values', async () => {
    const configValue = 'sk-secret-api-key';
    await setConfig('openrouter_api_key', configValue, true);
    
    // Verify stored encrypted
    const dbValue = await prisma.config.findUnique({
      where: { key: 'openrouter_api_key' }
    });
    
    expect(dbValue.value).not.toBe(configValue);  // Should be encrypted
    expect(dbValue.is_encrypted).toBe(true);
  });

  // A03: Injection
  test('should prevent SQL injection', async () => {
    const maliciousInput = "'; DROP TABLE users; --";
    
    const res = await request(app)
      .post('/api/projects')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ name: maliciousInput });
    
    expect(res.status).toBe(201);  // Should be treated as literal string
    expect(res.body.project.name).toBe(maliciousInput);
    
    // Verify users table still exists
    const userRes = await request(app)
      .get('/api/users')
      .set('Authorization', `Bearer ${authToken}`);
    
    expect(userRes.status).not.toBe(500);  // Table should still exist
  });

  // A06: Vulnerable and Outdated Components
  test('should have no known vulnerabilities in dependencies', async () => {
    // npm audit should return 0 vulnerabilities
    const auditResult = execSync('npm audit --audit-level=moderate').toString();
    expect(auditResult).not.toMatch(/vulnerability/i);
  });

  // A07: Identification and Authentication Failures
  test('should lock account after 5 failed login attempts', async () => {
    const username = 'testuser';
    
    for (let i = 0; i < 5; i++) {
      await request(app)
        .post('/api/auth/login')
        .send({ username, password: 'wrong' });
    }
    
    // 6th attempt should fail
    const res = await request(app)
      .post('/api/auth/login')
      .send({ username, password: 'wrong' });
    
    expect(res.status).toBe(429);  // Too many requests
  });

  // A08: Software and Data Integrity Failures
  test('should verify document integrity after upload', async () => {
    const originalFile = './test-data/RAMS.pdf';
    const originalHash = hashFile(originalFile);
    
    const uploadRes = await request(app)
      .post('/api/projects/:id/documents')
      .attach('file', originalFile)
      .set('Authorization', `Bearer ${authToken}`);
    
    const downloadRes = await request(app)
      .get(`/api/documents/${uploadRes.body.document.id}/download`)
      .set('Authorization', `Bearer ${authToken}`);
    
    const downloadedHash = hashBuffer(downloadRes.body);
    expect(downloadedHash).toBe(originalHash);
  });

  // A09: Logging and Monitoring Failures
  test('should log all security-relevant events', async () => {
    const action = 'FAILED_LOGIN_ATTEMPT';
    
    await request(app)
      .post('/api/auth/login')
      .send({ username: 'admin', password: 'wrong' });
    
    const logs = await prisma.audit_log.findMany({
      where: { action }
    });
    
    expect(logs.length).toBeGreaterThan(0);
  });
});
```

### Input Validation Tests

```javascript
// tests/security/input-validation.test.ts

describe('Input Validation', () => {
  test('should reject oversized uploads', async () => {
    const largeFile = Buffer.alloc(100 * 1024 * 1024);  // 100 MB
    
    const res = await request(app)
      .post('/api/projects/proj-1/documents')
      .attach('file', largeFile)
      .set('Authorization', `Bearer ${authToken}`);
    
    expect(res.status).toBe(413);  // Payload too large
  });

  test('should sanitize HTML in text fields', async () => {
    const xssPayload = '<script>alert("XSS")</script>';
    
    const res = await request(app)
      .post('/api/projects')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ name: xssPayload });
    
    const storedProject = await prisma.projects.findUnique({
      where: { id: res.body.project.id }
    });
    
    // Should be stored safely (escaped or stripped)
    expect(storedProject.name).not.toMatch(/<script>/);
  });

  test('should validate JWT format', async () => {
    const res = await request(app)
      .get('/api/projects')
      .set('Authorization', 'Bearer invalid.token.format');
    
    expect(res.status).toBe(401);
  });
});
```

---

## Acceptance Criteria

### Module-by-Module DoD

#### Module 1: Authentication

- [ ] Unit: Login function handles valid/invalid creds ✓
- [ ] Unit: Password hashing uses bcrypt ✓
- [ ] Integration: JWT token created and expires correctly ✓
- [ ] E2E: User can login and access protected routes ✓
- [ ] Security: Failed logins logged and rate-limited ✓

#### Module 2: Project Management

- [ ] Unit: Project creation validates required fields ✓
- [ ] Integration: Project created in Postgres with correct owner ✓
- [ ] E2E: User can create, edit, delete projects ✓
- [ ] E2E: Project state transitions work correctly ✓
- [ ] Security: User can only access own projects ✓

#### Module 3: HARA Workshop

- [ ] Unit: Risk level calculated correctly from impact ratings ✓
- [ ] Integration: HARA items saved and retrieved from DB ✓
- [ ] E2E: Complete HARA workflow (SuC→Categories→Items→Export) ✓
- [ ] Performance: HARA table with 100+ items responds <1 sec ✓
- [ ] Unit: CSV export contains all fields ✓

#### Module 4: Threat Canvas

- [ ] Unit: Node/edge CRUD validation ✓
- [ ] Integration: Canvas state synced to Postgres + Neo4j ✓
- [ ] E2E: Add/edit/delete nodes and edges ✓
- [ ] Performance: 100+ nodes render in <500 ms ✓
- [ ] Unit: Relationship validation (no invalid edges) ✓

#### Module 5: AI Features

- [ ] Unit: Threat suggestion ranking logic ✓
- [ ] Integration: Qdrant search + Neo4j context + LLM call ✓
- [ ] E2E: User can query and get relevant results ✓
- [ ] Performance: Query completes in <10 seconds ✓
- [ ] Unit: Response caching reduces duplicate LLM calls ✓

#### Module 6: Document Ingestion

- [ ] Unit: spaCy NER extraction accuracy >85% ✓
- [ ] Integration: Async ingestion pipeline works end-to-end ✓
- [ ] E2E: User can upload PDF, see ingestion progress, query results ✓
- [ ] Performance: 10 MB PDF ingested in <60 seconds ✓
- [ ] Unit: Extracted entities appear in Neo4j ✓

#### Module 7: Admin Configuration

- [ ] Unit: Config encryption/decryption works ✓
- [ ] Integration: Database connection test validates credentials ✓
- [ ] E2E: Admin can update all config values ✓
- [ ] Security: API keys not logged or exposed ✓
- [ ] Unit: Invalid config values rejected ✓

---

## Test Data & Fixtures

### Fixture Factory Pattern

```javascript
// tests/fixtures.ts

import { faker } from '@faker-js/faker';

export async function createMockUser(overrides?: Partial<User>) {
  return await prisma.users.create({
    data: {
      username: faker.internet.userName(),
      email: faker.internet.email(),
      password_hash: bcrypt.hashSync('test123', 10),
      is_active: true,
      ...overrides
    }
  });
}

export async function createMockProject(
  overrides?: Partial<Project>
) {
  const owner = await createMockUser();
  
  return await prisma.projects.create({
    data: {
      name: faker.company.name() + ' IEC 62443 Assessment',
      description: faker.lorem.sentences(3),
      location: faker.location.city(),
      operational_criticality: 'HIGH',
      owner_id: owner.id,
      status: 'DRAFT',
      ...overrides
    }
  });
}

export async function createMockHARAItem(
  projectId: string,
  overrides?: Partial<HaraItem>
) {
  return await prisma.hara_items.create({
    data: {
      project_id: projectId,
      name: faker.commerce.productName(),
      description: faker.lorem.sentences(2),
      asset_type: faker.helpers.arrayElement(['Subsystem', 'Device', 'Service']),
      impact_ratings: {
        'cat-1': faker.datatype.number({ min: 1, max: 5 }),
        'cat-2': faker.datatype.number({ min: 1, max: 5 })
      },
      ...overrides
    }
  });
}

export async function createMockGraphNode(
  projectId: string,
  overrides?: Partial<GraphNode>
) {
  return await prisma.graph_nodes.create({
    data: {
      project_id: projectId,
      node_type: 'ASSET',
      label: faker.word.adjective() + ' ' + faker.word.noun(),
      description: faker.lorem.sentence(),
      position_x: faker.datatype.number({ min: 0, max: 800 }),
      position_y: faker.datatype.number({ min: 0, max: 600 }),
      ...overrides
    }
  });
}

export const testDatasets = {
  // Minimal test data for unit tests
  minimal: {
    users: 1,
    projectsPerUser: 1,
    haraItemsPerProject: 3,
    graphNodesPerProject: 5
  },
  
  // Realistic test data for integration tests
  realistic: {
    users: 3,
    projectsPerUser: 2,
    haraItemsPerProject: 15,
    graphNodesPerProject: 50,
    documentsPerProject: 3
  },
  
  // Large dataset for performance tests
  large: {
    users: 10,
    projectsPerUser: 5,
    haraItemsPerProject: 100,
    graphNodesPerProject: 200,
    documentsPerProject: 10
  }
};
```

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml

name: Tests

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_PASSWORD: test123
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Start Docker services
        run: |
          docker-compose -f docker-compose.test.yml up -d
          sleep 30  # Wait for all services
      
      - name: Run Postgres migrations
        run: npm run migrate:latest
      
      - name: Run unit tests
        run: npm run test:unit -- --coverage --watch=false
      
      - name: Run integration tests
        run: npm run test:integration
      
      - name: Run E2E tests
        run: npm run test:e2e
        if: github.event_name == 'pull_request'
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
      
      - name: Security audit
        run: npm audit --audit-level=moderate
      
      - name: ESLint
        run: npm run lint
      
      - name: Type check
        run: npm run type-check
      
      - name: Cleanup
        run: docker-compose -f docker-compose.test.yml down
        if: always()
```

---

## Test Metrics & Reporting

### Target Metrics

```
Code Coverage
├── Statements: 80%+
├── Branches: 75%+
├── Functions: 80%+
└── Lines: 80%+

Test Execution
├── Unit tests: <5 min
├── Integration: <10 min
├── E2E: <15 min
└── Total: <30 min

Quality Gates (Block Merge if Failed)
├── Coverage < 75%: FAIL
├── Unit tests fail: FAIL
├── Security vulnerabilities: FAIL
├── Type errors: FAIL
└── Lint warnings > 10: WARNING
```

### Reporting Dashboard

```bash
# Generate test report
npm run test:report

# Output: ./reports/test-report.html
# Contains: Coverage, trends, slowest tests, failed tests
```

---

**End of Testing & QA Plan**

For questions, contact: QA Lead  
Last Updated: December 2024  
Version: 1.0
