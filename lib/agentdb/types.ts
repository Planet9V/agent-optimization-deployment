/**
 * AgentDB Type Definitions
 * TypeScript interfaces for AgentDB with Qdrant integration
 */

/**
 * Agent configuration interface
 */
export interface AgentConfig {
  agent_type: string;
  agent_name: string;
  capabilities: string[];
  specialization?: string;
  runtime?: string;
  memory_limit?: string;
  timeout_ms?: number;
  env_vars?: Record<string, string>;
  dependencies?: string[];
  templates?: Record<string, any>;
  context?: string;
  project_context?: string;
  team_id?: string;
}

/**
 * Agent point stored in Qdrant
 */
export interface AgentPoint {
  id: string;
  vector: number[];
  payload: {
    // Core metadata
    agent_type: string;
    agent_name: string;
    capabilities: string[];
    specialization?: string;

    // Configuration
    config_hash: string;
    config_version: string;
    agent_config: AgentConfig;

    // Performance metadata
    avg_spawn_time_ms: number;
    success_rate: number;
    total_spawns: number;

    // Cache metadata
    created_at: number;
    last_accessed: number;
    access_count: number;
    ttl_expires: number;

    // Similarity matching
    embedding_model: string;
    embedding_version: string;
    similarity_threshold: number;

    // Analytics
    tags?: string[];
    project_context?: string;
    team_id?: string;
  };
}

/**
 * Search result from Qdrant or L1 cache
 */
export interface SearchResult {
  id: string;
  score: number;
  payload: AgentPoint['payload'];
  agent?: any; // Actual agent instance if retrieved
  embedding?: number[]; // Embedding vector for L1 cache similarity comparison
}

/**
 * Cache statistics
 */
export interface CacheStats {
  // Hit/miss tracking
  total_requests: number;
  cache_hits: number;
  cache_misses: number;
  hit_rate: number;

  // Performance metrics
  avg_hit_latency_ms: number;
  avg_miss_latency_ms: number;
  p50_latency_ms: number;
  p99_latency_ms: number;

  // Cache size
  l1_cache_size: number;
  l1_cache_max: number;
  l2_cache_size: number;

  // Time-based stats
  last_reset: number;
  uptime_ms: number;
}

/**
 * AgentDB configuration options
 */
export interface AgentDBOptions {
  // Qdrant connection
  qdrantUrl?: string;
  qdrantApiKey?: string;
  collectionName?: string;

  // Caching configuration
  l1CacheSize?: number;
  l1CacheTTL?: number;
  l2DefaultTTL?: number;

  // Similarity thresholds
  similarityThresholds?: {
    exact: number;
    high: number;
    good: number;
  };

  // Embedding configuration
  embeddingModel?: string;
  embeddingDimension?: number;

  // Performance tuning
  batchSize?: number;
  maxConcurrency?: number;

  // Feature flags
  enableL1Cache?: boolean;
  enableL2Cache?: boolean;
  enableMetrics?: boolean;
  enableLogging?: boolean;
}

/**
 * Embedding generation result
 */
export interface EmbeddingResult {
  embedding: number[];
  cached: boolean;
  generation_time_ms: number;
}

/**
 * Cache level enum
 */
export enum CacheLevel {
  L1 = 'L1',
  L2 = 'L2',
  MISS = 'MISS',
}

/**
 * Cache operation result
 */
export interface CacheOperation {
  found: boolean;
  level: CacheLevel;
  latency_ms: number;
  result?: SearchResult;
}

/**
 * Agent spawn result
 */
export interface SpawnResult {
  agent: any;
  cached: boolean;
  cache_level?: CacheLevel;
  similarity_score?: number;
  latency_ms: number;
  spawn_time_ms?: number;
}

/**
 * TTL tier configuration
 */
export interface TTLTier {
  name: 'hot' | 'warm' | 'cold';
  ttl_days: number;
  access_threshold: number;
}

/**
 * Eviction policy configuration
 */
export interface EvictionPolicy {
  enabled: boolean;
  max_collection_size: number;
  eviction_percentage: number;
  weights: {
    recency: number;
    frequency: number;
    performance: number;
  };
}

/**
 * Search filter for Qdrant queries
 */
export interface SearchFilter {
  must?: Array<{
    key: string;
    match?: { value: any };
    range?: { gte?: number; lte?: number; gt?: number; lt?: number };
  }>;
  should?: Array<{
    key: string;
    match?: { value: any };
    range?: { gte?: number; lte?: number; gt?: number; lt?: number };
  }>;
  must_not?: Array<{
    key: string;
    match?: { value: any };
  }>;
}

/**
 * Batch operation result
 */
export interface BatchResult<T> {
  successful: T[];
  failed: Array<{ item: any; error: Error }>;
  total: number;
  success_rate: number;
}
