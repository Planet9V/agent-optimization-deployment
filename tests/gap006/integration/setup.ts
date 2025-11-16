/**
 * GAP-006 Integration Test Setup
 * Provides shared test environment configuration and utilities
 */

import { Pool } from 'pg';
import Redis from 'ioredis';
import { execSync } from 'child_process';
import * as path from 'path';

export interface TestEnvironment {
  pool: Pool;
  redis: Redis;
  cleanup: () => Promise<void>;
}

/**
 * Initialize test environment with PostgreSQL and Redis connections
 */
export async function setupTestEnvironment(): Promise<TestEnvironment> {
  // PostgreSQL connection
  const pool = new Pool({
    host: process.env.POSTGRES_HOST || 'localhost',
    port: parseInt(process.env.POSTGRES_PORT || '5432'),
    database: process.env.POSTGRES_DB || 'gap006_test',
    user: process.env.POSTGRES_USER || 'postgres',
    password: process.env.POSTGRES_PASSWORD || 'postgres',
  });

  // Redis connection
  const redis = new Redis({
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
    password: process.env.REDIS_PASSWORD || undefined,
    db: parseInt(process.env.REDIS_DB || '1'), // Use separate DB for testing
  });

  // Verify schema exists (migrations already run in deployment)
  try {
    const tableCheck = await pool.query(`
      SELECT COUNT(*) as count
      FROM information_schema.tables
      WHERE table_schema = 'public'
        AND table_name IN ('jobs', 'workers', 'job_executions', 'dead_letter_queue', 'job_dependencies', 'worker_health_logs', 'state_snapshots')
    `);

    const tableCount = parseInt(tableCheck.rows[0].count);
    if (tableCount !== 7) {
      throw new Error(`Expected 7 GAP-006 tables, found ${tableCount}. Run migrations first.`);
    }

    console.log('✅ GAP-006 schema verified: 7 tables found');
  } catch (error) {
    console.error('Schema verification failed:', error);
    throw error;
  }

  // Cleanup function
  const cleanup = async () => {
    await pool.query(`
      TRUNCATE
        jobs,
        workers,
        job_executions,
        dead_letter_queue,
        job_dependencies,
        worker_health_logs,
        state_snapshots
      CASCADE
    `);
    await redis.flushdb();
    await pool.end();
    await redis.quit();
  };

  return { pool, redis, cleanup };
}

/**
 * Wait for condition with timeout
 */
export async function waitFor(
  condition: () => Promise<boolean>,
  timeoutMs: number = 5000,
  intervalMs: number = 100
): Promise<void> {
  const startTime = Date.now();

  while (Date.now() - startTime < timeoutMs) {
    if (await condition()) {
      return;
    }
    await new Promise(resolve => setTimeout(resolve, intervalMs));
  }

  throw new Error(`Condition not met within ${timeoutMs}ms`);
}

/**
 * Generate test job payload
 */
export function generateTestJobPayload(overrides: any = {}): any {
  return {
    jobType: 'test-job',
    payload: { data: 'test-data', timestamp: Date.now() },
    priority: 3,
    maxRetries: 3,
    timeoutMs: 30000,
    ...overrides,
  };
}

/**
 * Generate test worker configuration
 */
export function generateTestWorkerConfig(overrides: any = {}): any {
  return {
    workerName: `test-worker-${Date.now()}`,
    workerType: 'coordinator',
    capabilities: ['data-processing'],
    maxConcurrentJobs: 5,
    ...overrides,
  };
}

/**
 * Verify job state in database
 */
export async function verifyJobState(
  pool: Pool,
  jobId: string,
  expectedState: {
    status?: string;
    workerId?: string;
    retryCount?: number;
  }
): Promise<void> {
  const result = await pool.query(
    'SELECT status, worker_id, retry_count FROM jobs WHERE job_id = $1',
    [jobId]
  );

  if (result.rows.length === 0) {
    throw new Error(`Job ${jobId} not found`);
  }

  const job = result.rows[0];

  if (expectedState.status && job.status !== expectedState.status) {
    throw new Error(
      `Expected status ${expectedState.status}, got ${job.status}`
    );
  }

  if (expectedState.workerId && job.worker_id !== expectedState.workerId) {
    throw new Error(
      `Expected worker_id ${expectedState.workerId}, got ${job.worker_id}`
    );
  }

  if (
    expectedState.retryCount !== undefined &&
    job.retry_count !== expectedState.retryCount
  ) {
    throw new Error(
      `Expected retry_count ${expectedState.retryCount}, got ${job.retry_count}`
    );
  }
}

/**
 * Verify worker state in database
 */
export async function verifyWorkerState(
  pool: Pool,
  workerId: string,
  expectedState: {
    status?: string;
    currentLoad?: number;
  }
): Promise<void> {
  const result = await pool.query(
    'SELECT status, current_load FROM workers WHERE worker_id = $1',
    [workerId]
  );

  if (result.rows.length === 0) {
    throw new Error(`Worker ${workerId} not found`);
  }

  const worker = result.rows[0];

  if (expectedState.status && worker.status !== expectedState.status) {
    throw new Error(
      `Expected status ${expectedState.status}, got ${worker.status}`
    );
  }

  if (
    expectedState.currentLoad !== undefined &&
    worker.current_load !== expectedState.currentLoad
  ) {
    throw new Error(
      `Expected current_load ${expectedState.currentLoad}, got ${worker.current_load}`
    );
  }
}
