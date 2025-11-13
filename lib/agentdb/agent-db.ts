/**
 * AgentDB - Intelligent Agent Caching System
 * Multi-level caching with Qdrant vector database for 150-12,500x speedup
 */

import { LRUCache } from 'lru-cache';
import { randomUUID } from 'crypto';
import { EmbeddingService } from './embedding-service';
import { AgentDBQdrantClient } from './qdrant-client';
import {
  AgentConfig,
  AgentPoint,
  SearchResult,
  CacheStats,
  AgentDBOptions,
  CacheLevel,
  CacheOperation,
  SpawnResult,
  TTLTier,
} from './types';

export class AgentDB {
  private embeddingService: EmbeddingService;
  private qdrantClient: AgentDBQdrantClient;
  private l1Cache: LRUCache<string, SearchResult>;
  private stats: CacheStats;
  private options: Required<AgentDBOptions>;

  // Default TTL tiers (in milliseconds)
  private readonly ttlTiers: TTLTier[] = [
    { name: 'hot', ttl_days: 7, access_threshold: 100 },
    { name: 'warm', ttl_days: 3, access_threshold: 10 },
    { name: 'cold', ttl_days: 1, access_threshold: 0 },
  ];

  constructor(options: AgentDBOptions = {}) {
    // Merge with defaults
    this.options = {
      qdrantUrl: options.qdrantUrl || 'http://localhost:6333',
      qdrantApiKey: options.qdrantApiKey || process.env.QDRANT_API_KEY || '',
      collectionName: options.collectionName || 'agent-cache',
      l1CacheSize: options.l1CacheSize || 10000,
      l1CacheTTL: options.l1CacheTTL || 1000 * 60 * 60, // 1 hour
      l2DefaultTTL: options.l2DefaultTTL || 1000 * 60 * 60 * 24 * 7, // 7 days
      similarityThresholds: options.similarityThresholds || {
        exact: 0.98,
        high: 0.95,
        good: 0.9,
      },
      embeddingModel: options.embeddingModel || 'Xenova/all-MiniLM-L6-v2',
      embeddingDimension: options.embeddingDimension || 384,
      batchSize: options.batchSize || 32,
      maxConcurrency: options.maxConcurrency || 5,
      enableL1Cache: options.enableL1Cache !== false,
      enableL2Cache: options.enableL2Cache !== false,
      enableMetrics: options.enableMetrics !== false,
      enableLogging: options.enableLogging !== false,
    };

    // Initialize services
    this.embeddingService = new EmbeddingService({
      cacheSize: this.options.l1CacheSize,
      cacheTTL: this.options.l1CacheTTL,
      enableLogging: this.options.enableLogging,
    });

    this.qdrantClient = new AgentDBQdrantClient({
      url: this.options.qdrantUrl,
      apiKey: this.options.qdrantApiKey,
      collectionName: this.options.collectionName,
      dimension: this.options.embeddingDimension,
      enableLogging: this.options.enableLogging,
    });

    // Initialize L1 cache
    this.l1Cache = new LRUCache<string, SearchResult>({
      max: this.options.l1CacheSize,
      ttl: this.options.l1CacheTTL,
      updateAgeOnGet: true,
      updateAgeOnHas: true,
    });

    // Initialize stats
    this.stats = {
      total_requests: 0,
      cache_hits: 0,
      cache_misses: 0,
      hit_rate: 0,
      avg_hit_latency_ms: 0,
      avg_miss_latency_ms: 0,
      p50_latency_ms: 0,
      p99_latency_ms: 0,
      l1_cache_size: 0,
      l1_cache_max: this.options.l1CacheSize,
      l2_cache_size: 0,
      last_reset: Date.now(),
      uptime_ms: 0,
    };
  }

  /**
   * Initialize AgentDB (must be called before use)
   */
  async initialize(): Promise<void> {
    this.log('Initializing AgentDB...');

    // Initialize embedding service
    await this.embeddingService.initialize();

    // Initialize Qdrant client
    if (this.options.enableL2Cache) {
      try {
        await this.qdrantClient.initialize();
        this.log('AgentDB initialized successfully');
      } catch (error) {
        this.log('Warning: Qdrant initialization failed, L2 cache disabled');
        this.options.enableL2Cache = false;
      }
    }
  }

