/**
 * Service Connectivity Test Suite
 * Validates actual connectivity to all 4 external services
 */

import { describe, it, expect, beforeAll } from '@jest/globals';
import neo4j from 'neo4j-driver';
import mysql from 'mysql2/promise';
import { QdrantClient } from '@qdrant/js-client-rest';
import * as Minio from 'minio';

const TIMEOUT = 15000; // 15 seconds

describe('Neo4j Connectivity', () => {
  let driver: neo4j.Driver;
  const uri = process.env.NEO4J_URI || 'bolt://localhost:7687';
  const user = process.env.NEO4J_USER || 'neo4j';
  const password = process.env.NEO4J_PASSWORD || 'password';

  beforeAll(() => {
    driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
  });

  afterAll(async () => {
    await driver.close();
  });

  it('should connect to Neo4j', async () => {
    const session = driver.session();
    try {
      await session.run('RETURN 1 as num');
      expect(true).toBe(true);
    } finally {
      await session.close();
    }
  }, TIMEOUT);

  it('should execute Cypher queries', async () => {
    const session = driver.session();
    try {
      const result = await session.run('RETURN 42 as answer');
      const record = result.records[0];
      expect(record.get('answer').toNumber()).toBe(42);
    } finally {
      await session.close();
    }
  }, TIMEOUT);

  it('should verify database is accessible', async () => {
    const session = driver.session();
    try {
      const result = await session.run('CALL dbms.components() YIELD name, versions');
      expect(result.records.length).toBeGreaterThan(0);
    } finally {
      await session.close();
    }
  }, TIMEOUT);

  it('should respond within 2 seconds', async () => {
    const session = driver.session();
    const start = Date.now();

    try {
      await session.run('RETURN 1');
      const duration = Date.now() - start;
      expect(duration).toBeLessThan(2000);
    } finally {
      await session.close();
    }
  }, TIMEOUT);

  it('should handle concurrent queries', async () => {
    const queries = Array(5).fill(null).map(async (_, i) => {
      const session = driver.session();
      try {
        const result = await session.run('RETURN $num as num', { num: i });
        return result.records[0].get('num').toNumber();
      } finally {
        await session.close();
      }
    });

    const results = await Promise.all(queries);
    expect(results).toEqual([0, 1, 2, 3, 4]);
  }, TIMEOUT);
});

describe('MySQL Connectivity', () => {
  const config = {
    host: process.env.MYSQL_HOST || 'localhost',
    port: parseInt(process.env.MYSQL_PORT || '3306'),
    user: process.env.MYSQL_USER || 'root',
    password: process.env.MYSQL_PASSWORD || 'password',
    database: process.env.MYSQL_DATABASE || 'test'
  };

  it('should connect to MySQL', async () => {
    const connection = await mysql.createConnection(config);
    await connection.ping();
    await connection.end();
    expect(true).toBe(true);
  }, TIMEOUT);

  it('should execute SQL queries', async () => {
    const connection = await mysql.createConnection(config);
    try {
      const [rows] = await connection.query('SELECT 42 as answer');
      expect((rows as any)[0].answer).toBe(42);
    } finally {
      await connection.end();
    }
  }, TIMEOUT);

  it('should verify database exists', async () => {
    const connection = await mysql.createConnection(config);
    try {
      const [rows] = await connection.query('SELECT DATABASE() as db');
      expect((rows as any)[0].db).toBe(config.database);
    } finally {
      await connection.end();
    }
  }, TIMEOUT);

  it('should respond within 2 seconds', async () => {
    const connection = await mysql.createConnection(config);
    const start = Date.now();

    try {
      await connection.query('SELECT 1');
      const duration = Date.now() - start;
      expect(duration).toBeLessThan(2000);
    } finally {
      await connection.end();
    }
  }, TIMEOUT);

  it('should handle concurrent queries', async () => {
    const connection = await mysql.createConnection(config);

    try {
      const queries = Array(5).fill(null).map((_, i) =>
        connection.query('SELECT ? as num', [i])
      );

      const results = await Promise.all(queries);
      const values = results.map(([rows]) => (rows as any)[0].num);
      expect(values).toEqual([0, 1, 2, 3, 4]);
    } finally {
      await connection.end();
    }
  }, TIMEOUT);

  it('should support transactions', async () => {
    const connection = await mysql.createConnection(config);

    try {
      await connection.beginTransaction();
      await connection.query('SELECT 1');
      await connection.commit();
      expect(true).toBe(true);
    } catch (error) {
      await connection.rollback();
      throw error;
    } finally {
      await connection.end();
    }
  }, TIMEOUT);
});

