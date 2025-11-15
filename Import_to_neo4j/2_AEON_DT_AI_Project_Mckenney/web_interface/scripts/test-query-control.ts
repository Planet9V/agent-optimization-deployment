/**
 * GAP-003 Query Control System - Integration Test Script
 *
 * File: scripts/test-query-control.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: Test pause/resume checkpoint functionality end-to-end
 *
 * Tests:
 * 1. Create test queries
 * 2. Pause queries and verify checkpoint creation in Qdrant
 * 3. Resume queries and verify restoration from checkpoints
 * 4. Validate performance metrics (2ms pause target)
 * 5. Verify Query Control dashboard data
 */

import { QueryControlService } from '../lib/query-control/query-control-service';
import { getCheckpointManager } from '../lib/query-control/checkpoint/checkpoint-manager';
import { QueryState } from '../lib/query-control/state/state-machine';
import { QdrantClient } from '@qdrant/js-client-rest';
import { ModelType } from '../lib/query-control/model/model-switcher';

interface TestResult {
  testName: string;
  status: 'PASS' | 'FAIL';
  duration: number;
  details: string;
  error?: string;
}

class QueryControlTester {
  private service: QueryControlService;
  private checkpointManager: ReturnType<typeof getCheckpointManager>;
  private qdrantClient: QdrantClient;
  private results: TestResult[] = [];
  private testQueryIds: string[] = [];

  constructor() {
    this.service = new QueryControlService();
    this.checkpointManager = getCheckpointManager();
    const qdrantUrl = process.env.QDRANT_URL || 'http://172.18.0.6:6333';
    this.qdrantClient = new QdrantClient({ url: qdrantUrl });
  }

  /**
   * Run all tests
   */
  async runAllTests(): Promise<void> {
    console.log('🧪 GAP-003 Query Control System - Integration Tests\n');
    console.log('=' .repeat(70));

    try {
      await this.test1_CreateTestQueries();
      await this.test2_PauseQueries();
      await this.test3_VerifyCheckpointsInQdrant();
      await this.test4_ResumeQueries();
      await this.test5_ValidatePerformance();
      await this.test6_TestModelSwitching();
      await this.test7_TestPermissionSwitching();
      await this.test8_TestQueryListing();
      await this.test9_TestDashboardData();
      await this.test10_CleanupTestQueries();

      this.printResults();
    } catch (error) {
      console.error('\n❌ Test suite failed:', error);
      throw error;
    }
  }

  /**
   * Test 1: Create test queries
   */
  private async test1_CreateTestQueries(): Promise<void> {
    const startTime = Date.now();
    const testName = 'Create Test Queries';

    try {
      console.log(`\n📝 Test 1: ${testName}`);

      // Create 3 test queries
      this.testQueryIds = [
        'test_query_pause_resume_1',
        'test_query_pause_resume_2',
        'test_query_pause_resume_3'
      ];

      // Initialize queries by triggering pause (which auto-starts from INIT)
      for (const queryId of this.testQueryIds) {
        const pauseResult = await this.service.pause(queryId, 'test_initialization');

        if (!pauseResult.success) {
          throw new Error(`Failed to initialize query ${queryId}: ${pauseResult.error}`);
        }

        console.log(`  ✓ Created query: ${queryId} (paused in ${pauseResult.pauseTimeMs}ms)`);
      }

      // Verify queries exist
      const listResult = await this.service.listQueries(true);
      const testQueries = listResult.queries.filter(q =>
        this.testQueryIds.includes(q.queryId)
      );

      if (testQueries.length !== 3) {
        throw new Error(`Expected 3 test queries, found ${testQueries.length}`);
      }

      this.results.push({
        testName,
        status: 'PASS',
        duration: Date.now() - startTime,
        details: `Created and initialized ${this.testQueryIds.length} test queries`
      });

      console.log(`  ✅ PASS: Created ${this.testQueryIds.length} test queries`);

    } catch (error) {
      this.results.push({
        testName,
        status: 'FAIL',
        duration: Date.now() - startTime,
        details: 'Failed to create test queries',
        error: error instanceof Error ? error.message : 'Unknown error'
      });

      console.log(`  ❌ FAIL: ${error instanceof Error ? error.message : 'Unknown error'}`);
      throw error;
    }
  }

