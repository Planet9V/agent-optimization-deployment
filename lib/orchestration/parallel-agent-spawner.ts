/**
 * Parallel Agent Spawner - GAP-001 Implementation
 *
 * File: parallel-agent-spawner.ts
 * Created: 2025-11-12
 * Purpose: 10-20x performance improvement for agent spawning using MCP tools
 *
 * Performance Targets:
 * - Single agent: 750ms → 50-75ms (10-15x faster)
 * - Batch of 5: 3.75s → 150-250ms (15-20x faster)
 * - Batch of 10: 7.5s → 200-300ms (25-37x faster)
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import { extractJSON } from '../utils/mcp-parser';

const execAsync = promisify(exec);

// ============================================================================
// Type Definitions
// ============================================================================

export interface AgentConfig {
  type: string;
  name: string;
  capabilities?: string[];
  priority?: 'low' | 'medium' | 'high' | 'critical';
  dependencies?: string[]; // Agent IDs this agent depends on
}

export interface SpawnResult {
  agentId: string;
  name: string;
  type: string;
  status: 'spawned' | 'failed';
  error?: string;
  spawnTime: number;
  batchId?: string;
}

export interface BatchSpawnMetrics {
  totalAgents: number;
  successCount: number;
  failedCount: number;
  totalDuration: number;
  averageSpawnTime: number;
  speedupFactor: number; // Compared to sequential baseline
  batchCount: number;
}

export interface ParallelSpawnerOptions {
  maxConcurrency?: number;
  batchSize?: number;
  enableFallback?: boolean;
  timeout?: number;
}

// ============================================================================
// Parallel Agent Spawner Class
// ============================================================================

export class ParallelAgentSpawner {
  private readonly claudeFlowPath: string = 'npx claude-flow@alpha';
  private readonly defaultOptions: Required<ParallelSpawnerOptions> = {
    maxConcurrency: 5,
    batchSize: 3,
    enableFallback: true,
    timeout: 30000 // 30 seconds
  };

  /**
   * Spawn multiple agents in parallel using claude-flow MCP tool
   *
   * @param agents - Array of agent configurations
   * @param options - Spawning options
   * @returns Array of spawn results with performance metrics
   */
  async spawnAgentsParallel(
    agents: AgentConfig[],
    options: ParallelSpawnerOptions = {}
  ): Promise<{ results: SpawnResult[]; metrics: BatchSpawnMetrics }> {
    const opts = { ...this.defaultOptions, ...options };

    console.log(`\n🚀 Parallel Agent Spawning (GAP-001)`);
    console.log(`   Agents: ${agents.length}`);
    console.log(`   Batch Size: ${opts.batchSize}`);
    console.log(`   Max Concurrency: ${opts.maxConcurrency}`);

    const startTime = Date.now();

    try {
      // Dependency analysis and intelligent batching
      const batches = this.createDependencyBatches(agents, opts.batchSize);

      console.log(`   Batches: ${batches.length}`);

      // Execute batches with dependency-aware sequencing
      const results = await this.executeBatches(batches, opts);

      const duration = Date.now() - startTime;
      const metrics = this.calculateMetrics(results, duration, agents.length, batches.length);

      this.logResults(results, metrics);

      return { results, metrics };

    } catch (error: any) {
      const duration = Date.now() - startTime;
      console.error(`❌ Parallel spawn failed after ${duration}ms:`, error.message);

      // Fallback to sequential if enabled
      if (opts.enableFallback) {
        console.warn(`🔄 Attempting sequential fallback...`);
        return await this.spawnAgentsSequential(agents);
      }

      // Return failed results for all agents
      return {
        results: agents.map(agent => ({
          agentId: `failed-${Math.random().toString(36).substr(2, 9)}`,
          name: agent.name,
          type: agent.type,
          status: 'failed',
          error: error.message,
          spawnTime: duration
        })),
        metrics: {
          totalAgents: agents.length,
          successCount: 0,
          failedCount: agents.length,
          totalDuration: duration,
          averageSpawnTime: duration / agents.length,
          speedupFactor: 0,
          batchCount: 0
        }
      };
    }
  }

  /**
   * Create dependency-aware batches for parallel execution
   *
   * @param agents - Array of agent configurations
   * @param batchSize - Maximum agents per batch
   * @returns Array of batches (each batch can be executed in parallel)
   */
  private createDependencyBatches(agents: AgentConfig[], batchSize: number): AgentConfig[][] {
    const batches: AgentConfig[][] = [];
    const processed = new Set<string>();
    const agentMap = new Map<string, AgentConfig>();

    // Create agent lookup map
    agents.forEach(agent => agentMap.set(agent.name, agent));

    // Topological sort by dependencies
    const sortedAgents: AgentConfig[] = [];
    const queue = agents.filter(a => !a.dependencies || a.dependencies.length === 0);

    while (queue.length > 0) {
      const agent = queue.shift()!;

      if (!processed.has(agent.name)) {
        sortedAgents.push(agent);
        processed.add(agent.name);

        // Find agents that depend on this one
        agents.forEach(a => {
          if (a.dependencies?.includes(agent.name)) {
            const allDepsSatisfied = a.dependencies.every(dep => processed.has(dep));
            if (allDepsSatisfied && !processed.has(a.name)) {
              queue.push(a);
            }
          }
        });
      }
    }

    // Add any remaining agents (circular dependencies or independent)
    agents.forEach(a => {
      if (!processed.has(a.name)) {
        sortedAgents.push(a);
      }
    });

    // Group into batches
    for (let i = 0; i < sortedAgents.length; i += batchSize) {
      batches.push(sortedAgents.slice(i, i + batchSize));
    }

    return batches;
  }

  /**
   * Execute batches sequentially (batch operations are parallel)
   *
   * @param batches - Array of agent batches
   * @param options - Spawning options
   * @returns Array of spawn results
   */
  private async executeBatches(
    batches: AgentConfig[][],
    options: Required<ParallelSpawnerOptions>
  ): Promise<SpawnResult[]> {
    const allResults: SpawnResult[] = [];

    for (let i = 0; i < batches.length; i++) {
      const batch = batches[i];
      const batchId = `batch-${i + 1}`;

      console.log(`\n   📦 Batch ${i + 1}/${batches.length}: Spawning ${batch.length} agents...`);

      const batchStartTime = Date.now();

      // Call MCP tool for parallel spawning
      const batchResults = await this.spawnBatchViaMCP(batch, batchId, options);

      const batchDuration = Date.now() - batchStartTime;
      const successCount = batchResults.filter(r => r.status === 'spawned').length;

      console.log(`   ✅ Batch ${i + 1} complete: ${successCount}/${batch.length} succeeded in ${batchDuration}ms`);

      allResults.push(...batchResults);

      // Brief pause between batches for coordination
      if (i < batches.length - 1) {
        await this.sleep(50); // 50ms coordination window
      }
    }

    return allResults;
  }

  /**
   * Spawn a batch of agents using claude-flow MCP tool
   *
   * @param agents - Batch of agent configurations
   * @param batchId - Batch identifier
   * @param options - Spawning options
   * @returns Array of spawn results
   */
  private async spawnBatchViaMCP(
    agents: AgentConfig[],
    batchId: string,
    options: Required<ParallelSpawnerOptions>
  ): Promise<SpawnResult[]> {
    try {
      // Prepare agent configurations for MCP tool
      const agentConfigs = agents.map(agent => ({
        type: agent.type,
        name: agent.name,
        capabilities: agent.capabilities || [],
        priority: agent.priority || 'medium'
      }));

      // Build MCP command
      const command = `${this.claudeFlowPath} mcp agents_spawn_parallel \
        --agents '${JSON.stringify(agentConfigs)}' \
        --max-concurrency ${options.maxConcurrency} \
        --batch-size ${options.batchSize}`;

      // Execute with timeout
      const { stdout, stderr } = await execAsync(command, {
        maxBuffer: 10 * 1024 * 1024, // 10MB buffer
        timeout: options.timeout
      });

      if (stderr && !stderr.includes('warning')) {
        console.warn(`⚠️ MCP stderr:`, stderr);
      }

      // Parse MCP response with robust JSON extraction (GAP-001 FIX)
      const mcpResults: any[] = extractJSON(stdout);

      // Convert to SpawnResult format
      return mcpResults.map((result, index) => ({
        agentId: result.agentId || `${batchId}-agent-${index}`,
        name: agents[index].name,
        type: agents[index].type,
        status: result.status === 'success' ? 'spawned' : 'failed',
        error: result.error,
        spawnTime: result.spawnTime || 0,
        batchId
      }));

    } catch (error: any) {
      console.error(`❌ MCP batch spawn failed:`, error.message);

      // Return failed results for this batch
      return agents.map((agent, index) => ({
        agentId: `${batchId}-failed-${index}`,
        name: agent.name,
        type: agent.type,
        status: 'failed',
        error: error.message,
        spawnTime: 0,
        batchId
      }));
    }
  }

  /**
   * Fallback: Sequential agent spawning
   *
   * @param agents - Array of agent configurations
   * @returns Spawn results with metrics
   */
  async spawnAgentsSequential(
    agents: AgentConfig[]
  ): Promise<{ results: SpawnResult[]; metrics: BatchSpawnMetrics }> {
    console.warn(`\n⚠️ Sequential Fallback Mode`);
    console.log(`   Spawning ${agents.length} agents sequentially...`);

    const results: SpawnResult[] = [];
    const startTime = Date.now();

    for (let i = 0; i < agents.length; i++) {
      const agent = agents[i];
      const agentStartTime = Date.now();

      try {
        const command = `${this.claudeFlowPath} mcp agent_spawn \
          --type ${agent.type} \
          --name "${agent.name}" \
          --capabilities '${JSON.stringify(agent.capabilities || [])}' \
          --priority ${agent.priority || 'medium'}`;

        const { stdout } = await execAsync(command, {
          timeout: this.defaultOptions.timeout
        });

        const result = extractJSON(stdout);

        results.push({
          agentId: result.agentId || `seq-${i}`,
          name: agent.name,
          type: agent.type,
          status: 'spawned',
          spawnTime: Date.now() - agentStartTime
        });

        console.log(`   ✅ Agent ${i + 1}/${agents.length}: ${agent.name} (${results[i].spawnTime}ms)`);

      } catch (error: any) {
        results.push({
          agentId: `seq-failed-${i}`,
          name: agent.name,
          type: agent.type,
          status: 'failed',
          error: error.message,
          spawnTime: Date.now() - agentStartTime
        });

        console.error(`   ❌ Agent ${i + 1}/${agents.length}: ${agent.name} failed`);
      }
    }

    const duration = Date.now() - startTime;
    const metrics = this.calculateMetrics(results, duration, agents.length, agents.length);

    this.logResults(results, metrics);

    return { results, metrics };
  }

  /**
   * Calculate performance metrics
   */
  private calculateMetrics(
    results: SpawnResult[],
    totalDuration: number,
    totalAgents: number,
    batchCount: number
  ): BatchSpawnMetrics {
    const successCount = results.filter(r => r.status === 'spawned').length;
    const failedCount = results.filter(r => r.status === 'failed').length;
    const averageSpawnTime = totalDuration / totalAgents;

    // Calculate speedup factor (compared to 750ms sequential baseline)
    const sequentialBaseline = totalAgents * 750; // 750ms per agent
    const speedupFactor = sequentialBaseline / totalDuration;

    return {
      totalAgents,
      successCount,
      failedCount,
      totalDuration,
      averageSpawnTime,
      speedupFactor,
      batchCount
    };
  }

  /**
   * Log results and metrics
   */
  private logResults(results: SpawnResult[], metrics: BatchSpawnMetrics): void {
    console.log(`\n📊 Parallel Spawning Metrics (GAP-001)`);
    console.log(`   ─────────────────────────────────────────`);
    console.log(`   Total Agents:      ${metrics.totalAgents}`);
    console.log(`   Successful:        ${metrics.successCount}`);
    console.log(`   Failed:            ${metrics.failedCount}`);
    console.log(`   Total Duration:    ${metrics.totalDuration}ms`);
    console.log(`   Avg Spawn Time:    ${metrics.averageSpawnTime.toFixed(2)}ms`);
    console.log(`   Speedup Factor:    ${metrics.speedupFactor.toFixed(2)}x`);
    console.log(`   Batches:           ${metrics.batchCount}`);
    console.log(`   ─────────────────────────────────────────`);

    if (metrics.speedupFactor >= 10) {
      console.log(`   ✅ TARGET ACHIEVED: ${metrics.speedupFactor.toFixed(2)}x speedup (>10x target)`);
    } else {
      console.log(`   ⚠️ Below target: ${metrics.speedupFactor.toFixed(2)}x speedup (<10x target)`);
    }
  }

  /**
   * Utility: Sleep for coordination windows
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Get current system time
   */
  async getSystemTime(): Promise<string> {
    const { stdout } = await execAsync("date '+%Y-%m-%d %H:%M:%S %Z'");
    return stdout.trim();
  }
}

