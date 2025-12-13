#!/usr/bin/env ts-node

/**
 * Qdrant Storage Integration for API Test Results
 * Stores comprehensive test results in Qdrant for analysis
 */

import { QdrantClient } from '@qdrant/js-client-rest';
import * as fs from 'fs';
import * as path from 'path';

interface TestResult {
  category: string;
  endpoint: string;
  method: string;
  url: string;
  status: 'PASS' | 'FAIL' | 'ERROR';
  http_status?: number;
  response_time?: number;
  error?: string;
  response_schema?: any;
  timestamp: string;
}

interface QdrantPoint {
  id: string;
  vector: number[];
  payload: any;
}

class QdrantAPITestStorage {
  private client: QdrantClient;
  private collectionName: string = 'api_test_results';

  constructor(url: string = 'http://localhost:6333') {
    this.client = new QdrantClient({ url });
  }

  /**
   * Initialize Qdrant collection
   */
  async initializeCollection(): Promise<void> {
    try {
      // Check if collection exists
      const collections = await this.client.getCollections();
      const exists = collections.collections.some(c => c.name === this.collectionName);

      if (!exists) {
        console.log(`Creating collection: ${this.collectionName}`);
        await this.client.createCollection(this.collectionName, {
          vectors: {
            size: 384, // For text embeddings
            distance: 'Cosine'
          }
        });
        console.log('✅ Collection created');
      } else {
        console.log('✅ Collection already exists');
      }
    } catch (error) {
      console.error('Error initializing collection:', error);
      throw error;
    }
  }

  /**
   * Generate simple vector embedding from test result
   * In production, use a proper embedding model
   */
  private generateEmbedding(result: TestResult): number[] {
    // Simple hash-based embedding for demonstration
    // In production, use sentence-transformers or similar

    const text = `${result.category} ${result.endpoint} ${result.method} ${result.status}`;
    const vector = new Array(384).fill(0);

    // Simple character-based encoding
    for (let i = 0; i < text.length; i++) {
      const charCode = text.charCodeAt(i);
      const idx = (charCode * i) % 384;
      vector[idx] = (vector[idx] + charCode) / 256;
    }

    // Normalize
    const magnitude = Math.sqrt(vector.reduce((sum, val) => sum + val * val, 0));
    return magnitude > 0 ? vector.map(v => v / magnitude) : vector;
  }

  /**
   * Store test results in Qdrant
   */
  async storeResults(results: TestResult[]): Promise<void> {
    console.log(`\n📦 Storing ${results.length} test results in Qdrant...`);

    const points: QdrantPoint[] = results.map((result, idx) => ({
      id: `test-${Date.now()}-${idx}`,
      vector: this.generateEmbedding(result),
      payload: {
        ...result,
        test_run_id: Date.now().toString(),
        stored_at: new Date().toISOString()
      }
    }));

    // Store in batches
    const batchSize = 100;
    for (let i = 0; i < points.length; i += batchSize) {
      const batch = points.slice(i, i + batchSize);
      await this.client.upsert(this.collectionName, {
        wait: true,
        points: batch
      });
      console.log(`  Stored batch ${Math.floor(i / batchSize) + 1}/${Math.ceil(points.length / batchSize)}`);
    }

    console.log('✅ All results stored in Qdrant');
  }

  /**
   * Query test results by category
   */
  async queryByCategory(category: string, limit: number = 10): Promise<any[]> {
    const results = await this.client.scroll(this.collectionName, {
      filter: {
        must: [
          {
            key: 'category',
            match: { value: category }
          }
        ]
      },
      limit,
      with_payload: true,
      with_vector: false
    });

    return results.points.map(p => p.payload);
  }

  /**
   * Query failed tests
   */
  async queryFailedTests(limit: number = 50): Promise<any[]> {
    const results = await this.client.scroll(this.collectionName, {
      filter: {
        should: [
          {
            key: 'status',
            match: { value: 'FAIL' }
          },
          {
            key: 'status',
            match: { value: 'ERROR' }
          }
        ]
      },
      limit,
      with_payload: true,
      with_vector: false
    });

    return results.points.map(p => p.payload);
  }

