/**
 * Integration Test Setup Utilities
 *
 * Provides shared setup, teardown, and utility functions for integration tests
 */

import { Pool, PoolClient } from 'pg';
import { Redis } from 'ioredis';
import { QdrantClient } from '@qdrant/js-client-rest';
import { Driver, auth } from 'neo4j-driver';
import { AgentDB } from '../../lib/agentdb/agent-db';

export interface TestEnvironment {
  postgres: Pool;
  redis: Redis;
  qdrant: QdrantClient;
  neo4j: Driver;
  agentDB: AgentDB;
}

export interface SystemSnapshot {
  timestamp: Date;
  postgres: {
    jobCount: number;
    workerCount: number;
    queryCount: number;
  };
  redis: {
    keyCount: number;
    memoryUsed: number;
  };
  qdrant: {
    pointCount: number;
    collectionCount: number;
  };
  neo4j: {
    nodeCount: number;
    relationshipCount: number;
  };
}

/**
 * Setup complete test environment with all services
 */
export async function setupTestEnvironment(): Promise<TestEnvironment> {
  console.log('Setting up integration test environment...');

  // PostgreSQL connection
  const postgres = new Pool({
    host: process.env.POSTGRES_HOST || '172.18.0.5',
    port: parseInt(process.env.POSTGRES_PORT || '5432'),
    database: process.env.POSTGRES_DB || 'aeon_saas_dev',
    user: process.env.POSTGRES_USER || 'postgres',
    password: process.env.POSTGRES_PASSWORD || 'postgres',
    max: 10,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 5000,
  });

  // Test connection
  try {
    const client = await postgres.connect();
    await client.query('SELECT 1');
    client.release();
    console.log('✓ PostgreSQL connected');
  } catch (error) {
    console.error('✗ PostgreSQL connection failed:', error);
    throw error;
  }

  // Redis connection
  const redis = new Redis({
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
    db: parseInt(process.env.REDIS_DB || '1'),
    retryStrategy: (times) => Math.min(times * 50, 2000),
  });

  try {
    await redis.ping();
    console.log('✓ Redis connected');
  } catch (error) {
    console.error('✗ Redis connection failed:', error);
    throw error;
  }

  // Qdrant connection
  const qdrant = new QdrantClient({
    url: process.env.QDRANT_URL || 'http://172.18.0.3:6333',
  });

  try {
    await qdrant.getCollections();
    console.log('✓ Qdrant connected');
  } catch (error) {
    console.error('✗ Qdrant connection failed:', error);
    throw error;
  }

  // Neo4j connection
  const neo4j = Driver(
    process.env.NEO4J_URI || 'bolt://172.18.0.6:7687',
    auth.basic(
      process.env.NEO4J_USER || 'neo4j',
      process.env.NEO4J_PASSWORD || 'password'
    )
  );

  try {
    await neo4j.verifyConnectivity();
    console.log('✓ Neo4j connected');
  } catch (error) {
    console.error('✗ Neo4j connection failed:', error);
    throw error;
  }

  // AgentDB initialization
  const agentDB = new AgentDB({
    qdrantUrl: process.env.QDRANT_URL || 'http://172.18.0.3:6333',
    redisClient: redis,
    l1MaxSize: 100,
    l1TTL: 3600,
  });

  await agentDB.initialize();
  console.log('✓ AgentDB initialized');

  console.log('✓ Test environment ready');

  return {
    postgres,
    redis,
    qdrant,
    neo4j,
    agentDB,
  };
}

/**
 * Cleanup test environment and close connections
 */
export async function cleanupTestEnvironment(env: Partial<TestEnvironment>): Promise<void> {
  console.log('Cleaning up test environment...');

  if (env.agentDB) {
    await env.agentDB.disconnect();
    console.log('✓ AgentDB disconnected');
  }

  if (env.postgres) {
    await env.postgres.end();
    console.log('✓ PostgreSQL disconnected');
  }

  if (env.redis) {
    await env.redis.quit();
    console.log('✓ Redis disconnected');
  }

  if (env.neo4j) {
    await env.neo4j.close();
    console.log('✓ Neo4j disconnected');
  }

  console.log('✓ Test environment cleaned up');
}

/**
 * Clean all test data from databases
 */
