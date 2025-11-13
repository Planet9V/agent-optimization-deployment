/**
 * Qdrant Client
 * Handles Qdrant vector database operations for AgentDB
 */

import { QdrantClient } from '@qdrant/js-client-rest';
import { AgentPoint, SearchResult, SearchFilter, BatchResult } from './types';

export class AgentDBQdrantClient {
  private client: QdrantClient;
  private collectionName: string;
  private dimension: number;
  private initialized = false;

  constructor(
    private options: {
      url?: string;
      apiKey?: string;
      collectionName?: string;
      dimension?: number;
      enableLogging?: boolean;
    } = {}
  ) {
    this.collectionName = options.collectionName || 'agent-cache';
    this.dimension = options.dimension || 384;

    // Initialize Qdrant client
    this.client = new QdrantClient({
      url: options.url || process.env.QDRANT_URL || 'http://localhost:6333',
      apiKey: options.apiKey || process.env.QDRANT_API_KEY,
    });
  }

  /**
   * Initialize collection if it doesn't exist
   */
  async initialize(): Promise<void> {
    if (this.initialized) return;

    try {
      this.log('Checking if collection exists:', this.collectionName);

      // Check if collection exists
      const collections = await this.client.getCollections();
      const exists = collections.collections.some(
        (c) => c.name === this.collectionName
      );

      if (!exists) {
        this.log('Creating collection:', this.collectionName);
        await this.createCollection();
      } else {
        this.log('Collection already exists:', this.collectionName);
      }

      this.initialized = true;
    } catch (error) {
      throw new Error(`Failed to initialize Qdrant collection: ${error}`);
    }
  }

  /**
   * Create collection with optimal configuration
   */
  private async createCollection(): Promise<void> {
    await this.client.createCollection(this.collectionName, {
      vectors: {
        size: this.dimension,
        distance: 'Cosine',
        on_disk: false, // Keep in RAM for speed
      },
      // HNSW index configuration
      hnsw_config: {
        m: 16, // Graph density (balanced)
        ef_construct: 128, // Build quality (high precision)
        full_scan_threshold: 10000,
        max_indexing_threads: 0, // Use all available
      },
      // Optimizer configuration
      optimizers_config: {
        deleted_threshold: 0.2,
        vacuum_min_vector_number: 1000,
        default_segment_number: 2,
        max_segment_size: 200000,
        memmap_threshold: 50000,
        indexing_threshold: 20000,
        flush_interval_sec: 5,
        max_optimization_threads: 1,
      },
      // Optional: Scalar quantization for memory reduction
      quantization_config: {
        scalar: {
          type: 'int8',
          quantile: 0.99,
          always_ram: true,
        },
      },
    });

    this.log('Collection created successfully');
  }

  /**
   * Store agent point in Qdrant
   */
  async storePoint(point: AgentPoint): Promise<void> {
    await this.ensureInitialized();

    try {
      await this.client.upsert(this.collectionName, {
        wait: true,
        points: [
          {
            id: point.id,
            vector: point.vector,
            payload: point.payload as any,
          },
        ],
      });

      this.log('Point stored:', point.id);
    } catch (error) {
      throw new Error(`Failed to store point: ${error}`);
    }
  }

  /**
   * Store multiple points in batch
   */
  async storeBatch(points: AgentPoint[]): Promise<BatchResult<AgentPoint>> {
    await this.ensureInitialized();

    const successful: AgentPoint[] = [];
    const failed: Array<{ item: AgentPoint; error: Error }> = [];

    try {
      await this.client.upsert(this.collectionName, {
        wait: true,
        points: points.map((point) => ({
          id: point.id,
          vector: point.vector,
          payload: point.payload as any,
        })),
      });

      successful.push(...points);
    } catch (error) {
      // If batch fails, try individual inserts
      for (const point of points) {
        try {
          await this.storePoint(point);
          successful.push(point);
        } catch (err) {
          failed.push({ item: point, error: err as Error });
        }
      }
    }

    return {
      successful,
      failed,
      total: points.length,
      success_rate: successful.length / points.length,
    };
  }

