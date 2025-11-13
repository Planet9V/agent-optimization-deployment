# GAP-003 Query Control System - API Reference

## Core Types

### QueryState
```typescript
enum QueryState {
  INIT = 'INIT',
  RUNNING = 'RUNNING',
  PAUSED = 'PAUSED',
  COMPLETED = 'COMPLETED',
  TERMINATED = 'TERMINATED',
  ERROR = 'ERROR'
}
```

### ModelType
```typescript
enum ModelType {
  SONNET = 'claude-sonnet-4-5-20250929',
  HAIKU = 'claude-3-5-haiku-20241022',
  OPUS = 'claude-3-opus-20240229'
}
```

### PermissionMode
```typescript
enum PermissionMode {
  DEFAULT = 'default',
  ACCEPT_EDITS = 'acceptEdits',
  BYPASS_PERMISSIONS = 'bypassPermissions',
  PLAN = 'plan'
}
```

### QueryContext
```typescript
interface QueryContext {
  queryId: string;
  state: QueryState;
  metadata?: Record<string, any>;
  timestamp: number;
  execution?: ExecutionContext;
  model?: ModelConfig;
}
```

## State Machine

### QueryStateMachine

**Constructor:**
```typescript
constructor(queryId: string, initialState?: QueryState)
```

**Methods:**

#### transition(action: string): Promise<boolean>
Execute a state transition.

**Parameters:**
- `action: string` - Transition action ('START', 'PAUSE', 'RESUME', 'COMPLETE', 'TERMINATE', 'ERROR')

**Returns:** `Promise<boolean>` - Success status

**Example:**
```typescript
await stateMachine.transition('START');
```

#### getState(): QueryState
Get current state.

**Returns:** `QueryState` - Current state

#### getContext(): QueryContext
Get current context.

**Returns:** `QueryContext` - Context object

#### updateContext(partial: Partial<QueryContext>): void
Update context.

**Parameters:**
- `partial: Partial<QueryContext>` - Context updates

---

## Checkpoint System

### CheckpointManager

**Methods:**

#### initialize(): Promise<void>
Initialize checkpoint system.

**Returns:** `Promise<void>`

#### createCheckpoint(queryId: string, context: QueryContext, reason?: string): Promise<Checkpoint>
Create a new checkpoint.

**Parameters:**
- `queryId: string` - Query identifier
- `context: QueryContext` - Current context
- `reason?: string` - Checkpoint reason (default: 'user_pause')

**Returns:** `Promise<Checkpoint>` - Created checkpoint

**Performance:** Target <150ms, Acceptable <300ms

**Example:**
```typescript
const checkpoint = await checkpointManager.createCheckpoint(
  queryId,
  context,
  'before_risky_operation'
);
```

#### retrieveCheckpoint(queryId: string): Promise<Checkpoint | null>
Retrieve a checkpoint.

**Parameters:**
- `queryId: string` - Query identifier

**Returns:** `Promise<Checkpoint | null>` - Checkpoint or null if not found

**Performance:** Target <100ms (L1), <200ms (L2)

#### getStatistics(): Promise<CheckpointStatistics>
Get checkpoint statistics.

**Returns:** `Promise<CheckpointStatistics>` - Statistics

### ResumeManager

**Constructor:**
```typescript
constructor(checkpointManager: CheckpointManager)
```

**Methods:**

#### resumeQuery(queryId: string): Promise<ResumeResult>
Resume query from checkpoint.

**Parameters:**
- `queryId: string` - Query identifier

**Returns:** `Promise<ResumeResult>` - Resume result with success status and duration

**Performance:** Target <300ms, Acceptable <500ms

**Throws:** Error if no checkpoint found

**Example:**
```typescript
const result = await resumeManager.resumeQuery(queryId);
console.log(`Resumed in ${result.duration}ms`);
```

#### validateCheckpoint(queryId: string): Promise<ValidationResult>
Validate checkpoint before resuming.

