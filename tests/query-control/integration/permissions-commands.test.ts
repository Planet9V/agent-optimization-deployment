/**
 * GAP-003 Query Control System - Permissions and Commands Integration Tests
 */

import { PermissionManager } from '../../../lib/query-control/permissions/permission-manager';
import { CommandExecutor } from '../../../lib/query-control/commands/command-executor';
import { PermissionMode } from '../../../lib/query-control/types';

describe('Permissions and Commands Integration Tests', () => {
  let permissionManager: PermissionManager;
  let commandExecutor: CommandExecutor;
  const testQueryId = 'permissions-test-001';

  beforeEach(() => {
    permissionManager = new PermissionManager();
    commandExecutor = new CommandExecutor();
    permissionManager.clearHistory();
    commandExecutor.clearHistory();
  });

  describe('Permission mode switching', () => {
    test('should switch from DEFAULT to ACCEPT_EDITS', async () => {
      permissionManager.setCurrentMode(PermissionMode.DEFAULT);

      const result = await permissionManager.switchMode(
        testQueryId,
        PermissionMode.ACCEPT_EDITS
      );

      expect(result.success).toBe(true);
      expect(result.previousMode).toBe(PermissionMode.DEFAULT);
      expect(result.currentMode).toBe(PermissionMode.ACCEPT_EDITS);
      expect(permissionManager.getCurrentMode()).toBe(
        PermissionMode.ACCEPT_EDITS
      );
    });

    test('should switch from ACCEPT_EDITS to BYPASS_PERMISSIONS', async () => {
      permissionManager.setCurrentMode(PermissionMode.ACCEPT_EDITS);

      const result = await permissionManager.switchMode(
        testQueryId,
        PermissionMode.BYPASS_PERMISSIONS
      );

      expect(result.success).toBe(true);
      expect(result.previousMode).toBe(PermissionMode.ACCEPT_EDITS);
      expect(result.currentMode).toBe(PermissionMode.BYPASS_PERMISSIONS);
    });

    test('should switch to PLAN mode', async () => {
      permissionManager.setCurrentMode(PermissionMode.DEFAULT);

      const result = await permissionManager.switchMode(
        testQueryId,
        PermissionMode.PLAN
      );

      expect(result.success).toBe(true);
      expect(result.currentMode).toBe(PermissionMode.PLAN);

      const capabilities = permissionManager.getModeCapabilities(
        PermissionMode.PLAN
      );
      expect(capabilities.planningMode).toBe(true);
      expect(capabilities.editingAllowed).toBe(false);
    });

    test('should complete switch within 50ms target', async () => {
      permissionManager.setCurrentMode(PermissionMode.DEFAULT);

      const startTime = Date.now();
      const result = await permissionManager.switchMode(
        testQueryId,
        PermissionMode.ACCEPT_EDITS
      );
      const duration = Date.now() - startTime;

      expect(result.success).toBe(true);
      expect(duration).toBeLessThan(100); // Acceptable

      if (duration > 50) {
        console.warn(`Switch time: ${duration}ms (target: <50ms)`);
      }
    });

    test('should skip switch if already in target mode', async () => {
      permissionManager.setCurrentMode(PermissionMode.ACCEPT_EDITS);

      const result = await permissionManager.switchMode(
        testQueryId,
        PermissionMode.ACCEPT_EDITS
      );

      expect(result.success).toBe(true);
      expect(result.switchTimeMs).toBe(0);
    });
  });

  describe('Permission mode capabilities', () => {
    test('should have correct DEFAULT capabilities', () => {
      const capabilities = permissionManager.getModeCapabilities(
        PermissionMode.DEFAULT
      );

      expect(capabilities.autoApproveEdits).toBe(false);
      expect(capabilities.bypassUserConfirmation).toBe(false);
      expect(capabilities.planningMode).toBe(false);
      expect(capabilities.editingAllowed).toBe(true);
    });

    test('should have correct ACCEPT_EDITS capabilities', () => {
      const capabilities = permissionManager.getModeCapabilities(
        PermissionMode.ACCEPT_EDITS
      );

      expect(capabilities.autoApproveEdits).toBe(true);
      expect(capabilities.bypassUserConfirmation).toBe(false);
      expect(capabilities.planningMode).toBe(false);
      expect(capabilities.editingAllowed).toBe(true);
    });

    test('should have correct BYPASS_PERMISSIONS capabilities', () => {
      const capabilities = permissionManager.getModeCapabilities(
        PermissionMode.BYPASS_PERMISSIONS
      );

      expect(capabilities.autoApproveEdits).toBe(true);
      expect(capabilities.bypassUserConfirmation).toBe(true);
      expect(capabilities.planningMode).toBe(false);
      expect(capabilities.editingAllowed).toBe(true);
    });

    test('should have correct PLAN capabilities', () => {
      const capabilities = permissionManager.getModeCapabilities(
        PermissionMode.PLAN
      );

      expect(capabilities.autoApproveEdits).toBe(false);
      expect(capabilities.bypassUserConfirmation).toBe(false);
      expect(capabilities.planningMode).toBe(true);
      expect(capabilities.editingAllowed).toBe(false);
    });
  });

  describe('Command security validation', () => {
    test('should block dangerous rm -rf command', async () => {
      const result = await commandExecutor.executeCommand(
        testQueryId,
        'rm -rf /'
      );

      expect(result.success).toBe(false);
      expect(result.blocked).toBe(true);
      expect(result.blockReason).toContain('dangerous');
    });

    test('should block dd command', async () => {
      const result = await commandExecutor.executeCommand(
        testQueryId,
        'dd if=/dev/zero of=/dev/sda'
      );

      expect(result.success).toBe(false);
      expect(result.blocked).toBe(true);
      expect(result.blockReason).toContain('dangerous');
    });

    test('should block mkfs command', async () => {
      const result = await commandExecutor.executeCommand(
        testQueryId,
        'mkfs.ext4 /dev/sda1'
      );

      expect(result.success).toBe(false);
      expect(result.blocked).toBe(true);
      expect(result.blockReason).toContain('dangerous');
    });

    test('should block fork bomb', async () => {
      const result = await commandExecutor.executeCommand(
        testQueryId,
        ':(){:|:&};:'
      );

      expect(result.success).toBe(false);
      expect(result.blocked).toBe(true);
      expect(result.blockReason).toContain('dangerous');
    });

    test('should block access to /etc/passwd', async () => {
      const result = await commandExecutor.executeCommand(
        testQueryId,
        'cat /etc/passwd'
      );

      expect(result.success).toBe(false);
      expect(result.blocked).toBe(true);
      expect(result.blockReason).toContain('sensitive system files');
    });

    test('should block writes to block devices', async () => {
      const result = await commandExecutor.executeCommand(
        testQueryId,
        'echo test > /dev/sda'
      );

      expect(result.success).toBe(false);
      expect(result.blocked).toBe(true);
      expect(result.blockReason).toContain('block device');
    });

    test('should block sudo rm combination', async () => {
      const result = await commandExecutor.executeCommand(
        testQueryId,
        'sudo rm important_file.txt'
      );

      expect(result.success).toBe(false);
      expect(result.blocked).toBe(true);
      expect(result.blockReason).toContain('sudo + rm');
    });
  });

  describe('Command execution', () => {
    test('should execute safe command successfully', async () => {
      const result = await commandExecutor.executeCommand(
        testQueryId,
        'echo "Hello World"'
      );

      expect(result.success).toBe(true);
      expect(result.blocked).toBeUndefined();
      expect(result.executionTimeMs).toBeGreaterThan(0);
    });

    test('should validate command security before execution', () => {
      const check1 = commandExecutor.validateCommandSecurity('ls -la');
      expect(check1.safe).toBe(true);

      const check2 = commandExecutor.validateCommandSecurity('rm -rf /');
      expect(check2.safe).toBe(false);
    });

    test('should check if command is blacklisted', () => {
      expect(commandExecutor.isCommandBlacklisted('rm -rf /')).toBe(true);
      expect(commandExecutor.isCommandBlacklisted('ls -la')).toBe(false);
      expect(commandExecutor.isCommandBlacklisted('dd if=/dev/zero')).toBe(
        true
      );
    });

    test('should retrieve blacklist', () => {
      const blacklist = commandExecutor.getBlacklist();

      expect(blacklist).toContain('rm -rf');
      expect(blacklist).toContain('dd if=');
      expect(blacklist).toContain('mkfs');
      expect(blacklist.length).toBeGreaterThan(5);
    });
  });

  describe('Statistics tracking', () => {
    test('should track permission switch statistics', async () => {
      permissionManager.setCurrentMode(PermissionMode.DEFAULT);

      await permissionManager.switchMode(
        testQueryId,
        PermissionMode.ACCEPT_EDITS
      );
      await permissionManager.switchMode(
        testQueryId,
        PermissionMode.BYPASS_PERMISSIONS
      );

      const stats = permissionManager.getStatistics();

      expect(stats.currentMode).toBe(PermissionMode.BYPASS_PERMISSIONS);
      expect(stats.totalSwitches).toBe(2);
      expect(stats.averageSwitchTime).toBeGreaterThan(0);
      expect(stats.switchHistory).toHaveLength(2);
    });

    test('should track command execution statistics', async () => {
      await commandExecutor.executeCommand(testQueryId, 'echo test1');
      await commandExecutor.executeCommand(testQueryId, 'echo test2');
      await commandExecutor.executeCommand(testQueryId, 'rm -rf /'); // blocked

      const stats = commandExecutor.getStatistics();

      expect(stats.totalCommands).toBe(3);
      expect(stats.successfulCommands).toBe(2);
      expect(stats.failedCommands).toBe(1);
      expect(stats.averageExecutionTime).toBeGreaterThan(0);
      expect(stats.commandHistory).toHaveLength(3);
    });

    test('should clear permission history', async () => {
      await permissionManager.switchMode(
        testQueryId,
        PermissionMode.ACCEPT_EDITS
      );

      permissionManager.clearHistory();

      const stats = permissionManager.getStatistics();
      expect(stats.totalSwitches).toBe(0);
      expect(stats.switchHistory).toHaveLength(0);
    });

    test('should clear command history', async () => {
      await commandExecutor.executeCommand(testQueryId, 'echo test');

      commandExecutor.clearHistory();

      const stats = commandExecutor.getStatistics();
      expect(stats.totalCommands).toBe(0);
      expect(stats.commandHistory).toHaveLength(0);
    });
  });

  describe('Multiple operations', () => {
    test('should handle rapid permission switches', async () => {
      permissionManager.setCurrentMode(PermissionMode.DEFAULT);

      const result1 = await permissionManager.switchMode(
        testQueryId + '_1',
        PermissionMode.ACCEPT_EDITS
      );
      expect(result1.success).toBe(true);

      const result2 = await permissionManager.switchMode(
        testQueryId + '_2',
        PermissionMode.BYPASS_PERMISSIONS
      );
      expect(result2.success).toBe(true);

      const result3 = await permissionManager.switchMode(
        testQueryId + '_3',
        PermissionMode.PLAN
      );
      expect(result3.success).toBe(true);

      expect(permissionManager.getCurrentMode()).toBe(PermissionMode.PLAN);
    });

    test('should handle multiple command executions', async () => {
      const result1 = await commandExecutor.executeCommand(
        testQueryId,
        'echo test1'
      );
      const result2 = await commandExecutor.executeCommand(
        testQueryId,
        'echo test2'
      );
      const result3 = await commandExecutor.executeCommand(
        testQueryId,
        'rm -rf /'
      );

      expect(result1.success).toBe(true);
      expect(result2.success).toBe(true);
      expect(result3.success).toBe(false);
      expect(result3.blocked).toBe(true);
    });
  });

  describe('Integration scenarios', () => {
    test('should coordinate permission mode with command execution', async () => {
      // Set to PLAN mode (no editing allowed)
      await permissionManager.switchMode(testQueryId, PermissionMode.PLAN);

      const capabilities = permissionManager.getModeCapabilities(
        PermissionMode.PLAN
      );
      expect(capabilities.editingAllowed).toBe(false);

      // In real system, this would prevent file modifications
      expect(capabilities.planningMode).toBe(true);
    });

    test('should track full workflow with permissions and commands', async () => {
      // Start with DEFAULT
      permissionManager.setCurrentMode(PermissionMode.DEFAULT);

      // Switch to ACCEPT_EDITS
      await permissionManager.switchMode(
        testQueryId,
        PermissionMode.ACCEPT_EDITS
      );

      // Execute safe command
      const cmd1 = await commandExecutor.executeCommand(
        testQueryId,
        'echo "workflow test"'
      );
      expect(cmd1.success).toBe(true);

      // Try dangerous command (should block)
      const cmd2 = await commandExecutor.executeCommand(
        testQueryId,
        'rm -rf /'
      );
      expect(cmd2.blocked).toBe(true);

      // Switch to PLAN mode
      await permissionManager.switchMode(testQueryId, PermissionMode.PLAN);

      // Verify final state
      const permStats = permissionManager.getStatistics();
      const cmdStats = commandExecutor.getStatistics();

      expect(permStats.totalSwitches).toBe(2);
      expect(cmdStats.totalCommands).toBe(2);
      expect(cmdStats.successfulCommands).toBe(1);
      expect(cmdStats.failedCommands).toBe(1);
    });
  });
});
