/**
 * File: performance-baseline.test.ts
 * Created: 2025-11-15
 * Purpose: Phase 3 performance baseline testing for GAP-006
 * Targets: 200-500 jobs/second throughput, dependency chain timing, fair scheduling overhead
 */

import { Pool } from 'pg';
import Redis from 'ioredis';
import { v4 as uuidv4 } from 'uuid';
import { JobService } from '../../../src/services/gap006/JobService';
import { WorkerService } from '../../../src/services/gap006/WorkerService';
import { setupTestEnvironment, TestEnvironment } from '../integration/setup';

interface PerformanceMetrics {
  operationName: string;
  totalOperations: number;
  totalTimeMs: number;
  avgTimeMs: number;
  minTimeMs: number;
  maxTimeMs: number;
  throughputPerSecond: number;
  p50Ms?: number;
  p95Ms?: number;
  p99Ms?: number;
}

describe('GAP-006 Phase 3 - Performance Baseline Testing', () => {
  let env: TestEnvironment;
  let jobService: JobService;
  let workerService: WorkerService;

  // Helper function to register a test worker (Phase 4: explicit transaction for atomicity)
  async function registerTestWorker(workerId: string): Promise<void> {
    const client = await env.pool.connect();
    try {
      await client.query('BEGIN');
      await client.query(
        `INSERT INTO workers (
          worker_id, worker_name, worker_type, status, capacity,
          current_load, last_heartbeat, health_score, metadata,
          created_at, updated_at
        ) VALUES ($1, $2, $3, $4, $5, $6, NOW(), $7, $8, NOW(), NOW())
        ON CONFLICT (worker_id) DO NOTHING`,
        [
          workerId,
          `perf-worker-${workerId.substring(0, 8)}`,
          'performance',
          'ACTIVE',
          100,
          0,
          1.0,
          JSON.stringify({ environment: 'performance-test' })
        ]
      );
      await client.query('COMMIT');

      // Phase 4: Add small delay to ensure transaction is fully committed
      await new Promise(resolve => setTimeout(resolve, 10));
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  // Calculate percentiles from sorted array
  function calculatePercentiles(sortedValues: number[]): { p50: number; p95: number; p99: number } {
    const p50Index = Math.floor(sortedValues.length * 0.5);
    const p95Index = Math.floor(sortedValues.length * 0.95);
    const p99Index = Math.floor(sortedValues.length * 0.99);

    return {
      p50: sortedValues[p50Index],
      p95: sortedValues[p95Index],
      p99: sortedValues[p99Index]
    };
  }

  // Calculate performance metrics from timing array
  function calculateMetrics(
    operationName: string,
    timingsMs: number[]
  ): PerformanceMetrics {
    const totalOperations = timingsMs.length;
    const totalTimeMs = timingsMs.reduce((sum, t) => sum + t, 0);
    const avgTimeMs = totalTimeMs / totalOperations;
    const minTimeMs = Math.min(...timingsMs);
    const maxTimeMs = Math.max(...timingsMs);
    const throughputPerSecond = (totalOperations / totalTimeMs) * 1000;

    const sortedTimings = [...timingsMs].sort((a, b) => a - b);
    const percentiles = calculatePercentiles(sortedTimings);

    return {
      operationName,
      totalOperations,
      totalTimeMs,
      avgTimeMs,
      minTimeMs,
      maxTimeMs,
      throughputPerSecond,
      p50Ms: percentiles.p50,
      p95Ms: percentiles.p95,
      p99Ms: percentiles.p99
    };
  }

  // Pretty print performance metrics
  function printMetrics(metrics: PerformanceMetrics): void {
    console.log(`\n📊 ${metrics.operationName} Performance Metrics:`);
    console.log(`   Total Operations: ${metrics.totalOperations}`);
    console.log(`   Total Time: ${metrics.totalTimeMs.toFixed(2)}ms`);
    console.log(`   Avg Time: ${metrics.avgTimeMs.toFixed(2)}ms`);
    console.log(`   Min Time: ${metrics.minTimeMs.toFixed(2)}ms`);
    console.log(`   Max Time: ${metrics.maxTimeMs.toFixed(2)}ms`);
    console.log(`   Throughput: ${metrics.throughputPerSecond.toFixed(2)} ops/sec`);
    if (metrics.p50Ms !== undefined) {
      console.log(`   P50: ${metrics.p50Ms.toFixed(2)}ms`);
      console.log(`   P95: ${metrics.p95Ms.toFixed(2)}ms`);
      console.log(`   P99: ${metrics.p99Ms.toFixed(2)}ms`);
    }
  }

  beforeAll(async () => {
    env = await setupTestEnvironment();
    jobService = new JobService(env.pool, env.redis);
    workerService = new WorkerService(env.pool, env.redis);
  }, 30000);

  afterAll(async () => {
    if (env && env.cleanup) {
      await env.cleanup();
    }
  });

  beforeEach(async () => {
    await env.pool.query('DELETE FROM job_dependencies');
    await env.pool.query('DELETE FROM job_executions');
    await env.pool.query('DELETE FROM jobs');
    await env.pool.query('DELETE FROM workers WHERE worker_type = \'performance\'');
    await env.redis.del('job:queue:high', 'job:queue:medium', 'job:queue:low');
  });

  describe('Baseline Job Creation Performance', () => {
    test('measure job creation throughput (target: 200+ jobs/sec)', async () => {
      const jobCount = 1000;
      const timings: number[] = [];

      console.log(`\n🚀 Creating ${jobCount} jobs...`);
      const startTime = Date.now();

      for (let i = 0; i < jobCount; i++) {
        const jobStart = Date.now();
        await jobService.createJob({
          jobType: `performance-test-${i}`,
          payload: { testData: `job-${i}`, timestamp: Date.now() },
          priority: (i % 5) + 1 // Distribute across priorities 1-5
        });
        timings.push(Date.now() - jobStart);
      }

      const metrics = calculateMetrics('Job Creation', timings);
      printMetrics(metrics);

      // Assertions
      expect(metrics.totalOperations).toBe(jobCount);
      expect(metrics.throughputPerSecond).toBeGreaterThan(200); // Target threshold
      expect(metrics.avgTimeMs).toBeLessThan(10); // Average under 10ms

      console.log(`   ✅ Created ${jobCount} jobs in ${(Date.now() - startTime).toFixed(2)}ms`);
    }, 30000);

    test('measure job creation with dependencies (target: 150+ jobs/sec)', async () => {
      const jobCount = 500;
      const timings: number[] = [];
      const jobIds: string[] = [];

      console.log(`\n🚀 Creating ${jobCount} jobs with dependencies...`);

      // Create first job without dependencies
      const rootJobId = await jobService.createJob({
        jobType: 'root-job',
        payload: { root: true },
        priority: 5
      });
      jobIds.push(rootJobId);

      // Create dependent jobs
      for (let i = 0; i < jobCount - 1; i++) {
        const jobStart = Date.now();
        const dependsOn = i > 0 ? [jobIds[Math.floor(Math.random() * jobIds.length)]] : [rootJobId];
        const jobId = await jobService.createJob({
          jobType: `dependent-job-${i}`,
          payload: { index: i },
          priority: 3,
          dependsOn
        });
        timings.push(Date.now() - jobStart);
        jobIds.push(jobId);
      }

      const metrics = calculateMetrics('Job Creation with Dependencies', timings);
      printMetrics(metrics);

      expect(metrics.totalOperations).toBe(jobCount - 1);
      expect(metrics.throughputPerSecond).toBeGreaterThan(150);
      expect(metrics.avgTimeMs).toBeLessThan(15);
    }, 30000);
  });

  describe('Job Acquisition and Processing Performance', () => {
    test('measure job acquisition throughput (target: 300+ acquisitions/sec)', async () => {
      const jobCount = 500;
      const workerCount = 5;
      const timings: number[] = [];

      // Create jobs first
      console.log(`\n🚀 Creating ${jobCount} jobs for acquisition test...`);
      for (let i = 0; i < jobCount; i++) {
        await jobService.createJob({
          jobType: 'acquisition-test',
          payload: { index: i },
          priority: 3
        });
      }

      // Register workers
      const workerIds: string[] = [];
      for (let i = 0; i < workerCount; i++) {
        const workerId = uuidv4();
        await registerTestWorker(workerId);
        workerIds.push(workerId);
      }

      // Acquire jobs
      console.log(`\n🚀 Acquiring ${jobCount} jobs with ${workerCount} workers...`);
      let acquiredCount = 0;
      let currentWorkerIndex = 0;

      while (acquiredCount < jobCount) {
        const workerId = workerIds[currentWorkerIndex];
        const acquireStart = Date.now();
        const jobId = await jobService.acquireJob(workerId);
        if (jobId) {
          timings.push(Date.now() - acquireStart);
          acquiredCount++;
        } else {
          break; // No more jobs to acquire
        }
        currentWorkerIndex = (currentWorkerIndex + 1) % workerCount;
      }

      const metrics = calculateMetrics('Job Acquisition', timings);
      printMetrics(metrics);

      expect(metrics.totalOperations).toBe(jobCount);
      expect(metrics.throughputPerSecond).toBeGreaterThan(300);
      expect(metrics.avgTimeMs).toBeLessThan(5);

      console.log(`   ✅ Acquired ${acquiredCount} jobs`);
    }, 60000);

    test('measure complete job lifecycle (create → acquire → complete)', async () => {
      const jobCount = 200;
      const createTimings: number[] = [];
      const acquireTimings: number[] = [];
      const completeTimings: number[] = [];

      const workerId = uuidv4();
      await registerTestWorker(workerId);

      console.log(`\n🚀 Running complete lifecycle for ${jobCount} jobs...`);

      for (let i = 0; i < jobCount; i++) {
        // Create
        const createStart = Date.now();
        const jobId = await jobService.createJob({
          jobType: 'lifecycle-test',
          payload: { index: i },
          priority: 3
        });
        createTimings.push(Date.now() - createStart);

        // Acquire
        const acquireStart = Date.now();
        const acquiredJobId = await jobService.acquireJob(workerId);
        acquireTimings.push(Date.now() - acquireStart);
        expect(acquiredJobId).toBe(jobId);

        // Complete
        const completeStart = Date.now();
        await jobService.completeJob(jobId, { result: `completed-${i}` });
        completeTimings.push(Date.now() - completeStart);
      }

      const createMetrics = calculateMetrics('Lifecycle - Create', createTimings);
      const acquireMetrics = calculateMetrics('Lifecycle - Acquire', acquireTimings);
      const completeMetrics = calculateMetrics('Lifecycle - Complete', completeTimings);

      printMetrics(createMetrics);
      printMetrics(acquireMetrics);
      printMetrics(completeMetrics);

      const totalAvgMs = createMetrics.avgTimeMs + acquireMetrics.avgTimeMs + completeMetrics.avgTimeMs;
      console.log(`\n   📊 Total Average Lifecycle Time: ${totalAvgMs.toFixed(2)}ms`);
      console.log(`   📊 Lifecycle Throughput: ${((1000 / totalAvgMs)).toFixed(2)} jobs/sec`);

      expect(totalAvgMs).toBeLessThan(50); // Complete lifecycle under 50ms
    }, 60000);
  });

  describe('Dependency Chain Execution Performance', () => {
    test('measure cascading execution timing (chain depth: 10)', async () => {
      const chainDepth = 10;
      const cascadeTimings: number[] = [];
      const workerId = uuidv4();
      await registerTestWorker(workerId);

      console.log(`\n🚀 Creating dependency chain of depth ${chainDepth}...`);

      // Create chain
      const jobIds: string[] = [];
      for (let i = 0; i < chainDepth; i++) {
        const dependsOn = i > 0 ? [jobIds[i - 1]] : undefined;
        const jobId = await jobService.createJob({
          jobType: `chain-job-${i}`,
          payload: { depth: i },
          priority: 3,
          dependsOn
        });
        jobIds.push(jobId);
      }

      // Execute chain
      console.log(`\n🚀 Executing dependency chain...`);
      for (let i = 0; i < chainDepth; i++) {
        const acquiredJobId = await jobService.acquireJob(workerId);
        expect(acquiredJobId).toBe(jobIds[i]);

        const cascadeStart = Date.now();
        await jobService.completeJob(jobIds[i], { result: `chain-${i}-complete` });
        cascadeTimings.push(Date.now() - cascadeStart);

        // Verify next job was queued (except for last job)
        if (i < chainDepth - 1) {
          const nextJobQueued = await env.redis.lrange('job:queue:medium', 0, -1);
          expect(nextJobQueued).toContain(jobIds[i + 1]);
        }
      }

      const metrics = calculateMetrics('Cascading Execution', cascadeTimings);
      printMetrics(metrics);

      expect(metrics.avgTimeMs).toBeLessThan(50); // Cascading under 50ms average
      console.log(`   ✅ Chain of ${chainDepth} jobs executed successfully`);
    }, 60000);

    test('measure parallel dependency resolution (fan-out: 50)', async () => {
      const fanOutSize = 50;
      const workerId = uuidv4();
      await registerTestWorker(workerId);

      console.log(`\n🚀 Creating parent job with ${fanOutSize} dependent children...`);

      // Create parent
      const parentJobId = await jobService.createJob({
        jobType: 'parent',
        payload: { type: 'parent' },
        priority: 5
      });

      // Create children depending on parent
      const childIds: string[] = [];
      const createStart = Date.now();
      for (let i = 0; i < fanOutSize; i++) {
        const childId = await jobService.createJob({
          jobType: `child-${i}`,
          payload: { childIndex: i },
          priority: 3,
          dependsOn: [parentJobId],
          inheritPriority: false  // Phase 4 Fix #2: Disable priority inheritance to test actual cascading
        });
        childIds.push(childId);
      }
      const createTimeMs = Date.now() - createStart;

      console.log(`   📊 Created ${fanOutSize} dependent children in ${createTimeMs.toFixed(2)}ms`);

      // Complete parent and measure cascade time
      await jobService.acquireJob(workerId);
      const cascadeStart = Date.now();
      await jobService.completeJob(parentJobId, { result: 'parent-complete' });
      const cascadeTimeMs = Date.now() - cascadeStart;

      console.log(`   📊 Cascaded to ${fanOutSize} children in ${cascadeTimeMs.toFixed(2)}ms`);

      // Verify all children are now queued
      const queuedJobs = await env.redis.lrange('job:queue:medium', 0, -1);
      expect(queuedJobs.length).toBe(fanOutSize);

      expect(cascadeTimeMs).toBeLessThan(1000); // Cascade 50 jobs under 1 second
    }, 60000);
  });

  describe('Fair Scheduling Overhead', () => {
    test('measure promotion overhead at various queue depths', async () => {
      const queueDepths = [10, 50, 100, 500];
      const workerId = uuidv4();
      await registerTestWorker(workerId);

      for (const depth of queueDepths) {
        // Clear queues
        await env.pool.query('DELETE FROM jobs');
        await env.redis.del('job:queue:low', 'job:queue:medium', 'job:queue:high');

        // Create jobs with old timestamps to trigger promotion
        console.log(`\n🚀 Testing promotion with queue depth ${depth}...`);
        for (let i = 0; i < depth; i++) {
          await jobService.createJob({
            jobType: `low-priority-${i}`,
            payload: { index: i },
            priority: 1 // Low priority
          });
        }

        // Update job timestamps to be old (trigger promotion)
        await env.pool.query(
          `UPDATE jobs SET created_at = NOW() - INTERVAL '2 minutes' WHERE job_type LIKE 'low-priority%'`
        );

        // Measure acquireJob time (includes promotion check)
        const acquireStart = Date.now();
        await jobService.acquireJob(workerId);
        const acquireTimeMs = Date.now() - acquireStart;

        console.log(`   📊 Queue Depth ${depth}: Acquire time with promotion = ${acquireTimeMs.toFixed(2)}ms`);

        // Verify some jobs were promoted
        const mediumQueue = await env.redis.lrange('job:queue:medium', 0, -1);
        console.log(`   📊 Jobs promoted to medium queue: ${mediumQueue.length}`);

        expect(acquireTimeMs).toBeLessThan(200); // Acquisition with promotion under 200ms
      }
    }, 120000);
  });

  describe('Priority Inheritance Performance', () => {
    test('measure priority inheritance overhead', async () => {
      const jobCount = 200;
      const timingsWithInheritance: number[] = [];
      const timingsWithoutInheritance: number[] = [];

      console.log(`\n🚀 Testing priority inheritance overhead...`);

      // Create parent job
      const parentJobId = await jobService.createJob({
        jobType: 'high-priority-parent',
        payload: { priority: 'high' },
        priority: 5
      });

      // Test WITH priority inheritance
      for (let i = 0; i < jobCount; i++) {
        const createStart = Date.now();
        await jobService.createJob({
          jobType: `child-with-inheritance-${i}`,
          payload: { index: i },
          priority: 1,
          dependsOn: [parentJobId],
          inheritPriority: true
        });
        timingsWithInheritance.push(Date.now() - createStart);
      }

      // Clean up
      await env.pool.query('DELETE FROM job_dependencies');
      await env.pool.query(`DELETE FROM jobs WHERE job_type LIKE 'child-with-inheritance%'`);

      // Test WITHOUT priority inheritance
      for (let i = 0; i < jobCount; i++) {
        const createStart = Date.now();
        await jobService.createJob({
          jobType: `child-without-inheritance-${i}`,
          payload: { index: i },
          priority: 1,
          dependsOn: [parentJobId],
          inheritPriority: false
        });
        timingsWithoutInheritance.push(Date.now() - createStart);
      }

      const metricsWithInheritance = calculateMetrics('Job Creation WITH Priority Inheritance', timingsWithInheritance);
      const metricsWithoutInheritance = calculateMetrics('Job Creation WITHOUT Priority Inheritance', timingsWithoutInheritance);

      printMetrics(metricsWithInheritance);
      printMetrics(metricsWithoutInheritance);

      const overheadMs = metricsWithInheritance.avgTimeMs - metricsWithoutInheritance.avgTimeMs;
      console.log(`\n   📊 Priority Inheritance Overhead: ${overheadMs.toFixed(2)}ms`);

      expect(overheadMs).toBeLessThan(5); // Overhead under 5ms
    }, 60000);
  });
});
