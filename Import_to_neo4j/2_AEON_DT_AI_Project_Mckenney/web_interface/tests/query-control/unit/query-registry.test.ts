/**
 * GAP-003 Query Control System - Query Registry Unit Tests
 *
 * File: tests/query-control/unit/query-registry.test.ts
 * Created: 2025-11-14
 * Version: v1.0.0
 * Purpose: Comprehensive unit tests for QueryRegistry
 *
 * Constitutional Compliance:
 * - DILIGENCE: >90% code coverage
 * - INTEGRITY: All CRUD operations tested
 * - NO DEVELOPMENT THEATER: Production-grade tests
 */

import { describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import {
  QueryRegistry,
  getQueryRegistry,
  type QueryMetadata
} from '../../../lib/query-control/registry/query-registry';
import { QueryState } from '../../../lib/query-control/state/state-machine';

describe('QueryRegistry', () => {
  let registry: QueryRegistry;

  beforeEach(() => {
    registry = new QueryRegistry();
  });

  afterEach(async () => {
    // Clean up after each test
    await registry.clear();
  });

  describe('Registration', () => {
    test('should register new query', async () => {
      const metadata: Omit<QueryMetadata, 'queryId' | 'lastUpdate'> = {
        state: QueryState.INIT,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 0,
        taskCount: 0,
        checkpointCount: 0
      };

      await registry.registerQuery('query-001', metadata);

      const retrieved = await registry.getQuery('query-001');
      expect(retrieved).not.toBeNull();
      expect(retrieved?.queryId).toBe('query-001');
      expect(retrieved?.state).toBe(QueryState.INIT);
      expect(retrieved?.model).toBe('sonnet');
    });

    test('should set lastUpdate timestamp on registration', async () => {
      const before = Date.now();

      await registry.registerQuery('query-002', {
        state: QueryState.RUNNING,
        model: 'haiku',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 3,
        taskCount: 5,
        checkpointCount: 0
      });

      const after = Date.now();
      const retrieved = await registry.getQuery('query-002');

      expect(retrieved?.lastUpdate).toBeGreaterThanOrEqual(before);
      expect(retrieved?.lastUpdate).toBeLessThanOrEqual(after);
    });

    test('should register multiple queries', async () => {
      await registry.registerQuery('query-003', {
        state: QueryState.RUNNING,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 2,
        taskCount: 3,
        checkpointCount: 1
      });

      await registry.registerQuery('query-004', {
        state: QueryState.PAUSED,
        model: 'opus',
        permissionMode: 'plan',
        startTime: Date.now(),
        agentCount: 5,
        taskCount: 10,
        checkpointCount: 2
      });

      const query1 = await registry.getQuery('query-003');
      const query2 = await registry.getQuery('query-004');

      expect(query1).not.toBeNull();
      expect(query2).not.toBeNull();
      expect(query1?.model).toBe('sonnet');
      expect(query2?.model).toBe('opus');
    });
  });

  describe('Retrieval', () => {
    test('should retrieve registered query', async () => {
      await registry.registerQuery('query-005', {
        state: QueryState.COMPLETED,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 4,
        taskCount: 8,
        checkpointCount: 3
      });

      const retrieved = await registry.getQuery('query-005');
      expect(retrieved).not.toBeNull();
      expect(retrieved?.queryId).toBe('query-005');
      expect(retrieved?.state).toBe(QueryState.COMPLETED);
    });

    test('should return null for non-existent query', async () => {
      const retrieved = await registry.getQuery('non-existent');
      expect(retrieved).toBeNull();
    });

    test('should retrieve from L1 cache (memory)', async () => {
      await registry.registerQuery('query-006', {
        state: QueryState.RUNNING,
        model: 'haiku',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 1,
        taskCount: 2,
        checkpointCount: 0
      });

      // Second retrieval should hit L1 cache
      const retrieved = await registry.getQuery('query-006');
      expect(retrieved).not.toBeNull();
      expect(retrieved?.model).toBe('haiku');
    });
  });

  describe('Updates', () => {
    test('should update existing query', async () => {
      await registry.registerQuery('query-007', {
        state: QueryState.RUNNING,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 2,
        taskCount: 3,
        checkpointCount: 0
      });

      await registry.updateQuery('query-007', {
        state: QueryState.PAUSED,
        agentCount: 5,
        checkpointCount: 1
      });

      const updated = await registry.getQuery('query-007');
      expect(updated?.state).toBe(QueryState.PAUSED);
      expect(updated?.agentCount).toBe(5);
      expect(updated?.checkpointCount).toBe(1);
      expect(updated?.model).toBe('sonnet'); // Preserved
    });

    test('should update lastUpdate timestamp', async () => {
      await registry.registerQuery('query-008', {
        state: QueryState.INIT,
        model: 'haiku',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 0,
        taskCount: 0,
        checkpointCount: 0
      });

      const original = await registry.getQuery('query-008');
      const originalTime = original!.lastUpdate;

      // Wait a bit to ensure timestamp changes
      await new Promise(resolve => setTimeout(resolve, 10));

      await registry.updateQuery('query-008', {
        state: QueryState.RUNNING
      });

      const updated = await registry.getQuery('query-008');
      expect(updated!.lastUpdate).toBeGreaterThan(originalTime);
    });

    test('should throw error updating non-existent query', async () => {
      await expect(registry.updateQuery('non-existent', {
        state: QueryState.COMPLETED
      })).rejects.toThrow('Query not found');
    });
  });

  describe('Listing', () => {
    beforeEach(async () => {
      // Register test queries
      await registry.registerQuery('list-001', {
        state: QueryState.RUNNING,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now() - 3600000, // 1 hour ago
        agentCount: 2,
        taskCount: 3,
        checkpointCount: 1
      });

      await registry.registerQuery('list-002', {
        state: QueryState.PAUSED,
        model: 'haiku',
        permissionMode: 'plan',
        startTime: Date.now() - 1800000, // 30 min ago
        agentCount: 1,
        taskCount: 5,
        checkpointCount: 2
      });

      await registry.registerQuery('list-003', {
        state: QueryState.COMPLETED,
        model: 'opus',
        permissionMode: 'default',
        startTime: Date.now() - 900000, // 15 min ago
        agentCount: 4,
        taskCount: 10,
        checkpointCount: 5
      });
    });

    test('should list all queries', async () => {
      const result = await registry.listQueries();
      expect(result.queries.length).toBeGreaterThanOrEqual(3);
      expect(result.total).toBeGreaterThanOrEqual(3);
    });

    test('should filter by state', async () => {
      const result = await registry.listQueries({
        state: QueryState.RUNNING
      });

      expect(result.queries.every(q => q.state === QueryState.RUNNING)).toBe(true);
      expect(result.queries.some(q => q.queryId === 'list-001')).toBe(true);
    });

    test('should filter by model', async () => {
      const result = await registry.listQueries({
        model: 'haiku'
      });

      expect(result.queries.every(q => q.model === 'haiku')).toBe(true);
      expect(result.queries.some(q => q.queryId === 'list-002')).toBe(true);
    });

    test('should filter by start time range', async () => {
      const now = Date.now();
      const twoHoursAgo = now - 7200000;
      const thirtyMinAgo = now - 1800000;

      const result = await registry.listQueries({
        startTimeAfter: twoHoursAgo,
        startTimeBefore: thirtyMinAgo
      });

      expect(result.queries.every(q =>
        q.startTime >= twoHoursAgo && q.startTime <= thirtyMinAgo
      )).toBe(true);
    });

    test('should apply multiple filters', async () => {
      await registry.registerQuery('list-004', {
        state: QueryState.RUNNING,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now() - 600000, // 10 min ago
        agentCount: 3,
        taskCount: 7,
        checkpointCount: 2
      });

      const result = await registry.listQueries({
        state: QueryState.RUNNING,
        model: 'sonnet'
      });

      expect(result.queries.every(q =>
        q.state === QueryState.RUNNING && q.model === 'sonnet'
      )).toBe(true);
    });

    test('should limit results', async () => {
      const result = await registry.listQueries({ limit: 2 });
      expect(result.queries).toHaveLength(2);
      expect(result.hasMore).toBe(true);
    });

    test('should sort by most recent first', async () => {
      const result = await registry.listQueries();

      // Check that queries are sorted by lastUpdate descending
      for (let i = 0; i < result.queries.length - 1; i++) {
        expect(result.queries[i].lastUpdate).toBeGreaterThanOrEqual(
          result.queries[i + 1].lastUpdate
        );
      }
    });
  });

  describe('Deletion', () => {
    test('should delete query', async () => {
      await registry.registerQuery('delete-001', {
        state: QueryState.COMPLETED,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 2,
        taskCount: 5,
        checkpointCount: 3
      });

      const deleted = await registry.deleteQuery('delete-001');
      expect(deleted).toBe(true);

      const retrieved = await registry.getQuery('delete-001');
      expect(retrieved).toBeNull();
    });

    test('should return false deleting non-existent query', async () => {
      const deleted = await registry.deleteQuery('non-existent');
      expect(deleted).toBe(false);
    });
  });

  describe('Query Count by State', () => {
    beforeEach(async () => {
      await registry.registerQuery('count-001', {
        state: QueryState.RUNNING,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 1,
        taskCount: 2,
        checkpointCount: 0
      });

      await registry.registerQuery('count-002', {
        state: QueryState.RUNNING,
        model: 'haiku',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 2,
        taskCount: 3,
        checkpointCount: 1
      });

      await registry.registerQuery('count-003', {
        state: QueryState.PAUSED,
        model: 'opus',
        permissionMode: 'plan',
        startTime: Date.now(),
        agentCount: 3,
        taskCount: 5,
        checkpointCount: 2
      });

      await registry.registerQuery('count-004', {
        state: QueryState.COMPLETED,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 4,
        taskCount: 8,
        checkpointCount: 5
      });
    });

    test('should count queries by state', async () => {
      const counts = await registry.getQueryCountByState();

      expect(counts[QueryState.RUNNING]).toBeGreaterThanOrEqual(2);
      expect(counts[QueryState.PAUSED]).toBeGreaterThanOrEqual(1);
      expect(counts[QueryState.COMPLETED]).toBeGreaterThanOrEqual(1);
    });

    test('should include all states in count', async () => {
      const counts = await registry.getQueryCountByState();

      expect(counts).toHaveProperty(QueryState.INIT);
      expect(counts).toHaveProperty(QueryState.RUNNING);
      expect(counts).toHaveProperty(QueryState.PAUSED);
      expect(counts).toHaveProperty(QueryState.COMPLETED);
      expect(counts).toHaveProperty(QueryState.TERMINATED);
      expect(counts).toHaveProperty(QueryState.ERROR);
    });
  });

  describe('Singleton Pattern', () => {
    test('should return same instance', () => {
      const instance1 = getQueryRegistry();
      const instance2 = getQueryRegistry();
      expect(instance1).toBe(instance2);
    });
  });

  describe('Clear', () => {
    test('should clear all queries', async () => {
      await registry.registerQuery('clear-001', {
        state: QueryState.RUNNING,
        model: 'sonnet',
        permissionMode: 'default',
        startTime: Date.now(),
        agentCount: 1,
        taskCount: 2,
        checkpointCount: 0
      });

      await registry.clear();

      const result = await registry.listQueries();
      expect(result.queries).toHaveLength(0);
      expect(result.total).toBe(0);
    });
  });
});
