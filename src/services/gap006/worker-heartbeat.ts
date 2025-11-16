/**
 * Worker Heartbeat Monitoring - GAP-006
 * Monitors worker health and triggers replacement for failing workers
 */

import WorkerService, { WorkerHealth } from './worker-service';

export interface HeartbeatConfig {
  intervalMs: number;
  timeoutMs: number;
  failureThreshold: number;
}

export class WorkerHeartbeatMonitor {
  private workerService: WorkerService;
  private config: HeartbeatConfig;
  private monitoringInterval: NodeJS.Timeout | null = null;
  private workerHealthCache: Map<string, WorkerHealth> = new Map();

  constructor(
    workerService: WorkerService,
    config?: Partial<HeartbeatConfig>
  ) {
    this.workerService = workerService;
    this.config = {
      intervalMs: config?.intervalMs || 30000, // 30 seconds
      timeoutMs: config?.timeoutMs || 60000, // 60 seconds
      failureThreshold: config?.failureThreshold || 0.7, // 70% confidence
    };
  }

  /**
   * Start monitoring worker heartbeats
   */
  start(): void {
    if (this.monitoringInterval) {
      console.warn('Heartbeat monitoring already running');
      return;
    }

    console.log('Starting worker heartbeat monitoring...');

    this.monitoringInterval = setInterval(
      async () => {
        await this.checkAllWorkers();
      },
      this.config.intervalMs
    );
  }

  /**
   * Stop monitoring worker heartbeats
   */
  stop(): void {
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
      this.monitoringInterval = null;
      console.log('Stopped worker heartbeat monitoring');
    }
  }

  /**
   * Update heartbeat for a specific worker
   */
  async updateWorkerHeartbeat(
    workerId: string,
    health: WorkerHealth
  ): Promise<void> {
    try {
      // Update in database
      await this.workerService.updateHeartbeat(workerId, health);

      // Update cache
      this.workerHealthCache.set(workerId, {
        ...health,
        lastHeartbeat: new Date(),
      });

      // Check if worker is degrading
      if (health.errorRate > 0.1 || health.status === 'DEGRADED') {
        await this.checkWorkerPrediction(workerId);
      }
    } catch (error) {
      console.error(`Failed to update heartbeat for worker ${workerId}:`, error);
    }
  }

  /**
   * Check all workers for stale heartbeats and predict failures
   */
  private async checkAllWorkers(): Promise<void> {
    try {
      // Get workers with stale heartbeats
      const staleWorkers = await this.workerService.checkStaleWorkers();

      if (staleWorkers.length > 0) {
        console.warn(`Found ${staleWorkers.length} workers with stale heartbeats`);
      }

      // Check each stale worker
      for (const workerId of staleWorkers) {
        await this.handleStaleWorker(workerId);
      }

      // Check predictions for active workers
      const activeWorkers = await this.workerService.getActiveWorkers();

      for (const worker of activeWorkers) {
        if (worker.status === 'DEGRADED' || worker.status === 'BUSY') {
          await this.checkWorkerPrediction(worker.workerId);
        }
      }
    } catch (error) {
      console.error('Error checking workers:', error);
    }
  }

  /**
   * Handle a worker with a stale heartbeat
   */
  private async handleStaleWorker(workerId: string): Promise<void> {
    try {
      console.log(`Handling stale worker: ${workerId}`);

      // Get worker details
      const workers = await this.workerService.getActiveWorkers();
      const worker = workers.find(w => w.workerId === workerId);

      if (!worker) {
        console.warn(`Worker ${workerId} not found`);
        return;
      }

      // Replace the worker
      console.log(`Replacing stale worker ${workerId} (${worker.workerName})`);

      const newWorkerId = await this.workerService.replaceWorker(workerId, {
        workerName: `${worker.workerName}-replacement-${Date.now()}`,
        workerType: worker.workerType,
        capabilities: worker.capabilities,
      });

      console.log(`Replaced worker ${workerId} with ${newWorkerId}`);

      // Remove from cache
      this.workerHealthCache.delete(workerId);
    } catch (error) {
      console.error(`Failed to handle stale worker ${workerId}:`, error);
    }
  }

  /**
   * Check worker failure prediction
   */
  private async checkWorkerPrediction(workerId: string): Promise<void> {
    try {
      const prediction = await this.workerService.predictWorkerFailure(workerId);

      console.log(
        `Worker ${workerId} prediction: ${prediction.prediction} ` +
        `(confidence: ${(prediction.confidence * 100).toFixed(1)}%) - ` +
        `Action: ${prediction.recommendedAction}`
      );

      // Handle based on recommendation
      if (prediction.recommendedAction === 'REPLACE') {
        console.log(`Replacing failing worker: ${workerId}`);

        const workers = await this.workerService.getActiveWorkers();
        const worker = workers.find(w => w.workerId === workerId);

        if (worker) {
          const newWorkerId = await this.workerService.replaceWorker(workerId, {
            workerName: `${worker.workerName}-replacement-${Date.now()}`,
            workerType: worker.workerType,
            capabilities: worker.capabilities,
          });

          console.log(`Replaced failing worker ${workerId} with ${newWorkerId}`);
          this.workerHealthCache.delete(workerId);
        }
      } else if (prediction.recommendedAction === 'MONITOR') {
        console.log(`Monitoring degraded worker: ${workerId}`);
      }
    } catch (error) {
      console.error(`Failed to check prediction for worker ${workerId}:`, error);
    }
  }

  /**
   * Get current health cache
   */
  getHealthCache(): Map<string, WorkerHealth> {
    return new Map(this.workerHealthCache);
  }

  /**
   * Get monitoring statistics
   */
  getStats(): {
    monitoredWorkers: number;
    isRunning: boolean;
    intervalMs: number;
  } {
    return {
      monitoredWorkers: this.workerHealthCache.size,
      isRunning: this.monitoringInterval !== null,
      intervalMs: this.config.intervalMs,
    };
  }
}

export default WorkerHeartbeatMonitor;
