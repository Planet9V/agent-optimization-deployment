/**
 * Worker Service - GAP-006 Implementation
 * Handles worker spawning, health monitoring, and Byzantine fault tolerance
 * using ruv-swarm mesh topology integration
 */

import { Pool, PoolClient } from 'pg';

// Type declarations for MCP tools (avoiding external dependencies)
declare function mcp__ruv_swarm__swarm_init(params: {
  topology: string;
  maxAgents: number;
  strategy: string;
}): Promise<{ swarmId: string; status: string }>;

declare function mcp__ruv_swarm__agent_spawn(params: {
  type: string;
  name: string;
  capabilities: string[];
}): Promise<{ agentId: string; status: string }>;

declare function mcp__ruv_swarm__neural_predict(params: {
  modelId: string;
  input: string;
}): Promise<{ prediction: string; confidence: number }>;

declare function mcp__claude_flow__memory_usage(params: {
  action: string;
  key: string;
  value: string;
  namespace: string;
  ttl?: number;
}): Promise<{ status: string }>;

export interface WorkerConfig {
  workerName: string;
  workerType: string;
  capabilities: string[];
  maxConcurrentJobs?: number;
}

export interface WorkerHealth {
  workerId: string;
  status: 'IDLE' | 'BUSY' | 'DEGRADED' | 'FAILING';
  lastHeartbeat: Date;
  cpuUsage: number;
  memoryUsage: number;
  errorRate: number;
  taskCount: number;
}

export interface WorkerMetrics {
  cpuUsagePercent: number;
  memoryUsagePercent: number;
  errorRate: number;
  taskCount: number;
  uptimeHours: number;
  secondsSinceHeartbeat: number;
}

export interface FailurePrediction {
  prediction: 'HEALTHY' | 'DEGRADED' | 'FAILING';
  confidence: number;
  metrics: WorkerMetrics;
  recommendedAction: 'NONE' | 'MONITOR' | 'REPLACE';
}

export class WorkerService {
  private pool: Pool;
  private swarmId: string | null = null;
  private readonly HEARTBEAT_TIMEOUT = 60; // seconds
  private readonly FAILURE_THRESHOLD = 0.7; // 70% confidence

  constructor(poolConfig?: {
    host?: string;
    database?: string;
    user?: string;
    password?: string;
    max?: number;
  }) {
    this.pool = new Pool({
      host: poolConfig?.host || process.env.POSTGRES_HOST || 'localhost',
      database: poolConfig?.database || 'aeon_saas_dev',
      user: poolConfig?.user || process.env.POSTGRES_USER || 'postgres',
      password: poolConfig?.password || process.env.POSTGRES_PASSWORD,
      max: poolConfig?.max || 20,
    });
  }

