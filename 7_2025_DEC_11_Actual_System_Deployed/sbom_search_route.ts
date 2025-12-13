import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getQdrantClient } from '@/lib/qdrant';

/**
 * POST /api/v2/sbom/components/search
 * Semantic search for SBOM components using Qdrant
 *
 * ICE Score: 7.29
 * Multi-tenant isolation via X-Customer-ID header
 */

interface ComponentSearchRequest {
  query: string;
  limit?: number;
  similarity_threshold?: number;
}

export async function POST(request: NextRequest) {
  try {
    // Validate customer ID
    const customerId = request.headers.get('X-Customer-ID');
    if (!customerId) {
      return NextResponse.json(
        { error: 'X-Customer-ID header is required' },
        { status: 401 }
      );
    }

    const body: ComponentSearchRequest = await request.json();
    const { query, limit = 10, similarity_threshold = 0.7 } = body;

    if (!query) {
      return NextResponse.json(
        { error: 'query is required' },
        { status: 400 }
      );
    }

    try {
      const qdrant = getQdrantClient();
      const collectionName = 'sbom_components';

      // Search with customer_id filter
      const searchResults = await qdrant.search(collectionName, {
        vector: Array(384).fill(0), // Placeholder - use actual embedding service
        limit,
        filter: {
          must: [
            {
              key: 'customer_id',
              match: { value: customerId }
            }
          ]
        },
        score_threshold: similarity_threshold
      });

      // Map results to response format
      const results = searchResults.map((hit: any) => ({
        component_id: hit.payload.component_id,
        name: hit.payload.name,
        version: hit.payload.version,
        sbom_id: hit.payload.sbom_id,
        project_name: hit.payload.project_name,
        similarity_score: hit.score,
        vulnerabilities_count: 0 // TODO: Query Neo4j for vulnerability count
      }));

      return NextResponse.json({
        results,
        total_results: results.length,
        query,
        customer_id: customerId
      });

    } catch (qdrantError) {
      console.error('Qdrant search error:', qdrantError);
      return NextResponse.json(
        {
          error: 'Component search failed',
          message: qdrantError instanceof Error ? qdrantError.message : 'Qdrant error'
        },
        { status: 500 }
      );
    }

  } catch (error) {
    console.error('Search route error:', error);
    return NextResponse.json(
      {
        error: 'Component search failed',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
