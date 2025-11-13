/**
 * MCP Integration Module
 *
 * Provides integration with Claude Flow MCP server for persistent memory storage.
 * Used by agent tracking system to store activity data in memory namespaces.
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export interface MemoryStoreOptions {
  action: 'store' | 'retrieve' | 'list' | 'delete';
  namespace: string;
  key: string;
  value?: string;
  ttl?: number;
}

/**
 * Direct MCP tool integration via claude-flow CLI
 * Uses ReasoningBank mode for persistent memory storage
 */
export class MCPIntegration {
  private readonly claudeFlowPath: string = 'npx claude-flow@alpha';

  /**
   * Store data in Claude Flow memory (ReasoningBank)
   * Format: claude-flow memory store <key> <value> --reasoningbank
   */
  async storeMemory(
    namespace: string,
    key: string,
    value: any,
    ttl: number = 604800 // 7 days default
  ): Promise<void> {
    try {
      // Create namespaced key: namespace:key
      const namespacedKey = `${namespace}:${key}`;

      // Serialize value to JSON string
      const jsonValue = JSON.stringify(value);

      // Escape for shell - replace single quotes with '\''
      const escapedValue = jsonValue.replace(/'/g, "'\\''");

      const command = `${this.claudeFlowPath} memory store "${namespacedKey}" '${escapedValue}' --reasoningbank`;

      const { stdout, stderr } = await execAsync(command, {
        maxBuffer: 10 * 1024 * 1024 // 10MB buffer for large data
      });

      if (stderr && !stderr.includes('Using ReasoningBank mode')) {
        console.error(`MCP memory store warning:`, stderr);
      }

      console.log(`✅ MCP Memory Stored: ${namespace}:${key}`);
    } catch (error: any) {
      console.error(`❌ MCP memory store failed:`, error.message);
      throw error;
    }
  }

  /**
   * Query data from Claude Flow memory (ReasoningBank)
   * Format: claude-flow memory query <search> --reasoningbank
   */
  async retrieveMemory(
    namespace: string,
    key: string
  ): Promise<any> {
    try {
      const namespacedKey = `${namespace}:${key}`;
      const command = `${this.claudeFlowPath} memory query "${namespacedKey}" --reasoningbank`;

      const { stdout } = await execAsync(command, {
        maxBuffer: 10 * 1024 * 1024
      });

      // Parse JSON from output (filter out info messages)
      const lines = stdout.trim().split('\n');
      const jsonLine = lines.find(line => line.startsWith('{') || line.startsWith('['));

      if (jsonLine) {
        return JSON.parse(jsonLine);
      }

      return null;
    } catch (error: any) {
      console.error(`❌ MCP memory retrieve failed:`, error.message);
      return null;
    }
  }

  /**
   * List all keys in namespace (queries by namespace prefix)
   */
  async listMemory(namespace: string): Promise<string[]> {
    try {
      const command = `${this.claudeFlowPath} memory query "${namespace}:" --reasoningbank`;

      const { stdout } = await execAsync(command, {
        maxBuffer: 10 * 1024 * 1024
      });

      // Parse results and extract keys
      const lines = stdout.trim().split('\n');
      const keys: string[] = [];

      for (const line of lines) {
        if (line.startsWith('{') || line.includes(`"${namespace}:`)) {
          try {
            const data = JSON.parse(line);
            if (data.key && data.key.startsWith(`${namespace}:`)) {
              keys.push(data.key);
            }
          } catch {
            // Skip non-JSON lines
          }
        }
      }

      return keys;
    } catch (error: any) {
      console.error(`❌ MCP memory list failed:`, error.message);
      return [];
    }
  }

  /**
   * Delete memory entry (not directly supported, but can overwrite with tombstone)
   */
  async deleteMemory(namespace: string, key: string): Promise<void> {
    try {
      // Store a tombstone record to mark as deleted
      await this.storeMemory(namespace, key, { _deleted: true, _timestamp: Date.now() }, 3600);
      console.log(`✅ MCP Memory Deleted: ${namespace}:${key}`);
    } catch (error: any) {
      console.error(`❌ MCP memory delete failed:`, error.message);
    }
  }

  /**
   * Health check - verify MCP is available
   */
  async healthCheck(): Promise<boolean> {
    try {
      const { stdout } = await execAsync(`${this.claudeFlowPath} --version`);
      console.log(`✅ MCP Available: ${stdout.trim()}`);
      return true;
    } catch (error: any) {
      console.error(`❌ MCP Unavailable:`, error.message);
      return false;
    }
  }
}

// Singleton instance
export const mcpIntegration = new MCPIntegration();
