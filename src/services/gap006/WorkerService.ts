/**
 * File: WorkerService.ts
 * Created: 2025-11-15
 * Modified: 2025-11-15
 * Version: v1.0.0
 * Author: AEON FORGE
 * Purpose: Worker management service with ruv-swarm mesh integration for GAP-006
 * Dependencies: pg, ioredis, @qdrant/js-client-rest (via MCP tools)
 * Status: ACTIVE
 */

import { Pool, PoolClient } from 'pg';
import Redis from 'ioredis';
import { v4 as uuidv4 } from 'uuid';

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
  value?: string;
  namespace?: string;
  ttl?: number;
}): Promise<{ status: string; value?: string }>;

export interface WorkerConfig {
  workerName: string;
  workerType?: string;
  capabilities?: string[];
  maxConcurrentJobs?: number;
  heartbeatIntervalMs?: number;
  autoRestart?: boolean;
}

export interface WorkerHealth {
  workerId: string;
  status: 'IDLE' | 'BUSY' | 'DEGRADED' | 'FAILING' | 'ACTIVE' | 'FAILED' | 'DRAINING';
  lastHeartbeat: Date;
  cpuUsage?: number;
  memoryUsage?: number;
  errorRate?: number;
  taskCount?: number;
  healthScore?: number;
}

export class WorkerService {
  private pool: Pool;
  private redis: Redis;
  private heartbeatIntervals: Map<string, NodeJS.Timeout> = new Map();

  constructor(pool: Pool, redis: Redis) {
    this.pool = pool;
    this.redis = redis;
  }

