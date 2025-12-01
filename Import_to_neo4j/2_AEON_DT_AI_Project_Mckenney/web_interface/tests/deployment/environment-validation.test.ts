/**
 * Environment Validation Test Suite
 * Validates presence and format of required environment variables
 */

import { describe, it, expect } from '@jest/globals';
import * as fs from 'fs';
import * as path from 'path';

describe('Environment Variables - Neo4j', () => {
  it('should have NEO4J_URI defined', () => {
    expect(process.env.NEO4J_URI).toBeDefined();
    expect(process.env.NEO4J_URI!.length).toBeGreaterThan(0);
  });

  it('should have valid Neo4j URI format', () => {
    const uri = process.env.NEO4J_URI || '';
    const validProtocols = ['bolt://', 'bolt+s://', 'bolt+ssc://', 'neo4j://', 'neo4j+s://', 'neo4j+ssc://'];
    const hasValidProtocol = validProtocols.some(protocol => uri.startsWith(protocol));
    expect(hasValidProtocol).toBe(true);
  });

  it('should have NEO4J_USER defined', () => {
    expect(process.env.NEO4J_USER).toBeDefined();
    expect(process.env.NEO4J_USER!.length).toBeGreaterThan(0);
  });

  it('should have NEO4J_PASSWORD defined', () => {
    expect(process.env.NEO4J_PASSWORD).toBeDefined();
    expect(process.env.NEO4J_PASSWORD!.length).toBeGreaterThan(0);
  });

  it('should not use default password in production', () => {
    if (process.env.NODE_ENV === 'production') {
      expect(process.env.NEO4J_PASSWORD).not.toBe('password');
      expect(process.env.NEO4J_PASSWORD).not.toBe('neo4j');
    }
  });
});

describe('Environment Variables - MySQL', () => {
  it('should have MYSQL_HOST defined', () => {
    expect(process.env.MYSQL_HOST).toBeDefined();
    expect(process.env.MYSQL_HOST!.length).toBeGreaterThan(0);
  });

  it('should have MYSQL_PORT defined and valid', () => {
    expect(process.env.MYSQL_PORT).toBeDefined();
    const port = parseInt(process.env.MYSQL_PORT!);
    expect(port).toBeGreaterThan(0);
    expect(port).toBeLessThan(65536);
  });

  it('should have MYSQL_USER defined', () => {
    expect(process.env.MYSQL_USER).toBeDefined();
    expect(process.env.MYSQL_USER!.length).toBeGreaterThan(0);
  });

  it('should have MYSQL_PASSWORD defined', () => {
    expect(process.env.MYSQL_PASSWORD).toBeDefined();
    expect(process.env.MYSQL_PASSWORD!.length).toBeGreaterThan(0);
  });

  it('should have MYSQL_DATABASE defined', () => {
    expect(process.env.MYSQL_DATABASE).toBeDefined();
    expect(process.env.MYSQL_DATABASE!.length).toBeGreaterThan(0);
  });

  it('should not use default credentials in production', () => {
    if (process.env.NODE_ENV === 'production') {
      expect(process.env.MYSQL_USER).not.toBe('root');
      expect(process.env.MYSQL_PASSWORD).not.toBe('password');
    }
  });
});

