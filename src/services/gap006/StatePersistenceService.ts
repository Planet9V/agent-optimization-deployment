/**
 * File: StatePersistenceService.ts
 * Created: 2025-11-15
 * Modified: 2025-11-15
 * Version: v1.0.0
 * Author: AEON FORGE
 * Purpose: State persistence service using Qdrant for GAP-006
 * Dependencies: pg, ioredis, @qdrant/js-client-rest
 * Status: ACTIVE
 */

import { Pool } from 'pg';
import Redis from 'ioredis';
import { QdrantClient } from '@qdrant/js-client-rest';
import { v4 as uuidv4 } from 'uuid';

interface SnapshotConfig {
  snapshotType: 'FULL' | 'INCREMENTAL' | 'AUTO';
  description?: string;
  baseSnapshotId?: string;
}

interface RestoreOptions {
  conflictResolution?: 'MERGE' | 'OVERWRITE' | 'SKIP';
  preserveNewData?: boolean;
}

interface Conflict {
  type: string;
  resolution: string;
  details?: any;
}

export interface ExecutionContext {
  jobId?: string;  // Optional to support test cases that pass context without jobId
  workerId?: string;
  executionSteps?: any[];
  intermediateResults?: any;
  jobType?: string;
  payload?: any;
  result?: any;
  steps?: string[];
  duration?: number;
  [key: string]: any;
}

interface SimilarExecution {
  jobId: string;
  score: number;
  payload?: any;
}

interface AutoSnapshotConfig {
  intervalMinutes: number;
  retentionDays: number;
}

export class StatePersistenceService {
  private pool: Pool;
  private redis: Redis;
  private qdrant: QdrantClient;
  private autoSnapshotTimer: NodeJS.Timeout | null = null;

  constructor(pool: Pool, redis: Redis, qdrant: QdrantClient) {
    this.pool = pool;
    this.redis = redis;
    this.qdrant = qdrant;
  }

  /**
   * Create a system state snapshot
   */
  async createSnapshot(config: SnapshotConfig): Promise<string> {
    const snapshotId = uuidv4();

    try {
      // Capture current state
      const workersResult = await this.pool.query(
        'SELECT * FROM workers WHERE status != $1',
        ['TERMINATED']
      );

      const jobsResult = await this.pool.query(
        'SELECT * FROM jobs WHERE status IN ($1, $2, $3)',
        ['PENDING', 'PROCESSING', 'COMPLETED']
      );

      const stateData: any = {
        workers: workersResult.rows,
        jobs: jobsResult.rows,
        timestamp: new Date().toISOString()
      };

      // If incremental, only store changes
      if (config.snapshotType === 'INCREMENTAL' && config.baseSnapshotId) {
        const baseSnapshot = await this.pool.query(
          'SELECT state_data FROM state_snapshots WHERE snapshot_id = $1',
          [config.baseSnapshotId]
        );

        if (baseSnapshot.rows.length > 0) {
          const baseState = baseSnapshot.rows[0].state_data;
          stateData.changes = this.calculateChanges(baseState, stateData);
          stateData.baseSnapshotId = config.baseSnapshotId;
        }
      }

      // Store snapshot in PostgreSQL
      await this.pool.query(
        `INSERT INTO state_snapshots (
          snapshot_id,
          snapshot_type,
          state_data,
          metadata,
          created_at
        ) VALUES ($1, $2, $3, $4, NOW())`,
        [
          snapshotId,
          config.snapshotType,
          JSON.stringify(stateData),
          JSON.stringify({ description: config.description || '' })
        ]
      );

      // Store in Qdrant for vector search
      await this.qdrant.upsert('gap006_state', {
        points: [
          {
            id: snapshotId,
            vector: await this.generateStateVector(stateData),
            payload: {
              snapshotType: config.snapshotType,
              timestamp: new Date().toISOString(),
              workerCount: workersResult.rows.length,
              jobCount: jobsResult.rows.length
            }
          }
        ]
      });

      return snapshotId;
    } catch (error) {
      console.error('Snapshot creation error:', error);
      throw new Error(`Failed to create snapshot: ${error.message}`);
    }
  }

