/**
 * Worker Service Tests - GAP-006
 * Unit tests for worker spawning, health monitoring, and fault tolerance
 */

import { describe, test, expect, beforeAll, afterAll, beforeEach } from '@jest/globals';
import { Pool } from 'pg';
import WorkerService, { WorkerConfig, WorkerHealth } from '../../src/services/gap006/worker-service';

// Mock MCP functions
const mockSwarmInit = jest.fn();
const mockAgentSpawn = jest.fn();
const mockNeuralPredict = jest.fn();
const mockMemoryUsage = jest.fn();

global.mcp__ruv_swarm__swarm_init = mockSwarmInit;
global.mcp__ruv_swarm__agent_spawn = mockAgentSpawn;
global.mcp__ruv_swarm__neural_predict = mockNeuralPredict;
global.mcp__claude_flow__memory_usage = mockMemoryUsage;

describe('WorkerService', () => {
  let workerService: WorkerService;
  let testPool: Pool;
  let testWorkerId: string;

  beforeAll(async () => {
    // Initialize test database connection
    testPool = new Pool({
      host: process.env.POSTGRES_HOST || 'localhost',
      database: 'aeon_saas_test',
      user: process.env.POSTGRES_USER || 'postgres',
      password: process.env.POSTGRES_PASSWORD,
      max: 5,
    });

    // Create test schema
    await testPool.query(`
      CREATE TABLE IF NOT EXISTS workers (
        worker_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        worker_name VARCHAR(255) NOT NULL,
        worker_type VARCHAR(100) NOT NULL,
        status VARCHAR(50) DEFAULT 'IDLE',
        capabilities JSONB DEFAULT '[]',
        max_concurrent_jobs INTEGER DEFAULT 5,
        total_jobs_completed INTEGER DEFAULT 0,
        total_jobs_failed INTEGER DEFAULT 0,
        last_heartbeat TIMESTAMP DEFAULT NOW(),
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
      )
    `);

    await testPool.query(`
      CREATE TABLE IF NOT EXISTS jobs (
        job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        worker_id UUID REFERENCES workers(worker_id),
        job_payload JSONB,
        status VARCHAR(50) DEFAULT 'PENDING',
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
      )
    `);

    workerService = new WorkerService({
      host: process.env.POSTGRES_HOST || 'localhost',
      database: 'aeon_saas_test',
      user: process.env.POSTGRES_USER || 'postgres',
      password: process.env.POSTGRES_PASSWORD,
      max: 5,
    });
  });

  afterAll(async () => {
    await workerService.close();
    await testPool.query('DROP TABLE IF EXISTS jobs CASCADE');
    await testPool.query('DROP TABLE IF EXISTS workers CASCADE');
    await testPool.end();
  });

  beforeEach(async () => {
    // Clean up test data
    await testPool.query('DELETE FROM jobs');
    await testPool.query('DELETE FROM workers');

    // Reset mocks
    jest.clearAllMocks();

    // Setup default mock responses
    mockSwarmInit.mockResolvedValue({
      swarmId: 'test-swarm-123',
      status: 'initialized',
    });

    mockAgentSpawn.mockResolvedValue({
      agentId: 'test-agent-456',
      status: 'spawned',
    });

    mockNeuralPredict.mockResolvedValue({
      prediction: 'HEALTHY',
      confidence: 0.95,
    });

    mockMemoryUsage.mockResolvedValue({
      status: 'stored',
    });
  });

  describe('spawnWorker', () => {
    test('should spawn a new worker successfully', async () => {
      const config: WorkerConfig = {
        workerName: 'test-worker-1',
        workerType: 'coordinator',
        capabilities: ['data-processing', 'analytics'],
        maxConcurrentJobs: 10,
      };

      const workerId = await workerService.spawnWorker(config);

      expect(workerId).toBeDefined();
      expect(typeof workerId).toBe('string');

      // Verify swarm initialization
      expect(mockSwarmInit).toHaveBeenCalledWith({
        topology: 'mesh',
        maxAgents: 5,
        strategy: 'adaptive',
      });

      // Verify agent spawning
      expect(mockAgentSpawn).toHaveBeenCalledWith({
        type: 'coordinator',
        name: 'test-worker-1',
        capabilities: ['data-processing', 'analytics'],
      });

      // Verify memory storage
      expect(mockMemoryUsage).toHaveBeenCalledWith(
        expect.objectContaining({
          action: 'store',
          namespace: 'worker-coordination',
        })
      );

      // Verify database insertion
      const result = await testPool.query(
        'SELECT * FROM workers WHERE worker_id = $1',
        [workerId]
      );

      expect(result.rows).toHaveLength(1);
      expect(result.rows[0].worker_name).toBe('test-worker-1');
      expect(result.rows[0].worker_type).toBe('coordinator');
      expect(result.rows[0].status).toBe('IDLE');
      expect(result.rows[0].max_concurrent_jobs).toBe(10);
    });

    test('should reuse existing swarm for multiple workers', async () => {
      const config1: WorkerConfig = {
        workerName: 'worker-1',
        workerType: 'coordinator',
        capabilities: ['task-1'],
      };

      const config2: WorkerConfig = {
        workerName: 'worker-2',
        workerType: 'analyzer',
        capabilities: ['task-2'],
      };

      await workerService.spawnWorker(config1);
      await workerService.spawnWorker(config2);

      // Swarm should only be initialized once
      expect(mockSwarmInit).toHaveBeenCalledTimes(1);
      expect(mockAgentSpawn).toHaveBeenCalledTimes(2);
    });
  });

  describe('updateHeartbeat', () => {
    beforeEach(async () => {
      const config: WorkerConfig = {
        workerName: 'heartbeat-test-worker',
        workerType: 'coordinator',
        capabilities: ['testing'],
      };
      testWorkerId = await workerService.spawnWorker(config);
    });

    test('should update worker heartbeat successfully', async () => {
      const health: WorkerHealth = {
        workerId: testWorkerId,
        status: 'BUSY',
        lastHeartbeat: new Date(),
        cpuUsage: 45.5,
        memoryUsage: 60.2,
        errorRate: 0.02,
        taskCount: 150,
      };

      await workerService.updateHeartbeat(testWorkerId, health);

      const result = await testPool.query(
        'SELECT status, last_heartbeat FROM workers WHERE worker_id = $1',
        [testWorkerId]
      );

      expect(result.rows[0].status).toBe('BUSY');
    });

    test('should throw error for non-existent worker', async () => {
      const health: WorkerHealth = {
        workerId: 'non-existent-id',
        status: 'IDLE',
        lastHeartbeat: new Date(),
        cpuUsage: 0,
        memoryUsage: 0,
        errorRate: 0,
        taskCount: 0,
      };

      await expect(
        workerService.updateHeartbeat('non-existent-id', health)
      ).rejects.toThrow('Worker not found');
    });
  });

  describe('predictWorkerFailure', () => {
    beforeEach(async () => {
      const config: WorkerConfig = {
        workerName: 'prediction-test-worker',
        workerType: 'coordinator',
        capabilities: ['testing'],
      };
      testWorkerId = await workerService.spawnWorker(config);
    });

    test('should predict healthy worker', async () => {
      mockNeuralPredict.mockResolvedValue({
        prediction: 'HEALTHY',
        confidence: 0.92,
      });

      const prediction = await workerService.predictWorkerFailure(testWorkerId);

      expect(prediction.prediction).toBe('HEALTHY');
      expect(prediction.confidence).toBe(0.92);
      expect(prediction.recommendedAction).toBe('NONE');
      expect(prediction.metrics).toBeDefined();
    });

    test('should predict degraded worker', async () => {
      // Simulate some failures
      await testPool.query(
        'UPDATE workers SET total_jobs_completed = 80, total_jobs_failed = 20 WHERE worker_id = $1',
        [testWorkerId]
      );

      mockNeuralPredict.mockResolvedValue({
        prediction: 'DEGRADED',
        confidence: 0.75,
      });

      const prediction = await workerService.predictWorkerFailure(testWorkerId);

      expect(prediction.prediction).toBe('DEGRADED');
      expect(prediction.recommendedAction).toBe('MONITOR');
    });

    test('should predict failing worker', async () => {
      // Simulate high failure rate
      await testPool.query(
        'UPDATE workers SET total_jobs_completed = 20, total_jobs_failed = 80 WHERE worker_id = $1',
        [testWorkerId]
      );

      mockNeuralPredict.mockResolvedValue({
        prediction: 'FAILING',
        confidence: 0.88,
      });

      const prediction = await workerService.predictWorkerFailure(testWorkerId);

      expect(prediction.prediction).toBe('FAILING');
      expect(prediction.recommendedAction).toBe('REPLACE');
    });
  });

  describe('replaceWorker', () => {
    beforeEach(async () => {
      const config: WorkerConfig = {
        workerName: 'replace-test-worker',
        workerType: 'coordinator',
        capabilities: ['testing'],
      };
      testWorkerId = await workerService.spawnWorker(config);
    });

    test('should replace failing worker', async () => {
      const replacementConfig: WorkerConfig = {
        workerName: 'replacement-worker',
        workerType: 'coordinator',
        capabilities: ['testing'],
      };

      const newWorkerId = await workerService.replaceWorker(
        testWorkerId,
        replacementConfig
      );

      expect(newWorkerId).toBeDefined();
      expect(newWorkerId).not.toBe(testWorkerId);

      // Check old worker marked as failed
      const oldWorker = await testPool.query(
        'SELECT status FROM workers WHERE worker_id = $1',
        [testWorkerId]
      );
      expect(oldWorker.rows[0].status).toBe('FAILED');

      // Check new worker exists
      const newWorker = await testPool.query(
        'SELECT * FROM workers WHERE worker_id = $1',
        [newWorkerId]
      );
      expect(newWorker.rows).toHaveLength(1);
      expect(newWorker.rows[0].status).toBe('IDLE');
    });

    test('should reassign pending jobs to new worker', async () => {
      // Create pending jobs for old worker
      await testPool.query(
        `INSERT INTO jobs (worker_id, job_payload, status)
         VALUES ($1, '{"task": "test"}', 'PENDING'),
                ($1, '{"task": "test2"}', 'RUNNING')`,
        [testWorkerId]
      );

      const replacementConfig: WorkerConfig = {
        workerName: 'replacement-worker',
        workerType: 'coordinator',
        capabilities: ['testing'],
      };

      const newWorkerId = await workerService.replaceWorker(
        testWorkerId,
        replacementConfig
      );

      // Check jobs reassigned
      const jobs = await testPool.query(
        'SELECT * FROM jobs WHERE worker_id = $1',
        [newWorkerId]
      );

      expect(jobs.rows).toHaveLength(2);
      expect(jobs.rows.every(job => job.status === 'PENDING')).toBe(true);
    });
  });

  describe('getActiveWorkers', () => {
    test('should return all active workers', async () => {
      // Spawn multiple workers
      const configs: WorkerConfig[] = [
        { workerName: 'worker-1', workerType: 'coordinator', capabilities: ['task-1'] },
        { workerName: 'worker-2', workerType: 'analyzer', capabilities: ['task-2'] },
        { workerName: 'worker-3', workerType: 'coordinator', capabilities: ['task-3'] },
      ];

      for (const config of configs) {
        await workerService.spawnWorker(config);
      }

      const activeWorkers = await workerService.getActiveWorkers();

      expect(activeWorkers).toHaveLength(3);
      expect(activeWorkers[0]).toHaveProperty('workerId');
      expect(activeWorkers[0]).toHaveProperty('workerName');
      expect(activeWorkers[0]).toHaveProperty('status');
      expect(activeWorkers[0]).toHaveProperty('capabilities');
    });
  });

  describe('checkStaleWorkers', () => {
    test('should detect workers with stale heartbeats', async () => {
      const config: WorkerConfig = {
        workerName: 'stale-worker',
        workerType: 'coordinator',
        capabilities: ['testing'],
      };

      const workerId = await workerService.spawnWorker(config);

      // Set heartbeat to 2 minutes ago
      await testPool.query(
        `UPDATE workers
         SET last_heartbeat = NOW() - INTERVAL '2 minutes'
         WHERE worker_id = $1`,
        [workerId]
      );

      const staleWorkers = await workerService.checkStaleWorkers();

      expect(staleWorkers).toContain(workerId);
    });
  });
});