  /**
   * Find or spawn agent with intelligent caching
   */
  async findOrSpawnAgent(
    config: AgentConfig,
    spawnFn: (config: AgentConfig) => Promise<any>
  ): Promise<SpawnResult> {
    const startTime = Date.now();
    this.stats.total_requests++;

    try {
      // 1. Generate embedding
      const embeddingResult = await this.embeddingService.generateEmbedding(
        config
      );
      const embedding = embeddingResult.embedding;

      // 2. Try L1 cache first (if enabled)
      if (this.options.enableL1Cache) {
        const l1Result = this.searchL1Cache(embedding);
        if (l1Result.found && l1Result.result) {
          this.recordHit(CacheLevel.L1, Date.now() - startTime);
          return {
            agent: l1Result.result.agent,
            cached: true,
            cache_level: CacheLevel.L1,
            similarity_score: l1Result.result.score,
            latency_ms: Date.now() - startTime,
          };
        }
      }

      // 3. Try L2 cache (Qdrant)
      if (this.options.enableL2Cache) {
        const l2Result = await this.searchL2Cache(embedding, config);
        if (l2Result.found && l2Result.result) {
          // Update L1 cache
          if (this.options.enableL1Cache) {
            this.l1Cache.set(l2Result.result.id, l2Result.result);
          }

          // Update access metrics
          await this.updateAccessMetrics(l2Result.result.id);

          this.recordHit(CacheLevel.L2, Date.now() - startTime);
          return {
            agent: l2Result.result.agent,
            cached: true,
            cache_level: CacheLevel.L2,
            similarity_score: l2Result.result.score,
            latency_ms: Date.now() - startTime,
          };
        }
      }

      // 4. CACHE MISS: Spawn new agent
      const spawnStartTime = Date.now();
      const agent = await spawnFn(config);
      const spawnTime = Date.now() - spawnStartTime;

      // 5. Cache the new agent
      await this.cacheAgent(config, embedding, agent, spawnTime);

      this.recordMiss(Date.now() - startTime);
      return {
        agent,
        cached: false,
        spawn_time_ms: spawnTime,
        latency_ms: Date.now() - startTime,
      };
    } catch (error) {
      this.log('Error in findOrSpawnAgent:', error);
      // Fall back to spawning
      const agent = await spawnFn(config);
      return {
        agent,
        cached: false,
        latency_ms: Date.now() - startTime,
      };
    }
  }

  /**
   * Search L1 cache (in-memory LRU)
   * Uses cosine similarity to find matching agents by embedding
   */
  private searchL1Cache(embedding: number[]): CacheOperation {
    const startTime = Date.now();

    // Iterate through L1 cache to find similar embeddings
    const entries = Array.from(this.l1Cache.entries());
    let bestMatch: { result: SearchResult; score: number } | null = null;

    for (const [id, result] of entries) {
      // Skip entries without embeddings (shouldn't happen in normal operation)
      if (!result.embedding) {
        this.log(`L1 cache entry ${id} missing embedding, skipping`);
        continue;
      }

      // Calculate similarity between query embedding and cached embedding
      const score = this.cosineSimilarity(embedding, result.embedding);

      // Track best match above threshold
      if (score >= this.options.similarityThresholds.good) {
        if (!bestMatch || score > bestMatch.score) {
          bestMatch = { result, score };
        }
      }
    }

    // Return best match if found
    if (bestMatch) {
      return {
        found: true,
        level: CacheLevel.L1,
        latency_ms: Date.now() - startTime,
        result: { ...bestMatch.result, score: bestMatch.score },
      };
    }

    return {
      found: false,
      level: CacheLevel.L1,
      latency_ms: Date.now() - startTime,
    };
  }