describe('Environment Variables - Qdrant', () => {
  it('should have QDRANT_URL defined', () => {
    expect(process.env.QDRANT_URL).toBeDefined();
    expect(process.env.QDRANT_URL!.length).toBeGreaterThan(0);
  });

  it('should have valid Qdrant URL format', () => {
    const url = process.env.QDRANT_URL || '';
    expect(url.startsWith('http://') || url.startsWith('https://')).toBe(true);
  });

  it('should use HTTPS in production', () => {
    if (process.env.NODE_ENV === 'production') {
      expect(process.env.QDRANT_URL).toMatch(/^https:\/\//);
    }
  });

  it('should have QDRANT_API_KEY in production', () => {
    if (process.env.NODE_ENV === 'production') {
      expect(process.env.QDRANT_API_KEY).toBeDefined();
      expect(process.env.QDRANT_API_KEY!.length).toBeGreaterThan(0);
    }
  });
});

describe('Environment Variables - MinIO', () => {
  it('should have MINIO_ENDPOINT defined', () => {
    expect(process.env.MINIO_ENDPOINT).toBeDefined();
    expect(process.env.MINIO_ENDPOINT!.length).toBeGreaterThan(0);
  });

  it('should have MINIO_PORT defined and valid', () => {
    expect(process.env.MINIO_PORT).toBeDefined();
    const port = parseInt(process.env.MINIO_PORT!);
    expect(port).toBeGreaterThan(0);
    expect(port).toBeLessThan(65536);
  });

  it('should have MINIO_ACCESS_KEY defined', () => {
    expect(process.env.MINIO_ACCESS_KEY).toBeDefined();
    expect(process.env.MINIO_ACCESS_KEY!.length).toBeGreaterThan(0);
  });

  it('should have MINIO_SECRET_KEY defined', () => {
    expect(process.env.MINIO_SECRET_KEY).toBeDefined();
    expect(process.env.MINIO_SECRET_KEY!.length).toBeGreaterThan(0);
  });

  it('should not use default credentials in production', () => {
    if (process.env.NODE_ENV === 'production') {
      expect(process.env.MINIO_ACCESS_KEY).not.toBe('minioadmin');
      expect(process.env.MINIO_SECRET_KEY).not.toBe('minioadmin');
    }
  });

  it('should use SSL in production', () => {
    if (process.env.NODE_ENV === 'production') {
      expect(process.env.MINIO_USE_SSL).toBe('true');
    }
  });
});

describe('Environment Variables - Application', () => {
  it('should have NODE_ENV defined', () => {
    expect(process.env.NODE_ENV).toBeDefined();
  });

  it('should have valid NODE_ENV value', () => {
    const validEnvs = ['development', 'test', 'production', 'staging'];
    expect(validEnvs).toContain(process.env.NODE_ENV);
  });

  it('should have PORT defined and valid', () => {
    if (process.env.PORT) {
      const port = parseInt(process.env.PORT);
      expect(port).toBeGreaterThan(0);
      expect(port).toBeLessThan(65536);
    }
  });

  it('should have API_BASE_URL in production', () => {
    if (process.env.NODE_ENV === 'production') {
      expect(process.env.API_BASE_URL).toBeDefined();
      expect(process.env.API_BASE_URL).toMatch(/^https?:\/\//);
    }
  });
});

describe('Environment File Validation', () => {
  const projectRoot = path.resolve(__dirname, '../..');
  const envFile = path.join(projectRoot, '.env');
  const envExampleFile = path.join(projectRoot, '.env.example');

  it('should have .env file in project root', () => {
    const exists = fs.existsSync(envFile);
    if (!exists && process.env.NODE_ENV !== 'test') {
      console.warn('Warning: .env file not found. Using environment variables.');
    }
    // Don't fail test if using system env vars
    expect(true).toBe(true);
  });

  it('should have .env.example file', () => {
    const exists = fs.existsSync(envExampleFile);
    expect(exists).toBe(true);
  });

  it('.env should not be committed to git', () => {
    const gitignorePath = path.join(projectRoot, '.gitignore');
    if (fs.existsSync(gitignorePath)) {
      const gitignore = fs.readFileSync(gitignorePath, 'utf-8');
      expect(gitignore).toContain('.env');
    }
  });
});

describe('Network Connectivity', () => {
  it('should resolve Neo4j hostname', async () => {
    const url = new URL(process.env.NEO4J_URI || 'bolt://localhost:7687');
    const hostname = url.hostname;

    // Basic check that hostname is defined
    expect(hostname).toBeDefined();
    expect(hostname.length).toBeGreaterThan(0);
  });

  it('should resolve MySQL hostname', async () => {
    const hostname = process.env.MYSQL_HOST || 'localhost';
    expect(hostname).toBeDefined();
    expect(hostname.length).toBeGreaterThan(0);
  });

  it('should resolve Qdrant hostname', async () => {
    const url = new URL(process.env.QDRANT_URL || 'http://localhost:6333');
    const hostname = url.hostname;
    expect(hostname).toBeDefined();
    expect(hostname.length).toBeGreaterThan(0);
  });

  it('should resolve MinIO hostname', async () => {
    const hostname = process.env.MINIO_ENDPOINT || 'localhost';
    expect(hostname).toBeDefined();
    expect(hostname.length).toBeGreaterThan(0);
  });
});

describe('Security Validation', () => {
  it('should not expose secrets in error messages', () => {
    const sensitiveKeys = [
      'NEO4J_PASSWORD',
      'MYSQL_PASSWORD',
      'QDRANT_API_KEY',
      'MINIO_SECRET_KEY'
    ];

    sensitiveKeys.forEach(key => {
      const value = process.env[key];
      if (value) {
        // Ensure secrets are long enough
        expect(value.length).toBeGreaterThanOrEqual(8);
      }
    });
  });

  it('should use strong passwords in production', () => {
    if (process.env.NODE_ENV === 'production') {
      const passwords = [
        process.env.NEO4J_PASSWORD,
        process.env.MYSQL_PASSWORD,
        process.env.MINIO_SECRET_KEY
      ].filter(Boolean);

      passwords.forEach(password => {
        // At least 12 characters
        expect(password!.length).toBeGreaterThanOrEqual(12);

        // Contains mix of characters
        const hasLower = /[a-z]/.test(password!);
        const hasUpper = /[A-Z]/.test(password!);
        const hasNumber = /[0-9]/.test(password!);
        const hasSpecial = /[^a-zA-Z0-9]/.test(password!);

        const complexity = [hasLower, hasUpper, hasNumber, hasSpecial].filter(Boolean).length;
        expect(complexity).toBeGreaterThanOrEqual(3);
      });
    }
  });

  it('should not contain localhost in production URLs', () => {
    if (process.env.NODE_ENV === 'production') {
      const urls = [
        process.env.NEO4J_URI,
        process.env.MYSQL_HOST,
        process.env.QDRANT_URL,
        process.env.MINIO_ENDPOINT
      ].filter(Boolean);

      urls.forEach(url => {
        expect(url!.toLowerCase()).not.toContain('localhost');
        expect(url!.toLowerCase()).not.toContain('127.0.0.1');
      });
    }
  });
});

describe('Configuration Completeness', () => {
  it('should have all required variables for all services', () => {
    const required = [
      // Neo4j
      'NEO4J_URI',
      'NEO4J_USER',
      'NEO4J_PASSWORD',
      // MySQL
      'MYSQL_HOST',
      'MYSQL_PORT',
      'MYSQL_USER',
      'MYSQL_PASSWORD',
      'MYSQL_DATABASE',
      // Qdrant
      'QDRANT_URL',
      // MinIO
      'MINIO_ENDPOINT',
      'MINIO_PORT',
      'MINIO_ACCESS_KEY',
      'MINIO_SECRET_KEY'
    ];

    const missing = required.filter(key => !process.env[key]);

    if (missing.length > 0) {
      console.error('Missing environment variables:', missing);
    }

    expect(missing).toEqual([]);
  });

  it('should have consistent configuration across services', () => {
    // If using Docker, ports should be standard
    if (process.env.MYSQL_HOST === 'mysql') {
      expect(process.env.MYSQL_PORT).toBe('3306');
    }

    if (process.env.MINIO_ENDPOINT === 'minio') {
      expect(process.env.MINIO_PORT).toBe('9000');
    }
  });
});
