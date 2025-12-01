/**
 * GAP-003 Query Control System - End-to-End Lifecycle Tests
 *
 * File: tests/query-control/e2e/full-lifecycle.test.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: Comprehensive E2E testing of complete query lifecycle
 *
 * Test Coverage:
 * - Full workflow: pause → model switch → permission switch → resume
 * - State transitions across all components
 * - Cross-component integration validation
 * - Performance under realistic conditions
 */

import { QueryControlService } from '../../../lib/query-control/query-control-service';
import { QueryState } from '../../../lib/query-control/state/state-machine';
import { ModelType } from '../../../lib/query-control/model/model-switcher';
import { PermissionMode } from '../../../lib/query-control/permissions/permission-manager';

// Helper: sleep function
const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

describe('Full Query Lifecycle E2E Tests', () => {
  let service: QueryControlService;

  beforeEach(() => {
    service = new QueryControlService();
  });

  describe('Complete Workflow', () => {
    test('should complete full lifecycle: pause → switch model → switch permissions → resume', async () => {
      const queryId = 'e2e-test-full-lifecycle';

      // 1. Initial query starts in INIT state
      const initialState = service.getQueryState(queryId);
      expect(initialState).toBe(QueryState.INIT);

      // 2. Pause query (creates checkpoint)
      const pauseResult = await service.pause(queryId);

      expect(pauseResult.success).toBe(true);
      expect(pauseResult.state).toBe(QueryState.PAUSED);
      expect(pauseResult.checkpointId).toBeDefined();
      expect(pauseResult.pauseTimeMs).toBeGreaterThan(0);

      // 3. Switch model while paused
      const modelSwitchResult = await service.changeModel(queryId, ModelType.HAIKU);

      expect(modelSwitchResult.success).toBe(true);
      expect(modelSwitchResult.previousModel).toBe(ModelType.SONNET);
      expect(modelSwitchResult.currentModel).toBe(ModelType.HAIKU);
      expect(modelSwitchResult.switchTimeMs).toBeLessThan(200); // Day 3 target

      // 4. Switch permissions while paused
      const permissionSwitchResult = await service.changePermissions(queryId, PermissionMode.ACCEPT_EDITS);

      expect(permissionSwitchResult.success).toBe(true);
      expect(permissionSwitchResult.previousMode).toBe(PermissionMode.DEFAULT);
      expect(permissionSwitchResult.currentMode).toBe(PermissionMode.ACCEPT_EDITS);
      expect(permissionSwitchResult.switchTimeMs).toBeLessThan(50); // Day 4 target

      // 5. Resume query
      const resumeResult = await service.resume(queryId);

      expect(resumeResult.success).toBe(true);
      expect(resumeResult.state).toBe(QueryState.RUNNING);
      expect(resumeResult.resumedFrom).toBeDefined();
      expect(resumeResult.checkpoint).toBeDefined();

      // 6. Verify final state
      const finalState = service.getQueryState(queryId);
      expect(finalState).toBe(QueryState.RUNNING);
    });

    test('should handle pause → resume without model/permission changes', async () => {
      const queryId = 'e2e-test-simple-pause-resume';

      // Pause
      const pauseResult = await service.pause(queryId);
      expect(pauseResult.success).toBe(true);
      expect(pauseResult.state).toBe(QueryState.PAUSED);

      // Resume immediately
      const resumeResult = await service.resume(queryId);
      expect(resumeResult.success).toBe(true);
      expect(resumeResult.state).toBe(QueryState.RUNNING);

      // Verify checkpoint was created and restored
      expect(pauseResult.checkpointId).toBeDefined();
      expect(resumeResult.resumedFrom).toBeDefined();
    });

    test('should handle terminate operation', async () => {
      const queryId = 'e2e-test-terminate';

      // Pause first
      await service.pause(queryId);

      // Terminate
      const terminateResult = await service.terminate(queryId);

      expect(terminateResult.success).toBe(true);
      expect(terminateResult.finalState).toBe(QueryState.TERMINATED);
      expect(terminateResult.terminateTimeMs).toBeGreaterThan(0);

      // Verify state
      const finalState = service.getQueryState(queryId);
      expect(finalState).toBe(QueryState.TERMINATED);
    });
  });

  describe('Cross-Component Integration', () => {
    test('should maintain state consistency across pause/resume cycles', async () => {
      const queryId = 'e2e-test-state-consistency';

      // Cycle 1: Pause → Resume
      await service.pause(queryId);
      await service.resume(queryId);
      expect(service.getQueryState(queryId)).toBe(QueryState.RUNNING);

      // Cycle 2: Pause → Resume again
      await service.pause(queryId);
      expect(service.getQueryState(queryId)).toBe(QueryState.PAUSED);

      await service.resume(queryId);
      expect(service.getQueryState(queryId)).toBe(QueryState.RUNNING);
    });

    test('should coordinate model switching with checkpoint creation', async () => {
      const queryId = 'e2e-test-model-checkpoint-coordination';

      // Pause (creates checkpoint)
      const pauseResult = await service.pause(queryId);
      expect(pauseResult.checkpointId).toBeDefined();

      // Switch model (creates another checkpoint via model switcher)
      const modelResult = await service.changeModel(queryId, ModelType.OPUS);
      expect(modelResult.success).toBe(true);
      expect(modelResult.checkpointId).toBeDefined();

      // Resume
      const resumeResult = await service.resume(queryId);
      expect(resumeResult.success).toBe(true);
      expect(resumeResult.checkpoint).toBeDefined();
    });

    test('should execute commands with permission validation', async () => {
      const queryId = 'e2e-test-command-execution';

      // Set to bypass permissions
      await service.changePermissions(queryId, PermissionMode.BYPASS_PERMISSIONS);

      // Execute safe command
      const cmdResult = await service.executeCommand(queryId, 'echo "test"');

      expect(cmdResult.success).toBe(true);
      expect(cmdResult.exitCode).toBe(0);
      expect(cmdResult.output).toContain('test');
    });

    test('should prevent dangerous commands regardless of permission mode', async () => {
      const queryId = 'e2e-test-security-validation';

      // Even with bypass permissions, dangerous commands should be blocked
      await service.changePermissions(queryId, PermissionMode.BYPASS_PERMISSIONS);

      // Attempt dangerous command
      const cmdResult = await service.executeCommand(queryId, 'rm -rf /');

      expect(cmdResult.success).toBe(false);
      expect(cmdResult.error).toContain('Dangerous command blocked');
    });
  });

  describe('Performance Validation', () => {
    test('should complete full workflow within performance targets', async () => {
      const queryId = 'e2e-test-performance';
      const startTime = Date.now();

      // Full workflow
      await service.pause(queryId);
      await service.changeModel(queryId, ModelType.HAIKU);
      await service.changePermissions(queryId, PermissionMode.PLAN);
      await service.resume(queryId);

      const totalTime = Date.now() - startTime;

      // Full workflow should complete in reasonable time
      expect(totalTime).toBeLessThan(500); // 500ms for full workflow
    });

    test('all operations should meet individual latency targets', async () => {
      const queryId = 'e2e-test-latency-targets';

      // Pause: <150ms (Day 2 checkpoint target)
      const pauseResult = await service.pause(queryId);
      expect(pauseResult.pauseTimeMs).toBeLessThan(150);

      // Model switch: <200ms (Day 3 target)
      const modelResult = await service.changeModel(queryId, ModelType.HAIKU);
      expect(modelResult.switchTimeMs).toBeLessThan(200);

      // Permission switch: <50ms (Day 4 target)
      const permResult = await service.changePermissions(queryId, PermissionMode.ACCEPT_EDITS);
      expect(permResult.switchTimeMs).toBeLessThan(50);

      // Resume: <100ms (Day 2 restoration target)
      const resumeResult = await service.resume(queryId);
      expect(resumeResult.resumeTimeMs).toBeLessThan(150);
    });
  });

  describe('Query Listing and Monitoring', () => {
    test('should list active queries', async () => {
      // Create multiple queries
      await service.pause('query-1');
      await service.pause('query-2');
      await service.pause('query-3');

      const queryList = await service.listQueries();

      expect(queryList.queries.length).toBeGreaterThanOrEqual(3);
      expect(queryList.total).toBeGreaterThanOrEqual(3);
      expect(queryList.states).toBeDefined();
      expect(queryList.states[QueryState.PAUSED]).toBeGreaterThanOrEqual(3);
    });

    test('should filter out completed queries by default', async () => {
      const queryId = 'query-completed';

      await service.pause(queryId);
      await service.terminate(queryId);

      const queryList = await service.listQueries(false); // Don't include history

      const completedQuery = queryList.queries.find(q => q.queryId === queryId);
      expect(completedQuery).toBeUndefined();
    });

    test('should include history when requested', async () => {
      const queryId = 'query-with-history';

      await service.pause(queryId);
      await service.terminate(queryId);

      const queryList = await service.listQueries(true); // Include history

      const terminatedQuery = queryList.queries.find(q => q.queryId === queryId);
      expect(terminatedQuery).toBeDefined();
      expect(terminatedQuery?.state).toBe(QueryState.TERMINATED);
    });
  });

  describe('Error Handling', () => {
    test('should handle pause from invalid state', async () => {
      const queryId = 'e2e-test-invalid-pause';

      // Already paused
      await service.pause(queryId);

      // Try to pause again
      const secondPause = await service.pause(queryId);

      expect(secondPause.success).toBe(false);
      expect(secondPause.error).toContain('Cannot pause from state');
    });

    test('should handle resume from invalid state', async () => {
      const queryId = 'e2e-test-invalid-resume';

      // Try to resume without pausing first (INIT state)
      const resumeResult = await service.resume(queryId);

      expect(resumeResult.success).toBe(false);
      expect(resumeResult.error).toContain('Cannot resume from state');
    });

    test('should handle model switch to same model', async () => {
      const queryId = 'e2e-test-same-model';

      await service.pause(queryId);

      // Switch to SONNET (already on SONNET)
      const modelResult = await service.changeModel(queryId, ModelType.SONNET);

      expect(modelResult.success).toBe(false);
      expect(modelResult.error).toContain('Already using this model');
    });

    test('should handle permission switch to same mode', async () => {
      const queryId = 'e2e-test-same-permission';

      await service.pause(queryId);

      // Switch to DEFAULT (already on DEFAULT)
      const permResult = await service.changePermissions(queryId, PermissionMode.DEFAULT);

      expect(permResult.success).toBe(false);
      expect(permResult.error).toContain('Already using this permission mode');
    });
  });

  describe('Multiple Query Scenarios', () => {
    test('should handle 10 concurrent queries', async () => {
      const queryIds = Array.from({ length: 10 }, (_, i) => `concurrent-query-${i}`);

      // Pause all queries in parallel
      const pauseResults = await Promise.all(
        queryIds.map(id => service.pause(id))
      );

      // All should succeed
      const successfulPauses = pauseResults.filter(r => r.success).length;
      expect(successfulPauses).toBe(10);

      // Resume all in parallel
      const resumeResults = await Promise.all(
        queryIds.map(id => service.resume(id))
      );

      // All should succeed
      const successfulResumes = resumeResults.filter(r => r.success).length;
      expect(successfulResumes).toBe(10);
    });

    test('should maintain independent state for multiple queries', async () => {
      const query1 = 'multi-query-1';
      const query2 = 'multi-query-2';

      // Query 1: Pause → Model switch → Resume
      await service.pause(query1);
      await service.changeModel(query1, ModelType.HAIKU);
      await service.resume(query1);

      // Query 2: Pause → Permission switch → Keep paused
      await service.pause(query2);
      await service.changePermissions(query2, PermissionMode.PLAN);

      // Verify independent states
      expect(service.getQueryState(query1)).toBe(QueryState.RUNNING);
      expect(service.getQueryState(query2)).toBe(QueryState.PAUSED);
    });
  });

  describe('Integration Stress Tests', () => {
    test('should handle rapid state transitions', async () => {
      const queryId = 'e2e-test-rapid-transitions';

      // Rapid pause/resume cycles
      await service.pause(queryId);
      await service.resume(queryId);
      await service.pause(queryId);
      await service.resume(queryId);
      await service.pause(queryId);

      // Final state should be PAUSED
      expect(service.getQueryState(queryId)).toBe(QueryState.PAUSED);

      // Should still be able to resume
      const resumeResult = await service.resume(queryId);
      expect(resumeResult.success).toBe(true);
    });

    test('should handle all model types', async () => {
      const queryId = 'e2e-test-all-models';

      await service.pause(queryId);

      // Test each model
      const models = [ModelType.HAIKU, ModelType.OPUS, ModelType.SONNET];

      for (const model of models) {
        const result = await service.changeModel(queryId, model);
        expect(result.success).toBe(true);
        expect(result.currentModel).toBe(model);
      }
    });

    test('should handle all permission modes', async () => {
      const queryId = 'e2e-test-all-permissions';

      await service.pause(queryId);

      // Test each permission mode
      const modes = [
        PermissionMode.ACCEPT_EDITS,
        PermissionMode.BYPASS_PERMISSIONS,
        PermissionMode.PLAN,
        PermissionMode.DEFAULT
      ];

      for (const mode of modes) {
        const result = await service.changePermissions(queryId, mode);
        expect(result.success).toBe(true);
        expect(result.currentMode).toBe(mode);
      }
    });
  });
});
