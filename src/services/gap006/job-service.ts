/**
 * File: job-service.ts
 * Created: 2025-11-15
 * Modified: 2025-11-15
 * Version: v1.0.0
 * Author: AEON FORGE
 * Purpose: Job lifecycle service with Redis atomic job acquisition for GAP-006
 * Dependencies: pg, ioredis
 * Status: ACTIVE
 */

import { Pool } from 'pg';
import Redis from 'ioredis';

interface JobConfig {
  jobType: string;
  payload: any;
  priority?: number;
  maxRetries?: number;
}

interface JobResult {
  jobId: string;
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  result?: any;
  error?: string;
}

class JobService {
  private pool: Pool;
  private redis: Redis;

  constructor() {
    this.pool = new Pool({
      host: process.env.POSTGRES_HOST || 'localhost',
      database: 'aeon_saas_dev',
      user: process.env.POSTGRES_USER || 'postgres',
      password: process.env.POSTGRES_PASSWORD,
      max: 20
    });

    this.redis = new Redis({
      host: process.env.REDIS_HOST || 'localhost',
      port: parseInt(process.env.REDIS_PORT || '6380'),
      password: process.env.REDIS_PASSWORD || 'redis@openspg',
      retryStrategy: (times) => Math.min(times * 50, 2000)
    });
  }

  /**
   * Create a new job
   * @param config Job configuration
   * @returns Job ID
   */
  async createJob(config: JobConfig): Promise<string> {
    // 1. Insert into PostgreSQL
    const result = await this.pool.query(
      `INSERT INTO jobs (job_type, status, priority, payload, max_retries, scheduled_at)
       VALUES ($1, $2, $3, $4, $5, NOW())
       RETURNING job_id`,
      [
        config.jobType,
        'PENDING',
        config.priority || 1,
        JSON.stringify(config.payload),
        config.maxRetries || 5
      ]
    );

    const jobId = result.rows[0].job_id;

    // 2. Add to Redis queue based on priority
    const queueName = this.getQueueForPriority(config.priority || 1);
    await this.redis.zadd(queueName, Date.now(), jobId);

    // 3. Store metadata
    await this.redis.hset(`gap006:job:${jobId}`, {
      jobType: config.jobType,
      status: 'PENDING',
      priority: config.priority || 1,
      createdAt: new Date().toISOString(),
      retryCount: 0
    });

    return jobId;
  }

  /**
   * Worker acquires job atomically using BRPOPLPUSH
   * @param workerId Worker identifier
   * @returns Job ID or null if no jobs available
   */
  async acquireJob(workerId: string): Promise<string | null> {
    // Try high priority first, then medium, then low
    const queues = [
      'gap006:high-priority-queue',
      'gap006:medium-priority-queue',
      'gap006:low-priority-queue'
    ];

    for (const queue of queues) {
      // BRPOPLPUSH: Atomic move from pending to processing
      const jobId = await this.redis.brpoplpush(
        queue,
        'gap006:processing-queue',
        5  // 5 second timeout
      );

      if (jobId) {
        // Update PostgreSQL
        await this.pool.query(
          `UPDATE jobs
           SET status = 'PROCESSING', worker_id = $2, started_at = NOW()
           WHERE job_id = $1`,
          [jobId, workerId]
        );

        // Create execution record
        await this.pool.query(
          `INSERT INTO job_executions (job_id, worker_id, attempt_number, status, started_at)
           SELECT $1, $2, COALESCE(MAX(attempt_number), 0) + 1, 'PROCESSING', NOW()
           FROM job_executions WHERE job_id = $1`,
          [jobId, workerId]
        );

        // Update metadata
        await this.redis.hset(`gap006:job:${jobId}`, {
          status: 'PROCESSING',
          workerId,
          startedAt: new Date().toISOString()
        });

        return jobId;
      }
    }

    return null;  // No jobs available
  }

