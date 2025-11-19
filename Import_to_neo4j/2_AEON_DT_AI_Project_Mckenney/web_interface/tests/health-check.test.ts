/**
 * Health Check Endpoint Test
 * Tests the /api/health endpoint for all service connections
 */

import { describe, it, expect } from '@jest/globals';

describe('Health Check Endpoint', () => {
  const HEALTH_ENDPOINT = 'http://localhost:3000/api/health';

  it('should return health status for all services', async () => {
    const response = await fetch(HEALTH_ENDPOINT);
    const data = await response.json();

    // Verify response structure
    expect(data).toHaveProperty('status');
    expect(data).toHaveProperty('timestamp');
    expect(data).toHaveProperty('services');
    expect(data).toHaveProperty('overallHealth');

    // Verify all services are present
    expect(data.services).toHaveProperty('neo4j');
    expect(data.services).toHaveProperty('mysql');
    expect(data.services).toHaveProperty('qdrant');
    expect(data.services).toHaveProperty('minio');

    // Verify service status format
    for (const [serviceName, service] of Object.entries(data.services)) {
      expect(service).toHaveProperty('status');
      expect(['ok', 'error', 'timeout']).toContain((service as any).status);

      if ((service as any).status === 'ok') {
        expect(service).toHaveProperty('responseTime');
        expect(typeof (service as any).responseTime).toBe('number');
      }
    }

    // Verify overall health calculation
    expect(['healthy', 'degraded', 'unhealthy']).toContain(data.status);
    expect(data.overallHealth).toMatch(/\d+\/4 services healthy/);

    console.log('✅ Health Check Response:', JSON.stringify(data, null, 2));
  });

  it('should return appropriate HTTP status codes', async () => {
    const response = await fetch(HEALTH_ENDPOINT);
    const data = await response.json();

    if (data.status === 'healthy') {
      expect(response.status).toBe(200);
    } else if (data.status === 'degraded') {
      expect(response.status).toBe(207);
    } else {
      expect(response.status).toBe(503);
    }
  });

  it('should include response times for healthy services', async () => {
    const response = await fetch(HEALTH_ENDPOINT);
    const data = await response.json();

    for (const [serviceName, service] of Object.entries(data.services)) {
      if ((service as any).status === 'ok') {
        expect((service as any).responseTime).toBeGreaterThan(0);
        expect((service as any).responseTime).toBeLessThan(5000); // Should be under timeout
        console.log(`✅ ${serviceName}: ${(service as any).responseTime}ms`);
      }
    }
  });

  it('should include service connection details', async () => {
    const response = await fetch(HEALTH_ENDPOINT);
    const data = await response.json();

    // Neo4j details
    if (data.services.neo4j.details) {
      expect(data.services.neo4j.details).toHaveProperty('uri');
    }

    // MySQL details
    if (data.services.mysql.details) {
      expect(data.services.mysql.details).toHaveProperty('host');
      expect(data.services.mysql.details).toHaveProperty('port');
    }

    // Qdrant details
    if (data.services.qdrant.details) {
      expect(data.services.qdrant.details).toHaveProperty('url');
    }

    // MinIO details
    if (data.services.minio.details) {
      expect(data.services.minio.details).toHaveProperty('endpoint');
    }
  });

  it('should include metadata', async () => {
    const response = await fetch(HEALTH_ENDPOINT);
    const data = await response.json();

    expect(data.metadata).toHaveProperty('environment');
    expect(data.metadata).toHaveProperty('nodeVersion');

    console.log('📊 Environment:', data.metadata.environment);
    console.log('📦 Node Version:', data.metadata.nodeVersion);
  });
});
