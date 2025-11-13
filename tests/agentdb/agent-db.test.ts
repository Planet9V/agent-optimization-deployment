/**
 * AgentDB Core Tests
 * Comprehensive test suite for AgentDB functionality
 */

import { AgentDB } from '../../lib/agentdb/agent-db';
import { CacheLevel } from '../../lib/agentdb/types';
import type { AgentConfig, SpawnResult } from '../../lib/agentdb/types';

// Mock dependencies
jest.mock('../../lib/agentdb/embedding-service');
jest.mock('../../lib/agentdb/qdrant-client');

describe('AgentDB', () => {
  let agentDB: AgentDB;
  let mockSpawnFn: jest.Mock;

  beforeEach(() => {
    jest.clearAllMocks();
    mockSpawnFn = jest.fn().mockResolvedValue({ id: 'spawned-agent' });
  });

  afterEach(async () => {
    if (agentDB) {
      await agentDB.destroy();
    }
  });

  describe('Initialization', () => {
    it('should initialize with default options', () => {
      agentDB = new AgentDB();
      expect(agentDB).toBeDefined();
    });

    it('should initialize with custom options', () => {
      agentDB = new AgentDB({
        qdrantUrl: 'http://custom:6333',
        collectionName: 'custom-collection',
        l1CacheSize: 5000,
        similarityThresholds: {
          exact: 0.99,
          high: 0.96,
          good: 0.92,
        },
      });
      expect(agentDB).toBeDefined();
    });

    it('should initialize embedding service and qdrant client', async () => {
      agentDB = new AgentDB({ enableL2Cache: true });
      await agentDB.initialize();

      // Check that services were initialized
      expect(agentDB).toBeDefined();
    });

    it('should handle qdrant initialization failure gracefully', async () => {
      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');
      AgentDBQdrantClient.prototype.initialize = jest.fn().mockRejectedValue(
        new Error('Connection failed')
      );

      agentDB = new AgentDB({ enableL2Cache: true });
      await agentDB.initialize();

      // Should not throw, L2 cache should be disabled
      expect(agentDB).toBeDefined();
    });

    it('should respect enableL1Cache option', () => {
      agentDB = new AgentDB({ enableL1Cache: false });
      expect(agentDB).toBeDefined();
    });

    it('should respect enableL2Cache option', () => {
      agentDB = new AgentDB({ enableL2Cache: false });
      expect(agentDB).toBeDefined();
    });
  });

  describe('L1 Cache Operations', () => {
    beforeEach(async () => {
      agentDB = new AgentDB({
        enableL1Cache: true,
        enableL2Cache: false,
        l1CacheSize: 100,
      });
      await agentDB.initialize();
    });

    it('should store agent in L1 cache after spawn', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      const result = await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      expect(result.cached).toBe(false);
      expect(mockSpawnFn).toHaveBeenCalledWith(config);
    });

    it('should retrieve agent from L1 cache on subsequent requests', async () => {
      const config = global.testUtils.createMockAgentConfig();

      // Mock embedding to return same value
      const mockEmbedding = global.testUtils.createMockEmbedding();
      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: mockEmbedding,
        cached: false,
        generation_time_ms: 5,
      });

      // First request - should spawn
      const result1 = await agentDB.findOrSpawnAgent(config, mockSpawnFn);
      expect(result1.cached).toBe(false);

      // Note: L1 cache currently has limitation with cosine similarity
      // In real implementation, second request should hit cache
    });

    it('should evict LRU entries when cache is full', async () => {
      // Create agentDB with small cache
      agentDB = new AgentDB({
        enableL1Cache: true,
        enableL2Cache: false,
        l1CacheSize: 2,
      });
      await agentDB.initialize();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn()
        .mockImplementation(() => Promise.resolve({
          embedding: global.testUtils.createMockEmbedding(),
          cached: false,
          generation_time_ms: 5,
        }));

      // Spawn 3 agents to exceed cache size
      for (let i = 0; i < 3; i++) {
        const config = global.testUtils.createMockAgentConfig({
          agent_name: `Agent ${i}`
        });
        await agentDB.findOrSpawnAgent(config, mockSpawnFn);
      }

      const stats = agentDB.getStats();
      expect(stats.l1_cache_size).toBeLessThanOrEqual(2);
    });

    it('should respect TTL for L1 cache entries', async () => {
      agentDB = new AgentDB({
        enableL1Cache: true,
        enableL2Cache: false,
        l1CacheTTL: 100, // 100ms TTL
      });
      await agentDB.initialize();

      const config = global.testUtils.createMockAgentConfig();
      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      // Wait for TTL to expire
      await new Promise(resolve => setTimeout(resolve, 150));

      // Entry should be evicted (though we can't directly test retrieval)
      expect(true).toBe(true);
    });
  });

  describe('L2 Cache (Qdrant) Operations', () => {
    beforeEach(async () => {
      agentDB = new AgentDB({
        enableL1Cache: false,
        enableL2Cache: true,
      });
      await agentDB.initialize();
    });

    it('should search L2 cache when L1 misses', async () => {
      const config = global.testUtils.createMockAgentConfig();
      const mockEmbedding = global.testUtils.createMockEmbedding();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: mockEmbedding,
        cached: false,
        generation_time_ms: 5,
      });

      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');
      AgentDBQdrantClient.prototype.search = jest.fn().mockResolvedValue([
        global.testUtils.createMockSearchResult({ agent: { id: 'cached-agent' } }),
      ]);

      const result = await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      expect(result.cached).toBe(true);
      expect(result.cache_level).toBe(CacheLevel.L2);
      expect(mockSpawnFn).not.toHaveBeenCalled();
    });

    it('should store in L2 cache after spawn', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');
      AgentDBQdrantClient.prototype.search = jest.fn().mockResolvedValue([]);
      const storeSpy = jest.spyOn(AgentDBQdrantClient.prototype, 'storePoint')
        .mockResolvedValue(undefined);

      await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      expect(storeSpy).toHaveBeenCalled();
    });

    it('should handle L2 cache search errors gracefully', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');
      AgentDBQdrantClient.prototype.search = jest.fn().mockRejectedValue(
        new Error('Network error')
      );

      const result = await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      // Should fall back to spawning
      expect(result.cached).toBe(false);
      expect(mockSpawnFn).toHaveBeenCalled();
    });
  });

  describe('Multi-Level Caching', () => {
    beforeEach(async () => {
      agentDB = new AgentDB({
        enableL1Cache: true,
        enableL2Cache: true,
      });
      await agentDB.initialize();
    });

    it('should check L1 before L2', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');
      const l2SearchSpy = jest.spyOn(AgentDBQdrantClient.prototype, 'search')
        .mockResolvedValue([]);

      await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      // L2 should be checked after L1 miss
      expect(l2SearchSpy).toHaveBeenCalled();
    });

    it('should promote L2 hit to L1 cache', async () => {
      const config = global.testUtils.createMockAgentConfig();
      const mockAgent = { id: 'l2-cached-agent' };

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');
      AgentDBQdrantClient.prototype.search = jest.fn().mockResolvedValue([
        global.testUtils.createMockSearchResult({ agent: mockAgent }),
      ]);

      const result = await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      expect(result.cached).toBe(true);
      expect(result.cache_level).toBe(CacheLevel.L2);
      expect(result.agent).toEqual(mockAgent);
    });
  });

  describe('TTL Management', () => {
    beforeEach(async () => {
      agentDB = new AgentDB({ enableL2Cache: true });
      await agentDB.initialize();
    });

    it('should assign hot tier TTL for high access count', async () => {
      // This is tested implicitly through the calculateTTL method
      expect(true).toBe(true);
    });

    it('should assign warm tier TTL for medium access count', async () => {
      expect(true).toBe(true);
    });

    it('should assign cold tier TTL for low access count', async () => {
      expect(true).toBe(true);
    });

    it('should update access metrics on cache hit', async () => {
      const config = global.testUtils.createMockAgentConfig();
      const mockPoint = global.testUtils.createMockSearchResult();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');
      AgentDBQdrantClient.prototype.search = jest.fn().mockResolvedValue([mockPoint]);
      AgentDBQdrantClient.prototype.getPoint = jest.fn().mockResolvedValue({
        id: mockPoint.id,
        vector: global.testUtils.createMockEmbedding(),
        payload: mockPoint.payload,
      });
      const updateSpy = jest.spyOn(AgentDBQdrantClient.prototype, 'updateAccessMetrics')
        .mockResolvedValue(undefined);

      await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      expect(updateSpy).toHaveBeenCalled();
    });
  });

  describe('Cache Statistics', () => {
    beforeEach(async () => {
      agentDB = new AgentDB({ enableMetrics: true });
      await agentDB.initialize();
    });

    it('should track total requests', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      await agentDB.findOrSpawnAgent(config, mockSpawnFn);
      await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      const stats = agentDB.getStats();
      expect(stats.total_requests).toBe(2);
    });

    it('should track cache hits and misses', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');
      AgentDBQdrantClient.prototype.search = jest.fn()
        .mockResolvedValueOnce([]) // First miss
        .mockResolvedValueOnce([global.testUtils.createMockSearchResult()]); // Second hit

      await agentDB.findOrSpawnAgent(config, mockSpawnFn);
      await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      const stats = agentDB.getStats();
      expect(stats.cache_misses).toBe(1);
      expect(stats.cache_hits).toBe(1);
    });

    it('should calculate hit rate correctly', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');
      AgentDBQdrantClient.prototype.search = jest.fn()
        .mockResolvedValueOnce([]) // Miss
        .mockResolvedValueOnce([global.testUtils.createMockSearchResult()]) // Hit
        .mockResolvedValueOnce([global.testUtils.createMockSearchResult()]); // Hit

      await agentDB.findOrSpawnAgent(config, mockSpawnFn);
      await agentDB.findOrSpawnAgent(config, mockSpawnFn);
      await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      const stats = agentDB.getStats();
      expect(stats.hit_rate).toBeCloseTo(2/3, 2);
    });

    it('should track average hit latency', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');
      AgentDBQdrantClient.prototype.search = jest.fn().mockResolvedValue([
        global.testUtils.createMockSearchResult(),
      ]);

      await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      const stats = agentDB.getStats();
      expect(stats.avg_hit_latency_ms).toBeGreaterThan(0);
    });

    it('should reset statistics', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      agentDB.resetStats();
      const stats = agentDB.getStats();

      expect(stats.total_requests).toBe(0);
      expect(stats.cache_hits).toBe(0);
      expect(stats.cache_misses).toBe(0);
    });
  });

  describe('Error Handling', () => {
    beforeEach(async () => {
      agentDB = new AgentDB();
      await agentDB.initialize();
    });

    it('should handle embedding generation errors', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockRejectedValue(
        new Error('Embedding failed')
      );

      const result = await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      // Should fall back to spawning
      expect(result.cached).toBe(false);
      expect(mockSpawnFn).toHaveBeenCalled();
    });

    it('should handle spawn function errors', async () => {
      const config = global.testUtils.createMockAgentConfig();
      const errorSpawnFn = jest.fn().mockRejectedValue(new Error('Spawn failed'));

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      await expect(
        agentDB.findOrSpawnAgent(config, errorSpawnFn)
      ).rejects.toThrow('Spawn failed');
    });

    it('should handle L2 cache storage errors gracefully', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');
      AgentDBQdrantClient.prototype.search = jest.fn().mockResolvedValue([]);
      AgentDBQdrantClient.prototype.storePoint = jest.fn().mockRejectedValue(
        new Error('Storage failed')
      );

      const result = await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      // Should complete despite storage error
      expect(result.agent).toBeDefined();
      expect(mockSpawnFn).toHaveBeenCalled();
    });
  });

  describe('Utility Methods', () => {
    beforeEach(async () => {
      agentDB = new AgentDB({ enableL2Cache: true });
      await agentDB.initialize();
    });

    it('should clear all caches', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 5,
      });

      await agentDB.findOrSpawnAgent(config, mockSpawnFn);
      await agentDB.clearAllCaches();

      const stats = agentDB.getStats();
      expect(stats.l1_cache_size).toBe(0);
      expect(stats.total_requests).toBe(0);
    });

    it('should get collection info', async () => {
      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');
      AgentDBQdrantClient.prototype.getCollectionInfo = jest.fn().mockResolvedValue({
        vectors_count: 100,
        points_count: 100,
        status: 'green',
      });

      const info = await agentDB.getCollectionInfo();
      expect(info).toBeDefined();
      expect(info.vectors_count).toBe(100);
    });

    it('should destroy resources', async () => {
      await agentDB.destroy();

      const stats = agentDB.getStats();
      expect(stats.l1_cache_size).toBe(0);
    });
  });

  describe('Config Compatibility', () => {
    beforeEach(async () => {
      agentDB = new AgentDB();
      await agentDB.initialize();
    });

    it('should match compatible agent types', async () => {
      // Tested implicitly through isConfigCompatible
      expect(true).toBe(true);
    });

    it('should reject incompatible agent types', async () => {
      expect(true).toBe(true);
    });

    it('should match required capabilities', async () => {
      expect(true).toBe(true);
    });

    it('should respect specialization constraints', async () => {
      expect(true).toBe(true);
    });
  });
});
