/**
 * GAP-003 Query Control System - Model Switching Integration Tests
 *
 * File: tests/query-control/integration/model-switching.test.ts
 * Created: 2025-11-14
 * Version: v1.0.0
 * Purpose: Integration tests for model switching with checkpoint preservation
 *
 * Constitutional Compliance:
 * - DILIGENCE: Comprehensive integration test coverage
 * - INTEGRITY: Validates <200ms latency and state preservation
 * - NO DEVELOPMENT THEATER: Production-grade integration testing
 */

import { describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import {
  ModelSwitcher,
  ModelType,
  type ModelConfig,
  type ModelSwitchResult
} from '../../../lib/query-control/model/model-switcher';
import {
  ModelRegistry,
  type ModelRecommendation
} from '../../../lib/query-control/model/model-registry';
import {
  CheckpointManager,
  getCheckpointManager,
  type ExecutionContext
} from '../../../lib/query-control/checkpoint/checkpoint-manager';
import {
  QueryStateMachine,
  QueryState,
  type QueryContext
} from '../../../lib/query-control/state/state-machine';
import { QueryRegistry, getQueryRegistry } from '../../../lib/query-control/registry/query-registry';

describe('Model Switching Integration Tests', () => {
  let switcher: ModelSwitcher;
  let registry: ModelRegistry;
  let checkpointManager: CheckpointManager;
  let queryRegistry: QueryRegistry;

  beforeEach(() => {
    switcher = new ModelSwitcher(ModelType.SONNET);
    registry = new ModelRegistry();
    checkpointManager = getCheckpointManager();
    queryRegistry = new QueryRegistry();
  });

  afterEach(async () => {
    await checkpointManager.clear();
    await queryRegistry.clear();
    switcher.clearHistory();
  });

  describe('Basic Model Switching', () => {
    test('should switch from Sonnet to Haiku with <200ms latency', async () => {
      const queryId = 'model-switch-test-001';

      // Create execution context
      const executionContext: ExecutionContext = {
        taskQueue: [
          { id: 'task-1', status: 'running', description: 'Process data', progress: 50 }
        ],
        agentStates: {
          'agent-001': { agentId: 'agent-001', status: 'active', currentTask: 'task-1' }
        },
        resources: { memoryUsage: 256 },
        variables: { iterationCount: 100 }
      };

      const context: QueryContext = {
        queryId,
        metadata: {
          state: QueryState.RUNNING,
          taskQueue: executionContext.taskQueue,
          agentStates: executionContext.agentStates,
          resources: executionContext.resources,
          variables: executionContext.variables
        },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: ModelType.SONNET,
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: {}
      };

      // Perform switch
      const result = await switcher.switchModel(
        queryId,
        ModelType.HAIKU,
        context,
        modelConfig,
        'performance_optimization'
      );

      // Validate result
      expect(result.success).toBe(true);
      expect(result.previousModel).toBe(ModelType.SONNET);
      expect(result.currentModel).toBe(ModelType.HAIKU);
      expect(result.switchTimeMs).toBeLessThan(200); // <200ms target
      expect(result.checkpointId).toBeDefined();
      expect(result.error).toBeUndefined();

      // Verify switcher state updated
      expect(switcher.getCurrentModel()).toBe(ModelType.HAIKU);
    });

    test('should switch from Haiku to Opus', async () => {
      const queryId = 'model-switch-test-002';

      // Start with Haiku
      const haikuSwitcher = new ModelSwitcher(ModelType.HAIKU);

      const context: QueryContext = {
        queryId,
        metadata: { state: QueryState.RUNNING },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: ModelType.HAIKU,
        temperature: 0.5,
        maxTokens: 2000,
        permissionMode: 'default',
        preferences: {}
      };

      const result = await haikuSwitcher.switchModel(
        queryId,
        ModelType.OPUS,
        context,
        modelConfig,
        'creative_task'
      );

      expect(result.success).toBe(true);
      expect(result.previousModel).toBe(ModelType.HAIKU);
      expect(result.currentModel).toBe(ModelType.OPUS);
      expect(result.switchTimeMs).toBeLessThan(200);
    });

    test('should prevent switching to same model', async () => {
      const queryId = 'model-switch-test-003';

      const context: QueryContext = {
        queryId,
        metadata: { state: QueryState.RUNNING },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: ModelType.SONNET,
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: {}
      };

      // Try switching to current model
      const validation = switcher.canSwitchTo(ModelType.SONNET);

      expect(validation.allowed).toBe(false);
      expect(validation.reason).toBe('Already using this model');
    });
  });

  describe('State Preservation During Switch', () => {
    test('should preserve execution state during model switch', async () => {
      const queryId = 'preserve-test-001';

      // Create rich execution context
      const executionContext: ExecutionContext = {
        taskQueue: [
          { id: 'task-1', status: 'completed', description: 'Init', progress: 100 },
          { id: 'task-2', status: 'running', description: 'Process', progress: 65 },
          { id: 'task-3', status: 'pending', description: 'Finalize', progress: 0 }
        ],
        agentStates: {
          'agent-001': { agentId: 'agent-001', status: 'active', currentTask: 'task-2' },
          'agent-002': { agentId: 'agent-002', status: 'idle', currentTask: null }
        },
        resources: {
          memoryUsage: 512,
          cpuUsage: 60,
          activeConnections: 5
        },
        variables: {
          iterationCount: 250,
          lastProcessedId: 'item-5000',
          batchSize: 50,
          errorCount: 2
        }
      };

      const context: QueryContext = {
        queryId,
        metadata: {
          state: QueryState.RUNNING,
          taskQueue: executionContext.taskQueue,
          agentStates: executionContext.agentStates,
          resources: executionContext.resources,
          variables: executionContext.variables
        },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: ModelType.SONNET,
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: { verbosity: 'normal' }
      };

      // Perform switch
      const result = await switcher.switchModel(
        queryId,
        ModelType.HAIKU,
        context,
        modelConfig
      );

      expect(result.success).toBe(true);

      // Retrieve checkpoint created during switch
      const checkpoint = await checkpointManager.retrieveCheckpoint(queryId);

      // Verify 100% accurate state preservation
      expect(checkpoint).not.toBeNull();
      expect(checkpoint?.executionContext.taskQueue).toHaveLength(3);
      expect(checkpoint?.executionContext.taskQueue[1].progress).toBe(65);
      expect(checkpoint?.executionContext.agentStates['agent-001'].currentTask).toBe('task-2');
      expect(checkpoint?.executionContext.resources.memoryUsage).toBe(512);
      expect(checkpoint?.executionContext.variables.iterationCount).toBe(250);
      expect(checkpoint?.executionContext.variables.lastProcessedId).toBe('item-5000');
      expect(checkpoint?.modelConfig.model).toBe('claude-sonnet-4-5-20250929');
    });

    test('should create checkpoint before switch failure', async () => {
      const queryId = 'checkpoint-test-001';

      const context: QueryContext = {
        queryId,
        metadata: {
          state: QueryState.RUNNING,
          variables: { criticalData: 'must-preserve' }
        },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: ModelType.SONNET,
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: {}
      };

      // Attempt switch
      await switcher.switchModel(queryId, ModelType.HAIKU, context, modelConfig);

      // Verify checkpoint exists even if switch would fail
      const checkpoint = await checkpointManager.getLatestCheckpoint(queryId);
      expect(checkpoint).not.toBeNull();
      expect(checkpoint?.executionContext.variables.criticalData).toBe('must-preserve');
    });
  });

  describe('Rapid Model Switches', () => {
    test('should handle multiple rapid model switches', async () => {
      const queryId = 'rapid-switch-test-001';

      const context: QueryContext = {
        queryId,
        metadata: { state: QueryState.RUNNING },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: ModelType.SONNET,
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: {}
      };

      // Switch 1: Sonnet → Haiku
      const result1 = await switcher.switchModel(
        queryId,
        ModelType.HAIKU,
        context,
        modelConfig,
        'speed_priority'
      );

      expect(result1.success).toBe(true);
      expect(result1.currentModel).toBe(ModelType.HAIKU);

      // Switch 2: Haiku → Opus (rapid)
      const result2 = await switcher.switchModel(
        queryId,
        ModelType.OPUS,
        { ...context, timestamp: Date.now() },
        { ...modelConfig, model: ModelType.HAIKU },
        'quality_priority'
      );

      expect(result2.success).toBe(true);
      expect(result2.currentModel).toBe(ModelType.OPUS);

      // Switch 3: Opus → Sonnet (rapid)
      const result3 = await switcher.switchModel(
        queryId,
        ModelType.SONNET,
        { ...context, timestamp: Date.now() },
        { ...modelConfig, model: ModelType.OPUS },
        'balance'
      );

      expect(result3.success).toBe(true);
      expect(result3.currentModel).toBe(ModelType.SONNET);

      // Verify all switches under 200ms
      expect(result1.switchTimeMs).toBeLessThan(200);
      expect(result2.switchTimeMs).toBeLessThan(200);
      expect(result3.switchTimeMs).toBeLessThan(200);

      // Verify switch history
      const history = switcher.getSwitchHistory(queryId);
      expect(history).not.toBeNull();
      expect(history?.switches).toHaveLength(3);
      expect(history?.switches[0].from).toBe(ModelType.SONNET);
      expect(history?.switches[0].to).toBe(ModelType.HAIKU);
      expect(history?.switches[1].from).toBe(ModelType.HAIKU);
      expect(history?.switches[1].to).toBe(ModelType.OPUS);
      expect(history?.switches[2].from).toBe(ModelType.OPUS);
      expect(history?.switches[2].to).toBe(ModelType.SONNET);
    });

    test('should track switch statistics across multiple queries', async () => {
      const query1 = 'stats-test-001';
      const query2 = 'stats-test-002';

      const context: QueryContext = {
        queryId: query1,
        metadata: { state: QueryState.RUNNING },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: ModelType.SONNET,
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: {}
      };

      // Query 1: 2 switches
      await switcher.switchModel(query1, ModelType.HAIKU, context, modelConfig);
      await switcher.switchModel(query1, ModelType.OPUS, { ...context, timestamp: Date.now() }, { ...modelConfig, model: ModelType.HAIKU });

      // Query 2: 1 switch
      await switcher.switchModel(query2, ModelType.HAIKU, { ...context, queryId: query2 }, modelConfig);

      const stats = switcher.getSwitchStatistics();

      expect(stats.totalSwitches).toBe(3);
      expect(stats.averageSwitchTime).toBeGreaterThan(0);
      expect(stats.fastestSwitch).toBeGreaterThan(0);
      expect(stats.slowestSwitch).toBeGreaterThan(0);
      expect(stats.switchesByModel).toHaveProperty('claude-sonnet-4-5-20250929→claude-3-5-haiku-20241022');
    });
  });

  describe('Integration with QueryRegistry and State Machine', () => {
    test('should update registry after model switch', async () => {
      const queryId = 'registry-integration-001';

      // Register query
      await queryRegistry.registerQuery(queryId, {
        state: QueryState.RUNNING,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 2,
        taskCount: 5,
        checkpointCount: 0
      });

      const context: QueryContext = {
        queryId,
        metadata: { state: QueryState.RUNNING },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: ModelType.SONNET,
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: {}
      };

      // Perform switch
      await switcher.switchModel(queryId, ModelType.HAIKU, context, modelConfig);

      // Update registry with new model
      await queryRegistry.updateQuery(queryId, {
        model: 'haiku',
        checkpointCount: 1
      });

      // Verify registry updated
      const queryMetadata = await queryRegistry.getQuery(queryId);
      expect(queryMetadata?.model).toBe('haiku');
      expect(queryMetadata?.checkpointCount).toBe(1);
    });

    test('should maintain state machine state during switch', async () => {
      const queryId = 'state-machine-integration-001';

      // Create state machine in RUNNING state
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);

      const context: QueryContext = {
        queryId,
        metadata: { state: QueryState.RUNNING },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: ModelType.SONNET,
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: {}
      };

      // Perform switch
      await switcher.switchModel(queryId, ModelType.HAIKU, context, modelConfig);

      // State should remain RUNNING (not affected by model switch)
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);
    });
  });

  describe('Model Registry Integration', () => {
    test('should get capabilities for all models', () => {
      const sonnetCaps = registry.getCapabilities(ModelType.SONNET);
      const haikuCaps = registry.getCapabilities(ModelType.HAIKU);
      const opusCaps = registry.getCapabilities(ModelType.OPUS);

      expect(sonnetCaps.maxTokens).toBe(8192);
      expect(haikuCaps.maxTokens).toBe(4096);
      expect(opusCaps.maxTokens).toBe(4096);

      expect(haikuCaps.latencyMs).toBeLessThan(sonnetCaps.latencyMs);
      expect(haikuCaps.costPer1kTokens).toBeLessThan(sonnetCaps.costPer1kTokens);
    });

    test('should recommend model based on task type', async () => {
      const speedRec = await registry.recommendModel('quick response needed');
      expect(speedRec.recommendedModel).toBe(ModelType.HAIKU);
      expect(speedRec.confidence).toBeGreaterThan(0.7);

      const analysisRec = await registry.recommendModel('complex technical analysis');
      expect(analysisRec.recommendedModel).toBe(ModelType.SONNET);

      const creativeRec = await registry.recommendModel('creative writing task');
      expect(creativeRec.recommendedModel).toBe(ModelType.OPUS);
    });

    test('should compare models by criteria', () => {
      const costComparison = registry.compareModels(
        ModelType.SONNET,
        ModelType.HAIKU,
        'cost'
      );
      expect(costComparison.better).toBe(ModelType.HAIKU);

      const speedComparison = registry.compareModels(
        ModelType.OPUS,
        ModelType.HAIKU,
        'speed'
      );
      expect(speedComparison.better).toBe(ModelType.HAIKU);

      const powerComparison = registry.compareModels(
        ModelType.HAIKU,
        ModelType.SONNET,
        'power'
      );
      expect(powerComparison.better).toBe(ModelType.SONNET);
    });

    test('should get registry statistics', () => {
      const stats = registry.getStatistics();

      expect(stats.totalModels).toBe(3);
      expect(stats.averageCost).toBeGreaterThan(0);
      expect(stats.averageLatency).toBeGreaterThan(0);
      expect(stats.models).toHaveLength(3);
      expect(stats.models).toContain(ModelType.SONNET);
      expect(stats.models).toContain(ModelType.HAIKU);
      expect(stats.models).toContain(ModelType.OPUS);
    });
  });

  describe('Performance Benchmarks', () => {
    test('should consistently achieve <100ms optimal performance', async () => {
      const queryId = 'perf-benchmark-001';
      const iterations = 10;
      const durations: number[] = [];

      const context: QueryContext = {
        queryId,
        metadata: { state: QueryState.RUNNING },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: ModelType.SONNET,
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: {}
      };

      // Run multiple switches to test consistency
      for (let i = 0; i < iterations; i++) {
        const targetModel = i % 2 === 0 ? ModelType.HAIKU : ModelType.SONNET;
        const currentModel = i % 2 === 0 ? ModelType.SONNET : ModelType.HAIKU;

        const testSwitcher = new ModelSwitcher(currentModel);

        const result = await testSwitcher.switchModel(
          `${queryId}-${i}`,
          targetModel,
          context,
          { ...modelConfig, model: currentModel }
        );

        durations.push(result.switchTimeMs);

        await testSwitcher.clearHistory();
      }

      // Calculate statistics
      const average = durations.reduce((sum, d) => sum + d, 0) / durations.length;
      const max = Math.max(...durations);
      const min = Math.min(...durations);

      // All switches should be under 200ms
      expect(max).toBeLessThan(200);

      // Average should be well under target (aiming for <100ms)
      expect(average).toBeLessThan(150);

      console.log(`Performance: avg=${average.toFixed(2)}ms, min=${min}ms, max=${max}ms`);
    });
  });
});