export async function cleanTestData(env: TestEnvironment): Promise<void> {
  console.log('Cleaning test data...');

  // PostgreSQL: Truncate test tables
  if (env.postgres) {
    const tables = ['jobs', 'job_executions', 'job_dependencies', 'job_schedules', 'dead_letter_jobs', 'queries', 'query_checkpoints'];
    for (const table of tables) {
      try {
        await env.postgres.query(`TRUNCATE TABLE ${table} CASCADE`);
      } catch (error) {
        // Table might not exist yet
        console.warn(`Could not truncate ${table}:`, error.message);
      }
    }
    console.log('✓ PostgreSQL test data cleared');
  }

  // Redis: Flush test database
  if (env.redis) {
    await env.redis.flushdb();
    console.log('✓ Redis test data cleared');
  }

  // Qdrant: Delete test collections
  if (env.qdrant) {
    const collections = await env.qdrant.getCollections();
    const testCollections = collections.collections
      .filter(c => c.name.includes('test') || c.name.includes('integration'))
      .map(c => c.name);

    for (const collection of testCollections) {
      try {
        await env.qdrant.deleteCollection(collection);
      } catch (error) {
        console.warn(`Could not delete collection ${collection}:`, error.message);
      }
    }
    console.log('✓ Qdrant test collections cleared');
  }

  // Neo4j: Delete test nodes
  if (env.neo4j) {
    const session = env.neo4j.session();
    try {
      await session.run(`
        MATCH (n)
        WHERE n.testMarker = true OR n.equipmentId STARTS WITH 'TEST-'
        DETACH DELETE n
      `);
      console.log('✓ Neo4j test data cleared');
    } finally {
      await session.close();
    }
  }

  console.log('✓ Test data cleaned');
}

/**
 * Capture system state snapshot
 */
export async function captureSystemState(env: TestEnvironment): Promise<SystemSnapshot> {
  const snapshot: SystemSnapshot = {
    timestamp: new Date(),
    postgres: { jobCount: 0, workerCount: 0, queryCount: 0 },
    redis: { keyCount: 0, memoryUsed: 0 },
    qdrant: { pointCount: 0, collectionCount: 0 },
    neo4j: { nodeCount: 0, relationshipCount: 0 },
  };

  // PostgreSQL counts
  try {
    const jobResult = await env.postgres.query('SELECT COUNT(*) FROM jobs');
    snapshot.postgres.jobCount = parseInt(jobResult.rows[0].count);

    const queryResult = await env.postgres.query('SELECT COUNT(*) FROM queries');
    snapshot.postgres.queryCount = parseInt(queryResult.rows[0].count);
  } catch (error) {
    console.warn('PostgreSQL snapshot failed:', error.message);
  }

  // Redis stats
  try {
    const keys = await env.redis.keys('*');
    snapshot.redis.keyCount = keys.length;

    const info = await env.redis.info('memory');
    const match = info.match(/used_memory:(\d+)/);
    if (match) {
      snapshot.redis.memoryUsed = parseInt(match[1]);
    }
  } catch (error) {
    console.warn('Redis snapshot failed:', error.message);
  }

  // Qdrant stats
  try {
    const collections = await env.qdrant.getCollections();
    snapshot.qdrant.collectionCount = collections.collections.length;

    for (const collection of collections.collections) {
      const info = await env.qdrant.getCollection(collection.name);
      snapshot.qdrant.pointCount += info.points_count || 0;
    }
  } catch (error) {
    console.warn('Qdrant snapshot failed:', error.message);
  }

  // Neo4j stats
  try {
    const session = env.neo4j.session();
    try {
      const nodeResult = await session.run('MATCH (n) RETURN count(n) as count');
      snapshot.neo4j.nodeCount = nodeResult.records[0].get('count').toNumber();

      const relResult = await session.run('MATCH ()-[r]->() RETURN count(r) as count');
      snapshot.neo4j.relationshipCount = relResult.records[0].get('count').toNumber();
    } finally {
      await session.close();
    }
  } catch (error) {
    console.warn('Neo4j snapshot failed:', error.message);
  }

  return snapshot;
}

/**
 * Wait for condition with timeout
 */
export async function waitFor(
  condition: () => Promise<boolean>,
  options: {
    timeout?: number;
    interval?: number;
    description?: string;
  } = {}
): Promise<void> {
  const timeout = options.timeout || 10000;
  const interval = options.interval || 100;
  const description = options.description || 'condition';

  const startTime = Date.now();

  while (Date.now() - startTime < timeout) {
    if (await condition()) {
      return;
    }
    await new Promise(resolve => setTimeout(resolve, interval));
  }

  throw new Error(`Timeout waiting for ${description} after ${timeout}ms`);
}

/**
 * Measure execution time of async function
 */
export async function measureExecutionTime<T>(
  fn: () => Promise<T>
): Promise<{ result: T; duration: number }> {
  const startTime = Date.now();
  const result = await fn();
  const duration = Date.now() - startTime;
  return { result, duration };
}

/**
 * Retry function with exponential backoff
 */
