/**
 * GAP-003 Query Control System - Permission Manager
 * Runtime permission mode switching for query control
 */

import { PermissionMode } from '../types';
import { mcpClient } from '../mcp-client';

export interface PermissionSwitchResult {
  success: boolean;
  previousMode: PermissionMode;
  currentMode: PermissionMode;
  switchTimeMs: number;
}

/**
 * Permission Manager
 * Handles runtime switching between permission modes
 * Target: <50ms switch time
 */
export class PermissionManager {
  private currentMode: PermissionMode = PermissionMode.DEFAULT;
  private switchHistory: Array<{
    from: PermissionMode;
    to: PermissionMode;
    timestamp: number;
    duration: number;
  }> = [];

  /**
   * Switch to a different permission mode
   * Target: <50ms
   */
  async switchMode(
    queryId: string,
    targetMode: PermissionMode
  ): Promise<PermissionSwitchResult> {
    const startTime = Date.now();

    try {
      console.log(
        `Switching permission mode for query ${queryId}: ${this.currentMode} → ${targetMode}`
      );

      // Validate target mode
      if (!this.isValidMode(targetMode)) {
        throw new Error(`Invalid permission mode: ${targetMode}`);
      }

      const previousMode = this.currentMode;

      // Skip if already in target mode
      if (previousMode === targetMode) {
        console.log('Already in target permission mode, no switch needed');
        return {
          success: true,
          previousMode,
          currentMode: targetMode,
          switchTimeMs: 0
        };
      }

      // Switch mode via MCP
      await mcpClient.queryControl({
        action: 'change_permissions',
        queryId,
        permissionMode: targetMode
      });

      // Store permission config in memory
      await mcpClient.storeMemory(
        `permission_config_${queryId}`,
        {
          mode: targetMode,
          switchedAt: Date.now(),
          previousMode: previousMode,
          capabilities: this.getModeCapabilities(targetMode)
        },
        3600 // 1 hour TTL
      );

      this.currentMode = targetMode;

      const switchTime = Date.now() - startTime;

      // Track switch history
      this.switchHistory.push({
        from: previousMode,
        to: targetMode,
        timestamp: Date.now(),
        duration: switchTime
      });

      // Train neural pattern on switch performance
      await mcpClient.trainNeuralPattern(
        'optimization',
        `permission_switch:${previousMode}->${targetMode}:${switchTime}ms`,
        20
      );

      console.log(
        `Permission switch completed: ${previousMode} → ${targetMode} (${switchTime}ms)`
      );

      // Validate performance target (<50ms)
      if (switchTime > 50) {
        console.warn(
          `Permission switch exceeded target: ${switchTime}ms (target: <50ms)`
        );
      }

      return {
        success: true,
        previousMode,
        currentMode: targetMode,
        switchTimeMs: switchTime
      };
    } catch (error) {
      console.error(`Permission switch failed: ${error}`);

      // Train failure pattern
      await mcpClient.trainNeuralPattern(
        'coordination',
        `permission_switch_failed:${this.currentMode}->${targetMode}:${error}`,
        10
      );

      throw new Error(`Failed to switch permission mode: ${error}`);
    }
  }

  /**
   * Get current permission mode
   */
  getCurrentMode(): PermissionMode {
    return this.currentMode;
  }

  /**
   * Set current mode (for initialization)
   */
  setCurrentMode(mode: PermissionMode): void {
    if (!this.isValidMode(mode)) {
      throw new Error(`Invalid permission mode: ${mode}`);
    }
    this.currentMode = mode;
  }

  /**
   * Get capabilities for a permission mode
   */
  getModeCapabilities(mode: PermissionMode): {
    autoApproveEdits: boolean;
    bypassUserConfirmation: boolean;
    planningMode: boolean;
    editingAllowed: boolean;
  } {
    switch (mode) {
      case PermissionMode.DEFAULT:
        return {
          autoApproveEdits: false,
          bypassUserConfirmation: false,
          planningMode: false,
          editingAllowed: true
        };

      case PermissionMode.ACCEPT_EDITS:
        return {
          autoApproveEdits: true,
          bypassUserConfirmation: false,
          planningMode: false,
          editingAllowed: true
        };

      case PermissionMode.BYPASS_PERMISSIONS:
        return {
          autoApproveEdits: true,
          bypassUserConfirmation: true,
          planningMode: false,
          editingAllowed: true
        };

      case PermissionMode.PLAN:
        return {
          autoApproveEdits: false,
          bypassUserConfirmation: false,
          planningMode: true,
          editingAllowed: false
        };

      default:
        throw new Error(`Unknown permission mode: ${mode}`);
    }
  }

  /**
   * Validate if mode is valid
   */
  isValidMode(mode: string): mode is PermissionMode {
    return Object.values(PermissionMode).includes(mode as PermissionMode);
  }

  /**
   * Get switch statistics
   */
  getStatistics(): {
    currentMode: PermissionMode;
    totalSwitches: number;
    averageSwitchTime: number;
    switchHistory: Array<{
      from: PermissionMode;
      to: PermissionMode;
      timestamp: number;
      duration: number;
    }>;
  } {
    const totalSwitches = this.switchHistory.length;
    const averageSwitchTime =
      totalSwitches > 0
        ? this.switchHistory.reduce((sum, s) => sum + s.duration, 0) /
          totalSwitches
        : 0;

    return {
      currentMode: this.currentMode,
      totalSwitches,
      averageSwitchTime,
      switchHistory: [...this.switchHistory]
    };
  }

  /**
   * Clear switch history
   */
  clearHistory(): void {
    this.switchHistory = [];
  }
}

export const permissionManager = new PermissionManager();