  /**
   * Restore system state from a snapshot
   */
  async restoreFromSnapshot(
    snapshotId: string,
    options: RestoreOptions = {}
  ): Promise<Conflict[]> {
    const conflicts: Conflict[] = [];

    try {
      const snapshotResult = await this.pool.query(
        'SELECT state_data FROM state_snapshots WHERE snapshot_id = $1',
        [snapshotId]
      );

      if (snapshotResult.rows.length === 0) {
        throw new Error(`Snapshot ${snapshotId} not found`);
      }

      const stateData = snapshotResult.rows[0].state_data;

      // Restore workers
      for (const worker of stateData.workers || []) {
        const existing = await this.pool.query(
          'SELECT status FROM workers WHERE worker_id = $1',
          [worker.worker_id]
        );

        if (existing.rows.length > 0 && options.preserveNewData) {
          // Conflict detected
          if (existing.rows[0].status !== worker.status) {
            conflicts.push({
              type: 'WORKER_STATUS_CONFLICT',
              resolution: 'PRESERVED_CURRENT',
              details: {
                workerId: worker.worker_id,
                snapshotStatus: worker.status,
                currentStatus: existing.rows[0].status
              }
            });
          }
        } else {
          await this.pool.query(
            `INSERT INTO workers (
              worker_id, worker_name, worker_type, status, capacity,
              current_load, last_heartbeat, health_score, metadata, created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, NOW(), NOW())
            ON CONFLICT (worker_id) DO UPDATE SET
              status = EXCLUDED.status,
              updated_at = NOW()`,
            [
              worker.worker_id,
              worker.worker_name,
              worker.worker_type,
              worker.status,
              worker.capacity,
              worker.current_load,
              worker.last_heartbeat,
              worker.health_score,
              worker.metadata
            ]
          );
        }
      }

      // Restore jobs
      for (const job of stateData.jobs || []) {
        await this.pool.query(
          `INSERT INTO jobs (
            job_id, job_type, status, priority, payload, max_retries,
            retry_count, timeout_ms, created_at, updated_at
          ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW(), NOW())
          ON CONFLICT (job_id) DO UPDATE SET
            status = EXCLUDED.status,
            updated_at = NOW()`,
          [
            job.job_id,
            job.job_type,
            job.status,
            job.priority,
            job.payload,
            job.max_retries,
            job.retry_count,
            job.timeout_ms
          ]
        );
      }

      return conflicts;
    } catch (error) {
      console.error('Restore error:', error);
      throw new Error(`Failed to restore from snapshot: ${error.message}`);
    }
  }

  /**
   * Store execution context in Qdrant
   */
  async storeExecutionContext(jobId: string, context: ExecutionContext): Promise<void> {
    try {
      const vector = await this.generateContextVector(context);

      await this.qdrant.upsert('gap006_state', {
        points: [
          {
            id: jobId, // Qdrant requires UUID without prefix
            vector,
            payload: {
              ...context,
              contextType: 'execution',
              timestamp: new Date().toISOString()
            }
          }
        ]
      });
    } catch (error) {
      console.error('Context storage error:', error);
      throw new Error(`Failed to store execution context: ${error.message}`);
    }
  }

  /**
   * Retrieve execution context from Qdrant
   */
  async retrieveExecutionContext(jobId: string): Promise<ExecutionContext | null> {
    try {
      const results = await this.qdrant.retrieve('gap006_state', {
        ids: [jobId] // Qdrant requires UUID without prefix
      });

      if (results.length > 0) {
        return results[0].payload as ExecutionContext;
      }

      return null;
    } catch (error) {
      console.error('Context retrieval error:', error);
      return null;
    }
  }

  /**
   * Search for similar executions using vector similarity
   */
  async searchSimilarExecutions(params: {
    queryText: string;
    limit: number;
  }): Promise<SimilarExecution[]> {
    try {
      const queryVector = await this.generateTextVector(params.queryText);

      const searchResults = await this.qdrant.search('gap006_state', {
        vector: queryVector,
        limit: params.limit,
        filter: {
          must: [{ key: 'contextType', match: { value: 'execution' } }]
        }
      });

      return searchResults.map(result => ({
        jobId: result.payload?.jobId as string,
        score: result.score,
        payload: result.payload
      }));
    } catch (error) {
      console.error('Similar execution search error:', error);
      return [];
    }
  }

  /**
   * Find similar execution patterns
   */
  async findSimilarPatterns(
    jobId: string,
    options: { minSimilarity: number }
  ): Promise<Array<{ jobId: string; similarity: number }>> {
    try {
      const context = await this.retrieveExecutionContext(jobId);
      if (!context) {
        return [];
      }

      const queryVector = await this.generateContextVector(context);

      const searchResults = await this.qdrant.search('gap006_state', {
        vector: queryVector,
        limit: 10,
        score_threshold: options.minSimilarity,
        filter: {
          must: [{ key: 'contextType', match: { value: 'execution' } }]
        }
      });

      return searchResults
        .filter(r => r.payload?.jobId !== jobId)
        .map(result => ({
          jobId: result.payload?.jobId as string,
          similarity: result.score
        }));
    } catch (error) {
      console.error('Pattern matching error:', error);
      return [];
    }
  }

