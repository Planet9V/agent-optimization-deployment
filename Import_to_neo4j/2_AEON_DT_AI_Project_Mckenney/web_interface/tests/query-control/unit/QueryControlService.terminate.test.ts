/**
 * GAP-003 Query Control System - Terminate Operation Unit Tests
 *
 * File: tests/query-control/unit/QueryControlService.terminate.test.ts
 * Created: 2025-11-14
 * Version: v1.0.0
 * Purpose: Comprehensive unit tests for QueryControlService.terminate() operation
 *
 * Constitutional Compliance:
 * - DILIGENCE: Complete test coverage for all terminate scenarios
 * - INTEGRITY: Validates accurate state transitions and cleanup
 * - NO DEVELOPMENT THEATER: Production-grade unit testing with >90% coverage
 *
 * Test Coverage:
 * - Success scenarios from all valid states (INIT, RUNNING, PAUSED, ERROR)
 * - State cleanup and registry updates
 * - Performance profiling (<100ms target)
 * - Error handling (already terminated, state transition failures)
 * - Concurrent termination scenarios
 *
 * Lines Tested: lib/query-control/query-control-service.ts:639-726
 */

import { describe, test, expect, beforeEach, afterEach, jest } from '@jest/globals';
import { QueryControlService } from '../../../lib/query-control/query-control-service';
import { QueryStateMachine, QueryState } from '../../../lib/query-control/state/state-machine';

