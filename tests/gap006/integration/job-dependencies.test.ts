/**
 * File: job-dependencies.test.ts
 * Created: 2025-11-15
 * Purpose: Integration tests for GAP-006 Phase 2 job dependency resolution
 * Tests: Dependency creation, priority inheritance, cascading execution, circular detection
 */

import { Pool } from 'pg';
import Redis from 'ioredis';
import { v4 as uuidv4 } from 'uuid';
import { JobService } from '../../../src/services/gap006/JobService';
import { setupTestEnvironment, TestEnvironment } from './setup';

describe('GAP-006 Job Dependencies Integration', () => {
  let env: TestEnvironment;
  let jobService: JobService;

  // Helper function to register a test worker
  async function registerTestWorker(workerId: string): Promise<void> {
    await env.pool.query(
      `INSERT INTO workers (
        worker_id,
        worker_name,
        worker_type,
        status,
        capacity,
        current_load,
        last_heartbeat,
        health_score,
        metadata,
        created_at,
        updated_at
      ) VALUES ($1, $2, $3, $4, $5, $6, NOW(), $7, $8, NOW(), NOW())
      ON CONFLICT (worker_id) DO NOTHING`,
      [
        workerId,
        `test-worker-${workerId.substring(0, 8)}`,
        'test',
        'ACTIVE',
        10,
        0,
        1.0,
        JSON.stringify({ environment: 'test' })
      ]
    );
  }

  beforeAll(async () => {
    env = await setupTestEnvironment();
    jobService = new JobService(env.pool, env.redis);
  }, 30000);

  afterAll(async () => {
    if (env && env.cleanup) {
      await env.cleanup();
    }
  });

  beforeEach(async () => {
    // Clean up jobs and dependencies before each test
    await env.pool.query('DELETE FROM job_dependencies');
    await env.pool.query('DELETE FROM jobs');
    await env.pool.query('DELETE FROM workers WHERE worker_type = \'test\'');
    await env.redis.del('job:queue:high', 'job:queue:medium', 'job:queue:low');
  });

  describe('Basic Dependency Creation', () => {
    test('create job with single dependency', async () => {
      // Create parent job
      const parentJobId = await jobService.createJob({
        jobType: 'parent-task',
        payload: { data: 'parent' },
        priority: 3
      });

      // Create child job that depends on parent
      const childJobId = await jobService.createJob({
        jobType: 'child-task',
        payload: { data: 'child' },
        priority: 2,
        dependsOn: [parentJobId]
      });

      // Verify dependency relationship exists
      const depResult = await env.pool.query(
        'SELECT * FROM job_dependencies WHERE job_id = $1 AND depends_on_job_id = $2',
        [childJobId, parentJobId]
      );
      expect(depResult.rows.length).toBe(1);

      // Verify child job is NOT queued (parent not complete)
      const queuedJobs = await env.redis.lrange('job:queue:medium', 0, -1);
      expect(queuedJobs).not.toContain(childJobId);
    }, 10000);

    test('create job with multiple dependencies', async () => {
      // Create 3 parent jobs
      const parent1 = await jobService.createJob({
        jobType: 'parent1',
        payload: { data: '1' }
      });

      const parent2 = await jobService.createJob({
        jobType: 'parent2',
        payload: { data: '2' }
      });

      const parent3 = await jobService.createJob({
        jobType: 'parent3',
        payload: { data: '3' }
      });

      // Create child that depends on all 3
      const childJobId = await jobService.createJob({
        jobType: 'child',
        payload: { data: 'child' },
        dependsOn: [parent1, parent2, parent3]
      });

      // Verify all 3 dependencies exist
      const depResult = await env.pool.query(
        'SELECT COUNT(*) as count FROM job_dependencies WHERE job_id = $1',
        [childJobId]
      );
      expect(parseInt(depResult.rows[0].count)).toBe(3);
    }, 10000);
  });

  describe('Priority Inheritance', () => {
    test('child job inherits higher priority from parent', async () => {
      // Create high priority parent
      const parentJobId = await jobService.createJob({
        jobType: 'high-priority-parent',
        payload: { data: 'parent' },
        priority: 5 // High priority
      });

      // Create low priority child that should inherit
      const childJobId = await jobService.createJob({
        jobType: 'child',
        payload: { data: 'child' },
        priority: 1, // Low priority
        dependsOn: [parentJobId]
        // inheritPriority defaults to true
      });

      // Verify child inherited high priority
      const jobResult = await env.pool.query(
        'SELECT priority FROM jobs WHERE job_id = $1',
        [childJobId]
      );
      expect(jobResult.rows[0].priority).toBe(5); // Inherited from parent
    }, 10000);

    test('child job keeps own priority if higher than parent', async () => {
      // Create low priority parent
      const parentJobId = await jobService.createJob({
        jobType: 'low-priority-parent',
        payload: { data: 'parent' },
        priority: 1 // Low priority
      });

      // Create high priority child
      const childJobId = await jobService.createJob({
        jobType: 'child',
        payload: { data: 'child' },
        priority: 5, // High priority
        dependsOn: [parentJobId]
      });

      // Verify child kept its own higher priority
      const jobResult = await env.pool.query(
        'SELECT priority FROM jobs WHERE job_id = $1',
        [childJobId]
      );
      expect(jobResult.rows[0].priority).toBe(5); // Kept own priority
    }, 10000);

    test('child job can disable priority inheritance', async () => {
      // Create high priority parent
      const parentJobId = await jobService.createJob({
        jobType: 'high-priority-parent',
        payload: { data: 'parent' },
        priority: 5
      });

      // Create child with inheritance disabled
      const childJobId = await jobService.createJob({
        jobType: 'child',
        payload: { data: 'child' },
        priority: 1,
        dependsOn: [parentJobId],
        inheritPriority: false // Explicitly disable
      });

      // Verify child kept low priority
      const jobResult = await env.pool.query(
        'SELECT priority FROM jobs WHERE job_id = $1',
        [childJobId]
      );
      expect(jobResult.rows[0].priority).toBe(1); // Kept own priority
    }, 10000);

    test('child inherits max priority from multiple parents', async () => {
      // Create parents with different priorities
      const parent1 = await jobService.createJob({
        jobType: 'parent1',
        payload: { data: '1' },
        priority: 2
      });

      const parent2 = await jobService.createJob({
        jobType: 'parent2',
        payload: { data: '2' },
        priority: 5 // Highest
      });

      const parent3 = await jobService.createJob({
        jobType: 'parent3',
        payload: { data: '3' },
        priority: 3
      });

      // Create child depending on all
      const childJobId = await jobService.createJob({
        jobType: 'child',
        payload: { data: 'child' },
        priority: 1,
        dependsOn: [parent1, parent2, parent3]
      });

      // Verify child inherited max priority (5)
      const jobResult = await env.pool.query(
        'SELECT priority FROM jobs WHERE job_id = $1',
        [childJobId]
      );
      expect(jobResult.rows[0].priority).toBe(5); // Max priority from parents
    }, 10000);
  });

  describe('Cascading Job Execution', () => {
    test('completing parent triggers dependent child job', async () => {
      // Create parent job
      const parentJobId = await jobService.createJob({
        jobType: 'parent',
        payload: { data: 'parent' },
        priority: 3
      });

      // Create child depending on parent
      const childJobId = await jobService.createJob({
        jobType: 'child',
        payload: { data: 'child' },
        priority: 3,
        dependsOn: [parentJobId]
      });

      // Verify child is NOT queued initially
      let mediumQueue = await env.redis.lrange('job:queue:medium', 0, -1);
      expect(mediumQueue).not.toContain(childJobId);

      // Register test worker and acquire parent job
      const workerId = uuidv4();
      await registerTestWorker(workerId);
      const acquiredJobId = await jobService.acquireJob(workerId);
      expect(acquiredJobId).toBe(parentJobId);

      await jobService.completeJob(parentJobId, { result: 'success' });

      // Verify child is NOW queued (triggered by parent completion)
      mediumQueue = await env.redis.lrange('job:queue:medium', 0, -1);
      expect(mediumQueue).toContain(childJobId);
    }, 10000);

    test('child waits for all dependencies to complete', async () => {
      // Create 2 parent jobs
      const parent1 = await jobService.createJob({
        jobType: 'parent1',
        payload: { data: '1' }
      });

      const parent2 = await jobService.createJob({
        jobType: 'parent2',
        payload: { data: '2' }
      });

      // Create child depending on both
      const childJobId = await jobService.createJob({
        jobType: 'child',
        payload: { data: 'child' },
        priority: 3,
        dependsOn: [parent1, parent2]
      });

      const workerId = uuidv4();
      await registerTestWorker(workerId);

      // Complete first parent
      await jobService.acquireJob(workerId);
      await jobService.completeJob(parent1, { result: 'success' });

      // Child should NOT be queued yet (parent2 still pending)
      let mediumQueue = await env.redis.lrange('job:queue:medium', 0, -1);
      expect(mediumQueue).not.toContain(childJobId);

      // Complete second parent
      await jobService.acquireJob(workerId);
      await jobService.completeJob(parent2, { result: 'success' });

      // Child should NOW be queued (all dependencies met)
      mediumQueue = await env.redis.lrange('job:queue:medium', 0, -1);
      expect(mediumQueue).toContain(childJobId);
    }, 10000);

    test('chain of dependencies executes in order', async () => {
      // Create chain: job1 -> job2 -> job3
      const job1 = await jobService.createJob({
        jobType: 'step1',
        payload: { step: 1 },
        priority: 3
      });

      const job2 = await jobService.createJob({
        jobType: 'step2',
        payload: { step: 2 },
        priority: 3,
        dependsOn: [job1]
      });

      const job3 = await jobService.createJob({
        jobType: 'step3',
        payload: { step: 3 },
        priority: 3,
        dependsOn: [job2]
      });

      const workerId = uuidv4();
      await registerTestWorker(workerId);

      // Only job1 should be queued initially
      let queue = await env.redis.lrange('job:queue:medium', 0, -1);
      expect(queue).toContain(job1);
      expect(queue).not.toContain(job2);
      expect(queue).not.toContain(job3);

      // Complete job1
      await jobService.acquireJob(workerId);
      await jobService.completeJob(job1, { result: 'step1-done' });

      // Now job2 should be queued
      queue = await env.redis.lrange('job:queue:medium', 0, -1);
      expect(queue).toContain(job2);
      expect(queue).not.toContain(job3);

      // Complete job2
      await jobService.acquireJob(workerId);
      await jobService.completeJob(job2, { result: 'step2-done' });

      // Now job3 should be queued
      queue = await env.redis.lrange('job:queue:medium', 0, -1);
      expect(queue).toContain(job3);
    }, 10000);
  });

  describe('Circular Dependency Prevention', () => {
    test('database trigger prevents circular dependency', async () => {
      // Create job1
      const job1 = await jobService.createJob({
        jobType: 'job1',
        payload: { data: '1' }
      });

      // Create job2 depending on job1
      const job2 = await jobService.createJob({
        jobType: 'job2',
        payload: { data: '2' },
        dependsOn: [job1]
      });

      // Try to make job1 depend on job2 (creates cycle)
      await expect(
        env.pool.query(
          'INSERT INTO job_dependencies (job_id, depends_on_job_id) VALUES ($1, $2)',
          [job1, job2]
        )
      ).rejects.toThrow(); // Trigger should reject circular dependency
    }, 10000);
  });

  describe('Edge Cases', () => {
    test('job with no dependencies is queued immediately', async () => {
      const jobId = await jobService.createJob({
        jobType: 'independent',
        payload: { data: 'test' },
        priority: 3
      });

      // Should be queued immediately
      const queue = await env.redis.lrange('job:queue:medium', 0, -1);
      expect(queue).toContain(jobId);
    }, 10000);

    test('failed parent does not trigger dependent child', async () => {
      // Create parent
      const parentJobId = await jobService.createJob({
        jobType: 'parent',
        payload: { data: 'parent' },
        priority: 3
      });

      // Create child
      const childJobId = await jobService.createJob({
        jobType: 'child',
        payload: { data: 'child' },
        priority: 3,
        dependsOn: [parentJobId]
      });

      const workerId = uuidv4();
      await registerTestWorker(workerId);

      // Acquire and FAIL parent
      await jobService.acquireJob(workerId);
      await jobService.failJob(parentJobId, { error: 'Parent failed' });

      // Child should NOT be queued (parent failed, not completed)
      const queue = await env.redis.lrange('job:queue:medium', 0, -1);
      expect(queue).not.toContain(childJobId);
    }, 10000);
  });
});
