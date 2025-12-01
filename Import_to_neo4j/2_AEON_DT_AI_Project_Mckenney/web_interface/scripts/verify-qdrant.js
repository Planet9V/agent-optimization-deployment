const { QdrantClient } = require('@qdrant/js-client-rest');

const client = new QdrantClient({
  url: process.env.QDRANT_URL || 'http://localhost:6333',
  apiKey: process.env.QDRANT_API_KEY
});

async function verify() {
  try {
    const collections = await client.getCollections();
    console.log('✅ Qdrant is accessible');
    console.log('📊 Available collections:');
    collections.collections.forEach(c => {
      const vectorCount = c.vectors_count || 0;
      console.log(`   - ${c.name} (${vectorCount} vectors)`);
    });

    const exists = collections.collections.some(c => c.name === 'aeon-dt-continuity');
    if (exists) {
      console.log('\n✅ Collection "aeon-dt-continuity" EXISTS');
      console.log('   Test results can be stored here.');
    } else {
      console.log('\n⚠️  Collection "aeon-dt-continuity" NOT FOUND');
    }
  } catch (error) {
    console.log('❌ Qdrant not accessible:', error.message);
    console.log('   Test results preserved in local files.');
  }
}

verify();
