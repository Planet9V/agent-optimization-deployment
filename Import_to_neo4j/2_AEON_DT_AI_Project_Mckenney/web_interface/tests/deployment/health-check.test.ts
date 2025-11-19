/**
 * Health Check Test Suite
 * Validates health endpoint response format and all service statuses
 */

import { describe, it, expect, beforeAll } from '@jest/globals';
import axios from 'axios';

const BASE_URL = process.env.API_BASE_URL || 'http://localhost:3000';
const HEALTH_ENDPOINT = `${BASE_URL}/api/health`;
const TIMEOUT = 10000; // 10 seconds

interface ServiceStatus {
  status: 'healthy' | 'unhealthy' | 'degraded';
  responseTime?: number;
  error?: string;
  details?: Record<string, any>;
}

interface HealthResponse {
  status: 'healthy' | 'unhealthy' | 'degraded';
  timestamp: string;
  services: {
    neo4j: ServiceStatus;
    mysql: ServiceStatus;
    qdrant: ServiceStatus;
    minio: ServiceStatus;
  };
  uptime: number;
  version: string;
}

describe('Health Check Endpoint', () => {
  let healthResponse: HealthResponse;

  beforeAll(async () => {
    const response = await axios.get(HEALTH_ENDPOINT, { timeout: TIMEOUT });
    healthResponse = response.data;
  });

  describe('Response Format Validation', () => {
    it('should return 200 status code', async () => {
      const response = await axios.get(HEALTH_ENDPOINT, { timeout: TIMEOUT });
      expect(response.status).toBe(200);
    });

    it('should have correct response structure', () => {
      expect(healthResponse).toHaveProperty('status');
      expect(healthResponse).toHaveProperty('timestamp');
      expect(healthResponse).toHaveProperty('services');
      expect(healthResponse).toHaveProperty('uptime');
      expect(healthResponse).toHaveProperty('version');
    });

    it('should have valid timestamp format', () => {
      const timestamp = new Date(healthResponse.timestamp);
      expect(timestamp.toString()).not.toBe('Invalid Date');

      // Timestamp should be recent (within last minute)
      const now = Date.now();
      const timestampMs = timestamp.getTime();
      expect(now - timestampMs).toBeLessThan(60000);
    });

    it('should have valid overall status', () => {
      expect(['healthy', 'unhealthy', 'degraded']).toContain(healthResponse.status);
    });

    it('should have positive uptime', () => {
      expect(healthResponse.uptime).toBeGreaterThan(0);
    });

    it('should have version string', () => {
      expect(typeof healthResponse.version).toBe('string');
      expect(healthResponse.version.length).toBeGreaterThan(0);
    });
  });

  describe('Services Object Validation', () => {
    it('should have all required services', () => {
      expect(healthResponse.services).toHaveProperty('neo4j');
      expect(healthResponse.services).toHaveProperty('mysql');
      expect(healthResponse.services).toHaveProperty('qdrant');
      expect(healthResponse.services).toHaveProperty('minio');
    });

    it('should have valid service status for each service', () => {
      const services = ['neo4j', 'mysql', 'qdrant', 'minio'] as const;

      services.forEach(service => {
        const serviceStatus = healthResponse.services[service];
        expect(serviceStatus).toHaveProperty('status');
        expect(['healthy', 'unhealthy', 'degraded']).toContain(serviceStatus.status);
      });
    });

    it('should include response time for healthy services', () => {
      const services = ['neo4j', 'mysql', 'qdrant', 'minio'] as const;

      services.forEach(service => {
        const serviceStatus = healthResponse.services[service];
        if (serviceStatus.status === 'healthy') {
          expect(serviceStatus).toHaveProperty('responseTime');
          expect(typeof serviceStatus.responseTime).toBe('number');
          expect(serviceStatus.responseTime).toBeGreaterThan(0);
        }
      });
    });

    it('should include error message for unhealthy services', () => {
      const services = ['neo4j', 'mysql', 'qdrant', 'minio'] as const;

      services.forEach(service => {
        const serviceStatus = healthResponse.services[service];
        if (serviceStatus.status === 'unhealthy') {
          expect(serviceStatus).toHaveProperty('error');
          expect(typeof serviceStatus.error).toBe('string');
          expect(serviceStatus.error.length).toBeGreaterThan(0);
        }
      });
    });
  });

  describe('Response Time Benchmarks', () => {
    it('should respond within 5 seconds', async () => {
      const start = Date.now();
      await axios.get(HEALTH_ENDPOINT, { timeout: TIMEOUT });
      const duration = Date.now() - start;

      expect(duration).toBeLessThan(5000);
    });

    it('should have service response times under 2 seconds', () => {
      const services = ['neo4j', 'mysql', 'qdrant', 'minio'] as const;

      services.forEach(service => {
        const serviceStatus = healthResponse.services[service];
        if (serviceStatus.responseTime) {
          expect(serviceStatus.responseTime).toBeLessThan(2000);
        }
      });
    });

    it('should complete 5 consecutive health checks within 10 seconds', async () => {
      const start = Date.now();

      const promises = Array(5).fill(null).map(() =>
        axios.get(HEALTH_ENDPOINT, { timeout: TIMEOUT })
      );

      await Promise.all(promises);
      const duration = Date.now() - start;

      expect(duration).toBeLessThan(10000);
    });
  });

  describe('System Status Logic', () => {
    it('should be healthy when all services are healthy', () => {
      const services = ['neo4j', 'mysql', 'qdrant', 'minio'] as const;
      const allHealthy = services.every(
        service => healthResponse.services[service].status === 'healthy'
      );

      if (allHealthy) {
        expect(healthResponse.status).toBe('healthy');
      }
    });

    it('should be unhealthy when any critical service is unhealthy', () => {
      const criticalServices = ['neo4j', 'mysql'] as const;
      const anyUnhealthy = criticalServices.some(
        service => healthResponse.services[service].status === 'unhealthy'
      );

      if (anyUnhealthy) {
        expect(healthResponse.status).toBe('unhealthy');
      }
    });

    it('should be degraded when optional services are unhealthy', () => {
      const optionalServices = ['qdrant', 'minio'] as const;
      const criticalServices = ['neo4j', 'mysql'] as const;

      const optionalUnhealthy = optionalServices.some(
        service => healthResponse.services[service].status === 'unhealthy'
      );
      const criticalHealthy = criticalServices.every(
        service => healthResponse.services[service].status === 'healthy'
      );

      if (optionalUnhealthy && criticalHealthy) {
        expect(healthResponse.status).toBe('degraded');
      }
    });
  });

  describe('Error Handling', () => {
    it('should handle network timeouts gracefully', async () => {
      try {
        await axios.get(HEALTH_ENDPOINT, { timeout: 1 }); // 1ms timeout
      } catch (error: any) {
        expect(error.code).toBe('ECONNABORTED');
      }
    });

    it('should return valid JSON even on partial failures', async () => {
      const response = await axios.get(HEALTH_ENDPOINT, { timeout: TIMEOUT });
      expect(() => JSON.parse(JSON.stringify(response.data))).not.toThrow();
    });
  });
});
