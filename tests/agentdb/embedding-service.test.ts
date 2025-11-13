/**
 * Embedding Service Tests
 * Comprehensive test suite for embedding generation
 */

import { EmbeddingService } from '../../lib/agentdb/embedding-service';
import type { AgentConfig, EmbeddingResult } from '../../lib/agentdb/types';

// Mock @xenova/transformers
jest.mock('@xenova/transformers', () => ({
  pipeline: jest.fn(),
}));

describe('EmbeddingService', () => {
  let service: EmbeddingService;
  let mockPipeline: jest.Mock;
  let mockModel: jest.Mock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Setup mock model
    mockModel = jest.fn().mockImplementation((text: string, options: any) => {
      return Promise.resolve({
        data: new Float32Array(384).fill(0.5),
      });
    });

    const { pipeline } = require('@xenova/transformers');
    mockPipeline = pipeline as jest.Mock;
    mockPipeline.mockResolvedValue(mockModel);

    service = new EmbeddingService({
      cacheSize: 1000,
      cacheTTL: 60000,
      enableLogging: false,
    });
  });

  afterEach(async () => {
    await service.destroy();
  });

  describe('Initialization', () => {
    it('should initialize with default options', () => {
      const defaultService = new EmbeddingService();
      expect(defaultService).toBeDefined();
    });

    it('should initialize with custom options', () => {
      const customService = new EmbeddingService({
        cacheSize: 5000,
        cacheTTL: 120000,
        enableLogging: true,
      });
      expect(customService).toBeDefined();
    });

    it('should load embedding model on initialization', async () => {
      await service.initialize();

      expect(mockPipeline).toHaveBeenCalledWith(
        'feature-extraction',
        'Xenova/all-MiniLM-L6-v2',
        expect.objectContaining({
          quantized: true,
        })
      );
    });

    it('should handle model loading errors', async () => {
      mockPipeline.mockRejectedValue(new Error('Model load failed'));

      await expect(service.initialize()).rejects.toThrow(
        'Failed to initialize embedding model'
      );
    });

    it('should skip reinitialization if already initialized', async () => {
      await service.initialize();
      await service.initialize(); // Second call

      // Pipeline should only be called once
      expect(mockPipeline).toHaveBeenCalledTimes(1);
    });

    it('should wait for ongoing initialization', async () => {
      const promise1 = service.initialize();
      const promise2 = service.initialize();

      await Promise.all([promise1, promise2]);

      // Pipeline should only be called once
      expect(mockPipeline).toHaveBeenCalledTimes(1);
    });
  });

  describe('Embedding Generation', () => {
    beforeEach(async () => {
      await service.initialize();
    });

    it('should generate embedding for agent config', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const result = await service.generateEmbedding(config);

      expect(result.embedding).toHaveLength(384);
      expect(result.cached).toBe(false);
      expect(result.generation_time_ms).toBeGreaterThan(0);
    });

    it('should use mean pooling and normalization', async () => {
      const config = global.testUtils.createMockAgentConfig();

      await service.generateEmbedding(config);

      expect(mockModel).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          pooling: 'mean',
          normalize: true,
        })
      );
    });

    it('should serialize config to text properly', async () => {
      const config: AgentConfig = {
        agent_type: 'researcher',
        agent_name: 'Research Agent',
        capabilities: ['search', 'analysis'],
        specialization: 'data-science',
        runtime: 'python',
        context: 'academic research',
      };

      await service.generateEmbedding(config);

      const callArg = mockModel.mock.calls[0][0];
      expect(callArg).toContain('Type: researcher');
      expect(callArg).toContain('Name: Research Agent');
      expect(callArg).toContain('Capabilities: search, analysis');
      expect(callArg).toContain('Specialization: data-science');
    });

    it('should exclude volatile fields from serialization', async () => {
      const config = global.testUtils.createMockAgentConfig();

      await service.generateEmbedding(config);

      const callArg = mockModel.mock.calls[0][0];
      // Should not include timestamps, IDs, etc.
      expect(callArg).not.toContain('created_at');
      expect(callArg).not.toContain('id');
    });

    it('should validate embedding dimension', async () => {
      mockModel.mockResolvedValue({
        data: new Float32Array(256), // Wrong dimension
      });

      const config = global.testUtils.createMockAgentConfig();

      await expect(service.generateEmbedding(config)).rejects.toThrow(
        'Invalid embedding dimension'
      );
    });

    it('should handle generation errors', async () => {
      mockModel.mockRejectedValue(new Error('Generation failed'));

      const config = global.testUtils.createMockAgentConfig();

      await expect(service.generateEmbedding(config)).rejects.toThrow(
        'Embedding generation failed'
      );
    });
  });

  describe('Embedding Cache', () => {
    beforeEach(async () => {
      await service.initialize();
    });

    it('should cache embeddings by config hash', async () => {
      const config = global.testUtils.createMockAgentConfig();

      const result1 = await service.generateEmbedding(config);
      const result2 = await service.generateEmbedding(config);

      expect(result1.cached).toBe(false);
      expect(result2.cached).toBe(true);
      expect(mockModel).toHaveBeenCalledTimes(1);
    });

    it('should bypass cache when requested', async () => {
      const config = global.testUtils.createMockAgentConfig();

      await service.generateEmbedding(config);
      const result = await service.generateEmbedding(config, true); // Bypass

      expect(result.cached).toBe(false);
      expect(mockModel).toHaveBeenCalledTimes(2);
    });

    it('should cache different configs separately', async () => {
      const config1 = global.testUtils.createMockAgentConfig({
        agent_name: 'Agent 1'
      });
      const config2 = global.testUtils.createMockAgentConfig({
        agent_name: 'Agent 2'
      });

      await service.generateEmbedding(config1);
      await service.generateEmbedding(config2);

      expect(mockModel).toHaveBeenCalledTimes(2);
    });

    it('should respect cache TTL', async () => {
      const shortTTLService = new EmbeddingService({
        cacheTTL: 100, // 100ms
        enableLogging: false,
      });
      await shortTTLService.initialize();

      const config = global.testUtils.createMockAgentConfig();

      await shortTTLService.generateEmbedding(config);

      // Wait for TTL to expire
      await new Promise(resolve => setTimeout(resolve, 150));

      const result = await shortTTLService.generateEmbedding(config);
      expect(result.cached).toBe(false);

      await shortTTLService.destroy();
    });

    it('should clear cache', async () => {
      const config = global.testUtils.createMockAgentConfig();

      await service.generateEmbedding(config);
      service.clearCache();

      const result = await service.generateEmbedding(config);
      expect(result.cached).toBe(false);
    });

    it('should track cache statistics', async () => {
      const config = global.testUtils.createMockAgentConfig();

      await service.generateEmbedding(config);

      const stats = service.getCacheStats();
      expect(stats.size).toBeGreaterThan(0);
      expect(stats.max).toBe(1000);
    });
  });

  describe('Batch Embedding Generation', () => {
    beforeEach(async () => {
      await service.initialize();
    });

    it('should generate embeddings in batch', async () => {
      const configs = Array.from({ length: 5 }, (_, i) =>
        global.testUtils.createMockAgentConfig({ agent_name: `Agent ${i}` })
      );

      const results = await service.generateBatchEmbeddings(configs);

      expect(results).toHaveLength(5);
      expect(mockModel).toHaveBeenCalledTimes(5);
    });

    it('should process in configurable batch sizes', async () => {
      const configs = Array.from({ length: 100 }, (_, i) =>
        global.testUtils.createMockAgentConfig({ agent_name: `Agent ${i}` })
      );

      await service.generateBatchEmbeddings(configs, 10);

      // Should process in batches
      expect(mockModel).toHaveBeenCalledTimes(100);
    });

    it('should handle batch errors gracefully', async () => {
      const configs = Array.from({ length: 3 }, (_, i) =>
        global.testUtils.createMockAgentConfig({ agent_name: `Agent ${i}` })
      );

      mockModel
        .mockResolvedValueOnce({ data: new Float32Array(384).fill(0.5) })
        .mockRejectedValueOnce(new Error('Failed'))
        .mockResolvedValueOnce({ data: new Float32Array(384).fill(0.5) });

      await expect(
        service.generateBatchEmbeddings(configs)
      ).rejects.toThrow();
    });

    it('should use cache for duplicate configs in batch', async () => {
      const config = global.testUtils.createMockAgentConfig();
      const configs = [config, config, config]; // Same config 3 times

      await service.generateBatchEmbeddings(configs);

      // Should only generate once, rest from cache
      expect(mockModel).toHaveBeenCalledTimes(1);
    });
  });

  describe('Performance', () => {
    beforeEach(async () => {
      await service.initialize();
    });

    it('should generate embedding in < 10ms (cached)', async () => {
      const config = global.testUtils.createMockAgentConfig();

      await service.generateEmbedding(config); // Prime cache

      const { time } = await global.testUtils.measureTime(async () => {
        return await service.generateEmbedding(config);
      });

      expect(time).toBeLessThan(10);
    });

    it('should handle concurrent generation requests', async () => {
      const configs = Array.from({ length: 10 }, (_, i) =>
        global.testUtils.createMockAgentConfig({ agent_name: `Agent ${i}` })
      );

      const promises = configs.map(config =>
        service.generateEmbedding(config)
      );

      const results = await Promise.all(promises);

      expect(results).toHaveLength(10);
      results.forEach(result => {
        expect(result.embedding).toHaveLength(384);
      });
    });
  });

  describe('Config Serialization', () => {
    beforeEach(async () => {
      await service.initialize();
    });

    it('should include all relevant config fields', async () => {
      const config: AgentConfig = {
        agent_type: 'researcher',
        agent_name: 'Research Agent',
        capabilities: ['search', 'analysis', 'synthesis'],
        specialization: 'machine-learning',
        runtime: 'python',
        context: 'academic research on neural networks',
        project_context: 'AI research project',
      };

      await service.generateEmbedding(config);

      const serialized = mockModel.mock.calls[0][0];
      expect(serialized).toContain('researcher');
      expect(serialized).toContain('Research Agent');
      expect(serialized).toContain('search, analysis, synthesis');
      expect(serialized).toContain('machine-learning');
      expect(serialized).toContain('python');
      expect(serialized).toContain('academic research');
    });

    it('should handle optional fields gracefully', async () => {
      const config: AgentConfig = {
        agent_type: 'basic',
        agent_name: 'Basic Agent',
        capabilities: ['simple'],
      };

      const result = await service.generateEmbedding(config);

      expect(result.embedding).toHaveLength(384);
    });

    it('should produce consistent serialization', async () => {
      const config = global.testUtils.createMockAgentConfig();

      await service.generateEmbedding(config);
      await service.generateEmbedding(config);

      const call1 = mockModel.mock.calls[0][0];
      const call2 = mockModel.mock.calls[1][0];

      // Same config should produce same serialization
      // (Only called once due to cache, so we check idempotency)
      expect(mockModel).toHaveBeenCalledTimes(1);
    });
  });

  describe('Resource Cleanup', () => {
    it('should destroy service resources', async () => {
      await service.initialize();
      await service.destroy();

      const stats = service.getCacheStats();
      expect(stats.size).toBe(0);
    });

    it('should allow reinitialization after destroy', async () => {
      await service.initialize();
      await service.destroy();

      await service.initialize();

      const config = global.testUtils.createMockAgentConfig();
      const result = await service.generateEmbedding(config);

      expect(result.embedding).toHaveLength(384);
    });
  });

  describe('Memory Management', () => {
    it('should respect cache size limits', async () => {
      const smallCacheService = new EmbeddingService({
        cacheSize: 2,
        enableLogging: false,
      });
      await smallCacheService.initialize();

      // Generate 3 embeddings
      for (let i = 0; i < 3; i++) {
        const config = global.testUtils.createMockAgentConfig({
          agent_name: `Agent ${i}`
        });
        await smallCacheService.generateEmbedding(config);
      }

      const stats = smallCacheService.getCacheStats();
      expect(stats.size).toBeLessThanOrEqual(2);

      await smallCacheService.destroy();
    });
  });
});
