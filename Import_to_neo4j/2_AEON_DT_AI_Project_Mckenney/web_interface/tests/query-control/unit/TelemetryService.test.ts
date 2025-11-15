/**
 * GAP-003 Query Control System - Telemetry Service Unit Tests
 *
 * File: tests/query-control/unit/TelemetryService.test.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: Comprehensive unit tests for TelemetryService
 *
 * Constitutional Compliance:
 * - DILIGENCE: >90% code coverage, >85% branch coverage
 * - INTEGRITY: All operation types and metrics tested
 * - NO DEVELOPMENT THEATER: Production-grade tests
 */

import { describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import {
  TelemetryService,
  getTelemetryService,
  type OperationMetrics,
  type AggregatedMetrics,
  type DetectedPattern
} from '../../../lib/query-control/telemetry/telemetry-service';

describe('TelemetryService', () => {
  let telemetry: TelemetryService;

  beforeEach(() => {
    telemetry = new TelemetryService();
  });

  afterEach(() => {
    telemetry.clearMetrics();
  });

  describe('recordOperation', () => {
    test('should record pause operation', () => {
      const metric: OperationMetrics = {
        operationType: 'pause',
        queryId: 'query-001',
        startTime: Date.now() - 100,
        endTime: Date.now(),
        durationMs: 100,
        success: true
      };

      telemetry.recordOperation(metric);
      const metrics = telemetry.getMetrics();

      expect(metrics).toHaveLength(1);
      expect(metrics[0].operationType).toBe('pause');
      expect(metrics[0].queryId).toBe('query-001');
      expect(metrics[0].success).toBe(true);
    });

    test('should record resume operation', () => {
      const metric: OperationMetrics = {
        operationType: 'resume',
        queryId: 'query-002',
        startTime: Date.now() - 50,
        endTime: Date.now(),
        durationMs: 50,
        success: true
      };

      telemetry.recordOperation(metric);
      const metrics = telemetry.getMetrics();

      expect(metrics).toHaveLength(1);
      expect(metrics[0].operationType).toBe('resume');
    });

    test('should record changeModel operation', () => {
      const metric: OperationMetrics = {
        operationType: 'changeModel',
        queryId: 'query-003',
        startTime: Date.now() - 200,
        endTime: Date.now(),
        durationMs: 200,
        success: true,
        metadata: {
          fromModel: 'sonnet',
          toModel: 'haiku'
        }
      };

      telemetry.recordOperation(metric);
      const metrics = telemetry.getMetrics();

      expect(metrics).toHaveLength(1);
      expect(metrics[0].operationType).toBe('changeModel');
      expect(metrics[0].metadata?.fromModel).toBe('sonnet');
      expect(metrics[0].metadata?.toModel).toBe('haiku');
    });

    test('should record changePermissions operation', () => {
      const metric: OperationMetrics = {
        operationType: 'changePermissions',
        queryId: 'query-004',
        startTime: Date.now() - 75,
        endTime: Date.now(),
        durationMs: 75,
        success: true,
        metadata: {
          fromMode: 'default',
          toMode: 'acceptEdits'
        }
      };

      telemetry.recordOperation(metric);
      const metrics = telemetry.getMetrics();

      expect(metrics).toHaveLength(1);
      expect(metrics[0].operationType).toBe('changePermissions');
      expect(metrics[0].metadata?.toMode).toBe('acceptEdits');
    });

    test('should record executeCommand operation', () => {
      const metric: OperationMetrics = {
        operationType: 'executeCommand',
        queryId: 'query-005',
        startTime: Date.now() - 300,
        endTime: Date.now(),
        durationMs: 300,
        success: true,
        metadata: {
          command: 'npm test',
          exitCode: 0
        }
      };

      telemetry.recordOperation(metric);
      const metrics = telemetry.getMetrics();

      expect(metrics).toHaveLength(1);
      expect(metrics[0].operationType).toBe('executeCommand');
      expect(metrics[0].metadata?.command).toBe('npm test');
    });

    test('should record terminate operation', () => {
      const metric: OperationMetrics = {
        operationType: 'terminate',
        queryId: 'query-006',
        startTime: Date.now() - 150,
        endTime: Date.now(),
        durationMs: 150,
        success: true
      };

      telemetry.recordOperation(metric);
      const metrics = telemetry.getMetrics();

      expect(metrics).toHaveLength(1);
      expect(metrics[0].operationType).toBe('terminate');
    });

    test('should record failed operations with error', () => {
      const metric: OperationMetrics = {
        operationType: 'pause',
        queryId: 'query-007',
        startTime: Date.now() - 100,
        endTime: Date.now(),
        durationMs: 100,
        success: false,
        error: 'Query not found'
      };

      telemetry.recordOperation(metric);
      const metrics = telemetry.getMetrics();

      expect(metrics).toHaveLength(1);
      expect(metrics[0].success).toBe(false);
      expect(metrics[0].error).toBe('Query not found');
    });

    test('should record multiple operations', () => {
      const metrics: OperationMetrics[] = [
        {
          operationType: 'pause',
          queryId: 'query-008',
          startTime: Date.now() - 100,
          endTime: Date.now(),
          durationMs: 100,
          success: true
        },
        {
          operationType: 'resume',
          queryId: 'query-008',
          startTime: Date.now() - 50,
          endTime: Date.now(),
          durationMs: 50,
          success: true
        },
        {
          operationType: 'terminate',
          queryId: 'query-008',
          startTime: Date.now() - 75,
          endTime: Date.now(),
          durationMs: 75,
          success: true
        }
      ];

      metrics.forEach(m => telemetry.recordOperation(m));
      const recorded = telemetry.getMetrics();

      expect(recorded).toHaveLength(3);
    });

    test('should enforce maxMetrics limit of 10,000', () => {
      // Record 10,001 metrics
      for (let i = 0; i < 10001; i++) {
        telemetry.recordOperation({
          operationType: 'pause',
          queryId: `query-${i}`,
          startTime: Date.now() - 100,
          endTime: Date.now(),
          durationMs: 100,
          success: true
        });
      }

      const metrics = telemetry.getMetrics();
      expect(metrics).toHaveLength(10000);
      // Should have removed oldest (first) metric
      expect(metrics[0].queryId).toBe('query-1');
    });
  });

  describe('getMetrics', () => {
    beforeEach(() => {
      // Record test metrics
      const testMetrics: OperationMetrics[] = [
        {
          operationType: 'pause',
          queryId: 'query-001',
          startTime: Date.now() - 100,
          endTime: Date.now(),
          durationMs: 100,
          success: true
        },
        {
          operationType: 'resume',
          queryId: 'query-001',
          startTime: Date.now() - 50,
          endTime: Date.now(),
          durationMs: 50,
          success: true
        },
        {
          operationType: 'pause',
          queryId: 'query-002',
          startTime: Date.now() - 75,
          endTime: Date.now(),
          durationMs: 75,
          success: false,
          error: 'Failed'
        }
      ];

      testMetrics.forEach(m => telemetry.recordOperation(m));
    });

    test('should return all metrics without filter', () => {
      const metrics = telemetry.getMetrics();
      expect(metrics).toHaveLength(3);
    });

    test('should filter metrics by queryId', () => {
      const metrics = telemetry.getMetrics('query-001');
      expect(metrics).toHaveLength(2);
      expect(metrics.every(m => m.queryId === 'query-001')).toBe(true);
    });

    test('should return empty array for non-existent queryId', () => {
      const metrics = telemetry.getMetrics('non-existent');
      expect(metrics).toHaveLength(0);
    });

    test('should return copy of metrics, not direct reference', () => {
      const metrics1 = telemetry.getMetrics();
      const metrics2 = telemetry.getMetrics();

      expect(metrics1).not.toBe(metrics2);
      expect(metrics1).toEqual(metrics2);
    });
  });

  describe('getAggregatedMetrics', () => {
    beforeEach(() => {
      // Record metrics for aggregation testing
      const testMetrics: OperationMetrics[] = [
        // Pause operations
        { operationType: 'pause', queryId: 'q1', startTime: 0, endTime: 100, durationMs: 100, success: true },
        { operationType: 'pause', queryId: 'q2', startTime: 0, endTime: 150, durationMs: 150, success: true },
        { operationType: 'pause', queryId: 'q3', startTime: 0, endTime: 200, durationMs: 200, success: false, error: 'Error' },
        { operationType: 'pause', queryId: 'q4', startTime: 0, endTime: 120, durationMs: 120, success: true },
        // Resume operations
        { operationType: 'resume', queryId: 'q1', startTime: 0, endTime: 50, durationMs: 50, success: true },
        { operationType: 'resume', queryId: 'q2', startTime: 0, endTime: 75, durationMs: 75, success: true },
        // ChangeModel operations
        { operationType: 'changeModel', queryId: 'q1', startTime: 0, endTime: 300, durationMs: 300, success: true },
        { operationType: 'changeModel', queryId: 'q2', startTime: 0, endTime: 250, durationMs: 250, success: false }
      ];

      testMetrics.forEach(m => telemetry.recordOperation(m));
    });

    test('should aggregate all operation types', () => {
      const aggregated = telemetry.getAggregatedMetrics();

      expect(aggregated).toHaveLength(3);
      expect(aggregated.some(a => a.operationType === 'pause')).toBe(true);
      expect(aggregated.some(a => a.operationType === 'resume')).toBe(true);
      expect(aggregated.some(a => a.operationType === 'changeModel')).toBe(true);
    });

    test('should filter by operation type', () => {
      const aggregated = telemetry.getAggregatedMetrics('pause');

      expect(aggregated).toHaveLength(1);
      expect(aggregated[0].operationType).toBe('pause');
    });

    test('should calculate total operations count', () => {
      const aggregated = telemetry.getAggregatedMetrics('pause');

      expect(aggregated[0].totalOperations).toBe(4);
    });

    test('should calculate success and failure counts', () => {
      const aggregated = telemetry.getAggregatedMetrics('pause');

      expect(aggregated[0].successCount).toBe(3);
      expect(aggregated[0].failureCount).toBe(1);
    });

    test('should calculate success rate correctly', () => {
      const pauseAgg = telemetry.getAggregatedMetrics('pause')[0];
      const resumeAgg = telemetry.getAggregatedMetrics('resume')[0];

      expect(pauseAgg.successRate).toBe(0.75); // 3/4
      expect(resumeAgg.successRate).toBe(1.0); // 2/2
    });

    test('should calculate duration statistics', () => {
      const aggregated = telemetry.getAggregatedMetrics('pause')[0];

      // Durations: [100, 120, 150, 200] sorted
      expect(aggregated.minDurationMs).toBe(100);
      expect(aggregated.maxDurationMs).toBe(200);
      expect(aggregated.avgDurationMs).toBe(142.5); // (100+120+150+200)/4
    });

    test('should calculate p50 percentile correctly', () => {
      const aggregated = telemetry.getAggregatedMetrics('pause')[0];

      // Sorted: [100, 120, 150, 200]
      // p50 at index floor(4 * 0.5) = 2 → 150
      expect(aggregated.p50DurationMs).toBe(150);
    });

    test('should calculate p95 percentile correctly', () => {
      const aggregated = telemetry.getAggregatedMetrics('pause')[0];

      // Sorted: [100, 120, 150, 200]
      // p95 at index floor(4 * 0.95) = 3 → 200
      expect(aggregated.p95DurationMs).toBe(200);
    });

    test('should calculate p99 percentile correctly', () => {
      const aggregated = telemetry.getAggregatedMetrics('pause')[0];

      // Sorted: [100, 120, 150, 200]
      // p99 at index floor(4 * 0.99) = 3 → 200
      expect(aggregated.p99DurationMs).toBe(200);
    });

    test('should handle single metric aggregation', () => {
      telemetry.clearMetrics();
      telemetry.recordOperation({
        operationType: 'pause',
        queryId: 'q1',
        startTime: 0,
        endTime: 100,
        durationMs: 100,
        success: true
      });

      const aggregated = telemetry.getAggregatedMetrics('pause')[0];

      expect(aggregated.totalOperations).toBe(1);
      expect(aggregated.minDurationMs).toBe(100);
      expect(aggregated.maxDurationMs).toBe(100);
      expect(aggregated.avgDurationMs).toBe(100);
      expect(aggregated.p50DurationMs).toBe(100);
    });
  });

  describe('analyzePatterns', () => {
    test('should detect frequent pause pattern', async () => {
      // Record 3+ pauses for same query
      for (let i = 0; i < 4; i++) {
        telemetry.recordOperation({
          operationType: 'pause',
          queryId: 'query-frequent-pause',
          startTime: Date.now() - 100,
          endTime: Date.now(),
          durationMs: 100 + i * 10,
          success: true
        });
      }

      const patterns = await telemetry.analyzePatterns();
      const frequentPause = patterns.find(p => p.patternType === 'frequent_pause');

      expect(frequentPause).toBeDefined();
      expect(frequentPause?.frequency).toBe(4);
      expect(frequentPause?.description).toContain('query-frequent-pause');
      expect(frequentPause?.confidence).toBeGreaterThan(0);
    });

    test('should calculate average duration for frequent pause pattern', async () => {
      const durations = [100, 110, 120, 130];
      const expectedAvg = 115; // (100+110+120+130)/4

      for (const duration of durations) {
        telemetry.recordOperation({
          operationType: 'pause',
          queryId: 'query-avg-test',
          startTime: 0,
          endTime: duration,
          durationMs: duration,
          success: true
        });
      }

      const patterns = await telemetry.analyzePatterns();
      const frequentPause = patterns.find(p => p.patternType === 'frequent_pause');

      expect(frequentPause?.avgDuration).toBe(expectedAvg);
    });

    test('should scale confidence with frequency for pause pattern', async () => {
      // Confidence = min(0.9, frequency/10)
      for (let i = 0; i < 5; i++) {
        telemetry.recordOperation({
          operationType: 'pause',
          queryId: 'query-confidence-test',
          startTime: 0,
          endTime: 100,
          durationMs: 100,
          success: true
        });
      }

      const patterns = await telemetry.analyzePatterns();
      const frequentPause = patterns.find(p => p.patternType === 'frequent_pause');

      expect(frequentPause?.confidence).toBe(0.5); // 5/10
    });

    test('should detect repeated failure pattern', async () => {
      // Record 2+ failures for same query
      for (let i = 0; i < 3; i++) {
        telemetry.recordOperation({
          operationType: 'resume',
          queryId: 'query-failures',
          startTime: Date.now() - 100,
          endTime: Date.now(),
          durationMs: 100,
          success: false,
          error: 'Failed to resume'
        });
      }

      const patterns = await telemetry.analyzePatterns();
      const repeatedFailure = patterns.find(p => p.patternType === 'repeated_failure');

      expect(repeatedFailure).toBeDefined();
      expect(repeatedFailure?.frequency).toBe(3);
      expect(repeatedFailure?.description).toContain('query-failures');
    });

    test('should calculate confidence for failure pattern', async () => {
      // Confidence = min(0.95, frequency/5)
      for (let i = 0; i < 4; i++) {
        telemetry.recordOperation({
          operationType: 'terminate',
          queryId: 'query-fail-confidence',
          startTime: 0,
          endTime: 100,
          durationMs: 100,
          success: false,
          error: 'Error'
        });
      }

      const patterns = await telemetry.analyzePatterns();
      const repeatedFailure = patterns.find(p => p.patternType === 'repeated_failure');

      expect(repeatedFailure?.confidence).toBe(0.8); // 4/5
    });

    test('should detect slow operation pattern', async () => {
      // Create operations with clear outliers above p95
      // With 21 values, p95 at index floor(21 * 0.95) = 19 (value 190)
      // Values 500 and 1000 are above p95
      const durations = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
                        110, 120, 130, 140, 150, 160, 170, 180, 190, 500, 1000];

      for (const duration of durations) {
        telemetry.recordOperation({
          operationType: 'changeModel',
          queryId: `query-${duration}`,
          startTime: 0,
          endTime: duration,
          durationMs: duration,
          success: true
        });
      }

      const patterns = await telemetry.analyzePatterns();
      const slowOp = patterns.find(p => p.patternType === 'slow_operation');

      expect(slowOp).toBeDefined();
      expect(slowOp?.description).toContain('changeModel');
      expect(slowOp?.confidence).toBe(0.8);
      expect(slowOp?.frequency).toBeGreaterThanOrEqual(1); // At least one outlier above p95
    });

    test('should not detect patterns with insufficient data', async () => {
      // Only 2 pauses (need 3+)
      telemetry.recordOperation({
        operationType: 'pause',
        queryId: 'query-insufficient',
        startTime: 0,
        endTime: 100,
        durationMs: 100,
        success: true
      });
      telemetry.recordOperation({
        operationType: 'pause',
        queryId: 'query-insufficient',
        startTime: 0,
        endTime: 100,
        durationMs: 100,
        success: true
      });

      const patterns = await telemetry.analyzePatterns();
      const frequentPause = patterns.find(
        p => p.patternType === 'frequent_pause' && p.description.includes('query-insufficient')
      );

      expect(frequentPause).toBeUndefined();
    });

    test('should detect multiple pattern types simultaneously', async () => {
      // Frequent pauses
      for (let i = 0; i < 4; i++) {
        telemetry.recordOperation({
          operationType: 'pause',
          queryId: 'query-multi-1',
          startTime: 0,
          endTime: 100,
          durationMs: 100,
          success: true
        });
      }

      // Repeated failures
      for (let i = 0; i < 3; i++) {
        telemetry.recordOperation({
          operationType: 'resume',
          queryId: 'query-multi-2',
          startTime: 0,
          endTime: 100,
          durationMs: 100,
          success: false,
          error: 'Error'
        });
      }

      // Slow operations - with 21 values, p95 at index 19, add 2 outliers above it
      const terminateDurations = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140,
                                  150, 160, 170, 180, 190, 200, 210, 220, 230, 800, 1000];
      for (let i = 0; i < terminateDurations.length; i++) {
        telemetry.recordOperation({
          operationType: 'terminate',
          queryId: `query-slow-${i}`,
          startTime: 0,
          endTime: terminateDurations[i],
          durationMs: terminateDurations[i],
          success: true
        });
      }

      const patterns = await telemetry.analyzePatterns();

      expect(patterns.length).toBeGreaterThanOrEqual(3);
      expect(patterns.some(p => p.patternType === 'frequent_pause')).toBe(true);
      expect(patterns.some(p => p.patternType === 'repeated_failure')).toBe(true);
      expect(patterns.some(p => p.patternType === 'slow_operation')).toBe(true);
    });
  });

  describe('getSummary', () => {
    beforeEach(() => {
      const testMetrics: OperationMetrics[] = [
        { operationType: 'pause', queryId: 'q1', startTime: 0, endTime: 100, durationMs: 100, success: true },
        { operationType: 'pause', queryId: 'q2', startTime: 0, endTime: 150, durationMs: 150, success: true },
        { operationType: 'resume', queryId: 'q1', startTime: 0, endTime: 50, durationMs: 50, success: true }
      ];

      testMetrics.forEach(m => telemetry.recordOperation(m));
    });

    test('should generate summary string', () => {
      const summary = telemetry.getSummary();

      expect(summary).toContain('Query Control Telemetry Summary');
      expect(summary).toContain('pause:');
      expect(summary).toContain('resume:');
    });

    test('should include total operations in summary', () => {
      const summary = telemetry.getSummary();

      expect(summary).toContain('Total Operations: 2'); // pause
      expect(summary).toContain('Total Operations: 1'); // resume
    });

    test('should include success rate in summary', () => {
      const summary = telemetry.getSummary();

      expect(summary).toContain('Success Rate: 100.0%');
    });

    test('should include duration statistics in summary', () => {
      const summary = telemetry.getSummary();

      expect(summary).toContain('Avg Duration:');
      expect(summary).toContain('p50:');
      expect(summary).toContain('p95:');
      expect(summary).toContain('p99:');
    });
  });

  describe('clearMetrics', () => {
    test('should clear all recorded metrics', () => {
      telemetry.recordOperation({
        operationType: 'pause',
        queryId: 'query-001',
        startTime: 0,
        endTime: 100,
        durationMs: 100,
        success: true
      });

      expect(telemetry.getMetrics()).toHaveLength(1);

      telemetry.clearMetrics();

      expect(telemetry.getMetrics()).toHaveLength(0);
    });

    test('should allow recording after clear', () => {
      telemetry.recordOperation({
        operationType: 'pause',
        queryId: 'query-001',
        startTime: 0,
        endTime: 100,
        durationMs: 100,
        success: true
      });

      telemetry.clearMetrics();

      telemetry.recordOperation({
        operationType: 'resume',
        queryId: 'query-002',
        startTime: 0,
        endTime: 50,
        durationMs: 50,
        success: true
      });

      const metrics = telemetry.getMetrics();
      expect(metrics).toHaveLength(1);
      expect(metrics[0].operationType).toBe('resume');
    });
  });

  describe('exportForTraining', () => {
    beforeEach(() => {
      const testMetrics: OperationMetrics[] = [
        {
          operationType: 'pause',
          queryId: 'query-001',
          startTime: 1000,
          endTime: 1100,
          durationMs: 100,
          success: true,
          metadata: { reason: 'user_requested' }
        },
        {
          operationType: 'pause',
          queryId: 'query-002',
          startTime: 2000,
          endTime: 2150,
          durationMs: 150,
          success: true,
          metadata: { reason: 'timeout' }
        },
        {
          operationType: 'resume',
          queryId: 'query-001',
          startTime: 3000,
          endTime: 3050,
          durationMs: 50,
          success: true
        }
      ];

      testMetrics.forEach(m => telemetry.recordOperation(m));
    });

    test('should export metrics grouped by operation type', () => {
      const exported = telemetry.exportForTraining();

      expect(exported).toHaveLength(2);
      expect(exported.some(e => e.operationType === 'pause')).toBe(true);
      expect(exported.some(e => e.operationType === 'resume')).toBe(true);
    });

    test('should include all samples for each operation type', () => {
      const exported = telemetry.exportForTraining();
      const pauseExport = exported.find(e => e.operationType === 'pause');

      expect(pauseExport?.samples).toHaveLength(2);
    });

    test('should include required fields in samples', () => {
      const exported = telemetry.exportForTraining();
      const pauseExport = exported.find(e => e.operationType === 'pause');
      const sample = pauseExport?.samples[0];

      expect(sample).toHaveProperty('queryId');
      expect(sample).toHaveProperty('durationMs');
      expect(sample).toHaveProperty('success');
      expect(sample).toHaveProperty('timestamp');
    });

    test('should use endTime as timestamp', () => {
      const exported = telemetry.exportForTraining();
      const pauseExport = exported.find(e => e.operationType === 'pause');

      expect(pauseExport?.samples[0].timestamp).toBe(1100);
      expect(pauseExport?.samples[1].timestamp).toBe(2150);
    });

    test('should include metadata when present', () => {
      const exported = telemetry.exportForTraining();
      const pauseExport = exported.find(e => e.operationType === 'pause');

      expect(pauseExport?.samples[0].metadata).toEqual({ reason: 'user_requested' });
      expect(pauseExport?.samples[1].metadata).toEqual({ reason: 'timeout' });
    });

    test('should handle operations without metadata', () => {
      const exported = telemetry.exportForTraining();
      const resumeExport = exported.find(e => e.operationType === 'resume');

      expect(resumeExport?.samples[0].metadata).toBeUndefined();
    });

    test('should return empty array when no metrics recorded', () => {
      telemetry.clearMetrics();
      const exported = telemetry.exportForTraining();

      expect(exported).toHaveLength(0);
    });
  });

  describe('Singleton Pattern', () => {
    test('should return same instance', () => {
      const instance1 = getTelemetryService();
      const instance2 = getTelemetryService();

      expect(instance1).toBe(instance2);
    });

    test('should share state across singleton instances', () => {
      const instance1 = getTelemetryService();
      instance1.recordOperation({
        operationType: 'pause',
        queryId: 'singleton-test',
        startTime: 0,
        endTime: 100,
        durationMs: 100,
        success: true
      });

      const instance2 = getTelemetryService();
      const metrics = instance2.getMetrics();

      expect(metrics.some(m => m.queryId === 'singleton-test')).toBe(true);
    });
  });

  describe('Edge Cases', () => {
    test('should handle operations with zero duration', () => {
      telemetry.recordOperation({
        operationType: 'pause',
        queryId: 'zero-duration',
        startTime: 1000,
        endTime: 1000,
        durationMs: 0,
        success: true
      });

      const aggregated = telemetry.getAggregatedMetrics('pause')[0];
      expect(aggregated.minDurationMs).toBe(0);
      expect(aggregated.avgDurationMs).toBe(0);
    });

    test('should handle operations with very large duration', () => {
      const largeDuration = 999999999;
      telemetry.recordOperation({
        operationType: 'executeCommand',
        queryId: 'large-duration',
        startTime: 0,
        endTime: largeDuration,
        durationMs: largeDuration,
        success: true
      });

      const aggregated = telemetry.getAggregatedMetrics('executeCommand')[0];
      expect(aggregated.maxDurationMs).toBe(largeDuration);
    });

    test('should handle operations with special characters in queryId', () => {
      const specialQueryId = 'query-with-特殊-chars-@#$%';
      telemetry.recordOperation({
        operationType: 'pause',
        queryId: specialQueryId,
        startTime: 0,
        endTime: 100,
        durationMs: 100,
        success: true
      });

      const metrics = telemetry.getMetrics(specialQueryId);
      expect(metrics).toHaveLength(1);
      expect(metrics[0].queryId).toBe(specialQueryId);
    });

    test('should handle operations with complex metadata', () => {
      const complexMetadata = {
        nested: {
          deep: {
            value: 'test'
          }
        },
        array: [1, 2, 3],
        null: null,
        undefined: undefined
      };

      telemetry.recordOperation({
        operationType: 'changeModel',
        queryId: 'complex-metadata',
        startTime: 0,
        endTime: 100,
        durationMs: 100,
        success: true,
        metadata: complexMetadata
      });

      const metrics = telemetry.getMetrics('complex-metadata');
      expect(metrics[0].metadata).toEqual(complexMetadata);
    });
  });
});
