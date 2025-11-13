/**
 * GAP-003 Query Control System - Type Definitions
 * Core types for state management, queries, and coordination
 */

export enum QueryState {
  INIT = 'INIT',
  RUNNING = 'RUNNING',
  PAUSED = 'PAUSED',
  COMPLETED = 'COMPLETED',
  TERMINATED = 'TERMINATED',
  ERROR = 'ERROR'
}

export enum ModelType {
  SONNET = 'claude-sonnet-4-5-20250929',
  HAIKU = 'claude-3-5-haiku-20241022',
  OPUS = 'claude-3-opus-20240229'
}

export enum PermissionMode {
  DEFAULT = 'default',
  ACCEPT_EDITS = 'acceptEdits',
  BYPASS_PERMISSIONS = 'bypassPermissions',
  PLAN = 'plan'
}

export interface QueryContext {
  queryId: string;
  state?: QueryState;
  metadata: Record<string, any>;
  timestamp: number;
  execution?: ExecutionContext;
  model?: ModelConfig;
  error?: Error;
}

export interface ExecutionContext {
  agentStates: Map<string, any>;
  taskQueue: Task[];
  completedTasks: Task[];
  dependencies?: DependencyGraph;
  resources?: ResourceAllocation;
}

export interface ModelConfig {
  currentModel: ModelType;
  permissionMode: PermissionMode;
  configuration: Record<string, any>;
}

export interface Task {
  id: string;
  type: string;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  dependencies?: string[];
}

export interface DependencyGraph {
  nodes: Map<string, Task>;
  edges: Map<string, string[]>;
}

export interface ResourceAllocation {
  cpuPercent: number;
  memoryMB: number;
  agentCount: number;
}

export interface StateTransition {
  from: QueryState;
  to: QueryState;
  action: string;
  guard?: (context: QueryContext) => boolean;
  effect?: (context: QueryContext) => Promise<void>;
}

export interface QueryMetadata {
  queryId: string;
  state: QueryState;
  model: ModelType;
  permissionMode: PermissionMode;
  startTime: number;
  lastUpdate: number;
  agentCount: number;
  taskCount: number;
  checkpointCount: number;
}

export interface MCPConfig {
  claudeFlowEnabled: boolean;
  ruvSwarmEnabled: boolean;
  qdrantEnabled: boolean;
  memoryNamespace: string;
  swarmTopology: 'mesh' | 'hierarchical' | 'ring' | 'star';
}
