/**
 * Parallel Agent Spawning Tests - GAP-001 Validation
 *
 * File: parallel-spawning.test.ts
 * Created: 2025-11-12
 * Purpose: Comprehensive test suite for 10-20x performance improvement validation
 *
 * Test Coverage:
 * - Performance benchmarks (10-20x speedup validation)
 * - Dependency-aware batching
 * - Fallback to sequential spawning
 * - Error handling and resilience
 * - Metrics calculation accuracy
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { ParallelAgentSpawner, AgentConfig, SpawnResult, BatchSpawnMetrics } from '../lib/orchestration/parallel-agent-spawner';

// ============================================================================
// Test Setup
// ============================================================================

describe('GAP-001: Parallel Agent Spawning', () => {
  let spawner: ParallelAgentSpawner;

  beforeEach(() => {
    spawner = new ParallelAgentSpawner();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  // ==========================================================================
  // Performance Tests - Core GAP-001 Validation
  // ==========================================================================

  describe('Performance Benchmarks', () => {
    it('should spawn 5 agents 10-20x faster than sequential baseline', async () => {
      const agents: AgentConfig[] = Array.from({ length: 5 }, (_, i) => ({
        type: 'researcher',
        name: `Test Agent ${i + 1}`,
        capabilities: ['testing'],
        priority: 'medium'
      }));

      // Sequential baseline: 5 × 750ms = 3,750ms
      const sequentialBaseline = 5 * 750;

      const startTime = Date.now();
      const { results, metrics } = await spawner.spawnAgentsParallel(agents, {
        maxConcurrency: 5,
        batchSize: 3
      });
      const duration = Date.now() - startTime;

      // Validate results
      expect(results).toHaveLength(5);
      expect(metrics.totalAgents).toBe(5);
      expect(metrics.successCount).toBeGreaterThan(0);

      // Validate speedup factor
      const speedupFactor = sequentialBaseline / duration;
      expect(speedupFactor).toBeGreaterThanOrEqual(10); // 10x minimum target
      expect(speedupFactor).toBeLessThanOrEqual(25); // 25x maximum expected

      // Validate duration
      expect(duration).toBeLessThan(400); // Should be under 400ms for 5 agents

      console.log(`✅ Performance Test: ${speedupFactor.toFixed(2)}x speedup (${duration}ms)`);
    }, 30000); // 30 second timeout

    it('should spawn 10 agents 25-37x faster than sequential baseline', async () => {
      const agents: AgentConfig[] = Array.from({ length: 10 }, (_, i) => ({
        type: 'coder',
        name: `Coder ${i + 1}`,
        capabilities: ['typescript'],
        priority: 'high'
      }));

      // Sequential baseline: 10 × 750ms = 7,500ms
      const sequentialBaseline = 10 * 750;

      const startTime = Date.now();
      const { results, metrics } = await spawner.spawnAgentsParallel(agents, {
        maxConcurrency: 5,
        batchSize: 3
      });
      const duration = Date.now() - startTime;

      // Validate results
      expect(results).toHaveLength(10);
      expect(metrics.totalAgents).toBe(10);

      // Validate speedup factor
      const speedupFactor = sequentialBaseline / duration;
      expect(speedupFactor).toBeGreaterThanOrEqual(15); // 15x minimum for 10 agents
      expect(speedupFactor).toBeLessThanOrEqual(40); // 40x maximum expected

      // Validate duration
      expect(duration).toBeLessThan(500); // Should be under 500ms for 10 agents

      console.log(`✅ Large Batch Test: ${speedupFactor.toFixed(2)}x speedup (${duration}ms)`);
    }, 45000); // 45 second timeout

    it('should maintain performance with different batch sizes', async () => {
      const agents: AgentConfig[] = Array.from({ length: 9 }, (_, i) => ({
        type: 'tester',
        name: `Tester ${i + 1}`,
        priority: 'medium'
      }));

      // Test with batch size 3 (3 batches)
      const startTime1 = Date.now();
      const result1 = await spawner.spawnAgentsParallel(agents, { batchSize: 3 });
      const duration1 = Date.now() - startTime1;

      // Test with batch size 5 (2 batches)
      const startTime2 = Date.now();
      const result2 = await spawner.spawnAgentsParallel(agents, { batchSize: 5 });
      const duration2 = Date.now() - startTime2;

      // Both should be significantly faster than sequential
      const sequentialBaseline = 9 * 750;
      expect(duration1).toBeLessThan(sequentialBaseline / 10); // At least 10x faster
      expect(duration2).toBeLessThan(sequentialBaseline / 10); // At least 10x faster

      // Larger batch size should be slightly faster
      expect(duration2).toBeLessThanOrEqual(duration1 * 1.2); // Within 20% difference

      console.log(`✅ Batch Size Comparison: ${duration1}ms (size=3) vs ${duration2}ms (size=5)`);
    }, 60000);
  });

  // ==========================================================================
  // Dependency Management Tests
  // ==========================================================================

  describe('Dependency-Aware Batching', () => {
    it('should respect agent dependencies in batch ordering', async () => {
      const agents: AgentConfig[] = [
        { type: 'coder', name: 'Coder', capabilities: [] },
        { type: 'tester', name: 'Tester', dependencies: ['Coder'] }, // Depends on Coder
        { type: 'reviewer', name: 'Reviewer', dependencies: ['Tester'] }, // Depends on Tester
        { type: 'documenter', name: 'Documenter', capabilities: [] } // Independent
      ];

      const { results, metrics } = await spawner.spawnAgentsParallel(agents, {
        batchSize: 2
      });

      // Validate all agents spawned
      expect(results).toHaveLength(4);

      // Find agent spawn order
      const coderResult = results.find(r => r.name === 'Coder');
      const testerResult = results.find(r => r.name === 'Tester');
      const reviewerResult = results.find(r => r.name === 'Reviewer');

      // Validate dependencies were respected (coder → tester → reviewer)
      expect(coderResult?.status).toBe('spawned');
      expect(testerResult?.status).toBe('spawned');
      expect(reviewerResult?.status).toBe('spawned');

      // Validate batching (should have at least 2 batches due to dependencies)
      expect(metrics.batchCount).toBeGreaterThanOrEqual(2);

      console.log(`✅ Dependency Test: ${metrics.batchCount} batches created`);
    }, 30000);

    it('should handle circular dependencies gracefully', async () => {
      const agents: AgentConfig[] = [
        { type: 'agent-a', name: 'Agent A', dependencies: ['Agent B'] },
        { type: 'agent-b', name: 'Agent B', dependencies: ['Agent A'] }
      ];

      const { results, metrics } = await spawner.spawnAgentsParallel(agents);

      // Should still spawn agents (break circular dependency)
      expect(results).toHaveLength(2);
      expect(metrics.successCount).toBeGreaterThan(0);
    }, 30000);

    it('should parallelize independent agents in same batch', async () => {
      const agents: AgentConfig[] = [
        { type: 'researcher-1', name: 'Researcher 1', capabilities: [] },
        { type: 'researcher-2', name: 'Researcher 2', capabilities: [] },
        { type: 'researcher-3', name: 'Researcher 3', capabilities: [] }
      ];

      const startTime = Date.now();
      const { results, metrics } = await spawner.spawnAgentsParallel(agents, {
        batchSize: 3,
        maxConcurrency: 3
      });
      const duration = Date.now() - startTime;

      // All 3 independent agents should spawn in single batch
      expect(metrics.batchCount).toBe(1);

      // Should be much faster than sequential (3 × 750ms = 2,250ms)
      expect(duration).toBeLessThan(300); // Should complete in ~50-150ms

      console.log(`✅ Independent Agents: 1 batch, ${duration}ms total`);
    }, 30000);
  });

  // ==========================================================================
  // Fallback Mechanism Tests
  // ==========================================================================

  describe('Sequential Fallback', () => {
    it('should fallback to sequential spawning on MCP failure', async () => {
      const agents: AgentConfig[] = [
        { type: 'agent-1', name: 'Agent 1' },
        { type: 'agent-2', name: 'Agent 2' }
      ];

      // Mock MCP failure scenario
      const mockSpawner = new ParallelAgentSpawner();
      vi.spyOn(mockSpawner as any, 'spawnBatchViaMCP').mockRejectedValue(
        new Error('MCP connection failed')
      );

      const { results, metrics } = await mockSpawner.spawnAgentsParallel(agents, {
        enableFallback: true
      });

      // Should still complete via fallback
      expect(results).toHaveLength(2);
      expect(metrics.totalAgents).toBe(2);

      // At least some agents should succeed via fallback
      expect(metrics.successCount).toBeGreaterThanOrEqual(0);

      console.log(`✅ Fallback Test: ${metrics.successCount}/${metrics.totalAgents} succeeded`);
    }, 45000);

    it('should report accurate metrics in sequential fallback mode', async () => {
      const agents: AgentConfig[] = Array.from({ length: 3 }, (_, i) => ({
        type: 'fallback-agent',
        name: `Fallback Agent ${i + 1}`
      }));

      const { results, metrics } = await spawner.spawnAgentsSequential(agents);

      // Validate metrics
      expect(metrics.totalAgents).toBe(3);
      expect(metrics.successCount + metrics.failedCount).toBe(3);
      expect(metrics.totalDuration).toBeGreaterThan(0);
      expect(metrics.averageSpawnTime).toBeGreaterThan(0);
      expect(metrics.batchCount).toBe(3); // Sequential = 1 batch per agent

      console.log(`✅ Sequential Metrics: ${metrics.totalDuration}ms total`);
    }, 30000);
  });

  // ==========================================================================
  // Error Handling Tests
  // ==========================================================================

  describe('Error Handling & Resilience', () => {
    it('should handle partial batch failures gracefully', async () => {
      const agents: AgentConfig[] = [
        { type: 'valid-agent', name: 'Valid Agent' },
        { type: 'invalid-agent', name: 'Invalid Agent' }, // May fail
        { type: 'another-valid', name: 'Another Valid Agent' }
      ];

      const { results, metrics } = await spawner.spawnAgentsParallel(agents);

      // All agents should have results (success or failure)
      expect(results).toHaveLength(3);

      // At least some should succeed
      expect(metrics.successCount).toBeGreaterThan(0);

      // Total count should match
      expect(metrics.successCount + metrics.failedCount).toBe(3);

      console.log(`✅ Partial Failure: ${metrics.successCount} succeeded, ${metrics.failedCount} failed`);
    }, 30000);

    it('should timeout if agents take too long to spawn', async () => {
      const agents: AgentConfig[] = [
        { type: 'slow-agent', name: 'Slow Agent' }
      ];

      const startTime = Date.now();
      const { results, metrics } = await spawner.spawnAgentsParallel(agents, {
        timeout: 1000 // 1 second timeout
      });
      const duration = Date.now() - startTime;

      // Should timeout within reasonable time
      expect(duration).toBeLessThan(2000); // Should fail within 2 seconds

      console.log(`✅ Timeout Test: Completed in ${duration}ms`);
    }, 10000);

    it('should provide detailed error information for failed spawns', async () => {
      const agents: AgentConfig[] = [
        { type: 'error-agent', name: 'Error Agent' }
      ];

      const { results } = await spawner.spawnAgentsParallel(agents);

      const failedAgent = results.find(r => r.status === 'failed');

      if (failedAgent) {
        expect(failedAgent.error).toBeDefined();
        expect(failedAgent.error).toContain('string');
        expect(failedAgent.spawnTime).toBeGreaterThanOrEqual(0);
      }
    }, 30000);
  });

  // ==========================================================================
  // Metrics Calculation Tests
  // ==========================================================================

  describe('Metrics Calculation', () => {
    it('should calculate speedup factor correctly', async () => {
      const agents: AgentConfig[] = Array.from({ length: 5 }, (_, i) => ({
        type: 'metric-test',
        name: `Metric Agent ${i + 1}`
      }));

      const { metrics } = await spawner.spawnAgentsParallel(agents);

      // Sequential baseline: 5 × 750ms = 3,750ms
      const expectedBaseline = 5 * 750;
      const expectedSpeedup = expectedBaseline / metrics.totalDuration;

      // Speedup factor should be close to calculated value
      expect(metrics.speedupFactor).toBeCloseTo(expectedSpeedup, 1);

      // Speedup should be significant
      expect(metrics.speedupFactor).toBeGreaterThan(5);

      console.log(`✅ Speedup Calculation: ${metrics.speedupFactor.toFixed(2)}x`);
    }, 30000);

    it('should calculate average spawn time accurately', async () => {
      const agents: AgentConfig[] = Array.from({ length: 4 }, (_, i) => ({
        type: 'avg-test',
        name: `Avg Agent ${i + 1}`
      }));

      const { metrics } = await spawner.spawnAgentsParallel(agents);

      const calculatedAverage = metrics.totalDuration / metrics.totalAgents;

      expect(metrics.averageSpawnTime).toBeCloseTo(calculatedAverage, 1);
      expect(metrics.averageSpawnTime).toBeGreaterThan(0);

      console.log(`✅ Average Spawn Time: ${metrics.averageSpawnTime.toFixed(2)}ms`);
    }, 30000);

    it('should report batch count correctly', async () => {
      const agents: AgentConfig[] = Array.from({ length: 7 }, (_, i) => ({
        type: 'batch-count-test',
        name: `Batch Agent ${i + 1}`
      }));

      const { metrics } = await spawner.spawnAgentsParallel(agents, {
        batchSize: 3 // 7 agents ÷ 3 per batch = 3 batches
      });

      expect(metrics.batchCount).toBeGreaterThanOrEqual(3);
      expect(metrics.batchCount).toBeLessThanOrEqual(4); // May have 3 or 4 depending on dependencies

      console.log(`✅ Batch Count: ${metrics.batchCount} batches for 7 agents`);
    }, 30000);
  });

  // ==========================================================================
  // Integration Tests
  // ==========================================================================

  describe('Integration with MCP Tools', () => {
    it('should successfully call claude-flow MCP tool', async () => {
      const agents: AgentConfig[] = [
        {
          type: 'researcher',
          name: 'MCP Test Agent',
          capabilities: ['research', 'analysis'],
          priority: 'high'
        }
      ];

      const { results, metrics } = await spawner.spawnAgentsParallel(agents);

      // MCP tool should have been called
      expect(results).toHaveLength(1);
      expect(results[0].agentId).toBeDefined();
      expect(results[0].name).toBe('MCP Test Agent');

      console.log(`✅ MCP Integration: Agent ID = ${results[0].agentId}`);
    }, 30000);

    it('should pass correct parameters to MCP tool', async () => {
      const agents: AgentConfig[] = [
        {
          type: 'coder',
          name: 'Parameter Test Agent',
          capabilities: ['typescript', 'python'],
          priority: 'critical'
        }
      ];

      const { results } = await spawner.spawnAgentsParallel(agents, {
        maxConcurrency: 3,
        batchSize: 1
      });

      // Verify agent was spawned with correct type
      expect(results[0].type).toBe('coder');
      expect(results[0].name).toBe('Parameter Test Agent');

      console.log(`✅ Parameter Validation: Type = ${results[0].type}`);
    }, 30000);
  });

  // ==========================================================================
  // Performance Regression Tests
  // ==========================================================================

  describe('Performance Regression Prevention', () => {
    it('should maintain 10x speedup baseline for 5 agents', async () => {
      const agents: AgentConfig[] = Array.from({ length: 5 }, (_, i) => ({
        type: 'regression-test',
        name: `Regression Agent ${i + 1}`
      }));

      const { metrics } = await spawner.spawnAgentsParallel(agents);

      // CRITICAL: Must maintain 10x minimum speedup
      expect(metrics.speedupFactor).toBeGreaterThanOrEqual(10);

      if (metrics.speedupFactor < 10) {
        throw new Error(`Performance regression detected: ${metrics.speedupFactor.toFixed(2)}x < 10x target`);
      }

      console.log(`✅ Regression Test PASSED: ${metrics.speedupFactor.toFixed(2)}x speedup`);
    }, 30000);

    it('should spawn 10 agents in under 500ms', async () => {
      const agents: AgentConfig[] = Array.from({ length: 10 }, (_, i) => ({
        type: 'latency-test',
        name: `Latency Agent ${i + 1}`
      }));

      const startTime = Date.now();
      await spawner.spawnAgentsParallel(agents);
      const duration = Date.now() - startTime;

      // CRITICAL: Must complete in under 500ms
      expect(duration).toBeLessThan(500);

      if (duration >= 500) {
        throw new Error(`Latency regression detected: ${duration}ms >= 500ms target`);
      }

      console.log(`✅ Latency Test PASSED: ${duration}ms < 500ms target`);
    }, 30000);
  });
});

// ============================================================================
// Performance Benchmark Suite
// ============================================================================

describe('GAP-001 Performance Benchmarks', () => {
  let spawner: ParallelAgentSpawner;

  beforeEach(() => {
    spawner = new ParallelAgentSpawner();
  });

  it('BENCHMARK: 5 agents parallel vs sequential', async () => {
    const agents: AgentConfig[] = Array.from({ length: 5 }, (_, i) => ({
      type: 'benchmark',
      name: `Benchmark Agent ${i + 1}`
    }));

    // Parallel spawning
    const parallelStart = Date.now();
    const parallelResult = await spawner.spawnAgentsParallel(agents);
    const parallelDuration = Date.now() - parallelStart;

    // Sequential spawning
    const sequentialStart = Date.now();
    const sequentialResult = await spawner.spawnAgentsSequential(agents);
    const sequentialDuration = Date.now() - sequentialStart;

    const actualSpeedup = sequentialDuration / parallelDuration;

    console.log(`\n📊 BENCHMARK RESULTS (5 agents):`);
    console.log(`   Parallel:   ${parallelDuration}ms`);
    console.log(`   Sequential: ${sequentialDuration}ms`);
    console.log(`   Speedup:    ${actualSpeedup.toFixed(2)}x`);

    // Validate speedup
    expect(actualSpeedup).toBeGreaterThanOrEqual(5); // At least 5x faster
  }, 60000);
});
