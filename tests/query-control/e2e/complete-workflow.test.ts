/**
 * GAP-003 Query Control System - End-to-End Integration Tests
 * Tests complete workflows across all system components
 */

import { QueryStateMachine } from '../../../lib/query-control/state/state-machine';
import { QueryRegistry } from '../../../lib/query-control/registry/query-registry';
import { CheckpointManager } from '../../../lib/query-control/checkpoint/checkpoint-manager';
import { ResumeManager } from '../../../lib/query-control/checkpoint/resume-manager';
import { ModelSwitcher } from '../../../lib/query-control/model/model-switcher';
import { ModelRegistry } from '../../../lib/query-control/model/model-registry';
import { PermissionManager } from '../../../lib/query-control/permissions/permission-manager';
import { CommandExecutor } from '../../../lib/query-control/commands/command-executor';
import { QueryState, ModelType, PermissionMode } from '../../../lib/query-control/types';

describe('GAP-003 Complete Workflow E2E Tests', () => {
  let stateMachine: QueryStateMachine;
  let queryRegistry: QueryRegistry;
  let checkpointManager: CheckpointManager;
  let resumeManager: ResumeManager;
  let modelSwitcher: ModelSwitcher;
  let modelRegistry: ModelRegistry;
  let permissionManager: PermissionManager;
  let commandExecutor: CommandExecutor;
  const testQueryId = 'e2e-workflow-001';

  beforeEach(async () => {
    stateMachine = new QueryStateMachine(testQueryId);
    queryRegistry = new QueryRegistry();
    checkpointManager = new CheckpointManager();
    resumeManager = new ResumeManager(checkpointManager);
    modelRegistry = new ModelRegistry();
    modelSwitcher = new ModelSwitcher(modelRegistry, checkpointManager);
    permissionManager = new PermissionManager();
    commandExecutor = new CommandExecutor();

    await checkpointManager.initialize();
    await queryRegistry.registerQuery(testQueryId, {
      userId: 'test-user',
      projectId: 'test-project'
    });
  });

  describe('Complete query lifecycle', () => {
    test('should execute full query lifecycle: START -> RUN -> PAUSE -> RESUME -> COMPLETE', async () => {
      const startTime = Date.now();

      // Phase 1: START
      await stateMachine.transition('START');
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);

      const query1 = await queryRegistry.getQuery(testQueryId);
      expect(query1).toBeDefined();

      // Phase 2: Model switch to Haiku for speed
      modelSwitcher.setCurrentModel(ModelType.SONNET);
      const modelSwitch = await modelSwitcher.switchModel(
        testQueryId,
        ModelType.HAIKU,
        stateMachine
      );
      expect(modelSwitch.success).toBe(true);
      expect(modelSwitch.currentModel).toBe(ModelType.HAIKU);

      // Phase 3: Permission switch to ACCEPT_EDITS
      permissionManager.setCurrentMode(PermissionMode.DEFAULT);
      const permSwitch = await permissionManager.switchMode(
        testQueryId,
        PermissionMode.ACCEPT_EDITS
      );
      expect(permSwitch.success).toBe(true);

      // Phase 4: Execute safe command
      const cmdResult = await commandExecutor.executeCommand(
        testQueryId,
        'echo "workflow test"'
      );
      expect(cmdResult.success).toBe(true);

      // Phase 5: PAUSE and create checkpoint
      await stateMachine.transition('PAUSE');
      expect(stateMachine.getState()).toBe(QueryState.PAUSED);

      const context = stateMachine.getContext();
      const checkpoint = await checkpointManager.createCheckpoint(
        testQueryId,
        context,
        'e2e_test_pause'
      );
      expect(checkpoint).toBeDefined();
      expect(checkpoint.queryId).toBe(testQueryId);

      // Phase 6: RESUME from checkpoint
      const resumeResult = await resumeManager.resumeQuery(testQueryId);
      expect(resumeResult.success).toBe(true);

      await stateMachine.transition('RESUME');
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);

      // Phase 7: COMPLETE
      await stateMachine.transition('COMPLETE');
      expect(stateMachine.getState()).toBe(QueryState.COMPLETED);

      const totalDuration = Date.now() - startTime;
      console.log(`Complete workflow duration: ${totalDuration}ms`);

      // Validate workflow completed successfully
      expect(stateMachine.getState()).toBe(QueryState.COMPLETED);
    });

    test('should handle complex multi-step workflow with all systems', async () => {
      // Step 1: Initialize and start query
      await stateMachine.transition('START');
      await queryRegistry.registerQuery(testQueryId, {
        userId: 'user-001',
        projectId: 'project-001'
      });

      // Step 2: Switch to optimal model based on task
      const recommendation = await modelRegistry.recommendModel('complex analysis task');
      modelSwitcher.setCurrentModel(ModelType.SONNET);

      if (recommendation.model !== ModelType.SONNET) {
        await modelSwitcher.switchModel(testQueryId, recommendation.model, stateMachine);
      }

      // Step 3: Configure permissions
      await permissionManager.switchMode(testQueryId, PermissionMode.BYPASS_PERMISSIONS);

      const capabilities = permissionManager.getModeCapabilities(PermissionMode.BYPASS_PERMISSIONS);
      expect(capabilities.bypassUserConfirmation).toBe(true);

      // Step 4: Execute multiple safe commands
      const cmd1 = await commandExecutor.executeCommand(testQueryId, 'echo step1');
      const cmd2 = await commandExecutor.executeCommand(testQueryId, 'echo step2');
      expect(cmd1.success).toBe(true);
      expect(cmd2.success).toBe(true);

      // Step 5: Create checkpoint before risky operation
      stateMachine.updateContext({
        metadata: { checkpoint_reason: 'before_complex_operation' }
      });
      await stateMachine.transition('PAUSE');

      const checkpoint1 = await checkpointManager.createCheckpoint(
        testQueryId,
        stateMachine.getContext(),
        'before_risky_op'
      );
      expect(checkpoint1.metadata.reason).toBe('before_risky_op');

      // Step 6: Resume and switch model
      await resumeManager.resumeQuery(testQueryId);
      await stateMachine.transition('RESUME');

      await modelSwitcher.switchModel(testQueryId, ModelType.OPUS, stateMachine);
      expect(modelSwitcher.getCurrentModel()).toBe(ModelType.OPUS);

      // Step 7: Complete workflow
      await stateMachine.transition('COMPLETE');

      const query = await queryRegistry.getQuery(testQueryId);
      expect(query?.status).toBe('active');
    });
  });

  describe('Error recovery workflows', () => {
    test('should recover from ERROR state via checkpoint restore', async () => {
      // Start and create checkpoint
      await stateMachine.transition('START');
      stateMachine.updateContext({
        metadata: { important_data: 'preserve_this' }
      });

      await stateMachine.transition('PAUSE');
      const checkpoint = await checkpointManager.createCheckpoint(
        testQueryId,
        stateMachine.getContext()
      );

      await stateMachine.transition('RESUME');

      // Simulate error
      await stateMachine.transition('ERROR');
      expect(stateMachine.getState()).toBe(QueryState.ERROR);

      // Recover via checkpoint
      const recovered = await checkpointManager.retrieveCheckpoint(testQueryId);
      expect(recovered).toBeDefined();
      expect(recovered?.executionContext).toBeDefined();

      // Create new state machine and restore
      const newStateMachine = new QueryStateMachine(testQueryId + '_recovery');
      await newStateMachine.transition('START');

      // Verify recovery possible
      expect(recovered?.state).toBe(QueryState.PAUSED);
    });

    test('should block dangerous commands during workflow', async () => {
      await stateMachine.transition('START');

      // Attempt dangerous command
      const result = await commandExecutor.executeCommand(
        testQueryId,
        'rm -rf /'
      );

      expect(result.success).toBe(false);
      expect(result.blocked).toBe(true);
      expect(result.blockReason).toContain('dangerous');

      // Verify query can continue
      await stateMachine.transition('PAUSE');
      await stateMachine.transition('RESUME');
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);
    });
  });

  describe('Performance validation', () => {
    test('should meet all performance targets in complete workflow', async () => {
      const metrics = {
        stateTransition: 0,
        modelSwitch: 0,
        permissionSwitch: 0,
        checkpointCreate: 0,
        checkpointRetrieve: 0,
        resume: 0
      };

      // State transition (<100ms)
      let start = Date.now();
      await stateMachine.transition('START');
      metrics.stateTransition = Date.now() - start;

      // Model switch (<200ms)
      modelSwitcher.setCurrentModel(ModelType.SONNET);
      start = Date.now();
      await modelSwitcher.switchModel(testQueryId, ModelType.HAIKU, stateMachine);
      metrics.modelSwitch = Date.now() - start;

      // Permission switch (<50ms)
      start = Date.now();
      await permissionManager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);
      metrics.permissionSwitch = Date.now() - start;

      // Checkpoint create (<150ms)
      await stateMachine.transition('PAUSE');
      start = Date.now();
      await checkpointManager.createCheckpoint(testQueryId, stateMachine.getContext());
      metrics.checkpointCreate = Date.now() - start;

      // Checkpoint retrieve (<100ms)
      start = Date.now();
      await checkpointManager.retrieveCheckpoint(testQueryId);
      metrics.checkpointRetrieve = Date.now() - start;

      // Resume (<300ms)
      start = Date.now();
      await resumeManager.resumeQuery(testQueryId);
      metrics.resume = Date.now() - start;

      // Log metrics
      console.log('Performance Metrics:', metrics);

      // Validate targets (using acceptable ranges)
      expect(metrics.stateTransition).toBeLessThan(200); // Target: <100ms, Acceptable: <200ms
      expect(metrics.modelSwitch).toBeLessThan(500); // Target: <200ms, Acceptable: <500ms
      expect(metrics.permissionSwitch).toBeLessThan(100); // Target: <50ms, Acceptable: <100ms
      expect(metrics.checkpointCreate).toBeLessThan(300); // Target: <150ms, Acceptable: <300ms
      expect(metrics.checkpointRetrieve).toBeLessThan(200); // Target: <100ms, Acceptable: <200ms
      expect(metrics.resume).toBeLessThan(500); // Target: <300ms, Acceptable: <500ms
    });

    test('should handle high-load concurrent operations', async () => {
      const queryIds = Array.from({ length: 5 }, (_, i) => `concurrent-${i}`);
      const machines = queryIds.map(id => new QueryStateMachine(id));

      // Start all queries
      await Promise.all(machines.map(m => m.transition('START')));

      // Pause all
      await Promise.all(machines.map(m => m.transition('PAUSE')));

      // Create checkpoints concurrently
      const checkpointPromises = machines.map((m, i) =>
        checkpointManager.createCheckpoint(queryIds[i], m.getContext())
      );
      const checkpoints = await Promise.all(checkpointPromises);

      expect(checkpoints).toHaveLength(5);
      checkpoints.forEach(cp => expect(cp).toBeDefined());

      // Resume all concurrently
      const resumePromises = queryIds.map(id => resumeManager.resumeQuery(id));
      const results = await Promise.all(resumePromises);

      expect(results.every(r => r.success)).toBe(true);
    });
  });

  describe('System integration', () => {
    test('should integrate registry, state machine, and checkpoint system', async () => {
      // Register query
      await queryRegistry.registerQuery(testQueryId, {
        userId: 'integration-user',
        projectId: 'integration-project'
      });

      // Start state machine
      await stateMachine.transition('START');

      // Update and checkpoint
      stateMachine.updateContext({
        metadata: { integration_test: true, step: 1 }
      });

      await stateMachine.transition('PAUSE');
      const checkpoint = await checkpointManager.createCheckpoint(
        testQueryId,
        stateMachine.getContext()
      );

      // Verify all systems have consistent data
      const query = await queryRegistry.getQuery(testQueryId);
      const retrieved = await checkpointManager.retrieveCheckpoint(testQueryId);

      expect(query?.queryId).toBe(testQueryId);
      expect(retrieved?.queryId).toBe(testQueryId);
      expect(stateMachine.getState()).toBe(QueryState.PAUSED);
    });

    test('should coordinate model switching with permission changes', async () => {
      await stateMachine.transition('START');

      // Switch to PLAN mode (no editing)
      await permissionManager.switchMode(testQueryId, PermissionMode.PLAN);

      const planCapabilities = permissionManager.getModeCapabilities(PermissionMode.PLAN);
      expect(planCapabilities.editingAllowed).toBe(false);

      // Model switch should still work
      modelSwitcher.setCurrentModel(ModelType.SONNET);
      const modelResult = await modelSwitcher.switchModel(
        testQueryId,
        ModelType.HAIKU,
        stateMachine
      );
      expect(modelResult.success).toBe(true);

      // Switch to ACCEPT_EDITS (editing allowed)
      await permissionManager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);

      const editCapabilities = permissionManager.getModeCapabilities(PermissionMode.ACCEPT_EDITS);
      expect(editCapabilities.editingAllowed).toBe(true);
    });

    test('should track complete workflow statistics', async () => {
      await stateMachine.transition('START');

      // Execute multiple operations
      await modelSwitcher.switchModel(testQueryId, ModelType.HAIKU, stateMachine);
      await modelSwitcher.switchModel(testQueryId, ModelType.OPUS, stateMachine);
      await permissionManager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);
      await permissionManager.switchMode(testQueryId, PermissionMode.BYPASS_PERMISSIONS);
      await commandExecutor.executeCommand(testQueryId, 'echo test1');
      await commandExecutor.executeCommand(testQueryId, 'echo test2');
      await commandExecutor.executeCommand(testQueryId, 'rm -rf /'); // blocked

      // Collect statistics
      const modelStats = modelSwitcher.getStatistics();
      const permStats = permissionManager.getStatistics();
      const cmdStats = commandExecutor.getStatistics();
      const checkpointStats = await checkpointManager.getStatistics();

      expect(modelStats.currentModel).toBe(ModelType.OPUS);
      expect(permStats.currentMode).toBe(PermissionMode.BYPASS_PERMISSIONS);
      expect(cmdStats.totalCommands).toBe(3);
      expect(cmdStats.successfulCommands).toBe(2);
      expect(cmdStats.failedCommands).toBe(1);
      expect(checkpointStats).toBeDefined();
    });
  });

  describe('Data integrity', () => {
    test('should preserve query context through pause-resume cycles', async () => {
      await stateMachine.transition('START');

      const originalContext = {
        metadata: { testData: 'important', iteration: 42 },
        execution: {
          agentStates: new Map([['agent-1', { status: 'active' }]]),
          taskQueue: [{ id: 'task-1', type: 'test', status: 'pending' as const }],
          completedTasks: []
        }
      };

      stateMachine.updateContext(originalContext);

      await stateMachine.transition('PAUSE');
      const checkpoint = await checkpointManager.createCheckpoint(
        testQueryId,
        stateMachine.getContext()
      );

      await resumeManager.resumeQuery(testQueryId);

      const retrieved = await checkpointManager.retrieveCheckpoint(testQueryId);
      expect(retrieved?.executionContext.taskQueue).toHaveLength(1);
      expect(Object.keys(retrieved?.executionContext.agentStates || {})).toHaveLength(1);
    });

    test('should validate checkpoint data consistency', async () => {
      await stateMachine.transition('START');

      modelSwitcher.setCurrentModel(ModelType.SONNET);
      permissionManager.setCurrentMode(PermissionMode.ACCEPT_EDITS);

      stateMachine.updateContext({
        metadata: { checkpoint_test: true },
        model: {
          currentModel: ModelType.SONNET,
          permissionMode: PermissionMode.ACCEPT_EDITS
        }
      });

      await stateMachine.transition('PAUSE');
      const checkpoint = await checkpointManager.createCheckpoint(
        testQueryId,
        stateMachine.getContext()
      );

      // Validate checkpoint data
      expect(checkpoint.state).toBe(QueryState.PAUSED);
      expect(checkpoint.modelConfig).toBeDefined();
      expect(checkpoint.embedding).toHaveLength(384);
      expect(checkpoint.embedding.every(v => v >= 0 && v <= 1)).toBe(true);

      // Validate retrieval
      const retrieved = await checkpointManager.retrieveCheckpoint(testQueryId);
      expect(retrieved?.queryId).toBe(checkpoint.queryId);
      expect(retrieved?.timestamp).toBe(checkpoint.timestamp);
    });
  });
});
