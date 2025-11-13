# GAP-003 Query Control System - User Guide

## Overview

The Query Control System provides real-time control over Claude Code query execution with capabilities for pause/resume, model switching, permission management, and runtime command execution.

## Quick Start

```typescript
import {
  QueryStateMachine,
  QueryRegistry,
  CheckpointManager,
  ResumeManager,
  ModelSwitcher,
  PermissionManager,
  CommandExecutor,
  QueryState,
  ModelType,
  PermissionMode
} from './lib/query-control';

// Initialize system
const queryId = 'my-query-001';
const stateMachine = new QueryStateMachine(queryId);
const queryRegistry = new QueryRegistry();
const checkpointManager = new CheckpointManager();
const resumeManager = new ResumeManager(checkpointManager);
const modelSwitcher = new ModelSwitcher();
const permissionManager = new PermissionManager();
const commandExecutor = new CommandExecutor();

// Register query
await queryRegistry.registerQuery(queryId, {
  userId: 'user-123',
  projectId: 'project-456'
});

// Start query
await stateMachine.transition('START');
```

## Core Features

### 1. Query State Management

Control query execution flow with six distinct states:

```typescript
// Start query
await stateMachine.transition('START');
console.log(stateMachine.getState()); // 'RUNNING'

// Pause query
await stateMachine.transition('PAUSE');
console.log(stateMachine.getState()); // 'PAUSED'

// Resume query
await stateMachine.transition('RESUME');
console.log(stateMachine.getState()); // 'RUNNING'

// Complete query
await stateMachine.transition('COMPLETE');
console.log(stateMachine.getState()); // 'COMPLETED'

// Terminate query
await stateMachine.transition('TERMINATE');
console.log(stateMachine.getState()); // 'TERMINATED'

// Handle errors
await stateMachine.transition('ERROR');
console.log(stateMachine.getState()); // 'ERROR'
```

**State Diagram:**
```
INIT → START → RUNNING
         ↓        ↓
       PAUSE ← RESUME
         ↓        ↓
    COMPLETED  TERMINATED
         ↓
       ERROR
```

### 2. Checkpoint and Resume

Save and restore query execution state:

```typescript
// Create checkpoint (target: <150ms)
const context = stateMachine.getContext();
const checkpoint = await checkpointManager.createCheckpoint(
  queryId,
  context,
  'user_pause' // reason
);

console.log(`Checkpoint created: ${checkpoint.metadata.size} bytes`);

// Retrieve checkpoint (target: <100ms)
const retrieved = await checkpointManager.retrieveCheckpoint(queryId);
console.log(`Retrieved checkpoint for query: ${retrieved.queryId}`);

// Resume from checkpoint (target: <300ms)
const resumeResult = await resumeManager.resumeQuery(queryId);
console.log(`Resumed successfully: ${resumeResult.success}`);
console.log(`Resume duration: ${resumeResult.duration}ms`);

// Validate checkpoint before resuming
const validation = await resumeManager.validateCheckpoint(queryId);
if (validation.valid) {
  await resumeManager.resumeQuery(queryId);
} else {
  console.error('Checkpoint validation failed:', validation.issues);
}
```

**Checkpoint Features:**
- **L1 Cache**: MCP memory (2-15ms, 7-day TTL)
- **L2 Storage**: Qdrant vector database (50-150ms, unlimited retention)
- **384-dimensional embeddings**: Semantic similarity search
- **Automatic promotion**: L2 hits promoted to L1 cache

### 3. Model Switching

Switch between Claude models dynamically:

```typescript
// Switch to Haiku for speed (target: <200ms)
const switchResult = await modelSwitcher.switchModel(
  queryId,
  ModelType.HAIKU,
  stateMachine
);

console.log(`Switched to: ${switchResult.currentModel}`);
console.log(`Switch time: ${switchResult.switchTimeMs}ms`);
console.log(`Checkpoint created: ${switchResult.checkpointCreated}`);

// Get model recommendation
const recommendation = await modelRegistry.recommendModel('complex analysis task');
console.log(`Recommended model: ${recommendation.model}`);
console.log(`Confidence: ${Math.round(recommendation.confidence * 100)}%`);
console.log(`Reasoning: ${recommendation.reasoning}`);

// Switch to optimal model automatically
const optimalResult = await modelSwitcher.switchToOptimalModel(
  queryId,
  'quick data extraction',
  stateMachine
);

// Get model capabilities
const capabilities = modelRegistry.getCapabilities(ModelType.SONNET);
console.log(`Max tokens: ${capabilities.maxTokens}`);
console.log(`Context window: ${capabilities.contextWindow}`);
console.log(`Strengths: ${capabilities.strengthAreas.join(', ')}`);
```

**Available Models:**

