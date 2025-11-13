/**
 * Agent Activity Tracker
 *
 * Tracks all agent spawns, executions, and completions using MCP tools.
 * Reports to Wiki Agent for documentation.
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import { mcpIntegration } from './mcp-integration';

const execAsync = promisify(exec);

export interface AgentSpawnRecord {
  agentId: string;
  agentType: string;
  task: string;
  status: 'spawned' | 'running' | 'completed' | 'failed';
  timestamp: string;
  startTime: number;
}

export interface AgentCompletionRecord {
  agentId: string;
  agentType: string;
  task: string;
  status: 'success' | 'failure' | 'error';
  outcome: any;
  error?: string;
  duration: number;
  timestamp: string;
}

export class AgentActivityTracker {
  private agentStartTimes: Map<string, number> = new Map();
  private agentMetadata: Map<string, { agentType: string; task: string }> = new Map();

  /**
   * Track agent spawn
   * Stores data in claude-flow memory using MCP
   */
  async trackAgentSpawn(
    agentId: string,
    agentType: string,
    task: string
  ): Promise<{ agentId: string; startTime: number }> {
    const startTime = Date.now();
    const timestamp = new Date().toISOString();

    // Store in local memory for duration calculation
    this.agentStartTimes.set(agentId, startTime);
    this.agentMetadata.set(agentId, { agentType, task });

    const record: AgentSpawnRecord = {
      agentId,
      agentType,
      task,
      status: 'spawned',
      timestamp,
      startTime
    };

    // ✅ ACTIVATED: Store in persistent memory via MCP
    try {
      await mcpIntegration.storeMemory(
        'agent-activities',
        `agent-${agentId}-spawn`,
        record,
        604800 // 7 days
      );
    } catch (error) {
      console.error(`Failed to persist agent spawn to MCP:`, error);
      // Don't throw - local tracking still works
    }

    console.log(`✅ Agent Spawned: ${agentType} (${agentId}) - ${task}`);

    return { agentId, startTime };
  }

  /**
   * Monitor agent execution in real-time
   */
  async monitorAgentExecution(agentId: string): Promise<any> {
    // Get real process metrics using Node.js built-in process API
    const metrics = {
      cpu: process.cpuUsage(),
      memory: process.memoryUsage(),
      uptime: process.uptime(),
      agentId,
      timestamp: new Date().toISOString()
    };

    // ✅ ACTIVATED: Store execution metrics in MCP
    try {
      await mcpIntegration.storeMemory(
        'agent-metrics',
        `agent-${agentId}-metrics-${Date.now()}`,
        metrics,
        3600 // 1 hour TTL for metrics
      );
    } catch (error) {
      console.error(`Failed to persist agent metrics:`, error);
    }

    console.log(`📊 Agent Metrics: ${agentId}`, metrics);

    return metrics;
  }

  /**
   * Record agent completion
   */
  async trackAgentCompletion(
    agentId: string,
    status: 'success' | 'failure' | 'error',
    outcome: any,
    error?: Error
  ): Promise<{ duration: number; status: string }> {
    const endTime = Date.now();
    const timestamp = new Date().toISOString();

    // Retrieve actual spawn data from memory
    const startTime = this.agentStartTimes.get(agentId) || endTime;
    const metadata = this.agentMetadata.get(agentId) || { agentType: 'unknown', task: 'unknown' };

    // Calculate REAL duration
    const duration = endTime - startTime;

    const record: AgentCompletionRecord = {
      agentId,
      agentType: metadata.agentType,
      task: metadata.task,
      status,
      outcome,
      error: error?.message,
      duration,
      timestamp
    };

    // ✅ ACTIVATED: Store completion record in MCP
    try {
      await mcpIntegration.storeMemory(
        'agent-activities',
        `agent-${agentId}-complete`,
        record,
        604800 // 7 days
      );
    } catch (error) {
      console.error(`Failed to persist agent completion to MCP:`, error);
    }

    // Notify Wiki Agent
    await this.notifyWikiAgent({
      type: 'agent-completion',
      agentId,
      agentType: record.agentType,
      duration,
      status
    });

    console.log(`✅ Agent Completed: ${agentId} - Status: ${status}, Duration: ${duration}ms`);

    return { duration, status };
  }

  /**
   * Notify Wiki Agent of significant events
   */
  private async notifyWikiAgent(event: any): Promise<void> {
    // ✅ ACTIVATED: Store notification for Wiki Agent to process
    try {
      await mcpIntegration.storeMemory(
        'wiki-notifications',
        `wiki-event-${Date.now()}`,
        event,
        3600 // 1 hour
      );
    } catch (error) {
      console.error(`Failed to send wiki notification:`, error);
    }

    console.log(`📝 Wiki Notification: ${event.type}`, event);
  }

  /**
   * Get real system time using system call
   */
  async getRealSystemTime(): Promise<string> {
    const { stdout } = await execAsync("date '+%Y-%m-%d %H:%M:%S %Z'");
    return stdout.trim();
  }
}

// Singleton instance
export const agentTracker = new AgentActivityTracker();