**Parameters:**
- `queryId: string` - Query identifier

**Returns:** `Promise<ValidationResult>` - Validation result with issues list

#### getStatistics(): ResumeStatistics
Get resume statistics.

**Returns:** `ResumeStatistics` - Statistics

---

## Model System

### ModelRegistry

**Methods:**

#### getCapabilities(model: ModelType): ModelCapabilities
Get model capabilities.

**Parameters:**
- `model: ModelType` - Model type

**Returns:** `ModelCapabilities` - Capabilities object

**Example:**
```typescript
const caps = modelRegistry.getCapabilities(ModelType.SONNET);
console.log(`Max tokens: ${caps.maxTokens}`);
```

#### recommendModel(taskType: string): Promise<ModelRecommendation>
Recommend model for task type.

**Parameters:**
- `taskType: string` - Task description

**Returns:** `Promise<ModelRecommendation>` - Recommendation with model, confidence, and reasoning

**Example:**
```typescript
const rec = await modelRegistry.recommendModel('complex analysis');
console.log(`Recommended: ${rec.model} (${rec.confidence})`);
```

#### compareModels(useCase: string): ModelComparison[]
Compare models for use case.

**Parameters:**
- `useCase: string` - Use case description

**Returns:** `ModelComparison[]` - Comparison array sorted by score

#### getAllModels(): ModelType[]
Get all registered models.

**Returns:** `ModelType[]` - Model list

#### isValidModel(model: string): model is ModelType
Validate model type.

**Parameters:**
- `model: string` - Model identifier

**Returns:** `boolean` - True if valid

### ModelSwitcher

**Constructor:**
```typescript
constructor(registry?: ModelRegistry, checkpointManager?: CheckpointManager)
```

**Methods:**

#### switchModel(queryId: string, targetModel: ModelType, stateMachine: QueryStateMachine): Promise<ModelSwitchResult>
Switch to a different model.

**Parameters:**
- `queryId: string` - Query identifier
- `targetModel: ModelType` - Target model
- `stateMachine: QueryStateMachine` - State machine instance

**Returns:** `Promise<ModelSwitchResult>` - Switch result with timing

**Performance:** Target <200ms, Acceptable <500ms

**Example:**
```typescript
const result = await modelSwitcher.switchModel(
  queryId,
  ModelType.HAIKU,
  stateMachine
);
console.log(`Switched in ${result.switchTimeMs}ms`);
```

#### switchToOptimalModel(queryId: string, taskType: string, stateMachine: QueryStateMachine): Promise<ModelSwitchResult>
Switch to optimal model for task.

**Parameters:**
- `queryId: string` - Query identifier
- `taskType: string` - Task description
- `stateMachine: QueryStateMachine` - State machine instance

**Returns:** `Promise<ModelSwitchResult>` - Switch result

#### getCurrentModel(): ModelType
Get current model.

**Returns:** `ModelType` - Current model

#### setCurrentModel(model: ModelType): void
Set current model.

**Parameters:**
- `model: ModelType` - Model to set

#### getStatistics(): ModelStatistics
Get switch statistics.

**Returns:** `ModelStatistics` - Statistics

---

## Permission System

### PermissionManager

**Methods:**

#### switchMode(queryId: string, targetMode: PermissionMode): Promise<PermissionSwitchResult>
Switch permission mode.

**Parameters:**
- `queryId: string` - Query identifier
- `targetMode: PermissionMode` - Target permission mode

**Returns:** `Promise<PermissionSwitchResult>` - Switch result with timing

**Performance:** Target <50ms, Acceptable <100ms

**Example:**
```typescript
const result = await permissionManager.switchMode(
  queryId,
  PermissionMode.ACCEPT_EDITS
);
console.log(`Switched in ${result.switchTimeMs}ms`);
```

#### getCurrentMode(): PermissionMode
Get current permission mode.

