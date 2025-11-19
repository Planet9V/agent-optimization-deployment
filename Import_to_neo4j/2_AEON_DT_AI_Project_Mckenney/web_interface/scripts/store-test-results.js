#!/usr/bin/env node
/**
 * Store Comprehensive Test Results in Qdrant
 * Collection: aeon-dt-continuity
 * Key: comprehensive-test-results-{timestamp}
 */

const fs = require('fs');
const { QdrantClient } = require('@qdrant/js-client-rest');

// Load test results
const path = require('path');
const testResults = require(path.join(__dirname, '../tests/test-results.json'));
const reportPath = path.join(__dirname, '../docs/COMPREHENSIVE_TEST_REPORT.md');
const reportContent = fs.readFileSync(reportPath, 'utf-8');

// Qdrant connection
const qdrantUrl = process.env.QDRANT_URL || 'http://localhost:6333';
const qdrantApiKey = process.env.QDRANT_API_KEY;

const client = new QdrantClient({
  url: qdrantUrl,
  apiKey: qdrantApiKey
});

const COLLECTION_NAME = 'aeon-dt-continuity';

async function storeTestResults() {
  console.log('📊 Storing Comprehensive Test Results in Qdrant...');
  console.log(`Target: ${qdrantUrl}`);
  console.log(`Collection: ${COLLECTION_NAME}`);

  try {
    // Check if collection exists
    let collectionExists = false;
    try {
      await client.getCollection(COLLECTION_NAME);
      collectionExists = true;
      console.log('✅ Collection exists');
    } catch (error) {
      console.log('⚠️  Collection does not exist, creating...');
    }

    // Create collection if it doesn't exist
    if (!collectionExists) {
      await client.createCollection(COLLECTION_NAME, {
        vectors: {
          size: 1536,
          distance: 'Cosine'
        }
      });
      console.log('✅ Collection created');
    }

    // Create document ID with timestamp
    const timestamp = new Date(testResults.timestamp).getTime();
    const pointId = `comprehensive-test-results-${timestamp}`;

    // Prepare payload with comprehensive test data
    const payload = {
      id: pointId,
      timestamp: testResults.timestamp,
      type: 'comprehensive-test-report',
      testSummary: {
        total: testResults.summary.total,
        passed: testResults.summary.passed,
        failed: testResults.summary.failed,
        successRate: ((testResults.summary.passed / testResults.summary.total) * 100).toFixed(2),
        errors: testResults.summary.errors
      },
      backendResults: {
        neo4j: testResults.backend['Neo4j Connection'],
        qdrant: testResults.backend['Qdrant Connection'],
        mysql: testResults.backend['MySQL Connection'],
        minio: testResults.backend['MinIO Connection']
      },
      pageResults: testResults.pages,
      apiResults: testResults.apis,
      navigationResults: testResults.navigation,
      quickActionResults: testResults.quickActions,
      reportMarkdown: reportContent,
      criticalFindings: [
        'ALL backend database connections failed (Neo4j, Qdrant, MySQL, MinIO)',
        '3 pages crash with 500 errors (Search, Tags, Graph)',
        'ALL API endpoints return errors or timeouts',
        'Production hostnames configured but services not running',
        'Missing Select component exports causing build errors'
      ],
      recommendations: [
        'Start all backend Docker services',
        'Create .env.local with localhost configuration',
        'Fix missing Select component exports',
        'Add graceful error handling for missing backends',
        'Implement connection retry logic'
      ],
      productionReadiness: {
        status: 'NOT READY',
        percentage: 20,
        blockers: [
          'Zero backend connectivity',
          'Critical page failures',
          'API endpoints non-functional',
          'Build/import errors present'
        ]
      },
      metadata: {
        testedBy: 'QA Testing Specialist',
        testDuration: '~30 seconds',
        serverPort: 3002,
        nodeEnv: 'development',
        evidenceFiles: [
          'tests/test-results.json',
          'tests/comprehensive-test.js',
          'docs/COMPREHENSIVE_TEST_REPORT.md'
        ]
      }
    };

    // Create a simple embedding vector (all zeros for now, or could use text embedding)
    // In production, you'd use an actual embedding model
    const vector = new Array(1536).fill(0);
    vector[0] = 0.1; // Add small value to distinguish from empty

    // Store in Qdrant
    await client.upsert(COLLECTION_NAME, {
      wait: true,
      points: [
        {
          id: pointId,
          vector: vector,
          payload: payload
        }
      ]
    });

    console.log('✅ Test results stored successfully');
    console.log(`   Point ID: ${pointId}`);
    console.log(`   Success Rate: ${payload.testSummary.successRate}%`);
    console.log(`   Production Ready: ${payload.productionReadiness.status}`);

    // Verify storage
    const stored = await client.retrieve(COLLECTION_NAME, {
      ids: [pointId]
    });

    if (stored && stored.length > 0) {
      console.log('✅ Verification successful - data retrieved from Qdrant');
      console.log(`   Stored payload size: ${JSON.stringify(stored[0].payload).length} bytes`);
    }

    return {
      success: true,
      pointId: pointId,
      collection: COLLECTION_NAME,
      url: qdrantUrl
    };

  } catch (error) {
    console.error('❌ Failed to store test results:', error.message);

    if (error.message.includes('ECONNREFUSED') || error.message.includes('ETIMEDOUT')) {
      console.error('⚠️  Qdrant service not accessible at', qdrantUrl);
      console.error('   This is expected if Qdrant is not running');
      console.error('   Test results are still available in local files:');
      console.error('   - tests/test-results.json');
      console.error('   - docs/COMPREHENSIVE_TEST_REPORT.md');
    }

    return {
      success: false,
      error: error.message
    };
  }
}

// Run storage
storeTestResults()
  .then(result => {
    if (result.success) {
      console.log('\n✅ Storage complete!');
      process.exit(0);
    } else {
      console.log('\n⚠️  Storage failed, but local files preserved');
      process.exit(1);
    }
  })
  .catch(error => {
    console.error('\n❌ Unexpected error:', error);
    process.exit(1);
  });
