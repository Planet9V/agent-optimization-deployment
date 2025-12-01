/**
 * File: JobService.ts
 * Created: 2025-11-15
 * Modified: 2025-11-15
 * Version: v2.0.0 (Phase 2: Dependency Resolution + Priority Inheritance)
 * Author: AEON FORGE
 * Purpose: Job lifecycle service with Redis atomic job acquisition for GAP-006
 * Dependencies: pg, ioredis
 * Status: ACTIVE
 *
 * Phase 2 Features:
 * - Job dependency resolution (parent/child relationships)
 * - Priority inheritance (child jobs inherit parent priority)
 * - Fair scheduling policies (prevent starvation)
 * - Cascading job execution (auto-trigger dependent jobs)
 */

import { Pool } from 'pg';
import Redis from 'ioredis';
import { v4 as uuidv4 } from 'uuid';

interface JobConfig {
  jobType: string;
  payload: any;
  priority?: number;
  maxRetries?: number;
  timeoutMs?: number;
  dependsOn?: string[];  // Phase 2: Array of job IDs this job depends on
  inheritPriority?: boolean; // Phase 2: Whether to inherit priority from dependencies (default: true)
}

interface JobResult {
  jobId: string;
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  result?: any;
  error?: string;
}

export class JobService {
  private pool: Pool;
  private redis: Redis;

  constructor(pool: Pool, redis: Redis) {
    this.pool = pool;
    this.redis = redis;
  }

  /**
   * Create a new job (Phase 2: with dependency resolution and priority inheritance)
   */
  async createJob(config: JobConfig): Promise<string> {
    const jobId = uuidv4();
    let priority = config.priority !== undefined ? config.priority : 3; // Default medium priority
    const maxRetries = config.maxRetries !== undefined ? config.maxRetries : 3;
    const timeoutMs = config.timeoutMs !== undefined ? config.timeoutMs : 300000; // 5 minutes default
    const inheritPriority = config.inheritPriority !== undefined ? config.inheritPriority : true;

    try {
      // Phase 2: Priority inheritance - check if we should inherit priority from dependencies
      if (config.dependsOn && config.dependsOn.length > 0 && inheritPriority) {
        const maxDependencyPriority = await this.getMaxDependencyPriority(config.dependsOn);
        if (maxDependencyPriority !== null && maxDependencyPriority > priority) {
          priority = maxDependencyPriority; // Inherit higher priority from dependencies
        }
      }

      // Insert job into PostgreSQL
      await this.pool.query(
        `INSERT INTO jobs (
          job_id,
          job_type,
          status,
          priority,
          payload,
          max_retries,
          retry_count,
          timeout_ms,
          created_at,
          updated_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW(), NOW())`,
        [
          jobId,
          config.jobType,
          'PENDING',
          priority,
          JSON.stringify(config.payload),
          maxRetries,
          0,
          timeoutMs
        ]
      );

      // Phase 2: Create dependency relationships if specified
      if (config.dependsOn && config.dependsOn.length > 0) {
        await this.createDependencies(jobId, config.dependsOn);
      }

      // Phase 2: Only queue job if it has no unmet dependencies
      const hasUnmetDependencies = await this.hasUnmetDependencies(jobId);
      if (!hasUnmetDependencies) {
        // Push job to appropriate priority queue in Redis
        const queueKey = this.getQueueKey(priority);
        await this.redis.lpush(queueKey, jobId);
      }
      // Otherwise, job stays in database with PENDING status until dependencies complete

      return jobId;
    } catch (error) {
      console.error('Job creation error:', error);
      throw new Error(`Failed to create job: ${error.message}`);
    }
  }

  /**
   * Phase 2: Get maximum priority from dependency jobs
   */
  private async getMaxDependencyPriority(dependsOnJobIds: string[]): Promise<number | null> {
    try {
      const result = await this.pool.query(
        'SELECT MAX(priority) as max_priority FROM jobs WHERE job_id = ANY($1)',
        [dependsOnJobIds]
      );
      return result.rows[0]?.max_priority || null;
    } catch (error) {
      console.error('Error getting dependency priority:', error);
      return null;
    }
  }

  /**
   * Phase 2: Create dependency relationships (triggers circular dependency check)
   */
  private async createDependencies(jobId: string, dependsOnJobIds: string[]): Promise<void> {
    try {
      for (const dependsOnJobId of dependsOnJobIds) {
        await this.pool.query(
          `INSERT INTO job_dependencies (job_id, depends_on_job_id)
           VALUES ($1, $2)
           ON CONFLICT (job_id, depends_on_job_id) DO NOTHING`,
          [jobId, dependsOnJobId]
        );
      }
    } catch (error) {
      // Circular dependency trigger will raise exception
      throw new Error(`Failed to create dependencies: ${error.message}`);
    }
  }

