/**
 * GAP-003 Query Control System - QueryControlService.changeModel() Unit Tests
 *
 * File: tests/query-control/unit/QueryControlService.changeModel.test.ts
 * Created: 2025-11-15
 * Version: v1.1.0
 * Purpose: Comprehensive unit tests for changeModel() operation
 *
 * Constitutional Compliance:
 * - DILIGENCE: >90% code coverage, >85% branch coverage
 * - INTEGRITY: All model combinations and instrumentation tested
 * - NO DEVELOPMENT THEATER: Production-grade test suite
 *
 * Performance Target: <200ms changeModel operation
 *
 * Test Coverage:
 * ✅ Success scenarios for all 3 models (sonnet, opus, haiku)
 * ✅ Previous/current model tracking
 * ✅ Telemetry recording with metadata
 * ✅ Performance profiling (<200ms target)
 * ✅ Neural hook training (model_switch pattern)
 * ✅ Error handling (invalid model, query not found)
 * ✅ All model transition combinations
 * ✅ Registry update verification
 */

import { describe, test, expect, beforeEach, afterEach, jest } from '@jest/globals';
import { QueryControlService } from '../../../lib/query-control/query-control-service';
import { ModelType } from '../../../lib/query-control/model/model-switcher';
import { QueryState, QueryStateMachine } from '../../../lib/query-control/state/state-machine';

