/**
 * Health Check API Tests
 * Tests for /api/health endpoint
 */

import { describe, test, expect } from '@jest/globals';

const API_BASE = process.env.API_BASE || 'http://localhost:3001';

describe('Health Check API', () => {
  test('GET /api/health - should return 200 or 503', async () => {
    const response = await fetch(`${API_BASE}/api/health`);
    // 200 = healthy, 503 = degraded (some services unavailable)
    expect([200, 503]).toContain(response.status);
  });

  test('GET /api/health - should have neo4j status in checks', async () => {
    const response = await fetch(`${API_BASE}/api/health`);
    const data = await response.json();

    expect(data).toHaveProperty('checks');
    expect(data.checks).toHaveProperty('neo4j');
    expect(data.checks.neo4j).toHaveProperty('status');
  });

  test('GET /api/health - should have qdrant status in checks', async () => {
    const response = await fetch(`${API_BASE}/api/health`);
    const data = await response.json();

    expect(data).toHaveProperty('checks');
    expect(data.checks).toHaveProperty('qdrant');
    expect(data.checks.qdrant).toHaveProperty('status');
  });

  test('GET /api/health - response time < 3 seconds', async () => {
    const start = Date.now();
    await fetch(`${API_BASE}/api/health`);
    const duration = Date.now() - start;

    expect(duration).toBeLessThan(3000);
  });
});
