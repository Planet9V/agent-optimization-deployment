/**
 * GAP-003 Query Control System - Performance Profiler
 *
 * File: lib/query-control/profiling/performance-profiler.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: Detailed performance profiling for query control operations
 *
 * Constitutional Compliance:
 * - DILIGENCE: Comprehensive latency tracking and analysis
 * - INTEGRITY: Accurate performance measurement
 * - NO DEVELOPMENT THEATER: Real profiling, not fake metrics
 *
 * Integration: Complements TelemetryService with detailed performance analysis
 */

/**
 * Performance statistics for an operation
 */
export interface PerformanceStatistics {
  operation: string;
  sampleCount: number;
  min: number;
  max: number;
  avg: number;
  median: number;
  p50: number;
  p75: number;
  p90: number;
  p95: number;
  p99: number;
  stdDev: number;
}

/**
 * Performance target for an operation
 */
export interface PerformanceTarget {
  operation: string;
  targetMs: number;
  criticalMs: number; // Performance is unacceptable beyond this
}

/**
 * Performance alert
 */
export interface PerformanceAlert {
  operation: string;
  latencyMs: number;
  targetMs: number;
  severity: 'warning' | 'critical';
  timestamp: number;
  message: string;
}

/**
 * PerformanceProfiler - Detailed latency tracking and analysis
 *
 * Purpose:
 * - Track operation latency with percentile analysis
 * - Identify performance regressions
 * - Monitor against performance targets
 * - Generate performance alerts
 *
 * Integration Points:
 * - QueryControlService: Records latency for all operations
 * - TelemetryService: Provides detailed performance metrics
 * - NeuralHooks: Feeds performance data to neural training
 */
export class PerformanceProfiler {
  private latencies: Map<string, number[]> = new Map();
  private targets: Map<string, PerformanceTarget> = new Map();
  private alerts: PerformanceAlert[] = [];
  private readonly maxSamples = 1000; // Limit memory usage per operation

  constructor() {
    // Initialize performance targets based on GAP-003 requirements
    this.setTarget('pause', 150, 300);
    this.setTarget('resume', 150, 300);
    this.setTarget('changeModel', 200, 400);
    this.setTarget('changePermissions', 50, 100);
    this.setTarget('executeCommand', 1000, 2000);
    this.setTarget('terminate', 100, 200);
    this.setTarget('full_workflow', 500, 1000);
  }

  /**
   * Set performance target for an operation
   *
   * @param operation - Operation name
   * @param targetMs - Target latency in milliseconds
   * @param criticalMs - Critical latency threshold
   */
  setTarget(operation: string, targetMs: number, criticalMs: number): void {
    this.targets.set(operation, {
      operation,
      targetMs,
      criticalMs
    });
  }

  /**
   * Record latency for an operation
   *
   * @param operation - Operation name
   * @param latencyMs - Operation latency in milliseconds
   */
  recordLatency(operation: string, latencyMs: number): void {
    // Initialize latency array if needed
    if (!this.latencies.has(operation)) {
      this.latencies.set(operation, []);
    }

    const latencyArray = this.latencies.get(operation)!;
    latencyArray.push(latencyMs);

    // Limit memory usage
    if (latencyArray.length > this.maxSamples) {
      latencyArray.shift();
    }

    // Check against targets
    const target = this.targets.get(operation);
    if (target) {
      if (latencyMs > target.criticalMs) {
        this.addAlert({
          operation,
          latencyMs,
          targetMs: target.targetMs,
          severity: 'critical',
          timestamp: Date.now(),
          message: `${operation} exceeded critical threshold: ${latencyMs}ms (target: ${target.targetMs}ms, critical: ${target.criticalMs}ms)`
        });
      } else if (latencyMs > target.targetMs) {
        this.addAlert({
          operation,
          latencyMs,
          targetMs: target.targetMs,
          severity: 'warning',
          timestamp: Date.now(),
          message: `${operation} exceeded target: ${latencyMs}ms (target: ${target.targetMs}ms)`
        });
      }
    }

    console.log(`[Profiler] ${operation}: ${latencyMs}ms`);
  }

  /**
   * Add performance alert
   *
   * @param alert - Performance alert
   */
  private addAlert(alert: PerformanceAlert): void {
    this.alerts.push(alert);

    // Limit alert history
    if (this.alerts.length > 100) {
      this.alerts = this.alerts.slice(-100);
    }

    // Log critical alerts immediately
    if (alert.severity === 'critical') {
      console.error(`[Profiler] CRITICAL: ${alert.message}`);
    } else {
      console.warn(`[Profiler] WARNING: ${alert.message}`);
    }
  }

