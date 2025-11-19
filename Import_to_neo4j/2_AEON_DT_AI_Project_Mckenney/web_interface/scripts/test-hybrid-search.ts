#!/usr/bin/env ts-node

/**
 * Test script for hybrid search functionality
 * Tests Neo4j full-text search, Qdrant semantic search, and RRF merging
 */

import { hybridSearch, checkSearchHealth, createFullTextIndex } from '../lib/hybrid-search';

async function testHealthCheck() {
  console.log('\n=== Testing Search Services Health ===');
  try {
    const health = await checkSearchHealth();
    console.log('Health Status:', health);

    if (!health.neo4j) {
      console.error('❌ Neo4j is not available');
    } else {
      console.log('✅ Neo4j is healthy');
    }

    if (!health.qdrant) {
      console.error('❌ Qdrant is not available');
    } else {
      console.log('✅ Qdrant is healthy');
    }

    if (!health.openai) {
      console.error('❌ OpenAI is not available');
    } else {
      console.log('✅ OpenAI is healthy');
    }

    return health;
  } catch (error) {
    console.error('Health check failed:', error);
    return { neo4j: false, qdrant: false, openai: false };
  }
}

async function testFullTextSearch() {
  console.log('\n=== Testing Full-Text Search ===');
  try {
    const results = await hybridSearch({
      query: 'requirements documentation',
      mode: 'fulltext',
      limit: 5,
    });

    console.log(`Found ${results.length} results`);
    results.forEach((result, idx) => {
      console.log(`\n${idx + 1}. ${result.title} (Score: ${result.score.toFixed(4)})`);
      console.log(`   Type: ${result.type} | Source: ${result.source}`);
      console.log(`   Content: ${result.content.substring(0, 100)}...`);
    });

    return results.length > 0;
  } catch (error) {
    console.error('Full-text search failed:', error);
    return false;
  }
}

async function testSemanticSearch() {
  console.log('\n=== Testing Semantic Search ===');
  try {
    const results = await hybridSearch({
      query: 'project specifications and design documents',
      mode: 'semantic',
      limit: 5,
    });

    console.log(`Found ${results.length} results`);
    results.forEach((result, idx) => {
      console.log(`\n${idx + 1}. ${result.title} (Score: ${result.score.toFixed(4)})`);
      console.log(`   Type: ${result.type} | Source: ${result.source}`);
      console.log(`   Content: ${result.content.substring(0, 100)}...`);
    });

    return results.length > 0;
  } catch (error) {
    console.error('Semantic search failed:', error);
    return false;
  }
}

async function testHybridSearch() {
  console.log('\n=== Testing Hybrid Search (RRF) ===');
  try {
    const results = await hybridSearch({
      query: 'system architecture and technical requirements',
      mode: 'hybrid',
      limit: 10,
    });

    console.log(`Found ${results.length} results (merged with RRF)`);
    results.forEach((result, idx) => {
      console.log(`\n${idx + 1}. ${result.title} (RRF Score: ${result.score.toFixed(4)})`);
      console.log(`   Type: ${result.type} | Source: ${result.source}`);
      console.log(`   Content: ${result.content.substring(0, 100)}...`);
    });

    return results.length > 0;
  } catch (error) {
    console.error('Hybrid search failed:', error);
    return false;
  }
}

async function testFiltering() {
  console.log('\n=== Testing Search with Filters ===');
  try {
    const results = await hybridSearch({
      query: 'documentation',
      mode: 'hybrid',
      filters: {
        customer: 'ACME Corp',
        tags: ['requirements', 'specification'],
      },
      limit: 5,
    });

    console.log(`Found ${results.length} filtered results`);
    results.forEach((result, idx) => {
      console.log(`\n${idx + 1}. ${result.title}`);
      console.log(`   Customer: ${result.metadata.customer}`);
      console.log(`   Tags: ${result.metadata.tags?.join(', ')}`);
    });

    return true;
  } catch (error) {
    console.error('Filtered search failed:', error);
    return false;
  }
}

async function setupIndexes() {
  console.log('\n=== Setting Up Full-Text Indexes ===');
  try {
    await createFullTextIndex();
    console.log('✅ Full-text index created successfully');
    return true;
  } catch (error) {
    console.error('❌ Index creation failed:', error);
    return false;
  }
}

async function main() {
  console.log('🔍 Hybrid Search Test Suite');
  console.log('============================');

  const results = {
    health: false,
    indexes: false,
    fulltext: false,
    semantic: false,
    hybrid: false,
    filtering: false,
  };

  // 1. Health check
  const health = await testHealthCheck();
  results.health = health.neo4j && health.qdrant && health.openai;

  if (!results.health) {
    console.error('\n❌ Some services are not available. Please check your configuration.');
    console.log('\nRequired environment variables:');
    console.log('- NEO4J_URI (default: bolt://localhost:7687)');
    console.log('- NEO4J_USER (default: neo4j)');
    console.log('- NEO4J_PASSWORD (default: neo4j@openspg)');
    console.log('- QDRANT_URL (default: http://localhost:6333)');
    console.log('- QDRANT_API_KEY');
    console.log('- OPENAI_API_KEY');
    process.exit(1);
  }

  // 2. Setup indexes
  results.indexes = await setupIndexes();

  // 3. Test full-text search
  if (health.neo4j) {
    results.fulltext = await testFullTextSearch();
  }

  // 4. Test semantic search
  if (health.qdrant && health.openai) {
    results.semantic = await testSemanticSearch();
  }

  // 5. Test hybrid search
  if (health.neo4j && health.qdrant && health.openai) {
    results.hybrid = await testHybridSearch();
  }

  // 6. Test filtering
  results.filtering = await testFiltering();

  // Summary
  console.log('\n=== Test Summary ===');
  console.log(`Health Check:      ${results.health ? '✅' : '❌'}`);
  console.log(`Index Setup:       ${results.indexes ? '✅' : '❌'}`);
  console.log(`Full-Text Search:  ${results.fulltext ? '✅' : '❌'}`);
  console.log(`Semantic Search:   ${results.semantic ? '✅' : '❌'}`);
  console.log(`Hybrid Search:     ${results.hybrid ? '✅' : '❌'}`);
  console.log(`Filtered Search:   ${results.filtering ? '✅' : '❌'}`);

  const allPassed = Object.values(results).every(r => r === true);
  console.log(`\n${allPassed ? '✅ All tests passed!' : '❌ Some tests failed'}`);

  process.exit(allPassed ? 0 : 1);
}

// Run tests
main().catch(error => {
  console.error('Test suite failed:', error);
  process.exit(1);
});
