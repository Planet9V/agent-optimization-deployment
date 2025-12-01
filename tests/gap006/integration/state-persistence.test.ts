/**
 * GAP-006 State Persistence Integration Tests
 * Tests Qdrant memory storage, state snapshots, and disaster recovery
 */

import {
  setupTestEnvironment,
  waitFor,
  generateTestJobPayload,
  generateTestWorkerConfig,
  TestEnvironment,
} from './setup';
import { JobService } from '../../../src/services/gap006/JobService';
import { WorkerService } from '../../../src/services/gap006/WorkerService';
import { StatePersistenceService } from '../../../src/services/gap006/StatePersistenceService';
import { QdrantClient } from '@qdrant/js-client-rest';

describe('GAP-006 State Persistence Integration', () => {
  let env: TestEnvironment;
  let jobService: JobService;
  let workerService: WorkerService;
  let stateService: StatePersistenceService;
  let qdrantClient: QdrantClient;

  beforeAll(async () => {
    env = await setupTestEnvironment();
    jobService = new JobService(env.pool, env.redis);
    workerService = new WorkerService(env.pool, env.redis);

    qdrantClient = new QdrantClient({
      url: process.env.QDRANT_URL || 'http://localhost:6333',
    });

    stateService = new StatePersistenceService(env.pool, env.redis, qdrantClient);
  });

  afterAll(async () => {
    // Clean up worker heartbeat timers and auto-snapshot timers before closing pools
    await workerService.cleanup();
    await stateService.cleanup();
    await env.cleanup();
  });

  beforeEach(async () => {
    await env.pool.query(`
      TRUNCATE
        jobs,
        workers,
        state_snapshots
      CASCADE
    `);
    await env.redis.flushdb();

    // Clear Qdrant collection
    try {
      await qdrantClient.deleteCollection('gap006_state');
    } catch (error) {
      // Collection might not exist
    }

    await qdrantClient.createCollection('gap006_state', {
      vectors: { size: 384, distance: 'Cosine' },
    });
  });

  describe('State Snapshot Creation', () => {
    test('create full system state snapshot', async () => {
      // Create some state
      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({ workerName: 'snapshot-worker-1' })
      );

      const jobIds = await Promise.all([
        jobService.createJob(generateTestJobPayload({ jobType: 'job-1' })),
        jobService.createJob(generateTestJobPayload({ jobType: 'job-2' })),
        jobService.createJob(generateTestJobPayload({ jobType: 'job-3' })),
      ]);

      // Acquire one job
      await jobService.acquireJob(workerId);

      // Create snapshot
      const snapshotId = await stateService.createSnapshot({
        snapshotType: 'FULL',
        description: 'Test full system snapshot',
      });

      expect(snapshotId).toBeDefined();

      // Verify snapshot in database
      const snapshotResult = await env.pool.query(
        `SELECT
          snapshot_type,
          state_data,
          metadata
        FROM state_snapshots
        WHERE snapshot_id = $1`,
        [snapshotId]
      );

      expect(snapshotResult.rows.length).toBe(1);
      expect(snapshotResult.rows[0].snapshot_type).toBe('FULL');

      const stateData = snapshotResult.rows[0].state_data;
      expect(stateData.workers).toHaveLength(1);
      expect(stateData.jobs).toHaveLength(3);
      expect(stateData.jobs.filter((j: any) => j.status === 'PROCESSING')).toHaveLength(1);

      // Verify snapshot in Qdrant
      const qdrantResult = await qdrantClient.retrieve('gap006_state', {
        ids: [snapshotId],
      });

      expect(qdrantResult.length).toBe(1);
      expect(qdrantResult[0].payload?.snapshotType).toBe('FULL');
    }, 10000);

    test('create incremental state snapshot', async () => {
      // Create initial snapshot
      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({ workerName: 'incremental-worker' })
      );

      const baseSnapshotId = await stateService.createSnapshot({
        snapshotType: 'FULL',
      });

      // Make some changes
      const jobId = await jobService.createJob(
        generateTestJobPayload({ jobType: 'incremental-job' })
      );

      await jobService.acquireJob(workerId);
      await jobService.completeJob(jobId, { status: 'success' });

      // Create incremental snapshot
      const incrementalSnapshotId = await stateService.createSnapshot({
        snapshotType: 'INCREMENTAL',
        baseSnapshotId: baseSnapshotId,
      });

      // Verify incremental snapshot only contains changes
      const incrementalResult = await env.pool.query(
        'SELECT state_data FROM state_snapshots WHERE snapshot_id = $1',
        [incrementalSnapshotId]
      );

      const incrementalData = incrementalResult.rows[0].state_data;
      expect(incrementalData.changes).toBeDefined();
      expect(incrementalData.changes.completedJobs).toContain(jobId);
      expect(incrementalData.baseSnapshotId).toBe(baseSnapshotId);
    }, 10000);
  });

  describe('State Restoration', () => {
    test('restore full system state from snapshot', async () => {
      // Create original state
      const originalWorkerId = await workerService.spawnWorker(
        generateTestWorkerConfig({ workerName: 'restore-worker' })
      );

      const originalJobIds = await Promise.all([
        jobService.createJob(generateTestJobPayload({ jobType: 'restore-job-1', priority: 5 })),
        jobService.createJob(generateTestJobPayload({ jobType: 'restore-job-2', priority: 3 })),
      ]);

      await jobService.acquireJob(originalWorkerId);

      // Create snapshot
      const snapshotId = await stateService.createSnapshot({
        snapshotType: 'FULL',
      });

      // Simulate system crash - clear all state
      await env.pool.query('TRUNCATE workers, jobs CASCADE');
      await env.redis.flushdb();

      // Restore from snapshot
      await stateService.restoreFromSnapshot(snapshotId);

      // Verify workers restored
      const workerResult = await env.pool.query(
        'SELECT worker_id, worker_name FROM workers'
      );
      expect(workerResult.rows.length).toBe(1);
      expect(workerResult.rows[0].worker_name).toBe('restore-worker');

      // Verify jobs restored
      const jobResult = await env.pool.query(
        'SELECT job_id, job_type, status, priority FROM jobs ORDER BY priority DESC'
      );
      expect(jobResult.rows.length).toBe(2);
      expect(jobResult.rows[0].job_type).toBe('restore-job-1');
      expect(jobResult.rows[0].priority).toBe(5);

      // Verify job processing state restored
      const processingJobs = jobResult.rows.filter((j: any) => j.status === 'PROCESSING');
      expect(processingJobs.length).toBe(1);
    }, 15000);

    test('restore with conflict resolution', async () => {
      // Create snapshot
      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({ workerName: 'conflict-worker' })
      );

      const snapshotId = await stateService.createSnapshot({
        snapshotType: 'FULL',
      });

      // Make conflicting changes
      await env.pool.query(
        'UPDATE workers SET status = $1 WHERE worker_id = $2',
        ['FAILED', workerId]
      );

      const newJobId = await jobService.createJob(
        generateTestJobPayload({ jobType: 'new-job' })
      );

      // Restore with conflict resolution strategy
      const conflicts = await stateService.restoreFromSnapshot(snapshotId, {
        conflictResolution: 'MERGE',
        preserveNewData: true,
      });

      // Verify conflict resolution
      expect(conflicts.length).toBeGreaterThan(0);
      expect(conflicts[0].type).toBe('WORKER_STATUS_CONFLICT');
      expect(conflicts[0].resolution).toBe('PRESERVED_CURRENT');

      // Verify new job preserved
      const jobResult = await env.pool.query(
        'SELECT COUNT(*) as count FROM jobs WHERE job_type = $1',
        ['new-job']
      );
      expect(parseInt(jobResult.rows[0].count)).toBe(1);
    }, 10000);
  });

  describe('Qdrant Memory Storage', () => {
    test('store and retrieve job execution context', async () => {
      const jobId = await jobService.createJob(
        generateTestJobPayload({
          jobType: 'context-test',
          payload: { operation: 'analyze', data: [1, 2, 3, 4, 5] },
        })
      );

      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({ workerName: 'context-worker' })
      );

      await jobService.acquireJob(workerId);

      // Store execution context in Qdrant
      const context = {
        jobId,
        workerId,
        executionSteps: [
          { step: 'validate', status: 'completed', duration: 50 },
          { step: 'transform', status: 'in_progress', duration: null },
        ],
        intermediateResults: { validated: true, transformCount: 3 },
      };

      await stateService.storeExecutionContext(jobId, context);

      // Retrieve context
      const retrievedContext = await stateService.retrieveExecutionContext(jobId);

      expect(retrievedContext).toBeDefined();
      expect(retrievedContext.jobId).toBe(jobId);
      expect(retrievedContext.executionSteps).toHaveLength(2);
      expect(retrievedContext.intermediateResults.validated).toBe(true);
    }, 5000);

    test('semantic search for similar job executions', async () => {
      // Store multiple job contexts
      const contexts = [
        {
          jobType: 'data-analysis',
          payload: { analysis: 'statistical', dataset: 'sales' },
          result: { mean: 100, median: 95 },
        },
        {
          jobType: 'data-analysis',
          payload: { analysis: 'statistical', dataset: 'inventory' },
          result: { mean: 200, median: 190 },
        },
        {
          jobType: 'data-transform',
          payload: { transform: 'normalize', dataset: 'customer' },
          result: { recordsProcessed: 1000 },
        },
      ];

      for (const ctx of contexts) {
        const jobId = await jobService.createJob(
          generateTestJobPayload(ctx)
        );
        await stateService.storeExecutionContext(jobId, ctx);
      }

      // Search for similar statistical analysis jobs
      const similar = await stateService.searchSimilarExecutions({
        queryText: 'statistical analysis on sales data',
        limit: 5,
      });

      expect(similar.length).toBeGreaterThan(0);
      expect(similar[0].payload?.jobType).toBe('data-analysis');
      expect(similar[0].score).toBeGreaterThan(0.7); // High similarity
    }, 10000);

    test('vector similarity for execution pattern matching', async () => {
      // Create execution patterns
      const pattern1 = {
        jobType: 'ml-training',
        steps: ['load_data', 'preprocess', 'train', 'validate'],
        duration: 3600000,
      };

      const pattern2 = {
        jobType: 'ml-training',
        steps: ['load_data', 'preprocess', 'train', 'test', 'deploy'],
        duration: 5400000,
      };

      const jobId1 = await jobService.createJob(
        generateTestJobPayload(pattern1)
      );
      const jobId2 = await jobService.createJob(
        generateTestJobPayload(pattern2)
      );

      await stateService.storeExecutionContext(jobId1, pattern1);
      await stateService.storeExecutionContext(jobId2, pattern2);

      // Find similar patterns
      const matches = await stateService.findSimilarPatterns(jobId1, {
        minSimilarity: 0.5,
      });

      expect(matches.length).toBeGreaterThan(0);
      expect(matches[0].jobId).toBe(jobId2);
      expect(matches[0].similarity).toBeGreaterThan(0.5);
    }, 5000);
  });

  describe('Disaster Recovery', () => {
    test('automatic snapshot scheduling', async () => {
      // Enable auto-snapshot
      await stateService.enableAutoSnapshot({
        intervalMinutes: 1,
        retentionDays: 7,
      });

      // Create some state
      await workerService.spawnWorker(
        generateTestWorkerConfig({ workerName: 'auto-snapshot-worker' })
      );

      // Wait for auto-snapshot
      await waitFor(
        async () => {
          const result = await env.pool.query(
            `SELECT COUNT(*) as count
            FROM state_snapshots
            WHERE snapshot_type = 'AUTO'`
          );
          return parseInt(result.rows[0].count) > 0;
        },
        90000, // 90 seconds
        5000
      );

      const snapshotResult = await env.pool.query(
        `SELECT snapshot_id, created_at
        FROM state_snapshots
        WHERE snapshot_type = 'AUTO'
        ORDER BY created_at DESC
        LIMIT 1`
      );

      expect(snapshotResult.rows.length).toBe(1);
    }, 120000);

    test('point-in-time recovery', async () => {
      const timestamps: Date[] = [];

      // Create state at T0
      const workerId1 = await workerService.spawnWorker(
        generateTestWorkerConfig({ workerName: 'pitr-worker-1' })
      );
      timestamps.push(new Date());
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Create state at T1
      const jobId1 = await jobService.createJob(
        generateTestJobPayload({ jobType: 'pitr-job-1' })
      );
      timestamps.push(new Date());
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Create state at T2
      const workerId2 = await workerService.spawnWorker(
        generateTestWorkerConfig({ workerName: 'pitr-worker-2' })
      );
      timestamps.push(new Date());

      // Recover to T1
      await stateService.pointInTimeRecovery(timestamps[1]);

      // Verify state at T1
      const workerCount = await env.pool.query(
        'SELECT COUNT(*) as count FROM workers'
      );
      expect(parseInt(workerCount.rows[0].count)).toBe(1);

      const jobCount = await env.pool.query(
        'SELECT COUNT(*) as count FROM jobs'
      );
      expect(parseInt(jobCount.rows[0].count)).toBe(1);
    }, 15000);
  });
});
