/**
 * GAP-001 MCP Parsing Bug - Test Suite
 * Tests robust JSON extraction from MCP output
 */

import { describe, it, expect } from '@jest/globals';

/**
 * Extract JSON from MCP output that may contain emoji/text prefix
 * This is the core fix for GAP-001
 */
function extractJSON(output: string): any {
  // Remove any leading non-JSON content (emojis, text, etc.)
  // JSON always starts with { or [
  const jsonStart = output.search(/[\{\[]/);

  if (jsonStart === -1) {
    throw new Error('No JSON found in output');
  }

  const jsonString = output.substring(jsonStart).trim();
  return JSON.parse(jsonString);
}

describe('GAP-001 MCP JSON Parsing', () => {
  it('should parse clean JSON output', () => {
    const output = '[{"agentId": "agent-1", "status": "success"}]';
    const result = extractJSON(output);
    expect(result).toEqual([{ agentId: 'agent-1', status: 'success' }]);
  });

  it('should parse JSON with emoji prefix', () => {
    const output = '🔧 Claude-Flow initialized\n[{"agentId": "agent-1", "status": "success"}]';
    const result = extractJSON(output);
    expect(result).toEqual([{ agentId: 'agent-1', status: 'success' }]);
  });

  it('should parse JSON with text prefix', () => {
    const output = 'Spawning agents...\n{"results": [{"id": "1"}]}';
    const result = extractJSON(output);
    expect(result).toEqual({ results: [{ id: '1' }] });
  });

  it('should parse JSON with multi-line prefix', () => {
    const output = `🚀 Starting parallel spawn
⚡ Batch processing enabled
[{"agentId": "a1"}, {"agentId": "a2"}]`;
    const result = extractJSON(output);
    expect(result).toEqual([{ agentId: 'a1' }, { agentId: 'a2' }]);
  });

  it('should handle JSON with whitespace', () => {
    const output = '  \n\t  [{"test": true}]  \n  ';
    const result = extractJSON(output);
    expect(result).toEqual([{ test: true }]);
  });

  it('should throw on no JSON', () => {
    const output = 'No JSON here!';
    expect(() => extractJSON(output)).toThrow('No JSON found in output');
  });

  it('should handle the exact error case from bug report', () => {
    const output = '🔧 Claude-Flow MCP Server v2.0.0\n[{"agentId":"agent-123","status":"spawned"}]';
    const result = extractJSON(output);
    expect(result).toEqual([{ agentId: 'agent-123', status: 'spawned' }]);
  });
});