  /**
   * Get test statistics
   */
  async getTestStatistics(): Promise<any> {
    const allResults = await this.client.scroll(this.collectionName, {
      limit: 10000,
      with_payload: true,
      with_vector: false
    });

    const points = allResults.points.map(p => p.payload as TestResult);

    const stats = {
      total_tests: points.length,
      passed: points.filter(p => p.status === 'PASS').length,
      failed: points.filter(p => p.status === 'FAIL').length,
      errors: points.filter(p => p.status === 'ERROR').length,
      by_category: {} as Record<string, any>,
      avg_response_time: 0
    };

    // Calculate average response time
    const responseTimes = points
      .filter(p => p.response_time !== undefined)
      .map(p => p.response_time!);

    stats.avg_response_time = responseTimes.length > 0
      ? Math.round(responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length)
      : 0;

    // Statistics by category
    const categories = [...new Set(points.map(p => p.category))];
    for (const category of categories) {
      const categoryPoints = points.filter(p => p.category === category);
      stats.by_category[category] = {
        total: categoryPoints.length,
        passed: categoryPoints.filter(p => p.status === 'PASS').length,
        failed: categoryPoints.filter(p => p.status === 'FAIL').length,
        errors: categoryPoints.filter(p => p.status === 'ERROR').length
      };
    }

    return stats;
  }

  /**
   * Search for similar test results
   */
  async searchSimilar(query: string, limit: number = 5): Promise<any[]> {
    // Create a dummy result for embedding generation
    const dummyResult: TestResult = {
      category: query,
      endpoint: '',
      method: 'GET',
      url: '',
      status: 'PASS',
      timestamp: new Date().toISOString()
    };

    const queryVector = this.generateEmbedding(dummyResult);

    const results = await this.client.search(this.collectionName, {
      vector: queryVector,
      limit,
      with_payload: true
    });

    return results.map(r => ({
      score: r.score,
      ...r.payload
    }));
  }
}

// CLI Interface
async function main() {
  const args = process.argv.slice(2);
  const qdrantUrl = process.env.QDRANT_URL || 'http://localhost:6333';

  const storage = new QdrantAPITestStorage(qdrantUrl);

  try {
    await storage.initializeCollection();

    if (args[0] === 'store') {
      // Store results from JSON file
      const resultsPath = args[1] || path.join(__dirname, 'results', 'latest-results.json');

      if (!fs.existsSync(resultsPath)) {
        console.error(`Results file not found: ${resultsPath}`);
        process.exit(1);
      }

      const results = JSON.parse(fs.readFileSync(resultsPath, 'utf-8'));
      await storage.storeResults(results);

    } else if (args[0] === 'query') {
      const category = args[1];
      if (!category) {
        console.error('Category required for query');
        process.exit(1);
      }

      const results = await storage.queryByCategory(category);
      console.log(JSON.stringify(results, null, 2));

    } else if (args[0] === 'stats') {
      const stats = await storage.getTestStatistics();
      console.log('\n📊 Test Statistics:');
      console.log(JSON.stringify(stats, null, 2));

    } else if (args[0] === 'failed') {
      const failed = await storage.queryFailedTests();
      console.log(`\n❌ Failed Tests (${failed.length}):`);
      console.log(JSON.stringify(failed, null, 2));

    } else {
      console.log('Usage:');
      console.log('  Store results:    npx ts-node qdrant-storage.ts store [results-file.json]');
      console.log('  Query category:   npx ts-node qdrant-storage.ts query <category>');
      console.log('  Get statistics:   npx ts-node qdrant-storage.ts stats');
      console.log('  Get failed tests: npx ts-node qdrant-storage.ts failed');
    }
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

export { QdrantAPITestStorage };