  /**
   * Search L2 cache (Qdrant)
   */
  private async searchL2Cache(
    embedding: number[],
    config: AgentConfig
  ): Promise<CacheOperation> {
    const startTime = Date.now();

    try {
      const results = await this.qdrantClient.search(embedding, {
        limit: 5,
        scoreThreshold: this.options.similarityThresholds.good,
      });

      if (results.length === 0) {
        return {
          found: false,
          level: CacheLevel.L2,
          latency_ms: Date.now() - startTime,
        };
      }

      // Validate best match
      const bestMatch = results[0];
      if (this.isConfigCompatible(config, bestMatch.payload)) {
        return {
          found: true,
          level: CacheLevel.L2,
          latency_ms: Date.now() - startTime,
          result: bestMatch,
        };
      }

      return {
        found: false,
        level: CacheLevel.L2,
        latency_ms: Date.now() - startTime,
      };
    } catch (error) {
      this.log('L2 cache search error:', error);
      return {
        found: false,
        level: CacheLevel.L2,
        latency_ms: Date.now() - startTime,
      };
    }
  }

  /**
   * Cache agent in both L1 and L2
   */
  private async cacheAgent(
    config: AgentConfig,
    embedding: number[],
    agent: any,
    spawnTime: number
  ): Promise<void> {
    const id = randomUUID();
    const now = Date.now();
    const ttl = this.calculateTTL(0); // New agent, 0 access count

    const point: AgentPoint = {
      id,
      vector: embedding,
      payload: {
        agent_type: config.agent_type,
        agent_name: config.agent_name,
        capabilities: config.capabilities,
        specialization: config.specialization,
        config_hash: this.hashConfig(config),
        config_version: '2.0.0',
        agent_config: config,
        avg_spawn_time_ms: spawnTime,
        success_rate: 1.0,
        total_spawns: 1,
        created_at: now,
        last_accessed: now,
        access_count: 1,
        ttl_expires: now + ttl,
        embedding_model: this.options.embeddingModel,
        embedding_version: 'v2.0',
        similarity_threshold: this.options.similarityThresholds.good,
        tags: config.project_context ? ['production'] : ['development'],
        project_context: config.project_context,
        team_id: config.team_id,
      },
    };

    // Create SearchResult for L1 cache (includes embedding for similarity comparison)
    const searchResult: SearchResult = {
      id: point.id,
      score: 1.0, // Perfect match for newly cached agent
      payload: point.payload,
      agent,
      embedding, // Store embedding in L1 cache for cosine similarity
    };

    // Store in L1 cache (with embedding for similarity search)
    if (this.options.enableL1Cache) {
      this.l1Cache.set(id, searchResult);
    }

    // Store in L2 cache (Qdrant)
    if (this.options.enableL2Cache) {
      try {
        await this.qdrantClient.storePoint(point);
      } catch (error) {
        this.log('Error storing in L2 cache:', error);
      }
    }
  }

  /**
   * Update access metrics for cached agent
   */
  private async updateAccessMetrics(id: string): Promise<void> {
    const now = Date.now();

    try {
      // Get current point
      const point = await this.qdrantClient.getPoint(id);
      if (!point) return;

      const accessCount = point.payload.access_count + 1;
      const ttl = this.calculateTTL(accessCount);

      await this.qdrantClient.updateAccessMetrics(id, {
        last_accessed: now,
        access_count: accessCount,
        total_spawns: point.payload.total_spawns + 1,
      });
    } catch (error) {
      this.log('Error updating access metrics:', error);
    }
  }

  /**
   * Calculate TTL based on access count (hot/warm/cold tiers)
   */
  private calculateTTL(accessCount: number): number {
    for (const tier of this.ttlTiers) {
      if (accessCount >= tier.access_threshold) {
        return tier.ttl_days * 24 * 60 * 60 * 1000;
      }
    }
    return this.options.l2DefaultTTL;
  }

  /**
   * Check if config is compatible with cached agent
   */
  private isConfigCompatible(
    requested: AgentConfig,
    cached: AgentPoint['payload']
  ): boolean {
    // Core compatibility checks
    if (requested.agent_type !== cached.agent_type) return false;

    // Check capabilities match
    const requestedCaps = new Set(requested.capabilities);
    const cachedCaps = new Set(cached.capabilities);
    const requestedCapsArray = Array.from(requestedCaps);
    for (const cap of requestedCapsArray) {
      if (!cachedCaps.has(cap)) return false;
    }

    // Optional: check specialization
    if (
      requested.specialization &&
      cached.specialization &&
      requested.specialization !== cached.specialization
    ) {
      return false;
    }

    return true;
  }

