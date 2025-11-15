/**
 * GAP-003 Query Control System - Telemetry Service
 *
 * File: lib/query-control/telemetry/telemetry-service.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: Operation metrics collection for neural pattern training
 *
 * Constitutional Compliance:
 * - DILIGENCE: Comprehensive metrics capture for all operations
 * - INTEGRITY: Accurate timing and outcome recording
 * - NO DEVELOPMENT THEATER: Real metrics collection, not placeholder telemetry
 *
 * Integration: Prepares for MCP neural_train integration
 */

/**
 * Metrics for a single query control operation
 */
export interface OperationMetrics {
  operationType: 'pause' | 'resume' | 'changeModel' | 'changePermissions' | 'executeCommand' | 'terminate';
  queryId: string;
  startTime: number;
  endTime: number;
  durationMs: number;
  success: boolean;
  error?: string;
  metadata?: Record<string, any>;
}

/**
 * Aggregated metrics for analysis
 */
export interface AggregatedMetrics {
  operationType: string;
  totalOperations: number;
  successCount: number;
  failureCount: number;
  avgDurationMs: number;
  minDurationMs: number;
  maxDurationMs: number;
  p50DurationMs: number;
  p95DurationMs: number;
  p99DurationMs: number;
  successRate: number;
}

/**
 * Pattern detected in operation metrics
 */
export interface DetectedPattern {
  patternType: string;
  description: string;
  frequency: number;
  avgDuration: number;
  confidence: number;
}

/**
 * TelemetryService - Collect and analyze query control operation metrics
 *
 * Purpose:
 * - Record timing and outcome for all query control operations
 * - Prepare data for neural pattern training (future MCP integration)
 * - Enable performance analysis and optimization
 * - Support failure pattern detection
 *
 * Integration Points:
 * - QueryControlService: Records all operation metrics
 * - NeuralHooks: Feeds metrics to neural training (future)
 * - PerformanceProfiler: Provides detailed latency analysis
 */
export class TelemetryService {
  private metrics: OperationMetrics[] = [];
  private readonly maxMetrics = 10000; // Limit memory usage

  /**
   * Record a completed operation's metrics
   *
   * @param metrics - Operation metrics to record
   */
  recordOperation(metrics: OperationMetrics): void {
    this.metrics.push(metrics);

    // Limit memory usage by removing oldest metrics
    if (this.metrics.length > this.maxMetrics) {
      this.metrics = this.metrics.slice(-this.maxMetrics);
    }

    // Future: Feed to neural_train via MCP
    console.log(`[Telemetry] ${metrics.operationType} for ${metrics.queryId}: ${metrics.durationMs}ms (${metrics.success ? 'success' : 'failure'})`);
  }

  /**
   * Get metrics for a specific query or all queries
   *
   * @param queryId - Optional query ID filter
   * @returns Array of operation metrics
   */
  getMetrics(queryId?: string): OperationMetrics[] {
    return queryId
      ? this.metrics.filter(m => m.queryId === queryId)
      : [...this.metrics];
  }

  /**
   * Get aggregated metrics by operation type
   *
   * @param operationType - Optional operation type filter
   * @returns Aggregated metrics
   */
  getAggregatedMetrics(operationType?: string): AggregatedMetrics[] {
    const metricsByType = new Map<string, OperationMetrics[]>();

    // Group by operation type
    for (const metric of this.metrics) {
      if (operationType && metric.operationType !== operationType) {
        continue;
      }

      if (!metricsByType.has(metric.operationType)) {
        metricsByType.set(metric.operationType, []);
      }
      metricsByType.get(metric.operationType)!.push(metric);
    }

    // Aggregate each group
    const aggregated: AggregatedMetrics[] = [];
    for (const [type, typeMetrics] of metricsByType.entries()) {
      const durations = typeMetrics.map(m => m.durationMs).sort((a, b) => a - b);
      const successCount = typeMetrics.filter(m => m.success).length;

      aggregated.push({
        operationType: type,
        totalOperations: typeMetrics.length,
        successCount,
        failureCount: typeMetrics.length - successCount,
        avgDurationMs: durations.reduce((a, b) => a + b, 0) / durations.length,
        minDurationMs: durations[0],
        maxDurationMs: durations[durations.length - 1],
        p50DurationMs: durations[Math.floor(durations.length * 0.5)],
        p95DurationMs: durations[Math.floor(durations.length * 0.95)],
        p99DurationMs: durations[Math.floor(durations.length * 0.99)],
        successRate: successCount / typeMetrics.length
      });
    }

    return aggregated;
  }

