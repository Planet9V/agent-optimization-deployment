/**
 * GAP-003 Query Control System - Command Executor
 * Runtime command execution with security validation
 */

import { mcpClient } from '../mcp-client';

export interface CommandExecutionResult {
  success: boolean;
  command: string;
  output?: string;
  error?: string;
  executionTimeMs: number;
  blocked?: boolean;
  blockReason?: string;
}

/**
 * Command Executor
 * Executes runtime commands with security validation
 */
export class CommandExecutor {
  private commandHistory: Array<{
    command: string;
    timestamp: number;
    success: boolean;
    duration: number;
  }> = [];

  // Security blacklist - dangerous commands
  private readonly DANGEROUS_COMMANDS = [
    'rm -rf',
    'dd if=',
    'mkfs',
    ':(){:|:&};:',
    'fork bomb',
    ':(){ :|:& };:',
    'chmod -R 777 /',
    'mv / /dev/null',
    '> /dev/sda',
    'wget http'
  ];

  /**
   * Execute a runtime command
   */
  async executeCommand(
    queryId: string,
    command: string
  ): Promise<CommandExecutionResult> {
    const startTime = Date.now();

    try {
      console.log(`Executing command for query ${queryId}: ${command}`);

      // Security validation
      const securityCheck = this.validateCommandSecurity(command);
      if (!securityCheck.safe) {
        console.warn(`Blocked dangerous command: ${command}`);
        console.warn(`Reason: ${securityCheck.reason}`);

        // Train failure pattern for dangerous commands
        await mcpClient.trainNeuralPattern(
          'coordination',
          `dangerous_command_blocked:${command}:${securityCheck.reason}`,
          30
        );

        return {
          success: false,
          command,
          executionTimeMs: Date.now() - startTime,
          blocked: true,
          blockReason: securityCheck.reason
        };
      }

      // Execute command via MCP
      const result = await mcpClient.queryControl({
        action: 'execute_command',
        queryId,
        command
      });

      const executionTime = Date.now() - startTime;

      // Store command execution in memory
      await mcpClient.storeMemory(
        `command_${queryId}_${Date.now()}`,
        {
          command,
          executedAt: Date.now(),
          output: result.output || '',
          success: true,
          duration: executionTime
        },
        3600 // 1 hour TTL
      );

      // Track command history
      this.commandHistory.push({
        command,
        timestamp: Date.now(),
        success: true,
        duration: executionTime
      });

      // Train neural pattern on command execution
      await mcpClient.trainNeuralPattern(
        'optimization',
        `command_execution:${command}:${executionTime}ms:success`,
        20
      );

      console.log(
        `Command executed successfully: ${command} (${executionTime}ms)`
      );

      return {
        success: true,
        command,
        output: result.output || 'Command executed successfully',
        executionTimeMs: executionTime
      };
    } catch (error) {
      const executionTime = Date.now() - startTime;

      console.error(`Command execution failed: ${error}`);

      // Track failed command
      this.commandHistory.push({
        command,
        timestamp: Date.now(),
        success: false,
        duration: executionTime
      });

      // Train failure pattern
      await mcpClient.trainNeuralPattern(
        'coordination',
        `command_execution_failed:${command}:${error}`,
        10
      );

      return {
        success: false,
        command,
        error: String(error),
        executionTimeMs: executionTime
      };
    }
  }

  /**
   * Validate command security
   */
  validateCommandSecurity(command: string): {
    safe: boolean;
    reason?: string;
  } {
    const commandLower = command.toLowerCase().trim();

    // Check against blacklist
    for (const dangerous of this.DANGEROUS_COMMANDS) {
      if (commandLower.includes(dangerous.toLowerCase())) {
        return {
          safe: false,
          reason: `Command contains dangerous pattern: ${dangerous}`
        };
      }
    }

    // Check for suspicious patterns
    if (commandLower.includes('sudo') && commandLower.includes('rm')) {
      return {
        safe: false,
        reason: 'Suspicious combination: sudo + rm'
      };
    }

    if (commandLower.match(/>\s*\/dev\/sd[a-z]/)) {
      return {
        safe: false,
        reason: 'Attempt to write to block device'
      };
    }

    if (commandLower.includes('/etc/passwd') || commandLower.includes('/etc/shadow')) {
      return {
        safe: false,
        reason: 'Attempt to access sensitive system files'
      };
    }

    // Command passes all checks
    return { safe: true };
  }

  /**
   * Get command execution statistics
   */
  getStatistics(): {
    totalCommands: number;
    successfulCommands: number;
    failedCommands: number;
    averageExecutionTime: number;
    commandHistory: Array<{
      command: string;
      timestamp: number;
      success: boolean;
      duration: number;
    }>;
  } {
    const totalCommands = this.commandHistory.length;
    const successfulCommands = this.commandHistory.filter(
      (c) => c.success
    ).length;
    const failedCommands = totalCommands - successfulCommands;
    const averageExecutionTime =
      totalCommands > 0
        ? this.commandHistory.reduce((sum, c) => sum + c.duration, 0) /
          totalCommands
        : 0;

    return {
      totalCommands,
      successfulCommands,
      failedCommands,
      averageExecutionTime,
      commandHistory: [...this.commandHistory]
    };
  }

  /**
   * Clear command history
   */
  clearHistory(): void {
    this.commandHistory = [];
  }

  /**
   * Check if command is in blacklist
   */
  isCommandBlacklisted(command: string): boolean {
    const commandLower = command.toLowerCase().trim();
    return this.DANGEROUS_COMMANDS.some((dangerous) =>
      commandLower.includes(dangerous.toLowerCase())
    );
  }

  /**
   * Get blacklist
   */
  getBlacklist(): string[] {
    return [...this.DANGEROUS_COMMANDS];
  }
}

export const commandExecutor = new CommandExecutor();
