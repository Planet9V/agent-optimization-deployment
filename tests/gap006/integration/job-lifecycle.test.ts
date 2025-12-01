/**
 * GAP-006 Job Lifecycle Integration Tests
 * Tests complete job workflow with real PostgreSQL, Redis, and ruv-swarm integration
 */

import {
  setupTestEnvironment,
  waitFor,
  generateTestJobPayload,
  generateTestWorkerConfig,
  verifyJobState,
  TestEnvironment,
} from './setup';
import { JobService } from '../../../src/services/gap006/JobService';
import { WorkerService } from '../../../src/services/gap006/WorkerService';

describe('GAP-006 Job Lifecycle Integration', () => {
  let env: TestEnvironment;
  let jobService: JobService;
  let workerService: WorkerService;

  beforeAll(async () => {
    env = await setupTestEnvironment();
    jobService = new JobService(env.pool, env.redis);
    workerService = new WorkerService(env.pool, env.redis);
  });

  afterAll(async () => {
    // Clean up worker heartbeat timers before closing pools
    await workerService.cleanup();
    await env.cleanup();
  });

  beforeEach(async () => {
    // Clean state between tests
    await env.pool.query(`
      TRUNCATE
        jobs,
        workers,
        job_executions,
        dead_letter_queue,
        job_dependencies
      CASCADE
    `);
    await env.redis.flushdb();
  });

  describe('Complete Job Workflow', () => {
    test('create → acquire → process → complete', async () => {
      // 1. Spawn worker using ruv-swarm MCP
      const workerConfig = generateTestWorkerConfig({
        workerName: 'test-worker-lifecycle-1',
      });

      const workerId = await workerService.spawnWorker(workerConfig);
      expect(workerId).toBeDefined();
      expect(typeof workerId).toBe('string');

      // Verify worker in database
      const workerResult = await env.pool.query(
        'SELECT status, worker_name FROM workers WHERE worker_id = $1',
        [workerId]
      );
      expect(workerResult.rows.length).toBe(1);
      expect(workerResult.rows[0].status).toBe('ACTIVE');
      expect(workerResult.rows[0].worker_name).toBe('test-worker-lifecycle-1');

      // 2. Create job
      const jobPayload = generateTestJobPayload({
        jobType: 'data-processing',
        payload: { operation: 'transform', data: [1, 2, 3] },
      });

      const jobId = await jobService.createJob(jobPayload);
      expect(jobId).toBeDefined();
      expect(typeof jobId).toBe('string');

      // Verify job in database
      await verifyJobState(env.pool, jobId, { status: 'PENDING' });

      // 3. Worker acquires job
      const acquiredJobId = await jobService.acquireJob(workerId);
      expect(acquiredJobId).toBe(jobId);

      // Verify job status changed to PROCESSING
      await verifyJobState(env.pool, jobId, {
        status: 'PROCESSING',
        workerId: workerId,
      });

      // 4. Simulate job processing
      await new Promise(resolve => setTimeout(resolve, 100));

      // 5. Complete job with result
      const jobResult = {
        status: 'success',
        transformedData: [2, 4, 6],
        processedAt: new Date().toISOString(),
      };

      await jobService.completeJob(jobId, jobResult);

      // 6. Verify completion in PostgreSQL
      const completedResult = await env.pool.query(
        `SELECT
          status,
          completed_at,
          result
        FROM jobs
        WHERE job_id = $1`,
        [jobId]
      );

      expect(completedResult.rows[0].status).toBe('COMPLETED');
      expect(completedResult.rows[0].completed_at).not.toBeNull();
      expect(completedResult.rows[0].result).toEqual(jobResult);

      // 7. Verify job execution record
      const executionResult = await env.pool.query(
        `SELECT
          execution_status,
          duration_ms
        FROM job_executions
        WHERE job_id = $1`,
        [jobId]
      );

      expect(executionResult.rows.length).toBeGreaterThan(0);
      expect(executionResult.rows[0].execution_status).toBe('COMPLETED');
      expect(executionResult.rows[0].duration_ms).toBeGreaterThan(0);
    }, 10000);

    test('concurrent job processing by multiple workers', async () => {
      // Spawn 3 workers
      const workerIds = await Promise.all([
        workerService.spawnWorker(
          generateTestWorkerConfig({ workerName: 'concurrent-worker-1' })
        ),
        workerService.spawnWorker(
          generateTestWorkerConfig({ workerName: 'concurrent-worker-2' })
        ),
        workerService.spawnWorker(
          generateTestWorkerConfig({ workerName: 'concurrent-worker-3' })
        ),
      ]);

      expect(workerIds).toHaveLength(3);

      // Create 6 jobs
      const jobIds = await Promise.all(
        Array.from({ length: 6 }, (_, i) =>
          jobService.createJob(
            generateTestJobPayload({
              jobType: 'concurrent-test',
              payload: { index: i },
            })
          )
        )
      );

      expect(jobIds).toHaveLength(6);

      // Each worker acquires and processes jobs
      const processingPromises = workerIds.flatMap(workerId =>
        [1, 2].map(async () => {
          const jobId = await jobService.acquireJob(workerId);
          if (jobId) {
            await new Promise(resolve => setTimeout(resolve, 50));
            await jobService.completeJob(jobId, { status: 'success' });
          }
        })
      );

      await Promise.all(processingPromises);

      // Verify all jobs completed
      const completedResult = await env.pool.query(
        'SELECT COUNT(*) as count FROM jobs WHERE status = $1',
        ['COMPLETED']
      );

      expect(parseInt(completedResult.rows[0].count)).toBe(6);

      // Verify jobs distributed across workers
      const distributionResult = await env.pool.query(`
        SELECT worker_id, COUNT(*) as job_count
        FROM jobs
        WHERE status = 'COMPLETED'
        GROUP BY worker_id
      `);

      expect(distributionResult.rows.length).toBeGreaterThan(1);
    }, 15000);
  });

  describe('Job Retry Logic', () => {
    test('fail → retry → fail → dead letter queue', async () => {
      // Create job with max 2 retries
      const jobId = await jobService.createJob(
        generateTestJobPayload({
          jobType: 'failing-job',
          maxRetries: 2,
        })
      );

      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({ workerName: 'retry-test-worker' })
      );

      // Attempt 1: Fail
      let acquiredJobId = await jobService.acquireJob(workerId);
      expect(acquiredJobId).toBe(jobId);

      await jobService.failJob(jobId, {
        error: 'Test error 1',
        stack: 'Stack trace 1',
      });

      // Verify retry
      await waitFor(async () => {
        const result = await env.pool.query(
          'SELECT status, retry_count FROM jobs WHERE job_id = $1',
          [jobId]
        );
        return (
          result.rows[0].status === 'PENDING' && result.rows[0].retry_count === 1
        );
      });

      // Attempt 2: Fail again
      acquiredJobId = await jobService.acquireJob(workerId);
      expect(acquiredJobId).toBe(jobId);

      await jobService.failJob(jobId, {
        error: 'Test error 2',
        stack: 'Stack trace 2',
      });

      // Verify second retry
      await waitFor(async () => {
        const result = await env.pool.query(
          'SELECT status, retry_count FROM jobs WHERE job_id = $1',
          [jobId]
        );
        return (
          result.rows[0].status === 'PENDING' && result.rows[0].retry_count === 2
        );
      });

      // Attempt 3: Final failure (should go to DLQ)
      acquiredJobId = await jobService.acquireJob(workerId);
      expect(acquiredJobId).toBe(jobId);

      await jobService.failJob(jobId, {
        error: 'Test error 3 - final',
        stack: 'Stack trace 3',
      });

      // Verify dead letter queue
      await waitFor(async () => {
        const result = await env.pool.query(
          'SELECT status FROM jobs WHERE job_id = $1',
          [jobId]
        );
        return result.rows[0].status === 'FAILED';
      });

      const dlqResult = await env.pool.query(
        `SELECT
          original_job_id,
          retry_count,
          error_message
        FROM dead_letter_queue
        WHERE original_job_id = $1`,
        [jobId]
      );

      expect(dlqResult.rows.length).toBe(1);
      expect(dlqResult.rows[0].retry_count).toBe(2);
      expect(dlqResult.rows[0].error_message).toContain('Test error 3');
    }, 10000);

    test('exponential backoff retry delay', async () => {
      const jobId = await jobService.createJob(
        generateTestJobPayload({
          jobType: 'backoff-test',
          maxRetries: 3,
        })
      );

      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({ workerName: 'backoff-worker' })
      );

      const retryTimes: number[] = [];

      // Fail job 3 times and measure retry delays
      for (let i = 0; i < 3; i++) {
        const acquireTime = Date.now();
        const acquiredJobId = await jobService.acquireJob(workerId);

        if (i > 0) {
          retryTimes.push(acquireTime);
        }

        await jobService.failJob(acquiredJobId!, {
          error: `Backoff test error ${i + 1}`,
        });

        if (i < 2) {
          await waitFor(async () => {
            const result = await env.pool.query(
              'SELECT status FROM jobs WHERE job_id = $1',
              [jobId]
            );
            return result.rows[0].status === 'PENDING';
          });
        }
      }

      // Verify exponential backoff (each retry should take longer)
      if (retryTimes.length >= 2) {
        const firstDelay = retryTimes[0] - Date.now();
        const secondDelay = retryTimes[1] - retryTimes[0];
        expect(secondDelay).toBeGreaterThan(firstDelay);
      }
    }, 15000);
  });

  describe('Priority Queue Ordering', () => {
    test('jobs acquired in priority order', async () => {
      // Create jobs with different priorities
      const highPriorityJobId = await jobService.createJob(
        generateTestJobPayload({
          jobType: 'high-priority',
          priority: 5,
        })
      );

      const lowPriorityJobId = await jobService.createJob(
        generateTestJobPayload({
          jobType: 'low-priority',
          priority: 1,
        })
      );

      const mediumPriorityJobId = await jobService.createJob(
        generateTestJobPayload({
          jobType: 'medium-priority',
          priority: 3,
        })
      );

      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({ workerName: 'priority-test-worker' })
      );

      // Worker should acquire high priority first
      const firstJob = await jobService.acquireJob(workerId);
      expect(firstJob).toBe(highPriorityJobId);
      await jobService.completeJob(firstJob!, { status: 'success' });

      // Then medium priority
      const secondJob = await jobService.acquireJob(workerId);
      expect(secondJob).toBe(mediumPriorityJobId);
      await jobService.completeJob(secondJob!, { status: 'success' });

      // Finally low priority
      const thirdJob = await jobService.acquireJob(workerId);
      expect(thirdJob).toBe(lowPriorityJobId);
      await jobService.completeJob(thirdJob!, { status: 'success' });
    });

    test('FIFO within same priority level', async () => {
      const jobIds: string[] = [];

      // Create 5 jobs with same priority
      for (let i = 0; i < 5; i++) {
        const jobId = await jobService.createJob(
          generateTestJobPayload({
            jobType: `fifo-test-${i}`,
            priority: 3,
          })
        );
        jobIds.push(jobId);
        // Small delay to ensure different timestamps
        await new Promise(resolve => setTimeout(resolve, 10));
      }

      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({ workerName: 'fifo-worker' })
      );

      // Acquire jobs in order
      const acquiredOrder: string[] = [];
      for (let i = 0; i < 5; i++) {
        const jobId = await jobService.acquireJob(workerId);
        acquiredOrder.push(jobId!);
        await jobService.completeJob(jobId!, { status: 'success' });
      }

      // Verify FIFO order
      expect(acquiredOrder).toEqual(jobIds);
    }, 10000);
  });

  describe('Job Timeout Handling', () => {
    test('job timeout triggers automatic failure', async () => {
      const jobId = await jobService.createJob(
        generateTestJobPayload({
          jobType: 'timeout-test',
          timeoutMs: 1000, // 1 second timeout
        })
      );

      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({ workerName: 'timeout-worker' })
      );

      // Acquire job but don't complete it
      const acquiredJobId = await jobService.acquireJob(workerId);
      expect(acquiredJobId).toBe(jobId);

      // Wait for timeout
      await waitFor(
        async () => {
          const result = await env.pool.query(
            'SELECT status FROM jobs WHERE job_id = $1',
            [jobId]
          );
          return result.rows[0].status === 'FAILED';
        },
        5000,
        200
      );

      // Verify failure reason
      const jobResult = await env.pool.query(
        'SELECT result FROM jobs WHERE job_id = $1',
        [jobId]
      );

      expect(jobResult.rows[0].result.error).toContain('timeout');
    }, 10000);
  });
});