export async function retry<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries?: number;
    initialDelay?: number;
    maxDelay?: number;
    backoffMultiplier?: number;
  } = {}
): Promise<T> {
  const maxRetries = options.maxRetries || 3;
  const initialDelay = options.initialDelay || 100;
  const maxDelay = options.maxDelay || 5000;
  const backoffMultiplier = options.backoffMultiplier || 2;

  let lastError: Error;
  let delay = initialDelay;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      if (attempt === maxRetries) {
        break;
      }

      await new Promise(resolve => setTimeout(resolve, delay));
      delay = Math.min(delay * backoffMultiplier, maxDelay);
    }
  }

  throw new Error(`Failed after ${maxRetries} retries: ${lastError!.message}`);
}

/**
 * Generate test agent configuration
 */
export function generateTestAgent(type: string = 'researcher'): any {
  return {
    type,
    name: `test-${type}-${Date.now()}`,
    capabilities: ['research', 'analysis', 'documentation'],
    config: {
      maxConcurrency: 5,
      timeout: 30000,
      retryPolicy: {
        maxRetries: 3,
        backoffMs: 1000,
      },
    },
    metadata: {
      testMarker: true,
      createdAt: new Date().toISOString(),
    },
  };
}

/**
 * Generate test job payload
 */
export function generateTestJob(type: string = 'analysis'): any {
  return {
    jobType: type,
    status: 'pending',
    priority: 50,
    payload: {
      action: 'test_action',
      parameters: {
        testMarker: true,
        data: `test-data-${Date.now()}`,
      },
    },
    maxRetries: 3,
    timeoutMs: 30000,
    metadata: {
      testRun: true,
      createdAt: new Date().toISOString(),
    },
  };
}

/**
 * Generate test query configuration
 */
export function generateTestQuery(model: string = 'claude-3-5-sonnet-20241022'): any {
  return {
    queryId: `test-query-${Date.now()}`,
    model,
    status: 'active',
    permissionMode: 'default',
    metadata: {
      testMarker: true,
      startedAt: new Date().toISOString(),
    },
  };
}

/**
 * Generate test equipment node
 */
export function generateTestEquipment(sector: string = 'Water'): any {
  const id = `TEST-${sector.toUpperCase()}-${Date.now()}`;
  return {
    equipmentId: id,
    name: `Test ${sector} Equipment ${Date.now()}`,
    equipmentType: `${sector}_Equipment`,
    sector,
    criticality: 'medium',
    tags: [
      'test',
      `GEO:${sector}`,
      'OPS:testing',
      'TECH:automated',
      `TIME:${new Date().getFullYear()}`,
    ],
    testMarker: true,
    createdAt: new Date().toISOString(),
  };
}

/**
 * Verify database connectivity
 */
export async function verifyConnectivity(env: TestEnvironment): Promise<boolean> {
  try {
    await env.postgres.query('SELECT 1');
    await env.redis.ping();
    await env.qdrant.getCollections();
    await env.neo4j.verifyConnectivity();
    return true;
  } catch (error) {
    console.error('Connectivity check failed:', error);
    return false;
  }
}

/**
 * Get test database statistics
 */
export async function getTestStats(env: TestEnvironment): Promise<any> {
  const stats = {
    postgres: {},
    redis: {},
    qdrant: {},
    neo4j: {},
  };

  try {
    const pgStats = await env.postgres.query(`
      SELECT
        (SELECT COUNT(*) FROM jobs) as job_count,
        (SELECT COUNT(*) FROM queries) as query_count,
        (SELECT COUNT(*) FROM job_executions) as execution_count
    `);
    stats.postgres = pgStats.rows[0];
  } catch (error) {
    stats.postgres = { error: error.message };
  }

  try {
    const redisKeys = await env.redis.keys('*');
    stats.redis = { keyCount: redisKeys.length };
  } catch (error) {
    stats.redis = { error: error.message };
  }

  try {
    const collections = await env.qdrant.getCollections();
    stats.qdrant = {
      collectionCount: collections.collections.length,
      collections: collections.collections.map(c => c.name),
    };
  } catch (error) {
    stats.qdrant = { error: error.message };
  }

  try {
    const session = env.neo4j.session();
    try {
      const result = await session.run(`
        MATCH (n)
        RETURN count(n) as nodeCount, labels(n)[0] as label
      `);
      stats.neo4j = {
        nodes: result.records.map(r => ({
          label: r.get('label'),
          count: r.get('nodeCount').toNumber(),
        })),
      };
    } finally {
      await session.close();
    }
  } catch (error) {
    stats.neo4j = { error: error.message };
  }

  return stats;
}
