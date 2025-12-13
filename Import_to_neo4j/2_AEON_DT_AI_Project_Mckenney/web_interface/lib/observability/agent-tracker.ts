/**
 * Agent Activity Tracker
 *
 * Tracks all agent spawning, task execution, and completion.
 * Reports to Wiki Agent for documentation.
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export interface AgentSpawnRecord {
  agentId: string;
  agentType: string;
  spawnedAt: string;
  systemTime: string;
  status: 'active' | 'completed' | 'failed';
}

export interface TaskExecutionRecord {
  taskId: string;
  agentId: string;
  taskDescription: string;
  startedAt: string;
  completedAt?: string;
  duration?: number;
  status: 'running' | 'completed' | 'failed';
  error?: string;
  systemTime: string;
}

export interface AgentMetrics {
  totalAgentsSpawned: number;
  activeAgents: number;
  completedTasks: number;
  failedTasks: number;
  averageTaskDuration: number;
  agentsByType: Record<string, number>;
}

export class AgentActivityTracker {
  private agents: Map<string, AgentSpawnRecord> = new Map();
  private tasks: Map<string, TaskExecutionRecord> = new Map();

  /**
   * Track agent spawn
   */
  async trackAgentSpawn(
    agentId: string,
    agentType: string
  ): Promise<AgentSpawnRecord> {
    const systemTime = await this.getRealSystemTime();

    const record: AgentSpawnRecord = {
      agentId,
      agentType,
      spawnedAt: new Date().toISOString(),
      systemTime,
      status: 'active'
    };

    this.agents.set(agentId, record);

    // Store agent spawn (via MCP through Task tool)
    // await mcp__claude_flow__memory_usage({
    //   action: 'store',
    //   namespace: 'agent-spawns',
    //   key: `agent-${agentId}`,
    //   value: JSON.stringify(record),
    //   ttl: 86400 // 24 hours
    // });

    // Notify Wiki Agent
    await this.notifyWikiAgent({
      type: 'agent-spawn',
      agentId,
      agentType
    });

    console.log(`🤖 Agent Spawned: ${agentType} (${agentId})`);

    return record;
  }

  /**
   * Track task execution start
   */
  async trackTaskStart(
    taskId: string,
    agentId: string,
    taskDescription: string
  ): Promise<TaskExecutionRecord> {
    const systemTime = await this.getRealSystemTime();

    const record: TaskExecutionRecord = {
      taskId,
      agentId,
      taskDescription,
      startedAt: new Date().toISOString(),
      status: 'running',
      systemTime
    };

    this.tasks.set(taskId, record);

    // Store task start (via MCP through Task tool)
    // await mcp__claude_flow__memory_usage({
    //   action: 'store',
    //   namespace: 'task-executions',
    //   key: `task-${taskId}`,
    //   value: JSON.stringify(record),
    //   ttl: 86400 // 24 hours
    // });

    console.log(`⏱️  Task Started: ${taskId} - ${taskDescription}`);

    return record;
  }

  /**
   * Track task completion
   */
  async trackTaskComplete(
    taskId: string,
    status: 'completed' | 'failed',
    error?: string
  ): Promise<void> {
    const task = this.tasks.get(taskId);
    if (!task) {
      console.warn(`⚠️  Task not found: ${taskId}`);
      return;
    }

    const completedAt = new Date().toISOString();
    const startTime = new Date(task.startedAt).getTime();
    const endTime = new Date(completedAt).getTime();
    const duration = endTime - startTime;

    task.completedAt = completedAt;
    task.duration = duration;
    task.status = status;
    task.error = error;

    // Update agent status if this was the last task
    const agentId = task.agentId;
    const agent = this.agents.get(agentId);
    if (agent && status === 'completed') {
      agent.status = 'completed';
    } else if (agent && status === 'failed') {
      agent.status = 'failed';
    }

    // Store task completion (via MCP through Task tool)
    // await mcp__claude_flow__memory_usage({
    //   action: 'store',
    //   namespace: 'task-executions',
    //   key: `task-${taskId}`,
    //   value: JSON.stringify(task),
    //   ttl: 86400 // 24 hours
    // });

    // Notify Wiki Agent
    await this.notifyWikiAgent({
      type: 'task-completion',
      taskId,
      agentId,
      status,
      duration,
      error
    });

    console.log(`✅ Task ${status === 'completed' ? 'Completed' : 'Failed'}: ${taskId} (${duration}ms)`);
  }

  /**
   * Get agent metrics
   */
  async getAgentMetrics(): Promise<AgentMetrics> {
    const agents = Array.from(this.agents.values());
    const tasks = Array.from(this.tasks.values());

    const activeAgents = agents.filter(a => a.status === 'active').length;
    const completedTasks = tasks.filter(t => t.status === 'completed').length;
    const failedTasks = tasks.filter(t => t.status === 'failed').length;

    const completedTasksWithDuration = tasks.filter(
      t => t.status === 'completed' && t.duration
    );
    const totalDuration = completedTasksWithDuration.reduce(
      (sum, t) => sum + (t.duration || 0),
      0
    );
    const averageTaskDuration = completedTasksWithDuration.length > 0
      ? totalDuration / completedTasksWithDuration.length
      : 0;

    const agentsByType: Record<string, number> = {};
    agents.forEach(agent => {
      agentsByType[agent.agentType] = (agentsByType[agent.agentType] || 0) + 1;
    });

    return {
      totalAgentsSpawned: agents.length,
      activeAgents,
      completedTasks,
      failedTasks,
      averageTaskDuration,
      agentsByType
    };
  }

  /**
   * Get recent agent activity
   */
  getRecentActivity(limit: number = 10): {
    agents: AgentSpawnRecord[];
    tasks: TaskExecutionRecord[];
  } {
    const agents = Array.from(this.agents.values())
      .sort((a, b) => new Date(b.spawnedAt).getTime() - new Date(a.spawnedAt).getTime())
      .slice(0, limit);

    const tasks = Array.from(this.tasks.values())
      .sort((a, b) => new Date(b.startedAt).getTime() - new Date(a.startedAt).getTime())
      .slice(0, limit);

    return { agents, tasks };
  }

  /**
   * Get real system time
   */
  private async getRealSystemTime(): Promise<string> {
    const { stdout } = await execAsync("date '+%Y-%m-%d %H:%M:%S %Z'");
    return stdout.trim();
  }

  /**
   * Notify Wiki Agent
   */
  private async notifyWikiAgent(event: any): Promise<void> {
    // Store notification (via MCP through Task tool)
    // await mcp__claude_flow__memory_usage({
    //   action: 'store',
    //   namespace: 'wiki-notifications',
    //   key: `wiki-event-${Date.now()}`,
    //   value: JSON.stringify(event),
    //   ttl: 3600 // 1 hour
    // });

    console.log(`📝 Wiki Notification: ${event.type}`, event);
  }
}

// Singleton instance
export const agentTracker = new AgentActivityTracker();
