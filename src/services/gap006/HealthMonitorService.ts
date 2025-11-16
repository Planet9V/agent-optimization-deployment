/**
 * File: HealthMonitorService.ts
 * Created: 2025-11-15
 * Modified: 2025-11-15
 * Version: v1.0.0
 * Author: AEON FORGE
 * Purpose: Worker health monitoring and predictive analytics for GAP-006
 * Dependencies: pg, ioredis
 * Status: ACTIVE
 */

import { Pool } from 'pg';
import Redis from 'ioredis';

interface FailurePrediction {
  failureProbability: number;
  estimatedTimeToFailure: number;
  recommendedAction: 'CONTINUE' | 'WATCH' | 'PREEMPTIVE_RESTART';
}

interface Anomaly {
  metricType: string;
  severity: number;
  anomalyScore: number;
  timestamp: Date;
}

interface WorkerCriteria {
  minHealthScore?: number;
  maxLoad?: number;
}

interface EvacuationOptions {
  reason: string;
  reassignJobs?: boolean;
}

export class HealthMonitorService {
  private pool: Pool;
  private redis: Redis;

  constructor(pool: Pool, redis: Redis) {
    this.pool = pool;
    this.redis = redis;
  }

  /**
   * Predict worker failure based on health metrics
   */
  async predictFailure(workerId: string): Promise<FailurePrediction> {
    try {
      // Get recent health scores
      const healthResult = await this.pool.query(
        `SELECT metric_value, logged_at
         FROM worker_health_logs
         WHERE worker_id = $1 AND metric_type = 'health_score'
         ORDER BY logged_at DESC
         LIMIT 10`,
        [workerId]
      );

      if (healthResult.rows.length < 3) {
        return {
          failureProbability: 0.1,
          estimatedTimeToFailure: Infinity,
          recommendedAction: 'CONTINUE'
        };
      }

      const scores = healthResult.rows.map(r => parseFloat(r.metric_value));

      // Calculate degradation rate (negative values indicate degrading health)
      const degradationRate = this.calculateDegradationRate(scores);

      // Calculate failure probability with improved formula
      // Higher degradation rate (more negative) should increase probability
      const currentScore = scores[0];
      const degradationFactor = Math.abs(degradationRate) * 2; // Amplify degradation impact
      const baseProbability = 1 - currentScore;
      const failureProbability = Math.max(0, Math.min(1, baseProbability * (1 + degradationFactor)));

      // Estimate time to failure
      const estimatedTimeToFailure = this.estimateTimeToFailure(currentScore, degradationRate);

      // Determine recommended action
      let recommendedAction: 'CONTINUE' | 'WATCH' | 'PREEMPTIVE_RESTART';
      if (failureProbability > 0.7) {
        recommendedAction = 'PREEMPTIVE_RESTART';
      } else if (failureProbability > 0.4) {
        recommendedAction = 'WATCH';
      } else {
        recommendedAction = 'CONTINUE';
      }

      // Log prediction
      await this.pool.query(
        `INSERT INTO worker_health_logs (
          worker_id,
          metric_type,
          metric_value,
          metadata,
          logged_at
        ) VALUES ($1, $2, $3, $4, NOW())`,
        [
          workerId,
          'failure_prediction',
          failureProbability,
          JSON.stringify({
            estimatedTimeToFailure,
            recommendedAction,
            currentScore,
            degradationRate
          })
        ]
      );

      return {
        failureProbability,
        estimatedTimeToFailure,
        recommendedAction
      };
    } catch (error) {
      console.error('Failure prediction error:', error);
      return {
        failureProbability: 0.5,
        estimatedTimeToFailure: 3600000,
        recommendedAction: 'WATCH'
      };
    }
  }

  /**
   * Detect anomalies in worker metrics
   */
  async detectAnomalies(workerId: string): Promise<Anomaly[]> {
    try {
      const metricsResult = await this.pool.query(
        `SELECT metric_type, metric_value, logged_at
         FROM worker_health_logs
         WHERE worker_id = $1
         ORDER BY logged_at DESC
         LIMIT 100`,
        [workerId]
      );

      const anomalies: Anomaly[] = [];

      // Group metrics by type
      const metricsByType = new Map<string, number[]>();
      for (const row of metricsResult.rows) {
        const metricType = row.metric_type;
        const metricValue = parseFloat(row.metric_value);

        if (!metricsByType.has(metricType)) {
          metricsByType.set(metricType, []);
        }
        metricsByType.get(metricType)!.push(metricValue);
      }

      // Detect anomalies for each metric type
      for (const [metricType, values] of metricsByType.entries()) {
        const { mean, stdDev } = this.calculateStats(values);
        const latestValue = values[0];

        // Calculate z-score
        const zScore = stdDev > 0 ? Math.abs((latestValue - mean) / stdDev) : 0;

        if (zScore > 2.0) {
          // Anomaly detected (> 2 standard deviations)
          const severity = Math.min(5, Math.floor(zScore));

          anomalies.push({
            metricType,
            severity,
            anomalyScore: zScore,
            timestamp: new Date()
          });
        }
      }

      return anomalies;
    } catch (error) {
      console.error('Anomaly detection error:', error);
      return [];
    }
  }

