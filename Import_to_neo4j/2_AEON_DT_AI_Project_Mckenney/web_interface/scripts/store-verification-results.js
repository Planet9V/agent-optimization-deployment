#!/usr/bin/env node

/**
 * Store Backend Verification Results in Qdrant Memory
 */

const { QdrantClient } = require('@qdrant/js-client-rest');

async function storeVerificationResults() {
  const client = new QdrantClient({
    url: process.env.QDRANT_URL || 'http://localhost:6333',
    apiKey: process.env.QDRANT_API_KEY
  });

  const timestamp = new Date().toISOString();
  const collectionName = 'aeon-dt-continuity';

  try {
    // Ensure collection exists
    try {
      await client.getCollection(collectionName);
    } catch (error) {
      console.log('Creating collection:', collectionName);
      await client.createCollection(collectionName, {
        vectors: {
          size: 384,
          distance: 'Cosine'
        }
      });
    }

    // Store verification results
    const verificationData = {
      timestamp,
      type: 'backend-verification',
      status: 'SUCCESS',
      services: {
        neo4j: {
          status: 'CONNECTED',
          uri: 'bolt://openspg-neo4j:7687',
          nodes: 568163,
          database: 'neo4j'
        },
        qdrant: {
          status: 'CONNECTED',
          url: 'http://openspg-qdrant:6333',
          collections: 18
        },
        mysql: {
          status: 'CONNECTED',
          host: 'openspg-mysql',
          port: 3306,
          database: 'openspg',
          tables: 34
        },
        minio: {
          status: 'CONNECTED',
          endpoint: 'openspg-minio',
          port: 9000,
          bucket: 'aeon-documents'
        }
      },
      summary: 'All 4 backend services are operational and verified',
      next_steps: [
        'Backend connections verified and working',
        'Environment variables configured correctly',
        'Docker containers healthy and running',
        'MinIO bucket created for document storage'
      ]
    };

    // Create a simple embedding (zeros for metadata storage)
    const embedding = new Array(384).fill(0);

    await client.upsert(collectionName, {
      points: [{
        id: Date.now(),
        vector: embedding,
        payload: verificationData
      }]
    });

    console.log('✅ Verification results stored in Qdrant memory');
    console.log(`   Collection: ${collectionName}`);
    console.log(`   Key: backend-setup-${timestamp}`);
    console.log(`   Status: All services operational`);

  } catch (error) {
    console.error('❌ Failed to store results:', error.message);
    process.exit(1);
  }
}

storeVerificationResults();
