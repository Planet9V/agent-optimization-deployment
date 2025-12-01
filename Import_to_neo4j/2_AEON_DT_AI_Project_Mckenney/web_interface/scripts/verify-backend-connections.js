#!/usr/bin/env node

/**
 * Backend Connection Verification Script
 * Tests all backend services for AEON UI
 */

const neo4j = require('neo4j-driver');
const { QdrantClient } = require('@qdrant/js-client-rest');
const mysql = require('mysql2/promise');
const Minio = require('minio');

// Color codes for output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

async function testNeo4j() {
  log('\n📊 Testing Neo4j Connection...', 'blue');
  try {
    const driver = neo4j.driver(
      process.env.NEO4J_URI || 'bolt://localhost:7687',
      neo4j.auth.basic(
        process.env.NEO4J_USER || 'neo4j',
        process.env.NEO4J_PASSWORD || 'neo4j@openspg'
      )
    );

    const session = driver.session();
    const result = await session.run('MATCH (n) RETURN count(n) as count');
    const count = result.records[0].get('count').toNumber();

    await session.close();
    await driver.close();

    log(`✅ Neo4j: CONNECTED (${count} nodes)`, 'green');
    return { service: 'Neo4j', status: 'SUCCESS', details: `${count} nodes`, uri: process.env.NEO4J_URI };
  } catch (error) {
    log(`❌ Neo4j: FAILED - ${error.message}`, 'red');
    return { service: 'Neo4j', status: 'FAILED', error: error.message };
  }
}

async function testQdrant() {
  log('\n🔍 Testing Qdrant Connection...', 'blue');
  try {
    const client = new QdrantClient({
      url: process.env.QDRANT_URL || 'http://localhost:6333',
      apiKey: process.env.QDRANT_API_KEY
    });

    const collections = await client.getCollections();

    log(`✅ Qdrant: CONNECTED (${collections.collections.length} collections)`, 'green');
    return {
      service: 'Qdrant',
      status: 'SUCCESS',
      details: `${collections.collections.length} collections`,
      collections: collections.collections.map(c => c.name),
      url: process.env.QDRANT_URL
    };
  } catch (error) {
    log(`❌ Qdrant: FAILED - ${error.message}`, 'red');
    return { service: 'Qdrant', status: 'FAILED', error: error.message };
  }
}

async function testMySQL() {
  log('\n💾 Testing MySQL Connection...', 'blue');
  try {
    const connection = await mysql.createConnection({
      host: process.env.MYSQL_HOST || 'localhost',
      port: parseInt(process.env.MYSQL_PORT || '3306'),
      user: process.env.MYSQL_USER || 'root',
      password: process.env.MYSQL_PASSWORD || 'openspg',
      database: process.env.MYSQL_DATABASE || 'openspg'
    });

    const [rows] = await connection.execute('SELECT DATABASE() as db, COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = ?', [process.env.MYSQL_DATABASE || 'openspg']);
    await connection.end();

    log(`✅ MySQL: CONNECTED (${rows[0].table_count} tables)`, 'green');
    return {
      service: 'MySQL',
      status: 'SUCCESS',
      details: `${rows[0].table_count} tables`,
      database: rows[0].db,
      host: process.env.MYSQL_HOST
    };
  } catch (error) {
    log(`❌ MySQL: FAILED - ${error.message}`, 'red');
    return { service: 'MySQL', status: 'FAILED', error: error.message };
  }
}

async function testMinIO() {
  log('\n📦 Testing MinIO Connection...', 'blue');
  try {
    const minioClient = new Minio.Client({
      endPoint: process.env.MINIO_ENDPOINT || 'localhost',
      port: parseInt(process.env.MINIO_PORT || '9000'),
      useSSL: process.env.MINIO_USE_SSL === 'true',
      accessKey: process.env.MINIO_ACCESS_KEY || 'minio',
      secretKey: process.env.MINIO_SECRET_KEY || 'minio@openspg'
    });

    const buckets = await minioClient.listBuckets();

    log(`✅ MinIO: CONNECTED (${buckets.length} buckets)`, 'green');
    return {
      service: 'MinIO',
      status: 'SUCCESS',
      details: `${buckets.length} buckets`,
      buckets: buckets.map(b => b.name),
      endpoint: process.env.MINIO_ENDPOINT
    };
  } catch (error) {
    log(`❌ MinIO: FAILED - ${error.message}`, 'red');
    return { service: 'MinIO', status: 'FAILED', error: error.message };
  }
}

async function main() {
  log('═══════════════════════════════════════════════', 'blue');
  log('  AEON UI - Backend Connection Verification', 'blue');
  log('═══════════════════════════════════════════════', 'blue');

  const results = [];

  // Run all tests
  results.push(await testNeo4j());
  results.push(await testQdrant());
  results.push(await testMySQL());
  results.push(await testMinIO());

  // Summary
  log('\n═══════════════════════════════════════════════', 'blue');
  log('  CONNECTION SUMMARY', 'blue');
  log('═══════════════════════════════════════════════', 'blue');

  const successful = results.filter(r => r.status === 'SUCCESS').length;
  const failed = results.filter(r => r.status === 'FAILED').length;

  results.forEach(result => {
    if (result.status === 'SUCCESS') {
      log(`✅ ${result.service}: ${result.details}`, 'green');
    } else {
      log(`❌ ${result.service}: ${result.error}`, 'red');
    }
  });

  log(`\n📊 Total: ${successful}/4 services connected`, successful === 4 ? 'green' : 'yellow');

  if (failed > 0) {
    log(`\n⚠️  ${failed} service(s) need attention`, 'yellow');
    process.exit(1);
  } else {
    log('\n🎉 All backend services are operational!', 'green');
    process.exit(0);
  }
}

main().catch(error => {
  log(`\n💥 Verification failed: ${error.message}`, 'red');
  process.exit(1);
});