// ============================================================================
// Singleton Instance
// ============================================================================

export const parallelAgentSpawner = new ParallelAgentSpawner();

// ============================================================================
// Example Usage
// ============================================================================

/**
 * Example: Spawn 5 agents in parallel
 *
 * Sequential baseline: 5 × 750ms = 3,750ms
 * Parallel target: 150-250ms (15-25x faster)
 */
export async function exampleParallelSpawn(): Promise<void> {
  const agents: AgentConfig[] = [
    {
      type: 'researcher',
      name: 'Research Agent 1',
      capabilities: ['document-analysis', 'web-search'],
      priority: 'high'
    },
    {
      type: 'coder',
      name: 'Coder Agent 1',
      capabilities: ['typescript', 'python'],
      priority: 'high'
    },
    {
      type: 'tester',
      name: 'Tester Agent 1',
      capabilities: ['unit-tests', 'integration-tests'],
      priority: 'medium',
      dependencies: ['Coder Agent 1'] // Depends on coder
    },
    {
      type: 'reviewer',
      name: 'Reviewer Agent 1',
      capabilities: ['code-review', 'security-audit'],
      priority: 'medium'
    },
    {
      type: 'documenter',
      name: 'Documenter Agent 1',
      capabilities: ['technical-writing', 'api-docs'],
      priority: 'low'
    }
  ];

  const { results, metrics } = await parallelAgentSpawner.spawnAgentsParallel(agents, {
    maxConcurrency: 5,
    batchSize: 3,
    enableFallback: true
  });

  console.log(`\n✅ Spawning complete!`);
  console.log(`   Results:`, results);
  console.log(`   Metrics:`, metrics);
}
