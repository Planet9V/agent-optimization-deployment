/**
 * Cache Statistics Verification Script
 * Tests that cache_hits and cache_misses are properly tracked
 */

import { AgentDB } from '../../lib/agentdb/agent-db';
import type { AgentConfig } from '../../lib/agentdb/types';

async function verifyCacheStats() {
  console.log('🔍 Verifying Cache Statistics Tracking...\n');

  // Initialize AgentDB with L1 and L2 disabled for predictable testing
  const agentDB = new AgentDB({
    enableL1Cache: false,
    enableL2Cache: false,
    enableLogging: true,
  });

  try {
    await agentDB.initialize();

    // Test config
    const config: AgentConfig = {
      agent_type: 'researcher',
      agent_name: 'test-agent',
      capabilities: ['search', 'analyze'],
    };

    // Mock spawn function
    let spawnCount = 0;
    const mockSpawnFn = async (cfg: AgentConfig) => {
      spawnCount++;
      return { id: `agent-${spawnCount}`, config: cfg };
    };

    // Perform multiple operations to generate stats
    console.log('📊 Performing test operations...');

    // First call - should be a MISS (no cache)
    await agentDB.findOrSpawnAgent(config, mockSpawnFn);

    // Second call - should be a MISS (L1/L2 disabled)
    await agentDB.findOrSpawnAgent(config, mockSpawnFn);

    // Third call - should be a MISS (L1/L2 disabled)
    await agentDB.findOrSpawnAgent(config, mockSpawnFn);

    // Get stats
    const stats = agentDB.getStats();
    console.log('\n📈 Cache Statistics:');
    console.log('─────────────────────────────────');
    console.log(`Total Requests:    ${stats.total_requests}`);
    console.log(`Cache Hits:        ${stats.cache_hits}`);
    console.log(`Cache Misses:      ${stats.cache_misses}`);
    console.log(`Hit Rate:          ${(stats.hit_rate * 100).toFixed(2)}%`);
    console.log(`Avg Hit Latency:   ${stats.avg_hit_latency_ms.toFixed(2)}ms`);
    console.log(`Avg Miss Latency:  ${stats.avg_miss_latency_ms.toFixed(2)}ms`);
    console.log('─────────────────────────────────\n');

    // Verification
    console.log('✅ Verification Results:');
    const issues: string[] = [];

    if (stats.total_requests !== 3) {
      issues.push(`❌ Expected 3 total requests, got ${stats.total_requests}`);
    } else {
      console.log('✓ Total requests tracked correctly');
    }

    if (stats.cache_hits !== 0) {
      issues.push(`❌ Expected 0 cache hits, got ${stats.cache_hits}`);
    } else {
      console.log('✓ Cache hits tracked correctly');
    }

    if (stats.cache_misses !== 3) {
      issues.push(`❌ Expected 3 cache misses, got ${stats.cache_misses}`);
    } else {
      console.log('✓ Cache misses tracked correctly');
    }

    if (stats.hit_rate !== 0) {
      issues.push(`❌ Expected 0% hit rate, got ${(stats.hit_rate * 100).toFixed(2)}%`);
    } else {
      console.log('✓ Hit rate calculated correctly');
    }

    if (stats.avg_miss_latency_ms <= 0) {
      issues.push(`❌ Expected positive miss latency, got ${stats.avg_miss_latency_ms}ms`);
    } else {
      console.log('✓ Miss latency tracked correctly');
    }

    // Final result
    console.log('\n' + '═'.repeat(40));
    if (issues.length === 0) {
      console.log('🎉 ALL CHECKS PASSED - Cache stats tracking works!');
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
verifyCacheStats();
