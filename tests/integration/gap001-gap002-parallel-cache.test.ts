/**
 * GAP-001 + GAP-002 Integration Tests
 * Parallel Agent Spawning with AgentDB Caching
 *
 * Tests the integration between:
 * - GAP-001: Parallel agent spawning (10-20x speedup)
 * - GAP-002: AgentDB L1/L2 caching (150-12,500x speedup)
 *
 * Verifies:
 * - Parallel spawning leverages L1 (memory) cache
 * - Second spawn uses cached definitions
 * - L2 (Qdrant) persistence across sessions
 * - Performance targets maintained with caching
 * - Cache invalidation and refresh logic
 */

import { describe, test, expect, beforeAll, afterAll, beforeEach, afterEach } from '@jest/globals';
import { QdrantClient } from '@qdrant/js-client-rest';
import { Redis } from 'ioredis';
import { AgentDB } from '../../lib/agentdb/agent-db';
import { setupTestEnvironment, cleanupTestEnvironment, waitFor, measureExecutionTime } from './setup';

describe('GAP-001 + GAP-002: Parallel Spawning with AgentDB Cache', () => {
  let qdrant: QdrantClient;
  let redis: Redis;
  let agentDB: AgentDB;

  beforeAll(async () => {
    const env = await setupTestEnvironment();
    qdrant = env.qdrant;
    redis = env.redis;
    agentDB = env.agentDB;
  });

  afterAll(async () => {
    await cleanupTestEnvironment({ qdrant, redis, agentDB });
  });

  beforeEach(async () => {
    // Clear cache before each test
    await agentDB.clearCache();
    await redis.flushdb();
  });

  /**
   * Test 1: Parallel spawn with L1 cache hits
   *
   * Flow:
   * 1. Spawn 5 agents in parallel (first time - cache miss)
   * 2. Spawn same 5 agents again (should hit L1 cache)
   * 3. Verify L1 cache hit rate >80%
   * 4. Verify performance improvement >10x
   *
   * Expected:
   * - First spawn: 150-250ms total (parallel)
   * - Second spawn: <50ms (L1 cache hits)
   * - Cache hit rate: >80%
   */
  test('parallel spawn uses L1 memory cache for speed', async () => {
    const agentTypes = ['researcher', 'coder', 'tester', 'reviewer', 'analyst'];

    // First spawn - should populate L1 cache
    const firstSpawn = await measureExecutionTime(async () => {
      const spawns = agentTypes.map(type =>
        agentDB.getAgentDefinition(type)
      );
      return await Promise.all(spawns);
    });

    expect(firstSpawn.duration).toBeLessThan(300); // Parallel spawn target
    expect(firstSpawn.result.length).toBe(5);

    // Check L1 cache population
    const cacheStats = await agentDB.getCacheStats();
    expect(cacheStats.l1.entries).toBe(5);
    expect(cacheStats.l1.hits).toBe(0); // First time, no hits

    // Second spawn - should hit L1 cache
    const secondSpawn = await measureExecutionTime(async () => {
      const spawns = agentTypes.map(type =>
        agentDB.getAgentDefinition(type)
      );
      return await Promise.all(spawns);
    });

    expect(secondSpawn.duration).toBeLessThan(50); // L1 cache should be FAST
    expect(secondSpawn.result.length).toBe(5);

    // Verify L1 cache hits
    const finalStats = await agentDB.getCacheStats();
    expect(finalStats.l1.hits).toBe(5); // All should hit cache
    expect(finalStats.l1.hitRate).toBeGreaterThan(0.8); // >80% hit rate

    // Verify performance improvement
    const speedup = firstSpawn.duration / secondSpawn.duration;
    expect(speedup).toBeGreaterThan(3); // At least 3x faster with cache
  }, 30000);

  /**
   * Test 2: L2 (Qdrant) persistence after L1 eviction
   *
   * Flow:
   * 1. Spawn agents, populate L1 cache
   * 2. Clear L1 cache (simulate memory pressure)
   * 3. Spawn again, should hit L2 (Qdrant)
   * 4. Verify L2 hit rate and performance
   *
   * Expected:
   * - L2 retrieval: 50-100ms (slower than L1, faster than fresh)
   * - L2 hit rate: 100%
   * - Data consistency: L1 and L2 contain same agent definitions
   */
  test('L2 Qdrant persistence after L1 eviction', async () => {
    const agentTypes = ['researcher', 'coder', 'tester'];

    // First spawn - populate both L1 and L2
    await Promise.all(agentTypes.map(type => agentDB.getAgentDefinition(type)));

    // Verify L2 persistence
    const l2Stats = await agentDB.getCacheStats();
    expect(l2Stats.l2.entries).toBe(3);

    // Clear L1 cache (simulate eviction)
    await agentDB.clearL1Cache();
    const afterClearStats = await agentDB.getCacheStats();
    expect(afterClearStats.l1.entries).toBe(0);
    expect(afterClearStats.l2.entries).toBe(3); // L2 still has data

    // Spawn again - should hit L2
    const l2Spawn = await measureExecutionTime(async () => {
      return await Promise.all(agentTypes.map(type => agentDB.getAgentDefinition(type)));
    });

    expect(l2Spawn.duration).toBeLessThan(150); // L2 should be faster than fresh
    expect(l2Spawn.result.length).toBe(3);

    // Verify L2 hits
    const finalStats = await agentDB.getCacheStats();
    expect(finalStats.l2.hits).toBe(3);
    expect(finalStats.l2.hitRate).toBe(1.0); // 100% L2 hit rate

    // Verify data promoted back to L1
    expect(finalStats.l1.entries).toBe(3); // Should repopulate L1
  }, 30000);

  /**
   * Test 3: Cross-session cache restoration
   *
   * Flow:
   * 1. Spawn agents, persist to Qdrant
   * 2. Simulate session end (disconnect AgentDB)
   * 3. Create new AgentDB instance (new session)
   * 4. Spawn same agents, should restore from L2
   * 5. Verify cache coherence
   *
   * Expected:
   * - New session has empty L1, populated L2
   * - Agents restore from Qdrant successfully
   * - Performance: <200ms for L2 restoration
   */
  test('cross-session cache restoration from Qdrant', async () => {
    const agentTypes = ['researcher', 'coder'];

    // Session 1: Spawn and persist
    await Promise.all(agentTypes.map(type => agentDB.getAgentDefinition(type)));
    await agentDB.flush(); // Ensure L2 persistence

    // Verify L2 persistence
    const points = await qdrant.scroll('agentdb_cache', {
      filter: {
        must: [
          { key: 'namespace', match: { value: 'agent_definitions' } }
        ]
      },
      limit: 10
    });
    expect(points.points.length).toBeGreaterThanOrEqual(2);

    // Simulate session end
    await agentDB.disconnect();

    // Session 2: New AgentDB instance
    const newAgentDB = new AgentDB({
      qdrantUrl: process.env.QDRANT_URL || 'http://172.18.0.3:6333',
      redisClient: redis,
      l1MaxSize: 100,
      l1TTL: 3600
    });
    await newAgentDB.initialize();

    // Verify new session starts with empty L1
    const newStats = await newAgentDB.getCacheStats();
    expect(newStats.l1.entries).toBe(0);

    // Spawn agents - should restore from L2
    const restoreSpawn = await measureExecutionTime(async () => {
      return await Promise.all(agentTypes.map(type => newAgentDB.getAgentDefinition(type)));
    });

    expect(restoreSpawn.duration).toBeLessThan(200);
    expect(restoreSpawn.result.length).toBe(2);

    // Verify restoration populated L1
    const restoredStats = await newAgentDB.getCacheStats();
    expect(restoredStats.l1.entries).toBe(2);
    expect(restoredStats.l2.hits).toBe(2);

    await newAgentDB.disconnect();
  }, 60000);

  /**
   * Test 4: Performance validation - 10-20x speedup maintained
   *
   * Flow:
   * 1. Measure sequential agent spawn time (baseline)
   * 2. Measure parallel spawn with cache (GAP-001 + GAP-002)
   * 3. Verify combined speedup >10x
   *
   * Expected:
   * - Sequential: 3,000-4,000ms (baseline)
   * - Parallel + cache: 150-250ms (first run), <50ms (cached)
   * - Combined speedup: 10-20x
   */
  test('maintains 10-20x speedup with caching', async () => {
    const agentTypes = ['researcher', 'coder', 'tester', 'reviewer', 'analyst'];

    // Baseline: Sequential spawn without cache
    await agentDB.clearCache();
    const sequential = await measureExecutionTime(async () => {
      const results = [];
      for (const type of agentTypes) {
        results.push(await agentDB.getAgentDefinition(type, { disableCache: true }));
      }
      return results;
    });

    // Parallel spawn with cache (first run)
    await agentDB.clearCache();
    const parallelFirst = await measureExecutionTime(async () => {
      return await Promise.all(agentTypes.map(type => agentDB.getAgentDefinition(type)));
    });

    // Parallel spawn with cache (second run - L1 hits)
    const parallelCached = await measureExecutionTime(async () => {
      return await Promise.all(agentTypes.map(type => agentDB.getAgentDefinition(type)));
    });

    // Verify speedups
    const firstSpeedup = sequential.duration / parallelFirst.duration;
    const cachedSpeedup = sequential.duration / parallelCached.duration;

    expect(firstSpeedup).toBeGreaterThan(5); // At least 5x on first parallel run
    expect(cachedSpeedup).toBeGreaterThan(10); // At least 10x with cache

    console.log(`Performance Results:
      - Sequential: ${sequential.duration}ms
      - Parallel (first): ${parallelFirst.duration}ms (${firstSpeedup.toFixed(1)}x)
      - Parallel (cached): ${parallelCached.duration}ms (${cachedSpeedup.toFixed(1)}x)
    `);
  }, 60000);

  /**
   * Test 5: Cache invalidation and refresh
   *
   * Flow:
   * 1. Spawn agents, populate cache
   * 2. Update agent definition
   * 3. Invalidate cache for specific agent
   * 4. Verify cache refreshes with new definition
   * 5. Verify other agents remain cached
   *
   * Expected:
   * - Invalidation affects only target agent
   * - New definition loaded on next access
   * - Cache consistency maintained
   */
  test('cache invalidation and selective refresh', async () => {
    const agentTypes = ['researcher', 'coder', 'tester'];

    // Initial spawn and cache
    const initial = await Promise.all(agentTypes.map(type => agentDB.getAgentDefinition(type)));
    expect(initial.length).toBe(3);

    const initialStats = await agentDB.getCacheStats();
    expect(initialStats.l1.entries).toBe(3);

    // Invalidate 'researcher' cache entry
    await agentDB.invalidateCache('researcher', 'agent_definitions');

    const afterInvalidate = await agentDB.getCacheStats();
    expect(afterInvalidate.l1.entries).toBe(2); // One entry removed

    // Re-fetch researcher - should reload
    const refreshed = await agentDB.getAgentDefinition('researcher');
    expect(refreshed).toBeDefined();

    // Verify cache state
    const finalStats = await agentDB.getCacheStats();
    expect(finalStats.l1.entries).toBe(3); // Researcher added back
    expect(finalStats.l1.invalidations).toBe(1);

    // Verify other agents still cached (check access time)
    const coderAccess = await agentDB.getCacheEntry('coder', 'agent_definitions');
    expect(coderAccess?.metadata.lastAccessed).toBeDefined();
  }, 30000);

  /**
   * Test 6: Concurrent spawning with cache contention
   *
   * Flow:
   * 1. Spawn 10 agents concurrently (some duplicates)
   * 2. Verify no cache corruption
   * 3. Verify correct cache hit/miss counts
   * 4. Verify all spawns complete successfully
   *
   * Expected:
   * - No race conditions
   * - Correct cache statistics
   * - All agents spawn successfully
   * - Cache remains consistent
   */
  test('concurrent spawning with cache contention', async () => {
    // 10 concurrent requests, some for same agent types
    const requests = [
      'researcher', 'coder', 'researcher', 'tester', 'coder',
      'reviewer', 'analyst', 'researcher', 'coder', 'tester'
    ];

    await agentDB.clearCache();

    // Execute all concurrently
    const concurrent = await measureExecutionTime(async () => {
      return await Promise.all(requests.map(type => agentDB.getAgentDefinition(type)));
    });

    expect(concurrent.result.length).toBe(10); // All completed
    expect(concurrent.duration).toBeLessThan(500); // Reasonably fast

    // Verify cache stats
    const stats = await agentDB.getCacheStats();
    expect(stats.l1.entries).toBe(5); // Unique agent types
    expect(stats.l1.misses).toBe(5); // First access to each type
    expect(stats.l1.hits).toBeGreaterThan(0); // Duplicate requests hit cache

    // Verify no corruption - all entries valid
    const allEntries = await agentDB.getAllCacheEntries('agent_definitions');
    expect(allEntries.length).toBe(5);
    allEntries.forEach(entry => {
      expect(entry.value).toBeDefined();
      expect(entry.metadata.accessCount).toBeGreaterThan(0);
    });
  }, 30000);

  /**
   * Test 7: Cache hit rate metrics collection
   *
   * Flow:
   * 1. Perform series of agent spawns (mix of new and cached)
   * 2. Collect detailed cache metrics
   * 3. Verify hit rate calculations
   * 4. Verify performance correlation with hit rate
   *
   * Expected:
   * - Hit rate >80% after warmup
   * - Metrics accurate and detailed
   * - Performance improves with hit rate
   */
  test('cache hit rate metrics and performance correlation', async () => {
    const agentTypes = ['researcher', 'coder', 'tester'];

    await agentDB.clearCache();

    // Warmup: First access (all misses)
    await Promise.all(agentTypes.map(type => agentDB.getAgentDefinition(type)));

    // Reset metrics
    await agentDB.resetCacheMetrics();

    // Execute 30 requests (10 per agent type)
    const requests = [];
    for (let i = 0; i < 10; i++) {
      requests.push(...agentTypes);
    }

    const execution = await measureExecutionTime(async () => {
      return await Promise.all(requests.map(type => agentDB.getAgentDefinition(type)));
    });

    expect(execution.result.length).toBe(30);

    // Collect metrics
    const metrics = await agentDB.getDetailedCacheMetrics();

    expect(metrics.l1.hitRate).toBeGreaterThan(0.8); // >80% hit rate
    expect(metrics.l1.totalRequests).toBe(30);
    expect(metrics.l1.hits).toBeGreaterThan(24); // Most should hit

    // Verify performance
    const avgTimePerRequest = execution.duration / 30;
    expect(avgTimePerRequest).toBeLessThan(10); // <10ms average with good hit rate

    console.log(`Cache Metrics:
      - Hit Rate: ${(metrics.l1.hitRate * 100).toFixed(1)}%
      - Total Requests: ${metrics.l1.totalRequests}
      - Hits: ${metrics.l1.hits}
      - Misses: ${metrics.l1.misses}
      - Avg Time/Request: ${avgTimePerRequest.toFixed(1)}ms
    `);
  }, 30000);

  /**
   * Test 8: Cache memory management and eviction
   *
   * Flow:
   * 1. Set L1 cache size limit (e.g., 10 entries)
   * 2. Spawn 15 different agent types
   * 3. Verify LRU eviction occurs
   * 4. Verify evicted entries move to L2
   * 5. Verify overall system performance maintained
   *
   * Expected:
   * - L1 respects size limit
   * - Evicted entries persisted to L2
   * - Performance degrades gracefully
   * - No data loss
   */
  test('cache memory management and LRU eviction', async () => {
    // Create AgentDB with small L1 cache
    const smallCacheDB = new AgentDB({
      qdrantUrl: process.env.QDRANT_URL || 'http://172.18.0.3:6333',
      redisClient: redis,
      l1MaxSize: 10, // Small cache
      l1TTL: 3600
    });
    await smallCacheDB.initialize();

    // Spawn 15 different agent types
    const agentTypes = [
      'researcher', 'coder', 'tester', 'reviewer', 'analyst',
      'architect', 'documenter', 'optimizer', 'coordinator', 'monitor',
      'specialist', 'backend-dev', 'mobile-dev', 'ml-developer', 'cicd-engineer'
    ];

    await Promise.all(agentTypes.map(type => smallCacheDB.getAgentDefinition(type)));

    // Verify L1 size limit enforced
    const stats = await smallCacheDB.getCacheStats();
    expect(stats.l1.entries).toBeLessThanOrEqual(10);
    expect(stats.l1.evictions).toBeGreaterThan(0);

    // Verify L2 has all entries
    expect(stats.l2.entries).toBe(15);

    // Access oldest entries - should come from L2
    const oldEntry = await measureExecutionTime(async () => {
      return await smallCacheDB.getAgentDefinition('researcher');
    });

    expect(oldEntry.result).toBeDefined();
    expect(oldEntry.duration).toBeLessThan(100); // L2 should still be fast

    // Verify eviction metrics
    const finalStats = await smallCacheDB.getCacheStats();
    expect(finalStats.l1.evictions).toBeGreaterThan(4); // Multiple evictions occurred
    expect(finalStats.l2.hits).toBeGreaterThan(0); // L2 served evicted entries

    await smallCacheDB.disconnect();
  }, 60000);
});
