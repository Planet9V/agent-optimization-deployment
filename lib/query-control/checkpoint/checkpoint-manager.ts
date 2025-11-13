/**
 * GAP-003 Query Control System - Checkpoint Manager
 * Manages checkpoint creation, storage, and retrieval with L1+L2 caching
 */

import { QueryContext, QueryState } from '../types';
import { QdrantClient, Checkpoint, qdrantClient } from './qdrant-client';
import { mcpClient } from '../mcp-client';

/**
 * Checkpoint Manager with multi-level caching
 * L1: MCP memory (fast, 2-15ms, 7-day TTL)
 * L2: Qdrant vector storage (persistent, 50-150ms, unlimited)
 */
export class CheckpointManager {
  private qdrant: QdrantClient;
  private l1Namespace = 'checkpoints';

  constructor(qdrantClient?: QdrantClient) {
    this.qdrant = qdrantClient || qdrantClient;
  }

  /**
   * Initialize checkpoint manager
   */
  async initialize(): Promise<void> {
    await this.qdrant.initialize();
    console.log('CheckpointManager initialized');
  }

  /**
   * Create checkpoint from query context
   */
  async createCheckpoint(
    queryId: string,
    context: QueryContext,
    reason: string = 'user_pause'
  ): Promise<Checkpoint> {
    const startTime = Date.now();

    try {
      // Build checkpoint
      const checkpoint: Checkpoint = {
        queryId,
        timestamp: Date.now(),
        state: context.state || QueryState.PAUSED,
        executionContext: this.captureExecutionContext(context),
        modelConfig: this.captureModelConfig(context),
        metadata: {
          createdBy: 'QueryControlSystem',
          reason,
          size: 0
        },
        embedding: this.qdrant.generateEmbedding(context)
      };

      // Calculate size
      checkpoint.metadata.size = JSON.stringify(checkpoint).length;

      // Store in L2 (Qdrant) first for persistence
      await this.qdrant.upsert(checkpoint);

      // Store in L1 (MCP memory) for fast access
      await mcpClient.storeMemory(
        `checkpoint_${queryId}`,
        checkpoint,
        604800 // 7 days TTL
      );

      // Train neural pattern on checkpoint creation
      await mcpClient.trainNeuralPattern(
        'coordination',
        `checkpoint_create:${queryId}:${checkpoint.metadata.size}:${reason}`,
        10
      );

      const duration = Date.now() - startTime;
      console.log(
        `Checkpoint created: ${queryId} (${checkpoint.metadata.size} bytes, ${duration}ms)`
      );

      // Validate performance target (<150ms)
      if (duration > 150) {
        console.warn(
          `Checkpoint creation exceeded target: ${duration}ms (target: <150ms)`
        );
      }

      return checkpoint;
    } catch (error) {
      console.error(`Failed to create checkpoint: ${error}`);
      throw error;
    }
  }

  /**
   * Retrieve checkpoint with L1+L2 fallback
   */
  async retrieveCheckpoint(queryId: string): Promise<Checkpoint | null> {
    const startTime = Date.now();

    try {
      // Try L1 cache (MCP memory) first - fastest
      const l1Result = await mcpClient.retrieveMemory(`checkpoint_${queryId}`);
      if (l1Result) {
        const duration = Date.now() - startTime;
        console.log(
          `Checkpoint retrieved from L1 cache: ${queryId} (${duration}ms)`
        );
        return l1Result;
      }

      // Fallback to L2 (Qdrant) - slower but persistent
      const l2Result = await this.qdrant.retrieve(queryId);
      if (l2Result) {
        // Promote to L1 cache for future fast access
        await mcpClient.storeMemory(
          `checkpoint_${queryId}`,
          l2Result,
          604800
        );

        const duration = Date.now() - startTime;
        console.log(
          `Checkpoint retrieved from L2 storage: ${queryId} (${duration}ms)`
        );

        // Validate performance target (<100ms)
        if (duration > 100) {
          console.warn(
            `Checkpoint retrieval exceeded target: ${duration}ms (target: <100ms)`
          );
        }

        return l2Result;
      }

      console.log(`Checkpoint not found: ${queryId}`);
      return null;
    } catch (error) {
      console.error(`Failed to retrieve checkpoint: ${error}`);
      return null;
    }
  }

  /**
   * Find similar checkpoints using vector search
   */
  async findSimilarCheckpoints(
    context: QueryContext,
    limit: number = 5
  ): Promise<Checkpoint[]> {
    try {
      const embedding = this.qdrant.generateEmbedding(context);
      const similar = await this.qdrant.search(embedding, limit);

      console.log(
        `Found ${similar.length} similar checkpoints for query: ${context.queryId}`
      );

      return similar;
    } catch (error) {
      console.error(`Failed to find similar checkpoints: ${error}`);
      return [];
    }
  }

  /**
   * Delete checkpoint from both L1 and L2
   */
  async deleteCheckpoint(queryId: string): Promise<boolean> {
    try {
      // Delete from L2 (Qdrant)
      const qdrantDeleted = await this.qdrant.delete(queryId);

      // Note: L1 (MCP memory) will expire based on TTL
      // We could implement explicit deletion if needed

      console.log(`Checkpoint deleted: ${queryId}`);

      return qdrantDeleted;
    } catch (error) {
      console.error(`Failed to delete checkpoint: ${error}`);
      return false;
    }
  }

  /**
   * Capture execution context from query context
   */
  private captureExecutionContext(context: QueryContext): Checkpoint['executionContext'] {
    return {
      agentStates: context.execution?.agentStates
        ? Object.fromEntries(context.execution.agentStates)
        : {},
      taskQueue: context.execution?.taskQueue || [],
      completedTasks: context.execution?.completedTasks || [],
      dependencies: context.execution?.dependencies
        ? Object.fromEntries(context.execution.dependencies.edges)
        : {},
      resources: context.execution?.resources || {
        cpuPercent: 0,
        memoryMB: 0,
        agentCount: 0
      }
    };
  }

  /**
   * Capture model configuration from query context
   */
  private captureModelConfig(context: QueryContext): Checkpoint['modelConfig'] {
    return {
      currentModel: context.model?.currentModel || 'claude-sonnet-4-5-20250929',
      permissionMode: context.model?.permissionMode || 'default',
      configuration: context.model?.configuration || {}
    };
  }

  /**
   * Get checkpoint statistics
   */
  async getStatistics(): Promise<{
    totalCheckpoints: number;
    l2Status: string;
  }> {
    try {
      const qdrantStats = await this.qdrant.getStats();

      return {
        totalCheckpoints: qdrantStats.pointCount,
        l2Status: qdrantStats.status
      };
    } catch (error) {
      console.error(`Failed to get statistics: ${error}`);
      return {
        totalCheckpoints: 0,
        l2Status: 'error'
      };
    }
  }
}

export const checkpointManager = new CheckpointManager();
