#!/usr/bin/env node
/**
 * Comprehensive Test Suite for AEON UI
 * Tests ALL functionality with FACT-BASED verification
 */

const http = require('http');
const https = require('https');
const { URL } = require('url');

// Test configuration
const BASE_URL = 'http://localhost:3002';
const TIMEOUT = 30000;

// Test results storage
const results = {
  timestamp: new Date().toISOString(),
  backend: {},
  pages: {},
  apis: {},
  navigation: {},
  quickActions: {},
  summary: {
    total: 0,
    passed: 0,
    failed: 0,
    errors: []
  }
};

// HTTP request helper
function makeRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const client = urlObj.protocol === 'https:' ? https : http;

    const req = client.request(url, {
      method: options.method || 'GET',
      headers: options.headers || {},
      timeout: TIMEOUT
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = data ? JSON.parse(data) : null;
          resolve({ status: res.statusCode, data: json, headers: res.headers });
        } catch (e) {
          resolve({ status: res.statusCode, data: data, headers: res.headers });
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });

    if (options.body) {
      req.write(JSON.stringify(options.body));
    }

    req.end();
  });
}

// Test 1: Backend Database Connections
async function testBackendConnections() {
  console.log('\n📊 Testing Backend Database Connections...');

  const tests = [
    {
      name: 'Neo4j Connection',
      url: `${BASE_URL}/api/neo4j/statistics`,
      verify: (data) => data && typeof data.nodeCount !== 'undefined'
    },
    {
      name: 'Qdrant Connection',
      url: `${BASE_URL}/api/health`,
      verify: (data) => data && data.qdrant === 'healthy'
    },
    {
      name: 'MySQL Connection',
      url: `${BASE_URL}/api/health`,
      verify: (data) => data && data.mysql === 'healthy'
    },
    {
      name: 'MinIO Connection',
      url: `${BASE_URL}/api/health`,
      verify: (data) => data && data.minio === 'healthy'
    }
  ];

  for (const test of tests) {
    try {
      const res = await makeRequest(test.url);
      const passed = res.status === 200 && test.verify(res.data);

      results.backend[test.name] = {
        status: passed ? 'PASS' : 'FAIL',
        httpStatus: res.status,
        data: res.data,
        verified: passed,
        error: passed ? null : 'Verification failed or invalid response'
      };

      console.log(`  ${passed ? '✅' : '❌'} ${test.name}: ${res.status}`);

      results.summary.total++;
      if (passed) results.summary.passed++;
      else {
        results.summary.failed++;
        results.summary.errors.push(`${test.name}: Failed verification`);
      }
    } catch (error) {
      results.backend[test.name] = {
        status: 'ERROR',
        error: error.message
      };
      console.log(`  ❌ ${test.name}: ERROR - ${error.message}`);
      results.summary.total++;
      results.summary.failed++;
      results.summary.errors.push(`${test.name}: ${error.message}`);
    }
  }
}

// Test 2: All Application Pages
async function testPages() {
  console.log('\n📄 Testing All 9 Application Pages...');

  const pages = [
    { path: '/', name: 'Home Dashboard' },
    { path: '/upload', name: 'Upload Page' },
    { path: '/search', name: 'Search Page' },
    { path: '/tags', name: 'Tags Page' },
    { path: '/customers', name: 'Customers Page' },
    { path: '/chat', name: 'Chat Page' },
    { path: '/graph', name: 'Graph Page' },
    { path: '/analytics', name: 'Analytics Page' },
    { path: '/observability', name: 'Observability Page' }
  ];

  for (const page of pages) {
    try {
      const res = await makeRequest(`${BASE_URL}${page.path}`);
      const passed = res.status === 200;

      results.pages[page.name] = {
        status: passed ? 'PASS' : 'FAIL',
        httpStatus: res.status,
        contentLength: res.data ? res.data.length : 0,
        error: passed ? null : `HTTP ${res.status}`
      };

      console.log(`  ${passed ? '✅' : '❌'} ${page.name}: ${res.status}`);

      results.summary.total++;
      if (passed) results.summary.passed++;
      else {
        results.summary.failed++;
        results.summary.errors.push(`${page.name}: HTTP ${res.status}`);
      }
    } catch (error) {
      results.pages[page.name] = {
        status: 'ERROR',
        error: error.message
      };
      console.log(`  ❌ ${page.name}: ERROR - ${error.message}`);
      results.summary.total++;
      results.summary.failed++;
      results.summary.errors.push(`${page.name}: ${error.message}`);
    }
  }
}

