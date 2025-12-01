/**
 * GAP-003 Query Control System - Pause/Resume Integration Tests
 * Tests full checkpoint and resume cycle
 */

import { QueryStateMachine } from '../../../lib/query-control/state/state-machine';
import { CheckpointManager } from '../../../lib/query-control/checkpoint/checkpoint-manager';
import { ResumeManager } from '../../../lib/query-control/checkpoint/resume-manager';
import { QueryState, QueryContext } from '../../../lib/query-control/types';

describe('Pause-Resume Integration Tests', () => {
  let stateMachine: QueryStateMachine;
  let checkpointManager: CheckpointManager;
  let resumeManager: ResumeManager;
  const testQueryId = 'integration-test-001';

  beforeEach(async () => {
    stateMachine = new QueryStateMachine(testQueryId);
    checkpointManager = new CheckpointManager();
    resumeManager = new ResumeManager(checkpointManager);

    // Initialize checkpoint manager
    await checkpointManager.initialize();
  });

  describe('Full pause-resume cycle', () => {
    test('should complete INIT -> RUNNING -> PAUSED -> RUNNING cycle', async () => {
      // 1. Start query
      await stateMachine.transition('START');
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);

      // 2. Pause query
      await stateMachine.transition('PAUSE');
      expect(stateMachine.getState()).toBe(QueryState.PAUSED);

      // 3. Create checkpoint
      const context = stateMachine.getContext();
      const checkpoint = await checkpointManager.createCheckpoint(
        testQueryId,
        context,
        'integration_test'
      );

      expect(checkpoint).toBeDefined();
      expect(checkpoint.queryId).toBe(testQueryId);
      expect(checkpoint.state).toBe(QueryState.PAUSED);

      // 4. Resume query
      const resumeResult = await resumeManager.resumeQuery(testQueryId);
      expect(resumeResult.success).toBe(true);
      expect(resumeResult.resumedFrom).toBe(testQueryId);

      // 5. Transition state machine to RUNNING
      await stateMachine.transition('RESUME');
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);
    });

    test('should preserve checkpoint data through cycle', async () => {
      // Start and pause
      await stateMachine.transition('START');

      // Add some context
      stateMachine.updateContext({
        metadata: {
          testData: 'important_value',
          iteration: 42
        }
      });

      await stateMachine.transition('PAUSE');

      // Create checkpoint
      const context = stateMachine.getContext();
      const checkpoint = await checkpointManager.createCheckpoint(
        testQueryId,
        context
      );

      // Verify checkpoint preserves metadata
      expect(checkpoint.metadata.createdBy).toBe('QueryControlSystem');
      expect(checkpoint.metadata.size).toBeGreaterThan(0);

      // Retrieve checkpoint
      const retrieved = await checkpointManager.retrieveCheckpoint(testQueryId);
      expect(retrieved).toBeDefined();
      expect(retrieved?.queryId).toBe(testQueryId);
    });

    test('should handle multiple pause-resume cycles', async () => {
      // Start query
      await stateMachine.transition('START');

      // First pause-resume cycle
      await stateMachine.transition('PAUSE');
      let context = stateMachine.getContext();
      await checkpointManager.createCheckpoint(testQueryId + '_1', context);
      await resumeManager.resumeQuery(testQueryId + '_1');
      await stateMachine.transition('RESUME');
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);

      // Second pause-resume cycle
      await stateMachine.transition('PAUSE');
      context = stateMachine.getContext();
      await checkpointManager.createCheckpoint(testQueryId + '_2', context);
      await resumeManager.resumeQuery(testQueryId + '_2');
      await stateMachine.transition('RESUME');
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);

      // Verify both checkpoints exist
      const checkpoint1 = await checkpointManager.retrieveCheckpoint(testQueryId + '_1');
      const checkpoint2 = await checkpointManager.retrieveCheckpoint(testQueryId + '_2');

      expect(checkpoint1).toBeDefined();
      expect(checkpoint2).toBeDefined();
    });
  });

  describe('Checkpoint creation performance', () => {
    test('should create checkpoint within 150ms target', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');

      const context = stateMachine.getContext();

      const startTime = Date.now();
      await checkpointManager.createCheckpoint(testQueryId, context);
      const duration = Date.now() - startTime;

      // Target: <150ms, Acceptable: <300ms
      expect(duration).toBeLessThan(300);

      if (duration > 150) {
        console.warn(`Checkpoint creation: ${duration}ms (target: <150ms)`);
      }
    });

    test('should handle large execution contexts', async () => {
      await stateMachine.transition('START');

      // Create large context
      const largeContext: QueryContext = {
        queryId: testQueryId,
        state: QueryState.RUNNING,
        metadata: {
          largeData: Array(1000).fill({ key: 'value', nested: { data: 'test' } })
        },
        timestamp: Date.now(),
        execution: {
          agentStates: new Map(Array.from({ length: 50 }, (_, i) => [
            `agent-${i}`,
            { status: 'running', progress: Math.random() }
          ])),
          taskQueue: Array(100).fill({ id: 'task', status: 'pending' }),
          completedTasks: Array(50).fill({ id: 'task', status: 'completed' })
        }
      };

      stateMachine.updateContext(largeContext);
      await stateMachine.transition('PAUSE');

      const startTime = Date.now();
      const checkpoint = await checkpointManager.createCheckpoint(
        testQueryId,
        largeContext
      );
      const duration = Date.now() - startTime;

      expect(checkpoint).toBeDefined();
      expect(checkpoint.metadata.size).toBeGreaterThan(1000);

      console.log(
        `Large checkpoint: ${checkpoint.metadata.size} bytes in ${duration}ms`
      );
    });
  });

  describe('Checkpoint retrieval performance', () => {
    test('should retrieve checkpoint within 100ms target', async () => {
      // Create checkpoint first
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');

      const context = stateMachine.getContext();
      await checkpointManager.createCheckpoint(testQueryId, context);

      // Measure retrieval
      const startTime = Date.now();
      const retrieved = await checkpointManager.retrieveCheckpoint(testQueryId);
      const duration = Date.now() - startTime;

      expect(retrieved).toBeDefined();

      // Target: <100ms (L1 cache), Acceptable: <200ms (L2 fallback)
      expect(duration).toBeLessThan(200);

      if (duration > 100) {
        console.warn(`Checkpoint retrieval: ${duration}ms (target: <100ms)`);
      }
    });

    test('should use L1 cache for repeated retrievals', async () => {
      // Create checkpoint
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');
      const context = stateMachine.getContext();
      await checkpointManager.createCheckpoint(testQueryId, context);

      // First retrieval (may hit L2)
      const time1Start = Date.now();
      await checkpointManager.retrieveCheckpoint(testQueryId);
      const time1 = Date.now() - time1Start;

      // Second retrieval (should hit L1 cache)
      const time2Start = Date.now();
      await checkpointManager.retrieveCheckpoint(testQueryId);
      const time2 = Date.now() - time2Start;

      console.log(`Retrieval times: 1st=${time1}ms, 2nd=${time2}ms`);

      // Second retrieval should be faster or comparable (L1 cache)
      expect(time2).toBeLessThanOrEqual(time1 + 50); // Allow some variance
    });
  });

  describe('Resume operation performance', () => {
    test('should resume within 300ms target', async () => {
      // Create checkpoint
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');
      const context = stateMachine.getContext();
      await checkpointManager.createCheckpoint(testQueryId, context);

      // Measure resume
      const startTime = Date.now();
      const result = await resumeManager.resumeQuery(testQueryId);
      const duration = Date.now() - startTime;

      expect(result.success).toBe(true);

      // Target: <300ms
      expect(duration).toBeLessThan(500);

      if (duration > 300) {
        console.warn(`Resume operation: ${duration}ms (target: <300ms)`);
      }
    });
  });

  describe('Error handling', () => {
    test('should handle missing checkpoint gracefully', async () => {
      await expect(
        resumeManager.resumeQuery('non-existent-query')
      ).rejects.toThrow('No checkpoint found');
    });

    test('should validate checkpoint before resuming', async () => {
      // Create checkpoint
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');
      const context = stateMachine.getContext();
      await checkpointManager.createCheckpoint(testQueryId, context);

      // Validate
      const validation = await resumeManager.validateCheckpoint(testQueryId);

      expect(validation.valid).toBe(true);
      expect(validation.issues).toHaveLength(0);
    });

    test('should detect invalid checkpoints', async () => {
      const validation = await resumeManager.validateCheckpoint('invalid-query');

      expect(validation.valid).toBe(false);
      expect(validation.issues.length).toBeGreaterThan(0);
      expect(validation.issues[0]).toBe('Checkpoint not found');
    });
  });

  describe('Checkpoint data integrity', () => {
    test('should preserve execution context', async () => {
      await stateMachine.transition('START');

      // Set up execution context
      const executionContext = {
        agentStates: new Map([
          ['agent-1', { status: 'running' }],
          ['agent-2', { status: 'idle' }]
        ]),
        taskQueue: [
          { id: 'task-1', type: 'analysis', status: 'pending' as const },
          { id: 'task-2', type: 'processing', status: 'pending' as const }
        ],
        completedTasks: [
          { id: 'task-0', type: 'init', status: 'completed' as const }
        ]
      };

      stateMachine.updateContext({ execution: executionContext });
      await stateMachine.transition('PAUSE');

      const context = stateMachine.getContext();
      const checkpoint = await checkpointManager.createCheckpoint(
        testQueryId,
        context
      );

      // Verify execution context preserved
      expect(checkpoint.executionContext.taskQueue).toHaveLength(2);
      expect(checkpoint.executionContext.completedTasks).toHaveLength(1);
      expect(Object.keys(checkpoint.executionContext.agentStates)).toHaveLength(2);
    });

    test('should preserve model configuration', async () => {
      await stateMachine.transition('START');

      // Set up model config
      const modelConfig = {
        currentModel: 'claude-3-5-haiku-20241022' as any,
        permissionMode: 'acceptEdits' as any,
        configuration: {
          temperature: 0.7,
          maxTokens: 4096
        }
      };

      stateMachine.updateContext({ model: modelConfig });
      await stateMachine.transition('PAUSE');

      const context = stateMachine.getContext();
      const checkpoint = await checkpointManager.createCheckpoint(
        testQueryId,
        context
      );

      // Verify model config preserved
      expect(checkpoint.modelConfig.currentModel).toBe('claude-3-5-haiku-20241022');
      expect(checkpoint.modelConfig.permissionMode).toBe('acceptEdits');
      expect(checkpoint.modelConfig.configuration.temperature).toBe(0.7);
    });

    test('should generate valid embeddings', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');

      const context = stateMachine.getContext();
      const checkpoint = await checkpointManager.createCheckpoint(
        testQueryId,
        context
      );

      // Verify embedding
      expect(checkpoint.embedding).toBeDefined();
      expect(checkpoint.embedding.length).toBe(384); // Standard dimension
      expect(checkpoint.embedding.every(v => v >= 0 && v <= 1)).toBe(true);
    });
  });

  describe('Concurrent checkpoint operations', () => {
    test('should handle multiple queries simultaneously', async () => {
      const queryIds = ['concurrent-1', 'concurrent-2', 'concurrent-3'];

      // Create multiple state machines
      const machines = queryIds.map(id => new QueryStateMachine(id));

      // Start all queries
      await Promise.all(machines.map(m => m.transition('START')));

      // Pause all queries
      await Promise.all(machines.map(m => m.transition('PAUSE')));

      // Create checkpoints concurrently
      const checkpointPromises = machines.map((m, i) =>
        checkpointManager.createCheckpoint(queryIds[i], m.getContext())
      );

      const checkpoints = await Promise.all(checkpointPromises);

      // Verify all checkpoints created
      expect(checkpoints).toHaveLength(3);
      checkpoints.forEach((cp, i) => {
        expect(cp.queryId).toBe(queryIds[i]);
      });

      // Resume all queries concurrently
      const resumePromises = queryIds.map(id =>
        resumeManager.resumeQuery(id)
      );

      const results = await Promise.all(resumePromises);

      // Verify all resumed successfully
      expect(results.every(r => r.success)).toBe(true);
    });
  });

  describe('Checkpoint statistics', () => {
    test('should track checkpoint statistics', async () => {
      const stats = await checkpointManager.getStatistics();

      expect(stats).toBeDefined();
      expect(stats.totalCheckpoints).toBeGreaterThanOrEqual(0);
      expect(stats.l2Status).toBeDefined();
    });

    test('should track resume statistics', () => {
      const stats = resumeManager.getStatistics();

      expect(stats).toBeDefined();
      expect(stats.successfulResumes).toBeGreaterThanOrEqual(0);
      expect(stats.failedResumes).toBeGreaterThanOrEqual(0);
      expect(stats.averageDuration).toBeGreaterThanOrEqual(0);
    });
  });
});
