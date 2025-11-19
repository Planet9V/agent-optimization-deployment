/**
 * GAP-003 Query Control API - Queries Endpoint
 *
 * File: app/api/query-control/queries/route.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: REST API for query listing and creation
 *
 * Endpoints:
 * - GET /api/query-control/queries - List all queries with state breakdown
 * - POST /api/query-control/queries - Create new query (placeholder)
 */

import { NextRequest, NextResponse } from 'next/server';
import { QueryControlService } from '@/lib/query-control/query-control-service';

// Singleton service instance
let serviceInstance: QueryControlService | null = null;

function getService(): QueryControlService {
  if (!serviceInstance) {
    serviceInstance = new QueryControlService();
  }
  return serviceInstance;
}

/**
 * GET /api/query-control/queries
 * List all active queries with state breakdown
 *
 * Query Parameters:
 * - state?: QueryState - Filter by state (optional)
 * - limit?: number - Max results (default: 100)
 * - offset?: number - Pagination offset (default: 0)
 *
 * Returns:
 * {
 *   queries: QueryInfo[],
 *   total: number,
 *   states: Record<QueryState, number>
 * }
 */
export async function GET(request: NextRequest) {
  try {
    const service = getService();
    const searchParams = request.nextUrl.searchParams;

    // Parse query parameters
    const stateFilter = searchParams.get('state');
    const limit = parseInt(searchParams.get('limit') || '100');
    const offset = parseInt(searchParams.get('offset') || '0');

    // Get all queries
    const result = service.listQueries();

    // Apply state filter if provided
    let filteredQueries = result.queries || [];
    if (stateFilter && filteredQueries.length > 0) {
      filteredQueries = filteredQueries.filter(q => q.state === stateFilter);
    }

    // Apply pagination
    const paginatedQueries = filteredQueries.slice(offset, offset + limit);

    return NextResponse.json({
      queries: paginatedQueries,
      total: filteredQueries.length,
      states: result.states,
      pagination: {
        limit,
        offset,
        hasMore: offset + limit < filteredQueries.length
      }
    });
  } catch (error) {
    console.error('Error listing queries:', error);
    return NextResponse.json(
      {
        error: 'Failed to list queries',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

/**
 * POST /api/query-control/queries
 * Create a new query (placeholder for future implementation)
 *
 * Body:
 * {
 *   prompt: string,
 *   model?: ModelType,
 *   permissionMode?: PermissionMode
 * }
 *
 * Returns:
 * {
 *   queryId: string,
 *   state: QueryState,
 *   message: string
 * }
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Placeholder implementation - in real system, this would:
    // 1. Validate request body
    // 2. Create new query in service
    // 3. Initialize state machine
    // 4. Return query ID

    return NextResponse.json({
      queryId: `query_${Date.now()}`,
      state: 'INIT',
      message: 'Query creation placeholder - not yet implemented',
      note: 'This is a placeholder for future query creation functionality'
    }, { status: 501 }); // 501 Not Implemented
  } catch (error) {
    console.error('Error creating query:', error);
    return NextResponse.json(
      {
        error: 'Failed to create query',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