// Test 3: All API Endpoints
async function testAPIs() {
  console.log('\n🔌 Testing All API Endpoints...');

  const apis = [
    {
      name: 'Health Check',
      url: `${BASE_URL}/api/health`,
      verify: (data) => data && data.status === 'healthy'
    },
    {
      name: 'Neo4j Statistics',
      url: `${BASE_URL}/api/neo4j/statistics`,
      verify: (data) => data && typeof data.nodeCount === 'number'
    },
    {
      name: 'Observability Overview',
      url: `${BASE_URL}/api/observability/overview`,
      verify: (data) => data !== null
    },
    {
      name: 'Customers API',
      url: `${BASE_URL}/api/customers`,
      verify: (data) => Array.isArray(data) || (data && typeof data === 'object')
    },
    {
      name: 'Tags API',
      url: `${BASE_URL}/api/tags`,
      verify: (data) => Array.isArray(data) || (data && typeof data === 'object')
    },
    {
      name: 'Search API',
      url: `${BASE_URL}/api/search?q=test`,
      verify: (data) => data !== null
    }
  ];

  for (const api of apis) {
    try {
      const res = await makeRequest(api.url);
      const passed = res.status === 200 && api.verify(res.data);

      results.apis[api.name] = {
        status: passed ? 'PASS' : 'FAIL',
        httpStatus: res.status,
        data: res.data,
        verified: passed,
        error: passed ? null : 'Verification failed'
      };

      console.log(`  ${passed ? '✅' : '❌'} ${api.name}: ${res.status}`);

      results.summary.total++;
      if (passed) results.summary.passed++;
      else {
        results.summary.failed++;
        results.summary.errors.push(`${api.name}: Failed verification`);
      }
    } catch (error) {
      results.apis[api.name] = {
        status: 'ERROR',
        error: error.message
      };
      console.log(`  ❌ ${api.name}: ERROR - ${error.message}`);
      results.summary.total++;
      results.summary.failed++;
      results.summary.errors.push(`${api.name}: ${error.message}`);
    }
  }
}

// Test 4: Navigation Links
async function testNavigation() {
  console.log('\n🧭 Testing Navigation...');

  // Test that navigation items exist and are accessible
  const navTests = [
    { name: 'Home accessible', url: `${BASE_URL}/` },
    { name: 'Upload accessible', url: `${BASE_URL}/upload` },
    { name: 'Search accessible', url: `${BASE_URL}/search` },
    { name: 'Analytics accessible', url: `${BASE_URL}/analytics` }
  ];

  for (const test of navTests) {
    try {
      const res = await makeRequest(test.url);
      const passed = res.status === 200;

      results.navigation[test.name] = {
        status: passed ? 'PASS' : 'FAIL',
        httpStatus: res.status
      };

      console.log(`  ${passed ? '✅' : '❌'} ${test.name}`);

      results.summary.total++;
      if (passed) results.summary.passed++;
      else {
        results.summary.failed++;
        results.summary.errors.push(`${test.name}: HTTP ${res.status}`);
      }
    } catch (error) {
      results.navigation[test.name] = {
        status: 'ERROR',
        error: error.message
      };
      console.log(`  ❌ ${test.name}: ERROR`);
      results.summary.total++;
      results.summary.failed++;
      results.summary.errors.push(`${test.name}: ${error.message}`);
    }
  }
}

// Test 5: Quick Actions
async function testQuickActions() {
  console.log('\n⚡ Testing Quick Actions...');

  // Quick actions point to these pages
  const actions = [
    { name: 'Upload Document', url: `${BASE_URL}/upload` },
    { name: 'Search Knowledge', url: `${BASE_URL}/search` },
    { name: 'View Graph', url: `${BASE_URL}/graph` },
    { name: 'Manage Tags', url: `${BASE_URL}/tags` },
    { name: 'View Customers', url: `${BASE_URL}/customers` },
    { name: 'Chat Interface', url: `${BASE_URL}/chat` },
    { name: 'View Analytics', url: `${BASE_URL}/analytics` }
  ];

  for (const action of actions) {
    try {
      const res = await makeRequest(action.url);
      const passed = res.status === 200;

      results.quickActions[action.name] = {
        status: passed ? 'PASS' : 'FAIL',
        httpStatus: res.status
      };

      console.log(`  ${passed ? '✅' : '❌'} ${action.name}`);

      results.summary.total++;
      if (passed) results.summary.passed++;
      else {
        results.summary.failed++;
        results.summary.errors.push(`${action.name}: HTTP ${res.status}`);
      }
    } catch (error) {
      results.quickActions[action.name] = {
        status: 'ERROR',
        error: error.message
      };
      console.log(`  ❌ ${action.name}: ERROR`);
      results.summary.total++;
      results.summary.failed++;
      results.summary.errors.push(`${action.name}: ${error.message}`);
    }
  }
}

// Generate final report
function generateReport() {
  console.log('\n' + '='.repeat(60));
  console.log('📊 COMPREHENSIVE TEST REPORT');
  console.log('='.repeat(60));

  const percentage = results.summary.total > 0
    ? ((results.summary.passed / results.summary.total) * 100).toFixed(2)
    : 0;

  console.log(`\n📈 Overall Results:`);
  console.log(`   Total Tests: ${results.summary.total}`);
  console.log(`   Passed: ${results.summary.passed} ✅`);
  console.log(`   Failed: ${results.summary.failed} ❌`);
  console.log(`   Success Rate: ${percentage}%`);

  if (results.summary.errors.length > 0) {
    console.log(`\n❌ Errors (${results.summary.errors.length}):`);
    results.summary.errors.forEach((err, i) => {
      console.log(`   ${i + 1}. ${err}`);
    });
  }

  // Save results
  const fs = require('fs');
  const reportPath = '/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/tests/test-results.json';
  fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));
  console.log(`\n💾 Full report saved to: ${reportPath}`);

  console.log('\n' + '='.repeat(60));

  return results;
}

// Main test runner
async function runAllTests() {
  console.log('🚀 Starting Comprehensive Test Suite...');
  console.log('Target: ' + BASE_URL);

  try {
    await testBackendConnections();
    await testPages();
    await testAPIs();
    await testNavigation();
    await testQuickActions();

    const report = generateReport();

    // Exit with error code if tests failed
    process.exit(results.summary.failed > 0 ? 1 : 0);
  } catch (error) {
    console.error('\n❌ Test suite error:', error);
    process.exit(1);
  }
}

// Run tests
runAllTests();