  /**
   * Enable automatic snapshots
   */
  async enableAutoSnapshot(config: AutoSnapshotConfig): Promise<void> {
    // Clear existing timer if any
    if (this.autoSnapshotTimer) {
      clearInterval(this.autoSnapshotTimer);
    }

    // Schedule automatic snapshots
    const intervalMs = config.intervalMinutes * 60 * 1000;

    this.autoSnapshotTimer = setInterval(async () => {
      try {
        await this.createSnapshot({
          snapshotType: 'AUTO',
          description: `Auto-snapshot at ${new Date().toISOString()}`
        });

        // Clean up old snapshots beyond retention period
        const retentionDate = new Date();
        retentionDate.setDate(retentionDate.getDate() - config.retentionDays);

        await this.pool.query(
          `DELETE FROM state_snapshots
           WHERE snapshot_type = 'AUTO'
           AND created_at < $1`,
          [retentionDate]
        );
      } catch (error) {
        console.error('Auto-snapshot error:', error);
      }
    }, intervalMs);

    console.log('Auto-snapshot enabled:', config);
  }

  /**
   * Disable automatic snapshots
   */
  async disableAutoSnapshot(): Promise<void> {
    if (this.autoSnapshotTimer) {
      clearInterval(this.autoSnapshotTimer);
      this.autoSnapshotTimer = null;
    }
  }

  /**
   * Cleanup: Stop auto-snapshot timer
   */
  async cleanup(): Promise<void> {
    await this.disableAutoSnapshot();
  }

  /**
   * Point-in-time recovery
   */
  async pointInTimeRecovery(timestamp: Date): Promise<void> {
    // Find the closest snapshot before the target timestamp
    const snapshotResult = await this.pool.query(
      `SELECT snapshot_id FROM state_snapshots
       WHERE created_at <= $1
       ORDER BY created_at DESC
       LIMIT 1`,
      [timestamp]
    );

    if (snapshotResult.rows.length > 0) {
      await this.restoreFromSnapshot(snapshotResult.rows[0].snapshot_id);
    } else {
      throw new Error(`No snapshot found before ${timestamp.toISOString()}`);
    }
  }

  /**
   * Calculate changes between states (for incremental snapshots)
   */
  private calculateChanges(baseState: any, currentState: any): any {
    const changes: any = {};

    // Compare jobs
    const completedJobs = currentState.jobs
      .filter((job: any) => job.status === 'COMPLETED')
      .map((job: any) => job.job_id);

    changes.completedJobs = completedJobs;

    return changes;
  }

  /**
   * Generate vector embedding for state data (simplified mock)
   */
  private async generateStateVector(stateData: any): Promise<number[]> {
    // Mock: Generate a 384-dimensional vector based on state characteristics
    const vector = new Array(384).fill(0);
    vector[0] = stateData.workers?.length || 0;
    vector[1] = stateData.jobs?.length || 0;
    return vector;
  }

  /**
   * Generate vector embedding for execution context (improved mock with variance)
   */
  private async generateContextVector(context: any): Promise<number[]> {
    // Create base vector with small random variance
    const vector = new Array(384).fill(0).map(() => Math.random() * 0.05);

    // Add semantic features from context
    vector[0] = (context.executionSteps?.length || 0) / 100;
    vector[1] = (context.jobType?.length || 0) / 100;
    vector[2] = (context.steps?.length || 0) / 100;
    vector[3] = (context.duration || 0) / 10000;

    // Add payload signature if available
    if (context.payload) {
      const payloadStr = JSON.stringify(context.payload);
      vector[4] = (payloadStr.length || 0) / 1000;
      // Simple hash-like feature from payload
      vector[5] = (payloadStr.split('').reduce((sum, char) => sum + char.charCodeAt(0), 0) % 100) / 100;
    }

    // Add result signature if available
    if (context.result) {
      const resultStr = JSON.stringify(context.result);
      vector[6] = (resultStr.length || 0) / 1000;
    }

    // Normalize vector to unit length
    const magnitude = Math.sqrt(vector.reduce((sum, val) => sum + val * val, 0));
    if (magnitude > 0) {
      return vector.map(val => val / magnitude);
    }

    return vector;
  }

  /**
   * Generate vector embedding from text (improved mock with variance)
   */
  private async generateTextVector(text: string): Promise<number[]> {
    // Create base vector with small random variance
    const vector = new Array(384).fill(0).map(() => Math.random() * 0.05);

    // Add text features
    vector[0] = text.length / 1000;
    vector[1] = (text.split(' ').length || 0) / 100;
    vector[2] = (text.split('\n').length || 0) / 100;

    // Add word frequency features (top common words)
    const words = text.toLowerCase().split(/\s+/);
    const commonWords = ['data', 'analysis', 'statistical', 'transform', 'process'];
    commonWords.forEach((word, idx) => {
      const count = words.filter(w => w.includes(word)).length;
      vector[10 + idx] = count / words.length;
    });

    // Add character-based hash features
    for (let i = 0; i < Math.min(text.length, 20); i++) {
      vector[20 + i] = (text.charCodeAt(i) % 100) / 100;
    }

    // Normalize vector to unit length
    const magnitude = Math.sqrt(vector.reduce((sum, val) => sum + val * val, 0));
    if (magnitude > 0) {
      return vector.map(val => val / magnitude);
    }

    return vector;
  }
}
