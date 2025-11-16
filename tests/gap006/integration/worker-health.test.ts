/**
 * GAP-006 Worker Health and Failure Integration Tests
 * Tests worker heartbeat monitoring, failure detection, and predictive analytics
 */

import {
  setupTestEnvironment,
  waitFor,
  generateTestWorkerConfig,
  verifyWorkerState,
  TestEnvironment,
} from './setup';
import { WorkerService } from '../../../src/services/gap006/WorkerService';
import { HealthMonitorService } from '../../../src/services/gap006/HealthMonitorService';

describe('GAP-006 Worker Health Integration', () => {
  let env: TestEnvironment;
  let workerService: WorkerService;
  let healthMonitor: HealthMonitorService;

  beforeAll(async () => {
    env = await setupTestEnvironment();
    workerService = new WorkerService(env.pool, env.redis);
    healthMonitor = new HealthMonitorService(env.pool, env.redis);
  });

  afterAll(async () => {
    // Clean up worker heartbeat timers before closing pools
    await workerService.cleanup();
    await env.cleanup();
  });

  beforeEach(async () => {
    await env.pool.query('TRUNCATE workers, worker_health_logs CASCADE');
    await env.redis.flushdb();
  });

  describe('Worker Heartbeat Monitoring', () => {
    test('worker sends regular heartbeats', async () => {
      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({
          workerName: 'heartbeat-test-worker',
          heartbeatIntervalMs: 500,
        })
      );

      // Wait for multiple heartbeats
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Verify heartbeats recorded
      const heartbeatResult = await env.pool.query(
        `SELECT COUNT(*) as count
        FROM worker_health_logs
        WHERE worker_id = $1
        AND metric_type = 'heartbeat'`,
        [workerId]
      );

      const heartbeatCount = parseInt(heartbeatResult.rows[0].count);
      expect(heartbeatCount).toBeGreaterThanOrEqual(3);

      // Verify last heartbeat timestamp
      const workerResult = await env.pool.query(
        'SELECT last_heartbeat FROM workers WHERE worker_id = $1',
        [workerId]
      );

      const lastHeartbeat = new Date(workerResult.rows[0].last_heartbeat);
      const now = new Date();
      const timeDiff = now.getTime() - lastHeartbeat.getTime();

      expect(timeDiff).toBeLessThan(1000); // Within last second
    }, 5000);

    test('missed heartbeat triggers health alert', async () => {
      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({
          workerName: 'missed-heartbeat-worker',
          heartbeatIntervalMs: 500,
        })
      );

      // Simulate worker stopping heartbeats
      await workerService.pauseWorkerHeartbeat(workerId);

      // Wait for health monitor to detect issue
      await waitFor(
        async () => {
          const result = await env.pool.query(
            `SELECT health_score
            FROM workers
            WHERE worker_id = $1`,
            [workerId]
          );
          return result.rows[0].health_score < 0.7;
        },
        5000,
        200
      );

      // Verify health alert created
      const alertResult = await env.pool.query(
        `SELECT alert_type, severity
        FROM worker_health_logs
        WHERE worker_id = $1
        AND metric_type = 'alert'
        ORDER BY logged_at DESC
        LIMIT 1`,
        [workerId]
      );

      expect(alertResult.rows.length).toBeGreaterThan(0);
      expect(alertResult.rows[0].alert_type).toBe('MISSED_HEARTBEAT');
      expect(alertResult.rows[0].severity).toBeGreaterThanOrEqual(3);
    }, 10000);
  });

  describe('Worker Failure Detection', () => {
    test('worker crash detected and marked as failed', async () => {
      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({
          workerName: 'crash-test-worker',
        })
      );

      // Verify initial state
      await verifyWorkerState(env.pool, workerId, { status: 'ACTIVE' });

      // Simulate worker crash
      await workerService.simulateCrash(workerId);

      // Wait for failure detection
      await waitFor(
        async () => {
          const result = await env.pool.query(
            'SELECT status FROM workers WHERE worker_id = $1',
            [workerId]
          );
          return result.rows[0].status === 'FAILED';
        },
        5000,
        200
      );

      // Verify failure metadata
      const workerResult = await env.pool.query(
        `SELECT
          status,
          failure_count,
          last_failure_at,
          metadata
        FROM workers
        WHERE worker_id = $1`,
        [workerId]
      );

      expect(workerResult.rows[0].status).toBe('FAILED');
      expect(workerResult.rows[0].failure_count).toBeGreaterThan(0);
      expect(workerResult.rows[0].last_failure_at).not.toBeNull();
      expect(workerResult.rows[0].metadata.crashReason).toBeDefined();
    }, 10000);

    test('worker auto-recovery after transient failure', async () => {
      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({
          workerName: 'recovery-test-worker',
          autoRestart: true,
        })
      );

      // Simulate transient failure
      await workerService.simulateTransientFailure(workerId);

      // Wait for auto-recovery
      await waitFor(
        async () => {
          const result = await env.pool.query(
            'SELECT status FROM workers WHERE worker_id = $1',
            [workerId]
          );
          return result.rows[0].status === 'ACTIVE';
        },
        10000,
        500
      );

      // Verify recovery recorded
      const recoveryResult = await env.pool.query(
        `SELECT COUNT(*) as count
        FROM worker_health_logs
        WHERE worker_id = $1
        AND metric_type = 'recovery'`,
        [workerId]
      );

      expect(parseInt(recoveryResult.rows[0].count)).toBeGreaterThan(0);
    }, 15000);
  });

  describe('Predictive Failure Analytics', () => {
    test('degrading health metrics predict failure', async () => {
      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({
          workerName: 'prediction-test-worker',
        })
      );

      // Simulate degrading health over time
      const healthScores = [1.0, 0.9, 0.75, 0.6, 0.45, 0.3];

      for (const score of healthScores) {
        await env.pool.query(
          `INSERT INTO worker_health_logs
          (worker_id, metric_type, metric_value, logged_at)
          VALUES ($1, 'health_score', $2, NOW())`,
          [workerId, score]
        );
        await new Promise(resolve => setTimeout(resolve, 100));
      }

      // Run predictive analytics
      const prediction = await healthMonitor.predictFailure(workerId);

      expect(prediction.failureProbability).toBeGreaterThan(0.7);
      expect(prediction.estimatedTimeToFailure).toBeLessThan(3600000); // < 1 hour
      expect(prediction.recommendedAction).toBe('PREEMPTIVE_RESTART');

      // Verify prediction logged
      const predictionResult = await env.pool.query(
        `SELECT metric_value, metadata
        FROM worker_health_logs
        WHERE worker_id = $1
        AND metric_type = 'failure_prediction'
        ORDER BY logged_at DESC
        LIMIT 1`,
        [workerId]
      );

      expect(predictionResult.rows.length).toBeGreaterThan(0);
      expect(predictionResult.rows[0].metric_value).toBeGreaterThan(0.7);
    }, 5000);

    test('anomaly detection in worker metrics', async () => {
      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({
          workerName: 'anomaly-test-worker',
        })
      );

      // Record normal metrics
      for (let i = 0; i < 10; i++) {
        await env.pool.query(
          `INSERT INTO worker_health_logs
          (worker_id, metric_type, metric_value, logged_at)
          VALUES ($1, 'cpu_usage', $2, NOW())`,
          [workerId, 0.3 + Math.random() * 0.1]
        );
      }

      // Record anomalous spike
      await env.pool.query(
        `INSERT INTO worker_health_logs
        (worker_id, metric_type, metric_value, logged_at)
        VALUES ($1, 'cpu_usage', $2, NOW())`,
        [workerId, 0.95]
      );

      // Run anomaly detection
      const anomalies = await healthMonitor.detectAnomalies(workerId);

      expect(anomalies.length).toBeGreaterThan(0);
      expect(anomalies[0].metricType).toBe('cpu_usage');
      expect(anomalies[0].severity).toBeGreaterThanOrEqual(3);
      expect(anomalies[0].anomalyScore).toBeGreaterThan(2.0); // > 2 std deviations
    }, 5000);
  });

  describe('Worker Load Balancing', () => {
    test('health-aware load distribution', async () => {
      // Spawn workers with varying health
      const healthyWorkerId = await workerService.spawnWorker(
        generateTestWorkerConfig({
          workerName: 'healthy-worker',
        })
      );

      const degradedWorkerId = await workerService.spawnWorker(
        generateTestWorkerConfig({
          workerName: 'degraded-worker',
        })
      );

      // Set health scores
      await env.pool.query(
        'UPDATE workers SET health_score = $1 WHERE worker_id = $2',
        [1.0, healthyWorkerId]
      );

      await env.pool.query(
        'UPDATE workers SET health_score = $1 WHERE worker_id = $2',
        [0.5, degradedWorkerId]
      );

      // Request optimal worker for job assignment
      const optimalWorker = await healthMonitor.getOptimalWorker({
        minHealthScore: 0.7,
        maxLoad: 0.8,
      });

      expect(optimalWorker).toBe(healthyWorkerId);

      // Verify degraded worker not selected
      const alternativeWorker = await healthMonitor.getOptimalWorker({
        minHealthScore: 0.3,
        maxLoad: 0.8,
      });

      // Should still prefer healthy worker
      expect(alternativeWorker).toBe(healthyWorkerId);
    }, 5000);

    test('worker evacuation on predicted failure', async () => {
      const workerId = await workerService.spawnWorker(
        generateTestWorkerConfig({
          workerName: 'evacuation-test-worker',
        })
      );

      // Assign some jobs
      await env.pool.query(
        `UPDATE jobs
        SET status = 'PROCESSING', worker_id = $1
        WHERE job_id IN (
          SELECT job_id FROM jobs
          WHERE status = 'PENDING'
          LIMIT 3
        )`,
        [workerId]
      );

      // Trigger evacuation due to predicted failure
      await healthMonitor.evacuateWorker(workerId, {
        reason: 'PREDICTED_FAILURE',
        reassignJobs: true,
      });

      // Verify jobs reassigned
      await waitFor(
        async () => {
          const result = await env.pool.query(
            `SELECT COUNT(*) as count
            FROM jobs
            WHERE worker_id = $1
            AND status = 'PROCESSING'`,
            [workerId]
          );
          return parseInt(result.rows[0].count) === 0;
        },
        5000,
        200
      );

      // Verify worker marked for evacuation
      const workerResult = await env.pool.query(
        'SELECT status, metadata FROM workers WHERE worker_id = $1',
        [workerId]
      );

      expect(workerResult.rows[0].status).toBe('DRAINING');
      expect(workerResult.rows[0].metadata.evacuationReason).toBe(
        'PREDICTED_FAILURE'
      );
    }, 10000);
  });
});