describe('QueryControlService.terminate() Unit Tests', () => {
  let service: QueryControlService;

  // Mock console to reduce test output noise
  const consoleSpy = {
    log: jest.spyOn(console, 'log').mockImplementation(),
    error: jest.spyOn(console, 'error').mockImplementation()
  };

  beforeEach(() => {
    service = new QueryControlService();
    consoleSpy.log.mockClear();
    consoleSpy.error.mockClear();
  });

  afterEach(async () => {
    // Access private registry for cleanup
    const registry = (service as any).queryRegistry;
    if (registry && typeof registry.clear === 'function') {
      await registry.clear();
    }

    // Clear state machines
    const stateMachines = (service as any).stateMachines;
    if (stateMachines) {
      stateMachines.clear();
    }

    jest.clearAllMocks();
  });

  describe('Success Scenarios', () => {
    test('should successfully terminate query from RUNNING state', async () => {
      const queryId = 'terminate-test-001';

      // Access internal registry
      const registry = (service as any).queryRegistry;

      // Register query in RUNNING state
      await registry.registerQuery(queryId, {
        state: QueryState.RUNNING,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 3,
        taskCount: 5,
        checkpointCount: 0
      });

      // Create state machine and transition to RUNNING
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);

      // Register state machine with service (simulate internal state)
      (service as any).stateMachines.set(queryId, stateMachine);

      // Execute terminate
      const startTime = Date.now();
      const result = await service.terminate(queryId);
      const duration = Date.now() - startTime;

      // Verify success result
      expect(result.success).toBe(true);
      expect(result.finalState).toBe(QueryState.TERMINATED);
      expect(result.terminateTimeMs).toBeGreaterThanOrEqual(0); // Can be 0ms for very fast operations
      expect(result.terminateTimeMs).toBeLessThan(100); // <100ms performance target
      expect(result.error).toBeUndefined();

      // Verify state machine transitioned to TERMINATED
      expect(stateMachine.getState()).toBe(QueryState.TERMINATED);

      // Verify registry was updated
      const queryMetadata = await registry.getQuery(queryId);
      expect(queryMetadata?.state).toBe(QueryState.TERMINATED);
      expect(queryMetadata?.metadata?.terminatedAt).toBeDefined();
      expect(queryMetadata?.metadata?.terminatedAt).toBeGreaterThan(startTime);
    });

    test('should successfully terminate query from PAUSED state', async () => {
      const queryId = 'terminate-test-002';

      // Access internal registry
      const registry = (service as any).queryRegistry;

      // Register query
      await registry.registerQuery(queryId, {
        state: QueryState.INIT,
        model: 'haiku',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 2,
        taskCount: 3,
        checkpointCount: 1
      });

      // Create state machine and transition to PAUSED
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START'); // INIT → RUNNING
      await stateMachine.transition('PAUSE'); // RUNNING → PAUSED
      expect(stateMachine.getState()).toBe(QueryState.PAUSED);

      // Register state machine
      (service as any).stateMachines.set(queryId, stateMachine);

      // Execute terminate
      const result = await service.terminate(queryId);

      // Verify success
      expect(result.success).toBe(true);
      expect(result.finalState).toBe(QueryState.TERMINATED);
      expect(result.terminateTimeMs).toBeLessThan(100);

      // Verify state transition
      expect(stateMachine.getState()).toBe(QueryState.TERMINATED);
    });

    test('should successfully terminate query from INIT state (auto-start then terminate)', async () => {
      const queryId = 'terminate-test-003';

      // Access internal registry
      const registry = (service as any).queryRegistry;

      // Register query in INIT state
      await registry.registerQuery(queryId, {
        state: QueryState.INIT,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 1,
        taskCount: 1,
        checkpointCount: 0
      });

      // Create state machine in INIT state (no transitions)
      const stateMachine = new QueryStateMachine(queryId);
      expect(stateMachine.getState()).toBe(QueryState.INIT);

      // Register state machine
      (service as any).stateMachines.set(queryId, stateMachine);

      // Execute terminate (should auto-start then terminate)
      const result = await service.terminate(queryId);

      // Verify success
      expect(result.success).toBe(true);
      expect(result.finalState).toBe(QueryState.TERMINATED);

      // Verify state machine went from INIT → RUNNING → TERMINATED
      expect(stateMachine.getState()).toBe(QueryState.TERMINATED);
    });

    test('should successfully terminate query from ERROR state (recovery scenario)', async () => {
      const queryId = 'terminate-test-004';

      // Create state machine and force ERROR state
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START'); // INIT → RUNNING
      await stateMachine.transition('ERROR'); // RUNNING → ERROR
      expect(stateMachine.getState()).toBe(QueryState.ERROR);

      // Register state machine
      (service as any).stateMachines.set(queryId, stateMachine);

      // Execute terminate (recovery from error)
      const result = await service.terminate(queryId);

      // Verify success
      expect(result.success).toBe(true);
      expect(result.finalState).toBe(QueryState.TERMINATED);
      expect(stateMachine.getState()).toBe(QueryState.TERMINATED);
    });

    test('should create state machine if not exists (for new queries)', async () => {
      const queryId = 'terminate-test-005';

      // Access internal registry
      const registry = (service as any).queryRegistry;

      // Register query but don't create state machine
      await registry.registerQuery(queryId, {
        state: QueryState.INIT,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 1,
        taskCount: 1,
        checkpointCount: 0
      });

      // Verify state machine doesn't exist yet
      expect((service as any).stateMachines.has(queryId)).toBe(false);

      // Execute terminate (should create state machine internally)
      const result = await service.terminate(queryId);

      // Verify success
      expect(result.success).toBe(true);
      expect(result.finalState).toBe(QueryState.TERMINATED);

      // Verify state machine was created
      expect((service as any).stateMachines.has(queryId)).toBe(true);
      const stateMachine = (service as any).stateMachines.get(queryId);
      expect(stateMachine.getState()).toBe(QueryState.TERMINATED);
    });
  });

  describe('State Cleanup', () => {
    test('should update registry with terminatedAt timestamp', async () => {
      const queryId = 'cleanup-test-001';

      // Access internal registry
      const registry = (service as any).queryRegistry;

      // Setup
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      (service as any).stateMachines.set(queryId, stateMachine);

      // Execute terminate
      const beforeTerminate = Date.now();
      await service.terminate(queryId);
      const afterTerminate = Date.now();

      // Verify registry update
      const queryMetadata = await registry.getQuery(queryId);
      expect(queryMetadata?.state).toBe(QueryState.TERMINATED);
      expect(queryMetadata?.metadata?.terminatedAt).toBeDefined();

      // Verify timestamp is accurate
      const terminatedAt = queryMetadata.metadata.terminatedAt;
      expect(terminatedAt).toBeGreaterThanOrEqual(beforeTerminate);
      expect(terminatedAt).toBeLessThanOrEqual(afterTerminate);
    });

    test('should maintain state machine in registry even after termination', async () => {
      const queryId = 'cleanup-test-002';

      // Setup
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      (service as any).stateMachines.set(queryId, stateMachine);

      // Execute terminate
      await service.terminate(queryId);

      // Verify state machine still exists (not removed)
      expect((service as any).stateMachines.has(queryId)).toBe(true);
      const retrievedMachine = (service as any).stateMachines.get(queryId);
      expect(retrievedMachine.getState()).toBe(QueryState.TERMINATED);
    });
  });

  describe('Error Handling', () => {
    test('should handle already terminated query gracefully', async () => {
      const queryId = 'error-test-001';

      // Create already terminated state machine
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      await stateMachine.transition('TERMINATE');
      expect(stateMachine.getState()).toBe(QueryState.TERMINATED);
      (service as any).stateMachines.set(queryId, stateMachine);

      // Mock transition to throw error
      jest.spyOn(stateMachine, 'transition').mockRejectedValueOnce(
        new Error('Cannot terminate from TERMINATED state')
      );

      // Execute terminate again (should fail gracefully)
      const result = await service.terminate(queryId);

      // Verify graceful failure
      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
      expect(result.error).toContain('terminate');
      expect(result.finalState).toBe(QueryState.TERMINATED);
    });

    test('should handle state transition errors', async () => {
      const queryId = 'error-test-002';

      // Setup
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      (service as any).stateMachines.set(queryId, stateMachine);

      // Mock transition to throw error
      const testError = new Error('State transition failed');
      jest.spyOn(stateMachine, 'transition').mockRejectedValueOnce(testError);

      // Execute terminate
      const result = await service.terminate(queryId);

      // Verify error handling
      expect(result.success).toBe(false);
      expect(result.error).toBe('State transition failed');
      expect(result.terminateTimeMs).toBeGreaterThanOrEqual(0);
    });

    test('should handle non-Error exceptions gracefully', async () => {
      const queryId = 'error-test-003';

      // Setup
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      (service as any).stateMachines.set(queryId, stateMachine);

      // Mock transition to throw non-Error
      jest.spyOn(stateMachine, 'transition').mockRejectedValueOnce('String error');

      // Execute terminate
      const result = await service.terminate(queryId);

      // Verify error handling
      expect(result.success).toBe(false);
      expect(result.error).toBe('Unknown error');
    });

    test('should return current state on failure', async () => {
      const queryId = 'error-test-004';

      // Setup in RUNNING state
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);
      (service as any).stateMachines.set(queryId, stateMachine);

      // Mock transition to throw error
      jest.spyOn(stateMachine, 'transition').mockRejectedValueOnce(
        new Error('Termination blocked')
      );

      // Execute terminate (should fail)
      const result = await service.terminate(queryId);

      // Verify finalState reflects current state (RUNNING) not TERMINATED
      expect(result.success).toBe(false);
      expect(result.finalState).toBe(QueryState.RUNNING);
    });
  });

  describe('Performance Benchmarks', () => {
    test('should meet <100ms performance target for terminate operation', async () => {
      const queryId = 'profiler-test-001';

      // Setup
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      (service as any).stateMachines.set(queryId, stateMachine);

      // Execute terminate
      const startTime = Date.now();
      const result = await service.terminate(queryId);
      const duration = Date.now() - startTime;

      // Verify performance target met
      expect(duration).toBeLessThan(100); // <100ms target
      expect(result.terminateTimeMs).toBeLessThan(100);
    });

    test('should terminate 10 queries in under 1 second total', async () => {
      const queryIds = Array.from({ length: 10 }, (_, i) => `bench-test-${i}`);

      // Setup all queries
      for (const queryId of queryIds) {
        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        (service as any).stateMachines.set(queryId, stateMachine);
      }

      // Terminate all queries
      const startTime = Date.now();
      const results = await Promise.all(
        queryIds.map(id => service.terminate(id))
      );
      const totalDuration = Date.now() - startTime;

      // Verify all succeeded
      results.forEach(result => {
        expect(result.success).toBe(true);
        expect(result.finalState).toBe(QueryState.TERMINATED);
      });

      // Verify total time under 1 second
      expect(totalDuration).toBeLessThan(1000);
    });

    test('should maintain performance under concurrent termination', async () => {
      const queryIds = Array.from({ length: 5 }, (_, i) => `concurrent-test-${i}`);

      // Setup all queries
      for (const queryId of queryIds) {
        const stateMachine = new QueryStateMachine(queryId);
        await stateMachine.transition('START');
        (service as any).stateMachines.set(queryId, stateMachine);
      }

      // Terminate concurrently
      const results = await Promise.all(
        queryIds.map(id => service.terminate(id))
      );

      // Verify all met performance target individually
      results.forEach(result => {
        expect(result.success).toBe(true);
        expect(result.terminateTimeMs).toBeLessThan(100);
      });
    });
  });

  describe('Integration with Other Operations', () => {
    test('should successfully terminate after pause operation', async () => {
      const queryId = 'integration-test-001';

      // Setup and pause
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');
      (service as any).stateMachines.set(queryId, stateMachine);

      // Terminate from paused state
      const result = await service.terminate(queryId);

      // Verify success
      expect(result.success).toBe(true);
      expect(result.finalState).toBe(QueryState.TERMINATED);
    });

    test('should successfully terminate from error recovery scenario', async () => {
      const queryId = 'integration-test-002';

      // Setup and transition to ERROR
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      await stateMachine.transition('ERROR');
      expect(stateMachine.getState()).toBe(QueryState.ERROR);
      (service as any).stateMachines.set(queryId, stateMachine);

      // Terminate from error state
      const result = await service.terminate(queryId);

      // Verify successful recovery termination
      expect(result.success).toBe(true);
      expect(result.finalState).toBe(QueryState.TERMINATED);
    });
  });

  describe('Console Output Verification', () => {
    test('should log successful termination', async () => {
      const queryId = 'console-test-001';

      // Setup
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      (service as any).stateMachines.set(queryId, stateMachine);

      // Execute terminate
      await service.terminate(queryId);

      // Verify console log was called
      expect(consoleSpy.log).toHaveBeenCalled();
      const logCalls = consoleSpy.log.mock.calls;
      const terminateLog = logCalls.find(call =>
        call[0]?.includes(`Query ${queryId} terminated`)
      );
      expect(terminateLog).toBeDefined();
    });

    test('should log error on termination failure', async () => {
      const queryId = 'console-test-002';

      // Setup
      const stateMachine = new QueryStateMachine(queryId);
      await stateMachine.transition('START');
      (service as any).stateMachines.set(queryId, stateMachine);

      // Mock to throw error
      jest.spyOn(stateMachine, 'transition').mockRejectedValueOnce(
        new Error('Test error')
      );

      // Execute terminate
      await service.terminate(queryId);

      // Verify console error was called
      expect(consoleSpy.error).toHaveBeenCalled();
      const errorCalls = consoleSpy.error.mock.calls;
      const terminateError = errorCalls.find(call =>
        call[0]?.includes(`Failed to terminate query ${queryId}`)
      );
      expect(terminateError).toBeDefined();
    });
  });
});
