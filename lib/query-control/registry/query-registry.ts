/**
 * GAP-003 Query Control System - Query Registry
 * Central registry for tracking all queries with MCP persistence
 */

import { QueryState, ModelType, PermissionMode, QueryMetadata } from '../types';
import { mcpClient } from '../mcp-client';

export class QueryRegistry {
  private queries: Map<string, QueryMetadata> = new Map();
  private namespace = 'query-registry';

  /**
   * Register a new query
   */
  async registerQuery(
    queryId: string,
    metadata: Partial<QueryMetadata>
  ): Promise<void> {
    const fullMetadata: QueryMetadata = {
      queryId,
      state: metadata.state || QueryState.INIT,
      model: metadata.model || ModelType.SONNET,
      permissionMode: metadata.permissionMode || PermissionMode.DEFAULT,
      startTime: metadata.startTime || Date.now(),
      lastUpdate: Date.now(),
      agentCount: metadata.agentCount || 0,
      taskCount: metadata.taskCount || 0,
      checkpointCount: metadata.checkpointCount || 0
    };

    // Store in local cache
    this.queries.set(queryId, fullMetadata);

    // Store in MCP memory for persistence (30 days)
    await mcpClient.storeMemory(
      queryId,
      fullMetadata,
      2592000 // 30 days TTL
    );

    // Train neural pattern on registration
    await mcpClient.trainNeuralPattern(
      'coordination',
      `query_register:${queryId}:${fullMetadata.model}`,
      10
    );
  }

  /**
   * Update existing query metadata
   */
  async updateQuery(
    queryId: string,
    updates: Partial<QueryMetadata>
  ): Promise<void> {
    const existing = this.queries.get(queryId);
    if (!existing) {
      throw new Error(`Query not found: ${queryId}`);
    }

    const updated: QueryMetadata = {
      ...existing,
      ...updates,
      lastUpdate: Date.now()
    };

    // Update local cache
    this.queries.set(queryId, updated);

    // Update MCP memory
    await mcpClient.storeMemory(queryId, updated, 2592000);

    // Train on update patterns
    if (updates.state) {
      await mcpClient.trainNeuralPattern(
        'coordination',
        `query_update:${queryId}:state:${updates.state}`,
        10
      );
    }
  }

  /**
   * Get query metadata
   */
  async getQuery(queryId: string): Promise<QueryMetadata | null> {
    // Try local cache first
    const local = this.queries.get(queryId);
    if (local) {
      return { ...local };
    }

    // Fallback to MCP memory
    const stored = await mcpClient.retrieveMemory(queryId);
    if (stored) {
      // Cache locally
      this.queries.set(queryId, stored);
      return stored;
    }

    return null;
  }

  /**
   * List all queries
   */
  async listQueries(filter?: {
    state?: QueryState;
    model?: ModelType;
  }): Promise<QueryMetadata[]> {
    let queries = Array.from(this.queries.values());

    if (filter) {
      if (filter.state) {
        queries = queries.filter(q => q.state === filter.state);
      }
      if (filter.model) {
        queries = queries.filter(q => q.model === filter.model);
      }
    }

    return queries;
  }

  /**
   * Get queries by state
   */
  async getQueriesByState(state: QueryState): Promise<QueryMetadata[]> {
    return this.listQueries({ state });
  }

  /**
   * Get active queries (INIT or RUNNING)
   */
  async getActiveQueries(): Promise<QueryMetadata[]> {
    const queries = Array.from(this.queries.values());
    return queries.filter(
      q => q.state === QueryState.INIT || q.state === QueryState.RUNNING
    );
  }

  /**
   * Get paused queries
   */
  async getPausedQueries(): Promise<QueryMetadata[]> {
    return this.getQueriesByState(QueryState.PAUSED);
  }

  /**
   * Get completed queries
   */
  async getCompletedQueries(): Promise<QueryMetadata[]> {
    const queries = Array.from(this.queries.values());
    return queries.filter(
      q => q.state === QueryState.COMPLETED || q.state === QueryState.TERMINATED
    );
  }

  /**
   * Delete query from registry
   */
  async deleteQuery(queryId: string): Promise<boolean> {
    const deleted = this.queries.delete(queryId);

    if (deleted) {
      // Note: MCP memory will expire based on TTL
      await mcpClient.trainNeuralPattern(
        'coordination',
        `query_delete:${queryId}`,
        10
      );
    }

    return deleted;
  }

  /**
   * Get registry statistics
   */
  getStatistics(): {
    total: number;
    byState: Record<QueryState, number>;
    byModel: Record<ModelType, number>;
  } {
    const queries = Array.from(this.queries.values());

    const byState: Record<QueryState, number> = {
      [QueryState.INIT]: 0,
      [QueryState.RUNNING]: 0,
      [QueryState.PAUSED]: 0,
      [QueryState.COMPLETED]: 0,
      [QueryState.TERMINATED]: 0,
      [QueryState.ERROR]: 0
    };

    const byModel: Record<ModelType, number> = {
      [ModelType.SONNET]: 0,
      [ModelType.HAIKU]: 0,
      [ModelType.OPUS]: 0
    };

    for (const query of queries) {
      byState[query.state]++;
      byModel[query.model]++;
    }

    return {
      total: queries.length,
      byState,
      byModel
    };
  }

  /**
   * Clear all queries (use with caution)
   */
  clearAll(): void {
    this.queries.clear();
  }
}

export const queryRegistry = new QueryRegistry();