  /**
   * Initialize swarm topology if not already initialized
   */
  private async ensureSwarmInitialized(): Promise<string> {
    if (this.swarmId) {
      return this.swarmId;
    }

    try {
      const swarmResult = await mcp__ruv_swarm__swarm_init({
        topology: 'mesh',
        maxAgents: 5,
        strategy: 'adaptive',
      });

      this.swarmId = swarmResult.swarmId;
      return this.swarmId;
    } catch (error) {
      throw new Error(`Failed to initialize swarm: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Spawn a new worker using ruv-swarm integration
   * Returns the worker ID from PostgreSQL
   */
  async spawnWorker(config: WorkerConfig): Promise<string> {
    const client: PoolClient = await this.pool.connect();

    try {
      await client.query('BEGIN');

      // 1. Initialize swarm if needed
      await this.ensureSwarmInitialized();

      // 2. Spawn worker agent in ruv-swarm
      const agentResult = await mcp__ruv_swarm__agent_spawn({
        type: 'coordinator',
        name: config.workerName,
        capabilities: config.capabilities,
      });

      // 3. Register worker in PostgreSQL
      const insertResult = await client.query(
        `INSERT INTO workers (
          worker_name,
          worker_type,
          status,
          capabilities,
          max_concurrent_jobs,
          last_heartbeat,
          created_at
        )
        VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
        RETURNING worker_id`,
        [
          config.workerName,
          config.workerType,
          'IDLE',
          JSON.stringify(config.capabilities),
          config.maxConcurrentJobs || 5,
        ]
      );

      const workerId = insertResult.rows[0].worker_id;

      // 4. Store worker config in memory for coordination
      await mcp__claude_flow__memory_usage({
        action: 'store',
        key: `worker/${workerId}/config`,
        value: JSON.stringify({
          workerId,
          agentId: agentResult.agentId,
          workerName: config.workerName,
          workerType: config.workerType,
          capabilities: config.capabilities,
          maxConcurrentJobs: config.maxConcurrentJobs || 5,
          spawnedAt: new Date().toISOString(),
          swarmId: this.swarmId,
        }),
        namespace: 'worker-coordination',
        ttl: 3600, // 1 hour TTL
      });

      await client.query('COMMIT');

      return workerId;
    } catch (error) {
      await client.query('ROLLBACK');
      throw new Error(`Failed to spawn worker: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      client.release();
    }
  }

  /**
   * Update worker heartbeat and status
   */
  async updateHeartbeat(workerId: string, health: WorkerHealth): Promise<void> {
    try {
      const result = await this.pool.query(
        `UPDATE workers
         SET last_heartbeat = NOW(),
             status = $2
         WHERE worker_id = $1
         RETURNING worker_id`,
        [workerId, health.status]
      );

      if (result.rowCount === 0) {
        throw new Error(`Worker not found: ${workerId}`);
      }

      // Store health metrics in memory
      await mcp__claude_flow__memory_usage({
        action: 'store',
        key: `worker/${workerId}/health`,
        value: JSON.stringify({
          ...health,
          timestamp: new Date().toISOString(),
        }),
        namespace: 'worker-coordination',
        ttl: 300, // 5 minutes
      });
    } catch (error) {
      throw new Error(`Failed to update heartbeat: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Get worker metrics from database
   */
  private async getWorkerMetrics(workerId: string): Promise<WorkerMetrics> {
    const result = await this.pool.query(
      `SELECT
        worker_name,
        status,
        total_jobs_completed,
        total_jobs_failed,
        created_at,
        EXTRACT(EPOCH FROM (NOW() - last_heartbeat)) as seconds_since_heartbeat,
        EXTRACT(EPOCH FROM (NOW() - created_at)) / 3600 as uptime_hours
       FROM workers
       WHERE worker_id = $1`,
      [workerId]
    );

    if (result.rows.length === 0) {
      throw new Error(`Worker not found: ${workerId}`);
    }

    const worker = result.rows[0];
    const totalJobs = worker.total_jobs_completed + worker.total_jobs_failed;
    const errorRate = totalJobs > 0 ? worker.total_jobs_failed / totalJobs : 0;

    return {
      cpuUsagePercent: 0, // Would integrate with monitoring system
      memoryUsagePercent: 0, // Would integrate with monitoring system
      errorRate,
      taskCount: worker.total_jobs_completed,
      uptimeHours: parseFloat(worker.uptime_hours) || 0,
      secondsSinceHeartbeat: parseFloat(worker.seconds_since_heartbeat) || 0,
    };
  }

  /**
   * Predict worker failure using neural pattern analysis
   */
  async predictWorkerFailure(workerId: string): Promise<FailurePrediction> {
    try {
      const metrics = await this.getWorkerMetrics(workerId);

      // Use ruv-swarm neural prediction for failure analysis
      const prediction = await mcp__ruv_swarm__neural_predict({
        modelId: 'worker-failure',
        input: JSON.stringify(metrics),
      });

      // Determine recommended action based on prediction and confidence
      let recommendedAction: 'NONE' | 'MONITOR' | 'REPLACE' = 'NONE';

      if (prediction.confidence >= this.FAILURE_THRESHOLD) {
        if (prediction.prediction === 'FAILING') {
          recommendedAction = 'REPLACE';
        } else if (prediction.prediction === 'DEGRADED') {
          recommendedAction = 'MONITOR';
        }
      }

      return {
        prediction: prediction.prediction as 'HEALTHY' | 'DEGRADED' | 'FAILING',
        confidence: prediction.confidence,
        metrics,
        recommendedAction,
      };
    } catch (error) {
      throw new Error(`Failed to predict worker failure: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Replace a failing worker with a new one
   * Implements Byzantine fault tolerance by spawning replacement
   */
  async replaceWorker(workerId: string, config: WorkerConfig): Promise<string> {
    const client = await this.pool.connect();

    try {
      await client.query('BEGIN');

      // 1. Mark old worker as failed
      await client.query(
        `UPDATE workers
         SET status = 'FAILED',
             updated_at = NOW()
         WHERE worker_id = $1`,
        [workerId]
      );

      // 2. Get old worker's pending jobs
      const jobsResult = await client.query(
        `SELECT job_id, job_payload
         FROM jobs
         WHERE worker_id = $1
         AND status IN ('PENDING', 'RUNNING')`,
        [workerId]
      );

      // 3. Spawn new worker
      const newWorkerId = await this.spawnWorker(config);

      // 4. Reassign pending jobs to new worker
      if (jobsResult.rows.length > 0) {
        await client.query(
          `UPDATE jobs
           SET worker_id = $1,
               status = 'PENDING',
               updated_at = NOW()
           WHERE worker_id = $2
           AND status IN ('PENDING', 'RUNNING')`,
          [newWorkerId, workerId]
        );
      }

      // 5. Store replacement event in memory
      await mcp__claude_flow__memory_usage({
        action: 'store',
        key: `worker/${workerId}/replacement`,
        value: JSON.stringify({
          oldWorkerId: workerId,
          newWorkerId,
          replacedAt: new Date().toISOString(),
          jobsReassigned: jobsResult.rows.length,
        }),
        namespace: 'worker-coordination',
        ttl: 86400, // 24 hours
      });

      await client.query('COMMIT');

      return newWorkerId;
    } catch (error) {
      await client.query('ROLLBACK');
      throw new Error(`Failed to replace worker: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      client.release();
    }
  }

  /**
   * Get all active workers
   */
  async getActiveWorkers(): Promise<Array<{
    workerId: string;
    workerName: string;
    workerType: string;
    status: string;
    capabilities: string[];
    lastHeartbeat: Date;
  }>> {
    const result = await this.pool.query(
      `SELECT
        worker_id,
        worker_name,
        worker_type,
        status,
        capabilities,
        last_heartbeat
       FROM workers
       WHERE status IN ('IDLE', 'BUSY', 'DEGRADED')
       ORDER BY last_heartbeat DESC`
    );

    return result.rows.map(row => ({
      workerId: row.worker_id,
      workerName: row.worker_name,
      workerType: row.worker_type,
      status: row.status,
      capabilities: JSON.parse(row.capabilities),
      lastHeartbeat: row.last_heartbeat,
    }));
  }

  /**
   * Check for workers with stale heartbeats
   */
  async checkStaleWorkers(): Promise<string[]> {
    const result = await this.pool.query(
      `SELECT worker_id
       FROM workers
       WHERE status IN ('IDLE', 'BUSY', 'DEGRADED')
       AND EXTRACT(EPOCH FROM (NOW() - last_heartbeat)) > $1`,
      [this.HEARTBEAT_TIMEOUT]
    );

    return result.rows.map(row => row.worker_id);
  }

  /**
   * Close database connection pool
   */
  async close(): Promise<void> {
    await this.pool.end();
  }
}

export default WorkerService;
