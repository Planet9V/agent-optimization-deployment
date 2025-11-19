import { NextResponse } from 'next/server';
import { getNeo4jDriver } from '@/lib/neo4j-enhanced';
import { getMySQLPool } from '@/lib/mysql';
import { getQdrantClient } from '@/lib/qdrant';
import { getMinIOClient } from '@/lib/minio';

/**
 * Comprehensive Health Check API Endpoint
 *
 * Tests connectivity to all OpenSPG backend services:
 * - Neo4j (bolt://openspg-neo4j:7687) - Graph database
 * - MySQL (openspg-mysql:3306) - Relational database
 * - Qdrant (http://openspg-qdrant:6333) - Vector database
 * - MinIO (openspg-minio:9000) - Object storage
 *
 * Returns JSON with per-service status, response times, and overall health.
 * Handles connection failures gracefully with timeout protection.
 */

// Service configuration
const SERVICE_TIMEOUT = 5000; // 5 second timeout per service
const OVERALL_TIMEOUT = 15000; // 15 second total timeout

interface ServiceHealth {
  status: 'ok' | 'error' | 'timeout';
  responseTime?: number;
  message?: string;
  details?: any;
}

interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  services: {
    neo4j: ServiceHealth;
    mysql: ServiceHealth;
    qdrant: ServiceHealth;
    minio: ServiceHealth;
  };
  overallHealth: string;
  metadata?: {
    environment: string;
    nodeVersion: string;
  };
}

/**
 * Wraps a promise with a timeout
 */
function withTimeout<T>(promise: Promise<T>, timeoutMs: number, serviceName: string): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new Error(`${serviceName} timeout after ${timeoutMs}ms`)), timeoutMs)
    ),
  ]);
}

/**
 * Test Neo4j connection
 */
async function checkNeo4j(): Promise<ServiceHealth> {
  const startTime = Date.now();
  let driver;

  try {
    driver = getNeo4jDriver();
    const session = driver.session();

    try {
      // Simple connectivity test
      await session.run('RETURN 1 as test');
      const responseTime = Date.now() - startTime;

      return {
        status: 'ok',
        responseTime,
        details: {
          uri: process.env.NEO4J_URI || 'bolt://openspg-neo4j:7687',
          database: 'neo4j'
        }
      };
    } finally {
      await session.close();
    }
  } catch (error) {
    const responseTime = Date.now() - startTime;
    return {
      status: 'error',
      responseTime,
      message: error instanceof Error ? error.message : 'Unknown Neo4j error',
      details: {
        uri: process.env.NEO4J_URI || 'bolt://openspg-neo4j:7687'
      }
    };
  }
}

/**
 * Test MySQL connection
 */
async function checkMySQL(): Promise<ServiceHealth> {
  const startTime = Date.now();

  try {
    const pool = getMySQLPool();

    // Simple connectivity test
    await pool.query('SELECT 1 as test');
    const responseTime = Date.now() - startTime;

    return {
      status: 'ok',
      responseTime,
      details: {
        host: process.env.MYSQL_HOST || 'openspg-mysql',
        port: parseInt(process.env.MYSQL_PORT || '3306'),
        database: process.env.MYSQL_DATABASE || 'openspg'
      }
    };
  } catch (error) {
    const responseTime = Date.now() - startTime;
    return {
      status: 'error',
      responseTime,
      message: error instanceof Error ? error.message : 'Unknown MySQL error',
      details: {
        host: process.env.MYSQL_HOST || 'openspg-mysql',
        port: parseInt(process.env.MYSQL_PORT || '3306')
      }
    };
  }
}

/**
 * Test Qdrant connection
 */
async function checkQdrant(): Promise<ServiceHealth> {
  const startTime = Date.now();

  try {
    const client = getQdrantClient();

    // Test by listing collections
    const collections = await client.getCollections();
    const responseTime = Date.now() - startTime;

    return {
      status: 'ok',
      responseTime,
      details: {
        url: process.env.QDRANT_URL || 'http://openspg-qdrant:6333',
        collections: collections.collections.length
      }
    };
  } catch (error) {
    const responseTime = Date.now() - startTime;
    return {
      status: 'error',
      responseTime,
      message: error instanceof Error ? error.message : 'Unknown Qdrant error',
      details: {
        url: process.env.QDRANT_URL || 'http://openspg-qdrant:6333'
      }
    };
  }
}

/**
 * Test MinIO connection
 */
async function checkMinIO(): Promise<ServiceHealth> {
  const startTime = Date.now();

  try {
    const client = getMinIOClient();

    // Test by listing buckets
    const buckets = await client.listBuckets();
    const responseTime = Date.now() - startTime;

    return {
      status: 'ok',
      responseTime,
      details: {
        endpoint: process.env.MINIO_ENDPOINT || 'openspg-minio:9000',
        buckets: buckets.length
      }
    };
  } catch (error) {
    const responseTime = Date.now() - startTime;
    return {
      status: 'error',
      responseTime,
      message: error instanceof Error ? error.message : 'Unknown MinIO error',
      details: {
        endpoint: process.env.MINIO_ENDPOINT || 'openspg-minio:9000'
      }
    };
  }
}

/**
 * GET /api/health - Health check endpoint
 */
export async function GET() {
  try {
    // Run all health checks in parallel for speed
    const [neo4jHealth, mysqlHealth, qdrantHealth, minioHealth] = await Promise.all([
      withTimeout(checkNeo4j(), SERVICE_TIMEOUT, 'Neo4j').catch((error): ServiceHealth => ({
        status: 'timeout',
        message: error.message
      })),
      withTimeout(checkMySQL(), SERVICE_TIMEOUT, 'MySQL').catch((error): ServiceHealth => ({
        status: 'timeout',
        message: error.message
      })),
      withTimeout(checkQdrant(), SERVICE_TIMEOUT, 'Qdrant').catch((error): ServiceHealth => ({
        status: 'timeout',
        message: error.message
      })),
      withTimeout(checkMinIO(), SERVICE_TIMEOUT, 'MinIO').catch((error): ServiceHealth => ({
        status: 'timeout',
        message: error.message
      }))
    ]);

    // Calculate overall health
    const services = {
      neo4j: neo4jHealth,
      mysql: mysqlHealth,
      qdrant: qdrantHealth,
      minio: minioHealth
    };

    const healthyCount = Object.values(services).filter(s => s.status === 'ok').length;
    const totalServices = Object.keys(services).length;

    let overallStatus: 'healthy' | 'degraded' | 'unhealthy';
    if (healthyCount === totalServices) {
      overallStatus = 'healthy';
    } else if (healthyCount >= totalServices / 2) {
      overallStatus = 'degraded';
    } else {
      overallStatus = 'unhealthy';
    }

    const response: HealthResponse = {
      status: overallStatus,
      timestamp: new Date().toISOString(),
      services,
      overallHealth: `${healthyCount}/${totalServices} services healthy`,
      metadata: {
        environment: process.env.NODE_ENV || 'development',
        nodeVersion: process.version
      }
    };

    // Return appropriate HTTP status code
    const statusCode = overallStatus === 'healthy' ? 200 : overallStatus === 'degraded' ? 207 : 503;

    return NextResponse.json(response, { status: statusCode });
  } catch (error) {
    // Catastrophic failure
    return NextResponse.json(
      {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        message: 'Health check failed catastrophically',
        error: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 503 }
    );
  }
}