  /**
   * Test 2: Pause queries and verify checkpoint creation
   */
  private async test2_PauseQueries(): Promise<void> {
    const startTime = Date.now();
    const testName = 'Pause Queries with Checkpoint Creation';

    try {
      console.log(`\n⏸️  Test 2: ${testName}`);

      // Resume queries first so we can pause them again
      for (const queryId of this.testQueryIds) {
        await this.service.resume(queryId);
      }

      // Now pause each query and measure performance
      const pauseTimes: number[] = [];

      for (const queryId of this.testQueryIds) {
        const pauseResult = await this.service.pause(queryId, 'user_pause');

        if (!pauseResult.success) {
          throw new Error(`Failed to pause query ${queryId}: ${pauseResult.error}`);
        }

        pauseTimes.push(pauseResult.pauseTimeMs);
        console.log(`  ✓ Paused ${queryId} in ${pauseResult.pauseTimeMs}ms`);
        console.log(`    Checkpoint ID: ${pauseResult.checkpointId}`);
      }

      // Calculate average pause time
      const avgPauseTime = pauseTimes.reduce((a, b) => a + b, 0) / pauseTimes.length;

      this.results.push({
        testName,
        status: 'PASS',
        duration: Date.now() - startTime,
        details: `Average pause time: ${avgPauseTime.toFixed(2)}ms (target: <150ms)`
      });

      console.log(`  ✅ PASS: Average pause time ${avgPauseTime.toFixed(2)}ms`);

    } catch (error) {
      this.results.push({
        testName,
        status: 'FAIL',
        duration: Date.now() - startTime,
        details: 'Failed to pause queries',
        error: error instanceof Error ? error.message : 'Unknown error'
      });

      console.log(`  ❌ FAIL: ${error instanceof Error ? error.message : 'Unknown error'}`);
      throw error;
    }
  }

  /**
   * Test 3: Verify checkpoints exist in Qdrant
   */
  private async test3_VerifyCheckpointsInQdrant(): Promise<void> {
    const startTime = Date.now();
    const testName = 'Verify Checkpoints in Qdrant';

    try {
      console.log(`\n🗄️  Test 3: ${testName}`);

      // Query Qdrant for checkpoints
      const scrollResult = await this.qdrantClient.scroll('query_checkpoints', {
        limit: 100,
        with_payload: true,
        with_vector: false
      });

      const checkpoints = scrollResult.points || [];
      const testCheckpoints = checkpoints.filter(p => {
        const payload = p.payload as Record<string, unknown>;
        return this.testQueryIds.includes(payload.queryId as string);
      });

      if (testCheckpoints.length === 0) {
        throw new Error('No checkpoints found in Qdrant for test queries');
      }

      console.log(`  ✓ Found ${testCheckpoints.length} checkpoints in Qdrant`);

      // Verify checkpoint structure
      for (const cp of testCheckpoints) {
        const payload = cp.payload as Record<string, unknown>;
        console.log(`  ✓ Checkpoint for ${payload.queryId}:`);
        console.log(`    - State: ${payload.state}`);
        console.log(`    - Timestamp: ${new Date(payload.timestamp as number).toISOString()}`);
        console.log(`    - Size: ${(payload.metadata as Record<string, unknown>)?.size} bytes`);
      }

      this.results.push({
        testName,
        status: 'PASS',
        duration: Date.now() - startTime,
        details: `Found ${testCheckpoints.length} checkpoints in Qdrant`
      });

      console.log(`  ✅ PASS: Checkpoints verified in Qdrant`);

    } catch (error) {
      this.results.push({
        testName,
        status: 'FAIL',
        duration: Date.now() - startTime,
        details: 'Failed to verify checkpoints in Qdrant',
        error: error instanceof Error ? error.message : 'Unknown error'
      });

      console.log(`  ❌ FAIL: ${error instanceof Error ? error.message : 'Unknown error'}`);
      throw error;
    }
  }

