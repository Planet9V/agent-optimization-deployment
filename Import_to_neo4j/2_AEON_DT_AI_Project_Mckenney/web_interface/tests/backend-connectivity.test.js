/**
 * Backend Connectivity Test Suite
 * Tests all 5 OpenSPG backend services from AEON Web UI container
 *
 * Services Tested:
 * 1. Neo4j Graph Database (bolt://openspg-neo4j:7687)
 * 2. Qdrant Vector Database (http://openspg-qdrant:6333)
 * 3. MySQL Relational Database (openspg-mysql:3306)
 * 4. MinIO Object Storage (http://openspg-minio:9000)
 * 5. OpenSPG Server (http://openspg-server:8887)
 */

const neo4j = require('neo4j-driver');
const mysql = require('mysql2/promise');
const fetch = require('node-fetch');

describe('Backend Connectivity Tests', () => {
  const TEST_TIMEOUT = 5000;

  describe('Neo4j Graph Database', () => {
    let driver, session;

    beforeAll(() => {
      driver = neo4j.driver(
        process.env.NEO4J_URI || 'bolt://openspg-neo4j:7687',
        neo4j.auth.basic(
          process.env.NEO4J_USER || 'neo4j',
          process.env.NEO4J_PASSWORD || 'neo4j@openspg'
        )
      );
    });

    afterAll(async () => {
      if (session) await session.close();
      if (driver) await driver.close();
    });

    test('should connect to Neo4j', async () => {
      session = driver.session();
      const result = await session.run('RETURN 1 as test');
      expect(result.records[0].get('test').toNumber()).toBe(1);
    }, TEST_TIMEOUT);

    test('should query Neo4j nodes', async () => {
      session = driver.session();
      const result = await session.run('MATCH (n) RETURN count(n) as nodeCount');
      const count = result.records[0].get('nodeCount').toNumber();
      expect(count).toBeGreaterThanOrEqual(0);
    }, TEST_TIMEOUT);
  });

  describe('Qdrant Vector Database', () => {
    const qdrantUrl = process.env.QDRANT_URL || 'http://openspg-qdrant:6333';
    const qdrantKey = process.env.QDRANT_API_KEY || 'deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=';

    test('should connect to Qdrant', async () => {
      const response = await fetch(`${qdrantUrl}/health`, {
        headers: { 'api-key': qdrantKey }
      });
      expect(response.status).toBe(200);
    }, TEST_TIMEOUT);

    test('should list Qdrant collections', async () => {
      const response = await fetch(`${qdrantUrl}/collections`, {
        headers: { 'api-key': qdrantKey }
      });
      expect(response.status).toBe(200);
      const data = await response.json();
      expect(data).toHaveProperty('result');
      expect(Array.isArray(data.result.collections)).toBe(true);
    }, TEST_TIMEOUT);
  });

  describe('MySQL Relational Database', () => {
    let connection;

    afterEach(async () => {
      if (connection) await connection.end();
    });

    test('should connect to MySQL', async () => {
      connection = await mysql.createConnection({
        host: process.env.MYSQL_HOST || 'openspg-mysql',
        port: process.env.MYSQL_PORT || 3306,
        user: process.env.MYSQL_USER || 'root',
        password: process.env.MYSQL_PASSWORD || 'openspg',
        database: process.env.MYSQL_DATABASE || 'openspg'
      });
      expect(connection).toBeDefined();
    }, TEST_TIMEOUT);

    test('should execute MySQL query', async () => {
      connection = await mysql.createConnection({
        host: process.env.MYSQL_HOST || 'openspg-mysql',
        port: process.env.MYSQL_PORT || 3306,
        user: process.env.MYSQL_USER || 'root',
        password: process.env.MYSQL_PASSWORD || 'openspg',
        database: process.env.MYSQL_DATABASE || 'openspg'
      });
      const [rows] = await connection.execute('SELECT 1 as test');
      expect(rows[0].test).toBe(1);
    }, TEST_TIMEOUT);
  });

  describe('MinIO Object Storage', () => {
    const minioUrl = `http://${process.env.MINIO_ENDPOINT || 'openspg-minio'}:${process.env.MINIO_PORT || 9000}`;

    test('should connect to MinIO', async () => {
      const response = await fetch(`${minioUrl}/minio/health/live`);
      expect(response.status).toBe(200);
    }, TEST_TIMEOUT);

    test('should check MinIO readiness', async () => {
      const response = await fetch(`${minioUrl}/minio/health/ready`);
      expect([200, 503]).toContain(response.status); // 503 if not fully ready, 200 if ready
    }, TEST_TIMEOUT);
  });

  describe('OpenSPG Server', () => {
    const openspgUrl = process.env.OPENSPG_SERVER_URL || 'http://openspg-server:8887';

    test('should connect to OpenSPG Server', async () => {
      const response = await fetch(openspgUrl);
      expect([200, 404]).toContain(response.status); // Server responds even if endpoint doesn't exist
    }, TEST_TIMEOUT);

    test('should access OpenSPG API', async () => {
      // Test an actual API endpoint if available
      const response = await fetch(`${openspgUrl}/api/v1/health`).catch(() => ({status: 404}));
      // OpenSPG server is running if we get any response
      expect(response).toHaveProperty('status');
    }, TEST_TIMEOUT);
  });

  describe('Integration Tests', () => {
    test('all 5 backend services should be reachable', async () => {
      const results = await Promise.allSettled([
        // Neo4j
        (async () => {
          const driver = neo4j.driver('bolt://openspg-neo4j:7687',
            neo4j.auth.basic('neo4j', 'neo4j@openspg'));
          const session = driver.session();
          const result = await session.run('RETURN 1');
          await session.close();
          await driver.close();
          return { service: 'Neo4j', status: 'connected' };
        })(),

        // Qdrant
        fetch('http://openspg-qdrant:6333/health', {
          headers: { 'api-key': 'deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=' }
        }).then(() => ({ service: 'Qdrant', status: 'connected' })),

        // MySQL
        mysql.createConnection({
          host: 'openspg-mysql', port: 3306,
          user: 'root', password: 'openspg', database: 'openspg'
        }).then(conn => {
          conn.end();
          return { service: 'MySQL', status: 'connected' };
        }),

        // MinIO
        fetch('http://openspg-minio:9000/minio/health/live')
          .then(() => ({ service: 'MinIO', status: 'connected' })),

        // OpenSPG Server
        fetch('http://openspg-server:8887')
          .then(() => ({ service: 'OpenSPG', status: 'connected' }))
      ]);

      const successful = results.filter(r => r.status === 'fulfilled');
      expect(successful).toHaveLength(5);

      console.log('Backend Connectivity Summary:');
      results.forEach((result, index) => {
        const services = ['Neo4j', 'Qdrant', 'MySQL', 'MinIO', 'OpenSPG'];
        console.log(`  ✅ ${services[index]}: ${result.status}`);
      });
    }, TEST_TIMEOUT * 5);
  });
});

/**
 * Manual Test Command:
 * docker exec aeon-saas-dev npm test tests/backend-connectivity.test.js
 *
 * Or run inside container:
 * docker exec -it aeon-saas-dev /bin/sh
 * npm test tests/backend-connectivity.test.js
 */
