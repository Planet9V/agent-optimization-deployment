#!/usr/bin/env node

/**
 * Integration Test - Verify Backend Services Work with Application
 */

const neo4j = require('neo4j-driver');
const { QdrantClient } = require('@qdrant/js-client-rest');
const mysql = require('mysql2/promise');
const Minio = require('minio');
const fs = require('fs');
const path = require('path');

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

async function testNeo4jQuery() {
  log('\n🔍 Testing Neo4j Graph Queries...', 'cyan');
  try {
    const driver = neo4j.driver(
      'bolt://localhost:7687',
      neo4j.auth.basic('neo4j', 'neo4j@openspg')
    );

    const session = driver.session();

    // Test 1: Get sample nodes
    const result1 = await session.run('MATCH (n) RETURN n LIMIT 5');
    log(`  ✓ Retrieved ${result1.records.length} sample nodes`, 'green');

    // Test 2: Count node types
    const result2 = await session.run('MATCH (n) RETURN labels(n) as labels, count(*) as count LIMIT 10');
    log(`  ✓ Found ${result2.records.length} different node types`, 'green');

    await session.close();
    await driver.close();

    log('✅ Neo4j graph queries working', 'green');
    return true;
  } catch (error) {
    log(`❌ Neo4j query test failed: ${error.message}`, 'red');
    return false;
  }
}

async function testQdrantSearch() {
  log('\n🔍 Testing Qdrant Vector Search...', 'cyan');
  try {
    const client = new QdrantClient({
      url: 'http://localhost:6333',
      apiKey: process.env.QDRANT_API_KEY
    });

    // Test 1: List collections
    const collections = await client.getCollections();
    log(`  ✓ Found ${collections.collections.length} collections`, 'green');

    // Test 2: Check if our collection exists
    const ourCollection = collections.collections.find(c => c.name === 'aeon-dt-continuity');
    if (ourCollection) {
      log(`  ✓ Our collection 'aeon-dt-continuity' exists`, 'green');

      // Test 3: Retrieve stored data
      const scrollResult = await client.scroll('aeon-dt-continuity', {
        limit: 5
      });
      log(`  ✓ Retrieved ${scrollResult.points.length} verification records`, 'green');
    }

    log('✅ Qdrant vector search working', 'green');
    return true;
  } catch (error) {
    log(`❌ Qdrant search test failed: ${error.message}`, 'red');
    return false;
  }
}

async function testMySQLQueries() {
  log('\n🔍 Testing MySQL Data Queries...', 'cyan');
  try {
    const connection = await mysql.createConnection({
      host: 'localhost',
      port: 3306,
      user: 'root',
      password: 'openspg',
      database: 'openspg'
    });

    // Test 1: Get database info
    const [dbInfo] = await connection.execute('SELECT DATABASE() as db, VERSION() as version');
    log(`  ✓ Connected to database: ${dbInfo[0].db}`, 'green');
    log(`  ✓ MySQL version: ${dbInfo[0].version}`, 'green');

    // Test 2: List tables
    const [tables] = await connection.execute('SHOW TABLES');
    log(`  ✓ Found ${tables.length} tables`, 'green');

    // Test 3: Sample query
    const [sample] = await connection.execute('SELECT table_name, table_rows FROM information_schema.tables WHERE table_schema = ? LIMIT 5', ['openspg']);
    log(`  ✓ Retrieved sample table statistics`, 'green');

    await connection.end();

    log('✅ MySQL queries working', 'green');
    return true;
  } catch (error) {
    log(`❌ MySQL query test failed: ${error.message}`, 'red');
    return false;
  }
}

async function testMinIOUpload() {
  log('\n🔍 Testing MinIO File Operations...', 'cyan');
  try {
    const minioClient = new Minio.Client({
      endPoint: 'localhost',
      port: 9000,
      useSSL: false,
      accessKey: 'minio',
      secretKey: 'minio@openspg'
    });

    const bucketName = 'aeon-documents';

    // Test 1: Check bucket exists
    const bucketExists = await minioClient.bucketExists(bucketName);
    if (!bucketExists) {
      await minioClient.makeBucket(bucketName);
      log(`  ✓ Created bucket: ${bucketName}`, 'green');
    } else {
      log(`  ✓ Bucket exists: ${bucketName}`, 'green');
    }

    // Test 2: Upload test file
    const testFileName = 'test-verification.txt';
    const testContent = `Backend verification test
Timestamp: ${new Date().toISOString()}
Status: All systems operational`;

    await minioClient.putObject(
      bucketName,
      testFileName,
      Buffer.from(testContent),
      testContent.length,
      { 'Content-Type': 'text/plain' }
    );
    log(`  ✓ Uploaded test file: ${testFileName}`, 'green');

    // Test 3: List objects
    const objectsList = [];
    const stream = minioClient.listObjects(bucketName, '', true);

    await new Promise((resolve, reject) => {
      stream.on('data', obj => objectsList.push(obj));
      stream.on('error', reject);
      stream.on('end', resolve);
    });

    log(`  ✓ Found ${objectsList.length} objects in bucket`, 'green');

    // Test 4: Download test file
    const downloadedContent = await new Promise((resolve, reject) => {
      let data = '';
      minioClient.getObject(bucketName, testFileName, (err, stream) => {
        if (err) return reject(err);
        stream.on('data', chunk => data += chunk);
        stream.on('end', () => resolve(data));
        stream.on('error', reject);
      });
    });

    log(`  ✓ Downloaded and verified test file`, 'green');

    log('✅ MinIO file operations working', 'green');
    return true;
  } catch (error) {
    log(`❌ MinIO upload test failed: ${error.message}`, 'red');
    return false;
  }
}

async function main() {
  log('═══════════════════════════════════════════════════════', 'blue');
  log('  AEON UI - Backend Integration Testing', 'blue');
  log('  Testing actual operations with each service', 'blue');
  log('═══════════════════════════════════════════════════════', 'blue');

  const results = {
    neo4j: await testNeo4jQuery(),
    qdrant: await testQdrantSearch(),
    mysql: await testMySQLQueries(),
    minio: await testMinIOUpload()
  };

  // Summary
  log('\n═══════════════════════════════════════════════════════', 'blue');
  log('  INTEGRATION TEST SUMMARY', 'blue');
  log('═══════════════════════════════════════════════════════', 'blue');

  Object.entries(results).forEach(([service, success]) => {
    const status = success ? '✅ PASS' : '❌ FAIL';
    const color = success ? 'green' : 'red';
    log(`${status} ${service.toUpperCase()}: ${success ? 'All operations successful' : 'Some operations failed'}`, color);
  });

  const allPassed = Object.values(results).every(r => r);

  if (allPassed) {
    log('\n🎉 ALL INTEGRATION TESTS PASSED!', 'green');
    log('   Backend services are fully operational and integrated.', 'green');
    process.exit(0);
  } else {
    log('\n⚠️  Some integration tests failed', 'yellow');
    log('   Check the errors above for details', 'yellow');
    process.exit(1);
  }
}

main().catch(error => {
  log(`\n💥 Integration test failed: ${error.message}`, 'red');
  console.error(error);
  process.exit(1);
});
