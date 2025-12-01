/**
 * Observability API Tests
 * Tests for /api/observability endpoints
 */

import { describe, test, expect } from '@jest/globals';

const API_BASE = process.env.API_BASE || 'http://localhost:3001';

describe('Observability System API', () => {
  describe('GET /api/observability/system', () => {
    test('should return system metrics', async () => {
      const response = await fetch(`${API_BASE}/api/observability/system`);
      expect(response.status).toBe(200);

      const data = await response.json();
      expect(data).toHaveProperty('timestamp');
      expect(data).toHaveProperty('memory');
      expect(data).toHaveProperty('cpu');
      expect(data).toHaveProperty('uptime');
      expect(data).toHaveProperty('status');
    });

    test('memory metrics should have required fields', async () => {
      const response = await fetch(`${API_BASE}/api/observability/system`);
      const data = await response.json();

      expect(data.memory).toHaveProperty('heapUsed');
      expect(data.memory).toHaveProperty('heapTotal');
      expect(data.memory).toHaveProperty('rss');
      expect(data.memory).toHaveProperty('percentage');

      expect(typeof data.memory.heapUsed).toBe('number');
      expect(typeof data.memory.percentage).toBe('number');
    });

    test('cpu metrics should have user and system', async () => {
      const response = await fetch(`${API_BASE}/api/observability/system`);
      const data = await response.json();

      expect(data.cpu).toHaveProperty('user');
      expect(data.cpu).toHaveProperty('system');
      expect(typeof data.cpu.user).toBe('number');
      expect(typeof data.cpu.system).toBe('number');
    });

    test('status should be valid health state', async () => {
      const response = await fetch(`${API_BASE}/api/observability/system`);
      const data = await response.json();

      expect(['healthy', 'warning', 'critical']).toContain(data.status);
    });
  });

  describe('GET /api/observability/agents', () => {
    test('should return agent metrics', async () => {
      const response = await fetch(`${API_BASE}/api/observability/agents`);
      expect(response.status).toBe(200);

      const data = await response.json();
      expect(data).toHaveProperty('activeAgents');
      expect(data).toHaveProperty('completedTasks');
      expect(data).toHaveProperty('failedTasks');
      expect(data).toHaveProperty('averageDuration');
    });

    test('agent counts should be non-negative', async () => {
      const response = await fetch(`${API_BASE}/api/observability/agents`);
      const data = await response.json();

      expect(data.activeAgents).toBeGreaterThanOrEqual(0);
      expect(data.completedTasks).toBeGreaterThanOrEqual(0);
      expect(data.failedTasks).toBeGreaterThanOrEqual(0);
      expect(data.averageDuration).toBeGreaterThanOrEqual(0);
    });
  });

  describe('GET /api/observability/performance', () => {
    test('should return performance metrics', async () => {
      const response = await fetch(`${API_BASE}/api/observability/performance`);
      expect(response.status).toBe(200);

      const data = await response.json();
      expect(data).toHaveProperty('avgResponseTime');
      expect(data).toHaveProperty('p95ResponseTime');
      expect(data).toHaveProperty('throughput');
      expect(data).toHaveProperty('errorRate');
    });

    test('performance values should be valid numbers', async () => {
      const response = await fetch(`${API_BASE}/api/observability/performance`);
      const data = await response.json();

      expect(typeof data.avgResponseTime).toBe('number');
      expect(typeof data.p95ResponseTime).toBe('number');
      expect(typeof data.throughput).toBe('number');
      expect(typeof data.errorRate).toBe('number');
    });
  });
});
