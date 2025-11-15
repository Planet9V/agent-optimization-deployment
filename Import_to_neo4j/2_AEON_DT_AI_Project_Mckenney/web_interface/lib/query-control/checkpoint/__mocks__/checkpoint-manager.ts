/**
 * Mock CheckpointManager for Testing
 *
 * Provides in-memory checkpoint storage without requiring Qdrant connection
 */

import { QueryState } from '../../state/state-machine';
import type { Checkpoint, CheckpointMetadata, ExecutionContext, ModelConfig } from '../checkpoint-manager';

class MockCheckpointManager {
  private checkpoints: Map<string, Checkpoint[]> = new Map();

  async createCheckpoint(
    queryId: string,
    context: ExecutionContext,
    modelConfig: ModelConfig,
    reason: CheckpointMetadata['checkpointReason']
  ): Promise<Checkpoint> {
    const timestamp = Date.now();
    const checkpoint: Checkpoint = {
      queryId,
      timestamp,
      state: QueryState.PAUSED,
      executionContext: context,
      modelConfig,
      metadata: {
        queryId,
        timestamp,
        state: QueryState.PAUSED,
        checkpointReason: reason,
        size: JSON.stringify(context).length,
        createdBy: 'system'
      },
      embedding: [] // Empty embedding for mock - not used in tests
    };

    const queryCheckpoints = this.checkpoints.get(queryId) || [];
    queryCheckpoints.push(checkpoint);
    this.checkpoints.set(queryId, queryCheckpoints);

    return checkpoint;
  }

  async getLatestCheckpoint(queryId: string): Promise<Checkpoint | null> {
    const queryCheckpoints = this.checkpoints.get(queryId);
    if (!queryCheckpoints || queryCheckpoints.length === 0) {
      return null;
    }
    return queryCheckpoints[queryCheckpoints.length - 1];
  }

  async getCheckpoint(queryId: string, timestamp: number): Promise<Checkpoint | null> {
    const queryCheckpoints = this.checkpoints.get(queryId);
    if (!queryCheckpoints) {
      return null;
    }
    return queryCheckpoints.find(cp => cp.timestamp === timestamp) || null;
  }

  async getCheckpointCount(queryId: string): Promise<number> {
    const queryCheckpoints = this.checkpoints.get(queryId);
    return queryCheckpoints?.length || 0;
  }

  async deleteCheckpoint(queryId: string, timestamp: number): Promise<boolean> {
    const queryCheckpoints = this.checkpoints.get(queryId);
    if (!queryCheckpoints) {
      return false;
    }

    const index = queryCheckpoints.findIndex(cp => cp.timestamp === timestamp);
    if (index === -1) {
      return false;
    }

    queryCheckpoints.splice(index, 1);
    return true;
  }

  clearAll(): void {
    this.checkpoints.clear();
  }
}

let mockInstance: MockCheckpointManager | null = null;

export function getCheckpointManager(): MockCheckpointManager {
  if (!mockInstance) {
    mockInstance = new MockCheckpointManager();
  }
  return mockInstance;
}

// Export types
export type { Checkpoint, CheckpointMetadata, ExecutionContext, ModelConfig };
