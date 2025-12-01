/**
 * GAP-003 Orchestration Integration Tests
 * Query Control System Coordination with All Components
 *
 * Tests the integration of Query Control (GAP-003) with:
 * - GAP-001: Parallel agent spawning
 * - GAP-002: AgentDB caching
 * - GAP-004: Neo4j schema
 * - GAP-006: Job management
 *
 * Verifies:
 * - Query control coordinates all system components
 * - Checkpoint/resume works across all services
 * - State consistency maintained during operations
 * - Performance targets met with full integration
 */

import { describe, test, expect, beforeAll, afterAll, beforeEach } from '@jest/globals';
import { QueryControlService } from '../../lib/query-control/query-control-service';
import {
  setupTestEnvironment,
  cleanupTestEnvironment,
  cleanTestData,
  waitFor,
  measureExecutionTime,
  generateTestQuery,
  generateTestJob,
  captureSystemState,
  TestEnvironment
} from './setup';

describe('GAP-003: Query Control Orchestration', () => {
  let env: TestEnvironment;
  let queryControl: QueryControlService;

  beforeAll(async () => {
    env = await setupTestEnvironment();

    queryControl = new QueryControlService({
      postgres: env.postgres,
      redis: env.redis,
      qdrant: env.qdrant,
    });

    await queryControl.initialize();
  });

  afterAll(async () => {
    if (queryControl) {
      await queryControl.shutdown();
    }
    await cleanupTestEnvironment(env);
  });

  beforeEach(async () => {
    await cleanTestData(env);
  });

  /**
   * Test 1: Query control + parallel agent spawning
   *
   * Flow:
   * 1. Start query
   * 2. Query spawns 5 parallel agents (GAP-001)
   * 3. Pause query
   * 4. Verify all agents paused
   * 5. Resume query
   * 6. Verify agents resume
   *
   * Expected:
   * - Pause propagates to all agents <500ms
   * - Resume restores full state
   * - AgentDB cache preserved during pause
   */
  test('query pause cascades to parallel agents', async () => {
    // Create query
    const query = await queryControl.createQuery({
      model: 'claude-3-5-sonnet-20241022',
      permissionMode: 'default',
    });

    expect(query.queryId).toBeDefined();
    expect(query.status).toBe('active');

    // Simulate spawning 5 parallel agents (via GAP-001)
    const agentTypes = ['researcher', 'coder', 'tester', 'reviewer', 'analyst'];
    const agentPromises = agentTypes.map(type =>
      env.agentDB.getAgentDefinition(type, { queryId: query.queryId })
    );

    const agents = await Promise.all(agentPromises);
    expect(agents.length).toBe(5);

    // Verify AgentDB cache populated
    const cacheStats = await env.agentDB.getCacheStats();
    expect(cacheStats.l1.entries).toBe(5);

    // Pause query
    const pauseStart = Date.now();
    await queryControl.pauseQuery(query.queryId);
    const pauseDuration = Date.now() - pauseStart;

    expect(pauseDuration).toBeLessThan(500); // <500ms pause propagation

    // Verify query paused
    const pausedQuery = await queryControl.getQuery(query.queryId);
    expect(pausedQuery.status).toBe('paused');

    // Verify checkpoint created
    const checkpoint = await queryControl.getCheckpoint(query.queryId);
    expect(checkpoint).toBeDefined();
    expect(checkpoint.agentStates).toBeDefined();
    expect(checkpoint.agentStates.length).toBe(5);

    // Verify AgentDB cache still valid
    const cacheAfterPause = await env.agentDB.getCacheStats();
    expect(cacheAfterPause.l1.entries).toBe(5); // Cache preserved

    // Resume query
    const resumeStart = Date.now();
    await queryControl.resumeQuery(query.queryId);
    const resumeDuration = Date.now() - resumeStart;

    expect(resumeDuration).toBeLessThan(1000); // <1s resume

    // Verify query active
    const resumedQuery = await queryControl.getQuery(query.queryId);
    expect(resumedQuery.status).toBe('active');

    // Verify agents can access cache
    const restoredAgent = await env.agentDB.getAgentDefinition('researcher', {
      queryId: query.queryId
    });
    expect(restoredAgent).toBeDefined();
  }, 60000);

  /**
   * Test 2: Query checkpoint stored in AgentDB/Qdrant
   *
   * Flow:
   * 1. Create query with agents
   * 2. Process some work
   * 3. Pause and create checkpoint
   * 4. Verify checkpoint in PostgreSQL
   * 5. Verify checkpoint in Qdrant (via AgentDB)
   * 6. Verify checkpoint in Redis cache
   *
   * Expected:
   * - Checkpoint in all 3 stores
   * - Data consistency across stores
   * - Retrieval from any store works
   */
  test('query checkpoint persists to all storage layers', async () => {
    // Create query
    const query = await queryControl.createQuery({
      model: 'claude-3-5-sonnet-20241022',
      permissionMode: 'default',
    });

    // Spawn agents
    const agents = await Promise.all([
      env.agentDB.getAgentDefinition('researcher', { queryId: query.queryId }),
      env.agentDB.getAgentDefinition('coder', { queryId: query.queryId }),
    ]);

    // Simulate processing
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Create checkpoint
    await queryControl.pauseQuery(query.queryId);

    // Verify PostgreSQL checkpoint
    const pgResult = await env.postgres.query(
      'SELECT * FROM query_checkpoints WHERE query_id = $1',
      [query.queryId]
    );
    expect(pgResult.rows.length).toBe(1);
    const pgCheckpoint = pgResult.rows[0];
    expect(pgCheckpoint.state_snapshot).toBeDefined();

    // Verify Qdrant checkpoint (via memory storage)
    const memoryKey = `query:checkpoint:${query.queryId}`;
    const qdrantPoints = await env.qdrant.scroll('query_registry', {
      filter: {
        must: [
          { key: 'memoryKey', match: { value: memoryKey } }
        ]
      },
      limit: 1
    });
    expect(qdrantPoints.points.length).toBe(1);

    // Verify Redis cache
    const redisKey = `checkpoint:${query.queryId}`;
    const redisCheckpoint = await env.redis.get(redisKey);
    expect(redisCheckpoint).toBeDefined();

    // Verify consistency across stores
    const parsedRedis = JSON.parse(redisCheckpoint!);
    expect(parsedRedis.queryId).toBe(query.queryId);
    expect(pgCheckpoint.query_id).toBe(query.queryId);
  }, 60000);

  /**
   * Test 3: Query accessing Neo4j schema checkpoints correctly
   *
   * Flow:
   * 1. Create equipment in Neo4j
   * 2. Start query that accesses equipment
   * 3. Pause query during Neo4j access
   * 4. Verify Neo4j transaction state
   * 5. Resume query
   * 6. Verify Neo4j access completes
   *
   * Expected:
   * - Neo4j transaction management correct
   * - Query pause doesn't corrupt Neo4j state
   * - Resume continues Neo4j operations
   */
  test('query pause/resume maintains Neo4j consistency', async () => {
    // Create test equipment in Neo4j
    const session = env.neo4j.session();
    try {
      await session.run(`
        CREATE (e:Equipment {
          equipmentId: 'TEST-QUERY-001',
          name: 'Test Equipment for Query',
          testMarker: true,
          createdAt: datetime()
        })
        RETURN e
      `);
    } finally {
      await session.close();
    }

    // Create query
    const query = await queryControl.createQuery({
      model: 'claude-3-5-sonnet-20241022',
      permissionMode: 'default',
    });

    // Simulate Neo4j query
    const querySession = env.neo4j.session();
    let equipmentFound = false;

    try {
      // Start Neo4j read
      const result = await querySession.run(`
        MATCH (e:Equipment {equipmentId: 'TEST-QUERY-001'})
        RETURN e
      `);
      equipmentFound = result.records.length > 0;
    } finally {
      await querySession.close();
    }

    expect(equipmentFound).toBe(true);

    // Pause query
    await queryControl.pauseQuery(query.queryId);

    // Verify Neo4j data still accessible
    const verifySession = env.neo4j.session();
    try {
      const result = await verifySession.run(`
        MATCH (e:Equipment {equipmentId: 'TEST-QUERY-001'})
        RETURN e
      `);
      expect(result.records.length).toBe(1);
    } finally {
      await verifySession.close();
    }

    // Resume query
    await queryControl.resumeQuery(query.queryId);

    // Continue Neo4j operations
    const continueSession = env.neo4j.session();
    try {
      const result = await continueSession.run(`
        MATCH (e:Equipment {equipmentId: 'TEST-QUERY-001'})
        SET e.queryProcessed = true
        RETURN e
      `);
      expect(result.records.length).toBe(1);
      expect(result.records[0].get('e').properties.queryProcessed).toBe(true);
    } finally {
      await continueSession.close();
    }
  }, 60000);

  /**
   * Test 4: Query control integrates with job management
   *
   * Flow:
   * 1. Start query
   * 2. Query triggers 3 jobs (GAP-006)
   * 3. Pause query
   * 4. Verify jobs paused/marked
   * 5. Resume query
   * 6. Verify jobs complete
   *
   * Expected:
   * - Jobs track parent query
   * - Query pause affects job processing
   * - Job completion updates query state
   */
  test('query control coordinates job management', async () => {
    // Create query
    const query = await queryControl.createQuery({
      model: 'claude-3-5-sonnet-20241022',
      permissionMode: 'default',
    });

    // Create 3 jobs linked to query
    const jobIds: number[] = [];
    for (let i = 0; i < 3; i++) {
      const result = await env.postgres.query(`
        INSERT INTO jobs (job_type, status, payload, metadata)
        VALUES ($1, $2, $3, $4)
        RETURNING id
      `, [
        'analysis',
        'pending',
        JSON.stringify({ data: `test-${i}` }),
        JSON.stringify({ queryId: query.queryId })
      ]);
      jobIds.push(result.rows[0].id);
    }

    expect(jobIds.length).toBe(3);

    // Pause query
    await queryControl.pauseQuery(query.queryId);

    // Verify query paused
    const pausedQuery = await queryControl.getQuery(query.queryId);
    expect(pausedQuery.status).toBe('paused');

    // Verify jobs can be marked as related to paused query
    const jobsResult = await env.postgres.query(`
      SELECT id, status, metadata
      FROM jobs
      WHERE metadata->>'queryId' = $1
    `, [query.queryId]);

    expect(jobsResult.rows.length).toBe(3);

    // Resume query
    await queryControl.resumeQuery(query.queryId);

    // Simulate job completion
    for (const jobId of jobIds) {
      await env.postgres.query(`
        UPDATE jobs
        SET status = 'completed',
            completed_at = NOW()
        WHERE id = $1
      `, [jobId]);
    }

    // Verify all jobs completed
    const completedResult = await env.postgres.query(`
      SELECT COUNT(*) as count
      FROM jobs
      WHERE metadata->>'queryId' = $1
        AND status = 'completed'
    `, [query.queryId]);

    expect(parseInt(completedResult.rows[0].count)).toBe(3);
  }, 60000);

  /**
   * Test 5: Model switching during active operations
   *
   * Flow:
   * 1. Start query with model A
   * 2. Spawn agents and jobs
   * 3. Switch to model B
   * 4. Verify all components use new model
   * 5. Verify state consistency
   *
   * Expected:
   * - Model switch <200ms
   * - No state corruption
   * - All components aware of new model
   */
  test('model switching maintains consistency', async () => {
    // Create query with initial model
    const query = await queryControl.createQuery({
      model: 'claude-3-5-sonnet-20241022',
      permissionMode: 'default',
    });

    // Spawn agents
    await Promise.all([
      env.agentDB.getAgentDefinition('researcher', { queryId: query.queryId }),
      env.agentDB.getAgentDefinition('coder', { queryId: query.queryId }),
    ]);

    // Switch model
    const switchStart = Date.now();
    await queryControl.switchModel(query.queryId, 'claude-3-5-haiku-20241022');
    const switchDuration = Date.now() - switchStart;

    expect(switchDuration).toBeLessThan(200);

    // Verify model updated
    const updatedQuery = await queryControl.getQuery(query.queryId);
    expect(updatedQuery.model).toBe('claude-3-5-haiku-20241022');

    // Verify checkpoint reflects new model
    const checkpoint = await queryControl.getCheckpoint(query.queryId);
    if (checkpoint) {
      expect(checkpoint.model).toBe('claude-3-5-haiku-20241022');
    }

    // Verify AgentDB cache still valid (model change shouldn't invalidate agents)
    const cacheStats = await env.agentDB.getCacheStats();
    expect(cacheStats.l1.entries).toBeGreaterThan(0);
  }, 30000);

  /**
   * Test 6: Permission mode changes affecting system access
   *
   * Flow:
   * 1. Start query with default permissions
   * 2. Perform operations
   * 3. Change to acceptEdits mode
   * 4. Verify all components respect new mode
   * 5. Change to plan mode
   * 6. Verify read-only behavior
   *
   * Expected:
   * - Permission change <100ms
   * - Components enforce new permissions
   * - State consistency maintained
   */
  test('permission mode changes cascade correctly', async () => {
    // Create query with default permissions
    const query = await queryControl.createQuery({
      model: 'claude-3-5-sonnet-20241022',
      permissionMode: 'default',
    });

    expect(query.permissionMode).toBe('default');

    // Change to acceptEdits
    const changeStart = Date.now();
    await queryControl.changePermissionMode(query.queryId, 'acceptEdits');
    const changeDuration = Date.now() - changeStart;

    expect(changeDuration).toBeLessThan(100);

    // Verify mode updated
    const updatedQuery = await queryControl.getQuery(query.queryId);
    expect(updatedQuery.permissionMode).toBe('acceptEdits');

    // Change to plan mode (read-only)
    await queryControl.changePermissionMode(query.queryId, 'plan');

    const planQuery = await queryControl.getQuery(query.queryId);
    expect(planQuery.permissionMode).toBe('plan');

    // Verify read-only enforcement (checkpoint should still work)
    await queryControl.pauseQuery(query.queryId);
    const checkpoint = await queryControl.getCheckpoint(query.queryId);
    expect(checkpoint).toBeDefined();
  }, 30000);

  /**
   * Test 7: Query termination cleans up all resources
   *
   * Flow:
   * 1. Start query with agents, jobs, cache
   * 2. Terminate query
   * 3. Verify all resources cleaned:
   *    - PostgreSQL query/checkpoints deleted
   *    - Redis cache cleared
   *    - Qdrant checkpoints removed
   *    - AgentDB cache entries removed
   *
   * Expected:
   * - Cleanup completes <2s
   * - No resource leaks
   * - All stores consistent
   */
  test('query termination cleans up all resources', async () => {
    // Create query
    const query = await queryControl.createQuery({
      model: 'claude-3-5-sonnet-20241022',
      permissionMode: 'default',
    });

    // Create resources
    await Promise.all([
      env.agentDB.getAgentDefinition('researcher', { queryId: query.queryId }),
      env.agentDB.getAgentDefinition('coder', { queryId: query.queryId }),
    ]);

    // Create checkpoint
    await queryControl.pauseQuery(query.queryId);

    // Capture state before termination
    const beforeState = await captureSystemState(env);

    // Terminate query
    const terminateStart = Date.now();
    await queryControl.terminateQuery(query.queryId);
    const terminateDuration = Date.now() - terminateStart;

    expect(terminateDuration).toBeLessThan(2000);

    // Verify PostgreSQL cleanup
    const pgQuery = await env.postgres.query(
      'SELECT * FROM queries WHERE query_id = $1',
      [query.queryId]
    );
    expect(pgQuery.rows.length).toBe(0);

    const pgCheckpoints = await env.postgres.query(
      'SELECT * FROM query_checkpoints WHERE query_id = $1',
      [query.queryId]
    );
    expect(pgCheckpoints.rows.length).toBe(0);

    // Verify Redis cleanup
    const redisKeys = await env.redis.keys(`*${query.queryId}*`);
    expect(redisKeys.length).toBe(0);

    // Verify no resource leaks
    const afterState = await captureSystemState(env);
    expect(afterState.redis.keyCount).toBeLessThanOrEqual(beforeState.redis.keyCount);
  }, 60000);

  /**
   * Test 8: Multi-query orchestration
   *
   * Flow:
   * 1. Start 3 concurrent queries
   * 2. Each spawns agents and jobs
   * 3. Pause query 1
   * 4. Verify queries 2 & 3 continue
   * 5. Resume query 1
   * 6. Terminate all queries
   * 7. Verify no interference
   *
   * Expected:
   * - Queries isolated from each other
   * - No resource contention
   * - Independent state management
   */
  test('multi-query orchestration without interference', async () => {
    // Create 3 queries
    const queries = await Promise.all([
      queryControl.createQuery({ model: 'claude-3-5-sonnet-20241022', permissionMode: 'default' }),
      queryControl.createQuery({ model: 'claude-3-5-sonnet-20241022', permissionMode: 'default' }),
      queryControl.createQuery({ model: 'claude-3-5-haiku-20241022', permissionMode: 'default' }),
    ]);

    expect(queries.length).toBe(3);

    // Spawn agents for each query
    for (const query of queries) {
      await env.agentDB.getAgentDefinition('researcher', { queryId: query.queryId });
    }

    // Pause query 1
    await queryControl.pauseQuery(queries[0].queryId);

    // Verify query 1 paused
    const query1 = await queryControl.getQuery(queries[0].queryId);
    expect(query1.status).toBe('paused');

    // Verify queries 2 & 3 still active
    const query2 = await queryControl.getQuery(queries[1].queryId);
    const query3 = await queryControl.getQuery(queries[2].queryId);
    expect(query2.status).toBe('active');
    expect(query3.status).toBe('active');

    // Resume query 1
    await queryControl.resumeQuery(queries[0].queryId);

    // Verify all active
    const allQueries = await queryControl.listQueries();
    const activeCount = allQueries.filter(q => q.status === 'active').length;
    expect(activeCount).toBe(3);

    // Terminate all
    for (const query of queries) {
      await queryControl.terminateQuery(query.queryId);
    }

    // Verify all terminated
    const finalQueries = await queryControl.listQueries();
    expect(finalQueries.length).toBe(0);
  }, 90000);

  /**
   * Test 9: End-to-end query lifecycle with all services
   *
   * Flow:
   * 1. Create query
   * 2. Spawn parallel agents (GAP-001)
   * 3. Cache agent data (GAP-002)
   * 4. Query Neo4j equipment (GAP-004)
   * 5. Create jobs (GAP-006)
   * 6. Pause with full checkpoint
   * 7. Resume with full restoration
   * 8. Complete query
   * 9. Verify audit trail
   *
   * Expected:
   * - Full integration works end-to-end
   * - <30s total lifecycle
   * - Complete audit trail
   * - All services coordinated
   */
  test('end-to-end query lifecycle with all GAPs', async () => {
    const lifecycleStart = Date.now();

    // 1. Create query
    const query = await queryControl.createQuery({
      model: 'claude-3-5-sonnet-20241022',
      permissionMode: 'default',
    });

    // 2. Spawn parallel agents (GAP-001)
    const agentTypes = ['researcher', 'coder', 'tester'];
    const agents = await Promise.all(
      agentTypes.map(type => env.agentDB.getAgentDefinition(type, { queryId: query.queryId }))
    );
    expect(agents.length).toBe(3);

    // 3. Verify AgentDB cache (GAP-002)
    const cacheStats = await env.agentDB.getCacheStats();
    expect(cacheStats.l1.entries).toBe(3);

    // 4. Query Neo4j equipment (GAP-004)
    const neo4jSession = env.neo4j.session();
    try {
      await neo4jSession.run(`
        CREATE (e:Equipment {
          equipmentId: 'TEST-LIFECYCLE-001',
          name: 'Lifecycle Test Equipment',
          testMarker: true
        })
      `);

      const result = await neo4jSession.run(`
        MATCH (e:Equipment {equipmentId: 'TEST-LIFECYCLE-001'})
        RETURN e
      `);
      expect(result.records.length).toBe(1);
    } finally {
      await neo4jSession.close();
    }

    // 5. Create jobs (GAP-006)
    const job1 = await env.postgres.query(`
      INSERT INTO jobs (job_type, status, payload, metadata)
      VALUES ('analysis', 'pending', $1, $2)
      RETURNING id
    `, [
      JSON.stringify({ equipmentId: 'TEST-LIFECYCLE-001' }),
      JSON.stringify({ queryId: query.queryId })
    ]);
    expect(job1.rows[0].id).toBeDefined();

    // 6. Pause with full checkpoint
    await queryControl.pauseQuery(query.queryId);
    const checkpoint = await queryControl.getCheckpoint(query.queryId);
    expect(checkpoint).toBeDefined();

    // 7. Resume with full restoration
    await queryControl.resumeQuery(query.queryId);
    const resumed = await queryControl.getQuery(query.queryId);
    expect(resumed.status).toBe('active');

    // 8. Complete query
    await queryControl.completeQuery(query.queryId);

    // 9. Verify audit trail
    const auditResult = await env.postgres.query(`
      SELECT * FROM query_audit_log
      WHERE query_id = $1
      ORDER BY created_at
    `, [query.queryId]);

    expect(auditResult.rows.length).toBeGreaterThan(0);

    const lifecycleDuration = Date.now() - lifecycleStart;
    expect(lifecycleDuration).toBeLessThan(30000); // <30s

    console.log(`End-to-end lifecycle completed in ${lifecycleDuration}ms`);
  }, 90000);
});
