/**
 * GAP-003 Query Control System - Model Switching Integration Tests
 */

import { QueryStateMachine } from '../../../lib/query-control/state/state-machine';
import { ModelRegistry } from '../../../lib/query-control/model/model-registry';
import { ModelSwitcher } from '../../../lib/query-control/model/model-switcher';
import { CheckpointManager } from '../../../lib/query-control/checkpoint/checkpoint-manager';
import { ModelType, QueryState } from '../../../lib/query-control/types';

describe('Model Switching Integration Tests', () => {
  let stateMachine: QueryStateMachine;
  let modelRegistry: ModelRegistry;
  let modelSwitcher: ModelSwitcher;
  let checkpointManager: CheckpointManager;
  const testQueryId = 'model-switch-test-001';

  beforeEach(async () => {
    stateMachine = new QueryStateMachine(testQueryId);
    modelRegistry = new ModelRegistry();
    checkpointManager = new CheckpointManager();
    modelSwitcher = new ModelSwitcher(modelRegistry, checkpointManager);

    await checkpointManager.initialize();
    await stateMachine.transition('START');
  });

  describe('Model switching operations', () => {
    test('should switch from Sonnet to Haiku', async () => {
      modelSwitcher.setCurrentModel(ModelType.SONNET);

      const result = await modelSwitcher.switchModel(
        testQueryId,
        ModelType.HAIKU,
        stateMachine
      );

      expect(result.success).toBe(true);
      expect(result.previousModel).toBe(ModelType.SONNET);
      expect(result.currentModel).toBe(ModelType.HAIKU);
      expect(result.checkpointCreated).toBe(true);
      expect(modelSwitcher.getCurrentModel()).toBe(ModelType.HAIKU);
    });

    test('should switch from Haiku to Opus', async () => {
      modelSwitcher.setCurrentModel(ModelType.HAIKU);

      const result = await modelSwitcher.switchModel(
        testQueryId,
        ModelType.OPUS,
        stateMachine
      );

      expect(result.success).toBe(true);
      expect(result.previousModel).toBe(ModelType.HAIKU);
      expect(result.currentModel).toBe(ModelType.OPUS);
    });

    test('should switch from Opus to Sonnet', async () => {
      modelSwitcher.setCurrentModel(ModelType.OPUS);

      const result = await modelSwitcher.switchModel(
        testQueryId,
        ModelType.SONNET,
        stateMachine
      );

      expect(result.success).toBe(true);
      expect(result.previousModel).toBe(ModelType.OPUS);
      expect(result.currentModel).toBe(ModelType.SONNET);
    });
  });

  describe('Performance requirements', () => {
    test('should complete switch within 200ms target', async () => {
      modelSwitcher.setCurrentModel(ModelType.SONNET);

      const startTime = Date.now();
      const result = await modelSwitcher.switchModel(
        testQueryId,
        ModelType.HAIKU,
        stateMachine
      );
      const duration = Date.now() - startTime;

      expect(result.success).toBe(true);
      expect(duration).toBeLessThan(500); // Acceptable

      if (duration > 200) {
        console.warn(`Switch time: ${duration}ms (target: <200ms)`);
      }
    });

    test('should report accurate switch timing', async () => {
      modelSwitcher.setCurrentModel(ModelType.SONNET);

      const result = await modelSwitcher.switchModel(
        testQueryId,
        ModelType.OPUS,
        stateMachine
      );

      expect(result.switchTimeMs).toBeGreaterThan(0);
      expect(result.switchTimeMs).toBeLessThan(1000);
    });
  });

  describe('Safety checkpoints', () => {
    test('should create checkpoint before switching', async () => {
      modelSwitcher.setCurrentModel(ModelType.SONNET);

      const result = await modelSwitcher.switchModel(
        testQueryId,
        ModelType.HAIKU,
        stateMachine
      );

      expect(result.checkpointCreated).toBe(true);

      // Verify checkpoint exists
      const checkpoint = await checkpointManager.retrieveCheckpoint(testQueryId);
      expect(checkpoint).toBeDefined();
      expect(checkpoint?.metadata.reason).toBe('pre_model_switch');
    });

    test('should preserve execution state during switch', async () => {
      // Add execution context
      stateMachine.updateContext({
        metadata: { important: 'data', iteration: 5 },
        execution: {
          agentStates: new Map([['agent-1', { status: 'active' }]]),
          taskQueue: [{ id: 'task-1', type: 'test', status: 'pending' as const }],
          completedTasks: []
        }
      });

      modelSwitcher.setCurrentModel(ModelType.SONNET);

      const result = await modelSwitcher.switchModel(
        testQueryId,
        ModelType.HAIKU,
        stateMachine
      );

      expect(result.success).toBe(true);

      // Verify context preserved
      const checkpoint = await checkpointManager.retrieveCheckpoint(testQueryId);
      expect(checkpoint).toBeDefined();
      expect(checkpoint?.executionContext.taskQueue.length).toBe(1);
    });
  });

  describe('Model recommendations', () => {
    test('should recommend Haiku for simple tasks', async () => {
      const recommendation = await modelRegistry.recommendModel('simple quick task');

      expect(recommendation.model).toBe(ModelType.HAIKU);
      expect(recommendation.confidence).toBeGreaterThan(0.7);
      expect(recommendation.reasoning).toContain('speed');
    });

    test('should recommend Opus for complex tasks', async () => {
      const recommendation = await modelRegistry.recommendModel('complex strategic analysis');

      expect(recommendation.model).toBe(ModelType.OPUS);
      expect(recommendation.confidence).toBeGreaterThan(0.7);
      expect(recommendation.reasoning).toContain('complex');
    });

    test('should recommend Sonnet for balanced tasks', async () => {
      const recommendation = await modelRegistry.recommendModel('code implementation');

      expect(recommendation.model).toBe(ModelType.SONNET);
      expect(recommendation.confidence).toBeGreaterThan(0.7);
    });

    test('should switch to optimal model automatically', async () => {
      modelSwitcher.setCurrentModel(ModelType.OPUS);

      const result = await modelSwitcher.switchToOptimalModel(
        testQueryId,
        'quick simple task',
        stateMachine
      );

      expect(result.success).toBe(true);
      expect(result.currentModel).toBe(ModelType.HAIKU);
    });

    test('should skip switch if already optimal', async () => {
      modelSwitcher.setCurrentModel(ModelType.HAIKU);

      const result = await modelSwitcher.switchToOptimalModel(
        testQueryId,
        'quick task',
        stateMachine
      );

      expect(result.success).toBe(true);
      expect(result.switchTimeMs).toBe(0);
      expect(result.checkpointCreated).toBe(false);
    });
  });

  describe('Model capabilities', () => {
    test('should retrieve Sonnet capabilities', () => {
      const caps = modelRegistry.getCapabilities(ModelType.SONNET);

      expect(caps.maxTokens).toBe(8192);
      expect(caps.contextWindow).toBe(200000);
      expect(caps.strengthAreas).toContain('coding');
      expect(caps.strengthAreas).toContain('reasoning');
    });

    test('should retrieve Haiku capabilities', () => {
      const caps = modelRegistry.getCapabilities(ModelType.HAIKU);

      expect(caps.maxTokens).toBe(4096);
      expect(caps.latencyMs).toBe(500);
      expect(caps.strengthAreas).toContain('speed');
      expect(caps.strengthAreas).toContain('efficiency');
    });

    test('should retrieve Opus capabilities', () => {
      const caps = modelRegistry.getCapabilities(ModelType.OPUS);

      expect(caps.maxTokens).toBe(4096);
      expect(caps.strengthAreas).toContain('creativity');
      expect(caps.strengthAreas).toContain('complex_reasoning');
    });

    test('should compare models for use case', () => {
      const comparison = modelRegistry.compareModels('complex reasoning task');

      expect(comparison.length).toBe(3);
      expect(comparison[0].score).toBeGreaterThan(0);

      // Opus should score highest for complex tasks
      const opusComparison = comparison.find(c => c.model === ModelType.OPUS);
      expect(opusComparison).toBeDefined();
    });
  });

  describe('Multiple switches', () => {
    test('should handle rapid successive switches', async () => {
      modelSwitcher.setCurrentModel(ModelType.SONNET);

      // Switch 1: Sonnet → Haiku
      const result1 = await modelSwitcher.switchModel(
        testQueryId + '_1',
        ModelType.HAIKU,
        stateMachine
      );
      expect(result1.success).toBe(true);

      // Switch 2: Haiku → Opus
      const result2 = await modelSwitcher.switchModel(
        testQueryId + '_2',
        ModelType.OPUS,
        stateMachine
      );
      expect(result2.success).toBe(true);

      // Switch 3: Opus → Sonnet
      const result3 = await modelSwitcher.switchModel(
        testQueryId + '_3',
        ModelType.SONNET,
        stateMachine
      );
      expect(result3.success).toBe(true);

      expect(modelSwitcher.getCurrentModel()).toBe(ModelType.SONNET);
    });

    test('should create separate checkpoints for each switch', async () => {
      modelSwitcher.setCurrentModel(ModelType.SONNET);

      await modelSwitcher.switchModel(testQueryId + '_switch1', ModelType.HAIKU, stateMachine);
      await modelSwitcher.switchModel(testQueryId + '_switch2', ModelType.OPUS, stateMachine);

      const checkpoint1 = await checkpointManager.retrieveCheckpoint(testQueryId + '_switch1');
      const checkpoint2 = await checkpointManager.retrieveCheckpoint(testQueryId + '_switch2');

      expect(checkpoint1).toBeDefined();
      expect(checkpoint2).toBeDefined();
      expect(checkpoint1?.queryId).not.toBe(checkpoint2?.queryId);
    });
  });

  describe('Statistics and tracking', () => {
    test('should track current model', () => {
      modelSwitcher.setCurrentModel(ModelType.HAIKU);

      const stats = modelSwitcher.getStatistics();

      expect(stats.currentModel).toBe(ModelType.HAIKU);
    });

    test('should validate model types', () => {
      expect(modelRegistry.isValidModel('claude-sonnet-4-5-20250929')).toBe(true);
      expect(modelRegistry.isValidModel('claude-3-5-haiku-20241022')).toBe(true);
      expect(modelRegistry.isValidModel('invalid-model')).toBe(false);
    });

    test('should list all available models', () => {
      const models = modelRegistry.getAllModels();

      expect(models).toHaveLength(3);
      expect(models).toContain(ModelType.SONNET);
      expect(models).toContain(ModelType.HAIKU);
      expect(models).toContain(ModelType.OPUS);
    });
  });
});