| Model | Max Tokens | Latency | Strengths | Best For |
|-------|-----------|---------|-----------|----------|
| **Sonnet** | 8192 | 1500ms | Reasoning, coding, analysis | Code generation, technical analysis |
| **Haiku** | 4096 | 500ms | Speed, efficiency | Simple queries, data extraction |
| **Opus** | 4096 | 3000ms | Creativity, nuance | Complex problems, strategic planning |

### 4. Permission Management

Control execution permissions dynamically:

```typescript
// Switch to ACCEPT_EDITS mode (target: <50ms)
const permResult = await permissionManager.switchMode(
  queryId,
  PermissionMode.ACCEPT_EDITS
);

console.log(`Permission mode: ${permResult.currentMode}`);
console.log(`Switch time: ${permResult.switchTimeMs}ms`);

// Get mode capabilities
const capabilities = permissionManager.getModeCapabilities(
  PermissionMode.ACCEPT_EDITS
);

console.log(`Auto-approve edits: ${capabilities.autoApproveEdits}`);
console.log(`Bypass confirmation: ${capabilities.bypassUserConfirmation}`);
console.log(`Planning mode: ${capabilities.planningMode}`);
console.log(`Editing allowed: ${capabilities.editingAllowed}`);

// Get current mode
const currentMode = permissionManager.getCurrentMode();
console.log(`Current mode: ${currentMode}`);
```

**Permission Modes:**

| Mode | Auto-Approve | Bypass Confirmation | Planning | Editing |
|------|-------------|-------------------|----------|---------|
| **DEFAULT** | ❌ | ❌ | ❌ | ✅ |
| **ACCEPT_EDITS** | ✅ | ❌ | ❌ | ✅ |
| **BYPASS_PERMISSIONS** | ✅ | ✅ | ❌ | ✅ |
| **PLAN** | ❌ | ❌ | ✅ | ❌ |

### 5. Command Execution

Execute runtime commands with security validation:

```typescript
// Execute safe command
const cmdResult = await commandExecutor.executeCommand(
  queryId,
  'echo "Hello World"'
);

if (cmdResult.success) {
  console.log(`Output: ${cmdResult.output}`);
  console.log(`Execution time: ${cmdResult.executionTimeMs}ms`);
} else if (cmdResult.blocked) {
  console.error(`Command blocked: ${cmdResult.blockReason}`);
} else {
  console.error(`Command failed: ${cmdResult.error}`);
}

// Validate command security before execution
const securityCheck = commandExecutor.validateCommandSecurity('rm -rf /');
if (!securityCheck.safe) {
  console.error(`Dangerous command: ${securityCheck.reason}`);
}

// Check if command is blacklisted
const isBlacklisted = commandExecutor.isCommandBlacklisted('dd if=/dev/zero');
console.log(`Blacklisted: ${isBlacklisted}`);

// Get security blacklist
const blacklist = commandExecutor.getBlacklist();
console.log(`Dangerous patterns: ${blacklist.join(', ')}`);
```

**Security Blacklist:**
- `rm -rf` - Recursive deletion
- `dd if=` - Direct disk writes
- `mkfs` - Filesystem formatting
- `:(){:|:&};:` - Fork bombs
- `sudo rm` - Elevated deletion
- `/etc/passwd`, `/etc/shadow` - System file access
- `> /dev/sd*` - Block device writes

## Complete Workflow Example

```typescript
async function completeQueryWorkflow() {
  const queryId = 'workflow-001';

  // 1. Initialize system
  const stateMachine = new QueryStateMachine(queryId);
  const queryRegistry = new QueryRegistry();
  const checkpointManager = new CheckpointManager();
  const resumeManager = new ResumeManager(checkpointManager);
  const modelSwitcher = new ModelSwitcher();
  const permissionManager = new PermissionManager();
  const commandExecutor = new CommandExecutor();

  await checkpointManager.initialize();

  // 2. Register and start query
  await queryRegistry.registerQuery(queryId, {
    userId: 'user-001',
    projectId: 'project-001'
  });
  await stateMachine.transition('START');

  // 3. Switch to optimal model
  const recommendation = await modelRegistry.recommendModel('code analysis');
  if (recommendation.model !== ModelType.SONNET) {
    await modelSwitcher.switchModel(queryId, recommendation.model, stateMachine);
  }

  // 4. Configure permissions
  await permissionManager.switchMode(queryId, PermissionMode.ACCEPT_EDITS);

  // 5. Execute commands
  const cmd1 = await commandExecutor.executeCommand(queryId, 'echo "Step 1"');
  console.log(`Command 1: ${cmd1.success ? 'success' : 'failed'}`);

  // 6. Pause and checkpoint
  await stateMachine.transition('PAUSE');
  const checkpoint = await checkpointManager.createCheckpoint(
    queryId,
    stateMachine.getContext(),
    'workflow_checkpoint'
  );
  console.log(`Checkpoint created: ${checkpoint.metadata.size} bytes`);

  // 7. Resume and continue
  await resumeManager.resumeQuery(queryId);
  await stateMachine.transition('RESUME');

  // 8. Complete workflow
  await stateMachine.transition('COMPLETE');

  // 9. Collect statistics
  const modelStats = modelSwitcher.getStatistics();
  const permStats = permissionManager.getStatistics();
  const cmdStats = commandExecutor.getStatistics();

  console.log(`Model: ${modelStats.currentModel}`);
  console.log(`Permission switches: ${permStats.totalSwitches}`);
  console.log(`Commands executed: ${cmdStats.totalCommands}`);
}
```

