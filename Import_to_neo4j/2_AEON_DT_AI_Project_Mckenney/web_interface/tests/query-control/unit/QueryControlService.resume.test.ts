/**
 * GAP-003 Query Control System - QueryControlService.resume() Unit Tests
 *
 * File: tests/query-control/unit/QueryControlService.resume.test.ts
 * Created: 2025-11-14
 * Version: v1.1.0
 * Purpose: Comprehensive unit tests for QueryControlService resume() operation
 *
 * Constitutional Compliance:
 * - DILIGENCE: >90% line coverage, >85% branch coverage
 * - INTEGRITY: Validates 100% checkpoint restoration accuracy
 * - NO DEVELOPMENT THEATER: Production-grade unit testing
 *
 * Test Coverage (v1.1.0):
 * 1. resume() success - Checkpoint restoration from PAUSED state
 * 2. State transition - PAUSED → RUNNING validation
 * 3. Checkpoint restoration - 100% context accuracy
 * 4. Telemetry recording - operationType='resume' instrumentation
 * 5. Performance profiling - Latency recording
 * 6. Neural hook training - trainTransitionPattern(PAUSED → RUNNING)
 * 7. Error handling - No checkpoint, invalid state, not found
 * 8. Performance target - <150ms resume time
 * 9. Metadata tracking - resumedFrom, checkpointId in telemetry
 * 10. Latest checkpoint - Resume from latest when no timestamp
 * 11. Specific checkpoint - Resume from specific timestamp
 * 12. Registry update - Query metadata update with resume info
 *
 * Coverage Goal: >90% line coverage, >85% branch coverage
 */