  /**
   * Search for similar agents
   */
  async search(
    vector: number[],
    options: {
      limit?: number;
      scoreThreshold?: number;
      filter?: SearchFilter;
      hnsw_ef?: number;
    } = {}
  ): Promise<SearchResult[]> {
    await this.ensureInitialized();

    try {
      const results = await this.client.search(this.collectionName, {
        vector,
        limit: options.limit || 5,
        score_threshold: options.scoreThreshold || 0.9,
        with_payload: true,
        with_vector: false,
        filter: options.filter as any,
        params: {
          hnsw_ef: options.hnsw_ef || 128,
          exact: false,
        },
      });

      return results.map((result) => ({
        id: result.id as string,
        score: result.score,
        payload: result.payload as any,
      }));
    } catch (error) {
      // Graceful degradation on error
      this.log('Search error:', error);
      return [];
    }
  }

  /**
   * Retrieve point by ID
   */
  async getPoint(id: string): Promise<AgentPoint | null> {
    await this.ensureInitialized();

    try {
      const points = await this.client.retrieve(this.collectionName, {
        ids: [id],
        with_payload: true,
        with_vector: true,
      });

      if (points.length === 0) return null;

      const point = points[0];
      return {
        id: point.id as string,
        vector: point.vector as number[],
        payload: point.payload as any,
      };
    } catch (error) {
      this.log('Error retrieving point:', error);
      return null;
    }
  }

  /**
   * Update access metrics for a point
   */
  async updateAccessMetrics(
    id: string,
    updates: {
      last_accessed?: number;
      access_count?: number;
      total_spawns?: number;
    }
  ): Promise<void> {
    await this.ensureInitialized();

    try {
      await this.client.setPayload(this.collectionName, {
        points: [id],
        payload: updates as any,
        wait: false, // Don't wait for consistency
      });
    } catch (error) {
      this.log('Error updating metrics:', error);
      // Non-critical operation, don't throw
    }
  }

  /**
   * Delete points by IDs
   */
  async deletePoints(ids: string[]): Promise<void> {
    await this.ensureInitialized();

    try {
      await this.client.delete(this.collectionName, {
        points: ids,
        wait: true,
      });

      this.log('Deleted points:', ids.length);
    } catch (error) {
      throw new Error(`Failed to delete points: ${error}`);
    }
  }

  /**
   * Delete points matching filter
   */
  async deleteByFilter(filter: SearchFilter): Promise<void> {
    await this.ensureInitialized();

    try {
      await this.client.delete(this.collectionName, {
        filter: filter as any,
        wait: true,
      });

      this.log('Deleted points by filter');
    } catch (error) {
      throw new Error(`Failed to delete by filter: ${error}`);
    }
  }

  /**
   * Get collection info
   */
  async getCollectionInfo() {
    await this.ensureInitialized();

    try {
      const info = await this.client.getCollection(this.collectionName);
      return {
        vectors_count: info.vectors_count || 0,
        points_count: info.points_count || 0,
        status: info.status,
        config: info.config,
      };
    } catch (error) {
      this.log('Error getting collection info:', error);
      return null;
    }
  }

  /**
   * Clear all points from collection
   */
  async clearCollection(): Promise<void> {
    await this.ensureInitialized();

    try {
      await this.client.deleteCollection(this.collectionName);
      await this.createCollection();
      this.log('Collection cleared');
    } catch (error) {
      throw new Error(`Failed to clear collection: ${error}`);
    }
  }

  /**
   * Ensure client is initialized
   */
  private async ensureInitialized(): Promise<void> {
    if (!this.initialized) {
      await this.initialize();
    }
  }

  /**
   * Log helper
   */
  private log(...args: any[]): void {
    if (this.options.enableLogging) {
      console.log('[QdrantClient]', ...args);
    }
  }

  /**
   * Cleanup resources
   */
  async destroy(): Promise<void> {
    // Qdrant client doesn't need explicit cleanup
    this.initialized = false;
  }
}
