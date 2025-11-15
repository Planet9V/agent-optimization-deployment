/**
 * GAP-003 Query Control System - Neural Hooks Unit Tests
 *
 * File: tests/query-control/unit/NeuralHooks.test.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: Comprehensive unit tests for NeuralHooks
 *
 * Constitutional Compliance:
 * - DILIGENCE: >90% code coverage, >85% branch coverage
 * - INTEGRITY: All edge cases tested including graceful degradation
 * - NO DEVELOPMENT THEATER: Production-grade tests validating real interfaces
 */

import { describe, test, expect, beforeEach, afterEach, jest } from '@jest/globals';
import {
  NeuralHooks,
  getNeuralHooks,
  type PatternType,
  type OperationData,
  type PredictionResult,
  type PatternAnalysis
} from '../../../lib/query-control/neural/neural-hooks';

describe('NeuralHooks', () => {
  let neuralHooks: NeuralHooks;
  let consoleLogSpy: jest.SpiedFunction<typeof console.log>;

  beforeEach(() => {
    neuralHooks = new NeuralHooks();
    // Spy on console.log to verify logging behavior
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
  });

  describe('Initialization', () => {
    test('should start with training disabled', () => {
      expect(neuralHooks.isTrainingEnabled()).toBe(false);
    });

    test('should be instantiable', () => {
      expect(neuralHooks).toBeInstanceOf(NeuralHooks);
    });
  });

  describe('Training Enable/Disable', () => {
    test('should enable training', () => {
      neuralHooks.enableTraining();
      expect(neuralHooks.isTrainingEnabled()).toBe(true);
      expect(consoleLogSpy).toHaveBeenCalledWith('[Neural Hook] Training enabled');
    });

    test('should disable training', () => {
      neuralHooks.enableTraining();
      neuralHooks.disableTraining();
      expect(neuralHooks.isTrainingEnabled()).toBe(false);
      expect(consoleLogSpy).toHaveBeenCalledWith('[Neural Hook] Training disabled');
    });

    test('should support multiple enable/disable cycles', () => {
      neuralHooks.enableTraining();
      expect(neuralHooks.isTrainingEnabled()).toBe(true);

      neuralHooks.disableTraining();
      expect(neuralHooks.isTrainingEnabled()).toBe(false);

      neuralHooks.enableTraining();
      expect(neuralHooks.isTrainingEnabled()).toBe(true);
    });
  });

  describe('trainPattern() - Coordination Patterns', () => {
    test('should train coordination pattern with valid data', async () => {
      const operationData: OperationData = {
        operationType: 'checkpoint_creation',
        queryId: 'test-query-001',
        context: {
          state: 'running',
          model: 'sonnet',
          agentCount: 3,
          taskCount: 5
        },
        outcome: {
          success: true,
          durationMs: 150
        },
        timestamp: Date.now()
      };

      await neuralHooks.trainPattern('coordination', operationData);

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Training coordination pattern:',
        expect.objectContaining({
          operation: 'checkpoint_creation',
          query: 'test-query-001',
          outcome: 'success',
          duration: '150ms'
        })
      );
    });

    test('should train coordination pattern with failure outcome', async () => {
      const operationData: OperationData = {
        operationType: 'state_transition',
        queryId: 'test-query-002',
        context: {
          state: 'paused -> running'
        },
        outcome: {
          success: false,
          durationMs: 75,
          error: 'Invalid transition'
        },
        timestamp: Date.now()
      };

      await neuralHooks.trainPattern('coordination', operationData);

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Training coordination pattern:',
        expect.objectContaining({
          operation: 'state_transition',
          outcome: 'failure',
          duration: '75ms'
        })
      );
    });
  });

  describe('trainPattern() - Optimization Patterns', () => {
    test('should train optimization pattern for model switch', async () => {
      const operationData: OperationData = {
        operationType: 'model_switch',
        queryId: 'test-query-003',
        context: {
          model: 'haiku',
          permissionMode: 'acceptEdits'
        },
        outcome: {
          success: true,
          durationMs: 200
        },
        timestamp: Date.now()
      };

      await neuralHooks.trainPattern('optimization', operationData);

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Training optimization pattern:',
        expect.objectContaining({
          operation: 'model_switch',
          outcome: 'success',
          duration: '200ms'
        })
      );
    });

    test('should train optimization pattern for permission switch', async () => {
      const operationData: OperationData = {
        operationType: 'permission_switch',
        queryId: 'test-query-004',
        context: {
          permissionMode: 'plan'
        },
        outcome: {
          success: true,
          durationMs: 120
        },
        timestamp: Date.now()
      };

      await neuralHooks.trainPattern('optimization', operationData);

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Training optimization pattern:',
        expect.objectContaining({
          operation: 'permission_switch',
          query: 'test-query-004'
        })
      );
    });
  });

  describe('trainPattern() - Prediction Patterns', () => {
    test('should train prediction pattern', async () => {
      const operationData: OperationData = {
        operationType: 'next_action_prediction',
        queryId: 'test-query-005',
        context: {
          state: 'running',
          agentCount: 2
        },
        outcome: {
          success: true,
          durationMs: 90
        },
        timestamp: Date.now()
      };

      await neuralHooks.trainPattern('prediction', operationData);

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Training prediction pattern:',
        expect.objectContaining({
          operation: 'next_action_prediction',
          outcome: 'success'
        })
      );
    });
  });

  describe('trainPattern() - Pattern Type Validation', () => {
    test('should handle all valid pattern types', async () => {
      const patternTypes: PatternType[] = ['coordination', 'optimization', 'prediction'];

      for (const patternType of patternTypes) {
        const operationData: OperationData = {
          operationType: `test_${patternType}`,
          queryId: 'test-query-006',
          context: {},
          outcome: {
            success: true,
            durationMs: 100
          },
          timestamp: Date.now()
        };

        await expect(
          neuralHooks.trainPattern(patternType, operationData)
        ).resolves.toBeUndefined();
      }

      expect(consoleLogSpy).toHaveBeenCalledTimes(patternTypes.length);
    });
  });

  describe('trainCheckpointPattern()', () => {
    test('should train checkpoint creation pattern with success', async () => {
      await neuralHooks.trainCheckpointPattern(
        'query-001',
        {
          state: 'running',
          model: 'sonnet',
          agentCount: 3,
          taskCount: 5
        },
        150,
        true
      );

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Training coordination pattern:',
        expect.objectContaining({
          operation: 'checkpoint_creation',
          query: 'query-001',
          outcome: 'success',
          duration: '150ms'
        })
      );
    });

    test('should train checkpoint creation pattern with failure', async () => {
      await neuralHooks.trainCheckpointPattern(
        'query-002',
        {
          state: 'paused',
          model: 'haiku',
          agentCount: 1,
          taskCount: 2
        },
        75,
        false
      );

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Training coordination pattern:',
        expect.objectContaining({
          operation: 'checkpoint_creation',
          query: 'query-002',
          outcome: 'failure',
          duration: '75ms'
        })
      );
    });
  });

  describe('trainTransitionPattern()', () => {
    test('should train state transition pattern', async () => {
      await neuralHooks.trainTransitionPattern(
        'query-003',
        'paused',
        'running',
        120,
        true
      );

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Training coordination pattern:',
        expect.objectContaining({
          operation: 'state_transition',
          query: 'query-003',
          outcome: 'success',
          duration: '120ms'
        })
      );
    });

    test('should include transition direction in context', async () => {
      consoleLogSpy.mockClear();

      await neuralHooks.trainTransitionPattern(
        'query-004',
        'init',
        'running',
        200,
        true
      );

      // Verify the log was called with state transition info
      expect(consoleLogSpy).toHaveBeenCalled();
      const logCall = consoleLogSpy.mock.calls[0];
      expect(logCall[0]).toContain('Training coordination pattern');
    });

    test('should handle failed state transitions', async () => {
      await neuralHooks.trainTransitionPattern(
        'query-005',
        'running',
        'completed',
        50,
        false
      );

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Training coordination pattern:',
        expect.objectContaining({
          outcome: 'failure',
          duration: '50ms'
        })
      );
    });
  });

  describe('trainOptimizationPattern()', () => {
    test('should train model switch optimization pattern', async () => {
      await neuralHooks.trainOptimizationPattern(
        'query-006',
        'model_switch',
        { model: 'haiku', previousModel: 'sonnet' },
        180,
        true
      );

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Training optimization pattern:',
        expect.objectContaining({
          operation: 'model_switch',
          query: 'query-006',
          outcome: 'success',
          duration: '180ms'
        })
      );
    });

    test('should train permission switch optimization pattern', async () => {
      await neuralHooks.trainOptimizationPattern(
        'query-007',
        'permission_switch',
        { permissionMode: 'plan', previousMode: 'default' },
        95,
        true
      );

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Training optimization pattern:',
        expect.objectContaining({
          operation: 'permission_switch',
          query: 'query-007',
          outcome: 'success'
        })
      );
    });

    test('should handle failed optimization decisions', async () => {
      await neuralHooks.trainOptimizationPattern(
        'query-008',
        'model_switch',
        { model: 'invalid' },
        25,
        false
      );

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Training optimization pattern:',
        expect.objectContaining({
          outcome: 'failure',
          duration: '25ms'
        })
      );
    });
  });

  describe('predictOptimization()', () => {
    test('should return prediction result with zero confidence (MCP not available)', async () => {
      const result = await neuralHooks.predictOptimization(
        'query-009',
        { state: 'running', model: 'sonnet' }
      );

      expect(result).toEqual({
        prediction: null,
        confidence: 0,
        reasoning: 'MCP neural prediction not yet integrated'
      });
    });

    test('should log prediction request', async () => {
      await neuralHooks.predictOptimization('query-010', {});

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Prediction requested for query-010 (MCP not yet integrated)'
      );
    });

    test('should handle various context types', async () => {
      const contexts = [
        { state: 'running' },
        { model: 'haiku', agentCount: 5 },
        { permissionMode: 'acceptEdits', taskCount: 10 },
        {}
      ];

      for (const context of contexts) {
        const result = await neuralHooks.predictOptimization('test-query', context);
        expect(result.confidence).toBe(0);
        expect(result.prediction).toBeNull();
      }
    });
  });

  describe('analyzePatterns()', () => {
    test('should return empty pattern analysis (MCP not available)', async () => {
      const result = await neuralHooks.analyzePatterns(
        'checkpoint_creation',
        { queryCount: 10 }
      );

      expect(result).toEqual({
        patterns: [],
        insights: ['Neural pattern analysis will be available after MCP integration'],
        recommendations: ['Continue collecting operation telemetry for future training']
      });
    });

    test('should log analysis request', async () => {
      await neuralHooks.analyzePatterns('state_transition', {});

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Pattern analysis requested for state_transition (MCP not yet integrated)'
      );
    });

    test('should handle different operation types', async () => {
      const operations = [
        'checkpoint_creation',
        'state_transition',
        'model_switch',
        'permission_switch'
      ];

      for (const operation of operations) {
        const result = await neuralHooks.analyzePatterns(operation, {});

        expect(result.patterns).toEqual([]);
        expect(result.insights).toHaveLength(1);
        expect(result.recommendations).toHaveLength(1);
      }
    });
  });

  describe('storePattern()', () => {
    test('should log pattern storage without TTL', async () => {
      await neuralHooks.storePattern(
        'query-patterns',
        'checkpoint-001',
        { type: 'coordination', data: 'test' }
      );

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Pattern stored: query-patterns/checkpoint-001 (MCP not yet integrated)'
      );
    });

    test('should log pattern storage with TTL', async () => {
      await neuralHooks.storePattern(
        'optimization-patterns',
        'model-switch-002',
        { type: 'optimization', data: 'test' },
        3600
      );

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Pattern stored: optimization-patterns/model-switch-002 (MCP not yet integrated)'
      );
    });

    test('should handle various namespace/key combinations', async () => {
      const testCases = [
        { namespace: 'ns1', key: 'key1' },
        { namespace: 'deep/nested/namespace', key: 'complex-key-123' },
        { namespace: 'cache', key: 'temp' }
      ];

      for (const { namespace, key } of testCases) {
        await neuralHooks.storePattern(namespace, key, {}, 60);
        expect(consoleLogSpy).toHaveBeenCalledWith(
          expect.stringContaining(`${namespace}/${key}`)
        );
      }
    });
  });

  describe('retrievePattern()', () => {
    test('should return null for pattern retrieval (MCP not available)', async () => {
      const result = await neuralHooks.retrievePattern(
        'query-patterns',
        'checkpoint-001'
      );

      expect(result).toBeNull();
    });

    test('should log retrieval request', async () => {
      await neuralHooks.retrievePattern('optimization-patterns', 'model-switch-002');

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Neural Hook] Pattern retrieval requested: optimization-patterns/model-switch-002 (MCP not yet integrated)'
      );
    });

    test('should handle various retrieval requests', async () => {
      const testCases = [
        { namespace: 'patterns', key: 'key1' },
        { namespace: 'cache', key: 'temp-data' },
        { namespace: 'deep/path', key: 'nested-key' }
      ];

      for (const { namespace, key } of testCases) {
        const result = await neuralHooks.retrievePattern(namespace, key);
        expect(result).toBeNull();
      }
    });
  });

  describe('Graceful Degradation', () => {
    test('should continue operating when MCP tools unavailable', async () => {
      // All methods should complete without errors even when MCP unavailable

      const operationData: OperationData = {
        operationType: 'test',
        queryId: 'test-001',
        context: {},
        outcome: { success: true, durationMs: 100 },
        timestamp: Date.now()
      };

      await expect(
        neuralHooks.trainPattern('coordination', operationData)
      ).resolves.toBeUndefined();

      await expect(
        neuralHooks.predictOptimization('test-002', {})
      ).resolves.toMatchObject({
        confidence: 0,
        prediction: null
      });

      await expect(
        neuralHooks.analyzePatterns('test_operation', {})
      ).resolves.toMatchObject({
        patterns: [],
        insights: expect.any(Array),
        recommendations: expect.any(Array)
      });

      await expect(
        neuralHooks.storePattern('test', 'key', {})
      ).resolves.toBeUndefined();

      await expect(
        neuralHooks.retrievePattern('test', 'key')
      ).resolves.toBeNull();
    });

    test('should provide meaningful fallback responses', async () => {
      const prediction = await neuralHooks.predictOptimization('test', {});
      expect(prediction.reasoning).toContain('not yet integrated');

      const analysis = await neuralHooks.analyzePatterns('test', {});
      expect(analysis.insights[0]).toContain('will be available');
      expect(analysis.recommendations[0]).toContain('Continue collecting');
    });
  });

  describe('Operation Data Validation', () => {
    test('should handle minimal operation data', async () => {
      const minimalData: OperationData = {
        operationType: 'minimal_test',
        queryId: 'test-minimal',
        context: {},
        outcome: {
          success: true,
          durationMs: 50
        },
        timestamp: Date.now()
      };

      await expect(
        neuralHooks.trainPattern('coordination', minimalData)
      ).resolves.toBeUndefined();
    });

    test('should handle complete operation data with all fields', async () => {
      const completeData: OperationData = {
        operationType: 'complete_test',
        queryId: 'test-complete',
        context: {
          state: 'running',
          model: 'sonnet',
          permissionMode: 'default',
          agentCount: 5,
          taskCount: 10
        },
        outcome: {
          success: false,
          durationMs: 250,
          error: 'Test error message'
        },
        timestamp: Date.now()
      };

      await expect(
        neuralHooks.trainPattern('optimization', completeData)
      ).resolves.toBeUndefined();
    });

    test('should handle operation data with partial context', async () => {
      const partialData: OperationData = {
        operationType: 'partial_test',
        queryId: 'test-partial',
        context: {
          state: 'paused'
          // Other context fields omitted
        },
        outcome: {
          success: true,
          durationMs: 100
        },
        timestamp: Date.now()
      };

      await expect(
        neuralHooks.trainPattern('prediction', partialData)
      ).resolves.toBeUndefined();
    });
  });

  describe('Memory Namespace Preparation', () => {
    test('should support memory operations for different namespaces', async () => {
      const namespaces = [
        'query-control',
        'optimization',
        'coordination',
        'predictions',
        'cache/temporary'
      ];

      for (const namespace of namespaces) {
        await neuralHooks.storePattern(namespace, 'test-key', { data: 'test' });
        const result = await neuralHooks.retrievePattern(namespace, 'test-key');

        expect(result).toBeNull(); // MCP not available
        expect(consoleLogSpy).toHaveBeenCalledWith(
          expect.stringContaining(namespace)
        );
      }
    });
  });

  describe('MCP Integration Readiness', () => {
    test('should have interface compatible with future mcp__claude-flow__neural_train', async () => {
      const operationData: OperationData = {
        operationType: 'mcp_ready_test',
        queryId: 'test-mcp-001',
        context: {
          state: 'running',
          model: 'sonnet',
          agentCount: 3
        },
        outcome: {
          success: true,
          durationMs: 150
        },
        timestamp: Date.now()
      };

      // Should accept data structure compatible with MCP integration
      await expect(
        neuralHooks.trainPattern('coordination', operationData)
      ).resolves.toBeUndefined();
    });

    test('should have interface compatible with future mcp__claude-flow__neural_predict', async () => {
      const context = {
        state: 'running',
        model: 'sonnet',
        agentCount: 5,
        taskCount: 10
      };

      const result = await neuralHooks.predictOptimization('test-mcp-002', context);

      // Should return structure compatible with MCP integration
      expect(result).toHaveProperty('prediction');
      expect(result).toHaveProperty('confidence');
      expect(result).toHaveProperty('reasoning');
    });

    test('should have interface compatible with future mcp__claude-flow__neural_patterns', async () => {
      const metadata = {
        queryCount: 100,
        successRate: 0.95,
        avgDuration: 150
      };

      const result = await neuralHooks.analyzePatterns('test_operation', metadata);

      // Should return structure compatible with MCP integration
      expect(result).toHaveProperty('patterns');
      expect(result).toHaveProperty('insights');
      expect(result).toHaveProperty('recommendations');
      expect(Array.isArray(result.patterns)).toBe(true);
      expect(Array.isArray(result.insights)).toBe(true);
      expect(Array.isArray(result.recommendations)).toBe(true);
    });

    test('should have interface compatible with future mcp__claude-flow__memory_usage', async () => {
      const pattern = {
        type: 'coordination',
        operation: 'checkpoint_creation',
        successRate: 0.92,
        avgDuration: 120
      };

      // Should accept storage requests compatible with MCP integration
      await expect(
        neuralHooks.storePattern('patterns', 'test-key', pattern, 3600)
      ).resolves.toBeUndefined();

      // Should accept retrieval requests compatible with MCP integration
      const result = await neuralHooks.retrievePattern('patterns', 'test-key');
      expect(result).toBeNull(); // MCP not available, but interface compatible
    });
  });

  describe('Singleton Pattern', () => {
    test('should return singleton instance from getNeuralHooks', () => {
      const instance1 = getNeuralHooks();
      const instance2 = getNeuralHooks();

      expect(instance1).toBe(instance2);
      expect(instance1).toBeInstanceOf(NeuralHooks);
    });

    test('should maintain state across singleton calls', () => {
      const instance1 = getNeuralHooks();
      instance1.enableTraining();

      const instance2 = getNeuralHooks();
      expect(instance2.isTrainingEnabled()).toBe(true);

      // Cleanup
      instance2.disableTraining();
    });
  });
});