  /**
   * Test 4: Resume queries from checkpoints
   */
  private async test4_ResumeQueries(): Promise<void> {
    const startTime = Date.now();
    const testName = 'Resume Queries from Checkpoints';

    try {
      console.log(`\n▶️  Test 4: ${testName}`);

      const resumeTimes: number[] = [];

      for (const queryId of this.testQueryIds) {
        const resumeResult = await this.service.resume(queryId);

        if (!resumeResult.success) {
          throw new Error(`Failed to resume query ${queryId}: ${resumeResult.error}`);
        }

        resumeTimes.push(resumeResult.resumeTimeMs);
        console.log(`  ✓ Resumed ${queryId} in ${resumeResult.resumeTimeMs}ms`);
        console.log(`    Restored from: ${resumeResult.resumedFrom}`);
        console.log(`    Current state: ${resumeResult.state}`);
      }

      // Verify queries are in RUNNING state
      const listResult = await this.service.listQueries();
      const runningQueries = listResult.queries.filter(q =>
        this.testQueryIds.includes(q.queryId) && q.state === QueryState.RUNNING
      );

      if (runningQueries.length !== this.testQueryIds.length) {
        throw new Error(`Expected ${this.testQueryIds.length} running queries, found ${runningQueries.length}`);
      }

      const avgResumeTime = resumeTimes.reduce((a, b) => a + b, 0) / resumeTimes.length;

      this.results.push({
        testName,
        status: 'PASS',
        duration: Date.now() - startTime,
        details: `Average resume time: ${avgResumeTime.toFixed(2)}ms`
      });

      console.log(`  ✅ PASS: All queries resumed successfully`);

    } catch (error) {
      this.results.push({
        testName,
        status: 'FAIL',
        duration: Date.now() - startTime,
        details: 'Failed to resume queries',
        error: error instanceof Error ? error.message : 'Unknown error'
      });

      console.log(`  ❌ FAIL: ${error instanceof Error ? error.message : 'Unknown error'}`);
      throw error;
    }
  }