describe('QueryControlService.changeModel()', () => {
  let service: QueryControlService;
  let testQueryId: string;

  beforeEach(async () => {
    service = new QueryControlService();
    testQueryId = `test-query-changemodel-${Date.now()}-${Math.random()}`; // Unique query ID per test

    // Create and register a test query
    await service.queryRegistry.registerQuery(testQueryId, {
      state: QueryState.INIT,
      model: ModelType.SONNET,
      permissionMode: 'default',
      startTime: Date.now(),
      agentCount: 0,
      taskCount: 0,
      checkpointCount: 0
    });

    // Create state machine and transition to RUNNING
    const stateMachine = new QueryStateMachine(testQueryId);
    await stateMachine.transition('START');
    service.stateMachines.set(testQueryId, stateMachine);
  });

  afterEach(async () => {
    // Clean up test state
    service.stateMachines.clear();
    await service.queryRegistry.clear();
    service.telemetryService.clearMetrics();
  });

  describe('Success Scenarios - All Models', () => {
    test('should switch from SONNET to OPUS successfully', async () => {
      const startTime = Date.now();
      const initialModel = service.modelSwitcher.getCurrentModel();

      const result = await service.changeModel(
        testQueryId,
        ModelType.OPUS,
        'testing_sonnet_to_opus'
      );

      const endTime = Date.now();
      const duration = endTime - startTime;

      expect(result.success).toBe(true);
      expect(result.previousModel).toBe(initialModel);
      expect(result.currentModel).toBe(ModelType.OPUS);
      expect(result.switchTimeMs).toBeGreaterThan(0);
      expect(result.error).toBeUndefined();

      // Performance target: <200ms
      expect(duration).toBeLessThan(200);
    });

    test('should switch from SONNET to HAIKU successfully', async () => {
      const startTime = Date.now();
      const initialModel = service.modelSwitcher.getCurrentModel();

      const result = await service.changeModel(
        testQueryId,
        ModelType.HAIKU,
        'testing_sonnet_to_haiku'
      );

      const endTime = Date.now();
      const duration = endTime - startTime;

      expect(result.success).toBe(true);
      expect(result.previousModel).toBe(initialModel);
      expect(result.currentModel).toBe(ModelType.HAIKU);
      expect(result.switchTimeMs).toBeGreaterThan(0);
      expect(result.error).toBeUndefined();

      // Performance target: <200ms
      expect(duration).toBeLessThan(200);
    });

    test('should switch from OPUS to HAIKU successfully', async () => {
      // First switch to OPUS
      await service.changeModel(testQueryId, ModelType.OPUS, 'setup');

      const startTime = Date.now();

      const result = await service.changeModel(
        testQueryId,
        ModelType.HAIKU,
        'testing_opus_to_haiku'
      );

      const endTime = Date.now();
      const duration = endTime - startTime;

      expect(result.success).toBe(true);
      expect(result.previousModel).toBe(ModelType.OPUS);
      expect(result.currentModel).toBe(ModelType.HAIKU);
      expect(result.switchTimeMs).toBeGreaterThan(0);
      expect(result.error).toBeUndefined();

      // Performance target: <200ms
      expect(duration).toBeLessThan(200);
    });

    test('should switch from OPUS to SONNET successfully', async () => {
      // First switch to OPUS
      await service.changeModel(testQueryId, ModelType.OPUS, 'setup');

      const result = await service.changeModel(
        testQueryId,
        ModelType.SONNET,
        'testing_opus_to_sonnet'
      );

      expect(result.success).toBe(true);
      expect(result.previousModel).toBe(ModelType.OPUS);
      expect(result.currentModel).toBe(ModelType.SONNET);
      expect(result.switchTimeMs).toBeGreaterThan(0);
      expect(result.error).toBeUndefined();
    });

    test('should switch from HAIKU to SONNET successfully', async () => {
      // First switch to HAIKU
      await service.changeModel(testQueryId, ModelType.HAIKU, 'setup');

      const result = await service.changeModel(
        testQueryId,
        ModelType.SONNET,
        'testing_haiku_to_sonnet'
      );

      expect(result.success).toBe(true);
      expect(result.previousModel).toBe(ModelType.HAIKU);
      expect(result.currentModel).toBe(ModelType.SONNET);
      expect(result.switchTimeMs).toBeGreaterThan(0);
      expect(result.error).toBeUndefined();
    });

    test('should switch from HAIKU to OPUS successfully', async () => {
      // First switch to HAIKU
      await service.changeModel(testQueryId, ModelType.HAIKU, 'setup');

      const result = await service.changeModel(
        testQueryId,
        ModelType.OPUS,
        'testing_haiku_to_opus'
      );

      expect(result.success).toBe(true);
      expect(result.previousModel).toBe(ModelType.HAIKU);
      expect(result.currentModel).toBe(ModelType.OPUS);
      expect(result.switchTimeMs).toBeGreaterThan(0);
      expect(result.error).toBeUndefined();
    });
  });

  describe('Model Tracking', () => {
    test('should correctly track previous and current models', async () => {
      const initialModel = service.modelSwitcher.getCurrentModel();

      const result = await service.changeModel(
        testQueryId,
        ModelType.OPUS,
        'tracking_test'
      );

      expect(result.previousModel).toBe(initialModel);
      expect(result.currentModel).toBe(ModelType.OPUS);

      // Verify subsequent switch tracks correctly
      const result2 = await service.changeModel(
        testQueryId,
        ModelType.HAIKU,
        'tracking_test_2'
      );

      expect(result2.previousModel).toBe(ModelType.OPUS);
      expect(result2.currentModel).toBe(ModelType.HAIKU);
    });

    test('should maintain model state across multiple switches', async () => {
      // Switch chain: SONNET → OPUS → HAIKU → SONNET
      const r1 = await service.changeModel(testQueryId, ModelType.OPUS);
      expect(r1.currentModel).toBe(ModelType.OPUS);

      const r2 = await service.changeModel(testQueryId, ModelType.HAIKU);
      expect(r2.currentModel).toBe(ModelType.HAIKU);

      const r3 = await service.changeModel(testQueryId, ModelType.SONNET);
      expect(r3.currentModel).toBe(ModelType.SONNET);
      expect(r3.previousModel).toBe(ModelType.HAIKU);
    });
  });

  describe('Telemetry Recording', () => {
    test('should record successful operation with correct metadata', async () => {
      const telemetry = service.telemetryService;
      telemetry.clearMetrics();
      const initialModel = service.modelSwitcher.getCurrentModel();

      await service.changeModel(
        testQueryId,
        ModelType.OPUS,
        'telemetry_test'
      );

      const metrics = telemetry.getMetrics();
      const changeModelMetric = metrics.find(m => m.operationType === 'changeModel');

      expect(changeModelMetric).toBeDefined();
      expect(changeModelMetric?.operationType).toBe('changeModel');
      expect(changeModelMetric?.queryId).toBe(testQueryId);
      expect(changeModelMetric?.success).toBe(true);
      expect(changeModelMetric?.durationMs).toBeGreaterThan(0);

      // Verify metadata
      expect(changeModelMetric?.metadata).toBeDefined();
      expect(changeModelMetric?.metadata?.previousModel).toBe(initialModel);
      expect(changeModelMetric?.metadata?.currentModel).toBe(ModelType.OPUS);
      expect(changeModelMetric?.metadata?.reason).toBe('telemetry_test');
    });

    test('should record failed operation with error', async () => {
      const telemetry = service.telemetryService;
      telemetry.clearMetrics();

      await service.changeModel(
        'nonexistent-query',
        ModelType.OPUS,
        'error_test'
      );

      const metrics = telemetry.getMetrics();
      const changeModelMetric = metrics.find(
        m => m.operationType === 'changeModel' && m.queryId === 'nonexistent-query'
      );

      expect(changeModelMetric).toBeDefined();
      expect(changeModelMetric?.success).toBe(false);
      expect(changeModelMetric?.error).toBeDefined();
    });

    test('should include timing metadata in telemetry', async () => {
      const telemetry = service.telemetryService;
      telemetry.clearMetrics();

      const beforeTime = Date.now();
      await service.changeModel(testQueryId, ModelType.OPUS);
      const afterTime = Date.now();

      const metrics = telemetry.getMetrics();
      const changeModelMetric = metrics.find(
        m => m.operationType === 'changeModel' && m.queryId === testQueryId
      );

      expect(changeModelMetric?.startTime).toBeGreaterThanOrEqual(beforeTime);
      expect(changeModelMetric?.endTime).toBeLessThanOrEqual(afterTime);
      expect(changeModelMetric?.durationMs).toBe(
        changeModelMetric!.endTime - changeModelMetric!.startTime
      );
    });
  });

  describe('Performance Profiling', () => {
    test('should record latency for successful model change', async () => {
      const profiler = service.performanceProfiler;
      const beforeCount = profiler.getLatencyStats('changeModel')?.count || 0;

      await service.changeModel(testQueryId, ModelType.OPUS);

      const stats = profiler.getLatencyStats('changeModel');

      expect(stats).toBeDefined();
      expect(stats?.count).toBeGreaterThan(beforeCount);
      expect(stats?.mean).toBeGreaterThan(0);
      expect(stats?.mean).toBeLessThan(200); // Performance target
    });

    test('should record latency for failed model change', async () => {
      const profiler = service.performanceProfiler;
      const beforeCount = profiler.getLatencyStats('changeModel')?.count || 0;

      await service.changeModel('nonexistent-query', ModelType.OPUS);

      const stats = profiler.getLatencyStats('changeModel');

      expect(stats).toBeDefined();
      expect(stats?.count).toBeGreaterThan(beforeCount);
    });

    test('should meet <200ms performance target', async () => {
      const startTime = Date.now();

      await service.changeModel(testQueryId, ModelType.HAIKU);

      const duration = Date.now() - startTime;

      expect(duration).toBeLessThan(200);
    });

    test('should track multiple model changes for performance analysis', async () => {
      const profiler = service.performanceProfiler;
      const beforeCount = profiler.getLatencyStats('changeModel')?.count || 0;

      // Perform multiple model changes
      await service.changeModel(testQueryId, ModelType.OPUS);
      await service.changeModel(testQueryId, ModelType.HAIKU);
      await service.changeModel(testQueryId, ModelType.SONNET);

      const stats = profiler.getLatencyStats('changeModel');

      expect(stats?.count).toBeGreaterThanOrEqual(beforeCount + 3);
      expect(stats?.p50).toBeGreaterThan(0);
      expect(stats?.p95).toBeGreaterThan(0);
      expect(stats?.p99).toBeGreaterThan(0);
    });
  });

  describe('Neural Hook Training', () => {
    test('should train optimization pattern on successful switch', async () => {
      const neuralHooks = service.neuralHooks;
      const trainSpy = jest.spyOn(neuralHooks, 'trainOptimizationPattern');
      const initialModel = service.modelSwitcher.getCurrentModel();

      await service.changeModel(
        testQueryId,
        ModelType.OPUS,
        'neural_test'
      );

      expect(trainSpy).toHaveBeenCalledWith(
        testQueryId,
        'model_switch',
        expect.objectContaining({
          previousModel: initialModel,
          targetModel: ModelType.OPUS
        }),
        expect.any(Number),
        true
      );

      trainSpy.mockRestore();
    });

    test('should include switch timing in neural training', async () => {
      const neuralHooks = service.neuralHooks;
      const trainSpy = jest.spyOn(neuralHooks, 'trainOptimizationPattern');

      const result = await service.changeModel(testQueryId, ModelType.HAIKU);

      expect(trainSpy).toHaveBeenCalledWith(
        testQueryId,
        'model_switch',
        expect.any(Object),
        result.switchTimeMs,
        true
      );

      trainSpy.mockRestore();
    });

    test('should not train pattern on failed switch', async () => {
      const neuralHooks = service.neuralHooks;
      const trainSpy = jest.spyOn(neuralHooks, 'trainOptimizationPattern');

      await service.changeModel('nonexistent-query', ModelType.OPUS);

      expect(trainSpy).not.toHaveBeenCalled();

      trainSpy.mockRestore();
    });
  });

  describe('Error Handling', () => {
    test('should handle query not found error', async () => {
      const currentModel = service.modelSwitcher.getCurrentModel();

      const result = await service.changeModel(
        'nonexistent-query-12345',
        ModelType.OPUS,
        'error_test'
      );

      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
      expect(result.error).toContain('Query not found');
      expect(result.switchTimeMs).toBe(0);
      expect(result.previousModel).toBe(currentModel);
      expect(result.currentModel).toBe(currentModel);
    });

    test('should handle invalid model type gracefully', async () => {
      const result = await service.changeModel(
        testQueryId,
        'invalid-model' as ModelType,
        'invalid_model_test'
      );

      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
    });

    test('should preserve state on failed model change', async () => {
      const initialModel = service.modelSwitcher.getCurrentModel();

      await service.changeModel('nonexistent-query', ModelType.OPUS);

      const currentModel = service.modelSwitcher.getCurrentModel();
      expect(currentModel).toBe(initialModel);
    });

    test('should record error in telemetry for failed changes', async () => {
      const telemetry = service.telemetryService;
      telemetry.clearMetrics();

      await service.changeModel('bad-query', ModelType.HAIKU);

      const metrics = telemetry.getMetrics();
      const errorMetric = metrics.find(
        m => m.operationType === 'changeModel' && m.queryId === 'bad-query'
      );

      expect(errorMetric).toBeDefined();
      expect(errorMetric?.error).toBeDefined();
      expect(errorMetric?.success).toBe(false);
    });
  });

  describe('Registry Updates', () => {
    test('should update query registry with new model', async () => {
      await service.changeModel(testQueryId, ModelType.OPUS);

      const queryInfo = await service.queryRegistry.getQuery(testQueryId);

      expect(queryInfo).toBeDefined();
      expect(queryInfo?.model).toBe(ModelType.OPUS);
    });

    test('should update metadata with model switch timestamp', async () => {
      const beforeSwitch = Date.now();

      await service.changeModel(testQueryId, ModelType.HAIKU);

      const afterSwitch = Date.now();
      const queryInfo = await service.queryRegistry.getQuery(testQueryId);

      expect(queryInfo?.metadata?.modelSwitchedAt).toBeDefined();
      expect(queryInfo!.metadata!.modelSwitchedAt).toBeGreaterThanOrEqual(beforeSwitch);
      expect(queryInfo!.metadata!.modelSwitchedAt).toBeLessThanOrEqual(afterSwitch);
    });

    test('should track multiple model switches in metadata', async () => {
      await service.changeModel(testQueryId, ModelType.OPUS);
      const time1 = Date.now();

      await new Promise(resolve => setTimeout(resolve, 10)); // Small delay

      await service.changeModel(testQueryId, ModelType.HAIKU);
      const time2 = Date.now();

      const queryInfo = await service.queryRegistry.getQuery(testQueryId);

      expect(queryInfo?.metadata?.modelSwitchedAt).toBeDefined();
      expect(queryInfo!.metadata!.modelSwitchedAt).toBeGreaterThan(time1);
      expect(queryInfo!.metadata!.modelSwitchedAt).toBeLessThanOrEqual(time2);
    });
  });

  describe('All Model Combination Matrix', () => {
    const modelCombinations = [
      { from: ModelType.SONNET, to: ModelType.OPUS, name: 'SONNET→OPUS' },
      { from: ModelType.SONNET, to: ModelType.HAIKU, name: 'SONNET→HAIKU' },
      { from: ModelType.OPUS, to: ModelType.SONNET, name: 'OPUS→SONNET' },
      { from: ModelType.OPUS, to: ModelType.HAIKU, name: 'OPUS→HAIKU' },
      { from: ModelType.HAIKU, to: ModelType.SONNET, name: 'HAIKU→SONNET' },
      { from: ModelType.HAIKU, to: ModelType.OPUS, name: 'HAIKU→OPUS' }
    ];

    modelCombinations.forEach(({ from, to, name }) => {
      test(`should handle ${name} transition`, async () => {
        // Set up initial model to 'from' state
        await service.changeModel(testQueryId, from, 'setup');

        // Verify we're at the expected starting state
        const currentModel = service.modelSwitcher.getCurrentModel();
        expect(currentModel).toBe(from);

        const result = await service.changeModel(testQueryId, to, `test_${name}`);

        expect(result.success).toBe(true);
        expect(result.previousModel).toBe(from);
        expect(result.currentModel).toBe(to);
        expect(result.switchTimeMs).toBeGreaterThan(0);
        expect(result.switchTimeMs).toBeLessThan(200);
      });
    });
  });

  describe('Edge Cases', () => {
    test('should handle switching to same model (no-op)', async () => {
      const currentModel = service.modelSwitcher.getCurrentModel();

      const result = await service.changeModel(
        testQueryId,
        currentModel, // Switch to same model
        'same_model_test'
      );

      // Should still succeed, just with minimal work
      expect(result.success).toBe(true);
      expect(result.previousModel).toBe(currentModel);
      expect(result.currentModel).toBe(currentModel);
    });

    test('should handle rapid consecutive model changes', async () => {
      const results = await Promise.all([
        service.changeModel(testQueryId, ModelType.OPUS),
        service.changeModel(testQueryId, ModelType.HAIKU),
        service.changeModel(testQueryId, ModelType.SONNET)
      ]);

      // All should complete successfully
      results.forEach(result => {
        expect(result.success).toBe(true);
      });
    });

    test('should handle empty reason parameter', async () => {
      const result = await service.changeModel(testQueryId, ModelType.OPUS);

      expect(result.success).toBe(true);

      const metrics = service.telemetryService.getMetrics();
      const metric = metrics.find(m => m.operationType === 'changeModel');

      // Should have default reason or no reason
      expect(metric).toBeDefined();
    });
  });

  describe('Integration with Other Operations', () => {
    test('should allow model change after pause', async () => {
      await service.pause(testQueryId, 'test pause');

      const result = await service.changeModel(testQueryId, ModelType.OPUS);

      expect(result.success).toBe(true);
    });

    test('should maintain query state during model change', async () => {
      const stateMachine = service.stateMachines.get(testQueryId);
      const stateBefore = stateMachine?.getState();

      await service.changeModel(testQueryId, ModelType.HAIKU);

      const stateAfter = stateMachine?.getState();
      expect(stateAfter).toBe(stateBefore);
    });

    test('should create checkpoint when changing model', async () => {
      const result = await service.changeModel(testQueryId, ModelType.OPUS);

      expect(result.checkpointId).toBeDefined();
      expect(result.checkpointId).toMatch(/^checkpoint-/);
    });
  });
});
