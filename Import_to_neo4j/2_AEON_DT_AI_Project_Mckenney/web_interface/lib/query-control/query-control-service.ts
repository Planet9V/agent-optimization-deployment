import { QueryState, QueryMetadata } from './types';
import { QueryRegistry } from './registry/query-registry';
import { CheckpointManager } from './checkpoint/checkpoint-manager';

export class QueryControlService {
  private registry: QueryRegistry;
  private checkpointManager: CheckpointManager;

  constructor() {
    this.registry = new QueryRegistry();
    this.checkpointManager = new CheckpointManager();
  }

  async listQueries(): Promise<QueryMetadata[]> {
    return this.registry.listAll();
  }

  async getQuery(queryId: string): Promise<QueryState | null> {
    return this.registry.get(queryId);
  }

  async pauseQuery(queryId: string): Promise<boolean> {
    const query = await this.registry.get(queryId);
    if (query) {
      query.status = 'paused';
      await this.registry.update(queryId, query);
      return true;
    }
    return false;
  }

  async resumeQuery(queryId: string): Promise<boolean> {
    const query = await this.registry.get(queryId);
    if (query) {
      query.status = 'running';
      await this.registry.update(queryId, query);
      return true;
    }
    return false;
  }

  async getCheckpoints(queryId: string) {
    return this.checkpointManager.list(queryId);
  }
}
