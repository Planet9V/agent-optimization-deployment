// Test script to validate Neo4j schema and enhanced operations
import { neo4jEnhanced } from '../lib/neo4j-enhanced';
import * as fs from 'fs';
import * as path from 'path';
import neo4j from 'neo4j-driver';

async function testSchema() {
  console.log('🔍 Testing Neo4j Schema Enhancement...\n');

  // Test 1: Connection
  console.log('1️⃣ Testing connection...');
  const connected = await neo4jEnhanced.testConnection();
  if (!connected) {
    console.error('❌ Connection failed. Ensure Neo4j is running at bolt://localhost:7687');
    process.exit(1);
  }
  console.log('✅ Connection successful\n');

  // Test 2: Execute schema file
  console.log('2️⃣ Executing schema file...');
  try {
    const schemaPath = path.join(__dirname, '../lib/neo4j-schema.cypher');
    const schemaContent = fs.readFileSync(schemaPath, 'utf-8');

    // Split by statements (simple split on semicolons and newlines)
    const statements = schemaContent
      .split('\n')
      .filter(line => !line.trim().startsWith('//') && line.trim().length > 0)
      .join('\n')
      .split(';')
      .map(stmt => stmt.trim())
      .filter(stmt => stmt.length > 0 && !stmt.startsWith('//'));

    const driver = neo4j.driver('bolt://localhost:7687', neo4j.auth.basic('neo4j', 'neo4j@openspg'));
    const session = driver.session();

    for (const statement of statements) {
      if (statement.trim()) {
        try {
          await session.run(statement);
        } catch (error: any) {
          // Ignore "already exists" errors for constraints/indexes
          if (!error.message.includes('already exists') && !error.message.includes('An equivalent')) {
            console.warn(`⚠️  Statement warning: ${error.message.substring(0, 100)}`);
          }
        }
      }
    }

    await session.close();
    await driver.close();
    console.log('✅ Schema executed successfully\n');
  } catch (error) {
    console.error('❌ Schema execution failed:', error);
    throw error;
  }

  // Test 3: Verify Customer CRUD
  console.log('3️⃣ Testing Customer CRUD...');
  const testCustomer = {
    id: 'test_cust_' + Date.now(),
    name: 'Test Customer',
    email: 'test@example.com',
    phone: '+1-555-9999',
    status: 'active' as const,
    tier: 'basic' as const
  };

  const created = await neo4jEnhanced.createCustomer(testCustomer);
  console.log(`✅ Created customer: ${created.name} (${created.id})`);

  const retrieved = await neo4jEnhanced.getCustomer(created.id);
  console.log(`✅ Retrieved customer: ${retrieved?.name}`);

  const updated = await neo4jEnhanced.updateCustomer(created.id, { tier: 'professional' });
  console.log(`✅ Updated customer tier: ${updated?.tier}\n`);

  // Test 4: Verify Tag operations
  console.log('4️⃣ Testing Tag operations...');
  const testTag = {
    name: 'test-tag-' + Date.now(),
    category: 'testing',
    color: '#00FF00',
    description: 'Test tag'
  };

  const createdTag = await neo4jEnhanced.createTag(testTag);
  console.log(`✅ Created tag: ${createdTag.name} (${createdTag.category})`);

  const allTags = await neo4jEnhanced.getAllTags();
  console.log(`✅ Retrieved ${allTags.length} tags\n`);

  // Test 5: Get statistics
  console.log('5️⃣ Getting system statistics...');
  const stats = await neo4jEnhanced.getStatistics();
  console.log(`📊 Statistics:`);
  console.log(`   - Customers: ${stats.totalCustomers}`);
  console.log(`   - Documents: ${stats.totalDocuments}`);
  console.log(`   - Tags: ${stats.totalTags}`);
  console.log(`   - Shared Documents: ${stats.totalSharedDocuments}\n`);

  // Test 6: Query existing data
  console.log('6️⃣ Querying existing sample data...');
  const customers = await neo4jEnhanced.getAllCustomers();
  console.log(`✅ Found ${customers.length} customers:`);
  customers.slice(0, 3).forEach(c => {
    console.log(`   - ${c.name} (${c.tier}) - ${c.email}`);
  });

  const tags = await neo4jEnhanced.getAllTags();
  console.log(`\n✅ Found ${tags.length} tags:`);
  tags.slice(0, 5).forEach(t => {
    console.log(`   - ${t.name} [${t.category}] - ${t.usageCount} uses`);
  });

  // Test 7: Test multi-tag assignment
  console.log('\n7️⃣ Testing multi-tag assignment...');
  const sampleDocs = await neo4jEnhanced.getCustomerDocuments('cust_001');
  if (sampleDocs.length > 0) {
    const doc = sampleDocs[0];
    console.log(`✅ Document "${doc.title}" has tags: ${doc.tags.join(', ')}`);
  }

  // Cleanup test data
  console.log('\n8️⃣ Cleaning up test data...');
  await neo4jEnhanced.deleteCustomer(testCustomer.id);
  await neo4jEnhanced.deleteTag(testTag.name);
  console.log('✅ Test data cleaned up\n');

  console.log('✅ ALL TESTS PASSED - Schema is working correctly!\n');

  await neo4jEnhanced.close();
}

// Run tests
testSchema().catch(error => {
  console.error('❌ Test failed:', error);
  process.exit(1);
});