## Performance Targets

| Operation | Target | Acceptable | Notes |
|-----------|--------|-----------|-------|
| State transition | <100ms | <200ms | Fast state changes |
| Model switch | <200ms | <500ms | Includes checkpoint |
| Permission switch | <50ms | <100ms | Minimal overhead |
| Checkpoint create | <150ms | <300ms | L1+L2 write |
| Checkpoint retrieve | <100ms | <200ms | L1 preferred |
| Query resume | <300ms | <500ms | Full restoration |

## Error Handling

```typescript
try {
  await stateMachine.transition('START');
} catch (error) {
  console.error('State transition failed:', error);

  // Check current state
  const currentState = stateMachine.getState();
  if (currentState === QueryState.ERROR) {
    // Recover from checkpoint
    const checkpoint = await checkpointManager.retrieveCheckpoint(queryId);
    if (checkpoint) {
      await resumeManager.resumeQuery(queryId);
    }
  }
}
```

## Best Practices

1. **Always register queries** before starting execution
2. **Create checkpoints** before risky operations
3. **Validate checkpoints** before resuming
4. **Use model recommendations** for optimal performance
5. **Configure permissions** based on trust level
6. **Validate commands** before execution
7. **Monitor statistics** for performance insights
8. **Handle errors gracefully** with checkpoint recovery

## MCP Integration

All operations integrate with MCP for coordination:

```typescript
// Memory stored in MCP with TTLs
// Neural patterns trained automatically
// Checkpoints persisted in Qdrant
// Coordination via ruv-swarm and claude-flow
```

## Statistics and Monitoring

```typescript
// State machine stats
const context = stateMachine.getContext();
console.log(`Current state: ${context.state}`);
console.log(`Query ID: ${context.queryId}`);
console.log(`Timestamp: ${new Date(context.timestamp).toISOString()}`);

// Model switching stats
const modelStats = modelSwitcher.getStatistics();
console.log(`Current model: ${modelStats.currentModel}`);
console.log(`Total switches: ${modelStats.totalSwitches}`);
console.log(`Average switch time: ${modelStats.averageSwitchTime}ms`);

// Permission stats
const permStats = permissionManager.getStatistics();
console.log(`Current mode: ${permStats.currentMode}`);
console.log(`Total switches: ${permStats.totalSwitches}`);
console.log(`Average switch time: ${permStats.averageSwitchTime}ms`);
console.log(`Switch history: ${permStats.switchHistory.length} entries`);

// Command execution stats
const cmdStats = commandExecutor.getStatistics();
console.log(`Total commands: ${cmdStats.totalCommands}`);
console.log(`Successful: ${cmdStats.successfulCommands}`);
console.log(`Failed: ${cmdStats.failedCommands}`);
console.log(`Average execution time: ${cmdStats.averageExecutionTime}ms`);

// Checkpoint stats
const checkpointStats = await checkpointManager.getStatistics();
console.log(`Total checkpoints: ${checkpointStats.totalCheckpoints}`);
console.log(`L2 status: ${checkpointStats.l2Status}`);

// Resume stats
const resumeStats = resumeManager.getStatistics();
console.log(`Successful resumes: ${resumeStats.successfulResumes}`);
console.log(`Failed resumes: ${resumeStats.failedResumes}`);
console.log(`Average duration: ${resumeStats.averageDuration}ms`);
```

## Troubleshooting

### Common Issues

**Q: Checkpoint retrieval is slow**
A: Check if L1 cache is being used. L2 fallback is slower (50-150ms vs 2-15ms).

**Q: Model switch failed**
A: Verify the target model is valid and MCP connection is active.

**Q: Permission switch rejected**
A: Check if the current state allows permission changes.

**Q: Command execution blocked**
A: Review security blacklist and validate command safety.

### Debug Mode

Enable verbose logging for troubleshooting:

```typescript
// All operations log to console
// Check console output for detailed information
// Neural training accuracy shown in logs
// Performance warnings logged when targets exceeded
```

## Next Steps

- Explore the [API Reference](./API_REFERENCE.md) for detailed API documentation
- Review [Architecture Documentation](./ARCHITECTURE.md) for system design
- Check [Performance Report](./PERFORMANCE_REPORT.md) for benchmarks
- Run E2E tests: `npm test -- tests/query-control/e2e`
