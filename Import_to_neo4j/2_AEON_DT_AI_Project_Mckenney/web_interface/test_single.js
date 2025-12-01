const { QueryControlService } = require('./lib/query-control/query-control-service');
const { getCheckpointManager } = require('./lib/query-control/checkpoint/checkpoint-manager');
const { QueryStateMachine, QueryState } = require('./lib/query-control/state/state-machine');
const { getQueryRegistry } = require('./lib/query-control/registry/query-registry');

async function test() {
  const service = new QueryControlService();
  const queryId = 'test-001';
  
  await getCheckpointManager().clear();
  await getQueryRegistry().clear();
  
  const modelConfig = {
    model: 'claude-3-5-sonnet-20241022',
    temperature: 0.7,
    maxTokens: 4000,
    permissionMode: 'default',
    preferences: {}
  };
  
  await getQueryRegistry().registerQuery(queryId, {
    state: QueryState.INIT,
    model: modelConfig.model,
    permissionMode: modelConfig.permissionMode,
    startTime: Date.now(),
    agentCount: 2,
    taskCount: 3,
    checkpointCount: 0
  });
  
  const stateMachine = new QueryStateMachine(queryId);
  await stateMachine.transition('START');
  await stateMachine.transition('PAUSE');
  service.stateMachines.set(queryId, stateMachine);
  
  const context = {
    queryId,
    metadata: {
      state: QueryState.PAUSED,
      taskQueue: [],
      agentStates: {},
      resources: {},
      variables: {}
    },
    timestamp: Date.now(),
    agentCount: 0,
    taskCount: 0
  };
  
  const checkpoint = await getCheckpointManager().createCheckpoint(queryId, context, modelConfig, 'user_pause');
  console.log('Checkpoint created:', checkpoint.queryId, checkpoint.timestamp);
  
  const result = await service.resume(queryId);
  console.log('Resume result:', result);
}

test().catch(console.error);