  /**
   * Phase 2: Check if job has unmet dependencies
   */
  private async hasUnmetDependencies(jobId: string): Promise<boolean> {
    try {
      const result = await this.pool.query(
        `SELECT COUNT(*) as count
         FROM job_dependencies jd
         INNER JOIN jobs j ON j.job_id = jd.depends_on_job_id
         WHERE jd.job_id = $1
         AND j.status NOT IN ('COMPLETED')`,
        [jobId]
      );
      const unmetCount = parseInt(result.rows[0]?.count || '0');
      return unmetCount > 0;
    } catch (error) {
      console.error('Error checking dependencies:', error);
      return false;
    }
  }

  /**
   * Phase 2: Trigger dependent jobs (called after job completion)
   */
  private async triggerDependentJobs(completedJobId: string): Promise<void> {
    try {
      // Find jobs that depended on this completed job
      const result = await this.pool.query(
        `SELECT DISTINCT jd.job_id, j.priority, j.status
         FROM job_dependencies jd
         INNER JOIN jobs j ON j.job_id = jd.job_id
         WHERE jd.depends_on_job_id = $1
         AND j.status = 'PENDING'`,
        [completedJobId]
      );

      // Check each dependent job - queue it if all its dependencies are now met
      for (const row of result.rows) {
        const dependentJobId = row.job_id;
        const priority = row.priority;

        const hasUnmet = await this.hasUnmetDependencies(dependentJobId);

        if (!hasUnmet) {
          // All dependencies met - queue the job
          const queueKey = this.getQueueKey(priority);
          await this.redis.lpush(queueKey, dependentJobId);
        }
      }
    } catch (error) {
      console.error('Error triggering dependent jobs:', error);
      // Don't throw - this is a best-effort operation
    }
  }

  /**
   * Acquire a job for processing (Phase 2: with fair scheduling to prevent starvation)
   * Phase 4: Added worker verification and retry logic to prevent race conditions
   */
  async acquireJob(workerId: string, timeoutSeconds: number = 5): Promise<string | null> {
    const MAX_RETRIES = 3;
    const RETRY_DELAY_MS = 50; // 50ms between retries

    for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
      try {
        // Phase 4: Verify worker exists before attempting acquisition
        const workerCheck = await this.pool.query(
          'SELECT worker_id FROM workers WHERE worker_id = $1',
          [workerId]
        );

        if (workerCheck.rows.length === 0) {
          if (attempt < MAX_RETRIES - 1) {
            // Worker not found, wait and retry (might be transaction lag)
            await new Promise(resolve => setTimeout(resolve, RETRY_DELAY_MS * (attempt + 1)));
            continue;
          } else {
            console.error(`Worker ${workerId} not found after ${MAX_RETRIES} attempts`);
            return null;
          }
        }

        // Phase 2: Fair scheduling - promote long-waiting low-priority jobs periodically
        await this.promoteStalledJobs();

        // Try high priority queue first
        let jobId = await this.redis.brpoplpush(
          'job:queue:high',
          `job:processing:${workerId}`,
          0.1
        );

        // Then medium priority
        if (!jobId) {
          jobId = await this.redis.brpoplpush(
            'job:queue:medium',
            `job:processing:${workerId}`,
            0.1
          );
        }

        // Finally low priority
        if (!jobId) {
          jobId = await this.redis.brpoplpush(
            'job:queue:low',
            `job:processing:${workerId}`,
            0.1
          );
        }

        if (jobId) {
          // Phase 4: Use explicit transaction to ensure atomicity
          const client = await this.pool.connect();
          try {
            await client.query('BEGIN');

            // Update job status in PostgreSQL
            await client.query(
              `UPDATE jobs SET
                status = 'PROCESSING',
                worker_id = $1,
                started_at = NOW(),
                updated_at = NOW()
               WHERE job_id = $2`,
              [workerId, jobId]
            );

            // Create job execution record (foreign key constraint requires worker to exist)
            await client.query(
              `INSERT INTO job_executions (
                execution_id,
                job_id,
                worker_id,
                attempt_number,
                status,
                execution_status,
                started_at,
                created_at
              ) VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW())`,
              [uuidv4(), jobId, workerId, 1, 'RUNNING', 'RUNNING']
            );

            await client.query('COMMIT');
            return jobId;
          } catch (txError) {
            await client.query('ROLLBACK');

            // If this was a foreign key violation and we have retries left, try again
            if (txError.code === '23503' && attempt < MAX_RETRIES - 1) {
              console.warn(`Foreign key violation on attempt ${attempt + 1}, retrying...`);
              // Put job back in queue
              const priority = await this.getJobPriority(jobId);
              if (priority !== null) {
                const queueKey = this.getQueueKey(priority);
                await this.redis.lpush(queueKey, jobId);
                await this.redis.lrem(`job:processing:${workerId}`, 1, jobId);
              }
              await new Promise(resolve => setTimeout(resolve, RETRY_DELAY_MS * (attempt + 1)));
              continue;
            }
            throw txError;
          } finally {
            client.release();
          }
        }

        return null;
      } catch (error) {
        if (attempt === MAX_RETRIES - 1) {
          console.error('Job acquisition error after retries:', error);
          return null;
        }
        // Continue to next retry
      }
    }

