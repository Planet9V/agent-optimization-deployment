/**
 * SMOKE TEST: Verify L1 cache cosine similarity works
 * This is the FIRST test to run after fixing the placeholder
 */

import { AgentDB } from '../../lib/agentdb/agent-db';
import { AgentConfig } from '../../lib/agentdb/types';

async function smokeTest() {
  console.log('🔥 GAP-002 Smoke Test: L1 Cache with Real Cosine Similarity');
  console.log('===========================================================\n');

  // Initialize AgentDB with L1 cache only (no Qdrant needed for smoke test)
  const agentDB = new AgentDB({
    enableL1Cache: true,
    enableL2Cache: false, // Disable L2 for isolated L1 testing
    l1CacheSize: 100,
    enableLogging: true,
  });

  await agentDB.initialize();

  // Test config
  const testConfig: AgentConfig = {
    agent_type: 'researcher',
    agent_name: 'Data Analyst',
    capabilities: ['data-analysis', 'visualization'],
    specialization: 'statistical-analysis',
  };

  // Mock spawn function
  let spawnCount = 0;
  const mockSpawn = async (config: AgentConfig) => {
    spawnCount++;
    console.log(`   [SPAWN] Creating new agent #${spawnCount}`);
    return {
      id: `agent-${spawnCount}`,
      type: config.agent_type,
      name: config.agent_name,
    };
  };

  // Test 1: First request (cache miss, should spawn)
  console.log('TEST 1: First request (cache miss)');
  const result1 = await agentDB.findOrSpawnAgent(testConfig, mockSpawn);
  console.log(`   Result: cached=${result1.cached}, latency=${result1.latency_ms}ms`);
  console.log(`   Spawn count: ${spawnCount}`);

  if (result1.cached) {
    console.log('   ❌ FAIL: First request should not be cached');
    process.exit(1);
  }
  console.log('   ✅ PASS: First request spawned new agent\n');

  // Test 2: Second request with SAME config (cache hit via hash)
  console.log('TEST 2: Second request - exact same config (L1 hit expected)');
  const result2 = await agentDB.findOrSpawnAgent(testConfig, mockSpawn);
  console.log(`   Result: cached=${result2.cached}, latency=${result2.latency_ms}ms`);
  console.log(`   Spawn count: ${spawnCount}`);

  if (!result2.cached) {
    console.log('   ❌ FAIL: Second request should be cached');
    process.exit(1);
  }
  if (result2.latency_ms > 2) {
    console.log(`   ⚠️  WARNING: L1 cache hit took ${result2.latency_ms}ms (expected <2ms)`);
  }
  console.log('   ✅ PASS: Second request hit L1 cache\n');

  // Test 3: Similar config (different name, should match via similarity)
  console.log('TEST 3: Similar config (different agent name, similarity match expected)');
  const similarConfig: AgentConfig = {
    agent_type: 'researcher',
    agent_name: 'Research Specialist', // Different name
    capabilities: ['data-analysis', 'visualization'], // Same capabilities
    specialization: 'statistical-analysis', // Same specialization
  };

  const result3 = await agentDB.findOrSpawnAgent(similarConfig, mockSpawn);
  console.log(`   Result: cached=${result3.cached}, latency=${result3.latency_ms}ms`);
  console.log(`   Spawn count: ${spawnCount}`);

  // This should hit L1 cache via similarity (score >= 0.90)
  if (!result3.cached) {
    console.log('   ❌ FAIL: Similar config should match via cosine similarity');
    console.log('   This means cosine similarity is still broken!');
    process.exit(1);
  }
  console.log('   ✅ PASS: Similar config matched via L1 cosine similarity\n');

  // Test 4: Very different config (should NOT match)
  console.log('TEST 4: Different config (no similarity, spawn expected)');
  const differentConfig: AgentConfig = {
    agent_type: 'coder',
    agent_name: 'Backend Developer',
    capabilities: ['typescript', 'api-design'],
    specialization: 'backend-development',
  };

  const result4 = await agentDB.findOrSpawnAgent(differentConfig, mockSpawn);
  console.log(`   Result: cached=${result4.cached}, latency=${result4.latency_ms}ms`);
  console.log(`   Spawn count: ${spawnCount}`);

  if (result4.cached) {
    console.log('   ❌ FAIL: Very different config should not match');
    console.log('   This means similarity threshold is too loose!');
    process.exit(1);
  }
  console.log('   ✅ PASS: Different config correctly spawned new agent\n');

  // Get stats
  const stats = agentDB.getStats();
  console.log('===================');
  console.log('FINAL STATISTICS:');
  console.log('===================');
  console.log(`Total requests: ${stats.total_requests}`);
  console.log(`Cache hits: ${stats.cache_hits}`);
  console.log(`Cache misses: ${stats.cache_misses}`);
  console.log(`Hit rate: ${(stats.hit_rate * 100).toFixed(1)}%`);
  console.log(`Avg hit latency: ${stats.avg_hit_latency_ms.toFixed(2)}ms`);
  console.log(`Avg miss latency: ${stats.avg_miss_latency_ms.toFixed(2)}ms`);
  console.log(`Total spawns: ${spawnCount}`);

  // Validate stats
  if (stats.total_requests !== 4) {
    console.log('\n❌ FAIL: Expected 4 total requests');
    process.exit(1);
  }
  if (stats.cache_hits !== 2) {
    console.log('\n❌ FAIL: Expected 2 cache hits');
    process.exit(1);
  }
  if (stats.cache_misses !== 2) {
    console.log('\n❌ FAIL: Expected 2 cache misses');
    process.exit(1);
  }
  if (spawnCount !== 2) {
    console.log('\n❌ FAIL: Expected 2 spawns');
    process.exit(1);
  }

  await agentDB.destroy();

  console.log('\n🎉 ALL SMOKE TESTS PASSED!');
  console.log('✅ L1 cache works correctly');
  console.log('✅ Cosine similarity implemented (NO PLACEHOLDERS)');
  console.log('✅ Similarity matching functional');
  console.log('✅ Cache statistics accurate');
  console.log('\n✨ Ready for full test suite execution');
}

// Run smoke test
smokeTest().catch((error) => {
  console.error('\n💥 SMOKE TEST FAILED:', error);
  process.exit(1);
});
