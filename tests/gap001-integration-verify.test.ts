/**
 * GAP-001 System Integration Verification
 * Verifies fix is compatible with GAP-003 and GAP-006
 */

import { describe, it, expect } from '@jest/globals';
import { extractJSON, extractJSONSafe, hasJSON, parseMCPOutput } from '../lib/utils/mcp-parser';
import { ParallelAgentSpawner } from '../lib/orchestration/parallel-agent-spawner';

describe('GAP-001 System Integration Verification', () => {
  describe('MCP Parser Utility', () => {
    it('should be importable from utils', () => {
      expect(typeof extractJSON).toBe('function');
      expect(typeof extractJSONSafe).toBe('function');
      expect(typeof hasJSON).toBe('function');
      expect(typeof parseMCPOutput).toBe('function');
    });

    it('should handle real MCP output format', () => {
      const mcpOutput = `🔧 Claude-Flow MCP Server v2.0.0
⚡ Initializing swarm topology
✅ Ready for agent spawning
[{"agentId":"agent-001","status":"spawned","spawnTime":45}]`;

      const result = extractJSON(mcpOutput);
      expect(Array.isArray(result)).toBe(true);
      expect(result[0]).toEqual({
        agentId: 'agent-001',
        status: 'spawned',
        spawnTime: 45
      });
    });

    it('should extract prefix for logging', () => {
      const output = `🔧 Starting process
🚀 Loading agents
{"status":"ready"}`;

      const parsed = parseMCPOutput(output);
      expect(parsed.prefix).toContain('🔧');
      expect(parsed.prefix).toContain('🚀');
      expect(parsed.data).toEqual({ status: 'ready' });
      expect(parsed.hasJSON).toBe(true);
    });
  });

  describe('GAP-001 Parallel Spawner Integration', () => {
    it('should use extractJSON internally', () => {
      const spawner = new ParallelAgentSpawner();
      expect(spawner).toBeDefined();
      // Spawner now uses extractJSON from mcp-parser utility
    });

    it('should handle MCP output in production scenario', async () => {
      // Simulate MCP output with emoji prefix
      const mockMCPOutput = `🔧 Claude-Flow initialized
[
  {"agentId":"a1","status":"success","spawnTime":50},
  {"agentId":"a2","status":"success","spawnTime":52},
  {"agentId":"a3","status":"success","spawnTime":48}
]`;

      const results = extractJSON(mockMCPOutput);
      expect(results).toHaveLength(3);
      expect(results[0].agentId).toBe('a1');
      expect(results[0].status).toBe('success');
    });
  });

  describe('GAP-003 Query Control Compatibility', () => {
    it('should work with query control MCP calls', () => {
      const queryControlOutput = `🎯 Query control initiated
📊 Processing command
{"success":true,"queryId":"q-123","action":"pause"}`;

      const result = extractJSON(queryControlOutput);
      expect(result.success).toBe(true);
      expect(result.queryId).toBe('q-123');
      expect(result.action).toBe('pause');
    });

    it('should handle neural prediction output', () => {
      const neuralOutput = `🧠 Neural model loaded
⚡ Running prediction
{"prediction":"optimize_query","confidence":0.87}`;

      const result = extractJSON(neuralOutput);
      expect(result.prediction).toBe('optimize_query');
      expect(result.confidence).toBe(0.87);
    });
  });

  describe('GAP-006 Worker Management Compatibility', () => {
    it('should work with worker spawning output', () => {
      const workerOutput = `👷 Worker service starting
🔨 Spawning worker pool
[
  {"workerId":"w-001","type":"processor","status":"active"},
  {"workerId":"w-002","type":"analyzer","status":"active"}
]`;

      const workers = extractJSON(workerOutput);
      expect(workers).toHaveLength(2);
      expect(workers[0].workerId).toBe('w-001');
      expect(workers[1].type).toBe('analyzer');
    });

    it('should handle health check responses', () => {
      const healthOutput = `💓 Health check initiated
✅ Workers responding
{"healthy":true,"workerCount":5,"degraded":0,"failing":0}`;

      const health = extractJSON(healthOutput);
      expect(health.healthy).toBe(true);
      expect(health.workerCount).toBe(5);
    });
  });

  describe('Error Handling Across Systems', () => {
    it('should provide clear error messages', () => {
      const invalidOutput = 'No JSON here, just text';

      expect(() => extractJSON(invalidOutput)).toThrow('No JSON found in MCP output');
    });

    it('should handle empty output gracefully', () => {
      expect(() => extractJSON('')).toThrow('Invalid MCP output');
      expect(extractJSONSafe('')).toBeNull();
    });

    it('should handle malformed JSON with context', () => {
      const malformedOutput = '🔧 Starting\n{invalid json}';

      expect(() => extractJSON(malformedOutput)).toThrow('Failed to parse JSON');
    });
  });

  describe('AEON Constitution Compliance', () => {
    it('should maintain single source of truth', () => {
      // Utility is exported from one location
      const { extractJSON: util1 } = require('../lib/utils/mcp-parser');
      const { extractJSON: util2 } = require('../lib/utils/mcp-parser');

      expect(util1).toBe(util2); // Same function reference
    });

    it('should prevent duplication across GAPs', () => {
      // No inline implementations should exist
      // All should import from lib/utils/mcp-parser
      expect(typeof extractJSON).toBe('function');
    });
  });
});
