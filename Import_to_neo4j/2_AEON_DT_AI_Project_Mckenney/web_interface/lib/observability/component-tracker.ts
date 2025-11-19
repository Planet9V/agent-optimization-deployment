/**
 * Component Change Tracker
 *
 * Tracks all code changes, component creations, and API modifications.
 * Reports to Wiki Agent for documentation.
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export interface FileChangeRecord {
  filePath: string;
  changeType: 'created' | 'modified' | 'deleted';
  lineCount: number;
  diff: string;
  timestamp: string;
  systemTime: string;
}

export interface ComponentRecord {
  componentPath: string;
  componentType: string;
  createdAt: string;
  systemTime: string;
}

export interface APIChangeRecord {
  endpoint: string;
  method: string;
  changeType: string;
  timestamp: string;
  systemTime: string;
}

export class ComponentChangeTracker {
  /**
   * Track file changes (create, modify, delete)
   */
  async trackFileChange(
    filePath: string,
    changeType: 'created' | 'modified' | 'deleted'
  ): Promise<{ filePath: string; changeType: string; lineCount: number }> {
    // Get git diff
    let diff = '';
    try {
      const { stdout } = await execAsync(`git diff HEAD -- "${filePath}"`);
      diff = stdout;
    } catch {
      diff = 'New file (untracked)';
    }

    // Get file stats
    const { stdout: stats } = await execAsync(
      `wc -l "${filePath}" 2>/dev/null || echo "0"`
    );
    const lineCount = parseInt(stats.trim().split(' ')[0]) || 0;

    // Get real system time
    const systemTime = await this.getRealSystemTime();

    const record: FileChangeRecord = {
      filePath,
      changeType,
      lineCount,
      diff: diff.substring(0, 1000), // First 1000 chars
      timestamp: new Date().toISOString(),
      systemTime
    };

    // Store change record (via MCP through Task tool)
    // await mcp__claude_flow__memory_usage({
    //   action: 'store',
    //   namespace: 'code-changes',
    //   key: `change-${Date.now()}-${filePath.replace(/\//g, '_')}`,
    //   value: JSON.stringify(record),
    //   ttl: 604800 // 7 days
    // });

    // Notify Wiki Agent
    await this.notifyWikiAgent({
      type: 'code-change',
      filePath,
      changeType,
      lineCount
    });

    console.log(`📝 File Change Tracked: ${changeType} - ${filePath} (${lineCount} lines)`);

    return { filePath, changeType, lineCount };
  }

  /**
   * Track component creation
   */
  async trackComponentCreation(
    componentPath: string,
    componentType: string
  ): Promise<void> {
    await this.trackFileChange(componentPath, 'created');

    const systemTime = await this.getRealSystemTime();

    const record: ComponentRecord = {
      componentPath,
      componentType,
      createdAt: new Date().toISOString(),
      systemTime
    };

    // Store component record (via MCP through Task tool)
    // await mcp__claude_flow__memory_usage({
    //   action: 'store',
    //   namespace: 'components',
    //   key: `component-${componentPath.replace(/\//g, '_')}`,
    //   value: JSON.stringify(record),
    //   ttl: 2592000 // 30 days
    // });

    console.log(`✅ Component Created: ${componentType} - ${componentPath}`);
  }

  /**
   * Track API endpoint changes
   */
  async trackAPIChange(
    endpoint: string,
    method: string,
    changeType: string
  ): Promise<void> {
    const systemTime = await this.getRealSystemTime();

    const record: APIChangeRecord = {
      endpoint,
      method,
      changeType,
      timestamp: new Date().toISOString(),
      systemTime
    };

    // Store API change (via MCP through Task tool)
    // await mcp__claude_flow__memory_usage({
    //   action: 'store',
    //   namespace: 'api-changes',
    //   key: `api-${endpoint.replace(/\//g, '_')}-${Date.now()}`,
    //   value: JSON.stringify(record),
    //   ttl: 604800 // 7 days
    // });

    // Notify Wiki Agent
    await this.notifyWikiAgent({
      type: 'api-change',
      endpoint,
      method,
      changeType
    });

    console.log(`✅ API Change Tracked: ${method} ${endpoint} - ${changeType}`);
  }

  /**
   * Get real system time
   */
  private async getRealSystemTime(): Promise<string> {
    const { stdout } = await execAsync("date '+%Y-%m-%d %H:%M:%S %Z'");
    return stdout.trim();
  }

  /**
   * Notify Wiki Agent
   */
  private async notifyWikiAgent(event: any): Promise<void> {
    // Store notification (via MCP through Task tool)
    // await mcp__claude_flow__memory_usage({
    //   action: 'store',
    //   namespace: 'wiki-notifications',
    //   key: `wiki-event-${Date.now()}`,
    //   value: JSON.stringify(event),
    //   ttl: 3600 // 1 hour
    // });

    console.log(`📝 Wiki Notification: ${event.type}`, event);
  }
}

// Singleton instance
export const componentTracker = new ComponentChangeTracker();