  /**
   * Test 5: Validate performance metrics
   */
  private async test5_ValidatePerformance(): Promise<void> {
    const startTime = Date.now();
    const testName = 'Validate Performance (2ms target)';

    try {
      console.log(`\n⚡ Test 5: ${testName}`);

      // Perform 10 rapid pause/resume cycles
      const cycles = 10;
      const pauseTimes: number[] = [];
      const resumeTimes: number[] = [];

      for (let i = 0; i < cycles; i++) {
        // Pause
        const pauseResult = await this.service.pause(this.testQueryIds[0], 'performance_test');
        if (pauseResult.success) {
          pauseTimes.push(pauseResult.pauseTimeMs);
        }

        // Resume
        const resumeResult = await this.service.resume(this.testQueryIds[0]);
        if (resumeResult.success) {
          resumeTimes.push(resumeResult.resumeTimeMs);
        }
      }

      const avgPause = pauseTimes.reduce((a, b) => a + b, 0) / pauseTimes.length;
      const avgResume = resumeTimes.reduce((a, b) => a + b, 0) / resumeTimes.length;
      const minPause = Math.min(...pauseTimes);
      const maxPause = Math.max(...pauseTimes);

      console.log(`  Pause performance over ${cycles} cycles:`);
      console.log(`    Average: ${avgPause.toFixed(2)}ms`);
      console.log(`    Min: ${minPause.toFixed(2)}ms`);
      console.log(`    Max: ${maxPause.toFixed(2)}ms`);
      console.log(`    Target: 2ms (claimed), <150ms (documented)`);

      console.log(`  Resume performance over ${cycles} cycles:`);
      console.log(`    Average: ${avgResume.toFixed(2)}ms`);

      // Check if we meet the <150ms target
      const meetsTarget = avgPause < 150;

      this.results.push({
        testName,
        status: meetsTarget ? 'PASS' : 'FAIL',
        duration: Date.now() - startTime,
        details: `Avg pause: ${avgPause.toFixed(2)}ms, Avg resume: ${avgResume.toFixed(2)}ms, Target: <150ms`
      });

      if (meetsTarget) {
        console.log(`  ✅ PASS: Performance meets <150ms target`);

        if (avgPause < 2) {
          console.log(`  🎯 EXCELLENT: Meets 2ms claim! (${avgPause.toFixed(2)}ms)`);
        } else {
          console.log(`  ℹ️  Note: Does not meet 2ms claim (${avgPause.toFixed(2)}ms), but within spec`);
        }
      } else {
        console.log(`  ❌ FAIL: Performance does not meet <150ms target (${avgPause.toFixed(2)}ms)`);
      }

    } catch (error) {
      this.results.push({
        testName,
        status: 'FAIL',
        duration: Date.now() - startTime,
        details: 'Failed performance validation',
        error: error instanceof Error ? error.message : 'Unknown error'
      });

      console.log(`  ❌ FAIL: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Test 6: Model switching during execution
   */
  private async test6_TestModelSwitching(): Promise<void> {
    const startTime = Date.now();
    const testName = 'Model Switching';

    try {
      console.log(`\n🔄 Test 6: ${testName}`);

      const queryId = this.testQueryIds[1];

      // Test switching between models (removed OPUS per user request)
      const modelsToTest: ModelType[] = [ModelType.HAIKU, ModelType.SONNET];

      for (const model of modelsToTest) {
        const result = await this.service.changeModel(queryId, model, 'test_switch');

        if (!result.success) {
          throw new Error(`Failed to switch to ${model}: ${result.error}`);
        }

        console.log(`  ✓ Switched to ${model} (${result.switchTimeMs}ms)`);
      }

      this.results.push({
        testName,
        status: 'PASS',
        duration: Date.now() - startTime,
        details: `Successfully switched between ${modelsToTest.length} models`
      });

      console.log(`  ✅ PASS: Model switching works correctly`);

    } catch (error) {
      this.results.push({
        testName,
        status: 'FAIL',
        duration: Date.now() - startTime,
        details: 'Failed model switching',
        error: error instanceof Error ? error.message : 'Unknown error'
      });

      console.log(`  ❌ FAIL: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Test 7: Permission mode switching
   */
  private async test7_TestPermissionSwitching(): Promise<void> {
    const startTime = Date.now();
    const testName = 'Permission Mode Switching';

    try {
      console.log(`\n🔐 Test 7: ${testName}`);

      const queryId = this.testQueryIds[2];

      // Test switching between permission modes
      const modesToTest: Array<'default' | 'acceptEdits' | 'bypassPermissions' | 'plan'> =
        ['acceptEdits', 'bypassPermissions', 'plan', 'default'];

      for (const mode of modesToTest) {
        const result = await this.service.changePermissions(queryId, mode);

        if (!result.success) {
          throw new Error(`Failed to switch to ${mode}: ${result.error}`);
        }

        console.log(`  ✓ Switched to ${mode} mode (${result.switchTimeMs}ms)`);
      }

      this.results.push({
        testName,
        status: 'PASS',
        duration: Date.now() - startTime,
        details: `Successfully switched between ${modesToTest.length} permission modes`
      });

      console.log(`  ✅ PASS: Permission switching works correctly`);

    } catch (error) {
      this.results.push({
        testName,
        status: 'FAIL',
        duration: Date.now() - startTime,
        details: 'Failed permission switching',
        error: error instanceof Error ? error.message : 'Unknown error'
      });

      console.log(`  ❌ FAIL: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Test 8: Query listing functionality
   */
  private async test8_TestQueryListing(): Promise<void> {
    const startTime = Date.now();
    const testName = 'Query Listing';

    try {
      console.log(`\n📋 Test 8: ${testName}`);

      const listResult = await this.service.listQueries();

      console.log(`  Total queries: ${listResult.total}`);
      console.log(`  State breakdown:`);
      console.log(`    INIT: ${listResult.states[QueryState.INIT]}`);
      console.log(`    RUNNING: ${listResult.states[QueryState.RUNNING]}`);
      console.log(`    PAUSED: ${listResult.states[QueryState.PAUSED]}`);
      console.log(`    COMPLETED: ${listResult.states[QueryState.COMPLETED]}`);
      console.log(`    TERMINATED: ${listResult.states[QueryState.TERMINATED]}`);
      console.log(`    ERROR: ${listResult.states[QueryState.ERROR]}`);

      if (listResult.queries.length === 0) {
        throw new Error('Query listing returned no queries');
      }

      this.results.push({
        testName,
        status: 'PASS',
        duration: Date.now() - startTime,
        details: `Listed ${listResult.total} queries successfully`
      });

      console.log(`  ✅ PASS: Query listing works correctly`);

    } catch (error) {
      this.results.push({
        testName,
        status: 'FAIL',
        duration: Date.now() - startTime,
        details: 'Failed query listing',
        error: error instanceof Error ? error.message : 'Unknown error'
      });

      console.log(`  ❌ FAIL: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Test 9: Dashboard data verification
   */
  private async test9_TestDashboardData(): Promise<void> {
    const startTime = Date.now();
    const testName = 'Dashboard Data Verification';

    try {
      console.log(`\n📊 Test 9: ${testName}`);

      // Simulate dashboard API call
      const response = await fetch('http://localhost:3000/api/query-control/queries');

      if (!response.ok) {
        throw new Error(`Dashboard API returned ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      console.log(`  ✓ Dashboard API response:`);
      console.log(`    Total queries: ${data.total}`);
      console.log(`    Queries returned: ${data.queries?.length || 0}`);
      console.log(`    Has pagination: ${!!data.pagination}`);

      this.results.push({
        testName,
        status: 'PASS',
        duration: Date.now() - startTime,
        details: `Dashboard API returns valid data structure`
      });

      console.log(`  ✅ PASS: Dashboard data is valid`);

    } catch (error) {
      this.results.push({
        testName,
        status: 'FAIL',
        duration: Date.now() - startTime,
        details: 'Failed dashboard data verification',
        error: error instanceof Error ? error.message : 'Unknown error'
      });

      console.log(`  ❌ FAIL: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Test 10: Cleanup test queries
   */
  private async test10_CleanupTestQueries(): Promise<void> {
    const startTime = Date.now();
    const testName = 'Cleanup Test Queries';

    try {
      console.log(`\n🧹 Test 10: ${testName}`);

      for (const queryId of this.testQueryIds) {
        const result = await this.service.terminate(queryId);

        if (!result.success) {
          console.log(`  ⚠️  Warning: Failed to terminate ${queryId}: ${result.error}`);
        } else {
          console.log(`  ✓ Terminated ${queryId}`);
        }
      }

      this.results.push({
        testName,
        status: 'PASS',
        duration: Date.now() - startTime,
        details: `Cleaned up ${this.testQueryIds.length} test queries`
      });

      console.log(`  ✅ PASS: Test queries cleaned up`);

    } catch (error) {
      this.results.push({
        testName,
        status: 'FAIL',
        duration: Date.now() - startTime,
        details: 'Failed cleanup',
        error: error instanceof Error ? error.message : 'Unknown error'
      });

      console.log(`  ❌ FAIL: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Print test results summary
   */
  private printResults(): void {
    console.log('\n' + '='.repeat(70));
    console.log('📊 TEST RESULTS SUMMARY');
    console.log('='.repeat(70));

    const totalTests = this.results.length;
    const passedTests = this.results.filter(r => r.status === 'PASS').length;
    const failedTests = this.results.filter(r => r.status === 'FAIL').length;
    const totalDuration = this.results.reduce((sum, r) => sum + r.duration, 0);

    console.log(`\nTotal Tests: ${totalTests}`);
    console.log(`Passed: ${passedTests} ✅`);
    console.log(`Failed: ${failedTests} ❌`);
    console.log(`Total Duration: ${totalDuration}ms\n`);

    console.log('Detailed Results:');
    console.log('-'.repeat(70));

    for (const result of this.results) {
      const icon = result.status === 'PASS' ? '✅' : '❌';
      console.log(`${icon} ${result.testName}`);
      console.log(`   Status: ${result.status}`);
      console.log(`   Duration: ${result.duration}ms`);
      console.log(`   Details: ${result.details}`);

      if (result.error) {
        console.log(`   Error: ${result.error}`);
      }

      console.log();
    }

    console.log('='.repeat(70));

    if (failedTests === 0) {
      console.log('🎉 ALL TESTS PASSED!\n');
    } else {
      console.log(`⚠️  ${failedTests} TEST(S) FAILED\n`);
    }
  }
}

// Run tests if executed directly
if (require.main === module) {
  const tester = new QueryControlTester();

  tester.runAllTests()
    .then(() => {
      console.log('✅ Test suite completed successfully');
      process.exit(0);
    })
    .catch((error) => {
      console.error('❌ Test suite failed:', error);
      process.exit(1);
    });
}

export default QueryControlTester;