**Returns:** `PermissionMode` - Current mode

#### setCurrentMode(mode: PermissionMode): void
Set current mode.

**Parameters:**
- `mode: PermissionMode` - Mode to set

#### getModeCapabilities(mode: PermissionMode): PermissionCapabilities
Get capabilities for mode.

**Parameters:**
- `mode: PermissionMode` - Permission mode

**Returns:** `PermissionCapabilities` - Capabilities object

**Example:**
```typescript
const caps = permissionManager.getModeCapabilities(
  PermissionMode.PLAN
);
console.log(`Editing allowed: ${caps.editingAllowed}`);
```

#### isValidMode(mode: string): mode is PermissionMode
Validate permission mode.

**Parameters:**
- `mode: string` - Mode identifier

**Returns:** `boolean` - True if valid

#### getStatistics(): PermissionStatistics
Get switch statistics.

**Returns:** `PermissionStatistics` - Statistics with history

#### clearHistory(): void
Clear switch history.

---

## Command Execution

### CommandExecutor

**Methods:**

#### executeCommand(queryId: string, command: string): Promise<CommandExecutionResult>
Execute a runtime command with security validation.

**Parameters:**
- `queryId: string` - Query identifier
- `command: string` - Command to execute

**Returns:** `Promise<CommandExecutionResult>` - Execution result

**Example:**
```typescript
const result = await commandExecutor.executeCommand(
  queryId,
  'echo "test"'
);

if (result.blocked) {
  console.error(`Blocked: ${result.blockReason}`);
} else if (result.success) {
  console.log(`Output: ${result.output}`);
}
```

#### validateCommandSecurity(command: string): SecurityCheckResult
Validate command security.

**Parameters:**
- `command: string` - Command to validate

**Returns:** `SecurityCheckResult` - Security check with reason

**Example:**
```typescript
const check = commandExecutor.validateCommandSecurity('rm -rf /');
if (!check.safe) {
  console.error(check.reason);
}
```

#### isCommandBlacklisted(command: string): boolean
Check if command is blacklisted.

**Parameters:**
- `command: string` - Command to check

**Returns:** `boolean` - True if blacklisted

#### getBlacklist(): string[]
Get security blacklist.

**Returns:** `string[]` - Dangerous command patterns

#### getStatistics(): CommandStatistics
Get execution statistics.

**Returns:** `CommandStatistics` - Statistics with history

#### clearHistory(): void
Clear command history.

---

## Query Registry

### QueryRegistry

**Methods:**

#### registerQuery(queryId: string, metadata: Partial<QueryMetadata>): Promise<void>
Register a new query.

**Parameters:**
- `queryId: string` - Query identifier
- `metadata: Partial<QueryMetadata>` - Query metadata

**Returns:** `Promise<void>`

**Example:**
```typescript
await queryRegistry.registerQuery(queryId, {
  userId: 'user-123',
  projectId: 'project-456'
});
```

#### getQuery(queryId: string): Promise<QueryMetadata | null>
Get query metadata.

**Parameters:**
- `queryId: string` - Query identifier

**Returns:** `Promise<QueryMetadata | null>` - Metadata or null

#### updateQuery(queryId: string, updates: Partial<QueryMetadata>): Promise<void>
Update query metadata.

**Parameters:**
- `queryId: string` - Query identifier
- `updates: Partial<QueryMetadata>` - Metadata updates

**Returns:** `Promise<void>`

#### deleteQuery(queryId: string): Promise<void>
Delete query.

**Parameters:**
- `queryId: string` - Query identifier

**Returns:** `Promise<void>`

#### listQueries(filters?: QueryFilters): Promise<QueryMetadata[]>
List queries with filters.

**Parameters:**
- `filters?: QueryFilters` - Optional filters

**Returns:** `Promise<QueryMetadata[]>` - Query list

#### getStatistics(): QueryRegistryStatistics
Get registry statistics.

