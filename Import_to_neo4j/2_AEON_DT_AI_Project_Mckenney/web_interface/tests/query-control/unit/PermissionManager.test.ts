/**
 * GAP-003 Query Control System - Permission Manager Unit Tests
 *
 * File: tests/query-control/unit/PermissionManager.test.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: Comprehensive unit tests for PermissionManager
 *
 * Constitutional Compliance:
 * - DILIGENCE: >90% code coverage target
 * - INTEGRITY: All edge cases tested
 * - NO DEVELOPMENT THEATER: Production-grade tests
 *
 * Performance Target: <50ms permission mode switch
 * Coverage Goal: >90% line coverage, >85% branch coverage
 */

import { describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import {
  PermissionManager,
  PermissionMode,
  getPermissionManager,
  type PermissionSwitchResult,
  type PermissionConfig
} from '../../../lib/query-control/permissions/permission-manager';

describe('PermissionManager', () => {
  let manager: PermissionManager;
  const testQueryId = 'test-query-001';

  beforeEach(() => {
    manager = new PermissionManager();
  });

  afterEach(() => {
    // Clear history after each test
    manager.clearHistory();
  });

  describe('Initialization', () => {
    test('should start in DEFAULT mode', () => {
      expect(manager.getCurrentMode()).toBe(PermissionMode.DEFAULT);
    });

    test('should initialize with custom mode', () => {
      const customManager = new PermissionManager(PermissionMode.ACCEPT_EDITS);
      expect(customManager.getCurrentMode()).toBe(PermissionMode.ACCEPT_EDITS);
    });

    test('should initialize with BYPASS_PERMISSIONS mode', () => {
      const bypassManager = new PermissionManager(PermissionMode.BYPASS_PERMISSIONS);
      expect(bypassManager.getCurrentMode()).toBe(PermissionMode.BYPASS_PERMISSIONS);
    });

    test('should initialize with PLAN mode', () => {
      const planManager = new PermissionManager(PermissionMode.PLAN);
      expect(planManager.getCurrentMode()).toBe(PermissionMode.PLAN);
    });

    test('should have empty switch history initially', () => {
      expect(manager.getSwitchHistory(testQueryId)).toEqual([]);
    });

    test('should have zero statistics initially', () => {
      const stats = manager.getSwitchStatistics();
      expect(stats.totalSwitches).toBe(0);
      expect(stats.averageSwitchTime).toBe(0);
      expect(stats.fastestSwitch).toBe(0);
      expect(stats.slowestSwitch).toBe(0);
    });
  });

  describe('Mode Switching', () => {
    test('should successfully switch from DEFAULT to ACCEPT_EDITS', async () => {
      const result = await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);

      expect(result.success).toBe(true);
      expect(result.previousMode).toBe(PermissionMode.DEFAULT);
      expect(result.currentMode).toBe(PermissionMode.ACCEPT_EDITS);
      expect(manager.getCurrentMode()).toBe(PermissionMode.ACCEPT_EDITS);
    });

    test('should successfully switch from DEFAULT to BYPASS_PERMISSIONS', async () => {
      const result = await manager.switchMode(testQueryId, PermissionMode.BYPASS_PERMISSIONS);

      expect(result.success).toBe(true);
      expect(result.previousMode).toBe(PermissionMode.DEFAULT);
      expect(result.currentMode).toBe(PermissionMode.BYPASS_PERMISSIONS);
      expect(manager.getCurrentMode()).toBe(PermissionMode.BYPASS_PERMISSIONS);
    });

    test('should successfully switch from DEFAULT to PLAN', async () => {
      const result = await manager.switchMode(testQueryId, PermissionMode.PLAN);

      expect(result.success).toBe(true);
      expect(result.previousMode).toBe(PermissionMode.DEFAULT);
      expect(result.currentMode).toBe(PermissionMode.PLAN);
      expect(manager.getCurrentMode()).toBe(PermissionMode.PLAN);
    });

    test('should successfully switch from ACCEPT_EDITS to DEFAULT', async () => {
      await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);
      const result = await manager.switchMode(testQueryId, PermissionMode.DEFAULT);

      expect(result.success).toBe(true);
      expect(result.previousMode).toBe(PermissionMode.ACCEPT_EDITS);
      expect(result.currentMode).toBe(PermissionMode.DEFAULT);
    });

    test('should support switching between all mode combinations', async () => {
      const modes = [
        PermissionMode.DEFAULT,
        PermissionMode.ACCEPT_EDITS,
        PermissionMode.BYPASS_PERMISSIONS,
        PermissionMode.PLAN
      ];

      for (let i = 0; i < modes.length; i++) {
        for (let j = 0; j < modes.length; j++) {
          if (i !== j) {
            const manager = new PermissionManager(modes[i]);
            const result = await manager.switchMode('test', modes[j]);
            expect(result.success).toBe(true);
            expect(result.currentMode).toBe(modes[j]);
          }
        }
      }
    });
  });

  describe('Performance Requirements', () => {
    test('should complete mode switch in <50ms (performance target)', async () => {
      const result = await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);

      expect(result.success).toBe(true);
      expect(result.switchTimeMs).toBeLessThan(50);
    });

    test('should complete multiple switches in <50ms each', async () => {
      const modes = [
        PermissionMode.ACCEPT_EDITS,
        PermissionMode.BYPASS_PERMISSIONS,
        PermissionMode.PLAN,
        PermissionMode.DEFAULT
      ];

      for (const mode of modes) {
        const result = await manager.switchMode(testQueryId, mode);
        expect(result.switchTimeMs).toBeLessThan(50);
      }
    });

    test('should track switch time accurately', async () => {
      const startTime = Date.now();
      const result = await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);
      const endTime = Date.now();

      expect(result.switchTimeMs).toBeGreaterThanOrEqual(0);
      expect(result.switchTimeMs).toBeLessThanOrEqual(endTime - startTime);
    });

    test('should maintain performance with multiple consecutive switches', async () => {
      const switches = [
        PermissionMode.ACCEPT_EDITS,
        PermissionMode.DEFAULT,
        PermissionMode.BYPASS_PERMISSIONS,
        PermissionMode.DEFAULT,
        PermissionMode.PLAN
      ];

      for (const mode of switches) {
        const result = await manager.switchMode(testQueryId, mode);
        expect(result.switchTimeMs).toBeLessThan(50);
      }
    });
  });

  describe('Error Handling', () => {
    test('should reject invalid permission mode', async () => {
      const result = await manager.switchMode(testQueryId, 'invalid-mode' as PermissionMode);

      expect(result.success).toBe(false);
      expect(result.error).toContain('Invalid permission mode');
      expect(manager.getCurrentMode()).toBe(PermissionMode.DEFAULT);
    });

    test('should reject switching to same mode', async () => {
      const result = await manager.switchMode(testQueryId, PermissionMode.DEFAULT);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Already using this permission mode');
      expect(result.previousMode).toBe(PermissionMode.DEFAULT);
      expect(result.currentMode).toBe(PermissionMode.DEFAULT);
    });

    test('should not change state on failed switch', async () => {
      await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);

      const beforeMode = manager.getCurrentMode();
      const result = await manager.switchMode(testQueryId, 'invalid' as PermissionMode);

      expect(result.success).toBe(false);
      expect(manager.getCurrentMode()).toBe(beforeMode);
    });

    test('should include error timing even on failure', async () => {
      const result = await manager.switchMode(testQueryId, 'invalid' as PermissionMode);

      expect(result.success).toBe(false);
      expect(result.switchTimeMs).toBeGreaterThanOrEqual(0);
    });

    test('should handle null/undefined mode gracefully', async () => {
      const result = await manager.switchMode(testQueryId, null as any);

      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
    });
  });

  describe('getCurrentMode()', () => {
    test('should return current mode', () => {
      expect(manager.getCurrentMode()).toBe(PermissionMode.DEFAULT);
    });

    test('should reflect mode changes immediately', async () => {
      await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);
      expect(manager.getCurrentMode()).toBe(PermissionMode.ACCEPT_EDITS);

      await manager.switchMode(testQueryId, PermissionMode.PLAN);
      expect(manager.getCurrentMode()).toBe(PermissionMode.PLAN);
    });

    test('should return same mode after failed switch', async () => {
      await manager.switchMode(testQueryId, PermissionMode.BYPASS_PERMISSIONS);
      const modeBefore = manager.getCurrentMode();

      await manager.switchMode(testQueryId, 'invalid' as PermissionMode);

      expect(manager.getCurrentMode()).toBe(modeBefore);
    });
  });

  describe('canSwitchTo()', () => {
    test('should allow valid mode switch', () => {
      const validation = manager.canSwitchTo(PermissionMode.ACCEPT_EDITS);

      expect(validation.allowed).toBe(true);
      expect(validation.reason).toBeUndefined();
    });

    test('should reject invalid mode', () => {
      const validation = manager.canSwitchTo('invalid-mode' as PermissionMode);

      expect(validation.allowed).toBe(false);
      expect(validation.reason).toContain('Invalid permission mode');
    });

    test('should reject switching to same mode', () => {
      const validation = manager.canSwitchTo(PermissionMode.DEFAULT);

      expect(validation.allowed).toBe(false);
      expect(validation.reason).toBe('Already using this permission mode');
    });

    test('should validate all permission modes', () => {
      const modes = [
        PermissionMode.DEFAULT,
        PermissionMode.ACCEPT_EDITS,
        PermissionMode.BYPASS_PERMISSIONS,
        PermissionMode.PLAN
      ];

      for (const mode of modes) {
        const testManager = new PermissionManager(
          mode === PermissionMode.DEFAULT ? PermissionMode.ACCEPT_EDITS : PermissionMode.DEFAULT
        );
        const validation = testManager.canSwitchTo(mode);
        expect(validation.allowed).toBe(true);
      }
    });

    test('should not modify state when checking validity', () => {
      const modeBefore = manager.getCurrentMode();

      manager.canSwitchTo(PermissionMode.ACCEPT_EDITS);
      manager.canSwitchTo(PermissionMode.BYPASS_PERMISSIONS);
      manager.canSwitchTo('invalid' as PermissionMode);

      expect(manager.getCurrentMode()).toBe(modeBefore);
    });
  });

  describe('Switch History Tracking', () => {
    test('should record switch in history', async () => {
      await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);

      const history = manager.getSwitchHistory(testQueryId);
      expect(history).toHaveLength(1);
      expect(history[0].from).toBe(PermissionMode.DEFAULT);
      expect(history[0].to).toBe(PermissionMode.ACCEPT_EDITS);
    });

    test('should maintain complete switch history', async () => {
      await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);
      await manager.switchMode(testQueryId, PermissionMode.BYPASS_PERMISSIONS);
      await manager.switchMode(testQueryId, PermissionMode.PLAN);

      const history = manager.getSwitchHistory(testQueryId);
      expect(history).toHaveLength(3);

      expect(history[0].from).toBe(PermissionMode.DEFAULT);
      expect(history[0].to).toBe(PermissionMode.ACCEPT_EDITS);

      expect(history[1].from).toBe(PermissionMode.ACCEPT_EDITS);
      expect(history[1].to).toBe(PermissionMode.BYPASS_PERMISSIONS);

      expect(history[2].from).toBe(PermissionMode.BYPASS_PERMISSIONS);
      expect(history[2].to).toBe(PermissionMode.PLAN);
    });

    test('should include timestamp in history entries', async () => {
      const before = Date.now();
      await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);
      const after = Date.now();

      const history = manager.getSwitchHistory(testQueryId);
      expect(history[0].timestamp).toBeGreaterThanOrEqual(before);
      expect(history[0].timestamp).toBeLessThanOrEqual(after);
    });

    test('should include duration in history entries', async () => {
      await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);

      const history = manager.getSwitchHistory(testQueryId);
      expect(history[0].durationMs).toBeGreaterThanOrEqual(0);
      expect(history[0].durationMs).toBeLessThan(50);
    });

    test('should track history per query ID', async () => {
      await manager.switchMode('query-1', PermissionMode.ACCEPT_EDITS);
      await manager.switchMode('query-2', PermissionMode.BYPASS_PERMISSIONS);
      await manager.switchMode('query-1', PermissionMode.PLAN);

      const history1 = manager.getSwitchHistory('query-1');
      const history2 = manager.getSwitchHistory('query-2');

      expect(history1).toHaveLength(2);
      expect(history2).toHaveLength(1);
    });

    test('should return empty array for unknown query ID', () => {
      const history = manager.getSwitchHistory('unknown-query');
      expect(history).toEqual([]);
    });

    test('should not record failed switches in history', async () => {
      await manager.switchMode(testQueryId, 'invalid' as PermissionMode);

      const history = manager.getSwitchHistory(testQueryId);
      expect(history).toHaveLength(0);
    });
  });

  describe('Switch Statistics', () => {
    test('should calculate total switches', async () => {
      await manager.switchMode('query-1', PermissionMode.ACCEPT_EDITS);
      await manager.switchMode('query-1', PermissionMode.BYPASS_PERMISSIONS);
      await manager.switchMode('query-2', PermissionMode.PLAN);

      const stats = manager.getSwitchStatistics();
      expect(stats.totalSwitches).toBe(3);
    });

    test('should calculate average switch time', async () => {
      await manager.switchMode('query-1', PermissionMode.ACCEPT_EDITS);
      await manager.switchMode('query-1', PermissionMode.DEFAULT);
      await manager.switchMode('query-1', PermissionMode.PLAN);

      const stats = manager.getSwitchStatistics();
      expect(stats.averageSwitchTime).toBeGreaterThan(0);
      expect(stats.averageSwitchTime).toBeLessThan(50);
    });

    test('should track fastest switch', async () => {
      await manager.switchMode('query-1', PermissionMode.ACCEPT_EDITS);
      await manager.switchMode('query-1', PermissionMode.DEFAULT);

      const stats = manager.getSwitchStatistics();
      expect(stats.fastestSwitch).toBeGreaterThanOrEqual(0);
      expect(stats.fastestSwitch).toBeLessThan(50); // Under performance target
      expect(stats.fastestSwitch).toBeLessThanOrEqual(stats.averageSwitchTime);
    });

    test('should track slowest switch', async () => {
      await manager.switchMode('query-1', PermissionMode.ACCEPT_EDITS);
      await manager.switchMode('query-1', PermissionMode.DEFAULT);

      const stats = manager.getSwitchStatistics();
      expect(stats.slowestSwitch).toBeGreaterThanOrEqual(stats.averageSwitchTime);
    });

    test('should count switches by mode transition', async () => {
      // Each manager instance starts in DEFAULT mode, so we need fresh instances
      const manager1 = new PermissionManager();
      const manager2 = new PermissionManager();

      await manager1.switchMode('query-1', PermissionMode.ACCEPT_EDITS);
      await manager2.switchMode('query-2', PermissionMode.ACCEPT_EDITS);

      // Combine statistics from both managers
      const stats1 = manager1.getSwitchStatistics();
      const stats2 = manager2.getSwitchStatistics();

      expect(stats1.switchesByMode['default→acceptEdits']).toBe(1);
      expect(stats2.switchesByMode['default→acceptEdits']).toBe(1);
    });

    test('should handle zero switches gracefully', () => {
      const stats = manager.getSwitchStatistics();

      expect(stats.totalSwitches).toBe(0);
      expect(stats.averageSwitchTime).toBe(0);
      expect(stats.fastestSwitch).toBe(0);
      expect(stats.slowestSwitch).toBe(0);
      expect(Object.keys(stats.switchesByMode)).toHaveLength(0);
    });

    test('should aggregate statistics across all queries', async () => {
      await manager.switchMode('query-1', PermissionMode.ACCEPT_EDITS);
      await manager.switchMode('query-2', PermissionMode.BYPASS_PERMISSIONS);
      await manager.switchMode('query-3', PermissionMode.PLAN);
      await manager.switchMode('query-1', PermissionMode.DEFAULT);

      const stats = manager.getSwitchStatistics();
      expect(stats.totalSwitches).toBe(4);
      expect(Object.keys(stats.switchesByMode).length).toBeGreaterThan(0);
    });
  });

  describe('clearHistory()', () => {
    test('should clear all switch history', async () => {
      await manager.switchMode('query-1', PermissionMode.ACCEPT_EDITS);
      await manager.switchMode('query-2', PermissionMode.BYPASS_PERMISSIONS);

      manager.clearHistory();

      expect(manager.getSwitchHistory('query-1')).toEqual([]);
      expect(manager.getSwitchHistory('query-2')).toEqual([]);
    });

    test('should reset statistics to zero', async () => {
      await manager.switchMode('query-1', PermissionMode.ACCEPT_EDITS);
      await manager.switchMode('query-1', PermissionMode.DEFAULT);

      manager.clearHistory();

      const stats = manager.getSwitchStatistics();
      expect(stats.totalSwitches).toBe(0);
      expect(stats.averageSwitchTime).toBe(0);
    });

    test('should not affect current mode', async () => {
      await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);
      const modeBefore = manager.getCurrentMode();

      manager.clearHistory();

      expect(manager.getCurrentMode()).toBe(modeBefore);
    });

    test('should allow new switches after clearing', async () => {
      await manager.switchMode('query-1', PermissionMode.ACCEPT_EDITS);
      manager.clearHistory();

      const result = await manager.switchMode('query-1', PermissionMode.BYPASS_PERMISSIONS);
      expect(result.success).toBe(true);

      const history = manager.getSwitchHistory('query-1');
      expect(history).toHaveLength(1);
    });
  });

  describe('Singleton Pattern', () => {
    // Note: These tests may fail if getPermissionManager singleton is already initialized
    // in other tests. They test the intended singleton behavior.

    test('should return same instance on multiple calls', () => {
      const instance1 = getPermissionManager();
      const instance2 = getPermissionManager();

      expect(instance1).toBe(instance2);
    });

    test('should preserve state across getPermissionManager calls', async () => {
      const manager1 = getPermissionManager();
      const initialMode = manager1.getCurrentMode();

      // Switch to a different mode
      const targetMode = initialMode === PermissionMode.DEFAULT
        ? PermissionMode.ACCEPT_EDITS
        : PermissionMode.DEFAULT;

      await manager1.switchMode(testQueryId, targetMode);

      const manager2 = getPermissionManager();
      expect(manager2.getCurrentMode()).toBe(targetMode);
    });

    test('should use initial mode only on first call (singleton behavior)', () => {
      // Note: This test assumes singleton is already initialized from previous tests
      // The singleton pattern means initial mode is only set on first-ever call
      const manager1 = getPermissionManager();
      const currentMode = manager1.getCurrentMode();

      const manager2 = getPermissionManager(PermissionMode.PLAN);
      // Should still have the same mode, ignoring the new initial mode parameter
      expect(manager2.getCurrentMode()).toBe(currentMode);
    });

    test('should maintain singleton across multiple operations', async () => {
      const manager1 = getPermissionManager();
      const currentMode = manager1.getCurrentMode();

      // Clear history to get clean baseline
      manager1.clearHistory();
      const beforeStats = manager1.getSwitchStatistics();

      // Determine modes to switch to (avoid already using same mode)
      const mode1 = currentMode === PermissionMode.ACCEPT_EDITS
        ? PermissionMode.BYPASS_PERMISSIONS
        : PermissionMode.ACCEPT_EDITS;

      const mode2 = mode1 === PermissionMode.BYPASS_PERMISSIONS
        ? PermissionMode.PLAN
        : PermissionMode.BYPASS_PERMISSIONS;

      await manager1.switchMode('singleton-query-1', mode1);

      const manager2 = getPermissionManager();
      await manager2.switchMode('singleton-query-2', mode2);

      const manager3 = getPermissionManager();
      const afterStats = manager3.getSwitchStatistics();

      // Should have exactly 2 switches from our operations
      expect(afterStats.totalSwitches).toBe(beforeStats.totalSwitches + 2);
      expect(manager1).toBe(manager2);
      expect(manager2).toBe(manager3);
    });
  });

  describe('MCP Integration Readiness', () => {
    test('should provide compatible interface for MCP query_control', async () => {
      const result = await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);

      // Verify structure matches MCP expectations
      expect(result).toHaveProperty('success');
      expect(result).toHaveProperty('previousMode');
      expect(result).toHaveProperty('currentMode');
      expect(result).toHaveProperty('switchTimeMs');
    });

    test('should support all MCP permission modes', async () => {
      const mcpModes = [
        PermissionMode.ACCEPT_EDITS,
        PermissionMode.BYPASS_PERMISSIONS,
        PermissionMode.PLAN
      ];

      // Test switching to each mode from DEFAULT
      for (const mode of mcpModes) {
        const testManager = new PermissionManager();
        const result = await testManager.switchMode(testQueryId, mode);
        expect(result.success).toBe(true);
        expect(result.currentMode).toBe(mode);
      }

      // Test DEFAULT mode explicitly (switch from another mode to DEFAULT)
      const testManager = new PermissionManager(PermissionMode.ACCEPT_EDITS);
      const result = await testManager.switchMode(testQueryId, PermissionMode.DEFAULT);
      expect(result.success).toBe(true);
      expect(result.currentMode).toBe(PermissionMode.DEFAULT);
    });

    test('should provide queryId-scoped operations for MCP', async () => {
      await manager.switchMode('mcp-query-1', PermissionMode.ACCEPT_EDITS);
      await manager.switchMode('mcp-query-2', PermissionMode.BYPASS_PERMISSIONS);

      const history1 = manager.getSwitchHistory('mcp-query-1');
      const history2 = manager.getSwitchHistory('mcp-query-2');

      expect(history1[0].to).toBe(PermissionMode.ACCEPT_EDITS);
      expect(history2[0].to).toBe(PermissionMode.BYPASS_PERMISSIONS);
    });

    test('should handle MCP error scenarios gracefully', async () => {
      const result = await manager.switchMode(testQueryId, 'invalid-mcp-mode' as PermissionMode);

      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
      expect(typeof result.error).toBe('string');
    });
  });

  describe('Complete Workflow Scenarios', () => {
    test('should support complete permission lifecycle', async () => {
      // Start in default
      expect(manager.getCurrentMode()).toBe(PermissionMode.DEFAULT);

      // Switch to accept edits
      let result = await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);
      expect(result.success).toBe(true);

      // Switch to bypass permissions
      result = await manager.switchMode(testQueryId, PermissionMode.BYPASS_PERMISSIONS);
      expect(result.success).toBe(true);

      // Switch to plan mode
      result = await manager.switchMode(testQueryId, PermissionMode.PLAN);
      expect(result.success).toBe(true);

      // Return to default
      result = await manager.switchMode(testQueryId, PermissionMode.DEFAULT);
      expect(result.success).toBe(true);

      const history = manager.getSwitchHistory(testQueryId);
      expect(history).toHaveLength(4);
    });

    test('should support rapid mode switching', async () => {
      const modes = [
        PermissionMode.ACCEPT_EDITS,
        PermissionMode.DEFAULT,
        PermissionMode.BYPASS_PERMISSIONS,
        PermissionMode.DEFAULT,
        PermissionMode.PLAN,
        PermissionMode.DEFAULT
      ];

      for (const mode of modes) {
        const result = await manager.switchMode(testQueryId, mode);
        expect(result.success).toBe(true);
        expect(result.switchTimeMs).toBeLessThan(50);
      }
    });

    test('should handle mixed success and failure switches', async () => {
      await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);
      await manager.switchMode(testQueryId, 'invalid' as PermissionMode);
      await manager.switchMode(testQueryId, PermissionMode.ACCEPT_EDITS);
      await manager.switchMode(testQueryId, PermissionMode.BYPASS_PERMISSIONS);

      const history = manager.getSwitchHistory(testQueryId);
      expect(history).toHaveLength(2); // Only successful switches recorded
    });

    test('should maintain consistency across multiple queries', async () => {
      await manager.switchMode('query-1', PermissionMode.ACCEPT_EDITS);
      await manager.switchMode('query-2', PermissionMode.BYPASS_PERMISSIONS);
      await manager.switchMode('query-3', PermissionMode.PLAN);

      expect(manager.getSwitchHistory('query-1')).toHaveLength(1);
      expect(manager.getSwitchHistory('query-2')).toHaveLength(1);
      expect(manager.getSwitchHistory('query-3')).toHaveLength(1);

      const stats = manager.getSwitchStatistics();
      expect(stats.totalSwitches).toBe(3);
    });
  });

  describe('Edge Cases', () => {
    test('should handle empty query ID', async () => {
      const result = await manager.switchMode('', PermissionMode.ACCEPT_EDITS);
      expect(result.success).toBe(true);

      const history = manager.getSwitchHistory('');
      expect(history).toHaveLength(1);
    });

    test('should handle very long query IDs', async () => {
      const longId = 'x'.repeat(1000);
      const result = await manager.switchMode(longId, PermissionMode.ACCEPT_EDITS);

      expect(result.success).toBe(true);
      expect(manager.getSwitchHistory(longId)).toHaveLength(1);
    });

    test('should handle special characters in query ID', async () => {
      const specialId = 'query-!@#$%^&*()';
      const result = await manager.switchMode(specialId, PermissionMode.ACCEPT_EDITS);

      expect(result.success).toBe(true);
      expect(manager.getSwitchHistory(specialId)).toHaveLength(1);
    });

    test('should handle rapid consecutive switches to different modes', async () => {
      const switches = await Promise.all([
        manager.switchMode('query-1', PermissionMode.ACCEPT_EDITS),
        manager.switchMode('query-2', PermissionMode.BYPASS_PERMISSIONS),
        manager.switchMode('query-3', PermissionMode.PLAN)
      ]);

      expect(switches.every(s => s.success)).toBe(true);
    });
  });
});
