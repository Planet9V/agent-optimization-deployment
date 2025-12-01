/**
 * Environment Validation Tests
 *
 * Tests for environment variable validation logic
 */

import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { validateEnv, validateEnvOrThrow } from '../lib/env-validation';

describe('Environment Validation', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    // Reset environment before each test
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    // Restore original environment
    process.env = originalEnv;
  });

  describe('validateEnv', () => {
    it('should pass with all required variables', () => {
      process.env = {
        NODE_ENV: 'production',
        NEO4J_URI: 'bolt://localhost:7687',
        NEO4J_USER: 'neo4j',
        NEO4J_PASSWORD: 'password',
        NEO4J_DATABASE: 'neo4j',
        MYSQL_HOST: 'localhost',
        MYSQL_PORT: '3306',
        MYSQL_DATABASE: 'testdb',
        MYSQL_USER: 'root',
        MYSQL_PASSWORD: 'password',
        QDRANT_URL: 'http://localhost:6333',
        MINIO_ENDPOINT: 'http://localhost:9000',
        MINIO_ACCESS_KEY: 'minio',
        MINIO_SECRET_KEY: 'miniosecret',
        PORT: '3000',
      };

      const result = validateEnv();
      expect(result.success).toBe(true);
      expect(result.errors).toHaveLength(0);
      expect(result.env).toBeDefined();
    });

    it('should fail with missing Neo4j URI', () => {
      process.env = {
        NEO4J_USER: 'neo4j',
        NEO4J_PASSWORD: 'password',
        MYSQL_HOST: 'localhost',
        MYSQL_DATABASE: 'testdb',
        MYSQL_USER: 'root',
        MYSQL_PASSWORD: 'password',
        QDRANT_URL: 'http://localhost:6333',
        MINIO_ENDPOINT: 'http://localhost:9000',
        MINIO_ACCESS_KEY: 'minio',
        MINIO_SECRET_KEY: 'miniosecret',
      };

      const result = validateEnv();
      expect(result.success).toBe(false);
      expect(result.errors.some(e => e.includes('NEO4J_URI'))).toBe(true);
    });

    it('should fail with invalid Neo4j URI format', () => {
      process.env = {
        NEO4J_URI: 'invalid-uri',
        NEO4J_USER: 'neo4j',
        NEO4J_PASSWORD: 'password',
        MYSQL_HOST: 'localhost',
        MYSQL_DATABASE: 'testdb',
        MYSQL_USER: 'root',
        MYSQL_PASSWORD: 'password',
        QDRANT_URL: 'http://localhost:6333',
        MINIO_ENDPOINT: 'http://localhost:9000',
        MINIO_ACCESS_KEY: 'minio',
        MINIO_SECRET_KEY: 'miniosecret',
      };

      const result = validateEnv();
      expect(result.success).toBe(false);
      expect(result.errors.some(e => e.includes('valid Neo4j URI'))).toBe(true);
    });

    it('should accept various Neo4j URI formats', () => {
      const validUris = [
        'bolt://localhost:7687',
        'neo4j://localhost:7687',
        'bolt+s://secure.host:7687',
        'neo4j+s://secure.host:7687',
        'bolt://host.example.com:7687',
      ];

      validUris.forEach(uri => {
        process.env = {
          NODE_ENV: 'production',
          NEO4J_URI: uri,
          NEO4J_USER: 'neo4j',
          NEO4J_PASSWORD: 'password',
          MYSQL_HOST: 'localhost',
          MYSQL_DATABASE: 'testdb',
          MYSQL_USER: 'root',
          MYSQL_PASSWORD: 'password',
          QDRANT_URL: 'http://localhost:6333',
          MINIO_ENDPOINT: 'http://localhost:9000',
          MINIO_ACCESS_KEY: 'minio',
          MINIO_SECRET_KEY: 'miniosecret',
        };

        const result = validateEnv();
        expect(result.success).toBe(true);
      });
    });

    it('should fail with missing MySQL configuration', () => {
      process.env = {
        NEO4J_URI: 'bolt://localhost:7687',
        NEO4J_USER: 'neo4j',
        NEO4J_PASSWORD: 'password',
        QDRANT_URL: 'http://localhost:6333',
        MINIO_ENDPOINT: 'http://localhost:9000',
        MINIO_ACCESS_KEY: 'minio',
        MINIO_SECRET_KEY: 'miniosecret',
      };

      const result = validateEnv();
      expect(result.success).toBe(false);
      expect(result.errors.some(e => e.includes('MYSQL'))).toBe(true);
    });

    it('should warn about localhost in production', () => {
      process.env = {
        NODE_ENV: 'production',
        NEO4J_URI: 'bolt://localhost:7687',
        NEO4J_USER: 'neo4j',
        NEO4J_PASSWORD: 'password',
        MYSQL_HOST: 'localhost',
        MYSQL_DATABASE: 'testdb',
        MYSQL_USER: 'root',
        MYSQL_PASSWORD: 'password',
        QDRANT_URL: 'http://localhost:6333',
        MINIO_ENDPOINT: 'http://localhost:9000',
        MINIO_ACCESS_KEY: 'minio',
        MINIO_SECRET_KEY: 'miniosecret',
      };

      const result = validateEnv();
      expect(result.success).toBe(true);
      expect(result.warnings.length).toBeGreaterThan(0);
      expect(result.warnings.some(w => w.includes('localhost'))).toBe(true);
    });

    it('should warn about missing authentication in production', () => {
      process.env = {
        NODE_ENV: 'production',
        NEO4J_URI: 'bolt://neo4j.example.com:7687',
        NEO4J_USER: 'neo4j',
        NEO4J_PASSWORD: 'password',
        MYSQL_HOST: 'mysql.example.com',
        MYSQL_DATABASE: 'testdb',
        MYSQL_USER: 'root',
        MYSQL_PASSWORD: 'password',
        QDRANT_URL: 'http://qdrant.example.com:6333',
        MINIO_ENDPOINT: 'http://minio.example.com:9000',
        MINIO_ACCESS_KEY: 'minio',
        MINIO_SECRET_KEY: 'miniosecret',
      };

      const result = validateEnv();
      expect(result.success).toBe(true);
      expect(result.warnings.some(w => w.includes('authentication'))).toBe(true);
    });

    it('should accept optional DATABASE_URL', () => {
      process.env = {
        NODE_ENV: 'production',
        NEO4J_URI: 'bolt://localhost:7687',
        NEO4J_USER: 'neo4j',
        NEO4J_PASSWORD: 'password',
        MYSQL_HOST: 'localhost',
        MYSQL_DATABASE: 'testdb',
        MYSQL_USER: 'root',
        MYSQL_PASSWORD: 'password',
        QDRANT_URL: 'http://localhost:6333',
        MINIO_ENDPOINT: 'http://localhost:9000',
        MINIO_ACCESS_KEY: 'minio',
        MINIO_SECRET_KEY: 'miniosecret',
        DATABASE_URL: 'postgresql://user:pass@host:5432/db',
      };

      const result = validateEnv();
      expect(result.success).toBe(true);
      expect(result.env?.DATABASE_URL).toBeDefined();
    });

    it('should fail with invalid port number', () => {
      process.env = {
        NEO4J_URI: 'bolt://localhost:7687',
        NEO4J_USER: 'neo4j',
        NEO4J_PASSWORD: 'password',
        MYSQL_HOST: 'localhost',
        MYSQL_PORT: '99999', // Invalid port
        MYSQL_DATABASE: 'testdb',
        MYSQL_USER: 'root',
        MYSQL_PASSWORD: 'password',
        QDRANT_URL: 'http://localhost:6333',
        MINIO_ENDPOINT: 'http://localhost:9000',
        MINIO_ACCESS_KEY: 'minio',
        MINIO_SECRET_KEY: 'miniosecret',
      };

      const result = validateEnv();
      expect(result.success).toBe(false);
      expect(result.errors.some(e => e.includes('Port'))).toBe(true);
    });
  });

  describe('validateEnvOrThrow', () => {
    it('should throw on validation failure', () => {
      process.env = {
        NEO4J_URI: 'invalid',
      };

      expect(() => validateEnvOrThrow()).toThrow('Environment validation failed');
    });

    it('should return validated env on success', () => {
      process.env = {
        NODE_ENV: 'production',
        NEO4J_URI: 'bolt://localhost:7687',
        NEO4J_USER: 'neo4j',
        NEO4J_PASSWORD: 'password',
        MYSQL_HOST: 'localhost',
        MYSQL_DATABASE: 'testdb',
        MYSQL_USER: 'root',
        MYSQL_PASSWORD: 'password',
        QDRANT_URL: 'http://localhost:6333',
        MINIO_ENDPOINT: 'http://localhost:9000',
        MINIO_ACCESS_KEY: 'minio',
        MINIO_SECRET_KEY: 'miniosecret',
      };

      const env = validateEnvOrThrow();
      expect(env).toBeDefined();
      expect(env.NEO4J_URI).toBe('bolt://localhost:7687');
    });
  });
});
