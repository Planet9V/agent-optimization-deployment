/**
 * Qdrant Vector Database Client
 * Singleton pattern for vector search and semantic queries
 */

import { QdrantClient } from '@qdrant/js-client-rest';

let qdrantClient: QdrantClient | null = null;

export function getQdrantClient(): QdrantClient {
  if (!qdrantClient) {
    const url = process.env.QDRANT_URL || 'http://openspg-qdrant:6333';
    const apiKey = process.env.QDRANT_API_KEY;

    qdrantClient = new QdrantClient({
      url,
      apiKey: apiKey || undefined,
    });

    console.log('✅ Qdrant client initialized:', url);
  }

  return qdrantClient;
}

export async function testQdrantConnection(): Promise<boolean> {
  try {
    const client = getQdrantClient();
    const collections = await client.getCollections();
    console.log('✅ Qdrant connected. Collections:', collections.collections.length);
    return true;
  } catch (error) {
    console.error('❌ Qdrant connection failed:', error);
    return false;
  }
}

export interface VectorSearchParams {
  collectionName: string;
  vector: number[];
  limit?: number;
  scoreThreshold?: number;
  filter?: Record<string, any>;
}

export async function vectorSearch(params: VectorSearchParams) {
  const client = getQdrantClient();
  const { collectionName, vector, limit = 10, scoreThreshold = 0.7, filter } = params;

  try {
    const searchResult = await client.search(collectionName, {
      vector,
      limit,
      score_threshold: scoreThreshold,
      filter: filter || undefined,
      with_payload: true,
      with_vector: false,
    });

    return {
      success: true,
      results: searchResult,
      count: searchResult.length,
    };
  } catch (error) {
    console.error('Vector search error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      results: [],
      count: 0,
    };
  }
}

export async function listCollections() {
  const client = getQdrantClient();

  try {
    const collections = await client.getCollections();
    return {
      success: true,
      collections: collections.collections,
      count: collections.collections.length,
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      collections: [],
      count: 0,
    };
  }
}

export function closeQdrantClient(): void {
  if (qdrantClient) {
    qdrantClient = null;
    console.log('Qdrant client closed');
  }
}

export default {
  getQdrantClient,
  testQdrantConnection,
  vectorSearch,
  listCollections,
  closeQdrantClient,
};