  /**
   * Get optimal worker for job assignment
   */
  async getOptimalWorker(criteria: WorkerCriteria): Promise<string | null> {
    try {
      const minHealthScore = criteria.minHealthScore !== undefined ? criteria.minHealthScore : 0.7;
      const maxLoad = criteria.maxLoad !== undefined ? criteria.maxLoad : 0.8;

      const workerResult = await this.pool.query(
        `SELECT worker_id, health_score, current_load, capacity
         FROM workers
         WHERE status = 'ACTIVE'
           AND health_score >= $1
           AND (current_load::float / capacity::float) <= $2
         ORDER BY health_score DESC, (current_load::float / capacity::float) ASC
         LIMIT 1`,
        [minHealthScore, maxLoad]
      );

      if (workerResult.rows.length > 0) {
        return workerResult.rows[0].worker_id;
      }

      return null;
    } catch (error) {
      console.error('Optimal worker selection error:', error);
      return null;
    }
  }

  /**
   * Evacuate worker (drain jobs and prepare for shutdown)
   */
  async evacuateWorker(workerId: string, options: EvacuationOptions): Promise<void> {
    try {
      // Mark worker as DRAINING
      await this.pool.query(
        `UPDATE workers SET
          status = 'DRAINING',
          metadata = metadata || $1,
          updated_at = NOW()
         WHERE worker_id = $2`,
        [JSON.stringify({ evacuationReason: options.reason }), workerId]
      );

      if (options.reassignJobs) {
        // Get jobs assigned to this worker
        const jobsResult = await this.pool.query(
          `SELECT job_id FROM jobs
           WHERE worker_id = $1 AND status = 'PROCESSING'`,
          [workerId]
        );

        // Reset jobs to PENDING for reassignment
        await this.pool.query(
          `UPDATE jobs SET
            status = 'PENDING',
            worker_id = NULL,
            updated_at = NOW()
           WHERE worker_id = $1 AND status = 'PROCESSING'`,
          [workerId]
        );

        // Re-queue jobs in Redis
        for (const row of jobsResult.rows) {
          const jobId = row.job_id;

          // Get job priority
          const jobResult = await this.pool.query(
            'SELECT priority FROM jobs WHERE job_id = $1',
            [jobId]
          );

          const priority = jobResult.rows[0]?.priority || 3;
          const queueKey = this.getQueueKey(priority);

          await this.redis.lpush(queueKey, jobId);
        }
      }
    } catch (error) {
      console.error('Worker evacuation error:', error);
      throw new Error(`Failed to evacuate worker: ${error.message}`);
    }
  }

  /**
   * Calculate degradation rate from health scores
   * Returns negative value if health is degrading (newer scores < older scores)
   */
  private calculateDegradationRate(scores: number[]): number {
    if (scores.length < 2) return 0;

    let totalChange = 0;
    // Calculate change from newest to oldest (scores[0] is newest)
    // Negative change means degradation
    for (let i = 0; i < scores.length - 1; i++) {
      totalChange += scores[i] - scores[i + 1];
    }

    const avgChange = totalChange / (scores.length - 1);

    // Return negative for degradation, positive for improvement
    // Since scores[0] is newest, positive avgChange means health improving
    // We want degradation to be positive for probability calculation
    return -avgChange;
  }

  /**
   * Estimate time to failure based on current score and degradation rate
   */
  private estimateTimeToFailure(currentScore: number, degradationRate: number): number {
    if (degradationRate <= 0) return Infinity;

    // Assume failure threshold is 0.3
    const failureThreshold = 0.3;
    const pointsToFailure = currentScore - failureThreshold;

    if (pointsToFailure <= 0) return 0;

    // Estimate time in milliseconds (assuming health score updates every 30 seconds)
    const updateIntervalMs = 30000;
    const updatesUntilFailure = pointsToFailure / degradationRate;

    return updatesUntilFailure * updateIntervalMs;
  }

  /**
   * Calculate mean and standard deviation
   */
  private calculateStats(values: number[]): { mean: number; stdDev: number } {
    if (values.length === 0) {
      return { mean: 0, stdDev: 0 };
    }

    const mean = values.reduce((sum, val) => sum + val, 0) / values.length;

    const variance =
      values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;

    const stdDev = Math.sqrt(variance);

    return { mean, stdDev };
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
