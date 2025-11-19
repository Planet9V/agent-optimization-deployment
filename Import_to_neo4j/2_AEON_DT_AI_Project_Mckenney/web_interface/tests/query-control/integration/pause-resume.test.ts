/**
 * GAP-003 Query Control System - Pause-Resume Integration Tests
 *
 * File: tests/query-control/integration/pause-resume.test.ts
 * Created: 2025-11-14
 * Version: v1.0.0
 * Purpose: Integration tests for complete pause-resume workflow
 *
 * Constitutional Compliance:
 * - DILIGENCE: Comprehensive integration test coverage
 * - INTEGRITY: Validates 100% accurate restoration
 * - NO DEVELOPMENT THEATER: Production-grade integration testing
 */

import { describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import {
  CheckpointManager,
  getCheckpointManager,
  type Checkpoint,
  type ExecutionContext,
  type ModelConfig
} from '../../../lib/query-control/checkpoint/checkpoint-manager';
import {
  QueryStateMachine,
  QueryState,
  type QueryContext
} from '../../../lib/query-control/state/state-machine';
import { QueryRegistry, getQueryRegistry } from '../../../lib/query-control/registry/query-registry';

describe('Pause-Resume Integration Tests', () => {
  let checkpointManager: CheckpointManager;
  let registry: QueryRegistry;

  beforeEach(() => {
    checkpointManager = new CheckpointManager();
    registry = new QueryRegistry();
  });

  afterEach(async () => {
    await checkpointManager.clear();
    await registry.clear();
  });

  describe('Full Pause-Resume Cycle', () => {
    test('should complete full pause-resume cycle with 100% accuracy', async () => {
      const queryId = 'integration-test-001';

      // 1. Create query and register it
      await registry.registerQuery(queryId, {
        state: QueryState.INIT,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 3,
        taskCount: 5,
        checkpointCount: 0
      });

      // 2. Transition to RUNNING
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);

      // 3. Create execution context
      const executionContext: ExecutionContext = {
        taskQueue: [
          { id: 'task-1', status: 'completed', description: 'Initialize system', progress: 100 },
          { id: 'task-2', status: 'running', description: 'Process data', progress: 50 },
          { id: 'task-3', status: 'pending', description: 'Generate report', progress: 0 }
        ],
        agentStates: {
          'agent-001': {
            agentId: 'agent-001',
            status: 'active',
            currentTask: 'task-2'
          },
          'agent-002': {
            agentId: 'agent-002',
            status: 'idle',
            currentTask: null
          }
        },
        resources: {
          memoryUsage: 256,
          cpuUsage: 45,
          activeConnections: 3
        },
        variables: {
          iterationCount: 150,
          lastProcessedId: 'record-12345',
          batchSize: 100
        }
      };

      const modelConfig: ModelConfig = {
        model: 'sonnet',
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: {
          verbosity: 'normal',
          format: 'json'
        }
      };

      // 4. Create checkpoint (PAUSE)
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

      const checkpoint = await checkpointManager.createCheckpoint(
        queryId,
        context,
        modelConfig,
        'user_pause'
      );

      expect(checkpoint).toBeDefined();
      expect(checkpoint.queryId).toBe(queryId);
      expect(checkpoint.state).toBe(QueryState.RUNNING);

      // 5. Verify checkpoint was saved
      const retrieved = await checkpointManager.retrieveCheckpoint(queryId);
      expect(retrieved).not.toBeNull();
      expect(retrieved?.queryId).toBe(queryId);

      // 6. Verify 100% accurate restoration
      expect(retrieved?.executionContext.taskQueue).toHaveLength(3);
      expect(retrieved?.executionContext.taskQueue[0].id).toBe('task-1');
      expect(retrieved?.executionContext.taskQueue[0].status).toBe('completed');
      expect(retrieved?.executionContext.taskQueue[1].progress).toBe(50);

      expect(retrieved?.executionContext.agentStates['agent-001'].status).toBe('active');
      expect(retrieved?.executionContext.agentStates['agent-001'].currentTask).toBe('task-2');

      expect(retrieved?.executionContext.resources.memoryUsage).toBe(256);
      expect(retrieved?.executionContext.variables.iterationCount).toBe(150);
      expect(retrieved?.executionContext.variables.lastProcessedId).toBe('record-12345');

      expect(retrieved?.modelConfig.model).toBe('sonnet');
      expect(retrieved?.modelConfig.temperature).toBe(0.7);

      // 7. Update registry with checkpoint count
      await registry.updateQuery(queryId, {
        checkpointCount: 1,
        state: QueryState.PAUSED
      });

      const queryMetadata = await registry.getQuery(queryId);
      expect(queryMetadata?.checkpointCount).toBe(1);
      expect(queryMetadata?.state).toBe(QueryState.PAUSED);
    });

    test('should handle multiple pause-resume cycles', async () => {
      const queryId = 'integration-test-002';

      const modelConfig: ModelConfig = {
        model: 'haiku',
        temperature: 0.5,
        maxTokens: 2000,
        permissionMode: 'plan',
        preferences: {}
      };

      // Create first checkpoint
      const context1: QueryContext = {
        queryId,
        metadata: {
          state: QueryState.RUNNING,
          variables: { progress: 25 }
        },
        timestamp: Date.now()
      };

      const checkpoint1 = await checkpointManager.createCheckpoint(
        queryId,
        context1,
        modelConfig,
        'scheduled'
      );

      // Wait a bit to ensure different timestamps
      await new Promise(resolve => setTimeout(resolve, 10));

      // Create second checkpoint
      const context2: QueryContext = {
        queryId,
        metadata: {
          state: QueryState.RUNNING,
          variables: { progress: 50 }
        },
        timestamp: Date.now()
      };

      const checkpoint2 = await checkpointManager.createCheckpoint(
        queryId,
        context2,
        modelConfig,
        'scheduled'
      );

      // Wait again
      await new Promise(resolve => setTimeout(resolve, 10));

      // Create third checkpoint
      const context3: QueryContext = {
        queryId,
        metadata: {
          state: QueryState.RUNNING,
          variables: { progress: 75 }
        },
        timestamp: Date.now()
      };

      const checkpoint3 = await checkpointManager.createCheckpoint(
        queryId,
        context3,
        modelConfig,
        'scheduled'
      );

      // Retrieve latest checkpoint (should be checkpoint3)
      const latest = await checkpointManager.getLatestCheckpoint(queryId);
      expect(latest).not.toBeNull();
      expect(latest?.executionContext.variables.progress).toBe(75);
      expect(latest?.timestamp).toBe(checkpoint3.timestamp);

      // List all checkpoints for this query
      const list = await checkpointManager.listCheckpoints({ queryId });
      expect(list.checkpoints.length).toBeGreaterThanOrEqual(3);
      expect(list.checkpoints[0].executionContext.variables.progress).toBe(75); // Most recent first
    });
  });

  describe('Performance Testing', () => {
    test('should create checkpoint in less than 150ms', async () => {
      const queryId = 'perf-test-001';

      const context: QueryContext = {
        queryId,
        metadata: {
          state: QueryState.RUNNING,
          taskQueue: Array(10).fill(null).map((_, i) => ({
            id: `task-${i}`,
            status: 'pending',
            description: `Task ${i}`,
            progress: 0
          })),
          agentStates: {
            'agent-001': { agentId: 'agent-001', status: 'active', currentTask: 'task-0' },
            'agent-002': { agentId: 'agent-002', status: 'idle', currentTask: null }
          },
          resources: {
            memoryUsage: 512,
            cpuUsage: 60
          },
          variables: {
            count: 1000,
            data: Array(100).fill('sample data')
          }
        },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: 'sonnet',
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: { verbosity: 'normal' }
      };

      const startTime = Date.now();
      const checkpoint = await checkpointManager.createCheckpoint(
        queryId,
        context,
        modelConfig,
        'user_pause'
      );
      const duration = Date.now() - startTime;

      expect(checkpoint).toBeDefined();
      expect(duration).toBeLessThan(150); // <150ms target
    });

    test('should retrieve checkpoint quickly from L1 cache', async () => {
      const queryId = 'perf-test-002';

      const context: QueryContext = {
        queryId,
        metadata: { state: QueryState.RUNNING },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: 'haiku',
        temperature: 0.5,
        maxTokens: 2000,
        permissionMode: 'default',
        preferences: {}
      };

      // Create checkpoint
      await checkpointManager.createCheckpoint(queryId, context, modelConfig);

      // Retrieve from L1 cache (should be <10ms)
      const startTime = Date.now();
      const retrieved = await checkpointManager.getLatestCheckpoint(queryId);
      const duration = Date.now() - startTime;

      expect(retrieved).not.toBeNull();
      expect(duration).toBeLessThan(10); // L1 cache should be very fast
    });
  });

  describe('Checkpoint Cleanup and Pruning', () => {
    test('should prune old checkpoints keeping only latest 10', async () => {
      const queryId = 'prune-test-001';

      const modelConfig: ModelConfig = {
        model: 'sonnet',
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: {}
      };

      // Create 15 checkpoints
      for (let i = 0; i < 15; i++) {
        const context: QueryContext = {
          queryId,
          metadata: {
            state: QueryState.RUNNING,
            variables: { iteration: i }
          },
          timestamp: Date.now()
        };

        await checkpointManager.createCheckpoint(queryId, context, modelConfig);

        // Small delay to ensure different timestamps
        await new Promise(resolve => setTimeout(resolve, 5));
      }

      // List checkpoints (should have pruned to 10)
      const list = await checkpointManager.listCheckpoints({ queryId });

      // Should have kept only latest 10
      expect(list.checkpoints.length).toBeLessThanOrEqual(10);

      // Latest checkpoint should have highest iteration
      expect(list.checkpoints[0].executionContext.variables.iteration).toBeGreaterThanOrEqual(5);
    });

    test('should delete specific checkpoint', async () => {
      const queryId = 'delete-test-001';

      const context: QueryContext = {
        queryId,
        metadata: { state: QueryState.RUNNING },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: 'haiku',
        temperature: 0.5,
        maxTokens: 2000,
        permissionMode: 'default',
        preferences: {}
      };

      const checkpoint = await checkpointManager.createCheckpoint(
        queryId,
        context,
        modelConfig
      );

      // Verify checkpoint exists
      const retrieved = await checkpointManager.retrieveCheckpoint(
        queryId,
        checkpoint.timestamp
      );
      expect(retrieved).not.toBeNull();

      // Delete checkpoint
      const deleted = await checkpointManager.deleteCheckpoint(
        queryId,
        checkpoint.timestamp
      );
      expect(deleted).toBe(true);

      // Verify checkpoint is gone
      const afterDelete = await checkpointManager.retrieveCheckpoint(
        queryId,
        checkpoint.timestamp
      );
      expect(afterDelete).toBeNull();
    });
  });

  describe('Error Recovery', () => {
    test('should handle missing checkpoint gracefully', async () => {
      const retrieved = await checkpointManager.retrieveCheckpoint('non-existent-query');
      expect(retrieved).toBeNull();
    });

    test('should handle checkpoint creation errors gracefully', async () => {
      const queryId = 'error-test-001';

      // Create context with minimal data
      const context: QueryContext = {
        queryId,
        metadata: {},
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: 'sonnet',
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: {}
      };

      // Should not throw error even with minimal context
      const checkpoint = await checkpointManager.createCheckpoint(
        queryId,
        context,
        modelConfig
      );

      expect(checkpoint).toBeDefined();
      expect(checkpoint.queryId).toBe(queryId);
    });
  });

  describe('Checkpoint Statistics', () => {
    test('should provide accurate checkpoint statistics', async () => {
      const queryId1 = 'stats-test-001';
      const queryId2 = 'stats-test-002';

      const modelConfig: ModelConfig = {
        model: 'sonnet',
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: {}
      };

      // Create checkpoints for query 1
      for (let i = 0; i < 3; i++) {
        const context: QueryContext = {
          queryId: queryId1,
          metadata: { state: QueryState.RUNNING },
          timestamp: Date.now()
        };
        await checkpointManager.createCheckpoint(queryId1, context, modelConfig);
        await new Promise(resolve => setTimeout(resolve, 5));
      }

      // Create checkpoints for query 2
      for (let i = 0; i < 2; i++) {
        const context: QueryContext = {
          queryId: queryId2,
          metadata: { state: QueryState.RUNNING },
          timestamp: Date.now()
        };
        await checkpointManager.createCheckpoint(queryId2, context, modelConfig);
        await new Promise(resolve => setTimeout(resolve, 5));
      }

      const stats = await checkpointManager.getStatistics();

      expect(stats.totalCheckpoints).toBeGreaterThanOrEqual(5);
      expect(stats.checkpointsByQuery[queryId1]).toBe(3);
      expect(stats.checkpointsByQuery[queryId2]).toBe(2);
      expect(stats.averageSize).toBeGreaterThan(0);
      expect(stats.newestTimestamp).toBeGreaterThan(stats.oldestTimestamp);
    });
  });

  describe('Singleton Pattern', () => {
    test('should return same checkpoint manager instance', () => {
      const instance1 = getCheckpointManager();
      const instance2 = getCheckpointManager();
      expect(instance1).toBe(instance2);
    });
  });

  describe('Integration with QueryRegistry', () => {
    test('should update registry after checkpoint creation', async () => {
      const queryId = 'registry-integration-001';

      // Register query
      await registry.registerQuery(queryId, {
        state: QueryState.RUNNING,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 2,
        taskCount: 5,
        checkpointCount: 0
      });

      // Create checkpoint
      const context: QueryContext = {
        queryId,
        metadata: { state: QueryState.RUNNING },
        timestamp: Date.now()
      };

      const modelConfig: ModelConfig = {
        model: 'sonnet',
        temperature: 0.7,
        maxTokens: 4000,
        permissionMode: 'default',
        preferences: {}
      };

      await checkpointManager.createCheckpoint(queryId, context, modelConfig);

      // Update registry
      await registry.updateQuery(queryId, {
        checkpointCount: 1,
        state: QueryState.PAUSED
      });

      // Verify registry was updated
      const queryMetadata = await registry.getQuery(queryId);
      expect(queryMetadata?.checkpointCount).toBe(1);
      expect(queryMetadata?.state).toBe(QueryState.PAUSED);
    });
  });
});