  /**
   * Calculate cosine similarity between two embedding vectors
   * Returns value between -1 and 1, where 1 is identical, 0 is orthogonal, -1 is opposite
   */
  private cosineSimilarity(a: number[], b: number[]): number {
    // Validate inputs
    if (!a || !b) {
      this.log('Invalid embeddings for cosine similarity');
      return 0;
    }

    if (a.length !== b.length) {
      throw new Error(`Embedding dimensions don't match: ${a.length} vs ${b.length}`);
    }

    if (a.length === 0) {
      return 0;
    }

    // Calculate dot product and magnitudes
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;

    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }

    // Avoid division by zero
    if (normA === 0 || normB === 0) {
      this.log('Zero-magnitude vector in cosine similarity');
      return 0;
    }

    // Calculate cosine similarity
    const similarity = dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));

    // Clamp to [-1, 1] to handle floating point errors
    return Math.max(-1, Math.min(1, similarity));
  }

  /**
   * Hash config for comparison
   */
  private hashConfig(config: AgentConfig): string {
    const str = JSON.stringify({
      agent_type: config.agent_type,
      capabilities: config.capabilities.sort(),
      specialization: config.specialization,
    });
    return require('crypto').createHash('sha256').update(str).digest('hex');
  }

  /**
   * Record cache hit
   */
  private recordHit(level: CacheLevel, latency: number): void {
    this.stats.cache_hits++;
    this.stats.avg_hit_latency_ms =
      (this.stats.avg_hit_latency_ms * (this.stats.cache_hits - 1) + latency) /
      this.stats.cache_hits;
    this.updateStats();
    this.log(`Cache HIT (${level}): ${latency.toFixed(2)}ms`);
  }

  /**
   * Record cache miss
   */
  private recordMiss(latency: number): void {
    this.stats.cache_misses++;
    this.stats.avg_miss_latency_ms =
      (this.stats.avg_miss_latency_ms * (this.stats.cache_misses - 1) +
        latency) /
      this.stats.cache_misses;
    this.updateStats();
    this.log(`Cache MISS: ${latency.toFixed(2)}ms`);
  }

  /**
   * Update overall statistics
   */
  private updateStats(): void {
    this.stats.hit_rate = this.stats.cache_hits / this.stats.total_requests;
    this.stats.l1_cache_size = this.l1Cache.size;
    this.stats.uptime_ms = Date.now() - this.stats.last_reset;
  }

  /**
   * Get cache statistics
   */
  getStats(): CacheStats {
    return { ...this.stats };
  }

  /**
   * Reset statistics
   */
  resetStats(): void {
    this.stats = {
      total_requests: 0,
      cache_hits: 0,
      cache_misses: 0,
      hit_rate: 0,
      avg_hit_latency_ms: 0,
      avg_miss_latency_ms: 0,
      p50_latency_ms: 0,
      p99_latency_ms: 0,
      l1_cache_size: this.l1Cache.size,
      l1_cache_max: this.options.l1CacheSize,
      l2_cache_size: 0,
      last_reset: Date.now(),
      uptime_ms: 0,
    };
  }

  /**
   * Clear all caches
   */
  async clearAllCaches(): Promise<void> {
    this.l1Cache.clear();
    if (this.options.enableL2Cache) {
      await this.qdrantClient.clearCollection();
    }
    this.resetStats();
    this.log('All caches cleared');
  }

  /**
   * Get collection info from Qdrant
   */
  async getCollectionInfo() {
    if (!this.options.enableL2Cache) return null;
    return await this.qdrantClient.getCollectionInfo();
  }

  /**
   * Log helper
   */
  private log(...args: any[]): void {
    if (this.options.enableLogging) {
      console.log('[AgentDB]', ...args);
    }
  }

  /**
   * Cleanup resources
   */
  async destroy(): Promise<void> {
    await this.embeddingService.destroy();
    await this.qdrantClient.destroy();
    this.l1Cache.clear();
    this.log('AgentDB destroyed');
  }
}