  /**
   * Get performance statistics for an operation
   *
   * @param operation - Operation name
   * @returns Performance statistics or null if no data
   */
  getStatistics(operation: string): PerformanceStatistics | null {
    const latencies = this.latencies.get(operation);
    if (!latencies || latencies.length === 0) {
      return null;
    }

    const sorted = [...latencies].sort((a, b) => a - b);
    const n = sorted.length;

    // Calculate average
    const avg = sorted.reduce((sum, val) => sum + val, 0) / n;

    // Calculate standard deviation
    const variance = sorted.reduce((sum, val) => sum + Math.pow(val - avg, 2), 0) / n;
    const stdDev = Math.sqrt(variance);

    return {
      operation,
      sampleCount: n,
      min: sorted[0],
      max: sorted[n - 1],
      avg,
      median: sorted[Math.floor(n * 0.5)],
      p50: sorted[Math.floor(n * 0.5)],
      p75: sorted[Math.floor(n * 0.75)],
      p90: sorted[Math.floor(n * 0.90)],
      p95: sorted[Math.floor(n * 0.95)],
      p99: sorted[Math.floor(n * 0.99)],
      stdDev
    };
  }

  /**
   * Get all performance statistics
   *
   * @returns Map of operation to statistics
   */
  getAllStatistics(): Map<string, PerformanceStatistics> {
    const stats = new Map<string, PerformanceStatistics>();

    for (const operation of this.latencies.keys()) {
      const stat = this.getStatistics(operation);
      if (stat) {
        stats.set(operation, stat);
      }
    }

    return stats;
  }

  /**
   * Get recent performance alerts
   *
   * @param severity - Optional severity filter
   * @param limit - Maximum number of alerts to return
   * @returns Recent performance alerts
   */
  getAlerts(severity?: 'warning' | 'critical', limit: number = 20): PerformanceAlert[] {
    let filtered = severity
      ? this.alerts.filter(a => a.severity === severity)
      : this.alerts;

    return filtered.slice(-limit);
  }

  /**
   * Clear all performance data
   */
  clear(): void {
    this.latencies.clear();
    this.alerts = [];
    console.log('[Profiler] Performance data cleared');
  }

  /**
   * Get performance report
   *
   * @returns Human-readable performance report
   */
  getReport(): string {
    let report = '=== Performance Profiler Report ===\n\n';

    const stats = this.getAllStatistics();
    for (const [operation, stat] of stats.entries()) {
      const target = this.targets.get(operation);
      const targetInfo = target
        ? ` (target: ${target.targetMs}ms, critical: ${target.criticalMs}ms)`
        : '';

      report += `${operation}${targetInfo}:\n`;
      report += `  Samples: ${stat.sampleCount}\n`;
      report += `  Min: ${stat.min.toFixed(2)}ms\n`;
      report += `  Avg: ${stat.avg.toFixed(2)}ms\n`;
      report += `  p50: ${stat.p50.toFixed(2)}ms\n`;
      report += `  p95: ${stat.p95.toFixed(2)}ms\n`;
      report += `  p99: ${stat.p99.toFixed(2)}ms\n`;
      report += `  Max: ${stat.max.toFixed(2)}ms\n`;
      report += `  StdDev: ${stat.stdDev.toFixed(2)}ms\n`;

      // Performance vs target
      if (target) {
        const avgVsTarget = ((stat.avg / target.targetMs) * 100).toFixed(1);
        const performance = stat.avg <= target.targetMs ? '✅ PASS' : '❌ FAIL';
        report += `  Performance: ${performance} (${avgVsTarget}% of target)\n`;
      }

      report += '\n';
    }

    // Recent alerts
    const recentAlerts = this.getAlerts(undefined, 5);
    if (recentAlerts.length > 0) {
      report += '=== Recent Alerts ===\n\n';
      for (const alert of recentAlerts) {
        const icon = alert.severity === 'critical' ? '🚨' : '⚠️';
        report += `${icon} ${alert.message}\n`;
      }
      report += '\n';
    }

    return report;
  }

  /**
   * Check if operation performance is acceptable
   *
   * @param operation - Operation name
   * @returns True if performance meets target
   */
  meetsTarget(operation: string): boolean {
    const stats = this.getStatistics(operation);
    const target = this.targets.get(operation);

    if (!stats || !target) {
      return true; // No data or no target = assume OK
    }

    return stats.avg <= target.targetMs;
  }

  /**
   * Get performance grade
   *
   * @param operation - Operation name
   * @returns Performance grade (A-F)
   */
  getGrade(operation: string): string {
    const stats = this.getStatistics(operation);
    const target = this.targets.get(operation);

    if (!stats || !target) {
      return 'N/A';
    }

    const ratio = stats.avg / target.targetMs;

    if (ratio <= 0.5) return 'A+'; // 50% better than target
    if (ratio <= 0.75) return 'A';  // 25% better than target
    if (ratio <= 1.0) return 'B';   // Meets target
    if (ratio <= 1.25) return 'C';  // 25% worse than target
    if (ratio <= 1.5) return 'D';   // 50% worse than target
    return 'F'; // More than 50% worse than target
  }
}

/**
 * Singleton performance profiler instance
 */
let profilerInstance: PerformanceProfiler | null = null;

/**
 * Get or create performance profiler singleton
 *
 * @returns PerformanceProfiler instance
 */
export function getPerformanceProfiler(): PerformanceProfiler {
  if (!profilerInstance) {
    profilerInstance = new PerformanceProfiler();
  }
  return profilerInstance;
}
