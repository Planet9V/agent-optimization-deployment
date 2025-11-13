/**
 * Qdrant Client Tests
 * Comprehensive test suite for Qdrant integration
 */

import { AgentDBQdrantClient } from '../../lib/agentdb/qdrant-client';
import type { AgentPoint, SearchFilter } from '../../lib/agentdb/types';

// Create mock methods that can be accessed across tests
const mockMethods = {
  getCollections: jest.fn(),
  createCollection: jest.fn(),
  getCollection: jest.fn(),
  deleteCollection: jest.fn(),
  upsert: jest.fn(),
  search: jest.fn(),
  retrieve: jest.fn(),
  setPayload: jest.fn(),
  delete: jest.fn(),
};

// Mock @qdrant/js-client-rest
jest.mock('@qdrant/js-client-rest', () => ({
  QdrantClient: jest.fn().mockImplementation(() => mockMethods),
}));

describe('AgentDBQdrantClient', () => {
  let client: AgentDBQdrantClient;
  let mockQdrantClient: any;

  beforeEach(() => {
    jest.clearAllMocks();
    mockQdrantClient = mockMethods;
    client = new AgentDBQdrantClient({
      url: 'http://test:6333',
      apiKey: 'test-key',
      collectionName: 'test-collection',
      dimension: 384,
      enableLogging: false,
    });
  });

  afterEach(async () => {
    await client.destroy();
  });

  describe('Initialization', () => {
    it('should initialize with default options', () => {
      const defaultClient = new AgentDBQdrantClient();
      expect(defaultClient).toBeDefined();
    });

    it('should initialize with custom options', () => {
      const customClient = new AgentDBQdrantClient({
        url: 'http://custom:6333',
        apiKey: 'custom-key',
        collectionName: 'custom-collection',
        dimension: 512,
      });
      expect(customClient).toBeDefined();
    });

    it('should check if collection exists on initialize', async () => {
      mockQdrantClient.getCollections.mockResolvedValue({
        collections: [{ name: 'test-collection' }],
      });

      await client.initialize();
      expect(mockQdrantClient.getCollections).toHaveBeenCalled();
    });

    it('should create collection if it does not exist', async () => {
      mockQdrantClient.getCollections.mockResolvedValue({
        collections: [],
      });
      mockQdrantClient.createCollection.mockResolvedValue({});

      await client.initialize();

      expect(mockQdrantClient.createCollection).toHaveBeenCalledWith(
        'test-collection',
        expect.objectContaining({
          vectors: expect.objectContaining({
            size: 384,
            distance: 'Cosine',
          }),
        })
      );
    });

    it('should use HNSW index configuration', async () => {
      mockQdrantClient.getCollections.mockResolvedValue({
        collections: [],
      });
      mockQdrantClient.createCollection.mockResolvedValue({});

      await client.initialize();

      expect(mockQdrantClient.createCollection).toHaveBeenCalledWith(
        'test-collection',
        expect.objectContaining({
          hnsw_config: expect.objectContaining({
            m: 16,
            ef_construct: 128,
          }),
        })
      );
    });

    it('should use scalar quantization for memory optimization', async () => {
      mockQdrantClient.getCollections.mockResolvedValue({
        collections: [],
      });
      mockQdrantClient.createCollection.mockResolvedValue({});

      await client.initialize();

      expect(mockQdrantClient.createCollection).toHaveBeenCalledWith(
        'test-collection',
        expect.objectContaining({
          quantization_config: expect.objectContaining({
            scalar: expect.objectContaining({
              type: 'int8',
            }),
          }),
        })
      );
    });

    it('should handle initialization errors', async () => {
      mockQdrantClient.getCollections.mockRejectedValue(
        new Error('Connection failed')
      );

      await expect(client.initialize()).rejects.toThrow(
        'Failed to initialize Qdrant collection'
      );
    });

    it('should skip initialization if already initialized', async () => {
      mockQdrantClient.getCollections.mockResolvedValue({
        collections: [{ name: 'test-collection' }],
      });

      await client.initialize();
      await client.initialize(); // Second call

      // Should only call once
      expect(mockQdrantClient.getCollections).toHaveBeenCalledTimes(1);
    });
  });

  describe('Point Storage', () => {
    beforeEach(async () => {
      mockQdrantClient.getCollections.mockResolvedValue({
        collections: [{ name: 'test-collection' }],
      });
      await client.initialize();
    });

    it('should store single point', async () => {
      const point: AgentPoint = {
        id: 'test-id',
        vector: global.testUtils.createMockEmbedding(),
        payload: global.testUtils.createMockSearchResult().payload,
      };

      mockQdrantClient.upsert.mockResolvedValue({});

      await client.storePoint(point);

      expect(mockQdrantClient.upsert).toHaveBeenCalledWith(
        'test-collection',
        expect.objectContaining({
          wait: true,
          points: expect.arrayContaining([
            expect.objectContaining({
              id: 'test-id',
              vector: point.vector,
            }),
          ]),
        })
      );
    });

    it('should handle storage errors', async () => {
      const point: AgentPoint = {
        id: 'test-id',
        vector: global.testUtils.createMockEmbedding(),
        payload: global.testUtils.createMockSearchResult().payload,
      };

      mockQdrantClient.upsert.mockRejectedValue(new Error('Storage failed'));

      await expect(client.storePoint(point)).rejects.toThrow('Failed to store point');
    });
  });

  describe('Batch Operations', () => {
    beforeEach(async () => {
      mockQdrantClient.getCollections.mockResolvedValue({
        collections: [{ name: 'test-collection' }],
      });
      await client.initialize();
    });

    it('should store multiple points in batch', async () => {
      const points: AgentPoint[] = Array.from({ length: 5 }, (_, i) => ({
        id: `point-${i}`,
        vector: global.testUtils.createMockEmbedding(),
        payload: global.testUtils.createMockSearchResult().payload,
      }));

      mockQdrantClient.upsert.mockResolvedValue({});

      const result = await client.storeBatch(points);

      expect(result.successful.length).toBe(5);
      expect(result.failed.length).toBe(0);
      expect(result.success_rate).toBe(1.0);
    });

    it('should handle partial batch failures', async () => {
      const points: AgentPoint[] = Array.from({ length: 3 }, (_, i) => ({
        id: `point-${i}`,
        vector: global.testUtils.createMockEmbedding(),
        payload: global.testUtils.createMockSearchResult().payload,
      }));

      // Batch fails, then individual inserts
      mockQdrantClient.upsert
        .mockRejectedValueOnce(new Error('Batch failed'))
        .mockResolvedValueOnce({}) // point-0
        .mockRejectedValueOnce(new Error('Failed')) // point-1
        .mockResolvedValueOnce({}); // point-2

      const result = await client.storeBatch(points);

      expect(result.successful.length).toBe(2);
      expect(result.failed.length).toBe(1);
      expect(result.success_rate).toBeCloseTo(2/3, 2);
    });
  });

  describe('Similarity Search', () => {
    beforeEach(async () => {
      mockQdrantClient.getCollections.mockResolvedValue({
        collections: [{ name: 'test-collection' }],
      });
      await client.initialize();
    });

    it('should search with default parameters', async () => {
      const vector = global.testUtils.createMockEmbedding();
      mockQdrantClient.search.mockResolvedValue([
        {
          id: 'result-1',
          score: 0.95,
          payload: global.testUtils.createMockSearchResult().payload,
        },
      ]);

      const results = await client.search(vector);

      expect(mockQdrantClient.search).toHaveBeenCalledWith(
        'test-collection',
        expect.objectContaining({
          vector,
          limit: 5,
          score_threshold: 0.9,
        })
      );
      expect(results.length).toBe(1);
      expect(results[0].score).toBe(0.95);
    });

    it('should search with custom parameters', async () => {
      const vector = global.testUtils.createMockEmbedding();
      mockQdrantClient.search.mockResolvedValue([]);

      await client.search(vector, {
        limit: 10,
        scoreThreshold: 0.95,
        hnsw_ef: 256,
      });

      expect(mockQdrantClient.search).toHaveBeenCalledWith(
        'test-collection',
        expect.objectContaining({
          limit: 10,
          score_threshold: 0.95,
          params: expect.objectContaining({
            hnsw_ef: 256,
          }),
        })
      );
    });

    it('should search with filters', async () => {
      const vector = global.testUtils.createMockEmbedding();
      const filter: SearchFilter = {
        must: [{ key: 'agent_type', match: { value: 'researcher' } }],
      };

      mockQdrantClient.search.mockResolvedValue([]);

      await client.search(vector, { filter });

      expect(mockQdrantClient.search).toHaveBeenCalledWith(
        'test-collection',
        expect.objectContaining({
          filter,
        })
      );
    });

    it('should handle search errors gracefully', async () => {
      const vector = global.testUtils.createMockEmbedding();
      mockQdrantClient.search.mockRejectedValue(new Error('Search failed'));

      const results = await client.search(vector);

      // Should return empty array instead of throwing
      expect(results).toEqual([]);
    });

    it('should return results sorted by score', async () => {
      const vector = global.testUtils.createMockEmbedding();
      mockQdrantClient.search.mockResolvedValue([
        { id: '1', score: 0.95, payload: {} },
        { id: '2', score: 0.98, payload: {} },
        { id: '3', score: 0.92, payload: {} },
      ]);

      const results = await client.search(vector);

      expect(results[0].score).toBe(0.95);
      expect(results[1].score).toBe(0.98);
      expect(results[2].score).toBe(0.92);
    });
  });

  describe('Point Retrieval', () => {
    beforeEach(async () => {
      mockQdrantClient.getCollections.mockResolvedValue({
        collections: [{ name: 'test-collection' }],
      });
      await client.initialize();
    });

    it('should retrieve point by ID', async () => {
      const mockPoint = {
        id: 'test-id',
        vector: global.testUtils.createMockEmbedding(),
        payload: global.testUtils.createMockSearchResult().payload,
      };

      mockQdrantClient.retrieve.mockResolvedValue([mockPoint]);

      const result = await client.getPoint('test-id');

      expect(result).toBeDefined();
      expect(result?.id).toBe('test-id');
    });

    it('should return null for non-existent point', async () => {
      mockQdrantClient.retrieve.mockResolvedValue([]);

      const result = await client.getPoint('non-existent');

      expect(result).toBeNull();
    });

    it('should handle retrieval errors', async () => {
      mockQdrantClient.retrieve.mockRejectedValue(new Error('Retrieval failed'));

      const result = await client.getPoint('test-id');

      expect(result).toBeNull();
    });
  });

  describe('Access Metrics Update', () => {
    beforeEach(async () => {
      mockQdrantClient.getCollections.mockResolvedValue({
        collections: [{ name: 'test-collection' }],
      });
      await client.initialize();
    });

    it('should update access metrics', async () => {
      mockQdrantClient.setPayload.mockResolvedValue({});

      await client.updateAccessMetrics('test-id', {
        last_accessed: Date.now(),
        access_count: 5,
        total_spawns: 10,
      });

      expect(mockQdrantClient.setPayload).toHaveBeenCalledWith(
        'test-collection',
        expect.objectContaining({
          points: ['test-id'],
          wait: false,
        })
      );
    });

    it('should handle update errors gracefully', async () => {
      mockQdrantClient.setPayload.mockRejectedValue(new Error('Update failed'));

      // Should not throw
      await expect(
        client.updateAccessMetrics('test-id', { access_count: 5 })
      ).resolves.toBeUndefined();
    });
  });

  describe('Point Deletion', () => {
    beforeEach(async () => {
      mockQdrantClient.getCollections.mockResolvedValue({
        collections: [{ name: 'test-collection' }],
      });
      await client.initialize();
    });

    it('should delete points by IDs', async () => {
      mockQdrantClient.delete.mockResolvedValue({});

      await client.deletePoints(['id-1', 'id-2', 'id-3']);

      expect(mockQdrantClient.delete).toHaveBeenCalledWith(
        'test-collection',
        expect.objectContaining({
          points: ['id-1', 'id-2', 'id-3'],
          wait: true,
        })
      );
    });

    it('should delete points by filter', async () => {
      const filter: SearchFilter = {
        must: [{ key: 'agent_type', match: { value: 'deprecated' } }],
      };

      mockQdrantClient.delete.mockResolvedValue({});

      await client.deleteByFilter(filter);

      expect(mockQdrantClient.delete).toHaveBeenCalledWith(
        'test-collection',
        expect.objectContaining({
          filter,
          wait: true,
        })
      );
    });

    it('should handle deletion errors', async () => {
      mockQdrantClient.delete.mockRejectedValue(new Error('Delete failed'));

      await expect(client.deletePoints(['id-1'])).rejects.toThrow(
        'Failed to delete points'
      );
    });
  });

  describe('Collection Management', () => {
    beforeEach(async () => {
      mockQdrantClient.getCollections.mockResolvedValue({
        collections: [{ name: 'test-collection' }],
      });
      await client.initialize();
    });

    it('should get collection info', async () => {
      mockQdrantClient.getCollection.mockResolvedValue({
        vectors_count: 1000,
        points_count: 1000,
        status: 'green',
        config: {},
      });

      const info = await client.getCollectionInfo();

      expect(info).toBeDefined();
      expect(info?.vectors_count).toBe(1000);
      expect(info?.status).toBe('green');
    });

    it('should handle collection info errors', async () => {
      mockQdrantClient.getCollection.mockRejectedValue(new Error('Info failed'));

      const info = await client.getCollectionInfo();

      expect(info).toBeNull();
    });

    it('should clear collection', async () => {
      mockQdrantClient.deleteCollection.mockResolvedValue({});
      mockQdrantClient.createCollection.mockResolvedValue({});

      await client.clearCollection();

      expect(mockQdrantClient.deleteCollection).toHaveBeenCalledWith('test-collection');
      expect(mockQdrantClient.createCollection).toHaveBeenCalled();
    });

    it('should handle clear errors', async () => {
      mockQdrantClient.deleteCollection.mockRejectedValue(
        new Error('Clear failed')
      );

      await expect(client.clearCollection()).rejects.toThrow(
        'Failed to clear collection'
      );
    });
  });

  describe('Connection Failures', () => {
    it('should handle connection timeout', async () => {
      mockQdrantClient.getCollections.mockImplementation(() =>
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Timeout')), 100)
        )
      );

      await expect(client.initialize()).rejects.toThrow(
        'Failed to initialize Qdrant collection'
      );
    });

    it('should handle authentication errors', async () => {
      mockQdrantClient.getCollections.mockRejectedValue(
        new Error('401 Unauthorized')
      );

      await expect(client.initialize()).rejects.toThrow(
        'Failed to initialize Qdrant collection'
      );
    });

    it('should handle network errors', async () => {
      mockQdrantClient.search.mockRejectedValue(
        new Error('ECONNREFUSED')
      );

      const vector = global.testUtils.createMockEmbedding();
      await client.initialize();

      const results = await client.search(vector);
      expect(results).toEqual([]);
    });
  });

  describe('Resource Cleanup', () => {
    it('should destroy client resources', async () => {
      await client.destroy();

      // After destroy, should be able to reinitialize
      mockQdrantClient.getCollections.mockResolvedValue({
        collections: [{ name: 'test-collection' }],
      });

      await client.initialize();
      expect(mockQdrantClient.getCollections).toHaveBeenCalled();
    });
  });
});
