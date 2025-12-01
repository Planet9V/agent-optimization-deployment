/**
 * Cache HIT Statistics Verification
 * Tests that cache_hits are properly tracked for L1 cache
 */

import { AgentDB } from '../../lib/agentdb/agent-db';
import type { AgentConfig } from '../../lib/agentdb/types';

async function verifyCacheHits() {
  console.log('🔍 Verifying Cache HIT Tracking...\n');

  // Initialize AgentDB with L1 enabled
  const agentDB = new AgentDB({
    enableL1Cache: true,
    enableL2Cache: false,
    l1CacheSize: 100,
    enableLogging: true,
  });

  try {
    await agentDB.initialize();

    // Test config - using same config for all calls to get cache hits
    const config: AgentConfig = {
      agent_type: 'researcher',
      agent_name: 'test-agent',
      capabilities: ['search', 'analyze'],
    };

    // Mock spawn function
    let spawnCount = 0;
    const mockSpawnFn = async (cfg: AgentConfig) => {
      spawnCount++;
      await new Promise(resolve => setTimeout(resolve, 10)); // Simulate work
      return { id: `agent-${spawnCount}`, config: cfg };
    };

    console.log('📊 Performing test operations...');

    // First call - should be a MISS (empty cache)
    console.log('\n1️⃣  First call (expect MISS):');
    const result1 = await agentDB.findOrSpawnAgent(config, mockSpawnFn);
    console.log(`   Result: cached=${result1.cached}, spawn_count=${spawnCount}`);

    // Second call - should be a HIT (cached from first call)
    console.log('\n2️⃣  Second call (expect HIT):');
    const result2 = await agentDB.findOrSpawnAgent(config, mockSpawnFn);
    console.log(`   Result: cached=${result2.cached}, spawn_count=${spawnCount}`);

    // Third call - should be a HIT (still cached)
    console.log('\n3️⃣  Third call (expect HIT):');
    const result3 = await agentDB.findOrSpawnAgent(config, mockSpawnFn);
    console.log(`   Result: cached=${result3.cached}, spawn_count=${spawnCount}`);

    // Get stats
    const stats = agentDB.getStats();
    console.log('\n📈 Cache Statistics:');
    console.log('─────────────────────────────────');
    console.log(`Total Requests:    ${stats.total_requests}`);
    console.log(`Cache Hits:        ${stats.cache_hits}`);
    console.log(`Cache Misses:      ${stats.cache_misses}`);
    console.log(`Hit Rate:          ${(stats.hit_rate * 100).toFixed(2)}%`);
    console.log(`L1 Cache Size:     ${stats.l1_cache_size}`);
    console.log(`Spawn Count:       ${spawnCount}`);
    console.log('─────────────────────────────────\n');

    // Verification
    console.log('✅ Verification Results:');
    const issues: string[] = [];

    if (stats.total_requests !== 3) {
      issues.push(`❌ Expected 3 total requests, got ${stats.total_requests}`);
    } else {
      console.log('✓ Total requests tracked correctly');
    }

    if (stats.cache_hits !== 2) {
      issues.push(`❌ Expected 2 cache hits, got ${stats.cache_hits}`);
    } else {
      console.log('✓ Cache hits tracked correctly (2 hits after initial miss)');
    }

    if (stats.cache_misses !== 1) {
      issues.push(`❌ Expected 1 cache miss, got ${stats.cache_misses}`);
    } else {
      console.log('✓ Cache misses tracked correctly (1 initial miss)');
    }

    const expectedHitRate = 2 / 3;
    if (Math.abs(stats.hit_rate - expectedHitRate) > 0.01) {
      issues.push(`❌ Expected ${(expectedHitRate * 100).toFixed(2)}% hit rate, got ${(stats.hit_rate * 100).toFixed(2)}%`);
    } else {
      console.log(`✓ Hit rate calculated correctly (${(stats.hit_rate * 100).toFixed(2)}%)`);
    }

    if (spawnCount !== 1) {
      issues.push(`❌ Expected 1 spawn (first call only), got ${spawnCount}`);
    } else {
      console.log('✓ Agent spawned only once (cache working)');
    }

    if (stats.l1_cache_size !== 1) {
      issues.push(`❌ Expected 1 entry in L1 cache, got ${stats.l1_cache_size}`);
    } else {
      console.log('✓ L1 cache size tracked correctly');
    }

    // Final result
    console.log('\n' + '═'.repeat(40));
    if (issues.length === 0) {
      console.log('🎉 ALL CHECKS PASSED - Cache HIT tracking works!');
      console.log('═'.repeat(40) + '\n');
      process.exit(0);
    } else {
      console.log('⚠️  ISSUES FOUND:');
      issues.forEach(issue => console.log(issue));
      console.log('═'.repeat(40) + '\n');
      process.exit(1);
    }

  } catch (error) {
    console.error('❌ Error during verification:', error);
    process.exit(1);
  } finally {
    await agentDB.destroy();
  }
}

// Run verification
verifyCacheHits();
