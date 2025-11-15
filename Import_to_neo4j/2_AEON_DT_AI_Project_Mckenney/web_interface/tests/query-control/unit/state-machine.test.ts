/**
 * GAP-003 Query Control System - State Machine Unit Tests
 *
 * File: tests/query-control/unit/state-machine.test.ts
 * Created: 2025-11-14
 * Version: v1.0.0
 * Purpose: Comprehensive unit tests for QueryStateMachine
 *
 * Constitutional Compliance:
 * - DILIGENCE: >90% code coverage
 * - INTEGRITY: All edge cases tested
 * - NO DEVELOPMENT THEATER: Production-grade tests
 */

import { describe, test, expect, beforeEach } from '@jest/globals';
import {
  QueryStateMachine,
  QueryState,
  createStateMachine,
  type QueryContext,
  type StateChangeEvent
} from '../../../lib/query-control/state/state-machine';

describe('QueryStateMachine', () => {
  let stateMachine: QueryStateMachine;
  const testQueryId = 'test-query-001';

  beforeEach(() => {
    stateMachine = new QueryStateMachine(testQueryId);
  });

  describe('Initialization', () => {
    test('should start in INIT state', () => {
      expect(stateMachine.getState()).toBe(QueryState.INIT);
    });

    test('should set query ID in context', () => {
      const context = stateMachine.getContext();
      expect(context.queryId).toBe(testQueryId);
    });

    test('should initialize with custom context', () => {
      const customContext = {
        model: 'sonnet',
        permissionMode: 'default',
        agentCount: 5
      };
      const sm = new QueryStateMachine(testQueryId, customContext);
      const context = sm.getContext();
      expect(context.model).toBe('sonnet');
      expect(context.permissionMode).toBe('default');
      expect(context.agentCount).toBe(5);
    });

    test('should initialize with empty history', () => {
      expect(stateMachine.getHistory()).toEqual([]);
    });
  });

  describe('State Transitions', () => {
    test('should transition from INIT to RUNNING', async () => {
      const result = await stateMachine.transition('START');
      expect(result).toBe(true);
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);
    });

    test('should transition from RUNNING to PAUSED', async () => {
      await stateMachine.transition('START');
      const result = await stateMachine.transition('PAUSE');
      expect(result).toBe(true);
      expect(stateMachine.getState()).toBe(QueryState.PAUSED);
    });

    test('should transition from PAUSED to RUNNING', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');
      const result = await stateMachine.transition('RESUME');
      expect(result).toBe(true);
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);
    });

    test('should transition from RUNNING to COMPLETED', async () => {
      await stateMachine.transition('START');
      const result = await stateMachine.transition('COMPLETE');
      expect(result).toBe(true);
      expect(stateMachine.getState()).toBe(QueryState.COMPLETED);
    });

    test('should transition from RUNNING to TERMINATED', async () => {
      await stateMachine.transition('START');
      const result = await stateMachine.transition('TERMINATE');
      expect(result).toBe(true);
      expect(stateMachine.getState()).toBe(QueryState.TERMINATED);
    });

    test('should transition from RUNNING to ERROR', async () => {
      await stateMachine.transition('START');
      const result = await stateMachine.transition('ERROR');
      expect(result).toBe(true);
      expect(stateMachine.getState()).toBe(QueryState.ERROR);
    });

    test('should transition from PAUSED to TERMINATED', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');
      const result = await stateMachine.transition('TERMINATE');
      expect(result).toBe(true);
      expect(stateMachine.getState()).toBe(QueryState.TERMINATED);
    });

    test('should transition from INIT to ERROR', async () => {
      const result = await stateMachine.transition('ERROR');
      expect(result).toBe(true);
      expect(stateMachine.getState()).toBe(QueryState.ERROR);
    });
  });

  describe('Invalid Transitions', () => {
    test('should reject PAUSE from INIT state', async () => {
      await expect(stateMachine.transition('PAUSE'))
        .rejects.toThrow('Invalid transition');
    });

    test('should reject RESUME from INIT state', async () => {
      await expect(stateMachine.transition('RESUME'))
        .rejects.toThrow('Invalid transition');
    });

    test('should reject START from RUNNING state', async () => {
      await stateMachine.transition('START');
      await expect(stateMachine.transition('START'))
        .rejects.toThrow('Invalid transition');
    });

    test('should reject RESUME from RUNNING state', async () => {
      await stateMachine.transition('START');
      await expect(stateMachine.transition('RESUME'))
        .rejects.toThrow('Invalid transition');
    });

    test('should reject START from COMPLETED state', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('COMPLETE');
      await expect(stateMachine.transition('START'))
        .rejects.toThrow('Invalid transition');
    });

    test('should reject any transition from COMPLETED (terminal state)', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('COMPLETE');
      await expect(stateMachine.transition('PAUSE'))
        .rejects.toThrow('Invalid transition');
    });

    test('should reject any transition from TERMINATED (terminal state)', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('TERMINATE');
      await expect(stateMachine.transition('RESUME'))
        .rejects.toThrow('Invalid transition');
    });
  });

  describe('History Tracking', () => {
    test('should record state changes in history', async () => {
      await stateMachine.transition('START');
      const history = stateMachine.getHistory();

      expect(history).toHaveLength(1);
      expect(history[0].from).toBe(QueryState.INIT);
      expect(history[0].to).toBe(QueryState.RUNNING);
      expect(history[0].action).toBe('START');
      expect(history[0].queryId).toBe(testQueryId);
    });

    test('should maintain complete transition history', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');
      await stateMachine.transition('RESUME');

      const history = stateMachine.getHistory();
      expect(history).toHaveLength(3);

      expect(history[0].from).toBe(QueryState.INIT);
      expect(history[0].to).toBe(QueryState.RUNNING);

      expect(history[1].from).toBe(QueryState.RUNNING);
      expect(history[1].to).toBe(QueryState.PAUSED);

      expect(history[2].from).toBe(QueryState.PAUSED);
      expect(history[2].to).toBe(QueryState.RUNNING);
    });

    test('should include timestamps in history events', async () => {
      const before = Date.now();
      await stateMachine.transition('START');
      const after = Date.now();

      const history = stateMachine.getHistory();
      expect(history[0].timestamp).toBeGreaterThanOrEqual(before);
      expect(history[0].timestamp).toBeLessThanOrEqual(after);
    });
  });

  describe('Context Management', () => {
    test('should update context metadata', () => {
      stateMachine.updateContext({
        model: 'haiku',
        agentCount: 3
      });

      const context = stateMachine.getContext();
      expect(context.model).toBe('haiku');
      expect(context.agentCount).toBe(3);
    });

    test('should preserve existing context when updating', () => {
      const sm = new QueryStateMachine(testQueryId, {
        model: 'sonnet',
        permissionMode: 'default'
      });

      sm.updateContext({ agentCount: 5 });

      const context = sm.getContext();
      expect(context.model).toBe('sonnet');
      expect(context.permissionMode).toBe('default');
      expect(context.agentCount).toBe(5);
    });

    test('should return immutable context copy', () => {
      const context1 = stateMachine.getContext();
      const context2 = stateMachine.getContext();

      expect(context1).not.toBe(context2);
      expect(context1).toEqual(context2);
    });
  });

  describe('Valid Actions Query', () => {
    test('should return valid actions for INIT state', () => {
      const actions = stateMachine.getValidActions();
      expect(actions).toContain('START');
      expect(actions).toContain('ERROR');
      expect(actions).toHaveLength(2);
    });

    test('should return valid actions for RUNNING state', async () => {
      await stateMachine.transition('START');
      const actions = stateMachine.getValidActions();

      expect(actions).toContain('PAUSE');
      expect(actions).toContain('COMPLETE');
      expect(actions).toContain('TERMINATE');
      expect(actions).toContain('ERROR');
      expect(actions).toHaveLength(4);
    });

    test('should return valid actions for PAUSED state', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');
      const actions = stateMachine.getValidActions();

      expect(actions).toContain('RESUME');
      expect(actions).toContain('TERMINATE');
      expect(actions).toContain('ERROR');
      expect(actions).toHaveLength(3);
    });

    test('should return no valid actions for terminal states', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('COMPLETE');
      const actions = stateMachine.getValidActions();

      expect(actions).toHaveLength(0);
    });
  });

  describe('Transition Validation', () => {
    test('should validate possible transitions', () => {
      expect(stateMachine.canTransition('START')).toBe(true);
      expect(stateMachine.canTransition('PAUSE')).toBe(false);
    });

    test('should validate transitions for RUNNING state', async () => {
      await stateMachine.transition('START');

      expect(stateMachine.canTransition('PAUSE')).toBe(true);
      expect(stateMachine.canTransition('COMPLETE')).toBe(true);
      expect(stateMachine.canTransition('START')).toBe(false);
    });

    test('should validate transitions for terminal states', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('COMPLETE');

      expect(stateMachine.canTransition('START')).toBe(false);
      expect(stateMachine.canTransition('PAUSE')).toBe(false);
      expect(stateMachine.canTransition('RESUME')).toBe(false);
    });
  });

  describe('Factory Function', () => {
    test('should create state machine with factory', () => {
      const sm = createStateMachine('factory-test-001');
      expect(sm).toBeInstanceOf(QueryStateMachine);
      expect(sm.getState()).toBe(QueryState.INIT);
      expect(sm.getContext().queryId).toBe('factory-test-001');
    });

    test('should create state machine with initial context', () => {
      const sm = createStateMachine('factory-test-002', {
        model: 'opus',
        agentCount: 10
      });

      const context = sm.getContext();
      expect(context.model).toBe('opus');
      expect(context.agentCount).toBe(10);
    });
  });

  describe('Complete Workflow Scenarios', () => {
    test('should support complete lifecycle: INIT → RUNNING → COMPLETED', async () => {
      expect(stateMachine.getState()).toBe(QueryState.INIT);

      await stateMachine.transition('START');
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);

      await stateMachine.transition('COMPLETE');
      expect(stateMachine.getState()).toBe(QueryState.COMPLETED);

      const history = stateMachine.getHistory();
      expect(history).toHaveLength(2);
    });

    test('should support pause/resume workflow', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');
      expect(stateMachine.getState()).toBe(QueryState.PAUSED);

      await stateMachine.transition('RESUME');
      expect(stateMachine.getState()).toBe(QueryState.RUNNING);

      await stateMachine.transition('COMPLETE');
      expect(stateMachine.getState()).toBe(QueryState.COMPLETED);

      const history = stateMachine.getHistory();
      expect(history).toHaveLength(4);
    });

    test('should support multiple pause/resume cycles', async () => {
      await stateMachine.transition('START');

      // First pause/resume
      await stateMachine.transition('PAUSE');
      await stateMachine.transition('RESUME');

      // Second pause/resume
      await stateMachine.transition('PAUSE');
      await stateMachine.transition('RESUME');

      await stateMachine.transition('COMPLETE');

      const history = stateMachine.getHistory();
      expect(history).toHaveLength(6);
      expect(stateMachine.getState()).toBe(QueryState.COMPLETED);
    });

    test('should support early termination from RUNNING', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('TERMINATE');

      expect(stateMachine.getState()).toBe(QueryState.TERMINATED);

      const history = stateMachine.getHistory();
      expect(history).toHaveLength(2);
      expect(history[1].action).toBe('TERMINATE');
    });

    test('should support early termination from PAUSED', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');
      await stateMachine.transition('TERMINATE');

      expect(stateMachine.getState()).toBe(QueryState.TERMINATED);

      const history = stateMachine.getHistory();
      expect(history).toHaveLength(3);
    });

    test('should support error handling from any state', async () => {
      await stateMachine.transition('START');
      await stateMachine.transition('PAUSE');
      await stateMachine.transition('ERROR');

      expect(stateMachine.getState()).toBe(QueryState.ERROR);

      const history = stateMachine.getHistory();
      expect(history[history.length - 1].action).toBe('ERROR');
    });
  });
});
