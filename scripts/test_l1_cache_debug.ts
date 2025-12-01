#!/usr/bin/env tsx
/**
 * L1 Cache Debug Test
 * Investigates why L1 cache isn't matching similar embeddings
 */

import { AgentDB } from '../lib/agentdb/agent-db';
import { AgentConfig } from '../lib/agentdb/types';

async function debugL1Cache(): Promise<void> {
  console.log('='.repeat(60));
  console.log('L1 CACHE DEBUG INVESTIGATION');
  console.log('='.repeat(60));

  const agentDB = new AgentDB({
    enableL1Cache: true,
    enableL2Cache: false,
    enableLogging: true,
    l1CacheSize: 1000,
    similarityThresholds: {
      exact: 0.98,
      high: 0.95,
      good: 0.90
    }
  });

  await agentDB.initialize();

  let spawnCount = 0;
  const mockSpawnFn = async (config: AgentConfig): Promise<any> => {
    spawnCount++;
    return { id: `agent_${spawnCount}`, config };
  };

  // First spawn
  const config1: AgentConfig = {
    agent_type: 'researcher',
    agent_name: 'research-assistant',
    capabilities: ['search', 'analyze', 'summarize'],
    specialization: 'web-research',
    context: 'Find information about AI safety'
  };

  console.log('\n1️⃣ First spawn...');
  const result1 = await agentDB.findOrSpawnAgent(config1, mockSpawnFn);
  console.log(`Result: cached=${result1.cached}, spawns=${spawnCount}`);

  // Access private l1Cache to inspect what was stored
  const l1Cache = (agentDB as any).l1Cache;
  const entries = Array.from(l1Cache.entries());

  console.log(`\n🔍 L1 Cache Inspection after first spawn:`);
  console.log(`Cache size: ${entries.length}`);

  if (entries.length > 0) {
    const [id, result] = entries[0];
    console.log(`\nEntry 1:`);
    console.log(`  ID: ${id}`);
    console.log(`  Score: ${result.score}`);
    console.log(`  Has agent: ${!!result.agent}`);
    console.log(`  Has embedding: ${!!result.embedding}`);
    if (result.embedding) {
      console.log(`  Embedding dimension: ${result.embedding.length}`);
      console.log(`  Embedding sample: [${result.embedding.slice(0, 5).map(n => n.toFixed(4)).join(', ')}...]`);
    }
    console.log(`  Agent type: ${result.payload.agent_type}`);
    console.log(`  Capabilities: ${result.payload.capabilities.join(', ')}`);
  }

  // Second spawn with EXACT same config
  console.log('\n' + '='.repeat(60));
  console.log('2️⃣ Second spawn with EXACT SAME config...');
  const result2 = await agentDB.findOrSpawnAgent(config1, mockSpawnFn);
  console.log(`Result: cached=${result2.cached}, spawns=${spawnCount}`);
  console.log(`Cache size: ${l1Cache.size}`);

  // Third spawn with slightly different config
  console.log('\n' + '='.repeat(60));
  console.log('3️⃣ Third spawn with SIMILAR config...');
  const config3: AgentConfig = {
    agent_type: 'researcher',
    agent_name: 'research-assistant-v2',
    capabilities: ['search', 'analyze', 'summarize'],
    specialization: 'web-research',
    context: 'Find information about machine learning'
  };
  const result3 = await agentDB.findOrSpawnAgent(config3, mockSpawnFn);
  console.log(`Result: cached=${result3.cached}, spawns=${spawnCount}`);
  if (result3.similarity_score) {
    console.log(`Similarity score: ${result3.similarity_score.toFixed(4)}`);
  }

  // Get embedding service to generate embeddings directly
  const embeddingService = (agentDB as any).embeddingService;

  console.log('\n' + '='.repeat(60));
  console.log('🔬 DIRECT EMBEDDING COMPARISON');
  console.log('='.repeat(60));

  const emb1 = await embeddingService.generateEmbedding(config1);
  const emb3 = await embeddingService.generateEmbedding(config3);

  console.log(`\nEmbedding 1 (config1):`);
  console.log(`  Dimension: ${emb1.embedding.length}`);
  console.log(`  Sample: [${emb1.embedding.slice(0, 5).map(n => n.toFixed(4)).join(', ')}...]`);
  console.log(`  Cached: ${emb1.cached}`);

  console.log(`\nEmbedding 3 (config3):`);
  console.log(`  Dimension: ${emb3.embedding.length}`);
  console.log(`  Sample: [${emb3.embedding.slice(0, 5).map(n => n.toFixed(4)).join(', ')}...]`);
  console.log(`  Cached: ${emb3.cached}`);

  // Calculate similarity manually
  const cosineSimilarity = (a: number[], b: number[]): number => {
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;

    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }

    if (normA === 0 || normB === 0) return 0;
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
  };

  const similarity = cosineSimilarity(emb1.embedding, emb3.embedding);
  console.log(`\n🎯 Manual Cosine Similarity: ${similarity.toFixed(4)}`);
  console.log(`   Threshold (good): 0.90`);
  console.log(`   Would match: ${similarity >= 0.90 ? 'YES ✅' : 'NO ❌'}`);

  // Final stats
  console.log('\n' + '='.repeat(60));
  console.log('📊 FINAL STATISTICS');
  console.log('='.repeat(60));
  const stats = agentDB.getStats();
  console.log(`Total spawns: ${spawnCount}`);
  console.log(`Total requests: ${stats.total_requests}`);
  console.log(`Cache hits: ${stats.cache_hits}`);
  console.log(`Cache misses: ${stats.cache_misses}`);
  console.log(`Hit rate: ${(stats.hit_rate * 100).toFixed(1)}%`);
  console.log(`L1 cache size: ${stats.l1_cache_size}`);

  console.log('\n' + '='.repeat(60));
  console.log('🔍 ROOT CAUSE ANALYSIS');
  console.log('='.repeat(60));

  if (spawnCount === 1) {
    console.log('✅ L1 cache is WORKING - only 1 spawn occurred');
  } else if (spawnCount === 2 && result2.cached) {
    console.log('✅ L1 cache is WORKING - exact match succeeded');
    console.log('❌ Similar config matching FAILED');
    console.log('\n💡 HYPOTHESIS: Similarity threshold too high or embedding variation too large');
  } else if (spawnCount === 3) {
    console.log('❌ L1 cache is COMPLETELY BROKEN - even exact match failed!');
    console.log('\n💡 HYPOTHESIS: searchL1Cache() may not be checking cache correctly');
    console.log('   Possible issues:');
    console.log('   1. Embedding not being stored in SearchResult');
    console.log('   2. searchL1Cache() not finding entries');
    console.log('   3. Config hash comparison preventing matches');
  }
}

debugL1Cache()
  .then(() => process.exit(0))
  .catch(error => {
    console.error('Error:', error);
    process.exit(1);
  });