import { describe, test, expect, beforeEach, afterEach, jest } from '@jest/globals';
import {
  QueryControlService,
  type ResumeResult
} from '../../../lib/query-control/query-control-service';
import {
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
import { getQueryRegistry } from '../../../lib/query-control/registry/query-registry';
import { getTelemetryService } from '../../../lib/query-control/telemetry/telemetry-service';
import { getPerformanceProfiler } from '../../../lib/query-control/profiling/performance-profiler';
import { getNeuralHooks } from '../../../lib/query-control/neural/neural-hooks';

describe('QueryControlService.resume() Unit Tests', () => {
  let service: QueryControlService;

  // Helper to create test execution context
  const createTestExecutionContext = (variables: Record<string, unknown> = {}): ExecutionContext => ({
    taskQueue: [
      { id: 'task-1', status: 'completed', description: 'First task', progress: 100 },
      { id: 'task-2', status: 'running', description: 'Second task', progress: 60 },
      { id: 'task-3', status: 'pending', description: 'Third task', progress: 0 }
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
      memoryUsage: 512,
      cpuUsage: 60,
      activeConnections: 5
    },
    variables: {
      iterationCount: 100,
      lastProcessedId: 'record-5000',
      ...variables
    }
  });

  // Helper to create test model config
  const createTestModelConfig = (overrides: Partial<ModelConfig> = {}): ModelConfig => ({
    model: 'claude-3-5-sonnet-20241022',
    temperature: 0.7,
    maxTokens: 4000,
    permissionMode: 'default',
    preferences: {},
    ...overrides
  });

  // Helper to create test query context
  const createTestQueryContext = (
    queryId: string,
    state: QueryState = QueryState.PAUSED,
    executionContext: ExecutionContext
  ): QueryContext => ({
    queryId,
    metadata: {
      state,
      ...executionContext
    },
    timestamp: Date.now(),
    agentCount: Object.keys(executionContext.agentStates || {}).length,
    taskCount: executionContext.taskQueue?.length || 0
  });

  beforeEach(async () => {
    // Create service (uses singleton pattern internally)
    service = new QueryControlService();

    // Clear all singleton services before each test
    await getCheckpointManager().clear();
    await getQueryRegistry().clear();
  });

  afterEach(async () => {
    // Clear singleton services after each test
    await getCheckpointManager().clear();
    await getQueryRegistry().clear();
  });

  describe('Successful Resume Operations', () => {
    describe('Resume from Latest Checkpoint', () => {
      test('should resume query from latest checkpoint successfully', async () => {
        const queryId = 'resume-test-001';
        const executionContext = createTestExecutionContext({ testVariable: 'value1' });
        const modelConfig = createTestModelConfig();

        // 1. Register query
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        // 2. Create state machine and transition to PAUSED
        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        expect(stateMachine.getState()).toBe(QueryState.PAUSED);

        // 3. Register state machine with service (simulate internal state)
        (service as any).stateMachines.set(queryId, stateMachine);

        // 4. Create checkpoint
        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        const checkpoint = await getCheckpointManager().createCheckpoint(
          queryId,
          context,
          modelConfig,
          'user_pause'
        );

        // 5. Resume without specifying timestamp (should use latest)
        const result = await service.resume(queryId);

        // Debug: Log result if test fails
        if (!result.success) {
          console.log('Resume failed:', result);
        }

        // Validate success
        expect(result.success).toBe(true);
        expect(result.state).toBe(QueryState.RUNNING);
        expect(result.checkpoint).toBeDefined();
        expect(result.checkpoint?.queryId).toBe(queryId);
        expect(result.checkpoint?.timestamp).toBe(checkpoint.timestamp);
        expect(result.resumedFrom).toBe(`${checkpoint.queryId}:${checkpoint.timestamp}`);
        expect(result.resumeTimeMs).toBeGreaterThan(0);

        // Validate state machine transitioned
        expect(stateMachine.getState()).toBe(QueryState.RUNNING);

        // Validate checkpoint restoration
        expect(result.checkpoint?.executionContext.variables.testVariable).toBe('value1');
        expect(result.checkpoint?.executionContext.taskQueue).toHaveLength(3);
        expect(result.checkpoint?.executionContext.taskQueue[1].progress).toBe(60);
      });

      test('should resume from latest checkpoint with complex execution context', async () => {
        const queryId = 'resume-test-002';
        const complexContext = createTestExecutionContext({
          complexData: {
            nested: {
              deeply: {
                value: 'found'
              }
            }
          },
          arrayData: [1, 2, 3, { nested: true }],
          largeIterationCount: 50000
        });

        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, complexContext);
        await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Resume
        const result = await service.resume(queryId);

        // Validate complex data restoration
        expect(result.success).toBe(true);
        expect(
          (result.checkpoint?.executionContext.variables.complexData as any).nested.deeply.value
        ).toBe('found');
        expect(result.checkpoint?.executionContext.variables.arrayData).toEqual([
          1,
          2,
          3,
          { nested: true }
        ]);
        expect(result.checkpoint?.executionContext.variables.largeIterationCount).toBe(50000);
      });
    });

    describe('Resume from Specific Checkpoint', () => {
      test('should resume from specific checkpoint by timestamp', async () => {
        const queryId = 'resume-test-003';
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        // Create first checkpoint
        const context1 = createTestQueryContext(
          queryId,
          QueryState.PAUSED,
          createTestExecutionContext({ version: 1 })
        );
        const checkpoint1 = await getCheckpointManager().createCheckpoint(
          queryId,
          context1,
          modelConfig
        );

        await new Promise(resolve => setTimeout(resolve, 50));

        // Create second checkpoint
        const context2 = createTestQueryContext(
          queryId,
          QueryState.PAUSED,
          createTestExecutionContext({ version: 2 })
        );
        const checkpoint2 = await getCheckpointManager().createCheckpoint(
          queryId,
          context2,
          modelConfig
        );

        // Resume from first checkpoint specifically
        const result = await service.resume(queryId, checkpoint1.timestamp);

        // Validate resumed from correct checkpoint
        expect(result.success).toBe(true);
        expect(result.checkpoint?.timestamp).toBe(checkpoint1.timestamp);
        expect(result.checkpoint?.executionContext.variables.version).toBe(1);
        expect(result.resumedFrom).toBe(`${checkpoint1.queryId}:${checkpoint1.timestamp}`);

        // Verify we didn't resume from checkpoint2
        expect(result.checkpoint?.timestamp).not.toBe(checkpoint2.timestamp);
      });

      test('should maintain checkpoint selection independence', async () => {
        const queryId = 'resume-test-004';
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        // Create 5 checkpoints
        const checkpoints: Checkpoint[] = [];
        for (let i = 0; i < 5; i++) {
          const context = createTestQueryContext(
            queryId,
            QueryState.PAUSED,
            createTestExecutionContext({ checkpointNumber: i })
          );
          const checkpoint = await getCheckpointManager().createCheckpoint(
            queryId,
            context,
            modelConfig
          );
          checkpoints.push(checkpoint);
          await new Promise(resolve => setTimeout(resolve, 10));
        }

        // Resume from middle checkpoint (index 2)
        const result = await service.resume(queryId, checkpoints[2].timestamp);

        expect(result.success).toBe(true);
        expect(result.checkpoint?.executionContext.variables.checkpointNumber).toBe(2);
      });
    });

    describe('State Transition Validation', () => {
      test('should transition state from PAUSED to RUNNING', async () => {
        const queryId = 'state-test-001';
        const executionContext = createTestExecutionContext();
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        // Verify initial state
        expect(stateMachine.getState()).toBe(QueryState.PAUSED);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Resume
        const result = await service.resume(queryId);

        // Validate state transition
        expect(result.success).toBe(true);
        expect(result.state).toBe(QueryState.RUNNING);
        expect(stateMachine.getState()).toBe(QueryState.RUNNING);
      });

      test('should update registry with RUNNING state and resume metadata', async () => {
        const queryId = 'registry-test-001';
        const executionContext = createTestExecutionContext();
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        const checkpoint = await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Resume
        const beforeResumeTime = Date.now();
        await service.resume(queryId);
        const afterResumeTime = Date.now();

        // Validate registry update
        const queryInfo = await getQueryRegistry().getQuery(queryId);
        expect(queryInfo).not.toBeNull();
        expect(queryInfo!.state).toBe(QueryState.RUNNING);
        expect(queryInfo!.metadata.resumedFrom).toBe(checkpoint.timestamp);
        expect(queryInfo!.metadata.resumedAt).toBeGreaterThanOrEqual(beforeResumeTime);
        expect(queryInfo!.metadata.resumedAt).toBeLessThanOrEqual(afterResumeTime);
      });
    });
  });

  describe('Performance Validation', () => {
    describe('Performance Target (<150ms)', () => {
      test('should complete resume operation in less than 150ms', async () => {
        const queryId = 'perf-test-001';
        const executionContext = createTestExecutionContext();
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Measure performance
        const startTime = Date.now();
        const result = await service.resume(queryId);
        const duration = Date.now() - startTime;

        expect(result.success).toBe(true);
        expect(duration).toBeLessThan(150);
        expect(result.resumeTimeMs).toBeLessThan(150);
      });

      test('should complete resume with large checkpoint in <150ms', async () => {
        const queryId = 'perf-test-002';
        const largeContext = createTestExecutionContext({
          largeArray: Array(100).fill({ data: 'large chunk of data' }),
          manyVariables: Object.fromEntries(
            Array(50)
              .fill(null)
              .map((_, i) => [`var${i}`, `value${i}`])
          )
        });

        // Add many tasks and agents
        largeContext.taskQueue = Array(50)
          .fill(null)
          .map((_, i) => ({
            id: `task-${i}`,
            status: 'pending',
            description: `Task ${i}`,
            progress: i * 2
          }));

        largeContext.agentStates = Object.fromEntries(
          Array(20)
            .fill(null)
            .map((_, i) => [
              `agent-${i}`,
              {
                agentId: `agent-${i}`,
                status: i % 2 === 0 ? 'active' : 'idle',
                currentTask: i % 2 === 0 ? `task-${i}` : null
              }
            ])
        );

        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 20,
          taskCount: 50,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, largeContext);
        await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Measure performance with large checkpoint
        const startTime = Date.now();
        const result = await service.resume(queryId);
        const duration = Date.now() - startTime;

        expect(result.success).toBe(true);
        expect(duration).toBeLessThan(150);
      });
    });

    describe('Performance Profiling Instrumentation', () => {
      test('should record latency in performance profiler', async () => {
        const queryId = 'profiler-test-001';
        const executionContext = createTestExecutionContext();
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Get stats before resume
        const statsBefore = getPerformanceProfiler().getStatistics();

        // Resume
        await service.resume(queryId);

        // Validate profiler recorded latency
        const statsAfter = getPerformanceProfiler().getStatistics();
        expect(statsAfter.operationCounts.resume).toBe((statsBefore.operationCounts.resume || 0) + 1);
        expect(statsAfter.averageLatencies.resume).toBeGreaterThan(0);
        expect(statsAfter.averageLatencies.resume).toBeLessThan(150);
      });
    });
  });

  describe('Telemetry and Instrumentation (v1.1.0)', () => {
    describe('Telemetry Recording', () => {
      test('should record successful resume operation in telemetry', async () => {
        const queryId = 'telemetry-test-001';
        const executionContext = createTestExecutionContext();
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        const checkpoint = await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Resume
        const beforeResume = Date.now();
        await service.resume(queryId);

        // Validate telemetry
        const operations = getTelemetryService().getOperations({
          operationType: 'resume',
          queryId
        });

        expect(operations.length).toBeGreaterThan(0);

        const resumeOp = operations[operations.length - 1];
        expect(resumeOp.operationType).toBe('resume');
        expect(resumeOp.queryId).toBe(queryId);
        expect(resumeOp.success).toBe(true);
        expect(resumeOp.durationMs).toBeGreaterThan(0);
        expect(resumeOp.durationMs).toBeLessThan(150);
        expect(resumeOp.startTime).toBeGreaterThanOrEqual(beforeResume);
        expect(resumeOp.metadata).toBeDefined();
      });

      test('should include resumedFrom and checkpointId in telemetry metadata', async () => {
        const queryId = 'metadata-test-001';
        const executionContext = createTestExecutionContext();
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        const checkpoint = await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Resume
        await service.resume(queryId);

        // Validate metadata
        const operations = getTelemetryService().getOperations({
          operationType: 'resume',
          queryId
        });

        const resumeOp = operations[operations.length - 1];
        expect(resumeOp.metadata.resumedFrom).toBe(checkpoint.timestamp);
        expect(resumeOp.metadata.checkpointId).toBe(`${checkpoint.queryId}:${checkpoint.timestamp}`);
        expect(resumeOp.metadata.state).toBe(QueryState.RUNNING);
      });

      test('should record failed resume operation in telemetry', async () => {
        const queryId = 'telemetry-fail-001';

        // Setup with no checkpoint (will fail)
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: 'sonnet',
          permissionMode: 'default',
          startTime: Date.now(),
          agentCount: 0,
          taskCount: 0,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        // Resume without checkpoint
        const result = await service.resume(queryId);

        expect(result.success).toBe(false);

        // Validate failure telemetry
        const operations = getTelemetryService().getOperations({
          operationType: 'resume',
          queryId
        });

        expect(operations.length).toBeGreaterThan(0);
        const resumeOp = operations[operations.length - 1];
        expect(resumeOp.success).toBe(false);
        expect(resumeOp.error).toBeDefined();
        expect(resumeOp.error).toContain('No checkpoint found');
      });
    });
  });

  describe('Neural Hooks Integration (v1.1.0)', () => {
    describe('Transition Pattern Training', () => {
      test('should train neural transition pattern PAUSED → RUNNING', async () => {
        const queryId = 'neural-test-001';
        const executionContext = createTestExecutionContext();
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Resume (should train pattern)
        await service.resume(queryId);

        // Validate pattern training
        const patterns = getNeuralHooks().getTransitionPatterns(queryId);
        expect(patterns).toBeDefined();
        expect(patterns.length).toBeGreaterThan(0);

        const resumePattern = patterns.find(
          p => p.fromState === QueryState.PAUSED && p.toState === QueryState.RUNNING
        );

        expect(resumePattern).toBeDefined();
        expect(resumePattern!.success).toBe(true);
        expect(resumePattern!.latencyMs).toBeGreaterThan(0);
      });

      test('should record successful transition in neural training', async () => {
        const queryId = 'neural-test-002';
        const executionContext = createTestExecutionContext();
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Resume
        const result = await service.resume(queryId);

        // Validate neural training success flag
        const patterns = getNeuralHooks().getTransitionPatterns(queryId);
        const resumePattern = patterns.find(
          p => p.fromState === QueryState.PAUSED && p.toState === QueryState.RUNNING
        );

        expect(resumePattern!.success).toBe(true);
        expect(result.success).toBe(true);
      });
    });
  });

  describe('Checkpoint Restoration Accuracy', () => {
    describe('100% Restoration Validation', () => {
      test('should restore execution context with 100% accuracy', async () => {
        const queryId = 'restoration-test-001';

        // Create comprehensive execution context
        const executionContext: ExecutionContext = {
          taskQueue: [
            {
              id: 'task-alpha',
              status: 'completed',
              description: 'Alpha task',
              progress: 100
            },
            { id: 'task-beta', status: 'running', description: 'Beta task', progress: 75 },
            { id: 'task-gamma', status: 'pending', description: 'Gamma task', progress: 0 },
            { id: 'task-delta', status: 'failed', description: 'Delta task', progress: 25 }
          ],
          agentStates: {
            'agent-primary': {
              agentId: 'agent-primary',
              status: 'active',
              currentTask: 'task-beta'
            },
            'agent-secondary': {
              agentId: 'agent-secondary',
              status: 'idle',
              currentTask: null
            },
            'agent-tertiary': {
              agentId: 'agent-tertiary',
              status: 'error',
              currentTask: 'task-delta'
            }
          },
          resources: {
            cpu: 85.5,
            memory: 4096,
            disk: 2048,
            network: 500,
            connections: 42,
            customMetric: 12345
          },
          variables: {
            stringVar: 'test-string-value',
            numberVar: 98765.432,
            booleanVar: true,
            nullVar: null,
            arrayVar: [1, 'two', { three: 3 }, [4, 5]],
            objectVar: {
              level1: {
                level2: {
                  level3: 'deep-value'
                }
              }
            },
            largeIterationCount: 5000000,
            lastProcessedId: 'record-xyz-12345'
          }
        };

        const modelConfig = createTestModelConfig({
          temperature: 0.85,
          maxTokens: 8000,
          permissionMode: 'bypassPermissions'
        });

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 3,
          taskCount: 4,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Resume
        const result = await service.resume(queryId);

        // Validate 100% accuracy restoration
        expect(result.success).toBe(true);
        expect(result.checkpoint).toBeDefined();

        const restored = result.checkpoint!.executionContext;

        // Task queue validation
        expect(restored.taskQueue).toHaveLength(4);
        expect(restored.taskQueue[0].id).toBe('task-alpha');
        expect(restored.taskQueue[0].status).toBe('completed');
        expect(restored.taskQueue[1].progress).toBe(75);
        expect(restored.taskQueue[2].status).toBe('pending');
        expect(restored.taskQueue[3].status).toBe('failed');

        // Agent states validation
        expect(restored.agentStates['agent-primary'].status).toBe('active');
        expect(restored.agentStates['agent-primary'].currentTask).toBe('task-beta');
        expect(restored.agentStates['agent-secondary'].currentTask).toBeNull();
        expect(restored.agentStates['agent-tertiary'].status).toBe('error');

        // Resources validation
        expect(restored.resources.cpu).toBe(85.5);
        expect(restored.resources.memory).toBe(4096);
        expect(restored.resources.connections).toBe(42);
        expect(restored.resources.customMetric).toBe(12345);

        // Variables validation (all types)
        expect(restored.variables.stringVar).toBe('test-string-value');
        expect(restored.variables.numberVar).toBe(98765.432);
        expect(restored.variables.booleanVar).toBe(true);
        expect(restored.variables.nullVar).toBeNull();
        expect(restored.variables.arrayVar).toEqual([1, 'two', { three: 3 }, [4, 5]]);
        expect((restored.variables.objectVar as any).level1.level2.level3).toBe('deep-value');
        expect(restored.variables.largeIterationCount).toBe(5000000);
        expect(restored.variables.lastProcessedId).toBe('record-xyz-12345');
      });
    });
  });

  describe('Error Handling', () => {
    describe('Query Not Found', () => {
      test('should return error when query does not exist', async () => {
        const result = await service.resume('non-existent-query');

        expect(result.success).toBe(false);
        expect(result.state).toBe(QueryState.ERROR);
        expect(result.error).toBeDefined();
        expect(result.error).toContain('not found');
        expect(result.resumeTimeMs).toBeGreaterThan(0);
      });

      test('should record error in telemetry for non-existent query', async () => {
        const queryId = 'error-test-001';
        await service.resume(queryId);

        const operations = getTelemetryService().getOperations({
          operationType: 'resume',
          queryId
        });

        expect(operations.length).toBeGreaterThan(0);
        const op = operations[operations.length - 1];
        expect(op.success).toBe(false);
        expect(op.error).toBeDefined();
      });
    });

    describe('Invalid State', () => {
      test('should return error when query is not in PAUSED state', async () => {
        const queryId = 'invalid-state-001';

        // Setup query in RUNNING state (not PAUSED)
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.RUNNING,
          model: 'sonnet',
          permissionMode: 'default',
          startTime: Date.now(),
          agentCount: 0,
          taskCount: 0,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        (service as any).stateMachines.set(queryId, stateMachine);

        expect(stateMachine.getState()).toBe(QueryState.RUNNING);

        // Attempt resume
        const result = await service.resume(queryId);

        expect(result.success).toBe(false);
        expect(result.state).toBe(QueryState.RUNNING);
        expect(result.error).toBeDefined();
        expect(result.error).toContain('Cannot resume from state');
        expect(result.error).toContain('Must be PAUSED');
      });

      test('should not transition state when resume fails due to invalid state', async () => {
        const queryId = 'invalid-state-002';

        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.RUNNING,
          model: 'sonnet',
          permissionMode: 'default',
          startTime: Date.now(),
          agentCount: 0,
          taskCount: 0,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        (service as any).stateMachines.set(queryId, stateMachine);

        const initialState = stateMachine.getState();

        await service.resume(queryId);

        // State should remain unchanged
        expect(stateMachine.getState()).toBe(initialState);
        expect(stateMachine.getState()).toBe(QueryState.RUNNING);
      });
    });

    describe('No Checkpoint Found', () => {
      test('should return error when no checkpoint exists', async () => {
        const queryId = 'no-checkpoint-001';

        // Setup query in PAUSED state but with no checkpoint
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.PAUSED,
          model: 'sonnet',
          permissionMode: 'default',
          startTime: Date.now(),
          agentCount: 0,
          taskCount: 0,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        // Attempt resume
        const result = await service.resume(queryId);

        expect(result.success).toBe(false);
        expect(result.state).toBe(QueryState.ERROR);
        expect(result.error).toBeDefined();
        expect(result.error).toContain('No checkpoint found');
      });

      test('should return error when specific checkpoint timestamp not found', async () => {
        const queryId = 'no-checkpoint-002';
        const executionContext = createTestExecutionContext();
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Attempt resume with invalid timestamp
        const result = await service.resume(queryId, 999999);

        expect(result.success).toBe(false);
        expect(result.error).toContain('No checkpoint found');
      });
    });

    describe('Exception Handling', () => {
      test('should handle and return errors gracefully', async () => {
        const queryId = 'exception-test-001';

        // Create state machine that will cause an error during transition
        const stateMachine = new QueryStateMachine(queryId);
        (service as any).stateMachines.set(queryId, stateMachine);

        // Attempt resume (will fail due to missing registry entry)
        const result = await service.resume(queryId);

        expect(result.success).toBe(false);
        expect(result.error).toBeDefined();
        expect(result.resumeTimeMs).toBeGreaterThan(0);
      });

      test('should record performance even for failed operations', async () => {
        const queryId = 'exception-test-002';

        // Get stats before
        const statsBefore = getPerformanceProfiler().getStatistics();

        // Attempt resume on non-existent query
        await service.resume(queryId);

        // Validate profiler still recorded latency
        const statsAfter = getPerformanceProfiler().getStatistics();
        expect(statsAfter.operationCounts.resume).toBe(
          (statsBefore.operationCounts.resume || 0) + 1
        );
      });
    });
  });

  describe('Edge Cases', () => {
    describe('Empty Execution Context', () => {
      test('should handle checkpoint with minimal execution context', async () => {
        const queryId = 'minimal-context-001';

        const minimalContext: ExecutionContext = {
          taskQueue: [],
          agentStates: {},
          resources: {},
          variables: {}
        };

        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 0,
          taskCount: 0,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, minimalContext);
        await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Resume
        const result = await service.resume(queryId);

        expect(result.success).toBe(true);
        expect(result.checkpoint?.executionContext.taskQueue).toEqual([]);
        expect(result.checkpoint?.executionContext.agentStates).toEqual({});
      });
    });

    describe('Multiple Resume Attempts', () => {
      test('should allow multiple resume operations on same query', async () => {
        const queryId = 'multiple-resume-001';
        const executionContext = createTestExecutionContext();
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // First resume
        const result1 = await service.resume(queryId);
        expect(result1.success).toBe(true);

        // Pause again
        await stateMachine.transition('PAUSE');

        // Create new checkpoint
        const context2 = createTestQueryContext(
          queryId,
          QueryState.PAUSED,
          createTestExecutionContext({ iteration: 2 })
        );
        await getCheckpointManager().createCheckpoint(queryId, context2, modelConfig);

        // Second resume
        const result2 = await service.resume(queryId);
        expect(result2.success).toBe(true);
        expect(result2.checkpoint?.executionContext.variables.iteration).toBe(2);
      });
    });
  });

  describe('Integration with Services', () => {
    describe('CheckpointManager Integration', () => {
      test('should retrieve checkpoint from CheckpointManager correctly', async () => {
        const queryId = 'integration-cp-001';
        const executionContext = createTestExecutionContext({ testData: 'checkpoint-test' });
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        const checkpoint = await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Resume
        const result = await service.resume(queryId);

        // Validate checkpoint retrieval
        expect(result.checkpoint).toBeDefined();
        expect(result.checkpoint?.queryId).toBe(checkpoint.queryId);
        expect(result.checkpoint?.timestamp).toBe(checkpoint.timestamp);
        expect(result.checkpoint?.executionContext.variables.testData).toBe('checkpoint-test');
      });
    });

    describe('QueryRegistry Integration', () => {
      test('should update registry with resume metadata', async () => {
        const queryId = 'integration-reg-001';
        const executionContext = createTestExecutionContext();
        const modelConfig = createTestModelConfig();

        // Setup
        await getQueryRegistry().registerQuery(queryId, {
          state: QueryState.INIT,
          model: modelConfig.model,
          permissionMode: modelConfig.permissionMode,
          startTime: Date.now(),
          agentCount: 2,
          taskCount: 3,
          checkpointCount: 0
        });

        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        await stateMachine.transition('PAUSE');
        (service as any).stateMachines.set(queryId, stateMachine);

        const context = createTestQueryContext(queryId, QueryState.PAUSED, executionContext);
        const checkpoint = await getCheckpointManager().createCheckpoint(queryId, context, modelConfig);

        // Resume
        await service.resume(queryId);

        // Validate registry update
        const queryInfo = await getQueryRegistry().getQuery(queryId);
        expect(queryInfo?.state).toBe(QueryState.RUNNING);
        expect(queryInfo?.metadata.resumedFrom).toBe(checkpoint.timestamp);
        expect(queryInfo?.metadata.resumedAt).toBeDefined();
      });
    });
  });
});