  /**
   * Complete job successfully
   * @param jobId Job identifier
   * @param result Job result data
   */
  async completeJob(jobId: string, result: any): Promise<void> {
    const startTime = Date.now();

    // 1. Update PostgreSQL
    await this.pool.query(
      `UPDATE jobs
       SET status = 'COMPLETED', completed_at = NOW()
       WHERE job_id = $1`,
      [jobId]
    );

    const executionTime = Date.now() - startTime;

    // 2. Update execution record
    await this.pool.query(
      `UPDATE job_executions
       SET status = 'COMPLETED', completed_at = NOW(), execution_time_ms = $2
       WHERE job_id = $1 AND status = 'PROCESSING'`,
      [jobId, executionTime]
    );

    // 3. Remove from processing queue
    await this.redis.lrem('gap006:processing-queue', 1, jobId);

    // 4. Update worker stats
    await this.pool.query(
      `UPDATE workers
       SET total_jobs_completed = total_jobs_completed + 1,
           status = 'IDLE',
           current_job_id = NULL
       WHERE worker_id = (SELECT worker_id FROM jobs WHERE job_id = $1)`,
      [jobId]
    );

    // 5. Store result metadata
    await this.redis.hset(`gap006:job:${jobId}`, {
      status: 'COMPLETED',
      result: JSON.stringify(result),
      completedAt: new Date().toISOString(),
      executionTimeMs: executionTime
    });

    // Set expiry on job metadata
    await this.redis.expire(`gap006:job:${jobId}`, 86400);  // 24 hours
  }

  /**
   * Fail job with retry logic
   * @param jobId Job identifier
   * @param error Error message
   */
  async failJob(jobId: string, error: string): Promise<void> {
    // Get current retry count
    const result = await this.pool.query(
      `SELECT retry_count, max_retries FROM jobs WHERE job_id = $1`,
      [jobId]
    );

    if (result.rows.length === 0) {
      throw new Error(`Job not found: ${jobId}`);
    }

    const { retry_count, max_retries } = result.rows[0];

    if (retry_count < max_retries) {
      // Retry job
      await this.pool.query(
        `UPDATE jobs
         SET status = 'PENDING', retry_count = retry_count + 1, error_message = $2
         WHERE job_id = $1`,
        [jobId, error]
      );

      // Re-add to queue with exponential backoff
      const backoffSeconds = Math.pow(2, retry_count) * 10;
      const retryTime = Date.now() + (backoffSeconds * 1000);
      await this.redis.zadd('gap006:medium-priority-queue', retryTime, jobId);

      // Update metadata
      await this.redis.hset(`gap006:job:${jobId}`, {
        status: 'PENDING',
        retryCount: retry_count + 1,
        lastError: error,
        retryScheduledAt: new Date(retryTime).toISOString()
      });
    } else {
      // Move to dead letter queue
      await this.pool.query(
        `UPDATE jobs SET status = 'FAILED', error_message = $2 WHERE job_id = $1`,
        [jobId, error]
      );

      // Insert into dead_letter_queue
      await this.pool.query(
        `INSERT INTO dead_letter_queue (original_job_id, job_type, payload, failure_reason, retry_count, last_error)
         SELECT job_id, job_type, payload, $2, retry_count, error_message
         FROM jobs WHERE job_id = $1`,
        [jobId, error]
      );

      // Add to Redis dead letter queue
      await this.redis.zadd('gap006:dead-letter-queue', Date.now(), jobId);

      // Update metadata
      await this.redis.hset(`gap006:job:${jobId}`, {
        status: 'FAILED',
        finalError: error,
        failedAt: new Date().toISOString()
      });
    }

    // Update execution record
    await this.pool.query(
      `UPDATE job_executions
       SET status = 'FAILED', completed_at = NOW(), error_message = $2
       WHERE job_id = $1 AND status = 'PROCESSING'`,
      [jobId, error]
    );

    // Remove from processing queue
    await this.redis.lrem('gap006:processing-queue', 1, jobId);
  }

  /**
   * Get queue name based on priority level
   * @param priority Priority value (1-5)
   * @returns Queue name
   */
  private getQueueForPriority(priority: number): string {
    if (priority >= 4) return 'gap006:high-priority-queue';
    if (priority >= 2) return 'gap006:medium-priority-queue';
    return 'gap006:low-priority-queue';
  }

  /**
   * Get job status
   * @param jobId Job identifier
   * @returns Job result
   */
  async getJobStatus(jobId: string): Promise<JobResult> {
    const result = await this.pool.query(
      `SELECT status, error_message FROM jobs WHERE job_id = $1`,
      [jobId]
    );

    if (result.rows.length === 0) {
      throw new Error(`Job not found: ${jobId}`);
    }

    const metadata = await this.redis.hgetall(`gap006:job:${jobId}`);

    return {
      jobId,
      status: result.rows[0].status,
      result: metadata.result ? JSON.parse(metadata.result) : undefined,
      error: result.rows[0].error_message
    };
  }

  /**
   * Close connections
   */
  async close(): Promise<void> {
    await this.pool.end();
    await this.redis.quit();
  }
}

export default JobService;
