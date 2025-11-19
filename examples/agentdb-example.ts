/**
 * AgentDB Usage Example
 * Demonstrates AgentDB integration with intelligent caching
 */

import { AgentDB, AgentConfig, SpawnResult } from '../lib/agentdb';

/**
 * Example: Using AgentDB for intelligent agent caching
 */
async function agentDBExample() {
  console.log('=== AgentDB Example ===\n');

  // 1. Initialize AgentDB
  console.log('1. Initializing AgentDB...');
  const agentDB = new AgentDB({
    qdrantUrl: process.env.QDRANT_URL || 'http://localhost:6333',
    collectionName: 'agent-cache-example',
    enableLogging: true,
    enableL1Cache: true,
    enableL2Cache: true,
    similarityThresholds: {
      exact: 0.98,
      high: 0.95,
      good: 0.90,
    },
  });

  try {
    await agentDB.initialize();
    console.log('✓ AgentDB initialized\n');
  } catch (error) {
    console.log('⚠ Qdrant unavailable, running in L1-only mode\n');
  }

  // 2. Define mock spawn function
  const mockSpawnAgent = async (config: AgentConfig): Promise<any> => {
    // Simulate agent spawning delay (250ms)
    await new Promise((resolve) => setTimeout(resolve, 250));

    return {
      id: `agent_${Date.now()}`,
      type: config.agent_type,
      name: config.agent_name,
      capabilities: config.capabilities,
      status: 'ready',
    };
  };

  // 3. Test case 1: First spawn (cache miss expected)
  console.log('2. First agent spawn (cache miss expected)...');
  const config1: AgentConfig = {
    agent_type: 'coder',
    agent_name: 'React Developer',
    capabilities: ['react', 'typescript', 'testing'],
    specialization: 'frontend',
    context: 'ecommerce project',
  };

  const result1: SpawnResult = await agentDB.findOrSpawnAgent(
    config1,
    mockSpawnAgent
  );

  console.log('Result:');
  console.log(`  - Cached: ${result1.cached}`);
  console.log(`  - Cache level: ${result1.cache_level || 'N/A'}`);
  console.log(`  - Latency: ${result1.latency_ms.toFixed(2)}ms`);
  console.log(`  - Spawn time: ${result1.spawn_time_ms?.toFixed(2) || 'N/A'}ms`);
  console.log('');

  // 4. Test case 2: Second spawn with same config (L1 cache hit expected)
  console.log('3. Second agent spawn - same config (L1 hit expected)...');
  const result2: SpawnResult = await agentDB.findOrSpawnAgent(
    config1,
    mockSpawnAgent
  );

  console.log('Result:');
  console.log(`  - Cached: ${result2.cached}`);
  console.log(`  - Cache level: ${result2.cache_level || 'N/A'}`);
  console.log(`  - Latency: ${result2.latency_ms.toFixed(2)}ms`);
  console.log(
    `  - Speedup: ${(result1.latency_ms / result2.latency_ms).toFixed(2)}x`
  );
  console.log('');

  // 5. Test case 3: Similar config (semantic match expected)
  console.log('4. Third agent spawn - similar config (semantic match)...');
  const config2: AgentConfig = {
    agent_type: 'coder',
    agent_name: 'React Component Developer',
    capabilities: ['react', 'typescript', 'testing', 'jest'],
    specialization: 'frontend',
    context: 'ecommerce project',
  };

  const result3: SpawnResult = await agentDB.findOrSpawnAgent(
    config2,
    mockSpawnAgent
  );

  console.log('Result:');
  console.log(`  - Cached: ${result3.cached}`);
  console.log(`  - Cache level: ${result3.cache_level || 'N/A'}`);
  console.log(`  - Similarity score: ${result3.similarity_score?.toFixed(4) || 'N/A'}`);
  console.log(`  - Latency: ${result3.latency_ms.toFixed(2)}ms`);
  console.log('');

  // 6. Test case 4: Different agent type (cache miss expected)
  console.log('5. Fourth agent spawn - different type (miss expected)...');
  const config3: AgentConfig = {
    agent_type: 'reviewer',
    agent_name: 'Code Reviewer',
    capabilities: ['code-review', 'security', 'best-practices'],
    specialization: 'quality-assurance',
  };

  const result4: SpawnResult = await agentDB.findOrSpawnAgent(
    config3,
    mockSpawnAgent
  );

  console.log('Result:');
  console.log(`  - Cached: ${result4.cached}`);
  console.log(`  - Cache level: ${result4.cache_level || 'N/A'}`);
  console.log(`  - Latency: ${result4.latency_ms.toFixed(2)}ms`);
  console.log('');

  // 7. Batch spawning demonstration
  console.log('6. Batch spawning (10 agents)...');
  const batchStartTime = Date.now();

  const batchConfigs: AgentConfig[] = [
    {
      agent_type: 'coder',
      agent_name: 'Backend Developer',
      capabilities: ['nodejs', 'express', 'postgresql'],
    },
    {
      agent_type: 'coder',
      agent_name: 'Frontend Developer',
      capabilities: ['react', 'redux', 'css'],
    },
    {
      agent_type: 'tester',
      agent_name: 'QA Engineer',
      capabilities: ['jest', 'playwright', 'testing'],
    },
    {
      agent_type: 'reviewer',
      agent_name: 'Senior Reviewer',
      capabilities: ['code-review', 'architecture'],
    },
    // Repeat some configs to test cache hits
    {
      agent_type: 'coder',
      agent_name: 'Backend Developer',
      capabilities: ['nodejs', 'express', 'postgresql'],
    },
    {
      agent_type: 'coder',
      agent_name: 'React Developer',
      capabilities: ['react', 'typescript', 'testing'],
    },
    {
      agent_type: 'tester',
      agent_name: 'Test Engineer',
      capabilities: ['jest', 'playwright', 'testing'],
    },
    {
      agent_type: 'coder',
      agent_name: 'Full Stack Developer',
      capabilities: ['react', 'nodejs', 'postgresql'],
    },
    {
      agent_type: 'reviewer',
      agent_name: 'Code Reviewer',
      capabilities: ['code-review', 'security', 'best-practices'],
    },
    {
      agent_type: 'coder',
      agent_name: 'Frontend Engineer',
      capabilities: ['react', 'redux', 'css'],
    },
  ];

  const batchResults = await Promise.all(
    batchConfigs.map((config) =>
      agentDB.findOrSpawnAgent(config, mockSpawnAgent)
    )
  );

  const batchTime = Date.now() - batchStartTime;
  const cacheHits = batchResults.filter((r) => r.cached).length;
  const cacheMisses = batchResults.filter((r) => !r.cached).length;

  console.log('Batch Results:');
  console.log(`  - Total agents: ${batchResults.length}`);
  console.log(`  - Cache hits: ${cacheHits}`);
  console.log(`  - Cache misses: ${cacheMisses}`);
  console.log(`  - Total time: ${batchTime}ms`);
  console.log(`  - Avg time per agent: ${(batchTime / batchResults.length).toFixed(2)}ms`);
  console.log('');

  // 8. Show statistics
  console.log('7. Cache Statistics:');
  const stats = agentDB.getStats();
  console.log(`  - Total requests: ${stats.total_requests}`);
  console.log(`  - Cache hits: ${stats.cache_hits}`);
  console.log(`  - Cache misses: ${stats.cache_misses}`);
  console.log(`  - Hit rate: ${(stats.hit_rate * 100).toFixed(2)}%`);
  console.log(`  - Avg hit latency: ${stats.avg_hit_latency_ms.toFixed(2)}ms`);
  console.log(`  - Avg miss latency: ${stats.avg_miss_latency_ms.toFixed(2)}ms`);
  console.log(`  - L1 cache size: ${stats.l1_cache_size} / ${stats.l1_cache_max}`);
  console.log(`  - Uptime: ${(stats.uptime_ms / 1000).toFixed(2)}s`);
  console.log('');

  // 9. Calculate speedup
  const baselineTime = stats.total_requests * 250; // 250ms per spawn
  const actualTime =
    stats.cache_hits * stats.avg_hit_latency_ms +
    stats.cache_misses * stats.avg_miss_latency_ms;
  const speedup = baselineTime / actualTime;

  console.log('8. Performance Analysis:');
  console.log(`  - Baseline time (no cache): ${baselineTime.toFixed(2)}ms`);
  console.log(`  - Actual time (with cache): ${actualTime.toFixed(2)}ms`);
  console.log(`  - Speedup: ${speedup.toFixed(2)}x`);
  console.log(`  - Time saved: ${(baselineTime - actualTime).toFixed(2)}ms`);
  console.log('');

  // 10. Collection info (if Qdrant available)
  try {
    const collectionInfo = await agentDB.getCollectionInfo();
    if (collectionInfo) {
      console.log('9. Qdrant Collection Info:');
      console.log(`  - Points: ${collectionInfo.points_count}`);
      console.log(`  - Vectors: ${collectionInfo.vectors_count}`);
      console.log(`  - Status: ${collectionInfo.status}`);
      console.log('');
    }
  } catch (error) {
    // Qdrant not available
  }

  // Cleanup
  console.log('10. Cleaning up...');
  await agentDB.destroy();
  console.log('✓ AgentDB destroyed\n');

  console.log('=== Example Complete ===');
}

// Run example
if (require.main === module) {
  agentDBExample()
    .then(() => {
      console.log('\n✓ Example completed successfully');
      process.exit(0);
    })
    .catch((error) => {
      console.error('\n✗ Example failed:', error);
      process.exit(1);
    });
}

export { agentDBExample };