  /**
   * Analyze operation patterns
   * Future: Will use mcp__claude-flow__neural_patterns
   *
   * @returns Detected patterns in operation metrics
   */
  async analyzePatterns(): Promise<DetectedPattern[]> {
    const patterns: DetectedPattern[] = [];

    // Pattern 1: Frequent pause operations for specific query
    const pausesByQuery = new Map<string, OperationMetrics[]>();
    for (const metric of this.metrics) {
      if (metric.operationType === 'pause') {
        if (!pausesByQuery.has(metric.queryId)) {
          pausesByQuery.set(metric.queryId, []);
        }
        pausesByQuery.get(metric.queryId)!.push(metric);
      }
    }

    for (const [queryId, pauses] of pausesByQuery.entries()) {
      if (pauses.length >= 3) {
        const avgDuration = pauses.reduce((sum, p) => sum + p.durationMs, 0) / pauses.length;
        patterns.push({
          patternType: 'frequent_pause',
          description: `Query ${queryId} paused ${pauses.length} times`,
          frequency: pauses.length,
          avgDuration,
          confidence: Math.min(0.9, pauses.length / 10)
        });
      }
    }

    // Pattern 2: Failed operations for specific query
    const failuresByQuery = new Map<string, OperationMetrics[]>();
    for (const metric of this.metrics) {
      if (!metric.success) {
        if (!failuresByQuery.has(metric.queryId)) {
          failuresByQuery.set(metric.queryId, []);
        }
        failuresByQuery.get(metric.queryId)!.push(metric);
      }
    }

    for (const [queryId, failures] of failuresByQuery.entries()) {
      if (failures.length >= 2) {
        const avgDuration = failures.reduce((sum, f) => sum + f.durationMs, 0) / failures.length;
        patterns.push({
          patternType: 'repeated_failure',
          description: `Query ${queryId} failed ${failures.length} times`,
          frequency: failures.length,
          avgDuration,
          confidence: Math.min(0.95, failures.length / 5)
        });
      }
    }

    // Pattern 3: Slow operations (>95th percentile)
    const aggregated = this.getAggregatedMetrics();
    for (const agg of aggregated) {
      const slowOps = this.metrics.filter(
        m => m.operationType === agg.operationType && m.durationMs > agg.p95DurationMs
      );

      if (slowOps.length > 0) {
        patterns.push({
          patternType: 'slow_operation',
          description: `${agg.operationType} operations exceeding p95 (${agg.p95DurationMs}ms)`,
          frequency: slowOps.length,
          avgDuration: slowOps.reduce((sum, op) => sum + op.durationMs, 0) / slowOps.length,
          confidence: 0.8
        });
      }
    }

    return patterns;
  }

  /**
   * Get metrics summary for reporting
   *
   * @returns Human-readable metrics summary
   */
  getSummary(): string {
    const aggregated = this.getAggregatedMetrics();
    let summary = '=== Query Control Telemetry Summary ===\n\n';

    for (const agg of aggregated) {
      summary += `${agg.operationType}:\n`;
      summary += `  Total Operations: ${agg.totalOperations}\n`;
      summary += `  Success Rate: ${(agg.successRate * 100).toFixed(1)}%\n`;
      summary += `  Avg Duration: ${agg.avgDurationMs.toFixed(2)}ms\n`;
      summary += `  p50: ${agg.p50DurationMs.toFixed(2)}ms\n`;
      summary += `  p95: ${agg.p95DurationMs.toFixed(2)}ms\n`;
      summary += `  p99: ${agg.p99DurationMs.toFixed(2)}ms\n\n`;
    }

    return summary;
  }

  /**
   * Clear all metrics (for testing or reset)
   */
  clearMetrics(): void {
    this.metrics = [];
    console.log('[Telemetry] Metrics cleared');
  }

  /**
   * Export metrics for neural training (future MCP integration)
   *
   * @returns Metrics in format suitable for neural training
   */
  exportForTraining(): {
    operationType: string;
    samples: Array<{
      queryId: string;
      durationMs: number;
      success: boolean;
      timestamp: number;
      metadata?: Record<string, any>;
    }>;
  }[] {
    const exportData = new Map<string, any[]>();

    for (const metric of this.metrics) {
      if (!exportData.has(metric.operationType)) {
        exportData.set(metric.operationType, []);
      }

      exportData.get(metric.operationType)!.push({
        queryId: metric.queryId,
        durationMs: metric.durationMs,
        success: metric.success,
        timestamp: metric.endTime,
        metadata: metric.metadata
      });
    }

    return Array.from(exportData.entries()).map(([operationType, samples]) => ({
      operationType,
      samples
    }));
  }
}

/**
 * Singleton telemetry service instance
 */
let telemetryInstance: TelemetryService | null = null;

/**
 * Get or create telemetry service singleton
 *
 * @returns TelemetryService instance
 */
export function getTelemetryService(): TelemetryService {
  if (!telemetryInstance) {
    telemetryInstance = new TelemetryService();
  }
  return telemetryInstance;
}