**Returns:** `QueryRegistryStatistics` - Statistics

---

## MCP Integration

### MCPClient

**Methods:**

#### storeMemory(key: string, value: any, ttl?: number): Promise<boolean>
Store data in MCP memory.

**Parameters:**
- `key: string` - Memory key
- `value: any` - Value to store
- `ttl?: number` - Time-to-live in seconds (optional)

**Returns:** `Promise<boolean>` - Success status

#### retrieveMemory(key: string): Promise<any | null>
Retrieve data from MCP memory.

**Parameters:**
- `key: string` - Memory key

**Returns:** `Promise<any | null>` - Stored value or null

#### trainNeuralPattern(patternType: 'coordination' | 'optimization' | 'prediction', trainingData: string, epochs?: number): Promise<TrainingResult>
Train neural pattern.

**Parameters:**
- `patternType: 'coordination' | 'optimization' | 'prediction'` - Pattern type
- `trainingData: string` - Training data
- `epochs?: number` - Training epochs (default: 20)

**Returns:** `Promise<TrainingResult>` - Training result with accuracy

#### queryControl(params: QueryControlParams): Promise<any>
Execute query control operation.

**Parameters:**
- `params: QueryControlParams` - Control parameters

**Returns:** `Promise<any>` - Operation result

#### createSnapshot(snapshotId: string, state: any): Promise<boolean>
Create state snapshot.

**Parameters:**
- `snapshotId: string` - Snapshot identifier
- `state: any` - State to snapshot

**Returns:** `Promise<boolean>` - Success status

#### restoreContext(contextId: string): Promise<any>
Restore execution context.

**Parameters:**
- `contextId: string` - Context identifier

**Returns:** `Promise<any>` - Restored context

---

## Type Definitions

### Checkpoint
```typescript
interface Checkpoint {
  queryId: string;
  timestamp: number;
  state: QueryState;
  executionContext: ExecutionContext;
  modelConfig: ModelConfig;
  embedding: number[];
  metadata: CheckpointMetadata;
}
```

### ModelCapabilities
```typescript
interface ModelCapabilities {
  maxTokens: number;
  contextWindow: number;
  costPer1kTokens: number;
  latencyMs: number;
  strengthAreas: string[];
  recommendedFor: string[];
}
```

### PermissionCapabilities
```typescript
interface PermissionCapabilities {
  autoApproveEdits: boolean;
  bypassUserConfirmation: boolean;
  planningMode: boolean;
  editingAllowed: boolean;
}
```

### CommandExecutionResult
```typescript
interface CommandExecutionResult {
  success: boolean;
  command: string;
  output?: string;
  error?: string;
  executionTimeMs: number;
  blocked?: boolean;
  blockReason?: string;
}
```

---

## Error Handling

All API methods may throw errors:

```typescript
try {
  await stateMachine.transition('INVALID_ACTION');
} catch (error) {
  console.error('Operation failed:', error.message);
}
```

Common error scenarios:
- **Invalid state transitions**: Attempting invalid state changes
- **Missing checkpoints**: Resuming without checkpoint
- **Invalid models**: Switching to non-existent models
- **Security violations**: Executing dangerous commands
- **MCP connection**: MCP server unavailable

---

## Performance Considerations

1. **Checkpoint operations** use L1+L2 caching for optimal performance
2. **Model switches** create automatic safety checkpoints
3. **Permission switches** are lightweight (<50ms target)
4. **Command validation** happens before execution (no overhead for safe commands)
5. **Neural training** runs asynchronously (non-blocking)

---

## Best Practices

1. Always initialize `CheckpointManager` before use
2. Validate checkpoints before resuming
3. Use model recommendations for optimal selection
4. Configure permissions based on trust level
5. Validate commands before execution
6. Monitor statistics for performance insights
7. Handle errors gracefully with try-catch
8. Clean up resources (clear histories periodically)