describe('Qdrant Connectivity', () => {
  const client = new QdrantClient({
    url: process.env.QDRANT_URL || 'http://localhost:6333',
    apiKey: process.env.QDRANT_API_KEY
  });

  it('should connect to Qdrant', async () => {
    const health = await client.api('cluster').clusterStatus();
    expect(health).toBeDefined();
  }, TIMEOUT);

  it('should list collections', async () => {
    const collections = await client.getCollections();
    expect(collections).toHaveProperty('collections');
    expect(Array.isArray(collections.collections)).toBe(true);
  }, TIMEOUT);

  it('should respond within 2 seconds', async () => {
    const start = Date.now();
    await client.api('cluster').clusterStatus();
    const duration = Date.now() - start;
    expect(duration).toBeLessThan(2000);
  }, TIMEOUT);

  it('should handle collection operations', async () => {
    const testCollection = 'test_collection_' + Date.now();

    try {
      // Create collection
      await client.createCollection(testCollection, {
        vectors: { size: 4, distance: 'Cosine' }
      });

      // Verify collection exists
      const collections = await client.getCollections();
      const exists = collections.collections.some(c => c.name === testCollection);
      expect(exists).toBe(true);

      // Delete collection
      await client.deleteCollection(testCollection);
    } catch (error) {
      // Cleanup if test fails
      try {
        await client.deleteCollection(testCollection);
      } catch {}
      throw error;
    }
  }, TIMEOUT);

  it('should support vector operations', async () => {
    const testCollection = 'test_vectors_' + Date.now();

    try {
      await client.createCollection(testCollection, {
        vectors: { size: 4, distance: 'Cosine' }
      });

      // Insert vector
      await client.upsert(testCollection, {
        points: [{
          id: 1,
          vector: [0.1, 0.2, 0.3, 0.4],
          payload: { test: true }
        }]
      });

      // Search vector
      const results = await client.search(testCollection, {
        vector: [0.1, 0.2, 0.3, 0.4],
        limit: 1
      });

      expect(results.length).toBeGreaterThan(0);
      expect(results[0].id).toBe(1);

      await client.deleteCollection(testCollection);
    } catch (error) {
      try {
        await client.deleteCollection(testCollection);
      } catch {}
      throw error;
    }
  }, TIMEOUT);
});

describe('MinIO Connectivity', () => {
  const client = new Minio.Client({
    endPoint: process.env.MINIO_ENDPOINT || 'localhost',
    port: parseInt(process.env.MINIO_PORT || '9000'),
    useSSL: process.env.MINIO_USE_SSL === 'true',
    accessKey: process.env.MINIO_ACCESS_KEY || 'minioadmin',
    secretKey: process.env.MINIO_SECRET_KEY || 'minioadmin'
  });

  it('should connect to MinIO', async () => {
    const buckets = await client.listBuckets();
    expect(Array.isArray(buckets)).toBe(true);
  }, TIMEOUT);

  it('should list buckets', async () => {
    const buckets = await client.listBuckets();
    expect(buckets).toBeDefined();
    expect(Array.isArray(buckets)).toBe(true);
  }, TIMEOUT);

  it('should respond within 2 seconds', async () => {
    const start = Date.now();
    await client.listBuckets();
    const duration = Date.now() - start;
    expect(duration).toBeLessThan(2000);
  }, TIMEOUT);

  it('should handle bucket operations', async () => {
    const testBucket = 'test-bucket-' + Date.now();

    try {
      // Create bucket
      await client.makeBucket(testBucket, 'us-east-1');

      // Verify bucket exists
      const exists = await client.bucketExists(testBucket);
      expect(exists).toBe(true);

      // Remove bucket
      await client.removeBucket(testBucket);
    } catch (error) {
      // Cleanup if test fails
      try {
        await client.removeBucket(testBucket);
      } catch {}
      throw error;
    }
  }, TIMEOUT);

  it('should support object operations', async () => {
    const testBucket = 'test-objects-' + Date.now();
    const testObject = 'test.txt';
    const testContent = 'Hello MinIO!';

    try {
      await client.makeBucket(testBucket, 'us-east-1');

      // Put object
      await client.putObject(testBucket, testObject, Buffer.from(testContent));

      // Get object
      const stream = await client.getObject(testBucket, testObject);
      const chunks: Buffer[] = [];

      for await (const chunk of stream) {
        chunks.push(chunk);
      }

      const content = Buffer.concat(chunks).toString();
      expect(content).toBe(testContent);

      // Remove object and bucket
      await client.removeObject(testBucket, testObject);
      await client.removeBucket(testBucket);
    } catch (error) {
      try {
        await client.removeObject(testBucket, testObject);
        await client.removeBucket(testBucket);
      } catch {}
      throw error;
    }
  }, TIMEOUT);
});

describe('Cross-Service Integration', () => {
  it('should have all 4 services available simultaneously', async () => {
    const results = await Promise.allSettled([
      // Neo4j check
      (async () => {
        const driver = neo4j.driver(
          process.env.NEO4J_URI || 'bolt://localhost:7687',
          neo4j.auth.basic(
            process.env.NEO4J_USER || 'neo4j',
            process.env.NEO4J_PASSWORD || 'password'
          )
        );
        const session = driver.session();
        try {
          await session.run('RETURN 1');
        } finally {
          await session.close();
          await driver.close();
        }
      })(),

      // MySQL check
      (async () => {
        const connection = await mysql.createConnection({
          host: process.env.MYSQL_HOST || 'localhost',
          port: parseInt(process.env.MYSQL_PORT || '3306'),
          user: process.env.MYSQL_USER || 'root',
          password: process.env.MYSQL_PASSWORD || 'password'
        });
        await connection.ping();
        await connection.end();
      })(),

      // Qdrant check
      (async () => {
        const client = new QdrantClient({
          url: process.env.QDRANT_URL || 'http://localhost:6333'
        });
        await client.api('cluster').clusterStatus();
      })(),

      // MinIO check
      (async () => {
        const client = new Minio.Client({
          endPoint: process.env.MINIO_ENDPOINT || 'localhost',
          port: parseInt(process.env.MINIO_PORT || '9000'),
          useSSL: false,
          accessKey: process.env.MINIO_ACCESS_KEY || 'minioadmin',
          secretKey: process.env.MINIO_SECRET_KEY || 'minioadmin'
        });
        await client.listBuckets();
      })()
    ]);

    const failures = results.filter(r => r.status === 'rejected');

    if (failures.length > 0) {
      console.error('Service failures:', failures);
    }

    expect(failures.length).toBe(0);
  }, TIMEOUT);
});
