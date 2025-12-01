/**
 * Embedding Service
 * Generates semantic embeddings for agent configurations using @xenova/transformers
 */

import { pipeline, Pipeline, FeatureExtractionPipeline } from '@xenova/transformers';
import { LRUCache } from 'lru-cache';
import { createHash } from 'crypto';
import { AgentConfig, EmbeddingResult } from './types';

export class EmbeddingService {
  private model: FeatureExtractionPipeline | null = null;
  private cache: LRUCache<string, number[]>;
  private initPromise: Promise<void> | null = null;
  private readonly modelName = 'Xenova/all-MiniLM-L6-v2';
  private readonly dimension = 384;

  constructor(
    private options: {
      cacheSize?: number;
      cacheTTL?: number;
      enableLogging?: boolean;
    } = {}
  ) {
    // Initialize L1 embedding cache
    this.cache = new LRUCache({
      max: options.cacheSize || 10000,
      maxSize: (options.cacheSize || 10000) * this.dimension * 4, // 4 bytes per float
      ttl: options.cacheTTL || 1000 * 60 * 60, // 1 hour default
      sizeCalculation: () => this.dimension * 4,
    });
  }

  /**
   * Initialize the embedding model
   */
  async initialize(): Promise<void> {
    if (this.model) return;
    if (this.initPromise) return this.initPromise;

    this.initPromise = (async () => {
      try {
        this.log('Initializing embedding model:', this.modelName);
        const startTime = Date.now();

        this.model = (await pipeline(
          'feature-extraction',
          this.modelName,
          {
            quantized: true, // Use quantized version for speed
            // @ts-ignore - device option exists but not in types
            device: 'auto', // Auto-select GPU/CPU
            // @ts-ignore - dtype option exists but not in types
            dtype: 'q8', // 8-bit quantization
          }
        )) as FeatureExtractionPipeline;

        const loadTime = Date.now() - startTime;
        this.log(`Model loaded in ${loadTime}ms`);
      } catch (error) {
        this.log('Error loading model:', error);
        throw new Error(`Failed to initialize embedding model: ${error}`);
      }
    })();

    return this.initPromise;
  }

  /**
   * Generate embedding for agent configuration
   */
  async generateEmbedding(
    config: AgentConfig,
    bypassCache = false
  ): Promise<EmbeddingResult> {
    const startTime = Date.now();

    // Ensure model is initialized
    if (!this.model) {
      await this.initialize();
    }

    // Serialize config to text
    const configText = this.serializeConfig(config);
    const cacheKey = this.hashText(configText);

    // Check cache
    if (!bypassCache && this.cache.has(cacheKey)) {
      const embedding = this.cache.get(cacheKey)!;
      return {
        embedding,
        cached: true,
        generation_time_ms: Date.now() - startTime,
      };
    }

    // Generate embedding
    try {
      // Validate model is available
      if (!this.model) {
        throw new Error('Model is null or undefined');
      }

      // The pipeline function is callable - invoke it directly
      const output = await (this.model as any)(configText, {
        pooling: 'mean',
        normalize: true,
      });

      // Extract embedding vector
      const embedding = Array.from(output.data as Float32Array);

      // Validate dimension
      if (embedding.length !== this.dimension) {
        throw new Error(
          `Invalid embedding dimension: expected ${this.dimension}, got ${embedding.length}`
        );
      }

      // Cache result
      this.cache.set(cacheKey, embedding);

      return {
        embedding,
        cached: false,
        generation_time_ms: Date.now() - startTime,
      };
    } catch (error) {
      throw new Error(`Embedding generation failed: ${error}`);
    }
  }

  /**
   * Generate embeddings in batch
   */
  async generateBatchEmbeddings(
    configs: AgentConfig[],
    batchSize = 32
  ): Promise<EmbeddingResult[]> {
    const results: EmbeddingResult[] = [];

    // Process in batches
    for (let i = 0; i < configs.length; i += batchSize) {
      const batch = configs.slice(i, i + batchSize);

      // Process batch in parallel
      const batchResults = await Promise.all(
        batch.map((config) => this.generateEmbedding(config))
      );

      results.push(...batchResults);
    }

    return results;
  }

  /**
   * Serialize agent config to optimized text representation
   */
  private serializeConfig(config: AgentConfig): string {
    const components = [
      `Type: ${config.agent_type}`,
      `Name: ${config.agent_name}`,
      `Capabilities: ${config.capabilities.join(', ')}`,
    ];

    if (config.specialization) {
      components.push(`Specialization: ${config.specialization}`);
    }

    if (config.runtime) {
      components.push(`Runtime: ${config.runtime}`);
    }

    if (config.context) {
      components.push(`Context: ${config.context}`);
    }

    if (config.project_context) {
      components.push(`Project: ${config.project_context}`);
    }

    // Exclude frequently changing fields (timestamps, IDs, etc.)
    // to improve semantic matching

    return components.join('\n');
  }

  /**
   * Hash text for cache key
   */
  private hashText(text: string): string {
    return createHash('sha256').update(text).digest('hex');
  }

  /**
   * Get cache statistics
   */
  getCacheStats() {
    return {
      size: this.cache.size,
      max: this.cache.max,
      hit_rate: this.calculateHitRate(),
    };
  }

  /**
   * Clear embedding cache
   */
  clearCache(): void {
    this.cache.clear();
  }

  /**
   * Calculate cache hit rate
   */
  private calculateHitRate(): number {
    // This is approximate - LRUCache doesn't track hits/misses directly
    return this.cache.size / (this.cache.max || 1);
  }

  /**
   * Log helper
   */
  private log(...args: any[]): void {
    if (this.options.enableLogging) {
      console.log('[EmbeddingService]', ...args);
    }
  }

  /**
   * Cleanup resources
   */
  async destroy(): Promise<void> {
    this.cache.clear();
    this.model = null;
    this.initPromise = null;
  }
}
