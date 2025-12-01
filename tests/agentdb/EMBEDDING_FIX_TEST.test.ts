/**
 * GAP-002 Embedding Fix Verification Test
 * Tests the embedding service fix for "Model is null or undefined" bug
 */

import { EmbeddingService } from '../../lib/agentdb/embedding-service';
import type { AgentConfig } from '../../lib/agentdb/types';

describe('GAP-002: Embedding Service Fix', () => {
  let service: EmbeddingService;

  beforeEach(() => {
    service = new EmbeddingService({
      cacheSize: 1000,
      cacheTTL: 60000,
      enableLogging: true,
    });
  });

  afterEach(async () => {
    await service.destroy();
  });

  test('Model initialization works correctly', async () => {
    await service.initialize();

    // If this completes without error, model initialization worked
    expect(true).toBe(true);
  });

  test('Can generate embedding without null model error', async () => {
    const config: AgentConfig = {
      agent_type: 'test-agent',
      agent_name: 'Test Agent',
      capabilities: ['testing'],
    };

    // This should NOT throw "Model is null or undefined"
    const result = await service.generateEmbedding(config);

    expect(result).toBeDefined();
    expect(result.embedding).toBeDefined();
    expect(result.embedding.length).toBe(384);
    expect(Array.isArray(result.embedding)).toBe(true);
  });

  test('Generated embeddings are valid numbers', async () => {
    const config: AgentConfig = {
      agent_type: 'researcher',
      agent_name: 'Research Agent',
      capabilities: ['search', 'analysis'],
    };

    const result = await service.generateEmbedding(config);

    // Check all embedding values are numbers
    result.embedding.forEach((value, index) => {
      expect(typeof value).toBe('number');
      expect(isNaN(value)).toBe(false);
      expect(isFinite(value)).toBe(true);
    });
  });

  test('Cache works correctly with embeddings', async () => {
    const config: AgentConfig = {
      agent_type: 'coder',
      agent_name: 'Code Agent',
      capabilities: ['coding'],
    };

    // First call - should generate
    const result1 = await service.generateEmbedding(config);
    expect(result1.cached).toBe(false);

    // Second call - should use cache
    const result2 = await service.generateEmbedding(config);
    expect(result2.cached).toBe(true);

    // Embeddings should be identical
    expect(result1.embedding).toEqual(result2.embedding);
  });

  test('Works with GAP-003 style checkpoint configs', async () => {
    // Simulate a checkpoint agent config like GAP-003 would use
    const checkpointConfig: AgentConfig = {
      agent_type: 'checkpoint-agent',
      agent_name: 'Query Control Checkpoint',
      capabilities: ['query-control', 'checkpoint-management'],
      specialization: 'gap-003-query-control',
      runtime: 'typescript',
      context: 'checkpoint caching for query control',
    };

    const result = await service.generateEmbedding(checkpointConfig);

    expect(result).toBeDefined();
    expect(result.embedding.length).toBe(384);
    expect(result.cached).toBe(false);

    // Cache stats should show the embedding was stored
    const stats = service.getCacheStats();
    expect(stats.size).toBeGreaterThan(0);
  });

  test('Works with GAP-006 style worker configs', async () => {
    // Simulate a worker agent config like GAP-006 would use
    const workerConfig: AgentConfig = {
      agent_type: 'worker-agent',
      agent_name: 'Job Processing Worker',
      capabilities: ['job-processing', 'state-management'],
      specialization: 'gap-006-job-management',
      runtime: 'typescript',
      context: 'worker agent caching for job queue',
    };

    const result = await service.generateEmbedding(workerConfig);

    expect(result).toBeDefined();
    expect(result.embedding.length).toBe(384);
    expect(result.cached).toBe(false);
  });

  test('Batch embedding generation works', async () => {
    const configs: AgentConfig[] = [
      {
        agent_type: 'researcher',
        agent_name: 'Researcher 1',
        capabilities: ['research'],
      },
      {
        agent_type: 'coder',
        agent_name: 'Coder 1',
        capabilities: ['coding'],
      },
      {
        agent_type: 'tester',
        agent_name: 'Tester 1',
        capabilities: ['testing'],
      },
    ];

    const results = await service.generateBatchEmbeddings(configs);

    expect(results).toHaveLength(3);
    results.forEach(result => {
      expect(result.embedding.length).toBe(384);
    });
  });
});
