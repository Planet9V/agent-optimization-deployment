/**
 * GAP-003 Query Control System - Performance Profiler Unit Tests
 *
 * File: tests/query-control/unit/PerformanceProfiler.test.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: Comprehensive unit tests for PerformanceProfiler
 *
 * Constitutional Compliance:
 * - DILIGENCE: >90% code coverage
 * - INTEGRITY: All edge cases tested
 * - NO DEVELOPMENT THEATER: Production-grade tests
 */

import { describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import {
  PerformanceProfiler,
  getPerformanceProfiler,
  type PerformanceStatistics,
  type PerformanceTarget,
  type PerformanceAlert
} from '../../../lib/query-control/profiling/performance-profiler';

describe('PerformanceProfiler', () => {
  let profiler: PerformanceProfiler;
  const consoleSpy = {
    log: jest.spyOn(console, 'log').mockImplementation(),
    warn: jest.spyOn(console, 'warn').mockImplementation(),
    error: jest.spyOn(console, 'error').mockImplementation()
  };

  beforeEach(() => {
    profiler = new PerformanceProfiler();
    consoleSpy.log.mockClear();
    consoleSpy.warn.mockClear();
    consoleSpy.error.mockClear();
  });

  afterEach(() => {
    profiler.clear();
  });

  describe('Initialization', () => {
    test('should initialize with default performance targets', () => {
      // Verify default targets are set
      expect(profiler.getTarget('pause')).toEqual({
        operation: 'pause',
        targetMs: 150,
        criticalMs: 300
      });

      expect(profiler.getTarget('resume')).toEqual({
        operation: 'resume',
        targetMs: 150,
        criticalMs: 300
      });

      expect(profiler.getTarget('changeModel')).toEqual({
        operation: 'changeModel',
        targetMs: 200,
        criticalMs: 400
      });

      expect(profiler.getTarget('changePermissions')).toEqual({
        operation: 'changePermissions',
        targetMs: 50,
        criticalMs: 100
      });

      expect(profiler.getTarget('executeCommand')).toEqual({
        operation: 'executeCommand',
        targetMs: 1000,
        criticalMs: 2000
      });

      expect(profiler.getTarget('terminate')).toEqual({
        operation: 'terminate',
        targetMs: 100,
        criticalMs: 200
      });

      expect(profiler.getTarget('full_workflow')).toEqual({
        operation: 'full_workflow',
        targetMs: 500,
        criticalMs: 1000
      });
    });

    test('should start with no latency data', () => {
      expect(profiler.getStatistics('pause')).toBeNull();
      expect(profiler.getAllStatistics().size).toBe(0);
    });

    test('should start with no alerts', () => {
      expect(profiler.getAlerts()).toEqual([]);
    });
  });

  describe('recordLatency()', () => {
    test('should record latency for an operation', () => {
      profiler.recordLatency('pause', 100);

      const stats = profiler.getStatistics('pause');
      expect(stats).not.toBeNull();
      expect(stats!.sampleCount).toBe(1);
      expect(stats!.min).toBe(100);
      expect(stats!.max).toBe(100);
      expect(stats!.avg).toBe(100);
    });

    test('should record multiple latencies for same operation', () => {
      profiler.recordLatency('pause', 100);
      profiler.recordLatency('pause', 150);
      profiler.recordLatency('pause', 120);

      const stats = profiler.getStatistics('pause');
      expect(stats!.sampleCount).toBe(3);
      expect(stats!.min).toBe(100);
      expect(stats!.max).toBe(150);
    });

    test('should record latencies for different operations', () => {
      profiler.recordLatency('pause', 100);
      profiler.recordLatency('resume', 200);
      profiler.recordLatency('terminate', 50);

      expect(profiler.getStatistics('pause')!.sampleCount).toBe(1);
      expect(profiler.getStatistics('resume')!.sampleCount).toBe(1);
      expect(profiler.getStatistics('terminate')!.sampleCount).toBe(1);
    });

    test('should enforce maxSamples limit of 1000', () => {
      // Record 1100 samples
      for (let i = 0; i < 1100; i++) {
        profiler.recordLatency('pause', 100 + i);
      }

      const stats = profiler.getStatistics('pause');
      expect(stats!.sampleCount).toBe(1000); // Should be limited to 1000
      expect(stats!.min).toBe(200); // First 100 samples should be removed (100-199)
      expect(stats!.max).toBe(1199); // Last sample
    });

    test('should log latency recording', () => {
      profiler.recordLatency('pause', 100);
      expect(consoleSpy.log).toHaveBeenCalledWith('[Profiler] pause: 100ms');
    });

    test('should not generate alert for latency within target', () => {
      profiler.recordLatency('pause', 100); // Target is 150ms
      expect(profiler.getAlerts()).toEqual([]);
    });

    test('should generate warning alert for latency exceeding target', () => {
      profiler.recordLatency('pause', 200); // Target: 150ms, Critical: 300ms

      const alerts = profiler.getAlerts();
      expect(alerts).toHaveLength(1);
      expect(alerts[0].severity).toBe('warning');
      expect(alerts[0].operation).toBe('pause');
      expect(alerts[0].latencyMs).toBe(200);
      expect(alerts[0].targetMs).toBe(150);
    });

    test('should generate critical alert for latency exceeding critical threshold', () => {
      profiler.recordLatency('pause', 350); // Target: 150ms, Critical: 300ms

      const alerts = profiler.getAlerts();
      expect(alerts).toHaveLength(1);
      expect(alerts[0].severity).toBe('critical');
      expect(alerts[0].operation).toBe('pause');
      expect(alerts[0].latencyMs).toBe(350);
    });

    test('should log warning alerts', () => {
      profiler.recordLatency('pause', 200);
      expect(consoleSpy.warn).toHaveBeenCalledWith(
        expect.stringContaining('[Profiler] WARNING:')
      );
    });

    test('should log critical alerts', () => {
      profiler.recordLatency('pause', 350);
      expect(consoleSpy.error).toHaveBeenCalledWith(
        expect.stringContaining('[Profiler] CRITICAL:')
      );
    });

    test('should not generate alerts for operations without targets', () => {
      profiler.recordLatency('custom_operation', 5000);
      expect(profiler.getAlerts()).toEqual([]);
    });
  });

  describe('getStatistics()', () => {
    test('should return null for operation with no data', () => {
      expect(profiler.getStatistics('nonexistent')).toBeNull();
    });

    test('should calculate min and max correctly', () => {
      profiler.recordLatency('pause', 100);
      profiler.recordLatency('pause', 50);
      profiler.recordLatency('pause', 200);

      const stats = profiler.getStatistics('pause');
      expect(stats!.min).toBe(50);
      expect(stats!.max).toBe(200);
    });

    test('should calculate average correctly', () => {
      profiler.recordLatency('pause', 100);
      profiler.recordLatency('pause', 150);
      profiler.recordLatency('pause', 200);

      const stats = profiler.getStatistics('pause');
      expect(stats!.avg).toBe(150);
    });

    test('should calculate median (p50) correctly', () => {
      profiler.recordLatency('pause', 50);
      profiler.recordLatency('pause', 100);
      profiler.recordLatency('pause', 150);
      profiler.recordLatency('pause', 200);
      profiler.recordLatency('pause', 250);

      const stats = profiler.getStatistics('pause');
      expect(stats!.median).toBe(150);
      expect(stats!.p50).toBe(150);
    });

    test('should calculate p75 correctly', () => {
      const values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
      values.forEach(v => profiler.recordLatency('pause', v));

      const stats = profiler.getStatistics('pause');
      expect(stats!.p75).toBe(80); // 75th percentile of 10 values
    });

    test('should calculate p90 correctly', () => {
      const values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
      values.forEach(v => profiler.recordLatency('pause', v));

      const stats = profiler.getStatistics('pause');
      expect(stats!.p90).toBe(100); // 90th percentile of 10 values
    });

    test('should calculate p95 correctly', () => {
      const values = Array.from({ length: 100 }, (_, i) => i + 1);
      values.forEach(v => profiler.recordLatency('pause', v));

      const stats = profiler.getStatistics('pause');
      expect(stats!.p95).toBe(96); // 95th percentile of 100 values
    });

    test('should calculate p99 correctly', () => {
      const values = Array.from({ length: 100 }, (_, i) => i + 1);
      values.forEach(v => profiler.recordLatency('pause', v));

      const stats = profiler.getStatistics('pause');
      expect(stats!.p99).toBe(100); // 99th percentile of 100 values
    });

    test('should calculate standard deviation correctly', () => {
      // Values: 10, 20, 30, 40, 50
      // Mean: 30
      // Variance: ((20^2 + 10^2 + 0^2 + 10^2 + 20^2) / 5) = 200
      // StdDev: sqrt(200) ≈ 14.14
      profiler.recordLatency('pause', 10);
      profiler.recordLatency('pause', 20);
      profiler.recordLatency('pause', 30);
      profiler.recordLatency('pause', 40);
      profiler.recordLatency('pause', 50);

      const stats = profiler.getStatistics('pause');
      expect(stats!.stdDev).toBeCloseTo(14.14, 1);
    });

    test('should handle single sample correctly', () => {
      profiler.recordLatency('pause', 100);

      const stats = profiler.getStatistics('pause');
      expect(stats!.sampleCount).toBe(1);
      expect(stats!.min).toBe(100);
      expect(stats!.max).toBe(100);
      expect(stats!.avg).toBe(100);
      expect(stats!.median).toBe(100);
      expect(stats!.stdDev).toBe(0); // No variance with single sample
    });

    test('should include operation name and sample count', () => {
      profiler.recordLatency('pause', 100);
      profiler.recordLatency('pause', 150);

      const stats = profiler.getStatistics('pause');
      expect(stats!.operation).toBe('pause');
      expect(stats!.sampleCount).toBe(2);
    });
  });

  describe('getAllStatistics()', () => {
    test('should return empty map with no data', () => {
      expect(profiler.getAllStatistics().size).toBe(0);
    });

    test('should return statistics for all operations', () => {
      profiler.recordLatency('pause', 100);
      profiler.recordLatency('resume', 120);
      profiler.recordLatency('terminate', 50);

      const allStats = profiler.getAllStatistics();
      expect(allStats.size).toBe(3);
      expect(allStats.has('pause')).toBe(true);
      expect(allStats.has('resume')).toBe(true);
      expect(allStats.has('terminate')).toBe(true);
    });

    test('should not include operations with no data', () => {
      profiler.recordLatency('pause', 100);

      const allStats = profiler.getAllStatistics();
      expect(allStats.size).toBe(1);
      expect(allStats.has('pause')).toBe(true);
      expect(allStats.has('resume')).toBe(false);
    });
  });

  describe('getGrade()', () => {
    test('should return "N/A" for operation with no data', () => {
      expect(profiler.getGrade('nonexistent')).toBe('N/A');
    });

    test('should return "N/A" for operation without target', () => {
      profiler.recordLatency('custom_op', 100);
      expect(profiler.getGrade('custom_op')).toBe('N/A');
    });

    test('should return "A+" for performance 50% better than target', () => {
      profiler.recordLatency('pause', 75); // Target: 150ms, 75/150 = 0.5
      expect(profiler.getGrade('pause')).toBe('A+');
    });

    test('should return "A" for performance 25% better than target', () => {
      profiler.recordLatency('pause', 112.5); // Target: 150ms, 112.5/150 = 0.75
      expect(profiler.getGrade('pause')).toBe('A');
    });

    test('should return "B" for performance meeting target', () => {
      profiler.recordLatency('pause', 150); // Target: 150ms, exactly on target
      expect(profiler.getGrade('pause')).toBe('B');
    });

    test('should return "C" for performance 25% worse than target', () => {
      profiler.recordLatency('pause', 187.5); // Target: 150ms, 187.5/150 = 1.25
      expect(profiler.getGrade('pause')).toBe('C');
    });

    test('should return "D" for performance 50% worse than target', () => {
      profiler.recordLatency('pause', 225); // Target: 150ms, 225/150 = 1.5
      expect(profiler.getGrade('pause')).toBe('D');
    });

    test('should return "F" for performance more than 50% worse than target', () => {
      profiler.recordLatency('pause', 300); // Target: 150ms, 300/150 = 2.0
      expect(profiler.getGrade('pause')).toBe('F');
    });

    test('should calculate grade based on average of multiple samples', () => {
      profiler.recordLatency('pause', 50);
      profiler.recordLatency('pause', 100);
      profiler.recordLatency('pause', 150);
      // Average: 100ms, Target: 150ms, Ratio: 0.667

      expect(profiler.getGrade('pause')).toBe('A');
    });
  });

  describe('setTarget() and getTarget()', () => {
    test('should set custom performance target', () => {
      profiler.setTarget('custom_op', 500, 1000);

      const target = profiler.getTarget('custom_op');
      expect(target).toEqual({
        operation: 'custom_op',
        targetMs: 500,
        criticalMs: 1000
      });
    });

    test('should override existing target', () => {
      profiler.setTarget('pause', 200, 400); // Override default 150/300

      const target = profiler.getTarget('pause');
      expect(target!.targetMs).toBe(200);
      expect(target!.criticalMs).toBe(400);
    });

    test('should return undefined for non-existent target', () => {
      expect(profiler.getTarget('nonexistent')).toBeUndefined();
    });

    test('should use custom target for alert generation', () => {
      profiler.setTarget('custom_op', 100, 200);
      profiler.recordLatency('custom_op', 150); // Between target and critical

      const alerts = profiler.getAlerts();
      expect(alerts).toHaveLength(1);
      expect(alerts[0].severity).toBe('warning');
      expect(alerts[0].targetMs).toBe(100);
    });
  });

  describe('Alert Generation', () => {
    test('should generate warning alert with correct message', () => {
      profiler.recordLatency('pause', 200);

      const alerts = profiler.getAlerts();
      expect(alerts[0].message).toContain('pause');
      expect(alerts[0].message).toContain('exceeded target');
      expect(alerts[0].message).toContain('200ms');
      expect(alerts[0].message).toContain('150ms');
    });

    test('should generate critical alert with correct message', () => {
      profiler.recordLatency('pause', 350);

      const alerts = profiler.getAlerts();
      expect(alerts[0].message).toContain('pause');
      expect(alerts[0].message).toContain('exceeded critical threshold');
      expect(alerts[0].message).toContain('350ms');
      expect(alerts[0].message).toContain('300ms');
    });

    test('should include timestamp in alerts', () => {
      const before = Date.now();
      profiler.recordLatency('pause', 200);
      const after = Date.now();

      const alerts = profiler.getAlerts();
      expect(alerts[0].timestamp).toBeGreaterThanOrEqual(before);
      expect(alerts[0].timestamp).toBeLessThanOrEqual(after);
    });

    test('should limit alert history to 100', () => {
      // Generate 150 alerts
      for (let i = 0; i < 150; i++) {
        profiler.recordLatency('pause', 200); // Each generates warning
      }

      const alerts = profiler.getAlerts(undefined, 1000);
      expect(alerts.length).toBe(100); // Should be limited to 100
    });

    test('should filter alerts by severity', () => {
      profiler.recordLatency('pause', 200); // Warning
      profiler.recordLatency('pause', 350); // Critical
      profiler.recordLatency('resume', 250); // Warning

      const warningAlerts = profiler.getAlerts('warning');
      expect(warningAlerts).toHaveLength(2);
      expect(warningAlerts.every(a => a.severity === 'warning')).toBe(true);

      const criticalAlerts = profiler.getAlerts('critical');
      expect(criticalAlerts).toHaveLength(1);
      expect(criticalAlerts[0].severity).toBe('critical');
    });

    test('should limit returned alerts', () => {
      for (let i = 0; i < 30; i++) {
        profiler.recordLatency('pause', 200);
      }

      const alerts = profiler.getAlerts(undefined, 5);
      expect(alerts).toHaveLength(5);
    });

    test('should return most recent alerts', () => {
      profiler.recordLatency('pause', 200); // First
      profiler.recordLatency('pause', 250); // Second
      profiler.recordLatency('pause', 280); // Third (most recent)

      const alerts = profiler.getAlerts(undefined, 1);
      expect(alerts).toHaveLength(1);
      expect(alerts[0].latencyMs).toBe(280); // Most recent
    });
  });

  describe('clear()', () => {
    test('should clear all latency data', () => {
      profiler.recordLatency('pause', 100);
      profiler.recordLatency('resume', 120);

      profiler.clear();

      expect(profiler.getStatistics('pause')).toBeNull();
      expect(profiler.getStatistics('resume')).toBeNull();
      expect(profiler.getAllStatistics().size).toBe(0);
    });

    test('should clear all alerts', () => {
      profiler.recordLatency('pause', 200); // Generates alert

      profiler.clear();

      expect(profiler.getAlerts()).toEqual([]);
    });

    test('should preserve targets after clear', () => {
      profiler.setTarget('custom_op', 500, 1000);

      profiler.clear();

      expect(profiler.getTarget('custom_op')).toEqual({
        operation: 'custom_op',
        targetMs: 500,
        criticalMs: 1000
      });
    });

    test('should log clear operation', () => {
      profiler.clear();
      expect(consoleSpy.log).toHaveBeenCalledWith(
        '[Profiler] Performance data cleared'
      );
    });
  });

  describe('meetsTarget()', () => {
    test('should return true for performance within target', () => {
      profiler.recordLatency('pause', 100); // Target: 150ms
      expect(profiler.meetsTarget('pause')).toBe(true);
    });

    test('should return false for performance exceeding target', () => {
      profiler.recordLatency('pause', 200); // Target: 150ms
      expect(profiler.meetsTarget('pause')).toBe(false);
    });

    test('should return true for operation with no data', () => {
      expect(profiler.meetsTarget('nonexistent')).toBe(true);
    });

    test('should return true for operation without target', () => {
      profiler.recordLatency('custom_op', 5000);
      expect(profiler.meetsTarget('custom_op')).toBe(true);
    });

    test('should check average performance, not single samples', () => {
      profiler.recordLatency('pause', 100);
      profiler.recordLatency('pause', 200); // One exceeds target
      // Average: 150ms, exactly on target

      expect(profiler.meetsTarget('pause')).toBe(true);
    });
  });

  describe('getReport()', () => {
    test('should generate report with statistics', () => {
      profiler.recordLatency('pause', 100);
      profiler.recordLatency('pause', 150);

      const report = profiler.getReport();
      expect(report).toContain('Performance Profiler Report');
      expect(report).toContain('pause');
      expect(report).toContain('Samples: 2');
    });

    test('should include target information in report', () => {
      profiler.recordLatency('pause', 100);

      const report = profiler.getReport();
      expect(report).toContain('target: 150ms');
      expect(report).toContain('critical: 300ms');
    });

    test('should include percentiles in report', () => {
      profiler.recordLatency('pause', 100);

      const report = profiler.getReport();
      expect(report).toContain('p50:');
      expect(report).toContain('p95:');
      expect(report).toContain('p99:');
    });

    test('should include performance vs target', () => {
      profiler.recordLatency('pause', 75); // 50% of target

      const report = profiler.getReport();
      expect(report).toContain('50.0% of target');
      expect(report).toContain('✅ PASS');
    });

    test('should show fail when exceeding target', () => {
      profiler.recordLatency('pause', 200); // 133% of target

      const report = profiler.getReport();
      expect(report).toContain('❌ FAIL');
    });

    test('should include recent alerts in report', () => {
      profiler.recordLatency('pause', 200); // Warning
      profiler.recordLatency('pause', 350); // Critical

      const report = profiler.getReport();
      expect(report).toContain('Recent Alerts');
      expect(report).toContain('⚠️');
      expect(report).toContain('🚨');
    });

    test('should handle empty profiler gracefully', () => {
      const report = profiler.getReport();
      expect(report).toContain('Performance Profiler Report');
      expect(report).not.toContain('Recent Alerts');
    });
  });

  describe('Singleton Pattern', () => {
    test('getPerformanceProfiler should return singleton instance', () => {
      const instance1 = getPerformanceProfiler();
      const instance2 = getPerformanceProfiler();

      expect(instance1).toBe(instance2); // Same instance
    });

    test('singleton should maintain state across calls', () => {
      const instance1 = getPerformanceProfiler();
      instance1.recordLatency('test_op', 100);

      const instance2 = getPerformanceProfiler();
      const stats = instance2.getStatistics('test_op');

      expect(stats).not.toBeNull();
      expect(stats!.sampleCount).toBe(1);
    });
  });

  describe('Edge Cases and Error Handling', () => {
    test('should handle zero latency', () => {
      profiler.recordLatency('pause', 0);

      const stats = profiler.getStatistics('pause');
      expect(stats!.min).toBe(0);
      expect(stats!.avg).toBe(0);
    });

    test('should handle very large latencies', () => {
      profiler.recordLatency('pause', 999999);

      const stats = profiler.getStatistics('pause');
      expect(stats!.max).toBe(999999);
    });

    test('should handle decimal latencies', () => {
      profiler.recordLatency('pause', 123.456);

      const stats = profiler.getStatistics('pause');
      expect(stats!.avg).toBeCloseTo(123.456, 2);
    });

    test('should handle operations with special characters', () => {
      profiler.recordLatency('custom:operation-123', 100);

      const stats = profiler.getStatistics('custom:operation-123');
      expect(stats).not.toBeNull();
      expect(stats!.operation).toBe('custom:operation-123');
    });

    test('should handle rapid successive recordings', () => {
      for (let i = 0; i < 100; i++) {
        profiler.recordLatency('pause', i);
      }

      const stats = profiler.getStatistics('pause');
      expect(stats!.sampleCount).toBe(100);
    });

    test('should handle mixed warning and critical alerts', () => {
      profiler.recordLatency('pause', 200); // Warning
      profiler.recordLatency('pause', 100); // OK
      profiler.recordLatency('pause', 350); // Critical
      profiler.recordLatency('pause', 180); // Warning

      const allAlerts = profiler.getAlerts();
      expect(allAlerts).toHaveLength(3);

      const warnings = profiler.getAlerts('warning');
      expect(warnings).toHaveLength(2);

      const criticals = profiler.getAlerts('critical');
      expect(criticals).toHaveLength(1);
    });
  });

  describe('Performance Target Validation', () => {
    test('should validate all default targets are set correctly', () => {
      const targets = [
        { op: 'pause', target: 150, critical: 300 },
        { op: 'resume', target: 150, critical: 300 },
        { op: 'changeModel', target: 200, critical: 400 },
        { op: 'changePermissions', target: 50, critical: 100 },
        { op: 'executeCommand', target: 1000, critical: 2000 },
        { op: 'terminate', target: 100, critical: 200 },
        { op: 'full_workflow', target: 500, critical: 1000 }
      ];

      targets.forEach(({ op, target, critical }) => {
        const t = profiler.getTarget(op);
        expect(t).toBeDefined();
        expect(t!.targetMs).toBe(target);
        expect(t!.criticalMs).toBe(critical);
      });
    });

    test('should ensure critical threshold is always greater than target', () => {
      profiler.setTarget('test', 100, 200);
      const target = profiler.getTarget('test');
      expect(target!.criticalMs).toBeGreaterThan(target!.targetMs);
    });
  });
});
