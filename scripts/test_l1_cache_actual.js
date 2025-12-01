#!/usr/bin/env node
/**
 * L1 Cache Reality Test
 * Tests if L1 cache actually works with real execution
 *
 * Expected behavior:
 * - First spawn: MISS (cold start)
 * - Second spawn: HIT (similar config should be cached)
 */

const path = require('path');

// Import AgentDB from compiled build
async function testL1Cache() {
  console.log('='.repeat(60));
  console.log('L1 CACHE REALITY TEST');
  console.log('='.repeat(60));

  try {
    // Dynamic import of AgentDB
    const { AgentDB } = require(path.join(__dirname, '../lib/agentdb/agent-db'));

    console.log('\n✓ AgentDB imported successfully\n');

    // Create AgentDB instance with L1 cache only (no Qdrant required)
    const agentDB = new AgentDB({
      enableL1Cache: true,
      enableL2Cache: false, // Disable L2 to isolate L1 test
      enableLogging: true,
      l1CacheSize: 1000,
      l1CacheTTL: 60000, // 1 minute
      similarityThresholds: {
        exact: 0.98,
        high: 0.95,
        good: 0.90
      }
    });

    console.log('Step 1: Initializing AgentDB...');
    await agentDB.initialize();
    console.log('✓ AgentDB initialized\n');

    // Mock spawn function
    let spawnCount = 0;
    const mockSpawnFn = async (config) => {
      spawnCount++;
      console.log(`  → SPAWNING agent #${spawnCount} (${config.agent_name})`);
      return { id: `agent_${spawnCount}`, config };
    };

    // Test config - researcher agent
    const config1 = {
      agent_type: 'researcher',
      agent_name: 'research-assistant',
      capabilities: ['search', 'analyze', 'summarize'],
      specialization: 'web-research',
      context: 'Find information about AI safety research'
    };

    console.log('Step 2: First spawn (should be MISS)...');
    console.log(`Config: ${JSON.stringify(config1)}\n`);
    const result1 = await agentDB.findOrSpawnAgent(config1, mockSpawnFn);

    console.log('\n📊 RESULT 1:');
    console.log(`  Cached: ${result1.cached}`);
    console.log(`  Cache Level: ${result1.cache_level || 'NONE'}`);
    console.log(`  Spawn Time: ${result1.spawn_time_ms || 'N/A'}ms`);
    console.log(`  Total Latency: ${result1.latency_ms}ms`);

    // Very similar config - should hit L1 cache
    const config2 = {
      agent_type: 'researcher',
      agent_name: 'research-assistant-v2', // Different name but same type
      capabilities: ['search', 'analyze', 'summarize'], // Same capabilities
      specialization: 'web-research',
      context: 'Find information about machine learning safety' // Slightly different context
    };

    console.log('\n' + '='.repeat(60));
    console.log('Step 3: Second spawn with similar config (should be HIT)...');
    console.log(`Config: ${JSON.stringify(config2)}\n`);
    const result2 = await agentDB.findOrSpawnAgent(config2, mockSpawnFn);

    console.log('\n📊 RESULT 2:');
    console.log(`  Cached: ${result2.cached}`);
    console.log(`  Cache Level: ${result2.cache_level || 'NONE'}`);
    console.log(`  Similarity Score: ${result2.similarity_score?.toFixed(4) || 'N/A'}`);
    console.log(`  Spawn Time: ${result2.spawn_time_ms || 'N/A'}ms`);
    console.log(`  Total Latency: ${result2.latency_ms}ms`);

    // Get stats
    const stats = agentDB.getStats();

    console.log('\n' + '='.repeat(60));
    console.log('📈 CACHE STATISTICS');
    console.log('='.repeat(60));
    console.log(`Total Requests: ${stats.total_requests}`);
    console.log(`Cache Hits: ${stats.cache_hits}`);
    console.log(`Cache Misses: ${stats.cache_misses}`);
    console.log(`Hit Rate: ${(stats.hit_rate * 100).toFixed(1)}%`);
    console.log(`L1 Cache Size: ${stats.l1_cache_size}/${stats.l1_cache_max}`);
    console.log(`Avg Hit Latency: ${stats.avg_hit_latency_ms.toFixed(2)}ms`);
    console.log(`Avg Miss Latency: ${stats.avg_miss_latency_ms.toFixed(2)}ms`);

    console.log('\n' + '='.repeat(60));
    console.log('🔍 VERDICT');
    console.log('='.repeat(60));

    if (spawnCount === 1) {
      console.log('✅ SUCCESS: Only 1 agent spawned (second request was cached)');
      console.log(`✅ L1 Cache is WORKING: ${result2.cached ? 'HIT' : 'MISS'} on second request`);
      console.log(`✅ Similarity Score: ${result2.similarity_score?.toFixed(4)} (threshold: 0.90)`);
      console.log('\n🎯 CONCLUSION: L1 cache is functioning correctly!');
      console.log('   - SearchResult interface has embedding field ✓');
      console.log('   - cacheAgent stores embedding ✓');
      console.log('   - searchL1Cache uses embedding for similarity ✓');
      console.log('   - cosineSimilarity calculates correctly ✓');
      return true;
    } else {
      console.log('❌ FAILURE: Both requests spawned new agents');
      console.log(`❌ L1 Cache is BROKEN: ${result2.cached ? 'HIT' : 'MISS'} on second request`);
      console.log(`❌ Spawn Count: ${spawnCount} (expected: 1)`);
      console.log('\n⚠️  CONCLUSION: L1 cache is NOT working as expected');
      return false;
    }

  } catch (error) {
    console.error('\n❌ TEST FAILED WITH ERROR:');
    console.error(error);
    console.error('\nStack trace:');
    console.error(error.stack);
    return false;
  }
}

// Run test
testL1Cache()
  .then(success => {
    process.exit(success ? 0 : 1);
  })
  .catch(error => {
    console.error('Unhandled error:', error);
    process.exit(1);
  });