    return null;
  }

  /**
   * Phase 4: Helper to get job priority for re-queuing
   */
  private async getJobPriority(jobId: string): Promise<number | null> {
    try {
      const result = await this.pool.query(
        'SELECT priority FROM jobs WHERE job_id = $1',
        [jobId]
      );
      return result.rows[0]?.priority || null;
    } catch (error) {
      console.error('Error getting job priority:', error);
      return null;
    }
  }

  /**
   * Complete a job successfully
   */
  async completeJob(jobId: string, result: any): Promise<void> {
    try {
      // Get job info with started_at as epoch milliseconds
      const jobResult = await this.pool.query(
        `SELECT
          worker_id,
          started_at,
          ROUND(EXTRACT(EPOCH FROM started_at) * 1000) AS started_at_ms
         FROM jobs
         WHERE job_id = $1`,
        [jobId]
      );

      if (jobResult.rows.length === 0) {
        throw new Error(`Job ${jobId} not found`);
      }

      const workerId = jobResult.rows[0].worker_id;
      const startedAtMs = jobResult.rows[0].started_at_ms;

      // Update job status
      await this.pool.query(
        `UPDATE jobs SET
          status = 'COMPLETED',
          result = $1,
          completed_at = NOW(),
          updated_at = NOW()
         WHERE job_id = $2`,
        [JSON.stringify(result), jobId]
      );

      // Update job execution - calculate duration using epoch milliseconds
      const now = Date.now();
      const durationMs = startedAtMs ? Math.round(now - startedAtMs) : 0;

      await this.pool.query(
        `UPDATE job_executions SET
          status = 'COMPLETED',
          execution_status = 'COMPLETED',
          completed_at = NOW(),
          duration_ms = $1
         WHERE job_id = $2 AND execution_status = 'RUNNING'`,
        [durationMs, jobId]
      );

      // Remove from processing queue
      if (workerId) {
        await this.redis.lrem(`job:processing:${workerId}`, 1, jobId);
      }

      // Decrement worker load
      if (workerId) {
        await this.pool.query(
          `UPDATE workers SET
            current_load = GREATEST(0, current_load - 1),
            updated_at = NOW()
           WHERE worker_id = $1`,
          [workerId]
        );
      }

      // Phase 2: Trigger any dependent jobs that are now ready to execute
      await this.triggerDependentJobs(jobId);
    } catch (error) {
      console.error('Job completion error:', error);
      throw new Error(`Failed to complete job: ${error.message}`);
    }
  }

  /**
   * Fail a job
   */
  async failJob(jobId: string, errorInfo: { error: string; stack?: string }): Promise<void> {
    try {
      const jobResult = await this.pool.query(
        'SELECT retry_count, max_retries, worker_id, priority FROM jobs WHERE job_id = $1',
        [jobId]
      );

      if (jobResult.rows.length === 0) {
        throw new Error(`Job ${jobId} not found`);
      }

      const { retry_count, max_retries, worker_id, priority } = jobResult.rows[0];

      // Check if we should retry
      if (retry_count < max_retries) {
        // Increment retry count and reset to PENDING
        await this.pool.query(
          `UPDATE jobs SET
            status = 'PENDING',
            retry_count = retry_count + 1,
            error_message = $1,
            updated_at = NOW()
           WHERE job_id = $2`,
          [JSON.stringify(errorInfo), jobId]
        );

        // Re-queue with exponential backoff
        const backoffMs = Math.min(1000 * Math.pow(2, retry_count), 60000);

        // In test environment, re-queue immediately; in production, use exponential backoff
        if (process.env.NODE_ENV === 'test') {
          const queueKey = this.getQueueKey(priority);
          await this.redis.lpush(queueKey, jobId);
        } else {
          setTimeout(async () => {
            const queueKey = this.getQueueKey(priority);
            await this.redis.lpush(queueKey, jobId);
          }, backoffMs);
        }

        // Remove from processing queue
        if (worker_id) {
          await this.redis.lrem(`job:processing:${worker_id}`, 1, jobId);
        }
      } else {
        // Max retries exceeded - move to FAILED and DLQ
        await this.pool.query(
          `UPDATE jobs SET
            status = 'FAILED',
            error_message = $1,
            completed_at = NOW(),
            updated_at = NOW()
           WHERE job_id = $2`,
          [JSON.stringify(errorInfo), jobId]
        );

        // Insert into dead letter queue
        await this.pool.query(
          `INSERT INTO dead_letter_queue (
            dlq_id,
            original_job_id,
            job_type,
            payload,
            retry_count,
            error_message,
            created_at
          )
          SELECT
            $1,
            job_id,
            job_type,
            payload,
            retry_count,
            $2,
            NOW()
          FROM jobs
          WHERE job_id = $3`,
          [uuidv4(), errorInfo.error, jobId]
        );

        // Remove from processing queue
        if (worker_id) {
          await this.redis.lrem(`job:processing:${worker_id}`, 1, jobId);
        }

        // Update job execution
        await this.pool.query(
          `UPDATE job_executions SET
            status = 'FAILED',
            execution_status = 'FAILED',
            error_message = $1,
            completed_at = NOW()
           WHERE job_id = $2 AND execution_status = 'RUNNING'`,
          [errorInfo.error, jobId]
        );
      }

      // Decrement worker load
      if (worker_id) {
        await this.pool.query(
          `UPDATE workers SET
            current_load = GREATEST(0, current_load - 1),
            updated_at = NOW()
           WHERE worker_id = $1`,
          [worker_id]
        );
      }
    } catch (error) {
      console.error('Job failure error:', error);
      throw new Error(`Failed to handle job failure: ${error.message}`);
    }
  }

  /**
   * Phase 2: Promote long-waiting jobs to prevent starvation (fair scheduling)
   * Jobs waiting longer than thresholds get promoted to higher priority queues
   */
  private async promoteStalledJobs(): Promise<void> {
    try {
      const now = Date.now();

      // Define starvation thresholds (milliseconds)
      const LOW_TO_MEDIUM_THRESHOLD = 60000;  // 1 minute - low priority jobs
      const MEDIUM_TO_HIGH_THRESHOLD = 120000; // 2 minutes - medium priority jobs

      // Promote low priority jobs that have been waiting > 1 minute
      const lowJobIds = await this.redis.lrange('job:queue:low', 0, -1);
      for (const jobId of lowJobIds) {
        const result = await this.pool.query(
          `SELECT ROUND(EXTRACT(EPOCH FROM created_at) * 1000) AS created_at_ms, priority
           FROM jobs WHERE job_id = $1 AND status = 'PENDING'`,
          [jobId]
        );

        if (result.rows.length > 0) {
          const createdAtMs = result.rows[0].created_at_ms;
          const waitTimeMs = now - createdAtMs;

          if (waitTimeMs > LOW_TO_MEDIUM_THRESHOLD) {
            // Promote to medium queue
            await this.redis.lrem('job:queue:low', 1, jobId);
            await this.redis.lpush('job:queue:medium', jobId);

            // Update priority in database
            await this.pool.query(
              'UPDATE jobs SET priority = 2, updated_at = NOW() WHERE job_id = $1',
              [jobId]
            );
          }
        }
      }

      // Promote medium priority jobs that have been waiting > 2 minutes
      const mediumJobIds = await this.redis.lrange('job:queue:medium', 0, -1);
      for (const jobId of mediumJobIds) {
        const result = await this.pool.query(
          `SELECT ROUND(EXTRACT(EPOCH FROM created_at) * 1000) AS created_at_ms, priority
           FROM jobs WHERE job_id = $1 AND status = 'PENDING'`,
          [jobId]
        );

        if (result.rows.length > 0) {
          const createdAtMs = result.rows[0].created_at_ms;
          const waitTimeMs = now - createdAtMs;

          if (waitTimeMs > MEDIUM_TO_HIGH_THRESHOLD) {
            // Promote to high queue
            await this.redis.lrem('job:queue:medium', 1, jobId);
            await this.redis.lpush('job:queue:high', jobId);

            // Update priority in database
            await this.pool.query(
              'UPDATE jobs SET priority = 4, updated_at = NOW() WHERE job_id = $1',
              [jobId]
            );
          }
        }
      }
    } catch (error) {
      console.error('Error promoting stalled jobs:', error);
      // Don't throw - this is a best-effort fairness mechanism
    }
  }

  /**
   * Get priority queue key for Redis
   */
  private getQueueKey(priority: number): string {
    if (priority >= 4) return 'job:queue:high';
    if (priority >= 2) return 'job:queue:medium';
    return 'job:queue:low';
  }
}
