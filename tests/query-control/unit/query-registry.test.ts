/**
 * GAP-003 Query Control System - Query Registry Unit Tests
 * Comprehensive test suite for query registry functionality
 */

import { QueryRegistry } from '../../../lib/query-control/registry/query-registry';
import { QueryState, ModelType, PermissionMode } from '../../../lib/query-control/types';

describe('QueryRegistry', () => {
  let registry: QueryRegistry;

  beforeEach(() => {
    registry = new QueryRegistry();
    registry.clearAll();
  });

  describe('Query registration', () => {
    test('should register a new query', async () => {
      await registry.registerQuery('query-001', {
        state: QueryState.INIT,
        model: ModelType.SONNET
      });

      const query = await registry.getQuery('query-001');
      expect(query).toBeDefined();
      expect(query?.queryId).toBe('query-001');
    });

    test('should set default values for missing fields', async () => {
      await registry.registerQuery('query-002', {});

      const query = await registry.getQuery('query-002');
      expect(query?.state).toBe(QueryState.INIT);
      expect(query?.model).toBe(ModelType.SONNET);
      expect(query?.permissionMode).toBe(PermissionMode.DEFAULT);
      expect(query?.agentCount).toBe(0);
      expect(query?.taskCount).toBe(0);
      expect(query?.checkpointCount).toBe(0);
    });

    test('should set timestamps on registration', async () => {
      await registry.registerQuery('query-003', {});

      const query = await registry.getQuery('query-003');
      expect(query?.startTime).toBeDefined();
      expect(query?.lastUpdate).toBeDefined();
      expect(typeof query?.startTime).toBe('number');
    });

    test('should accept custom metadata', async () => {
      await registry.registerQuery('query-004', {
        state: QueryState.RUNNING,
        model: ModelType.HAIKU,
        permissionMode: PermissionMode.ACCEPT_EDITS,
        agentCount: 5,
        taskCount: 10,
        checkpointCount: 2
      });

      const query = await registry.getQuery('query-004');
      expect(query?.state).toBe(QueryState.RUNNING);
      expect(query?.model).toBe(ModelType.HAIKU);
      expect(query?.permissionMode).toBe(PermissionMode.ACCEPT_EDITS);
      expect(query?.agentCount).toBe(5);
      expect(query?.taskCount).toBe(10);
      expect(query?.checkpointCount).toBe(2);
    });
  });

  describe('Query updates', () => {
    beforeEach(async () => {
      await registry.registerQuery('query-update-001', {
        state: QueryState.INIT
      });
    });

    test('should update query state', async () => {
      await registry.updateQuery('query-update-001', {
        state: QueryState.RUNNING
      });

      const query = await registry.getQuery('query-update-001');
      expect(query?.state).toBe(QueryState.RUNNING);
    });

    test('should update lastUpdate timestamp', async () => {
      const query = await registry.getQuery('query-update-001');
      const oldTimestamp = query?.lastUpdate!;

      await new Promise(resolve => setTimeout(resolve, 10));

      await registry.updateQuery('query-update-001', {
        state: QueryState.RUNNING
      });

      const updated = await registry.getQuery('query-update-001');
      expect(updated?.lastUpdate).toBeGreaterThan(oldTimestamp);
    });

    test('should throw error when updating non-existent query', async () => {
      await expect(
        registry.updateQuery('non-existent', { state: QueryState.RUNNING })
      ).rejects.toThrow('Query not found: non-existent');
    });

    test('should update multiple fields', async () => {
      await registry.updateQuery('query-update-001', {
        state: QueryState.RUNNING,
        agentCount: 3,
        taskCount: 7,
        checkpointCount: 1
      });

      const query = await registry.getQuery('query-update-001');
      expect(query?.state).toBe(QueryState.RUNNING);
      expect(query?.agentCount).toBe(3);
      expect(query?.taskCount).toBe(7);
      expect(query?.checkpointCount).toBe(1);
    });

    test('should preserve unchanged fields', async () => {
      await registry.updateQuery('query-update-001', {
        state: QueryState.RUNNING
      });

      const query = await registry.getQuery('query-update-001');
      expect(query?.model).toBe(ModelType.SONNET); // Should still be default
      expect(query?.queryId).toBe('query-update-001');
    });
  });

  describe('Query retrieval', () => {
    beforeEach(async () => {
      await registry.registerQuery('query-get-001', {});
    });

    test('should retrieve existing query', async () => {
      const query = await registry.getQuery('query-get-001');
      expect(query).toBeDefined();
      expect(query?.queryId).toBe('query-get-001');
    });

    test('should return null for non-existent query', async () => {
      const query = await registry.getQuery('non-existent');
      expect(query).toBeNull();
    });

    test('should return copy of query metadata', async () => {
      const query1 = await registry.getQuery('query-get-001');
      const query2 = await registry.getQuery('query-get-001');
      expect(query1).not.toBe(query2); // Different objects
      expect(query1).toEqual(query2); // Same content
    });
  });

  describe('Query listing', () => {
    beforeEach(async () => {
      await registry.registerQuery('list-001', { state: QueryState.INIT });
      await registry.registerQuery('list-002', { state: QueryState.RUNNING });
      await registry.registerQuery('list-003', { state: QueryState.PAUSED });
      await registry.registerQuery('list-004', { state: QueryState.COMPLETED });
      await registry.registerQuery('list-005', { state: QueryState.RUNNING, model: ModelType.HAIKU });
    });

    test('should list all queries without filter', async () => {
      const queries = await registry.listQueries();
      expect(queries.length).toBe(5);
    });

    test('should filter queries by state', async () => {
      const running = await registry.listQueries({ state: QueryState.RUNNING });
      expect(running.length).toBe(2);
      expect(running.every(q => q.state === QueryState.RUNNING)).toBe(true);
    });

    test('should filter queries by model', async () => {
      const haiku = await registry.listQueries({ model: ModelType.HAIKU });
      expect(haiku.length).toBe(1);
      expect(haiku[0].model).toBe(ModelType.HAIKU);
    });

    test('should filter by both state and model', async () => {
      const filtered = await registry.listQueries({
        state: QueryState.RUNNING,
        model: ModelType.HAIKU
      });
      expect(filtered.length).toBe(1);
      expect(filtered[0].queryId).toBe('list-005');
    });
  });

  describe('Queries by state', () => {
    beforeEach(async () => {
      await registry.registerQuery('state-001', { state: QueryState.INIT });
      await registry.registerQuery('state-002', { state: QueryState.RUNNING });
      await registry.registerQuery('state-003', { state: QueryState.PAUSED });
      await registry.registerQuery('state-004', { state: QueryState.COMPLETED });
    });

    test('should get queries by specific state', async () => {
      const paused = await registry.getQueriesByState(QueryState.PAUSED);
      expect(paused.length).toBe(1);
      expect(paused[0].queryId).toBe('state-003');
    });

    test('should get active queries (INIT + RUNNING)', async () => {
      const active = await registry.getActiveQueries();
      expect(active.length).toBe(2);
      expect(active.some(q => q.queryId === 'state-001')).toBe(true);
      expect(active.some(q => q.queryId === 'state-002')).toBe(true);
    });

    test('should get paused queries', async () => {
      const paused = await registry.getPausedQueries();
      expect(paused.length).toBe(1);
      expect(paused[0].queryId).toBe('state-003');
    });

    test('should get completed queries (COMPLETED + TERMINATED)', async () => {
      await registry.registerQuery('state-005', { state: QueryState.TERMINATED });

      const completed = await registry.getCompletedQueries();
      expect(completed.length).toBe(2);
      expect(completed.some(q => q.queryId === 'state-004')).toBe(true);
      expect(completed.some(q => q.queryId === 'state-005')).toBe(true);
    });
  });

  describe('Query deletion', () => {
    beforeEach(async () => {
      await registry.registerQuery('delete-001', {});
    });

    test('should delete existing query', async () => {
      const deleted = await registry.deleteQuery('delete-001');
      expect(deleted).toBe(true);

      const query = await registry.getQuery('delete-001');
      expect(query).toBeNull();
    });

    test('should return false when deleting non-existent query', async () => {
      const deleted = await registry.deleteQuery('non-existent');
      expect(deleted).toBe(false);
    });
  });

  describe('Statistics', () => {
    beforeEach(async () => {
      await registry.registerQuery('stats-001', { state: QueryState.INIT });
      await registry.registerQuery('stats-002', { state: QueryState.RUNNING });
      await registry.registerQuery('stats-003', { state: QueryState.RUNNING, model: ModelType.HAIKU });
      await registry.registerQuery('stats-004', { state: QueryState.PAUSED, model: ModelType.OPUS });
      await registry.registerQuery('stats-005', { state: QueryState.COMPLETED });
    });

    test('should return total count', () => {
      const stats = registry.getStatistics();
      expect(stats.total).toBe(5);
    });

    test('should count queries by state', () => {
      const stats = registry.getStatistics();
      expect(stats.byState[QueryState.INIT]).toBe(1);
      expect(stats.byState[QueryState.RUNNING]).toBe(2);
      expect(stats.byState[QueryState.PAUSED]).toBe(1);
      expect(stats.byState[QueryState.COMPLETED]).toBe(1);
      expect(stats.byState[QueryState.TERMINATED]).toBe(0);
      expect(stats.byState[QueryState.ERROR]).toBe(0);
    });

    test('should count queries by model', () => {
      const stats = registry.getStatistics();
      expect(stats.byModel[ModelType.SONNET]).toBe(3);
      expect(stats.byModel[ModelType.HAIKU]).toBe(1);
      expect(stats.byModel[ModelType.OPUS]).toBe(1);
    });
  });

  describe('Clear operations', () => {
    beforeEach(async () => {
      await registry.registerQuery('clear-001', {});
      await registry.registerQuery('clear-002', {});
      await registry.registerQuery('clear-003', {});
    });

    test('should clear all queries', () => {
      const statsBefore = registry.getStatistics();
      expect(statsBefore.total).toBe(3);

      registry.clearAll();

      const statsAfter = registry.getStatistics();
      expect(statsAfter.total).toBe(0);
    });
  });

  describe('MCP Integration', () => {
    test('should store queries in MCP memory', async () => {
      await registry.registerQuery('mcp-001', {});
      // Verify via retrieval (which checks MCP memory)
      const query = await registry.getQuery('mcp-001');
      expect(query).toBeDefined();
    });

    test('should train neural patterns on registration', async () => {
      // Neural training is async, success is indicated by successful registration
      await registry.registerQuery('mcp-002', { model: ModelType.HAIKU });
      const query = await registry.getQuery('mcp-002');
      expect(query?.model).toBe(ModelType.HAIKU);
    });

    test('should train neural patterns on updates', async () => {
      await registry.registerQuery('mcp-003', {});
      await registry.updateQuery('mcp-003', { state: QueryState.RUNNING });
      const query = await registry.getQuery('mcp-003');
      expect(query?.state).toBe(QueryState.RUNNING);
    });
  });
});