  /**
   * Spawn a new worker using ruv-swarm mesh topology
   */
  async spawnWorker(config: WorkerConfig): Promise<string> {
    const workerId = uuidv4();
    const workerType = config.workerType || 'general';
    const capabilities = config.capabilities || ['job-processing'];
    const maxConcurrentJobs = config.maxConcurrentJobs || 5;
    const heartbeatInterval = config.heartbeatIntervalMs || 30000; // 30 seconds default

    try {
      // Initialize worker in PostgreSQL
      const insertResult = await this.pool.query(
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
        RETURNING worker_id`,
        [
          workerId,
          config.workerName,
          workerType,
          'ACTIVE',
          maxConcurrentJobs,
          0,
          1.0, // Initial health score
          JSON.stringify({
            capabilities,
            heartbeatInterval,
            autoRestart: config.autoRestart || false
          })
        ]
      );

      // Store worker state in redis
      await this.redis.hset(
        `worker:${workerId}`,
        'name', config.workerName,
        'type', workerType,
        'status', 'ACTIVE',
        'capacity', maxConcurrentJobs.toString(),
        'load', '0'
      );

      // Store in claude-flow memory for persistence (if available)
      try {
        if (typeof mcp__claude_flow__memory_usage !== 'undefined') {
          await mcp__claude_flow__memory_usage({
            action: 'store',
            key: `worker:${workerId}:config`,
            value: JSON.stringify(config),
            namespace: 'worker-coordination',
            ttl: 3600 // 1 hour
          });
        }
      } catch (error) {
        console.warn('claude-flow memory storage failed (non-critical):', error);
      }

      // Initialize ruv-swarm agent (only if capabilities include swarm coordination)
      if (capabilities.includes('swarm-coordination')) {
        try {
          const swarmAgent = await mcp__ruv_swarm__agent_spawn({
            type: 'coordinator',
            name: config.workerName,
            capabilities: capabilities
          });

          await this.pool.query(
            `UPDATE workers SET metadata = metadata || $1 WHERE worker_id = $2`,
            [JSON.stringify({ swarmAgentId: swarmAgent.agentId }), workerId]
          );
        } catch (error) {
          console.warn('ruv-swarm agent spawn failed (non-critical):', error);
        }
      }

      // Start heartbeat monitoring
      if (heartbeatInterval > 0) {
        this.startHeartbeat(workerId, heartbeatInterval);
      }

      return workerId;
    } catch (error) {
      console.error('Worker spawn error:', error);
      throw new Error(`Failed to spawn worker: ${error.message}`);
    }
  }

  /**
   * Start heartbeat monitoring for a worker
   */
  private startHeartbeat(workerId: string, intervalMs: number): void {
    const heartbeatTimer = setInterval(async () => {
      try {
        await this.pool.query(
          `UPDATE workers SET last_heartbeat = NOW(), updated_at = NOW()
           WHERE worker_id = $1`,
          [workerId]
        );

        await this.redis.hset(`worker:${workerId}`, 'last_heartbeat', Date.now().toString());

        // Log heartbeat
        await this.pool.query(
          `INSERT INTO worker_health_logs (worker_id, metric_type, metric_value, logged_at)
           VALUES ($1, 'heartbeat', 1.0, NOW())`,
          [workerId]
        );
      } catch (error) {
        console.error(`Heartbeat error for worker ${workerId}:`, error);
      }
    }, intervalMs);

    this.heartbeatIntervals.set(workerId, heartbeatTimer);
  }

  /**
   * Pause worker heartbeat (for testing)
   */
  async pauseWorkerHeartbeat(workerId: string): Promise<void> {
    const timer = this.heartbeatIntervals.get(workerId);
    if (timer) {
      clearInterval(timer);
      this.heartbeatIntervals.delete(workerId);
    }
  }

  /**
   * Simulate worker crash (for testing)
   */
  async simulateCrash(workerId: string): Promise<void> {
    await this.pauseWorkerHeartbeat(workerId);

    await this.pool.query(
      `UPDATE workers SET
        status = 'FAILED',
        failure_count = failure_count + 1,
        last_failure_at = NOW(),
        metadata = metadata || $1,
        updated_at = NOW()
       WHERE worker_id = $2`,
      [JSON.stringify({ crashReason: 'Simulated crash for testing' }), workerId]
    );

    await this.redis.hset(`worker:${workerId}`, 'status', 'FAILED');
  }

  /**
   * Simulate transient failure (for testing)
   */
  async simulateTransientFailure(workerId: string): Promise<void> {
    await this.pool.query(
      `UPDATE workers SET status = 'DEGRADED', updated_at = NOW()
       WHERE worker_id = $1`,
      [workerId]
    );

    await this.redis.hset(`worker:${workerId}`, 'status', 'DEGRADED');

    // Auto-recover after 5 seconds
    setTimeout(async () => {
      await this.pool.query(
        `UPDATE workers SET status = 'ACTIVE', updated_at = NOW()
         WHERE worker_id = $1`,
        [workerId]
      );

      await this.redis.hset(`worker:${workerId}`, 'status', 'ACTIVE');

      // Log recovery
      await this.pool.query(
        `INSERT INTO worker_health_logs (worker_id, metric_type, metric_value, metadata, logged_at)
         VALUES ($1, 'recovery', 1.0, $2, NOW())`,
        [workerId, JSON.stringify({ recoveryType: 'auto', reason: 'transient_failure' })]
      );
    }, 5000);
  }

  /**
   * Get worker health information
   */
  async getWorkerHealth(workerId: string): Promise<WorkerHealth | null> {
    const result = await this.pool.query(
      `SELECT worker_id, status, last_heartbeat, health_score, current_load
       FROM workers
       WHERE worker_id = $1`,
      [workerId]
    );

    if (result.rows.length === 0) {
      return null;
    }

    const row = result.rows[0];
    return {
      workerId: row.worker_id,
      status: row.status,
      lastHeartbeat: row.last_heartbeat,
      healthScore: row.health_score,
      taskCount: row.current_load
    };
  }

  /**
   * Cleanup: Stop all heartbeat timers
   */
  async cleanup(): Promise<void> {
    for (const timer of this.heartbeatIntervals.values()) {
      clearInterval(timer);
    }
    this.heartbeatIntervals.clear();
  }
}
